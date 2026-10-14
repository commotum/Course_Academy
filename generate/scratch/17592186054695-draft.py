#!/usr/bin/env python3
"""Local, unregistered three-level two-point graph draft; steps 3–7 only.

Easy: signed integer/unit rational coefficient, integer point coordinates.
Moderate (authored): nonunit reduced rational coefficient, integer shift/points.
Hard (authored): same arithmetic chain with halfinteger shift/point readings.
Historical complete profiles are public evidence replay, with exact omission parity.
"""
import argparse, hashlib, json, math, os, random, re, sys, tempfile, threading, uuid
from pathlib import Path
import sympy as sp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
KP_ID=17592186054695
KP_UUID='ebeb4e5a-adbe-5a94-b05d-61933a687892'
TITLE='Sketching a Line Using Two Points'
VERSION='two-point-lines-draft-v2'
PACKAGE=Path(__file__).with_suffix('')
SOURCE=json.loads((PACKAGE/'source.json').read_text())
CONTRACT=json.loads((PACKAGE/'contract.json').read_text())
PROFILES=CONTRACT['profiles']
LOCK=threading.RLock()
def digest(v): return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def ident(v): return str(uuid.uuid5(uuid.UUID(KP_UUID),digest(v)))
def rat(z): return sp.Rational(str(z))
def tex(z): return sp.latex(rat(z))
def values(p):
 if isinstance(p,dict): return rat(p['m']),rat(p.get('b',0)),rat(p.get('x2',sp.denom(rat(p['m'])))),p.get('layout','coefficient-first')
 if len(p)==2:return rat(p[0]),rat(p[1]),sp.denom(rat(p[0])),'coefficient-first'
 return rat(p[0]),rat(p[1]),rat(p[2]),p[3] if len(p)>3 else 'coefficient-first'
def normal_domain(level,m,b,x2):
 d=sp.denom(m);n=abs(sp.numer(m))
 if m==0 or x2==0 or x2 not in [-2*d,-d,d,2*d] or abs(b)>4 or abs(m*x2+b)>14: return False
 if level=='easy':return (d==1 and n<=4 or n==1 and d in [2,3,4]) and sp.denom(b)==1
 if level=='moderate':return d in [2,3,4] and 2<=n<=5 and b!=0 and sp.denom(b)==1
 if level=='hard':return d in [2,3,4] and 2<=n<=5 and sp.denom(b)==2
 return False
def expr(m,b,layout='coefficient-first',x='x'):
 c=(tex(m)+x) if m not in [1,-1] else (x if m==1 else '-'+x)
 if layout=='constant-first' and b!=0:return tex(b)+('+' if m>0 else '-')+((tex(abs(m))+x) if abs(m)!=1 else x)
 return c+('+'+tex(b) if b>0 else tex(b) if b<0 else '')
def source_bank(profile,m,b):
 if profile=='q-54286':return [(m,b),(-m,-b),(m,-b),(m/4,b/2),(-m/4,-b/2)]
 if profile=='q-59678':return [(-m,-2*b),(m,b),(-2*m,-b),(2*m,0),(4*m,2*b)]
 if profile=='q-102054':return [(-m,m),(m,-m),(m/2,0),(m,0),(-m,0)]
 if profile=='q-109055':return [(-m,-b),(m,2*b),(m,b),(-m,0),(m,0)]
 raise ValueError('Unknown historical bank')
def normal_bank(profile,m,b):
 if profile=='method-shift':return [(m,b),(-m,b),(m,-b),(-m,-b),(m+b,b)]
 if profile=='method-origin':return [(m,0),(-m,0),(m/2,0),(2*m,0),(1/m,0)]
 if profile=='method-unit-origin':return [(m,0),(-m,0),(m/2,0),(2*m,0),(0,0)]
 raise ValueError('Unknown complete bank')
def valid_bank(bank):return len(bank)==5 and len(set(bank))==5

