# Reproduction and verification

Run in the supplied workspace. `PY` below means `/home/jake/Developer/Course_Academy/.venv/bin/python`; `REPO` means `/home/jake/Developer/Course_Academy`; `JOB` means `$REPO/generate/repairs/2026-10-20-early-cohort/jobs/17592186124629`. These are command abbreviations, not runtime dependencies.

1. Initial failure: copy the original entrypoint and its source.json into an isolated temporary directory, then run `PY -I <copy>/17592186124629.py --difficulty moderate --count 5 --seed 24629 --format json`. Fails with StopIteration while searching parents for scripts/generator_policy.py. Exact stderr is in initial-failure.json. Original entrypoint is preserved in pre-repair-generator.py.
2. Initial shortcut: enumerate the original `batch('moderate', 100, 24629)` domain. All 18 semantic records across nine source templates have a single correct-answer vector per template; initial-shortcut.json records them. The new test reconstructs visible answer vectors instead of accepting sampler metadata.
3. `PY check_relocation.py`: PASS. Checks every runtime import against standard library and declared local files, copies only manifest files, then runs the actual CLI in isolated Python with only the relocated package added to the import path. Five records, no undeclared imports, no runtime-file writes. Result: relocation.json. Registered in ../repair-regressions.json using the retained packaging event code (history has no named findings).
4. `PY validate_repair.py`: PASS. Replays every complete source profile and bank, checks all prior eligible premise cases, evaluates visible implications against compatible rank witnesses, rejects the empty explicit checkbox mask, verifies unsupported bands and determinism, and writes source-replay-report.json, test-records.json, counterfactuals.json, native-input.json and pedagogical-variation.json. Current results: 15 banks, 81 complete choices / 54 distractors, 316 decision records, 12 legacy premise records; 106 identical-hypothesis cue groups across 14 recognizable profiles. The script calls the following shared tools once per validation pass:

   `REPO/generate/runs/current/check-engine evidence/native-input.json evidence/native-report.json`

   PASS: 623 accepted responses, 1,232 rejected responses, zero unresolved; zero database writes.

   `PY REPO/generate/pipeline/check_delivery.py --input evidence/test-records.json --source JOB/source/source.json --inventory JOB/source/inventory.json --difficulty moderate --output evidence/delivery --math-root /media/jake/SSD/EDB/math`

   PASS: 316 accepted. Coverage/cue probes are computed before and after filtering. Unclassified resolves to the declared moderate default; the shared tool requires the effective band.
5. `PY REPO/generate/pipeline/check_delivery.py --input evidence/samples.json --source JOB/source/source.json --inventory JOB/source/inventory.json --difficulty moderate --output evidence/delivery-samples --math-root /media/jake/SSD/EDB/math`

   PASS: requested sample accepted 5/5, no duplicates.
6. `PY REPO/generate/pipeline/render_preview.py --input evidence/render-records.json --output evidence/render --math-root /media/jake/SSD/EDB/math`

   PASS: five actual UI screenshots. Initial horizontal theorem clipping was found by visual inspection and repaired by stacking its equivalence. All five final screenshots inspected; see visual-review.json and render/rendering.json. No assets were generated or published.

7. `PY check_inventory.py`: PASS. Inspects all 16 captured IDs, verifies equality with original source IDs and absence of generator provenance, and saves the snapshot hash and inspected IDs in inventory-assessment.json. No stored generated instance of the runtime/structural findings exists in this snapshot. Original source errors are described separately; no original is marked generated.

Source fidelity, mathematics, grading, variation, delivery and visual layout are separate claims with the corresponding reports. Symbolic dimensions have representative rank witnesses at n=1,2,5,9; the lesson's universal theorem supplies the general justification. Database content was not edited. Live learner history, later inventory, and configured policy draws are outside the offline evidence.

## Targeted batch-selection repair (2026-10-21)

The earlier sections describe the completed construction/packaging repair. Current version 2.0.1 changes only finite batch ordering and the version metadata. Existing runtime helpers, source snapshot, question construction, banks, and worked solutions are unchanged.

Run the following commands from this workspace, using the `PY`, `REPO` and `JOB` abbreviations above:

1. Before editing: `PY -B failing_batch_check.py 17592186124629.py`. Copied verbatim from the supplied previous review. FAIL: exit 1, two det/col/pivot checkbox records both [false,true,false]. Exact stdout/stderr/command: batch-repair/reproduction.json. Runtime snapshot: batch-repair/before-generator.py. The regression recreates its complete records in batch-repair/before-records.json.
2. After editing: `PY -B check_relocation.py`. PASS: declared closure alone runs from a temporary relocated directory, Python 3.13.5, five records, no undeclared imports. See relocation.json.
3. `PY -B check_batch_selection.py`. PASS: exact reviewer assertion, source snapshot equality and 15 complete source bodies replayed, independent visible hypothesis/conclusion/solution witnesses, four additional five-item regression seeds, all eligible subsets in a 73-record selection prefix, and equality of the entire 606-instance old/new semantic domains. The script invokes shared delivery filtering twice (5 and 73 accepted, no duplicates) and the actual native grader once (12 records, 68 responses, 28 accepted/40 rejected). Full commands are in the script. Results: batch-repair/validation.json, source-replay.json, domain-preservation.json, strict-regression.json, counterfactuals.json and native-report.json. The matching complete records and delivery reports are in batch-repair/reported-batch.json, reported-batch-delivery/, decision-prefix.json and decision-prefix-delivery/.
4. `PY -B check_inventory.py`. PASS: all 16 captured entries are original source IDs and have no generator provenance. affected-inventory.json stays empty; inventory-assessment.json documents the verified scope. No database connection or writes.
5. `PY -B REPO/generate/pipeline/render_preview.py --input evidence/batch-repair/reported-batch-delivery/accepted.json --output evidence/batch-repair/render --asset-root evidence/batch-repair --math-root /media/jake/SSD/EDB/math`. PASS: five actual Learning UI renders. All five screenshots inspected. See batch-repair/render/rendering.json and batch-repair/visual-inspection.json.

The strict regression is retained unchanged. Additional checks identify families from printed propositions rather than accepting source-template metadata. The 73-record prefix exercises changed targets with compatible values and fixed theorem workload; its labels, positions, counts and subset probes run both before and after actual delivery. Singletons in the exact five-item batch do not independently demonstrate within-family variation. Live learner history and weighted selection remain untested, as recorded in the instructional account. No image publication, database changes, engine edits, or other-job edits occurred.
