"""Produce only this KP's source classification/extraction/plot evidence."""
import hashlib,importlib.util,json,re,itertools,math
from pathlib import Path
from PIL import Image
HERE=Path(__file__).resolve().parent;spec=importlib.util.spec_from_file_location('g',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def dump(n,v):(HERE/n).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
measured={'q-43310':[(18,31),(166,18),(333,175)],'q-43343':[(110,208),(28,39),(233,23)],'q-161107':[(256,195),(16,131),(205,4)],'q-161109':[(18,197),(169,16),(288,171)],'q-280279':[(139,251),(6,9),(278,251)],'q-280282':[(18,19),(103,12),(132,194)],'q-365424':[(18,171),(186,6),(300,97)],'q-43328':[(18,18),(164,45),(161,220)],'q-43339':[(18,17),(138,49),(232,230)]}
plots=[];bankmap=[]
for sid,q in g.SOURCES.items():
 asset=re.search(r'!\[\]\(([^)]+)\)',q[':question/problem'])[1];path=Path('/media/jake/SSD/EDB/math')/asset;im=Image.open(path);kind,b,c,t,u=g.ANCHORS[sid];A,B,C=measured[sid];uvec=(B[0]-A[0],B[1]-A[1]);vvec=(C[0]-A[0],C[1]-A[1]);angle=math.degrees(math.acos(sum(x*y for x,y in zip(uvec,vvec))/(math.hypot(*uvec)*math.hypot(*vvec))))
 plots.append({'source_id':sid,'asset':asset,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'size':im.size,'pixel_vertices_estimated':dict(zip('ABC',measured[sid])),'measurement_uncertainty_pixels':3,'apparent_angle_degrees':angle,'diagram_to_scale':False,'labels':{'AB':c,'AC':b if kind=='angle' else None,'angle':t if kind=='side' else None,'unit':u},'markers':'filled wedge at A; blue sides / green or orange angles; no axes/arrows','role':'prompt'})
 f=q[':question/answer-fields'][0]
 for a in f[':answer-field/choices']:
  bankmap.append({'source_id':sid,'field':f[':answer-field/key'],'type':f[':answer-field/type'][':db/ident'],'profile':'raw_'+sid,'answer_id':a[':answer/id'],'original_value':a[':answer/value'],'correct_designation':a[':answer/id']==f[':answer-field/correct'][':answer/id'] if ':answer-field/correct' in f else None,'recipe':'exact complete original scalar × common side dilation s; no inferred error intent' if kind=='side' else 'fixed exact angle under uniform geometric dilation; historical wrong-angle intent unresolved','eligible_for_learning':False,'origin':'observed-opaque-radio' if len(f[':answer-field/choices'])>1 else 'observed-exact-blank'})
dump('source-geometry.json',plots);dump('bank-map.json',bankmap)
(HERE/'classification.md').write_text('''# Classification — KP17592186105904

**Calculating an Angle or Side of a Triangle Given the Area of a Triangle** belongs to topic17592186050149, *The Area of a General Triangle* (MA1275). Frozen `math` basis1356, lineage01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1. The source wrapper is preserved in source.json.

There are **9 practice sources**, plus the canonical example. Seven practice questions are labeled moderate, two are unrated. There are six five-option radio fields and three scalar blank fields. Two unrated radio records lack correct refs and worked solutions; raw public replay preserves all three omissions. They receive an explicitly authored moderate assignment for completed normal variants.

The broad operations are side isolation and acute included-angle identification, both using A=½bc sin A. Exact masks distinguish nine source layouts/stage recipes: q-43310 and q-43343 have no original solution; q-161107 cancels a whole radical coefficient; q-161109 cancels radical and denominator; q-280279 factors out sine; q-280282 includes an additional reduced-sine row; q-365424 omits that redundant row; q-43328 factors and cancels b/2 then rationalizes; q-43339 collects integer products. These are preserved independently of generic operator equality.

| Sources | Observed level | Field | Operation | Plot rating |
|---|---|---|---|---|
|q-43310|unrated|radio|side|moderate|
|q-43343|unrated|radio|angle|moderate|
|q-161107, q-161109|moderate|radio|side, distinct cancellation masks|moderate|
|q-280279|moderate|blank|side|moderate|
|q-280282, q-365424|moderate|blank|acute angle, distinct reduction masks|moderate|
|q-43328, q-43339|moderate|radio|acute angle, distinct factor masks|moderate|

All nine prompt diagrams carry side/angle givens; changed numerical instances require new diagrams. Full source rasters were inspected at original resolution, white-composited in source-montage.png; no choice plots exist. `source-geometry.json` records labels, pixel measurements, dimensions and hashes.

Six distinct complete observed radio banks remain explicit raw profiles. Their wrong numerical values do not uniquely identify an operation. They are evidence only and never sampled as normal defaults. Three observed blank profiles preserve exact answer fragments. `bank-map.json` maps every one of 33 displayed values and all 7 available correct designations.

Normal moderate serves all nine source families with method-derived whole banks or observed-shaped blanks. Easy and hard each add authored radio/blank side templates. No level adds cross products, quadrilateral area, cosine law, inverse-calculator trigonometry or a sequence of increasing demands.
''')
(HERE/'template-extraction.md').write_text('''# Four extraction stages

## 1. Specific source descriptions

The exhaustive source components are in source.json, source-cases.json, bank-map.json and source-geometry.json. q-43310 uses AB=3, angle30°, area21/4 cm², unknown AC=7. q-43343 uses AB=5, AC=6, area15√3/2 cm², acute angle60°. Both omit rated difficulty, correct designation and worked solution. The owning original MA1275 Markdown confirms these omissions and complete five-option banks.

q-161107: AB=5,60°, area5√3, unknown AC=4; five scalar cm options, whole-radical cancellation. q-161109: AB=6,45°, area21√2/2, AC=7; five cm options, separate radical/denominator cancellation then 3b=21. q-280279: AB=10,120°, area25√3/2, AC=5; field-1 scalar blank, known sine factored before cancellation. q-280282: AB=√3,AC=4, area3 mm²,60°; scalar degree fragment, rationalization with duplicated direction of sine equality. q-365424: AB=8,AC=10, area20√2,45°; scalar degree fragment, no redundant reduced fraction row. q-43328: AB=√2,AC=√6, area√6/2,45°; radio angles, common b/2 cancellation then 1/√2 rationalization. q-43339: AB=5,AC=12, area15,30°; radio angles, product30 then fraction15/30.

Decoded strings contain adjacent ord92 values only for aligned row breaks (maximum run2). Commands have a single decoded slash. No TeX escape repair is claimed from serialized output.

## 2. Generalized shared pattern

Read the two sides adjoining marked A. Use A=½bc sin A. If b is unknown, evaluate the supplied special angle, form the side coefficient and isolate b. If A is unknown, divide twice the area by bc and recognize the acute special angle. The angle branch is limited to30°,45°,60°. Source geometry is schematic; only the included angle A is described as acute in normal prose, rather than making a global triangle claim. Side families also include obtuse120°.

## 3. Components and complete banks

source_chain implements each observed ordered arithmetic mask independently. Formal operator, Here component definitions, sine evaluation (side families), substitution, individual coefficient multiplication, cancellation/reduction, final unit and conclusion remain separate stages. Blocks replace complete mathematical components inside unchanged source prose; no short numeric replacement crosses variable labels or prose. At original parameters all seven present solutions are byte exact.

bank-map.json lists all 33 original values, field ownership, original correct state and raw replay recipe. Raw side profiles apply common geometric dilation s to all side options and s² to area; raw angle profiles keep exact angles fixed while sides/area dilate. This is an evidence parameterization, **not a recovery of historical wrong operations**. Permitted s is½,1,2,3. Raw profiles retain missing metadata and are always ineligible for learning. Missing correct values (7 cm and60°) are independently derived only in completed normal variants, and never counted as matched observed designations.

The authored default side bank is chosen whole before sampling: [b, b/2, bc², c, b/c]. Its four wrong operations are omitting½; multiplying by known c instead of dividing; isolating the already supplied side instead of requested b; dividing by c twice. All are derived directly from ½bc sin A. The special-angle recognition bank is [30°,45°,60°,120°,135°], representing familiar-angle lookup and supplementary-branch errors. The requested acute branch makes only one option eligible. Entire instances are rejected on duplicate/invalid values. Blanks have no distractors.

## 4. Reusable masks and bounds

Public API is generate(level,seed,template,field_type,parameters,profile), with three level entrypoints. Parameters are exactly {b,c,theta,unit}. Explicit invalid parameters are rejected. Completed questions use owned UUID answers and lookup refs; source IDs/provenance and recipe eligibility stay outside learner content. Identity derives from actual prompt, solution, sorted whole bank, level and shape. Seed/option order do not change identity. Mathematical task fingerprints omit unit-letter changes and bank profiles.

Easy authored supplies sin30°=½ in the prompt; positive integral side values2..12 leave one linear isolation. Moderate integer families use sides2..12 and their observed special angle, preserving their exact operation sequence. Radical families independently vary half/integer side multipliers through8 subject to both lengths≤12: q-280282 has28 meaningful side combinations, q-43328 has45. Hard authored keeps the same side-isolation method but both side lengths are reduced nonintegral rationals in[1,12], denominators2,3,4; familiar45°,60°,120°,135° preserve exact trig evaluation. Both the given side and recovered answer are genuinely nonintegral, so no explicit parameter choice can collapse hard to moderate. No branch or progression occurs within any level.

variety.json enumerates actual eligible arithmetic tasks per family, ignoring unit aliases, seed and bank aliases: easy radio108/blank121; moderate families28–121 each; hard radio11792/blank12100. Layout variants are not new mathematics and are not summed as distinct task counts. Scope follows linked lesson order17592186106917 introduction→06918 area KP→06919 this inverse KP→06920 quadrilateral→06921 difference areas→06922 derivation, and the Special Trigonometric Ratios prerequisite. Authored hard expands number forms, not the lesson method. Cross-product topic1299 is the succeeding topic and is excluded.

Normal angle prose specifies the acute included angle only; original public raw prompts remain unchanged. A source prose error occurs in q-280282: “acute triangle” is false as a whole-triangle classification, since cos B has numerator √3−4cos60°=√3−2<0. The intended included angle is acute. Raw evidence is exact; normal prompts specify only acute ∠A, a minimal supported branch clarification. The two omitted designations remain unknown source attributes despite independently identifiable answers.
''')
(HERE/'plot-extraction.md').write_text('''# Four plot extraction stages

1. **Specific diagrams.** source-geometry.json records each original raster, hash, original dimensions and estimated A/B/C pixels (±3px). All are black closed triangles on transparent/white backgrounds, italic vertex labels, side givens outside edges, and a colored filled wedge at A. Side problems use blue wedges with degree labels; angle problems use orange or green unlabeled wedges. No grid, axes, vectors, arrows or solution plots. The q-43310 layout is very flat, q-280279 obtuse, q-280282 and q-43328 narrow. These source rasters are schematic: apparent pixel angles differ from stated angles and lengths cannot be recovered from scale.
2. **Shared visual purpose.** Identify the included angle and adjacent supplied sides. Preserve the ownership of AB=c, AC=b and the unknown object's absence of a numeric label. The orientation/rotation is incidental; labeled adjacency and acute/obtuse class are meaningful.
3. **Components.** The recorded source vertices, side labels and wedge are matched to every source individually. Source references/hashes are retained at exact anchor replay. Generated rasters use A=(0,0), C=(b,0), B=(c cos theta,c sin theta), no axes, black edges and blue/green wedges. Thus true Euclidean geometry and area are derived from the exact same parameters. Labels are attached to their edge/vertex and placed outside edges. Unknown b gets no side label; unknown angle gets no degree label.
4. **Reusable specification.** Matplotlib Figure, equal aspect, white background,4.7×3.5in,150DPI. Wedge radius is0.2 min(b,c); vertices have point-offset labels and the short AC label sits34points below its edge to avoid thin-triangle overlap. Bounds include all vertices and label margins. PNGs and JSON sidecars are atomically written under private plots/ or concurrency/ using unique temporary filenames and a renderer lock; cache hits require both. Content-addressed names include exact geometry, response kind, units and renderer version. Sidecars record actual Python/Matplotlib versions, dimensions/DPI, vertices, labels and PNG SHA256. No SVG, model, external image generation or shared cache writes. All produced assets are retained for concurrent parent review.

Original full-resolution inspection: source-montage.png. Generated inspection: generated-montage.png. Validation independently computes both side lengths, included angle and determinant area from rendered sidecar vertices and matches these to printed area and labels, with strict numerical tolerance. It also samples every edge at three positions using the actual axes-to-raster transform and requires a black stroke within3pixels of each sample. Fresh concurrent calls exercise identical and different parameters. Reuse is restricted to unchanged anchor geometry, not a parameterized instance with changed labels.
''')
(HERE/'README.md').write_text('''# Inverse triangle-area generator

Run `.venv/bin/python generate/scratch/17592186105904/validate.py` for displayed mathematics, whole banks, all source keys/stages, sampler family coverage, identity, mutation, concurrency and real native grader checks.

Preview `.venv/bin/python generate/scratch/17592186105904.py --difficulty all --seed 42 --count 2 --format json`. API/CLI never write EDB or edit the engine. Source snapshot basis1356 is preserved.

Nine raw public profiles reproduce33 displayed values,9 exact prompts,7 exact present solutions and7 observed designations;2 missing difficulties/solutions/designations remain absent. Raw opaque banks are ineligible for learning. Completed defaults serve all observed source-shaped families with independently derived banks/blank answers. Easy supplies the sine; hard adds bounded reduced rational side arithmetic, explicitly authored same-method extensions. review.md/review.json contain originals and at least two variants at every level and family.

Review limitations: historical scalar distractor intent remains unresolved (retained evidence only), original diagrams are schematic, and two original correct refs are absent. The q-280282 whole-triangle acute claim is false (angle B is obtuse); normal output repairs it to acute included ∠A. No original source label or recovery claim is fabricated. Native results and build hash are in validation.json/engine.json. Changes stop at step7.
''')
print('evidence written')
