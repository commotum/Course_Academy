import sys
sys.dont_write_bytecode=True
from pathlib import Path
import importlib.util,json,hashlib,shutil
D=Path(__file__).resolve().parent;R=D.parents[2];sp=importlib.util.spec_from_file_location('analysis00869',D.with_suffix('.py'));g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g)
rows=[];components=[]
for t,q in g.SOURCES.items():
 p=g.source_parameters(t);labels=[m[1] for m in g.MAT.finditer(q[':question/problem'])];dims=list(map(g.shape,p['arrays']));products=[''.join(labels[i] for i in pair) for pair in p['products']]
 rows.append('| '+t+' | '+g.source_level(t)+' | '+', '.join(f'{n}: {r}×{c}' for n,(r,c) in zip(labels,dims))+' | '+', '.join(products)+' | '+', '.join(f[':answer-field/correct'][':answer/value'] for f in q[':question/answer-fields'])+' |')
 components.append({'source':t,'labels':labels,'arrays':p['arrays'],'dimensions':dims,'ordered_products':products,'prompt':q[':question/problem'],'solution_stages':q[':question/worked-solution'].split('\n\n'),'fields':[{'key':f[':answer-field/key'],'type':f[':answer-field/type'],'choices':f[':answer-field/choices'],'correct':f[':answer-field/correct'],'recipes':{'false':'The requested ordered left-column count does not equal the right-row count.','true':'The requested ordered left-column count equals the right-row count.'}} for f in q[':question/answer-fields']]})
