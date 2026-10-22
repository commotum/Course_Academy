import json,pathlib,hashlib
E=pathlib.Path(__file__).resolve().parent;P=E.parent/'workspace'
def save(n,x):(E/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
# Inspected the generated screenshots and contact sheets, not only renderer status.
render=json.load(open(E/'render-all/rendering.json'));assert render['passed'] and len(render['cases'])==19
save('visual-inspection.json',{'renderer':'Unmodified ui/Learning.html and learning.js via shared render_preview.py','rendered_records':19,'screenshot_inspected':['render-all/contact-1.png','render-all/contact-2.png','render-all/contact-3.png','render-all/contact-4.png'],'cases':'1-13 cover each construction pair, 14-18 actual batch, 19 option-order counterfactual of 1.','observed':['All four theorem clauses and the stacked equivalence fit inside the question and solution panels.','Every blank is visible at its intended location; moved-blank pairs change the rendered prompt and mathematical answer.','All five radio choices readable; spaces, dimensions, zero set and scalar zero distinct.','Solutions contain the completed theorem and matching final missing expression.','No broken images, MathJax errors, javascript errors or missing glyphs reported.'],'limitations':'Desktop preview at renderer viewport; no separate mobile-layout certification.'})
# Source/scope reasoning is distinct from item math or source replay claims.
save('scope-review.json',{'source_refs':['lesson tutorial 17592186125780 / step 4620379b-2eed-5dd7-bf3a-9edf0b4aea79','canonical fff1daf8-5a1f-54c9-90d7-87710ca00d23','all 16 practice IDs in source-analysis.json'],'observed':'Generated task remains one missing fragment in the same four-clause theorem with five radio options and a full-theorem reminder solution. No computations, proof, rectangular matrix analysis or new operators.','canonical_extension':'dim Null(A) target is canonical-solution-backed; five-choice radio format is inherited from every practice item, not claimed present in canonical record.','corrections':'New banks remove six source/boundary ambiguities without removing any target or restricting n>=1. See source-corrections.json.','finite_domain':'11 semantic target contracts, 13 bank/target constructions; alternate choice order is not semantic variety. This is defensible finite theorem recognition practice.','difficulty':'Easy only; moderate/hard reject explicitly.','instructional_reason_for_fixed_roles':'Invertibility, n, and zero are the lesson theorem facts. Changing the source label A or row order is eligible presentation variation but not needed to exercise its finite recall targets.'})
actual={str(p.relative_to(P)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(P.rglob('*')) if p.is_file()}; before=json.load(open(E/'package-hashes-before.json'));assert actual==before
save('package-integrity.json',{'unchanged':True,'file_count':len(actual),'baseline':'package-hashes-before.json','after':actual,'external_outputs':'Review files only under evidence_root. Python bytecode disabled; author checks executed from an exact copy below evidence_root; TMPDIR below evidence_root; no database/publish invocation.'})
# Validate supplied pedagogical evidence schema, using installed jsonschema if available.
pv=json.load(open(E/'pedagogical-variation.json'));schema_path=pathlib.Path('/home/jake/Developer/Course_Academy/generate/pipeline/pedagogical-variation.schema.json');schema=json.load(open(schema_path))
def validate(v,s,path='$'):
 typ=s.get('type')
 if typ=='object':
  assert isinstance(v,dict),path
  assert all(k in v for k in s.get('required',[])),path
  if s.get('additionalProperties')==False:assert not(set(v)-set(s.get('properties',{}))),path
  for k,z in v.items():
   if k in s.get('properties',{}):validate(z,s['properties'][k],path+'.'+k)
 elif typ=='array':
  assert isinstance(v,list) and len(v)>=s.get('minItems',0),path
  for i,z in enumerate(v):validate(z,s.get('items',{}),path+f'[{i}]')
 elif typ=='string':assert isinstance(v,str) and len(v)>=s.get('minLength',0),path
 elif typ=='integer':assert type(v)==int,path
 elif typ=='number':assert isinstance(v,(int,float)),path
 if 'enum' in s:assert v in s['enum'],path
 if 'minimum' in s:assert v>=s['minimum'],path
 if 'maximum' in s:assert v<=s['maximum'],path
validate(pv,schema)
refs=[]
def walk(v):
 if isinstance(v,dict):
  for k,z in v.items():
   if k=='sample_refs':
    for r in z:
     p=E/r;assert not pathlib.Path(r).is_absolute() and p.is_file() and p.stat().st_size>0,r;refs.append(r)
   else:walk(z)
 elif isinstance(v,list):
  for z in v:walk(z)
walk(pv)
assert json.load(open(E/'grader-report.json'))['accepted_checks']==31
assert json.load(open(E/'grader-report.json'))['rejected_checks']==124
for f,n in [('delivery-fresh/delivery.json',13),('delivery-batch/delivery.json',5),('delivery-duplicates/delivery.json',1)]:assert json.load(open(E/f))['accepted_count']==n
assert len(json.load(open(E/'source-replay-results.json')))==16
save('evidence-contract.json',{'pedagogical_schema_valid':True,'schema':str(schema_path),'sample_refs_verified':len(refs),'unique_nonempty_sample_files':sorted(set(refs)),'package_unchanged':True,'grader_counts':{'accepted':31,'rejected':124},'rendered_cases':19,'source_replays':16})
checks={
'source_replay':{'status':'passed','evidence_paths':['source-analysis.json','source-replays.json','source-replay-results.json','source-corrections.json'],'details':'All 16 captured prompts, solutions and complete five-choice banks replay exactly. Ambiguous originals and n=1 collisions are explicitly corrected in generated banks; no target family omitted. Canonical bank is absent and its radio extension is identified.'},
'math':{'status':'passed','evidence_paths':['audit.py','math-results.json','runner-batch.json'],'details':'51 records, including all 13 construction pairs and the exact five-record batch, independently checked from visible expressions using rational matrix witnesses at n=1,2,4 and a symbolic theorem argument. Exactly one correct choice and matching solution in each.'},
'variety':{'status':'passed','evidence_paths':['fresh-samples.json','coverage-stage-results.json','delivery-fresh/delivery.json','delivery-batch/delivery.json','selection-results.json'],'details':'Fresh seeds 27,814,20261021 cover all 11 target roles and 13 bank/target pairs; all survive shared delivery as 13 distinct records. Exact batch retains five different targets. Selection rules and explicit exclusion/weight scenarios inspected; live policy/history unavailable.'},
'scope':{'status':'passed','evidence_paths':['source-analysis.json','scope-review.json','source-corrections.json'],'details':'Easy theorem recognition, one blank and five radio choices preserved. Fixed theorem facts are instructional; no added computational skill. Finite capacity of 11 target contracts is explicit.'},
'grading':{'status':'passed','evidence_paths':['grader-input.json','grader-report.json','counterfactuals.json'],'details':'Real native grade_field: 31 valid radio selections accepted, 124 independently wrong selections rejected, zero unresolved. Covers all constructions, exact batch and 13 irrelevant order counterfactuals. No free-entry field exists.'},
'rendering':{'status':'passed','evidence_paths':['render-all/rendering.json','visual-inspection.json','render-all/contact-1.png','render-all/contact-2.png','render-all/contact-3.png','render-all/contact-4.png'],'details':'Actual unmodified UI rendered all 13 constructions, five batch records and an order variant. Screenshots inspected: visible blanks, complete theorem, readable options and matching solutions; no reported rendering errors.'},
'packaging':{'status':'passed','evidence_paths':['runtime-results.json','dependency-check.json','legacy-regression.json','author-check-run.json','package-integrity.json','reproduce.sh'],'details':'Exact Python 3.13.5 standard-library dependency contract verified. Counts 0,1,5,11 succeed; 12 and negative counts reject. Deterministic replay and declared-files-only relocation pass. Retained old zero-record defect reproduced; current returns five. Package unchanged.'},
'decision_variation':{'status':'passed','evidence_paths':['pedagogical-variation.json','counterfactuals.json','shortcut-results.json','coverage-stage-results.json','selection-results.json','evidence-contract.json'],'details':'Same-bank moved-blank pairs change correct expressions and rendered content together; reordered choices preserve responses. Conditional bank/position and constant-answer probes show no demonstrated incidental bypass. Adjective recognition is a justified fixed theorem fact; batch singleton groups are not claimed balanced.'}}
for c in checks.values():
 for f in c['evidence_paths']:assert (E/f).is_file() and (E/f).stat().st_size>0
account=json.load(open(E/'source-analysis.json'))
result={'verdict':'accepted','summary':'No demonstrated current-generator defect. All eight checks pass for the finite easy recognition family and the exact five-record batch; live learner-state conclusions remain limited to inspected rules and explicit scenarios. Package unchanged.','source_analysis':{'skill':account['skill'],'reasoning_steps':account['reasoning_steps'],'invariants':account['invariants'],'permitted_variations':account['permitted_variations'],'source_refs':account['source_refs'],'evidence_paths':['source-analysis.json','source-corrections.json','scope-review.json']},'checks':checks,'findings':[]}
save('review.json',result)
(E/'session-state.md').write_text('Completed review: accepted, all eight checks pass within documented limits. Source account written before package inspection. 16 source bank replays; 51 independent math records; native grader 31 accepted/124 rejected; all 19 actual UI previews inspected; actual five-record batch survives shared delivery. Fresh sample 33 -> 13 after deduplication covers all bank/target pairs. Legacy count failure reproduced and repaired behavior verified. Inventory contains only original sources. Conditional learner-selection scenarios examined without DB writes; live policy/history unavailable. Package hashes unchanged. Final report review.json; reproduction reproduce.sh.\n')
print(json.dumps({'verdict':result['verdict'],'checks':{k:v['status'] for k,v in checks.items()},'package_unchanged':True,'evidence_contract_valid':True}))
