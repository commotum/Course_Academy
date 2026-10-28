#!/usr/bin/env python3
"""Seeded smooth-field circulation practice. No database or runtime repository access."""
import argparse
import hashlib
import json
import random
from uuid import UUID, uuid5
import sympy as S
from math_format import normalize_prose, normalize_tex, validate_generated_record

VERSION = '1.0.1'
NS = UUID('4bbe0f96-6e8a-4239-bd15-8ef35b1f7068')
KP = {'db_id':17592186179741, 'id':'976e05d4-59a8-5a93-be2f-b22357f388b9', 'title':'Calculating Circulation'}
x,y,t = S.symbols('x y t', real=True)

def tex(v):
    return normalize_tex(S.latex(S.sympify(v)))

def display(v):
    return '$$\n' + v + '\n$$'

def aligned(rows):
    return display('\\begin{aligned}\n' + '\\\\\n'.join(rows) + '\n\\end{aligned}')

def vector(u,v):
    return r'\left(' + tex(u) + r'\right)\mathbf i+\left(' + tex(v) + r'\right)\mathbf j'

def identity(s):
    return str(uuid5(NS,s))

# Every tuple is one complete, selected error profile. No first-valid pooling.
PROFILES = {
 'direction-traversal-area': ['reverse','half','double','lose_area'],
 'axes-direction': ['reverse','lose_a','lose_b','swap_a'],
 'traversal-axes': ['half','double','sum_axes','swap_b'],
 'direction-swapped-axes': ['reverse','half','swap_a','swap_b'],
 'area-and-axis': ['lose_area','lose_a','swap_b','double'],
 'direction-and-area': ['reverse','lose_area','sum_axes','swap_a'],
 'paired-half-area': ['half','reverse_half','double','lose_area'],
 'paired-double-axis': ['double','reverse_double','lose_a','swap_b'],
 'paired-lost-axis': ['lose_a','reverse_lost_a','lose_b','sum_axes'],
 'two-opposite-pairs': ['reverse','half','reverse_half','double'],
}

def bank(a,b,k,o,d,e,profile):
    c = 2*o*k*a*b
    if k == 0:
        # Losing a component and replacing sin*cos with a square or 1.
        z=d*a*a
        h=e*b*b-d*a*a
        recipes = {'lost_y_squared':-z, 'lost_x_squared':e*b*b,
                   'lost_y_constant':-2*z, 'lost_x_constant':2*e*b*b,
                   'cross_average':h, 'cross_constant':2*h}
        names = {
          'radial-components':['lost_y_squared','lost_x_squared','lost_y_constant','lost_x_constant'],
          'radial-cross':['lost_y_squared','lost_x_squared','cross_average','cross_constant'],
        }[profile]
    else:
        recipes={'reverse':-c,'reverse_half':-c/2,'reverse_double':-2*c,'reverse_lost_a':-c/a,'half':c/2,'double':2*c,'lose_a':c/a,'lose_b':c/b,
                 'lose_area':c/(a*b),'swap_a':c*a/b,'swap_b':c*b/a,
                 'sum_axes':2*o*k*(a+b)}
        names=PROFILES[profile]
    vals=[S.simplify(c)]+[S.simplify(recipes[n]) for n in names]
    if len(set(vals)) != 5:
        raise ValueError('degenerate complete bank')
    return vals,['correct']+names

