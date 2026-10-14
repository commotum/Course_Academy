#!/usr/bin/env python3
"""Draft, local-only natural-log sum differentiation generator (steps 3–7).

Complete source bank profiles remain public evidence. Normal generation selects
complete method-derived banks before parameters, and keeps each family's ordered
formal derivative / term derivative / reduction / evaluation masks. No DB access.
"""
from __future__ import annotations
import argparse, hashlib, json, random, re, sys, uuid
from pathlib import Path
import sympy as sp

KP_ID=17592186096614
ROOT=Path(__file__).resolve().parent/str(KP_ID)
SOURCE=json.loads((ROOT/'source.json').read_text())
KP=SOURCE['record']; TITLE=KP[':knowledge-point/title']; VERSION='1.1.0'
X=sp.Symbol('x',positive=True)
SOURCES={q[':question/math-academy-id']:q for q in KP[':knowledge-point/questions']}
# Each observed record's layout is a separate mask; shared mathematical families
# do not erase distinct term order, reduction rows or point-evaluation omissions.
SPECS={
'q-1919':dict(level='moderate',kind='radio',family='base',p=dict(a=-5,b=1,base=11)),
'q-1920':dict(level='moderate',kind='radio',family='exp-first',p=dict(a=2,b=-5)),
'q-11914':dict(level='easy',kind='radio',family='quadratic',p=dict(a=5,b=-3,c=2)),
'q-339973':dict(level='hard',kind='blank',family='irrational',p=dict(a=2,r='pi',c=1)),
'q-101716':dict(level='easy',kind='radio',family='cubic',p=dict(a=2,b=7,c=-10,d=-1)),
'q-11911':dict(level='easy',kind='radio',family='linear',p=dict(a=1,b=2)),
'q-308854':dict(level='hard',kind='blank',family='power-point',p=dict(a=1,b=3,r='e',t=1)),
'q-340099':dict(level='easy',kind='blank',family='exp-point-unit',p=dict(a=2,b=1,t=1)),
'q-340100':dict(level='easy',kind='blank',family='exp-point-scaled',p=dict(a=-3,b=2,c=4,t=2)),
'q-340104':dict(level='easy',kind='blank',family='base-point',p=dict(a=4,b='-1/3',base=2,c=5,t=2)),
'q-17392':dict(level='hard',kind='radio',family='power-point-negative',p=dict(a=-1,b=2,r='e',t=1)),
}

def num(v):
    return {'pi':sp.pi,'e':sp.E}.get(str(v),sp.sympify(v))
def tex(v):
    return sp.latex(sp.sympify(v),ln_notation=True).replace(r'\left', '').replace(r'\right','').replace('- ', '-')
def coef(v,term):
    v=num(v)
    return term if v==1 else '-'+term if v==-1 else tex(v)+term

def add(*items):
    out=''
    for item in items:
        if item in ('','0'): continue
        out+=item if not out or item.startswith('-') else '+'+item
    return out or '0'
def frac(n,d='x'):
    n=num(n)
    return ('-' if n<0 else '')+r'\frac{'+tex(abs(n))+'}{'+str(d)+'}'
def power(r): return r'{x}^{'+r+'}'
def rp(r): return r'\pi ' if r=='pi' else 'e'

