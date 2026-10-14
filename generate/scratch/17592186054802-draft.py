#!/usr/bin/env python3
"""Private all-level graph recognition draft with parameterized complete original raw banks."""
import argparse
import hashlib
import importlib.util
import json
import os
import random
import re
import uuid
import sys
from pathlib import Path

if __name__ == '__main__' and (importlib.util.find_spec('sympy') is None or importlib.util.find_spec('matplotlib') is None):
    interpreter = Path(__file__).resolve().parents[2] / '.venv/bin/python'
    if interpreter.is_file() and str(interpreter) != sys.executable:
        os.execv(str(interpreter), [str(interpreter), __file__, *sys.argv[1:]])
os.environ.setdefault('MPLCONFIGDIR', '/tmp/course-academy-mpl')
import sympy as sp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

KP_ID = 17592186054802
KP_UUID = '3986a3cd-c543-54e9-8d55-f744d9436313'
TITLE = 'Identifying a Line Given a Graph'
VERSION = 'graph-line-all3-local-draft-v4'
PACKAGE = Path(__file__).with_suffix('')
GENERATOR_UUID = str(uuid.uuid5(uuid.UUID(KP_UUID), 'question-generator'))
SOURCE = json.loads((PACKAGE / 'source.json').read_text())
PROFILES = {q[':question/math-academy-id']: q for q in SOURCE['record'][':knowledge-point/questions'] if ':question/math-academy-id' in q}
SUPPORTED = ('q-71837', 'q-54293')
SOURCE_CASES = {'q-71837': {'b': 6, 't': 2}, 'q-54293': {'b': 2, 't': 4}}

def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()

def ident(value):
    return str(uuid.uuid5(uuid.UUID(KP_UUID), digest(value)))

def tex(value):
    return sp.latex(sp.Rational(value))

def equations(profile, p):
    b, t = p['b'], p['t']
    c = sp.Rational(b, t)
    if profile == 'q-71837':
        k = int(c)
        return [f'y+{k}x={b}', rf'\frac{{1}}{{{k}}}y+x={t}', f'y=-{k}x+{b}']
    return [rf'y=-{b}x+{tex(c)}', rf'y=-{tex(c)}x+{b}', rf'y={tex(c)}x+{b}']

def aligned(rows):
    return '$$\n' + r'\begin{aligned}' + r' \\ '.join(rows) + r'\end{aligned}' + '\n$$'

def solution(profile, p, asset):
    b, t = p['b'], p['t']; c = sp.Rational(b, t); eq = equations(profile, p)
    header = (f"Let's pick two distinct points on the line. For example, $A$ and $B$ with coordinates $(0,{b})$ and $({t},0)$, respectively.\n\n![]({asset})\n\n"
              "Now, we substitute the coordinates of both points in our equations. If both points satisfy an equation, then we can conclude that the equation represents the line in the graph. Otherwise, if any point does *not* satisfy the equation, then we can conclude that the equation does *not* represent the line in the graph.")
    if profile == 'q-71837':
        k = int(c); f = rf'\frac{{1}}{{{k}}}'
        rows = [
            [f'({b})+{k}(0) & ={b}', rf'{b} & ={b}\,✓', f'(0)+{k}({t}) & ={b}', rf'{b} & ={b}\,✓'],
            [f'{f}({b})+(0) & ={t}', f'{t}+0 & ={t}', rf'{t} & ={t}\,✓', f'{f}(0)+({t}) & ={t}', f'0+{t} & ={t}', rf'{t} & ={t}\,✓'],
            [f'({b}) & =-{k}(0)+{b}', rf'{b} & ={b}\,✓', f'(0) & =-{k}({t})+{b}', f'0 & =-{b}+{b}', rf'0 & =0\,✓']]
        blocks = []
        for i in range(3):
            concluding = f'Therefore,{eq[i]}' if i == 1 else f'Therefore, {eq[i]}'
            space = '  ' if i == 2 else ' '
            blocks.append(f'- Equation {("I", "II", "III")[i]}: ${eq[i]}.$\nSubstituting the coordinates of $A(0,{b})$ and $B({t},0)$, we obtain\n\n' + aligned(rows[i]) + f'\n\n{concluding}$ is{space}an equation of the line in the graph.')
        # Add the opening dollar at the same position as the source.
        blocks = [z.replace('Therefore,', 'Therefore,$', 1) if i == 1 else z.replace('Therefore, ', 'Therefore, $', 1) for i,z in enumerate(blocks)]
        tail = 'All the given equations represented the line in the graph. Therefore, the correct answer is "I, II and III."'
    else:
        f = tex(c)
        rows = [
            [rf'({b}) & =-{b}(0)+{f}', rf'{b} & ={f}\,\times '],
            [rf'({b}) & =-{f}(0)+{b}', rf'{b} & ={b}\,✓', rf'(0) & =-{f}({t})+{b}', f'0 & =-{b}+{b}', rf'0 & =0\,✓'],
            [rf'({b}) & ={f}(0)+{b}', rf'{b} & ={b}\,✓', rf'(0) & ={f}({t})+{b}', f'0 & ={b}+{b}', rf'0 & ={2*b}\,\times ']]
        blocks = []
        for i in range(3):
            coords = f'$A(0,{b})$' + (f' and $B({t},0)$' if i else '')
            before = f'- Equation {("I", "II", "III")[i]}: ${eq[i]}.$\nSubstituting the coordinates of {coords}, we obtain\n\n'
            if i == 1:
                after = f'Therefore,${eq[i]}$ is an equation of the line in the graph.'
            else:
                after = f'Therefore, ${eq[i]}$ is *not* equation of the line in the graph.'
            blocks.append(before + aligned(rows[i]) + '\n\n' + after)
        tail = f'Of the given equations, the only equation that represented the line in the graph was ${eq[1]},$ corresponding to answer choice II. Therefore, the correct answer is "II only."'
    return header + '\n\n' + '\n\n'.join(blocks) + '\n\n' + tail

