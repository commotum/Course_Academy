"""Independent, read-only audit. Run: PYTHONDONTWRITEBYTECODE=1 <job python> review.py"""
import json, pathlib, sys, hashlib, importlib.util, re, subprocess, shutil, copy
from functools import lru_cache
E=pathlib.Path(__file__).resolve().parent
sys.dont_write_bytecode=True
sys.path.insert(0,str(E/'deps'))
import sympy as S
from sympy.parsing.latex import parse_latex
R=pathlib.Path('/home/jake/Developer/Course_Academy')
J=E.parent; W=J/'workspace'; P=R/'.venv/bin/python'
def save(name,obj):
 p=E/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,indent=2,default=str)+'\n')
def load(path):return json.loads(path.read_text())
def hashes():return {str(p.relative_to(W)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(W.rglob('*')) if p.is_file()}
initial=hashes();save('package-before.json',initial)
spec=importlib.util.spec_from_file_location('audited_generator', W/'17592186147454.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
src=load(J/'source/source.json'); batch=load(J/'samples.json'); save('batch.json',batch)
questions=src['material']['kp'][':knowledge-point/questions'];source_by={q[':question/math-academy-id']:q for q in questions}
replays=[]; replay_results=[]
for t,q in source_by.items():
 if not q.get(':question/worked-solution') or not q[':question/answer-fields'][0].get(':answer-field/correct'):
  replay_results.append({'source_id':q[':question/id'],'template':t,'status':'unsupported','reason':'Captured key/solution absent; independent correction in source-analysis.json. Source says hard, contrary to author claim of missing rating.'});continue
 level=q[':question/difficulty'][':db/ident'].split('/')[-1]
 r=g.generate(level, 731, t, {'shift':0});replays.append(r);f=r['question'][':question/answer-fields'][0];sf=q[':question/answer-fields'][0]
 checks={'prompt':r['question'][':question/problem']==q[':question/problem'],'solution':r['question'][':question/worked-solution'].replace(r'\left','').replace(r'\right','')==q[':question/worked-solution'].replace(r'\left','').replace(r'\right',''),'complete_bank':sorted(a[':answer/value'].replace(r'\left','').replace(r'\right','') for a in f[':answer-field/choices'])==sorted(a[':answer/value'].replace(r'\left','').replace(r'\right','') for a in sf[':answer-field/choices']),'key':next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]).replace(r'\left','').replace(r'\right','')==sf[':answer-field/correct'][':answer/value'].replace(r'\left','').replace(r'\right','')}
 replay_results.append({'source_id':q[':question/id'],'template':t,'status':'passed','checks':checks})
save('source-replays.json',replays); save('source-replay-results.json',{'cases':replay_results,'canonical':'047ea3c1-8ebf-5e26-9f28-c5a87e7cf997 has no radio bank and no executable template; independent derivative check in math-results.json','source_corrections':'Nonzero domain wording appropriate; explicit reciprocal notation fixes ambiguous source 1/4x and 3/2x.'})
records=[]
for t,q in source_by.items():
 if t not in g.SOURCES or t=='q-109029':continue
 level=q[':question/difficulty'][':db/ident'].split('/')[-1]
 for h in [-6,6]:records.append(g.generate(level,192337,t,{'shift':h}))
for seed in range(71831,71841):records.append(g.generate('moderate',seed))
a=g.generate('moderate',98301,'q-109154',{'shift':1});b=g.generate('moderate',98301,'q-109154',{'shift':2});c=g.generate('moderate',73429,'q-109154',{'shift':1})
records.extend([a,b,c]); save('independent-samples.json',records)
save('moderate-samples.json',[r for r in records if r['question'][':question/difficulty'].endswith('/moderate')]);save('hard-samples.json',[r for r in records if r['question'][':question/difficulty'].endswith('/hard')])
save('counterfactual-records.json',[a,b,c])
x,y,C,D=S.symbols('x y C D', positive=True)
@lru_cache(None)
def parse(s):
 s=s.strip().rstrip('.,').replace(r'\pm','').replace('\u2061','').replace(r'\dfrac',r'\frac')
 s=re.sub(r'\\frac\{\\text\{d\}y\}\{\\text\{d\}x\}|\\frac\{dy\}\{dx\}', 'D',s)
 v=parse_latex(s,strict=True)
 return v.xreplace({z:{'x':x,'y':y,'C':C,'D':D,'e':S.E}.get(str(z),z) for z in v.free_symbols})
