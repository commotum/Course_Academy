#!/usr/bin/env python3
"""Green area evaluation, frozen math basis 1356. Steps 3–7 only.

Each observed source is a real coefficient-mask recipe (numeric scalars and
omitted unit coefficients), used equally at its anchor and changed parameters.
Historical banks are opaque homogeneous-scale evidence profiles, ineligible for
learning. Defaults choose an observed family before coefficients and use complete
method-derived banks. Easy is authored ellipse evaluation from lesson tutorial;
moderate evaluates a one-piece trig loop; hard evaluates two polynomial segments.
No EDB, registration, network, SVG or image models.
"""
from __future__ import annotations
import argparse, copy, functools, hashlib, json, os, random, re, sys, tempfile, threading, uuid
from pathlib import Path
import sympy as sp
os.environ.setdefault('MPLCONFIGDIR','/tmp/green-area-mpl')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
ROOT=Path(__file__).resolve().parent/'17592186133897'
SOURCE=json.loads((ROOT/'source.json').read_text())
RECORD=SOURCE['record']; KP=17592186133897; VERSION='green-area-v8'
T,U=sp.symbols('t u',real=True)
A,B=sp.symbols('a b',positive=True)
QS={str(q[':db/id']):q for q in RECORD[':knowledge-point/questions']}
# family, a0,b0, level, scalar-slot maps for prompt and solution.
SPECS={
'17592186134376':('sin_sin2',3,2,'moderate',{0:A,1:B},{5:A,6:2*B,9:B,11:A,12:A*B,15:A*B,18:2*A*B,21:2*A*B,25:2*A*B,29:2*A*B/3,33:2*A*B/3,38:4*A*B/3}),
'17592186134386':('right_polynomial',2,1,'hard',{4:A,11:A},{}),
'17592186369399':('sin2_minus_sin',2,2,'moderate',{0:A,2:B},{5:2*A,7:B,9:A,11:B,12:A*B,15:A*B,18:2*A*B,21:2*A*B,25:2*A*B,29:2*A*B,34:2*A*B,40:4*A*B}),
'17592186369406':('sin2_cos',1,1,'moderate',{}, {5:2*A,19:2*A*B,24:2*A*B,28:2*A*B,32:2*A*B,37:2*A*B,43:4*A*B}),
'17592186369427':('left_polynomial',2,3,'hard',{4:A,6:B,12:A,13:B,14:B},{9:2*A,10:3*B,20:B,22:2*A,23:B,24:B,26:2*A*B,31:2*A*B,36:2*A*B,39:4*A*B}),
'17592186369448':('upper_polynomial',1,1,'hard',{10:B},{9:5*A,11:4*B,22:4*B,27:4*A*B,32:4*A*B,37:4*A*B,40:8*A*B}),
'17592186431051':('minus_cos_sin2',1,2,'moderate',{0:B},{5:2*B,10:B,12:A*B,17:A*B,22:2*A*B,27:2*A*B,31:2*A*B,35:2*A*B,40:2*A*B,46:4*A*B}),
'17592186431052':('lower_polynomial',1,2,'hard',{5:B,11:B},{9:5*A,11:4*B,22:4*B,27:4*A*B,32:4*A*B,37:4*A*B,40:8*A*B}),
}
FAMILY_SOURCE={v[0]:k for k,v in SPECS.items()}
FAMILY_LEVEL={v[0]:v[3] for v in SPECS.values()}|{'ellipse':'easy'}
def tex(v):return sp.latex(sp.sympify(v))
def scalar(v):return tex(v)
def coef(v):return '' if v==1 else scalar(v)
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def uid(v):return str(uuid.uuid5(uuid.NAMESPACE_URL,'green-area:'+v))
def num_mask(s, mapping,p):
    """Scalar slots extracted by position; never touch indices, powers or bounds."""
    matches=list(re.finditer(r'(?<![A-Za-z])\d+',s)); changes=[]
    for i,e in mapping.items():
        m=matches[i];changes.append((m.start(),m.end(),scalar(e.subs({A:p['a'],B:p['b']}))))
    for start,end,val in sorted(changes,reverse=True):s=s[:start]+val+s[end:]
    return s
