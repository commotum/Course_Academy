# Original lesson-source brace-accent census

Read-only source audit performed 2026-10-17/18. No EDB content or importer code changed.

## Scope and method

Scanned every original numbered source JSON and paired HTML under `/home/jake/Developer/MA/DATA/Lessons/*/Source/`: 2,964 JSON files and 2,964 HTML files, with no missing files or parse errors. For JSON, counted only `normalized_html` leaves, omitting mirrored `readable_text` and whole-item summaries. For original HTML, parsed actual MathML `<mo>` nodes, recorded their `munder`/`mover` parents and enclosing step/question DOM IDs, and compared occurrence counts to normalized source by topic, content item, and accent kind.

## Findings

The original rendered HTML contains 620 brace accents: 448 underbraces (`⏟` directly under `munder`) and 172 overbraces (`⏞` directly under `mover`). All 620 became literal ASCII sub/superscript expressions in normalized JSON: `_(⏟)` and `^(⏞)`. This comparison matches exactly for every source content item, not just in aggregate.

These affect 268 content items across 153 topics: 120 tutorials, 130 canonical examples, and 18 practice questions. The 287 affected normalized leaves represent those 268 items because 18 items have multiple affected sections, producing 19 additional leaves. The full item/MA-ID/topic/path mapping is in `affected-source-items.json` and `.tsv`; individual leaf contents and paths are in `normalized.json`.

There are no plain-language or ordinary brace character false positives in that set: every detected literal is inside a normalized math span, every literal has the specific `_(⏟)` or `^(⏞)` syntax, and every counterpart in the original HTML is a MathML accent under `munder` or `mover`. The original layout is available in each record's `mathml` and `math_source` fields in `original-html.json`.

A separate population already preserves valid TeX commands: 557 `\underbrace` and 65 `\overbrace` occurrences, 622 total, across 290 leaves in 157 topics. These are not alternative counts of the 620 corrupted occurrences. For example, the preserved underbrace in topic 1037 is present as TeX in a MathJax SVG `<title>` and survives into normalized JSON. Two individual leaves (topics 1458 and 3414) contain both preserved TeX in some expressions and damaged MathML-derived braces in other expressions. Across valid and corrupted populations together there are 575 leaves in 283 topics.

The alternate accent search decoded JSON and HTML entities in all 5,928 numbered source files. It found no instances of U+23B4 `⎴`, U+23B5 `⎵`, U+23DC `⏜`, U+23DD `⏝`, U+FE37 `︷`, or U+FE38 `︸`. The source archive's confirmed brace-accent defect is limited to U+23DF `⏟` and U+23DE `⏞`.

## Evidence and limits

- `census.py` performs the primary source scan and emits `normalized.json`, `original-html.json`, and `summary.json`.
- `summarize.py` verifies exact item-level reconciliation, rejects plain-text/non-math false positives, checks alternate accent glyphs, and emits `affected-source-items.json`, `affected-source-items.tsv`, and `verification.json`.
- This census concerns the original 2,964 archived lessons only. It does not assert that all 268 items remain damaged in current EDB: later captures or repairs can supersede original content, and newer captured questions can introduce additional affected items. The parent audit queries live EDB separately.
- Preserved brace commands are not proof that an entire expression has no unrelated formatting defect; legacy multiline TeX may have independent row-separator issues.
- A broad secondary scan of later capture directories was stopped before completion and contributes no counts to this report.
