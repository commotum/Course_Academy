# Classification — Eliminating the First Variable

Frozen evidence: `math`, basis **1356**, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. `source.json` is the unchanged capture wrapper. Two practice sources, neither rated, neither with correct references or worked solutions. Canonical e-13995 is context, not a third practice source.

| Source | Original system | Fields | Bank | Difficulty | Plots |
|---|---|---|---|---|---|
| q-210858 | x−y=1; −7x+5y=9 | field-1 text select(2), field-2 math select(4); capture field order 2,1 | first/second; 5,7,−7,−5 | absent | none |
| q-210859 | 3s+4t=8; s+5t=10 | field-1 text select(2), field-2 math select(4); capture field order 1,2 | second/first; 4,−3,3,−4 | absent | none |

One mathematical/presentation template with two distinct observed bank profiles. Public raw profiles retain each source's field order, identities, complete banks, missing difficulty/solution/correct keys, and exact decoded prompt. Pulled field/answer enum entities are projected to their exact ident strings for the local generator interface; source.json retains every original nested entity. Missing keys are not replaced with nulls. Both original systems contain an unmatched literal `{` inside mathematics: verified decoded text has one unescaped brace, not doubled slashes. Evidence replay preserves this anomaly; normal presentation escapes the visible brace as `\{`.

Independent cancellation establishes q-210858 = **first, 7**, q-210859 = **second, −3**. There is exactly one valid pair among each full Cartesian answer bank. These are inferred completions, not source correct-designation fidelity. Completed output is eligible only with authored correct refs, worked solutions, repaired presentation and difficulty.

## Curriculum boundary and authored levels

Owning topic 17592186050190 (MA4026) is **Solving Systems of Linear Equations Using Elimination: One Transformation**. Frozen lesson traversal is activity first-step 17592186193457 (Introduction) → 17592186193458 (this KP) → 17592186193459 (second variable) → 17592186193460 (solve by first variable) → 17592186193461 (solve by second variable). Collection order was not used. Key prerequisite is Introduction to the Elimination Method, MA742, which includes equation transformation and signed integer elimination.

Canonical e-13995 multiplies one unit-coefficient equation by −2, prints the two resulting equations, grouped addition and collected remaining equation, then states the operation. It does not solve for either unknown. Sources supply multipliers +7 and −3 and positive/negative integer coefficients; sibling one-transformation examples use nonunit coefficients and small integer ratios. This supports bounded signed integer quotient recognition as the same operation. MA742 `742.md` and MA4026 `4026.md`/`Source/4026.json` were read locally; they are curriculum context, not new fixed-basis source questions.

All labels below are **authored design claims**, not recovered source levels. Each level has exactly the same paired-select response and one scaling/addition; variations within a level have equal structure, never a progression.

| Level | Smaller absolute first-variable coefficient | Larger/smaller absolute ratio | Fixed reasoning demand |
|---|---|---|---|
| easy | 1 | integer 2–7 | Read two signed coefficients and cancel by a single familiar integer multiplier; observed originals fit |
| moderate | 2–4 | integer 2–4 | Recognize the signed integer quotient of two nonunit coefficients, then identify the single row |
| hard | 2–4 | integer 5–7 | Same nonunit quotient and signed cancellation with larger familiar products; a bounded arithmetic workload distinction |

Hard's integer-ratio arithmetic is an explicit extrapolation of the observed multiplier 7 to nonunit coefficients; it is not evidence that MA labeled such tasks hard. Maximum first-variable coefficient is 28; other coefficients are nonzero signed integers of magnitude 1–10; constants are −12…12. Bounds are guarded for explicit parameters as well as samples. These familiar integer products avoid introducing fractional arithmetic or two transformations. No solving for the remaining variable, substitution, pivot, second-variable branch, row normalization or second scale occurs.

The task asks for an **operation pair** whose scaled equation adds to the unchanged equation and eliminates the FIRST variable. Merely preserving a complete system's solution set is insufficient. Both row choices can work with reciprocal multipliers in unrestricted mathematics; the chosen complete bank intentionally includes only one valid pair. The default bank is picked before parameters and rejected as a whole on any collision or additional valid pair.

Parent interface/variety correction: public raw fields and answers use enum ident strings, while the captured full Pull objects remain unchanged in source.json. Global coefficient-sign aliases share a mathematical fingerprint; actual nonunit division operands remain because they define the authored workload. Exhaustive meaningful task domains are24 easy,36 moderate,36 hard.
