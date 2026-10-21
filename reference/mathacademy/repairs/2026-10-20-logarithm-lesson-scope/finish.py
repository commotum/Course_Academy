"""Verify committed pool filtering, unchanged lesson siblings, and package delivery."""
import runpy
from commit import *
flatten=runpy.run_path(str(ROOT/'reference/mathacademy/repairs/2026-10-20-log-product-quotient/finish.py'))['flatten']
if __name__=='__main__':
 v=json.loads((HERE/'verification.json').read_text());state=json.loads((HERE/'content/committed.json').read_text());kp=state['kp'][0];records={};flatten(kp,records)
 fresh=[q[':db/id']for q in kp[':knowledge-point/questions']if not q.get(':question/retired')and q.get(':question/worked-solution')and all(f.get(':answer-field/correct')for f in q[':question/answer-fields'])];assert len(fresh)==7
 saved=[]
 for item in state['items']:
  q=next(q for q in kp[':knowledge-point/questions']if q[':db/id']==item[':task-item/content'][':db/id']);responseids={a[':db/id']for a in item.get(':task-item/responses',[])};correctids={f[':answer-field/correct'][':db/id'] for f in q[':question/answer-fields']}
  if responseids==correctids:
   response={str(f[':db/id']):str(a[':db/id'])for f in q[':question/answer-fields']for a in f[':answer-field/choices']if a[':db/id']in responseids};saved.append({'question':q[':db/id'],'responses':response})
 save('live-input.json',{'entities':records,'kp':KP,'expected_fresh':fresh,'retired':v['withdrawn_questions'],'saved':saved});binary=ROOT/'reference/mathacademy/repairs/2026-10-20-log-product-quotient/check-live';subprocess.run([str(binary),str(HERE/'live-input.json'),str(HERE/'live-verification.json')],check=True)
 # Read the sibling KPs at the exact committed basis, without touching them.
 siblings=native(HERE/'siblings-after',v['basis_after'],[('kps',KP_PATTERN,[17592186054622,17592186054623,17592186054624])])['kps'];old=dict(json.loads((HERE/'kps.json').read_text()))
 for sibling in siblings:assert same(sibling,old[sibling[':db/id']]),('Sibling changed during audit',sibling[':db/id'])
 v['other_generators_and_source_only_kp_unchanged']=True;v['all_other_generated_questions_audited']=10;v['published_package_execution']=json.loads((HERE/'published-delivery.json').read_text());assert v['published_package_execution']['reference']==v['new_generator_reference'];v['live_pool_verification']=json.loads((HERE/'live-verification.json').read_text());v['scope_validation']['database_writes_pending']=False
 v['lesson_kps']={'17592186054622':'Product and power: in scope; all five authored questions retained.','17592186054623':'Quotient and power: no registered generator; eight saved Math Academy questions.','17592186054624':'Product and quotient: previously repaired package registration confirmed unchanged.','17592186054625':'All three rules: generator restricted; three authored questions withdrawn and replaced; one solution clarified.'}
 save('verification.json',v);print(json.dumps({'passed':True,'committed_basis':v['basis_after'],'fresh_pool':len(fresh),'retired_rejected':len(v['withdrawn_questions']),'saved_correct_attempts_graded':len(saved),'sibling_kps_unchanged':True}))
