#!/usr/bin/env python3
"""Seeded qualitative vector-field signs. No database writes; see package README."""
import argparse,copy,hashlib,json,random,sys,uuid
from pathlib import Path
import sympy as sp
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
D=Path(__file__).with_suffix('');ROOT=D.parents[2]
RAW=json.loads((D/'source.json').read_text());KP=RAW['record'];VERSION='qualitative-work-v1'
SOURCES={q[':question/math-academy-id']:q for q in KP[':knowledge-point/questions']}
# Profile = three (path orientation, sign assertion) pairs, independently of field layout.
PROFILES={'positive-negative-reverse-positive':[(1,1),(1,-1),(-1,1)],'positive-negative-reverse-negative':[(1,1),(1,-1),(-1,-1)],'positive-zero-reverse-zero':[(1,1),(1,0),(-1,0)],'negative-zero-reverse-negative':[(1,-1),(1,0),(-1,-1)],'negative-zero-reverse-positive':[(1,-1),(1,0),(-1,1)],'positive-zero-reverse-negative':[(1,1),(1,0),(-1,-1)]}
# Every source has a concrete preserved replay, including the source's field-owned bank.
SOURCE_CASES={
'q-125380':('segment_perpendicular',0,'positive-zero-reverse-zero'),
'q-125381':('ellipse_tangent',-1,'positive-negative-reverse-positive'),
'q-125500':('ellipse_normal',0,'negative-zero-reverse-negative'),
'q-125501':('ellipse_normal',0,'negative-zero-reverse-positive'),
'q-125504':('ellipse_normal',0,'positive-zero-reverse-negative'),
'q-125507':('ellipse_tangent',-1,'positive-negative-reverse-positive'),
'q-125688':('curve_against',-1,'positive-negative-reverse-positive'),
'q-150018':('segment_perpendicular',0,'positive-zero-reverse-negative'),
'q-125499':('ellipse_tangent',1,'positive-negative-reverse-positive'),
'q-125687':('curve_against',-1,'positive-negative-reverse-positive'),
'q-150013':('curve_with',1,'positive-negative-reverse-negative'),
'q-125502':('ellipse_normal',0,'positive-zero-reverse-zero'),
'q-125497':('ellipse_tangent',1,'positive-negative-reverse-positive')}
LEVELS={'easy':['ellipse_tangent'],'moderate':['ellipse_normal']}
def uid(parts):return str(uuid.uuid5(uuid.UUID(KP[':knowledge-point/id']),json.dumps(parts,sort_keys=True)))
def truth(sign,profile):return [orient*sign==assertion for orient,assertion in PROFILES[profile]]
def subset(values):
 names=[n for n,v in zip(('I','II','III'),values) if v]
 return (' and '.join(names)+' only') if len(names)<3 else 'I, II, and III'
def normalize(q):
 return {':question/id':q[':question/id'],':question/problem':q[':question/problem'],':question/worked-solution':q[':question/worked-solution'],':question/difficulty':q[':question/difficulty'][':db/ident'],':question/answer-fields':[{':answer-field/id':f[':answer-field/id'],':answer-field/key':f[':answer-field/key'],':answer-field/type':f[':answer-field/type'][':db/ident'],':answer-field/correct':[':answer/id',f[':answer-field/correct'][':answer/id']],':answer-field/choices':[{':answer/id':a[':answer/id'],':answer/type':a[':answer/type'][':db/ident'],':answer/value':a[':answer/value']} for a in f[':answer-field/choices']]} for f in q[':question/answer-fields']]}
def replay(mid):
 family,sign,profile=SOURCE_CASES[mid]
 return {'question':normalize(SOURCES[mid]),'knowledge_point':{'db_id':KP[':db/id'],'title':KP[':knowledge-point/title']},'generation':{'version':VERSION,'template':family,'source_id':mid,'profile':profile,'sign':sign,'evidence_only':True,'eligible_for_learning':False,'source_basis':RAW['basis']}}
def guard(level,p):
 if level not in LEVELS:raise ValueError('Unsupported difficulty: '+str(level))
 if set(p)!={'a','b','start','sweep','direction','force_sign'}:raise ValueError('Unknown parameter slots')
 if (p['a'],p['b']) not in ((1,1),(2,1),(1,2),(3,2),(2,3)):raise ValueError('Unsupported axis ratio')
 if p['start'] not in range(4) or p['direction'] not in (-1,1) or p['force_sign'] not in (-1,1):raise ValueError('Invalid geometry/orientation')
 if p['sweep'] not in ((2,3) if level=='easy' else (1,2)):raise ValueError('Sweep outside source backbone')
 return p

