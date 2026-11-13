#!/usr/bin/env python3
"""Complete four explicitly assigned gradient/Hessian imports; no EDB writes."""
import json,re,sys,uuid
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent;BASE=HERE.parent
ROOT=next(p for p in HERE.parents if (p/'scripts/question_capture/math_format.py').exists())
sys.path.insert(0,str(ROOT))
from scripts.question_capture.math_format import matrix_tex,normalize_prose,validate_prose,validate_tex
qs={}
for file in ['capture/questions.json','gradient-capture/questions.json']:
    qs.update({q[':db/id']:q for q in json.loads((BASE/file).read_text())})
kps={p[':db/id']:p for p in json.loads((BASE/'gradient-completion-context/parents.json').read_text())}
NS=uuid.UUID('c4fa99ea-25d2-5c70-8b82-3130e074eadb')
x,y,z,w,a,b,c,m=sp.symbols('x y z w a b c m')
expected={17592186204560:sp.Matrix([x,1]),17592186204562:sp.Matrix([[2*y,2*x],[2*x,0]]),
          17592186204565:sp.Matrix([y**2,2*x*y+z**2]),17592186204566:sp.Matrix([x,1])}
assert sp.Matrix([sp.diff(m*x+b,m),sp.diff(m*x+b,b)])==expected[17592186204560]
assert sp.hessian(x**2*y+y*z**2,(x,y))==expected[17592186204562]
assert sp.Matrix([sp.diff(x*y**2+y*z**2+z*w**2,v) for v in (x,y)])==expected[17592186204565]
assert sp.Matrix([sp.diff(a*x+b*y+c,v) for v in (a,c)])==expected[17592186204566]

def display(tex):return '$$\n'+tex+'\n$$'
def gradient_solution(variables,expression,results,basic=False):
    v1,v2=variables
    intro=f'To compute $\\nabla_{{{v1},{v2}}}f$, we take partial derivatives with respect to ${v1}$ and ${v2}$'+(' only.' if basic else '.')
    derivatives=r'\begin{aligned}'+r'\frac{\partial f}{\partial '+v1+r'} &=\frac{\partial}{\partial '+v1+'}('+expression+')='+results[0]+r' \\ '+r'\frac{\partial f}{\partial '+v2+r'} &=\frac{\partial}{\partial '+v2+'}('+expression+')='+results[1]+r'\end{aligned}'
    result=r'\begin{aligned}\nabla_{'+v1+','+v2+'}f &='+matrix_tex([[r'\frac{\partial f}{\partial '+v1+'}'],[r'\frac{\partial f}{\partial '+v2+'}']])+r' \\ &='+matrix_tex([[results[0]],[results[1]]])+r'\end{aligned}'
    return intro+'\n\n'+display(derivatives)+'\n\nTherefore, we obtain the following:\n\n'+display(result)

hessian_solution=('First, we take the variable subset gradient:\n\n'+display(r'\nabla_{x,y}f='+matrix_tex([[r'\frac{\partial}{\partial x}(x^{2}y+yz^{2})'],[r'\frac{\partial}{\partial y}(x^{2}y+yz^{2})']])+'='+matrix_tex([['2xy'],['x^{2}+z^{2}']]))+'\n\nNext, we compute the second derivatives with respect to $x$ and $y$:\n\n'+display(r'\begin{aligned}\frac{\partial}{\partial x}(2xy) &=2y & \frac{\partial}{\partial y}(2xy) &=2x \\ \frac{\partial}{\partial x}(x^{2}+z^{2}) &=2x & \frac{\partial}{\partial y}(x^{2}+z^{2}) &=0\end{aligned}')+'\n\nTherefore, we obtain the following:\n\n'+display(r'\begin{aligned}\nabla_{x,y}(\nabla_{x,y}f) &='+matrix_tex([[r'\frac{\partial^{2}f}{\partial x^{2}}',r'\frac{\partial^{2}f}{\partial x\partial y}'],[r'\frac{\partial^{2}f}{\partial y\partial x}',r'\frac{\partial^{2}f}{\partial y^{2}}']])+r' \\ &='+matrix_tex([['2y','2x'],['2x','0']])+r'\end{aligned}'))