def pieces(name,p):
    """Explicit ordered mathematical component masks, not a simplified CAS chain.

    Return function, derivative-stage RHSs, displayed point-stage RHSs, complete
    historical-bank expressions and correct index. Every source option receives
    one expression-pattern recipe, including opaque ones (evidence only).
    """
    a=num(p['a']); b=num(p.get('b',1)); c=num(p.get('c',0)); d=num(p.get('d',0))
    f=SPECS[name]['family']; ln={'base':'ln⁡x','exp-first':r'\ln x','quadratic':r'\operatorname{ln}x','irrational':r'\operatorname{ln}x','cubic':r'\operatorname{ln}⁡x','linear':'ln⁡x','power-point':'ln⁡x','power-point-negative':'ln⁡x','exp-point-unit':r'\operatorname{ln}⁡x','exp-point-scaled':r'\operatorname{ln}⁡x','base-point':'ln⁡x'}[f]
    L=coef(a,ln); A=frac(a); stages=[]; evaluations=[]
    if f=='base':
        base=p['base']; E='{'+str(base)+'}^{x}'; lb='ln⁡'+str(base)
        F=add(E,L); G=add(E+lb,A)
        stages=[add(E+r'\cdot '+lb,coef(a,r'(\frac{1}{x})')),G]
        bank=[add(E,'-'+lb,A),add(E+'ln⁡x',r'-\frac{1}{x}'),add(lb,frac(-a)),G,add(E,r'-\frac{1}{x}')]; correct=3
    elif f=='exp-first':
        E=coef(b,r'e^{x}'); F=E+' + '+L
        G=E+' + '+A; stages=[G]
        bank=[E+r'\ln x + \frac{1}{x}',E+r'\ln '+tex(b).replace('-', '- ')+' + '+A,r'-e^{x} + \frac{1}{x}',E+r' - \ln 3 + '+A,G]; correct=4
    elif f=='quadratic':
        F=add(L,coef(b,power('2')),coef(c,'x'))
        G=add(A,coef(2*b,'x'),tex(c))
        stages=[add(coef(a,r'(\frac{1}{x})'),coef(b,r'\cdot 2x'),tex(c)),G]
        bank=[add(A,coef(-2*b,'x'),tex(c)),G,add(r'\frac{1}{x}',coef(2*b,'x'),tex(c)),add(A,coef(b,'x^{2}'),tex(c)),add(A,coef(b,'x'),tex(c))]; correct=1
    elif f=='cubic':
        F=add(L,coef(c,'x'),coef(b,power('3')),tex(d)); G=add(A,tex(c),coef(3*b,power('2')))
        stages=[add(coef(a,r'(\frac{1}{x})'),tex(c),coef(3*b,power('2'))),G]
        bank=[add(r'\frac{1}{x}',tex(c),coef(b,power('2'))),add(r'\frac{1}{x}',tex(c),coef(3*b,power('2'))),G,add(A,tex(-c),coef(3*b,power('3'))),add(frac(2*a),tex(-c),coef(3*b,power('2')))]; correct=2
    elif f=='linear':
        F=add(coef(b,'x'),L); G=add(tex(b),A); stages=[G]
        bank=[frac(b),add(tex(b),frac(b)),r'\frac{1}{'+tex(b)+'x}',add(coef(b,'x'),A),G]; correct=4
    elif f=='irrational':
        r=rp(p['r']); P=power(r); D=r+'{x}^{'+r+'-1}'
        F=add(L,P,tex(c)); G=add(A,D)
        stages=[add(coef(a,r'(\frac{1}{x})'),D),G]; bank=[G]; correct=0
    elif f.startswith('power-point'):
        r=rp(p['r']); P=coef(b,power(r)); D=coef(b,r+'{x}^{'+r+'-1}')
        F=add(P,L); G=add(D,A); stages=[G]
        t=p['t']; val=add(coef(b,r),tex(a))
        evaluations=[add(coef(b,r+r'\cdot {'+str(t)+'}^{'+r+'-1}'),frac(a,t)),val]
        if f=='power-point-negative':
            bank=[coef(b,r),val,tex(b),add(coef(b,r),tex(-a)),tex(a)]; correct=1
        else: bank=[val]; correct=0
    else:
        t=p['t']; base=p.get('base','e'); E='{'+str(base)+'}^{x}'
        if f=='base-point': E=tex(b)+r'\cdot '+E
        else: E=coef(b,E)
        F=add(L,E,tex(c)); ED=E+('ln⁡('+str(base)+')' if f=='base-point' else '')
        G=add(A,ED); stages=[G]
        if f=='exp-point-unit':
            ev=add(frac(a,t),'{e}^{'+str(t)+'}'); final=add(tex(a), 'e') if t==1 else add(frac(a,t),'{e}^{'+str(t)+'}')
            evaluations=[ev,final]
        elif f=='exp-point-scaled':
            ev=add(frac(a,t),coef(b,'{e}^{'+str(t)+'}')); evaluations=[ev]
        else:
            ev=add(frac(a,t),tex(b)+r'\cdot {'+str(base)+'}^{'+str(t)+'}ln⁡('+str(base)+')')
            final=add(tex(a/t),coef(b*num(base)**t,'ln⁡('+str(base)+')')); evaluations=[ev,final]
        bank=[evaluations[-1].replace('ln⁡',r'\operatorname{ln}') if f=='base-point' else evaluations[-1]]; correct=0
    return dict(F=F,G=G,stages=stages,evaluations=evaluations,bank=bank,correct=correct)

