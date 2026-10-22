import json,pathlib,hashlib
E=pathlib.Path(__file__).resolve().parent
def read(n):return json.loads((E/n).read_text())
def save(n,x):(E/n).write_text(json.dumps(x,indent=2)+'\n')
s=read('source-analysis.json')
report={
 'verdict':'accepted',
 'summary':'Both retained defects are resolved. All eight checks passed, including the exact five-record batch. No new concrete failure was demonstrated; package files remained unchanged.',
 'source_analysis':{k:s[k] for k in ['skill','reasoning_steps','invariants','permitted_variations','source_refs','evidence_paths']},
 'checks':{
  'source_replay':{'status':'passed','evidence_paths':['source-analysis.json','source-replay.json','source-replay-records.json','strict-regressions.json','executable-regression-verification.json'],'details':'All 14 complete captured banks, keys, prompts and solutions replay after notation normalization, including restored q-105158. q-34574 lacks captured key/solution and the canonical lacks a bank; those evidence gaps remain explicit.'},
  'math':{'status':'passed','evidence_paths':['review.py','math.json','counterfactual-results.json','delivered-grader-input.json'],'details':'269 records passed independently parsed exact Fraction arithmetic, unique choice/key checks, every worked-solution vector, signed division and final component arithmetic. Includes all five batch items and controlled target/evidence changes.'},
  'variety':{'status':'passed','evidence_paths':['fresh-records.json','target-records.json','delivered-probes.json','delivery-fresh/delivery.json','delivery-batch/delivery.json','learner-selection.json','resampling-results.json'],'details':'168 fresh items span 14 profiles; all 53 eligible profile/target cases exercised. Actual filtering retains 168/168 and batch 5/5. Semantic duplicates are rejected and retried; learner selection is examined conditionally on explicit fresh all-easy pools.'},
  'scope':{'status':'passed','evidence_paths':['scope.json','source-analysis.json','fresh-records.json','source-replay.json'],'details':'Preserves one-vector isolation, three/four components, integer arithmetic, optional two-component sum/difference and five-choice radio response. Only evidenced easy difficulty is supported; no extra operator or reasoning stage introduced.'},
  'grading':{'status':'passed','evidence_paths':['grader-input.json','grader-report.json','delivered-grader-input.json','delivered-grader-report.json'],'details':'Native learning::grade_field accepted 62 correct selections and rejected 248 alternatives; normalized delivered batch separately accepted 5 and rejected 20. Controlled relevant and irrelevant pairs included. Free-entry equivalence is inapplicable to these radio fields.'},
  'rendering':{'status':'passed','evidence_paths':['render-inspection.json','render/rendering.json','render-records.json','ui-choice-order.json'],'details':'Actual unmodified UI rendered 12 cases; every screenshot inspected. Covers all five batch records, target reversal/retargeting, changed correct roles at a fixed bank, and irrelevant-coordinate pair. Math, controls and explanations display correctly; actual UI shuffle independently matched all saved DOMs.'},
  'packaging':{'status':'passed','evidence_paths':['packaging.json','package-integrity.json','external-output.json','relocated-records.json','resampling-results.json','commands.json'],'details':'Declared exact Python 3.13.5 and SymPy 1.14.0 match installed versions. Deterministic replay, invalid-input rejection, bounded resampling and manifest-only relocation pass. No unexpected runtime outputs; entire original package file hash map unchanged.'},
  'decision_variation':{'status':'passed','evidence_paths':['pedagogical-variation.json','retained-shortcuts-after-delivery.json','simple-cues.json','ui-choice-order.json','counterfactual-results.json','executable-regression-verification.json'],'details':'Original executable fails the retained strict tests; current executable passes them. Fresh delivered old-cue successes are 5/12, 0/12 and 1/12. Fixed-bank controls make every choice correct through relevant data changes. Exact batch and conditional UI/rank/shape/sign probes examined separately; finite-sample coincidences and live-selection limits are disclosed.'}
 },
 'findings':[]
}
for name,c in report['checks'].items():
 assert c['status']=='passed' and c['evidence_paths']
 for p in c['evidence_paths']:assert (E/p).is_file() and (E/p).stat().st_size>0,(name,p)
assert set(report['checks'])=={'source_replay','math','variety','scope','grading','rendering','packaging','decision_variation'}
save('result.json',report)
cmd=read('commands.json');cmd['commands']+=['/home/jake/Developer/Course_Academy/.venv/bin/python resampling.py','python3 make_report.py'];save('commands.json',cmd)
before=read('package-before.json');P=E.parent/'workspace'
now={str(p.relative_to(P)):hashlib.sha256(p.read_bytes()).hexdigest() for p in P.rglob('*') if p.is_file()}
assert now==before
(E/'session-state.md').write_text('Review complete: accepted. result.json contains all eight passed checks with independent evidence. Both retained defects fail on the hash-verified old executable and pass current strict tests. 14 complete source banks replay; 269 exact-math records; actual delivery fresh 168/168 and exact batch 5/5; 335 native radio outcomes across raw/control and delivered batches; 12 actual UI screenshots inspected; actual UI choice ordering verified; semantic duplicate retry/exhaustion tested. Captured inventory verified originals only; affected-inventory.json empty on that basis. Whole package hash map unchanged; no database/publication writes. Remaining limitations: incomplete source bank evidence for q-34574/canonical, finite sampling, unavailable live policy/history/future entity IDs.\n')
print(json.dumps({'verdict':report['verdict'],'checks':list(report['checks']),'findings':0,'package_unchanged':True}))
