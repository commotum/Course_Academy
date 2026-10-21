import sys,json,pathlib,copy,subprocess,hashlib,platform,shutil,re,itertools,collections
sys.dont_write_bytecode=True
E=pathlib.Path(__file__).resolve().parent; W=E.parent/'workspace';sys.path.insert(0,str(W));import generator as g

def save(n,x):(E/n).write_text(json.dumps(x,indent=2)+'\n')
def ref(m,b):
 m=copy.deepcopy(m)
 for i,j in b:m[i][j]=0
 leads=[next((j for j,v in enumerate(row) if v),4) for row in m]
 nz=[v for v in leads if v<4]
 return leads==nz+[4]*(4-len(nz)) and all(a<b for a,b in zip(nz,nz[1:]))
def ci(r):
 f=r['question'][':question/answer-fields'][0];return next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1])
# Controlled change swaps one conflicting entry from row 2 to row 3, with the bank fixed.
m=[[1,1,4,7],[2,4,2,1],[0,0,5,6],[0,0,1,3]]
bank=[[[1,0],[3,2]],[[2,0],[3,2]],[[1,1],[2,2]],[[3,2]],[[1,0]]]
p={'matrix':m,'bank':bank};a=g.generate('moderate',62817,parameters=p);p2=copy.deepcopy(p);p2['matrix'][1][0]=0;p2['matrix'][2][0]=2;b=g.generate('moderate',62817,parameters=p2)
p3=copy.deepcopy(p);p3['matrix'][0][0]=-2;c=g.generate('moderate',62817,parameters=p3)
assert [ci(a),ci(b),ci(c)]==[0,1,0]
cf=[a,b,c];save('counterfactual-records.json',cf)
res=[]
for r in cf:
 p=r['generation']['parameters']; valid=[i for i,b in enumerate(p['bank']) if ref(p['matrix'],b)];assert valid==[ci(r)]
 res.append({'seed':r['generation']['seed'],'parameters':p,'valid':valid,'question_id':r['question'][':question/id']})
save('counterfactual-results.json',{'cases':res,'relevant':'Set a21=0 and a31=2, fixed bank; answer switches from {a21,a43} to {a31,a43}.','irrelevant':'a11 1 -> -2 with original bank; answer preserved.','solution_checked':True})
# Source profiles are exercised through real replay interface.
replays=[]
for x in json.load(open(E/'source-replay.json')):
 r=g.generate('moderate',93312,profile=x['source_id'],replay=True); assert r['generation']['parameters']==x['parameters']
 replays.append(r)
save('profile-replay-records.json',replays)
# Nonminimum case now actually checked, rather than merely accepting a normal process exit.
p=json.load(open(E/'nonminimum-case.json'))['parameters'];nm=g.generate('moderate',8801,parameters=p);assert ci(nm)==0 and ref(p['matrix'],p['bank'][0]) and ref(p['matrix'],[[1,0],[3,2]])
save('nonminimum-current-records.json',[nm])
# Native grader all choices, with expected results independently derived, including delivered exact batch.
cases=[]
rs=json.load(open(E/'delivery-batch/accepted.json'))+json.load(open(E/'independent-samples.json'))[:4]+cf+[nm]+[replays[5],replays[0]]
for r in rs:
 f=r['question'][':question/answer-fields'][0];p=r['generation']['parameters'];checks=[]
 for i,a_ in enumerate(f[':answer-field/choices']):checks.append({'field_index':0,'submitted_answer_id':a_[':answer/id'],'expected':'accepted' if ref(p['matrix'],p['bank'][i]) else 'rejected','purpose':'independent exact row-echelon check for offered operation'})
 cases.append({'label':r['question'][':question/id'],'record':r,'checks':checks})
save('target-render-input.json',[replays[0],nm]);save('grader-input.json',cases);save('render-records.json',json.load(open(E/'delivery-batch/accepted.json'))+cf+[nm])
# Packaging declared files copied for relocation.
rel=E/'relocated';rel.mkdir(exist_ok=True);manifest=json.load(open(W/'package.json'))
for n in manifest['files']+['package.json']:shutil.copyfile(W/n,rel/n)
args=['--difficulty','moderate','--seed','194083','--count','5']
a_=subprocess.run([sys.executable,str(W/'generator.py')]+args,capture_output=True,text=True);b_=subprocess.run([sys.executable,str(rel/'generator.py')]+args,capture_output=True,text=True,cwd=E)
assert a_.returncode==b_.returncode==0 and json.loads(a_.stdout)==json.loads(b_.stdout)
save('cli-records.json',json.loads(a_.stdout));invalid=[]
for args in [['--difficulty','easy'],['--difficulty','moderate','--count','0']]:
 t=subprocess.run([sys.executable,str(W/'generator.py')]+args,capture_output=True,text=True);assert t.returncode!=0;invalid.append({'args':args,'exit_code':t.returncode,'stderr':t.stderr})
reject=[]
for label,p_ in [('multiple correct',{'matrix':m,'bank':[bank[0],bank[0]+[[0,1]],bank[2],bank[3],bank[4]]}),('none correct',{'matrix':m,'bank':bank[1:]+[[[0,0]]]}),('out of range',{'matrix':m,'bank':bank[:4]+[[[4,0]]]}),('repeated coordinate',{'matrix':m,'bank':bank[:4]+[[[0,0],[0,0]]]}),('already echelon',{'matrix':[[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]],'bank':bank})]:
 try:g.generate('moderate',1,parameters=p_);raise AssertionError(label)
 except ValueError as ex:reject.append({'case':label,'parameters':p_,'error':str(ex)})
save('rejection-results.json',reject)
save('packaging-results.json',{'python_actual':platform.python_version(),'dependencies':manifest['dependencies'],'relocation_identical':True,'deterministic_replay':g.generate('moderate',194083)==json.loads(a_.stdout)[0],'invalid_cli':invalid,'files_copied':manifest['files'],'external_output':'stdout JSON; no generated assets; all paths relative to package __file__','package_root_file_hashes_unchanged':json.load(open(E/'package-before.json'))=={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in W.iterdir() if p.is_file()}})
print(json.dumps({'profiles':len(replays),'grader_records':len(cases),'counterfactual_indices':[ci(r) for r in cf],'rejections':len(reject),'packaging':json.load(open(E/'packaging-results.json'))}))
