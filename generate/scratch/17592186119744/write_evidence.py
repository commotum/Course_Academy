"""Build exhaustive human-readable evidence from immutable captured data."""
import json,importlib.util,re
from pathlib import Path
H=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('g',H.with_suffix('.py'));g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g)
Q=g.QS
names={'q-77065':'Cubic/quadratic, directly completed square','q-77066':'Fractional-power/linear, affine radical integral','q-127573':'Exponential spiral, product rules and cross-term cancellation','q-127585':'Reflected cubic/quadratic, factored square and signed endpoint arithmetic','q-127602':'Linear/nested power, chain rule and completed square','q-77068':'Logarithmic/quadratic, reciprocal completed square','q-77070':'Trigonometric involute, product-rule cancellation','q-77219':'Linear/reciprocal cubic, factored reciprocal square','q-77220':'Double-angle involute, product/chain cancellation','q-77072':'Cubic/quadratic, nonnegative-t radical substitution'}
classification='''# Classification (step 3)

Database `math`, basis1356, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. The wrapper and every original field/answer/solution/asset reference are preserved in `source.json`. There are10 practice questions:5easy,5moderate,0hard; all are one scalar math radio field (`selection`) with5choices and a correct reference. No source field anomaly or blank presentation repair applies.

| Source/template | Level | Mathematical/presentation family | Profile | Plot |
|---|---|---|---|---|
'''
for sid,q in Q.items():classification+=f"| {sid} | {g.TEMPLATES[sid]['level']} | {names[sid]} | observed:{sid} | moderate |​\n".replace('\u200b','')
classification+='''
There are10 observed Markdown/value templates and10 complete observed banks. The two cubic templates share a mathematical family but have different fixed stage sequences (direct square vs external factor3 and signed endpoint distribution); they are not collapsed. Every question has one parameter-dependent prompt curve diagram; no answer or solution plot appears. Plots clarify the interval but exact symbolic length remains the assessed response.

Hard has2 explicitly authored templates and no observed difficulty labels. Exponential/trig unequal rates require two product/chain derivatives, retaining both opposite cross terms before cancellation. Affine reciprocal-cubic requires a nontrivial affine chain factor, completed reciprocal square, positive-domain reasoning and the existing power substitution. Both integrate elementary functions already present in this KP; neither introduces spatial coordinates, elliptic integrals, by-parts, inverse functions or a new integration branch. Each family has a fixed unordered workload, not a lesson progression.

Curriculum anchor: the canonical example computes a shifted circle's constant speed using the Pythagorean identity. Key prerequisite is that identity; topic incoming prerequisites include vector differentiation and parametric arc length. Activity route follows `first-step`/`next`: Introduction → Concrete Example (nonnegative-t radical/u-substitution) → integral-setup sibling → this planar KP → three-dimensional spatial sibling → deriving arc length. The spatial sibling is an explicit scope boundary. Hard extends product/chain simplification and positive perfect-square norm reductions already practiced here; hard attribution is a design claim, not recovered evidence.
'''
(H/'classification.md').write_text(classification)
extraction='''# Template extraction (step 4)

## 1. Specific originals

The exact prompts, all scalar choices, field types, correct designations, shared solution sentences, ordered derivative/norm/integration/evaluation stages and image references are retained without loss in `source.json` and reproduced in `review.md`. The inventory below describes each original before generalization. All intervals are increasing and every answer is exact; no rounding requirement exists.

'''
for sid,q in Q.items():
 x,y,a,b,speed=g.BASE[sid];extraction+=f"- **{sid}**: {names[sid]}. Curve `({x}, {y})`, interval `[{a},{b}]`, simplified speed `{speed}`. The response is an entire scalar length, not an integral setup or missing fragment. The source contains {len(re.findall(r'&\s*=',q[':question/worked-solution']))} aligned equality rows.\n"