(D/'source-components.json').write_text(json.dumps(components,indent=2))
table='| MA ID | observed level | displayed shapes | ordered products | I, II, III keys |\n|---|---|---|---|---|\n'+'\n'.join(rows)
(D/'classification.md').write_text('''# Classification

Immutable math basis 2275, lineage 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1. `source.json` is byte-identical to the full refreshed capture wrapper. There are ten MA-identified practice questions: seven easy and three moderate. No independent inventory or hard source exists. The canonical e-4403 is context, not practice.

Every practice question has three separate checkbox fields I, II, III, each with exactly two text choices `false` and `true`. All 30 fields, 60 choices, and 30 correct designations are retained. This is a finite-subset response: each unselected statement submits its explicit false entity; no radio migration is permitted.

One mathematical family reads three displayed matrices and checks three ordered products. Layout profiles retain single-spaced bullets, blank-separated bullets, or the q-42374 unbulleted source list. Ten source template IDs preserve their exact opening punctuation, vector roles and layout; these are layout/role profiles, not ten distinct mathematical skills. Easy has six ordinary-array profiles and one column-vector profile; moderate has one-row-vector and two-row-vector profiles. All plot ratings are **none**: arrays and factor annotations are typeset mathematics, not plots.

'''+table+'''

Authored hard adds one row vector, one column vector and one ordinary nonsquare matrix. The two vector orders are both assessed and vector lengths differ, so the learner must keep the inner dimensions in their ordered roles. The third comparison remains the same rule. No output dimensions, entries of products, variable dimension equations, or extra operation is assessed.
''')
(D/'template-extraction.md').write_text('''# Four extraction stages

## 1. Specific source descriptions

'''+table+'''

All actual source arrays, every Boolean bank member and designation, complete prompt strings, and individual solution paragraphs/annotation stages are transcribed in `source-components.json`. Entries include signed integers, zeros, q-42374's literal -0, rectangular arrays, square arrays, row vectors and one easy column vector. Entry values never affect conformability and are excluded from task counts.

q-22063 has a final column vector and an opening without a period. q-129437 has two row vectors, trailing opening whitespace, and singular “row” in its first comparison. q-22062 has two row vectors and singular “row” in its second comparison. q-42381 has a final row vector and the source grammar “1 rows”. q-42375 has its original comma outside the final math delimiters in stages II and III. q-42374 has a trailing matrix-list comma, singular “statement”, and three plain lines which Markdown collapses in the real player. These details are preserved in raw replay and separately normalized only where documented for normal learning.

## 2. Shared pattern and purpose

Read the row and column counts of each supplied array. For three requested **ordered** products, compare the number of columns of the first factor with the number of rows of the second. Select precisely the true statements using three Boolean checkbox fields. The solution identifies all three dimensions, gives the left-column/right-row counts in prose for each ordered pair, states equality or inequality, prints both factors in order with dimensions and check/inequality annotations, boxes both equal inner dimensions, and concludes the complete true/false subset.

## 3. Components and complete banks

The prompt has a display containing three named bmatrices, a shared question sentence, the three product statements and the selection instruction. Each field owns distinct false/true answer UUIDs and a single correct lookup ref. Both Boolean options are real bank members; false is not omitted just because its checkbox is unchecked. A true member means left columns = right rows; false means inequality. There is no opaque numeric distractor inference and no choice pooling.

`source-components.json` maps each captured answer entity one-to-one to its field, exact value, correctness and rule. `source-cases.json` records original arrays and ordered pairs for every MA source, through normal public generate API with raw profile. At anchors both prompt and full solution match original strings byte-for-byte. Identity UUIDs are generated local identities, not copied database entities.

## 4. Reusable backbone, slots and fixed roles

Fixed: three supplied arrays, three distinct ordered pairs of different supplied arrays, three independent checkbox fields, two text answers per field, three full ordered-comparison stages and one complete conclusion. Three comparisons are fixed to preserve source workload; self-products are excluded because the observed role is comparison of two different supplied factors. The source names are retained as aliases, not counted as variety. There is no additional learner-facing distractor diagnosis.

Variable slots: each full array is rectangular and its dimensions are jointly bounded; entries are integers -9..9 and incidental; each full requested ordered factor pair varies among the six pairs without repetition, changing every dependent prose and factor annotation together. Source role/layout profiles retain their specific row/column-vector positions. Easy normal ordinary shapes use dimensions 2..4; q-22063 retains the third column-vector slot with length 2..4. Moderate normal ordinary dimensions use 2..5, at most20 cells, and row-vector lengths 2..5 in the source positions. Hard has exactly one row vector and one column vector of unequal lengths 2..5 and a nonsquare ordinary array with dimensions 2..5, at most20 cells; their label positions vary. Both vector orders and one other ordered pair are requested, in any statement order. These are equal-workload instances within each level, with no progression inside a level.

All normal and explicit inputs use the same role, dimension, entry and product guards. Raw evidence profiles retain original grammar and source number forms but remain bounded to dimension maximum5 and20 cells. Complete Boolean profiles are chosen before shapes/entries; every required option is always computed together. Any invalid array, role, repeated pair, unsupported profile or dimension is rejected as a whole. No subset fallback exists.

Meaningful task fingerprint includes the supplied shape multiset and the multiset of requested ordered factor-dimension pairs; it excludes names, array order, statement order, entries, seed, layout aliases and Boolean bank. Ordered factor roles are retained inside each comparison. Content identity includes normalized actual prompt, fixed solution, all Boolean banks/designations, version and level. Replaying fixed parameters with another seed returns the same question identities. Easy and moderate domains are disjoint by orientation roles (easy column-vector exception retained); hard requires both vector orientations and their ordered contrast. Canonical meaningful task counts are easy4542, moderate11040, hard576, exhaustively enumerated in semantic-catalog files. The larger ordered-presentation counts are explicitly separate in domains.json.

The authored hard rationale comes from e-4403's ordered AB/BA contrast, observed row/column-vector recognition, and prerequisites Introduction to Matrices and Multiplying Square Matrices. The linked activity route is first-step 17592186101674 →17592186101747 →17592186101675 (this KP) →17592186101676 (00870) →17592186101677 (00871), read from next links. The following siblings ask product dimensions from given dimensions or actual arrays; that assessed result is deliberately excluded here. The tutorial capture has omissions in generic dimension notation and repeated array images, so canonical and verified practice establish the recognition rule instead of inventing missing content.
''')
(D/'plot-extraction.md').write_text('''# Plot assessment

Rating none. All ten practice prompts contain recoverable bmatrix mathematics and no raster plots. Solutions contain symbolic ordered-factor dimensions and boxed inner counts. No new diagram renderer is required.

The canonical example has raster typeset arrays. Both original assets were inspected at native resolution: A=[[19,2],[sqrt(2),-1]], B=[[1,2,-1],[-1,1,2]], so A is2×2 and B is2×3. AB is conformable, BA is not. These assets establish context only and are never copied into parameterized practice.
''')
errors={'mathematical_errors':[],'missing_fields_or_keys':[],'field_contract_migrations':'Already Boolean checkbox in basis2275; preserved unchanged.','presentation_findings':[{'source':'q-42374','raw':'Plain adjacent I/II/III lines collapse in the actual Markdown player; singular statement grammar.','normal_repair':'Render the same three statements as separate bold Roman bullets and use statements.','mathematical_change':False,'raw_profile_retained':True},{'source':'q-42381','raw':'1 rows; raw retained exactly.','normal_repair':'Singular row/column inflection is derived from actual counts.','mathematical_change':False,'raw_profile_retained':True}],'fidelity_denominators':{'raw_questions':10,'normalized_questions':10,'mathematical_repairs':0,'complete_boolean_banks':30,'choices':60,'correct_designations':30},'unresolved':[]}
(D/'source-errors.json').write_text(json.dumps(errors,indent=2))
(D/'domains.json').write_text(json.dumps({'easy':{'meaningful_tasks':4542,'ordered_presentations':116640,'formula':'9^3*120 + 9^2*3*120','ordinary_dimensions':'2..4','column_vector_exception':'q-22063 final array length2..4'},'moderate':{'meaningful_tasks':11040,'ordered_presentations':165600,'formula':'(15*4^2*2 + 15^2*4)*120','ordinary_shapes':15,'row_lengths':4,'ordinary_dimension_bound':'2..5, rows*columns<=20','vector_role_profiles':[[False,True,True],[True,True,False],[False,False,True]]},'hard':{'meaningful_tasks':576,'ordered_presentations':20736,'formula':'6 label placements *12 unequal vector-length pairs *12 ordinary nonsquare shapes *24 ordered statement profiles','lengths':'2..5','matrix_cell_cap':20,'product_roles':'both row-column and column-row plus one of the four other ordered pairs, permuted'},'all':{'entries':'integer -9..9 incidental','arrays':3,'statements':3,'self_products':False,'response_contract':'3 Boolean checkbox fields; complete true/false subset','normal_and_explicit_guards':'identical','numeric_baseline':'absent before and after imports'}},indent=2))
(D/'README.md').write_text('''# Conformability checkbox draft

Script: `../17592186100869-draft.py`. Review only; stop after step7. No DB registration or mutation. The numeric baseline did not exist before import and remains absent. The latest candidate inventory records has_generator=false; proof is in `numeric-before-import.json` and `reference/registration-evidence.json`.

Run from repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B generate/scratch/17592186100869-draft/validate.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B generate/scratch/17592186100869-draft/whole-question.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B generate/scratch/17592186100869-draft/render-preview.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B generate/scratch/17592186100869-draft/freeze.py
```

Chrome rendering needs the permitted local process escalation in restricted environments. It reads frozen actual UI only. CLI supports difficulty/seed/count/format/template/profile; JSON output is a bare list. Raw source profiles require explicit public API parameters from source-cases and are flagged evidence_only/ineligible. Normal levels use complete Boolean banks, retain source solution stages and vary actual array shapes and ordered requested products. Authored hard contrasts vector orientations without asking product dimensions.

`source-fidelity.json` separates full original strings/banks/keys; `validation.json` checks displayed mathematics and identity; `engine-report.json` checks both false/true members through the current native grade_field; `whole-validation.json` checks all eight finite subsets plus missing/extra fields through native grade; `render-validation.json` maps full screenshots to exact generated records/hashes and tests actual UI checkbox controls/collectResponses for all eight subsets. Source discrepancies and minimal normal presentation repairs are in source-errors. No mathematical source errors or unresolved grading issues remain.
''')
for h in ['5357fcb0ec150699b4d50cbd6fa9651c421ac3500660703396146362160328a2','63d354773d145f05e73e808efe2a21164cb28d6ff19ae104d6bbde6510cf10e6']:
 p=Path('/media/jake/SSD/EDB/math/images')/h[:2]/(h+'.png');shutil.copyfile(p,D/'reference'/(h+'.png'))