# Local all-level extension. Baseline solution recipes are retained above, isolated
# by PACKAGE derived from this *draft* filename before importing source evidence.
import tempfile
import threading
import math
_RENDER_LOCK = threading.RLock()
BASE_SOLUTION = solution
BASE_EQUATIONS = equations
SOURCE_CASES.update({'q-54285': {'b':2,'t':4}, 'q-59732':{'b':4,'t':4}})
SOURCE_LEVELS = {'q-54285':'moderate','q-59732':'easy','q-71837':'hard','q-54293':'hard'}
LABELS = ('I','II','III')

def line(p, profile=None):
    if 'm' in p: return sp.Rational(p['m']), sp.Rational(p['b'])
    b,t=sp.Rational(p['b']),sp.Rational(p['t'])
    return (b/t if profile=='q-54285' else -b/t),b

def task_key(p, profile=None):
    # The graph locus is assessed; traversal, plot bounds, bank and aliases are not.
    return digest([str(v) for v in line(p,profile)])

def point_pair(profile,p):
    m,b=line(p,profile)
    u=sp.Rational(p.get('u',p.get('t',1)))
    return [(sp.Integer(0),b),(u,sp.simplify(m*u+b))]

def y_eq(m,b):
    return 'y='+tex(m)+'x'+('+' if b>=0 else '-')+tex(abs(b))

def equations(profile,p):
    if profile in SUPPORTED:return BASE_EQUATIONS(profile,p)
    b=sp.Rational(p['b'])
    if profile=='q-54285':
        c=b/sp.Rational(p['t'])
        return [rf'y = x + {tex(c)}',rf'y = {tex(c)}x + {tex(b)}',rf'y = {tex(c)}x + {tex(c)}']
    if profile=='q-59732':return [f'x + 2y = {tex(b)}',f'y = {tex(b/2)} - x',f'y = {tex(b)} - x']
    m,b=line(p)
    if profile=='authored-easy':return [y_eq(m,b),y_eq(-m,b),y_eq(m,-b)]
    if profile=='authored-moderate':return [y_eq(b,m),y_eq(m,b),y_eq(-m,b)]
    if profile=='authored-hard':
        return [y_eq(m,b),y_eq(1/m,b),tex(m)+'x-y='+tex(-b)]
    raise ValueError('Unknown whole bank profile')

def math_expr(text):
    z=text.replace(' ','').replace('&','').replace(r'\,','').replace(r'\times','').replace('✓','').rstrip('.')
    z=re.sub(r'\\d?frac\{(-?\d+)\}\{(-?\d+)\}',r'(\1)/(\2)',z)
    if not re.fullmatch(r'[\d()+\-*/xy]+',z):raise ValueError('Unsupported printed math '+text)
    z=re.sub(r'(?<=[\d)xy])(?=[xy(])','*',z)
    return sp.sympify(z,locals=dict(zip('xy',sp.symbols('x y'))),rational=True)

