"""Create local extraction documentation from immutable source evidence."""
import inspect, importlib.util,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('g',ROOT.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
original=json.loads(Path('/home/jake/Developer/MA/DATA/Lessons/803/Source/803.json').read_text())
def find(o):
 if isinstance(o,dict):
  if o.get('question_id')=='70341':return o
  for v in o.values():
   x=find(v)
   if x:return x
 if isinstance(o,list):
  for v in o:
   x=find(v)
   if x:return x
widget=find(original);assert widget
(ROOT/'q-70341-widget.json').write_text(json.dumps(widget,indent=2,ensure_ascii=False)+'\n')
head='''# Classification

Source: immutable `math` snapshot at basis **1356**, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`; full wrapper retained in `source.json`.

There are 16 practice sources: 8 easy, 7 moderate, 1 unrated. Canonical e-5292 is context, not counted as practice. All inputs are independent affine sine/cosine coordinates on **0≤θ<2π**. That half-open parameter interval still attains both coordinate extrema: cosine ±1 at 0/π and sine ±1 at π/2 and 3π/2. Both coordinate output intervals are closed. No calculus or Cartesian elimination occurs.

Each difficulty uses radio (one field, five complete interval-pair options) and blank (six endpoint/relation fragments) layouts. Easy: 4 radios and 4 six-blank sources; moderate: 3 radios and 4 six-blank sources. The unrated source is one radio. No source graphs or image references occur in this KP; plot rating **none**.

The implementation has 16 named source presentation/stage recipes, plus one authored hard recipe. A named source recipe preserves its exact prose, field order, placeholder positioning, omitted unit-scaling row, negative-coefficient reversal row, shift-first notation and radio closing sentence. These are presentations of the same affine-range method, not claims that a changed coefficient defines a new skill/template. Recipes that differ only in field/key order or rational-number workload are intentionally documented as layout/workload profiles within that method.

Unrated q-70341 is assigned **authored moderate**, because each coordinate requires scaling and translation as in q-327882. Its original widget has five options and no captured solution or correct marker. Correct [-4,2]×[0,4] follows from 3[-1,1]−1 and 2[-1,1]+2. Captured widget ordering differs from the database ordering; full sets match. Correct designation is **inferred**, never counted as source-matched. Its supplied worked solution is separately authored.

## Source inventory

| Source | Captured level | Fields | a,b,h,k | Coordinate stages x/y | Bank/profile |
|---|---|---|---|---|---|
'''
for sid,q in g.SOURCES.items():
 spec=g.TEMPLATES[sid];p=g.parse_parameters(dict(zip('abhk',g.PARAMS[sid])))
 stages=[len(x.split(r'\\')) for x in re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',q.get(':question/worked-solution',''),re.S)]
 head+='| '+sid+' | '+('unrated' if sid=='q-70341' else spec['level'])+' | '+spec['kind']+(' ×6' if spec['kind']=='blank' else ' ×1 (5 options)')+' | '+','.join(str(p[v]) for v in 'abhk')+' | '+str(stages or 'absent')+' | '+('observed:'+sid if spec['kind']=='radio' else 'no bank')+' |\n'
head+='''
## Scope and level bounds

Lesson order is recovered through activity/first-step and step/next: introduction → table of values → curve plotting → polynomial ranges → alternative parameter θ → this trig-range KP. Its prerequisite is **Properties of Transformed Sine and Cosine Functions (2062)**. The sibling range KP separates coordinate range analysis from plotting; Cartesian Equations of Parametric Curves is a downstream topic and excluded here.

Observed easy recipes keep their original zero-shift/unit-scale/negative-sign/fraction structure; moderate recipes keep their observed sign/translation and integer-versus-rational arithmetic structure. Original values are eligible. Each source recipe preserves signs and zeros, unit/nonunit status, integer/noninteger status, and thus the same number of multiplication, reversal, translation and endpoint stages when parameters change. Magnitudes ≤9 and denominator ≤4 are enforced on explicit inputs and sampling. All four coordinate coefficients/shifts are displayed and substantive; the fixed domain is not cosmetic variety.

**Missing hard is authored, not recovered:** both a and b are negative nonintegral rationals; both h and k are nonzero nonintegral rationals; magnitudes ≤9, reduced denominators 2/3/4. Both coordinates have exactly five aligned rows: base trig interval, reversed signed multiplication, reordered interval, translation of both endpoints, simplified coordinate range. This requires exactly two signed inequality reversals and four rational endpoint additions. It adds a second noninteger negative scale/reversal beyond moderate q-327884 (one negative rational scale), while retaining that example's rational translations and familiar arithmetic. At least one final endpoint in **each** coordinate must remain fractional, preventing full cancellation of its fractional endpoint work. Hard samples have no new function, branch, angle evaluation, domain restriction, graph-choice task or identity manipulation. Every hard instance has this fixed workload; there is no internal progression.
'''
(ROOT/'classification.md').write_text(head)
text='''# Template extraction

The four stages below are based on all 16 practice records at basis 1356. `source.json` retains every original field and snapshot provenance; `review.md` displays all original prompts, banks, layouts and complete worked solutions. `source-cases.json` replays every original through the normal parameterized renderer. No source payload is returned as a special-case answer lookup.

## 1. Describe each source specifically

All coordinates are x=a cos θ+h and y=b sin θ+k, with θ∈[0,2π). The source inventory in `classification.md` lists every signed/rational coefficient, shift, response layout and per-coordinate row count. Radio prompts have no embedded field token and conclude with the pair of ranges; blank prompts retain every original {{field-N}} placement, endpoint slot, relation slot, and key order and omit that final summary as observed. The original Unicode function application marker, `operatorname` notation, whitespace and shift-first forms are retained in source replay.

Each coordinate solution starts with its trig range. A positive nonunit scale adds a multiplication row. A negative scale adds reversed inequalities and then an ascending reordered row. A nonzero shift adds one unevaluated endpoint-translation row. The final row names x/y, followed by the original “So, we can conclude” sentence. Unit scaling rows are omitted exactly as in the sources. No new stage is appended to make rescaling convenient.

## 2. Generalized mathematical pattern

Determine two independent coordinate ranges by applying signed scale and additive translation to the known sine/cosine interval [-1,1]. Return the complete ordered closed interval pair or the six supplied endpoint/inequality fragments. The complete pair is assessed; comparison never checks only one coordinate or only an endpoint.

## 3. Components and every observed choice

Let a,b,h,k denote displayed parameters; A=|a|, B=|b|. Let C=(h−A,h+A,k−B,k+B)=(l,u,m,n), and interpret each four-tuple as xmin≤x≤xmax, ymin≤y≤ymax. The exact complete observed bank formulas are below (the branch order is the original database choice order). This is an explicit expression-pattern replay mapping. Its identities and numerical values are independently checked against displayed choices at every original, and its parameterized variants are checked for valid intervals and collisions.

```python
'''+inspect.getsource(g.observed_bank)+'''```

Supported method hypotheses (not learner-facing diagnosis): q-16201 swaps amplitudes or uses [0,1] for each trig function, including a compound swapped-amplitude plus nonnegative-range option. q-123777 and q-123773 include negation of complete translated ranges, omitted shifts/unit bounds, and treating a shift as an amplitude. q-123775 includes reciprocal x amplitude and negated translated y range, including the compound reciprocal-plus-negation option, and treating the y shift as its amplitude. These operations can account for the complete values at the source parameters but cannot prove author intent.

**Residual underidentified patterns:** q-16201's degenerate (1,1,1,1) option; q-123775's cross-coordinate (k−2B,k,m,n); all four wrong choices of q-70523 and q-73632; the mixed-endpoint distractors of q-73626 and q-70341. Their complete expression patterns are preserved only in explicitly selected observed profiles, not promoted to default error-method banks. Their formulas are one bounded replay extension consistent with the captured values; the evidence does not identify unique generalization or author intent. This distinction is not a mathematical-fidelity failure: complete source values still match. It limits the pedagogical interpretation and use of those profiles.

### Exact field mapping at original parameters
'''
for sid,q in g.SOURCES.items():
 spec=g.TEMPLATES[sid]
 text+='\n#### '+sid+'\n\nParameters: '+str(dict(zip('abhk',g.PARAMS[sid])))+'. Template/profile: '+sid+' / '+('observed:'+sid if spec['kind']=='radio' else 'none')+'.\n\n'
 for f in q[':question/answer-fields']:
  text+='Field `'+f[':answer-field/key']+'` ('+f[':answer-field/type'][':db/ident']+').\n\n'
  for i,a in enumerate(f[':answer-field/choices']):
   iscorrect=f.get(':answer-field/correct',{}).get(':answer/id')==a[':answer/id'];status='observed correct' if iscorrect else 'correct designation absent' if sid=='q-70341' else 'observed wrong' if spec['kind']=='radio' else 'fragment'
   text+=str(i+1)+'. `'+a[':answer/value']+'` — '+status+'; mapped to '+('bank formula tuple '+str(i+1) if spec['kind']=='radio' else {'field-1':'h−A','field-2':'\\le (left/upper relation according to original placement)','field-3':'h+A','field-4':'k−B','field-5':'\\le (left/upper relation according to original placement)','field-6':'k+B'}[f[':answer-field/key']])+'.\n'
text+='''
## 4. Reusable template, constraints and calculations

Fixed: parameter domain 0≤θ<2π, sine/cosine roles, independent coordinate method, source field ownership, radio count=5, blank count=6, exact math answer type and fragment shape. Variable slots are the **whole coordinate formula**, **whole aligned row block**, and **whole concluded coordinate interval**. Coordinate text is rendered directly from current parameters into the unchanged prose skeleton. Slots never globally replace a short numeral/function/variable across unrelated prose. First-shift notation, sign reversal and omission of unit scaling are conditioned on extracted source structure; explicit guards preserve these regimes.

For each coordinate compute L=d−|c| and U=d+|c| exactly with SymPy Rational. Every printed intermediate inequality is independently parsed and checked against the actual displayed coordinate formula over trig value [-1,1]. The domain remains half-open in θ while output endpoints remain attained/closed. Source replay compares complete prompt and worked solution byte-for-byte, plus every field's type/key/bank/correct designation mathematically, allowing harmless answer whitespace/fraction notation normalization. q-70341's missing solution/designation is excluded only from those absent-value denominators, not from prompt/bank coverage.

Normal radio generation chooses one complete authored method bank. If h=k=0 the five entries are: C, restricting both trig functions to [0,1], doubling both amplitudes, halving both amplitudes, swapping amplitudes. If at least one shift is nonzero they are: C, omitting both shifts, doubling both amplitudes, halving both amplitudes, negating both complete ranges. These are separately labeled bank extensions; their cardinality matches the sources. Every option is computed before validation; the whole instance is rejected for reversed ranges, equivalence, a correct distractor or collisions. There is no first-valid candidate pool or post-hoc replacement of a wrong option.

Observed profiles are selected explicitly by `observed:<source-id>`, preserving their complete bank. Invalid explicit inputs raise; random sampling rejects and resamples the whole instance under the already chosen complete profile. Blanks never acquire distractors. One fixed solution is generated independent of selected wrong options.

Presentation identity hashes version, level, template, complete bank/profile/layout, canonical parameters, displayed prompt and fixed solution, excluding seed and choice order. Mathematical-task fingerprint separately canonicalizes the actual two affine trig formulas and fixed domain, excluding layouts and profiles. Hence radio/blank presentations of the same assessed formulas deduplicate mathematically while differing display banks remain separate content records.
'''
(ROOT/'template-extraction.md').write_text(text)
(ROOT/'plot-extraction.md').write_text('''# Plot extraction

All 16 source prompt/choice/solution records and canonical e-5292 were inspected for image references. None occur in this KP. The owning lesson has plots in its introduction and sibling graphing/table sections; they do not belong to this assessed template and are not inserted into generated questions. Plot rating: **none**. No parameter-dependent plots or asset recreation is required. No image model, direct SVG, Matplotlib or TikZ is used.
''')
(ROOT/'README.md').write_text('''# Trigonometric parametric range generator

Local, frozen step-7 candidate. No EDB writes or registration.

```sh
.venv/bin/python generate/scratch/17592186087736/validate.py
.venv/bin/python generate/scratch/17592186087736.py --difficulty all --seed 5 --count 2 --format markdown
.venv/bin/python generate/scratch/17592186087736.py --difficulty moderate --template q-70523 --profile observed:q-70523 --count 2 --format json
```

API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` plus `generate_easy`, `generate_moderate`, `generate_hard`. Explicit parameters have exactly a,b,h,k and accept exact rational strings. Source replay cases use every original bank/profile. Normal radio defaults use complete authored method banks; observed residual banks remain explicit.

All levels keep full-period sine/cosine coordinate ranges. Hard is authored with both negative fractional scales and both nonzero fractional shifts, two inequality reversals and four rational endpoint additions. See `classification.md` for exact guards and curriculum rationale. `template-extraction.md` distinguishes defensible wrong operations from underidentified source expression patterns.

`validation.json` separates 16 source prompts/banks, 15 available exact solutions, 55 available source correct designations, and the one independently inferred designation/one authored missing solution. Native grading is `course_academy_engine::learning::grade_field`, using the shared memory-only harness. The validator parses actual displayed mathematics and every intermediate inequality, not just generation metadata. Review includes every original, source replay and generated profile plus at least two examples per level. No plots.
''')
print('Evidence documents written.')
