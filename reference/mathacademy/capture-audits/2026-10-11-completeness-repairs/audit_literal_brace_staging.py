"""Audit each staged brace refresh without mutating completed packages or outboxes."""
from pathlib import Path
import json,hashlib
from scripts.browser.adapter import EXTRACT
from scripts.storage import read_json,atomic_json
from scripts.activity.policy import answer_fields
R=Path(__file__).resolve().parent;out=[]
latest={}
for path in R.glob('later-source-review-literal-braces*.json'):
 for row in read_json(path,[]):
  key=(row['account'],row['task_id'])
  if row.get('completed_at',0)>latest.get(key,{}).get('completed_at',0):latest[key]=row
for row in latest.values():
 d=Path(row['directory']);p=Path(row['repair']);c=read_json(p/'content.json',{});original=read_json(p/'originals/content.json',{});validation=read_json(p/'validation.json',{})
 protected=row.get('source_only_completion_assertions',{}).get('protected_sha256',{})
 expected={name:hashlib.sha256((d/name).read_bytes()).hexdigest() for name in protected}
 r={'account':row['account'],'task_id':row['task_id'],'repair':str(p),'status':row['status'],'shared_originals_unchanged':expected==protected,'source_gaps':validation.get('gaps'),'unsupported_records':[{'id':q.get('math_academy_id'),'validation':q.get('answer_validation')} for bucket in ['questions','canonical_examples'] for q in c.get(bucket,[]) if q.get('answer_validation',{}).get('status')!='supported']}
 records=[]
 for bucket in ['questions','canonical_examples']:
  old={q.get('math_academy_id'):q for q in original.get(bucket,[])}
  for q in c.get(bucket,[]):
   record={'id':q.get('math_academy_id'),'bucket':bucket,'extractor_generation':q.get('recovery',{}).get('extractor_sha256'),'answer_supported':q.get('answer_validation',{}).get('status')=='supported'}
   source=q.get('html_path');sha=q.get('recovery',{}).get('source_sha256')
   record['source_hash_matches']=bool(source and Path(source).is_file() and hashlib.sha256(Path(source).read_bytes()).hexdigest()==sha)
   prev=old.get(q.get('math_academy_id'))
   if prev:
    def semantic(x):return {'problem':x.get('problem'),'worked_solution':x.get('worked_solution'),'complete':x.get('answer_fields_complete'),'fields':[{'key':f.get('key'),'type':f.get('type'),'complete':f.get('choices_complete'),'choices':[{'option':v.get('option'),'type':v.get('type'),'value':v.get('value')} for v in f.get('choices',[])]} for f in answer_fields(x)],'errors':x.get('errors',[])}
    a,b=semantic(prev),semantic(q);record['changed_keys']=[k for k in a if a[k]!=b[k]]
   records.append(record)
 r['records']=records;r['all_source_hashes_match']=all(x['source_hash_matches'] for x in records)
 r['all_current_extractor']=all(x['extractor_generation']==hashlib.sha256(EXTRACT.encode()).hexdigest() for x in records)
 out.append(r)
atomic_json(R/'literal-brace-staging-verification.json',{'extractor_sha256':hashlib.sha256(EXTRACT.encode()).hexdigest(),'captures':out})
print(json.dumps({'prepared':len(out),'failed':[ {k:v for k,v in r.items() if k!='records'} for r in out if not(r['shared_originals_unchanged'] and r['all_source_hashes_match'] and r['all_current_extractor'] and not r['source_gaps'] and not r['unsupported_records'])]}))
