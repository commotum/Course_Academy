#!/usr/bin/env python3
"""Known-solid divergence-theorem flux; frozen math basis1356, no database writes.
Raw profiles retain opaque historical banks as evidence. Defaults use whole
method-derived banks. Each family preserves its source theorem/divergence/volume
chain; no integration of a variable divergence occurs in this KP.
"""
import argparse, hashlib, json, random, re, sys, uuid
from pathlib import Path
import sympy as sp
import os
os.environ.setdefault('MPLCONFIGDIR','/tmp/kp17592186133930-mpl')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon
ROOT=Path(__file__).resolve().parent
HERE=ROOT/'17592186133930'
CAP=json.loads((HERE/'source.json').read_text())
KP=CAP['record']; VERSION='1.0.0'
x,y,z=sp.symbols('x y z'); XYZ=(x,y,z)
# Ordered source component objects, matched independently to captured TeX.
BASE=[(x,x*z,3*z),(z**2,2*y,x**2+y),(x-y,y+z,2*x-3*z),
 (3*x+y*sp.exp(z),x*y+2,1-x*z),(z,6*y,x+3*z),
 (y**2-x**2,4*y,2*x*z),(1-2*x,5*y-3*z**2,x**3-y**2),
 (3*x-y*z**2,y+sp.exp(z),2*y*sp.sin(x)),(y-z,y-2*x,x+4*z),
 (y*z-2*x,3*y,x+z)]
GEOM=[('sphere',5,(0,2,-1)),('cylinder',1,2,'z'),('cylinder',2,3,'x'),
 ('box',1,2,3),('sphere',2,(0,0,4)),('sphere',1,(-2,1,0)),
 ('cylinder',3,2,'y'),('box',1,2,1),('box',4,2,2),('sphere',3,(0,2,0))]
BANKS=[(sp.Rational(16,3)*sp.pi,sp.Rational(25,4)*sp.pi**2,sp.Rational(2000,3)*sp.pi,sp.Rational(400,3)*sp.pi,sp.Rational(800,3)*sp.pi),
 (sp.pi/2,2*sp.pi,6*sp.pi,4*sp.pi/3,4*sp.pi),
 (4*sp.pi,-12*sp.pi,-16*sp.pi,6*sp.pi,-8*sp.pi),
 (18,24,21,16,12),(64*sp.pi,128*sp.pi/3,256*sp.pi/3,96*sp.pi,78*sp.pi),
 (12*sp.pi,8*sp.pi/3,32*sp.pi/3,18*sp.pi,16*sp.pi/3),
 (32*sp.pi,54*sp.pi,64*sp.pi,27*sp.pi,48*sp.pi),(10,8,4,-2,-6),
 (50,42,80,64,96),(81*sp.pi,72*sp.pi,64*sp.pi,36*sp.pi,48*sp.pi)]
SPECS={}
for i,q in enumerate(KP[':knowledge-point/questions']):
 name=q[':question/math-academy-id']; blocks=re.findall(r'\$\$\n(.*?)\n\$\$',q[':question/worked-solution'],re.S)
 formal=blocks[1].split(r' \\')[0]
 comps=re.findall(r'\\frac{∂}{∂[xyz]}\((.*?)\)(?:\+|$)',formal)
 assert len(comps)==3,(name,comps)
 # Full components are masked before substitution; never replace short tokens.
 prompt=q[':question/problem']; field=re.search(r'\$F=(.*?)\$',prompt).group(1)
 skel=prompt.replace(field,'@@FIELD@@',1)
 if GEOM[i][0]=='sphere':
  geometry=re.search(r'given by \$(.*?)\$',prompt).group(1);skel=skel.replace(geometry,'@@GEOMETRY@@',1)
 else: geometry=None
 solution=q[':question/worked-solution'].replace(blocks[1],'@@DIV@@').replace(blocks[2],'@@FLUX@@')
 if GEOM[i][0]=='sphere': solution=solution.replace('$'+str(GEOM[i][1])+'$ enclosed','$@@R@@$ enclosed')
 SPECS[name]={'source':q,'i':i,'level':q[':question/difficulty'][':db/ident'].split('/')[-1],
 'components':comps,'field':field,'geometry':geometry,'prompt':skel,'solution':solution,'blocks':blocks}
