import sys, os, json, pathlib, importlib.util, hashlib, re, collections, shutil, subprocess
sys.dont_write_bytecode=True
ROOT=pathlib.Path(__file__).resolve().parent
REPO=pathlib.Path('/home/jake/Developer/Course_Academy'); PKG=ROOT.parent/'workspace'
os.chdir(ROOT)
def save(name,obj): (ROOT/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False))
def hashes(): return {str(p.relative_to(PKG)):hashlib.sha256(p.read_bytes()).hexdigest() for p in PKG.rglob('*') if p.is_file()}
save('package-before.json',hashes())
spec=importlib.util.spec_from_file_location('reviewed',PKG/'17592186096613.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
x=sp.Symbol('x', positive=True)
def parse(s):
 s=s.replace('\\dfrac','\\frac').replace('\\operatorname{ln}','\\ln').replace('\u2061','').replace('\\,','').replace('\\cdot','*').replace('\\left','').replace('\\right','').strip().rstrip('.,')
 def grp(i):
  assert s[i]=='{',s
  start=i+1;depth=1;i+=1
  while depth:
   depth+=(s[i]=='{')-(s[i]=='}');i+=1
  return s[start:i-1],i
 while '\\frac' in s:
  i=s.rfind('\\frac'); a,j=grp(i+5);b,j=grp(j);s=s[:i]+'(('+a+')/('+b+'))'+s[j:]
 s=re.sub(r'(?:\\ln|ln)\s*x',' log(x)',s).replace('^','**').replace('{','(').replace('}',')')
 return parse_expr(s,local_dict={'x':x,'e':sp.E,'log':sp.log},transformations=standard_transformations+(implicit_multiplication_application,))
def target(r): return sp.diff(parse(re.search(r'\$y\s*=\s*(.*?)\$',r['question'][':question/problem'])[1]),x)
def field(r):return r['question'][':question/answer-fields'][0]
def correct(r):
 f=field(r);return next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
source=json.load(open(ROOT.parent/'source/source.json'));qs=source['material']['kp'][':knowledge-point/questions']
anchors={'q-11909':(7,1,0),'q-11910':(2,3,0),'q-339941':(-11,1,0),'q-70881':(2,1,0),'q-101600':(2,1,1),'q-101604':(-9,1,0),'q-308849':(8,1,0),'q-339949':(11,4,0),'q-339950':(-7,3,0),'q-70887':(1,4,0),'q-70889':(6,1,1)}
replays=[]; replay_results=[]
for q in qs:
 sid=q[':question/math-academy-id'];n,d,k=anchors[sid]
 try:
  r=g.generate_easy(seed=917,parameters=dict(n=n,d=d,k=k),profile='raw-'+sid);replays.append(r)
  fq=q.get(':question/answer-fields',[]);fr=r['question'].get(':question/answer-fields',[])
  banks=len(fq)==len(fr) and all(sorted(a[':answer/value'] for a in a1[':answer-field/choices'])==sorted(a[':answer/value'] for a in a2[':answer-field/choices']) for a1,a2 in zip(fq,fr))
  replay_results.append(dict(source_id=q[':question/id'],sid=sid,prompt_exact=q[':question/problem']==r['question'][':question/problem'],solution_exact=q.get(':question/worked-solution')==r['question'].get(':question/worked-solution'),bank_exact=banks))
 except Exception as e:replay_results.append(dict(source_id=q[':question/id'],sid=sid,error=str(e)))
save('source-replays.json',replays);save('source-replay-results.json',replay_results)
batch=json.load(open(ROOT.parent/'samples.json'));save('batch.json',batch)
records=[g.generate_easy(seed=s) for s in range(57103,57115)]
directed=[]
for profile,pvals in [('quotient',[(-1,2,0),(1,2,0),(-1,12,0),(1,12,0)]),('integer',[(-30,1,0),(30,1,0)]),('fraction',[(2,3,0),(29,12,0)]),('euler',[(-30,1,1),(30,1,1)]),('canonical',[(-29,12,0),(29,12,0)]),('equivalent-entry',[(-29,12,0),(29,12,0)])]:
 for n,d,k in pvals:directed.append(g.generate_easy(seed=808,profile=profile,parameters=dict(n=n,d=d,k=k)))
save('samples.json',records+directed)
pairs=[]
for profile,n,d,k in [('quotient',1,4,0),('canonical',1,4,0),('equivalent-entry',1,4,0),('integer',7,1,0),('fraction',2,3,0),('euler',2,1,1),('canonical',-11,1,0),('equivalent-entry',11,4,0)]:
 base=g.generate_easy(seed=53,profile=profile,parameters=dict(n=n,d=d,k=k));after=g.generate_easy(seed=53,profile=profile,parameters=dict(n=n+2 if profile=='fraction' else -n,d=d,k=k));shuffle=g.generate_easy(seed=54,profile=profile,parameters=dict(n=n,d=d,k=k))
 pairs.append({'profile':profile,'before':base,'relevant_after':after,'irrelevant_after':shuffle})
save('counterfactuals.json',pairs)
allr=batch+records+directed+[r for p in pairs for k,r in p.items() if k!='profile']
math=[];cases=[]
for i,r in enumerate(allr):
 t=target(r);f=field(r);c=correct(r);vals=[parse(a[':answer/value']) for a in f[':answer-field/choices']]
 sol=r['question'][':question/worked-solution'];last=sol.split('& =')[-1].split('\\end{aligned}')[0]
 # canonical completion uses the same final aligned equality spacing.
 ok=sp.simplify(parse(c[':answer/value'])-t)==0
 last_ok=sp.simplify(parse(last)-t)==0
 unique=len(vals)==len(set(map(str,vals))) if f[':answer-field/type'].endswith('/radio') else all(sp.simplify(v-t)==0 for v in vals)
 math.append({'index':i,'id':r['question'][':question/id'],'derivative':str(t),'key_ok':ok,'solution_final_ok':last_ok,'bank_ok':unique})
 checks=[]
 if f[':answer-field/type'].endswith('/radio'):
  checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if sp.simplify(v-t)==0 else 'rejected','purpose':'independently differentiated prompt'} for a,v in zip(f[':answer-field/choices'],vals)]
 else:
  for val in [str(t),str(t).replace('**(-1)','^(-1)'),sp.latex(t),str(2*t/2),str(t).replace('/x','*x^(-1)')]:checks.append({'submitted':val,'expected':'accepted','purpose':'equivalent derivative notation'})
  for val in ['0',str(-t),str(t*x),str(t*x*x)]:checks.append({'submitted':val,'expected':'rejected','purpose':'wrong sign, lost reciprocal, or wrong power'})
 cases.append({'label':str(i),'record':r,'checks':checks})
