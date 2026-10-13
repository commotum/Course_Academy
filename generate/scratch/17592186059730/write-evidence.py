import hashlib
import importlib.util
import json
from pathlib import Path
H=Path(__file__).parent
spec=importlib.util.spec_from_file_location('g',H.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
cases=json.loads((H/'source-cases.json').read_text()); replay=json.loads((H/'source-replay.json').read_text()); review=json.loads((H/'review.json').read_text())
# Preserve the captured lesson widget as additional read-only evidence.
p=Path('/home/jake/Developer/MA/DATA/Lessons/177/Source/177.json'); lesson=json.loads(p.read_text()); widget=[]
def walk(v):
 if isinstance(v,dict):
  if v.get('question_id')=='1355': widget.append(v)
  for w in v.values():walk(w)
 elif isinstance(v,list):
  for w in v:walk(w)
walk(lesson)
(H/'authoritative-1355-widget.json').write_text(json.dumps({'source_path':str(p),'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'records':widget},indent=2)+'\n')
(H/'classification.md').write_text('''# Classification at immutable math basis 1356

Lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`; raw capture is `source.json`. Six rated easy practice questions and one unrated practice original are all retained. The decimal canonical example is context, not an eighth practice question.

| Level | Original practice count | Templates | Fields | Plots |
|---|---:|---|---|---|
| Easy | 6 rated + 1 unrated assigned authored easy | let2_radio; if3_arrow_radio; if3_radio; dependent3_blank; if2_blank | One five-option radio or one scalar blank | none |
| Moderate | 0 | components3_radio; components3_blank, authored | Same radio/blank layouts | none |
| Hard | 0 | components3_radio; components3_blank, authored | Same radio/blank layouts | none |

`let2_radio` has two observed complete banks (q-1340, q-101406). `if2_blank` has q-317910 and q-317911 with shared prose and differing names/numbers. Other templates preserve the source prompt/solution distinctions rather than merging their layouts. Missing levels are explicit design claims, not inferred original labels.

The ordered activity route is obtained from `activity/first-step` and `step/next`: 17592186060617 Introduction → 17592186060618 assigned general formula → 17592186060620 solving an unknown from perpendicular vectors → 17592186060619 intuition behind the formula. Collection order would place intuition incorrectly. The prerequisite is Three-Dimensional Vectors in Component Form (topic 1166). The sibling requires solving an unknown with a zero dot product; it is excluded. Angle/magnitude and downstream angle, plane, integration, matrix, and N-dimensional skills are excluded.

The introduction explicitly teaches summing corresponding products for two and three components. The assigned canonical example includes a negative decimal and zero: <0,-0.4,11>·<2,5,2>. Moderate therefore uses exactly three nonzero integer products of mixed sign, with component magnitudes 2..12. Hard uses exactly three products of mixed sign, with at least two nonintegral contributions, using exact tenths and component magnitudes 1..6. The difficulty difference is only numerical arithmetic workload; neither introduces unknowns, angles, perpendicularity, vectors beyond three components, or extra formulas. Each level's two layouts have the same numerical demand and no internal progression. Guards also apply to explicit parameters.

Source anomalies: q-1355 lacks a level, correct reference, and solution. The captured owning lesson's widget independently confirms all five answer values but has no key or solution; exact arithmetic supplies -40. Assigning easy and authoring the common four-stage solution are labeled repairs, not matched evidence. q-168035 depends on part 1, omitted from its prompt capture; vectors <0,-3,2> and <0,4,3> are explicitly present in its source worked solution. Prepending those given vectors makes the prompt standalone while retaining the captured raw text and full solution. Its explicit observed profile retains “From part 1”; normal variants use “For these vectors.”

Plot extraction is unnecessary: no source asset occurs in this KP's captured prompts, choices, or solutions. The dependent source's earlier context is supplied as components, so no graph-reading or drawing workload is introduced.
''')
text='''# Template extraction

## 1. Describe each source before generalizing

'''
for case in cases:
 q=g.SOURCES[case['source_id']];f=q[':question/answer-fields'][0]
 text+=f"### {case['source_id']} — {case['template']} / {case['bank_profile']}\n\n"
 text+='Original prompt:\n\n'+q[':question/problem']+'\n\n'
 text+='Components: '+json.dumps(case['parameters'])+'. One '+f[':answer-field/type'][':db/ident'].split('/')[-1]+' field. Original choices: '+', '.join(a[':answer/value'] for a in f[':answer-field/choices'])+'. '
 text+='Original correct: '+f.get(':answer-field/correct',{}).get(':answer/value','absent; inferred -40')+'.\n\n'
 text+='Original full worked solution:\n\n'+q.get(':question/worked-solution','[Absent in captured source; authored formal → substitution → individually evaluated products → final scalar.]')+'\n\n'
text+='''## 2. Shared mathematical pattern and response

Given complete component vectors, compute the scalar sum of products of corresponding components. The observed radio field has five delimiter-free scalar math choices; the blank contains a matching `{{field-1}}` placeholder and one exact scalar value. All source numerical products are integers. The canonical decimal example anchors exact noninteger authored arithmetic.

## 3. Map every source component and complete bank

Let `a_i,b_i` be corresponding input components, `t_i=a_i*b_i`, and `c=sum(t_i)`. The following tables account for every source answer. Every scalar reconstruction is an operation on actual inputs, not an answer lookup or unrelated perturbation. Original incorrect-choice intent is underdetermined, particularly compound expressions; these reconstructions are replay-only profiles and are not promoted to default learner banks. An exact reconstruction does not establish the original intended mistake.

'''
for case,r in zip(cases,replay):
 f=g.SOURCES[case['source_id']][':question/answer-fields'][0]; recipes=r['generation']['recipes'];text+='### '+case['source_id']+'\n\n| Original value | Reconstructed operation | Correct status |\n|---|---|---|\n'
 for a in f[':answer-field/choices']:
  v=a[':answer/value'];text+=f"| {v} | {recipes[v]} | {'inferred correct' if case['source_id']=='q-1355' and v=='-40' else 'correct' if f.get(':answer-field/correct',{}).get(':answer/value')==v else 'incorrect'} |\n"
 text+='\n'
text+='''Explicit profile formulas, in the same original bank order:

- observed_1340: `[b0*b1, 2*c, -t0+t1, c, a0*a1+b0*b1]` → `[63,-6,39,-3,57]`.
- observed_101406: `[t1-t0, c, 2*t0, t1, -t0]` → `[-2,6,8,2,-4]`.
- observed_1341: `[t0, t0+t2, t0-2*t1, t0-t2, c]` → `[11,7,27,15,-1]`.
- observed_1355: `[t2-t0, c, -t0, -c, t0-t2]` → `[-20,-40,10,40,20]`.
- observed blank profiles: `[c]` → `[-6]`, `[14]`, `[12]` respectively.

## 4. Reusable templates and constraints

Fixed prose and stage masks preserve each original's exact words, punctuation, arrow notation, component labels, row ordering, and evaluated-product signs. Slots are entire vectors, factors, names, sums, and final scalars. Normal output computes `c`, selects a complete eligible bank, computes every required option, and rejects the whole instance on equality. Radio options are shuffled deterministically only after field-owned answer identities and correct ref are recorded. A single worked solution is independent of any selected wrong option.

The four arithmetic stages are (1) formal corresponding-component formula, (2) actual ordered multiplication of signed grouped factors, (3) individually evaluated products in source addition/subtraction notation, (4) final scalar. The dependent template splits the formal block from the last three stages and includes its common explanatory paragraph. Arrow radio retains parenthesized negative evaluated terms. Blank solutions retain the omitted colon and final period. Source q-1355 has no worked solution, so the shared four-stage reconstruction is explicitly authored.

The authored default radio bank is complete: `[c, sum(a)+sum(b), sum(a)*sum(b), sum(t[1:]), sum(t[:-1])]`. These represent adding components in place of products, including all cross-coordinate products by multiplying the component sums, omitting the first corresponding product, and omitting the last corresponding product. All four are tied to the assessed operation. No random numerical perturbation, source-intent diagnosis, or mixed first-valid recipe pool is used. Exact rational duplicate/correct collisions reject the whole bank. Authored blanks use `[c]`.

Easy components are integral in [-12,12], for observed two/three-component layouts. Moderate components have absolute magnitude 2..12, exactly three nonzero integer products, at least one positive and one negative product. Hard components are nonzero exact tenths of absolute magnitude 1..6, exactly three products, at least two noninteger products, and mixed product signs. Within each level every sampled question has the same method and documented workload. The finite domains contain hundreds of directly checked distinct mathematical tasks at every level; only semantic component-pair tasks count toward variety. Normal radio banks are authored extensions while explicit `observed_*` profiles preserve all original banks.

Mathematical fingerprints sort corresponding factor pairs, quotienting multiplication-factor order and simultaneous coordinate permutations; labels, layouts, profiles, and option order do not inflate task variety. Full content identities hash generator version, difficulty, actual prompt, fixed solution, field kind, and complete sorted displayed bank. Changing a seed or unused profile spelling at fixed content does not change the identity. Full displayed changes produce different identities.

Source fidelity is separate from independent arithmetic and native grading: 7/7 complete banks and 23/23 displayed values match; 16/16 original distractors match; 6/6 present original correct designations match, with one separately inferred; 6/6 present full solution strings match, with one separately authored; 6/7 raw prompts match with one explicitly repaired standalone prompt. All seven practice records remain in `source-cases.json`. No source ambiguity or mathematical error remains hidden, and unknown original distractor intentions remain documented rather than claimed as recovered.
'''
(H/'template-extraction.md').write_text(text)
(H/'plot-extraction.md').write_text('''# Plot decision

Rating: none. All captured source prompts, choices and worked solutions are component-form scalar arithmetic, with no image links or embedded plot references. q-168035's dependency is repaired by copying its explicitly given component vectors from its original worked solution into the prompt, preserving the assessed dot-product task without introducing graph interpretation. No plot renderer or generated asset is required.
''')
review_text='# Dot product generator review\n\nImmutable math basis 1356. Original source records are distinguished from generated replays and parameter variants below. Correct answers appear only in this author review.\n\n'
for case,r in zip(cases,replay):
 q=g.SOURCES[case['source_id']]; f=q[':question/answer-fields'][0]
 review_text+='## Original '+case['source_id']+'\n\n'+q[':question/problem']+'\n\nOriginal complete bank: '+', '.join('$'+a[':answer/value']+'$' for a in f[':answer-field/choices'])+'.\n\n'+q.get(':question/worked-solution','Captured worked solution absent.')+'\n\n'
 review_text+='### Generated original-parameter replay\n\nTemplate '+case['template']+'; bank '+case['bank_profile']+'. '+('Standalone vector presentation repair; captured solution exact.' if case['source_id']=='q-168035' else 'Missing correct/level/solution authored; original complete bank exact.' if case['source_id']=='q-1355' else 'Original prompt, complete bank, and full solution exact.')+'\n\n'+g.markdown(r)+'\n\n'
for i,r in enumerate(review):
 gen=r['generation'];level=r['question'][':question/difficulty'].split('/')[-1]
 review_text+=f"## Generated variant {i+1} — {level}\n\nTemplate `{gen['template']}`, profile `{gen['bank_profile']}`, seed {gen['seed']}. Origin: {gen['origin']}; level: {gen['level_origin']}.\n\n"+g.markdown(r)+'\n\n'
(H/'review.md').write_text(review_text)
(H/'README.md').write_text('''# Component dot product generator

Scope: KP17592186059730 only; captured math basis 1356. One scalar dot product by corresponding-component multiplication and addition. No database operations.

Run from the repository root:

```sh
.venv/bin/python generate/scratch/17592186059730/validate.py
.venv/bin/python generate/scratch/17592186059730.py --difficulty all --seed 42 --count 2 --format markdown
.venv/bin/python generate/scratch/17592186059730.py --difficulty easy --profile observed_1340 --seed 42 --format json
```

The API exposes `generate`, `generate_easy`, `generate_moderate`, and `generate_hard`; explicit parameters/profile replay follows `source-cases.json`. Original sources remain in `source.json`. All seven source complete banks replay; source-format repairs and absent correct/solution data are reported separately in `validation.json`. Moderate and hard levels and normal radio banks are authored extensions. Source scalar distractor intent remains underdetermined and observed-bank numerical reconstructions are explicit replay profiles only.

`validate.py` independently reads the actual printed vectors, checks every option and every formal/multiplication/evaluated-product/final stage, exact full source solution equality, identity, formatting, workload guards, and native engine grading. `engine-input.json` and `engine-report.json` preserve native evidence. `review.md` includes every original, every original-parameter replay, changed variants for every observed bank, and at least two authored variants per difficulty/layout. `freeze.json` records the frozen actual artifact hashes for parent QA.
''')
