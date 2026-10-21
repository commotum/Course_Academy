# Source-link coverage for the live brace inventory

This joins all 1,688 current malformed text attributes (1,615 entities) to saved import/capture evidence by stable Math Academy source identity. It does not render every source or certify every original formula visually.

| Best evidence found | Attributes |
| --- | ---: |
| Exact match to saved capture record |457|
| Exact match to saved newer import record |257|
| Exact match to rendered original source JSON |61|
| Match after only U+2061 cleanup and whitespace collapse |4|
| Stable source identity linked, text does not match exactly |799|
| No link found in the bounded source corpora |110|

There are 775 byte-for-byte matches and 4 limited-normalization matches. “No link found” means only that this join did not locate one in the datasets below; it does not establish that no original source exists. Those 110 attributes represent 99 source IDs.

Sources examined:

- Newer-import `questions-with-local-images.json`, `source-occurrences.json`, and `tutorials.json`.
- The original archived source census's 268 items whose normalized JSON contains malformed brace glyphs. Tutorial/example/question rendering used the real MA Markdown renderer, preserving source image paths rather than guessing hashed image mappings.
- A bounded 928 `content.json` or `history-content.json` files under `reference/mathacademy` containing literal brace glyphs, with matching `questions`, `canonical_examples`, or `tutorials` records. Every selected file parsed successfully.

For matching saved capture records with an embedded `html` field, the audit also inspected the corresponding question, solution, or tutorial DOM container for MathML `munder`/`mover` nodes whose decoration child is ⏟/⏞. That found raw brace-node evidence for 220 current attributes, of which 88 also have an exact or limited-normalization text match in the same saved capture. This check covers only the embedded HTML that was present and the supported field-container selectors. It does not exhaust separate observation files, complete HTML snapshots, or all captured solution structures; an absent result is not evidence of absent source MathML.

`source-links.json` supplies one row per current attribute: entity ID, attribute, stable source identity, current value SHA-256, match class, source record path and index, source/capture paths, archived selectors where available, and raw MathML check results. `source-link-summary.json` supplies exact totals and missing source IDs. The internal version additionally retains current text for reproducibility.

Normalizing comparison was deliberately narrow: remove actual U+2061 and literal backslash-u2061, then collapse whitespace. It does not alter brace syntax, simplify equations, or conflate function notation. Identity-only records may differ because of later converter improvements, image-path remapping, content edits, or later capture changes; these reasons were not individually established in this bounded join.
