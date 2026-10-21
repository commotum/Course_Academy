import json,pathlib
E=pathlib.Path(__file__).resolve().parent
src=json.loads((E/'source-analysis.json').read_text())
result={
 'verdict':'revise',
 'summary':'Default answer banks expose a deterministic numeric-rank shortcut, including all five delivered runner records. Valid source IVPs are rejected, and two supplied source profiles are missing. Seven stored generated questions reproduce the rank weakness. Package unchanged.',
 'source_analysis':{k:src[k] for k in ['skill','reasoning_steps','invariants','permitted_variations','source_refs','evidence_paths']},
 'checks':{
  'source_replay':{'status':'failed','evidence_paths':['source-analysis.json','source-replay.json','source-replay-records.json','regression-results.json'],'details':'Nine older cases replay their prompts, normalized solutions, complete five-option banks and keys. Supplied q-107121/body and q-107123/pork profiles are absent; canonical bulb wording is unavailable. Its missing captured bank is explicitly documented.'},
  'math':{'status':'passed','evidence_paths':['math-results.json','solution-dependencies.json','scope-and-math.json'],'details':'76 independently computed numeric answers and72 solution dependency checks pass. Easy and moderate givens parsed from printed prompts. Documented outside-source unit typo is preserved only by the raw opt-in evidence profile; normal outside solutions use Fahrenheit consistently.'},
  'variety':{'status':'failed','evidence_paths':['fresh-samples.json','regression.py','regression-results.json','packaging.json'],'details':'Numerical slots vary across all five easy contexts, but rejecting any bank option outside ambient<choice<initial excludes valid source IVPs. Canonical ambient23,initial80,rate.25,time4 and body ambient21,initial40,rate.06,time4 both fail Whole bank temperature-domain violation.'},
  'scope':{'status':'passed','evidence_paths':['source-analysis.json','scope-and-math.json','fresh-samples.json','runner-batch.json'],'details':'Requested easy records retain the explicit-rate initial-condition temperature evaluation, integer rounding, five-choice radio contract and separation-of-variables explanation. Moderate controls retain source calibration/inversion stages. No exhaustive scope certification of authored hard extensions is claimed.'},
  'grading':{'status':'passed','evidence_paths':['grader-input.json','grader-report.json','counterfactual-results.json'],'details':'Actual native learner grader passed130 option selections:26 independently checked correct choices accepted and104 distractors rejected, including relevant/irrelevant counterfactuals. Free-entry notation is inapplicable to the source radio contract.'},
  'rendering':{'status':'passed','evidence_paths':['render-records.json','render/rendering.json','render-counterfactuals/rendering.json','rendering-inspection.json','render/question-001.png','render-counterfactuals/question-002.png','render-counterfactuals/question-005.png'],'details':'Actual unmodified UI rendered11 cases, including all five runner records and all controlled pairs. Representative full screenshots inspected; math, radio controls and worked solutions display correctly.'},
  'packaging':{'status':'passed','evidence_paths':['packaging.json','relocated-records.json','package-integrity.json','commands.txt'],'details':'Declared exact Python3.13.5 and nested sympy1.14.0 match runtime. Relocated entrypoint plus packaged source dependency runs deterministically without external assets. Invalid-input rejection exercised. Package file hashes unchanged; no database writes or publication.'},
  'decision_variation':{'status':'failed','evidence_paths':['pedagogical-variation.json','shortcut-results.json','delivery-selection.json','delivery-batch/accepted.json','delivery-fresh/accepted.json','affected-inventory.json','generated-records.json'],'details':'Choose median succeeds50/50 fresh easy samples,10/10 within each easy template, and5/5 exact runner survivors. Choose second-largest succeeds12/12 moderate samples and7/7 exactly replayed stored generated target-time records. Relevant time/target changes and irrelevant context changes update correctly but retain these answer-producing shortcuts. Actual delivery filters and conditional learner-selection rules cannot eliminate the invariant.'}
 },
 'findings':[
  {'kind':'decision_shortcut','description':'Default easy construction always places two distractor values below and two above the correct value. Selecting the median temperature solves every accepted default easy instance without using the ODE. All five exact runner survivors exhibit this defect. Sampled moderate layouts and all seven stored generated target-time records similarly expose the second-largest-time rule. Option shuffling does not change numeric rank.','source_refs':['daa15db5-c1a1-535c-9031-79b2bb1e03e9','2b60de53-dea5-5dd2-908e-421b529445e3','6ff863d3-8088-512b-858b-b0b33302607f','8b0ed3c5-b3aa-5668-ae2c-48b159839332','tutorial f58653bc-cafb-532a-b92d-8183054c181b, separation and integration stages','generate/principles.md §2 meaningful variety'],
   'reproduction':'Run PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python regression.py. Minimal exact runner record9d4ab96c-d8a2-56aa-91e4-663ddd431436,seed1403253416,compressor,ambient20,initial96,k=.09,time12: options29,64,46,53,26; correct46 is median. See runner-batch.json and delivery-batch/accepted.json. inventory-audit.py exactly replays all7 records in generated-records.json; affected-inventory.json identifies their stored entities.',
   'requested_change':'Change the family-wide bank-construction rule so error recipes and their signed relations do not determine a fixed correct numeric rank within recognizable templates. Derive all keys/solutions from each instance, retain plausible distractors and source radio contracts, and replace the five shortcut-answerable runner records. Retain the strict rank regression and check delivered as well as raw samples.'},
  {'kind':'restriction','description':'Whole-bank physical-domain validation suppresses valid IVPs whenever the omit-ambient distractor is at or below ambient. With integer ambient A, that recipe forces every accepted easy correct answer above2A, a condition absent from the lesson and contradicted by the canonical bulb and stored body example. The model itself is valid; the fixed distractor set causes rejection.','source_refs':['e3e001a8-9294-59a4-82e6-b1122afdc72f','44b64320-501f-5d6a-b8c7-b8cf6a960fc2','tutorial da7cd802-d46b-546f-bdc3-8a783a8bb999: solution approaches ambient from above'],
   'reproduction':'regression.py reproduces generate("easy",84199,"coffee",parameters={"ambient":23,"initial":80,"rate":"0.25","time":4}) -> ValueError("Whole bank temperature-domain violation"), although the canonical result is44. The same call with21,40,.06,4 rejects the body source result36. Complete inputs and outputs are in regression-results.json.',
   'requested_change':'Retain these valid source parameter combinations. Construct a suitable full bank for the IVP instead of conditioning the IVP domain on every fixed misconception recipe surviving the physical-domain filter; preserve source-level workload and the strict acceptance tests.'},
  {'kind':'source_fidelity','description':'The packaged snapshot/profile catalog covers nine older questions and omits two supplied current source cases: body q-107121 and pork q-107123. Both explicit source profiles fail before construction, so complete source replay is not established.','source_refs':['44b64320-501f-5d6a-b8c7-b8cf6a960fc2 (q-107121)','4360bcb1-959b-53b1-855f-91f5d582be11 (q-107123)'],
   'reproduction':'regression.py calls generate("easy",84199,profile="q-107121") and generate("moderate",84199,profile="q-107123"); both raise Unknown explicit observed bank profile. source-replay.json records9 successful older replays and the two missing source IDs.',
   'requested_change':'Add the two supplied source layouts and original-parameter profiles, including their complete banks and worked-solution stages, and verify them independently against the current source. Keep the documented Fahrenheit-label correction for q-107122 in served content.'}
 ]}
