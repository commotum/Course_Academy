All writes are under this evidence directory. Package imports use Python -B and sys.dont_write_bytecode. Job Python: /home/jake/Developer/Course_Academy/.venv/bin/python. Repository: /home/jake/Developer/Course_Academy.

Reproduction sequence (working directory = evidence_root):

```bash
/home/jake/Developer/Course_Academy/.venv/bin/python -B review.py
/home/jake/Developer/Course_Academy/.venv/bin/python -B additional_pairs.py
/home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py --input samples.json --source ../source/source.json --inventory ../source/inventory.json --difficulty moderate --output delivery --asset-root ../workspace --math-root /media/jake/SSD/EDB/math
/home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py --input runner-batch.json --source ../source/source.json --inventory ../source/inventory.json --difficulty moderate --output batch-delivery --asset-root ../workspace --math-root /media/jake/SSD/EDB/math
/home/jake/Developer/Course_Academy/.venv/bin/python -B revision_probes.py
/home/jake/Developer/Course_Academy/.venv/bin/python -B variation_checks_fast.py
/home/jake/Developer/Course_Academy/.venv/bin/python -B selection_check.py
/home/jake/Developer/Course_Academy/.venv/bin/python -B confirm_rank.py
/home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py --input rank-holdout-records.json --source ../source/source.json --inventory ../source/inventory.json --difficulty moderate --output rank-delivery --asset-root ../workspace --math-root /media/jake/SSD/EDB/math
/home/jake/Developer/Course_Academy/.venv/bin/python -B confirm_rank.py --analyze
/home/jake/Developer/Course_Academy/generate/runs/current/check-engine grader-input-final.json grading-final.json
/home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input render-records.json --output render-full --limit 31 --asset-root ../workspace --math-root /media/jake/SSD/EDB/math
/home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input rank-render-records.json --output render-rank --limit 2 --asset-root ../workspace --math-root /media/jake/SSD/EDB/math
python3 finalize_review.py
```

Review seeds: 20491029,7139851,922710 (120 records each). Holdout seed: 94172863 (480 mixed records; predeclared P exponent-2 subgroup 35). CLI replay seed 720519. Explicit boundaries and pairs are retained in scripts and JSON. Earlier scripts are reused with provenance in script-provenance.json; current checks are rerun. Initial inherited polynomial factors were invalid under the revised factor domain; the test was corrected to preserve eligible wrong divisors 2 and 8 while updating relative factors with n. This was an audit-adaptation error, not a generator defect. Full render rerun uses --limit 31 because the interface default renders only six records.

No publication preparation file exists. Delivery uses the actual shared read-only publisher filter at captured basis 5277. Selection is a source-confirmed read-only reproduction with synthetic appended IDs and five policy/history scenarios, not a claim about unobserved live state. No database or publishing tools were invoked.
