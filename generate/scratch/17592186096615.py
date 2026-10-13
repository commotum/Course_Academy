#!/usr/bin/env python3
"""Source-preserving general-base logarithm derivatives, v1.

Easy and hard source labels retained. Moderate has no validated template.
No new plots. Source text and full observed banks are parameterized together.
"""
import argparse, copy, hashlib, json, random, re, sys, uuid
from pathlib import Path
try:
    import sympy as sp
except ImportError:
    import os
    os.execv(str(Path(__file__).resolve().parents[2]/'.venv/bin/python'), [str(Path(__file__).resolve().parents[2]/'.venv/bin/python'),__file__,*sys.argv[1:]])

HERE=Path(__file__).with_suffix('')
KP_ID=17592186096615
KP_UUID='5856f3cc-5423-5a97-b2fd-7f44e0797ec7'
TITLE='Differentiating a Logarithmic Function With a General Base'
VERSION='general-base-log-v1'
X=sp.Symbol('x',positive=True)
SOURCES={q[':question/math-academy-id']:q for q in json.loads((HERE/'source.json').read_text())['record'][':knowledge-point/questions']}
# Different answer layouts and different worked sequences stay separate.
TEMPLATES={
 'scaled-log':('easy','q-11900'),
 'exp-explicit-radio':('easy','q-105256'),
 'exp-common-radio':('easy','q-1921'),
 'quadratic-slope':('easy','q-339989'),
 'log-minus-ln':('easy','q-339997'),
 'cubic-slope':('easy','q-339994'),
 'exp-common-blank':('easy','q-340105'),
 'negative-exp-log':('easy','q-340106'),
 'log-ln-exp-slope':('hard','q-308866'),
}
PARAMETERS={
 'scaled-log':{'a':5,'base':4},
 'exp-explicit-radio':{'expbase':7,'base':5,'wrong_expbase':4},
 'exp-common-radio':{'expbase':2,'base':10,'wrong_expbase':4},
 'quadratic-slope':{'a':4,'b':6,'base':3,'point':1},
 'log-minus-ln':{'base':7,'b':3},
 'cubic-slope':{'a':2,'b':3,'base':6,'point':3},
 'exp-common-blank':{'expbase':3,'base':10},
 'negative-exp-log':{'a':3,'base':5},
 'log-ln-exp-slope':{'a':2,'b':4,'c':5,'base':3,'point':1},
}

def tex(v):return sp.latex(v).replace(r'\log',r'\ln')

def expressions(t,p):
    a,b,c,base=[sp.Integer(p.get(k,1)) for k in ('a','b','c','base')]
    log=sp.log(X)/sp.log(base)
    if t=='scaled-log':f=a*log
    elif t.startswith('exp-'):f=sp.Integer(p['expbase'])**X+log
    elif t=='quadratic-slope':f=a*X**2-b*log
    elif t=='log-minus-ln':f=log-b*sp.log(X)
    elif t=='cubic-slope':f=a*X**3+X-b*log
    elif t=='negative-exp-log':f=-sp.exp(X)+a*log
    elif t=='log-ln-exp-slope':f=a*log-b*sp.log(X)+c*sp.exp(X)
    else:raise ValueError(t)
    d=sp.diff(f,X)
    return f,d,sp.simplify(d.subs(X,p['point'])) if 'point' in p else d

def validate_parameters(p,level,t,profile='source-bank'):
    assert t in TEMPLATES and TEMPLATES[t][0]==level
    assert set(p)==set(PARAMETERS[t]) and all(isinstance(x,int) and not isinstance(x,bool) for x in p.values())
    assert 2<=p['base']<=12
    assert all(2<=p[k]<=12 for k in ('a','b','c','expbase') if k in p)
    if 'common' in t:assert p['base']==10
    if 'wrong_expbase' in p:assert p['wrong_expbase']==4 and p['expbase']!=4
    if t=='scaled-log':assert p['a']!=p['base']
    # The deployed grader can fail to distinguish zero from a transcendental
    # rate with mixed signs. Keep c >= b, including the observed source, so
    # the evaluated rate is provably positive under its supported rules.
    if t=='log-ln-exp-slope':assert p['c']>=p['b']
    if 'point' in p:assert p['point']==PARAMETERS[t]['point']
    assert profile=='source-bank'

def sampler(t,rng):
    p=copy.deepcopy(PARAMETERS[t])
    for k in p:
        if k not in ('point','wrong_expbase') and not(k=='base' and 'common' in t):p[k]=rng.randint(2,12)
    return p

def numeric(s,mapping):
    # One simultaneous pass avoids replacements cascading into each other.
    return re.sub(r'(?<![0-9])(?:'+ '|'.join(sorted(mapping,key=len,reverse=True))+r')(?![0-9])',lambda m:str(mapping[m[0]]),s)

