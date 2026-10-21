import json,pathlib,hashlib,sys
E=pathlib.Path(__file__).resolve().parent;B=E.parent;R=pathlib.Path('/home/jake/Developer/Course_Academy');P=B/'workspace'
def load(p):return json.loads((E/p).read_text())
def save(p,v):(E/p).write_text(json.dumps(v,indent=2)+'\n')
def hashes(p):return {str(f.relative_to(p)):hashlib.sha256(f.read_bytes()).hexdigest() for f in p.rglob('*') if f.is_file()}
now=hashes(P);save('package-tree-after.json',now);assert now==load('package-tree-before.json')
assert all(r['passed'] and not r['math']['errors'] for r in load('source-replay-results.json'))
assert not load('math-results.json')['failures'];assert not load('supplemental-results.json')['failures'];assert all(not r['errors'] for r in load('apparent-cue-results.json')['math'])
g=load('grader-final-results.json');assert (g['accepted_checks'],g['rejected_checks'],g['database_writes'],g['documented_unresolved_checks'])==(96,384,0,0)
assert load('render/rendering.json')['passed'] and len(load('render/rendering.json')['cases'])==18
for label,n in [('independent',34),('batch',5),('supplemental',26),('counterfactual',9),('apparent',5)]:
 assert len(load(f'delivery-{label}/accepted.json'))==n
assert all(r['rejected'] for r in load('generator-rejection.json'))
p=load('packaging-results.json');assert p['deterministic_replay'] and p['relocation_identical'] and p['package_unchanged'];assert {'python':p['python'],'packages':p['packages']}==p['manifest']['dependencies']
reg=load('regression-verification.json');assert [r['exit_code'] for r in reg]==[1,0];assert "missing=['q-131634', 'q-74625']" in reg[0]['stderr']
v=load('pedagogical-variation.json');ch=load('apparent-cue-results.json')['results']
for probe in v['shortcut_probes']:
 if probe['subgroup'].startswith(('fresh_raw:','fresh_delivered:')) and probe['correct']==probe['total'] and probe['total']>1:
  c=next(c for c in ch if c['profile']==probe['subgroup'].split(':')[1] and c['cue']==probe['cue'])
  probe['conclusion']+=f" Explicit counterexample: seed {c['seed']} predicts option {c['predicted_index']}, whereas correct option is {c['correct_index']}; native grading confirms this."
  probe['sample_refs']+=['apparent-cue-counterexamples.json','apparent-cue-results.json','grader-final-results.json','delivery-apparent/accepted.json']
for cf in v['counterfactuals']:cf['sample_refs']=[p.replace('grader-all-results.json','grader-final-results.json') for p in cf['sample_refs']]
v['delivery']['sample_refs']+=['delivery-apparent/delivery.json'];v['delivery']['result']+=' All five independently replayed counterexamples also survive filtering.'
save('pedagogical-variation.json',v)
sys.path.insert(0,str(E));import importlib.util
schema= json.loads((R/'generate/pipeline/pedagogical-variation.schema.json').read_text())
# Schema validator may be supplied by the host interpreter, rather than generator dependencies.
try:
 import jsonschema
 jsonschema.Draft202012Validator(schema).validate(v)
 validation='Validated with jsonschema Draft202012Validator.'
except ImportError:
 def validate(x,s,path='$'):
  if '$ref' in s:raise ValueError('unexpected schema ref')
  if 'enum' in s:assert x in s['enum'],path
  t=s.get('type')
  if t=='object':
   assert isinstance(x,dict) and set(s.get('required',[]))<=set(x),path
   if s.get('additionalProperties') is False:assert set(x)<=set(s.get('properties',{})),path
   for k,a in x.items():
    if k in s.get('properties',{}):validate(a,s['properties'][k],path+'.'+k)
  elif t=='array':
   assert isinstance(x,list) and len(x)>=s.get('minItems',0),path
   for j,a in enumerate(x):validate(a,s['items'],f'{path}[{j}]')
  elif t=='string':assert isinstance(x,str) and len(x)>=s.get('minLength',0),path
  elif t in ('integer','number'):
   assert isinstance(x,int if t=='integer' else (int,float)) and not isinstance(x,bool),path
   assert x>=s.get('minimum',float('-inf')) and x<=s.get('maximum',float('inf')),path
 validate(v,schema);validation='Validated all constraints in the supplied schema with a local validator; no references in schema.'
