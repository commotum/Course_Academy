#!/usr/bin/env python3
"""Seeded, relocatable geometric line-integral generator. No database writes."""
from __future__ import annotations
import argparse, copy, hashlib, json, math, os, random, sys, tempfile, uuid
from pathlib import Path
os.environ.setdefault('MPLCONFIGDIR',str(Path(tempfile.gettempdir())/'unity-generator-mpl'))
import sympy as sp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from math_format import normalize_prose, normalize_tex, validate_generated_record
ROOT=Path(__file__).resolve().parent
NS=uuid.UUID('b4ac9e7d-ea92-5cd3-af26-4c902196e80b')
VERSION='unity-geometry-3'
KP={'db_id':17592186162081,'id':str(NS),'title':'Calculating Line Integrals of Unity'}
BANDS=('easy','moderate','hard')
CASES={'easy':['horizontal','vertical','diagonal','radius_half','radius_full'],
       'moderate':['horizontal_half','vertical_half','horizontal_full','vertical_full'],
       'hard':['diagonal_half','diagonal_full']}

def tx(x): return normalize_tex(sp.latex(sp.simplify(x)))
def uid(s): return str(uuid.uuid5(NS,s))
def canonical(x): return json.dumps(x,sort_keys=True,separators=(',',':'))
def output_dir():
    p=os.environ.get('COURSE_ACADEMY_GENERATOR_OUTPUT_DIR')
    if not p: raise ValueError('COURSE_ACADEMY_GENERATOR_OUTPUT_DIR must name an asset directory')
    p=Path(p).resolve()
    if p==ROOT or ROOT in p.parents:
        # Workspace evidence subdirectories are fine; runtime files themselves are never overwritten.
        if p==ROOT: raise ValueError('Use a separate generated-asset directory')
    p.mkdir(parents=True,exist_ok=True);return p

def sample(level,case,rng):
    circle='_' in case
    kind=case.split('_')[0]
    extent=case.split('_')[-1] if circle else None
    x,y=rng.randint(-3,2),rng.randint(-3,2)
    if kind=='radius':
        return dict(level=level,case=case,kind='radius',extent=extent,r=rng.randint(1,9),side=rng.choice([-1,1]),direction=rng.choice([-1,1]))
    if kind=='horizontal': dx,dy=rng.randint(2,10),0
    elif kind=='vertical': dx,dy=0,rng.randint(2,10)
    else:
        # familiar integer triangles and small, simplifiable radicals
        dx,dy=rng.choice([(2,4),(3,6),(3,4),(4,3),(2,2),(3,3),(4,4),(2,3),(3,2),(1,2),(2,1)])
        if level=='easy': dx,dy=rng.choice([(a,b) for a in range(2,7) for b in range(2,7) if a!=b])
    dx*=rng.choice([-1,1]);dy*=rng.choice([-1,1])
    return dict(level=level,case=case,kind=kind,extent=extent,A=[x,y],B=[x+dx,y+dy],side=rng.choice([-1,1]),direction=rng.choice([-1,1]))

def geometry(p):
    if p['kind']=='radius':
        d=sp.Integer(2*p['r']);a=b=sp.Integer(0)
    else:
        a=sp.Integer(abs(p['B'][0]-p['A'][0]));b=sp.Integer(abs(p['B'][1]-p['A'][1]));d=sp.sqrt(a*a+b*b)
        if not d: raise ValueError('degenerate curve')
    L=d if p['extent'] is None else sp.pi*d/(2 if p['extent']=='half' else 1)
    return a,b,d,sp.expand(L)

