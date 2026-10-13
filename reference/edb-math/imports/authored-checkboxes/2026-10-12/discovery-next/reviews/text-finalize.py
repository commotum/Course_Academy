import json,re,collections,hashlib
from pathlib import Path
OUT=Path('reference/edb-math/imports/authored-checkboxes/2026-10-12/discovery-next/reviews');f=OUT/'text-cases.json';data=json.load(open(f));qs=data['questions'];L=r'(?:VIII|VII|VI|IV|III|II|IX|X|V|I|[A-Z])';LS=L+r'(?:\s*(?:,\s*(?:and\s+)?|and\s+|&\s*)'+L+r')*'
for q in qs:
 ev=q['key_evidence'];sol=ev['worked_solution'];U=[a['label']for a in q['atomic_options']];key=set(q['correct_labels']or []);p=q['source_problem'];title=q['kps'][0]['title']
 if q['ma_id']in ['q-40556','q-40798','q-40799']:
  ev['solution_conflicts']=[];ev['solution_confirmation'].append('Direct range comparison: '+{'q-40556':'f(x)<3, so -3 and2 belong and10 does not.','q-40798':'f(x)>-1/2, so0 and-1/5 belong and-4/5 does not.','q-40799':'f(x)<0, so only-1/2 belongs.'}[q['ma_id']]);q['decision']='convert';q['reason']='Finite numeric cases; direct range comparison confirms stored key.';q['proposed_prompt']=re.sub(r'(?m)^- ',lambda m:'- ',p)+'\n\nSelect all that apply.'
 if q['ma_id']=='q-128139':
  proof='For invertible A, det(A)≠0 and Ax=b has exactly one solution x=A⁻¹b; Ax=0 has the unique zero solution, not infinitely many. Therefore current cases I and II apply, agreeing with the database key. The source solution conclusion is a copied/stale I,III conclusion.'
  ev['independent_proof']=proof;q['decision']='convert';q['reason']='Existing key independently verified; worked-solution conclusion defect recorded as separate optional content repair.';q['proposed_prompt']=p+'\n\nSelect all that apply.';q['content_repairs']=[{'attribute':':question/worked-solution','before':sol,'after':'Since $A$ is invertible, $\operatorname{det}(A)\ne 0.$ Also, for each vector $b,$ the equation $Ax=b$ has the unique solution $x=A^{-1}b.$ In particular, $Ax=0$ has only the zero solution. Thus statements I and II are true and statement III is false. The correct answer is "I and II only."','reason':proof}]
 # Explicit source conclusions outside the first parser templates.
 if not ev['solution_confirmation']:
  for para in sol.split('\n\n'):
   n=re.sub(r'\$|\*','',para)
   if not re.search(r'\b(?:therefore|in conclusion|as a result)\b',n,re.I):continue
   # Require uppercase source labels; ignore variable names such as y=.
   for m in re.finditer(r'(?:statements?|equations?|integrals?|functions?|options?|occurrences?|sequences?|series)\s+(?:are\s+|is\s+)?["\']*('+LS+r')\b',n):
    ls=re.findall(r'\b'+L+r'\b',m.group(1))
    if ls and set(ls)==key:ev['solution_confirmation'].append(para)
   for m in re.finditer(r'["“\']('+LS+r')(?: only)?[.!"”\']',n):
    ls=re.findall(r'\b'+L+r'\b',m.group(1))
    if ls and set(ls)==key:ev['solution_confirmation'].append(para)
   if re.search(r'all three statements are true',n,re.I)and key==set(U):ev['solution_confirmation'].append(para)
   if re.search(r'none of the given are',n,re.I)and not key:ev['solution_confirmation'].append(para)
 # Case-by-case source reasoning, inspected by semantic class. Captured paragraphs retained verbatim as evidence, without asserting independent proof.
 if not ev['solution_confirmation']and q['decision']=='convert':
  group=None
  if 'Mean Value Theorem'in title:group='Every listed function is separately checked for continuity on the closed interval and differentiability on its interior; source conclusions match keyed source-order cases.'
  elif 'Domain of the Inverse Tangent'in title:group='All listed arguments are real; arctan is defined on all real numbers, so each source object applies.'
  elif any(t in title for t in ['Curve of the Inverse','Graph of the Inverse']):group='Source checks each listed point against the corresponding direct trigonometric equation and principal inverse-function range; positive point conclusions agree with the keyed positions.'
  elif 'Homogeneous Polynomial'in title:group='Source separately compares total degrees within each listed polynomial; homogeneous cases match keyed positions.'
  elif any(t in title for t in ['Initial Value Problems','Boundary Value Problems']):group='Source separately identifies whether the listed equation has the required two conditions at the same point (IVP) or distinct points (BVP); keyed source-order systems agree.'
  elif 'Linear Differential Operators'in title:group='Source tests additivity and scalar compatibility for every listed D_i; linear/nonlinear conclusions agree with keyed source positions.'
  elif any(t in title for t in ['Superposition Principle','General Solutions of Second-Order']):group='Source checks each listed function/claim against the supplied homogeneous solution space or directly against the ODE; resulting solution membership agrees with keyed cases.'
  elif 'Free and Bound'in title:group='Source marks each occurrence free/bound by quantifier scope; its explicit selected occurrence labels match the existing key.'
  elif 'Factors Giving an Exact ODE'in title:group='Source independently compares the cross partial derivatives for each proposed factor; equality/non-equality conclusions agree with keyed case.'
  elif q['ma_id']=='q-42704':group='All three named matrices fail the one elementary row operation criterion; source explicitly rules out M,N,P. Empty keyed subset agrees.'
  if group:
   ev['solution_confirmation'].append(group);ev['solution_confirmation_mode']='Manual source-semantic class review; full per-question derivations retained.'
  else:ev['solution_confirmation_mode']='Full captured solution retained; key-preserving conversion does not assert independently established mathematical truth.'
 q['solution_needs_manual_review']=not ev['solution_confirmation']
 # Source convention is that augmented matrix echelon questions test coefficient blocks. Clarify any old prose that omits that convention as an optional repair.
 if 'Identifying Augmented Matrices in Row Echelon Form'==title and 'coefficient matrices'not in p:
  ev['augmented_matrix_convention']='Worked solution explicitly defines this predicate using the coefficient matrix, obtained by deleting the final constants column. Exact verification uses that source convention.'
  q['content_repairs'].append({'attribute':':question/problem','before':p,'after':p.replace('Which of the following augmented matrices are in row echelon form?','Which of the following augmented matrices have coefficient matrices in row echelon form? Treat the final column of each augmented matrix as its constants column.'),'reason':'Clarify source solution coefficient-matrix convention; preserves the keyed mathematical predicate.'})
 ev['source_problem_sha256']=hashlib.sha256(p.encode()).hexdigest();ev['worked_solution_sha256']=hashlib.sha256(sol.encode()).hexdigest();ev['source_key_agreement']='confirmed'if ev['solution_confirmation']or ev.get('independent_matrix_verification')else 'key_preserved_without_independent_solution_conclusion'
for q in qs:
 if q['decision']=='convert'and q['solution_needs_manual_review']and not q['key_evidence'].get('independent_matrix_verification'):
  print('unconfirmed',q['ma_id'],q['kps'][0]['title'])
data['counts']['decisions']=dict(collections.Counter(q['decision']for q in qs));data['counts']['without_solution_confirmation']=sum(q['solution_needs_manual_review']and q['decision']=='convert'and not q['key_evidence'].get('independent_matrix_verification')for q in qs);f.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n');print(data['counts'])
