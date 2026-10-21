#!/usr/bin/env python3
"""Explicit separable ODE solution families. Snapshot math basis 1356.

Eleven source templates and complete observed banks; all original prose and
ordered mathematical rows are retained by mathematical expression masks.
Observed profiles retain documented bad distractors for evidence replay. Normal
banks apply four actual method errors as a complete bank, never a choice pool.
Only translations with unit derivative vary observed integrands; differential
labels and prose are protected. Hard is authored from canonical/intro examples.
Stop 7: local review records only; no database clients or writes.
"""
from __future__ import annotations
import argparse, hashlib, json, random, re, uuid
from pathlib import Path
from functools import lru_cache
import sympy as s
KP_ID=17592186068840
KP_UUID='16f0876a-33f0-5c6b-9195-8b9a0a550655'
TITLE='Finding a General Solution in Explicit Form'
VERSION='explicit-separable-v1'
ROOT=Path(__file__).with_suffix('')
RAW=json.loads((ROOT/'source.json').read_text())
X,Y,C,K=s.symbols('x y C K',real=True)
Q=RAW['record'][':knowledge-point/questions']
NAMES=['linear_sin','autonomous_tan','temperature_blank','reciprocal_cube','linear_sec2','linear_cos','linear_power','linear_arcsin','linear_sectan','negative_exp','cube_power']
TEMPLATES={name:{'source':q, 'level':q[':question/difficulty'][':db/ident'].split('/')[-1], 'field_type':q[':question/answer-fields'][0][':answer-field/type'][':db/ident'].split('/')[-1]} for name,q in zip(NAMES,Q)}
TEMPLATES.update({'canonical_root':{'level':'hard','field_type':'radio'},'intro_log':{'level':'hard','field_type':'radio'}})
BANK_PROFILES={f'observed_{n}':n for n in NAMES}
BANK_PROFILES.update({'operation_errors':None})

def tex(v):
    return s.latex(v).replace(r'\log',r'\ln').replace(r'\operatorname{asin}',r'\arcsin').replace(r'\operatorname{atan}',r'\arctan')
def block(t):return '$$\n'+t+'\n$$'
def aligned(rows):return block(r'\begin{aligned}'+r' \\ '.join(a+' & ='+b for a,b in rows)+r'\end{aligned}')
def uid(v):return str(uuid.uuid5(uuid.NAMESPACE_URL,v))
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,ensure_ascii=False).encode()).hexdigest()

def expression_mask(text,var='x'):
    """Mask free input symbols in complete math expressions, protect commands/dx.

    Called only on extracted mathematical components (math spans or choices),
    never on shared prose. A symbol used as the name of the independent variable
    in dy/dx, dx, y(x), or the integration instruction is not a substitution slot.
    """
    protected=[]
    def hold(m):protected.append(m[0]);return '§'+str(len(protected)-1)+'§'
    text=re.sub(r'\\(?:text|textrm)\{d\}'+var,hold,text)
    text=re.sub(r'[yT]=[yT]\('+var+r'\)',hold,text)
    text=re.sub(r'\\(?:text|textrm|operatorname)\{[^{}]*\}|\\[A-Za-z]+',hold,text)
    text=re.sub(r'(?<![A-Za-z])'+var+r'(?![A-Za-z])','@ARG@',text)
    for i,v in enumerate(protected):text=text.replace('§'+str(i)+'§',v)
    return text

def shift_math(text,h,var='x',choice=False):
    arg=var if h==0 else '('+var+('+' if h>0 else '-')+str(abs(h))+')'
    if choice:return expression_mask(text,var).replace('@ARG@',arg)
    def span(m):
        part=m[0]
        # Independent-variable-only prose spans are labels, not expressions.
        if part in ('$x:$','$x{:}$','$t,$','$t:$','$x,$'):return part
        return expression_mask(part,var).replace('@ARG@',arg)
    return re.sub(r'\$\$[\s\S]*?\$\$|\$[^$]*?\$',span,text)