refs=[]
def check_refs(x):
 if isinstance(x,dict):
  for k,a in x.items():
   if k=='sample_refs':
    for p in a:
     assert not pathlib.Path(p).is_absolute() and (E/p).is_file() and (E/p).stat().st_size>0,p;refs.append(p)
   else:check_refs(a)
 elif isinstance(x,list):
  for a in x:check_refs(a)
check_refs(v)
source=load('source-analysis.json')
scope={'source_refs':source['source_refs'],'operation':'Rank-two Gauss-Jordan reduction; select RREF or full one-parameter affine vector.','observed':'All 17 sources and tested variations retain three equations, x/y pivots, free z, rank two, single-select five-choice contract. Added q-74625 includes unit second pivot; q-131634 already has zero above it, as tutorial 3949 permits. Fresh signed/zero coefficients, constants and bounded affine values stay within the same method and arithmetic workload.','unsupported_source_families':[],'excluded_scope':'Adjacent inconsistent/one-pivot topics are boundaries, not assessed target families. Canonical example informs scope without an invented bank.'};save('scope-results.json',scope)
checks={
'source_replay':{'status':'passed','evidence_paths':['source-replay-results.json','replays.json','regression-verification.json','regression-current/evidence/source-coverage-results.json','revision-scope.json'],'details':'All 17 supplied cases replay with complete 85-choice banks and correct keys. Retained regression fails on the old omission and passes current. Source correction and formatting-only differences retained.'},
'math':{'status':'passed','evidence_paths':['math-results.json','supplemental-results.json','apparent-cue-results.json','review_math.py'],'details':'Independent exact checks pass for 96 generated records: visible equations, unique valid option, solution matrices and generated row-operation labels.'},
'variety':{'status':'passed','evidence_paths':['coverage-results.json','independent-samples.json','runner-batch.json','delivery-independent/delivery.json','delivery-batch/delivery.json'],'details':'Fresh samples cover all 17 profiles, both families, all five correct slots and signed/zero affine values. All 34 fresh and five exact batch records survive filtering; batch has five distinct RREFs.'},
'scope':{'status':'passed','evidence_paths':['scope-results.json','source-analysis.json','math-results.json'],'details':'Tested variations preserve rank-two 3x3 Gauss-Jordan reasoning, five-choice responses and comparable hard workload, including both added boundary profiles.'},
'grading':{'status':'passed','evidence_paths':['grader-final-input.json','grader-final-results.json'],'details':'Native learner grader accepts 96 independently checked correct choices and rejects 384 alternatives. All source fields are radio; free-entry notation is inapplicable.'},
'rendering':{'status':'passed','evidence_paths':['render/rendering.json','visual-inspection.json','rendered-choice-results.json','render/question-001.png','render/question-006.png','render/question-012.png','render/question-015.png','render/question-016.png'],'details':'Actual UI renders all 18 requested records, including exact batch, controlled pairs and both repaired source replays. Representative screenshots inspected.'},
'packaging':{'status':'passed','evidence_paths':['packaging-results.json','generator-rejection.json','relocation-samples.json','package-tree-before.json','package-tree-after.json'],'details':'Exact Python/SymPy dependency versions match. Deterministic CLI, relocation and invalid-parameter rejection pass. Complete package tree is unchanged.'},
'decision_variation':{'status':'passed','evidence_paths':['pedagogical-variation.json','counterfactual-results.json','decision-probe-results.json','apparent-cue-results.json','learner-selection-results.json','delivery-supplemental/delivery.json','delivery-counterfactual/delivery.json','delivery-apparent/delivery.json'],'details':'Relevant and irrelevant controlled changes pass math, rendering and native grading. Conditional cue probes include explicit counterexamples for every apparent multi-item predictor. Exact batch tested separately. Selection support follows captured inputs and explicit fresh-learner/positive-hard-weight assumptions.'}}
result={'verdict':'accepted','summary':'The two missing source profiles are repaired. All eight checks pass; no concrete remaining defect demonstrated. Package unchanged; no publication or database writes.','source_analysis':{k:source[k] for k in ['skill','reasoning_steps','invariants','permitted_variations','source_refs','evidence_paths']},'checks':checks,'findings':[]}
for c in checks.values():
 for p in c['evidence_paths']:assert (E/p).is_file() and (E/p).stat().st_size>0,p
