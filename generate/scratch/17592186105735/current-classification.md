# Current classification and extraction

Supersedes the basis-1356 classification for current inventory. At math basis
2671, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`, all 15 practice sources
have difficulty, a complete field-owned bank, a correct designation and a worked
solution. The immutable current snapshot is `reference/initial/snapshot.edn`;
the original `source.json` remains historical evidence.

| Level | Sources | Fields | Prompt/solution layouts | Plots |
|---|---:|---|---|---|
| easy | 9 | 4 radio, 5 scalar blank | integer supplied-cross; radical cdot; radical parentheses; thin-spaced radical parentheses | none |
| moderate | 6 | 5 radio, 1 scalar blank | cross/dot radio; source-commuted minor radio; cross/dot blank with evaluated-products row | none |
| hard | 0 observed | authored radio or scalar blank | existing dense cross/dot masks | none |

Each radio source has its own complete empirical bank profile, recorded below.
Each blank has one scalar and no distractors. The hard policy remains explicitly
authored: nine nonzero integer inputs, magnitude at most five, at least one
magnitude five, and three nonzero cross components. This increases arithmetic
workload within the same cross-then-dot method; it introduces no geometric or
scalar-determinant method. Easy and moderate retain the v2 production bounds.
No level is declared unsupported.

The newly captured q-128090 supplies a=(-2,0,4), d=(7,-4,9), requests the scalar
22 and uses the three-row cdot solution. q-73451 uses a=(-5,2,3), d=(1,-5,4),
with scalar -3 and the same layout. q-128093 supplies a=(5,-8,-7), b=(-1,1,2),
c=(-3,1,0); its five cross rows yield (-2,-6,2) before the three dot rows yield
24. Its distributed minor row commutes each second product and leaves the first
negative j-minor factor ungrouped. `current_replay.py` retains that separate
parameterized notation mask. Larger a components are source replay evidence;
normal moderate sampling remains magnitude at most four.

q-317306 uses a=(2sqrt(2),-1,4), d=(-2sqrt(2),3,-5), a scalar blank -31,
thin-spaced tuples, grouped products, an evaluated-products row and final scalar.
The coefficient-two square roots are replayed by the same operation mask with
an explicit coefficient-aware renderer. They do not silently expand v2's unit
coefficient normal sampling policy. q-20065 is now a complete moderate source:
its repaired current prompt uses b×c, canonical cross vector (-3,-5,2), scalar
16, and the standard cross/dot solution. The older malformed capture is retained
only as historical evidence. No source record is changed by replenishment.

The backbone, parameter roles, source wording, answer fragments and ordered
solution stages remain those extracted in `template-extraction.md`. Eligible
radical coordinates remain slots rather than fixed first/third positions.
Current-source rendering checks preserve original sqrt(8) spelling separately
from mathematical simplification. The scalar identity derives from actual
vectors, independent of tuple spacing, radical spelling, choice order, bank,
profile, seed, or UUID. This also prevents a source task being regenerated in a
different blank/radio layout and counted as new stock.

All current sources and complete banks:

| Source | Level / mask | Parameters | Correct | Complete bank | Residual profile |
|---|---|---|---|---|---|
| q-20063 | easy / dot_int_radio | a=(1,0,2); d=(-2,1,8) | 14 | 14, 20, 18, 12, 16 | 0, 6, 4, -2, 2 |
| q-20065 | moderate / cross_radio | a=(0,-2,3); b=(4,-2,1); c=(3,-1,2) | 16 | 20, 10, 24, 12, 16 | 4, -6, 8, -4, 0 |
| q-128091 | easy / dot_int_radio | a=(-1,1,0); d=(6,1,7) | -5 | -7, 14, -12, 2, -5 | -2, 19, -7, 7, 0 |
| q-275347 | easy / dot_radical_cdot_blank | a=(-sqrt(3),0,-2); d=(-sqrt(3),10,-10) | 23 | 23 | 0 |
| q-275348 | moderate / cross_blank | a=(1,2,3); b=(-1,0,-2); c=(0,-2,1) | 4 | 4 | 0 |
| q-317302 | easy / dot_radical_parens_blank | a=(sqrt(7),-2,5); d=(sqrt(7),3,-1) | -4 | -4 | 0 |
| q-317303 | easy / dot_radical_thin_blank | a=(-2*sqrt(2),4,-3); d=(2*sqrt(2),-1,2) | -18 | -18 | 0 |
| q-317304 | easy / dot_radical_thin_blank | a=(0,5,sqrt(11)); d=(7,-2,sqrt(11)) | 1 | 1 | 0 |
| q-73457 | moderate / cross_radio | a=(1,-3,2); b=(2,-1,-1); c=(3,-3,0) | 0 | 16, 3, -21, -9, 0 | 16, 3, -21, -9, 0 |
| q-73458 | moderate / cross_radio | a=(-2,4,3); b=(-1,3,2); c=(2,-1,4) | -11 | -14, 32, -11, -15, 28 | -3, 43, 0, -4, 39 |
| q-73459 | moderate / cross_radio | a=(-2,0,-1); b=(-2,-1,0); c=(3,1,4) | 7 | 9, 8, 7, 5, 6 | 2, 1, 0, -2, -1 |
| q-128090 | easy / dot_int_radio | a=(-2,0,4); d=(7,-4,9) | 22 | 22, 14, 24, 18, 50 | 0, -8, 2, -4, 28 |
| q-73451 | easy / dot_int_radio | a=(-5,2,3); d=(1,-5,4) | -3 | -3, 5, -2, 12, -15 | 0, 8, 1, 15, -12 |
| q-128093 | moderate / cross_commuted_radio | a=(5,-8,-7); b=(-1,1,2); c=(-3,1,0) | 24 | 24, 44, 16, -52, -72 | 0, 20, -8, -76, -96 |
| q-317306 | easy / dot_radical_thin_blank | a=(2*sqrt(2),-1,4); d=(-2*sqrt(2),3,-5) | -31 | -31 | 0 |

These numerical residuals reproduce complete source values without claiming a
recovered error intention. They are evidence-only profiles. Production radios
continue to choose one entire operation-derived bank before sampling and reject
all collisions, as documented in the original extraction. All new production
records must replay exactly through v2 and pass its independent rendered-stage
validator and actual learner grader. Blank grading checks canonical and
equivalent sums as accepted and a wrong scalar as rejected.

Source fidelity: 15/15 prompts, 15/15 solutions, 15/15 complete banks,
51/51 values and 36/36 distractors. Actual current-source grading: 21 accepted,
42 rejected, zero unresolved. Existing v2 validation: 900 distinct changed tasks
across the three levels, exact historical bank replay, determinism and mutation
checks. No plots occur, so stages 5 and 7 require no assets.

Preparation and durable receipts are under `reference/replenishment/`. The
publisher holds `api.lock` through fresh inventory, basis capture, preview,
submission and exact-basis readback. Its datom allowlist permits only additive
new question/field/answer facts, generator registration and this KP membership.
It verifies every existing source and unrelated KP field is unchanged. Complete
intent and source attribution are retained before guarded submission.