# Omitted unit coefficients are complete coefficient-prefix slots, not number substitutions.
INSERTIONS={
 'sin2_cos':[(r'=\operatorname{sin}⁡2t',r'={a}\operatorname{sin}⁡2t'),(r'i+\operatorname{cos}⁡t',r'i+{b}\operatorname{cos}⁡t'),(r'i-\operatorname{sin}⁡t',r'i-{b}\operatorname{sin}⁡t'),(r'}\operatorname{sin}⁡2t\cdot (-\operatorname{sin}⁡t)',r'}{a}\operatorname{sin}⁡2t\cdot (-{b}\operatorname{sin}⁡t)'),(r'= -',r'= -')],
 'minus_cos_sin2':[(r'=-\operatorname{cos}⁡t',r'=-{a}\operatorname{cos}⁡t'),(r'=\operatorname{sin}⁡t\,i',r'={a}\operatorname{sin}⁡t\,i'),(r'sin}⁡2t\cdot \operatorname{sin}⁡t\,\text{d}t',r'sin}⁡2t\cdot {a}\operatorname{sin}⁡t\,\text{d}t')],
 'upper_polynomial':[(r'(t)={t}^{5}',r'(t)={a}{t}^{5}'),(r'i+{t}^{4}',r'i+{b}{t}^{4}'),(r'(t)=-t\,i',r'(t)=-{a}t\,i'),(r'(t)=-i',r'(t)=-{a}i'),(r'}{t}^{5}\cdot',r'}{a}{t}^{5}\cdot'),(r'(-t)\cdot',r'(-{a}t)\cdot')],
 'lower_polynomial':[(r'(t)={t}^{5}',r'(t)={a}{t}^{5}'),(r'(t)=-t\,i',r'(t)=-{a}t\,i'),(r'(t)=-i',r'(t)=-{a}i'),(r'}{t}^{5}\cdot',r'}{a}{t}^{5}\cdot'),(r'(-t)\cdot',r'(-{a}t)\cdot')],
 'right_polynomial':[(r'i - t^{3}',r'i - {b}t^{3}'),(r'i + tj',r'i + {b}tj')],
}
def fill(text,sid,kind,p):
    family,_,_,_,pm,sm=SPECS[sid]
    # Remove plot before numeric-slot extraction: filenames are not coefficients.
    plot=re.search(r'!\[\]\((.*?)\)',text);old=plot.group(0) if plot else None
    if old:text=text.replace(old,'@@PLOT@@')
    text=num_mask(text,pm if kind=='prompt' else sm,p)
    for orig,mask in INSERTIONS.get(family,[]):
        text=text.replace(orig,mask.replace('{a}',coef(p['a'])).replace('{b}',coef(p['b'])))
    if family=='sin2_cos' and kind=='solution':
        # The source's two omitted ab factors before the reduced integrals.
        text=text.replace(r'& =-{\int }',r'& =-'+coef(p['a']*p['b'])+r'{\int }')
    if old:text=text.replace('@@PLOT@@',old)
    return text

def geometry(family,p):
    a,b=map(sp.Integer,(p['a'],p['b']))
    if family=='ellipse':return [(a*sp.cos(T),b*sp.sin(T),0,2*sp.pi)],1,'y'
    if family=='sin_sin2':return [(a*sp.sin(T),b*sp.sin(2*T),0,sp.pi)],-1,'y'
    if family=='sin2_minus_sin':return [(a*sp.sin(2*T),-b*sp.sin(T),0,sp.pi)],-1,'x'
    if family=='sin2_cos':return [(a*sp.sin(2*T),b*sp.cos(T),sp.pi/2,3*sp.pi/2)],1,'x'
    if family=='minus_cos_sin2':return [(-a*sp.cos(T),b*sp.sin(2*T),sp.pi/2,3*sp.pi/2)],1,'y'
    if family=='left_polynomial':return [(-a*T**2,b*T**3,-1,1),(-a,-T,-b,b)],1,'y'
    if family=='right_polynomial':return [(a*T**2,-b*T**3,-1,1),(a,b*T,-1,1)],1,'y'
    if family=='upper_polynomial':return [(a*T**5,b*T**4,-1,1),(-a*T,b,-1,1)],1,'x'
    if family=='lower_polynomial':return [(a*T**5,-b*T**4,-1,1),(-a*T,-b,-1,1)],-1,'x'
    raise ValueError(family)
