import json,pathlib,hashlib
root=pathlib.Path(__file__).resolve().parent
def read(p):return json.loads((root/p).read_text())
def save(p,x):(root/p).write_text(json.dumps(x,indent=2))
def check(status,paths,details):return {'status':status,'evidence_paths':paths,'details':details}
src=read('source-analysis.json')
result={'verdict':'revise','summary':'The radio answer-bank construction leaks the answer through option spacing. The shortcut succeeds on all 30 tested simple linear-root radios, including the actual batch radio, and three eligible stored questions. Mathematics, native grading, rendering and packaging checks passed.','source_analysis':{k:src[k] for k in ['skill','reasoning_steps','invariants','permitted_variations','source_refs','evidence_paths']},'checks':{
'source_replay':check('passed',['source-analysis.json','source-replays.json','source-replay-results.json','scope-results.json','canonical-record.json'],'Replayed all 17 captured questions and canonical e-182. All radio banks and mathematical keys match; prompt comparisons passed. Missing q-48846 key/solution/difficulty were independently assessed. Extra historical blank submissions in the newer snapshot are documented separately from visible response banks.'),
'math':check('passed',['math-results.json','verify_saved.py','counterfactual-results.json'],'Independently parsed displayed functions and differentiated 102 records, including all source replays, 75 fresh samples, the exact batch and controlled pairs. All keys and unique radio answers agree on the positive-radicand domain. Representative worked solutions checked visually.'),
'variety':check('passed',['coverage-results.json','independent-samples.json','batch-records.json'],'All 15 layouts sampled; every radio bank role 0..4 exercised. Coefficients, targets and positive/negative/zero quadratic slopes vary within supported scope. Adequate parameter variation does not cure the separate decision shortcut.'),
'scope':check('passed',['source-analysis.json','scope-results.json','coverage-results.json'],'No unsupported function operators or response formats found. Captured symbolic/evaluated difficulty families and the observed additive cubic family remain represented.'),
'grading':check('passed',['grader-input.json','grader-results.json'],'Native learning::grade_field completed 435 checks: 180 accepted equivalents/correct options and 255 rejected wrong entries/options; zero unresolved. Includes typed and LaTeX symbolic equivalents and unreduced numeric fractions.'),
'rendering':check('passed',['render/rendering.json','render-extra/rendering.json','visual-inspection.json'],'Actual unmodified UI rendered 15 records. Representative radio, blank, reciprocal, sum, negative and zero-slope screenshots inspected; no MathJax, image or JavaScript failures.'),
'packaging':check('passed',['packaging-results.json','package-before.json','commands.md'],'Exact installed Python 3.13.5 and SymPy 1.14.0 match manifest. CLI deterministic replay matches runner batch; relocated execution matches. Invalid-domain boundary rejection verified. Package hashes remain unchanged.'),
'decision_variation':check('failed',['pedagogical-variation.json','shortcut--independent-samples.json','shortcut-delivery-batch-accepted.json','counterfactual-results.json','delivery-batch/delivery.json','delivery-independent/delivery.json','selection-results.json','inventory-results.json'],'Correctness follows relevant counterfactuals and is invariant to option shuffling, but coefficient-times-option-spacing bypasses differentiation. It succeeds 5/5 within each of six simple linear-root radio templates, 10/10 easy survivors, and 1/1 applicable actual-batch member. Three eligible stored radios reproduce the same weakness. Difficulty-first selection supplies no mitigating bank filter.')},'findings':[
{'kind':'decision_shortcut','description':'The production scale_bank forces five consecutive multiples of the correct radical contribution divided by the visible coefficient a. For simple linear square-root radios, choose a times the common positive spacing; for reciprocal roots choose -a times it. This supplies the outer derivative and, for slopes, the target evaluation without doing either. Randomizing rank or displayed position does not remove the cue. The exact batch contains this defect in its single radio; its four blanks are not claimed bypassable by this strategy.','source_refs':['c8b46779-d19f-5cca-987d-5f500a9de334 (q-107360)','67f07fb8-cc06-5cda-9a1f-cc029f68242d (q-107288)','854ec833-4bc0-54f0-9210-c708a9342fef (q-48730)','tutorial 743ad997-8732-5c0f-9676-ff1d44f3b513: separately differentiate outer and inner, multiply, then substitute.'],'reproduction':'From evidence_root run /home/jake/Developer/Course_Academy/.venv/bin/python -B shortcut_probe.py batch-records.json (exit 1 is the retained failure). Minimal current case: seed 3173462203, easy, slope_sqrt_radio, a=7,b=37,t=-4. Prompt y=sqrt(37+7x), x=-4; sorted choices 1,7/6,4/3,3/2,5/3 have spacing 1/6. Read coefficient 7 and select 7*(1/6)=7/6 without evaluating the radicand or target. Shared delivery preserves it; see shortcut-delivery-batch-accepted.json. The script accepts an explicit candidate-records JSON file.','requested_change':'Replace the family-wide scale_bank rule with source-supported whole distractor banks whose numerical spacing does not reveal the outer derivative or evaluated factor. Preserve all source families, scope, legitimate targets and deterministic replay. Retain the executable spacing regression for each applicable template and prospective delivered batches; changing a seed, shuffling choices or fixing only this item is insufficient. The runner should regenerate its batch after package repair.'},
{'kind':'inventory','description':'Three currently captured, non-retired stored radios have the same answer-spacing defect. Independent generation plus publisher stable identities reproduces their exact IDs and content fingerprints: 90db644a-fd4a-5c58-b43a-e0452a6336d1 (entity 17592186657674), ab67789f-4616-5914-aa8d-59736a54c4f6 (17592186657677), and f48647ea-8ebd-5583-b713-aef1cac5a291 (17592186657682).','source_refs':['98cde390-f268-5ffd-9f2f-31f016a0c432 (q-107303)','854ec833-4bc0-54f0-9210-c708a9342fef (q-48730)','0ce97e32-c8a9-5155-bb70-6cb7385360f5 (q-107291)','inventory basis 5644'],'reproduction':'Run /home/jake/Developer/Course_Academy/.venv/bin/python -B inventory_probe.py. Parameters: sqrt_linear_radio a=4,b=3,bank_role=3; reciprocal_radio a=-2,b=12,bank_role=4; sqrt_constfirst_radio a=-7,b=-6,bank_role=3; all moderate, independent replay seed 70001. generated-records.json contains complete normalized records with matching stable question IDs and generation parameters. affected-inventory.json lists all three records. The replay seed is not asserted to be the unknown historical seed.','requested_change':'After repairing the generator, the runner should repair or retire these proven eligible generated records and refresh inventory for independent review. Preserve original source questions and history. No package-author database write or database-dependent regression is requested.'}
]}
save('review-result.json',result)
(root/'commands.md').write_text('''All commands run from evidence_root. Package/database content was not modified. PYTHONDONTWRITEBYTECODE=1 was used for package imports.

Python: /home/jake/Developer/Course_Academy/.venv/bin/python

- `python -B audit.py` saves deterministic samples, 17 replays, target/order pairs and packaging tests.
- `python -B verify_saved.py` independently checks displayed functions and positive-domain symbolic equivalents, then saves native-grader input. The initial audit parser did not simplify sqrt(u^3) versus u^(3/2); verify_saved.py explicitly corrects that review-tool limitation without changing package outputs.
- `/home/jake/Developer/Course_Academy/generate/runs/current/check-engine grader-input.json grader-results.json`
- `python -B shortcut_probe.py CANDIDATE_RECORDS.json` fails with exit 1 when the option-spacing cue succeeds. Used with independent-samples.json, batch-records.json, delivery-independent/accepted.json and delivery-batch/accepted.json.
- `python -B inventory_probe.py` reproduces affected stored IDs and complete normalized content.
- `python -B summarize_evidence.py` saves coverage, counterfactual, delivery-selection and pedagogical reports.

Shared delivery commands (no writes to database):

`python -B /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py --input batch-records.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output delivery-batch --asset-root ../workspace --math-root /media/jake/SSD/EDB/math`

Repeat with `--input independent-easy.json --output delivery-independent`.

Actual renderer commands:

`python -B /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input render-records.json --output render --asset-root ../workspace --math-root /media/jake/SSD/EDB/math`

`python -B /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input render-extra-records.json --output render-extra --limit 9 --asset-root ../workspace --math-root /media/jake/SSD/EDB/math`

Default first render handles six records; second handles the remaining nine. Screenshot inspection is recorded in visual-inspection.json.

No repair_history_file, repair_preflight_file, previous_review or publication preparation existed for this captured job; this was an initial independent review.
''')
# Validate the exact schema and every evidence reference, plus package invariance.
import jsonschema
schema=json.load(open('/home/jake/Developer/Course_Academy/generate/pipeline/pedagogical-variation.schema.json'))
jsonschema.validate(read('pedagogical-variation.json'),schema)
refs=[]
def walk(x):
 if isinstance(x,dict):
  for k,v in x.items():
   if k in ['evidence_paths','sample_refs']:refs.extend(v)
   else:walk(v)
 elif isinstance(x,list):
  for v in x:walk(v)
walk(result);walk(read('pedagogical-variation.json'))
for ref in refs:assert not pathlib.Path(ref).is_absolute() and (root/ref).is_file() and (root/ref).stat().st_size,ref
for x in read('affected-inventory.json')['affected_questions']:assert (root/x['evidence_path']).stat().st_size
pkg=root.parent/'workspace';after={str(p.relative_to(pkg)):hashlib.sha256(p.read_bytes()).hexdigest() for p in pkg.rglob('*') if p.is_file()}
assert after==read('package-before.json')
save('evidence-contract.json',{'pedagogical_schema_valid':True,'nonempty_evidence_references_checked':len(refs),'affected_inventory_records':3,'package_unchanged':True,'eight_checks_present':len(result['checks'])==8})
print('Verdict revise; schema and evidence paths valid; package unchanged.')
