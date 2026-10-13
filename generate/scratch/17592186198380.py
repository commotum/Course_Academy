#!/usr/bin/env python3
"""Exact rectangular parametric flux generators; no database or plotting code.

Observed recipes keep their fixed polynomial geometry and field and vary rectangle
bounds. Source LaTeX lexemes are formatting aliases for independently computed
expressions, never answer lookups. Ten original scalar banks remain explicitly
named empirical replay profiles: wrong values are constant areal densities.
Their error intent is unresolved, so normal generation uses complete authored
operation banks. See the evidence folder for provenance and limitations.
"""
from __future__ import annotations
import argparse, hashlib, json, random, re, uuid
from pathlib import Path
import sympy as sp

ROOT=Path(__file__).resolve().parent/'17592186198380'
KP_ID=17592186198380
KP_UUID='f322cca7-7530-50bf-b262-89faa81f5906'
TITLE='Evaluating Flux Through a Surface'
VERSION='flux-rectangular-1'
u,v,x,y,z=sp.symbols('u v x y z', real=True)
SYMBOLS={s.name:s for s in (u,v,x,y,z)}
DATA=json.loads((ROOT/'extraction.json').read_text())
TEMPLATES={k:d['level'] for k,d in DATA.items()}
TEMPLATES.update({'easy_affine_hint':'easy'})
PROFILES=('authored_primitive','authored_weighted','authored_rectangle')

class SampleRejected(ValueError): pass

def expr(s): return sp.sympify(s,locals=SYMBOLS)
def tex(s): return sp.latex(sp.simplify(s))
def block(s): return '$$\n'+s+'\n$$'
def vec(a): return '⟨'+r',\,'.join(tex(e) for e in a)+'⟩'
def digest(d): return hashlib.sha256(json.dumps(d,sort_keys=True).encode()).hexdigest()
def exact_bounds(p):
    if set(p)!={'u_min','u_max','v_min','v_max'}: raise ValueError('Expected exactly four rectangle bounds')
    out={k:expr(str(t)) for k,t in p.items()}
    if any(not t.is_Rational or abs(t)>6 for t in out.values()): raise ValueError('Bounds must be rational with magnitude <= 6')
    if out['u_min']>=out['u_max'] or out['v_min']>=out['v_max']: raise ValueError('Rectangle has nonpositive area')
    return out

def evaluate(name,p):
    if name=='easy_affine_hint':
        # Canonical affine field/geometry; supplied vector removes cross-product workload.
        r=sp.Matrix([1+2*u+v,u+v,u-v]); F=sp.Matrix([z,x,y])
    else:
        d=DATA[name];r=sp.Matrix([expr(t) for t in d['r']]);F=sp.Matrix([expr(t) for t in d['F']])
    ru=r.diff(u);rv=r.diff(v);normal=ru.cross(rv)
    composed=F.subs(dict(zip((x,y,z),r)),simultaneous=True).applyfunc(sp.expand)
    f=sp.expand(composed.dot(normal))
    ul,ur,vl,vr=(p[k] for k in ('u_min','u_max','v_min','v_max'))
    integ=lambda g:sp.integrate(g,(u,ul,ur),(v,vl,vr))
    C=sp.simplify(integ(f));area=(ur-ul)*(vr-vl)
    return {'r':r,'F':F,'ru':ru,'rv':rv,'normal':normal,'composed':composed,'f':f,'correct':C,'area':area,'integrate':integ}

def alias(value,original,original_value):
    """Source spelling is retained only if it represents this calculated value."""
    return original if sp.simplify(value-expr(original_value))==0 else tex(value)

def integral(var,lo,hi,body,space=True):
    return r'{\int }_{'+tex(lo)+'}^{'+tex(hi)+'}'+body+(r'\,\text{d}' if space else r'\text{d}')+str(var)

