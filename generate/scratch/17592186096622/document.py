"""Private extraction evidence, without database or shared-file writes."""
import hashlib,importlib.util,json
from pathlib import Path
H=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('leibniz_document_generator',H.with_suffix('.py'));g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g)
def save(n,v):(H/n).write_text(json.dumps(v,indent=2,ensure_ascii=False,default=str)+'\n')
save('independent-inventory.json',{'database':g.RAW['database'],'basis':2275,'lineage':g.RAW['lineage'],'questions':[{'record':q,'role':'independently authored inventory'} for q in g.KP[':knowledge-point/questions'] if ':question/math-academy-id' not in q]})
recipes={
'q-47994':['c*(x*cos(x)+sin(x))/x^2','c*x*(cos(x)-sin(x))/x^2','c*(x*cos(x)-sin(x))/x^2','c*(cos(x)-x*sin(x))/x^2','c*(x*cos(x)-sin(x))/x'],
'q-11969':['-c*b/(a*x+b)^2','c*b/(a*x+b)^2','c*(b+2*a*x)/(a*x+b)^2','-c*(b+a*x)/(a*x+b)^2','-c*(b+2*a*x)/(a*x+b)^2'],
'q-11944':['(a*ln(x)-(a*x+b))/(x*ln(x)^2)','(a*x*ln(x)-(a*x+b))/ln(x)^2','(a*x*ln(x)-(a*x+b))/(x*ln(x)^2)','(x*ln(x)-(a*x+b))/(x*ln(x)^2)','(a*ln(x)-(a*x+b))/ln(x)^2'],
'q-9909':['c/sin(x)^2','c/(1-cos(x))','-c/sin(x)^2','-c/(1+cos(x))','-c/(1-cos(x))']}
components=[];sections=[]
parser=g.frozen('math_parser')
for t,d in g.TEMPLATES.items():
 q=g.SOURCES[t];p=d['p'];u,v=g.parts(t,p);values,ans=g.answer_and_bank(t,p,'observed');profile='observed-'+t[2:] if d['field']=='radio' else 'fragment';mapping=[]
 for field in q[':question/answer-fields']:
  for a in field[':answer-field/choices']:
   matches=[i for i,z in enumerate(values) if g.eq(parser.scalar(a[':answer/value']),z)];assert len(matches)==1
   index=matches[0];mapping.append({'source_field_id':field[':answer-field/id'],'source_answer_id':a[':answer/id'],'exact_value':a[':answer/value'],'profile':profile,'parameterized_expression':recipes[t][index] if t in recipes else str(ans),'complete_value_reproduced':True,'correct':g.eq(values[index],ans),'captured_correct_reference_present':':answer-field/correct' in field,'recipe_interpretation':'observed expression pattern; misconception intent unresolved' if t in recipes else 'exact required derivative fragment'})
 components.append({'source_id':t,'record':q,'template':t,'difficulty':d['level'],'source_difficulty':q.get(':question/difficulty'),'parameters':p,'numerator':str(u),'denominator':str(v),'du':str(g.s.diff(u,g.X)),'dv':str(g.s.diff(v,g.X)),'bank_profile':profile,'choice_mapping':mapping,'ordered_normal_stages':g.rows(t,p),'ordered_source_solution':q.get(':question/worked-solution'),'authored_completion':':question/worked-solution' not in q})
 sections.append('## '+t+'\n\n1. **Specific observation.** '+q[':question/problem']+'\n\nSource rating '+str(q.get(':question/difficulty','absent'))+'. Numerator `'+str(u)+'`, denominator `'+str(v)+'`, ordered derivatives `'+str(g.s.diff(u,g.X))+'` and `'+str(g.s.diff(v,g.X))+'`. The response is '+d['field']+'. Captured prose and complete banks appear verbatim in source-components.json.\n\n2. **General pattern.** Identify u and v in Leibniz notation, differentiate each, substitute the four ordered operands in (v du/dx−u dv/dx)/v², preserve this family’s factor/collection stages, and fill the printed derivative or derivative fragment.\n\n3. **Components and banks.** Anchor slots `'+json.dumps(p)+'`; complete bank `'+profile+'`.\n\n'+'\n'.join('- `'+m['exact_value']+'` → `'+m['parameterized_expression']+'`.' for m in mapping)+'\n\n4. **Backbone and slots.** Kind `'+d['kind']+'`; exact slot keys `'+', '.join(p)+'`. Slots are substantive coefficients, log base, or a positive integer power as detailed below. Each slot changes the actual function, both derivative definitions, every substituted factor, every dependent intermediate, the requested fragment/factor and all options. Original anchors are retained. No target-name, choice-order or seed variation counts as a new task.\n')
