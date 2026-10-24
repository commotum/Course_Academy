"""Bounded amplitude transport of complete source banks for trig substitution.

m=1 replays sources; m=2..12 changes the integrand and every answer by m.
Workload, inner substitutions, field contracts, and complete banks are preserved.
"""
import argparse,hashlib,json,os,random,sys,uuid
from pathlib import Path
try: import sympy as sp
except ImportError:
    if __name__=='__main__':
        runtime=Path(__file__).resolve().parents[2]/'.venv/bin/python'
        os.execv(str(runtime),[str(runtime),__file__,*sys.argv[1:]])
    raise
KP_ID=17592186068917
KP_UUID='d359337c-4ec2-5100-bdac-d0858619db3b'
GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),'question-generator'))
VERSION='trig-substitution-amplitude-1'
HERE=Path(__file__).with_suffix('')
sys.path.insert(0,str(HERE))
import printed as p
x=p.x;u=p.u;R=sp.Rational
# level, outer coefficient, inner expression, trig factor in u, primitive in u, lower, upper
DATA={
'q-13461':('moderate',1,x**2,sp.sin(u),-sp.cos(u),None,None),
'q-13474':('moderate',4,x**3,sp.sec(u)**2,sp.tan(u),None,None),
'q-13464':('moderate',1,x**2,sp.csc(u)**2,-sp.cot(u),None,None),
'q-13533':('hard',5,2*x**2,sp.cos(u),sp.sin(u),0,sp.sqrt(sp.pi/2)),
'q-13537':('hard',3,2*x**2,sp.sin(u),-sp.cos(u),0,sp.sqrt(sp.pi)),
'q-3038':('hard',1,1/x,sp.sec(u)**2,sp.tan(u),None,None),
'q-350202':('hard',8,4*x**2,sp.sec(u)*sp.tan(u),sp.sec(u),0,sp.sqrt(sp.pi/12)),
'q-350203':('hard',12,6*x**2,sp.cos(u),sp.sin(u),sp.sqrt(sp.pi/12),sp.sqrt(sp.pi/6))}
def sources():return {q[':question/math-academy-id']:q for q in json.loads((HERE/'source.json').read_text())['kp'][':knowledge-point/questions']}
def math_data(t,m):
    level,A,inner,h,H,lo,hi=DATA[t]
    outer=x**2 if t=='q-13474' else 1/x**2 if t=='q-3038' else x
    integrand=m*A*outer*h.subs(u,inner)
    factor=sp.simplify(m*A*outer/sp.diff(inner,x));assert x not in factor.free_symbols
    primitive=factor*H.subs(u,inner)
    correct=primitive if lo is None else sp.simplify(primitive.subs(x,hi)-primitive.subs(x,lo))
    return integrand,primitive,correct,factor,inner,h,H,lo,hi

def fingerprint(q):
    f,lo,hi=p.integral(q[':question/problem'])
    return hashlib.sha256(json.dumps([sp.srepr(sp.trigsimp(f)),None if lo is None else sp.srepr(lo),None if hi is None else sp.srepr(hi)]).encode()).hexdigest()

