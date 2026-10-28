#!/usr/bin/env python3
"""Seeded, database-free divergence-theorem setup generator. See instructional-account.md."""
from __future__ import annotations
from audit_presentation import prose as _ca_prose, problem as _ca_problem, values as _ca_values, question as _ca_question, identity_material as _ca_material
import argparse, hashlib, json, random, re, sys, uuid
from functools import lru_cache
from pathlib import Path
import sympy as sp
BASE=Path(__file__).resolve().parent
SNAPSHOT=json.loads((BASE/'source-data.json').read_text())
KP=SNAPSHOT['record']; KP_ID=17592186133929
VERSION='flux-setup-v3-format-audit-9837-v1'
x,y,z=sp.symbols('x y z',real=True); VARS=(x,y,z)
SOURCE=KP[':knowledge-point/questions']
# Each family retains its source field layout and solution route. The raw banks
# below are symbolic expression shapes, not correct-answer or payload lookups.
CONFIG={
 'legacy':dict(index=0,level='easy',components=(x*z,y**2,sp.Integer(1)),outer=((x,1,3),(y,-1,1)),inner=(z,0,1),bank=(y**2+z,1,y**2+x,2*y+z,2*y+x)),
 'typeII':dict(index=1,level='moderate',components=(x*y**2,x*z,y),outer=((y,-1,1),(z,0,1)),inner=(x,y-2*z,4-y**2-z**2),bank=((z+3*y,-2,4),(y**2,4-y**2-z**2,y-2*z),(y**2,y-2*z,4-y**2-z**2),(2*y+1,y-2*z,4-y**2-z**2),(2*y+1,4-y**2-z**2,y-2*z))),
 'typeI':dict(index=2,level='moderate',components=(x+y,-2*y,x**2*z),outer=((x,0,2),(y,0,1)),inner=(z,y,x**2+y),bank=((2*x*z,y,x**2+y),(x**2-1,2*y,2*x**2+1),(y+z-2,2*y,2*x**2+1),(y+z-2,y,x**2+y),(x**2-1,y,x**2+y))),
 'typeIIIbowl':dict(index=3,level='moderate',components=(y**3-z,z,2*x*y*z),outer=((x,-1,1),(z,0,1)),inner=(y,x**2+z**2,2),bank=((x+y,0,2),(2*x*y,0,2),(3*y**2+x*y,x**2+z**2,2),(3*y**2+x*y,2,z**2+x**2),(2*x*y,x**2+z**2,2))),
 'box_product':dict(index=4,level='easy',components=(x*y,2*y,x**2*z),outer=((x,-1,0),(y,1,2)),inner=(z,0,1),bank=(2*x+y+1,x*y+2,x**2+2*y,x**2+x*y,x**2+y+2)),
 'box_collect':dict(index=5,level='easy',components=(x**2+y,-y*z,4*x*z),outer=((x,0,4),(y,-1,1)),inner=(z,0,2),bank=(2*x+3*z,2*x-z+4,6*x-z,6*x+4*z,2*x-y-2*z)),
 'typeIIIlinear':dict(index=6,level='moderate',components=(z,-4*y,z**3),outer=((x,0,1),(z,0,1)),inner=(y,x**2,x-z+2),bank=((3*z**2-4,x**2,x-z+2),(3*z**2-4,x**2,2),(z**3-3,x**2,2),(z**2,x**2,x-z+2),(z**3-3,x**2,x-z+2))),
 'box_zero':dict(index=7,level='easy',components=(x**2,x*y*z,2*y),outer=((x,-1,1),(y,0,2)),inner=(z,1,2),bank=(2*x+x*z,2+z,x+2*z,y+z,x+y*z)),
}
CONFIG.update({
 'box_exp':dict(index=8,level='easy',components=(y*sp.exp(x),z**2,3*z),outer=((x,0,3),(y,-1,2)),inner=(z,0,4),bank=(y+3,y*sp.exp(x)+2*z+3,sp.exp(x)+y,sp.exp(x)+2*z,y*sp.exp(x)+3)),
 'box_log':dict(index=9,level='easy',components=(x*sp.sqrt(y),-sp.log(y),x*y),outer=((x,0,2),(y,1,3)),inner=(z,1,2),bank=(x/(2*sp.sqrt(y))+y,x-sp.log(y),sp.sqrt(y)-1/y+x,sp.sqrt(y)-1/y,sp.sqrt(y)+x)),
 'typeIIlinear':dict(index=10,level='moderate',components=(sp.Integer(1),x*z**3,x*z),outer=((y,-1,1),(z,0,2)),inner=(x,y-z,1+y**2),bank=((3*x*z**2+z,y-z,1+y**2),(x,-1,2),(3*x*z**2+z,-1,2),(x,y-z,1+y**2),(x**2,y-z,1+y**2))),
})
from math_format import normalize_prose, normalize_tex, checked_math_content
def digest(obj):return hashlib.sha256(json.dumps(obj,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def uid(text):return str(uuid.uuid5(uuid.NAMESPACE_URL,'flux-setup:'+text))
def tex(e):return sp.latex(sp.sympify(e)).replace(' ', '').replace(r'\log', r'\ln')
def source_q(t):return SOURCE[CONFIG[t]['index']]
def integral(d,outer,inner,style=False):
 v,lo,hi=inner
 s=''.join(r'{\int }_{'+tex(a)+r'}^{'+tex(b)+'}' for _,a,b in outer)+r'{\int }_{'+tex(lo)+r'}^{'+tex(hi)+'}'
 return s+r'\,'+('('+tex(d)+')' if sp.sympify(d).is_Add else tex(d))+r'\,\text{d}'+str(v)+''.join(r'\,\text{d}'+str(w) for w,_,_ in reversed(outer))
def triple(d):return r'{∭}_{R}'+('('+tex(d)+')' if sp.sympify(d).is_Add else tex(d))+r'\,\text{d}V'
def field_tex(cs):
 return '+'.join('('+tex(c)+r')\,'+b for c,b in zip(cs,'ijk'))
def partials(cs):return tuple(sp.diff(c,v) for c,v in zip(cs,VARS))
def derivative_block(cs,ds):
 formal='+'.join(r'\frac{∂}{∂'+str(v)+'}('+tex(c)+')' for v,c in zip(VARS,cs))
 terms='+'.join('('+tex(d)+')' if d.could_extract_minus_sign() else tex(d) for d in ds)
 return r'\begin{aligned}\text{div}\,F & ='+formal+r' \\  & ='+terms+r' \\  & ='+tex(sum(ds))+r'.\end{aligned}'
THEOREM='Let $R$ be a simple solid region bounded by a closed surface $S$ with positive (outward) orientation. If a vector field $F$ has continuous partial derivatives for all its components in an open region in space that contains $R,$ then the divergence theorem states that\n\n$$\n'+r'{∬}_{S}F\cdot dS={∭}_{R}\text{div}\,F\,\text{d}V.'+'\n$$\n\nComputing the divergence of $F,$ we obtain\n\n$$\n'
def region(outer,inner):
 v,l,u=inner
 inequalities=[tex(a)+r'\le '+str(w)+r'\le '+tex(b) for w,a,b in outer]
 inequalities.append(tex(l)+r'\le '+str(v)+r'\le '+tex(u))
 return r'R=\left\{(x,y,z):\begin{array}{l}'+r' \\ '.join(inequalities)+r'\end{array}\right\}.'
def normal_solution(cs,outer,inner,easy):
 ds=partials(cs);d=sp.expand(sum(ds));s=THEOREM+derivative_block(cs,ds)+'\n$$\n\n'
 if easy:
  return s+'Let $R$ be the solid region enclosed by $S.$ Then, using the divergence theorem, we have\n\n$$\n'+r'\begin{aligned}{∬}_{S}F\cdot dS & ='+triple(d)+r' \\  & ='+integral(d,outer,inner)+r'.\end{aligned}'+'\n$$'
 label={x:'II',y:'III',z:'I'}[inner[0]]
 return s+'Therefore, using the divergence theorem, we have\n\n$$\n'+r'{∬}_{S}F\cdot dS='+triple(d)+',\n$$\n\nwhere $R$ is a type '+label+' solid region that can be written as\n\n$$\n'+region(outer,inner)+'\n$$\n\nAs a result,\n\n$$\n'+r'\begin{aligned}&'+triple(d)+r' \\ & ='+integral(d,outer,inner)+r'.\end{aligned}'+'\n$$'

def normal_prompt(cs,outer,inner,easy):
 planes=', '.join('$'+str(w)+'='+tex(bound)+'$' for w,a,b in outer for bound in (a,b))
 if easy:description='rectangular prism enclosed by the planes '+planes+', $'+str(inner[0])+'='+tex(inner[1])+'$, $'+str(inner[0])+'='+tex(inner[2])+'$'
 else:description='finite solid region enclosed by the planes '+planes+', and the surfaces $'+str(inner[0])+'='+tex(inner[1])+'$ and $'+str(inner[0])+'='+tex(inner[2])+'$'
 prompt='Let $S$ be the boundary of the '+description+'. Given that the surface $S$ is positively (outward) oriented and $F='+field_tex(cs)+'$, the flux of $F$ across $S$ can be written as\n\n$$\n'+r'{∬}_{S}F\cdot dS='
 if easy:prompt+=integral(sp.Symbol('MISSING'),outer,inner).replace('MISSING',r'\bbox[2pt,border: 1pt solid currentColor]{\phantom{AAAAA}}')+'.\n$$\n\nWhat is the missing part of the expression?'
 else:prompt+='\n$$'
 return prompt


def source_replay(template):
    """Immutable historical question, including defects; never learner output."""
    import copy
    return copy.deepcopy(source_q(template))


def instance(template, scale=1, shift=0, original=False, k=0, u=0, r=0):
    cfg=CONFIG[template]
    if type(scale) is not int or not 1<=scale<=9:
        raise ValueError('scale must be an integer in 1..9')
    if type(shift) is not int or not 0<=shift<=3 or (cfg['level']=='easy' and shift):
        raise ValueError('shift is 0 for easy, or an integer in 0..3 for moderate')
    for key,value,maximum in (('k',k,2),('u',u,2),('r',r,1)):
        if type(value) is not int or not 0<=value<=maximum or (cfg['level']=='easy' and value):
            raise ValueError(key+' outside supported domain')
    cs=tuple(sp.expand(scale*e) for e in cfg['components'])
    outer=cfg['outer']
    if template=='typeIIIbowl' and not original:
        outer=((x,0,1),(z,0,1))
    outer=((outer[0][0],outer[0][1],outer[0][2]-sp.Rational(r,2)),outer[1])
    inner=(cfg['inner'][0],sp.sympify(cfg['inner'][1])+shift,sp.sympify(cfg['inner'][2])+shift+u)
    if cfg['level']=='easy':
        choices=tuple(sp.expand(scale*e) for e in cfg['bank'])
    else:
        s=scale
        component_delta,integrands={
            'typeII':((k*x*y**2,0,0),(s*z+(3*s+2*k)*y,(s+k)*y**2,(s+k)*y**2,2*(s+k)*y+s,2*(s+k)*y+s)),
            'typeI':((0,-k*y,0),(2*s*x*z,s*x**2-s-k,s*(y+z-2)-k,s*(y+z-2)-k,s*x**2-s-k)),
            'typeIIIbowl':((0,0,k*x*y*z),(s*(x+y),(2*s+k)*x*y,3*s*y**2+(s+k)*x*y,3*s*y**2+(s+k)*x*y,(2*s+k)*x*y)),
            'typeIIIlinear':((0,-k*y,0),(3*s*z**2-4*s-k,3*s*z**2-4*s-k,s*(z**3-3)-k,s*z**2,s*(z**3-3)-k)),
            'typeIIlinear':((0,0,k*x*z),(3*s*x*z**2+(s+k)*z,(s+k)*x,3*s*x*z**2+(s+k)*z,(s+k)*x,(s+k)*x**2)),
        }[template]
        cs=tuple(sp.expand(c+delta) for c,delta in zip(cs,component_delta))
        choices=[]
        for d,(_,lo,hi) in zip(integrands,cfg['bank']):
            reversed_bounds=sp.expand(lo-cfg['inner'][2])==0 and sp.expand(hi-cfg['inner'][1])==0
            choices.append((sp.expand(d),sp.sympify(lo)+shift+(u if reversed_bounds else 0),
                            sp.sympify(hi)+shift+(0 if reversed_bounds else u)))
        choices=tuple(choices)
    return cs,outer,inner,choices


@lru_cache(maxsize=1024)
def integral_value(spec,outer,variable):
    d,l,u=spec
    result=sp.integrate(d,(variable,l,u))
    for w,a,b in reversed(outer):
        result=sp.integrate(result,(w,a,b))
    return sp.simplify(result)


def correct_position(template,cs,inner,choices):
    d=sp.expand(sum(partials(cs)))
    wanted=d if CONFIG[template]['level']=='easy' else (d,inner[1],inner[2])
    def same(a,b):
        if isinstance(a,tuple):return all(sp.simplify(v-w)==0 for v,w in zip(a,b))
        return sp.simplify(a-b)==0
    matches=[i for i,c in enumerate(choices) if same(c,wanted)]
    if len(matches)!=1:raise ValueError('bank must have exactly one correct setup')
    return matches[0]


def ordered_region(outer,inner):
    # Every supported gap is a sum of univariate quadratics plus a constant.
    gap=sp.expand(inner[2]-inner[1]);points=[{}]
    for w,lo,hi in outer:
        if lo>=hi:return False
        roots=sp.solve(sp.diff(gap,w),w)
        axis=[lo,hi]+[v for v in roots if v.is_real and not v.free_symbols and lo<=v<=hi]
        points=[p|{w:v} for p in points for v in axis]
    return min(gap.subs(p) for p in points)>=0


@lru_cache(maxsize=8192)
def eligible(template,shift,scale=1,k=0,u=0,r=0):
    cs,outer,inner,choices=instance(template,scale,shift,k=k,u=u,r=r)
    correct_position(template,cs,inner,choices)
    if not ordered_region(outer,inner):return False
    if CONFIG[template]['level']=='easy':
        return all(sp.simplify(a-b)!=0 for i,a in enumerate(choices) for b in choices[i+1:])
    values=[integral_value(c,outer,inner[0]) for c in choices]
    return len(set(values))==5


def parameter_candidates(level,rng):
    from itertools import product
    domain=[dict(zip(('s','h','k','u','r'),v)) for v in product(
        range(1,10),range(4) if level=='moderate' else [0],
        range(3) if level=='moderate' else [0],range(3) if level=='moderate' else [0],
        range(2) if level=='moderate' else [0])]
    rng.shuffle(domain)
    return domain


def valid_parameters(t,p):
    return eligible(t,p['h'],p['s'],p['k'],p['u'],p['r'])


@checked_math_content
def generate(level='moderate',seed=0,template=None,parameters=None):
    if level not in ('easy','moderate'):raise ValueError('unsupported difficulty: '+str(level))
    rng=random.Random(seed)
    names=[t for t,c in CONFIG.items() if c['level']==level]
    t=template if template is not None else rng.choice(names)
    if t not in names:raise ValueError('template/difficulty mismatch')
    if parameters is None:
        p=next((p for p in parameter_candidates(level,rng) if valid_parameters(t,p)),None)
        if p is None:raise ValueError('no eligible whole bank')
    else:
        p={'k':0,'u':0,'r':0}|dict(parameters)
        if set(p)!={'s','h','k','u','r'}:raise ValueError('parameters require s,h and optional k,u,r')
    cs,outer,inner,bank=instance(t,p['s'],p['h'],k=p['k'],u=p['u'],r=p['r'])
    if not valid_parameters(t,p):raise ValueError('whole bank collision or invalid region')
    correct_index=correct_position(t,cs,inner,bank)
    prompt=normalize_prose(normal_prompt(cs,outer,inner,level=='easy'))
    solution=normalize_prose(normal_solution(cs,outer,inner,level=='easy'))
    values=[normalize_tex(tex(e) if level=='easy' else integral(e[0],outer,(inner[0],e[1],e[2]))) for e in bank]
    prompt=_ca_problem(prompt);solution=_ca_prose(solution)
    identity=digest({'version':VERSION,'prompt':prompt,'solution':solution,'bank':sorted(values),'difficulty':level})
    field_id=uid(identity+':selection')
    answers=[{':answer/id':uid(field_id+':'+v),':answer/type':':answer.type/math',':answer/value':v} for v in values]
    correct=answers[correct_index][':answer/id']
    rng.shuffle(answers)
    question={':question/id':uid(identity),':question/difficulty':':question.difficulty/'+level,
              ':question/problem':prompt,':question/worked-solution':solution,
              ':question/answer-fields':[{':answer-field/id':field_id,':answer-field/key':'selection',
                 ':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,
                 ':answer-field/correct':[':answer/id',correct]}]}
    d=sp.expand(sum(partials(cs)))
    task={'divergence':str(d),'level':level}
    if level=='moderate':task.update(outer=str(outer),inner=str(inner))
    return {'knowledge_point':{'db_id':KP_ID,'id':KP[':knowledge-point/id'],'title':KP[':knowledge-point/title']},
            'question':question,'generation':{'version':VERSION,'seed':seed,'template':t,
              'profile':'source_bank_'+source_q(t)[':question/math-academy-id'],
              'parameters':p,'source_ids':[source_q(t)[':question/math-academy-id']],
              'source':{k:SNAPSHOT[k] for k in ('database','basis','lineage')},
              'source_difficulty':source_q(t).get(':question/difficulty'),
              'mathematical_fingerprint':digest(task),'eligible_for_learning':True,
              'repairs':['positive_x_projection'] if t=='typeIIIbowl' else (['inferred_key_solution_and_easy_band'] if t=='legacy' else []),
              'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__}}}


def generate_batch(level,count,seed):
    if count<0:raise ValueError('count must be nonnegative')
    names=[t for t,c in CONFIG.items() if c['level']==level]
    if not names:raise ValueError('unsupported difficulty: '+str(level))
    maximum=len(names)*(648 if level=='moderate' else 9)
    if count>maximum:raise ValueError('count exceeds parameter domain')
    rng=random.Random(seed);rng.shuffle(names)
    domains={t:iter(parameter_candidates(level,rng)) for t in names}
    records=[];seen=set()
    while domains and len(records)<count:
        for t in list(domains):
            for p in domains[t]:
                if not valid_parameters(t,p):continue
                record=generate(level,seed+len(records),t,p)
                fingerprint=record['generation']['mathematical_fingerprint']
                if fingerprint in seen:continue
                seen.add(fingerprint);records.append(record);break
            else:del domains[t]
            if len(records)==count:break
    if len(records)<count:raise ValueError('count exceeds distinct semantic domain')
    return records



if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--difficulty',choices=('easy','moderate','hard'),default='moderate')
    parser.add_argument('--count',type=int,default=5)
    parser.add_argument('--seed',type=int,default=0)
    parser.add_argument('--format',choices=('json',),default='json')
    args=parser.parse_args()
    try:records=generate_batch(args.difficulty,args.count,args.seed)
    except ValueError as error:parser.error(str(error))
    print(json.dumps(records,ensure_ascii=False,indent=2))
