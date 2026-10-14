#!/usr/bin/env python3
"""Factored polynomial -> qualitative graph choice only; basis 1356.

Seven observed complete banks; authored easy simplification to two simple roots.
No inverse recovery or coefficient-magnitude discrimination. Sources/recipes and
validation live in the adjacent private folder. CLI and generate APIs stop at
steps 3–7. A bank is chosen before sampling; all pairwise qualitative signatures
must differ or the entire instance is rejected. PNGs use the same exact factors.
"""
from pathlib import Path
import argparse,hashlib,itertools,json,os,random,re,tempfile,threading,uuid
# Inventory jobs invoke system Python; reuse the repository dependency environment.
try:
 import sympy as sp
except ImportError:
 import sys
 runtime=Path(__file__).resolve().parents[2]/'.venv/bin/python'
 os.execv(str(runtime),[str(runtime),__file__,*sys.argv[1:]])
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).with_suffix(''); VERSION='factored-to-graph-v3'
WRAPPER=json.loads((ROOT/'source.json').read_text()); RECORD=WRAPPER['record']
X=sp.Symbol('x',real=True); ROMANS=['I','II','III','IV']; LOCK=threading.Lock()
SOURCES={q[':question/math-academy-id']:q for q in RECORD[':knowledge-point/questions']}
# Each profile lists complete I–IV graph components. Tuple: sign multiplier,
# multiplicities at the ordered supplied roots. Exponents encode visible class,
# not recovered exact degree for unlabeled sketch distractors.
DATA={
 'q-38630':{'level':'moderate','roots':[-1,0,1],'m':[1,1,1],'a':1,'order':[1,0,2],'bank':[(1,[1,2,2]),(-1,[1,1,1]),(1,[1,1,2]),(1,[1,1,1])],'correct':'IV','groups':[('0,\\pm 1',[0,1,2])]},
 'q-38631':{'level':'moderate','roots':[-2,-1,1],'m':[1,2,1],'a':1,'order':[0,1,2],'bank':[(1,[1,2,1]),(1,[1,1,1]),(-1,[1,2,1]),(1,[2,2,2])],'correct':'I','groups':[('-2,1',[0,2]),('-1',[1])]},
 'q-38632':{'level':'moderate','roots':[0,1,2],'m':[2,2,1],'a':-5,'order':[0,1,2],'bank':[(-1,[2,2,1]),(-1,[2,1,1]),(1,[1,1,1]),(1,[2,2,1])],'correct':'IV','groups':[('2',[2]),('0,1',[0,1])]},
 'q-80353':{'level':'moderate','roots':[-1,0,2],'m':[1,2,2],'a':-1,'order':[1,0,2],'bank':[(1,[1,2,1]),(1,[1,2,2]),(1,[1,1,1]),(-1,[1,2,2])],'correct':'II','groups':[('-1',[0]),('0,2',[1,2])]},
 'q-80356':{'level':'moderate','roots':[-3,-1,1],'m':[1,2,1],'a':1,'order':[0,1,2],'bank':[(1,[1,2,1]),(1,[1,3,1]),(-1,[3,3,1]),(-1,[1,2,1])],'correct':'I','groups':[('-3,1',[0,2]),('-1',[1])]},
 'q-112599':{'level':'hard','roots':[-2,0,2],'m':[2,1,3],'a':-1,'order':[1,0,2],'bank':[(1,[2,1,3]),(1,[3,1,2]),(-1,[3,1,2]),(-1,[2,1,3])],'correct':'I','groups':[('-2',[0]),('0',[1]),('2',[2])]},
 'q-80361':{'level':'hard','roots':[-1,0,2],'m':[1,4,3],'a':-1,'order':[1,0,2],'bank':[(1,[1,4,1]),(-1,[1,4,1]),(1,[1,4,3]),(-1,[1,2,3])],'correct':'III','groups':[('0',[1]),('-1',[0]),('2',[2])]},
 'authored-easy':{'level':'easy','roots':[-1,1],'m':[1,1],'a':1,'order':[0,1],'bank':[(1,[1,1]),(-1,[1,1]),(1,[2,1]),(1,[2,2])],'correct':'I','groups':[]}}