def make(level,a,b,k,o,d=0,e=0,profile=None,rng=None,replay_bank=None):
    rng = rng or random.Random('|'.join(map(str,(level,a,b,k,o,d,e,profile))))
    a,b,k,o,d,e = map(S.sympify,(a,b,k,o,d,e))
    if a<=0 or b<=0 or o not in [-1,1]: raise ValueError('invalid path')
    P,Q=d*x-k*y,k*x+e*y
    X,Y=a*S.cos(t),o*b*S.sin(t)
    U,V=S.expand(P.subs({x:X,y:Y})),S.expand(Q.subs({x:X,y:Y}))
    DX,DY=S.diff(X,t),S.diff(Y,t)
    h=e*b*b-d*a*a
    c=o*k*a*b
    integrand=c+h*S.sin(t)*S.cos(t)
    primitive=c*t+h*S.sin(t)**2/2
    result=2*c*S.pi
    orientation='counterclockwise' if o==1 else 'clockwise'
    shape='circle' if a==b else 'ellipse'
    # Clear denominators without inflating integer coefficient sizes.
    aa,bb=S.simplify(a*a),S.simplify(b*b)
    common=S.ilcm(int(aa),int(bb))
    curve=tex(S.expand(common/aa*x*x+common/bb*y*y))+'='+str(common)
    path=r'\mathbf r(t)='+vector(X,Y)+r',\qquad 0\le t\le 2\pi.'
    problem=r'Calculate the circulation $\Gamma$ of the vector field'+'\n\n'+display(r'\mathbf F(x,y)='+vector(P,Q))+ '\n\n'
    if level=='easy':
        problem+=r'along the closed curve $C$, traversed once according to'+'\n\n'+display(path)
    else:
        problem+=f'along the {shape} $C$ with equation'+'\n\n'+display(curve)+f'\n\ntraversed once {orientation}.'
    if level=='hard': problem+=' Give an exact answer.\n\n'+r'$\Gamma=$ {{value}}'
    solution=''
    if level!='easy':
        solution+='Write the curve in standard form:\n\n'+display(r'\frac{x^2}{'+tex(aa)+r'}+\frac{y^2}{'+tex(bb)+r'}=1.')
        solution+=f'\n\nChoose the {orientation} parametrization\n\n'+display(path)
        solution+=f'\n\nAt $t=0$, the path starts at $({tex(a)},0)$ and moves '+('upward' if o==1 else 'downward')+', confirming the orientation.\n\n'
    solution+='Circulation is total work around the closed path:\n\n'+display(r'\Gamma=\oint_C\mathbf F\cdot\mathrm d\mathbf r=\int_0^{2\pi}\mathbf F(\mathbf r(t))\cdot\mathbf r\prime(t)\,\mathrm dt.')
    solution+='\n\nSubstitute the path into the field and differentiate the path:\n\n'+aligned([
       r'\mathbf F(\mathbf r(t))&=\left('+tex(U)+r'\right)\mathbf i',
       r'&\quad+\left('+tex(V)+r'\right)\mathbf j,',
       r'\mathbf r\prime(t)&=\left('+tex(DX)+r'\right)\mathbf i',
       r'&\quad+\left('+tex(DY)+r'\right)\mathbf j.'])
    # Preserve a factored dot-product construction, then explain the only identity.
    expanded_rows=[]
    for term in [c*S.sin(t)**2,c*S.cos(t)**2,h*S.sin(t)*S.cos(t)]:
        if term==0:continue
        if not expanded_rows:expanded_rows.append(r'&='+tex(term))
        elif term.could_extract_minus_sign():expanded_rows.append(r'&\quad-'+tex(-term))
        else:expanded_rows.append(r'&\quad+'+tex(term))
    if not expanded_rows:expanded_rows=[r'&=0']
    expanded_rows[-1]+='.'
    solution+='\n\nTake the dot product of corresponding components:\n\n'+aligned([
       r'&\mathbf F(\mathbf r(t))\cdot\mathbf r\prime(t)',
       r'&=\left('+tex(U)+r'\right)\left('+tex(DX)+r'\right)',
       r'&\quad+\left('+tex(V)+r'\right)\left('+tex(DY)+r'\right)']+expanded_rows)
    solution+='\n\nUsing $\\sin^2t+\\cos^2t=1$ and collecting terms gives\n\n'+display(r'\mathbf F(\mathbf r(t))\cdot\mathbf r\prime(t)='+tex(integrand)+'.')
    if h!=0:
        solution+='\n\nSince $\\frac{\\mathrm d}{\\mathrm dt}\\sin^2t=2\\sin t\\cos t$, an antiderivative of $\\sin t\\cos t$ is $\\frac12\\sin^2t$.\n\n'
    solution+='\n\nIntegrate over the complete traversal:\n\n'+aligned([
       r'\Gamma&=\int_0^{2\pi}\left('+tex(integrand)+r'\right)\,\mathrm dt',
       r'&=\left['+tex(primitive)+r'\right]_0^{2\pi}',r'&='+tex(result)+'.'])
    if h!=0:
        solution+='\n\nThe sine-squared term is zero at both endpoints. The varying term therefore integrates to zero; it is not zero at every point.'
    else:
        solution+='\n\nThe dot product is constant on this path.'
    if k==0:
        profile=profile or rng.choice(['radial-components','radial-cross'])
    else:
        profile=profile or rng.choice(list(PROFILES))
    kind='blank' if level=='hard' else 'radio'
    if replay_bank is not None:
        original_values,ci=replay_bank
        original_values=list(map(S.sympify,original_values))
        if S.simplify(original_values[ci]*S.pi-result)!=0:raise ValueError('Source replay key contradicts the circulation')
        vals=[original_values[ci]]+[v for i,v in enumerate(original_values) if i!=ci]
        recipes=['correct']+['historical-literal']*(len(vals)-1)
        profile='historical-replay'
    elif kind=='radio': vals,recipes=bank(a,b,k,o,d,e,profile)
    else: vals,recipes=[S.simplify(result/S.pi)],['correct'];profile='exact-entry'
    order=list(range(len(vals)));rng.shuffle(order)
    problem,solution=map(normalize_prose,(problem,solution))
    # Normalize before content identities, including complete bank semantics.
    values=[tex(v*S.pi) for v in vals]
    semantic=json.dumps([level,problem,solution,values,profile],sort_keys=True)
    content=hashlib.sha256(semantic.encode()).hexdigest()
    fieldid=identity(content+'/field')
    choices=[{':answer/id':identity(fieldid+'/'+values[i]),':answer/type':':answer.type/math',':answer/value':values[i]} for i in order]
    key=identity(fieldid+'/'+values[0])
    rec={'knowledge_point':KP.copy(),'question':{':question/id':identity(content),':question/difficulty':':question.difficulty/'+level,
        ':question/problem':problem,':question/worked-solution':solution,':question/answer-fields':[{':answer-field/id':fieldid,':answer-field/key':'value' if kind=='blank' else 'selection',':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':choices,':answer-field/correct':[':answer/id',key]}]},
        'generation':{'version':VERSION,'template':'supplied-path' if level=='easy' else 'implicit-curve',
          'family':'radial' if k==0 else ('mixed' if d or e else 'rotation'), 'profile':profile,
          'parameters':{name:str(v) for name,v in zip(['a','b','k','o','d','e'],[a,b,k,o,d,e])},
          'choice_recipes':{identity(fieldid+'/'+values[i]):recipes[i] for i in order},
          'solution_path':{'final':tex(result),'integrand':tex(integrand),'primitive':tex(primitive),
          'conversions':['sin^2(t)+cos^2(t)=1','integral sin(t)cos(t) dt = sin^2(t)/2'],
          'support':['e-9539','q-125446','q-125455','tutorial-5833','published-17592186708869' if level=='hard' else 'published-17592186708868'],
          'steps':['parametrize oriented path','substitute field','differentiate path','dot product','collect with Pythagorean identity','integrate and evaluate endpoints']}}}
    validate_generated_record(rec)
    return rec

