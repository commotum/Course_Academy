import os,sys,json,re,hashlib,platform,importlib.util,shutil,subprocess
from pathlib import Path
import sympy as s
E=Path(__file__).resolve().parent
B=E.parent; P=B/'workspace'; R=Path('/home/jake/Developer/Course_Academy')
os.environ['PYTHONDONTWRITEBYTECODE']='1';sys.dont_write_bytecode=True
sys.path.insert(0,str(P));import generator as g

def save(name,x): (E/name).write_text(json.dumps(x,indent=2)+'\n')
def digest():return {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in P.iterdir() if p.is_file()}
def enum(x):return x.get(':db/ident') if isinstance(x,dict) else x
def num(t):
 t=re.sub(r'\\frac\{(-?\d+)\}\{(-?\d+)\}',r'((\1)/(\2))',t.strip());return s.sympify(t)
MP=re.compile(r'\\begin\{(?:bmatrix|array)\}(?:\{ccc\|c\})?(.*?)\\end\{(?:bmatrix|array)\}',re.S)
def mats(text):
 return [s.Matrix([[num(v) for v in row.split('&')] for row in m[1].split(r'\\')]) for m in MP.finditer(text)]
def vec(text):
 ms=mats(text)
 if ms:return ms[0][:,3]
 text=text.replace(r'\langle','⟨').replace(r'\rangle','⟩').strip()
 return s.Matrix([num(v) for v in text[1:-1].split(',')])
def parse_problem(text):
 body=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',text,re.S)[1]
 vs=s.symbols('x y z'); rows=[]
 for row in body.split(r'\\'):
  lhs,rhs=row.replace('&','').split('=');expr=s.sympify(lhs.replace(' ','').replace('x','*x').replace('y','*y').replace('z','*z').lstrip('*').replace('+*','+').replace('-*','-'))
  rows.append([expr.coeff(v) for v in vs]+[num(rhs)])
 return s.Matrix(rows)
def correct(q):
 f=q[':question/answer-fields'][0];c=f[':answer-field/correct'];cid=c[':answer/id'] if isinstance(c,dict) else c[1]
 return next(a for a in f[':answer-field/choices'] if a[':answer/id']==cid)
def row_ops(work):
 matches=list(MP.finditer(work)); stages=mats(work);results=[]
 for i in range(1,len(stages)-1):
  # matrices 0 and 1 repeat augmented system; each following matrix follows a displayed operation.
  tail=work[matches[i].end():matches[i+1].start()];a,b=stages[i],stages[i+1]
  rr=re.sub(r'\{R\}_\{(\d)\}',r'R\1',tail)
  rr=rr.replace('\\right]','').replace('\\left','').strip()
  swap=re.search(r'R([123])\s*(?:&\s*)?(?:↔|\\leftrightarrow)\s*R([123])',rr)
  assign=re.search(r'R([123])\s*&\s*:=\s*(.*?)(?:\\\\|$)',rr,re.S)
  if swap:
   expected=a.copy();expected.row_swap(int(swap[1])-1,int(swap[2])-1)
  elif assign:
   ix=int(assign[1])-1;ex=assign[2].strip().replace(r'\left','').replace(r'\right','')
   ex=re.sub(r'\\frac\{(-?\d+)\}\{(-?\d+)\}',r'((\1)/(\2))',ex)
   ex=re.sub(r'(\d|\))(?=R)',r'\1*',ex)
   v=s.symbols('R1 R2 R3');pol=s.sympify(ex,locals=dict(zip(['R1','R2','R3'],v)))
   expected=a.copy();new=s.zeros(1,4)
   for j,x in enumerate(v):new+=pol.coeff(x)*a[j,:]
   expected[ix,:]=new
  else:results.append({'step':i,'ok':False,'unparsed':rr});continue
  results.append({'step':i,'ok':expected==b,'operation':rr})
 return results

def check(r):
 q=r['question'];a=parse_problem(q[':question/problem']);ms=mats(q[':question/worked-solution']);f=q[':question/answer-fields'][0];v=vec(correct(q)[':answer/value']);rr=a.rref()[0]; ops=row_ops(q[':question/worked-solution'])
 errors=[]
 if a!=ms[0]:errors.append('prompt/initial matrix mismatch')
 if rr!=ms[-1]:errors.append('wrong final RREF')
 if a[:,:3].det()==0:errors.append('singular')
 if rr[:,3]!=v:errors.append('wrong answer key')
 if len(set(str(vec(x[':answer/value'])) for x in f[':answer-field/choices']))!=5:errors.append('bank collision')
 for i,m in enumerate(ms):
  if m[:, :3]*v!=m[:,3] or m.rref()[0]!=rr:errors.append('invalid stage '+str(i))
 for o in ops:
  if not o['ok']:errors.append('row operation '+str(o))
 return {'question_id':q[':question/id'],'template':r['generation']['template'],'seed':r['generation']['seed'],'errors':errors,'row_operations':len(ops),'solution':list(map(str,v)),'rhs':list(map(str,a[:,3]))}

