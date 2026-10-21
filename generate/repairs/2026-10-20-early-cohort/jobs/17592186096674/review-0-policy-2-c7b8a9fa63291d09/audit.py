import sys,json,re,hashlib,importlib.util,pathlib,subprocess,shutil,collections
sys.dont_write_bytecode=True
ROOT=pathlib.Path(__file__).resolve().parent
REPO=pathlib.Path('/home/jake/Developer/Course_Academy'); WORK=ROOT.parent/'workspace'; PY=REPO/'.venv/bin/python'
sys.path.insert(0,str(WORK));import generator as g
import sympy as sp

def save(name,v): (ROOT/name).write_text(json.dumps(v,indent=2)+'\n')
def hashes():return {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in WORK.iterdir() if p.is_file()}
save('package-hashes-before.json',hashes())
def matrices(s):
 out=[]
 for m in re.finditer(r'\\begin\{(bmatrix|array)\}(?:\{[^}]*\})?(.*?)\\end\{\1\}',s,re.S):
  out.append([[int(x.strip()) for x in row.split('&')] for row in m[2].split(r'\\')])
 return out

def system(s):
 block=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',s,re.S)[1]
 rows=[]
 for row in block.split(r'\\'):
  left,right=row.replace('&','').split('=');right=right.strip().rstrip('.')
  coeff=[]
  for var in 'xyz':
   m=re.search(r'([+-]?\d*)'+var,left.replace(' ',''));c=m[1] if m else '0';coeff.append(int(c+'1') if c in ('','+','-') else int(c))
  rows.append(coeff+[int(right)])
 return rows

def triple(v):
 ms=matrices(v)
 if ms:return [r[3] for r in ms[0]]
 if 'langle' in v or '⟨' in v:return list(map(int,re.findall(r'-?\d+',v)))
 return [int(re.search(var+r'\s*=\s*(-?\d+)',v)[1]) for var in 'xyz']

def check(r):
 q=r['question'];M=sp.Matrix(system(q[':question/problem']));target=list(M.rref()[0][:,3]);f=q[':question/answer-fields'][0];choices=f[':answer-field/choices'];ts=[triple(c[':answer/value']) for c in choices];correct=[c[':answer/id'] for c,t in zip(choices,ts) if t==target]
 assert len(correct)==1 and correct[0]==f[':answer-field/correct'][1]
 assert len(set(map(tuple,ts)))==5
 ms=matrices(q[':question/worked-solution']);assert ms[0]==M.tolist();assert ms[-1]==M.rref()[0].tolist()
 # Independently parse each displayed row operation and check its resulting full matrix.
 ops=re.findall(r'R_\{(\d)\}:=R_\{\d\}([+-])(\d*)R_\{(\d)\}',q[':question/worked-solution'])
 assert len(ops)==len(ms)-1
 for before,after,(t,sign,n,p) in zip(ms,ms[1:],ops):
  expected=[row[:] for row in before];factor=(int(n) if n else 1)*(1 if sign=='+' else -1);expected[int(t)-1]=[x+factor*y for x,y in zip(before[int(t)-1],before[int(p)-1])];assert expected==after
 return {'id':q[':question/id'],'solution':list(map(int,target)),'steps':len(ops),'profile':r['generation']['source_profile'],'correct_position':next(i for i,c in enumerate(choices) if c[':answer/id']==correct[0])}
source=json.load(open(ROOT.parent/'source/source.json'));qs=source['material']['kp'][':knowledge-point/questions']
replays=[];rep=[]
for q in qs+[source['material']['kp'][':knowledge-point/canonical-example']]:
 profile=q[':question/math-academy-id']
 try:r=g.generate(seed=731,template=profile,replay=True)
 except Exception as e:rep.append({'source_id':q[':question/id'],'profile':profile,'status':'unsupported','error':repr(e)});continue
 result=check(r);assert system(q[':question/problem'])==system(r['question'][':question/problem'])
 srcbank=[triple(c[':answer/value']) for c in q[':question/answer-fields'][0][':answer-field/choices']];got=[triple(c[':answer/value']) for c in r['question'][':question/answer-fields'][0][':answer-field/choices']];assert sorted(srcbank)==sorted(got)
 assert q[':question/answer-fields'][0][':answer-field/type'][':db/ident']==r['question'][':question/answer-fields'][0][':answer-field/type']
 rep.append({'source_id':q[':question/id'],'profile':profile,'status':'passed','complete_bank':True,'math':result});replays.append(r)
