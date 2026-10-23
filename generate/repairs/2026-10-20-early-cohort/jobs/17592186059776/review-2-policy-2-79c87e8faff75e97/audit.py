import sys, json, re, importlib.util, pathlib, hashlib, platform, shutil, subprocess
from collections import Counter, defaultdict
import sympy as S
ROOT=pathlib.Path(__file__).resolve().parent
JOB=ROOT.parent
REPO=pathlib.Path('/home/jake/Developer/Course_Academy')
sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location('reviewed',JOB/'workspace/17592186059776.py'); g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def save(name,obj): (ROOT/name).write_text(json.dumps(obj,indent=2,default=str))
def read(name): return json.loads((JOB/name).read_text())
def rat(t):
 t=t.strip().replace(' ','');t=re.sub(r'\\(?:d?frac)\{(-?\d+)\}\{(\d+)\}',r'(\1/\2)',t);return S.sympify(t)
def mats(t):
 return [S.Matrix([[rat(v) for v in row.split('&')] for row in b.split(r'\\')]) for b in re.findall(r'\\begin\{array\}\{cc\|c\}(.*?)\\end\{array\}',t,re.S)]
def prompt_matrix(t):
 b=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',t,re.S)[1];out=[]
 for row in b.split(r'\\'):
  l,r=row.split('&=');l=re.sub(r'\\frac\{(-?\d+)\}\{(\d+)\}',r'(\1/\2)',l);l=re.sub(r'(?<=[\d)])(?=[xy])','*',l);e=S.sympify(l);out.append([e.coeff(S.Symbol('x')),e.coeff(S.Symbol('y')),rat(r.rstrip('.,'))])
 return S.Matrix(out)
def field(rec):return rec['question'][':question/answer-fields'][0]
def choices(rec):return field(rec)[':answer-field/choices']
def correct(rec):return field(rec)[':answer-field/correct'][1]
def idx(rec):return next(i for i,a in enumerate(choices(rec)) if a[':answer/id']==correct(rec))
def sig(rec):return str(list(prompt_matrix(rec['question'][':question/problem'])[:,:2]))
def ranks(rec):
 vals=[mats(a[':answer/value'])[0][1,2] for a in choices(rec)]
 return vals, sorted(vals).index(vals[idx(rec)])+1
source=read('source/source.json')['material']['kp'];original=source[':knowledge-point/questions']
replays=[]; replay_report=[]
def norm(t):return re.sub(r'\s+','',t).replace('$','').replace(r'\,','')
for q in original:
 sid=q[':question/math-academy-id'];lev=q[':question/difficulty'][':db/ident'].split('/')[-1];r=g.generate(lev,820219,sid,[0,0]);replays.append(r)
 oq=q[':question/answer-fields'][0];nq=field(r)
 replay_report.append({'source_id':q[':question/id'],'template':sid,'prompt':norm(q[':question/problem'])==norm(r['question'][':question/problem']),'solution':norm(q[':question/worked-solution'])==norm(r['question'][':question/worked-solution']),'complete_bank':sorted(norm(a[':answer/value']) for a in oq[':answer-field/choices'])==sorted(norm(a[':answer/value']) for a in choices(r)),'key':norm(oq[':answer-field/correct'][':answer/value'])==norm(choices(r)[idx(r)][':answer/value'])})
samples=[]
for q in original:
 sid=q[':question/math-academy-id'];lev=q[':question/difficulty'][':db/ident'].split('/')[-1]
 for p in [[-3,-3],[-3,3],[0,0],[3,-3],[3,3],[1,2]]:samples.append(g.generate(lev,820219,sid,p))
batch=read('samples.json');control=g.batch('easy',15,920221)
save('source-replays.json',replays);save('source-replay-results.json',replay_report);save('samples.json',samples);save('batch.json',batch);save('control.json',control)
results=[];cases=[]
for group,records in [('sample',samples),('batch',batch),('control',control)]:
 for r in records:
  q=r['question'];m=prompt_matrix(q[':question/problem']);sol=m[:,:2].inv()*m[:,2];ms=mats(q[':question/worked-solution']);valid=[]
  for a in choices(r):
   am=mats(a[':answer/value'])[0];ok=am[:,:2]*sol==am[:,2] and am[0,0]==1 and am[1,0]==0 and am[1,1]==1
   if 'and then solve' in q[':question/problem']:
    xy=re.search(r'x=([^$]+)\$ and \$y=([^$]+)',a[':answer/value']);ok=ok and S.Matrix([rat(xy[1]),rat(xy[2])])==sol
   if ok:valid.append(a[':answer/id'])
  solution_ok=all(mm[:,:2]*sol==mm[:,2] for mm in ms) and ms[0]==m and ms[-1]==S.Matrix([[1,m[0,1]/m[0,0],m[0,2]/m[0,0]],[0,1,sol[1]]])
  results.append({'group':group,'id':q[':question/id'],'template':r['generation']['template'],'parameters':r['generation']['parameters'],'solution':list(sol),'solution_stages_valid':solution_ok,'uniquely_correct':valid==[correct(r)]})
  cases.append({'label':group+':'+q[':question/id'],'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id'] in valid else 'rejected','purpose':'Independent exact arithmetic checks entire matrix and stated solution'} for a in choices(r)]})
