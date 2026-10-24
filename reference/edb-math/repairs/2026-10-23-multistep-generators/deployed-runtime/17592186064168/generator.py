#!/usr/bin/env python3
"""Radical antiderivatives: relocate this directory with its declared runtime files.

Exact source replay is evidence-only. Normal output is complete and database-free.
No assets are generated. See instructional-account.md for the bounded domains.
"""
from __future__ import annotations

# Standalone source eligibility: immutable policy ledger, seeded CLI guard.
import sys as _ca_sys, os as _ca_os
from pathlib import Path as _ca_Path
_ca_sys.path.insert(0,str(_ca_Path(__file__).resolve().parent))
if __name__ == "__main__" and not _ca_os.environ.get("_CA_SOURCE_POLICY_CHILD"):
    from ca_source_runtime import cli as _ca_source_cli
    _ca_source_cli(__file__,_ca_Path(__file__).with_name('17592186064168-source-policy.json'))
    raise SystemExit(0)

import argparse, copy, hashlib, json, math, random, re, uuid
from pathlib import Path
import sympy as sp
from math_format import normalize_prose, normalize_tex, checked_math_content

KP_ID=17592186064168
KP_UUID='85af4ca3-5e66-522a-9e5a-6efb1c7114ba'
TITLE='Finding the Antiderivative of a Radical Function'
VERSION='radical-antiderivative-v3'
ROOT=Path(__file__).resolve().parent
SNAPSHOT=json.loads((ROOT/'source-data.json').read_text())
SOURCES={q[':question/math-academy-id']:q for q in SNAPSHOT['material']['kp'][':knowledge-point/questions']}
X=sp.Symbol('x',positive=True)
C=sp.Symbol('C',real=True)

# Observed prompt/solution/layout templates. Unrated levels below are authored.
SOURCE_SPEC={
 'q-2023':('moderate','legacy_root_radio',2,3),
 'q-29635':('easy','legacy_power_radio',1,3),
 'q-113674':('easy','power',1,4),
 'q-113680':('hard','root_calculate',3,5),
 'q-113695':('hard','root_find',2,5),
 'q-143041':('easy','fragment_compact',1,3),
 'q-71096':('easy','power',5,2),
 'q-167564':('easy','fragment_spaced',1,5),
 'q-2024':('moderate','integral_radio',1,2),
 'q-29665':('moderate','integral_opaque',3,2),
 'q-29652':('hard','hard_opaque',7,5),
 'q-113672':('easy','power_radio',4,5),
 'q-167646':('easy','fragment_compact',1,6),
 'q-167541':('easy','fragment_compact',1,4),
}
TEMPLATES={
 'easy':['power','fragment_compact','fragment_spaced','legacy_power_radio','power_radio'],
 'moderate':['integral_radio','legacy_root_radio'],
 'hard':['root_find','root_calculate'],
}
OPAQUE={'q-29635','q-29665','q-29652'}
# Finite reduced number-form domains. Equivalent unreduced spellings are invalid.
POWER_DOMAIN=tuple((p,d) for d in range(2,6) for p in range(1,6)
                   if math.gcd(p,d)==1 and sp.Rational(p,d)<=sp.Rational(5,2))
UNIT_DOMAIN=tuple((1,d) for d in range(2,7))
# Same positive rational-power rule for proper and improper peers. The lesson
# gives unrestricted n!=-1; q-71096 explicitly establishes n=5/2. These authored
# ceilings keep one numerator+index addition and reciprocal reduction in small
# two-digit arithmetic, rather than introducing a new integration operation.
ROOT_NUMERATOR_MAX=20
SUCCESSOR_NUMERATOR_MAX=24
ROOT_EXPONENT_MAX=sp.Integer(5)
def root_workload_pairs(indices):
    return tuple((p,d) for d in indices for p in range(2,ROOT_NUMERATOR_MAX+1)
                 if math.gcd(p,d)==1 and p+d<=SUCCESSOR_NUMERATOR_MAX
                 and sp.Rational(p,d)<=ROOT_EXPONENT_MAX)
MODERATE_DOMAIN=tuple((p,d) for d in range(2,5) for p in range(1,8)
                      if math.gcd(p,d)==1 and sp.Rational(p,d)<=sp.Rational(7,2))
