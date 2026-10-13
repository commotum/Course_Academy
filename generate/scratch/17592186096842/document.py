"""Write the extraction audit and full one-to-one source choice map."""
from pathlib import Path
import importlib.util,json
root=Path(__file__).parent
s=importlib.util.spec_from_file_location('validate',root/'validate.py');v=importlib.util.module_from_spec(s);s.loader.exec_module(v);g=v.g
raw=json.loads((root/'source.json').read_text());qs={q[':question/math-academy-id']:q for q in raw['record'][':knowledge-point/questions']};cases=json.loads((root/'source-cases.json').read_text())
classification='''# Classification

Immutable provenance: math, basis 1356, lineage 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1. `source.json` is a byte-preserving copy of the captured wrapper. All nine practice questions are included; the canonical e-182 is context only.

| Observed level | Fields | Practice sources | Markdown/value layouts | Complete banks | Plot rating |
|---|---|---:|---:|---:|---|
| easy | one radio / one blank | 2 | 2 | 2 | none |
| moderate | one radio / one blank | 4 | 4 | 4 | none |
| hard | one blank | 2 | 2 | 2 | none |
| absent / unrated | one radio | 1 | 1 | 1 | none |

The unrated q-48846 is explicitly assigned moderate, alongside the observed linear-square-root radio q-107291. Its numeric demand and five-choice layout are comparable. This assignment is authored, not a recovered source rating. The two reciprocal blank sources retain distinct extracted notation scaffolds (braced closing parenthesis in q-314194); their mathematics and stage order agree. The hard source label for linear q-342683 is retained despite its simpler algebra. No within-level progression is inferred.

Lesson route was reconstructed from activity/first-step and step/next: Introduction → polynomial raised to a power KP17592186096841 → this radical KP17592186096842 → prime notation tutorial → prime notation KP17592186096843 → derivation of the chain rule. This generator retains Leibniz notation and radical/reciprocal-radical outer powers ±1/2. It never introduces arbitrary integer outer powers, prime notation, tangent equations, logarithmic/exponential/trigonometric functions or multiple nested chain applications. Prior polynomial differentiation and fractional powers are used exactly as in the canonical and practice solutions.

There are no graphic references, mathematical plots or parameter-dependent visual assets in these sources. Steps 5 and 7 therefore require no renderer; standalone TeX is not a plot.

The authoritative q-48846 widget was inspected at `/home/jake/Developer/MA/DATA/Lessons/1108/Source/1108.json`, Question 4, and the matching Markdown at 1108.md. It confirms the five choices and single radio. It too lacks a recorded correct designation and worked solution. The derivative 4/(2√(4x−3)) = 2/√(4x−3) independently identifies its correct choice. The absent designation is a repair, never counted as an original designation match. Its solution is authored using the captured chain-rule stages.
'''
(root/'classification.md').write_text(classification)
extraction='''# Template extraction

## Stage 1: specific source descriptions

Each row below names the exact original parameter pattern and field. Prompts, UUIDs, every original bank and raw solutions remain in source.json and review.md; none are omitted. A blank always expects only the derivative RHS or scalar slope, because the left side and/or surrounding sentence already appears in the prompt.

| Source | Parameters | Outer / inner | Response / level |
|---|---|---|---|
'''
for c in cases:
 s=g.TEMPLATES[c['template']];extraction+='| '+c['source_id']+' | `'+json.dumps(c['parameters'])+'` | '+s['family']+'; degree '+str(s['degree'])+' | '+s['field']+(' scalar slope' if s.get('slope') else ' derivative RHS')+'; '+c['level']+(' (authored unrated repair)' if c['repairs'] else '')+' |\n'
