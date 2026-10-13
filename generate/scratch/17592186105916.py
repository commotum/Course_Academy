#!/usr/bin/env python3
"""Scalar projection from magnitude and familiar angle. Steps 3–7 only.

Observed raw profiles preserve missing key presence and all complete historical
banks using homogeneous parameterized expressions. Their error intent cannot
be established from a scalar alone; they are explicitly evidence-only. Normal
radio profiles derive complete banks from cosine/sine, lost sign, omitted
magnitude or denominator, selected BEFORE parameters. Whole-bank collisions
reject an instance; no replacement pools. All three levels share M*cos(theta).
Easy retains all observed workloads. Authored moderate: reduced noninteger
rational magnitude. Authored hard: reduced noninteger rational radical magnitude
with a different nontrivial cosine radical, giving a crossed radical product.
No coordinate products, inverse trig, nonstandard angles or vector answers.
"""
from __future__ import annotations
import argparse, hashlib, json, random, re, sys, uuid
from pathlib import Path
import sympy as sp
KP_ID=17592186105916
KP_UUID='e598ad1e-cee5-5d5f-b2a9-c067e4625cf6'
TITLE='Calculating a Scalar Projection Using Angles and Magnitudes'
VERSION='scalar-angle-1'
ROOT=Path(__file__).with_suffix('')
SOURCE=json.loads((ROOT/'source.json').read_text())
RAW=SOURCE['record'][':knowledge-point/questions']
ANGLES=(30,45,60,90,120,135,150)
# Profile metadata holds display masks, not complete source payloads.
OBSERVED={}

def tex(x):
    return sp.latex(sp.simplify(x)).replace(' ', '')

def parse_scalar(t):
    """Small exact reader for the source scalar grammar (not the generator math)."""
    t=t.replace(' ', '')
    def group(s,i):
        assert s[i]=='{'; depth=1;j=i+1
        while depth:
            depth+=(s[j]=='{')-(s[j]=='}');j+=1
        return s[i+1:j-1],j
    def convert(s):
        out='';i=0
        while i<len(s):
            if s.startswith('\\frac',i):
                a,j=group(s,i+5);b,i=group(s,j);out+='(('+convert(a)+')/('+convert(b)+'))'
            elif s.startswith('\\sqrt',i):
                a,i=group(s,i+5);out+='sqrt('+convert(a)+')'
            elif s[i] in '{}':i+=1
            else:out+=s[i];i+=1
        return out
    from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
    return sp.simplify(parse_expr(convert(t),transformations=standard_transformations+(implicit_multiplication_application,)))

# Recover complete scalar expressions relative to M. This homogeneous family is
# an honest evidence pattern, NOT a recovered misconception or authored default.
for q in RAW:
    sid=q[':question/math-academy-id']; prompt=q[':question/problem']
    mm=re.search(r'\|=(.*?)\$ and',prompt).group(1).strip()
    magnitude=parse_scalar(mm)
    a,b=re.search(r'vectors \$(\w)\$ and \$(\w)\$',prompt).groups()
    at=re.search(r'(?:\\theta|θ)\s*=\s*(.*?)\$',prompt).group(1).rstrip('.')
    if 'pi' in at:
        z=at.replace('\\pi','pi').replace(' ', '');angle=int(parse_scalar(z)*180/sp.pi);unit='radians'
    else:angle=int(re.search(r'\d+',at).group());unit='degrees'
    f=q[':question/answer-fields'][0];kind=f[':answer-field/type'][':db/ident'].split('/')[-1]
    sol=q.get(':question/worked-solution');style=('legacy' if sol is None else 'plain_have' if 'we have' in sol else 'plain' if 'cos\\,' in sol else 'operator')
    profile='observed_'+sid
    OBSERVED[profile]={'source_id':sid,'template':('legacy_radio' if style=='legacy' else kind+'_'+style),
        'parameters':{'coefficient':str(sp.simplify(magnitude/sp.sqrt(2))) if magnitude.has(sp.sqrt(2)) else str(sp.simplify(magnitude/sp.sqrt(3))) if magnitude.has(sp.sqrt(3)) else str(magnitude),
            'radicand':2 if magnitude.has(sp.sqrt(2)) else 3 if magnitude.has(sp.sqrt(3)) else 1,'angle':angle,'unit':unit,'a':a,'b':b},
        'ratios':[str(sp.simplify(parse_scalar(x[':answer/value'])/magnitude)) for x in f[':answer-field/choices']],
        'field_key':f[':answer-field/key'],'kind':kind,'style':style,
        'has_solution':':question/worked-solution' in q,'has_difficulty':':question/difficulty' in q,
        'has_correct':':answer-field/correct' in f,'difficulty':q.get(':question/difficulty',{}).get(':db/ident'),
        'raw_q':q}