def render(s,t,p):
    if t=='scaled-log':return numeric(s,{'5':p['a'],'4':p['base']})
    if t=='exp-explicit-radio':return numeric(s,{'7':p['expbase'],'5':p['base']})
    if t=='exp-common-radio':return numeric(s,{'2':p['expbase']})
    if t=='exp-common-blank':return numeric(s,{'3':p['expbase']})
    if t=='negative-exp-log':return numeric(s,{'3':p['a'],'5':p['base']})
    if t=='log-minus-ln':return numeric(s,{'7':p['base'],'3':p['b']})
    if t=='quadratic-slope':return numeric(s,{'4':p['a'],'6':p['b'],'3':p['base'],'8':2*p['a']})
    if t=='log-ln-exp-slope':return numeric(s,{'2':p['a'],'4':p['b'],'5':p['c'],'3':p['base']})
    if t=='cubic-slope':
        # Source 3 is exponent, coefficient, and point; source 6 is base and
        # derivative coefficient. Replace entire role-bearing fragments.
        pairs={
          '2{x}^{3}':f"{p['a']}{{x}}^{{3}}",
          '3{log}_{6}':f"{p['b']}{{log}}_{{{p['base']}}}",
          r'2\cdot 3':str(p['a'])+r'\cdot 3',
          r'3\cdot \frac{1}{xln⁡6}':str(p['b'])+r'\cdot \frac{1}{xln⁡'+str(p['base'])+'}',
          '6{x}^{2}':f"{3*p['a']}{{x}}^{{2}}",
          r'\frac{3}{xln⁡6}':r'\frac{'+str(p['b'])+'}{xln⁡'+str(p['base'])+'}',
          '6(3)^{2}':f"{3*p['a']}(3)^{{2}}",
          r'\frac{3}{3\cdot ln⁡6}':r'\frac{'+str(p['b'])+r'}{3\cdot ln⁡'+str(p['base'])+'}',
          '55':str(27*p['a']+1),
          r'\frac{1}{ln⁡6}':r'\frac{'+str(sp.Rational(p['b'],3).p)+'}{'+('' if sp.Rational(p['b'],3).q==1 else str(sp.Rational(p['b'],3).q))+r'ln⁡'+str(p['base'])+'}',
          r'\frac{1}{\operatorname{ln}6}':r'\frac{'+str(sp.Rational(p['b'],3).p)+'}{'+('' if sp.Rational(p['b'],3).q==1 else str(sp.Rational(p['b'],3).q))+r'\operatorname{ln}'+str(p['base'])+'}',
        }
        return re.sub('|'.join(re.escape(k) for k in sorted(pairs,key=len,reverse=True)),lambda m:pairs[m[0]],s)
    raise ValueError(t)

def fingerprint(t,p):
    f,d,answer=expressions(t,p)
    # The assessed derivative and evaluation point define the task. A constant,
    # bank profile, field type, order, UUID or seed cannot create a new task.
    return hashlib.sha256(json.dumps([sp.srepr(sp.expand(sp.expand_log(d,force=True))),str(p['point']) if 'point' in p else None],sort_keys=True).encode()).hexdigest()

def generate(level,seed=0,template=None,parameters=None,profile='source-bank'):
    rng=random.Random(seed)
    candidates=[t for t,(l,_) in TEMPLATES.items() if l==level]
    if not candidates:raise ValueError('Unsupported difficulty '+level+': no validated source template')
    t=template or rng.choice(candidates)
    for _ in range(100):
        p=parameters or sampler(t,rng)
        try:validate_parameters(p,level,t,profile);break
        except AssertionError:
            if parameters:raise
    else:raise ValueError('No valid parameters')
    source=SOURCES[TEMPLATES[t][1]]
    fp=fingerprint(t,p)
    qid=str(uuid.uuid5(uuid.UUID(KP_UUID),VERSION+'/'+t+'/'+json.dumps(p,sort_keys=True)))
    fsrc=source[':question/answer-fields'][0]
    fid=str(uuid.uuid5(uuid.UUID(qid),'field/'+fsrc[':answer-field/key']))
    choices=[];correct=None
    for a in fsrc[':answer-field/choices']:
        value=render(a[':answer/value'],t,p)
        aid=str(uuid.uuid5(uuid.UUID(fid),value))
        choices.append({':answer/id':aid,':answer/type':a[':answer/type'][':db/ident'],':answer/value':value})
        if a[':answer/id']==fsrc[':answer-field/correct'][':answer/id']:correct=aid
    q={':question/id':qid,':question/problem':render(source[':question/problem'],t,p),':question/worked-solution':render(source[':question/worked-solution'],t,p),':question/difficulty':':question.difficulty/'+level,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':fsrc[':answer-field/key'],':answer-field/type':fsrc[':answer-field/type'][':db/ident'],':answer-field/choices':choices,':answer-field/correct':[':answer/id',correct]}]}
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'parameters':p,'template':t,'bank_profile':profile,'parameter_fingerprint':fp,'domain':'x > 0; integer logarithm bases 2..12','source_question_ids':[TEMPLATES[t][1]],'sympy_version':sp.__version__,'sampling_policy':'Integer coefficients/bases 2..12; fixed source evaluation points; hard exponential coefficient c >= ln coefficient b for native zero rejection; observed altered exponential base 4 retained without inferring its mistake.'}}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',required=True);ap.add_argument('--count',type=int,default=1);ap.add_argument('--seed',type=int,default=0);ap.add_argument('--format',choices=['json','markdown'],default='json');ap.add_argument('--template');args=ap.parse_args()
    # Mathematical fingerprints deduplicate the requested batch.
    records=[];used=set()
    for i in range(max(100,args.count*100)):
        if len(records)>=args.count:break
        r=generate(args.difficulty,args.seed+i,args.template)
        fp=r['generation']['parameter_fingerprint']
        if fp not in used:used.add(fp);records.append(r)
    if len(records)<args.count:raise ValueError('Finite limit: insufficient distinct variants')
    print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(r['question'][':question/problem']+'\n\n'+r['question'][':question/worked-solution'] for r in records))
if __name__=='__main__':main()