TEMPLATES={n:s['level'] for n,s in SPECS.items()}|{'sphere_two_cancellations':'hard'}
def latex(e):return sp.latex(sp.sympify(e))
def signed(e):
 t=latex(e);return '('+t+')' if t.startswith('-') else t
def uid(v):return str(uuid.uuid5(uuid.NAMESPACE_URL,v))
def volume(g):
 if g[0]=='sphere':return sp.Rational(4,3)*sp.pi*g[1]**3
 if g[0]=='cylinder':return sp.pi*g[1]**2*g[2]
 return sp.prod(g[1:])
def geometry_tex(g):
 return '+'.join('{'+v+'}^{2}' if c==0 else '('+v+('-'+str(c) if c>0 else '+'+str(-c))+')^{2}' for v,c in zip('xyz',g[2]))+'='+str(g[1]**2)
def plot(g):
 """Projected closed solid; all rings/edges and labels derive from g."""
 key=hashlib.sha256(json.dumps({'geometry':g,'recipe':2}).encode()).hexdigest()[:20];folder=HERE/'plots';folder.mkdir(exist_ok=True)
 out=folder/(key+'.png');side=folder/(key+'.json')
 if out.exists() and side.exists():return str(out)
 vectors=np.array([[-.72,-.58],[1,-.10],[0,1.]])
 project=lambda a:np.asarray(a)@vectors
 fig,ax=plt.subplots(figsize=(5,4.5));ax.set_aspect('equal');ax.axis('off')
 if g[0]=='box':
  dims=g[1:];verts=np.array([[a,b,c] for a in (0,dims[0]) for b in (0,dims[1]) for c in (0,dims[2])]);p=project(verts)
  for ids in ([0,1,3,2],[2,3,7,6],[0,2,6,4],[0,1,5,4],[4,5,7,6],[1,3,7,5]):ax.add_patch(Polygon(p[ids],facecolor='#b5d2e8',edgecolor='#82afd0',alpha=.6,lw=.7))
  for j in range(3):
   a=np.zeros(3);a[j]=dims[j];ax.plot(*project(np.array([np.zeros(3),a])).T,color='#606060',ls='--',lw=.8)
 else:
  _,r,h,axis=g;ind='xyz'.index(axis);others=[j for j in range(3) if j!=ind];dims=[r,r,r];dims[ind]=h
  t=np.linspace(0,2*np.pi,161);ring=np.zeros((len(t),3));ring[:,others[0]]=r*np.cos(t);ring[:,others[1]]=r*np.sin(t)
  top=ring.copy();top[:,ind]=h;p=project(ring);q=project(top)
  # Side quads, closed circular caps, and hidden axial segment.
  for j in range(0,160,4):ax.add_patch(Polygon(np.vstack([p[j],p[j+4],q[j+4],q[j]]),facecolor='#c2dbea',edgecolor='none',alpha=.35))
  ax.fill(*p.T,color='#99bfdc',alpha=.45);ax.fill(*q.T,color='#bcd5e7',alpha=.5)
  ax.plot(*p.T,color='#81accb',lw=.7);ax.plot(*q.T,color='#81accb',lw=.7)
  a=np.zeros(3);a[ind]=h;ax.plot(*project(np.array([np.zeros(3),a])).T,'--',color='gray',lw=.8)
  verts=np.vstack([ring,top])
 for j in range(3):
  e=np.zeros(3);e[j]=dims[j]*1.4;end=project(e);a=np.zeros(3);a[j]=dims[j]
  ax.plot(*project(np.array([np.zeros(3),a])).T,color='#606060',ls='--',lw=.8)
  ax.annotate('',xy=end,xytext=project(a),arrowprops={'arrowstyle':'->','lw':1})
  ax.text(*(end+np.array([-.15,-.12] if j==0 else [.07,.08])),'$'+ 'xyz'[j]+'$',fontsize=12)
  a=np.zeros(3);a[j]=dims[j];loc=project(a);ax.plot(*loc,'k.',ms=3);offset=np.array([-.2,.08]) if j==2 else np.array([.03,-.23]);ax.text(*(loc+offset),str(dims[j]),fontsize=11)
 p=project(verts);ax.set_xlim(min(p[:,0].min(),-dims[0]*1.2)-.4,max(p[:,0].max(),dims[1]*1.5)+.5);ax.set_ylim(min(p[:,1].min(),-dims[0])-.4,max(p[:,1].max(),dims[2]*1.5)+.5)
 import tempfile,os
 fd,tmp=tempfile.mkstemp(suffix='.png',dir=folder);os.close(fd)
 fig.savefig(tmp,dpi=150,bbox_inches='tight',facecolor='white');plt.close(fig);os.replace(tmp,out)
 data={'geometry':g,'renderer':'Matplotlib','version':matplotlib.__version__,'axis_vectors':vectors.tolist(),'dimensions':dims,'closed_boundary':True,'cap_count':2 if g[0]=='cylinder' else 0,'face_count':6 if g[0]=='box' else 0,'bounds':[ax.get_xlim(),ax.get_ylim()]}
 fd,tmp=tempfile.mkstemp(suffix='.json',dir=folder);os.close(fd);Path(tmp).write_text(json.dumps(data));os.replace(tmp,side)
 return str(out)