extraction+='''
## 2. Shared instructional pattern

Differentiate both planar coordinates, form the Euclidean norm, retain the source's distributed cross terms and ordered simplifications, establish the sign needed to remove the norm square root, and integrate that positive speed over the displayed interval. A fixed worked solution applies to every chosen option. Involute families cancel product-rule terms; exponential spirals cancel opposite norm cross terms; polynomial/reciprocal pairs complete positive squares; radical curves use the source elementary substitution. These are observations, not inferred source authoring code.

## 3. Components and complete bank mapping

Each observed profile is the complete bank displayed together, with5members and4wrong values. A scalar value generally cannot identify its error operation. Consequently the only asserted extension for an observed bank is the justified homothety operation **H_c(v)=c·v**, with the same positive multiplier applied to the entire curve, every derivative vector, every norm and every explicit base-integrand/evaluation node (the symbolic displayed-curve norm integral already includesc). This operation exactly reproduces all original options atc=1 and preserves their inequalities for every admissible positivec. Distractor intent remains unresolved, explicitly; these banks are replay profiles, not claimed recovered error recipes or the default learner bank. Correctness is recomputed from the curve, never read from the correct option.

'''
for sid,q in Q.items():
 f=q[':question/answer-fields'][0];cid=f[':answer-field/correct'][':answer/id'];extraction+=f"### {sid}: `observed:{sid}`, field `selection`\n\n| Source answer ID | Exact original scalar | Designation | Parameterized recipe |\n|---|---|---|---|\n"
 for i,v in enumerate(f[':answer-field/choices']):extraction+=f"| {v[':answer/id']} | ${v[':answer/value']}$ | {'correct' if v[':answer/id']==cid else 'wrong; intent unresolved'} | H_c({v[':answer/value']}) / observed_homothety:{i} |\n"
 extraction+='\n'
