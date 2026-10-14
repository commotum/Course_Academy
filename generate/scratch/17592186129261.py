#!/usr/bin/env python3
"""Given transformations: map four boundaries, calculate Jacobian and area.

Frozen math basis 1356. Source templates and explicitly authored profiles are
separate. Raw replay is evidence-only and preserves missing attributes. Public
sampling chooses a COMPLETE operation bank before parameters; collisions reject
the whole instance. Four source recipes are parameterized, never payload replay.
Easy uses linear maps; moderate uses the two observed nonlinear maps; hard is
an authored nonunit-coefficient cubic reciprocal map with the same four stages.
No transformation discovery, inverse solving, Type I regions, or database writes.
"""
from __future__ import annotations
import argparse, hashlib, json, os, random, re, sys, tempfile, uuid
from pathlib import Path
import sympy as S
os.environ.setdefault('MPLCONFIGDIR','/tmp/given-area-matplotlib')

KP=17592186129261
ROOT=Path(__file__).with_suffix('')
SOURCE=json.loads((ROOT/'source.json').read_text())
REC=SOURCE['record']
QUESTIONS={q[':question/math-academy-id']:q for q in REC[':knowledge-point/questions']}
VERSION='given-transform-area-v2'
x,y=S.symbols('x y',positive=True)
u,v=S.symbols('u v',positive=True)
TEMPLATES={'linear_legacy':'easy','linear':'easy','quotient':'moderate','reciprocal':'moderate','reciprocal_scaled':'hard'}
CASES=[
 {'source_id':'q-160365','template':'linear_legacy','level':'easy','parameters':dict(a=2,b=1,l=-1,h=1,j=1,k=2),'bank_profile':'observed-linear-legacy'},
 {'source_id':'q-160379','template':'quotient','level':'moderate','parameters':dict(n=2,l=1,h=2,j=1,k=4),'bank_profile':'observed-quotient'},
 {'source_id':'q-160870','template':'linear','level':'easy','parameters':dict(a=3,b=2,l=-2,h=2,j=1,k=3),'bank_profile':'observed-linear'},
 {'source_id':'q-160891','template':'reciprocal','level':'moderate','parameters':dict(c=1,d=1,n=2,l=2,h=3,j=1,k=3),'bank_profile':'observed-reciprocal'}]
BY_TEMPLATE={c['template']:c for c in CASES}
PROFILES={c['bank_profile']:c['template'] for c in CASES}|{'linear-method':'linear','linear-legacy-method':'linear_legacy','quotient-method':'quotient','reciprocal-method':'reciprocal','scaled-method':'reciprocal_scaled'}
PROFILES.update({'linear-unit-method':'linear','linear-legacy-unit-method':'linear_legacy','quotient-lower-unit-method':'quotient','reciprocal-lower-unit-method':'reciprocal','scaled-lower-unit-method':'reciprocal_scaled'})

def tex(z):return S.latex(S.expand_log(S.sympify(z),force=True),ln_notation=True)
def fraction(a,b):return r'\frac{'+str(a)+'}{'+str(b)+'}'
def signed(z):return ('+' if z>=0 else '-')+str(abs(z))
def identity(value):return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def uid(value):return str(uuid.uuid5(uuid.NAMESPACE_URL,'given-area:'+value))

