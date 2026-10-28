#!/usr/bin/env python3
"""Seeded piecewise unity line integrals; all assets belong to the output directory."""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import json
import math
import os
import random
import tempfile
import uuid
from pathlib import Path
import sympy as s
from math_format import normalize_prose, normalize_tex, validate_generated_record

KP=17592186162082
KPID='e60b3dd1-0842-562d-a72f-5adb6a60cba8'
VERSION='piecewise-unity-5'
FAMILIES={'easy':['semi','three_quarter'], 'moderate':['quarter_open','quarter_closed','three_segments','two_segments'], 'hard':['arc_slants']}
SOURCE_IDS={'semi':'ef2f2e1e-2df6-5eea-a523-f7500a9f7301','three_quarter':'f87f9aea-995d-5fa2-9903-84aef89b9be9','three_segments':'23524215-604c-5fbd-8acf-4af9e94c29ca','two_segments':'efd8621e-7cbb-5240-b849-bfa0535c815e','quarter_open':'65d60feb-29ba-53eb-9de0-464deb1c4c60','quarter_closed':'f166d21e-a0b0-5de8-91b5-84f57909990e','arc_slants':'48add826-1240-58c0-af1f-b2af8adce870'}

def tex(x):
    return normalize_tex(s.latex(s.sympify(x)).replace('\\left','').replace('\\right',''))

def uid(value):
    return str(uuid.uuid5(uuid.NAMESPACE_URL,VERSION+'/'+value))

def display(value):
    return '\n\n$$\n'+value+'\n$$'

def geometry(t,p):
    r=p.get('r')
    if t=='semi': return {'center':[0,1], 'arc':[r,0,s.pi], 'points':[[-r,1],[r,1]]}
    if t=='three_quarter': return {'center':[0,0], 'arc':[r,0,3*s.pi/2], 'points':[[0,-r],[r,-r]]}
    if t=='quarter_closed': return {'center':[0,0], 'arc':[r,0,s.pi/2], 'points':[[0,r],[r,0]]}
    if t=='quarter_open': return {'center':[0,0], 'arc':[r,-s.pi/2,0], 'points':[[r,0],[0,r]]}
    if t=='three_segments':
        a,b=p['a'],p['b']; return {'points':[[0,0],[0,a],[b,0],[b,a]]}
    if t=='two_segments':
        return {'points':[[-p['a'],0],[0,p['h']],[p['b'],0]]}
    cx,cy=p['cx'],p['cy']
    return {'center':[cx,cy], 'arc':[r,0,s.pi], 'points':[[cx-r,cy],[p['dx'],cy-p['h']],[cx+r,cy]]}

def lengths(t,p):
    g=geometry(t,p); out=[]
    if 'arc' in g:
        r,lo,hi=g['arc'];out.append(s.simplify(r*(hi-lo)))
    pts=g['points']
    out.extend(s.sqrt(sum((s.Integer(y)-s.Integer(x))**2 for x,y in zip(a,b))) for a,b in zip(pts,pts[1:]))
    return out

PROFILES=('mixed',)
def bank(profile,t,p,L):
    """Whole misconception profiles, selected before sampling dimensions."""
    A=sum(L); first=L[0]; rest=sum(L[1:])
    if profile=='omit':
        return [(A,'correct'),(first,'only_first'),(rest,'omit_first'),(A/2,'halve_all_lengths'),(2*A,'double_traversal')]
    if profile=='scale':
        return [(A,'correct'),(A/2,'halve_all_lengths'),(2*A,'double_all_lengths'),(2*first+rest,'double_first'),(first+2*rest,'double_remaining')]
    if profile=='signed':
        return [(A,'correct'),(first-rest,'subtract_remaining'),(2*first-rest,'double_first_and_subtract_remaining'),(first+rest/2,'halve_remaining'),(first/2+2*rest,'halve_first_double_remaining')]
    if profile.startswith('q-'):
        from source_banks import bank as source_bank
        return source_bank(profile,t,{k:s.Integer(v) for k,v in p.items()},L)
    if profile=='exemplar':
        if t=='semi':return [(first,'omit_diameter'),(first+p['r'],'radius_for_diameter'),(2*first+rest,'full_circle'),(A,'correct'),(s.Integer(0),'closed_zero')]
        if t=='quarter_closed':return [(first+2*p['r'],'chord_as_two_radii'),(A,'correct'),(2*first+rest,'semicircle'),(first,'omit_chord'),(first-rest,'subtract_chord')]
        return [(s.Integer(0),'closed_zero'),(first+2*p['r'],'replace_return_by_diameter'),(2*first+rest,'diameter_as_radius'),(first+2*L[1],'assume_equal_slants'),(A,'correct')]
    raise ValueError('Unknown profile')

