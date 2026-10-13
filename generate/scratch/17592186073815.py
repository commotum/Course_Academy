#!/usr/bin/env python3
"""Closest-point questions: bounded vertical translations of complete source banks.

Easy and moderate retain their observed source ratings and equation layouts.
Each complete source bank is a separate profile, translated as one geometric
object. This is an explicit bounded recipe, not an inferred misconception.
Hard has no validated source template. Seed and bank order never define novelty.
"""
from __future__ import annotations
import argparse, hashlib, json, os, random, re, sys, uuid
from pathlib import Path
os.environ.setdefault('MPLCONFIGDIR','/tmp/course-academy-closest-point-matplotlib')
try:
    import sympy as sp
except ImportError:
    runtime=Path(__file__).resolve().parents[2]/'.venv/bin/python'
    if __name__=='__main__' and runtime.exists():os.execv(str(runtime),[str(runtime),__file__,*sys.argv[1:]])
    raise
KP_ID=17592186073815
KP_UUID='59d3a391-c163-5a04-944c-5d61a3950e03'
TITLE='Finding a Point on a Line That Is Closest to a Given Point'
VERSION='closest-point-vertical-translation-1'
HERE=Path(__file__).resolve().with_suffix('')
GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),'question-generator'))
x,y=sp.symbols('x y',real=True)
def sources():return {q[':question/math-academy-id']:q for q in json.loads((HERE/'source.json').read_text())['record'][':knowledge-point/questions']}
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def expr(t):
    t=re.sub(r'\\(?:d?frac)\{([^{}]+)\}\{([^{}]+)\}',r'(\1/\2)',t.replace(' ',''))
    t=re.sub(r'(\d|\))([xy])',r'\1*\2',t)
    return sp.expand(sp.sympify(t,locals={'x':x,'y':y}))
def line(t):
    l,r=t.split('=');e=expr(l)-expr(r)
    return e.coeff(x),e.coeff(y),-e.subs({x:0,y:0})
def pair(t):return tuple(expr(z) for z in t.strip('()').split(','))
def tex(e):return sp.latex(sp.expand(e)).replace('- ','-')
def pairtex(p):return '('+','.join(map(tex,p))+')'
def printed(q):
    p=q[':question/problem'];equation=re.search(r'on the line \$(.*?)\$',p)[1]
    u,v=map(int,re.search(r'closest to the point \$\((-?\d+),\s*(-?\d+)\)',p).groups())
    A,B,C=line(equation)
    return A,B,C,sp.Integer(u),sp.Integer(v),equation
def fingerprint(q):
    A,B,C,u,v,_=printed(q);scale=A if A else B
    return digest([str(z) for z in (A/scale,B/scale,C/scale,u,v)])
def instance(s,t):
    q=sources()[s];A,B,C,u,v,equation=printed(q);C+=B*t;v+=t
    m=-A/B;b=C/B;n=-1/m;d=v-n*u
    foot=(sp.cancel((d-b)/(m-n)),sp.cancel(m*(d-b)/(m-n)+b))
    eq=(equation.split('=')[0]+'='+tex(C)) if not equation.startswith('y=') else 'y='+tex(m*x+b)
    return A,B,C,u,v,m,b,n,d,foot,eq
