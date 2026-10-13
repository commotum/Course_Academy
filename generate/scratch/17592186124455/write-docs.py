import importlib.util,json,hashlib,re
from pathlib import Path
P=Path(__file__).parent
sp=importlib.util.spec_from_file_location('g',P.with_suffix('.py'));g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g)
(P/'classification.md').write_text('''# Classification

Immutable source: math basis1356, lineage01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1. Eleven practice sources: ten moderate, one unrated(q36391). No observed easy/hard labels. Eleven distinct Markdown/value layouts, twelve complete EDB radio banks, sixty displayed options. q65204 has duplicate selection-key fields, each with five choices; the original MA1940 JSON widget has a single multiple-choice demand with five choices. Both raw fields are preserved, while the completed profile retains the authoritative later field. There are no blank fields or supplied answer fragments.

All practice templates have plot rating **none**. The canonical example has an explanatory diagram after its worked answer; it is not an assessment input or a required element of any practice template. Neither a reusable graph nor a renderer is needed here.

## Ordered curriculum and scope

Following activity/first-step and step/next gives: Introduction17592186125292 → Tangent Line to a Level Curve17592186125464 → tangent-line KP17592186125293 → Tangent Vector tutorial17592186125294 → assigned tangent-vector KP17592186125295 → perpendicular-vector-point sibling17592186125296. The tutorial proves that(f_y,-f_x) is orthogonal to(f_x,f_y). This task uses that formula at the specified point. Tangent-line equations, finding points with prescribed vector orientation, normal-vector questions, normalization, and parametrization are outside this generator.

Easy is an authored canonical-example extension with a quadratic, one mixed term and one linear y term. Moderate is anchored in q130192/q36391's mixed polynomial derivatives, with nonzero signed coordinates. Hard is an authored workload choice anchored in q37516: the same two partial derivatives and point substitution, with logarithmic and reciprocal terms evaluated at e or e² and nonzero signed x. Hard's extra arithmetic is collecting both nonzero evaluated derivative sums; it does not introduce a new method. Source log/trig examples remain observed moderate evidence, regardless of this separate authored design choice. Variants within a level have identical operations and do not constitute a progression.

## Arithmetic and banks

All authored coefficients are nonzero primitive integer triples of magnitude1..4; x0 is±1 or±2. Easy/moderate y0 is±1 or±2; hard y0 is e or e². Reduced rational numerator magnitude≤32, denominator≤4 and actual numeric magnitude≤32 apply to parameters, both evaluated partial derivatives and curve level. These guards also apply to explicit calls. Source replay allows its original constants/number forms; evaluated source quantities obey the same finite arithmetic ceiling. Samplers select the fixed complete five-operation profile before parameters, then reject the whole instance on zero vectors, tangent ambiguity or any proportional choice collision.

The finite primitive coefficient domain has440 triples. After quotienting common sign, potential mathematical tasks before bank/arithmetic rejection are3520 per easy/moderate and1760 hard. These are upper bounds, not claims of fully eligible catalogs. validation.json reports actual distinct eligible sampled tasks. Variable notation, seed, option order and profiles do not inflate mathematical-task counts.

Historical incorrect-option intent is unresolved. Their fixed full components and mathematically derived correct components are explicit evidence profiles. Raw and completed historical records always carry evidence_only=true and eligible_for_learning=false. The authored default bank is separately specified from actual displayed operations.
''')
text='''# Template extraction

## 1. Describe each original

Each row below is a complete individual record. source.json retains all EDB attribute presence, identities, original banks, missing refs and errors. source-templates.json retains full sentence/row masks, coordinate factors and numeric spelling components; source-cases.json records original parameters. Original MA widgets for q36391/q65204 are saved in original-widgets.json.

'''
for qid,q in g.QUESTIONS.items():
 F=g.expr(qid);a,b=map(g.sym,g.SOURCE_SPEC[qid][1:]);grad=[z.subs({g.x:a,g.y:b}) for z in (g.s.diff(F,g.x),g.s.diff(F,g.y))]
 text+='### '+qid+'\n\n'+q[':question/problem']+'\n\n'
 text+='Observed difficulty: '+('moderate' if ':question/difficulty' in q else 'unrated')+'. Symbolic implicit expression: `'+str(F)+'`. Point: `('+str(a)+','+str(b)+')`. Evaluated derivative pair: `'+str(grad)+'`.\n\n'
 for fi,f in enumerate(q[':question/answer-fields']):
  text+=f"Field{fi}: key `{f[':answer-field/key']}`; radio; source correct-ref present: {':answer-field/correct' in f}.\n\n| Choice UUID | Full observed component | Correct designation | Mathematical tangent condition | Recipe interpretation |\n|---|---|---|---|---|\n"
  for ans in f[':answer-field/choices']:
   valid=g.dot(tuple(grad),g.pair(ans[':answer/value']))==0;mark=ans[':answer/id']==f.get(':answer-field/correct',{}).get(':answer/id')
   text+='| '+ans[':answer/id']+' | `'+ans[':answer/value']+'` | '+('marked' if mark else 'unmarked')+' | '+str(valid)+' | '+('computed f_y,-f_x with captured scalar spelling' if valid else 'fixed opaque complete observed expression; no inferred error operation')+' |\n'
 text+='\nFull worked-solution string present: '+str(':question/worked-solution' in q)+'. Ordered sentence and mathematical masks retain rearrangement, level definition, formula, formal partial-operator inputs, symbolic component derivatives, original coordinate-factor evaluation row, final collected vector and concluding sentence. q36391 has no observed solution and receives a separately authored completion.\n\n'
