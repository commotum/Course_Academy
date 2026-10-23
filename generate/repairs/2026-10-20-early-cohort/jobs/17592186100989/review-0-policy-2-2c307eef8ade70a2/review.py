import sys, json, re, pathlib, importlib.util, copy, collections, hashlib, platform, subprocess, shutil
sys.dont_write_bytecode=True
ROOT=pathlib.Path(__file__).resolve().parent
REPO=pathlib.Path('/home/jake/Developer/Course_Academy')
JOB=REPO/'generate/repairs/2026-10-20-early-cohort/jobs/17592186100989'
PKG=JOB/'workspace'
def save(n,x): (ROOT/n).write_text(json.dumps(x,indent=2)+'\n')
def load(n): return json.load(open(n))
spec=importlib.util.spec_from_file_location('reviewed_generator',PKG/'17592186100989.py'); g=importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
def parsed(q):
 s=q[':question/problem']; m=re.search(r'\\begin\{(?:bmatrix|aligned)\}(.*?)\\end\{(?:bmatrix|aligned)\}',s,re.S)
 a=[[v.strip() for v in row.split('&')] for row in m[1].split('\\\\')]
 t=re.search(r'_\{(\d)(\d)\}',s);i,j=map(int,t.groups());return a,i,j
def expected(q):
 a,i,j=parsed(q);return a[i-1][j-1] if 1<=i<=len(a) and 1<=j<=len(a[0]) else 'No such entry'
def key(q):
 f=q[':question/answer-fields'][0]; c=f.get(':answer-field/correct');id=c[':answer/id'] if isinstance(c,dict) else c[1]
 return next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==id)
def norm(s):return re.sub(r'\s+','',s.replace(r'[\begin{aligned}',r'\begin{bmatrix}').replace(r'\end{aligned}]',r'\end{bmatrix}'))
def bank(q):return sorted(a[':answer/value'] for a in q[':question/answer-fields'][0][':answer-field/choices'])
source=load(JOB/'source/source.json')['material']['kp']; replay=[]; replay_results=[]
for q in source[':knowledge-point/questions']:
 a,i,j=parsed(q); name=re.search(r'matrix \$([A-Z])\$',q[':question/problem'])[1]; sid=q[':question/math-academy-id']; p={'name':name,'matrix':a,'i':i,'j':j}
 if sid=='q-13490':p['opaque']=['5','4']
 raw=g.generate_easy(seed=47,parameters=p,profile='raw_'+sid); r=raw if sid=='q-13490' else g.generate_easy(seed=47,parameters=p,profile=sid)
 replay.append(r)
 checks={'matrix_and_target':parsed(r['question'])==(a,i,j),'complete_bank':bank(q)==bank(r['question']),'prompt':norm(q[':question/problem'])==norm(r['question'][':question/problem']),'key':key(r['question'])==expected(q)}
 if ':question/worked-solution' in q:checks['learner_solution']=norm(q[':question/worked-solution'])==norm(r['question'][':question/worked-solution'])
 replay_results.append({'source_id':q[':question/id'],'source_ma_id':sid,'parameters':p,'checks':checks,'raw_solution_matches':norm(q.get(':question/worked-solution',''))==norm(raw['question'].get(':question/worked-solution','')),'completion_note':'q-13506 key and solution independently inferred; q-13490 uses evidence-only raw bank; q-125593 current learner output matches R, historical raw profile names E.'})
q=source[':knowledge-point/canonical-example'];a,i,j=parsed(q); canonical=g.generate_easy(seed=47,profile='blank',parameters={'name':'B','matrix':a,'i':i,'j':j}); replay.append(canonical)
replay_results.append({'source_id':q[':question/id'],'checks':{'canonical_value':key(canonical['question'])=='2','canonical_matrix_target':parsed(canonical['question'])==(a,i,j)},'note':'Canonical has no source answer fields; blank interface is an authored reconstruction.'})
save('source-replay-records.json',replay);save('source-replay-results.json',replay_results)
records=[g.generate_easy(seed=s) for s in range(70401,70529)]
batch=load(JOB/'samples.json');save('batch-records.json',batch);save('samples.json',records)
math_results=[]
for r in records+batch+replay:
 q=r['question']; a,i,j=parsed(q);e=expected(q);ans=key(q)
 math_results.append({'id':q[':question/id'],'seed':r['generation']['seed'],'expected':e,'actual':ans,'passed':e==ans and len(set(bank(q)))==len(bank(q)),'solution_consistent':(e in q[':question/worked-solution']) if e!='No such entry' else ('does not have' in q[':question/worked-solution'])})
save('math-results.json',math_results)
# Controlled changes generated through public API, including target change with same data.
p={'name':'A','matrix':[['1','2','3'],['4','5','6'],['7','8','9']],'i':2,'j':2}
cp=[]
for label,change in [('base',{}),('target',{'i':1,'j':3}),('target_value',{'matrix':[['1','2','3'],['4','-3','6'],['7','8','9']]}),('irrelevant',{'matrix':[['-2','2','3'],['4','5','6'],['7','8','9']]}),('rename',{'name':'R'})]:
 r=g.generate_easy(seed=29,profile='blank',parameters=p|change);cp.append(r)