def render_plot(s,t,output_dir):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib.patches import Polygon
    A,B,C,u,v,m,b,n,d,foot,eq=instance(s,t)
    Q=np.array(list(map(float,foot)));P=np.array([float(u),float(v)])
    direction=np.array([1.,float(m)]);direction/=np.linalg.norm(direction)
    normal=(P-Q)/np.linalg.norm(P-Q);distance=np.linalg.norm(P-Q)
    length=max(3.,distance*.85);mark=min(.38,distance*.13)
    fig,ax=plt.subplots(figsize=(5.4,4.2),dpi=120)
    ends=np.array([Q-length*direction,Q+length*direction])
    ax.plot(ends[:,0],ends[:,1],color='#2776b9',lw=1.7)
    ax.plot([Q[0],P[0]],[Q[1],P[1]],color='black',lw=.8,linestyle=(0,(5,5)))
    ax.add_patch(Polygon([Q,Q+mark*direction,Q+mark*(direction+normal),Q+mark*normal],color='#f4cf78',zorder=2))
    ax.scatter(*Q,s=15,color='#2776b9',zorder=3);ax.scatter(*P,s=22,color='red',zorder=3)
    ax.annotate('$(?,?)$',Q,xytext=tuple(-14*np.sign(normal)),textcoords='offset points',ha='right' if normal[0]>0 else 'left',va='top' if normal[1]>0 else 'bottom',fontsize=12)
    ax.annotate('$'+pairtex((u,v))+'$',P,xytext=tuple(11*np.sign(normal)),textcoords='offset points',ha='left' if normal[0]>0 else 'right',va='bottom' if normal[1]>0 else 'top',fontsize=12)
    label=Q+.63*length*direction-.25*normal
    ax.text(*label,'$'+eq+'$',ha='center',va='center',fontsize=11,rotation=float(np.degrees(np.arctan(float(m)))),rotation_mode='anchor',bbox={'facecolor':'white','edgecolor':'none','pad':2})
    allp=np.vstack([ends,P]);low=allp.min(axis=0);high=allp.max(axis=0);pad=max(1.,distance*.3)
    ax.set_xlim(low[0]-pad,high[0]+pad);ax.set_ylim(low[1]-pad,high[1]+pad);ax.set_aspect('equal');ax.axis('off')
    fig.subplots_adjust(left=.04,right=.96,bottom=.04,top=.96)
    output_dir=Path(output_dir);output_dir.mkdir(parents=True,exist_ok=True)
    path=output_dir/(s+'-t'+str(t)+'.png');fig.savefig(path,facecolor='white',metadata={'Software':VERSION});plt.close(fig)
    return path
def solution(s,t):
    old=sources()[s]
    if t==0:return old[':question/worked-solution']
    A,B,C,u,v,m,b,n,d,foot,eq=instance(s,t);r,z=foot
    start=''
    if not printed(old)[5].startswith('y='):
        start=f'First, we rewrite the equation of the given line in slope-intercept form:\n\n$$\n\\begin{{aligned}}{tex(A*x+B*y)} &= {tex(C)} \\\\ {tex(B*y)} &= {tex(C-A*x)} \\\\ y &= {tex(m*x+b)}\\end{{aligned}}\n$$\n\nNext, '
    else:start='First, '
    return start+f"we find the equation of the line that's perpendicular to $y={tex(m*x+b)}$ and passes through the point ${pairtex((u,v))}.$\n\nThe given line has a slope of ${tex(m)},$ so our perpendicular line must have a slope of ${tex(n)}.$\n\nUsing point-slope form and simplifying, we obtain the equation of the perpendicular line:\n\n$$\n\\begin{{aligned}}y-y_1 &= m(x-x_1) \\\\ y-({tex(v)}) &= {tex(n)}(x-({tex(u)})) \\\\ y-({tex(v)}) &= {tex(n*(x-u))} \\\\ y &= {tex(n*x+d)}\\end{{aligned}}\n$$\n\nWe now find the point where the two lines intersect. To do this, we solve the following system of equations:\n\n$$\n\\begin{{cases}}y={tex(m*x+b)} \\\\ y={tex(n*x+d)}\\end{{cases}}\n$$\n\nWe can solve this system by putting the two equations equal to one another and solving for $x.$ This gives\n\n$$\n\\begin{{aligned}}{tex(m*x+b)} &= {tex(n*x+d)} \\\\ {tex((m-n)*x)} &= {tex(d-b)} \\\\ x &= {tex(r)}\\end{{aligned}}\n$$\n\nSubstituting $x={tex(r)}$ into either of the two equations gives $y={tex(z)}.$ So, our solution is $x={tex(r)}$ and $y={tex(z)}.$ Therefore, the lines intersect at the point ${pairtex(foot)}.$\n\nTherefore, we conclude that the point on the line ${eq}$ that is closest to the point ${pairtex((u,v))}$ is ${pairtex(foot)}.$"