def values_bank(d,g):
 v=volume(g);a=d*v
 if g[0]=='sphere':r=g[1];return [a,-a,v,d*sp.Rational(4,3)*sp.pi*r**2,d*4*sp.pi*r**3]
 if g[0]=='cylinder':r,h=g[1:3];return [a,-a,v,d*sp.pi*r*h,d*sp.pi*r*r]
 aa,b,c=g[1:];return [a,-a,v,d*aa*b,d*aa*c]
def domain_check(level,template,p,raw):
 if raw:
  if set(p)!={'k'} or type(p['k'])!=int or not 1<=p['k']<=3:raise ValueError('raw profile supports uniform field scale k=1..3 and fixed geometry')
 else:
  if level=='hard':
   if set(p)!={'a','b','c','geometry'} or any(type(p[t])!=int or not lo<=p[t]<=hi for t,lo,hi in [('a',1,3),('b',1,3),('c',2,6)]):raise ValueError('hard requires a,b=1..3,c=2..6,geometry')
  elif set(p)!={'k','geometry'} or type(p['k'])!=int or not 1<=p['k']<=3:raise ValueError('parameters must be k=1..3 and geometry')
  g=p['geometry'];base=GEOM[SPECS[template]['i']] if template in SPECS else ('sphere',2,(-2,1,0))
  if g[0]!=base[0]:raise ValueError('solid family cannot change')
  if g[0]=='sphere':
   if len(g)!=3 or type(g[1])!=int or not 2<=g[1]<=5 or len(g[2])!=3 or any(type(c)!=int or abs(c)>4 for c in g[2]) or not any(g[2]):raise ValueError('sphere: radius2..5, shifted integer center magnitude<=4')
   if any(bool(c)!=bool(d) for c,d in zip(g[2],base[2])):raise ValueError('preserve source translation support')
  elif g[0]=='cylinder':
   if len(g)!=4 or g[3]!=base[3] or any(type(v)!=int or not 2<=v<=4 for v in g[1:3]):raise ValueError('cylinder: radius/height2..4, fixed source axis')
  elif len(g)!=4 or any(type(v)!=int or not 1<=v<=4 for v in g[1:]):raise ValueError('box dimensions1..4')
