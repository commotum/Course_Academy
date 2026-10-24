"""Definite rational integrals: bounded transport of each complete source bank.

Multiply numerator and every source-bank value by m=2..6, retaining poles,
bounds, factorization workload, source difficulty and field contract. m=1 is
source replay. No seed, identity or order change establishes distinct content.
"""

# Standalone source eligibility: immutable policy ledger, seeded CLI guard.
import sys as _ca_sys, os as _ca_os
from pathlib import Path as _ca_Path
_ca_sys.path.insert(0,str(_ca_Path(__file__).resolve().parent))
if __name__ == "__main__" and not _ca_os.environ.get("_CA_SOURCE_POLICY_CHILD"):
    from ca_source_runtime import cli as _ca_source_cli
    _ca_source_cli(__file__,_ca_Path(__file__).with_name('17592186068923-source-policy.json'))
    raise SystemExit(0)

import argparse,hashlib,json,os,random,sys,uuid
from functools import lru_cache
from pathlib import Path
try:import sympy as sp
except ImportError:
    if __name__=='__main__':
        runtime=Path(__file__).resolve().parents[2]/'.venv/bin/python';os.execv(str(runtime),[str(runtime),__file__,*sys.argv[1:]])
    raise
KP_ID=17592186068923
KP_UUID='771dfcc1-f6c3-59ed-8961-3fe477b011b6'
GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),'question-generator'))
VERSION='definite-rational-amplitude-1'
HERE=Path(__file__).with_suffix('');sys.path.insert(0,str(HERE));import printed as p
x=p.x;R=sp.Rational
# Difficulty, numerator, ordered linear factors, lower/upper bounds, expanded denominator.
DATA={
'q-49761':('hard',3*x+4,x+4,x-4,2,3,True),
'q-49766':('moderate',2*x+2,x-3,x+5,4,7,False),
'q-128238':('moderate',x-2,x+3,x+1,-5,-4,False),
'q-347077':('moderate',2*x+2,x-2,x+4,3,6,False),
'q-348975':('hard',3*x+7,x-2,x-6,3,5,True),
'q-348976':('hard',5*x-1,x+5,x-1,-4,0,True),
'q-349040':('hard',36*x-10,4*x-3,3*x+2,0,R(1,2),True),
'q-349041':('hard',15*x-39,5*x+1,x-4,0,2,True),
'q-49762':('hard',2*x+6,x+2,x-2,-1,1,True),
'q-49764':('moderate',5*x+29,x+7,x+4,-6,-5,False),
'q-49765':('moderate',11*x+46,x+2,x+8,-7,-3,False),
'q-49769':('moderate',x+1,x,x+3,-2,-1,False),
'q-75825':('hard',3*x-6,x+2,x-4,-1,3,True),
'q-75828':('hard',sp.Integer(14),5*x+1,x+3,4,11,True)}
@lru_cache(None)
def source_package():return json.loads((HERE/'source.json').read_text())
@lru_cache(None)
def sources():return {q[':question/math-academy-id']:q for q in source_package()['kp'][':knowledge-point/questions']}
@lru_cache(None)
def math_data(t,m):
    level,N,g1,g2,lo,hi,expanded=DATA[t];lo=sp.sympify(lo);hi=sp.sympify(hi);N=m*N
    r1=sp.solve(g1,x)[0];r2=sp.solve(g2,x)[0]
    A=sp.simplify(N.subs(x,r1)/g2.subs(x,r1));B=sp.simplify(N.subs(x,r2)/g1.subs(x,r2))
    a=sp.simplify(A/sp.diff(g1,x));b=sp.simplify(B/sp.diff(g2,x))
    F=a*sp.log(sp.Abs(g1))+b*sp.log(sp.Abs(g2))
    answer=sp.expand_log(F.subs(x,hi)-F.subs(x,lo),force=True)
    return N,g1,g2,lo,hi,A,B,a,b,F,answer

def L(e):return sp.latex(e).replace(r'\log',r'\ln')
def frac(N,D):return r'\frac{'+L(N)+'}{'+D+'}'
def den(t):
    _,_,g1,g2,_,_,expanded=DATA[t]
    return L(sp.expand(g1*g2)) if expanded else '('+L(g1)+')('+L(g2)+')'
