#!/usr/bin/env python3
from pathlib import Path
import importlib.util,json,hashlib
H=Path(__file__).parent;sp=importlib.util.spec_from_file_location('g',H.with_suffix('.py'));g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g)
def write(name,text):(H/name).write_text(text)
context={'topic':json.load(open('generate/runs/current/topics/17592186050567.json')),'lesson':json.load(open('generate/runs/current/lessons/17592186050567.json'))}
write('context.json',json.dumps(context,indent=2,ensure_ascii=False))
authoritative=json.load(open('/home/jake/Developer/MA/DATA/Lessons/2198/Source/2198.json'))
widgets=[q for q in authoritative['lesson']['items'] if q.get('question_id') in ('125852','125853')]
write('authoritative-widgets.json',json.dumps({'source':authoritative['source_html'],'schema_version':authoritative['schema_version'],'widgets':widgets},indent=2,ensure_ascii=False))
cases=[{'source_id':t,'template':t,'level':g.LEVELS[t],'parameters':p,'bank_profile':'raw'} for t,p in g.ANCHORS.items()]
write('source-cases.json',json.dumps(cases,indent=2))
classification='''# Classification

Snapshot: database math, basis 1356, lineage 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1. Seven practice questions; the canonical example is not counted. All require exactly the set of fields whose scalar curl is identically 1 on R². Equaling 1 at some points or enclosing one particular area does not qualify.

| Level | Practice templates | Captured banks | Fields | Plot rating |
|---|---:|---:|---|---|
| Easy | 2 | 3 | radio selection; q-125852 has a redundant legacy radio field | none |
| Moderate | 5 | 6 | radio selection; q-125853 has a redundant legacy radio field | none |
| Hard | 0 observed; 1 authored | 1 authored operation bank | radio selection | none |

Sources q-125852 and q-125853 carry two same-key fields; the older field lacks a correct reference. The authoritative lesson capture shows one five-choice widget for each (authoritative-widgets.json). Public raw replay retains both fields, all bank values, every original UUID and reference at the anchor, and key-presence parity. Normal generation uses the single active field, with its original complete bank. This is a documented presentation repair. There are seven captured active correct designations, not nine inferred matches.

Every source is a distinct expression/solution family within its observed level; changes of coefficients or powers remain variants of that family. No prompt, answer, or solution contains a plot asset. No rendering is needed in steps 5/7.

Lesson route (following first-step / next): introduction 17592186134864 → concrete example 17592186134868 → negatively oriented curves 17592186134876 → this KP 17592186134865 → setup KP 17592186134866 → area-calculation KP 17592186134867. The key prerequisite is Introduction to Green's Theorem (2116). This generator stops at recognizing admissible fields; neither adjacent setup nor area calculation is assessed.

Hard is explicitly authored, not an observed difficulty claim. It preserves three fields, the same five-choice set response and identical unit-curl criterion. Two candidates require both mixed-variable held derivatives plus fractional linear contributions; a third requires signed exponential chain contributions whose curls are not identically one. These are familiar polynomial/exponential partial derivatives already present in the easy/moderate/canonical sources, with more contributions to retain. Every hard instance has 11 nonzero additive contributions across its six held partials, whereas each observed family has at most 7. This whole-question workload distinction persists at every explicit parameter boundary. It introduces no integration, region computation, domain branch, or progression.
'''
write('classification.md',classification)
extraction='''# Four-stage template extraction

## Stage 1 — specific source descriptions

Each source uses the same simple/piecewise-smooth/closed/positive curve premise and a circulation equal to area for **any** such curve in R². Easy prints P,Q pairs and moderate prints F vectors. All sources have three candidates, five text choices and an explanatory Green's theorem opening, area/circulation equality chain, three held partial derivative checks, three collected curls and one concluding response-set sentence. Bullet versus Roman-number list, missing/retained thin space in the area identity, per-pair wording and mathematical spellings are fixed separately for each source.

'''
for t,q in g.QUESTIONS.items():
 fs=g.fields(t,g.ANCHORS[t]);ds=g.derivatives(fs)
 extraction+=f'### {t} ({g.LEVELS[t]})\n\nObserved parameters: `{json.dumps(g.ANCHORS[t])}`.\n\n'
 for i,((P,Q),(py,qx)) in enumerate(zip(fs,ds)):
  extraction+=f'- {g.LABELS[i]}: P = ${g.tex(P)}$, Q = ${g.tex(Q)}$; held P_y = ${g.tex(py)}$, held Q_x = ${g.tex(qx)}$; curl = ${g.tex(g.s.simplify(qx-py))}$.\n'
 extraction+='\n'
