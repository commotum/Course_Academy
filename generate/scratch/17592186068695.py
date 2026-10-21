#!/usr/bin/env python3
"""Graphical continuity at a specified point (math basis1356); finite-catalog generation and replenishment.

Observed profiles reproduce every source component with numeric x-coordinate
slots and image-role slots. Explicit observed replay preserves missing fields,
missing correct refs and duplicate legacy fields. Defaults complete supported
source-shaped families with one radio field. Curves at changed parameters are
Matplotlib renderings of the documented geometric recipes, not source samplers.

Easy: select one continuous function among five graphs, at integer coordinate.
Moderate: check three integer positions on one graph; three checkbox fields.
Hard (authored): same three-point reading at half-unit coordinates, with a
removable point discontinuity AND a jump in the graph; exactly three local
checks and no calculus/limit calculations asked of the learner. No progression.
Historical observed replay retains radio banks; normal moderate/hard output uses
the current three-checkbox source contract. All samplers choose a complete
graph/bank profile before coordinate parameters.
Unlabelled source ordinates are schematic; exact branch formulas are authored
realizations of inspected topology, not recovered source formulas.
"""
from __future__ import annotations
import argparse, copy, hashlib, json, random, re, sys, uuid, os
os.environ.setdefault('MPLCONFIGDIR','/tmp/mpl-continuity')
from pathlib import Path
import sympy as sp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

