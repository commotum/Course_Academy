#!/usr/bin/env python3
"""Relocatable two-point line recognition generator; adapted from supplied draft."""
import argparse, copy, hashlib, json, math, os, random, re, sys, tempfile, threading, uuid
from pathlib import Path
os.environ.setdefault('MPLCONFIGDIR', '/tmp/course-academy-mpl')
import sympy as sp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from math_format import normalize_prose, checked_math_content
KP_ID=17592186054802
KP_UUID='3986a3cd-c543-54e9-8d55-f744d9436313'
TITLE='Identifying a Line Given a Graph'
VERSION='two-point-line-v11-compatible-intercepts'
PACKAGE=Path(__file__).resolve().parent
SOURCE=json.loads((PACKAGE/'source-data.json').read_text())
PROFILES={q[':question/math-academy-id']:q for q in SOURCE['kp'][':knowledge-point/questions']}
LABELS=('I','II','III')
_RENDER_LOCK=threading.RLock()
def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def ident(value):
    return str(uuid.uuid5(uuid.UUID(KP_UUID),digest(value)))
def tex(value): return sp.latex(sp.Rational(value))
def line(p,profile=None): return sp.Rational(p['m']),sp.Rational(p['b'])
def point_pair(profile,p):
    m,b=line(p);u=sp.Rational(p.get('u',m.q));return [(sp.Integer(0),b),(u,m*u+b)]
def y_eq(m,b): return 'y='+affine(m,b)
def affine(m,b):
    m,b=sp.Rational(m),sp.Rational(b)
    first=('x' if m==1 else '-x' if m==-1 else tex(m)+'x') if m else ''
    return first+('+' if b>0 and first else '')+(tex(b) if b else '') or '0'
def aligned(rows): return '$$\n'+r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}'+'\n$$'
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

def graph_limits(p):
    """A band-wide frame independent of the target, claims, seed, and key."""
    extent=7 if p['presentation'] in EASY_FORMS else 9
    return (-extent,extent,-extent,extent)

def plot(profile,p,role):
    """Matplotlib only; unique fresh PNG/sidecar temporaries, atomic destinations."""
    m,b=line(p,profile);points=point_pair(profile,p)
    limits=graph_limits(p)
    signature=digest({'version':VERSION,'line':[str(m),str(b)],'points':[[str(z) for z in a] for a in points],'role':role,'limits':limits})
    directory=Path(os.environ['COURSE_ACADEMY_GENERATOR_OUTPUT_DIR']).resolve();directory.mkdir(parents=True,exist_ok=True)
    local=directory/(signature+'.png');sidecar=local.with_suffix('.json')
    if local.exists() and sidecar.exists():return str(local),json.loads(sidecar.read_text())
    # Never pad around the target: that leaks its intercept through axis labels.
    # Both possible graph targets share exactly the same axes, ticks and scale.
    xmin,xmax,ymin,ymax=limits;span=xmax-xmin
    if not all(xmin<u<xmax and ymin<v<ymax for u,v in points):
        raise ValueError('Selected graph points outside supported fixed frame')
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
                offset=(14,12 if v>=0 else -16)
                marker_labels.append(ax.annotate('$'+label+'$',(float(u),float(v)),xytext=offset,textcoords='offset points',fontsize=11,zorder=6))
        fig.canvas.draw();renderer=fig.canvas.get_renderer()
        origin=ax.transData.transform((0,0));unit=ax.transData.transform((1,1))-origin
        boxes=[list(t.get_window_extent(renderer).bounds) for t in ax.get_xticklabels()+ax.get_yticklabels() if t.get_text()]
        marker_boxes=[list(t.get_window_extent(renderer).bounds) for t in marker_labels]
        marker_clearance=min([min(xx-origin[0],(yy-origin[1]) if yy>origin[1] else origin[1]-(yy+hh)) for xx,yy,ww,hh in marker_boxes],default=999)
        # Labels are verified in actual UI previews; use offsets away from both axes.
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

# Complete observed subset banks (q-54293 and q-54292 have the same bank).
BANKS={name:[a[':answer/value'] for a in PROFILES[name][':question/answer-fields'][0][':answer-field/choices']]
       for name in ('q-71837','q-54293','q-102089')}
SLOPES=tuple(sp.Rational(v) for v in ('-2','2','-3','3','-1/2','1/2','-2/3','2/3','-3/2','3/2','-4/3','4/3'))
INTERCEPTS=tuple(v for v in range(-4,5) if v)
FORMS={'explicit':('slope','intercept','standard'), 'mixed':('standard','scaled','slope')}
EASY_FORMS={'checkbox-affine':('slope','intercept','standard'),
            'checkbox-doubled':('slope','double','intercept')}
