# Template extraction

An equation `s(k+h)x+b=c` over the reals has no solution exactly when `s(k+h)=0` and `c-b != 0`. Each complete source gives unequal integer constants; outer scale `s` is nonzero, so the required blank is `k=-h`. All fields are singleton math blanks with no distractors or feedback.

Source-specific components and original wording are retained in `extraction.json`; source parameters and full bank mappings are in `source-cases.json`:

- q-287667: moderate, variable x, parameter p, scale 2, shift -4, constants 2 and 5. Only bank value 4; correct designation matched.
- q-288634: moderate, variable x, parameter p, scale 3, shift 2, constants 7 and 10. Only bank value -2; correct designation matched.
- q-288644: easy, variable v, parameter k, scale 1, shift -2, constants -3 and 5. Only bank value 2; correct designation matched.
- q-288646: easy, variable x, parameter m, scale 1, shift 6, constants 2 and 7. Only bank value -6; correct designation matched.
- q-288648: easy, variable u, parameter q, scale 1, shift -5, constants 9 and 0. Only bank value 5; correct designation matched.

The fixed shared sentences are replayed verbatim. The prompt introduces the variable, displays the equation, requests the parameter, and retains `$k=$` before `{{field-1}}`. The solution states the zero-coefficient/nonzero-constant rule, subtracts the left constant from both sides, labels the coefficient and residual with underbraces, sets the coefficient to zero, and isolates the parameter. In the moderate template it also divides by the outer scale. Positive/negative shifts and left constants control signs; the source solution row counts are preserved. Equation inputs and blanks contain no new figures.

Fixed components: instructional sentences, blank key/type, LaTeX layout and solution order. Variable components: parameter and variable names, shift, unequal constants, positive scale. Conditional components: plus/minus signs and the moderate division step. No optional answer fields, inferred distractors or feedback are added.

Observed values are recorded independently from sampling bounds. Bounds include every complete source: nonzero shifts -9..9, nonzero left constants -9..9, right constants -10..10, easy scale 1, moderate scale 2..9. Scales 4..9 and unobserved signed constant combinations are explicitly labeled arithmetic extensions. Zero shift and zero left constant are excluded to retain the observed solution steps. Equal constants and zero scale are rejected because they change the no-solution condition. Variables and constants are not used to inflate task distinctness: only the 18 roots per method count.

q-288643 has a compact inline prompt and incomplete bank, so it remains a separate excluded layout with no fidelity claim. There are no unresolved comparisons among the five supported complete source banks. Plot extraction/generation are not applicable: no referenced assets or mathematical diagrams occur in these sources.
