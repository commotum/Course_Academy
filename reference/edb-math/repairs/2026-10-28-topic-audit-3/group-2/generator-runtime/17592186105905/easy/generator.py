#!/usr/bin/env python3
"""Seeded, relocatable quadrilateral-area generator; no database access."""
from __future__ import annotations
import argparse, copy, hashlib, itertools, json, math, os, random, re, sys, uuid
from functools import lru_cache
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from math_format import normalize_prose, validate_generated_record
os.environ.setdefault('MPLCONFIGDIR', '/tmp/course-academy-quadrilateral-mpl')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Arc

VERSION='quadrilateral-included-angles-2'
KP={'db_id':17592186105905,'id':'3173d361-b91d-5699-97d8-6595ef59d0a3','title':'Calculating the Area of a Quadrilateral'}
NS=uuid.UUID(KP['id'])
HERE=Path(__file__).resolve().parent
BANDS=('easy','moderate','hard')
# Each tuple is one complete, authored bank profile, selected before parameters.
PROFILES={
 'para':[
  ('half','product','cos','square_a'),
  ('product','cos','square_a','radian'),
  ('halfproduct','cos','square_b','radian'),
  ('double','square_a','square_b','cos'),
 ],
 'general':[
  ('first','second','double','difference'),
  ('first','nohalf_first','nohalf_second','double'),
  ('half_first','half_second','cos_first','cos_second'),
  ('cos_both','radian','nohalf_first','half_second'),
 ]}

def digest(v): return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def sine(t):return {30:0.5,90:1.0,150:0.5}.get(t,math.sin(math.radians(t)))
def ray(r,t):return (r*math.cos(math.radians(t)),r*sine(t))
def num(x):return str(int(x)) if float(x).is_integer() else str(x)
def rounded(x):return str(Decimal(str(x)).quantize(Decimal('0.1'),rounding=ROUND_HALF_UP))
def cross(a,b,c):return (b[0]-a[0])*(c[1]-b[1])-(b[1]-a[1])*(c[0]-b[0])

def geometry(p):
    if p['family']=='split':
        return dict(A=(0.,0.),B=(p['a'],0.),C=ray(p['l'],p['beta']),D=ray(p['b'],p['beta']+p['gamma']))
    a,b,t=p['a'],p['b'],p['theta']
    pts=dict(A=(0.,0.),B=(a,0.),D=ray(b,t))
    if p['family']=='para':
        pts['C']=(a+pts['D'][0],pts['D'][1]);return pts
    B,D=pts['B'],pts['D'];v=(D[0]-B[0],D[1]-B[1]);L=math.hypot(*v)
    c,d=p['c'],p['d'] # BC and DC respectively
    x=(c*c+L*L-d*d)/(2*L);h=math.sqrt(c*c-x*x)
    pts['C']=(B[0]+x*v[0]/L+h*v[1]/L,B[1]+x*v[1]/L-h*v[0]/L)
    return pts

def legible(p):
    try:pts=geometry(p)
    except (ValueError,ZeroDivisionError):return False
    poly=[pts[k] for k in 'ABCD']
    if not all(cross(poly[i],poly[(i+1)%4],poly[(i+2)%4])>1e-7 for i in range(4)):return False
    for i in range(4):
        q=poly[i];a=poly[(i-1)%4];b=poly[(i+1)%4]
        x=(a[0]-q[0],a[1]-q[1]);y=(b[0]-q[0],b[1]-q[1])
        co=sum(v*w for v,w in zip(x,y))/math.hypot(*x)/math.hypot(*y)
        if math.degrees(math.acos(max(-1,min(1,co))))<20:return False
    return True

@lru_cache(None)
def catalog():
    """Exact shared diagonal lengths using integer cosine values 2 cos(theta)."""
    groups={}
    for a in range(4,17):
      for b in range(a,17):
       for t,cos2 in [(60,1),(90,0),(120,-1)]:
        groups.setdefault(a*a+b*b-cos2*a*b,[]).append((a,b,t))
    result=[]
    for triples in groups.values():
      for (a,b,t),(c,d,f) in itertools.combinations(triples,2):
        p=dict(family='general',a=a,b=b,theta=t,c=c,d=d,phi=f)
        if abs(a*b*sine(t)-c*d*sine(f))<1e-7:continue
        if legible(p):result.append(p)
    return result

