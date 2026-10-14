"""Write the prescribed local author review after validate.py passes."""
import hashlib,importlib.util,json
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('matrix_add_docs',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
load=lambda n:json.loads((HERE/n).read_text())
def write(n,s):(HERE/n).write_text(s.strip()+'\n')

classification='''# Classification — Adding Square Matrices

Draft only. The registered numeric generator and its entire evidence directory are preserved. Source is the whole immutable `math` wrapper at basis **2275**, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`; `source.json`, `topic.json` and `lesson.json` retain their wrappers. Owning topic is **17592186049304**, Adding and Subtracting Matrices (MA29).

Six MA original practice questions (five easy, one unrated), plus one independently authored easy inventory record. These seven captured practice records are distinguished throughout; `independent-inventory.json` preserves the independent record exactly with its role, basis and lineage. They contain 14 raw answer fields (six five-choice radio banks including a legacy duplicate, eight scalar blanks) and 38 values. The canonical example is curriculum evidence, not an eighth practice question. `inventory.json` independently preserves learner availability: five easy, zero moderate, zero hard; availability is not the practice-source denominator.

| Source | Observed difficulty | Template | Raw fields | Bank profile | Plots |
| --- | --- | --- | --- | --- | --- |
| q-101 / 17592186054939 | unrated | inline-question | one radio, absent key | observed-q-101 | none |
| q-11440 / 17592186054967 | easy | named-radio | two radios with same key; legacy lacks key | observed-q-11440 | none |
| q-100 / 17592186237775 | easy | inline-equality | one radio | observed-q-100 | none |
| q-125630 / 17592186259832 | easy | named-radio | one radio | observed-q-125630 | none |
| q-125631 / 17592186259833 | easy | named-radio | one radio | observed-q-125631 | none |
| q-319591 / 17592186299781 | easy | cell-blanks | four scalar blanks | none | none |
| ef70fb38-cef6-5843-b533-7177233ed52d / 17592186510633 | easy | cell-blanks | four scalar blanks | none | none |

Four backbones, five observed whole-bank profiles. Named matrix letters and parentheses around negative first operands are notation slots, not additional skill templates. A blank returns each of the four integer cells; it does not request a single matrix fragment. Moderate/hard share these existing response contracts and have no observed template count or label.

The original MA29 capture shows q-11440 as one five-choice widget. Its two raw EDB fields have identical full banks and identical `selection` keys; normal output has one radio. Raw public replay preserves both fields and their distinct key-presence contracts, and the absent legacy key does not count as a matched original designation. q-101 has no supplied designation/solution/rating: its raw public API preserves all three absences. Entrywise mathematics identifies [-13,0;18,-8]; a separately labeled eligible completion authors the matching solution, key and easy placement. Its raw EDB prompt is retained although the independent MA widget used inline equality wording. `authoritative-layout.json` records that discrepancy without overriding the fixed-basis source.

The canonical prompt omits B and the tutorial prompt omits one displayed matrix; their solutions supply the missing operands. These are curriculum capture defects, preserved raw. Neither incomplete prompt is used as a generated question. No practice source is excluded, no mathematical value is corrected, and all existing solutions replay exactly (including valid redundant nested aligned environments).

Lesson route is followed by links: Introduction → Adding Square Matrices → Adding Non-Square Matrices → Subtracting Matrices tutorial → Subtracting Matrices KP. The tutorial states corresponding-entry addition of equal-dimension matrices; prerequisites are Introduction to Matrices, Adding a Negative Number and Subtracting a Negative Number. Neighbor KPs exclude rectangular addition and matrix subtraction from the assessed operation; scalar multiplication follows this topic and is excluded.

Moderate/hard are conservative authored arithmetic-workload bands, not recovered MA labels. Moderate uses nonzero signed entries of absolute value 1..25, exactly two opposite-sign corresponding pairs, and at least two two-digit operands. Hard uses four opposite-sign two-digit corresponding pairs (absolute value 10..99), with two positive and two negative sums. Both retain the same two supplied 2×2 matrices, four entrywise additions, response layouts, wording and solution stages. There is no sequence/progression within a band. Choosing larger signed integer operands increases the arithmetic demands without adding an operation or field. These design labels remain subject to independent root QA.
'''
write('classification.md',classification)

parts=['''# Template extraction

The whole raw source and every field/value are retained in `source.json`. `source-cases.json` contains six MA-original public raw-API replay cases, including the unrated original. `independent-cases.json` separately replays the one exact independently authored inventory record preserved in `independent-inventory.json`. `source-choice-mapping.json` maps every one of 38 raw answer values to its complete expression pattern and generated value, including both duplicate q-11440 banks. All 24 raw distractors are accounted for. Recipes below represent observed mathematical patterns; exact numeric reproduction does not establish cognitive intent.

## Stage 1 — describe each source before generalizing
''']
for case,q in zip(load('source-cases.json')+load('independent-cases.json'),g.SOURCE['record'][':knowledge-point/questions']):
 p=case['parameters'];c=g.addition(p);parts.append(f"### {case.get('source_math_academy_id') or ('Independently authored inventory '+case['source_id'])}\n\nSource {q[':db/id']}, {case['observed_level'] or 'unrated'}. Operand entries in row-major order: A={p['a']}, B={p['b']}; result={c}. Values are exact signed integers; zeros, opposite signs and cancellation are retained. Names {p['names']} and first-operand wrapping positions {p['wrap_first']} are source notation. Template `{case['template']}`; "+('five complete matrix choices.' if case['template']!='cell-blanks' else 'four scalar blanks, field-1/2 on the first response row and field-3/4 on the second.')+'\n\n'+q[':question/problem']+'\n\n'+q.get(':question/worked-solution','No source worked solution. Raw replay preserves its absence; the separately labeled eligible completion authors the corresponding-entry solution.')+'\n')
parts.append('''## Stage 2 — shared mathematical pattern

Given two 2×2 integer matrices, add each pair of corresponding entries and return the whole sum, either by selecting its matrix or entering all four scalar cells. No scalar-solving, matrix multiplication, determinant, dimension inference, symbolic coefficients or rectangular matrices are added. Every displayed cell affects the assessed task; no unrelated unqueried entry is sampled.

## Stage 3 — components and complete banks

Prompt components are the two supplied matrices, addition sign, optional distinct names, and one observed response contract. Solutions share “We add the corresponding entries:” followed by displayed operand sum, corresponding-entry arithmetic matrix and collected matrix. The inline-equality solution combines the operand and arithmetic matrices in its first equality row; named/inline-question/cell templates keep the operand sum as its own equality row. The source contains no distractor feedback; none is added.

For complete source banks let a/b/c be row-major first operand, second operand and correct sum, with indices 00,01,10,11. Each list below is a complete five-choice bank in recipe order; choice order is not fidelity. Every untouched entry is c. Source answer UUIDs and each exact source matrix are mapped one-to-one in `source-choice-mapping.json`.
''')
for profile,recipes in g.OBSERVED_RECIPES.items():parts.append('### '+profile+'\n\n'+'\n'.join(str(i+1)+'. `'+r+'`.' for i,r in enumerate(recipes))+'\n')
parts.append('''Copy-entry, repeated-entry, arbitrary +1, and compound sign patterns have underdetermined cognitive intent. These full observed banks are public **evidence-only** profiles requiring explicit parameters; they never enter default learner sampling. They are parameterized expressions, not literal question/value return branches. Raw `raw-q-*` profiles and separate eligible completed `observed-q-*` profiles use the same parameterized prompt/solution/bank calculations and shared assembly. Raw profiles preserve source difficulty/solution/key presence and duplicate contracts; completed profiles add only the documented eligible presentation. No captured learner payload is copied into an API result. Changed-parameter review cases verify each pattern through the public API; their status remains evidence-only, not a recovered method bank. A full-bank collision rejects the entire explicit instance.

Default authored profiles derive complete wrong operations from the assessed corresponding-entry/sign method. They are distinct from observed-bank fidelity:
''')
for profile,recipes in g.AUTHORED_RECIPES.items():parts.append('### '+profile+'\n\n'+'\n'.join(str(i+1)+'. '+r+'.' for i,r in enumerate(recipes))+'\n')
parts.append('''## Stage 4 — backbone, slots and constraints

| Component | Role / allowed slot | Dependent content / constraint |
| --- | --- | --- |
| Dimension/operator | fixed 2×2, two supplied matrices, addition | four corresponding additions; no change of skill |
| a00..a11 and b00..b11 | eight exact integer operand slots | prompt, all solution operand/addend/sum cells, every whole-bank operation, four keys |
| All result cells | fixed target set {00,01,10,11} | radio selects whole matrix; blanks request all four, no unqueried cell |
| Matrix names | distinct uppercase names | named prompt and solution change together; notation only, excluded from task counts |
| First-negative grouping | eligible row-major indices 0..3 | explicit parentheses only; unused positive grouping does not change content identity |
| Redundant outer alignment | boolean notation slot | source blanks retain nested aligned; no extra arithmetic stage or task count |
| Complete bank | one eligible complete profile chosen first | compute all five options, reject any correct/incorrect or incorrect/incorrect equality; no first-valid pooling |
| Level | authored guards described in classification | applied equally to explicit parameters and sampler; observed banks only easy |

The four fixed parameterized prompt/solution builders preserve full original wording and stage sequence. Source parameters and source profile replay through `generate(level, seed=0, template=..., parameters=..., profile=...)`. Normal blanks have no bank profile; raw blank profiles preserve their source field layouts and order. Every scalar blank owns its value. `raw-q-101` leaves solution, grade and correct ref absent; `raw-q-11440` retains the duplicate selection fields and absent legacy ref. Only separately labeled eligible completions author missing stages/key/rating or collapse the legacy field. Raw source records are ineligible for native fixture grading when a correct ref is absent; no engine change is made.

Normal samples retain one concrete worked solution independent of the chosen error. Both summands are shown at every cell, negative second operands are parenthesized, and no malformed `+-`/`--` sequences are introduced. Shared `math_format.py` supplies matrix rendering, normalizes prose/bare answers before identities, and validates every public return. Raw evidence is never normalized in place.

Semantic task identity hashes the unordered pair of complete supplied matrices (addition is commutative), excludes names, grouping, profile, bank, layout, level, seed and option order. Presentation identity hashes version, displayed difficulty (or its absence), actual normalized prompt, complete fixed solution (or its absence), canonically ordered keyed field contracts, complete unordered banks and present correct values. Absent attributes and duplicate raw contracts enter the identity explicitly; field collection order alone does not. Different banks get distinct identities; changing seed/order alone does not. Unused notation parameters cannot add identities.

Scope limits and fidelity denominators are recorded in `validation.json`. All supplied designations and available solutions are tested separately from bank matching, inferred missing keys, native grading, or authored-level design claims.
''')
write('template-extraction.md','\n\n'.join(parts))
write('plot-extraction.md','''# Plot extraction / specification

No mathematical plot, diagram, image option or asset reference occurs in the seven practice sources. The supplied matrices and solutions are text mathematics, not plots. All four templates and all three levels have plot rating **none**. Shared `math_format.matrix_tex` renders parameterized matrices into TeX. No rendering model, direct SVG, external image or stale source asset is used; plot-generation step 7 requires no assets.
''')

v=load('validation.json');review=load('review.json')
lines=['# Source and generated review','Author review only. All answers and solutions are shown. Source raw values/fields are retained; generated records are not database transactions.']
for item in review:
 r=item['record'];kind=item['kind'];lines.append('## '+kind+' — '+str(item.get('source_id') or item.get('level'))+' / '+r['generation']['template']+' / '+str(r['generation']['profile']))
 if 'original' in item:
  q=item['original'];lines.append('### Original\n\n'+q[':question/problem'])
  for f in q[':question/answer-fields']:lines.append('Original field '+f[':answer-field/id']+' (`'+f[':answer-field/key']+'`):\n\n'+'\n'.join('- $'+a[':answer/value']+'$' for a in f[':answer-field/choices'])+'\n\n'+('Supplied correct: $'+f[':answer-field/correct'][':answer/value']+'$' if ':answer-field/correct' in f else 'Original correct designation absent.'))
  lines.append('Original worked solution:\n\n'+q.get(':question/worked-solution','Absent in raw replay; only the separate eligible completion adds a solution.'))
 lines.append('### Generated '+('replay' if kind=='observed-replay' else 'variant')+'\n\n'+g.markdown(r))
 if kind=='generated-evidence-variant':lines.append('**Evidence-only parameterized source-bank pattern; unresolved cognitive intent. Not a default learner bank.**')
 if r['generation']['authored_level']:lines.append('**Authored difficulty placement; no observed moderate/hard source label.**')
write('review.md','\n\n'.join(lines))

# Finite domains: upper bounds before eligibility rejection, not claims of supported usable-bank capacity.
N=25**4;bounds={'easy':N*(N+1)//2,'moderate':(50**4)*(50**4+1)//2,'hard':(180**4)*(180**4+1)//2}
finite={'domain':'finite bounded integer domains','mathematical_equivalence':'unordered operand pair; all 4 cells assessed','upper_bounds_before_level_sign_and_bank_rejection':bounds,'eligible_capacity_not_exhaustively_enumerated':True,'verified_distinct_tasks_by_level':v['distinct_mathematical_tasks_by_level'],'verified_distinct_content_by_level':v['distinct_content_by_level'],'not_counted_as_task_variety':['seed','option order','profile','bank','layout','level label','matrix letters','unused grouping'],'observed_evidence_profiles':'Five explicit profiles; no claimed cognitive-template capacity'}
(HERE/'finite-capacity.json').write_text(json.dumps(finite,indent=2)+'\n')
write('report.md',f'''# Verification report

Worker validation passed; independent root QA is still required. All work is confined to `17592186054648-draft.py` and `17592186054648-draft/`; no database, generator registration, engine edits or commits occurred. All {v['baseline_files']} files in the registered numeric baseline retain their before hashes.

MA-original raw fidelity: **6/6 prompts exact, 5/5 available solutions exact, 10/10 raw field banks, 34/34 answer values, 24/24 distractors, 8/8 supplied correct designations**. Raw public replay preserves the two absent designations, one absent grade, one absent solution and the legacy duplicate field. Independently authored inventory: **1/1 exact record, 1/1 prompt and solution, 4/4 raw banks/values/keys**, recorded separately. Across both categories, all seven captured records and 38 values replay. Only eligible completion infers missing keys/solution/rating and collapses the legacy duplicate radio field after complete bank equivalence and authoritative widget inspection. No mathematical/presentation correction was needed for practice replay. Canonical/tutorial incomplete prompts are preserved curriculum evidence and are not served.

Observed source profiles remain evidence-only. All five source profiles have a changed-parameter review example generated through the public API; two authored complete banks provide normal radio generation. All source and authored choices are validated as complete 2×2 matrices; source distractor operations and compound patterns are explicitly mapped.

There are **{v['sample_count']}** tested authored-bank samples, 280 presentations per level. Distinct actual assessed tasks after removing all layout/bank/label differences are **{v['distinct_mathematical_tasks_by_level']}**. Every displayed operand cell varies, with actual slot values recorded in validation.json. The fixed requested target is all four cells; target-location variation would change no assessed demand and is not claimed. Six valid extrema, eleven invalid/bank-collision cases and seven mutation probes (five displayed-content, two raw-presence/duplicate-contract) pass. Every present source solution and every complete sample is read from its actual prompt and all operand, uncollected addend and collected solution cells before checking every answer cell/key. Raw missing solutions/grades/refs remain absent. Two overlapping-domain probes verify that a changed displayed grade changes content identity while leaving task fingerprints unchanged.

Actual `course_academy_engine::learning::grade_field` memory-only tests: **{v['native_grading']['accepted']} accepted, {v['native_grading']['rejected']} rejected, zero unresolved**, across every radio choice and canonical, parenthesized, independently unreduced rational-equivalent and wrong scalar blank entries. No matrix-valued blank fragment exists in this source contract. Two raw profiles (q-101, q-11440) retain absent correct refs and are explicitly ineligible for the native harness; supported raw profiles and every separately completed source profile are graded. `raw-native-ineligible.json` records the limit without supplying fake raw keys. Engine binary hash: `{v['native_grading']['engine_sha256']}`. The grader does not perform EDB operations.

Both random and explicit inputs enforce the same per-level bounds. Stable identity tests cover fixed parameters with changed seed/order, unused grouping, changed complete bank and notation; mathematical fingerprints quotient operand exchange. `finite-capacity.json` gives conservative finite upper bounds before sign/bank eligibility and separately reports verified distinct tasks. These bounded integer domains are not described as unlimited, and upper bounds are not claimed as fully admissible whole-bank counts.

Runtime: Python {v['runtime']['python']}, SymPy {v['runtime']['sympy']}. No plots or plotting runtime is needed.

Remaining interpretation limits: no observed moderate/hard label exists; signed-number workload bands are authored design decisions within the same KP. Copy-entry/repeated-entry/+1/compound source pattern intent is unresolved, so those profiles are never default learner banks. Root independent QA remains pending.
''')
write('README.md','''# Adding Square Matrices — draft generator

This draft preserves the registered `../17592186054648.py` and all numeric evidence. It implements same-method easy, moderate and hard 2×2 signed-integer addition with four observed prompt/solution backbones, five explicit source-evidence banks and two complete authored default banks. All existing radio or four-cell blank contracts remain supported. Moderate/hard labels are authored, not observed MA placements. No within-level progression, matrix subtraction assessment, multiplication, determinant or new field layout is introduced.

Verify from repository root:

```sh
.venv/bin/python generate/scratch/17592186054648-draft/validate.py
.venv/bin/python generate/scratch/17592186054648-draft/build-docs.py
.venv/bin/python generate/scratch/17592186054648-draft.py --difficulty all --seed 42 --count 2 --format json
```

Public interface: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)`, plus `generate_easy`, `generate_moderate`, `generate_hard`. CLI supports all/easy/moderate/hard, template, field type, profile and JSON parameters. Observed evidence-only profiles require explicit parameters and cannot be selected by normal sampling; source-cases.json provides six MA-original raw replay calls; independent-cases.json separately provides the exact inventory replay. Raw profiles preserve all attribute-presence contracts; normal eligible completions are distinct and explicitly labeled. Invalid explicit parameters or equivalent complete banks raise ValueError/SampleRejected instead of silently changing parameters or options.

independent-inventory.json retains the independent generated practice record with its exact captured payload and role; inventory.json instead records learner availability. Source coverage and limitations are in report.md and validation.json; every bank operation in source-choice-mapping.json and template-extraction.md; source/variant previews in review.md and review.json; slots, finite domain bounds and task deduplication in finite-capacity.json. Source, topic and lesson wrappers all retain math2275 provenance. inventory.json separately preserves availability, which is not the source count. baseline-hashes.json verifies every registered-baseline file remains unchanged.

Native grading runs the existing check-engine binary in memory, with no database access. No registration, transaction data, engine edits or shared edits are authorized. Worker checks passed; independent root QA is required before treating the draft as approved.
''')
files=[HERE.with_suffix('.py'),*[p for p in sorted(HERE.rglob('*')) if p.is_file() and p.name!='final-hashes.json' and '__pycache__' not in p.parts]]
(HERE/'final-hashes.json').write_text(json.dumps({'scope':'All draft deliverables excluding this self-referential file and Python cache; worker snapshot before root QA','sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}},indent=2)+'\n')
print('Wrote classify/extraction/review/report/README/finite-capacity and draft hashes.')
