import json,re,collections
from pathlib import Path
import sympy as sp
BASE=Path('reference/edb-math/imports/authored-checkboxes/2026-10-12/discovery-next');OUT=BASE/'reviews';p=OUT/'text-cases.json';d=json.load(open(p));snap={x[0][':db/id']:x[0]for x in json.load(open(BASE/'snapshot.json'))['questions']}
def echelon(M):
 piv=[];seen=False
 for row in M.tolist():
  nz=[i for i,x in enumerate(row)if x!=0]
  if not nz:seen=True
  elif seen:return False
  else:piv.append(nz[0])
 return all(a<b for a,b in zip(piv,piv[1:]))
def matrix(s):
 t=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',s,re.S).group(1);return sp.Matrix([[sp.Rational(x.strip())for x in r.split('&')]for r in re.split(r'\\\\',t)])
rows=[]
for q in d['questions']:
 if q['kps'][0]['title']!='Identifying Augmented Matrices in Row Echelon Form':continue
 labels=[a['label']for a in q['atomic_options']];full=[echelon(matrix(a['text']))for a in q['atomic_options']];coeff=[echelon(matrix(a['text'])[:,:-1])for a in q['atomic_options']];source=snap[q['id']];sol=source[':question/worked-solution'];different=full!=coeff
 row={'id':q['id'],'ma_id':q['ma_id'],'labels':labels,'full_augmented_ref':full,'coefficient_block_ref':coeff,'key':q['correct_labels'],'key_value':source[':question/answer-fields'][0][':answer-field/correct'][':answer/value'],'source_solution_predicate':sol.split('\n\n')[0],'different':different,'resolution':'required_prompt_clarification_to_source_coefficient_predicate'if different else 'same_verdict_under_both_interpretations'};rows.append(row);q['key_evidence']['augmented_ref_comparison']=row
 if different:
  before=q['source_problem'];after=before.replace('Which of the following augmented matrices are in row echelon form?','Which of the following augmented matrices have coefficient matrices in row echelon form? Treat the final column of each augmented matrix as its constants column.')
  assert after!=before or 'coefficient matrices'in before
  q['proposed_prompt']=after+'\n\nSelect all that apply.';q['reason']='Converted with required prompt clarification: captured solution and database key test the coefficient block, while full augmented-matrix REF gives different verdicts.'
  q['content_repairs']=[r for r in q['content_repairs']if r['attribute']!=':question/problem'];q['content_repairs'].append({'attribute':':question/problem','before':before,'after':after,'required_for_conversion':True,'handled_by_main_prompt_cas':True,'reason':'Source solution explicitly tests the coefficient matrix. Clarification resolves full-vs-coefficient REF ambiguity and preserves the stored key.'})
for q in d['questions']:
 if q['ma_id']=='q-31919':
  q['decision']='convert';q['classification']='finite_completion_statements';q['reason']='Finite listed completions are independently testable. Noninvertible and singular overlap for square matrices, so this is not a mutually exclusive category bank. Under det(A)≠0 only completion I is true; preserve the stored subset.';q['proposed_prompt']=q['source_problem']+'\n\nSelect all that apply.';q['key_evidence']['independent_proof']='For square A, det(A)≠0 iff A is invertible. Thus I is true, II (not invertible) and III (singular) are false; II and III have the same meaning, not mutually exclusive categories.'
  for a in q['atomic_options']:a['proof']=q['key_evidence']['independent_proof']
d['counts']['decisions']=dict(collections.Counter(q['decision']for q in d['questions']));d['counts']['classes']=dict(collections.Counter(q['classification']for q in d['questions']));d['counts']['atomic_checkbox_fields']=sum(len(q['atomic_options'])for q in d['questions']if q['decision']=='convert');d['counts']['old_choices_mapped']=sum(len(q['choice_mapping'])for q in d['questions']if q['decision']=='convert');d['counts']['required_prompt_clarifications']=sum(r['different']for r in rows);p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n');(OUT/'text-augmented-ref-comparison.json').write_text(json.dumps(rows,indent=2,ensure_ascii=False)+'\n');print(json.dumps(rows,indent=2));print(d['counts'])