def mixed_bank(t,p,L,rng,rank=None):
    """Sample four identifiable errors, independently of the correct position.

    No profile signature fixes the answer's numerical rank. The requested rank
    varies within each visible geometry in a finite batch. Source-replay banks
    remain separate from production banks.
    """
    A=s.simplify(sum(L));first=L[0];rest=sum(L[1:])
    pool=[(first,'only_first'),(rest,'omit_first'),
          (A/2,'halve_all_lengths'),(2*A,'double_traversal'),
          (first-rest,'subtract_remaining'),(rest-first,'subtract_first'),
          (2*first+rest,'double_first'),(first+2*rest,'double_remaining'),
          (first/2+rest,'halve_first'),(first+rest/2,'halve_remaining'),
          (first/2+2*rest,'halve_first_double_remaining'),
          (2*first+rest/2,'double_first_halve_remaining')]
    geom=geometry(t,p);pts=geom['points'];offset=int('arc' in geom)
    for i,(a,b) in enumerate(zip(pts,pts[1:])):
        dx,dy=abs(b[0]-a[0]),abs(b[1]-a[1])
        pool.append((A-L[i+offset]+dx+dy,'segment_'+str(i+1)+'_coordinate_legs'))
        if len(pts)>2:pool.append((A-L[i+offset],'omit_segment_'+str(i+1)))
    if offset:
        for fraction in (s.Rational(1,4),s.Rational(1,2),s.Rational(3,4),s.Integer(1)):
            pool.append((fraction*2*s.pi*p['r']+rest,'wrong_arc_fraction_'+str(fraction)))
    if t=='arc_slants':
        pool.extend([(first+2*L[1],'assume_both_slants_like_left'),(first+2*L[2],'assume_both_slants_like_right')])
    unique=[]
    for value,recipe in pool:
        value=s.simplify(value)
        if s.simplify(value-A)!=0 and all(s.simplify(value-v)!=0 for v,_ in unique):unique.append((value,recipe))
    below=[v for v in unique if float(v[0]-A)<0];above=[v for v in unique if float(v[0]-A)>0]
    eligible=[n for n in range(5) if len(below)>=n and len(above)>=4-n]
    n=rank-1 if rank is not None else rng.choice(eligible)
    if n not in eligible:raise ValueError('Insufficient plausible distinct errors for requested rank')
    for attempt in range(500):
        proposed=[(A,'correct')]+rng.sample(below,n)+rng.sample(above,4-n)
        expanded=[s.expand(v) for v,_ in proposed]
        supports=[set(term.as_coeff_Mul()[1] for term in s.Add.make_args(v) if term!=0) for v in expanded]
        sizes=[len(row) for row in supports]
        # No unique formatting of the key or recognizable three-full/two-
        # omitted-component median signature. Original banks are replay only.
        if sizes.count(sizes[0])==1 or (max(sizes)>1 and sizes.count(max(sizes))==3):continue
        bases=sorted(set.union(*supports),key=str)
        coefficients=[[v.coeff(b) if b!=1 else v.as_coeff_Add()[0] for b in bases] for v in expanded]
        modes=[]
        for col in zip(*coefficients):
            counts=Counter(col);maximum=max(counts.values())
            modes.append({v for v,c in counts.items() if c==maximum})
        if sum(all(v in mode for v,mode in zip(row,modes)) for row in coefficients)==1:continue
        # A lone positive/negative counterpart is also a visible bank marker.
        counterparts=[i for i,v in enumerate(expanded) if float(v)>0 and any(s.expand(v+w)==0 for j,w in enumerate(expanded) if i!=j)]
        if len(counterparts)==1:continue
        return proposed
    raise ValueError('Cannot build a complete plausible bank without a unique surface marker')

def choose_parameters(level,t,rng):
    if t in ('semi','three_quarter','quarter_open','quarter_closed'):return {'r':rng.randint(1,9)}
    if t=='three_segments':
        a,b=rng.choice([(3,4),(4,3),(5,12),(12,5),(6,8),(8,6)])
        return {'a':a,'b':b}
    if t=='two_segments':
        a,h=rng.choice([(3,4),(4,3),(6,8),(8,6)]);b=rng.randint(1,6)
        return {'a':a,'b':b,'h':h}
    r=rng.randint(2,5);cx=rng.randint(-3,3);cy=rng.choice([-2,-1,1,2,3])
    return {'r':r,'cx':cx,'cy':cy,'dx':cx+rng.randint(-r+1,r-1),'h':rng.randint(2,5)}

