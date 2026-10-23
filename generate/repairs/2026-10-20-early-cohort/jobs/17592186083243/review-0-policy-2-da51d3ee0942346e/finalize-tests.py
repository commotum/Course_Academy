from review import *
import subprocess,shutil,collections
# Version/dependency and relocation checks operate only on copied files.
rel=ROOT/'relocated-package';shutil.copytree(PKG,rel,dirs_exist_ok=True)
code="import sys,json;sys.dont_write_bytecode=True;sys.path.insert(0,sys.argv[1]);import generator as g;print(json.dumps([g.generate('easy',3175644379),g.generate('easy',8201,'cubic_blank',parameters=dict(a=2,b=1,u=2))],sort_keys=True))"
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
a=subprocess.run([sys.executable,'-c',code,str(PKG)],env=env,cwd=ROOT,capture_output=True,text=True)
b=subprocess.run([sys.executable,'-c',code,str(rel)],env=env,cwd=ROOT,capture_output=True,text=True)
noout=dict(env);noout.pop('COURSE_ACADEMY_GENERATOR_OUTPUT_DIR',None)
c=subprocess.run([sys.executable,'-c',"import sys;sys.path.insert(0,sys.argv[1]);import generator as g;g.generate('easy',1,'cubic_blank',parameters=dict(a=4,b=3,u=2))",str(rel)],env=noout,cwd=ROOT,capture_output=True,text=True)
save('packaging-results.json',{'relocation_equal':a.returncode==b.returncode==0 and a.stdout==b.stdout,'relocation_errors':[a.stderr,b.stderr],'external_output_required':c.returncode!=0 and 'COURSE_ACADEMY_GENERATOR_OUTPUT_DIR is required' in c.stderr,'no_output_stderr':c.stderr,'manifest':json.load(open(PKG/'package.json')),'runtime':json.load(open('runtime.json')),'package_unchanged':json.load(open('package-before.json'))=={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in PKG.iterdir() if p.is_file()}})
# A smaller exact counterexample, same source family, with one common coefficient.
r=g.generate('hard',917,'reciprocal_exp_root_blank',parameters=dict(a=1,b=1,c=1,u=2))
save('minimal-grading-record.json',[r])
checks=[{'submitted':v,'expected':expected,'purpose':'fractional exponential equivalence, with positive and negative controls'} for v,expected in [(r'\frac{8}{5\sqrt{5}\exp(1/2)}','accepted'),('8*sqrt(5)*exp(-1/2)/25','accepted'),('8*sqrt(5)*e^(-1/2)/25','accepted'),('8*sqrt(5)*e^(1/2)/25','rejected'),('0','rejected')]]
save('minimal-grader-input.json',[{'label':'fractional exp counterexample','record':r,'checks':checks}])
p=subprocess.run(['/home/jake/Developer/Course_Academy/generate/runs/current/check-engine',str(ROOT/'minimal-grader-input.json'),str(ROOT/'minimal-grader-result.json')],capture_output=True,text=True)
save('minimal-grader-execution.json',{'command':'/home/jake/Developer/Course_Academy/generate/runs/current/check-engine minimal-grader-input.json minimal-grader-result.json','returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr})
# Preserve required strict failure input, then independently exercise passing controls.
save('minimal-grader-controls-input.json',[{'label':'counterexample controls','record':r,'checks':checks[2:]}])
p=subprocess.run(['/home/jake/Developer/Course_Academy/generate/runs/current/check-engine',str(ROOT/'minimal-grader-controls-input.json'),str(ROOT/'minimal-grader-controls-result.json')],capture_output=True,text=True)
print('minimal',key(r),'controls',p.returncode)
# Captured eligibility and occurrence review, without attributing generation to source questions.
inv=json.load(open(ROOT.parent/'source/inventory.json'));source=json.load(open('source-cases.json'));sourceids={q[':question/id'] for q in source}
summary=[]
for q in inv['questions']:
 summary.append({'question_id':q[':question/id'],'entity_id':q[':db/id'],'original_source':q[':question/id'] in sourceids,'retired':q.get(':question/retired',False),'field_type':q[':question/answer-fields'][0][':answer-field/type'][':db/ident'],'problem':q[':question/problem'],'contains_exponential': 'e^' in q[':question/problem'] or '{e}^' in q[':question/problem']})
save('inventory-review.json',{'basis':inv['basis'],'questions':summary,'selection_rules':'learning.rs validate_practice_question excludes retired/free/multistep; these five non-source questions have a complete blank or radio field and no retirement flag. question_selection.rs selects by difficulty then uniformly within fresh eligible band; seen/current-prefix exclusions depend on learner history.','conclusion':'No demonstrated generated stored-pool instance of fractional-exponential grading defect: all five non-source stored curves are trigonometric. Original source questions are not marked generated. This is an absence of this defect in that captured generated subset, not a universal grading audit of inventory.','limitations':['Captured inventory has no generation envelope or learner history; no database access performed.']})
save('affected-inventory.json',{'affected_questions':[]})
(ROOT/'session-state.md').write_text('Milestone: 22 source banks replayed; 77 independent math checks; 356 native grading checks pass except separately retained fractional-exp alias failures. Runner batch 5/5 delivered. 21 actual UI cases rendered; visual inspection in progress/completing. Package relocation checked; original unchanged. Finalize variation/selection evidence and report.\n')
