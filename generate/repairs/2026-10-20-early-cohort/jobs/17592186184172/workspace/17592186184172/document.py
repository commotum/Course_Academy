"""Record source classification and the deliberately bounded variable domains."""
import json,re
from pathlib import Path
import validate as v
g=v.g;D=Path(__file__).resolve().parent
GROUPS={
'M1-pivot-radio':['q-34934','q-142538'],
'M2-pivot-checkbox':['q-79420','q-79367'],
'M3-nonpivot-checkbox':['q-142544','q-79417'],
'M4-nonpivot-radio':['q-79411'],
'M5-parametric-nullspace-checkbox':['q-143533'],
'H1-span-count-radio':['q-34930'],
'H2-span-count-checkbox':['q-139986'],
'H3-parametric-three-free-checkbox':['q-79423'],
'H4-span-rank-invertibility-checkbox':['q-142542'],
'H5-parametric-line-radio':['q-35435'],
'H6-span-line-pivot-radio':['q-79410']}
rows=[];extraction=[]
for name,keys in GROUPS.items():
 rows.append({'template':name,'difficulty':g.level_of(keys[0]),'field_types':[g.clean(g.Q[keys[0]])[':question/answer-fields'][i][':answer-field/type'] for i in range(len(g.Q[keys[0]][':question/answer-fields']))],'plot_rating':'none','sources':keys,'profiles':keys})
 for key in keys:
  q=g.clean(g.Q[key]);t=g.task_data(q);truths=[v.truth(s,t) for s in t['statements']];fs=[]
  for f in q[':question/answer-fields']:
   choices=[]
   for a in f[':answer-field/choices']:
    if f[':answer-field/type'].endswith('/radio'):
     subset=[i for i in ['I','II','III'] if re.search(r'\b'+i+r'\b',a[':answer/value'])]
     disagrees=[i for i,b in zip(['I','II','III'],truths) if (i in subset)!=b]
     recipe={'selected_statement_subset':subset,'incorrect_assumptions':disagrees}
    else:recipe={'boolean':a[':answer/value']}
    choices.append({'source_answer_id':a[':answer/id'],'value':a[':answer/value'],'recipe':recipe,'correct':a[':answer/id']==f[':answer-field/correct'][1]})
   fs.append({'key':f[':answer-field/key'],'type':f[':answer-field/type'],'choices':choices})
  extraction.append({'source':key,'template':name,'profile':key,'observed':t,'original_parameters':g.default_parameters(key),'fixed_statement_roles':t['statements'],'prompt':q[':question/problem'],'worked_solution':q[':question/worked-solution'],'fields':fs,'parameter_policy':'Positive invertible diagonal row factors, each 1..3; all vectors, including solution bases, change together. Subspaces deduplicated by exact RREF.' if g.is_vector(key) else 'Uniform k=1..3 multiplies every dimensional/count literal in prompt and solution; rank+nullity=n and truth values preserved. Zero stays zero.'})
v.save(D/'classification.json',{'basis':g.RAW['basis'],'knowledge_point':g.KP_ID,'practice_sources':len(g.Q),'templates':rows,'unsupported_levels':['easy'],'canonical_example':'e-5426 is incomplete/unrated and excluded from practice and generator templates; its image mathematics is not needed for source replay.','unresolved':[]})
v.save(D/'template-extraction.json',extraction)
md='# Classification and template extraction\n\nSource basis: '+str(g.RAW['basis'])+'. All 14 source practice questions were read together, including fields, choices, keys, solutions and difficulty. There is no registered generator. No practice source contains an image or requires a new plot; stages 5 and 7 are inapplicable. The incomplete canonical example is excluded.\n\n'
md+='| Template | Difficulty | Fields | Sources / bank profiles | Plots |\n|---|---|---|---|---|\n'
for r in rows:md+='| '+r['template']+' | '+r['difficulty']+' | '+', '.join(x.split('/')[-1] for x in r['field_types'])+' | '+', '.join(r['sources'])+' | none |\n'
md+='\nCount templates give a square matrix order and pivot or non-pivot count. Null-space templates supply independent spanning vectors or a linear free-parameter description. Each asks for the truth of three fixed source claims. Preserve the supplied-object role, claim order, field layout, complete radio subset bank or per-statement Boolean bank, and the solution stages: square-matrix invertibility equivalences; rank-nullity; statement I, II and III in turn; final truth subset.\n\n'
md+='Two conservative generalizations are supported. For count templates, multiply all positive dimensional and count literals by the same integer k in {1,2,3}, retaining zero and all theorem relations. This extends source dimensions to at most 21; no large matrix computation is added. For vector templates apply one invertible diagonal coordinate map with integer row factors in {1,2,3} to every supplied and worked-solution vector. This preserves support, independence, free-parameter count, rank-nullity and source truth patterns while permitting genuinely different subspaces. General coordinate permutations, matrix dimensions for vector sources, arbitrary statement changes, new distractor subsets, and new methods are outside this version.\n\n'
md+='These are deliberately narrow policies, not claims that broader variations are impossible. At original parameters prompt and solution must replay byte for byte and every full bank must match. The extraction JSON records each exact source component and every option-to-subset/Boolean recipe. Radio distractors retain exactly the authored subset selections; checkbox fields retain both authored Boolean states. No pooled or inferred bank recipes are introduced.\n\n'
md+='The q-79423 domain is finite at one semantic task: diagonal changes leave its coordinate hyperplane unchanged. Count it once, regardless of coefficient text, seed, identity, or bank order. Every other null-space candidate is compared using exact RREF of the transposed basis; proportional vectors or alternative bases of the same space cannot establish novelty. Count tasks are compared by order, supplied count and claims. Field type, choice order, seed and difficulty label are omitted from novelty.\n\n'
md+='Easy remains unsupported: no observed easy backbone or classification evidence. Its nominal shortage remains five; this version cannot call that band filled. New source evidence reopens classification.\n\n'
md+='The source text includes legacy grammatical and set-brace formatting defects (for example the singular “column” and missing escaped set braces). This version preserves source prose and mathematical meaning rather than changing previously captured content. All vectors are readable as mathematical arrays; all statement keys are checked independently using exact rank calculations. No source mathematical key error was found.\n'
(D/'template-extraction.md').write_text(md)
(D/'review.md').write_text('# Source/variant review\n\nThe side-by-side review.json pairs each source with a changed mathematical-data instance where the bounded domain permits one. All 14 source prompts and solutions replay exactly. The rank-nullity substitutions, invertibility decisions, claim truth values, field layouts and complete authored choice banks agree. Uniform count dilation changes the supplied order and column counts together. Diagonal coordinate maps update both the free-parameter vector and every explicit spanning vector in the solution. q-79423 has no genuinely new subspace in this domain and is excluded from variant novelty.\n\nNo field shape was converted. Checkbox fields are graded through their authored true/false choice identities, which is the application grading contract. The native report tests both states for all checkbox fields and every option for radio fields.\n')
print('Recorded',len(rows),'templates and',len(extraction),'source profiles')