extraction+='''
## Stage 2: generalized method and purpose

Write u as the radicand, express y as u^(1/2) or u^(−1/2), compute dy/du and du/dx separately, multiply, then substitute u back. Evaluated slope prompts additionally substitute the displayed x value. The hard quadratic blank retains the explicit factor-of-two cancellation stage; the hard linear blank retains the symbolic chain product followed by the numeric inner derivative. Reciprocal blanks retain a product row, a simplified u row and a substituted radicand row. These fixed stages are independent of chosen errors.

## Stage 3: components and complete banks

Fixed prose, paragraph separators, display blocks, final periods, field placement and source-specific punctuation are in templates.json. Variable components are the function, radicand, exponent rewrite, both derivatives, product rows and optional substitution rows. All these mathematical components are calculated. UUIDs below are raw evidence IDs; newly authored record IDs are field-owned UUIDv5 values.

Empirical source banks are explicit-only profiles. They retain an underdetermined expression shape without pretending it is a recovered cognitive error or authoring algorithm. In particular −3/u in q-48730 is a fixed empirical numerator over the varying radicand. The scalar shapes −5/√u(t), 1/√u(t), √u(t)/a and −a/2 in q-107360 reproduce its full bank; their intent is unknown. These parameterized recipes can generate variants through the normal API, but never enter default bank selection.

Observed operation shapes are also hypotheses about intent. `source_spaced` reverses the constant in two options, omits the inner derivative in two options and omits 1/2 in one option. `source_constfirst` uses −1/(2a√u), a/(2b√u), −a/√u and sign(a)/(2√u). The a/(2b√u) option is a parameterized constant-as-divisor shape; the original one example does not establish author intent.

Default radio bank is a separately labeled complete authored bank: correct result, omit du/dx, reverse derivative sign, omit the factor 1/2, and fail to lower the outer exponent. Formally, with e=±1/2, these four wrong operations yield e*u^(e−1), −e*u^(e−1)*u′, 2e*u^(e−1)*u′, e*u^e*u′, evaluated at t if required. Every member is selected together; if any collision or invalid member occurs, the entire instance is rejected. No first-valid distractor pool is used. Blank fragments have no distractor bank.

### Full original choice map

'''
mapping=[]
for c in cases:
 rec=g.generate(c['level'],template=c['template'],parameters=c['parameters'],profile=c['bank_profile']);field=rec['question'][':question/answer-fields'][0];of=qs[c['source_id']][':question/answer-fields'][0]
 extraction+='#### '+c['source_id']+' / '+c['template']+' / '+c['bank_profile']+'\n\n'
 extraction+='Original field `'+of[':answer-field/id']+'`, key `'+of[':answer-field/key']+'`, type `'+of[':answer-field/type'][':db/ident']+'`.\n\n'
 for a in of[':answer-field/choices']:
  matches=[b for b in field[':answer-field/choices'] if v.equal(v.displayed(a[':answer/value']),v.displayed(b[':answer/value']))];assert len(matches)==1
  b=matches[0];recipe=rec['generation']['recipes'][b[':answer/value']]
  designated=of.get(':answer-field/correct',{}).get(':answer/id')==a[':answer/id']
  row={'source_id':c['source_id'],'source_field_uuid':of[':answer-field/id'],'source_answer_uuid':a[':answer/id'],'source_value':a[':answer/value'],'original_correct':designated if ':answer-field/correct' in of else None,'recipe':recipe,'profile':c['bank_profile'],'generated_value':b[':answer/value'],'full_value_equivalent':True}
  mapping.append(row)
  extraction+='- `'+a[':answer/id']+'`: $'+a[':answer/value']+'$ → `'+recipe+'`; '+('original correct' if designated else ('original incorrect' if ':answer-field/correct' in of else 'original designation absent'))+'; full expression matched.\n'
 extraction+='\n'
