import json,pathlib,hashlib,importlib.util,sys
sys.dont_write_bytecode=True
R=pathlib.Path(__file__).resolve().parent;J=R.parent;W=J/'workspace';REPO=pathlib.Path('/home/jake/Developer/Course_Academy')
def load(n):return json.loads((R/n).read_text())
def save(n,v):(R/n).write_text(json.dumps(v,indent=2)+'\n')
# Update reused report logic for newly measured input counts and current inventory eligibility.
pv=load('pedagogical-variation.json')
pv['delivery']['sample_refs']=[x for x in pv['delivery']['sample_refs'] if x!='delivery-stored/delivery.json']
for x in ['inventory-eligibility.json','selection-code.json','grader-delivered-report.json','delivery-batch/accepted.json','delivery-hard/accepted.json']:
 if x not in pv['delivery']['sample_refs']:pv['delivery']['sample_refs'].append(x)
pv['delivery']['result']='Exact runner batch 5 -> 5; independent easy 12 -> 10 by deduplication; focused hard 37 -> 37. Both mixed positions remain. Four historical mixed questions are retired, excluded before fresh selection. Conditional prospective selection reaches both positions. Actual delivered records pass native grading. Captured basis 5573 only.'
for cf in pv['counterfactuals']:
 for x in ['render-rest/rendering.json','render-rest-records.json','render-inspection.json']:
  if x not in cf['sample_refs']:cf['sample_refs'].append(x)
save('pedagogical-variation.json',pv)
inspection={'passed':True,'renderer':'Unmodified actual UI through render_preview.py','cases':len(load('render/rendering.json')['cases'])+len(load('render-rest/rendering.json')['cases']),'inspected_screenshots':['render/question-002.png','render-rest/question-001.png','render-rest/question-002.png','render-rest/question-006.png'],'observations':['Easy batch blank, rational coefficients, exponent signs and worked solution are legible.','Reordering moves resonance to the second term: beta*x*e^x, explanation and product-rule steps agree.','Changing h from 1 to 2 changes complementary solution, coefficient equations and final answer consistently.','Initial-value cancellation visibly removes the complementary term.'],'limits':['No diagrams or image answer choices. Long-boundary horizontal scrolling was verified in the matching prior package review; current representative screenshots and MathJax checks independently inspected.']}
assert load('render/rendering.json')['passed'] and load('render-rest/rendering.json')['passed']
save('render-inspection.json',inspection)
# Preserve reusable independent boundary-scroll evidence with explicit provenance.
import shutil
P=J/'review-1-policy-2-48d685555902faba'
for n in ['render-scroll/rendering.json','render-scroll/question-001.png']:
 dest=R/'reused'/n;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(P/n,dest)
