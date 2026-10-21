# Source-backed recovery of flattened braces

Prepared 83 field replacements covering all 154 flattened `_(⏟)` / `^(⏞)` occurrences in the current audit. These 83 fields require 150 replacement spans because two nested-label expressions contain three accents each.

For 82 fields, the original archived HTML/MathML supplies the exact accent subtree and scope. Its historical converter output matches a substring of the current field exactly after whitespace removal. The replacement keeps the historical spelling of non-accent mathematics, reconstructs the original underbrace/overbrace structure, and treats label words as text. There are no ambiguous equal historical strings with different source scopes within a field. All prose and text outside recorded replacement spans remain byte-identical.

Fifteen replacement spans across fourteen fields contain original source `[math]...[/math]` wrappers in brace-label text. These wrappers are interpreted as their original math content, with adjacent words in text mode. This avoids preserving literal import markup in the repaired labels.

One field, `17592186078326 :question/worked-solution`, requires restoring the first two rows of its affected source equation. The historical converter confused absolute-value delimiters with a matrix across those rows and consequently destroyed the accent's base. The exact original two rows are reconstructed through the repaired maintained converter; subsequent rows and the surrounding field are unchanged.

The source for `17592186224898` itself puts the minus before the brace in `- (brace around 5x-x labelled -6x)`. This one documented source annotation error is corrected by moving the existing leading minus into the brace: `\underbrace{-5x - x}_{-6x}`. The visible equation tokens remain unchanged. Exact symbolic verification confirms that `-5*x-x` equals the `-6*x` label. The replacement proof records the source scope, corrected scope, unchanged token check, and zero algebraic difference.

Artifacts:

- `changes.json`: complete before/after fields, source paths/selectors/hashes, and exact per-span source proofs.
- `changes.diff`: reviewable changes.
- `summary.json`: counts and invariant verification.
- `source-candidates.json`: archived MathML and historical converter output.
- `serialized-candidates.json`: independently reserialized source fragments using the repaired maintained DOM converter.
- `dom-for-source-recovery.js` and `converter-source.json`: frozen converter and hash.

Reproduce with the repository Python environment: `prepare.py`, `serialize.py`, `node serialize.cjs`, then `finish.py`. The `serialize.cjs` step uses an isolated offline Chrome page. `source_notation.py` retains the historical non-accent math spelling when building the final replacements. No database writes are performed by these scripts.
