import json
from pathlib import Path
P=Path(__file__).resolve().parent
x=json.loads((P/'source.json').read_text());source=x['record'][':knowledge-point/questions'];ts=json.loads((P/'templates.json').read_text())
(P/'classification.md').write_text('''# Classification

Database math, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`, source basis '''+str(x['basis'])+'''. All 13 source practice questions and the canonical example were read together, with difficulty, complete fields/banks/correct references and worked solutions. No source images or plots occur. No generated input file existed for the requested job.

Easy has six source questions with radio and blank fields. Four Markdown/solution families: inline integer-power radio (q-5962, q-152755; two profiles), evaluate integer-power radio (q-152758; one profile), shortened inverse-square radio (q-100310; one profile), and explicit exact-answer blank (q-350322, q-350324; no distractor profile). Variations in exponent-one simplification are conditional layout features. All plot ratings are none.

Moderate has seven source questions with radio and blank fields. Five families: radical radio with integer numerator (q-152777), evaluate radical radio (q-152762), radical radio with reciprocal coefficient (q-152754), explicit exact-answer radical blank (q-350331, q-350333, q-350337), and a rational-function blank (q-128340). Each radio family has its own complete source bank. All plot ratings are none.

q-128340 is defective in the available source: its prompt contains only an integral of undefined f(x). Its worked solution reveals 7/(2x²-5x-3), but neither the function definition nor an image appears in the prompt. The solution/answer ln(9/2) is mathematically correct for that revealed integrand. Exclude this source from generator and validated inventory; preserve its database facts unchanged. Do not pretend it is a complete standalone task.

Hard has no observed question or template. Absence alone does not prove impossibility. This frozen package makes a bounded unsupported-hard declaration: no demonstrated hard template or validated sampling policy. New source evidence reopens classification.

Implementation keeps 12 source layouts as fixed-parameter subtemplates. They are not 12 independent mathematical families. Template count, bank profile count, and fixed-parameter implementation branches are different quantities.
''')
text='''# Template extraction

The common task is to evaluate a convergent upper-limit improper integral of C x^(-p), with C>0, p>1 and lower endpoint L>0. First replace infinity by a, rewrite a radical as a rational power where needed, integrate using the power rule, evaluate the endpoints, then let a tend to infinity. The exact answer is C L^(1-p)/(p-1). For real radicals the positive integration domain avoids branch ambiguity. No new or reused plot assets are required; stage 5 and 7 plot work is inapplicable.

Every source question's original Markdown, answer shape, complete field-owned bank, correct reference and exact fixed solution are retained in source.json. templates.json lists every source answer ID, value, type, correct designation, coefficient-scaled expression, and profile. No pooled/mixed banks are used. The proportional observed recipes reproduce complete source mathematical values; their error interpretations remain unresolved. They are recorded as observed patterns rather than asserted misconception theories. There is no unresolved algebraic source-bank comparison.

The extracted templates hold exponent, endpoint, variable, root degree, expression layout, and solution sequence fixed in each subtemplate. @INTEGRAND@, @C@, @K@ and @V@ vary together. K=C/(p-1) and V=K L^(1-p). Each complete radio bank scales each original math value by C/C0; its text divergence option is unchanged when present. Blank answers are just the exact scalar, with no added distractors or feedback. The source instructional sentences and source notation are unchanged. Parenthesized versus unparenthesized primitives and the shortened inverse-square sequence remain separate layouts.

The proposed sampling policy is deliberately narrower than unrestricted power-law integrals: C is an integer from 1 to 2000, except q-152754 uses C=1/D with 2<=D<=2000. Every observed coefficient lies in its corresponding policy. Across the set of fixed source subtemplates, every observed exponent, endpoint and variable is covered. Negative or zero coefficients, new endpoint values, new exponents, and divergence tasks are excluded. Changed positive coefficients produce different integrands and different exact answers, not seed-only or formatting-only variants.

## Source-specific components

|Source|Level|C|p|L|Variable|Response/layout|Profile|
|---|---|---:|---:|---:|---|---|---|
'''
for t in ts:text+='|'+ '|'.join(map(str,[t['source_id'],t['level'],t['source_coefficient'],t['exponent'],t['lower'],t['variable'],t['field_type'].split('/')[-1]+'/'+t['layout'],t['bank_profile'] or 'none']))+'|\n'
text+='\nThe 13th source, q-128340, uses partial fractions of 7/((x-3)(2x+1)) on x>=4, with log-difference primitive and logarithmic limit. It requires a separate rational-function template. Its missing prompt definition is retained as evidence, and this frozen package excludes the family explicitly. The canonical e-511 uses C=8,p=5,L=2 and yields 1/8; it supports the common method but does not count as practice.\n'
(P/'template-extraction.md').write_text(text)
cap={'supported_levels':['easy','moderate'],'unsupported_levels':['hard'],'reason':'No observed hard source/template or validated hard sampling policy; bounded package capability, not mathematical impossibility.','nominal_unsupported_shortage':{'hard':5},'unsupported_levels_filled':False,'excluded_source_ids':['q-128340'],'excluded_template':'Rational blank with undefined f(x); source facts are preserved.','sampling_policy':'Fixed p,L and source layout per subtemplate; only positive coefficient varies. Integer C in [1,2000], reciprocal C=1/D with D in [2,2000] for q-152754.','finite_distinct_tasks':{'easy':12000,'moderate':11999},'task_fingerprint':'Normalized coefficient, exponent and lower endpoint; excludes seed, identity, bank, variable spelling and option order.','evidence':['source.json','templates.json','classification.md','template-extraction.md','validation.json']}
(P/'capabilities.json').write_text(json.dumps(cap,indent=2)+'\n')
(P/'README.md').write_text('''# Upper-limit improper integral generator

Script: `generate/scratch/17592186083195.py`. Validated source basis: '''+str(x['basis'])+'''. Generator UUID is deterministic under the existing KP UUID and retained by registration. Source questions, canonical example and learner history are immutable here.

Run `python3 generate/scratch/17592186083195.py --difficulty easy --count 5 --seed 42 --format json`. Moderate is also supported. Hard raises an explicit unsupported-level error. Output is an object with instances; each instance carries the existing question/field/owned-answer representation and separate reproducibility metadata. Run `.venv/bin/python generate/scratch/17592186083195/validate.py` for source replay, symbolic verification and actual native grading.

See classification.md, template-extraction.md, templates.json and capabilities.json for bounded coverage; review.md shows originals replayed next to coefficient variants. Validation reports fidelity, correctness and actual grading separately. check-engine was compiled from the existing application harness and current application release library, and does no database operations. Native grading accepts canonical exact values and plain equivalent rational entries, and rejects wrong values. The numeric policy does not require general symbolic-expression grading.

Only fresh, distinct mathematically validated tasks may be committed. Deduplicate by coefficient/exponent/endpoint independently of authored bank and notation. Registration alone can resolve this classify job when supported stock already meets quota; unsupported hard remains explicit in the result. reference/replenishment retains exact requests, speculative previews, durable receipts and exact-basis readback. api.lock serializes the inventory recheck, submission and readback with the application.
''')
