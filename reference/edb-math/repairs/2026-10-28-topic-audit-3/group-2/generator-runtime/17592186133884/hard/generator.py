#!/usr/bin/env python3
"""Seeded, relocatable Green's theorem setup generator. No database access."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import random
import uuid
import sympy as s
from math_format import normalize_prose, normalize_tex, validate_generated_record

x,y=s.symbols('x y', real=True)
KP=17592186133884
NS=uuid.UUID('48652211-e469-55b9-96cb-2526a4135d34')
VERSION='greens-setup-v3'
def tex(v): return s.latex(s.sympify(v)).replace(r'\log',r'\ln')
def ident(v): return str(uuid.uuid5(NS,VERSION+v))
def display(v): return '$$\n'+v+'\n$$'
def integral(c,b,inner,outer):
    a,z,l,h=b
    return (r'\int_{'+tex(a)+'}^{'+tex(z)+r'}\int_{'+tex(l)+'}^{'+tex(h)+r'}\left('+tex(c)+r'\right)\,\mathrm{d}'+str(inner)+r'\,\mathrm{d}'+str(outer))
def sample_parameters(rng):
    return {
        'order':rng.choice(['yx','xy']), 'a':rng.choice([-2,-1,1,2]),
        'b':rng.choice([-2,-1,0,1,2]), 'c':rng.choice([-2,0,2]),
        'A':rng.choice([-1,0,1]),'L':rng.choice([1,2,3]),
        'C':rng.choice([-1,0,1]),'H':rng.choice([1,2,3]),
        'r':rng.choice([-2,-1]),'z':rng.choice([1,2]),'irrelevant':0}

def instance(level,rng,parameters=None):
    p=dict(parameters) if parameters is not None else sample_parameters(rng)
    inner,outer=(y,x) if p['order']=='yx' else (x,y)
    a,b,c=p['a'],p['b'],p['c']
    if level=='easy':
        P=a*y*y+p.get('irrelevant',0)*x*x; Q=b*x*y
    elif level=='moderate':
        P=a*x*y*y+p.get('irrelevant',0)*x*x; Q=b*x*x*y
    else:
        P=s.log(x+p.get('log_offset',4))-a*y*y+p.get('irrelevant',0)*x*x
        Q=b*x*x+c*x*y+y*y
    if level=='easy':
        A,B,C,D=map(s.Integer,[p['A'],p['A']+p['L'],p['C'],p['C']+p['H']])
        if (A,B)==(C,D):raise ValueError('identical rectangle intervals')
        bounds=(A,B,C,D); bad=[(A,B,D,C),(C,D,A,B)]
    elif level=='moderate':
        A,B,C,H=map(s.Integer,[p['A'],p['A']+p['L'],p['C'],p['H']])
        upper=C+H*(outer-A)/(B-A)
        bounds=(A,B,C,upper);bad=[(A,B,upper,C),(A,B,C,C+H)]
    else:
        A,B=s.Integer(p['r']),s.Integer(p['z']);lower=outer**2
        upper=(A+B)*outer-A*B
        bounds=(A,B,lower,upper);bad=[(A,B,upper,lower),(s.Integer(0),B,lower,upper)]
    py=s.diff(P,y);qx=s.diff(Q,x);curl=s.expand(qx-py)
    errors=[]
    for name,e in [('sum',qx+py),('reverse',py-qx),('omit-P',qx),('omit-Q',-py),
                   ('miss-factor-P',qx-py/2),('miss-factor-Q',qx/2-py)]:
        e=s.expand(e)
        if s.simplify(e-curl)!=0 and not any(s.simplify(e-v)==0 for _,v in errors):errors.append((name,e))
    if len(errors)<2:raise ValueError('not enough distinct derivative errors')
    rng.shuffle(errors)
    return p,P,Q,inner,outer,bounds,bad,curl,errors

def diagram(level,bounds,inner,outer,output):
    # Backend and cache are explicitly outside the immutable package.
    os.environ.setdefault('MPLCONFIGDIR',str(output/'mpl-cache'))
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np
    key=hashlib.sha256((level+str(bounds)+str(inner)).encode()).hexdigest()[:20]
    file=output/('region-'+key+'.png')
    if not file.exists():
        A,B,lo,hi=bounds;t=np.linspace(float(A),float(B),160)
        def values(v):
            q=s.lambdify(outer,v,'numpy')(t)
            return np.full_like(t,float(q)) if np.ndim(q)==0 else q
        low,high=values(lo),values(hi)
        fig,ax=plt.subplots(figsize=(4.8,3.4),layout='constrained')
        if inner==y:
            ax.fill_between(t,low,high,color='#c5e3f5');ax.plot(t,low,t,high,color='#206e9a')
            ax.plot([float(A),float(A)],[low[0],high[0]],color='#206e9a');ax.plot([float(B),float(B)],[low[-1],high[-1]],color='#206e9a')
            ax.annotate('',xy=(t[55],low[55]),xytext=(t[35],low[35]),arrowprops={'arrowstyle':'->','color':'#142b3b'})
            ax.text(t[80],(low[80]+high[80])/2,'D',ha='center')
            ax.text(t[85],high[85],r'$y='+tex(hi)+'$',va='bottom',fontsize=9)
            ax.text(t[85],low[85],r'$y='+tex(lo)+'$',va='top',fontsize=9)
        else:
            ax.fill_betweenx(t,low,high,color='#c5e3f5');ax.plot(low,t,high,t,color='#206e9a')
            ax.plot([low[0],high[0]],[float(A),float(A)],color='#206e9a');ax.plot([low[-1],high[-1]],[float(B),float(B)],color='#206e9a')
            # Along the right boundary, increasing y is counterclockwise.
            ax.annotate('',xy=(high[55],t[55]),xytext=(high[35],t[35]),arrowprops={'arrowstyle':'->','color':'#142b3b'})
            ax.text((low[80]+high[80])/2,t[80],'D',ha='center')
            ax.text(high[85],t[85],r'$x='+tex(hi)+'$',ha='left',fontsize=9)
            ax.text(low[85],t[85],r'$x='+tex(lo)+'$',ha='right',fontsize=9)
        ax.axhline(0,lw=.6,color='gray');ax.axvline(0,lw=.6,color='gray')
        ax.set_xlabel('x');ax.set_ylabel('y');ax.margins(.28);ax.set_title('Counterclockwise boundary',fontsize=10)
        fig.savefig(file,dpi=125);plt.close(fig)
    return str(file)

def make_record(level,rng,output,parameters=None,with_diagram=True):
    p,P,Q,iv,ov,bounds,bad,curl,errors=instance(level,rng,parameters)
    # Grid profile prevents a single repeated component from identifying the key.
    e1,e2=errors[:2];rng.shuffle(bad)
    specs=[(curl,bounds,'correct'),(e1[1],bounds,e1[0]),
           (curl,bad[0],'limits'),(e1[1],bad[0],e1[0]+'+limits'),
           (e2[1],bad[1],e2[0]+'+limits')]
    if p.get('source_replay')=='q-108467':
        specs=[(2*x*y,(0,1,0,2*x),'correct'),(x*x*y,(0,1,0,2*x),'source'),
               (x*x*y*y,(0,2,0,2*x),'source'),(x*y*y,(0,1,0,2*x),'source'),(2*x,(0,2,0,x),'source')]
    elif p.get('source_replay')=='q-109263':
        specs=[(2*(x+y),(-1,2,x*x,x+2),'correct'),(2*(x+y),(-1,2,x+2,x*x+x+2),'source'),
               (2*(x+y),(0,2,-x*x,x+2),'source'),(2*(x-y),(0,2,x*x,x+2),'source'),(2*y-x,(-1,2,x*x,x+2),'source')]
    values=[normalize_tex(integral(c,b,iv,ov)) for c,b,_ in specs]
    assert len(set(values))==5
    A,B,lo,hi=bounds
    inequalities=tex(A)+r'\le '+str(ov)+r'\le '+tex(B)+r',\quad '+tex(lo)+r'\le '+str(iv)+r'\le '+tex(hi)
    if level=='easy': region='Let $D$ be the rectangle $'+inequalities+'$.'
    elif level=='moderate':
        pts=[(A,lo),(B,lo),(B,hi.subs(ov,B))]
        if iv==x:pts=[(v,u) for u,v in pts]
        region='Let $D$ be the triangle with vertices '+', '.join('$('+tex(u)+','+tex(v)+')$' for u,v in pts)+'.'
    else:region='Let $D$ be the region enclosed by $'+str(iv)+'='+tex(lo)+'$ and $'+str(iv)+'='+tex(hi)+'$.'
    line=r'\oint_C\left('+tex(P)+r'\right)\,\mathrm{d}x+\left('+tex(Q)+r'\right)\,\mathrm{d}y'
    prompt=region+' Its boundary $C$ is traversed counterclockwise.\n\n'
    if level=='easy':prompt+="Use Green's theorem:\n\n"+display(r'\oint_C P\,\mathrm{d}x+Q\,\mathrm{d}y=\iint_D(Q_x-P_y)\,\mathrm{d}A.')+'\n\n'
    prompt+='Which repeated integral, integrating with respect to $'+str(iv)+'$ first, represents the following line integral? Use the actual region $D$ with bounds in increasing order. Do not evaluate it.\n\n'+display(line)
    if level=='hard':
        prompt=prompt.replace(display(line),display(r'\oint_C\mathbf{F}\cdot\mathrm{d}\mathbf{r}')+'\n\nwhere\n\n'+display(r'\mathbf{F}(x,y)=\langle '+tex(P)+', '+tex(Q)+r'\rangle.'))
    sol="The component functions are continuously differentiable on an open set containing $D$. For counterclockwise traversal, Green's theorem uses $Q_x-P_y$.\n\n"
    sol+=display(r'\begin{aligned}P&='+tex(P)+r',\\Q&='+tex(Q)+r',\\P_y&='+tex(s.diff(P,y))+r',\\Q_x&='+tex(s.diff(Q,x))+r',\\Q_x-P_y&=('+tex(s.diff(Q,x))+r')-('+tex(s.diff(P,y))+r')\\&='+tex(curl)+r'.\end{aligned}')+'\n\n'
    if level=='moderate':
        sol+='The sloping edge has equation $'+str(iv)+'='+tex(hi)+'$. The other edges give the constant limits.\n\n'
    if level=='hard':
        sol+='Equating the two boundary expressions gives\n\n'+display(r'\begin{aligned}'+tex(lo)+'&='+tex(hi)+r',\\'+tex(s.factor(lo-hi))+r'&=0,\\'+str(ov)+'&='+tex(A)+r'\quad\text{or}\quad '+tex(B)+r'.\end{aligned}')+'\n\n'
        sol+='Between these intersections, the line is above the parabola in the inner coordinate: $'+tex(s.factor(hi-lo))+r'\ge0$.'+'\n\n'
    sol+='Thus $D$ is described by $'+inequalities+'$. The bounds stay attached to their variables.\n\n'
    if with_diagram:sol+='![]('+diagram(level,bounds,iv,ov,output)+')\n\n'
    sol+='The required setup is\n\n'+display(r'\begin{aligned}'+r'\oint_C P\,\mathrm{d}x+Q\,\mathrm{d}y&=\iint_D(Q_x-P_y)\,\mathrm{d}A\\&='+values[0]+r'.\end{aligned}')
    prompt,sol=normalize_prose(prompt),normalize_prose(sol)
    signature=json.dumps([prompt,values],sort_keys=True)
    qid=ident(signature);fid=ident(qid+'field')
    choices=[{':answer/id':ident(fid+v),':answer/type':':answer.type/math',':answer/value':v} for v in values]
    correct=choices[0][':answer/id'];rng.shuffle(choices)
    rec={'knowledge_point':{'db_id':KP,'id':str(NS),'title':"Expressing a Line Integral as a Repeated Integral Using Green's Theorem"},
         'question':{':question/id':qid,':question/problem':prompt,':question/worked-solution':sol,':question/difficulty':':question.difficulty/'+level,
                     ':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',correct]}]},
         'generation':{'version':VERSION,'parameters':p,'template':level+'-'+p['order'],'bank_profile':e1[0]+'/'+e2[0],
                       'source_ids':{'easy':['q-42085'],'moderate':['q-108467'],'hard':['q-109263']}[level],
                       'basis':7408,'derivation':{'P':str(P),'Q':str(Q),'curl':str(curl),'bounds':list(map(str,bounds)),
                                                'final':values[0],'necessary_conversions':[]}}}
    return validate_generated_record(rec)

def source_replay(source_id,output):
    p={'order':'yx','a':1,'b':2,'c':0,'A':0,'L':1,'C':0,'H':2,'r':-1,'z':2,'irrelevant':0,'source_replay':source_id}
    if source_id=='q-108467':level='moderate'
    elif source_id=='q-109263':level='hard';p.update(b=1,log_offset=2)
    else:raise ValueError('Only the two legacy supported source banks have literal replay')
    return make_record(level,random.Random(0),Path(output),p)

def generate_batch(level,count,seed,output):
    output=Path(output).resolve();output.mkdir(parents=True,exist_ok=True)
    rng=random.Random(seed);out=[];seen=set();attempts=0
    # Small batches must exercise the available geometric decisions. Cycle
    # shuffled profiles rather than relying on independent draws to cover them.
    orders=['yx','xy'];rng.shuffle(orders)
    roots=[(-2,1),(-2,2),(-1,1),(-1,2)];rng.shuffle(roots)
    while len(out)<count:
        attempts+=1
        if attempts>100*max(1,count):raise ValueError('cannot supply requested distinct batch')
        parameters=sample_parameters(rng)
        parameters['order']=orders[len(out)%len(orders)]
        if level=='hard':parameters['r'],parameters['z']=roots[len(out)%len(roots)]
        try:r=make_record(level,rng,output,parameters)
        except ValueError:continue
        # Semantic identity excludes shuffle, bank, diagrams, and irrelevant field components.
        d=r['generation']['derivation'];key=(d['P'],d['Q'],tuple(d['bounds']),r['generation']['template'])
        if key in seen:continue
        seen.add(key);r['generation'].update(seed=seed,batch_index=len(out));out.append(r)
    return out

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--difficulty',choices=['easy','moderate','hard'],default='moderate');p.add_argument('--count',type=int,default=1);p.add_argument('--seed',type=int,default=0);p.add_argument('--format',choices=['json'],default='json');a=p.parse_args()
    if a.count<1:p.error('count must be positive')
    dest=os.environ.get('COURSE_ACADEMY_GENERATOR_OUTPUT_DIR')
    if not dest:p.error('set COURSE_ACADEMY_GENERATOR_OUTPUT_DIR to an explicit writable asset directory')
    print(json.dumps(generate_batch(a.difficulty,a.count,a.seed,dest),indent=2))
if __name__=='__main__':main()