HARD_DOMAIN=root_workload_pairs(range(5,9))

def domain(level,template):
    if template in ('fragment_compact','fragment_spaced'):return UNIT_DOMAIN
    if template=='legacy_root_radio':return tuple(pair for pair in MODERATE_DOMAIN if pair[0]>1)
    return {'easy':POWER_DOMAIN,'moderate':MODERATE_DOMAIN,'hard':HARD_DOMAIN}[level]

def fingerprint(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False).encode()).hexdigest()

def uid(value):return str(uuid.uuid5(uuid.UUID(KP_UUID),value))

def ratio(p,d):return str(p) if d==1 else f'{p}/{d}'

def frac(p,d):return str(p) if d==1 else rf'\frac{{{p}}}{{{d}}}'

def power(p,d,brace=True):return ('{x}' if brace else 'x')+'^{'+ratio(p,d)+'}'

def root(p,d,style='modern'):
    if style=='legacy':return rf'\sqrt[{d}]{{x^{{{p}}}}}'
    if p==1:return rf'\sqrt[{d}]{{x}}'
    return rf'\sqrt[{d}]{{{{x}}^{{{p}}}}}'

def primitive(p,d,brace=True,reciprocal=False,with_c=False):
    """Numerator/denominator comes from exact power-rule division, not lookup."""
    coefficient=sp.Rational(d,p+d)
    if reciprocal:coefficient=1/coefficient
    a,b=map(int,coefficient.as_numer_denom())
    monomial=power(p+d,d,brace)
    numerator=('' if a==1 else str(a))+monomial
    result=numerator if b==1 else rf'\frac{{{numerator}}}{{{b}}}'
    return result+(' + C' if with_c else '')

def check_block(p,d):
    s=primitive(p,d);e=ratio(p+d,d);n=ratio(p,d)
    # Five distinct formal derivative stages, exactly as rated practice sources.
    return ("$$\n"+rf"\begin{{aligned}}\frac{{\text{{d}}}}{{\text{{d}}x}}({s}+C) & ="+r' \\ '+
      rf"\frac{{\text{{d}}}}{{\text{{d}}x}}({s})+\frac{{\text{{d}}}}{{\text{{d}}x}}(C) & ="+r' \\ '+
      rf"{frac(d,p+d)}\frac{{\text{{d}}}}{{\text{{d}}x}}({power(p+d,d)})+0 & ="+r' \\ '+
      rf"{frac(d,p+d)}\cdot {frac(p+d,d)}{{x}}^{{{e}-1}} & ="+r' \\ '+
      rf"{{x}}^{{{n}}}\,✓\end{{aligned}}"+"\n$$")

def solution(p,d,kind='power',root_tex=None):
    """Whole ordered prose plus formal radical/power/integral/arithmetic stages."""
    n=ratio(p,d);f=frac(p,d);e=ratio(p+d,d)
    r=root_tex or root(p,d)
    if kind=='root':
        opening=rf'We start by writing the root as a rational power, ${r}={{x}}^{{{n}}}.$ So, we can apply the power rule with $n={f}$ and get'
        first=rf'\int {r}\,\text{{d}}x & =\int {{x}}^{{{n}}}\,\text{{d}}x'+r' \\  & ='
    elif kind=='fragment':
        opening=rf'Since ${r}={{x}}^{{{n}}}$, we can apply the power rule with $n={f}$ and get'
        first=rf'\int {{x}}^{{{n}}}\,\text{{d}}x & ='
    else:
        opening=rf'We can apply the power rule with $n={f}$ and get'
        first=rf'\int {{x}}^{{{n}}}\,\text{{d}}x & ='
    integrals=("$$\n"+r'\begin{aligned}'+first+
      rf'\frac{{{{x}}^{{{n}+1}}}}{{({f}+1)}}+C'+r' \\  & ='+
      rf'\frac{{{{x}}^{{{e}}}}}{{({frac(p+d,d)})}}+C'+r' \\  & ='+primitive(p,d)+r'+C.\end{aligned}'+"\n$$")
    ending="Let's check our answer by differentiating:" if kind=='fragment' else "Again, let's check by differentiating:"
    return opening+'\n\n'+integrals+'\n\n'+ending+'\n\n'+check_block(p,d)

