#!/usr/bin/env python3
"""Independent read-only audit. Run with job Python; writes only beside this script."""
import sys
sys.dont_write_bytecode=True
import json,re,hashlib,importlib.util,pathlib,copy,shutil,platform,subprocess
ROOT=pathlib.Path(__file__).resolve().parent
JOB=ROOT.parent
PACKAGE=JOB/'workspace'
REPO=pathlib.Path('/home/jake/Developer/Course_Academy')
def save(n,o): (ROOT/n).write_text(json.dumps(o,indent=2,default=str))
def load(p): return json.loads(pathlib.Path(p).read_text())
def package_hashes(): return {str(p.relative_to(PACKAGE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(PACKAGE.rglob('*')) if p.is_file()}
save('package-before.json',package_hashes())
sys.path.insert(0,str(PACKAGE))
spec=importlib.util.spec_from_file_location('reviewed_generator',PACKAGE/'17592186119784.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def matrix(t):
 bodies=re.findall(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',t,re.S)
 return [[[int(c.strip()) for c in row.split('&')] for row in b.split(r'\\')] for b in bodies]
def canonical(s): return re.sub(r'[{}\s$]','',s)
def expression(m,expr):
 a=canonical(expr);name=next(c for c in a if c.isalpha());a=a.replace(name,'X');t=list(map(list,zip(*m)))
 if a=='X':return m
 if a=='X^T':return t
 if a in ('X+X^T','X^T+X'):return [[x+y for x,y in zip(r,s)] for r,s in zip(m,t)]
 if a=='X^T-X':return [[x-y for x,y in zip(r,s)] for r,s in zip(t,m)]
 if a=='X-X^T':return [[x-y for x,y in zip(r,s)] for r,s in zip(m,t)]
 raise ValueError(expr)
def bank(f):
 ref=f[':answer-field/correct'];aid=ref.get(':answer/id') if isinstance(ref,dict) else ref[1]
 return next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==aid)
def expected_record(r):
 q=r['question'];m=matrix(q[':question/problem'])[0];out=[];derived=[]
 for f in q[':question/answer-fields']:
  key=f[':answer-field/key']
  if key=='None of the above': out.append(not any(out));continue
  match=re.search(r'\$(.*?)\$ is (upper triangular|lower triangular|diagonal)',key)
  expr,kind=match.groups();b=expression(m,expr);derived.append(b)
  ok=all(b[i][j]==0 for i in range(len(m)) for j in range(len(m)) if (i>j if kind=='upper triangular' else i<j if kind=='lower triangular' else i!=j))
  out.append(ok)
 return out,derived
sources=load(JOB/'source/source.json')['material']['kp'][':knowledge-point/questions']
records=[]
for sid,t in g.TEMPLATES.items():
 if t['level']=='easy':continue
 for seed in [8191,8209,8221,8231,8233]: records.append(g.generate(t['level'],seed,template=sid))
save('samples-independent.json',records)
batch=load(JOB/'samples.json');save('batch.json',batch)
math_checks=[]
for label,rs in [('independent',records),('runner-batch',batch)]:
 for r in rs:
  exp,derived=expected_record(r);q=r['question'];actual=[bank(f)=='true' for f in q[':question/answer-fields']]
  solution=matrix(q[':question/worked-solution'])
  assertions=re.findall(r'\*\*(true|false)\*\*',q[':question/worked-solution'])
  math_checks.append({'set':label,'id':q[':question/id'],'template':r['generation']['template'],'seed':r['generation']['seed'],'expected':exp,'actual':actual,'key_pass':exp==actual,'solution_matrix_pass':solution==derived,'solution_truth_pass':[v=='true' for v in assertions]==exp[:len(derived)]})
save('math-results.json',math_checks)
replays=[];source_checks=[]
for q in sources:
 sid=q[':question/math-academy-id'];p={'matrix':matrix(q[':question/problem'])[0]};lev=(q.get(':question/difficulty') or {':db/ident':':question.difficulty/hard'})[':db/ident'].split('/')[-1]
 try:
  r=g.generate(lev,101,template=sid,parameters=p);raw=g.generate(lev,101,template=sid,profile='source-replay',parameters=p);replays.append({'source_id':q[':question/id'],'normal':r,'raw':raw})
  source_bank={canonical(f[':answer-field/key']):bank(f) for f in q[':question/answer-fields']};generated_bank={canonical(f[':answer-field/key']):bank(f) for f in r['question'][':question/answer-fields']}
  source_checks.append({'source_id':q[':question/id'],'template':sid,'status':'supported','same_matrix':matrix(r['question'][':question/problem'])[0]==p['matrix'],'source_bank':source_bank,'generated_bank':generated_bank,'same_complete_bank':source_bank==generated_bank,'raw_field_types':[f[':answer-field/type'] for f in raw['question'][':question/answer-fields']],'raw_matches_current_checkbox_contract':False})
 except Exception as e:source_checks.append({'source_id':q[':question/id'],'template':sid,'status':'unsupported','error':str(e),'parameters':p})
save('source-replay-records.json',replays);save('source-replay-results.json',source_checks)
# Relevant zero-region change: clear only nonzero strict-lower entry.
p0={'matrix':[[4,0,0],[1,1,0],[0,0,3]]};p1={'matrix':[[4,0,0],[0,1,0],[0,0,3]]};pi=copy.deepcopy(p0);pi['matrix'][0][0]=-8
r0=g.generate('moderate',101,template='q-42091',parameters=p0);ri=g.generate('moderate',101,template='q-42091',parameters=pi)
cf={'command':'<job-python> audit.py','template':'q-42091','seed':101,'before_parameters':p0,'relevant_after_parameters':p1,'irrelevant_after_parameters':pi,'before':r0,'irrelevant_after':ri,'expected_before':[False,True,True,False],'expected_relevant_after':[True,True,True,False],'expected_irrelevant_after':[False,True,True,False]}
try: cf['relevant_after']=g.generate('moderate',101,template='q-42091',parameters=p1);cf['relevant_status']='generated'
except Exception as e:cf['relevant_status']='rejected';cf['error']=str(e)
cf['irrelevant_pass']=expected_record(r0)[0]==expected_record(ri)[0]
save('counterfactuals.json',cf)
save('render-records.json',batch+[r0,ri,records[25],records[-1]])
# The native learner receives choice IDs for both Boolean settings of every field.
cases=[]
for r in batch+[r0,ri,records[25],records[-1]]:
 exp,_=expected_record(r);checks=[]
 for i,(f,v) in enumerate(zip(r['question'][':question/answer-fields'],exp)):
  for a in f[':answer-field/choices']:
   checks.append({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if (a[':answer/value']=='true')==v else 'rejected','purpose':'Independent exact zero-region oracle; both checkbox settings'})
 cases.append({'label':r['question'][':question/id'],'record':r,'checks':checks})
save('grader-input.json',cases)
# Boundary/rejection and runtime/relocation contracts.
reject=[]
for label,p in [('out-of-range',{'matrix':[[9,0,0],[1,0,0],[0,0,0]]}),('float',{'matrix':[[1.0,0,0],[1,0,0],[0,0,0]]}),('wrong-size',{'matrix':[[0,0],[1,0]]}),('in-scope-upper',{'matrix':[[0,1,0],[0,0,0],[0,0,0]]}),('in-scope-neither',{'matrix':[[0,1,0],[1,0,0],[0,0,0]]})]:
 try:g.generate('moderate',101,'q-42091',parameters=p);reject.append({'case':label,'parameters':p,'rejected':False})
 except Exception as e:reject.append({'case':label,'parameters':p,'rejected':True,'error':str(e)})
save('rejection-results.json',reject)
relocated=ROOT/'relocated-package';shutil.copytree(PACKAGE,relocated,dirs_exist_ok=True)
command=[sys.executable,'-B',str(relocated/'17592186119784.py'),'--difficulty','moderate','--seed','8191','--count','1','--format','json']
x=json.loads(subprocess.check_output(command,cwd=ROOT));y=[g.generate('moderate',8191)]
runtime={'python':platform.python_version(),'sympy':g.sp.__version__,'manifest':load(PACKAGE/'package.json'),'relocation_command':command,'relocation_equal':x==y,'deterministic_replay':records[0]==g.generate('moderate',8191,'q-42091'),'batch_replay_equal':[r==g.generate('moderate',r['generation']['seed']) for r in batch],'boundary_supports':{sid:len(g.supports(sid)) for sid in g.TEMPLATES}}
save('packaging-results.json',runtime)
# Inventory: distinguish original questions from the single unprovenanced stored entry.
inv=load(JOB/'source/inventory.json');source_ids={q[':question/id'] for q in sources};unmatched=[q for q in inv['questions'] if q[':question/id'] not in source_ids]
save('inventory-unmatched.json',unmatched)
save('inventory-assessment.json',{'basis':inv['basis'],'total':len(inv['questions']),'original_source_questions':len(source_ids),'unmatched_count':len(unmatched),'unmatched_ids':[q[':question/id'] for q in unmatched],'conclusion':'No affected generated instance reproduced with matching question ID and generation metadata. The one non-source record has no generation metadata in captured inventory; provenance and exact regeneration remain unverified. Empty affected list is not verified absence of the family weakness. Original source questions are not designated generated.'})
save('affected-inventory.json',{'affected_questions':[]})
save('package-after.json',package_hashes());assert load(ROOT/'package-before.json')==load(ROOT/'package-after.json')
(ROOT/'session-state.md').write_text('Independent source analysis, 50 sampled records, runner batch, source replay, math, controlled rejection/diagonal counterfactuals, relocation and inventory assessment saved. Package byte hashes unchanged. Next: native grader, actual renderer, delivery stages, conditional cue probes and final report.\n')
print(json.dumps({'samples':len(records),'math_failures':[x for x in math_checks if not all(x[k] for k in ('key_pass','solution_matrix_pass','solution_truth_pass'))],'unsupported_source':[x['template'] for x in source_checks if x['status']=='unsupported'],'counterfactual':cf['relevant_status'],'runtime':runtime,'package_unchanged':True},indent=2))