extraction+='''## Stage 2 — shared mathematical pattern

Differentiate each Q with respect to x holding y fixed, and each P with respect to y holding x fixed. Subtract P_y from Q_x, retaining signs; a pair is admissible exactly when that function is identically 1 over the declared domain. Return the complete set. Fields whose curl only happens to equal 1 somewhere remain ineligible.

## Stage 3 — component and complete-bank map

The source strings and extracted complete expression slots are in source.json and extraction-components.json. Each option below is a full finite subset of {I,II,III}; its exact recipe is the indicated subset, independently compared with the derived admissible set. These historical choices contain no numeric distractor whose intent needs guessing. No source distractor diagnosis is added to learner prose.

'''
components={}
for t,q in g.QUESTIONS.items():
 components[t]={'parameters':g.ANCHORS[t],'prompt_mask':g.MASKS[t][0],'solution_mask':g.MASKS[t][1],'original_field_components':g.MASKS[t][2],'original_P_y':g.MASKS[t][3],'original_Q_x':g.MASKS[t][4],'original_curls':g.MASKS[t][5],'fields':q[':question/answer-fields']}
 for j,f in enumerate(q[':question/answer-fields']):
  extraction+=f'### {t}, bank {j+1}, field `{f[":answer-field/id"]}`\n\n'
  for a in f[':answer-field/choices']:
   idx=[i for i,name in enumerate(g.LABELS) if __import__('re').search(r'\b'+name+r'\b',a[':answer/value'])]
   correct=f.get(':answer-field/correct',{}).get(':answer/id')==a[':answer/id']
   extraction+=f'- `{a[":answer/id"]}` → `{a[":answer/value"]}`; recipe = subset {idx}; '+('captured correct' if correct else 'captured incorrect' if ':answer-field/correct' in f else 'designation absent in this legacy bank')+'.\n'
  extraction+='\n'