EASY_SLOPES=tuple(sp.Rational(v) for v in ('-2','-1','-1/2','1/2','1','2'))
EASY_SUBSETS=tuple(tuple(bool(n & (1<<i)) for i in range(3)) for n in range(1,8))
MODERATE_SUBSETS=tuple(tuple(bool(n & (1<<i)) for i in range(3)) for n in range(8))
MODERATE_SLOPES=tuple(sp.Rational(v) for v in ('-2','2','-1/2','1/2','-2/3','2/3','-3/2','3/2'))
MODERATE_INTERCEPTS=tuple(range(-4,5))
RECIPES=('negate','reciprocal','up','down')

def subset(value): return tuple(label in re.findall(r'\bI{1,3}\b',value) for label in LABELS)
def subset_value(truth):
    labels=[label for label,ok in zip(LABELS,truth) if ok]
    if len(labels)==3:return 'I, II and III'
    if not labels:raise ValueError('Empty subset is outside source banks')
    return ' and '.join(labels)+' only'

def format_equation(m,b,form):
    m,b=sp.Rational(m),sp.Rational(b)
    if form=='slope': return y_eq(m,b)
    if form=='intercept':
        return 'y='+tex(b)+('+' if m>0 else '-')+('x' if abs(m)==1 else tex(abs(m))+'x')
    if form=='standard': return 'y'+('+' if m<0 else '-')+('x' if abs(m)==1 else tex(abs(m))+'x')+'='+tex(b)
    if form=='scaled':
        # Divide y-mx=b by -m, as in q-71837; no new operation is required of the learner.
        return tex(-1/m)+'y+x='+tex(-b/m)
    if form=='double':
        c=-2*m
        return '2y'+('+' if c>0 else '-')+('x' if abs(c)==1 else tex(abs(c))+'x')+'='+tex(2*b)
    raise ValueError(form)

def wrong_lines(m,b):
    return {'negate':(-m,b),'reciprocal':(1/m,b),'up':(m,b+1),'down':(m,b-1)}

def instance(seed,bank=None,value=None,presentation=None,m=None,b=None):
    rng=random.Random(seed)
    bank=bank or rng.choice(tuple(BANKS))
    value=value or rng.choice(BANKS[bank])
    if value not in BANKS[bank]:raise ValueError('Response outside selected complete bank')
    truth=subset(value)
    presentation=presentation or rng.choice(tuple(FORMS))
    m=sp.Rational(m if m is not None else rng.choice(SLOPES))
    b=sp.Rational(b if b is not None else rng.choice(INTERCEPTS))
    if m not in SLOPES or b not in INTERCEPTS:raise ValueError('Graph outside supported domain')
    wrong=wrong_lines(m,b);claims=[];recipes=[]
    for ok in truth:
        if ok:claims.append((m,b));recipes.append('target')
        else:
            recipe=rng.choice(tuple(wrong))
            claims.append(wrong[recipe]);recipes.append(recipe)
    return {'bank':bank,'truth':list(truth),'presentation':presentation,'m':str(m),'b':str(b),
            'claims':[[str(v) for v in c] for c in claims],'recipes':recipes}

def statement_equations(p):
    forms=list((EASY_FORMS if p['presentation'] in EASY_FORMS else FORMS)[p['presentation']])
    return [format_equation(*c,form) for c,form in zip(p['claims'],forms)]

