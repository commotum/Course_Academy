#!/usr/bin/env python3
"""QI Pythagorean-identity radio generator. No database operations.

Bounded sampling and complete source-bank profiles are documented in the
adjacent package. Seeds choose mathematics; identities do not use seeds.
"""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import random
import re
import sys
import uuid

os.environ.setdefault('MPLCONFIGDIR', '/tmp/ca-17592186110755-mpl')
if __name__ == '__main__':
    try:
        import sympy
        import matplotlib
    except ModuleNotFoundError:
        # The application's worker uses system Python; use the existing project
        # environment rather than installing or changing application code.
        runtime = Path(__file__).resolve().parents[2]/'.venv/bin/python'
        os.execv(str(runtime), [str(runtime), str(Path(__file__).resolve()), *sys.argv[1:]])

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge
import sympy as s

HERE = Path(__file__).with_suffix('')
ROOT = HERE.parents[2]
KP_ID = 17592186110755
KP_UUID = '3c73db44-2ec2-5025-9431-acb02e414916'
GENERATOR_UUID = str(uuid.uuid5(uuid.UUID(KP_UUID), 'pythagorean-identity-generator'))
VERSION = 'qi-pythagorean-radio-v1'
SUPPORTED_LEVELS = ('easy', 'moderate')
DEFAULTS = {
    'q-124625': {'m':6, 'n':7},
    'q-37899': {'m':3, 'n':7},
    'q-64681': {'m':1, 'n':2},
    'q-65059': {'m':5, 'n':9},
    'q-37915': {'a':10, 'b':4},
}
CAPTURE = json.loads((HERE/'source.json').read_text())
SOURCES = {q[':question/math-academy-id']:q for q in CAPTURE['record'][':knowledge-point/questions']}

def tex(x):
    return s.latex(s.simplify(x)).replace(' ', '')

def frac(a,b):
    return rf'\frac{{{a}}}{{{b}}}'

def values(template,p):
    """A complete profile is selected before any options are constructed."""
    if template == 'q-37915':
        a,b=p['a'],p['b']
        if not (3<=b<=9 and 1<a<b*b and s.mobius(a)!=0):
            raise ValueError('Moderate requires an interior squarefree radicand')
        given=s.sqrt(a)/b; squared=s.Rational(a,b*b); correct=2*(1-squared)
        bank=[correct/2,correct,1/correct,correct/squared,2*correct]
        return given,correct,list(map(s.simplify,bank))
    m,n=p['m'],p['n']
    if not (2<=n<=12 and 0<m<n and math.gcd(m,n)==1):
        raise ValueError('Easy requires a reduced positive interior ratio')
    D=n*n-m*m; given=s.Rational(m,n); correct=s.sqrt(D)/n
    if template=='q-124625':
        if D<=10:raise ValueError('Offset-radicand profile requires D>10')
        bank=[-s.sqrt(D-10)/n,s.sqrt(D-8)/n,-s.sqrt(D-3)/n,s.Rational(1,n),correct]
    elif template=='q-37899':
        bank=[s.Rational(m+1,n),correct,correct/2,correct/s.sqrt(8),given]
    elif template=='q-64681':
        bank=[-given,-correct,correct,correct**2,given]
    elif template=='q-65059':
        bank=[s.Rational(D-1,n),s.Rational(m-1,n),s.Rational(D,n*n),correct,s.Rational(D,n)]
    else:raise ValueError('Unknown source profile')
    return given,correct,list(map(s.simplify,bank))

def valid(template,p):
    try:
        _,correct,bank=values(template,p)
        return all(v.is_real is True for v in bank) and len(set(bank))==5 and sum(s.simplify(v-correct)==0 for v in bank)==1
    except ValueError:return False

def domain(template):
    if template=='q-37915':
        return [{'a':a,'b':b} for b in range(3,10) for a in range(2,b*b) if valid(template,{'a':a,'b':b})]
    return [{'m':m,'n':n} for n in range(2,13) for m in range(1,n) if valid(template,{'m':m,'n':n})]