def autonomous_render(text,a,choice=False):
    """Original constant coefficient masks, including implied-one integral rows."""
    number=str(a);arg='x' if a==1 else '('+number+'x)'
    if choice:return expression_mask(text).replace('@ARG@',arg)
    def span(m):
        part=m[0]
        if part in ('$x:$','$x{:}$'):return part
        part=expression_mask(part).replace('@ARG@',arg)
        # Replace complete RHS components, never denominators or unrelated 1s.
        rhs=r'{y}^{2}+1'
        scaled=rhs if a==1 else number+'('+rhs+')'
        part=part.replace('& ='+rhs,'& ='+scaled)
        if '′' in part and r'\begin{aligned}' not in part:part=part.replace('='+rhs,'='+scaled)
        part=part.replace(r'& =1\end{aligned}',r'& ='+number+r'\end{aligned}')
        part=part.replace(r'\int \,\text{d}x',r'\int '+('' if a==1 else number)+r'\,\text{d}x')
        return part
    return re.sub(r'\$\$[\s\S]*?\$\$|\$[^$]*?\$',span,text)

def data(name,p):
    """Exact separated primitives and inversions; every family is local/real."""
    u=X+p.get('h',0)
    if name.startswith('linear_'):
        hh,HH={'linear_sin':(s.sin(u),-s.cos(u)), 'linear_cos':(s.cos(u),s.sin(u)), 'linear_sec2':(s.sec(u)**2,s.tan(u)), 'linear_power':(u**2,u**3/3), 'linear_arcsin':(1/s.sqrt(1-u**2),s.asin(u)), 'linear_sectan':(s.sec(u)*s.tan(u),s.sec(u))}[name]
        return hh*Y,1/Y,s.log(s.Abs(Y)),hh,HH,K*s.exp(HH),'exp'
    if name=='autonomous_tan':
        a=p['a'];return a*(Y**2+1),1/(Y**2+1),s.atan(Y),s.Integer(a),a*X,s.tan(a*X+C),'tan'
    if name=='reciprocal_cube':return 2*u/(3*Y**2),3*Y**2,Y**3,2*u,u**2,(u**2+C)**s.Rational(1,3),'root3'
    if name=='negative_exp':return u*s.exp(-Y),s.exp(Y),s.exp(Y),u,u**2/2,s.log(u**2/2+C),'log'
    if name=='cube_power':return 6*u*s.Abs(Y)**s.Rational(2,3),s.Abs(Y)**s.Rational(-2,3)/3,s.real_root(Y,3),2*u,u**2,(u**2+C)**3,'cube'
    if name=='temperature_blank':
        r=s.Rational(str(p['rate']));b=p['ambient']
        return -r*(Y-b),1/(Y-b),s.log(s.Abs(Y-b)),-r,-r*X,b+K*s.exp(-r*X),'temperature'
    a,b,n=p.get('a'),p.get('b'),p.get('n')
    if name=='canonical_root':return a*u**n/Y,Y,Y**2/2,a*u**n,a*u**(n+1)/s.Integer(n+1),s.sqrt(2*a*u**(n+1)/(n+1)+C),'root2'
    if name=='intro_log':return a*s.exp(b*X-Y),s.exp(Y),s.exp(Y),a*s.exp(b*X),s.Rational(a,b)*s.exp(b*X),s.log(s.Rational(a,b)*s.exp(b*X)+C),'log'
    raise ValueError(name)

def invert(kind,z):
    return {'exp':lambda:K*s.exp(z),'tan':lambda:s.tan(z+C),'root3':lambda:(z+C)**s.Rational(1,3),'cube':lambda:(z+C)**3,'log':lambda:s.log(z+C),'root2':lambda:s.sqrt(2*z+C)}[kind]()

def operation_bank(name,p):
    rhs,sep,F,h,H,correct,kind=data(name,p)
    if kind=='temperature':return [s.exp(H)]
    return [correct,invert(kind,h),invert(kind,-H),H+C, (s.exp(H)+K if kind=='exp' else (s.tan(H)+C if kind=='tan' else invert(kind,H).subs(C,0)+C))]

