from pathlib import Path
import sys
sys.dont_write_bytecode=True
import importlib.util,json
H=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('g',H.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
(H/'classification.md').write_text('''# Classification: registered revalidation draft, basis 2275

Frozen database math; lineage 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1. The source wrapper is unchanged. Original practice consists of fourteen MA-identified questions: ten labeled easy, two labeled moderate and two unrated. Twelve have captured solutions and correct designations; two have neither. Four fields are blank, including one supplied-cubic-term fragment, and ten are five-equation radio banks. Fourteen source prompt/solution/layout masks are kept separately. The conservative fourteen-mask count does not claim fourteen distinct skills: polynomial masks share a direct-integration backbone but retain different operative rows and response contracts.

Eight additional records lack MA IDs: three moderate and five hard independently authored inventory entries. independent-inventory.json preserves every exact record, the exact role "independently authored inventory", and its concrete relationship to original families. These are contextual inventory, not recovered original templates or observed MA difficulty evidence.

Easy originals include reciprocal-square, exponential, trigonometric, polynomial, reciprocal-square-root, linear-logarithmic and constant primitives. Moderate originals combine one polynomial and one exponential primitive. There are no original MA hard examples. Hard defaults are explicitly authored three-component polynomial/exponential/trigonometric peers: three nonzero standard primitives, one additive constant and one initial condition. This conservatively extends the moderate two-component workload within the same method. Independent inventory has comparable authored instances, but does not establish observed MA hard difficulty.

The actual lesson route follows activity/first-step 17592186097555 and successive step/next references through 17592186097560: Introduction; general direct integration; the separate second-order KP; the separate solution-curve KP; Particular Solutions tutorial; this KP. Canonical e-531 integrates 3/(1+x²) and evaluates f(0)=2. Exponential/trigonometric substitution and verification are prerequisites. Integrating factors and separation are successors and excluded. Second order, multiple conditions, graph sketches and contextual models are excluded.

Plot rating is none for every original and authored family. All normal easy/moderate source-shaped families are sampled; full method-derived banks are selected before scale and target. No bank member is replaced after sampling and no radio instance silently becomes a blank. All opaque source banks, including their repaired profiles, are explicitly evidence-only/ineligible.
''')
text='''# Template extraction

## 1. Specific source instances

The fourteen original records are analyzed at fixed basis 2275. All use x as the independent variable and y or f(x) as the dependent quantity. The requested response is an explicit particular function, or precisely the supplied blank fragment. The initial pair determines a single additive constant. Every complete original choice and source field is mapped below; prose and full source stages remain in source.json and review.md.

'''
for t,q in g.QUESTIONS.items():
 field=q[':question/answer-fields'][0];der,P,a,b,fragment,bank=g.DEFS[t]
 text+='### '+t+'\n\n'+q[':question/problem']+'\n\nField '+field[':answer-field/type'][':db/ident']+'; key '+field[':answer-field/key']+'. Captured difficulty '+q.get(':question/difficulty',{}).get(':db/ident','absent')+'. Primitive '+g.tex(P)+'; given pair ('+str(a)+', '+str(b)+'); supplied component '+g.tex(fragment)+'.\n\n'
 text+='| Choice identity | Captured complete value | Explicit replay expression | Captured designation |\n|---|---|---|---|\n'
 for choice,expr in zip(field[':answer-field/choices'],bank):
  designation=choice[':answer/id']==field.get(':answer-field/correct',{}).get(':answer/id') if ':answer-field/correct' in field else 'absent'
  text+='| '+choice[':answer/id']+' | `'+choice[':answer/value'].replace('|',r'\vert')+'` | `r * ('+str(expr)+')` | '+str(designation)+' |\n'
 text+='\n'
text+='''## 2. Generalized backbone

Rearrange the supplied first-order equation to a derivative depending only on x; integrate once; retain source factorization and primitive stages; write P(x)+C; substitute the actual given function value; evaluate each displayed primitive component in the source order; collect the arithmetic when the source does; solve C=v−P(a); give the explicit particular function. The supplied cubic term in q-347842 is not part of its blank answer. An arbitrary-C family alone does not meet the particular-response criterion.

## 3. Components, banks and interpretation limits

Observed replay uses a genuine mathematical symmetry: rescale the dependent function by a nonzero integer r. Its derivative, primitive, initial target and every complete candidate function all rescale together. The actual displayed ODE preserves its derivative coefficient and rescales its derivative-free terms; this produces derivative r*g₀(x). The initial target is r*b₀. Each bank recipe is r*Fᵢ(x), as explicitly mapped above, rather than a source-value offset, unrelated perturbation or original-parameter answer table. The intent of historical wrong operations remains opaque, so both observed_raw and observed_repaired are ineligible evidence. Unit scalar multipliers suppress themselves as a generic component-formatting rule; there is no original-parameter branch returning a source question payload.

Normal families use the same observed prompt/solution masks and response contracts, but an independently sampled target v. Correct values come from r*P₀+v−r*P₀(a). A complete authored radio bank contains correct; discard the supplied initial value (impose zero instead); negate the primitive and then impose the real condition; use the derivative as a primitive and impose the condition (for q-49942 instead ignore the displayed derivative coefficient 2 while isolating, since its unscaled exponential derivative equals its primitive); and one family-specific operation. The fifth operation is: add instead of subtracting the primitive value when solving C for reciprocal/exponential single-term families; reciprocate the displayed coefficient in trig integration; swap exponential differentiation/integration scale for moderate sums; omit the new-power 1/2 divisor for the radical; omit inner-linear divisor 2 for the logarithm; treat a constant derivative as linear before integrating; or omit each new-degree divisor in polynomial integration. Hard uses the polynomial new-power-divisor-3 omission in one component. These are authored method operations, not recovered historical error intent. No distractor feedback is invented.

Banks are fixed as complete profiles before any parameters. Equivalent complete functions, duplicate options or correct distractors reject the entire sampled instance. Explicit invalid inputs raise, rather than being changed. Source blank shapes remain fixed in normal sampling; hard blank/radio peers are separately authored layouts. Captured absent answer feedback remains absent.

## 4. Slots, masks, bounds and dependencies

Observed replay parameters contain only scale r∈{−2,−1,1,2,3,4}. This bounded rescaling changes actual integration coefficients and conditions while keeping the operation, singularities, familiar evaluation input and all source stage roles. Normal easy/moderate parameters are exactly r in that catalog and integer v with 0<|v|≤12. Normal default selection exercises all twelve supported easy masks (including two explicitly authored easy assignments for unrated originals) and both moderate masks. Initial input a stays at its family-specific source point so the existing rational, perfect-square, trigonometric or exponential evaluation workload and its operative masks remain intact. This is a documented conservative arithmetic policy; it does not claim that source targets are intrinsically immutable. The v slot varies the requested initial function value and its solved constant independently with every other mathematical input held fixed in QA.

Signed scale factors wrap complete mathematical components with a visible multiplication operator. They do not concatenate numeric factors or modify variable/function labels, prose, TeX commands or differentials. Primitive factors, factored integrals, evaluated components and collected arithmetic remain separate ordered masks. Normal repair removes q-50044's erroneous dx before scaling, placing C outside the coefficient mask. This avoids treating r*C as the same subsequently solved C.

Hard parameters are integer nonzero |a|≤6, |b|≤3, |d|≤4, k∈{−2,−1,1,2}, initial input zero and integer |v|≤12. Three nonzero components are mandatory. Explicit fractional/huge-denominator coefficients or targets and noncatalog inputs fail. All samplers use these same bounds. Zero initial targets may produce a hard blank but an ambiguous radio bank is rejected as a whole. The coefficient/target arithmetic stays bounded and uses prerequisite power, exponential and trig rules. All family variants within one level are peers; no integrating-factor, separation, second-order or extra-condition branch is added.

Mathematical fingerprints normalize the actual derivative with exact factor/cancel and include the actual initial input and target. Function-letter aliases, banks, seed, shuffle and unused parameters do not inflate mathematical-task counts. Content identities use normalized displayed prompt, fixed solution, complete sorted bank, actual difficulty/key presence and actual correct designation. Shared scripts/question_capture/math_format.py normalizes before IDs and validates repaired/normal public output. Explicit observed_raw is ineligible evidence and preserves original bytes without learner normalization; it carries learner_normalization_applied=false. Raw source format diagnostics are separate from complete mathematics and native diagnostics, and missing raw solutions remain absent. Runtime Python and SymPy versions are recorded.

## Domain and source errors

Initial connected intervals are x>1 for q-119078; x>3 for q-352066; x>−1 for q-352068; x>−1/2 for q-50159; and x<0 for rearranging q-50044. The last polynomial also satisfies its original unisolated equation at x=0, but the displayed division method uses the interval containing the negative given input. Others use all real x. No unconditional absolute-value/sign stripping is allowed: the validator verifies logarithmic expressions on the actual positive connected branch by a positive-symbol substitution.

q-119078 and q-49942 are unrated and lack worked solutions/correct references. Raw replay preserves all omissions. Repaired profiles explicitly author the easy assignment, infer the unique mathematically valid third/fifth choice and supply complete same-method stages. No missing source solution/difficulty is claimed recovered. q-119045's general-solution prose misnames f as y; q-50044 attaches dx to an evaluated primitive and misnames the final y solution f. Raw profiles preserve these errors and remain ineligible; repaired/normal profiles make the smallest supported corrections. Twelve exact original worked-solution matches are separate from ten unmodified complete solutions, two supported teaching corrections and two absent solutions completed by authorship. Public observed_raw also preserves all 54 complete captured answer strings byte-for-byte at unit scale, including spacing and factored/plain-slash notation. A generic unit-scale component mask suppresses its own scalar; nonunit scales wrap the entire original RHS or blank fragment. Repaired and normal profiles use the standard-TeX mathematical view separately. The source-format audit measures actual decoded backslash runs and shared structural errors; it does not infer doubled commands from serialized display. No TeX escape anomaly is inferred from serialized display alone.
'''
(H/'template-extraction.md').write_text(text)
(H/'plot-extraction.md').write_text('# Plot extraction and generation\n\nNone for all fourteen original MA questions and e-531. Neighboring solution-curve plots belong to a separate KP and are not used. No renderer or assets are necessary.\n')
(H/'README.md').write_text('''# Basis-2275 registered revalidation draft

Only 17592186096699-draft.py and its private evidence are modified. registered-baseline.json records the entire original numeric script/evidence pathset and hashes; validation checks it unchanged. No registration, database writes, engine edits or shared QA edits.

```sh
.venv/bin/python generate/scratch/17592186096699-draft/validate.py
.venv/bin/python generate/scratch/17592186096699-draft.py --difficulty all --count 2 --seed 7 --format markdown
.venv/bin/python generate/scratch/17592186096699-draft.py --difficulty easy --template q-119078 --profile observed_raw --format json
```

API generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None), plus three difficulty wrappers. Original public replay uses observed_raw with {scale:1}; all 54 captured choice strings are exact. Raw ineligible evidence alone bypasses learner normalization, preserving any actually malformed capture bytes without serving them. observed_repaired preserves opaque complete banks while making explicitly authored repairs. Both are evidence-only/ineligible. Observed variants use bounded dependent-function rescaling, with no arbitrary bank offsets. Normal defaults choose every supported source-shaped easy/moderate family and authored method-derived banks, with {scale,target} slots; hard uses three familiar primitive components, one initial condition and bounded explicit parameters.

source.json is the exact math basis-2275 wrapper. source-cases.json covers all fourteen MA originals. independent-inventory.json preserves all eight independent records as separately labeled context, not observed MA templates. The validator reads the actual supplied equation, condition, all choices, formal inputs, primitive and evaluation stages, final prose, domains, branches and grading contracts. Mutation controls change math and operative structure while refreshing content hashes. Native memory-only grade_field checks cover every radio option and canonical/equivalent/wrong blank entries. Review and validation separate original fidelity, notation normalization, source errors, authored scope, mathematics, native grading and baseline preservation.
''')
print('draft documentation built')
