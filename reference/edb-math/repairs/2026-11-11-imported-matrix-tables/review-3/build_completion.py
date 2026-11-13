#!/usr/bin/env python3
"""Exact, read-only q-completion preparation for five matrix exponents.

Missing field-owned answers are authored under explicit completion scope.
Duplicate empty field links are removed only from their owning question;
entities and retained history are preserved.
"""
from pathlib import Path
import json
import sys
import uuid
import sympy as s
from bs4 import BeautifulSoup

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p/'scripts/question_capture/math_format.py').exists())
sys.path.insert(0,str(ROOT))
from scripts.question_capture.math_format import matrix_tex

parents = json.loads((HERE.parent/'completion-context/parents.json').read_text())
questions = {q[':db/id']:q for kp in parents for q in kp.get(':knowledge-point/questions',[])}
owners = {q[':db/id']:kp for kp in parents for q in kp.get(':knowledge-point/questions',[])}
layouts={p['entity']:p['after'] for p in json.loads((HERE/'proposals.json').read_text())}
t=s.symbols('t',real=True)

def display(tex): return '\n\n$$\n'+tex+'\n$$\n\n'
def aligned(*rows): return r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}'
def matrix(A): return matrix_tex([[s.latex(v) for v in row] for row in A.tolist()])

targets = [
    {'id':17592186221932,'A':s.Matrix([[3,-4],[2,-1]]),'kind':'complex','a':1,'b':2,
     'inner':s.Matrix([[s.cos(2*t)+s.sin(2*t),-2*s.sin(2*t)],[s.sin(2*t),s.cos(2*t)-s.sin(2*t)]]),
     'factor':s.exp(t),'fields':{'field-1':((0,1),r'-2\sin(2t)'),'field-2':((1,1),r'\cos(2t)-\sin(2t)')}},
    {'id':17592186221933,'A':s.Matrix([[1,2],[-2,5]]),'kind':'repeated','a':3,
     'inner':s.Matrix([[1-2*t,2*t],[-2*t,1+2*t]]),'factor':s.exp(3*t),
     'fields':{'field-1':((0,0),'1-2t'),'field-2':((1,0),'-2t')}},
    {'id':17592186221994,'A':s.Matrix([[0,6],[1,-1]]),'kind':'real','u':-3,'v':2,
     'inner':s.Matrix([[3*s.exp(2*t)+2*s.exp(-3*t),6*s.exp(2*t)-6*s.exp(-3*t)],
                       [s.exp(2*t)-s.exp(-3*t),2*s.exp(2*t)+3*s.exp(-3*t)]]),'factor':s.Rational(1,5),
     'fields':{'field-1':((0,0),r'3e^{2t}+2e^{-3t}'),'field-2':((1,0),r'e^{2t}-e^{-3t}')}},
    {'id':17592186222002,'A':s.Matrix([[1,1],[-2,-1]]),'kind':'complex','a':0,'b':1,
     'inner':s.Matrix([[s.cos(t)+s.sin(t),s.sin(t)],[-2*s.sin(t),s.cos(t)-s.sin(t)]]),'factor':s.Integer(1),
     'fields':{'field-1':((0,0),r'\cos(t)+\sin(t)'),'field-2':((1,0),r'-2\sin(t)')}},
    {'id':17592186222003,'A':s.Matrix([[3,1],[-1,1]]),'kind':'repeated','a':2,
     'inner':s.Matrix([[1+t,t],[-t,1-t]]),'factor':s.exp(2*t),
     'fields':{'field-1':((0,0),'1+t'),'field-2':((0,1),'t')}},
]

