"""Matplotlib renderer: exact segment geometry and opaque captured ink evidence.
No graph is sampled here; input includes the entire computed instance.
"""
import json, os, sys, tempfile, hashlib
from pathlib import Path
os.environ.setdefault('MPLCONFIGDIR','/tmp/kp17592186124472-mpl')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
from PIL import Image

BLUE='#2879ba'
def draw_segments(ax,g,solution=False):
    for s in g['segments']:
        x=np.linspace(s['a'],s['b'],301)
        if 'expression' in s:
            sy=sp.Symbol('x');e=sp.sympify(s['expression']);f=sp.lambdify(sy,e,'numpy');y=np.asarray(f(x))*np.ones_like(x)
        else:
            c=s['coefficients'];y=sum(float(sp.Rational(v))*x**i for i,v in enumerate(c))
        line,=ax.plot(x,y,color=BLUE,lw=2,zorder=3)
        for t,closed in [(s['a'],s['left_closed']),(s['b'],s['right_closed'])]:
            val=float(sp.sympify(s['expression']).subs(sp.Symbol('x'),t)) if 'expression' in s else sum(float(sp.Rational(v))*t**i for i,v in enumerate(c))
            ax.plot(t,val,'o',color=BLUE,mfc=BLUE if closed else 'white',ms=6,lw=1.5,zorder=4)
    if solution:
        if g['witness'] is not None:
            ax.axhline(g['witness'],color='black',ls=(0,(4,3)),lw=1.4,zorder=2)
        else:
            ax.axhline(g['test_height'],color='black',ls=(0,(4,3)),lw=1.4,zorder=2)

