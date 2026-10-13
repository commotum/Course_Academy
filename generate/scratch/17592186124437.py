#!/usr/bin/env python3
"""Supplied partial derivative -> slope at a fixed-coordinate surface section.
All 11 observed radio families replay via masks and computed component recipes.
Historical opaque profiles are evidence-only; defaults use complete method banks.
Easy retains observed evaluation workloads. Missing moderate: two rational/
polynomial components with a nonunit denominator. Missing hard: the same two
components plus one familiar-angle trigonometric component, no differentiation,
line equation, vectors, or internal level progression. See adjacent evidence.
No database, network, plots, engine changes, or transaction construction.
"""
from __future__ import annotations
import argparse, hashlib, json, random, sys, uuid
from pathlib import Path
import sympy as s
KP_ID=17592186124437
KP_UUID='049e8586-8348-50be-ac56-4ea79eba43cd'
TITLE='Finding the Slope of the Tangent Line to a Curve at a Point'
VERSION='supplied-section-slope-1'
ROOT=Path(__file__).with_suffix('')
CAPTURE=json.loads((ROOT/'source.json').read_text())
SOURCES=CAPTURE['record'][':knowledge-point/questions']
x,y=s.symbols('x y', real=True)

def tex(v):
    return s.latex(s.sympify(v)).replace(r'\log',r'\ln')
def val(v):
    return s.sympify(v,locals={'pi':s.pi,'e':s.E})
def par(v): return '('+tex(v)+')'
def uid(v): return str(uuid.uuid5(uuid.NAMESPACE_URL,'course-academy:'+v))
def digest(v): return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()

# The fixed coordinate, point layout, and each operative aligned-chain family
# are independently retained. Distinct structures are not merged by row count.
CONFIG={
'linear':(0,'x','full',{'x':2,'y':3,'z':9,'a':6}),
'cos_sum':(1,'x','coordinate',{'x':'pi/2','y':0}),
'sin_product':(2,'x','coordinate',{'x':'-pi/2','y':2}),
'rational_radical':(3,'x','full',{'x':1,'y':-3,'z':8}),
'cos_shift':(4,'y','coordinate',{'x':1,'y':0}),
'polynomial':(5,'y','coordinate',{'x':2,'y':1,'a':3,'b':6}),
'monomial':(6,'x','full',{'x':1,'y':2,'z':5,'a':4}),
'log_exp':(7,'y','full',{'x':'E','y':2,'z':3}),
'exp_cos':(8,'x','coordinate',{'x':1,'y':'pi'}),
'radical_ratio':(9,'x','coordinate',{'x':3,'y':2}),
'base_exp':(10,'x','full',{'x':0,'y':1,'z':0,'a':2}),
'canonical_rational':(None,'y','full',{'x':2,'y':3,'z':8,'a':4}),
'canonical_trig':(None,'y','full',{'x':2,'y':3,'z':8,'a':4,'b':2}),
}
TEMPLATES={k:{'level':'moderate' if k=='canonical_rational' else 'hard' if k=='canonical_trig' else 'easy','source':None if c[0] is None else SOURCES[c[0]][':question/math-academy-id'],'plot':'none'} for k,c in CONFIG.items()}

