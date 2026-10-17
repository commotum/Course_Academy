# Pivot-column solution corrections

Prepared seven solution-only repairs from audit snapshot basis 3212. The parent
migration performs fresh reads, exact-before CAS, preview, commit, and readback.
This directory's preparation script has no database access.

| Question | Entity | Correction |
| --- | --- | --- |
| q-35457 | 17592186124884 | Conclusion names B, matching the prompt |
| q-35459 | 17592186124885 | Second operation is R5 := R5 + (2/7) R4; final row ends in +1 |
| q-35734 | 17592186124906 | Conclusion names P, matching the prompt |
| q-130957 | 17592186266022 | Conclusion names B, matching the prompt |
| q-130963 | 17592186266026 | Conclusion names B, matching the prompt |
| q-73621 | 17592186364337 | Singular “column” for the sole non-pivot column |
| q-73618 | 17592186342033 | Plural “columns” for two non-pivot columns |

`corrections.json` contains exact before/after strings, replacement fragments,
reasons, hashes, and independent exact-rational mathematical validation. Keys,
difficulty, memberships, and learner data are outside these corrections. All 68
topic solutions and 52 displayed operations pass after applying the repairs in
memory. Historical audit files remain unchanged.

The count generator `generate/scratch/17592186124479.py` already renders the
prompt's matrix name correctly and retains its single numerical radio answer.
No generator code change is needed. Its 16 source replays and 192 generated
variants passed exact math, rendered operations, and matrix-name checks. Native
grading accepted 208 correct choices and rejected 832 wrong choices. See
`count-generator-verification.json` and `count-generator-native-report.json`.
The excluded q-35459 profile remains excluded; template scope is unchanged.

Reproduce preparation and isolated generator checks from the repository root:

```sh
.venv/bin/python reference/edb-math/imports/authored-checkboxes/2026-10-16/topic-17592186049723/solution-repairs/prepare.py
```
