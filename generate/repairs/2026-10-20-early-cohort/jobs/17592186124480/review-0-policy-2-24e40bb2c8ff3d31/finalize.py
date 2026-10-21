import sys,json,pathlib,hashlib,collections
sys.dont_write_bytecode=True
R=pathlib.Path(__file__).resolve().parent
J=R.parent
read=lambda p:json.load(open(R/p))
def save(n,v):(R/n).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
rs=read('moderate-samples.json')+read('hard-samples.json')+read('boundaries.json')+read('runner-batch.json')
scope=[]
for r in rs:
 g=r['generation'];profile=g['profile'];ops=g['operations'];adds=sum(op[0]=='add' for op in ops);swaps=len(ops)-adds
 scope.append({'id':r['question'][':question/id'],'profile':profile,'shape':g['shape'],'swaps':swaps,'adds':adds,'entries_bound':max(abs(x) for row in g['matrix'] for x in row),'within_profile':(adds==0 and 1<=swaps<=(1 if r['question'][':question/difficulty'].endswith('/moderate') else 2)) if profile.endswith('_swap') else ((swaps==0 and 1<=adds<=2) if profile.endswith('_eliminate') else (swaps==1 and adds==1))})
save('scope-results.json',{'source_basis':'All six moderate source questions use one swap; hard sources include one/two swaps, one/two eliminations and mixed reduction.','cases':scope,'all_within_profile':all(c['within_profile'] for c in scope),'unsupported_families':'Easy is absent in the instructional evidence and explicitly rejected. All 17 original practice cases, both radio banks and the canonical matrix are covered.','boundary_rejections':dict(collections.Counter(r['generation']['rejections'] for r in read('boundaries.json'))),'hard_rejections':dict(collections.Counter(r['generation']['rejections'] for r in read('hard-samples.json'))),'sampling_analysis':'All permitted pivot combinations can be realized by a row permutation of REF at fixed allowed shape/rank. Eligibility does not rely on labels or signs. Boundary samples include rejected numeric attempts followed by valid outputs with the originally assigned pivots retained.'})
save('visual-inspection.json',{'renderer':'Unmodified UI via generate/pipeline/render_preview.py','report':'render-all/rendering.json','passed_report':read('render-all/rendering.json')['passed'],'inspected_screenshots':['render/question-001.png','render-all/question-006.png','render-all/question-007.png','render-all/question-008.png','render-all/question-010.png','render-all/question-012.png'],'observations':['Checkbox column vectors, matrix signs, indices and worked row swaps render clearly in the exact batch.','Relevant pair changes column2 checkbox true -> false and column3 false -> true; matrix and conclusion follow. Irrelevant pair keeps 1st/2nd columns selected while showing -5.','Five radio answer labels and ordinal prose are readable; selected option agrees with solution.','Wide 4x6 matrix uses gathered solution layout; matrix and row-swap annotations remain within the content card.','No missing fonts, broken images, unresolved glyph references, MathJax errors or JavaScript errors in any of 12 rendered cases.'],'limits':['Desktop 1280x1000 viewport, full-page captures. Preview is a completed-answer fixture; actual grader outcomes tested separately.']})
current={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((J/'workspace').iterdir()) if p.is_file()}
save('package-after.json',current)
assert current==read('package-before.json')
checks={
 'source_replay':{'status':'passed','evidence_paths':['source-replay-results.json','source-replays.json','canonical-replay.json'],'details':'All 17 original prompts, complete choice banks, keyed answers, field order, and solution matrix chains replay; canonical matrix checked separately because source has no answer fields.'},
 'math':{'status':'passed','evidence_paths':['audit.py','math-results.json','counterfactual-results.json'],'details':'152 records independently checked with exact Fraction elimination from prompt text. Keys, original vectors, every displayed row operation, final REF and conclusions agree; zero failures.'},
 'variety':{'status':'passed','evidence_paths':['moderate-samples.json','hard-samples.json','boundary-results.json','stage-results.json','selection-results.json'],'details':'All ten eligible moderate subsets observed across supported shapes; 30 boundary assignments and all six hard profiles tested. Both hard elimination outcomes occur. Actual delivery retains 60/60 independent and 5/5 exact batch records; selection rules examined against captured basis 5362.'},
 'scope':{'status':'passed','evidence_paths':['source-analysis.json','scope-results.json'],'details':'Moderate preserves sparse one-swap workload; hard preserves demonstrated one/two-operation reductions and original response types. Restrictions to nontrivial subsets retain the source instructional task; unsupported easy rejected.'},
 'grading':{'status':'passed','evidence_paths':['grader-input.json','grader-results.json'],'details':'Native learning::grade_field: 115 accepted and 130 rejected checks, no unresolved cases. Tests include all source banks, exact batch, both values for each controlled-pair checkbox, and hard profiles. No free-entry fields exist.'},
 'rendering':{'status':'passed','evidence_paths':['render-all/rendering.json','visual-inspection.json','render-all/question-006.png','render-all/question-007.png','render-all/question-008.png','render-all/question-010.png','render-all/question-012.png'],'details':'12 records rendered through actual UI; screenshots inspected for exact batch, relevant/irrelevant pairs, radio bank and wide matrix. Controls, notation and worked solutions display correctly.'},
 'packaging':{'status':'passed','evidence_paths':['packaging-results.json','package-before.json','package-after.json'],'details':'Exact Python 3.13.5 matches manifest; standard-library-only packages object is empty. Fixed seed repeats identically after relocation. Invalid difficulty/count rejected. No external outputs; package hashes unchanged.'},
 'decision_variation':{'status':'passed','evidence_paths':['pedagogical-variation.json','shortcut-results.json','counterfactual-records.json','counterfactual-results.json','stage-results.json','selection-results.json','inventory-review.json','affected-inventory.json'],'details':'Relevant/irrelevant controlled pairs agree across prompts, explanations, renderer and native grading. 43 probes include conditional label/shape/template groups; none demonstrates an incidental full-answer predictor. Exact five-record batch has three subsets. Reading row-leading positions in swap-only cases is the intended source skill. Inventory assessment is limited to captured state and demonstrated weaknesses.'}
}
a=read('source-analysis.json')
report={'verdict':'accepted','summary':'No concrete failure demonstrated. All eight checks pass; the exact five-question batch survives filtering and contains three distinct pivot subsets. Package unchanged.','source_analysis':{k:a[k] for k in ['skill','reasoning_steps','invariants','permitted_variations','source_refs','evidence_paths']},'checks':checks,'findings':[]}
report['source_analysis']['source_refs']+=['tutorial feec6418-f447-5ee0-8c62-7d6b690f9228: first nonzero entries in each REF row','tutorial d45a4eba-96ce-5bef-92b7-b8f0d4cd8b72: convert a general matrix to REF before identifying pivot columns']
save('review.json',report)
# Validate prescribed variation contract and every local evidence link.
import jsonschema
jsonschema.validate(read('pedagogical-variation.json'),json.load(open('/home/jake/Developer/Course_Academy/generate/pipeline/pedagogical-variation.schema.json')))
refs=[]
def visit(v):
 if isinstance(v,dict):
  for k,x in v.items():
   if k in ('evidence_paths','sample_refs'):refs.extend(x)
   else:visit(x)
 elif isinstance(v,list):
  for x in v:visit(x)
visit(report);visit(read('pedagogical-variation.json'))
assert all((R/p).is_file() and (R/p).stat().st_size>0 and not pathlib.Path(p).is_absolute() for p in refs)
save('evidence-validation.json',{'variation_schema_valid':True,'all_evidence_refs_nonempty_relative':True,'references_checked':len(refs),'package_hashes_unchanged':True,'reports':'review.json','commands':['PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python audit.py','PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python variation.py','PYTHONDONTWRITEBYTECODE=1 python3 finalize.py']})
(R/'session-state.md').write_text('Completed independent review. Verdict accepted in review.json. 152 exact math cases; source replay 17 plus canonical; 245 native grading checks; 12 actual UI renders and visual inspection; 43 conditional/overall shortcut probes; delivery 60/60 independent and 5/5 exact runner batch. Package unchanged. No demonstrated affected inventory entries; limitations recorded. Evidence schema and paths verified.\n')
print(json.dumps({'verdict':report['verdict'],'checks':{k:v['status'] for k,v in checks.items()},'variation_schema_valid':True,'package_unchanged':True}))