def build(spec,k,g,raw):
 comps=[k*v for v in spec.get('expressions',BASE[spec['i']])]
 ctxt=[t if k==1 else str(k)+r'\left('+t+r'\right)' for t in spec['components']]
 deriv=[sp.diff(v,c) for v,c in zip(comps,XYZ)];d=sp.simplify(sum(deriv));a=sp.simplify(d*volume(g))
 # Exact source slot spellings at source values; all changed slots computed.
 original=GEOM[spec['i']];anchor=k==1 and tuple(g)==original
 formal=r'\text{div}\,F & ='+ '+'.join(r'\frac{∂}{∂'+c+'}('+t+')' for c,t in zip('xyz',ctxt))
 div=formal+r' \\  & ='+ '+'.join(signed(v) for v in deriv)+r' \\  & ='+latex(d)+r'.\end{aligned}'
 div=r'\begin{aligned}'+div
 if k==1:
  # Preserve individual evaluated component spellings, rather than replaying
  # a whole source solution block. Hard's grouped row is authored dynamically.
  substitution=spec['blocks'][1].split(r' \\  & =')[1]
  div=r'\begin{aligned}'+formal+r' \\  & ='+substitution+r' \\  & ='+latex(d)+r'.\end{aligned}'
 # Source field separators/parentheses retained by complete-component masks.
 field=spec['field']
 # Build from full component slots: source formal inputs can be substrings of fields.
 if spec['level']=='easy':field='⟨'+r',\,'.join(ctxt)+'⟩'
 else:
  field='+'.join(('('+t+')' if '+' in t or '-' in t else t)+r'\,'+c for t,c in zip(ctxt,'ijk'))
 if k==1:field=spec['field']
 if d==-1:factor='-';vrow=r'-\text{Volume}(R)';formula='-'
 else:factor=latex(d);vrow=factor+r'\cdot \text{Volume}(R)';formula=factor+r'\cdot '
 if g[0]=='sphere':formula+=r'\frac{4}{3}\pi \cdot {'+str(g[1])+r'}^{3}'
 elif g[0]=='cylinder':formula+=r'\pi \cdot {'+str(g[1])+r'}^{2}\cdot '+str(g[2])
 else:formula+=r'\cdot '.join(map(str,g[1:]))
 flux=r'\begin{aligned}{∬}_{S}F\cdot dS & ={∭}_{R}'+latex(d)+r'\,\text{d}V \\  & ='+factor+r'{∭}_{R}\,\text{d}V \\  & ='+vrow+r' \\  & ='+formula+r' \\  & ='+latex(a)+r'.\end{aligned}'
 if anchor:
  # Only the final scalar's original spelling is a notation slot; all five
  # mathematical rows are constructed from the displayed field and geometry.
  atom=spec['blocks'][2].split(r' \\  & =')[-1].split(r'.\end{aligned}')[0]
  flux=flux.replace(latex(a)+r'.\end{aligned}',atom+r'.\end{aligned}')
 prompt=spec['prompt'].replace('@@FIELD@@',field)
 if g[0]=='sphere':prompt=prompt.replace('@@GEOMETRY@@',spec['geometry'] if anchor else geometry_tex(g))
 elif not raw:
  prompt=re.sub(r'!\[\]\(.*?\)',lambda _: '![]('+plot(g)+')',prompt)
  if g[0]=='cylinder':
   prompt=re.sub(r'height \$\d+\$',lambda _: 'height $'+str(g[2])+'$',prompt)
   prompt=re.sub(r'radius \$\d+\$',lambda _: 'radius $'+str(g[1])+'$',prompt)
 solution=spec['solution'].replace('@@DIV@@',div).replace('@@FLUX@@',flux).replace('@@R@@',str(g[1]))
 return prompt,solution,a,d,comps,deriv
