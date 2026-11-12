#!/usr/bin/env python3
"""Geometric scalar comparison. Assets are outputs, never package files."""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import random
import uuid
from fractions import Fraction as F
from math_format import normalize_prose, validate_generated_record
from label_layout import endpoint_labels

HERE = Path(__file__).resolve().parent
KP = {'db_id':17592186096701,'id':'2fbb8f19-f35a-59c4-9b77-8f6c3542ef28','title':'Finding a Scalar Factor in a Linear Combination'}
VERSION = 'geometric-scalar-4'
BANDS = ('easy','moderate','hard')
# Complete observed all-positive banks. The correct role is independently assigned.
BANKS = [('1','3/2','2','5/2','3'), ('3/2','2','5/2','3','7/2')]

def tex(v):
    v=F(v)
    return str(v.numerator) if v.denominator==1 else ('-' if v<0 else '')+r'\frac{'+str(abs(v.numerator))+'}{'+str(v.denominator)+'}'

def digest(x):
    return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def vm(s): return r'\mathbf{'+s+'}'

def term(k,s): return ('' if F(k)==1 else tex(k))+vm(s)

def point(p): return '('+', '.join(tex(x) for x in p)+')'

def instance(a,b,unknown,known,scalar,profile):
    a=tuple(map(F,a));b=tuple(map(F,b));k=F(known);s=F(scalar)
    if unknown not in ('a','b') or k<=0 or s<=0: raise ValueError('Positive scalar domain')
    if a[0]*b[1]-a[1]*b[0]==0: raise ValueError('Nonparallel vectors required')
    ca,cb=(s,k) if unknown=='a' else (k,s)
    c=tuple(ca*x+cb*y for x,y in zip(a,b))
    base=b if unknown=='a' else a
    p=tuple(k*x for x in base)
    residual=tuple(x-y for x,y in zip(c,p))
    pts=[a,b,c,p]
    half=any((x*2).denominator==1 and x.denominator==2 for v in pts for x in v)
    if any((x*2).denominator!=1 for v in pts for x in v): raise ValueError('Endpoint not on half-grid')
    return {'a':a,'b':b,'c':c,'p':p,'residual':residual,'unknown':unknown,'known':k,'scalar':s,'profile':profile,'half':half}

def serial(p):
    return {k:([str(x) for x in v] if isinstance(v,tuple) else str(v) if isinstance(v,F) else v) for k,v in p.items()}

def sample(level,rng):
    # Answer-bearing roles and rule case precede geometry.
    u=rng.choice(('a','b'))
    profile=rng.choice(('multiple','oblique','fractional')) if level=='moderate' else level
    radio=level!='hard' and rng.choice((True,False))
    bank=rng.choice(BANKS) if radio else None
    s=F(rng.choice(bank if bank else ('1/2','1','3/2','2','5/2','3') if level!='hard' else ('1/4','1/2','3/4','1','5/4','3/2','7/4','2')))
    if profile=='easy':
        k=F(1);known_vec=(rng.randint(2,5),0);unknown_vec=(0,rng.choice((2,4)))
    elif profile=='multiple':
        k=F(rng.choice((2,3)));known_vec=(rng.choice((-2,-1,1,2)),rng.choice((1,2)));unknown_vec=(rng.choice((2,4)),0)
    elif profile=='oblique':
        k=F(1);known_vec=(rng.choice((3,4,5)),0);unknown_vec=(rng.choice((2,4)),rng.choice((2,4)))
    elif profile=='fractional':
        k=F(rng.choice(('1/2','3/2','4/3')));known_vec=(rng.choice((3,6)) if k.denominator==3 else rng.choice((2,4)),0);unknown_vec=(rng.choice((2,4)),rng.choice((2,4)))
    else:
        k=F(rng.choice(('1/2','3/2','5/2')))
        known_vec=(rng.choice((1,3)),rng.choice((1,2)))
        unknown_vec=(rng.choice((2,4)),rng.choice((2,4)))
        if known_vec[0]*unknown_vec[1]==known_vec[1]*unknown_vec[0]: return sample(level,rng)
    # Reflections/quarter-turns retain unit-grid reading, without reversing a scalar.
    sx=rng.choice((-1,1));sy=rng.choice((-1,1));swap=rng.choice((True,False))
    def transform(v):
        v=(sx*v[0],sy*v[1]);return (v[1],v[0]) if swap else v
    a,b=(unknown_vec,known_vec) if u=='a' else (known_vec,unknown_vec)
    return instance(transform(a),transform(b),u,k,s,profile),bank