def integral(t,m,definite=True):
    N,g1,g2,lo,hi,*_=math_data(t,m)
    return r'{\int }'+('_{'+L(lo)+'}^{'+L(hi)+'}' if definite else '')+frac(N,den(t))+r'\,\text{d}x'
def logarithm(a,g):return L(a)+r'\ln|'+L(g)+'|'
def aligned(rows):return r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}'

def solution(t,m):
    old=sources()[t];N,g1,g2,lo,hi,A,B,a,b,F,answer=math_data(t,m)
    f=frac(N,den(t));partial=L(A/g1+B/g2);primitive=logarithm(a,g1)+('+' if b>=0 else '-')+logarithm(abs(b),g2)
    power=sp.ilcm(a.q,b.q);product=g1**(power*a)*g2**(power*b)
    combined=L(R(1,power))+r'\ln|'+L(product)+'|'
    first=aligned([f+r' &= '+frac(N,'('+L(g1)+')('+L(g2)+')')+r'=\frac{A}{'+L(g1)+r'}+\frac{B}{'+L(g2)+'}'])
    identity=L(N)+'=A('+L(g2)+')+B('+L(g1)+')'
    def plug(which):
        root=sp.solve(g1 if which=='A' else g2,x)[0];v=N.subs(x,root);div=(g2 if which=='A' else g1).subs(x,root);coef=A if which=='A' else B
        return aligned([L(v)+' &= '+L(div)+which,which+' &= '+L(coef)])
    integration=aligned([integral(t,m,False)+r' &= \int ('+partial+r')\,\text{d}x',r'&= '+primitive+'+C'])
    logs=aligned([primitive+'+C &= '+combined+'+C'])
    endpoints=aligned([integral(t,m)+r' &= ['+primitive+']_{'+L(lo)+'}^{'+L(hi)+'}',r'&= ('+L(F.subs(x,hi))+')-('+L(F.subs(x,lo))+')',r'&= '+L(answer)])
    if t=='q-49766':
        # Legacy record has no source solution; complete locally with the same
        # moderate factored-denominator sequence as the neighboring sources.
        texts=["We'll work out the indefinite integral first and then proceed with the definite integral.\n\nFirst, we convert the integrand into a sum of partial fractions:\n\n",'\n\nwhich gives\n\n','\n\nPlugging in $x=-5,$ we can eliminate $A$ and solve for $B:$\n\n','\n\nOn the other hand, plugging in $x=3,$ we can eliminate $B$ and solve for $A:$\n\n','\n\nTherefore,\n\n','\n\nNow, we integrate, and we get\n\n','\n\nWe can simplify the result using the laws of logarithms, as follows:\n\n','\n\nFinally, the definite integral is\n\n','']
        blocks=[first,identity,plug('B'),plug('A'),f+'='+partial,integration,logs,endpoints]
    else:
        parts=old[':question/worked-solution'].split('$$');texts=parts[::2]
        if t=='q-128238':blocks=[f+'='+partial,integration,logs,endpoints]
        else:
            # The two nonmonic factors in q-349040 reverse the elimination order.
            first_letter='A' if t=='q-349040' else 'B'
            blocks=[first,identity,plug(first_letter),plug('B' if first_letter=='A' else 'A'),f+'='+partial,integration,logs,endpoints]
            if DATA[t][-1]:blocks.insert(0,L(sp.expand(g1*g2))+'=('+L(g1)+')('+L(g2)+')')
        assert len(texts)==len(blocks)+1
    sol=''.join(texts[i]+'$$\n'+block+'\n$$' for i,block in enumerate(blocks))+texts[-1]
    if m==1 and old.get(':question/worked-solution'):
        sol=old[':question/worked-solution']
        if t=='q-49761':sol=sol.replace(r'2{\int }_{2}^{3}\frac{1}{x-4}',r'2\int \frac{1}{x-4}')
    return sol

