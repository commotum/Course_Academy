from pathlib import Path
import importlib.util,json
D=Path(__file__).resolve().parent
z=importlib.util.spec_from_file_location('draft',D.with_suffix('.py'));g=importlib.util.module_from_spec(z);z.loader.exec_module(g)
s=json.load(open(D/'source.json'));qs=[q for q in s['record'][':knowledge-point/questions'] if ':question/math-academy-id' in q]
(D/'classification.md').write_text('''# Classification at frozen math basis 2275

Lineage: 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1. The registered numeric generator and every existing evidence path remain immutable; registered-baseline.json records the complete 83-file path and SHA256 baseline before this draft. No database operations are performed.

The captured pool contains 8 original MA practice records: 7 explicitly easy and 1 unrated. One independently authored easy inventory record is captured in full in independent-inventory.json; it is the registered reciprocal n=12 extension and supplies no new original evidence. The canonical e-374 supports context, not practice fidelity counts.

All original fields are one five-choice math radio with key `selection`. Six mathematical coefficient families are observed: positive integer (q-29934, q-103369, q-103590), negative integer (q-29831), positive reciprocal integer (q-49097), positive reciprocal radical (q-29838), negative rational (q-71098), negative reciprocal radical (q-72059). Eight named anchor profiles preserve source layout, complete bank and ordered operands. The two rated positive integer anchors share the same mathematical bank under parameter substitution; their literal order/ln markup does not count as another mathematical template. The unrated positive integer presentation lacks a key and solution. No source medium/hard examples exist.

Four complete source banks are valid without mathematical repair: q-49097, q-29838, q-71098, q-72059. Four contain duplicate wrong primitive families and are excluded unaltered from ordinary learning output: q-29934, q-103369, q-103590, q-29831. Every original remains parameterized through `profile="raw"`; normal output uses separately named `repaired` banks for these four. This is an explicit source defect repair, not a claim of unchanged served fidelity.

No prompt, answer or solution has a plot or mathematical diagram. Plot classification is **none** for every family and authored level.
''')
intro='''# Template extraction

## 1. Specific original descriptions

All full original records and canonical/prerequisite references are frozen in source.json. Every original component is mapped below. Literal source value and corresponding recipe use the captured choice order; the generator may shuffle output, retaining field-owned identities. Recipes are complete displayed expression patterns, not claims about inferred learner psychology.

'''
for q in qs:
 mid=q[':question/math-academy-id'];t=g.TEMPLATES[mid];f=q[':question/answer-fields'][0]
 intro+='### '+mid+'\n\nPrompt: '+q[':question/problem']+'\n\nObserved parameters: `'+json.dumps(t['parameters'])+'`; coefficient family '+t['kind']+'. Field selection: five-choice math radio. '+('Source has its key and worked solution.' if ':question/worked-solution' in q else 'Source omits difficulty, correct designation and worked solution.')+'\n\n'
 intro+='| Choice | Captured exact value | Parameter recipe | Captured key |\n|---|---|---|---|\n'
 for i,a in enumerate(f[':answer-field/choices']):
  literal=a[':answer/value'].replace('|',r'\|');recipe=t['values'][i].replace('|',r'\|');key='yes' if a[':answer/id']==f.get(':answer-field/correct',{}).get(':answer/id') else 'no' if ':answer-field/correct' in f else 'missing'
  intro+='| '+str(i)+' | `'+literal+'` | `'+recipe+'` | '+key+' |\n'
 intro+='\nOrdered source solution: '+q.get(':question/worked-solution','absent; authored served repair follows canonical e-374 constant extraction then reciprocal primitive.')+'\n\n'
