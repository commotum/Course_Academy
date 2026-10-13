#!/usr/bin/env python3
"""Radical antiderivatives, basis 1356. No DB access or plots.

Public raw:<MA-id> profiles reconstruct all eight captured records from complete
parameterized masks/operation banks, preserving missing attribute presence.
Raw/opaque profiles are evidence_only and ineligible_for_learning. Normal records
complete missing fields/keys/solutions and explicitly restrict x>0. Fraction blanks
request the primitive term without any additive constant. All arithmetic is exact.

Three finite level domains are enumerated below and enforced on explicit calls.
Moderate is an authored level: nonunit powers under roots with small indices 2–4;
hard has nonunit powers under indices 5–8. Proper and improper positive
fractions are peer variants, with p<=20, p+d<=24, and p/d<=5. Neither introduces
coefficients, sums, negative integrand powers, substitutions or another topic. The sibling constant-multiple
rule follows this lesson. Power-rule and derivative-check stages retain source
prose, distinct unsimplified arithmetic and formal operators. No progression.
"""
from __future__ import annotations
import argparse, copy, hashlib, json, math, random, re, uuid
from pathlib import Path
import sympy as sp

KP_ID=17592186064168
KP_UUID='85af4ca3-5e66-522a-9e5a-6efb1c7114ba'
TITLE='Finding the Antiderivative of a Radical Function'
VERSION='radical-antiderivative-v2'
ROOT=Path(__file__).with_suffix('')
SNAPSHOT=json.loads((ROOT/'source.json').read_text())
SOURCES={q[':question/math-academy-id']:q for q in SNAPSHOT['record'][':knowledge-point/questions']}
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
}
TEMPLATES={
 'easy':['power','fragment_compact','fragment_spaced','legacy_power_radio'],
 'moderate':['root_moderate','legacy_root_radio'],
 'hard':['root_find','root_calculate'],
}
# Finite reduced number-form domains. Equivalent unreduced spellings are invalid.
POWER_DOMAIN=tuple((p,d) for d in range(2,6) for p in range(1,6)
                   if math.gcd(p,d)==1 and sp.Rational(p,d)<=sp.Rational(5,2))
UNIT_DOMAIN=tuple((1,d) for d in range(2,6))
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
MODERATE_DOMAIN=root_workload_pairs(range(2,5))
HARD_DOMAIN=root_workload_pairs(range(5,9))

def domain(level,template):
    if template in ('fragment_compact','fragment_spaced'):return UNIT_DOMAIN
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