def _sample(difficulty,count,seed):
    if difficulty=='unclassified':difficulty='moderate'
    if count<0:raise ValueError('negative count')
    rng=random.Random(seed)
    cases=[-1,0,1];rng.shuffle(cases)
    geometries=[True,False];rng.shuffle(geometries)
    out=[];seen=set();attempts=0;rotation_count=0
    bank_groups=[
       ['direction-traversal-area','axes-direction','direction-swapped-axes','direction-and-area'],
       ['paired-half-area','paired-double-axis','paired-lost-axis'],
       ['traversal-axes','area-and-axis','two-opposite-pairs']]
    rng.shuffle(bank_groups)
    axes=[S.Integer(1),S.Integer(2),S.Integer(3),S.Integer(4),S.Integer(5),S.sqrt(3),S.sqrt(5)]
    while len(out)<count:
        attempts+=1
        if attempts>max(1000,count*100):raise ValueError('requested batch exceeds available semantic instances')
        target=cases[len(out)%3]
        o=rng.choice([-1,1]);k=target*o*rng.choice([1,2])
        if difficulty=='hard':d,e=rng.choice([-2,-1,1,2]),rng.choice([-2,-1,1,2])
        elif target==0:d=e=rng.choice([-2,-1,1,2])
        else:d=e=0
        profile=rng.choice(['radial-components','radial-cross'] if k==0 else bank_groups[rotation_count%3])
        a=rng.choice(axes)
        b=a if geometries[len(out)%2] else rng.choice([v for v in axes if v!=a])
        token=tuple(map(str,(a,b,k,o,d,e)))
        if token in seen:continue
        try:rec=make(difficulty,a,b,k,o,d,e,profile,rng)
        except ValueError as exc:
            if 'degenerate complete bank' in str(exc):continue
            raise
        rec['generation'].update(seed=seed,index=len(out))
        out.append(rec);seen.add(token)
        if k!=0:rotation_count+=1
    return out


