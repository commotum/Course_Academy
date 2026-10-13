#!/usr/bin/env python3
"""Regenerate local extraction documentation from frozen source and recipes."""
import importlib.util,json,sys
sys.dont_write_bytecode=True
from pathlib import Path
HERE=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('g',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
validation=json.loads((HERE/'validation.json').read_text())
classification='''# Classification — amplitude extraction

Frozen `math` basis 1356, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`; 9 practice sources. `source.json` is the untouched capture wrapper. No database operation was used.

| Observed level | Practice count | Fields | Presentation masks | Plot rating |
|---|---:|---|---:|---|
| easy | 4 | 3 five-option math radios; 1 fieldless | 4 | none |
| moderate | 3 | 2 five-option math radios; 1 fieldless | 3 | none |
| absent/unrated | 2 | 2 five-option math radios without correct refs | 2 | none |
| hard | 0 | none observed | 0 | none |

The mathematical prompt families are a directly supplied coefficient (positive, negative, or implicit one), and a numerator quotient needing separation of its sinusoidal coefficient. The nine masks retain differing operator spelling, invisible function-application character U+2061, fraction position, punctuation, unit coefficient omission and worked-solution layout. Those presentation differences are not nine separate mathematical skills. Seven distinct original complete banks are mapped below before any extension.

Lesson order was followed through activity/first-step and step/next: introduction → this amplitude KP → period KP → midline KP → range tutorial → range KP. The introduction states amplitude |A| for A sin(Bx+C)+D and applies the same formula to cosine. The key prerequisite is Vertical Stretches of Trigonometric Functions. The canonical example e-15609 has negative A=-2, a pi horizontal shift, and D=1. Period, range and midline remain sibling assessments and are not requested here.

## Raw anomalies and scope decisions

q-43277/q-43278 omit difficulty, worked solution and correct refs. Their captured widgets were inspected at full resolution: each has exactly five radio options; neither widget supplied an observed correct designation. Mathematical amplitudes 5 and 2/13 follow independently from the displayed coefficients, but are not counted as matched source correct refs. Their evidence routing levels easy/moderate are authored assignments; raw public output still omits difficulty.

q-117568/q-117575 have observed easy/moderate difficulty and worked solutions but omit answer-fields entirely. Public raw output omits that key. Normal questions have explicitly authored five-choice radio fields, grounded in the supported source layout rather than falsely claiming recovered fields.

All raw profiles are evidence only and ineligible for learning, including mathematically sound banks. q-43277 contains the opaque A² distractor and q-53428 the opaque 1/(BC) distractor; these recipes reproduce observed expression patterns but do not recover a documented error intention. Neither opaque bank is promoted to normal defaults. No mathematical or TeX correction was needed for present source content. Decoded byte counts in decoded-source-byte-counts.json establish actual adjacent backslash counts; no assertion is made from JSON display escaping.
'''
classification+='\n## Per-source inventory\n\n| Source | Observed difficulty | Mask | Original bank | Missing keys |\n|---|---|---|---|---|\n'
for sid,spec in g.SPECS.items():
 q=g.QUESTIONS[sid];level=q.get(':question/difficulty',{}).get(':db/ident','absent').split('/')[-1]
 bank='; '.join(a[':answer/value'] for f in q.get(':question/answer-fields',[]) for a in f[':answer-field/choices']) or 'fieldless'
 missing=[k.split('/')[-1] for k in [':question/difficulty',':question/worked-solution',':question/answer-fields'] if k not in q]
 if any(':answer-field/correct' not in f for f in q.get(':question/answer-fields',[])):missing+=['correct ref']
 classification+=f"| {sid} | {level} | {spec['kind']} | `{bank}` | {', '.join(missing) or 'none'} |\n"
(HERE/'classification.md').write_text(classification)

extraction='''# Template extraction

## Stage 1 — Specific source descriptions

'''
for sid,spec in g.SPECS.items():
 q=g.QUESTIONS[sid]
 extraction+=f"### {sid}\n\n{q[':question/problem']}\n\nParameters: `{json.dumps(spec['params'],sort_keys=True)}`; function `{spec['trig']}`; operator spelling `{spec['spelling']}`. Mask `{spec['kind']}`.\n\n"
 extraction+='Worked solution (complete captured prose and stage sequence):\n\n'+q.get(':question/worked-solution','Absent, preserved as absent.')+'\n\n'
 extraction+='Original response layout: '+('five-option math radio, key `selection`' if ':question/answer-fields' in q else 'no answer-field attribute')+'.\n\n'

extraction+='''## Stage 2 — Shared mathematical pattern

Extract the coefficient of one sine or cosine term in A trig(Bx+C)+D, then return |A|. Argument scaling, phase and constant vertical shifts are distractor-bearing information, not additional requested outputs. The quotient family first splits the numerator across its denominator; its full rewrite must remain visible. All functions are nonconstant (B and sinusoidal coefficient nonzero), with real x and exact numerical coefficients.

## Stage 3 — Complete source component and bank map

Each recipe below is evaluated at the explicit source parameters by generate(..., profile="raw:<source>"). Option order is immaterial; all values and every present correct designation are compared one-to-one. Scalar recipes are numerical structure evidence. Labels below distinguish plausible method confusion from unresolved intention.

'''
interpretations={
'q-43277':['reciprocal vertical coefficient','full vertical extent rather than half extent','half coefficient; intention unresolved','amplitude','squared coefficient; intention unresolved'],
'q-43278':['numerator constant instead of coefficient','denominator instead of coefficient','amplitude','omitted denominator','signed coefficient without absolute value'],
'q-117569':['reciprocal horizontal coefficient','reciprocal argument constant','horizontal coefficient','amplitude','argument constant'],
'q-117570':['reciprocal horizontal coefficient','horizontal coefficient','multiplied external/internal coefficients','amplitude','reciprocal external coefficient'],
'q-117574':['reciprocal external coefficient magnitude','horizontal coefficient','reciprocal horizontal coefficient','amplitude','argument constant'],
'q-117576':['unit numerator divided by Q','vertical constant divided by Q','amplitude','omitted division of vertical constant','omitted division of sinusoidal coefficient'],
'q-53428':['reciprocal horizontal coefficient','horizontal coefficient','reciprocal product of argument parameters; intention unresolved','argument constant','amplitude']}
for sid,spec in g.SPECS.items():
 q=g.QUESTIONS[sid];extraction+=f'### raw:{sid}\n\n'
 if not spec['bank']:extraction+='No source field or bank; raw API output keeps absence. Normal field completion is authored.\n\n';continue
 extraction+='| Source field | Original answer UUID | Exact value | Parameterized recipe | Interpretation | Designation |\n|---|---|---|---|---|---|\n'
 f=q[':question/answer-fields'][0];cid=f.get(':answer-field/correct',{}).get(':answer/id')
 for a,r,label in zip(f[':answer-field/choices'],spec['bank'],interpretations[sid],strict=True):
  extraction+=f"| selection | {a[':answer/id']} | `{a[':answer/value']}` | `{r}` | {label} | {'correct' if a[':answer/id']==cid else 'incorrect' if cid else 'absent'} |\n"
 extraction+='\n'

extraction+='''## Stage 4 — Reusable masks, domains and extensions

The script uses complete coefficient, argument, numerator, denominator and conclusion components. It does not find/replace single digits across prose or return a literal source question payload. Raw prompt styles place the question mark inside/outside math exactly as observed; worked prose and optional rewrite display are also retained. Scalar A and its absolute value are separately rendered in the final prose chain. All generated choice IDs are field-owned UUIDs; field UUIDs derive from stable content identity. Raw local representations normalize enum objects into enum strings and correct entities into lookup refs; database IDs are not part of local question records.

Normal authored notation uses \\sin/\\cos and preserves the same explanation sentences. This is explicitly authored notation, not a claim of exact source formatting. Missing fields, missing source labels and missing correct refs are not repaired inside raw evidence. Raw masks reject parameters their printed structure cannot show, e.g. a bare-x mask requires B=1,C=0.

| Normal family | Level and workload | Parameters and complete bank |
|---|---|---|
| positive | easy: identify positive external coefficient | A reduced positive rational, numerator 1..12, denominator 1..6; A=1 would collide in this bank and belongs to unit instead. B integer 2..6, D=0. [|A|,1/|A|,B,1/B,|A|B] |
| unit | easy: recognize implicit coefficient 1 | A=1,D=0; B=1/b,C=1/c, b,c integer 2..9, b≠c. [1,B,1/B,|C|,1/|C|] |
| negative | moderate: identify negative coefficient then take magnitude | A negative reduced rational, absolute numerator 1..13, denominator 1..6; B integer 2..6,D integer -6..6. [|A|,A,B,1/B,|C|] |
| quotient | moderate: one division, then magnitude | N negative integer -13..-2, Q integer 3..13, gcd(|N|,Q)=1, N/Q noninteger; D integer 1..9; B=1,C=0. Either complete bank [|N/Q|,|N|,|D/Q|,|D|,1/Q] or [|N/Q|,|N|,D,Q,N/Q]. |
| factored | hard: two coefficient operations, then magnitude | P integer ±2..±4; N integer ±2..±13; Q 3..13; gcd(|PN|,Q)=1 and gcd(|N|,Q)=1; |PN|≤36; |N|≠|P| for the complete bank; D 1..9,E nonzero integer -6..6; B integer 1..4,C nonzero. [|PN/Q|,|N/Q|,|PN|,|PD/Q|,|P/Q|] |

Except unit's explicitly bounded reciprocals, C is a reduced rational with |numerator|≤6 and denominator≤6, or a rational multiple of pi with |numerator|≤3 and denominator≤6; |C|≤3pi. These incidental arguments do not require trigonometric evaluation. Raw evidence profiles may use broader exact parameters but remain ineligible.

All normal banks are selected before sampling parameters; the entire instance is rejected on any duplicate, equivalent, missing or invalid option. There is no first-valid option replacement. Recipes derive actual parameter confusion or an omitted multiplication/division/absolute-value step. In particular, the hard bank forgets outer P, forgets Q, selects the numerator constant instead of its sinusoidal coefficient, or ignores N. No learner-facing diagnosis has been invented.

The authored hard scope follows the source quotient rewrite plus the prerequisite's vertical scale: P(D+N trig(Bx+C))/Q+E. Every hard instance exposes two nonunit coefficient operations (multiply P and divide Q), with primitive reduced inputs preventing collapse to moderate's one division or easy's directly supplied coefficient. It adds no graph reading, trig identity, period, range, midline or extrema task. This is an authored difficulty claim, not an observed hard label. Signed P/N, sine/cosine, familiar horizontal shifts and constant offsets are unordered same-level variations. Each hard worked solution has original expression, explicitly unevaluated product/quotient row, collected sinusoidal form, then source-style |A| conclusion.

Mathematical task fingerprints retain only assessed coefficient extraction demand: implicit unit; direct signed reduced A; primitive N/Q; or the hard P,N,Q operation tree. Trig alias, B,C,D,E, choice order and profile are incidental and excluded. Presentation identity includes actual difficulty, prompt, fixed complete solution, complete sorted displayed bank and presence state. Thus changing a distractor-bearing offset changes presentation identity but does not inflate substantive task counts.

Finite eligible mathematical-task domain counts are established by exhaustive candidate signature enumeration with a valid complete bank witness for each signature (no offset/bank/letter multiplicity):

'''
extraction+='| Level | Eligible substantive tasks | Sampled tasks in validation |\n|---|---:|---:|\n'
for l,c in validation['finite_eligible_semantic_domain'].items():extraction+=f"| {l} | {c} | {validation['sampled_semantic_tasks'][l]} |\n"
extraction+='\nAll samplers and explicit calls share guards. The validator tests displayed prompt, every rewrite row and the concluding coefficient/absolute-value chain, whole banks, exact source strings/presence, seed-stable identities, numeric aliases, substantive-domain witnesses, and native grading.\n'
for old,new in [('|A|','abs(A)'),('|N/Q|','abs(N/Q)'),('|D/Q|','abs(D/Q)'),('|PN/Q|','abs(PN/Q)'),('|PD/Q|','abs(PD/Q)'),('|P/Q|','abs(P/Q)'),('|PN|','abs(PN)'),('|N|','abs(N)'),('|P|','abs(P)'),('|C|','abs(C)'),('|D|','abs(D)'),('|numerator|','abs(numerator)')]:
    extraction='\n'.join(line.replace(old,new) if line.startswith('|') else line for line in extraction.split('\n'))
(HERE/'template-extraction.md').write_text(extraction)
(HERE/'plot-extraction.md').write_text('''# Plot assessment — none

There are no prompt, answer or worked-solution plots in any of the 9 practice sources or their generators. All learner content is algebraic. No Matplotlib renderer or sidecar is required.

The introduction's unchanged tutorial image `images/e0/e0ccd47111e0b05a9e8eeba3e8098e6ff0775c183d4c4f95e1bd2fae2a60d949.png` was inspected at full resolution after compositing its transparent pixels on white (`tutorial-context-white.png`). It shows a blue sinusoid, x/y axes, dotted midline, labelled vertical double arrows for amplitude/vertical shift, a horizontal period arrow between troughs, and a phase arrow. It explains which outer coefficient is measured vertically; no numerical geometry is requested in this KP's practice. It remains contextual evidence, is not substituted into generated questions, and does not count as an observed practice template.

Original q-43277/q-43278 widget captures in `/home/jake/Developer/MA/DATA/Lessons/2062/Source/Sections/03-question-43277.png` and `04-question-43278.png` were inspected at full resolution. Their mathematical text and five radio choices agree with the captured EDB values; they display no selected correct answer. No parameter-dependent raster is reused.
''')
(HERE/'README.md').write_text('''# Amplitude generator — frozen step 7

Local script: `../17592186129121.py`. Basis 1356; no EDB writes or engine changes.

```sh
.venv/bin/python generate/scratch/17592186129121/validate.py
.venv/bin/python generate/scratch/17592186129121.py --difficulty all --seed 10 --count 2 --format markdown
.venv/bin/python generate/scratch/17592186129121.py --difficulty easy --profile raw:q-43277 --format json
```

Easy/moderate/hard normal questions use parameterized method-derived five-choice radio banks. Hard is an authored multiply/divide amplitude extraction extension, bounded to two nonunit operations. Every raw source is publicly replayable with `profile="raw:q-ID"`; the unrated raw profiles are routed under authored easy/moderate API levels but retain omitted difficulty keys. Raw profiles are evidence only and ineligible for learning; their missing source attributes and opaque bank interpretations remain visible.

See classification.md, template-extraction.md, plot-extraction.md, source-cases.json, review.md/review.json and validation.json. Validation independently parses displayed mathematics and conclusions, rejects whole-bank collisions, enumerates substantive domains, and sends complete eligible fields through the real memory-only application grader. Omitted correct refs and fields cannot be natively graded as faithful raw records and are honestly excluded from native source denominators. Seven complete banks/35 values, five present correct refs and all seven present solutions are exact fidelity targets.

Normal mathematical identity excludes argument/offset/bank aliases; content identity includes difficulty, actual prompt/solution and complete displayed bank. Source image paths remain unchanged. No learner output needs image resolution or an absolute asset path.
''')
print('Documentation written from validated evidence.')