save('evidence-contract.json',{'passed':True,'schema_validation':validation,'sample_ref_count':len(refs),'all_sample_refs_nonempty_relative':True,'package_unchanged':True,'review_binding':{'policy_version':2,'package_hash':'efd26d2bc2a7ec47782275b5ff299b0861808ba1274bc17b483ee76d3e32c300','batch_hash':'9a8c8bd00e509aef17ff88180eaf2885bc7b89345a91ba295ed9a79ea52f60db','source_hash':'a01855f60dce86df1a79af3fa8438b7082f187d0b36e82fb096c2a2a301db539','inventory_hash':'2cfc595642d94e4f3b03657e6cc267101125cad88344415a79648b7008e3f59e','engine_hash':'672f80847254dc41dcd11347ced250b1a1266dc90c24cef9f2d1e9688dfa7d6a'}})
py=str(R/'.venv/bin/python')
commands=[[py,'audit.py'],[py,'supplemental.py'],[str(R/'generate/runs/current/check-engine'),'grader-final-input.json','grader-final-results.json'],[py,'review_decisions.py'],[py,'challenge_apparent.py'],[py,'finalize_review.py']]
for label,name in [('independent','independent-samples.json'),('batch','runner-batch.json'),('supplemental','supplemental-records.json'),('counterfactual','counterfactual-records.json'),('apparent','apparent-cue-counterexamples.json')]:commands.append([py,str(R/'generate/pipeline/check_delivery.py'),'--input',name,'--source',str(B/'source/source.json'),'--inventory',str(B/'source/inventory.json'),'--difficulty','hard','--output','delivery-'+label,'--math-root','/media/jake/SSD/EDB/math'])
commands.append([py,str(R/'generate/pipeline/render_preview.py'),'--input','render-input.json','--output','render','--limit','18','--asset-root',str(P),'--math-root','/media/jake/SSD/EDB/math'])
save('commands.json',{'cwd':str(E),'environment':{'PYTHONDONTWRITEBYTECODE':'1'},'commands':commands,'regression_commands':'regression-verification.json; scripts execute on evidence-local copies so author writes remain under evidence_root.','order':'audit; supplemental; delivery filters; render; review_decisions; challenge_apparent; final grader and apparent delivery; finalize. Results include saved records and explicit seeds/parameters.'})
save('review-result.json',result);save('result.json',result)
(E/'session-state.md').write_text('Completed: ACCEPTED. All eight checks pass. Retained omission reproduced on old snapshot and absent current; all 17 full source banks replay. 96 independent exact-math records; native grader accepts 96 keys/rejects 384 alternatives. Actual UI renders 18, representative screenshots inspected. Actual shared delivery retains all tested records, including exact five-record batch. Conditional apparent predictors disproved with ordinary-seed examples. Captured inventory: no affected generated instance demonstrated; historical seed reproduction limited by missing metadata. Complete package tree unchanged; no publication or DB writes. Final result: result.json; full evidence index in review-result.json.\n')
print(json.dumps({'verdict':result['verdict'],'checks':{k:v['status'] for k,v in checks.items()},'math_records':96,'native_accepted':96,'native_rejected':384,'rendered':18,'package_unchanged':True,'schema_validation':validation}))
