#!/usr/bin/env python3
"""Private deterministic evidence renderer; never modifies shared files."""
from pathlib import Path
import importlib.util,json,hashlib
ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('axes',ROOT.parent/(ROOT.name+'.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
source=json.loads((ROOT/'source.json').read_text());questions=source['record'][':knowledge-point/questions'];cases=g.source_cases();reviews=json.loads((ROOT/'review.json').read_text())
lookup={q[':question/math-academy-id']:q for q in questions}
classification='''# Classification

Captured database math, basis1356, lineage01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1. The immutable capture has21 practice questions, separately from canonical e-5073.

| Level | Observed practice | Fields | Markdown/layout templates | Complete radio profiles | Plots |
|---|---:|---|---:|---:|---|
| Easy |20|12 radio;8 pairs of blanks|5|12|none|
| Unrated |1|radio; missing correct ref|1|1|none|
| Moderate |0|authored radio or paired blanks|shared standard form|authored default|none|
| Hard |0|authored radio or paired blanks|shared standard form|authored default|none|

Six presentation templates retain So/Thus, a double space before one radius, the unrated compact fraction spelling, and the newline preceding the first blank equation. These are presentation distinctions, not six mathematical skills. All21 use x²/dx+y²/dy=1 with positive unequal integer denominators. No assessment prompt, option or solution references a plot. Other tutorial illustrations do not enter this generator.

Lesson route was followed using activity/first-step then step/next: Introduction → wide ellipse KP87839 → tall ellipse KP87840 → Major and Minor Axes tutorial → this KP87841. The tutorial explicitly defines axes as diameters, semi-axes as radii. Canonical e-5073 reads squared radii36,25, takes roots6,5 and doubles12,10. Key prerequisite is The Product Rule for Radicals, topic1927. The next origin-shift topic is outside this scope.

Easy sampling preserves observed integer denominators1..100, including one or two nonsquare radicands and both orientations. Missing levels are authored number-form extensions of the same operation sequence, not claimed observed labels: moderate requires exactly one reduced fractional squared radius with denominator4 or9; hard requires two reduced fractional nonsquare squared radii with denominator4,9 or16 and squarefree numerator part2,3,5,6 or7, with reduced extracted radical coefficient at most3. Both numerators are ≤100 and denominators ≤16 independently. These add one versus two rational radical simplifications while preserving read → root → compare → double. No normalizations, translations, completing squares, conic classification or new geometry appear.

Meaningful tasks are unordered pairs of squared radii. Orientation, layout, field ordering and bank aliases do not count. Eligible number-form domains:4950 easy blank tasks (4949 authored radio banks; pair1,4 collides),11700 moderate tasks,153 hard tasks. Workload guards apply equally to explicit calls and sampled values after fraction reduction; large reduced denominators fail.

Raw omissions: q-7600 has no difficulty, no worked solution and no correct reference. Public observed replay preserves these omissions. Its mathematically correct option2√10 and6 is independently inferred, not a matched original designation. A separate authored completion is labeled in review. All raw TeX commands contain a single decoded backslash; no escape anomaly was inferred from JSON display.

| Source | template | level | dx,dy | field order | profile |
|---|---|---|---|---|---|
'''
for c in cases:
 classification+=f"|{c['source_id']}|{c['template']}|{'unrated; authored easy arithmetic assignment' if c['authored_level_assignment'] else 'easy'}|{c['parameters']['dx']},{c['parameters']['dy']}|{','.join(c['field_order'])}|{c.get('bank_profile','no distractors')}|\n"
(ROOT/'classification.md').write_text(classification)
extraction='''# Template extraction

## 1. Specific original descriptions

Every original asks major first and minor second, using x and y as coordinates and a,b as horizontal/vertical radius labels. Positive integer squared radii determine the number-form workload; denominators are not radii. Radio answers are text containing two separate inline math fragments joined by “and”; blanks supply the axis-length sentences and expect delimiter-free math fragments. Source field order is retained even where field-2 precedes field-1. Per-original number forms, complete banks and solutions follow in review.md; the classification table records all exact squared-radius pairs and layouts.

## 2. Shared pattern

Identify a²=dx,b²=dy from the already normalized origin-centered standard equation. Take a=√dx,b=√dy. Choose the larger radius as semi-major and smaller as semi-minor; double each. The same complete fixed solution applies regardless of selected wrong answer. Blanks ask for the two scalar lengths; radios ask for an ordered pair.

## 3. Components and complete bank map

Notation: U=max(dx,dy), V=min(dx,dy), A=√U, B=√V. Each recipe below is a complete pair of mathematical expressions. Recipe number is the original bank position, not a correctness-independent random perturbation. All values reproduce literally at original inputs; complete banks are preserved together, and a collision rejects the entire changed instance. Original distractor intent cannot be recovered from scalar values alone. “Opaque” explicitly marks weak arithmetic evidence, retained only by an explicit observed replay profile. Other operations are explicit generalizations, with original intent still unverified. Authored defaults use correct(2A,2B), omit both doubles(A,B), omit minor double(2A,B), omit major double(A,2B), and use squared radii(U,V).

All source fields, values, designated correct values, presence/absence, parameter inputs and recipe expressions are mapped below.

'''
for c in cases:
 q=lookup[c['source_id']];extraction+=f"### {c['source_id']}: dx={c['parameters']['dx']}, dy={c['parameters']['dy']}; {c['template']}\n\n"
 dx,dy=map(g.sp.Rational,(c['parameters']['dx'],c['parameters']['dy']))
 extraction+='Horizontal radius: $'+g.tex(g.sp.sqrt(dx))+'$; vertical radius: $'+g.tex(g.sp.sqrt(dy))+'$. Major orientation: '+('horizontal' if dx>dy else 'vertical')+'. '+str(sum(not g.sp.sqrt(v).is_Integer for v in (dx,dy)))+' nonsquare integer radicands.\n\n'
 for f in q[':question/answer-fields']:
  extraction+=f"Field `{f[':answer-field/key']}`: `{f[':answer-field/type'][':db/ident']}`. Correct ref: "+(f[':answer-field/correct'][':answer/value'] if ':answer-field/correct' in f else 'absent; inference separately recorded')+'.\n\n'
  if 'bank_profile' in c:
   extraction+='|position|original value|parameterized pair|evidence status|\n|---:|---|---|---|\n'
   for i,answer in enumerate(f[':answer-field/choices']):
    recipe=g.RECIPES[c['bank_profile']][i]
    extraction+=f"|{i+1}|{answer[':answer/value']}|`{recipe['expression'][0]}`, `{recipe['expression'][1]}`|{recipe['interpretation']}|\n"
   extraction+='\nProfile: `'+c['bank_profile']+'`.\n\n'
  else:
   extraction+='Value `'+f[':answer-field/choices'][0][':answer/value']+'`; recipe `'+('2*sqrt(U)' if f[':answer-field/key']=='field-1' else '2*sqrt(V)')+'`.\n\n'
extraction+='''## 4. Reusable templates and constraints

The Python script defines complete equation slots, each mathematical prose equality, optional simplified radical stages, major/minor variable names, and final doubling components. Neither answer strings nor worked prose are returned from source objects. Default equations retain `\\frac{{x}^{2}}{DX}+\\frac{{y}^{2}}{DY}=1`; the compact source profile spells `\\frac{x^{2}}{DX} + \\frac{y^{2}}{DY} = 1`. Blank placeholders exactly match field-1/field-2. Introductory/general-equation sentences, displayed block, variable roles, identification → square-root bullets → ordered semi-axes → double axes stage order remain fixed; redundant radius simplification is omitted precisely when its radical spelling is already simplest.

Positive unequal squared radii are mandatory. All radio instances require five distinct complete ordered pairs, exactly one correct pair and positive real lengths; there is no distractor replacement pool. Source decimals remain decimals for designated profile positions when values are integers/halves; other exact values use radical/fraction TeX. No plot assets or renderer are needed.

At raw replay the source's absent difficulty/solution/correct fields remain absent. Generated UUIDs replace original entity IDs, enum dictionaries become local enum strings and correct objects become field-owned lookup refs. These are representation changes, not learner-content changes. The fidelity normalization preserves question text, entire worked prose, field order/types/keys, every complete answer value/type, exact correct value and attribute presence. All practice originals, including the unrated record, are counted. All math identities are independently checked from actual displayed TeX, separate from exact source-content comparison and native grading.

Source q-7600's correct option is derivable as2√10,6, but no original designation exists. No mathematical errors or presentation repairs were found. Six opaque choice transformations remain an interpretation limit, not a fidelity failure. Moderate/hard remain authored design claims. This work stops at guide step7; no database data preparation occurs.
'''
(ROOT/'template-extraction.md').write_text(extraction)
def displayed_review(record):
 q=record['question'];parts=[q[':question/problem']]
 parts.append('Difficulty: '+q.get(':question/difficulty','unrated (attribute absent)')+'. Generation scope: '+record['generation']['level']+'. Evidence only: '+str(record['generation']['evidence_only'])+'.')
 for f in q[':question/answer-fields']:
  parts.append('Field '+f[':answer-field/key']+':')
  cid=f.get(':answer-field/correct',[None,None])[1]
  parts.extend('- '+a[':answer/value']+(' **correct**' if a[':answer/id']==cid else '') for a in f[':answer-field/choices'])
 if ':question/worked-solution' in q:parts.append(q[':question/worked-solution'])
 return '\n\n'.join(parts)
review='# Original and generated review\n\nOriginals are unmodified captured learner content. Generated variants are labeled; q-7600 raw omissions remain visible. No correctness designation is fabricated for its original.\n\n'
for q in questions:
 review+='## Original '+q[':question/math-academy-id']+'\n\n'+q[':question/problem']+'\n\nDifficulty: '+q.get(':question/difficulty',{}).get(':db/ident','unrated (attribute absent)')+'.\n\n'
 for f in q[':question/answer-fields']:
  review+=f"Field {f[':answer-field/key']} ({f[':answer-field/type'][':db/ident']}):\n\n"
  for choice in f[':answer-field/choices']:review+='- '+choice[':answer/value']+ (' **correct**' if f.get(':answer-field/correct',{}).get(':answer/id')==choice[':answer/id'] else '')+'\n'
  review+='\n'
 review+=q.get(':question/worked-solution','Worked solution, difficulty and correct ref absent in capture.')+'\n\n'
 for item in reviews:
  if item['label'].endswith(q[':question/math-academy-id']) and 'Observed-template' in item['label']:
   review+='### '+item['label']+'\n\n'+displayed_review(item['record'])+'\n\n'
for item in reviews:
 if not item['label'].startswith('Observed-template'):
  review+='## '+item['label']+'\n\n'+displayed_review(item['record'])+'\n\n'
review+='''## Difficulty review

Easy repeats the observed root/order/double method with integer squared radii, including radicals. Moderate introduces exactly one fractional squared radius with a small perfect-square denominator; hard has two fractional nonsquare squared radii. These are comparable instances within each authored level, not a progression through mathematical branches. Every level uses the same fixed five-choice authored bank or original two-blank layout. All three sets preserve positive lengths, exact arithmetic, familiar small squarefree parts, and the complete source stage sequence. Changed-parameter source variants test every observed bank/layout; the raw incomplete q-7600 variant is evidence, with normal authored completion shown separately. Native results:104 accepted,150 rejected,0 unresolved; missing-ref raw q-7600 cannot be graded and was not counted as a native pass.
'''
(ROOT/'review.md').write_text(review)
(ROOT/'README.md').write_text('''# Ellipse axis-length generator

Run `.venv/bin/python generate/scratch/17592186087841/validate.py`, then `.venv/bin/python generate/scratch/17592186087841/build_evidence.py` to regenerate private review evidence. Preview: `.venv/bin/python generate/scratch/17592186087841.py --difficulty all --count 2 --seed 42 --format markdown`.

API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` and three difficulty entrypoints. Parameters are exact `dx`,`dy` squared radii. Explicit observed radio profiles use `observed_q-N`; source blank layouts use `source_q-N`. All replay cases are in source-cases.json. Default banks are separately authored; observed profiles are explicit evidence requests.

21/21 source banks,81/81 option values,21/21 prompts,20/20 present worked solutions and28/28 present correct refs match. One source lacks difficulty, solution and correct ref; raw presence parity is verified, completion is separate. 90 authored instances plus21 changed-source profiles are mathematically checked. Native checks104 accepted and150 rejected; raw missing-ref evidence is not grader-compatible and is excluded from native fixtures only, never source coverage. Six opaque numerical transforms have no recovered intent. Moderate/hard scope is authored bounded rational arithmetic of the same ellipse method. No plots or DB writes.

manifest.json freezes producer/input/output SHA256 hashes; evidence is local review data. Parent independent QA remains separate.
''')
# Freeze exact producer and evidence hashes. The manifest itself is not recursively
# hashed; transient __pycache__ is excluded. No evidence or asset pruning.
paths=[ROOT.parent/(ROOT.name+'.py')]+sorted(p for p in ROOT.iterdir() if p.is_file() and p.name!='manifest.json')
inputs=[Path('generate/runs/current/sources/17592186087841.json'),Path('generate/runs/current/topics/17592186049456.json'),Path('generate/runs/current/lessons/17592186049456.json')]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
manifest={'generator_version':g.VERSION,'source_provenance':g.SOURCE,'producer_frozen':True,'producer_sha256':sha(ROOT.parent/(ROOT.name+'.py')),'input_sha256':{str(p):sha(p) for p in inputs},'files':{str(p):sha(p) for p in paths}}
(ROOT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('Wrote classification, extraction, review, README and frozen manifest.')
