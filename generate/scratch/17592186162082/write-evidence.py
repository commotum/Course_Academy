import hashlib,importlib.util,json,platform,shutil
from pathlib import Path
R=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('v',R/'validate.py');v=importlib.util.module_from_spec(sp);sp.loader.exec_module(v);g=v.g
shutil.copyfile(g.SOURCE,R/'source.json')
cases=json.loads((R/'source-cases.json').read_text());evidence=[]
for c in cases:
 rec=g.generate(c['level'],template=c['template'],parameters=c['parameters'],profile=c['profile']);q=g.SOURCE_Q[c['source_id']];p={k:g.s.Rational(x) for k,x in c['parameters'].items()};bank=g.bank(c['source_id'],c['template'],p,g.lengths(c['template'],p));mapping=[]
 for a in q[':question/answer-fields'][0][':answer-field/choices']:
  matches=[(x,name) for x,name in bank if v.s.simplify(v.parse(a[':answer/value'])-x)==0];assert len(matches)==1;x,name=matches[0]
  mapping.append({'source_option_id':a[':answer/id'],'source_value':a[':answer/value'],'generated_value':g.tex(x),'exact_mathematical_value':str(x),'recipe':name,'full_value_matched':True,'interpretation':'observed empirical expression pattern; error intent underidentified' if 'empirical' in name else 'inferred operation label, not observed author intent'})
 evidence.append({'source_id':c['source_id'],'source_parameters':c['parameters'],'template':c['template'],'profile':c['profile'],'level':c['level'],'level_observed':c['source_id']!='q-122484','geometry':json.loads(json.dumps(g.geometry(c['template'],p),default=str)),'prompt':q[':question/problem'],'worked_solution':q.get(':question/worked-solution'),'option_mapping':mapping,'source_plot_files':[f.name for f in R.glob(c['source_id']+'-source-*.png')],'raw_source_attribute_presence_preserved':rec['generation']['preserved_attribute_presence'],'exact_source_prompt':q[':question/problem']==rec['question'][':question/problem'],'exact_source_solution_if_present':q.get(':question/worked-solution')==rec['question'].get(':question/worked-solution'),'source_prose_normalized_full_match':bool(q.get(':question/worked-solution')) and v.normtext(q[':question/worked-solution'])==v.normtext(rec['question'].get(':question/worked-solution','')),'source_prompt_normalized_full_match':v.normtext(q[':question/problem'])==v.normtext(rec['question'][':question/problem'])})