def sample_instance(level,rng,family=None):
    family=family or ('split' if level=='hard' else rng.choice(['para','general']))
    if family=='para':
        p=dict(family=family,a=rng.randint(5,15),b=rng.randint(5,15),theta=rng.choice([35,40,45,50,55,60,65,70,75,100,110,115,120,125,130,135,140]))
    elif family=='general':
        p=dict(rng.choice(catalog()))
        if rng.randrange(2):
            p['a'],p['b'],p['theta'],p['c'],p['d'],p['phi']=p['c'],p['d'],p['phi'],p['a'],p['b'],p['theta']
        if rng.randrange(2):p['a'],p['b']=p['b'],p['a']
        if rng.randrange(2):p['c'],p['d']=p['d'],p['c']
    else:
        p=dict(family='split',a=rng.randint(7,13),b=rng.randint(7,13),l=rng.randint(8,14),beta=rng.choice([25,30,35,40,45,50,55,60,65,70,90,100]),gamma=rng.choice([25,30,35,40,45,50,55,60,65,70,90,100]))
        if not 80<=p['beta']+p['gamma']<=145:raise ValueError('full angle outside legible range')
        p['known']=rng.choice(['beta','gamma'])
    p['rotation']=rng.randrange(4)
    if not legible(p):raise ValueError('nonconvex or cramped geometry')
    return p

def derivation(p):
    """Keep the ordered operator inputs and supplied/derived angles intact."""
    if p['family']=='split':
        triples=[('ABC',p['a'],p['l'],p['beta']),('ACD',p['l'],p['b'],p['gamma'])]
    else:
        triples=[('ABD',p['a'],p['b'],p['theta'])]
        if p['family']=='general':triples.append(('BCD',p['c'],p['d'],p['phi']))
    terms=[dict(triangle=tri,sides=[a,b],angle=t,coefficient=a*b/2,value=a*b*sine(t)/2) for tri,a,b,t in triples]
    return dict(terms=terms,total=sum(t['value'] for t in terms)*(2 if p['family']=='para' else 1),combine='double' if p['family']=='para' else 'sum')

def bank(p,profile):
    d=derivation(p);u=d['terms'][0]['value'];T=d['total'];a,b=p['a'],p['b']
    if p['family']=='para':
        t=p['theta'];P=a*b
        errors=dict(half=T/2,double=2*T,product=P,cos=P*abs(math.cos(math.radians(t))),halfproduct=P/2,square_a=a*a*sine(t),square_b=b*b*sine(t),radian=P*abs(math.sin(t)))
    else:
        v=d['terms'][1]['value'];t=p['theta'];f=p['phi']
        cu=a*b*abs(math.cos(math.radians(t)))/2;cv=p['c']*p['d']*abs(math.cos(math.radians(f)))/2
        errors=dict(first=u,second=v,double=2*T,difference=abs(u-v),half_first=u/2+v,half_second=u+v/2,nohalf_first=2*u+v,nohalf_second=u+2*v,cos_first=cu+v,cos_second=u+cv,cos_both=cu+cv,radian=abs(a*b*math.sin(t)/2+p['c']*p['d']*math.sin(f)/2))
    values=[rounded(T)]+[rounded(errors[r]) for r in profile]
    sortedvals=sorted(map(float,values))
    if sortedvals[0]<=0 or any(y-x<2-1e-9 for x,y in zip(sortedvals,sortedvals[1:])):raise ValueError('colliding or cramped complete bank')
    # Redundant error combinations can expose the key using the bank alone.
    # Test the displayed rounded bank, without consulting which value is correct.
    doubled=[(i,j) for i,x in enumerate(map(float,values))
             for j,y in enumerate(map(float,values)) if i!=j and abs(2*x-y)<=.151]
    chain_centers=[i for i in range(5) if any(j==i for _,j in doubled)
                   and any(j==i for j,_ in doubled)]
    touched={i for edge in doubled for i in edge}
    if len(chain_centers)==1 or (len(doubled)==2 and len(touched)==4):
        raise ValueError('redundant doubling structure in complete bank')
    return values