def calculate(family,p):
    seg,orientation,variable=geometry(family,p);ints=[]
    for x,y,l,h in seg:
        f=orientation*(x*sp.diff(y,T) if variable=='x' else -y*sp.diff(x,T))
        ints.append(sp.integrate(f,(T,l,h)))
    return sp.simplify(sum(ints)),seg,orientation,variable

_PLOT_LOCK=threading.RLock()
def serialized_plot(fn):
    @functools.wraps(fn)
    def wrapped(*args,**kwargs):
        with _PLOT_LOCK:return fn(*args,**kwargs)
    return wrapped

def route_leader(start,end,obstacles,canvas):
    """Shortest pixel-space polyline avoiding actual rendered text rectangles."""
    import heapq
    from matplotlib.path import Path as MplPath
    from matplotlib.transforms import Bbox
    blocks=[Bbox.from_extents(b.x0-3,b.y0-3,b.x1+3,b.y1+3) for b in obstacles]
    vertices=[tuple(start),tuple(end)]
    for b in blocks:
        for x in [b.x0-1,b.x1+1]:
            for y in [b.y0-1,b.y1+1]:
                if 0<x<canvas[0] and 0<y<canvas[1] and not any(c.contains(x,y) for c in blocks):vertices.append((x,y))
    def clear(a,b):return not any(MplPath([a,b]).intersects_bbox(box,filled=False) for box in blocks)
    distances={0:0};parents={};queue=[(0,0)]
    while queue:
        distance,node=heapq.heappop(queue)
        if distance!=distances[node]:continue
        if node==1:break
        for j,v in enumerate(vertices):
            if j==node or not clear(vertices[node],v):continue
            candidate=distance+float(np.hypot(v[0]-vertices[node][0],v[1]-vertices[node][1]))
            if candidate<distances.get(j,float('inf')):
                distances[j]=candidate;parents[j]=node;heapq.heappush(queue,(candidate,j))
    assert 1 in distances,'no clear leader route'
    indexes=[1]
    while indexes[-1]!=0:indexes.append(parents[indexes[-1]])
    route=[vertices[j] for j in reversed(indexes)]
    assert all(clear(a,b) for a,b in zip(route,route[1:])),'leader crosses rendered text'
    return route

