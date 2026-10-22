import json,pathlib,importlib.util,sys,collections,re,subprocess
sys.dont_write_bytecode=True
E=pathlib.Path(__file__).resolve().parent;W=E.parent/'workspace'
spec=importlib.util.spec_from_file_location('candidate',W/'17592186119771.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def save(p,x):(E/p).write_text(json.dumps(x,indent=2)+'\n')
def matrix(r):
 b=re.search(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',r['question'][':question/problem'],re.S)[1]
 return [[int(v.strip()) for v in z.split('&')] for z in b.split(r'\\')]
def answer(r):
 f=r['question'][':question/answer-fields'][0];return next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
def independent(m):
 n=len(m);up=any(m[i][j] for i in range(n) for j in range(i+1,n));lo=any(m[i][j] for i in range(n) for j in range(i))
 return ('Identity matrix' if all(m[i][i]==1 for i in range(n)) else 'Diagonal matrix') if not(up or lo) else 'Other' if up and lo else 'Upper triangular matrix' if up else 'Lower triangular matrix'
def position(r):
 f=r['question'][':question/answer-fields'][0];return next(i+1 for i,a in enumerate(f[':answer-field/choices']) if a[':answer/value']==answer(r))
seeds=[263,1227,40291];batches=[g.batch('easy',5,s) for s in seeds];records=[r for batch in batches for r in batch];save('fresh-batches.json',records)
# Rejection/resampling boundaries are tested on the modified batch branch.
checks=[]
for seed,b in zip(seeds,batches):
 checks.append({'seed':seed,'count':len(b),'support_count':len({tuple(tuple(int(v!=0) for j,v in enumerate(row) if i!=j) for i,row in enumerate(matrix(r))) for r in b}),'answers':dict(collections.Counter(answer(r) for r in b)),'attempt':b[0]['generation']['batch_selection_attempt'],'math_correct':all(answer(r)==independent(matrix(r)) for r in b)})
base=json.load(open(E/'independent-records.json'))[:18];fingerprints=[r['generation']['parameter_fingerprint'] for r in base]
boundaries=[]
for name,fun in [('catalog_exhaustion',lambda:g.batch('easy',19,1227)),('all_excluded',lambda:g.batch('easy',1,1227,exclude_fingerprints=fingerprints))]:
 try:fun();boundaries.append({'case':name,'rejected':False})
 except ValueError as e:boundaries.append({'case':name,'rejected':True,'message':str(e)})
# A finite remainder must remain available, including a sole sparse task.
remain=g.batch('easy',1,1227,exclude_fingerprints=fingerprints[:-1]);save('remainder-records.json',remain)
boundaries.append({'case':'one_remaining','count':len(remain),'fingerprint_matches':remain[0]['generation']['parameter_fingerprint']==fingerprints[-1]})
# Source-backed canonical + each sole witness: parameter acceptance stays unconditional.
sparse=[]
for i in range(3):
 for j in range(3):
  if i==j:continue
  m=[[0]*3 for _ in range(3)]
  for k in range(3):m[k][k]=[-10,0,10][k]
  m[i][j]=10 if (i+j)%2 else -10
  sparse.append(g.generate('easy',1227,parameters={'matrix':m,'letter':'C','layout':'bmatrix'}))
save('sparse-records.json',sparse)
assert all(answer(r)==independent(matrix(r)) for r in sparse+records)
save('focused-results.json',{'command':sys.executable+' '+str(E/'audit_focus.py'),'fresh_batches':checks,'boundaries':boundaries,'sole_witness_cases':[{'matrix':matrix(r),'answer':answer(r),'key_correct':answer(r)==independent(matrix(r))} for r in sparse]})
# Surface probes from visible matrices and answer controls, independent of template metadata.
def probe(rs):
 out=[]
 for n in sorted({len(matrix(r)) for r in rs}):
  sub=[r for r in rs if len(matrix(r))==n]
  for cue,fn in [('top-left sign',lambda r:(matrix(r)[0][0]>0)-(matrix(r)[0][0]<0)),('matrix letter',lambda r:re.search(r'([AC])\s*=',r['question'][':question/problem'])[1]),('diagonal sign pattern',lambda r:tuple((matrix(r)[i][i]>0)-(matrix(r)[i][i]<0) for i in range(n))),('raw correct position',position)]:
   if cue=='raw correct position':
    c=collections.Counter(position(r) for r in sub);hits=max(c.values());counts=dict(c)
   else:
    c=collections.defaultdict(collections.Counter)
    for r in sub:c[str(fn(r))][answer(r)]+=1
    hits=sum(max(x.values()) for x in c.values());counts={k:dict(v) for k,v in c.items()}
   out.append({'size':n,'cue':cue,'lookup_hits':hits,'total':len(sub),'groups':counts,'interpretation':'Fitted lookups with singleton cells are descriptive only; no universal generator claim.'})
  orient=[r for r in sub if independent(matrix(r)) in ['Upper triangular matrix','Lower triangular matrix']]
  first=sum(next(a[':answer/value'] for a in r['question'][':question/answer-fields'][0][':answer-field/choices'] if a[':answer/value'] in ['Upper triangular matrix','Lower triangular matrix'])==answer(r) for r in orient)
  out.append({'size':n,'cue':'first upper/lower choice','correct':first,'total':len(orient),'complement_correct':len(orient)-first})
 return out
batch=json.load(open(E/'runner-batch.json'));save('focused-shortcuts.json',{'exact_batch':probe(batch),'fresh_batches':[{'seed':s,'probes':probe(b)} for s,b in zip(seeds,batches)],'controls':probe(json.load(open(E/'independent-records.json')))})
# Preserve observed support coverage without duplicating the earlier exhaustive 334-case audit.
ss=lambda r:(len(matrix(r)),tuple(int(v!=0) for i,row in enumerate(matrix(r)) for j,v in enumerate(row) if i!=j))
save('support-coverage.json',{'full_easy_count':len({ss(r) for r in base}),'expected':18,'source_case':'canonical sole lower witness and all six 3x3 coordinates accepted','source_ref':'tutorial 658a47dc-4d32-5d9d-a04c-82d683e87739','records':'independent-records.json'})
print(json.dumps({'fresh_batches':checks,'boundaries':boundaries,'exact_batch_probes':probe(batch)}))