save('source-replay-records.json',replays);save('source-replay.json',rep)
samples=[]
for pi,profile in enumerate(sorted(g.PROFILES)):
 for role in range(5):
  mask=g.MASKS[(pi+role)%4];params={'role':role,'mask':list(mask),'coefficients':[(5 if (pi+role+j)%2 else -5) if a else 0 for j,a in enumerate(mask)],'translation':[-5,0,5] if role%2 else [5,-5,0],'scale':1+role%2}
  samples.append(g.generate(seed=918271+100*pi+role,template=profile,parameters=params))
# Fresh unforced samples exercise actual random sampler and rejection/dedup path.
raw=g.batch('easy',60,6804921);save('random-records.json',raw);save('controlled-records.json',samples)
batch=json.load(open(ROOT.parent/'samples.json'));save('runner-batch.json',batch)
pairs=[];pairreport=[]
for profile in ['q-20594','q-20591','q-131586']:
 p={'role':0,'mask':[1,1,1],'coefficients':[2,-3,1],'translation':[0,0,0],'scale':1}
 before=g.generate(seed=924,template=profile,parameters=p);relevant=g.generate(seed=924,template=profile,parameters=dict(p,role=1));irrelevant=g.generate(seed=924,template=profile,parameters=dict(p,coefficients=[-2,3,-1]))
 b,r,i=map(check,[before,relevant,irrelevant]);assert b['solution']!=r['solution'] and b['solution']==i['solution'];assert before['question'][':question/problem']!=relevant['question'][':question/problem'] and before['question'][':question/problem']!=irrelevant['question'][':question/problem']
 pairs.extend([before,relevant,irrelevant]);pairreport.append({'profile':profile,'seed':924,'parameters':p,'relevant_change':{'role':1},'irrelevant_change':{'coefficients':[-2,3,-1]},'before':b,'relevant':r,'irrelevant':i,'status':'passed','note':'Parameters only construct pairs; expectations recomputed from displayed equations and displayed choices, steps independently checked.'})
save('counterfactual-records.json',pairs);save('counterfactual-results.json',pairreport)
allrecords=replays+samples+raw+batch+pairs;math=[check(r) for r in allrecords];save('math-results.json',{'checked':len(math),'failures':[],'records':math})
cases=[]
for n,r in enumerate(allrecords):
 q=r['question'];f=q[':question/answer-fields'][0];target=list(sp.Matrix(system(q[':question/problem'])).rref()[0][:,3]);checks=[{'submitted_answer_id':c[':answer/id'],'expected':'accepted' if triple(c[':answer/value'])==target else 'rejected','purpose':'independent substitution of displayed choice into displayed system'} for c in f[':answer-field/choices']];cases.append({'label':str(n)+' '+r['generation']['source_profile'],'record':r,'checks':checks})
save('grader-input.json',cases)
rejections=[]
for kwargs in [{'difficulty':'hard'},{'parameters':{'role':5}},{'parameters':{'mask':[0,0,0]}},{'parameters':{'coefficients':[0,0,0],'mask':[1,1,1]}},{'parameters':{'translation':[6,0,0]}},{'parameters':{'scale':0}}]:
 try:g.generate(**kwargs);rejections.append({'kwargs':kwargs,'rejected':False})
 except (ValueError,KeyError) as e:rejections.append({'kwargs':kwargs,'rejected':True,'error':str(e)})
assert all(x['rejected'] for x in rejections)
assert g.batch('easy',5,862901)==g.batch('easy',5,862901)
reloc=ROOT/'relocated';shutil.copytree(WORK,reloc,dirs_exist_ok=True)
def cli(path):return subprocess.run([str(PY),'-B',str(path/'generator.py'),'--count','5','--seed','862901'],cwd=ROOT,check=True,capture_output=True,text=True).stdout
assert cli(WORK)==cli(reloc)
save('packaging.json',{'versions':{'python':sys.version.split()[0],'sympy':sp.__version__},'manifest':json.load(open(WORK/'package.json')),'rejections':rejections,'deterministic':True,'relocation_equal':True,'external_outputs':'CLI emits JSON on stdout; no assets or external output paths; disabled bytecode writes.','unchanged':hashes()==json.load(open(ROOT/'package-hashes-before.json'))})
# Render all batch, each representation pair and nonduplicate representative replay.
save('render-records.json',batch+pairs+[next(r for r in replays if r['generation']['source_profile']=='q-20600')])
print(json.dumps({'source_replay':collections.Counter(x['status'] for x in rep),'math_checked':len(math),'native_cases':len(cases),'counterfactual_pairs':len(pairreport)*2}))