# Each historical recipe is explicitly a pattern continuation, not a recovered
# misconception. Historical scalar banks remain public and ineligible by default.
# Whole banks are evaluated together; no first-valid option replacements.
def math_data(t,p):
    X,Y=p['x'],p['y']; A=p.get('a',1);B=p.get('b',1)
    if t=='linear':
        d=A*x-y; parts=[A*X,-Y]; wrong=[A*X+Y,A*X,-Y,A*Y-X]
        historical=[-Y,A*X,sum(parts),X-1,1-X]
    elif t=='cos_sum':
        d=y*s.cos(x)+s.cos(y);parts=[Y*s.cos(X),s.cos(Y)];wrong=[Y*s.sin(X)+s.cos(Y),-s.cos(Y),Y,Y*s.sin(X)-s.cos(Y)]
        historical=[sum(parts),2*X,2, X, 0]
    elif t=='sin_product':
        d=s.sin(x)+x*y;parts=[s.sin(X),X*Y];wrong=[-s.sin(X)+X*Y,s.sin(X),X*Y,s.sin(X)+X]
        historical=[sum(parts),-s.sin(X)-2*X*Y,X*Y,Y+X*Y,s.sin(X)-X*Y]
    elif t=='rational_radical':
        d=(x*x+1)/(x*x*y*y)+y*s.sqrt(x);parts=[(X*X+1)/(X*X*Y*Y),Y*s.sqrt(X)];wrong=[(X*X+1)/(X*X*Y)+Y*s.sqrt(X),parts[0],parts[1],parts[0]-parts[1]]
        historical=[sum(parts),-5*Y/6,-2/Y,(X*X+1)/(-Y)+Y*s.sqrt(X),(X*X+1)/(Y*Y)+2*Y/3]
    elif t=='cos_shift':
        d=s.sqrt(2)*x*s.cos(x*y+s.pi/4);parts=[s.sqrt(2)*X,s.cos(X*Y+s.pi/4)];wrong=[s.sqrt(2)*X*s.cos(X*Y),X*s.cos(X*Y+s.pi/4),s.sqrt(2)*X,-s.prod(parts)]
        historical=[Y,s.prod(parts),2*X,-2*X,-X]
    elif t=='polynomial':
        d=A*x*x*y-B*x*y*y;parts=[A*X*X*Y,-B*X*Y*Y];wrong=[parts[0]-parts[1],parts[0],parts[1],A*Y*Y*X-B*Y*X*X]
        historical=[Y,-Y,X,sum(parts),-A*Y]
    elif t=='monomial':
        d=A*x*x*y;parts=[A*X*X*Y];wrong=[A*X*Y,A*Y*Y*X,A*X*X,A*(X*X+Y)]
        historical=[A*(X+Y),A*(X+Y*Y),parts[0],A+Y,A]
    elif t=='log_exp':
        d=2*y*s.log(x)-s.exp(y)/x;parts=[2*Y*s.log(X),-s.exp(Y)/X];wrong=[Y*s.log(X)-s.exp(Y),parts[0],parts[1],2*Y*s.log(X)+s.exp(Y)/X]
        historical=[Y-s.exp(Y),Y+1,sum(parts),2*Y*s.exp(Y),(Y+1)*X]
    elif t=='exp_cos':
        d=(x+y)*s.exp(s.cos(x*y));parts=[X+Y,s.exp(s.cos(X*Y))];wrong=[Y,(X+Y)*s.exp(-s.cos(X*Y)),X+s.exp(s.cos(X*Y))*Y,(X+Y)*s.cos(X*Y)]
        historical=[Y,s.prod(parts),2*Y*s.E,s.E+Y,Y/s.E**2]
    elif t=='radical_ratio':
        d=s.sqrt(x*x-2*y*y)/(y-x);parts=[s.sqrt(X*X-2*Y*Y),1/(Y-X)];wrong=[parts[0]/(X-Y),parts[0]/Y,-parts[0]/Y,s.sqrt(X*X-Y*Y)/(Y-X)]
        historical=[-1/Y,1/Y,1,0,s.prod(parts)]
    elif t=='base_exp':
        d=A**(x+y)*y*(x*s.log(A)+1);parts=[A**(X+Y),Y,X*s.log(A)+1];wrong=[A**X*Y*(X*s.log(A)+1),-s.prod(parts),A**(X+Y)*Y*X*s.log(A),A**(X+Y)*(X*s.log(A)+Y+1)]
        historical=[s.prod(parts),Y,-Y,-A**(X+Y),X]
    else:
        d=A*x/y-A*x*x*y;parts=[A*X/Y,-A*X*X*Y]
        if t=='canonical_trig':d+=B*s.cos(s.pi*y);parts +=[B*s.cos(s.pi*Y)]
        wrong=[parts[0]-parts[1]+sum(parts[2:]),sum(parts[1:]),parts[0]+sum(parts[2:]),A*X-A*X*X*Y+sum(parts[2:])]
        historical=[]
    simplify=s.expand if t=='base_exp' else s.simplify
    answer=simplify(d.subs({x:X,y:Y}))
    return d,parts,answer,list(map(simplify,wrong)),list(map(simplify,historical))