def objects(template,p):
    if template.startswith('linear'):
        a,b=p['a'],p['b']; U=y-a*x;V=y+b*x
        curves=[a*x+p['l'],a*x+p['h'],p['j']-b*x,p['k']-b*x]
    elif template=='quotient':
        U=y/x**p['n'];V=x*y
        curves=[p['l']*x**p['n'],p['h']*x**p['n'],p['j']/x,p['k']/x]
    else:
        U=p['c']/(x*y);V=p['d']*x**p['n']*y
        curves=[p['c']/(p['l']*x),p['c']/(p['h']*x),p['j']/(p['d']*x**p['n']),p['k']/(p['d']*x**p['n'])]
    jac=S.det(S.Matrix([[S.diff(U,x),S.diff(U,y)],[S.diff(V,x),S.diff(V,y)]]))
    if template.startswith('linear'): J=-1/S.Integer(p['a']+p['b'])
    elif template=='quotient':J=-1/((p['n']+1)*u)
    else:J=S.Rational(p['c'],p['n']-1)/(u**2*v)
    if template.startswith('linear'):area=S.Rational((p['h']-p['l'])*(p['k']-p['j']),p['a']+p['b'])
    elif template=='quotient':area=S.Rational(p['k']-p['j'],p['n']+1)*S.log(S.Rational(p['h'],p['l']))
    else:area=S.Rational(p['c'],p['n']-1)*(S.Rational(1,p['l'])-S.Rational(1,p['h']))*S.log(S.Rational(p['k'],p['j']))
    return U,V,curves,jac,J,area

def check_parameters(template,p,raw=False):
    required=set(BY_TEMPLATE.get(template,{'parameters':dict(c=2,d=2,n=3,l=1,h=2,j=1,k=3)})['parameters'])
    if set(p)!=required or any(type(z)!=int for z in p.values()):raise ValueError('Exact integer slots required: '+str(required))
    if not(-5<=p['l']<p['h']<=9 and 1<=p['j']<p['k']<=10):raise ValueError('Invalid rectangle bounds')
    if template.startswith('linear'):
        if not(1<=p['a']<=4 and 1<=p['b']<=4):raise ValueError('Linear coefficients 1..4')
        if not raw:
            # Normal prompt has no quadrant claim: the full bounded parallelogram is assessed.
            if p['h']-p['l']>8 or p['k']-p['j']>6:raise ValueError('Easy arithmetic ceiling')
    elif template=='quotient':
        if p['n']!=2 or p['l']<1:raise ValueError('Observed moderate quadratic quotient only')
    elif template=='reciprocal':
        if (p['c'],p['d'],p['n'])!=(1,1,2) or p['l']<1:raise ValueError('Observed moderate unit reciprocal quadratic only')
    elif template=='reciprocal_scaled':
        if not(2<=p['c']<=4 and 2<=p['d']<=4 and p['n']==3 and p['l']>=1):raise ValueError('Authored hard nonunit c,d and cubic exponent required')
    else:raise ValueError(template)

def bank(template,p,profile,A):
    """Complete banks. Observed opaque recipes are evidence, not inferred intent."""
    L,H,j,k=map(S.Integer,[p['l'],p['h'],p['j'],p['k']]);W=H-L;Z=k-j
    if template.startswith('linear'):
        a,b=S.Integer(p['a']),S.Integer(p['b']);D=a+b
        if profile=='observed-linear-legacy':values=[W*Z,A,Z/D,D*W*Z,W*W*Z]
        elif profile=='observed-linear':values=[D/(W+Z),W/D,W*Z/a,W/a,A]
        elif 'unit-method' in profile:
            if sorted([a,b])[0]!=1 or a==b:raise ValueError('Unit bank requires exactly one unit coefficient')
            values=[A,W*Z,D*W*Z,Z/D,(W+Z)/D]
        else:values=[A,W*Z,D*W*Z,W*Z/a,W*Z/b]
    elif template=='quotient':
        R=S.log(H/L)
        if profile=='observed-quotient':values=[Z*R,k*R,S.log(k/j),A,A/2]
        elif profile=='quotient-lower-unit-method':
            if L!=1:raise ValueError('Unit lower-bound bank requires L=1')
            values=[A,Z*R,Z*R/p['n'],Z*S.log(k/j)/(p['n']+1),Z*W/(p['n']+1)]
        else:values=[A,Z*R,Z*R/p['n'],Z*S.log(H),Z*S.log(L)/(p['n']+1)]
    else:
        R=S.log(k/j);C=S.Rational(p['c'],p['n']-1)
        if profile=='observed-reciprocal':values=[R/H,A,S.log(Z)/H,C*(1/L-1/H)*S.log(Z),R/L]
        elif 'lower-unit-method' in profile:
            if j!=1:raise ValueError('Unit lower-bound bank requires j=1')
            values=[A,C*R/L,C*R/H,C*R,C*(1/L-1/H)*(k-j)]
        else:values=[A,C*R/L,C*R/H,C*(1/L-1/H)*S.log(k),C*(1/L-1/H)*S.log(j)]
    values=[S.simplify(z) for z in values]
    if any(S.simplify(values[i]-values[z])==0 for i in range(5) for z in range(i)):raise ValueError('Whole bank collision')
    if sum(S.simplify(z-A)==0 for z in values)!=1:raise ValueError('Whole bank lacks one correct area')
    return values

