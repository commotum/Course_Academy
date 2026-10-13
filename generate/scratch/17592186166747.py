#!/usr/bin/env python3
"""Basis-1356, steps 3–7 only: two intermediate variables, one independent variable.

Observed evidence profiles are public, parameterized time-translation masks, never
literal-payload branches. Opaque historical banks remain ineligible. Normal banks
use the two actual branch products, preserving every source calculation stage.
Moderate/hard are explicitly authored workload claims, not observed ratings.
No database, shared engine, renderer or registration mutations are performed.
"""
from __future__ import annotations
import argparse, copy, hashlib, json, random, re, sys, uuid
from pathlib import Path
import sympy as sp

KP=17592186166747
HERE=Path(__file__).with_suffix('')
SNAPSHOT=json.loads((HERE/'source.json').read_text())
REC=SNAPSHOT['record']; TITLE=REC[':knowledge-point/title']; VERSION='one-independent-v1'
SOURCES=REC[':knowledge-point/questions']
NAMES=['exp_product','log_trig','trig_product','power_exp','root_log','linear_cos','exp_power','linear_log','trig_quotient','rational_power','exp_trig','root_exp']
QMAP=dict(zip(NAMES,SOURCES)); LEVELS=('easy','moderate','hard')
x,y=sp.symbols('x y',real=True)

def latex(e):
    return sp.latex(e,ln_notation=True).replace(r'\left', '').replace(r'\right','')
def digest(o):return hashlib.sha256(json.dumps(o,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
def uid(o):return str(uuid.uuid5(uuid.NAMESPACE_URL,digest(o)))
def normalize(s):
    return s.replace('\\\\','\\').replace(r'\u2061','').replace('\u2061','').replace('⁡','')
def formal(v):return r'\frac{\text{d}f}{\text{d}'+v+'}'
def part(c):return rf'\frac{{∂f}}{{∂{c}}}'
def coord(c,v):return r'\frac{\text{d}'+c+r'}{\text{d}'+v+'}'
def block(s):return '\n\n$$\n'+s+'\n$$'
def aligned(rows):return r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}'
def raw_mask(s,v,h):
    """Only whole mathematical variable tokens change; abstract dependency/derivative
    labels are protected. Numeric arguments of sqrt/ln remain mathematical slots.
    Translation derivative is 1, so all source component/product rows remain valid.
    h=0 is rendered by the same slot recipe, preserving exact raw text bytes.
    """
    protected=[]
    def hold(m):protected.append(m[0]);return f'@@{len(protected)-1}@@'
    # Complete formal differential fractions and generic dependency declarations.
    pat=r'\\(?:d?frac)\{(?:\\text\{d\}|\\textrm\{d\}|d)[fxy]\}\{(?:\\text\{d\}|\\textrm\{d\}|d)'+v+r'\}|[xy]\('+v+r'\)'
    s=re.sub(pat,hold,s)
    s=re.sub(r'\$'+v+r'[, .]*\$',hold,s)
    token=v if h==0 else '('+v+('+' if h>0 else '')+str(h)+')'
    # Never edit prose, command names or dependent-variable labels.
    chunks=re.split(r'(\$\$.*?\$\$|\$[^$]*\$)',s,flags=re.S)
    for i,c in enumerate(chunks):
        if c.startswith('$'):chunks[i]=re.sub(r'(?<![A-Za-z\\])'+v+r'(?![A-Za-z])',lambda _:token,c)
    s=''.join(chunks)
    for i,p in enumerate(protected):s=s.replace(f'@@{i}@@',p)
    return s

def raw_question(name,h,repair=False):
    q=QMAP[name]; v='s' if name in ('exp_power','linear_log','trig_quotient','rational_power','root_exp') else 't'
    result={k:copy.deepcopy(val) for k,val in q.items() if k not in (':question/id',':question/answer-fields')}
    for key in (':question/problem',':question/worked-solution'):
        if key in result:result[key]=raw_mask(result[key],v,h)
    fields=[]
    for f in q[':question/answer-fields']:
        out={':db/id':f[':db/id'],':answer-field/key':f[':answer-field/key'],':answer-field/type':f[':answer-field/type'][':db/ident'],':answer-field/choices':[]}
        for a in f[':answer-field/choices']:
            val=raw_mask('$'+a[':answer/value']+'$',v,h)[1:-1]
            out[':answer-field/choices'].append({':db/id':a[':db/id'],':answer/type':a[':answer/type'][':db/ident'],':answer/value':val})
        if ':answer-field/correct' in f:
            out['_correct_index']=next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][':answer/id'])
        fields.append(out)
    result[':question/answer-fields']=fields
    if repair and name=='exp_product':
        fields[0]['_correct_index']=1
        result[':question/difficulty']=':question.difficulty/easy'
        result[':question/worked-solution']=normal_question(name,'easy',{'n':2,'a':1,'b':1,'h':h,'k':h})[0][':question/worked-solution']
    if ':question/difficulty' in result and isinstance(result[':question/difficulty'],dict):result[':question/difficulty']=result[':question/difficulty'][':db/ident']
    return result