if __name__=='__main__':
 before=digest();save('package-before.json',before)
 src=json.load(open(B/'source/source.json'));qs=src['material']['kp'][':knowledge-point/questions'];replays=[];replay_report=[]
 for q in qs:
  mid=q[':question/math-academy-id'];r=g.generate(seed=41021,template=mid,replay=True);replays.append(r)
  orig=q[':question/answer-fields'][0];rf=r['question'][':question/answer-fields'][0]
  source_vs=[vec(c[':answer/value']) for c in orig[':answer-field/choices']];new_vs=[vec(c[':answer/value']) for c in rf[':answer-field/choices']]
  replay_report.append({'source_id':q[':question/id'],'template':mid,'same_equations':parse_problem(q[':question/problem'])==parse_problem(r['question'][':question/problem']),'complete_ordered_bank':source_vs==new_vs,'same_correct':vec(correct(q)[':answer/value'])==vec(correct(r['question'])[':answer/value']),'same_stage_matrices':mats(q[':question/worked-solution'])==mats(r['question'][':question/worked-solution']),'prompt_exact':q[':question/problem']==r['question'][':question/problem'],'checks':check(r)})
 save('replays.json',replays);save('source-replay-results.json',replay_report)
 independent=[];pairs=[];counter=[]
 for i,q in enumerate(qs):
  mid=q[':question/math-academy-id']
  for role in range(5):
   t=[-3,0,3] if role%2 else [3,-3,0]
   independent.append(g.generate(seed=730001+i*101+role,template=mid,parameters={'answer_role':role,'translation':t}))
  base=g.generate(seed=581031+i,template=mid,parameters={'answer_role':0,'translation':[0,0,0]})
  changed=g.generate(seed=581031+i,template=mid,parameters={'answer_role':1,'translation':[0,0,0]})
  irrelevant=g.generate(seed=581033+i,template=mid,parameters={'answer_role':0,'translation':[0,0,0]})
  start=len(pairs);pairs += [base,changed,irrelevant]
  counter.append({'template':mid,'record_indices':[start,start+1,start+2],'relevant':'answer_role 0 -> 1: A and unordered full answer bank held fixed; RHS and solution must change','same_A':parse_problem(base['question'][':question/problem'])[:,:3]==parse_problem(changed['question'][':question/problem'])[:,:3],'same_bank':sorted(c[':answer/value'] for c in base['question'][':question/answer-fields'][0][':answer-field/choices'])==sorted(c[':answer/value'] for c in changed['question'][':question/answer-fields'][0][':answer-field/choices']),'changed_prompt':base['question'][':question/problem']!=changed['question'][':question/problem'],'changed_solution':correct(base['question'])[':answer/value']!=correct(changed['question'])[':answer/value'],'irrelevant':'seed-only answer shuffle with all mathematical parameters held fixed','same_prompt_irrelevant':base['question'][':question/problem']==irrelevant['question'][':question/problem'],'same_worked_irrelevant':base['question'][':question/worked-solution']==irrelevant['question'][':question/worked-solution'],'same_correct_id_irrelevant':correct(base['question'])[':answer/id']==correct(irrelevant['question'])[':answer/id']})
 save('independent-samples.json',independent);save('counterfactual-records.json',pairs);save('counterfactual-results.json',counter)
 raw=g.batch(seed=927410,count=42);save('fresh-batch.json',raw)
 runner=json.load(open(B/'samples.json'));save('runner-batch.json',runner)
 results={name:[check(r) for r in records] for name,records in [('independent',independent),('counterfactual',pairs),('fresh_batch',raw),('runner_batch',runner)]};save('math-results.json',results)
 cases=[]
 for name,records in [('replay',replays),('independent',independent),('counterfactual',pairs),('runner_batch',runner)]:
  for i,r in enumerate(records):
   q=r['question'];v=mats(q[':question/worked-solution'])[-1][:,3];checks=[]
   for c in q[':question/answer-fields'][0][':answer-field/choices']:
    checks.append({'submitted_answer_id':c[':answer/id'],'expected':'accepted' if vec(c[':answer/value'])==v else 'rejected','purpose':'independent exact RREF versus each complete radio bank member'})
   cases.append({'label':f'{name}:{i}','record':r,'checks':checks})
 save('grader-input.json',cases)
 render=[runner[0],next(r for r in runner if 'then solve' in r['question'][':question/problem'])]+pairs[:3]+[replays[10]]
 save('render-records.json',render)
 errors={}
 for kw in [{'difficulty':'easy'},{'difficulty':'hard'},{'template':'q-20266','parameters':{'translation':[4,0,0]}},{'template':'q-20266','parameters':{'translation':[0,0]}},{'template':'q-20266','parameters':{'answer_role':5}}]:
  try:g.generate(**kw);out='UNEXPECTED acceptance'
  except Exception as e:out=type(e).__name__+': '+str(e)
  errors[str(kw)]=out
 for n in [0,-1]:
  try:out=g.batch(count=n)
  except Exception as e:out=type(e).__name__+': '+str(e)
  errors['count='+str(n)]=out
 replay_equal=g.generate(seed=800123)==g.generate(seed=800123)
 relocate=E/'relocated-package';relocate.mkdir(exist_ok=True)
 for p in P.iterdir():
  if p.is_file():shutil.copy2(p,relocate/p.name)
 out=E/'relocated-output.json'
 proc=subprocess.run([sys.executable,str(relocate/'generator.py'),'--seed','800123','--count','5','--output',str(out)],cwd=E,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'},capture_output=True,text=True)
 cli_equal=json.load(open(out))==g.batch(seed=800123,count=5) if out.exists() else False
 save('packaging-results.json',{'python':platform.python_version(),'sympy':s.__version__,'manifest':json.load(open(P/'package.json')),'deterministic':replay_equal,'relocation_returncode':proc.returncode,'relocation_stderr':proc.stderr,'relocated_cli_equal':cli_equal,'boundary_tests':errors,'package_unchanged':digest()==before,'notes':'No generated assets or external dependencies beyond declared sympy and local source/math_format. Outputs written only inside evidence_root.'})
 print(json.dumps({'replay':len(replays),'source_replay_failures':[x['template'] for x in replay_report if not all(x[k] for k in ['same_equations','complete_ordered_bank','same_correct','same_stage_matrices'])],'math_counts':{n:len(v) for n,v in results.items()},'math_failures':{n:[x for x in v if x['errors']] for n,v in results.items()},'packaging':json.load(open(E/'packaging-results.json'))}))