@serialized_plot
def render_plots(family,p,output_dir=None):
    """Single-instance Matplotlib; unique temporary files + atomic final writes."""
    out=Path(output_dir or ROOT/'plots');out.mkdir(parents=True,exist_ok=True)
    key=digest([VERSION,family,p]);png=out/(key+'.png');side=out/(key+'.json')
    if png.exists() and side.exists():return str(png)
    seg,orientation,var=geometry(family,p);points=[]; arrays=[]
    for x,y,l,h in seg:
        ts=np.linspace(float(l),float(h),601)
        xf,yf=sp.lambdify(T,x,'numpy'),sp.lambdify(T,y,'numpy')
        xx=np.broadcast_to(xf(ts),ts.shape);yy=np.broadcast_to(yf(ts),ts.shape)
        arrays.append((ts,xx,yy));points.extend(zip(xx.tolist(),yy.tolist()))
    xs,ys=zip(*points)
    xr=max(max(xs)-min(xs),1);yr=max(max(ys)-min(ys),1)
    lo,hi=min(min(xs),0)-.25*xr,max(max(xs),0)+.4*xr
    bottom,top=min(min(ys),0)-.2*yr,max(max(ys),0)+.3*yr
    ratio=(hi-lo)/(top-bottom)
    # Widen/tall the canvas for long regions, retaining equal coordinate scale.
    # Labels use a reserved screen-space column rather than thin data-space gaps.
    width=5.8+min(3.0,max(0.0,ratio-2.0)*.5)
    height=4.6+min(3.0,max(0.0,1/ratio-2.0)*.5)
    with plt.rc_context({'font.family':'DejaVu Serif','font.size':12}):
        fig=plt.figure(figsize=(width,height),dpi=125)
        ax=fig.add_axes([.10,.13,.59,.74])
        ax.fill(xs,ys,color='#d6e8f5',zorder=0)
        callouts=[]
        for n,(ts,xx,yy) in enumerate(arrays):
            color='#ef9b00' if n==0 else '#d173ab';ax.plot(xx,yy,c=color,lw=1.7)
            for fraction in ([.18,.42,.68,.87] if len(seg)==1 else [.12,.88] if n==0 else [.27,.74]):
                k=int(fraction*(len(ts)-1));ax.annotate('',xy=(xx[k+9],yy[k+9]),xytext=(xx[k-9],yy[k-9]),arrowprops={'arrowstyle':'->','color':'black','lw':1})
            k=510 if n==0 else 300
            label='$C$' if len(seg)==1 else f'$C_{n+1}$'
            callouts.append((label,(float(xx[k]),float(yy[k])),color))
        a,b=p['a'],p['b']
        region={'ellipse':(.2*a,.35*b),'sin_sin2':(.65*a,.5*b),'minus_cos_sin2':(.65*a,.5*b),'sin2_minus_sin':(.35*a,-.5*b),'sin2_cos':(.35*a,-.5*b),'left_polynomial':(-.75*a,.3*b),'right_polynomial':(.75*a,.3*b),'upper_polynomial':(.5*a,.8*b),'lower_polynomial':(.5*a,-.8*b)}[family]
        callouts.append(('$D$',region,'#286eaa'))
        ax.set_xlim(lo,hi);ax.set_ylim(bottom,top);ax.set_aspect('equal',adjustable='box')
        for spine in ['top','right']:ax.spines[spine].set_visible(False)
        ax.spines['left'].set_position('zero');ax.spines['bottom'].set_position('zero')
        ax.spines['left'].set_visible(False);ax.spines['bottom'].set_visible(False)
        ax.annotate('',xy=(hi,0),xytext=(lo,0),arrowprops={'arrowstyle':'->','lw':.9});ax.annotate('',xy=(0,top),xytext=(0,bottom),arrowprops={'arrowstyle':'->','lw':.9})
        xt=sorted(set(int(round(v)) for v in [min(xs),max(xs)] if abs(v)>1e-5));yt=sorted(set(int(round(v)) for v in [min(ys),max(ys)] if abs(v)>1e-5))
        ax.set_xticks(xt);ax.set_yticks(yt)
        for tick,value in zip(ax.get_yticklabels(),yt):tick.set_verticalalignment('bottom' if value>0 else 'top')
        from matplotlib.transforms import ScaledTranslation
        for tick,value in zip(ax.get_xticklabels(),xt):
            tick.set_horizontalalignment('left' if value>0 else 'right')
            tick.set_transform(tick.get_transform()+ScaledTranslation((3 if value>0 else -3)/72,0,fig.dpi_scale_trans))
        axis_labels=[ax.annotate('$x$',xy=(hi,0),xytext=(-7,7),textcoords='offset points',ha='right',va='bottom'),ax.annotate('$y$',xy=(0,top),xytext=(7,7),textcoords='offset points',ha='left',va='bottom')]
        text_artists=[]
        for j,(label,anchor,color) in enumerate(sorted(callouts,key=lambda z:z[1][1])):
            # Vertically separated at fixed FIGURE positions, even when the axes
            # shrink under equal aspect. Screen-space leaders identify real anchors.
            yf=.28+.44*j/(len(callouts)-1)
            artist=ax.annotate(label,xy=anchor,xycoords='data',xytext=(.84,yf),textcoords='figure fraction',ha='left',va='center',color=color,annotation_clip=False)
            text_artists.append((label,artist,anchor))
        fig.canvas.draw();renderer=fig.canvas.get_renderer()
        # Annotation.get_window_extent includes its leader; inspect the actual
        # Text portion only, so harmless leaders do not count as label collisions.
        from matplotlib.text import Text
        boxes=[(label,Text.get_window_extent(artist,renderer),anchor) for label,artist,anchor in text_artists]
        axis_boxes=[Text.get_window_extent(artist,renderer) for artist in axis_labels]
        tick_boxes=[artist.get_window_extent(renderer) for artist in ax.get_xticklabels()+ax.get_yticklabels() if artist.get_visible()]
        assert all(not box.overlaps(tick) for box in axis_boxes for tick in tick_boxes),'axis title overlaps a scale label'
        for i,(_,box,_) in enumerate(boxes):
            assert all(not box.expanded(1.2,1.2).overlaps(other.expanded(1.2,1.2)) for _,other,_ in boxes[i+1:]),'rendered label collision'
            assert all(not box.expanded(1.2,1.2).overlaps(other) for other in axis_boxes+tick_boxes),'rendered axis/label collision'
            assert box.x0>=0 and box.y0>=0 and box.x1<fig.bbox.width and box.y1<fig.bbox.height,'clipped label'
        from matplotlib.path import Path as MplPath
        from matplotlib.patches import PathPatch
        from matplotlib.transforms import IdentityTransform
        leader_paths={}
        for label,box,anchor in boxes:
            start=(box.x0-8,(box.y0+box.y1)/2);end=ax.transData.transform(anchor)
            route=route_leader(start,end,[b for _,b,_ in boxes]+axis_boxes+tick_boxes,(fig.bbox.width,fig.bbox.height))
            patch=PathPatch(MplPath(route),transform=IdentityTransform(),fill=False,color='#929292',lw=.7,zorder=3)
            fig.add_artist(patch);leader_paths[label]=[[float(x),float(y)] for x,y in route]
        text_boxes={label:[float(v) for v in box.extents] for label,box,_ in boxes}
        anchor_pixels={label:[float(v) for v in ax.transData.transform(anchor)] for label,_,anchor in boxes}
        axes_bounds=[float(v) for v in ax.get_window_extent(renderer).extents]
        scale_x=float(ax.transData.transform((1,0))[0]-ax.transData.transform((0,0))[0]);scale_y=float(ax.transData.transform((0,1))[1]-ax.transData.transform((0,0))[1])
        assert abs(scale_x-scale_y)<1e-8,'coordinate-scale distortion'
        fd,tmp=tempfile.mkstemp(suffix='.png',prefix='render-',dir=out);os.close(fd)
        try:fig.savefig(tmp,facecolor='white');os.replace(tmp,png)
        finally:
            plt.close(fig)
            if os.path.exists(tmp):os.unlink(tmp)
    payload={'family':family,'parameters':p,'segments':[[str(v) for v in z] for z in seg],'orientation':orientation,'renderer':'Matplotlib','version':matplotlib.__version__,'python':sys.version.split()[0],'xlim':[lo,hi],'ylim':[bottom,top],'ticks':[xt,yt],'arrow_fractions':[[.18,.42,.68,.87]] if len(seg)==1 else [[.12,.88],[.27,.74]],'closed':True,'label_policy':'reserved figure-space column with leaders to exact-instance anchors','text_boxes_pixels':text_boxes,'anchor_pixels':anchor_pixels,'axes_bounds_pixels':axes_bounds,'unit_pixels':[scale_x,scale_y],'canvas_inches':[width,height],'label_collisions':0,'leader_text_collisions':0,'leader_paths_pixels':leader_paths,'axis_text_boxes_pixels':[[float(v) for v in box.extents] for box in axis_boxes],'tick_text_boxes_pixels':[[float(v) for v in box.extents] for box in tick_boxes]}
    fd,tmp=tempfile.mkstemp(suffix='.json',prefix='sidecar-',dir=out)
    with os.fdopen(fd,'w') as f:json.dump(payload,f,indent=2)
    os.replace(tmp,side);return str(png)