(R/'extraction.json').write_text(json.dumps(evidence,indent=2)+'\n')
(R/'classification.md').write_text('''# Classification: KP 17592186162082

Math database basis 2275, lineage 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1. The immutable refresh source is copied in source.json. Six practice sources; canonical e9471 is context, never counted as practice.

| Level | Practice sources | Backbone families | Fields | Plots |
|---|---|---|---|---|
| Easy observed | q122481, q122843 | semicircle+diameter; three-quarter circle+horizontal segment | one radio, five math options | heavy |
| Moderate observed | q122828, q122845, q122850 | three segments; two segments; quarter circle+chord open | one radio, five math options | heavy |
| Unrated | q122484 | quarter circle+chord closed | one radio, five math options; no key/solution | heavy |
| Hard authored | no practice sources | existing quarter-open and three-segment geometry, bounded rational dimensions | same radio contract | heavy |

Each observed family has one complete empirical bank. One shared length-sum teaching chain is expressed with family-specific primitive-length rows. Different arc sweeps and part counts remain fixed per family because changing them changes the operative geometric formula or sum structure. Authored normal banks remain separate from observed profiles. The normal authored completion of q122484 is assigned moderate as a design judgment; raw-q-122484 preserves the missing level/key/solution: its quarter-circle length and diagonal chord have the same operation count and radical arithmetic as q122850.

The route reconstructed from first-step/next is Introduction → Calculating Line Integrals of Unity → piecewise-smooth tutorial → this KP → independence tutorial → independence KP. The sole key prerequisite is The Distance Formula. The canonical example sums a semicircle and two familiar diagonals. Adjacent circle/segment integration KPs are later branches; weighted integrands, general parameterization, 3D, new arc families, and extra parts are excluded.

Calculator flags are absent on all six sources in the priority13 capture: requirement remains unknown and no false boolean is inferred.
''')
(R/'template-extraction.md').write_text('''# Template extraction

## 1. Specific sources

extraction.json preserves every original prompt, every available full worked solution, exact parameter slots, geometry, five source option identities and complete value mappings. All 30 choices reproduce through the public generate API; the five observed correct designations reproduce. q122484 lacks difficulty, key and solution. Its figure supplies a radius-2 quarter arc and chord, giving π+2√2, so that option is an independently inferred key rather than an observed matched designation.

q122481 uses center (0,1), radius 2, the upper semicircle CCW and its diameter returning right. q122843 uses origin center, radius 2, a 3π/2 CCW arc then a rightward radius-length horizontal segment at y=-2. q122484 closes a quarter arc with its chord. q122828 traverses (0,0)→(0,3)→(4,0)→(4,3). q122845 traverses (-3,0)→(0,4)→(2,0). q122850 traverses (0,-4)→(4,0) along a quarter arc then a chord to (0,4).

## 2. Shared pattern

Read a planar path as two or three smooth pieces, apply additivity and the line integral of unity equals arc length, calculate each primitive length using a fixed circle fraction or the distance formula, then sum. The response is one exact scalar in a five-option radio bank. No parameterized integration is performed.

## 3. Components and banks

extraction.json accounts for each source option with exact whole mathematical value and a parameterized recipe. Script bank() defines the full recipe operations, including the compound π/radical coefficients. Observed q122484 has rπ/4+r√3/2 and rπ+3r√2/2 patterns; q122850 has 3rπ/16+r√2/4, rπ+r√2/2, rπ/16+r√2/4, and rπ/2+3r√2/4. These are retained empirical shape profiles, not claims about underlying misconceptions. Nothing is fitted around a correct total or returned as a captured literal payload.

Default authored_arc selects [arc+segment, arc, segment, 2arc+segment, arc+2segment]. Default authored_segments selects [first+rest, first, rest, 2first+rest, first+2rest]. The complete profile is selected before parameters. Whole-instance rejection catches every correct/wrong and wrong/wrong equivalence, nonpositive lengths, and absent options. No first-valid pool or mixed-bank fallback exists. Inferred operation names and empirical patterns remain author metadata.

## 4. Reusable backbone and slots

Radius r varies over integers 1..12 for easy/moderate circle families. Arc sweep, actual zero axes, center, chord role, line direction and number of parts remain fixed. Three-segment a,b pairs are (3,4),(4,3),(5,12),(12,5),(6,8),(8,6),(9,12),(12,9): familiar Pythagorean arithmetic. Two-segment a,h is (3,4),(4,3),(6,8),(8,6), b is 1..8 with noninteger second distance. Guards preserve the observed perfect-square first distance and radical second distance in normal sampling. Explicit replay may use any positive integer a,b,h ≤12 with perfect-square first distance, still preserving the family arithmetic; source banks reject collisions.

Authored hard uses only quarter_open radius k/2 or k/3, 0<r≤12, noninteger, and the same three-segment pairs divided by 2 or 3 with at least one noninteger dimension. Each adds only fixed rational coordinate/radius bookkeeping; source easy already has π and radius reading, moderate already has radicals. No instructional progression or new mathematical branch is claimed. The label is an authored difficulty policy, not recovered evidence.

Every dependent prompt radius, length row, final sum, key, option, curve, tick and C-part label is derived from one exact instance. Arc-length ds stays positive under orientation; reversing traversal and translating geometry would not create distinct assessed tasks, and neither is used to inflate capacity. Mathematical fingerprint excludes bank, profile and seed. Content identity uses version, actual prompt, actual fixed solution and complete bank; order/seed never creates a new identity.

Raw profiles raw-q-122481, raw-q-122843, raw-q-122484, raw-q-122828, raw-q-122845 and raw-q-122850 preserve exact source component strings at anchors, including original plot refs, ordered banks, correct-ref presence and rating/solution presence. Source cases select these profiles; raw q122484 has no key, rating or solution. They assemble computed expression masks and shared sentence templates, never return a whole captured payload. Changed parameters use new plots and computed chains while preserving the same omissions. Existing q- profiles are explicitly normalized completed empirical evidence, flagged evidence_only and ineligible_for_normal_generation. Default authored banks are the only normal policies.

Shared source sentences and the full five display-row sequence in normal completed reconstructions reproduce with recorded TeX spacing/factorization normalization. q122850's repeated question sentence in its solution is preserved. Original source assets are saved on white for inspection; parameter-dependent plots are always generated. No source prompt/solution strings are returned by replay branches.
''')
(R/'plot-extraction.md').write_text('''# Plot extraction and specification

All six prompt plots and five available solution plots were inspected directly, composited on white. The original assets are 360×304 PNGs. Source-contact.png supplies a review sheet; per-source files preserve native size. Blue thin curves/arrows, black x/y zero axes, sparse numeric ticks and open-path endpoint dots carry the assessed geometry. Solution assets add C1/C2, plus C3 for the three-segment family. Sources do not label every radius on x; generated figures add usable numeric axis values from the same exact instance.

q122481 axes cross at (0,0), while the semicircle center is (0,1); ticks y=1 and 3 distinguish that offset from the center. Its CCW arrows go leftward across the top and right along y=1. q122843 marks ±2 and has a large 270° CCW arc ending at the bottom, followed by the short rightward line. q122484 marks 2 on each positive axis and has a 90° CCW arc and southeastward chord. q122828 has two upward vertical legs, southeast diagonal, origin/start and upper-right endpoint dots, ticks x=4,y=3 and C1/C2/C3 solution labels. q122845 has ascending left diagonal and descending right diagonal, x=-3,2 and y=4, endpoint dots and C1/C2. q122850 has a first-quadrant-to-fourth-quadrant plot occupying right half-plane: arc begins (0,-4), goes CCW to (4,0), then chord heads northwest to (0,4), with endpoint dots and C1 on arc, C2 on chord.

The infinite black axes are contextual coordinate backgrounds, clipped at display bounds; they are never additional parts of C. There are no additional infinite source curves. Equal coordinate scale is meaningful; arrows and labels distinguish traversal and part decomposition. Axis clipping beyond the finite path is incidental.

Matplotlib recreates prompt and labeled solution assets at 432×364 (3.6×3.04 inches,120dpi), near the native aspect ratio. Visible zero axes, x/y labels, numeric units and margins adapt to exact geometry. Coordinates are numeric only at rendering; exact SymPy dimensions determine answers and text. PNG/sidecar hashes and bounds are stable for identical input. Unique per-call temporary input/output directories and atomic file replacement prevent concurrent instance mixing. Cache hits require both PNG and sidecar. Fresh concurrent tests render identical and different parameter sets in a private directory. No imagegen or direct SVG renderer is used. The renderer makes stylistic differences but preserves meaningful source geometry/cues; parent visual QA remains pending.
''')
(R/'README.md').write_text('''# KP 17592186162082 local draft

Verify with `.venv/bin/python generate/scratch/17592186162082/validate.py`.
Generate with `.venv/bin/python generate/scratch/17592186162082.py --difficulty all --seed 42 --count 2 --format json`.

Public functions: generate, generate_easy, generate_moderate, generate_hard. Explicit parameters/profile use the same pipeline as normal generation. Sources at immutable math basis 2275. All files stay within this KP's script and evidence directory; no registration, EDB writes, commits or shared edits.

Six observed empirical banks, two authored complete default banks; all three levels. Raw replay via `generate("moderate", profile="raw-q-122484")` preserves absent key, solution and rating. The moderate routing argument adds no difficulty attribute to that raw question; other raw profiles route through their observed levels. Missing q122484 fields/level in the separate normal moderate completion are inferred/authored and missing hard label is an authored rational-bookkeeping policy. See extraction.json for full original evidence and option mappings; validation.json separates value fidelity, observed/inferred designations, worked-solution normalization and native grading. review.md/review.json show side-by-side originals and variants. Worker validation is not parent approval.
''')
print([(e['source_id'],e['source_prompt_normalized_full_match'],e['source_prose_normalized_full_match']) for e in evidence])