def worked_solution(p,asset,eqs,checkbox=False):
    points=point_pair(None,p);truth=p['truth'];blocks=[]
    text=(f"Let's pick two distinct points on the line. For example, $A$ and $B$ with coordinates "
          f'$({tex(points[0][0])},{tex(points[0][1])})$ and $({tex(points[1][0])},{tex(points[1][1])})$, respectively.\n\n![]({asset})\n\n'
          'Now, we substitute the coordinates of both points in our equations. If both points satisfy an equation, then we can conclude that the equation represents the line in the graph. Otherwise, if any point does *not* satisfy the equation, then we can conclude that the equation does *not* represent the line in the graph.')
    x,y=sp.symbols('x y')
    for label,eq,valid in zip(LABELS,eqs,truth):
        lhs,rhs=eq.split('=');rows=[];checked=[]
        for name,(u,v) in zip(('A','B'),points):
            substitute=lambda s:re.sub('[xy]',lambda a:'('+tex(u if a[0]=='x' else v)+')',s)
            l=math_expr(lhs).subs({x:u,y:v});r=math_expr(rhs).subs({x:u,y:v})
            rows.extend([substitute(lhs)+' &='+substitute(rhs),tex(l)+' &='+tex(r)+(r'\,\checkmark' if l==r else r'\,\times')])
            checked.append(name)
            if l!=r:break
        # Explicit names keep the first/second-point references tied to this instance.
        coords=' and '.join('$'+name+f'({tex(points[0 if name=="A" else 1][0])},{tex(points[0 if name=="A" else 1][1])})$' for name in checked)
        heading='Equation' if checkbox else 'Equation '+label
        blocks.append(f'- {heading}: ${eq}.$\nSubstituting the coordinates of {coords}, we obtain\n\n'+aligned(rows)+
                      '\n\nTherefore, $'+eq+'$ is '+('' if valid else '*not* ')+'an equation of the line in the graph.')
    selected=[label for label,ok in zip(LABELS,truth) if ok]
    if checkbox:
        conclusion=('Select '+', '.join('$'+eq+'$' for eq,ok in zip(eqs,truth) if ok)+'.' if any(truth) else
                    'None of the given equations represents the line in the graph. Leave all boxes unchecked.')
        return text+'\n\n'+'\n\n'.join(blocks)+'\n\n'+conclusion
    tail=('All the given equations represented the line in the graph.' if all(truth) else
          'Of the given equations, the equations that represented the line in the graph were '+', '.join('$'+eq+'$' for eq,ok in zip(eqs,truth) if ok)+', corresponding to '+', '.join(selected)+'.')
    return text+'\n\n'+'\n\n'.join(blocks)+'\n\n'+tail+' Therefore, the correct answer is "'+subset_value(truth)+'."'

def fields_for(qid,specs,kind,rng=None):
    fields=[]
    for key,values,correct in specs:
        fid=ident([qid,key]);choices=[{':answer/id':ident([fid,value]),':answer/type':':answer.type/text',':answer/value':value} for value in values]
        if rng:rng.shuffle(choices)
        aid=next(a[':answer/id'] for a in choices if a[':answer/value']==correct)
        fields.append({':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+kind,
                       ':answer-field/choices':choices,':answer-field/correct':[':answer/id',aid]})
    return fields

def record(prompt,solution,specs,kind,difficulty,generation,seed):
    prompt,solution=normalize_prose(prompt),normalize_prose(solution)
    qid=ident([VERSION,prompt,solution,specs,difficulty]);q={':question/id':qid,':question/problem':prompt,':question/worked-solution':solution,
         ':question/answer-fields':fields_for(qid,specs,kind,random.Random(digest([seed,"answer-order"])))}
    if difficulty:q[':question/difficulty']=':question.difficulty/'+difficulty
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,
            'generation':dict(version=VERSION,seed=seed,source_basis=SOURCE['basis'],source_lineage=SOURCE['lineage'],**generation)}

@checked_math_content
def generate(level='hard',seed=0,parameters=None):
    if level=='easy':return generate_easy(seed,parameters)
    if level=='moderate':return generate_moderate(seed,parameters)
    if level!='hard':raise ValueError('Only source-rated hard is supported')
    p=copy.deepcopy(parameters) if parameters is not None else instance(seed)
    eqs=statement_equations(p);actual=truths(None,p,eqs)
    if actual!=p['truth']:raise ValueError('Inconsistent role assignment')
    if subset_value(actual) not in BANKS[p['bank']]:raise ValueError('Missing complete response')
    if len(set(eqs))!=3:raise ValueError('Duplicate displayed equation')
    a1,meta1=plot(None,p,'prompt');a2,meta2=plot(None,p,'solution')
    prompt=f'![]({a1})\n\nWhich of the following gives the graph of the straight line above?\n\n'+'\n\n'.join(label+'. $'+eq+'$' for label,eq in zip(LABELS,eqs))
    specs=[('selection',BANKS[p['bank']],subset_value(actual))]
    return record(prompt,worked_solution(p,a2,eqs),specs,'radio','hard',
                  {'template':p['presentation'],'bank_profile':p['bank'],'parameters':p,'equations':eqs,'assets':[meta1,meta2],
                   'semantic_instance':digest([p['m'],p['b'],sorted(p['claims'])]),'source_ids':list(BANKS),'rejections':0},seed)

