# Targeted repair verification

Repaired finding `e00c00847a8d35dee226` and retained
`6900891930e4bdc756fa` plus the external-import regression. The old sampler's
opposite-label requirement forced two singleton answers, excluding the joint
outcome. Repeated profiles now receive their complete semantic decision set in
one label-to-shape and bank subgroup. Profile allocation changes when needed to
fit the requested count. Short batches can have singleton profiles; these make
no conditional-coverage claim. `runtime.patch` records the runtime change.

The source account was amended before implementation. All matrices, banks,
source profiles, source replay parameters and record IDs are preserved: current
catalog equality against retained evidence verifies 39 presentations and 24
semantic instances. No runtime mathematical construction was changed.

- Fidelity: ten complete source questions, 15 fields/banks and 54 choices replay
  against the supplied source. Two original questions lack keys/solutions and
  remain explicitly outside verified replay, as before.
- Correctness: independent Fraction elimination reads visible matrices; decoded
  banks, keys and worked-solution rank/dimension assertions agree. Controlled
  A-only to A+C changes only C; C-only to A+C changes only A. B is unchanged in
  both controls. Stale keys and solutions fail; nonzero scaling preserves ranks
  and the response.
- Grading: the two targeted scripts together exercise 47 expected acceptances
  and 108 expected rejections with the native learner grader, zero unresolved.
  Both versions of “inspect one eligible matrix and assume exclusivity” are
  rejected on the delivered joint case. Hardcoding A fails on delivered C-only.
- Decision variation: exact original and latest runner candidate prefixes now
  retain A-only, C-only and A+C within the affected subgroup. The latest review's
  original checker also passes (shortcut succeeds 2/3, failing the joint case).
  The stronger check tests each eligible subset matrix for independent decision
  influence, both within shape-multiset groups and label-to-shape groups.
  Fixed labels, constant positions and fixed subset counts are separately
  probed. Matrix-radio's singular-answer cardinality is a source contract.
- Delivery: ten actual read-only filtering runs retain all 88 input records.
  Checks repeat on accepted records. These are validation runs, not 88 distinct
  semantic instances. Sample controls include counts 0, 1, 2, 3, 4, 5, 23 and 24;
  both full-capacity runs retain all 24 semantic classes. No hidden generator
  rejection/resampling was introduced: finite construction, semantic deduplication,
  complete-case allocation, then seeded interleaving.
- Rendering: three actual-UI screenshots were opened and visually inspected.
  A-only, C-only and joint cases have readable unclipped matrices, all controls
  and complete solutions. `visual-review.json` and `render/rendering.json` record
  inspection and automated results.
- Packaging: declared-only relocation and two deterministic CLI executions pass.
  Installed Python 3.13.5 and SymPy 1.14.0 match the unchanged manifest/pins.
- Inventory: twelve stored items are verified original sources, with no stored
  generated instances of these batch defects. Ten complete originals were
  independently checked; two incomplete originals remain untestable. See
  `../../affected-inventory.json` and `../inventory-audit.json`. The empty affected
  list is not a claim that missing source keys were verified.

Commands (run from workspace; PY is
`/home/jake/Developer/Course_Academy/.venv/bin/python`):

```sh
# Exact latest failure, before implementation: expected exit 1, 2/2 successes.
$PY -B ../review-2-policy-2-7a41c9f08b6c9942/check_exclusive_subset.py --input ../review-2-policy-2-7a41c9f08b6c9942/delivery-batch/accepted.json --report evidence/repair-3/latest-failure.json
$PY -B checks/check_batch_decisions.py
$PY -B checks/check_exclusive_subset.py
$PY -B checks/check_runtime.py
$PY -B checks/audit_inventory.py
$PY -B 17592186119848.py --difficulty easy --count 5 --seed 0 --format json > evidence/repair-3/cli-sample.json
$PY -B ../review-2-policy-2-7a41c9f08b6c9942/check_exclusive_subset.py --input evidence/repair-3/exact-prefix-repaired-delivery/accepted.json --report evidence/repair-3/reviewer-check-current.json --native-input evidence/repair-3/reviewer-shortcut-grader-input.json
$PY -B /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input evidence/repair-3/render-records.json --output evidence/repair-3/render --asset-root evidence/repair-3/assets --math-root /media/jake/SSD/EDB/math
```

Full inputs and results are adjacent. Exact subprocess commands for the shared
`check_delivery.py` and native `check-engine` are recorded in
`exclusive-regression.json` and `retained-first/batch-regression.json`.
`repair-regressions.json` declares all retained checks; each uses current runtime
records, and both historical counterexamples remain failing negative controls.

Limits: publication and learner history were not exercised. The inspected
`question_selection.rs` selects uniformly within a configured positive-weight
fresh difficulty band; its unconfigured fallback picks the first sorted entity.
Neither guarantees a particular learner sequence. Captured inventory is basis
5415; future inventory, histories or reservations may remove cases or exhaust
this finite family. Conditional support in the checked delivered pool is the
verified claim. Earlier repair-2 evidence remains historical; its two-singleton
sufficiency claim is superseded by this repair. No database, engine, published
image, publication, or other-job content was edited.
