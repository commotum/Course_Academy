#!/usr/bin/env python3
"""Seeded, relocatable triangle-area practice. No database or runtime repo reads."""
import sys
sys.dont_write_bytecode = True
import argparse
import copy
from decimal import Decimal, ROUND_HALF_UP
import hashlib
import json
import math
import os
from pathlib import Path
import random
import tempfile
import uuid
from math_format import normalize_prose, normalize_tex, validate_generated_record
os.environ.setdefault('MPLCONFIGDIR', str(Path(tempfile.gettempdir())/'triangle-area-mpl'))
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from matplotlib.patches import Polygon, Wedge

VERSION='triangle-area-4'
KP={'db_id':17592186105903,'id':'acc86fb6-2ef4-5f8f-b204-6e1fdbbf0530','title':'Calculating the Area of a Triangle'}
PROFILES=('differential_factor','side_pair','function_input')

def stable(x): return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False)
def digest(x): return hashlib.sha256(stable(x).encode()).hexdigest()
def uid(x): return str(uuid.uuid5(uuid.NAMESPACE_URL, VERSION+':'+stable(x)))
def rounded(x,digits=2):
    # School rounding of positive areas: an exact halfway value rounds upward.
    value=Decimal(str(x)).quantize(Decimal(1).scaleb(-digits), rounding=ROUND_HALF_UP)
    return f'{value:.{digits}f}'
def angle_tex(n): return str(n)+r'^{\circ}'
def aligned(rows): return '$$\n'+r'\begin{aligned}'+'\n'+('\\\\\n'.join(rows))+'\n'+r'\end{aligned}'+'\n$$'

def make_instance(level,rng):
    kind=rng.choice(['radio','blank']) if level=='easy' else 'blank'
    profile=rng.choice(PROFILES) if kind=='radio' else 'blank'
    vertex=rng.choice('ABC'); others=[s for s in 'ABC' if s!=vertex]
    rng.shuffle(others)
    region=rng.choice(['acute','right','obtuse'])
    theta=rng.randint(40,85) if region=='acute' else (90 if region=='right' else rng.randint(95,135))
    first=rng.randint(18,theta-18) if level!='easy' else None
    assignment=rng.randrange(2)
    if level=='hard':
        x=rng.randint(3,7); k=rng.randint(1,4); m=rng.choice([2,3])
        sides=[m*x,x+k]
        if assignment: sides.reverse()
        u,v=sides
    else:
        u,v=rng.randint(4,18),rng.randint(4,18); x=k=m=None
    if max(u,v)/min(u,v)>2.4: raise ValueError('Diagram aspect ratio')
    return dict(level=level,kind=kind,profile=profile,vertex=vertex,base=others[0],upper=others[1],
                u=u,v=v,theta=theta,first=first,x=x,k=k,m=m,assignment=assignment,
                digits=rng.choice([0,1,2]) if level=='easy' and kind=='blank' else 2)

def bank(p):
    u,v,t=p['u'],p['v'],math.radians(p['theta']); a=.5*u*v*math.sin(t)
    if p['kind']=='blank': return [rounded(a,p['digits'])],rounded(a,p['digits']),['area']
    profile=p['profile']
    if profile=='differential_factor':
        recipes=['area','omit_half','cosine','omit_half_cosine','double_angle']
        vals=[a,2*a,.5*u*v*abs(math.cos(t)),u*v*abs(math.cos(t)),.5*u*v*abs(math.sin(2*t))]
    elif profile=='side_pair':
        recipes=['area','repeat_first_side','repeat_second_side','half_angle','double_angle']
        vals=[a,.5*u*u*math.sin(t),.5*v*v*math.sin(t),.5*u*v*math.sin(t/2),.5*u*v*abs(math.sin(2*t))]
    else:
        recipes=['area','sine_squared','cosine','half_angle','double_angle']
        vals=[a,a*math.sin(t),.5*u*v*abs(math.cos(t)),.5*u*v*math.sin(t/2),.5*u*v*abs(math.sin(2*t))]
    values=[rounded(n) for n in vals]
    if min(map(float,values))<=0 or any(abs(float(a)-float(b))<.12-1e-9 for i,a in enumerate(values) for b in values[i+1:]):
        raise ValueError('Indistinct or insufficiently separated complete bank')
    return values,values[0],recipes

def side_expressions(p):
    if p['level']!='hard': return [str(p['u']),str(p['v'])]
    result=[str(p['m'])+'x','x+'+str(p['k'])]
    return result[::-1] if p['assignment'] else result