def source_solution(name,p,m):
    d=DATA[name];factor=expr(d['factor']);g=sp.expand(m['f']/factor)
    inner=u if d['inner']=='u' else v;outer=v if inner==u else u
    il,ih=p[str(inner)+'_min'],p[str(inner)+'_max'];ol,oh=p[str(outer)+'_min'],p[str(outer)+'_max']
    primitive=sp.integrate(g,inner)
    reduced=sp.expand(primitive.subs(inner,ih)-primitive.subs(inner,il))
    outer_primitive=sp.integrate(reduced,outer)
    terms=[sp.expand(term.subs(outer,oh)-term.subs(outer,ol)) for term in sp.Add.make_args(outer_primitive)]
    result=sp.simplify(factor*sum(terms))
    # Slots are mathematical calculations; source expression spellings remain aliases.
    a=lambda key,value:alias(value,d['aliases'][key]['tex'],d['aliases'][key]['expr'])
    slots={k:tex(value) for k,value in p.items()}
    slots.update({'reduced':a('reduced',reduced),'outer_primitive':a('outer_primitive',outer_primitive),
                  'correct':a('correct',result), 'width_u':tex(p['u_max']-p['u_min']),
                  'width_v':tex(p['v_max']-p['v_min'])})
    kind=d['evaluation']
    if kind=='terms':
        # Addends retain the source ordering, checked independently against total.
        slots['evaluation']=d['evaluation_tex'] if p=={k:expr(str(t)) for k,t in d['bounds'].items()} else sum_tex(terms,factor)
    elif kind=='separable_v':
        ev=sp.integrate(g,(v,p['v_min'],p['v_max']))
        slots['evaluation']=tex(p['u_max']-p['u_min'])+r'\cdot '+tex(ev)
    elif kind=='separable_uv':
        eu=sp.integrate(u,(u,p['u_min'],p['u_max']));ev=sp.integrate(v,(v,p['v_min'],p['v_max']))
        slots['evaluation']=tex(factor)+'('+tex(eu)+')('+tex(ev)+')'
    final=d['final_template']
    for key,value in slots.items(): final=final.replace('<<'+key+'>>',value)
    if '<<' in final: raise AssertionError('Unexpanded solution slot')
    return d['prefix']+final,{'inner':str(inner),'factor':str(factor),'primitive':str(primitive),
        'reduced':str(reduced),'outer_primitive':str(outer_primitive),'evaluated_terms':[str(t) for t in terms]}

def sum_tex(values,factor=sp.Integer(1)):
    s=''
    for value in values:
        if not s: s=tex(value)
        elif value>=0:s+='+'+tex(value)
        else:s+=tex(value)
    return s if factor==1 else tex(factor)+'('+s+')'

def easy_solution(p,m):
    f=m['f'];P=sp.integrate(f,v);R=sp.integrate(f,(v,p['v_min'],p['v_max']));Q=sp.integrate(R,u)
    intro=DATA['q-161278']['prefix'].split("We first compute")[0]
    solution=intro+"We're given that the fundamental vector product for our surface is\n\n"+block(r"{r}_{u}^{′}\times {r}_{v}^{′}="+vec(m['normal'])+'.')
    solution+='\n\nNext, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$\n\n'+block(r'F(r(u,v))='+vec(m['composed']))
    solution+='\n\nThen, we calculate the dot product of $F$ and ${r}_{u}^{′}\\times {r}_{v}^{′}:$\n\n'+block(vec(m['composed'])+r'\cdot '+vec(m['normal'])+'='+tex(f))
    solution+='\n\nTherefore, the surface integral evaluates to\n\n'+block(r'\begin{aligned}{∬}_{S}F\cdot \text{d}S & ='+integral(u,p['u_min'],p['u_max'],integral(v,p['v_min'],p['v_max'],'('+tex(f)+')'))+r' \\ & ='+integral(u,p['u_min'],p['u_max'],'['+tex(P)+']_{v='+tex(p['v_min'])+'}^{v='+tex(p['v_max'])+'}')+r' \\ & ='+integral(u,p['u_min'],p['u_max'],'('+tex(R)+')')+r' \\ & =['+tex(Q)+']_{'+tex(p['u_min'])+'}^{'+tex(p['u_max'])+'}'+r' \\ & ='+tex(m['correct'])+r'.\end{aligned}')
    return solution,{'inner':'v','factor':'1','primitive':str(P),'reduced':str(R),'outer_primitive':str(Q)}

