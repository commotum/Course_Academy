#!/usr/bin/env python3
"""KP17592186115242; steps 3–7, exact arithmetic, no database operations.

Observed complete bank profiles are explicit arithmetic patterns, with unresolved
scalar error intent documented. They are never the default bank. Source masks
contain complete mathematical slots, not numeric substring replacements. Normal
sampling uses assessed-operation distractor banks. All three levels are supported.
"""
from __future__ import annotations
import argparse,hashlib,json,pathlib,random,re,uuid,sys
from math_format import normalize_prose, normalize_tex, matrix_tex as format_matrix, checked_math_content
import sympy as s
KP_ID=17592186115242
KP_UUID='22733f71-de4a-5058-a41c-039e66e333c5'
TITLE='Determining the Value of a Constant for Which a Given Linear System Is Consistent or Inconsistent'
VERSION='constant-consistency-v3'
DIR=pathlib.Path(__file__).with_suffix('')
TEMPLATES={'easy':['inconsistent_easy'],'moderate':['inconsistent_bare','inconsistent_shift','inconsistent_scaled','inconsistent_scaled_shift'],'hard':['dependent_swap','dependent_fractional','dependent_negative']}

def tex(z):
    z=s.sympify(z)
    return s.latex(z).replace(' ','')

def term(z,var):
    z=s.sympify(z)
    return '' if z==0 else var if z==1 else '-'+var if z==-1 else tex(z)+var

def aff(u,v,var='k',constant_first=False):
    t=term(u,var)
    if constant_first and v:
        return tex(v)+('+' if u>0 else '')+t
    return t+('+' if v>0 and t else '')+(tex(v) if v else '') or '0'

def equation(a,b,c):return term(a,'x')+('+' if b>0 else '')+term(b,'y')+'='+tex(c)
def matrix(rows):return format_matrix(rows, augmented=True)
def components(p,style):
    a,b,c,d,u,v,e=[s.Rational(p[k]) for k in 'a b c d u v e'.split()]
    coef=aff(u,v)
    if style.get('negative_coeff_factored'):coef='-('+aff(-u,-v)+')'
    eq1=equation(a,b,c)
    cy=coef if v==0 else '('+coef+')'
    if style.get('negative_coeff_factored'):cy=coef
    eq2=term(d,'x')+('+' if u>0 else '')+cy+'y='+tex(e)
    swap=style.get('swap',False)
    rows=[[tex(a),tex(b),tex(c)],[tex(d),coef,tex(e)]]
    if swap:
        r=a/d; alpha=-r*u;beta=b-r*v;h=c-r*e; pivot=eq2; prow=rows[1]
    else:
        r=d/a;alpha=u;beta=v-r*b;h=e-r*c;pivot=eq1;prow=rows[0]
    red=aff(alpha,beta,constant_first=swap and alpha<0)
    cyred=red
    if style.get('negative_coeff_factored'):cyred='-('+aff(-alpha,-beta)+')'
    elif len(red)>1:cyred='('+red+')'
    reduced=cyred+'y='+tex(h)
    op=style.get('rowop','plus_parenthesized')
    m=-r
    if op=='subtract' and r>0:opt='-'+tex(r)
    elif m<0 and op=='plus_parenthesized':opt='+('+tex(m)+')'
    else:opt=('+' if m>0 else '')+tex(m)
    if m==1 and op!='subtract':opt='+'
    if m==-1 and op=='subtract':opt='-'
    rowop=r'{R}_{2} & :={R}_{2}'+opt+r'{R}_{1}'
    t=(d*b/a-v)/u
    return {'equation1':eq1,'equation2':eq2,'pivot_equation':pivot,'reduced_equation':reduced,'matrix0':matrix(rows),'matrix1':matrix(list(reversed(rows))) if swap else '', 'matrix2':matrix([prow,['0',red,tex(h)]]),'rowop':rowop,'answer':'k='+tex(t),'zero_equation':'0='+tex(h)}

