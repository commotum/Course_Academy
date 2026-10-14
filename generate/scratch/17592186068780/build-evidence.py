import importlib.util,json,re,hashlib
from pathlib import Path
import numpy as np
from PIL import Image
HERE=Path(__file__).parent;s=importlib.util.spec_from_file_location('g',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
cal={'e-5926':(169,163,24,24),'q-39046':(169,163,29.25,29.25),'q-39047':(169,163,24,24),'q-113479':(169,203,26.5,26.5),'q-113476':(169,187,24,24),'q-113478':(169,114,32.5,32.5),'q-113482':(99,163,35,35),'q-270750':(169,163,24,24),'q-320718':(201,195,16,16)}
plots={}
qs={'e-5926':g.REC[':knowledge-point/canonical-example'],**g.QS}
for sid,q in qs.items():
 p=g.norm(g.ANCHORS[sid] if sid in g.ANCHORS else dict(a=3,b=2,k=-1,px=3,py=2));asset=re.search(r'!\[\]\((.*?)\)',q[':question/problem']).group(1);path=Path('/media/jake/SSD/EDB/math')/asset
 rgba=Image.open(path).convert('RGBA');white=Image.new('RGBA',rgba.size,'white');white.alpha_composite(rgba);im=white.convert('RGB');rgb=np.array(im);blue=(rgb[:,:,2]>110)&(rgb[:,:,0]<90)&(rgb[:,:,1]>55)&(rgb[:,:,1]<160);vv,uu=np.where(blue)
 u0,v0,sx,sy=cal[sid];a,b,k,x,y=(float(p[t]) for t in ('a','b','k','px','py'));X=(uu-u0)/sx-b;Y=(v0-vv)/sy-k
 # Distance in native pixels to the implicit reciprocal locus: denominator is
 # gradient with respect to raster coordinates, permits near-vertical branches.
 dist=np.abs(X*Y-a)/np.sqrt((Y/sx)**2+(X/sy)**2)
 # Stroke radius and calibration uncertainty capped at two native pixels.
 away=(np.abs(uu-(u0+x*sx))>6)|(np.abs(vv-(v0-y*sy))>6)
 assert float(np.quantile(dist[away],.99))<2.2,(sid,np.quantile(dist[away],.99))
 pu,pv=u0+x*sx,v0-y*sy;u,v=round(pu),round(pv);assert blue[max(0,v-3):v+4,max(0,u-3):u+4].sum()>=8,(sid,'marker')
 plots[sid]={'asset':asset,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'native_dimensions':list(im.size),'parameters':{t:str(v) for t,v in p.items()},'calibration':{'origin':[u0,v0],'pixels_per_x_unit':sx,'pixels_per_y_unit':sy,'positive_x':'right','positive_y':'up'},'marked_point_pixel':[pu,pv],'vertical_asymptote_pixel':u0+b*sx,'horizontal_asymptote_pixel':v0-k*sy,'axes':{'horizontal':v0,'vertical':u0,'arrowheads':['positive x','positive y']},'tick_labels':{'vertical_asymptote':g.fmt(p['b']) if b else 'coincides with y-axis, no extra tick','horizontal_asymptote':g.fmt(p['k']) if k else 'coincides with x-axis, no extra tick'},'branch_sign':int(sp_sign:=1 if a>0 else -1),'branch_locations':'upper-right/lower-left of asymptote intersection' if a>0 else 'upper-left/lower-right of asymptote intersection','geometry_check':{'blue_pixels':int(blue.sum()),'implicit_distance_99_percentile_pixels':float(np.quantile(dist[away],.99)),'allowed_pixels':2.2,'marked_point_blue_pixel_count':int(blue[max(0,v-3):v+4,max(0,u-3):u+4].sum())},'native_visual_inspection':'Entire 360×304 source inspected: curve, both branches, marked point label, signed asymptote labels, axes and arrowheads; no grid or numeric zero label.'}
(HERE/'plot-extraction.json').write_text(json.dumps({'basis':1356,'plots':plots,'source_graphs_inspected':9,'renderer':'Matplotlib only'},indent=2))
(HERE/'classification.md').write_text('''# Classification — KP 17592186068780

Frozen math basis 1356, lineage 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1. Eight practice sources plus one canonical example. All plots are heavy: graph labels and asymptotes supply the unknown numerical information.

| Observed level | Template | Field contract | Sources | Banks |
|---|---|---|---|---|
| Unrated | unshifted a/x, find a | radio, five scalars; correct absent | q-39046 | 1 |
| Moderate | a/x+k, find a+k | radio, five scalars | q-39047, q-113476, q-113478 | 3 |
| Moderate | a/x+k, enter a,k | two scalar blanks | q-270750 | singleton fields |
| Hard | a/(x-b)+k, find a+b+k | radio, five scalars or absent fields | q-113482, q-113479 | 1 radio, 1 fieldless |
| Hard | a/(x-b)+k, enter a,b,k | three scalar blanks | q-320718 | singleton fields |

No observed easy label exists. Easy is an authored assignment for unshifted graph coefficient recovery: a single integer coordinate product. Moderate reads one nonzero shift and isolates a; hard additionally reads b and computes the signed difference x-b. Original ratings and omissions are preserved by raw profiles.

Lesson route follows first-step/next: Introduction → Applying a Stretch With a Scale Factor Less Than One → Graphing a Stretched Reciprocal Function → Applying a Stretch to a Negative Reciprocal Curve → Graphing a Stretched Negative Reciprocal Function → Graphing a Transformed Reciprocal Function → this KP. Prerequisites: Combining Reflections With Other Graph Transformations (2841), Graph Transformations of Reciprocal Functions (3735). Successors (domain/range, vertical asymptotes, intersections) are outside scope.

Normal defaults sample every eligible observed response family: moderate sum and blanks; hard sum and blanks. Easy radio includes two complete method profiles chosen before parameters. Source radio intentions are underdetermined; raw offset masks preserve complete evidence and remain ineligible.
''')
lines=['# Template extraction','', '## 1. Specific source descriptions','']
for sid,q in g.QS.items():
 lines+=['### '+sid,'',q[':question/problem'],'','Parameters: '+json.dumps(g.ANCHORS[sid])+'.','']
 for f in q.get(':question/answer-fields',[]):lines+=['Field '+f[':answer-field/key']+' '+f[':answer-field/type'][':db/ident']+': '+', '.join(a[':answer/value'] for a in f[':answer-field/choices'])+'. Correct: '+f.get(':answer-field/correct',{}).get(':answer/value','absent')+'.','']
 lines += [q.get(':question/worked-solution','Worked solution absent in capture.'),'']
lines+=['## 2. Generalized mathematical backbone','',r'Read k from the horizontal asymptote and b from the vertical asymptote when present. Insert the labelled point into y=a/(x-b)+k; isolate a=(point_y-k)(point_x-b). Return a, a+k, a+b+k, or individual scalar fragments according to the observed response roles. There is no graph-construction task.','', '## 3. Components and complete banks','']
for sid,q in g.QS.items():
 level=g.FAMILIES[g.SOURCE_FAMILY[sid]][0];p=g.norm(g.ANCHORS[sid]);v=p['a']+(p['k'] if level!='easy' else 0)+(p['b'] if level=='hard' else 0)
 for f in q.get(':question/answer-fields',[]):
  for a in f[':answer-field/choices']:
   role='required scalar '+f[':answer-field/key'] if f[':answer-field/type'][':db/ident'].endswith('blank') else 'correct_target + ('+g.fmt(g.NUM(a[':answer/value'])-v)+')'
   lines+=['- '+sid+' / '+f[':answer-field/key']+' / '+a[':answer/value']+' / `raw:'+sid+'` / '+role+'.']
lines+=['','Historical radio offsets are parameterized expression patterns with unknown instructional intent; numerical anchor reproduction is claimed, inferred authoring mistakes are not. Raw profiles are always evidence-only. Blank entries have no distractors or feedback. No source answer feedback is present.','', '## 4. Reusable prompt, solution and slots','', '''Full prompt prose and response fragments are retained from each source. The entire solution prose is retained as a math-island mask: all inline and block components are complete replacements. The ordered asymptote reading → function rewrite → labelled-point sentence → formal equation → coordinate substitution → subtraction/denominator evaluation → a isolation → optional concluding sum is fixed. q-270750 instead retains its y=a+k reduction row, with x=1 fixed; blank templates omit the sum. q-320718 retains its negative-b rewrite and parenthesized negative denominator, conditionally removing the double rewrite for positive b. q-39047 retains the original k+a summation order.

Slots: a (nonzero coefficient), b (zero at easy/moderate, nonzero integer ±1…±3 at hard), k (zero at easy, nonzero halves ±0.5…±3 otherwise), marked x and y constrained by the graph. Easy uses positive integer a and signed same-branch integer coordinate products, |x|=2…8, |y|=1…4, a≤32; these are familiar multiplication-table products, one multiplication regardless of magnitudes. Moderate fixes point x=1, coefficient absolute value 0.5…4. Hard uses an integer point-to-asymptote difference of absolute value 1…3 and coefficient absolute value 0.5…6. All non-easy displayed coordinates remain integers/halves of magnitude at most9. Every explicit input obeys the same bounds. Raw profiles use wider evidence bounds but preserve zero/nonzero shift roles and q-270750 x=1.

Complete authored radio banks: easy-unit [xy,x+y,x-y,y,y/x], easy-product [xy,x+y,x-y,x/y,y/x]; moderate [a+k,a,k,a-k,-a+k]; hard [a+b+k,a-b+k,-a+b+k,a+b-k,a+b]. These are coordinate-operation, omission and sign mistakes from the assessed substitutions. All criterion pairs must be distinct; reject the whole instance. Profiles are selected before parameter sampling.

Raw public replay omits the unrated question's difficulty, missing solution, missing correct ref and the fieldless question's answer-fields attribute. Normal completion of q-39046 uses independently derived a=4 and an authored worked solution. Normal q-113479 receives a supported radio field; neither repair counts as an observed exact designation/layout.

Content identity includes actual prompt, solution, entire displayed bank and difficulty; mathematical task identity excludes seed, option order, profile aliases and renderer padding. It includes the actual graph/point and assessed response role. Blank and sum requests are distinct tasks. No cosmetic aliases are counted as variety.''']
(HERE/'template-extraction.md').write_text('\n'.join(lines))
(HERE/'plot-extraction.md').write_text('''# Plot extraction

1. Every native source is 360×304. Blue reciprocal branches, black axes with positive arrowheads, one blue marked point and coordinate label; gray dashed nonzero asymptotes with signed labels. There is no grid. Each source's origin and per-axis pixel unit are independently transcribed in plot-extraction.json, including the canonical example. q-39046 has zero asymptotes coincident with axes; the negative-a sources have upper-left/lower-right branches. Every source graph was visually inspected at native resolution.

2. Shared pattern: a labelled point plus horizontal/vertical asymptote locations determine a=(y-k)(x-b). The positions of these features are the assessed information.

3. Per-source JSON records origin, independent x/y calibration, marker location, each asymptote, each signed axis tick label, branch sign and locations, both arrowheads, hashes and full blue-stroke geometric checks. The numerical check measures native pixel distance to the implicit hyperbola using its pixel gradient and allows 2.2 pixels for stroke width/calibration; a marker region must contain at least8 blue pixels. This establishes geometry independently of image hashes. Blue-stroke measurements cover every visible branch pixel outside a six-pixel marked-point neighborhood; the larger marker is checked separately.

4. New plots use Matplotlib, true zero axes, blue curve, dashed nonzero asymptotes, explicit signed tick/point labels. Bounds depend on asymptote/point features and include zero. Curve branches are rendered separately to avoid crossing the asymptote. Geometry sidecars record exact parameters, transform, pixels, plotted labels and Python/Matplotlib versions. Temporary files are unique and final PNG/JSON writes atomic. A cache hit requires both assets. Raw anchor replay can reuse the inspected native asset; changed parameters always require new plots. No SVG generation or image model is used.

Normal PNG checks recover the axes transform from the rendered dimensions/bounds, independently calculate the marked point and >12 reciprocal curve positions, test actual blue pixels, verify true zero-axis black strokes and gray asymptote strokes, read back the actual Matplotlib text artists, and check every label bounding box stays within the native canvas. Both visible branches are required. Concurrent fresh identical/different renders are tested in a private directory.
''')
(HERE/'README.md').write_text('''# Reciprocal graph unknowns — scratch draft

Run `.venv/bin/python generate/scratch/17592186068780/validate.py` from the repository root. CLI: `.venv/bin/python generate/scratch/17592186068780.py --difficulty all --seed 42 --count 2 --format json`.

Five source-shaped response families, all three levels. Easy is authored from an unrated unshifted graph source. Moderate/hard preserve observed recovery steps and scalar fragments; method radio banks are authored, while opaque complete historical banks remain public `raw:q-ID` evidence profiles. See source-cases.json for exact replay parameters. Raw omissions remain absent. All raw outputs are explicitly ineligible; normal outputs have supported native contracts.

Exact source question prose, solution masks, answer values and key-presence are checked separately from correctness and native grading. No database writes, registration, shared environment edits or step8 artifacts. Local PNG assets and evidence are retained for parent QA.
''')
print('Native source geometry passed',len(plots))
