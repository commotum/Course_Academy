from pathlib import Path
import importlib.util,json
ROOT=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('g',ROOT.with_suffix('.py'));g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g)
raw=json.loads((ROOT/'source.json').read_text());questions=raw['record'][':knowledge-point/questions'];cases=json.loads((ROOT/'source-cases.json').read_text())
classification='''# Classification at math basis 1356

Snapshot lineage: 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1. The wrapper is preserved in source.json; topic.json and lesson.json preserve curriculum context.

13 practice questions: 11 observed easy (8 single-field blanks and 3 single-field five-option radios), 2 unrated five-option radios. The unrated questions are analyzed and replayed with explicitly authored easy placement. There are 12 observed Markdown/value templates and 5 complete radio profiles. q-319909 and q-319903 share the right-fragment polynomial–exponential template, with conditional prime notation. Positive and negative exponential–logarithmic left blanks preserve distinct notation masks. Neither source has plots; rating is none for every template, and no renderer is needed.

Lesson route follows first-step 17592186097425 and next links: Introduction -> trigonometric-product KP -> this exponential/logarithmic-product KP -> Leibniz Notation -> tangent-slope KP. Pull array order is not used. The Introduction explicitly derives two component derivatives and distributes two products. The canonical example x² ln x demonstrates power plus logarithmic factors and four derivative stages. Exponential/logarithmic differentiation are the key prerequisites. Trigonometry occurs only in already-observed exponential/trig or log/trig products. The sibling tangent-slope KP and subsequent quotient-rule topic are excluded.

Moderate and hard levels are authored scope claims because no such labels occur here. Moderate peers replace the atomic polynomial factor with two nonzero monomials; hard peers use three nonzero terms (two powers plus a constant). Both keep exactly one product-rule application, elementary exponential/logarithmic derivatives and finite distribution; there are no nested/composed arguments, quotient derivatives, evaluation-at-a-point tasks, or tangent lines. Exponential and logarithmic factors are unordered peers at each level. Moderate n=2..4, 1<=m<n and |a|,|c|=1..5. Hard has the same power/coefficient bounds and also nonzero |h|=1..5. These require two versus three substantive components in the polynomial factor, even where collection simplifies the result. Signed coefficients never remove the defined workload. Full derivative blanks at authored levels are explicit extensions, distinguished from observed fragment blanks.

| Template | Level status | Field | Sources | Profile | Plot |
|---|---|---|---|---|---|
'''
for t,(level,ft,ids) in g.TEMPLATES.items():classification+='| '+t+' | '+('observed easy / missing label' if t in ('log_log_radio','power_log_radio') else 'observed '+level if ids else 'authored '+level)+' | '+ft+' | '+', '.join(ids)+' | '+str(g.PROFILES.get(t,'none'))+' | none |\n'
(ROOT/'classification.md').write_text(classification)
text='''# Template extraction

## Stage 1: specific source descriptions

All original strings and fields appear below and in raw source.json. No source was omitted. Numbers, notation, fragment location, full option ownership and exact mathematical values are preserved. Parameters listed here are observed values, not recovered sampling code.
'''
for case,q in zip(cases,questions):
 t=case['template'];p=case['parameters'];pr,sol,bank,u,v,rows=g.build(t,p)
 text+='\n### '+case['source_id']+'\n\nParameters: `'+json.dumps(p)+'`; template `'+t+'`; profile `'+str(case['bank_profile'])+'`.\n\n'+q[':question/problem']+'\n\nField: `'+q[':question/answer-fields'][0][':answer-field/type'][':db/ident']+'`; key `'+q[':question/answer-fields'][0][':answer-field/key']+'`.\n\n'
 text+='Original worked solution:\n\n'+q.get(':question/worked-solution','Absent. The four-row solution in generated replay is authored from the displayed product; it is not counted as source solution fidelity.')+'\n\n'
 text+='| Original option (exact bytes after JSON decoding) | Parameterized recipe | Designation |\n|---|---|---|\n'
 for (value,e,recipe),answer in zip(bank,q[':question/answer-fields'][0][':answer-field/choices']):
  # Choice pull order can differ: find original by complete value instead.
  original=next(a for a in q[':question/answer-fields'][0][':answer-field/choices'] if a[':answer/value']==value)
  text+='| `$'+original[':answer/value']+'$` | '+recipe+'; exact expression `'+str(e)+'` at these parameters | '+('correct, derived because original ref absent' if recipe=='correct' and case['correct_ref_status']=='independently_derived' else 'correct' if recipe in ('correct','fragment') else 'distractor')+' |\n'