def diagram(p,out):
    """Coordinates use the SAME instance; E is the ray/opposite-edge intersection."""
    name='triangle-'+digest(p)[:24]+'.png'; path=out/name
    if path.exists(): return name
    u,v,theta=p['u'],p['v'],p['theta']; angle=math.radians(theta)
    # Normalize lengths only for drawing; actual ratio and included angle are preserved.
    scale=10/max(u,v); U,V=u*scale,v*scale
    tip=(V*math.cos(angle),V*math.sin(angle)); points=[(0,0),(U,0),tip]
    fig,ax=plt.subplots(figsize=(6.4,4.2),dpi=120); ax.set_aspect('equal'); ax.axis('off')
    ax.add_patch(Polygon(points,closed=True,facecolor='#edf5fb',edgecolor='#202830',lw=1.8))
    radius=min(U,V)*.22
    if p['first'] is not None:
        f=math.radians(p['first']); direction=(math.cos(f),math.sin(f))
        delta=(tip[0]-U,tip[1]); cross=lambda a,b:a[0]*b[1]-a[1]*b[0]
        distance=cross((U,0),delta)/cross(direction,delta)
        endpoint=(distance*direction[0],distance*direction[1])
        ax.plot([0,endpoint[0]],[0,endpoint[1]],color='#28737b',lw=1.3)
        ax.text(endpoint[0]+.26,endpoint[1]+.24,'$E$',fontsize=13,ha='center')
        parts=[(0,p['first']),(p['first'],theta)]
    else: parts=[(0,theta)]
    for i,(first,last) in enumerate(parts):
        ax.add_patch(Wedge((0,0),radius,first,last,facecolor=['#b8dfe1','#f6e0a3'][i],edgecolor='#28737b',lw=.8))
        mid=math.radians((first+last)/2)
        ax.text(1.8*radius*math.cos(mid),1.8*radius*math.sin(mid),'$'+angle_tex(last-first)+'$',ha='center',va='center',fontsize=12)
    ax.text(-.32,-.55,'$'+p['vertex']+'$',fontsize=14,ha='center')
    ax.text(U+.4,-.32,'$'+p['base']+'$',fontsize=14,ha='center')
    ax.text(tip[0],tip[1]+.5,'$'+p['upper']+'$',fontsize=14,ha='center')
    side1,side2=side_expressions(p)
    ax.text(U/2,-.72,'$'+side1+'$',fontsize=13,ha='center')
    ax.text(tip[0]/2-1.05*math.sin(angle),tip[1]/2+1.05*math.cos(angle),'$'+side2+'$',fontsize=13,ha='center')
    ax.set_xlim(min(0,tip[0])-2,max(U,tip[0])+1.4); ax.set_ylim(-1.5,tip[1]+1.4)
    fig.savefig(path,bbox_inches='tight',pad_inches=.12,facecolor='white',metadata={'Software':VERSION}); plt.close(fig)
    return name

