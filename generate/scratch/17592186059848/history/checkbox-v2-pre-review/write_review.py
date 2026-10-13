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
classification=['# Classification','',f"Snapshot: math / basis {source['basis']} / lineage {source['lineage']}.",'','| Level | Practices | Observed templates | Fields | Plot rating |','|---|---:|---:|---|---|']
for level in ('easy','moderate','hard'):
 qs=[q for q in questions.values() if q[':question/difficulty'][':db/ident'].endswith('/'+level)]
 ts=[t for t,v in g.TEMPLATES.items() if v['level']==level and v['source_ids']]
 classification.append(f'| {level} | {len(qs)} | {len(ts)} | Three Boolean checkboxes, I/II/III | none |')
classification+=['',f"There are {sum(bool(v['source_ids']) for v in g.TEMPLATES.values())} observed structural templates, one Boolean response profile, and 51 fields across 17 questions. The checkbox migration unifies the old bullet/Roman labels; statement order, blank-line spacing, arithmetic level and five/six-stage solution distinctions remain separate.",'','Hard is an authored template because there is no observed hard label. It retains the numeric determinant and singularity task with dense signed fractions and one repeated radical family. Fraction minors occur in q-77478 and q-38187; fraction/radical cancellation occurs in q-128490 and squared radicals in q-128491. No unknown-entry solving, inverse calculation, row reduction or additional mathematical branch is introduced.','','Lesson order: Introduction → Calculating the Determinant → Singular Matrices → Identifying Singular Matrices → Solving for a Variable → Solving for an Unknown. The prerequisite Introduction to the Inverse of a Matrix establishes singularity as determinant zero.','','The database migration removed the duplicate legacy assessment on q-128490. Its current three Boolean keys are present and reproduced. The previous radio banks and missing legacy designation remain historical evidence, not active generator profiles. Malformed solution bold on q-77477/q-128491 is normalized; equivalent cofactor typography is documented separately from source key and bank fidelity.','','| Template | Sources | Stages |','|---|---|---:|']
for name,v in g.TEMPLATES.items():classification.append(f"| {name} | {', '.join(v['source_ids']) or 'authored'} | {v['solution_rows']} |")
(D/'classification.md').write_text('\n'.join(classification)+'\n')
extraction=['# Template extraction','','## 1. Specific source descriptions','']
for case in cases:
 spec=g.TEMPLATES[case['template']]
 extraction+=['### '+case['source_id'],'',f"Level {case['level']}; {case['template']}; {spec['solution_rows']} solution stages. Matrix/name/claims: `{json.dumps(case['parameters'])}`. Database keys: `{json.dumps(case['correct_original'])}`.",'']
extraction+=['## 2. Shared mathematical pattern','','Expand det=a(ei−fh)−b(di−fg)+c(dh−eg), evaluate the minors and signed products, compare the determinant with zero and test each of the three statements independently. A numeric determinant claim tests equality; singular tests det=0; nonsingular tests det≠0.','','## 3. Components and complete bank mapping','','Every statement label I/II/III owns exactly the text choices false and true. The correct choice is computed from that displayed statement, with no subset radio bank and no None option. All eight Boolean response combinations can be represented, although statement logic constrains which combinations can be correct. Matrix entries and determinant claims are exact parameters. source-cases.json maps all 17 questions to explicit normal-generator replay calls, including all 51 fields and 102 choices.','','## 4. Reusable template and constraints','','The prompt preserves the source question, Select all that apply, bold Roman bullet labels, and the named matrix. Fixed solution sentences and the five/six cofactor stages remain; evaluated products and conclusions are parameterized. Spaced and unspaced source bullet layouts remain distinct. Matrix values, determinant claims and computed intermediate equalities are independently parsed and checked.','','Easy uses signed integers. Moderate samples rational column scaling and one repeated radical family; explicit replay supports the observed mixed entry patterns. Hard requires nine nonzero entries with dense rational/repeated-radical scaling. Bounds and zero/nonzero determinant construction retain the previous same-KP sampling policy. Explicit invalid parameters fail; sampled invalid matrices or duplicate determinant claims reject the complete instance. There is no longer a rejection solely because a radio bank omitted the true statement subset.','','Identity includes generator version, displayed prompt, fixed solution and all Boolean fields; seed/order do not change identity. Mathematical fingerprints contain matrix values and statement predicates. Old basis-1356 captures and generator code are retained under history/basis-1356.']
(D/'template-extraction.md').write_text('\n'.join(extraction)+'\n')
(D/'plot-extraction.md').write_text('# Plot extraction\n\nAll practice matrices use LaTeX; the canonical image is unchanged numeric matrix notation. No parameter-dependent graph or diagram is required. Plot rating: none.\n')
(D/'README.md').write_text(f'''# Identifying Singular Matrices ({g.KP_ID})

Current source: math basis {source['basis']}. All 17 practice questions use three Boolean checkbox fields with bold I/II/III bullets and Select all that apply. Old artifacts are retained in history/basis-1356.

Easy and moderate retain their numeric determinant/singularity scopes. Hard retains the documented authored dense fraction/repeated-radical scope. Matrix sampling and fixed cofactor derivations are shared; no database writes or registrations occur.

Run from the repository root:

```sh
.venv/bin/python generate/scratch/{g.KP_ID}/build_evidence.py
.venv/bin/python generate/scratch/{g.KP_ID}/write_review.py
.venv/bin/python generate/scratch/{g.KP_ID}/validate.py
.venv/bin/python generate/scratch/{g.KP_ID}.py --difficulty all --seed 13 --count 2
```

The public generate function supports explicit parameters/template and checkbox field_type. The sole current profile is checkbox_I_II_III. Radio requests fail. recipes.json records the captured source basis and parameterized structures; source-cases.json covers every current question. Validation checks all 51 database keys, displayed mathematics, identities, and native field/whole-question grading.

Review records show originals, parameterized replays, two variants per source and two authored hard examples. Equivalent solution arithmetic typography and the two source bold repairs are documented separately from exact Boolean-bank fidelity. The native grader helper is in ../source-refresh-2026-10-12.
''')
print('Wrote current review:',len(records),'records')
