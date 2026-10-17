#!/usr/bin/env python3
"""One transformation, eliminate the second variable, then back-substitute.

Captured basis1356; all difficulty policies are authored (both practices unrated).
Raw public source profiles preserve omissions/opaque evidence, never default.
Easy: unit back coefficient, ratio2..7; moderate: nonunit2..3, ratio2..4;
hard: nonunit2..3, ratio5..7. All solutions are signed nonzero integers1..5.
A whole method-derived five-choice bank is selected before parameters; collisions
reject the entire instance. No additional elimination method/branch is introduced.
See sibling17592186192656 and owning topic4026 for the integer workload anchor.
"""
from __future__ import annotations
import argparse, hashlib, json, random, sys, uuid
from pathlib import Path
import sympy as sp
KP_ID=17592186192657
KP_UUID='238f847f-5009-5183-b9bd-b8e136f0ba4d'
TITLE='Solving a System of Equations by Eliminating the Second Variable'
VERSION='second-variable-one-transform-v1'
HERE=Path(__file__).with_suffix('')
SOURCE=json.loads((HERE/'source.json').read_text())
NS=uuid.UUID(KP_UUID)
TEMPLATES=('radio_hint','pair_blank')
RAW={'source_radio':0,'source_blank':1}
PROFILES=('signed_substitution','distribution_division')
LEVELS=('easy','moderate','hard')

def serial(v):
    return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False)
def uid(v):return str(uuid.uuid5(NS,v))
def tex(v):return sp.latex(sp.Rational(v))
def term(c,v):
    c=sp.Rational(c)
    return ('-' if c<0 else '')+('' if abs(c)==1 else tex(abs(c)))+v

def add(parts):
    return ''.join(s if i==0 or s.startswith('-') else '+'+s for i,s in enumerate(parts))
def linear(a,b,x='x',y='y'):return add([term(a,x),term(b,y)])
def relation(a,b,c,x='x',y='y'):return linear(a,b,x,y)+'='+tex(c)
def system(p):
    return r'\left\{\begin{aligned}'+relation(p['a'],p['b'],p['C']).replace('=','&=')+r'\\'+relation(p['c'],p['d'],p['D']).replace('=','&=')+r'\end{aligned}\right.'
def raw_row(a,b,c,style):
    # Full signed terms, preserving original spaces at the observed anchor.
    first=term(a,'x')
    if style=='radio1':return first+(' - ' if b<0 else ' + ')+term(abs(b),'y')+' ='+(' ' if c>=0 else '')+tex(c)
    if style=='radio2':return first+(' - ' if b<0 else ' + ')+term(abs(b),'y')+' ='+(' ' if c>=0 else '')+tex(c)
    return first+(' - ' if b<0 else ' + ')+term(abs(b),'y')+' = '+tex(c)
def prompt(p,template,raw=False):
    if raw:
        mode='radio' if template=='radio_hint' else 'blank'
        sysraw='{'+raw_row(p['a'],p['b'],p['C'],mode+'1')+'; '+raw_row(p['c'],p['d'],p['D'],mode+'2')
        if mode=='radio':return 'Find the solution $(x, y)$ to the following system of equations using the elimination method:\n$'+sysraw+'$\n\n*Hint: Eliminate the variable $y$.*'
        return 'Consider the following system of equations:\n\n$'+sysraw+'$\n\nFind the solution $(x, y)$ to this system by eliminating the variable $y$.\n\nThe solution is $($\n{{field-1}} $$,\n{{field-2}}\n$)$.'
    if template=='radio_hint':return 'Find the solution $(x, y)$ to the following system of equations using the elimination method:\n$$\n'+system(p)+'\n$$\n\n*Hint: Eliminate the variable $y$.*'
    return 'Consider the following system of equations:\n\n$$\n'+system(p)+'\n$$\n\nFind the solution $(x, y)$ to this system by eliminating the variable $y$.\n\nThe solution is $($ {{field-1}} $,$ {{field-2}} $)$.'

