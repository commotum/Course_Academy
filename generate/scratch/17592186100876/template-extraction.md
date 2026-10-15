# Extraction and bounded sampling policy

source-components.json records every source's exact matrices, target, values, choice owner, choice value and recipe, prompt and ordered solution. source-bank-map.json records full replay including both duplicate q-41949 banks, 53/53 values and no missing/extra values. side-by-side.json juxtaposes every original, replay and examples covering its target slots.

The fixed backbone is one square source-sized matrix and one compatible row/column of the identity; find their product, retaining source matrix names, multiplication order, response shape, placeholders and Markdown table. Easy solutions notice the basis column, explain column selection, display the selected column, then show multiplication, scalar dot products and the result. Moderate solutions notice the basis row, explain left multiplication/row selection, display the selected row, then show the long-way matrix multiplication and result. Those operative sentences and stages are retained from each source with ordinal and mathematical slots substituted. The first erroneous result of q-130247 is corrected in new output only.

Slots: matrix entries; selected basis index; numeric parameters internal to radicals, fractions, decimal coefficients, logarithms and constant multiples. The source parameters remain exactly replayable. Normal sampling preserves source-sized zero positions, sign and scalar form (integer, terminating decimal, radical, rational, pi/e fraction or logarithm). Radical coefficients are 1..4 and radicands are selected from 2,3,5,6,7,10,11,13,17,19. Signed integers are 1..9 (two-digit source roles up to 14); fractions have numerator 1..5 and denominator 2..7; decimal magnitudes are 1.1..4.9; logarithm arguments are integers 2..9. All are exact reals. These are conservative same-method bounds, not inferred source bounds.

General target indices span every row/column compatible with the original role. Every dependent basis vector, ordinal, selected answer, distractor, and solution changes together. No extra operations or stages are introduced. q-130247 uses a=sqrt(d)/d and t=1/d, d in {2,3,5,7}, matrix [[a,-a,0],[a,a,0],[0,0,1]], fixed second-column target. Its four variants form an explicit finite profile; other easy templates have much larger pools.

Let R_i and C_i be a matrix row and column, and transpose preserve its entries while switching orientation. For general radio profiles, rotate the referenced indices cyclically by target minus source target, modulo three. A complete profile is chosen before constructing options; a collision rejects the entire instance. Source order is retained, and shuffling never creates another task.

| Profile/source | Complete bank at original target (zero-based) |
|---|---|
| q-41949 | R1, C2, C1, C0 correct, R0 |
| q-41943 | C2 correct, C1, transpose(C1), C0, transpose(C0) |
| q-130247 | [-a,a,0] column correct; C2; [-a,t,0] column; [a,a,0] row; [-t,t,0] column |
| q-41944/q-41979 | R1 correct, R0, R2, C0, C1 (source orders retained separately) |
| q-41977 | C1, altered R0, R1 correct, C2, R2 |
| q-41950 (replay only) | C0, R0, C2, R2 correct, R1 |

q-41977's altered row replaces its third entry with -sqrt(d-4), where d is the radicand in original matrix cell (0,2). Source d=7 reproduces -sqrt(3); normal d is one of 7,10,11,13,17,19. This is an observed-value-preserving expression extension with unresolved psychological interpretation. The anchor stays fixed as the wrong-row role rotates. No inferred feedback is presented. Every other bank value is an exact supplied row/column or orientation error. Blank fields have no distractor profiles and accept one delimiter-free scalar per field key in original order.

Identities are deterministic UUIDv5 under the KP UUID. A task fingerprint includes the exact matrix, orientation and selected index, ignoring seed, IDs, option order and field form. New content excludes every existing task and canonical task. Different source profiles may name separate generator records but cannot be accepted as distinct inventory for the same task. Each answer UUID is owned by its field. Source Math Academy IDs are never copied to generated questions.

Validation: exact SymPy products independently compared with parsed prompt, rendered solution results and dot products, every keyed field and every option. Source-bank replay and notation/layout checks are separate. Actual learner grading covers replay and target-position representatives; every batch intended for persistence is checked again. changed-target.json keeps identical matrices while changing only targets across both orientations, field forms and dimensions. validation.json reports coverage, fidelity and capability limits separately. Dependency version is embedded per record; deterministic replay is checked before freezing.