def square_root(p):
    return r'\sqrt{x}' if p==1 else rf'\sqrt{{{{x}}^{{{p}}}}}'

def prompt(template,p,d):
    if template in ('power','power_radio'):return rf'Find the antiderivative of ${{x}}^{{{ratio(p,d)}}}.$'
    if template in ('integral_radio','integral_opaque'):return rf'$\int {square_root(p)}\,\text{{d}}x=$'
    if template=='hard_opaque':return rf'What is the antiderivative of ${root(p,d)}?$'
    if template=='legacy_power_radio':return rf'Find the antiderivative of $x^{{{ratio(p,d)}}}$.'
    if template=='legacy_root_radio':return rf'Find the antiderivative of ${root(p,d,"legacy")}$.'
    if template in ('root_find','root_moderate'):return rf'Find the antiderivative of ${root(p,d)}.$'
    if template=='root_calculate':return rf'Calculate the integral of ${root(p,d)}.$'
    tail='$+\\,\\text{\u00a0}C$'
    if template=='fragment_compact':return rf'The antiderivative of ${root(p,d)}$ equals{{{{field-1}}}} '+tail
    if template=='fragment_spaced':
        return rf'The antiderivative of ${root(p,d)}$ equals'+'\n\n                            \n                                    \n                            \n                                        {{field-1}}                \n                                    \n                                \n                                    \n                                        \n                                         '+tail
    raise ValueError('Unknown template')

def bank(p,d,profile):
    """Select a complete bank first; return all recipes, never a first-valid pool.

    legacy-radical is recovered operations. opaque-power contains structural
    parameterizations with unresolved author intent and cannot be learner output.
    The default authored bank uses actual wrong power-rule operations.
    """
    correct=primitive(p,d,brace=(profile!='legacy-radical'),with_c=True)
    if profile=='legacy-radical':
        return [('lose-inner-power-and-invert',primitive(1,d,False,True,True)),
                ('invert-new-exponent',primitive(p,d,False,True,True)),
                ('omit-division-and-constant',power(p+d,d,False)),
                ('correct',correct),('lose-inner-power',primitive(1,d,False,False,True))]
    if profile=='opaque-power':
        # Observed complete structural bank, not recovered error intent.
        b=2*d
        return [('correct',primitive(p,d,False,with_c=True)),
          ('opaque-reciprocal-surrogate',rf'\frac{{{b+1}x^{{-{b+1}}}}}{{{b}}} + C'),
          ('opaque-surrogate-without-coefficient',rf'x^{{-{b+1}}} + C'),
          ('opaque-old-complement-coefficient',rf'\frac{{{d-p}x^{{{ratio(p+d,d)}}}}}{{{d}}} + C'),
          ('opaque-positive-surrogate',rf'\frac{{x^{{{b}}}}}{{{b+1}}} + C')]
    if profile=='modern-power':
        e=power(p+d,d);h=power(p+d-2,d)
        return [('omit-index-numerator',rf'\frac{{{e}}}{{{d}}} + C'),
                ('shift-exponent-and-omit-index',rf'\frac{{{h}}}{{{p+d-2}}} + C'),
                ('shift-exponent',rf'\frac{{{d}{h}}}{{{p+d-2}}} + C'),
                ('correct',correct),
                ('decrement-index-coefficient',rf'\frac{{{d-1}{e}}}{{{p+d}}} + C')]
    if profile=='modern-integral':
        return [('correct',correct),
                ('divide-by-index',rf'\frac{{{power(p+d,d)}}}{{{d}}} + C'),
                ('increase-exponent-twice',primitive(p+d,d,with_c=True)),
                ('differentiate',rf'\frac{{{p}{power(p-d,d)}}}{{{d}}} + C'),
                ('keep-exponent',rf'\frac{{{d}{power(p,d)}}}{{{p+d}}} + C')]
    if profile!='authored':raise ValueError('Unknown bank')
    # Five full solution families; omitting only C would duplicate a valid family.
    return [('correct',correct),
      ('multiply-instead-of-divide',primitive(p,d,reciprocal=True,with_c=True)),
      ('omit-division',power(p+d,d)+' + C'),
      ('fail-to-increase-exponent',rf'\frac{{{d}'+power(p,d)+rf'}}{{{p+d}}} + C'),
      ('differentiate-instead-of-integrate',rf'\frac{{{p}'+power(p-d,d)+rf'}}{{{d}}} + C')]