@lru_cache(None)
def solve_check(prompt,values,h):
 eq=re.search(r'\$\$([\s\S]*?)\$\$',prompt)[1].strip().rstrip('.');l,r=eq.split('=');F=S.expand(parse(l)-parse(r));F=S.simplify(-F.subs(D,0)/S.diff(F,D));F=S.expand(F.subs(x,x-h))
 # Determine powers from displayed ODE, not generation template or expected key.
 terms=S.Add.make_args(F);exponents={S.simplify(y*S.diff(t,y)/t) for t in terms}; assert 1 in exponents and len(exponents)==2,exponents
 n=next(e for e in exponents if e!=1)
 p=S.simplify(-sum(t/y for t in terms if S.simplify(y*S.diff(t,y)/t)==1));q=S.simplify(sum(t/y**n for t in terms if S.simplify(y*S.diff(t,y)/t)==n))
 result=[]
 for text in values:
  Y=S.simplify(parse(text.split('=',1)[1]).subs(x,x-h));z=S.powdenest(Y**(1-n),force=True)
  if n==S.Rational(1,2):z=z.replace(S.Abs,lambda v:v)
  z=S.simplify(z)
  res=linear_residual(z,p,q,n)
  result.append({'value':text,'transformed_z':str(z),'residual':str(res),'is_solution':res==0})
 return {'p':str(p),'q':str(q),'n':str(n),'choices':result}
@lru_cache(None)
def linear_residual(z,p,q,n):return S.simplify(S.expand(S.diff(z,x)+(1-n)*p*z-(1-n)*q))
math=[]
for i,r in enumerate(replays+records+batch):
 q=r['question'];f=q[':question/answer-fields'][0];vals=tuple(v[':answer/value'] for v in f[':answer-field/choices']);h=r['generation']['parameters']['shift']
 result=copy.deepcopy(solve_check(q[':question/problem'],vals,h));result['question_id']=q[':question/id'];result['template']=r['generation']['template'];result['shift']=h
 keys=[a[':answer/id']==f[':answer-field/correct'][1] for a in f[':answer-field/choices']]
 result['correct_key_matches_unique_solution']=[v['is_solution'] for v in result['choices']]==keys
 assert result['correct_key_matches_unique_solution'],result
 math.append(result)
 if i%10==0: print('math verified',i+1,flush=True);save('math-progress.json',math)
