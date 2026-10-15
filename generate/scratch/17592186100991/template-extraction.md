# Source extraction and generator contract

`source-components.json` lists every source's exact operands, expression, names,
field layout, choices, key and any exclusion. `source-cases.json` gives the six
complete source replays. `source-replay.json` separates exact fidelity from the
two unresolved raw records. No source record is changed.

The backbone is entrywise arithmetic on three supplied matrices. Flat addition
and addition/subtraction have three displayed solution stages: substitute the
three matrices, show the scalar operations in each cell, then show the result.
Nested variants have five stages: substitution, cellwise inner difference,
evaluated inner difference, cellwise outer operation, final matrix. Four blanks
retain field-1 through field-4 in row-major order and the original Markdown
table. The 3x2 radio template retains five whole-matrix choices and the source
solution's colon and final punctuation. These are distinct backbones and field
combinations, not interchanged within a template.

Variable slots are the twelve 2x2 or eighteen 3x2 operand entries, and three
distinct single-letter matrix names. Every operand entry participates in its
corresponding requested result cell. There is no selected target-cell slot:
all entries are requested. The expression and shape stay fixed per template
because changing them would alter workload or solution stages. The supplied
matrix names are cosmetic and do not count as distinct mathematical tasks.
No multiplication, scaling, inversion, four-matrix variants or new response
contracts are introduced.

Observed parameters are preserved verbatim for replay. Normal blank sampling
uses signed integers -9 through 9 (including zero); this conservatively extends
the observed signed entries within the same entrywise method. Radio sampling
uses observed signs and zero locations, magnitudes 1 through 12; its 3x2 shape
stays fixed. Sampled zero/nonzero entries and signed boundaries are validated.
The source matrix letters may vary together in prompt and every solution stage.
Correct entries are computed with SymPy before authoring fields or choices.

For blanks, each field owns one delimiter-free integer answer. No distractors
or feedback are added. The complete 3x2 q-69636 radio bank uses the following
parameterized recipes, with A=a, B=b, C=c, and z=a+b+c (indices zero-based).
Unlisted cells equal z. The compound mistakes' psychological interpretation is
unresolved; these are exact observed expression patterns, not learner feedback.

| Bank member | Changed cells |
| --- | --- |
| 1 | (0,1)=-a01+b01+c01; (1,0)=-z10; (2,0)=-z20; (2,1)=a21-b21+c21 |
| 2 | (1,1)=a11-b11+c11; (2,0)=-z20; (2,1)=a21-b21+c21 |
| 3 | (0,1)=-a01+b01+c01; (1,0)=-z10 |
| 4, correct | z everywhere |
| 5 | (0,1)=a01-b01+c01; (1,1)=a11-b11+c11; (2,1)=-z21 |

The entire profile is selected before sampling. A collision between any complete
matrices rejects the whole sample; options are not pooled or patched. Every
source option has exactly one match and the correct designation is preserved.
The two incomplete 2x2 radio banks retain exact observed offsets for analysis
only and are not emitted. Their absent difficulty is not guessed.

Identity and inventory distinctness use operand arrays and the resulting signed
arithmetic, ignoring seed, option order, names and UUIDs. Flat A+B-C and nested
A+(B-C) with identical operands therefore cannot inflate the pool. The separate
content identity preserves exact authored presentation; selection deduplicates
mathematical tasks before committing. Source UUIDs and MA IDs are never reused.

Validation independently reads the displayed operands, operators, answer values
and every worked-solution stage; all must equal the evaluated matrix. Exact
source replay checks wording, punctuation, field layout and entire banks.
The real application grader checks correct and incorrect radio IDs, every blank,
equivalent expressions, and wrong integers. Fixed-operand changed-operation
cases catch stale keys and solution references. Deliberate operand/key/operator/
solution mutations must fail. Side-by-side review is in `review.md`.
