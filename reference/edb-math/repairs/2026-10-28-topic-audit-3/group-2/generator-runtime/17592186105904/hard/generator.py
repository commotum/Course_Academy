#!/usr/bin/env python3
"""Exact inverse triangle-area practice. Pure seeded construction; no database IO."""
from __future__ import annotations
import argparse, copy, hashlib, itertools, json, math, os, random, uuid
from pathlib import Path
os.environ.setdefault('MPLCONFIGDIR', '/tmp/course-academy-triangle-mpl')
import sympy as sp
import matplotlib
matplotlib.use('Agg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.patches import Wedge
from matplotlib.text import Text
from math_format import normalize_prose, normalize_tex, validate_generated_record
HERE=Path(__file__).resolve().parent
DATA=json.loads((HERE/'source-cases.json').read_text())
KP=DATA['knowledge_point']
VERSION='triangle-area-inverse-8'
NAMESPACE=uuid.UUID(KP['id'])
def digest(v): return hashlib.sha256(json.dumps(v, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
def ident(v): return str(uuid.uuid5(NAMESPACE,str(v)))
def tex(v): return normalize_tex(sp.latex(sp.factor(sp.sympify(v))))
def sine(t): return sp.simplify(sp.sin(sp.pi*t/180))
def display(rows): return '$$\n'+r'\begin{aligned}'+'\n'+(' \\\\\n'.join(rows))+'\n'+r'\end{aligned}'+'\n$$'
def plot(instance, output_dir):
    """Reuse legacy equal-aspect construction, with semantic labels/unknown roles."""
    b,c=map(lambda k:float(sp.sympify(instance[k])),('b','c'))
    t=instance['theta']; unit=instance['unit']; kind=instance['kind']
    labels=instance['labels']; target=instance['target']
    key=digest({k:instance[k] for k in ('b','c','theta','unit','kind','labels','target')})
    out=Path(output_dir);out.mkdir(parents=True,exist_ok=True);path=out/(key+'.png')
    A=(0.,0.);B=(c*math.cos(math.radians(t)),c*math.sin(math.radians(t)));C=(b,0.)
    maxlen=max(b,c);radius=min(b,c)*.18
    fig=Figure(figsize=(5.4,3.7),dpi=150);FigureCanvasAgg(fig);ax=fig.subplots()
    ax.set_aspect('equal');ax.axis('off')
    ax.plot([0,B[0],C[0],0],[0,B[1],0,0],color='#253448',lw=1.8)
    ax.add_patch(Wedge(A,radius,0,t,facecolor='#d9e9f2',edgecolor='#627e92',lw=.7))
    for name,point,off in [(labels[0],A,(-8,-17)),(labels[1],B,(0,14)),(labels[2],C,(12,-5))]:
        ax.annotate(name,point,xytext=off,textcoords='offset points',fontsize=14,fontstyle='italic',ha='center')
    known_c=kind=='angle' or target=='b';known_b=kind=='angle' or target=='c'
    c_label=('$'+tex(instance['c'])+'$ '+unit) if known_c else '$'+labels[0]+labels[1]+'$'
    b_label=('$'+tex(instance['b'])+'$ '+unit) if known_b else '$'+labels[0]+labels[2]+'$'
    ax.annotate(c_label,(B[0]/2,B[1]/2),xytext=(-14,8),textcoords='offset points',ha='right',fontsize=12)
    ax.annotate(b_label,(b/2,0),xytext=(0,-26),textcoords='offset points',ha='center',fontsize=12)
    mid=math.radians(t/2)
    if kind=='side':
        ax.annotate('$'+str(t)+r'^\circ$',A,
                    xytext=(-35,-42),textcoords='offset points',ha='center',fontsize=12,
                    arrowprops={'arrowstyle':'-','linestyle':':','color':'#666','linewidth':.7})
    else:
        ax.text(radius*.7*math.cos(mid),radius*.7*math.sin(mid),'?',ha='center',va='center',fontsize=13)
    ax.set_xlim(min(0,B[0])-.35*maxlen,max(C[0],B[0])+.23*maxlen)
    ax.set_ylim(-.27*maxlen,B[1]+.27*maxlen)
    fig.tight_layout(pad=.5);fig.canvas.draw()
    renderer=fig.canvas.get_renderer()
    bounds=[{'text':text.get_text(),'bbox':list(Text.get_window_extent(text,renderer).bounds)} for text in ax.texts]
    for i,left in enumerate(bounds):
        x,y,width,height=left['bbox']
        for right in bounds[i+1:]:
            u,v,w,h=right['bbox']
            if min(x+width,u+w)>max(x,u) and min(y+height,v+h)>max(y,v):
                raise ValueError('Overlapping diagram labels: '+left['text']+' / '+right['text'])
    fig.savefig(path,facecolor='white')
    return path.name,{'vertices':{labels[0]:A,labels[1]:B,labels[2]:C},'equal_aspect':True,
                     'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                     'label_bounds':bounds,'image_pixels':list(fig.canvas.get_width_height()),
                     'labels':{'b':b_label,'c':c_label,'angle':str(t) if kind=='side' else '?'}}
# These are distinct errors in solving area=k*x*sin(theta)/2. Sample a whole
# bank, so no fixed half/key/double arrangement identifies the answer.
SIDE_PROFILES={'mixed-errors':None}
def side_banks(x,k,s):
    recipes=[('omit half',x/2),('apply half twice',2*x),
             ('omit sine',x*s),('multiply by sine',x*s*s),
             ('divide by sine twice',x/s),('square reciprocal sine',x/(s*s)),
             ('omit known-side division',x*k),('divide by known side twice',x/k),
             ('copy known side',k)]
    errors={}
    for name,v in recipes:
        v=sp.simplify(v)
        if v>0 and v!=x:errors.setdefault(v,name)
    banks=[]
    for selected in itertools.combinations(errors,4):
        values=[x,*selected]
        # A sole middle of a doubling chain is an avoidable bank-only cue.
        if any(v/2 in values and 2*v in values for v in values):continue
        # Integer source answers must not be the sole integer option.
        if x.is_integer and sum(v.is_integer is True for v in values)<2:continue
        banks.append((values,[errors[v] for v in selected]))
    return banks

def angle_bank_arrangements(t):
    same=[25,30,35,40,45,50,60,65,75]
    if t>90:same=[180-a for a in same]
    lower=[a for a in same if a<t];upper=[a for a in same if a>t]
    special={30,45,60} if t<90 else {120,135,150}
    return [(n+1+(5-count if t>90 else 0),count,n)
            for count in (2,3) for n in range(count)
            if n<=len(lower) and count-1-n<=len(upper)
            and ((n>0 and special.intersection(lower)) or
                 (count-1-n>0 and special.intersection(upper)))]
# Explicit complete error banks are chosen before the numbers, not pooled first-valid recipes.
def build(level, seed, instance, profile=None, field_type=None, output_dir=None, position=None, bank_rank=None):
    rng=random.Random(seed);p=copy.deepcopy(instance)
    b,c=sp.sympify(p['b']),sp.sympify(p['c']);t=int(p['theta']);kind=p['kind']
    if b<=0 or c<=0 or t not in (30,45,60,120,135,150): raise ValueError('Positive sides and familiar angles required')
    if kind not in ('side','angle') or p['target'] not in ('b','c','angle'):raise ValueError('Unknown role')
    if (kind=='angle')!=(p['target']=='angle'):raise ValueError('Target and operation disagree')
    p['b'],p['c']=str(b),str(c)
    s=sine(t);area=sp.simplify(b*c*s/2)
    v,u,z=p['labels'];sb=v+z;sc=v+u;unit=p['unit']
    target=sb if p['target']=='b' else sc if p['target']=='c' else v
    x=(b if p['target']=='b' else c) if kind=='side' else sp.Integer(t)
    k=c if p['target']=='b' else b
    ft=field_type or ('radio' if level=='easy' else rng.choice(['radio','blank']))
    profile=profile or ('blank' if ft=='blank' else rng.choice(list(SIDE_PROFILES)) if kind=='side' else 'special-angle-bank')
    if ft=='blank':values=[x]
    elif kind=='side':
        banks=side_banks(x,k,s)
        if bank_rank is not None:
            banks=[a for a in banks if 1+sum(bool(v<x) for v in a[0])==bank_rank]
        if not banks:raise ValueError('Complete bank collision')
        values,error_labels=rng.choice(banks)
    else:
        # Source-supported recognition bank: imported alternatives include 25,35,40,
        # 50,65,75 degrees. Supplements extend the same branch-recognition errors.
        acute=[25,30,35,40,45,50,60,65,75]
        same=acute if t<90 else [180-a for a in acute]
        other=[180-a for a in same]
        arrangements=angle_bank_arrangements(t)
        if bank_rank is not None:arrangements=[a for a in arrangements if a[0]==bank_rank]
        rank,same_count,lower_count=rng.choice(arrangements)
        below=[a for a in same if a<t];above=[a for a in same if a>t]
        same_banks=[list(a)+list(b) for a in itertools.combinations(below,lower_count)
                    for b in itertools.combinations(above,same_count-1-lower_count)
                    if ({30,45,60} if t<90 else {120,135,150}).intersection(list(a)+list(b))]
        values=list(map(sp.Integer,[t]+rng.choice(same_banks)+rng.sample(other,5-same_count)))
    if len(set(values))!=len(values) or any(a<=0 for a in values): raise ValueError('Complete bank collision')
    out=Path(output_dir or os.environ.get('COURSE_ACADEMY_GENERATOR_OUTPUT_DIR',''))
    if not str(output_dir or os.environ.get('COURSE_ACADEMY_GENERATOR_OUTPUT_DIR','')):raise ValueError('Set COURSE_ACADEMY_GENERATOR_OUTPUT_DIR')
    asset,geometry=plot(p,out)
    prompt=f'![Triangle {v}{u}{z} with its given side lengths and included angle]({asset})\n\n'
    prompt+='The area of $'+r'\triangle '+v+u+z+'$ is $'+tex(area)+r'\,\text{'+unit+r'}^2$. '
    if kind=='side':
        prompt+='Find $'+target+'$.'
        if level=='easy':prompt+='\n\nUse $'+r'\mathcal A=\frac12('+sc+')('+sb+r')\sin '+v+'$ and $'+r'\sin '+str(t)+r'^\circ='+tex(s)+'$.'
        if ft=='blank':prompt+='\n\n$'+target+'=$ {{field-1}} $'+r'\text{'+unit+'}$.'
        coefficient=sp.simplify(k*s/2)
        rows=[r'\mathcal A&=\frac12('+sc+')('+sb+r')\sin '+v,
              tex(area)+r'&=\frac12\cdot\left('+tex(k)+r'\right)\cdot x\cdot\sin '+str(t)+r'^\circ',
              tex(area)+r'&=\frac12\cdot\left('+tex(k)+r'\right)\cdot x\cdot\left('+tex(s)+r'\right)',
              tex(area)+'&='+r'\left('+tex(coefficient)+r'\right)x',
              'x&='+r'\frac{'+tex(area)+'}{'+tex(coefficient)+'}='+tex(x)]
        sine_step=(r'\sin '+str(t)+r'^\circ=\sin(180^\circ-'+str(t)+r'^\circ)=\sin '+str(180-t)+r'^\circ='+tex(s)) if t>90 else (r'\sin '+str(t)+r'^\circ='+tex(s))
        solution='The angle at $'+v+'$ is included between $'+sc+'$ and $'+sb+'$. Let $x$ be the length of $'+target+'$ in '+unit+'. Use $'+sine_step+'$:\n\n'+display(rows)+'\n\nThus $'+target+'='+tex(x)+r'\,\text{'+unit+'}$. '
    else:
        branch='acute' if t<90 else 'obtuse';ref=min(t,180-t)
        prompt+='The angle at $'+v+'$ is **'+branch+'**. Find its exact measure.'
        if ft=='blank':prompt+='\n\n$m'+r'\angle '+v+r'=$ {{field-1}} $^\circ$.'
        coefficient=sp.simplify(b*c/2)
        rows=[r'\mathcal A&=\frac12('+sc+')('+sb+r')\sin '+v,
              tex(area)+r'&=\frac12\cdot\left('+tex(c)+r'\right)\cdot\left('+tex(b)+r'\right)\sin '+v,
              tex(area)+'&='+r'\left('+tex(coefficient)+r'\right)\sin '+v,
              r'\sin '+v+'&='+r'\frac{'+tex(area)+'}{'+tex(coefficient)+'}='+tex(s)]
        solution='The known sides $'+sc+'='+tex(c)+'$ and $'+sb+'='+tex(b)+'$ meet at $'+v+'$. Isolate the sine:\n\n'+display(rows)
        solution+='\n\nSince $'+r'\sin '+str(ref)+r'^\circ='+tex(s)+'$, the possible angles inside a triangle are $'+str(ref)+r'^\circ$ and $180^\circ-'+str(ref)+r'^\circ='+str(180-ref)+r'^\circ$. The requested angle is **'+branch+'**, so $m'+r'\angle '+v+'='+str(t)+r'^\circ$. '
    solution+='Checking the area gives $'+r'\frac12\cdot\left('+tex(c)+r'\right)\cdot\left('+tex(b)+r'\right)\cdot\left('+tex(s)+r'\right)='+tex(area)+r'\,\text{'+unit+r'}^2$.'
    prompt,solution=map(normalize_prose,(prompt,solution))
    shown=[tex(a)+(r'\,\text{'+unit+'}' if kind=='side' else r'^\circ') if ft=='radio' else tex(a) for a in values]
    correct_index=values.index(x);payload={'prompt':prompt,'solution':solution,'bank':sorted(shown),'type':ft,'correct':shown[correct_index],'level':level}
    h=digest(payload);fid=ident(h+'field')
    answers=[{':answer/id':ident(fid+text),':answer/type':':answer.type/math',':answer/value':text} for text in shown]
    correct=answers[correct_index]
    rng.shuffle(answers)
    if position is not None and ft=='radio':
        answers.remove(correct);answers.insert(position%5,correct)
    field={':answer-field/id':fid,':answer-field/key':'field-1' if ft=='blank' else 'selection',':answer-field/type':':answer-field.type/'+ft,':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct[':answer/id']]}
    q={':question/id':ident(h),':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':[field]}
    record={'knowledge_point':KP,'question':q,'generation':{'version':VERSION,'seed':seed,'instance':p,'profile':profile,'area':str(area),'sine':str(s),'answer':str(x),'geometry':geometry,'basis':DATA['basis'],'bank_origin':'authored-error-profile','bank_errors':error_labels if kind=='side' and ft=='radio' else [],'solution_path':{'displayed_final':tex(x),'requested_fragment':tex(x),'conversions':['special-angle sine evaluation']+(['supplementary angle selection'] if kind=='angle' else ['linear isolation and exact cancellation']),'shown_rows':rows}}}
    return validate_generated_record(record)

def sample(level,count,seed,output_dir=None):
    if count<0:raise ValueError('Count must be nonnegative')
    rng=random.Random(seed);result=[];seen=set();used_angle_ranks={'acute':set(),'obtuse':set()};used_shape_ranks={};used_side_ranks={}
    # A shuffled cycle covers method-relevant cases in small finite batches.
    angles=[30,45,60] if level=='easy' else [30,45,60,120,135,150]
    rng.shuffle(angles);profiles=list(SIDE_PROFILES);rng.shuffle(profiles)
    targets=['b','c'];rng.shuffle(targets);positions=list(range(5));rng.shuffle(positions)
    for i in range(count):
        kind='angle' if level=='hard' else 'side'
        t=angles[i%len(angles)];target='angle' if kind=='angle' else targets[i%2]
        ft='radio' if level=='easy' or i%2==0 else 'blank'
        profile='blank' if ft=='blank' else profiles[(i//2)%len(profiles)] if kind=='side' else 'special-angle-bank'
        bank_rank=None
        if kind=='angle' and ft=='radio':
            branch='acute' if t<90 else 'obtuse'
            feasible={a[0] for a in angle_bank_arrangements(t)}
            unused=feasible-used_angle_ranks[branch]
            bank_rank=rng.choice(sorted(unused or feasible))
        for attempt in range(200):
            b,c=sp.Integer(rng.randint(3,12)),sp.Integer(rng.randint(3,12))
            if kind=='angle' and rng.randrange(2):
                # Small radical lengths normalize the exact sine without unrelated fractions.
                c=sp.Integer(rng.randint(2,5))*sp.sqrt(2 if min(t,180-t)==45 else 3)
            if max(float(b),float(c))/min(float(b),float(c))>2.5:continue
            j=rng.randrange(3);labels=['ABC'[j:]+ 'ABC'[:j]][0]
            p={'b':str(b),'c':str(c),'theta':t,'unit':rng.choice(['cm','mm']),'kind':kind,'labels':labels,'target':target}
            if kind=='angle' and ft=='radio':
                # A balanced aggregate can hide a fixed rank in diagrams with
                # radical labels. Choose the bank after the visible shape is known.
                shape='radical' if b.has(sp.Pow) or c.has(sp.Pow) else 'rational'
                groups=[used_angle_ranks[branch],used_shape_ranks.get(shape,set()),
                        used_shape_ranks.get((branch,shape),set())]
                scores={rank:sum(rank not in used for used in groups) for rank in feasible}
                bank_rank=rng.choice(sorted(rank for rank in feasible if scores[rank]==max(scores.values())))
            if kind=='side' and ft=='radio':
                x=b if target=='b' else c;k=c if target=='b' else b
                feasible={1+sum(bool(v<x) for v in a[0]) for a in side_banks(x,k,sine(t))}
                if not feasible:continue
                unused=feasible-used_side_ranks.get(t,set())
                bank_rank=rng.choice(sorted(unused or feasible))
            try:r=build(level,rng.getrandbits(64),p,profile,ft,output_dir,positions[i%5],bank_rank)
            except ValueError as e:
                if str(e)=='Complete bank collision':continue
                raise
            semantic=digest({'kind':kind,**{k:p[k] for k in ('b','c','theta','target')}})
            if semantic in seen:continue
            seen.add(semantic);result.append(r)
            if bank_rank is not None:
                if kind=='angle':
                    used_angle_ranks[branch].add(bank_rank)
                    used_shape_ranks.setdefault(shape,set()).add(bank_rank)
                    used_shape_ranks.setdefault((branch,shape),set()).add(bank_rank)
                else:used_side_ranks.setdefault(t,set()).add(bank_rank)
            break
        else:raise RuntimeError('Cannot construct complete distinct bank')
    return result

def replay_sources():
    """Evidence replay of complete captured records, never used by normal sampling."""
    records=[]
    for source in DATA['questions']:
        q=copy.deepcopy(source);sid=q.get(':question/math-academy-id','canonical')
        q={k:v for k,v in q.items() if k.startswith(':question/') and k!=':question/math-academy-id'}
        q[':question/id']=ident('replay:'+sid)
        for key in (':question/problem',':question/worked-solution'):q[key]=normalize_prose(q[key])
        for f in q.get(':question/answer-fields',[]):
            old=f[':answer-field/correct'][':answer/id'];f.pop(':db/id',None);f[':answer-field/id']=ident('replay:'+sid+f[':answer-field/key']);f[':answer-field/type']=f[':answer-field/type'][':db/ident']
            for a in f[':answer-field/choices']:
                aid=a[':answer/id'];a.pop(':db/id',None);a[':answer/type']=':answer.type/math';a[':answer/value']=normalize_tex(a[':answer/value']);a[':answer/id']=ident('replay:'+sid+aid)
                if aid==old:f[':answer-field/correct']=[':answer/id',a[':answer/id']]
        records.append({'knowledge_point':KP,'question':q,'generation':{'replay_source':source[':question/id'],'evidence_only':True}})
    return records

def main():
    a=argparse.ArgumentParser();a.add_argument('--difficulty',choices=['easy','moderate','hard','all','unclassified'],default='moderate');a.add_argument('--count',type=int,default=1);a.add_argument('--seed',type=int,default=0);a.add_argument('--format',choices=['json'],default='json');a.add_argument('--replay-sources',action='store_true');args=a.parse_args()
    if args.replay_sources:records=replay_sources()
    else:
        level='moderate' if args.difficulty=='unclassified' else args.difficulty
        records=[r for band in (['easy','moderate','hard'] if level=='all' else [level]) for r in sample(band,args.count,args.seed)]
    print(json.dumps(records,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