def diagram(p,solution,out):
    os.environ.setdefault('MPLCONFIGDIR',str(out/'mpl-cache'))
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.ticker import MultipleLocator
    name=digest({'version':VERSION,'p':serial(p),'solution':solution})+'.png'
    target=out/'assets'/name
    if target.exists(): return 'assets/'+name
    target.parent.mkdir(parents=True,exist_ok=True)
    pts=[(0,0),p['a'],p['b'],p['c'],p['p']]
    lo=[math.floor(min(float(v[i]) for v in pts))-1.2 for i in range(2)]
    hi=[math.ceil(max(float(v[i]) for v in pts))+1.2 for i in range(2)]
    fig,ax=plt.subplots(figsize=(5.8,5.4),dpi=140)
    ax.set(xlim=(lo[0],hi[0]),ylim=(lo[1],hi[1]),aspect='equal')
    for axis in (ax.xaxis,ax.yaxis):
        axis.set_major_locator(MultipleLocator(1))
        if p['half']: axis.set_minor_locator(MultipleLocator(.5))
    ax.grid(which='major',color='#bfc7d0',lw=.7,zorder=0)
    if p['half']:ax.grid(which='minor',color='#dbe0e5',lw=.6,linestyle=':',zorder=0)
    ax.tick_params(which='both',bottom=False,left=False,labelbottom=False,labelleft=False)
    for spine in ax.spines.values():spine.set_visible(False)
    colors={'a':'#2166ac','b':'#a86600','c':'#202124'}
    def arrow(start,end,color,style='-',lw=2):
        ax.annotate('',xy=tuple(map(float,end)),xytext=tuple(map(float,start)),arrowprops=dict(arrowstyle='-|>',color=color,lw=lw,linestyle=style,mutation_scale=13),zorder=3)
    def label(pt,text,offset=(0,0),color='#202124'):
        ax.annotate(text,tuple(map(float,pt)),xytext=offset,textcoords='offset points',color=color,fontsize=12,zorder=6,bbox=dict(facecolor='white',edgecolor='none',alpha=.9,pad=.6))
    # Position point labels outward from the origin; vector labels on alternate sides.
    label((0,0),'$O$',(-14,-14))
    for idx,sym in enumerate(('a','b','c')):
        end=p[sym];arrow((0,0),end,colors[sym])
    if solution:
        known='b' if p['unknown']=='a' else 'a'
        arrow((0,0),p['p'],colors[known],'--',1.5)
        arrow(p['p'],p['c'],colors[p['unknown']],'--',1.8)
        endpoint='A' if p['known']==1 and known=='a' else 'B' if p['known']==1 else 'P'
        if endpoint=='P':label(p['p'],'$P$',(7,-15))
        mid=tuple((x+y)/2 for x,y in zip(p['p'],p['c']))
        label(mid,r'$\lambda'+vm(p['unknown'])+'$',(9,2),colors[p['unknown']])
        if p['known']!=1:
            label(tuple(F(3,4)*x for x in p['p']),'$'+term(p['known'],known)+'$',(-26,5),colors[known])
    fig.tight_layout(pad=.4)
    witness=endpoint_labels(fig,ax,[(sym.upper(),sym,p[sym],colors[sym]) for sym in ('a','b','c')])
    fig.savefig(target,facecolor='white',metadata={'Software':VERSION});plt.close(fig)
    # Machine-readable geometry witnesses are evidence assets, never runtime imports.
    target.with_suffix('.json').write_text(json.dumps({'geometry':serial(p),'bounds':[lo,hi],'solution':solution,'renderer_version':4,'labels':witness},indent=2))
    return 'assets/'+name