# Shared family mathematics; all coordinates are functions of the same symbol.
def components(name,p,v):
    n,a,b,h,k=(p[z] for z in ('n','a','b','h','k'))
    u=v+h; w=v+k
    if name=='exp_product':F=x*sp.exp(x*y); X=a*u**n;Y=b*w
    elif name=='log_trig':F=sp.log(x*y**n);X=sp.cos(a*u);Y=sp.sin(b*w)
    elif name=='trig_product':F=sp.sin(x)*sp.cos(y);X=a*u**n;Y=b*w
    elif name=='power_exp':F=x**2*sp.exp(y);X=a*u;Y=b*w**n
    elif name=='root_log':F=sp.sqrt(2*x*y);X=a*u**n;Y=sp.log(b*w)
    elif name=='linear_cos':F=x*sp.cos(y);X=a*u;Y=b*w
    elif name=='exp_power':F=sp.exp(x+b*y);X=a*u**n;Y=w
    elif name=='linear_log':F=y+x*sp.log(y);X=a*u;Y=b*w
    elif name=='trig_quotient':F=x/y;X=sp.cos(a*u);Y=sp.sin(a*u)
    elif name=='rational_power':F=x/(b+y);X=a*u**n;Y=w
    elif name=='exp_trig':F=sp.exp(b*y-x);X=sp.cos(a*u);Y=sp.sin(a*u)
    elif name=='root_exp':F=y*sp.exp(x);X=a*sp.sqrt(u);Y=b*w**n
    elif name=='authored_moderate':F=x*sp.exp(x*y);X=a*v**n;Y=v**b
    elif name=='authored_hard':F=x*sp.exp(x*y);X=(a*v+h)**n;Y=(b*v+k)**2
    else:raise ValueError('Unknown template')
    return F,X,Y

ORIGINAL={name:dict(n=2,a=1,b=1,h=0,k=0) for name in NAMES}
for name in ('root_log','linear_cos','linear_log','trig_quotient','exp_trig'):ORIGINAL[name]['n']=1
ORIGINAL['power_exp']['a']=2
ORIGINAL['linear_cos']['a']=4
ORIGINAL['exp_power']['b']=2
ORIGINAL['linear_log']['b']=2
ORIGINAL['trig_quotient']['a']=2
ORIGINAL['exp_trig']['b']=2
ORIGINAL['root_exp']['n']=1

