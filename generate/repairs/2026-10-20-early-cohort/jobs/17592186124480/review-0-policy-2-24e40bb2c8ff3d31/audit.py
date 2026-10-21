import sys,os,json,re,random,hashlib,pathlib,subprocess,shutil,itertools
from fractions import Fraction
sys.dont_write_bytecode=True
ROOT=pathlib.Path(__file__).resolve().parent
JOB=ROOT.parent
REPO=pathlib.Path('/home/jake/Developer/Course_Academy')
PKG=JOB/'workspace'
PY=REPO/'.venv/bin/python'
os.environ['PYTHONDONTWRITEBYTECODE']='1'
sys.path.insert(0,str(PKG))
import generator as g

def save(name,x): (ROOT/name).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def hashes(): return {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(PKG.iterdir()) if p.is_file()}
def ident(v):return v.get(':db/ident') if isinstance(v,dict) else v

def matrices(text):
 def num(s):
  s=s.strip();m=re.fullmatch(r'(-?)\\frac\{(\d+)\}\{(\d+)\}',s)
  return Fraction((-1 if m[1] else 1)*int(m[2]),int(m[3])) if m else Fraction(s)
 return [[[num(x) for x in r.split('&')] for r in re.split(r'\\\\',body)] for body in re.findall(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',text,re.S)]
def pivots(a):
 a=[list(map(Fraction,r)) for r in a];row=0;ps=[]
 for j in range(len(a[0])):
  pick=next((i for i in range(row,len(a)) if a[i][j]),None)
  if pick is None:continue
  a[row],a[pick]=a[pick],a[row];p=a[row][j];a[row]=[x/p for x in a[row]]
  for i in range(len(a)):
   if i!=row:
    k=a[i][j];a[i]=[x-k*y for x,y in zip(a[i],a[row])]
  ps.append(j);row+=1
  if row==len(a):break
 return ps

def correct(f):
 ref=f[':answer-field/correct'];aid=ref[':answer/id'] if isinstance(ref,dict) else ref[1]
 return next(c[':answer/value'] for c in f[':answer-field/choices'] if c[':answer/id']==aid)
def selected(r):
 fs=r['question'][':question/answer-fields']
 if ident(fs[0][':answer-field/type']).endswith('/checkbox'):
  return sorted(int(re.search(r'Column (\d+)',f[':answer-field/key'])[1])-1 for f in fs if correct(f)=='true')
 return [int(i)-1 for i in re.findall(r'\$(\d+)\$',correct(fs[0]))]

def check(r):
 q=r['question'];a=matrices(q[':question/problem'])[0];ps=pivots(a);fails=[]
 if selected(r)!=ps:fails.append('incorrect key')
 chain=matrices(q[':question/worked-solution'])
 if chain[0]!=a:fails.append('solution initial matrix differs')
 if any(pivots(v)!=ps for v in chain):fails.append('solution pivot indices change')
 # Every consecutive matrix must match the displayed exact swap/add annotation.
 ann=re.findall(r'(R_\{\d+\}\\leftrightarrow R_\{\d+\}|R_\{\d+\}:=R_\{\d+\}\+.*?)(?= \\\\ )',q[':question/worked-solution'])
 if len(ann)!=len(chain)-1:fails.append('annotation count')
 for before,after,op in zip(chain,chain[1:],ann):
  b=[row[:] for row in before]
  if 'leftrightarrow' in op:
   i,j=map(lambda t:int(t)-1,re.findall(r'R_\{(\d+)\}',op));b[i],b[j]=b[j],b[i]
  else:
   ix=re.findall(r'R_\{(\d+)\}',op);i,j=int(ix[0])-1,int(ix[-1])-1
   coef=op.split('+',1)[1].rsplit('R_',1)[0]
   if coef=='': k=Fraction(1)
   else:
    coef=coef.replace(r'\left','').replace(r'\right','').strip('()');fm=re.fullmatch(r'(-?)\\frac\{(\d+)\}\{(\d+)\}',coef)
    k=Fraction((-1 if fm[1] else 1)*int(fm[2]),int(fm[3])) if fm else Fraction(coef)
   b[i]=[x+k*y for x,y in zip(b[i],b[j])]
  if b!=after:fails.append('incorrect annotated row operation')
 leads=[next((j for j,x in enumerate(row) if x),len(row)) for row in chain[-1]]
 if leads!=sorted(leads) or len(set(j for j in leads if j<len(a[0])))!=len(ps):fails.append('final matrix not REF')
 tail=q[':question/worked-solution'].split('In particular,')[-1]
 if [int(i)-1 for i in re.findall(r'\$(\d+)\$',tail)]!=ps:fails.append('wrong conclusion')
 for f in q[':question/answer-fields']:
  if ident(f[':answer-field/type']).endswith('/checkbox'):
   col=int(re.search(r'Column (\d+)',f[':answer-field/key'])[1])-1
   if matrices(f[':answer-field/key'])[0]!=[[row[col]] for row in a]:fails.append('column vector mismatch')
 return {'id':q[':question/id'],'shape':[len(a),len(a[0])],'pivots':ps,'failures':fails}

save('package-before.json',hashes())
source=json.load(open(JOB/'source/source.json'));inv=json.load(open(JOB/'source/inventory.json'));batch=json.load(open(JOB/'samples.json'));save('runner-batch.json',batch)
original=source['material']['kp'][':knowledge-point/questions'];by_id={q[':question/id']:q for q in original}
replays=[g.replay(c) for c in g.source_cases()];save('source-replays.json',replays)
replay_checks=[]
for c,r in zip(g.source_cases(),replays):
 q=by_id[c['question'][':question/id']];generated=r['question']
 def fields(q):return [(f[':answer-field/key'],ident(f[':answer-field/type']),[a[':answer/value'] for a in f[':answer-field/choices']],correct(f)) for f in q[':question/answer-fields']]
 # Source boolean bank order is incidental UI data; retain complete banks and keyed value.
 before=fields(q);after=fields(generated)
 same=len(before)==len(after) and all(a[:2]==b[:2] and sorted(a[2])==sorted(b[2]) and a[3]==b[3] for a,b in zip(before,after))
 replay_checks.append({'source_id':q[':question/id'],'math_academy_id':c['source_id'],'prompt_equal':q[':question/problem'].strip()==generated[':question/problem'].strip(),'complete_banks_keys_field_order_equal':same,'source_math':pivots(matrices(q[':question/problem'])[0]),'generated':check(r),'source_solution_matrices_equal':matrices(q[':question/worked-solution'])==matrices(generated[':question/worked-solution'])})
canonical=source['material']['kp'][':knowledge-point/canonical-example']; cr=g.build_record([[int(x) for x in row] for row in matrices(canonical[':question/problem'])[0]],'B','hard',source=[canonical[':question/id']],profile='canonical_reconstruction');save('canonical-replay.json',[cr]);save('source-replay-results.json',replay_checks+[{'canonical':canonical[':question/id'],'generated':check(cr),'solution_matrices_equal':matrices(canonical[':question/worked-solution'])==matrices(cr['question'][':question/worked-solution'])}])
moderate=g.generate('moderate',60,928471); hard=[]
for index,profile in enumerate(g.PROFILES['hard']):
 hard.extend(g.sample(random.Random(78210+100*index+j),'hard',seed=78210+100*index+j,profile=profile) for j in range(6))
save('moderate-samples.json',moderate);save('hard-samples.json',hard)
boundaries=[];errors=[]
for band,shapes in g.SHAPES.items():
 for shape in shapes:
  for rank in sorted(set([2,min(shape[0],shape[1]-1)])):
   for ps in [list(range(rank)),list(range(shape[1]-rank,shape[1]))]:
    seed=441000+len(boundaries)
    try:boundaries.append(g.sample(random.Random(seed),band,seed=seed,shape=shape,pivots=ps,profile='checkbox_swap'))
    except Exception as e: errors.append({'band':band,'shape':shape,'pivots':ps,'seed':seed,'error':str(e)})
save('boundaries.json',boundaries);save('boundary-results.json',{'errors':errors,'cases':[check(r) for r in boundaries]})
# Minimal controlled construction, preserving one swap and almost every entry.
base=[[1,2,5],[0,0,0],[0,4,3]]
relevant=[[1,2,5],[0,0,0],[0,0,3]]
irrelevant=[[1,2,-5],[0,0,0],[0,4,3]]
cf=[g.build_record(a,'A','moderate',profile=tag) for a,tag in [(base,'independent_base'),(relevant,'independent_relevant'),(irrelevant,'independent_irrelevant')]]
save('counterfactual-records.json',cf)
save('counterfactual-results.json',{'command':str(PY)+' audit.py','changes':['Row3 column2: 4 -> 0; pivot membership must change from {1,2} to {1,3}.','Row1 column3: 5 -> -5; pivot membership must remain {1,2}.'],'checks':[check(r) for r in cf],'all_are_one_swap':all(len(r['generation']['operations'])==1 for r in cf),'limitation':'Controlled explicit build_record calls test dependency construction, while observed sampler reachability is checked in boundaries and samples.'})
all_records=replays+[cr]+moderate+hard+boundaries+batch+cf
math_results=[check(r) for r in all_records];save('math-results.json',{'cases':math_results,'total':len(math_results),'failures':[v for v in math_results if v['failures']]})
# Test both booleans for every field on every exact batch member, source replay,
# controlled counterfactual and one record per hard profile. No free input exists.
grade_cases=[]
for label,rs in [('batch',batch),('replay',replays),('counterfactual',cf),('hard profiles',hard[::6])]:
 for r in rs:
  checks=[]
  for i,f in enumerate(r['question'][':question/answer-fields']):
   for a in f[':answer-field/choices']:
    checks.append({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/value']==correct(f) else 'rejected','purpose':'independently verified complete selection bank'})
  grade_cases.append({'label':label+' '+r['question'][':question/id'],'record':r,'checks':checks})
save('grader-input.json',grade_cases)
# Runtime/dependency/relocation and invalid public CLI behavior.
copy=ROOT/'relocated';copy.mkdir(exist_ok=True)
for p in PKG.iterdir():
 if p.is_file():shutil.copyfile(p,copy/p.name)
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
commands=[]
for name,path,args in [('original',PKG/'generator.py',['--difficulty','moderate','--seed','674120','--count','5']),('replay',PKG/'generator.py',['--difficulty','moderate','--seed','674120','--count','5']),('relocated',copy/'generator.py',['--difficulty','moderate','--seed','674120','--count','5']),('unsupported',PKG/'generator.py',['--difficulty','easy']),('negative count',PKG/'generator.py',['--count','-1'])]:
 run=subprocess.run([str(PY),str(path)]+args,capture_output=True,text=True,env=env,cwd=ROOT)
 (ROOT/('runtime-'+name.replace(' ','-')+'.txt')).write_text(run.stdout+run.stderr)
 commands.append({'name':name,'command':[str(PY),str(path)]+args,'exit':run.returncode,'stdout_hash':hashlib.sha256(run.stdout.encode()).hexdigest(),'stderr':run.stderr})
save('packaging-results.json',{'python':sys.version.split()[0],'manifest':json.load(open(PKG/'package.json')),'commands':commands,'deterministic_relocated_equal':len({c['stdout_hash'] for c in commands[:3]})==1,'dependencies':'standard library only; no external outputs or assets; package-local imports resolved relative to entrypoint','package_unchanged':hashes()==json.load(open(ROOT/'package-before.json'))})
save('render-records.json',batch+cf+[hard[6],hard[18],hard[24],next(r for r in hard if r['generation']['shape'][1]>=5)])
(ROOT/'session-state.md').write_text('Source account complete. Independent audit.py saved and executed: source replays, exact batch, 60 moderate, 36 hard, boundary assignments, controlled relevant/irrelevant pairs. Grader and renderer inputs saved; pipeline and UI checks pending.\n')
print(json.dumps({'math_cases':len(math_results),'math_failures':[v for v in math_results if v['failures']][:5],'source_replay_mismatches':[v for v in replay_checks if not(v['prompt_equal'] and v['complete_banks_keys_field_order_equal'] and v['source_solution_matrices_equal'])],'boundary_errors':errors,'packaging':json.load(open(ROOT/'packaging-results.json'))['deterministic_relocated_equal']}))