def construct(p,out,rng=None,render=True):
    rng=rng or random.Random(0); values,key,recipes=bank(p)
    o,b,c=p['vertex'],p['base'],p['upper']; side1,side2=side_expressions(p)
    e1,e2=o+b,o+c; angle=b+o+c; u,v,theta=p['u'],p['v'],p['theta']
    name=diagram(p,out) if render else 'triangle-'+digest(p)[:24]+'.png'
    intro=f'In $\\triangle ABC$, ${e1}={side1}$ and ${e2}={side2}$.'
    if p['level']=='hard': intro+=f' Also, ${e1}+{e2}={u+v}$. All lengths use the same unit.'
    if p['first'] is None: intro+=f' The included angle is $\\angle {angle}={angle_tex(theta)}$.'
    else: intro+=f' Point $E$ lies on ${b+c}$. The marked angles are $\\angle {b+o}E={angle_tex(p["first"])}$ and $\\angle E{o+c}={angle_tex(theta-p["first"])}$.'
    precision={0:'nearest integer',1:'nearest tenth',2:'two decimal places'}[p['digits']]
    if p['kind']=='blank': request=f'Rounded to **{precision}**, the area of $\\triangle ABC$ is {{{{field-1}}}} square units.'
    else: request='Find the area of $\\triangle ABC$, in square units. Round your answer to **two decimal places**.'
    prompt=f'![]({name})\n\n{intro}\n\n{request}\n\n> Use a scientific calculator in degree mode.'
    steps=[]
    if p['level']=='hard':
        x,k,m=p['x'],p['k'],p['m']
        steps+=['First use the sum to recover the side lengths.',aligned([
            f'({side1})+({side2})&={u+v}',f'{m+1}x+{k}&={u+v}',f'x&={x}']),
            f'Thus ${e1}={side1}={u}$ and ${e2}={side2}={v}$.']
    if p['first'] is not None:
        steps+=['The two marked parts together form the angle between the two whole sides.',
            '$$\n'+f'\\angle {angle}={angle_tex(p["first"])}+{angle_tex(theta-p["first"])}={angle_tex(theta)}.'+'\n$$']
    else: steps+=[f'The sides ${e1}={u}$ and ${e2}={v}$ meet at ${o}$, so ${angle_tex(theta)}$ is their included angle.']
    area=.5*u*v*math.sin(math.radians(theta))
    steps+=['Apply the triangle area formula to those two sides and their included angle.',aligned([
        f'\\mathcal A&=\\frac12({e1})({e2})\\sin(\\angle {angle})',
        f'&=\\frac12({u})({v})\\sin {angle_tex(theta)}',
        f'&={u*v/2:g}\\sin {angle_tex(theta)}',f'&\\approx {area:.8f}',f'&\\approx {key}.']),
        f'The area is ${key}$ square units. Keep full calculator precision until the final rounding.']
    prompt=normalize_prose(prompt); solution=normalize_prose('\n\n'.join(steps)); values=[normalize_tex(s) for s in values]
    content=dict(prompt=prompt,solution=solution,values=sorted(values),kind=p['kind'],level=p['level'])
    identity=digest(content); fieldid=uid([identity,'field'])
    answers=[{':answer/id':uid([fieldid,a]),':answer/type':':answer.type/math',':answer/value':a} for a in values]; rng.shuffle(answers)
    field={':answer-field/id':fieldid,':answer-field/key':'field-1' if p['kind']=='blank' else 'selection',
           ':answer-field/type':':answer-field.type/'+p['kind'],':answer-field/choices':answers,
           ':answer-field/correct':[':answer/id',uid([fieldid,key])]}
    record={'knowledge_point':KP.copy(),'question':{':question/id':uid(identity),':question/problem':prompt,':question/worked-solution':solution,
            ':question/difficulty':':question.difficulty/'+p['level'],':question/requires-calculator':True,':question/answer-fields':[field]},
            'generation':{'version':VERSION,'parameters':p.copy(),'profile':p['profile'],'recipes':recipes,
             'source_ids':['523e58fd-720f-5d57-874d-652c697b8c8b' if p['level']=='easy' else '62053f65-aa41-51ba-ae55-9daf395476d3' if p['level']=='moderate' else '9f6e2d93-8e5c-5502-80c2-43af157cdfdc'],
             'semantic_fingerprint':digest({k:p[k] for k in ['level','u','v','theta','first','x','k','m','digits']})}}
    return validate_generated_record(record)

def generate_batch(level,count,seed,out):
    if count<1: raise ValueError('Count must be positive')
    out=Path(out);out.mkdir(parents=True,exist_ok=True); rng=random.Random(seed); records=[]; seen=set()
    for _ in range(count):
        for attempt in range(1000):
            try:
                p=make_instance(level,rng); bank(p)
                semantic=digest({k:p[k] for k in ['level','u','v','theta','first','x','k','m','digits']})
                if semantic in seen:continue
                rec=construct(p,out,rng);rec['generation']['seed']=seed
                records.append(rec);seen.add(semantic); break
            except ValueError: continue
        else: raise RuntimeError('Could not construct a complete distinct bank')
    return records

def replay(source_id):
    data=json.loads(Path(__file__).with_name('source-replay.json').read_text())
    return copy.deepcopy(next(r for r in data if r['generation']['source_id']==source_id))

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty',choices=['easy','moderate','hard','unclassified','all'],default='easy')
    parser.add_argument('--count',type=int,default=1);parser.add_argument('--seed',type=int,default=0)
    parser.add_argument('--format',choices=['json'],default='json');parser.add_argument('--source-id')
    args=parser.parse_args()
    if args.source_id: records=[replay(args.source_id)]
    else:
        output=os.environ.get('COURSE_ACADEMY_GENERATOR_OUTPUT_DIR')
        if not output: parser.error('Set COURSE_ACADEMY_GENERATOR_OUTPUT_DIR to an asset output directory')
        levels=['easy','moderate','hard'] if args.difficulty=='all' else ['easy' if args.difficulty=='unclassified' else args.difficulty]
        records=[r for level in levels for r in generate_batch(level,args.count,args.seed,output)]
    print(json.dumps(records,ensure_ascii=False,indent=2))
if __name__=='__main__': main()
