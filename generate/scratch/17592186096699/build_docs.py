from pathlib import Path
import importlib.util,json
H=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('g',H.with_suffix('.py'));g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g)
(H/'classification.md').write_text('''# Classification — basis 1356

Database math; lineage 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1. Fourteen practice originals: ten easy, two moderate, two unrated legacy radios. Unrated questions get an authored easy assignment only in repaired completion; raw replay omits difficulty. Twelve complete designations were captured; two are absent. Twelve worked solutions were captured; two are absent.

Every question asks for an explicit particular first-order solution obtained by rearranging to y′=g(x), integrating once, then determining the single additive constant from a given function value. No plots occur in any practice source or this KP's canonical example. Fourteen prompt/stage/layout templates are retained separately; ten have radio banks of five equations and four use one blank fragment. The four blank layouts include a supplied cubic term (q-347842), so its response is the remaining fragment, not the whole function.

Easy includes polynomial, rational reciprocal, square-root, logarithmic, trigonometric and exponential primitives; moderate has one polynomial and one exponential component. Hard has no observed source. Its authored peers combine three familiar nonzero primitive components (polynomial, exponential, trigonometric), still requiring exactly one integration and one constant equation. This is a scope design claim, not a recovered source difficulty label.

Lesson route follows first-step 17592186097555 and step/next through 17592186097560: Introduction → general solution by integration → second order (a different sibling KP) → sketching (a different sibling KP) → Particular Solutions tutorial → this KP. Canonical e-531 integrates 3/(1+x²), then evaluates f(0)=2. Prerequisite topics provide exponential/trig substitution and verification. Integrating factors and separation are successor topics and excluded. Second order, solution curves, contextual models and multiple conditions are excluded.

Normal profiles select a full authored operation bank before any parameter sampling; invalid or equivalent members reject the entire instance. Observed banks are available by explicit replay profile only, with opaque error interpretation flagged. Every normal level includes both radio and blank layouts as labeled authored layout peers.
''')
text='''# Template extraction

## 1. Specific originals

All originals have independent variable x; dependent variable is y or f(x). Domains are connected real intervals containing the initial input. Rational denominator and radical restrictions are part of mathematical verification; q-50159 is restricted to x>−1/2 for its given input. Multiplication by x in q-50044 is handled away from x=0 when rearranging, and the derived smooth polynomial remains a solution of its displayed original equation at x=0 as well.

'''
for t,q in g.QUESTIONS.items():
 f=q[':question/answer-fields'][0];der,P,a,b,fragment,bank=g.DEFS[t]
 text+='### '+t+'\n\n'+q[':question/problem']+'\n\nField: '+f[':answer-field/type'][':db/ident']+'; key '+f[':answer-field/key']+'. Observed difficulty '+q.get(':question/difficulty',{}).get(':db/ident','absent')+'. Primitive '+g.tex(P)+'; actual given input '+str(a)+'; target '+str(b)+'. Supplied fragment '+g.tex(fragment)+'.\n\n'
 text+='| Source choice | Exact captured value | Parameter recipe | Correct captured |\n|---|---|---|---|\n'
 for ans,expr in zip(f[':answer-field/choices'],bank):
  correct=f.get(':answer-field/correct',{}).get(':answer/id')==ans[':answer/id'] if ':answer-field/correct' in f else 'absent'
  text+='| '+ans[':answer/id']+' | `'+ans[':answer/value'].replace('|',r'\vert')+'` | `'+str(expr)+' + B − ('+str(b)+')` | '+str(correct)+' |\n'
 text+='\nSolution stages: '+str(q.get(':question/worked-solution','No captured worked solution.').count(r'\\'))+' aligned row separators. Original complete solution stays in source.json and review.md; replay preserves all sentences and each primitive/initial-substitution row.\n\n'
