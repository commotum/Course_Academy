"""Build prose/review/plot evidence after mathematical and grading validation."""
import importlib.util,json,re,hashlib
from pathlib import Path
from PIL import Image
H=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('g',H.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
review=json.loads((H/'review.json').read_text());cases=json.loads((H/'source-cases.json').read_text())
# Record each raster's own pixel geometry/scales; alpha compositing retains it.
plots=[]
for sid,q in [('e-5072',g.SOURCE['record'][':knowledge-point/canonical-example'])]+list(g.RECORDS.items()):
 p=Path('/media/jake/SSD/EDB/math')/re.search(r'!\[\]\((.*?)\)',q[':question/problem'])[1]
 im=Image.open(p).convert('RGBA');bg=Image.new('RGBA',im.size,'white');bg.alpha_composite(im);im=bg.convert('RGB');blue=[]
 for y in range(im.height):
  for x in range(im.width):
   rr,gg,bb=im.getpixel((x,y))
   if bb>rr*1.6 and gg>rr*1.5 and rr<100:blue.append((x,y))
 xmin,xmax=min(x for x,y in blue),max(x for x,y in blue);ymin,ymax=min(y for x,y in blue),max(y for x,y in blue)
 a,b=(g.rat(2),g.rat(4)) if sid=='e-5072' else tuple(map(g.rat,g.SOURCE_GEOMETRY[sid]))
 sx=(xmax-xmin)/(2*float(a));sy=(ymax-ymin)/(2*float(b))
 assert abs(sx-sy)<1.4,(sid,sx,sy)
 plots.append({'source_id':sid,'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'size':im.size,'blue_curve_bbox':[xmin,ymin,xmax,ymax],'fitted_origin':[(xmin+xmax)/2,(ymin+ymax)/2],'pixels_per_unit_x':sx,'pixels_per_unit_y':sy,'radii':{'a':str(a),'b':str(b)},'visually_inspected':'native-resolution source sheets 0–3; q-7605 also individually at original resolution','observed_bottom_label_error':sid=='q-7605'})
(H/'source-plots.json').write_text(json.dumps(plots,indent=2)+'\n')
classification='''# Classification: Determining the Equation of a Tall Ellipse

Captured immutable database `math`, basis 1356, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. Canonical e-5072 is evidence, not a practice question. There are 21 practice questions, 69 answer values, 12 five-choice radio banks and 9 one-answer blank banks.

| Level | Practice counts | Markdown/value templates | Bank profiles | Plots |
|---|---:|---|---|---|
| Easy observed | 11 radio, 2 blank | integer_radio; integer_blank | 11 original radio profiles; blank | heavy: plotted intercepts carry the prompt |
| Unrated | 1 radio, q-7605 | integer_radio (authored easy assignment) | q-7605 | heavy |
| Moderate observed | 7 blank | half_blank | blank | heavy |
| Hard authored | 0 observed | rational_blank | blank | heavy |

The graph is centered at (0,0), axes are aligned with coordinates, and vertical radius exceeds horizontal radius. Blanks supply `=1` and require only the LHS. Radio choices are complete equations, not separately compared sides. No shifted centers, rotation, eccentricity, foci, major-axis identification, or square-root extraction is introduced.

Lesson order is recovered by following activity/first-step 17592186088758 and next links, not collection order: Introduction → Wide Ellipse (17592186087839) → Tall Ellipse (17592186087840) → Major and Minor Axes tutorial → Axis lengths (17592186087841). The current skill therefore uses radii, before the later major/minor-axis terminology. Previous topics are Introduction to Ellipses and Circles Centered at the Origin; general centers occur afterward. The tutorial and canonical example use the same x²/a²+y²/b²=1 substitution.

Hard is a declared authored extension, never an inferred source label. It replaces exact half-unit radius labels with exact thirds/quarters (both noninteger), requiring the same graph reading, fraction squaring and reciprocal simplification. All hard instances share that workload. Its extra fraction arithmetic stays within the same ellipse equation skill.

q-7605 lacks difficulty, worked solution and correct ref; its lower raster intercept is mislabeled +4. Raw replay retains every omission and exact asset. The supported repair assigns easy, infers x²/9+y²/16=1 from the graph, supplies the shared solution, and renders -4 below the origin. No designation-match credit is claimed for that missing source attribute.
'''
(H/'classification.md').write_text(classification)
parts=['# Four-stage template extraction\n',
'''## 1. Individual observations

Every practice question is listed below with original radii, field shape, source complete value bank and slot operation. Integer radii range from 1 to 9. Moderate radii are reduced integers or halves with at least one noninteger half, shown as decimals on the graph and fractions in the solution. Original formatting is retained, including explicit denominator 1 except q-69892, and q-7605's spaced plain-power syntax. Source-specific banks are never silently merged.
''']
for case in cases:
 sid=case['source_id'];q=g.RECORDS[sid];f=q[':question/answer-fields'][0];profile=sid if sid in g.BANKS else 'blank'
 parts.append(f"\n### {sid}: {case['level']}; {case['template']}; a={case['parameters']['a']}, b={case['parameters']['b']}\n")
 if sid=='q-7605':parts.append('Unrated, correct ref absent, solution absent. Raw key presence is preserved.\n')
 parts.append('| Original complete value/fragment | Slot recipe | Designation | Interpretation |\n|---|---|---|---|\n')
 for i,ans in enumerate(f[':answer-field/choices']):
  recipe=g.BANKS[profile][i] if profile!='blank' else 'reciprocal squared radii; LHS only'
  correct=f.get(':answer-field/correct',{}).get(':answer/id')==ans[':answer/id']
  status='opaque proportional denominator pattern; evidence only' if 'opaque' in recipe else ('decrement-radius hypothesis; evidence only' if '(a-1)' in recipe else 'observed expression operation; cognitive intent unverified')
  parts.append('| `'+ans[':answer/value']+'` | `'+recipe+'` | '+('correct' if correct else ('not designated in source' if sid=='q-7605' else 'incorrect'))+' | '+status+' |\n')
parts.append('''
## 2. Shared mathematical pattern and purpose

Read a>0 and b>a from the labeled horizontal/vertical intercepts of an origin-centered ellipse. Write x²/a²+y²/b²=1. The solution states the general relation, identifies horizontal and vertical radii in prose, substitutes both radius powers, evaluates the squares, and simplifies reciprocals when fractions occur. Integer sources have three aligned rows; fractional sources have four. The solved equation is fixed independently of a selected error.

## 3. Components and complete bank mapping

The tables above map all 69 values. `a2` means a², `b2` means b², `2a` means 2a, `2b` means 2b, `2a2` means 2a², `(a-1)2` means (a−1)² and `(a+1)2` means (a+1)². A pair denotes full denominators of x² and y² with RHS1. Every bank is chosen whole and rejected if any denominator is nonpositive, any complete equations coincide, or there is not exactly one correct equation. No option is replaced from a pool.

Opaque patterns: q-73627's observed denominators (12,32) are parameterized as ((3/4)a²,(8/9)b²); q-7605's (9,4) as (a²,b²/4). These formulas describe normalized denominator patterns only. They are not recovered mistake models. q-73631's (16,49) is written ((a−1)²,b²), but source evidence does not establish that intended error. Those profiles are explicit evidence replay and never default sampled. Other observed expression recipes also remain hypotheses, and all source profiles are explicit replay rather than defaults.

The separate authored default radio bank is exactly: correct squared radii, swapped squared radii, unsquared radii, swapped unsquared radii, and diameters mistaken for squared radii. These five operations are defined before any sampling. No learner-facing distractor diagnosis is added. Normal blank banks have one exact LHS fragment.

## 4. Reusable slots and bounds

Fixed prompt: image followed by “What is the equation of the ellipse given above?” Blank prompts append `{{field-1}}$=1$`. Variable slots are exactly a,b, their squares/reciprocals, the plot geometry/intercept labels, and full-bank operations. Fixed prose and aligned stage ordering are recovered byte-for-byte for every present source solution. General relation and substituted powers stay structurally separate from evaluated values. `solution()` constructs these complete components, without textual global replacement.

Easy: reduced integers 1≤a<b≤12, b/a≤4 (54 exact radius pairs). Moderate: 1≤a<b≤10, values at half increments, at least one reduced denominator2, b/a≤4 (110 pairs). Hard: 1≤a<b≤8, each reduced denominator3 or4, b/a≤3 (315 pairs). All explicit parameters obey the same guards. The domains are finite enumerations; equivalent rational spellings, seed, layout, profile aliases and option order do not increase mathematical task counts. Geometry is the assessed object, not its display alias. Integer easy tasks require squaring integers; moderate tasks require at least one half-unit square; every authored hard task requires two third/quarter squares.

Public profiles named by q-ID replay observed banks and attribute presence. `repair-q-7605` is an explicit supported completion/presentation repair. `authored` and `blank` are normal banks. Source metadata includes immutable provenance. Raw source options/prose/presence fidelity is counted separately from repaired source correctness and authored correctness; missing designation/solution cannot be called matched present data.
''')
(H/'template-extraction.md').write_text(''.join(parts))
(H/'plot-extraction.md').write_text('''# Four-stage plot extraction and renderer specification

1. Specific originals: all 22 PNGs (canonical plus21 practice) are 360×304 with transparent background, black horizontal/vertical axes crossing at the origin, arrows toward positive axes, italic x/y labels, blue ellipse and four intercept tick/number labels. Source sheets0–3 composite each image onto white and paste at native resolution, without enlarging or reducing any original. q-7605 was inspected separately at original resolution. `source-plots.json` records each image's own curve bounds, origin and pixels per unit. Moderate half intercept labels are decimals; solution radii are exact fractions. Each source's curve and own axis scales agree with the transcribed radii; q-7605 has a clear erroneous +4 below the origin, preserved only in raw evidence.

2. Shared visual role: central mathematical prompt, origin-centered axis-aligned tall ellipse. Horizontal intercept magnitude is a, vertical magnitude is b. A graph must change with either radius. Raw replay can reuse its exact original asset only at exactly its original a,b.

3. Components: blue ellipse x=a cos(t), y=b sin(t), t∈[0,2π]; equal scales in x/y; origin; negative and positive intercept ticks; labels ±a,±b; arrowed axes, x/y labels; white background. Labels must remain readable over adjacent curves/axes. Each raster has independent fitted pixel scale; equal overall image dimensions do not imply equal unit scales across originals.

4. Extracted renderer: Matplotlib Agg, 480×400, equal coordinate scales; bounds ±1.2b in each coordinate; blue1.8pt curve; black1.2pt axes; exact integer or half-decimal labels and exact fractional third/quarter labels. White label backgrounds and offsets preserve readability. Own parameter-based asset specification controls every label and curve. Original source style fidelity and generated plot style are distinct: generated figures preserve the mathematical plot components rather than exact source pixels. PNG and sidecar are atomically published from unique temporary inputs. Cache hits require both. Fresh simultaneous identical/different parameter rendering is validated. No caches are pruned. The renderer uses the cached read-only Python3.10 Matplotlib dependency fallback because project Python3.13 lacks Matplotlib; each sidecar records dependency provenance.
''')
# Every original and changed profile, plus at least two per level, visibly labeled.
md=['# Tall ellipse review\n\nOriginals are raw captured practice data. Changed source-profile variants use public parameterized replay and retain the evidence profile omissions; they are not default banks. Normal authored examples and q-7605 repair are labeled separately. Missing source correct designation or solution is stated, not fabricated.\n']
def display(q):
 q=dict(q);q[':question/problem']=re.sub(r'!\[\]\((images/.*?)\)',r'![](/media/jake/SSD/EDB/math/\1)',q[':question/problem']);s=q[':question/problem']+'\n\n'
 f=q[':question/answer-fields'][0];cv=f.get(':answer-field/correct');cid=cv.get(':answer/id') if isinstance(cv,dict) else (cv[1] if cv else None)
 for a in f[':answer-field/choices']:s+='- $'+a[':answer/value']+'$'+(' **correct**' if a[':answer/id']==cid else '')+'\n'
 if not cid:s+='\n**Original correct designation absent.**\n'
 return s+'\n'+q.get(':question/worked-solution','**Original worked solution absent.**')+'\n'
for q,r in zip(g.RECORDS.values(),review['changed_parameter_observed_profiles']):
 sid=q[':question/math-academy-id'];md.append('\n## Original '+sid+' ('+q.get(':question/difficulty',{}).get(':db/ident','unrated')+')\n\n'+display(q));md.append('\n## Generated observed-profile variant '+sid+' ('+r['generation']['template']+'; '+next(c['level'] for c in cases if c['source_id']==sid)+' assigned)\n\nParameters `'+json.dumps(r['generation']['parameters'])+'`. Default sampling eligible: false.\n\n'+display(r['question']))
for i,r in enumerate(review['authored_generated']):
 label='Supported q-7605 repair (authored easy assignment, evidence-only opaque bank)' if r['generation']['presentation_repair'] else 'Authored normal '+r['question'][':question/difficulty'].split('/')[-1]
 md.append('\n## '+label+' example '+str(i+1)+'\n\n'+display(r['question']))
(H/'review.md').write_text(''.join(md))
(H/'README.md').write_text('''# Tall ellipse generator

Script: `../17592186087840.py`. Local review data only; no EDB registration/transactions.

Verification: `.venv/bin/python generate/scratch/17592186087840/validate.py`.
Evidence rebuild before freeze: add `--write-evidence`, then run `build_evidence.py`.
CLI: `.venv/bin/python generate/scratch/17592186087840.py --difficulty all --seed 2 --count 2 --format json`.

Observed integer-radio, integer-blank and half-blank templates replay all21 sources, all69 values, all20 present solutions and correct designations; q-7605's missing attributes are retained in raw public profile replay. The explicit supported q-7605 repair infers its correct equation and fixes its lower intercept label. Source banks have complete public q-ID profiles and are never default sampled. Opaque operations remain labeled evidence only. Normal radio banks are authored assessed-method operations. Hard rational-blank is an authored same-skill extension to thirds/quarters, with no observed hard label claimed.

See classification, extraction, per-asset plot evidence, labeled review and validation/native-grading results. `manifest.json` records SHA256 after private producers freeze; running generation later may append new assets and requires a refreshed manifest if those new artifacts are handed off.
''')