text+='''
## Stage 2: shared mathematical pattern

Identify u and v from a displayed product containing an exponential or logarithmic function, differentiate each, substitute into u′v+uv′, distribute and collect/factor only where the source does. Blanks expect a single prescribed summand, not an interchangeable complete derivative. The two base-log layouts retain the supplied complement term and generic formal-rule row. Polynomial–exponential blanks omit the redundant final factored row; their radios keep it. The exponential-sine and exponential-tangent blanks have three rows, while base-log blanks have four. The cosine/common-log radio has three rows.

## Stage 3: components and complete bank operations

The per-source tables account for every displayed option. In generator code bank tuples contain complete parameterized rendered expressions, exact SymPy expressions and recipe labels. Wrong-operation labels are hypotheses about the displayed expression transformations, not recovered author intent and never learner feedback. The full five-member banks remain separate:

- log_log_observed: omit the logarithm-base derivative divisor, omit one logarithmic factor, omit the coefficient in only the second term, correct two-term product derivative, omit the other logarithmic factor. For c=1, the missing-coefficient option collides with correct; reject the whole explicit instance or resample the whole random instance.
- power_log_observed: omit ln b from log derivative, multiply derivatives, negate derivative structure with the wrong power, add derivatives, correct factored derivative.
- linear_base_observed: remove both x and first term, remove x from second term, correct, retain only first term, retain only second term.
- power_exp_observed: correct factorization; fail to reduce power and multiply by n; omit exponential in second term; use n−1 instead of n; omit exponential in first term.
- cos_log_observed: omit x denominator; omit ln b divisor; reverse sine sign; correct; omit log and base divisor together.

q-1933 and q-47966 have no source correct reference, solution, or difficulty. Differentiating 5 log_3 x ln x independently gives 10 ln x/(x ln 3), uniquely matching the fourth displayed option. Differentiating x^−3 log_2 x gives x^−4(−3 log_2 x+1/ln 2), uniquely matching the fifth displayed option. These two inferred references do not count as matched source designations. Raw capture is retained unchanged. Authored easy placement is based on atomic factors and a single product rule, comparable to the full easy exponential/cosine-log radios. Original MA widget excerpts were read from /home/jake/Developer/MA/DATA/Lessons/1109/Source/1109.json and preserved in widget-excerpts.json with hash. They confirm the two five-option radio layouts, lack any correct designation/explanation, and order their choices differently (derived correct letters a for1933 and d for47966). No mathematical or presentation repair is required for the existing 11 worked solutions; all 11 replay byte-exact. JSON serialization doubles backslashes visually, but decoded source command bytes use ordinary single backslashes. Unicode application characters and original math notation remain intact in observed replay, and formatting checks still apply.

## Stage 4: reusable masks and sampling bounds

The build function constructs complete component masks U,V,D,DV and complete row masks, with shared prose and source-specific punctuation/prime notation. It contains no source-record import, answer lookup or literal-source payload return branch. At original parameters every full bank is byte-exact; at changed parameters the same mathematical operations compute all answers and each intermediate row. Source-bank selection occurs as one complete profile before sampling; collisions reject the entire instance. Seeds shuffle owned radio options after correct identity is recorded.

Easy bases are integers 2..10. Polynomial–exponential blank coefficients are 1..6, powers 2..4, exponential scales 1..3. The observed polynomial–exponential radio retains scale 1 and powers 2..4 and common scalar coefficient 1..6, preserving its entire five-operation bank. Negative-power/log radio powers are −4..−1. Exponential-log negative layout uses −x, and other base-log layouts use kx for k=1..3. These are authored bounded sampling policies supported by observed structures, not claims about original randomization. Explicit calls obey identical guards. Invalid base, zero coefficient, collapsed degree and complete-bank ambiguity are failures, never silently substituted.

The authored moderate/hard solution has the common formal rule, actual factor operator row, component-derivative row and distribution/collection row. Coefficient signs use grouped sums. No eager CAS rewrite to hyperbolic functions occurs; natural-log notation uses ln. Mathematical-task fingerprints depend only on the canonical displayed product, excluding answer banks, profile names, and layout; content identity includes actual prompt, fixed worked solution, field type and complete displayed bank. Shuffling cannot change identity. Source profiles are not disguised as authored default banks.

Native alternate submissions normalize invisible Unicode application marks in source component-row notation; this affects test-entry spelling only, not replay learner content. The native parser reports unsupported notation for sec² followed by the invisible application mark, while the canonical source blank has no such mark and grades correctly. A mathematically equivalent ln4=2ln2 denominator rewrite yields native unresolved domain differences; a dedicated fixture records that real restriction, with source canonicals and supported unreduced component forms tested independently. Authored logarithmic distribution masks retain the displayed logarithm base and each original x·ln(base) denominator, while independently parsing every distributed term proves equality. Canceling x in those quotients is mathematically valid on the prompt’s logarithmic domain x>0, but the native grader retains a composite nonzero denominator guard and reports unresolved domain differences after the cancellation. A separate independently verified fixture records this native limitation. The distribution row still explicitly distributes every polynomial component and avoids introducing a new quotient differentiation task. All 75 supported accepted entries and 90 incorrect rejections pass; three dedicated unsupported/equivalent entries are reported explicitly unresolved. No engine changes were made.

No plots are present; plot extraction and generator stages 5/7 are not applicable beyond this checked none rating. This work stops before database preparation or registration.
'''
(ROOT/'template-extraction.md').write_text(text)
(ROOT/'README.md').write_text('''# Product-rule generator

Local generator and evidence for KP 17592186096618, math basis 1356. No database writes.

Run `.venv/bin/python generate/scratch/17592186096618/validate.py` from the repository root. Additional explicit boundary/identity checks: `.venv/bin/python generate/scratch/17592186096618/boundary.py`. Preview: `.venv/bin/python generate/scratch/17592186096618.py --difficulty all --seed 4 --count 2 --format json`.

The API exposes generate_easy, generate_moderate, generate_hard, and generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None). Explicit parameters reject invalid/ambiguous inputs. source-cases.json lists all 13 replay calls. Twelve observed templates and five complete source radio profiles are preserved; moderate/hard add two authored templates each. Eight observed blanks require fragments; authored blanks require the full derivative.

validation.json separates exact prompts/banks/solutions, observed correct references, two mathematically inferred missing references, actual printed-math readback, changed-parameter tests, and real learning::grade_field checks. readback.py parses displayed products, u/v definitions, formal derivatives, component derivatives, distributed sums, choices, and reinserted blank fragments without reading generation parameters. Raw source/topic/lesson wrappers retain capture provenance. Review examples label source replays and authored/generated variants explicitly. No plots or image models are used.
''')
review=json.loads((ROOT/'review.json').read_text());md='# Original and generated review\n\n'
for q in questions:
 md+='## Raw original '+q[':question/math-academy-id']+'\n\n'+q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$' for a in q[':question/answer-fields'][0][':answer-field/choices'])+'\n\n'+q.get(':question/worked-solution','Original solution and correct reference absent; see explicit inference in template-extraction.md.')+'\n\n'
for item in review:md+='## '+item['label']+'\n\n'+('Authored '+item['record']['question'][':question/difficulty'].rsplit('/',1)[-1]+' level extension.\n\n' if item['record']['generation']['authored'] else '')+g.markdown(item['record'])+'\n\n'
(ROOT/'review.md').write_text(md)
