#!/usr/bin/env python3
"""Computing planar arc lengths, read-only scratch generator (steps 3–7).

Ten observed structural templates preserve every source arithmetic row. Observed
banks are explicitly constrained homothety replay profiles: scalar distractors
alone do not reveal their author's error operation. Default banks are separately
authored complete method operations. Hard is authored from existing perfect-
square and product/chain-rule simplifications, not a spatial-curve extension.

Positive homothety c changes every printed coordinate and every length, while
preserving the source's elementary integration branch and sign conditions.
Changing seed only shuffles a bank for fixed parameters; identities include
all learner content and exclude seed/order. Mathematical fingerprints use the
speed and interval, excluding translations and bank/profile presentation.
"""
from __future__ import annotations
import argparse, hashlib, json, os, random, re, subprocess, sys, tempfile, uuid
from pathlib import Path
import sympy as S
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

KP_ID=17592186119744
KP_UUID='1e310cbe-9d6b-5bc4-960a-8813333bc8be'
TITLE='Computing the Arc Length of a Planar Curve'
VERSION='planar-arc-v2'
HERE=Path(__file__).with_suffix('')
T=S.Symbol('t',real=True)
U=S.Symbol('u',real=True)
SOURCE=json.loads((HERE/'source.json').read_text())
QS={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
# Ordered source families are distinct in presentation/stage sequence, not all
# claimed as distinct skills. The two cubic variants share a mathematical family.
BASE={
 'q-77065':(T**3-3*T,3*T**2,S.Integer(1),S.Integer(2),3*T**2+3),
 'q-77066':(2*T**S.Rational(3,2),3*T,S.Integer(0),S.Integer(3),3*S.sqrt(T+1)),
 'q-127573':(S.exp(T)*S.cos(T),S.exp(T)*S.sin(T),S.Integer(0),S.pi/2,S.sqrt(2)*S.exp(T)),
 'q-127585':(3*T-T**3,3*T**2,S.Integer(-1),S.Integer(1),3*(T**2+1)),
 'q-127602':(T,(T**2+2)**S.Rational(3,2)/3,S.Integer(-1),S.Integer(2),T**2+1),
 'q-77068':(S.log(T)-T**2/2,2*T,S.Integer(1),S.E,1/T+T),
 'q-77070':(T*S.sin(T)+S.cos(T),T*S.cos(T)-S.sin(T),S.Integer(0),S.Integer(2),T),
 'q-77219':(6*T,-3/T-T**3,S.Integer(1),S.Integer(3),3*(T**-2+T**2)),
 'q-77220':(S.cos(2*T)+2*T*S.sin(2*T),S.sin(2*T)-2*T*S.cos(2*T),S.Integer(1),S.Integer(2),4*T),
 'q-77072':(7-2*T**3,3*T**2+10,S.Integer(0),S.sqrt(3),6*T*S.sqrt(T**2+1)),
}
TEMPLATES={sid:{'level':q[':question/difficulty'][':db/ident'].split('/')[-1],'origin':'observed','source_id':sid} for sid,q in QS.items()}
TEMPLATES.update({'hard_exp_spiral':{'level':'hard','origin':'authored'},'hard_reciprocal_affine':{'level':'hard','origin':'authored'}})

def tex(e): return S.latex(S.sympify(e))
def digest(v): return hashlib.sha256(json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
def uid(v): return str(uuid.uuid5(uuid.NAMESPACE_URL,VERSION+':'+v))
def braces(s,i):
    if s[i]!='{': raise ValueError('Expected TeX group: '+s[i:])
    n=1;j=i+1
    while n:
        if j>=len(s): raise ValueError('Unbalanced group')
        n+=(s[j]=='{')-(s[j]=='}');j+=1
    return s[i+1:j-1],j

def parse_math(s):
    """Independent restricted parser for actual displayed coordinate/scalar TeX.

    Fractions, roots, exponent groups and elementary trig/log/exp are parsed
    recursively; implicit multiplication is then handled by SymPy's parser.
    It does not read generation parameters. Unsupported TeX fails explicitly.
    """
    s=s.strip().rstrip('.,?').replace('⁡','').replace('−','-')
    s=s.replace(r'\operatorname{ln}',r'\ln').replace(r'\operatorname{sin}',r'\sin').replace(r'\operatorname{cos}',r'\cos')
    s=s.replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\:','').replace(r'\cdot','*').replace(r'\times','*')
    s=re.sub(r'\{(sin|cos)\}\^',lambda m:'\\'+m.group(1)+'^',s)
    s=s.replace(r'\dfrac',r'\frac').replace(r'\tfrac',r'\frac')
    def convert(z):
        if '|' in z:
            z=re.sub(r'\|([^|]+)\|',lambda m:'abs('+m.group(1)+')',z)
        out='';i=0
        while i<len(z):
            if z.startswith(r'\frac',i):
                a,k=braces(z,i+5);b,j=braces(z,k);out+='(('+convert(a)+')/('+convert(b)+'))';i=j
            elif z.startswith(r'\sqrt',i):
                a,j=braces(z,i+5);out+='(sqrt('+convert(a)+'))';i=j
            elif z[i]=='{':
                a,j=braces(z,i);out+='('+convert(a)+')';i=j
            elif z[i]=='^':out+='**';i+=1
            elif z.startswith(r'\pi',i):out+='(pi)';i+=3
            elif z.startswith(r'\sin',i) or z.startswith(r'\cos',i) or z.startswith(r'\ln',i):
                name='ln' if z.startswith(r'\ln',i) else z[i+1:i+4];i+=len(name)+1
                while i<len(z) and z[i].isspace():i+=1
                power=''
                if i<len(z) and z[i]=='^':
                    if z[i+1]=='{':power,j=braces(z,i+1);i=j
                    else:power=z[i+1];i+=2
                while i<len(z) and z[i].isspace():i+=1
                if i<len(z) and z[i] in '({':
                    close=')' if z[i]=='(' else '}';start=i+1;n=1;i+=1
                    while n:
                        n+=(z[i]==z[start-1])-(z[i]==close);i+=1
                    arg=z[start:i-1]
                else:
                    m=re.match(r'(?:\d+)?[tu]|e|1',z[i:])
                    if not m:raise ValueError('Function argument missing: '+z)
                    arg=m.group();i+=len(arg)
                val=('log' if name=='ln' else name)+'('+convert(arg)+')'
                out+='('+val+')**('+convert(power)+')' if power else '('+val+')'
            elif z[i]=='\\':raise ValueError('Unsupported TeX '+z[i:])
            else:out+=z[i];i+=1
        return out
    expr=convert(s).replace('[','(').replace(']',')')
    return parse_expr(expr,local_dict={'t':T,'u':U,'e':S.E,'pi':S.pi,'sin':S.sin,'cos':S.cos,'log':S.log,'sqrt':S.sqrt,'abs':S.Abs},transformations=standard_transformations+(implicit_multiplication_application,))

def factor(c,s):
    # Uniform coefficient simplification, not a literal-source replay branch.
    return s if c==1 else str(c)+r'\left('+s+r'\right)'

def aligned(rows):return '$$\n'+r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}'+'\n$$'
def inttex(a,b,f,var='t'):return r'\int_{'+tex(a)+'}^{'+tex(b)+'}'+f+r'\,\mathrm{d}'+var

def source_solution(sid,c):
    """Compile captured ordered mathematical nodes into a homothety recipe.

    Each complete derivative/vector/norm/integration/evaluation node is linear
    in c. No substring coefficient replacement; original nested arithmetic is
    retained inside that node. The substitution u and prose remain fixed.
    """
    sol=QS[sid][':question/worked-solution']
    if sid=='q-77220':
        sol=sol.replace(r'16{t}^{2}{cos}^{2}⁡t+16{t}^{2}{sin}^{2}',r'16{t}^{2}{cos}^{2}⁡2t+16{t}^{2}{sin}^{2}⁡2t')
    nodes=[]
    def block(m):
        rows=m.group(1).split(r'\\')
        built=[]
        for raw in rows:
            before,rhs=raw.split('=',1)
            rhs=rhs.rstrip();tail=''
            if rhs.endswith('.'):rhs=rhs[:-1];tail='.'
            # A symbolic norm of the displayed g/r already contains the
            # homothety. Its generic arc-length integral must not be scaled
            # again; explicit source integrands still require the factor c.
            node_scale=1 if '‖' in rhs and r'\int' in rhs else c
            built.append(before+'='+factor(node_scale,rhs)+tail)
            nodes.append({'original_rhs':rhs,'scaled_rhs':factor(node_scale,rhs),'c':node_scale})
        return r'\begin{aligned}'+r'\\'.join(built)+r'\end{aligned}'
    sol=re.sub(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',block,sol,flags=re.S)
    return sol,nodes

def hard_math(template,p):
    c,k,a,b=(S.Integer(p[n]) for n in ('c','k','a','b'));d=S.Integer(p.get('d',0))
    u=k*T+d
    if template=='hard_exp_spiral':
        q=S.Integer(p['q']);x=c*S.exp(k*T)*S.cos(q*T);y=c*S.exp(k*T)*S.sin(q*T)
        speed=c*S.sqrt(k*k+q*q)*S.exp(k*T)
    else:x=2*c*u;y=-c/u-c*u**3/3;speed=c*k*(u**-2+u**2)
    return x,y,a,b,speed

def hard_solution(template,p,x,y,a,b,speed,L):
    c,k=(S.Integer(p[n]) for n in ('c','k'));d=S.Integer(p.get('d',0));u=k*T+d
    dx,dy=S.diff(x,T),S.diff(y,T)
    opening="First, we find $r'(t)$ and $\\|r'(t)\\|:$\n\n"
    rows=[r"r'(t)&=\left\langle\frac{\mathrm{d}}{\mathrm{d}t}("+tex(x)+r'),\frac{\mathrm{d}}{\mathrm{d}t}('+tex(y)+r')\right\rangle',r'&=\left\langle '+tex(dx)+','+tex(dy)+r'\right\rangle',r"\|r'(t)\|&=\sqrt{("+tex(dx)+r')^2+('+tex(dy)+')^2}']
    if template=='hard_exp_spiral':
        q=S.Integer(p['q']);cs=r'\cos('+tex(q*T)+')';sn=r'\sin('+tex(q*T)+')';common=tex(c*S.exp(k*T))
        rows += [r'&='+common+r'\sqrt{('+tex(k)+cs+'-'+tex(q)+sn+r')^2+('+tex(k)+sn+'+'+tex(q)+cs+r')^2}',r'&='+common+r'\sqrt{'+tex(k*k)+cs+'^2-'+tex(2*k*q)+cs+sn+'+'+tex(q*q)+sn+'^2+'+tex(k*k)+sn+'^2+'+tex(2*k*q)+cs+sn+'+'+tex(q*q)+cs+'^2}',r'&='+common+r'\sqrt{'+tex(k*k+q*q)+r'(\cos^2('+tex(q*T)+r')+\sin^2('+tex(q*T)+r'))}',r'&='+tex(speed)]
        anti=c*S.sqrt(k*k+q*q)*S.exp(k*T)/k
        integ=[r'L&='+inttex(a,b,tex(speed)),r'&='+tex(c*S.sqrt(k*k+q*q))+' '+inttex(a,b,tex(S.exp(k*T))),r'&='+tex(anti)+r'\big|_{'+tex(a)+'}^{'+tex(b)+'}',r'&='+tex(c*S.sqrt(k*k+q*q)/k)+r'\left('+tex(S.exp(k*b))+'-'+tex(S.exp(k*a))+r'\right)',r'&='+tex(L)]
        return opening+aligned(rows)+'\n\nTherefore, the arc length of the curve is\n\n'+aligned(integ)
    rows += [r'&='+tex(c*k)+r'\sqrt{4+\left(\frac{1}{('+tex(u)+r')^2}-('+tex(u)+r')^2\right)^2}',r'&='+tex(c*k)+r'\sqrt{4+\frac{1}{('+tex(u)+r')^4}-2+('+tex(u)+r')^4}',r'&='+tex(c*k)+r'\sqrt{\frac{1}{('+tex(u)+r')^4}+2+('+tex(u)+r')^4}',r'&='+tex(c*k)+r'\sqrt{\left(\frac{1}{('+tex(u)+r')^2}+('+tex(u)+r')^2\right)^2}',r'&='+tex(speed)]
    ua,ub=k*a+d,k*b+d;anti=c*(-1/U+U**3/3)
    integ=[r'L&='+inttex(a,b,tex(speed)),r'&='+inttex(ua,ub,tex(c*(U**-2+U**2)),'u'),r'&='+tex(anti)+r'\big|_{'+tex(ua)+'}^{'+tex(ub)+'}',r'&='+tex(c)+r'\left[\left(-\frac{1}{'+tex(ub)+r'}+\frac{'+tex(ub)+r'^3}{3}\right)-\left(-\frac{1}{'+tex(ua)+r'}+\frac{'+tex(ua)+r'^3}{3}\right)\right]',r'&='+tex(L)]
    return opening+aligned(rows)+'\n\nNotice that $'+tex(u)+'>0$ throughout the given interval.\n\nWe can solve this using the substitution $u='+tex(u)+r'$, $\mathrm{d}u='+tex(k)+r'\mathrm{d}t$.'+'\n\nTherefore, the arc length of the curve is\n\n'+aligned(integ)

def validate_parameters(level,template,p):
    required={'c'} if template in BASE else {'c','k','a','b'}|({'q'} if template=='hard_exp_spiral' else {'d'})
    if set(p)!=required:raise ValueError('Parameter keys must be '+str(sorted(required)))
    if any(type(v)!=int for v in p.values()):raise ValueError('Integer parameters required')
    if not 1<=p['c']<=12:raise ValueError('c must be in1..12')
    if template not in BASE:
        if not 2<=p['k']<=3 or not 1<=p.get('d',1)<=2 or not 0<=p['a']<p['b']<=2:raise ValueError('Hard workload bounds violated')
        if template=='hard_reciprocal_affine' and (p['a']!=0 or p['b']!=1):raise ValueError('Affine reciprocal requires interval0..1')
        if template=='hard_exp_spiral' and (not 1<=p['q']<=3 or p['q']==p['k']):raise ValueError('Hard exponential requires q in1..3 unequal to k')

def render_plots(x,y,a,b,identity,template):
    """Render exact-instance sampled coordinates through cached Matplotlib.

    Unique input files and atomic renderer output make concurrent calls safe.
    Curves are sampled here with the primary exact-math runtime; renderer never
    resamples parameters. Existing source assets are evidence, never reused as
    changed-instance figures.
    """
    out=HERE/'plots'/('curve-'+identity[:24]+'.png');out.parent.mkdir(exist_ok=True)
    if out.exists() and out.with_suffix('.json').exists():
        saved=json.loads(out.with_suffix('.json').read_text())
        if saved.get('identity')==identity:
            return {'prompt':str(out.resolve()),'sidecar':str(out.with_suffix('.json').resolve()),'renderer':'Matplotlib'}
    af,bf=float(a),float(b);span=bf-af
    if template=='hard_reciprocal_affine':lo=max(-.1,af-span*.15);hi=bf+span*.15
    elif template=='hard_exp_spiral':lo=af-span*.12;hi=bf+span*.12
    elif template=='q-77065':lo=0.;hi=bf+span*.3
    elif template=='q-77068':lo=.08;hi=bf+span*.25
    elif template=='q-77220':lo=-2.5;hi=2.5
    elif template=='q-127602':lo=af-span*.2;hi=bf+span*.2
    elif template in ('q-77219',):
        lo=max(0.08,af-span*.28);hi=bf+span*.28
    elif template=='q-77066':lo=0.;hi=bf+span*.5
    elif template in ('q-77070','q-77220'):lo=-4.;hi=4.
    elif template=='q-77072':lo=-max(2.,bf*.8);hi=bf+span*.35
    else:lo=af-span*.4;hi=bf+span*.4
    fx=S.lambdify(T,x,'math');fy=S.lambdify(T,y,'math')
    def coords(lo,hi,n):
        ts=[lo+(hi-lo)*i/(n-1) for i in range(n)];return [[fx(v),fy(v)] for v in ts]
    data={'output':str(out.resolve()),'context':coords(lo,hi,501),'segment':coords(af,bf,401),'labels':[tex(a),tex(b)],'template':template,'identity':identity,'interval':[str(a),str(b)],'curve':[str(x),str(y)]}
    fd,path=tempfile.mkstemp(prefix='render-input-',suffix='.json',dir=HERE)
    try:
        with os.fdopen(fd,'w') as f:json.dump(data,f)
        subprocess.run([sys.executable,str(HERE/'render.py'),path],check=True,stdout=subprocess.DEVNULL)
    finally:Path(path).unlink(missing_ok=True)
    return {'prompt':str(out.resolve()),'sidecar':str(out.with_suffix('.json').resolve()),'renderer':'Matplotlib'}

# EASY and MODERATE: observed source-specific arithmetic-stage recipes.
# HARD: authored same-KP perfect-square/product-chain-rule recipes above.
def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ('easy','moderate','hard'):raise ValueError('Unknown difficulty')
    if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Sources only support scalar radio')
    rng=random.Random(seed);eligible=[k for k,v in TEMPLATES.items() if v['level']==level]
    if profile and profile.startswith('observed:'):
        requested=profile.split(':',1)[1]
        if template and template!=requested:raise ValueError('Profile/template mismatch')
        template=requested
    template=template or rng.choice(eligible)
    if template not in eligible:raise ValueError('Template/difficulty mismatch')
    profile=profile or 'authored-method-bank'
    if profile not in ('authored-method-bank','observed:'+template):raise ValueError('Unknown profile')
    if profile.startswith('observed:') and template not in BASE:raise ValueError('No observed hard profiles')
    for attempt in range(100):
        if parameters is not None:p=dict(parameters)
        elif template in BASE:p={'c':rng.randint(1,12)}
        else:p={'c':rng.randint(1,12),'k':rng.randint(2,3),'d':rng.randint(1,2),'a':0,'b':1}
        if template=='hard_exp_spiral' and parameters is None:p.update(q=rng.choice([n for n in range(1,4) if n!=p['k']]));p.pop('d');p['a'],p['b']=rng.choice([(0,1),(0,2),(1,2)])
        validate_parameters(level,template,p)
        c=S.Integer(p['c'])
        if template in BASE:
            bx,by,a,b,bs=BASE[template];x,y,speed=c*bx,c*by,c*bs
        else:x,y,a,b,speed=hard_math(template,p)
        anti=S.integrate(speed,T);L=S.simplify(anti.subs(T,b)-anti.subs(T,a))
        # Correct-first, complete eligible bank, no first-valid distractor pool.
        if profile.startswith('observed:'):
            field=QS[template][':question/answer-fields'][0]
            original=field[':answer-field/choices'];correct_id=field[':answer-field/correct'][':answer/id']
            values=[S.simplify(c*parse_math(v[':answer/value'])) for v in original]
            recipes=['observed_homothety:'+str(i) for i in range(5)]
            correct_index=next(i for i,v in enumerate(original) if v[':answer/id']==correct_id)
            if S.simplify(values[correct_index]-L)!=0:raise ValueError('Source correct value fails independent derivation')
        else:
            dx,dy=S.diff(x,T),S.diff(y,T)
            squared=S.simplify(S.integrate(S.trigsimp(dx*dx+dy*dy),(T,a,b)))
            chord=S.sqrt((x.subs(T,b)-x.subs(T,a))**2+(y.subs(T,b)-y.subs(T,a))**2)
            if template=='q-127585':
                # Select this complete bank before collision checking: the
                # symmetric cubic's chord is identically half its length.
                values=[L,2*L,L/2,squared,c*S.integrate(3*T*T,(T,a,b))]
                recipes=['arc_length','double_traversal','half_antiderivative','omit_norm_square_root','omit_constant_speed_term']
            else:
                values=[L,2*L,L/2,squared,chord]
                recipes=['arc_length','double_traversal','half_antiderivative','omit_norm_square_root','endpoint_chord']
            correct_index=0
        invalid=any(v.is_real is False or float(S.N(v))<=0 for v in values) or any(abs(float(S.N(values[i]-values[j],60)))<1e-10 for i in range(5) for j in range(i))
        if not invalid:break
        if parameters is not None:raise ValueError('Whole bank rejected: duplicate/equivalent/nonpositive member')
    else:raise ValueError('Could not sample complete valid bank')
    task=digest({'speed':str(S.trigsimp(speed)),'interval':[str(a),str(b)],'reasoning':template if template not in ('q-77065','q-127585','q-127602') else 'positive_quadratic_speed'})
    if template in BASE:
        q=QS[template];original_prompt=q[':question/problem'];inside=re.search('⟨(.*?)⟩',original_prompt,re.S).group(1)
        components=re.split(r',(?:\\,)?',inside)
        if len(components)!=2:raise ValueError('Coordinate mask mismatch')
        prompt=original_prompt.replace('⟨'+inside+'⟩','⟨'+re.search(r',(?:\\,)?',inside).group().join(factor(p['c'],v) for v in components)+'⟩')
        solution,nodes=source_solution(template,p['c'])
        original_values=[v[':answer/value'] for v in QS[template][':question/answer-fields'][0][':answer-field/choices']]
        # Preserve observed notation at coefficient one; all values are still
        # independently computed and checked against the profile expression.
        bank_tex=[factor(p['c'],v) for v in original_values] if profile.startswith('observed:') else list(map(tex,values))
    else:
        prompt='Find the arc length of the curve $r(t)=\\langle '+tex(x)+','+tex(y)+r'\rangle$ from $t='+tex(a)+'$ to $t='+tex(b)+'$.\n\n![](PLOT)'
        solution=hard_solution(template,p,x,y,a,b,speed,L);nodes=[];bank_tex=list(map(tex,values))
    # Plot placeholder excluded from identity; exact plot data included instead.
    prompt=re.sub(r'!\[\]\(.*?\)','![](PLOT)',prompt)
    content={'version':VERSION,'level':level,'prompt':prompt,'solution':solution,'bank':sorted(bank_tex),'correct':bank_tex[correct_index],'parameters':p,'profile':profile,'curve':[str(x),str(y)],'interval':[str(a),str(b)]}
    identity=digest(content);qid=uid(identity);fid=uid(qid+':selection')
    answers=[{':answer/id':uid(fid+':'+v),':answer/type':':answer.type/math',':answer/value':v} for v in bank_tex]
    correct=answers[correct_index][':answer/id'];rng.shuffle(answers)
    assets=render_plots(x,y,a,b,identity,template);prompt=prompt.replace('PLOT',assets['prompt'])
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]}]},'generation':{'version':VERSION,'seed':seed,'template':template,'parameters':p,'bank_profile':profile,'origin':TEMPLATES[template]['origin'],'source':{k:SOURCE[k] for k in ('database','basis','lineage')},'source_ids':[template] if template in BASE else [],'content_fingerprint':identity,'mathematical_task_fingerprint':task,'curve':[str(x),str(y)],'interval':[str(a),str(b)],'speed':str(speed),'antiderivative':str(anti),'length':str(L),'ordered_source_nodes':nodes,'recipes':recipes,'domain':'c>0; source interval retained' if template in BASE else 'c,k>0; positive affine u for reciprocal family','plot':assets,'sympy':S.__version__}}

def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)
def generate_hard(seed=0,**kw):return generate('hard',seed,**kw)

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=1);parser.add_argument('--format',choices=['markdown','json'],default='markdown');parser.add_argument('--template');parser.add_argument('--profile');args=parser.parse_args()
    levels=['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty];records=[generate(l,args.seed+i,template=args.template,profile=args.profile) for l in levels for i in range(args.count)]
    if args.format=='json':print(json.dumps(records,ensure_ascii=False,indent=2))
    else:
        for r in records:
            q=r['question'];print(q[':question/problem']);print('\n');print('\n'.join('- $'+a[':answer/value']+'$' for a in q[':question/answer-fields'][0][':answer-field/choices']));print('\n'+q[':question/worked-solution']+'\n')
if __name__=='__main__':main()
