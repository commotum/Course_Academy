import json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4];p=R/'reference/edb-math/repairs/2026-10-26-structural-math/recover_formulas.py';ns={'__file__':str(p)};exec(compile(p.read_text().split('index=collections.defaultdict(list)')[0],str(p),'exec'),ns);S=json.loads((H/'sources.json').read_text())
changed=0
for i,s in enumerate(S):
 fs=ns['formulas'](s['html']);changed+=fs!=s['formulas'];s['formulas']=fs
 if i%200==0:print(i,'updated',changed,flush=True)
(H/'sources.json').write_text(json.dumps(S,indent=2));print('changed source records',changed)
