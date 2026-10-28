"""Easy expression/evaluation helpers adapted from supplied scratch generator."""
import sympy as s
x,y=s.symbols("x y", real=True)
def tex(v):
    return s.latex(s.sympify(v)).replace(r'\log',r'\ln')

def val(v):
    return s.sympify(v,locals={'pi':s.pi,'e':s.E})

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

ANCHOR_SPELLINGS={
'linear':{},'cos_sum':{'x':r'\frac{π}{2}'},'sin_product':{'x':r'-\frac{\pi }{2}'},
'exp_cos':{'y':r'\pi '},'log_exp':{'x':'e'},
}

def coord(t,p,name):
    anchor=val(CONFIG[t][3][name]);return ANCHOR_SPELLINGS.get(t,{}).get(name,tex(p[name])) if p[name]==anchor else tex(p[name])

def expression(t,p):
    A=tex(p.get('a',1));
    return {'linear':f'{A}x-y','cos_sum':r'y\cos x + \cos y','sin_product':r'\operatorname{sin}⁡x+xy','rational_radical':r'\frac{{x}^{2}+1}{{x}^{2}{y}^{2}}+y\sqrt{x}','cos_shift':r'\sqrt{2}x\operatorname{cos}⁡(xy+\frac{\pi }{4})','polynomial':f'{A}'+r'{x}^{2}y-'+tex(p.get('b',6))+r'x{y}^{2}','monomial':f'{A}'+r'{x}^{2}y','log_exp':r'2y\operatorname{ln}⁡x-\frac{{e}^{y}}{x}','exp_cos':r'(x+y){e}^{\operatorname{cos}⁡(xy)}','radical_ratio':r'\frac{\sqrt{{x}^{2}-2{y}^{2}}}{y-x}','base_exp':rf'{{{A}}}^{{x+y}}y(x\operatorname{{ln}}⁡({A})+1)','canonical_rational':rf'\dfrac{{{A}x}}y - {A}x^2y','canonical_trig':rf'\dfrac{{{A}x}}y - {A}x^2y+{tex(p.get("b",2))}\cos(\pi y)'}[t]

def source_dialect(t,p,rows):
    # Formatting rules: source uses \pi trailing spaces and /4 unbraced angle.
    rows=[r.replace(r'\frac{\pi}{2}',r'\frac{\pi }{2}').replace(r'\frac{\pi}{4}',r'\frac{\pi }{4}').replace(r'\pi + 1',r'1+\pi ').replace(r'- \pi - 1',r'-1-\pi ').replace(r'\frac{1 + \pi}{e}',r'\frac{1+\pi }{e}').replace(' - ','-').replace(' + ','+') for r in rows]
    rows=[v.replace('- '+chr(92)+'frac', '-'+chr(92)+'frac') for v in rows]
    if t=='sin_product':rows[1]=rows[1].replace(r'- \pi',r'-\pi ')
    if t=='cos_shift':rows[2]=rows[2].replace(r'\frac{\sqrt{2}}{2}',r'\frac{\sqrt{2}}{2}')
    return rows

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
