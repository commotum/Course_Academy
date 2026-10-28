"""Matplotlib rendering from one immutable instance; unique inputs, atomic output."""
import json,os,sys,math
from pathlib import Path
os.environ.setdefault('MPLCONFIGDIR',str(Path(os.environ['COURSE_ACADEMY_GENERATOR_OUTPUT_DIR'])/'.mplconfig'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
def render(g,out):
    out=Path(out);A=g['A'];P=g.get('P');B=g['B'];h=g['grid_increment']
    for solution in (False,True):
        fig,ax=plt.subplots(figsize=(5,5));pts=[A,B]+([P] if P else []);xs=[p[0] for p in pts];ys=[p[1] for p in pts];lo=min(xs)-1.5;hi=max(xs)+1.5;bottom=min(ys)-1.5;top=max(ys)+1.7;size=max(hi-lo,top-bottom);hi=lo+size;top=bottom+size
        ax.set(xlim=(lo,hi),ylim=(bottom,top),aspect='equal');ax.xaxis.set_major_locator(MultipleLocator(h));ax.yaxis.set_major_locator(MultipleLocator(h));ax.grid(color='#cccccc',linewidth=.8);ax.tick_params(left=False,bottom=False,labelleft=False,labelbottom=False)
        for spine in ax.spines.values():spine.set_color('#cccccc')
        sx=lo+.5;sy=top-.5;ax.plot([sx,sx+1],[sy,sy],color='#2873b5',linewidth=2);ax.plot([sx,sx],[sy-.12,sy+.12],color='#2873b5');ax.plot([sx+1,sx+1],[sy-.12,sy+.12],color='#2873b5');ax.text(sx+.5,sy-.2,'1',color='#2873b5',ha='center',va='top')
        segments=[(A,B,g['names'][0])] if not P else [(A,P,g['names'][0]),(P,B,g['names'][1])]
        for tail,tip,name in segments:
            ax.annotate('',xy=tip,xytext=tail,arrowprops={'arrowstyle':'-|>','lw':2,'color':'black','shrinkA':0,'shrinkB':0});dx=tip[0]-tail[0];dy=tip[1]-tail[1];norm=(dx*dx+dy*dy)**.5;ax.text((tail[0]+tip[0])/2+.22*dy/norm,(tail[1]+tip[1])/2-.22*dx/norm,'$'+name+'$',fontsize=15,ha='center',va='center')
        if solution:
            H=[B[0],A[1]];ax.plot([A[0],H[0],B[0]],[A[1],H[1],B[1]],'r--',lw=1.2);ax.annotate('',xy=B,xytext=A,arrowprops={'arrowstyle':'-|>','lw':1.8,'color':'red','shrinkA':0,'shrinkB':0})
            if P:
                dx=B[0]-A[0];dy=B[1]-A[1];length=math.hypot(dx,dy);angle=math.degrees(math.atan2(dy,dx));angle=angle-180 if angle>90 else angle+180 if angle< -90 else angle
                def distance(point,start,end):
                    ux=end[0]-start[0];uy=end[1]-start[1];q=ux*ux+uy*uy
                    t=max(0,min(1,((point[0]-start[0])*ux+(point[1]-start[1])*uy)/q)) if q else 0
                    return math.hypot(point[0]-start[0]-t*ux,point[1]-start[1]-t*uy)
                obstacles=[(A,P),(P,B),(A,H),(H,B)]
                for tail,tip,label in segments:
                    vx=tip[0]-tail[0];vy=tip[1]-tail[1];vl=math.hypot(vx,vy);point=((tail[0]+tip[0])/2+.22*vy/vl,(tail[1]+tip[1])/2-.22*vx/vl);obstacles.append((point,point))
                candidates=[((A[0]+B[0])/2-z*dy/length,(A[1]+B[1])/2+z*dx/length) for z in (-.75,-.55,-.35,.35,.55,.75)]
                position=max(candidates,key=lambda point:min(distance(point,s,t) for s,t in obstacles))
                ax.text(*position,'$'+'+'.join(g['names'])+'$',color='red',fontsize=11,rotation=angle,ha='center',va='center')
            signx=1 if B[0]>A[0] else -1;signy=1 if B[1]>A[1] else -1
            for pt,label,off in [(A,'A',(-signx*.25,-signy*.3)),(B,'B',(signx*.17,signy*.2)),(H,'H',(signx*.2,-signy*.25))]:ax.text(pt[0]+off[0],pt[1]+off[1],'$'+label+'$',fontsize=14)
        elif P:
            ax.text(A[0]-.25,A[1]+.2,'$A$',fontsize=14);ax.text(B[0]-.25,B[1]+.2,'$B$',fontsize=14)
        fig.tight_layout(pad=.1);dest=out.with_name(out.stem+('-solution' if solution else '-prompt')+'.png');temp=dest.with_name(dest.stem+'.'+str(os.getpid())+'.tmp.png');fig.savefig(temp,dpi=120);plt.close(fig);os.replace(temp,dest)
    side=out.with_suffix('.json');temp=side.with_name(side.name+'.'+str(os.getpid())+'.tmp');temp.write_text(json.dumps({'geometry':g,'matplotlib':matplotlib.__version__,'python':sys.version,'renderer':'Matplotlib'},indent=2));os.replace(temp,side)