def method_bank(family,p):
    """Complete profile selected before p: each error follows the displayed method."""
    area,segments,orient,var=calculate(family,p);a,b=map(sp.Integer,(p['a'],p['b']))
    if FAMILY_LEVEL[family]=='moderate':
        # sin(2t) identity omitted factor2; missing /3 in primitive;
        # upper endpoint only; reversing orientation omitted.
        values=[area,2*a*b/3,4*a*b, -area, sp.Integer(0)]
        recipes=['area','omit_double_angle_factor','omit_primitive_divisor','omit_orientation_sign','drop_single_angle_factor_so_sin2t_integrates_to_zero']
    elif family=='ellipse':
        values=[area,-area,2*area,a*sp.pi,b*sp.pi]
        recipes=['area','wrong_orientation','omit_half_angle_divisor','omit_y_coefficient','omit_x_coefficient']
    else:
        n=2 if family in ['left_polynomial','right_polynomial'] else 4
        d=5 if n==2 else 9
        values=[area,2*a*b/d,n*a*b, -area,2*n*a*b]
        recipes=['area','omit_derivative_factor','upper_endpoint_only_and_omit_divisor','wrong_orientation','omit_primitive_divisor']
    if len(set(values))!=5:raise ValueError('Whole bank collision')
    return values,recipes

