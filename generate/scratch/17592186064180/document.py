"""Produce scoped source, extraction and bounded-capability evidence."""
import importlib.util,json,re
from pathlib import Path
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('v',HERE/'validate.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
s=json.loads((HERE/'source.json').read_text());qs=s['record'][':knowledge-point/questions'];g=v.g
analyses=[];sources=[]
for q in qs+[s['record'][':knowledge-point/canonical-example']]:
    mid=q[':question/math-academy-id'];fields=q.get(':question/answer-fields',[]);t=g.TEMPLATES.get(mid)
    e=g.integrand(q[':question/problem']);var=next(iter(e.free_symbols));primitive=v.primitive(e,var)
    banks=[]
    for f in fields:
        for a in f[':answer-field/choices']:
            pattern=t['choices'][[x[':answer/value'] for x in f[':answer-field/choices']].index(a[':answer/value'])] if t else a[':answer/value']
            banks.append({'source_field':str(f[':answer-field/id']),'source_answer_id':str(a[':answer/id']),'original_value':a[':answer/value'],'parameterized_expression_recipe':pattern,'profile':mid if t else 'incomplete-unrated-evidence-only','parameters':t['parameters'] if t else {},'original_value_reproduced':g.render(pattern,t['parameters'])==a[':answer/value'] if t else None,'interpretation':'Observed complete expression; no inferred learner error explanation added.'})
    analyses.append({'source_id':mid,'source_db_id':q[':db/id'],'difficulty':q.get(':question/difficulty',{}).get(':db/ident','unrated'),'complete_supported':bool(t),'exact_integrand':str(e),'number_features':'Negative rational coefficient' if mid=='q-113935' else 'Integer coefficients with observed signs; unit trig argument','variable':str(var),'independently_verified_primitive':str(primitive)+' + C','domain':'Connected real intervals excluding poles of every function appearing in integrand and bank. C arbitrary.','field_types':[f[':answer-field/type'][':db/ident'] for f in fields],'field_keys':[f[':answer-field/key'] for f in fields],'missing_evidence':[name for name in (':question/difficulty',':question/worked-solution',':question/answer-fields') if name not in q]+([':answer-field/correct'] if any(':answer-field/correct' not in f for f in fields) else []),'plot_rating':'none','choices':banks,'source_record':q})
    sources.append('## '+mid+'\n\n'+q[':question/problem']+'\n\n'+('\n'.join('- $'+a['original_value']+'$' for a in banks) or 'No answer field is supplied. This is not evidence of a blank response shape.')+'\n\n'+q.get(':question/worked-solution','No worked solution supplied.'))
assert not any(re.search(r'!\[|images/|<img',q[':question/problem']+q.get(':question/worked-solution','')) for q in qs)
(HERE/'source-analysis.json').write_text(json.dumps(analyses,indent=2)+'\n');(HERE/'source-questions.md').write_text('\n\n'.join(sources)+'\n')
classification=f'''# Classification

Captured math basis {s['basis']}, lineage {s['lineage']}. source.json and reference/initial retain the scoped EDB read and native inventory. This KP has 10 practice sources and canonical e-384. No generator or supplied .generated artifact existed at capture. The initial native counts are easy 2, moderate 3. Fresh counts are rechecked under the application lock before any submission.

| Band | Complete response shape | Supported templates | Bank profiles | Plot rating | Source IDs |
|---|---|---:|---:|---|---|
| Easy | One radio field, key selection, five math choices | 2 | 2 | none | q-113936, q-113937 |
| Moderate | One radio field, key selection, five math choices | 3 | 3 | none | q-113944, q-2164, q-49122 |
| Hard | No source evidence of field, template or solution | 0 | 0 | none | none |

The easy templates differ in sign, variable notation and the worked-solution sequence; they remain separate. The moderate templates are sec squared minus cosecant-cotangent, cosecant-cotangent plus sec squared, and a factored secant product expanded before linearity. q-2035 and q-49118 retain banks but lack difficulty, correct designation and solution. q-113935 is easy with a negative rational coefficient; q-2162 and q-2165 are moderate with distinct sine and secant-tangent linearity sequences, but all three lack fields. Missing fields do not establish a blank. These five incomplete sources are preserved and excluded from validated availability and sampling. They remain assigned in source-analysis.json; no bank choice is silently discarded.

Hard is a bounded unsupported capability of this generator: no verified hard template is available; combining arbitrary extra terms or changing trig arguments would require independently justified difficulty and response evidence. Absence alone does not prove mathematical impossibility. Reopen classification when new verified hard source evidence or an independently validated extension becomes available. Nominal hard shortage 5 remains explicit and is not filled.
'''
(HERE/'classification.md').write_text(classification)
extraction='''# Template extraction

Each complete source uses the integral rule sec²(v) -> tan(v), with linearity where needed. The required response is an antiderivative plus an arbitrary constant. Variable roles, numeric features, exact original layout, complete field/choice mappings and source-specific components are retained in source-analysis.json. templates.json contains the executable Markdown, fixed worked-solution sequence and full bank recipes. review.md compares source questions to exact replay and variants.

| Template / profile | Integrand and parameters | Complete choice recipes, in retained source order | Canonical index |
|---|---|---|---:|
| q-113936 | a sec²(theta), observed a=2 | a sec(theta)+C; -a csc(theta)+C; -csc²(theta)+C; tan²(theta)+C; a tan(theta)+C | 4 |
| q-113937 | -a sec²(z), observed a=4 | -a sec(z)+C; a tan(z)+C; a sec²(z)+C; a cot(z)+C; -a tan(z)+C | 4 |
| q-113944 | sec²(x)-b csc(x)cot(x), observed b=2 | tan(x)+b csc(x)+C; cot(x)-b csc²(x)+C; tan(x)-b cot(x)+C; cot(x)+b csc(x)+C; -tan(x)+b csc²(x)+C | 0 |
| q-2164 | b csc(x)cot(x)+sec²(x), observed b=4 | b csc(x)+tan(x)+C; -b csc(x)-tan(x)+C; b csc(x)+sec(x)+C; -b cot(x)+tan(x)+C; -b csc(x)+tan(x)+C | 4 |
| q-49122 | sec(x)(a sec(x)+b tan(x)), observed a=7,b=4 | -a tan(x)+b csc(x)+C; -a tan(x)-b csc(x)+C; a tan(x)+b sec(x)+C; a cot(x)+b sec(x)+C; a cot(x)-b sec(x)+C | 2 |

All bank expressions are observed profiles, rather than inferred descriptions of mistakes. Every option reproduces its exact original value at the source parameters; full mathematical values, designated correct answers and counts are checked independently. No pooled bank or mixed-profile bank is authored. The solutions retain every source sentence and equality line, including nested aligned markup. There are no repairs to supported sources.

Sampling is a bounded extension of observed coefficient values: positive integer magnitudes 1..9, restricted to 2..9 in the easy templates to preserve nonunit layout. Source signs, unit trig arguments and fixed variables are retained. In the two unscaled moderate templates the sec² coefficient stays 1. Sampling preserves observed values and all template conditions. It does not claim coverage of fractional or arbitrary real coefficients. Common variable renaming, seed changes, bank changes and choice order do not count as new tasks. The exact expanded integrand defines mathematical novelty, independently of bank/identity.

Every integral is local to real connected intervals avoiding all trig poles. Correct options are independently differentiated; all distractors must differentiate differently from the prompt and be pairwise inequivalent on the common domain. The complete finite parameter domain is checked, including a=b and a!=b in the factored template. No additional feedback is added to learner content.
'''
(HERE/'template-extraction.md').write_text(extraction)
(HERE/'plot-extraction.md').write_text('# Plot extraction\n\nAll ten practice prompts, available solutions and banks contain only mathematical text. No graphs, diagrams, image assets or variable plot requirements occur. Plot rating is none for every template; stage 7 has no assets to render or publish.\n')
caps={'knowledgePoint':g.KP_ID,'source_basis':s['basis'],'lineage':s['lineage'],'supported_levels':['easy','moderate'],'unsupported_levels':['hard'],'finite_distinct_task_domain':{'easy':16,'moderate':99},'exceptions':[{'level':'hard','kind':'unsupported','nominal_shortage':5,'reason':'No verified hard source template, field or solution. Bounded generator capability; not proof of mathematical impossibility. Reopen with verified hard evidence or an independently validated extension.'},{'profiles':['q-2035','q-49118','q-113935','q-2162','q-2165'],'kind':'incomplete-source','reason':'Missing rating, correct designation, solution and/or fields. Original records and every choice retained; excluded from gradable inventory and sampling.'}],'unsupported_levels_filled':False,'sampling_bounds':'Easy signed sec-squared coefficients 2..9; moderate b 1..9 in two fixed-unit-sec-squared templates, a,b 1..9 in factored secant template. 16 easy and 99 moderate integrands; seen/source tasks further reduce unused capability.'}
(HERE/'capabilities.json').write_text(json.dumps(caps,indent=2)+'\n')
(HERE/'README.md').write_text('''# Integrating Secant Squared generator

17592186064180.py is a pure seeded generator using the five exact, complete source profiles. Run validate.py for full bank replay, exhaustive exact mathematics, all solution lines, boundary/negative controls and application grading. The local check-engine binary is linked to the current application library; engine-build.json records exact hashes and the build command. Fidelity and correctness are separate checks.

replenish.py rechecks the current native inventory and a conservative distinct, mathematically validated pool. It holds api.lock through basis capture, source-stability checks, native-spec preview, guarded durable submission and exact-basis readback. It registers the existing or deterministic generator UUID with question-generator/id, question-generator/script and the KP reference. Identity lookups, complete requests, previews, receipts and verification are retained in reference/replenishment. Only additive generated content and this KP generator reference are permitted; source questions, canonical example and learner history are preserved. Invalid or duplicate supplied artifacts are not counted as new content.

Read classification.md, template-extraction.md, source-analysis.json and capabilities.json for evidence and bounds. Easy and moderate are supported. Hard remains an explicit unsupported capability, nominal shortage 5, pending new verified evidence. No source field is invented from missing evidence.
''')