def validate_parameters(t,p):
    keys={'r'} if t in ('semi','three_quarter','quarter_open','quarter_closed') else {'a','b'} if t=='three_segments' else {'a','b','h'} if t=='two_segments' else {'r','cx','cy','dx','h'}
    if set(p)!=keys or any(not isinstance(v,int) for v in p.values()):raise ValueError('Unexpected integer slots')
    if any(p[k]<=0 for k in keys & {'r','a','b','h'}):raise ValueError('Positive dimensions required')
    if t=='arc_slants' and not p['cx']-p['r']<p['dx']<p['cx']+p['r']:raise ValueError('Return vertex must lie between diameter endpoints horizontally')

def plot(t,p,output_dir,reverse=False):
    # Same instance drives prompt and solution. No package-relative output or cache.
    dest=Path(output_dir).resolve();dest.mkdir(parents=True,exist_ok=True)
    os.environ.setdefault('MPLCONFIGDIR',str(Path(tempfile.gettempdir())/'course-academy-mpl'))
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    g=geometry(t,p)
    digest=hashlib.sha256(json.dumps([VERSION,t,p,reverse],sort_keys=True).encode()).hexdigest()[:24]
    files={role:dest/(digest+'-'+role+'.png') for role in ('prompt','solution')}
    if all(f.exists() for f in files.values()):return {k:str(v) for k,v in files.items()}
    curves=[]
    if 'arc' in g:
        r,lo,hi=map(float,g['arc']);cx,cy=g['center']
        curves.append([(cx+r*math.cos(lo+(hi-lo)*i/180),cy+r*math.sin(lo+(hi-lo)*i/180)) for i in range(181)])
    curves.extend([a,b] for a,b in zip(g['points'],g['points'][1:]))
    allpts=[v for c in curves for v in c];xs=[v[0] for v in allpts];ys=[v[1] for v in allpts]
    xmin,xmax=min(0,min(xs)),max(0,max(xs));ymin,ymax=min(0,min(ys)),max(0,max(ys))
    span=max(xmax-xmin,ymax-ymin);pad=.24*span;blue='#2168aa'
    for role,path in files.items():
        fig,ax=plt.subplots(figsize=(5.7,4.6),dpi=120)
        fig.subplots_adjust(left=.03,right=.97,bottom=.03,top=.97)
        ax.set_aspect('equal');ax.axis('off')
        ax.set_xlim(xmin-pad,xmax+pad);ax.set_ylim(ymin-pad,ymax+pad)
        ax.annotate('',(xmax+.8*pad,0),(xmin-pad,0),arrowprops={'arrowstyle':'->','lw':.8,'color':'#666'})
        ax.annotate('',(0,ymax+.8*pad),(0,ymin-pad),arrowprops={'arrowstyle':'->','lw':.8,'color':'#666'})
        ax.text(xmax+.75*pad,-.055*span,'$x$',fontsize=10);ax.text(.025*span,ymax+.7*pad,'$y$',fontsize=10)
        for i,c in enumerate(curves):
            ax.plot([v[0] for v in c],[v[1] for v in c],lw=1.9,color=blue)
            if len(c)>2:
                j=70;aa,bb=c[j-4],c[j+4];mid=c[110];off=(.025*span,.065*span)
            else:
                aa=tuple(.54*x+.46*y for x,y in zip(c[0],c[1]));bb=tuple(.46*x+.54*y for x,y in zip(c[0],c[1]));mid=tuple((x+y)/2 for x,y in zip(c[0],c[1]));off=(.035*span,-.08*span if t in ('semi','quarter_closed') else .04*span)
            if reverse:aa,bb=bb,aa
            ax.annotate('',bb,aa,arrowprops={'arrowstyle':'->','color':blue,'lw':1.7,'mutation_scale':12})
            if role=='solution':ax.text(mid[0]+off[0],mid[1]+off[1],'$C_'+str(i+1)+'$',fontsize=11,color=blue,bbox={'facecolor':'white','edgecolor':'none','alpha':.85,'pad':1})
        # Coordinates at vertices are authoritative, not inferred from axis ticks.
        pts=g['points'];names=['A','D','B'] if t=='arc_slants' else list('ABDE')[:len(pts)]
        for i,((x,y),name) in enumerate(zip(pts,names)):
            if t=='arc_slants': offset=(-.015*span,.065*span) if i!=1 else (.025*span,-.1*span);ha='right' if i==0 else 'left'
            else:offset=(-.035*span,.06*span) if i%2==0 else (.035*span,-.1*span);ha='right' if i%2==0 else 'left'
            ax.scatter([x],[y],s=14,color=blue,zorder=4)
            ax.text(x+offset[0],y+offset[1],f'${name}({x},{y})$',fontsize=9,ha=ha)
        if t=='arc_slants' and role=='solution':
            cx,cy=g['center'];r=p['r'];ax.plot([cx-r,cx+r],[cy,cy],ls='--',color='#999',lw=1)
            ax.scatter([cx],[cy],s=12,color='#999');ax.text(cx+.03*span,cy+.035*span,'$r='+str(r)+'$',fontsize=10,color='#666')
        fig.savefig(path,facecolor='white',metadata={'Software':VERSION});plt.close(fig)
    return {k:str(v) for k,v in files.items()}