def render_plot(m,b,points=(),reading=1,bounds=None):
 """Fresh Matplotlib render with atomic PNG+sidecar; synchronized threads, unique inputs."""
 pts=[[str(x),str(y)] for x,y in points]
 if bounds is None:
  xx=[0,1]+[float(x) for x,y in points]; yy=[0,float(b),float(m+b)]+[float(y) for x,y in points]
  xmax=max(4,math.ceil(max(xx)+2));xmin=min(-4,math.floor(min(xx)-2));ymax=max(4,math.ceil(max(yy)+2));ymin=min(-4,math.floor(min(yy)-2))
  bounds=[xmin,xmax,ymin,ymax]
 xmin,xmax,ymin,ymax=bounds
 if max(xmax-xmin,ymax-ymin)>34:raise ValueError('Illegible bounded figure')
 spec={'line':[str(m),str(b)],'points':pts,'reading_grid':str(reading),'bounds':bounds,'line_color':'red','marker_color':'blue','renderer':'Matplotlib','version':VERSION}
 key=digest(spec);folder=PACKAGE/'assets';folder.mkdir(exist_ok=True);out=folder/(key+'.png');side=folder/(key+'.json')
 with LOCK:
  if not out.exists() or not side.exists():
   with tempfile.TemporaryDirectory(prefix='render-',dir=folder) as td:
    td=Path(td);(td/'input.json').write_text(json.dumps(spec));fig,ax=plt.subplots(figsize=(5.8,5.8),dpi=110)
    ax.set(xlim=(xmin,xmax),ylim=(ymin,ymax));ax.set_aspect('equal',adjustable='box');ax.set_position([.13,.12,.76,.76])
    # Every halfunit tick is labelled on H; integer grid elsewhere. Actual axes carry real zero.
    tick=sp.Rational(str(reading));major=1 if tick==1 else 1
    ax.set_xticks(range(xmin,xmax+1));ax.set_yticks(range(ymin,ymax+1))
    if tick==sp.Rational(1,2):
     import numpy as np
     ax.set_xticks(np.arange(xmin,xmax+.25,.5),minor=True);ax.set_yticks(np.arange(ymin,ymax+.25,.5),minor=True)
    ax.grid(which='major',color='#c7c7c7',linewidth=.8);ax.grid(which='minor',color='#e1e1e1',linewidth=.6);ax.set_axisbelow(True)
    ax.spines[['right','top']].set_visible(False);ax.spines[['left','bottom']].set_position('zero');ax.spines[['left','bottom']].set_linewidth(1.4)
    ax.tick_params(which='both',length=0,labelsize=8,pad=5)
    ax.set_xticklabels(['' if i==0 else str(i) for i in range(xmin,xmax+1)]);ax.set_yticklabels(['' if i==0 else str(i) for i in range(ymin,ymax+1)])
    ax.text(-.14,-.18,'0',ha='right',va='top',fontsize=9,bbox={'facecolor':'white','edgecolor':'none','pad':.3})
    ax.plot([xmin,xmax],[float(m*xmin+b),float(m*xmax+b)],color='red',linewidth=1.8)
    if points:
     ax.scatter([float(x) for x,y in points],[float(y) for x,y in points],s=28,c='blue',zorder=5)
     for x,y in points:
      # Label away from rising/falling segment; opaque white under text keeps the ordered point role legible.
      ax.annotate('$('+tex(x)+','+tex(y)+')$',(float(x),float(y)),xytext=(9,10 if m<0 else -20),textcoords='offset points',fontsize=10,color='blue',bbox={'facecolor':'white','edgecolor':'none','pad':1})
    ax.plot(xmax,0,'>k',clip_on=False,markersize=5);ax.plot(0,ymax,'^k',clip_on=False,markersize=5);ax.annotate('$x$',(xmax,0),xytext=(10,-4),textcoords='offset points',fontsize=13);ax.annotate('$y$',(0,ymax),xytext=(-3,12),textcoords='offset points',fontsize=13)
    fig.savefig(td/'plot.png',metadata={'Software':VERSION});plt.close(fig);os.replace(td/'plot.png',out)
    metadata={**spec,'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'local':str(out),'python':sys.version.split()[0],'sympy':sp.__version__,'matplotlib':matplotlib.__version__}
    (td/'side.json').write_text(json.dumps(metadata,indent=2)+'\n');os.replace(td/'side.json',side)
 metadata=json.loads(side.read_text());sha=metadata['sha256'];metadata['path']=f'images/{sha[:2]}/{sha}.png';return metadata['path'],metadata

def solution(m,b,x2,layout,asset,short=False):
 e=expr(m,b,layout)
 def rows(x):
  subst=expr(m,b,layout,'('+tex(x)+')'); product=m*x; value=product+b
  if b==0:return [e,subst,tex(value)+'.']
  reduced=tex(b)+('+' if product>0 or product==0 and m>0 else '-')+tex(abs(product)) if layout=='constant-first' else tex(product)+('+'+tex(b) if b>0 else tex(b))
  return [e,subst,reduced,tex(value)+'.']
 result='We need to find two distinct points that lie on our line. Any two points will do!\n\n'
 for i,x in enumerate([sp.Integer(0),x2]):
  word=['first','second'][i];result+=f'- For the {word} point, we will let the $x$-coordinate be $x={tex(x)}.$ Then the $y$-coordinate is'+(' \n\n' if short and i==0 else '\n\n')
  rs=rows(x);result+='$$\n'+r'\begin{aligned}y & ='+r' \\  & ='.join(rs)+r'\end{aligned}'+'\n$$\n\n'+f'So, the {word} point is $({tex(x)},{tex(m*x+b)}).$\n\n'
 result+=f'Finally, we plot those two points on the $xy$-plane and draw a line through them. This is the graph of $y={e}.$'+(' \n\n' if short else '\n\n')+f'![]({asset})'
 return result

# EASY: recovered two-point method; each historical bank remains distinct.
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
# MODERATE: authored nonunit numerator multiply then integer shift, integer plotted points.
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
# HARD: authored halfinteger shift and halfunit coordinate readings, same ordered stages.
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)
def parameter_domain(level,template):
 ms=[sp.Rational(n,d) for d in [1,2,3,4] for n in range(-5,6) if n and sp.gcd(n,d)==1]
 bs=[sp.Rational(n,2) for n in range(-8,9)]
 out=[]
 for m in ms:
  for b in bs:
   if template=='homogeneous' and b!=0 or template!='homogeneous' and b==0:continue
   for x2 in [-2*sp.denom(m),-sp.denom(m),sp.denom(m),2*sp.denom(m)]:
    if not normal_domain(level,m,b,x2):continue
    profile='method-unit-origin' if b==0 and abs(m)==1 else 'method-origin' if b==0 else 'method-shift'
    if valid_bank(normal_bank(profile,m,b)):out.append({'m':str(m),'b':str(b),'x2':str(x2),'layout':'constant-first' if template=='constant-first' else 'coefficient-first'})
 return out