def sample(template,rng,profile):
    p=dict(l=rng.randint(1,4),h=rng.randint(5,9),j=rng.randint(1,3),k=rng.randint(4,8))
    if template.startswith('linear'):
        p.update(a=rng.randint(1,4),b=rng.randint(1,4));p['l']=rng.randint(-4,1);p['h']=rng.randint(2,4)
    elif template=='quotient':p['n']=2
    elif template=='reciprocal':p.update(c=1,d=1,n=2)
    else:p.update(c=rng.randint(2,4),d=rng.randint(2,4),n=3)
    if template.startswith('linear') and 'unit-method' in profile:
        p['a'],p['b']=rng.choice([(1,z) for z in (2,3,4)]+[(z,1) for z in (2,3,4)])
    if profile=='quotient-lower-unit-method':p['l']=1
    if template.startswith('reciprocal') and 'lower-unit-method' in profile:p['j']=1
    return p

def render_plot(p,template):
    """Matplotlib native-pixel rectangle; solid horizontal boundary, fill vertical edges.
    Unique temporary output files and atomic final writes; metadata is required
    alongside PNG for cache acceptance. No shared render-input files.
    """
    import matplotlib;matplotlib.use('Agg')
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_agg import FigureCanvasAgg
    L,H,j,k=[p[z] for z in ('l','h','j','k')]
    upper,lower=('red','blue') if template.startswith('linear') else ('blue','red')
    data={'bounds':[L,H,j,k],'edge_inclusion':{'left':True,'right':True,'bottom':True,'top':True},'edge_strokes':{'left':'fill-only','right':'fill-only','bottom':'solid','top':'solid'},'upper':upper,'lower':lower,'renderer':matplotlib.__version__,'version':VERSION,'pixels':[559,468],'axes_fraction':[.04,.10,.94,.94],'limits':[min(0,L)-1,max(0,H)+1.6,-.6,k+1.1]}
    directory=ROOT/'plots';directory.mkdir(exist_ok=True)
    name=identity(data);out=directory/(name+'.png');side=out.with_suffix('.json')
    if out.exists() and side.exists():return str(out),data
    fig=Figure(figsize=(4.3,3.6),dpi=130);FigureCanvasAgg(fig);ax=fig.add_subplot(111)
    ax.set_xlim(min(0,L)-1,max(0,H)+1.6);ax.set_ylim(-.6,k+1.1)
    ax.fill([L,H,H,L],[j,j,k,k],color='#dfeaf2',zorder=1)
    ax.plot([L,H],[j,j],color=lower,lw=1.6);ax.plot([L,H],[k,k],color=upper,lw=1.6)
    for z in (L,H):ax.plot([z,z],[0,j],ls='--',color='#a5a5a5',lw=.75)
    ax.annotate('',(max(0,H)+1.4,0),(min(0,L)-.9,0),arrowprops=dict(arrowstyle='->',color='black',lw=1))
    ax.annotate('',(0,k+.95),(0,-.5),arrowprops=dict(arrowstyle='->',color='black',lw=1))
    ax.text(max(0,H)+1.4,-.15,'$u$',fontsize=12);ax.text(.08,k+.95,'$v$',fontsize=12)
    for z in (L,H):ax.text(z,-.18,str(z),ha='center',va='top',fontsize=11)
    label_x=(L+H)/2;delta_x=label_x
    if L<=0<=H:
        # The source signed plot deliberately places labels beside the zero
        # axis. Keep every label and the region marker off that black stroke.
        label_x=L+.75*(H-L)
        if abs(label_x)<.18*(H-L):label_x=L+.25*(H-L)
        delta_x=L+.30*(H-L)
        if abs(delta_x)<.12*(H-L):delta_x=L+.15*(H-L)
    ax.text(label_x,k+.10,f'$v={k}$',ha='center',color=upper,fontsize=12)
    ax.text(label_x,j-.12,f'$v={j}$',ha='center',va='top',color=lower,fontsize=12)
    ax.text(delta_x,(j+k)/2,r'$\Delta$',ha='center',va='center',color='#2279bb',fontsize=16)
    ax.axis('off');fig.subplots_adjust(left=.04,right=.94,bottom=.10,top=.94)
    fd,tmp=tempfile.mkstemp(prefix='rect-',suffix='.png',dir=directory);os.close(fd)
    try:fig.savefig(tmp);os.replace(tmp,out)
    finally:
        if os.path.exists(tmp):os.unlink(tmp)
    fd,tmp=tempfile.mkstemp(prefix='rect-',suffix='.json',dir=directory);os.close(fd)
    try:Path(tmp).write_text(json.dumps(data,indent=2));os.replace(tmp,side)
    finally:
        if os.path.exists(tmp):os.unlink(tmp)
    return str(out),data

