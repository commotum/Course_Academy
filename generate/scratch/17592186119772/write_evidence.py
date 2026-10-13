import json,hashlib
from pathlib import Path
H=Path(__file__).resolve().parent;root=H.parents[2]
s=json.loads((H/'source.json').read_text());c=json.loads((H/'contract.json').read_text());v=json.loads((H/'validation.json').read_text())
caps={'generator_version':'triangular-recognition-v1','basis':s['basis'],'lineage':s['lineage'],'supported_levels':['easy','moderate'],'unsupported_levels':{'hard':{'supported':False,'available':0,'nominal_quota':5,'shortage':5,'reason':'This validated package covers direct inspection of complete numeric square matrices only. Six easy sources ask for one matrix; two moderate sources classify three matrices independently. No hard source or verified hard extension is present. Larger matrices or larger coefficients alone do not establish hard difficulty. Symbolic parameter conditions, matrix products, or transformed matrices introduce an unvalidated task or extra prerequisite and are excluded from this version. This is a bounded capability exception, not proof of mathematical impossibility. Reopen on new hard source evidence or a validated extension.'}},'finite_domain':'Each matrix independently maps distinct nonzero source-value groups injectively to the 22 integers in [-11,11] excluding zero. Zero locations, dimensions, equality relations and bank profile remain fixed. Sampling deduplicates complete mathematical tasks, ignores seed/identity/option order, and raises on a bounded search failure. No proven global exhaustion; current shortages are feasible.'}
(H/'capability.json').write_text(json.dumps(caps,indent=2)+'\n')
text=f'''# Classification

Math basis {s['basis']}; lineage `{s['lineage']}`. All eight current practice records and the canonical example are retained in source.json/source.edn. No registered generator or earlier target scratch package was present. The job's supplied .generated file was absent.

Six easy questions have one five-option radio field, key `selection`, containing full matrix values. Two moderate questions have three independent Boolean checkbox fields, A/B/C. No blank or mixed field layout occurs. Current fields, including the migrated checkbox layouts, take precedence over the historical radio captures at basis 1356. No source or learner facts are altered by this package.

Four Markdown/value templates: easy-upper single-recognition (five complete bank profiles), easy-lower single-recognition (one profile), moderate-upper three-matrix subset (one profile), moderate-lower three-matrix subset (one profile). Eight source matrix banks keep their distinct sizes, zero patterns, repeated entries and coordinate witnesses. Every source is assigned below. Each template has plot rating **none**: the inline TeX matrices are mathematical notation, not diagrams. The canonical lower-triangular example has an unchanged image, but it is context and is not sampled or counted as practice.

Hard is an explicit version-bounded unsupported band. Absence of hard sources is evidence requiring classification, not proof of impossibility. The retained capability exception explains the direct-recognition workload boundary. Its nominal shortage remains five, never filled.

| Source | Entity | Level | Field layout | Template | Bank profile |
|---|---:|---|---|---|---|
'''
for sid,p in c['profiles'].items():text+=f"| {sid} | {p['source_entity']} | {p['difficulty']} | {p['kind']} | {p['difficulty']}-{p['direction']} | {sid} |\n"
(H/'classification.md').write_text(text)
text='''# Template extraction

The task is to recognize a square matrix whose entries strictly below (upper triangular) or strictly above (lower triangular) the main diagonal are zero. Diagonal entries may be zero; signs and magnitudes of unconstrained entries do not change the property. Moderate requires classifying all three given matrices and is graded with three independent Boolean fields.

Numbers are exact integers, including negative values, zero diagonal entries, equal entries, symmetric-looking distractors, 2×2/3×3/4×4 dimensions, diagonal matrices, and single or multiple off-triangle violations. The script keeps every complete observed profile rather than mixing matrix choices across source banks. Distractors are entire matrices with witnessed nonzero entries in the forbidden triangle; no intent such as “wrong diagonal” is inferred. Contract.json retains every cell and full observed bank, every field key and correct designation, and each original ordered sentence/solution fragment.

Fixed components: target triangle, dimension per matrix, zero pattern, equality pattern, labels, field layout and source-specific bank. Variable components: nonzero integer value groups per matrix. Sampling bounds -11..11 include every observed source nonzero; both signs are sampled. Distinct source values remain distinct in a matrix; equal source values remain equal. These bounds are an authored finite sampling policy, not an inferred original distribution. No pivot/nonzero diagonal or invertibility restriction is imposed.

Each matrix placeholder expands to the complete labeled aligned matrix. Each solution witness is the exact entry at its original row/column, coupled to the displayed matrix. Single-matrix solution order is correct matrix → definition → all four contrasting matrices → conclusion. The moderate solution order is qualifying matrix/matrices → definition → nonqualifying matrix/matrices → one precise off-triangle witness per invalid matrix. Every sentence replays at original parameters.

Some imported radio choice math contains doubled TeX command and row escapes while the canonical correct value and solution use single escapes. Generated choice presentation normalizes one doubling layer; this is reported separately from complete matrix-bank equality and does not rewrite source records. No mathematical source error or unresolved bank comparison remains.

## Each source and every bank component

'''
source={q[':question/math-academy-id']:q for q in s['record'][':knowledge-point/questions']}
for sid,p in c['profiles'].items():
 q=source[sid];text+=f"### {sid}\n\n{q[':question/problem']}\n\nObserved labeled matrices and all exact cell values:\n\n```json\n"+json.dumps(p['matrices'],indent=2)+'\n```\n\n'
 for f in p['fields']:
  text+=f"Field `{f['key']}`: {f['type']}; correct recipe `{f['correct']}`. Complete bank:\n\n"
  for a in f['choices']:text+=f"- `{a['type']}`: `{a['value']}`. "+('Reconstruct the complete labeled matrix from its grouped entries; correctness is strict-triangle zeros.' if p['kind']=='radio' else 'Fixed Boolean text; correctness is the independent matrix predicate for this field label.')+'\n'
 text+='\nOriginal worked solution:\n\n'+q[':question/worked-solution']+'\n\n'
