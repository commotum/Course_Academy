#!/usr/bin/env python3
"""Seeded Green's theorem integrand practice. No services or database writes."""
import argparse
import hashlib
import itertools
import json
import os
from pathlib import Path
import random
import uuid
import sympy as s
from math_format import normalize_prose, normalize_tex, validate_generated_record

VERSION = 'greens-oriented-v2'
KP = {'db_id':17592186133882,'id':'bf385144-2f48-5874-8c0d-dec31d8fc6e3',
      'title':"Expressing a Line Integral as a Double Integral Using Green's Theorem"}
x,y=s.symbols('x y', real=True)
SQUARE='images/aa/aa60dd35a920d166f7cc3238a366bde93bd2c33e1b39b0a38313ab46a8de2d8b.png'
TRIANGLE='images/0d/0dfe132146c4095954d6b628b055317c975fed6ec429b9ad48b68f4015d6c033.png'
FAMILIES={'easy':['triangle-polynomial','square-polynomial','mixed-polynomial'],
          'moderate':['exp-product','exp-pair','trig-product'],
          'hard':['exp-product','exp-pair','trig-product']}
SOURCES={'triangle-polynomial':['q-109111'],'square-polynomial':['q-108588'],
         'mixed-polynomial':['q-108830'],'exp-product':['q-109114'],
         'exp-pair':['q-109114','q-109112'],'trig-product':['q-109112']}
PROFILES={
 'subtraction':('reverse','add','omit-P','omit-Q'),
 'signs':('add','negative-add','omit-P','omit-Q'),
 'variables':('wrong-both','wrong-P','wrong-Q','add'),
 'recognition':('reverse','coefficients','zero','wrong-both'),
 'mixed':('omit-P','wrong-Q','negative-add','zero')}


def tex(z):
    # Expand only products and collect like terms; no trig/function rewrites.
    return normalize_tex(s.latex(s.expand(z)))


def choice_tex(z):
    """Break long additive banks without changing the mathematical expression."""
    parts=s.expand(z).as_ordered_terms()
    if len(parts)<4:return tex(z)
    rows=[]
    for i in range(0,len(parts),2):
        row=tex(s.Add(*parts[i:i+2]))
        if i and not row.lstrip().startswith('-'):row='+'+row
        rows.append(row)
    return normalize_tex(r'\begin{aligned}&'+r'\\&\quad'.join(rows)+r'\end{aligned}')


def uid(z):
    return str(uuid.uuid5(uuid.UUID(KP['id']),VERSION+':'+z))


def terms(family,p):
    """Learner derivation built by explicit power/product/chain rules."""
    a,b,c,d,k,h=(s.Integer(p.get(n,0)) for n in ('a','b','c','d','k','h'))
    if family=='triangle-polynomial':
        return a*y**2,b*x*y,2*a*y,b*y
    if family=='square-polynomial':
        return a*y**2,b*x*y+c*x**2,2*a*y,b*y+2*c*x
    if family=='mixed-polynomial':
        return a*x**2*y**2,b*x**3*y+h*s.sin(y),2*a*x**2*y,3*b*x**2*y
    E=s.exp(k*x*y)
    if family=='exp-product':
        return (a*y**2*E+c*y**2,b*x*y*E+d*x**2*y,
                (2*a*y+a*k*x*y**2)*E+2*c*y,(b*y+b*k*x*y**2)*E+2*d*x*y)
    if family=='exp-pair':
        return (a*y*E+c*y**2,b*x*E+d*x**2*y,
                a*(1+k*x*y)*E+2*c*y,b*(1+k*x*y)*E+2*d*x*y)
    if family=='trig-product':
        return (a*y*s.sin(y)-c*x**2*y,b*x*s.sin(y)+d*x*y*s.cos(y),
                a*s.sin(y)+a*y*s.cos(y)-c*x**2,b*s.sin(y)+d*y*s.cos(y))
    raise ValueError(f'Unknown family {family}')


