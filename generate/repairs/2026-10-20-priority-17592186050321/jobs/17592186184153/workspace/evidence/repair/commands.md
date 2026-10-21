# Current repair: reproducible commands and results

Run from the supplied workspace with Python 3.13.5. Runtime uses only the standard library; independent validation uses the job environment's SymPy and existing native grader/UI tools. All writes are local evidence. No publication or database operations.

```bash
/home/jake/Developer/Course_Academy/.venv/bin/python repair_validate.py > evidence/repair/prepare.log 2>&1
/home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py --input evidence/repair/records.json --source ../source/source.json --inventory ../source/inventory.json --difficulty moderate --output evidence/repair/delivery --asset-root evidence/repair --math-root /media/jake/SSD/EDB/math > evidence/repair/delivery.log 2>&1
/home/jake/Developer/Course_Academy/generate/runs/current/check-engine evidence/repair/grader-input.json evidence/repair/grading.json > evidence/repair/grading.log 2>&1
/home/jake/Developer/Course_Academy/.venv/bin/python repair_validate.py --after-delivery > evidence/repair/after-delivery.log 2>&1
/home/jake/Developer/Course_Academy/generate/runs/current/check-engine evidence/repair/delivered-grader-input.json evidence/repair/delivered-grading.json > evidence/repair/delivered-grading.log 2>&1
python3 /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input evidence/repair/render-records.json --output evidence/repair/render --asset-root evidence/repair --math-root /media/jake/SSD/EDB/math --limit 6 > evidence/repair/render.log 2>&1
/home/jake/Developer/Course_Academy/.venv/bin/python repair_controls.py > evidence/repair/rank-controls.log 2>&1
/home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py --input evidence/repair/rank-controls.json --source ../source/source.json --inventory ../source/inventory.json --difficulty moderate --output evidence/repair/rank-controls-delivery --asset-root evidence/repair --math-root /media/jake/SSD/EDB/math > evidence/repair/rank-controls-delivery.log 2>&1
/home/jake/Developer/Course_Academy/.venv/bin/python repair_controls.py --after-delivery > evidence/repair/selection.log 2>&1
/home/jake/Developer/Course_Academy/generate/runs/current/check-engine evidence/repair/rank-controls-grader-input.json evidence/repair/rank-controls-grading.json > evidence/repair/rank-controls-grading.log 2>&1
```

`repair_controls.py` was first run through its after-delivery step before the selection-coverage report was added; its final command above reruns only that affected stage. All resulting reports are final/current. The supplemental render input contains the first and third n=5 records with s=1, constant_first=true from `rank-controls-delivery/accepted.json`:

```python
import json
from pathlib import Path
records = json.loads(Path('evidence/repair/rank-controls-delivery/accepted.json').read_text())
group = [r for r in records if r['generation']['parameters']['s']==1 and r['generation']['parameters']['constant_first']]
Path('evidence/repair/rank-render-records.json').write_text(json.dumps([group[0],group[2]],indent=2)+'\n')
```

```bash
python3 /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input evidence/repair/rank-render-records.json --output evidence/repair/rank-render --asset-root evidence/repair/rank-controls-delivery/assets --math-root /media/jake/SSD/EDB/math --limit 2 > evidence/repair/rank-render.log 2>&1
```

## Claims and evidence

- Fidelity: seven original antiderivatives replayed; all 21 captured choices retained and compared, including four full radio banks. Two moderate source banks reconstructed from recipes. Bundled source exactly matches the seven supplied source records (`source-snapshot.json`). Existing missing evidence and restored derivative premise remain documented.
- Correctness: all 840 polynomial divisor-pair/sign/omitted-cell instances pass exact independent differentiation and unique-answer checks; 105 complete printed banks independently parsed with SymPy. Also 16 P boundaries, 73 fresh P records, eight R/B regression records and 22 controlled pairs pass. The additional 12 n=5 controls pass independently. See `validation.json`, `exhaustive.json`, `counterfactuals.json` and `rank-controls-results.json`.
- Grading: native application grading passes 141 accepted/498 rejected in the source/boundary/control/regression suite, 73 accepted/292 rejected across every delivered P option, and 12 accepted/48 rejected across all supplementary delivered control options. Total 226 accepted/838 rejected checks, no unexpected or unresolved outcomes. Blank equivalents and incorrect expressions included.
- Variation: the exact review strategy uniquely identifies zero of 27 fresh n=4/6 records, before and after delivery; it leaves two or three candidates. The full polynomial coefficient domain has no unique typography cue. Position/length-rank/single-summand checks pass for both radio templates, including exponent and sign/order groups. The small normal n=5 subgroup's eight cases all happened to have smallest constant-matched coefficient magnitude; twelve controlled delivered records demonstrate every rank for each sign/order without changing integrands or keys. This is explicitly reported rather than treating the sample as proof of balance. No sampling quota was introduced.
- Delivery: 240 fresh seed-86184906 records become 218 after 22 duplicates, preserving all 168 semantic integrands and every declared slot. All 12 targeted controls survive separately. Shared tool uses actual publisher normalization/deduplication with captured inventory basis 5277.
- Selection: read-only within-positive-moderate-band reproduction over the combined 230-item validation pool, 1,024 synthetic draws; 228 distinct records/166 semantic instances selected, all 12 control records represented. P=369/R=333/B=322. Coverage and the repaired cue are checked on the selected records too. This is a validation pool containing targeted controls; it is not a claim about a live random batch, learner history or production ID ordering. All 230 have positive selection probability under a positive moderate weight. No-policy selection and live exclusions remain unavailable offline.
- Rendering: six current representatives and two supplemental same-integrand n=5 banks pass the actual UI renderer; all eight screenshots were visually inspected. Polynomial fractions, signs, full answer banks, worked steps, reciprocal radicals and blank with external C are legible, with no exposed TeX or clipping. See both rendering.json files and `visual-inspection.json`.
- Packaging: generator v1.1.0 is deterministic and relocates using exactly the manifest's three runtime files; Python 3.13.5 and no third-party runtime packages. Invalid explicit grid assignments and unsupported easy/hard bands are rejected. Current five-item sample: `sample.json`.

All claims apply to the supported moderate domain and tested strategies. Prior v1 evidence is historical. Source-fidelity limitations, later constant-factor knowledge point boundary, and unsupported source response contracts remain in `instructional-account.md`.