def substitute(text,pairs):
    """Replace whole component slots once; never cascade short-token changes."""
    mapping=dict(pairs)
    if not mapping:return text
    return re.sub('|'.join(re.escape(k) for k in sorted(mapping,key=len,reverse=True)),lambda m:mapping[m[0]],text)

def render(name,p,raw):
    src=SOURCES[name]; anchor=pieces(name,SPECS[name]['p']); now=pieces(name,p)
    # Complete expressions (including all derivatives and all evaluated terms)
    # are slots, so coefficients never leak into prose or TeX command names.
    pairs=[(anchor['F'],now['F']),(anchor['G'],now['G'])]+list(zip(anchor['stages'],now['stages']))+list(zip(anchor['evaluations'],now['evaluations']))
    prompt=substitute(src[':question/problem'],pairs)
    solution=substitute(src.get(':question/worked-solution',''),pairs)
    if 't' in p:
        old=str(SPECS[name]['p']['t']); new=str(p['t'])
        prompt=prompt.replace('x='+old,'x='+new); solution=solution.replace('x='+old,'x='+new)
    if not raw:
        prompt=prompt.replace('Do not round the answer.','Give an exact answer.')
        if name=='q-1920':
            substituted=add(coef(num(p['b']),r'(e^{x})'),coef(num(p['a']),r'(\frac{1}{x})'))
            solution='Taking the derivative, we have\n\n$$\n'+r'\begin{aligned}\frac{dy}{dx} &=\frac{d}{dx}('+now['F']+') '+r'\\ &= '+substituted+r'\\ &= '+now['G']+r'.\end{aligned}'+'\n$$'
    return prompt,solution,now

# Complete selected banks; q1919/q11911 contain historically opaque errors and
# remain explicit evidence. Normal defaults use real errors of the method.
RECIPES={
 'quadratic':['flip_quadratic_sign','correct','drop_log_coefficient','retain_quadratic','omit_power_multiplier'],
 'cubic':['drop_log_coefficient_and_power_multiplier','drop_log_coefficient','correct','flip_linear_and_retain_cubic_power','double_log_and_flip_linear'],
 'power-point-negative':['omit_log','correct','omit_power_multiplier_and_log','flip_log_sign','omit_power'],
}

def authored_bank(name,p,math):
    a=num(p['a']); b=num(p.get('b',1)); fam=SPECS[name]['family']; G=math['derivative']
    if fam=='linear':
        vals=[G,b+a*sp.log(X),b+1/X,b*X+a/X,a/X]
        recipes=['correct','retain_log','drop_log_coefficient','retain_linear','omit_linear']
    elif fam=='base':
        B=num(p['base']); E=B**X
        vals=[G,E+a/X,E*sp.log(X)+a/X,E*sp.log(B)-a/X,a/X]
        recipes=['correct','omit_exponential_log_factor','use_variable_in_log_factor','flip_log_sign','omit_exponential']
    elif fam=='irrational':
        r=rp(p['r']);D=r+'{x}^{'+r+'-1}'
        vals=[math['target'],1/X+num(p['r'])*X**(num(p['r'])-1),a/X+X**(num(p['r'])-1),a/X+num(p['r'])*X**num(p['r']),-a/X+num(p['r'])*X**(num(p['r'])-1)]
        recipes=['correct','omit_log_coefficient','omit_power_exponent_factor','fail_exponent_decrement','flip_log_derivative_sign']
        return [parts for parts in (add(frac(a),D),add(r'\frac{1}{x}',D),add(frac(a),'{x}^{'+r+'-1}'),add(frac(a),r+'{x}^{'+r+'}'),add(frac(-a),D))],0,recipes
    elif fam=='exp-first':
        vals=[G,-b*sp.exp(X)+a/X,b*sp.exp(X)+1/X,b*sp.exp(X)+a*sp.log(X),a/X]
        recipes=['correct','flip_exponential_sign','drop_log_coefficient','retain_log','omit_exponential']
    else: raise ValueError('No authored radio bank for '+name)
    return [tex(v) for v in vals],0,recipes

def mathematics(name,p):
    a=num(p['a']); b=num(p.get('b',1)); c=num(p.get('c',0)); d=num(p.get('d',0)); f=SPECS[name]['family']
    L=a*sp.log(X)
    if f=='base': F=num(p['base'])**X+L
    elif f=='exp-first': F=b*sp.exp(X)+L
    elif f=='quadratic': F=L+b*X**2+c*X
    elif f=='cubic': F=L+c*X+b*X**3+d
    elif f=='linear': F=b*X+L
    elif f=='irrational': F=L+X**num(p['r'])+c
    elif f.startswith('power-point'): F=b*X**num(p['r'])+L
    else: F=L+b*num(p.get('base','e'))**X+c
    G=sp.diff(F,X); target=G.subs(X,p['t']) if 't' in p else G
    return dict(function=F,derivative=G,target=target)

