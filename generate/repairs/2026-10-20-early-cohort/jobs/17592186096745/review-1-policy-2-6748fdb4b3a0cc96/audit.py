import json,sys,re,hashlib,copy,subprocess,shutil,platform
from pathlib import Path
import sympy as S
ROOT=Path(__file__).resolve().parent
PKG=ROOT.parent/'workspace'
REPO=Path('/home/jake/Developer/Course_Academy')
sys.dont_write_bytecode=True
sys.path.insert(0,str(PKG))
import generator as g

def save(name,v): (ROOT/name).write_text(json.dumps(v,indent=2,default=str)+'\n')
def load(p): return json.loads(Path(p).read_text())
def hashes(p): return {f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in p.iterdir() if f.is_file()}
save('package-hashes-before.json',hashes(PKG))
src=load(ROOT/'source-extract.json')
x,y,z=S.symbols('x y z')
def expr(t):
 t=t.strip().replace('−','-')
 t=re.sub(r'\\frac\{(-?\d+)\}\{(-?\d+)\}',r'(\1/\2)',t)
 t=re.sub(r'(\d)\s*([xyz])',r'\1*\2',t)
 return S.sympify(t,locals={'x':x,'y':y,'z':z})
def prompt(q):
 t=q[':question/problem'].split(r'\begin{aligned}')[1].split(r'\end{aligned}')[0]
 out=[]
 for line in t.split('\\\\'):
  a,b=line.replace('&','').split('='); a=expr(a);out.append([a.coeff(v) for v in (x,y,z)]+[expr(b)])
 return S.Matrix(out)
def matrices(t):
 if r'\\begin' in t:t=t.replace('\\\\','\\')
 pat=r'\\begin\{(?:bmatrix|array)\}(?:\{[^}]*\})?(.*?)\\end\{(?:bmatrix|array)\}'
 return [S.Matrix([[expr(v) for v in row.split('&')] for row in body.split('\\\\')]) for body in re.findall(pat,t,re.S)]
def semantic(t):
 if t=='No solution':return t
 return str(matrices(t)[0].tolist())
def correct_index(q):
 f=q[':question/answer-fields'][0]; k=f[':answer-field/correct'];k=k[':answer/id'] if isinstance(k,dict) else k[1]
 return next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==k)
def check(r):
 q=r['question'];m=prompt(q);red,piv=m.rref();f=q[':question/answer-fields'][0]; hits=[]
 for a in f[':answer-field/choices']:
  t=a[':answer/value']
  if t=='No solution':hits.append(False);continue
  v=matrices(t)[0]
  hits.append(v==red if v.shape==(3,4) else v.shape==(3,1) and m[:,:3]*v==m[:,3] and v[2]==z)
 states=[a for a in matrices(q[':question/worked-solution']) if a.shape==(3,4)]
 errs=[]
 if piv!=(0,1):errs.append('pivot/rank')
 if sum(hits)!=1 or not hits[correct_index(q)]:errs.append('bank/key')
 if not states or states[0]!=m or states[-1]!=red or any(a.rref()[0]!=red for a in states):errs.append('solution matrices')
 # Inspect the actual displayed operation labels, not metadata or generator trace.
 ops=re.findall(r'(R_\{\d\}(?:\\leftrightarrow R_\{\d\}|:=.*?))\\qquad M\\sim',q[':question/worked-solution'])
 if ops:
  states=[a for j,a in enumerate(states) if j==0 or a!=states[j-1]]
  if len(ops)!=len(states)-1:errs.append('trace count')
  for before,after,op in zip(states,states[1:],ops):
   b=before.copy();i=int(re.search(r'R_\{(\d)\}',op)[1])-1
   if 'leftrightarrow' in op:b.row_swap(i,int(re.findall(r'R_\{(\d)\}',op)[1])-1)
   else:
    k=expr(re.search(r'\\left\((.*?)\\right\)',op)[1])
    if ':=R_' in op:b[i,:]=b[i,:]+k*b[int(re.findall(r'R_\{(\d)\}',op)[-1])-1,:]
    else:b[i,:]=k*b[i,:]
   if b!=after:errs.append('operation '+op)
 return {'id':q[':question/id'],'template':r['generation'].get('template'),'index':correct_index(q),'matrix':m.tolist(),'rref':red.tolist(),'errors':errs,'vector': 'and then solve' in q[':question/problem']}
replays=[]; replay_results=[]
for q in src['questions']:
 profile=q[':question/math-academy-id']
 try:
  r=g.generate(template=profile,replay=True);replays.append(r)
  f=q[':question/answer-fields'][0];rf=r['question'][':question/answer-fields'][0]
  banks=[semantic(a[':answer/value']) for a in f[':answer-field/choices']]==[semantic(a[':answer/value']) for a in rf[':answer-field/choices']]
  replay_results.append({'source_id':q[':question/id'],'template':profile,'passed':banks and prompt(q)==prompt(r['question']) and correct_index(q)==correct_index(r['question']),'bank_match':banks,'math':check(r)})
 except Exception as e: replay_results.append({'source_id':q[':question/id'],'template':profile,'passed':False,'exception':repr(e)})