def bank(name,profile,p,m):
    C=m['correct'];f=m['f'];I=m['integrate'];ul,ur,vl,vr=(p[k] for k in ('u_min','u_max','v_min','v_max'))
    if profile.startswith('observed:'):
        if profile!='observed:'+name or name not in DATA:raise ValueError('Profile does not own this template')
        d=DATA[name];source_area=expr(d['source_area'])
        # Empirical replay density, not a recovered error operation. Never default.
        values=[C]+[expr(w['value'])*m['area']/source_area for w in d['wrong']]
        labels=['correct']+['unresolved_observed_area_density:'+str(i) for i in range(4)]
    elif profile=='authored_weighted':
        values=[C,-C,I(u*f),I(v*f),I(u*v*f)]
        labels=['correct','reversed_cross_product','erroneous_u_measure','erroneous_v_measure','erroneous_uv_measure']
    elif profile=='authored_primitive':
        no_div=sum(c*(ur**(i+1)-ul**(i+1))*(vr**(j+1)-vl**(j+1)) for (i,j),c in sp.Poly(f,u,v).terms())
        shifted_div=sum(c*(ur**(i+1)-ul**(i+1))*(vr**(j+1)-vl**(j+1))/((i+2)*(j+2)) for (i,j),c in sp.Poly(f,u,v).terms())
        values=[C,-C,no_div,shifted_div,I(f*m['normal'].dot(m['normal']))]
        labels=['correct','reversed_cross_product','omitted_antiderivative_divisors','divisors_one_too_large','extra_squared_surface_jacobian']
    elif profile=='authored_rectangle':
        no_div=sum(c*(ur**(i+1)-ul**(i+1))*(vr**(j+1)-vl**(j+1)) for (i,j),c in sp.Poly(f,u,v).terms())
        quarter=m['area']*f.subs({u:ul+(ur-ul)/4,v:vl+(vr-vl)/4})
        values=[C,-C,m['area']*f.subs({u:ul,v:vl}),m['area']*f.subs({u:ur,v:vr}),quarter]
        labels=['correct','reversed_cross_product','lower_corner_rectangle','upper_corner_rectangle','quarter_point_rectangle']
    else:raise ValueError('Unknown bank profile')
    values=list(map(sp.simplify,values))
    if any(t.free_symbols or t.is_real is not True for t in values):raise SampleRejected('Nonreal/nonscalar option')
    if len(set(values))!=5:raise SampleRejected('Whole bank rejected: equivalent or correct distractor')
    return values,labels

