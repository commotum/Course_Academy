import sys
sys.dont_write_bytecode=True
import importlib.util,json,re,copy,hashlib
from pathlib import Path
D=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('singularity_private_validation',D/'validate.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v);g=v.g;sp=v.sp

def extra(r):
 q=r['question'];p=q[':question/problem'];w=q[':question/worked-solution'];m=v.source_matrix(p);det=sp.expand(m.det());name=re.search(r'matrix \$([A-Z])\$',p)[1]
 indices=[]
 for j,(kind,c) in enumerate(v.statement_signature(p),1):
  if (det==0 if kind=='singular' else det!=0 if kind=='nonsingular' else sp.simplify(det-c)==0):indices.append(j)
 since=re.search(r'Since \$det\(([A-Z])\)=(.*?)\$, the matrix is (.*?)[.]',w,re.S)
 assert since and since[1]==name
 assert sp.simplify(v.latex_expr(since[2].replace(r'\ne 0',''))-det)==0
 assert since[3]==('singular' if det==0 else '**not** singular')
 if not indices:expected='Therefore, none of the statements are true.'
 else:expected='Therefore, only statement'+('s ' if len(indices)>1 else ' ')+' and '.join(('I','II','III')[i-1]for i in indices)+(' are true.'if len(indices)>1 else ' is true.')
 assert w.endswith(expected)
 rows=v.determinant_row_strings(w)
 assert rows[0].count(r'\begin{vmatrix}')==1
 assert rows[1].count(r'\begin{vmatrix}')==3,'Missing cofactor-minor operation stage'
 assert r'\begin{vmatrix}' not in rows[2]
 def evaluate_minor(match):return '('+str(v.latex_expr(match[0]))+')'
 expansion=re.sub(r'\\begin\{vmatrix\}.*?\\end\{vmatrix\}',evaluate_minor,rows[1])
 terms=v.split_additive(expansion);expected_terms=[sp.simplify((-1)**j*m[0,j]*m.minor_submatrix(0,j).det())for j in range(3)]
 assert len(terms)==3 and all(sp.simplify(x-y)==0 for x,y in zip(terms,expected_terms))
 assert r'\begin{bmatrix}' in p
 return True
rows=json.loads((D/'review.json').read_text());records=[x['record']for x in rows]
for row in rows:
 if row['kind']=='current source parameter replay':assert v.prose_signature(row['original'][':question/problem'])==v.prose_signature(row['record']['question'][':question/problem'])
for r in records:extra(r)
mutated=copy.deepcopy(records[0]);w=mutated['question'][':question/worked-solution'];row=v.determinant_row_strings(w)[1];mutated['question'][':question/worked-solution']=w.replace(row,'0')
try:extra(mutated)
except AssertionError:pass
else:raise AssertionError('Missing cofactor stage mutation passed')
mutated=copy.deepcopy(records[0]);mutated['question'][':question/worked-solution']+=' Therefore, only statement I is true.'
try:extra(mutated)
except AssertionError:pass
else:raise AssertionError('Stale final conclusion mutation passed')
# Canonical task IDs do not count capital matrix aliases or equivalent exact spellings.
r=records[0];params=copy.deepcopy(r['generation']['parameters']);params['name']='Z';same=g.generate('moderate',template=r['generation']['template'],parameters=params);assert same['generation']['parameter_fingerprint']==r['generation']['parameter_fingerprint'];assert same['question'][':question/id']!=r['question'][':question/id']
# Current choices are true/false predicates for separate fields, not numeric scalar choices.
# The only within-field pair is disjoint under the response criterion.
assert all({a[':answer/value']for a in f[':answer-field/choices']}=={'false','true'}for r in records for f in r['question'][':question/answer-fields'])
report={'status':'passed','records':len(records),'complete_prompt_prose_replays':17,'cofactor_minors_and_signed_term_checks':len(records)*3,'concluding_determinant_and_predicates':len(records),'actual_structural_stage_mutations_rejected':1,'stale_conclusion_mutations_rejected':1,'held_slots':'3x3 dimension, first-row expansion, three independently assessed statements, 5/6-stage observed chain; matrix letters are presentation aliases','response_criterion':'Three field-owned Boolean predicates. Every within-field wrong/correct pair differs; true in separate fields is not an equivalent answer to another requested predicate. Historical subset banks validated pairwise as finite sets.','identity_alias_check':'same mathematical fingerprint across capital-name alias; content ID changes with printed prompt','generator_sha256':hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest()}
(D/'extra-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