def labels(p):
    return dict(zip('ABCD','ABCD'[p['rotation']:]+ 'ABCD'[:p['rotation']]))
def named(text,p):return ''.join(labels(p).get(c,c) for c in text)
def angletext(s,t):return rf'$\angle {s}={num(t)}^\circ$'

def measurements(p,level):
    n=lambda s:named(s,p)
    if p['family']=='split':
        known=p['known'];part='BAC' if known=='beta' else 'CAD'
        if level!='hard':
            return ', '.join([rf'${n("AB")}={p["a"]}$',rf'${n("AD")}={p["b"]}$',rf'${n("AC")}={p["l"]}$',angletext(n('BAC'),p['beta']),angletext(n('CAD'),p['gamma'])])
        return ', '.join([rf'${n("AB")}={p["a"]}$',rf'${n("AD")}={p["b"]}$',rf'${n("AC")}={p["l"]}$',angletext(n('DAB'),p['beta']+p['gamma']),angletext(n(part),p[known])])
    parts=[rf'${n("AB")}={p["a"]}$',rf'${n("AD")}={p["b"]}$',angletext(n('BAD'),p['theta'])]
    if p['family']=='general':parts += [rf'${n("BC")}={p["c"]}$',rf'${n("CD")}={p["d"]}$',angletext(n('BCD'),p['phi'])]
    return ', '.join(parts)

def draw(p,level,solution,output):
    pts=geometry(p);xy=[pts[k] for k in 'ABCD'];cx=sum(x for x,y in xy)/4;cy=sum(y for x,y in xy)/4
    span=max(max(x for x,y in xy)-min(x for x,y in xy),max(y for x,y in xy)-min(y for x,y in xy))
    fig,ax=plt.subplots(figsize=(6.4,4.4),dpi=135)
    ax.add_patch(Polygon(xy,closed=True,facecolor='#eff6fb',edgecolor='#172b3b',lw=1.8,zorder=1))
    diag='AC' if p['family']=='split' else 'BD'
    if level!='moderate' or solution or p['family']=='split':
        a,b=[pts[k] for k in diag];ax.plot([a[0],b[0]],[a[1],b[1]],'--',color='#4d6374',lw=1.3,zorder=2)
    for k,(x,y) in pts.items():
        dx,dy=x-cx,y-cy;norm=math.hypot(dx,dy)
        ax.text(x+.045*span*dx/norm,y+.045*span*dy/norm,labels(p)[k],ha='center',va='center',fontstyle='italic',fontsize=13)
    def edge(k,l,v,internal=False):
        a,b=pts[k],pts[l];x,y=(a[0]+b[0])/2,(a[1]+b[1])/2
        dx,dy=b[1]-a[1],a[0]-b[0]
        if dx*(x-cx)+dy*(y-cy)<0:dx,dy=-dx,-dy
        norm=math.hypot(dx,dy);offset=.033 if internal else .055
        ax.text(x+offset*span*dx/norm,y+offset*span*dy/norm,num(v),ha='center',va='center',fontsize=12,zorder=5,bbox=dict(facecolor='white',edgecolor='none',pad=.8))
    def arc(k,l,m,v,r=.095,lr=.16,color='#266b9a'):
        o,a,b=pts[k],pts[l],pts[m]
        start=math.degrees(math.atan2(a[1]-o[1],a[0]-o[0]));end=math.degrees(math.atan2(b[1]-o[1],b[0]-o[0]));delta=(end-start)%360
        if delta>180:start=end;delta=360-delta
        ax.add_patch(Arc(o,2*r*span,2*r*span,theta1=start,theta2=start+delta,color=color,lw=1.2,zorder=3))
        mid=math.radians(start+delta/2)
        ax.text(o[0]+lr*span*math.cos(mid),o[1]+lr*span*math.sin(mid),num(v)+'°',ha='center',va='center',fontsize=10.5,zorder=4,color=color,bbox=dict(facecolor='#eff6fb',edgecolor='none',pad=.3))
    edge('A','B',p['a']);edge('A','D',p['b'])
    if p['family']=='split':
        edge('A','C',p['l'],True)
        if level=='hard':arc('A','B','D',p['beta']+p['gamma'],.25,.31,'#7a4f0b')
        if p['known']=='beta' or solution or level!='hard':arc('A','B','C',p['beta'])
        if p['known']=='gamma' or solution or level!='hard':arc('A','C','D',p['gamma'])
    else:
        arc('A','B','D',p['theta'])
        if p['family']=='general':
            edge('B','C',p['c']);edge('C','D',p['d']);arc('C','B','D',p['phi'])
    ax.set_aspect('equal');ax.axis('off')
    ax.set_xlim(min(x for x,y in xy)-.13*span,max(x for x,y in xy)+.13*span)
    ax.set_ylim(min(y for x,y in xy)-.12*span,max(y for x,y in xy)+.12*span)
    fig.tight_layout(pad=.2)
    filename=digest(dict(p=p,support=level if not solution else 'solution',version=VERSION))+'.png'
    path=output/filename
    fig.savefig(path,facecolor='white',metadata={'Software':VERSION});plt.close(fig)
    return str(path)