def parse_math(tex):
    """Independent utility used for whole-bank collisions (x is positive)."""
    match=re.search(r'(?:\{x\}|x)\^\{(-?\d+(?:/\d+)?)\}',tex)
    if not match:raise ValueError('Expected monomial answer')
    exponent=sp.Rational(match[1]);coefficient=tex[:match.start()]+tex[match.end():]
    coefficient=coefficient.replace(' + C','').replace('+C','')
    coefficient=re.sub(r'\\frac\{(\d*)\}\{(\d+)\}',lambda m:str(sp.Rational(int(m[1] or 1),int(m[2]))),coefficient)
    if coefficient=='':coefficient='1'
    return sp.Rational(coefficient)*X**exponent+(C if 'C' in tex else 0)

def equivalent_family(a,b):
    # Additive arbitrary constants, nonzero rescaling/shifting of C are immaterial.
    return sp.simplify(sp.diff(a-b,X))==0

def validate_bank(values):
    exprs=[parse_math(t) for _,t in values]
    for i,e in enumerate(exprs):
        for j in range(i):
            if equivalent_family(e,exprs[j]):raise ValueError('Whole bank rejected: equivalent solution families')
    return values

def validate_parameters(level,template,parameters):
    if not isinstance(parameters,dict) or set(parameters)!={'p','d'}:raise ValueError('Expected exactly p and d')
    p,d=parameters['p'],parameters['d']
    if any(isinstance(v,bool) or not isinstance(v,int) for v in (p,d)):raise ValueError('p,d must be integers')
    if (p,d) not in domain(level,template):raise ValueError('Outside finite reduced level workload domain')
    return {'p':p,'d':d}

def local_field(values,key,kind,content_id,correct=True):
    fid=uid(content_id+'|field|'+key)
    choices=[{':answer/id':uid(fid+'|'+recipe+'|'+text),':answer/type':':answer.type/math',':answer/value':text} for recipe,text in values]
    f={':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':choices}
    if correct:
        answer=next(a for a,(recipe,_) in zip(choices,values) if recipe=='correct')
        f[':answer-field/correct']=[':answer/id',answer[':answer/id']]
    return f

def varied_bank(p,d,rng,roles=None,design=None):
    """Authored same-operation bank without fixed magnitude/order cues.

    Choose eligible ranks and shared-component assignments before values.
    Wrong outputs change the exponent, coefficient, or both. Their numerical
    error intent is authored rather than attributed to opaque source constants.
    """
    if roles is not None:
        # Explicit source-like offsets support controlled, fixed-bank interventions.
        offsets=(-d,-1,0,1,d)
        eligible=[(a,b) for a in offsets for b in offsets if (a,b)!=(0,0)]
        roles=[tuple(role) for role in roles]
        if len(roles)!=4 or len(set(roles))!=4 or any(role not in eligible for role in roles):
            raise ValueError('Expected four distinct eligible nonzero choice offsets')
        if design is not None:design.update({'kind':'controlled-offsets','offsets':roles})
        pairs=[(sp.Rational(d,p+d+b),sp.Rational(p+d+a,d)) for a,b in roles]
        recipes=[f'successor-offset:{a};divisor-offset:{b}' for a,b in roles]
    else:
        # A complete 2x3 (or 3x2) coefficient/exponent bank minus one pair.
        # Choose which pair is correct uniformly before compatible numeric values.
        # Thus every edge signature, rank, frequency and singleton role is eligible
        # for the key; no symmetric-around-the-key central-value bias remains.
        nc,ne=rng.choice([(2,3),(3,2)])
        all_roles=[(ci,ei) for ci in range(nc) for ei in range(ne)]
        omitted=rng.choice(all_roles)
        roles=[role for role in all_roles if role!=omitted]
        target_ci,target_ei=rng.choice(roles)
        c=sp.Rational(d,p+d);e=sp.Rational(p+d,d)
        coefficient_pool=sorted({sp.Rational(a,b) for a in range(1,max(8,d+2)+1) for b in range(1,max(12,p+d+2)+1)})
        exponent_pool=[sp.Rational(p+d+offset,d) for offset in range(-6,7) if offset and p+d+offset!=0]
        def values(pool,target,count,target_index):
            rank=rng.randrange(count)
            candidates=rng.sample([v for v in pool if v<target],rank)+rng.sample([v for v in pool if v>target],count-1-rank)
            rng.shuffle(candidates)
            candidates.insert(target_index,target)
            return candidates
        cs=values(coefficient_pool,c,nc,target_ci)
        es=values(exponent_pool,e,ne,target_ei)
        if design is not None:
            design.update({'kind':'five-pairs','shape':[nc,ne],'omitted':omitted,'target':[target_ci,target_ei],
                           'coefficient_rank':sorted(cs).index(c),'exponent_rank':sorted(es).index(e),
                           'coefficient_values':list(map(str,cs)),'exponent_values':list(map(str,es))})
        wrong_roles=[role for role in roles if role!=(target_ci,target_ei)]
        pairs=[(cs[ci],es[ei]) for ci,ei in wrong_roles]
        recipes=[f'authored-pair:{ci},{ei};coefficient:{cs[ci]};exponent:{es[ei]}' for ci,ei in wrong_roles]
    result=[('correct',primitive(p,d,with_c=True))]
    for recipe,(coefficient,exponent) in zip(recipes,pairs):
        num,den=map(int,coefficient.as_numer_denom())
        ep,ed=map(int,exponent.as_numer_denom())
        term=('' if num==1 else str(num))+power(ep,ed)
        value=term if den==1 else rf'\frac{{{term}}}{{{den}}}'
        result.append((recipe,value+' + C'))
    return result



