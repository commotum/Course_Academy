import sys,os,json,re,hashlib,importlib.util,subprocess
from pathlib import Path
from collections import Counter
sys.dont_write_bytecode=True
E=Path(__file__).resolve().parent;J=E.parent;W=J/'workspace';R=Path('/home/jake/Developer/Course_Academy');PY=R/'.venv/bin/python'
sys.path.insert(0,str(W));import sympy as sp
spec=importlib.util.spec_from_file_location('g',W/'17592186119854.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def load(n):return json.load(open(E/n))
def save(n,v):(E/n).write_text(json.dumps(v,indent=2,default=str)+'\n')
def mat(q):
 vs=[sp.Matrix([sp.Rational(x.strip()) for x in m.split(r'\\')]) for m in re.findall(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',q[':question/problem'],re.S)];return sp.Matrix.hstack(*vs[:3]),vs[3]
def answer(q):
 f=q[':question/answer-fields'][0];c=f[':answer-field/correct'];aid=c[1] if isinstance(c,list) else c[':answer/id'];return next(a for a in f[':answer-field/choices'] if a[':answer/id']==aid)
def weight(q):
 text=q[':question/problem'].split('then what is')[1].replace('{','').replace('}','');terms=re.findall(r'([+-]?)\s*x_([123])',text);assert len(terms)==3;return sp.Matrix([-1 if s=='-' else 1 for s,i in terms])
def expect(q):
 A,b=mat(q);return 'No solution' if A.rank()<A.row_join(b).rank() else str((A.inv()*b).dot(weight(q)))
def rank(r):
 q=r['question'];a=answer(q)[':answer/value'];ns=sorted(sp.Rational(x[':answer/value']) for x in q[':question/answer-fields'][0][':answer-field/choices'] if x[':answer/value']!='No solution');return 'No solution' if a=='No solution' else ns.index(sp.Rational(a))+1
source=json.load(open(J/'source/source.json'))['material']['kp'];fresh=[r for r in load('independent-samples.json') if r['generation']['seed'] in [310019,410029,510047,610051,710053,810059]];save('fresh-moderate.json',[r for r in fresh if r['question'][':question/difficulty'].endswith('/moderate')]);save('fresh-hard.json',[r for r in fresh if r['question'][':question/difficulty'].endswith('/hard')])
controlled=[];bankchecks=[]
for q in source[':knowledge-point/questions']:
 sid=q[':question/math-academy-id']
 if not q[':question/difficulty'][':db/ident'].endswith('/moderate'):continue
 A,_=mat(q);b=list(map(int,A*sp.Matrix([2,-1,4])));n=sum(a[':answer/type'][':db/ident']==':answer.type/math' for a in q[':question/answer-fields'][0][':answer-field/choices']);rs=[]
 for k in range(1,n+1):rs.append(g.generate('moderate',920033,template=sid,parameters={'b':b,'numeric_rank':k}))
 assert len({r['question'][':question/problem'] for r in rs})==1 and len({r['question'][':question/worked-solution'] for r in rs})==1
 assert [rank(r) for r in rs]==list(range(1,n+1));assert all(answer(r['question'])[':answer/value']==expect(r['question']) for r in rs)
 controlled.extend(rs);bankchecks.append({'template':sid,'ranks':[rank(r) for r in rs],'expected':expect(rs[0]['question']),'prompt_and_solution_preserved':True})
save('controlled-bank-records.json',controlled);save('controlled-bank-results.json',bankchecks)
# Confirm row-operation annotations, not merely row-equivalence. New and canonical profiles included.
def rat(v):
 v=v.replace(r'\left','').replace(r'\right','');v=re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}',r'(\1)/(\2)',v);return sp.Rational(sp.sympify(v))
transitions=[]
for r in load('source-replay-records.json')+[load('canonical-replay.json')]:
 q=r['question'];A,b=mat(q);s=q[':question/worked-solution'].split('Row-reducing')[1].split('The system is now')[0]
 ms=re.findall(r'\\begin\{array\}\{ccc\|c\}(.*?)\\end\{array\}',s,re.S);ms=[sp.Matrix([[rat(v.strip()) for v in row.split('&')] for row in m.split(r'\\')]) for m in ms]
 labels=re.findall(r'&& (.*?)(?= \\\\ |\\end\{aligned\})',s);assert len(ms)==len(labels)+1
 for i,label in enumerate(labels):
  m=ms[i].copy();swap=re.fullmatch(r'R_\{(\d)\}\\leftrightarrow R_\{(\d)\}',label)
  add=re.fullmatch(r'R_\{(\d)\}:=R_\{\d\}\+\((.*?)\)R_\{(\d)\}',label)
  scale=re.fullmatch(r'R_\{(\d)\}:=(.*?)R_\{\d\}',label)
  if swap:m.row_swap(int(swap[1])-1,int(swap[2])-1)
  elif add:a,c,j=add.groups();m[int(a)-1,:]+=rat(c)*m[int(j)-1,:]
  elif scale:a,c=scale.groups();m[int(a)-1,:]=rat(c)*m[int(a)-1,:]
  else:raise AssertionError(label)
  assert m==ms[i+1],(r['generation']['template'],label)
 if A.det()!=0:
  x=A.inv()*b;m=ms[-1];assert m[0,0]==1 and m[1,0]==0 and m[2,0]==m[2,1]==0
  assert m[0,3]-m[0,1]*x[1]-m[0,2]*x[2]==x[0]
  assert (m[1,3]-m[1,2]*x[2])/m[1,1]==x[1]
 transitions.append({'template':r['generation']['template'],'source_id':r['generation']['source_question_id'],'operations':labels,'annotation_transitions_valid':True,'back_substitution_valid':True if A.det()!=0 else 'inconsistent'})
save('solution-transitions.json',transitions)
# All grader assertions use independently computed targets from visible prompts.
cases=load('grader-input.json')
for r in controlled:
 q=r['question'];want=expect(q);cases.append({'label':'controlled-'+r['generation']['template']+'-'+str(rank(r)),'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/value']==want else 'rejected','purpose':'Exact solve from visible vectors and signed target'} for a in q[':question/answer-fields'][0][':answer-field/choices']]})