def generate(level,seed=0,template=None,parameters=None):
    if level not in ('easy','moderate'):raise ValueError('Hard unsupported: no source evidence or validated hard template')
    src=sources();eligible=[s for s,q in src.items() if q[':question/difficulty'][':db/ident']==':question.difficulty/'+level]
    s=template or random.Random(seed).choice(eligible);p=parameters if parameters is not None else {'t':random.Random(seed).randint(-4,4)}
    if s not in eligible or set(p)!={'t'} or type(p['t'])!=int or not -4<=p['t']<=4:raise ValueError('Outside bounded capability')
    t=p['t'];old=src[s];f=old[':question/answer-fields'][0];A,B,C,u,v,m,b,n,d,foot,eq=instance(s,t)
    prompt=old[':question/problem'];old_eq=printed(old)[5]
    prompt=prompt.replace('$'+old_eq+'$','$'+eq+'$')
    prompt=re.sub(r'closest to the point \$\([^)]*\)',lambda _: 'closest to the point $'+pairtex((u,v)),prompt)
    if t==0:prompt=old[':question/problem']
    else:prompt=re.sub(r'!\[\]\([^)]*\)',lambda _: '![]('+str(render_plot(s,t,HERE/'plots').relative_to(HERE.parent.parent.parent))+')',prompt)
    values=[a[':answer/value'] if t==0 else pairtex((pair(a[':answer/value'])[0],pair(a[':answer/value'])[1]+t)) for a in f[':answer-field/choices']]
    correct=[i for i,z in enumerate(values) if pair(z)==foot]
    if len(correct)!=1 or len(set(map(pair,values)))!=5:raise ValueError('Invalid complete bank')
    fp=digest([str(z) for z in (A/(A if A else B),B/(A if A else B),C/(A if A else B),u,v)])
    qid=str(uuid.uuid5(uuid.UUID(KP_UUID),'task:'+fp));fid=str(uuid.uuid5(uuid.UUID(qid),'field:'+f[':answer-field/key']))
    answers=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),'value:'+z)),':answer/type':':answer.type/math',':answer/value':z} for z in values]
    q={':question/id':qid,':question/problem':prompt,':question/worked-solution':solution(s,t),':question/difficulty':':question.difficulty/'+level,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':f[':answer-field/key'],':answer-field/type':':answer-field.type/radio',':answer-field/correct':[':answer/id',answers[correct[0]][':answer/id']],':answer-field/choices':answers}]}
    import matplotlib
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'template':s,'parameters':p,'source_basis':json.loads((HERE/'source.json').read_text())['basis'],'source_question':s,'bank_profile':s,'mathematical_fingerprint':fp,'domain':'real coordinates; fixed nonzero slope; vertical translation integer -4..4','dependencies':{'sympy':sp.__version__,'matplotlib':matplotlib.__version__},'solution_origin':'exact source at t=0; original instructional sentences and sequence with normalized algebra rows for variants'}}
def candidates(level):
    for s,q in sources().items():
        if q[':question/difficulty'][':db/ident']==':question.difficulty/'+level:
            for t in range(-4,5):yield s,{'t':t}
def batch(level,count,seed):
    if level not in ('easy','moderate'):raise ValueError('Unsupported difficulty')
    if type(count)!=int or count<1:raise ValueError('Positive count required')
    ps=list(candidates(level));random.Random(seed).shuffle(ps)
    if count>len(ps):raise ValueError(f'Finite capacity {len(ps)}; requested {count}')
    return [generate(level,seed,s,p) for s,p in ps[:count]]
def markdown(r):
    q=r['question'];return q[':question/problem']+'\n\n'+'\n'.join(a[':answer/value'] for a in q[':question/answer-fields'][0][':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--difficulty',required=True);a.add_argument('--count',type=int,default=1);a.add_argument('--seed',type=int,default=0);a.add_argument('--format',choices=['json','markdown'],default='json');o=a.parse_args();rs=batch(o.difficulty,o.count,o.seed);print(json.dumps(rs,indent=2) if o.format=='json' else '\n\n'.join(map(markdown,rs)))
