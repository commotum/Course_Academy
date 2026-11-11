import hashlib,json,shutil
from pathlib import Path
H=Path(__file__).resolve().parent
selected={17592186096652:[('easy',20261111,0),('easy',20261111,2),('moderate',20261111,0),('moderate',20261111,2),('hard',20261111,0),('hard',20261111,1)],17592186096653:[('easy',20261111,0),('easy',20261111,2),('moderate',20261111,1),('moderate',20261111,2),('hard',20261111,1),('hard',20261111,2)],17592186096701:[('easy',20261111,0),('easy',20261111,1),('moderate',20261111,0),('moderate',20261111,1),('hard',20261111,0),('hard',20261111,2)]}
# Include a distinct known-multiple family if present in the second saved seed.
x=json.loads((H/'17592186096701/samples/moderate/47/delivery/accepted.json').read_text())
for i,r in enumerate(x):
 if r['generation']['parameters']['profile']=='multiple':selected[17592186096701].append(('moderate',47,i));break
for kp,cases in selected.items():
 d=H/str(kp);rows=[];mapping=[];assets=d/'ui-assets';assets.mkdir(exist_ok=True)
 for band,seed,index in cases:
  source=d/'samples'/band/str(seed)/'delivery';rec=json.loads((source/'accepted.json').read_text())[index];rows.append(rec);mapping.append(dict(index=len(rows)-1,source=str((source/'accepted.json').relative_to(H)),source_index=index,band=band,seed=seed,question_uuid=rec['question'][':question/id']))
  for p in (source/'assets').rglob('*'):
   if p.is_file():target=assets/p.relative_to(source/'assets');target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,target)
 (d/'ui-records.json').write_text(json.dumps(rows,indent=2)+'\n');(d/'ui-map.json').write_text(json.dumps(mapping,indent=2)+'\n')
