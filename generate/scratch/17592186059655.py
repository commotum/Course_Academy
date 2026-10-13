#!/usr/bin/env python3
"""Expansion → grouping → Pythagorean identity; basis 1356, read-only local records.

Observed replay uses genuinely angle-slotted source masks (including fixed ordered
solutions and full banks). Source masks do not pretend to recover coefficient
ranges or opaque distractor intent. Normal coefficient extensions have separate
explicitly authored banks and solutions. Raw profiles preserve missing attributes
and are evidence-only. See sibling README and extraction for scope and limits.
"""
from pathlib import Path
import argparse, hashlib, json, random, re, uuid
import sympy as sp
KP_ID=17592186059655
VERSION='expand-pythagorean-1'
ROOT=Path(__file__).with_suffix('')
SOURCE=json.loads((ROOT/'source.json').read_text())
KP=SOURCE['record']
QUESTIONS=KP[':knowledge-point/questions']
NAMES=['paired_squares','cos_ratio','cos_reciprocal','cross_ratio','cubic','linear_cos','linear_sin']
OBSERVED=dict(zip(NAMES,QUESTIONS))
LEVELS={'easy':NAMES,'moderate':['cross_single'],'hard':['cross_double']}
X=sp.Symbol('x',real=True)
COS_BANKS={
    'cos_reciprocal_unit': {'a_values':(1,), 'recipes':('a+1','a','0','-a','-(a+1)')},
    'cos_reciprocal_nonunit': {'a_values':(2,3,4,5,6), 'recipes':('a+1','a','1','0','-(a+1)')},
}

def eligible_cos_bank(a):
    matches=[name for name,bank in COS_BANKS.items() if a in bank['a_values']]
    if len(matches)!=1: raise ValueError('no eligible complete cos-reciprocal bank')
    return matches[0]


