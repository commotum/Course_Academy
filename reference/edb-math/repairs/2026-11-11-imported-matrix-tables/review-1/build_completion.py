#!/usr/bin/env python3
"""Prepare three authored completions from captured basis14371; no DB writes."""
import hashlib
import json
import re
import sys
import uuid
from pathlib import Path
import sympy as sp

HERE=Path(__file__).resolve().parent
BASE=HERE.parent
ROOT=next(p for p in HERE.parents if (p/'scripts/question_capture/math_format.py').exists())
sys.path.insert(0,str(ROOT))
from scripts.question_capture.math_format import matrix_tex,normalize_prose,validate_prose,validate_tex

QUESTIONS={q[':db/id']:q for q in json.loads((BASE/'capture/questions.json').read_text())}
PARENTS={p[':db/id']:p for p in json.loads((BASE/'completion-context/parents.json').read_text())}
LAYOUT={p['entity']:p for p in json.loads((BASE/'proposals.json').read_text()) if p['attribute']=='question/problem'}
NS=uuid.UUID('c4fa99ea-25d2-5c70-8b82-3130e074eadb')

# Independently verify the target mathematics before using nearby prose.
t=sp.symbols('t', positive=True)
x1,x2,w1,w2,z1,z2=sp.symbols('x1 x2 w1 w2 z1 z2')
A=sp.Matrix([[1,5],[0,-2]])
forcing=sp.Matrix([2*sp.log(t),-t**2])
rhs=A*sp.Matrix([x1,x2])+forcing
assert sp.expand(rhs[0]-x1-5*x2)==2*sp.log(t)
assert sp.expand(rhs[1]+2*x2)==-t**2
exponents=[sp.Rational(v,3) for v in [3,-12,9,21]]
powers=[sp.Integer(2)**e for e in exponents]
assert powers==[2,sp.Rational(1,16),8,128]
gradient=[sp.diff(w1*z1+w2*z2,w).subs({z1:2,z2:-1}) for w in [w1,w2]]
assert gradient==[2,-1]

def question_in(kp,eid):
    return next(q for q in PARENTS[kp][':knowledge-point/questions'] if q[':db/id']==eid)

def display(tex):return '$$\n'+tex+'\n$$'

ode_near=question_in(17592186129315,17592186314808)
prefix=ode_near[':question/worked-solution'].split('We have the following system.')[0]
ode_original=r'\left\{\begin{aligned}{x}_{1}^{\prime}(t)-{x}_{1}(t)-5{x}_{2}(t) &=2\ln(t) \\ {x}_{2}^{\prime}(t)+2{x}_{2}(t) &=-t^{2}\end{aligned}\right.'
ode_standard=r'\left\{\begin{aligned}{x}_{1}^{\prime}(t) &={x}_{1}(t)+5{x}_{2}(t)+2\ln(t) \\ {x}_{2}^{\prime}(t) &=-2{x}_{2}(t)-t^{2}\end{aligned}\right.'
ode_solution=prefix+'We have the following system.\n\n'+display(ode_original)+'\n\nWriting our system in standard form, we get the following:\n\n'+display(ode_standard)+'\n\nSo, we can rewrite our system in matrix form as follows:\n\n'+display(r'x^{\prime}(t)='+matrix_tex([['1','5'],['0','-2']])+r'x(t)+'+matrix_tex([[r'2\ln(t)'],['-t^{2}']]))

diag_near=question_in(17592186157268,17592186292544)
diag_prefix=diag_near[':question/worked-solution'].split('Therefore, we have')[0]
diag_sub=[['2^{3/3}','0','0','0'],['0','2^{-12/3}','0','0'],['0','0','2^{9/3}','0'],['0','0','0','2^{21/3}']]
diag_result=[['2','0','0','0'],['0',r'\frac{1}{16}','0','0'],['0','0','8','0'],['0','0','0','128']]
diag_solution=diag_prefix+'Here, the function is $f(z)=2^{z/3}$. Therefore, we have\n\n'+display(r'2^{D/3}='+matrix_tex(diag_sub)+'='+matrix_tex(diag_result)+'.')