(H/'template-extraction.md').write_text(text)
(H/'plot-extraction.md').write_text('''# Plot requirements

Rating none for all four templates. Current source practice matrices occur as TeX in prompt or options; no practice image occurs. Matrix notation requires no generated plot. The canonical-example image is unchanged source context and is not used in generated instances. Therefore stages 5/7 require no renderer, publication, asset hashes or new files in the image store.
''')
review='# Original and generated review\n\n'
replays=json.loads((H/'source-replay.json').read_text());variants=json.loads((H/'review.json').read_text())
for r in replays:
 sid=r['generation']['template'];q=source[sid]
 review+='## Original '+sid+'\n\n'+q[':question/problem']+'\n\n'+q[':question/worked-solution']+'\n\nOriginal complete fields:\n\n```json\n'+json.dumps(q[':question/answer-fields'],indent=2)+'\n```\n\n'
 for record in [r]+[z for z in variants if z['generation']['template']==sid]:
  mq=record['question'];review+='### Replay or parameter variant; seed '+str(record['generation']['seed'])+'\n\n'+mq[':question/problem']+'\n\n```json\n'+json.dumps(mq[':question/answer-fields'],indent=2)+'\n```\n\n'+mq[':question/worked-solution']+'\n\n'
(H/'review.md').write_text(review)
(H/'README.md').write_text('''# Identifying triangular matrices

Run `.venv/bin/python generate/scratch/17592186119772/validate.py` for source fidelity, independent displayed-math checks, deterministic replay, parameter boundaries and native engine grading. Run `.venv/bin/python generate/scratch/17592186119772.py --difficulty moderate --count 3 --seed 42 --format json` for previews. Easy and moderate are supported; hard raises a bounded capability exception. Generator identity is stable under the KP UUID; database registration reuses a preexisting identity if found.

Source.json/source.edn retain current immutable evidence. Contract.json maps all eight profiles and complete fields. Classification, template extraction and capability.json document source fidelity, grouped entry recipes, observed vs authored constraints and hard shortage. Review.md juxtaposes originals, exact parameter replays and two variants per profile. No source, learner, scheduler or other KP changes are made.

`replenish.py` rechecks native inventory under api.lock, batches content/identity reads at that basis, validates and deduplicates missing supported questions, retains exact EDN and requests, previews with deployed native predicates, commits with a basis guard, and verifies content, attribution and source retention at the receipt basis. Preparation and receipts live under this package's reference/replenishment folder.
''')
files=['source.json','source.edn','contract.json','validate.py','validation.json','engine-input.json','engine-report.json','source-replay.json','review.json','classification.md','template-extraction.md','plot-extraction.md','capability.json']
freeze={'generator_uuid':__import__('uuid').uuid5(__import__('uuid').UUID('b55b50a0-034f-57c0-8a61-883cfb0412dc'),'question-generator').__str__(),'generator_sha256':hashlib.sha256(H.with_suffix('.py').read_bytes()).hexdigest(),'hashes':{f:hashlib.sha256((H/f).read_bytes()).hexdigest() for f in files},'validation_passed':v['passed'],'source_basis':s['basis']}
(H/'freeze.json').write_text(json.dumps(freeze,indent=2)+'\n')