def check_parameters(name,level,p):
    if set(p)!=set(('n','a','b','h','k')) or any(type(z)!=int for z in p.values()):raise ValueError('Parameters require exactly integer n,a,b,h,k')
    if name.startswith('authored_'):
        if name=='authored_moderate':
            if level!='moderate' or not(2<=p['n']<=5 and 2<=p['b']<=5 and p['n']!=p['b'] and 1<=p['a']<=4 and p['h']==p['k']==0):raise ValueError('Moderate requires two unequal nonlinear monomials, powers 2–5, a 1–4, no offsets')
        elif level!='hard' or not(2<=p['n']<=3 and 1<=p['a']<=3 and 1<=p['b']<=3 and 1<=abs(p['h'])<=3 and 1<=abs(p['k'])<=3):raise ValueError('Hard requires two affine-power maps, nonzero bounded offsets')
    elif level!='easy' or not(1<=p['n']<=4 and 1<=p['a']<=6 and 1<=p['b']<=5 and abs(p['h'])<=3 and abs(p['k'])<=3):raise ValueError('Easy bounds: n1–4,a1–6,b1–5,offset magnitude<=3')
    if name in ('log_trig','trig_quotient') and (p['h']!=p['k'] or (name=='log_trig' and p['a']!=p['b'])):raise ValueError('Common angle required for the source trigonometric reduction/domain')