def option_tex(v,kind):
    if kind in ('root3','root2'):
        base=v.base if isinstance(v,s.Pow) and v.exp in (s.Rational(1,3),s.Rational(1,2)) else None
        if base is not None:return 'y='+('\\pm ' if kind=='root2' else '')+(r'\sqrt[3]{' if kind=='root3' else r'\sqrt{')+tex(base)+'}'
    return 'y='+tex(v)

@lru_cache(None)
def family_equivalent(a,b):
    """Complete families modulo supported affine free-constant reparameterization.

    Exponential families are additionally compared by constant nonzero ratio;
    this recognizes arbitrary multiplicative constants and their sign branches.
    Numerical tests are never used to certify equivalence.
    """
    a,b=s.sympify(a),s.sympify(b)
    if a==b:return True
    if a.func==b.func and a.func in (s.log,s.tan):
        return family_equivalent(a.args[0],b.args[0])
    if isinstance(a,s.Pow) and isinstance(b,s.Pow) and a.exp==b.exp:
        return family_equivalent(a.base,b.base)
    fa=K if K in a.free_symbols else C
    fb=K if K in b.free_symbols else C
    if fa in a.free_symbols and fb in b.free_symbols and s.diff(a,fa,2)==0 and s.diff(b,fb,2)==0:
        aa,bb=s.diff(a,fa),s.diff(b,fb)
        ratio=s.simplify(aa/bb)
        if ratio==0 or s.simplify(s.diff(ratio,X))!=0:return False
        offset=s.simplify((a.subs(fa,0)-b.subs(fb,0))/bb)
        return s.simplify(s.diff(offset,X))==0
    return False


def params(name,level,rng,p):
    default={'rate':str(rng.choice(['0.02','0.03','0.04','0.05','0.06'])),'ambient':rng.choice([15,20,25,30,35])} if name=='temperature_blank' else {'h':0 if name=='autonomous_tan' else rng.randint(-8,8)}
    if name=='autonomous_tan':default={'a':rng.randint(1,5)}
    if name=='canonical_root':default={'h':rng.randint(-4,4),'a':rng.choice([1,2,3,4,5]),'n':rng.choice([2,3,4])}
    if name=='intro_log':default={'a':rng.randint(1,5),'b':rng.choice([-5,-4,-3,-2,2,3,4,5])}
    if name=='intro_log':default['a']=abs(default['a'])*(1 if default['b']>0 else -1)
    p=default if p is None else dict(p)
    if set(p)!=set(default):raise ValueError('exact parameter keys required: '+str(set(default)))
    if 'h' in p and (type(p['h']) is not int or abs(p['h'])>(4 if level=='hard' else 8)):raise ValueError('h bound')
    if name=='autonomous_tan' and (type(p['a']) is not int or not 1<=p['a']<=5):raise ValueError('autonomous positive a=1..5; absorbed translations excluded')
    if name=='temperature_blank' and (type(p['rate']) is not str or type(p['ambient']) is not int or str(p['rate']) not in ['0.02','0.03','0.04','0.05','0.06'] or p['ambient'] not in [15,20,25,30,35]):raise ValueError('temperature bounds')
    if level=='hard':
        if type(p['a']) is not int or not 1<=abs(p['a'])<=5:raise ValueError('hard a bound')
        if name=='canonical_root' and (type(p['n']) is not int or p['n'] not in [2,3,4] or p['a']<1):raise ValueError('hard root n/a bounds')
        if name=='intro_log' and p['a']*p['b']<=0:raise ValueError('intro log a/b must be positive for full bank domain')
        if name=='intro_log' and (type(p['b']) is not int or not 2<=abs(p['b'])<=5):raise ValueError('hard b bound')
    return p

