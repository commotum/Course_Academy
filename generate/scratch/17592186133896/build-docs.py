#!/usr/bin/env python3
import importlib.util,json,shutil
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('g',ROOT.with_suffix('.py'));g=importlib.util.module_from_spec(s);s.loader.exec_module(g)

def write(name,content): (ROOT/name).write_text(content)
sourceids={sid:template for template,(lev,sid,p) in g.TEMPLATES.items() if template!='circle_cw'}
write('classification.md',"""# Classification at math basis 1356

Snapshot database `math`, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`, topic 17592186050567 / MA 2198. All eight practice sources are included; canonical example e-9554 is curriculum evidence rather than a ninth practice question.

| Level | Sources | Field layout | Templates | Plot rating |
|---|---|---|---|---|
| easy | none observed | authored one radio, five math expressions | clockwise circle | moderate |
| moderate | q-41466 | one radio `selection` | positive ellipse | moderate |
| hard | q-42238, q-126750, q-126751, q-126748, q-126760, q-126761 | one radio per original widget; q-42238 EDB additionally retains a duplicate legacy radio | clockwise ellipse, clockwise exponential, half double-sine loop, half double-cos loop, mixed harmonics, odd-power trig curve | moderate |
| unrated | q-42221 | one radio, no correct ref, no worked solution | counterclockwise exponential | moderate |

Every captured field is radio and every displayed answer is a delimiter-free mathematical integrand fragment. This conclusion comes from inspecting all nine fields, including the legacy field, rather than assuming a common field type. Each source has its own five-option bank; q-42238 has two notation profiles of the same bank. The curves must be replotted when scales or powers change. Plots show closure, orientation, region D, and curve C; their traversal arrows are part of the assessed information.

The unrated exponential receives an **authored hard level** because its chain rule workload matches rated hard q-126750. No source difficulty is claimed for it. Raw replay preserves absent difficulty, solution and correct reference.

Curriculum route follows `activity/first-step` then `step/next`: Introduction → A Concrete Example → Negatively Oriented Curves → unit-curl identification KP17592186133895 → this setup KP → area-evaluation KP17592186133897. The explicit prerequisite is MA3705, Sums of Line Integrals With Respect to X and Y Over Parametric Curves. Easy circles use the canonical e-9554's two elementary trig derivatives, known negative orientation, fixed unit-curl P=-y,Q=0, and one scalar product. Positive scales and odd powers vary the existing operation; they add no integration technique. Every output stops at the integrand setup, before the adjacent evaluated-area KP.

Normal generation retains the source curve families and solution stage order but uses a whole authored operation bank. This resolves equal complete-integral values in observed banks. `observed_raw` is the public exact evidence replay, while `observed` is a notation-normalized, field-repaired evidence presentation. Neither evidence profile is learner eligible. Every normal default family uses `authored`.
""")
lines=["# Template extraction\n\nThe four stages below cover all practice questions and both legacy fields. Raw strings remain in source.json; generated UUIDs are new field-owned identities. Source database entity IDs and MA provenance IDs remain author metadata, not new question identities.\n"]
lines.append("## 1. Specific source descriptions\n")
for sid,k in sourceids.items():
 q=g.QUESTIONS[sid];level=g.TEMPLATES[k][0];p=g.TEMPLATES[k][2];d=g.mathematical_data(k,p)
 lines.append(f"### {sid}: {k}\n\nObserved parameters `{p}`. Curve x(t)={d['x']}, y(t)={d['y']}; t∈{d['domain']}; {'clockwise' if d['sign']<0 else 'counterclockwise'}. Given field P={'-y' if d['field']=='P' else '0'}, Q={'0' if d['field']=='P' else 'x'} has scalar curl one. Prompt contains a curve plot, parametrization, area/double-integral/integral equality with missing integrand, and supplied P/Q. " + ('No solution or correct designation or difficulty survives in the frozen record. Original lesson JSON confirms one five-choice multiple-choice widget and literal AAAAAAA missing-value placeholder.' if sid=='q-42221' else 'Full source solution verifies unit curl, states Green’s theorem, '+('explains negative orientation, ' if d['sign']<0 else '')+'substitutes the supplied vector field, differentiates both coordinates, gives the unsimplified substitution product, and then collects its scalar factors. No area evaluation appears.')+'\n\n')
 lines.append('```text\n'+q[':question/problem']+'\n```\n')
