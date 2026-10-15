import json,sys
from pathlib import Path
import validate as v
g=v.g;H=g.HERE
save=v.save
classification={'basis':g.CAP['basis'],'lineage':g.CAP['lineage'],'knowledge_point':g.KP,'title':g.TITLE,'supported_levels':['easy'],'unsupported_levels':['moderate','hard'],'levels':{'easy':{'field_combinations':['radio','blank+blank'],'template_count':4},'unrated':{'field_combinations':['radio'],'template_count':1,'source':'q-13566','sampling':'excluded'}},'templates':[],'source_exclusions':[{'source':'q-13564','issue':'Two selection fields, one without correct ref. Preserve both; exclude source record from validated inventory.'},{'source':'q-13566','issue':'Unrated and absent key/solution. Preserve and exclude from inventory and normal generation.'},{'source':'q-126512','issue':'Correct source mathematics and grading; irregular distractors unresolved. Source can count when available; its generator bank is original-parameter replay only.'}],'plots':{'rating':'none','reason':'All practice matrices are standalone LaTeX mathematical notation. Canonical PNGs contain matrix notation only; no new diagrams or plots required.'}}
extraction=[]
for t,ids in g.GROUPS.items():
 classification['templates'].append({'template':t,'sources':ids,'difficulty':'unrated' if t=='what-radio' else 'easy','field_types':['blank','blank'] if t.endswith('blank') else ['radio'],'plot_rating':'none','normal_sampling_supported':t in g.ELIGIBLE})
 for mid in ids:
  q=g.SOURCES[mid];p=g.parameters(q);computed=g.dot(p);mapped=[]
  for f in q[':question/answer-fields']:
   choices=[]
   for a in f[':answer-field/choices']:
    text=a[':answer/value'];norm=text.replace('\\\\begin','\\begin').replace('\\\\end','\\end')
    value=tuple(v.val(row[0]) for row in v.scan(norm)[0]) if t.endswith('radio') else (v.val(norm),)
    recipe=[recipe for recipe,z in g.bank(mid,p) if z==value] if t.endswith('radio') else ['row-'+f[':answer-field/key'][-1]+'-dot-product']
    assert len(recipe)==1
    choices.append({'answer_id':a[':answer/id'],'exact_source_value':text,'mathematical_value':value,'recipe':recipe[0],'source_field':f[':db/id'],'profile':mid})
   mapped.append({'source_field':f[':db/id'],'key':f[':answer-field/key'],'type':f[':answer-field/type'][':db/ident'],'correct':f.get(':answer-field/correct'),'choices':choices})
  extraction.append({'source_id':mid,'question_id':q[':db/id'],'template':t,'profile':mid,'parameters':p,'number_features':{'signed_integers':True,'zero_matrix_entries':0 in [p[k] for k in ('a','b','c','d')],'equal_vector_entries':p['u']==p['v']},'prompt':q[':question/problem'],'solution':q.get(':question/worked-solution'),'product':computed,'fields':mapped,'sampling_supported':mid not in ('q-126512','q-13566')})
