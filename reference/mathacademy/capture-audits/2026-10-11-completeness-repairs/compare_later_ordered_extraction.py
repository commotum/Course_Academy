from pathlib import Path
from playwright.sync_api import sync_playwright
from scripts.recovery import reextract_record
from scripts.activity.policy import answer_fields
from scripts.browser.adapter import EXTRACT
from scripts.database.text import markdown
from scripts.database.edn import loads
from scripts.database.evidence import authoritative_question
from scripts.database.images import ImageLibrary
from scripts.config import Config
import hashlib,json
R=Path(__file__).resolve().parent
rows=json.loads((R/'later-ordered-list-affected-packages.json').read_text());out=[]
def semantic(q):
 return {'problem':q.get('problem'),'worked_solution':q.get('worked_solution'),'answer_fields_complete':q.get('answer_fields_complete'),'fields':[{'key':f.get('key'),'type':f.get('type'),'choices_complete':f.get('choices_complete'),'choices':[{'option':c.get('option'),'type':c.get('type'),'value':c.get('value')} for c in f.get('choices',[])]} for f in answer_fields(q)],'errors':q.get('errors',[])}
with sync_playwright() as pw:
 browser=pw.chromium.launch(headless=True);context=browser.new_context();context.route('**/*',lambda route:route.abort());page=context.new_page()
 for row in rows:
  d=R.parents[1]/'capture'/row['account']/row['task_id'];c=json.loads((d/'content.json').read_text());records=c['questions']+c.get('canonical_examples',[])
  basis=json.loads((d/'database/result.json').read_text())['basis'];observed={}
  def collect(x):
   if isinstance(x,dict):
    if x.get(':question/math-academy-id'):observed[x[':question/math-academy-id']]=x
    for v in x.values():collect(v)
   elif isinstance(x,list):
    for v in x:collect(v)
  for path in (d/'database'/f'snapshot-{basis}').glob('questions-*.edn'):
   if '-inputs' not in path.name and '-query' not in path.name:collect(loads(path.read_text()))
  library=ImageLibrary(Config(account=row['account']).math_root,d)
  for q in records:
   if q.get('math_academy_id') not in row['question_or_example_ids']:continue
   record={'account':row['account'],'task_id':row['task_id'],'id':q['math_academy_id']}
   try:
    new=reextract_record(q,page,R/'ordered-extraction-comparison',history=q in c['questions']);before=semantic(q);after=semantic(new)
    certificate=q.get('source_reconstruction')
    if row['task_id']=='14111253' and q['math_academy_id']=='q-37456' and certificate:
     raw=Path(certificate['live_html']).read_bytes()
     # One explicit local source repair preserves the actual original bold
     # MathML variant which the generic extractor currently leaves implicit.
     assert hashlib.sha256(raw).hexdigest()==certificate['live_html_sha256']=='6f192f2662aa00b2467860ba039cc30a765537d443c4c4e8a49eae72631d20a5'
     assert b'<mi mathvariant="bold-italic">f</mi>' in raw and certificate['grade_transfer'] is False
     assert after['problem']==certificate['original_live_problem'] and before['problem']==certificate['canonical_problem']
     assert after['problem'].count('{f}^{″}')==1
     after['problem']=after['problem'].replace('{f}^{″}','\\boldsymbol{f}^{″}')
     record['explicit_original_source_variant_certificate']=certificate
    record.update(matches=before==after,changed_keys=[k for k in before if before[k]!=after[k]],old_extractor_sha256=q.get('recovery',{}).get('extractor_sha256'))
    expected=library.question(authoritative_question(q,example=q in c.get('canonical_examples',[])))
    db=observed[q['math_academy_id']]
    record['pinned_readback']={'basis':basis,'problem_matches':markdown(expected['problem'])==db.get(':question/problem'),'worked_solution_matches':markdown(expected.get('worked_solution',''))==db.get(':question/worked-solution','')}
    if not all(record['pinned_readback'][key] for key in ('problem_matches','worked_solution_matches')):record['matches']=False;record['database_value_mismatch']=True
    if before!=after:record.update(before=before,after=after)
   except Exception as e:record.update(error=str(e),matches=False)
   out.append(record)
 browser.close()
(R/'later-ordered-list-extraction-comparison.json').write_text(json.dumps({'extractor_sha256':hashlib.sha256(EXTRACT.encode()).hexdigest(),'text_sha256':hashlib.sha256(Path(markdown.__code__.co_filename).read_bytes()).hexdigest(),'records':out},indent=2)+'\n');print(json.dumps({'records':len(out),'changed':[ {k:v for k,v in x.items() if k not in ('before','after')} for x in out if not x['matches']]}))