def render_plots(template,p,output_dir):
    """Both pictures derive from the same exact first-quadrant point."""
    given,_,_=values(template,p)
    if template=='q-37915':y=given;x=s.sqrt(1-y*y)
    else:x=given;y=s.sqrt(1-x*x)
    x,y=float(x),float(y);angle=math.degrees(math.atan2(y,x))
    output_dir=Path(output_dir);output_dir.mkdir(parents=True,exist_ok=True)
    out={}
    for role in ('prompt','solution'):
        token=json.dumps({'template':template,'parameters':p,'role':role,'version':VERSION},sort_keys=True)
        name=hashlib.sha256(token.encode()).hexdigest()+'.png';path=output_dir/name
        if not path.exists():
            fig,ax=plt.subplots(figsize=(4.6,4.6),dpi=140)
            ax.set_aspect('equal');ax.set_xlim(-1.35,1.6);ax.set_ylim(-1.35,1.4)
            ax.set_xticks([-1,0,1]);ax.set_yticks([-1,0,1]);ax.set_xticklabels([]);ax.set_yticklabels([])
            ax.grid(color='#c7c7c7',linewidth=.6);ax.tick_params(length=0)
            for spine in ax.spines.values():spine.set_visible(False)
            ax.annotate('',xy=(1.36,0),xytext=(-1.3,0),arrowprops={'arrowstyle':'->','color':'black','lw':1.3})
            ax.annotate('',xy=(0,1.34),xytext=(0,-1.3),arrowprops={'arrowstyle':'->','color':'black','lw':1.3})
            t=[2*math.pi*i/400 for i in range(401)]
            ax.plot([math.cos(v) for v in t],[math.sin(v) for v in t],color='#2878b5',lw=1.5)
            ax.add_patch(Wedge((0,0),.26,0,angle,color='#e5ac00'))
            ax.plot([0,x],[0,y],color='black',lw=1.4);ax.plot(x,y,'ko',markersize=3)
            label=r'$P$' if role=='prompt' else r'$P(\cos\theta,\sin\theta)$'
            # Above the point avoids the axes and circle, even near their endpoints.
            ax.text(x+.035,y+.075,label,fontsize=10,ha='left',va='bottom')
            ax.text(.35*math.cos(math.radians(angle/2)),.35*math.sin(math.radians(angle/2)),r'$\theta$',fontsize=10)
            for n in (-1,1):
                ax.text(n,-.08,str(n),fontsize=9,ha='center',va='top')
                ax.text(-.07,n,str(n),fontsize=9,ha='right',va='center')
            ax.text(1.41,-.035,r'$x$',fontsize=11);ax.text(.04,1.35,r'$y$',fontsize=11)
            fig.subplots_adjust(left=.03,right=.98,bottom=.03,top=.98)
            fig.savefig(path,facecolor='white',metadata={'Software':VERSION});plt.close(fig)
        out[role]={'path':str(path.relative_to(ROOT)), 'sha256':hashlib.sha256(path.read_bytes()).hexdigest(), 'point':[str(s.sqrt(1-given*given)) if template=='q-37915' else str(given),str(given) if template=='q-37915' else str(s.sqrt(1-given*given))], 'renderer':'matplotlib','dimensions':[644,644]}
    return out

def replacements(template,p):
    old=DEFAULTS[template]
    if template=='q-37915':
        a,b=p['a'],p['b'];A,B=old['a'],old['b']
        return {tex(s.sqrt(A)/B):tex(s.sqrt(a)/b),frac(A,B*B):frac(a,b*b),frac(2*A,B*B):frac(2*a,b*b),tex(2*(1-s.Rational(A,B*B))):tex(2*(1-s.Rational(a,b*b)))}
    m,n=p['m'],p['n'];M,N=old['m'],old['n'];D=n*n-m*m;OD=N*N-M*M
    return {frac(M,N):frac(m,n),frac(M*M,N*N):frac(m*m,n*n),frac(OD,N*N):frac(D,n*n),tex(s.sqrt(OD)/N):tex(s.sqrt(D)/n)}