def prompt(template,p,raw=False):
    U,V,curves,*_=objects(template,p)
    if raw and template=='linear_legacy':
        a,b,l,h,j,k=[p[z] for z in ('a','b','l','h','j','k')]
        return f'Using the change of variables\n\n$u = y - {a}x, v = y + '+('x' if b==1 else f'{b}x')+f'$,\ncalculate the area of the finite region $D$ in the first quadrant bounded by the lines\n$y = {a}x '+ ('- ' if l<0 else '+ ')+f'{abs(l)}, y = {a}x + {h}, y = {j} - '+('x' if b==1 else f'{b}x')+f', y = {k} - '+('x' if b==1 else f'{b}x')+'$.'
    if raw and template=='quotient':
        return 'Using the change of variables\n\n$u = '+fraction('y','x^{'+str(p['n'])+'}')+', v = xy$,\n\ncalculate the area of the finite region $D$ in the first quadrant bounded by the curves\n$y = '+('' if p['l']==1 else str(p['l']))+'x^{'+str(p['n'])+'}, y = '+str(p['h'])+'x^{'+str(p['n'])+'}, y = '+fraction(p['j'],'x')+', y = '+fraction(p['k'],'x')+'$.'
    if raw and template=='linear':
        a,b,l,h,j,k=[p[z] for z in ('a','b','l','h','j','k')]
        return f'Using the change of variables \n\n$$\nu=y-{a}x,\\,v=y+{b}x,\n$$\n\ncalculate the area of the finite region $D$ in the first quadrant bounded by the lines\n\n$$\ny={a}x{signed(l)},\\,y={a}x{signed(h)},\\,y={j}-{b}x,\\,y={k}-{b}x.\n$$'
    if raw and template=='reciprocal':
        l,h,j,k=[p[z] for z in ('l','h','j','k')]
        return 'Using the change of variables\n\n$$\nu=\\frac{1}{xy},\\,v={x}^{2}y,\n$$\n\ncalculate the area of the finite region $D$ in the first quadrant bounded by the curves\n\n$$\ny='+fraction(1,str(l)+'x')+',\\,y='+fraction(1,str(h)+'x')+',\\,y='+fraction(j,'{x}^{2}')+',\\,y='+fraction(k,'{x}^{2}')+'.\n$$'
    quadrant='' if template.startswith('linear') else ' in the first quadrant'
    kind='lines' if template.startswith('linear') else 'curves'
    return 'Using the change of variables\n\n$$\nu='+tex(U)+r',\qquad v='+tex(V)+',\n$$\n\ncalculate the area of the finite region $D$'+quadrant+' bounded by the '+kind+'\n\n$$\n'+r',\qquad '.join('y='+tex(z) for z in curves)+'.\n$$'

