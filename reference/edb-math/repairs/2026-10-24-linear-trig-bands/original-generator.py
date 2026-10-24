"""Source-bank-preserving positive coordinate dilations for linear trig integrals.

Finite policy: k in 1..12. Argument x becomes k*x, bounds become bounds/k,
and every antiderivative/value becomes its transported value divided by k.
This is a documented narrow transport policy, not an inferred misconception.
"""
import argparse
import hashlib
import json
from pathlib import Path
import random
import uuid
import os
import sys
try:
    import sympy as sp
except ImportError:
    runtime=Path(__file__).resolve().parents[2]/'.venv/bin/python'
    if __name__=='__main__' and runtime.exists():os.execv(str(runtime),[str(runtime),__file__,*sys.argv[1:]])
    raise

KP_ID = 17592186068915
KP_UUID = '746d1bc6-98ec-59a1-bec6-9dcfb7081a5d'
GENERATOR_UUID = '513f5406-21a7-5dd9-ab2a-147029c58468'
VERSION = 'linear-trig-dilation-1'
HERE = Path(__file__).with_suffix('')
x = sp.Symbol('x', real=True)
pi = sp.pi
R = sp.Rational
# level, function, amplitude, slope, shift, lower, upper, complete base bank
DATA = {
 'q-10061': ('easy','sin',1,2,0,None,None,
              [R(1,2)*sp.cos(2*x),-2*sp.cos(2*x),2*sp.cos(2*x),-R(1,2)*sp.sin(2*x),-R(1,2)*sp.cos(2*x)]),
 'q-2204': ('easy','sin',1,5,0,None,None,
             [sp.cos(5*x),-R(1,5)*sp.cos(5*x),R(1,5)*sp.cos(5*x),-R(1,5)*sp.cos(x),5*sp.cos(5*x)]),
 'q-10064': ('easy','cos',1,-9,3,None,None,
              [-R(1,3)*sp.sin(3-9*x),-R(1,9)*sp.sin(3-9*x),R(1,9)*sp.cos(3-9*x),R(1,9)*sp.sin(3-9*x),-R(1,9)*sp.cos(3-9*x)]),
 'q-350040': ('easy','sin',9,2,0,0,pi/4,[R(9,2)]),
 'q-13647': ('moderate','sin',5,4,0,0,pi/8,[0,R(5,4),-R(5,4),1,-1]),
 'q-346081': ('moderate','cos',1,pi/4,0,0,2,[4/pi]),
 'q-10574': ('moderate','sin',1,3,pi/3,0,pi/9,[R(1,2),R(1,3),R(2,3),R(1,6),R(3,2)])
}

def sources():
    return {q[':question/math-academy-id']:q for q in json.loads((HERE/'source.json').read_text())['kp'][':knowledge-point/questions']}

def math_data(template,k):
    level,fn,A,b,c,lo,hi,bank=DATA[template]
    trig=getattr(sp,fn);b=sp.sympify(b)*k;c=sp.sympify(c);A=sp.sympify(A)
    integrand=A*trig(b*x+c)
    primitive=(-A/b*sp.cos(b*x+c)) if fn=='sin' else A/b*sp.sin(b*x+c)
    lo=None if lo is None else sp.sympify(lo)/k
    hi=None if hi is None else sp.sympify(hi)/k
    correct=primitive if lo is None else sp.simplify(primitive.subs(x,hi)-primitive.subs(x,lo))
    choices=[sp.sympify(v).subs(x,k*x)/k for v in bank]
    return level,fn,A,b,c,lo,hi,integrand,primitive,correct,choices

def mathematical_key(template,k):
    *_,lo,hi,integrand,primitive,correct,bank=math_data(template,k)
    return hashlib.sha256(json.dumps([sp.srepr(sp.expand_trig(integrand)),None if lo is None else sp.srepr(lo),None if hi is None else sp.srepr(hi)],separators=(',',':')).encode()).hexdigest()

def fingerprint(q):
    # Parse actual printed prompts, independent of generation metadata. Variable
    # renaming, identities, choices, solution prose and seed do not imply novelty.
    sys.path.insert(0,str(HERE))
    from printed import integral
    value,lo,hi=integral(q[':question/problem'])
    return hashlib.sha256(json.dumps([sp.srepr(sp.expand_trig(value)),None if lo is None else sp.srepr(lo),None if hi is None else sp.srepr(hi)],separators=(',',':')).encode()).hexdigest()

