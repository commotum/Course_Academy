# Targeted repair commands and results

Run from this workspace with `PYTHONDONTWRITEBYTECODE=1`. These paths invoke offline tools; no publication or database mutation occurs.

```bash
repo=/home/jake/Developer/Course_Academy
py="$repo/.venv/bin/python"
export PYTHONDONTWRITEBYTECODE=1
"$py" checks/single_witness.py
"$py" checks/validate.py
"$py" checks/prepare_targeted.py
"$repo/generate/runs/current/check-engine" evidence/grader-all-input.json evidence/grader-report.json
"$py" "$repo/generate/pipeline/check_delivery.py" --input evidence/delivery-input.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output evidence/delivery --asset-root evidence --math-root /media/jake/SSD/EDB/math
"$py" "$repo/generate/pipeline/check_delivery.py" --input evidence/samples.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output evidence/sample-delivery --asset-root evidence --math-root /media/jake/SSD/EDB/math
"$py" "$repo/generate/pipeline/check_delivery.py" --input evidence/single-witness-records.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output evidence/sparse-delivery --asset-root evidence --math-root /media/jake/SSD/EDB/math
"$py" checks/delivery_probe.py
"$py" checks/targeted_delivery.py
"$py" checks/package_check.py
"$py" "$repo/generate/pipeline/render_preview.py" --input evidence/render-input.json --output evidence/render-sparse --asset-root evidence/sparse-delivery/assets --math-root /media/jake/SSD/EDB/math
```

Original failure: exact seed-739 normal easy canonical parameters reproduced the density exception; command, stdout, stderr and parameters are in single-witness-before.json. The strict regression itself also exited 1 before the fix (single-witness-regression-before.stderr). The older five-question exhaustion counterexample remains in before.stderr and is retained in checks/validate.py. Both registered scripts now pass. The current finding ID dbcd1ab741c06c08a3a5 is registered in ../repair-regressions.json, alongside the earlier legacy event regression.

Fidelity: 11/11 supplied source banks and 55/55 choices replay, including original key, difficulty and solution presence/absence. Visible matrix contents and normalized prompt/solution prose match; source q-13769 remains ungraded raw evidence. All 11 source parameter sets also pass normal generation. The canonical single-witness example now passes normal CLI generation without a raw profile. See source-replay.json, validation.json and single-witness-acceptance.json.

Correctness: removed the same density rule from both parameter guard and catalog, without changing classification/witness construction. Independent parsing of visible matrices, keys, repeated solution matrices and printed witness coordinates passes. Full supported support domains are exercised in normal generation: easy 2x2=3, easy 3x3=15, moderate 3x3=15, authored hard 4x4=127. These counts include the diagonal contrast. All nonempty one-sided supports are also explicitly accepted. See single-witness-coverage.json. The previous five-question CLI passes with distinct structures and deterministic replay; exhaustion is now 19, and exclusion of 13 leaves exactly five.

Grading: one native harness invocation passed 60 correct selections and rejected 240 distractors. All six 3x3 sole-witness coordinates, the canonical example, relevant transpose/clearing controls and irrelevant sign/letter changes are included. No engine changes.

Decision variation: the finite easy catalog now has 18 structural patterns. Normal full-catalog sampling covers all six 3x3 sole-witness coordinates, rather than exposing them only through explicit parameters. Size/letter subgroups have multiple answers and answer positions vary. Within size and nonzero-count groups, both upper and lower occur. When the first above/below cell pair is zero, upper, lower and diagonal answers all remain possible, defeating the fixed-cell strategy. Empty off-diagonal support implies diagonal mathematically and is not an incidental cue. Controlled relevant changes update printed matrices, keys, solutions and native grades; irrelevant changes preserve the classification. See pedagogical-variation.json and targeted-delivery-probes.json.

Delivery: actual shared publisher filter retained 42/42 audit records, 10/10 sparse controls, 5/5 requested samples, with no duplicates. Visible mathematics, complete support sets, label/position cues and new density/fixed-cell probes pass after filtering. Read-only fresh-pool within-band selection probes retain all three classes under two surrogate orders; actual history-sensitive live selection remains untested. See delivery/delivery.json, sparse-delivery/delivery.json, sample-delivery/delivery.json and postdelivery-variation.json.

Rendering: actual Learning.html/learning.js UI passed three affected examples. Visually inspected all three screenshots: canonical lower matrix with a21=6, shifted lower matrix with a32=6, and a cleared diagonal contrast. Readable matrices, five options and full solutions; no clipping, overlaps or stale references observed. See render-inspection.json and render-sparse/rendering.json. Earlier upper-triangular rendering evidence remains under render/.

Packaging: manifest unchanged, only three declared runtime files needed. Python 3.13.5 and SymPy 1.14.0 match installed versions; requirements pinned. Relocation from those files produces an identical five-record array. See relocation.json.

Inventory: all 16 captured matrices inspected for the demonstrated former 3x3 sole-witness exclusion: zero matches. Fifteen available stored keys agree with independent classification; q-13769 has no stored key. affected-inventory.json is empty because no affected stored generated instance is demonstrated. This is a verified absence of the specified matrix pattern in the snapshot, with generated provenance unavailable; it is not a broader claim about historical generation. No original source was marked generated.

Limits: easy has 18 structural tasks; number changes do not enlarge the structural count. Identity and Other remain source-bank distractors rather than correct sampled families. The hard band is the retained authored 4x4 extension, not a source-observed hard rating. Live history, future entity IDs, policy configuration and inventory changes after basis 5451 remain untested. All changes are confined to this workspace; no images published and no engine/database content changed.