def prose(t,p,assets,L,reverse=False):
    g=geometry(t,p);r=p.get('r');names=['A','D','B'] if t=='arc_slants' else list('ABDE')[:len(g['points'])]
    coords=', '.join('$'+name+str(tuple(pt)).replace(' ','')+'$' for name,pt in zip(names,g['points']))
    intro='Calculate'+display(r'\int_C\,\mathrm{d}s,')+'\n\n'
    direction='opposite to the arrows' if reverse else 'in the direction of the arrows'
    # Plot arrows themselves reverse, so the prompt always refers to shown arrows.
    direction='in the direction of the arrows'
    if t=='arc_slants':
        description='where $C$ is the closed path shown, traversed once '+direction+'. The curved part joining $A$ and $B$ is a semicircle with diameter $AB$; the other two parts are straight segments. The labeled points are '+coords+'.'
    elif r:
        shapes={'semi':'semicircular arc and then its diameter','three_quarter':'three-quarter-circle arc and then the horizontal segment','quarter_closed':'quarter-circle arc and then the straight chord joining its endpoints','quarter_open':'quarter-circle arc and then the straight segment'}
        description='where $C$ follows the '+shapes[t]+', once '+direction+'. The circular arc has radius $'+tex(r)+'$ and center $'+str(tuple(g['center'])).replace(' ','')+'$. The straight part joins '+coords+'.'
    else:description='where $C$ follows the straight segments between the consecutive labeled points '+coords+', once '+direction+'.'
    problem='![]('+assets['prompt']+')\n\n'+intro+description
    n=len(L)
    solution='The **line integral of unity** is the total path length. Split the path into its '+str(n)+' pieces:\n\n![]('+assets['solution']+')'
    solution+=display(r'\int_C\,\mathrm{d}s='+ '+'.join('L_'+str(i+1) for i in range(n))+'.')
    rows=[];offset=0
    if r:
        fraction={'semi':r'\frac12','three_quarter':r'\frac34','quarter_closed':r'\frac14','quarter_open':r'\frac14','arc_slants':r'\frac12'}[t]
        if t=='arc_slants':
            left,right=g['points'][0],g['points'][-1]
            solution+='\n\nThe horizontal diameter runs from $A'+str(tuple(left)).replace(' ','')+'$ to $B'+str(tuple(right)).replace(' ','')+'$. Hence'
            solution+=display('r=\\frac{'+tex(right[0])+'-('+tex(left[0])+')}{2}='+tex(r)+'.')
        solution+='\n\nThe circular piece contributes'
        solution+=display('L_1='+fraction+r'(2\pi\cdot '+tex(r)+')='+tex(L[0])+'.')
        offset=1
    solution+='\n\nUse the distance formula for the straight pieces:'
    for j,(a,b) in enumerate(zip(g['points'],g['points'][1:])):
        idx=j+offset
        rows.append('L_'+str(idx+1)+r'&=\sqrt{('+tex(b[0])+'-('+tex(a[0])+'))^2+('+tex(b[1])+'-('+tex(a[1])+'))^2}='+tex(L[idx]))
    solution+=display(r'\begin{aligned}'+'\n'+',\\\\\n'.join(rows)+'.\n'+r'\end{aligned}')
    value=tex(s.simplify(sum(L)))
    solution+='\n\nAdd every traversed length positively:'+display(r'\int_C\,\mathrm{d}s='+'+'.join(tex(x) for x in L)+'='+value+'.')
    if t=='arc_slants':solution+='\n\nThe dashed diameter is a construction aid, not part of $C$.'
    return normalize_prose(problem),normalize_prose(solution)

