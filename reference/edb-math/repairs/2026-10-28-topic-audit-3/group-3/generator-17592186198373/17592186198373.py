#!/usr/bin/env python3
"""Domain-inferred transformations, math basis 1356; local draft, steps 3–7.

Six observed families have five-option radios. Source profiles are public,
parameterized homogeneous evidence recipes: k scales each original integral,
its entire bank and its Step 5 equality chain. Their opaque historical wrong
atoms are never sampled for learning. Raw attribute omissions and legacy fields
are preserved. Default banks instead derive five complete, method-based values.
Normal solutions retain each family's separation/order/expansion/primitive
operations, with additional individually evaluated endpoint components.
Easy is authored: infer u=x,v=x+m*y for a linear polynomial integral, unit
Jacobian, zero lower limits. Moderate keeps the six observed reasoning demands
(and explicitly assigns the unrated Gaussian-substitution source). Hard is
an authored bookkeeping extension: nonunit Jacobian and nonzero lower limits;
radical hard has asymmetric limits, preventing symmetric endpoint shortcuts.
No plots are needed: canonical assets are standalone transformation notation.
No database/engine changes. Run evidence/validate.py for independent readback QA.
"""
from __future__ import annotations
import sys
sys.dont_write_bytecode=True
from audit_runtime import asset_payload,normalize_question
from math_format import normalize_prose,normalize_tex
import argparse, hashlib, json, random, re, sys, uuid
from pathlib import Path
import sympy as s
KP_ID=17592186198373
KP_UUID='cd546dda-c78f-5367-b03e-9b3acb420040'
TITLE='Cases When the Transformation Is Inferred From the Domain'
VERSION='domain-inferred-1-audit9837'
D=Path(__file__).with_suffix('')
SOURCE=json.loads((D/'source.json').read_text())
RAW=SOURCE['record'][':knowledge-point/questions']
x,y,u,v=s.symbols('x y u v',real=True)
FAMILIES=('arctan','gaussian','linear_exp','radical','quadratic_exp','sine')
SOURCE_NAMES=dict(zip(FAMILIES,[q[':question/math-academy-id'] for q in RAW]))
SOURCE_BY_NAME={q[':question/math-academy-id']:q for q in RAW}
LEVEL_FAMILIES={'easy':('linear',),'moderate':FAMILIES,'hard':FAMILIES}

def tex(z):
    z=s.sympify(z); atoms=sorted(z.atoms(s.exp),key=str);mask={a:s.Symbol('Zexp'+str(i)) for i,a in enumerate(atoms)}
    text=s.latex(z.xreplace(mask)).replace(r'\log',r'\ln').replace(r'\operatorname{atan}',r'\arctan')
    for a,letter in mask.items():text=text.replace(s.latex(letter),'e^{'+s.latex(a.args[0])+'}')
    return text