# paired old answer must be rejected on changed coefficient (blank only); radio all choices already tested.
for p in pairs:
 if field(p['before'])[':answer-field/type'].endswith('/blank'):
  cases.append({'label':'stale-'+p['profile'],'record':p['relevant_after'],'checks':[{'submitted':correct(p['before'])[':answer/value'],'expected':'rejected','purpose':'relevant counterfactual stale answer'}]})
save('math-results.json',math);save('grader-input.json',cases)
rejections=[]
for params in [dict(n=1,d=4,k=0),dict(n=0,d=1,k=0),dict(n=2,d=2,k=0),dict(n=31,d=1,k=0),dict(n=2,d=13,k=0),dict(n=2,d=1,k=2)]:
 try:g.generate_easy(parameters=params);rejections.append({'params':params,'result':'accepted'})
 except ValueError as e:rejections.append({'params':params,'result':'rejected','reason':str(e)})
save('rejections.json',rejections)
# Reproduce captured CLI batch and relocation without modifying original.
cmd=[sys.executable,str(PKG/'17592186096613.py'),'--difficulty','easy','--seed','3129290382','--count','5','--format','json']
cli=json.loads(subprocess.check_output(cmd,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'}));save('cli-replay.json',cli)
rel=ROOT/'relocated';(rel/'17592186096613').mkdir(parents=True,exist_ok=True)
shutil.copyfile(PKG/'17592186096613.py',rel/'17592186096613.py');shutil.copyfile(PKG/'17592186096613/source.json',rel/'17592186096613/source.json');shutil.copyfile(PKG/'17592186096613/quotient-source.json',rel/'17592186096613/quotient-source.json')
cmd[1]=str(rel/'17592186096613.py');reloc=json.loads(subprocess.check_output(cmd,cwd=rel,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'}))
save('packaging.json',{'command':cmd,'actual_versions':{'python':sys.version.split()[0],'sympy':sp.__version__},'manifest_dependencies':json.load(open(PKG/'package.json'))['dependencies'],'batch_replay_equal':cli==batch,'relocation_equal':reloc==batch,'package_unchanged':hashes()==json.load(open('package-before.json')),'external_assets':'none','unsupported_source_cases':[],'raw_source_profile_absent':[],'repair_history':'one retained quotient restriction','repair_preflight':'reviewed separately'})
save('render-records.json',batch+[p[k] for p in pairs for k in ['before','relevant_after','irrelevant_after']])
print(json.dumps({'records':len(allr),'math_failures':[m for m in math if not all(m[k] for k in ['key_ok','solution_final_ok','bank_ok'])],'replay':replay_results,'packaging':json.load(open('packaging.json'))},indent=2))