def solution(x):
    A=x['A']
    alpha1,alpha0=s.symbols('alpha_1 alpha_0')
    # Follow the canonical sequence: degree-one remainder for At; interpolate
    # at scaled eigenvalues (and its derivative for a repeated eigenvalue),
    # solve its coefficients, then substitute into the requested entries.
    expansion=matrix(A*t*alpha1+s.eye(2)*alpha0)
    text='We have a square matrix of dimension $n=2.$ Thus,'
    text+=display(aligned(r'e^{At} &= \alpha_1At+\alpha_0I',
                        r'&=\alpha_1'+matrix(A)+r't+\alpha_0'+matrix(s.eye(2)),
                        '&='+expansion))
    text+=r'where $\alpha_1$ and $\alpha_0$ are functions to be determined.'+'\n\n'
    text+=r'Consider the polynomial $r(\lambda)=\alpha_1\lambda+\alpha_0.$ '
    if x['kind']=='complex':
        a,b=x['a'],x['b']
        l=(a+s.I*b)*t
        c1=s.exp(a*t)*s.sin(b*t)/(b*t)
        c0=s.exp(a*t)*(s.cos(b*t)-s.Rational(a,b)*s.sin(b*t))
        assert s.simplify((a+s.I*b)*t*c1+c0-s.exp(a*t)*(s.cos(b*t)+s.I*s.sin(b*t)))==0
        assert s.simplify((a-s.I*b)*t*c1+c0-s.exp(a*t)*(s.cos(b*t)-s.I*s.sin(b*t)))==0
        text+='The eigenvalues of $At$ are '+ '$'+s.latex(l)+'$ and $'+s.latex(s.conjugate(l))+'$, which are complex conjugates. Thus, we have the following:'
        text+=display(aligned(r'r('+s.latex(l)+r')&=e^{'+s.latex(l)+'}',
                            s.latex(l)+r'\alpha_1+\alpha_0&='+s.latex(s.exp(a*t))+r'\bigl('+s.latex(s.cos(b*t))+r'+\mathrm{i}'+s.latex(s.sin(b*t))+r'\bigr)'))
        text+=r'Now, we equate the real and imaginary parts, and solve for $\alpha_1$ and $\alpha_0$:'
        text+=display(aligned(s.latex(a*t*alpha1+alpha0)+'&='+s.latex(s.exp(a*t)*s.cos(b*t)),
                            s.latex(b*t*alpha1)+'&='+s.latex(s.exp(a*t)*s.sin(b*t)),
                            r'\alpha_1&='+s.latex(c1),r'\alpha_0&='+s.latex(c0)))
    elif x['kind']=='repeated':
        a=x['a']; c1=s.exp(a*t);c0=s.exp(a*t)*(1-a*t)
        assert s.simplify(a*t*c1+c0-s.exp(a*t))==0
        assert c1==s.exp(a*t) # derivative interpolation rprime(at)=exp(at)
        text+='The only eigenvalue of $At$ is $'+s.latex(a*t)+'$, of multiplicity two. Thus, we have the following:'
        text+=display(aligned(r'r('+s.latex(a*t)+r')&=e^{'+s.latex(a*t)+'}',
                            r'r\,^{\prime}('+s.latex(a*t)+r')&=e^{'+s.latex(a*t)+'}',
                            s.latex(a*t*alpha1+alpha0)+'&='+s.latex(c1),r'\alpha_1&='+s.latex(c1)))
        text+=r'Now, we solve the system for $\alpha_1$ and $\alpha_0$:'+'\n\n'
        text+='- From the second equation, we get'
        text+=display(r'\alpha_1='+s.latex(c1)+'.')
        text+='- Substituting this into the first one, we get'
        text+=display(s.latex(a*t*c1)+r'+\alpha_0='+s.latex(c1)+r'\quad\Rightarrow\quad\alpha_0='+s.latex(c0)+'.')
    else:
        u,v=x['u'],x['v'];c1=(s.exp(v*t)-s.exp(u*t))/((v-u)*t);c0=(v*s.exp(u*t)-u*s.exp(v*t))/(v-u)
        assert s.simplify(u*t*c1+c0-s.exp(u*t))==0
        assert s.simplify(v*t*c1+c0-s.exp(v*t))==0
        text+='The eigenvalues of $At$ are $'+s.latex(u*t)+'$ and $'+s.latex(v*t)+'$, both of multiplicity one. Thus, we have the following:'
        text+=display(aligned(r'r('+s.latex(u*t)+r')&=e^{'+s.latex(u*t)+'}',r'r('+s.latex(v*t)+r')&=e^{'+s.latex(v*t)+'}',
                            s.latex(u*t*alpha1+alpha0)+'&='+s.latex(s.exp(u*t)),s.latex(v*t*alpha1+alpha0)+'&='+s.latex(s.exp(v*t))))
        text+=r'Now, we solve the system for $\alpha_1$ and $\alpha_0$:'+'\n\n'
        text+='- Subtracting the first equation from the second one, we get'
        text+=display(s.latex((v-u)*t*alpha1)+'='+s.latex(s.exp(v*t)-s.exp(u*t))+r'\quad\Rightarrow\quad\alpha_1='+s.latex(c1)+'.')
        text+='- Multiplying the first equation by $2$ and the second by $3$, then adding, we get'
        text+=display(r'5\alpha_0='+s.latex(2*s.exp(u*t)+3*s.exp(v*t))+r'\quad\Rightarrow\quad\alpha_0='+s.latex(c0)+'.')
    result=(A*t*c1+s.eye(2)*c0).applyfunc(s.simplify)
    assert (result-x['factor']*x['inner']).applyfunc(s.simplify)==s.zeros(2)
    text+=r'Substituting $\alpha_1$ and $\alpha_0$ into the expressions for the required entries of $e^{At}$, we get the following:'
    lines=[]
    for key,(pos,answer) in x['fields'].items():
        i,j=pos
        intermediate=A[i,j]*t*c1+(c0 if i==j else 0)
        final=(s.latex(x['factor'])+r'\bigl('+answer+r'\bigr)' if x['factor']!=1 else answer)
        lines.append(s.latex((A*t*alpha1+s.eye(2)*alpha0)[i,j])+' &='+s.latex(intermediate))
        lines.append('&='+final)
    text+=display(aligned(*lines))
    text+='Therefore,'
    fac='' if x['factor']==1 else s.latex(x['factor'])
    text+=display('e^{At}='+fac+matrix(x['inner'])+'.')
    if x['kind']!='repeated':
        text+=r'The coefficient $\alpha_1$ at $t=0$ is understood by continuity; the final matrix formula holds for every real $t$.'+'\n'
    return text.strip()

