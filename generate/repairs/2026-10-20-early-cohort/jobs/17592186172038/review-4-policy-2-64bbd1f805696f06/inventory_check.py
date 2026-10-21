import json,pathlib,copy,hashlib
from pixel_probe import main as pixel_main
ROOT=pathlib.Path.cwd();JOB=ROOT.parent
archive=JOB/'workspace/17592186172038/reference/replenishment/basis-2383/generated.json'
hist={r['question'][':question/id']:r for r in json.loads(archive.read_text())};inventory=json.loads((JOB/'source/inventory.json').read_text());records=[];checks=[]
norm=lambda t:t.replace('\\left','').replace('\\right','')
for q in inventory['questions']:
 if q.get(':question/math-academy-id'):continue
 h=hist[q[':question/id']];hq=h['question'];f=q[':question/answer-fields'][0];hf=hq[':question/answer-fields'][0]
 assert norm(q[':question/problem'])==norm(hq[':question/problem'])
 assert norm(q[':question/worked-solution'])==norm(hq[':question/worked-solution'])
 assert f[':answer-field/correct'][':answer/id']==hf[':answer-field/correct'][1]
 assert {a[':answer/id']:a[':answer/value'] for a in f[':answer-field/choices']}=={a[':answer/id']:a[':answer/value'] for a in hf[':answer-field/choices']}
 rec={**copy.deepcopy(h),'question':copy.deepcopy(q)};assert rec['generation']==h['generation'];verified=[]
 for a in h['generation']['published_assets']:
  path=pathlib.Path('/media/jake/SSD/EDB/math')/a['database_path'];assert hashlib.sha256(path.read_bytes()).hexdigest()==a['sha256'];verified.append(a['database_path'])
 records.append(rec);checks.append({'question_id':q[':question/id'],'entity_id':q[':db/id'],'generation_seed':h['generation']['seed'],'version':h['generation']['version'],'original_generation_equal':True,'complete_stored_question_equal':rec['question']==q,'stored_bank_key_and_normalized_prose_match_archive':True,'canonical_asset_hashes_verified':verified})
(ROOT/'generated-records.json').write_text(json.dumps(records,indent=2))
(ROOT/'inventory-record-provenance.json').write_text(json.dumps({'historical_archive':str(archive),'archive_sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),'basis':inventory['basis'],'method':'Reconstruct full stored generated records from historical generation plus exact captured question. Independently verify UUIDs, full bank, key, normalized prose, metadata identity and canonical image hashes. Source questions are never labeled generated.','records':checks},indent=2))
pixel_main()
affected=json.loads((ROOT/'affected-inventory.json').read_text());ids={r['question'][':question/id'] for r in records}
for q in affected['affected_questions']:
 assert q['question_id'] in ids;q['evidence_path']='generated-records.json';q['reproduction']='PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python inventory_check.py; '+q['reproduction']
(ROOT/'affected-inventory.json').write_text(json.dumps(affected,indent=2))
print('reconstructed',len(records),'historical generated records; source questions kept separate')
