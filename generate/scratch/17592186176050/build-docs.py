import importlib.util,json,sys
from pathlib import Path
import sympy as sp
sys.dont_write_bytecode=True
D=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('g',D.with_suffix('.py'));g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
def put(name,s): (D/name).write_text(s+'\n')
put('classification.md',r'''# Classification

Snapshot: database `math`, basis **1356**, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. `source.json` is an unchanged copy of the frozen wrapper.

Seven practice questions; all have one `selection` radio field with five math choices. Five have observed moderate labels. Two are unrated and omit both worked solutions and correct refs. No source question has a plot; plot rating **none**. The lesson illustrations teach the period but do not occur in these practice templates, so no renderer or plot extraction is required.

| Observed difficulty | Markdown/value template | IDs | Bank profiles |
|---|---|---|---|
| Unrated | spaced LaTeX affine, no solution | q-29382 | source_q-29382 |
| Unrated | spaced LaTeX direct, no solution | q-66218 | source_q-66218 |
| Moderate | Unicode affine with product-before-collection chain | q-103307 | source_q-103307 |
| Moderate | Unicode fractional scaling with integral product | q-103312 | source_q-103312 |
| Moderate | Unicode direct radical substitution | q-66594, q-71002 | two distinct complete banks |
| Moderate | Unicode additive substitution | q-70998 | source_q-70998 |

Six observed Markdown/value templates, seven complete bank profiles. Direct radical questions share their prose/chain while keeping their two banks distinct. The two unrated sources receive authored easy/direct and moderate/affine assignments only in case metadata. Public raw replay omits difficulty, solution and correct designation exactly as captured; these omissions are never counted as matched designations or solutions.

Easy and hard have no observed difficulty labels. Easy is an authored completion of the canonical direct substitution and unrated direct question. Hard is authored rational affine arithmetic, anchored to moderate's scaling and offset operations. These are design claims, not recovered difficulty assignments.
''')
rows=[r'''# Template extraction

## Stage 1: original descriptions

All questions give the tangent of an unspecified real angle and request a tangent at that same angle plus an integer multiple of π. There is no negative coefficient on x inside tangent and no half-period shift. Thus the assessed trigonometric step is precisely periodicity. The domain is any x at which the supplied tangent is defined; integer shifts preserve definedness. Correct-answer refs are absent in two raw records.
''']
questions=g.SOURCE['record'][':knowledge-point/questions']
for q in questions:
 sid=q[':question/math-academy-id'];spec=g.SPECS[sid]
 rows+=['### '+sid,'',q[':question/problem'],'','Parameters: `'+json.dumps(spec['p'])+'`. Field: `selection`, radio, five complete scalar answers.','',q.get(':question/worked-solution','**No worked solution in the snapshot.**'), '']
rows+=[r'''## Stage 2: generalized family

Given tan(x)=v, use tan(x+nπ)=tan(x)=v and evaluate a·v+b. Direct uses a=1,b=0; additive uses a=1,b≠0; scaling uses nonunit a,b=0; affine uses nonunit a,b≠0. The distinct source shared sentences, comma placements, function token style and arithmetic stages are retained in explicit replay. Normal authored output changes the source's Unicode `tan⁡` token into standard `	an ` only. It retains the same formal identity, substituted-integer identity, value substitution and family-specific final arithmetic chain. No chosen distractor changes the solution.

## Stage 3: component and complete-bank mapping

The following exact operation formulas reproduce every displayed scalar. They are explicit parameterizations of observed forms, not claims to recover the original error-generation code. In particular, a singleton constant, π coefficient or squared radical can fit several explanations. Every observed profile is evidence-only; the normal bank is separately authored. `anum` and `aden` are the reduced numerator and denominator of a. Each row belongs to the complete five-entry source bank; no pooled option picking occurs.
''']
for q in questions:
 sid=q[':question/math-academy-id'];spec=g.SPECS[sid];field=q[':question/answer-fields'][0];p=g.cleanparams(spec['p']);vs=g.values(p,spec['template'],'source_'+sid)
 rows+=['### '+sid,'','| Original choice | Parameterized operation | Match | Source designation |','|---|---|---|---|']
 for opt,op,val in zip(field[':answer-field/choices'],spec['ops'],vs):
  designation='correct' if field.get(':answer-field/correct',{}).get(':answer/id')==opt[':answer/id'] else ('wrong' if ':answer-field/correct' in field else 'absent')
  rows.append('| `'+opt[':answer/value']+'` | `'+sp.sstr(op)+'` | exact mathematical value | '+designation+' |')
 rows+=['', 'The uniquely correct derived value is `'+g.tex(p['a']*p['v']+p['b'])+'`. '+('That designation is independently inferred for completed practice; raw replay omits it.' if ':answer-field/correct' not in field else 'The captured designation agrees with the derivation.'),'']