TARGETS={
17592186204560:{'kp':17592186204086,'near':[17592186530425,17592186530461],
 'values':['x','1'],'positions':[[1,1],[2,1]],'solution':gradient_solution(('m','b'),'mx+b',['x','1']),
 'function':'f(x;m,b)=mx+b','differentiate':['m','b'],'held_fixed':['x'],
 'derivation':['partial(mx+b)/partial m=x','partial(mx+b)/partial b=1'],
 'template':'Parameter subset gradient: differentiate only with respect to the two listed parameters, holding input variables fixed, then put the derivatives into a column in the stated parameter order.',
 'incorrect':['m','b'],'equivalent':['1*x','2-1']},
17592186204562:{'kp':17592186204088,'near':[17592186530530,17592186530538],
 'values':['2y','2x','2x','0'],'positions':[[1,1],[1,2],[2,1],[2,2]],'solution':hessian_solution,
 'function':'f(x,y,z)=x^2*y+y*z^2','differentiate':['x','y'],'held_fixed':['z'],
 'derivation':['First gradient=(2*x*y,x^2+z^2)^T','Differentiate first component with respect to x,y: (2*y,2*x)','Differentiate second component with respect to x,y: (2*x,0)','Hessian=[[2*y,2*x],[2*x,0]], symmetric in the mixed partials'],
 'template':'Subset Hessian: compute the first subset gradient; differentiate each gradient component in the same ordered variable subset; assemble all four second derivatives row by row. Canonical uses a parameter vector; matching nearby x,y and x,z examples verify the target variable ordering and matrix layout.',
 'incorrect':['2x','2y','2y','1'],'equivalent':['y+y','x+x','x+x','0*x']},
17592186204565:{'kp':17592186204085,'near':[17592186204559,17592186530463],
 'values':['y^{2}','2xy+z^{2}'],'positions':[[1,1],[2,1]],
 'solution':gradient_solution(('x','y'),'xy^{2}+yz^{2}+zw^{2}',['y^{2}','2xy+z^{2}'],basic=True),
 'function':'f(x,y,z,w)=x*y^2+y*z^2+z*w^2','differentiate':['x','y'],'held_fixed':['z','w'],
 'derivation':['partial f/partial x=y^2','partial f/partial y=2*x*y+z^2','The term z*w^2 is constant with respect to both selected variables.'],
 'template':'Basic subset gradient: compute partial derivatives with respect to x and y only, holding all other variables fixed, then assemble the two components as a column in the requested order.',
 'incorrect':['2xy','y^{2}+2zw'],'equivalent':['y*y','z^2+2*y*x']},
17592186204566:{'kp':17592186204086,'near':[17592186530425,17592186530461],
 'values':['x','1'],'positions':[[1,1],[2,1]],'solution':gradient_solution(('a','c'),'ax+by+c',['x','1']),
 'function':'f(x,y;a,b,c)=a*x+b*y+c','differentiate':['a','c'],'held_fixed':['x','y','b'],
 'derivation':['partial(ax+by+c)/partial a=x','partial(ax+by+c)/partial c=1','b is a parameter of f but is not in the requested differentiation subset.'],
 'template':'Parameter subset gradient: use the requested parameter subset a,c in its stated order, holding x,y and the unselected parameter b fixed; assemble the derivatives as a column.',
 'incorrect':['a','y'],'equivalent':['1*x','2-1']}}

proposals=[];answers=[];evidence=[];grading=[]
for qid,target in TARGETS.items():
 q=qs[qid];kp=kps[target['kp']];canonical=kp[':knowledge-point/canonical-example'];assert canonical.get(':question/worked-solution')
 near=[next(v for v in kp[':knowledge-point/questions'] if v[':db/id']==eid) for eid in target['near']]
 assert all(n.get(':question/worked-solution') for n in near)
 fields={f[':answer-field/key']:f for f in q[':question/answer-fields']}
 assert set(fields)=={f'field-{i+1}' for i in range(len(target['values']))}
 solution=normalize_prose(target['solution']);validate_prose(solution)
 if not q.get(':question/worked-solution'):
  proposals.append({'entity':qid,'attribute':'question/worked-solution','before':q.get(':question/worked-solution'),
                    'after':solution,'provenance':'locally authored completion; canonical and matching nearby solutions provide the teaching template, not the target answer'})
 mappings=[]
 for i,value in enumerate(target['values']):
  key=f'field-{i+1}';f=fields[key];fid=f[':db/id'];validate_tex(value)
  assert f[':answer-field/type'][':db/ident']==':answer-field.type/blank'
  if f.get(':answer-field/correct'):
   # Never overwrite a valid existing key; no such key existed in these pulls.
   assert f[':answer-field/correct'][':answer/value']==value
   continue
  assert not f.get(':answer-field/choices')
  tempid=f'matrix-completion-answer-{fid}';answer_uuid=str(uuid.uuid5(NS,f'{fid}:{value}'))
  answers.append({'field_entity':fid,'field_key':key,'question_entity':qid,'answer_type':':answer.type/math',
                  'answer_value':value,'answer_uuid':answer_uuid,'answer_tempid':tempid,'correct_before':None,'choices_before':[],
                  'provenance':'locally authored canonical answer, independently differentiated'})
  mappings.append({'field_entity':fid,'field_key':key,'matrix_position':target['positions'][i],
                   'answer_value':value,'answer_tempid':tempid,'existing_correct':None,'existing_answer_bank':[],
                   'unique_value_established':True,'existing_answer_id_available':False})
  grading.append({'question_entity':qid,'field_entity':fid,'field_key':key,'correct_input':value,
                  'equivalent_input':target['equivalent'][i],'incorrect_input':target['incorrect'][i]})
 evidence.append({'question_entity':qid,'question_uuid':q[':question/id'],'imported_id':q[':question/math-academy-id'],
                  'basis':14371,'status':'prepared; native application grading/rendering/commit delegated to root',
                  'knowledge_point_entity':kp[':db/id'],'knowledge_point_title':kp[':knowledge-point/title'],
                  'canonical':canonical,'matching_nearby':near,'template':target['template'],
                  'target':{k:target[k] for k in ['function','differentiate','held_fixed']},
                  'independent_derivation':target['derivation'],'symbolically_verified_result':str(expected[qid]),
                  'answer_field_mapping':mappings,'solution_previously_present':bool(q.get(':question/worked-solution')),
                  'authorship':'local derived completion; not an observed Math Academy answer',
                  'validation':{'exact_sympy_derivatives':True,'validate_prose':True,'validate_tex':True,
                                'identity_changes':False,'database_writes':False,'application_grading':'pending root'}})
assert len(answers)==10 and len(proposals)==4
for file,value in [('supplemental-completion-proposals.json',proposals),('supplemental-answer-creations.json',answers),
                   ('supplemental-completion-evidence.json',evidence),('supplemental-completion-grading-cases.json',grading)]:
 (HERE/file).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'questions':len(TARGETS),'solutions':len(proposals),'new_canonical_answers':len(answers),
                  'exact_derivative_checks':'passed','math_validation':'passed','database_writes':0},indent=2))