text+='''## 2. Shared pattern

Write the implicit curve as f(x,y)=k; evaluate f_y and-f_x at the specified point; select a nonzero vector tangent to the actual curve. Validity means ∇F(point)·v=0, so vectors proportional to the displayed formula are also mathematically correct. The bank audit checks all options by that criterion, including every source correct designation that exists. No source bank has a second tangent direction. q130201's specified point fails membership in the source curve, an independent prompt error.

## 3. Components and profiles

The per-source tables above map every field and choice. Twelve observed complete banks stay separate. Correct components are regenerated from actual symbolic derivatives; source scalar spelling masks preserve original notation at the original parameters. Incorrect opaque components remain explicit fixed expressions under the public raw/completed profile. They are not numerical fits and are not promoted as recovered historical error recipes. Their changed-point banks may have new mathematical ambiguities; the evidence record reports this limitation and stays ineligible for learning.

Authored method-bank has exactly five fixed operations: (f_y,-f_x); gradient (f_x,f_y); omit the rotation minus (f_y,f_x); reverse derivative roles with the same sign pattern(-f_x,f_y); omit the first family-defining summand before differentiation. All operations use actual displayed F and point. This bank is selected as a whole before sampling, and collisions reject the whole instance. No unused pool replacements or unrelated random perturbations occur.

## 4. Reusable masks and restrictions

Source masks preserve complete raw prose and ordered blocks, including omission of redundant numerical rows. The level constant, point tuple, every complete numeric coordinate factor and computed vector component are slots. Symbolic operator inputs and derivatives retain each source's own function structure. Authored templates derive F, its level, both partials, substituted-coordinate masks, individual evaluated coefficients and the final vector from exact SymPy data. Changed coordinates must remain within finite familiar forms and the actual arithmetic ceiling; logarithms require y>0. Raw malformed presentation is never silently called learner-ready.

## Source errors, repairs and limitations

- q36391: absent difficulty, worked solution and correct ref. Original MA1940 widget confirms one five-choice radio demand. Independent F_x=6,F_y=2 uniquely supports2i-6j. Completion adds that inferred ref, authored moderate label and full method solution. These are not matched observed attributes.
- q65204: two EDB fields share selection key; original MA1940 widget has one five-choice demand. Later field has correct ref and the same complete mathematical bank. Completion removes the earlier legacy field; both raw banks remain exact evidence. Decoded answer strings have only single-backslash runs; JSON/tool escaping is not a presentation anomaly. No backslash repair is counted; source-format-audit.json records decoded run lengths.
- q72463: rearrangement gives f=1 but level prose says f=0. Raw solution remains exact; completion corrects only the stated level.
- q130201: point(-1,-1) gives xy+x²+y³=1, while source constant is3. Completion changes the curve and its level/rearrangement constant to1, retaining the derivative/vector method. Correct vector values alone do not establish raw prompt correctness.

Raw exact denominators:11 prompts/key-presence layouts;12 banks/60 values;10 existing correct designations;10 full solution strings. Completions are counted separately. Authored easy/hard labels are design claims. Every historical profile, even repaired, remains evidence-only because distractor intent was not recovered.
'''
(P/'template-extraction.md').write_text(text)
(P/'README.md').write_text('''# Finding a Tangent Vector to a Plane Curve

Generator: `../17592186124455.py`. Scope: implicit curve → partial derivatives → tangent vector at specified point. Local review records only; no EDB writes.

```sh
.venv/bin/python generate/scratch/17592186124455/validate.py
.venv/bin/python generate/scratch/17592186124455.py --difficulty all --seed0 --count2 --format markdown
.venv/bin/python generate/scratch/17592186124455.py --profile raw:q-36391 --count1
.venv/bin/python generate/scratch/17592186124455.py --profile completed:q-65204 --count1
```

Use spaced CLI arguments (`--seed 0`, `--count 2`). API: generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None), and generate_easy/moderate/hard. Observed profiles replay using levelmoderate; q36391's raw difficulty stays absent. The default generated banks are authored, complete, deterministic and independently checked from their display. Raw/completed historical banks stay evidence-only. Source-bank mathematical correctness, raw fidelity, repairs, authored scope and actual native grading are distinct results in validation.json. No blanks exist, so free-entry equivalence checks are inapplicable.

The source/topic/lesson snapshots remain immutable at basis1356. Full extraction, original-widget evidence, review and test artifacts live in this folder. Missing easy/hard labels are authored, and historical wrong-choice intention is unresolved. See classification.md and template-extraction.md for exact restrictions and repairs. No plot generator is required by practice templates.
'''.replace('--seed0','--seed 0').replace('--count2','--count 2').replace('--count1','--count 1'))
