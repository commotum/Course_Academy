import pathlib,json,importlib.util
D=pathlib.Path(__file__).parent
spec=importlib.util.spec_from_file_location('g',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
s=json.loads((D/'source.json').read_text());qs=s['record'][':knowledge-point/questions'];recipes=json.loads((D/'recipes.json').read_text())
lesson=json.load(open('generate/runs/current/lessons/17592186048445.json'))['record'][0];steps={q[':db/id']:q for q in lesson[':activity/steps']};route=[];cur=lesson[':activity/first-step'][':db/id']
while cur in steps:
 node=steps[cur];content=node[':step/content'];route.append(content.get(':tutorial/title',content.get(':knowledge-point/title')))
 if ':step/next' not in node:break
 cur=node[':step/next'][':db/id']
classification='''# Classification at math basis 1356

Lineage: 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1. All 15 practice records and the canonical example were examined. There are 8 moderate and 7 hard sources, no easy sources, no unrated practice records and no field anomalies. Eleven sources have malformed unescaped literal system braces, repaired to visible escaped braces in generated prompts and solutions. Every source has one radio field named selection, five whole equations k=value, and one correct designation. The canonical example is context, not a sixteenth practice question.

| Level | Template | Response / work | Sources | Plots |
|---|---|---|---|---|
| easy, authored | inconsistent_easy | 2 equations, a=1, coefficient k; integer elimination and contradiction | none | none |
| moderate | inconsistent_bare | coefficient k; one integer elimination | q-32245, q-32331 | none |
| moderate | inconsistent_shift | coefficient k+v; one integer elimination | q-42059, q-131726, q-74646 | none |
| moderate | inconsistent_scaled | coefficient uk; one integer elimination | q-131727, q-74688 | none |
| moderate | inconsistent_scaled_shift | coefficient uk+v; one integer elimination | q-131728 | none |
| hard | dependent_swap | swap to unit pivot, eliminate, identify free variable | q-32246, q-131729, q-74695, q-131730 | none |
| hard | dependent_fractional | fractional elimination, shifted k, identify free variable | q-131731, q-74650 | none |
| hard | dependent_negative | negative affine parameter coefficient, eliminate, identify free variable | q-42021 | none |

The seven observed mathematical templates have fifteen complete observed bank profiles. Wording, alignment, row-operation sign style and white-space variants remain per-source presentation masks. They do not claim additional skills. No source options are pooled. All raw original prompts, solutions, fields and banks are preserved in source.json, and all replay through the normal generator interface.

## Curriculum and missing easy level

The route reconstructed from activity/first-step and step/next is:

'''+ ' → '.join(route)+'''

The preceding classification tutorial defines inconsistency, dependence and independence. The sibling solving KP uses general NxM elimination and free variables; this KP asks only for k, never a general solution. The later null-space/span topics are excluded. Canonical e-4712 is a two-equation inconsistent system requiring one integer row subtraction and a contradiction. Authored easy retains this exact demand with unit first pivot, bare k, |b|≤4, |d|=2 or 3, small integer constants, and a nonzero residual. This is a design claim, not an observed label. Easy questions differ in multiplier sign, y-coefficient sign and contradiction value, without a within-level progression. Moderate remains the observed inconsistent affine-k problem with integer row multiplier. Bare-k moderate requires |a|≥2, matching the observed non-unit pivots and preventing overlap with the authored easy workload; shifted/scaled families retain observed unit pivots because their k-rearrangement or division adds the observed moderate demand. Hard remains observed dependence with swap, fractional multiplier or negative affine coefficient; every hard instance has proportional constants and one free variable. All explicit parameters obey the same bounds as samplers.
'''
(D/'classification.md').write_text(classification)
text=['# Template extraction: four stages\n\nSnapshot provenance is retained unchanged in source.json. Recipes are arithmetic patterns, not a reconstruction of proprietary authoring code. No scalar bank is promoted to normal default solely because it matches an isolated source.']
text+=['## 1. Specific source descriptions\n\nAll systems use real x,y and a real parameter k; no determinants, eigenvalues, additional unknowns or higher-degree parameter branches are introduced. Exact integers/fractions are retained.']
for q in qs:
 sid=q[':question/math-academy-id'];r=recipes[sid];p=r['parameters'];style=r['style']
 text+=['### '+sid, q[':question/problem'],f"Source database ID {q[':db/id']}; observed {r['level']}; template `{r['template']}`; parameters `{p}`. Row swap: {style['swap']}; row-operation notation: {style['rowop']}. The worked sequence has an initial augmented matrix, repeated initial matrix plus operation, {'a swapped matrix plus second operation, ' if style['swap'] else ''}a row-echelon matrix, corresponding two equations, classification rationale, special k value, and concluding sentence. Hard sources also remove the zero equation and identify basic x/free y."]
text+=['## 2. Shared mathematical description\n\nFor a x+b y=c and d x+(u k+v)y=e, eliminate x. The second row is [0,u k+v-(d/a)b,e-(d/a)c], except the swap family first places the unit second row above the first and produces [0,b-a k,c-a e]. The parameter makes the remaining y coefficient zero: k=((d/a)b-v)/u. A nonzero residual yields inconsistency; zero residual yields one equation in two variables and dependence. The response is always the complete equation k=value. Fixed teaching prose follows each original with a single solution independent of the selected option.']
text+=['## 3. Components and complete banks\n\nEach source field is radio `selection`. Correct value is computed from the prompt before constructing the complete bank. In the tables r=d/a, t=((d/a)b-v)/u, h=e-r c. Expression-pattern intent is explicitly unresolved for opaque offsets; these are observed replay profiles only, never authored default recipes. Complete numeric reproduction alone is not an error-model claim.']
import sympy as sp
for q in qs:
 sid=q[':question/math-academy-id'];r=recipes[sid];p=r['parameters'];env={k:sp.Rational(v) for k,v in p.items()};env['r']=env['d']/env['a'];env['t']=(env['r']*env['b']-env['v'])/env['u'];env['h']=env['e']-env['r']*env['c']
 text+=['### Bank '+sid,'| Field | Original answer UUID | Original full value | Parameterized expression | Correct |\n|---|---|---|---|---|']
 for a,expr in zip(q[':question/answer-fields'][0][':answer-field/choices'],r['bank']):
  # Source order was captured at recipe extraction; table covers every option.
  value=sp.sympify(expr,locals=env);assert g.tex(value)==a[':answer/value'].split('=',1)[1]
  correct=a[':answer/id']==q[':question/answer-fields'][0][':answer-field/correct'][':answer/id']
  text += [f"| selection | {a[':answer/id']} | `{a[':answer/value']}` | `k={expr}` | {correct} |"]
 text += ['Atomic mathematical components: '+', '.join('`'+key+'`' for key in g.components(p,r['style']))+'. The exact prompt and complete ordered solution masks are in recipes.json.']
text+=['''## 4. Reusable template and constraints

Fixed components: determine-k prompt, two aligned equations, augmented matrix, Gaussian elimination sentence, classification definition, final sentence; dependence adds the fixed removal/basic/free-variable paragraphs. Variable components are complete equations, whole matrices, full row operation, reduced equation, k equation and zero-row equation. Optional swapped stage belongs only to dependent_swap. All objects derive from the same a,b,c,d,u,v,e. Masks never replace a bare numeral or expression substring. Whitespace and per-source sentence differences are kept in masks.

The generator performs exact SymPy arithmetic and samples signed integers, preserving an integer multiplier for moderate and a fractional multiplier for dependent_fractional. Every bank is selected as a complete set before validating options; collisions reject the whole instance. Explicit input rejects invalid domains instead of resampling. Bounds are enforced in validate_parameters. Source replay profiles remain arithmetic expression patterns outside normal defaults. Authored default banks are method based:

- easy/bare/scaled: t, -t, b/u, -b/u, 0 (sign error, omitted elimination multiplier, sign plus omitted multiplier, setting parameter zero).
- shifted moderate: t, -t, r b/u, -v/u, (r b+v)/u (root sign, omitted shift, omitted row contribution, wrong shift sign).
- swap hard: t, -t, 1/t, b, 0 (sign, reciprocal ratio, omitted pivot coefficient, zero).
- other hard: t, -t, -v/u, (b-v)/u, 0 (sign, omitted row contribution, omitted multiplier, zero).

These banks are authored extensions and contain five unequal values. There is no learner-facing error diagnosis. Integers and reduced rationals are exact. No unused plot parameters exist. Mathematical identity uses the full symbolic augmented-system row space plus singular parameter, independent of level, excluding banks/profile. Presentation identity uses version, level, template, parameters, full prompt, full fixed solution and unordered full answer bank; changing seed only shuffles options.

## Source errors and repairs

q-74695: original corresponding system and remaining-equation prose say x+ky=2 while prompt, initial matrix and swapped pivot are x+ky=-2. Both incorrect occurrences are repaired to -2. Correct k and bank are unchanged.

q-42021: original initial augmented matrix says first RHS -3 while prompt and elimination matrix say +3; repair to +3. The corresponding first equation is printed 1-2y=3, incompatible with either row; repair to x+2y=3. Reduced row -(k-5)y=0 is preserved (equivalent to the matrix coefficient -k+5). Correct k and bank are unchanged.

Raw evidence remains in source.json and originals in review.md. Four of fifteen original prompt strings and three original solution strings are byte-exact. After escaping the malformed system braces, fifteen prompt strings and thirteen full source solution strings match; after the two mathematical repairs as well, all fifteen full solution strings match. Matrices and row operations retain their original stage count and notation. No incorrect teaching rules are copied to normal output. Raw source masks retain captured literal left-system braces as evidence. Rendering escapes every unescaped left-system brace in observed replays; authored masks already use escaped visible braces. This presentation repair prevents unclosed TeX groups. All remaining component groups and math delimiters must balance.
''']
(D/'template-extraction.md').write_text('\n\n'.join(text)+'\n')
(D/'plot-extraction.md').write_text('# Plot extraction and generator disposition\n\nAll 15 practice prompts, answer banks and worked solutions were read. They contain inline/display LaTeX systems and matrices, no plotted geometry or referenced image assets. Plot rating is none for every observed and authored template. Steps 5 and 7 require no plot specifications or renderer. Canonical image references represent static mathematical notation; their mathematical contents are redundantly given by its row-elimination display and final paragraph. They are not question plots or parameter-dependent assets used by this generator.\n')
(D/'README.md').write_text('''# KP17592186115242 local generator

Run from repository root:

```sh
.venv/bin/python generate/scratch/17592186115242/validate.py
.venv/bin/python generate/scratch/17592186115242.py --difficulty all --seed 4 --count 2 --format markdown
```

All three difficulties; no database access or registration. Seven observed templates, fifteen five-choice radio banks, one missing-level authored easy template, and method-based authored default banks. Observed profiles replay via `generate(level, parameters=..., profile="q-...")` using source-cases.json. Opaque observed bank intent remains unresolved and is not used for normal defaults. Two source mathematical solution errors and eleven source system-brace presentation errors have explicit repairs. Exact and repaired fidelity counts are reported separately. Validation independently parses printed equations, every printed matrix and row operation, all answer values and solution statements; fidelity and native radio grading are counted separately. Review includes every original, replay and changed-profile variant, and two authored defaults of each template.
''')