def hard_content(name,p):
    rhs,sep,F,h,H,ans,kind=data(name,p)
    prompt='Find the general solution to the differential equation $y\u2032='+tex(rhs)+'.$'
    if kind=='root2':prompt+=' Assume $x'+('+' if p['h']>=0 else '-')+str(abs(p['h']))+'>0.$ Take both sign branches on intervals where the radicand is positive and $y\\ne 0.$'
    else:prompt+=' Work on intervals where the logarithm argument is positive.'
    solution='To find the general solution, we first separate the variables:\n\n'+aligned([("y\u2032",tex(rhs)),(tex(sep)+r'\,\frac{\mathrm{d}y}{\mathrm{d}x}',tex(h))])
    solution+='\n\nThen, we integrate both sides with respect to $x:$\n\n'+aligned([(r'\int '+tex(sep)+r'\,\frac{\mathrm{d}y}{\mathrm{d}x}\,\mathrm{d}x',r'\int '+tex(h)+r'\,\mathrm{d}x'),(r'\int '+tex(sep)+r'\,\mathrm{d}y',r'\int '+tex(h)+r'\,\mathrm{d}x'),(tex(F),tex(H)+'+C')])
    solution+='\n\nTherefore, the general solution to the differential equation (in implicit form) is\n\n'+block(tex(F)+'='+tex(H)+'+C.')
    solution+="\n\nWe're required to write the solution in the form $y=y(x).$ By doing this, we get\n\n"
    if kind=='root2':solution+=aligned([(r'y^2',tex(2*H)+'+2C'),('y',r'\pm\sqrt{'+tex(2*H)+'+2C}'),('y',r'\pm\sqrt{'+tex(2*H)+'+K}')])+'\n\nwhere $K=2C$ is an arbitrary real constant. Use either sign consistently on each interval where the radicand is positive.'
    else:solution+=block(option_tex(ans,kind)+'.')+'\n\nThe logarithm argument must be positive on the solution interval; $C$ is an arbitrary real constant.'
    return prompt,solution

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ['easy','moderate','hard']:raise ValueError('level')
    rng=random.Random(seed)
    if profile and profile not in BANK_PROFILES:raise ValueError('unknown profile')
    if profile and profile.startswith('observed_'):
        inferred=BANK_PROFILES[profile]
        if template and template!=inferred:raise ValueError('profile/template mismatch')
        template=inferred
    eligible=[n for n,t in TEMPLATES.items() if t['level']==level and (field_type is None or field_type==t['field_type'])]
    if template is None:
        if not eligible:raise ValueError('field type')
        template=rng.choice(eligible)
    if template not in eligible:raise ValueError('template/level/field mismatch')
    spec=TEMPLATES[template];profile=profile or 'operation_errors'
    p=params(template,level,rng,parameters)
    rhs,sep,F,h,H,ans,kind=data(template,p)
    raw=spec.get('source')
    observed=profile.startswith('observed_')
    if raw:
        if template=='temperature_blank':
            def render(t):return t.replace('-0.03','-'+str(p['rate'])).replace('25',str(p['ambient']))
        elif template=='autonomous_tan':
            def render(t):return autonomous_render(t,p['a'])
        else:
            def render(t):return shift_math(t,p['h'])
        prompt=render(raw[':question/problem']);solution=render(raw[':question/worked-solution'])
        if not observed:
            if template=='temperature_blank':prompt='Find the general solution to $\\frac{\\mathrm{d}T}{\\mathrm{d}t}=-'+str(p['rate'])+'(T-'+str(p['ambient'])+')$ for $T\\ne '+str(p['ambient'])+'.$\n\n$T='+str(p['ambient'])+r'+K\cdot$ {{field-1}}, where $K$ is an arbitrary nonzero constant. Write the factor as a single exponential with leading coefficient 1.'
            solution+='\n\n'+({'exp':'Here $K$ is arbitrary and nonzero.','root3':'Use the real cube root, on intervals where $y\\ne 0.$','cube':'Use the real cube root during separation, on intervals where $y\\ne 0.$','tan':'Use intervals avoiding tangent poles.','log':'Use intervals where the logarithm argument is positive.','temperature':'Here $K$ is arbitrary and nonzero.'}[kind])
        if not observed and template in ('negative_exp','reciprocal_cube'):prompt+=' Assume $x'+('+' if p['h']>=0 else '-')+str(abs(p['h']))+'>0.$'
        f0=raw[':question/answer-fields'][0]
        if observed:
            values=[(a[':answer/value'].replace('-0.03','-'+str(p['rate'])) if template=='temperature_blank' else (autonomous_render(a[':answer/value'],p['a'],choice=True) if template=='autonomous_tan' else shift_math(a[':answer/value'],p.get('h',0),choice=True))) for a in f0[':answer-field/choices']]
            ci=next(i for i,a in enumerate(f0[':answer-field/choices']) if a[':answer/id']==f0[':answer-field/correct'][':answer/id'])
        else:
            vals=operation_bank(template,p);values=[expression_mask(tex(vals[0])).replace('@ARG@','t')] if kind=='temperature' else [option_tex(v,kind) for v in vals];ci=0
    else:
        prompt,solution=hard_content(template,p);vals=operation_bank(template,p);values=[option_tex(v,kind) for v in vals];ci=0
    if not observed and kind!='temperature':
        vals=operation_bank(template,p)
        for i,a in enumerate(vals):
            for b in vals[i+1:]:
                if family_equivalent(a,b):raise ValueError('reject entire equivalent bank')
    assessed_rhs=-s.Rational(p['rate'])*Y if template=='temperature_blank' else rhs
    fingerprint=digest({'rhs':s.srepr(assessed_rhs),'domain_family':kind})
    identity=digest({'version':VERSION,'prompt':prompt,'solution':solution,'bank':sorted(values)})
    qid=uid(identity);fid=uid(qid+'/field');choices=[{':answer/id':uid(fid+'/'+v),':answer/type':':answer.type/math',':answer/value':v} for v in values]
    correct=choices[ci][':answer/id'];rng.shuffle(choices)
    key='field-1' if spec['field_type']=='blank' else 'selection'
    question={':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+spec['field_type'],':answer-field/choices':choices,':answer-field/correct':[':answer/id',correct]}]}
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':question,'generation':{'version':VERSION,'basis':1356,'lineage':RAW['lineage'],'template':template,'seed':seed,'parameters':p,'bank_profile':profile,'source_id':raw[':db/id'] if raw else None,'authored_level':level=='hard','mathematical_fingerprint':fingerprint,'content_hash':identity,'domain':kind,'observed_bank_anomalies_retained':observed,'sympy_version':s.__version__}}

# EASY: four observed inversion/primitive peers. Translations h in [-8,8]
# preserve unit derivative and familiar primitive workload; tan uses positive a=1..5, with absorbed translations excluded.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):
    """Observed primitive/inversion peers; h=-8..8, tan has positive a=1..5."""
    return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE: seven observed logarithmic separations (one blank). h in [-8,8]
# preserves original primitive and exponentiation; temperature 25 rate/ambient peers.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):
    """Observed logarithmic separations; translated elementary primitives/rates."""
    return generate('moderate',seed,template,field_type,parameters,profile)
# HARD: authored canonical radical and lesson-intro logarithm peers. Both use
# separation, one elementary primitive, explicit inversion and domain/branch care;
# a nonzero |a|<=5; root n=2..4, |h|<=4; log nonunit 2<=|b|<=5.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):
    """Authored canonical root and intro logarithm coefficient/domain peers."""
    return generate('hard',seed,template,field_type,parameters,profile)

def markdown(r):
    q=r['question'];f=q[':question/answer-fields'][0]
    return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$'+(' (correct)' if a[':answer/id']==f[':answer-field/correct'][1] else '') for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['all','easy','moderate','hard'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['json','markdown'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');ap.add_argument('--field-type',choices=['radio','blank']);a=ap.parse_args()
    if a.count<1:ap.error('positive count required')
    levels=['easy','moderate','hard'] if a.difficulty=='all' else [a.difficulty]
    rows=[generate(level,a.seed+i,a.template,a.field_type,profile=a.profile) for level in levels for i in range(a.count)]
    print(json.dumps(rows,indent=2,ensure_ascii=False) if a.format=='json' else '\n\n---\n\n'.join(map(markdown,rows)))
if __name__=='__main__':main()
