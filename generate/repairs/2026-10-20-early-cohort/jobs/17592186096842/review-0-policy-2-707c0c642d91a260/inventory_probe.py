from audit_helpers import *
from shortcut_probe import probe
sys.path.insert(0,'/home/jake/Developer/Course_Academy')
from scripts.generator_publish import stable_identities,normalized_question,content_fingerprint
inv=json.load(open(ROOT.parent/'source/inventory.json'))
params=[('sqrt_linear_radio','moderate',{'a':4,'b':3},3),('reciprocal_radio','moderate',{'a':-2,'b':12},4),('sqrt_constfirst_radio','moderate',{'a':-7,'b':-6},3)]
stored={q[':question/id']:q for q in inv['questions']};records=[];affected=[];results=[]
for name,level,p,role in params:
 r=g.generate(level,seed=70001,template=name,parameters=p,bank_role=role)
 r['question']=stable_identities(r['question'],g.KP_UUID)
 qid=r['question'][':question/id'];q=stored.get(qid)
 result={'reproduction':{'template':name,'level':level,'parameters':p,'bank_role':role,'seed':70001},'reproduced_question_id':qid,'matches_inventory':q is not None}
 if q:
  result.update({'entity_id':q[':db/id'],'retired':q.get(':question/retired',False),'content_fingerprint_equal':content_fingerprint(q)==content_fingerprint(r['question']),'shortcut':probe(r)})
  records.append(r)
  if not result['retired'] and result['shortcut']['success']:
   affected.append({'question_id':qid,'entity_id':q[':db/id'],'finding':'Radio answer ladder leaks the derivative: choose visible linear coefficient times common positive option spacing (negate for reciprocal root); no chain-rule computation required.','reproduction':f'{sys.executable} -B inventory_probe.py; explicit parameters: '+json.dumps(result['reproduction']),'evidence_path':'generated-records.json'})
 results.append(result)
save('generated-records.json',records);save('inventory-results.json',{'basis':inv['basis'],'questions':len(inv['questions']),'original_questions':17,'non_source_questions':5,'eligibility':'All five non-source records have a valid canonical key, worked solution, ordinary radio/blank field and no retirement marker in capture. learning.rs validate_practice_question excludes retired, unusable and multistep questions. Unknown learner history may exclude any previously seen question.','results':results,'limits':'Metadata seed 70001 is an independent replay seed, not asserted to be the historical seed. Stable content IDs and complete normalized content match captured records. Two non-source blanks do not expose a radio spacing cue.'});save('affected-inventory.json',{'affected_questions':affected});print(json.dumps(results,indent=2))