extraction+='''## Stage 4: reusable templates and domain/sampling policies

The extracted scaffold is parameterized at mathematical-component boundaries, not by returning a source payload or selecting prewritten answers. `extract.py` freezes the prose and TeX block placement, and `blocks()` independently constructs every mathematical chunk from integer parameters. All eight existing solutions and nine existing prompts replay exactly at their source parameters; full value equivalence handles harmless bank notation differences. There is no seed-specific source branch or answer lookup table.

Explicit parameter dictionaries must have exactly a,b for linear templates; a,b,c for quadratic templates; and t for slope templates. Noninteger inputs, zero leading coefficients, invalid slope domains and colliding complete banks raise errors rather than silently resampling. For learner output the mathematical domain is u(x)>0; it is recorded outside content, not inserted into source prompt text. Positive domains ensure both square-root derivatives and reciprocal radicals exist. Numeric slopes require u(t)>0, a perfect-square radicand and u′(t)≠0, including explicit parameter calls. Quadratic templates require c=0 to preserve the observed two-term structure. Source c=0 remains valid and is the default quadratic structure.

Authored variation policy, not recovered source code:

- Linear derivative templates use signed leading coefficients with magnitude 2–8 and nonzero constants −12…12: 336 initial parameter combinations per layout, before whole-bank rejection. Both constant-first and x-first source styles remain available.
- Quadratic derivative blanks use a=1…5, b∈−12…12 excluding zero, c=0: 120 parameter combinations. This keeps the observed two-term quadratic and the source cancellation workload; no additional algebra branch is introduced.
- Linear square-root slope radios use |a|=2…8, t∈{−3,−2,−1,1,2,3}, and r=2…9, then b=r²−a*t: 672 initial combinations. Perfect-square radicands retain rational slope arithmetic as in the easy original.
- Quadratic reciprocal slope blanks sample the 114 enumerated tuples with a=1…6, |b|=1…24, c=0, |t|=1…4 and matching signs of b,t, restricted to u(t)=r² for integer r=2…12. Positive and negative t are coordinate reflections with the same rational arithmetic and chain-rule workload. The source tuple a=3,b=12,t=2 is included. Every default therefore retains the original perfect-square radicand and rational slope; no radical simplification branch is added. Both easy templates require one application of the chain rule and one evaluation, despite different source algebra.

All three levels are directly observed. No missing-level expansion or new function skill is required. The authored extensions consist of parameter bounds, moderate assignment/solution/designation for q-48846, and operation-derived default radio banks. All original empirical profiles remain retained and explicitly labeled.

Deterministic identity includes generator version, template, parameters, domain, profile, displayed prompt, complete sorted bank, fixed solution and field layout. UUIDv5 answers are owned by their field's question content. Seed and answer order are excluded. A separate parameter fingerprint uses canonical expanded radicand, outer exponent, evaluation point, response kind and positive domain, independent of layout/profile/difficulty, to deduplicate the same mathematical task across profiles and notation. Changing the displayed bank changes content identity.

## Source findings and repairs

q-48846 lacks difficulty, solution and correct ref in EDB. Authoritative captured widget confirms layout and choices but cannot recover the missing designation. Independent differentiation repairs it; validation reports 8/8 existing designation matches and 1 authored designation. It does not claim 9 original designations matched. No source mathematical errors were found. Source empirical distractor intent remains unresolved, explicitly constrained to replay profiles. This is an interpretation limit, not a hidden missing bank.

## Validation and review

`validate.py` parses displayed TeX through an independent recursive grammar, differentiates the displayed polynomial mathematically, and verifies all answer values and every displayed derivative/product/substitution stage. It tests full-bank one-to-one source correspondence, exact prompt/solution scaffolds, all template/default combinations, collisions, invalid explicit inputs, stable UUID/content identity and variation counts. `engine-input.json` sends all reviewed radios through every choice and all blanks through canonical, equivalent, independently unreduced/expanded-cubic-radical, wrong-sign, omitted-half and zero entries. A separate domain-equivalent fractional-power probe is reported as a failed acceptance capability, not counted as a supported equivalent success or wrong-answer rejection. The mathematical equivalence holds on the positive-radicand question domain; the native grader currently lacks that context. `engine-report.json` uses the real native grade_field. `review.md` and `review.json` show every raw original plus source replay, two variants of every original template/bank and two defaults per template. `validation.json` separates fidelity, mathematical correctness, source repairs and native grading.
'''
(root/'template-extraction.md').write_text(extraction);(root/'choice-map.json').write_text(json.dumps(mapping,indent=2)+'\n')
(root/'plot-spec.md').write_text('# Plot extraction\n\nAll nine practice prompts, every choice, all eight captured solutions and the canonical example have no plot references or diagrams. Rating: none. No variable plot assets are required. No renderer is implemented.\n')
(root/'README.md').write_text('''# Radical chain rule generator

Run from repository root:

```sh
.venv/bin/python generate/scratch/17592186096842/validate.py
.venv/bin/python generate/scratch/17592186096842.py --difficulty all --seed 42 --count 2 --format json
```

All nine source questions and all three observed levels are supported. Original complete banks are explicit profiles; radios default to authored whole operation banks. Scope: square-root/reciprocal-square-root outer functions, linear/two-term quadratic radicands, Leibniz differentiation or slope evaluation. No plots, registrations or database writes. q-48846's missing level, correct ref and solution are documented repairs. Unresolved empirical distractor intent is preserved as evidence; defaults do not use it.

See classification.md, template-extraction.md, choice-map.json, source-cases.json, review.md/json, and validation.json. templates.json contains reusable prose scaffolds, never source answer payloads. Re-extraction uses extract.py; regenerate documentation with document.py. The native grader binary path and digest are recorded in validation.json. Canonical and expanded-cubic-radical equivalent blanks are tested. A mathematically correct fractional-power alternate receives an unresolved-domain error from the current native grader; this failed acceptance capability is reported separately in engine-domain-probe-report.json and never counted as wrong-answer rejection.
''')