def normal_solution(template,p,plot):
    U,V,curves,jac,J,A=objects(template,p);L,H,j,k=[p[z] for z in ('l','h','j','k')]
    base=QUESTIONS['q-160870' if template.startswith('linear') else 'q-160891'][':question/worked-solution']
    blocks=re.findall(r'\$\$(.*?)\$\$',base,re.S)
    blocks[3]='\nu='+tex(U)+r',\,v='+tex(V)+'\n'
    def mapped(transform,cs,vals,variable):
        return '\n'+r'\begin{aligned}'+r' \\ '.join(' & y='+tex(c)+r' & ⟹\, & '+tex(transform)+'='+str(z)+r' & ⟹\, & '+variable+'='+str(z) for c,z in zip(cs,vals))+r'\end{aligned}'+'\n'
    blocks[5]=mapped(U,curves[:2],[L,H],'u');blocks[6]=mapped(V,curves[2:],[j,k],'v')
    blocks[7]='\n'+r'\Delta=\{(u,v)\,:\,'+f'{L}'+r'\le u\le '+f'{H},'+r'\,'+f'{j}'+r'\le v\le '+f'{k}'+r'\}'+'\n'
    formal=re.findall(r'\$\$(.*?)\$\$',base,re.S)[8].split(r' \\  & =')[0]
    M=S.Matrix([[S.diff(U,x),S.diff(U,y)],[S.diff(V,x),S.diff(V,y)]])
    entries=r'\begin{aligned}'+tex(M[0,0])+' & '+tex(M[0,1])+r' \\ '+tex(M[1,0])+' & '+tex(M[1,1])+r'\end{aligned}'
    blocks[8]=formal+r' \\  & =|'+entries+r'| \\  & ='+tex(jac)+r'.\end{aligned}'+'\n'
    inverse_stages=[tex(1/jac)]
    if template.startswith('reciprocal'):
        # Preserve the observed ratio/cancellation stage as an unevaluated mask.
        denom=tex((p['n']-1)*p['c']*p['d']*x**p['n']*y)
        inverse_stages.append(fraction(tex(x**2*y**2),denom))
    inverse_stages.append(tex(J))
    blocks[9]='\n'+r'\frac{∂(x,y)}{∂(u,v)}={(\frac{∂(u,v)}{∂(x,y)})}^{-1}='+'='.join(inverse_stages)+'.\n'
    opening=r'\begin{aligned}{∬}_{D}\text{d}x\text{d}y & ={∬}_{Δ}|\frac{∂(x,y)}{∂(u,v)}|\,\text{d}u\text{d}v'
    if template.startswith('linear'):
        rows=[r'{∬}_{Δ}|'+tex(J)+r'|\,\text{d}u\text{d}v',tex(abs(J))+r'{∬}_{Δ}\,\text{d}u\text{d}v',tex(abs(J))+r'\cdot \text{Area}(Δ)',tex(abs(J))+r'\cdot '+str(H-L)+r'\cdot '+str(k-j),tex(A)]
    else:
        C=S.Rational(1,p['n']+1) if template=='quotient' else S.Rational(p['c'],p['n']-1)
        fu=1/u if template=='quotient' else 1/u**2;fv=S.Integer(1) if template=='quotient' else 1/v
        eu=rf'(\ln {H}-\ln {L})' if template=='quotient' else '('+tex(-S.Rational(1,H))+'+'+tex(S.Rational(1,L))+')'
        ev=f'({k}-{j})' if template=='quotient' else rf'(\ln {k}-\ln {j})'
        factor='' if C==1 else tex(C)
        rows=[r'{∬}_{Δ}|'+tex(J)+r'|\,\text{d}u\text{d}v',rf'\int_{{{L}}}^{{{H}}}\int_{{{j}}}^{{{k}}}'+tex(abs(J))+r'\,\mathrm d v\,\mathrm d u',factor+rf'\int_{{{L}}}^{{{H}}}'+tex(fu)+r'\,\mathrm d u'+rf'\int_{{{j}}}^{{{k}}}'+tex(fv)+r'\,\mathrm d v',(factor+r'\cdot ' if factor else '')+eu+r'\cdot '+ev,tex(A)+'.']
    blocks[10]='\n'+opening+''.join(r' \\  & ='+z for z in rows)+r'\end{aligned}'+'\n'
    it=iter(blocks);solution=re.sub(r'\$\$(.*?)\$\$',lambda m:'$$'+next(it)+'$$',base,flags=re.S)
    # Complete inline component slots; no short symbol substitutions.
    oldU='y-3x' if template.startswith('linear') else r'\frac{1}{xy}'
    oldV='y+2x' if template.startswith('linear') else '{x}^{2}y'
    solution=solution.replace('$u='+oldU+'$','$u='+tex(U)+'$').replace('$v='+oldV+'$','$v='+tex(V)+'$')
    return re.sub(r'!\[\]\([^)]*\)',lambda m:'![]('+plot+')',solution)

