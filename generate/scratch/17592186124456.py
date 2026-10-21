#!/usr/bin/env python3
"""Basis-1356 tangent-perpendicular point sets, stages 3–7 only.

Observed replay uses coordinate translations of COMPLETE original question,
field-bank and ordered solution masks. Historical banks have opaque intention
and remain evidence-only, including completed missing-key profiles. Normal
banks are separately authored, complete five-operation banks, selected before
sampling. There are no source-payload return branches or keyed answer tables.
Easy: canonical rank-one quadratic, one linear substitution. Moderate: symmetric
quadratic intersections with two rational points. Hard: q-72440 quadratic
factorization, two unequal integer roots. These are authored scope labels;
source observed difficulties are nine hard and two unrated. No normalization,
new equation-solving branches, plots or database writes.
"""
from __future__ import annotations
import argparse, hashlib, json, random, re, sys, uuid
from pathlib import Path
import sympy as S
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
ROOT=Path(__file__).resolve().parent/'17592186124456'
SNAP=json.loads((ROOT/'source.json').read_text()); REC=SNAP['record']; KP=17592186124456
VERSION='tangent-perpendicular-1.1.0'
GENERATOR_UUID= str(uuid.uuid5(uuid.UUID(REC[':knowledge-point/id']), 'question-generator'))
SUPPORTED_LEVELS=('easy','moderate','hard')
X,Y=S.symbols('x y',real=True)
SOURCES={q[':question/math-academy-id']:q for q in REC[':knowledge-point/questions']}
TRANS=standard_transformations+(implicit_multiplication_application,)
DOMAINS={'easy':{'A':[1,4],'b':[2,5],'r':[-6,6],'r_nonzero':True},'moderate':{'D':[1,3],'m':[2,4],'r':[1,4]},'hard':{'a':[-6,6],'b':[-6,6],'nonzero':True,'a_less_b':True,'a_plus_b_nonzero':True},'observed':{'h':[-3,3],'k':[-3,3],'integers_only':True}}
BANKS={'easy':['solve','wrong_relation_sign','wrong_x_sign','omit_division_b','omit_y_substitution'], 'moderate':['solve','omit_negative_root','omit_positive_root','wrong_relation_sign','swap_coordinates'], 'hard':['solve','omit_second_root','omit_first_root','wrong_x_sign','swap_coordinates']}

def tex(e):return S.latex(S.sympify(e)).replace(r'\left', '').replace(r'\right','')
def parse_math(t):
    t=t.replace('−','-').replace('\\,','').replace('\\ ','').strip().rstrip('.,?')
    # Exact recursive simple fractions; complete bank coefficients are kept exact.
    pat=r'\\frac\{([^{}]*)\}\{([^{}]*)\}'
    while re.search(pat,t):t=re.sub(pat,lambda m:'(('+m[1]+')/('+m[2]+'))',t)
    t=t.replace('{','(').replace('}',')').replace('^','**')
    return parse_expr(t,local_dict={'x':X,'y':Y},transformations=TRANS,evaluate=True)
def pointset(t):
    found=re.findall(r'\(([^(),]+),([^(),]+)\)',t)
    if not found:raise ValueError('No complete coordinate tuples: '+t)
    return tuple(sorted({(S.simplify(parse_math(a)),S.simplify(parse_math(b))) for a,b in found},key=str))
def curve_vector(prompt):
    blocks=re.findall(r'\$([^$]*)\$',prompt)
    equation=next(t for t in blocks if '=' in t);l,r=equation.split('=',1)
    F=S.expand(parse_math(l)-parse_math(r));v=blocks[-1].replace(r'\mathbf','').replace('{','').replace('}','').rstrip('?').strip()
    # Source and normal vectors use i,j only; exact numeric coefficients supported.
    v=v.replace(r'\,','').replace(r'\ ','').replace('i','u').replace('j','v');U,V=S.symbols('u v')
    e=parse_expr(v,local_dict={'u':U,'v':V},transformations=TRANS)
    return F,(S.expand(e).coeff(U),S.expand(e).coeff(V))