def render(data,path):
    if data['mode']=='raw':
        # The complete pixel coordinate cloud is a parameterized opaque raw profile.
        # This is evidence, not a claimed recovered polynomial.
        im=Image.open(data['asset']).convert('RGBA');w,h=im.size
        arr=np.asarray(im);alpha=arr[:,:,3]/255
        rgb=arr[:,:,:3]*alpha[:,:,None]+255*(1-alpha[:,:,None])
        is_ink=rgb.min(axis=2)<220
        ys,xs=np.nonzero(is_ink)
        fig=plt.figure(figsize=(w/100,h/100),dpi=100)
        ax=fig.add_axes([0,0,1,1]);ax.set_xlim(0,w);ax.set_ylim(h,0);ax.axis('off')
        # Affine coordinates apply to every ink point, including axes/labels/endpoints.
        # Positive diagonal maps preserve all intersections and hollow markers.
        sx,sy=data['scale'];cx,cy=w/2,h/2
        ax.scatter(cx+(xs+.5-cx)*sx,cy+(ys+.5-cy)*sy,c=rgb[ys,xs]/255,s=.52,marker='s',linewidths=0)
        side={'opaque':True,'width':w,'height':h,'python':sys.version.split()[0],'matplotlib':matplotlib.__version__,'ink_points':len(xs),'affine_scale':[sx,sy]}
    else:
        fig,axs=plt.subplots(2,2,figsize=(9,8),dpi=120)
        fig.subplots_adjust(left=.065,right=.965,bottom=.065,top=.935,wspace=.22,hspace=.32)
        layout=[]
        for i,(ax,g) in enumerate(zip(axs.flat,data['graphs'])):
            ax.set_xlim(-4.7,4.7);ax.set_ylim(-4.7,4.7)
            ax.set_aspect('equal');ax.set_xticks([]);ax.set_yticks([])
            for spine in ax.spines.values():spine.set_visible(False)
            ax.annotate('',xy=(4.65,0),xytext=(-4.65,0),arrowprops={'arrowstyle':'->','color':'black','lw':1.1})
            ax.annotate('',xy=(0,4.65),xytext=(0,-4.65),arrowprops={'arrowstyle':'->','color':'black','lw':1.1})
            # Panel and coordinate labels sit outside all curves/axis arrows.
            title=ax.text(.04,1.035,['I','II','III','IV'][i],transform=ax.transAxes,fontsize=14,clip_on=False)
            xlabel=ax.text(1.055,.5,'x',transform=ax.transAxes,fontsize=11,clip_on=False)
            ylabel=ax.text(.5,1.055,'y',transform=ax.transAxes,fontsize=11,clip_on=False)
            draw_segments(ax,g,data['solution'])
            if g['level']!='easy':
                # Only endpoint y-values receive reference tick labels. They are
                # explicitly tied to the corresponding dashed grid level.
                vals=sorted({sum(sp.Rational(v)*sp.Rational(t)**j for j,v in enumerate(s['coefficients'])) for s in g['segments'] for t in [s['a'],s['b']]})
                for exact_y in vals:
                    y=float(exact_y)
                    ax.axhline(y,color='#ddd',lw=.7,zorder=0)
                    ax.text(-4.85,y,f'{y:g}',ha='right',va='center',fontsize=9,clip_on=False)
            layout.append((ax,title,xlabel,ylabel,g))
        fig.canvas.draw();renderer=fig.canvas.get_renderer();boxes=[]
        for ax,*rest in layout:
            texts=[t for t in ax.texts if t.get_text()];g=rest[3]
            for i,t in enumerate(texts):
                for previous in texts[:i]:
                    assert not t.get_window_extent(renderer).overlaps(previous.get_window_extent(renderer)),'text/text overlap'
                bb=t.get_window_extent(renderer);boxes.append({'text':t.get_text(),'bbox':list(bb.bounds),'position':list(t.get_position())})
                assert bb.x0>=0 and bb.y0>=0 and bb.x1<=fig.bbox.width and bb.y1<=fig.bbox.height,'clipped label'
                # Measure actual text boxes against every curve/marker and axis shaft.
                expanded=bb.expanded(1.03,1.08)
                for s in g['segments']:
                    x=np.linspace(s['a'],s['b'],1201)
                    if 'expression' in s:
                        f=sp.lambdify(sp.Symbol('x'),sp.sympify(s['expression']),'numpy');y=np.asarray(f(x))*np.ones_like(x)
                    else:y=sum(float(sp.Rational(v))*x**j for j,v in enumerate(s['coefficients']))
                    px=ax.transData.transform(np.column_stack([x,y]))
                    assert not any(expanded.contains(*p) for p in px),'text/curve overlap'
                for coords in [np.column_stack([np.linspace(-4.65,4.65,501),np.zeros(501)]),np.column_stack([np.zeros(501),np.linspace(-4.65,4.65,501)])]:
                    assert not any(expanded.contains(*p) for p in ax.transData.transform(coords)),'text/axis overlap'
        side={'opaque':False,'python':sys.version.split()[0],'matplotlib':matplotlib.__version__,'text_boxes_pixels':boxes,'bounds':[-4.7,4.7,-4.7,4.7],'graphs':data['graphs'],'solution':data['solution'],'canvas':[1080,960],'axes_boxes':[list(ax.bbox.bounds) for ax in axs.flat], 'renderer_version':'1.3'}
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    fd,tmp=tempfile.mkstemp(suffix='.png',dir=path.parent);os.close(fd)
    fig.savefig(tmp,dpi=fig.dpi,facecolor='white');plt.close(fig)
    with Image.open(tmp) as im:im.load();side['png_size']=list(im.size)
    side['sha256']=hashlib.sha256(Path(tmp).read_bytes()).hexdigest()
    os.replace(tmp,path)
    fd,tmp=tempfile.mkstemp(suffix='.json',dir=path.parent);os.close(fd)
    Path(tmp).write_text(json.dumps(side,indent=2)+'\n');os.replace(tmp,path.with_suffix('.json'))
if __name__=='__main__':
    payload=json.loads(Path(sys.argv[1]).read_text());render(payload,sys.argv[2])
