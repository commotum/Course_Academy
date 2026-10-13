"""Retain per-source extraction evidence and explicit bounded policies."""
import json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE));import validate as v
g=v.g;s=json.loads((HERE/'source.json').read_text());components=[]
for t,q in g.sources().items():
 r=g.generate(g.DATA[t][0],0,t,{'m':1});f=q[':question/answer-fields'][0];expr,F,answer,factor,inner,h,H,lo,hi=g.math_data(t,1)
 components.append({'source_question':t,'source_entity':q[':db/id'],'observed_difficulty':q.get(':question/difficulty'),'generated_difficulty':g.DATA[t][0],'field_key':f[':answer-field/key'],'field_type':f[':answer-field/type'][':db/ident'],'original_problem':q[':question/problem'],'original_solution':q.get(':question/worked-solution'),'integrand':str(expr),'substitution':str(inner),'derivative':str(v.sp.diff(inner,v.p.x)),'outer_to_derivative_ratio':str(factor),'primitive':str(F),'bounds':None if lo is None else [str(lo),str(hi)],'domain':'Connected real interval excluding trig poles; reciprocal substitution additionally x != 0. Definite sec*tan u-range [0,pi/3], cosine/sine entire.','choice_bank_profile':t if len(f[':answer-field/choices'])>1 else None,'choices':[{'source_field':str(f[':answer-field/id']),'source_answer':str(a[':answer/id']),'original_value':a[':answer/value'],'original_exact_expression':str(v.p.scalar(a[':answer/value']).subs(v.p.C,0)),'recipe':'m * ('+str(v.p.scalar(a[':answer/value']).subs(v.p.C,0))+')'+(' + arbitrary C' if lo is None else ''),'reproduces_complete_source_value_at_m1':True,'correct':i==[a[':answer/id'] for a in r['question'][':question/answer-fields'][0][':answer-field/choices']].index(r['question'][':question/answer-fields'][0][':answer-field/correct'][1]),'interpretation':'Observed expression transported as a whole; misconception not inferred.'} for i,a in enumerate(f[':answer-field/choices'])],'parameter_features_observed':{'m':1,'exact_coefficients':True,'zero_answers':answer==0,'nonzero_lower_bound':lo not in (None,0),'reciprocal_substitution':t=='q-3038'},'proposed_bounds':{'m':[2,12],'positive_integer_only':True},'layout':'Source prompt shape and field key retained; source solutions exact at replay, generated solutions use same substitution/integral/primitive/back-substitution or bounds sequence.','source_issues':['Missing difficulty, marker, and solution; local moderate label and exact derived marker/solution only in generated copies.'] if t=='q-13461' else ['Redundant nested aligned environment; variant uses one balanced environment.'] if t=='q-3038' else []})