def easy_instance(seed,truth=None,presentation=None,m=None,b=None):
    rng=random.Random(seed)
    # Choose the answer-bearing assignment before compatible graph/claim data.
    truth=tuple(truth) if truth is not None else rng.choice(EASY_SUBSETS)
    presentation=presentation or rng.choice(tuple(EASY_FORMS))
    m=sp.Rational(m if m is not None else rng.choice(EASY_SLOPES))
    b=sp.Rational(b if b is not None else rng.choice(INTERCEPTS))
    if truth not in EASY_SUBSETS or presentation not in EASY_FORMS:raise ValueError('Unsupported easy assignment')
    if m not in EASY_SLOPES or b not in INTERCEPTS:raise ValueError('Unsupported easy graph')
    wrong={k:v for k,v in wrong_lines(m,b).items() if v!=(m,b)}
    # A decoy line can own two claims, just as the target can. Thus an
    # equivalent pair does not identify the graph without inspecting it.
    decoy=rng.choice(tuple(wrong))
    claims=[];recipes=[]
    for ok in truth:
        recipe='target' if ok else decoy
        claims.append((m,b) if ok else wrong[recipe]);recipes.append(recipe)
    return {'truth':list(truth),'presentation':presentation,'m':str(m),'b':str(b),
            'claims':[[str(v) for v in c] for c in claims],'recipes':recipes}

def moderate_instance(seed,truth=None,presentation=None,m=None,b=None,decoy=None):
    """Authored middle band: independent checkbox decisions, small rational arithmetic.

    Assign qualifying roles and rejection case before numerical/presentation data.
    Shared decoys can outnumber the true claims; equivalence alone cannot choose
    the drawn line. All/none are legitimate finite decision cases.
    """
    rng=random.Random(seed)
    truth=tuple(truth) if truth is not None else rng.choice(MODERATE_SUBSETS)
    decoy=decoy or rng.choice(RECIPES)
    presentation=presentation or rng.choice(tuple(EASY_FORMS))
    m=sp.Rational(m if m is not None else rng.choice(MODERATE_SLOPES))
    # Use an interchangeable domain: every candidate can instead be the graph.
    # A shift at an endpoint must point inward, never outside the target domain.
    compatible=[v for v in MODERATE_INTERCEPTS
                if wrong_lines(m,sp.Rational(v))[decoy][1] in MODERATE_INTERCEPTS]
    b=sp.Rational(b if b is not None else rng.choice(compatible))
    if truth not in MODERATE_SUBSETS or presentation not in EASY_FORMS or decoy not in RECIPES:
        raise ValueError('Unsupported moderate assignment')
    if m not in MODERATE_SLOPES or b not in compatible:
        raise ValueError('Unsupported moderate graph')
    other=wrong_lines(m,b)[decoy]
    # Preserve two visible integer points even at intercept ±4.
    u=m.q if -7 < b+m.p < 7 else -m.q
    return {'truth':list(truth),'presentation':presentation,'m':str(m),'b':str(b),'u':str(u),
            'claims':[[str(v) for v in ((m,b) if ok else other)] for ok in truth],
            'recipes':['target' if ok else decoy for ok in truth],'decoy_case':decoy}

def generate_easy(seed=0,parameters=None):
    return generate_checkbox(seed,parameters,'easy')

def generate_moderate(seed=0,parameters=None):
    return generate_checkbox(seed,parameters,'moderate')

def generate_checkbox(seed,parameters,level):
    sampler=moderate_instance if level=='moderate' else easy_instance
    p=copy.deepcopy(parameters) if parameters is not None else sampler(seed)
    eqs=statement_equations(p);actual=truths(None,p,eqs)
    if actual!=p['truth'] or (level=='easy' and not any(actual)):raise ValueError('Inconsistent checkbox assignment')
    if len(set(eqs))!=3:raise ValueError('Duplicate displayed equation')
    a1,meta1=plot(None,p,'prompt');a2,meta2=plot(None,p,'solution')
    prompt=f'![]({a1})\n\nWhich of the following gives the graph of the straight line above?\n\nSelect all that apply.'
    specs=[('$'+eq+'$',['true','false'],str(ok).lower()) for eq,ok in zip(eqs,actual)]
    return record(prompt,worked_solution(p,a2,eqs,checkbox=True),specs,'checkbox',level,
                  {'template':p['presentation'],'bank_profile':'checkbox-true-false','parameters':p,
                   'equations':eqs,'assets':[meta1,meta2],
                   'semantic_instance':digest([p['m'],p['b'],sorted(p['claims'])]),
                   'source_ids':['q-54285','q-59732','e-1702'],
                   'difficulty_basis':('authored moderate extension: small rational coefficients and one rearranged/scaled claim' if level=='moderate' else
                                       'authored easy extension of unrated checkbox sources'),
                   'rejections':0},seed)