# Source styles are parameterized complete factor components, never global prose substitutions.
STYLES={'q-38630':['x','(x+1)','(x-1)'],'q-38631':['(x+2)','(x+1)^{2}','(x-1)'],'q-38632':['{x}^{2}','(x-1{)}^{2}','(x-2)'],'q-80353':['{x}^{2}','(x+1)','(x-2{)}^{2}'],'q-80356':['(x+3)','(x+1{)}^{2}','(x-1)'],'q-112599':['x','(x+2)^{2}','(x-2)^{3}'],'q-80361':['{x}^{4}','(x+1)','(x-2{)}^{3}']}
def dump(v):return json.dumps(v,sort_keys=True,separators=(',',':'))
def fingerprint(v):return hashlib.sha256(dump(v).encode()).hexdigest()
def uid(v):return str(uuid.uuid5(uuid.NAMESPACE_URL,v))
def polynomial(p,m=None,a=None):return sp.Integer(p['a'] if a is None else a)*sp.prod((X-r)**k for r,k in zip(p['roots'],p['m'] if m is None else m))
def category(k):return 'simple' if k==1 else 'even' if k%2==0 else 'odd-multiple'
def signature(p,m=None,a=None):return (1 if (p['a'] if a is None else a)>0 else -1,tuple(zip(p['roots'],map(category,p['m'] if m is None else m))))
def validate_parameters(level,t,p):
 if set(p)!={'roots','m','a'}:raise ValueError('parameters require exactly roots,m,a')
 if any(type(v)!=int for v in p['roots']+p['m']+[p['a']]):raise ValueError('integer parameters required')
 d=DATA[t]
 if p['m']!=d['m'] or len(p['roots'])!=len(d['roots']):raise ValueError('fixed level workload/multiplicity roles')
 if p['roots']!=sorted(set(p['roots'])) or any(abs(r)>4 for r in p['roots']):raise ValueError('distinct ordered roots in -4..4')
 if not 1<=abs(p['a'])<=5:raise ValueError('nonzero signed coefficient with magnitude 1..5')
 if d['level']!=level:raise ValueError('profile level mismatch')
def factor_tex(r,k,style=None):
 base='x' if r==0 else '(x'+('+'+str(-r) if r<0 else '-'+str(r))+')'
 if style and '{x}' in style and r==0:base='{x}'
 if style and '{)}' in style and r!=0:base=base[:-1]+'{)}'
 return base+(('^{'+str(k)+'}') if k!=1 else '')
def equation_tex(t,p):
 d=DATA[t];styles=STYLES.get(t,[None]*len(p['m']))
 prefix='' if p['a']==1 else '-' if p['a']==-1 else str(p['a'])
 return prefix+''.join(factor_tex(p['roots'][i],p['m'][i],s) for i,s in zip(d['order'],styles))
def solution(t,p):
 d=DATA[t]
 if t in SOURCES:
  text=SOURCES[t][':question/worked-solution']
  # Protect complete root-component occurrences with independent placeholders.
  for n,(old,indices) in enumerate(d['groups']):text=text.replace('x='+old,'x=@@ROOT'+str(n)+'@@')
  for n,(old,indices) in enumerate(d['groups']):
   val=old if p['roots']==d['roots'] else ','.join(str(p['roots'][i]) for i in indices)
   text=text.replace('@@ROOT'+str(n)+'@@',val)
  if (p['a']>0)!=(d['a']>0):
   text=text.replace('coefficient is positive','coefficient is @@SIGN@@').replace('coefficient is negative','coefficient is @@SIGN@@').replace('@@SIGN@@','positive' if p['a']>0 else 'negative')
   # Sign flip of all candidate curves leaves the correct panel role unchanged.
   text=text.replace('$-\\infty .$', '$@@END@@ .$').replace('$\\infty .$','$@@END@@ .$')
   text=text.replace('$@@END@@ .$','$'+('\\infty' if p['a']>0 else '-\\infty')+' .$')
  return text
 roots=','.join(map(str,p['roots']))
 return ('Based on the factored equation, we can make the following conclusions about the graph:\n\n'
  f'- Since the multiplicity of the roots $x={roots}$ is $1,$ which is odd, the graph must cross the $x$-axis at these points. Moreover, because these are simple roots, the graph must *not* be tangent to the $x$-axis at these points.\n\n'
  'Only the graphs $\\text{I}$ and $\\text{II}$ satisfy these conditions.\n\n'
  'To choose between these two graphs, we need to consider the end behavior. Since the leading coefficient is '+('positive' if p['a']>0 else 'negative')+', as $x$ approaches $\\infty ,$ $y$ approaches $'+('\\infty' if p['a']>0 else '-\\infty')+' .$\n\nOnly graph $\\text{I}$ displays this end behavior. Therefore, the correct answer is $\\text{I}.$')
def graph_bank(t,p):
 d=DATA[t];banks=[{'label':r,'a':p['a']*s,'roots':p['roots'],'m':m} for r,(s,m) in zip(ROMANS,d['bank'])]
 ss=[signature(b) for b in banks]
 if len(set(ss))!=4 or ss.count(signature(p))!=1:raise ValueError('whole graph bank is qualitatively ambiguous')
 if banks[ROMANS.index(d['correct'])]['m']!=p['m'] or banks[ROMANS.index(d['correct'])]['a']!=p['a']:raise ValueError('recipe/key mismatch')
 return banks