def equation_tuple(text):
    x,y=sp.symbols('x y'); sides=text.split('=')
    if len(sides)!=2:raise ValueError('Whole equation required')
    poly=sp.Poly(sp.expand(math_expr(sides[0])-math_expr(sides[1])),x,y)
    if poly.total_degree()!=1:raise ValueError('Nonlinear statement')
    coefficients=[poly.coeff_monomial(x),poly.coeff_monomial(y),poly.coeff_monomial(1)]
    pivot=next(z for z in coefficients if z!=0)
    return tuple(sp.cancel(z/pivot) for z in coefficients)

def truths(profile,p,eqs):
    m,b=line(p,profile);target=equation_tuple(y_eq(m,b))
    return [equation_tuple(e)==target for e in eqs]

def source_asset(profile,role):
    q=PROFILES[profile]
    refs=re.findall(r'!\[.*?\]\((.*?)\)',q.get(':question/problem' if role=='prompt' else ':question/worked-solution',''))
    return refs[0] if refs else None

def plot(profile,p,role):
    """Matplotlib only; unique fresh PNG/sidecar temporaries, atomic destinations."""
    m,b=line(p,profile);points=point_pair(profile,p)
    if profile in PROFILES and p==SOURCE_CASES[profile]:
        old=source_asset(profile,role)
        if old:
            local=Path('/media/jake/SSD/EDB/math')/old
            return old,{'local':str(local),'path':old,'sha256':hashlib.sha256(local.read_bytes()).hexdigest(),'role':role,'source_calibration':profile,'renderer':'captured native PNG'}
    signature=digest({'version':VERSION,'line':[str(m),str(b)],'points':[[str(z) for z in a] for a in points],'role':role})
    directory=PACKAGE/'assets';directory.mkdir(exist_ok=True)
    local=directory/(signature+'.png');sidecar=local.with_suffix('.json')
    if local.exists() and sidecar.exists():return str(local),json.loads(sidecar.read_text())
    # Bounds track the two selected readable points. One integer coordinate unit per grid.
    xs=[float(v[0]) for v in points]+[0.0];ys=[float(v[1]) for v in points]+[0.0]
    xmin,xmax=math.floor(min(xs))-3,math.ceil(max(xs))+3
    ymin,ymax=math.floor(min(ys))-3,math.ceil(max(ys))+3
    span=max(xmax-xmin,ymax-ymin);xmax=xmin+span;ymax=ymin+span
    if span>30:raise ValueError('Native graph would be unreadable')
    with _RENDER_LOCK:
        fig,ax=plt.subplots(figsize=(4.6,4.6),dpi=120)
        fig.subplots_adjust(left=.12,right=.9,bottom=.12,top=.9)
        ax.set(xlim=(xmin,xmax),ylim=(ymin,ymax));ax.set_aspect('equal')
        ax.set_xticks(range(xmin,xmax+1));ax.set_yticks(range(ymin,ymax+1))
        ax.grid(color='#cccccc',linewidth=.65);ax.set_axisbelow(True)
        ax.spines[['right','top']].set_visible(False);ax.spines[['left','bottom']].set_position('zero')
        ax.tick_params(length=0,labelsize=9,pad=7)
        ax.set_xticklabels(['' if z==0 or (span>14 and z%2) else str(z) for z in range(xmin,xmax+1)])
        ax.set_yticklabels(['' if z==0 or (span>14 and z%2) else str(z) for z in range(ymin,ymax+1)])
        ax.plot([xmin,xmax],[float(m*xmin+b),float(m*xmax+b)],color='#ff0000',linewidth=1.8,zorder=3)
        ax.plot(xmax,0,'>k',clip_on=False,markersize=5);ax.plot(0,ymax,'^k',clip_on=False,markersize=5)
        ax.annotate('$x$',(xmax,0),xytext=(13,-3),textcoords='offset points',fontsize=12)
        ax.annotate('$y$',(0,ymax),xytext=(-3,13),textcoords='offset points',fontsize=12)
        marker_labels=[]
        if role=='solution':
            for label,(u,v) in zip(('A','B'),points):
                ax.scatter([float(u)],[float(v)],color='blue',s=24,zorder=5)
                offset=(24,(10 if m<0 else -14)) if v==0 else (24,-6)
                marker_labels.append(ax.annotate('$'+label+'$',(float(u),float(v)),xytext=offset,textcoords='offset points',fontsize=11,zorder=6))
        fig.canvas.draw();renderer=fig.canvas.get_renderer()
        origin=ax.transData.transform((0,0));unit=ax.transData.transform((1,1))-origin
        boxes=[list(t.get_window_extent(renderer).bounds) for t in ax.get_xticklabels()+ax.get_yticklabels() if t.get_text()]
        marker_boxes=[list(t.get_window_extent(renderer).bounds) for t in marker_labels]
        marker_clearance=min([min(xx-origin[0],(yy-origin[1]) if yy>origin[1] else origin[1]-(yy+hh)) for xx,yy,ww,hh in marker_boxes],default=999)
        if marker_clearance<4:raise ValueError('Marker label too close to a zero axis')
        w,h=fig.canvas.get_width_height()
        # Native pixel calibration independent of PNG curve pixels, retained for readback.
        meta={'local':str(local),'path':str(local),'role':role,'renderer':'matplotlib','dimensions':[w,h],
              'origin_pixels':[float(origin[0]),float(h-origin[1])],'unit_pixels':[float(unit[0]),float(unit[1])],
              'limits':[xmin,xmax,ymin,ymax],'points':[[str(z) for z in a] for a in points],
              'line':[str(m),str(b)],'tick_bboxes_display':boxes,'marker_bboxes_display':marker_boxes,'marker_min_axis_clearance_px':float(marker_clearance),'glyph_min_axis_clearance_px':min([origin[1]-(y+hh) for x,y,ww,hh in boxes[:len([t for t in ax.get_xticklabels() if t.get_text()])]]+[origin[0]-(x+ww) for x,y,ww,hh in boxes[len([t for t in ax.get_xticklabels() if t.get_text()]):]])}
        fd,temp=tempfile.mkstemp(prefix=signature+'-',suffix='.png',dir=directory);os.close(fd)
        try:fig.savefig(temp,metadata={'Software':VERSION});os.replace(temp,local)
        finally:
            if os.path.exists(temp):os.unlink(temp)
            plt.close(fig)
        meta['sha256']=hashlib.sha256(local.read_bytes()).hexdigest()
        fd,temp=tempfile.mkstemp(prefix=signature+'-',suffix='.json',dir=directory);os.close(fd)
        try:Path(temp).write_text(json.dumps(meta,indent=2)+'\n');os.replace(temp,sidecar)
        finally:
            if os.path.exists(temp):os.unlink(temp)
    return str(local),meta

