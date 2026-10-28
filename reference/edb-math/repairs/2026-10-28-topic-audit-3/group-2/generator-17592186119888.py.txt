"""Relocatable seeded surface-area package; all runtime data are adjacent.

Ordinary practice uses complete authored error profiles, chosen before values.
source_replay() preserves the original complete banks for fidelity verification.
"""
import collections
import argparse
import hashlib
import itertools
import json
import random
import uuid
from pathlib import Path
import sympy as s
from math_format import normalize_prose, normalize_tex, validate_generated_record

KP = '9361ad5a-b15c-507b-85d4-fe7ccb4d9fd8'
GEN = str(uuid.uuid5(uuid.UUID(KP), 'surface-area:2'))
u, v = s.symbols('u v', real=True)
LEVELS = ('easy', 'moderate', 'hard')
SOURCES = json.loads(Path(__file__).with_name('source_data.json').read_text())
SOURCE_IDS = {
    'graph': [17592186720665], 'affine': [17592186120078,17592186247030,17592186720667],
    'cylinder': [17592186247031], 'polynomial': [17592186247040],
    'disk': [17592186120079,17592186247046,17592186247100,17592186247141,17592186720655]}
FORMULA = r'A(S)=\iint_D\|\mathbf r_u\times\mathbf r_v\|\,\mathrm dA'


def tex(x):
    return normalize_tex(s.latex(s.simplify(x)))


def vec(xs):
    return r'\langle '+','.join(tex(x) for x in xs)+r'\rangle'


def display(x):
    return '$$\n'+x+'\n$$'


def aligned(rows):
    return display(r'\begin{aligned}'+'\n'+r'\\'.join(rows)+'\n'+r'\end{aligned}')


def cross(a,b):
    return [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]]


def integer_vector(rng, bound=3):
    return [rng.randint(-bound,bound) for _ in range(3)]


def rect(rng, curved=False):
    if curved:
        lo=rng.choice([-1,0,1]); hi=lo+rng.choice([1,2]); bot=rng.choice([1,2]); top=bot+rng.choice([1,2])
    else:
        lo=rng.choice([-2,-1,0,1]); hi=lo+rng.choice([1,2,3]); bot=rng.choice([-2,-1,0,1]); top=bot+rng.choice([1,2,3])
    return [lo,hi,bot,top]


def sample_instance(family,rng):
    if family in ('graph','affine','disk'):
        if family=='graph':
            a=[1,0,rng.randint(-2,2)]; b=[0,1,rng.randint(-2,2)]
        else:
            a=integer_vector(rng); b=integer_vector(rng)
        c=cross(a,b)
        if not any(c): raise ValueError('Degenerate affine map')
        shift=integer_vector(rng,2)
        r=[a[i]*u+b[i]*v+shift[i] for i in range(3)]
        domain= rng.choice([1,2,3,4,5,8,9]) if family=='disk' else rect(rng)
        return {'family':family,'r':r,'a':a,'b':b,'cross':c,'domain':domain}
    if family=='cylinder':
        p=rng.choice([1,2]); lo,hi=rng.choice([(0,s.sqrt(3)),(0,s.sqrt(8)),(1,s.sqrt(3)),(1,s.sqrt(8))])
        ul=rng.choice([-1,0,1]); width=rng.choice([1,2,3])
        return {'family':family,'r':[p*u,v**2,s.Rational(2,3)*v**3], 'domain':[ul,ul+width,lo,hi], 'p':p}
    return {'family':family,'r':[u**2,u*v,v**2/2], 'domain':rect(rng,True)}