# EASY: six observed field masks, cylinders/boxes, held-coordinate derivatives.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE: four shifted-sphere masks, including one cancellation pair.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# HARD (authored): same sphere-volume reduction, two cancellation pairs.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)
def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard') or field_type not in (None,'radio'):raise ValueError('unsupported level/field type')
 rng=random.Random(seed);raw=bool(profile and profile.startswith('raw-'))
 if raw:
  n=profile[4:]
  if template and template!=n:raise ValueError('profile/template mismatch')
  template=n
 elif profile not in (None,'method'):raise ValueError('unknown profile')
 template=template or rng.choice([n for n,l in TEMPLATES.items() if l==level])
 if TEMPLATES.get(template)!=level:raise ValueError('template/level mismatch')
 if template in SPECS:spec=SPECS[template];i=spec['i']
 else:
  # Authored structural change of the cancellation-sphere mask.
  spec=dict(SPECS['q-162580']);spec['components']=[r'{y}^{2}-{x}^{2}+2xy',r'4y-{y}^{2}',r'2xz'];spec['field']=r'({y}^{2}-{x}^{2}+2xy)\,i+(4y-{y}^{2})\,j+2xz\,k.'
  spec['expressions']=[y*y-x*x+2*x*y,4*y-y*y,2*x*z];spec['blocks']=list(spec['blocks']);spec['blocks'][1]=r'\begin{aligned}\text{div}\,F & =\frac{∂}{∂x}({y}^{2}-{x}^{2}+2xy)+\frac{∂}{∂y}(4y-{y}^{2})+\frac{∂}{∂z}(2xz) \\  & =-2x+2y+(4-2y)+2x \\  & =4.\end{aligned}'
  i=5
 if raw and template not in SPECS:raise ValueError('hard has no raw source')
 for attempt in range(300):
  p=parameters
  if p is None:
   if raw:p={'k':1}
   else:
    base=GEOM[i]
    if base[0]=='sphere':g=('sphere',rng.randint(2,5),tuple(rng.choice([-4,-3,-2,-1,1,2,3,4]) if c else 0 for c in base[2]))
    elif base[0]=='cylinder':g=('cylinder',rng.randint(2,4),rng.randint(2,4),base[3])
    else:g=('box',rng.randint(1,4),rng.randint(1,4),rng.randint(1,4))
    p={'a':rng.randint(1,3),'b':rng.randint(1,3),'c':rng.randint(2,6),'geometry':g} if level=='hard' else {'k':rng.randint(1,3),'geometry':g}
  domain_check(level,template,p,raw);k=p.get('k',1);g=GEOM[i] if raw else tuple(p['geometry'])
  if template=='sphere_two_cancellations':
   aa,bb,cc=p['a'],p['b'],p['c']
   term=lambda n,v:('' if n==1 else str(n))+v
   spec['expressions']=[y*y-aa*x*x+2*bb*x*y,cc*y-bb*y*y,2*aa*x*z]
   spec['components']=[r'{y}^{2}-'+term(aa,r'{x}^{2}')+'+'+term(2*bb,'xy'),term(cc,'y')+'-'+term(bb,r'{y}^{2}'),term(2*aa,'xz')]
   spec['field']='('+spec['components'][0]+r')\,i+('+spec['components'][1]+r')\,j+'+spec['components'][2]+r'\,k.'
   spec['blocks'][1]=r'\begin{aligned}\text{div}\,F & ='+ '+'.join(r'\frac{∂}{∂'+v+'}('+t+')' for v,t in zip('xyz',spec['components']))+r' \\  & =-'+term(2*aa,'x')+'+'+term(2*bb,'y')+'+('+str(cc)+'-'+term(2*bb,'y')+')+'+term(2*aa,'x')+r' \\  & ='+str(cc)+r'.\end{aligned}'
  prompt,solution,a,d,comps,deriv=build(spec,k,g,raw)
  vals=[sp.sympify(v)*k for v in BANKS[i]] if raw else values_bank(d,g)
  if len(set(map(sp.simplify,vals)))==5 and (raw or d not in (0,1)) :break
  if parameters is not None:raise ValueError('whole method bank collision/degeneracy')
 else:raise ValueError('unable to sample eligible whole bank')
 source=spec['source'];fields=[]
 rawfields=source[':question/answer-fields'] if raw else [source[':question/answer-fields'][-1]]
 fielddata=[]
 for j,f in enumerate(rawfields):
  if raw:
   # Homogeneous evidence extension only; interpretation remains unresolved.
   choices=[{'value':a0[':answer/value'] if k==1 else latex(sp.sympify(BANKS[i][next(n for n,v in enumerate(BANKS[i]) if sp.simplify(v-sp.sympify(parse_scalar(a0[':answer/value'])))==0)])*k),'correct':':answer-field/correct' in f and a0[':answer/id']==f[':answer-field/correct'][':answer/id']} for a0 in f[':answer-field/choices']]
  else:choices=[{'value':latex(v),'correct':n==0} for n,v in enumerate(vals)]
  fielddata.append(choices)
 canonical={'version':VERSION,'level':level,'prompt':prompt,'solution':solution,'fields':fielddata}
 identity=hashlib.sha256(json.dumps(canonical,sort_keys=True).encode()).hexdigest();qid=uid(identity)
 for j,(f,data) in enumerate(zip(rawfields,fielddata)):
  fid=uid(qid+':field:'+str(j));choices=[{':answer/id':uid(fid+':'+c['value']),':answer/type':':answer.type/math',':answer/value':c['value']} for c in data]
  out={':answer-field/id':fid,':answer-field/key':f[':answer-field/key'],':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices}
  cs=[v for v,c in zip(choices,data) if c['correct']]
  if raw:
   out[':db/id']=f[':db/id']
   for ca in choices:
    aa=next(aa for aa in f[':answer-field/choices'] if (aa[':answer/value'] if k==1 else latex(parse_scalar(aa[':answer/value'])*k))==ca[':answer/value']);ca[':db/id']=aa[':db/id']
  if cs:out[':answer-field/correct']=[':answer/id',cs[0][':answer/id']]
  rng.shuffle(choices);fields.append(out)
 q={':question/id':qid,':question/problem':prompt,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+level,':question/answer-fields':fields}
 if raw:q[':db/id']=source[':db/id'];q[':question/math-academy-id']=source[':question/math-academy-id']
 fingerprint=hashlib.sha256(json.dumps({'field':[sp.srepr(v) for v in comps],'solid':(g[:2] if g[0]=='sphere' else g)},sort_keys=True).encode()).hexdigest()
 return {'knowledge_point':{'db_id':KP[':db/id'],'id':KP[':knowledge-point/id'],'title':KP[':knowledge-point/title']},'question':q,'generation':{'version':VERSION,'template':template,'profile':profile or 'method','seed':seed,'parameters':p,'geometry':g,'source_id':source[':db/id'] if template in SPECS else None,'basis':CAP['basis'],'lineage':CAP['lineage'],'evidence_only':raw,'eligible_for_learning':not raw,'mathematical_fingerprint':fingerprint,'content_identity':identity,'exact_flux':str(a),'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__,'matplotlib':matplotlib.__version__}}}
def parse_scalar(t):
 t=t.replace(r'\,','').replace(' ','').replace('π',r'\pi')
 m=re.fullmatch(r'\\frac\{(.*?)\}\{(\d+)\}',t)
 if m:return parse_scalar(m[1])/int(m[2])
 t=re.sub(r'\{(\d+)\}',r'\1',t)
 t=t.replace(r'\pi','*pi').replace('^','**').replace('{','').replace('}','')
 if t.startswith('*'):t=t[1:]
 return sp.sympify(t)
def markdown(r):
 q=r['question'];s=q[':question/problem']+'\n\n'
 for f in q[':question/answer-fields']:
  for a in f[':answer-field/choices']:s+='- $'+a[':answer/value']+'$'+(' (correct)' if f.get(':answer-field/correct',[None,None])[1]==a[':answer/id'] else '')+'\n'
 return s+'\n'+q[':question/worked-solution']
def main():
 p=argparse.ArgumentParser();p.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');p.add_argument('--seed',type=int,default=0);p.add_argument('--count',type=int,default=1);p.add_argument('--template');p.add_argument('--profile');p.add_argument('--format',choices=['json','markdown'],default='markdown');a=p.parse_args()
 levels=['easy','moderate','hard'] if a.difficulty=='all' else [a.difficulty]
 if a.count<1:p.error('count must be positive')
 records=[generate(l,a.seed+i,a.template,profile=a.profile) for l in levels for i in range(a.count)]
 print(json.dumps(records,indent=2,ensure_ascii=False) if a.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
if __name__=='__main__':main()