intro+='''## 2. Shared family pattern

Calculate the indefinite integral c/x by extracting one nonzero constant, then applying integral(1/x)=ln|x|+C on each connected real interval x>0 or x<0. Radical coefficients use the existing source rationalization before the same integration. The supplied object is always one constant multiple of the reciprocal function and the requested object is its whole antiderivative. Every normal instance retains one five-choice radio selection; no sums, substitutions, shifted reciprocal functions, definite limits, initial conditions or logarithmic arbitrary-constant transformations are introduced.

## 3. Components, profiles and source repairs

Source prompts, field key/type/count, correct coefficient, full banks, sentences, coefficient factors, integral operands and final primitive are generated together. Profiles are chosen as complete banks; recipes are never pooled. `raw` is a normalized parameterized schema reference: it reproduces every captured mathematical value, prompt, ordered source solution and relevant omission after required TeX normalization. It is not the full captured Pull record; only source.json preserves that exact full immutable wrapper and attributes. It is explicitly evidence-only. Unchanged normal `observed` banks are the four valid source profiles. `repaired` changes exactly one wrong option in each defective bank:

- q-29934: n+ln|x|+C duplicates ln|x|+C modulo constant. Replace the former by -n ln|x|+C (wrong extracted sign). Its missing key is independently derived as n ln|x|+C, its solution is authored from canonical e-374, and its missing level receives an authored easy assignment.
- q-103369 and q-103590: n+ln|x|+C duplicates ln|x|+C. Replace that sole wrong value by -n ln|x|+C, preserving all other values and the supplied key, prompt and source solution.
- q-29831: n ln x+C and n ln|x|+C coincide as primitive families on x>0. Retain n ln|x|+C and replace n ln x+C by -(1/n)ln|x|+C (reciprocated extracted magnitude). All four other original choices remain. The n/ln x+C wrong choice has real domain x>0,x!=1; it is not claimed to define a real primitive on x<0. It is a source distractor with insufficient domain and a wrong derivative even where defined.

Original C-inside-log errors in q-29838 are retained: they fail as arbitrary primitive families even if a special C=0 yields a valid member. A distractor ln(k|x|)+C has derivative 1/x; it is wrong only when the required coefficient differs from one. Our nonsquare radical bounds enforce that difference. All ordinary choices are pairwise different derivative families on both admissible branch intervals; raw defective banks are never passed as ordinary compatibility tests. Original complete-bank replication, unchanged served-bank fidelity, narrow repair comparisons and authored completeness are separate denominators in source-fidelity.json/validation.json.

TeX normalization removes invisible function-application characters, replaces bare ln/operatorname ln by a delimited \\ln command, decodes legacy double-escaped answer commands and applies the shared course-academy-tex-v1 normalizer before IDs. This presentation normalization preserves operands and ordered rows. Raw source JSON remains byte-for-byte unchanged.

## 4. Backbone and bounded slots

Fixed: c/x structure, constant multiple rule then reciprocal integral, one global arbitrary additive C, whole primitive answer contract, five complete choices, source instructional prose and ordered solution operands. Each source profile freezes its own differential layout/row sequence as observed; these are not counted as distinct assessed tasks. Exact source parameters remain legal and replayable.

Variable slots:

| Level | Slot | Bounds and constraints | Dependent components |
|---|---|---|---|
| easy | integer magnitude n | 2..20 for positive, negative and reciprocal integer families | coefficient, integrand, extracted coefficient, all five complete recipes and final primitive |
| easy | radical radicand n | squarefree 2,3,5,6,7,10,11,13,14,15 | radical denominator and rationalization, five choices |
| easy | rational a,b | a=2..7,b=2..11,gcd(a,b)=1 | signed reduced coefficient, reciprocal/sign distractors and all printed operands |
| moderate authored | rational a,b | a=2..14,b=2..15,gcd(a,b)=1 | exactly the q-71098 complete bank/prose/row structure |
| hard authored | radical numerator a, radicand n | a=2..9; n in the squarefree set above | exactly q-72059 rationalization and integral structure, numerator propagated to all five recipe values |

Source coefficients and domains are distinguished from these author-defined bounds. Squarefree radicands and reduced fractions exclude aliases; no C changes or option shuffles count as variation. A canonical task fingerprint is the exact coefficient c of c/x, independent of bank/prompt/seed. Finite catalog batches deduplicate across source layouts and bank profiles, reject requests above the meaningful count, and never silently truncate. All slots are enumerated exhaustively; capacity.json records each slot's observed coverage and the meaningful count per level.

### Missing-level authorship and curricular calibration

The frozen lesson route is reconstructed from activity/first-step17592186106584 through step/next, not collection order: introduction (derivative of ln|x| on x!=0), this KP (step17592186106585), integrating a reciprocal-plus-power sum (17592186106586, KP17592186105716), arbitrary-constant log tutorial (17592186106587), then KP17592186105720. The canonical e-374 extracts integer2. Prerequisites are the Constant Multiple Rule for Indefinite Integrals (topic43) and Differentiating Logarithmic Functions (topic1116). Those anchors permit coefficient arithmetic and the same ln|x| rule, while adjacent KPs exclude sums and constant-law rewrites from this draft.

No observed medium/hard label is inferred. Moderate is an authored calibration to reduced negative nonunit rational coefficients, retaining one extraction and two aligned rows. Hard is an authored calibration to nonunit radical numerators, retaining the observed q-72059 rationalization identity and two integral rows. Numerator multiplication/rationalization increases coefficient bookkeeping but requires no additional integration method, new operator branch or subsequent lesson. Each level has a single comparable workload policy; there is no progression within a level. Some coefficient forms overlap original easy evidence; the level distinction is an explicit conservative authorship claim, not source-confirmed difficulty. We do not multiply capacities with new operators to manufacture variety.
'''
(D/'template-extraction.md').write_text(intro)
(D/'plot-extraction.md').write_text('''# Plot extraction (docs5)

All eight original prompt/bank/solution records, canonical context and authored templates contain TeX only, with no image or diagram references. Specific plot inventory: zero for each source. Shared visual pattern: none. Plot components, parameter dependencies, asset placements and variable geometric targets: none. Reusable specification: no assets, no rendering. All mathematical variation is expressed in text from the same coefficient instance. Rating: none.
''')
(D/'plot-generator.md').write_text('''# Plot generator (docs7)

No template requires generated or reused plots. No plot backend or image model is invoked. This is a documented not-applicable result of docs5, not an omitted plot requirement.
''')
(D/'generator.md').write_text('''# Template generator (docs6)

The private -draft.py script implements all three levels, exact SymPy coefficient work, strict seeded bounded sampling, source/repair/authored profiles, complete banks, field-owned UUIDs, a private frozen math_format.py dependency loaded by explicit local file path, shared-format normalization/validation and flat JSON/Markdown CLI previews. Observed profile generation is parameterized rather than a raw Pull lookup. Normalized parameterized raw evidence-only references preserve the relevant question/field omission semantics but are not full Pull records; source.json alone is the exact full immutable Pull wrapper; shared generated-record validation applies to every served record. Identity hashes normalized prompt, solution, whole bank, level and profile; changing seed or option order preserves identity. All choices are shuffled deterministically by an independent Random(seed), so replaying recorded template/parameters reproduces exact option order whether those slots were originally sampled or supplied. The exact c/x coefficient is the separate cross-layout mathematical deduplication key.

validate.py independently parses the actual displayed integrand, every displayed answer and each solution operand and inline rationalization equality. Exact derivatives are checked on x>0 and x<0 modulo arbitrary additive constants; wrong choice pairs may not share a derivative on either branch. Correct arbitrary C must remain outside the logarithm. All bounded profiles and slot values are enumerated; the frozen native check-engine receives every normal bounded record, all owned correct/wrong choices. Radio text0,1,+1 is tested separately as foreign-ID ownership diagnostics. These native ID-selection checks establish the radio answer contract, while independent calculus establishes displayed mathematics. Foreign IDs/malformed ownership diagnostics do not enter mathematical compatibility totals; equivalent mathematical text is not a radio-field submission.

source-fidelity.json separates all40 raw original values from the four narrow repairs. review.md/review.json show every original, every normal source anchor, a changed coefficient for each source profile and two authored instances at each missing level. Registered baseline path/hash stability and frozen native engine SHA are asserted at each validation run. No EDB writes, registration, shared QA/queue edits or commits.
''')
(D/'README.md').write_text('''# Private reciprocal integration draft

Run `.venv/bin/python generate/scratch/17592186105715-draft/validate.py` to verify full original replay, all bounded served mathematics and frozen native grading. Preview with `.venv/bin/python generate/scratch/17592186105715-draft.py --difficulty all --count 1 --seed 17 --format json`.

This draft supports all three levels. Original evidence is 7 easy and1 unrated MA record, plus1 independent inventory context. Four defective source banks have narrow separately named repairs; raw complete bank reproduction and normal repaired fidelity have separate totals. Moderate/hard are explicitly authored coefficient calibrations, not observed source labels. See template-extraction.md and source-fidelity.json.

Registered numeric generator and its83-file existing evidence path/hash baseline remain unchanged. Source wrapper is exactly frozen basis2275. Private work stops after docs3–7 and awaits parent independent readback; no registration or database write.
''')
print('docs written')
