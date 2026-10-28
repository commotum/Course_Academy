import json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=json.loads((H/'source-manifest.json').read_text());paths=M.get('q-334121',[]);out=[]
for p in paths:
 if not p.endswith('.json'):continue
 d=json.loads(Path(p).read_text());out.append({'path':p,'fields':d.get('fields',[]),'problem':d.get('problem'),'worked_solution':d.get('worked_solution')})
(H/'q334121-source-bank-evidence.json').write_text(json.dumps(out,indent=2));print('captures',len(out));
for d in out[:1]:
 for f in d['fields']:print(f['key'],f['type'],[(a.get('type'),a.get('value'))for a in f.get('choices',[])])