def build(level,p,bank=None,seed=0,out=None):
    out=Path(out or os.environ.get('COURSE_ACADEMY_GENERATOR_OUTPUT_DIR','/tmp/course-academy-scalar-output')).resolve()
    out.mkdir(parents=True,exist_ok=True)
    assets={role:diagram(p,role=='solution',out) for role in ('prompt','solution')}
    u=p['unknown'];known='a' if u=='b' else 'b';k=p['known'];s=p['scalar']
    given=(r'\lambda'+vm('a')+'+'+term(k,'b')) if u=='a' else term(k,'a')+r'+\lambda'+vm('b')
    final=term(s,'a')+'+'+term(k,'b') if u=='a' else term(k,'a')+'+'+term(s,'b')
    endpoint='A' if k==1 and known=='a' else 'B' if k==1 else 'P'
    remaining=r'\overrightarrow{'+endpoint+'C}'
    scale_text='Solid grid lines are one unit apart; dotted lines divide each square in half.' if p['half'] else 'Grid squares have side length one unit.'
    prompt=(r'The arrows show $\overrightarrow{OA}=\mathbf a$, $\overrightarrow{OB}=\mathbf b$, and $\overrightarrow{OC}=\mathbf c$. '+scale_text+'\n\n![]('+assets['prompt']+')\n\nGiven that $'+vm('c')+'='+given+r'$, find $\lambda$.')
    if not bank:prompt+='\n\n'+r'$\lambda=$ {{field-1}}.'
    base=p[known];v=p[u];r=p['residual'];construction=p['p']
    solution=('Construct the known component $'+term(k,known)+'$ from $O$'+(', ending at $'+endpoint+'$.' if k==1 else ', and call its endpoint $P$.')+' Count signed horizontal and vertical grid displacements:\n\n$$\n'+r'\begin{aligned}'+'\n'+r'\overrightarrow{O'+endpoint+'} &='+tex(k)+r'\,('+', '.join(tex(x) for x in base)+')='+point(construction)+r'. \\'+'\n'+remaining+' &='+point(r)+r'.'+'\n'+r'\end{aligned}'+'\n$$\n\n![]('+assets['solution']+')\n\n')
    rows=[]
    for i,axis in enumerate(('Horizontal','Vertical')):
        if v[i]:rows.append(r'\text{'+axis+r' scale} &=\frac{'+tex(r[i])+'}{'+tex(v[i])+'}='+tex(s))
    solution+='Compare the remaining displacement with $'+vm(u)+'$, whose grid displacement is $'+point(v)+'$:\n\n$$\n'+r'\begin{aligned}'+'\n'+(' \\\\\n'.join(rows))+'\n'+r'\end{aligned}'+'\n$$\n\n'
    solution+='The scale is positive, so the remaining vector has the same direction as $'+vm(u)+'$. Thus $'+remaining+'='+term(s,u)+'$. By the triangle law,\n\n$$\n'+r'\begin{aligned}'+'\n'+vm('c')+r' &=\overrightarrow{O'+endpoint+'}+'+remaining+r' \\'+'\n&='+term(k,known)+'+'+term(s,u)+r' \\'+'\n&='+final+'.\n'+r'\end{aligned}'+'\n$$\n\nThe vectors $'+vm('a')+'$ and $'+vm('b')+'$ are not parallel, so their coefficients are unique. Matching the coefficient of $'+vm(u)+'$ gives $'+r'\lambda='+tex(s)+'$.'
    prompt=normalize_prose(prompt);solution=normalize_prose(solution)
    answers=[tex(x) for x in bank] if bank else [tex(s)]
    if len(set(answers))!=len(answers) or tex(s) not in answers:raise ValueError('Invalid bank')
    content={'version':VERSION,'level':level,'p':serial(p),'problem':prompt,'solution':solution,'bank':sorted(answers)}
    qid=str(uuid.uuid5(uuid.UUID(KP['id']),digest(content)));fid=str(uuid.uuid5(uuid.UUID(qid),'field-1' if not bank else 'selection'))
    choices=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),v)),':answer/type':':answer.type/math',':answer/value':v} for v in answers]
    correct=next(a[':answer/id'] for a in choices if a[':answer/value']==tex(s))
    random.Random(seed).shuffle(choices)
    record={'knowledge_point':KP,'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection' if bank else 'field-1',':answer-field/type':':answer-field.type/'+('radio' if bank else 'blank'),':answer-field/choices':choices,':answer-field/correct':[':answer/id',correct]}]},'generation':{'version':VERSION,'seed':seed,'parameters':serial(p),'bank_profile':BANKS.index(tuple(bank)) if bank and tuple(bank) in BANKS else 'explicit' if bank else 'blank','instructional_inference':('Hard fractional scales apply the same source-taught endpoint subtraction and scalar ratio to half-grid endpoints; fractions and linear combinations are prerequisite operations. Bands are authored progression without empirical calibration.' if level=='hard' else None),'source_ids':['q-19338','q-70187'] if level=='easy' else ['q-20435','q-327046','q-327052'] if level=='moderate' else ['e-5212'],'assets':assets,'solution_path':{'known_component':point(construction),'remaining_displacement':point(r),'scale_comparisons':rows,'displayed_final':tex(s),'key':tex(s),'conversions':['Reduce grid displacement ratio to a positive rational scalar'],'support':'e-5212; lesson path tracing; prerequisite scalar multiplication'}}}
    validate_generated_record(record)
    return record

def batch(level,count,seed,out=None):
    rng=random.Random(seed);records=[];seen=set();calculations=set()
    for attempt in range(max(1000,count*100)):
        if len(records)==count:return records
        p,bank=sample(level,rng)
        # No repeated main scalar/known calculation in a short batch; eventually
        # allow it for large catalog requests, while retaining distinct geometry.
        calc=(p['profile'],str(p['known']),str(p['scalar']))
        coords=p['a']+p['b'];g=math.gcd(*(abs(int(x)) for x in coords))
        fp=(p['unknown'],str(p['known']),str(p['scalar']),tuple(str(x/g) for x in coords))
        if fp in seen or (count<=5 and calc in calculations):continue
        record=build(level,p,bank,seed+attempt,out)
        seen.add(fp);calculations.add(calc);records.append(record)
    raise ValueError('Requested batch exceeds available distinct constructions')

def replay(source_id):
    # Frozen normalized source replay is isolated from fresh practice sampling.
    data=json.loads((HERE/'replay.json').read_text())
    if source_id not in data: raise ValueError('Unknown replay source')
    return data[source_id]

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=(*BANDS,'unclassified','all'),default='easy');ap.add_argument('--count',type=int,default=1);ap.add_argument('--seed',type=int,default=0);ap.add_argument('--format',choices=('json',),default='json');ap.add_argument('--replay');args=ap.parse_args()
    if args.count<0:ap.error('count must be nonnegative')
    levels=BANDS if args.difficulty=='all' else ('easy' if args.difficulty=='unclassified' else args.difficulty,)
    records=[replay(args.replay)] if args.replay else [r for l in levels for r in batch(l,args.count,args.seed)]
    print(json.dumps(records,indent=2))
