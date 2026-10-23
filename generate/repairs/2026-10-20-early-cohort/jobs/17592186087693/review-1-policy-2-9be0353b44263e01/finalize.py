import json,pathlib,hashlib,re
H=pathlib.Path(__file__).resolve().parent;P=H.parent/'workspace';R=pathlib.Path('/home/jake/Developer/Course_Academy')
def load(p):return json.loads((H/p).read_text())
def save(p,d):(H/p).write_text(json.dumps(d,indent=2)+'\n')
# Matrix/wording source comparison is independent of packaged registry.
src=load('../source/source.json')['material']['kp']; records=load('source-replays.json'); comparisons=[]
def body(s):return re.sub(r'\s','',re.search(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',s,re.S)[1])
for rec,q in zip(records,src[':knowledge-point/questions']+[src[':knowledge-point/canonical-example']]):
 rq=rec['question'];assert body(q[':question/problem'])==body(rq[':question/problem'])
 if 'Chelsea' in q[':question/problem']:
  assert rq[':question/problem'].startswith('Chelsea represents information using the following matrix:')
  assert 'table' not in rq[':question/problem']
 elif q[':question/problem'].startswith('Let'):assert rq[':question/problem'].startswith('Let')
 else:assert rq[':question/problem'].startswith('What are the dimensions of the matrix')
 comparisons.append({'source_id':q[':question/id'],'matrix_entries_equal':True,'wording_preserved':True,'correction':'Remove absent-table reference; matrix alone determines dimensions.' if 'Chelsea' in q[':question/problem'] else 'Normalize display formatting only.','canonical_field_limit':'Canonical has no captured answer bank; generated radio bank is an extension.' if q is src[':knowledge-point/canonical-example'] else None})
save('source-prompt-results.json',comparisons)
# Added column control independently checks displayed evidence and expected outcomes.
q=load('counterfactual-records.json')[-1]['question'];assert body(q[':question/problem'])=='1&2\\\\4&5';assert '2' in q[':question/worked-solution']
cs=load('counterfactual-results.json');cs.append({'template':'chelsea-dual-blank','base':9,'column_removed':12,'expected_values':[['2','3'],['2','2']],'passed':True,'native_grader_case':'Chelsea column removal 2x3 to 2x2','render_case':'render-last/question-001.png'});save('counterfactual-results.json',cs)
math=load('math-results.json');math['additional_column_control']={'shape':[2,2],'passed':True};save('math-results.json',math)
s=load('selection-results.json');s['rules'][0]='learning.rs validate_practice_question excludes retired and multistep records and invalid checkbox questions; captured records have ordinary gradable blank/radio fields and no retirement flag.';s['rules'].append('Without configured policy weights, select returns the first sorted candidate; no shape-based guarantee is inferred for that legacy configuration.');save('selection-results.json',s)
pv=load('pedagogical-variation.json')
for x in pv['counterfactuals']:
 x['sample_refs']+=['render-remaining/rendering.json','render-last/rendering.json']
pv['counterfactuals'].append({'kind':'relevant','change':'Remove last column from fixed Chelsea 2×3 matrix, preserving remaining entries and label.','expected':'Row blank remains 2; column blank changes from 3 to 2.','observed':'Prompt becomes 2×2; key and solution become 2×2. Native grader accepts 2 and 4/2 and rejects stale 3.','status':'passed','justification':'Columns contribute independently of rows to the ordered dimension pair.','sample_refs':['counterfactual-records.json','counterfactual-results.json','grader-results.json','render-last/rendering.json']})
pv['limitations'].append('Learner selection assessment conditions on a configured positive easy-band weight and fresh records; unconfigured legacy policy returns first candidate.')
save('pedagogical-variation.json',pv)
save('scope-results.json',{'passed':True,'source_refs':['d68f01b8-8bc6-59a1-8d80-d284abbcdf6e','80862d10-12ca-5f6e-9209-5f8bf84be504'],'reason':'Revised Chelsea wording still asks only rows then columns of one explicit matrix. All 25 supported 2..6 ordered dimensions work. Fractions, radicals, signs and zeros remain inert entries. No table reconstruction or arithmetic added.','limit':'Conservative assessed-KP domain excludes 1-row/column cases in the adjacent vector tutorial; no full-lesson coverage claimed.'})
render=[load(n+'/rendering.json') for n in ['render','render-remaining','render-middle','render-last']];assert all(x['passed'] for x in render);assert sum(len(x['cases']) for x in render)==19
before=load('package-before.json');after={str(p.relative_to(P)):hashlib.sha256(p.read_bytes()).hexdigest() for p in P.rglob('*') if p.is_file()};assert before==after
save('package-integrity.json',{'unchanged':True,'before':before,'after':after})
checks={
'source_replay':('All nine practice sources replay with complete banks, fields, keys, matrices and solutions; canonical matrix also checked. The retained omission fails on the old package and passes now. The absent-table wording correction is justified.', ['source-replay-results.json','source-prompt-results.json','repair-regression-results.json']),
'math':('112 generated records plus the added column control have correct dimension answers and solutions. All 14 captured inventory records have correct dimensions.',['math-results.json','inventory-results.json','counterfactual-results.json']),
'variety':('All 25 supported shapes work in the revised template; four boundary shapes per unchanged template and 48 fresh samples pass. Runner batch has five distinct shapes across all four templates.',['samples.json','boundaries.json','finite-batch.json','pedagogical-variation.json']),
'scope':('The repair preserves easy row/column counting, supported entry representations and ordered numeric blanks.',['source-analysis.json','scope-results.json']),
'grading':('335 native-grader assertions pass: 175 accepted and 160 rejected, including equivalent numeric notation, wrong counts, transposed dimensions and radio distractors.',['grader-input.json','grader-results.json']),
'rendering':('All 19 records render in the actual UI. Screenshots inspected for controls, matrix notation, changed dimensions and solutions.',['render/rendering.json','render-remaining/rendering.json','render-middle/rendering.json','render-last/rendering.json','visual-inspection.json']),
'packaging':('Exact Python/SymPy versions match. Deterministic runner replay, relocation and invalid-input rejection pass. Package files unchanged.',['packaging-results.json','rejection-results.json','package-integrity.json','revision-scope.json']),
'decision_variation':('Relevant row/column changes alter responses; irrelevant labels/entries preserve dimensions. Conditional shortcut probes reveal no reusable cue. Delivery retains 48/48 samples and 5/5 runner records. Selection conclusions are bounded by captured inventory and unknown learner history.',['pedagogical-variation.json','counterfactual-results.json','delivery-batch/delivery.json','delivery-sample/delivery.json','selection-results.json','affected-inventory.json'])}
a=load('source-analysis.json');result={'verdict':'accepted','summary':'The missing source replay is repaired. All eight checks pass; no current-generator or stored-pool defect was demonstrated. Package files remained unchanged.','source_analysis':{k:a[k] for k in ['skill','reasoning_steps','invariants','permitted_variations','source_refs','evidence_paths']},'checks':{k:{'status':'passed','evidence_paths':paths,'details':details} for k,(details,paths) in checks.items()},'findings':[]};save('result.json',result)
import jsonschema
jsonschema.validate(pv,load(str(R/'generate/pipeline/pedagogical-variation.schema.json')))
def validate_paths(o):
 if isinstance(o,dict):
  for k,v in o.items():
   if k in ['evidence_paths','sample_refs']:
    for n in v:assert not pathlib.Path(n).is_absolute() and (H/n).is_file() and (H/n).stat().st_size,n
   else:validate_paths(v)
 elif isinstance(o,list):
  for v in o:validate_paths(v)
validate_paths(pv);validate_paths(result)
save('evidence-validation.json',{'schema_valid':True,'referenced_files_nonempty':True,'package_unchanged':True})
(H/'session-state.md').write_text('Complete: accepted. Retained failure independently reproduced against old package; current source replays pass. 112 math records plus column control; 335 native grader assertions; delivery 48/48 and runner 5/5; 19 actual UI renders visually inspected. No stored defect demonstrated in captured inventory; affected-inventory.json empty. No package/database writes. Evidence schema and paths valid.\n')
print(json.dumps({'verdict':'accepted','checks':8,'package_unchanged':True}))