def compute(p):
    a,b,c,d,C,D=(sp.Rational(p[k]) for k in ('a','b','c','d','C','D'))
    row=p['row'];k=-d/b if row==1 else -b/d
    aa,bb,CC=(k*a,k*b,k*C) if row==1 else (a,b,C)
    cc,dd,DD=(c,d,D) if row==1 else (k*c,k*d,k*D)
    h=aa+cc;n=CC+DD
    if not h:raise ValueError('singular system')
    x=n/h;y=(D-c*x)/d if row==2 else (C-a*x)/b
    return dict(k=k,aa=aa,bb=bb,CC=CC,cc=cc,dd=dd,DD=DD,h=h,n=n,x=x,y=y)

def guard(level,p,raw=False):
    if set(p)!=set(('a','b','c','d','C','D','row')):raise ValueError('exact parameter keys required')
    if any(isinstance(v,bool) or sp.Rational(v).q!=1 for v in p.values()):raise ValueError('integer parameters required')
    if p['row'] not in (1,2) or any(p[k]==0 for k in ('a','b','c','d')):raise ValueError('nonzero coefficients and row1/2 required')
    z=compute(p)
    if z['k'].q!=1 or abs(z['k'])<=1:raise ValueError('exactly one nonunit integer row scaling required')
    if raw:return z
    back=p['b'] if p['row']==1 else p['d']
    if any(abs(p[k])>7 for k in ('a','c')):raise ValueError('other coefficients bounded1..7')
    if any(z[v].q!=1 or not 1<=abs(z[v])<=5 for v in ('x','y')):raise ValueError('signed integer solution bounds1..5')
    small=abs(back);ratio=abs(z['k'])
    if (sp.gcd(abs(p['a']),abs(p['b']))!=1 or sp.gcd(abs(p['c']),abs(p['d']))!=1):raise ValueError('nonunit workload requires primitive original rows')
    if level=='easy':ok=back==1 and 2<=ratio<=7;ceiling=25
    elif level=='moderate':ok=2<=small<=3 and 2<=ratio<=4;ceiling=35
    else:ok=2<=small<=3 and 5<=ratio<=7;ceiling=40
    if not ok or abs(z['h'])<2 or max(abs(p['C']),abs(p['D']))>ceiling:raise ValueError('level division/multiplier/RHS bounds violated')
    return z

def wrong_bank(p,z,profile):
    x,y=z['x'],z['y'];a,b,c,d,C,D=(sp.Rational(p[k]) for k in ('a','b','c','d','C','D'))
    row=p['row'];A,B,R=(a,b,C) if row==1 else (c,d,D)
    def back(t):return (t,(R-A*t)/B)
    scaled_rhs=C if row==1 else D;unscaled_rhs=D if row==1 else C
    scaled_a=a if row==1 else c;unscaled_a=c if row==1 else a
    h=z['h'];k=z['k']
    omitted_rhs=back((unscaled_rhs+scaled_rhs)/h)
    sign_rhs=back((unscaled_rhs-k*scaled_rhs)/h)
    add_in_back=(x,(R+A*x)/B)
    if profile=='signed_substitution':return [(x,y),omitted_rhs,sign_rhs,add_in_back,(x,-y)]
    if profile=='distribution_division':
        if abs(B)==1:raise ValueError('division bank requires nonunit substitution coefficient')
        den=unscaled_a+scaled_a
        if not den:raise ValueError('omitted coefficient scaling makes denominator zero')
        return [(x,y),back(z['n']/den),omitted_rhs,add_in_back,(x,R-A*x)]
    raise ValueError('unknown authored profile')

def raw_bank(z):
    x,y=z['x'],z['y']
    # Observed offsets are opaque evidence, NOT inferred mistake operations.
    return [('('+tex(x-2)+','+tex(y-3)+')'),('('+tex(x+6)+', '+tex(y+4)+')'),('('+tex(x-2)+', '+tex(y+6)+')'),('('+tex(x)+','+tex(y)+')'),('('+tex(x)+', '+tex(y+3)+')')]
def tuple_tex(v):return '('+tex(v[0])+','+tex(v[1])+')'
def assert_bank(vals):
    if len(set(vals))!=len(vals):raise ValueError('whole bank rejected: duplicate tuples')

