#!/usr/bin/env python3
"""Level-surface normal vectors; steps 3–7 only, no database access.

Twelve observed easy families retain their complete ordered five-stage solutions.
Public raw_q-* profiles parameterize the original opaque banks as documented
component scaling patterns, preserve all legacy fields and absent attributes,
and are evidence-only. Normal practice uses a complete method-derived omission
bank, rejecting the whole bank whenever the requested normal criterion is
ambiguous. Missing moderate/hard are authored workload designs, not source labels.
"""
from __future__ import annotations
import argparse, copy, hashlib, json, random, re, sys, uuid
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
KP_ID=17592186124463
KP_UUID='4516cb28-0fc0-5c15-b9b2-747c3827e189'
TITLE='Finding a Normal Vector to a Level Surface'
VERSION='surface-normal-1'
DIR=Path(__file__).with_suffix('')
SOURCE=json.loads((DIR/'source.json').read_text())
QUESTIONS={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
x,y,z=sp.symbols('x y z',real=True)
VARS=(x,y,z)
TRANS=standard_transformations+(implicit_multiplication_application,)
class Rejected(ValueError): pass

def scalar(s):
    """Read complete displayed scalar TeX, without dependence on generation data."""
    s=s.replace('\u2061','').replace(r'\operatorname{ln}',r'\ln')
    s=re.sub(r'\\(?:left|right|,|;|!|:|quad|cdot|text\{[^}]*\})','',s)
    def group(t,i):
        if i>=len(t) or t[i]!='{': raise ValueError('Expected complete TeX group: '+t[i:])
        n=1;j=i+1
        while n:
            if j>=len(t):raise ValueError('Unbalanced TeX')
            n+=(t[j]=='{')-(t[j]=='}');j+=1
        return t[i+1:j-1],j
    def expand(t):
        out='';i=0
        while i<len(t):
            if t.startswith(r'\frac',i) or t.startswith(r'\dfrac',i):
                i+=6 if t.startswith(r'\dfrac',i) else 5
                a,i=group(t,i);b,i=group(t,i);out+='(('+expand(a)+')/('+expand(b)+'))'
            elif t.startswith(r'\sqrt',i):
                i+=5;a,i=group(t,i);out+='sqrt('+expand(a)+')'
            elif t.startswith(r'\ln',i):out+='log';i+=3
            elif t[i]=='{':a,i=group(t,i);out+='('+expand(a)+')'
            else:out+=t[i];i+=1
        return out
    s=expand(s).replace('^','**')
    return parse_expr(s,local_dict={'x':x,'y':y,'z':z,'e':sp.E,'sqrt':sp.sqrt,'log':sp.log},transformations=TRANS)

def vector_parts(s):
    clean=re.sub(r'\\text\{[^}]*\}', '', s).replace('\xa0','')
    clean=re.sub(r'\\(?:left|right)', '', clean)
    clean=clean.replace(r'\,','').replace(r'\ ','').replace(' ','')
    chunks=[];last=0
    for m in re.finditer('[ijk]',clean):
        coeff=clean[last:m.start()]; coeff=coeff if coeff not in ('','+','-') else coeff+'1'
        chunks.append((m.group(),scalar(coeff)));last=m.end()
    if last!=len(clean) or not chunks:raise ValueError('Unconsumed vector notation '+s)
    return chunks

def vector(s):
    out=[sp.S.Zero]*3
    for basis,c in vector_parts(s):out['ijk'.index(basis)]+=c
    return sp.Matrix(out)

def tex(a):return sp.latex(sp.expand(sp.sympify(a).rewrite(sp.exp)),ln_notation=True)

def coefficient_tex(a):
    t=tex(a)
    return r'\left('+t+r'\right)' if sp.expand(sp.sympify(a).rewrite(sp.exp)).is_Add else t

def vtex(v):
    result=''
    for c,b in zip(v,'ijk'):
        if c==0:continue
        negative=c.could_extract_minus_sign();a=-c if negative else c
        term=('' if a==1 else coefficient_tex(a)+r'\,')+b
        result+=('-' if negative else '+' if result else '')+term
    return result or '0'

def render_like(v,original):
    """Parameterized coefficients with each source's basis/spacing/explicit-1 masks."""
    result='';last=0
    for m in re.finditer('[ijk]',original):
        prefix=original[last:m.start()]; last=m.end()
        b=m.group(); old=vector_parts(prefix+b)[0][1]; c=v['ijk'.index(b)]
        # Retain the exact source coefficient notation at ANY equal scalar,
        # not a source-question payload shortcut; changed scalars use same mask.
        spacing=re.search(r'(\\,|\s*)$',prefix).group()
        compact=prefix.strip().removesuffix(r'\,').strip()
        old_sign='-' if compact.startswith('-') else '+' if compact.startswith('+') else ''
        bare=compact.lstrip('+-').strip()
        sign='-' if c.could_extract_minus_sign() else '+' if result else ''
        a=-c if c.could_extract_minus_sign() else c
        if sp.simplify(c-old)==0: result+=prefix+b;continue
        explicit_one=bare not in ('',)
        coeff=coefficient_tex(a) if a!=1 or explicit_one else ''
        lead=' ' if prefix.startswith(' ') else ''
        trail=' ' if compact.startswith(('+ ','- ')) else ''
        result+=lead+sign+trail+coeff+spacing+b
    if last!=len(original):raise ValueError('Source vector mask not fully consumed')
    present={b for b,_ in vector_parts(original)}
    missing=sp.Matrix([v[i] if b not in present else 0 for i,b in enumerate('ijk')])
    if missing!=sp.zeros(3,1):
        extra=vtex(missing);result+=('' if extra.startswith('-') else '+')+extra
    return result

# Complete scalar coordinates, not blind substring replacement.
POINTS={'q-37570':[1,-1,2],'q-65167':[1,-1,1],'q-131115':[1,4,1],
'q-65168':[-1,1,-1],'q-71403':[3,4,0],'q-71404':[1,-2,0],
'q-131119':[0,0,1],'q-131117':[1,-2,1],'q-131116':[1,-1,-1],
'q-71396':[-1,0,1],'q-71399':[0,0,0],'q-71397':[-2,-3,1]}
# All observed substituted-component masks. The extra ) in q-65168 is raw evidence.
EVAL={
'q-37570':r'({Y}+5)\,i+({X})\,j+2({Z})\,k',
'q-65167':r'({Y})^{{2}}\,i+(2({X})({Y})-2({Z}))\,j+(-2({Y})+1)\,k',
'q-131115':r'\frac{{{Y}}}{{2\sqrt{{{X}({Y})}}}}\,i+(\frac{{{X}}}{{2\sqrt{{{X}({Y})}}}}+\frac{{{Z}}}{{2\sqrt{{{Y}({Z})}}}})j+\frac{{{Y}}}{{2\sqrt{{{Y}({Z})}}}}\,k',
'q-65168':r'(({Y})^{{2}}+2({X})({Z}))\,i+(2({X})({Y})+({Z})^{{2}}))\,j+(2({Y})({Z})+({X})^{{2}})\,k',
'q-71403':r'\frac{{{X}}}{{\sqrt{{({X})^{{2}}+({Y})^{{2}}+({Z})^{{2}}}}}}\,i+\frac{{{Y}}}{{\sqrt{{({X})^{{2}}+({Y})^{{2}}+({Z})^{{2}}}}}}\,j+\frac{{{Z}}}{{\sqrt{{({X})^{{2}}+({Y})^{{2}}+({Z})^{{2}}}}}}\,k',
'q-71404':r'-\frac{{({Y})}}{{({Z})^{{2}}-({X})({Y})}}\,i+(-\frac{{{X}}}{{({Z})^{{2}}-({X})({Y})}}-{Z})\,j+(\frac{{2({Z})}}{{({Z})^{{2}}-({X})({Y})}}-({Y}))\,k',
'q-131119':r'({{e}}^{{{Y}}}+({Z}){{e}}^{{{X}}})i+(({X}){{e}}^{{{Y}}}+{{e}}^{{{Z}}})j+(({Y}){{e}}^{{{Z}}}+{{e}}^{{{X}}})k',
'q-131117':r'(3({X})^{{2}}({Y})({Z})-({Y})({Z})^{{2}})\,i+(({X})^{{3}}({Z})-({X})({Z})^{{2}})\,j+(({X})^{{3}}({Y})-2({X})({Y})({Z}))\,k',
'q-131116':r'3({X})^{{2}}\,i+2({Z})^{{2}}({Y})\,j+(2({Z})({Y})^{{2}}+2)k',
'q-71396':r'2({X})\,i+2({Y})\,j+2({Z})\,k',
'q-71399':r'({{e}}^{{{X}+{Y}+{Z}}}+1)\,i+({{e}}^{{{X}+{Y}+{Z}}}+1)\,j+({{e}}^{{{X}+{Y}+{Z}}}+1)\,k',
'q-71397':r'(4({X})-({Y}))\,i-({X})\,j+2({Z})\,k'}

FUNCTION_TEX={k:re.search(r'f\(x,y,z\)=(.*?)\$',q[':question/problem']).group(1).rstrip(',') for k,q in QUESTIONS.items()}
FUNCTIONS={k:scalar(t) for k,t in FUNCTION_TEX.items()}
TEMPLATES={k:{'level':'easy','source':k} for k in QUESTIONS}
TEMPLATES.update({'weighted_quadratic':{'level':'moderate','source':None},'rational_quadratic':{'level':'hard','source':None}})
PROFILES={**{'raw_'+k:{'template':k,'evidence_only':True} for k in QUESTIONS},**{'method_'+k:{'template':k,'evidence_only':False} for k in TEMPLATES}}

def point_tex(p):return ','.join(tex(a) for a in p)

def deriv(f,p):
    partials=[sp.diff(f,a) for a in VARS]
    values=sp.Matrix([sp.simplify(a.subs(dict(zip(VARS,p)))) for a in partials])
    if any(a.is_real is not True or not a.is_finite for a in values) or values==sp.zeros(3,1):raise Rejected('Undefined or zero gradient')
    c=sp.simplify(f.subs(dict(zip(VARS,p))))
    if c.is_real is not True or not c.is_finite:raise Rejected('Point outside function domain')
    return partials,values,c

def source_solution(k,p,g,raw):
    q=QUESTIONS[k];w=q[':question/worked-solution'];pt=point_tex(p);old=point_tex(POINTS[k])
    a,b=w.split(r'\begin{aligned}');body,c=b.split(r'\end{aligned}')
    rows=body.split(r'\\');orig_final=rows[4].split('=',1)[1]
    slots=dict(zip(('X','Y','Z'),map(tex,p)))
    if k=='q-71399':slots={key:('('+value+')' if value.startswith('-') else value) for key,value in slots.items()}
    if k=='q-71404' and p[2]<0:slots['Z']='('+slots['Z']+')'
    rows[3]=' ∇f('+pt+') & ='+EVAL[k].format(**slots)+' '
    rows[4]='  & ='+render_like(g,orig_final)
    w=a+r'\begin{aligned}'+r'\\'.join(rows)+r'\end{aligned}'+c
    # Complete tuple/function-argument slots throughout prose, including conclusion.
    w=w.replace('('+old+')','('+pt+')')
    conclusion=re.search(r'Therefore, \$(.*?)\$',w).group(1)
    w=w.replace('Therefore, $'+conclusion+'$', 'Therefore, $'+render_like(g,conclusion)+'$')
    if not raw:
        w=w.replace(r'\sqrt{yz}+',r'\sqrt{yz}')
        w=w.replace('^{2}))\\,j','^{2})\\,j')
        if k=='q-131117':w=w.replace('(1,-1,2):$', '('+pt+'):$')
    return w

def normalized(o):
    if isinstance(o,list):return [normalized(v) for v in o]
    if isinstance(o,dict):
        if set(o)=={':db/ident'}:return o[':db/ident']
        return {k:([':answer/id',v[':answer/id']] if k==':answer-field/correct' else normalized(v)) for k,v in o.items()}
    return o

def uid(s):return str(uuid.uuid5(uuid.NAMESPACE_URL,str(s)))

def guard(level,p,template,raw=False):
    if set(p)!=({'point'} if template in QUESTIONS else {'point','coefficients'}):raise ValueError('Unexpected or missing parameters')
    point=[sp.sympify(a) for a in p['point']]
    if len(point)!=3 or any(a.is_real is not True for a in point):raise ValueError('Three real point coordinates required')
    if raw:
        if any(a.is_Rational is not True or abs(a)>6 for a in point):raise ValueError('Evidence point bounds: rational magnitudes <=6')
    elif level=='easy':
        if any(a.is_Integer is not True or abs(a)>(9 if template=='q-131115' else 4) for a in point):raise ValueError('Easy integer coordinates bounded by 4')
        if template=='q-131119' and any(abs(a)>1 for a in point):raise ValueError('Exponential easy coordinates -1..1')
        if template=='q-71403' and sp.sqrt(sum(a*a for a in point)).is_Integer is not True:raise ValueError('Radial easy requires a perfect-square radicand')
        if template=='q-131115' and (any(a<=0 for a in point) or any(sp.sqrt(a).is_Rational is not True for a in (point[0]*point[1],point[1]*point[2]))):raise ValueError('Root-product easy requires positive perfect-square products')
    else:
        c=[sp.sympify(a) for a in p['coefficients']]
        if len(c)!=6 or any(a.is_Integer is not True or not 1<=abs(a)<=3 for a in c):raise ValueError('Six nonzero integer coefficients of magnitude 1..3')
        if level=='moderate' and any(a.is_Integer is not True or not 2<=abs(a)<=3 for a in point):raise ValueError('Moderate nonunit integer coordinates of magnitude 2..3')
        if level=='hard' and any(a.is_Rational is not True or a.q not in (2,3) or not 1<=abs(a)<=3 for a in point):raise ValueError('Hard nonintegral rational coordinates, denominator 2 or 3, magnitude 1..3')
    return point

def sample(level,k,rng):
    if k in QUESTIONS:
        if k=='q-131115':pt=[rng.choice([1,4,9]),rng.choice([1,4,9]),rng.choice([1,4,9])]
        elif k=='q-71403':pt=list(rng.choice([(1,2,2),(2,1,2),(2,2,1),(2,4,4),(4,2,4),(4,4,2)]));pt=[a*rng.choice([-1,1]) for a in pt];pt=[a if abs(a)<=4 else a//2 for a in pt]
        else:pt=[rng.randint(-1,1) if k=='q-131119' else rng.randint(-4,4) for _ in range(3)]
        return {'point':pt}
    return {'point':[rng.choice([-3,-2,2,3]) if level=='moderate' else str(rng.choice([sp.Rational(a,b) for b in (2,3) for a in range(-9,10) if 1<=abs(sp.Rational(a,b))<=3 and sp.Rational(a,b).q==b])) for _ in range(3)],'coefficients':[rng.choice([-3,-2,-1,1,2,3]) for _ in range(6)]}

def method_bank(g):
    # A complete operation bank chosen BEFORE coordinates: omit computed partial
    # contributions. All must exist; no replacement or pooled first-valid errors.
    vs=[g,sp.Matrix([0,g[1],g[2]]),sp.Matrix([g[0],0,g[2]]),sp.Matrix([g[0],g[1],0]),sp.Matrix([0,0,g[2]])]
    return vs

def parallel(a,b):return a!=sp.zeros(3,1) and all(sp.simplify(v)==0 for v in a.cross(b))

def eligible(v,g,criterion='normal'):
    if criterion=='gradient':return all(sp.simplify(a-b)==0 for a,b in zip(v,g))
    return parallel(v,g) and (criterion!='unit_normal' or sp.simplify(v.dot(v)-1)==0)

def authored_solution(f,ft,p,partials,g):
    pt=point_tex(p)
    formal='+'.join(r'\frac{\partial}{\partial '+str(a)+'}('+ft+r')\,'+b for a,b in zip(VARS,'ijk'))
    pv='+'.join('('+tex(d)+r')\,'+b for d,b in zip(partials,'ijk'))
    ev='+'.join('('+substitute_tex(tex(d),p)+r')\,'+b for d,b in zip(partials,'ijk'))
    return 'A normal vector to the level surface that passes through the point where $(x,y,z)=('+pt+')$ can be found by computing \n$∇f('+pt+').$ \n\nSo, we first find the gradient and evaluate it at $(x,y,z)=('+pt+'):$\n\n$$\n'+r'\begin{aligned}∇f(x,y,z) & ={f}_{x}(x,y,z)\,i+{f}_{y}(x,y,z)\,j+{f}_{z}(x,y,z)\,k \\  & ='+formal+r' \\  & ='+pv+r' \\ ∇f('+pt+r') & ='+ev+r' \\  & ='+vtex(g)+r'\end{aligned}'+'\n$$\n\nTherefore, $'+vtex(g)+'$ is perpendicular to the level surface that passes through the point where $(x,y,z)=('+pt+').$'

def substitute_tex(s,p):
    # Token construction protects command names but permits grouped arguments.
    return re.sub(r'\\[A-Za-z]+|[xyz]',lambda m:m.group() if m.group().startswith('\\') else r'\left('+tex(p['xyz'.index(m.group())])+r'\right)',s)

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ('easy','moderate','hard') or field_type not in (None,'radio'):raise ValueError('Only easy/moderate/hard radio records supported')
    if profile:
        if profile not in PROFILES:raise ValueError('Unknown profile')
        implied=PROFILES[profile]['template']
        if template and template!=implied:raise ValueError('Profile/template mismatch')
        template=implied
    names=[k for k,v in TEMPLATES.items() if v['level']==level]
    if template and template not in names:raise ValueError('Wrong template level')
    rng=random.Random(seed);k=template or rng.choice(names)
    profile=profile or 'method_'+k;raw=PROFILES[profile]['evidence_only']
    for _ in range(1000):
        pp=copy.deepcopy(parameters) if parameters is not None else sample(level,k,rng)
        try:
            p=guard(level,pp,k,raw)
            if k in QUESTIONS:f=FUNCTIONS[k];ft=FUNCTION_TEX[k]
            else:
                a,b,c,d,e,h=map(sp.sympify,pp['coefficients']);f=a*x*x+b*y*y+c*z*z+d*x*y+e*y*z+h*x*z;ft=tex(f)
            partials,g,c=deriv(f,p)
            if k in QUESTIONS:
                q=normalized(copy.deepcopy(QUESTIONS[k]));old=point_tex(POINTS[k]);pt=point_tex(p)
                q[':question/problem']=q[':question/problem'].replace('('+old+')','('+pt+')')
                q[':question/worked-solution']=source_solution(k,p,g,raw)
            else:q={':question/problem':'For the function $f(x,y,z)='+ft+'$, find a vector that\'s perpendicular to the level surface that passes through the point where $(x,y,z)=('+point_tex(p)+').$',':question/worked-solution':authored_solution(f,ft,p,partials,g)}
            if raw:
                _,g0,_=deriv(f,list(map(sp.sympify,POINTS[k])))
                for field in q[':question/answer-fields']:
                    for ans in field[':answer-field/choices']:
                        v=vector(ans[':answer/value']);vv=sp.Matrix([sp.simplify(v[i]*g[i]/g0[i]) if g0[i]!=0 else v[i] for i in range(3)])
                        ans[':answer/value']=render_like(vv,ans[':answer/value'])
            else:
                vs=method_bank(g)
                if sum(eligible(v,g) for v in vs)!=1 or any(v==sp.zeros(3,1) for v in vs) or len({str(v) for v in vs})!=5:raise Rejected('Reject entire ambiguous omission bank')
                q={':question/problem':q[':question/problem'],':question/worked-solution':q[':question/worked-solution'],':question/difficulty':':question.difficulty/'+level,':question/answer-fields':[{':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':[{':answer/type':':answer.type/math',':answer/value':vtex(v)} for v in vs]}]}
            # Content identity excludes seed/order/profile aliases, includes actual level.
            semantic=copy.deepcopy(q)
            for field in semantic.get(':question/answer-fields',[]):
                field.pop(':db/id',None);field.pop(':answer-field/id',None)
                designation=field.pop(':answer-field/correct',None)
                if designation:
                    field['correct_value']=next(a[':answer/value'] for a in field[':answer-field/choices'] if a[':answer/id']==designation[1])
                for aa in field[':answer-field/choices']:aa.pop(':answer/id',None);aa.pop(':db/id',None)
                field[':answer-field/choices']=sorted(field[':answer-field/choices'],key=lambda a:a[':answer/value'])
            semantic.pop(':db/id',None);semantic.pop(':question/id',None);semantic.pop(':question/math-academy-id',None)
            identity=hashlib.sha256(json.dumps([VERSION,semantic],sort_keys=True).encode()).hexdigest()
            if not raw:
                q[':question/id']=uid(identity)
                for index,field in enumerate(q[':question/answer-fields']):
                    field[':answer-field/id']=uid(identity+str(index));right=None
                    for ii,ans in enumerate(field[':answer-field/choices']):
                        ans[':answer/id']=uid(field[':answer-field/id']+ans[':answer/value'])
                        if ii==0:right=ans[':answer/id']
                    field[':answer-field/correct']=[':answer/id',right];rng.shuffle(field[':answer-field/choices'])
            # Normalized function modulo positive/negative scalar aliases; constant
            # offsets are incidental to gradient assessment. Variables fixed x,y,z.
            df=[sp.expand(d) for d in partials]; terms=[t for d in df for t in sp.Add.make_args(d) if t!=0];scale=terms[0].as_coeff_Mul()[0]
            fingerprint=hashlib.sha256(str(([sp.simplify(d/scale) for d in df],p,'normal')).encode()).hexdigest()
            return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'template':k,'bank_profile':profile,'parameters':{'point':[str(a) for a in p],**({'coefficients':pp['coefficients']} if k not in QUESTIONS else {})},'provenance':{'database':SOURCE['database'],'basis':SOURCE['basis'],'lineage':SOURCE['lineage']},'evidence_only':raw,'eligible_for_learning':not raw,'authored_level':level!='easy','criterion':'normal','task_fingerprint':fingerprint,'content_identity':identity,'level_surface_value':str(c),'python':sys.version.split()[0],'sympy':sp.__version__,'plots':'none'}}
        except (ValueError,TypeError) as exc:
            if parameters is not None:raise
    raise Rejected('No eligible complete bank in bounded sampler')