def fingerprint(q):
    f,lo,hi=p.integral(q[':question/problem'])
    return hashlib.sha256(json.dumps([sp.srepr(sp.cancel(f)),sp.srepr(lo),sp.srepr(hi)]).encode()).hexdigest()

def generate(level,seed,template,parameters):
    t=template;m=parameters['m']
    if t not in DATA or DATA[t][0]!=level or type(m)is not int or not 1<=m<=6:raise ValueError('Unsupported difficulty/template/parameter')
    old=sources()[t];of=old[':question/answer-fields'][0];answer=math_data(t,m)[-1]
    bank=[p.scalar(a[':answer/value'])*m for a in of[':answer-field/choices']]
    indices=[i for i,a in enumerate(bank) if p.equivalent(a,answer)];assert len(indices)==1
    prompt=p.clean(old[':question/problem'])
    if m!=1:
        # Replace every displayed copy of the original definite integral only.
        original=p.clean(old[':question/problem']); start=original.index(r'\int');start=start-1 if original[start-1]=='{' else start
        stop=original.index(r'\text{d}x',start)+len(r'\text{d}x') if r'\text{d}x' in original else original.index('dx',start)+2
        prompt=original.replace(original[start:stop],integral(t,m))
    values=[p.clean(a[':answer/value']) for a in of[':answer-field/choices']] if m==1 else [L(sp.expand_log(a,force=True)) for a in bank]
    if m>1 and of[':answer-field/type'][':db/ident']==':answer-field.type/blank':values[indices[0]]=L(answer)
    fp=fingerprint({':question/problem':prompt});uid=lambda s:str(uuid.uuid5(uuid.UUID(GENERATOR_UUID),s))
    qid=uid('question:'+fp+':profile:'+t);fid=uid(qid+':field:'+of[':answer-field/key'])
    answers=[{':answer/id':uid(fid+':answer:'+str(i)),':answer/type':':answer.type/math',':answer/value':a} for i,a in enumerate(values)]
    q={':question/id':qid,':question/problem':prompt,':question/worked-solution':solution(t,m),':question/difficulty':':question.difficulty/'+level,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':of[':answer-field/key'],':answer-field/type':of[':answer-field/type'][':db/ident'],':answer-field/choices':answers,':answer-field/correct':[':answer/id',answers[indices[0]][':answer/id']]}]}
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':source_package()['kp'][':knowledge-point/title']},'question':q,'generation':{'version':VERSION,'generator_id':GENERATOR_UUID,'seed':seed,'template':t,'profile':t if len(bank)>1 else None,'parameters':{'m':m},'source_question':t,'source_basis':source_package()['basis'],'mathematical_fingerprint':fp,'domain':'Real connected interval between exact endpoints, excluding both denominator roots; absolute logarithms retained.','dependencies':{'sympy':sp.__version__},'recipe_policy':'Positive amplitude multiplies the numerator and every complete source-bank mathematical value; observed literal log bases preserved, no mixed banks or inferred misconception.'}}

def candidates(level):
    for t in DATA:
        if DATA[t][0]==level:
            for m in range(2,7):yield t,{'m':m}
def batch(level,count,seed):
    if level not in ('moderate','hard') or type(count)is not int or count<1:raise ValueError('Unsupported difficulty/count')
    c=list(candidates(level));random.Random(seed).shuffle(c)
    if count>len(c):raise ValueError('Finite variant limit: '+str(len(c)))
    return [generate(level,seed,t,params) for t,params in c[:count]]
def markdown(rec):
    q=rec['question'];f=q[':question/answer-fields'][0]
    return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$'+(' (correct)' if a[':answer/id']==f[':answer-field/correct'][1] else '') for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']

from ca_source_runtime import install as _ca_source_install
_ca_source_install(globals(),_ca_Path(__file__).with_name('17592186068923-source-policy.json'))

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--difficulty',required=True);a.add_argument('--count',type=int,default=5);a.add_argument('--seed',type=int,default=0);a.add_argument('--format',choices=['json','markdown'],default='json');args=a.parse_args();records=batch(args.difficulty,args.count,args.seed);print(json.dumps(records,indent=2) if args.format=='json' else '\n\n'.join(map(markdown,records)))