KP_ID=17592186068695
KP_UUID='6cd6c125-ecaf-5847-a802-ec1b3594a15c'
TITLE='Determining Whether a Function Is Continuous at a Given Point'
VERSION='continuity-graph-7'
ROOT=Path(__file__).with_suffix('')
SOURCE=json.loads((ROOT/'source.json').read_text())
QUESTIONS={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
CURRENT_SOURCE=json.loads((ROOT/'current-source.json').read_text())
CURRENT_QUESTIONS={q[':question/math-academy-id']:q for q in CURRENT_SOURCE['record'][':knowledge-point/questions']}
X=sp.Symbol('x',real=True)
NS=uuid.UUID(KP_UUID)
ROMAN=['I','II','III']


def rat(v):return sp.Rational(str(v))
def tex(v):return sp.latex(rat(v))
def plain(v):return str(rat(v))
def digest(o):return hashlib.sha256(json.dumps(o,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(s):return str(uuid.uuid5(NS,s))
def segments(points):
    """Exact line-segment realization of a source branch (open external ends)."""
    out=[]
    for (a,c),(b,d) in zip(points,points[1:]):
        a,b,c,d=map(rat,(a,b,c,d));out.append({'lo':str(a),'hi':str(b),'expr':str(c+(d-c)*(X-a)/(b-a))})
    return out

def graph(*branches, values=None, holes=None, poles=None, bounds=(-4,4,-4,4), notes='', extend=True):
    ss=[];vs={}
    for b in branches:
        ss.extend(segments(b))
        for a,c in b[1:-1]:vs[str(rat(a))]=str(rat(c))
    if extend and ss:
        ss[0]['lo']=str(rat(bounds[0]));ss[-1]['hi']=str(rat(bounds[1]))
    vs.update({str(rat(k)):str(rat(v)) for k,v in (values or {}).items()})
    for a in (holes or []):vs.pop(str(rat(a)),None)
    return {'segments':ss,'values':vs,'holes':[str(rat(a)) for a in (holes or [])],
            'poles':poles or [],'bounds':list(map(str,bounds)),'notes':notes}

def pole(a,sign_left,sign_right,offset=0,bounds=(-4,4,-4,4),values=None):
    a=rat(a);lo,hi=map(rat,bounds[:2]);f1=rat(offset)+rat(sign_left)/(X-a)**2;f2=rat(offset)+rat(sign_right)/(X-a)**2
    return {'segments':[{'lo':str(lo),'hi':str(a),'expr':str(f1)}, {'lo':str(a),'hi':str(hi),'expr':str(f2)}],
            'values':{str(rat(k)):str(rat(v)) for k,v in (values or {}).items()},'holes':[],
            'poles':[str(a)],'bounds':list(map(str,bounds)),'notes':'Dashed guide at excluded vertical asymptote; no curve traversal arrows.'}

# Per-original geometric recipes, independently transcribed from all32 rasters.
G={}
def add(prefix,g):G[prefix]=g
add('4020dd89',pole(-2,-1,1,2))
add('4a009c92',graph([(-4,3),(-3.5,3.7),(-2.6,2.3),(-2,3)], [(-2,1),(-1,1),(0,.8),(2,-2)],values={-2:1}))
add('56576892',graph([(-4,4),(-2,3),(0,2),(4,0)],values={-2:1},holes=[-2]))
G['56576892']['values']['-2']='1'
add('f4a28f88',graph([(-3,-2),(-2,3),(-1,1.2),(0,1),(1,.75),(3,-3)],values={1:-1},holes=[1]))
G['f4a28f88']['values']['1']='-1'
add('29ff22e9',pole(-2,-1,-1,3))
add('0a31db89',graph([(-.5,-1),(2,4),(4.5,-1)],values={2:2},holes=[2]))
G['0a31db89']['values']['2']='2'
add('8c2cca8f',pole(2,-1,1,2,bounds=(-2.5,6,-2,6)))
add('fdd6b61f',graph([(-2,4),(0,1),(1,1.5),(2,3),(2.7,-1),(4,-1.7),(5,-3)],bounds=(-2.5,6,-2,6)))
add('56a689e2',pole(2,1,1,1,bounds=(-4,4,-1,5)))
add('4ad2a8ae',graph([(-2,3),(-1,3.5),(0,3),(1,3.5),(2,3)],[(2,2),(2.7,3),(3.5,1.2),(4.8,3.5),(6,-.5)],values={2:2},bounds=(-2.5,6,-2,6)))
add('42e1d990',graph([(-1,-2),(2,3),(5,3)],[(5,-2),(7,-2)],values={5:-2},bounds=(-1.5,7.5,-3.5,4)))
add('d124370f',graph([(-1,-2),(2,-2)],[(2,2.5),(3,0),(4,-1.5),(5,-2),(6,-1.5),(7,0),(7.5,1.5)],values={2:-2},bounds=(-1.5,7.5,-3.5,4)))
add('17fc3c79',pole(5,-1,1,0,bounds=(-1.5,7.5,-3.5,4)))
add('76a1b2ca',graph([(-1,-.4),(5,2),(7.5,3)],values={5:-2},holes=[5],bounds=(-1.5,7.5,-3.5,4)))
G['76a1b2ca']['values']['5']='-2'
add('135973e3',pole(5,-1,-1,0,bounds=(-1.5,7.5,-3.5,4)))
add('c6f0914f',graph([(-2,5),(-1,2.5),(0,2),(1,1.5),(2,1),(3,-1),(4,-4)],values={2:2},holes=[2]))
G['c6f0914f']['values']['2']='2'
add('c2f85d1a',pole(0,-1,1,0,values={0:0}));G['c2f85d1a']['guides']=[]
add('14349b3d',graph([(-4,3),(-3.5,3.8),(-2.6,2.4),(-1.7,3.3),(-.5,2.8),(0,3)],[(0,2),(1,2.1),(2,1.5),(3,2.7),(4,1.4)],values={0:2}))
add('3073f651',graph([(-4,5),(0,1),(4,5)],values={0:0},holes=[0]))
G['3073f651']['values']['0']='0'
add('c95d9944',graph([(-4,1.5),(0,1.5)],values={0:1.5},extend=False))
G['c95d9944']['segments'].append({'lo':'0','hi':'4','expr':'1+1/x**2'})
G['c95d9944']['poles']=['0'];G['c95d9944']['guides']=[]
# Moderate source graphs retain nonqueried holes and jumps as context.
add('d9cf9a5c',graph([(-2,-1),(-1,1),(0,0),(1,-1)],[(1,-1),(2,-.8),(3,-.2)],values={1:2},bounds=(-2.5,5.5,-3.5,3.5),extend=False))
G['d9cf9a5c']['segments'][0]['lo']='-5/2'
G['d9cf9a5c']['segments'] += [{'lo':'3','hi':'4','expr':'-1/(x-4)**2+2/(x-4)**2-6/5'}, {'lo':'4','hi':'11/2','expr':'1-1/(x-4)**2'}]
G['d9cf9a5c']['values']['3']='-1/5';G['d9cf9a5c']['poles']=['4']
# The left pole branch tends +infinity; choose its offset to meet x=3 exactly.
G['d9cf9a5c']['segments'][-2]['expr']='1/(x-4)**2-6/5'
add('43544a1b',graph([(-9,-2),(-7,-2)],[(-7,-4),(-6,-1.5),(-4,0),(-2,-2),(-1,-4),(0,-3.5),(2,3)],values={-7:-4,-1:0},holes=[-1],bounds=(-9,3,-5,3)))
G['43544a1b']['values']['-1']='0'
add('d1d91b2d',graph([(-2.5,-2.5),(-1,-1)],[(-1,1),(-.5,.15),(0,0),(.5,-.2),(1,-1)],[(1,-1),(1.5,-.5),(2,-.2),(3,.5),(4.5,1)],values={-1:-1,1:2},bounds=(-2.5,4.5,-3,3)))
add('3c0dc4b8',pole(-2,-1,-1,3,bounds=(-3.5,3.5,-5,3)))
# Replace right branch by rising pole branch followed by a closed cusp at0.
G['3c0dc4b8']['segments']=[{'lo':'-7/2','hi':'-2','expr':'1-1/(x+2)**2'}, {'lo':'-2','hi':'0','expr':'5/4-1/(x+2)**2'},*segments([(0,1),(1,-.8),(2,-1.4),(3.5,-1.8)])]
G['3c0dc4b8']['values']={'0':'1','1':'-4/5','2':'-7/5'}
add('890e7eaf',graph([(-3.5,2),(-2,2),(-1.5,.5),(0,-.8),(1,-1)],[(1,2),(3,0),(4.5,-1.5)],values={1:2},bounds=(-3.5,4.5,-3.5,3.5)))
# Solution plots highlight only the source's assessed continuous neighborhoods.
ALIASES={'63e7a219':'f4a28f88','d8720531':'d124370f','90c2fbe9':'c6f0914f','95967eb8':'d9cf9a5c','57415045':'d1d91b2d','7c96c401':'890e7eaf'}
for alias,base in ALIASES.items():G[alias]=copy.deepcopy(G[base])
# q48082's original solution image reverses the hole/filled marker positions:
# the filled point lies on the curve; an isolated upper open circle is annotation.
# Raw evidence records that asset separately; normal solution uses the corrected
# same function as its answer option. It cannot support a claim of a hole at2.
G['90c2fbe9']['holes']=[];G['90c2fbe9']['values']['2']='1'
G['90c2fbe9']['open_annotations']=[['2','2']];G['90c2fbe9']['marked_values']=['2']
add('e395863c',{'segments':[{'lo':'-5/2','hi':'0','expr':'1/x'},{'lo':'0','hi':'5/2','expr':'1/x'}],'values':{},'holes':[],'poles':['0'],'bounds':['-5/2','5/2','-7/2','7/2'],'notes':'Canonical y=1/x; labelled unit x and y scales.'})

SPECS={
 'q-48039':{'level':'easy','targets':[-2],'correct':'f4a28f88','context':[1]},
 'q-48081':{'level':'easy','targets':[2],'correct':'fdd6b61f','context':[]},
 'q-69782':{'level':'easy','targets':[5],'correct':'d124370f','context':[2]},
 'q-48082':{'level':'easy','targets':[0],'correct':'c6f0914f','context':[2]},
 'q-102106':{'level':'moderate','targets':[-1,2,4],'graph':'d9cf9a5c','correct':'I and II only'},
 'q-78133':{'level':'moderate','targets':[-7,-4,-1],'graph':'43544a1b','correct':'II only'},
 'q-102115':{'level':'moderate','targets':[-1,1,3],'graph':'d1d91b2d','correct':'III only'},
 'q-78131':{'level':'moderate','targets':[-2,0,2],'graph':'3c0dc4b8','correct':'II and III only'},
 'q-78132':{'level':'moderate','targets':[-2,1,3],'graph':'890e7eaf','correct':'I and III only'},
}
TEMPLATES={**{k:v['level'] for k,v in SPECS.items()},'hard_jump_and_hole':'hard'}
BANKS={'q-102106':['I only','II only','I and II only','I and III only','I, II and III'],
       'q-78133':['I only','II only','III only','I and II only','II and III only']}
ASSET_REFS={Path(r).stem[:8]:r for r in re.findall(r'images/[\w/]+\.png',json.dumps(SOURCE))}


def transformed(g,p):
    """Build exact graph objects from complete affine coordinate slots."""
    s,h,k=map(rat,(p['scale'],p['shift'],p['vertical']))
    out=copy.deepcopy(g);out['segments']=[]
    for b in g['segments']:
        e=sp.sympify(b['expr'],locals={'x':X},evaluate=False)
        # Retain raw poles before CAS simplification, including cancelled holes.
        denominators=[node.base for node in sp.preorder_traversal(e) if isinstance(node,sp.Pow) and node.exp.is_number and node.exp<0]
        excluded=sorted(set(root for denominator in denominators for root in sp.solve(denominator,X)),key=str)
        out['segments'].append({'lo':str(s*rat(b['lo'])+h),'hi':str(s*rat(b['hi'])+h),
          'expr':str(e.subs(X,(X-h)/s)+k),'raw_excluded':[str(s*a+h) for a in excluded if a.is_real]})
    out['values']={str(s*rat(a)+h):str(rat(v)+k) for a,v in g['values'].items()}
    out['holes']=[str(s*rat(a)+h) for a in g['holes']]
    out['poles']=[str(s*rat(a)+h) for a in g['poles']]
    if 'marked_values' in g:out['marked_values']=[str(s*rat(a)+h) for a in g['marked_values']]
    if 'guides' in g:out['guides']=[str(s*rat(a)+h) for a in g['guides']]
    if 'open_annotations' in g:out['open_annotations']=[[str(s*rat(a)+h),str(rat(v)+k)] for a,v in g['open_annotations']]
    bounds=[s*rat(g['bounds'][0])+h,s*rat(g['bounds'][1])+h,rat(g['bounds'][2])+k,rat(g['bounds'][3])+k]
    width=bounds[1]-bounds[0];height=bounds[3]-bounds[2]
    if bounds[0]>=0:bounds[0]=-width/12
    if bounds[1]<=0:bounds[1]=width/12
    if bounds[2]>=0:bounds[2]=-height/12
    if bounds[3]<=0:bounds[3]=height/12
    # Outer segments are schematic clipped continuations, not finite endpoints.
    # Keep the real zero axes visible after translation; never relocate y-axis.
    out['segments'][0]['lo']=str(bounds[0]);out['segments'][-1]['hi']=str(bounds[1])
    out['bounds']=list(map(str,bounds))
    return out


def inspect_at(g,a):
    """Check actual displayed graph object: both sides, defined value, agreement."""
    a=rat(a);left=[];right=[];value=None
    for b in g['segments']:
        lo,hi=rat(b['lo']),rat(b['hi']);e=sp.sympify(b['expr'],locals={'x':X})
        if lo<a<=hi:left.append(sp.limit(e,X,a,dir='-'))
        if lo<=a<hi:right.append(sp.limit(e,X,a,dir='+'))
        if lo<a<hi and str(a) not in b.get('raw_excluded',[]) and str(a) not in g['holes'] and str(a) not in g['poles']:
            z=e.subs(X,a)
            if z.is_finite:value=z
    # Internal shared knots belong to the connected polyline even if not values.
    if str(a) in g['values']:value=rat(g['values'][str(a)])
    def unique(vals):return vals[0] if vals and all(sp.simplify(v-vals[0])==0 for v in vals[1:]) else None
    l,r=unique(left),unique(right)
    exists=l is not None and r is not None and l.is_finite is True and r.is_finite is True and sp.simplify(l-r)==0
    matches=bool(exists and value is not None and sp.simplify(value-l)==0)
    return {'left':str(l),'right':str(r),'value':str(value),'defined':value is not None,'limit_exists':bool(exists),'limit_matches_value':matches,'continuous':matches}


def render_plot(prefix,p,targets,observed=False,highlight=False):
    base=G[ALIASES[prefix]] if prefix=='90c2fbe9' and not observed else G[prefix]
    g=transformed(base,p)
    if observed and p=={'scale':1,'shift':0,'vertical':0}:
        return ASSET_REFS[prefix],g
    hard_scale=rat(p['scale'])==sp.Rational(1,2)
    ticks=list(range(int(sp.ceiling(rat(g['bounds'][0]))),int(sp.floor(rat(g['bounds'][1])))+1)) if hard_scale else targets
    data={'graph':g,'targets':list(map(str,targets)),'tick_values':list(map(str,ticks)),'tick_step':'1' if hard_scale else 'specified targets','highlight':highlight,'renderer':matplotlib.__version__,'renderer_version':VERSION}
    lo,hi,bottom,top=map(lambda z:float(rat(z)),g['bounds']);padding=.08*(top-bottom);data['render_bounds']=[lo,hi,bottom-padding,top+padding]
    key=digest(data);directory=ROOT/'plots';directory.mkdir(exist_ok=True)
    png=directory/(key+'.png');side=directory/(key+'.json')
    if png.exists() and side.exists():return str(png.resolve()),g
    fig,ax=plt.subplots(figsize=(4.5,3.9),dpi=130)
    lo,hi,bottom,top=data['render_bounds']
    for b in g['segments']:
        a,c=map(lambda z:float(rat(z)),(b['lo'],b['hi']));xx=np.linspace(a+(c-a)*1e-5,c-(c-a)*1e-5,180)
        fn=sp.lambdify(X,sp.sympify(b['expr'],locals={'x':X}),'numpy');yy=fn(xx)
        if np.isscalar(yy):yy=np.full_like(xx,yy)
        # Clipping handles infinite branches; never joins across excluded poles.
        ax.plot(xx,yy,color='#f11',lw=1.7,zorder=2)
        if highlight:
            for t in targets:
                tt=float(rat(t));m=np.abs(xx-tt)<.32*float(rat(p['scale']))
                if inspect_at(g,t)['continuous'] and m.any():ax.plot(xx[m],np.asarray(yy)[m],color='blue',lw=1.8,zorder=3)
    # Every excluded finite end is open unless a same-value neighbor connects it.
    endpoints={}
    for b in g['segments']:
        e=sp.sympify(b['expr'],locals={'x':X})
        for v,dr in ((rat(b['lo']),'+'),(rat(b['hi']),'-')):
            if float(v)<=lo+1e-8 or float(v)>=hi-1e-8:continue
            lim=sp.limit(e,X,v,dir=dr)
            if lim.is_finite is True:endpoints.setdefault((str(v),str(lim)),0);endpoints[(str(v),str(lim))]+=1
    for (a,v),count in endpoints.items():
        filled=g['values'].get(a)==v
        if filled or (count>1 and a not in g['holes'] and a not in g['values']):continue
        ax.scatter([float(rat(a))],[float(rat(v))],s=42,facecolors='white',edgecolors='#f11',zorder=5)
    # Interior holes need open marker derived from branch value separately.
    for a in g['holes']:
        v=None
        for b in g['segments']:
            if rat(b['lo'])<=rat(a)<=rat(b['hi']):
                z=sp.sympify(b['expr'],locals={'x':X}).subs(X,rat(a))
                if z.is_finite:v=z;break
        if v is not None:ax.scatter([float(rat(a))],[float(v)],s=42,facecolors='white',edgecolors='#f11',zorder=5)
    for a,v in g.get('open_annotations',[]):ax.scatter([float(rat(a))],[float(rat(v))],s=42,facecolors='white',edgecolors='#f11',zorder=5)
    for a,v in g['values'].items():
        status=inspect_at(g,a)
        # Mark specified singleton values only when discontinuity is visible.
        if not status['continuous'] or a in g.get('marked_values',[]):ax.scatter([float(rat(a))],[float(rat(v))],s=29,c='#f11',zorder=6)
    for a in g.get('guides',g['poles']):ax.axvline(float(rat(a)),ls='--',color='#888',lw=1,zorder=1)
    ax.set(xlim=(lo,hi),ylim=(bottom,top));ax.spines[['right','top']].set_visible(False)
    ax.spines['left'].set_position(('data',0))
    ax.spines['bottom'].set_position(('data',0))
    ax.set_xticks(list(map(lambda z:float(rat(z)),ticks)));ax.set_xticklabels(['$'+tex(t)+'$' for t in ticks]);ax.set_yticks([])
    if hard_scale:ax.grid(axis='x',color='#ddd',lw=.5,zorder=0)
    axis_x=0;axis_y=0
    ax.annotate('',xy=(hi,axis_y),xytext=(hi-.035*(hi-lo),axis_y),arrowprops={'arrowstyle':'->','color':'black','lw':1})
    ax.annotate('',xy=(axis_x,top),xytext=(axis_x,top-.035*(top-bottom)),arrowprops={'arrowstyle':'->','color':'black','lw':1})
    ax.annotate('$x$',xy=(hi,axis_y),xytext=(-4,7),textcoords='offset points',ha='right')
    ax.annotate('$y$',xy=(axis_x,top),xytext=(7,-4),textcoords='offset points',va='top')
    fig.tight_layout(pad=.6)
    origin=ax.transData.transform((0,0));unit=ax.transData.transform((1,1));height=fig.get_figheight()*fig.dpi
    data['pixel_transform']={'x_offset':float(origin[0]),'x_scale':float(unit[0]-origin[0]),'y_offset':float(height-origin[1]),'y_scale':float(origin[1]-unit[1])}
    # Unique temp files, atomic final PNG/sidecar writes; safe concurrent callers.
    tmp=directory/(key+'.'+uuid.uuid4().hex+'.png');fig.savefig(tmp,facecolor='white');plt.close(fig);tmp.replace(png)
    tmpj=directory/(key+'.'+uuid.uuid4().hex+'.json');tmpj.write_text(json.dumps(data,indent=2)+'\n');tmpj.replace(side)
    return str(png.resolve()),g


def subset_text(flags):
    names=[ROMAN[i] for i,z in enumerate(flags) if z]
    if len(names)==3:return 'I, II and III'
    if len(names)==2:return ' and '.join(names)+' only'
    if len(names)==1:return names[0]+' only'
    return 'None'


def parameterize_text(text,p):
    # Complete coordinate components only; no blind substitution inside prose.
    s,h=rat(p['scale']),rat(p['shift'])
    text=re.sub(r'x=(-?\d+(?:\.\d+)?)',lambda m:'x='+tex(s*rat(m[1])+h),text)
    # One malformed source omission is retained in raw replay, but its number varies.
    text=re.sub(r'at \$(-?\d+)\.\$',lambda m:'at $'+tex(s*rat(m[1])+h)+'.$',text)
    return text


def normalized_parameters(level,p,observed):
    if p is None:raise ValueError('Internal parameters required')
    if set(p)!={'scale','shift','vertical'}:raise ValueError('Parameters: scale, shift, vertical only')
    out={k:rat(v) for k,v in p.items()}
    if any(v.q!=1 for k,v in out.items() if k!='scale'):raise ValueError('Integer offsets only')
    if abs(out['shift'])>4 or abs(out['vertical'])>2:raise ValueError('Offset workload bounds exceeded')
    allowed=[sp.Rational(1,2)] if level=='hard' else [sp.Integer(1),sp.Integer(2)]
    if observed:allowed=[sp.Integer(1),sp.Integer(2)]
    if out['scale'] not in allowed:raise ValueError('Level-specific coordinate scale violated')
    return {k:int(v) if v.q==1 else str(v) for k,v in out.items()}


def compile_question(source_id,p,profile,level,seed):
    spec=SPECS[source_id];raw=profile in ('observed','current')
    src=CURRENT_QUESTIONS[source_id] if profile=='current' or (not raw and spec['level']=='moderate') else QUESTIONS[source_id]
    targets=[rat(p['scale'])*rat(a)+rat(p['shift']) for a in spec['targets']]
    if level=='hard' and sum(t.q==2 for t in targets)<2:raise ValueError('Hard requires at least two unlabelled half-unit target readings')
    asset_map={};graphs={}
    for ref in sorted(set(re.findall(r'images/[\w/]+\.png',json.dumps(src)))):
        prefix=Path(ref).stem[:8];path,obj=render_plot(prefix,p,targets,raw,prefix in ALIASES);asset_map[ref]=path;graphs[path]=obj
    def text_slots(text):
        text=parameterize_text(text,p)
        for ref,path in asset_map.items():text=text.replace(ref,path)
        return text
    problem=text_slots(src[':question/problem']);solution=text_slots(src[':question/worked-solution'])
    fields=[]
    source_fields=src.get(':question/answer-fields',[])
    if not raw and source_id=='q-48081':source_fields=source_fields[1:]
    if not raw and not source_fields:
        bank=BANKS[source_id];source_fields=[{':answer-field/key':'selection',':answer-field/type':{':db/ident':':answer-field.type/radio'},':answer-field/choices':[{':answer/value':v,':answer/type':{':db/ident':':answer.type/text'}} for v in bank],':answer-field/correct':{':answer/value':spec['correct']}}]
    for f in source_fields:
        ff={':answer-field/key':f[':answer-field/key'],':answer-field/type':f[':answer-field/type'][':db/ident'],':answer-field/choices':[]}
        for a in f.get(':answer-field/choices',[]):ff[':answer-field/choices'].append({':answer/type':a[':answer/type'][':db/ident'],':answer/value':text_slots(a[':answer/value'])})
        if ':answer-field/correct' in f:ff['_correct_value']=text_slots(f[':answer-field/correct'][':answer/value'])
        fields.append(ff)
    if level=='hard':
        # Authored scale reading keeps all original local checks and shared prose.
        problem=problem.replace('The curve $y=f(x)$ is shown above.', 'The curve $y=f(x)$ is shown above. Use the unit-spaced tick marks to locate the listed points.')
    if not raw:
        if source_id=='q-48081':
            correct_path=next(path for ref,path in asset_map.items() if Path(ref).stem.startswith(spec['correct']))
            opening,rest=solution.split('\n\n',1);solution=opening+'\n\n![]('+correct_path+')\n\n'+rest
        if source_id=='q-78132':solution=solution.replace('continuous $x=','continuous at $x=')
    q={':question/problem':problem,':question/worked-solution':solution}
    if ':question/difficulty' in src or not raw:q[':question/difficulty']=':question.difficulty/'+level
    if ':question/answer-fields' in src or not raw:q[':question/answer-fields']=fields
    statuses=[]
    if spec['level']=='easy':
        unique={}
        for a in fields[-1][':answer-field/choices']:unique[a[':answer/value']]=inspect_at(graphs[a[':answer/value']],targets[0])
        statuses=list(unique.values())
        if sum(z['continuous'] for z in statuses)!=1:raise ValueError('Whole graph bank is ambiguous')
    else:
        prompt_ref=next(iter(re.findall(r'!\[\]\(([^)]+)\)',problem)))
        statuses=[inspect_at(graphs[prompt_ref],t) for t in targets]
        if subset_text([s['continuous'] for s in statuses])!=spec['correct']:raise ValueError('Recipe topology contradicts inspected source key')
    return q,graphs,targets,statuses


def finalize(q,template,p,profile,level,seed,graphs,targets,statuses):
    # Identity excludes option order/profile aliases but preserves omissions/layout.
    core=copy.deepcopy(q)
    for f in core.get(':question/answer-fields',[]):f[':answer-field/choices'].sort(key=lambda a:json.dumps(a,sort_keys=True))
    content=digest({'version':VERSION,'knowledge_point':KP_ID,'question':core})
    q[':question/id']=uid(content)
    rng=random.Random(seed)
    for i,f in enumerate(q.get(':question/answer-fields',[])):
        f[':answer-field/id']=uid(content+':field:'+str(i));correct=f.pop('_correct_value',None)
        for a in f[':answer-field/choices']:
            a[':answer/id']=uid(f[':answer-field/id']+':'+a[':answer/type']+':'+a[':answer/value'])
        if correct is not None:
            found=[a for a in f[':answer-field/choices'] if a[':answer/value']==correct]
            if len(found)!=1:raise ValueError('Bank correct designation not unique')
            f[':answer-field/correct']=[':answer/id',found[0][':answer/id']]
        if len({(a[':answer/type'],a[':answer/value']) for a in f[':answer-field/choices']})!=len(f[':answer-field/choices']):raise ValueError('Whole bank has repeated option')
        rng.shuffle(f[':answer-field/choices'])
    # The assessed categorical task is invariant under affine graph translation.
    # A half-unit coordinate reading is meaningful hard bookkeeping; variable
    # aliases, vertical offset, and unqueried numeric point labels are excluded.
    task=digest({'template':template,'assessed_graphs':SPECS[template].get('graph',SPECS[template].get('correct')),
                 'topology':[s['continuous'] for s in statuses],'coordinate_reading':'half-unit' if level=='hard' else 'integer'})
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{
      'version':VERSION,'seed':seed,'template':template,'requested_level':level,'parameters':p,'bank_profile':profile,
      'source':{'database':'math','basis':(SOURCE if profile=='observed' else CURRENT_SOURCE)['basis'],'lineage':SOURCE['lineage']},
      'source_id':template,'content_fingerprint':content,'mathematical_fingerprint':task,'graphs':graphs,
      'targets':list(map(str,targets)),'half_unit_target_readings':sum(t.q==2 for t in targets),'continuity_checks':statuses,
      'eligible_for_learning':profile not in ('observed','current') or (template not in (('q-48081','q-102106','q-78133','q-48082') if profile=='observed' else ('q-48081','q-48082'))),
      'evidence_only':profile in ('observed','current') and template in (('q-48081','q-102106','q-78133','q-48082') if profile=='observed' else ('q-48081','q-48082')),
      'domain':'Graph branches with open external ends, exclusions and separately specified singleton values',
      'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__,'matplotlib':matplotlib.__version__},
      'authored_scope':level=='hard'}}


def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ('easy','moderate','hard'):raise ValueError('Unsupported level')
    if field_type not in (None,'radio',':answer-field.type/radio','checkbox',':answer-field.type/checkbox'):raise ValueError('Only source radio and checkbox fields supported')
    if profile not in (None,'observed','current','authored','normal'):raise ValueError('Unknown complete bank profile')
    rng=random.Random(seed);profile='authored' if profile is None else profile
    # A complete template/bank is selected first, then coordinate parameters.
    if template=='hard_jump_and_hole':template=rng.choice(['q-78133','q-102115'])
    if template is None:template=rng.choice(['q-78133','q-102115'] if level=='hard' else [k for k,v in SPECS.items() if v['level']==level])
    if template not in SPECS:raise ValueError('Unsupported source-shaped template')
    if level!='hard' and SPECS[template]['level']!=level:raise ValueError('Template level mismatch')
    if level=='hard' and template not in ('q-78133','q-102115'):raise ValueError('Hard needs jump + removable point roles')
    observed=profile in ('observed','current')
    if observed and level!=SPECS[template]['level']:raise ValueError('Raw source difficulty must be preserved')
    if parameters is None:
        parameters={'scale':1 if observed else ('1/2' if level=='hard' else rng.choice([1,2])), 'shift':0 if observed else rng.randint(-4,4),'vertical':0 if observed else rng.randint(-2,2)}
        if level=='hard':
            # Targets must include at least one half-integer, inherent in both banks.
            pass
    p=normalized_parameters(level,parameters,observed)
    q,graphs,targets,statuses=compile_question(template,p,profile,level,seed)
    return finalize(q,template,p,profile,level,seed,graphs,targets,statuses)

# Easy: one local check across five plots, observed4 complete graphical banks.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# Moderate: three specified integer points, observed5 graph families/banks.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# Hard: authored half-unit scales, exactly3 point checks with jump+hole roles.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)


def markdown(r):
    q=r['question'];lines=[q[':question/problem']]
    for f in q.get(':question/answer-fields',[]):
        lines+=['']
        for a in f[':answer-field/choices']:
            val=a[':answer/value'];lines.append('- '+('![]('+val+')' if a[':answer/type']==':answer.type/image' else val))
    lines+=['','Worked solution:','',q.get(':question/worked-solution','')]
    return '\n'.join(lines)


# Every learner-facing checkbox question has a nonempty correct selection.
import sys as _policy_sys
from pathlib import Path as _PolicyPath
_policy_sys.path.insert(0, str(next(p for p in _PolicyPath(__file__).resolve().parents if (p / "scripts/generator_policy.py").is_file())))
from scripts.generator_policy import nonempty_checkbox as _nonempty_checkbox
for _policy_name in ['generate', 'generate_easy', 'generate_hard', 'generate_moderate']:
    globals()[_policy_name] = _nonempty_checkbox(globals()[_policy_name])

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
    rs=[generate(l,args.seed+i,args.template,profile=args.profile) for l in (['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]) for i in range(args.count)]
    print(json.dumps(rs,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in rs))