def solve_points(F,v,bank=()):
    Fy,Fx=S.diff(F,Y),S.diff(F,X);C=S.expand(v[0]*Fy-v[1]*Fx)
    # EX handles every polynomial/bank coefficient, including exact algebraics.
    allcoeff=[c for e in (F,C)+tuple(c for pts in bank for pair in pts for c in pair) for c in S.Poly(e,X,Y,domain='EX').coeffs()]
    G=S.groebner([F,C],X,Y,domain='EX');solutions=S.solve_poly_system(list(G),X,Y)
    if solutions is None:raise ValueError('Positive-dimensional or unsupported point locus')
    pts=[]
    for a,b in solutions:
        if a.is_real is False or b.is_real is False:continue
        if a.is_real is not True or b.is_real is not True:raise ValueError('Undecidable real point')
        if S.simplify(Fx.subs({X:a,Y:b}))==0 and S.simplify(Fy.subs({X:a,Y:b}))==0:raise ValueError('Nonregular curve point')
        pts.append((S.simplify(a),S.simplify(b)))
    return tuple(sorted(set(pts),key=str)),(Fx,Fy,C),allcoeff

def shown_points(pts,typ='text'):
    tuples=['('+tex(a)+','+tex(b)+')' for a,b in pts]
    if typ=='math':
        if len(tuples)!=1:raise ValueError('Source math field expects one tuple')
        return tuples[0]
    return ' and '.join('$'+t+'$' for t in tuples)+(' only' if len(tuples)==1 else '')

def translate_mask(text,h,k):
    """Transform complete math components only; protect operators/function labels.
    Translation chain derivatives are one. A source x=c becomes x-h=c, keeping
    all original arithmetic rows valid, while constant point tuples become h+c.
    Zero translation is mask evaluation, not a literal-source replay branch.
    """
    def math(m):
        delimiter=m.group(1);t=m.group(2);slots={}
        def protect(z):
            token='QPROTECT'+str(len(slots))+'Q';slots[token]=z.group();return token
        t=re.sub(r'(?:f(?:_[xy]|_\{[xy]\})?|t)\(\s*x\s*,\s*y\s*\)',protect,t)
        t=re.sub(r'∂[xy]|f_[xy]|f_\{[xy]\}',protect,t)
        def pair(z):
            token='QPROTECT'+str(len(slots))+'Q';a,b=pointset(z.group())[0]
            slots[token]=z.group() if h==0 and k==0 else '('+tex(a+h)+','+tex(b+k)+')';return token
        t=re.sub(r'\(([-0-9\\{}frac\s]+),([-0-9\\{}frac\s]+)\)',pair,t)
        # TeX commands are lexed and preserved before single variable tokens.
        pieces=re.split(r'(\\\\|\\[A-Za-z]+)',t)
        for i in range(0,len(pieces),2):
            pieces[i]=re.sub('[xy]',lambda z: z.group() if (h if z.group()=='x' else k)==0 else '('+z.group()+('-'+tex(h if z.group()=='x' else k) if (h if z.group()=='x' else k)>0 else '+'+tex(-(h if z.group()=='x' else k)))+')',pieces[i])
        t=''.join(pieces)
        for key,value in slots.items():t=t.replace(key,value)
        return delimiter+t+delimiter
    return re.sub(r'(\$\$|\$)(.*?)\1',math,text,flags=re.S)

def shift_value(value,h,k):
    def repl(z):
        a,b=pointset(z.group())[0]
        return z.group() if h==0 and k==0 else '('+tex(a+h)+','+tex(b+k)+')'
    return re.sub(r'\(([^(),]+),([^(),]+)\)',repl,value)