def solution(profile,p,asset,eqs=None):
    if profile in SUPPORTED:
        text=BASE_SOLUTION(profile,p,asset)
        return text
    b,t=sp.Rational(p['b']),sp.Rational(p.get('t',1))
    if profile=='q-54285':return f'The line crosses the y-axis at {b} and passes through ({t},{2*b}); its slope is {b/t}. Therefore y=x/{t/b}+{b}, statement II.'
    if profile=='q-59732':return f'The line has intercepts (0,{b}) and ({t},0), so its equation is y={b}-x, statement III.'
    eqs=eqs or equations(profile,p);points=point_pair(profile,p);truth=truths(profile,p,eqs)
    intro=f"Let's pick two distinct points on the line. For example, $A$ and $B$ with coordinates $({tex(points[0][0])},{tex(points[0][1])})$ and $({tex(points[1][0])},{tex(points[1][1])})$, respectively.\n\n![]({asset})\n\nNow, we substitute the coordinates of both points in our equations. If both points satisfy an equation, then we can conclude that the equation represents the line in the graph. Otherwise, if any point does *not* satisfy the equation, then we can conclude that the equation does *not* represent the line in the graph."
    blocks=[];x,y=sp.symbols('x y')
    for label,eq,valid in zip(LABELS,eqs,truth):
        lhs,rhs=eq.split('=');rows=[]
        for u,v in points:
            subst=lambda s:re.sub(r'([xy])',lambda a:'('+tex(u if a[1]=='x' else v)+')',s)
            left,right=math_expr(lhs).subs({x:u,y:v}),math_expr(rhs).subs({x:u,y:v})
            rows += [subst(lhs)+' & ='+subst(rhs),tex(left)+' & ='+tex(right)+(r'\,✓' if left==right else r'\,\times')]
            if left!=right:break
        blocks.append(f'- Equation {label}: ${eq}.$\nSubstituting the coordinates of the selected points, we obtain\n\n'+aligned(rows)+'\n\nTherefore, $'+eq+'$ is '+('' if valid else '*not* ')+'an equation of the line in the graph.')
    return intro+'\n\n'+'\n\n'.join(blocks)+'\n\nThe equations representing the line are '+', '.join(a for a,v in zip(LABELS,truth) if v)+'.'