def bank(p,profile):
    a,b,d,L=geometry(p)
    if p['extent'] is not None:
        # Missing/doubled radius and extent factors may occur on either side
        # of the correct length. Keep the same visible bank forms while varying
        # which candidate plays the correct role within those forms.
        mode,profile=divmod(profile,5)
        low,high=[(L/2,2*L),(2*L,4*L),(L/4,L/2)][mode%3]
        # All are concrete geometric mistakes; the complete profile is chosen first.
        region_area=sp.pi*d*d/(8 if p['extent']=='half' else 4)
        profiles=[[(L/2,'halve again'),(2*L,'double extent'),(d,'diameter as length'),(region_area,'enclosed region area instead of arc length')],
                  [(2*L,'double extent'),(4*L,'double twice'),(L+d,'include diameter'),(sp.pi*d*d/4,'disk area')],
                  [(L/2,'halve again'),(region_area,'enclosed region area instead of arc length'),(d/2,'radius as length'),(d,'diameter as length')],
                  [(2*L,'double extent'),(L/2,'halve again'),(sp.pi*d*d/4,'disk area'),(sp.pi*d*d,'diameter as radius in area')],
                  [(L/2,'halve again'),(2*L,'double extent'),(d,'diameter as length'),(L+d,'include diameter')]]
        profiles[0][:2]=[(low,'radius/extent factor error'),(high,'radius/extent factor error')]
        profiles[1][:2]=[[(2*L,'double extent'),(4*L,'double twice')],
                         [(L/2,'halve again'),(2*L,'double extent')],
                         [(L/4,'halve twice'),(L/2,'halve again')]][mode%3]
        profiles[2][0]=([(L/2,'halve again'),(2*L,'double extent'),(4*L,'double twice')][mode%3])
        profiles[3][:2]=[(high,'radius/extent factor error'),(low,'radius/extent factor error')]
        profiles[4][:2]=[(low,'radius/extent factor error'),(high,'radius/extent factor error')]
    elif a and b:
        profile%=5
        profiles=[[(a,'horizontal leg'),(b,'vertical leg'),(a+b,'sum of legs'),(sp.sqrt(a+b),'root of sum instead of squares')],
                  [(d/2,'halve distance'),(2*d,'double distance'),(a+b,'sum of legs'),(d*d,'squared distance')],
                  [(a/2,'half horizontal leg'),(b/2,'half vertical leg'),(sp.sqrt(a+b),'root of sum instead of squares'),(d/2,'halve distance')],
                  [(2*d,'double distance'),(d*d,'squared distance'),(2*(a+b),'double sum of legs'),(sp.sqrt(a+b),'root of sum instead of squares')],
                  [(a+b,'sum of legs'),(2*d,'double distance'),(sp.sqrt(a+b),'root of sum instead of squares'),(d*d,'squared distance')]]
    else:
        profile%=5
        axis=0 if a else 1;lo,hi=sorted([p['A'][axis],p['B'][axis]])
        profiles=[[(abs(lo),'first coordinate magnitude'),(abs(hi),'second coordinate magnitude'),(abs(lo+hi),'coordinate sum magnitude'),(d*d,'squared distance')],
                  [(d/2,'halve distance'),(2*d,'double distance'),(d*d,'squared distance'),(sp.sqrt(d),'unnecessary root')],
                  [(abs(lo),'first coordinate magnitude'),(abs(hi),'second coordinate magnitude'),(d/2,'halve distance'),(sp.sqrt(d),'unnecessary root')],
                  [(2*d,'double distance'),(d*d,'squared distance'),(abs(lo+hi),'coordinate sum magnitude'),(sp.sqrt(d),'unnecessary root')],
                  [(2*d,'double distance'),(d/2,'halve distance'),(abs(lo),'first coordinate magnitude'),(abs(hi),'second coordinate magnitude')]]
    entries=[(L,'path length')]+profiles[profile]
    vals=[sp.expand(v) for v,_ in entries]
    if any(sp.expand(v-w)==0 for i,v in enumerate(vals) for w in vals[i+1:]): raise ValueError('colliding complete bank')
    return vals,[e for _,e in entries]

