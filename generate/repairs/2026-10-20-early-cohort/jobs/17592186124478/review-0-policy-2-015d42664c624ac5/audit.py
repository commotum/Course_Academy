import sys,os,json,re,pathlib,itertools,hashlib,platform,importlib.metadata,shutil,subprocess
sys.dont_write_bytecode=True
ROOT=pathlib.Path(__file__).resolve().parent
JOB=ROOT.parent
PKG=JOB/'workspace'
sys.path.insert(0,str(PKG))
import generator as g

def save(name,v): (ROOT/name).write_text(json.dumps(v,indent=2)+'\n')
def mats(text):
 return [[[int(x.strip()) for x in row.split('&')] for row in body.split(r'\\')] for body in re.findall(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',text,re.S)]
def correct(f):
 a=f[':answer-field/correct']
 if isinstance(a,dict):return a[':answer/value']
 return next(c[':answer/value'] for c in f[':answer-field/choices'] if c[':answer/id']==a[1])
def inspect(rec):
 q=rec.get('question',rec);m=mats(q[':question/problem'])[0];rows=len(m);cols=len(m[0]);lead=[next((j for j,x in enumerate(row) if x),None) for row in m];ps=[j for j in lead if j is not None];non=[j+1 for j in range(cols) if j not in ps];errors=[]
 if ps!=sorted(set(ps)) or lead!=ps+[None]*(rows-len(ps)):errors.append('not REF')
 fields=q[':question/answer-fields']; seen=[]
 for f in fields:
  j=int(re.match(r'Column (\d+):',f[':answer-field/key'])[1]);seen.append(j)
  if mats(f[':answer-field/key'])[0]!=[[row[j-1]] for row in m]:errors.append('vector mismatch')
  if correct(f)!=str(j in non).lower():errors.append('key mismatch')
  if sorted(a[':answer/value'] for a in f[':answer-field/choices'])!=['false','true']:errors.append('bank mismatch')
 if sorted(seen)!=list(range(1,cols+1)):errors.append('incomplete columns')
 sol=q[':question/worked-solution']; sm=mats(sol)
 if sm!=[m]:errors.append('solution matrix mismatch')
 tail=sol.split('Therefore,')[-1];claimed=[int(x) for x in re.findall(r'\$(\d+)\$',tail)]
 if sorted(claimed)!=non:errors.append('solution conclusion mismatch')
 return {'id':q[':question/id'],'shape':[rows,cols],'pivots':[p+1 for p in ps],'non':non,'label':re.search(r'matrix \$(\w)\$',q[':question/problem'])[1],'errors':errors}
files={str(p.relative_to(PKG)):hashlib.sha256(p.read_bytes()).hexdigest() for p in PKG.rglob('*') if p.is_file()};save('package-hashes-before.json',files)
s=json.load(open(JOB/'source/source.json'));qs=s['material']['kp'][':knowledge-point/questions'];replays=[];replay_results=[]
for q in qs:
 sid=q[':question/math-academy-id'];r=g.generate(template=sid,parameters=g.DEFAULTS[sid],seed=9137);replays.append(r)
 # Compare normalized prose and complete column-labelled banks; UUID/order are incidental.
 n=lambda x:re.sub(r'\s+',' ',x).strip()
 out=r['question'];a={re.match(r'Column (\d+):',f[':answer-field/key'])[1]:(mats(f[':answer-field/key']),sorted(c[':answer/value'] for c in f[':answer-field/choices']),correct(f)) for f in q[':question/answer-fields']};b={re.match(r'Column (\d+):',f[':answer-field/key'])[1]:(mats(f[':answer-field/key']),sorted(c[':answer/value'] for c in f[':answer-field/choices']),correct(f)) for f in out[':question/answer-fields']}
 replay_results.append({'source':q[':question/id'],'prompt':n(q[':question/problem'])==n(out[':question/problem']),'solution':n(q[':question/worked-solution'])==n(out[':question/worked-solution']),'complete_banks':a==b,'math':inspect(r)})
save('source-replays.json',replays);save('source-replay-results.json',replay_results)
random=[g.generate(seed=i) for i in range(824031,824151)];save('fresh-samples.json',random)
# Cover each justified shape/rank/leading-position slot with small boundary-valued matrices.
structural=[]
shapes=sorted({(len(mats(q[':question/problem'])[0]),len(mats(q[':question/problem'])[0][0])) for q in qs})
for rows,cols in shapes:
 for rank in range(2,min(rows,4)+1):
  if cols-rank not in (1,2):continue
  for ps in itertools.combinations(range(cols),rank):
   m=[[0]*cols for _ in range(rows)]
   for i,p in enumerate(ps):
    m[i][p]=-9 if i%2 else 9
    for j in range(p+1,cols):m[i][j]=0 if (i+j)%2 else -9
   structural.append(g.generate(seed=824030,template='q-35730',parameters={'matrix':m,'label':'A','replay':False}))
save('structural-samples.json',structural)
batch=json.load(open(JOB/'samples.json'));save('runner-batch.json',batch)
# Controlled relevant pair: same 3x4 matrix except second-row first nonzero shifts col 2->3.
base=[[2,4,5,6],[0,3,4,5],[0,0,0,0]]
change=[[2,4,5,6],[0,0,4,5],[0,0,0,0]]
irrel=[[2,-9,5,6],[0,3,4,5],[0,0,0,0]]
pairs=[g.generate(seed=824030,template='q-35730',parameters={'matrix':m,'label':'A','replay':False}) for m in (base,change,irrel)]
save('counterfactual-records.json',pairs)
allgroups={'source':replays,'random':random,'structural':structural,'batch':batch,'counterfactual':pairs};save('math-results.json',{k:[inspect(r) for r in v] for k,v in allgroups.items()})
# Actual native grader: both UI actions on every field, based solely on prompt-derived math.
cases=[]
for group,records in [('batch',batch),('pairs',pairs),('source',replays),('structural',structural)]:
 for r in records:
  truth=inspect(r)['non'];checks=[]
  for i,f in enumerate(r['question'][':question/answer-fields']):
   j=int(re.match(r'Column (\d+):',f[':answer-field/key'])[1])
   for a in f[':answer-field/choices']:
    valid=(a[':answer/value']=='true')==(j in truth)
    checks.append({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if valid else 'rejected','purpose':'prompt-derived column membership; exercise both checkbox states'})
  cases.append({'label':group+':'+r['question'][':question/id'],'record':r,'checks':checks})
save('grader-input.json',cases)
# Reject malformed inputs and out-of-family workloads, rather than silently replacing them.
invalid={'non_REF':[[2,0,1],[0,0,0],[0,3,4]],'descending':[[0,1,2],[1,2,3],[0,0,0]],'duplicate_pivot':[[1,2,3],[2,3,4],[0,0,0]],'noninteger':[[1.5,2,3],[0,1,2],[0,0,0]],'range':[[10,2,3],[0,1,2],[0,0,0]],'full_rank':[[1,2,3],[0,1,2],[0,0,1]],'rank_one':[[1,2,3],[0,0,0],[0,0,0]]}
reject=[]
for name,m in invalid.items():
 try:g.generate(parameters={'matrix':m,'label':'A','replay':False});reject.append({'case':name,'rejected':False})
 except Exception as e:reject.append({'case':name,'rejected':True,'error':type(e).__name__})
for kwargs in [{'difficulty':'hard'},{'count':-1},{'count':len(structural)+1}]:
 try:g.batch(seed=824031,**kwargs) if 'count' in kwargs else g.generate(seed=824031,**kwargs);reject.append({'case':kwargs,'rejected':False})
 except Exception as e:reject.append({'case':kwargs,'rejected':True,'error':type(e).__name__})
save('rejection-results.json',reject)
manifest=json.load(open(PKG/'package.json'));deps=manifest['dependencies'];runtime={'python':platform.python_version(),'packages':{n:importlib.metadata.version(n) for n in deps['packages']}}
small=g.batch('easy',5,824031);save('independent-batch.json',small)
rel=ROOT/'relocated-package';shutil.copytree(PKG,rel,dirs_exist_ok=True)
run=subprocess.run([sys.executable,'-B',str(rel/'generator.py'),'--seed','824031','--count','5','--output',str(ROOT/'relocated-batch.json')],cwd=ROOT,capture_output=True,text=True)
pack={'declared':deps,'actual':runtime,'dependencies_exact':deps==runtime,'deterministic':small==g.batch('easy',5,824031),'relocation_exit':run.returncode,'relocation_stderr':run.stderr,'relocation_equal':json.load(open(ROOT/'relocated-batch.json'))==small,'empty_count':g.batch('easy',0,824031)==[],'hashes_unchanged':files=={str(p.relative_to(PKG)):hashlib.sha256(p.read_bytes()).hexdigest() for p in PKG.rglob('*') if p.is_file()}}
save('packaging-results.json',pack)
inv=json.load(open(JOB/'source/inventory.json'));save('inventory-inspection.json',{'basis':inv['basis'],'total':len(inv['questions']),'questions':[{'id':q[':question/id'],'entity_id':q[':db/id'],'keys':list(q),'math':inspect(q)} for q in inv['questions']]})
save('affected-inventory.json',{'affected_questions':[]})
save('render-records.json',batch+pairs+[replays[0],structural[-1]])
print(json.dumps({'source_cases':len(replays),'replay_failures':[r['source'] for r in replay_results if not all(r[k] for k in ['prompt','solution','complete_banks'])],'structural_cases':len(structural),'math_errors':{k:[inspect(r) for r in v if inspect(r)['errors']] for k,v in allgroups.items()},'packaging':pack,'rejection_failures':[r for r in reject if not r['rejected']]}))