TEMPLATES={'radio_operator':'radio','blank_operator':'blank','blank_plain':'blank','blank_plain_have':'blank','legacy_radio':'radio'}
NORMAL_TEMPLATES=tuple(x for x in TEMPLATES if x!='legacy_radio')
PROFILES={'trig_signed':'M cos, M sin, -M cos, M, cos (omit magnitude)',
          'trig_denominator':'M cos, -M cos, 2 M cos (omit trig denominator), cos (omit magnitude), M/2 (use cos60)',
          'right_angle':'0, M (use sine), -M (negative sine), M/2 (cos60), -M/2 (cos120)',
          'blank':'correct scalar only'}

def angle_tex(angle,unit,legacy=False):
    if unit=='degrees':return str(angle)+'^{∘}' if legacy else '{'+str(angle)+'}^{∘}'
    r=sp.Rational(angle,180)
    n=('' if r.p==1 else str(r.p))+r'\pi '
    return n.strip() if r.q==1 else r'\frac{'+n+'}{'+str(r.q)+'}'

def uid(value):return str(uuid.uuid5(uuid.UUID(KP_UUID),value))
def digest(o):return hashlib.sha256(json.dumps(o,sort_keys=True,ensure_ascii=False).encode()).hexdigest()

def guard(level,p,observed=False):
    if set(p)!={'coefficient','radicand','angle','unit','a','b'}:raise ValueError('parameters require exactly coefficient,radicand,angle,unit,a,b')
    c=sp.sympify(p['coefficient']);d=p['radicand'];ang=p['angle']
    if not c.is_Rational or c<=0 or c.p>24 or c.q>4 or type(d)!=int or d not in (1,2,3):raise ValueError('positive reduced rational coefficient numerator <=24, denominator <=4; radicand 1,2,3')
    if type(ang)!=int or ang not in ANGLES or p['unit'] not in ('radians','degrees'):raise ValueError('familiar observed angle required')
    if any(not re.fullmatch('[a-z]',p[k]) for k in ('a','b')) or p['a']==p['b']:raise ValueError('distinct one-letter vectors required')
    if not observed:
        if level=='easy' and c.q!=1:raise ValueError('easy uses observed integer or integer-radical magnitudes')
        if level=='moderate' and (c.p<3 or c.q==1 or d!=1 or ang==90):raise ValueError('moderate needs reduced noninteger rational magnitude and nonzero cosine')
        if level=='hard' and (c.p<3 or c.q==1 or d not in (2,3) or ang not in ((30,150) if d==2 else (45,135))):raise ValueError('hard needs crossed rational radical product')
    return c,sp.simplify(c*sp.sqrt(d)),sp.cos(sp.pi*ang/180)

def sample(level,rng,profile):
    angle=rng.choice(ANGLES if level=='easy' else (30,45,60,120,135,150))
    d=rng.choice((1,2,3)) if level=='easy' else 1 if level=='moderate' else rng.choice((2,3))
    if level=='hard':angle=rng.choice((30,150) if d==2 else (45,135))
    if profile=='right_angle':angle=90
    if profile in ('trig_signed','trig_denominator') and angle==90:angle=rng.choice((30,45,60,120,135,150))
    c=sp.Integer(rng.randint(1,24)) if level=='easy' else sp.Rational(rng.randint(3,24),rng.randint(2,4))
    return {'coefficient':str(c),'radicand':d,'angle':angle,'unit':rng.choice(('degrees','radians')),'a':'a','b':'b'}

