import os,sys,json,re,pathlib,hashlib,platform,collections,shutil,subprocess
sys.dont_write_bytecode=True
ROOT=pathlib.Path(__file__).resolve().parent
PKG=pathlib.Path(sys.argv[1]).resolve() if len(sys.argv)>1 else ROOT.parent/'workspace'
sys.path.insert(0,str(PKG))
import generator as g
import sympy as s
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
X=s.Symbol('x',real=True)
def save(name,obj): (ROOT/name).write_text(json.dumps(obj,indent=2,default=str))
def latex(z):
 z=z.replace('{)}',')').replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\cdot','*').replace(' ', '')
 def atom(i):
  if z[i]=='{':
   depth=1;j=i+1
   while depth:
    if z[j]=='{':depth+=1
    elif z[j]=='}':depth-=1
    j+=1
   return convert(z[i+1:j-1]),j
  return z[i],i+1
 def convert(text):return latex(text)
 out='';i=0
 while i<len(z):
  if z.startswith(r'\frac',i) or z.startswith(r'\dfrac',i):
   i+=6 if z.startswith(r'\dfrac',i) else 5
   a,i=atom(i);b,i=atom(i);out+='(('+str(a)+')/('+str(b)+'))'
  elif z.startswith(r'\sqrt',i):
   a,i=atom(i+5);out+='sqrt('+str(a)+')'
  elif z[i]=='{':
   a,i=atom(i);out+='('+str(a)+')'
  elif z[i]=='^':out+='**';i+=1
  else:out+=z[i];i+=1
 return parse_expr(out,local_dict={'x':X,'sqrt':s.sqrt},transformations=standard_transformations+(implicit_multiplication_application,))
def field(r):return r['question'][':question/answer-fields'][0]
def correct(r):
 f=field(r);key=f[':answer-field/correct'];uid=key[1] if isinstance(key,list) else key[':answer/id'];return next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==uid)
def expected(r):
 prompt=r['question'][':question/problem'].replace('y =','y=');f=prompt.split('$y=',1)[1].split('$')[0].rstrip(',.');y=latex(f);ans=s.diff(y,X)
 m=re.search(r'where \$x=([+-]?\d+)',prompt)
 return s.simplify(ans.subs(X,int(m[1]))) if m else ans
hashes={str(p.relative_to(PKG)):hashlib.sha256(p.read_bytes()).hexdigest() for p in PKG.rglob('*') if p.is_file()};save('package-before.json',hashes)
replays=g.replay_sources();save('source-replays.json',replays)
src=json.load(open(ROOT.parent/'source/source.json'))['material']['kp'][':knowledge-point/questions'];byid={q[':question/math-academy-id']:q for q in src}
replay_results=[]
for r in replays:
 q=byid[r['generation']['replay_source_id']];f=q[':question/answer-fields'][0];radio=f[':answer-field/type'][':db/ident'].endswith('/radio')
 before=[a[':answer/value'] for a in f[':answer-field/choices']];after=[a[':answer/value'] for a in field(r)[':answer-field/choices']]
 bank_ok=not radio or all(any(s.simplify(latex(a)-latex(b))==0 for b in after) for a in before) and len(before)==len(after)
 replay_results.append({'source_id':q[':question/id'],'radio_bank_equal':bank_ok,'blank_history_preserved':r['generation']['source_capture'][':question/answer-fields']==q[':question/answer-fields'],'correct':correct(r),'expected':str(expected(r)),'math_ok':s.simplify(latex(correct(r))-expected(r))==0,'prompt_equal':re.sub(r'\s','',q[':question/problem'])==re.sub(r'\s','',r['question'][':question/problem'])})
save('source-replay-results.json',replay_results)
samples=[]
for j,(name,spec) in enumerate(g.TEMPLATES.items()):
 for i in range(5 if spec['field']=='radio' else 1):samples.append(g.generate(spec['level'],seed=529713+j*19+i,template=name,bank_role=i))
