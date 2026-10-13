#!/usr/bin/env python3
"""Surface-integral Stokes generators, frozen math basis 1356. Stop at step 7.

All observed full prose/stage masks and opaque complete banks replay publicly via
profile='raw'; these are evidence-only. Their scalar extension multiplies the
entire supplied field and every field-dependent stage, with honest historical
errors retained. Normal profiles derive complete banks from real operations.
Easy is authored (no observed easy sources); moderate/hard preserve source
families and labels. Sampling chooses a family first, then the whole bank.
No database access, plots, registration, or engine mutation.
"""
from __future__ import annotations
import argparse, hashlib, json, random, re, sys, uuid
from functools import lru_cache
from pathlib import Path
import sympy as s
ROOT=Path(__file__).with_suffix('')
VERSION='surface-stokes-1'
CAPTURE=json.loads((ROOT/'source.json').read_text())
KP=CAPTURE['record']
T,X,Y,Z=s.symbols('t x y z',real=True)
LOC={'t':T,'x':X,'y':Y,'z':Z,'pi':s.pi,'sin':s.sin,'cos':s.cos,'exp':s.exp}
# Full coordinate/field components, not token substitutions. Each tuple is
# (observed level, original r, original F, lower, upper).
FAMILIES={
'q-161928':('moderate',('t**2-t','t-t**3','2*t**2-2*t'),('y','0','x'),'0','1'),
'q-162377':('hard',('sin(pi*t)','cos(pi*t)','sin(pi*t)'),('x','0','y'),'-1','1'),
'q-162316':('moderate',('2*t**3-2*t','3*t**2+3*t','t**3-t'),('z','0','y'),'-1','0'),
'q-162324':('hard',('cos(pi*t)','sin(pi*t)','cos(pi*t)'),('y','0','x'),'-1','1'),
'q-162886':('moderate',('t**2+t','t**3+t**2','2*t**2+2*t'),('y','z','x'),'-1','0'),
'q-162887':('moderate',('t**3-t','2*t**2+1','t**2-1'),('y','3','y*z'),'-1','1'),
'q-162892':('hard',('cos(pi*t)','sin(pi*t)','2*sin(pi*t)'),('2*y','-2*x','exp(z-2*y)'),'-1','1'),
'q-162889':('hard',('cos(t)','sin(t)','1'),('z','3*x','2*y**2'),'0','2*pi'),
'q-162891':('hard',('cos(t)','sin(t)','1-sin(t)'),('y-z','z-x','x-y'),'0','2*pi'),
'q-162999':('moderate',('t**2-t','t**2-t**3','t**2-t'),('2*z','0','3*y'),'0','1'),
'q-162314':('hard',('2*t**3-2*t','t+t**2','-t-t**2'),('y','0','x'),'-1','0'),
'easy-circle':('easy',('cos(t)','sin(t)','1'),('-y','x','0'),'0','2*pi'),
}
SOURCES={q[':question/math-academy-id']:q for q in KP[':knowledge-point/questions']}
MASKS=json.loads((ROOT/'source-masks.json').read_text())
def expr(text): return s.sympify(text,locals=LOC)
def tex(e): return s.latex(e).replace(r'\log',r'\ln')
def fingerprint(data): return hashlib.sha256(json.dumps(data,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def uid(text): return str(uuid.uuid5(uuid.NAMESPACE_URL,VERSION+':'+text))
def wrap(e): return r'\left('+tex(e)+r'\right)'
def vec(v): return r'\langle '+', '.join(tex(a) for a in v)+r'\rangle'
def display(content): return '\n\n$$\n'+content+'\n$$'
def align(lhs, rows): return display(r'\begin{aligned}'+lhs+' & ='+r' \\ & ='.join(rows)+r'\end{aligned}')
def scale_mask(c,raw):
    # Unit-factor normalization is an ordinary parameterized recipe, not replay.
    return ('' if c==1 else tex(c)+r'\left(')+raw+('' if c==1 else r'\right)')
def parse_scalar(raw):
    text=raw.replace('π',r'\pi').strip()
    text=re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}',r'(\1)/(\2)',text)
    text=text.replace(r'\pi','pi').replace(' ','')
    text=re.sub(r'(?<=[0-9)])pi', '*pi', text)
    return expr(text)
def make_fields(banks,identity,seed):
    fields=[]
    for i,bank in enumerate(banks):
        fuid=uid(identity+':field:'+str(i)); answers=[]
        for val in bank['values']:
            answers.append({':answer/id':uid(fuid+':'+val),':answer/type':':answer.type/math',':answer/value':val})
        field={':answer-field/id':fuid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers}
        if 'correct_index' in bank: field[':answer-field/correct']=[':answer/id',answers[bank['correct_index']][':answer/id']]
        random.Random(seed+17*i).shuffle(answers); fields.append(field)
    return fields

def raw_record(template,p,seed):
    """Instantiate extracted full field-dependent component masks and banks.

    Raw historical mistakes remain ineligible even after a scalar change. Key
    omissions and duplicate fields are preserved, never inferred in raw mode.
    """
    if set(p)!={'c'} or type(p['c']) is not int or not 1<=abs(p['c'])<=4: raise ValueError('raw requires nonzero integer c of magnitude <=4')
    c=p['c']; m=MASKS[template]; q={}
    for key,value in m['attributes'].items():
        if isinstance(value,str):
            for name,fragment in m['slots'].items(): value=value.replace('{{'+name+'}}',scale_mask(c,fragment))
        q[key]=value
    banks=[]
    for b in m['banks']:
        bb={'values':[v if c==1 else tex(c*parse_scalar(v)) for v in b['values']]}
        if 'correct_index' in b: bb['correct_index']=b['correct_index']
        banks.append(bb)
    content=fingerprint([VERSION,q,banks]); q[':question/id']=uid(content)
    q[':question/answer-fields']=make_fields(banks,content,seed)
    level=FAMILIES[template][0]
    r,f,lo,hi=objects(template,{'a':1,'b':1,'d':1,'c':c})
    return {'knowledge_point':{'db_id':KP[':db/id'],'id':KP[':knowledge-point/id'],'title':KP[':knowledge-point/title']},'question':q,'generation':{'version':VERSION,'template':template,'parameters':p,'bank_profile':'raw','seed':seed,'eligible_for_learning':False,'evidence_only':True,'raw_source':template,'source':{k:CAPTURE[k] for k in ['database','basis','lineage']},'mathematical_fingerprint':task_fingerprint(r,f,lo,hi),'content_fingerprint':content,'difficulty_assignment':'authored hard for unrated trigonometric source' if template=='q-162377' else 'observed','dependencies':{'python':sys.version.split()[0],'sympy':s.__version__}}}

def objects(template,p):
    _,rr,ff,l,h=FAMILIES[template]
    r=tuple(s.expand(expr(v)*p[n]) for v,n in zip(rr,['a','b','d']))
    f=tuple(s.expand(expr(v)*p['c'],power_exp=False) for v in ff)
    return r,f,expr(l),expr(h)
def task_fingerprint(r,f,lo,hi):
    # Boundary parameterization and its traversal are assessed here. Bank,
    # coefficient spelling and source/profile aliases are excluded.
    return fingerprint([[s.srepr(s.simplify(v)) for v in r],[s.srepr(s.simplify(v)) for v in f],s.srepr(lo),s.srepr(hi),'surface curl integral via oriented boundary'])
@lru_cache(maxsize=4096)
def computation(template,a,b,d,c):
    r,f,lo,hi=objects(template,dict(a=a,b=b,d=d,c=c))
    fr=tuple(s.expand(v.subs(dict(zip((X,Y,Z),r)),simultaneous=True)) for v in f)
    rp=tuple(s.diff(v,T) for v in r)
    terms=tuple(s.expand(u*v) for u,v in zip(fr,rp))
    dot=s.expand(sum(terms)); reduced=dot
    # Explicit trig identities make the integrand elementary without CAS
    # introducing special functions or absorbing primitive component stages.
    reduced=s.expand_trig(reduced).expand().subs(s.sin(s.pi*T)**2,(1-s.cos(2*s.pi*T))/2).subs(s.cos(s.pi*T)**2,(1+s.cos(2*s.pi*T))/2).subs(s.sin(T)**2,(1-s.cos(2*T))/2).subs(s.cos(T)**2,(1+s.cos(2*T))/2).expand()
    components=tuple(s.integrate(v,T) for v in s.Add.make_args(reduced))
    primitive=sum(components); correct=s.simplify(sum(v.subs(T,hi)-v.subs(T,lo) for v in components))
    return r,f,lo,hi,fr,rp,terms,dot,reduced,components,primitive,correct

def check_parameters(level,template,p):
    if set(p)!={'a','b','d','c'}: raise ValueError('parameters require exactly a,b,d,c')
    if any(type(v) is not int or not 1<=abs(v)<=3 for v in p.values()): raise ValueError('nonzero integer coefficient magnitudes must be <=3')
    if template=='q-162892' and p['d']!=p['b']: raise ValueError('exponential must reduce to exp(0): d=b')
    if level=='easy' and p['d']!=1: raise ValueError('easy horizontal circle height remains 1')
    if template=='q-162887' and max(abs(p[v]) for v in ['b','d'])>2: raise ValueError('moderate bilinear component coefficient magnitude <=2')

def bank_values(template,data):
    r,f,lo,hi,fr,rp,terms,dot,reduced,components,primitive,correct=data
    if template=='easy-circle':
        return [correct,-correct,s.S.Zero,s.integrate(dot,(T,lo,(lo+hi)/2)),s.simplify(correct/s.pi)],['correct','reverse boundary','zero curl assumption','half boundary interval','omit pi from angular endpoint']
    if any(v.has(s.sin,s.cos) for v in r):
        # π-angle families lose the chain factor; unit-angle families lose the
        # 1/2 in the square identity (twice the square contribution).
        frequency=s.pi if any(v.has(s.sin(s.pi*T),s.cos(s.pi*T)) for v in r) else s.S.One
        wrong_chain=s.simplify(correct/frequency) if frequency!=1 else s.simplify(2*correct)
        return [correct,-correct,s.S.Zero,s.integrate(dot,(T,lo,(lo+hi)/2)),wrong_chain],['correct','reverse boundary','zero curl assumption','half boundary interval','omit pi chain factor' if frequency!=1 else 'omit half in squared trig identity']
    wrong_input=tuple(v.subs(dict(zip((X,Y,Z),rp)),simultaneous=True) for v in f)
    vals=[correct,-correct,s.integrate(sum(u*v for u,v in zip(fr,r)),(T,lo,hi)),s.integrate(sum(fr),(T,lo,hi)),s.integrate(sum(u*v for u,v in zip(wrong_input,rp)),(T,lo,hi))]
    return [s.simplify(v) for v in vals],['correct','reverse boundary','use r instead of tangent','omit tangent in dot product','substitute tangent into field']

def normal_record(level,template,p,seed):
    check_parameters(level,template,p)
    data=computation(template,**p); r,f,lo,hi,fr,rp,terms,dot,reduced,components,primitive,correct=data
    vals,recipes=bank_values(template,data)
    if any(s.simplify(a-b)==0 for i,a in enumerate(vals) for b in vals[:i]): raise ValueError('whole-bank equivalence rejection')
    if correct==0 or any(v.has(s.Integral,s.nan,s.oo,s.zoo) for v in vals): raise ValueError('invalid complete bank')
    problem='Let $S$ be an oriented piecewise-smooth surface bounded by the closed curve $C$ with positive orientation and parametrization $r(t)='+vec(r)+'$ for $t\\in ['+tex(lo)+','+tex(hi)+').$\nGiven that $F(x,y,z)='+vec(f)+',$ evaluate the integral'+display(r'\iint_S\operatorname{curl}F\cdot\mathrm{d}S.')
    opening=MASKS['q-161928']['opening']
    sol=opening+'\n\nAlong the curve $C,$ we have'+display(',\\quad '.join(tex(v)+'='+tex(u) for v,u in zip((X,Y,Z),r)))
    # Preserve complete formal/substitution/reduction stages. Unsimplified
    # component substitutions retain exponential/bilinear workload visibly.
    substituted=[]
    for component in f:
        text=tex(component)
        for symbol,value in [(X,r[0]),(Y,r[1]),(Z,r[2])]:
            text=re.sub(r'(?<![A-Za-z\\])'+str(symbol)+r'(?![A-Za-z])',lambda m:wrap(value),text)
        substituted.append(text)
    rawvec=r'\langle '+', '.join(substituted)+r'\rangle'
    sol+='\n\nSo,'+align('F(r(t))',[vec(f),rawvec,vec(fr)])
    deriv=r'\langle '+', '.join(r'\frac{\mathrm d}{\mathrm dt}'+wrap(v) for v in r)+r'\rangle'
    sol+='\n\nComputing $r\\prime(t),$ we get'+align(r'r\prime(t)',[deriv,vec(rp)])
    products='+'.join(wrap(u)+r'\cdot '+wrap(v) for u,v in zip(fr,rp))
    distributed='+'.join(wrap(v) for v in terms)
    sol+='\n\nTherefore,'+align(r'F(r(t))\cdot r\prime(t)',[vec(fr)+r'\cdot '+vec(rp),products,distributed,tex(dot),tex(reduced)])
    intprefix=r'\int_{'+tex(lo)+'}^{'+tex(hi)+'}'
    primitive_row=' + '.join(wrap(v) for v in components)
    endpoint=lambda pt:' + '.join(wrap(v.subs(T,pt)) for v in components)
    sol+='\n\nFinally, we evaluate the integral as follows:'+align(r'\iint_S\operatorname{curl}F\cdot\mathrm dS',[r'\oint_C F\cdot\mathrm dr',intprefix+r' F(r(t))\cdot r\prime(t)\,\mathrm dt',intprefix+wrap(reduced)+r'\,\mathrm dt',r'\left['+primitive_row+r'\right]_{'+tex(lo)+'}^{'+tex(hi)+'}',r'\left('+endpoint(hi)+r'\right)-\left('+endpoint(lo)+r'\right)',tex(correct)])
    values=[tex(v) for v in vals]; banks=[{'values':values,'correct_index':0}]
    q={':question/problem':problem,':question/worked-solution':sol,':question/difficulty':':question.difficulty/'+level}
    content=fingerprint([VERSION,q,banks]);q[':question/id']=uid(content);q[':question/answer-fields']=make_fields(banks,content,seed)
    return {'knowledge_point':{'db_id':KP[':db/id'],'id':KP[':knowledge-point/id'],'title':KP[':knowledge-point/title']},'question':q,'generation':{'version':VERSION,'template':template,'bank_profile':'method','parameters':p,'seed':seed,'eligible_for_learning':True,'evidence_only':False,'source':{k:CAPTURE[k] for k in ['database','basis','lineage']},'mathematical_fingerprint':task_fingerprint(r,f,lo,hi),'content_fingerprint':content,'recipes':recipes,'scope':'authored easy' if level=='easy' else ('authored hard assignment of unrated source' if template=='q-162377' else 'observed family, authored bank and coefficient variation'),'dependencies':{'python':sys.version.split()[0],'sympy':s.__version__}}}

# EASY: authored two nonzero tangent components, a horizontal ellipse, two
# linear field components; identity collapses the integral to a constant.
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
# MODERATE: observed polynomial boundaries and fields; <=degree-five dot
# products, with source-sized exact polynomial primitive/evaluation stages.
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
# HARD: observed full-cycle trigonometric/chain-rule families and observed
# signed-endpoint polynomial source q-162314; no unknown surface construction.
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)
def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ['easy','moderate','hard']:raise ValueError('unknown level')
    if field_type not in [None,'radio',':answer-field.type/radio']:raise ValueError('radio only')
    if profile not in [None,'method','raw']:raise ValueError('unknown profile')
    rng=random.Random(seed)
    choices=[k for k,v in FAMILIES.items() if v[0]==level]
    if template is None:template=rng.choice(choices)
    if template not in choices:raise ValueError('template outside requested difficulty')
    if profile=='raw':
        if template not in SOURCES:raise ValueError('no source for authored easy')
        return raw_record(template,parameters if parameters is not None else {'c':1},seed)
    if parameters is not None:return normal_record(level,template,parameters,seed)
    for _ in range(500):
        p={k:rng.choice([-3,-2,-1,1,2,3]) for k in ['a','b','d','c']}
        if level=='easy':p['d']=1
        if template=='q-162892':p['d']=p['b']
        if template=='q-162887':p['b']=rng.choice([-2,-1,1,2]);p['d']=rng.choice([-2,-1,1,2])
        try:return normal_record(level,template,p,seed)
        except ValueError as exc:
            if 'bank' not in str(exc):raise
    raise ValueError('no eligible instance in fixed family/bank')

def markdown(rec):
    q=rec['question'];meta=rec['generation'];raw=meta['evidence_only']
    label=('Original source evidence' if meta['parameters']['c']==1 else 'Generated source evidence') if raw else 'Generated variant'
    level=q.get(':question/difficulty','unrated').split('/')[-1]
    parts=['## '+label+' — '+level,meta.get('scope',meta.get('difficulty_assignment','')),q[':question/problem']]
    for f in q.get(':question/answer-fields',[]):
        correct=f.get(':answer-field/correct',[None,None])[1]
        for a in f[':answer-field/choices']:
            marker=' **(source designation)**' if raw else ' **(correct)**'
            parts.append('- $'+a[':answer/value']+'$'+(marker if a[':answer/id']==correct else ''))
        if correct is None:parts.append('Original correct designation absent.')
    parts+=['**Worked solution**',q.get(':question/worked-solution','Original worked solution absent.')]
    return '\n\n'.join(parts)
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile')
    args=ap.parse_args();levels=['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]
    records=[generate(l,args.seed+i,template=args.template,profile=args.profile) for l in levels for i in range(args.count)]
    print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
if __name__=='__main__':main()