grad_near=question_in(17592186204087,17592186530418)
grad_solution=(r'To compute $\nabla_{w}f$, we take partial derivatives with respect to each component of $w.$'+'\n\n'+display(r'\begin{aligned}\frac{\partial f}{\partial w_{1}} &=\frac{\partial}{\partial w_{1}}(w_{1}x_{1}+w_{2}x_{2})=x_{1} \\ \frac{\partial f}{\partial w_{2}} &=\frac{\partial}{\partial w_{2}}(w_{1}x_{1}+w_{2}x_{2})=x_{2}\end{aligned}')+'\n\nTherefore, with $x=[2,-1]^{T}$, we obtain the following:\n\n'+display(r'\nabla_{w}f='+matrix_tex([['x_{1}'],['x_{2}']])+'='+matrix_tex([['2'],['-1']])+'.'))

TARGETS={
17592186129589:{'kp':17592186129315,'near':[17592186314807,17592186314808,17592186314809],
 'values':{'field-1':'1','field-2':'5','field-3':r'2\ln(t)','field-4':'0','field-5':'-2','field-6':'-t^{2}'},
 'positions':{'field-1':'A[1,1]','field-2':'A[1,2]','field-3':'forcing[1]','field-4':'A[2,1]','field-5':'A[2,2]','field-6':'forcing[2]'},
 'solution':ode_solution,
 'template':'Introduce the standard first-order system and its coefficient matrix/forcing vector; copy the target system; isolate both derivatives; collect coefficients row by row and forcing terms in a column. Canonical uses a homogeneous system; matching nearby six-blank examples explicitly support the nonhomogeneous vector term.',
 'parameters':{'coefficient_matrix':[['1','5'],['0','-2']],'forcing_vector':[[r'2\ln(t)'],['-t^{2}']],'domain':'t>0, as required by the given logarithm'},
 'derivation':['x1prime=x1+5*x2+2*ln(t)','x2prime=0*x1-2*x2-t^2','A*x+forcing expands back to both original equations'],
 'incorrect':{'field-1':'-1','field-2':'-5','field-3':r'\ln(t)','field-4':'1','field-5':'2','field-6':'t^{2}'}},
17592186157699:{'kp':17592186157268,'near':[17592186292544,17592186292545,17592186292546],
 'values':{'field-1':'2','field-2':'0','field-3':'0','field-4':r'\frac{1}{16}','field-5':'8','field-6':'128'},
 'positions':{'field-1':'matrix[1,1]','field-2':'matrix[1,2]','field-3':'matrix[1,3]','field-4':'matrix[2,2]','field-5':'matrix[3,3]','field-6':'matrix[4,4]'},
 'solution':diag_solution,
 'template':'State the diagonal-matrix function rule; apply the scalar function to each diagonal entry while keeping every off-diagonal entry zero; evaluate the resulting scalar powers. Canonical logarithm example supplies the rule, nearby base-2 exponential and scaled-sine examples support this scalar-function substitution.',
 'parameters':{'diagonal':[3,-12,9,21],'scalar_function':'f(z)=2^(z/3)','exponents':['1','-4','3','7'],'result_diagonal':['2','1/16','8','128']},
 'derivation':['3/3=1; -12/3=-4; 9/3=3; 21/3=7','2^1=2; 2^-4=1/16; 2^3=8; 2^7=128','All off-diagonal entries remain zero; this is not entrywise exponentiation of all matrix entries.'],
 'incorrect':{'field-1':'8','field-2':'1','field-3':'1','field-4':'16','field-5':'512','field-6':'2097152'}},
17592186204561:{'kp':17592186204087,'near':[17592186530418,17592186204567],
 'values':{'field-1':'2','field-2':'-1'},'positions':{'field-1':'gradient[1]','field-2':'gradient[2]'},
 'solution':grad_solution,
 'template':'Differentiate with respect to each component of w while holding x fixed; assemble the derivatives as a column; substitute the given x. Canonical uses cubed inputs; the matching nearby two- and three-component linear-weighted sums use the target structure exactly.',
 'parameters':{'function':'w1*x1+w2*x2','differentiate_with_respect_to':['w1','w2'],'input':[2,-1],'gradient':['x1','x2'],'evaluated_gradient':[2,-1]},
 'derivation':['partial f/partial w1=x1; partial f/partial w2=x2','Substitute x1=2 and x2=-1 to obtain the column [2,-1]^T'],
 'incorrect':{'field-1':'1','field-2':'1'}}}

