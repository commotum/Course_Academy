import json,re,sys,hashlib,importlib.util,copy,platform,subprocess,shutil
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
ROOT=Path(__file__).resolve().parent
JOB=ROOT.parent
REPO=Path('/home/jake/Developer/Course_Academy')
PACKAGE=JOB/'workspace'
sys.dont_write_bytecode=True

def save(name,obj):
 (ROOT/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False,default=str))
def load(p):return json.loads(Path(p).read_text())
def hashpkg():return {str(p.relative_to(PACKAGE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in PACKAGE.rglob('*') if p.is_file()}
save('package-before.json',hashpkg())
spec=importlib.util.spec_from_file_location('reviewed_generator',PACKAGE/'17592186096669.py'); g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
x,y,z=sp.symbols('x y z')
def expr(s):
 s=s.strip().replace(' ','').replace('⟨','').replace('⟩','')
 s=re.sub(r'\\(?:d?frac)\{(-?\d+)\}\{(\d+)\}',r'(\1/\2)',s)
 for a,b in [('{x}_{1}','x'),('{x}_{2}','y'),('{x}_{3}','z'),('x_{1}','x'),('x_{2}','y'),('x_{3}','z')]:s=s.replace(a,b)
 s=s.replace(r'\left','').replace(r'\right','').replace(r'\,','').rstrip('.')
 return parse_expr(s,local_dict={'x':x,'y':y,'z':z},transformations=standard_transformations+(implicit_multiplication_application,),evaluate=True)
def vec(s):
 if s.startswith('\\\\begin') or s.startswith('⟨') and '\\\\frac' in s:s=s.replace('\\\\','\\')
 if s.startswith('⟨'):parts=s[1:-1].split(',')
 else:parts=s.removeprefix(r'\begin{bmatrix}').removesuffix(r'\end{bmatrix}').split(r'\\')
 return tuple(expr(a) for a in parts)
def equations(q):
 body=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',q[':question/problem'],re.S)[1]
 return [expr(a)-expr(b) for a,b in (row.replace('&','').split('=') for row in body.split(r'\\'))]
def inspect(r):
 q=r['question'];f=q[':question/answer-fields'][0];eq=equations(q);sol=sp.solve(eq,(x,y,z));v=tuple(sol[t] for t in (x,y,z));bank=[vec(a[':answer/value']) for a in f[':answer-field/choices']];correct=f[':answer-field/correct'];cid=correct[1] if isinstance(correct,list) else correct[':answer/id'];idx=next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==cid)
 assert len(set(bank))==5 and bank.count(v)==1 and bank[idx]==v,(q[':question/id'],v,bank)
 # Independently evaluate every equality in the generated two displayed substitution chains.
 chains=[]
 for block in re.findall(r'\$\$(.*?)\$\$',q.get(':question/worked-solution',''),re.S):
  for chain in block.split('⟹'):
   chain=chain.replace(r'\,','').strip()
   terms=chain.split('=')
   if len(terms)<2:continue
   vals=[sp.simplify(expr(t).subs(sol)) for t in terms]
   assert len(set(vals))==1,(q[':question/id'],chain,vals)
   chains.append(chain)
 return {'id':q[':question/id'],'profile':r.get('generation',{}).get('profile'),'solution':list(map(str,v)),'bank':[list(map(str,a)) for a in bank],'correct_index':idx,'equations':list(map(str,eq)),'checked_solution_chains':chains}
source=load(JOB/'source/source.json');sourceqs=source['material']['kp'][':knowledge-point/questions'];sq={q[':question/math-academy-id']:q for q in sourceqs}
records=[g.generate(seed=73421,profile=p,scale=k) for p in g.PARAMETERS for k in (1,4,9)]
save('samples.json',records);batch=load(JOB/'samples.json');save('batch.json',batch)
replay=[]
for p,q in sq.items():
 if p not in g.PARAMETERS:
  try:g.generate(seed=73421,profile=p,scale=1)
  except Exception as e:replay.append({'profile':p,'source_id':q[':question/id'],'supported':False,'error':repr(e),'complete_source':':question/worked-solution' in q})
  continue
 r=g.generate(seed=73421,profile=p,scale=1);origbank=[vec(c[':answer/value']) for c in q[':question/answer-fields'][0][':answer-field/choices']];newbank=[vec(c[':answer/value']) for c in r['question'][':question/answer-fields'][0][':answer-field/choices']]
 assert equations(q)==equations(r['question']) and origbank==newbank
 replay.append({'profile':p,'source_id':q[':question/id'],'supported':True,'prompt_equations_equal':True,'complete_bank_equal':True,'math':inspect(r)})
save('source-replay.json',replay)
# Real constructor controls: RHS scaling changes all solution coordinates; variable notation changes none.
base=g.generate(seed=73421,profile='q-10195',scale=1);changed=g.generate(seed=73421,profile='q-10195',scale=4)
old=g.QUESTIONS['q-10195'];g.QUESTIONS['q-10195']=copy.deepcopy(old)
g.QUESTIONS['q-10195'][':question/problem']=re.sub(r'\b[xyz]\b',lambda m:{'x':'{x}_{1}','y':'{x}_{2}','z':'{x}_{3}'}[m[0]],old[':question/problem'])
renamed=g.generate(seed=73421,profile='q-10195',scale=1);g.QUESTIONS['q-10195']=old
pairs=[base,changed,renamed];save('counterfactual-records.json',pairs)
assert inspect(base)['solution']==inspect(renamed)['solution']
assert all(sp.Rational(b)==4*sp.Rational(a) for a,b in zip(inspect(base)['solution'],inspect(changed)['solution']))
assert base['question'][':question/problem']!=renamed['question'][':question/problem']
# A legitimate local RHS perturbation is outside the authored construction domain.
oldparam=g.PARAMETERS['q-10195'];g.PARAMETERS['q-10195']=(*oldparam[:3],'3','1','2')
try:g.generate(seed=73421,profile='q-10195',scale=1);restriction='unexpectedly accepted'
except Exception as e:restriction=type(e).__name__
g.PARAMETERS['q-10195']=oldparam
save('counterfactual-results.json',{'relevant':{'before':inspect(base),'after':inspect(changed),'expected':'solution multiplied by 4','passed':True},'irrelevant':{'before':inspect(base),'after':inspect(renamed),'expected':'renaming variables preserves ordered solution','passed':True},'local_rhs_probe':{'source_profile':'q-10195','change':'c=1/2 to c=3, e=1 and f=2 unchanged','expected_solution':['2','-1','2'],'construction_result':restriction,'method':'In-memory PARAMETERS override only; package files unchanged. Author must derive banks for independently varied RHSs.'}})
save('math-results.json',{'samples':[inspect(r) for r in records],'batch':[inspect(r) for r in batch],'counterfactuals':[inspect(r) for r in pairs]})
cases=[]
for label,rs in [('sample',records),('batch',batch),('counterfactual',pairs)]:
 for i,r in enumerate(rs):
  info=inspect(r);f=r['question'][':question/answer-fields'][0]
  cases.append({'label':f'{label}-{i}','record':r,'checks':[{'field_index':0,'submitted_answer_id':c[':answer/id'],'expected':'accepted' if j==info['correct_index'] else 'rejected','purpose':'Independent exact equation solution; check every radio option'} for j,c in enumerate(f[':answer-field/choices'])]})
save('grader-input.json',cases)
# Inventory contains only original source questions; do not classify them as generated.
inv=load(JOB/'source/inventory.json');sourceids={q[':question/id'] for q in sourceqs}
save('inventory-review.json',{'basis':inv['basis'],'question_count':len(inv['questions']),'all_original_source_ids':all(q[':question/id'] in sourceids for q in inv['questions']),'generated_record_count':sum(q[':question/id'] not in sourceids for q in inv['questions']),'questions':[{'id':q[':question/id'],'entity_id':q[':db/id'],'original_source':q[':question/id'] in sourceids,'generation_keys':[k for k in q if 'generat' in k],'retirement_keys':[k for k in q if 'retir' in k]} for q in inv['questions']],'conclusion':'No historical generated records in captured inventory; original instructional sources are not eligible for generated-pool repair.'})
save('affected-inventory.json',{'affected_questions':[]})
# Determinism, relocation, boundaries, dependencies; no runtime output files requested or created.
rel=ROOT/'relocated';rel.mkdir(exist_ok=True);shutil.copy2(PACKAGE/'17592186096669.py',rel/'17592186096669.py');(rel/'17592186096669').mkdir(exist_ok=True);shutil.copy2(PACKAGE/'17592186096669/source.json',rel/'17592186096669/source.json')
cmd=[sys.executable,str(rel/'17592186096669.py'),'--seed','73421','--count','5'];one=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True);two=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True)
save('relocated-records.json',json.loads(one.stdout));original=subprocess.run([sys.executable,str(PACKAGE/'17592186096669.py'),'--seed','73421','--count','5'],cwd=ROOT,text=True,capture_output=True)
bounds=[]
for args in [['--scale','0'],['--scale','10'],['--count','100'],['--difficulty','hard'],['--count','0']]:
 r=subprocess.run([sys.executable,str(rel/'17592186096669.py'),*args],cwd=ROOT,text=True,capture_output=True);bounds.append({'args':args,'exit':r.returncode,'stderr':r.stderr[-650:]})
save('packaging-results.json',{'python':platform.python_version(),'sympy':sp.__version__,'manifest_dependencies':load(PACKAGE/'package.json')['dependencies'],'deterministic':one.stdout==two.stdout,'relocated_matches_original':one.stdout==original.stdout,'commands':cmd,'boundary_rejections':bounds,'external_outputs':'None; generator emits JSON on stdout and reads adjacent source.json.','package_unchanged':hashpkg()==load(ROOT/'package-before.json'),'history_files':{'repair_history':(JOB/'repair-history.json').exists(),'repair_preflight':(JOB/'repair-preflight.json').exists()}})
save('render-records.json',[records[0],records[6],records[24],*batch,*pairs])
(ROOT/'session-state.md').write_text('Source analysis complete before author inspection. Independent source replay: 11 supported, q-20450 missing, q-20451 incomplete. Exact math checked for 33 samples, 5 batch records, and 3 counterfactual records. Native grading and actual UI render inputs saved. Inventory basis 5578 has 13 original sources, zero generated records. Package hashes saved.\n')
print(json.dumps({'samples':len(records),'batch':len(batch),'source_replay_missing':[r for r in replay if not r['supported']],'math':'passed','packaging':load(ROOT/'packaging-results.json')},indent=2))
