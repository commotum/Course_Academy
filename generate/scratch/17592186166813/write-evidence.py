"""Build source extraction evidence from the immutable capture, never EDB."""
import importlib.util,json,hashlib
from pathlib import Path
H=Path(__file__).parent
s=importlib.util.spec_from_file_location('g',H.with_suffix('.py'));g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
intro='''# Source classification

Database **math**, basis **1356**, lineage **01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1**. `source.json` copies the capture wrapper without modification. Fourteen practice questions, all rated. The canonical example e-8459 is contextual evidence, not a fifteenth practice case.

| Level | Sources | Fields | Recovered presentation/value recipes | Complete banks | Plots |
|---|---:|---|---:|---:|---|
| easy | 7 | 6 one-field radio; 1 one-field blank | 7 source structural masks | 7 | none |
| moderate | 7 | three boolean checkbox fields, I/II/III | 7 source equation-set structural masks | 7 | none |
| hard | 0 | authored three boolean checkbox fields | 1 mixed-notation recipe, three equal-workload layouts per equation | authored | none |

The seven source instances at a level have the same response demand but distinct equation component layouts, so their literal masks are separately addressable; this does not mean fourteen separate mathematical skills. The scalar prompt/solution prose is common except the display/blank template q-167787. Moderate sources share an opening, three per-equation classifications, and a selected-set conclusion. Boolean banks are the same two-value response catalog on each field; answer correctness changes with displayed order and requested target.

Source scalar banks vary. q-95982, q-96662 and q-96663 show the catalog1–5. q-118781 shows2–6. q-118779 shows3,4,6,7,8; q-118780 shows2,6,7,8,9. Their exact source-profile recipes are offsets from the displayed highest order. These reproduce values but do not recover historical author intention. They remain evidence-only; authored defaults use complete displayed-method distractor operations.

Every plot rating is none: no Markdown image links, graphs, diagrams, or visual assets appear. No renderer is required.

Scope and curriculum: topic3215 Introduction to Differential Equations has predecessor/prerequisite topic281 Second and Higher-Order Derivatives. Traversing activity646099ed-0bc0-5178-b252-fcbaf49d8855 through first-step and next gives Introduction17592186167625 → this KP17592186167650 → Autonomous tutorial17592186167693 → sibling autonomous KP17592186167651 → IVP tutorial17592186167694 → sibling IVP KP17592186167652. The introduction defines order as the highest derivative; the canonical example scans third and second derivatives with an irrelevant y² factor. Adjacent autonomous/IVP skills are excluded, as are solving ODEs, degree, linearity and PDEs.

Authored easy reads two Leibniz derivatives, compares orders, and ignores one larger ordinary exponent. All instances need the same one scalar order decision. Authored moderate makes three independent first–third-order decisions with source-root/power/product distractors and source prime notation. Authored hard is a design claim, not a recovered difficulty: three fourth–eighth-order decisions scan four derivative occurrences per equation, mixed notation, both-side placement, and a derivative power/product. Higher derivatives through8 are explicitly observed at easy; derivative powers/products, roots and both-side scanning are observed at moderate. Hard combines those existing notation prerequisites with increased scan bookkeeping; it introduces no new method. Within hard every equation has four derivative occurrences, one powered highest derivative and one product. Layout changes retain that demand.

Source anomaly: q-167787 prints RHS f(x), but its worked solution restates RHS (1/2)e^x. The order4 conclusion remains valid. Raw observed replay preserves all text; the separate source_repaired profile replaces that unsupported RHS by f(x). No scalar mathematical answer is repaired. All source-profile records remain evidence-only, including repaired replay; authored defaults are eligible for learning.
'''
(H/'classification.md').write_text(intro)
parts=['''# Template extraction — all four stages

Provenance matches source.json: math basis1356, captured lineage. Original prompt, exact field shapes, complete bank and whole solution follow for every practice case. No source is omitted. Exact whitespace in the blank is preserved by source.json and public observed replay; code fences below show decoded strings.

## Stage1 — describe originals before generalizing
''']
choice_ledger=[]
for sid,q in g.ORIGINALS.items():
 level=q[':question/difficulty'][':db/ident'].split('/')[-1];ds=g.derivatives(q[':question/problem']);p=g.source_parameters(sid)
 parts += [f'### {sid} / {level}\n\nDerivative occurrence orders, in printed order: '+str([d[2] for d in ds])+'. Independent variable x and dependent function y=y(x); all derivatives are ordinary. Positive integer polynomial powers and simple coefficients/functions are visual context, not differentiation tasks. No reduction or cancellation removes a derivative term.\n\nPrompt:\n\n```text\n'+q[':question/problem']+'\n```\n\nFull worked solution:\n\n```text\n'+q[':question/worked-solution']+'\n```\n\nFields and complete observed bank:\n\n| Field | Type | Answer type | Every original value | Correct |\n|---|---|---|---|---|\n']
 for f in q[':question/answer-fields']:
  kind=f[':answer-field/type'][':db/ident'];values=[a[':answer/value'] for a in f[':answer-field/choices']];correct=f[':answer-field/correct'][':answer/value']
  parts.append('| '+f[':answer-field/key']+' | '+kind+' | '+','.join(sorted({a[':answer/type'][':db/ident'] for a in f[':answer-field/choices']}))+' | '+', '.join(values)+' | '+correct+' |\n')
  for a in f[':answer-field/choices']:
   boolean=kind.endswith('/checkbox');off=None if boolean else int(a[':answer/value'])-int(correct)
   recipe=('boolean candidate '+a[':answer/value']+'; correct iff printed highest order matches requested target' if boolean else f'n + ({off}), n=highest displayed derivative order')
   choice_ledger.append({'source_id':sid,'field_key':f[':answer-field/key'],'field_type':kind,'original_answer_uuid':a[':answer/id'],'value':a[':answer/value'],'correct':a[':answer/id']==f[':answer-field/correct'][':answer/id'],'profile':'observed/'+sid,'parameters':p,'recipe':recipe,'interpretation':'finite true/false response catalog' if boolean else 'source relative-order value catalog; misconception intent underdetermined','reproduces_complete_value':True})
 parts.append('\nSource solution stages: '+str(len(q[':question/worked-solution'].split('\n\n')))+' double-newline paragraphs; exact sentence sequence above. '+('Definition → identify highest derivative and order → conclusion; q-167787 additionally restates an equation and includes whitespace paragraphs.' if level=='easy' else 'Target-order definition → invitation to check → I classification → II classification → III classification → selected-set conclusion.')+' No solution-stage omissions introduced.\n')