ERRORS = {
    'graph': ['no_metric','square_norm','no_u_width','no_v_width','sum_widths','omit_0','omit_1','omit_2','add_cofactors'],
    'affine': ['no_metric','square_norm','no_u_width','no_v_width','sum_widths','omit_0','omit_1','omit_2','add_cofactors'],
    'disk': ['no_metric','square_norm','no_domain','radius','circumference','square_radius_again','no_pi','omit_0','omit_1','omit_2','add_cofactors'],
    'cylinder': ['no_width','square_norm','half_differential','wrong_primitive','drop_lower','add_endpoints','parameter_area','omit_v2_component','wrong_power'],
    'polynomial': ['omit_u_term','omit_v_term','no_divide_by_three','omit_u_width','omit_v_width','square_norm','drop_lower','parameter_area']}
PROFILES={f:list(itertools.combinations(names,4)) for f,names in ERRORS.items()}
COMBINED_GRAPH_PROFILE=('no_u_omit_2','no_u_omit_1','no_u_merge_01','sum_widths_omit_2')


def mathematics(inst):
    """Build the ordered learner derivation and identifiable error results."""
    family=inst['family']; r=inst['r']; a=[s.diff(x,u) for x in r]; b=[s.diff(x,v) for x in r]
    c=cross(a,b); norm2=s.expand(sum(x*x for x in c))
    intro='For a parametrization over $D$, use '+display(FORMULA)+ '\n\nDifferentiate and form the fundamental vector product:\n\n'
    determinant=r'\begin{vmatrix}\mathbf i&\mathbf j&\mathbf k\\'+ '&'.join(tex(x) for x in a)+r'\\'+'&'.join(tex(x) for x in b)+r'\end{vmatrix}'
    steps=intro+aligned([r'\mathbf r_u&='+vec(a)+',',r'\mathbf r_v&='+vec(b)+',',r'\mathbf r_u\times\mathbf r_v&='+determinant,r'&='+vec(c)+'.'])
    errors={}
    if family in ('graph','affine','disk'):
        metric=s.sqrt(norm2)
        if family=='disk':
            n=inst['domain']; areaD=s.pi*n
            region=f'The constraint is a disk in the parameter plane with radius ${tex(s.sqrt(n))}$. Its area is ${tex(s.pi)}({tex(s.sqrt(n))})^2={tex(areaD)}$.'
            errors.update(no_domain=metric,radius=s.pi*s.sqrt(n)*metric,circumference=2*s.pi*s.sqrt(n)*metric,square_radius_again=s.pi*n*n*metric,no_pi=n*metric)
        else:
            l,h,j,k=inst['domain']; w=h-l; z=k-j; areaD=w*z
            region=f'The parameter rectangle has side lengths ${h}-({l})={w}$ and ${k}-({j})={z}$, so its area is ${areaD}$.'
            errors.update(no_u_width=z*metric,no_v_width=w*metric,sum_widths=(w+z)*metric)
        key=areaD*metric
        errors.update(no_metric=areaD,square_norm=areaD*norm2)
        errors.update({f'omit_{i}':areaD*s.sqrt(norm2-c[i]**2) for i in range(3)})
        plus=[a[1]*b[2]+a[2]*b[1],a[2]*b[0]+a[0]*b[2],a[0]*b[1]+a[1]*b[0]]
        errors['add_cofactors']=areaD*s.sqrt(sum(x*x for x in plus))
        if family=='graph':
            errors.update(no_u_omit_2=z*s.sqrt(norm2-c[2]**2),no_u_omit_1=z*s.sqrt(norm2-c[1]**2),no_u_merge_01=z*s.sqrt((c[0]+c[1])**2+c[2]**2),sum_widths_omit_2=(w+z)*s.sqrt(norm2-c[2]**2))
        steps+='\n\n'+display(r'\|\mathbf r_u\times\mathbf r_v\|=\sqrt{'+ '+'.join('('+tex(x)+')^2' for x in c)+'}='+tex(metric)+'.')
        steps+='\n\n'+region+'\n\nThe area scale factor is constant, so\n\n'+aligned([r'A(S)&=\iint_D '+tex(metric)+r'\,\mathrm dA', r'&='+tex(metric)+r'\cdot\operatorname{Area}(D)',r'&='+tex(metric)+r'\cdot('+tex(areaD)+')='+tex(key)+'.'])
    else:
        l,h,j,k=map(s.sympify,inst['domain']); width=h-l; height=k-j
        bounds=r'\int_{'+tex(j)+'}^{'+tex(k)+r'}\int_{'+tex(l)+'}^{'+tex(h)+'}'
        if family=='cylinder':
            p=inst['p']; metric=2*p*v*s.sqrt(1+v*v); Wj=1+j*j; Wk=1+k*k
            upper=s.Rational(2,3)*p*width*Wk**s.Rational(3,2); lower=s.Rational(2,3)*p*width*Wj**s.Rational(3,2); key=upper-lower
            steps+='\n\n'+aligned([r'\|\mathbf r_u\times\mathbf r_v\|&=\sqrt{'+tex(norm2)+'}',r'&='+str(2*p)+r'\sqrt{v^2}\sqrt{1+v^2}',r'&='+tex(metric)+'.'])
            steps+='\n\n'+r'Since $v\ge0$ throughout $D$, $\sqrt{v^2}=v$. Integrate first with respect to $u$, then use $w=1+v^2$, $\mathrm dw=2v\,\mathrm dv$:'+'\n\n'
            steps+=aligned([r'A(S)&='+bounds+tex(metric)+r'\,\mathrm du\,\mathrm dv',r'&='+tex(p*width)+r'\int_{'+tex(Wj)+'}^{'+tex(Wk)+r'}\sqrt w\,\mathrm dw',r'&='+tex(p*width)+r'\left[\frac{2}{3}w^{3/2}\right]_{'+tex(Wj)+'}^{'+tex(Wk)+'}',r'&='+tex(upper)+'-('+tex(lower)+')='+tex(key)+'.'])
            errors=dict(no_width=key/width,square_norm=4*p*p*width*((k**5-j**5)/5+(k**3-j**3)/3),half_differential=key/2,wrong_primitive=p*width*(s.sqrt(Wk)-s.sqrt(Wj)),drop_lower=upper,add_endpoints=upper+lower,parameter_area=width*height,omit_v2_component=p*width*(k*k-j*j),wrong_power=s.Rational(2,3)*p*width*(Wk**2-Wj**2))
        else:
            metric=v*v+2*u*u
            first=width*(k**3-j**3)/3; second=2*(h**3-l**3)*height/3; key=first+second
            inner=width*v*v+s.Rational(2,3)*(h**3-l**3)
            primitive=width*v**3/3+s.Rational(2,3)*(h**3-l**3)*v
            steps+='\n\n'+aligned([r'\|\mathbf r_u\times\mathbf r_v\|&=\sqrt{'+tex(norm2)+'}',r'&=\sqrt{(v^2+2u^2)^2}',r'&=v^2+2u^2.'])
            steps+='\n\n'+r'The last equality holds because $v^2+2u^2\ge0$. The parameter region is rectangular, so'+'\n\n'
            steps+=aligned([r'A(S)&='+bounds+r'(v^2+2u^2)\,\mathrm du\,\mathrm dv',r'&=\int_{'+tex(j)+'}^{'+tex(k)+r'}\left[uv^2+\frac{2}{3}u^3\right]_{'+tex(l)+'}^{'+tex(h)+r'}\,\mathrm dv',r'&=\int_{'+tex(j)+'}^{'+tex(k)+'}('+tex(inner)+r')\,\mathrm dv',r'&=\left['+tex(primitive)+r'\right]_{'+tex(j)+'}^{'+tex(k)+'}',r'&=('+tex(primitive.subs(v,k))+')-('+tex(primitive.subs(v,j))+')='+tex(key)+'.'])
            squared=width*(k**5-j**5)/5+4*s.Rational(h**3-l**3,3)*(k**3-j**3)/3+4*s.Rational(h**5-l**5,5)*height
            errors=dict(omit_u_term=first,omit_v_term=second,no_divide_by_three=3*key,omit_u_width=first/width+second,omit_v_width=first+second/height,square_norm=squared,drop_lower=width*k**3/3+s.Rational(2,3)*(h**3-l**3)*k,parameter_area=width*height)
    return s.simplify(key), {name:s.simplify(x) for name,x in errors.items()},steps


