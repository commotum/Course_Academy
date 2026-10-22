# Sentence completion using the invertible matrix theorem

Source snapshot: EDB math basis 2657; immutable lineage 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1. `source.json` retains every original question, field, choice, key, solution, and canonical example. `reference/source.edn` retains typed evidence.

The backbone supplies a real square matrix, one condition, and three proposed conclusions. The learner evaluates each implication using invertibility, full rank, column space, null space, or pivot columns. Each solution recalls the theorem, evaluates the three complete conditional sentences in order, explains each truth value, and gives the selected subset. Numeric dimensions supply context without requiring matrix computation. Varying those numbers alone is outside the distinct-task policy.

These conservative templates remain separate because their conclusions, explanation sequences or field layouts differ. One bank profile per source is preserved without mixing banks:

| Source | Supplied condition | Proposed conclusions in order | Fields | Parameters |
|---|---|---|---|---|
| q-47599 | invertible, dimension 7 | zero determinant; full column space; 5 pivots | I, II, III checkboxes | fixed |
| q-142475 | nullity zero | invertible; rank below n; full column space | I, II, III checkboxes | equivalent given fact |
| q-142476 | invertible, dimension 8 | zero determinant; column space R^16; 8 pivots | I, II, III checkboxes | fixed |
| q-47587 | determinant zero | no inverse; full rank; all columns pivot | I, II, III checkboxes | fixed |
| q-79334 | nullity zero | not invertible; full rank; full column space | I, II, III checkboxes | equivalent given fact |
| q-139978 | determinant zero, dimension 5 | no inverse; nullity zero; fewer than 5 pivots | I, II, III checkboxes | fixed |
| q-141215 | invertible, dimension 6 | zero determinant; null space R^6; column dimension 6 | selection radio | fixed |
| q-142479 | rank below n | invertible; null space has no basis; determinant zero | selection radio | fixed |
| q-141341 | nullity zero | invertible; zero determinant; full column dimension | selection radio | equivalent given fact |

For the three variable templates, the supplied condition can range over nullity zero, nonzero determinant, full rank, trivial null space, full column space, or full column dimension. Exclude any condition whose concept is already among that question's proposed conclusions: copying the given fact reduces the workload. These are explicitly supported same-method generalizations, rather than observed parameters. Every eligible condition forces invertibility, so the original conclusions and their individual explanation stages remain valid. Substitute the precise condition into every occurrence of the original premise in the prompt and worked solution; leave the recalled theorem intact. `domain()` is the complete bounded domain. No statement reordering, numerical dimension variation, or arbitrary new assertions are sampled.

All source values and complete choice mappings are retained in `choice-recipes.json`. Checkbox profiles use exactly the field-owned text values `true` and `false`. Radio choices use the complete original five Roman-numeral subset strings as fixed values. Their psychological distractor interpretations are not inferred. `source-replay.json` reports every matched bank, answer designation, and distractor. There are no blank fields. The current field representation, including migrated checkboxes, takes precedence over historical radio captures.

q-47586 is excluded: it lacks difficulty, solution and key; the mathematically true subset III only is absent from its stored bank. q-141342 is excluded from generation and validated inventory: its premise is nonzero nullity, but its three worked conditional sentences quote zero nullity. Both originals are preserved unchanged. `Null(A) has no basis` is false: every finite dimensional subspace has a basis, including the trivial space with its empty basis.

No generated prompt or solution requires a plot. All supported source mathematics is already text/LaTeX; no source assets need publication. The canonical example's inline theorem image is mathematical typesetting, not a diagram, and is not sampled as practice.

`review.md` places exact source replays and changed-premise variants side by side. `validate.py` reads the rendered statements independently, checks all relevant ranks with exact diagonal matrix witnesses, exercises every bounded premise, preserves complete field banks, verifies printed solution truth values and stale-premise absence, and passes all options through the actual learner grader. Source fidelity, mathematics, and grading are reported separately.
