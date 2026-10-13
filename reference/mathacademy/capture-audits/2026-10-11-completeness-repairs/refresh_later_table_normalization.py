"""Fresh normal imports only for the two verified complex-table packages."""
from pathlib import Path
import argparse, hashlib, json, threading, time
from scripts.config import Config
from scripts import recovery
from scripts.database.pipeline import DatabasePipeline
from scripts.database.evidence import authoritative_question
from scripts.database.images import ImageLibrary
from scripts.database.text import markdown
from scripts.database.edn import loads
from scripts.storage import atomic_json, file_lock, read_json
ROOT=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('offset',type=int,choices=[7,32]);a=p.parse_args()
account,task,ids=('multivariable','14111253',['q-335106']) if a.offset==7 else ('differential','14110945',['q-350398','q-143316','q-149651'])
config=Config(account=account);d=config.output_root/task
artifact=ROOT/f'later-table-normalization-refresh-{a.offset}.json'
protected=['checkpoint.json','capture-complete.json','post-activity.json','content.json']
sha=lambda path:hashlib.sha256(path.read_bytes()).hexdigest()
before={name:sha(d/name) for name in protected}
original_result=read_json(d/'database/result.json')
assert original_result['status'] in ('verified','no_changes')
expected_omissions=original_result.get('omissions',[])
assert not (d/'database/request.json').exists()
assert (read_json(config.state_root/'active.json',{}) or {}).get('directory')!=str(d)
record={'account':account,'task_id':task,'version':recovery.version(),'text_sha256':sha(Path(markdown.__code__.co_filename)),'protected_sha256':before,'started_at':time.time()}
with file_lock(config.database_lock):
 pipeline=DatabasePipeline(config,threading.Event())
 preview=pipeline.process(d,apply=False);record['preview']=preview
 assert preview['status'] in ('previewed','no_changes'),preview
 assert preview.get('omissions',[])==expected_omissions,preview
 if preview['status']=='previewed':
  applied=pipeline.process(d,apply=True);record['apply']=applied
  assert applied['status'] in ('verified','no_changes'),applied
  assert applied.get('omissions',[])==expected_omissions,applied
 repeat=pipeline.process(d,apply=False);record['repeat_preview']=repeat
 assert repeat['status']=='no_changes' and repeat.get('omissions',[])==expected_omissions,repeat
 basis=repeat['basis'];observed={}
 def collect(x):
  if isinstance(x,dict):
   if x.get(':question/math-academy-id'):observed[x[':question/math-academy-id']]=x
   for v in x.values():collect(v)
  elif isinstance(x,list):
   for v in x:collect(v)
 for path in (d/'database'/f'snapshot-{basis}').glob('questions-*.edn'):
  if '-inputs' not in path.name and '-query' not in path.name:collect(loads(path.read_text()))
 content=read_json(d/'content.json');library=ImageLibrary(config.math_root,d);checks=[]
 for q in content['questions']:
  if q.get('math_academy_id') not in ids:continue
  expected=library.question(authoritative_question(q));db=observed[q['math_academy_id']]
  check={'id':q['math_academy_id'],'basis':basis,'values':{}}
  for key in ('problem','worked_solution'):
   value=markdown(expected[key]);actual=db[':question/'+key.replace('_','-')]
   check['values'][key]={'matches':value==actual,'expected_sha256':hashlib.sha256(value.encode()).hexdigest(),'expected':value,'observed':actual}
   assert value==actual,(q['math_academy_id'],key)
  checks.append(check)
 record['pinned_table_readbacks']=checks
 record['preservation']={name:before[name]==sha(d/name) for name in protected}
 assert all(record['preservation'].values())
record['completed_at']=time.time();atomic_json(artifact,record)
print(json.dumps({'artifact':str(artifact),'preview':preview['status'],'basis':basis,'tables':len(checks),'preserved':True}))
