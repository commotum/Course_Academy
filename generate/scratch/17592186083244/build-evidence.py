from pathlib import Path
import importlib.util,json,hashlib,sys
import PIL
ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('g',ROOT.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
context=json.loads((ROOT.parents[2]/'generate/runs/current/topics/17592186050162.json').read_text())
lesson=json.loads((ROOT.parents[2]/'generate/runs/current/lessons/17592186050162.json').read_text())
source=json.loads(Path('/home/jake/Developer/MA/DATA/Lessons/799/Source/799.json').read_text())
def find(value):
 if isinstance(value,dict):
  if value.get('question_id')=='6862':return value
  for v in value.values():
   result=find(v)
   if result:return result
 elif isinstance(value,list):
  for v in value:
   result=find(v)
   if result:return result
widget=find(source);(ROOT/'source-widget-q6862.json').write_text(json.dumps(widget,indent=2,ensure_ascii=False)+'\n')
route=[]
for activity in lesson['record']:
 steps={s[':db/id']:s for s in activity[':activity/steps']};current=activity[':activity/first-step'][':db/id']
 while current:
  step=steps[current];content=step[':step/content'];route.append({'step':current,'content':content[':db/id'],'title':content.get(':tutorial/title',content.get(':knowledge-point/title'))});current=step.get(':step/next',{}).get(':db/id')
(ROOT/'lesson-route.json').write_text(json.dumps(route,indent=2)+'\n')
(ROOT/'classification.md').write_text('''# Classification — KP 17592186083244

Database `math`, basis **1356**, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. Frozen wrappers are the sole source of observed enums. Six practice questions have seven fields and 23 answer values. Outer generator `knowledge_point` uses plain keys; captured inner enums become ident strings, and correct answer entities become owned lookup references.

| Observed difficulty | Questions | Field/layout | Mathematical templates | Plot rating |
|---|---:|---|---|---|
| moderate | 2 | radio whole line (5 options), blank RHS of `y=` | cubic/quadratic point-slope line; cubic/quadratic slope-intercept line | none |
| hard | 3 | radio coordinate pair (5 options) ×2; two coordinate blanks | exponential-product y-intercept; trigonometric-sum x-intercept; logarithmic-product y-intercept | none |
| absent | 1 | radio whole line (5 options), missing correct ref | quadratic/fifth-power tangent line | none |
| easy | 0 | authored radio whole line (5 options) | canonical-grounded linear/cubic tangent line | none |

Difficulty values are checked as well as key presence: exactly two `:question.difficulty/moderate`, three `:question.difficulty/hard`, and one absent. The unrated question does not acquire a captured difficulty in raw replay. Its normal moderate assignment is authored.

The canonical e-597 uses x=2t+3, y=t³−4t, t=−1: one constant coordinate derivative and one polynomial derivative, then derivative ratio and point-slope form. It anchors the missing easy level. The observed moderate problems differentiate both coordinates, while the hard problems compute a tangent then substitute the requested axis value. Source e-597's supplemental plot is not an assessment input; none of the six practice prompts, answer banks or solutions has an image reference.

The actual linked lesson route in lesson-route.json is Introduction → this KP → Horizontal or Vertical Tangents tutorial → Determining Points Where Tangent Is Horizontal/Vertical → Computing Normal Line → Determining Points Where Normal Is Horizontal/Vertical. The prerequisite KPs are Differentiating Parametric Curves and Calculating Equation of Tangent Line Using Differentiation. This generator does not search for horizontal/vertical parameter values or calculate normal lines. All supported tangent inputs have finite nonzero slopes.

Observed banks are kept intact as six public observed profiles, including both blank layouts. Three radio banks contain opaque historical distractors. Their explicit component generalizations are evidence only and not claimed as recovered mistake algorithms. Normal banks have four complete operation-derived errors; the bank is rejected as a whole when any option is equivalent, undefined, or correct.
''')
sections=['''# Template extraction

## 1. Describe every original specifically

Original prompts and all five present full worked solutions are in source.json and are publicly reconstructed at original parameters. q-6862 has no worked-solution attribute, difficulty attribute, or correct designation. source-widget-q6862.json confirms the original widget is a five-choice whole-equation multiple-choice layout, with the same values up to ordering, but it also contains no correct key or worked solution. The unique tangent equation is independently derived as y+1=−5/4(x−3); this is a mathematical inference, not a recovered designation.
''']
for c in g.CASES:
 q=g.QUESTIONS[c['source_id']];r=g.generate(c['level'],template=c['template'],parameters=c['parameters'],profile=c['bank_profile'])
 sections += [f"### {q[':question/math-academy-id']} / {c['source_id']}\n\nTemplate `{c['template']}`, raw profile `{c['bank_profile']}`. Parameters `{json.dumps(c['parameters'],sort_keys=True)}`. Difficulty: `{q.get(':question/difficulty',{}).get(':db/ident','ABSENT')}`.\n\n"+q[':question/problem']+'\n\n| Field | Type | Original answer value | Original correct? | Parameterized complete object |\n|---|---|---|---|---|']
 objects=r['generation']['bank_objects']
 oi=0
 for fi,f in enumerate(q[':question/answer-fields']):
  for a in f[':answer-field/choices']:
   correct='absent' if ':answer-field/correct' not in f else 'yes' if a[':answer/id']==f[':answer-field/correct'][':answer/id'] else 'no'
   sections.append('| '+f[':answer-field/key']+' | '+f[':answer-field/type'][':db/ident']+' | $'+a[':answer/value']+'$ | '+correct+' | profile recipe '+str(oi+1)+': `'+r['generation']['recipes'][oi]+'`; complete object `'+str(objects[oi])+'` (stage 3 formula order) |')
   oi+=1
 sections.append('\nComputed bank objects at original parameters (ordered by the fixed profile, not shuffled display):\n\n```json\n'+json.dumps(objects,indent=2)+'\n```\n')
sections += ['''## 2. Generalize the shared pattern

Substitute the given parameter into x(t), y(t); differentiate both coordinates; use y′/x′ at that parameter; insert the point and slope in point-slope form. Whole-line radios retain whole equations; RHS blanks retain only the missing expression. Hard intercept questions additionally set x=0 or y=0 and rearrange. Trigonometric arguments are radians; exponential problems stay at t=0, trigonometric ones at π/2, and log ones at eⁿ so the exact arithmetic remains familiar.

## 3. Map all components and complete profiles

Use P=(p,q), D=x′(u), E=y′(u), m=E/D, B=q−mp, A=p−q/m.

* polynomial raw bank: y=(12m/11)x+m/11; y−q=(m/2)(x−p); correct y−q=m(x−p); y−q=m(x−q); y−q=(m/2)(x−q). The 12/11 and 1/11 expression has no identifiable method error from the sole source. This entire bank is evidence only.
* quintic raw bank: y+q=(3m/5)(x−p); y−q=m(x+p); y−q=m(x−p); y+q=2m(x−p); y−q=−m(x−p). Raw designation is absent. Normal inference is unique third relation; its new bank and complete solution are explicitly authored.
* exponential raw bank, ω=wπ: (0,m), (0,ω/p), (0,−ω), correct (0,B), (0,−m/p). The historical intent of ω/p and −ω is unresolved, so the whole raw profile is evidence only.
* trig raw bank: (2A/3,0), correct (A,0), (6A/7,0), (6A/5,0), (3A/4,0). These are deliberately documented component ratios reproducing the source's opaque 2/9, 1/3, 2/7, 2/5, 1/4 bank. They are not promoted to normal practice.
* polynomial RHS blank: mx+(q−mp). No bank/distractors added.
* log coordinate blanks retain captured field order field-2 then field-1; values B then 0, while the prompt's tuple remains field-1 then field-2.

Normal whole-line radio complete bank: tangent; inverted derivative ratio through P; negated slope through P; tangent with reversed point x coordinate; tangent with reversed point y coordinate. Each wrong operation comes from computing slope or inserting P into point-slope form. Normal exponential intercept bank: correct B; omit exponential chain factor in x′; reverse slope sign; return C's y coordinate; return slope as intercept. Normal trig intercept bank: correct A; wrongly set cos(π/2)=−1 in x′; reverse slope sign in axis calculation; return C's x coordinate; omit C's x coordinate. All five values are built together, and collisions reject the complete instance.

The historical source prose is shared by complete mathematical-span slots. Replacements cover introductory t, both coordinate substitution/evaluation chains, point prose, both derivatives, formal derivative ratio, every ratio simplification row, every numeric slope row, point-slope substitution, all line rearrangements, and final prose equations/tuples. No short-number replacement occurs. No source IDs/answer UUIDs are used to determine mathematical correctness.

## 4. Extract constrained reusable templates

| Family | Supported explicit/sampled parameters | Workload preserved |
|---|---|---|
| authored easy | a∈±1..±4, b∈−5..5, c∈±1..±3, d∈±1..±5, u∈{−2,−1,1,2}; x=at+b, y=ct³+dt | 3 nonzero coordinate terms, constant x′, 2-term y′; no axis step |
| moderate polynomial | a=1..3, b=1..6, c=1..4, d∈±1..±6, u∈{−2,−1,1,2}; x=at³−bt, y=ct²+d | 4 coordinate terms; 2-term x′, 1-term nonconstant y′; point-slope or RHS rearrangement |
| authored-rated quintic | a=1..3,b=1..4,c=1..3,u∈{−1,1}; x=at²−bt,y=ct⁵ | same two derivative computations and ratio; familiar fifth powers avoid arithmetic escalation |
| hard exp | a=2..5,h=1..4,w=1..3; x=e^(at)+h,y=eᵗsin(wπt),u=0 | chain derivative, product derivative, exponent cancellation, y-axis substitution; 48 curve/intersection tasks before bank exclusions |
| hard trig | a,b,c,k=1..4,h reduced nonintegral rational with numerator magnitude1..6 and denominator2..6; x=a sin t+b cos t+h,y=c cos t+k,u=π/2 | both trig derivatives, reciprocal then sign-reversed ratio, familiar evaluation, x-axis substitution |
| hard log | n=1..3,k=1..4; x=t(ln t+k),y=ln t,u=eⁿ | product derivative, common denominator ratio, exact logarithm evaluation, y-axis substitution; 12 meaningful tasks |

Each difficulty has unordered variations of its own required method, with no internal progression. Nonzero coefficients retain every advertised term. Explicit inputs obey the same bounds as sampling and are never silently altered. Every source anchor is valid for both its raw profile and completed normal family. Every raw profile is publicly parameterized and separately exercised away from its anchor; bank equality/ambiguity guards remain applicable. An absent source difficulty stays absent in raw output.

Finite-slope limits avoid introducing a new conditional tangent-classification branch. The domain is all real t for polynomial/exponential/trig sources and t>0 for log. No rounding is introduced. Normal log exact-entry wording uses “Give exact answers.” because the native engine detects every occurrence of “round” as requiring identical form; public raw replay retains “Do not round the answers.” and documents its rejection of correct equivalent submissions.
''']
(ROOT/'template-extraction.md').write_text('\n'.join(sections))
(ROOT/'plot-extraction.md').write_text('''# Plot extraction and decision

Practice sources: zero prompt, option, or solution plot references. Plot rating **none** for every supported practice template; normal output has no plot generation or plot cache. Fresh/cache plot equality and concurrent atomic rendering are therefore inapplicable, rather than silently claimed as tested.

Canonical e-597 contains supplemental solution image `images/0f/0fa3fc12e83e2a581499680145df9229917c7426e6a3d12c51d88e115a42033e.png`, inspected at full 360×304 resolution and composited onto white in canonical-inspection.png because the original is transparent. It shows black unlabeled-scale axes with positive arrowheads, blue cubic curve, orange dashed tangent with negative slope, and orange point above/right of the origin. No numerical tick labels or traversal arrows exist. At original parameters, the point is (1,3), slope −1/2, intercept7/2; the parametric curve is y=((x−3)/2)³−4((x−3)/2). The local maximum is at t=−2/√3 and x=3−4/√3≈0.691, to the left of the tangent point; local minimum at x≈5.309. The observed blue curve and tangent agree with these qualitative features. Exact crop bounds are not labeled and are not asserted.

General illustrative specification if later requested: Matplotlib equal geometry with black axes, the actual parametric cubic, dashed tangent through actual tangent point, orange point marker, bounds derived from extrema and tangent point. It is optional illustration and does not affect the learner's computation. This draft deliberately has no changed-parameter figure because no practice source requires one and authored easy prose never claims a plot is present. No direct SVG or image model was used.
''')
(ROOT/'README.md').write_text('''# Parametric tangent-line generator

Run from the repository root:

```sh
.venv/bin/python generate/scratch/17592186083244/validate.py
.venv/bin/python generate/scratch/17592186083244.py --difficulty all --seed 42 --count 2 --format json
.venv/bin/python generate/scratch/17592186083244.py --difficulty hard --profile observed_17592186319230
```

Public Python API: generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None), plus generate_easy/generate_moderate/generate_hard. Normal default profiles use authored complete banks. Public observed profiles reproduce raw captured field layouts and omission/presence; they are explicitly evidence_only and ineligible. source-cases.json contains all six calls at original parameters. No DB clients, registration, shared environment changes or plots are generated.

Scope: substitute parameter, derive finite tangent slope, compute line; hard asks its source-shaped axis intersection. Easy is the missing-level authored canonical extension. Moderate quintic rating/key/solution are authored from independent mathematics because captured q6862 lacks them. Source opaque banks are parameterized evidence, with unresolved intent documented. Full line equations are checked modulo nonzero scalar using actual point and derivative ratio; native UUID grading is separate. Native blank equivalents are exercised for every coordinate field. Raw log “Do not round” intentionally retains the engine's rejection limitation; normal “Give exact answers” preserves the exact-answer mathematical demand.

Evidence: source.json frozen wrapper; source-widget-q6862.json original widget confirming absent key; lesson-route.json next-link traversal; classification.md; template-extraction.md; plot-extraction.md; canonical-inspection.png; review.md/json; engine-input/report.json; validation.json. display-parser.py is a private read-only copy of the parent elementary parser, used independently of generator helpers and mathematics metadata. validate.py checks every original value, captured difficulty enum/presence, source prose/row fidelity, displayed curve and all solution stages, choice ambiguity, level limits, JSON equality, identity, and native grading. The parser is fail-closed for supported displayed forms.
''')
asset=Path('/media/jake/SSD/EDB/math/images/0f/0fa3fc12e83e2a581499680145df9229917c7426e6a3d12c51d88e115a42033e.png')
provenance={'source_sha256':hashlib.sha256((ROOT/'source.json').read_bytes()).hexdigest(),'canonical_asset':str(asset),'canonical_asset_sha256':hashlib.sha256(asset.read_bytes()).hexdigest(),'canonical_size':[360,304],'source_lesson_json':'/home/jake/Developer/MA/DATA/Lessons/799/Source/799.json','native_engine_sha256':hashlib.sha256((ROOT.parents[2]/'generate/runs/current/check-engine').read_bytes()).hexdigest(),'private_parser_sha256':hashlib.sha256((ROOT/'display-parser.py').read_bytes()).hexdigest(),'python':sys.version.split()[0],'inspection_compositor':{'library':'Pillow','version':PIL.__version__,'operation':'RGBA composited onto white for full-resolution inspection'},'plot_renderer':None}
(ROOT/'provenance.json').write_text(json.dumps(provenance,indent=2)+'\n')