def diagram(p,helper=False):
    a,b,d,L=geometry(p);circle=p['extent'] is not None
    name=hashlib.sha256(canonical({'p':{k:v for k,v in p.items() if k!='level'},'helper':helper,'style':VERSION+('-half-direction2' if p['extent']=='half' else '')}).encode()).hexdigest()+'.png'
    dest=output_dir()/name
    if dest.exists():return str(dest)
    fig,ax=plt.subplots(figsize=(5.4,4.5),dpi=115)
    blue='#246fb3';grey='#737373'
    if p['kind']=='radius':
        cx=cy=0.;r=float(d)/2;A=(-r,0);B=(r,0)
    else:
        A=tuple(p['A']);B=tuple(p['B']);cx=(A[0]+B[0])/2;cy=(A[1]+B[1])/2;r=float(d)/2
    if circle:
        if p['extent']=='full': t0=math.atan2(A[1]-cy,A[0]-cx);t1=t0+p['direction']*2*math.pi
        else:
            t0=math.atan2(B[1]-cy,B[0]-cx);t1=t0+p['side']*math.pi
            if p['direction']!=p['side']:t0,t1=t1,t0
        ts=[t0+(t1-t0)*i/240 for i in range(241)]
        xs=[cx+r*math.cos(t) for t in ts];ys=[cy+r*math.sin(t) for t in ts]
        ax.plot(xs,ys,c=blue,lw=2)
        for f in (.2,.52,.82):
            t=t0+(t1-t0)*f;u=t+(t1-t0)*.025
            ax.annotate('',xy=(cx+r*math.cos(u),cy+r*math.sin(u)),xytext=(cx+r*math.cos(t),cy+r*math.sin(t)),arrowprops={'arrowstyle':'->','color':blue,'lw':1.6})
        if p['kind']=='radius':
            t=(t0+t1)/2 if p['extent']=='half' else math.pi/4
            end=(cx+r*math.cos(t),cy+r*math.sin(t));ax.plot([cx,end[0]],[cy,end[1]],'--',c=grey,lw=1)
            ax.annotate('$r='+tx(p['r'])+'$',((cx+end[0])/2,(cy+end[1])/2),xytext=(10,3),textcoords='offset points',fontsize=12,bbox={'facecolor':'white','edgecolor':'none','pad':1})
        else:ax.plot([A[0],B[0]],[A[1],B[1]],'--',c=grey,lw=1)
        xx=xs+[A[0],B[0],0];yy=ys+[A[1],B[1],0]
    else:
        ax.plot([A[0],B[0]],[A[1],B[1]],c=blue,lw=2)
        start,end=(A,B) if p['direction']>0 else (B,A)
        ax.annotate('',xy=(start[0]+.58*(end[0]-start[0]),start[1]+.58*(end[1]-start[1])),xytext=(start[0]+.42*(end[0]-start[0]),start[1]+.42*(end[1]-start[1])),arrowprops={'arrowstyle':'->','color':blue,'lw':1.8})
        xx=[A[0],B[0],0];yy=[A[1],B[1],0]
    if p['kind']!='radius':
        ax.scatter([A[0],B[0]],[A[1],B[1]],s=18,c=blue,zorder=5)
        for pt,label in [(A,'A'),(B,'B')]:
            # Labels go outward from the center, leaving the guide and curve clear.
            right=pt[0]>cx or (pt[0]==cx and pt[1]>cy)
            off=(8,15) if right else (-8,-24)
            ax.annotate('$'+label+'('+str(pt[0])+','+str(pt[1])+')$',pt,xytext=off,textcoords='offset points',ha='left' if right else 'right',fontsize=10,bbox={'facecolor':'white','edgecolor':'none','pad':1})
        if helper and a and b:
            ax.plot([A[0],B[0],B[0]],[A[1],A[1],B[1]],':',c='#b36b00',lw=1.5)
    width=max(max(xx)-min(xx),4);height=max(max(yy)-min(yy),4)
    pad=max(width,height)*.23
    ax.set_xlim(min(xx)-pad,max(xx)+pad);ax.set_ylim(min(yy)-pad,max(yy)+pad)
    ax.set_aspect('equal');ax.spines[['top','right']].set_visible(False);ax.spines[['left','bottom']].set_position('zero')
    ax.set_xlabel('$x$',loc='right');ax.set_ylabel('$y$',loc='top',rotation=0)
    ax.set_xticks(sorted(set([0,int(A[0]),int(B[0])])));ax.set_yticks(sorted(set([0,int(A[1]),int(B[1])])));ax.tick_params(labelsize=9)
    ax.text(.08,.87,'$C$',transform=ax.transAxes,c=blue,fontsize=14)
    fig.tight_layout(pad=1.5);fig.savefig(dest,facecolor='white');plt.close(fig)
    return str(dest)