lines.append("## 2. Generalized mathematical pattern\n\nGiven a simple closed parametrized curve with its traversal and a supplied unit-curl field, form the orientation-adjusted P(x(t),y(t))x′(t)+Q(x(t),y(t))y′(t). Return the pointwise integrand fragment. Fixed fields remain P=-y,Q=0 or P=0,Q=x. Domains and coordinate shapes remain the observed closed loops. No new field-identification demand or evaluated-area demand is introduced. The three levels each have fixed workload bounds, without a sequence of harder subskills within a level.\n")
lines.append("## 3. Components and every source choice\n\nThe following formulas are parameterized expression shapes. Error interpretations are hypotheses except the correct operation; a displayed expression does not reveal the original authoring code. Every bank is retained complete. All recipes reproduce original values exactly at original parameters. `a,b` are outer scales, `m` an odd positive power. Every field's presence/absence of a correct ref remains unchanged in raw replay.\n")
mapping=[]
for sid,k in sourceids.items():
 q=g.QUESTIONS[sid];p=g.TEMPLATES[k][2];symbolic={'a':g.sp.Symbol('a',positive=True),'b':g.sp.Symbol('b',positive=True),'m':5}
 # Bank render functions support symbolic scales; odd powers use source m, documented slot separately.
 if k=='power':symbolic['m']=p['m']
 lines.append(f"### {sid}\n\n")
 for fi,f in enumerate(q[':question/answer-fields']):
  legacy=sid=='q-42238' and fi==0
  b=g.bank(k,p,legacy);sb=g.bank(k,symbolic,legacy)
  byvalue={v:(recipe,sv) for (recipe,v),(_,sv) in zip(b,sb)}
  lines.append(f"Field {fi}: `{f[':answer-field/key']}`, `{f[':answer-field/type'][':db/ident']}`, correct ref {'present' if ':answer-field/correct' in f else 'absent'}.\n\n| Captured exact value | Parameterized recipe | Operation-shape label | Correct ref |\n|---|---|---|---|\n")
  for answer in f[':answer-field/choices']:
   value=answer[':answer/value'];recipe,formula=byvalue[value];correct=f.get(':answer-field/correct',{}).get(':answer/id')==answer[':answer/id']
   lines.append(f"| `{value}` | `{formula}` | `{recipe}` | {'yes' if correct else 'no' if ':answer-field/correct' in f else 'not captured'} |\n")
   mapping.append({'source_id':sid,'field_index':fi,'source_answer_id':answer[':answer/id'],'source_value':value,'parameters':p,'recipe':recipe,'parameterized_formula':formula,'source_correct':correct if ':answer-field/correct' in f else None,'profile':'observed_raw','exact_match':True})
 lines.append('\nPrompt slots: complete coordinate tuple only. Solution slots: complete derivative tuple, complete unsimplified substitution product, complete collected integrand. All remaining prose and math stages are source-fixed. Complete component masks prevent short-token replacement from corrupting differentials or unrelated function labels.\n\n')