# Easy: integer arithmetic, three directly written claims, two readable points.
# Moderate: simple rational arithmetic, swapped slope/intercept and sign profiles.
# Hard: three equations including equivalent rearrangements, original full banks.
def candidates(profile):
    if profile.endswith('-raw'):profile=profile[:-4]
    if profile=='q-71837':return [{'b':k*t,'t':t} for k in range(2,6) for t in range(1,5)]
    if profile=='q-54293':return [{'b':b,'t':t} for b in range(1,7) for t in (2,3,4,6,8)]
    if profile=='q-54285':return [{'b':b,'t':2*b} for b in range(2,6)]
    if profile=='q-59732':return [{'b':b,'t':b} for b in range(2,9,2)]
    if profile=='authored-easy':return [{'m':m,'b':b,'u':2} for m in (-2,-1,1,2) for b in range(-6,7) if b]
    if profile=='authored-moderate':return [{'m':str(sp.Rational(m,d)),'b':b,'u':d} for m,d in ((1,2),(-1,2),(2,3),(-2,3),(3,2),(-3,2)) for b in range(-6,7) if b]
    if profile=='authored-hard':return [{'m':m,'b':b,'u':2} for m in (-4,-3,-2,2,3,4) for b in range(-6,7) if b]
    raise ValueError('Unknown template/profile')

def subset_value(labels):
    if len(labels)==3:return 'I, II and III'
    return (' and '.join(labels)+' only') if len(labels)==2 else labels[0]+' only'

