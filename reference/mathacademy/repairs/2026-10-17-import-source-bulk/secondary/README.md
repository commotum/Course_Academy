# Secondary source-structure repair proposals

All 2,727 fields from the October 16 secondary queue are classified. The final
proposals repair 2,724 fields through 3,456 exact source-bound replacements.
One changed tutorial is handled by the parent's manual contextual repair.
Two old answer entities are negative controls: their UUIDs identify original
choices with genuine minus signs; the audit's phantom-minus loss witnesses
belong to different choices that the original import collapsed to equal text.
Changing these retained answer values would introduce an error.

`changes.json` contains exact fresh before values and source-bound replacement
spans; `decisions.json` contains every original candidate. `manifest.json`
binds the frozen source converter and proposal files. This directory performs
no database writes. The parent merges proposals, applies separately reviewed
responsive display layout, validates, and transacts.

Each proposal proves the original source occurrence's bytes/hash and maps it
through the archived owner/field rendering. Answer entities additionally bind
the import's deterministic answer UUID and actual source choice ordinal;
equal text alone is insufficient. Current answer representation determines
whether a value is raw TeX or Markdown containing delimited math. Existing
non-target prose and answer-control markers are retained.

The converter retains table rows, cells, rules, fences, zero-rule fractions,
phantoms, exact cancellation directions, mathematical variants, colors,
visible boxes, explicit display style, and embedded text/math boundaries.
Ragged source rows receive only implicit trailing empty cells. Bare zero-width
phantoms become vertical phantoms; empty tables have no visible expression.
Font sizes and incidental inter-row/column spacing can use application defaults.
Balanced source `[math]...[/math]` fragments are recovered without discarding
surrounding prose. Four source-specific corrections have SHA-256 guards and
source evidence (see `manual-source/README.md`).

Sixteen focused regression tests passed, including the original wrong-fraction
bar failure, visible phantom/box failure, missing matrix separator, text/math
wrapper failure, and invisible-right-delimiter punctuation regression, full-height binomial fences,
and literal hash text. The
parent's independent review additionally renders complete final fields and
compares source mathematical structure to actual MathJax output.