write('choice-mapping.json',json.dumps(mapping,indent=2,ensure_ascii=False)+'\n')
lines.append("""## 4. Reusable templates, constraints and calculations

`source_masks()` replaces complete mathematical components with named slots; `components()` emits them with source notation, including the exact source sentence/stage sequence. At original parameters, public `observed_raw` replays all eight complete prompts and all seven available solutions verbatim. The eighth solution is absent and stays absent in raw replay. Plot references stay raw when geometry is unchanged; changed-parameter raw evidence uses a rendered same-instance plot.

Shared exact calculations produce x,y,x′,y′, the unit-curl field substitution and the orientation-adjusted scalar product. Collection does not erase the unsimplified product row. For mixed harmonics, the two ordered source factor masks remain visible before the reordered factored final row. Powers retain their outer derivative coefficient m and derivative exponent m−1.

Parameter policy: easy clockwise circles a=b∈2..20 (a broader familiar integer slot; the assessed setup still uses exactly one coordinate substitution and one derivative); moderate unequal ellipse a,b∈1..12 with the scale in the first substitution factor greater than one; hard outer scales a,b∈1..6 with that same authored-bank restriction, and power m∈{3,5,7}. Explicit inputs follow the same bounds and reject complete-bank collisions without silent resampling. Raw replay permits original unit scales. These are authored bounds, not recovered source sampling code. Equal-product semiaxis pairs do not inflate mathematical task counts: fingerprint uses the demanded integrand and actual interval, omitting profile, seed, option order, coordinate aliases and intermediate scale spelling. Presentation identity includes full prompt, fixed solution, field types, complete banks and correct attribute presence.

The complete authored default bank is selected before parameters: correct product; reversed orientation; omitted first-coordinate scale; incorrectly doubled derivative; coordinate substituted in place of its derivative. This bank has exactly five expressions. The two omission/doubling recipes require a first-factor scale greater than one. Every instance is rejected whole if any pointwise expressions or complete definite integrals coincide. For exponential terms, full integrals use exact modified Bessel constants from the Fourier integral; high-precision separation is used only when SymPy does not settle equality of distinct Bessel constants. The actual grading engine receives radio IDs; its strict selections are tested separately from these mathematical criteria.

### Source anomalies, repairs and evidence limits

- q-42221: original lesson snapshot and frozen EDB both lack a correct key and worked solution; EDB also lacks difficulty. AAAAAAA is a captured missing-integrand placeholder. Derivation from x=e^(cos t), y=e^(sin t), positive orientation and Q=x gives cos(t)e^(cos t+sin t). Normal output authors that correct designation, a full standard solution with the shared source sentences, a hard level supported by q-126750, and a valid displayed integral with boxed missing fragment. None counts as a matched missing source designation or existing solution.
- q-42238: original MA lesson JSON (`/home/jake/Developer/MA/DATA/Lessons/2198/Source/2198.json`) shows one widget with five choices. Frozen EDB retains two selection fields; first has no correct designation, second is complete. Raw API preserves both; normal output uses one complete field.
- q-41466: cos² and sin² have equal full definite integrals. q-42238 likewise has repeated zero integral values among odd products. q-126750 has equal full integrals for negative sine/cosine exponential terms. Several other banks have equal zero integral values. `validation.json` reports every equal-value pair for all nine fields. Raw banks remain public evidence; no ambiguous full-integral bank is advertised as normal learner output.
- q-126748 explicitly requests the **pointwise** integrand in the frozen prompt. Its source is correct under that criterion even when whole integral values coincide. Full-integral coincidences are still recorded; normal authored bank uses unique complete values.
- q-126760 and q-126761 retain piecewise/smooth labels and actual negative traversal; no source geometry is inferred from an orientation label alone. All source arrows were inspected at original resolution.

Raw-exact fidelity is eight prompts, seven existing solutions, nine field layouts, forty-five displayed choice values and seven existing correct designations. Missing original keys stay absent. Normal presentation normalizes function notation, updates the plot reference, and explicitly requests the pointwise integrand using the q-126748 response criterion. These presentation changes are separately identified; raw evidence profiles are learner-ineligible and excluded from native delivery fixtures.
""")
write('template-extraction.md',''.join(lines))
plots=[]
for sid,k in sourceids.items():
 q=g.QUESTIONS[sid];import re
 ref=re.findall(r'!\[\]\((.*?)\)',q[':question/problem'])[0];src=Path('/media/jake/SSD/EDB/math')/ref
 dst=ROOT/ref;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst)
 with Image.open(src) as im:dims=list(im.size)
 d=g.mathematical_data(k,g.TEMPLATES[k][2]);plots.append({'source_id':sid,'reference':ref,'absolute_source':str(src),'dimensions':dims,'orientation':d['sign'],'closure':'coordinates agree at displayed interval endpoints','inspection':'view_image original resolution','role':'prompt region and traversal diagram'})