extraction+='''
The separate authored default is chosen as a whole eligible operation bank before computing/rejecting members: `[L,2L,L/2,∫||r'||²dt,||r(b)−r(a)||]`, corresponding to correct arc length, double traversal, halved antiderivative, omitted norm square root, and endpoint chord. All are derived mathematical operations and positive lengths; no unrelated numerical perturbation appears. For the symmetric cubic source family the chord equalsL/2 identically, so that family selects the separately declared complete bank `[L,2L,L/2,∫||r'||²dt,c∫3t²dt]` (omitted constant speed term) before checking collisions. There is no first-valid recipe pool or repair of sampled bad members. A nonpositive, non-real or coincident member rejects the whole instance; explicit bad parameters fail rather than silently resample.

## 4. Reusable masks and constraints

Observed families use a positive integer homothetyc in1..12; original intervals are retained, including signed endpoints, e,π/2 and√3. This deliberately bounded parameter space yields60 distinct assessed lengths per observed difficulty across5families. The multiplier changes the derivative magnitude and final length, so it is a substantive assessed parameter; translations/reflections with unchanged length are not added to inflate variety. One c=1 case per source is available through the ordinary parameter/profile API. Every source-specific mathematical block is compiled into ordered, complete-component masks; the factorc applies to explicit base-function mathematical nodes rather than substituting short tokens. Generic `L=∫||g′(t)||dt` nodes remain unscaled because the displayed g already includesc; the validator independently integrates their actual printed-curve norm. Coefficientone is uniformly omitted. The original rows remain structurally present, especially q-127585's8integration/evaluation rows and q-77072's separate6-rowu-substitution block. No source-payload return branch exists.

Hard exponential: `r(t)=<c exp(kt) cos(qt),c exp(kt) sin(qt)>`, c1..12,k2..3,q1..3 withq≠k, and integer0≤a<b≤2. Nonzero unequal rates force both product and chain coefficients while preserving positive speed `c√(k²+q²)exp(kt)` and elementary exponential integration. Hard affine reciprocal: `u=kt+d`, `r=<2cu,−c/u−cu³/3>`, c1..12,k2..3,d1..2,a=0,b=1, guaranteeingu>0. Speed is `ck(u⁻²+u²)`; changing tou uses the source power-rule integration branch. Explicit input guards enforce these bounds as strictly as samplers. These are alternatives at the same intended hard level, not successive tasks.

Presentation identity hashes generator version, prompt mask, fixed worked solution, complete displayed bank, designated value, full parameters/domain and curve data. UUIDs are field-owned and stable across option shuffling/seed. Task fingerprints hash the simplified positive speed, interval and reasoning family, excluding banks/profiles, incidental translations and option order. Cubic/nested-power tasks with the same positive quadratic speed use the same reasoning tag. Parameterization is assessed through speed and interval; the plot is contextual, not a plotted-locus response.

### Source defects and supported repairs

- **q-77220 worked norm stage:** raw `16t²cos²(t)+16t²sin²` loses the double-angle argument and the second argument entirely. Independently differentiating the printed curve gives`<4tcos(2t),4tsin(2t)>`; the minimal repair is`16t²cos²(2t)+16t²sin²(2t)`. Raw evidence remains unchanged. Raw complete solution fidelity is9/10; repaired complete solution fidelity is10/10, preserving all rows and prose.
- **q-77220 source plot:** raw labels putt=1 left of the y-axis andt=2 right. Actual printed coordinates aret=1≈(1.402448,1.741591),t=2≈(−3.680854,1.857772). The source graphic depicts reflected/reversed involute geometry inconsistent with the formula. Generated diagrams use the actual printed curve and those exact endpoints. This is a plot-content repair, not a bank/value exclusion. Raw plot montage and path remain evidence.
- Source notation uses Unicode function application and some shorthand`{cos}`/`{sin}` powers. Source replay retains these except the explicit defective argument repair; the independent parser normalizes them internally. Row whitespace is normalized for comparisons. Source prompt syntax/spacing is preserved with only the recreated asset path changing. No mathematical source is excluded.
'''
(H/'template-extraction.md').write_text(extraction)
plot='''# Plot extraction/specification (steps 5 and 7)

## 1. Specific plots

All10 original PNGs were composited on white and inspected in `source-plots.png`; original references are retained in source records. q-77065 shows a cubic bend, q-77066 a fractional-power arc from the origin, q-127573 an exponential spiral, q-127585 a symmetric cubic bend with crossing continuations, q-127602 a nested-power bowl, q-77068 a positive-t log/quadratic bend, q-77070 an involute loop, q-77219 a positive-t rational/cubic arc below the x-axis, q-77220 an involute loop with incorrect source geometry/endpoints, and q-77072 a translated cusp-shaped cubic/quadratic arc. Source diagrams have black arrowheaded axes, axis labelsx,y, a red contextual continuation, a blue assessed interval, blue endpoint dots and blue exact parameter labels. They have no tick scales, grids, guides, curve-direction arrows or response plots.

## 2. Shared visual pattern

One planar coordinate diagram accompanies each arc-length calculation, distinguishing the requested interval from the surrounding curve. Endpoint order corresponds to the displayed parameter interval. Numeric coordinates are determined by the curve, not diagram guesswork. Plot rating ismoderate: every variant needs a changed curve/endpoint image, though it does not supply an otherwise missing mathematical value.

## 3. Components

White background; blackx/y axes with arrowheads; equal unit scales by default; independent axis scales for readable reciprocal-cubic diagrams, as recorded in sidecars; red continuation; thick blue assessed curve; blue endpoint dots and exacttlabels. Context ranges respect real-domain constraints (t≥0 for fractional powers,t>0 for log/reciprocal functions). Polynomial continuations include both signs where the source does; involutes include the surrounding loop. Hard families reuse the same layout. Coordinates are computed from the exact question in the primary SymPy runtime; the renderer accepts those coordinate arrays and does not resample anything.

## 4. Reusable renderer and verification

`render_plots` writes a unique temporary JSON input and calls `render.py`, which uses Matplotlib only. The primaryPython3.13environment lacks Matplotlib, so the already-cachedPython3.10/Matplotlib wheels are loaded read-only; no install/network operation occurs. Each asset's JSON sidecar records Python, Matplotlib, resolved dependency paths, exact curve/domain, sampled coordinates, styles and computed bounds. Bounds include curve features and axes with margins. Axis arrows, labels and endpoint offsets are retained; there are no invented traversal arrows. Output names derive from stable content identity. Renderer PNG and sidecar writes use unique temporaries plus atomic replacement. Concurrent identical/different parameter tests pass and leave no temporary inputs.

Generated plots are inspected in `generated-plots.png`. The scalar prompt/answer/worked-solution validation independently reparses printed coordinates and checks endpoint positions against each sidecar. The source's q-77220 geometric inconsistency is repaired by plotting its actual printed curve. Source plots are not reused for changed parameters. No image model, direct SVG generation or shared environment change occurs.
'''
(H/'plot-extraction.md').write_text(plot)
(H/'README.md').write_text('''# Planar arc length scratch generator

Run `.venv/bin/python generate/scratch/17592186119744/validate.py` to replay10source questions, check actual printed mathematics and all complete banks, exercise authored hard alternatives, test stable identities/concurrent plots, and run the real native radio grader. Preview with `.venv/bin/python generate/scratch/17592186119744.py --difficulty all --seed 4 --count 2 --format markdown` (orjson). Explicit source example: `--difficulty easy --template q-77065 --profile observed:q-77065` through the PythonAPI withparameters`{"c":1}`; CLI samples c normally.

`source.json` preserves database/basis/lineage. Observedscalar-bank homotheties are explicit replay profiles with unresolved original distractor intent; normal banks are authored complete mathematical operations. Hard is2authored planar families grounded in existing prerequisites/methods. q-77220 has an explicitly repaired norm row and an inconsistent source plot; raw evidence remains intact. No sources are omitted. Full numerical/bank fidelity, raw and repaired prose/stage fidelity, native grading and plot verification are reported separately in `validation.json`.

The renderer uses already-cached read-onlyPython3.10/Matplotlib dependencies. Assets and every other write remain inside this evidence folder. No database writes, registration, engine modification or commits; work stops afterstep7.
''')
records=json.loads((H/'review.json').read_text())
review='# Original and generated review\n\nOriginal records retain full source prose, every field/choice and their PNG asset references. Generated records are labeled by origin/profile; their plots are recreated from actual parameters. Correct designations are author review data, not learner feedback.\n\n'
for sid,q in Q.items():
 review+=f"## Original {sid}\n\n"+q[':question/problem']+'\n\n'
 f=q[':question/answer-fields'][0];review+='Field: `selection`, scalar math radio,5choices.\n\n'
 for v in f[':answer-field/choices']:review+='- $'+v[':answer/value']+'$'+(' (correct)' if v[':answer/id']==f[':answer-field/correct'][':answer/id'] else '')+'\n'
 review+='\n'+q[':question/worked-solution']+'\n\n'
 for r in [r for r in records if r['generation']['template']==sid]:
  m=r['generation'];qq=r['question'];review+=f"### Generated {m['origin']} template / {m['bank_profile']} / c={m['parameters']['c']}\n\n"+qq[':question/problem']+'\n\n';ff=qq[':question/answer-fields'][0]
  for v in ff[':answer-field/choices']:review+='- $'+v[':answer/value']+'$'+(' (correct)' if v[':answer/id']==ff[':answer-field/correct'][1] else '')+'\n'
  review+='\n'+qq[':question/worked-solution']+'\n\n'
for r in [r for r in records if r['generation']['origin']=='authored']:
 m=r['generation'];q=r['question'];review+=f"## Generated authored hard / {m['template']} / {json.dumps(m['parameters'])}\n\n"+q[':question/problem']+'\n\n';f=q[':question/answer-fields'][0]
 for v in f[':answer-field/choices']:review+='- $'+v[':answer/value']+'$'+(' (correct)' if v[':answer/id']==f[':answer-field/correct'][1] else '')+'\n'
 review+='\n'+q[':question/worked-solution']+'\n\n'
(H/'review.md').write_text(review)
print('Wrote classification, four-stage extraction, plot specification, README and exhaustive original/generated review.')