# NORMAL solutions preserve ordered formal, partial, substitution, coordinate,
# product, distribution, family-specific fraction/trig reduction and final stages.
def normal_question(name,level,p):
    v=sp.Symbol('s' if name in ('exp_power','linear_log','trig_quotient','rational_power','root_exp') else 't',positive=True)
    F,X,Y=components(name,p,v); fx=sp.diff(F,x);fy=sp.diff(F,y)
    sub={x:X,y:Y}; sx=fx.subs(sub,simultaneous=True);sy=fy.subs(sub,simultaneous=True);dx=sp.diff(X,v);dy=sp.diff(Y,v)
    A=sx*dx;B=sy*dy;C=sp.factor_terms(A+B)
    if name=='trig_quotient':C=-p['a']*sp.csc(p['a']*(v+p['h']))**2
    if name=='log_trig':C=p['n']*p['b']*sp.cot(p['a']*(v+p['h']))-p['a']*sp.tan(p['a']*(v+p['h']))
    if name in ('rational_power','root_log'):C=sp.factor(sp.together(A+B))
    exponent_args={'exp_product':X*Y,'power_exp':Y,'exp_power':X+p['b']*Y,'exp_trig':p['b']*Y-X,'root_exp':X,'authored_moderate':X*Y,'authored_hard':X*Y}
    if name in exponent_args:
        C=C.xreplace({atom:sp.exp(exponent_args[name]) for atom in C.atoms(sp.exp)})
    fml=part('x')+r'\cdot '+coord('x',v.name)+'+'+part('y')+r'\cdot '+coord('y',v.name)
    domain=''
    if name=='log_trig':domain=rf' for $0<{latex(p["a"]*(v+p["h"]))}<\frac{{\pi}}{{2}}$'
    elif name=='root_log':domain=rf' for ${latex(v+p["h"])}>0$ and ${latex(p["b"]*(v+p["k"]))}>1$'
    elif name=='linear_log':domain=rf' for ${latex(v+p["k"])}>0$'
    elif name=='root_exp':domain=rf' for ${latex(v+p["h"])}>0$ and ${latex(v+p["k"])}>0$'
    elif name=='trig_quotient':domain=rf' where $\sin({latex(p["a"]*(v+p["h"]))})\ne0$'
    elif name=='rational_power':domain=rf' where ${latex(p["b"]+Y)}\ne0$'
    fdisplay=r'\sqrt{2xy}' if name=='root_log' else latex(F)
    prompt=rf'If $f(x,y)={fdisplay},$ $x={latex(X)}$ and $y={latex(Y)},$ compute ${formal(v.name)}$'+domain+'.'
    source=QMAP.get(name,QMAP['exp_product'])
    prose=source.get(':question/worked-solution',QMAP['trig_product'][':question/worked-solution'])
    paras=re.split(r'\$\$.*?\$\$',prose,flags=re.S)
    # Static dependency tree fixed labels match actual independent variable.
    if v.name=='s':paras=[z.replace('f0/f01b253f560405a8c0f4be8f8797c652fb0ddf774f4db110b8822313b8ac50f3','7e/7e5b5001794ecdf2c9b9e9102f334a63d2c59bc6f7511c2eb7fa358fc94cb0c5') for z in paras]
    if name.startswith('authored_') or name=='exp_product':
        paras=re.split(r'\$\$.*?\$\$',QMAP['trig_product'][':question/worked-solution'],flags=re.S)
    rawpartials=[latex(fx),latex(fy)]
    if name=='root_log':rawpartials=[r'\frac{y}{\sqrt{2xy}}',r'\frac{x}{\sqrt{2xy}}']
    if name=='log_trig':rawpartials=[rf'\frac{{{latex(y**p["n"])}}}{{{latex(x*y**p["n"])}}}='+latex(fx),rf'\frac{{{latex(p["n"]*x*y**(p["n"]-1))}}}{{{latex(x*y**p["n"])}}}='+latex(fy)]
    partial=aligned([part('x')+'='+rawpartials[0]+r',\,'+part('y')+'='+rawpartials[1]])
    # Preserve explicit coordinate-substitution arithmetic for power_exp and
    # linear_log, not merely a second copy of a simplified CAS result.
    substrows=[]
    for c,fexpr,reduced in [('x',fx,sx),('y',fy,sy)]:
        substituted=latex(fexpr)
        substituted=re.sub(r'\bx\b',lambda _: '('+latex(X)+')',substituted)
        substituted=re.sub(r'\by\b',lambda _: '('+latex(Y)+')',substituted)
        show_arithmetic=name=='power_exp' or (name=='linear_log' and c=='y')
        val=substituted+'='+latex(sp.simplify(reduced)) if show_arithmetic else latex(reduced)
        if name=='root_log':val=rf'\frac{{{latex(Y if c=="x" else X)}}}{{\sqrt{{2({latex(X)})({latex(Y)})}}}}'
        substrows.append(part(c)+' & ='+val)
    coordinates=aligned([coord('x',v.name)+'='+latex(dx)+r',\,'+coord('y',v.name)+'='+latex(dy)+'.'])
    products='('+latex(sx)+r')\cdot ('+latex(dx)+')+('+latex(sy)+r')\cdot ('+latex(dy)+')'
    distributed=latex(A)+' + ('+latex(B)+')'
    if name=='root_log':
        rad=rf'\sqrt{{2({latex(X)})({latex(Y)})}}'
        sxtext=rf'\frac{{{latex(Y)}}}{{{rad}}}';sytext=rf'\frac{{{latex(X)}}}{{{rad}}}'
        products='('+sxtext+r')\cdot ('+latex(dx)+')+('+sytext+r')\cdot ('+latex(dy)+')'
        distributed=rf'\frac{{{latex(Y*dx)}}}{{{rad}}}+\frac{{{latex(X*dy)}}}{{{rad}}}'
    if name=='exp_product' or name.startswith('authored_'):
        distributed=latex(dx*sp.exp(X*Y))+' + ('+latex(X*Y*dx*sp.exp(X*Y))+') + ('+latex(X**2*dy*sp.exp(X*Y))+')'
    rows=[formal(v.name)+' & ='+fml,' & ='+products]
    # Match each observed sequence's optional distribution/reduction row count.
    short=name in ('trig_product','linear_cos','linear_log','exp_trig')
    if (not short or name.startswith('authored_')) and name!='trig_quotient':rows.append(' & ='+distributed)
    if name=='trig_quotient':rows.extend([' & ='+latex(-p['a']-p['a']*sp.cos(p['a']*(v+p['h']))**2/sp.sin(p['a']*(v+p['h']))**2),' & ='+latex(-p['a']-p['a']*sp.cot(p['a']*(v+p['h']))**2)])
    if name=='rational_power':
        rows.append(' & ='+rf'\frac{{({latex(dx)})({latex(p["b"]+Y)})-({latex(X)})({latex(dy)})}}{{({latex(p["b"]+Y)})^2}}')
    finaldisplay=rf'\frac{{{latex(sp.simplify(Y*dx+X*dy))}}}{{{rad}}}' if name=='root_log' else latex(C)
    rows.append(' & ='+finaldisplay+'.')
    blocks=[formal(v.name)+'='+fml,partial,aligned(substrows),coordinates,aligned(rows)]
    solution=''.join(paras[i]+'$$\n'+b+'\n$$' for i,b in enumerate(blocks))+paras[-1]
    bank=[C,A,B,A-B,-C]
    return {':question/problem':prompt,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+level,':question/answer-fields':[{':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':[{':answer/type':':answer.type/math',':answer/value':latex(z)} for z in bank],'_correct_index':0}]},(F,X,Y,fx,fy,sx,sy,dx,dy,A,B,C),[sp.srepr(z) for z in bank]