rows+=[r'''## Stage 4: reusable templates and constraints

All mathematical slots are complete components: given v; shift x±|n|π; integer multiplier `(n)·π` when negative; entire scalar coefficient a; entire offset b; product a·v and collected answer. No blind replacement of short numerals or variable letters is used. Signed outside coefficients are grouped. Substitution products retain visible parentheses, so adjacent numbers cannot merge. The final product-before-collection row is preserved for affine questions. Direct and additive sources use their original “Therefore, if …” and “Finally, then” wording; scale/affine use their original “Since … Therefore” wording.

Normal banks are chosen whole, before parameters, with five required expressions:

| Workload | Complete authored bank |
|---|---|
| Direct | v; 1/v; -v; -1/v; v+nπ |
| Additive | v+b; v; b; -v+b; v+nπ+b |
| Scaling | av; v; v/a; -av; a(v+nπ) |
| Affine | av+b; av; av-b; a+bv; a(v+nπ)+b |

The operations arise from the printed method: reciprocating tangent as cotangent, applying an erroneous sign change, adding the angle shift outside tangent, omitting the outside scaling/offset, dividing rather than multiplying, reversing the offset sign, or exchanging coefficient and offset roles. No learner-facing distractor diagnosis is invented. These are authored error operations, not inferred source intent.

A collision, a second mathematically correct option, an invalid scalar or a missing required option rejects the entire sampled instance. Explicit invalid parameters raise an error and are never resampled. Stable IDs use the actual prompt, fixed solution, complete displayed bank, difficulty and source key-presence state; option order and seed do not affect identity. Mathematical fingerprints use the given value and requested affine operation plus difficulty. Integer shift magnitude, function-token style and bank profile are excluded as incidental to the mathematical task.

## Scope and all three levels

Lesson order is reconstructed from activity first-step and step/next: introduction → describing tangent → periodicity tutorial → **this KP** → oddness tutorial → oddness KP. The sole key prerequisite is **Periodic Functions** (topic 17592186049353 / MA 2148). Therefore negative x, oddness, quarter-period identities, evaluating tangent at familiar angles, solving trig equations and tangent addition formulas are excluded.

Easy: integer v with 2≤|v|≤16, a=1,b=0. Exactly one integer-period substitution, anchored to canonical e-11005 and unrated q-66218. The given integer bound matches observed integer 16 elsewhere in this same KP. Moderate uses unordered equivalent-workload families observed here: familiar roots ±√k (k=2,3,5,6,7); integer additive v (2≤|v|≤9), 1≤|b|≤6; fractional scaling (denominator 2–4, numerator magnitude ≤3) of an integer value |v|≤16, with an integral product; affine integer coefficient 2≤|a|≤12, reduced given numerator magnitude ≤8 and denominator ≤4, integral |av|≤24, nonzero integer offset |b|≤6. The normalized affine legacy name is a presentation alias, not an extra substantive family.

Hard: authored noninteger rational a and v, reduced denominators 2–4, reduced numerator magnitude ≤6, noninteger av, integer 1≤|b|≤5. Every item requires the same period substitution, rational multiplication and rational offset collection. It adds arithmetic demand already represented by moderate scaling/offsets, without adding a trigonometric property. Inputs that cancel to an integer product or omit the offset are rejected. All levels use nonzero integer n of magnitude ≤12. These domains are finite; integer-shift, spelling and profile aliases do not inflate task counts. `variety.json` enumerates substantive parameter tasks in the supported domains before counting seeds.

## Missing-data fidelity and independent evidence

The owning MA widget capture at `/home/jake/Developer/MA/DATA/Lessons/3558/Source/3558.json` confirms q-29382 and q-66218 are ordinary five-choice widgets without captured solutions or correctness. q-29382's last two choices are ordered differently there; source matching treats radio order as incidental. There is no evidence of a mathematical source error. Missing refs and solutions are retained raw, with independently derived values 3 and 4 used only in explicitly authored completion. IDs are new field-owned UUIDs for review records; captured DB/MA identifiers remain in raw `source.json` and case provenance. No fake MA identifier is minted. Presence parity is enforced for difficulty, worked solution, answer fields and correct refs.

Plots: none. Steps 5/7 need no renderer; the tutorial graph is not copied into practice questions. Work stops before registration or database preparation.
''']
put('template-extraction.md','\n'.join(rows))
put('README.md',r'''# Tangent periodicity scratch generator

Frozen math basis 1356; no database writes. Generator: `../17592186176050.py`.

```sh
.venv/bin/python generate/scratch/17592186176050/validate.py
.venv/bin/python generate/scratch/17592186176050.py --difficulty all --seed 19 --count 2 --format json
.venv/bin/python generate/scratch/17592186176050.py --difficulty moderate --profile source_q-103307 --count 1
```

Public API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` and `generate_easy`, `generate_moderate`, `generate_hard`. Parameters require exactly `v,a,b,n`; scalars may be exact SymPy-compatible strings. Only radio fields are supported. Explicit source profiles are parameterized evidence-only replays and preserve omitted source attributes. Normal output is completed, with separately labeled authored banks and levels.

`validate.py` reads actual prompt/answer/solution strings through an independent scalar and tangent-period parser, compares every source bank and source attribute presence, checks every displayed equality and required arithmetic stage, exercises rejected mutations, and runs the real native grader. `validation.json` separates fidelity, authored sampling and native grading. Raw originals missing correct refs remain ungraded evidence; no missing designation is reported as matched. `review.md`/`review.json` include every source bank and at least two normal variants per family and difficulty. `classification.md`, `template-extraction.md` and `variety.json` document scope and finite task counts.
''')
