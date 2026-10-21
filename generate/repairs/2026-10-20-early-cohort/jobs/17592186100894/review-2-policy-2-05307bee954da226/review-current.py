from auditlib import *
from collections import Counter,defaultdict
import shutil,difflib
PREV=JOB/'review-1-policy-2-a0e5ad288aa2c633'
# Verify the author's claimed narrow change against the retained executable.
old=PREV/'relocated/17592186100894.py'
(E/'independent-package-diff.patch').write_text(''.join(difflib.unified_diff(old.read_text().splitlines(True),(W/'17592186100894.py').read_text().splitlines(True),fromfile='previous independent relocated generator',tofile='current package generator')))
manifest=json.load(open(W/'package.json'))
unchanged={n:hashlib.sha256((W/n).read_bytes()).hexdigest()==hashlib.sha256((PREV/'relocated'/n).read_bytes()).hexdigest() for n in manifest['files'] if n!='17592186100894.py'}
save('provenance.json',{'previous_review':str(PREV),'source_confirmation':'source-analysis.json; all 26 prompts/banks independently reconfirmed','reused_scripts':['auditlib.py','package-review.py'],'unchanged_runtime_files':unchanged,'reused_math':'reused-unchanged-math-results.json covers earlier unchanged translation families; current source replay and small regression checks below','generator_diff':'independent-package-diff.patch','engine_current_sha256':hashlib.sha256((ROOT/'generate/runs/current/check-engine').read_bytes()).hexdigest(),'engine_previous_sha256':json.load(open(PREV/'packaging.json'))['engine_sha256']})
# Faithful replay: complete banks and keys; presentation normalization is shared, mathematics separate.
source=json.load(open(JOB/'source/source.json')); original={q[':question/math-academy-id']:q for q in source['material']['kp'][':knowledge-point/questions']}
replays=[]; fidelity=[]
for i,(mid,q) in enumerate(original.items()):
 if mid=='q-104058':continue
 r=g.generate(q[':question/difficulty'][':db/ident'].split('/')[-1],731900+i,mid,replay=True);replays.append(r)
 sf=q[':question/answer-fields'][0]
 fidelity.append({'template':mid,'source_id':q[':question/id'],'bank_equal':Counter(g.normalize_tex(a[':answer/value']) for a in sf[':answer-field/choices'])==Counter(a[':answer/value'] for a in field(r)[':answer-field/choices']),'key_equal':correct(r)==g.normalize_tex(sf[':answer-field/correct'][':answer/value']),'prompt_equal':r['question'][':question/problem']==g.normalize_prose(q[':question/problem']),'solution_equal':r['question'][':question/worked-solution']==g.normalize_prose(q[':question/worked-solution'])})
save('source-replay-records.json',replays)
save('source-replay.json',{'results':fidelity,'excluded':{'q-104058':'At (1,1), (1/(xy)-1/x)yprime=2 is 0=2; impossible classical IVP, not an engine exclusion.'},'corrections':g.REPAIRS,'additional_corrections':{'q-126765':'ODE restored from own worked solution and positive-cosine local branch specified.','q-128199':'Unavailable part 6 cross-reference replaced by direct separation/integration wording.'},'canonical':'Instructional evidence only: no captured field/bank.'})
assert all(v['bank_equal'] and v['key_equal'] for v in fidelity)
print('source replay 25 banks/keys confirmed',flush=True)
# Choose role controls from each VISIBLE exemplar bank, without reading its catalog.
roles=[];groups=[]
for bank in range(15):
 h=(-4,2,4)[bank%3];seed=731971+bank
 ex=g.generate('easy',seed,'q-104065',{'h':h,'bank':bank})
 _,(x0,_) = prompt_data(ex); shift=simplify(x0-S.pi/2)
 group=[]
 for opt in field(ex)[':answer-field/choices']:
  v=explicit(ex,opt[':answer/value']);poly=S.expand(v-S.log(S.sin(x-shift)));a=poly.coeff(x,2);c=S.expand(poly-a*(x-shift)**2)
  rr=g.generate('easy',seed,'q-104065',{'h':h,'bank':bank,'a':int(a),'c':str(c)})
  group.append(rr)
 roles+=group;groups.append(group)