proposals=[];creations=[];evidence=[];grading=[]
for qid,target in TARGETS.items():
    q=QUESTIONS[qid];kp=PARENTS[target['kp']]
    canonical=kp[':knowledge-point/canonical-example']
    assert canonical.get(':question/worked-solution')
    assert all(question_in(target['kp'],n).get(':question/worked-solution') for n in target['near'])
    solution=normalize_prose(target['solution']);validate_prose(solution)
    if q.get(':question/worked-solution'):
        # Preserve any pre-existing valid explanation rather than overwrite it.
        solution=q[':question/worked-solution']
    else:
        proposals.append({'entity':qid,'attribute':'question/worked-solution','before':q.get(':question/worked-solution'),
                          'after':solution,'provenance':'locally authored completion inferred from the canonical and nearby method, independently solved; not an observed Math Academy answer'})
    fields={f[':answer-field/key']:f for f in q[':question/answer-fields']}
    assert set(fields)==set(target['values'])
    mappings=[]
    for key,value in target['values'].items():
        field=fields[key];fid=field[':db/id'];validate_tex(value)
        assert field[':answer-field/type'][':db/ident']==':answer-field.type/blank'
        assert not field.get(':answer-field/correct') and not field.get(':answer-field/choices')
        answer_uuid=str(uuid.uuid5(NS,f'{fid}:{value}'))
        tempid=f'matrix-completion-answer-{fid}'
        creations.append({'field_entity':fid,'field_key':key,'question_entity':qid,
                          'answer_type':':answer.type/math','answer_value':value,'answer_uuid':answer_uuid,'answer_tempid':tempid,
                          'correct_before':None,'choices_before':[],
                          'provenance':'locally authored canonical answer; independently derived from existing prompt'})
        mappings.append({'field_entity':fid,'field_key':key,'position':target['positions'][key],'answer_value':value,
                         'answer_tempid':tempid,'existing_answer_bank':[],'existing_correct':None,
                         'unique_value_established':True,'existing_answer_id_available':False})
        grading.append({'question_entity':qid,'field_entity':fid,'field_key':key,'correct_input':value,
                        'incorrect_input':target['incorrect'][key],
                        'equivalent_input': '1/16' if value==r'\frac{1}{16}' else ('2*ln(t)' if value==r'2\ln(t)' else value)})
    evidence.append({'question_entity':qid,'question_uuid':q[':question/id'],'imported_id':q[':question/math-academy-id'],
                     'basis':14371,'status':'prepared; root must preview, render, grade and commit',
                     'knowledge_point_entity':target['kp'],'knowledge_point_title':kp[':knowledge-point/title'],
                     'canonical':canonical,'nearby_templates':[question_in(target['kp'],n) for n in target['near']],
                     'template':target['template'],'target_parameters':target['parameters'],
                     'independent_derivation':target['derivation'],'answer_field_mapping':mappings,
                     'authorship':'locally authored completion; source supplied teaching template only',
                     'solution_previously_present':bool(q.get(':question/worked-solution')),
                     'validation':{'exact_symbolic_calculation':True,'validate_prose':True,'validate_tex_answers':True,
                                   'application_grader':'pending root read-only preview','database_mutation':False}})

qid=17592186157699
before=LAYOUT[qid]['after']
old='$2^{D/2} =$';new='$2^{D/3} =$'
assert before.count(old)==1
corrected=before.replace(old,new)
validate_prose(corrected)
correction=[{'entity':qid,'attribute':'question/problem','before':before,'after':corrected,
             'apply_after':'root layout proposal',
             'replacement':{'before':old,'after':new},
             'reason':'Correct upstream answer-label typo to D/3, matching the explicit requested function and diagonal values divisible by 3. Exact source screenshot exhibits the same typo; no imported numerical entries or controls change.',
             'source_screenshot':'/home/jake/Developer/MA/DATA/Lessons/2927/Source/Sections/05-question-253242.png',
             'source_screenshot_sha256':hashlib.sha256(Path('/home/jake/Developer/MA/DATA/Lessons/2927/Source/Sections/05-question-253242.png').read_bytes()).hexdigest()}]
evidence[1]['upstream_source_typo']=correction[0]
for filename,data in [('completion-proposals.json',proposals),('answer-creations.json',creations),
                      ('completion-evidence.json',evidence),('prompt-correction-proposals.json',correction),
                      ('completion-grading-cases.json',grading)]:
    (HERE/filename).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'questions':len(TARGETS),'solutions':len(proposals),'new_field_owned_canonical_answers':len(creations),
                  'prompt_typo_corrections':len(correction),'application_grading':'delegated to root','database_writes':0},indent=2))
