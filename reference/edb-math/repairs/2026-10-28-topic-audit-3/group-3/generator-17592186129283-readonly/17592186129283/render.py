"""Matplotlib region renderer, exact question geometry input only, no sampling.
Cached dependency fallback; never installs packages or writes outside own evidence.
"""
import json,os,re,subprocess,sys,uuid
from pathlib import Path
HERE=Path(__file__).resolve().parent
os.environ['MPLCONFIGDIR']='/tmp/kp17592186129283-mpl'
provenance={}
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from fractions import Fraction
if sys.argv[1]=='--check':
    from PIL import Image
    checks=json.loads(Path(sys.argv[2]).read_text())
    for item in checks:
        im=Image.open(item['path']).convert('RGB')
        for point in item['points']:
            rgb=im.getpixel((round(point['x']),round(point['y'])))
            expected=point['shaded']
            shaded=rgb[2]>rgb[0]+8 and rgb[0]<235
            assert shaded==expected,(item['path'],point,rgb)
    print('Actual PNG pixel shading checks:',sum(len(i['points']) for i in checks))
    sys.exit(0)
for item in json.loads(Path(sys.argv[1]).read_text()):
    s=item['spec'];h,k,n,c,m=float(Fraction(str(s['h']))),float(Fraction(str(s['k']))),s['degree'],float(Fraction(s['coefficient'])),s['mode']
    # Bounds track translations and characteristic curve scale/intercepts.
    radius=max(3,2*abs(c)**(1/(abs(n)+1)))
    xlim=(min(0,h)-radius,max(0,h)+radius);ylim=(min(0,k)-radius,max(0,k)+radius)
    if 'bounds' in item:xlim=tuple(item['bounds'][:2]);ylim=tuple(item['bounds'][2:])
    xs=np.linspace(*xlim,601);ys=np.linspace(*ylim,601);X,Y=np.meshgrid(xs,ys);U=X-h;V=Y-k
    with np.errstate(divide='ignore',invalid='ignore'):
        F=c*U**n if n else np.zeros_like(U)
    if m=='product_gt':mask=U*V>c
    elif m=='product_lt':mask=U*V<c
    elif m=='above':mask=V>F
    elif m=='below':mask=V<F
    elif m=='right':mask=U>0
    elif m=='left':mask=U<0
    elif m=='top':mask=V>0
    elif m=='bottom':mask=V<0
    else:raise ValueError(m)
    fig,ax=plt.subplots(figsize=(4,3.5));ax.contourf(X,Y,mask.astype(int),levels=[.5,1.5],colors=['#d5e3ef'])
    if n==0:
        if m in ('top','bottom'):
            ax.axhline(k,color='#2c78bd',ls=(0,(3,3)),lw=1.5);label=f'v={k:g}'
        else:
            ax.axvline(h,color='#2c78bd',ls=(0,(3,3)),lw=1.5);label=f'u={h:g}'
    else:
        branches=[xs] if n!=-1 else [xs[xs<h-.01],xs[xs>h+.01]]
        for branch in branches:
            curve=k+c*(branch-h)**n;ax.plot(branch,curve,color='#2c78bd',ls=(0,(3,3)),lw=1.5)
        # Clear label in axes-relative position, avoiding shaded/curve obscuring.
        fraction=Fraction(s['coefficient']);coeff=str(fraction.numerator) if fraction.denominator==1 else r'\frac{'+str(fraction.numerator)+'}{'+str(fraction.denominator)+'}';Utex='u' if h==0 else '(u'+('+'+f'{-h:g}' if h<0 else '-'+f'{h:g}')+')'
        expr=Utex if n==1 else Utex+'^{'+str(n)+'}'
        if n==-1:expr=r'\frac{'+coeff+'}{'+Utex+'}'
        elif c==1:pass
        elif c==-1:expr='-'+expr
        else:expr=coeff+expr
        label=('v='+(''+f'{k:g}'+'+' if k else '')+expr).replace('+-','-')
    ax.text(.04,.94,'$'+label+'$',transform=ax.transAxes,va='top',fontsize=10,bbox={'facecolor':'white','edgecolor':'none','alpha':.85})
    ax.annotate('',xy=(xlim[1],0),xytext=(xlim[0],0),arrowprops={'arrowstyle':'->','color':'#333','lw':.8});ax.annotate('',xy=(0,ylim[1]),xytext=(0,ylim[0]),arrowprops={'arrowstyle':'->','color':'#333','lw':.8})
    ax.text(xlim[1],0,'$u$',ha='right',va='bottom');ax.text(0,ylim[1],'$v$',ha='left',va='top')
    ax.set(xlim=xlim,ylim=ylim);ax.set_aspect('equal');ax.axis('off');fig.canvas.draw()
    # Fixed uncropped canvas makes independent PNG probes reproducible.
    bbox=ax.get_window_extent();scale=110/fig.dpi
    token=uuid.uuid4().hex;sidecar=Path(item['path']+'.json');tmp_sidecar=Path(str(sidecar)+'.tmp-'+token)
    tmp_sidecar.write_text(json.dumps({'label':label,'xlim':xlim,'ylim':ylim,'bbox':[bbox.x0*scale,bbox.y0*scale,bbox.x1*scale,bbox.y1*scale],'height':3.5*110}));os.replace(tmp_sidecar,sidecar)
    tmp_image=item['path']+'.tmp-'+token+'.png';fig.savefig(tmp_image,dpi=110,facecolor='white');os.replace(tmp_image,item['path']);plt.close(fig)
provenance_root=Path(os.environ.get('COURSE_ACADEMY_GENERATOR_OUTPUT_DIR',str(Path(sys.argv[1]).resolve().parent)))
provenance_root.mkdir(parents=True,exist_ok=True)
tmp_provenance=provenance_root/('render-provenance.tmp-'+uuid.uuid4().hex+'.json')
tmp_provenance.write_text(json.dumps({'python':sys.version,'matplotlib':matplotlib.__version__,'dependency_paths':provenance,'renderer':'Matplotlib Agg','sampling':False},indent=2)+'\n')

os.replace(tmp_provenance,provenance_root/'render-provenance.json')
