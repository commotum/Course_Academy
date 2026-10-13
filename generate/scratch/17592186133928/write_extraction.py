import importlib.util,json,sys
from pathlib import Path
ROOT=Path(__file__).parent
spec=importlib.util.spec_from_file_location('stokes',ROOT.with_suffix('.py'));g=importlib.util.module_from_spec(spec);sys.modules[spec.name]=g;spec.loader.exec_module(g)
parts=['# Template extraction — four stages\n\nFrozen math basis 1356; lineage and complete untouched source are in source.json.','## 1. Describe the sources\n\nAll 11 prompts request a scalar surface integral of curl, with supplied positively oriented closed parameterized boundary. Coordinates use t; field uses x,y,z. Excluding the terminal duplicated point does not alter the definite integral endpoints. Moderate polynomial arithmetic is on [0,1), [−1,0) or [−1,1). Hard uses full trigonometric cycles (πt on [−1,1), t on [0,2π)), plus the explicitly observed signed polynomial source. All fields are five-option radios; one historical duplicate and one unrated/missing-ref source are preserved raw. No images occur.','## 2. Generalize the family\n\nUse Stokes to turn the supplied curl flux into circulation, substitute every coordinate into the field, differentiate each coordinate, form the dot product, reduce it, integrate and evaluate both endpoints. This is the reverse of the sibling task that chooses a surface for a supplied line integral. Positive normal orientation is induced by increasing-t boundary traversal, not automatically upward.','## 3. Map every component and whole bank\n\nEach row below maps a source-owned option to an exact parameterized scalar pattern. Historical distractor intent is opaque. All raw banks are evidence-only; multiplying the field by c consistently multiplies each field-dependent stage/value by c. This is not a recovered wrong-operation interpretation. The entire original bank is retained, not mixed or filled from a pool. Full source prose and whole mathematical-component masks are in source-masks.json.']
for sid,q in g.SOURCES.items():
 level,rr,ff,lo,hi=g.FAMILIES[sid]
 parts+=['### '+sid+'\n\nObserved label: '+str(q.get(':question/difficulty','unrated'))+'; coordinates `'+str(rr)+'`; field `'+str(ff)+'`; interval `['+lo+','+hi+')`.','| Field | Source option UUID | Original scalar | Parameterized pattern | Designation |\n|---:|---|---|---|---|']
 for i,f in enumerate(q[':question/answer-fields']):
  for a in f[':answer-field/choices']:
   designation='missing ref' if ':answer-field/correct' not in f else ('correct' if a[':answer/id']==f[':answer-field/correct'][':answer/id'] else 'wrong')
   parts.append('| '+str(i)+' | '+a[':answer/id']+' | `'+a[':answer/value']+'` | `c*('+a[':answer/value']+')` | '+designation+' |')
 parts.append('Source solution: '+('absent; raw retains omission' if ':question/worked-solution' not in q else 'full theorem → coordinates → field substitution → formal/evaluated derivative → dot product expansion/reduction → integral, primitive and endpoints → final scalar. Full original row fragments are in the extracted masks, with exact source replay tested separately from correctness.'))
parts+=['''## 4. Reusable masks and authored variation

Raw fixed scaffold holds every shared source sentence, derivative, coordinate and interval. Complete field/vector/scalar RHS components are the variable slots, not short coordinate or basis-letter replacements. Unit scale removes an ordinary identity factor, so c=1 and changed c pass through the same slot recipe. Symbolic boundary and F(r) integral rows already refer to the parameterized field and are not scaled twice. Numerical integrands/primitives/endpoints are scaled as whole components. Scalar source-bank patterns scale with c and remain opaque/ineligible. The raw public API preserves the unrated source's absent difficulty/solution/correct ref and the legacy field's absent ref. No literal source payload-return or answer lookup branch exists.

Normal source-shaped families vary coordinate multipliers a,b,d and whole-field multiplier c, nonzero signed integers |value|≤3. Moderate bilinear b,d are further bounded by 2. The exponential family enforces d=b, keeping z−2y=0 along the boundary, so the original substitution simplification survives. Easy fixes d=1. All rules apply equally to explicit inputs and sampled ones. These broader same-method coefficients are authored bounds, not observed source-authoring rules.

Easy has no observed source. Its authored horizontal ellipse with field (−cy,cx,0) has two nonzero tangent coordinates and immediate sin²+cos² reduction. Moderate/hard retain observed per-family polynomial or full-turn trigonometric workload; the unrated π-angle, three-coordinate tangent gets an explicit authored hard assignment. No surface-selection, new theorem, non-elementary integration, or within-level progression is added.

Normal solutions share the original theorem and common prose, while their vector notation and additional formal/distributed/component endpoint stages are authored. This difference is disclosed: normal prose/stage layout is not falsely counted as raw-exact source replication. Every field substitution (including yz and exponential cancellation), coordinate derivative including zero, first dot-product distribution, reduced integrand, primitive and individually evaluated endpoints is independently checked from displayed math.

Complete method banks are fixed before parameters:

* Polynomial: correct integral; reversed boundary; integrate F(r)·r (coordinate instead of tangent); integrate sum of field components (omit tangent); integrate F(r′)·r′ (wrong field input). Values are actual results of these displayed-method operations.
* π-angle trig: correct; reverse; assume zero curl; first half interval; omit π chain factor in tangent.
* Unit-angle hard: correct; reverse; assume zero curl; first half interval; omit the 1/2 factor in squared-trigonometric identities. The other linear/cross terms integrate to zero over a full turn, so this final wrong operation doubles the correct scalar.
* Authored easy: correct; reverse; zero; half interval; omit π from the angular endpoint.

No diagnoses are invented in learner-facing output. Each complete five-value bank must be pairwise mathematically unequal. A collision/invalid value rejects the WHOLE instance; no first-valid replacement is allowed. Historical opaque banks do not become defaults. Sampling chooses a family/bank before coefficients and default family coverage is verified.

Content identity includes generator version, displayed difficulty, prompt, fixed worked solution and entire bank; random order/seed cannot change it. The mathematical fingerprint includes the actual parameterized curve, its traversal/interval and field, not profile/bank or spelling. Assessed curve derivatives and field substitutions make these coefficients substantive even when final scalars coincide.

No practice plot exists; plot extraction/specification and Matplotlib/TikZ rendering are consequently unnecessary (rating none). Tutorial diagrams were treated solely as lesson context. No figure or unrelated demand is introduced just to require a plot. Freeze after step 7; no database preparation/registration/transactions are performed.
''']
(ROOT/'template-extraction.md').write_text('\n\n'.join(parts)+'\n')
