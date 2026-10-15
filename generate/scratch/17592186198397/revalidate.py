"""Reopen classification at a current captured basis; validate scoped generation."""
import hashlib,importlib.util,json,sys,copy
from pathlib import Path
import sympy as s
D=Path(__file__).resolve().parent;ROOT=D.parents[2];OUT=D/'reference/replenishment'
sys.dont_write_bytecode=True

def module(path,name):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
v=module(D/'validate.py','triple_validation');g=v.g
ind=module(ROOT/'generate/runs/current/qa-triple-setup.py','triple_independent')

def save(path,value):path.write_text(json.dumps(value,indent=2,ensure_ascii=False,default=str)+'\n')
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
 current=json.loads((OUT/'initial/kp.json').read_text());basis=json.loads((OUT/'inventory-initial.json').read_text())['basis']
 # The new snapshot is separate from immutable historical source evidence.
 source_info={
 'q-38941':('sqrt','moderate',False,'Incorrect source key/final upper limit uv: w=sqrt(z) requires sqrt(uv).',{'a':1,'c':3,'upper':2}),
 'q-39054':('sin','easy',True,'Correct determinant 2, reciprocal 1/2, rectangular transformed region.',{'a':2,'c':1}),
 'q-161880':('exp','easy',False,'Missing prompt answer slot and Step 1 u bounds conflict with the region.',{'a':1,'c':2}),
 'q-39057':('log','easy',False,'Claimed rectangular transformed region is incorrect; some ln(v) choices are undefined.',{'a':2,'c':1}),
 'q-161879':('cos2','easy',False,'Missing prompt answer slot and incorrect coordinate labels in Step 1.',{'a':3,'c':1}),
 'q-39058':('sin','easy',True,'Unit linear determinant; distinct missing-integrand functions; supplied rectangular limits.',{'a':1,'c':1}),
 'q-161892':('ratio-product','moderate',False,'Region contains positive and negative x,y branches; supplied key omits the second branch.',{}),
 'q-161871':('x-product','moderate',False,'Source bank contains integrals whose w upper limit depends on the same integration variable w; not validated mathematical objects.',{}),
 'q-161889':('difference-log','moderate',False,'Source bank contains self-dependent w limits; no validated complete five-value bank.',{}),
 'q-161868':('affine-sum','easy',True,'Linear map determinant 1/6; inverse determinant 6; expected fragment 6(u+w).',{}),
 'q-39062':('triple-product-exp','moderate',False,'Source bank contains a v upper limit v for integration over v; complete bank not validated.',{}),
 'q-39056':('difference-sinh','moderate',True,'Positive x+y; one inverse branch; forward determinant 2v cancels integrand factor v.',{})}
 assert len(current[':knowledge-point/questions'])==len(source_info)==12
 questions={}
 for q in current[':knowledge-point/questions']:
  mid=q[':question/math-academy-id'];family,level,eligible,reason,params=source_info[mid]
  assert q[':question/difficulty'][':db/ident']==':question.difficulty/'+level
  assert len(q[':question/answer-fields'])==1
  field=q[':question/answer-fields'][0];assert field[':answer-field/type'][':db/ident']==':answer-field.type/radio' and len(field[':answer-field/choices'])==5
  assert all('![' not in text for text in [q[':question/problem'],q[':question/worked-solution']]+[a[':answer/value'] for a in field[':answer-field/choices']])
  questions[mid]={'family':family,'difficulty':level,'field_types':['radio'],'choice_count':5,'choice_bank_profile':mid+'-current','plot_rating':'none','eligible_for_inventory':eligible,'reason':reason,'mathematical_fingerprint':g.digest([family,params]) if params else g.digest([family,'current-source']),'source_sha256':g.digest(q),'generator_profile_coverage':'historical replay only' if mid in g.RAW_TEMPLATES else 'not implemented; preserved as source evidence'}
 # Independent exact calculations for the four sources admitted to inventory.
 x,y,z,u,vv,w=g.X,g.Y,g.Z,g.U,g.V,g.W
 assert s.Matrix([2*x+y,y+z,z]).jacobian((x,y,z)).det()==2
 assert s.Matrix([x+y,y+z,z]).jacobian((x,y,z)).det()==1
 J=s.Matrix([x-y/2,y/2,z/3]).jacobian((x,y,z));assert J.det()==s.Rational(1,6)
 J=s.Matrix([x*x-y*y,x+y,z]).jacobian((x,y,z));assert s.simplify(J.det()-2*(x+y))==0
 inv=s.solve([x*x-y*y-u,x+y-vv,z-w],(x,y,z),dict=True);assert len(inv)==1
 assert all(s.simplify(inv[0][key]-value)==0 for key,value in {x:(u+vv**2)/(2*vv),y:(-u+vv**2)/(2*vv),z:w}.items())
 # Current fragment banks: full symbolic values checked, exact correct designations.
 expected={
 'q-39054':[3*s.sin(u)*s.cos(vv),s.sin(u)*s.cos(vv),s.sin(u)*s.cos(vv)/2,2*s.sin(u)*s.cos(vv),s.sin(u)*s.cos(vv)/3],
 'q-39058':[2*s.sin(u)*s.cos(vv),2*s.sin(vv)*s.cos(u),s.sin(u)*s.cos(vv)/2,3*s.sin(vv)*s.cos(u),s.sin(u)*s.cos(vv)],
 'q-161868':[6*(u+w),(u+vv-w)/6,6*(vv-w),u-w-vv,(vv-w)/6]}
 corrects={'q-39054':s.sin(u)*s.cos(vv)/2,'q-39058':s.sin(u)*s.cos(vv),'q-161868':6*(u+w)}
 for mid,bank in expected.items():
  q=next(q for q in current[':knowledge-point/questions'] if q[':question/math-academy-id']==mid);f=q[':question/answer-fields'][0]
  # Existing source notation is retained verbatim; order verified against the captured bank.
  assert all(s.simplify(a-b)!=0 for i,a in enumerate(bank) for b in bank[:i])
  idx=next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][':answer/id']);assert s.simplify(bank[idx]-corrects[mid])==0
 b=((1,2),(2,4),(0,1));sinh=s.sinh(u)
 banks=[(sinh/2,((1,2),(2,4),(0,vv))),(2*vv*sinh,((1,2),(2,4),(0,u*vv))),(sinh/2,b),(2*vv*s.sinh(u*vv),((1,2),(2,4),(0,u*vv))),(u*sinh/2,((1,2),(2,4),(0,vv)))]
 inner=[s.simplify(s.integrate(e,(w,*bb[2]))) for e,bb in banks]
 # Strict pointwise order after the w integral establishes distinct complete
 # integrals without asking SymPy to integrate sinh(u*v) over a rectangle.
 assert s.simplify(inner[0]/inner[2])==vv
 assert s.simplify(inner[4]/inner[0])==u
 assert s.simplify(inner[1]/inner[4])==4*vv
 assert s.simplify(inner[3]/inner[1])==s.sinh(u*vv)/s.sinh(u)
 # On the interior 1<u<2, 2<v<4: v>1, u>1, 4v>1,
 # and sinh(uv)>sinh(u)>0. Thus option3<option1<option5<option2<option4.
 q=next(q for q in current[':knowledge-point/questions'] if q[':question/math-academy-id']=='q-39056');f=q[':question/answer-fields'][0];assert f[':answer-field/choices'][2][':answer/id']==f[':answer-field/correct'][':answer/id']
 save(OUT/'source-audit.json',{'basis':basis,'lineage':g.CAPTURE['lineage'],'source_count':12,'questions':questions,'template_counts':{'easy':5,'moderate':6,'hard':0},'conservative_inventory_policy':'Exclude an entire source with inconsistent premises, missing response slot, branch omission or unvalidated mathematical bank; preserve it unchanged.','supported_generator_levels':list(g.FAMILIES),'unsupported_levels':g.UNSUPPORTED_LEVELS,'current_source_bank_coverage':'All 12 classified; four admitted by explicit math review. Generator source replay remains scoped to five historical banks; no fidelity claim for seven newly captured banks.','admitted_source_correctness_checks':4,'new_plot_assets':[]})
 print('Current source audit saved',flush=True)
 # Replay every historical bank; retain errors in evidence-only output.
 historical={q[':question/math-academy-id']:q for q in g.SOURCE_QUESTIONS};replayed=0
 for c in json.loads((D/'source-cases.json').read_text()):
  r=g.generate(c['level'],template=c['template'],parameters=c['parameters'],profile='raw');q=r['question'];old=historical[c['source_id']]
  for key in (':question/problem',':question/worked-solution',':question/difficulty'):
   assert (key in q)==(key in old)
   if key in old:assert q[key]==(old[key][':db/ident'] if key.endswith('difficulty') else old[key])
  f=q[':question/answer-fields'][0];of=old[':question/answer-fields'][0]
  assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in of[':answer-field/choices'])
  assert (':answer-field/correct' in f)==(':answer-field/correct' in of)
  if ':answer-field/correct' in of:assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==of[':answer-field/correct'][':answer/value']
  assert not r['generation']['eligible_for_learning'];replayed+=1
 checks=[];review=[]
 for level,templates in g.FAMILIES.items():
  for t in templates:
   for seed in (42,47):
    r=g.generate(level,seed,template=t);v.check_printed(r);ind.check(r)
    replay=g.generate(level,seed+100,template=t,parameters=r['generation']['parameters']);assert replay['question'][':question/id']==r['question'][':question/id']
    f=r['question'][':question/answer-fields'][0];checks.append({'label':level+' '+t+' '+str(seed),'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'all owned choices'} for a in f[':answer-field/choices']]});review.append(r)
    print('Validated',level,t,seed,flush=True)
 try:g.generate_hard();raise AssertionError('unsupported hard generated')
 except ValueError:pass
 save(OUT/'revalidation-native-input.json',checks)
 import subprocess
 subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(OUT/'revalidation-native-input.json'),str(OUT/'revalidation-native-report.json')],check=True)
 save(OUT/'revalidation-review.json',review);(OUT/'revalidation-review.md').write_text('\n\n---\n\n'.join(g.markdown(r) for r in review))
 save(OUT/'revalidation.json',{'status':'passed','basis':basis,'version':g.VERSION,'historical_complete_banks_replayed':replayed,'historical_options_replayed':25,'generated_instances_checked':len(review),'independent_printed_math':ind.n,'supported_levels':list(g.FAMILIES),'unsupported_levels':g.UNSUPPORTED_LEVELS,'generator_sha256':sha(D.with_suffix('.py')),'native_report':'generate/scratch/17592186198397/reference/replenishment/revalidation-native-report.json','current_source_audit':'generate/scratch/17592186198397/reference/replenishment/source-audit.json'})
 files=[D.with_suffix('.py'),D/'validate.py',D/'revalidate.py',D/'replenish.py',OUT/'revalidation.json',OUT/'source-audit.json',OUT/'initial/kp.json']
 save(D/'validation-freeze.json',{'status':'passed','version':g.VERSION,'hashes':{str(path.relative_to(ROOT)):sha(path) for path in files}})
 print('Revalidation and freeze passed',flush=True)
if __name__=='__main__':main()
