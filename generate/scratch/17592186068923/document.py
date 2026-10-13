"""Emit scoped evidence from the captured source bank, keeping every choice."""
import importlib.util,json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
spec=importlib.util.spec_from_file_location('g',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
s=g.source_package();rows=[]
for t,q in g.sources().items():
 N,g1,g2,lo,hi,A,B,a,b,F,answer=g.math_data(t,1);field=q[':question/answer-fields'][0]
 rows.append({'source':t,'db_id':q[':db/id'],'observed_difficulty':q.get(':question/difficulty'),'generator_difficulty':g.DATA[t][0],'numerator':str(N),'denominator_factors':[str(g1),str(g2)],'expanded_denominator':g.DATA[t][-1],'bounds':[str(lo),str(hi)],'coefficients':[str(A),str(B)],'log_coefficients':[str(a),str(b)],'exact_answer':str(answer),'original_problem':q[':question/problem'],'original_solution':q.get(':question/worked-solution'),'field_key':field[':answer-field/key'],'field_type':field[':answer-field/type'][':db/ident'],'profile':t if len(field[':answer-field/choices'])>1 else None,'choices':[{'source_field':field[':db/id'],'source_answer':c[':db/id'],'source_value':c[':answer/value'],'complete_value':str(g.p.scalar(c[':answer/value'])),'recipe':'m * ('+str(g.p.scalar(c[':answer/value']))+')','source_correct':c[':db/id']==field.get(':answer-field/correct',{}).get(':db/id'),'interpretation':'Observed exact expression transported under amplitude; misconception unresolved; log base frozen, not inferred.'} for c in field[':answer-field/choices']]})
(HERE/'template-extraction.json').write_text(json.dumps({'basis':s['basis'],'lineage':s['lineage'],'sources':rows},indent=2)+'\n')
(HERE/'classification.md').write_text('''# Classification

Math lineage 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1, basis 1978. All 14 practice sources, canonical e-507 and generator lookup read together. No registered generator, scratch package or supplied .generated file. Native inventory requests classification only: moderate/hard currently have no shortages.

| Difficulty | Fields | Markdown/value templates | Bank profiles | Plot rating |
| --- | --- | --- | --- | --- |
| Moderate | radio selection; blank field-1 | 5 rated source contracts + 1 local unrated completion | 4 radio banks, 2 blanks | none |
| Hard | radio selection; blank field-1 | 8 source contracts | 4 radio banks, 4 blanks | none |
| Easy | none observed | 0 supported | 0 | none |

Source render and solution contracts are kept separate, even where a broad mathematical family is shared. Moderate factorization is supplied; hard factorization is expanded and may have nonmonic linear factors. q-128238 has a repeated integral and starts from known partial fractions; q-347077 asks for an exact blank. Factored radio q-49764 uses an equation prompt; q-49765 and q-49769 use Evaluate prompts and different log-coefficient banks. Hard q-49761/q-75825/q-75828 use a line break; q-49762 has a one-line Evaluate prompt. Hard exact blanks q-348975/q-348976 have monic factors with rational coefficients; q-349040/q-349041 require nonmonic factor integration. Every source is identified with its complete contract in template-extraction.json.

Unrated q-49766 has no correct marker, difficulty or solution. Its two partial-fraction coefficients are both one. The exact endpoint result is ln(16/3), uniquely matching the original bank. It is classified moderate locally alongside the factored-denominator sources, with an authored fixed solution; original evidence remains unchanged. Canonical e-507 supports nonmonic factorization but is excluded from practice stock.

Easy is unsupported by this bounded package. Its five-question reserve remains unfilled; lack of source evidence does not prove mathematical impossibility. New source evidence reopens classification.
''')
(HERE/'template-extraction.md').write_text('''# Template extraction

Each source is described before generalization in template-extraction.json: exact forms, signs, factors, bounds, coefficients, original Markdown/solution and every field-owned option. Each radio source defines one complete profile; no recipes are pooled. All 40 radio options, including 32 distractors, are accounted for by exact mathematical expression. Six blanks have no distractor profile.

Shared move: decompose a rational function with two distinct linear denominator factors, integrate logarithms with absolute values, then evaluate exact bounds in one pole-free real interval. Required response is one scalar exact value, via the source field contract. Signs, zero/nonzero endpoints, rational endpoints, monic/nonmonic factors and expanded/factored denominator presentation are fixed for each contract.

The bounded sampler uses an integer amplitude m=2..6. The numerator is multiplied by m; the denominator, endpoints and their domain remain fixed. Partial-fraction coefficients, log coefficients, endpoint result and every complete source-bank expression are multiplied by m. m=1 is source replay. This covers the original parameter values and preserves all signed shifts and scales; it is deliberately narrower than a new factor/bound sampler. Every exact bank recipe is m times its recorded source expression, including compound constants inside logarithms. Bases are frozen observed values, not inferred misconception recipes. Correctness and uniqueness are checked before output. The source profile is selected before its bank. No mixed banks are permitted.

Fixed components: field key/type/count, source instructional prose, endpoint domain, factorization workload and math-stage ordering. Variable components: numerator, solved coefficients, primitive, endpoint rows and complete values. Twelve source replay solutions are exact; q-49761 has its mixed-bound typo corrected locally, and q-49766 has a locally authored solution. Variant equation rows are compacted while retaining all source instructional sentences and their order; this layout variation is recorded separately from complete bank fidelity. Historical double-escaped Markdown is normalized in generated copies for rendering.

Source q-49761 error: an indefinite integration row incorrectly includes 2 integral from 2 to 3 of 1/(x-4). The primitive row and final answer ln(7/24) establish that it should be 2 integral of 1/(x-4) without bounds. Generated replay removes those bounds; all originals remain intact.

Mathematical identity hashes use the exact canceled printed integrand and both exact bounds; seed, choice order and UUID never establish a new task. Stable IDs include the whole source profile, and database selection additionally excludes any existing mathematical task regardless of profile. All finite candidates are validated. Exhaustion leaves shortages explicit.
''')
(HERE/'plot-extraction.md').write_text('''# Plot extraction

All captured practice and canonical Markdown, fields and solutions inspected. They contain LaTeX mathematical expressions and no image/diagram references. Every template has plot rating none. No new or reused plots and no asset publication are required.
''')
(HERE/'README.md').write_text('''# Definite rational integral generator

Run from the repository root:

```sh
.venv/bin/python generate/scratch/17592186068923.py --difficulty moderate --count 5 --seed 1978 --format json
.venv/bin/python generate/scratch/17592186068923/validate.py
.venv/bin/python generate/scratch/17592186068923/replenish.py
```

Moderate and hard are supported, with 30 and 40 finite mathematical tasks respectively. Easy is unsupported and its reserve remains explicit. Complete source evidence, per-choice extraction, full replay, exhaustive symbolic and actual learner grading checks, side-by-side review and exact commit requests/receipts are scoped to this KP. Replenishment is additive, checks current inventory under api.lock and retains it through submission and exact-basis readback. Source questions and history are preserved; application/ca-engine owns generated facts. No content is committed when current supported reserves already meet their rolling minima.
''')
print('Wrote classification/extraction/plot evidence for',len(rows),'sources')