# Original notation dialect, including operative substitution/evaluation masks.
def source_rows(t,p):
    X,Y=coord(t,p,'x'),coord(t,p,'y');A=tex(p.get('a',1));B=tex(p.get('b',1));_,parts,ans,_,_=math_data(t,p)
    n=[tex(v) for v in parts]; out=tex(ans)
    if t=='linear': return [f'{A}({X})-({Y})={out}']
    if t=='cos_sum':return [rf'({Y})\cos ({X})+\cos ({Y})',out]
    if t=='sin_product':return [rf'\operatorname{{sin}}⁡({X})+({X})\cdot {Y}',out]
    if t=='rational_radical':return [rf'\frac{{{{{X}}}^{{2}}+1}}{{{{{X}}}^{{2}}({Y})^{{2}}}}+({Y})\sqrt{{{X}}}',rf'\frac{{{tex(p["x"]**2+1)}}}{{{tex(p["x"]**2*p["y"]**2)}}}{"-" if p["y"]<0 else "+"}{tex(abs(p["y"]))}({tex(s.sqrt(p["x"]))})',out]
    if t=='cos_shift':return [rf'\sqrt{{2}}({X})\operatorname{{cos}}⁡({X}\cdot {Y}+\frac{{\pi }}{{4}})',rf'\sqrt{{2}}'+('' if p['x']==1 else f'({X})')+rf'\operatorname{{cos}}⁡({tex(p["x"]*p["y"]+s.pi/4)})',rf'\sqrt{{2}}'+('' if p['x']==1 else f'({X})')+rf'\cdot {tex(s.cos(p["x"]*p["y"]+s.pi/4))}',out]
    if t=='polynomial':return [rf'{A}({X})^{{2}}({Y})-{B}({X})({Y})^{{2}}',f'{n[0]}'+('-'+tex(-parts[1]) if parts[1]<0 else '+('+n[1]+')'),out]
    if t=='monomial':return [rf'{A}({X})^{{2}}({Y})={out}']
    if t=='log_exp':return [rf'2({Y})\operatorname{{ln}}⁡{X}-\frac{{{{e}}^{{{Y}}}}}{{{X}}}={out}']
    if t=='exp_cos':
        sumxy=X+'+'+Y if not Y.startswith('-') else X+Y
        return [rf'({sumxy}){{e}}^{{\operatorname{{cos}}⁡({Y}\cdot {X})}}',rf'({sumxy}){{e}}^{{{tex(s.cos(p["x"]*p["y"]))}}}',out]
    if t=='radical_ratio':
        denom=Y+'-'+X if not X.startswith('-') else Y+'-('+X+')'
        return [rf'\frac{{\sqrt{{({X})^{{2}}-2({Y})^{{2}}}}}}{{{denom}}}',rf'\frac{{\sqrt{{{tex(p["x"]**2)}-{tex(2*p["y"]**2)}}}}}{{{tex(p["y"]-p["x"])}}}',out]
    if t=='base_exp':return [rf'{{{A}}}^{{{X}+{Y}}}({Y})({X}\cdot \operatorname{{ln}}⁡({A})+1)={out}']
    first=rf'\frac{{{A}({X})}}{{({Y})}}-{A}({X})^2({Y})'
    if t=='canonical_trig': first+=rf'+{B}\cos(\pi ({Y}))'
    return [first,'+'.join('('+v+')' for v in n),out]

# Preserve original rendering spellings at the anchors using complete component
# masks; changed values are rendered from the SAME recipes, never source payload.
ANCHOR_SPELLINGS={
'linear':{},'cos_sum':{'x':r'\frac{π}{2}'},'sin_product':{'x':r'-\frac{\pi }{2}'},
'exp_cos':{'y':r'\pi '},'log_exp':{'x':'e'},
}
def coord(t,p,name):
    anchor=val(CONFIG[t][3][name]);return ANCHOR_SPELLINGS.get(t,{}).get(name,tex(p[name])) if p[name]==anchor else tex(p[name])