def aligned(rows):return '$$\n'+r'\begin{aligned}'+'\n'+('\\\\\n'.join(rows))+'\n'+r'\end{aligned}'+'\n$$'

def assemble(p,level,typ,values,output,rng,render=True):
    d=derivation(p);n=lambda s:named(s,p);diag=n('AC' if p['family']=='split' else 'BD')
    promptimg=draw(p,level,False,output) if render else str(output/(digest(p)+'-prompt.png'))
    solimg=draw(p,level,True,output) if render else str(output/(digest(p)+'-solution.png'))
    shape='parallelogram' if p['family']=='para' else 'convex quadrilateral'
    prompt=f'Find the area of {shape} $ABCD$, rounded to the **nearest tenth**. All lengths are in units.\n\n'+measurements(p,level)+'.\n\n'+f'![]({promptimg})'
    if level=='easy':
        if p['family']=='para':support=rf'The dashed diagonal ${diag}$ forms two congruent triangles. Find the area of $\triangle {n("ABD")}$ and double it.'
        else:support=rf'The dashed diagonal ${diag}$ divides the quadrilateral into $\triangle {n("ABD")}$ and $\triangle {n("BCD")}$. Calculate each triangle area and add.'
        prompt+='\n\n'+support+rf' Use $A=\frac12 ab\sin C$, where $C$ is the included angle.'
    if typ=='blank':prompt+='\n\nArea: {{field-1}} square units. Enter the rounded number using digits and a decimal point.'
    prompt+='\n\nA scientific calculator in degree mode may be used.'
    solution=rf'Diagonal ${diag}$ '+('divides the parallelogram into two congruent triangles.' if p['family']=='para' else 'divides the quadrilateral into two nonoverlapping triangles.')+'\n\n'+f'![]({solimg})'
    if p['family']=='split' and level=='hard':
        unknown='gamma' if p['known']=='beta' else 'beta';ang=n('CAD' if unknown=='gamma' else 'BAC')
        solution+='\n\nThe diagonal splits the full angle, so the other included angle is\n\n'+aligned([rf'\angle {ang}&={p["beta"]+p["gamma"]}^\circ-{p[p["known"]]}^\circ={p[unknown]}^\circ.'])
    for term in d['terms']:
        tri=n(term['triangle']);a,b=term['sides'];t=term['angle']
        solution+=rf'\n\nIn $\triangle {tri}$, the sides of lengths ${num(a)}$ and ${num(b)}$ enclose the ${num(t)}^\circ$ angle. Applying the triangle area formula gives\n\n'.replace('\\n','\n')
        solution+=aligned([rf'A_{{{tri}}}&=\frac12({num(a)})({num(b)})\sin {num(t)}^\circ',rf'&={num(term["coefficient"])}\sin {num(t)}^\circ',rf'&\approx {term["value"]:.4f}.'])
    terms=d['terms'];total=d['total']
    if d['combine']=='double':
        rows=[rf'A_{{ABCD}}&=2A_{{{n(terms[0]["triangle"])}}}',rf'&=2\left({num(terms[0]["coefficient"])}\sin {num(terms[0]["angle"])}^\circ\right)',rf'&\approx {total:.4f}.']
        transition='Double the triangle area, retaining full calculator precision:'
    else:
        rows=[rf'A_{{ABCD}}&=A_{{{n(terms[0]["triangle"])}}}+A_{{{n(terms[1]["triangle"])}}}',r'&='+ '+'.join(rf'{num(t["coefficient"])}\sin {num(t["angle"])}^\circ' for t in terms),rf'&\approx {total:.4f}.']
        transition='Add the two areas, retaining full calculator precision:'
    solution+='\n\n'+transition+'\n\n'+aligned(rows)+rf'\n\nRound only the final total: $\boxed{{{rounded(total)}}}$ square units.'.replace('\\n','\n')
    prompt=normalize_prose(prompt);solution=normalize_prose(solution)
    # Location-independent identities after prose normalization; no UUID-only variety.
    identity=digest(dict(version=VERSION,problem=re.sub(r'!\[\]\([^)]*\)',lambda m:'![]('+Path(m[0][4:-1]).name+')',prompt),solution=re.sub(r'!\[\]\([^)]*\)',lambda m:'![]('+Path(m[0][4:-1]).name+')',solution),values=sorted(values),type=typ,level=level))
    qid=str(uuid.uuid5(NS,identity));fid=str(uuid.uuid5(uuid.UUID(qid),'area'))
    choices=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),v)),':answer/type':':answer.type/math',':answer/value':v} for v in values]
    correct=choices[0][':answer/id'];rng.shuffle(choices)
    q={':question/id':qid,':question/problem':prompt,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+level,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'field-1' if typ=='blank' else 'selection',':answer-field/type':':answer-field.type/'+typ,':answer-field/choices':choices,':answer-field/correct':[':answer/id',correct]}]}
    rec={'knowledge_point':KP.copy(),'question':q,'generation':dict(version=VERSION,parameters=p,derivation=d,identity=identity,authored=True)}
    validate_generated_record(rec);return rec