def math_data(level,p):
 guard(level,p);a,b=p['a'],p['b'];t=sp.symbols('t',real=True);x,y=sp.symbols('x y',real=True)
 angle=sp.pi/2*(p['start']+p['direction']*t);r=sp.Matrix([a*sp.cos(angle),b*sp.sin(angle)])
 field=sp.Matrix([-a*a*y,b*b*x]) if level=='easy' else sp.Matrix([b*b*x,a*a*y]);field*=p['force_sign']
 force=field.subs({x:r[0],y:r[1]},simultaneous=True);dot=sp.trigsimp(force.dot(r.diff(t)));work=sp.integrate(dot,(t,0,p['sweep']))
 return {'t':t,'r':r,'field':field,'force':force,'dot':dot,'work':work,'sign':int(sp.sign(work))}
def fingerprint(level,p):
 # Positive field scale and common geometric scale never make a task. Axes are
 # reduced to a ratio; seed, bank, statement order, identity are absent.
 guard(level,p);shape='circle' if p['a']==p['b'] else 'ellipse'
 return json.dumps([level,shape,p['sweep'],p['direction']*p['force_sign'] if level=='easy' else 0],separators=(',',':'))
def render(level,p,out):
 """Programmatic prompt, forward-motion and reverse-motion plot set."""
 guard(level,p);out=Path(out);out.mkdir(parents=True,exist_ok=True)
 digest=hashlib.sha256(json.dumps([level,p],sort_keys=True).encode()).hexdigest()[:20];a,b=p['a'],p['b'];fs=p['force_sign'];assets={}
 for role in ('prompt','forward','reverse'):
  path=out/(digest+'-'+role+'.png')
  if path.exists():assets[role]=str(path);continue
  fig,ax=plt.subplots(figsize=(5,4.6),dpi=130);X,Y=np.meshgrid(np.linspace(-1.35*a,1.35*a,13),np.linspace(-1.35*b,1.35*b,13))
  U,V=(-a*a*Y,b*b*X) if level=='easy' else (b*b*X,a*a*Y)
  # One common scale, never per-arrow normalization; relative magnitudes remain.
  scale=max(np.max(np.hypot(U,V)),1);ax.quiver(X,Y,fs*U/scale,fs*V/scale,color='#888888',angles='xy',scale_units='xy',scale=2.3/min(a,b),width=.0035)
  ts=np.linspace(0,p['sweep'],180);ang=np.pi/2*(p['start']+p['direction']*ts);xx,yy=a*np.cos(ang),b*np.sin(ang)
  ax.plot(xx,yy,color='#2378b8',lw=2.5,zorder=3)
  for label,j in [('A',0),('B',-1)]:ax.plot(xx[j],yy[j],'o',color='#2378b8',ms=4);ax.annotate('$'+label+'$',(xx[j],yy[j]),xytext=(8,8),textcoords='offset points',color='#2378b8',fontsize=13)
  if role!='prompt':
   i,j=(78,92) if role=='forward' else (92,78);ax.annotate('',(xx[j],yy[j]),(xx[i],yy[i]),arrowprops={'arrowstyle':'->','color':'#d2581b','lw':2.6},zorder=4)
  ax.axhline(0,color='black',lw=.8);ax.axvline(0,color='black',lw=.8);ax.text(1.43*a,0,'$x$');ax.text(0,1.44*b,'$y$')
  ax.set(xlim=(-1.5*a,1.5*a),ylim=(-1.5*b,1.5*b),aspect='equal');ax.set_xticks([]);ax.set_yticks([])
  for spine in ax.spines.values():spine.set_visible(False)
  fig.tight_layout();fig.savefig(path,facecolor='white',metadata={'Software':VERSION});plt.close(fig);assets[role]=str(path)
 return assets

