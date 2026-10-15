import sys;sys.dont_write_bytecode=True
import importlib.util,json,hashlib
from pathlib import Path
D=Path(__file__).resolve().parent;ROOT=D.parents[2]
spec=importlib.util.spec_from_file_location('draft',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def write(name,obj):(D/name).write_text(json.dumps(obj,indent=2)+'\n')
components=[]
for sid,q in g.SOURCES.items():
 p=g.params(q);a,b=p['A'],p['B'];row=a[p['row']-1];col=[r[p['column']-1] for r in b];answer=sum(x*y for x,y in zip(row,col));f=q[':question/answer-fields'][0];key=f.get(':answer-field/correct',{}).get(':answer/id')
 components.append({'source_id':sid,'record':q,'parameters':p,'field_type':g.typename(f),'row':row,'column':col,'ordered_products':[x*y for x,y in zip(row,col)],'independently_inferred_correct':answer,'correct_ref_present':key is not None,'source_mathematical_issue':'historical first-stage scalar equals full matrix product; mathematically imprecise and ineligible' if ':question/worked-solution' in q else None,'profile':'observed:'+sid,'choices':[{'source_answer_id':x[':answer/id'],'source_field_id':f[':answer-field/id'],'exact_value':x[':answer/value'],'correct_designation':x[':answer/id']==key if key else 'MISSING','recipe':'selected row dot selected column' if x[':answer/id']==key else 'opaque captured integer constant; evidence only; no inferred error intent','feedback_present':':answer/feedback' in x} for x in f[':answer-field/choices']]})
write('source-components.json',components)
write('canonical-evidence.json',{'basis':g.CAPTURE['basis'],'lineage':g.CAPTURE['lineage'],'role':'canonical example, not practice','record':g.SOURCE[':knowledge-point/canonical-example'],'image_inspected':'/home/jake/Developer/MA/DATA/Lessons/1196/Source/Sections/05-step-16189.png','selected_row':[1,2],'selected_column':[4,-2],'ordered_products':[4,-4],'answer':0,'source_mathematical_issue':'Historical first equation equates scalar entry c32 to full3x3 matrix product; imprecise, retained as source evidence only'})
write('source-mathematical-issues.json',{'practice_source_ids':[sid for sid,q in g.SOURCES.items() if ':question/worked-solution' in q],'canonical_source_id':'e-4407','issue':'Historical scalar entry equated to entire matrix product; mathematically imprecise and ineligible learner content','raw_policy':'All12 practice replays and canonical record preserved exactly, including two absent solutions','normal_repair':r'First RHS becomes \left([A][B]\right)_{ij}; remaining four stages unchanged','validation':'Actual printed operands, both dimensions, index admissibility and prompt target independently checked; wrong/missing/index-out-of-range/dimension mutations leave keys unchanged and are rejected'})
write('independent-inventory.json',{'basis':g.CAPTURE['basis'],'lineage':g.CAPTURE['lineage'],'questions':[]})
(D/'classification.md').write_text('''# Classification at math basis 2275

Primary source is the immutable refreshed wrapper `source.json`, lineage
01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1. All 12 practice questions carry MA IDs;
independent inventory is empty. Canonical e-4407 is separate evidence.

Ten originals are Easy (six radio, four blank); two are unrated radio originals
q-70791/q-70792. Their missing difficulty, worked solution and correct ref remain
absent in public raw replay. They have complete five-choice banks. The MA1196
captured widget confirms those same prompts/banks and does not supply a key.
Independent row-column evaluation gives12 and13 respectively; these are inferred,
not matched historical designations. Normal variants add authored Easy solutions
and keys through the same source-backed row-column procedure.

There is one mathematical backbone: select one cell of a compatible matrix
product and calculate its row-column dot product. Two-/three-term workloads,
radio/blank contracts, inline/display prompts and dotted/parenthesized products
are tracked separately. Twelve named masks preserve source prose/layout and eight
complete opaque radio-bank profiles; they are not twelve different skills.
Every source is mapped with all fields, choices and raw attribute presence in
source-components.json and source-cases.json. No feedback exists in these sources.

The ten stored practice solutions and canonical example contain a historical
scalar-equals-full-matrix-product error. Raw replays are explicitly ineligible;
normal solutions index that product at the requested cell before the same
row-column calculation. See source-mathematical-issues.json.

Plot rating: none. The canonical raster contains only typeset coefficient
matrices. It was inspected at full size and transcribed correctly in its captured
solution; changing matrices is handled as ordinary coefficient-matrix TeX.
No asset generation is needed.

The actual activity first-step/next chain is Introduction16186 → full matrix
product00872 → selected entry00873 → column-by-row outer product00913 → index
notation16188 (DB route IDs in reference/lesson.json). Prerequisite is
Conformability for Matrix Multiplication1198. The siblings assess all entries;
this draft always assesses exactly one scalar entry. There is no inverse,
equation solving, complex/fractional arithmetic or outer-product branch.

Missing Moderate/Hard are explicitly authored. Both retain the three-product
backbone, five solution rows and scalar radio/blank response. Moderate requires
three nonzero nonunit products each at most16 and L1 at most36. Hard requires the
same three products with mixed signs, product magnitudes at most30 and L1 37–58.
These increase signed arithmetic/collection workload within the observed ceiling
(two-term Easy30−28 already has L1=58). They do not claim observed MA labels.
''')
(D/'template-extraction.md').write_text('''# Four extraction stages

## 1. Specific originals

source-components.json contains every complete captured source record, explicit
A/B matrices, cell indices, field ID/type/key, answer ID/value, correct-ref
presence, inferred exact arithmetic and complete bank mapping. q-70791/70792 use
inline matrices and no stored solution/rating/key. q-130111/130120/70956 use
three-term dotted expansion; q-70946/70949/70958 use two terms. q-275547 is a
2-term dotted blank. q-318462/318463 are3-term parenthesized blanks; q-318470
is2-term parenthesized blank. Original dimensions range2–5 outer rows/columns
and2–3 inner dimension. All entries are integers; whole matrices include zero
and signed values through20; assessed factors through10, products through30,
L1 through58, bank magnitudes through58. These are coupled ceilings, not
independent coefficient boxes. No source feedback or answer fragments beyond
one scalar after the displayed cell notation occur.

## 2. Shared pattern and stable backbone

Supply two full matrices and C=AB. Request c_ij. State which row/column to
multiply; display both full matrices; extract the selected row and column;
expand the ordered scalar products; evaluate each signed product; collect to
one integer. Preserve all five aligned rows and source shared prose. One fixed
worked solution is generated independently of the learner's selected error.
The raw source first row equates a scalar to the full matrix product. This is
mathematically imprecise, not a valid scalar equality. Ten practice solutions
and the canonical example contain it; raw replay retains it as historical,
ineligible evidence. Normal output wraps the complete matrix product in
\\left(...\\right)_{ij}, explicitly selecting its scalar entry before extracting
the row and column. All five operative stages and shared prose remain. The
indices are derived from the actual requested cell in every normal record.

## 3. Components and banks

Every source choice is individually mapped in source-components.json. Historical
scalar wrong values do not determine their operations. Their public observed:
profiles retain opaque integer patterns, computed designated correct values and
raw omissions; they are evidence-only and never sampled for learning. This is
not a claim to recover error intent. No arbitrary polynomial fit is used.
All44 values across12 banks replay;10 historical keys match,2 are truly missing.

Normal five-choice profiles are separately authored complete operations:
method-omit-sign = [sum(products), sum(all but last), sum(abs(products)),
negative sum(products), sum(row)+sum(column)].
method-reverse-column = [sum(products), dot(row,reverse(column)), first product,
sum(all but first), dot(row,row)]. These represent omission, sign loss/reversal,
entry addition, reversed alignment and use of the row as both inputs. Blanks
retain their observed one canonical scalar and supplied cell-equals fragment.
Choose a whole profile before parameters. Compute every member; reject the
entire instance for any collision or magnitude>58. Never replace a single
invalid option or select first-valid errors. No distractor diagnosis is added
to learner content. Evidence flags are explicit on all opaque public replays.

## 4. Reusable masks, slots, domains and dependencies

Source shapes, field contracts and source label sets are fixed per mask.
A and B are whole-matrix slots with compatible source shape; row and column
independently range over every valid requested cell. The eligible target role
is any entry of this same product, not a source-fixed location. Target changes
update the prompt, supplied blank fragment, prose ordinals, selected row/column,
ordered factors/products and correct key together. Source missing solutions
receive the same common instructional prose only in authored normal records.

Normal sampling uses signed integer matrices−6..6. All public explicit inputs
obey the same ceilings: whole operands≤20, selected operands≤10, each assessed
product≤30, sum of assessed absolute products≤58, every bank member≤58.
At least two assessed products are nonzero. Easy3 has unit/zero support in at
least one factor pair; Easy2 retains two substantive products. Moderate/Hard
both require three terms and all six assessed factor magnitudes2..6. Moderate
requires each product≤16 and L1 12..36; Hard requires mixed product signs and
L1 37..58. Exact original profiles keep all observed raw parameters, with the
same global source ceilings but no authored-level guards. Invalid explicit
calls raise; random calls resample whole instances. No hidden expression branches.

IDs are computed after shared math_format normalization from actual prompt,
worked solution, difficulty, field contract and complete bank; order/seed/profile
alias cannot create an ID. Task fingerprints use ordered assessed row/column
vectors plus target relation and actual level, excluding irrelevant matrix
entries, labels, distractors and seed. Full irrelevant entries remain in content
identity. Large finite integer domains provide repeated practice:600 seeds yield
598/600/600 substantive tasks (not a claim of exhaustive enumeration). Slot
coverage and fixed-matrices/changed-target regressions are separate from this
count. Exact source replays reproduce the complete original strings through
parameterized masks rather than returning completed captured question payloads.
''')
(D/'plot-extraction.md').write_text('''# Plot extraction

No mathematical diagrams occur. Canonical e-4407's image contains ordinary
coefficient matrices A=[[1,2],[-2,0],[1,2]], B=[[3,4,-1],[1,-2,2]]. Full-size
inspection confirms row3[1,2], column2[4,-2], products4 and−4. The captured five-row
solution matches. Original practices all already contain TeX matrices. Draft
uses shared matrix_tex(..., augmented=False) and normalizes before IDs. No
parameter-dependent raster plot or new image asset is needed.
''')
(D/'README.md').write_text('''# Selected matrix-product entry draft

Only owned draft files were changed; the registered numeric script/tree/caches
are protected by registered-before.json and rechecked in validate.py. No EDB
writes, registration, engine edits or shared changes. Stop after generator step7.

Run from repo root:

```
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python generate/scratch/17592186100873-draft/validate.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python generate/scratch/17592186100873-draft/render.py
.venv/bin/python -B generate/scratch/17592186100873-draft.py --difficulty all --count 2 --format markdown
```

Browser rendering needs loopback permission; it uses local installed Chromium
and actual player routines/assets. Native private grader is copied from the
current59716 draft and42 actual source/dependency hashes are verified before/after.
Old shared grader is not used to establish results. Native scalar equivalents
and all displayed radio choices are tested separately from mathematical QA.
Wrong matrix-shaped blank submissions trigger48 documented unsupported-notation
errors; they are not accepted or counted as ordinary wrong-answer rejections.
Raw two missing-key sources cannot be graded and remain ineligible evidence;
normal inferred variants are complete and grade normally. Normal first-stage
matrix products explicitly carry the selected-entry index; raw scalar/matrix
equality errors remain flagged ineligible historical evidence. No valid scalar-answer
native failures are hidden. Moderate/Hard bounds are authored scope claims.
''')
review=['# Originals and generated variants','Raw originals retain absent keys, solutions and ratings. Historical opaque banks are evidence-only; normal banks are labeled authored method profiles.']
for c in components:
 sid=c['source_id'];raw=g.generate('easy',template=sid,profile='observed:'+sid);review+=['## Original '+sid,g.markdown(raw)]
 for level in (['easy'] if g.TEMPLATES[sid]['terms']==2 else g.LEVELS):
  for seed in (41,92):review+=['### Authored '+level+' variant '+str(seed),g.markdown(g.generate(level,seed,template=sid,profile=(g.PROFILES[0] if seed==41 else g.PROFILES[1]) if g.TEMPLATES[sid]['field_type']=='radio' else 'blank'))]
(D/'review.md').write_text('\n\n'.join(review)+'\n')
