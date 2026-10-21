import json,pathlib
R=pathlib.Path(__file__).resolve().parent
load=lambda n:json.load(open(R/n))
def check(status,paths,details):return {'status':status,'evidence_paths':paths,'details':details}
a=load('source-analysis.json')
result={'verdict':'revise','summary':'The old fractionless cue is repaired, but revised quotient banks expose a new prompt-blind answer-bank signature: 18/18 focused cases and the replacement batch’s quotient item. Mathematics and native grading pass; package files are unchanged.','source_analysis':{k:a[k] for k in ['skill','reasoning_steps','invariants','permitted_variations','source_refs','evidence_paths']},'checks':{
'source_replay':check('passed',['source-replay.json','source-replay-records.json'],'All ten complete captured source banks reproduce prompts, choices, correct values and solutions. The canonical radical has no captured answer bank; that evidence gap remains explicit.'),
'math':check('passed',['independent_checks.py','math-results.json','revision-records.json'],'Independent symbolic parsing verifies one separated equivalent choice and every worked stage on 81 records, including revised profiles, boundaries, counterfactuals and exact batch.'),
'variety':check('failed',['generation-summary.json','revision-records.json','bank-shortcut-results.json','delivery-selection.json'],'All six easy families and both quotient profiles survive filtering, but quotient-bank repetition patterns reveal the correct answer despite numerical variation and shuffling.'),
'scope':check('passed',['scope-results.json','runtime-changes.json','independent-records.json'],'Changed choices retain the source algebra, five-equation radio contract and easy workload. No integration is added. Unchanged moderate/hard families were covered by a small regression sample.'),
'grading':check('passed',['grader-input.json','grader-report.json','revision-counterfactual-results.json'],'The actual native grader accepted 81 correct choices and rejected 324 alternatives. Relevant shared-choice truth flips and irrelevant shuffles pass. All fields are radio; free-entry equivalents are inapplicable.'),
'rendering':check('passed',['render-all/rendering.json','visual-inspection.json','render-contact-sheet.png','render-all/question-003.png','render-all/question-021.png'],'Actual UI rendered 32 records. Inspected screenshots show readable equations, controls and explanations, including changed pairs and the batch shortcut.'),
'packaging':check('passed',['packaging.json','package-integrity.json','runtime-changes.json','retained-regression-verification.json','commands.md'],'Exact Python 3.13.5/SymPy 1.14.0 declarations match runtime. Determinism, relocation and invalid-input rejection pass. The retained check fails the previous target and passes current. Package hashes remain unchanged.'),
'decision_variation':check('failed',['pedagogical-variation.json','bank_shortcut.py','bank-shortcut-results.json','minimal_repro.py','minimal-reproduction-records.json','minimal-reproduction-results.json','delivery-selection.json','affected-inventory.json','inventory-probe.json'],'Modal y-power plus modal RHS identifies the key in both quotient profiles: 18/18 focused and 18/18 accepted quotient controls. The power/sign profile also leaks the key as the shortest of three same-LHS rows. Both cues solve the exact batch quotient. All captured inventory was inspected for this family-specific failure; none of its six generated entries is a revised quotient instance.')},'findings':[{'kind':'decision_shortcut','description':'Both revised quotient profiles make the correct dependent power appear four times and its RHS three times, allowing prompt-blind modal-component selection. In quotient-power-sign, the correct equation is also always the shortest of the three rows sharing one left side. This succeeds on 18/18 focused quotient cases, 18/18 accepted quotient controls, and batch question 4cc34a53-2d0e-5e5d-9f42-8f3c31da05f8. This is a family construction defect and a concrete batch failure, not a claim that the cue solves all five batch members.','source_refs':['31bffd11-cf10-5855-9455-e621eb1969bd (q-158025)','7037401f-27c0-588d-a952-7eb3ef7b14ef (q-158030)','Tutorial 6767 / 56fc1c96-3599-5022-8d83-60d4188ccf07: identify h(x)g(y), then (1/g(y))dy/dx=h(x).'],'reproduction':'From evidence_root run PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python minimal_repro.py; it exits 1. Exact minimal instance: generate_easy(seed=17, template="simple_quotient", parameters={"n":1}). With D=dy/dx, the bank is yD=1/x, yD=x, xD=y, yD=-x, y^2D=x. Hide the ODE and choose the shortest of the three yD rows: yD=x, the correct answer. bank_shortcut.py retains the two-profile attack and delivered measurements. The exact batch witness is seed=2404317989, template=exp_quotient, parameters={"base":4,"a":4,"n":4}.','requested_change':'Change quotient_bank’s family-wide distractor construction so correctness is not determined by modal component frequencies or by the unique shortest/sign-free RHS within a repeated-LHS subgroup. Vary eligible distractor and answer-bearing relationships while retaining both source families, exact observed replay, unique mathematical correctness and workload. Preserve the prior strict regression and adopt these new failing probes. Regenerate the affected batch item after repairing the rule; new numbers or option shuffles alone cannot resolve it.'}]}
(R/'result.json').write_text(json.dumps(result,indent=2,ensure_ascii=False))
# Evidence references and the required variation schema, checked without extra dependencies.
schema=json.load(open('/home/jake/Developer/Course_Academy/generate/pipeline/pedagogical-variation.schema.json'))
def validate(x,s,where='root'):
 if 'enum' in s:assert x in s['enum'],where
 t=s.get('type');types={'object':dict,'array':list,'string':str,'integer':int,'number':(int,float)}
 if t:assert isinstance(x,types[t]),where
 if t=='object':
  assert all(k in x for k in s.get('required',[])),where
  if s.get('additionalProperties') is False:assert set(x)<=set(s['properties']),where
  for k,v in x.items():
   if k in s.get('properties',{}):validate(v,s['properties'][k],where+'.'+k)
 if t=='array':
  assert len(x)>=s.get('minItems',0),where
  for v in x:validate(v,s['items'],where+'[]')
 if t=='string':assert len(x)>=s.get('minLength',0),where
 if t in ('integer','number'):
  assert x>=s.get('minimum',-float('inf')) and x<=s.get('maximum',float('inf')),where
validate(load('pedagogical-variation.json'),schema)
refs=[]
def walk(x):
 if isinstance(x,dict):
  for k,v in x.items():
   if k in ['evidence_paths','sample_refs']:refs.extend(v)
   else:walk(v)
 elif isinstance(x,list):
  for v in x:walk(v)
walk(result);walk(load('pedagogical-variation.json'))
for p in refs:
 assert not pathlib.Path(p).is_absolute(),p
 assert (R/p).is_file() and (R/p).stat().st_size>0,p
assert len(result['checks'])==8
(R/'contract-check.json').write_text(json.dumps({'variation_schema_passed':True,'all_evidence_paths_nonempty':True,'checked_reference_count':len(refs),'eight_checks_present':True},indent=2))
(R/'session-state.md').write_text('Review complete: revise. New modal-component and repeated-LHS shortest-row cues in both revised quotient families; minimal seed17,n1 and exact batch exp quotient reproduced. Six checks passed; variety and decision_variation failed. Source replay 10/10, independent math81/81, native81 accepted/324 rejected, UI32 rendered and screenshots inspected. Shared delivery 40->28 controls and5->5 exactbatch. Captured generated inventory has no revised quotient; affected-inventory empty with bounded conclusion. Package hashes unchanged. Final result.json and all runnable scripts are here; contract-check.json confirms required paths/schema.\n')
print(json.dumps({'verdict':result['verdict'],'checks':{k:v['status'] for k,v in result['checks'].items()},'evidence_contract':'passed'}))
