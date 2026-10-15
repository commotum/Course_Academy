import json,importlib.util,sys
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('triangle_generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def put(name,s):(HERE/name).write_text(s.strip()+'\n')
rows=[];recipes=[]
for mid,q in g.SOURCES.items():
 f=q[':question/answer-fields'][0];s=g.signs(f[':answer-field/correct'][':answer/value']);bank,masks=g.profile(mid,s)
 rows.append('| '+mid+' | '+str(s)+' | '+q[':question/problem'].split('path $')[1].split('$')[0]+' | '+('clockwise' if '**clockwise**' in q[':question/problem'] else 'counterclockwise')+' |')
 recipes.append({'source_id':mid,'level':'easy','template':'triangle-three-oriented-edges','profile':mid,'parameters':{'signs':list(s)},'question':q[':question/problem'],'solution':q[':question/worked-solution'],'field_key':'selection','field_type':'radio','choices':[{'field':'selection','original':a[':answer/value'],'sign_vector':list(v),'recipe':{'componentwise_multiplier_of_correct_vector':list(mask)},'exact_source_replay':g.value(v)==a[':answer/value'],'correct':a[':answer/id']==f[':answer-field/correct'][':answer/id']} for a,v,mask in zip(f[':answer-field/choices'],bank,masks)]})
(HERE/'recipes.json').write_text(json.dumps(recipes,indent=2)+'\n')
put('classification.md',f'''# Classification

Captured math basis {g.SOURCE['basis']}; lineage 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1. All ten practice questions, all fields/answers/solutions, and canonical e-6319 are retained in source.json and reference/initial/kp.edn. No registered generator or supplied .generated file existed at capture.

Easy: one Markdown/value template, one radio field named selection, five mathematical choices, ten observed whole-bank profiles, recurring central directed-triangle diagram: **heavy**. Source positions, colors and labels differ but assess the same three orientation decisions. There are no numerical evaluations, blank fields, functions to integrate, or supplied vector-field formulas. The path is closed and triangular. F is arbitrary, so the three integrals are independent formal quantities for choice comparisons.

| Source | Correct signs C1,C2,C3 | Traversal path | Winding |
|---|---|---|---|
'''+ '\n'.join(rows)+'''

Every source is easy. Source geometry and arrowheads were visually inspected in reference/source-contact-sheet.png; independent endpoint transcription appears in validate.py. The canonical example has signs (-1,-1,+1), also present in q-77143, and contributes no practice inventory.

Moderate/hard: no supported templates within this extracted backbone. This is a bounded package capability, not a claim that harder line-integral questions are mathematically impossible. All eight orientation states retain the same three-term workload; relabeling their difficulty would not establish a harder band. Introducing vector fields to evaluate, additional segments, multiple loops or coefficients changes the instructional backbone and is outside this job's evidence.

Source pattern counts: ten source records, six distinct relative sign vectors. Ignore geometric deformation, winding reversal together with reference-arrow reversal, vertex names, colors, seed, IDs, and choice bank when deduplicating mathematical tasks. Existing source duplicates remain intact.
''')
put('template-extraction.md',r'''# Template extraction

Each source instance is described separately in classification.md; recipes.json retains its full prompt, solution, field and each original option, parameter vector, exact sign-flip recipe, correctness and complete-bank profile. No choice is unmapped. Bank order is retained for source replay. Signs are coefficient vectors of the independent formal integrals I1,I2,I3; equality requires all three coefficients to agree.

Backbone: inspect a closed triangular path in a specified winding; compare each of its three edges with the arrow of C1,C2,C3; express the integral over the closed path as a sum of three component integrals. Response: one selection from five sums. Solution stages: (1) express C as the union of the three directed component paths; (2) explain opposite traversal/reversal; (3) use additivity and sign reversal to give the three-term sum. No numerical integration or conservative-field assumption.

Parameter slots: each of three relative edge orientations independently takes -1 or +1. Triangle coordinates, label assignment and winding are incidental to those roles and fixed in normal sampling for clarity. Source replay retains all original diagrams and prose. Source-specific vertex names and locations do not establish a constraint; the generator exercises all permitted arrow-orientation states at fixed nondegenerate geometry and the same winding, so arrows must genuinely change rather than merely rename curves. Clockwise source cases are normalized to counterclockwise while preserving the three reference-edge roles.

Observed domain: six mixed-sign states. Conservative same-method extension: the two uniform states, all forward or all reverse. These preserve three component integrals and the same additivity/reversal rule; the explanatory sentence explicitly handles zero or three reverse traversals. No extra reasoning stage. This extension is reported separately from observed source parameters.

Whole-bank recipe: for a source correct vector c and original option v, store the complete mask m=(v1*c1,v2*c2,v3*c3). For target s, emit (m1*s1,m2*s2,m3*s3). At s=c this exactly reproduces every original option. Select one complete source profile before rendering; never pool masks or take the first convenient options. Masks are exact algebraic transformations; psychological interpretations of compound errors remain unresolved. A bijective sign transformation preserves the five distinct options and the unique correct option for every profile and all eight parameter states. Blank/free-answer equivalence is not applicable.

Fidelity: original complete mathematical banks and correct designations replay exactly (50/50 choices, 40/40 distractors, 10/10 complete banks). Original prompts/solutions are retained verbatim as evidence. Normal generated prose follows the same stages with regularized grammar, notation, a field placeholder and parameterized target references; it is not claimed to be literal prose reproduction. Source comparisons and generated examples appear in source-replay.json and review.md.

Finite novelty bound: eight relative sign states. Bank/profile/option order, seed, question UUID, winding/label transformations or different triangle coordinates cannot enlarge this bound. At capture, six states already occur in source questions, leaving at most two potential new easy tasks. Only current actual shortages justify importing them.
''')
put('plot-extraction.md',r'''# Plot extraction and generation

The source set is shown in reference/source-contact-sheet.png. Each source has one prompt diagram and no answer or solution diagrams: a nondegenerate triangle, three named black vertices, coordinate axes without measurements, three colored edge paths C1,C2,C3 with repeated arrowheads, and no scale-dependent calculations. Source vertex placement, axis crossings and colors differ; mathematical content consists of endpoint connectivity and arrow direction. No assets are unreadable.

Source-specific directed endpoints, traversal paths and consequent signs appear in validate.py's independently transcribed EDGES table and source-replay.json. All eleven original image references are retained in source.json. Plots are central and new orientation variants need changed arrows: rating heavy. Original assets remain unchanged for source evidence.

Normal specification: A=(-2,-1), B=(3,-1), C=(0.7,3); ABCA counterclockwise (positive determinant). Edge i joins vertex i to i+1 cyclically. If sign i is +1 its reference arrows follow that traversal; otherwise they reverse. Red/brown/blue distinguish C1,C2,C3 without carrying answer information. Black vertices, readable offset labels, x/y axes and arrowheads remain visible. Geometry, color and label font are fixed to prevent cosmetic novelty. All edge directions and solution signs come from one parameter vector.

Matplotlib Agg raster renderer only; no SVG renderer. Deterministic names derive from the mathematical state, PNG bytes have SHA-256 manifests in each instance, and Matplotlib/SymPy versions are recorded. Validation enumerates all eight arrow combinations and each bank profile, checks endpoint directions independently, and includes a changed-edge case at fixed geometry. reference/generated-contact-sheet.png supports visual inspection at display size. Local plots are review artifacts; none are published unless a current easy shortage requires new content.
''')
(HERE/'capabilities.json').write_text(json.dumps({'supported_levels':['easy'],'unsupported_levels':{'moderate':{'reason':'No validated moderate template within the source three-edge orientation backbone. Every orientation state retains easy workload.','shortage':5},'hard':{'reason':'No validated hard template within the source three-edge orientation backbone. Reclassification by label alone is invalid.','shortage':5}},'finite_variants':{'easy':8,'source_distinct_patterns':6,'potential_new_patterns':2,'novelty':'relative orientation vector only'},'scope':'bounded to extracted source family; new source evidence reopens classification','unsupported_levels_filled':False},indent=2)+'\n')
put('README.md','''# Finite triangle line-integral generator

Script: ../17592186179672.py. Source/classification/extraction are local to this KP. Run `.venv/bin/python generate/scratch/17592186179672/validate.py` for complete source-bank replay, all 80 profile/state pairs and actual learner grading. Run the generator with `--difficulty easy --count 5 --seed 0 --format json`; counts above eight and unsupported bands fail explicitly. The generator never accesses the database.

Six mathematical states already exist in the unchanged source bank. Only two additional states are possible under this backbone. Replenishment must deduplicate across profiles, seeds, geometry, winding and labels, count actual gradable fresh practice, and preserve current reserves. This classification job has no easy shortage at its current basis. See reference/ for exact application inventory, speculative preview, saved request, verified receipt and readback. Moderate/hard remain shortages under the bounded package capability in capabilities.json.
''')
if __name__=='__main__':print('Classification, extraction, recipes, plots and bounded capability recorded.')
