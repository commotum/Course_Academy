# Classification at EDB basis 2358

KP 17592186129115: Identifying Operations That Would Transform a Matrix To Row Echelon Form.
Lineage: 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1. All ten practice questions and the canonical example were read together with a fixed as-of basis.

| Difficulty | Source questions | Fields | Templates | Bank profiles | Plot rating |
|---|---:|---|---:|---:|---|
| Moderate | 10 | one radio field, selection; five text options | 1 | 10 | none |
| Easy | 0 | unobserved | 0 | 0 | unclassified |
| Hard | 0 | unobserved | 0 | 0 | unclassified |

The common backbone is a 4 by 4 matrix, choosing one complete set of two or three entries to replace by zero, and checking the resulting leading-entry order and zero rows. Signed integer magnitudes do not affect the method. Row swapping, arithmetic row operations, reduced echelon form, and computing a row reduction are outside the backbone. Source matrices have different zero patterns and correction sets; these are parameter slots rather than separate prompt templates. All five options from each source remain together as one profile.

| Source | DB entity | Observed matrix | Correct entries (zero-based) | Original leading columns (4 means zero row) |
|---|---|---|---|---|
| q-42008 | 17592186129772 | `[[1, 1, 4, 7], [2, 4, 2, 1], [0, 0, 5, 6], [0, 0, 1, 3]]` | `[[1, 0], [3, 2]]` | [0, 0, 2, 2] |
| q-42370 | 17592186129779 | `[[0, 2, 4, 2], [0, 4, 5, 3], [0, -1, 7, 3], [0, 0, 0, 0]]` | `[[1, 1], [2, 1], [2, 2]]` | [1, 1, 1, 4] |
| q-129423 | 17592186265724 | `[[0, 4, 0, 9], [0, 3, 8, -1], [0, 0, -7, 0], [0, 0, 0, 9]]` | `[[1, 1], [2, 2], [3, 3]]` | [1, 1, 2, 3] |
| q-129424 | 17592186265725 | `[[9, 0, 7, 2], [0, 7, -3, 1], [-3, 2, 5, -1], [0, 0, 6, -4]]` | `[[2, 0], [2, 1], [3, 2]]` | [0, 1, 0, 2] |
| q-42371 | 17592186329643 | `[[-5, 4, 0, 3], [0, 0, 3, -6], [0, 0, 7, 6], [0, 0, 9, 0]]` | `[[2, 2], [3, 2]]` | [0, 2, 2, 2] |
| q-73149 | 17592186341915 | `[[-1, -2, 0, 1], [0, 2, 0, 1], [1, 0, 1, 6], [0, 1, 0, 3]]` | `[[2, 0], [3, 1]]` | [0, 1, 0, 1] |
| q-73151 | 17592186341916 | `[[1, 1, 4, 6], [0, 0, 8, -2], [0, 3, -3, 1], [6, 0, 0, 0]]` | `[[2, 1], [2, 2], [3, 0]]` | [0, 2, 1, 0] |
| q-73154 | 17592186341917 | `[[5, 1, 0, 3], [0, 0, 6, 0], [0, 0, 3, 0], [1, 0, 0, 0]]` | `[[2, 2], [3, 0]]` | [0, 2, 2, 0] |
| q-42372 | 17592186402803 | `[[1, -2, 3, -4], [0, 1, 5, 0], [-5, 0, 0, 3], [7, 0, 0, 0]]` | `[[2, 0], [3, 0]]` | [0, 1, 0, 0] |
| q-42373 | 17592186413822 | `[[-1, 5, 0, 0], [0, -1, 2, 3], [0, -1, 0, 2], [0, 0, 2, 4]]` | `[[2, 1], [3, 2], [3, 3]]` | [0, 1, 1, 2] |

All source banks have exactly one mathematically valid option under an independent exact echelon check. q-73151 contains the malformed label `${a}_{32}$ only ${a}_{33}$ only`. Its two explicit indices denote the incorrect set {a32,a33}; normal generated instances render “a32 and a33 only”. Replay retains the original verbatim. The original source question is not edited and is excluded from the conservative usable reserve count, leaving nine fresh clear moderate tasks.

Easy and hard are unsupported by this package: source evidence supplies no calibrated workload, bank or solution at these levels, and manufacturing a difficulty label for this same task would not establish difficulty. This is a bounded evidence exception, not a claim that such levels are mathematically impossible. New source evidence reopens classification. Unsupported shortages remain five each.
