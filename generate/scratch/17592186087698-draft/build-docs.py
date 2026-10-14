from pathlib import Path
import json,importlib.util,sys,hashlib
sys.dont_write_bytecode=True
D=Path(__file__).resolve().parent;spec=importlib.util.spec_from_file_location('g',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
components=[]
for sid,q in g.ORIGINALS.items():
 pf=g.ALIASES[sid];p=g.source_parameters(sid);fields=[]
 for f in q[':question/answer-fields']:
  choices=[]
  for a in f[':answer-field/choices']:
   value=a[':answer/value'];recipe=('direct named predicate '+g.LABELS[value]) if value in g.LABELS else ('exact selected subset '+','.join(__import__('re').findall(r'\$([A-Z])\$',value))) if '$' in value else 'boolean membership '+value
   choices.append({'source_answer_uuid':a[':answer/id'],'exact_value':value,'type':a[':answer/type'][':db/ident'],'recipe':recipe,'inferred_error_intent':None,'role':'stored correct' if f.get(':answer-field/correct',{}).get(':answer/value')==value else 'stored wrong' if ':answer-field/correct' in f else 'designation missing','replay_match':True})
  fields.append({'key':f[':answer-field/key'],'type':f[':answer-field/type'][':db/ident'],'complete_choices':choices,'stored_correct':f.get(':answer-field/correct',{}).get(':answer/value')})
 components.append({'source_id':sid,'template':g.PROFILE_TEMPLATE[pf],'profile':pf,'extracted_source_template':pf,'parameters':p,'source_prompt':q[':question/problem'],'source_solution':q.get(':question/worked-solution'),'difficulty':q.get(':question/difficulty'),'mathematical_features':[g.predicates(m) for m in p['matrices']],'fields':fields,'stages':['test each named shape predicate','summarize exact selected subset'] if len(p['matrices'])==3 else ['inspect structural/category defining predicates','state unique best name'],'plot_rating':'none'})
(D/'source-components.json').write_text(json.dumps(components,indent=2)+'\n')
classification='''# Classification

Immutable source/context wrappers: math basis 2275, lineage 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1. source.json, topic.json and lesson.json are byte copies of refresh-2026-10-14. The registered numeric script and every existing evidence file are listed with SHA-256 in registered-baseline.json and must remain unchanged. independent-inventory.json is the complete historical post-registration inventory at basis 2199, not a refreshed question snapshot. authority-widgets.json preserves the full original lesson capture.

Five practice sources are easy; q-7831 and q-7836 are unrated and omit correct designations and worked solutions. The original lesson widgets also lack keys/solutions; no widget evidence supplies an observed grade. No source is excluded. Public raw profiles preserve these absences and are ineligible for learning. Separate repaired profiles use independently derived F-only and Other keys and authored solutions.

| Backbone | Sources / complete profiles | Fields | Plot |
|---|---|---|---|
| Single best category; two-line display, shared category-specific solution | q-11563 row; q-126293 diagonal; q-7830 other | one radio, five text choices | none |
| Single best category; compact inline layout, absent key/solution | q-7836 legacy_other_raw / repaired | one radio, five text choices | none |
| Three row memberships, bullet solution then exact subset | q-68751 rows | three checkbox fields, false/true bank each | none |
| Three column memberships, bullet solution then exact subset; none instruction | q-126287 columns | three checkbox fields, false/true bank each | none |
| Three row memberships, five exact subset options, absent key/solution | q-7831 row_sets_raw / repaired | one radio, five text subsets | none |

There are seven extracted source templates and seven complete observed banks. The first table row contains three separate category-specific solution templates (row, diagonal, Other); the other four rows each contain one template. Classification retains each distinct solution sequence and bank. The executable uses four shared method dispatches and profile-specific layouts. Each original retains its profile, full field layout, all answer values and attribute-presence contract.

Row/column checkbox queries mean every true membership, including both memberships for 1x1. The subset radio asks for the exact true subset, not the best individual name. “Best describes” chooses the unique maximal true offered name: identity specializes diagonal/square, diagonal specializes square. Incomparable true names (e.g. singleton row and column; zero and square) reject the complete instance. This partial specificity rule is conservative interpretation of the wording, not recovered author code. Other means no taught category applies, so a square with no square option cannot silently become Other.

Canonical e-4393 explicitly recognizes one column. Follow lesson first-step 88517 then next chain: zero definitions → zero KP → square KP → tutorial 88523 (diagonal/identity/row/column definitions) → special-square KP → this KP. The tutorial includes I1 and explicitly permits zero diagonal entries. Next-topic matrix multiplication/triangular/index operations are excluded.

Moderate/hard have no observed labels. Authored inspection bands keep the same category definitions and field contracts: easy maximum dimension 1–6 (all originals), moderate maximum dimension 7–8 for EACH object, hard 9–10 for EACH object. Longer shapes require more visible counting/scanning, without matrix operations, larger scalar arithmetic or new classes. These labels are draft design judgments with substantial uncertainty; vector membership remains a narrow categorical skill. They are not psychometrically calibrated levels. All profile families remain available at every level. Extended three-object membership instances require at least one negative predicate and every negative queried row/column count to lie in the level band; this preserves an actual longer count in the rendered explanation. Easy retains all eight checkbox masks; extended levels retain every mask except all-true, with the same three-checkbox response contract. Singletons remain easy only. Public explicit parameters obey the same bounds as sampling.

No plots, external assets, matrix computations or learner-facing distractor feedback are required. Scalar magnitudes, labels, bank aliases, ordering and seeds cannot inflate semantic task capacity. Actual assessed shape/count and category predicates define the finite fingerprint.
'''
(D/'classification.md').write_text(classification)
extraction='''# Template extraction

## 1. Specific original descriptions

source-components.json records each source specifically: exact prompt/solution, original parameters and category features, complete fields and every choice's UUID/type/value, designated/undesignated role, direct predicate or exact subset recipe and replay result. Source order is retained for field layout, not assumed to be lesson order. Canonical examples support scope but do not enter seven-practice-question fidelity counts.

q-11563: nonzero 1x3 integer row A, radio row/zero/identity/square/column, single-row explanation then row conclusion. q-126293: 4x4 P, off-diagonal zeros, diagonal 1,1,-1,-1, radio diagonal/column-matrix/identity/Other/row, square + off-diagonal zero + not-all-one explanation, then diagonal conclusion. q-7830: nonzero 4x5 rectangular identity-like E, square/Other/identity/row/zero bank, no-special-name solution. q-7836: 6x4 rectangular identity-like M, row/zero/identity/Other/column bank, compact inline source, no solution or designation. q-7831: E 5x1 includes sqrt2, F 1x5, G 2x2; exact five subsets EF, EG, E, G, F; no solution/designation. q-68751: A 2x5, B 4x1, C 1x2; three false/true checkbox banks; one bullet per object with row count or opposite-vector description, then C-only conclusion. q-126287: A 1x2, B 3x1, C 2x2; same Boolean layout for column membership, B-only conclusion and none-unchecked instruction.

## 2. Shared mathematical pattern

Inspect supplied matrices using the tutorial's structural definitions. Supply a unique best offered category, exact row-vector subset, or each row/column membership. No arithmetic operations are performed on matrices. The response contract, categories and reasoning stage order form the backbone; arrays, names and shape/pattern slots provide variations.

## 3. Components and complete banks

All 37 source answer values in 11 fields are mapped individually in source-components.json. Classification choices directly denote a taught predicate; Other denotes failure of all taught names. Checkbox choices are false and true for the actual queried object's predicate. Subset recipes select exact index sets (0,1), (0,2), (0), (2), (1), then insert current names. Wrong subset/categorical choices are whole response meanings, not scalar perturbations. Their author psychology is not recoverable and is marked unknown. Fixed complete banks are selected before parameters; any absent correct option, repeated meaning or incomparable best candidates rejects the WHOLE question. No pooling or first-valid replacement is used.

Raw q-7831/q-7836 banks replay through generate with profile row_sets_raw / legacy_other_raw, preserving absent key/solution/rating. Derived profiles are distinct bank-state contracts and identities; their keys/solutions are authored, not matched source designations. All source fields and choices remain in raw evidence. There are no malformed source TeX repairs or mathematical corrections. normalize_prose and matrix_tex only apply shared UI presentation formatting; raw and normalized comparisons are counted separately (all seven original prompts match both).

## 4. Reusable template and slots

Fixed: one matrix + one five-choice classification radio OR three matrices + three checkbox fields OR three matrices + one five-choice subset radio. Checkbox keys/names remain A,B,C because those keys are the contract. The classification prompt uses the selected profile's layout. Three-object solutions test each matrix in order, describe a defining count or opposite-vector role, then summarize the actual true subset. Each rendered instance has one worked solution independent of the submitted response. The missing-source solution extends the observed bullet/check/conclusion structure; it is labeled authored.

Variable: single-letter matrix names (classification and subset only); matrix dimensions within the level inspection band; bounded exact integers, rational fractions and radicals (magnitude at most 12), interpreted exactly; zero/nonzero, all-one-diagonal/not-all-one-diagonal and off-diagonal patterns; row, column and general roles in each of the three positions; none/one/two/all membership where the original bank contract permits it. Easy checkbox variations support all eight Boolean masks; extended authored bands support the other seven masks and require their negative queried axes to be in band. The subset-radio bank supports only its five complete index subsets; empty/all/(1,2) reject instead of inventing options. Classification supports all tutorial names represented by that bank; an omitted name cannot be called Other. All counts, names, categorical stages, answers and summaries derive from the same displayed arrays.

Observed source parameters are retained exactly. Authored random samplers select representative taught categories with rows/columns sized for the chosen inspection band. Explicit parameters may use any bounded valid exact pattern and must satisfy the same unique-bank and level conditions. Singleton row/column/diagonal/square/zero/identity overlaps are checked by actual predicates, not mutually exclusive labels. Ambiguous radio instances reject. Easy checkbox singletons are valid, and zero/identity membership depends solely on the queried row/column criterion.

Fingerprint policy: classification includes actual ordered shape and categorical truth predicates; row membership includes each object's actual row count and single-column alternate-role flag, column membership includes actual column count and single-row alternate-role flag. Objects in three-matrix tasks are a sorted multiset, so object permutations cannot inflate capacity. Names, scalar magnitudes, complete banks and profiles are excluded from mathematical fingerprints; actual prompt, whole worked solution, complete bank, correct state and served difficulty are included in content identity. Entry magnitudes produce different presentations but cannot inflate semantic capacities. A positive vector alone remains categorically equivalent across bands. Each extended three-object instance therefore includes a negative queried count in band, separating whole assessed objects across normal levels. No psychometric ordering is claimed; validation checks zero whole-task overlap in the sampled levels.

Validation reads arrays and names from the actual prompt, uses independent SymPy predicates, checks every response and wrong pair by the source criterion, verifies full source solutions and generated stages, probes all binary 1x1/2x2 overlaps, all checkbox masks, transposed-role changes, finite shape/property representatives, all profiles and every authored level. Native grading submits every displayed answer ID to the memory-only real engine. No blank fields exist, so textual algebraic equivalent-entry checks are not applicable; categorical synonyms cannot be entered through radio/checkbox UI.
'''
(D/'template-extraction.md').write_text(extraction)
(D/'plot-extraction.md').write_text('# Plot extraction / specification\n\nAll seven originals and the canonical example use TeX arrays only. No plot appears in prompts, banks or solutions; plot rating is none. Shared matrix_tex preserves coefficient-matrix role and rectangular row structure. No plot renderer or assets are required. Steps 5 and 7 have no parameter-dependent graphics.\n')
(D/'README.md').write_text('''# Identifying Other Matrices isolated draft

Draft script: ../17592186087698-draft.py. Raw source/context are immutable basis-2275 copies. The registered numeric generator and its entire existing evidence tree remain untouched. No database reads/writes, registration, engine edits or commits are performed.

```sh
.venv/bin/python generate/scratch/17592186087698-draft/validate.py
.venv/bin/python generate/scratch/17592186087698-draft.py --difficulty all --seed 42 --count 2 --format json
.venv/bin/python generate/scratch/17592186087698-draft.py --difficulty easy --profile row_sets_raw --count 2 --format markdown
```

API: generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None); generate_easy, generate_moderate and generate_hard. Complete profiles are documented in classification.md; source-cases.json replays all seven originals through this public API. Raw missing-key profiles are evidence-only; repaired profiles derive keys/solutions independently. Names and exact TeX string matrices are the parameter contract. Explicit invalid requests fail.

Fidelity: 7/7 complete prompts/banks, 37/37 options; 9/9 stored designations and 5/5 existing complete solutions. Two missing designations/solutions remain absent in raw replays and are separately authored in repaired records. Moderate/hard are uncertain authored inspection bands 7–8 / 9–10, preserving every source field contract and classification method. No new linear algebra classes or operations.

validation.json separates fidelity, rendered mathematical checks, finite-domain probes and native categorical grading. review.json contains original records/replays and two variants of every profile at every level; review.md is the readable preview. registered-baseline.json verifies all registered files remain unchanged. artifact-hashes.json freezes private deliverables after validation; parent independent QA is still required.
''')
print('docs written',len(components))