canonical_z=(2*x**5+C)/(5*x**2)
assert S.simplify(S.diff(canonical_z,x)+2/x*canonical_z-2*x**2)==0
save('math-results.json',{'method':'Independently parse displayed ODE and every choice with antlr/SymPy; infer p,q,n and verify residual of z=Y^(1-n). Real branches as specified; even roots require positive z. No generator math helpers called.','cases':math,'canonical_residual':'0','all_unique_keys_correct':True})
checks=[]
for r in replays+records+batch:
 f=r['question'][':question/answer-fields'][0]
 checks.append({'label':r['question'][':question/id'],'record':r,'checks':[{'field_index':0,'submitted_answer_id':v[':answer/id'],'expected':'accepted' if v[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Independently residual-verified entire radio bank'} for v in f[':answer-field/choices']]})
save('grader-input.json',checks)
proc=subprocess.run([str(R/'generate/runs/current/check-engine'),str(E/'grader-input.json'),str(E/'grader-report.json')],capture_output=True,text=True);save('grader-execution.json',{'command':proc.args,'exit_code':proc.returncode,'stdout':proc.stdout,'stderr':proc.stderr});assert proc.returncode==0
# A relevant shift changes mathematical solution; irrelevant seed leaves rendered content intact.
assert a['question']!=b['question'] and a['question']==c['question']
# Eligible coefficient is deliberately attempted at the API boundary; current generator refuses it.
try:g.generate('moderate',98301,'q-109154',{'shift':1,'q_scale':2})
except (AssertionError,ValueError) as e:coeff={'status':'rejected','exception':type(e).__name__}
else:coeff={'status':'accepted'}
# Independent witness for required answer change under q -> 2q.
u=x+1;Y=5*u/(C-2*u**S.Rational(5,2));p=-1/u;qq=S.sqrt(u)
base=S.simplify(S.diff(Y,x)+p*Y-qq*Y**2);changed=S.simplify(S.diff(Y,x)+p*Y-2*qq*Y**2);new=S.simplify(S.diff(Y/2,x)+p*Y/2-2*qq*(Y/2)**2)
assert base==0 and changed!=0 and new==0
save('counterfactual-results.json',{'records':'counterfactual-records.json','relevant_shift':{'before':1,'after':2,'math_result':'both unique correct families verified from displayed math; formula argument and explanatory stages change together','grader':'All five outcomes checked for both in grader-report.json'},'irrelevant_seed':{'before':98301,'after':73429,'question_equal':a['question']==c['question'],'grader':'Identical complete question, all outcomes tested'},'eligible_coefficient':{'call':"generate('moderate',98301,'q-109154',{'shift':1,'q_scale':2})",'observed':coeff,'expected':'Same substitution and integration; displayed q doubles and solution Y must change to Y/2 (constant may be rescaled).','old_solution_residual_with_q_doubled':str(changed),'revised_solution_residual':'0'}})
# Determinism, boundary rejection, relocation using only runtime-relevant declared files.
reject=[]
for kwargs in [dict(difficulty='easy'),dict(difficulty='moderate',template='q-109154',parameters={'shift':7}),dict(difficulty='moderate',template='q-109154',parameters={'shift':-7}),dict(difficulty='moderate',template='q-109029',parameters={'shift':1}),dict(difficulty='hard',template='q-106074',parameters={'shift':1})]:
 try:g.generate(**kwargs)
 except (ValueError,AssertionError) as e:reject.append({'parameters':kwargs,'outcome':type(e).__name__})
 else:raise AssertionError(kwargs)
rel=E/'relocated';(rel/'17592186147454').mkdir(parents=True,exist_ok=True)
for name in ['17592186147454.py','17592186147454/source.json']:shutil.copyfile(W/name,rel/name)
cmd=[str(P),str(rel/'17592186147454.py'),'--difficulty','moderate','--seed','71831','--count','5'];run=subprocess.run(cmd,capture_output=True,text=True,env={**__import__('os').environ,'PYTHONDONTWRITEBYTECODE':'1'},cwd=E);assert run.returncode==0,run.stderr
out=json.loads(run.stdout);save('relocation-records.json',out)
run2=subprocess.run(cmd,capture_output=True,text=True,env={**__import__('os').environ,'PYTHONDONTWRITEBYTECODE':'1'},cwd=E);assert run2.stdout==run.stdout
manifest=load(W/'package.json');save('packaging-results.json',{'command':cmd,'relocation':'passed','deterministic_cli':'passed','boundary_rejections':reject,'installed':{'python':sys.version.split()[0],'packages':{'sympy':S.__version__}},'declared':manifest['dependencies'],'all_manifest_files_exist':all((W/p).is_file() for p in manifest['files']),'dependencies':'Runtime imports sympy only; antlr4 is independent reviewer-only dependency under evidence/deps. CLI generates JSON on stdout, no assets or file writes.','source_external':'Included source snapshot is a declared relative runtime dependency.','package_unchanged':hashes()==initial})
assert hashes()==initial;save('package-after.json',hashes())
(E/'session-state.md').write_text('Source reconstruction, exact supported-source replay, independent math/bank checks, native grader, controlled shifts/seed pairs, and relocation/boundary checks completed. Package hashes unchanged. Next: delivery/selection, shortcut statistics, actual-UI screenshots, inventory reproduction, final report.\n')
print('audit sample, math, grader, packaging complete',len(math),flush=True)