def case_of(p,d):
    return 'unit' if p==1 else 'proper' if p<d else 'improper'

def select_parameters(rng, level, template):
    pairs=domain(level,template)
    cases=sorted({case_of(*pair) for pair in pairs})
    case=rng.choice(cases)
    return dict(zip(('p','d'),rng.choice([pair for pair in pairs if case_of(*pair)==case])))


def replay(source_id, completed=False):
    """Immutable exact replay; missing fields are never silently invented in raw mode.

    Completed snapshots keep every source choice. Opaque profiles remain evidence
    only; their error intent is not inferred from unrelated constants.
    """
    level,template,p,d=SOURCE_SPEC[source_id]
    q=copy.deepcopy(SOURCES[source_id])
    if completed:
        q[':question/problem']+='\n\nWork on $x>0$.'
        if ':question/worked-solution' not in q:
            q[':question/worked-solution']=solution(p,d,'root' if source_id=='q-2023' else 'power',root(p,d,'legacy'))
        fs=q.get(':question/answer-fields')
        if not fs:
            q[':question/problem']+='\n\nThe antiderivative is {{field-1}} $+C$. Enter only the term before $+C$, with no additive constant.'
            q[':question/answer-fields']=[local_field([('correct',primitive(p,d))],'field-1','blank',source_id)]
        elif ':answer-field/correct' not in fs[0]:
            # Both missing keys are uniquely identifiable by differentiating the
            # original banks; the validation script independently verifies them.
            target=primitive(p,d,False,with_c=True)
            answer=next(a for a in fs[0][':answer-field/choices'] if a[':answer/value']==target)
            fs[0][':answer-field/correct']=[':answer/id',answer[':answer/id']]
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,
            'generation':{'version':VERSION,'source_id':source_id,'template':template,
                          'parameters':{'p':p,'d':d},'profile':'completed' if completed else 'raw',
                          'evidence_only':True,'eligible_for_learning':False}}


