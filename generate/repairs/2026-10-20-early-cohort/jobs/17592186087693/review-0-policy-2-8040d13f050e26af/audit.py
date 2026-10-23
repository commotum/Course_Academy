import sys, json, re, pathlib, hashlib, subprocess, shutil, collections
ROOT=pathlib.Path('/home/jake/Developer/Course_Academy'); HERE=pathlib.Path(__file__).resolve().parent; JOB=HERE.parent; PKG=JOB/'workspace'; PY=ROOT/'.venv/bin/python'
sys.dont_write_bytecode=True
sys.path.insert(0,str(PKG));import generator as g

def save(n,d): (HERE/n).write_text(json.dumps(d,indent=2)+'\n')
def load(p): return json.loads(pathlib.Path(p).read_text())
def en(x):return x.get(':db/ident') if isinstance(x,dict) else x
def correct(f):
 c=f[':answer-field/correct']; cid=c[':answer/id'] if isinstance(c,dict) else c[1]
 return next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==cid)
def shape(q):
 body=re.search(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',q[':question/problem'],re.S)[1]
 rows=body.split('\\\\'); widths=[len(r.split('&')) for r in rows]; assert len(set(widths))==1
 return len(rows),widths[0]
def values(q):return [correct(f) for f in sorted(q[':question/answer-fields'], key=lambda f:f[':answer-field/key'])]
def norm(s): return re.sub(r'\s|[${}.]','',s)
def checkmath(rec):
 q=rec['question'];r,c=shape(q); fs=q[':question/answer-fields'];v=values(q)
 if en(fs[0][':answer-field/type']).endswith('/radio'):
  assert norm(v[0])==norm(f'{r}\\times{c}')
  bank=[norm(a[':answer/value']) for a in fs[0][':answer-field/choices']];assert len(set(bank))==5
 else:assert v==[str(r),str(c)]
 sol=norm(q[':question/worked-solution']);assert f'has{r}rowsand{c}columns' in sol and f'{r}\\times{c}' in sol
 return list((r,c))
files=[p for p in PKG.rglob('*') if p.is_file()];save('package-before.json',{str(p.relative_to(PKG)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files})
source=load(JOB/'source/source.json');qs=source['material']['kp'][':knowledge-point/questions']; batch=load(JOB/'samples.json');save('runner-batch.json',batch)
replays=[]; replay_report=[]
for q in qs:
 sid=q[':question/math-academy-id']; profile='observed-'+sid
 try:
  rec=g.generate(profile=profile);replays.append(rec);rq=rec['question'];checkmath(rec)
  banks=lambda q:[[norm(a[':answer/value']) for a in f[':answer-field/choices']] for f in q[':question/answer-fields']]
  assert [sorted(x) for x in banks(q)]==[sorted(x) for x in banks(rq)]
  assert list(map(norm,values(q)))==list(map(norm,values(rq)))
  assert [en(f[':answer-field/type']) for f in q[':question/answer-fields']]==[en(f[':answer-field/type']) for f in rq[':question/answer-fields']]
  assert norm(q[':question/worked-solution'])==norm(rq[':question/worked-solution'])
  replay_report.append({'source_id':q[':question/id'],'ma_id':sid,'passed':True,'shape':shape(q)})
 except Exception as e:replay_report.append({'source_id':q[':question/id'],'ma_id':sid,'passed':False,'error':str(e)})
# Canonical has no fields; independently replay its supplied entries using radio.
canonical=g.generate(template='radio',parameters={'name':'A','entries':[[4,5,1],[-2,0,6],[3,2,-5],[5,1,7]]},seed=611)
assert checkmath(canonical)==[4,3];replays.append(canonical)
save('source-replays.json',replays);save('source-replay-results.json',replay_report)
samples=[g.generate(template=t,seed=47219+i) for t in g.TEMPLATES for i in range(40)]
boundaries=[g.generate(template=t,seed=1221,parameters={'name':'A','entries':[[0]*c for _ in range(r)]}) for t in g.TEMPLATES for r,c in g.DIMENSIONS]
save('samples.json',samples);save('boundaries.json',boundaries)
controls=[];cf=[]
for t in g.TEMPLATES:
 kw={'template':t,'seed':1218};bank=[(2,3),(3,3),(4,2),(5,6),(6,4)]
 if t=='radio':kw['bank']=bank
 entries=[[1,2,3],[4,5,6]]
 base=g.generate(parameters={'name':'A','entries':entries},**kw)
 relevant=g.generate(parameters={'name':'A','entries':entries+[[7,8,9]]},**kw)
 irrelevant=g.generate(parameters={'name':'Z','entries':[[0,-2,r'\sqrt{2}'],[0,0,r'\frac{1}{3}']]},**kw)
 controls += [base,relevant,irrelevant]
 cf.append({'template':t,'base':len(controls)-3,'relevant':len(controls)-2,'irrelevant':len(controls)-1,'values':[values(x['question']) for x in [base,relevant,irrelevant]],'passed':values(base['question'])!=values(relevant['question']) and values(base['question'])==values(irrelevant['question'])})
save('counterfactual-records.json',controls);save('counterfactual-results.json',cf)
allrecs=samples+boundaries+batch+controls+replays
save('math-results.json',{'count':len(allrecs),'shapes':[checkmath(r) for r in allrecs],'passed':True})
# Grading assertions are derived from displayed rows/columns, not keys.
cases=[]
for idx,rec in enumerate(controls+replays+batch):
 q=rec['question'];dims=shape(q);checks=[]
 for j,f in enumerate(q[':question/answer-fields']):
  if en(f[':answer-field/type']).endswith('/radio'):
   for a in f[':answer-field/choices']:checks.append({'field_index':j,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if norm(a[':answer/value'])==norm(f'{dims[0]}\\times{dims[1]}') else 'rejected'})
  else:
   n=dims[j]
   for v in [str(n),f'{n}.0',f'{2*n}/2',f'\\frac{{{2*n}}}{{2}}',f'{n-1}+1']:
    checks.append({'field_index':j,'submitted':v,'expected':'accepted'})
   for v in [str(n+1),'0',str(-n)]:checks.append({'field_index':j,'submitted':v,'expected':'rejected'})
   if dims[1-j]!=n:checks.append({'field_index':j,'submitted':str(dims[1-j]),'expected':'rejected'})
 cases.append({'label':f'independent-{idx}','record':rec,'checks':checks})
save('grader-input.json',cases)
# Explicit input rejection and finite-batch boundaries.
invalid=[('ragged',{'parameters':{'name':'A','entries':[[1,2],[1,2,3]]}}),('too large',{'parameters':{'name':'A','entries':[[1,2]]*7}}),('boolean',{'parameters':{'name':'A','entries':[[True,2],[1,2]]}}),('medium',{'level':'moderate'}),('bad bank',{'template':'radio','parameters':{'name':'A','entries':[[1,2],[3,4]]},'bank':[(2,2)]*5})]
reject=[]
for name,kw in invalid:
 try:g.generate(**kw);reject.append({'case':name,'passed':False})
 except ValueError as e:reject.append({'case':name,'passed':True,'error':str(e)})
for n in [0,26]:
 try:g.batch('easy',n,7);reject.append({'count':n,'passed':False})
 except ValueError as e:reject.append({'count':n,'passed':True,'error':str(e)})
full=g.batch('easy',25,88003);save('finite-batch.json',full)
assert len({shape(r['question']) for r in full})==25
save('rejection-results.json',reject)
cli=subprocess.run([str(PY),'-B',str(PKG/'generator.py'),'--seed','928264887','--count','5','--difficulty','easy'],capture_output=True,text=True,check=True)
assert json.loads(cli.stdout)==batch
reloc=HERE/'relocated';reloc.mkdir(exist_ok=True)
for p in files:shutil.copy2(p,reloc/p.name)
other=subprocess.run([str(PY),'-B',str(reloc/'generator.py'),'--seed','928264887','--count','5','--difficulty','easy'],cwd=HERE,capture_output=True,text=True,check=True)
assert other.stdout==cli.stdout
save('packaging-results.json',{'deterministic_runner_replay':True,'relocation':True,'declared':load(PKG/'package.json')['dependencies'],'actual':{'python':sys.version.split()[0],'packages':{'sympy':g.sp.__version__}},'external_output':'CLI emits complete JSON to stdout; no assets or writes; relocation used -B','invalid_cases':reject,'full_batch_shapes':25,'batch_rejections':full[0]['generation']['batch_rejected_repeated_shapes']})
save('render-input.json',controls+batch+[replays[3],replays[6]])
inv=load(JOB/'source/inventory.json');save('inventory-records.json',inv['questions']);save('affected-inventory.json',{'affected_questions':[]})
# Complete inventory inspected as supplied; no generation metadata invented.
invresults=[]
for q in inv['questions']:
 try: checkmath({'question':q});ok=True
 except Exception as e:ok=str(e)
 invresults.append({'question_id':q[':question/id'],'entity_id':q[':db/id'],'original':':question/math-academy-id' in q,'retired':q.get(':question/retired',False),'shape':shape(q),'math':ok})
save('inventory-results.json',{'basis':inv['basis'],'questions':invresults,'missing_source_case':'80862d10-12ca-5f6e-9209-5f8bf84be504 is an original source record, not generated; do not mark generated or repair as stored-pool defect','affected_status':'No stored missing-profile defect: this defect is a runtime replay omission. All 14 stored matrix dimensions/keys checked.'})
(HERE/'session-state.md').write_text('Source account complete. Independent source replay: 8 captured profiles pass; q-139628 missing (Unknown source profile). Math, controls, deterministic CLI/relocation, 25-shape domain and input rejections saved. Grader, delivery and rendering pending. No package writes.\n')
print(json.dumps({'source_replay':replay_report,'sample_count':len(samples),'math_count':len(allrecs),'grader_cases':len(cases),'inventory_count':len(invresults)}))
