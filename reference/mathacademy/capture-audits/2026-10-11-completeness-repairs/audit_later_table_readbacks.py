"""Check all four authored complex tables against latest verified pinned values."""
from pathlib import Path
import hashlib,json
from scripts.config import Config
from scripts.storage import atomic_json,read_json
from scripts.database.edn import loads
from scripts.database.images import ImageLibrary
from scripts.database.evidence import authoritative_question
from scripts.database.text import markdown
from scripts.browser.adapter import EXTRACT
ROOT=Path(__file__).resolve().parent;rows=[]
for account,task,ids in [('multivariable','14111253',['q-335106']),('differential','14110945',['q-350398','q-143316','q-149651'])]:
 d=ROOT.parents[1]/'capture'/account/task;c=read_json(d/'content.json');result=read_json(d/'database/result.json');assert result['status'] in ('verified','no_changes')
 basis=result['basis'];observed={}
 def collect(x):
  if isinstance(x,dict):
   if x.get(':question/math-academy-id'):observed[x[':question/math-academy-id']]=x
   for v in x.values():collect(v)
  elif isinstance(x,list):
   for v in x:collect(v)
 for p in (d/'database'/f'snapshot-{basis}').glob('questions-*.edn'):
  if '-inputs' not in p.name and '-query' not in p.name:collect(loads(p.read_text()))
 library=ImageLibrary(Config(account=account).math_root,d)
 for original in c['questions']:
  if original.get('math_academy_id') not in ids:continue
  q=library.question(authoritative_question(original));db=observed[original['math_academy_id']];values={}
  for key in ['problem','worked_solution']:
   expected=markdown(q[key]);actual=db.get(':question/'+key.replace('_','-'))
   values[key]={'matches':expected==actual,'expected':expected,'observed':actual,'expected_sha256':hashlib.sha256(expected.encode()).hexdigest()}
   assert expected==actual,(task,original['math_academy_id'],key)
  source=original['recovery']['original_source'];raw=Path(source).read_bytes();assert hashlib.sha256(raw).hexdigest()==original['recovery']['source_sha256']
  rows.append({'account':account,'task_id':task,'id':original['math_academy_id'],'basis':basis,'source_html':source,'source_sha256':hashlib.sha256(raw).hexdigest(),'values':values})
assert len(rows)==4
atomic_json(ROOT/'later-complex-table-pinned-readbacks.json',{'text_sha256':hashlib.sha256(Path(markdown.__code__.co_filename).read_bytes()).hexdigest(),'extractor_sha256':hashlib.sha256(EXTRACT.encode()).hexdigest(),'records':rows})
print(json.dumps({'table_records':len(rows),'all_values_match':True}))
