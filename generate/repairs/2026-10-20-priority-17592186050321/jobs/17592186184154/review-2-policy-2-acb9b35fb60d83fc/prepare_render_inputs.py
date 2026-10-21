import json
from pathlib import Path
E=Path(__file__).resolve().parent
load=lambda n:json.loads((E/n).read_text())
controlled=load('controlled.json');replays=load('source-replays.json');pairs=load('counterfactuals.json');rp=load('revision-counterfactuals.json')
records=replays[:2]+[controlled[i] for i in range(0,40,4)]+[r for p in pairs for r in [p['before'],p['after']]]
records += [r for p in rp[:3] for r in [p['before'],p['after']]]+load('delivery-batch/accepted.json')
remaining=[r for p in rp[3:] for r in [p['before'],p['after']]]
assert len(records)==45 and len(remaining)==22
for name,data in [('render-records.json',records),('render-revision-records.json',remaining)]:
 p=E/name
 if p.exists():assert json.loads(p.read_text())==data
 p.write_text(json.dumps(data,indent=2)+'\n')
