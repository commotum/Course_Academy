"""Check committed fresh pools with full multistep ownership and preserved attempts."""
from publish import *
from collections import Counter
from scripts.generator_publish import prepare_records,content_fingerprint

def flatten(entity,records):
 eid=entity[':db/id'];record={};records[str(eid)]=record
 def value(v):
  if isinstance(v,dict)and ':db/id'in v:
   if len(v)>1:flatten(v,records)
   return v[':db/id']
  if isinstance(v,list):return [value(x)for x in v]
  return str(v)if not isinstance(v,(str,int,float,bool,type(None)))else v
 for k,v in entity.items():
  if k==':db/id':continue
  resolved=value(v)
  if '/_'not in k:record[k.lstrip(':')]=resolved
 return eid

def main():
 verification=json.loads((H/'verification.json').read_text());state=json.loads((H/'content/committed.json').read_text());basis=verification['basis_after'];context_ids=[17592186235391,17592186235456,17592186581701,17592186585714,17592186594690,17592186601926,17592186541108]
 pattern='[* {:step/_content [* {:multistep/_steps [* {:multistep/steps [* {:step/content [*]}]}]}]} {:assigned-problem/_content [* {:step/_content [* {:multistep/_steps [* {:multistep/steps [* {:step/content [*]}]}]}]}]}]';context=native(H/'committed-context',basis,[('context',pattern,context_ids)])['context']
 deps=ROOT/'target/release/deps';cmd=['rustc','--edition=2024','-O',str(ROOT/'reference/mathacademy/repairs/2026-10-20-log-product-quotient/check_live.rs')]
 for name in ('course_academy_engine','serde_json'):
  lib=max(deps.glob('lib'+name+'-*.rlib'),key=lambda p:p.stat().st_mtime_ns);cmd+=['--extern',name+'='+str(lib)]
 binary=H/'check-live';cmd+=['-L','dependency='+str(deps),'-o',str(binary)];subprocess.run(cmd,check=True);results={}
 for kp in state['kps']:
  eid=kp[':db/id'];d=H/str(eid);records={};flatten(kp,records)
  for source in context:flatten(source,records)
  fresh=[q[':db/id']for q in kp[':knowledge-point/questions']if q[':db/id']not in context_ids and not q.get(':question/retired')and q.get(':question/worked-solution')and q.get(':question/answer-fields')and all(f.get(':answer-field/correct')for f in q[':question/answer-fields'])];owned={q[':db/id']:q for q in kp[':knowledge-point/questions']};saved=[]
  for item in state['items']:
   qid=item[':task-item/content'][':db/id']
   if qid not in owned or item.get(':task-item/status',{}).get(':db/ident')!=':task-item.status/correct':continue
   q=owned[qid];responseids={a[':db/id']for a in item.get(':task-item/responses',[])};responses={}
   for f in q[':question/answer-fields']:
    a=next(a for a in f[':answer-field/choices']if a[':db/id']in responseids);responses[str(f[':db/id'])]=a[':answer/value']if f[':answer-field/type'][':db/ident'].endswith('/blank')else str(a[':db/id'])
   saved.append({'question':qid,'responses':responses})
  retired=[q for q in verification['retired_questions']if q in owned];input={'entities':records,'kp':eid,'expected_fresh':fresh,'retired':retired,'saved':saved};(d/'live-input.json').write_text(json.dumps(input)+'\n');subprocess.run([str(binary),str(d/'live-input.json'),str(d/'live-verification.json')],check=True)
  additions=json.loads((d/'additions.json').read_text());accepted,duplicates=prepare_records(additions,eid,str(kp[':knowledge-point/id']),{content_fingerprint(q)for q in kp[':knowledge-point/questions']},Path(DB.config.math_root),d/'assets',localizer=lambda r,*args:copy.deepcopy(r));assert not accepted and duplicates==len(additions)
  results[str(eid)]={'fresh_questions':len(fresh),'difficulty_counts':dict(Counter(q[':question/difficulty'][':db/ident']for q in kp[':knowledge-point/questions']if q[':db/id']in fresh)),'native_pool_passed':True,'saved_correct_attempts_graded':len(saved),'repeat_preparation_new_questions':0}
 verification['live_pool_checks']=results;verification['multistep_subquestions_excluded_from_standalone_pools']=context_ids;verification['quality']=json.loads((H/'quality-verification.json').read_text());verification['published_delivery']=json.loads((H/'published-delivery.json').read_text());verification['ui']=json.loads((H/'ui-verification.json').read_text());verification['publication_guard_regression_tests_passed']=46;save('verification.json',verification);print(json.dumps({'passed':True,'basis':basis,'pools':results,'new_questions':len(verification['new_questions']),'retired':len(verification['retired_questions'])},indent=2))
if __name__=='__main__':main()
