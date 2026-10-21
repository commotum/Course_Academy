import sys,os,json,re,hashlib,importlib.util,random,subprocess,shutil,platform
from pathlib import Path
from collections import Counter,defaultdict
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parent
JOB=ROOT.parent
REPO=Path('/home/jake/Developer/Course_Academy')
PKG=JOB/'workspace'
sys.path.insert(0,str(PKG))
import generator as g

def save(n,v): (ROOT/n).write_text(json.dumps(v,indent=2)+'\n')
def enum(v):return v.get(':db/ident') if isinstance(v,dict) else v
def ms(text):
 return [[[int(x.strip()) for x in row.split('&')] for row in body.split(r'\\')] for body in re.findall(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',text,re.S)]
def ref(m):
 # Independent direct search of nonzero cells, then all pairwise row comparisons.
 leading=[min([j for j,x in enumerate(row) if x] or [len(row)]) for row in m]
 width=len(m[0]); valid=all(a<b or a==b==width for a,b in zip(leading,leading[1:]))
 return valid,leading

def value(f):
 c=f[':answer-field/correct'];id=c[1] if isinstance(c,list) else c[':answer/id']
 return next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==id)
def examine(r):
 q=r['question']; neg='**not**' in q[':question/problem']; rows=[];errors=[]
 sm=ms(q[':question/worked-solution'])
 fields=q[':question/answer-fields']
 for f in fields:
  m=ms(f[':answer-field/key'])[0]; label=re.search(r'\$([ABC])\s*=',f[':answer-field/key'])[1]
  valid,pivots=ref(m);expected=valid!=neg
  if value(f)!=str(expected).lower():errors.append(label+' key mismatch')
  if sm['ABC'.index(label)]!=m:errors.append(label+' solution matrix mismatch')
  status=f'- The matrix ${label}$ is '+('in' if valid else 'not in')+' row echelon form'
  if status not in q[':question/worked-solution']:errors.append(label+' solution classification mismatch')
  rows.append({'label':label,'shape':[len(m),len(m[0])],'pivots':pivots,'valid':valid,'selected':expected})
 return {'id':q[':question/id'],'profile':r['generation']['profile'],'negate':neg,'selected':''.join(x['label'] for x in sorted(rows,key=lambda x:x['label']) if x['selected']),'rows':rows,'errors':errors}

source=json.load(open(JOB/'source/source.json'))['material']['kp']
sourceq={q[':question/math-academy-id']:q for q in source[':knowledge-point/questions']}
manifest=json.load(open(PKG/'package.json'))
hashes={str(p.relative_to(PKG)):hashlib.sha256(p.read_bytes()).hexdigest() for p in PKG.rglob('*') if p.is_file()}
save('package-before.json',hashes)
replays=[];replay_results=[]
for profile in g.PROFILES:
 # Extract original matrices independently, not through generator original().
 old=sourceq[profile]; maps={re.search(r'\$([ABC])\s*=',f[':answer-field/key'])[1]:ms(f[':answer-field/key'])[0] for f in old[':question/answer-fields']}
 r=g.generate('easy',73021,profile=profile,parameters={'matrices':[maps[x] for x in 'ABC']},replay=True)
 replays.append(r)
 checks={'profile':profile,'source_id':old[':question/id'],'problem':r['question'][':question/problem']==old[':question/problem'],'banks':[],'mathematics':examine(r)}
 for a,b in zip(old[':question/answer-fields'],r['question'][':question/answer-fields']):
  checks['banks'].append({'key_equal':a[':answer-field/key']==b[':answer-field/key'],'types_equal':enum(a[':answer-field/type'])==enum(b[':answer-field/type']),'bank_equal':[x[':answer/value'] for x in a[':answer-field/choices']]==[x[':answer/value'] for x in b[':answer-field/choices']],'correct_equal':a[':answer-field/correct'][':answer/value']==value(b)})
 # Corrections independently approved in source analysis.
 checks['solution_equal_or_documented_correction']=r['question'][':question/worked-solution']==old[':question/worked-solution'] or profile in ('q-129225','q-42366')
 replay_results.append(checks)
save('source-replays.json',replays);save('source-replay-results.json',replay_results)
records=[]
for p in g.PROFILES:
 for seed in range(81731,81763):records.append(g.generate('easy',seed,profile=p))
save('independent-samples.json',records)
batch=json.load(open(JOB/'samples.json'));save('runner-batch.json',batch)
metrics=[examine(r) for r in records]; bm=[examine(r) for r in batch]
save('math-results.json',{'command':'PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python audit.py','samples':metrics,'batch':bm,'errors':sum((r['errors'] for r in metrics+bm),[])})
# Small fresh normal batch exercises semantic rejection; compare exact replay.
stats={};normal=g.batch('easy',64,920113,stats=stats);save('normal-batch.json',normal)
raw=[g.generate.__wrapped__.__wrapped__('easy',seed) for seed in range(920113,920177)]
save('pre-policy-samples.json',raw)
save('sampling-results.json',{'profiles':list(g.PROFILES),'per_profile':{p:dict(Counter(m['selected'] for m in metrics if m['profile']==p)) for p in g.PROFILES},'normal_batch':stats,'selected_before_nonempty_policy':dict(Counter(examine(r)['selected'] for r in raw)),'selected_after_rejection':dict(Counter(examine(r)['selected'] for r in normal)),'deterministic_replay':normal==g.batch('easy',64,920113)})
# Controlled relevant change: move one row's leading entry left into previous pivot column.
p='q-129214';base=[[[1,2,3,4],[0,2,3,4],[0,0,3,4],[0,0,0,4],[0,0,0,0]],[[1,2,3,4],[0,2,3,4],[0,0,3,4],[0,0,0,0]],[[1,2,3,4],[0,2,3,4],[0,0,3,4]]]
from copy import deepcopy
relevant=deepcopy(base);relevant[0][1][0]=7
irrelevant=deepcopy(base);irrelevant[0][0][-1]=-9
cf=[g.generate('easy',431,profile=p,parameters={'matrices':m}) for m in (base,relevant,irrelevant)]
# Polarity pair uses same dimensions and all other evidence; source profiles identical 3x4,3x4,3x6.
polms=[[[1,2,3,4],[0,2,3,4],[0,0,0,0]],[[1,2,3,4],[0,0,0,0],[0,2,3,4]],[[1,2,3,4,5,6],[0,2,3,4,5,6],[0,0,3,4,5,6]]]
# q-42024 only has this shape profile, so polarity is not explicit independent target slot.
save('counterfactual-records.json',cf);save('counterfactual-results.json',{'changes':['base','A[2,1]: 0 -> 7','A[1,4]: 4 -> -9'],'results':[examine(r) for r in cf],'expected_selected':['ABC','BC','ABC']})
# Every possible selection for a fixed recognizable profile, nonempty only; preserve shape.
decisions=[]; rejected=[]
for bits in range(8):
 m=deepcopy(base)
 for k in range(3):
  if not (bits>>k)&1:m[k][1][0]=7
 try: decisions.append(g.generate('easy',432,profile=p,parameters={'matrices':m}))
 except Exception as e: rejected.append({'selected_bits':bits,'error':type(e).__name__+': '+str(e)})
save('decision-records.json',decisions);save('decision-results.json',{'selected':[examine(r)['selected'] for r in decisions],'rejections':rejected})
# Invalid and boundary calls.
rejects=[]
for label,fn in [('unsupported difficulty',lambda:g.batch('hard',1,99)),('negative count',lambda:g.batch('easy',-1,99)),('excess count',lambda:g.batch('easy',1001,99)),('unsupported profile',lambda:g.generate('easy',99,profile='q-42369')),('shape mismatch',lambda:g.generate('easy',99,profile=p,parameters={'matrices':[[[1]],[[1]],[[1]]]}))]:
 try:fn();rejects.append({'case':label,'rejected':False})
 except Exception as e:rejects.append({'case':label,'rejected':True,'error':str(e)})
rel=ROOT/'relocated';rel.mkdir(exist_ok=True)
for name in manifest['files']+['package.json']:shutil.copyfile(PKG/name,rel/name)
cmd=[sys.executable,str(rel/'generator.py'),'--difficulty','easy','--count','5','--seed','802139']
x=subprocess.run(cmd,cwd='/tmp',capture_output=True,text=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
save('relocation-records.json',json.loads(x.stdout))
save('packaging-results.json',{'python':platform.python_version(),'declared_dependencies':manifest['dependencies'],'relocation_command':cmd,'relocation_exit':x.returncode,'relocation_stderr':x.stderr,'relocation_equal':json.loads(x.stdout)==g.batch('easy',5,802139),'zero_count':g.batch('easy',0,99),'rejections':rejects,'package_unchanged':hashes=={str(p.relative_to(PKG)):hashlib.sha256(p.read_bytes()).hexdigest() for p in PKG.rglob('*') if p.is_file()}})
# Native grader: test both choices for every field of source, runner, boundary and counterfactual records.
grade=[]
for i,r in enumerate(replays+batch+cf+decisions):
 checks=[]
 for j,f in enumerate(r['question'][':question/answer-fields']):
  expected=ref(ms(f[':answer-field/key'])[0])[0]!=('**not**' in r['question'][':question/problem'])
  for a in f[':answer-field/choices']:
   checks.append({'field_index':j,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/value']==str(expected).lower() else 'rejected','purpose':'independent row echelon classification; both checkbox states'})
 grade.append({'label':f'independent-{i}','record':r,'checks':checks})
save('grader-input.json',grade)
save('render-records.json',batch+cf+[replays[4],replays[10]])
print(json.dumps({'replays':len(replays),'independent':len(records),'math_errors':sum(len(x['errors']) for x in metrics+bm),'batch_selected':[x['selected'] for x in bm],'replay_mismatches':[x['profile'] for x in replay_results if not all(v for b in x['banks'] for v in b.values()) or not x['solution_equal_or_documented_correction']],'packaging':json.load(open(ROOT/'packaging-results.json')),'normal_batch':stats},indent=2))