def validate_parameters(level,template,p):
    if set(p)!=set('a b c d u v e'.split()):raise ValueError('Exactly a,b,c,d,u,v,e required')
    vals={k:s.Rational(v) for k,v in p.items()}
    if any(v.q!=1 for v in vals.values()):raise ValueError('Displayed input coefficients must be integers')
    a,b,c,d,u,v,e=[vals[k] for k in 'a b c d u v e'.split()]
    if not a*b*d*u:raise ValueError('Nonzero pivot and y coefficients required')
    if max(abs(a),abs(b),abs(d))>10 or abs(u)>4 or abs(v)>15 or max(abs(c),abs(e))>40:raise ValueError('Curriculum arithmetic bounds exceeded')
    r=d/a;h=e-r*c
    if level=='easy':
        if a!=1 or u!=1 or v!=0 or not 2<=abs(d)<=3 or abs(b)>4 or max(abs(c),abs(e))>8:raise ValueError('Easy bounds: a=u=1, v=0, |d|=2..3, |b|<=4, |c|,|e|<=8')
    elif level=='moderate':
        if r.q!=1 or not 2<=abs(r)<=4 or abs(a)>4 or abs(b)>4 or max(abs(c),abs(e))>5:raise ValueError('Moderate bounds: integer multiplier 2..4, |a|,|b|<=4, |c|,|e|<=5')
        if template.endswith('bare') and (u!=1 or v!=0 or abs(a)<2):raise ValueError('Moderate bare coefficient k requires |a|>=2')
        if template.endswith('shift') and 'scaled' not in template and (u!=1 or v==0):raise ValueError('Shifted coefficient must have u=1, v!=0')
        if template.endswith('scaled') and (u not in (2,3) or v!=0):raise ValueError('Scaled coefficient must be 2k or 3k')
        if template.endswith('scaled_shift') and (u not in (2,3) or v==0):raise ValueError('Scaled shifted coefficient required')
    else:
        if template=='dependent_swap' and (d!=1 or u!=1 or v!=0 or not 2<=abs(a)<=4 or abs(b)>7):raise ValueError('Swap bounds: d=u=1,v=0,|a|2..4,|b|<=7')
        if template=='dependent_fractional' and (u!=1 or r.q==1 or abs(a)>4 or abs(d)>5 or abs(b)>6):raise ValueError('Fractional row multiplier with bare or shifted k required')
        if template=='dependent_negative' and (a!=1 or d not in (-2,-3,-4) or u!=-1 or v>=0 or abs(b)>4):raise ValueError('Negative parameter family bounds exceeded')
    if level=='hard' and h!=0:raise ValueError('Dependent requires proportional constants')
    if level!='hard' and h==0:raise ValueError('Inconsistent requires nonzero residual constant')
    return {k:int(v) for k,v in vals.items()}

def sample(level,template,rng):
    if level=='easy':return dict(a=1,b=rng.choice([-4,-3,-2,2,3,4]),c=rng.randint(-5,5),d=rng.choice([-3,-2,2,3]),u=1,v=0,e=rng.randint(-8,8))
    if level=='moderate':
        a=rng.choice([-3,-2,2,3] if template.endswith('bare') else [-3,-2,-1,1,2,3]);r=rng.choice([-3,-2,2,3]);d=a*r
        return dict(a=a,b=rng.choice([-4,-3,-2,-1,1,2,3,4]),c=rng.randint(-4,4),d=d,u=rng.choice([2,3]) if 'scaled' in template else 1,v=rng.choice([-9,-6,-3,-1,1,3,6,9]) if 'shift' in template else 0,e=rng.randint(-5,5))
    if template=='dependent_swap':
        a=rng.choice([-4,-3,-2,2,3,4]);e=rng.choice([-4,-3,-2,2,3,4]);return dict(a=a,b=rng.choice([-7,-6,-5,-4,-3,-2,2,3,4,5,6,7]),c=a*e,d=1,u=1,v=0,e=e)
    if template=='dependent_negative':
        d=rng.choice([-4,-3,-2]);c=rng.choice([-4,-2,2,3,4]);return dict(a=1,b=rng.choice([-4,-3,-2,2,3,4]),c=c,d=d,u=-1,v=rng.choice([-4,-3,-2,-1]),e=d*c)
    a=rng.choice([-4,-3,-2,2,3,4]);d=rng.choice([-5,-3,-1,1,3,5]);n=rng.choice([-3,-2,1,2,3]);return dict(a=a,b=rng.choice([-6,-4,-2,2,4,6]),c=a*n,d=d,u=1,v=rng.choice([-6,-3,-1,0,1,3,6]),e=d*n)

