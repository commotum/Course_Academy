"""Common-scale Matplotlib diagrams. Geometry is content-addressed; assets external."""
import hashlib,json,math,os
from pathlib import Path
os.environ.setdefault('MPLCONFIGDIR','/tmp/course-academy-vector-field-mpl')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

def render_bank(points,banks,output):
    output=output.resolve();output.mkdir(parents=True,exist_ok=True)
    points=[[float(z) for z in row] for row in points]
    banks=[[[float(z) for z in row] for row in bank] for bank in banks]
    coords=points+[[x+u,y+v] for bank in banks for (x,y),(u,v) in zip(points,bank)]
    lo=math.floor(min(-1,*[min(z) for z in coords]))-1
    hi=math.ceil(max(1,*[max(z) for z in coords]))+1
    bounds=[lo,hi];paths=[]
    for bank in banks:
        geom={'points':points,'vectors':bank,'bounds':bounds,'version':3}
        name=hashlib.sha256(json.dumps(geom,sort_keys=True).encode()).hexdigest()+'.png'
        path=output/name;paths.append(str(path))
        if path.exists():continue
        fig,ax=plt.subplots(figsize=(4,4),dpi=100)
        ax.set(xlim=bounds,ylim=bounds,aspect='equal')
        ax.set_xticks(range(lo+1,hi));ax.set_yticks(range(lo+1,hi))
        ax.grid(color='#d9dfe5',lw=.6);ax.set_axisbelow(True)
        for spine in ax.spines.values():spine.set_visible(False)
        ax.tick_params(length=0,labelsize=10,pad=3)
        ax.axhline(0,color='#394550',lw=1);ax.axvline(0,color='#394550',lw=1)
        ax.set_xlabel('$x$',fontsize=12);ax.set_ylabel('$y$',fontsize=12,rotation=0)
        for label,(x,y),(u,v) in zip('ABC',points,bank):
            if u or v:ax.add_patch(FancyArrowPatch((x,y),(x+u,y+v),arrowstyle='-|>',mutation_scale=14,lw=2,color='#246da4',shrinkA=0,shrinkB=0,zorder=3))
            else:ax.annotate('0',(x,y),xytext=(7,7),textcoords='offset points',color='#246da4',fontsize=10)
            ax.plot(x,y,'o',color='#e49a13',markersize=5,zorder=4)
            ax.annotate(label,(x,y),xytext=(-10,-13),textcoords='offset points',fontsize=13,weight='bold',zorder=5)
        fig.subplots_adjust(left=.10,right=.96,bottom=.10,top=.96)
        # Atomic write supports concurrent deterministic replay.
        tmp=path.with_name(path.stem+'-'+str(os.getpid())+'.png')
        fig.savefig(tmp,facecolor='white');plt.close(fig);os.replace(tmp,path)
        path.with_suffix('.json').write_text(json.dumps(geom,indent=2)+'\n')
    return paths,bounds