def digest(x): return hashlib.sha256(json.dumps(x,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def uid(s): return str(uuid.uuid5(uuid.NAMESPACE_URL,s))
def tex(e):
    t=sp.latex(sp.expand(e))
    return re.sub(r'\\(sin|cos)(\^\{[0-9]+\})?\{\\left\(x \\right\)\}',lambda m:chr(92)+m[1]+(m[2] or '')+' x',t)
def scale(k,s): return s if k==1 else ('-'+s if k==-1 else str(k)+s)
def signed(terms):
    out=''
    for k,v in terms:
        if not k: continue
        t=scale(abs(k),v) if v else str(abs(k))
        out+=('-' if k<0 else ('+' if out else ''))+t
    return out or '0'

def angle_mask(text,old,angle):
    # Slots are complete angle tokens, never short replacements in prose/functions.
    if old==r'\theta': return text.replace(old,angle)
    if old=='θ': return text.replace('θ',angle)
    return re.sub(r'(?<![A-Za-z])'+old+r'(?![A-Za-z])',lambda m:angle,text)

def scale_display(expression,k):
    if k==1: return expression
    # Scale a complete mathematical object; never replace a digit inside prose.
    lead=expression[:len(expression)-len(expression.lstrip())]
    trail=expression[len(expression.rstrip()):]
    core=expression.strip(); tail=re.search(r'[=.]+$',core); punctuation=tail[0] if tail else ''
    if punctuation: core=core[:-len(punctuation)]
    return lead+str(k)+r'\left('+core+r'\right)'+punctuation+trail

def scale_source_solution(solution,k):
    if solution is None or k==1: return solution
    def block(match):
        text=match[1]
        begin=r'\begin{aligned}' if r'\begin{aligned}' in text else ''
        end=r'\end{aligned}' if begin else ''
        text=text.replace(begin,'').replace(end,'') if begin else text
        rows=[]
        for row in text.split(r'\\'):
            parts=re.split(r'([=&])',row)
            rows.append(''.join(part if part in ['=','&'] or not part.strip() else scale_display(part,k) for part in parts))
        return '$$'+begin+r'\\'.join(rows)+end+'$$'
    return re.sub(r'\$\$(.*?)\$\$',block,solution,flags=re.S)

def raw_source(name,angle,k=1):
    q=OBSERVED[name]; old={'paired_squares':'x','cos_ratio':'θ','linear_cos':'t','linear_sin':'t'}.get(name,r'\theta')
    # Every source prompt, option and worked-solution goes through the same slots.
    prompt=angle_mask(q[':question/problem'],old,angle)
    solution=angle_mask(q[':question/worked-solution'],old,angle) if ':question/worked-solution' in q else None
    bank=[angle_mask(a[':answer/value'],old,angle) for a in q[':question/answer-fields'][0][':answer-field/choices']]
    present=q[':question/answer-fields'][0].get(':answer-field/correct')
    correct=angle_mask(present[':answer/value'],old,angle) if present else None
    if k!=1:
        prompt=re.sub(r'(?<!\$)\$(?!\$)(.*?)\$(?!\$)',lambda m:'$'+scale_display(m[1],k)+'$',prompt,flags=re.S)
        solution=scale_source_solution(solution,k)
        bank=[scale_display(v,k) for v in bank]
        correct=scale_display(correct,k) if correct is not None else None
    return prompt,solution,bank,correct

def validate_parameters(level,name,p,raw=False):
    if set(p)!={'a','b','d','angle'}: raise ValueError('parameters require exactly a,b,d,angle')
    if p['angle'] not in ['x','t',r'\theta','θ']: raise ValueError('unsupported angle slot')
    for k in ['a','b','d']:
        if type(p[k]) is not int: raise ValueError('integer coefficients required')
    a,b,d=p['a'],p['b'],p['d']
    if raw:
        if not (1<=a<=6 and b==d==1): raise ValueError('observed masks support a common scalar1–6,b=d=1')
        return
    if level=='easy':
        if not (1<=a<=6 and 1<=b<=6 and d==1): raise ValueError('easy coefficient ceiling 6, d=1')
    elif level=='moderate':
        if not (2<=abs(a)<=8 and 1<=b<=6 and d==1): raise ValueError('moderate: 2≤|a|≤8, 1≤b≤6,d=1')
    else:
        if not (2<=abs(a)<=6 and 2<=abs(d)<=6 and a*d>0 and 1<=b<=6): raise ValueError('hard: two nonzero same-sign cross coefficients with magnitude2–6, b1–6')

def normal_math(name,p,bank_profile=None):
    a,b,d=p['a'],p['b'],p['d']; s,c=sp.sin(X),sp.cos(X)
    S,C=r'\sin x',r'\cos x'; SS,CC=r'\sin^{2}x',r'\cos^{2}x'; SC=S+C
    domain='all real angles'
    if name=='paired_squares':
        left=rf'({scale(a,S)}-{scale(a,C)})^{{2}}+({scale(a,S)}+{scale(a,C)})^{{2}}'
        expanded=signed([(a*a,SS),(-2*a*a,SC),(a*a,CC),(a*a,SS),(2*a*a,SC),(a*a,CC)])
        grouped=rf'{2*a*a}({SS}+{CC})'; result=sp.Integer(2*a*a)
        expr=(a*s-a*c)**2+(a*s+a*c)**2
        bank=[result,a*a,-a*a,0,-2*a*a]
    elif name=='cos_ratio':
        left=rf'{CC}({a}+\frac{{{scale(a,SS)}}}{{{CC}}})'; expanded=rf'{scale(a,CC)}+{CC}\cdot\frac{{{scale(a,SS)}}}{{{CC}}}'; grouped=rf'{a}({CC}+{SS})'; result=sp.Integer(a)
        expr=c*c*(a+a*s*s/(c*c)); bank=[result,-a,2*a,0,-2*a]; domain='cos(angle)≠0'
    elif name=='cos_reciprocal':
        left=rf'{C}({C}+\frac{{{a}}}{{{C}}})+{SS}'
        expanded=rf'{CC}+{C}\cdot\frac{{{a}}}{{{C}}}+{SS}'; grouped=rf'{a}+({CC}+{SS})'; result=sp.Integer(a+1)
        if bank_profile not in COS_BANKS or a not in COS_BANKS[bank_profile]['a_values']:
            raise ValueError('selected complete cos-reciprocal bank is ineligible')
        expr=c*(c+a/c)+s*s
        bank=[result,a,0,-a,-a-1] if bank_profile=='cos_reciprocal_unit' else [result,a,1,0,-a-1]
        domain='cos(angle)≠0'
    elif name=='cross_ratio':
        left=rf'{scale(a,C)}{S}(\frac{{{C}}}{{{S}}}+\frac{{{S}}}{{{C}}})'; expanded=rf'{scale(a,C)}{S}\cdot\frac{{{C}}}{{{S}}}+{scale(a,C)}{S}\cdot\frac{{{S}}}{{{C}}}'; grouped=rf'{a}({CC}+{SS})'; result=sp.Integer(a)
        expr=a*c*s*(c/s+s/c); bank=[result,0,-2*a,-a,2*a]; domain='sin(angle)≠0 and cos(angle)≠0'
    elif name=='cubic':
        left=rf'\frac{{{a}}}{{{S}}}(\sin^{{3}}x+{CC}{S})'; expanded=rf'\frac{{{a}\sin^{{3}}x}}{{{S}}}+\frac{{{scale(a,CC)}{S}}}{{{S}}}'; grouped=rf'{a}({SS}+{CC})'; result=sp.Integer(a)
        expr=a/s*(s**3+c*c*s); bank=[result,-a,2*a,0,-2*a]; domain='sin(angle)≠0'
    elif name=='linear_cos':
        left=rf'{C}({a}-{scale(b,C)})-{scale(b,SS)}'; expanded=signed([(a,C),(-b,CC),(-b,SS)]); grouped=rf'{scale(a,C)}-{b}({CC}+{SS})'; result=a*c-b
        expr=c*(a-b*c)-b*s*s; bank=[result,a*c+b,-a*c,-a*c-b,a*c]
    elif name=='linear_sin':
        left=rf'{S}({scale(b,S)}-{a})+{scale(b,CC)}'; expanded=signed([(b,SS),(-a,S),(b,CC)]); grouped=rf'{b}({SS}+{CC})-{scale(a,S)}'; result=b-a*s
        expr=s*(b*s-a)+b*c*c; bank=[result,-b-a*s,a*s,-a*s,b+a*s]
    elif name=='cross_single':
        left=rf'{S}({signed([(a,C),(-b,S)])})-{scale(b,CC)}'; expanded=signed([(a,SC),(-b,SS),(-b,CC)]); grouped=signed([(a,SC)])+rf'-{b}({SS}+{CC})'; result=a*s*c-b
        expr=s*(a*c-b*s)-b*c*c; bank=[result,a*s*c+b,-a*s*c-b,a*s*c, a*s*c-b*s*s]
    else:
        left=rf'{S}({signed([(a,C),(-b,S)])})+{C}({signed([(d,S),(-b,C)])})'
        expanded=signed([(a,SC),(-b,SS),(d,SC),(-b,CC)]); grouped=signed([(a+d,SC)])+rf'-{b}({SS}+{CC})'; result=(a+d)*s*c-b
        expr=s*(a*c-b*s)+c*(d*s-b*c); bank=[result,(a+d)*s*c+b,(a-d)*s*c-b,(a+d)*s*c,(a+d)*s*c-b*s*s]
    bank=[sp.sympify(z) for z in bank]
    if any(sp.trigsimp(bank[i]-bank[j])==0 for i in range(5) for j in range(i)): raise ValueError('whole bank invalid: equivalent options')
    final=tex(result)
    solution='First, we expand the parentheses:\n\n$$\n'+left+' = '+expanded+'\n$$\n\nNext, we group the $\\sin^2 x$ and $\\cos^2 x$ terms.\n\n$$\n'+expanded+' = '+grouped+'\n$$\n\nThen, we use $\\sin^2{x}+\\cos^2{x}=1$ to simplify the expression in the parentheses:\n\n$$\n'+grouped+' = '+final+'\n$$\n\nTherefore, we conclude that\n\n$$\n'+left+' = '+final+'.\n$$'
    prompt='Simplify the trigonometric expression $'+left+'.$'
    return prompt,solution,[tex(z) for z in bank],final,domain

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in LEVELS: raise ValueError('difficulty')
    if field_type not in [None,'radio',':answer-field.type/radio']: raise ValueError('radio only')
    rng=random.Random(seed); name=template or rng.choice(LEVELS[level])
    if name not in LEVELS[level]: raise ValueError('template/difficulty mismatch')
    profile=profile or 'authored'
    bank_profile=profile if profile in COS_BANKS else None
    if bank_profile:
        if name!='cos_reciprocal': raise ValueError('cos-reciprocal bank requires its owning template')
        profile='authored'
    raw=profile in ['observed_raw','observed_completed']
    if profile not in ['authored','observed_raw','observed_completed'] or (raw and name not in OBSERVED): raise ValueError('profile not supported')
    # Choose the complete unit/nonunit bank before sampling its permitted a domain.
    # Explicit parameters determine the unique eligible complete bank; an explicit
    # requested bank never silently switches on an incompatible parameter.
    if name=='cos_reciprocal' and not raw:
        if bank_profile is None:
            bank_profile=eligible_cos_bank(parameters['a']) if parameters is not None else rng.choice(['cos_reciprocal_unit']+['cos_reciprocal_nonunit']*5)
        if parameters is not None and parameters['a'] not in COS_BANKS[bank_profile]['a_values']:
            raise ValueError('explicit parameters outside selected complete bank domain')
    if parameters is None:
        if raw:
            old={'paired_squares':'x','cos_ratio':'θ','linear_cos':'t','linear_sin':'t'}.get(name,r'\theta'); p=dict(a=1,b=1,d=1,angle=old)
        else:
            p=dict(a=rng.choice(COS_BANKS[bank_profile]['a_values']) if bank_profile else rng.randint(1,6),b=rng.randint(1,6),d=1,angle=rng.choice(['x','t',r'\theta']))
            if level=='moderate': p['a']=rng.choice([-1,1])*rng.randint(2,8)
            if level=='hard':
                sign=rng.choice([-1,1]); p['a']=sign*rng.randint(2,6); p['d']=sign*rng.randint(2,6)
    else: p=dict(parameters)
    validate_parameters(level,name,p,raw)
    source=OBSERVED.get(name)
    if raw:
        prompt,solution,bank,correct=raw_source(name,p['angle'],p['a'])
        if profile=='observed_completed' and correct is None:
            correct=scale_display({'paired_squares':'2','cos_ratio':'1'}[name],p['a'])
        domain={'cos_ratio':'cos(angle)≠0','cos_reciprocal':'cos(angle)≠0','cross_ratio':'sin(angle)≠0 and cos(angle)≠0','cubic':'sin(angle)≠0'}.get(name,'all real angles')
        if profile=='observed_completed' and solution is None:
            _,solution,_,_,_=normal_math(name,dict(p,a=1))
            solution=scale_source_solution(solution,p['a'])
            solution=angle_mask(solution,'x',p['angle'])
    else:
        prompt,solution,bank,correct,domain=normal_math(name,p,bank_profile)
        prompt=angle_mask(prompt,'x',p['angle']); solution=angle_mask(solution,'x',p['angle']); bank=[angle_mask(v,'x',p['angle']) for v in bank]; correct=angle_mask(correct,'x',p['angle'])
    identity=digest([VERSION,prompt,solution,sorted(bank),correct])
    f_id=uid(identity+'/selection'); choices=[{':answer/id':uid(f_id+'/'+v),':answer/type':':answer.type/math',':answer/value':v} for v in bank]
    field={':answer-field/id':f_id,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices}
    if correct is not None: field[':answer-field/correct']=[':answer/id',uid(f_id+'/'+correct)]
    rng.shuffle(choices)
    q={':question/id':uid(identity),':question/problem':prompt,':question/answer-fields':[field]}
    if solution is not None: q[':question/worked-solution']=solution
    if profile!='observed_raw' or ':question/difficulty' in source: q[':question/difficulty']=':question.difficulty/'+level
    # Canonical math fingerprint excludes angle aliases, bank profiles, unused coefficients.
    used=['a'] if name in NAMES[:5] else (['a','b','d'] if name=='cross_double' else ['a','b'])
    if name=='paired_squares': semantic={'square_coefficient':p['a'] if raw else p['a']**2}
    elif name=='cos_reciprocal': semantic={'square_coefficient':p['a'] if raw else 1,'cancelled_constant':p['a']}
    elif name in ['linear_cos','linear_sin']: semantic={'a':p['a'],'b':p['a'] if raw else p['b']}
    elif name=='cross_double': semantic={'cross_sum':p['a']+p['d'],'b':p['b']}
    else: semantic={k:p[k] for k in used}
    return {'knowledge_point':{'db_id':KP_ID,'id':KP[':knowledge-point/id'],'title':KP[':knowledge-point/title']},'question':q,'generation':{'version':VERSION,'template':name,'profile':profile,'bank_profile':bank_profile or (profile if raw else name+'_authored'),'bank_eligibility':COS_BANKS[bank_profile]['a_values'] if bank_profile else None,'bank_recipes':COS_BANKS[bank_profile]['recipes'] if bank_profile else None,'original_difficulty':source[':question/difficulty'][':db/ident'].split('/')[-1] if source and ':question/difficulty' in source else None,'difficulty_origin':'inferred completion' if profile=='observed_completed' and source and ':question/difficulty' not in source else ('original absent' if profile=='observed_raw' and source and ':question/difficulty' not in source else ('observed' if raw else 'authored')),'level':level,'seed':seed,'parameters':p,'domain':domain,'source':{k:SOURCE[k] for k in ['database','basis','lineage']},'source_ids':[source[':question/math-academy-id']] if source else [],'origin':('observed replay' if p['a']==1 else 'observed common-scalar mask extension') if raw else 'authored coefficient extension'+(' (missing source level)' if level!='easy' else ''),'evidence_only':raw,'eligible_for_learning':not raw,'content_fingerprint':identity,'mathematical_fingerprint':digest([name,semantic]),'recipes':('observed complete bank; interpretation limited' if raw else 'complete authored expansion/identity operation bank')}}

# EASY: observed expression structures; bounded coefficients ≤6.
def generate_easy(seed=0,**kw): return generate('easy',seed,**kw)
# MODERATE: authored canonical-style single expansion and retained cross term.
def generate_moderate(seed=0,**kw): return generate('moderate',seed,**kw)
# HARD: authored two nonzero expansions and cross-term collection; same identity.
def generate_hard(seed=0,**kw): return generate('hard',seed,**kw)

def markdown(record):
    q=record['question']; g=record['generation']
    difficulty=('Unrated — original difficulty absent' if ':question/difficulty' not in q else ('Inferred '+g['level'].title()+' — original difficulty absent' if g['difficulty_origin']=='inferred completion' else g['level'].title()))
    status='evidence-only' if g['evidence_only'] else 'eligible authored practice'
    rows=[f"### {difficulty} — {g['template']} ({g['origin']}; {g['profile']}; {status}; bank {g['bank_profile']})",q[':question/problem']]
    for f in q.get(':question/answer-fields',[]):
        correct=f.get(':answer-field/correct',[None,None])[1]
        rows.extend(f"- ${a[':answer/value']}$"+(' **correct**' if a[':answer/id']==correct else '') for a in f[':answer-field/choices'])
    if ':question/worked-solution' in q: rows+=['',q[':question/worked-solution']]
    else: rows+=['','Worked solution absent in original evidence.']
    if not any(':answer-field/correct' in f for f in q.get(':question/answer-fields',[])): rows+=['Correct designation absent in original evidence.']
    return '\n\n'.join(rows)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all'); ap.add_argument('--seed',type=int,default=0); ap.add_argument('--count',type=int,default=1); ap.add_argument('--format',choices=['json','markdown'],default='markdown'); ap.add_argument('--template'); ap.add_argument('--profile'); args=ap.parse_args()
    levels=list(LEVELS) if args.difficulty=='all' else [args.difficulty]
    out=[generate(l,args.seed+i,template=args.template,profile=args.profile) for l in levels for i in range(args.count)]
    print(json.dumps(out,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n'.join(map(markdown,out)))
if __name__=='__main__': main()