def validate_parameters(name,p):
    spec=SPECS[name]; anchor=spec['p']
    if set(p)!=set(anchor):raise ValueError('Explicit parameters must have exactly '+str(sorted(anchor)))
    for key,value in p.items():
        if key=='r':
            if value not in ('pi','e'):raise ValueError('Only observed constant exponent forms pi/e')
        elif key=='b' and name=='q-340104':
            v=num(value)
            if v not in [sp.Rational(-i,j) for i in (1,2) for j in (2,3,4)]:raise ValueError('Small negative rational exponential coefficient required')
        elif key=='base':
            if not isinstance(value,int) or not 2<=value<=12:raise ValueError('Base must be integer2..12')
        elif key=='t':
            if value!=(1 if name in ('q-308854','q-17392','q-340099') else 2):raise ValueError('Fixed familiar evaluation point is part of this workload')
        else:
            if not isinstance(value,int) or isinstance(value,bool) or not 1<=abs(value)<=10:raise ValueError('Nonzero integer coefficients with absolute value1..10 required')
    if name in ('q-1919','q-11911','q-1920') and abs(num(p['a']))==1:raise ValueError('Nonunit log coefficient required for eligible authored banks')
    if name=='q-1919' and p['b']!=1:raise ValueError('Observed unit exponential coefficient fixed')
    if name=='q-11911' and abs(p['b'])==1:raise ValueError('Nonunit linear coefficient required')
    if name=='q-11914' and p['b']>=0:raise ValueError('Quadratic negative coefficient fixed role')
    if name=='q-101716' and (p['b']<=0 or p['c']>=0 or p['d']>=0):raise ValueError('Observed signed cubic roles required')
    if name=='q-1920' and p['b']>=-1:raise ValueError('Negative nonunit exponential coefficient required')
    if name=='q-340099' and (p['b']!=1 or p['a']<2):raise ValueError('Unit exponential/positive scaled log role fixed')
    if name=='q-340100' and (p['a']>=0 or p['b']<2 or p['c']<1):raise ValueError('Signed scaled log/exponential/constant roles fixed')
    if name=='q-340104' and (p['a']<2 or p['c']<1 or p['base']>5):raise ValueError('Familiar evaluated base2..5 required')
    if name in ('q-308854','q-17392') and (p['b']<2 or (p['a']<1 if name=='q-308854' else p['a']>=0)):raise ValueError('Irrational-power/sign roles fixed')
    if name=='q-339973' and (abs(p['a'])<2 or p['c']<1):raise ValueError('Nonunit ln coefficient and positive constant required')

def sample(name,rng):
    p=dict(SPECS[name]['p'])
    for k in p:
        if k=='r':p[k]=rng.choice(['pi','e'])
        elif k=='base':p[k]=rng.randint(2,5 if name=='q-340104' else 12)
        elif k=='t':continue
        elif k=='b' and name=='q-340104':p[k]=str(rng.choice([sp.Rational(-i,j) for i in (1,2) for j in (2,3,4)]))
        elif k=='b' and name in ('q-1919','q-340099'):continue
        else:
            sign=-1 if num(p[k])<0 else 1
            p[k]=sign*rng.randint(2 if k in ('a','b') else 1,10)
    return p