(E/'review.json').write_text(json.dumps(result,indent=2,ensure_ascii=False))
# Minimal schema interpreter for the provided contract, with no new dependencies.
schema=json.loads(pathlib.Path('/home/jake/Developer/Course_Academy/generate/pipeline/pedagogical-variation.schema.json').read_text())
def validate(x,s,path='$'):
 typ=s.get('type');types={'object':dict,'array':list,'string':str,'integer':int,'number':(int,float),'boolean':bool}
 if typ:assert isinstance(x,types[typ]),(path,typ)
 if 'enum' in s:assert x in s['enum'],path
 if isinstance(x,dict):
  assert all(k in x for k in s.get('required',[])),path
  if s.get('additionalProperties') is False:assert set(x)<=set(s.get('properties',{})),path
  for k,v in x.items():
   if k in s.get('properties',{}):validate(v,s['properties'][k],path+'.'+k)
 if isinstance(x,list):
  assert len(x)>=s.get('minItems',0),path
  for i,v in enumerate(x):validate(v,s.get('items',{}),path+f'[{i}]')
 if isinstance(x,str):assert len(x)>=s.get('minLength',0),path
 if isinstance(x,(int,float)):
  assert x>=s.get('minimum',float('-inf')) and x<=s.get('maximum',float('inf')),path
variation=json.loads((E/'pedagogical-variation.json').read_text());validate(variation,schema)
def refs(x):
 if isinstance(x,dict):
  for k,v in x.items():
   if k in ['sample_refs','evidence_paths']:
    for p in v:assert (E/p).is_file() and (E/p).stat().st_size>0,p
   refs(v)
 elif isinstance(x,list):
  for v in x:refs(v)
refs(variation);refs(result)
assert len(result['checks'])==8
assert json.loads((E/'package-integrity.json').read_text())['unchanged']
(E/'evidence-validation.json').write_text(json.dumps({'pedagogical_schema_passed':True,'evidence_paths_nonempty':True,'eight_checks_present':True,'package_unchanged':True},indent=2))
print('Saved review.json; schema, evidence references, eight checks and package integrity verified.')