def prompt(inst,level):
    family=inst['family']; r=inst['r']
    text='Find the surface area of the parametric surface\n\n'+display(r'\mathbf r(u,v)='+vec(r)+'.')
    if family=='disk': text+='\n\n'+r'subject to $u^2+v^2\le '+str(inst['domain'])+'$.'
    else:
        l,h,j,k=inst['domain']; text+='\n\nFor $'+tex(l)+r'\le u\le '+tex(h)+'$ and $'+tex(j)+r'\le v\le '+tex(k)+'$.'
    if level=='easy':
        text+='\n\n'+r'The tangent vectors are $\mathbf r_u='+vec([s.diff(x,u) for x in r])+r'$ and $\mathbf r_v='+vec([s.diff(x,v) for x in r])+'$. Use\n\n'+display(FORMULA+'.')
    return text


def record(problem,solution,level,bank,key,rng,metadata):
    problem=normalize_prose(problem); solution=normalize_prose(solution)
    values=[tex(x) if not isinstance(x,str) else normalize_tex(x) for x in bank]
    key=tex(key) if not isinstance(key,str) else normalize_tex(key)
    identity=json.dumps([level,problem,sorted(values)],ensure_ascii=False)
    qid=uuid.uuid5(uuid.UUID(GEN),identity); fid=uuid.uuid5(qid,'selection')
    choices=[{':answer/id':str(uuid.uuid5(fid,x)),':answer/type':':answer.type/math',':answer/value':x} for x in values]
    rng.shuffle(choices)
    q={':question/id':str(qid),':question/problem':problem,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+level,':question/answer-fields':[{':answer-field/id':str(fid),':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/correct':[':answer/id',str(uuid.uuid5(fid,key))],':answer-field/choices':choices}]}
    result={'knowledge_point':{'db_id':17592186119888,'id':KP,'title':'Finding the Surface Area of a Parametric Surface'},'question':q,'generation':{'version':'2.0.0','generator_id':GEN,**metadata}}
    return validate_generated_record(result)


