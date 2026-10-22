import os,sys,json,re,hashlib,importlib.util,platform,shutil,subprocess
from pathlib import Path
from collections import Counter,defaultdict
os.environ['PYTHONDONTWRITEBYTECODE']='1';sys.dont_write_bytecode=True
E=Path(__file__).resolve().parent; J=E.parent; W=J/'workspace'; R=Path('/home/jake/Developer/Course_Academy'); PY=R/'.venv/bin/python'
sys.path.insert(0,str(W))
import sympy as sp
def save(n,d): (E/n).write_text(json.dumps(d,indent=2,default=str)+'\n')
def hashes():return {str(p.relative_to(W)):hashlib.sha256(p.read_bytes()).hexdigest() for p in W.rglob('*') if p.is_file()}
before=hashes();save('package-hashes-before.json',before)
spec=importlib.util.spec_from_file_location('review_generator',W/'17592186119854.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
src=json.load(open(J/'source/source.json'));inv=json.load(open(J/'source/inventory.json'));batch=json.load(open(J/'samples.json'));save('runner-batch.json',batch)
def rational(v):
 v=re.sub(r'\\(?:d?frac)\{([^{}]+)\}\{([^{}]+)\}',r'(\1)/(\2)',v.strip())
 return sp.Rational(sp.sympify(v))
def matrix(q):
 ms=re.findall(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',q[':question/problem'],re.S)
 vs=[sp.Matrix([sp.Rational(x.strip()) for x in m.split(r'\\')]) for m in ms];return sp.Matrix.hstack(*vs[:3]),vs[3]
def field(q):return q[':question/answer-fields'][0]
def correct(q):
 f=field(q);c=f[':answer-field/correct'];aid=c[':answer/id'] if isinstance(c,dict) else c[1]
 return next(a for a in f[':answer-field/choices'] if a[':answer/id']==aid)
def rank(q):
 a=correct(q);nums=sorted(sp.Rational(x[':answer/value']) for x in field(q)[':answer-field/choices'] if x[':answer/value']!='No solution');return 'No solution' if a[':answer/value']=='No solution' else nums.index(sp.Rational(a[':answer/value']))+1
# Source replay uses current independent capture, not author's old inventory.
replay=[];recs=[]
for q in src['material']['kp'][':knowledge-point/questions']:
 sid=q[':question/math-academy-id'];A,b=matrix(q);c=correct(q)[':answer/value'];expected='No solution' if A.rank()<A.row_join(b).rank() else str((A.inv()*b).dot(sp.Matrix([1,1,-1] if sid=='q-74028' else [1,1,1])))
 row={'source_id':q[':question/id'],'template':sid,'source_answer':c,'independent_answer':expected,'source_answer_correct':c==expected}
 try:
  rec=g.generate(q[':question/difficulty'][':db/ident'].split('/')[-1],901,template=sid,parameters={'b':list(map(int,b))});recs.append(rec)
  row.update(status='passed',complete_bank_match=sorted(a[':answer/value'] for a in field(q)[':answer-field/choices'])==sorted(a[':answer/value'] for a in field(rec['question'])[':answer-field/choices']),answer_match=correct(rec['question'])[':answer/value']==expected)
 except Exception as ex:row.update(status='failed',error=type(ex).__name__+': '+str(ex))
 replay.append(row)
save('source-replay-records.json',recs);save('source-replay.json',replay)
# Four fresh seeds for every supported profile, and integer solution boundaries.
sampled=[]
for sid in sorted(g.CASES):
 for seed in [28619,44027,91909,107071]:sampled.append(g.generate(g.level(sid),seed,template=sid))
 for x in ([[-7,7,-7],[0,0,0],[7,-7,7]] if g.level(sid)=='moderate' else []):
  A,_=matrix(g.CASES[sid]);sampled.append(g.generate('moderate',17,template=sid,parameters={'b':list(map(int,A*sp.Matrix(x)))}))
save('independent-samples.json',sampled)
# Controlled relevant and irrelevant pairs in the recognizable q-73992 template.
sid='q-73992';A,_=matrix(g.CASES[sid]);pairs=[]
for label,x in [('base',[1,2,3]),('relevant',[1,2,4]),('irrelevant',[2,1,3])]:
 rec=g.generate('moderate',613,template=sid,parameters={'b':list(map(int,A*sp.Matrix(x)))});pairs.append(rec)
save('counterfactual-records.json',pairs)
cf=[{'label':label,'x':x,'b':r['generation']['parameters']['b'],'answer':correct(r['question'])[':answer/value'],'numeric_rank':rank(r['question']),'prompt_changed':r['question'][':question/problem']!=pairs[0]['question'][':question/problem'],'solution_changed':r['question'][':question/worked-solution']!=pairs[0]['question'][':question/worked-solution']} for (label,x),r in zip([('base',[1,2,3]),('relevant',[1,2,4]),('irrelevant',[2,1,3])],pairs)]
save('counterfactual-results.json',{'command':str(PY)+' audit.py','cases':cf,'relevant_expected':'6 -> 7','irrelevant_expected':'6 -> 6; changing b by A*(1,-1,0) changes coefficients but preserves the target sum'})
# Independent exact solver reads displayed vectors, target and solution matrices.
mathchecks=[]
for group,rs in [('source',recs),('fresh',sampled),('batch',batch),('pairs',pairs)]:
 for i,r in enumerate(rs):
  q=r['question'];A,b=matrix(q);no=A.rank()<A.row_join(b).rank();target=q[':question/problem'].split('then what is')[1];weights=[1,1,-1] if '- x_{3}' in target or '-x_3' in target else [1,1,1];x=None if no else A.inv()*b;z='No solution' if no else str(x.dot(sp.Matrix(weights)));c=correct(q)[':answer/value'];steps=re.findall(r'\\begin\{array\}\{ccc\|c\}(.*?)\\end\{array\}',q[':question/worked-solution'],re.S);ok=[]
  for m in steps:
   M=sp.Matrix([[rational(v) for v in row.split('&')] for row in m.split(r'\\')]);ok.append(M.rref()[0]==A.row_join(b).rref()[0])
  final=q[':question/worked-solution'].split('Consequently,')[-1] if not no else ''
  final_ok=(('='+z+'.' in final) if not no else 'system has no solution' in q[':question/worked-solution'])
  mathchecks.append({'group':group,'index':i,'question_id':q[':question/id'],'template':r['generation']['template'],'expected':z,'stored':c,'answer_correct':z==c,'numeric_augmented_steps':len(ok),'all_steps_equivalent':all(ok),'final_solution_correct':final_ok,'x':list(x) if x is not None else None})
save('math-results.json',{'command':str(PY)+' audit.py','checks':mathchecks,'failures':[c for c in mathchecks if not all(c[k] for k in ['answer_correct','all_steps_equivalent','final_solution_correct'])]})
# Every authored choice through native grader, plus the shortcut-selected answer.
cases=[]
for group,rs in [('fresh',sampled),('batch',batch),('pair',pairs),('source',recs)]:
 for i,r in enumerate(rs):
  q=r['question'];ca=correct(q)[':answer/id'];cases.append({'label':f'{group}-{i}-{r["generation"]["template"]}','record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==ca else 'rejected','purpose':'Independent exact solver verified target; exercise each selectable response.'} for a in field(q)[':answer-field/choices']]})
save('grader-input.json',cases)
# Scope and observed rank/position outcomes.
coverage={}
for name,rs in [('fresh',sampled),('batch',batch)]:
 out={}
 for sid in sorted(set(r['generation']['template'] for r in rs)):
  rows=[r for r in rs if r['generation']['template']==sid];out[sid]={'n':len(rows),'ranks':dict(Counter(str(rank(r['question'])) for r in rows)),'answers':[correct(r['question'])[':answer/value'] for r in rows],'b':[r['generation']['parameters']['b'] for r in rows]}
 coverage[name]=out
save('coverage.json',coverage)
# Inventory contains only original questions: verify explicit absence of generated metadata.
save('affected-inventory.json',{'affected_questions':[]});save('inventory-audit.json',{'basis':inv['basis'],'total':len(inv['questions']),'original_source_ids':[q[':question/id'] for q in inv['questions']],'generated_records':[q[':question/id'] for q in inv['questions'] if any('generat' in k for k in q)],'conclusion':'All 15 captured inventory questions have original MA source IDs; none is marked generated. Do not apply a generator-family shortcut finding to isolated original questions. Verified no stored generated instances in this captured inventory; future/live inventory untested.'})
# Determinism, invalid requests, explicit bounds, relocation and version contract.
pack={'actual_python':platform.python_version(),'actual_packages':{'sympy':sp.__version__},'manifest_dependencies':json.load(open(W/'package.json'))['dependencies'],'replay_equal':g.generate('moderate',28619)==g.generate('moderate',28619),'invalid':[]}
for args in [('easy',{}),('bogus',{}),('moderate',{'template':'q-34566'}),('hard',{'template':'q-34566','parameters':{'b':[1,2,3]}})]:
 try:g.generate(args[0],9,**args[1]);pack['invalid'].append({'request':args,'rejected':False})
 except Exception as ex:pack['invalid'].append({'request':args,'rejected':True,'error':str(ex)})
rel=E/'relocated';rel.mkdir(exist_ok=True)
for f in json.load(open(W/'package.json'))['files']+['package.json']:
 p=rel/f;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(W/f,p)
p=subprocess.run([str(PY),str(rel/'17592186119854.py'),'--difficulty','moderate','--count','2','--seed','28619'],env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'},capture_output=True,text=True,cwd=E)
pack['relocation_exit']=p.returncode;pack['relocation_stderr']=p.stderr
if p.returncode==0:save('relocated-samples.json',json.loads(p.stdout));pack['relocation_records']=len(json.loads(p.stdout))
save('packaging.json',pack)
save('render-input.json',batch+pairs+[next(r for r in sampled if r['generation']['template']=='q-74046'),next(r for r in sampled if r['generation']['template']=='q-34566')])
save('package-hashes-after.json',hashes());assert hashes()==before
(E/'session-state.md').write_text('Completed source replay attempts (3 missing current families), exact math on generated records, fresh seeds/boundaries, controlled RHS pairs, per-template rank shortcut measurements, inventory audit, determinism/dependencies/relocation. Package hashes unchanged. Next: native grader, delivery, actual UI render and decision report.\n')
print(json.dumps({'supported_profiles':len(g.CASES),'fresh_records':len(sampled),'math_failures':len(json.load(open(E/'math-results.json'))['failures']),'source_failures':[r for r in replay if r['status']=='failed'],'packaging':pack},default=str))
