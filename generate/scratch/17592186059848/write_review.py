"""Regenerate current-snapshot review evidence and generator documentation."""
import importlib.util,json
from pathlib import Path
D=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('g',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
source=json.loads((D/'source.json').read_text());cases=json.loads((D/'source-cases.json').read_text())
questions={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']}
records=[];review=['# Identifying Singular Matrices: review','',f"Database {source['database']}, basis {source['basis']}, lineage {source['lineage']}. Original captures and preconversion generator artifacts remain in history/basis-1356. Current source records are shown verbatim; all generated records are local review data."]
for case in cases:
 q=questions[case['source_id']]
 review+=['','## Original '+case['source_id'],'',q[':question/problem'],'','Database field keys: '+', '.join(f[':answer-field/key']+'='+f[':answer-field/correct'][':answer/value'] for f in q[':question/answer-fields']),'',q[':question/worked-solution']]
 record=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile'])
 records.append({'role':'source-replay','source_id':case['source_id'],'record':record})
 review+=['','### Parameterized replay','',g.markdown(record)]
 for seed in (13,41):
  record=g.generate(case['level'],seed=seed,template=case['template'],profile=case['bank_profile'])
  records.append({'role':'generated-variant','source_id':case['source_id'],'record':record})
  review+=['','### Generated '+case['level']+' variant, seed '+str(seed),'',g.markdown(record)]
for seed in (13,41):
 record=g.generate_hard(seed);records.append({'role':'authored-hard','record':record})
 review+=['','## Authored hard example, seed '+str(seed),'',g.markdown(record)]
(D/'review.md').write_text('\n'.join(review)+'\n');(D/'review.json').write_text(json.dumps(records,indent=2)+'\n')
classification=['# Classification','',f"Snapshot: math / basis {source['basis']} / lineage {source['lineage']}.",'','| Level | Practices | Layout/order/stage patterns | Fields | Plot rating |','|---|---:|---:|---|---|']
for level in ('easy','moderate','hard'):
 qs=[q for q in questions.values() if q[':question/difficulty'][':db/ident'].endswith('/'+level)]
 ts=[t for t,v in g.TEMPLATES.items() if v['level']==level and v['source_ids']]
 classification.append(f'| {level} | {len(qs)} | {len(ts)} | Three Boolean checkboxes, I/II/III | none |')
classification+=['',f"There is one mathematical method: calculate a numeric 3×3 determinant, compare with zero, and evaluate three statements. The {sum(bool(v['source_ids']) for v in g.TEMPLATES.values())} observed templates distinguish layout, statement order, arithmetic level and five/six solution stages; they are not different mathematical methods. One Boolean response profile supplies 51 fields across 17 questions.",'','Hard is an authored template because there is no observed hard label. It retains the numeric determinant and singularity task with dense signed fractions and one repeated radical family. Its difficulty is not calibrated against original hard questions. Fraction minors occur in q-77478 and q-38187; fraction/radical cancellation occurs in q-128490 and squared radicals in q-128491. No unknown-entry solving, inverse calculation, row reduction or additional mathematical branch is introduced.','','Lesson order: Introduction → Calculating the Determinant → Singular Matrices → Identifying Singular Matrices → Solving for a Variable → Solving for an Unknown. The prerequisite Introduction to the Inverse of a Matrix establishes singularity as determinant zero.','','The database migration removed the duplicate legacy assessment on q-128490. Its current three Boolean keys are present and reproduced. The previous radio banks and missing legacy designation remain historical evidence, not active generator profiles. Malformed solution bold on q-77477/q-128491 is normalized; equivalent cofactor typography is documented separately from source key and bank fidelity.','','| Layout/order/stage template | Sources | Stages |','|---|---|---:|']
for name,v in g.TEMPLATES.items():classification.append(f"| {name} | {', '.join(v['source_ids']) or 'authored'} | {v['solution_rows']} |")
(D/'classification.md').write_text('\n'.join(classification)+'\n')
extraction=['# Template extraction','','## 1. Specific source descriptions','']
for case in cases:
 spec=g.TEMPLATES[case['template']]
 extraction+=['### '+case['source_id'],'',f"Level {case['level']}; {case['template']}; {spec['solution_rows']} solution stages. Matrix/name/claims: `{json.dumps(case['parameters'])}`. Database keys: `{json.dumps(case['correct_original'])}`.",'']
extraction+=['## 2. Shared mathematical pattern','','Expand det=a(ei−fh)−b(di−fg)+c(dh−eg), evaluate the minors and signed products, compare the determinant with zero and test each of the three statements independently. A numeric determinant claim tests equality; singular tests det=0; nonsingular tests det≠0.','','## 3. Components and complete bank mapping','','Every statement label I/II/III owns exactly the text choices false and true. The correct choice is computed from that displayed statement, with no subset radio bank and no None option. All eight Boolean response combinations can be represented, although statement logic constrains which combinations can be correct. Matrix entries and determinant claims are exact parameters. source-cases.json maps all 17 questions to explicit normal-generator replay calls, including all 51 fields and 102 choices.','','## 4. Reusable template and constraints','','The prompt preserves the source question, Select all that apply, bold Roman bullet labels, and the named matrix. Fixed solution sentences and the five/six cofactor stages remain; evaluated products and conclusions are parameterized. Spaced and unspaced source bullet layouts remain distinct. Matrix values, determinant claims and computed intermediate equalities are independently parsed and checked.','','Easy uses signed integers, with independent matrices or rank-two singular matrices constructed using a row combination, proportional rows (q-69834), or proportional columns (q-77479/q-38187). Moderate independently selects six matrix families before rejection: rational row or column scaling; mixed additive radicals (q-77477); sparse rational/radical positions (q-128491); fraction/radical dependent rows (q-128490); and a radical column with a fraction in another column (q-128484). Every family can generate singular and nonsingular matrices. Normal sampling excludes zero rows and columns, which provide an immediate determinant-zero shortcut absent from the sources; nonzero proportional rows and columns remain supported. This sampling guard leaves explicit replay parameters unchanged. Parameterized formulas produce fresh inputs; replay coverage is reported separately from fresh structural coverage. Hard requires nine nonzero entries with dense rational/repeated-radical scaling.','','Normal easy/moderate sampling is bounded by source maxima for entry magnitude, minor-product magnitude, cofactor contribution, sum of absolute contributions, and determinant magnitude. Easy limits are 8, 35, 48, 89, 30; moderate limits are 8, 42, 28, 33, 23. These are arithmetic workload bounds, not a complete difficulty model. Explicit replay is exempt. Hard has no original calibration.','','False numeric claims are authored arithmetic alternatives from the actual entries, minors and cofactor products: reversing signs, omitting contributions or coefficients, adding minor products, reporting one contribution/entry/trace, or assuming zero. Equal-to-correct and duplicate values are removed. No fixed small-integer false-claim range remains. Fractions, radicals, additive radicals and large integers occur as false claims as well as true claims. These recipes do not claim to recover original misconception intent.','','Explicit invalid parameters fail; sampled invalid matrices or duplicate determinant claims reject the complete instance. There is no longer a rejection solely because a radio bank omitted the true statement subset. Fresh sampling validation parses displayed mathematics, checks arithmetic bounds against independently measured source maxima, and verifies both truth states per matrix family and both proportional dependency types. sampling-review.json retains one normal example per family.','','Identity includes generator version, displayed prompt, fixed solution and all Boolean fields; seed/order do not change identity. Mathematical fingerprints contain matrix values and statement predicates. Old basis-1356 captures and generator code are retained under history/basis-1356; pre-review checkbox artifacts are retained in history/checkbox-v2-pre-review.']
(D/'template-extraction.md').write_text('\n'.join(extraction)+'\n')
(D/'plot-extraction.md').write_text('# Plot extraction\n\nAll practice matrices use LaTeX; the canonical image is unchanged numeric matrix notation. No parameter-dependent graph or diagram is required. Plot rating: none.\n')
(D/'README.md').write_text(f'''# Identifying Singular Matrices ({g.KP_ID})

Current source: math basis {source['basis']}. All 17 practice questions use three Boolean checkbox fields with bold I/II/III bullets and Select all that apply. Old artifacts are retained in history/basis-1356.

All originals share one mathematical method. The twelve observed layout/order/stage patterns do not represent twelve methods. Easy and moderate retain their numeric determinant/singularity scopes. Hard is an authored dense fraction/repeated-radical extension with no original hard calibration. No database writes or registrations occur.

Fresh sampling includes proportional rows and columns, mixed additive radical determinants, and sparse rational/radical positions, alongside fraction row/column scaling. False determinant claims come from the actual matrix arithmetic and can be fractions, radicals or large integers. Easy and moderate arithmetic is bounded by measured source maxima; see template-extraction.md. Each moderate family is selected before rejection to preserve its sampling coverage. Normal samples exclude completely zero rows or columns while retaining nonzero proportional dependencies.

Run from the repository root:

```sh
.venv/bin/python generate/scratch/{g.KP_ID}/build_evidence.py
.venv/bin/python generate/scratch/{g.KP_ID}/write_review.py
.venv/bin/python generate/scratch/{g.KP_ID}/validate.py
.venv/bin/python generate/scratch/{g.KP_ID}.py --difficulty all --seed 13 --count 2
```

The public generate function supports explicit parameters/template and checkbox field_type. The sole current profile is checkbox_I_II_III. Radio requests fail. recipes.json records the captured source basis and layout/order/stage structures; source-cases.json covers every current question. Validation checks all 51 database keys, displayed mathematics, identities, native field/whole-question grading, and 360 additional fresh easy/moderate samples for structural coverage, claim formats and workload. sampling-review.json contains representative normal samples.

Review records show originals, parameterized replays, two variants per source and two authored hard examples. Equivalent solution arithmetic typography and the two source bold repairs are documented separately from exact Boolean-bank fidelity. The native grader helper is in ../source-refresh-2026-10-12.
''')
print('Wrote current review:',len(records),'records')
