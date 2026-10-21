import os,sys,json,re,hashlib,shutil,subprocess,platform,collections,itertools,copy
from pathlib import Path
os.environ['PYTHONDONTWRITEBYTECODE']='1';sys.dont_write_bytecode=True
E=Path(__file__).resolve().parent; J=E.parent; W=J/'workspace';R=Path('/home/jake/Developer/Course_Academy');PY=R/'.venv/bin/python'
def save(n,d): (E/n).write_text(json.dumps(d,indent=2,ensure_ascii=False))
def hashes():return {str(p.relative_to(W)):hashlib.sha256(p.read_bytes()).hexdigest() for p in W.rglob('*') if p.is_file()}
before=hashes();save('package-before.json',before)
sys.path.insert(0,str(W));import importlib.util
spec=importlib.util.spec_from_file_location('audit_candidate',W/'17592186087868.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
import sympy as s
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
x,y,D=s.symbols('x y D')
def expr(t):
 t=t.strip().rstrip('.,').replace('{y}^{′}','D');t=re.sub(r'\{x\}\^\{(\d+)\}',r'x**\1',t);t=t.replace('{','(').replace('}',')').replace('^','**').replace('&','')
 return s.expand(parse_expr(t,local_dict={'x':x,'y':y,'D':D},transformations=standard_transformations+(implicit_multiplication_application,)))
def norm(eq):
 a,b=eq.split('=');z=expr(a)-expr(b);assert z.coeff(D)==1;return s.expand(z)
def keys(r):
 fs=r['question'][':question/answer-fields'];return [next(a[':answer/value']=='true' for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]) for f in fs]
def check(r):
 q=r['question']; fs=q[':question/answer-fields']; ns=[norm(f[':answer-field/key'].strip('$')) for f in fs];target='inhomogeneous' if 'are inhomogeneous?' in q[':question/problem'] else 'homogeneous';want=[(s.simplify(z.subs({y:0,D:0}))!=0)==(target=='inhomogeneous') for z in ns];assert keys(r)==want,(r['generation'],want,keys(r))
 assert len(set(f[':answer-field/key'] for f in fs))==3
 sol=q[':question/worked-solution'];blocks=re.split(r'- (?:First|Next|Finally), we consider the equation',sol)[1:];assert len(blocks)==3
 for b in blocks:
  eqs=[]
  for block in re.findall(r'\$\$(.*?)\$\$',b,re.S):
   block=block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','')
   for eq in block.split(r'\\'):
    if '=' in eq: eqs.append(norm(eq))
  assert eqs and all(s.expand(z-eqs[0])==0 for z in eqs)
  assert any(s.expand(eqs[0]-n)==0 for n in ns)
 conclusion=sol.rsplit('Therefore, the correct answer is ',1)[-1]
 selected=re.findall(r'\$(.*?)\$',conclusion)
 assert set(selected)==set(f[':answer-field/key'].strip('$') for f,v in zip(fs,want) if v)
 return want
src=json.load(open(J/'source/source.json')); sourceqs=src['material']['kp'][':knowledge-point/questions'];replay=[];replay_results=[]
for q in sourceqs:
 name=q[':question/math-academy-id'];level=q[':question/difficulty'][':db/ident'].split('/')[-1];r=g.generate(level,seed=78419,profile='raw_'+name);replay.append(r)
 qq=r['question'];assert qq[':question/problem']==g.normalize_prose(q[':question/problem']);assert qq[':question/worked-solution']==g.normalize_prose(q[':question/worked-solution'])
 for a,b in zip(qq[':question/answer-fields'],q[':question/answer-fields']):
  assert a[':answer-field/key']==g.normalize_prose(b[':answer-field/key']);assert [v[':answer/value'] for v in a[':answer-field/choices']]==[v[':answer/value'] for v in b[':answer-field/choices']]
 assert keys(r)==[f[':answer-field/correct'][':answer/value']=='true' for f in q[':question/answer-fields']];check(r);replay_results.append({'source_id':q[':question/id'],'template':name,'prompt_solution_complete_bank':'exact after shared normalization','passed':True})
save('source-replays.json',replay);save('source-replay-results.json',replay_results)
records=[];profiles=[];invalid=[];randomrows=[]
for level in ['easy','moderate']:
 for roles in g.role_catalog(level):
  bs=iter([-5,4]);cs=iter([-9,8]);p={'a':-9,'n':3,'rhs':[]}
  for role in roles:p['rhs'].append([0,0,0] if role=='zero' else [next(bs),0,0] if role=='move_y' else [0,next(cs),0 if role=='constant_forcing' else 3])
  r=g.generate(level,seed=92317,parameters=p);check(r);records.append(r);profiles.append({'level':level,'roles':roles,'parameters':p,'key':keys(r)})
 for seed in range(683021,683277):
  r=g.generate(level,seed);check(r);assert g.generate(level,seed)==r;records.append(r);randomrows.append({'level':level,'seed':seed,'roles':r['generation']['roles'],'key':keys(r)})
 for name,p in [('cancel',{'a':1,'n':0,'rhs':[[1,0,0],[0,-9,3],[0,0,0]]}),('signed-boundaries',{'a':9,'n':0,'rhs':[[-5,0,0],[0,9,0],[0,-9,3]]})]:
  r=g.generate(level,seed=91377,parameters=p);check(r);records.append(r)
 tests=[('zero_a',{'a':0,'n':1,'rhs':[[1,0,0],[0,1,1],[0,0,0]]}),('duplicate',{'a':1,'n':1,'rhs':[[1,0,0],[1,0,0],[0,1,0]]}),('nonlinear-encoding',{'a':1,'n':1,'rhs':[[1,1,1],[0,1,0],[0,0,0]]}),('too_many_moves',{'a':1,'n':1,'rhs':[[1,0,0],[2,0,0],[3,0,0]]})]
 for name,p in tests:
  try:g.generate(level,seed=1,parameters=p);out='unexpected acceptance'
  except ValueError as e:out=str(e)
  invalid.append({'level':level,'case':name,'parameters':p,'outcome':out});assert out!='unexpected acceptance'