(HERE/'template-components.json').write_text(json.dumps(components,indent=2)+'\n')
(HERE/'classification.md').write_text('''# Classification

Database math, lineage 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1, captured basis 1941. All eight source practice questions and canonical e-466 read together, including complete fields, banks, solutions and generator reference. No registered generator or supplied .generated file. Native inventory requires three moderate questions; hard has its rolling reserve already.

| Difficulty | Field contracts | Markdown/value templates | Choice profiles | Plot rating |
| --- | --- | --- | --- | --- |
| Moderate | radio selection | 2 rated; 1 locally completed legacy template | 3 complete banks | none |
| Hard | radio selection; blank field-1 | 5 | 3 complete radio banks; 2 blanks with no profile | none |
| Easy | no observed contract | 0 supported | 0 | none |

Each source has its own render and solution contract. q-13474 uses x^3 and sec squared; q-13464 uses x^2 and csc squared. Unrated q-13461 is a basic x*sin(x^2) substitution, conservatively classified moderate locally alongside those observed indefinite substitutions. Its missing marker follows differentiation; a worked solution is authored for generated copies. The source record remains unchanged and unavailable as unrated practice.

Hard contracts distinguish definite cosine and sine radio prompts, reciprocal sec-squared substitution, definite sec*tan blank, and definite cosine blank with a nonzero lower bound. Definite endpoint answers can be zero but their integrands still differ. Canonical e-466 provides shifted x^3 sec-squared evidence; it is not a practice template and adds no inventory.

Easy is unsupported by this bounded package, not proved impossible for the KP. No easy source bank/solution exists. New source evidence reopens classification; its five-question reserve is not called filled.
''')
(HERE/'template-extraction.md').write_text('''# Template extraction

Per-question particulars and every original choice appear in template-components.json with source IDs, exact expressions, field ownership, bounds, substitutions, bank profile, original Markdown and solution. All 32 source values and 24 distractors are accounted for without pooling banks. Six radio source profiles are distinct; blanks have none.

Shared mathematical pattern: integrate A*x^(n-1)*h(b*x^n) using the displayed inner expression as u, or the reciprocal sec-squared variant using u=1/x. The required response is one primitive plus arbitrary C or one exact definite value. This exercises recognizing the derivative factor, retaining its coefficient, and transforming bounds where present.

Fixed components: inner substitution, trig function/product, original bounds, source choice count, field type/key, prompt shape, solution sequence and complete source-bank profile. Variable component: positive outer amplitude multiplier m. Compute the correct primitive from the derivative ratio first; then transport every observed bank expression by m. All literal constants in distractors scale too. m=1 is an exact replay; m=2..12 is a deliberately narrow sampling policy. Arbitrary C remains arbitrary and is not treated as a fixed value.

Every recipe is m times the complete exact source expression listed in the component ledger. At m=1 it reproduces the whole source value. The source expressions are retained as observed patterns; no learner misconception is inferred. A complete bank is selected by source template before any answers are rendered. No choice mixing or source literals left unscaled.

Domains: real connected intervals excluding sec/csc/cot/tan poles and x=0 for reciprocal u. The definite sec*tan interval maps to [0,pi/3], which has no poles. Sine and cosine definite intervals are regular and monotone under positive x-squared substitutions. Positive nonzero m preserves all domain restrictions and bank equivalence relationships.

Source issues: q-13461 has no difficulty, correct marker or worked solution and malformed integral spacing; generated variants use a moderate label, mathematically derived marker, a fixed solution and repaired spacing. Seven supplied source solutions are retained exactly at replay. q-3038 has redundant nested aligned markup; variants use one balanced environment. No source facts are repaired in the database.

Fidelity is separate from correctness: all eight exact source prompts, all source fields/keys, all 32 bank values and seven provided solutions replay exactly. Variant LaTeX is normalized by SymPy and intermediate rows are shortened to substitution, transformed integral, primitive, bound evaluation/back-substitution and final value. This notation/layout normalization is explicit; original prose and evidence remain in the ledger.
''')
(HERE/'plot-extraction.md').write_text('''# Plot extraction and generation

All eight practice sources and canonical e-466 are textual mathematics; no image, diagram, plot or asset reference occurs in the captured prompts, answer values or worked solutions. No varying or reusable graphical asset is required. Every supported template has plot rating **none**. Stages 5 and 7 need no renderer or published asset; LaTeX mathematics is not a plot.
''')
(HERE/'README.md').write_text('''# Trigonometric substitution generator

Run from repository root:

```sh
.venv/bin/python generate/scratch/17592186068917.py --difficulty moderate --count 3 --seed 1941 --format json
.venv/bin/python generate/scratch/17592186068917/validate.py
.venv/bin/python generate/scratch/17592186068917/replenish.py
```

The package supports moderate and hard via a bounded positive amplitude policy. Easy remains unsupported. Source evidence, per-choice extraction, exact replay, actual grading, review and retained database requests are local to this KP. The replenisher rechecks inventory under api.lock, preserves source and history, uses application/ca-engine attribution and a basis guard, and verifies exact commit readback before reporting success. Repeated seeds never count as new content. Exhaustion of the finite domain must leave the shortage explicit.
''')
print('Wrote eight source component ledgers and workflow evidence')
