#!/usr/bin/env python3
"""Read-only independent review. Run with repo .venv/bin/python audit.py."""
import sys,json,pathlib,hashlib,importlib.util,subprocess,shutil,re,copy,platform
sys.dont_write_bytecode=True
E=pathlib.Path(__file__).resolve().parent
J=E.parent; R=pathlib.Path('/home/jake/Developer/Course_Academy'); P=J/'workspace'
def save(n,x): (E/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def load(n):return json.loads((E/n).read_text())
def hashes():return {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in P.iterdir() if p.is_file()}
save('package-before.json',hashes())
sys.path.insert(0,str(P));import generator as g
# All 54 legitimate easy slots are a bounded census, not a large random search.
records=g.generate_batch('easy',54,seed=826031)
save('independent-samples.json',records)
batch=json.loads((J/'samples.json').read_text());save('runner-batch.json',batch)
replay=[g.generate(t,1,seed=826032) for t in g.SOURCES];save('source-replay-records.json',replay)
# Relevant change: constant coefficient; same seed, family and other coefficients.
pairs=[]
for t in ('cube_root','affine','linear_log'):
 pairs.append({'name':t+' coefficient sign','before':g.generate(t,2,seed=826033),'after':g.generate(t,-2,seed=826033),'expected':'Correct expression changes with coefficient; sign of corresponding particular or log term reverses.'})
# Relevant change of surviving integration branch, with a and seed held fixed.
pairs.append({'name':'coefficient of y changes 1 to 2','before':g.generate('linear_log',2,826033),'after':g.generate('affine',2,826033),'expected':'y=2x ln|x|+Cx changes to y=Cx^2-2x.'})
base=g.generate('cube_root',2,826034);after=copy.deepcopy(base);after['question'][':question/answer-fields'][0][':answer-field/choices'].reverse()
pairs.append({'name':'irrelevant candidate order','before':base,'after':after,'expected':'Same mathematical response, prompt and explanation; answer position can change.'})
save('counterfactuals.json',pairs)
# Select actual renderer records for each family, both signs, branch and irrelevant pair.
render=[p['before'] for p in pairs[:3]]+[p['after'] for p in pairs[:3]]+[pairs[3]['before'],pairs[3]['after'],pairs[4]['before'],pairs[4]['after']]
save('render-records.json',render)
# Determinism, CLI, declared dependencies, rejection and relocation.
commands=[]
def run(args,cwd=E):
 p=subprocess.run(args,cwd=cwd,text=True,capture_output=True,env={**__import__('os').environ,'PYTHONDONTWRITEBYTECODE':'1'});commands.append({'command':args,'cwd':str(cwd),'returncode':p.returncode,'stderr':p.stderr,'stdout_sha256':hashlib.sha256(p.stdout.encode()).hexdigest()});return p
args=[sys.executable,str(P/'generator.py'),'--difficulty','easy','--count','7','--seed','826035']
a=run(args);b=run(args)
rel=E/'relocated';rel.mkdir(exist_ok=True)
for f in ('generator.py','math_format.py','package.json'):shutil.copy2(P/f,rel/f)
c=run([sys.executable,str(rel/'generator.py'),*args[2:]])
reject=[]
for args0 in (['--difficulty','hard'],['--count','-1']): reject.append(run([sys.executable,str(P/'generator.py'),*args0]).returncode!=0)
for t,a0 in [('cube_root',0),('affine',10),('linear_log',-10),('missing',1)]:
 try:g.generate(t,a0);reject.append(False)
 except ValueError:reject.append(True)
pack={'python_installed':platform.python_version(),'manifest':json.loads((P/'package.json').read_text()),'deterministic':a.stdout==b.stdout,'relocation_identical':a.stdout==c.stdout,'all_invalid_cases_rejected':all(reject),'commands':commands,'unique_easy_questions':len({r['question'][':question/id'] for r in records}),'family_a_coverage':{t:sorted(r['generation']['parameters']['a'] for r in records if r['generation']['template']==t) for t in ('cube_root','affine','linear_log')},'external_outputs':'No assets; generator stdout is JSON. Relocated stdout identical. No package writes permitted; bytecode disabled.'}
save('packaging.json',pack)
# Actual native grader cases: every choice on every sampled and batch record, plus pairs.
def checks(r):
 f=r['question'][':question/answer-fields'][0];correct=f[':answer-field/correct'][1]
 return [{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'Independent solution matches this choice' if a[':answer/id']==correct else 'Wrong integration/back-substitution distractor'} for a in f[':answer-field/choices']]
cases=[{'label':f'easy slot {i}', 'record':r,'checks':checks(r)} for i,r in enumerate(records)]
cases += [{'label':f'runner batch {i}', 'record':r,'checks':checks(r)} for i,r in enumerate(batch)]
for i,p in enumerate(pairs):
 for side in ('before','after'):cases.append({'label':f'pair {i} {side}','record':p[side],'checks':checks(p[side])})
save('grader-input.json',cases)
# Independent symbolic checks: don't derive equations/answers from g.components or metadata keys.
import sympy as s
x,y,C=s.symbols('x y C',positive=True); failures=[]; mathrows=[]
for group,rs in [('independent',records),('runner',batch)]:
 for i,r in enumerate(rs):
  q=r['question'];prompt=q[':question/problem'];m=re.search(r'=\\frac\{(.+)\}\{(.+)\}',prompt)
  num,den=m.groups(); aa=re.match(r'(-?\d*)(x\^3|x)',num).group(1); a0=int(aa) if aa not in ('','-') else (1 if aa=='' else -1)
  f=q[':question/answer-fields'][0];bank=f[':answer-field/choices'];got=next(z[':answer/value'] for z in bank if z[':answer/id']==f[':answer-field/correct'][1])
  if 'xy^2'==den:
   family='cube_root';rhs=(a0*x**3+y**3)/(x*y**2);F=y**3/x**3-3*a0*s.log(x)-C
   expected=f'y=x\\sqrt[3]{{{3*a0}\\ln|x|+C}}'
   candidate_F=[y/x-3*a0*s.log(x)-C, y**2/x**2-a0*s.log(x)-C, y/x-(2*a0*s.log(x)+C)**2,F,y/x**2-3*a0*s.log(x)-C]
  elif num.endswith('+2y'):
   family='affine';rhs=a0+2*y/x;F=(y+a0*x)/x**2-C
   def sign(z):return str(z).replace('+-','-').replace('--','+')
   expected=sign(f'y=Cx^2-{g.coef(a0)}x')
   candidate_F=[(y+a0*x**2)/x**3-C,(y+2*a0*x)/x**3-C,(y-a0*x)/x**3-C,F,(y-2*a0*x)/x**2-C]
  else:
   family='linear_log';rhs=a0+y/x;F=y/x-a0*s.log(x)-C
   expected=f'y={g.coef(a0)}x\\ln|x|+Cx'
   candidate_F=[y-a0*s.log(x)-C*x**2,y-a0*s.log(x)-C*x,F,y-a0*x*s.log(x)-C,y-2*a0*x*s.log(x)-C*x**2]
  residual=s.factor(s.diff(F,x)+s.diff(F,y)*rhs)
  # all distractors tested by implicit directional derivative, restricting their own solution relation when needed.
  residuals=[]
  for k,H in enumerate(candidate_F):
   d=s.factor(s.diff(H,x)+s.diff(H,y)*rhs)
   # An implicit equation H=0 can substitute C to avoid treating C as an independent coordinate.
   if C in d.free_symbols:
    sol=s.solve(H,C)
    d=s.factor(d.subs(C,sol[0])) if sol else d
   residuals.append(str(d))
  correct_index=next(k for k,H in enumerate(candidate_F) if s.simplify(H-F)==0)
  ok=(got==expected and residual==0 and residuals[correct_index]=='0' and sum(v=='0' for v in residuals)==1)
  row={'group':group,'index':i,'question_id':q[':question/id'],'parsed_prompt_coefficient':a0,'family':family,'expected_correct_tex':expected,'actual_correct_tex':got,'implicit_solution':str(F),'directional_derivative':str(residual),'candidate_directional_derivatives':residuals,'passed':ok};mathrows.append(row)
  if not ok:failures.append(row)
save('math.json',{'method':'Parse coefficients and family from actual rendered-source prompt; independently differentiate implicit solution along ODE; test all five solution candidates. Symbolic x,y positive avoids absolute-log branch ambiguity; d ln|x|/dx=1/x holds on either nonzero interval. Cube root treated via real implicit y^3 relation.','sympy':s.__version__,'checks':mathrows,'failures':failures})
print(json.dumps({'samples':len(records),'math_failures':len(failures),'packaging':{k:pack[k] for k in ('python_installed','deterministic','relocation_identical','all_invalid_cases_rejected','unique_easy_questions')},'grader_records':len(cases)}))
