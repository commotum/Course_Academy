"""Matplotlib region renderer; read-only cached Python dependencies."""
import json,os,re,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
os.environ['MPLCONFIGDIR']='/tmp/kp17592186133927-mpl'
provenance={}
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
p=json.loads(Path(sys.argv[1]).read_text());out=Path(sys.argv[2]);a=p['a'];name=p['name']
if name=='triangle':vertices=[(0,0),(a,0),(0,a)];label=f'$y={a}-x$';pos=(.98*a,.76*a);D=(.22*a,.27*a)
elif name=='xy_triangle':vertices=[(0,0),(a,0),(0,-a)];label=f'$y=x-{a}$';pos=(.98*a,-.82*a);D=(.23*a,-.28*a)
elif name=='cone_triangle':vertices=[(-a,0),(0,0),(0,a)];label=f'$y={a}+x$';pos=(-.85*a,.98*a);D=(-.22*a,.25*a)
elif name=='reciprocal':vertices=[(-a,-a),(a,-a),(a,a),(-a,a)];label=f'$x,y=\\pm {a}$';pos=(.6*a,1.28*a);D=(.4*a,.35*a)
else:vertices=[(0,0),(a,0),(a,a),(0,a)];label=f'$0\\leq x,y\\leq {a}$';pos=(.5*a,1.28*a);D=(.3*a,.35*a)
fig,ax=plt.subplots(figsize=(4.7,4.1),dpi=140); ax.set_aspect('equal');ax.add_patch(Polygon(vertices,facecolor='#cddfea',edgecolor='#2379ba',lw=1.6))
ax.axhline(0,color='black',lw=1);ax.axvline(0,color='black',lw=1)
lo=min(min(v) for v in vertices);hi=max(max(v) for v in vertices)
ax.set_xlim(lo-.38*a,hi+.48*a);ax.set_ylim(lo-.38*a,hi+.48*a)
# Label locations deliberately offset from all incident edges; measured below.
texts=[ax.text(*pos,label,ha='center',fontsize=12),ax.text(*D,'$D$',fontsize=14)]
ax.set_xticks(sorted(set(x for x,y in vertices)));ax.set_yticks(sorted(set(y for x,y in vertices)))
ax.tick_params(direction='out',pad=8);ax.set_xlabel('$x$',loc='right');ax.set_ylabel('$y$',loc='top',rotation=0)
for sp in ax.spines.values():sp.set_visible(False)
# The orange slice stays strictly inside the actual vertical integration bounds.
xx=(.65*a if name in ('triangle','xy_triangle','tilted_blank') else -.55*a)
if name=='triangle':lower,upper=0,a-xx
elif name=='xy_triangle':lower,upper=xx-a,0
elif name=='cone_triangle':lower,upper=0,a+xx
elif name=='reciprocal':lower,upper=-a,a
else:lower,upper=0,a
span=upper-lower;arrow_data=[(xx,lower+.08*span),(xx,upper-.08*span)]
ax.annotate('',xy=arrow_data[1],xytext=arrow_data[0],arrowprops={'arrowstyle':'->','color':'orange','lw':1.6})
fig.tight_layout();fig.canvas.draw();renderer=fig.canvas.get_renderer();bbs=[t.get_window_extent(renderer).expanded(1.03,1.03) for t in texts]
assert not bbs[0].overlaps(bbs[1]);box=fig.bbox
assert all(box.contains(b.x0,b.y0) and box.contains(b.x1,b.y1) for b in bbs)
# D's bbox clearance from polygon edges (pixel metric, segment distance).
import numpy as np
verts=ax.transData.transform(vertices);db=bbs[1];corners=np.array([[db.x0,db.y0],[db.x0,db.y1],[db.x1,db.y0],[db.x1,db.y1]])
def distance(pt,u,v):
 t=np.clip(np.dot(pt-u,v-u)/np.dot(v-u,v-u),0,1);return float(np.linalg.norm(pt-u-t*(v-u)))
clear=min(distance(c,verts[i],verts[(i+1)%len(verts)]) for c in corners for i in range(len(verts)))
assert clear>8,(name,a,clear)
# Check equation-label bbox against every actual boundary segment and arrow.
from matplotlib.path import Path as MPath
bb=bbs[0];eqcorners=np.array([[bb.x0,bb.y0],[bb.x0,bb.y1],[bb.x1,bb.y1],[bb.x1,bb.y0],[bb.x0,bb.y0]])
eqpath=MPath(eqcorners)
boundary=MPath(np.vstack([verts,verts[0]]))
assert not eqpath.intersects_path(boundary,filled=False)
equation_clearance=min(distance(c,verts[i],verts[(i+1)%len(verts)]) for c in eqcorners for i in range(len(verts)))
arrow=ax.transData.transform(arrow_data)
assert not eqpath.intersects_path(MPath(arrow),filled=False)
arrow_clearance=min(distance(c,*arrow) for c in eqcorners)
assert equation_clearance>8 and arrow_clearance>8,(name,equation_clearance,arrow_clearance)
axis_clearances=[]
axes_segments=[ax.transData.transform([(ax.get_xlim()[0],0),(ax.get_xlim()[1],0)]),ax.transData.transform([(0,ax.get_ylim()[0]),(0,ax.get_ylim()[1])])]
for bb in bbs:
 corners=np.array([[bb.x0,bb.y0],[bb.x0,bb.y1],[bb.x1,bb.y1],[bb.x1,bb.y0],[bb.x0,bb.y0]])
 for segment in axes_segments:
  assert not MPath(corners).intersects_path(MPath(segment),filled=False),(name,'label crosses an axis')
  axis_clearances.append(min(distance(c,*segment) for c in corners))
assert min(axis_clearances)>8,(name,'axis clearance',axis_clearances)
import tempfile
with tempfile.NamedTemporaryFile(dir=out.parent,suffix='.png',delete=False) as f:tmp=Path(f.name)
fig.savefig(tmp,dpi=140);tmp.replace(out);plt.close(fig)
import hashlib
side={'png_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'python':sys.version.split()[0],'matplotlib':matplotlib.__version__,'dependency_paths':provenance,'vertices':vertices,'label_clearance_px':clear,'equation_edge_clearance_px':equation_clearance,'equation_arrow_clearance_px':arrow_clearance,'renderer_version':4,'label_bboxes_px':[[b.x0,b.y0,b.x1,b.y1] for b in bbs],'orientation':'CCW supplied in prompt; orange arrow is Cartesian integration slice','parameters':p,'axes_bbox_pixels':list(ax.get_window_extent(renderer).bounds),'figure_pixels':list(fig.canvas.get_width_height()),'limits':[float(v) for v in (*ax.get_xlim(),*ax.get_ylim())],'arrow_data':arrow_data,'vertical_slice_bounds':[lower,upper],'background_masks':False,'minimum_text_axis_clearance_px':min(axis_clearances)}
with tempfile.NamedTemporaryFile(dir=out.parent,suffix='.json',mode='w',delete=False) as f:json.dump(side,f,indent=2);tmp=Path(f.name)
tmp.replace(out.with_suffix('.json'))