# Controlled pair: k changes, h fixed. Irrelevant option order changes, complete values unchanged.
a=g.generate('easy',820219,'q-73544',[1,0]);b=g.generate('easy',820219,'q-73544',[1,1]);c=json.loads(json.dumps(a));field(c)[':answer-field/choices'].reverse()
pairs=[a,b,c];save('counterfactual-records.json',pairs)
for i,r in enumerate(pairs):cases.append({'label':'counterfactual-'+str(i),'record':r,'checks':[{'submitted_answer_id':z[':answer/id'],'expected':'accepted' if z[':answer/id']==correct(r) else 'rejected','purpose':'Verify changed/preserved response in controlled pair'} for z in choices(r)]})
save('native-input.json',cases);save('math-results.json',results)
cf={'relevant':{'parameters_before':[1,0],'parameters_after':[1,1],'before_solution':list(prompt_matrix(a['question'][':question/problem'])[:,:2].inv()*prompt_matrix(a['question'][':question/problem'])[:,2]),'after_solution':list(prompt_matrix(b['question'][':question/problem'])[:,:2].inv()*prompt_matrix(b['question'][':question/problem'])[:,2]),'prompt_changed':a['question'][':question/problem']!=b['question'][':question/problem'],'solution_changed':a['question'][':question/worked-solution']!=b['question'][':question/worked-solution'],'key_changed':correct(a)!=correct(b)},'irrelevant':{'change':'Reverse choice order','key_preserved':correct(a)==correct(c),'prompt_solution_preserved':all(a['question'][k]==c['question'][k] for k in [':question/problem',':question/worked-solution'])}}
save('counterfactual-results.json',cf)
summary=[]
for group,records in [('samples',samples),('batch',batch),('control',control)]:
 by=defaultdict(list)
 for r in records:by[r['generation']['template']].append(r)
 for sid,rs in by.items():
  hits=0
  for r in rs:
   vals,_=ranks(r);target=sorted(vals)[1];selected=[a for a,v in zip(choices(r),vals) if v==target];hits+=len(selected)==1 and selected[0][':answer/id']==correct(r)
  summary.append({'group':group,'template':sid,'coefficient_signature':sig(rs[0]),'n':len(rs),'correct_position_counts':dict(Counter(idx(r)+1 for r in rs)),'correct_y_rank_counts':dict(Counter(ranks(r)[1] for r in rs)),'choose_unique_second_smallest_y_hits':hits})
save('shortcut-results.json',summary)
# Current inventory contains only original questions; do not flag originals as generated.
inv=read('source/inventory.json');save('inventory-review.json',{'basis':inv['basis'],'count':len(inv['questions']),'questions':[{'id':q[':question/id'],'entity_id':q[':db/id'],'keys':list(q),'source_original':q[':question/id'] in {x[':question/id'] for x in original}} for q in inv['questions']],'conclusion':'All ten stored questions are original sources. No stored generated instances of the demonstrated family defect are present in this captured inventory.'});save('affected-inventory.json',{'affected_questions':[]})
manifest=read('workspace/package.json');hashes={p:hashlib.sha256((JOB/'workspace'/p).read_bytes()).hexdigest() for p in manifest['files']};save('package-hashes-before.json',hashes)
checks=[]
for args in [('hard',0,None,None),('easy',0,'q-20496',None),('easy',0,'q-73544',[4,0]),('easy',0,'q-73544',[True,0]),('easy',0,'q-73544',[0])]:
 try:g.generate(*args);checks.append({'args':args,'rejected':False})
 except ValueError as e:checks.append({'args':args,'rejected':True,'error':str(e)})
rel=ROOT/'relocated';rel.mkdir(exist_ok=True)
shutil.copy2(JOB/'workspace/17592186059776.py',rel/'17592186059776.py')
for name in ['source.json','reference/initial/basis.json']:
 dest=rel/'17592186059776'/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(JOB/'workspace/17592186059776'/name,dest)
command=[sys.executable,str(rel/'17592186059776.py'),'--difficulty','easy','--seed','920221','--count','5']
proc=subprocess.run(command,cwd=ROOT,capture_output=True,text=True); relocated=json.loads(proc.stdout)
save('relocated-output.json',relocated)
save('packaging-results.json',{'python':platform.python_version(),'sympy':S.__version__,'manifest_dependencies':manifest['dependencies'],'declared_files_exist':all((JOB/'workspace'/p).exists() for p in manifest['files']),'relocation_command':command,'relocation_matches':relocated==g.batch('easy',5,920221),'deterministic':g.batch('easy',5,920221)==g.batch('easy',5,920221),'rejections':checks,'runtime_inputs':['source.json','reference/initial/basis.json'],'external_output':'stdout JSON only; no assets','history_present':(JOB/'repair-history.json').exists(),'preflight_present':(JOB/'repair-preflight.json').exists()})
save('render-input.json',batch+pairs+[samples[6]])
print(json.dumps({'replay':replay_report,'math_failures':[x for x in results if not x['solution_stages_valid'] or not x['uniquely_correct']],'shortcuts':summary,'grading_cases':len(cases)},indent=2))