def generate(level='easy',seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ['easy','moderate','hard']:raise ValueError('Unknown difficulty')
 if field_type not in [None,'radio',':answer-field.type/radio']:raise ValueError('Only radio is supported')
 rng=random.Random(seed);raw=profile in PROFILES or template in PROFILES
 if raw:
  if level!='easy':raise ValueError('Original replay band is easy; source omissions retained')
  sid=profile if profile in PROFILES else template;t=PROFILES[sid];m,b,x2,layout=values(parameters or t['parameters']);template=t['template'];profile=sid
  if (b==0 and sid!='q-102054') or (b!=0 and sid=='q-102054') or m==0 or x2==0:raise ValueError('Historical profile domain')
  bank=source_bank(sid,m,b)
  if not valid_bank(bank):raise ValueError('Complete historical bank collision')
  anchor=(m,b,x2,layout)==values(t['parameters'])
 else:
  template=template or rng.choice(['homogeneous','coefficient-first','constant-first'] if level=='easy' else ['coefficient-first','constant-first'])
  if template not in ['homogeneous','coefficient-first','constant-first']:raise ValueError('Unknown template')
  if parameters is None:
   eligible=['method-unit-origin','method-origin'] if template=='homogeneous' else ['method-shift']
   profile=profile or rng.choice(eligible)
   if profile not in eligible:raise ValueError('Profile ineligible for family')
   domain=[p for p in parameter_domain(level,template) if ('method-unit-origin' if rat(p['b'])==0 and abs(rat(p['m']))==1 else 'method-origin' if rat(p['b'])==0 else 'method-shift')==profile]
   if not domain:raise ValueError('No valid same-method domain')
   parameters=rng.choice(domain)
  m,b,x2,layout=values(parameters);layout='constant-first' if template=='constant-first' else 'coefficient-first'
  if not normal_domain(level,m,b,x2) or (template=='homogeneous')!=(b==0):raise ValueError('Outside declared workload domain')
  expected='method-unit-origin' if b==0 and abs(m)==1 else 'method-origin' if b==0 else 'method-shift'
  profile=profile or expected
  if profile!=expected:raise ValueError('Complete profile is ineligible for supplied parameters')
  bank=normal_bank(profile,m,b)
  if not valid_bank(bank):raise ValueError('Complete authored bank collision')
  anchor=False
 # Correct object and chosen point roles precede all render construction.
 points=[(sp.Integer(0),b),(x2,m*x2+b)];reading=sp.Rational(1,2) if level=='hard' and not raw else sp.Integer(1);assets=[]
 if raw and anchor:
  prompt=t['prompt'];values_bank=t['choice_paths'];asset=t.get('solution_path')
  sol=solution(m,b,x2,layout,asset,short=b==0) if asset else None
 else:
  prompt=f'Which of the following graphs shows the line $y={expr(m,b,layout)}?$'
  # All five answer plots use common axes; avoid incidental per-option bounds as a clue.
  xx=[0,1,float(x2)]; yy=[0]+[float(c) for a,c in bank]+[float(a+c) for a,c in bank]+[float(y) for x,y in points]
  bounds=[min(-4,math.floor(min(xx)-2)),max(4,math.ceil(max(xx)+2)),min(-4,math.floor(min(yy)-2)),max(4,math.ceil(max(yy)+2))]
  values_bank=[]
  for a,c in bank:
   v,inf=render_plot(a,c,reading=reading,bounds=bounds);values_bank.append(v);assets.append(inf)
  asset,inf=render_plot(m,b,points,reading,bounds);assets.append(inf);sol=solution(m,b,x2,layout,asset,short=b==0)
 # Identity from actual content, order-independent bank; seed/aliases excluded.
 identity=[VERSION,level,prompt,sol,sorted(values_bank),raw and anchor and t.get('difficulty_present',False)]
 qid=ident(identity);fid=ident([qid,'selection']);choices=[{':answer/id':ident([fid,v]),':answer/type':':answer.type/image',':answer/value':v} for v in values_bank]
 correct_index=bank.index((m,b));correct_uuid=choices[correct_index][':answer/id'];rng.shuffle(choices)
 f={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices}
 if not(raw and anchor and not t['correct_present']):f[':answer-field/correct']=[':answer/id',correct_uuid]
 q={':question/id':qid,':question/problem':prompt,':question/answer-fields':[f]}
 if not(raw and anchor and not t['difficulty_present']):q[':question/difficulty']=':question.difficulty/'+level
 if not(raw and anchor and not t['solution_present']):q[':question/worked-solution']=sol
 if raw and anchor and t['solution_present'] and sol!=t['solution']:raise AssertionError('Parameterized source chain differs from captured source')
 pars={'m':str(m),'b':str(b),'x2':str(x2),'layout':layout}
 # Actual supplied equation, fixed two-point roles and reading demand matter.
 # The freely chosen second x is a solution slot, not a new supplied graph-selection task.
 fp=digest([level,str(m),str(b),str(reading),'given-equation; choose-line; two-forward-computed-points; first-x-zero'])
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'template':template,'profile':profile,'parameters':pars,'source_ids':[profile] if raw else [],'basis':SOURCE['basis'],'lineage':SOURCE['lineage'],'evidence_only':raw,'eligible_for_learning':not raw,'mathematical_fingerprint':fp,'choice_lines':[[str(a),str(c)] for a,c in bank],'choice_paths':values_bank,'correct_index':correct_index,'formal_points':[[str(x),str(y)] for x,y in points],'reading_grid':str(reading),'recipes':CONTRACT['recipes'][profile],'assets':assets,'python':sys.version.split()[0],'sympy':sp.__version__,'matplotlib':matplotlib.__version__,'source_sha256':hashlib.sha256((PACKAGE/'source.json').read_bytes()).hexdigest()}}
def markdown(rec):
 q=rec['question'];s=q[':question/problem']+'\n\n'+'\n\n'.join('![]('+a[':answer/value']+')' for a in q[':question/answer-fields'][0][':answer-field/choices']);return s+'\n\n'+q.get(':question/worked-solution','[Source worked solution absent.]')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');p.add_argument('--seed',type=int,default=0);p.add_argument('--count',type=int,default=1);p.add_argument('--format',choices=['markdown','json'],default='json');p.add_argument('--template');p.add_argument('--profile');a=p.parse_args()
 rs=[generate(level,a.seed+i,template=a.template,profile=a.profile) for level in (['easy','moderate','hard'] if a.difficulty=='all' else [a.difficulty]) for i in range(a.count)];print(json.dumps(rs,indent=2) if a.format=='json' else '\n\n---\n\n'.join(map(markdown,rs)))