def sample_parameters(family,relationship,rng):
    signed=(-3,-2,-1,1,2,3)
    a=rng.choice((-2,-1,1,2)); b=rng.choice(signed)
    if family=='triangle-polynomial':
        b={'equal':2*a,'partial':a,'unequal':-a}[relationship]
    elif family=='mixed-polynomial':
        if relationship=='equal': a,b=3*rng.choice((-1,1)),2*rng.choice((-1,1)); b=2*(a//3)
        elif relationship=='partial': b=a
        else: b=-a
    elif family in ('exp-product','trig-product'):
        b=2*a if relationship=='equal' else (a if relationship=='partial' else -a)
    elif family=='exp-pair':
        b=a if relationship in ('equal','partial') else -a
    c=rng.choice((-1,0,1));d=rng.choice((-1,0,1));h=rng.choice((-2,-1,1,2))
    if family=='trig-product':
        b=a if relationship in ('equal','sin-cancels') else -a
        d=a if relationship in ('equal','cos-cancels') else -a
    return dict(a=a,b=b,c=c,d=d,k=1,h=h)


def bank(P,Q,A,B,orientation,profile):
    z=orientation
    candidates={'correct':s.expand(z*(B-A)), 'reverse':z*(A-B),
      'add':z*(B+A),'negative-add':-z*(B+A), 'omit-P':z*B,'omit-Q':-z*A,
      'wrong-both':z*(s.diff(Q,y)-s.diff(P,x)),
      'wrong-P':z*(B-s.diff(P,x)), 'wrong-Q':z*(s.diff(Q,y)-A),
      'coefficients':z*(Q-P),'zero':s.Integer(0)}
    names=['correct',*PROFILES[profile]]
    values=[s.expand(candidates[n]) for n in names]
    # Whole selected profiles are retained or rejected, never truncated/padded.
    if any(s.expand(a-b)==0 for a,b in itertools.combinations(values,2)):
        raise ValueError('Equivalent alternatives in selected bank')
    return list(zip(names,values))


def clockwise_image():
    dest=Path(os.environ['COURSE_ACADEMY_GENERATOR_OUTPUT_DIR']).resolve()
    dest.mkdir(parents=True,exist_ok=True)
    target=dest/'clockwise-square.png'
    if not target.exists():
        os.environ.setdefault('MPLCONFIGDIR',str(dest/'.matplotlib'))
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        from matplotlib.patches import Polygon
        fig,ax=plt.subplots(figsize=(3.8,3.4),dpi=130)
        ax.add_patch(Polygon([(0,0),(0,1),(1,1),(1,0)],facecolor='#d5e8f5',edgecolor='#d99000',linewidth=1.7))
        for start,end in [((0,.25),(0,.7)),((.25,1),(.7,1)),((1,.7),(1,.25)),((.7,0),(.25,0))]:
            ax.annotate('',xy=end,xytext=start,arrowprops={'arrowstyle':'->','lw':1.3})
        for px,py in [(0,0),(0,1),(1,1),(1,0)]:
            ax.text(px+(.05 if px else -.2),py+(.05 if py else -.12),f'({px},{py})',fontsize=10)
        ax.text(.45,.45,'$D$',fontsize=16);ax.set(xlim=(-.3,1.35),ylim=(-.25,1.25),aspect='equal');ax.axis('off')
        fig.savefig(target,bbox_inches='tight',facecolor='white');plt.close(fig)
    return "clockwise-square.png"


def make_record(level,family,p,orientation=1,profile='subtraction',seed=0,start=0,
                explicit=None,source_override=None):
    P,Q,A,B=terms(family,p) if source_override is None else source_override['terms']
    key=s.expand(orientation*(B-A))
    values=bank(P,Q,A,B,orientation,profile) if source_override is None else source_override['bank']
    square=[(0,0),(1,0),(1,1),(0,1)]
    vertices=square if orientation==1 else list(reversed(square))
    vertices=vertices[start:]+vertices[:start]
    orient='counterclockwise' if orientation==1 else 'clockwise'
    implicit=(level=='hard') if explicit is None else not explicit
    if implicit:
        route=r'\longrightarrow'.join(f'({a},{b})' for a,b in vertices+[vertices[0]])
        lead='The curve $C$ follows the straight sides of a square in the order\n\n$$\n'+route+'.\n$$\n\nLet $D$ be its interior.'
    elif family=='triangle-polynomial':
        lead='Let $C$ be the boundary of the triangle with vertices $(-1,0)$, $(1,0)$ and $(0,1)$, traversed '+orient+', and let $D$ be its interior.'
    else:
        lead='Let $C$ be the boundary of the unit square, traversed '+orient+', and let $D$ be its interior.'
    integral=(r'\begin{aligned}&\oint_C\left('+tex(P)+r'\right)\,\mathrm{d}x\\'
              +r'&\quad+\left('+tex(Q)+r'\right)\,\mathrm{d}y=\iint_D f(x,y)\,\mathrm{d}A.\end{aligned}')
    prompt=lead+'\n\nUse Green\'s theorem to choose the function $f(x,y)$ in\n\n$$\n'+integral+'\n$$'
    image=TRIANGLE if family=='triangle-polynomial' and not implicit else (SQUARE if orientation==1 else clockwise_image())
    if source_override and source_override.get('image'):image=source_override['image']
    intro=(('The traversal keeps the interior on the left, so it is **counterclockwise**.' if orientation==1 else
            'The traversal keeps the interior on the right, so it is **clockwise**.') if implicit else
           'The stated traversal is **'+orient+'**.')
    theorem=(r'\oint_C P\,\mathrm{d}x+Q\,\mathrm{d}y=\iint_D(Q_x-P_y)\,\mathrm{d}A.' if orientation==1 else
             r'\begin{aligned}\oint_C P\,\mathrm{d}x+Q\,\mathrm{d}y&=-\iint_D(Q_x-P_y)\,\mathrm{d}A\\&=\iint_D(P_y-Q_x)\,\mathrm{d}A.\end{aligned}')
    solution=(intro+' Green\'s theorem applies because both coefficients have continuous first partial derivatives on an open region containing $D$. '
       +('For this orientation,' if orientation==1 else 'Reversing the positively oriented boundary changes the sign, so')
       +'\n\n$$\n'+theorem+'\n$$\n\n![The region and oriented boundary.]('+image+')\n\n'
       +'Identify the coefficients of the two differentials:\n\n$$\n'
       +r'\begin{aligned}P(x,y)&='+tex(P)+r',\\Q(x,y)&='+tex(Q)+r'.\end{aligned}'+'\n$$\n\n'
       +'Hold the other variable constant when taking each partial derivative. '
       +('Apply the product and chain rules where required.' if family.startswith(('exp','trig')) else 'Apply the power rule to each relevant term.')
       +'\n\n$$\n'+r'\begin{aligned}P_y&='+tex(A)+r',\\Q_x&='+tex(B)+r'.\end{aligned}'+'\n$$\n\n'
       +'Subtract the entire derivative in the order required by the traversal, then collect like terms:\n\n$$\n'
       +r'\begin{aligned}f(x,y)&='+('Q_x-P_y' if orientation==1 else 'P_y-Q_x')+r'\\'
       +r'&=\left('+tex(B if orientation==1 else A)+r'\right)\\'
       +r'&\quad-\left('+tex(A if orientation==1 else B)+r'\right)\\'
       +r'&='+tex(key)+r'.\end{aligned}'+'\n$$\n\nThus $f(x,y)='+tex(key)+'$. No evaluation of the double integral is needed.')
    if source_override:
        prompt=source_override['prompt']
        solution=source_override.get('solution',solution)
    prompt,solution=normalize_prose(prompt),normalize_prose(solution)
    # Content identities exclude seed and cosmetic order, include the complete bank.
    value_strings=[(n,choice_tex(v)) for n,v in values]
    identity=json.dumps([level,prompt,solution,sorted(v for _,v in value_strings)],sort_keys=True)
    qid=uid(identity);fid=uid(qid+':selection')
    answers=[{':answer/id':uid(fid+':'+str(i)+':'+v),':answer/type':':answer.type/math',':answer/value':v}
             for i,(_,v) in enumerate(value_strings)]
    correct=answers[[n for n,v in value_strings].index('correct')][':answer/id']
    random.Random(str(seed)+qid).shuffle(answers)
    record={'knowledge_point':KP.copy(),'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+level,
        ':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':[
          {':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',
           ':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]}]},
        'generation':{'version':VERSION,'template':family,'parameters':p,'orientation':orientation,'start':start,
          'bank_profile':profile,'source_ids':SOURCES.get(family,[]),'seed':seed,
          'ordered_derivation':{'P':str(P),'Q':str(Q),'P_y':str(A),'Q_x':str(B),'final':str(key)},
          'choice_recipes':{v:n for n,v in value_strings}}}
    return validate_generated_record(record)



def decision_signature(record):
    """Bank-only cues used to keep a repeated family from becoming predictable.

    Both fixed interior points predate sampling; neither is a target-dependent
    evaluation. All expressions remain whole, plausible error profiles. This is
    a batch diversity guard, not a change to the mathematical task or solution.
    """
    meta=record['generation']
    P,Q,A,B=terms(meta['template'],meta['parameters'])
    values=[v for _,v in bank(P,Q,A,B,meta['orientation'],meta['bank_profile'])]
    strings=[choice_tex(v) for v in values]
    result={}
    for index,point in enumerate(((s.Rational(2,5),s.Rational(3,7)),
                                  (s.Rational(1,3),s.Rational(2,3)))):
        nums=[float(v.subs({x:point[0],y:point[1]})) for v in values]
        result['rank-'+str(index)]=(sorted(range(5),key=lambda i:nums[i]).index(0)
            if len(set(round(n,10) for n in nums))==5 else None)
        for sign in (-1,1):
            result['unique-sign-'+str(index)+'-'+str(sign)]=[
                i for i,n in enumerate(nums) if sign*n>0]==[0]
    result['unique-shortest']=[i for i,t in enumerate(strings) if len(t)==min(map(len,strings))]==[0]
    result['unique-multiline']=[i for i,t in enumerate(strings) if r'\begin{aligned}' in t]==[0]
    result['unique-zero']=[i for i,v in enumerate(values) if v==0]==[0]
    result['unique-exp-free']=[i for i,v in enumerate(values) if not v.has(s.exp)]==[0]
    return result


def diverse_after(previous,current):
    if not previous:return True
    for cue,value in current.items():
        if cue.startswith('rank-'):
            if value is not None and all(row[cue]==value for row in previous):return False
        elif value and all(row[cue] for row in previous):return False
    return True


def generate_batch(difficulty,count,seed):
    if difficulty=='unclassified':difficulty='easy'
    if difficulty not in FAMILIES:raise ValueError('Expected easy, moderate or hard')
    if not 1<=count<=1000:raise ValueError('Count must be 1..1000')
    rng=random.Random(seed);out=[];seen=set();signatures={}
    families=FAMILIES[difficulty].copy();rng.shuffle(families)
    # Plan target families/relationships before values; full cycles prevent a small
    # batch from degenerating to amplitude-only clones of one source arrangement.
    relationships=['equal','partial','unequal'];rng.shuffle(relationships)
    directions=[1,-1];rng.shuffle(directions)
    trig_roles=['equal','sin-cancels','cos-cancels','unequal']
    if difficulty!='easy':rng.shuffle(trig_roles)
    for i in range(count):
        family=families[i%len(families)];relationship=(trig_roles[(i//len(families))%4] if family=='trig-product' else relationships[(i//len(families)+i)%3])
        orientation=directions[i%2] if difficulty=='hard' else 1
        for attempt in range(300):
            p=sample_parameters(family,relationship,rng);profile=rng.choice(list(PROFILES))
            try:r=make_record(difficulty,family,p,orientation,profile,seed,rng.randrange(4))
            except ValueError:continue
            semantic=(family,tuple(tex(z) for z in terms(family,p)[:2]),orientation)
            if semantic in seen:continue
            signature=decision_signature(r)
            previous=signatures.setdefault(family,[])
            if not diverse_after(previous,signature):continue
            previous.append(signature)
            seen.add(semantic);r['generation']['relationship']=relationship;out.append(r);break
        else:raise RuntimeError('Cannot construct enough distinct valid banks')
    return out


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty',choices=['unclassified','easy','moderate','hard'],default='easy')
    parser.add_argument('--count',type=int,default=1);parser.add_argument('--seed',type=int,default=0)
    parser.add_argument('--format',choices=['json'],default='json');args=parser.parse_args()
    print(json.dumps(generate_batch(args.difficulty,args.count,args.seed),indent=2))

if __name__=='__main__':main()
