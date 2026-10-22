import sys
sys.dont_write_bytecode=True
import json,re,hashlib,importlib.util,copy,platform,shutil,subprocess
from pathlib import Path
from fractions import Fraction
ROOT=Path(__file__).resolve().parent
JOB=ROOT.parent
REPO=Path('/home/jake/Developer/Course_Academy')
PKG=JOB/'workspace'
PY=REPO/'.venv/bin/python'
def save(n,d):
 p=ROOT/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def load(n):return json.load(open(n))
def snapshot():return {str(p.relative_to(PKG)):hashlib.sha256(p.read_bytes()).hexdigest() for p in PKG.rglob('*') if p.is_file()}
if not (ROOT/'package-before.json').exists():save('package-before.json',snapshot())
spec=importlib.util.spec_from_file_location('reviewed',PKG/'17592186119805.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
MAT=re.compile(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',re.S)
def scalar(s):
 s=s.strip().replace('\\\\frac','\\frac').replace(' ','');m=re.fullmatch(r'(-?)\\frac\{(-?\d+)\}\{(\d+)\}',s)
 return (-1 if m[1] else 1)*Fraction(int(m[2]),int(m[3])) if m else Fraction(s)
def mats(s):return [[scalar(x) for x in re.split(r'\\\\',v)] for v in MAT.findall(s)]
def key(q):
 f=q[':question/answer-fields'][0];c=f[':answer-field/correct'];cid=c[':answer/id'] if isinstance(c,dict) else c[1] if isinstance(c,list) else c
 return next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==cid)
def solve(q):
 text=q[':question/problem'];a,u,*bs=mats(text);m=re.search(r'if \$(\d+)',text);c=int(m[1]) if m else 1
 minus=bool(re.search(r'\{a\}_\{1\}-[a-z]',text));b=bs[0] if bs else [0]*len(a)
 residual=[(x-c*y)*(-1 if minus else 1) for x,y in zip(b,a)]
 ratios={x/y for x,y in zip(residual,u) if y}
 ans=next(iter(ratios)) if len(ratios)==1 and all(y or x==0 for x,y in zip(residual,u)) else 'No solution'
 return ans,residual
# This strategy uses only the variable label and unordered visible choices, never vectors or generation metadata.
def shortcut(q):
 text=q[':question/problem'];letter=re.search(r'Find \$([a-z])',text)[1]
 choices=q[':question/answer-fields'][0][':answer-field/choices'];numeric=sorted((scalar(a[':answer/value']),a[':answer/value']) for a in choices if a[':answer/value']!='No solution')
 if re.search(r'=0\$',text):return 'No solution','zero-target'
 if letter=='l' and any(a[':answer/value']=='No solution' for a in choices):return next(v for n,v in numeric if n<0),'l-with-No-solution'
 if letter=='l':return numeric[-2][1],'l-numeric-bank'
 if letter=='h':return numeric[-1][1],'h'
 if letter=='m':return numeric[0][1],'m'
 if letter=='k':return numeric[1][1],'k-explicit-target'
 if letter=='j':return next(v for n,v in numeric if n>0),'j-subtraction'
 return None,'unknown'
def stats(records):
 groups={}
 for r in records:
  q=r['question'];prediction,cue=shortcut(q);v=groups.setdefault(cue,{'correct':0,'total':0,'question_ids':[]});v['total']+=1;v['correct']+=prediction==key(q);v['question_ids'].append(q[':question/id'])
 return groups
records=[];domain_report=[]
for level,sids in g.LEVELS.items():
 for sid in sids:
  dom=g.domain(sid)
  domain_report.append({'level':level,'profile':sid,'domain_count':len(dom),'answer_values':sorted({g.render(sid,p)[2] for p in dom}),'varying_a_coordinates':sorted({i for p in dom for i,x in enumerate(p['a']) if x!=g.CASES[sid]['a'][i]}),'correct_slots':sorted({g.render(sid,p)[3].index(g.render(sid,p)[2]) for p in dom})})
  for seed in [11027,84533,230219,330721,984311,1234579]:records.append(g.generate(level,seed,sid))
save('independent-records.json',records)
batch=load(JOB/'samples.json');save('runner-batch.json',batch)
math=[]
for r in records+batch:
 q=r['question'];ans,res=solve(q);stored=key(q);actual=stored if stored=='No solution' else scalar(stored)
 sm=mats(q[':question/worked-solution']);solution_residual=sm[7] if len(sm)>7 else None
 # Ordered source solution has 3 matrices substitution, 3 isolation, 2 residual matrices, plus contradiction pair.
 residual_ok=sm[7]==res
 math.append({'id':q[':question/id'],'independent_answer':str(ans),'stored':stored,'correct':ans==actual,'solution_residual_ok':residual_ok,'bank_distinct':len(set(a[':answer/value'] for a in q[':question/answer-fields'][0][':answer-field/choices']))==5})
save('math-results.json',{'cases':math,'passed':all(x['correct'] and x['solution_residual_ok'] and x['bank_distinct'] for x in math)})
source=load(JOB/'source/source.json');replay=[];replays=[]
for q in source['material']['kp'][':knowledge-point/questions']:
 sid=q[':question/math-academy-id'];entry={'source_id':q[':question/id'],'profile':sid}
 if sid not in g.PROFILES:
  entry.update(status='unavailable',reason='No sampler profile; incomplete unrated source' if not q.get(':question/difficulty') else 'Complete rated source absent from package profile set')
 else:
  level=q[':question/difficulty'][':db/ident'].split('/')[-1];r=g.generate(level,55001,sid,copy.deepcopy(g.CASES[sid]));replays.append(r)
  norm=lambda x:'No solution' if x=='No solution' else str(scalar(x))
  sourcebank=[norm(a[':answer/value']) for a in q[':question/answer-fields'][0][':answer-field/choices']]
  ourbank=[norm(a[':answer/value']) for a in r['question'][':question/answer-fields'][0][':answer-field/choices']]
  entry.update(status='passed' if mats(q[':question/problem'])==mats(r['question'][':question/problem']) and sourcebank==ourbank and norm(key(q))==norm(key(r['question'])) else 'failed',vectors_equal=mats(q[':question/problem'])==mats(r['question'][':question/problem']),banks_equal=sourcebank==ourbank,solution_matrices_equal=mats(q[':question/worked-solution'])==mats(r['question'][':question/worked-solution']),source_bank=sourcebank,replayed_bank=ourbank)
 replay.append(entry)
save('source-replay-records.json',replays);save('source-replay-results.json',replay);save('coverage.json',{'domains':domain_report,'independent_shortcuts':stats(records),'runner_batch_shortcuts':stats(batch),'history_files':'repair-history.json and repair-preflight.json absent'})
# Controlled actual-generator pairs, held vectors/known scalar/profile fixed.
sid='q-34249';base=copy.deepcopy(g.CASES[sid]);changed=copy.deepcopy(base);changed['s']=-3
pair=[g.generate('easy',64193,sid,base),g.generate('easy',64193,sid,changed)]
irrelevant=copy.deepcopy(base);irrelevant['a'][0]+=1
pair.append(g.generate('easy',64193,sid,irrelevant))
save('counterfactual-records.json',pair)
save('counterfactual-results.json',{'relevant':{'change':'s -2 to -3, rebuilding b; a,u,c,letter,profile fixed','expected':['-2','-3'],'actual':[key(r['question']) for r in pair[:2]],'math_verified':[str(solve(r['question'])[0]) for r in pair[:2]],'same_shortcut':[shortcut(r['question']) for r in pair[:2]],'prompts_changed':pair[0]['question'][':question/problem']!=pair[1]['question'][':question/problem'],'solutions_changed':pair[0]['question'][':question/worked-solution']!=pair[1]['question'][':question/worked-solution']},'irrelevant':{'change':'a[0] 9 to 10 with corresponding b[0] +5 (u[0]=0)','expected':'-2','actual':key(pair[2]['question']),'math_verified':str(solve(pair[2]['question'])[0])}})
# Boundary acceptance/rejection including the subtraction known coefficient, which must remain 1.
rejections=[]
for label,level,sid,p in [('zero scalar','easy','q-34249',dict(base,s=0)),('rename unknown','easy','q-34249',dict(base,letter='x')),('subtraction c=2','easy','q-34241',dict(copy.deepcopy(g.CASES['q-34241']),c=2))]:
 try:
  r=g.generate(level,64193,sid,p);ans,_=solve(r['question']);rejections.append({'case':label,'accepted':True,'math_answer':str(ans),'stored':key(r['question']),'parameters':p});save('boundary-'+label.replace(' ','-').replace('=','')+'.json',[r])
 except Exception as e:rejections.append({'case':label,'accepted':False,'exception':type(e).__name__,'parameters':p})
save('rejection-results.json',rejections)
# Reproduce both non-source inventory records by exact current-generator parameters and stable identity.
inv=load(JOB/'source/inventory.json');affected=[];generated=[]
for q in inv['questions']:
 if q.get(':question/math-academy-id'):continue
 a,u,*_=g.vectors(q[':question/problem']);c=int(re.search(r'if \$(\d+)',q[':question/problem'])[1]);p={'a':a,'u':u,'c':c,'s':None,'letter':'k'}
 r=g.generate('moderate',64193,'q-34570',p)
 assert r['question'][':question/id']==q[':question/id']
 assert r['question'][':question/problem']==q[':question/problem']
 assert key(r['question'])==key(q)
 generated.append(r);affected.append({'question_id':q[':question/id'],'entity_id':q[':db/id'],'finding':'Homogeneous template always answers No solution, allowing zero-RHS cue to bypass component consistency.','reproduction':f'PYTHONDONTWRITEBYTECODE=1 {PY} {ROOT}/audit.py (q-34570, seed 64193, parameters '+json.dumps(p,sort_keys=True)+')','evidence_path':'generated-records.json'})
save('generated-records.json',generated);save('affected-inventory.json',{'affected_questions':affected})
# All choices, including vector-blind shortcut actions, through native grader in one batch.
cases=[]
for i,r in enumerate(records+batch+pair+generated):
 ans=solve(r['question'])[0];f=r['question'][':question/answer-fields'][0];checks=[]
 for a in f[':answer-field/choices']:
  val=a[':answer/value'];correct=(val==ans if val=='No solution' else scalar(val)==ans)
  checks.append({'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if correct else 'rejected','purpose':'Independent componentwise answer, all choices tested; radio has no typed equivalent-notation contract.'})
 cases.append({'label':f'independent-{i}', 'record':r,'checks':checks})
save('grader-input.json',cases)
render=batch+pair+[next(r for r in records if r['generation']['bank_profile']==sid) for sid in ['q-34241','q-34570','q-34602','q-73923']]
save('render-records.json',render)
# Runtime, deterministic replay and relocation; copy only runtime essentials beneath evidence root.
manifest=load(PKG/'package.json');reloc=ROOT/'relocated';reloc.mkdir(exist_ok=True);shutil.copy2(PKG/'17592186119805.py',reloc/'17592186119805.py');target=reloc/'17592186119805/reference';target.mkdir(parents=True,exist_ok=True);shutil.copy2(PKG/'17592186119805/reference/source.json',target/'source.json')
cmd=[str(PY),str(reloc/'17592186119805.py'),'--difficulty','easy','--seed','4201007','--count','5'];result=subprocess.run(cmd,capture_output=True,text=True,env={**__import__('os').environ,'PYTHONDONTWRITEBYTECODE':'1'});relocated=json.loads(result.stdout);save('relocated-records.json',relocated)
control=g.batch('easy',5,4201007)
save('packaging-results.json',{'command':cmd,'manifest_dependencies':manifest['dependencies'],'actual_dependencies':{'python':platform.python_version(),'packages':{'sympy':g.sp.__version__}},'versions_match':manifest['dependencies']=={'python':platform.python_version(),'packages':{'sympy':g.sp.__version__}},'relocation_exit':result.returncode,'relocation_matches':relocated==control,'deterministic':g.batch('easy',5,4201007)==control,'package_unchanged':snapshot()==load(ROOT/'package-before.json')})
(ROOT/'session-state.md').write_text('Independent source reconstruction, 54 fresh samples, 5 exact runner records, 9 source replays, counterfactuals, boundary checks, inventory reproduction and packaging checks complete. Pending delivery/native grading/rendering and final report. All writes under evidence root.\n')
print(json.dumps({'samples':len(records),'math_passed':all(x['correct'] and x['solution_residual_ok'] for x in math),'replay':{s:sum(x['status']==s for x in replay) for s in ['passed','failed','unavailable']},'domains':domain_report,'batch_shortcuts':stats(batch),'rejections':rejections,'affected_inventory':len(affected),'relocated':result.returncode}))