def render(template,p,replay=False):
    source=SOURCES[template];mapping=replacements(template,p)
    pattern=re.compile('|'.join(re.escape(k) for k in sorted(mapping,key=len,reverse=True)))
    texts={key:pattern.sub(lambda m:mapping[m[0]],source[key]) for key in (':question/problem',':question/worked-solution')}
    assets={}
    if not replay:
        assets=render_plots(template,p,HERE/'assets')
        for key,role in ((':question/problem','prompt'),(':question/worked-solution','solution')):
            texts[key]=re.sub(r'!\[\]\([^)]+\)', '![]('+assets[role]['path']+')',texts[key])
    return texts,assets

def generate(difficulty,seed=0,template=None,parameters=None,bank_profile=None,replay=False):
    if difficulty not in SUPPORTED_LEVELS:raise ValueError('Unsupported difficulty: '+difficulty)
    rng=random.Random(seed)
    eligible=[m for m in DEFAULTS if (m=='q-37915')==(difficulty=='moderate')]
    template=template or rng.choice(eligible)
    if template not in eligible or bank_profile not in (None,template):raise ValueError('Ineligible source profile')
    p=dict(parameters or rng.choice(domain(template)))
    if not valid(template,p):raise ValueError('Invalid or colliding complete bank')
    given,correct,bank=values(template,p);texts,assets=render(template,p,replay)
    identity=json.dumps({'version':VERSION,'template':template,'parameters':p,'bank':[str(v) for v in bank]},sort_keys=True)
    qid=str(uuid.uuid5(uuid.UUID(GENERATOR_UUID),identity));fid=str(uuid.uuid5(uuid.UUID(qid),'selection'))
    answers=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),tex(v))),':answer/type':':answer.type/math',':answer/value':tex(v)} for v in bank]
    correct_id=next(a[':answer/id'] for a,v in zip(answers,bank) if s.simplify(v-correct)==0)
    return {'question':{':question/id':qid,**texts,':question/difficulty':':question.difficulty/'+difficulty,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct_id]}]},'knowledge_point':{'id':KP_UUID,'db_id':KP_ID,'title':CAPTURE['record'][':knowledge-point/title']},'generation':{'generator_id':GENERATOR_UUID,'version':VERSION,'seed':seed,'template':template,'bank_profile':template,'parameters':p,'domain':'first quadrant; exact unit circle; bounded integer slots','source_question_ids':[SOURCES[template][':question/id']], 'source_basis':CAPTURE['basis'],'dependencies':{'sympy':s.__version__,'matplotlib':matplotlib.__version__},'assets':assets,'source_replay':replay}}

def batch(difficulty,count,seed=0):
    if difficulty not in SUPPORTED_LEVELS:raise ValueError('Unsupported difficulty: '+difficulty)
    if count<=0:return []
    templates=[m for m in DEFAULTS if (m=='q-37915')==(difficulty=='moderate')]
    candidates=[(m,p) for m in templates for p in domain(m)]
    random.Random(seed).shuffle(candidates);seen=set();out=[]
    for m,p in candidates:
        task=('y-squared-cos',s.Rational(p['a'],p['b']**2)) if m=='q-37915' else ('x-sin',s.Rational(p['m'],p['n']))
        if task in seen:continue
        seen.add(task);out.append(generate(difficulty,seed,m,p))
        if len(out)>=count:break
    return out

def markdown(rec):
    q=rec['question'];f=q[':question/answer-fields'][0]
    return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$'+(' (correct)' if a[':answer/id']==f[':answer-field/correct'][1] else '') for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--difficulty',choices=SUPPORTED_LEVELS,required=True);parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=1);parser.add_argument('--output',type=Path);parser.add_argument('--format',choices=('json','markdown'),default='json')
    args=parser.parse_args();records=batch(args.difficulty,args.count,args.seed)
    rendered=json.dumps(records,indent=2)+'\n' if args.format=='json' else '\n\n---\n\n'.join(map(markdown,records))
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(rendered);args.output.with_suffix('.md').write_text('\n\n---\n\n'.join(map(markdown,records)))
    else:print(rendered,end='')
