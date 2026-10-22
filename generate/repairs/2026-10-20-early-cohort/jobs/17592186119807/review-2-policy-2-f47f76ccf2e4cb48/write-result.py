import json,pathlib,hashlib
E=pathlib.Path(__file__).resolve().parent;J=E.parent;P=J/'workspace'
def load(p):return json.loads(pathlib.Path(p).read_text())
def check(paths,details):
 for p in paths:assert (E/p).is_file() and (E/p).stat().st_size>0,p
 return {'status':'passed','evidence_paths':paths,'details':details}
a=load(E/'source-analysis.json')
result={
'verdict':'accepted',
'summary':'All eight checks pass. Retained defects reproduce on historical failures and are repaired in the current package and exact delivered batch. No current defect was demonstrated; package files are unchanged.',
'source_analysis':{k:a[k] for k in ['skill','reasoning_steps','invariants','permitted_variations','source_refs','evidence_paths']},
'checks':{
'source_replay':check(['source-analysis.json','source-replay.json','source-records.json','source-math-results.json'],'All 14 supplied exercise prompts, complete five-choice banks and worked methods replay. The q-105163 arithmetic correction is verified. Canonical example has no captured answer field; its sum -10 is independently confirmed.'),
'math':check(['math-results.json','solution-math-results.json','sign-counterfactual-results.json','targeted-tests.log'],'Fraction arithmetic independently verifies 157 source/control/fresh/boundary/batch records. An additional four sign controls and ten fresh batch items pass; 147 written-solution candidate/check sequences agree with displayed vectors.'),
'variety':check(['coverage.json','revision-scope.json','resampling-results.json','shortcut-results.json','delivery-batch/accepted.json'],'Controlled cases retain both consistency outcomes and all four numeric key ranks within every source profile. New rejection logic retains all four sign/consistency cases in two fresh requested-size batches. The exact delivered batch defeats the retained sign and numeric-order strategies.'),
'scope':check(['source-analysis.json','scope-results.json','boundary-records.json','revision-scope.json'],'The conservative finite source coefficient profiles preserve two coefficients, three components, elementary substitution/elimination, a remaining-row consistency check and one five-choice radio response. Only batch selection changed since the previous review.'),
'grading':check(['grader-input.json','grader-report.json','sign-counterfactual-records.json'],'Actual native learner grader passes 161 accepted and 644 rejected radio responses, including every alternative on relevant/irrelevant controls and normalized batch records. No free-entry fields occur, so equivalent free-entry notation is inapplicable.'),
'rendering':check(['render-final/rendering.json','render-inspection.json','render-records.json'],'All 17 actual UI renders pass and their screenshots were inspected: the exact batch, controlled response flips and irrelevant changes, four restored source profiles and fractional boundary notation. No math or JavaScript errors.'),
'packaging':check(['packaging-results.json','relocation-records.json','package-integrity.json','retained-regressions.json','retained-sign-regression.json','author-check-rerun.log','author-batch-rerun.log'],'Exact installed Python 3.13.5 and SymPy 1.14.0 match the nested manifest. Deterministic replay, relocation, boundary rejection and read-only author-check reruns pass. Historical failures are reproduced, rather than inferred from passing current tests. Every package file hash remains unchanged.'),
'decision_variation':check(['pedagogical-variation.json','shortcut-results.json','selection-results.json','retained-sign-regression.json','resampling-results.json','delivery/delivery.json','delivery-batch/delivery.json','inventory-audit.json','affected-inventory.json','evidence-contract.json'],'Relevant evidence changes update prompt, explanation and native grading; irrelevant order/distractor changes preserve the response. Controls filter 138->136; exact batch 5->5. In the exact batch, nonpositive banks have two No solution and one numeric key; positive-only banks have one of each. Fresh batches preserve all four cases after filtering. Selection rules and history exclusion were inspected with conditional synthetic-ID tests. Captured inventory contains 14 source originals and no stored generated instances. Future histories/inventory and singleton cue groups limit these finite conclusions.')},
'findings':[]}
(E/'result.json').write_text(json.dumps(result,indent=2)+'\n')
(E/'reproduction.md').write_text('''Independent revision review. Run from this evidence directory with PYTHONDONTWRITEBYTECODE=1.

Context Python: /home/jake/Developer/Course_Academy/.venv/bin/python

- `review.py`: confirmed source replay, independent Fraction mathematics, controlled consistency/rank cases, fresh seed104729, boundaries, retained original failures, determinism, relocation and inventory comparison.
- `delivery-tests.py`: builds native grader and UI inputs after shared delivery. Run shared `generate/pipeline/check_delivery.py` with raw-records.json and batch.json, the supplied source and inventory paths, --difficulty moderate and outputs delivery / delivery-batch first.
- `targeted-tests.py`: fresh batch seeds104729 and20261021, resampling traces, exact sign-counterexample controls and original-fails/current-passes strict regression. It appends the four sign controls to grader/render inputs; run once after delivery-tests.py.
- `batch_regression.py --records original-sign-batch.json` must fail with3/3. The same command with delivery-batch/accepted.json or sign-counterfactual-records.json must pass. Historical failure records are complete and copied from the prior matched review.
- `<repo>/generate/runs/current/check-engine grader-input.json grader-report.json`: actual native learner grader; final805 outcomes pass.
- `<context-python> <repo>/generate/pipeline/render_preview.py --input render-records.json --output render-final --limit 17 --math-root /media/jake/SSD/EDB/math`: actual UI render,17 inspected screenshots. Contact sheets preserve screenshot pixels.
- `complete-review.py`: parses written solutions with Fraction arithmetic, computes cue probes and compares actual delivery/selection stages. Uses system python3 jsonschema for evidence-contract validation, because context Python lacks that optional review-only package.
- `author-check-rerun.py` and `author-batch-rerun.py` retain supplied tests with only import and output paths redirected to this evidence directory. These supplement independent checks and do not establish acceptance alone.
- `write-result.py`: serializes the eight independent checks and verifies evidence paths and final package hashes.

Current batch:5/5 survive actual publisher preparation with captured inventory basis5400. Publication preparation file is absent; no publication or database write occurred. Future entity IDs, policy weights and learner history were not supplied; selection conclusions are conditional on fresh moderate eligibility. No finite audit certifies absence of every shortcut.
''')
# Final integrity guard includes all tests and report writing.
before=load(E/'package-hashes-before.json');after={str(p.relative_to(P)):hashlib.sha256(p.read_bytes()).hexdigest() for p in P.rglob('*') if p.is_file()};assert before==after
for name,c in result['checks'].items():assert c['status']=='passed' and c['evidence_paths']
assert 'source-analysis.json' in result['source_analysis']['evidence_paths']
assert load(E/'affected-inventory.json')=={'affected_questions':[]}
(E/'session-state.md').write_text('Review complete. Verdict accepted in result.json. All eight checks pass, with finite-probe and future-history limits stated. Source14/14; independent math157 plus targeted14; written checks147; native grading161 accepted/644 rejected; actual UI17 inspected; delivery138->136 and exact5->5. Historical sign batch still fails3/3; current/control pass. Package byte hashes unchanged. No current defect demonstrated; captured inventory14 source originals only.\n')
print(json.dumps({'verdict':result['verdict'],'checks':len(result['checks']),'findings':0,'package_unchanged':True,'result':'result.json'}))
