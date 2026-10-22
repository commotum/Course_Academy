import sys,json,importlib.util,collections,re,os,subprocess,platform,hashlib,copy
from pathlib import Path
from unittest.mock import patch
sys.dont_write_bytecode=True
E=Path(__file__).resolve().parent;J=E.parent;W=J/'workspace';R=Path('/home/jake/Developer/Course_Academy');PY=R/'.venv/bin/python'
load=lambda p:json.loads(Path(p).read_text())
def save(n,x):(E/n).write_text(json.dumps(x,indent=2,default=str)+'\n')
sys.path.insert(0,str(W));spec=importlib.util.spec_from_file_location('g',W/'17592186119848.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
from review_helpers import matrices,rank,expected,correct
from audit_delivery import info
cat=g.catalog();assert cat==load(E/'prior/catalog.json')
replays=[]
for rec in load(E/'prior/replays.json'):
 sid=rec['generation']['source_id'];params=rec['generation']['parameters'];new=g.generate('easy',rec['generation']['seed'],sid,params,source_replay=True);assert new==rec;replays.append(new)
save('unchanged-construction.json',{'catalog_equal':True,'presentations':len(cat),'semantic_instances':len({x['generation']['mathematical_fingerprint'] for x in cat}),'source_replays_equal':len(replays),'source_replay_evidence':'prior/source-replay.json','independent_math_evidence':'prior/math-results.json','diff':'implementation.diff','rationale':'Only batch allocation and label-shape grouping changed; generated catalog and exact replays identical to prior independent outputs.'})
save('catalog.json',cat)
runs=[];records=[]
for seed,count in [(93827,5),(57209,5),(32843,1),(93827,2),(93827,3),(93827,4),(93827,0),(57209,24),(57209,23)]:
 rs=g.batch('easy',count,seed);assert len(rs)==count;assert rs==g.batch('easy',count,seed);assert len({r['generation']['mathematical_fingerprint'] for r in rs})==count
 name=f'sampler-{seed}-{count}.json';save(name,rs);runs.append({'seed':seed,'count':count,'file':name});records+=rs
old=load(E/'previous-batch.json');ids=[r['question'][':question/id'] for r in old]
def prefix(_rng,rows):
 idx={r['question'][':question/id']:r for r in rows};rows[:]=[idx[k] for k in ids if k in idx]+[r for r in rows if r['question'][':question/id'] not in ids]
with patch.object(g.random.Random,'shuffle',prefix):repaired=g.batch('easy',5,0)
save('exact-prefix-repaired.json',repaired)
# Change one physically displayed candidate at a time, holding all others fixed.
controls=[g.generate('easy',60217,'q-139965',{'matches':m,'assignment':['C','A','B'],'scale':s}) for m,s in [(['A'],2),(['A','C'],2),(['C'],2),(['A','C'],1)]]
ms=[matrices(r['question']) for r in controls]
assert ms[0]['A']==ms[1]['A'] and ms[0]['B']==ms[1]['B'] and ms[0]['C']!=ms[1]['C']
assert ms[2]['C']==ms[1]['C'] and ms[2]['B']==ms[1]['B'] and ms[2]['A']!=ms[1]['A']
assert controls[1]['question'][':question/worked-solution']==controls[3]['question'][':question/worked-solution']
save('counterfactual-records.json',controls)
allrs=load(E/'batch.json')+records+repaired+controls;cases=[];results=[]
for rec in allrs:
 q=rec['question'];rr={k:rank(m) for k,m in matrices(q).items()};errors=[];checks=[]
 for fi,f in enumerate(q[':question/answer-fields']):
  ex=expected(q,f)
  if len(ex)!=1 or ex[0][':answer/id']!=correct(f)[':answer/id']:errors.append('incorrect key')
  for a in f[':answer-field/choices']:checks.append({'field_index':fi,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a in ex else 'rejected','purpose':'Independent Fraction elimination from displayed integer matrices'})
 for lab,val in re.findall(r'\\(?:text|textrm)\{rank\}\(([A-E])\)\s*=\s*(\d+)',q[':question/worked-solution']):
  if int(val)!=rr[lab]:errors.append('stale solution '+lab)
 results.append({'id':q[':question/id'],'ranks':rr,'errors':errors});cases.append({'label':'fresh math and answer control','record':rec,'checks':checks})
# Reusing a response by value across controlled changes tests a stale key in actual grading.
for before,after in [(0,1),(2,1),(1,3)]:
 f0=controls[before]['question'][':question/answer-fields'][0];f1=controls[after]['question'][':question/answer-fields'][0];value=correct(f0)[':answer/value'];choice=next(a for a in f1[':answer-field/choices'] if a[':answer/value']==value)
 cases.append({'label':f'counterfactual response transfer {before}->{after}','record':controls[after],'checks':[{'submitted_answer_id':choice[':answer/id'],'expected':'accepted' if before==1 else 'rejected','purpose':'Response changes after relevant pivot change; preserved after irrelevant scale change'}]})
save('math-results.json',{'records':len(allrs),'failures':[x for x in results if x['errors']],'results':results});assert not any(x['errors'] for x in results)
save('grader-input.json',cases)
# Independent cardinality/label shortcut comparisons by exact visible layout.
def groups(rs):
 out=collections.defaultdict(list)
 for rec in rs:
  x=info(rec);key=(x['profile'],x['target'],tuple((k,tuple(v)) for k,v in sorted(x['shapes'].items())),tuple(x['excluded']),len(rec['question'][':question/answer-fields']),rec['generation']['choice_profile']);out[str(key)].append(x)
 return [{'group':k,'count':len(xs),'truths':[x['matches'] for x in xs],'ids':[x['question_id'] for x in xs],'eligible':xs[0]['eligible']} for k,xs in out.items()]
save('sampler-results.json',{'runs':runs,'groups_by_run':{r['file']:groups(load(E/r['file'])) for r in runs},'current_batch':groups(load(E/'batch.json')),'restored_previous_prefix':groups(repaired)})
rel=E/'relocated';env={k:v for k,v in os.environ.items() if k not in ('PYTHONPATH','PYTHONHOME')};env['PYTHONDONTWRITEBYTECODE']='1';env['TMPDIR']=str(E);env['COURSE_ACADEMY_GENERATOR_OUTPUT_DIR']=str(E/'external-assets')
cmd=[str(PY),'-B',str(rel/'17592186119848.py'),'--seed','32843','--count','5'];a=subprocess.run(cmd,cwd=E,env=env,capture_output=True,text=True);b=subprocess.run(cmd,cwd=E,env=env,capture_output=True,text=True);assert a.returncode==0 and a.stdout==b.stdout;save('relocation-sample.json',json.loads(a.stdout))
pack={'command':cmd,'returncode':a.returncode,'deterministic':a.stdout==b.stdout,'installed':{'python':platform.python_version(),'packages':{'sympy':g.sp.__version__}},'declared':load(W/'package.json')['dependencies'],'boundaries':[]};assert pack['installed']==pack['declared']
for desc,func in [('count25',lambda:g.batch('easy',25,7)),('count-1',lambda:g.batch('easy',-1,7)),('hard',lambda:g.generate('hard',7)),('invalid subset',lambda:g.generate('easy',7,'q-34823',{'matches':['B']}))]:
 try:func();raise AssertionError('invalid input accepted '+desc)
 except ValueError as e:pack['boundaries'].append({'case':desc,'error':str(e)})
runtime=subprocess.run([str(PY),'-B',str(rel/'checks/check_runtime.py')],cwd=E,env=env,capture_output=True,text=True);assert runtime.returncode==0
entry=rel/'17592186119848.py';orig=entry.read_text();entry.write_text('import scripts\n'+orig);bad=subprocess.run([str(PY),'-B',str(rel/'checks/check_runtime.py')],cwd=E,env=env,capture_output=True,text=True);entry.write_text(orig);assert bad.returncode!=0 and 'Undeclared/unresolved runtime import' in bad.stderr
pack['retained_runtime']={'current':runtime.returncode,'stdout':runtime.stdout,'negative_control':bad.returncode,'negative_stderr':bad.stderr};save('packaging-results.json',pack)
save('render-records.json',load(E/'batch.json')+controls)
(E/'session-state.md').write_text('Current catalog39 and ten exact source replays identical to prior independent evidence. Focused fresh sampler, independent math and relocation checks complete. Retained runtime negative control fails as required. Next: retained decision checks, actual delivery, grading and rendering.\n')
print(json.dumps({'catalog_unchanged':len(cat),'replays_unchanged':len(replays),'fresh_runs':len(runs),'math_records':len(allrs),'failures':0,'batch':groups(load(E/'batch.json'))}))