def generate(level,seed,template,parameters):
    k=parameters['k']
    if type(k) is not int or not 1<=k<=12 or template not in DATA or level!=DATA[template][0]:raise ValueError('Unsupported band/template/parameter')
    old=sources()[template];of=old[':question/answer-fields'][0]
    level,fn,A,b,c,lo,hi,integrand,primitive,correct,bank=math_data(template,k)
    var=sp.Symbol('z') if template=='q-2204' else x
    def latex(v):return sp.latex(sp.sympify(v).subs(x,var))
    indefinite=lo is None
    correct_indices=[i for i,v in enumerate(bank) if sp.simplify(v-correct)==0]
    assert len(correct_indices)==1
    correct_index=correct_indices[0]
    integral=(r'\int '+latex(integrand)+r'\,\text{d}'+str(var)) if indefinite else (r'{\int }_{'+latex(lo)+r'}^{'+latex(hi)+'}'+latex(integrand)+r'\,\text{d}x')
    if k==1:
        prompt=old[':question/problem']
        values=[a[':answer/value'] for a in of[':answer-field/choices']]
    else:
        integral=(r'\int '+latex(integrand)+r'\,\text{d}'+str(var)) if indefinite else (r'{\int }_{'+latex(lo)+r'}^{'+latex(hi)+'}'+latex(integrand)+r'\,\text{d}x')
        if template=='q-2204':prompt='Calculate $\\displaystyle '+integral+'$.'
        elif template in ('q-10061','q-10064','q-10574'):prompt='Calculate $'+integral+'.$'
        elif template=='q-13647':prompt='$'+integral+'=$'
        else:prompt='Evaluate the following integral. Do not round the answer.\n\n$'+integral+'=$\n'+('\n' if template=='q-350040' else '')+'{{field-1}}'
        values=[latex(v)+('+C' if indefinite else '') for v in bank]
    # Every value uses the same instance; one fixed worked solution. Exact source
    # solution retained at original parameters, except the incomplete legacy source.
    u=sp.Symbol('u',real=True);arg=b*x+c;ulo=None if lo is None else sp.simplify(b*lo+c);uhi=None if hi is None else sp.simplify(b*hi+c)
    up=(-A/b*sp.cos(u)) if fn=='sin' else A/b*sp.sin(u)
    sol='If we let $u='+latex(arg)+',$ then\n\n$$\n'+r'\frac{\text{d}u}{\text{d}'+str(var)+'}='+latex(b)+r'\,\Longrightarrow\,\text{d}'+str(var)+'='+latex(1/b)+r'\,\text{d}u.'+'\n$$\n\n'
    if not indefinite:
        sol+='Calculating the limits for $u$ gives\n\n| $x$ | $'+latex(lo)+'$ | $'+latex(hi)+'$ |\n| --- | --- | --- |\n| $u$ | $'+latex(ulo)+'$ | $'+latex(uhi)+'$ |\n\n'
    sol+='Using the above, we can '+('rewrite' if template=='q-346081' else 'write')+' the integral in terms of $u$ and evaluate:\n\n$$\n'
    if indefinite:
        sol+=r'\begin{aligned}\int '+latex(integrand)+r'\,\text{d}'+str(var)+' &= '+latex(A)+r'\int '+'\\'+fn+r'(u)\cdot '+latex(1/b)+r'\,\text{d}u \\ &= '+latex(A/b)+'\\int \\'+fn+r'(u)\,\text{d}u \\ &= '+latex(up)+r'+C \\ &= '+latex(correct)+r'+C\end{aligned}'
    else:
        limits=r'_{'+latex(ulo)+r'}^{'+latex(uhi)+'}'
        sol+=r'\begin{aligned}'+integral+r' &= {\int }'+limits+latex(A)+'\\'+fn+r'(u)\cdot '+latex(1/b)+r'\,\text{d}u \\ &= '+latex(A/b)+r'{\int }'+limits+'\\'+fn+r'(u)\,\text{d}u \\ &= '+latex(up)+r'\big|'+limits+r' \\ &= '+latex(up.subs(u,uhi))+'-('+latex(up.subs(u,ulo))+r') \\ &= '+latex(correct)+r'\end{aligned}'
    sol+='\n$$'
    if k==1 and old.get(':question/worked-solution'):sol=old[':question/worked-solution']
    fp=mathematical_key(template,k)
    uid=lambda text:str(uuid.uuid5(uuid.UUID(GENERATOR_UUID),text))
    qid=uid('question:'+fp+':profile:'+template)
    fid=uid(qid+':field:'+of[':answer-field/key'])
    answers=[{':answer/id':uid(fid+':answer:'+str(i)),':answer/type':':answer.type/math',':answer/value':value} for i,value in enumerate(values)]
    question={':question/id':qid,':question/problem':prompt,':question/worked-solution':sol,':question/difficulty':':question.difficulty/'+level,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':of[':answer-field/key'],':answer-field/type':of[':answer-field/type'][':db/ident'],':answer-field/choices':answers,':answer-field/correct':[':answer/id',answers[correct_index][':answer/id']]}]}
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':'Integrating Trigonometric Functions With Linear Arguments'},'question':question,'generation':{'version':VERSION,'generator_id':GENERATOR_UUID,'seed':seed,'template':template,'profile':template,'parameters':{'k':k},'domain':'real variable; slope nonzero; positive integer coordinate dilation','source_basis':json.loads((HERE/'source.json').read_text())['basis'],'source_question':template,'mathematical_fingerprint':fp,'dependencies':{'sympy':sp.__version__},'recipe_policy':'Complete source bank transported by x -> k*x, bounds -> bounds/k, values -> values/k. Integration constant remains arbitrary C.'}}

def candidates(level):
    seen=set()
    for t in DATA:
        if DATA[t][0]!=level:continue
        for k in range(2,13):
            key=mathematical_key(t,k)
            if key not in seen:seen.add(key);yield t,{'k':k}

def batch(level,count,seed):
    if level not in ('easy','moderate') or type(count) is not int or count<1:raise ValueError('Unsupported level/count')
    choices=list(candidates(level));random.Random(seed).shuffle(choices)
    if count>len(choices):raise ValueError('Finite variant limit: '+str(len(choices)))
    return [generate(level,seed,t,p) for t,p in choices[:count]]

def markdown(rec):
    q=rec['question'];f=q[':question/answer-fields'][0]
    return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$'+(' (correct)' if a[':answer/id']==f[':answer-field/correct'][1] else '') for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--difficulty',required=True);parser.add_argument('--count',type=int,default=5);parser.add_argument('--seed',type=int,default=0);parser.add_argument('--format',choices=['json','markdown'],default='json');a=parser.parse_args()
    records=batch(a.difficulty,a.count,a.seed)
    print(json.dumps(records,indent=2) if a.format=='json' else '\n\n'.join(markdown(r) for r in records))