proposals=[]
creations=[]
duplicate_retractions=[]
ANSWER_NAMESPACE=uuid.UUID('c4fa99ea-25d2-5c70-8b82-3130e074eadb')
evidence={'basis':14371,'authorship':'Locally authored exact mathematical completion; canonical solutions supply the method, not observed target answers.',
          'verification':'Exact SymPy E(0)=I and Eprime=A E checks. Application grader/rendering reserved to root; no learner data written.',
          'templates':[],'questions':[],'unresolved':[]}
for kpid in [17592186221408,17592186221409,17592186221410]:
    kp=next(k for k in parents if k[':db/id']==kpid)
    c=kp[':knowledge-point/canonical-example']
    nearby=[q for q in kp[':knowledge-point/questions'] if q.get(':question/worked-solution')]
    evidence['templates'].append({'knowledge_point':kpid,'title':kp[':knowledge-point/title'],
        'canonical':c, 'nearby_inspected':[{'entity':q[':db/id'],'problem':q[':question/problem'],'worked_solution':q[':question/worked-solution']} for q in nearby[:2]],
        'backbone':['Write e^(At)=alpha1 At+alpha0 I and expand all entries.',
                    'Interpolate r(lambda)=alpha1 lambda+alpha0 at eigenvalues of At; for a repeated eigenvalue include derivative interpolation.',
                    'Solve coefficients; complex conjugates use real/imaginary parts.',
                    'Substitute into required entries and extract supplied outer factor, then present whole matrix.'],
        'constraints':'Real2x2 matrices, known distinct real/complex conjugate or defective repeated eigenvalues; same field layout and externally supplied factor.'})

