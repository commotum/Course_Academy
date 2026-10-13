"""Point-on-line source templates; exact replay, bounded integer sampling and plots.

Easy: positive slope, three integer points, A and C satisfy the equation.
Moderate: negative slope, signed coordinates, only C satisfies the equation.
These bounds are intentionally narrower than arbitrary linear equations. Hard
is unsupported: no source establishes a harder response or solution sequence.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import random
import re
import sys
import uuid
os.environ.setdefault('MPLCONFIGDIR', '/tmp/course-academy-mpl')
try:
    import matplotlib
    import sympy as s
except ModuleNotFoundError:
    runtime=Path(__file__).resolve().parents[2]/'.venv/bin/python'
    if __name__=='__main__' and runtime.is_file() and Path(sys.prefix).resolve()!=runtime.parent.parent.resolve():
        os.execv(str(runtime),[str(runtime),str(Path(__file__).resolve()),*sys.argv[1:]])
    raise
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE = Path(__file__).with_suffix('')
KP_ID = 17592186054676
KP_UUID = '3123f8ed-a1ca-52b7-8427-2f3b60d9e68a'
GENERATOR_UUID = str(uuid.uuid5(uuid.UUID(KP_UUID), 'point-on-line-generator'))
VERSION = '1.0.0'
SUPPORTED_LEVELS = ('easy', 'moderate')
SOURCES = {q[':question/math-academy-id']:q for q in json.loads((HERE/'reference/source.json').read_text())['record'][':knowledge-point/questions']}
DEFAULTS = {'q-71829':{'m':4,'b':2,'points':[[-1,-2],[0,1],[1,6]]},
            'q-102142':{'m':-5,'b':6,'points':[[0,5],[1,2],[2,-4]]}}
TEMPLATES = {'easy':'q-71829', 'moderate':'q-102142'}

def equation(p):
    m,b=p['m'],p['b']
    coefficient='' if m==1 else '-' if m==-1 else str(m)
    return coefficient+'x'+('+'+str(b) if b>0 else str(b) if b<0 else '')

def sample(level, rng):
    while True:
        m=rng.choice([1,2,3,4]) if level=='easy' else rng.choice([-2,-3,-4,-5])
        b=rng.randint(-4,6);xs=sorted(rng.sample(range(-3,4),3));points=[]
        for i,x in enumerate(xs):
            delta=0 if (i in (0,2) if level=='easy' else i==2) else rng.choice([-2,-1,1,2])
            points.append([x,m*x+b+delta])
        if all(-10<=y<=10 for x,y in points):
            return {'m':m,'b':b,'points':points}

def render_plots(p, output_dir):
    """Coordinates, ticks and labels all use the same exact question data."""
    output_dir=Path(output_dir);output_dir.mkdir(parents=True,exist_ok=True)
    key=hashlib.sha256(json.dumps(p,sort_keys=True).encode()).hexdigest()
    target=output_dir/(key+'.png')
    xs,ys=zip(*p['points']);lo=min(-2,*xs)-1;hi=max(2,*xs)+2
    bottom=min(-2,*ys)-1;top=max(2,*ys)+2
    fig,ax=plt.subplots(figsize=(4.5,4.5),dpi=120)
    ax.set_xlim(lo,hi);ax.set_ylim(bottom,top);ax.set_aspect('equal')
    ax.set_xticks(range(lo,hi+1));ax.set_yticks(range(bottom,top+1))
    ax.grid(color='#c8c8c8',linewidth=.65);ax.set_axisbelow(True)
    for name in ('left','bottom'):ax.spines[name].set_position('zero')
    for name in ('right','top'):ax.spines[name].set_visible(False)
    ax.tick_params(labelsize=8,length=2)
    ax.annotate('',xy=(hi,0),xytext=(lo,0),arrowprops={'arrowstyle':'->','color':'black'})
    ax.annotate('',xy=(0,top),xytext=(0,bottom),arrowprops={'arrowstyle':'->','color':'black'})
    ax.text(hi-.2,.4,'x',fontsize=11);ax.text(.3,top-.3,'y',fontsize=11)
    for label,(x,y) in zip('ABC',p['points']):
        ax.plot(x,y,'o',color='red',markersize=4)
        ax.annotate(label,(x,y),xytext=(-14 if x<0 else 6,6),textcoords='offset points',fontsize=11)
    fig.tight_layout(pad=1);fig.savefig(target,metadata={'Software':'Course Academy point-on-line v1'});plt.close(fig)
    return target

def generate(level, seed=0, template=None, parameters=None, bank_profile=None, output_dir=None):
    if level not in SUPPORTED_LEVELS:raise ValueError('Unsupported level: '+level)
    template=template or TEMPLATES[level];assert template==TEMPLATES[level]
    profile=template+'-complete-bank';assert bank_profile in (None,profile)
    p=parameters if parameters is not None else sample(level,random.Random(seed))
    assert isinstance(p['m'],int) and p['m']!=0 and isinstance(p['b'],int)
    assert len(p['points'])==3 and len({tuple(v) for v in p['points']})==3
    truth=[s.Integer(y)==s.Integer(p['m'])*x+p['b'] for x,y in p['points']]
    assert truth==([True,False,True] if level=='easy' else [False,False,True])
    old=SOURCES[template];eq=equation(p);old_eq=equation(DEFAULTS[template])
    # Source image is reused only at exact source parameters; variants render it.
    if p==DEFAULTS[template]:asset=re.search(r'!\[\]\((.*?)\)',old[':question/problem'])[1]
    else:asset=str(render_plots(p,output_dir or HERE/'assets'))
    prompt=re.sub(r'!\[\]\(.*?\)',lambda _: '![]('+asset+')',old[':question/problem'])
    prompt=prompt.replace(old_eq,eq)
    solution=old[':question/worked-solution']
    # Keep the authored coordinate-list layout and each instructional sentence.
    for label,(x,y),(ox,oy) in zip('ABC',p['points'],DEFAULTS[template]['points']):
        solution=solution.replace(label+'('+str(ox)+','+str(oy)+')',label+'('+str(x)+','+str(y)+')')
    blocks=iter(zip(p['points'],truth))
    def replace_block(match):
        (x,y),ok=next(blocks);rhs=str(p['m'])+'('+str(x)+')'+('+'+str(p['b']) if p['b']>=0 else str(p['b']))
        value=p['m']*x+p['b'];mark='✓' if ok else r'\times '
        return r'\begin{aligned}y & ='+eq+r' \\ ('+str(y)+') & ='+rhs+r' \\ '+str(y)+' & ='+str(value)+r'\,'+mark+r'\end{aligned}'
    solution=re.sub(r'\\begin\{aligned\}.*?\\end\{aligned\}',replace_block,solution,flags=re.S)
    task=json.dumps({'equation':[p['m'],p['b']],'points':p['points'],'response':'point-subset'},sort_keys=True)
    qid=str(uuid.uuid5(uuid.UUID(KP_UUID),task))
    fid=str(uuid.uuid5(uuid.UUID(qid),'selection'))
    oldf=old[':question/answer-fields'][0];values=sorted(a[':answer/value'] for a in oldf[':answer-field/choices'])
    answers=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),value)),':answer/type':':answer.type/text',':answer/value':value} for value in values]
    correct=oldf[':answer-field/correct'][':answer/value']
    field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',next(a[':answer/id'] for a in answers if a[':answer/value']==correct)]}
    return {'knowledge_point':{'id':KP_UUID,'title':'Identifying Points That Lie on a Line'},'question':{':question/id':qid,':question/problem':prompt,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+level,':question/answer-fields':[field]},'generation':{'version':VERSION,'generator_id':GENERATOR_UUID,'template':template,'source_question':old[':question/id'],'source_basis':2027,'bank_profile':profile,'seed':seed,'parameters':p,'domain':'integer coordinates; nonzero integer slope','task_fingerprint':hashlib.sha256(task.encode()).hexdigest(),'dependencies':{'sympy':s.__version__,'matplotlib':matplotlib.__version__},'plot_renderer':'Matplotlib','plot_path':asset}}

def batch(level,count=20,seed=0):
    result=[];seen=set()
    for i in range(count*10):
        r=generate(level,seed+i);key=r['generation']['task_fingerprint']
        if key not in seen:result.append(r);seen.add(key)
        if len(result)==count:return result
    raise ValueError('Bounded sampling exhausted')

def markdown(rec):
    q=rec['question'];f=q[':question/answer-fields'][0]
    return q[':question/problem']+'\n\n'+'\n'.join('- '+a[':answer/value'] for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=SUPPORTED_LEVELS,required=True);ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=('json','markdown'),default='json');ap.add_argument('--output',type=Path)
    args=ap.parse_args();records=batch(args.difficulty,args.count,args.seed)
    output=json.dumps(records,indent=2)+'\n' if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records)
    if args.output:
        args.output.write_text(output)
        if args.format=='json':args.output.with_suffix('.md').write_text('\n\n---\n\n'.join(markdown(r) for r in records))
    else:print(output,end='')
