import os,sys,json,re,hashlib,platform,importlib.metadata,collections,subprocess,shutil
from pathlib import Path
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parent; JOB=ROOT.parent; PKG=JOB/'workspace'; REPO=Path('/home/jake/Developer/Course_Academy')
sys.dont_write_bytecode=True;sys.path.insert(0,str(PKG));import generator as g

def save(n,v): (ROOT/n).write_text(json.dumps(v,indent=2,default=str))
def mats(s):
 return [[[F(re.sub(r'\\frac\{(-?\d+)\}\{(\d+)\}',r'\1/\2',v.replace(r'\,','').replace(' ','').strip())) for v in row.split('&')] for row in body.split(r'\\')] for body in re.findall(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',s,re.S)]
def target(s):
 x=re.search(r'a\}?_\{(\d)(\d)\}',s);return int(x[1])-1,int(x[2])-1

def op(s):
 s=s.replace(' ',''); rows=[int(x)-1 for x in re.findall(r'(?:\{R\}|R)_\{([123])\}',s)]
 if '↔' in s or r'\leftrightarrow' in s:return ('swap',*rows)
 lhs,rhs=s.split(':='); t=rows[0]
 rhs=re.sub(r'(?:\{R\}|R)_\{([123])\}',r'r\1',rhs)
 rhs=re.sub(r'\\frac\{(-?\d+)\}\{(\d+)\}',r'(\1/\2)',rhs).replace(r'\cdot','*')
 # Parse a linear combination using signed row terms, no generator parser or sympy.
 terms=re.findall(r'([+-]?(?:\([^()]+\)|[\d/]+)?\*?)r([123])',rhs)
 cs=[F(0)]*3
 for k,r in terms:
  k=k.rstrip('*').replace('(','').replace(')',''); k=k.replace('+-','-').replace('++','+'); cs[int(r)-1]+=F(k if k not in ('','+','-') else {'':'1','+':'1','-':'-1'}[k])
 assert len(terms)==rhs.count('r'),rhs
 return ('linear',t,cs)
def apply(a,o):
 b=[row[:] for row in a]
 if o[0]=='swap':b[o[1]],b[o[2]]=b[o[2]],b[o[1]]
 else:b[o[1]]=[sum(o[2][i]*a[i][c] for i in range(3)) for c in range(3)]
 return b

def analyze(r):
 q=r['question']; a=mats(q[':question/problem'])[0];t,c=target(q[':question/problem']);f=q[':question/answer-fields'][0];vs=f[':answer-field/choices'];key=f[':answer-field/correct'];kid=key[1] if isinstance(key,list) else key[':answer/id'];oks=[]
 for i,v in enumerate(vs):
  o=op(v[':answer/value']);b=apply(a,o)
  if b[t][c]==0:oks.append(i)
 assert len(oks)==1,(q[':question/id'],oks)
 i=oks[0];assert vs[i][':answer/id']==kid
 b=apply(a,op(vs[i][':answer/value'])); sol=mats(q[':question/worked-solution']);assert sol[0]==a and sol[-1]==b,(q[':question/id'],'solution mismatch')
 return {'id':q[':question/id'],'profile':r.get('generation',{}).get('bank_profile'),'target':f'{t+1}{c+1}','position':i,'correct':vs[i][':answer/value'],'kind':op(vs[i][':answer/value'])[0],'row_outcome':b,'choice_count':len(vs)}

before={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in PKG.iterdir() if p.is_file()};save('package-before.json',before)
source=json.load(open(JOB/'source/source.json')); sq=source['material']['kp'][':knowledge-point/questions']; replays=[]; replay_pairs=[]; replay_failures=[]
for q in sq:
 try:
  r=g.replay(q[':question/math-academy-id']);replays.append(r);replay_pairs.append((q,r))
 except Exception as e:replay_failures.append({'source_id':q[':question/id'],'profile':q[':question/math-academy-id'],'exception':str(e),'command':"g.replay("+repr(q[':question/math-academy-id'])+")"})
save('source-replays.json',replays); save('source-replay-failures.json',replay_failures)
source_report=[]
for q,r in replay_pairs:
 ar=analyze(r); f=q[':question/answer-fields'][0]; rf=r['question'][':question/answer-fields'][0]
 assert mats(q[':question/problem'])==mats(r['question'][':question/problem'])
 assert [op(v[':answer/value']) for v in f[':answer-field/choices']]==[op(v[':answer/value']) for v in rf[':answer-field/choices']]
 source_report.append({'source_id':q[':question/id'],'profile':q[':question/math-academy-id'],'complete_bank_replayed':True,'correct':ar['correct'],'original_solution_matches':mats(q.get(':question/worked-solution',''))[-1:]==mats(r['question'][':question/worked-solution'])[-1:]})
save('source-replay-results.json',source_report)
# Exercise all independently eligible winners in every available source bank.
records=[]; coverage=[]
for q in sq:
 sid=q[':question/math-academy-id'];t,c=target(q[':question/problem']); eligible=[]
 for j,v in enumerate(q[':question/answer-fields'][0][':answer-field/choices']):
  o=op(v[':answer/value'])
  if (o[0]=='swap' and t in o[1:]) or (o[0]=='linear' and o[1]==t and o[2][t]==1 and sum(x!=0 for i,x in enumerate(o[2]) if i!=t)==1):eligible.append(j)
 for j in eligible:
  for seed in [81703,419531]:
   try:
    r=g.generate(seed=seed,template=sid,parameters={'winner':j});records.append(r);coverage.append({'profile':sid,'winner':j,'seed':seed,'result':'generated'})
   except Exception as e:coverage.append({'profile':sid,'winner':j,'seed':seed,'result':str(e)})
records+=g.batch('hard',30,8102026);save('independent-samples.json',records);save('coverage.json',coverage)
batch=json.load(open(JOB/'samples.json'));save('runner-batch.json',batch)
# Controlled changes preserve all other data and choice order.
base={'source':'q-20388','rows':[0,1,2],'cols':[0,1,2],'order':[0,1,2,3,4]}
params=[dict(base,winner=3,matrix=[[4,2,2],[3,6,4],[2,4,1]]),dict(base,winner=4,matrix=[[4,2,2],[3,8,4],[2,4,1]]),dict(base,winner=3,matrix=[[9,2,2],[3,6,4],[2,4,-9]]),dict(base,winner=3,matrix=[[4,2,2],[3,6,4],[2,4,1]],cols=[1,0,2]),dict(base,winner=3,matrix=[[4,2,2],[3,6,4],[2,4,1]],rows=[1,0,2])]
pairs=[g.generate(seed=67103,parameters=p) for p in params];save('counterfactual-records.json',pairs)
checked={name:[analyze(r) for r in rs] for name,rs in [('independent',records),('batch',batch),('counterfactual',pairs)]};save('math-results.json',checked)
checks=[]
for r in batch+replays+pairs+[next(r for r in records if analyze(r)['kind']=='swap')]:
 ar=analyze(r);f=r['question'][':question/answer-fields'][0];checks.append({'label':r['question'][':question/id'],'record':r,'checks':[{'field_index':0,'submitted_answer_id':v[':answer/id'],'expected':'accepted' if i==ar['position'] else 'rejected','purpose':'Independent Fraction arithmetic for every choice'} for i,v in enumerate(f[':answer-field/choices'])]})
save('grader-input.json',checks)
reject=[]
for label,args in [('unsupported difficulty',{'difficulty':'easy'}),('ambiguous matrix',{'parameters':dict(base,winner=3,matrix=[[4,2,2],[3,6,4],[2,3,1]])}),('zero target',{'parameters':dict(base,winner=3,matrix=[[4,2,2],[3,0,4],[2,3,1]])}),('bad permutation',{'parameters':dict(base,rows=[0,0,2])}),('scale as winner',{'template':'q-20388','parameters':{'winner':0}})]:
 try:g.generate(**args);reject.append({'case':label,'result':'UNEXPECTED ACCEPT'})
 except Exception as e:reject.append({'case':label,'result':'rejected','message':str(e)})
save('rejection-results.json',reject)
replay_comparison=[{'id':r['question'][':question/id'],'question_matches':g.generate(seed=r['generation']['seed'],parameters=r['generation']['parameters'])['question']==r['question']} for r in records[:10]+batch]; assert all(x['question_matches'] for x in replay_comparison); assert g.batch('hard',5,819211)==g.batch('hard',5,819211); save('determinism-results.json',replay_comparison)
versions={'python':platform.python_version(),'packages':{x:importlib.metadata.version(x) for x in ['sympy','mpmath']}}
copy=ROOT/'relocated';copy.mkdir(exist_ok=True)
for p in PKG.iterdir():
 if p.is_file():shutil.copy2(p,copy/p.name)
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'); command=[sys.executable,str(copy/'generator.py'),'--count','5','--seed','864209']
x=json.loads(subprocess.check_output(command,cwd=ROOT,env=env));assert x==g.batch('hard',5,864209);save('relocated-records.json',x)
save('packaging-results.json',{'versions':versions,'manifest_matches':versions==json.load(open(PKG/'package.json'))['dependencies'],'deterministic_replay':True,'relocation_command':command,'relocation_matches':True,'package_unchanged':before=={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in PKG.iterdir() if p.is_file()}})
# Render all exact batch items, both relevant counterfactuals, irrelevant and target changes, and corrected source.
save('render-records.json',batch+pairs+[replays[4],replays[1]])
print(json.dumps({'source_replays':len(replays),'independent':len(records),'coverage_failures':[c for c in coverage if c['result']!='generated'],'math_checks':sum(map(len,checked.values())),'versions':versions},indent=2))
(ROOT/'session-state.md').write_text('Source replay, independent exact Fraction arithmetic, controlled counterfactual records, deterministic replay, relocation and rejection probes completed. See audit.py and resulting JSON files. Native grader, delivery, rendering and decision analysis pending. No package writes.\n')
