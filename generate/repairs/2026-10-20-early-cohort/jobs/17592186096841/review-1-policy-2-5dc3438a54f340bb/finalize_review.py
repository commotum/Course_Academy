import json,hashlib
from pathlib import Path
import jsonschema
E=Path(__file__).resolve().parent;ROOT=Path('/home/jake/Developer/Course_Academy');W=E.parent/'workspace'
def read(p):return json.loads((E/p).read_text())
def save(p,o):(E/p).write_text(json.dumps(o,indent=2))
def check(files,detail):return {'status':'passed','evidence_paths':files,'details':detail}
a=read('source-analysis.json')
result={'verdict':'accepted','summary':'The canonical cubic-term restriction is resolved. All eight checks passed, including the exact five-record batch. Package files remained unchanged; no affected stored record was demonstrated.','source_analysis':{k:a[k] for k in ['skill','reasoning_steps','invariants','permitted_variations','source_refs','evidence_paths']},'checks':{
'source_replay':check(['source-analysis.json','source-replays.json','source-replay-results.json','repair-regression-results.json','author-old.log','author-current.log'],'All 12 practice cases replay complete banks with documented source corrections; canonical e-181 now reproduces its function and derivative. Retained regression fails on the old package and passes on the current package.'),
'math':check(['revision_checks.py','math-results.json','solution-results.json','boundary-records.json','boundary-results.json'],'79 independent prompt-derived exact checks passed; 36 quartic solutions independently checked. Both degree cases and coefficient/power boundaries passed.'),
'variety':check(['coverage-results.json','degree-rank-results.json','samples-independent.json','reuse-provenance.json','changed-files.json'],'Fresh quartic samples include 11 linear and 13 cubic second terms. Both groups vary leading coefficient ranks, outer ranks and answer positions; unchanged families retain prior independently tested variation.'),
'scope':check(['source-analysis.json','scope-results.json','batch.json'],'The added cubic term is supported by the canonical example and preserves the chain-rule workload. The requested easy batch retains affine inner functions.'),
'grading':check(['grader-input.json','grader-results.json','reused/grader-input.json','reused/grader-results.json'],'Native grader passed 47 acceptance and 94 rejection checks on current records, including expanded/factored blank equivalents and reordered choices. Prior unaffected counterfactual grading retained under matched bindings.'),
'rendering':check(['render-records.json','render/rendering.json','visual-inspection.json','reused/visual-inspection.json'],'Nine actual-UI renders passed. Five screenshots inspected, covering the degree-change pair, reordered choices, blank control and signed cubic boundary.'),
'packaging':check(['packaging-results.json','runtime.json','package-before.json','commands.json','changed-files.json'],'Exact dependency versions match. Current easy and quartic CLI output survives relocation unchanged; seeded replay passes. Recursive package hashes remain unchanged.'),
'decision_variation':check(['pedagogical-variation.json','counterfactual-records.json','shortcut-results.json','selection-results.json','delivery-batch/delivery.json','delivery-quartic/delivery.json','inventory-inspection.json','affected-inventory.json'],'Relevant degree changes and irrelevant choice reordering propagate correctly. No tested surface rule solves either degree subgroup or the exact radio batch. All 5 batch, 9 independent easy and 24 independent moderate records survive delivery. Selection conclusions are limited to captured inventory and documented policy/history rules.')},'findings':[]}
jsonschema.validate(read('pedagogical-variation.json'),json.loads((ROOT/'generate/pipeline/pedagogical-variation.schema.json').read_text()))
paths=[]
def visit(o):
 if isinstance(o,dict):
  for k,v in o.items():
   if k in ('sample_refs','evidence_paths'):paths.extend(v)
   else:visit(v)
 elif isinstance(o,list):
  for v in o:visit(v)
visit(result);visit(read('pedagogical-variation.json'))
for p in paths:
 assert not Path(p).is_absolute() and '..' not in Path(p).parts,p
 assert (E/p).is_file() and (E/p).stat().st_size>0,p
before=read('package-before.json');after={str(p.relative_to(W)):hashlib.sha256(p.read_bytes()).hexdigest() for p in W.rglob('*') if p.is_file()};assert before==after
save('review-result.json',result)
save('evidence-validation.json',{'schema':'generate/pipeline/pedagogical-variation.schema.json','schema_valid':True,'reference_count':len(paths),'nonempty_root_relative_references':True,'package_unchanged':True,'all_eight_checks_present':len(result['checks'])==8,'findings':0,'result':'review-result.json'})
(E/'session-state.md').write_text('Review complete: accepted. Retained canonical-degree restriction resolved and corroborated on old/current fixtures. All eight checks passed; evidence schema and root-relative references validated; package unchanged. Final report: review-result.json. No database writes or asset publication.\n')
print(json.dumps({'verdict':result['verdict'],'checks':len(result['checks']),'evidence_references':len(paths),'package_unchanged':True}))