def prompt(name,p,m):
    if name in DATA:
        out=DATA[name]['prompt_template']
        for key,value in p.items():out=out.replace('<<'+key+'>>',tex(value))
        return out
    return 'Evaluate the surface integral\n\n'+block('{∬}_{S}'+vec(m['F'])+r'\cdot \text{d}S')+'\n\nwhere the parametric surface $S$ is defined by\n\n'+block('r(u,v)='+vec(m['r']))+'\n\nover the domain $D={(u,v)\\,:\\,'+tex(p['u_min'])+r'\le u\le '+tex(p['u_max'])+r',\,'+tex(p['v_min'])+r'\le v\le '+tex(p['v_max'])+'}.$\n\n*Hint: You can use the fact that ${r}_{u}^{′}\\times {r}_{v}^{′}='+vec(m['normal'])+'.$*'

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ('easy','moderate','hard'):raise ValueError('Unknown difficulty')
    if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Only radio fields are supported')
    rng=random.Random(seed)
    if template is None and profile and profile.startswith('observed:'):template=profile.split(':',1)[1]
    if template is None:template=rng.choice([k for k,l in TEMPLATES.items() if l==level])
    if template not in TEMPLATES or TEMPLATES[template]!=level:raise ValueError('Template is outside this difficulty')
    profile=profile or rng.choice(PROFILES) # Pick a complete bank BEFORE sampling.
    for attempt in range(300):
        if parameters is not None:p=exact_bounds(parameters)
        elif profile.startswith('observed:'):
            p=exact_bounds(DATA[template]['bounds'])
        else:
            # Translated short integer rectangles vary the same integration task.
            # Choose the full interval pair before constructing the complete bank.
            ul=rng.randint(-3,2);vl=rng.randint(-2,2)
            if template in ('q-161260','q-161263'):vl=rng.randint(0,2)
            if template in ('q-161273','q-161283'):ul=rng.randint(0,2);vl=rng.randint(0,2)
            ur=ul+rng.randint(1,4);vr=vl+rng.randint(1,4)
            if template=='q-161262':ul=-rng.randint(1,4);ur=0;vl=0;vr=rng.randint(1,4)
            p=exact_bounds({'u_min':ul,'u_max':ur,'v_min':vl,'v_max':vr})
        if template in ('q-161260','q-161263') and p['v_min']<0:raise ValueError('This template retains a nonnegative v domain')
        if template in ('q-161273','q-161283') and (p['u_min']<0 or p['v_min']<0):raise ValueError('This template retains nonnegative u and v domains')
        if template=='q-161262' and (p['u_max']!=0 or p['v_min']!=0):raise ValueError('This template retains u_max=0 and v_min=0')
        m=evaluate(template,p)
        try:values,labels=bank(template,profile,p,m)
        except SampleRejected:
            if parameters is not None or profile.startswith('observed:'):raise
            continue
        break
    else:raise SampleRejected('This whole bank has no valid sampled instance')
    solution,steps=source_solution(template,p,m) if template in DATA else easy_solution(p,m)
    pp={k:str(t) for k,t in p.items()};parameter_key=digest({'template':template,'parameters':pp})
    problem=prompt(template,p,m)
    content_key=digest({'parameters':parameter_key,'problem':problem,'solution':solution,'bank':sorted(map(str,values))})
    qid=uuid.uuid5(uuid.NAMESPACE_URL,f'flux/{KP_UUID}/{VERSION}/{content_key}');fid=uuid.uuid5(qid,'selection')
    choices=[];metadata={}
    for value,label in zip(values,labels):
        aid=str(uuid.uuid5(fid,'math:'+str(value)))
        # Preserve exact scalar source spelling when it is the same computed value.
        vt=tex(value)
        if template in DATA and profile.startswith('observed:'):
            for aa in DATA[template]['bank']:
                if expr(aa['value'])==value:vt=aa['tex'];break
        choices.append({':answer/id':aid,':answer/type':':answer.type/math',':answer/value':vt})
        metadata[aid]={'recipe':label,'value':str(value)}
        if label=='correct':correct_id=aid
    rng.shuffle(choices)
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},
        'question':{':question/id':str(qid),':question/difficulty':':question.difficulty/'+level,':question/problem':problem,
            ':question/worked-solution':solution,':question/answer-fields':[{':answer-field/id':str(fid),':answer-field/key':'selection',
                ':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',correct_id]}]},
        'generation':{'version':VERSION,'sympy_version':sp.__version__,'seed':seed,'template':template,'parameters':pp,
            'parameter_fingerprint':parameter_key,'content_fingerprint':content_key,'bank_profile':profile,
            'bank_origin':'observed_empirical_replay' if profile.startswith('observed:') else 'authored',
            'authored_extension':not profile.startswith('observed:'),'plot_rating':'none','plot_assets':{},
            'source_analysis':{'database':'math','basis':1356,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1','question_ids':[template] if template in DATA else [],'canonical':'e-12358'},
            'orientation':'r_u cross r_v','domain':'rectangle','math':{key:[str(t) for t in value] if isinstance(value,sp.MatrixBase) else str(value) for key,value in m.items() if key!='integrate'},
            'solution_steps':steps,'answer_recipes':metadata}}

# Easy: authored full evaluation, canonical affine geometry, supplied normal.
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
# Moderate: four hinted templates and the observed unhinted curved template.
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
# Hard: observed full derivative/cross-product/substitution/integration sequences.
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)

def markdown(record):
    q=record['question'];g=record['generation'];f=q[':question/answer-fields'][0]
    return f"### {g['template']} / {g['bank_profile']}\n\n"+q[':question/problem']+'\n\n'+ '\n'.join('- $'+a[':answer/value']+'$'+(' (correct)' if a[':answer/id']==f[':answer-field/correct'][1] else '') for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']+'\n'

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');ns=ap.parse_args()
    if ns.count<1:ap.error('count must be positive')
    levels=['easy','moderate','hard'] if ns.difficulty=='all' else [ns.difficulty]
    records=[generate(l,ns.seed+i,template=ns.template,profile=ns.profile) for l in levels for i in range(ns.count)]
    print(json.dumps(records,indent=2,ensure_ascii=False) if ns.format=='json' else '\n'.join(map(markdown,records)))
if __name__=='__main__':main()
