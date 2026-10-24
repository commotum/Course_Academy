"""Exact positive amplitude transports of source differentiation tasks.

Finite policy k=1..12; k=1 is replay, k=2..12 is stock. Complete choice
banks scale together. This preserves observed banks without guessing errors.
"""

# Standalone source eligibility: immutable policy ledger, seeded CLI guard.
import sys as _ca_sys, os as _ca_os
from pathlib import Path as _ca_Path
_ca_sys.path.insert(0,str(_ca_Path(__file__).resolve().parent))
if __name__ == "__main__" and not _ca_os.environ.get("_CA_SOURCE_POLICY_CHILD"):
    from ca_source_runtime import cli as _ca_source_cli
    _ca_source_cli(__file__,_ca_Path(__file__).with_name('17592186059675-source-policy.json'))
    raise SystemExit(0)

import argparse, hashlib, json, random, sys, uuid, os
from pathlib import Path
try: import sympy as sp
except ImportError:
    runtime=Path(__file__).resolve().parents[2]/'.venv/bin/python'
    if __name__=='__main__':os.execv(str(runtime),[str(runtime),__file__,*sys.argv[1:]])
    raise
HERE=Path(__file__).with_suffix('');sys.path.insert(0,str(HERE));import printed as p
KP_ID=17592186059675
KP_UUID='0de0627b-2568-5c02-8928-d14344df5a2f'
GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),'question-generator'))
VERSION='trig-derivative-amplitude-1'
x=p.x
DATA={'q-1847':('easy',4*sp.cos(x)+2*sp.sin(x),None),
'q-1900':('moderate',2*x-5*sp.cos(x),sp.pi/6),
'q-30991':('easy',6*(x**2-sp.cos(x))+5,None),
'q-341383':('easy',sp.Rational(5,4)*sp.sin(x)+x**4/4,None),
'q-47985':('easy',-2*sp.cos(x)+x**-2,None)}
def sources():return {q[':question/math-academy-id']:q for q in json.loads((HERE/'source.json').read_text())['kp'][':knowledge-point/questions']}
def printed_task(q):
    text=q[':question/problem']
    if 'curve $y=' in text:
        body=text.split('curve $y=',1)[1].split('$',1)[0]
        point=text.split('point $x=',1)[1].split('$',1)[0].rstrip('?')
        return p.scalar(body),p.scalar(point)
    if '$y=' in text:body=text.split('$y=',1)[1].split('$',1)[0]
    elif '(4cos' in text:body='4cosx+2sinx'
    elif r'\frac{\text{d}}{\text{d}x}(' in text:body=text.split(r'\frac{\text{d}}{\text{d}x}(',1)[1].split(')=$',1)[0]
    else:raise ValueError('Incomplete/unrecognized prompt')
    return p.scalar(body),None
def fingerprint(q):
    expr,point=printed_task(q)
    # Additive constants cannot create novelty in differentiation tasks.
    derivative=sp.expand(sp.diff(expr,x))
    return hashlib.sha256(json.dumps([sp.srepr(derivative),None if point is None else sp.srepr(point)]).encode()).hexdigest()
