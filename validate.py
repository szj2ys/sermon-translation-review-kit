"""Validate file structure, never the linguistic or theological correctness of text."""
import argparse
import csv
import datetime
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
TERM_FIELDS = ["term_id", "source_language", "target_language", "target_variety", "source_term", "sentence_context", "intended_sense", "evidence_location", "proposed_rendering", "review_status", "reviewer_role", "reviewed_on", "approved_rendering", "review_note"]
ISSUE_FIELDS = ["issue_id", "observed_at", "segment_reference", "spoken_words", "source_transcript", "target_output", "expected_meaning", "stage", "severity", "evidence_location", "action_owner", "next_action", "recheck_evidence", "status"]
PROMPT_FIELDS = ["id", "source_term", "category", "review_question", "pass_evidence", "fail_action"]
STAGES = {"INPUT_OR_ASR", "CONTEXT_REVIEW", "TRANSLATION", "PRESENTATION", "MULTIPLE", "UNKNOWN"}


def read_csv(path, fields):
    with path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != fields:
            raise ValueError(f"{path.name}: incorrect column headings")
        rows = list(reader)
    for number, row in enumerate(rows, 2):
        if None in row or any(value is None for value in row.values()):
            raise ValueError(f"{path.name}:{number}: incorrect column count")
        if any(value.lstrip().startswith(("=", "+", "-", "@")) for value in row.values()):
            raise ValueError(f"{path.name}:{number}: formula-like cell; convert to plain text before sharing")
    return rows


def check_terms(path, gate=False):
    rows = read_csv(path, TERM_FIELDS)
    seen = set()
    for row in rows:
        term_id = row["term_id"]
        if not term_id or term_id in seen:
            raise ValueError(f"{path.name}: empty or duplicate term_id")
        seen.add(term_id)
        for field in TERM_FIELDS[:8]:
            if not row[field].strip():
                raise ValueError(f"{term_id}: missing {field}")
        state = row["review_status"]
        if state not in {"PENDING", "BLOCKED", "APPROVED"}:
            raise ValueError(f"{term_id}: invalid review_status")
        if state != "APPROVED" and row["approved_rendering"].strip():
            raise ValueError(f"{term_id}: unapproved row has approved_rendering")
        if state == "APPROVED":
            for field in ["reviewer_role", "reviewed_on", "approved_rendering", "review_note"]:
                if not row[field].strip():
                    raise ValueError(f"{term_id}: approved row missing {field}")
            datetime.date.fromisoformat(row["reviewed_on"])
            for field in ["source_language", "target_language", "target_variety"]:
                if row[field].strip().upper() in {"UNDECIDED", "UNKNOWN", "TBD"}:
                    raise ValueError(f"{term_id}: approved row has unresolved {field}")
        if gate and state != "APPROVED":
            raise ValueError(f"{term_id}: {state}; administrative readiness gate failed")
    if gate and not rows:
        raise ValueError("empty register; administrative readiness gate failed")
    return len(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--terms", type=Path, help="Optional local term register to validate")
    parser.add_argument("--gate", action="store_true", help="Require approved nonempty records; does not judge meaning")
    args = parser.parse_args()
    if args.gate and args.terms is None:
        parser.error("--gate requires --terms")
    try:
        prompts = read_csv(ROOT / "data/review-prompts.csv", PROMPT_FIELDS)
        if len(prompts) != 18 or len({row["id"] for row in prompts}) != 18:
            raise ValueError("expected 18 uniquely identified review prompts")
        if any(not value.strip() for row in prompts for value in row.values()):
            raise ValueError("review prompt has an empty field")
        document = json.loads((ROOT / "data/diagnostic-cases.json").read_text(encoding="utf-8"))
        cases = document["cases"]
        if len(cases) != 12 or len({row["id"] for row in cases}) != 12:
            raise ValueError("expected 12 uniquely identified teaching cases")
        for row in cases:
            if row["expected_stage"] not in STAGES or row["severity"] not in {"MEANING", "COSMETIC", "UNRESOLVED"}:
                raise ValueError(f"{row['id']}: invalid stage or severity")
            if row["target_output"] is not None:
                raise ValueError(f"{row['id']}: this English-only kit must not supply unreviewed translations")
            for field in ["label", "observable_failure", "next_action", "pass_recheck"]:
                if not row[field].strip():
                    raise ValueError(f"{row['id']}: missing {field}")
        check_terms(ROOT / "templates/term-register.csv")
        read_csv(ROOT / "templates/issue-log.csv", ISSUE_FIELDS)
        check_terms(ROOT / "examples/unreviewed-register.csv")
        extra = check_terms(args.terms.resolve(), args.gate) if args.terms else None
        print(f"PASS: 18 prompts; 12 fictional English cases; two CSV templates; incomplete example preserved.")
        if extra is not None:
            print(f"PASS: {extra} local term rows; administrative gate {'enabled' if args.gate else 'disabled'}.")
        print("No linguistic, theological, accessibility, or live-service approval is implied.")
        return 0
    except (ValueError, KeyError, TypeError, OSError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
