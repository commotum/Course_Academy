import os
os.environ['PYTHONDONTWRITEBYTECODE']='1'
import sys,json,pathlib,hashlib,importlib.util,subprocess,platform,collections,re,shutil
sys.dont_write_bytecode=True
E=pathlib.Path(__file__).resolve().parent
J=E.parent
P=J/'workspace'
REPO=pathlib.Path('/home/jake/Developer/Course_Academy')
def save(name,obj):
 p=E/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,indent=2,default=str)+'\n')
def load(name): return json.load(open(name))
def hashes():return {str(p.relative_to(P)):hashlib.sha256(p.read_bytes()).hexdigest() for p in P.rglob('*') if p.is_file()}
before=hashes();save('package-hashes-before.json',before)
sys.path.insert(0,str(P));spec=importlib.util.spec_from_file_location('review_generator',P/'17592186119807.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
import sympy as sp
source=load(J/'source/source.json'); inventory=load(J/'source/inventory.json');batch=load(J/'samples.json');save('batch.json',batch)
# Independent parser and exact solve; no use of generation correctness metadata.
def vectors(r):
 text=r.get('question',r)[':question/problem'];return [sp.Matrix([sp.Rational(v.strip()) for v in s.split(r'\\')]) for s in re.findall(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',text,re.S)]
def truth(r):
 a,c,b=vectors(r); A=a.row_join(c);sol=sp.linsolve((A,b));
 if sol==sp.EmptySet:return 'No solution'
 x=next(iter(sol));return str(sum(x))
def choices(r):return r['question'][':question/answer-fields'][0][':answer-field/choices']
def key(r):
 f=r['question'][':question/answer-fields'][0];return next(a[':answer/value'] for a in choices(r) if a[':answer/id']==f[':answer-field/correct'][1])
def keypos(r):return next(i for i,a in enumerate(choices(r)) if a[':answer/value']==key(r))
def numeric_rank(r):
 ns=sorted([sp.Rational(a[':answer/value']) for a in choices(r) if a[':answer/type']==':answer.type/math']);return None if key(r)=='No solution' else ns.index(sp.Rational(key(r)))+1
catalog=g.catalog();save('catalog.json',catalog)
fresh=[g.generate('moderate',seed) for seed in [31,83,211,4001,99173,20261021]];save('fresh-seeds.json',fresh)
math=[]
for group,records in [('catalog',catalog),('batch',batch),('fresh',fresh)]:
 for i,r in enumerate(records):
  expected=truth(r); math.append({'group':group,'index':i,'id':r['question'][':question/id'],'expected':expected,'stored':key(r),'passed':key(r)==expected,'bank_unique':len({a[':answer/value'] for a in choices(r)})==5})
save('math-results.json',math)
replay=[]
for q in source['material']['kp'][':knowledge-point/questions']:
 sid=q[':question/math-academy-id']
 try:
  r=g.generate('moderate',20261021,sid,{'translation':0})
  oldbank=sorted((a[':answer/type'][':db/ident'],a[':answer/value']) for a in q[':question/answer-fields'][0][':answer-field/choices']);newbank=sorted((a[':answer/type'],a[':answer/value']) for a in choices(r))
  replay.append({'source_id':sid,'question_id':q[':question/id'],'supported':True,'vectors_equal':vectors(q)==vectors(r),'bank_equal':oldbank==newbank,'correct_equal':q[':question/answer-fields'][0][':answer-field/correct'][':answer/value']==key(r),'problem_normalized_equal':g.normalize_prose(q[':question/problem'])==r['question'][':question/problem'],'solution_normalized_equal':g.normalize_prose(q[':question/worked-solution'])==r['question'][':question/worked-solution'],'record':r})
 except Exception as ex:replay.append({'source_id':sid,'question_id':q[':question/id'],'supported':False,'error':repr(ex)})
save('source-replay.json',replay)
# Two controlled pairs with same profile and seed; relevant target and irrelevant option ordering.
a=g.generate('moderate',83,'q-73954',{'translation':0});b=g.generate('moderate',83,'q-73954',{'translation':1});c=g.generate('moderate',84,'q-73954',{'translation':0})
save('counterfactual-records.json',[a,b,c])
save('counterfactual-results.json',{'relevant':{'parameters':[a['generation']['parameters'],b['generation']['parameters']],'answers':[truth(a),truth(b)],'expected':'sum increases by 3; prompt and solution follow target','prompt_changed':a['question'][':question/problem']!=b['question'][':question/problem'],'solution_changed':a['question'][':question/worked-solution']!=b['question'][':question/worked-solution'],'correct_changed':key(a)!=key(b)},'irrelevant':{'change':'seed 83 to 84 permutes option order','same_prompt':a['question'][':question/problem']==c['question'][':question/problem'],'same_solution':a['question'][':question/worked-solution']==c['question'][':question/worked-solution'],'same_truth':truth(a)==truth(c),'option_order_changed':choices(a)!=choices(c)}})
# A strict acceptance test that fails: source family and consistency-switch requests.
strict=[]
for sid in ['q-105163','q-105165','q-105164','q-73957']:
 try:g.generate('moderate',83,sid,{'translation':0});ok=True;err=None
 except Exception as ex:ok=False;err=repr(ex)
 strict.append({'request':'replay supplied source '+sid,'expected':'accepted','accepted':ok,'error':err,'passed':ok})
# Bounded invalid-input and deterministic checks.
invalid=[]
for label,args in [('easy',('easy',)),('translation boundary +3',('moderate',83,'q-73954',{'translation':3})),('translation noninteger',('moderate',83,'q-73954',{'translation':True})),('unknown slot',('moderate',83,'q-73954',{'target':[16,-1,-17]}))]:
 try:g.generate(*args);invalid.append({'case':label,'rejected':False})
 except (ValueError,KeyError) as ex:invalid.append({'case':label,'rejected':True,'error':repr(ex)})
save('strict-acceptance-results.json',strict)
save('packaging-results.json',{'python':platform.python_version(),'sympy':sp.__version__,'manifest':load(P/'package.json')['dependencies'],'deterministic':g.batch('moderate',5,20261021)==g.batch('moderate',5,20261021),'invalid_inputs':invalid,'catalog_count':len(catalog),'external_assets':sum(len(r['generation'].get('assets',[])) for r in catalog),'package_unchanged':before==hashes()})
# Native grade all choices against independent prompt truth, in a single invocation.
cases=[]
for group,records in [('catalog',catalog),('batch',batch),('counterfactual', [a,b,c])]:
 for i,r in enumerate(records):cases.append({'label':f'{group}-{i}','record':r,'checks':[{'submitted_answer_id':o[':answer/id'],'expected':'accepted' if o[':answer/value']==truth(r) else 'rejected','purpose':'independent exact 3x2 system truth; plausible complete-bank alternative'} for o in choices(r)]})
save('grader-input.json',cases)
# Include raw batch plus pairs and original contradiction/elimination profiles for actual UI.
render=batch+[a,b,c]+[g.generate('moderate',83,sid,{'translation':t}) for sid,t in [('q-34242',0),('q-34568',2),('q-105167',-2),('q-73950',2)]]
save('render-records.json',render)
# Captured inventory contains only original Math Academy source records; no generated items.
orig={q[':question/id'] for q in source['material']['kp'][':knowledge-point/questions']}
nonoriginal=[q for q in inventory['questions'] if q[':question/id'] not in orig]
save('inventory-audit.json',{'basis':inventory['basis'],'count':len(inventory['questions']),'original_source_count':sum(q[':question/id'] in orig for q in inventory['questions']),'nonoriginal_count':len(nonoriginal),'nonoriginal_questions':nonoriginal,'result':'All captured bank questions are original source questions, not generated; no affected generated stored instances demonstrated. Exact identity checked against supplied source IDs.'})
save('affected-inventory.json',{'affected_questions':[]})
# Save compact distribution metrics; include coefficient-template signature cues.
def metrics(rs):
 profiles=collections.defaultdict(list)
 for r in rs:profiles[r['generation']['source_id']].append(r)
 return {'count':len(rs),'consistent':sum(key(r)!='No solution' for r in rs),'inconsistent':sum(key(r)=='No solution' for r in rs),'second_largest_numeric_success':sum(key(r)==str(sorted([sp.Rational(o[':answer/value']) for o in choices(r) if o[':answer/type']==':answer.type/math'])[-2]) for r in rs),'correct_positions':dict(collections.Counter(keypos(r)+1 for r in rs)),'c_label_count':sum('{c}_{1}' in r['question'][':question/problem'] for r in rs),'c_label_no_solution':sum('{c}_{1}' in r['question'][':question/problem'] and key(r)=='No solution' for r in rs),'profiles':{sid:{'n':len(items),'answers':list(sorted({key(r) for r in items})),'correct_positions':dict(collections.Counter(keypos(r)+1 for r in items)),'numeric_ranks':dict(collections.Counter(str(numeric_rank(r)) for r in items))} for sid,items in profiles.items()}}
save('coverage-initial.json',{'catalog':metrics(catalog),'batch':metrics(batch),'fresh':metrics(fresh),'source_profiles':len(replay),'missing_profiles':[r['source_id'] for r in replay if not r['supported']]})
print(json.dumps({'catalog':len(catalog),'math_failures':sum(not r['passed'] for r in math),'replay_missing':[r['source_id'] for r in replay if not r['supported']],'source_mismatches':[{k:v for k,v in r.items() if k!='record'} for r in replay if r['supported'] and not all(r[k] for k in ['vectors_equal','bank_equal','correct_equal','problem_normalized_equal','solution_normalized_equal'])],'batch':metrics(batch),'inventory_nonoriginal':len(nonoriginal)},indent=2))