save(H/'classification.json',classification);save(H/'template-extraction.json',extraction)
recipes='''With A=[[a,b],[c,d]], x=[u,v], r=a*u+b*v, s=c*u+d*v:
- q-13564: (r,s), (-r,-s), (r,-s), (-r,s), (v,u).
- q-126511: (r,s), (a+b,c+d), (-a-b,-c-d), (s,r), (a,c).
- q-13555: (r,s), (r,r), (r,-s), (-r,-s), (-r,s).
- q-13565: (r,s), (-s,-r), (r,-s), (-r,-s), (-s,r).
- q-13629: (r,s), (r+1,s), (r,s-1), (r,s+1), (r-1,s-1).
- q-13560: (r,s), (r+1,s), (s,r), (r,r), (s,s).
- q-126512: original bank only: (1,-2),(10,-12),(-8,6),(-4,4),(-44,14). Underlying errors unresolved; no parameterized normal sampling.
- q-13566: original bank only: (21,12),(21,-12),(-21,-12),(12,21),(19,12). Missing source key and solution; replay evidence only.
- Blanks: field-1=r, field-2=s. Canonical answers remain field-owned.
'''
(H/'template-extraction.md').write_text('''# Multiplying a 2x2 matrix by a column vector

Source capture: math basis '''+str(g.CAP['basis'])+''', lineage '''+g.CAP['lineage']+'''. Exact source fields, prompts, solutions and every choice mapping are in template-extraction.json.

The fixed backbone is two row dot products: multiply row one by the supplied column vector, retain its first result while evaluating row two, then display the full two-component column vector. All questions request the entire product. Row and column roles and vector dimension remain fixed because changing them changes the assessed operation or workload. There is no queried-cell slot.

Keep four easy templates separate: named matrix and vector with radio answer, inline product with radio answer, named product with two scalar blanks in a table, and inline product with two scalar blanks in a table. The unrated “What is” template remains evidence-only. Both blank keys denote output rows, independent of source field storage order. Labels vary together throughout named prompts and solutions but are excluded from distinctness.

Slots a,b,c,d are integers in [-11,11]; u,v are signed nonzero integers in [-9,9]. These bounds conservatively extend observed integer inputs, including zero matrix entries, equal vector entries and negative inputs. Sampling does not introduce fractions, extra dimensions, extra operations or new reasoning stages. Matrix labels A,Z,X,H and vector labels x,y,n,a are observed labels sampled independently. Every original parameter is replayed.

Each complete radio bank is selected by source profile before parameter sampling. Reject whole colliding banks. The original author's intended error is unknown: the formulas below are observed-value-preserving generalizations, not claims about cognitive errors. The unresolved irregular bank is withheld rather than inventing its extension.

'''+recipes+'''
All generated math is delimiter-free inside answer values. Source radio matrices have double-escaped begin/end commands; generated values use canonical single LaTeX commands. Bank replay compares complete integer vectors after this documented notation correction. Other source defects remain unchanged: q-13564 has duplicate selection fields and a missing key; q-13566 has no difficulty, key or solution.

The parameterized worked solution retains source wording, first-row and second-row accumulated matrix displays, and the final named or inline conclusion. Parenthesize negative factors consistently; the original q-275589 sometimes omits those optional parentheses. This is a notation normalization, not a new stage. Every displayed row expression and resulting vector is independently read back and checked.

Practice matrices are LaTeX, not plots. Canonical example PNGs are matrix notation. Stages 5 and 7 require no generated assets. The generator uses exact SymPy matrices. Slot coverage includes all sampled integer values, labels, signs, zero matrix entries and equal/unequal vector components. Holding coefficients fixed while renaming labels verifies references; mathematical row roles remain fixed.

A content fingerprint ignores seed, identities, option order, labels, response format and source bank. It canonicalizes a simultaneous column/vector-coordinate permutation, preserving output row roles. Existing operands, including the canonical example [1,3;7,-2]*[2,5], cannot become new content by rendering or seeding again.

Moderate and hard have no source-backed templates. Larger numbers alone do not establish a new difficulty, and extra dimensions or operations would leave this KP backbone. Each nominal five-item band remains explicitly unfilled pending new source evidence; this is a bounded package capability exception, not proof that this mathematics can never have harder exercises.
''')
save(H/'capabilities.json',{'knowledge_point':g.KP,'supported_levels':['easy'],'unsupported_levels':['moderate','hard'],'target_per_supported_band':5,'exceptions':[{'kind':'unsupported-band','level':level,'unfilled_nominal_target':5,'evidence':'All ten rated source questions are easy. The eleventh is unrated/incomplete. No moderate/hard same-backbone evidence; no reclassification by coefficient magnitude.','reopens_on':'new source evidence'} for level in ('moderate','hard')],'excluded_sampling_profiles':['q-126512','q-13566'],'finite_variant_limit':None,'plots':'none'})
# Concrete source/variant review with different arithmetic, signs, zeros and labels.
reviews=[]
for t,profile in [('named-radio','q-126511'),('inline-radio','q-13560'),('named-blank','q-275589'),('inline-blank','q-318640')]:
 for seed in (3,27):
  r=g.generate('easy',seed,t,profile=profile);v.check(r);reviews.append({'source':g.SOURCES[profile],'variant':r,'mathematics_passed':True,'solution_backbone':'row one, row two, final vector','fidelity':'same prompt/field contract and concrete ordered source solution stages'})
save(H/'review.json',reviews)
(H/'review.md').write_text('\n\n'.join('## '+z['variant']['generation']['template']+' / seed '+str(z['variant']['generation']['seed'])+'\n\nSource '+z['variant']['generation']['bank_profile']+':\n\n'+z['source'][':question/problem']+'\n\nVariant:\n\n'+z['variant']['question'][':question/problem']+'\n\n'+z['variant']['question'][':question/worked-solution'] for z in reviews))
(H/'README.md').write_text('''# Matrix-column generator

Run `.venv/bin/python generate/scratch/17592186100866/validate.py` for exact rendered-math, source-bank and native learner-grading validation. Run `.venv/bin/python generate/scratch/17592186100866.py --difficulty easy --seed 3 --count 2` for JSON previews. Unsupported levels raise an explicit error.

The scoped `replenish.py` checks the native learner pool and independently validates available source records, excludes incomplete records, and adds only a supported shortage. It registers the stable generator UUID and repository-relative path, serializes the entire durable workflow with application api.lock and retains exact requests, previews, receipts, attribution and exact-basis readback in reference/replenishment. It never repairs source content or modifies learner history.
''')
print('Wrote classification, extraction, capability and side-by-side evidence')