save('reused-render-provenance.json',{'from':str(P),'package_binding_matches':True,'files':['reused/render-scroll/rendering.json','reused/render-scroll/question-001.png'],'use':'Previously verified long-boundary scrolling retained; current renderer outputs and screenshots independently examined.'})
before=load('package-before.json');after={str(p.relative_to(W)):hashlib.sha256(p.read_bytes()).hexdigest() for p in W.rglob('*') if p.is_file()};assert before==after
save('package-integrity.json',{'unchanged':True,'files_checked':len(after),'changed':[],'database_writes':0,'assets_published':0})
runtime=load('runtime-results.json');deps=load('../workspace/package.json')['dependencies'];assert {'python':runtime['python'],'packages':runtime['packages']}==deps
assert runtime['deterministic_replay'] and all(x['rejected'] for x in runtime['guards'])
assert all(x['passed'] for x in load('math-results.json')) and all(x['passed'] for x in load('hard-math-results.json'))
save('publication-state.json',{'preparation_exists':(J/'publication/preparation.json').exists(),'method':'check_delivery.py actual prepare_records against current source/inventory; no publishing','reports':['delivery-batch/delivery.json','delivery-independent/delivery.json','delivery-hard/delivery.json']})
def check(paths,details):return {'status':'passed','evidence_paths':paths,'details':details}
a=load('source-analysis.json');sa={k:a[k] for k in ['skill','reasoning_steps','invariants','permitted_variations','source_refs']};sa['evidence_paths']=['source-analysis.json','scope-results.json','provenance.json']
result={'verdict':'accepted','summary':'All eight checks pass for the unchanged generator and exact five-question easy batch. The prior positional defect fails on the old implementation and passes current tests. All four affected historical mixed questions are retired and excluded from fresh practice.','source_analysis':sa,'checks':{
'source_replay':check(['source-replay-results.json','source-replays.json','source-analysis.json'],'All 15 practice cases reproduce available prompts, worked solutions and complete answer banks. Canonical IVP independently checked; two incomplete source captures remain documented gaps.'),
'math':check(['audit.py','math-results.json','targeted.py','hard-math-results.json'],'40 regression records satisfy displayed ODEs and initial values. All 37 focused hard records also pass independent derivative, substitution, coefficient and final-solution checks.'),
'variety':check(['coverage-results.json','hard-samples.json','retained-finding-results.json'],'Fresh 24 mixed seeds split 12/12 between resonant positions. Signed rates, coefficient signs, fractions, cancellation and original families remain represented.'),
'scope':check(['source-analysis.json','scope-results.json','construction-review.json'],'Observed easy/moderate scope preserved. Two-forcing hard extension uses earlier same-lesson methods; role exchange adds no prerequisite or workload.'),
'grading':check(['grader-delivered-input.json','grader-delivered-report.json','grader-command.json'],'Actual native grader matches 211 expectations: 71 accepted and 140 rejected, including factored equivalents, stale counterfactual keys and normalized delivered records.'),
'rendering':check(['render-inspection.json','render/rendering.json','render-rest/rendering.json','reused-render-provenance.json'],'15 actual-UI cases pass MathJax/control checks. Current screenshots inspected for easy batch, reordered resonance, transferred resonance and cancellation.'),
'packaging':check(['package-integrity.json','runtime-results.json','relocation-results.json','retained-finding-results.json'],'Package unchanged. Exact installed dependency versions, deterministic replay, invalid inputs and relocation at all difficulties pass. Old report-installation failure is superseded by this independently validated report.'),
'decision_variation':check(['pedagogical-variation.json','controlled-results.json','shortcut-results.json','delivery-batch/delivery.json','selection-results.json','inventory-eligibility.json','affected-inventory.json','evidence-contract.json'],'Controlled role transfer changes the answer; reorder preserves it through actual grading and rendering. Both mixed roles survive delivery and selection. Conditional sign/order probes do not reproduce the positional shortcut. Exact easy batch passes; prior affected stored records are retired.')},'findings':[]}
save('result.json',result);save('review-result.json',result)
import jsonschema
jsonschema.validate(pv,json.loads((REPO/'generate/pipeline/pedagogical-variation.schema.json').read_text()))
refs=[p for k in ['coverage','counterfactuals','shortcut_probes'] for row in pv[k] for p in row['sample_refs']]+pv['delivery']['sample_refs']
for p in refs:assert not pathlib.Path(p).is_absolute() and (R/p).is_file() and (R/p).stat().st_size,p
save('evidence-contract.json',{'passed':True,'schema':'pedagogical-variation.schema.json','relative_nonempty_refs':len(refs),'current_report_supersedes_old_installation_failure':True})
spec=importlib.util.spec_from_file_location('review_contract',REPO/'scripts/generator_review.py');contract=importlib.util.module_from_spec(spec);spec.loader.exec_module(contract);contract.validate_review(result,R)
(R/'session-state.md').write_text('Complete: accepted current package and exact five-item easy batch. All eight checks pass; 211 native grader expectations, 15 fresh UI renders, 15 source replays, 40 regression math records and 37 focused hard records. Fresh mixed positions 12/12; all 37 survive delivery. Four historical affected mixed records exactly reproduced and verified retired at basis 5573. No eligible affected records; affected-inventory.json empty by verification. Package unchanged. Final report result.json passes actual review contract and pedagogical schema.\n')
print(json.dumps({'verdict':result['verdict'],'package_files_unchanged':len(after),'rendered_cases':inspection['cases'],'contract':'passed'}))
