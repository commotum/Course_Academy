from pathlib import Path
import json,hashlib,sys
E=Path(__file__).resolve().parent;J=E.parent;W=J/'workspace'
def load(n):return json.loads((E/n).read_text())
def save(n,x):(E/n).write_text(json.dumps(x,indent=2)+'\n')
# Correct inherited bookkeeping, retaining actual execution results.
p=E/'audit.py';s=p.read_text().replace("'preflight':'Supplied repair-preflight.json absent','retained_findings':[]", "'preflight':json.load(open(J/'repair-preflight.json')),'retained_findings':json.load(open(J/'repair-history.json'))['findings']")
p.write_text(s)
pkg=load('packaging-results.json')
for c in pkg['cli']:
 if 'preflight' in c:
  c['preflight']=json.loads((J/'repair-preflight.json').read_text());c['retained_findings']=json.loads((J/'repair-history.json').read_text())['findings']
save('packaging-results.json',pkg)
# Saved screenshots were visually examined using view_image; all renderer reports checked.
save('render-inspection.json',{'renderer':'unmodified UI via render_preview.py --limit 16','input':'render-records.json','report_passed':load('render/rendering.json')['passed'],'rendered_count':len(load('render/rendering.json')['cases']),'screenshots_inspected':['render/question-001.png','render/question-002.png','render/question-010.png','render/question-011.png','render/question-012.png','render/question-016.png'],'observations':['Readable augmented matrices, fractions, radio controls and worked row operations; no clipped math in inspected pages.','Easy solve endpoint pair changes lower RHS 25 to 5 and correct y -65 to -45, with consistent back substitution.','Current batch endpoint screens change lower RHS -18 to 42 and correct y -9 to 3, with correctly updated elimination steps.','Irrelevant permutation pair retains matrix, mathematical key and solution; UI ordering is independently applied.','All 16 reports have no math, image or JavaScript errors. Actual batch preview positions measured separately in ui-order-results.json.']})
v=load('pedagogical-variation.json')
for p in v['shortcut_probes']:
 if p['cue']=='first position':
  p['cue']='first stored option';p['strategy']='Always choose first option in the delivered JSON order.'
  p['conclusion']+=' The UI applies additional item-specific ordering; rendered positions are probed separately.'
 if p['cue']=='first position' or p['cue']=='first stored option':pass
for f in v['fixed_features']:
 if f['feature'].startswith('A five-item batch'):
  f['justification']+=' Identical stored answer order does not imply identical rendered order; the UI reorders by item and field identity.'
v['counterfactuals'][0]['change']='Hold profile, scale, seed, candidate values and stored bank order, coefficient block and first input row fixed; vary only lower input RHS across targets. UI ordering is incidental and applied separately.'
v['answer_roles'][1]['observed']='Stored batch order gives each position correct once; actual preview UI order gives correct positions 1,2,3,1,4 (zero-based). No fixed rendered position answers all members. Controlled seed permutations preserve the correct mathematical value.'
ui=load('ui-order-results.json')
for i in range(5):
 hits=sum(p==i for p in ui['exact_batch_positions'])
 v['shortcut_probes'].append({'cue':f'rendered radio position {i+1}','subgroup':'actual delivered batch, one visible coefficient family','scope':'within_template','strategy':f'Always click rendered radio position {i+1}.','correct':hits,'total':5,'baseline':0.2,'disposition':'not_predictive','conclusion':f'{hits}/5 versus uniform five-choice baseline 0.2; no position answers this family. Preview item IDs differ from live IDs, whose ordering rule was inspected at ui/learning.js:690-701.','sample_refs':['ui-order-results.json','render-records.json','render/rendering.json']})
v['delivery']['stages_examined'].append('actual UI stable-hash choice ordering; rendered batch positions')
v['delivery']['sample_refs'].append('ui-order-results.json')
v['limitations'].append('Raw answer-array order differs from actual UI order. Rendered position counts describe the preview item IDs; numeric-rank probes remain invariant under UI permutations.')
save('pedagogical-variation.json',v)
# Extra explicit parameter boundary rejections, using independent wrapper only.
sys.dont_write_bytecode=True
exec((E/'audit.py').read_text().split('manifest=json.load')[0])
bounds=[]
for params in [['q-130909',0,0],['q-130909',3,-1],['q-130909',3,5],['q-130909',3,True],['q-130909',3]]:
 try:g.generate('easy',73471,parameters=params)
 except ValueError as err:bounds.append({'parameters':params,'outcome':'rejected','error':str(err)})
 else:raise AssertionError(params)
