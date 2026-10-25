# Sermon term review kit

Prepare the words that need discussion before a multilingual service, then record what actually went wrong during a rehearsal. This offline kit gives a speaker, a language reviewer, and an audio volunteer a shared record. It supplies no translations or theological definitions.

The kit is original, AI-assisted preparation material. Its English examples are constructed teaching cases, not recordings, model outputs, field trials, or evidence of translation accuracy. A church decides its own terminology with people competent in the language and its context.

## Start with one passage of your own material

1. Copy `templates/term-register.csv` into a private working folder. Choose the actual source language, target language, and relevant language variety with the people who will use the material.
2. Read the speaker's outline. Use `data/review-prompts.csv` to find names, references, ambiguous words, and expressions that need discussion. Add only terms present in the material; the prompt list is not a mandatory vocabulary.
3. Write each term's complete sentence, intended meaning, and where a reviewer can check it. Ask the speaker about unclear meaning. Do not guess a definition from the word alone.
4. Ask a competent language reviewer to propose and review wording in context. Record a role identifier, date, and reason for the choice. Leave the approved wording empty and use `PENDING` or `BLOCKED` when the review has not happened. A machine suggestion is a proposal.
5. Rehearse with the planned audio and support method. Use `checklists/review-and-rehearse.md` and record failures in `templates/issue-log.csv`. Distinguish what was said, what was transcribed, and what a listener received.
6. Keep a dated copy for the service team. Reopen affected entries when the sermon, wording, language variety, or support system changes. Keep recordings, people’s names, and private pastoral material out of a public repository.

The register is a team worksheet, not an import format for a translation service. No account, paid tool, or PewTranslate feature is needed to use it. Download the folder and open the CSV files as UTF-8 with comma separators, or write the headings on paper. Let a spreadsheet save quoting; do not add formulas to shared cells.

## Files and the job each one does

| File | Use |
| --- | --- |
| `data/review-prompts.csv` | Eighteen English terms or patterns with specific review questions, without suggested translations. |
| `data/diagnostic-cases.json` | Twelve fictional English-only cases for practicing error classification. Each includes an observable failure and a recheck. |
| `templates/term-register.csv` | Blank term register; one row per term, context, and language pair. |
| `templates/issue-log.csv` | Blank evidence and action log for rehearsal or service review. |
| `checklists/review-and-rehearse.md` | Observable PASS, FAIL, and NOT CHECKED criteria with a response to each failure. |
| `examples/unreviewed-register.csv` | Two fictional entries demonstrating honest incomplete states. Neither is approved. |
| `validate.py` | Offline file checks and an optional administrative readiness gate. It cannot judge meaning or reviewer competence. |

## Keep the stages separate

Human interpreting conveys spoken or signed communication between languages; written translation concerns text. The [American Translators Association explains the spoken/written distinction](https://www.atanet.org/client-assistance/translator-vs-interpreter/). A tool that transcribes audio, translates text, and reads text aloud is a different workflow. This kit does not certify either workflow or replace a competent interpreter.

In a speech-to-text-to-translation pipeline, compare the source transcript with the actual words first. A missing “not,” a wrong name, or a changed number can enter before translation. If the transcript is right but the target wording changes the intended meaning, ask the language reviewer to examine the translation and context. Without a source transcript or intelligible audio, mark the stage `UNKNOWN` instead of blaming a component.

[Deepgram's keyterm documentation](https://developers.deepgram.com/docs/keyterm) describes transcription vocabulary hints for supported models. [DeepL's glossary documentation](https://support.deepl.com/hc/en-us/articles/360021634540-About-the-glossary) describes preferred source/target word and phrase pairs. These are separate provider capabilities, subject to their current models, languages, plans, and integrations. This kit does not assume that a church's app exposes either feature. A term list is not evidence that a provider accepted it or that the resulting sentence is correct.

Captions also carry information beyond spoken words, including relevant sounds and speaker identification. W3C explains why [automatic captions need accuracy review](https://www.w3.org/WAI/media/av/captions/). A translated transcript alone is not evidence that a service meets a person's access needs. Ask people who use the support whether the format and corrections are usable; arrange a suitable alternative when they are not.

## Run the checks

With Python 3 installed, from this folder:

```sh
python validate.py
python validate.py --terms examples/unreviewed-register.csv
python validate.py --terms templates/term-register.csv --gate
```

The first two commands should pass file checks. The third should fail because a blank register is not a reviewed working plan. To check your local copy, replace the path with your own file. `--gate` requires nonempty approved records with review evidence; passing it proves only that the administrative fields are present, not linguistic accuracy, doctrinal agreement, service readiness, or accessibility.

## Ownership, sources, and reuse

Maintained by the PewTranslate project. Its public [preaching with live translation guide](https://pewtranslate.com/guides/preaching-with-live-translation/) gives broader preparation context. As checked on October 25, 2026, PewTranslate's public site says accounts are not open; this kit does not imply that signup, live translation, or payments are available.

Source pages above were checked on October 25, 2026. Their authors do not endorse this kit. Original kit files use the [MIT License](LICENSE); linked resources retain their own terms. No Bible passages, songs, third-party translations, or recordings are bundled.