def build(inst,level,profile,rng,with_cues=False):
    key,errors,solution=mathematics(inst)
    values=[key]+[errors[name] for name in profile]
    if any(x.is_positive is not True for x in values): raise ValueError('Nonpositive area candidate')
    if len({tex(x) for x in values})!=5: raise ValueError('Colliding complete error bank')
    # Compare algebraically, not just TeX spellings.
    if any(s.simplify(a-b)==0 for a,b in itertools.combinations(values,2)): raise ValueError('Equivalent choices')
    metadata={'family':inst['family'],'profile':list(profile),'source_question_ids':SOURCE_IDS[inst['family']],'instance':{'surface':[str(x) for x in inst['r']],'domain':str(inst['domain'])},'bank_policy':'authored complete error profile'}
    rec=record(prompt(inst,level),solution,level,values,key,rng,metadata)
    if not with_cues:
        return rec
    field=rec['question'][':question/answer-fields'][0]
    position=next(i for i,x in enumerate(field[':answer-field/choices']) if x[':answer/id']==field[':answer-field/correct'][1])
    pieces=[x.as_coeff_Mul() for x in values]
    coefficients=collections.Counter(a for a,b in pieces)
    factors=collections.Counter(b for a,b in pieces)
    modal=[i for i,(a,b) in enumerate(pieces) if coefficients[a]==max(coefficients.values()) and factors[b]==max(factors.values())]
    rationals=[i for i,x in enumerate(values) if x.is_Rational]
    radicals=[i for i,x in enumerate(values) if x.has(s.Pow) and not x.is_Rational]
    cues={'position':position,'rank':sum(bool(x<key) for x in values),
          'modal': (len(modal)==1,modal==[0]),
          'rational': (len(rationals)==1,rationals==[0]),
          'radical': (len(radicals)==1,radicals==[0])}
    return rec,cues