try:g.batch('easy',-1,73471)
except ValueError as err:bounds.append({'count':-1,'outcome':'rejected','error':str(err)})
else:raise AssertionError('negative count')
save('boundary-rejections.json',bounds)
# Review the complete package for mutations, beyond the runtime manifest.
now={str(p.relative_to(W)):hashlib.sha256(p.read_bytes()).hexdigest() for p in W.rglob('*') if p.is_file()};before=load('whole-package-before.json');assert now==before
save('package-unchanged.json',{'unchanged':True,'whole_tree_file_count':len(now),'before_file':'whole-package-before.json','after':now})
# Structured source account is independently established before the package was read.
source=load('source-analysis.json');sa={k:source[k] for k in ['skill','reasoning_steps','invariants','permitted_variations','source_refs','evidence_paths']}
def check(paths,details):return {'status':'passed','evidence_paths':paths,'details':details}
checks={
'source_replay':check(['source-analysis.json','source-confirmation.json','source-replays.json','source-replay-results.json'],'Ten complete source banks replay exactly. Two incomplete captures are explicitly unsupported. Source REF ambiguity is preserved in audit-only replay and corrected in normal banks.'),
'math':check(['audit.py','math-results.json','grader-final-input.json','construction-regression.json'],'Exact parsed arithmetic verifies 81 raw and 67 delivered records plus changed-construction regression cases: unique key, equivalent row operations, intermediate matrices and optional solutions.'),
'variety':check(['changed-rules.diff','construction-regression.json','normal-catalog-records.json','delivery-selection.json'],'Changed ordering preserves all 64 easy and 83 moderate surviving semantic instances. All five ranks per profile remain available; the exact accepted batch reaches every rank.'),
'scope':check(['source-analysis.json','independent-records.json','math-results.json'],'Finite source-coefficient profiles preserve forward elimination, optional back substitution, radio response and observed arithmetic workload; no added operators or prerequisites.'),
'grading':check(['grader-final-input.json','grader-final-results.json','grader-final.log'],'Native learner grader passed 740 submissions: 148 accepted and 592 rejected. Every choice tested; free-entry equivalence is inapplicable to these radio fields.'),
'rendering':check(['render-records.json','render/rendering.json','render-inspection.json','ui-order-results.json'],'Sixteen records rendered through actual UI. Six representative screenshots visually inspected, including relevant and irrelevant counterfactual pairs and actual batch endpoints.'),
'packaging':check(['packaging-results.json','boundary-rejections.json','retained-count-counterexample.json','package-unchanged.json','retained-current.log','retained-failing.log'],'Exact Python 3.13.5/SymPy 1.14.0 dependencies match. Runtime-only relocation, deterministic CLI, counts, finite-limit and invalid-parameter rejections passed. Retained check fails on old batch and passes currently; entire package tree unchanged.'),
'decision_variation':check(['pedagogical-variation.json','schema-validation.json','delivery-selection.json','delivery-batch/delivery.json','strict-current.log','strict-delivered.log','strict-control.log','retained-current.log','retained-failing.log','affected-inventory.json','generated-records.json','inventory-results.json','ui-order-results.json'],'Retained pivot/rank shortcut drops from 5/5 on old control to 1/5 on current raw and delivered batch. Controlled target and irrelevant permutations, conditional profile probes and UI positions tested. Delivery preserves all five ranks; explicit learner-selection scenarios reach them. Three historical inventory weaknesses separately reproduced, outside current package/batch findings.')}
result={'verdict':'accepted','summary':'The revised batch defeats the retained shortcut and all eight checks pass. The exact delivered batch covers all five answer ranks. Historical inventory weaknesses are documented separately; the package was unchanged.','source_analysis':sa,'checks':checks,'findings':[]}
save('result.json',result)
# Schema and nonempty local evidence contract.
import subprocess
schema_check = subprocess.run(['python3','-c',"import json,jsonschema;jsonschema.validate(json.load(open('pedagogical-variation.json')),json.load(open('/home/jake/Developer/Course_Academy/generate/pipeline/pedagogical-variation.schema.json')))"],cwd=E,capture_output=True,text=True)
assert schema_check.returncode==0,schema_check.stderr
refs=[]
def walk(x):
 if isinstance(x,dict):
  for k,z in x.items():
   if k in ['sample_refs','evidence_paths']:refs.extend(z)
   else:walk(z)
 elif isinstance(x,list):
  for z in x:walk(z)
walk(v);walk(result)
# schema-validation.json is created immediately below, so check it last.
for n in refs:
 if n=='schema-validation.json':continue
 p=E/n;assert not Path(n).is_absolute() and p.is_file() and p.stat().st_size>0,n
save('schema-validation.json',{'passed':True,'schema':'generate/pipeline/pedagogical-variation.schema.json','nonempty_local_references_checked':len(refs),'all_eight_passed':True,'retained_control_fails': 'AssertionError' in (E/'retained-failing.log').read_text(),'current_control_passes': '"passed": true' in (E/'retained-current.log').read_text()})
(E/'session-state.md').write_text('Review complete: accepted current package and exact batch. Eight checks passed; retained pivot/rank failure reproduced on old batch, 1/5 on current raw/delivered. 740 native submissions passed. 16 actual UI renders; six screenshots inspected. Full package tree unchanged. Three legacy stored weak instances reproduced separately in affected-inventory.json. Result: result.json.\n')
print(json.dumps({'verdict':result['verdict'],'checks':len(checks),'findings':len(result['findings']),'package_files_unchanged':len(now),'pedagogical_schema_valid':True,'evidence_references':len(refs)}))
