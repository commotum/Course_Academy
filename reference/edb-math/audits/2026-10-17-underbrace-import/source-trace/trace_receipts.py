import sys,json,uuid,datetime
sys.dont_write_bytecode=True
from pathlib import Path
R=Path('/home/jake/Developer/Course_Academy');O=Path('/tmp/underbrace-import-trace-agent');sys.path.insert(0,str(R/'capture'));from scripts.database.edn import loads
records=[]
for rel in ['reference/edb-math/imports/math-academy/lessons/receipts/lessons-0003.edn','reference/edb-math/imports/math-academy/newer-captures/receipts/052-tutorials-commit.edn']:
 x=loads((R/rel).read_text());ids={r[0] for r in x[':edb/tx-data'] if r[2]==uuid.UUID('40bcba62-6d88-5cfd-9d89-e773514e5a63')};ids.update(v for k,v in x[':edb/tempids'].items() if str(k)=='tutorial-40bcba62-6d88-5cfd-9d89-e773514e5a63')
 records.append({'path':rel,'basis_before':x[':edb/db-before-t'],'basis_after':x[':edb/db-after-t'],'committed':x[':edb/committed'],'tutorial_eids':list(ids),'datoms':[r for r in x[':edb/tx-data'] if r[0] in ids],'txmeta':[r for r in x[':edb/tx-data'] if r[0]>10000000000000 and r[0]<14000000000000]})
(O/'archived-receipt-evidence.json').write_text(json.dumps(records,ensure_ascii=False,indent=2,default=str)+'\n')
for r in records:
 print({k:v for k,v in r.items() if k not in ['datoms','txmeta']});print('matchingdatoms',len(r['datoms']));print('times',r['txmeta'][:2])