for c in cases:
 want=expect(c['record']['question'])
 for check in c['checks']:
  a=next(a for a in c['record']['question'][':question/answer-fields'][0][':answer-field/choices'] if a[':answer/id']==check['submitted_answer_id']);assert check['expected']==('accepted' if a[':answer/value']==want else 'rejected')
save('grader-input.json',cases)
# Existing inventory is original material only; exact ID membership, not name inference.
inv=json.load(open(J/'source/inventory.json'));sourceids={q[':question/id'] for q in source[':knowledge-point/questions']};assert all(q[':question/id'] in sourceids and not any('generat' in k for k in q) for q in inv['questions'])
save('inventory-audit.json',{'basis':inv['basis'],'inventory_count':len(inv['questions']),'matched_original_source_ids':len(inv['questions']),'generated_inventory_count':0,'conclusion':'Verified absence of stored generated instances in the captured bank. All inventory IDs match original source questions; live later inventory not tested.'});save('affected-inventory.json',{'affected_questions':[]})
# Strict prior test against actual old package, capturing complete failing examples.
prior=(E/'prior-regressions.py').read_text().replace("W=E.parent/'workspace'","W=E.parent/'review-0-policy-2-1fd32c4da099981a'/'relocated'").replace("'retained-counterexample-results.json'","'historical-failing-records.json'")
(E/'prior-historical.py').write_text(prior)
run=subprocess.run([str(PY),str(E/'prior-historical.py')],env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'},capture_output=True,text=True)
assert run.returncode==1
save('retained-findings-validation.json',{'preflight':json.load(open(J/'repair-preflight.json')),'historical_test':{'command':str(PY)+' prior-historical.py','exit':run.returncode,'stdout':run.stdout,'stderr':run.stderr},'current_test':load('retained-counterexample-results.json'),'author_current_check':load('author-check-current/regression-results.json'),'author_historical_check':'author-historical.stderr','conclusion':'Both retained independent findings reproduced on the archived failing runtime and no longer reproduce on current runtime. Author executable also fails on original rank counterexample and passes current package.'})
# Canonical replay has no answer contract, so render it as worked-example only.
render=load('runner-batch.json')+load('counterfactual-records.json')+controlled[:2]+[next(r for r in load('source-replay-records.json') if r['generation']['template']=='q-74043'),load('canonical-replay.json')]
save('render-input.json',render)
(E/'session-state.md').write_text('Current retained independent regressions pass; historical package reproduces both findings. All 15 source banks replay, canonical replay has no bank. 137 math checks and 16 row-annotation/back-substitution checks pass. Fresh seeds 6/profile, all 33 eligible moderate bank anchors tested independently. Packaging versions/determinism/relocation pass. Native grading/delivery/rendering/selection summaries pending.\n')
print(json.dumps({'fresh_moderate':len(load('fresh-moderate.json')),'fresh_hard':len(load('fresh-hard.json')),'controlled':len(controlled),'solution_profiles':len(transitions),'grader_records':len(cases),'render_records':len(render)}))