def authored_bank(t,rank,spacing):
    """A complete offset profile; rank is chosen before coefficient sampling.

    All values share the root's denominator, so integral notation itself does
    not identify the key. Zero roots require no special exclusion or resampling.
    """
    step=s.Rational(spacing,t.q)
    recipes=['t'+('+' if j-rank>=0 else '')+str((j-rank)*step) for j in range(5)]
    return [t+(j-rank)*step for j in range(5)],recipes

def normalize_system_braces(text):
    return re.sub(r'(?<!\\)\{(?=\\begin\{aligned\})',lambda _: r'\{',text)

def mask_render(mask,comp):
    for k,v in comp.items():mask=mask.replace('@@'+k+'@@',v)
    if '@@' in mask:raise ValueError('Unresolved math slot')
    return normalize_system_braces(mask)

def generic_masks(style,hard):
    prefix='Determine the value of $k$ for which the following system of linear equations is '+('consistent dependent' if hard else 'inconsistent')+':\n\n$$\n'+r'\{\begin{aligned} & @@equation1@@ \\  & @@equation2@@\end{aligned}'+'\n$$'
    elimination=r'\begin{aligned}M & =@@matrix0@@'
    if style['swap']:elimination+=r' & {R}_{1} & ↔{R}_{2} \\  & ∼@@matrix1@@'
    elimination+=r' & @@rowop@@ \\  & ∼@@matrix2@@\end{aligned}'
    sol='The augmented matrix for this system is\n\n$$\nM=@@matrix0@@.\n$$\n\nUsing the method of Gaussian elimination, we can reduce this matrix to row echelon form, as follows:\n\n$$\n'+elimination+'\n$$\n\nThe corresponding system is now \n\n$$\n'+r'\{\begin{aligned} & @@pivot_equation@@ \\  & @@reduced_equation@@.\end{aligned}'+'\n$$\n\n'
    if hard:sol+='The system is consistent dependent if it has infinitely many solutions. For the system to have infinitely many solutions, it must have at least one free variable.\n\nIf $@@answer@@,$ then the second equation is $0=0,$ which is true for any value of $y$, and we can remove this equation from the system. As a result, the system will contain only one equation, $@@pivot_equation@@.$ \n\nThen, the basic variable will be $x,$ and we will have a free variable $y.$ That means the system will have infinitely many solutions.\n\n'
    else:sol+='The system is inconsistent if it has no solutions. For the system to have no solutions, one of the equations above must be false.\n\nIf $@@answer@@,$ then the second equation is $@@zero_equation@@,$ which is false, and the system will have no solution.\n\n'
    sol+='Therefore, our system is '+('consistent dependent' if hard else 'inconsistent')+' when $@@answer@@.$'
    return prefix,sol

