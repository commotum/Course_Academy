"""Moderate position-vector magnitudes. Finite, source-bank-preserving scale extension.
Only scales 1..4, same integer coordinates and five-choice field shape as evidence.
Math Academy source records remain untouched. Seed/order never creates a new task.
"""
import argparse, hashlib, json, os, random, sys, uuid
from pathlib import Path
os.environ.setdefault('MPLCONFIGDIR','/tmp/course-academy-mpl-17592186059715')
try:
    import sympy as sp
except ModuleNotFoundError:
    if sys.executable != str(Path(__file__).resolve().parents[2]/'.venv/bin/python'):
        os.execv(str(Path(__file__).resolve().parents[2]/'.venv/bin/python'),[str(Path(__file__).resolve().parents[2]/'.venv/bin/python'),__file__,*sys.argv[1:]])
    raise
KP_ID=17592186059715
KP_UUID='7bc170fa-a70e-55af-8f3e-f4ea07431e30'
GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),'question-generator'))
SUPPORTED_LEVELS=('moderate',)
VERSION='position-magnitude-source-scale-1'
HERE=Path(__file__).with_suffix('')
ROOT=HERE.parents[2]
SPECS={
 'q-18051':{'labels':['A','B'],'points':[[-4,1],[3,0]],'values':[r'5\sqrt{2}','6',r'5\sqrt{3}',r'3\sqrt{2}','5'],'correct':0},
 'q-18052':{'labels':['P','Q'],'points':[[-2,2],[3,3]],'values':[r'\sqrt{27}',r'\sqrt{23}','8','5',r'\sqrt{26}'],'correct':4},
}

def expression(v):
    import re
    m=re.fullmatch(r'(\d*)\\sqrt\{(\d+)\}',v)
    return sp.Integer(m[1] or 1)*sp.sqrt(int(m[2])) if m else sp.Integer(v)

def fingerprint_squared(n):return hashlib.sha256(('squared-distance:'+str(n)).encode()).hexdigest()

def vector(x,y):
    v=sp.latex(x*sp.Symbol('i')+y*sp.Symbol('j'))
    return v

def render_plots(profile,scale):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    spec=SPECS[profile];pts=[[scale*x,scale*y] for x,y in spec['points']]
    fig,ax=plt.subplots(figsize=(4.6,3.6),dpi=100)
    xs=[0]+[p[0] for p in pts];ys=[0]+[p[1] for p in pts]
    lo=min(xs+ys)-scale;hi=max(xs+ys)+scale
    ax.set_xlim(min(xs)-1.7*scale,max(xs)+1.7*scale)
    ax.set_ylim(min(ys)-1.4*scale,max(ys)+1.4*scale)
    ax.set_aspect('equal',adjustable='box');ax.axis('off')
    xl=ax.get_xlim();yl=ax.get_ylim()
    ax.annotate('',xy=(xl[1],0),xytext=(xl[0],0),arrowprops={'arrowstyle':'->','color':'black'})
    ax.annotate('',xy=(0,yl[1]),xytext=(0,yl[0]),arrowprops={'arrowstyle':'->','color':'black'})
    ax.text(xl[1],-.35*scale,'$x$',ha='right');ax.text(.15*scale,yl[1],'$y$',va='top')
    ax.text(-.3*scale,-.3*scale,'$O$',ha='right',va='top')
    for label,(x,y) in zip(spec['labels'],pts):
        ax.annotate('',xy=(x,y),xytext=(0,0),arrowprops={'arrowstyle':'->','color':'#2876b9','lw':1.8})
        ax.plot(x,y,'.',color='#2876b9')
        ax.annotate(f'${label}({x},{y})$',(x,y),xytext=(5,8 if y>=0 else -15),textcoords='offset points',fontsize=10)
        ax.text(x*.55+.15*scale,y*.55+.2*scale,'$'+label.lower()+'$',color='#2876b9')
    if profile=='q-18052':
        ax.annotate('',xy=pts[1],xytext=pts[0],arrowprops={'arrowstyle':'->','color':'#e69800','lw':1.6})
    for end,name in [((1,0),'i'),((0,1),'j')]:
        ax.annotate('',xy=end,xytext=(0,0),arrowprops={'arrowstyle':'->','color':'#d96a28','lw':1.1})
        ax.annotate('$'+name+'$',end,xytext=(6,-14) if name=='i' else (5,10),textcoords='offset points',color='#d96a28',fontsize=9)
    fig.tight_layout(pad=.6)
    directory=HERE/'plots';directory.mkdir(parents=True,exist_ok=True)
    path=directory/(profile+'-'+str(scale)+'.png')
    fig.savefig(path,metadata={'Software':VERSION});plt.close(fig)
    digest=hashlib.sha256(path.read_bytes()).hexdigest()
    relative='images/'+digest[:2]+'/'+digest+'.png'
    return {'path':str(path.relative_to(ROOT)),'reference':relative,'sha256':digest,'role':'prompt','points':pts,'renderer':'matplotlib','dimensions':[460,360]}

