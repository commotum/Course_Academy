import os
os.environ['MPLCONFIGDIR']='/tmp/ingest-six/mpl'
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path
R=Path('/home/jake/Developer/study/vault/F26/source/255')
# Source crops with no clipped surrounding prose.
from PIL import Image
Image.open('/tmp/ingest-six/doc1-5.png').crop((145,172,765,343)).save(R/'WHW-6/laplacian-surface-and-gradient.png')
Image.open('/tmp/ingest-six/doc1-4.png').crop((175,682,765,765)).save(R/'WHW-6/maxwell-separate-axes.png')
z=np.linspace(0,2*np.pi,25);zero=np.zeros_like(z);s=np.sin(z)
fig,axs=plt.subplots(1,2,figsize=(10,3.5),constrained_layout=True)
for ax,label,color in zip(axs,['Electric field: x component','Magnetic field: y component'],['#b43535','#285c9b']):
 ax.axhline(0,color='black',lw=.8);ax.quiver(z,zero,zero,s,angles='xy',scale_units='xy',scale=1,color=color,width=.004);ax.set(xlim=(-.2,2*np.pi+.2),ylim=(-1.3,1.3),xlabel='z',ylabel=label.split(':')[1].strip(),title=label);ax.set_xticks([0,np.pi/2,np.pi,3*np.pi/2,2*np.pi],['0','π/2','π','3π/2','2π']);ax.grid(alpha=.2)
fig.savefig(R/'WHW-6/authored-maxwell-separate.png',dpi=150);plt.close(fig)
fig=plt.figure(figsize=(7,5),constrained_layout=True);ax=fig.add_subplot(projection='3d');ax.plot(z,zero,zero,color='gray',lw=1);ax.quiver(z,zero,zero,zero,zero,s,color='#b43535',arrow_length_ratio=.15);ax.quiver(z,zero,zero,zero,s,zero,color='#285c9b',arrow_length_ratio=.15);ax.set(xlabel='z (propagation axis)',ylabel='y (B direction)',zlabel='x (E direction)',title='Authored reference: simultaneous E and B vectors at t = 0');ax.set_ylim(-1.25,1.25);ax.set_zlim(-1.25,1.25);ax.set_box_aspect((2.6,1,1));fig.savefig(R/'WHW-6/authored-maxwell-combined.png',dpi=150);plt.close(fig)
# Vector field within the ball; quiver endpoints use a uniform display scale.
g=np.linspace(-1.5,1.5,7);X,Y,Z=np.meshgrid(g,g,g);mask=(X*X+Y*Y+Z*Z<=4)&(X*X+Y*Y+Z*Z>0);X,Y,Z=X[mask],Y[mask],Z[mask];coef=2*np.exp(-(X*X+Y*Y+Z*Z));fig=plt.figure(figsize=(6,5),constrained_layout=True);ax=fig.add_subplot(projection='3d');ax.quiver(X,Y,Z,X*coef,Y*coef,Z*coef,length=.6,normalize=False,color='#285c9b',arrow_length_ratio=.25);ax.set(xlabel='x',ylabel='y',zlabel='z',title='Authored heat-flow reference: outward radial vectors',xlim=(-2,2),ylim=(-2,2),zlim=(-2,2));ax.set_box_aspect((1,1,1));fig.savefig(R/'R-6/authored-heat-flow-ball.png',dpi=150);plt.close(fig)
# Images of the oriented boundary of the unit square, parameterized CCW.
t=np.linspace(0,1,120)
sides=[(t,0*t),(1+0*t,t),(1-t,1+0*t),(0*t,1-t)]
transforms=[lambda u,v:(u+v,u-v),lambda u,v:(u-v,u+v),lambda u,v:(u*u-v*v,2*u*v),lambda u,v:(v*v-u*u,2*u*v)]
for index,T in enumerate(transforms):
 fig,ax=plt.subplots(figsize=(5,4),constrained_layout=True);allx=[];ally=[]
 for u,v in sides:
  a,b=T(u,v);allx.extend(a);ally.extend(b);ax.plot(a,b,color='#285c9b',lw=2);mid=60;ax.annotate('',xy=(a[mid+10],b[mid+10]),xytext=(a[mid],b[mid]),arrowprops={'arrowstyle':'->','color':'#b43535','lw':2})
 ax.fill(allx,ally,color='#285c9b',alpha=.08);ax.set(xlabel='x',ylabel='y',title='Authored reference: part ('+chr(97+index)+')');ax.set_aspect('equal');ax.axhline(0,color='gray',lw=.5);ax.axvline(0,color='gray',lw=.5);ax.grid(alpha=.2);fig.savefig(R/'WHW-7'/('authored-boundary-'+chr(97+index)+'.png'),dpi=150);plt.close(fig)
print('Saved seven authored mathematical reference figures.')