save('role-records.json',roles)
print('generated 75 roles across 15 visible banks',flush=True)
# Exact ODE/IC checks from printed prompt and options, optimized only by cancelling
# their shared printed logarithm. No generator MODELS or expected_fragment used.
def trig_math(r):
 ode,(x0,y0)=prompt_data(r);h=simplify(x0-S.pi/2);log=S.log(S.sin(x-h));opts=[]
 for option in field(r)[':answer-field/choices']:
  v=explicit(r,option[':answer/value']);poly=S.expand(v-log)
  assert poly.is_polynomial(x) and S.degree(poly,x)<=2
  residual=S.trigsimp(S.expand(ode.subs({z:S.diff(poly,x)+S.cos(x-h)/S.sin(x-h),y:v},simultaneous=True)))
  ic=simplify(poly.subs(x,x0)-y0)
  opts.append({'value':option[':answer/value'],'ODE':str(residual),'IC':str(ic),'valid':residual==0 and ic==0})
 key=next(o for o in opts if o['value']==correct(r));final=re.search(r'Therefore \$y=(.*?)\$\.',r['question'][':question/worked-solution']).group(1)
 final_match=simplify(expr(final)-explicit(r,correct(r)))==0
 return {'id':r['question'][':question/id'],'template':'q-104065','parameters':r['generation']['parameters'],'passed':key['valid'] and final_match,'valid_choice_count':sum(o['valid'] for o in opts),'IC_matching_choices':sum(o['IC']=='0' for o in opts),'solution_matches':final_match,'choices':opts}
math=[trig_math(r) for r in roles]
assert all(v['passed'] and v['valid_choice_count']==1 and v['IC_matching_choices']>=2 for v in math)
# Prior counterexample seeds, plus restored branch and engine families at fresh boundaries.
prior=[(492797,-4,2,'pi^2'),(492800,1,4,'0'),(492802,1,4,'pi^2'),(492803,4,6,'-pi^2'),(492805,4,6,'0')]
controls=[g.generate('easy',seed,'q-104065',{'h':h,'a':a,'c':c}) for seed,h,a,c in prior]
controls.append(g.generate('easy',847003,'q-104065',{'h':1}))
reg=[g.generate(g.level(mid),732100+i,mid,params) for i,(mid,params) in enumerate([('q-128199',{'h':-4,'b':-2}),('q-128199',{'h':4,'b':1}),('q-355559',{'h':-4}),('q-355577',{'h':4}),('q-355582',{'h':-4}),('q-350957',{'h':4}),('q-104064',{'h':-4}),('q-355560',{'h':4})])]
save('regression-records.json',controls+reg)
batch=json.load(open(E/'batch.json'))
for r in controls+reg+batch:
 if r['generation']['template']=='q-104065':result=trig_math(r)
 elif r['generation']['template']=='q-126765':
  v=expr(correct(r));h=r['generation']['parameters']['h'];C=S.Symbol('C',real=True)
  result={'id':r['question'][':question/id'],'template':'q-126765','passed':simplify(S.diff(v,x)-2*(x-h))==0,'valid_choice_count':1,'scaffold':'On the printed positive-cosine branch, derivative of sin(v+C) is 2(x-h)cos(v+C)=2(x-h)sqrt(1-y²).'}
 else:result=math_check(r)
 math.append(result)
save('math-results.json',math);assert all(v['passed'] and v['valid_choice_count']==1 for v in math)
# A controlled SAME bank and order: initial condition only, then ODE only.
before=groups[2][0];a0=r0=None
# Select same coefficient/different constants directly from printed bank, then
# same initial ordinate/different coefficient. All eligible roles already tested.
for a in groups[2]:
 for b in groups[2]:
  if a is b:continue
  oa,ica=prompt_data(a);ob,icb=prompt_data(b)
  if simplify(oa-ob)==0 and ica[0]==icb[0] and simplify(ica[1]-icb[1])!=0: a0,b0=a,b
  if simplify(oa-ob)!=0 and ica==icb:a1,b1=a,b
assert a0 is not None
ir=copy.deepcopy(a0);ir['question'][':question/problem']=ir['question'][':question/problem'].replace('Find','Determine');field(ir)[':answer-field/choices'].reverse()
cf=[a0,b0,a1,b1,ir];save('counterfactual-records.json',cf)
save('counterfactual-results.json',{'IC_only':{'same_ODE':simplify(prompt_data(a0)[0]-prompt_data(b0)[0])==0,'bank_same_in_order':[a[':answer/value'] for a in field(a0)[':answer-field/choices']]==[a[':answer/value'] for a in field(b0)[':answer-field/choices']],'key_difference':str(simplify(explicit(b0,correct(b0))-explicit(a0,correct(a0)))),'ordinate_difference':str(simplify(prompt_data(b0)[1][1]-prompt_data(a0)[1][1]))},'ODE_only':{'same_IC':prompt_data(a1)[1]==prompt_data(b1)[1],'different_ODE':simplify(prompt_data(a1)[0]-prompt_data(b1)[0])!=0,'key_difference':str(simplify(explicit(b1,correct(b1))-explicit(a1,correct(a1))))},'irrelevant':{'same_response':correct(ir)==correct(a0),'same_correct_uuid':field(ir)[':answer-field/correct']==field(a0)[':answer-field/correct']},'render_and_grading':'All five cf records are rendered and all own-bank choices tested; old correct value is a real wrong candidate in each relevant pair.'})
# Demonstrated scaffold failure: the arbitrary C makes constant shifts equivalent.
sine=next(r for r in batch if r['generation']['template']=='q-126765');v=expr(correct(sine));h=sine['generation']['parameters']['h'];C=S.Symbol('C',real=True)
variants=[S.expand(v-v.subs(x,0)),v+1];proof=[]
for candidate in variants:
 delta=simplify(candidate-v)
 proof.append({'submitted':str(candidate).replace('**','^'),'constant_difference':str(delta),'derivative_difference':str(simplify(S.diff(candidate,x)-S.diff(v,x))),'family_identity':str(simplify((candidate+C)-(v+(C+delta)))),'expected':'accepted','justification':'C is arbitrary; reparameterize C_new=C+delta. Both explicit sine families and local branch ranges coincide.'})
