from pathlib import Path
import sys,json,hashlib,subprocess,re,shutil
from urllib.parse import unquote,urlsplit
R=Path('/home/jake/Developer/Course_Academy');sys.path.insert(0,str(R/'scripts'))
from migrate_learner_history import connection,kw,loads
H=Path('/tmp/source-reconcile');O=R/'reference/edb-math/imports/oregon-state/2026-11-06-source-pdf-names'
plan=json.loads((H/'plan.json').read_text());p=json.loads((H/'db-plan.json').read_text())
for x in plan['files']:
 assert hashlib.sha256(Path(x['new']).read_bytes()).hexdigest()==x['sha256']
for x in plan['notes']:assert Path(x['new']).read_text()==x['after']
assert len(p['changes'])==33 and {x['attribute'] for x in p['changes']}=={':tutorial/content',':multistep/context'}
payload=H/'links.edn';assert hashlib.sha256(payload.read_bytes()).hexdigest()==p['sha256']
for x in p['changes']:
 for match in re.finditer(r'/api/(?:source|asset)\?path=([^\s\)<>#]+)',x['after']):
  asset=Path(unquote(match[1]));assert asset.is_file(),asset
O.mkdir(parents=True,exist_ok=True)
for name in ['db-plan.json','links.edn','db_apply.py']:
 target=O/name
 if target.exists(): assert target.read_bytes()==(H/name).read_bytes()
 else:shutil.copy2(H/name,target)
db=connection();receiptfile=O/'receipt.edn';intentfile=O/'intent.json'
if intentfile.exists():
 intent=json.loads(intentfile.read_text());assert intent['sha256']==p['sha256']
else:
 assert db.basis()==p['basis'],'Database changed; recompute from the known unsubmitted plan.'
 intent={'database':'math','source':p['source'],'basis':p['basis'],'file':str(O/'links.edn'),'endpoint':'/tmp/edb-math/writer.sock','sha256':p['sha256'],'request_key':p['request_key']}
 intentfile.write_text(json.dumps(intent,indent=2)+'\n')
receipt=loads(receiptfile.read_text()) if receiptfile.exists() and receiptfile.stat().st_size else None
if not isinstance(receipt,dict) or receipt.get(':edb/committed') is not True:
 preview=R/'.local/edb/f26-missing-2026-10-21/preview'
 run=subprocess.run([str(preview),intent['file']],env=db.env,capture_output=True,text=True,check=True,timeout=120)
 (O/'preview.txt').write_text(run.stdout+run.stderr)
 with receiptfile.open('w') as out,(O/'submit.stderr').open('w') as err:
  subprocess.run([db.args.edb_bin,'transact','--database',intent['database'],'--source',intent['source'],'--file',intent['file'],'--endpoint',intent['endpoint'],'--request-key',intent['request_key'],'--basis',str(intent['basis']),'--timeout-ms','120000'],env=db.env,stdout=out,stderr=err,check=True,timeout=160)
 receipt=loads(receiptfile.read_text())
assert receipt[':edb/committed'] is True
basis=receipt[':edb/db-after-t'];assert receipt[':edb/db-before-t']==intent['basis']
ids=sorted(set(x['entity'] for x in p['changes']))
rows=db.query('[:find (pull ?e [*]) :in $ [?e ...] :where [?e ?a ?v]]',[ids],O,'entities-after',basis)
before={x[':db/id']:x for x in p['records']};expected={e:dict(before[e]) for e in ids}
for x in p['changes']:expected[x['entity']][x['attribute']]=x['after']
for row in rows:
 actual=json.loads(json.dumps(row[0],default=str));assert actual==expected[actual[':db/id']],actual[':db/id']
learner=db.query('[:find (pull ?l [*]) :in $ ?id :where [?l :learner/id ?id]]',['59d5cf13-351c-4114-be19-4c3bb64ee051'],O,'learner-after',basis)[0][0]
assert json.loads(json.dumps(learner,default=str))==p['learner']
attrs=db.query('[:find ?e ?a :in $ [?a ...] :where [?e :db/ident ?a]]',[[kw('tutorial/content'),kw('multistep/context'),kw('db/txInstant')]],O,'attributes',basis)
byattr={str(a):e for e,a in attrs};allowed={(x['entity'],byattr[x['attribute']]) for x in p['changes']}
assert len(receipt[':edb/tx-data'])==2*len(p['changes'])+1
assert all((d[0],d[1]) in allowed or d[1]==byattr[':db/txInstant'] for d in receipt[':edb/tx-data'])
result={'committed':True,'basis':basis,'source_attributes_updated':len(p['changes']),'assignments_preserved':len(learner[':learner/assignments']),'learner_and_targets_preserved':True,'only_source_links_and_labels_changed':True,'assignment_pdfs':len(plan['files']),'printable_replacements':5}
(O/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