for x in targets:
    q=questions[x['id']];kp=owners[x['id']]
    E=x['factor']*x['inner'];A=x['A']
    assert E.subs(t,0)==s.eye(2)
    assert (E.diff(t)-A*E).applyfunc(s.simplify)==s.zeros(2)
    layout=BeautifulSoup(layouts[x['id']],'html.parser')
    matrix_table=layout.select_one('.matrix-answer-brackets table')
    layout_rows=[[td.get_text().strip() for td in tr.find_all('td')] for tr in matrix_table.find_all('tr')]
    assert len(layout_rows)==2 and all(len(row)==2 for row in layout_rows)
    for key,(pos,value) in x['fields'].items():
        assert layout_rows[pos[0]][pos[1]]=='{{'+key+'}}', ('field/grid ownership mismatch',x['id'],key)
    ev={'entity':x['id'],'source_id':q[':question/math-academy-id'],'knowledge_point':kp[':db/id'],
        'problem_before':q[':question/problem'],
        'repaired_layout_rows':layout_rows,
        'A':A.tolist(),'eigenvalues':{str(k):v for k,v in A.eigenvals().items()},'exact_exponential':s.latex(E),
        'factor':s.latex(x['factor']),'inner':s.latex(x['inner']),'fields':[],
        'checks':{'E(0)=I':True,'Eprime=A E':True,'all_field_positions_match_repaired_layout':True},
        'solution_preserved':bool(q.get(':question/worked-solution'))}
    for key,(pos,value) in x['fields'].items():
        for field in [f for f in q[':question/answer-fields'] if f[':answer-field/key']==key]:
            entry={'field':field[':db/id'],'key':key,'position_1_based':[pos[0]+1,pos[1]+1],
                   'expected_fragment':value,'exact_fragment':s.latex(x['inner'][pos[0],pos[1]]),
                   'existing_choices':field.get(':answer-field/choices',[]),'existing_correct':field.get(':answer-field/correct')}
            if field.get(':answer-field/correct'):
                entry['status']='existing keyed same-key field preserved'
            else:
                assert not field.get(':answer-field/choices'), 'Newly present choices require explicit equivalence review'
                populated=[f for f in q[':question/answer-fields'] if f[':answer-field/key']==key and f.get(':answer-field/correct')]
                if populated:
                    assert x['id']==17592186222003 and len(populated)==1
                    valid=populated[0]
                    assert valid[':answer-field/correct'][':answer/value']==value
                    duplicate_retractions.append({'question_entity':x['id'],'attribute':'question/answer-fields',
                        'field_entity':field[':db/id'],'field_key':key,
                        'retained_valid_field_entity':valid[':db/id'],
                        'retained_valid_correct_answer_entity':valid[':answer-field/correct'][':db/id'],
                        'retained_valid_answer_value':value,
                        'rationale':'Empty orphan field duplicates a populated same-key field of this question. Retract only this question-to-orphan-field reference; preserve orphan entity and history.'})
                    entry['status']='unlink empty duplicate field; preserve populated same-key field'
                else:
                    answer_uuid=str(uuid.uuid5(ANSWER_NAMESPACE,str(field[':db/id'])+':'+value))
                    creation={'field_entity':field[':db/id'],'key':key,'type':':answer.type/math','value':value,
                              'answer_uuid':answer_uuid,'answer_tempid':'matrix-completion-answer-'+str(field[':db/id'])}
                    creations.append(creation)
                    entry['status']='author missing field-owned math answer and link as choice/correct'
                    entry['answer_creation']=creation
            ev['fields'].append(entry)
    if not q.get(':question/worked-solution'):
        proposals.append({'entity':x['id'],'attribute':'question/worked-solution','before':None,'after':solution(x)})
        ev['checks']['interpolation_coefficients_verified']=True
    evidence['questions'].append(ev)

for name,data in [('completion-proposals',proposals),('completion-evidence',evidence),
                  ('answer-creations',creations),('duplicate-field-retractions',duplicate_retractions)]:
    def scan(value):
        if isinstance(value,str):
            assert not any(ord(c)<32 and c not in '\n\t\r' for c in value), ('C0 control',name,repr(value))
        elif isinstance(value,dict):
            for k,v in value.items(): scan(k);scan(v)
        elif isinstance(value,(list,tuple)):
            for v in value: scan(v)
    scan(data)
    (HERE/f'{name}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2,default=str)+'\n')
print(json.dumps({'solution_proposals':len(proposals),'answer_creations':len(creations),
                  'duplicate_field_unlinks':len(duplicate_retractions),'unresolved':len(evidence['unresolved'])}))