# EASY: observed 12 function families; direct partial differentiation/substitution.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE: authored six-term quadratic, six nonzero coefficients and three
# nonunit integer substitutions; every partial has three substantive terms.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# HARD: same six-term quadratic and same gradient method, all three substitutions
# nonintegral rationals of denominator 2/3; no tangent planes or normal lines.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)

def markdown(r):
    q=r['question'];g=r['generation'];rows=['## '+g['template']+' — '+('raw evidence only' if g['evidence_only'] else 'generated '+q[':question/difficulty'].split('/')[-1]),q[':question/problem']]
    for index,f in enumerate(q.get(':question/answer-fields',[])):
        rows.append('Field '+str(index)+' (`'+f[':answer-field/key']+'`):')
        for a in f[':answer-field/choices']:rows.append('- $'+a[':answer/value']+'$'+(' **designated**' if f.get(':answer-field/correct',[None,None])[1]==a[':answer/id'] else ''))
    return '\n\n'.join(rows+['Worked solution:',q.get(':question/worked-solution','[absent]')])

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');a=ap.parse_args()
    levels=['easy','moderate','hard'] if a.difficulty=='all' else [a.difficulty]
    if a.count<1:ap.error('Positive count required')
    records=[generate(l,a.seed+i,a.template,profile=a.profile) for l in levels for i in range(a.count)]
    print(json.dumps(records,indent=2,ensure_ascii=False) if a.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
if __name__=='__main__':main()