def expression(t,p):
    A=tex(p.get('a',1));
    return {'linear':f'{A}x-y','cos_sum':r'y\cos x + \cos y','sin_product':r'\operatorname{sin}⁡x+xy','rational_radical':r'\frac{{x}^{2}+1}{{x}^{2}{y}^{2}}+y\sqrt{x}','cos_shift':r'\sqrt{2}x\operatorname{cos}⁡(xy+\frac{\pi }{4})','polynomial':f'{A}'+r'{x}^{2}y-'+tex(p.get('b',6))+r'x{y}^{2}','monomial':f'{A}'+r'{x}^{2}y','log_exp':r'2y\operatorname{ln}⁡x-\frac{{e}^{y}}{x}','exp_cos':r'(x+y){e}^{\operatorname{cos}⁡(xy)}','radical_ratio':r'\frac{\sqrt{{x}^{2}-2{y}^{2}}}{y-x}','base_exp':rf'{{{A}}}^{{x+y}}y(x\operatorname{{ln}}⁡({A})+1)','canonical_rational':rf'\dfrac{{{A}x}}y - {A}x^2y','canonical_trig':rf'\dfrac{{{A}x}}y - {A}x^2y+{tex(p.get("b",2))}\cos(\pi y)'}[t]

def render(t,p,raw=False):
    idx,var,layout,anchor=CONFIG[t]; X,Y=coord(t,p,'x'),coord(t,p,'y');Z=tex(p.get('z',0));hold='y' if var=='x' else 'x'; H=Y if hold=='y' else X; V=X if var=='x' else Y
    pair=f'({X},{Y})';point=f'P({X},{Y},{Z})'
    if idx is not None:
        src=SOURCES[idx]; problem=src[':question/problem'];solution=src.get(':question/worked-solution')
        a={k:val(v) for k,v in anchor.items()};ax,ay=coord(t,a,'x'),coord(t,a,'y');az=tex(a.get('z',0));ah=ay if hold=='y' else ax;av=ax if var=='x' else ay
        # Each slot is a complete math/prose component; never substitute short x/y.
        slots=[(f'P({ax},{ay},{az})',point),(f'({ax},{ay})',pair),(f'{hold}={ah}.',f'{hold}={H}.'),(f'{hold} = {ah}',f'{hold} = {H}'),(f'coordinate ${av}$',f'coordinate ${V}$'),(f'{var}={av}',f'{var}={V}'),(expression(t,a),expression(t,p))]
        def mask(text):
            if text is None:return None
            for i,(old,new) in enumerate(sorted(slots,key=lambda z:-len(z[0]))):text=text.replace(old,f'@@SLOT{i}@@')
            for i,(old,new) in enumerate(sorted(slots,key=lambda z:-len(z[0]))):text=text.replace(f'@@SLOT{i}@@',new)
            return text
        problem=mask(problem)
        if solution is not None:
            before,after=solution.split(r'\begin{aligned}',1); _,tail=after.split(r'\end{aligned}',1)
            # Retain source spaces/punctuation around its aligned rows. Exact
            # anchor rows below are render-dialect masks, not payload returns.
            rows=source_rows(t,p)
            rows=source_dialect(t,p,rows)
            sep=r' \\  & ='
            solution=mask(before)+r'\begin{aligned}{f}_{'+var+'}'+pair+' & ='+sep.join(rows)+r'\end{aligned}'+tail
        elif not raw:solution=authored_solution(var,hold,H,point,pair,source_rows(t,p))
        return problem,solution
    problem=f'A surface $S$ is defined by $z=f(x,y).$ The curve $C$ is the intersection of $S$ with the plane ${hold}={H}.$ Given that the point ${point}$ lies on $C,$ and that $f_{var} = {expression(t,p)}$, find the slope of the tangent to $C$ at $P.$'
    return problem,authored_solution(var,hold,H,point,pair,source_rows(t,p))

def authored_solution(var,hold,H,point,pair,rows):
    return f'The curve $C$ is the intersection of the surface $z=f(x,y)$ with the plane ${hold}={H}.$ Hence, the slope of the tangent to the curve $C$ at the point ${point}$ will be given by the partial derivative ${{f}}_{{{var}}}{pair}.$\n\nTo get the slope, we evaluate the partial derivative ${{f}}_{{{var}}}(x,y)$ at ${pair}:$\n\n$$\n'+r'\begin{aligned}{f}_{'+var+'}'+pair+' & ='+r' \\  & ='.join(rows)+r'\end{aligned}'+'\n$$'

