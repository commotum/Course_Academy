# Hat-accent source audit and recovery

Two import paths mishandled MathML `mover` accents. The capture extractor and historical import renderer treated every `mover` as a generic `\overset`, producing `\overset{^}{BASE}`. TeX reads the unescaped caret as an incomplete superscript, so these formulas report “Missing superscript or subscript argument.” The older lesson JSON converter flattened the same structure into `BASE^(^)`, losing the original base boundary. Original source MathML supplies that boundary.

`importer-root-cause.json` preserves the relevant pre-repair code excerpts, repository revision, paths, and hashes. The separate legacy question-capture converter already recognized hats, but always emitted `\hat`, ignoring the source's wide-versus-narrow distinction.

The 20 errors first observed during the brace repair contain 375 malformed hat occurrences. All 375 have matching original source MathML in saved solution modals. The saved capture records exactly match their pre-brace database texts. All 375 source caret operators have no attributes and use a wide hat. `seed-source-proofs.json` records exact paths, hashes, selectors, MathML, and counts.

The original lesson archive census examined 2,964 HTML files. It found 383 hat movers in 118 items across 36 topics: 294 caret operators with no attributes and 89 with `stretchy="false"`. Every operator is an ASCII caret; no Unicode hat variants or caret operator color/background attributes were found. All mover nodes have no attributes. Authentic base styling is recorded separately in `hat-base-styles.json`.

MathJax's source distinction matters: `stretchy="false"` represents `\hat`; the default stretchy caret represents `\widehat`. The importer validation agent independently round-tripped these commands through the local MathJax renderer. Restoration uses the original operator attribute, never the number of letters in the current base.

`recover_flattened.py` reconstructs all 242 flattened occurrences in 106 fields. Each affected substring matches the historical converter output for the exact owning source item, allowing only whitespace normalization. It preserves the current non-accent base notation and restores only the source's hat scope and width. Fifteen orphan answer entities are linked to their original source questions through exact answer UUIDs in historical lesson-seed EDN; current ownership is not guessed.

Final flattened replacements are in `../flattened/changes.json`, with a review diff and validation summary. No unresolved cases remain. The script verifies source hashes, unchanged text outside replacement spans, unchanged placeholders, exact replay, and complete coverage.

`structured-widths.json` supplies source-proved width information for structured hats, with source-specific entries where the same textual base appears in both styles. Additional capture-based source evidence is produced by the structured-repair agent. This directory performs no database writes.
