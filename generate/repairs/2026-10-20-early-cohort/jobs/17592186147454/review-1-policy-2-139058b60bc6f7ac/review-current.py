"""Read-only independent revision audit: PYTHONDONTWRITEBYTECODE=1 <job python> review-current.py"""
import sys,pathlib,json,hashlib,importlib.util,subprocess,shutil,re,copy,os
from collections import Counter
E=pathlib.Path(__file__).resolve().parent;J=E.parent;R=pathlib.Path('/home/jake/Developer/Course_Academy');W=J/'workspace';sys.dont_write_bytecode=True;sys.path.insert(0,str(E/'deps'))
import sympy as S
from independent_math import solve_check,parse,linear_residual,x,y,C,D

def save(n,v):(E/n).write_text(json.dumps(v,indent=2,default=str)+'\n')
def load(p):return json.loads(p.read_text())
def module(p):
 spec=importlib.util.spec_from_file_location('g'+hashlib.md5(str(p).encode()).hexdigest(),p);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g);return g
def field(r):return r['question'][':question/answer-fields'][0]
def key(r):return field(r)[':answer-field/correct'][1]
def normalize(v):return v.replace(r'\left','').replace(r'\right','')
def keyval(r):return next(a[':answer/value'] for a in field(r)[':answer-field/choices'] if a[':answer/id']==key(r))
g=module(W/'17592186147454.py');old=module(J/'review-0-policy-2-6ca8b422a4136178/relocated/17592186147454.py')
# Retained failures must fail against the previous construction, not just pass new tests.
def oldcue(r):
 vals=[a for a in field(r)[':answer-field/choices'] if re.search(r'C\s*-\s*2',a[':answer/value']) and ('5/2' in a[':answer/value'] or r'\frac{5}{2}' in a[':answer/value'])]
 return len(vals)==1 and vals[0][':answer/id']==key(r)
oldrecords=[old.generate('moderate',98301,'q-109154',{'shift':h}) for h in old.SHIFTS]
oldrestriction=False
try:old.generate('moderate',0,'q-109029',{'shift':1})
except AssertionError:oldrestriction=True
assert all(oldcue(r) for r in oldrecords) and oldrestriction
save('prior-failing-examples.json',oldrecords)
source=load(J/'source/source.json');replays=[];replay=[]
for q in source['material']['kp'][':knowledge-point/questions']:
 t=q[':question/math-academy-id'];sf=q[':question/answer-fields'][0]
 if not q.get(':question/worked-solution') or not sf.get(':answer-field/correct'):
  replay.append({'source_id':q[':question/id'],'template':t,'status':'unsupported','reason':'Captured key and worked solution absent; all five choices invalid by prior independent exact residuals.'});continue
 level=q[':question/difficulty'][':db/ident'].split('/')[-1];r=g.generate(level,612879,t,{'shift':0});replays.append(r);f=field(r)
 assert r['question'][':question/problem']==q[':question/problem']
 assert normalize(r['question'][':question/worked-solution'])==normalize(q[':question/worked-solution'])
 assert sorted(normalize(a[':answer/value']) for a in f[':answer-field/choices'])==sorted(normalize(a[':answer/value']) for a in sf[':answer-field/choices'])
 assert normalize(keyval(r))==normalize(sf[':answer-field/correct'][':answer/value'])
 replay.append({'source_id':q[':question/id'],'template':t,'status':'passed','full_prompt_solution_bank_key':True})
save('source-replays.json',replays);save('source-replay-results.json',replay)
# Controlled fixed banks permit every answer-bearing role to change without changing the bank.
controlled=[];relations=[]
for t in g.FAMILIES:
 level=g.SOURCES[t][':question/difficulty'][':db/ident'].split('/')[-1];a=2 if t=='q-109172' else 1
 bank=[[a,-2],[a,1],[a,3],[a+1,-1],[a+2,2]]
 rr=[g.generate(level,612879,t,{'shift':-6,'bank':bank,'target':i}) for i in range(5)]
 assert len({tuple(sorted(a[':answer/value'] for a in field(r)[':answer-field/choices'])) for r in rr})==1
 assert len({keyval(r) for r in rr})==5
 irrelevant=g.generate(level,799367,t,rr[0]['generation']['parameters']);assert irrelevant['question']==rr[0]['question']
 controlled+=rr;relations.append({'template':t,'fixed_bank':bank,'five_distinct_keys_prompts_solutions':all(len({r['question'][k] for r in rr})==5 for k in [':question/problem',':question/worked-solution']), 'irrelevant_seed_equal':True})