def generate(level,seed,template,parameters):
    m=parameters['m'];t=template
    if t not in DATA or DATA[t][0]!=level or type(m) is not int or not 1<=m<=12:raise ValueError('Unsupported difficulty/template/parameter')
    old=sources()[t];of=old[':question/answer-fields'][0]
    integrand,F,correct,factor,inner,h,H,lo,hi=math_data(t,m)
    bank=[p.scalar(a[':answer/value']).subs(p.C,0)*m for a in of[':answer-field/choices']]
    indefinite=lo is None
    indices=[i for i,a in enumerate(bank) if sp.trigsimp(a-correct)==0];assert len(indices)==1
    L=sp.latex
    integral=r'\int '+L(integrand)+r'\,\text{d}x' if indefinite else r'{\int }_{'+L(lo)+r'}^{'+L(hi)+'}'+L(integrand)+r'\,\text{d}x'
    if m==1:prompt=old[':question/problem'];values=[a[':answer/value'] for a in of[':answer-field/choices']]
    else:
        if t in ('q-13474','q-13533'):prompt='$'+integral+'=$'
        elif t=='q-13537':prompt='Evaluate the integral $'+integral+'.$'
        elif t=='q-3038':prompt='Calculate the integral $'+integral+'.$'
        elif t in ('q-350202','q-350203'):prompt='Evaluate the following integral. Do not round the answer.\n\n$'+integral+'=$\n{{field-1}}'
        else:prompt='Calculate $'+integral+'.$'
        values=[L(a)+('+C' if indefinite else '') for a in bank]
    sol=('If we let' if t in ('q-350202','q-350203') else 'Let')+' $u='+L(inner)+',$ then\n\n$$\n'+r'\frac{\text{d}u}{\text{d}x}='+L(sp.diff(inner,x))+'.\n$$\n\n'
    if not indefinite:
        ulo=sp.simplify(inner.subs(x,lo));uhi=sp.simplify(inner.subs(x,hi))
        sol+='Calculating the limits for $u$ gives\n\n| $x$ | $'+L(lo)+'$ | $'+L(hi)+'$ |\n| --- | --- | --- |\n| $u$ | $'+L(ulo)+'$ | $'+L(uhi)+'$ |\n\n'
    sol+='Using the above, we can '+('rewrite' if t in ('q-350202','q-350203') else 'write')+' the integral in terms of $u$ and evaluate:\n\n$$\n'+r'\begin{aligned}'+integral+r' &= '
    if indefinite:sol+=L(factor)+r'\int '+L(h)+r'\,\text{d}u \\ &= '+L(factor*H)+r'+C \\ &= '+L(correct)+r'+C'
    else:
        limits=r'_{'+L(ulo)+'}^{'+L(uhi)+'}'
        sol+=L(factor)+r'{\int }'+limits+L(h)+r'\,\text{d}u \\ &= '+L(factor*H)+r'\big|'+limits+r' \\ &= '+L((factor*H).subs(u,uhi))+'-('+L((factor*H).subs(u,ulo))+r') \\ &= '+L(correct)
    sol+=r'\end{aligned}'+'\n$$'
    if m==1 and old.get(':question/worked-solution'):sol=old[':question/worked-solution']
    proto={':question/problem':prompt};fp=fingerprint(proto)
    uid=lambda s:str(uuid.uuid5(uuid.UUID(GENERATOR_UUID),s))
    qid=uid('question:'+fp+':profile:'+t);fid=uid(qid+':field:'+of[':answer-field/key'])
    answers=[{':answer/id':uid(fid+':answer:'+str(i)),':answer/type':':answer.type/math',':answer/value':a} for i,a in enumerate(values)]
    q={':question/id':qid,':question/problem':prompt,':question/worked-solution':sol,':question/difficulty':':question.difficulty/'+level,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':of[':answer-field/key'],':answer-field/type':of[':answer-field/type'][':db/ident'],':answer-field/choices':answers,':answer-field/correct':[':answer/id',answers[indices[0]][':answer/id']]}]}
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':'Integrating Products Containing Trigonometric Functions Using Substitution'},'question':q,'generation':{'version':VERSION,'generator_id':GENERATOR_UUID,'seed':seed,'template':t,'profile':t if len(bank)>1 else None,'parameters':{'m':m},'source_question':t,'source_basis':json.loads((HERE/'source.json').read_text())['basis'],'mathematical_fingerprint':fp,'domain':'Connected real intervals excluding poles; x != 0 for reciprocal substitution. Definite intervals avoid poles.','dependencies':{'sympy':sp.__version__},'recipe_policy':'Multiply every complete source-bank expression, including constants, by positive amplitude m; no inferred learner misconception.'}}
def candidates(level):
    for t in DATA:
        if DATA[t][0]==level:
            for m in range(2,13):yield t,{'m':m}
def batch(level,count,seed):
    if level not in ('moderate','hard') or type(count) is not int or count<1:raise ValueError('Unsupported level/count')
    c=list(candidates(level));random.Random(seed).shuffle(c)
    if count>len(c):raise ValueError('Finite variant limit: '+str(len(c)))
    return [generate(level,seed,t,params) for t,params in c[:count]]
def markdown(rec):
    q=rec['question'];f=q[':question/answer-fields'][0]
    return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$'+(' (correct)' if a[':answer/id']==f[':answer-field/correct'][1] else '') for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--difficulty',required=True);a.add_argument('--count',type=int,default=5);a.add_argument('--seed',type=int,default=0);a.add_argument('--format',choices=['json','markdown'],default='json');args=a.parse_args();records=batch(args.difficulty,args.count,args.seed);print(json.dumps(records,indent=2) if args.format=='json' else '\n\n'.join(map(markdown,records)))