def source_dialect(t,p,rows):
    # Formatting rules: source uses \pi trailing spaces and /4 unbraced angle.
    rows=[r.replace(r'\frac{\pi}{2}',r'\frac{\pi }{2}').replace(r'\frac{\pi}{4}',r'\frac{\pi }{4}').replace(r'\pi + 1',r'1+\pi ').replace(r'- \pi - 1',r'-1-\pi ').replace(r'\frac{1 + \pi}{e}',r'\frac{1+\pi }{e}').replace(' - ','-').replace(' + ','+') for r in rows]
    rows=[v.replace('- '+chr(92)+'frac', '-'+chr(92)+'frac') for v in rows]
    if t=='sin_product':rows[1]=rows[1].replace(r'- \pi',r'-\pi ')
    if t=='cos_shift':rows[2]=rows[2].replace(r'\frac{\sqrt{2}}{2}',r'\frac{\sqrt{2}}{2}')
    return rows

def bank_tex(t,p,vals):
    # Historical mathematical expression spelling is a separate complete bank
    # mask, with one-to-one symbolic values validated against the capture.
    if t=='linear':return [tex(v) for v in vals]
    if t=='cos_sum':return [tex(vals[0]),tex(vals[1]).replace(r'\pi','π'),tex(vals[2]),tex(vals[3]).replace(r'\pi','π'),tex(vals[4])]
    if t=='sin_product':
        def fmt(v):return tex(v).replace(' ','').replace(r'\pi',r'\pi ')
        def plus(a,b):return fmt(a)+('+'+fmt(b) if b>=0 else fmt(b))
        return [plus(s.sin(p['x']),p['x']*p['y']),plus(-s.sin(p['x']),-2*p['x']*p['y']),fmt(p['x']*p['y']),plus(p['y'],p['x']*p['y']),plus(-p['x']*p['y'],s.sin(p['x']))]
    if t=='rational_radical':
        out=[tex(v).replace('- '+chr(92)+'frac','-'+chr(92)+'frac') for v in vals];out[1]=rf'\frac{{{tex(-5*p["y"])}}}{{6}}';return out
    if t=='log_exp':return [tex(v).replace(r'2 - e^{2}',r'2-{e}^{2}').replace(r'4 - e','4-e').replace(r'4 e^{2}',r'4{e}^{2}').replace('3 e','3e') for v in vals]
    if t=='exp_cos':
        return [tex(v).replace(r'\pi',r'\pi ').replace(r'\frac{1 + \pi }{e}',r'\frac{1+\pi }{e}').replace(r'2 e \pi ',r'2\pi e').replace(r'e + \pi ',r'e+\pi ').replace(r'\frac{\pi }{e^{2}}',r'\frac{\pi }{{e}^{2}}') for v in vals]
    return [tex(v).replace('- '+chr(92)+'frac','-'+chr(92)+'frac') for v in vals]