text+='''## 2. Shared pattern

Rearrange the actual ODE; integrate the independent-variable function; write P(x)+C; substitute the actual initial pair; individually evaluate primitive components; solve C=B−P(a); render the explicit particular solution. A supplied-fragment blank expects precisely the missing additive fragment. A radio candidate is eligible only if its complete function both differentiates to the actual displayed ODE and satisfies the actual initial condition. An arbitrary-constant family is not a valid particular response.

## 3. Component mapping and bank interpretation

The tables map every captured option to its original field and complete bank. Observed error intent is opaque: the recipes explicitly retain each observed derivative candidate and translate its constant by the target displacement B−B₀. This is a genuine vertical-translation parameter family, not recovery of the author's error-generation code. These profiles are replay-only and ineligible for default generation. The explicit symbolic definitions are independently compared to every captured option. No polynomial fit or random wrong-value perturbation is used.

Correctness is derived independently from the actual prompt and condition; missing correct references are inferred only in observed_repaired completion. Missing raw difficulty, worked solution and correct references remain absent in observed_raw output. Raw evidence preserves source answer notation; generated bank values use standard TeX normalization of the explicit symbolic recipes. Full mathematical values and equation/fragment shapes match one-to-one. Authored operation banks have five complete candidates: correct; omit C; negate primitive and impose condition; use derivative as primitive and impose condition; halve primitive and impose condition. Every record exposes evidence_only and eligible_for_learning booleans in generation metadata. Both observed profiles are ineligible for learner generation; authored operation profiles are eligible. No option-specific feedback is added. Each bank is fixed before parameters; a collision rejects the whole instance.

## 4. Reusable masks and constraints

Observed parameter B changes the complete initial-condition component, numeric left components of substitution rows, complete solved constant component, and complete final solution component. Source primitive factors and all original evaluation rows remain fixed. Conditional algebra suppresses an empty zero translation in the complete expression; it does not return a copied source question. This conservative parameter axis honestly preserves observed stage structure. Authored defaults additionally vary integrand coefficients and initial pairs. Mathematical task hashes omit answer banks and function-letter aliases; content hashes include actual displayed prompt, fixed worked solution, full bank and key presence. Seeds only change samples or option order, never identity for fixed displayed content.

Easy authored power/trig peers use signed |a|≤8, nonzero coefficients, familiar integer power inputs or trig input zero. Moderate uses two nonzero components with |a|≤8, |b|≤4, exponent k∈{−2,−1,1/2,1,2} and initial input zero. Hard uses three nonzero components with |a|≤6, |b|≤3, |d|≤4, k∈{−2,−1,1,2} and input zero. All used coefficients and targets are integers; all targets satisfy |v|≤12. Initial inputs come from the stated finite integer catalog; fractional inputs, fractional targets and unbounded-denominator coefficients are rejected. Only the moderate exponent scale has the explicit familiar 1/2 option. Bounds apply to explicit inputs as well as samplers. Authored levels are parallel same-method workloads, not a progression within a difficulty. Coefficient-times-primitive stages and component substitution/evaluation rows use grouped signs, so negative numeric products cannot concatenate into another scalar.

## Source anomalies and repairs

q-119078 and q-49942 are unrated and lack worked solutions/correct references in this fixed-basis record. Their mathematical particular solutions uniquely identify the third and fifth source options, respectively; repaired records infer these designations and supply complete same-method stages. The owning authoritative 1061.json capture contains no matching question identifiers for these legacy items; no source difficulty or missing solution is claimed recovered.

q-119045's general-solution prose uses y although its ODE and final solution use f(x); repaired output uses f(x). q-50044 incorrectly prints dx after an evaluated primitive and names the final y solution f(x); repaired output removes that dx, retains the additive C stage, and uses y. Raw replay retains the captured errors as evidence, and the validator distinguishes them from normal correctness. There are no assumed TeX byte anomalies or image repairs.
'''
(H/'template-extraction.md').write_text(text)
(H/'plot-extraction.md').write_text('# Plot extraction and generation\n\nNone. All fourteen practice originals and e-531 contain mathematical text only. Steps 5 and 7 require no assets or rendering. The neighboring solution-curves KP contains plots but is outside this assignment.\n')
(H/'README.md').write_text('''# Particular first-order solutions

Private generator and evidence, database math basis 1356. Stops after step 7. No database writes or shared edits.

```sh
.venv/bin/python generate/scratch/17592186096699/validate.py
.venv/bin/python generate/scratch/17592186096699.py --difficulty all --count 2 --seed 7 --format markdown
.venv/bin/python generate/scratch/17592186096699.py --difficulty easy --template q-119078 --profile observed_raw --format json
```

API: generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None), with generate_easy/moderate/hard wrappers. Source cases select observed_raw explicitly. Bank notation is normalized from independent symbolic recipes; complete values and response shapes remain faithful. observed_repaired supplies documented missing labels/designations/solutions and repairs two teaching errors. Normal defaults use authored_operations and never select opaque banks. Original profiles parameterize only the initial ordinate; authored defaults provide varied integrands at all three levels. Hard is explicitly authored because no hard source was captured. See classification, extraction, complete original/variant review and validation.json for separate fidelity, math and native grading evidence.

SymPy checks read the actual ODE, condition, complete choices, primitive and constant-substitution rows. Native checks use the real memory-only learning::grade_field executable, with canonical/equivalent/wrong blank entries and every radio selection. Raw records missing correct references cannot enter the complete-fixture grader and are tested after explicitly inferred completion; these are never counted as observed correct-designation matches.
''')
