"""Confirm learner-facing pool membership and idempotent publication at db_after."""
from collections import Counter
from commit import *
from scripts.generator_publish import prepare_records,content_fingerprint
def flatten(entity,records):
 eid=entity[':db/id'];record={};records[str(eid)]=record
 for k,v in entity.items():
  if k==':db/id':continue
  def value(v):
   if isinstance(v,dict)and ':db/id'in v:
    if len(v)>1:flatten(v,records)
    return v[':db/id']
   if isinstance(v,list):return [value(x)for x in v]
   return str(v)if not isinstance(v,(str,int,float,bool,type(None)))else v
  record[k.lstrip(':')]=value(v)
 return eid
if __name__=='__main__':
 v=json.loads((HERE/'verification.json').read_text());assert v['committed']and v['passed'];state=json.loads((HERE/'content/committed.json').read_text());kp=state['kp'][0];records={};flatten(kp,records)
 fresh=[q[':db/id']for q in kp[':knowledge-point/questions']if not q.get(':question/retired')and q.get(':question/worked-solution')and q.get(':question/answer-fields')and all(f.get(':answer-field/correct')for f in q[':question/answer-fields'])];assert len(fresh)==20
 saved=[]
 for item in state['items']:
  q=next(q for q in kp[':knowledge-point/questions']if q[':db/id']==item[':task-item/content'][':db/id']);responseids={a[':db/id']for a in item.get(':task-item/responses',[])};correctids={f[':answer-field/correct'][':db/id']for f in q[':question/answer-fields']}
  if responseids==correctids:
   response={str(f[':db/id']):str(a[':db/id'])for f in q[':question/answer-fields']for a in f[':answer-field/choices']if a[':db/id']in responseids};saved.append({'question':q[':db/id'],'responses':response})
 save('live-input.json',{'entities':records,'kp':KP,'expected_fresh':fresh,'retired':[],'saved':saved});binary=ROOT/'reference/mathacademy/repairs/2026-10-20-log-product-quotient/check-live';subprocess.run([str(binary),str(HERE/'live-input.json'),str(HERE/'live-verification.json')],check=True)
 additions=json.loads((HERE/'additions.json').read_text());fingerprints={content_fingerprint(q)for q in kp[':knowledge-point/questions']};accepted,duplicates=prepare_records(additions,KP,str(kp[':knowledge-point/id']),fingerprints,Path(DB.config.math_root),HERE/'delivery-assets',localizer=lambda r,*args:copy.deepcopy(r));assert not accepted and duplicates==12
 published=json.loads((HERE/'published-delivery.json').read_text());assert published['passed']and published['reference']==v['new_generator_reference'];v['published_delivery']=published;v['live_pool_verification']=json.loads((HERE/'live-verification.json').read_text());v['fresh_difficulty_counts']=dict(Counter(q[':question/difficulty'][':db/ident']for q in kp[':knowledge-point/questions']if q[':db/id']in fresh));assert v['fresh_difficulty_counts'][':question.difficulty/hard']==14
 v['repeat_preparation']={'new_questions':0,'duplicates_skipped':duplicates};v['diagnosis']='Both reported questions are Math Academy sources. The registered generator covered moderate integer-RHS questions only; hard practice had two complete, closely structured root-RHS sources. Added a source-grounded hard root family varying the affine exponent, plus 12 new hard questions. Original source and authored questions, canonical example and saved learner items are unchanged.';save('verification.json',v)
 print(json.dumps({'passed':True,'committed_basis':v['basis_after'],'fresh_pool':len(fresh),'hard_pool':v['fresh_difficulty_counts'][':question.difficulty/hard'],'saved_correct_attempts_still_grade':len(saved),'repeat_preparation_new_questions':0}))