def sample(name,level,r):
    p=ORIGINAL.get(name,dict(n=2,a=1,b=2,h=0,k=0)).copy()
    if level=='moderate':p.update(n=r.randint(2,5),b=r.randint(2,5),a=r.randint(1,4))
    elif level=='hard':p.update(n=r.randint(2,3),a=r.randint(1,3),b=r.randint(1,3),h=r.choice([-3,-2,-1,1,2,3]),k=r.choice([-3,-2,-1,1,2,3]))
    else:
        p.update(a=r.randint(1,6),b=r.randint(1,5),h=0,k=0)
        if name in ('exp_product','trig_product','power_exp','exp_power','rational_power','root_log','root_exp'):p['n']=r.randint(2,4)
        if name=='log_trig':p.update(n=r.randint(2,4),b=p['a'],k=p['h'])
        if name=='trig_quotient':p['k']=p['h']
    return p

def bank_equal(a,b):
    z=a-b
    if z==0:return True
    witness=z.subs({v:sp.Rational(7,3) for v in z.free_symbols}).evalf(35)
    if witness.is_finite and abs(complex(witness))>1e-20:return False
    return sp.simplify(sp.trigsimp(z))==0

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in LEVELS:raise ValueError('Unknown level')
    if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Only observed radio fields are supported')
    r=random.Random(seed)
    name=template or r.choice(NAMES if level=='easy' else ['authored_'+level])
    if name not in NAMES+['authored_moderate','authored_hard']:raise ValueError('Unknown template')
    # Select complete profile BEFORE parameters, never mix option recipes.
    profile=profile or 'method_branches'
    if profile not in ('method_branches','observed_raw','observed_repaired'):raise ValueError('Unknown bank profile')
    if profile!='method_branches':
        if name not in NAMES or level!='easy':raise ValueError('Observed profiles belong to their easy/authored-unrated replay only')
        p={'h':0} if parameters is None else dict(parameters)
        if set(p)!={'h'} or type(p['h'])!=int or abs(p['h'])>3:raise ValueError('Observed evidence parameters: integer h, |h|<=3')
        q=raw_question(name,p['h'],profile=='observed_repaired');stage=[];bank_expr=[]
    else:
        for attempt in range(200):
            p=dict(parameters) if parameters is not None else sample(name,level,r)
            try:
                check_parameters(name,level,p)
                q,stage,bank_expr=normal_question(name,level,p)
                bank=[sp.sympify(z) for z in bank_expr]
                if any(bank_equal(bank[i],bank[j]) for i in range(5) for j in range(i)):raise ValueError('Ambiguous complete bank')
                break
            except ValueError:
                if parameters is not None:raise
        else:raise RuntimeError('Failed whole-instance sampling')
    fs=q[':question/answer-fields']
    content={'version':VERSION,'level':q.get(':question/difficulty'),'prompt':q[':question/problem'],'solution':q.get(':question/worked-solution'),'bank':sorted(a[':answer/value'] for f in fs for a in f[':answer-field/choices']),'correct':[f[':answer-field/choices'][f['_correct_index']][':answer/value'] if '_correct_index' in f else None for f in fs]}
    qid=uid(content); q[':question/id']=qid
    for i,f in enumerate(fs):
        f[':answer-field/id']=uid([qid,'field',i]);ci=f.pop('_correct_index',None)
        for a in f[':answer-field/choices']:a[':answer/id']=uid([f[':answer-field/id'],a[':answer/value']])
        if ci is not None:f[':answer-field/correct']=[':answer/id',f[':answer-field/choices'][ci][':answer/id']]
        if profile!='observed_raw':r.shuffle(f[':answer-field/choices'])
    # Canonical mathematical object: complete composite F(X(v),Y(v)) up to
    # nonzero output scaling, independent-symbol alias. No bank/seed/order.
    if stage:
        vv=next(z for z in stage[1].free_symbols if z.name in ('t','s'))
        composite=stage[0].subs({x:stage[1],y:stage[2]},simultaneous=True).subs(vv,sp.Symbol('u',positive=True))
        composite=sp.factor_terms(composite)
        # Exp-product canonicalization explicitly removes constant exponential
        # scaling and polynomial leading output scale, while retaining its
        # argument polynomial. This catches swapped coordinate scale aliases.
        if name=='exp_product' or name.startswith('authored_'):
            uu=sp.Symbol('u',positive=True)
            pref=sp.Poly(stage[1].subs(vv,uu),uu);prefcore=sp.expand(pref.as_expr()/pref.LC())
            exponent=sp.Poly(sp.expand((stage[1]*stage[2]).subs(vv,uu)),uu)
            argcore=sp.expand(exponent.as_expr()-exponent.TC())
            composite=sp.Mul(prefcore,sp.exp(argcore),evaluate=False)
        scale,core=composite.as_independent(sp.Symbol('u',positive=True),as_Add=False)
        fingerprint=digest([level,sp.srepr(core),'differentiate two-branch dependency'])
    else:fingerprint=digest(['evidence',name])
    gen={'version':VERSION,'seed':seed,'template':name,'profile':profile,'parameters':p,'source':{k:SNAPSHOT[k] for k in ('database','basis','lineage')},'source_ids':[QMAP[name][':db/id']] if name in QMAP else [REC[':knowledge-point/canonical-example'][':db/id'],QMAP['exp_product'][':db/id']],'original_refs':copy.deepcopy(QMAP[name]) if profile!='method_branches' else None,'eligible_for_learning':profile=='method_branches','evidence_only':profile!='method_branches','authored_level':level!='easy' or name=='exp_product','mathematical_fingerprint':fingerprint,'content_fingerprint':digest(content),'stage_expressions':[sp.srepr(z) for z in stage],'bank_expressions':bank_expr,'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__},'plot_rating':'none'}
    return {'knowledge_point':{'db_id':KP,'id':REC[':knowledge-point/id'],'title':TITLE},'question':q,'generation':gen}

# EASY: observed two branch families; modest coefficient, power and offset changes.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE (authored): both monomial coordinate maps nonlinear, unequal powers.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# HARD (authored): both coordinate maps have nonzero affine inner shifts and powers.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)

def markdown(r):
    q=r['question'];s=q[':question/problem']+'\n\n'
    for f in q.get(':question/answer-fields',[]):
        for a in f[':answer-field/choices']:s+='- $'+a[':answer/value']+'$\n'
    return s+'\n'+q.get(':question/worked-solution','[Source has no worked solution]')
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=(*LEVELS,'all'),default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=('markdown','json'),default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
    records=[generate(l,args.seed+i,args.template,profile=args.profile) for l in (LEVELS if args.difficulty=='all' else [args.difficulty]) for i in range(args.count)]
    print(json.dumps(records,ensure_ascii=False,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(z) for z in records))