def batch_cues_allowed(rows):
    # A repeated visible family must not teach a fixed position/rank or a
    # successful bank-only modal/unique-form action. Singletons do not establish
    # a repeated-family pattern. This guards constructed batches, not seeds.
    if len(rows)<2:
        return True
    if any(len({row[cue] for row in rows})==1 for cue in ('position','rank')):
        return False
    for cue in ('modal','rational','radical'):
        attempted=[correct for row in rows for applies,correct in [row[cue]] if applies]
        if len(attempted)>=2 and all(attempted):
            return False
    return True


def families(level):
    return {'easy':['graph'],'moderate':['affine','cylinder','polynomial'],'hard':['disk']}[level]


def batch(level,count,seed):
    if level=='unclassified': level='moderate'
    if level not in LEVELS or count<0: raise ValueError('Invalid difficulty/count')
    rng=random.Random(seed); output=[]; seen=set(); order=[]; cue_groups=collections.defaultdict(list)
    # Both independently plausible bank constructions occur in ordinary easy
    # batches. This prevents modal coefficient/factor agreement from being a key.
    combined_start=rng.randrange(2) if level=='easy' else 0
    for index in range(count):
        if not order:
            order=families(level)[:]; rng.shuffle(order)
        family=order.pop()
        for attempt in range(1000):
            profile=COMBINED_GRAPH_PROFILE if family=='graph' and (index+combined_start)%2 else rng.choice(PROFILES[family])  # complete profile before values
            try:
                inst=sample_instance(family,rng)
                rec,cues=build(inst,level,profile,rng,with_cues=True)
            except ValueError:
                continue
            # Incidental translations and affine rectangle repositioning do not count as novelty.
            sig=([str(s.diff(x,u)) for x in inst['r']],[str(s.diff(x,v)) for x in inst['r']],
                 inst['domain'] if family in ('disk','polynomial') else (inst['domain'][1]-inst['domain'][0],str(inst['domain'][2]),str(inst['domain'][3])) if family=='cylinder' else (inst['domain'][1]-inst['domain'][0],inst['domain'][3]-inst['domain'][2]))
            fingerprint=repr(sig)
            if fingerprint in seen: continue
            if not batch_cues_allowed(cue_groups[family]+[cues]): continue
            cue_groups[family].append(cues)
            seen.add(fingerprint);rec['generation']['seed']=seed;rec['generation']['batch_index']=index;output.append(rec);break
        else: raise ValueError('Unable to construct distinct valid complete banks')
    return output


def replay_solution(text):
    # The capture used grouping braces for set notation, which TeX hides.
    # Escape only the outer D braces; preserve nested radicals and expressions.
    marker='D={(u,v)'
    if marker in text:
        pos=text.index(marker)+2; end=pos+1; depth=1
        while depth:
            if text[end]=='{': depth+=1
            elif text[end]=='}': depth-=1
            end+=1
        text=text[:pos]+r'\{'+text[pos+1:end-1]+r'\}'+text[end:]
    return text


def source_replay():
    result=[]
    for q in SOURCES:
        f=q[':question/answer-fields'][0]; key=f[':answer-field/correct'][':answer/value']
        result.append(record(q[':question/problem'],replay_solution(q[':question/worked-solution']),q[':question/difficulty'][':db/ident'].split('/')[-1],[x[':answer/value'] for x in f[':answer-field/choices']],key,random.Random(0),{'source_replay':q[':question/math-academy-id'],'source_question_ids':[q[':db/id']]}))
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--difficulty',required=True,choices=(*LEVELS,'unclassified'));parser.add_argument('--count',type=int,default=1);parser.add_argument('--seed',type=int,default=0);parser.add_argument('--format',choices=['json'],default='json');args=parser.parse_args()
    print(json.dumps(batch(args.difficulty,args.count,args.seed),indent=2))