def generate(level,seed,template,parameters):
    k=parameters['k']
    if template not in DATA or level!=DATA[template][0] or type(k)is not int or not 1<=k<=12:raise ValueError('Unsupported level/template/parameter')
    old=sources()[template];of=old[':question/answer-fields'][0]
    _,base,point=DATA[template];expr=k*base;derivative=sp.diff(expr,x);correct=derivative if point is None else sp.simplify(derivative.subs(x,point))
    bank=[sp.simplify(k*p.scalar(a[':answer/value'])) for a in of[':answer-field/choices']]
    chosen=[i for i,a in enumerate(bank) if sp.simplify(a-correct)==0];assert len(chosen)==1
    for i,a in enumerate(bank):assert all(sp.simplify(a-b)!=0 for b in bank[:i])
    latex=sp.latex
    if k==1:prompt=old[':question/problem'];values=[a[':answer/value'] for a in of[':answer-field/choices']]
    else:
        if point is not None:prompt='What is the slope of the tangent line to the curve $y='+latex(expr)+'$ at the point $x='+latex(point)+'$?'
        elif template=='q-1847':prompt=r'$\frac{\text{d}}{\text{d}x}('+latex(expr)+')=$'
        else:prompt='Find the derivative of $y='+latex(expr)+'.$'+('\n\n'+r'$\frac{\text{d}y}{\text{d}x}=$'+'\n{{field-1}}' if of[':answer-field/type'][':db/ident'].endswith('/blank') else '')
        values=[latex(v) for v in bank]
    if k==1:
        solution=old[':question/worked-solution']
        # Preserve source evidence separately; fix its degree/radian label typo locally.
        if template=='q-1900':solution=solution.replace('{f}^{′}(30)',r'{f}^{′}(\frac{\pi }{6})')
    else:
        parts=sp.Add.make_args(sp.expand(expr))
        intermediate='+'.join('('+latex(sp.diff(term,x))+')' for term in parts)
        solution='We know that $'+r'\frac{\text{d}}{\text{d}x}(\sin x)=\cos x'+',$ and that $'+r'\frac{\text{d}}{\text{d}x}(\cos x)=-\sin x'+'.$ Applying these formulas and the sum and constant multiple rules, we have\n\n$$\n'+r'\begin{aligned}\frac{\text{d}y}{\text{d}x} &= \frac{\text{d}}{\text{d}x}('+latex(expr)+r') \\ &= '+intermediate+r' \\ &= '+latex(derivative)+r'.\end{aligned}'+'\n$$'
        if point is not None:
            solution='The slope is the derivative evaluated at $x='+latex(point)+'.$\n\n'+solution+'\n\nEvaluating at $x='+latex(point)+',$ we get\n\n$$\n'+r'y^{\prime}('+latex(point)+')='+latex(2*k)+'+'+latex(5*k)+r'\sin('+latex(point)+')='+latex(2*k)+'+'+latex(5*k)+r'\left(\frac{1}{2}\right)'+'='+latex(correct)+'.\n$$\n\nTherefore, the slope is $'+latex(correct)+'.$'
    fp=fingerprint({':question/problem':prompt});uid=lambda text:str(uuid.uuid5(uuid.UUID(GENERATOR_UUID),text))
    qid=uid('question:'+fp+':profile:'+template);fid=uid(qid+':field:'+of[':answer-field/key'])
    answers=[{':answer/id':uid(fid+':answer:'+str(i)),':answer/type':':answer.type/math',':answer/value':v} for i,v in enumerate(values)]
    question={':question/id':qid,':question/problem':prompt,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+level,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':of[':answer-field/key'],':answer-field/type':of[':answer-field/type'][':db/ident'],':answer-field/choices':answers,':answer-field/correct':[':answer/id',answers[chosen[0]][':answer/id']]}]}
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':json.loads((HERE/'source.json').read_text())['kp'][':knowledge-point/title']},'question':question,'generation':{'version':VERSION,'generator_id':GENERATOR_UUID,'seed':seed,'template':template,'profile':template,'parameters':{'k':k},'domain':'real x; x != 0 for q-47985','source_basis':1963,'source_question':template,'mathematical_fingerprint':fp,'dependencies':{'sympy':sp.__version__},'recipe_policy':'Scale complete observed function and answer bank by positive integer k; no inferred misconception recipes.'}}
def candidates(level):
    for t in DATA:
        if DATA[t][0]==level:
            for k in range(2,13):yield t,{'k':k}
def batch(level,count,seed):
    if level not in ('easy','moderate') or type(count)is not int or count<1:raise ValueError('Unsupported band/count')
    pool=list(candidates(level));random.Random(seed).shuffle(pool)
    if count>len(pool):raise ValueError('Finite variant limit '+str(len(pool)))
    return [generate(level,seed,t,p) for t,p in pool[:count]]
def markdown(rec):
    q=rec['question'];f=q[':question/answer-fields'][0]
    return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$'+(' (correct)' if a[':answer/id']==f[':answer-field/correct'][1] else '') for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']

from ca_source_runtime import install as _ca_source_install
_ca_source_install(globals(),_ca_Path(__file__).with_name('17592186059675-source-policy.json'))

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--difficulty',required=True);a.add_argument('--count',type=int,default=5);a.add_argument('--seed',type=int,default=0);a.add_argument('--format',choices=['json','markdown'],default='json');args=a.parse_args();records=batch(args.difficulty,args.count,args.seed);print(json.dumps(records,indent=2) if args.format=='json' else '\n\n'.join(markdown(r) for r in records))
