import importlib.util,json,pathlib,sys
sys.dont_write_bytecode=True
D=pathlib.Path(__file__).resolve().parent;spec=importlib.util.spec_from_file_location('kp64246',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
(D/'independent-inventory.json').write_text(json.dumps({k:g.CAPTURE[k] for k in ['database','basis','lineage']}|{'questions':[],'reason':'All 15 captured practice records have MA identities; canonical e-492 is separate instructional evidence.'},indent=2)+'\n')
lesson=json.load(open(D/'lesson.json'))['record'][0];steps={r[':db/id']:r for r in lesson[':activity/steps']};route=[];at=lesson[':activity/first-step'][':db/id']
while at:
 st=steps[at];c=st[':step/content'];route.append({'step_id':at,'content_id':c[':db/id'],'title':c.get(':tutorial/title',c.get(':knowledge-point/title'))});at=st.get(':step/next',{}).get(':db/id')
(D/'lesson-route.json').write_text(json.dumps(route,indent=2)+'\n')
classification='''# Classification

Immutable capture: math basis 2275, lineage 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1. Owning topic 17592186050929 (MA317), Introduction to Integration by Parts. source.json is the full wrapper copied byte-for-byte. No prior numeric script/evidence/cache existed at the first-import snapshot; registration-evidence.json records has_generator:false. This draft neither imports nor writes a registered generator.

Lesson traversal follows activity/first-step then step/next (lesson-route.json): Introduction → exponential indefinite parts → this trig indefinite parts → definite parts → product-rule derivation → final choice-of-factors remark. The actual prerequisite is MA478, Integrating Trigonometric Functions Using Substitution. Canonical e-492 is x cos(2x), not an additional practice source. Sibling KP64245 contains exponentials and KP64274 contains definite bounds; neither is added here.

All 15 practice records are original MA-identified inventory; 8 easy, 6 moderate, 1 hard. All are single `selection` radio fields with 5 complete math primitive choices, each including +C. No missing correct refs, solutions, difficulty attributes or field attributes. No feedback is present or invented. No blank forms, diagrams or assets occur. Plot rating: none.

| Level | Source backbone | Fields | Source banks |
|---|---|---|---|
| easy | ax times sin(kx) or cos(kx); one parts application, primitive reduction; some cos sources show the uncollected second primitive before collection | radio | 8 |
| moderate | (ax+b) times unshifted sin/cos OR ax times sin/cos(kx+h); one parts application, one primitive | radio | 6 |
| hard | x csc²x; one parts application; cot rewritten cos/sin, then explicit u=sin x and logarithmic substitution | radio | 1 |

The script exposes 13 presentation/operative-stage recipes. They include distinct prompt style, optional primitive row, and unit/frequency constraints; these are not 13 new mathematical skills. sin_unit has q14437/q14449 banks; cos_frequency has q114297/q114312 banks. All other recipes have one observed complete bank.

All levels are observed, so no missing-level difficulty is inferred. Authored extensions keep the observed operators and stage sequence. Integer ranges broaden the source coefficients (1..10) and frequencies (1..5), and moderate affine/phase offsets (-8..8). Only one nonzero shift role occurs in moderate. Hard varies coefficient a and inner shift h, keeps b=0 and k=1 and the same logarithmic substitution workload. There is no within-level progression. Negative shifts do not add an integration method.

Source choices include several empirical expressions whose historical intent is not identifiable. They remain complete public observed:SOURCE replay profiles, evidence_only=true. Normal families use a separate complete operation bank. No algebraic source error has been found; raw spelling is kept separately from normalized generated notation. Full fidelity denominators are reported in validation.json.
'''
(D/'classification.md').write_text(classification)
lines=['# Template extraction','\n## Stage 1: individual observed records','\nEach row uses the exact original prompt, recorded number forms, field shape and correct source value. The complete raw fixed solution is in source.json and is printed in review.md; its whole prose skeleton and each operative row are validated.']
for sid,name,p in g.SOURCE_CASES:
 q=g.SOURCES[sid];f=q[':question/answer-fields'][0];lines += ['\n### '+sid+' — '+name+' ('+g.TEMPLATES[name][0]+')','\n'+q[':question/problem'],'\nParameters: `'+json.dumps(p,sort_keys=True)+'`. Integer affine polynomial factor; real independent x. Field `selection`, radio, five whole primitive families ending +C. Correct: $'+f[':answer-field/correct'][':answer/value']+'$.','\nOriginal ordered solution math blocks: '+str([m[0].count(r'\\')+1 for m in g.MATH.finditer(q[':question/worked-solution']) if r'\begin{aligned}' in m[0]])+' rows (definitions / substitution / reduction).']
lines += ['\n## Stage 2: shared generalized pattern','\nUse u=ax+b and v′ equal to the single supplied trigonometric factor. Find u′ and v, substitute both products into ∫uv′=uv−∫vu′, reduce the remaining integral, evaluate the primitive and collect. The csc² family additionally rewrites cot as cos/sin and uses the source substitution to evaluate the logarithmic primitive. Return one complete primitive with arbitrary +C, choosing from a complete five-member bank.','\n## Stage 3: all source components and complete bank recipes','\nRecipe symbols: U=ax+b, Z=kx+h, S=sin Z, T=cos Z. The two columns are the ordered summands before +C. These are whole empirical patterns, not an inferred historical-error catalog. Correct recipes use the actual parameter-dependent primitive, even when an anchor coefficient is coincidentally 1 or equals k. Normal learning never selects these empirical banks.']
for sid,name,p in g.SOURCE_CASES:
 q=g.SOURCES[sid];f=q[':question/answer-fields'][0];lines+=['\n### Bank observed:'+sid,'\n| Source choice | Original whole value | Parameterized ordered summands | Original designation |','|---|---|---|---|']
 for i,(a,parts) in enumerate(zip(f[':answer-field/choices'],g.BANK_PARTS[sid])):
  lines += ['| '+str(i+1)+' | $'+a[':answer/value']+'$ | `'+str(parts).replace('|','abs')+'` then +C | '+('correct' if a[':answer/id']==f[':answer-field/correct'][':answer/id'] else 'wrong')+' |']
lines += ['''\n## Stage 4: backbone, variable slots and constraints

Fixed roles: one integration variable x; one linear polynomial u; exactly one observed trig function; one parts application; `selection` radio; 5 complete primitive families with +C; the complete shared source prose, formula, definition block, substituted-product block and final reduction sequence. Coefficient and phase slots do not change the requested object or introduce targets from another method. Formula u′/v′ notation is preserved rather than replacing it with generic CAS prose.

| Slot | Role and permitted values | Dependencies |
|---|---|---|
| a | integer 1..10, nonzero differentiated coefficient | u, u′, product, residual coefficient, primitive, full banks |
| b | moderate affine family only, nonzero integer -8..8; otherwise 0 | complete affine factor in prompt, all product occurrences and final primitive |
| k | source-shaped frequency recipes 2..5; unit recipes and hard exactly 1 | trig input, primitive 1/k, residual a/k, final a/k², bank frequencies |
| h | moderate phase families nonzero integer -8..8; hard integer -8..8; otherwise 0 | every trig argument, hard substitution and differential, all banks |
| source presentation recipe | one of the observed compatible styles/stage masks | prompt shell, full shared source prose, retained primitive row |

Coupled arithmetic constraints: reduced a/k and a/k² numerator ≤10 and denominator ≤25; moderate |a b|≤64 (where b is used); k²≤25. No sampled or explicit input may remove a required nonzero moderate shift or the nonunit frequency of its source-shaped family. Hard keeps unit inner slope and monomial u, so it does not create a new harder coefficient-chain branch. All public explicit calls use identical guards. Signed shifts are grouped as whole affine components; no blind text replacement can alter function labels or differentials.

Profile is chosen before parameter sampling. Correct answer is computed before a whole bank. Every pair of complete primitives is compared modulo additive constants, and the correct derivative is compared with the actual integrand. Any collision, invalid term or ambiguity rejects the whole instance. No first-valid distractor pool exists.

Normal complete bank: let P=uv and R=correct−P, with u′=a. The five recipes are P+R (correct), P−R (wrong residual sign), P (omitted residual), −P+R (wrong product sign), P+(u/a)R (using u instead of u′ in the residual coefficient). The last is derived from the displayed derivative role, not an unrelated scalar perturbation. This is an authored operation bank; it does not assert observed distractor intent. The same full bank is available for each supported family and checked as a unit.

Each normal worked solution keeps the source prose and ordered operative blocks. Mathematical notation is normalized independently: source operatorname trig convention, consistent explicit argument parentheses, equivalent fraction placement and spacing; source hard `{csc}^{2}` becomes an explicit trig operator. Raw text remains unchanged in source.json/review.md. The long concrete by-parts equality and final calculation left side are line-wrapped after their equals signs for the native learner card. This is a display continuation within the same equality, not an added mathematical stage; validation folds only an explicit continuation and compares the original logical rows. Raw-exact math strings are not counted as exact matches. No source mathematical correction or missing-key completion is required.

Identities use normalized prompt, complete fixed solution, full displayed bank, version and actual level. Seeds/option order never change content ID. Mathematical fingerprints use the expanded actual integrand and exclude bank/style aliases. Finite domain counts in validation.json exclude labels, notation and option order. Equal primitives differing only by a constant are ambiguous even when spellings differ.
''']
(D/'template-extraction.md').write_text('\n'.join(lines)+'\n')
(D/'plot-extraction.md').write_text('# Plot extraction\n\nNone. No prompt, answer or solution contains an image or diagram. All trig and logarithmic forms are learner mathematics rendered by the actual player MathJax pipeline, not plot assets. No plot generator or image model was used.\n')
(D/'README.md').write_text('''# KP17592186064246 local draft

Script: `../17592186064246-draft.py`. Evidence at immutable math basis2275. Local review only; stop after generation/verification step7. No EDB writes, registration, engine changes or package installation.

Run from repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python generate/scratch/17592186064246-draft/validate.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python generate/scratch/17592186064246-draft.py --difficulty all --seed 7 --count 2 --format json
```

All easy/moderate/hard levels have original source evidence. 15 MA originals, no independent inventory. Normal default families use one complete authored method-error bank; complete historical profiles remain public evidence-only `observed:q-ID` replays with their original field/layout contracts. All source prose and ordered teaching stages survive. See template-extraction.md for slot/recipe bounds and validation.json for exact denominators, native results and limitations. JSON CLI output is a bare list.

Source mathematical fidelity permits normalized argument parentheses and fraction placement; it does not claim byte-exact math strings. The immutable original wrapper retains all source bytes. There are no blank equivalents to test; native checks exercise all 5 actual radio selections in every source/profile/default record. No source omission has been inferred away.
''')