def generate_batch(level,count,seed,output,render=True):
    if level=='unclassified':level='moderate'
    if level not in BANDS or count<0:raise ValueError('invalid difficulty/count')
    rng=random.Random(seed);output=Path(output).resolve();output.mkdir(parents=True,exist_ok=True)
    records=[];seen=set()
    plan=[('split','blank')] if level=='hard' else ([('para','blank'),('general','blank')] if level=='easy' else [('para','radio'),('general','radio'),('para','blank'),('general','blank'),('split','blank')])
    rng.shuffle(plan)
    for i in range(count):
        family,typ=plan[i%len(plan)]
        profile=rng.choice(PROFILES[family]) if typ=='radio' else None
        for attempt in range(3000):
            try:
                p=sample_instance(level,rng,family);d=derivation(p)
                signature=digest({k:v for k,v in p.items() if k!='rotation'})
                if signature in seen:continue
                vals=bank(p,profile) if profile else [rounded(d['total'])]
                rec=assemble(p,level,typ,vals,output,rng,render=render)
                rec['generation'].update(seed=seed,batch_index=i,profile=list(profile) if profile else 'numeric-entry')
                records.append(rec);seen.add(signature);break
            except ValueError:continue
        else:raise RuntimeError('No valid instance for complete profile '+str(profile))
    return records

def replay_source():
    """Evidence-only replay at captured parameters, never sampled into practice."""
    return json.loads((HERE/'source-replay.json').read_text())

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--difficulty',choices=(*BANDS,'unclassified'),default='moderate');ap.add_argument('--count',type=int,default=5);ap.add_argument('--seed',type=int,default=0);ap.add_argument('--format',choices=['json'],default='json')
    args=ap.parse_args()
    out=os.environ.get('COURSE_ACADEMY_GENERATOR_OUTPUT_DIR')
    if not out:ap.error('Set COURSE_ACADEMY_GENERATOR_OUTPUT_DIR to an explicit generated-asset directory')
    print(json.dumps(generate_batch(args.difficulty,args.count,args.seed,Path(out)),indent=2))
if __name__=='__main__':main()
