"""Build owned evidence from immutable capture and documented extracted recipes."""
import importlib.util,json,re,hashlib
from pathlib import Path
from PIL import Image
H=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('g',H.with_suffix('.py'));g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
for name in ('topics','lessons'):
 (H/(name[:-1]+'-context.json')).write_bytes((H.parents[1]/'runs/current/refresh-2026-10-14'/name/'17592186049212.json').read_bytes())
calc=json.loads((H.parents[1]/'runs/current/refresh-2026-10-14/priority13-calculator-requirements.json').read_text());rows=[v for k,v in calc['records'] if k==g.KP_ID]
(H/'calculator-requirements.json').write_text(json.dumps({'database':calc['database'],'basis':calc['basis'],'lineage':calc['lineage'],'records':rows,'interpretation':'No requirement attribute present in any six records. Unknown, not false.'},indent=2)+'\n')
assets=[];mapping=[]
source_pixel_fits={'q-122567':([168,259],48.33),'q-122768':([34,264],67.5),'q-122766':([112,219],56),'q-122767':([27,106],56.25),'q-122769':([101,163],67.33),'q-122770':([168,139],48.2)}
for sid,(t,p) in g.P.items():
 src=g.QUESTIONS[sid];d=g.data(t,p);v,recipes=g.bank(t,d,'original:'+sid)
 mapping.append({'source_id':sid,'template':t,'parameters':p,'profile':'original:'+sid,'field':src[':question/answer-fields'][0], 'complete_choices':[{'source_answer_id':a[':answer/id'],'source_value':a[':answer/value'],'expression':str(expr),'expression_recipe':('semicircle radius expression' if t=='semicircle' else 'rho * ('+str(expr)+'), rho = positive homothety factor of both legs'),'intent':'Geometric interpretation supported' if t=='semicircle' else 'Underidentified; homogeneous literal expression mask is evidence only','matched':True} for a,expr in zip(src[':question/answer-fields'][0][':answer-field/choices'],v)],'solution_stages':(['unity is length','radius','pi times radius','integral conclusion (authored canonical completion; raw omitted)'] if t=='semicircle' else ['unity is length','axis direction','one endpoint difference = length'] if t in ('vertical','horizontal') else ['unity is length','two right triangle legs']+(['source-specific helper triangle'] if t=='diagonal_helper' else [])+['substituted squares','individually evaluated squares','collected radicand','simplified length','integral conclusion'])})
 refs=re.findall(r'!\[.*?\]\((.*?)\)',src[':question/problem']+' '+src.get(':question/worked-solution',''))
 for i,ref in enumerate(refs):
  path=Path('/media/jake/SSD/EDB/math')/ref
  assets.append({'source_id':sid,'asset':ref,'role':'prompt' if i==0 else 'solution helper','sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'native_size':list(Image.open(path).size),'source_axes_fit':{'origin_pixels':source_pixel_fits[sid][0],'pixels_per_coordinate_unit':source_pixel_fits[sid][1],'pixel_uncertainty':2,'ticks':'Exact marked endpoint coordinate values from geometry; source does not show a full grid.'},'geometry':g.plot_recipe(t,d,i>0),'independent_worker_inspection':'Viewed six original prompt rasters together at native resolution and both helper images separately. Direction arrows inspected: upper semicircle counterclockwise; diagonal down-right/up-right/down-right; axis up/right. Helper q122769 corner (3,-1), q122770 corner (3,1); dotted legs, solid oriented hypotenuse, filled endpoints, coordinate labels.'})
(H/'choice-extraction.json').write_text(json.dumps(mapping,indent=2)+'\n');(H/'plot-extraction.json').write_text(json.dumps(assets,indent=2)+'\n')
(H/'classification.md').write_text('''# Classification at math basis 2275

Immutable lineage 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1. Six original MA practice questions, zero independent questions. Five rated easy; q-122567 is unrated and lacks correct ref and solution. All are single radio fields with key `selection`, five scalar math choices, no feedback. There are five observed prompt/solution families: semicircle, vertical, horizontal, diagonal without helper, diagonal with helper. The helper family contains two numerical variants with different complete banks. Six original complete bank profiles, four authored complete geometric banks (diagonal layouts share the method bank). Plot rating moderate for every family: geometry is recurring and supplies endpoint/length information.

Normal easy covers all five source family masks. Moderate and hard are authored diagonal arithmetic bands; the current capture supplies no rated moderate/hard evidence. They retain the same supplied graph, required scalar length, one radio, and Pythagorean chain. They do not infer difficulty from signed coordinates or simplified nonsquare radicals, both already easy in the source.
''')
(H/'template-extraction.md').write_text('''# Four extraction stages

## 1. Individual originals

q-122567: upper semicircle centered at origin, radius 3, counterclockwise. Choices 3π, 3π/2, 1, 6π, 0. Original omits difficulty, solution, key. Canonical e-9470 uses a radius-4 right semicircle, confirms length πr and the unity-is-length prose.

q-122768: (0,3) to (4,0), five answers 5, 3, 3√5, 4, 4√5. Plain triangle prose with legs 3 then 4; substituted squares → 9+16 → 25 → 5 → integral 5. No helper raster.

q-122766: (2,-1) to (2,3), choices 3,2,5,4,6. Vertical single difference 3-(-1)=4; prose says directed along y-axis, meaning parallel to it, and is retained.

q-122767: (1,-2) to (5,-2), choices 3,7/2,2,4,5/2. Horizontal difference 5-1=4; no additional stages.

q-122769: (-1,-1) to (3,1), choices 2,2√5,4,5,5√2. Helper corner (3,-1), dotted horizontal and vertical legs, solid oriented hypotenuse. Legs 2 and 4 → √(2²+4²) → √(4+16) → √20 → 2√5 → integral.

q-122770: (-3,1) to (3,-2), choices 5,3,3√5,5√3,3√2. Helper corner (3,1), dotted legs above/right, legs 3 and 6 → √(3²+6²) → √(9+36) → √45 → 3√5 → integral.

## 2. Shared pattern

Identify the integral of unity as geometric length, recover the supplied radius or endpoint coordinate differences, and use semicircle circumference / single axis difference / two-leg Pythagorean length. Retain all family-specific prose, formal equality and ordered solution operations. One concrete solution per question is independent of selected error.

## 3. Component and whole-bank mapping

`choice-extraction.json` maps every answer ID, exact source expression and field, all 30 choices, every complete profile, and solution stages. For segment banks, scalar numbers alone cannot identify all source error operations. We explicitly expose positive homogeneous masks rho times each original mathematical expression, with rho constrained by both original leg ratios. This is an evidence-only expression family, not a reconstructed misconception algorithm or arbitrary polynomial fit. It replays original complete banks and changed homothetic instances through the public API. The original q-122567 bank remains evidence only because its key is absent; 3π is independently mathematically inferred, never counted as an observed matched key. Raw omissions remain actual absent attributes.

The normal complete bank is chosen before values: semicircle [πr,2πr,πr/2,2r,πr²]; axis [difference, absolute sum of endpoint coordinates, upper magnitude, lower magnitude, squared difference]; diagonal [hypotenuse,horizontal leg,vertical leg,sum of legs,sum of squared legs]. Every option must be positive and every pair unequal, including two incorrect options. Reject the whole instance for collisions. These operations use actual displayed geometric components. No invented option feedback.

## 4. Backbone and slots

Fixed: unity with ds, single curve traversed once, source radio shape/count, family-specific geometric formula, full ordered teaching stages. Variable: positive radius; exact endpoint coordinates; eligible segment slope and translations; optional helper only as prescribed by chosen family. All labels, arrows, bounds, marked endpoints, helper corner, prose legs, squared components, radical simplification and conclusion depend on the same instance. Orientation changes preserve positive length and do not count toward variety.

Public raw profiles: radius positive <=12; segment positive rational homothety with original horizontal/vertical leg ratio; coordinates absolute <=12. Changed assets are recreated. Source refs are reused only for exact anchor geometry. Source notation is computed from expression masks, not copied payloads. All five available worked solutions match bytes at their anchors.

Normal easy: integer coordinates absolute <=12, nonzero relevant legs <=10; sampled diagonal distinct integer legs 2..10, axis endpoint pairs from lo {-4,-3,-2,1,2}, hi {5,6,7,8} with length <=10, semicircle r=1..10 subject to complete-bank validity. Easy already contains negatives, nonsquare roots and simplification.

Authored moderate: two unequal reduced half-integer legs from 3/2,5/2,...,19/2. Both squares share denominator 4; same fixed two-square chain. Authored hard: one reduced third from 4/3..23/3 and one reduced quarter from 5/4..31/4 with odd quarter numerator; denominators 9 and 16 require mixed-denominator collection. Legs bounded <=8, coordinates <=12. Every hard instance has that same arithmetic workload, with either leg orientation. This distinction is a conservative design claim, supported by the distance-formula prerequisite, rather than recovered source labels.

Meaningful tasks deduplicate translations, traversal, helper/layout aliases and bank aliases. Capacities are independently enumerated from required arithmetic roles. No count multiplies by arbitrary translations or shuffles. Radius formulas and required leg calculations remain separate roles even for equal final scalars.

Lesson route follows first-step/next: introduction → this KP → piecewise tutorial → piecewise KP → independence tutorial → independence KP. Adjacent piecewise and parametric-independence material bounds this draft: no piecewise length sums, parametric integration, weighted integrands, new calculus branches or 3D variations. Prerequisites are circumference, scalar line integrals and distance formula.
''')
(H/'plot-extraction.md').write_text('''# Plot extraction and specification

1. Originals: six native prompt rasters have white coordinate axes, black mathematical labels, thin blue C curve, multiple blue arrowheads, and filled segment endpoints. The semicircle is upper radius 3 with top scale label 3 and counterclockwise arrows from (3,0) through (0,3) to (-3,0). Segment geometry and direction, all coordinates, and the two helper corners are individually documented in `plot-extraction.json`. Canonical right semicircle radius 4 was inspected separately and is contextual evidence, not another practice template.

2. Shared visual pattern: a single clearly oriented path in equal coordinate scale, enough coordinate information to determine length. Helpers add a right triangle with dashed axis-parallel legs; they do not alter the original segment.

3. Components: origin-crossing axes; readable exact tick labels; x/y labels; C; directed solid blue path; filled segment endpoints; dashed helper legs if and only if the helper family. Axis bounds include origin and all curve extrema/endpoints with margin. Both source helper layouts have a corner at (x2,y1), including the descending case. No quarter arc or full circle is silently substituted for a semicircle.

4. Parameterized renderer: Matplotlib PNG at 540×456, equal data scale; exact values enter the math first and convert to floating coordinates only for raster construction. Every changed endpoint gets an explicit exact coordinate label so fractional ticks do not need guessing. Tick set is distinct and includes 0 and both endpoint coordinates. Semicircle radius controls endpoint and peak ticks. Arrows always point from first endpoint toward second or counterclockwise around the upper semicircle. Helper assets use precisely the same instance. Geometry/version-derived asset names, per-call temporary PNG/JSON files and atomic replacements prevent partial writes. Never prune active assets. Renderer dependency and file hashes live in sidecars. Original anchor refs remain exactly source paths.

Native inspection: worker inspected all six prompt originals and two solution helper originals, and changed rational variants. `validate.py` checks real raster blue paths, dimensions, hashes and recipe consistency; `native-review.png` provides a native montage for independent parent inspection. Mathematical/raster checks remain separate from parent approval.
''')
(H/'README.md').write_text('''# Local line-integral generator

Run `.venv/bin/python generate/scratch/17592186162081/validate.py`.
Preview `.venv/bin/python generate/scratch/17592186162081.py --difficulty all --count 2 --format json`.

Public API: generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None), plus easy/moderate/hard wrappers. Templates: semicircle, vertical, horizontal, diagonal_plain, diagonal_helper. Default profile geometric. Raw profiles original:q-122567 through original:q-122770 are public evidence-only banks with exact presence omissions. Five available source keys/solutions are preserved; q-122567 omissions are retained. No registration, commits, DB writes or shared edits. Moderate/hard are authored rational-coordinate geometric-length arithmetic bands. Native grading uses the real engine in memory. Calculator flags are unknown in all six captured supplement records. Parent independent QA is outstanding.
''')