def generate(level,seed=0,template=None,parameters=None,profile=None,output_dir=None,reverse=False,asset_override=None,answer_rank=None):
    if level not in FAMILIES:raise ValueError('Unknown difficulty')
    rng=random.Random(seed);t=template or rng.choice(FAMILIES[level]);selected=profile or rng.choice(PROFILES)
    if t not in FAMILIES[level]:raise ValueError('Family outside difficulty')
    for attempt in range(100):
        p=dict(parameters) if parameters is not None else choose_parameters(level,t,rng)
        validate_parameters(t,p);L=lengths(t,p);A=s.simplify(sum(L));B=mixed_bank(t,p,L,rng,answer_rank) if selected=='mixed' else bank(selected,t,p,L)
        if all(s.simplify(x-y)!=0 for j,(x,_) in enumerate(B) for y,_ in B[j+1:]):break
        if parameters is not None:raise ValueError('Ambiguous complete bank')
    else:raise ValueError('No distinct complete bank')
    if output_dir is None:output_dir=os.environ.get('COURSE_ACADEMY_GENERATOR_OUTPUT_DIR')
    if not output_dir and asset_override is None:raise ValueError('Set COURSE_ACADEMY_GENERATOR_OUTPUT_DIR for generated assets')
    assets=asset_override or plot(t,p,output_dir,reverse)
    prompt,solution=prose(t,p,assets,L,reverse)
    values=[tex(x) for x,_ in B]
    # Identities do not depend on machine-specific output directory or option order.
    stable_prompt=prompt;stable_solution=solution
    for role,path in assets.items():
        stable_prompt=stable_prompt.replace(path,Path(path).name);stable_solution=stable_solution.replace(path,Path(path).name)
    identity=json.dumps([VERSION,level,stable_prompt,stable_solution,sorted(values)],sort_keys=True)
    qid=uid(identity);fid=uid(qid+'/selection')
    choices=[{':answer/id':uid(fid+'/'+v),':answer/type':':answer.type/math',':answer/value':v} for v in values]
    correct=next(a[':answer/id'] for a,(x,_) in zip(choices,B) if s.simplify(x-A)==0)
    rng.shuffle(choices)
    record={'knowledge_point':{'db_id':KP,'id':KPID,'title':'Calculating Line Integrals Over Piecewise-Smooth Curves'},'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',correct]}]},'generation':{'version':VERSION,'seed':seed,'template':t,'profile':selected,'parameters':p,'source_refs':[SOURCE_IDS[t]],'lengths':[str(v) for v in L],'displayed_final':tex(A),'answer':str(A),'recipes':{tex(x):recipe for x,recipe in B},'assets':assets,'reversed':reverse}}
    return validate_generated_record(record)

def batch(level,count,seed):
    if count<0:raise ValueError('count must be nonnegative')
    rng=random.Random(seed);out=[];seen=set();families=[]
    last_rank={};last_position={}
    # Vary rank within repeated visible families. Select from independently
    # derived errors; never perturb an answer numerically to fill a bank.
    for _ in range(count):
        for attempt in range(100):
            if not families:families=rng.sample(FAMILIES[level],len(FAMILIES[level]))
            t=families.pop()
            rank=rng.choice([i for i in range(1,6) if i!=last_rank.get(t)])
            rec=generate(level,rng.getrandbits(64),template=t,profile='mixed',answer_rank=rank)
            # Reflection or reordering of the same lengths is the same arithmetic
            # instance, even when the diagram and coordinate labels differ.
            semantic=json.dumps([t,sorted(rec['generation']['lengths'])],sort_keys=True)
            if semantic not in seen:break
        else:raise ValueError('Requested batch exceeds sampled semantic capacity')
        last_rank[t]=rank
        field=rec['question'][':question/answer-fields'][0]
        choices=field[':answer-field/choices'];correct=field[':answer-field/correct'][1]
        position=rng.choice([i for i in range(5) if i!=last_position.get(t)])
        key=next(a for a in choices if a[':answer/id']==correct)
        choices.remove(key);choices.insert(position,key);last_position[t]=position
        seen.add(semantic);out.append(rec)
    return out

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--difficulty',choices=['easy','moderate','hard','unclassified','all'],default='easy')
    parser.add_argument('--count',type=int,default=1);parser.add_argument('--seed',type=int,default=0);parser.add_argument('--format',choices=['json'],default='json')
    a=parser.parse_args();levels=list(FAMILIES) if a.difficulty=='all' else [('easy' if a.difficulty=='unclassified' else a.difficulty)]
    print(json.dumps([r for level in levels for r in batch(level,a.count,a.seed)],indent=2))