def prompt(template,p,d):
    if template=='power':return rf'Find the antiderivative of ${{x}}^{{{ratio(p,d)}}}.$'
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

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    """Public parameterized generation including exact raw evidence profiles.

    Explicit inputs always fail rather than silently resample or coerce. Raw source
    profiles may omit rated difficulty, fields, correct refs or solution exactly as
    captured. Completed opaque replay remains ineligible. Seed affects only sampling
    and radio order; content identity is independent of seed/order/profile alias.
    """
    if level not in TEMPLATES:raise ValueError('Unknown difficulty')
    rng=random.Random(seed)
    raw=bool(profile and profile.startswith('raw:'))
    replay=raw or bool(profile and profile.startswith('completed:'))
    source_id=profile.split(':',1)[1] if replay else None
    spec=SOURCE_SPEC.get(source_id) if replay else None
    if replay and not spec:raise ValueError('Unknown source profile')
    if spec:
        source_level,source_template,sp_,sd=spec
        if level!=source_level:raise ValueError('Source assigned level mismatch')
        if template is not None and template!=source_template:raise ValueError('Source template mismatch')
        template=source_template
    else:
        template=template or rng.choice(TEMPLATES[level])
        if template not in TEMPLATES[level]:raise ValueError('Template/level mismatch')
    parameters=validate_parameters(level,template,parameters if parameters is not None else
      ({'p':spec[2],'d':spec[3]} if spec else dict(zip(('p','d'),rng.choice(domain(level,template))))))
    p,d=parameters['p'],parameters['d']
    expected_kind='radio' if 'radio' in template else 'blank'
    if raw and spec and ':question/answer-fields' not in SOURCES[source_id]:expected_kind=None
    if field_type is not None and field_type!=expected_kind:raise ValueError('Field layout mismatch')
    bank_profile='opaque-power' if replay and template=='legacy_power_radio' else 'legacy-radical' if template=='legacy_root_radio' else 'authored'
    if profile and not replay and profile not in ('authored','default','legacy-radical'):raise ValueError('Unknown profile')
    if bank_profile=='opaque-power' and (p!=1 or not 2<=d<=5):raise ValueError('Opaque profile is limited to unit fractional powers with indices 2–5')
    if profile=='legacy-radical' and template!='legacy_root_radio':raise ValueError('Bank/template mismatch')
    text=prompt(template,p,d)
    kind='fragment' if template.startswith('fragment') else 'power' if template in ('power','legacy_power_radio') else 'root'
    r=root(p,d,'legacy') if template=='legacy_root_radio' else root(p,d)
    worked=solution(p,d,kind,r)
    values=bank(p,d,bank_profile) if expected_kind=='radio' else [('correct',primitive(p,d))]
    validate_bank(values)
    if not raw:
        text+='\n\nWork on $x>0$.'
        if expected_kind=='blank' and not template.startswith('fragment'):
            text+='\n\nThe antiderivative is {{field-1}} $+C$.'
        if expected_kind=='blank':text+=' Enter only the term before $+C$, with no additive constant.'
    q={':question/problem':text}
    if not raw or ':question/difficulty' in SOURCES[source_id]:q[':question/difficulty']=':question.difficulty/'+level
    if not raw or ':question/worked-solution' in SOURCES[source_id]:q[':question/worked-solution']=worked
    fingerprint_math=fingerprint({'integrand':str(sp.Rational(p,d)),'domain':'x>0','radical_to_power':template not in ('power','legacy_power_radio')})
    content_id=fingerprint({'version':VERSION,'question':q,'field_type':expected_kind,'values':sorted(t for _,t in values) if expected_kind else [],'task':fingerprint_math})
    q[':question/id']=uid(content_id)
    if expected_kind is not None:
        missing_correct=raw and ':answer-field/correct' not in SOURCES[source_id][':question/answer-fields'][0]
        f=local_field(values,'selection' if expected_kind=='radio' else 'field-1',expected_kind,content_id,not missing_correct)
        if expected_kind=='radio':rng.shuffle(f[':answer-field/choices'])
        q[':question/answer-fields']=[f]
    if raw:
        # Evidence IDs and DB source keys retain key-presence; identities are local.
        original=SOURCES[source_id]
        q[':db/id']=original[':db/id'];q[':question/math-academy-id']=source_id
        if expected_kind:
            f[':db/id']=original[':question/answer-fields'][0][':db/id']
            original_values=original[':question/answer-fields'][0][':answer-field/choices']
            # db IDs are evidence provenance. Parameterized values are never read here.
            for a in f[':answer-field/choices']:
                recipe=next(rec for rec,t in values if t==a[':answer/value'])
                i=next(i for i,(rec,_) in enumerate(values) if rec==recipe)
                a[':db/id']=original_values[i][':db/id']
    evidence=raw or bank_profile=='opaque-power'
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,
      'generation':{'version':VERSION,'seed':seed,'level':level,'template':template,'profile':profile or 'authored',
        'bank_profile':bank_profile if expected_kind=='radio' else None,'parameters':parameters,
        'domain':'x>0; real powers; raw source omission is retained only for evidence',
        'mathematical_fingerprint':fingerprint_math,'content_fingerprint':content_id,
        'evidence_only':evidence,'eligible_for_learning':not evidence,'ineligible_for_learning':evidence,
        'source_id':source_id,'authored_level':level=='moderate' or bool(spec and source_id in ('q-2023','q-29635')),
        'repairs':[] if raw else ['explicit-positive-domain','primitive-fragment-form' if expected_kind=='blank' else 'complete-family-bank']+(['source-completion'] if replay else []),
        'source':{k:SNAPSHOT[k] for k in ('database','basis','lineage')},
        'recipes':[] if expected_kind is None else [r for r,_ in values] if expected_kind=='radio' else ['power-rule-primitive'],
        'finite_parameter_domain_size':(len(UNIT_DOMAIN) if bank_profile=='opaque-power' else len(domain(level,template)))}}

# EASY — provided positive rational exponent or unit power under a root; no coefficients.
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)

# MODERATE — authored; convert a nonunit power under a root of index 2–4.
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)

# HARD — observed fifth roots; indices 5–8, proper/improper positive peers.
# Same finite numerator/successor/exponent ceilings as moderate; no extra stages.
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)

def markdown(record):
    q=record['question'];g=record['generation']
    shown_level=q.get(':question/difficulty','').split('/')[-1] or ('unrated (authored replay route: '+g['level']+')')
    out=[f"### {shown_level} / {g['template']} / {g['profile']}",q[':question/problem']]
    for f in q.get(':question/answer-fields',[]):
        for a in f[':answer-field/choices']:
            mark=' [correct]' if f.get(':answer-field/correct',[None,None])[1]==a[':answer/id'] else ''
            if mark and g['source_id'] and not any(':answer-field/correct' in old for old in SOURCES[g['source_id']].get(':question/answer-fields',[])):
                mark=' [correct; inferred/authored completion]'
            out.append('- $'+a[':answer/value']+'$'+mark)
        if ':answer-field/correct' not in f:out.append('Correct designation absent in raw source evidence.')
    if ':question/answer-fields' not in q:out.append('Assessment field absent in raw source evidence.')
    if ':question/worked-solution' in q:out.append(q[':question/worked-solution'])
    out.append('Evidence only / ineligible' if g['evidence_only'] else 'Eligible for learning')
    return '\n\n'.join(out)

def main():
    a=argparse.ArgumentParser(description=__doc__);a.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');a.add_argument('--seed',type=int,default=0);a.add_argument('--count',type=int,default=1);a.add_argument('--format',choices=['markdown','json'],default='markdown');a.add_argument('--template');a.add_argument('--profile');args=a.parse_args()
    if args.count<1:a.error('count must be positive')
    levels=TEMPLATES if args.difficulty=='all' else [args.difficulty]
    records=[generate(level,args.seed+i,template=args.template,profile=args.profile) for level in levels for i in range(args.count)]
    print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
if __name__=='__main__':main()