def uid(s):return str(uuid.uuid5(uuid.NAMESPACE_URL,'course-academy/tangent-perpendicular/'+s))
def digest(o):return hashlib.sha256(json.dumps(o,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def enum(v):return v[':db/ident'] if isinstance(v,dict) else v

def assemble(level,template,profile,p,prompt,solution,values,types,correct,presence,seed,evidence,origin):
    bank=[pointset(v) for v in values];F,v=curve_vector(prompt);actual,stages,coeff=solve_points(F,v,bank)
    if len(set(bank))!=len(bank):raise ValueError('Reject whole instance: equivalent point-set choices')
    hits=[i for i,b in enumerate(bank) if b==actual]
    if hits!=[correct]:raise ValueError('Reject whole instance: missing/ambiguous correct set')
    # Content ID includes displayed bank but is independent of its order/seed.
    content={'version':VERSION,'prompt':prompt,'solution':solution,'bank':sorted(zip(values,types)),'difficulty':level if presence['difficulty'] else None,'presence':presence}
    fingerprint=digest({'F':str(S.Poly(F,X,Y).monic().as_expr()),'v':str(tuple(S.simplify(c/next(z for z in v if z!=0)) for c in v))})
    key=digest(content);qid=uid(key);fid=uid(key+'/selection')
    answers=[{':answer/id':uid(key+'/selection/'+digest([val,typ])),':answer/type':':answer.type/'+typ,':answer/value':val} for val,typ in zip(values,types)]
    field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':list(answers)}
    if presence['correct']:field[':answer-field/correct']=[':answer/id',answers[correct][':answer/id']]
    random.Random(seed).shuffle(field[':answer-field/choices'])
    question={':question/id':qid,':question/problem':prompt,':question/answer-fields':[field]}
    if presence['difficulty']:question[':question/difficulty']=':question.difficulty/'+level
    if presence['solution']:question[':question/worked-solution']=solution
    return {'knowledge_point':{'db_id':KP,'id':REC[':knowledge-point/id'],'title':REC[':knowledge-point/title']},'question':question,'generation':{'version':VERSION,'seed':seed,'template':template,'profile':profile,'parameters':p,'domain':DOMAINS['observed' if template in SOURCES else level],'source':{k:SNAP[k] for k in ('database','basis','lineage')},'source_ids':[template] if template in SOURCES else ['e-3364' if level=='easy' else 'q-72410' if level=='moderate' else 'q-72440'],'dependencies':{'python':sys.version.split()[0],'sympy':S.__version__},'origin':origin,'evidence_only':evidence,'eligible_for_learning':not evidence,'bank_recipes':(['coordinate_translation_of_complete_observed_bank; intention_opaque'] if evidence else BANKS[level]),'content_hash':key,'mathematical_fingerprint':fingerprint,'actual_points':[[str(a),str(b)] for a,b in actual],'operator_input':str(F),'Fx':str(stages[0]),'Fy':str(stages[1]),'orthogonality':str(stages[2]),'regular_curve':True,'nonzero_given_vector':True,'curve_domain':(['x-h != 0; forced by the displayed curve'] if template=='q-130223' else ['real x,y; retain regular curve points']),'assumptions':['given vector is nonzero','tangent vector is nonzero at every included point'],'coefficient_domain':'EX; complete-bank coefficients included','source_snapshot_sha256':hashlib.sha256((ROOT/'source.json').read_bytes()).hexdigest()}}

def check_params(p,level,observed=False):
    expected={'h','k'} if observed else {'A','b','r'} if level=='easy' else {'D','m','r'} if level=='moderate' else {'a','b'}
    if set(p)!=expected or any(type(v)!=int for v in p.values()):raise ValueError('Exact integer parameter keys required')
    if observed:
        if any(abs(v)>3 for v in p.values()):raise ValueError('Translation domain -3..3')
    elif level=='easy':
        if not (1<=p['A']<=4 and 2<=p['b']<=5 and 1<=abs(p['r'])<=6):raise ValueError('Easy domain')
    elif level=='moderate':
        if not (1<=p['D']<=3 and 2<=p['m']<=4 and 1<=p['r']<=4):raise ValueError('Moderate domain')
    elif not(1<=abs(p['a'])<=6 and 1<=abs(p['b'])<=6 and p['a']<p['b'] and p['a']+p['b']!=0):raise ValueError('Hard domain')

def worked(F,v,pts,condition,relation,substitution,rows):
    # Shared source sentences and ordered method stages; one solution for all choices.
    f=tex(F);fx,fy=S.diff(F,X),S.diff(F,Y);vs=('j' if v==(0,1) else 'i' if v==(1,0) else tex(v[0])+'i+'+tex(v[1])+'j')
    tangent='('+tex(fy)+r')\,i-('+tex(fx)+r')\,j'
    return ('First, we bring all variables to one side:\n\n$$'+f+'=0$$\n\n'+
      'If we set $f(x,y)='+f+'$, our curve can be viewed as the level curve $f(x,y)=0.$\n\n'+
      'A tangent vector to the level curve can be computed as follows:\n\n$$t(x,y)=f_y(x,y)\\,i-f_x(x,y)\\,j$$\n\n'+
      'So, we calculate $t(x,y):$\n\n$$\\begin{aligned}t(x,y)&=\\frac{∂}{∂y}('+f+')\\,i-\\frac{∂}{∂x}('+f+')\\,j\\\\&='+tangent+'\\end{aligned}$$\n\n'+
      'Since our tangent vector needs to be perpendicular to $'+vs+'$, we must have $t\\cdot '+vs+'=0.$\n\n'+
      '$$\\begin{aligned}t(x,y)\\cdot '+vs+'&=0\\\\'+condition+'&=0\\\\'+relation+'\\end{aligned}$$\n\n'+
      'Substituting $'+relation.replace('&','')+'$ into the equation of our curve gives:\n\n$$\\begin{aligned}'+substitution+'&=0\\\\'+'\\\\'.join(rows)+'\\end{aligned}$$\n\nFinally, the corresponding '+('point is ' if len(pts)==1 else 'points are ')+shown_points(pts).replace(' only','')+'.')

# EASY: authored missing level, one linear substitution as in e-3364.
def authored_easy(p):
    A,b,r=(p[k] for k in ('A','b','r'));c=b*r
    F=A*(X+Y)**2-b*Y-c;v=(0,1);pts=((S.Integer(r),S.Integer(-r)),)
    values=[shown_points(z) for z in [pts,((r,r),),((-r,r),),((c,-c),),((r,0),)]]
    relation='y&=-x';sub=tex(A)+r'(x+(-x))^{2}-'+tex(b)+r'(-x)-('+tex(c)+')'
    sol=worked(S.expand(F),v,pts,tex(-2*A*(X+Y)),relation,sub,[tex(b)+r'x-('+tex(c)+')&=0',tex(b)+r'x&='+tex(c),'x&='+tex(r)])
    return F,v,pts,values,sol
# MODERATE: authored missing level, two opposite roots as in q-72410.
def authored_moderate(p):
    D,m,r=p['D'],p['m'],p['r'];F=D*Y**2+2*m*X*Y-m*m*X**2-(D+1)*m*m*r*r;v=(0,1)
    pts=((S.Integer(r),S.Integer(m*r)),(S.Integer(-r),S.Integer(-m*r)))
    values=[shown_points(z) for z in [pts,pts[:1],pts[1:],((r,-m*r),(-r,m*r)),((m*r,r),(-m*r,-r))]]
    relation='y&='+tex(m)+'x';sub=tex(D)+'('+tex(m)+r'x)^{2}+'+tex(2*m)+'x('+tex(m)+r'x)-'+tex(m*m)+r'x^{2}-'+tex((D+1)*m*m*r*r)
    sol=worked(F,v,pts,tex(-S.diff(F,X)),relation,sub,[tex((D+1)*m*m)+r'x^{2}-'+tex((D+1)*m*m*r*r)+'&=0',r'x^{2}&='+tex(r*r),r'x&=\pm '+tex(r)])
    return F,v,pts,values,sol
# HARD: factorable quadratic route q-72440; no harder algebra branch.
def authored_hard(p):
    a,b=p['a'],p['b'];F=X**2+2*X*Y+(a+b)*Y-a*b;v=(0,1)
    pts=((S.Integer(-a),S.Integer(a)),(S.Integer(-b),S.Integer(b)))
    values=[shown_points(z) for z in [pts,pts[:1],pts[1:],((a,a),(b,b)),((a,-a),(b,-b))]]
    relation='x&=-y';sub=r'(-y)^{2}+2(-y)y+('+tex(a+b)+')y-('+tex(a*b)+')'
    sol=worked(F,v,pts,tex(-S.diff(F,X)),relation,sub,[r'-y^{2}+('+tex(a+b)+')y-('+tex(a*b)+')&=0',r'y^{2}-('+tex(a+b)+')y+('+tex(a*b)+')&=0','(y-('+tex(a)+'))(y-('+tex(b)+'))&=0','y&='+tex(a)+r'\text{ or }'+tex(b)])
    return F,v,pts,values,sol

AUTH={'canonical_linear':'easy','symmetric_quadratic':'moderate','factor_quadratic':'hard'}
def sample(level,rng):
    if level=='easy':return {'A':rng.randint(1,4),'b':rng.randint(2,5),'r':rng.choice([v for v in range(-6,7) if v])}
    if level=='moderate':return {'D':rng.randint(1,3),'m':rng.randint(2,4),'r':rng.randint(1,4)}
    a,b=sorted(rng.sample([v for v in range(-6,7) if v],2))
    return {'a':a,'b':b}

def _generate_radio(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ('easy','moderate','hard'):raise ValueError('Unknown difficulty')
    if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Radio field required')
    rng=random.Random(seed)
    if template in SOURCES:
        if profile not in ('observed_raw','observed_completed'):raise ValueError('Opaque historical banks require explicit evidence profile')
        q=SOURCES[template]
        if level!='hard':raise ValueError('Source/evidence templates assigned hard; raw unrated presence retained')
        p={'h':rng.randint(-3,3),'k':rng.randint(-3,3)} if parameters is None else dict(parameters);check_params(p,level,True)
        h,k=p['h'],p['k'];prompt=translate_mask(q[':question/problem'],h,k);solution=translate_mask(q.get(':question/worked-solution',''),h,k)
        f=q[':question/answer-fields'][0];values=[shift_value(a[':answer/value'],h,k) for a in f[':answer-field/choices']];types=[enum(a[':answer/type']).split('/')[-1] for a in f[':answer-field/choices']]
        actual,stages,_=solve_points(*curve_vector(prompt),[pointset(v) for v in values]);hits=[i for i,val in enumerate(values) if pointset(val)==actual]
        if len(hits)!=1:raise ValueError('Unsupported historical bank')
        correct=hits[0];pres={'difficulty':':question/difficulty' in q,'solution':':question/worked-solution' in q,'correct':':answer-field/correct' in f}
        if pres['difficulty'] and level!='hard':raise ValueError('Observed source is hard')
        if pres['correct'] and pointset(shift_value(f[':answer-field/correct'][':answer/value'],h,k))!=actual:raise ValueError('Source wrong key')
        if profile=='observed_completed':
            pres={z:True for z in pres}
            if not solution:
                F,v=curve_vector(prompt);fx,fy,C=stages
                baseF,basev=curve_vector(q[':question/problem']);basepts,basestages,_=solve_points(baseF,basev)
                if template=='q-36332':
                    solution=worked(baseF,basev,basepts,tex(basestages[2]),'y&=x',r'2x(x)+3(x)^{2}-x^{2}-4',[r'4x^{2}&=4',r'x^{2}&=1',r'x&=\pm 1'])
                else:
                    solution=worked(baseF,basev,basepts,tex(basestages[2]),r'y&=x\text{ or }y=-x',r'9x^{2}(x)-3(x)^{3}+6x',[r'6x(x^{2}+1)&=0',r'x&=0'])
                    marker='Finally, the corresponding points are '
                    second=('For the second relation $y=-x$, substitution gives:\n\n$$\\begin{aligned}9x^{2}(-x)-3(-x)^{3}+6x&=0\\\\-6x^{3}+6x&=0\\\\-6x(x-1)(x+1)&=0\\\\x&=0,1,-1\\end{aligned}$$\n\n')
                    solution=solution.replace(marker,second+marker)
                solution=translate_mask(solution,h,k)
        return assemble(level,template,profile,p,prompt,solution,values,types,correct,pres,seed,True,'observed_raw' if profile=='observed_raw' else 'observed_bank_with_inferred_completion')
    template=template or next(t for t,l in AUTH.items() if l==level)
    if AUTH.get(template)!=level:raise ValueError('Wrong level/template')
    profile=profile or 'authored_method_bank'
    if profile!='authored_method_bank':raise ValueError('Unknown authored profile')
    # Profile is selected above, before any parameters are sampled.
    for attempt in range(1000):
        p=dict(parameters) if parameters is not None else sample(level,rng)
        try:
            check_params(p,level);F,v,pts,values,solution=globals()['authored_'+level](p)
            if level=='easy':
                A,b,r=p['A'],p['b'],p['r'];equation=tex(2*A*X*Y+A*Y**2)+'='+tex(b*r+b*Y-A*X**2)
            elif level=='moderate':
                D,m,r=p['D'],p['m'],p['r'];equation=tex(D*Y**2+2*m*X*Y)+'='+tex(m*m*X**2+(D+1)*m*m*r*r)
            else:
                a,b=p['a'],p['b'];equation=tex(X**2+2*X*Y)+'='+tex(-(a+b)*Y+a*b)
            solution=solution.replace('$$'+tex(S.expand(F))+'=0$$', '$$\\begin{aligned}'+equation.replace('=','&=')+r'\\'+tex(S.expand(F))+'&=0\\end{aligned}$$',1)
            prompt='At which '+('point' if len(pts)==1 else 'points')+' on the curve $'+equation+'$ is the tangent vector to the curve perpendicular to the vector $j$?'
            return assemble(level,template,profile,p,prompt,solution,values,['text']*5,0,{z:True for z in ('difficulty','solution','correct')},seed,False,'authored_missing_level' if level!='hard' else 'authored_bank_same_observed_hard_method')
        except ValueError:
            if parameters is not None:raise
    raise ValueError('No eligible complete instance')
def checkbox_coordinates(level,p):
    """Complete current q-72410/q-72440 coordinate profiles, ignoring order.

    Opaque observed coordinate patterns are retained as patterns, not inferred
    misconception claims. Reject the whole profile on coordinate collisions.
    """
    if level=='moderate':
        m,r=S.Integer(p['m']),S.Integer(p['r'])
        return [(-r,-m*r),(0,m*r),(r/2,m*r),(r,0),(r,m*r/2),(r,m*r)]
    a,b=S.Integer(p['a']),S.Integer(p['b'])
    return [(-b,a),(-b,b),(-b/2,b),(-a,a),(-a,b),(a,a),(b,-b)]

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if template in SOURCES or level=='easy':
        return _generate_radio(level,seed,template,field_type,parameters,profile)
    if field_type not in (None,'checkbox',':answer-field.type/checkbox'):
        raise ValueError('Current multi-point templates require checkbox fields')
    if profile not in (None,'current_coordinate_bank'):
        raise ValueError('Current coordinate bank required')
    rng=random.Random(seed)
    for _ in range(1000):
        p=dict(parameters) if parameters is not None else sample(level,rng)
        try:
            old=_generate_radio(level,seed,template,None,p,'authored_method_bank')
            coords=checkbox_coordinates(level,p)
            if len(set(coords))!=len(coords):raise ValueError('Complete coordinate bank collision')
            q=old['question'];correct={tuple(S.sympify(c) for c in point) for point in old['generation']['actual_points']}
            if not correct.issubset(set(coords)):raise ValueError('Missing correct point')
            values=['('+tex(a)+','+tex(b)+')' for a,b in coords]
            key=digest({'version':VERSION,'task':old['generation']['mathematical_fingerprint'],'coordinates':values,'level':level})
            q[':question/id']=uid(key);fields=[];labels=['I','II','III','IV','V','VI','VII']
            for i,(point,val) in enumerate(zip(coords,values)):
                label=labels[i];fid=uid(key+'/'+label)
                choices=[{':answer/id':uid(key+'/'+label+'/'+v),':answer/type':':answer.type/text',':answer/value':v} for v in ('false','true')]
                fields.append({':answer-field/id':fid,':answer-field/key':label,':answer-field/type':':answer-field.type/checkbox',':answer-field/choices':choices,':answer-field/correct':[':answer/id',choices[int(point in correct)][':answer/id']]})
            q[':question/answer-fields']=fields
            q[':question/problem']+='\n\nSelect all that apply. If none apply, leave all boxes unchecked.\n\n'+'\n'.join('- **'+labels[i]+'.** $'+v+'$' for i,v in enumerate(values))
            old['generation'].update(profile='current_coordinate_bank',bank_recipes=['current source coordinate pattern '+str(i+1) for i in range(len(coords))],coordinates=values,content_hash=key,current_source_ids=['q-72410' if level=='moderate' else 'q-72440'])
            return old
        except ValueError:
            if parameters is not None:raise
    raise ValueError('No distinct coordinate bank')

def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)
def markdown(r):
    q=r['question'];g=r['generation'];lines=[f"### {g['template']} / {g['profile']} — {g['origin']}",f"Evidence only: {g['evidence_only']}; parameters: {g['parameters']}",q[':question/problem']]
    for f in q.get(':question/answer-fields',[]):
        key=f.get(':answer-field/correct',[None,None])[1]
        lines.extend(('**CORRECT** ' if a[':answer/id']==key else '')+a[':answer/value'] for a in f[':answer-field/choices'])
        if key is None:lines.append('Original correct designation absent; inferred value retained in author metadata only.')
    lines.append(q.get(':question/worked-solution','Original worked solution absent.'))
    return '\n\n'.join(lines)

# Every learner-facing checkbox question has a nonempty correct selection.
import sys as _policy_sys
from pathlib import Path as _PolicyPath
_policy_sys.path.insert(0, str(next(p for p in _PolicyPath(__file__).resolve().parents if (p / "scripts/generator_policy.py").is_file())))
from scripts.generator_policy import nonempty_checkbox as _nonempty_checkbox
for _policy_name in ['generate', 'generate_easy', 'generate_hard', 'generate_moderate']:
    globals()[_policy_name] = _nonempty_checkbox(globals()[_policy_name])

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=2);ap.add_argument('--template');ap.add_argument('--profile');ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--parameters',type=json.loads)
    args=ap.parse_args();levels=['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]
    records=[generate(l,args.seed+i,template=args.template,profile=args.profile,parameters=args.parameters) for l in levels for i in range(args.count)]
    print(json.dumps(records,indent=2) if args.format=='json' else '\n\n'.join(markdown(r) for r in records))