def raw_bank(sid,p,field):
    _,a0,b0,_,_,_=SPECS[sid];ratio=sp.Rational(p['a']*p['b'],a0*b0)
    vals=[]
    for answer in field[':answer-field/choices']:
        original=answer[':answer/value'];clean=original.replace('\\\\','\\');m=re.fullmatch(r'\\frac\{(\d+)\}\{(\d+)\}',clean)
        if m:value=sp.Rational(int(m[1]),int(m[2]))
        elif '\\pi' in clean:value=sp.Integer(clean.split('\\pi')[0])*sp.pi
        else:value=sp.Integer(clean)
        if '\\pi' in clean:
            pos=clean.index('\\pi');rendered=tex(value*ratio/sp.pi)+clean[pos:]
        else:rendered=tex(value*ratio)
        vals.append((value*ratio,rendered))
    return vals

def extra_endpoint_rows(family,p,solution):
    """Retain all source stages and add individually evaluated endpoint components."""
    a,b=p['a'],p['b']
    if FAMILY_LEVEL[family]=='moderate':
        k=sp.Rational(2*a*b,3)
        extra=r'\\  & ='+tex(k)+r'\cdot 1-'+tex(k)+r'\cdot (-1) '+r'\\  & ='+tex(k)+'-('+tex(-k)+') '
        # Before final row. Existing source substituted cubic endpoint row stays.
        pos=solution.rfind(r'\\  & =');return solution[:pos]+extra+solution[pos:]
    n=2 if family in ['left_polynomial','right_polynomial'] else 4;d=5 if n==2 else 9;k=n*a*b
    target=str(k)+r'\cdot \frac{2}{'+str(d)+'}'
    extra=tex(k)+r'\left(\frac{1^{'+str(d)+'}}{'+str(d)+r'}-\frac{(-1)^{'+str(d)+'}}{'+str(d)+r'}\right) '+r'\\  & ='+tex(k)+r'\left(\frac{1}{'+str(d)+r'}-\left(-\frac{1}{'+str(d)+r'}\right)\right) '+r'\\  & ='+target
    return solution.replace(target,extra)

def inferred_polynomial_solution(p):
    a,b=p['a'],p['b'];sid='17592186369427';sol=fill(QS[sid][':question/worked-solution'],sid,'solution',p)
    # Same positive traversal, reflected both coordinates; derivatives and substituted
    # components change sign together. Closing segment now has y=b t on [-1,1].
    sol=sol.replace('=-'+str(2*a)+'t', '='+str(2*a)+'t').replace('+'+str(3*b)+r'{t}^{2}', '-'+str(3*b)+r'{t}^{2}')
    sol=sol.replace(r'(t)=-j',r'(t)='+coef(b)+'j')
    sol=sol.replace(str(b)+r'{t}^{3}\cdot (-'+str(2*a)+'t)',r'(-'+str(b)+r'{t}^{3})\cdot '+str(2*a)+'t')
    sol=sol.replace('_{-'+str(b)+'}^{'+str(b)+'}(-t)',r'_{-1}^{1}('+coef(b)+'t)')
    return sol