def display(s):return '\n\n$$\n'+s+'\n$$\n\n'
def make(p,profile=0,seed=0):
    vals,recipes=bank(p,profile);a,b,d,L=geometry(p);image=diagram(p)
    closed=p['extent']=='full';op=r'\oint_C' if closed else r'\int_C';integral=op+r'\,\mathrm{d}s'
    direction='counterclockwise' if p['direction']>0 else 'clockwise'
    if p['extent'] is None:
        start,end=('A','B') if p['direction']>0 else ('B','A')
        desc=f'where $C$ is the line segment shown, traversed once from ${start}$ to ${end}$.'
    else:
        extent='semicircular arc' if p['extent']=='half' else 'circle'
        measurement=('radius $'+tx(p['r'])+'$') if p['kind']=='radius' else 'diameter $AB$'
        desc=f'where $C$ is the {extent} with {measurement} shown, traversed once {direction}. The dashed guide is not part of the path.'
    prompt=f'![Curve and its measurements]({image})\n\nCalculate'+display(integral+',')+desc
    sol='The line integral of unity with respect to arc length equals the length $L$ of the path:'+display(r'\int_C\,\mathrm{d}s=L.')
    if p['kind']=='radius':
        sol+='The supplied radius determines the diameter:'+display('d=2r=2('+tx(p['r'])+')='+tx(d)+'.')
    else:
        A,B=p['A'],p['B']
        sol+='The endpoints are $A('+','.join(map(str,A))+')$ and $B('+','.join(map(str,B))+')$.'
        if a and b:
            helper=diagram(p,True)
            sol+=f' The dotted right triangle is an auxiliary construction, not additional path.\n\n![Auxiliary right triangle]({helper})\n\n'
            sol+='Use the two coordinate differences:'+display(r'\begin{aligned}d=AB&=\sqrt{('+str(B[0])+'-('+str(A[0])+'))^2+('+str(B[1])+'-('+str(A[1])+r'))^2}\\&=\sqrt{'+tx(a*a)+'+'+tx(b*b)+r'}=\sqrt{'+tx(a*a+b*b)+'}='+tx(d)+r'.\end{aligned}')
        else:
            axis=0 if a else 1
            sol+=' The segment is '+('horizontal' if a else 'vertical')+'. Its endpoint distance is'+display('d=AB=|'+str(B[axis])+'-('+str(A[axis])+')|='+tx(d)+'.')
    if p['extent'] is None: sol+='Here the path is the segment itself, so'+display('L=d='+tx(L)+'.')
    elif p['extent']=='half': sol+='The path is half of a circle. Using circumference from diameter,'+display(r'\begin{aligned}L&=\frac{\pi d}{2}\\&=\frac{\pi('+tx(d)+')}{2}='+tx(L)+r'.\end{aligned}')
    else: sol+='The path is a full circle. Its circumference is'+display(r'\begin{aligned}L&=\pi d\\&=\pi('+tx(d)+')='+tx(L)+r'.\end{aligned}')
    sol+='Therefore,'+display(integral+'='+tx(L)+'.')+'Reversing the direction leaves traveled length unchanged.'
    if closed:sol+=' A closed path has zero net displacement, but its length is positive.'
    prompt=normalize_prose(prompt);sol=normalize_prose(sol);values=[tx(v) for v in vals]
    # Output directory is not mathematical content and cannot change identity.
    body={'prompt':prompt.replace(str(output_dir()),'ASSET'),'solution':sol.replace(str(output_dir()),'ASSET'),'bank':sorted(values),'level':p['level'],'version':VERSION}
    qid=uid(canonical(body));fid=uid(qid+'selection')
    answers=[{':answer/id':uid(fid+v),':answer/type':':answer.type/math',':answer/value':v} for v in values]
    key=answers[0][':answer/id'];random.Random(seed).shuffle(answers)
    f={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',key]}
    semantic=['circle',p['extent'],str(d)] if p['extent'] else ['segment',*sorted([str(a),str(b)])]
    result={'knowledge_point':KP,'question':{':question/id':qid,':question/problem':prompt,':question/worked-solution':sol,':question/difficulty':':question.difficulty/'+p['level'],':question/answer-fields':[f]},'generation':{'version':VERSION,'seed':seed,'parameters':p,'profile':profile,'recipes':dict(zip(values,recipes)),'length':str(L),'semantic':canonical(semantic)}}
    return validate_generated_record(result)

def _batch_candidate(level,count,seed):
    if level=='unclassified':level='easy'
    if level not in BANDS or count<0:raise ValueError('invalid difficulty/count')
    rng=random.Random(seed);cases=CASES[level][:];rng.shuffle(cases);profiles=list(range(15));rng.shuffle(profiles)
    slots=[(cases[i%len(cases)],profiles[(i//len(cases)+i%len(cases))%15]) for i in range(count)]
    catalog={}
    for case,profile in dict.fromkeys(slots):
        kind=case.split('_')[0]
        if kind=='radius': shapes=list(range(1,10))
        elif kind in ('horizontal','vertical'): shapes=list(range(2,11))
        elif level=='easy': shapes=[(a,b) for a in range(2,7) for b in range(a+1,7)]
        else: shapes=[(2,4),(3,6),(3,4),(2,2),(3,3),(4,4),(2,3),(1,2)]
        rng.shuffle(shapes);eligible={}
        for shape in shapes:
            # Try compatible translations/signs without discarding a useful semantic shape.
            for attempt in range(36):
                p=sample(level,case,rng)
                if kind=='radius':p['r']=shape
                else:
                    if kind=='horizontal':dx,dy=shape,0
                    elif kind=='vertical':dx,dy=0,shape
                    else:
                        dx,dy=shape
                        if rng.choice([True,False]):dx,dy=dy,dx
                    dx*=rng.choice([-1,1]);dy*=rng.choice([-1,1])
                    p['B']=[p['A'][0]+dx,p['A'][1]+dy]
                try:bank(p,profile)
                except ValueError:continue
                a,b,d,L=geometry(p)
                semantic=canonical(['circle',p['extent'],str(d)] if p['extent'] else ['segment',*sorted([str(a),str(b)])])
                eligible[semantic]=p;break
        catalog[(case,profile)]=eligible
    # Match finite batch slots to semantic instances. Greedy rejection can consume
    # the sole compatible instance needed by a later complete bank profile.
    owners={};assigned={}
    def match(i,visited):
        for semantic in catalog[slots[i]]:
            if semantic in visited:continue
            visited.add(semantic)
            if semantic not in owners or match(owners[semantic],visited):
                owners[semantic]=i;assigned[i]=semantic;return True
        return False
    for i in sorted(range(count),key=lambda i:len(catalog[slots[i]])):
        if not match(i,set()):raise ValueError('requested batch exceeds the distinct supported semantic pool')
    plan=[(catalog[slots[i]][assigned[i]],slots[i][1],rng.getrandbits(63)) for i in range(count)]
    if not balanced_plan(plan):return None
    return [make(p,profile,item_seed) for p,profile,item_seed in plan]

def balanced_plan(plan):
    """Reject recurring answer-only cues before rendering a small batch.

    Group only by information visible before answering: path extent and bank
    shape. Single observations do not imply a recurring predictor.
    """
    groups={}
    for p,profile,item_seed in plan:
        vals,_=bank(p,profile);texts=[tx(v) for v in vals]
        rank=1+sum(bool(v<vals[0]) for v in vals)
        positions=list(range(5));random.Random(item_seed).shuffle(positions)
        position=positions.index(0)
        pi=[i for i,t in enumerate(texts) if r'\pi' in t and '+' not in t]
        radical_pi=[i for i in pi if r'\sqrt' in texts[i]]
        has_sum=any('+' in t for t in texts)
        signatures=[('extent',p['extent'] or 'segment')]
        signatures.append(('bank',p['extent'] or 'segment',len(pi),len(radical_pi),has_sum))
        for sig in signatures:
            groups.setdefault(sig,[]).append((rank,position))
        for name,indices in [('pure-pi',pi),('radical-pi',radical_pi)]:
            if 0 in indices and len(indices)>1:
                subrank=1+sum(bool(vals[i]<vals[0]) for i in indices)
                groups.setdefault((name,p['extent'],len(indices),has_sum),[]).append((subrank,position))
    return all(len(rows)<2 or all(len({row[i] for row in rows})>1 for i in range(2)) for rows in groups.values())

def batch(level,count,seed):
    # Deterministic rejection is a construction rule, not a replacement seed
    # chosen by a caller after seeing a poor batch.
    for attempt in range(160):
        candidate_seed=seed if attempt==0 else int.from_bytes(hashlib.sha256(f'{seed}/bank-balance/{attempt}'.encode()).digest()[:8],'big')
        try:result=_batch_candidate(level,count,candidate_seed)
        except ValueError as error:
            if 'distinct supported semantic pool' not in str(error):raise
            continue
        if result is not None:return result
    raise ValueError('requested batch cannot satisfy supported pool and answer-bank balance')

def replay_sources():
    """Complete imported cases at original coordinates/banks, never used in normal sampling."""
    result=[]
    for q in json.loads((ROOT/'source-cases.json').read_text()):
        q=copy.deepcopy(q)
        for k in (':question/problem',':question/worked-solution'):q[k]=normalize_prose(q[k])
        q[':question/worked-solution']=q[':question/worked-solution'].replace('directed along the $y$-axis','parallel to the $y$-axis').replace('directed along the $x$-axis','parallel to the $x$-axis')
        f=q[':question/answer-fields'][0]
        for a in f[':answer-field/choices']:
            a[':answer/type']=':answer.type/math';a[':answer/value']=normalize_tex(a[':answer/value'])
        f[':answer-field/type']=':answer-field.type/radio';f[':answer-field/correct']=[':answer/id',f[':answer-field/correct'][':answer/id']]
        q[':question/difficulty']=':question.difficulty/easy'
        result.append(validate_generated_record({'knowledge_point':KP,'question':q}))
    return result

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=[*BANDS,'unclassified'],default='easy');ap.add_argument('--count',type=int,default=1);ap.add_argument('--seed',type=int,default=0);ap.add_argument('--format',choices=['json'],default='json');args=ap.parse_args()
    print(json.dumps(batch(args.difficulty,args.count,args.seed),indent=2))
