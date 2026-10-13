"""Source extraction evidence (four stages), local files only."""
import importlib.util,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('g',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
source=g.SOURCE
route=json.load(open(HERE.parents[2]/'generate/runs/current/lessons/17592186048917.json'))['record'][0]
steps={z[':db/id']:z for z in route[':activity/steps']};current=route[':activity/first-step'][':db/id'];ordered=[]
while current:
 z=steps[current];c=z[':step/content'];ordered.append(c.get(':tutorial/title',c.get(':knowledge-point/title')));current=z.get(':step/next',{}).get(':db/id')
classification=['# Classification\n\nDatabase math, basis 1356, lineage '+source['lineage']+'. Captured wrappers are preserved in source.json. Nine practice records (canonical example excluded): 3 observed easy, 5 observed moderate, 1 unrated, no observed hard. All have one selection radio field, five choices (four full function equations plus the exact text None of the listed), prompt image, and no answer/solution plots. Plot rating **heavy**: the prompt diagram is the assessment.\n\nLesson route traversed by activity/first-step and step/next: '+' → '.join(ordered)+'. Incoming topic is Vector Fields; subsequent topics include phase portraits, divergence, curl, gradients, and stream functions. Those operations are excluded.\n\nEach distinct shared-prose/stage skeleton is a separate API template, with one complete observed bank profile. A rotated template retains its source stage skeleton even when component orientations change.']
classification+=['\n| Source | Difficulty | Template | Bank | Stages |\n|---|---|---|---|---|']
stages={
'q-122296':'horizontal variation → vertical negative → F (authored completion)',
'q-122463':'horizontal negative → vertical positive → G',
'q-122629':'horizontal positive → vertical varies with x → K',
'q-122631':'horizontal zero → vertical varies with y → F',
'q-122632':'horizontal zero → vertical varies with x → H',
'q-122633':'vertical zero → horizontal varies with y → G',
'q-122634':'vertical zero → horizontal positive → K',
'q-122637':'horizontal zero → vertical negative → H',
'q-122630':'horizontal negative → vertical varies with y → H'}
for name,spec in g.PROFILES.items():classification+=['| '+name+' | '+spec[0]+(' (authored; unrated original)' if name=='q-122296' else ' (observed)')+' | '+spec[1]+' | '+name+' | '+stages[name]+' |']
classification+=['\nHard is explicitly authored: two nonconstant linear components, each ±x or ±y, with distinct independent-coordinate dependence. Unit coefficients only. Eight signed/dependency tasks. The lesson introduction x i+y j, same-topic sketching at coordinates, and q122296 distractor -x i+y j anchor the two-component content. Hard requires identifying both coordinate dependencies and their signs; it adds no differentiation, integration, radial norm, trajectory, curl/divergence, polynomial degree, or third coordinate.']
(HERE/'classification.md').write_text('\n'.join(classification)+'\n')
extraction=['# Template extraction\n\n## Stage 1 — Specific source descriptions\n\nAll prompts use one full-plane blue-arrow diagram and the identical question sentence. Source coordinate axes have arrowheads and x/y labels but no numeric ticks; identification is qualitative. Source answer math is delimiter-free, named F/G/H/K, and uses x/y input plus i/j output components. Captured notation is rendered by a whole-component formatter; source spaces and thin spaces are preserved per profile. Exact source strings and all fields remain in source.json and source-cases.json.']
for name,spec in g.PROFILES.items():
 q=g.QUESTIONS[name];extraction+=['\n### '+name+'\n\nUnderlying field at original parameters: '+str(spec[2])+'. '+stages[name]+'. Original stage sequence has two elimination bullet paragraphs, two displayed bank-equation blocks, and one inline final conclusion, except q122296 has none captured. Parameter a originally 1, sx=sy=1, swap=false. Field layout: selection, radio, five choices.']
extraction+=['\n## Stage 2 — Shared mathematical pattern\n\nMatch vector-component zero/nonzero status, sign, and variation across horizontal/vertical positions to a complete proposed formula. Use elimination and conclude with one named function. Easy has no variable components, moderate exactly one, authored hard exactly two. Distinct prose/stage patterns remain distinct templates. Choices are complete fields, not independently graded components.']
extraction+=['\n## Stage 3 — Complete component and bank mapping\n\nEach table below maps every original option to its whole-bank recipe. Every field key is selection. Recipes are symbolic expressions in common signed scale a, followed by the same signed-coordinate transformation R V(R^-1 p) as the prompt field. Scalar multiples, constant choices, mixed dependencies and signs are observed expression patterns; their cognitive error intentions are unresolved. None of the listed is retained in every profile. It is wrong because exactly one displayed full field matches. No option is dropped or replaced.']
p=dict(a=1,sx=1,sy=1,swap=False)
for name,spec in g.PROFILES.items():
 q=g.QUESTIONS[name];sf=q[':question/answer-fields'][0];source_correct=sf.get(':answer-field/correct',{}).get(':answer/value')
 extraction+=['\n### '+name+'\n\n| Exact original full value | Recipe before R | Original designation |\n|---|---|---|']
 for nm,u,v in spec[3]:
  val=g.formula(nm,g.transform((u,v),p),name)
  extraction+=['| `'+val+'` | `('+u+', '+v+')` | '+('correct' if val==source_correct else 'missing; independently derived correct' if name=='q-122296' and nm=='F' else 'incorrect' if source_correct else 'designation absent')+' |']
 extraction+=['| None of the listed | fixed text | '+('incorrect' if source_correct else 'designation absent; independently derived incorrect')+' |']
extraction+=['\n## Stage 4 — Reusable templates and constraints\n\nFixed: prompt sentence, one five-choice radio, field key selection, same source two-bullet elimination/stage sequence and fixed conclusion, source function labels. Variable: complete displayed formulas; source images reused only for original complete field geometry; all changed diagrams rendered. Conditional: component/direction nouns swap together when axes swap; positive/negative prose flips by sign(a)*sx or sign(a)*sy before swap. Formula slots are protected while prose is transformed, so function inputs/basis variables are not accidentally rewritten. All four choices are constructed from a selected complete bank; duplicate or unmatched fields reject the whole instance. No diagnosis or seed/domain metadata appears in learner text.\n\nR maps each old component to its new basis with sx/sy signs and optionally swaps axes. Old input coordinates receive the same inverse map. Common scale a is a nonzero signed integer with |a|≤3; hard requires a=1. Defaults use a=±1 and signed isometries. Explicit parameters have identical guards. The authored hard bank is the correct field, flipped horizontal sign, flipped vertical sign, and exchanged coordinate dependencies, plus None of the listed. Every hard field has two nonzero linear components and distinct x/y dependencies.\n\nFinite meaningful catalogs (common positive magnitude removed, signs/ratios/dependencies retained): easy 8, moderate 32, hard 8. No unlimited numeric-variety claim. Content identity includes actual prompt asset path, full solution, full bank, level/version; seed/order excluded. Mathematical identity excludes profiles/banks and common positive magnitude. Cross-profile i and rotated/scaled -5j dedup while content IDs remain separate.\n\n## Source anomalies and repair denominators\n\nq122296 lacks difficulty, correct designation, and solution in EDB. Captured original widget confirms exactly the same five choices and one radio assessment; widget-q122296.json preserves evidence. The plotted horizontal component is x and vertical is constant negative; only F=xi-j fits. Moderate is authored because it matches the one-variable observed workload. Complete bank reproduction counts 5/5; designation is inferred, not claimed matched. Worked solution is authored from the source common elimination/conclusion pattern.\n\nq122629 lists F=-i-j but its solution prints F=-i+xj as an eliminated option. The horizontal-negative elimination is valid for the actual F, so generator minimally replaces that whole erroneous formula with the actual bank F. Raw evidence remains unedited. Bank and designation exact; raw solution prose 7/8, repaired solution 1/8, missing/authored 1. No algebraically wrong source teaching is copied into normal output.\n\nOriginal prompt references are normalized to absolute captured local assets; exact sentence/layout and original PNG bytes match all9, but raw path strings are not claimed exact. All45 displayed choice strings reproduce exactly. Full mathematical comparison is separate from native radio-selection grading.']
(HERE/'template-extraction.md').write_text('\n'.join(extraction)+'\n')
(HERE/'plot-extraction.md').write_text('''# Plot extraction and specification

## Stage 1 — Specific source plots

Inspected all nine practice images and canonical e9441. Each is a small approximately 360×304 white/transparent diagram: black horizontal/vertical axes, positive-end arrowheads, x/y labels; repeated blue tail-anchored arrows across quadrants; no numerical ticks or grid. q122296 shows rightward/downward on x>0, leftward/downward on x<0, growing horizontal component with |x| and constant downward component. q122463 is uniform up-left. q122629 is rightward with vertical component increasing with x, downward left of y-axis and upward right of it. q122631 has vertical arrows toward x-axis, increasing length with |y|. q122632 is vertical, downward left/upward right of y-axis, increasing with |x|. q122633 is horizontal left below/right above x-axis, increasing with |y|. q122634 is uniform rightward. q122637 is uniform downward. q122630 has constant left component and vertical component matching y, with increasing vertical lengths away from x-axis. Canonical e9441 has horizontal arrows toward the y-axis growing with |x|.

## Stage 2 — Shared pattern

A qualitative full-plane vector field conveys component directions, zero components and growth/dependency. Absolute arrow-length scale is unspecified, so a uniform positive display scale does not affect identification. It must be global per field, never independently normalize each vector.

## Stage 3 — Components

White background; equal-aspect x/y coordinates; blue field arrows, black positive-axis arrowheads/labels; rectangular quadrantal lattice; full field formulas supply each arrow vector at its tail. There are no curves, integral paths, trajectories, separate samples, or answer plots. Coordinate labels are legible and not covered by field arrows. Bounds include tails and arrow tips. Prompt role only. Source copies live in source-images and retain exact image bytes.

## Stage 4 — Reusable specification

Matplotlib Agg renders every changed field. Tail coordinates are odd half-integers from -4.5 to4.5 in both axes (100 arrows), preserving the source's axis-offset lattice. Evaluate both exact components at every tail, then apply one display scale 0.85/max magnitude. Bounds [-5.7,5.7], axes from -5.6 to5.25, labels at5.4/5.45. Figure 4.2×3.7 inches at140dpi. Colors/styling fixed. No ticks/numeric scale, since the assessment is qualitative. Signs, zero status, growth ratios and coordinate dependencies come from the same instance that supplies the correct choice.

PNG naming hashes the actual full field and style. Cache hit requires both PNG and sidecar; each input/temp PNG/temp sidecar has a unique filename; atomic replacement of completed outputs prevents mixed-instance artifacts. Sidecar records exact tail/vector values, global display scale, bounds, runtime and dependency paths. Cached Python3.10 Matplotlib dependencies are read only; no installation or shared-environment changes. Concurrent tests make fresh identical-output and different-output writes inside a private temporary folder and verify exact sidecar math. No caches are pruned.

All original and generated review diagrams are inspected as rendered contact sheets. Arrows preserve intended directions/growth, axis labels remain clear, tips fit within bounds, and directions near the axes remain visible. Heavy plot rating applies to all templates.
''')
(HERE/'README.md').write_text('''# Identifying a Two-Dimensional Vector Field

Generator: ../17592186172084.py. Source: math basis1356. No EDB actions.

```sh
.venv/bin/python generate/scratch/17592186172084/build_evidence.py
.venv/bin/python generate/scratch/17592186172084/validate.py
.venv/bin/python generate/scratch/17592186172084.py --difficulty all --count 2 --seed 42 --format json
```

API: generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None), with generate_easy/moderate/hard. Required explicit parameter keys: a, sx, sy, swap. a is nonzero integer |a|≤3 (hard a=1); sx/sy=±1; swap is Boolean. Profiles are original source IDs or authored_two_variable. See classification for separate source templates.

Nine observed whole banks (45 choices) match exactly; eight available correct designations match. q122296 receives documented authored moderate/correct/solution completion. q122629's mistaken eliminated formula is minimally repaired. Source solution raw exact7/8; repaired1/8. Hard is authored from the same lesson's two-linear-component fields; no calculus/new branch. Catalogs: easy8, moderate32, hard8 meaningful qualitative tasks.

review.md has originals and two generated variants per observed bank, plus two authored hard variants. review.json is schema-shaped local review data. validate independently reads actual displayed formulas, full worked stages, prose predicates, all plotted vector samples, whole source banks, cross-profile task identity and native engine selections. hashes.json freezes actual file hashes for parent QA; dynamically generated later plot cache additions do not alter existing artifacts.
''')