save('source-components.json',components)
(H/'classification.md').write_text('''# Classification at math basis2275

Lineage 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1. The immutable source snapshot contains eleven MA practice questions and zero non-MA questions. The canonical example is context, not practice.

| Source difficulty | Records | Fields | Families | Bank profiles | Plots |
|---|---:|---|---:|---:|---|
| easy |4|3 blank,1 radio|4|1 radio bank|none|
| moderate |4|3 blank,1 radio|4|1 radio bank|none|
| hard |1|1 blank|1|none|none|
| unrated |2|2 radio|2|2 radio banks|none|

All eleven source families and complete banks are supported. The two unrated records q-11944 and q-9909 have no correct reference or worked solution; normal completions label both the solution and assigned moderate/hard rating as authored. Raw evidence keeps every omitted attribute absent. q-340335 uses f(x)/f′ in its first sentence but y/dy in the answer and solution; normal output consistently uses y. Function Unicode application marks, raw sec macros, redundant nested aligned environments and equivalent TeX layout are normalized in served records. Source raw bytes remain unchanged.

The independently authored inventory is separate in independent-inventory.json, with questions record wrappers; its current questions list is empty. source-cases.json accounts for every MA record including the unrated pair. There are no absent difficulty bands: variety at all three levels comes from conservative parameter slots within source-shaped families.\n''')
(H/'template-extraction.md').write_text('''# Four-stage extraction

Evidence source.json is the exact basis2275 wrapper. Topic/lesson snapshots are frozen alongside it. Normal mathematical replay, complete-bank matching, operative stages and raw fidelity are reported separately. The following source-specific families are kept separate because their answer fragments or solution stages differ.

'''+ '\n\n'.join(sections)+'''

## Fixed method, slots and constraints

x remains the independent variable and y the dependent variable because this KP assesses Leibniz notation. u always means the actual displayed numerator and v the actual displayed denominator. Quotient order is v du/dx−u dv/dx with denominator v². Power, trig, exponential and logarithmic derivatives are already present in the lesson/practice. No tangent evaluation, new derivative rule, nested quotient, inverse trig, new answer contract or plot is introduced.

Every integer slot is nonzero with absolute value at most12. q-340336 scales tan x/x² by c while retaining the x⁻³ printed factor and its four-row chain. q-340340 uses c eˣ/(x+b), retaining substitution, unsimplified x+b−1 and final collection. q-340337 scales x/cos x by c and retains the cos⁻² printed factor. q-47994 scales sin x/x by c and preserves its full five-member source profile.

q-11969 varies c x/(a x+b), a,b,c nonzero: its original −x/(9−2x) is an anchor. q-340332 uses c x²/(x²+b), preserving the separate cubic terms before cancellation. q-340341 scales x/ln x by c. q-340343 varies log base b=2..12 and denominator power n=2..4. The source change-of-base equality, quotient substitution, separate logarithmic fractions, common denominator, power factorization, cancellation and final printed factor remain in order. n changes the power-rule coefficient and exponents without adding a rule or operation count. Negative log bases and n=1 are excluded to preserve real domains and the positive-power factorization stage.

q-340335 uses (a−b sin x)/sin x with positive a,b=1..12. Its six quotient rows preserve factoring cos x, cancelling the opposite sine terms, multiplying the remaining constant, splitting reciprocal factors, then csc/cot notation. q-9909 scales (1+cos x)/sin x by a nonzero c; its completed normal chain uses the existing quotient rule followed by the familiar sin²+cos² identity and reciprocal simplification. The source missing rating is assigned hard because this matches the captured hard trig simplification workload; that label is authored. q-11944 uses (a x+b)/ln x, nonzero a,b: its authored moderate completion follows the captured moderate x/ln x chain and clears the inner 1/x denominator.

Within each band these are peer practice families; seed selection has no pedagogical progression. Defaults can select any eligible family. Every family is explicitly selectable for review and replay. Source parameter domains include all positive and negative original values. In q-11944’s observed profile, a=1 makes the fourth source option identical to the correct option; the entire bank is ineligible and is rejected. The authored method profile remains eligible at a=1. Boundary tests preserve and report this collision rather than deleting a bank member. Any invalid or duplicate whole bank rejects the entire sampled instance; no first-valid recipe pool is used.

## Source bank mapping and authored profiles

All four original five-member banks are mapped member by member above and in source-components.json, including all altered coefficients/constants and missing x factors. The mapping formulas reproduce complete mathematical values at original anchors. Historical misconception intent is unresolved where the expression alone does not establish it; learner feedback does not claim an intent. q-11944/q-9909 correct designations are independently derived, not recovered source facts.

An explicitly selectable method profile for radio families is authored as one complete bank: correct quotient rule, addition instead of subtraction, reversed subtraction, unsquared denominator, and quotient of derivatives. Profile selection precedes construction; every wrong value must be wrong as a function on the real source domain, and every pair must be inequivalent. Equivalent isolated point values do not make two derivative functions equivalent. All whole-bank profiles are tested after selection. Normal defaults use the complete observed profile to establish fidelity; authored profiles are distinguishable in metadata and question content IDs.

Blank responses preserve the exact original requested fragment. tan-square and linear-cos expect only a bracket numerator after a supplied factor, log-power expects 1−n ln x before its printed factor, and other blanks expect the entire derivative. 0/1 learner entries are tested as mathematical values without rejection by policy.

## Ordered prose and source replay

Shared sentences are retained: “Let u=… and v=…. Then” followed by both Leibniz derivatives, and “Using the quotient rule, we get” before the ordered equations. Source-specific operative chains are represented by independent literal expected row counts and structural checks in validate.py. The original nine complete solutions are compared mathematically row by row in original order. Full prose, original symbols and erroneous/missing parts remain exact in raw records. The two missing solutions are authored and separately marked. q-340335’s inconsistent dependent-variable label is an explicit repaired source defect.

## Lesson scope

Following :activity/first-step and :step/next in lesson.json gives introduction → polynomial quotients → quotients with other functions → introduction to Leibniz notation → this KP → justification/tangent application. The immediately preceding Leibniz introduction establishes dy/dx notation; the owning topic’s canonical e-3639 sets u,v, computes du/dx,dv/dx, applies quotient rule and collects. This generator stays on that method. The source practice itself contains trig, exponential, log, polynomial and factored fragment contracts at the observed levels. No missing difficulty level needs an invented curriculum branch; both assigned ratings for the two incomplete records are explicitly authored completions.

## Identity and domains

Mathematical identity uses the supplied function, monic square-free polynomial denominator zero-set (fixed trig/log zero-set otherwise) and requested derivative task, excluding seed, choice order and profile. Content IDs include normalized prose, solution, complete bank, level and profile; answer IDs belong to their field. Banks cannot alias one identity. Real domains require denominator nonzero; logarithmic families also require x>0 and log bases positive and unequal1. Source replay retains original parameters, source membership, exact values and correct designation presence separately from normal completion. No source claims depend on a live capture parser or formatter; imports use explicit paths to frozen private copies.
''')
(H/'plot-extraction.md').write_text('''# Plot extraction

Every original prompt, answer bank, worked solution and canonical example is mathematical text. No plot references occur in these eleven source records. Plot rating none: no generated plot or image asset, and no unknown graphic needs to be inferred. The topic/lesson context is retained for instructional scope.\n''')
(H/'README.md').write_text('''# Leibniz quotient generator

New numeric pair for KP17592186096622, basis2275. At assignment start the numeric script/tree did not exist and the manifest had no registered baseline. No existing registered files, shared manifests, queues, database or grader code are edited.

```sh
.venv/bin/python generate/scratch/17592186096622.py --difficulty all --count 2 --seed 110 --format markdown
.venv/bin/python generate/scratch/17592186096622/validate.py
```

The public API is generate(level, seed=0, template=None, parameters=None, profile=None, bank_profile=None), with generate_easy/moderate/hard helpers. Normal output is checked against the frozen canonical formatter at return. profile="raw" is deliberately exact evidence-only output, including absent attributes and historical malformed TeX, and bypasses normal presentation validation. It is restricted to original source parameters and is ineligible for learning. Normal solutions and native learner checks are separate from evidence output.

All eleven source families replay complete banks and ordered mathematical solution stages at their original anchors. All three difficulty levels have independently distinct parameterized tasks. The raw-keyless q-11944/q-9909 have explicitly authored normal keys, solutions and difficulty assignments. q-340335’s f/y inconsistency is corrected in normal content. review.json/review.md put every raw original beside its completed anchor and changed parameters/profile. validate.py independently reads printed givens, definitions, derivative operands, substituted factors, all stages and complete banks; it includes destructive mutation controls that leave the final key unchanged.

The frozen grader SHA256 is 71d435e31aa0cdea66d992aa4d4bd1043cdd871aaffc7a3af9f54e9b0f846dea. engine-input.json contains owned native correct/wrong IDs, separate foreign/malformed submissions, canonical and equivalent blank fragments, and wrong 0/1 values. Any unresolved valid mathematics is reported as an engine limitation rather than silently removed. No database operation or registration is performed.
''')
save('capabilities.json',{'kp_id':g.KP_ID,'basis':2275,'version':g.VERSION,'supported_levels':list(g.SUPPORTED_LEVELS),'templates':g.TEMPLATES,'plots':'none','source_records':11,'authored_inventory':0})
print('Wrote private extraction evidence.')
