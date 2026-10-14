#!/usr/bin/env python3
"""Source-derived bounded quartic factoring generators; easy/moderate only."""
import argparse, hashlib, json, os, random, sys, uuid
from pathlib import Path
if __name__=='__main__':
    try: import sympy
    except ImportError:
        interpreter=Path(__file__).resolve().parents[2]/'.venv/bin/python'
        os.execv(str(interpreter),[str(interpreter),__file__,*sys.argv[1:]])
import sympy as sp
x=sp.Symbol('x')
KP_ID=17592186054803
KP_UUID='c2e897cc-b3fe-5d2f-8b47-3afdfe276bcf'
TITLE='Factoring a Quartic Polynomial Given Two Factors'
GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),'question-generator'))
VERSION='quartic-two-factors-v1'
PACKAGE=Path(__file__).with_suffix('')
SOURCE=json.loads((PACKAGE/'source.json').read_text())
PROFILES={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
CASES={
 'q-112626':dict(r=5,s=-1,c=1,a=1,b=-7),
 'q-18862':dict(r=2,s=3,c=1,a=-1,b=-3),
 'q-328505':dict(r=2,s=3,c=1,a=-2,b=1),
 'q-112615':dict(r=3,s=-1,c=3,a=1,b=2),
 'q-112617':dict(r=3,s=-4,c=3,a=2,b=-1)}
LEVELS={'easy':('q-112626','q-18862','q-328505'),'moderate':('q-112615','q-112617')}
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def ident(v):return str(uuid.uuid5(uuid.UUID(KP_UUID),digest(v)))
def tex(e):return sp.latex(e)
def lin(c,a):return tex(c*x-a)
def fact(c,a,b):return '('+lin(c,a)+')('+lin(1,b)+')'
def bank(profile,p):
    r,s,c,a,b=(p[k] for k in ('r','s','c','a','b'))
    if profile=='q-112626':return [fact(1,-b,-a),fact(1,a,b),'('+lin(1,a)+')('+tex(r-x)+')','('+tex(a+1-x)+')('+lin(1,-a)+')',fact(1,r,b)],1
    if profile=='q-18862':return [fact(1,-a,b),fact(1,a,b),fact(1,a,-b),fact(1,-a,-b),'('+tex(-a-x)+')('+lin(1,b)+')'],1
    if profile=='q-112615':return [fact(c+1,a,b-1),fact(c,-a,b),fact(c-1,-a,-b),fact(c-1,a,-b),fact(c,a,b)],4
    if profile=='q-112617':return [fact(c-1,-(a+1),-b),fact(c,a,b),fact(c-1,a+1,-b),fact(c,-a,b),fact(c+1,a+1,b-1)],1
    if profile=='q-328505':return [tex(sp.expand((c*x-a)*(x-b)))],0
    raise ValueError('Excluded source profile')
def synthetic(coeffs,root):
    bottom=[coeffs[0]];products=[]
    for coeff in coeffs[1:]:
        products.append(bottom[-1]*root);bottom.append(coeff+products[-1])
    return bottom,products

def table(poly,root):
    co=sp.Poly(poly,x).all_coeffs();bo,pr=synthetic(co,root);n=len(co)-1
    row=lambda cells:'| '+' | '.join(cells)+' |'
    return '\n'.join([row(['']+['$x^{'+str(i)+'}$' for i in range(n,-1,-1)]),row(['---']*(n+2)),row(['$'+str(root)+'$']+['$'+str(z)+'$' for z in co]),row(['','$\\downarrow$']+['$'+str(z)+'$' for z in pr]),row(['']+['$'+str(z)+'$' for z in bo])])
def solution(profile,p,F,Q,P):
    r,s=p['r'],p['s'];c,a,b=p['c'],p['a'],p['b'];fr,fs=lin(1,r),lin(1,s)
    first,second=(s,r) if profile=='q-18862' else (r,s)
    l1,l2=lin(1,first),lin(1,second);T=sp.div(F,x-first,x)[0]
    tf,tT,tP=tex(F),tex(T),tex(P)
    sol=f'Let $f(x)={tf}.$ We know that $({fr})$ and $({fs})$ are factors of $f(x),$ and we need to find its other factors.\n\n'
    sol+=f'Because $({l1})$ is a factor of $f(x),$ we know that $({l1})$ divides $f(x)$ with no remainder. So, to begin factoring $f(x),$ we can divide it by $({l1})$ using synthetic division:\n\n'+table(F,first)+'\n\nTherefore,\n\n'
    sol+='$$\n\\frac{'+tf+'}{'+l1+'}='+tT+',\n$$\n\nwhich means that\n\n$$\n'+tf+'=('+l1+')('+tT+').\n$$\n\n'
    sol+=f'Now, because $({l2})$ is also a factor of $f(x),$ it must be a factor of the quotient $({tT}).$ So, we divide this quotient by $({l2})$ using synthetic division once more:\n\n'+table(T,second)+'\n\nTherefore,\n\n'
    sol+='$$\n\\frac{'+tT+'}{'+l2+'}='+tP+',\n$$\n\nwhich means that\n\n$$\n'+tf+'=('+fr+')('+fs+')('+tP+').\n$$\n\n'
    if profile=='q-328505':sol+='Therefore,\n\n$$\nP(x)='+tP+'='+fact(c,a,b)+'.\n$$'
    else:sol+='We can factor the quadratic factor even further, and get\n\n$$\n'+tf+'=('+fr+')('+fs+')\\underbrace{'+fact(c,a,b)+'}_{P(x)}.\n$$\n\nTherefore, $P(x)='+fact(c,a,b)+'.$'
    return sol

def generate(difficulty,seed=0,profile=None,parameters=None):
    if difficulty not in LEVELS:raise ValueError('Unsupported band; no rated hard source')
    profile=profile or LEVELS[difficulty][0]
    if profile not in LEVELS[difficulty]:raise ValueError('Profile difficulty mismatch')
    p=dict(parameters or CASES[profile]);r,s,c,a,b=(p[k] for k in ('r','s','c','a','b'))
    if not all(isinstance(z,int) for z in (r,s,c,a,b)) or r==s or c<1 or 0 in (r,s,a,b):raise ValueError('Invalid parameter boundary')
    if difficulty=='easy' and c!=1 or difficulty=='moderate' and c!=3:raise ValueError('Leading coefficient outside source-derived workload')
    P=sp.expand((c*x-a)*(x-b));Q=sp.expand((x-s)*P);F=sp.expand((x-r)*Q)
    values,correct=bank(profile,p)
    # Reject degeneracies in the complete chosen source bank.
    from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
    parse=lambda t:parse_expr(t.replace('^{','**').replace('^','**').replace('{','').replace('}',''),transformations=standard_transformations+(implicit_multiplication_application,),local_dict={'x':x})
    polys=[sp.expand(parse(t)) for t in values]
    if len(set(map(str,polys)))!=len(values) or sum(z==P for z in polys)!=1 or polys[correct]!=P:raise ValueError('Ambiguous source bank')
    task=digest([str(F),sorted((r,s))]);qid=ident(['question',task,profile,values]);fid=ident(['field',qid]);key='field-1' if profile=='q-328505' else 'selection'
    answers=[{':answer/id':ident(['answer',fid,value]),':answer/type':':answer.type/math',':answer/value':value} for value in values]
    if key=='field-1':
        prompt='The polynomial\n\n$$\n'+tex(F)+'\n$$\n\ncan be expressed as\n\n$$\n('+lin(1,r)+')('+lin(1,s)+')\\cdot P(x).\n$$\n\nFind the polynomial $P(x).$\n\n$P(x)=$\n{{field-1}}'
    else:prompt='Find the polynomial $P(x)$ given that\n\n$$\n'+tex(F)+'=('+lin(1,r)+')('+lin(1,s)+')P(x).\n$$'
    q={':question/id':qid,':question/problem':prompt,':question/worked-solution':solution(profile,p,F,Q,P),':question/difficulty':':question.difficulty/'+difficulty,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+('blank' if key=='field-1' else 'radio'),':answer-field/choices':answers,':answer-field/correct':[':answer/id',answers[correct][':answer/id']]}]}
    return {'question':q,'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'generation':{'version':VERSION,'seed':seed,'template':'expanded-quartic-blank' if key=='field-1' else 'factored-quartic-radio','bank_profile':profile,'source_refs':[profile],'parameters':p,'parameter_fingerprint':task,'sympy_version':sp.__version__,'assets':[]}}

def candidates(profile):
    # Bounded same-method extension: small signed roots, monic easy / coefficient-three moderate.
    base=CASES[profile]
    for r in (-4,-2,1,2,3,4,5):
      for s in (-5,-3,-1,1,2,3):
       for delta in (-1,0,1):
        for shift in (-1,0,1):
         p=dict(base,r=r,s=s,a=base['a']+delta,b=base['b']+shift)
         try:generate('easy' if profile in LEVELS['easy'] else 'moderate',profile=profile,parameters=p)
         except ValueError:continue
         yield p

def batch(difficulty,count,seed):
    if difficulty not in LEVELS:raise ValueError('Unsupported difficulty')
    if count<1:raise ValueError('Positive count required')
    rng=random.Random(seed);profiles=list(LEVELS[difficulty]);pools={k:list(candidates(k)) for k in profiles}
    for pool in pools.values():rng.shuffle(pool)
    records=[];used=set()
    while any(pools.values()) and len(records)<count:
      for profile in profiles:
       while pools[profile]:
        rec=generate(difficulty,seed,profile,pools[profile].pop());fp=rec['generation']['parameter_fingerprint']
        if fp not in used:records.append(rec);used.add(fp);break
       if len(records)==count:break
    if len(records)<count:raise ValueError(f'Finite distinct task limit: {len(records)}; requested {count}')
    return records
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',required=True);ap.add_argument('--count',type=int,default=1);ap.add_argument('--seed',type=int,default=0);ap.add_argument('--format',choices=['json','markdown'],default='json');args=ap.parse_args()
    out=batch(args.difficulty,args.count,args.seed)
    print(json.dumps(out,indent=2) if args.format=='json' else '\n\n---\n\n'.join(r['question'][':question/problem']+'\n\n'+r['question'][':question/worked-solution'] for r in out))
