#!/usr/bin/env python3
"""Author exact missing keys/solutions for five explicit completion targets.

Reads captured basis14371 only; never calls EDB or writes peer artifacts.
New answers are declarations for root's guarded native transaction, not DB IDs.
"""
from pathlib import Path
import collections,json,re,sys,uuid
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,rationalize
HERE=Path(__file__).resolve().parent;BASE=HERE.parent
ROOT=next(p for p in HERE.parents if (p/'scripts/question_capture/math_format.py').exists());sys.path.insert(0,str(ROOT))
from scripts.question_capture.math_format import matrix_tex,validate_prose
QS={q[':db/id']:q for q in json.loads((BASE/'capture/questions.json').read_text())}
PARENTS=json.loads((BASE/'completion-context/parents.json').read_text())
REPAIRED={p['entity']:p['after'] for p in json.loads((BASE/'proposals.json').read_text())}
NS=uuid.UUID('c4fa99ea-25d2-5c70-8b82-3130e074eadb')
x,y,lam=sp.symbols('x y lambda',real=True)

def mat(rows):return matrix_tex(rows)
def display(s):return '$$\n'+s+'\n$$'
def dump(name,data):(HERE/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')

DATA={
17592186167247:{'f':[x-sp.Rational(1,2)*x*y,-sp.Rational(1,5)*y+2*x*y],'point':[sp.Rational(1,10),2],
 'f_tex':['x-0.5xy','-0.2y+2xy'],'J_tex':[['1-0.5y','-0.5x'],['2y','-0.2+2x']],
 'eval_tex':[['1-0.5(2)','-0.5(0.1)'],['2(2)','-0.2+2(0.1)']],
 'point_tex':['0.1','2'],'values':['0','-0.05','4','0'],
 'characteristic_tex':r'\det(J(\mathbf{x}^{\ast})-\lambda I)=\lambda^2+0.2=0',
 'conclusion':r'The eigenvalues are $\lambda_{1,2}=\pm\frac{1}{\sqrt{5}}\,\mathrm{i}.$ For this classical Lotka–Volterra model, the positive coexistence equilibrium is a stable center. It is not asymptotically stable.',
 'classification':'stable center; not asymptotically stable; classical positive Lotka-Volterra coexistence equilibrium',
 'nearby':[17592186167246,17592186370201]},
17592186167252:{'f':[2*x*(1-x)-x*y,-2*y+4*x*y],'point':[1,0],
 'f_tex':['2x(1-x)-xy','-2y+4xy'],'J_tex':[['2-4x-y','-x'],['4y','-2+4x']],
 'eval_tex':[['2-4(1)-0','-1'],['4(0)','-2+4(1)']],
 'point_tex':['1','0'],'values':['-2','-1','0','2'],
 'characteristic_tex':r'\det(J(\mathbf{x}^{\ast})-\lambda I)=(-2-\lambda)(2-\lambda)=\lambda^2-4=0',
 'conclusion':r'The eigenvalues are $\lambda_1=-2$ and $\lambda_2=2.$ Since they are real with opposite signs, the equilibrium is an unstable saddle.',
 'classification':'unstable saddle',
 'nearby':[17592186167261,17592186370423]},
17592186167253:{'f':[2*x*(1-4*x)-x*y,-2*y+4*x*y],'point':[sp.Rational(1,4),0],
 'f_tex':['2x(1-4x)-xy','-2y+4xy'],'J_tex':[['2-16x-y','-x'],['4y','-2+4x']],
 'eval_tex':[['2-16(0.25)-0','-0.25'],['4(0)','-2+4(0.25)']],
 'point_tex':['0.25','0'],'values':['-2','-0.25','0','-1'],
 'characteristic_tex':r'\det(J(\mathbf{x}^{\ast})-\lambda I)=(-2-\lambda)(-1-\lambda)=\lambda^2+3\lambda+2=0',
 'conclusion':r'The eigenvalues are $\lambda_1=-2$ and $\lambda_2=-1.$ Since both are real and negative, the equilibrium is an asymptotically stable sink.',
 'classification':'asymptotically stable sink',
 'nearby':[17592186167254,17592186370462]},
17592186221965:{'f':[x*x-y,3*x+y*y],'point':[0,0],
 'f_tex':['x^2-y','3x+y^2'],'J_tex':[['2x','-1'],['3','2y']],
 'eval_tex':[['2(0)','-1'],['3','2(0)']],
 'point_tex':['0','0'],'deviation_tex':['x','y'],'values':['0','-1','3','0'],
 'classification':'linearized matrix has purely imaginary eigenvalues; nonlinear classification is not requested or inferred',
 'nearby':[17592186368134,17592186368143]},
17592186221966:{'f':[x*x-x+2*y-4,-3*x+y*y-4*y+7],'point':[1,2],
 'f_tex':['x^2-x+2y-4','-3x+y^2-4y+7'],'J_tex':[['2x-1','2'],['-3','2y-4']],
 'eval_tex':[['2(1)-1','2'],['-3','2(2)-4']],
 'point_tex':['1','2'],'deviation_tex':['x-1','y-2'],'values':['1','2','-3','0'],
 'classification':'eigenvalues (1±sqrt(23)i)/2; positive real part (not needed in requested linearization answer)',
 'nearby':[17592186368134,17592186368143]}}

def solution(d,lotka):
 f1,f2=d['f_tex'];general=mat(d['J_tex']);numeric=mat([d['values'][:2],d['values'][2:]])
 point=mat([[v] for v in d['point_tex']]);evaluated=mat(d['eval_tex'])
 derivatives=(r'\begin{aligned}\frac{\partial f_1}{\partial x}&='+d['J_tex'][0][0]+r', & \frac{\partial f_1}{\partial y}&='+d['J_tex'][0][1]+r', \\ \frac{\partial f_2}{\partial x}&='+d['J_tex'][1][0]+r', & \frac{\partial f_2}{\partial y}&='+d['J_tex'][1][1]+r'.\end{aligned}')
 if lotka:
  return (f"Let's denote $f_1(x,y)={f1}$ and $f_2(x,y)={f2}.$\n\nNow, we compute the partial derivatives:\n\n"+display(derivatives)+'\n\nThus, the Jacobian matrix is\n\n'+display('J(x,y)='+general+'.')+'\n\nNext, we evaluate the Jacobian at the equilibrium $\\mathbf{x}^{\\ast}='+point+'$ to get\n\n'+display('J(\\mathbf{x}^{\\ast})='+evaluated+'='+numeric+'.')+'\n\nTo find the eigenvalues of the Jacobian matrix, we write down the characteristic equation:\n\n'+display(d['characteristic_tex']+'.')+'\n\n'+d['conclusion'])
 return ('The system can be rewritten in matrix form as\n\n'+display(r'\mathbf{x}^{\prime}=\boldsymbol{f}(\mathbf{x}),\qquad \mathbf{x}='+mat([['x(t)'],['y(t)']])+r',\qquad \boldsymbol{f}(\mathbf{x})='+mat([[f1],[f2]])+'.')+'\n\nWe need to compute the Jacobian matrix (or the total derivative) of $\\boldsymbol{f}.$ First, we compute the partial derivatives:\n\n'+display(derivatives)+'\n\nThus, we have\n\n'+display('J(x,y)='+general+'.')+'\n\nNext, we evaluate the Jacobian at the equilibrium $\\mathbf{x}^{\\ast}='+point+'$ to get\n\n'+display('J(\\mathbf{x}^{\\ast})='+evaluated+'='+numeric+'.')+'\n\nFinally, near the equilibrium, the nonlinear system is approximated by\n\n'+display(r'\mathbf{u}^{\prime}='+numeric+r'\mathbf{u},')+'\n\nwhere the deviation vector is\n\n'+display(r'\mathbf{u}=\mathbf{x}-\mathbf{x}^{\ast}='+mat([['x'],['y']])+'-'+point+'='+mat([[v] for v in d['deviation_tex']])+'.'))

props=[];new=[];evidence=[]
for eid,d in DATA.items():
 q=QS[eid];lotka=eid<17592186200000
 kp=next(k for k in PARENTS if any(z[':db/id']==eid for z in k.get(':knowledge-point/questions',[])))
 canonical=kp[':knowledge-point/canonical-example'];assert canonical.get(':question/worked-solution')
 neighbors={z[':db/id']:z for z in kp[':knowledge-point/questions']}
 for nid in d['nearby']:assert neighbors[nid].get(':question/worked-solution')
 F=sp.Matrix(d['f']);J=F.jacobian([x,y]);point=dict(zip([x,y],d['point']));JP=J.subs(point)
 assert F.subs(point)==sp.zeros(2,1)
 expected=sp.Matrix(2,2,[sp.Rational(v) for v in d['values']]);assert JP==expected
 for i in range(2):
  for j in range(2):assert sp.expand(parse_expr(d['J_tex'][i][j],local_dict={'x':x,'y':y},transformations=standard_transformations+(implicit_multiplication_application,rationalize))-J[i,j])==0
 field_evidence=[]
 for i,f in enumerate(sorted(q[':question/answer-fields'],key=lambda f:f[':answer-field/key'])):
  key=f[':answer-field/key'];index=int(key.removeprefix('field-'))-1;val=d['values'][index]
  assert ':answer-field/correct' not in f
  choices=f.get(':answer-field/choices',[])
  matches=[a for a in choices if sp.Rational(a[':answer/value'])==sp.Rational(val)]
  assert len(matches)<=1
  fe={'field_entity':f[':db/id'],'field_key':key,'matrix_position':[index//2+1,index%2+1],'expected_value':val,'existing_choices':[{ 'entity':a[':db/id'],'value':a[':answer/value'],'is_correct':a in matches} for a in choices]}
  if matches:
   selected=matches[0];props.append({'entity':f[':db/id'],'attribute':'answer-field/correct','before':None,'after':selected[':db/id']});fe['selected_existing_answer_entity']=selected[':db/id']
  else:
   assert not choices or (eid==17592186167247 and key=='field-3' and val=='4')
   tempid='matrix-completion-answer-'+str(f[':db/id']);uid=str(uuid.uuid5(NS,str(f[':db/id'])+':'+val))
   new.append({'question_entity':eid,'field_entity':f[':db/id'],'field_key':key,'answer_type':':answer.type/math','answer_value':val,'answer_uuid':uid,'answer_tempid':tempid,'reason':'missing correct option in existing select bank' if choices else 'empty blank answer bank','ownership_attribute':'answer-field/choices','correct_attribute':'answer-field/correct'})
   fe.update(required_new_answer_tempid=tempid,required_new_answer_uuid=uid,missing_existing_correct_choice=True)
  field_evidence.append(fe)
 assert len(field_evidence)==4
 authored=solution(d,lotka);validate_prose(authored)
 assert not re.search(r'\{\{(?:answer-field:)?field-',authored)
 before=q.get(':question/worked-solution');assert before is None or not before.strip()
 props.append({'entity':eid,'attribute':'question/worked-solution','before':before,'after':authored})
 stages=['name component functions','compute four partial derivatives','assemble Jacobian','evaluate at specified equilibrium']
 stages+=['compute characteristic polynomial and eigenvalues','classify the specified target equilibrium'] if lotka else ['write u-prime=J(x-star)u','define the shifted deviation vector']
 template={'canonical_question_entity':canonical[':db/id'],'canonical_source_id':canonical[':question/math-academy-id'],'canonical_problem':canonical[':question/problem'],'canonical_solution':canonical[':question/worked-solution'],'matching_nearby_question_entities':d['nearby'],'matching_nearby_solutions':[{ 'entity':nid,'source_id':neighbors[nid][':question/math-academy-id'],'problem':neighbors[nid][':question/problem'],'solution':neighbors[nid][':question/worked-solution']} for nid in d['nearby']],'preserved_stage_order':stages,'response_contract':'four row-major scalar Jacobian entries only; the target does not contain canonical classification fields' if lotka else 'four row-major scalar entries in the matrix multiplying the deviation vector','target_specific_difference':'Target equilibrium may have a different stability classification than the canonical example; evaluate the specified point independently.' if lotka else 'Substitute target component functions and equilibrium; preserve the canonical linearization and deviation-vector method.'}
 ev={'question_entity':eid,'question_uuid':q[':question/id'],'source_id':q[':question/math-academy-id'],'knowledge_point_entity':kp[':db/id'],'knowledge_point_title':kp[':knowledge-point/title'],'basis':14371,'authorship':'Locally authored completion derived independently from the target and adapted to stored canonical/nearby worked-solution templates; not an observed Math Academy answer.','original_problem':q[':question/problem'],'layout_repaired_problem':REPAIRED[eid],'template_comparison':template,'derivation':{'component_functions':[str(v) for v in F],'equilibrium':[str(v) for v in d['point']],'equilibrium_verified':True,'Jacobian_symbolic':[[str(v) for v in row] for row in J.tolist()],'Jacobian_at_equilibrium':[[str(v) for v in row] for row in JP.tolist()],'characteristic_polynomial':str(JP.charpoly(lam).as_expr()),'eigenvalues':[{ 'value':str(k),'multiplicity':v} for k,v in JP.eigenvals().items()],'classification':d['classification']},'fields':field_evidence,'worked_solution':authored,'preserved':{'existing_correct_links':True,'existing_solutions':True,'all_existing_choice_ids_and_values':True,'question_field_and_source_ids':True,'KP_membership':True},'validation':{'exact_symbolic_jacobian':True,'equilibrium_verified':True,'unique_existing_choice_or_explicit_new_answer':True,'solution_prose_validation':True,'application_read_only_grader':'pending root native preview and saved-content verification; no grader claim from mathematical checks alone'}}
 if eid==17592186167252:ev['KP_context_distinction']='The specified target equilibrium [1,0] is a saddle. The parent title Stable Case may describe the model parameter regime rather than every equilibrium; this target calculation alone does not establish an inconsistency in KP placement. KP membership is preserved.'
 if eid==17592186167247:
  H=2*x-sp.Rational(1,5)*sp.log(x)+sp.Rational(1,2)*y-sp.log(y)
  assert sp.simplify(sp.diff(H,x)*F[0]+sp.diff(H,y)*F[1])==0
  Hess=sp.hessian(H,[x,y]).subs(point);assert all(v>0 for v in Hess.eigenvals())
  ev['derivation']['nonlinear_center_verification']={'first_integral':str(H),'time_derivative_exact':'0','Hessian_at_equilibrium':[[str(v) for v in row] for row in Hess.tolist()],'conclusion':'First integral has a strict local minimum at the positive equilibrium; nearby level curves are closed, confirming a stable center rather than relying on purely imaginary linearized eigenvalues alone.'}
 evidence.append(ev)
assert len(props)==16 and len(new)==9
assert sum(p['attribute']=='answer-field/correct' for p in props)==11
assert sum(p['attribute']=='question/worked-solution' for p in props)==5
dump('completion-proposals.json',props);dump('answer-creations.json',new);dump('completion-evidence.json',{'basis':14371,'status':'prepared for root transaction; application preview pending','target_count':5,'existing_answer_correct_refs':11,'required_new_owned_answers':9,'new_worked_solutions':5,'unresolved_math_or_choices':[],'questions':evidence})
print(json.dumps({'existing_refs':11,'new_owned_answers':9,'worked_solutions':5,'all_exact_checks_passed':True},indent=2))
