All commands below run from this evidence directory; scripts use the supplied absolute job paths. No publishing or database-writing command was used. `-B` prevents bytecode cache writes into original packages.

```bash
/home/jake/Developer/Course_Academy/.venv/bin/python -B review.py
/home/jake/Developer/Course_Academy/generate/runs/current/check-engine native-input.json native-results.json
/home/jake/Developer/Course_Academy/.venv/bin/python -B /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py --input all-records.json --source ../source/source.json --inventory ../source/inventory.json --difficulty moderate --output delivery --asset-root runtime --math-root /media/jake/SSD/EDB/math
/home/jake/Developer/Course_Academy/.venv/bin/python -B /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py --input runner-batch.json --source ../source/source.json --inventory ../source/inventory.json --difficulty moderate --output batch-delivery --asset-root runtime --math-root /media/jake/SSD/EDB/math
/home/jake/Developer/Course_Academy/.venv/bin/python -B stages.py
/home/jake/Developer/Course_Academy/generate/runs/current/check-engine delivered-native-input.json delivered-native-results.json
/home/jake/Developer/Course_Academy/.venv/bin/python -B rejection_probe.py
/home/jake/Developer/Course_Academy/.venv/bin/python -B inspect_delivery.py
/home/jake/Developer/Course_Academy/.venv/bin/python -B /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input render-records.json --output render --asset-root delivery/assets --asset-root runtime --math-root /media/jake/SSD/EDB/math
```

The first renderer invocation used its default six-record limit. To reproduce the remaining five previews:

```bash
python3 -B - <<'PY'
import json
records=json.load(open('render-records.json'))
json.dump(records[6:],open('render-remaining-records.json','w'),indent=2)
PY
/home/jake/Developer/Course_Academy/.venv/bin/python -B /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input render-remaining-records.json --output render-remaining --asset-root delivery/assets --asset-root runtime --math-root /media/jake/SSD/EDB/math --limit 5
/home/jake/Developer/Course_Academy/.venv/bin/python -B finalize.py
```

`review.py` preserves exact commands and results for legacy failing invocations, copied author checks, relocated CLI counts and deterministic replay in `runtime-results.json`. It checks fresh seed 694821; controlled panels use seed 832715, boundaries use 3329. `rejection_probe.py` reproduces the identity-swap rejection with parameters `["q-130098",0,0,-2,[0,1,2],0]` and finds seed 429 whose initial rejected proposal is resampled to a full five-record batch. `stages.py` retains explicit selection scenarios and the proposal trace.

Source reconstruction was written and verified before package inspection. The original source is immutable; `source-analysis.json` records missing evidence. The historical fixed-key and CLI defects are retained as failing baselines, not current findings. The initial package file snapshot was compared byte-for-byte after the audit.