def render_plots(t,p,output_dir=None):
 """Qualitative no-y-scale 2x2 graphs; extrema and exact roots control bounds."""
 out=Path(output_dir or ROOT/'plots');out.mkdir(parents=True,exist_ok=True)
 banks=graph_bank(t,p);key=fingerprint({'version':VERSION,'bank':banks})
 png=out/(key+'.png');side=out/(key+'.json')
 with LOCK:
  if png.exists() and side.exists():return {'prompt':str(png),'sidecar':str(side),'kind':'parameterized'}
  fig,axes=plt.subplots(2,2,figsize=(10,8),dpi=130)
  panels=[]
  for ax,b in zip(axes.flat,banks):
   f=polynomial(b);der=sp.Poly(sp.diff(f,X),X)
   extrema=[float((ab[0]+ab[1])/2) for ab,mul in sp.polys.polytools.intervals(der,eps=sp.Rational(1,10**8)) if min(p['roots'])<float((ab[0]+ab[1])/2)<max(p['roots'])]
   fn=sp.lambdify(X,f,'numpy');span=max(p['roots'])-min(p['roots']);lo=min(min(p['roots'])-.22*span,-.25);hi=max(max(p['roots'])+.22*span,.25)
   scale=max([abs(float(fn(z))) for z in extrema]+[1.0]);Ymax=scale*1.4
   grid=np.unique(np.r_[np.linspace(lo,hi,2200),p['roots'],extrema]);values=np.asarray(fn(grid),float)
   ax.plot(grid,values,color='red',lw=1.5);ax.set_xlim(lo,hi);ax.set_ylim(-Ymax,Ymax)
   for spine in ax.spines.values():spine.set_visible(False)
   ax.set_xticks([]);ax.set_yticks([])
   ax.annotate('',(hi,0),(lo,0),arrowprops={'arrowstyle':'->','color':'black','lw':1})
   ax.annotate('',(0,Ymax),(0,-Ymax),arrowprops={'arrowstyle':'->','color':'black','lw':1})
   for r in p['roots']:
    ax.plot([r,r],[0,-Ymax*.022],color='black',lw=.7)
    ax.annotate(str(r),(r,0),xytext=(0,-10),textcoords='offset points',ha='center',va='top',fontsize=10)
   ax.text(-.035,1.025,b['label'],transform=ax.transAxes,ha='left',va='bottom',fontsize=13)
   ax.text(.99,.51,'x',transform=ax.transAxes,fontsize=10);ax.text((0-lo)/(hi-lo)+.02,.96,'y',transform=ax.transAxes,fontsize=10)
   # Arrows where the curve exits top/bottom prove direction; source does not assess y scale.
   for left in [True,False]:
    inds=range(len(grid)) if left else range(len(grid)-1,-1,-1)
    visible=[i for i in inds if abs(values[i])<=Ymax*.9]
    if visible:
     i=visible[0];j=min(i+6,len(grid)-1) if left else max(i-6,0)
     arrow=ax.annotate('',(grid[i],values[i]),(grid[j],values[j]),arrowprops={'arrowstyle':'->','color':'red','lw':1.5})
     arrow.arrow_patch.set_clip_path(ax.patch)
   # Reserve a separate row of native polynomial root zooms. These use
   # actual f(x), true horizontal axes, and explicitly independent y scales.
   box=ax.get_position();ax.set_position([box.x0,box.y0+box.height*.30,box.width,box.height*.70])
   zooms=[]
   for n,r in enumerate(p['roots']):
    near=min(abs(r-z) for z in p['roots'] if z!=r);rad=near*.14
    gx=np.linspace(r-rad,r+rad,301);gy=np.asarray(fn(gx),float);yy=max(abs(gy))*1.12
    zx=fig.add_axes([box.x0+n*box.width/len(p['roots'])+.015,box.y0+.02,box.width/len(p['roots'])-.03,box.height*.21])
    zx.plot(gx,gy,color='red',lw=1.3);zx.axhline(0,color='black',lw=.6);zx.axvline(r,color='gray',lw=.5)
    zx.set_xlim(r-rad,r+rad);zx.set_ylim(-yy,yy);zx.set_xticks([]);zx.set_yticks([])
    zx.set_title('x='+str(r),fontsize=9,pad=2)
    for ss in zx.spines.values():ss.set_color('#bbbbbb');ss.set_linewidth(.5)
    zooms.append({'root':r,'x':gx.tolist(),'y':gy.tolist(),'ylim':[-yy,yy]})
   panels.append({'zooms':zooms,'label':b['label'],'factors':b,'expression':str(f),'xlim':[lo,hi],'ylim':[-Ymax,Ymax],'extrema':extrema,'sample_x':grid.tolist(),'sample_y':values.tolist()})
  fig.text(.5,.01,'Small boxes: local views at roots, with independent vertical scales.',ha='center',fontsize=10)
  fd,tmp=tempfile.mkstemp(prefix='render-',suffix='.png',dir=out);os.close(fd)
  try:fig.savefig(tmp,facecolor='white');os.replace(tmp,png)
  finally:plt.close(fig);Path(tmp).unlink(missing_ok=True)
  payload={'renderer':'Matplotlib','matplotlib':matplotlib.__version__,'sympy':sp.__version__,'instance':p,'bank':banks,'panels':panels,'pixel_size':[1300,1040]}
  fd,tmp=tempfile.mkstemp(prefix='side-',suffix='.json',dir=out);os.close(fd)
  try:Path(tmp).write_text(dump(payload));os.replace(tmp,side)
  finally:Path(tmp).unlink(missing_ok=True)
 return {'prompt':str(png),'sidecar':str(side),'kind':'parameterized'}

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ['easy','moderate','hard']:raise ValueError('difficulty')
 if field_type not in [None,'radio',':answer-field.type/radio']:raise ValueError('radio only')
 requested_profile=profile or template
 raw=bool(requested_profile and requested_profile.startswith('raw:'))
 t=requested_profile[4:] if raw else requested_profile
 if profile and template and t!=template:raise ValueError('template/profile mismatch')
 rng=random.Random(seed)
 if t is None:t=rng.choice([k for k,v in DATA.items() if v['level']==level])
 if t not in DATA or (raw and t not in SOURCES):raise ValueError('unknown complete profile')
 d=DATA[t]
 # Correct object is constructed first; the already-selected complete bank follows.
 p=parameters if parameters is not None else {'roots':sorted(rng.sample(range(-4,5),len(d['roots']))),'m':d['m'][:],'a':rng.choice([-1,1])}
 p=json.loads(dump(p));validate_parameters(level,t,p);correct=polynomial(p);banks=graph_bank(t,p)
 if raw and t in SOURCES and p=={k:d[k] for k in ['roots','m','a']}:
  rel=re.search(r'!\[\]\(([^)]+)\)',SOURCES[t][':question/problem'])[1]
  asset=ROOT/'originals'/Path(rel).name
  if not asset.exists():raise FileNotFoundError(asset)
  plot={'prompt':str(asset),'sidecar':None,'kind':'original-native','source_ref':rel}
 else:plot=render_plots(t,p)
 if t in SOURCES:
  old=SOURCES[t][':question/problem'];prompt=re.sub(r'!\[\]\([^)]+\)',lambda _: '![]('+plot['prompt']+')',old)
  prompt=re.sub(r'\$y=.*?\$',lambda match: '$y='+equation_tex(t,p)+('?' if match[0].endswith('?$') else '')+'$',prompt)
 else:prompt='![]('+plot['prompt']+')\n\nWhich of the above could be the graph of $y='+equation_tex(t,p)+'?$'
 sol=solution(t,p);values=[('\\text{'+r+'}',':answer.type/math') for r in ROMANS]+[('None of the given graphs are correct',':answer.type/text')]
 content=fingerprint({'version':VERSION,'prompt':prompt,'solution':sol,'bank':sorted(values),'difficulty':level});qid=uid(content);fid=uid(qid+'/selection')
 choices=[{':answer/id':uid(fid+'/'+v),':answer/type':typ,':answer/value':v} for v,typ in values];correct_id=next(a[':answer/id'] for a in choices if a[':answer/value']=='\\text{'+d['correct']+'}')
 rng.shuffle(choices)
 question={':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':sol,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',correct_id]}]}
 return {'knowledge_point':{'db_id':RECORD[':db/id'],'id':RECORD[':knowledge-point/id'],'title':RECORD[':knowledge-point/title']},'question':question,'generation':{'version':VERSION,'source':{k:WRAPPER[k] for k in ['database','basis','lineage']},'seed':seed,'template':t,'bank_profile':('raw:'+t if raw else t),'parameters':p,'correct_polynomial':str(correct),'graphs':banks,'plot':plot,'source_id':t if t in SOURCES else None,'content_fingerprint':content,'mathematical_fingerprint':fingerprint(signature(p)),'criterion':'root locations; simple/even/odd-multiple behavior; leading coefficient sign; no y-scale amplitude or exact exponent recovered','authored':t=='authored-easy','raw_evidence_profile':raw,'normal_eligible':not raw}}
def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)
def generate_hard(seed=0,**kw):return generate('hard',seed,**kw)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
 recs=[generate(l,args.seed+i,template=args.template,profile=args.profile) for l in (['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]) for i in range(args.count)]
 if args.format=='json':print(json.dumps(recs,indent=2))
 else:
  for r in recs:
   q=r['question'];print(q[':question/problem']+'\n\n'+q[':question/worked-solution']+'\n')
