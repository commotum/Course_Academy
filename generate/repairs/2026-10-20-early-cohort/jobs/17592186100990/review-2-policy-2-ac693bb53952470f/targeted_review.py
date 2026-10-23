"""Run with /home/jake/Developer/Course_Academy/.venv/bin/python -B targeted_review.py.
Read-only package review; all outputs resolve relative to this evidence directory.
"""
import json,pathlib,sys,hashlib,subprocess,os,shutil,platform,re,collections
R=pathlib.Path(__file__).resolve().parent;J=R.parent;P=J/'workspace';REPO=pathlib.Path('/home/jake/Developer/Course_Academy');PY=REPO/'.venv/bin/python'
sys.dont_write_bytecode=True
exec(compile((R/'audit.py').read_text().split('source=json.load')[0],str(R/'audit.py'),'exec'))
def load(n):return json.loads((R/n).read_text())
def run(args,name):
 p=subprocess.run(list(map(str,args)),capture_output=True,text=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',COURSE_ACADEMY_GENERATOR_OUTPUT_DIR=str(R/'assets')))
 save(name,{'command':p.args,'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr});return p
old=J/'review-1-policy-2-51ba951d744c2d08'
oldhash=load('reuse-provenance.json')['previous_binding']
manifest=json.loads((P/'package.json').read_text());oldfiles=json.loads((old/'initial-package-hashes.json').read_text())
binding={'runtime_files_match_previous':all(hashlib.sha256((P/f).read_bytes()).hexdigest()==oldfiles[f] for f in manifest['files']), 'batch_matches_previous':json.loads((J/'samples.json').read_text())==load('batch.json'),'previous_binding':oldhash,'current_engine_sha256':hashlib.sha256((REPO/'generate/runs/current/check-engine').read_bytes()).hexdigest(),'ui_files_match':all(hashlib.sha256((REPO/'ui'/f).read_bytes()).hexdigest()==h for f,h in load('render/ui-hashes.json').items()),'delivery_implementation_matches':all(hashlib.sha256((REPO/f).read_bytes()).hexdigest()==h for f,h in load('delivery-batch/delivery.json')['implementation_sha256'].items())}
assert binding['runtime_files_match_previous'] and binding['batch_matches_previous']
save('binding-verification.json',binding)
# All supplied source cases replay again, compared to independently verified prior records.
source=json.loads((J/'source/source.json').read_text())['material']['kp'][':knowledge-point/questions']
replays=[g.generate_easy(seed=73,profile='completed:'+q[':question/math-academy-id']) for q in source]
assert json.loads(json.dumps(replays))==load('source-replays.json');save('current-source-replays.json',replays)
# Fresh CLI-size samples, independently chosen seeds; unchanged broad domain reused.
fresh=[]
for s in (983041,983042):fresh+=g.generate_batch('easy',s,5)
save('current-fresh-batches.json',fresh)
# Symbolic boundary and off-diagonal controls; values fixed and each target moved.
controls=[]
for i,j in [(1,1),(1,4),(4,1),(4,4),(2,3),(3,2)]:
 p={'matrix':[[r*4+c-8 for c in range(4)] for r in range(4)],'i':i,'j':j,'letter':'A'}
 controls.append(g.generate_easy(seed=46321,template='notation_blank',parameters=p))
p={'matrix':[[1]*4 for _ in range(4)],'i':2,'j':3,'letter':'A'}
controls.append(g.generate_easy(seed=46321,template='notation_blank',parameters=p))
save('current-symbolic-controls.json',controls)
records=load('batch.json')+replays+fresh+controls
results=[facts(r) for r in records];assert not any(x['errors'] for x in results)
save('current-math.json',{'seeds':[983041,983042,46321],'count':len(records),'results':results,'all_sources_match_independent_previous_replay':True})
# Retained strict native expectations plus fresh visible-coordinate cases in one invocation.
cases=[]
for n in ['native-input.json','pair-grader-input.json','prior-grader-symbolic-strict.json','comma-strict-input.json']:
 for c in load(n):c['label']=n+':'+c['label'];cases.append(c)
for r in records:
 fs=r['question'][':question/answer-fields'];fct=facts(r);i,j=fct['position'];b=fct['letter'];checks=[]
 for fi,f in enumerate(fs):
  k=key(f)
  if f[':answer-field/type'].endswith('/radio'):
   checks.extend({'field_index':fi,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if coords(a[':answer/value'])==(i,j) else 'rejected','purpose':'Visible cell coordinate decides, not metadata'} for a in f[':answer-field/choices'])
  elif '_' in k:
   good=[f'{b}_{{{i}{j}}}',f'{b}_{{{i},{j}}}',f'{{{b}}}_{{ {i} , {j} }}',f'{{{{{b}}}}}_{{{{{i}}},{{{j}}}}}',f'{b}_{{{i},\\,{j}}}',f'{b}_{{{i},{j}}}+0',f'2*{b}_{{{i},{j}}}-{b}_{{{i}{j}}}']
   bad=[f'{b}_{{{i%4+1},{j}}}',f'{b}_{{{i},{j%4+1}}}',f'z_{{{i},{j}}}' if b!='z' else f'a_{{{i},{j}}}',f'{b}_{{{i},1{j}}}',f'{b}_{{{i},,{j}}}',f'{b}_{{{i},{j},1}}',b,'0',f'{b}_{i}{j}']
   if i!=j:bad.append(f'{b}_{{{j},{i}}}')
   checks.extend({'field_index':fi,'submitted':v,'expected':exp,'purpose':'Equivalent compact/comma/grouped matrix coordinates' if exp=='accepted' else 'Wrong coordinates, label, value, extra component, or unbraced TeX'} for vals,exp in [(good,'accepted'),(bad,'rejected')] for v in vals)
  else:
   checks.extend({'field_index':fi,'submitted':v,'expected':exp,'purpose':'Numeric equivalent or wrong index'} for v,exp in [(k,'accepted'),(str(int(k)*2)+'/2','accepted'),(str(int(k)+1),'rejected')])
 cases.append({'label':'current:'+r['question'][':question/id'],'record':r,'checks':checks})
# Test stale comma response on moved box, and preserve it under value-only change.
for before,after,expected in [(4,5,'rejected'),(4,6,'accepted')]:
 cases.append({'label':f'comma-counterfactual-{before}-{after}','record':controls[after],'checks':[{'submitted':'a_{2,3}','expected':expected,'purpose':'Relevant/irrelevant evidence change with same comma response'}]})
save('current-native-input.json',cases)
p=run([REPO/'generate/runs/current/check-engine',R/'current-native-input.json',R/'current-native-report.json'],'current-native-execution.json')
# Reproducible actual delivery and cue checks for exact runner batch and new small batches.
for name,inp in [('current-delivery-batch','batch.json'),('current-delivery-fresh','current-fresh-batches.json')]:
 r=run([PY,REPO/'generate/pipeline/check_delivery.py','--input',R/inp,'--source',J/'source/source.json','--inventory',J/'source/inventory.json','--difficulty','easy','--output',R/name,'--asset-root',R/'assets','--math-root','/media/jake/SSD/EDB/math'],name+'-execution.json');assert r.returncode==0
for name,inp in [('current-batch-cue','current-delivery-batch/accepted.json'),('current-fresh-cue','current-delivery-fresh/accepted.json'),('old-failing-cue','prior-batch.json')]:
 run([PY,'-B',R/'regression_shortcut.py',R/inp,R/(name+'.json')],name+'-execution.json')
# Determinism and relocation on exact runner inputs; no package writes.
rel=R/'current-relocated'
for f in manifest['files']:
 d=rel/f;d.parent.mkdir(exist_ok=True,parents=True);shutil.copyfile(P/f,d)
r=run([PY,'-B',rel/'17592186100990.py','--difficulty','easy','--seed','3782988951','--count','5','--format','json'],'current-relocation-execution.json')
assert r.returncode==0 and json.loads(r.stdout)==load('batch.json')
versions={'python':platform.python_version(),'packages':{'sympy':g.sp.__version__}}
assert manifest['dependencies']==versions
save('current-packaging.json',{'versions':versions,'manifest_exact_match':True,'relocated_cli_matches_runner_batch':True,'direct_batch_matches':json.loads(json.dumps(g.generate_batch('easy',3782988951,5)))==load('batch.json'),'no_external_assets':True,'unchanged_boundary_rejection_evidence':'packaging-results.json'})
# Current actual UI render: exact batch, restored 4x4 source, relevant and irrelevant symbolic controls.
save('current-render-records.json',load('current-delivery-batch/accepted.json')+[replays[-1],controls[4],controls[5],controls[6]])
save('current-summary.json',{'native_exit':p.returncode,'native_cases':len(cases),'native_checks':sum(len(c['checks']) for c in cases),'math_records':len(records),'source_cases':len(replays),'batch_survivors':len(load('current-delivery-batch/accepted.json')),'fresh_survivors':len(load('current-delivery-fresh/accepted.json'))})
(R/'session-state.md').write_text('Source and previous binding verified. Fresh math, source replay, delivery, relocation completed. Native grading run; inspect current-summary.json and current-native-execution.json. UI rendering and final report remain. Package untouched.\n')
print(json.dumps(load('current-summary.json')))
