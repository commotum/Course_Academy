"""LOCAL draft: 2D endpoints → end-minus-start displacement → Euclidean norm.
Reuses baseline exact vector/schema helpers; all paths redirected BEFORE any call.
No publication, database operation, registration, or engine modification.
Evidence profiles preserve original omissions; normal completions are authored.
"""
import argparse, hashlib, json, os, random, re, sys, tempfile, uuid
from pathlib import Path
os.environ.setdefault('MPLCONFIGDIR','/tmp/course-academy-mpl-17592186059715-draft')
import sympy as sp
KP_ID=17592186059715
KP_UUID='7bc170fa-a70e-55af-8f3e-f4ea07431e30'
TITLE='Calculating a Vector From Position Vectors and then Computing its Magnitude'
VERSION='position-magnitude-all3-local-draft-1'
HERE=Path(__file__).with_suffix(''); ROOT=HERE.parents[2]
SOURCE=json.loads((HERE/'source.json').read_text())
ORIGINALS={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions'] if ':question/math-academy-id' in q}
SPECS={
 'q-18051':{'labels':['A','B'],'points':[[-4,1],[3,0]],'style':'position','family':'coordinate_ab'},
 'q-18052':{'labels':['P','Q'],'points':[[-2,2],[3,3]],'style':'position-displacement','family':'coordinate_pq'},
 'q-125118':{'labels':['P','Q'],'points':[[1,2],[-2,1]],'style':'position-displacement','family':'coordinate_pq_signed'},
 'q-18049':{'labels':['C','D'],'points':[[-1,3],[1,-2]],'style':'position','family':'coordinate_cd'},
 'q-18055':{'labels':['P','Q'],'points':[[1,1],[2,3]],'style':'grid','family':'graph_read'},
}
FAMILIES={s['family']:mid for mid,s in SPECS.items()}
DOMAINS={
 'easy':{'coordinate_bound':6,'difference_bound':6,'grid_increment':1,'rule':'printed nonnegative integer endpoints 0..6; two nonzero unequal components'},
 'moderate':{'coordinate_bound':5,'difference_bound':8,'grid_increment':1,'rule':'printed signed integer endpoints -5..5 with a negative coordinate, or positive unit-grid graph_read endpoints 1..4'},
 'hard':{'coordinate_bound':8,'difference_bound':12,'grid_increment':2,'rule':'graph_read only; signed integer endpoints -8..8, negative coordinate and at least one odd coordinate read between even ticks'},
}

def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def expression(v):
    v=v.replace(' ','');m=re.fullmatch(r'(\d*)\\sqrt\{(\d+)\}',v)
    if m:return sp.Integer(m[1] or 1)*sp.sqrt(int(m[2]))
    return sp.Integer(v)
def vector(x,y):return sp.latex(x*sp.Symbol('i')+y*sp.Symbol('j'))
def source_vector(x,y):return vector(x,y).replace(' ','')
def arrow(pair):return r'\overset{\to }{'+pair+'}'
def valid_points(points):
    if not isinstance(points,(list,tuple)) or len(points)!=2 or any(len(p)!=2 for p in points):raise ValueError('two 2D points required')
    if any(type(v) is not int for p in points for v in p):raise ValueError('integer coordinates required')
    if points[0]==points[1]:raise ValueError('distinct endpoints required')
    return [list(p) for p in points]
def check_domain(level,family,points):
    p,q=valid_points(points);d=[q[i]-p[i] for i in range(2)];lim=DOMAINS[level]
    if any(abs(v)>lim['coordinate_bound'] for pt in points for v in pt) or any(abs(v)>lim['difference_bound'] for v in d):raise ValueError('level coordinate/difference bounds')
    if not all(d) or abs(d[0])==abs(d[1]):raise ValueError('two unequal nonzero displacement components required')
    flat=p+q
    if level=='easy':
        if family=='graph_read' or min(flat)<0:raise ValueError('easy requires printed nonnegative endpoints')
    elif level=='moderate':
        if family=='graph_read':
            if not all(1<=v<=4 for v in flat):raise ValueError('moderate graph is positive unit-grid, coordinates 1..4')
        elif min(flat)>=0:raise ValueError('moderate printed family needs signed input')
    elif family!='graph_read' or min(flat)>=0 or not any(v%2 for v in flat):raise ValueError('hard needs signed two-unit graph reading with odd coordinate')

def bank(points,profile):
    p,q=points;dx,dy=q[0]-p[0],q[1]-p[1];n=dx*dx+dy*dy;correct=sp.sqrt(n)
    if profile=='method-derived':
        vals=[correct,sp.sqrt((q[0]+p[0])**2+(q[1]+p[1])**2),sp.Integer(abs(dx)+abs(dy)),sp.Integer(n),sp.sqrt(abs(dx)+abs(dy))]
        recipes=['correct end-minus-start and square/sum/root','add position vectors then square/sum/root','sum absolute displacement components without squares','square/sum without final root','sum absolute displacement components then root without squares']
    else:raise ValueError('unsupported normal bank profile')
    for i in range(len(vals)):
        if vals[i].is_real is not True or vals[i]<0:raise ValueError('invalid magnitude option')
        for j in range(i):
            if sp.simplify(vals[i]-vals[j])==0:raise ValueError('whole-bank ambiguity')
    return [sp.latex(v) for v in vals],recipes

def render_plots(points,labels,style,tick=1):
    """Same endpoint data, equal units, unique temporary PNG + atomic sidecar.
    Native source snapshots are reused ONLY for exact source anchors.
    """
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    key=digest({'points':points,'labels':labels,'style':style,'tick':tick,'version':VERSION,'render_revision':4 if any(pt[0]==0 and pt[1]>0 for pt in points) else 3})[:24]
    directory=HERE/'plots';directory.mkdir(parents=True,exist_ok=True)
    path=directory/(key+'.png');side=path.with_suffix('.json')
    if path.exists() and side.exists():return json.loads(side.read_text())
    p,q=points;xs=[0,p[0],q[0]];ys=[0,p[1],q[1]]
    margin=2.0;xl=[min(xs)-margin,max(xs)+margin];yl=[min(ys)-margin,max(ys)+margin]
    fig,ax=plt.subplots(figsize=(6,5),dpi=120);ax.set_xlim(xl);ax.set_ylim(yl);ax.set_aspect('equal',adjustable='box')
    if style=='grid':
        ax.set_xticks(range(int(xl[0])//tick*tick,int(xl[1])+1,tick));ax.set_yticks(range(int(yl[0])//tick*tick,int(yl[1])+1,tick))
        ax.grid(color='#b8b8b8',lw=.7);ax.spines[['top','right']].set_visible(False)
        ax.spines['left'].set_position('zero');ax.spines['bottom'].set_position('zero')
        ax.tick_params(labelsize=10,pad=5)
        for axis in [ax.xaxis,ax.yaxis]:
            from matplotlib.ticker import FuncFormatter
            axis.set_major_formatter(FuncFormatter(lambda v,pos: '' if v==0 else str(int(v))))
    else:ax.axis('off')
    ax.annotate('',xy=(xl[1],0),xytext=(xl[0],0),arrowprops={'arrowstyle':'->','color':'black','lw':1.3})
    ax.annotate('',xy=(0,yl[1]),xytext=(0,yl[0]),arrowprops={'arrowstyle':'->','color':'black','lw':1.3})
    ax.annotate('$x$',(xl[1],0),xytext=(-6,11) if style=='grid' else (-3,-18),textcoords='offset points');ax.annotate('$y$',(0,yl[1]),xytext=(8,-6),textcoords='offset points')
    origin_offset=(-16,-17)
    if style!='grid':
        import math
        rays=[(1,0),(0,1)]+[tuple(pt) for pt in points if any(pt)]
        candidates=[(-16,-17),(-16,12),(10,-17),(10,12)]
        def overlap(offset):
            return max((offset[0]*x+offset[1]*y)/(math.hypot(*offset)*math.hypot(x,y)) for x,y in rays)
        origin_offset=min(candidates,key=overlap)
    ax.annotate('$O$',(0,0),xytext=origin_offset,textcoords='offset points')
    for label,(x,y) in zip(labels,points):
        ax.plot(x,y,'o',color='#2779b8',ms=5,zorder=5)
        # Grid family contains labels alone: coordinates must be read from scale.
        text=label if style=='grid' else f'{label}({x},{y})'
        ax.annotate('$'+text+'$',(x,y),xytext=(9,12 if y>=0 else -20),textcoords='offset points',fontsize=12,zorder=6,bbox={'facecolor':'white','edgecolor':'none','pad':.4})
        if style!='grid':
            ax.annotate('',xy=(x,y),xytext=(0,0),arrowprops={'arrowstyle':'->','color':'#2876b9','lw':1.8})
            length=(x*x+y*y)**.5
            letter_offset=(9,0) if x==0 and y>0 else ((-9*y/length,9*x/length) if length else (8,8))
            ax.annotate('$'+label.lower()+'$',(x*.56,y*.56),xytext=letter_offset,textcoords='offset points',color='#2876b9')
    if style=='position-displacement':ax.annotate('',xy=q,xytext=p,arrowprops={'arrowstyle':'->','color':'#e69800','lw':1.8})
    if style!='grid':
        for endpoint,name in [((1,0),'i'),((0,1),'j')]:
            ax.annotate('',xy=endpoint,xytext=(0,0),arrowprops={'arrowstyle':'->','color':'#d96a28','lw':1.3})
            ax.annotate('$'+name+'$',endpoint,xytext=(5,-15) if name=='i' else (-12,5),textcoords='offset points',color='#d96a28')
    fig.tight_layout(pad=.9);fig.canvas.draw()
    pixel_points=[ax.transData.transform(pt).tolist() for pt in points]
    origin=ax.transData.transform((0,0)).tolist();unitx=ax.transData.transform((1,0)).tolist();unity=ax.transData.transform((0,1)).tolist()
    fd,tmp=tempfile.mkstemp(prefix=key+'-',suffix='.png',dir=directory);os.close(fd)
    try:fig.savefig(tmp,metadata={'Software':VERSION});os.replace(tmp,path)
    finally:plt.close(fig);Path(tmp).unlink(missing_ok=True)
    asset={'path':str(path.relative_to(ROOT)),'reference':str(path.relative_to(ROOT)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'role':'prompt','points':points,'labels':labels,'style':style,'grid_increment':tick,'renderer':'matplotlib','renderer_version':matplotlib.__version__,'dimensions':[720,600],'axes':{'xlim':xl,'ylim':yl,'equal_scale':True,'origin_pixel':origin,'unit_x_pixel':unitx,'unit_y_pixel':unity,'endpoint_pixels':pixel_points}}
    fd,tmp=tempfile.mkstemp(prefix=key+'-',suffix='.json',dir=directory);os.close(fd);Path(tmp).write_text(json.dumps(asset,indent=2)+'\n');os.replace(tmp,side)
    return asset

def source_asset(mid):
    ref=re.search(r'!\[\]\(([^)]+)\)',ORIGINALS[mid][':question/problem']).group(1)
    path=HERE/'source-plots'/Path(ref).name
    return {'path':str(path.relative_to(ROOT)),'reference':ref,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'role':'prompt','renderer':'original captured raster','points':SPECS[mid]['points'],'style':SPECS[mid]['style'],'geometric_proof':'plot-extraction.md native pixel calibration, not hash equality'}

def source_solution(mid,points):
    """Exact source masks with complete vector/component slots, never literal replay.
    Original stage count, punctuation, spacing and shared sentences remain fixed.
    """
    orig=ORIGINALS[mid].get(':question/worked-solution')
    if orig is None:return None
    old=SPECS[mid]['points'];p,q=points;d=[q[i]-p[i] for i in range(2)];od=[old[1][i]-old[0][i] for i in range(2)]
    # Replace longest exact complete components once into collision-safe slots.
    slots={}
    pairs=[(source_vector(*old[0]),source_vector(*p)),(source_vector(*old[1]),source_vector(*q)),(source_vector(*od),source_vector(*d))]
    for i,(before,after) in enumerate(pairs):
        # Complete expression matching; original masks contain these exact vectors.
        token=f'@@VECTOR{i}@@';orig=orig.replace(before,token);slots[token]=after
    for token,value in slots.items():orig=orig.replace(token,value)
    # Signed-square and evaluated-square rows are complete masks, preserving
    # source grouping distinctions ({2} vs (2)) for positive changed inputs.
    a,b=od;c,e=d
    signed_first=f'({c})' if c<0 else '{'+str(c)+'}'
    patterns={
      'q-125118':[(rf'\sqrt{{({a})^{{2}}+({b})^{{2}}}}',rf'\sqrt{{({c})^{{2}}+({e})^{{2}}}}')],
      'q-18049':[(rf'\sqrt{{{{{a}}}^{{2}}+({b})^{{2}}}}',rf'\sqrt{{{signed_first}^{{2}}+({e})^{{2}}}}')],
      'q-18055':[(rf'\sqrt{{{{{a}}}^{{2}}+({b})^{{2}}}}',rf'\sqrt{{{signed_first}^{{2}}+({e})^{{2}}}}')],
    }
    for before,after in patterns[mid]:orig=orig.replace(before,after)
    orig=orig.replace(rf'\sqrt{{{a*a}+{b*b}}}',rf'\sqrt{{{c*c}+{e*e}}}')
    new_root=rf'\sqrt{{{c*c+e*e}}}'
    simplified=sp.latex(sp.sqrt(c*c+e*e))
    terminal=new_root+(r' \\  & ='+simplified if simplified!=new_root else '')
    orig=orig.replace(rf'\sqrt{{{a*a+b*b}}}',terminal)
    if mid=='q-18055':
        orig=orig.replace('P(1,1)',f'P({p[0]},{p[1]})').replace('Q(2,3)',f'Q({q[0]},{q[1]})')
    return orig

def normal_solution(points,labels,graph=False,source_mid=None):
    p,q=points;dx,dy=q[0]-p[0],q[1]-p[1];n=dx*dx+dy*dy;a,b=labels;aa,bb=a.lower(),b.lower();v=arrow(a+b)
    if source_mid in ['q-125118','q-18049','q-18055']:
        # Retain observed formal/position-vector, subtraction, component,
        # signed-square, square-sum and radical stages under changed values.
        result=source_solution(source_mid,points)
        # An explicit coordinate subtraction row makes signs reviewable; this
        # authored addition is separate from exact raw replay.
        marker='Now, using the formula'
        row=f'The displacement components are $({q[0]})-({p[0]})={dx}$ and $({q[1]})-({p[1]})={dy}$.\n\n'
        return result.replace(marker,row+marker)
    root=rf'\sqrt{{{n}}}';simplified=sp.latex(sp.sqrt(n));terminal=root+(r' \\ &= '+simplified if simplified!=root else '')
    intro=(f'From the picture, we obtain ${a}({p[0]},{p[1]})$ and ${b}({q[0]},{q[1]})$. So, we have' if graph else 'We have')
    return (intro+'\n\n$$\n'+rf'\begin{{aligned}} & {arrow("O"+a)}={aa}={source_vector(*p)}, \\ & {arrow("O"+b)}={bb}={source_vector(*q)}.\end{{aligned}}'+'\n$$\n\n'
      +f'Expressing ${v}$ as the difference of position vectors, we obtain:\n\n$$\n'
      +rf'\begin{{aligned}}{v} &= {arrow("O"+b)}-{arrow("O"+a)} \\ &= {bb}-{aa} \\ &= ({source_vector(*q)})-({source_vector(*p)}) \\ &= {source_vector(dx,dy)}\end{{aligned}}'+'\n$$\n\n'
      +f'The displacement components are $({q[0]})-({p[0]})={dx}$ and $({q[1]})-({p[1]})={dy}$.\n\n'
      +'Now, using the formula for the magnitude of a vector, we get\n\n$$\n'
      +rf'\begin{{aligned}}|{v}| &= \sqrt{{({dx})^{{2}}+({dy})^{{2}}}} \\ &= \sqrt{{{dx*dx}+{dy*dy}}} \\ &= {terminal}.\end{{aligned}}'+'\n$$')

def prompt(mid,points,asset,raw=False):
    a,b=SPECS[mid]['labels'];p,q=points
    if raw:
        original=ORIGINALS[mid][':question/problem'];old=SPECS[mid]['points']
        ref=re.search(r'!\[\]\(([^)]+)\)',original).group(1)
        original=original.replace(ref,asset['reference'])
        # Coordinate tuples only; complete component slots preserve all wording.
        for label,before,after in zip([a,b],old,points):
            original=re.sub(r'\b'+label+r'\(-?\d+,\s*-?\d+\)',f'{label}({after[0]},'+(' ' if mid in ['q-18051','q-18052'] else '')+f'{after[1]})',original)
        return original
    if SPECS[mid]['style']=='grid':return f"![]({asset['reference']})\n\nPoints ${a}$ and ${b}$ are shown in the picture above. Find $|{arrow(a+b)}|$."
    if mid in ['q-125118','q-18049']:return prompt(mid,points,asset,True)
    return f"![]({asset['reference']})\n\nLet ${a}({p[0]}, {p[1]})$ and ${b}({q[0]}, {q[1]})$. Find $|{arrow(a+b)}|$."

def build(level,seed,mid,points,profile,raw=False,scale=None):
    points=valid_points(points);p,q=points;d=[q[i]-p[i] for i in range(2)];n=sum(v*v for v in d)
    labels=SPECS[mid]['labels'];style=SPECS[mid]['style'];tick=DOMAINS[level]['grid_increment']
    asset=source_asset(mid) if raw and points==SPECS[mid]['points'] else render_plots(points,labels,style,tick)
    problem=prompt(mid,points,asset,raw);solution=source_solution(mid,points) if raw else normal_solution(points,labels,style=='grid',mid)
    values=[];recipes=[]
    if raw and mid in ['q-18051','q-18052']:
        source_values=[a[':answer/value'] for a in ORIGINALS[mid][':question/answer-fields'][0][':answer-field/choices']]
        values=[v if scale==1 else sp.latex(scale*expression(v)) for v in source_values]
        recipes=[f'opaque observed homogeneous evidence: scale * ({v}); intent unresolved' for v in source_values]
    elif not raw:values,recipes=bank(points,profile)
    if values:
        vals=[expression(v) for v in values]
        if any(sp.simplify(vals[i]-vals[j])==0 for i in range(len(vals)) for j in range(i)):raise ValueError('whole-bank ambiguity')
        if sum(sp.simplify(v-sp.sqrt(n))==0 for v in vals)!=1:raise ValueError('bank lacks unique actual magnitude')
    identity=digest({'version':VERSION,'level':None if raw else level,'problem':problem,'solution':solution,'bank':sorted(values),'presence':{k:k in ORIGINALS[mid] for k in [':question/difficulty',':question/answer-fields',':question/worked-solution']} if raw else None})
    qid=str(uuid.uuid5(uuid.UUID(KP_UUID),identity));question={':question/id':qid,':question/problem':problem}
    if not raw or ':question/difficulty' in ORIGINALS[mid]:question[':question/difficulty']=':question.difficulty/'+level
    if solution is not None:question[':question/worked-solution']=solution
    if raw:question[':question/math-academy-id']=mid
    if values:
        fid=str(uuid.uuid5(uuid.UUID(qid),'field:selection'));answers=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),'value:'+v)),':answer/type':':answer.type/math',':answer/value':v} for v in values]
        correct=next(a[':answer/id'] for a in answers if sp.simplify(expression(a[':answer/value'])-sp.sqrt(n))==0)
        random.Random(seed).shuffle(answers)
        field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers}
        if not raw:field[':answer-field/correct']=[':answer/id',correct]
        question[':question/answer-fields']=[field]
    sign_workload=[(1 if q[i]>0 else -1 if q[i]<0 else 0,1 if p[i]>0 else -1 if p[i]<0 else 0) for i in range(2)]
    # Translation is excluded, while signed subtractions, directed components,
    # supplied information and coordinate-scale reading remain assessed data.
    fingerprint=digest({'displacement':d,'subtraction_signs':sign_workload,'level':None if raw and ':question/difficulty' not in ORIGINALS[mid] else level,'reading':{'graph':style=='grid','tick':1 if raw else tick}})
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':question,'generation':{'version':VERSION,'template':SPECS[mid]['family'],'bank_profile':profile,'parameters':{'points':points,**({'scale':scale} if scale is not None else {})},'seed':seed,'source_ids':[mid],'basis':SOURCE['basis'],'lineage':SOURCE['lineage'],'domains':DOMAINS[level] if not raw else {'evidence_scale':[1,4],'source_anchor':SPECS[mid]['points']},'parameter_fingerprint':fingerprint,'content_fingerprint':identity,'recipes':recipes,'eligible_for_learning':not raw,'evidence_only':raw,'authored_completion':None if raw else 'Missing levels/fields/keys/solutions explicitly authored; source omissions retained only in raw evidence profiles','dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__},'assets':[asset]}}

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in DOMAINS:raise ValueError('difficulty must be easy|moderate|hard')
    if field_type not in [None,'radio',':answer-field.type/radio']:raise ValueError('only radio observed for normal completions')
    rng=random.Random(seed);parameters=parameters or {}
    if profile and profile.startswith('evidence:'):
        mid=profile.split(':',1)[1]
        if mid not in SPECS:raise ValueError('unknown evidence source')
        if template not in [None,mid,SPECS[mid]['family']]:raise ValueError('template/profile mismatch')
        if mid in ['q-18051','q-18052']:
            if set(parameters)-{'scale','points'}:raise ValueError('unknown evidence parameter')
            scale=parameters.get('scale',1)
            if type(scale) is not int or not 1<=scale<=4:raise ValueError('evidence scale must be integer 1..4')
            points=[[scale*v for v in p] for p in SPECS[mid]['points']]
            if 'points' in parameters and parameters['points']!=points:raise ValueError('opaque evidence requires homogeneous source scaling')
        else:
            if set(parameters)-{'points'}:raise ValueError('unknown evidence parameter')
            scale=None;points=parameters.get('points',SPECS[mid]['points']);check_domain(level,SPECS[mid]['family'],points)
        if ':question/difficulty' in ORIGINALS[mid] and level!='moderate':raise ValueError('rated source evidence must remain moderate')
        return build(level,seed,mid,points,profile,True,scale)
    if profile not in [None,'method-derived']:raise ValueError('unknown bank profile')
    allowed=list(FAMILIES) if level=='moderate' else (['graph_read'] if level=='hard' else [f for f in FAMILIES if f!='graph_read'])
    if template in SPECS:template=SPECS[template]['family']
    family=template or rng.choice(allowed)
    if family not in allowed:raise ValueError('template outside level scope')
    mid=FAMILIES[family]
    if parameters:
        if set(parameters)!={'points'}:raise ValueError('normal parameters contain points only')
        points=parameters['points'];check_domain(level,family,points)
        return build(level,seed,mid,points,'method-derived')
    for _ in range(10000):
        if level=='easy':lo,hi=0,6
        elif level=='moderate' and family=='graph_read':lo,hi=1,4
        else:lo,hi=-DOMAINS[level]['coordinate_bound'],DOMAINS[level]['coordinate_bound']
        points=[[rng.randint(lo,hi),rng.randint(lo,hi)] for i in range(2)]
        try:check_domain(level,family,points);bank(points,'method-derived')
        except ValueError:continue
        return build(level,seed,mid,points,'method-derived')
    raise RuntimeError('bounded domain sampling failed')

# EASY: authored printed small nonnegative integer endpoints; SAME two stages.
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
# MODERATE: observed signed-coordinate/unit-grid families with authored banks.
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
# HARD: authored signed graph reading at two-unit ticks, integer midpoint reading.
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=2);parser.add_argument('--format',choices=['json','markdown'],default='json');parser.add_argument('--template');parser.add_argument('--profile');parser.add_argument('--parameters',type=json.loads);args=parser.parse_args()
    if args.count<1:parser.error('count positive required')
    levels=list(DOMAINS) if args.difficulty=='all' else [args.difficulty]
    records=[generate(level,args.seed+i,args.template,parameters=args.parameters,profile=args.profile) for level in levels for i in range(args.count)]
    if args.format=='json':print(json.dumps(records,indent=2))
    else:
        for record in records:
            q=record['question'];print(q[':question/problem']);print('\n'+q.get(':question/worked-solution',''))
            for field in q.get(':question/answer-fields',[]):print('Choices: '+', '.join('$'+a[':answer/value']+'$' for a in field[':answer-field/choices']))
            print('\n---\n')
if __name__=='__main__':main()