def par(z):return r'\left('+tex(z)+r'\right)'
def mul(*zs):return r'\cdot '.join(par(z) for z in zs)
def digest(z):return hashlib.sha256(json.dumps(z,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
def uid(z):return str(uuid.uuid5(uuid.UUID(KP_UUID),z))
def normalize(z):
    if isinstance(z,dict):return {k:normalize(a) for k,a in z.items()}
    if isinstance(z,list):return [normalize(a) for a in z]
    if isinstance(z,s.Basic):return str(z)
    return z

def parameters_for(level,f,rng):
    # Easy: one linear primitive; moderate: original-family operations;
    # hard: same primitives, nonunit factor + four nonzero endpoint values.
    if level=='easy':return dict(a=0,b=rng.randint(2,8),c=0,d=rng.randint(2,6),m=1,k=1,h=0,q=1,R=9)
    a= rng.randint(1,3); b=rng.randint(a+1,min(6,a+4))
    c,d=(0,rng.randint(1,3)) if level=='moderate' else (rng.randint(1,2),rng.randint(3,4))
    p=dict(a=a,b=b,c=c,d=d,m=(2 if f=='gaussian' else 1) if level=='moderate' else rng.choice([3,4]),k=1,h=rng.randint(1,a),q=rng.choice([1,2]),R=9)
    if f=='arctan' and level=='moderate':p.update(a=0,b=rng.randint(2,8),c=0,d=rng.randint(2,6))
    if f=='radical':
        B=rng.choice([1,2])
        if level=='moderate':p.update(a=0,b=rng.randint(1,5),c=-B,d=B,R=rng.choice([r for r in (4,9,16,25) if r>B*B]),m=1)
        else:
            aa=rng.randint(1,2);cc=rng.randint(1,2);dd=rng.randint(cc+1,3)
            p.update(a=aa,b=rng.randint(aa+1,5),c=cc,d=dd,R=rng.choice([r for r in (9,16,25) if r>dd*dd]),m=1)
    if f=='linear_exp' and level=='moderate':
        cc=rng.choice([-1,0,1]);p.update(c=cc,d=cc+rng.randint(1,2))
    if f=='sine':p.update(c='-pi/2' if level=='moderate' else 'pi/6',d=rng.choice(['pi/3','pi/2']) if level=='moderate' else '2*pi/3')
    if f=='quadratic_exp' and level=='moderate':p.update(a=0,b=rng.randint(1,5),c=0,d=rng.randint(1,5))
    if f!='linear_exp':p['h']=0
    return p

def guard(level,f,p):
    keys={'a','b','c','d','m','k','h','q','R'}
    if set(p)!=keys:raise ValueError('parameters require exactly '+','.join(sorted(keys)))
    z={k:s.sympify(val,locals={'pi':s.pi}) for k,val in p.items()}
    if any(z[k].is_Integer is not True for k in keys-{'c','d'}):raise ValueError('integer workload parameters required')
    bmax=8 if level=='easy' or (level=='moderate' and f=='arctan') else (5 if level=='moderate' and f=='quadratic_exp' else 6)
    dmax=6 if level=='easy' or (level=='moderate' and f=='arctan') else (5 if level=='moderate' and f=='quadratic_exp' else 4)
    if not(0<=z['a']<z['b']<=bmax and z['c']<z['d'] and 1<=z['m']<=4 and z['k']==1 and 0<=z['h']<=z['a'] and z['q'] in (1,2) and z['R'] in (4,9,16,25)):raise ValueError('unsupported arithmetic bounds')
    if f=='sine':
        if z['c'] not in (-s.pi/2,s.pi/6) or z['d'] not in (s.pi/3,s.pi/2,2*s.pi/3):raise ValueError('familiar sine angles required')
    elif not(-2<=z['c']<z['d']<=dmax and z['c'].is_Integer and z['d'].is_Integer):raise ValueError('integer rectangle bounds required')
    if f=='linear_exp' and not(1<=z['h']<=z['a']):raise ValueError('shifted linear primitive requires nonzero h')
    if f=='radical' and not(z['R']>max(z['c']**2,z['d']**2) and z['m']==1):raise ValueError('positive radical throughout rectangle required')
    if level=='easy' and not(f=='linear' and z['a']==z['c']==z['h']==0 and z['m']==1 and z['b']<=8 and z['d']<=6):raise ValueError('easy zero-bound unit-Jacobian demand')
    if level=='moderate':
        if f=='arctan' and not(z['a']==0 and z['c']==0):raise ValueError('moderate arctan zero-bound demand')
        if f=='gaussian' and z['c']!=0:raise ValueError('moderate Gaussian zero exponent endpoint')
        if f=='quadratic_exp' and not(z['a']==0 and z['c']==0):raise ValueError('moderate quadratic exponential unit endpoint values')
        if z['m']!=(2 if f=='gaussian' else 1):raise ValueError('moderate original Jacobian workload')
        if f=='radical' and not(z['a']==0 and z['c']==-z['d'] and z['d'] in (1,2)):raise ValueError('moderate symmetric radical demand')
        if f=='sine' and z['c']!=-s.pi/2:raise ValueError('moderate original negative endpoint')
    if level=='hard':
        if not(z['a']>0 and z['c']>0):raise ValueError('hard requires nonzero lower endpoints')
        if f=='radical':
            if not(z['a'] in (1,2) and z['b']<=5 and (z['c'],z['d']) in ((1,2),(1,3),(2,3)) and z['R'] in (9,16,25)):raise ValueError('hard radical asymmetric bounded workload')
        elif z['m'] not in (3,4):raise ValueError('hard nonunit Jacobian demand')
        if f=='sine' and (z['c']!=s.pi/6 or z['d']!=2*s.pi/3):raise ValueError('hard sine familiar nonzero endpoints')
    return z

def model(f,p):
    a,b,c,d,m,k,h,q,R=[p[j] for j in ('a','b','c','d','m','k','h','q','R')]
    if f=='radical':
        U=x/s.sqrt(R-y*y);V=y;X=u*s.sqrt(R-v*v);Y=v;F=x*y*y;A=u;B=v*v*(R-v*v);order='vu'
    else:
        sign=-1 if f=='arctan' else 1
        U=x;V=x+sign*m*y if f!='quadratic_exp' else m*y+x*x
        X=u;Y=(v-u)/(sign*m) if f!='quadratic_exp' else (v-u*u)/m
        if f=='linear':F=V;A=s.Integer(1);B=v;order='uv'
        elif f=='arctan':F=1/(1+V*V);A=s.Integer(1);B=1/(1+v*v);order='uv'
        elif f=='gaussian':F=V*s.exp(V*V);A=s.Integer(1);B=v*s.exp(v*v);order='uv'
        elif f=='linear_exp':F=(x-h)*s.exp(q*V);A=u-h;B=s.exp(q*v);order='vu'
        elif f=='quadratic_exp':F=s.exp(x+V);A=s.exp(u);B=s.exp(v);order='vu'
        else:F=x*s.sin(V);A=u;B=s.sin(v);order='uv'
    J=s.simplify(s.det(s.Matrix([U,V]).jacobian([x,y])));j=s.simplify(s.det(s.Matrix([X,Y]).jacobian([u,v])))
    substituted=s.simplify(F.subs({x:X,y:Y},simultaneous=True))
    weighted=s.simplify(substituted*(s.sqrt(p['R']-v*v) if f=='radical' else abs(j)))
    coefficient=s.Integer(1) if f=='radical' else abs(j)
    Au=s.integrate(A,u);Bv=s.integrate(B,v)
    du=s.expand(Au.subs(u,b)-Au.subs(u,a));dv=s.expand(Bv.subs(v,d)-Bv.subs(v,c))
    I=s.expand(coefficient*du*dv)
    return dict(U=U,V=V,X=X,Y=Y,F=F,J=J,j=j,sub=substituted,weighted=weighted,A=A,B=B,Au=Au,Bv=Bv,du=du,dv=dv,I=I,coef=coefficient,order=order)

def integral(expr,var,lo,hi):return rf'\int_{{{tex(lo)}}}^{{{tex(hi)}}} {expr}\,\mathrm{{d}}{var}'
def bracket(expr,var,lo,hi):return rf'\left[{tex(expr)}\right]_{{{tex(lo)}}}^{{{tex(hi)}}}'
def endpoint(expr,var,val):
    """Keep signed primitive components individually evaluated, no 0^0 artifacts."""
    terms=s.Add.make_args(s.expand(expr));return '+'.join(par(t.subs(var,val)) for t in terms)

def family_chain(f,p,z):
    """Family-specific operative stages; CAS never chooses which operation to show."""
    a,b,c,d=[p[j] for j in ('a','b','c','d')];K=z['coef'];A,B=z['A'],z['B'];Au,Bv=z['Au'],z['Bv'];du,dv=z['du'],z['dv']
    rows=[r'\iint_D '+tex(z['F'])+r'\,\mathrm{d}x\,\mathrm{d}y']
    if f=='quadratic_exp':rows.append(r'\iint_D e^{x+('+tex(z['V'])+r')}\,\mathrm{d}x\,\mathrm{d}y')
    rows.extend([r'\iint_\Delta '+tex(z['sub'])+r'\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\,\mathrm{d}u\,\mathrm{d}v',r'\iint_\Delta '+mul(z['sub'],s.sqrt(p['R']-v*v) if f=='radical' else abs(z['j']))+r'\,\mathrm{d}u\,\mathrm{d}v'])
    if f=='radical':
        rows.append(r'\iint_\Delta u v^2('+tex(p['R'])+r'-v^2)\,\mathrm{d}u\,\mathrm{d}v')
        rows.append(integral(par(A)+'['+integral(tex(s.expand(B)),'v',c,d)+']','u',a,b))
    elif z['order']=='uv':
        rows.append(tex(K)+integral('['+integral(tex(A*B),'u',a,b)+']','v',c,d))
        rows.append(tex(K)+integral(tex(B)+'['+integral(tex(A),'u',a,b)+']','v',c,d))
    else:
        rows.append(tex(K)+integral('['+integral(tex(A*B),'v',c,d)+']','u',a,b))
        # Preserve the original linear factor-out and quadratic exponential split.
        rows.append(tex(K)+integral(par(A)+'['+integral(tex(B),'v',c,d)+']','u',a,b))
    if z['order']=='uv':
        rows.append(tex(K)+integral(tex(B)+bracket(Au,u,a,b),'v',c,d))
        rows.append(tex(K)+integral(tex(B)+r'\left('+endpoint(Au,u,b)+'-('+endpoint(Au,u,a)+r')\right)','v',c,d))
        rows.append(mul(K,du)+integral(tex(B),'v',c,d))
        rows.append(mul(K,du)+bracket(Bv,v,c,d))
        rows.append(mul(K,du)+r'\left('+endpoint(Bv,v,d)+'-('+endpoint(Bv,v,c)+r')\right)')
    else:
        rows.append(tex(K)+integral(par(A)+bracket(Bv,v,c,d),'u',a,b))
        rows.append(tex(K)+integral(par(A)+r'\left('+endpoint(Bv,v,d)+'-('+endpoint(Bv,v,c)+r')\right)','u',a,b))
        rows.append(mul(K,dv)+integral(tex(A),'u',a,b))
        rows.append(mul(K,dv)+bracket(Au,u,a,b))
        rows.append(mul(K,dv)+r'\left('+endpoint(Au,u,b)+'-('+endpoint(Au,u,a)+r')\right)')
    rows.append(mul(K,du,dv));rows.append(tex(z['I']))
    return r'\begin{aligned}'+rows[0]+' & ='+rows[1]+''.join(r' \\ & ='+r for r in rows[2:])+r'\end{aligned}'

COMMON=RAW[0][':question/worked-solution']
INTRO=COMMON.split('**Step 1**')[0]
INVERSE_PROSE=COMMON.split('This change of variables gives us')[1].split('**Step 2**')[0]

def normal_question(level,f,p,z):
    a,b,c,d=[p[j] for j in ('a','b','c','d')]
    constraints=rf'{tex(a)}\le {tex(z["U"])}\le {tex(b)},\quad {tex(c)}\le {tex(z["V"])}\le {tex(d)}'
    prompt='Use a change of variables to evaluate the double integral\n\n$$\n'+r'\iint_D '+tex(z['F'])+r'\,\mathrm{d}x\,\mathrm{d}y'+ '\n$$\n\nwhere $D=\\{(x,y):'+constraints+r'\}.$'
    matrix=s.Matrix([z['U'],z['V']]).jacobian([x,y]);J=z['J'];j=z['j']
    sol=INTRO+'**Step 1**: Find a suitable change of variables.\n\nThe inequalities that define the region $D,$\n\n$$\n'+constraints+',\n$$\n\nsuggest that we use the change of variables\n\n$$\nu='+tex(z['U'])+r'\,\text{and}\,v='+tex(z['V'])+'.\n$$\n\nThis change of variables gives us'+INVERSE_PROSE
    sol+='**Step 2**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$\n\nOur domain in the $uv$-plane is\n\n$$\n'+rf'\Delta=\{{(u,v):{tex(a)}\le u\le {tex(b)},\,{tex(c)}\le v\le {tex(d)}\}}.'+'\n$$\n\n'
    sol+='**Step 3**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$\n\nThe Jacobian determinant corresponding to ${T}^{-1}$ is\n\n$$\n'+r'\begin{aligned}\frac{\partial(u,v)}{\partial(x,y)} & =\left|\begin{matrix}\frac{\partial u}{\partial x}&\frac{\partial u}{\partial y}\\\frac{\partial v}{\partial x}&\frac{\partial v}{\partial y}\end{matrix}\right|\\&=\left|'+tex(matrix)+r'\right|\\&='+tex(J)+r'.\end{aligned}'+'\n$$\n\n'
    sol+='**Step 4**: Compute the Jacobian determinant corresponding to $T:$\n\n$$\n'+r'\frac{\partial(x,y)}{\partial(u,v)}=\left(\frac{\partial(u,v)}{\partial(x,y)}\right)^{-1}='+tex(1/J)+'='+tex(j)+'.\n$$\n\n'
    sol+='Note that $'+r'\frac{\partial(x,y)}{\partial(u,v)}\ne0'+'$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$\n\n'
    # Explicit inverse proves global injectivity; nonzero Jacobian alone is insufficient.
    sol+='Solving the transformation equations gives $x='+tex(z['X'])+r',\ y='+tex(z['Y'])+'$, so the transformation is one-to-one on this domain.\n\n'
    sol+='**Step 5**: Perform the change of variables, and evaluate the integral:\n\nPerforming the change of variables, we obtain\n\n$$\n'+family_chain(f,p,z)+'\n$$'
    return prompt,sol

def bank(f,p,z):
    """Choose this complete operation bank before sampling; no first-valid pooling."""
    a,b,c,d,m=[p[j] for j in ('a','b','c','d','m')];K=z['coef'];A,B=z['Au'],z['Bv'];du,dv=z['du'],z['dv'];I=z['I']
    if f=='radical':
        # The radical cancels with the nonconstant Jacobian. Wrong recipes omit
        # the -v^4 term, reverse its sign, omit 1/2 primitive, or lose lower endpoint.
        V=lambda expr:s.integrate(expr,(v,c,d))
        vals=[I,du*V(p['R']*v*v),du*V(p['R']*v*v+v**4),2*du*dv,(A.subs(u,b)*dv if a!=0 else (b-a)*dv)]
        names=['correct','drop_quartic','quartic_sign','omit_u_reciprocal','omit_u_lower']
    elif f=='sine':
        # Original symmetric sine integral is zero. Distinct meaningful errors
        # use cosine instead, upper primitive only, reverse sine primitive,
        # or the area times sine at upper endpoint. Reverse primitive coincides
        # at zero, so use omitted lower u endpoint with cosine-integrand error.
        cosint=s.sin(d)-s.sin(c)
        vals=[I,K*du*cosint,-K*du*cosint,K*A.subs(u,b)*cosint,K*(b-a)*(d-c)*s.sin(d)]
        names=['correct','integrate_cosine','reverse_cosine_integral','cosine_and_omit_u_lower','upper_rectangle']
    else:
        vals=[I,K*du*B.subs(v,d),K*du*(B.subs(v,d)+B.subs(v,c)),K*(b-a)*(d-c)*z['B'].subs(v,d)*(z['A'].subs(u,b)),K*du*(d-c)]
        names=['correct','omit_v_lower','add_v_lower','upper_rectangle','replace_v_integrand_by_one']
        if f=='linear' or (f=='arctan' and c==0):
            # Zero primitive at c makes the first two bank members collide;
            # this separately eligible profile uses omitted rectangle width,
            # sign reversal, wrong antiderivative input, and upper rectangle.
            vals=[I,K*dv,-I,K*du*(s.atan(d*d) if f=='arctan' else d/2),K*(b-a)*(d-c)*z['B'].subs(v,d)]
            names=['correct','omit_u_width','reverse_orientation','wrong_primitive_input','upper_rectangle']
        if f=='gaussian':
            vals=[I,du*dv, K*du*(s.exp(d)-s.exp(c))/2,K*du*(s.exp(d*d)+s.exp(c*c))/2,K*du*s.exp(d*d)/2]
            names=['correct','omit_jacobian','omit_squared_exponent','add_lower_endpoint','omit_lower_endpoint']
    vals=[s.expand(t) for t in vals]
    if any(s.simplify(vals[i]-vals[j])==0 for i in range(5) for j in range(i)):raise ValueError('whole bank collision')
    return [tex(z) for z in vals],names

# Homogeneous source evidence: original mathematical components are immutable
# atoms, not a source-answer lookup. At k != 1 a genuine integral, all equality
# sides, and all displayed scalar choices scale together. No opaque recipes are
# claimed as recovered error operations. Normal default families use bank().
def scaled(text,k):return text if k==1 else tex(k)+r'\left('+text+r'\right)'
def source_recipe(f,k):
    q=SOURCE_BY_NAME[SOURCE_NAMES[f]];prompt=q[':question/problem']
    if k!=1:
        if f=='gaussian':
            a=r'(x + 2y)e^{(x + 2y)^{2}}';prompt=prompt.replace(a,scaled(a,k))
        else:
            # One complete integrand region between the D integral and dxdy.
            pat=r'(\{∬\}_\{D\})(.*?)(\\,dxdy)'
            prompt=re.sub(pat,lambda m:m[1]+scaled(m[2],k)+m[3],prompt,count=1,flags=re.S)
    sol=q.get(':question/worked-solution')
    if sol is not None and k!=1:
        start=sol.rfind(r'\begin{aligned}');end=sol.find(r'\end{aligned}',start)
        chain=sol[start+len(r'\begin{aligned}'):end];parts=chain.split(r' \\  & =')
        lhs,rhs=parts[0].split(' & =',1);parts[0]=scaled(lhs,k)+' & ='+scaled(rhs,k)
        parts[1:]=[scaled(t,k) for t in parts[1:]]
        sol=sol[:start]+r'\begin{aligned}'+r' \\  & ='.join(parts)+sol[end:]
    fields=[]
    for original in q.get(':question/answer-fields',[]):
        atoms=[a[':answer/value'] for a in original[':answer-field/choices']]
        values=[scaled(atom,k) for atom in atoms]
        correct=original.get(':answer-field/correct');correct_index=next((i for i,a in enumerate(original[':answer-field/choices']) if correct and a[':answer/id']==correct[':answer/id']),None)
        fields.append((values,correct_index))
    return prompt,sol,fields,q

def record(level,f,p,prompt,sol,banks,seed,profile,raw=None,names=None,mathdata=None):
    if raw is None:prompt=normalize_prose(prompt);sol=normalize_prose(sol);banks=[([normalize_tex(v)for v in vals],correct)for vals,correct in banks]
    content=dict(version=VERSION,difficulty=None if raw and ':question/difficulty' not in raw else level,prompt=prompt,solution=sol,banks=[dict(values=sorted(values),correct=None if correct is None else values[correct]) for values,correct in banks])
    ident=digest(content);q={':question/id':uid('question:'+ident),':question/problem':prompt}
    if raw is None or ':question/worked-solution' in raw:q[':question/worked-solution']=sol
    if raw is None or ':question/difficulty' in raw:q[':question/difficulty']=':question.difficulty/'+level
    fields=[]
    for i,(values,correct) in enumerate(banks):
        fid=uid(ident+':field:'+str(i));answers=[{':answer/id':uid(fid+':answer:'+val),':answer/type':':answer.type/math',':answer/value':val} for val in values]
        field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers}
        if correct is not None:field[':answer-field/correct']=[':answer/id',answers[correct][':answer/id']]
        random.Random(seed+101*i).shuffle(answers);fields.append(field)
    if raw is None or ':question/answer-fields' in raw:q[':question/answer-fields']=fields
    if raw is None:
        obj=mathdata if mathdata is not None else model(f,guard(level,f,p)); meaningful=[level,f,*[str(obj[j]) for j in ('F','U','V')],*[str(s.sympify(p[j],locals={'pi':s.pi})) for j in ('a','b','c','d')]]
    else:meaningful=['homogeneous-source',f,p['k']]
    task=digest(meaningful)
    return dict(knowledge_point=dict(db_id=KP_ID,id=KP_UUID,title=TITLE),question=q,generation=dict(version=VERSION,template=f,profile=profile,seed=seed,parameters=normalize(p),source=dict(database=SOURCE['database'],basis=SOURCE['basis'],lineage=SOURCE['lineage']),source_ids=[SOURCE_NAMES[f]] if f in SOURCE_NAMES else [],mathematical_fingerprint=task,content_fingerprint=ident,evidence_only=raw is not None,eligible_for_learning=raw is None,authored_level=raw is None and (level!='moderate' or f=='gaussian'),recipes=names,dependencies=dict(python=sys.version.split()[0],sympy=s.__version__)))

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in LEVEL_FAMILIES:raise ValueError('unknown difficulty')
    if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('only observed radio format is supported')
    rng=random.Random(seed)
    if profile and profile.startswith('source:'):
        name=profile[7:];f=next((f for f,q in SOURCE_NAMES.items() if q==name),None)
        if f is None or template not in (None,f):raise ValueError('source profile/template mismatch')
        if level!='moderate':raise ValueError('observed profiles use moderate; unrated retains omission')
        p=parameters if parameters is not None else {'k':1}
        if set(p)!={'k'} or type(p['k'])!=int or p['k'] not in (1,2,3):raise ValueError('homogeneous source k in {1,2,3}')
        prompt,sol,fields,q=source_recipe(f,p['k'])
        return record(level,f,p,prompt,sol,fields,seed,profile,raw=q)
    if profile not in (None,'method','authored-method'):raise ValueError('unknown profile')
    if template not in (None,*LEVEL_FAMILIES[level]):raise ValueError('template outside level')
    f=template or rng.choice(LEVEL_FAMILIES[level])
    for _ in range(400):
        p=parameters if parameters is not None else parameters_for(level,f,rng)
        z=guard(level,f,p);data=model(f,z)
        try:values,names=bank(f,z,data)
        except ValueError:
            if parameters is not None:raise
            continue
        prompt,sol=normal_question(level,f,z,data)
        return record(level,f,p,prompt,sol,[(values,0)],seed,'method',names=names,mathdata=data)
    raise ValueError('no eligible complete bank in bounded sampler')

# EASY: authored unit-Jacobian, positive rectangle, linear primitive.
def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
# MODERATE: five observed rated families plus authored unrated-source completion.
def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)
# HARD: authored nonunit Jacobian/nonzero endpoints; asymmetric radical bounds.
def generate_hard(seed=0,**kw):return generate('hard',seed,**kw)

def markdown(r):
    q=r['question'];parts=[q[':question/problem']]
    for f in q.get(':question/answer-fields',[]):
        parts.extend('- $'+a[':answer/value']+'$' for a in f[':answer-field/choices'])
    if ':question/worked-solution' in q:parts.append(q[':question/worked-solution'])
    return '\n\n'.join(parts)

def main():
    p=argparse.ArgumentParser();p.add_argument('--difficulty',choices=(*LEVEL_FAMILIES,'all'),default='all');p.add_argument('--seed',type=int,default=0);p.add_argument('--count',type=int,default=1);p.add_argument('--format',choices=('markdown','json'),default='markdown');p.add_argument('--template');p.add_argument('--profile');a=p.parse_args()
    levels=LEVEL_FAMILIES if a.difficulty=='all' else [a.difficulty]
    records=[generate(level,a.seed+i,template=a.template,profile=a.profile) for level in levels for i in range(a.count)]
    print(json.dumps(records,indent=2,ensure_ascii=False) if a.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
if __name__=='__main__':main()