def raw_solution(template,p,plot):
    """Explicit complete-component masks, preserving source teaching sequence.
    At anchors the masks preserve exact original spelling. Changed parameters
    follow normal operative stages; raw profiles remain evidence-only.
    """
    if template not in ('linear','reciprocal'):return None
    case=BY_TEMPLATE[template];base=QUESTIONS[case['source_id']][':question/worked-solution']
    anchor=case['parameters']
    # Slot complete numeric equations and expressions, simultaneously, so no
    # replacement can affect a newly inserted component or incidental prose.
    if template=='linear':
        a,b,l,h,j,k=[p[z] for z in ('a','b','l','h','j','k')];D=a+b
        changes={'y-3x':f'y-{a}x','y+2x':f'y+{b}x','y=3x-2':f'y={a}x{signed(l)}','y=3x+2':f'y={a}x{signed(h)}','y=1-2x':f'y={j}-{b}x','y=3-2x':f'y={k}-{b}x',
         'y-3x=-2':f'y-{a}x={l}','y-3x=2':f'y-{a}x={h}','u=-2':f'u={l}','u=2':f'u={h}','y+2x=1':f'y+{b}x={j}','y+2x=3':f'y+{b}x={k}','v=1':f'v={j}','v=3':f'v={k}',
         r'-2\le u\le 2':f'{l}'+r'\le u\le '+str(h),r'1\le v\le 3':f'{j}'+r'\le v\le '+str(k),r'-3 & 1 \\ 2 &':f'-{a}'+r' & 1 \\ '+str(b)+' &','=-5.':f'=-{D}.',r'\frac{1}{5}':fraction(1,D),r'\cdot 4\cdot 2':r'\cdot '+str(h-l)+r'\cdot '+str(k-j),r'\frac{8}{5}':tex(S.Rational((h-l)*(k-j),D))}
    else:
        l,h,j,k=[p[z] for z in ('l','h','j','k')]
        changes={r'y=\frac{1}{2x}':'y='+fraction(1,str(l)+'x'),r'y=\frac{1}{3x}':'y='+fraction(1,str(h)+'x'),r'\frac{1}{xy}=2':r'\frac{1}{xy}='+str(l),r'\frac{1}{xy}=3':r'\frac{1}{xy}='+str(h),'u=2':f'u={l}','u=3':f'u={h}',r'y=\frac{1}{{x}^{2}}':'y='+fraction(j,'{x}^{2}'),r'y=\frac{3}{{x}^{2}}':'y='+fraction(k,'{x}^{2}'),'{x}^{2}y=1':f'{{x}}^{{2}}y={j}','{x}^{2}y=3':f'{{x}}^{{2}}y={k}','v=1':f'v={j}','v=3':f'v={k}',r'2\le u\le 3':str(l)+r'\le u\le '+str(h),r'1\le v\le 3':str(j)+r'\le v\le '+str(k),r'{\int }_{2}^{3}':r'{\int }_{'+str(l)+'}^{'+str(h)+'}',r'{\int }_{1}^{3}':r'{\int }_{'+str(j)+'}^{'+str(k)+'}',r'(-\frac{1}{3}+\frac{1}{2})':'(-'+fraction(1,h)+'+'+fraction(1,l)+')',r'(\operatorname{ln}⁡3-\operatorname{ln}⁡1)':r'(\operatorname{ln}⁡'+str(k)+r'-\operatorname{ln}⁡'+str(j)+')',r'\frac{1}{6}\operatorname{ln}⁡3':tex((S.Rational(1,l)-S.Rational(1,h))*S.log(S.Rational(k,j)))}
        # Anchor final notation preserved by the same expression-mask recipe.
        if (k,j)==(3,1):changes[r'\frac{1}{6}\operatorname{ln}⁡3']=tex(S.Rational(1,l)-S.Rational(1,h))+r'\operatorname{ln}⁡3'
    pattern=re.compile('|'.join(re.escape(z) for z in sorted(changes,key=len,reverse=True)))
    text=pattern.sub(lambda m:changes[m.group()],base)
    # Use source reference iff geometry unchanged; changed instances rerender.
    source_image=re.search(r'!\[\]\(([^)]*)\)',base).group(1)
    return text.replace(source_image,plot)

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ('easy','moderate','hard'):raise ValueError(level)
    if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Only observed radio')
    rng=random.Random(seed)
    if profile is not None:
        if profile not in PROFILES:raise ValueError(profile)
        template=template or PROFILES[profile]
        if PROFILES[profile]!=template:raise ValueError('Profile/template mismatch')
    template=template or rng.choice([z for z,l in TEMPLATES.items() if l==level])
    if TEMPLATES.get(template)!=level:raise ValueError('Template/level mismatch')
    if profile is None:
        choices={'linear':['linear-method','linear-unit-method'],'linear_legacy':['linear-legacy-method','linear-legacy-unit-method'],'quotient':['quotient-method','quotient-lower-unit-method'],'reciprocal':['reciprocal-method','reciprocal-lower-unit-method'],'reciprocal_scaled':['scaled-method','scaled-lower-unit-method']}[template]
        if parameters is not None:
            unit=(min(parameters.get('a',2),parameters.get('b',2))==1) if template.startswith('linear') else (parameters.get('l')==1) if template=='quotient' else parameters.get('j')==1
            profile=choices[int(unit)]
        else:profile=rng.choice(choices)
    raw=profile.startswith('observed-')
    explicit=parameters is not None
    for _ in range(500):
        p=dict(parameters) if explicit else (dict(BY_TEMPLATE[template]['parameters']) if raw else sample(template,rng,profile))
        try:
            check_parameters(template,p,raw);U,V,curves,jac,J,A=objects(template,p);values=bank(template,p,profile,A)
            break
        except ValueError:
            if explicit or raw:raise
    else:raise ValueError('No eligible whole bank')
    plot,data=render_plot(p,template)
    if raw and template in ('linear','reciprocal') and all(p[z]==BY_TEMPLATE[template]['parameters'][z] for z in ('l','h','j','k')):
        plot=re.search(r'!\[\]\(([^)]*)\)',QUESTIONS[BY_TEMPLATE[template]['source_id']][':question/worked-solution']).group(1)
    problem=prompt(template,p,raw)
    solution=raw_solution(template,p,plot) if raw else normal_solution(template,p,plot)
    texts=[tex(z) for z in values]
    # Historical notation choices are variable complete expression recipes.
    if raw and template=='linear_legacy':texts=[str((p['h']-p['l'])*(p['k']-p['j'])),tex(A),fraction(p['k']-p['j'],p['a']+p['b']),str((p['a']+p['b'])*(p['h']-p['l'])*(p['k']-p['j'])),str((p['h']-p['l'])**2*(p['k']-p['j']))]
    if raw and template=='quotient':
        R=S.Rational(p['h'],p['l']);C=S.Rational(p['k']-p['j'],p['n']+1)
        texts=[tex(S.Integer(p['k']-p['j']))+r'\ln '+tex(R),tex(p['k'])+r'\ln '+tex(R),r'\ln '+tex(S.Rational(p['k'],p['j'])),('' if C==1 else tex(C))+r'\ln '+tex(R),tex(C/2)+r'\ln '+tex(R)]
    if raw and template=='reciprocal':
        L,H,j,k=map(S.Integer,[p['l'],p['h'],p['j'],p['k']]);texts=[tex(1/H)+r'\operatorname{ln}⁡'+tex(k/j),tex(1/L-1/H)+r'\operatorname{ln}⁡'+tex(k/j),tex(1/H)+r'\operatorname{ln}⁡'+tex(k-j),tex(1/L-1/H)+r'\operatorname{ln}⁡'+tex(k-j),tex(1/L)+r'\operatorname{ln}⁡'+tex(k/j)]
    content={'version':VERSION,'difficulty':level if not raw or template in ('linear','reciprocal') else None,'prompt':problem,'solution':solution,'bank':sorted(texts)}
    digest=identity(content);question_id=uid(digest);fid=uid(digest+':selection')
    answers=[{':answer/id':uid(fid+':'+text),':answer/type':':answer.type/math',':answer/value':text} for text in texts]
    correct=answers[next(i for i,z in enumerate(values) if S.simplify(z-A)==0)][':answer/id']
    rng.shuffle(answers)
    field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers}
    if not raw or template in ('linear','reciprocal'):field[':answer-field/correct']=[':answer/id',correct]
    question={':question/id':question_id,':question/problem':problem,':question/answer-fields':[field]}
    if solution is not None:question[':question/worked-solution']=solution
    if not raw or template in ('linear','reciprocal'):question[':question/difficulty']=':question.difficulty/'+level
    return {'knowledge_point':{'db_id':KP,'id':REC[':knowledge-point/id'],'title':REC[':knowledge-point/title']},'question':question,'generation':{'version':VERSION,'source':{k:SOURCE[k] for k in ('database','basis','lineage')},'seed':seed,'template':template,'profile':profile,'parameters':p,'evidence_only':raw,'eligible_for_learning':not raw,'authored_level':template=='reciprocal_scaled' or template in ('linear_legacy','quotient'),'source_ids':[BY_TEMPLATE[template]['source_id']] if template in BY_TEMPLATE else ['q-160891'],'mathematical_fingerprint':identity({'map':[str(U),str(V)],'bounds':[p[z] for z in ('l','h','j','k')],'demand':'given-map-area','level':level}),'content_fingerprint':digest,'plot':{'path':plot,'spec':data},'derived':{'jacobian':str(jac),'inverse_jacobian':str(J),'area':str(A)},'dependencies':{'python':sys.version.split()[0],'sympy':S.__version__}}}

# Easy: observed linear boundary substitutions, constant determinant and products.
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
# Moderate: observed quadratic quotient or reciprocal, variable Jacobian and logs.
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
# Hard: authored scaled cubic reciprocal, nonunit differentiation and cancellation.
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)

def markdown(r):
    q=r['question'];f=q[':question/answer-fields'][0]
    s=q[':question/problem']+'\n\n'+ '\n'.join('- $'+a[':answer/value']+'$' for a in f[':answer-field/choices'])
    return s+'\n\n'+q.get(':question/worked-solution','[Worked solution absent in raw capture.]')

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=1);parser.add_argument('--format',choices=['markdown','json'],default='markdown');parser.add_argument('--template');parser.add_argument('--profile');args=parser.parse_args()
    levels=['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]
    records=[generate(l,args.seed+i,template=args.template,profile=args.profile) for l in levels for i in range(args.count)]
    print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
if __name__=='__main__':main()