def digest(obj):return hashlib.sha256(json.dumps(obj,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def ident(obj):return str(uuid.uuid5(uuid.NAMESPACE_URL,digest(obj)))

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ('easy','moderate','hard'):raise ValueError('Unknown level')
    eligible=[n for n,s in SPECS.items() if s['level']==level and (field_type is None or ('radio' if n=='q-339973' and not (profile and profile.startswith('observed:')) else s['kind'])==field_type)]
    if profile and profile.split(':',1)[0] in ('observed','authored','method'):template=profile.split(':',1)[1] if template is None else template
    if template is not None and template not in eligible:raise ValueError('Template/level/field mismatch')
    rng=random.Random(seed); name=template or rng.choice(eligible); spec=SPECS[name]
    # Whole profile selected BEFORE coefficients. Stable explicit defaults do
    # not depend on seed; seed affects only presentation choice order.
    profile=profile or ('authored:'+name if name in ('q-1919','q-1920','q-11911','q-339973') else 'method:'+name)
    if profile not in ('observed:'+name,'authored:'+name,'method:'+name):raise ValueError('Profile/template mismatch')
    if profile=='method:'+name and name in ('q-1919','q-1920','q-11911','q-339973'):raise ValueError('Opaque banks require observed evidence or authored bank profile')
    if profile.startswith('authored:') and name not in ('q-1919','q-1920','q-11911','q-339973'):raise ValueError('No authored profile')
    raw=profile.startswith('observed:')
    kind='radio' if name=='q-339973' and not raw else spec['kind']
    for _ in range(128):
        p=dict(parameters) if parameters is not None else sample(name,rng)
        # Source q11911 has unit ln coefficient: supported raw evidence retains
        # it; authored bank requires nonunit coefficient to avoid a duplicate.
        if raw and name=='q-11911':
            if p==spec['p']:pass
            else:validate_parameters(name,p)
        else:validate_parameters(name,p)
        prompt,solution,parts=render(name,p,raw); math=mathematics(name,p)
        if not raw and name=='q-339973':prompt=prompt.split('\n\n',1)[0]
        if not raw and name=='q-308854' and p['r']=='e':
            original=parts['bank'][0]; visible=original.replace(coef(num(p['b']),'e'),tex(num(p['b']))+r'\cdot e',1)
            parts['bank']=[visible];solution=solution.replace(original,visible)
        if profile.startswith('authored:'):bank,ci,recipes=authored_bank(name,p,math)
        else:bank,ci=parts['bank'],parts['correct'];recipes=RECIPES.get(spec['family'],['historical_expression_'+str(i) for i in range(len(bank))])
        # Exact evidence q1920 is deliberately ineligible, its malformed ln(-5)
        # cannot be validated as a real-domain distractor. No per-option repair.
        if not raw or name!='q-1920':
            values=[read_math(v) for v in bank]
            if any(sp.simplify(v-w)==0 for i,v in enumerate(values) for w in values[:i]):
                if parameters is not None:raise ValueError('Whole bank rejected: equivalent choices')
                continue
            if sp.simplify(values[ci]-math['target'])!=0:raise AssertionError('Correct expression recipe mismatch')
        break
    else:raise ValueError('Whole-bank bounded sampling exhausted')
    q={':question/problem':prompt}
    src=SOURCES[name]
    if not raw or ':question/difficulty' in src:q[':question/difficulty']=':question.difficulty/'+level
    if not raw or ':question/worked-solution' in src:q[':question/worked-solution']=solution
    fid=ident([VERSION,level,prompt,solution,sorted(bank),kind])
    answers=[]
    for i,value in enumerate(bank):
        ans={':answer/id':ident([fid,'answer',value]),':answer/type':':answer.type/math',':answer/value':value}
        if name=='q-11914':
            feedback=src[':question/answer-fields'][0][':answer-field/choices'][i].get(':answer/feedback')
            # Feedback has its own complete mathematical slots and prose values.
            feedback=feedback.replace('5 ln(x)',str(p['a'])+' ln(x)').replace('5/x',str(p['a'])+'/x').replace('coefficient 5','coefficient '+str(p['a']))
            feedback=feedback.replace('-3x^2',str(p['b'])+'x^2').replace('-6x',str(2*p['b'])+'x').replace('2x]/dx = 2',str(p['c'])+'x]/dx = '+str(p['c']))
            feedback=feedback.replace('-3(2x)',str(p['b'])+'(2x)')
            ans[':answer/feedback']=feedback
        answers.append(ans)
    correct_id=answers[ci][':answer/id']; random.Random(seed).shuffle(answers)
    field={':answer-field/id':fid,':answer-field/key':'selection' if name=='q-339973' and not raw else src[':question/answer-fields'][0][':answer-field/key'],':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':answers}
    if not raw or ':answer-field/correct' in src[':question/answer-fields'][0]:field[':answer-field/correct']=[':answer/id',correct_id]
    q[':question/answer-fields']=[field]
    q[':question/id']=ident([fid,'question'])
    task=digest([sp.srepr(math['function'].diff(X)),p.get('t'),'derivative' if 't' not in p else 'instantaneous rate'])
    return {'knowledge_point':{'db_id':KP_ID,'id':KP[':knowledge-point/id'],'title':TITLE},'question':q,
      'generation':{'version':VERSION,'python_version':sys.version.split()[0],'sympy_version':sp.__version__,'seed':seed,'template':name,'parameters':p,'bank_profile':profile,'source_field_type':spec['kind'],'generated_field_type':kind,'authored_radio_adaptation':name=='q-339973' and not raw,'profile_origin':'observed' if raw else 'authored' if profile.startswith('authored:') else 'observed method bank','eligible_for_learning':not raw,'evidence_only':raw,'authored_extension':not raw,'domain':'x>0 (before differentiation/cancellation)','parameter_fingerprint':task,'content_fingerprint':digest([VERSION,level,prompt,solution,sorted(bank),kind]),'source_analysis':{k:SOURCE[k] for k in ('database','basis','lineage')},'source_ids':[src[':question/id']],'plot_rating':'none','distractor_recipes':recipes}}

# EASY: six observed layouts. Integer-power sums and simple exponential sums;
# point layouts preserve their fixed familiar point and evaluation row omissions.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):
    return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE: observed non-e exponential needs its logarithmic factor. Unrated
# e-exponential signed sum has an explicitly authored level and repaired bank.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):
    return generate('moderate',seed,template,field_type,parameters,profile)
# HARD: constant irrational exponent (pi/e), symbolic successor exponent, and
# optional evaluation at1. No inner function or non-natural logarithm is added.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):
    return generate('hard',seed,template,field_type,parameters,profile)

# Independent displayed-math parser: never consumes generation answer metadata.
# This bounded grammar covers all assessed masks and reports malformed evidence.
def read_math(value):
    from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
    s=value.strip().replace(r'\,','').rstrip('.,').replace('⁡','').replace('−','-').replace(r'\,','').replace(r'\!','')
    s=s.replace(r'\operatorname{ln}','ln').replace(r'\ln','ln').replace(r'\cdot','*').replace(r'\pi','pi')
    s=s.replace(r'\left','').replace(r'\right','')
    def group(text,start):
        if text[start]!='{':raise ValueError('Expected TeX group')
        depth=1;i=start+1
        while depth:
            if i>=len(text):raise ValueError('Unbalanced group')
            depth+=(text[i]=='{')-(text[i]=='}');i+=1
        return text[start+1:i-1],i
    while '\\frac' in s or '\\dfrac' in s:
        m=re.search(r'\\d?frac',s); n,e=group(s,m.end()); den,e2=group(s,e)
        s=s[:m.start()]+'(('+n+')/('+den+'))'+s[e2:]
    s=re.sub(r'ln\s*(\d+|x)(?![a-z])',lambda m:'log('+m[1]+')',s)
    s=re.sub(r'(?<![A-Za-z])e(?![A-Za-z])','EULER',s); s=s.replace('{','(').replace('}',')').replace('^','**'); s=re.sub(r'ln\s*\(', 'log(',s)
    if '\\' in s or 'ln' in s:raise ValueError('Unsupported/malformed expression '+repr(value))
    return parse_expr(s,local_dict={'x':X,'pi':sp.pi,'e':sp.E,'EULER':sp.E,'log':sp.log},transformations=standard_transformations+(implicit_multiplication_application,))

def markdown(rec):
    q=rec['question'];g=rec['generation'];f=q[':question/answer-fields'][0]
    lines=['## '+g['template']+' — '+q.get(':question/difficulty','unrated evidence').split('/')[-1],q[':question/problem'],'']
    for a in f[':answer-field/choices']:lines.append('- $'+a[':answer/value']+'$'+(' (correct)' if f.get(':answer-field/correct',[None,None])[1]==a[':answer/id'] else ''))
    lines+=['',q.get(':question/worked-solution','*Original worked solution absent.*')]
    return '\n'.join(lines)
def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['json','markdown'],default='markdown');ap.add_argument('--template',choices=list(SPECS));ap.add_argument('--profile');args=ap.parse_args()
    if args.count<1 or ((args.template or args.profile) and args.difficulty=='all'):ap.error('Positive count and specific level required for template/profile')
    recs=[]
    for level in (['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]):
        seen=set(); attempt=0
        while len(seen)<args.count:
            if attempt>=max(500,args.count*100):ap.error('Requested count exceeds bounded distinct mathematical tasks')
            record=generate(level,args.seed+attempt,args.template,profile=args.profile);attempt+=1
            key=record['generation']['parameter_fingerprint']
            if key not in seen:seen.add(key);recs.append(record)
    print(json.dumps(recs,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,recs)))
if __name__=='__main__':main()
