"""Read-only original-source assessment of the finite frozen inventory."""
from pathlib import Path
import hashlib,json
from playwright.sync_api import sync_playwright
from scripts.activity.capture import capture_gaps
from scripts.activity.policy import answer_fields
from scripts.recovery import reextract_record
from scripts.storage import atomic_json,read_json
from scripts.config import Config
from historical_solution_supplement import validate_cached_graphics
ROOT=Path(__file__).resolve().parent;initial=read_json(ROOT/'finite-source-inspection-initial.json');out=[]
with sync_playwright() as pw:
 browser=pw.chromium.launch(headless=True);context=browser.new_context();context.route('**/*',lambda route:route.abort());page=context.new_page()
 for row in initial['items']:
  if not row['source_gaps']:continue
  d=Path(row['directory']);config=Config(account=row['account']);protected={name:hashlib.sha256((d/name).read_bytes()).hexdigest() for name in ['checkpoint.json','content.json','capture-complete.json']}
  if (read_json(config.state_root/'active.json',{}) or {}).get('directory')==str(d):out.append({'account':row['account'],'task_id':row['task_id'],'classification':'excluded_current_active_capture'});continue
  content=read_json(d/'content.json');repair=ROOT/'finite-source-inspection'/row['account']/row['task_id'];repair.mkdir(parents=True,exist_ok=True)
  keys={(x['record_kind'],x['question']) for x in row['source_gaps']}
  for bucket in ['questions','canonical_examples']:
   for q in content.get(bucket,[]):
    identity=q.get('source_id') or q.get('math_academy_id')
    if (bucket,identity) not in keys:continue
    record={'account':row['account'],'task_id':row['task_id'],'capture_key':identity,'source_id':q.get('math_academy_id'),'record_kind':bucket,'original_field_count':len(answer_fields(q)),'original_errors':q.get('errors',[]),'original_source_error':(q.get('answer_validation') or {}).get('status')}
    try:
     parsed=reextract_record(q,page,repair,history=bucket=='questions');parsed=validate_cached_graphics(parsed,repair)
     fresh_gaps=capture_gaps({bucket:[parsed]});record.update(fresh_id=parsed.get('math_academy_id'),fresh_complete=parsed.get('answer_fields_complete'),fresh_field_count=len(answer_fields(parsed)),fresh_errors=parsed.get('errors',[]),fresh_gaps=fresh_gaps)
     atomic_json(repair/('parsed-'+identity.replace(':','-')+'.json'),parsed)
     if not fresh_gaps:record['classification']='saved_source_complete_after_current_extraction_or_verified_asset_decode'
     elif all(g.get('missing')==['source_question_id'] for g in fresh_gaps):record['classification']='source_identity_pair_requires_strict_reconciliation'
     else:record['classification']='remaining_source_gap_requires_original_source_inspection'
    except Exception as e:record.update(classification='saved_source_reextraction_failed',error=str(e))
    out.append(record)
  assert protected=={name:hashlib.sha256((d/name).read_bytes()).hexdigest() for name in protected}
 browser.close()
atomic_json(ROOT/'finite-source-inspection-reextraction.json',{'frozen_observed_at':initial['frozen_observed_at'],'records':out,'shared_completed_packages_unchanged':True,'network':'all isolated browser requests aborted'})
print(json.dumps({'records':len(out),'classifications':{key:sum(r['classification']==key for r in out) for key in sorted({r['classification'] for r in out})},'remaining':[r for r in out if r['classification']!='saved_source_complete_after_current_extraction_or_verified_asset_decode']}))
