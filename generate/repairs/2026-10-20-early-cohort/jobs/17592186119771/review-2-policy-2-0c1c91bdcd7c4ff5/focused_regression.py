import pathlib,json,subprocess,sys,itertools,importlib.util,shutil,hashlib
E=pathlib.Path(__file__).resolve().parent;W=E.parent/'workspace';PY=sys.executable;sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location('candidate',W/'17592186119771.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def save(p,x):(E/p).write_text(json.dumps(x,indent=2)+'\n')
old=E.parent/'review-1-policy-2-0e9bf2a26bc3c6cc/relocated/17592186119771.py'
commands=[]
for kind,entry in [('old',old),('current',W/'17592186119771.py')]:
 cmd=[PY,str(E/'test_single_witness.py'),str(entry)];p=subprocess.run(cmd,capture_output=True,text=True);commands.append({'target':kind,'command':cmd,'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr});shutil.copyfile(E/'single-witness-acceptance.json',E/(kind+'-single-witness.json'))
 assert p.returncode==(1 if kind=='old' else 0)
# Independently enumerate source-grounded support combinations and inspect actual normal output.
all_records=[];coverage=[]
for level,n in [('easy',2),('easy',3),('moderate',3),('hard',4)]:
 wanted=set();explicit=[]
 for upper in (False,True):
  cells=[(i,j) for i in range(n) for j in range(n) if (i<j if upper else i>j)]
  for bits in itertools.product((0,1),repeat=len(cells)):
   if not any(bits):continue
   m=[[(-2 if i==0 else 0) if i==j else 0 for j in range(n)] for i in range(n)]
   for b,(i,j) in zip(bits,cells):m[i][j]=6*b
   r=g.generate(level,seed=9023,parameters={'matrix':m,'letter':'C','layout':'bmatrix'});all_records.append(r)
   def signature(m):return (len(m),tuple(v!=0 for i,row in enumerate(m) for j,v in enumerate(row) if i!=j))
   wanted.add(signature(m))
   explicit.append({'matrix':m,'record_index':len(all_records)-1,'expected':('Upper' if upper else 'Lower')+' triangular matrix'})
 wanted.add((n,tuple(False for _ in range(n*(n-1)))))
 normal=g.batch(level,18 if level=='easy' else len(wanted),seed=6109)
 observed={signature(r['generation']['parameters']['matrix']) for r in normal if len(r['generation']['parameters']['matrix'])==n}
 assert observed==wanted,(level,n,wanted-observed)
 coverage.append({'difficulty':level,'size':n,'expected_supports':len(wanted),'observed_supports':len(observed),'missing':list(wanted-observed),'explicit_cases':explicit,'normal_record_start':len(all_records),'normal_record_count':len(normal)})
 all_records+=normal
save('focused-support-records.json',all_records);save('focused-support-results.json',{'command':[PY,str(E/'focused_regression.py')],'retained_finding':'dbcd1ab741c06c08a3a5','old_and_current':commands,'coverage':coverage})
# The retained author preflight script is run unchanged except output redirection.
a=E/'author-suite';a.mkdir(exist_ok=True);shutil.copyfile(E/'author-check-redirected.py',a/'validate.py');shutil.copyfile(W/'checks/single_witness.py',a/'single_witness.py')
p=subprocess.run([PY,str(a/'single_witness.py')],capture_output=True,text=True);save('author-preflight-rerun.json',{'command':[PY,str(a/'single_witness.py')],'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr});assert p.returncode==0,p.stderr
# Boundary rejection / exclusion contracts on changed catalog.
b=[]
for label,kwargs in [('catalog_exhaustion',{'count':19}),('all_excluded',{'count':1,'exclude_fingerprints':[r['generation']['parameter_fingerprint'] for r in g.batch('easy',18,6109)]})]:
 try:g.batch('easy',seed=6109,**kwargs);b.append({'case':label,'rejected':False})
 except ValueError as ex:b.append({'case':label,'rejected':True,'message':str(ex)})
assert all(x['rejected'] for x in b);save('boundary-results.json',b)
print(json.dumps({'old_failure_reproduced':True,'current_accepts':True,'support_counts':[(x['difficulty'],x['size'],x['observed_supports']) for x in coverage],'records':len(all_records),'preflight_exit':p.returncode}))