# Easy / moderate / hard all use shared exact mathematical recipes.
@checked_math_content
def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in TEMPLATES:raise ValueError('Unsupported level')
    if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Only observed radio layout supported')
    rng=random.Random(seed);specs=json.loads((DIR/'recipes.json').read_text())
    # Independent role assignment precedes coefficient sampling and rejection.
    bank_rank=rng.randrange(5);bank_spacing=rng.choice([1,2])
    observed=profile is not None and profile!='authored'
    if observed:
        if profile not in specs:raise ValueError('Unknown profile')
        spec=specs[profile]
        if spec['level']!=level:raise ValueError('Profile difficulty mismatch')
        if template and template!=spec['template']:raise ValueError('Profile template mismatch')
        template=spec['template']
    template=template or rng.choice(TEMPLATES[level])
    if template not in TEMPLATES[level]:raise ValueError('Template difficulty mismatch')
    style=spec['style'] if observed else {'swap':template=='dependent_swap','rowop':'plus_parenthesized','negative_coeff_factored':template=='dependent_negative'}
    if observed:pm,sm=spec['problem_mask'],spec['solution_mask']
    else:pm,sm=generic_masks(style,level=='hard')
    for _ in range(10000):
        try:
            p=validate_parameters(level,template,parameters if parameters is not None else sample(level,template,rng))
            vals={k:s.Rational(v) for k,v in p.items()};a,b,c,d,u,v,e=[vals[k] for k in 'a b c d u v e'.split()];r=d/a;t=(r*b-v)/u;h=e-r*c
            env=dict(vals,r=r,t=t,h=h)
            bank_variant='authored_offsets'
            if observed:
                recipes=spec['bank']
                bank=[s.cancel(s.sympify(q,locals=env)) for q in recipes]
                bank_variant='observed'
                if any(z.has(s.zoo,s.nan,s.oo) for z in bank) or len(set(bank))!=5 or bank.count(t)!=1:
                    bank,recipes=authored_bank(t,bank_rank,bank_spacing)
                    bank_variant='authored_offsets_collision_fallback'
            else:bank,recipes=authored_bank(t,bank_rank,bank_spacing)
            break
        except (ValueError,TypeError,ZeroDivisionError):
            if parameters is not None:raise
    else:raise ValueError('No eligible complete instance')
    comp=components(p,style);problem=mask_render(pm,comp);solution=mask_render(sm,comp)
    values=['k='+tex(z) for z in bank]
    # Mathematical identity excludes presentation style, bank and profile. RREF
    # canonical row space of polynomial augmented matrix removes scalar row variants.
    k=s.Symbol('k');mat=s.Matrix([[a,b,c],[d,u*k+v,e]])
    canonical=[s.srepr(z) for z in mat.rref()[0]]
    fp=hashlib.sha256(json.dumps([str(t),canonical],sort_keys=True).encode()).hexdigest()
    problem,solution=normalize_prose(problem),normalize_prose(solution)
    values=[normalize_tex(value) for value in values]
    content=[VERSION,level,template,p,problem,solution,sorted(values)]
    identity=json.dumps(content,sort_keys=True);qid=str(uuid.uuid5(uuid.NAMESPACE_URL,identity));fid=str(uuid.uuid5(uuid.UUID(qid),'selection'))
    answers=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),value)),':answer/type':':answer.type/math',':answer/value':value} for value in values]
    correct=answers[bank.index(t)][':answer/id'];rng.shuffle(answers)
    field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]}
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':problem,':question/worked-solution':solution,':question/answer-fields':[field]},'generation':{'version':VERSION,'basis':1356,'database':'math','lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1','seed':seed,'template':template,'profile':profile or 'authored','bank_variant':bank_variant,'parameters':p,'recipes':recipes,'mathematical_fingerprint':fp,'math_fingerprint':fp,'authored_level':level=='easy','plot_rating':'none','sympy_version':s.__version__}}

def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)
def markdown(rec):
    q=rec['question'];f=q[':question/answer-fields'][0]
    return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$' for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']

def easy_batch_has_contrasts(records):
    """Require witnesses against the reported finite sign/rank/position cue.

    This selects unchanged v3 instances; it never edits an individual bank or
    excludes a coefficient value from single-seed/source replay.
    """
    groups={False:[],True:[]}
    if len({r['question'][':question/id'] for r in records})!=len(records):return False
    for rec in records:
        p=rec['generation']['parameters'];t=p['b']*p['d']  # easy a=u=1, v=0
        f=rec['question'][':question/answer-fields'][0]
        choices=f[':answer-field/choices'];key=f[':answer-field/correct'][1]
        rank=sum(int(a[':answer/value'].split('=')[1])<t for a in choices)
        pos=next(i for i,a in enumerate(choices) if a[':answer/id']==key)
        groups[t>0].append((t,rank,pos))
    for rows in groups.values():
        if len({t for t,_,_ in rows})<2:return False
        ranks={rank for _,rank,_ in rows}
        if not ranks.intersection({0,4}) or not ranks.intersection({1,2,3}):return False
        if len({pos for _,_,pos in rows})<2:return False
    return True

def generate_batch(level,count,seed=0,template=None,profile=None):
    if count<1:raise ValueError('count must be positive')
    if level!='easy' or profile not in (None,'authored') or count<4:
        return [generate(level,seed+i,template=template,profile=profile) for i in range(count)]
    window=[generate(level,seed+i,template=template,profile=profile) for i in range(count)]
    for offset in range(10000):
        if easy_batch_has_contrasts(window):return window
        window=window[1:]+[generate(level,seed+count+offset,template=template,profile=profile)]
    raise ValueError('No easy batch with contrasting sign, numeric and display roles found')

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=1);parser.add_argument('--format',choices=['json','markdown'],default='markdown');parser.add_argument('--template');parser.add_argument('--profile');args=parser.parse_args()
    if args.count<1:parser.error('count must be positive')
    levels=list(TEMPLATES) if args.difficulty=='all' else [args.difficulty]
    records=[r for level in levels for r in generate_batch(level,args.count,args.seed,template=args.template,profile=args.profile)]
    print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
if __name__=='__main__':main()