def _bank_cues(rec):
    """Choice-only actions; the key scores a cue but never helps select it."""
    f=rec['question'][':question/answer-fields'][0]
    p=rec['generation']['parameters']
    a,b,k,o,d,e=[S.sympify(p[n]) for n in ['a','b','k','o','d','e']]
    vals,_=bank(a,b,k,o,d,e,rec['generation']['profile'])
    by_tex={tex(v*S.pi):v for v in vals}
    ordered=[by_tex[v[':answer/value']] for v in f[':answer-field/choices']]
    ci=next(i for i,v in enumerate(f[':answer-field/choices']) if v[':answer/id']==f[':answer-field/correct'][1])
    numbers=list(map(float,ordered));hits=set()
    hits.add('position-'+str(ci))
    hits.add('rank-'+str(sorted(range(5),key=lambda i:numbers[i]).index(ci)))
    for name,fun in [('min-absolute',min),('max-absolute',max)]:
        z=fun(map(abs,numbers));ix=[i for i,v in enumerate(numbers) if abs(abs(v)-z)<1e-8]
        if ix==[ci]:hits.add(name)
    for sign in [-1,1]:
        if [i for i,v in enumerate(numbers) if S.sign(v)==sign]==[ci]:hits.add('unique-sign-'+str(sign))
    pairs=[(i,j) for i in range(5) for j in range(i+1,5) if S.simplify(ordered[i]+ordered[j])==0]
    majority=S.sign(sum(S.sign(z) for z in numbers))
    ix=[i for i in pairs[0] if S.sign(numbers[i])==majority] if len(pairs)==1 else []
    if ix==[ci]:hits.add('single-pair-majority')
    return hits

def _batch_bank_safe(records):
    groups={}
    for rec in records:
        p=rec['generation']['parameters'];a,b,k=map(S.sympify,[p['a'],p['b'],p['k']])
        if k==0:continue # zero is a mathematical invariant of diagonal fields
        for group in ['nonzero','circle' if a==b else 'ellipse',
                      'radical' if not (a.is_Integer and b.is_Integer) else 'integer-axes']:
            groups.setdefault(group,[]).append(_bank_cues(rec))
    return all(len(rows)<2 or not set.intersection(*rows) for rows in groups.values())

def generate(difficulty,count,seed):
    records=_sample(difficulty,count,seed)
    if difficulty=='hard' or _batch_bank_safe(records):return records
    # Keep the mathematical cases fixed. Re-select complete plausible error
    # profiles and positions until no tested action answers a repeated visible
    # subgroup. This is deterministic rejection using the original CLI seed.
    rng=random.Random(str(seed)+'/bank-repair/v1')
    for attempt in range(1000):
        candidate=[]
        for rec in records:
            p=rec['generation']['parameters']
            a,b,k,o,d,e=[S.sympify(p[n]) for n in ['a','b','k','o','d','e']]
            if k==0:candidate.append(rec);continue
            for _ in range(200):
                try:
                    new=make(difficulty if difficulty!='unclassified' else 'moderate',a,b,k,o,d,e,
                             profile=rng.choice(list(PROFILES)),rng=rng)
                    break
                except ValueError as exc:
                    if 'degenerate complete bank' not in str(exc):raise
            else:raise ValueError('No complete error profile for batch instance')
            new['generation'].update(seed=seed,index=len(candidate))
            candidate.append(new)
        if _batch_bank_safe(candidate):return candidate
    raise ValueError('No shortcut-safe complete bank assignment for requested batch')

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--difficulty',choices=['easy','moderate','hard','unclassified'],default='moderate')
    p.add_argument('--count',type=int,default=5);p.add_argument('--seed',type=int,required=True)
    p.add_argument('--format',choices=['json'],default='json');args=p.parse_args()
    print(json.dumps(generate(args.difficulty,args.count,args.seed),ensure_ascii=False,indent=2))
if __name__=='__main__':main()
