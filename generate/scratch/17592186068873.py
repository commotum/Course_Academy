#!/usr/bin/env python3
"""Basis1356 isolated perfect-square rewriting. No equations are solved, no terms
are added/subtracted inside the isolated square, and the linear coefficient stays
positive. Raw source profiles preserve missing labels, keys and solutions;
completed profiles explicitly author these attributes. See adjacent evidence.

Easy: observed sum blanks, a=1..10, outer magnitude1..10.
Moderate: observed difference radio/blanks, a=1..10, magnitude1..10.
Hard: authored difference, explicit numerical square a² (not supplied a^2),
a=11..15, magnitude1..10. Same factoring operation, greater square recognition
workload only. Authored design, no observed hard label. Family/bank first, then
whole-instance rejection; all public explicit calls enforce identical bounds.
"""
from __future__ import annotations
import argparse, hashlib, json, random, re, sys, uuid
from pathlib import Path
import sympy as sp
KP_ID=17592186068873
KP_UUID='f10e4a34-a512-5ff4-abbc-66e6830d63d0'
TITLE='Completing the Square When the Perfect Square is Isolated'
VERSION='isolated-square-1'
HERE=Path(__file__).with_suffix('')
SOURCE=json.loads((HERE/'source.json').read_text())
QUESTIONS={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
# Each layout is an observed prompt/solution family, not a number variant skill.
CONFIG={
'q-140186':('moderate','x',3,2,-1,'number','radio'),
'q-140271':('easy','y',2,1,1,'power','radio'),
'q-250399':('moderate','x',3,2,-1,'power','blank'),
'q-141513':('moderate','y',6,3,-1,'power','radio'),
'q-250392':('easy','x',7,1,1,'number','blank'),
'q-250395':('easy','x',6,4,1,'power','blank'),
'q-250396':('easy','y',10,7,1,'power','blank'),
'q-250397':('moderate','x',2,3,-1,'number','blank'),
}
# Observed bank algebra; q141513's a-2 choice is opaque evidence, never default.
BANKS={'q-140186':['a','-a','2*a','a*a','-2*a'],
'q-140271':['2*a','4*a','a','-2*a','-a'],
'q-141513':['a-2','-a/2','a/2','-a','a']}
DEFAULT_BANK=['a','-a','2*a','a/2','-2*a']

def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(x):return str(uuid.uuid5(uuid.NAMESPACE_URL,VERSION+':'+str(x)))
def tex(q):return sp.latex(sp.Rational(q))
def enum(v):return v[':db/ident'] if isinstance(v,dict) else v

def math_variable(text,old,new):
    # Complete math regions only; prose "expression" and commands are untouched.
    return re.sub(r'\$\$.*?\$\$|\$[^$]*\$',lambda m:re.sub(r'(?:(?<![A-Za-z\\])|(?<=a))'+old+r'(?![A-Za-z])',new,m[0]),text,flags=re.S)

def masked(text,sid):
    """Compile numerical masks once, matching full mathematical components.
    Outer constant is selected only after an isolated expression/square, never
    by blind replacement of a scalar that might also be a linear coefficient.
    """
    _,v,a,k,sign,notation,_=CONFIG[sid]
    # Keep literal exponent2 and identity coefficient2. Numeric constant terms
    # in each trinominal are distinguished by trailing position.
    text=math_variable(text,v,'VARSLOT')
    # math_variable protects prose but VARSLOT is now a complete variable token.
    # Numeric role masks, applied only within math segments.
    def region(m):
        t=m[0]
        # Constant after the enclosing perfect-square expression or square.
        t=re.sub(r'(?<=\))\s*([+-])\s*'+str(k)+r'\b',lambda n:re.sub(str(k)+r'\b','KSLOT',n[0]),t)
        t=re.sub(r'(\^\{2\})\s*([+-])\s*'+str(k)+r'\b',lambda n:n[0][:-len(str(k))]+'KSLOT',t)
        # Last blank answer coefficient is outside math in prompt; handled later.
        # a as explicitly supplied base of square, but never variable exponent.
        t=re.sub(r'\{'+str(a)+r'\}\^\{2\}',r'{ASLOT}^{2}',t)
        t=re.sub(r'(?<![\w])'+str(a)+r'\^\{2\}',r'ASLOT^{2}',t)
        # coefficient immediately preceding printed variable.
        t=re.sub(r'(?<![\w])'+str(2*a)+r'\s*(?=VARSLOT)',r'BSLOT',t)
        # source distributed product 2 dot a variable.
        t=re.sub(r'(\\cdot\s*)'+str(a)+r'(?=VARSLOT)',lambda n:n[1]+'ASLOT',t)
        # Numerical perfect square constant at the end of a trinomial.
        t=re.sub(r'(VARSLOT\s*\+\s*)'+str(a*a)+r'\b',lambda n:n[1]+'SSLOT',t)
        # a in the factor's binomial.
        t=re.sub(r'(VARSLOT\s*[+-]\s*)'+str(a)+r'(?=\s*(?:\\,)?[{})])',lambda n:n[1]+'ASLOT',t)
        return t
    text=re.sub(r'\$\$.*?\$\$|\$[^$]*\$',region,text,flags=re.S)
    return text
MASKS={sid:{key:masked(q[key],sid) for key in (':question/problem',':question/worked-solution') if key in q} for sid,q in QUESTIONS.items()}

def fill(mask,p):
    for key,val in {'VARSLOT':p['variable'],'ASLOT':str(p['a']),'BSLOT':str(2*p['a']),'SSLOT':str(p['a']**2),'KSLOT':str(p['k'])}.items():mask=mask.replace(key,val)
    return mask

def answer(v,r,k,sign,style='normal'):
    s='+' if r>=0 else '-';base=f'({v}{s}{tex(abs(r))})'
    if style=='q-140186' or style=='q-140271':return f'({v} {s} {tex(abs(r))})^{{2}} {"+" if sign>0 else "-"} {k}'
    if style=='q-141513':base=f'({v}{s}{tex(abs(r))}{{)}}'
    return base+'^{2}'+('+' if sign>0 else '-')+str(k)

def completed_solution(p,notation):
    v,a,k,sg=p['variable'],p['a'],p['k'],'+' if p['sign']>0 else '-'
    c=str(a*a) if notation=='number' else f'{{{a}}}^{{2}}'
    inner=f'{{{v}}}^{{2}}+{2*a}{v}+{c}'
    rows=[inner]
    if notation=='number':rows.append(f'{{{v}}}^{{2}}+{2*a}{v}+{{{a}}}^{{2}}')
    rows.extend([f'{{{v}}}^{{2}}+2\\cdot {a}{v}+{{{a}}}^{{2}}',f'({v}+{a}{{)}}^{{2}}'])
    return ('First, we recall the following formula:\n\n$$\n'+f'{{{v}}}^{{2}}+2a{v}+{{a}}^{{2}}=({v}+a{{)}}^{{2}}'+'\n$$\n\nNotice that we have a perfect square in the parentheses that we can factor as follows:\n\n$$\n'+r'\begin{aligned}'+(' & = '+r' \\ ').join(rows)+r' & \end{aligned}'+'\n$$\n\nTherefore, we obtain\n\n$$\n'+r'\begin{aligned}'+f'({inner}){sg}{k}'+r' & = \\ '+answer(v,a,k,p['sign'],'q-141513')+r' & .\end{aligned}'+'\n$$')

def parameters_for(sid):
    level,v,a,k,sign,notation,kind=CONFIG[sid]
    return {'variable':v,'a':a,'k':k,'sign':sign}

def guard(level,p,sid):
    if set(p)!={'variable','a','k','sign'}:raise ValueError('expected variable,a,k,sign')
    if p['variable'] not in ('x','y','z') or type(p['a']) is not int or type(p['k']) is not int:raise ValueError('integer parameters and x/y/z only')
    if not 1<=p['k']<=10:raise ValueError('outer magnitude1..10')
    if level=='hard':
        if not 11<=p['a']<=15 or p['sign']!=-1:raise ValueError('hard numerical squares11..15 and difference')
    else:
        if not 1<=p['a']<=10:raise ValueError('observed familiar squares1..10')
        if p['sign']!=CONFIG[sid][4]:raise ValueError('sign belongs to prompt family')


def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ('easy','moderate','hard'):raise ValueError('unknown difficulty')
    if field_type not in (None,'radio','blank'):raise ValueError('supported fields: radio/blank')
    rng=random.Random(seed)
    if profile and profile.startswith(('raw:','completed:')):
        sid=profile.split(':',1)[1]; raw=profile.startswith('raw:')
        if sid not in CONFIG:raise ValueError('unknown source')
        if template and template!=sid:raise ValueError('template/profile mismatch')
        if level!=CONFIG[sid][0]:raise ValueError('authored unrated replay level or observed level required')
    else:
        raw=False
        options=[sid for sid,c in CONFIG.items() if c[0]==level and (not field_type or c[6]==field_type)] if level!='hard' else ['hard_radio','hard_blank']
        if level=='hard' and field_type:options=['hard_'+field_type]
        sid=template or rng.choice(options)
        if sid not in options:raise ValueError('template outside level')
    kind=CONFIG[sid][6] if sid in CONFIG else sid.split('_')[1]
    if field_type and kind!=field_type:raise ValueError('field mismatch')
    if profile and not profile.startswith(('raw:','completed:')) and profile!='method':raise ValueError('unknown bank profile')
    candidates=list(range(11,16) if level=='hard' else range(1,11))
    if profile and profile.startswith(('raw:','completed:')) and kind=='radio':
        recipe=BANKS[sid]
        candidates=[a for a in candidates if len({sp.sympify(r).subs({'a':a}) for r in recipe})==5]
    p=dict(parameters) if parameters is not None else {'variable':rng.choice(['x','y','z']),'a':rng.choice(candidates),'k':rng.randint(1,10),'sign':CONFIG[sid][4] if sid in CONFIG else -1}
    guard(level,p,sid)
    v,a,k,sign=(p[z] for z in ('variable','a','k','sign'))
    notation=CONFIG[sid][5] if sid in CONFIG else 'number'
    observed=profile is not None and profile.startswith(('raw:','completed:'))
    if sid in MASKS:
        prompt=fill(MASKS[sid][':question/problem'],p)
        solution=fill(MASKS[sid].get(':question/worked-solution',''),p) or completed_solution(p,notation)
    else:
        inner=f'({v}^{{2}}+{2*a}{v}+{a*a})-{k}'
        prompt=f'Rewrite the expression ${inner}$ as the difference between a perfect square and a constant.' if kind=='radio' else f'Rewrite the following expression as the difference between a perfect square and a constant.\n\n${inner}=(${{{{field-1}}}}$)^{{2}}-$\n{{{{field-2}}}}'
        solution=completed_solution(p,notation)
    # Banks chosen as complete profiles; source operations remain evidence profiles.
    recipe=BANKS.get(sid,DEFAULT_BANK) if observed else DEFAULT_BANK
    values=[answer(v,sp.sympify(r).subs({'a':a}),k,sign,sid if observed else 'normal') for r in recipe] if kind=='radio' else [v+'+'+str(a),str(k)]
    if kind=='radio' and len(set(values))!=5:raise ValueError('whole bank collision')
    if raw:
        source=QUESTIONS[sid]
        q={':question/problem':prompt}
        if ':question/worked-solution' in source:q[':question/worked-solution']=solution
        if ':question/difficulty' in source:q[':question/difficulty']=enum(source[':question/difficulty'])
    else:q={':question/problem':prompt,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+level}
    # Identity: actual displayed content, level presence and complete banks, no seed/profile alias.
    presence=sorted([[f[':answer-field/key'],':answer-field/choices' in f,':answer-field/correct' in f] for f in QUESTIONS[sid][':question/answer-fields']]) if raw else [[key,True,True] for key in (['selection'] if kind=='radio' else ['field-1','field-2'])]
    ident=digest([VERSION,q,kind,sorted(values),presence])
    q[':question/id']=uid(ident)
    q[':question/answer-fields']=[]
    source_fields=QUESTIONS[sid][':question/answer-fields'] if raw else []
    keys=['selection'] if kind=='radio' else ([f[':answer-field/key'] for f in source_fields] if raw else ['field-1','field-2'])
    for key in keys:
        f={':answer-field/id':uid(ident+key),':answer-field/key':key,':answer-field/type':':answer-field.type/'+kind}
        vals=values if kind=='radio' else [v+'+'+str(a) if key=='field-1' else str(k)]
        src=next((z for z in source_fields if z[':answer-field/key']==key),None)
        if not raw or ':answer-field/choices' in src:
            choices=[{':answer/id':uid(ident+key+value),':answer/type':':answer.type/math',':answer/value':value} for value in vals]
            correct=answer(v,a,k,sign,sid if observed else 'normal') if kind=='radio' else vals[0]
            if not raw or ':answer-field/correct' in src:f[':answer-field/correct']=[':answer/id',uid(ident+key+correct)]
            if kind=='radio':rng.shuffle(choices)
            f[':answer-field/choices']=choices
        q[':question/answer-fields'].append(f)
    # Variable aliases excluded, square notation not extra skill, fragments assessed separately.
    mathematical=digest([a,k,sign,'whole expression' if kind=='radio' else 'supplied binomial and constant'])
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'template':sid,'parameters':p,'bank_profile':profile or 'method','mathematical_fingerprint':mathematical,'content_fingerprint':ident,'source':{key:SOURCE[key] for key in ('database','basis','lineage')},'origin':'raw observed evidence' if raw else ('authored completion' if observed else ('authored hard' if level=='hard' else 'observed family with authored method bank')),'raw_replay':raw,'evidence_only':raw or (observed and sid=='q-141513'),'eligible_for_learning':not raw and not (observed and sid=='q-141513'),'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__}}}

# Easy: independent isolated sum/difference family instances, no progression.
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
# Moderate: source subtraction sign bookkeeping, same positive-linear factoring.
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
# Hard: authored familiar numerical square recognition at11..15, no new algebra.
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)

def markdown(rec):
    q=rec['question'];out=q[':question/problem']+'\n\n'
    for f in q[':question/answer-fields']:
        out+=f[':answer-field/key']+': '+', '.join('$'+c[':answer/value']+'$' for c in f.get(':answer-field/choices',[]))+'\n\n'
    return out+q.get(':question/worked-solution','[Source omits worked solution.]')
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['json','markdown'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
    recs=[generate(level,args.seed+i,template=args.template,profile=args.profile) for level in (['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]) for i in range(args.count)]
    print(json.dumps(recs,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in recs))
