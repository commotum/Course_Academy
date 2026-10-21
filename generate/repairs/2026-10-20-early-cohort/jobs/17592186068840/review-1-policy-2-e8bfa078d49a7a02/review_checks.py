"""Independent focused review. All writes are beneath this script's directory.
Run: /home/jake/Developer/Course_Academy/.venv/bin/python -B review_checks.py
"""
import collections,hashlib,importlib.util,json,pathlib,platform,re,shutil,subprocess,sys
sys.dont_write_bytecode=True
E=pathlib.Path(__file__).resolve().parent;J=E.parent;W=J/'workspace';R=pathlib.Path('/home/jake/Developer/Course_Academy')
def save(n,x): (E/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def load(n):return json.loads((E/n).read_text())
spec=importlib.util.spec_from_file_location('reviewed',W/'17592186068840.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
# A syntax reader only; all derivatives, expectations and decisions below are independent.
from latex_reader import parse,equal,X,Y,C,K,s

def field(r):return r['question'][':question/answer-fields'][0]
def key(r):
 f=field(r);return next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
def cmd(args,out):
 p=subprocess.run(list(map(str,args)),text=True,capture_output=True,cwd=E)
 save(out,{'command':list(map(str,args)),'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr});return p

def pset(n,a=1,h=3):
 p={'a':a}
 if n=='autonomous_tan':p['candidates']=[-2,-1,1,2,3]
 else:p['h']=h
 if n=='affine_root':p['b']=-2
 return p
families=['autonomous_tan','reciprocal_cube','negative_exp','cube_power','affine_root']
rows=[]
for n in families:
 for a in [-2,-1,1,2,3]:rows.append(g.generate_easy(82711,n,parameters=pset(n,a)))
 if n!='autonomous_tan':
  for h,a in [(-8,-2),(8,3)]:rows.append(g.generate_easy(82719,n,parameters=pset(n,a,h)))
for seed in range(82031,82043):rows.append(g.generate_easy(seed))
rows.append(g.generate_easy(82721,'autonomous_tan',parameters={'a':5,'candidates':[-2,-1,2,3,5]}))
save('independent-easy-current.json',rows)
# New blank families and a small unchanged moderate regression sample.
moderate=[]
for n in ['reciprocal_blank','context_log_blank']:
 for a in [-2,3]:moderate.append(g.generate_moderate(82801,n,parameters={'a':a}))
for b,rate in [(15,'0.02'),(35,'0.06'),(25,'0.03')]:moderate.append(g.generate_moderate(82803,'temperature_blank',parameters={'ambient':b,'rate':rate}))
for n in ['linear_sin','linear_cos','linear_sec2','linear_power','linear_arcsin','linear_sectan']:moderate.append(g.generate_moderate(82811,n,parameters={'h':-3}))
save('moderate-current.json',moderate)
# Replay every original source question, using its own ID/bank/key as the oracle.
source=json.loads((J/'source/source.json').read_text())['material']['kp'];replay=[];replay_result=[]
byid={t['source'][':question/id']:n for n,t in g.TEMPLATES.items() if 'source' in t}
def norm(t):
 return re.sub(r'\s+','',t.replace('\u2061','').replace(r'\left','').replace(r'\right',''))
for q in source[':knowledge-point/questions']:
 n=byid.get(q[':question/id']);assert n is not None,q[':question/id']
 p={'a':1} if n=='autonomous_tan' else {'a':2} if n=='reciprocal_blank' else {'a':3} if n=='context_log_blank' else {'rate':'0.03','ambient':25} if n=='temperature_blank' else {'h':0}
 r=g.generate(q[':question/difficulty'][':db/ident'].split('/')[-1],82823,n,parameters=p,profile='observed_'+n);replay.append(r);f=field(r);sf=q[':question/answer-fields'][0]
 checks={k:norm(r['question'][k])==norm(q[k]) for k in [':question/problem',':question/worked-solution']}
 checks.update(bank=sorted(norm(a[':answer/value']) for a in f[':answer-field/choices'])==sorted(norm(a[':answer/value']) for a in sf[':answer-field/choices']),correct=norm(key(r))==norm(sf[':answer-field/correct'][':answer/value']),response_type=f[':answer-field/type']==sf[':answer-field/type'][':db/ident'])
 replay_result.append({'source_id':q[':question/id'],'template':n,'checks':checks});assert all(checks.values())
save('source-replay-records.json',replay);save('source-replay.json',{'cases':replay_result,'passed':True,'normalization':'Only whitespace, U+2061 and delimiter sizing ignored; all complete banks compared.'})
# Relevant a-only pairs, irrelevant shuffle-only pairs, and ambient-only blank pair.
pairs=[];pairtests=[]
for n in families:
 before=g.generate_easy(82903,n,parameters=pset(n,-1));after=g.generate_easy(82903,n,parameters=pset(n,2));irrelevant=g.generate_easy(82904,n,parameters=pset(n,-1));pairs.extend([before,after,irrelevant])
 pairtests.append({'template':n,'indices':[len(pairs)-3,len(pairs)-2,len(pairs)-1],'relevant_expected':'same complete bank, changed equation/key/solution','relevant_passed':key(before)!=key(after) and all(before['question'][k]!=after['question'][k] for k in [':question/problem',':question/worked-solution']) and sorted(a[':answer/value'] for a in field(before)[':answer-field/choices'])==sorted(a[':answer/value'] for a in field(after)[':answer-field/choices']),'irrelevant_expected':'same equation, solution and answer; options may reorder','irrelevant_passed':key(before)==key(irrelevant) and all(before['question'][k]==irrelevant['question'][k] for k in [':question/problem',':question/worked-solution'])})
pairs.extend([g.generate_moderate(82911,'temperature_blank',parameters={'rate':'0.03','ambient':b}) for b in [25,35]])
pairtests.append({'template':'temperature_blank','indices':[15,16],'irrelevant_expected':'ambient changes prompt and full solution, not requested exponential factor','irrelevant_passed':key(pairs[-2])==key(pairs[-1]) and all(pairs[-2]['question'][k]!=pairs[-1]['question'][k] for k in [':question/problem',':question/worked-solution'])})
assert all(v for t in pairtests for k,v in t.items() if k.endswith('_passed'))
save('counterfactual-records.json',pairs);save('counterfactual-results.json',pairtests)
# Independent exact visible-expression oracle: integrate lhs derivative identity;
# power solutions use implicit polynomials, avoiding principal complex cube roots.
def rhs_of(r):
 spans=re.findall(r'\$([^$]+)\$',r['question'][':question/problem']);v=next(v for v in spans if '=' in v and ('′' in v or r'\frac' in v));return parse(v.split('=',1)[1].rstrip('.'))
def valid(v,rhs):
 if Y in v.free_symbols or not ({C,K}&v.free_symbols):return False
 if v.is_Pow and v.exp==s.Rational(1,3):return equal(s.diff(v.base,X),3*Y**2*rhs)
 if v.is_Pow and v.exp==3:return equal(3*s.diff(v.base,X),rhs/s.Abs(Y)**s.Rational(2,3))
 if v.is_Pow and v.exp==s.Rational(1,2):return equal(s.diff(v.base,X),2*Y*rhs)
 return equal(s.diff(v,X),rhs.subs(Y,v))
math=[]
for r in rows+load('batch-records.json')+pairs[:15]:
 rhs=rhs_of(r);choices=[]
 for a in field(r)[':answer-field/choices']:
  text=a[':answer/value'];v=parse(text.split('=',1)[1]);truth=valid(v,rhs);isk=a[':answer/id']==field(r)[':answer-field/correct'][1]
  assert truth==isk,(r['question'][':question/problem'],text,truth)
  if v.is_Pow and v.exp==s.Rational(1,2):assert r'\pm' in text,'square root needs both branches'
  choices.append({'value':text,'key':isk,'valid':truth})
 aligned=re.findall(r'\\begin\{aligned\}([\s\S]*?)\\end\{aligned\}',r['question'][':question/worked-solution']);left,right=aligned[1].split(r'\\')[-1].split(' & =');F,H=parse(left),parse(right)
 prim_ok=equal(3*s.diff(H,X),rhs/s.Abs(Y)**s.Rational(2,3)) if F==Y**s.Rational(1,3) else equal(s.diff(F,Y)*rhs,s.diff(H,X))
 assert prim_ok,(F,H,rhs)
 last=re.findall(r'\$\$\s*([\s\S]*?)\s*\$\$',r['question'][':question/worked-solution'])[-1]
 if r'\begin{aligned}' in last:last=last.split(r'\\')[-1].replace(r'\end{aligned}','').replace(' & =','=')
 v=parse(last.strip().rstrip('.').split('=',1)[1]);assert equal(v,parse(key(r).split('=',1)[1]))
 math.append({'id':r['question'][':question/id'],'rhs':str(rhs),'choices':choices,'primitive_derivative':prim_ok,'displayed_solution_matches':True})
save('math-results.json',{'cases':math,'passed':True,'method':'Read displayed ODE, all five choices, implicit integral row and final solution; exact symbolic derivative identities, with real cube and both square-root branch handling. No generator data() used.'})
# Blanks: derive full solutions directly from displayed requested factors and ODE.
blank_results=[]
for r in moderate+pairs[15:]:
 if not field(r)[':answer-field/type'].endswith('/blank'):continue
 n=r['generation']['template'];v=parse(key(r));rhs=rhs_of(r);rhs=rhs.xreplace({z:Y for z in rhs.free_symbols if z.name in ['s','p']})
 if n=='temperature_blank':b=int(re.search(r'T=([0-9]+)',r['question'][':question/problem'])[1]);full=b+K*v
 elif n=='reciprocal_blank':full=1/(v+K)
 else:full=s.log(v+C)
 assert equal(s.diff(full,X),rhs.subs(Y,full)),(n,full,rhs)
 blank_results.append({'id':r['question'][':question/id'],'rhs':str(rhs),'full_solution':str(full),'derivative_checked':True})
save('blank-math.json',{'cases':blank_results,'passed':True})
# Package boundaries and exact declared environment; no package outputs permitted.
manifest=json.loads((W/'package.json').read_text());runtime={'python':platform.python_version(),'packages':{'sympy':s.__version__}}
rejections=[]
for level,n,p in [('easy','reciprocal_cube',{'a':0,'h':0}),('easy','affine_root',{'a':1,'b':0,'h':0}),('easy','negative_exp',{'a':1,'h':9}),('easy','cube_power',{'a':1,'h':-9}),('easy','autonomous_tan',{'a':1,'candidates':[1,1,2,3,4]}),('moderate','reciprocal_blank',{'a':0}),('moderate','context_log_blank',{'a':4}),('moderate','temperature_blank',{'rate':'0','ambient':25})]:
 try:g.generate(level,83001,n,parameters=p);out='accepted'
 except ValueError as ex:out='rejected: '+str(ex)
 rejections.append({'level':level,'template':n,'parameters':p,'outcome':out});assert out.startswith('rejected')
rel=E/'relocated';rel.mkdir(exist_ok=True)
for f in manifest['files']+['package.json']:
 dest=rel/f;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(W/f,dest)
r=g.generate_easy(83007);p=cmd([sys.executable,'-B',rel/'17592186068840.py','--difficulty','easy','--seed','83007','--format','json'],'relocation-execution.json');rel_equal=p.returncode==0 and json.loads(p.stdout)==[r];assert rel_equal
save('packaging.json',{'manifest':manifest,'runtime':runtime,'exact_dependency_match':manifest['dependencies']==runtime,'deterministic':r==g.generate_easy(83007),'relocation_equal':rel_equal,'boundary_rejections':rejections,'output_contract':'stdout JSON; no runtime file writes, network, database calls or assets in inspected entrypoint.'});assert manifest['dependencies']==runtime
# Complete native learner checks plus pair responses identified by visible value.
cases=[]
for i,r in enumerate(rows+moderate+load('batch-records.json')+pairs+replay):
 f=field(r);checks=[]
 if f[':answer-field/type'].endswith('/radio'):
  checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'each full bank choice'} for a in f[':answer-field/choices']]
 else:
  n=r['generation']['template'];v=parse(key(r));checks=[{'submitted':key(r),'expected':'accepted','purpose':'stored answer'},{'submitted':'0','expected':'rejected','purpose':'zero is wrong factor/fragment'}]
  if n=='temperature_blank':
   rate=r['generation']['parameters']['rate'];checks.extend([{'submitted':r'\frac{1}{e^{'+rate+'t}}','expected':'accepted','purpose':'source-valid reciprocal exponential'},{'submitted':'e^{'+rate+'t}','expected':'rejected','purpose':'wrong sign'},{'submitted':r'e^{\frac{-'+str(int(s.Rational(rate)*100))+r't}{100}}','expected':'accepted','purpose':'rational exponent'}])
  else:
   a=s.diff(v,X);checks.extend([{'submitted':str(2*a)+'t/2','expected':'accepted','purpose':'equivalent fragment'},{'submitted':str(-a)+'t','expected':'rejected','purpose':'wrong sign'}])
 cases.append({'label':str(i)+' '+r['generation']['template'],'record':r,'checks':checks})
for i in range(0,15,3):
 a,b,irr=pairs[i:i+3];old=key(a);z=next(x for x in field(b)[':answer-field/choices'] if x[':answer/value']==old);z2=next(x for x in field(irr)[':answer-field/choices'] if x[':answer/value']==old)
 cases.extend([{'label':'controlled relevant stale answer '+a['generation']['template'],'record':b,'checks':[{'submitted_answer_id':z[':answer/id'],'expected':'rejected','purpose':'before answer must fail after relevant coefficient changes'}]},{'label':'controlled irrelevant same answer '+a['generation']['template'],'record':irr,'checks':[{'submitted_answer_id':z2[':answer/id'],'expected':'accepted','purpose':'preserve answer after irrelevant shuffle'}]}])
cases+=load('grader-reciprocal-input.json');save('grader-input.json',cases)
p=cmd([R/'generate/runs/current/check-engine',E/'grader-input.json',E/'grader-results.json'],'grader-execution.json');assert p.returncode==0,p.stderr
save('sampling.json',{'fresh_seed_range':[82031,82042],'easy_count':len(rows),'moderate_count':len(moderate),'easy_counts':dict(collections.Counter(r['generation']['template'] for r in rows)),'all_five_coefficient_roles_per_easy_family':True,'generator_rejections':rejections,'resampling':'No caller resampling required in selected fresh draws or supported boundaries. Inspected bank-equivalence guard rejects whole records, not target cases; every easy coefficient survived.'})
render=load('batch-records.json')+[pairs[0],pairs[1],pairs[2],pairs[15],pairs[16]]+[rows[28],rows[-1]]+[next(r for r in moderate if r['generation']['template']==n) for n in ['reciprocal_blank','context_log_blank']]
save('render-records.json',render);save('render-counterfactuals.json',pairs)
(E/'session-state.md').write_text('Completed source replay (14 banks), old/current retained counterexamples, independent easy visible math and blank derivatives, boundaries/runtime/relocation and batched native grading. Next: delivery, conditional shortcut metrics, selector and inventory review, actual UI screenshots.\n')
print(json.dumps({'source_cases':len(replay),'easy_samples':len(rows),'math_cases':len(math),'native_cases':len(cases),'grader':p.stdout.strip(),'render_records':len(render)}))
