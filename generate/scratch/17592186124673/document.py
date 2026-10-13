import json,importlib.util,hashlib
from pathlib import Path
D=Path(__file__).resolve().parent;spec=importlib.util.spec_from_file_location('g',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
s=json.loads((D/'source.json').read_text());qs=s['record'][':knowledge-point/questions'];cases=json.loads((D/'source-cases.json').read_text())
widget=json.loads(Path('/home/jake/Developer/MA/DATA/Lessons/1924/Source/1924.json').read_text())
def walk(x):
 if isinstance(x,dict):
  if x.get('question_id') in ('106661','106662'):yield x
  for v in x.values():yield from walk(v)
 elif isinstance(x,list):
  for v in x:yield from walk(v)
(D/'authoritative-widgets.json').write_text(json.dumps(list(walk(widget)),indent=2)+'\n')
classification='''# Classification

Immutable math snapshot basis1356, lineage01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1; source.json copies the captured wrapper and source-cases.json covers all practice sources.

| Level | Observed sources | Templates | Complete banks | Fields | Plot |
|---|---:|---:|---:|---|---|
| Unrated |1|1 factored equation|1|radio5|none|
| Moderate |1|1 expanded equation|2 (duplicate legacy)|two radio5|none|
| Hard |4|factored IVP; expanded IVP with2 or3 above-cap comparisons|4|radio5|none|
| Easy |0 labeled|factored equation inferred from unrated source|authored completion of observed bank|radio5|none|

The hard expanded family has two solution stage templates (two or three excluded negative-slope IVPs); counting those separately gives five Markdown/solution templates overall, with four API mathematical families. There are six practice questions and seven complete original banks /35 options. All six are included, not only the canonical example. No image/plot references appear anywhere in their prompts, choices, or solutions; steps5/7 require no renderer.

Lesson route is resolved by first-step/next:17592186125687 Introduction →17592186125688 this KP →17592186125689 Modeling Inhibited Growth tutorial →17592186125697 continuation →17592186125690 Modeling Inhibited Growth KP →17592186125691 Solving an Inhibited Growth Model. Prerequisite: Exponential Growth and Decay Models With First-Order ODEs (topic17592186048127). This KP recognizes k(a−y), k>0, and for IVPs checks initial<a; it does not model scenarios, integrate, or solve the IVP.

q106661 is unrated and has no correct ref or worked solution: exact raw replay omits these attributes, while normal easy has independently derived correct choice and an authored solution/label. Canonical e6686 and the factored source anchor easy's direct recognition workload. q106662 contains a legacy five-choice field lacking correct ref and a newer five-choice field with correct ref. Captured authoritative lesson1924 widget has ONE five-option multiple-choice question; normal generation uses this single field. Raw public observed_106662 retains both banks and absent legacy designation. q37180 option2's thin-space grouping1\\,23 equals123; its source presentation is retained, no mathematical correction is claimed.

No observed source is excluded. Missing designations cannot be included in the5/5 designation match denominator. All35 options and all5 present whole solutions must match exactly. Heterogeneous IVP coefficient choices do not establish a shared numerical distractor transformation: parameterized object banks retain evidence without claiming recovered author intent.
'''
(D/'classification.md').write_text(classification)
extract=['''# Template extraction

## Stage1 — original instances

Exact prompt, source answer fields, complete choices, correct refs and entire solutions are preserved in source.json; source-cases.json declares actual parameter recipes. The mapping below enumerates every option of every source field, including the legacy field.
''']
for q,case in zip(qs,cases):
 extract.append('\n### '+case['source_id']+' / '+case['template']+' / '+case['bank_profile']+'\n\nParameters: `'+json.dumps(case['parameters'])+'`\n\nPrompt: '+q[':question/problem'])
 if case['template']=='factored_equation':recipes=['−k(y+a)','a(y+k)','a(y−k)','k(a−y) correct','k(y−a)']
 elif case['template']=='expanded_equation':recipes=['k−ka·y','ky−ka','ka−ky correct','ky²−ka','ka−ky²']
 elif case['template']=='factored_ivp':recipes=['k(y−a),initials[0]','k(a−y),initials[1]>a','k(a−y),initials[2]<a correct','ky(y−a),initials[3]','−k(y+a),initials[4]']
 else:recipes=[f"Independent affine object options[{i}]: c+bP, P(0)=initial; k=−b, a=−c/b" for i in range(5)]
 for ix,f in enumerate(q[':question/answer-fields']):
  rr=[recipes[i] for i in [3,0,2,1,4]] if case['template']=='expanded_equation' and ix==0 else recipes
  extract.append('\nField '+str(ix)+' id '+f[':answer-field/id']+' /selection/radio\n\n| Original value | Parameterized complete value recipe | Designation |\n|---|---|---|')
  for a,recipe in zip(f[':answer-field/choices'],rr):extract.append('|`'+a[':answer/value']+'`|'+recipe+'|'+('correct' if f.get(':answer-field/correct',{}).get(':answer/id')==a[':answer/id'] else 'not designated' if ':answer-field/correct' not in f else 'wrong')+'|')
 extract.append('\nWorked solution: '+q.get(':question/worked-solution','ABSENT; raw replay keeps it absent.'))
extract.append('''
## Stage2 — generalized pattern

An inhibited growth model is a negative-slope linear RHS with the stated limiting level, k(a−y), k>0. When a bound y<a is supplied, the correct candidate must grow throughout that declared range; a different equilibrium cannot establish that. For an IVP, additionally initial<a. Factored recognition is easy (inferred); expanded integer coefficients require factoring (observed moderate); factored or heterogeneous expanded IVPs add initial-condition discrimination (observed hard). Every variation at a level has the same assessed demands; there is no staged progression and no new solving skill.

## Stage3 — complete components and bank accounting

Every source choice above is an entire equation or entire IVP, not separately compared equation sides. Factored bank sign/reversal/swap/nonlinearity operations are defensible actual-method distractors. Expanded-equation swap k−ka·y has negative slope but its cap1/a differs from the declared a; it is ineligible under the stated range. Heterogeneous hard original banks hold five independent affine triples (intercept c, slope b, initial) with exactly one negative-slope below-cap model, two or three negative-slope above-cap objects and the remaining reversed-slope objects. Their independent intercept/rate numbers are not evidence of an inferred scalar-error algorithm. They are publicly replayable with new complete parameters and fixed role positions; raw evidence profiles are not weighted as normal defaults.

There are7/7 exact complete raw banks and35/35 exact options. Present wrong-designation count20/20 corresponds to the five source banks with correct refs; the other10 choices cannot be called observed distractors without inferring their missing designation. Independent mathematics identifies4 wrong choices in each of those2 missing-ref banks for normal completion, separately labeled authored/inferred. Source solutions:5/5 exact whole prose and display-stage sequences; absent1 is not an exact solution match.

## Stage4 — reusable templates, conditions and workload

Fixed components: original instructional sentences and formal k(a−y) definition; prompt question relation; five radio choices; one fixed worked solution. Variable components: complete numerical coefficients/caps/initial values everywhere in math and prose. Optional source attributes: q106661 difficulty, correct and solution are absent; q106662 legacy field is raw-only. Conditional components: expanded equation factoring paragraph; hard affine correct-factor row and two/three explicit excluded above-cap model rows; normal P teaching row uses P throughout while raw source preserves the original generic y definition. Nonstandard1\\,23 grouping is raw-only. Formula arguments/variable names are built as complete components, not blind scalar replacements.

Domains enforced on sampling AND explicit inputs: factored equation/factored IVP2≤a≤500 and0.1≤k≤20; distinct a,k in easy prevents a swap collision. Moderate uses integer a,k withka≤10000. Factored-IVP five nonnegative initials≤1000 with second initial>a and third initial<a. Hard affine |c|≤100000,0.0001≤|b|≤40,0≤initial≤500000, c and b opposite signs, capacity1..500000, all rates/caps/initials have at most4 decimal places and terminating decimal form. Exactly one below-cap negative-slope candidate; complete fixed profile slope counts and raw role positions; reject duplicate whole IVPs. Bounds preserve source workload of one linear factor or at most one rational division per considered affine model, followed by initial comparison; no arbitrary transcendental evaluation is introduced.

Normal parameter samplers: easy50 caps×6 rates=300 substantive model pairs; moderate20 caps×9 rates=180 pairs; factored hard9 caps×8 rates=72 correct-model/initial tasks; heterogeneous hard16 rates, capacity multiples of100 from200 through min(100000,100000/rate), optional half-unit caps, and10 positive gaps per candidate. This enumerates205300 distinct correct rate/cap/initial triples per below-cap role after clamped-endpoint deduplication; only substantive recovered-cap/initial triples count, and distractor variation does not inflate that count. Wrong-bank variation and variable aliases do not inflate canonical mathematical-task counts. None of these finite counts claim recovery of the original sampler. Normal hard chooses factored or heterogeneous families; profiles2/3 denote fixed comparison count, not progression.

Identity: actual prompt, full fixed solution, complete banks and designation presence plus version determine content UUID/hash. Seed/order cannot change it. Canonical mathematical fingerprint uses exact reduced assessed model/cap/initial rather than number spelling, source id, profile, bank or seed. Owned answer UUIDs are field scoped. No database/Math Academy identities are fabricated. The CLI and public API permit explicit parameter/profile raw replay and handle absent solutions/difficulty/correct refs.

No plots were found; steps5/7 complete as none. No plotted-source extraction or image renderer is needed. Stop before database preparation.
''')
(D/'template-extraction.md').write_text('\n'.join(extract)+'\n')
(D/'README.md').write_text('''# Inhibited growth identification generator

Verify from repository root:

```sh
.venv/bin/python generate/scratch/17592186124673/validate.py
.venv/bin/python generate/scratch/17592186124673.py --difficulty all --seed42 --count2 --format json
```

CLI arguments require spaces: `--seed 42 --count 2`. Public API: generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None), plus generate_easy/moderate/hard. Four mathematical families, eleven complete profiles. Six original sources/seven original banks/five present solutions, including missing attributes and legacy duplicate field in raw observed profiles. Five authored default profiles supply all levels; easy's label/solution/correct completion is inferred, not observed. No plots or database writes. validation.json separates exact fidelity, present-designation native grading, and normal-output repairs. Native source fixtures project original designated fields because missing correct refs cannot grade.
'''.replace('--seed42 --count2','--seed 42 --count 2'))
