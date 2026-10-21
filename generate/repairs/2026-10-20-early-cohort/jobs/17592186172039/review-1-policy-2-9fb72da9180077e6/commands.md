All commands run from this evidence directory. PYTHONDONTWRITEBYTECODE=1 prevents writes into the package. audit.py additionally directs generated assets, matplotlib config and cache into this directory.

1. `/home/jake/Developer/Course_Academy/.venv/bin/python audit.py`
2. `PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python inventory_replay.py`
3. `PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python boundary_checks.py`
4. For each `INPUT,OUTPUT` pair `samples-moderate.json,delivery-samples` and `batch.json,delivery-batch`:
   `/home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py --input INPUT --source ../source/source.json --inventory ../source/inventory.json --difficulty moderate --output OUTPUT --asset-root assets --math-root /media/jake/SSD/EDB/math`
5. `python3 analyze_delivery.py`
6. `/home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input render-records.json --output render --asset-root assets --asset-root delivery-batch/assets --math-root /media/jake/SSD/EDB/math --limit 12`
7. `/home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input render-extra-records.json --output render-extra --asset-root assets --math-root /media/jake/SSD/EDB/math --limit 3`
8. `PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python finish_validation.py`
9. `/home/jake/Developer/Course_Academy/generate/runs/current/check-engine native-input.json native-report.json`
10. `python3 finalize_report.py`

The render inputs and full sampled records are retained. The initial renderer invocation used its default limit of 6; it was rerun with explicit limit 12 to cover every controlled pair and all five runner records. An initial source replay omitted the historical bank profile and consequently added the generator's authored parity explanation; replay was corrected to supply the source bank profiles. Neither observation was a generator defect.

No author test script was executed against its original writable output path. The legacy import counterexample is replayed with a virtual isolated __file__ ancestry, because the entire evidence directory itself remains nested under the repository. The current manifest-only runtime is copied to relocated/ and runs with PYTHONPATH empty, local helper imports and external assets.