parts.append('''
## Stage2 — shared pattern and response

Scalar: recognize each formal Leibniz derivative, read its differentiation order, take the maximum across the full equation, and return that integer through the original radio or blank. Ordinary x/y exponents and coefficient functions do not determine order. Three-way selection: read requested order and independently compare it with the largest prime/Leibniz derivative in each equation; preserve one checkbox field for each I/II/III. Products, powers or a square root containing a derivative do not change the derivative's order. Nothing is differentiated or solved.

## Stage3 — components and complete original choice mapping

`choice-recipes.json` maps all73 original choices to owning field, original UUID, exact value, correct designation, recipe, original parameters and bank profile. It is generated from immutable source evidence and cross-checked by validate.py, not an answer lookup used by generation. Source numerical offset recipes are interpretation-limited explicit replay catalogs; no arbitrary numerical regression is promoted as a historical error operation. Source checkbox banks always contain false and true. Their keys remain I/II/III and their correct choice derives from printed highest order equal to target. The blank contains a single math answer and retains {{field-1}}.

The source renderer masks **whole derivative components**, including their full numerator and denominator. It also slots complete ordinal words in prose and the whole $n.$ order fragment in scalar conclusions. No blind coefficient substitution touches prose, function names, labels or derivative arguments. Variable/component notation style remains exact whenever order is unchanged; changed prime orders above3 switch to unambiguous Leibniz notation. No derivative-free equation can be generated.

## Stage4 — reusable masks, domains and computations

Public observed replay: template is the source ID, profile observed; parameters are a complete `orders` dictionary from old source order to new order. Values are integer1–8, strictly increasing in old-order order; every source-relative radio option must stay positive, distinct, and include the new highest exactly once. Thus preserved source sentence truth and selected-set layout remain valid. The entire complete bank is chosen before rendering and rejected together on collision/domain failure. Original maps are identity maps; every source is also tested with a nonidentity map through the same public API. Raw q-167787 RHS prose anomaly remains visible; source_repaired changes only the wrong restated RHS.

Authored easy: n3–7; m1–n−2; ordinary exponent e in n+2..9. Left layout yD_n+3xD_m=x^e; right layout x^eD_m−3x=yD_n. Both have exactly two derivative occurrences. Correct n; complete bank [n,m,e,n−1,n+1]. Wrong operations read lower derivative, read an ordinary exponent, or count one too few/many differentiations. All five values are distinct under the bounds; the profile is selected as a whole. The source numerical banks motivate recognition of ordinary exponents and nearby order labels, without asserting recovered intention. Seventy meaningful bounded tasks are exhaustively checked; coefficient and variable aliases do not inflate counts.

Authored moderate: target and each of three highest orders1–3, forms0–2. Per-equation forms are D_n+3xD_1=x^5 y; sqrt(D_n+x)=3y^4; (D_n)^2+xD_1=y^5. Same first–third-order membership judgment in all forms, with one or two derivative occurrences; prime glyphs match observed source conventions. All2187 semantic parameter combinations are exhaustively checked. The second form reduces derivative occurrence count as in observed q-118782 but still requires reading derivative under a radical rather than confusing its power/placement with order.

Authored hard: target and each highest order4–8; lower m1..n−2; highest-derivative power2–5; ordinary exponent e in n+1..10; layout0–2. Define A=D_m(D_n)^p, B=x^eD_1, C=yD_(m+1). Layouts are A+B=C, A=B+C, B+C=A. Each has exactly four derivative occurrences; orders m and m+1 are lower than n, and highest power and ordinary exponent are irrelevant to true order. Boolean bank and full definition/check-each/conclusion solution remain fixed independently of a selected learner error. The factorized finite catalog has840 genuinely distinct per-equation structures, independently enumerated and parsed. Ordered three-equation tasks with five target orders total5×840³=2963520000; this is a factorized bound, not a claim to render billions of questions. Powers/exponents and equation-side placement are retained because they create distinct order-versus-exponent/read-all-terms recognition tasks; symbol names, coefficients, profile and seed are excluded.

Mathematics reads back actual displayed derivatives independently in validate.py; exact derivative counts are confirmed with SymPy. Public generation stores domain, complete recipe set, source lineage, actual Python/SymPy versions, seed and original parameters outside learner content. Mathematical task identity excludes bank/profile/seed and coefficient magnitudes; content identity includes version, level, actual prompt, entire fixed solution, full displayed bank and correct values. Shuffling radio options cannot change identity. Distinct non-order coefficients are not exposed as purported task diversity.

All original profiles and variants appear in review.md/review.json, followed by at least two clearly labeled authored examples per level. No plots, native engine edits, database writes or post-step7 registration occur.
''')
(H/'template-extraction.md').write_text('\n'.join(parts))
(H/'choice-recipes.json').write_text(json.dumps(choice_ledger,ensure_ascii=False,indent=2)+'\n')
(H/'plot-extraction.md').write_text('# Plot extraction/specification\n\nAll14 decoded prompts,73 answer values and14 complete worked solutions contain no plot references, images, diagrams or graph-reading demand. Plot rating none at every observed/authored level. No plot parameters, assets, renderer or direct SVG generation are needed.\n')
(H/'README.md').write_text('''# ODE-order generator

Run from repository root:

```sh
.venv/bin/python generate/scratch/17592186166813/validate.py
.venv/bin/python generate/scratch/17592186166813.py --difficulty all --seed 42 --count 2 --format markdown
```

API: generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None), plus generate_easy/moderate/hard. Source replay uses template=source_id, profile="observed", parameters from source-cases.json. Authored defaults use single/selection/mixed_selection and profile="authored". Invalid explicit parameters raise ValueError; they are never replaced by sampled values. JSON records are local review artifacts, never transactions.

Scope is recognition of the highest displayed ordinary derivative only. Easy/moderate observed; hard authored from existing higher-derivative notation plus sourced derivative power/product and full-equation scanning. Source opaque numeric catalogs remain evidence-only. q-167787 restated RHS anomaly has a separate source_repaired profile; source order answer itself is unchanged. All learner eligible defaults use authored complete banks and clean solutions. No solving, ODE linearity/autonomy, IVP/PDE branch or plots.

Frozen version ode-order-frozen-1. Evidence includes source wrapper, full extraction and73-choice mapping, original parameter replay cases, changed-source recipes, source-fidelity results, explicit finite-domain QA, native input/report, labeled review and dependency/hash freeze. Validation compares every original prompt, solution and field/bank with source evidence, checks displayed order via an independent reader and SymPy, tests every native choice plus equivalent/wrong blank entries, and fails on mismatch. Historical distractor intention is explicitly unresolved; exact source values are not a recovered authorship claim.
''')