write('plot-extraction.json',json.dumps(plots,indent=2)+'\n')
write('plot-extraction.md',"""# Plot extraction and specification

1. Every original plot was visually inspected at original resolution. The exact references, dimensions, curve template and orientations are listed in plot-extraction.json. q-42221 has an orange, pale-blue filled exponential loop in the first quadrant with 1/e and e axis marks and counterclockwise arrows. q-126750 has the swapped exponential loop with clockwise arrows. q-41466 is a horizontal ellipse with counterclockwise arrows; q-42238 is a vertical ellipse with clockwise arrows. q-126751 has a right-half double-sine loop, closed at the origin, clockwise. q-126748 is an upper double-cos loop with a bottom origin cusp, clockwise. q-126760 has a mixed-harmonic curve with an upper dent, its coincident endpoints at (0,1), clockwise. q-126761 is the four-cusped odd-power trig boundary, clockwise. Canonical e-9554 circle was also inspected and is clockwise. All figures label orange C and blue interior D and show black coordinate axes.

2. The shared visual pattern is a filled simple closed loop, its coordinate axes and increasing-parameter traversal arrows. These arrows supply orientation information used by Green’s theorem. The plot is recurring and carries mathematical information: moderate plot rating.

3. Components: white background; black axes through zero with x/y labels; orange curve; pale blue region fill; blue D label; orange C label; axis tick values tied to actual coordinates; four increasing-t arrows. Each plotted sample, label position and bound comes from the same exact x(t),y(t) and t interval printed in the question. Fixed colors and typography are presentation choices. No answer/solution plot is present in the source.

4. Renderer: Matplotlib Agg, 4.8×4.2 inches, 140 dpi, equal axis aspect. Bounds include origin and actual geometry extrema, with an 18% feature-span margin. For non-origin-centered exponential loops, include both axes and the full curved first-quadrant region. Plot endpoints are numerically sampled from exactly agreeing symbolic closure endpoints. Arrow tails/tips occur at t sample indices i and i+18 (four locations), so every arrow follows actual traversal. Sidecars retain samples, arrow parameter values, coordinate endpoints, domain, orientation, bounds and Matplotlib version. PNGs and sidecars commit atomically through unique private temporary files; cache hits require both files. Parallel same/different instance calls are tested. No SVG or image model is used.

Unchanged exact raw source geometry reuses the source asset. All normal variants get a same-instance rendered asset. Source copies under images/ make raw reviews locally resolvable. Generated assets remain available for parent QA; no cache pruning occurs.
""")
write('README.md',"""# Green’s theorem area setup generator

Script: `generate/scratch/17592186133896.py`. Scope is the missing orientation-adjusted pointwise integrand for a supplied unit-curl field and one closed parametric curve. It stops before evaluating area.

```sh
.venv/bin/python generate/scratch/17592186133896/validate.py
.venv/bin/python generate/scratch/17592186133896.py --difficulty all --seed 31 --count 2 --format json
```

All three levels are supported. Easy circles and the unrated exponential’s hard label are authored curriculum-supported extensions. Default `authored` uses a whole five-operation bank with unique complete definite integral values. `observed_raw` is the parameterized exact public source replay; `observed` is a normalized evidence presentation. Both evidence profiles are learner-ineligible, retaining source limitations without changing the engine. Explicit source parameters and profiles are in source-cases.json.

source.json is the frozen basis-1356 capture. classification.md and template-extraction.md cover all sources, original widget evidence, all forty-five option recipes, and anomaly repairs. review.md/review.json include all originals and two generated examples per family, with each of easy/moderate/hard represented. validate.py checks actual displayed coordinates, derivatives, both substitution rows, closure, orientation, pointwise answers, full integral values, plot sidecars, formatting, identities, explicit constraints, concurrent assets and the actual native grader. validation.json separates exact source fidelity from normal correctness and raw ambiguity; engine.json reports native radio selection checks. No EDB writes or registration.
""")