def ellipse_solution(p):
    a,b=p['a'],p['b'];ab=a*b
    return ("First, let $P(x,y)=-y$ and $Q(x,y)=0.$\n\nOur simple, smooth, closed path $C$ is positively oriented, and\n\n"+r'$$\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}=0-(-1)=1.$$'+"\n\nSo, according to Green's theorem, we can write the area of the region $D$ enclosed by the curve $C$ as follows:\n\n"+r'$$\begin{aligned}\text{Area}(D)&=\iint_D\text{d}A\\&=\iint_D(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y})\,\text{d}A\\&=\oint_C P\,\text{d}x+Q\,\text{d}y\end{aligned}$$'+"\n\nSubstituting $P(x,y)=-y$ and $Q(x,y)=0,$ we get\n\n"+r'$$\oint_C P\,\text{d}x+Q\,\text{d}y=-\oint_C y\,\text{d}x.$$'+"\n\nThe derivative of $r(t)$ is\n\n"+r"$$r'(t)="+r'\langle -'+str(a)+r'\sin t,'+str(b)+r'\cos t\rangle.$$'+"\n\nTherefore, we can write our line integral as\n\n"+r'$$\begin{aligned}-\oint_C y\,\text{d}x&=-\int_0^{2\pi}'+str(b)+r'\sin t\cdot(-'+str(a)+r'\sin t)\,\text{d}t\\&='+str(ab)+r'\int_0^{2\pi}\sin^2 t\,\text{d}t\\&='+str(ab)+r'\int_0^{2\pi}\frac{1-\cos 2t}{2}\,\text{d}t\\&=\int_0^{2\pi}\left('+tex(sp.Rational(ab,2))+'-'+tex(sp.Rational(ab,2))+r'\cos 2t\right)\,\text{d}t\\&=\left['+tex(sp.Rational(ab,2))+'t-'+tex(sp.Rational(ab,4))+r'\sin 2t\right]_0^{2\pi}\\&=\left('+tex(ab*sp.pi)+r'-0\right)-\left(0-0\right)\\&='+tex(ab*sp.pi)+r'\end{aligned}$$'+"\n\nTherefore, we conclude that $\\text{Area}(D)="+tex(ab*sp.pi)+'.$')

