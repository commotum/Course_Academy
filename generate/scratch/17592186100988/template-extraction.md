# Four-stage template extraction

Source math basis1356. `source.json` preserves all raw evidence; `source-cases.json` sends every practice record through public `generate`, with a source-specific raw bank profile. `source-questions.md` lists all original content and choices, and the table below accounts for every choice operation.

## 1. Describe each original

q-13488: unrated, missing worked solution/correct reference; inline A=2×3 matrix with repeated1s, signed-1 and3, requested a13. Five radio choices(-1,0,3,“No such entry”,2). The correct scalar2 follows directly from row1,column3; raw does not invent a designation. q-13496: unrated with the same omissions, inline D=3×4, requested d43 outside the three-row range. Five choices(5,-3,-1,4,“No such entry”). Its mathematical conclusion is absent-entry, not an observed correct marking. Both inline widgets and complete values were checked against authoritative `/home/jake/Developer/MA/DATA/Lessons/1167/Source/1167.json`; that widget likewise does not supply a solution/correct marker.

q-279260: easy radio, Y=2×3, y22=-1; values1,2,-1,-2,7. q-279539: easy blank, E=5×4, e53=2; q-279540: easy blank, F=3×4, f32=4. Both blanks supply the named entry followed by `{{field-1}}` and expect only the scalar, not an equation or index pair. q-13497: easy radio,C=3×4,c24=5; “should lie” prose and omitted period in the repeated solution matrix. q-125561: easy radio,E=3×2,e31=-3; “lies” prose and omitted repeated-matrix period. Full original matrices and shared wording are in source evidence and exact replay tests, including repeated entries and negative/zero numbers.

## 2. Generalize the common pattern

Read first subscript as row, second as column, locate their intersection, report its signed integer value. The observed out-of-range request reports no such entry and supports a normal easy absence-entry family. Matrix typesetting is mathematical notation, not a plot. Every worked solution identifies the requested row and column, states the entry, and repeats the complete matrix. No algebra or matrix operation occurs. Preserve display/inline masks, subscript bracing, period placement, blank notation and all source omissions.

## 3. Map components and complete source banks

Each matrix is an independently parameterized array of integers. `i`, `j`, and `letter` are full slots, not short global text substitutions. `external.zero` and `external.two` explicitly retain opaque historical scalar slots. Every complete bank is chosen as one profile; no option is silently dropped or replaced. A cell map can be nonunique when a value occurs twice, so these are replay definitions rather than asserted original misconceptions.

| Profile | Complete ordered source choice recipes | Original values |
| --- | --- | --- |
| raw:q-13488 | cell(2,1); external.zero; cell(2,3); missing; target | -1;0;3;No such entry;2 |
| raw:q-13496 | cell(2,4);cell(3,3);cell(2,1);cell(3,4);missing |5;-3;-1;4;No such entry |
| raw:q-279260 |cell(1,1);external.two;target;cell(2,1);cell(2,3)|1;2;-1;-2;7|
| raw:q-279539 |target|2|
| raw:q-279540 |target|4|
| raw:q-13497 |missing;cell(2,3);cell(1,4);cell(2,1);target|No such entry;-3;4;-1;5|
| raw:q-125561 |cell(1,1);target;cell(3,2);cell(2,1);cell(2,2)|1;-3;4;-1;5|

All27 values match one-to-one with type preservation; five available correct designations match. The two missing designations remain absent. Source-bank error intention for external0 and2 is unresolved; those profiles are evidence-only and never normal default recipes. `completed:q-13488` and `completed:q-13496` explicitly author easy API workload, the mathematical reference and the shared canonical explanation; they remain evidence-only to avoid promoting external opaque banks into learning.

## 4. Reusable masks, bounds and consistency calculations

Fixed pieces: “Find the entry,” named matrix, where; `bmatrix` inline versus bracketed `aligned` display; radio key selection versus blank field-1. Variable pieces: complete matrix body, matrix name, entry name/index, both ordinal row/column phrases, final scalar and repeated matrix. Conditional pieces: blank's answer placeholder; original “should lie”; solution-matrix period; absence of difficulty/solution/correct ref; explicitly authored absence-entry conclusion for completed unrated evidence. Scalar target is computed from the actual1-based position; source fixed cell locations/external slots generate the complete bank through the same API at changed signed parameters. Negative-entry samples require no arithmetic.

Authored normal radio profiles are complete operations chosen before parameters: location_no_entry={target,neighbor row,neighbor column,diagonal neighbor,missing}; four_locations={target,neighbor row,neighbor column,diagonal neighbor,other nearby column}; swap_no_entry={target,swapped row-column indices,neighbor row,neighbor column,missing}. The neighbor is+1 except at a boundary where it is-1. The additional column is the other immediate neighbor where available, otherwise two columns inward. A swap must exist and differ. No diagnosis enters learner prose. Repeated selected locations, equal selected scalars, invalid swaps or any duplicate/equivalent answer reject the whole instance. The blank profile has only the scalar reference. Missing/default unsupported requests are rejected, never silently resampled for explicit inputs.

Default entries are integers[-9,9]. Easy dimensions are the exact observed2×3,3×2,3×4,5×4; moderate5×6/6×5,maxindex≥4; hard6×7/7×6,maxindex≥5. Normal easy inline_no_entry_radio extends the observed out-of-range demand: exactly one index equals its dimension plus1 and the other remains in bounds; larger gaps, simultaneous overflows, zero/negative indices and absence-entry blanks are rejected. Moderate/hard keep their established numeric in-bounds scan demands; a boundary comparison does not inherit a harder scan label. Per-level methods and bounds are documented in separate generator sections. The public interface supports field filters, template and profile selection, full explicit parameters and deterministic seed shuffling.

A meaningful assessed task fingerprint is(dimensions,row index,column index,target scalar or absent), excluding matrix-letter aliases, layout/bank names and unused matrix values. Other cells are visual context or distractors, not additional assessed reads. Full content identity separately includes version, actual prompt, complete worked solution, difficulty/key presence, field type/key, complete typed bank and correct-reference presence. All display values and aliases remain in that identity; unused external parameters/profile spelling and option order do not. The finite numeric authored core has836 easy,798 moderate and988 hard tasks (19 possible target values times44,42,52 admissible dimension/index combinations). The validator enumerates each, including all eligible whole-bank profiles, rather than counting cosmetic display changes.


### Normal no-entry bank and variety correction

`overflow_locations` is a complete bank chosen before parameters: No such entry; last valid overflow coordinate; first valid overflow coordinate; last plus adjacent coordinate in the other direction; first plus that adjacent coordinate. For a row overflow it reads (m,j),(1,j),(m,neighbor(j)),(1,neighbor(j)); for a column overflow it reads (i,n),(i,1),(neighbor(i),n),(neighbor(i),1). This embodies clamping, restarting counting, and adjacent-coordinate miscounting. The neighbor moves1 inward at a boundary. All four wrong scalars come from the displayed matrix; equal values reject the whole bank. Normal no-entry solution explicitly states row/column dimensions and absence of the requested position. Its mathematical fingerprint is(m,n,i,j,None), irrespective of selected bank scalars or other matrix entries. The26 eligible dimension/index tasks add to836 numeric easy tasks, yielding862 easy,798 moderate,988 hard and2648 total. Source-cases/raw fidelity remain unchanged; difficulty/refs/prose on the two raw unrated records remain absent.