SOURCE_PARAMETERS={'q-54285':{'m':'1/2','b':2,'t':4},'q-59732':{'m':-1,'b':4,'t':4},
                   'q-71837':{'m':-3,'b':6,'t':2},'q-54293':{'m':'-1/2','b':2,'t':4},
                   'q-54292':{'m':-2,'b':4,'t':2},'q-102089':{'m':'-4/3','b':4,'t':3}}

def source_equations(profile,p):
    m,b=sp.Rational(p['m']),sp.Rational(p['b']);t=sp.Rational(p['t']);c=b/t
    # Recipes retain all source claims, not just a selected distractor.
    if profile=='q-54285':return [f'y = {tex(c)}x + {tex(b)}',f'y = {tex(c)}x + {tex(c)}',f'y = x + {tex(c)}']
    if profile=='q-59732':return [f'y = {tex(b/2)} - x',f'x + 2y = {tex(b)}',f'y = {tex(b)} - x']
    if profile=='q-71837':return [f'y+{tex(c)}x={tex(b)}',rf'\frac{{1}}{{{tex(c)}}}y+x={tex(t)}',f'y=-{tex(c)}x+{tex(b)}']
    if profile=='q-54293':return [f'y=-{tex(b)}x+{tex(c)}',f'y=-{tex(c)}x+{tex(b)}',f'y={tex(c)}x+{tex(b)}']
    if profile=='q-54292':return [f'y=-{tex(b)}x+{tex(c)}',f'y=x+{tex(b)}',f'y=-{tex(c)}x+{tex(b)}']
    if profile=='q-102089':return [f'y={tex(1/c)}x+1',f'y={tex(b)}-{tex(c)}x',f'y={tex(c)}x']
    raise ValueError(profile)

@checked_math_content
def replay_source(profile):
    source=PROFILES[profile];p=SOURCE_PARAMETERS[profile];eqs=source_equations(profile,p);truth=truths(None,p,eqs)
    kind=source[':question/answer-fields'][0][':answer-field/type'][':db/ident'].split('/')[-1]
    prompt=source[':question/problem']
    if kind=='radio':
        prefix=prompt[:prompt.index('I. $')];prompt=prefix+'\n\n'.join(label+'. $'+eq+'$' for label,eq in zip(LABELS,eqs))
        specs=[('selection',[a[':answer/value'] for a in source[':question/answer-fields'][0][':answer-field/choices']],subset_value(truth))]
    else:specs=[(field[':answer-field/key'],[a[':answer/value'] for a in field[':answer-field/choices']],str(ok).lower())
                for field,ok in zip(source[':question/answer-fields'],truth)]
    worked=source[':question/worked-solution']
    if profile=='q-54293':worked=worked.replace('-1(0)','-2(0)',1)
    difficulty=source.get(':question/difficulty',{}).get(':db/ident','').split('/')[-1] or None
    return record(prompt,worked,specs,kind,difficulty,{'source_replay':profile,'parameters':p,'equations':eqs,'truth':truth,'source_ids':[profile]},0)

def batch(level,count,seed):
    if count<1:raise ValueError('Positive count required')
    if level not in ('easy','moderate','hard'):raise ValueError('Unsupported difficulty')
    records=[];seen=set();attempt=0
    while len(records)<count:
        if attempt>max(1000,count*100):raise ValueError('Unique instance domain exhausted')
        rec=generate(level,seed+attempt);attempt+=1
        key=rec['generation']['semantic_instance']
        if key in seen:continue
        seen.add(key);records.append(rec)
    return records


# Every learner-facing checkbox question has a nonempty correct selection.
from generator_policy import nonempty_checkbox as _nonempty_checkbox
for _policy_name in ['batch', 'generate', 'generate_checkbox', 'generate_easy', 'generate_moderate']:
    globals()[_policy_name] = _nonempty_checkbox(globals()[_policy_name])

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--difficulty',choices=['easy','moderate','hard'],default='moderate')
    parser.add_argument('--count',type=int,default=5);parser.add_argument('--seed',type=int,default=0)
    parser.add_argument('--format',choices=['json'],default='json')
    parser.add_argument('--replay-source',choices=list(PROFILES))
    args=parser.parse_args()
    try: records=[replay_source(args.replay_source)] if args.replay_source else batch(args.difficulty,args.count,args.seed)
    except (ValueError,KeyError) as error:parser.error(str(error))
    print(json.dumps(records,indent=2))