# Guards apply to explicit calls as well as samplers. Original replay anchors
# remain supported at observed easy even when authored levels are disjoint.
def guards(t,p):
    for k,v in p.items():
        if v.free_symbols:raise ValueError('parameters must be exact constants')
    X,Y=p['x'],p['y'];d=math_data(t,p)[0]
    if 'z' in p and (not p['z'].is_integer or abs(p['z'])>9):raise ValueError('small integer ancillary height')
    if t in ('linear','polynomial','monomial'):
        if any(not p[k].is_integer or abs(p[k])>6 for k in ('x','y')):raise ValueError('integer coordinate magnitude <=6')
        if any(not p[k].is_integer or not 2<=p[k]<=6 for k in ('a','b') if k in p):raise ValueError('coefficient 2..6')
    if t=='rational_radical' and (X not in (1,4,9) or Y not in (-4,-3,-2,2,3,4)):raise ValueError('perfect-square x and nonzero small y')
    if t=='sin_product' and (X not in tuple(k*s.pi/2 for k in (-3,-1,1,3)) or Y not in (-4,-3,-2,2,3,4)):raise ValueError('familiar odd quarter-turn x; small nonunit y')
    if t=='cos_sum' and (X not in tuple(k*s.pi/2 for k in (-3,-1,1,3)) or Y not in (0,s.pi,2*s.pi)):raise ValueError('familiar x/y angles')
    if t=='cos_shift' and (X not in (-3,-2,-1,1,2,3) or Y not in (0,s.pi/(2*X),s.pi/X)):raise ValueError('familiar shifted angle')
    if t=='log_exp' and (X not in (s.E,s.E**2,s.E**3) or Y not in (1,2,3)):raise ValueError('familiar ln(exp) x; small integer y')
    if t=='exp_cos' and (X not in (-3,-2,-1,1,2,3) or Y not in (s.pi,-s.pi,2*s.pi)):raise ValueError('integer times pi angle')
    if t=='radical_ratio' and ((X,Y) not in ((3,2),(-3,2),(3,-2),(-3,-2),(6,4),(-6,4),(6,-4),(-6,-4))):raise ValueError('perfect-square radicand and nonzero denominator')
    if t=='base_exp' and (X != 0 or Y not in (1,2,3) or p['a'] not in (2,3,4)):raise ValueError('small base/exponent workload')
    if t.startswith('canonical_'):
        if X not in (-3,-2,2,3) or Y not in (-4,-3,3,4) or p['a'] not in (2,3,4,5):raise ValueError('nonunit small rational/polynomial components')
        if (p['a']*X/Y).q==1:raise ValueError('noninteger rational component required')
        if t=='canonical_trig' and p['b'] not in (2,3,4):raise ValueError('nonzero small trig component')
    if not math_data(t,p)[2].is_real:raise ValueError('real finite slope required')
    if math_data(t,p)[2].has(s.zoo,s.nan,s.oo):raise ValueError('singular point')