# Easy: authored ellipse, a,b>=2 unequal so omitted-coordinate banks are complete.
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
# Moderate: all four observed trig substitution families, coefficients 1..8.
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
# Hard: both vertical/horizontal closing-segment families, coefficients 1..8.
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ('easy','moderate','hard'):raise ValueError('difficulty')
    if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('radio only')
    rng=random.Random(seed);raw=bool(profile and str(profile).startswith('original:'))
    if raw:
        sid=str(profile).split(':',1)[1]
        if sid not in SPECS:raise ValueError('unknown source profile')
        family,a0,b0,observed_level,_,_=SPECS[sid]
        if level!=observed_level:raise ValueError('source level mismatch; unrated authored hard')
        if template and template!=family:raise ValueError('template/profile mismatch')
    else:
        if profile not in (None,'method'):raise ValueError('unknown profile')
        families=[f for f,l in FAMILY_LEVEL.items() if l==level]
        family=template or rng.choice(families)
        if family not in families:raise ValueError('template outside difficulty')
        sid=FAMILY_SOURCE.get(family);a0,b0=(SPECS[sid][1:3] if sid else (2,3))
    if parameters is not None:
        if set(parameters)!={'a','b'}:raise ValueError('parameters a,b required')
        p=dict(parameters)
        if any(type(v)!=int or not 1<=v<=8 for v in p.values()):raise ValueError('integer coefficients 1..8')
        if family=='ellipse' and (min(p.values())<2 or p['a']==p['b']):raise ValueError('easy coefficients >=2 unequal')
    else:p={'a':rng.randint(2 if family=='ellipse' else 1,8),'b':rng.randint(2 if family=='ellipse' else 1,8)}
    # Profile chosen before parameters; every collision rejects the whole instance.
    for attempt in range(100):
        try:
            if raw:
                fields0=QS[sid][':question/answer-fields'];vals=[raw_bank(sid,p,f) for f in fields0]
                if any(len(set(v for v,_ in bank))!=len(bank) for bank in vals):raise ValueError('raw bank collision')
            else:values,recipes=method_bank(family,p)
            break
        except ValueError:
            if parameters is not None:raise
            p={'a':rng.randint(2 if family=='ellipse' else 1,8),'b':rng.randint(2 if family=='ellipse' else 1,8)}
    else:raise ValueError('no valid bank')
    area,segments,orientation,variable=calculate(family,p)
    if family=='ellipse':
        prompt="Use Green's theorem to find the area of the region $D$ enclosed by the curve $C$ parametrized as $r(t)="+str(p['a'])+r'\cos t\,i+'+str(p['b'])+r'\sin t\,j$ for $t\in[0,2\pi].$'
        solution=ellipse_solution(p)
    else:
        source=QS[sid];prompt=fill(source[':question/problem'],sid,'prompt',p)
        solution=fill(source[':question/worked-solution'],sid,'solution',p) if ':question/worked-solution' in source else (None if raw else inferred_polynomial_solution(p))
    anchor=p=={'a':a0,'b':b0}
    plot=render_plots(family,p)
    if raw and anchor:pass
    else:prompt=re.sub(r'!\[\]\(.*?\)',f'![]({plot})',prompt) if '![](' in prompt else prompt+f'\n\n![]({plot})'
    if not raw and family!='ellipse':
        solution=extra_endpoint_rows(family,p,solution)
        if FAMILY_LEVEL[family]=='moderate':solution=solution.replace('simple, smooth, closed','simple, piecewise-smooth, closed')
    q={':question/problem':prompt}
    if not raw or ':question/difficulty' in QS[sid]:q[':question/difficulty']=':question.difficulty/'+level
    if solution is not None:q[':question/worked-solution']=solution
    fields=[]
    if raw:
        for f,bank in zip(fields0,vals):
            field={':answer-field/key':f[':answer-field/key'],':answer-field/type':f[':answer-field/type'][':db/ident'],':answer-field/choices':[]}
            for a,(v,s) in zip(f[':answer-field/choices'],bank):field[':answer-field/choices'].append({':answer/type':a[':answer/type'][':db/ident'],':answer/value':s,'anchor_id':a[':answer/id']})
            if ':answer-field/correct' in f:field['correct_anchor']=f[':answer-field/correct'][':answer/id']
            fields.append(field)
    else:fields=[{':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':[{':answer/type':':answer.type/math',':answer/value':tex(v)} for v in values],'correct_index':0}]
    q[':question/answer-fields']=fields
    identity=digest([VERSION,level,prompt,solution,[(f[':answer-field/key'],f[':answer-field/type'],sorted(a[':answer/value'] for a in f[':answer-field/choices']),f.get('correct_anchor'),f.get('correct_index')) for f in fields],':question/difficulty' in q,':question/worked-solution' in q])
    q[':question/id']=uid(identity)
    for i,f in enumerate(fields):
        f[':answer-field/id']=uid(identity+f':field:{i}')
        correct=None
        for j,a in enumerate(f[':answer-field/choices']):
            a[':answer/id']=uid(identity+f':field:{i}:answer:'+a[':answer/value'])
            if ('correct_anchor' in f and a.get('anchor_id')==f['correct_anchor']) or j==f.get('correct_index'):correct=a[':answer/id']
            a.pop('anchor_id',None)
        f.pop('correct_index',None);f.pop('correct_anchor',None)
        if correct:f[':answer-field/correct']=[':answer/id',correct]
        rng.shuffle(f[':answer-field/choices'])
    # Mathematical identity: curve geometry/traversal and evaluation demand,
    # excluding complete bank, aliases and the incidental closing-segment speed.
    mathematical=digest([family,level,sorted(p.values()) if family=='ellipse' else [[str(x),str(y),str(l),str(h)] for x,y,l,h in segments],orientation,variable,'evaluate_area'])
    return {'knowledge_point':{'db_id':KP,'id':RECORD[':knowledge-point/id'],'title':RECORD[':knowledge-point/title']},'question':q,'generation':{'version':VERSION,'template':family,'profile':profile if raw else 'method','parameters':p,'seed':seed,'mathematical_fingerprint':mathematical,'content_identity':identity,'source_id':sid,'basis':1356,'lineage':SOURCE['lineage'],'eligible_for_learning':not raw,'evidence_only':raw,'bank_recipes':(['opaque homogeneous scale; intent unresolved'] if raw else recipes),'area':str(area),'plot':plot,'python':sys.version.split()[0],'sympy':sp.__version__,'matplotlib':matplotlib.__version__}}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=1);parser.add_argument('--format',choices=['markdown','json'],default='markdown');parser.add_argument('--template');parser.add_argument('--profile');a=parser.parse_args()
    records=[generate(level,a.seed+n,template=a.template,profile=a.profile) for level in (['easy','moderate','hard'] if a.difficulty=='all' else [a.difficulty]) for n in range(a.count)]
    if a.format=='json':print(json.dumps(records,indent=2))
    else:
        for r in records:
            q=r['question'];print(q[':question/problem']);print('\nChoices:');print('\n'.join(x[':answer/value'] for f in q[':question/answer-fields'] for x in f[':answer-field/choices']));print('\nWorked solution:\n'+q.get(':question/worked-solution','[not present in raw source]'))
if __name__=='__main__':main()
