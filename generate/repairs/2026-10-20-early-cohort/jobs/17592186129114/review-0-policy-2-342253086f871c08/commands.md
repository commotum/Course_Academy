All commands run from this evidence directory. Package files were read only; bytecode writes disabled for generator imports. No publication or database command was used.

```sh
PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python audit.py
/home/jake/Developer/Course_Academy/generate/runs/current/check-engine grader-input.json grader-results.json
/home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py --input independent-samples.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output delivery-independent --asset-root ../workspace --math-root /media/jake/SSD/EDB/math
/home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py --input runner-batch.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output delivery-batch --asset-root ../workspace --math-root /media/jake/SSD/EDB/math
/home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input render-records.json --output render --limit 6 --asset-root ../workspace --math-root /media/jake/SSD/EDB/math
/home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input render-remaining.json --output render-remaining --limit 4 --asset-root ../workspace --math-root /media/jake/SSD/EDB/math
PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python inventory_probe.py
/home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py --input inventory-reproduction-input.json --source ../source/source.json --inventory inventory-empty-for-identity-check.json --difficulty easy --output inventory-identity --asset-root ../workspace --math-root /media/jake/SSD/EDB/math
python3 batch_role_probe.py delivery-batch/accepted.json batch-role-results.json
# Expected failure: C selected 5, unselected 0. Exit status 1.
python3 batch_role_probe.py delivery-independent/accepted.json control-role-results.json
# Control passes: C selected 204, unselected 180.
PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python c_counterfactual.py
/home/jake/Developer/Course_Academy/generate/runs/current/check-engine c-counterfactual-grader-input.json c-counterfactual-grader-results.json
/home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input c-counterfactual-records.json --output render-c-counterfactual --limit 2 --asset-root ../workspace --math-root /media/jake/SSD/EDB/math
python3 delivery_analysis.py
python3 finalize_evidence.py
```

Fresh profile seeds: 81731–81762 per supported profile; normal batch seed 920113; relocated package seed 802139. Runner seeds and all explicit counterfactual matrices are preserved in the record files. Inventory original seeds were not captured; explicit matrix parameters reproduce normalized stored UUIDs.

The strict batch regression checks a finite-pool action shortcut. It does not claim that every five-item random draw must contain every outcome or follow equal quotas. It fails this role-variable pool because one visible label supplies the correct response to the same independent checkbox decision in every item. It does not claim that selecting C completes the whole question.