save('sine-scaffold-proof.json',{'question_id':sine['question'][':question/id'],'source_id':'1bc80b6f-e02e-58f0-97b4-8ea651af23ac','generation':sine['generation'],'record':'batch.json','variants':proof})
# Native grader: retained independent checks, all changed roles, small regressions,
# full runner batch, and counterfactuals. Strict new equivalents retained separately.
cases=json.load(open(E/'retained-grader-input.json'))
for i,r in enumerate(roles+controls+reg+batch+cf):
 f=field(r)
 if f[':answer-field/type'].endswith('/radio'):
  checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected'} for a in f[':answer-field/choices']]
 else:
  v0=correct(r);alt=str(expr(v0)).replace('**','^').replace('log(','ln(').replace('E','e')
  checks=[{'submitted':v0,'expected':'accepted'},{'submitted':alt,'expected':'accepted'},{'submitted':'0','expected':'rejected'}]
  if r['generation']['template']!='q-126765':checks.append({'submitted':'('+v0+')+1','expected':'rejected'})
  else:checks.append({'submitted':'2*(x-3)^2','expected':'rejected','purpose':'wrong derivative cannot be absorbed into C'})
  if r['generation']['template']=='q-128199':checks.append({'submitted':'-('+v0+')','expected':'rejected'})
 cases.append({'label':'current '+str(i)+' '+r['generation']['template'],'record':r,'checks':checks})
# Observation matches the actual engine outcome, without weakening strict expectations.
strict={'label':'exact batch sine scaffold arbitrary C','record':sine,'checks':[{'submitted':p['submitted'],'expected':'accepted','purpose':p['justification']} for p in proof]}
save('sine-scaffold-grader-input.json',[strict])
obs=copy.deepcopy(strict)
for c in obs['checks']:c['expected']='rejected';c['purpose']='Observe known defect; strict acceptance assertion retained in sine-scaffold-grader-input.json'
cases.append(obs);save('grader-observation-input.json',cases)
cmd=[str(ROOT/'generate/runs/current/check-engine'),str(E/'grader-observation-input.json'),str(E/'grader-observation-report.json')]
p=subprocess.run(cmd,capture_output=True,text=True);(E/'grader-observation-console.txt').write_text(p.stdout+p.stderr)
save('grader-execution.json',{'command':cmd,'exit':p.returncode,'cases':len(cases),'checks':sum(len(c['checks']) for c in cases),'strict_failure_file':'sine-scaffold-grader-input.json','warning':'Successful observation includes EXPECTED REJECTIONS of mathematically valid scaffold entries; grading verdict FAILS.'})
assert p.returncode==0,p.stderr
cmd=[str(ROOT/'generate/runs/current/check-engine'),str(E/'sine-scaffold-grader-input.json'),str(E/'sine-scaffold-grader-report.json')]
p=subprocess.run(cmd,capture_output=True,text=True);(E/'sine-scaffold-grader-console.txt').write_text(p.stdout+p.stderr)
save('sine-scaffold-grader-execution.json',{'command':cmd,'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'expected_exit_after_repair':0})
# Source/revision milestones persisted.
save('render-records.json',batch+cf+[reg[0]])
save('samples.json',roles+controls+reg)
(E/'session-state.md').write_text('Source replay: all 25 valid banks/keys matched; invalid IVP excluded with proof. Current finite trig construction: 75 role records/math results saved; prior controls and small regression checked. Exact batch and controlled pairs checked. Native observation and strict sine-scaffold failure retained. Delivery/render/packaging pending.\n')
print('math',len(math),'native observation',len(cases),'strict scaffold exit',p.returncode,flush=True)