extraction+='''## Stage 4 — reusable template and constraints

Public API templates are the seven source IDs plus `mixed`. Prompt masks replace only six complete component RHS slots (never incidental x in prose). Solution masks replace every complete held partial and each complete curl RHS. Original spellings are selected by mathematical expression equality, not a whole-source literal return. Changed components use exact SymPy LaTeX. The public raw profile preserves the original three collected curl rows with no added rows; normal solutions retain the same prose and sequence and add grouped subtraction and individually signed distribution before each collection. The final sentence is generated from all three admissibility checks, including hard candidate permutations.

Parameters and workload guards apply to samplers and explicit calls: a ∈ {1,…,5}; d ∈ {2,…,8}; n ∈ {2,3,4}; authored hard b,k ∈ {1,2,3}; order ∈ {0,…,5} denotes a permutation of the three candidates. Sources retain their original parameter sets; unused keys reject. Every hard instance keeps exactly 11 nonzero additive contributions across the six held partials; observed families have at most 7. This distinguishes the authored level without a new method. These small integers/fractions preserve the familiar source number forms. n remains a single power-rule/chain-rule operation, not a progression. Held-only arctan x, cos x², x, √2x and y components remain globally smooth on R² even though their assessed held derivatives vanish. No logarithms or singular trigonometric fields are permitted.

The default source profile reproduces the complete active historical bank; its operation recipes remain valid over every allowed parameter. Each observed subset T is implemented as the complete eligibility-flip operation S symmetric-difference (S_anchor symmetric-difference T), selected as a whole bank before parameters. This derives each response from the actual assessed decisions instead of looking up source strings. The family/profile is chosen before parameters and any missing/duplicate response rejects the whole bank. `method_toggle` is an authored five-member complete bank: correct set S, S symmetric-difference {I}, S symmetric-difference {II}, S symmetric-difference {III}, and complement(S). These represent individual eligibility decision mistakes and complete reversal. The raw profile retains every captured bank together, including the two absent legacy references, and is evidence-only. Normal defaults cover all source families; hard uses the method bank. No first-valid distractor pooling occurs.

Content identity hashes actual difficulty, prompt, fixed solution and complete displayed bank. Original raw anchors preserve source UUIDs; changed raw records receive owned IDs derived from their actual content. Seed/answer order cannot change normal content identity. Mathematical task fingerprints remove held-only components and identical nonconstant terms canceled from both derivatives, sort candidate derivative pairs to exclude Roman-label permutations, and exclude bank aliases. Shared gradient decorations, hard n/b changes that only cancel and answer order are not counted as meaningful variety. Finite enumeration uses only parameters affecting the retained assessed derivatives; the resulting counts appear in validation.json.

No mathematical source error was found in the seven practice prompts, partials, curls or active keys. Raw equality statements with `≠1` mean “not identically one” in this universal-curve context, not “unequal at every point.” For example q-126575's polynomial curl can equal one at individual points but is not eligible.
'''
write('template-extraction.md',extraction);write('extraction-components.json',json.dumps(components,indent=2,ensure_ascii=False))
write('plot-extraction.md','# Plot extraction\n\nAll seven practice prompts, solutions and full banks have been checked: no mathematical plots or asset references occur. The owning lesson’s introductory region diagrams are contextual, not assessed objects in this KP. Plot rating is none; no figure is inherited or regenerated. Steps 5 and 7 are complete without a renderer.\n')
reviews=[]
for t,p in g.ANCHORS.items():
 reviews.append({'label':'Original public raw replay '+t,'record':g.generate(g.LEVELS[t],template=t,parameters=p,profile='raw')})
 for seed in (17,39):reviews.append({'label':'Generated observed-family variant '+t+' seed '+str(seed),'record':g.generate(g.LEVELS[t],template=t,seed=seed)})
for seed in (7,23,49):reviews.append({'label':'Authored hard variant seed '+str(seed),'record':g.generate('hard',seed=seed)})
write('review.json',json.dumps(reviews,indent=2,ensure_ascii=False))
review='# Original and generated review\n\nOriginal sections are public parameterized raw replays. Generated source-family sections use the active original bank with added distributed arithmetic. Hard is authored and labeled. No plots occur. Metadata stays outside learner content.\n\n'
for item in reviews:review+='## '+item['label']+'\n\n'+g.markdown(item['record'])+'\n\n---\n\n'
write('review.md',review)
write('README.md','''# Unit curl recognition scratch generator

Run from the repository root:

```sh
.venv/bin/python generate/scratch/17592186133895.py --difficulty all --seed 17 --count 2
.venv/bin/python generate/scratch/17592186133895/validate.py
```

API: generate_easy, generate_moderate, generate_hard, and generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None). Replay each source with source-cases.json, its observed level, exact parameters and `profile="raw"`. Raw anchors retain all captured fields and ref omissions; they are evidence-only. Normal output uses one active radio field. Seven observed families (two easy, five moderate), one explicitly authored hard family; every component is smooth on R². No plots, database writes, engine edits or registration.

Validator reads actual displayed fields, partials, every grouped/distributed/collected curl stage and concluding selection with independent exact mathematics. It checks complete subset banks, fidelity/key-presence separately, all default families, guards, stable identities, formatting mutations and actual native engine choices. The two raw legacy fields without correct references cannot be graded; their absence is recorded and never counted as a matched designation.
''')
print('Evidence built',len(reviews),'reviews')