def generate(level='hard',seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ('easy','moderate','hard'):raise ValueError('Unknown difficulty')
    rng=random.Random(seed)
    requested_profile=profile or template or ('authored-'+level)
    raw=requested_profile.endswith('-raw')
    profile=requested_profile[:-4] if raw else requested_profile
    if raw and profile not in PROFILES:raise ValueError('Raw replay only for original MA profiles')
    if template and template not in (profile,requested_profile):raise ValueError('Template/profile mismatch')
    if profile in PROFILES and SOURCE_LEVELS[profile]!=level:raise ValueError('Source profile assigned different authored/sourced level')
    if profile not in PROFILES and profile!='authored-'+level:raise ValueError('Level scope mismatch')
    # Normalize exact numeric spelling; no alias can create extra mathematical tasks.
    domain=candidates(profile)
    p=parameters if parameters is not None else rng.choice(domain)
    if any(not isinstance(v,(str,int)) or isinstance(v,bool) for v in p.values()):raise ValueError('Exact integers/rational strings required')
    canonical=lambda z:{k:str(sp.Rational(v)) for k,v in z.items()}
    if canonical(p) not in [canonical(z) for z in domain]:raise ValueError('Parameters outside explicit per-level domain')
    p=next(z for z in domain if canonical(z)==canonical(p))
    eqs=equations(profile,p);truth=truths(profile,p,eqs)
    if not any(truth):raise ValueError('No qualifying claims')
    if profile in ('q-54285','q-59732') or profile.startswith('authored-'):kind='checkbox'
    else:kind='radio'
    if field_type and field_type not in (kind,':answer-field.type/'+kind):raise ValueError('Field contract mismatch')
    prompt_asset,a1=plot(profile,p,'prompt')
    # Unrated source solutions have no solution image; preserve that absence.
    if profile in ('q-54285','q-59732'):solution_asset,a2=None,None
    else:solution_asset,a2=plot(profile,p,'solution')
    prompt=f'![]({prompt_asset})\n\nWhich of the following gives the graph of the straight line above?\n\n'
    if kind=='checkbox':prompt+='Select all that apply.\n\n'+'\n'.join(f'- **{label}.** ${e}$' for label,e in zip(LABELS,eqs))
    else:prompt+='\n\n'.join(f'{label}. ${e}$' for label,e in zip(LABELS,eqs))
    worked=solution(profile,p,solution_asset,eqs)
    if raw and profile=='q-54293':
        # Explicit observed typo mask: actual coefficient b is replaced by b-1 in
        # this single zero-coordinate substitution, never normal generation.
        worked=worked.replace(f'({p["b"]}) & =-{p["b"]}(0)',f'({p["b"]}) & =-{p["b"]-1}(0)',1)
    specs=[]
    if kind=='checkbox':specs=[(label,['false','true'],str(ok).lower()) for label,ok in zip(LABELS,truth)]
    else:
        values=[a[':answer/value'] for a in PROFILES[profile][':question/answer-fields'][0][':answer-field/choices']]
        desired=subset_value([label for label,ok in zip(LABELS,truth) if ok])
        if desired not in values or len({frozenset(re.findall(r'\bI{1,3}\b',v)) for v in values})!=len(values):raise ValueError('Incomplete/duplicate whole-subset bank')
        specs=[('selection',sorted(values),desired)]
    key=task_key(p,profile)
    # Identity includes the actual content and complete banks, no seed/profile alias.
    qid=ident([VERSION,level,prompt,worked,specs]);fields=[]
    for fieldkey,values,correct in specs:
        fid=ident([qid,fieldkey]);choices=[{':answer/id':ident([fid,v]),':answer/type':':answer.type/text',':answer/value':v} for v in values]
        aid=next(a[':answer/id'] for a in choices if a[':answer/value']==correct)
        if kind=='radio':rng.shuffle(choices)
        fields.append({':answer-field/id':fid,':answer-field/key':fieldkey,':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':choices,':answer-field/correct':[':answer/id',aid]})
    q={':question/id':qid,':question/problem':prompt,':question/worked-solution':worked,':question/difficulty':':question.difficulty/'+level,':question/answer-fields':fields}
    if raw and ':question/difficulty' not in PROFILES[profile]:q.pop(':question/difficulty')
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'template':profile,'bank_profile':requested_profile,'raw_source_replay':raw,'level':level,'source_errors':[f'q-54293 displayed coefficient -{p["b"]}, raw zero-coordinate stage uses -{p["b"]-1}'] if raw and profile=='q-54293' else [],'eligible_for_normal_inventory':not(raw and profile=='q-54293'),'parameters':p,'domain':'two point graph to complete equation recognition; finite domain in candidates()', 'source_ids':[profile] if profile in PROFILES else [],'parameter_fingerprint':key,'mathematical_task_roles':['given graph locus','three whole equation claims','complete qualifying subset'],'assets':[a for a in (a1,a2) if a],'sympy':sp.__version__,'matplotlib':matplotlib.__version__,'source_basis':SOURCE['basis'],'source_lineage':SOURCE['lineage'],'policy':'authored missing-level policy' if level!='hard' else 'observed hard / authored same-method extension'}}

def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)

def batch(level,count,seed,template=None,profile=None):
    if count<1:raise ValueError('Positive count required')
    rng=random.Random(seed);family=profile or template or 'authored-'+level
    pairs=candidates(family)[:];rng.shuffle(pairs)
    if count>len(pairs):raise ValueError('Finite mathematical domain exhausted')
    return [generate(level,seed+i,template=template,profile=family,parameters=p) for i,p in enumerate(pairs[:count])]

def markdown(rec):
    q=rec['question']
    return q[':question/problem']+'\n\n'+'\n'.join(f[':answer-field/key']+': '+', '.join(a[':answer/value'] for a in f[':answer-field/choices']) for f in q[':question/answer-fields'])+'\n\n'+q[':question/worked-solution']

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');parser.add_argument('--count',type=int,default=1);parser.add_argument('--seed',type=int,default=0);parser.add_argument('--format',choices=['markdown','json'],default='json');parser.add_argument('--template');parser.add_argument('--profile')
    args=parser.parse_args();records=[]
    for level in ('easy','moderate','hard') if args.difficulty=='all' else (args.difficulty,):records+=batch(level,args.count,args.seed,args.template,args.profile)
    print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
