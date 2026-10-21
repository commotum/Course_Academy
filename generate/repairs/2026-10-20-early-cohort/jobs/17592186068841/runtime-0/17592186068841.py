#!/usr/bin/env python3
"""Separable ODEs requiring rearrangement before integration (math basis 1356).

Source component masks preserve the complete worked-solution sequence and prose.
Each observed bank is a complete public profile, with symbolic coefficient recipes;
the less transparent wrong shapes are evidence patterns, not recovered intentions.
Normal output repairs domain omissions and the signed-K absolute-value row.
Use profile='observed' to replay original domain wording/teaching error as evidence.
No plots, databases, IVPs, integrating factors, or equation-substitution branches.
See the same-ID evidence directory for extraction, independent checks and review.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import random
import re
import uuid
from functools import lru_cache
import sympy as sp

KP_ID=17592186068841
KP_UUID='74b784e1-ad0e-5cf2-8b02-604a7098c6a9'
TITLE='Finding General Solutions by Rearranging Then Integrating'
VERSION='rearrange-integrate-1'
EVIDENCE=Path(__file__).with_suffix('')
SNAPSHOT=json.loads((EVIDENCE/'source.json').read_text())
QUESTIONS={q[':question/math-academy-id']:q for q in SNAPSHOT['record'][':knowledge-point/questions']}
X,Y,C,K=sp.symbols('x y C K',real=True)
D=sp.Symbol('D',real=True)
DY=r'\frac{\text{d}y}{\text{d}x}'
SOURCE_DEFAULTS={'q-8303':1,'q-8305':1,'q-128191':1,'q-14247':1,
 'q-14253':1,'q-158009':3,'q-158010':1,'q-3854':2,'q-79660':1,
 'q-79663':2,'q-79664':1,'q-79665':1,'q-79666':1,'q-8304':1}
LEVELS={k:q[':question/difficulty'][':db/ident'].split('/')[-1] for k,q in QUESTIONS.items()}
LEVELS.update(easy_linear='easy',easy_constant='easy')
AUTHORED_BANKS={'q-14247','q-14253','q-158009','q-79660','q-79664','q-79665','q-8304'}
DOMAINS={
 'q-8303':r'y>0,\quad x^2+a x+C>0',
 'q-8305':r'K\ne0', 'q-128191':r'x^{a+1}+K\ne0',
 'q-14247':r'K\ne0','q-14253':r'x^2+a x+C\ne0',
 'q-158009':r'x\ne0,\quad K\ne0',
 'q-158010':r'|x|<1,\quad K\ne0','q-3854':r'K\ne0',
 'q-79660':r'x\ne0,\quad K-3a/x\ne0',
 'q-79663':r'K\ne0','q-79664':r'2x^3+a x+C\ne0',
 'q-79665':r'x>0,\quad a x^{3/2}/3+K>0',
 'q-79666':r'a\cos x+C>0',
 'q-8304':r'x>0,\quad 3a\sqrt{x}+K>0',
 'easy_linear':r'K\ne0','easy_constant':r'K\ne0'}

def tex(e):
    return sp.latex(e).replace(r'\log',r'\ln').replace(r'\operatorname{asin}',r'\arcsin').replace(r'\operatorname{atan}',r'\arctan')

def source_tex(e):
    """Compact source notation for complete coefficient/primitive slots."""
    return re.sub(r'(?<![A-Za-z])x\^',r'{x}^',tex(e).replace(' ',''))

def ct(a,term=''):
    """Positive integer coefficient, grouped complete mathematical term."""
    return ('' if a==1 and term else str(a))+term

def component_mask(text,mapping):
    """Compile complete source expression/term slots before rendering.

    All replacements are simultaneous and confined to mathematical spans; no
    short variable/function labels are blindly replaced across prose.
    """
    if not mapping:return text
    pattern=re.compile('|'.join(re.escape(k) for k in sorted(mapping,key=len,reverse=True)))
    def math(m):return pattern.sub(lambda z:mapping[z[0]],m[0])
    return re.sub(r'\$\$.*?\$\$|\$[^$]*?\$',math,text,flags=re.S)

def spec(name,a):
    """Exact separated multiplier g(y), f(x), primitive F and whole bank.

    Recipes are explicit algebraic shapes. Source wrong-operation intention is
    not asserted; each complete profile remains a coherent observed bank.
    """
    f=F=g=None;mapping={};bank=[];correct=0
    if name=='q-8303':
        f=2*X+a;F=X**2+a*X;g=Y**sp.Rational(-1,2)
        p=source_tex(F);mapping={r'{x}^{2}+x':p,r'2x+1':'2x+'+str(a),
          r'-\sqrt{y}':'-'+ct(a,r'\sqrt{y}'),r'+\sqrt{y}':'+'+ct(a,r'\sqrt{y}')}
        bank=[((F+C)/2)**2,F+C,F**2,(F+C)**2,(F/2)**2]
    elif name=='q-8305':
        f=a*sp.cos(X);F=a*sp.sin(X);g=1/Y
        mapping={r'\operatorname{cos}⁡x':ct(a,r'\operatorname{cos}⁡x'),r'\operatorname{sin}⁡x':ct(a,r'\operatorname{sin}⁡x')}
        bank=[K*sp.exp(-a*sp.cos(X)),sp.exp(-a*sp.cos(X))+K,
          sp.exp(F)+K,K*sp.exp(a*sp.cos(X)),K*sp.exp(F)];correct=4
    elif name=='q-128191':
        f=X**a;F=X**(a+1)/(a+1);g=1/Y**2
        # Full x-power, primitive and solved denominator components; derivative
        # labels and 'with respect to x' prose are protected by complete masks.
        mapping={r'{x}^{2}+2C':source_tex(X**(a+1))+f'+{a+1}C',
          r'{x}^{2}+K':source_tex(X**(a+1))+'+K',r'\frac{{x}^{2}}{2}':source_tex(F),
          r'{x}^{2}':source_tex(X**(a+1)),r'x{y}^{2}':source_tex(X**a)+r'{y}^{2}',
          r'=x\end':r'='+source_tex(X**a)+r'\end',r'\int x\,':r'\int '+source_tex(X**a)+r'\,',
          r'\frac{{x}^{2}+2C}{2}':r'\frac{'+source_tex(X**(a+1))+f'+{a+1}C'+'}{'+str(a+1)+'}',
          r'-\frac{2}{':'-'+r'\frac{'+str(a+1)+'}{',r'-2{(':'-'+str(a+1)+r'{(',
          r'-2($':'-'+str(a+1)+'($',r'$K=2C$':f'$K={a+1}C$'}
        bank=[X**(a+1)]
    elif name=='q-14247':
        f=a+3*X**2;F=X**3+a*X;g=1/Y
        mapping={r'y+3y':ct(a,'y')+'+3y',r'1+3{x}^{2}':str(a)+r'+3{x}^{2}',
          r'x+{x}^{3}':ct(a,'x')+r'+{x}^{3}',r'{x}^{3}+x':r'{x}^{3}+'+ct(a,'x')}
        bank=[K*sp.exp(sp.sqrt(X**2+2*a)),K*sp.exp(X**2+2*a*X),
          K*sp.exp(sp.sqrt(F)),K*sp.exp(F),K*sp.exp(3*X**2+a*X)];correct=3
    elif name=='q-14253':
        f=a+2*X;F=X**2+a*X;g=1/Y**2
        mapping={r'={y}^{2}+2':r'='+ct(a,r'{y}^{2}')+'+2',
          r'1+2x':str(a)+'+2x',r'x+{x}^{2}':ct(a,'x')+r'+{x}^{2}',r'{x}^{2}+x':r'{x}^{2}+'+ct(a,'x')}
        bank=[-1/(2*a*X+C),-1/F+C,1/(2*X**2+a*X)+C,1/(X**3+C),-1/(F+C)];correct=4
    elif name=='q-158009':
        f=1/X**2;F=-1/X;g=1/(Y+a)
        mapping={r'& =3':r'& ='+str(a),r'=3$':'='+str(a)+'$',r'y+3':'y+'+str(a),r'y\ne -3':r'y\ne -'+str(a),r'-3.':'-'+str(a)+'.'}
        bank=[K*sp.exp(-a/X),K*sp.exp(-X)-a,K*sp.exp(1/X)+a,K*sp.exp(X)+a,K*sp.exp(F)-a];correct=4
    elif name=='q-158010':
        f=a/sp.sqrt(1-X**2);F=a*sp.asin(X);g=1/Y
        mapping={r'-y &':'-'+ct(a,'y')+' &',r'-y=0':'-'+ct(a,'y')+'=0',r'& =y':r'& ='+ct(a,'y'),r'\frac{1}{\sqrt{1-{x}^{2}}}':r'\frac{'+str(a)+r'}{\sqrt{1-{x}^{2}}}',r'\operatorname{arcsin}⁡x':ct(a,r'\operatorname{arcsin}⁡x')}
        bank=[K*sp.exp(f),K*sp.exp(F),K*sp.exp(a*sp.atan(X)),K*sp.exp(a*sp.sin(X)),K*sp.exp(a*sp.sqrt(1-X**2))];correct=1
    elif name=='q-3854':
        f=a*X+X**2;F=a*X**2/2+X**3/3;g=1/Y
        mapping={r'2yx':ct(a,'yx'),r'2x+{x}^{2}':ct(a,'x')+r'+{x}^{2}',
          r'{x}^{2}+\frac{{x}^{3}}{3}':source_tex(a*X**2/2)+r'+\frac{{x}^{3}}{3}',
          r'{x}^{2}+{x}^{3}/3':source_tex(a*X**2/2)+r'+{x}^{3}/3'}
        bank=[sp.exp(a*X**2/2)+sp.exp(X**3)+K,K*sp.exp(F),F+K,
          sp.log(a*X**2/2)+sp.log(X**3/3)+K,sp.log(a*X**2/2)+sp.log(X**3)+K];correct=1
    elif name=='q-79660':
        f=a/X**2;F=-a/X;g=Y**2
        mapping={r'& =1':r'& ='+str(a),r'=1$':'='+str(a)+'$',
          r'\frac{1}{{x}^{2}}':r'\frac{'+str(a)+r'}{{x}^{2}}',r'\frac{1}{x}':r'\frac{'+str(a)+'}{x}',r'\frac{3}{x}':r'\frac{'+str(3*a)+'}{x}'}
        bank=[(a*K/X+1)**sp.Rational(1,3),(K-a/X)**sp.Rational(1,3),sp.sqrt(K+a/X),sp.sqrt(K-2*a/X),(K-3*a/X)**sp.Rational(1,3)];correct=4
    elif name=='q-79663':
        f=3*X**2+a*X;F=X**3+a*X**2/2;g=1/Y
        mapping={r'2xy':ct(a,'xy'),r'3{x}^{2}+2x':r'3{x}^{2}+'+ct(a,'x'),r'{x}^{3}+{x}^{2}':r'{x}^{3}+'+source_tex(a*X**2/2)}
        bank=[K*sp.exp(sp.sqrt(F)),K*sp.exp(sp.sqrt(f)),K*sp.exp(F),K*sp.exp(sp.diff(f,X)),K*sp.exp(f)];correct=2
    elif name=='q-79664':
        f=6*X**2+a;F=2*X**3+a*X;g=1/Y**2
        mapping={r'-{y}^{2}':'-'+ct(a,r'{y}^{2}'),r'+{y}^{2}':'+'+ct(a,r'{y}^{2}'),r'6{x}^{2}+1':r'6{x}^{2}+'+str(a),r'2{x}^{3}+x':r'2{x}^{3}+'+ct(a,'x')}
        bank=[1/(X**3+a*X**2)+C,-1/(F+C),1/(X**2-a*X)+C,1/(X**3+a*X**2+C),-C/F];correct=1
    elif name=='q-79665':
        f=a*sp.sqrt(X);F=2*a*X**sp.Rational(3,2)/3;g=1/sp.sqrt(Y)
        mapping={r'& =1':r'& ='+str(a),r'=1$':'='+str(a)+'$',r'& =\sqrt{x}':r'& ='+ct(a,r'\sqrt{x}'),
          r'\int \sqrt{x}':r'\int '+ct(a,r'\sqrt{x}'),r'\int {x}^{1/2}':r'\int '+ct(a,r'{x}^{1/2}'),
          r'\frac{2}{3}{x}^{3/2}':tex(2*sp.Rational(a,3))+r'{x}^{3/2}',r'\frac{1}{3}{x}^{3/2}':tex(sp.Rational(a,3))+r'{x}^{3/2}'}
        bank=[(a*X**3+K)**2,(a*X**sp.Rational(3,2)/3+K)**2,a*a*X**sp.Rational(3,2)/9+K,a*a*X**3/9+K,(3*a*sp.sqrt(X)+K)**2];correct=1
    elif name=='q-79666':
        f=-a*sp.sin(X);F=a*sp.cos(X);g=2*Y
        mapping={r'\operatorname{sin}⁡x':ct(a,r'\operatorname{sin}⁡x'),r'\operatorname{cos}⁡x':ct(a,r'\operatorname{cos}⁡x')}
        bank=[sp.exp(F+C),sp.exp(a*sp.sec(X)+C),sp.exp(sp.sqrt(F+C)),sp.sqrt(a*sp.sec(X)+C),sp.sqrt(F+C)];correct=4
    elif name=='q-8304':
        f=a/sp.sqrt(X);F=2*a*sp.sqrt(X);g=sp.sqrt(Y)
        mapping={r'& =1':r'& ='+str(a),r'=1.$':'='+str(a)+'.$',r'\frac{1}{\sqrt{x}}':r'\frac{'+str(a)+r'}{\sqrt{x}}',r'\int {x}^{-1/2}':r'\int '+ct(a,r'{x}^{-1/2}'),r'2{x}^{1/2}':ct(2*a,r'{x}^{1/2}'),r'3{x}^{1/2}':ct(3*a,r'{x}^{1/2}')}
        bank=[3*a*X**sp.Rational(1,3)+K,3*a*sp.sqrt(X)+K,(3*a*sp.sqrt(X)+K)**sp.Rational(2,3),(a*sp.sqrt(X)+K)**sp.Rational(2,3),(a*X**sp.Rational(2,3)+K)**sp.Rational(1,2)];correct=2
    elif name in ('easy_linear','easy_constant'):
        f=-a*(X if name=='easy_linear' else 1);F=sp.integrate(f,X);g=1/Y
        bank=[K*sp.exp(F),K*sp.exp(-F),sp.exp(F)+K,K*sp.exp(f),F+K]
    else:raise ValueError('Unknown template '+name)
    return {'f':f,'F':F,'g':g,'mapping':mapping,'bank':bank,'correct':correct}

def easy_presentation(name,a,s):
    term=tex(a*(X if name=='easy_linear' else 1))+'y'
    ode="y'+"+term+'=0' if a>0 else "y'-"+tex(-a*(X if name=='easy_linear' else 1))+'y=0'
    f,F=tex(s['f']),tex(s['F'])
    prompt='Find the general solution to the differential equation $'+ode+r'$ for $y\ne0.$'
    rows=[ode,DY+'+'+term+' & =0',DY+' & ='+f+'y',r'\frac{1}{y}\cdot '+DY+' & ='+f]
    # Signed coefficients are grouped before addition; avoid +-, -- artifacts.
    rows[1]=DY+('+'+term if a>0 else '-'+tex(-a*(X if name=='easy_linear' else 1))+'y')+' & =0'
    b=lambda r:'$$\n'+r'\begin{aligned}'+r' \\ '.join(r)+r'\end{aligned}'+'\n$$'
    solution='To find the general solution, we first separate the variables:\n\n'+b(rows)
    solution+='\n\nThen, we integrate both sides with respect to $x:$\n\n'+b([
     r'\int \frac{1}{y}\cdot '+DY+r'\,\text{d}x & =\int ('+f+r')\,\text{d}x',
     r'\int \frac{1}{y}\,\text{d}y & =\int ('+f+r')\,\text{d}x',r'\ln|y| & ='+F+'+C'])
    solution+='\n\nTherefore, the general solution to the differential equation (in implicit form) is\n\n$$\n'+r'\ln|y|='+F+'+C.\n$$'
    solution+="\n\nWe're required to write the solution in the form $y=y(x).$ By doing this, we get\n\n"+b([
     r'\ln|y| & ='+F+'+C',r'|y| & =e^{'+F+'+C}',r'|y| & =e^{'+F+r'}\cdot e^C',r'|y| & =K e^{'+F+'}'])
    solution+='\n\nwhere $K=e^C$ and $K>0.$\n\nWe can drop the absolute value bars by allowing $K$ to be either positive or negative. Therefore, the most general solution is\n\n$$\ny=K e^{'+F+'}.\n$$'
    return prompt,solution

def authored_bank(name,a,s):
    """One complete method-based bank, separate from uncertain evidence shapes."""
    f,F=s['f'],s['F'];correct=s['bank'][s['correct']]
    if name=='q-14247':
        bank=[correct,K*sp.exp(-F),sp.exp(F)+K,K*sp.exp(f),K*sp.exp(X**3)]
        recipes=['correct','negate primitive','add constant after exponentiating','use integrand as primitive','omit constant-term primitive']
    elif name in ('q-14253','q-79664'):
        bank=[correct,1/(F+C),-(F+C),-1/F+C,-1/(f+C)]
        recipes=['correct','omit inverse sign','omit reciprocal inversion','add constant after inversion','use integrand as primitive']
    elif name=='q-158009':
        bank=[correct,K*sp.exp(-F)-a,sp.exp(F)+K-a,K*sp.exp(F)+a,K*sp.exp(f)-a]
        recipes=['correct','negate primitive','add constant after exponentiating','wrong shift when solving for y','use integrand as primitive']
    elif name=='q-79660':
        bank=[correct,(K-a/X)**sp.Rational(1,3),sp.sqrt(K-3*a/X),K-3*a/X,(K+3*a/X)**sp.Rational(1,3)]
        recipes=['correct','omit factor three when solving for y','square root instead of cube root','omit cube root','negate primitive']
    elif name=='q-79665':
        P=a*X**sp.Rational(3,2)/3
        bank=[correct,(2*P+K)**2,P+K,(P+K)**3,(a*sp.sqrt(X)+K)**2]
        recipes=['correct','omit division by two','omit square inversion','cube instead of square inversion','use integrand as primitive']
    elif name=='q-8304':
        P=3*a*sp.sqrt(X)
        bank=[correct,P+K,(a*sp.sqrt(X)+K)**sp.Rational(2,3),(P+K)**2,sp.sqrt(P+K)]
        recipes=['correct','omit inversion','omit factor three when solving for y','square instead of power two-thirds','square root instead of power two-thirds']
    else:raise ValueError('No authored complete bank for '+name)
    return bank,recipes

@lru_cache(maxsize=None)
def family_invariant(e):
    constants=e.free_symbols & {C,K}
    if not constants:return ('singleton',sp.simplify(e))
    c=next(iter(constants))
    sols=sp.solve(sp.Eq(e,Y),c)
    if not sols:return ('unsupported',sp.srepr(e))
    invariants=[]
    for z in sols:
        zy=sp.diff(z,Y)
        if zy!=0:invariants.append(sp.simplify(-sp.diff(z,X)/zy))
    return ('family',invariants)

@lru_cache(maxsize=None)
def family_equivalent(v,w):
    """General solution equality modulo affine relabeling of a free constant.

    Eliminate the constant using inverse/log transforms and compare derivatives:
    the constant-free ODE family invariant is more robust than literal C spelling.
    Squared/powered primitives use their unpowered inner expression and therefore
    retain the branch information; missing constants stay singleton functions.
    """
    if sp.simplify(v-w)==0:return True
    iv,iw=family_invariant(v),family_invariant(w)
    if iv[0]!=iw[0]:return False
    if iv[0]=='singleton':return sp.simplify(iv[1]-iw[1])==0
    if iv[0]!='family':return False
    return len(iv[1])==len(iw[1]) and all(any(sp.simplify(a-b)==0 for b in iw[1]) for a in iv[1])

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ('easy','moderate','hard'):raise ValueError('Unknown difficulty')
    rng=random.Random(seed)
    choices=[n for n,l in LEVELS.items() if l==level and (field_type is None or ('blank' if n=='q-128191' else 'radio')==field_type)]
    if template is None:
        if not choices:raise ValueError('No templates for field type')
        template=rng.choice(choices)
    if template not in choices:raise ValueError('Template/level/field mismatch')
    profile=profile or ('authored' if level=='easy' or template in AUTHORED_BANKS else 'repaired')
    allowed=('authored',) if level=='easy' else ('observed','repaired','authored') if template in AUTHORED_BANKS else ('observed','repaired')
    if profile not in allowed:raise ValueError('Unsupported public profile')
    if parameters is None:
        a=rng.choice([i for i in range(-12,13) if i]) if level=='easy' else rng.randint(1,4 if template=='q-128191' else 8)
        parameters={'a':a}
    if set(parameters)!={'a'}:raise ValueError('Exactly the a component parameter is required')
    a=parameters['a']
    if type(a) is not int or (level=='easy' and (not a or abs(a)>12)) or (level!='easy' and not 1<=a<=(4 if template=='q-128191' else 8)):
        raise ValueError('Coefficient outside documented level bounds')
    s=spec(template,a)
    recipes=None
    if template in AUTHORED_BANKS and profile!='observed':
        s['bank'],recipes=authored_bank(template,a,s);s['correct']=0
    if template=='q-3854' and profile=='repaired':
        # Original last two log families differ only by a constant. This is an
        # authored one-option bank repair, not an inferred original operation.
        s['bank'][4]=sp.log(a*X**2/2)+sp.log(X**2)+K
    if level=='easy':prompt,solution=easy_presentation(template,a,s)
    else:
        q=QUESTIONS[template]
        prompt=component_mask(q[':question/problem'],s['mapping'])
        solution=component_mask(q[':question/worked-solution'],s['mapping'])
        if profile!='observed':
            if template=='q-128191':
                prompt+='\n\nGive the nonconstant polynomial term; put the integration constant in $K.$'
            if template in ('q-79665','q-8304'):
                prompt+='\n\nAssume $x>0$ and $y>0.$'
            if template=='q-158009':
                # Delete only the mathematically false signed-K |y+a| row.
                solution=solution.replace(r'\begin{aligned}|y+'+str(a)+r'| & =K{e}^{-1/x} \\ ',r'\begin{aligned}')
                prompt+='\n\nAssume $x\\ne0.$'
            if template=='q-8303':prompt+='\n\nUse an interval where $'+tex(s['F'])+'+C>0.$'
            if template=='q-79665':prompt+='\n\nUse an interval where $'+tex(a*X**sp.Rational(3,2)/3)+'+K>0.$'
            if template=='q-8304':prompt+='\n\nUse an interval where $'+tex(3*a*sp.sqrt(X))+'+K>0.$'
    kind='blank' if template=='q-128191' else 'radio';key='field-1' if kind=='blank' else 'selection'
    values=[tex(v) if kind=='blank' else 'y='+tex(v) for v in s['bank']]
    # Observed wrong log choices require source positive x intervals but are
    # mathematical expressions with nonempty real domains. No domain is guessed.
    if len(set(values))!=len(values):raise ValueError('Complete bank has rendered collision')
    for i,v in enumerate(s['bank']):
        for w in s['bank'][:i]:
            if family_equivalent(v,w) and not (template=='q-3854' and profile=='observed'):
                raise ValueError('Complete bank has equivalent answer families')
    content=json.dumps([VERSION,prompt,solution,sorted(values),values[s['correct']]],ensure_ascii=False)
    fingerprint=hashlib.sha256(content.encode()).hexdigest()
    qid=uuid.uuid5(uuid.NAMESPACE_URL,'kp68841:'+fingerprint);fid=uuid.uuid5(qid,key)
    answers=[{':answer/id':str(uuid.uuid5(fid,v)),':answer/type':':answer.type/math',':answer/value':v} for v in values]
    correct=answers[s['correct']][':answer/id'];rng.shuffle(answers)
    # Mathematical fingerprint excludes bank/profile and uses the actual ODE.
    rhs=sp.simplify(s['f']/s['g'])
    task=hashlib.sha256(sp.srepr(rhs).encode()).hexdigest()
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},
      'question':{':question/id':str(qid),':question/difficulty':':question.difficulty/'+level,
       ':question/problem':prompt,':question/worked-solution':solution,
       ':question/answer-fields':[{':answer-field/id':str(fid),':answer-field/key':key,
        ':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':answers,
        ':answer-field/correct':[':answer/id',correct]}]},
      'generation':{'version':VERSION,'template':template,'parameters':dict(parameters),'seed':seed,
       'bank_profile':profile,'bank_origin':('authored complete operation bank' if level=='easy' or template in AUTHORED_BANKS and profile!='observed' else 'authored one-option repair of observed bank' if template=='q-3854' and profile=='repaired' else 'observed complete symbolic shapes'),
       'bank_recipes':recipes,
       'authored_bank_repair':template=='q-3854' and profile=='repaired',
       'field_normalization':('nonconstant polynomial term; all integration constants in K' if template=='q-128191' and profile!='observed' else None),
       'authored_extension':level=='easy','source_id':QUESTIONS[template][':db/id'] if template in QUESTIONS else None,
       'source_provenance':{k:SNAPSHOT[k] for k in ('database','basis','lineage')},
       'content_fingerprint':fingerprint,'parameter_fingerprint':task,'mathematical_fingerprint':task,
       'domain':re.sub(r'(?<![A-Za-z])a(?![A-Za-z])',str(a),DOMAINS[template]),'plot_rating':'none','plot_assets':{},'sympy_version':sp.__version__,
       'evidence_only':profile=='observed' and template in ('q-158009','q-8303','q-79665','q-8304','q-3854'),
       'normalization':'SymPy answer TeX; complete source mathematical component masks',
       'method':'separate, integrate, solve for y; no IVP or integrating factor'}}

# EASY: authored from the canonical y'+2xy=0, one rearrangement and logarithmic
# primitive, constant or linear x coefficient. |a|<=12, nonzero.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):
    return generate('easy',seed,template,field_type,parameters,profile)

# MODERATE: preserve each of eight source routes, including the fragment blank.
# Coefficient 1..8, or power 1..4 for the observed power-rule blank; same route.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):
    return generate('moderate',seed,template,field_type,parameters,profile)

# HARD: six observed logarithmic-to-exponential routes, including polynomial,
# trigonometric, inverse-trigonometric and affine-y forms. Coefficient 1..8.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):
    return generate('hard',seed,template,field_type,parameters,profile)

def markdown(r):
    q=r['question'];f=q[':question/answer-fields'][0]
    return q[':question/problem']+'\n\n'+'\n'.join(f'{i+1}. ${a[":answer/value"]}$' for i,a in enumerate(f[':answer-field/choices']))+'\n\n'+q[':question/worked-solution']

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all')
    p.add_argument('--seed',type=int,default=0);p.add_argument('--count',type=int,default=1)
    p.add_argument('--format',choices=['markdown','json'],default='markdown')
    p.add_argument('--template');p.add_argument('--profile');args=p.parse_args()
    records=[generate(l,args.seed+i,template=args.template,profile=args.profile) for l in (['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]) for i in range(args.count)]
    print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