def bank_values(profile,M,co,angle):
    si=sp.sin(sp.pi*angle/180);v=M*co
    if profile=='blank':return [v]
    if profile=='right_angle':
        if angle!=90:raise ValueError('right-angle bank requires 90 degrees')
        return [v,M,-M,M/2,-M/2]
    if angle==90:raise ValueError('nonzero cosine bank')
    if profile=='trig_signed':return [v,M*si,-v,M,co]
    if profile=='trig_denominator':return [v,-v,2*v,co,M/2]
    raise ValueError('unknown complete profile')

def prompt_solution(p,M,co,style,kind):
    a,b=p['a'],p['b'];mt=tex(M);at=angle_tex(p['angle'],p['unit'],style=='legacy');ct=tex(co);vt=tex(M*co)
    if style=='legacy':
        prompt=f'Suppose $\\mid {a}|= {mt}$ and the angle between vectors ${a}$ and ${b}$ is $θ = {at}$. Find the scalar projection of ${a}$ onto ${b}$.'
        return prompt,None
    prompt=f'Suppose $|\\,{a}\\,|={mt}$ and the angle between vectors ${a}$ and ${b}$ is $\\theta ={at}.$ Find the scalar projection of ${a}$ onto ${b}.$'
    comp=r'{\text{comp}}_{'+b+r'}\,'+a
    if kind=='blank':prompt+='\n\n$'+comp+'=$\n{{field-1}}'
    product=mt+r'\cdot '+('('+ct+')' if co<0 else ct)
    subst=mt+(r'cos\,(' if style.startswith('plain') else r'\operatorname{cos}⁡(')+at+')'
    opening='Using the formula for the scalar projection, we '+('have' if style=='plain_have' else 'obtain')
    sol=opening+'\n\n$$\n'+r'\begin{aligned}'+comp+r' & =|\,'+a+r'\,|\operatorname{cos}⁡\theta  \\  & ='+subst+r' \\  & ='+product+r' \\  & ='+vt+r'.\end{aligned}'+'\n$$'
    return prompt,sol

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ('easy','moderate','hard'):raise ValueError('difficulty')
    rng=random.Random(seed);obs=OBSERVED.get(profile);raw=False
    if obs:
        raw=True
        if template and template!=obs['template']:raise ValueError('profile/template mismatch')
        template=obs['template'];kind=obs['kind'];style=obs['style']
        p=dict(obs['parameters'] if parameters is None else parameters)
        c,M,co=guard(level,p)
        # Raw source labels are respected, including an absent rating.
        if obs['has_difficulty'] and level!=obs['difficulty'].split('/')[-1]:raise ValueError('observed label mismatch')
        vals=[sp.simplify(M*sp.sympify(r)) for r in obs['ratios']]
    else:
        if profile and profile not in PROFILES:raise ValueError('unknown profile')
        if template is None:
            eligible=list(NORMAL_TEMPLATES)
            if field_type:eligible=[t for t in eligible if TEMPLATES[t]==field_type]
            if profile and profile!='blank':eligible=[t for t in eligible if TEMPLATES[t]=='radio']
            if profile=='blank':eligible=[t for t in eligible if TEMPLATES[t]=='blank']
            if not eligible:raise ValueError('unsupported field type')
            template=rng.choice(eligible)
        if template not in NORMAL_TEMPLATES:raise ValueError('legacy template requires evidence profile')
        kind=TEMPLATES[template];style=template.split('_',1)[1]
        if profile is None:profile='blank' if kind=='blank' else rng.choice(('trig_signed','trig_denominator','right_angle') if level=='easy' else ('trig_signed','trig_denominator'))
        if (kind=='blank')!=(profile=='blank'):raise ValueError('bank/field mismatch')
        if level!='easy' and profile=='right_angle':raise ValueError('right angle would remove authored workload')
        for attempt in range(2000):
            p=dict(parameters) if parameters is not None else sample(level,rng,profile)
            try:
                c,M,co=guard(level,p);vals=[sp.simplify(x) for x in bank_values(profile,M,co,p['angle'])]
                if len(set(map(str,vals)))!=len(vals):raise ValueError('complete ambiguous bank')
                break
            except ValueError:
                if parameters is not None:raise
        else:raise ValueError('no eligible complete instance')
    if field_type and field_type!=kind:raise ValueError('field type mismatch')
    if len(set(map(str,vals)))!=len(vals):raise ValueError('complete ambiguous bank')
    correct=sp.simplify(M*co)
    if sum(sp.simplify(v-correct)==0 for v in vals)!=1:raise ValueError('complete bank lacks exactly one mathematical correct value')
    prompt,solution=prompt_solution(p,M,co,style,kind)
    # Identity from displayed content, presence, level and complete unordered bank.
    presence={'solution':obs['has_solution'] if obs else True,'difficulty':obs['has_difficulty'] if obs else True,'correct':obs['has_correct'] if obs else True}
    ci=digest([VERSION,level if presence['difficulty'] else None,prompt,solution,sorted(tex(v) for v in vals),presence,kind])
    qid=uid(ci);fid=uid(ci+':field')
    answers=[{':answer/id':uid(ci+':answer:'+tex(v)),':answer/type':':answer.type/math',':answer/value':tex(v)} for v in vals]
    f={':answer-field/id':fid,':answer-field/key':obs['field_key'] if obs else 'field-1' if kind=='blank' else 'selection',':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':answers}
    if presence['correct']:f[':answer-field/correct']=[':answer/id',uid(ci+':answer:'+tex(correct))]
    if kind=='radio':rng.shuffle(answers)
    q={':question/id':qid,':question/problem':prompt,':question/answer-fields':[f]}
    if raw:q[':question/math-academy-id']=obs['source_id']
    if presence['difficulty']:q[':question/difficulty']=obs['difficulty'] if obs else ':question.difficulty/'+level
    if presence['solution']:q[':question/worked-solution']=solution
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{
        'version':VERSION,'template':template,'profile':profile,'seed':seed,'parameters':p,'source':{k:SOURCE[k] for k in ('database','basis','lineage')},
        'source_id':obs['source_id'] if obs else None,'origin':'observed homogeneous bank evidence' if raw else 'authored complete method bank; observed prose masks',
        'evidence_only':raw,'eligible_for_learning':not raw,'mathematical_fingerprint':digest([str(M) if co!=0 else 'incidental_at_right_angle',p['angle']]),'content_fingerprint':ci,
        'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__},'plot_rating':'none','correct_value':tex(correct)}}

# EASY: observed integer / integer-radical magnitudes, familiar exact angles.
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
# MODERATE (authored absent level): reduced noninteger rational magnitude, same cosine substitution.
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
# HARD (authored absent level): crossed rational radical product, same four source solution stages.
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)

def markdown(r):
    q=r['question'];out='## '+('Original evidence replay' if r['generation']['evidence_only'] else 'Generated variant')+' / '+q.get(':question/difficulty','unrated').split('/')[-1]+' / '+r['generation']['template']+'\n\n'+q[':question/problem']+'\n\n'
    for f in q.get(':question/answer-fields',[]):
        out+='\n'.join('- $'+a[':answer/value']+'$'+(' **CORRECT**' if f.get(':answer-field/correct',[None,None])[1]==a[':answer/id'] else '') for a in f[':answer-field/choices'])+'\n\n'
    return out+q.get(':question/worked-solution','[Source worked solution absent.]')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=('easy','moderate','hard','all'),default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=('json','markdown'),default='markdown');ap.add_argument('--template');ap.add_argument('--profile');a=ap.parse_args()
    records=[generate(l,a.seed+i,template=a.template,profile=a.profile) for l in (('easy','moderate','hard') if a.difficulty=='all' else (a.difficulty,)) for i in range(a.count)]
    print(json.dumps(records,ensure_ascii=False,indent=2) if a.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
if __name__=='__main__':main()
