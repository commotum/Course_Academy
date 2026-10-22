#!/usr/bin/env python3
import audit as a
import json
E=a.E
v=a.load('visual-inspection.json')
v['screenshots_inspected'] += ['render-delivered/question-001.png','render-delivered/question-002.png','render-delivered/question-004.png']
v['delivered_batch']='All five normalized records rendered successfully; representative screenshots inspected. Actual displayed correct positions are 4,3,4,5,4, so no constant position answers the batch. See actual-ui-order.json.'
a.save('visual-inspection.json',v)
source=a.load('source-analysis.json')
def check(paths,details):return {'status':'passed','evidence_paths':paths,'details':details}
report={
 'verdict':'accepted',
 'summary':'The revision fixes all retained failures and passes the eight checks for the requested easy batch. Three historically affected inventory records remain separately documented. Package files are unchanged.',
 'source_analysis':{k:source[k] for k in ['skill','reasoning_steps','invariants','permitted_variations','source_refs','evidence_paths']},
 'checks':{
  'source_replay':check(['source-analysis.json','source-replay.json','source-replay-records.json','retained-finding-regressions.json'],'All 13 source cases and 69 complete-bank choices replay exactly. Five previously missing profiles restored. Canonical e-4395 has no captured answer bank; its visible classification is independently verified.'),
  'math':check(['audit.py','math-results.json','counterfactual-records.json'],'192 records pass independent exact Fraction checks of visible matrices, keys, solution classifications and nonzero witnesses; includes 100 fresh instances, source replays, controlled roles and exact batch.'),
  'variety':check(['slot-coverage.json','controlled-role-results.json','controlled-role-records.json','shortcut-results.json'],'All 40 easy label assignments and 30 moderate subsets work at fixed dimensions. Every source profile varies answers in fresh ordinary samples. Easy control has 77 distinct unlabeled support banks; exact batch has four across five records.'),
  'scope':check(['source-analysis.json','scope-results.json'],'Requested easy records retain five 2x2/3x3 integer matrix choices, exactly one qualifier and the original zero-side inspection method. Unchanged authored hard extension is outside this requested-easy certification.'),
  'grading':check(['grader-input-final.json','grader-report-final.json','grader-command-final.json'],'Native learner grader agrees on 162 accepted and 369 rejected authored-choice checks, including controlled changes and normalized batch identities. 64 explicitly out-of-contract literal-radio diagnostics are correctly unresolved; no valid learner response remains unresolved. Source fields require choice IDs, with no free-entry equivalence contract.'),
  'rendering':check(['render/rendering.json','render-delivered/rendering.json','visual-inspection.json','actual-ui-order.json'],'18 actual-UI render cases pass; representative screenshots inspected. Controlled target changes, restored decimal/checkbox and subset-radio banks, explanations and exact normalized batch display correctly.'),
  'packaging':check(['packaging-results.json','runtime-results.json','package-before.json','package-after.json','evidence-validation.json'],'Exact Python 3.13.5 and SymPy 1.14.0 declarations match runtime. 100 deterministic replays, boundary/invalid-input checks and manifest-only relocation pass. All protected package file hashes remain unchanged.'),
  'decision_variation':check(['pedagogical-variation.json','counterfactual-results.json','stage-summary.json','delivery-control/delivery.json','delivery-batch/delivery.json','selection-results.json','actual-ui-order.json','author-preflight-verification.json','affected-inventory.json','generated-records.json','inventory-audit.json'],'Retained defects fail old code and pass the revision. Relevant target/role changes and irrelevant-entry preservation agree across math, native grading and rendering. All 80 controls and five exact batch records survive filtering. Tested conditional cues have counterexamples; prior size rule succeeds 10/60 applicable controls and 0/5 batch records. Selection analysis is conditional on captured easy-band rules and explicit histories; live weights/history are unavailable. Three historical affected inventory records are content-reverified separately.')
 },
 'findings':[]
}
for c in report['checks'].values():
 for p in c['evidence_paths']:assert (E/p).is_file() and (E/p).stat().st_size>0,p
assert a.hashes()==a.load('package-before.json')
a.save('result.json',report)
a.save('review-binding.json',{'policy_version':2,'package_hash':'036c5ec26ac6683e4b6b3d816fe43dcde013d935f897f9615c4b92bb2053fae0','batch_hash':'34d3096d2bf31219b27c8e36e43eb2216ecf44f5fd12b9cf0cda262ea8d3ccca','source_hash':'96d19341f1375cc8bb96bf885723dda62c2c56c4a958746a5a88763677015758','inventory_hash':'1fb894322f0cde77b0fd2ebc242f77fdf43f99fe902ee960221ecffb06ddff63','effective_difficulty':'easy','engine_hash':'dc1e0a8583ca33c6028bc0a641128ecc8e7896742189dd42b292170c9726bad9'})
with (E/'session-state.md').open('a') as f:f.write('Final result.json written and all eight check evidence paths verified nonempty. Delivered UI order checked separately after normalization. No current-package findings. Historical inventory defects remain in affected-inventory.json.\n')
print(json.dumps({'verdict':report['verdict'],'checks':{k:v['status'] for k,v in report['checks'].items()},'package_unchanged':True}))