def worked(p,z):
    row=p['row'];name='first' if row==1 else 'second';other='second' if row==1 else 'first'
    b,d=p['b'],p['d'];before=b if row==1 else d;opposite=d if row==1 else b
    k=z['k'];x=z['x'];y=z['y']
    annotation=(r'\left('+relation(p['a'],b,p['C'])+r'\right)\cdot ('+tex(k)+')' if row==1 else relation(p['a'],b,p['C']))+'; '+(r'\left('+relation(p['c'],d,p['D'])+r'\right)\cdot ('+tex(k)+')' if row==2 else relation(p['c'],d,p['D']))
    rows=[relation(z['aa'],z['bb'],z['CC']),relation(z['cc'],z['dd'],z['DD']), '('+add([term(z['aa'],'x'),term(z['cc'],'x')])+')=('+add([tex(z['CC']),tex(z['DD'])])+')',term(z['h'],'x')+'='+tex(z['n']),'x='+tex(x)]
    A,B,R=(p['a'],b,p['C']) if row==1 else (p['c'],d,p['D'])
    subs=[relation(A,B,R),add([tex(A)+'('+tex(x)+')',term(B,'y')])+'='+tex(R),add([tex(A*x),term(B,'y')])+'='+tex(R)]
    if B==1:subs+=['y='+tex(y)]
    else:subs+=[term(B,'y')+'='+tex(R-A*x),'y='+tex(y)]
    def block(rs):return '$$\n'+r'\begin{aligned}'+'\n'+(' '+r'\\'+'\n').join(r.replace('=','&=') for r in rs)+'\n'+r'\end{aligned}'+'\n$$'
    return f'Notice that the $y$-coefficient in the first equation is ${tex(b)}$, while in the second equation it is ${tex(d)}$.\n\nIf we multiply the {name} equation by ${tex(k)}$, then the $y$-coefficient will become ${tex(k*before)}$, which will cancel with the coefficient of ${tex(opposite)}$ in the {other} equation.\n\n$$\n\\{{ '+annotation+'\n$$\n\nNow, when we add the two equations, the variable $y$ will be eliminated:\n\n'+block(rows)+f"\n\nSo, the solution must have $x = {tex(x)}$. However, we still need to find $y$. To do this, we substitute $x = {tex(x)}$ back into one of the equations. Let's choose the {name} equation:\n\n"+block(subs)+'\n\nTherefore, the solution to the system of equations is\n\n$$\nx = '+tex(x)+r', \,y = '+tex(y)+'\n$$\n\nwhich can be expressed as $'+tuple_tex((x,y))+'$.'

def sample(level,rng,profile):
    for _ in range(10000):
        row=rng.choice((1,2));small=1 if level=='easy' else rng.choice((2,3))*rng.choice((-1,1))
        ratio=rng.randint(2,7) if level=='easy' else rng.randint(*( (2,4) if level=='moderate' else (5,7)))
        other=small*ratio*rng.choice((-1,1));b,d=(small,other) if row==1 else (other,small)
        a,c=(rng.choice([n for n in range(-7,8) if n]) for _ in range(2))
        x,y=(rng.choice([n for n in range(-5,6) if n]) for _ in range(2))
        p=dict(a=a,b=b,c=c,d=d,C=a*x+b*y,D=c*x+d*y,row=row)
        try:z=guard(level,p);assert_bank(wrong_bank(p,z,profile));return p
        except ValueError:pass
    raise RuntimeError('eligible whole-bank sampling exhausted')