def generate_profile(profile,scale,seed=0):
    assert profile in SPECS and isinstance(scale,int) and 1<=scale<=4
    spec=SPECS[profile];p,q=[[scale*x,scale*y] for x,y in spec['points']]
    dx,dy=q[0]-p[0],q[1]-p[1];n=dx*dx+dy*dy
    fp=fingerprint_squared(n)
    qid=str(uuid.uuid5(uuid.UUID(KP_UUID),VERSION+':'+profile+':'+str(scale)))
    fid=str(uuid.uuid5(uuid.UUID(qid),'field:selection'))
    answers=[]
    for i,v in enumerate(spec['values']):
        value=v if scale==1 else sp.latex(scale*expression(v))
        answers.append({':answer/id':str(uuid.uuid5(uuid.UUID(fid),'recipe:'+str(i))),':answer/type':':answer.type/math',':answer/value':value})
    a,b=spec['labels'];low_a=a.lower();low_b=b.lower();asset=render_plots(profile,scale)
    problem=f"![]({asset['reference']})\n\nLet ${a}({p[0]}, {p[1]})$ and ${b}({q[0]}, {q[1]})$. Find $|\\overrightarrow{{{a+b}}}|$."
    solution=(f"We have\n\n$$\n\\begin{{aligned}}\n\\overrightarrow{{O{a}}} &= {low_a} = {vector(*p)}, \\\\\n\\overrightarrow{{O{b}}} &= {low_b} = {vector(*q)}.\n\\end{{aligned}}\n$$\n\n"
      f"Expressing $\\overrightarrow{{{a+b}}}$ as the difference of position vectors, we obtain:\n\n$$\n\\begin{{aligned}}\n\\overrightarrow{{{a+b}}} &= \\overrightarrow{{O{b}}} - \\overrightarrow{{O{a}}} \\\\\n&= {low_b} - {low_a} \\\\\n&= ({vector(*q)}) - ({vector(*p)}) \\\\\n&= {vector(dx,dy)}\n\\end{{aligned}}\n$$\n\n"
      f"Now, using the formula for the magnitude of a vector, we get\n\n$$\n\\begin{{aligned}}\n|\\overrightarrow{{{a+b}}}| &= \\sqrt{{({dx})^{{2}} + ({dy})^{{2}}}} \\\\\n&= \\sqrt{{{dx*dx} + {dy*dy}}} \\\\\n&= \\sqrt{{{n}}} \\\\\n&= {sp.latex(sp.sqrt(n))}\n\\end{{aligned}}\n$$")
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':'Calculating a Vector From Position Vectors and then Computing its Magnitude'},
      'question':{':question/id':qid,':question/problem':problem,':question/worked-solution':solution,':question/requires-calculator':False,':question/difficulty':':question.difficulty/moderate',':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/correct':[':answer/id',answers[spec['correct']][':answer/id']],':answer-field/choices':answers}]},
      'generation':{'version':VERSION,'template':profile,'bank_profile':profile,'parameters':{'scale':scale,'points':[p,q],'displacement':[dx,dy],'squared_distance':n},'seed':seed,'source_ids':[profile],'parameter_fingerprint':fp,'eligible_for_learning':True,'authored_completion':'Source key, worked solution and moderate rating; complete bank scales homogeneously. Original records untouched.','domains':'Integer coordinates; scale in {1,2,3,4}; distinct endpoints','dependencies':{'sympy':sp.__version__},'assets':[asset]}}

def batch(difficulty,count,seed):
    if difficulty not in SUPPORTED_LEVELS:raise ValueError('Unsupported difficulty: '+difficulty)
    keys=[(p,s) for p in SPECS for s in range(1,5)];random.Random(seed).shuffle(keys)
    return [generate_profile(p,s,seed) for p,s in keys[:min(count,len(keys))]]

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--difficulty',default='moderate');parser.add_argument('--count',type=int,default=5);parser.add_argument('--seed',type=int,default=0);parser.add_argument('--format',choices=['json','markdown'],default='json');args=parser.parse_args()
    if args.count<1:parser.error('count must be positive')
    records=batch(args.difficulty,args.count,args.seed)
    print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(r['question'][':question/problem']+'\n\n'+r['question'][':question/worked-solution'] for r in records))