def generate(level,seed=0,parameters=None,profile=None,field_type='checkbox',output_dir=None):
 rng=random.Random(seed)
 # Easy: with/against a curved path. Moderate: nonzero normal field, zero work.
 p=parameters or dict(zip(('a','b'),rng.choice(((1,1),(2,1),(1,2),(3,2),(2,3)))),start=rng.randrange(4),sweep=rng.choice((2,3) if level=='easy' else (1,2)),direction=rng.choice((-1,1)),force_sign=rng.choice((-1,1)))
 guard(level,p)
 profile=profile or ('positive-negative-reverse-positive' if level=='easy' else rng.choice(('positive-zero-reverse-zero','negative-zero-reverse-negative','negative-zero-reverse-positive','positive-zero-reverse-negative')))
 if profile not in (('positive-negative-reverse-positive',) if level=='easy' else ('positive-zero-reverse-zero','negative-zero-reverse-negative','negative-zero-reverse-positive','positive-zero-reverse-negative')):raise ValueError('Profile not observed at this difficulty')
 if field_type not in ('radio','checkbox'):raise ValueError('Unsupported field layout')
 if field_type=='radio' and profile not in ('positive-negative-reverse-positive','positive-zero-reverse-zero'):raise ValueError('No radio source bank observed for profile')
 d=math_data(level,p);values=truth(d['sign'],profile);qid=uid([VERSION,level,p,profile,field_type]);assets=render(level,p,output_dir or D/'assets')
 def asset(role):return Path(assets[role]).resolve().relative_to(ROOT).as_posix()
 relation={1:'>0',-1:'<0',0:'=0'}
 statements=[r'${\int }_{'+('C' if ori==1 else '-C')+r'}F\cdot \text{d}r'+relation[sgn]+'$' for ori,sgn in PROFILES[profile]]
 shape='semicircle' if p['a']==p['b'] and p['sweep']==2 else 'three-quarter circle' if p['a']==p['b'] and p['sweep']==3 else 'quarter circle' if p['a']==p['b'] else 'elliptic arc'
 prompt='![]('+asset('prompt')+')\n\nConsider the vector field $F(x,y)$ shown above. Let $C$ be the path where the '+shape+' is traversed from $A$ to $B.$ Which of the following statements are true?\n\n'
 prompt+='\n\n'.join((n+'. ' if field_type=='radio' else '- ')+st for n,st in zip(('I','II','III'),statements))
 if field_type=='checkbox':prompt+='\n\nSelect all that apply.'
 original=SOURCES['q-125380'][':question/worked-solution'];solution=original.split("With that in mind")[0]+"With that in mind, let's check each statement.\n\n"
 if d['sign']==0:explain='Since the force $F$ acts perpendicular to the motion of the particle as it moves from $A$ to $B,$ it neither helps nor hinders its motion.';rev='If we reverse the orientation of $C,$ the force is still perpendicular to the motion.'
 elif d['sign']>0:explain='The force $F$ assists the motion of the particle as it moves from $A$ to $B.$';rev='The force $F$ works against the motion of the particle as it moves from $B$ to $A.$'
 else:explain='The force $F$ works against the motion of the particle as it moves from $A$ to $B.$';rev='The force $F$ assists the motion of the particle as it moves from $B$ to $A.$'
 solution+='- Statement I is '+str(values[0]).lower()+', while statement II is '+str(values[1]).lower()+'. '+explain+'\n\n![]('+asset('forward')+')\n\nSo, '+r'${\int }_{C}F\cdot \text{d}r'+relation[d['sign']]+'$.\n\n'
 solution+='- Statement III is '+str(values[2]).lower()+'. '+rev+'\n\n![]('+asset('reverse')+')\n\nSo, '+r'${\int }_{-C}F\cdot \text{d}r'+relation[-d['sign']]+'$.\n\nTherefore, the correct answer is "'+subset(values)+'."'
 fields=[]
 if field_type=='checkbox':banks=[(n,('false','true'),str(v).lower()) for n,v in zip(('I','II','III'),values)]
 else:banks=[('selection',('I only','II only','III only','I and III only','II and III only'),subset(values))]
 for key,bank,correct in banks:
  fid=uid([qid,key]);answers=[{':answer/id':uid([fid,val]),':answer/type':':answer.type/text',':answer/value':val} for val in bank];assert correct in bank
  fields.append({':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+field_type,':answer-field/choices':answers,':answer-field/correct':[':answer/id',uid([fid,correct])]})
 return {'question':{':question/id':qid,':question/problem':prompt,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+level,':question/answer-fields':fields},'knowledge_point':{'db_id':KP[':db/id'],'title':KP[':knowledge-point/title']},'generation':{'version':VERSION,'seed':seed,'template':LEVELS[level][0],'parameters':p,'profile':profile,'field_type':field_type,'mathematical_fingerprint':fingerprint(level,p),'field':list(map(str,d['field'])),'work':str(d['work']),'sign':d['sign'],'assets':assets,'source_ids':[m for m,c in SOURCE_CASES.items() if c[0]==LEVELS[level][0]],'evidence_only':False,'eligible_for_learning':True,'dependencies':{'sympy':sp.__version__,'matplotlib':matplotlib.__version__,'numpy':np.__version__}}}

# Every learner-facing checkbox question has a nonempty correct selection.
import sys as _policy_sys
from pathlib import Path as _PolicyPath
_policy_sys.path.insert(0, str(next(p for p in _PolicyPath(__file__).resolve().parents if (p / "scripts/generator_policy.py").is_file())))
from scripts.generator_policy import nonempty_checkbox as _nonempty_checkbox
for _policy_name in ['generate']:
    globals()[_policy_name] = _nonempty_checkbox(globals()[_policy_name])

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=(*LEVELS,'hard'),default='easy');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--replay',choices=list(SOURCES));ap.add_argument('--output',type=Path);a=ap.parse_args();r=replay(a.replay) if a.replay else generate(a.difficulty,a.seed);text=json.dumps(r,indent=2)+'\n'
 if a.output:a.output.write_text(text)
 else:print(text)