try:g.generate_hard(1);raise AssertionError('hard accepted')
except ValueError:pass
pairs=[]
base={'a':2,'n':1,'rhs':[[1,0,0],[0,3,2],[0,0,0]]}
for level in ['easy','moderate']:
 for name,p in [('base',base),('relevant',{'a':2,'n':1,'rhs':[[1,0,0],[-3,0,0],[0,0,0]]}),('irrelevant',{'a':-9,'n':3,'rhs':[[1,0,0],[0,3,2],[0,0,0]]})]:
  if level=='moderate' and name=='relevant':p={'a':2,'n':1,'rhs':[[1,0,0],[0,3,2],[0,-4,0]]}
  r=g.generate(level,seed=91379,parameters=p);check(r);pairs.append({'level':level,'change':name,'parameters':p,'key':keys(r),'record':r})
for level in ['easy','moderate']:
 group=[p for p in pairs if p['level']==level];assert group[0]['key']!=group[1]['key'];assert group[0]['key']==group[2]['key']
save('counterfactuals.json',pairs);save('counterfactual-records.json',[p['record'] for p in pairs]);save('independent-samples.json',records);save('sampling-results.json',{'profiles':profiles,'fresh_seed_rows':randomrows,'rejections':invalid,'deterministic_replays':512,'math_records':len(records)+len(replay)+len(pairs)})
batch=json.load(open(J/'samples.json'));save('runner-batch.json',batch)
for r in batch:check(r)
# Every tested field gets UI-native boolean answer IDs, with independent truth rather than metadata as oracle.
cases=[]
for i,r in enumerate(records+replay+[p['record'] for p in pairs]+batch):
 want=check(r);checks=[]
 for fi,(f,v) in enumerate(zip(r['question'][':question/answer-fields'],want)):
  for a in f[':answer-field/choices']:checks.append({'field_index':fi,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if (a[':answer/value']=='true')==v else 'rejected','purpose':'independent forcing-identity classification'})
 cases.append({'label':f'independent-{i}','record':r,'checks':checks})
save('grader-input.json',cases)
# UI sample includes source all-selected, cancellation, relevant/irrelevant pairs for both levels.
render=[p['record'] for p in pairs]+[next(r for r in records if r['generation']['parameters']=={'a':1,'n':0,'rhs':[[1,0,0],[0,-9,3],[0,0,0]]}),replay[4],batch[0]];save('render-records.json',render)
inv=json.load(open(J/'source/inventory.json'));save('inventory-inspection.json',{'basis':inv['basis'],'question_count':len(inv['questions']),'questions':[{'id':q.get(':question/id'),'entity_id':q.get(':db/id'),'keys':list(q),'has_generation':bool(q.get('generation') or q.get(':question/generation'))} for q in inv['questions']],'conclusion':'Captured inventory consists of original source questions, not reproduced generated instances. No demonstrated generated defect; source validity checked via exact replay. No claim about later inventory.'});save('affected-inventory.json',{'affected_questions':[]})
manifest=json.load(open(W/'package.json'));dest=E/'relocated';dest.mkdir(exist_ok=True)
for f in manifest['files']:
 to=dest/f;to.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(W/f,to)
run=subprocess.run([str(PY),'-B',str(dest/manifest['entrypoint']),'--difficulty','easy','--seed','683021','--count','5','--format','json'],cwd=E,env={**os.environ,'PYTHONPATH':''},capture_output=True,text=True);assert run.returncode==0,run.stderr;rel=json.loads(run.stdout);assert rel==[g.generate('easy',683021+i) for i in range(5)];save('relocated-records.json',rel)
import importlib.metadata
actual={'python':platform.python_version(),'packages':{p:importlib.metadata.version(p) for p in manifest['dependencies']['packages']}};save('packaging-results.json',{'manifest':manifest,'actual':actual,'exact_dependencies_match':actual==manifest['dependencies'],'relocation_command':run.args,'returncode':run.returncode,'stderr':run.stderr,'deterministic_match':True,'external_outputs':'No assets or external-output generation in live path','hashes_unchanged':hashes()==before});assert actual==manifest['dependencies'];assert hashes()==before
(E/'session-state.md').write_text('Completed independent source replay (12 full banks), all supported role profiles, 512 fresh seeded samples, exact displayed math and solution chains, boundary/rejection and deterministic tests, counterfactual records, inventory inspection, and manifest-only relocation. Next: native grading, actual UI rendering, shared delivery and selection/cue coverage.\n')
print(json.dumps({'records':len(records),'profiles':len(profiles),'grader_cases':len(cases),'render_records':len(render),'dependencies':actual,'package_unchanged':True}))