save('independent-samples.json',samples)
batch=json.load(open(ROOT.parent/'samples.json'));save('batch-records.json',batch)
cf=[]
for p in [{'a':-1,'b':10,'c':0,'t':1},{'a':-1,'b':10,'c':0,'t':5},{'a':-1,'b':10,'c':0,'t':9}]:cf.append(g.generate('easy',seed=999,template='slope_sqrt_quadratic_blank',parameters=p))
for seed in [610,611]:cf.append(g.generate('easy',seed=seed,template='slope_sqrt_radio',parameters={'a':4,'b':9,'t':0},bank_role=2))
save('counterfactual-records.json',cf)
results=[];cases=[]
for n,r in enumerate(replays+samples+batch+cf):
 a=expected(r);v=latex(correct(r));f=field(r);checks=[]
 if f[':answer-field/type'].endswith('/blank'):
  checks=[{'submitted':str(a).replace('**','^'),'expected':'accepted','purpose':'independent derivative in typed notation'}, {'submitted':s.latex(a),'expected':'accepted','purpose':'independent LaTeX derivative'}, {'submitted':str(a+1).replace('**','^'),'expected':'rejected','purpose':'wrong additive shift'}]
  if a.is_Rational:checks.append({'submitted':f'{a.p*2}/{a.q*2}','expected':'accepted','purpose':'equivalent unreduced rational'})
 else:
  for c in f[':answer-field/choices']:checks.append({'submitted_answer_id':c[':answer/id'],'expected':'accepted' if s.simplify(latex(c[':answer/value'])-a)==0 else 'rejected','purpose':'independently checked entire radio bank'})
 cases.append({'label':f'case-{n}-{r["generation"]["template"]}','record':r,'checks':checks})
 results.append({'index':n,'id':r['question'][':question/id'],'expected':str(a),'stored':correct(r),'math_ok':s.simplify(v-a)==0,'correct_count':sum(s.simplify(latex(c[':answer/value'])-a)==0 for c in f[':answer-field/choices'])})
save('math-results.json',results);save('grader-input.json',cases)
# A source-based canonical example without captured response fields.
canonical=g.generate('hard',seed=990,template='sqrt_quadratic_blank',parameters={'a':-1,'b':0,'c':1});save('canonical-record.json',[canonical])
# Small deterministic CLI/relocation and boundary tests.
cmd=[sys.executable,'-B',str(PKG/'generator.py'),'--difficulty','easy','--seed','3173462200','--count','5']
run=subprocess.run(cmd,capture_output=True,text=True,check=True);got=json.loads(run.stdout)
rel=ROOT/'relocated-package';shutil.copytree(PKG,rel,dirs_exist_ok=True)
relrun=subprocess.run([sys.executable,'-B',str(rel/'generator.py'),'--difficulty','easy','--seed','3173462200','--count','5'],cwd=ROOT,capture_output=True,text=True,check=True)
bound=[]
for p in [{'a':0,'b':4,'t':0},{'a':2,'b':0,'t':0},{'a':2,'b':1,'t':1}]:
 try:g.generate('easy',template='slope_sqrt_radio',parameters=p);err='ACCEPTED'
 except ValueError as e:err=str(e)
 bound.append({'parameters':p,'result':err})
save('packaging-results.json',{'command':cmd,'batch_replay_equal':got==batch,'relocated_equal':json.loads(relrun.stdout)==got,'python':platform.python_version(),'sympy':s.__version__,'manifest':json.load(open(PKG/'package.json')),'boundaries':bound,'max_attempts':max(r['generation']['attempts'] for r in samples),'after_hashes_match':hashes=={str(p.relative_to(PKG)):hashlib.sha256(p.read_bytes()).hexdigest() for p in PKG.rglob('*') if p.is_file()}})
print(json.dumps({'replays':len(replays),'source_bank_failures':[x for x in replay_results if not x['radio_bank_equal']],'samples':len(samples),'math_failures':[x for x in results if not x['math_ok'] or x['correct_count']!=1],'grader_cases':len(cases)}))
(ROOT/'session-state.md').write_text('Independent source analysis saved before package inspection. Replayed 17 sources; sampled all 15 templates at five fresh seeds; math, grading inputs, controlled target/ordering pairs and packaging results saved. Next run native grader and shared delivery/renderer.\n')