save('replays.json',replays);save('source-replay-results.json',replay_results)
records=[g.generate(seed=seed+1000003*j,template=p) for j,p in enumerate(g.PROFILES) for seed in ((552319,993701,2857291) if p in ('q-74625','q-131634') else (552319,))]
save('independent-samples.json',records)
batch=load(ROOT.parent/'samples.json');save('runner-batch.json',batch)
# Explicit corners, correct target changes within the same bank, and solution-preserving row changes.
p={'candidates':[[-3,3,-4,4],[3,-3,4,-4],[0,0,0,0],[0,2,0,-4],[1,0,4,0]],'correct_index':0,'row_order':[0,1,2],'row_signs':[1,1,1]}
pairs=[]
for t in ('q-74525','q-74532','q-74625','q-131634'):
 for label,param in [('base',p),('relevant',dict(p,correct_index=1)),('irrelevant',dict(p,row_order=[2,0,1],row_signs=[-1,1,-1]))]:
  r=g.generate(seed=96745,template=t,parameters=param);r['review_case']=label;pairs.append(r)
save('counterfactual-records.json',pairs)
results=[check(r) for r in replays+records+batch+pairs];save('math-results.json',{'command':f'{sys.executable} audit.py','cases':results,'failures':[r for r in results if r['errors']]})
cf=[]
for j in (0,3,6,9):
 b,r,i=pairs[j:j+3];cf.append({'template':b['generation']['template'],'relevant_answer_changes':semantic(b['question'][':question/answer-fields'][0][':answer-field/choices'][0][':answer/value'])!=semantic(r['question'][':question/answer-fields'][0][':answer-field/choices'][1][':answer/value']),'relevant_prompt_changes':b['question'][':question/problem']!=r['question'][':question/problem'],'irrelevant_rref_preserved':prompt(b['question']).rref()[0]==prompt(i['question']).rref()[0],'irrelevant_correct_value_preserved':correct_index(b['question'])==correct_index(i['question']),'math_errors':[check(a)['errors'] for a in (b,r,i)]})
save('counterfactual-results.json',cf)
invalid=[]
for name,kw in [('wrong difficulty',{'difficulty':'easy'}),('duplicate bank',{'parameters':dict(p,candidates=[p['candidates'][0]]*5)}),('slope boundary',{'parameters':dict(p,candidates=[[4,0,0,0]]+p['candidates'][1:])}),('intercept boundary',{'parameters':dict(p,candidates=[[0,0,5,0]]+p['candidates'][1:])}),('invalid target',{'parameters':dict(p,correct_index=5)}),('invalid order',{'parameters':dict(p,row_order=[0,0,1])}),('invalid sign',{'parameters':dict(p,row_signs=[0,1,1])})]:
 try:g.generate(template='q-74525',**kw);invalid.append({'case':name,'rejected':False})
 except Exception as e:invalid.append({'case':name,'rejected':True,'exception':repr(e)})
save('generator-rejection.json',invalid)
# One native invocation will cover every choice, including controlled changed targets.
cases=[]
for r in replays+records+batch+pairs:
 q=r['question'];f=q[':question/answer-fields'][0];idx=correct_index(q)
 cases.append({'label':q[':question/id']+':'+r.get('review_case',''),'record':r,'checks':[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if j==idx else 'rejected','purpose':'independently computed rank-two RREF / affine solution'} for j,a in enumerate(f[':answer-field/choices'])]})
save('grader-input.json',cases)
save('render-input.json',batch+pairs[6:]+[pairs[0],pairs[3]])
# Relocate the exact package without importing or writing into the original package.
rel=ROOT/'relocated';rel.mkdir(exist_ok=True)
for f in PKG.iterdir():
 if f.is_file():shutil.copyfile(f,rel/f.name)
cmd=[sys.executable,str(PKG/'generator.py'),'--count','5','--seed','718993']
a=subprocess.check_output(cmd,env={**__import__('os').environ,'PYTHONDONTWRITEBYTECODE':'1'})
b=subprocess.check_output(cmd,env={**__import__('os').environ,'PYTHONDONTWRITEBYTECODE':'1'})
c=subprocess.check_output([sys.executable,str(rel/'generator.py'),'--count','5','--seed','718993'],cwd=ROOT,env={**__import__('os').environ,'PYTHONDONTWRITEBYTECODE':'1'})
save('relocation-samples.json',json.loads(c))
save('packaging-results.json',{'command':cmd,'python':platform.python_version(),'packages':{'sympy':S.__version__},'deterministic_replay':a==b,'relocation_identical':a==c,'package_unchanged':hashes(PKG)==load(ROOT/'package-hashes-before.json'),'manifest':load(PKG/'package.json'),'stdout_is_json':True,'external_outputs':'No files emitted by generator; source-data path anchored to __file__. No image assets.'})
print(json.dumps({'replays':len(replays),'replay_failures':[x for x in replay_results if not x['passed']],'math_cases':len(results),'math_failures':sum(bool(r['errors']) for r in results),'independent':len(records),'pairs':len(pairs),'invalid_cases':len(invalid)},default=str))
