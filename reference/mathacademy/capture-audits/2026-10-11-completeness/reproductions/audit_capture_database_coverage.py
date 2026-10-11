import json,threading,time,subprocess
from pathlib import Path
from scripts.config import Config
from scripts.database.client import EDBClient
root=Path('/home/jake/Developer/Course_Academy');legacy=json.loads(Path('/tmp/legacy-capture-completeness.json').read_text());new=json.loads(Path('/tmp/new-capture-completeness-extended.json').read_text());aux=json.loads(Path('/tmp/auxiliary-capture-completeness.json').read_text()); expected={};groups=[]
for r in legacy['captures']:
 d=root/'reference/mathacademy/question-capture'/r['task_id'];c=json.loads((d/'content.json').read_text());ids={q['math_academy_id'] for bucket in ['questions','canonical_examples'] for q in c.get(bucket,[]) if q.get('math_academy_id')}; groups.append({'engine':'legacy','task_id':r['task_id'],'ids':sorted(ids),'local_commit_verified':r['legacy_commit_verified']})
for r in new['captures']:
 d=root/'reference/mathacademy/capture'/r['account']/r['task_id'];c=json.loads((d/'content.json').read_text());ids={q['math_academy_id'] for bucket in ['questions','canonical_examples'] for q in c.get(bucket,[]) if q.get('math_academy_id')};groups.append({'engine':'new','account':r['account'],'task_id':r['task_id'],'ids':sorted(ids),'local_commit_verified':r['import_status']=='verified'})
for r in aux['captures']:groups.append({'engine':'auxiliary','task_id':r['task_id'],'ids':r['question_ids'],'capture_only':r.get('capture_only',False)})
ids=sorted({mid for g in groups for mid in g['ids']});c=EDBClient(Config(),threading.Event());identity=c.status();present=set();d=Path('/tmp/capture-audit-database/coverage');print('AUDITING',len(ids),'ids',json.dumps(identity),flush=True)
try:
 for start in range(0,len(ids),250):
  rows=c.query('[:find ?id :in $ [?id ...] :where [?q :question/math-academy-id ?id]]',[ids[start:start+250]],d,'identities-'+str(start),identity['basis']);present.update(r[0] for r in rows)
except subprocess.CalledProcessError as error:print(error.stderr,flush=True);raise
for g in groups:g['missing_ids']=sorted(set(g.pop('ids'))-present)
result={'identity':identity,'read_at':time.time(),'expected_unique_ids':len(ids),'present_unique_ids':len(present),'missing_unique_ids':sorted(set(ids)-present),'captures':groups,
 'limitations':'Identity presence does not establish complete fields, correct source attribution, structure membership, or mathematical correctness. Historical local commit verification does not bind a migrated database lineage.'}
Path('/tmp/capture-database-coverage.json').write_text(json.dumps(result,indent=2)+'\n');print('RESULT',len(present),'present;',len(ids)-len(present),'absent',flush=True)