def fingerprint(p,level,z):
    # Remove each complete equation's common signed scaling from task identity.
    # Retain actual collected/back division operands because workload uses them.
    rows=[]
    for ks in (('a','b','C'),('c','d','D')):
        v=[sp.Rational(p[k]) for k in ks];g=sp.gcd_list(v);g=g*(1 if v[0]>0 else -1);rows.append([str(t/g) for t in v])
    return hashlib.sha256(serial([sorted(rows),rows[p['row']-1],str(abs(z['h'])),str(abs(p['b'] if p['row']==1 else p['d']))]).encode()).hexdigest()

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in LEVELS:raise ValueError('difficulty easy/moderate/hard required')
    rng=random.Random(seed);raw=profile in RAW
    if raw:
        required=TEMPLATES[RAW[profile]]
        if template and template!=required:raise ValueError('source profile/template mismatch')
        template=required
        if parameters is None:raise ValueError('raw replay requires explicit parameters')
    else:
        if profile is None:profile=rng.choice(PROFILES if level!='easy' else PROFILES[:1])
        if profile not in PROFILES:raise ValueError('unknown profile')
        if template is None:
            if field_type in ('blank',':answer-field.type/blank'):template='pair_blank'
            elif field_type in ('radio',':answer-field.type/radio'):template='radio_hint'
            else:template=rng.choice(TEMPLATES)
    if template not in TEMPLATES:raise ValueError('unknown template')
    kind='radio' if template=='radio_hint' else 'blank'
    if field_type and field_type not in (kind,':answer-field.type/'+kind):raise ValueError('field type/template mismatch')
    if not raw and level=='easy' and profile=='distribution_division':raise ValueError('easy cannot use nonunit division bank')
    p=dict(parameters) if parameters is not None else sample(level,rng,profile)
    z=guard(level,p,raw)
    if not raw:assert_bank(wrong_bank(p,z,profile))
    text=prompt(p,template,raw)
    vals=raw_bank(z) if raw and kind=='radio' else [tuple_tex(v) for v in wrong_bank(p,z,profile)] if kind=='radio' else [tex(z['x']),tex(z['y'])]
    if kind=='radio':assert_bank(vals)
    solution=None if raw else worked(p,z)
    identity=serial([VERSION,level if not raw else None,text,solution,sorted(vals)])
    qid=uid(identity);q={':question/id':qid,':question/problem':text};fields=[]
    original=SOURCE['record'][':knowledge-point/questions'][RAW[profile]] if raw else None
    if raw:
        q[':db/id']=original[':db/id'];q[':question/math-academy-id']=original[':question/math-academy-id']
    else:q[':question/difficulty']=':question.difficulty/'+level;q[':question/worked-solution']=solution
    keys=['selection'] if kind=='radio' else ['field-1','field-2']
    for i,key in enumerate(keys):
        f={':answer-field/id':uid(qid+key),':answer-field/key':key,':answer-field/type':':answer-field.type/'+kind}
        if raw:f[':db/id']=original[':question/answer-fields'][i][':db/id']
        if kind=='radio' or not raw:
            bank=vals if kind=='radio' else [vals[i]]
            choices=[{':answer/id':uid(qid+key+v),':answer/type':':answer.type/math',':answer/value':v} for v in bank]
            if raw:
                for a,o in zip(choices,original[':question/answer-fields'][i][':answer-field/choices']):a[':db/id']=o[':db/id']
            if not raw:
                correct=tuple_tex((z['x'],z['y'])) if kind=='radio' else vals[i]
                f[':answer-field/correct']=[':answer/id',uid(qid+key+correct)]
            if kind=='radio':rng.shuffle(choices)
            f[':answer-field/choices']=choices
        fields.append(f)
    q[':question/answer-fields']=fields
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'template':template,'profile':profile,'seed':seed,'parameters':p,'source':{k:SOURCE[k] for k in ('database','basis','lineage')},'authored_level':level,'evidence_only':raw,'eligible_for_learning':not raw,'bank_interpretation':'opaque affine source offsets' if raw and kind=='radio' else 'method-derived complete bank' if kind=='radio' else 'coordinate fragments','mathematical_fingerprint':fingerprint(p,level,z),'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__}}}

# Easy: signed integer solutions; unit back coefficient; one nonunit elimination.
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
# Moderate: signed integer solutions; nonunit collected and back-sub divisions.
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
# Hard: same full method, larger familiar multiplier5..7; integer divisions only.
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)

def markdown(r):
    q=r['question'];out=q[':question/problem']
    for f in q.get(':question/answer-fields',[]):
        if ':answer-field/choices' in f:out+='\n\n'+f[':answer-field/key']+': '+', '.join('$'+a[':answer/value']+'$' for a in f[':answer-field/choices'])
    if ':question/worked-solution' in q:out+='\n\n'+q[':question/worked-solution']
    return out
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=(*LEVELS,'all'),default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=('json','markdown'),default='markdown');ap.add_argument('--template');ap.add_argument('--profile');ap.add_argument('--parameters',type=json.loads);args=ap.parse_args()
    rs=[generate(l,args.seed+i,args.template,parameters=args.parameters,profile=args.profile) for l in (LEVELS if args.difficulty=='all' else (args.difficulty,)) for i in range(args.count)]
    print(json.dumps(rs,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in rs))
