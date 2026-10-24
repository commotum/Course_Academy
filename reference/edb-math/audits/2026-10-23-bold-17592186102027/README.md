# Literal bold markers in tutorial 17592186102027

Read-only investigation of database `math` at T6225. This is tutorial 840, “Introduction,” in lesson 1159 (integration by substitution for definite integrals).

## Confirmed cause

The original captured HTML has `<strong> Step 1</strong>` and `<strong> Step 2</strong>`, but `<strong>Step 3</strong>`. Whitespace inside HTML emphasis is legal. Converting that HTML by concatenating `**` + children + `**` produces `** Step 1**` and `** Step 2**`. Those opening delimiters cannot open Markdown emphasis because they are followed by whitespace. The player therefore correctly displays their stars literally.

The legacy converter in `scripts/import_historical_question_content.py:158` reproduces those exact strings from the saved HTML. Its italic branch has the same whitespace-handling weakness. The staged `reference/edb-math/imports/math-academy/newer-captures/tutorials.json` contains the same malformed tutorial text and identifies `reference/mathacademy/question-capture/14004889/tutorial-840.html` as its source. The current capture converter in `capture/scripts/database/text.py` already trims emphasis bodies, but that does not repair existing database values or the legacy converter.

## Retained history

`history.jsonl` shows valid bold labels in the initial T44 content. T127 replaced that text with the malformed labels. T5769, the later display-integral repair, preserved the preexisting malformed labels. Thus this regression entered with the replacement import, before the integral formatting repair.

## Renderer verification

`reproduce.py` exercises the actual player Markdown function with its installed marked parser and sanitization. `reproduction.json` records:

- Stored text produces only one bold label: Step 3. Steps 1 and 2 retain literal stars.
- An in-memory change of `** Step 1**` to `**Step 1**` and likewise Step 2 produces three `<strong>` labels.

A repair should normalize whitespace at confirmed emphasis boundaries, keeping necessary word separation outside the delimiters. Importers should apply that rule during HTML-to-Markdown conversion. A broad replacement of every `** ` would be unsafe because the same character sequence can occur after a valid closing delimiter.

No database changes or application-code changes were made by this investigation.