def sample(t,r):
    p=dict(CONFIG[t][3]);c=lambda a:r.choice(a)
    if t in ('linear','polynomial','monomial'):p.update(x=c([-3,-2,-1,1,2,3]),y=c([-4,-3,-2,1,2,3,4]),a=r.randint(2,6));p.update({'b':r.randint(2,6)} if t=='polynomial' else {})
    elif t=='sin_product':p.update(x=c([-3,-1,1,3])*s.pi/2,y=c([-4,-3,-2,2,3,4]))
    elif t=='cos_sum':p.update(x=c([-3,-1,1,3])*s.pi/2,y=c([0,s.pi,2*s.pi]))
    elif t=='rational_radical':p.update(x=c([1,4,9]),y=c([-4,-3,-2,2,3,4]))
    elif t=='cos_shift':
        p['x']=c([-3,-2,-1,1,2,3]);p['y']=c([0,s.pi/(2*p['x']),s.pi/p['x']])
    elif t=='log_exp':p.update(x=s.E**r.randint(1,3),y=r.randint(1,3))
    elif t=='exp_cos':p.update(x=c([-3,-2,-1,1,2,3]),y=c([s.pi,-s.pi,2*s.pi]))
    elif t=='radical_ratio':p.update(zip(('x','y'),c([(3,2),(-3,2),(3,-2),(-3,-2),(6,4),(-6,4),(6,-4),(-6,-4)])))
    elif t=='base_exp':p.update(x=0,y=r.randint(1,3),a=r.randint(2,4))
    else:p.update(x=c([-3,-2,2,3]),y=c([-4,-3,3,4]),a=r.randint(2,5));p.update({'b':r.randint(2,4)} if t=='canonical_trig' else {})
    if 'z' in p:p['z']=r.randint(-9,9)
    return p

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ('easy','moderate','hard'):raise ValueError('unknown difficulty')
    r=random.Random(seed);t=template or r.choice([k for k,v in TEMPLATES.items() if v['level']==level])
    if t not in TEMPLATES or TEMPLATES[t]['level']!=level:raise ValueError('template difficulty mismatch')
    profile=profile or 'authored_method';raw=profile=='observed_raw';evidence=profile.startswith('observed_')
    if profile not in ('authored_method','observed_raw','observed_supported'):raise ValueError('unknown profile')
    if evidence and CONFIG[t][0] is None:raise ValueError('no observed bank')
    kind=(field_type or 'radio').removeprefix(':answer-field.type/')
    if kind not in ('radio','blank') or evidence and kind!='radio':raise ValueError('source radio layout; authored radio/blank only')
    for attempt in range(1000):
        pp=parameters if parameters is not None else sample(t,r)
        p={k:val(v) for k,v in pp.items()};expected=set(CONFIG[t][3]);
        if set(p)!=expected:raise ValueError('complete exact parameter keys required: '+str(sorted(expected)))
        try:guards(t,p)
        except ValueError:
            if parameters is not None:raise
            continue
        d,parts,answer,wrong,historical=math_data(t,p)
        options=historical if evidence else [answer]+wrong
        if kind=='blank':options=[answer]
        collision=any(s.simplify(a-b)==0 for i,a in enumerate(options) for b in options[i+1:])
        if not collision:break
        if parameters is not None:raise ValueError('whole bank has equivalent options')
    else:raise ValueError('no eligible full bank')
    prompt,solution=render(t,p,raw)
    if kind=='blank':prompt+='\n\nSlope: {{slope}}'
    values=bank_tex(t,p,options) if evidence else [tex(v) for v in options]
    q={':question/problem':prompt}
    src=SOURCES[CONFIG[t][0]] if evidence else None
    if not raw or ':question/difficulty' in src:q[':question/difficulty']=':question.difficulty/'+level
    if solution is not None:q[':question/worked-solution']=solution
    identity=digest({'version':VERSION,'level':q.get(':question/difficulty'),'prompt':prompt,'solution':solution,'kind':kind,'bank':sorted(values),'correct':tex(answer) if not raw or ':answer-field/correct' in src[':question/answer-fields'][0] else None})
    qid=uid(identity);fid=uid(qid+':field');choices=[{':answer/id':uid(fid+':'+v),':answer/type':':answer.type/math',':answer/value':v} for v in values]
    corrects=[c for c,v in zip(choices,options) if s.simplify(v-answer)==0]
    if len(corrects)!=1:raise ValueError('correct answer must occur exactly once')
    correctid=corrects[0][':answer/id'];r.shuffle(choices)
    f={':answer-field/id':fid,':answer-field/key':'slope' if kind=='blank' else 'selection',':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':choices}
    if not raw or ':answer-field/correct' in src[':question/answer-fields'][0]:f[':answer-field/correct']=[':answer/id',correctid]
    q.update({':question/id':qid,':question/answer-fields':[f]})
    task=digest({'derivative':s.srepr(d),'x':s.srepr(p['x']),'y':s.srepr(p['y']),'varying_coordinate':CONFIG[t][1],'assessed_workload':level})
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'template':t,'profile':profile,'seed':seed,'parameters':{k:str(v) for k,v in p.items()},'source':{k:CAPTURE[k] for k in ('database','basis','lineage')},'source_question':TEMPLATES[t]['source'],'origin':'observed-mask' if evidence else 'authored-bank/source-mask' if CONFIG[t][0] is not None else 'authored-missing-level','evidence_only':evidence,'eligible_for_learning':not evidence,'mathematical_fingerprint':task,'content_fingerprint':identity,'plot_rating':'none','dependencies':{'python':sys.version.split()[0],'sympy':s.__version__}}}

# EASY: observed supplied derivative and familiar substitutions, no derivation.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE: authored two nontrivial rational/polynomial component substitutions.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# HARD: authored same two components plus one familiar trig evaluation.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)

def markdown(record):
    q=record['question'];text=q[':question/problem']+'\n\n'
    for f in q.get(':question/answer-fields',[]):
        text+='\n'.join('- $'+c[':answer/value']+'$' for c in f[':answer-field/choices'])+'\n\n'
    return text+q.get(':question/worked-solution','[Raw source has no worked solution.]')
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');ap.add_argument('--field-type',choices=['radio','blank']);args=ap.parse_args()
    records=[generate(l,args.seed+i,args.template,args.field_type,profile=args.profile) for l in (['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]) for i in range(args.count)]
    print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(markdown(v) for v in records))