normal=[g.generate('moderate',s) for s in range(61783,61801)]+[g.generate('hard',s) for s in range(72679,72683)]
focused=[g.generate('moderate',98301,'q-109154',{'shift':h}) for h in g.SHIFTS]
scaled=[g.generate('moderate',98301,'q-109154',{'shift':1,'q_scale':b}) for b in (1,2)]
auto=g.generate('moderate',0,'q-109029',{'shift':1})
assert not all(oldcue(r) for r in focused) and any(r['generation']['template']=='q-109029' for r in normal)
save('retained-regression-results.json',{'old_shortcut':{'correct':sum(map(oldcue,oldrecords)),'total':len(oldrecords),'acceptance_failed':True},'old_autonomous_rejected':oldrestriction,'current_shortcut':{'correct':sum(map(oldcue,focused)),'total':len(focused)},'current_autonomous_generated':auto['question'][':question/id'],'ordinary_autonomous':sum(r['generation']['template']=='q-109029' for r in normal),'controlled':relations})
batch=load(J/'samples.json');save('batch.json',batch);save('controlled-records.json',controlled);save('ordinary-records.json',normal);save('focused-records.json',focused);save('scaled-records.json',scaled);save('autonomous-record.json',[auto])
allrecords=replays+controlled+normal+scaled+[auto]+batch
math=[];fail=[]
for i,r in enumerate(allrecords):
 q=r['question'];h=r['generation']['parameters']['shift'];f=field(r)
 try:
  result=copy.deepcopy(solve_check(q[':question/problem'],tuple(a[':answer/value'] for a in f[':answer-field/choices']),h))
  valid=[a['is_solution'] for a in result['choices']];expected=[a[':answer/id']==key(r) for a in f[':answer-field/choices']]
  assert valid==expected,{'valid':valid,'key':expected}
  if not r['generation']['evidence_only']:
   sol=q[':question/worked-solution'];ztext=re.search(r'\$\$z=([\s\S]*?)\$\$',sol)[1]
   z=parse(ztext).subs(x,x-h);assert linear_residual(z,S.sympify(result['p'],locals={'x':x}),S.sympify(result['q'],locals={'x':x}),S.sympify(result['n']))==0
   final=re.search(r'\$\$y=([\s\S]*?)\$\$',sol)[1].rstrip('.')
   assert final==keyval(r).split('=',1)[1]
  result.update({'question_id':q[':question/id'],'template':r['generation']['template'],'passed':True});math.append(result)
 except Exception as ex:
  fail.append({'index':i,'question_id':q[':question/id'],'generation':r['generation'],'error':repr(ex)})
 if i%10==0:save('math-results.json',{'tested':len(math),'failures':fail,'cases':math});print('math',i+1,'failures',len(fail),flush=True)
save('math-results.json',{'tested':len(math),'failures':fail,'cases':math,'method':'Prior independent reviewer parser, exact Bernoulli transformed residual for every displayed choice, unique-key check; derived z and final answer checked from solution. Positive-base restrictions applied for fractional powers.'})
save('math-records.json',allrecords)
# Explicit replay and CLI relocation/determinism, bounded parameter rejection.
rel=E/'relocated';(rel/'17592186147454').mkdir(parents=True,exist_ok=True)
for n in ['17592186147454.py','17592186147454/source.json','requirements.txt']:shutil.copyfile(W/n,rel/n)
cmd=[str(R/'.venv/bin/python'),str(rel/'17592186147454.py'),'--difficulty','moderate','--seed','61783','--count','5']
p=subprocess.run(cmd,capture_output=True,text=True,cwd=E);p2=subprocess.run(cmd,capture_output=True,text=True,cwd=E)
assert p.returncode==0 and p.stdout==p2.stdout
save('relocation-records.json',json.loads(p.stdout));rejections=[]
for kwargs in [dict(difficulty='easy'),dict(difficulty='moderate',template='q-109154',parameters={'shift':7}),dict(difficulty='moderate',template='q-109154',parameters={'target':5}),dict(difficulty='moderate',template='q-109154',parameters={'a':0}),dict(difficulty='hard',template='q-106074'),dict(difficulty='moderate',template='q-109154',parameters={'bank':[[1,1]]*5})]:
 try:g.generate(**kwargs)
 except (ValueError,AssertionError) as ex:rejections.append({'kwargs':kwargs,'rejected':type(ex).__name__})
 else:raise AssertionError(kwargs)
manifest=load(W/'package.json');installed={'python':sys.version.split()[0],'packages':{'sympy':S.__version__}};assert manifest['dependencies']==installed
save('packaging-results.json',{'command':cmd,'deterministic_relocation':True,'stdout_record_count':len(json.loads(p.stdout)),'rejections':rejections,'installed':installed,'declared':manifest['dependencies'],'all_manifest_files_exist':all((W/n).is_file() for n in manifest['files']),'runtime_dependencies':'sympy plus standard library; antlr4 reviewer-only. Relative snapshot retained. No asset output or other external-output handles.','cli_resampling':'Seeds seed..seed+999; duplicate template/complete parameter tuples skipped. Explicit malformed parameters rejected; no hidden math rejection. Full bank/target/a/b/shift retained in generation metadata.'})
# Batch complete banks into a single native invocation, including both sides of counterfactuals.
cases=[]
for i,r in enumerate(allrecords+focused):
 cases.append({'label':str(i)+':'+r['question'][':question/id'],'record':r,'checks':[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==key(r) else 'rejected','purpose':'Full radio bank independently checked by exact ODE residual'} for a in field(r)[':answer-field/choices']]})
save('grader-input.json',cases)
cmd=[str(R/'generate/runs/current/check-engine'),str(E/'grader-input.json'),str(E/'grader-report.json')];p=subprocess.run(cmd,capture_output=True,text=True);save('grader-execution.json',{'command':cmd,'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr});assert p.returncode==0
save('counterfactual-results.json',{'controlled':relations,'relevant':'For each of 10 recognizable profiles, five coefficient targets with a fixed formula bank each produce a distinct prompt, worked solution, and correct formula; all full banks tested by native grader and independent residuals.','irrelevant':'Changing only seed on fully specified instance leaves complete question equal for each profile.','scaled_q':'q_scale=1 and 2 both emitted with distinct correct formulas and native outcomes; scaled-records.json.','native_grader_exit_code':p.returncode})
(E/'session-state.md').write_text('Source replays, retained old failure witnesses, current regression construction, independent exact math, native bank grading, runtime dependency and relocation checks completed. Delivery, UI, conditional shortcut probes and inventory remain.\n')
print(json.dumps({'math_tested':len(math),'math_failures':fail,'native_exit':p.returncode,'ordinary_templates':dict(Counter(r['generation']['template'] for r in normal))}),flush=True)
