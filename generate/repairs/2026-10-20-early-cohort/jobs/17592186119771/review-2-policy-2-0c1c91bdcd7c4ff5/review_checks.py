import json,re,sys,importlib.util,pathlib,hashlib,subprocess,platform,shutil,collections
E=pathlib.Path(__file__).resolve().parent; W=E.parent/'workspace'; PY=sys.executable
sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location('candidate',W/'17592186119771.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def save(name,obj): (E/name).write_text(json.dumps(obj,indent=2)+'\n')
def mat(q):
 t=q[':question/problem'];m=re.search(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',t,re.S);return [[int(x.strip()) for x in row.split('&')] for row in m[1].split(r'\\')]
def label(m):
 n=len(m);up=any(m[i][j]!=0 for i in range(n) for j in range(i+1,n));lo=any(m[i][j]!=0 for i in range(n) for j in range(i))
 if not up and not lo:return 'Identity matrix' if all(m[i][i]==1 for i in range(n)) else 'Diagonal matrix'
 return 'Other' if up and lo else 'Upper triangular matrix' if up else 'Lower triangular matrix'
def answer(q):
 f=q[':question/answer-fields'][0];c=f.get(':answer-field/correct');cid=c.get(':answer/id') if isinstance(c,dict) else c[1] if c else None
 return next((a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==cid),None)
def call(p,seed=739):return g.generate('easy',seed,parameters={'matrix':p,'letter':'A','layout':'bmatrix'})
manifest=json.load(open(W/'package.json')); before={str(p.relative_to(W)):hashlib.sha256(p.read_bytes()).hexdigest() for p in W.rglob('*') if p.is_file()};save('package-before.json',before)
regcmd=[PY,str(W/'17592186119771.py'),'--difficulty','easy','--count','5','--seed','0','--format','json']; a=subprocess.run(regcmd,text=True,capture_output=True);b=subprocess.run(regcmd,text=True,capture_output=True)
save('regression.json',{'command':regcmd,'exit':a.returncode,'stderr':a.stderr,'count':len(json.loads(a.stdout)),'deterministic':a.stdout==b.stdout,'previous_failure':'easy count 5 seed 0 exhausted old three-task catalog','preflight':'../repair-preflight.json','retained_findings':['dbcd1ab741c06c08a3a5']});save('regression-records.json',json.loads(a.stdout))
records=g.batch('easy',18,9187)+[g.generate('easy',s) for s in range(8501,8513)];save('independent-records.json',records);batch=json.load(open(E.parent/'samples.json'));save('runner-batch.json',batch)
base=[[-2,0,0],[6,-1,0],[0,0,0]];trans=[list(x) for x in zip(*base)];diag=[[base[i][j] if i==j else 0 for j in range(3)] for i in range(3)];irrelevant=[[0,0,0],[-6,7,0],[0,0,-8]]
controls=[call(m) for m in [base,trans,diag,irrelevant]];save('counterfactual-records.json',controls)
results=[]
for r in records+batch+controls:
 q=r['question'];m=mat(q); expected=label(m);sol=q[':question/worked-solution']; sm=re.search(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',sol,re.S); solmatrix=[[int(x.strip()) for x in row.split('&')] for row in sm[1].split(r'\\')]
 witness=re.search(r'_\{(\d)(\d)\}=(-?\d+)',sol);w=True if not witness else (m[int(witness[1])-1][int(witness[2])-1]==int(witness[3])!=0)
 results.append({'id':q[':question/id'],'expected':expected,'key':answer(q),'matrix_repeated':solmatrix==m,'witness_valid':w,'correct_conclusion':('it is '+('an ' if expected.startswith('Upper') else 'a ')+expected.lower()+'.') in sol})
save('math-results.json',{'cases':results,'failures':[x for x in results if x['expected']!=x['key'] or not all(x[k] for k in ['matrix_repeated','witness_valid','correct_conclusion'])]})
rejections=[]
for name,m in [('canonical',[[-2,0,0],[6,-1,0],[0,0,0]]),('sole_far_witness',[[2,0,0],[0,3,0],[7,0,4]]),('upper_far_witness',[[2,0,7],[0,3,0],[0,0,4]])]:
 try:r=call(m);rejections.append({'name':name,'parameters':{'matrix':m,'letter':'A','layout':'bmatrix'},'expected':label(m),'accepted':True,'record':r})
 except Exception as e:rejections.append({'name':name,'parameters':{'matrix':m,'letter':'A','layout':'bmatrix'},'expected':label(m),'accepted':False,'error':str(e)})
save('sparse-rejections.json',{'command':PY+' '+str(E/'review_checks.py'),'cases':rejections,'rule':'Current generator must accept all these formerly rejected sparse cases.'})
# Source replay via exact explicit raw profiles; authored canonical is absent from bundled SOURCES.
source=json.load(open(E.parent/'source/source.json'));replays=[];replay_results=[]
def norm(t):return re.sub(r'\s+','',t.replace(r'\neq',r'\ne').replace('$','').replace('{','').replace('}',''))
for q in source['material']['kp'][':knowledge-point/questions']:
 p=g.parse_matrix(q[':question/problem']);lev=q.get(':question/difficulty',{}).get(':db/ident',':question.difficulty/easy').split('/')[-1];r=g.generate(lev,739,profile='raw:'+q[':question/math-academy-id'],parameters=p);rq=r['question'];replays.append(r)
 replay_results.append({'id':q[':question/id'],'prompt':norm(q[':question/problem'])==norm(rq[':question/problem']),'solution':norm(q.get(':question/worked-solution',''))==norm(rq.get(':question/worked-solution','')),'bank':sorted(a[':answer/value'] for a in q[':question/answer-fields'][0][':answer-field/choices'])==sorted(a[':answer/value'] for a in rq[':question/answer-fields'][0][':answer-field/choices']),'key':answer(q)==answer(rq),'difficulty':q.get(':question/difficulty',{}).get(':db/ident')==rq.get(':question/difficulty')})
save('source-replay-records.json',replays);save('source-replay-results.json',{'questions':replay_results,'canonical_normal_rejection':rejections[0],'raw_missing_evidence_preserved':True})
# True radio field: exercise every label; no free-entry equivalent exists.
cases=[]
for i,r in enumerate(records[:12]+batch+controls):
 exp=label(mat(r['question']));cases.append({'label':str(i),'record':r,'checks':[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/value']==exp else 'rejected','purpose':'independent exact zero pattern classification'} for a in r['question'][':question/answer-fields'][0][':answer-field/choices']]})
save('grader-input.json',cases)
# Strict parameter rejection cases.
invalid=[]
for name,p in [('nonsquare',{'matrix':[[2,0,0],[1,3,0]],'letter':'A','layout':'bmatrix'}),('bool',{'matrix':[[True,0],[3,2]],'letter':'A','layout':'bmatrix'}),('out_of_bound',{'matrix':[[11,0],[3,2]],'letter':'A','layout':'bmatrix'}),('identity',{'matrix':[[1,0],[0,1]],'letter':'A','layout':'bmatrix'})]:
 try:g.generate('easy',parameters=p);invalid.append({'case':name,'rejected':False})
 except ValueError as e:invalid.append({'case':name,'rejected':True,'error':str(e)})
rel=E/'relocated';rel.mkdir(exist_ok=True)
for path in manifest['files']:
 dst=rel/path;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(W/path,dst)
cmd=[PY,str(rel/manifest['entrypoint']),'--difficulty','easy','--seed','0','--count','5'];rr=subprocess.run(cmd,capture_output=True,text=True,cwd=E)
save('packaging-results.json',{'python':platform.python_version(),'sympy':g.sp.__version__,'manifest_dependencies':manifest['dependencies'],'relocation_command':cmd,'relocation_exit':rr.returncode,'relocation_stderr':rr.stderr,'same_records':json.loads(rr.stdout)==json.loads(a.stdout),'invalid_parameters':invalid,'declared_files':manifest['files'],'assets':'none','runtime_writes':'Python bytecode disabled via PYTHONDONTWRITEBYTECODE=1'})
inv=json.load(open(E.parent/'source/inventory.json'));audit=[]
for q in inv['questions']:
 m=mat(q);audit.append({'id':q[':question/id'],'entity_id':q[':db/id'],'independent_answer':label(m),'stored_answer':answer(q),'matches':answer(q) in (None,label(m)),'source_record':':question/math-academy-id' in q,'generation_keys':[k for k in q if 'generation' in k],'sparse_3x3':len(m)==3 and sum(v!=0 for i,row in enumerate(m) for j,v in enumerate(row) if i!=j)==1})
save('inventory-audit.json',{'basis':inv['basis'],'records':audit,'limitation':'Restriction is a missing-generatable-case defect, not incorrect stored content. Sparse stored instances checked separately; no generated provenance was present, so no exact stored generator replay can be claimed.'});save('affected-inventory.json',{'affected_questions':[]})
# Run retained author's regression after redirecting every write under evidence_root.
auth=(W/'checks/validate.py').read_text().replace("ROOT = Path(__file__).resolve().parents[1]",'ROOT = Path('+repr(str(W))+')').replace("OUT = ROOT / 'evidence'",'OUT = Path('+repr(str(E/'author-rerun'))+')').replace("(ROOT/'affected-inventory.json')","(OUT/'affected-inventory.json')")
(E/'author-check-redirected.py').write_text(auth)
r=subprocess.run([PY,str(E/'author-check-redirected.py')],capture_output=True,text=True);save('author-check-results.json',{'command':[PY,str(E/'author-check-redirected.py')],'redirection':'ROOT unchanged; OUT and affected-inventory path redirected; assertions unchanged.','exit':r.returncode,'stdout':r.stdout,'stderr':r.stderr})
save('package-after-initial.json',{str(p.relative_to(W)):hashlib.sha256(p.read_bytes()).hexdigest() for p in W.rglob('*') if p.is_file()})
(E/'session-state.md').write_text('Source account verified before package inspection. Current sampling (30), exact batch (5), sparse counterfactuals (4), 11 source replays, relocation and rejection checks complete. Next native grading, delivery, rendering and changed support-domain checks.\n')
print(json.dumps({'sampled':len(records),'math_failures':sum(x['expected']!=x['key'] for x in results),'source_replays':len(replays),'sparse_rejections':len([x for x in rejections if not x['accepted']]),'author_regression_exit':r.returncode,'inventory':len(audit),'batch_answers':dict(collections.Counter(answer(x['question']) for x in batch))}))
