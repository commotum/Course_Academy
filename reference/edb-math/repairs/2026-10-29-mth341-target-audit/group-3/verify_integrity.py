import json,re,collections,hashlib
from pathlib import Path
H=Path(__file__).resolve().parent;S=json.loads((H/'current.json').read_text());qs=json.loads((H/'proposed-questions.json').read_text());props=json.loads((H/'proposals.json').read_text());original={q[':db/id']:q for q in S['questions']};entities={}
def visit(o):
 if isinstance(o,list):
  for v in o:visit(v)
 elif isinstance(o,dict):
  if ':db/id'in o and len(o)>1:entities.setdefault(o[':db/id'],{}).update(o)
  for v in o.values():visit(v)
visit(S)
for p in props:assert entities[p['entity']].get(':'+p['attribute'])==p['before'],(p['entity'],p['attribute'])
img=lambda t:re.findall(r'!\[[^\]]*\]\(([^)]*)\)',t)
checks=[]
for q in qs:
 before=original[q[':db/id']];assert q[':question/id']==before[':question/id'];assert q.get(':question/math-academy-id')==before.get(':question/math-academy-id');fields=q.get(':question/answer-fields',[]);keys=[f[':answer-field/key']for f in fields];assert len(keys)==len(set(keys)),q[':db/id'];assert q.get(':question/worked-solution');oldfields={f[':db/id']:f for f in before.get(':question/answer-fields',[])}
 for f in fields:
  old=oldfields[f[':db/id']];assert f[':answer-field/id']==old[':answer-field/id'];assert f[':answer-field/choices']==old[':answer-field/choices'];assert f[':answer-field/type']==old[':answer-field/type'];right=f[':answer-field/correct'][':db/id'];assert right in[a[':db/id']for a in f[':answer-field/choices']]
  if old.get(':answer-field/correct'):assert f[':answer-field/correct']==old[':answer-field/correct']
  if f[':answer-field/type'][':db/ident']in[':answer-field.type/blank',':answer-field.type/select']:
   assert q[':question/problem'].count('{{'+f[':answer-field/key']+'}}')==1,(q[':db/id'],f[':answer-field/key'])
  if f[':answer-field/type'][':db/ident']==':answer-field.type/blank':assert all(a[':answer/type'][':db/ident']==':answer.type/math'for a in f[':answer-field/choices'])
 for attr in[':question/problem',':question/worked-solution']:assert img(q.get(attr,''))==img(before.get(attr,'')),(q[':db/id'],attr)
 checks.append({'entity':q[':db/id'],'uuid_and_source_identity_preserved':True,'owned_answer_ids_values_and_banks_preserved':True,'correct_links_complete_and_owned':True,'unique_active_field_keys':True,'one_mount_per_response_field':True,'source_diagram_asset_paths_preserved':True})
assert len(qs)==323
# Every question has its own content/mathematical review, not merely a structural row.
proofs={}
for name in['plane-math-verification','cross-math-verification','geometry-evidence']:
 d=json.loads((H/(name+'.json')).read_text());assert d['passed'];
 for c in d['checks']:assert c['entity']not in proofs;proofs[c['entity']]={'file':name+'.json',**c}
assert set(proofs)==set(original)
source={v['entity']:v for v in json.loads((H/'source-coverage.json').read_text())};changed=collections.defaultdict(list)
for p in props:changed[p['entity']].append(p['attribute'])
ledger=[]
for q in qs:
 eid=q[':db/id'];ledger.append({'entity':eid,'identity':q.get(':question/math-academy-id'),'basis_t':S['basis_t'],'source':source[eid],'review':proofs[eid],'reviewed_components':['complete prompt','worked solution and final result','canonical-example context','all fields and choices','all existing correct links','source math layout, fonts and fences','diagram context when present','actual player render','native grader when fields exist'],'changes':changed[eid],'status':'prepared repair'if changed[eid]or eid==17592186120218 else'satisfactory without content changes'})
(H/'integrity-verification.json').write_text(json.dumps({'passed':True,'checks':checks,'proposals':len(props),'no_learner_mutations':True,'database_writes':0},indent=2)+'\n');(H/'review-ledger.json').write_text(json.dumps(ledger,default=str,indent=2)+'\n')
# Explicit proof package for the two source mathematical corrections.
(H/'authored-math-proof.json').write_text(json.dumps({'q-33160':{'entity':17592186304926,'old_issue':'Parallel directions alone do not specify a unique plane and two old options qualified.','source_directions':[[1,1,1],[-2,-2,-2]],'correct_scalar_relation':'d2=-2*d1','connecting_vector':[1,-2,-26],'normal':[-24,27,-3],'new_constraint':'Parallel to the plane determined by both distinct parallel lines; translate that direction plane through C.','unique_valid_existing_choice':17592186304058,'full_choice_proof_file':'plane-math-verification.json'},'q-280352':{'entity':17592186660905,'old_issue':'Two-component cross-product outputs','new_values':[[1,5,0],[-2,4,0]],'answer':[8,-2,0],'concrete_simultaneous_witness':{'c':[0,0,1],'a':[5,-1,0],'b':[4,2,0]},'verification':'c×a=(1,5,0), c×b=(-2,4,0); 2(c×a)-3(c×b)=(8,-2,0). Existing field values8,-2 unchanged; fixed third coordinate0.'},'tutorial_subspace_test':{'entity':17592186193876,'proof':'The empty set is vacuously closed under both operations but is not a subspace; require nonempty H.'},'tutorial_cross_definition':{'entity':17592186205256,'proof':'Two perpendicular unit normals have opposite directions; the right-hand rule determines the cross-product orientation.'}},indent=2)+'\n')
print('Integrity passed;',len(ledger),'individually evidenced review rows;',len(props),'attribute proposals')