save('counterfactual-records.json',cp)
# Minimal shape-cue and valid relevant decision change suppressed by construction.
small={'name':'B','matrix':[['1','-3'],['0','5']],'i':3,'j':2}
minimal=g.generate_easy(seed=11,profile='all_four',parameters=small);save('minimal-shortcut.json',[minimal])
restrictions=[]
for label,p2,profile in [('existing_same_matrix',small|{'i':2},'all_four'),('missing_in_3x3',p|{'i':4},'all_four'),('existing_2x2_default_radio',small|{'i':2},'transpose_neighbors'),('existing_first_column',p|{'j':1},'right_up_left')]:
 try:r=g.generate_easy(seed=11,profile=profile,parameters=p2);result={'accepted':True,'record':r}
 except ValueError as e:result={'accepted':False,'error':str(e)}
 restrictions.append({'case':label,'seed':11,'parameters':p2,'profile':profile,**result})
save('construction-restrictions.json',restrictions)
# Boundary rejection should reject invalid inputs, preserving required safety.
invalid=[]
for label,p2 in [('zero_index',p|{'i':0}),('negative_index',p|{'j':-1}),('nonsquare',p|{'matrix':[['1','2','3'],['4','5','6']]}),('out_of_range_blank',p|{'i':4})]:
 try:g.generate_easy(seed=29,profile='blank',parameters=p2);ok=False;err='accepted'
 except ValueError as e:ok=True;err=str(e)
 invalid.append({'case':label,'parameters':p2,'rejected':ok,'error':err})
save('rejection-results.json',invalid)
# Real grader: all radio choices, and varied legitimate free entries.
cases=[]
for idx,r in enumerate(batch+cp+replay+[minimal]):
 q=r['question'];f=q[':question/answer-fields'][0];e=expected(q); checks=[]
 if f[':answer-field/type'].endswith('/radio'):
  checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/value']==e else 'rejected','purpose':'independent prompt lookup'} for a in f[':answer-field/choices']]
 else:
  if re.fullmatch(r'-?\d+',e):
   v=int(e);forms=[(e,True),(f'{v}.0',True),(f'{2*v}/2',True),(str(v+1),False)]
  else:forms=[(e,True),('sqrt(2)' if e==r'\sqrt{2}' else 'sqrt(3)',True),('2',False)]
  checks=[{'submitted':v,'expected':'accepted' if ok else 'rejected','purpose':'equivalent scalar or plausible wrong entry'} for v,ok in forms]
 if idx in (6,7): checks.append({'submitted':'5','expected':'rejected','purpose':'stale base answer rejected after relevant target/value change'})
 cases.append({'label':f'record-{idx}','record':r,'checks':checks})
rad=g.generate_easy(seed=19,profile='blank',parameters={'name':'G','matrix':[['0',r'\sqrt{2}'],['-1','2']],'i':1,'j':2})
cases.append({'label':'radical-blank','record':rad,'checks':[{'submitted':v,'expected':e,'purpose':'legitimate radical notation or incorrect rational'} for v,e in [(r'\sqrt{2}','accepted'),('sqrt(2)','accepted'),('2^(1/2)','accepted'),('2','rejected')]]})
save('grader-input.json',cases)
save('render-records.json',batch+cp+[rad]+[r for r in replay if r['generation']['bank_profile']=='q-125593'])
# Snapshot package hashes and runtime dependencies, relocation without sibling data.
manifest=load(PKG/'package.json');hashes={str(f.relative_to(PKG)):hashlib.sha256(f.read_bytes()).hexdigest() for f in PKG.rglob('*') if f.is_file()};save('package-hashes-before.json',hashes)
rel=ROOT/'relocated';rel.mkdir(exist_ok=True);shutil.copyfile(PKG/manifest['entrypoint'],rel/manifest['entrypoint'])
cmd=[sys.executable,str(rel/manifest['entrypoint']),'--difficulty','easy','--seed','3302362091','--count','5','--format','json'];proc=subprocess.run(cmd,capture_output=True,text=True,cwd=rel)
relocated=json.loads(proc.stdout);save('relocated-records.json',relocated)
save('packaging-results.json',{'command':cmd,'declared_dependencies':manifest['dependencies'],'installed':{'python':platform.python_version(),'packages':{'sympy':g.sp.__version__}},'all_manifest_files_present':all((PKG/f).is_file() for f in manifest['files']),'deterministic_replay':records==[g.generate_easy(seed=s) for s in range(70401,70529)],'relocated_cli_replays_batch':relocated==batch,'exit_code':proc.returncode,'stderr':proc.stderr,'external_outputs':'No asset outputs or runtime external file reads in entrypoint; reads standard library and sympy only.'})
inv=load(JOB/'source/inventory.json');save('inventory-analysis.json',{'basis':inv['basis'],'question_count':len(inv['questions']),'source_ids':[q[':question/id'] for q in inv['questions']],'generated_records':sum(':question/generation' in q for q in inv['questions']),'result':'All six captured records are original MA source questions, identified by source question IDs and MA IDs. No stored generated records exist in this captured inventory; no eligible generated historical defect can be demonstrated. No originals relabeled.','selection_rules':'learning.rs validate_question rejects retired and malformed fields; question_selection.rs select filters by weighted difficulty then uniform within chosen band, with caller history exclusions. No shape/target correction occurs in selection. Live history and weights absent from capture.'});save('affected-inventory.json',{'affected_questions':[]})
(ROOT/'session-state.md').write_text('Independent source account and scripts saved. Source replay, 128 fresh easy samples, exact batch, controlled pairs, boundary rejection, dependency/replay/relocation completed. Shape-conditioned radio shortcut demonstrated; delivery, native grading and renderer next. Inventory contains only six original source records.\n')
print(json.dumps({'source_checks_failed':[x for x in replay_results if not all(x['checks'].values())],'math_failures':sum(not x['passed'] for x in math_results),'samples':len(records),'counterfactuals':len(cp),'restrictions':restrictions,'packaging':load(ROOT/'packaging-results.json')},indent=2))
