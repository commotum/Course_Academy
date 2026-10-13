import importlib.util,json
from pathlib import Path
P=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('v',P/'validate.py');V=importlib.util.module_from_spec(spec);spec.loader.exec_module(V);G=V.G
RECIPES={
'q-100642':['(n+1)/n','divergent','n','2*n','(n-1)/n'],
'q-5964':['divergent','-K/4','-K/15','-K','-K/5'],
'q-100643':['divergent','-2/n','n/2','2*sqrt(n+2)/n','-2*sqrt(n+2)'],
'q-80342':['-sqrt(n)','divergent','-sqrt(n)/2','-2*sqrt(n)','-4*sqrt(n)'],
'q-80347':['1/3','2','-2','-2/3','divergent'],
'q-6034':['1/log(n)','n*log(n)','log(n)','divergent','exp(n)'],
'q-20700':['divergent','exp(n)','n*log(n)','log(n)','1/log(n)'],
'q-20698':['divergent','log(n)','1/n','1/(n*log(n))','n*log(n)']}
templates=[];rows=[]
for t in G.TEMPLATES:
 mid=t['source_id'];q=G.BY_ID[mid];components=[]
 for expr,lo,hi,x in V.printed(q[':question/problem']):
  components.append({'variable':str(x),'integrand':str(expr),'lower':str(lo),'upper':str(hi),'exact_result':str(V.limit_result((expr,lo,hi,x))),'features':'Real half-line, no finite pole crossing; radical arguments positive on radical tails; logarithmic endpoints exceed 1 when ln(ln(x)) occurs.'})
 banks=[]
 for f in q[':question/answer-fields']:
  choices=[]
  for i,a in enumerate(f[':answer-field/choices']):
   recipe=RECIPES[mid][i] if mid in RECIPES else a[':answer/value']
   if mid in RECIPES and recipe!='divergent':
    n=t['observed_value'];K=6*V.s.Rational(n,n-1)
    actual=V.s.sympify(recipe,locals={'n':n,'K':K})
    assert V.s.simplify(actual-V.value(a[':answer/value']))==0,(mid,recipe,a[':answer/value'])
   choices.append({'source_answer_id':a[':answer/id'],'source_field_id':f[':answer-field/id'],'source_value':a[':answer/value'],'type':a[':answer/type'][':db/ident'],'correct':a[':answer/id']==f[':answer-field/correct'][':answer/id'],'recipe':recipe,'complete_value_reproduced_at_source':True,'interpretation':'Observed exact expression pattern. Parameter extension is explicit; misconception mechanism is not claimed.'})
  banks.append({'field_key':f[':answer-field/key'],'field_type':f[':answer-field/type'][':db/ident'],'profile':mid+':'+f[':answer-field/key'],'source_choice_count':len(choices),'choices':choices})
 templates.append({**t,'components':components,'problem_source':q[':question/problem'],'worked_solution_source':q[':question/worked-solution'],'banks':banks,'fixed':'Variable spelling, integrand structure except named parameter, all other component integrals, field layout and solution sequence.','conditional':'At source parameter render exact notation; new values render exact SymPy fractions/radicals. q-101734 uses recorded truncation-bound correction.','variable':'Only '+t['parameter'],'extension_policy':'Recipe expressions explicitly extend a sparse observed bank; preserve complete profile rather than pooling banks. For q-5964 K=6*n/(n-1). q-80347 finite distractors are fixed observed constants.','generalized_description':'Identify divergence by a primitive and an infinite endpoint limit; moderate requires three independent judgments.'})
 rows.append('| '+t['level']+' | '+mid+' | '+', '.join(f['field_type'].split('/')[-1]+':'+f['field_key'] for f in banks)+' | '+t['parameter']+'='+str(t['observed_value'])+' | none |')
V.write('templates.json',templates)
cap={'supported_levels':list(G.SUPPORTED_LEVELS),'unsupported_levels':['hard'],'reason':'No hard source examples or validated hard extension in this bounded package. Unobserved is not a proof of impossibility; new evidence reopens classification.','excluded_template':'q-6294 has two radio fields sharing selection, and one has no canonical answer. Full authored response layout cannot be graded. Source remains unchanged.','finite_distinct_tasks':{k:sum(len(t['sampling_values']) for t in G.TEMPLATES if t['level']==k) for k in G.SUPPORTED_LEVELS},'unsupported_levels_filled':False,'sampling':'All enumerated bounds checked; exhaustion must leave shortages explicit. No seed/identity/choice-order variants counted.'}
V.write('capabilities.json',cap)
(P/'classification.md').write_text('# Classification\n\nCaptured all 14 practice questions at basis '+str(json.loads((P/'source.json').read_text())['basis'])+'. Canonical example is retained as evidence and excluded from practice counts. Easy has 9 layouts, 8 supported radio layouts; moderate has 5 layouts, each with three checkbox fields I/II/III. Hard is unobserved. All plots: none; all displayed mathematics is LaTeX.\n\n| Difficulty | Source/template | Fields | Observed parameter | Plot rating |\n|---|---|---|---|---|\n'+'\n'.join(rows)+'\n\nq-6294 is excluded: duplicate selection keys and missing correct answer in one field. q-101734 has a finite-truncation typo: the second displayed limit retains upper infinity inside the truncated integral; generated copies use upper a. Source preserved.\n')
(P/'template-extraction.md').write_text('# Template extraction\n\n`templates.json` retains every source prompt, solution, field, owned choice and exact value with its profile. There is one complete profile per layout and checkbox field. Mathematical components are independently parsed. `render` in the generator implements the numeric slots as simultaneous replacements and records conditions per layout. Sparse source evidence limits inference: numeric distractor extensions are expression patterns, not asserted diagnoses of errors.\n\nSource q-6294 is captured but excluded; its duplicate fields prevent supported full replay. All 13 supported banks must replay without missing or extra options. q-101734 alone receives the documented finite-bound correction, justified by the definition of truncating an improper integral. No plot extraction/rendering is required.\n\nEasy variants change odd root degree (3–21), positive slope, radicand shift, or a logarithmic lower cutoff. Moderate variants change one endpoint with all finite evaluations updated. Exponents and other integrals stay fixed in moderate. Every distinct task is normalized by integrands and endpoints; variable names and field/answer order do not count.\n')
(P/'README.md').write_text('# Identifying Divergent Improper Integrals\n\nRun `.venv/bin/python generate/scratch/17592186083201.py --difficulty easy --count 5 --seed 83201` for reproducible JSON. `--format markdown` gives a worked preview. Moderate uses three field-owned checkbox banks. Hard raises an unsupported-level error.\n\nRun `.venv/bin/python generate/scratch/17592186083201/build_evidence.py` then `.venv/bin/python generate/scratch/17592186083201/validate.py`. `replenish.py` uses the existing native EDB integration and application lock, saves exact requests, previews with native predicates, commits with a basis guard, and verifies additive scoped changes at db_after.\n')
print('Extracted',len(templates),'supported source layouts')