@checked_math_content
def generate(level,seed=0,template=None,parameters=None,profile=None,choice_offsets=None):
    """Learning output only. Source replay is deliberately a separate API."""
    if level not in TEMPLATES:raise ValueError('Unsupported difficulty')
    rng=random.Random(seed)
    template=template or rng.choice(TEMPLATES[level])
    if template not in TEMPLATES[level]:raise ValueError('Template/level mismatch')
    bank_profile='authored-role-ranks'
    if profile is not None and profile!=bank_profile:raise ValueError('Bank/template mismatch')
    attempts=0
    while True:
        attempts+=1
        chosen=validate_parameters(level,template,parameters if parameters is not None else select_parameters(rng,level,template))
        p,d=chosen['p'],chosen['d']
        field_type='radio' if 'radio' in template else 'blank'
        design={}
        values=varied_bank(p,d,rng,choice_offsets,design) if field_type=='radio' else [('correct',primitive(p,d))]
        try:validate_bank(values)
        except ValueError:
            if parameters is not None:raise
            if attempts>100:raise RuntimeError('Cannot construct a distinct bank')
            continue
        break
    text=prompt(template,p,d)
    # Captured excess whitespace is not meaningful layout.
    if template=='fragment_spaced':
        text=rf'The antiderivative of ${root(p,d)}$ equals {{{{field-1}}}} $+C$.'
    if template=='fragment_compact':text=rf'The antiderivative of ${root(p,d)}$ equals {{{{field-1}}}} $+C$.'
    text+='\n\nWork on $x>0$.'
    if field_type=='blank':
        if not template.startswith('fragment'):
            text+='\n\nThe antiderivative is {{field-1}} $+C$.'
        text+=' Enter only the term before $+C$, with no additive constant.'
    kind='fragment' if template.startswith('fragment') else 'power' if template in ('power','power_radio','legacy_power_radio') else 'root'
    r=square_root(p) if template=='integral_radio' and d==2 else root(p,d,'legacy') if template=='legacy_root_radio' else root(p,d)
    # Integral prompt index must agree with its exponent when d is not two.
    if template=='integral_radio' and d!=2:
        text=rf'$\int {r}\,\text{{d}}x=$'+'\n\nWork on $x>0$.'
    q={':question/problem':normalize_prose(text),
       ':question/worked-solution':normalize_prose(solution(p,d,kind,r)),
       ':question/difficulty':':question.difficulty/'+level}
    values=[(recipe,normalize_tex(value)) for recipe,value in values]
    content_id=fingerprint({'version':VERSION,'question':q,'field_type':field_type,'values':sorted(value for _,value in values)})
    q[':question/id']=uid(content_id)
    f=local_field(values,'selection' if field_type=='radio' else 'field-1',field_type,content_id)
    # Shuffle answer-bearing roles before assigning displayed positions.
    if field_type=='radio':
        f[':answer-field/choices'].sort(key=lambda a:a[':answer/value'])
        rng.shuffle(f[':answer-field/choices'])
    q[':question/answer-fields']=[f]
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,
            'generation':{'version':VERSION,'seed':seed,'template':template,'bank_profile':bank_profile if field_type=='radio' else None,
                          'parameters':chosen,'case':case_of(p,d),'attempts':attempts,
                          'domain':'x>0','eligible_for_learning':True,'evidence_only':False,
                          'source_ids':[sid for sid,spec in SOURCE_SPEC.items() if spec[1]==template],
                          'basis':SNAPSHOT['basis'],'bank_design':design if field_type=='radio' else None,'recipes':[recipe for recipe,_ in values]}}


def main():
    parser=argparse.ArgumentParser(description='Seeded radical-antiderivative questions, no database or assets.')
    parser.add_argument('--difficulty',choices=['easy','moderate','hard'],default='easy')
    parser.add_argument('--count',type=int,default=1)
    parser.add_argument('--seed',type=int,default=0)
    parser.add_argument('--format',choices=['json','markdown'],default='json')
    parser.add_argument('--template',choices=sum(TEMPLATES.values(),[]))
    parser.add_argument('--replay',choices=list(SOURCE_SPEC))
    args=parser.parse_args()
    if args.count<1:parser.error('count must be positive')
    records=[replay(args.replay) if args.replay else generate(args.difficulty,args.seed+i,args.template) for i in range(args.count)]
    if args.format=='json':print(json.dumps(records,ensure_ascii=False,indent=2))
    else:
        print('\n\n---\n\n'.join(r['question'][':question/problem']+'\n\n'+r['question'].get(':question/worked-solution','') for r in records))


from ca_source_runtime import install as _ca_source_install
_ca_source_install(globals(),_ca_Path(__file__).with_name('17592186064168-source-policy.json'))

if __name__=='__main__':main()
