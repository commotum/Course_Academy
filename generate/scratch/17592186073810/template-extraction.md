# Source templates and bounded extension

Read with `source.json`, `reference/source.edn`, and `choice-recipes.json` for complete identities and option-level mappings. All number forms are integers; coordinates/constants may be negative; scalar distance answers are positive. The domain is the Euclidean plane, with a point off an axis-aligned infinite line.

| Source/profile | Axis | Point | Constant | Distance | Complete observed bank | Source solution computation |
|---|---|---|---:|---:|---|---|
| q-74034 | y | (5,-1) | 2 | 3 | 1,2,3,4,5 | d=\|-1-2\|=3 |
| q-114323 | x | (4,3) | 2 | 2 | 1,2,3,4,7 | d=\|4-2\|=2 |
| q-74202 | x | (-1,-4) | 4 | 5 | 3,4,5,6,7 | d=\|-1-4\|=5 |
| q-74206 | y | (2,-3) | 5 | 8 | 2,5,6,7,8 | d=\|-3-5\|=8 |
| q-74207 | y | (-3,3) | -2 | 5 | 2,3,5,6,7 | d=\|3-(-2)\|=5 |

Each prompt asks for the shortest distance between one supplied point and either x=c or y=c. Required response: one scalar in a radio field named selection. The fixed solution sequence is “Let's sketch the given situation”, sketch, horizontal/vertical identification, relevant coordinate difference, “So, the shortest distance is”, and a displayed absolute-value computation. Every original instructional sentence is retained. Replay k=1 preserves exact source prompt, solution and asset; generated k>1 updates all parameter spans and one displayed equality. No feedback is added.

Generalized pattern: compute |u-c| where u is the relevant point coordinate. A bounded extension dilates the entire geometry and each complete source bank by positive integer k=1..3. Correct answer is computed first as |ku-kc|, independently checked against k times the source answer. Each choice recipe is exactly k times that profile's original scalar (including all four distractors); source values are recorded in choice-recipes.json with original answer identities and explicit complete-value reproduction. The distractors' original cognitive interpretation is unresolved and is not invented. No pooling or profile mixing occurs.

Observed policy: k=1 only. Proposed, exhaustively validated sampling policy: k=2 or 3, integer coordinates of magnitude at most 15, positive distance at most 24; no new mathematical operation or answer shape. The two orientations and positive/negative constants remain easy coordinate subtraction as in rated sources. This is a deliberately narrow ten-variant family, not a claim of unrestricted fidelity or capacity. Distinctness hashes axis, relevant point coordinate and line constant. The unused coordinate, identity, bank order, profile and seed never establish novelty. Existing practice and canonical tasks are excluded from selection.

Excluded q-74033 remains unchanged and is not replayed as a keyed bank. All five supported complete banks must replay with 25/25 whole values, 20/20 distractors, exact correct designation and no missing/extra options before preparation. Fidelity, independent mathematical validity, actual grading, and visual review are separately recorded.
