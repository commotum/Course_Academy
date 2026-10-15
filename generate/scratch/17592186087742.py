#!/usr/bin/env python3
"""Circle parametrization: observed easy recognition and moderate oriented construction.

Radius is the sole mathematical slot. Center, full-period domain, speed, starting
axis point and orientation stay fixed because varying these changes the source
solution stages. See package evidence for bounded unsupported hard scope.
"""
from __future__ import annotations
import argparse,hashlib,json,random,re,uuid
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().with_suffix('')
SNAP=json.loads((HERE/'source.json').read_text());KP_ID=17592186087742
KP_UUID=SNAP['record'][':knowledge-point/id'];TITLE=SNAP['record'][':knowledge-point/title']
VERSION='circle-origin-parametric-v1';LEVELS=('easy','moderate')
ORIGINALS={q[':question/math-academy-id']:q for q in SNAP['record'][':knowledge-point/questions']}
R=sp.Symbol('r',positive=True)
# Complete source bank profiles: (x amplitude,y amplitude,swapped trig,x shift,y shift).
def pair(a,b=None,swap=False,h=0,k=0):return (a,a if b is None else b,swap,h,k)
C=pair(R)
PROFILES={
'q-105915':[pair(2*R),C,pair(R**2),pair(R/2),pair(sp.sqrt(R))],
'q-106032':[pair(2*R),pair(sp.sqrt(R)),pair(1/R),pair(R**2),C],
'q-15802':[pair(sp.sqrt(R),swap=True),pair(R**2,swap=True),pair(2*R,swap=True),pair(R/2,swap=True),C],
'q-6896':[C,pair(R/2,swap=True),pair(2*R,swap=True),pair(R**2,swap=True),pair(sp.sqrt(R),swap=True)],
'q-6877':[pair(1,swap=True,h=R,k=R),pair(R**2),pair(R**2,swap=True),pair(sp.sqrt(R),swap=True),C],
'q-105916':[pair(1/R**2),pair(2*R),pair(R**2),C,pair(1/R)],
'q-106040':[pair(sp.sqrt(R)),pair(R**2,2*R),pair(2*R),C,pair(R**2)],
'q-6878':[pair(R,swap=True),pair(sp.sqrt(R)),pair(2*R),pair(sp.sqrt(R),swap=True),C],
'q-6893':[C,pair(sp.sqrt(R),swap=True),pair(R,swap=True),pair(2*R),pair(sp.sqrt(R))],
'q-15857':[pair(2*R),pair(sp.sqrt(R)),pair(sp.sqrt(R),swap=True),C,pair(R,swap=True)],
'q-15804':[pair(2*R,R,True),pair(sp.sqrt(R)),pair(2*R,R/2),pair(R,swap=True),C],
'q-15851':[pair(R/2,swap=True),pair(R**2,swap=True),C,pair(2*R,swap=True),pair(sp.sqrt(R),swap=True)]}
RADII={'q-105915':'15','q-106032':'1/2','q-15802':'5','q-6896':'7','q-6877':'3','q-105916':'1/3','q-106040':'5','q-6878':'9','q-6893':'12','q-15857':'16','q-321890':'4','q-321891':'10','q-15804':'8','q-15851':'6'}
INCOMPLETE={'q-15804','q-15851'}

def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def uid(x):return str(uuid.uuid5(uuid.NAMESPACE_URL,'course-academy:'+str(KP_ID)+':'+str(x)))
GENERATOR_UUID=uid('question-generator')
def tex(x):return sp.latex(sp.sympify(x))
def radius_from_prompt(text):
 s=re.search(r'circle of radius \$(.*?)\$',text)[1]
 m=re.fullmatch(r'\\frac\{(\d+)\}\{(\d+)\}',s)
 return sp.Rational(*map(int,m.groups())) if m else sp.Rational(s)
def level_of(sid):
 q=ORIGINALS[sid]
 return q.get(':question/difficulty',{}).get(':db/ident',':question.difficulty/'+('moderate'if sid=='q-15804'else'easy')).split('/')[-1]
def bank(sid,r):return [tuple(sp.simplify(z.subs(R,r))if isinstance(z,sp.Basic)else z for z in row)for row in PROFILES[sid]]
def expression(a,fn,shift=0):
 return (''if a==1 else tex(a))+ '\\'+fn+r'\theta'+('+'+tex(shift)if shift else'')
def bank_value(row):
 a,b,swap,h,k=row
 return 'x='+expression(a,'sin'if swap else'cos',h)+r',\,y='+expression(b,'cos'if swap else'sin',k)
def parse_value(text):
 """Read complete source or generated equations, including shifted-center banks."""
 s=text.replace('\\\\','\\').replace('⁡','').replace('θ',r'\theta').replace(r'\operatorname{cos}',r'\cos').replace(r'\operatorname{sin}',r'\sin').replace(r'\,','').replace(' ','')
 # q-6896 contains a documented source decimal-comma typo; caller must opt to correct it.
 if '3,5\\cos' in s:raise ValueError('Malformed decimal comma in q-6896')
 parts=re.split(r',y=',s);assert len(parts)==2,s
 out=[]
 for var,part in zip(('x','y'),parts):
  part=part.removeprefix(var+'=');m=re.fullmatch(r'(.*?)\\(sin|cos)\\theta(?:\+(.*))?',part);assert m,part
  def math(z):
   if not z:return sp.Integer(1)
   z=re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}',r'((\1)/(\2))',z)
   z=re.sub(r'\\sqrt\{([^{}]+)\}',r'sqrt(\1)',z)
   z=re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}',r'((\1)/(\2))',z)
   return sp.sympify(re.sub(r'(\d)(sqrt\()',r'\1*\2',z),rational=True)
  out.append((math(m[1]),m[2],math(m[3])if m[3]else sp.Integer(0)))
 return out

def valid_bank(sid,r):
 rows=bank(sid,r);theta=sp.Symbol('theta',real=True);truth=[];objs=[]
 for row in rows:
  a,b,swap,h,k=row;x=a*(sp.sin(theta)if swap else sp.cos(theta))+h;y=b*(sp.cos(theta)if swap else sp.sin(theta))+k
  objs.append((x,y))
  if level_of(sid)=='easy':good=h==k==0 and sp.simplify(a*a-r*r)==0 and sp.simplify(b*b-r*r)==0
  else:good=h==k==0 and not swap and a==b==r
  truth.append(bool(good))
 if len(set(objs))!=5 or sum(truth)!=1:raise ValueError('Complete bank collision or multiple correct choices')
 return rows,truth

def render_plot(r,out):
 import matplotlib
 matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 import numpy as np
 out=Path(out);out.mkdir(parents=True,exist_ok=True);path=out/('circle-'+digest(str(r))[:16]+'.png')
 if path.exists():return path
 fig,ax=plt.subplots(figsize=(4.3,3.7),dpi=140);v=float(r);angles=np.linspace(0,2*np.pi,500)
 ax.plot(v*np.cos(angles),v*np.sin(angles),color='#2878b8',lw=1.7)
 for axis in ('left','bottom'):ax.spines[axis].set_position('zero')
 for axis in ('right','top'):ax.spines[axis].set_visible(False)
 ax.set_xlim(-1.4*v,1.6*v);ax.set_ylim(-1.4*v,1.55*v);ax.set_aspect('equal')
 ax.set_xticks([-v,v],['$-'+tex(r)+'$','$'+tex(r)+'$']);ax.set_yticks([-v,v],['$-'+tex(r)+'$','$'+tex(r)+'$'])
 ax.scatter([v],[0],s=22,c='#dd9c00',zorder=5);ax.annotate('$A('+tex(r)+',0)$',(v,0),xytext=(3,10),textcoords='offset points',fontsize=11)
 ax.annotate('',xy=(v*np.cos(.85),v*np.sin(.85)),xytext=(v*np.cos(.65),v*np.sin(.65)),arrowprops={'arrowstyle':'->','color':'#2878b8','lw':1.5})
 ax.text(1.48*v,.07*v,'$x$');ax.text(.06*v,1.43*v,'$y$');ax.plot(1.6*v,0,'>k',clip_on=False,ms=5);ax.plot(0,1.55*v,'^k',clip_on=False,ms=5)
 fig.tight_layout();fig.savefig(path,metadata={'Software':VERSION});plt.close(fig);return path

def text_slots(sid,r,assets):
 q=ORIGINALS[sid];old=sp.Rational(RADII[sid]);oldtex=tex(old)
 def replace(s):
  if old.q==1:return re.sub(r'(?<![\d])'+re.escape(str(old))+r'(?![\d])',lambda m:tex(r),s)
  return s.replace(oldtex,tex(r))
 prompt=q[':question/problem'];plot=re.search(r'!\[\]\((.*?)\)',prompt)
 if plot:prompt=prompt[:plot.start()]+'{{CIRCLE_ASSET}}'+prompt[plot.end():]
 prompt=replace(prompt)
 if plot:prompt=prompt.replace('{{CIRCLE_ASSET}}','![]('+str(render_plot(r,assets))+')')
 return prompt,replace(q[':question/worked-solution'])

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None,output_dir=None):
 if level not in LEVELS:raise ValueError('Unsupported hard: no same-method difficulty increase established')
 eligible=[sid for sid in ORIGINALS if sid not in INCOMPLETE and level_of(sid)==level and (field_type is None or ('blank'if sid.startswith('q-32189')else'radio')==field_type)]
 if profile:template=profile.removeprefix('bank-')
 rng=random.Random(seed);sid=template or rng.choice(eligible)
 if sid not in eligible:raise ValueError('Unsupported source template / difficulty / field combination')
 for attempt in range(100):
  r=sp.Rational(parameters['radius'])if parameters else (sp.Rational(rng.randint(1,19),rng.choice([2,3,4,5]))if level=='easy'and rng.random()<.3 else sp.Integer(rng.randint(2,30)))
  if not 0<r<=30 or r.q>5 or level=='moderate'and r.q!=1:raise ValueError('Radius must be positive <=30, denominator <=5; moderate integer')
  try:
   rows,truth=valid_bank(sid,r)if sid in PROFILES else (None,None)
  except ValueError:
   if parameters:raise
   continue
  break
 else:raise ValueError('Bounded sampling exhausted')
 prompt,solution=text_slots(sid,r,output_dir or HERE/'assets')
 layout=[]
 if rows:layout=[('selection',[bank_value(row)for row in rows],truth.index(True))]
 else:
  # Two RHS fragments, exactly as supplied after x= and y= in the prompt.
  layout=[('field-1',[expression(r,'cos')],0),('field-2',[expression(r,'sin')],0)]
 identity=digest({'version':VERSION,'prompt':re.sub(r'!\[\]\(.*?\)', '{{circle}}',prompt),'solution':solution,'level':level,'bank':layout});qid=uid(identity);fields=[]
 for key,values,ci in layout:
  fid=uid(qid+key);answers=[{':answer/id':uid(fid+value),':answer/type':':answer.type/math',':answer/value':value}for value in values]
  correct=answers[ci][':answer/id'];random.Random(seed).shuffle(answers)
  fields.append({':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+('radio'if rows else'blank'),':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]})
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':qid,':question/problem':prompt,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+level,':question/answer-fields':fields},'generation':{'version':VERSION,'seed':seed,'template':sid,'profile':'bank-'+sid if rows else None,'parameters':{'radius':str(r)},'source_basis':SNAP['basis'],'source_lineage':SNAP['lineage'],'source_question':sid,'sympy_version':sp.__version__,'plot_rating':'moderate'if level=='moderate'else'none','assets':re.findall(r'!\[\]\((.*?)\)',prompt),'task_fingerprint':digest({'radius':str(r),'task':'oriented'if level=='moderate'else'recognition'})}}

def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)
def markdown(r):
 q=r['question'];return q[':question/problem']+'\n\n'+json.dumps(q[':question/answer-fields'],ensure_ascii=False,indent=2)+'\n\n'+q[':question/worked-solution']
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--difficulty',default='easy');p.add_argument('--seed',type=int,default=0);p.add_argument('--count',type=int,default=1);p.add_argument('--template');p.add_argument('--field-type');p.add_argument('--format',default='json');a=p.parse_args()
 records=[]
 for level in (LEVELS if a.difficulty=='all'else[a.difficulty]):
  seen=set();accepted=[]
  if a.count<0:raise ValueError('Count cannot be negative')
  for index in range(1000):
   if len(accepted)>=a.count:break
   record=generate(level,a.seed+index,template=a.template,field_type=a.field_type)
   fp=record['generation']['task_fingerprint']
   if fp not in seen:seen.add(fp);accepted.append(record)
  if len(accepted)<a.count:raise ValueError('Finite-limit: bounded distinct radius domain exhausted; requested '+str(a.count)+', produced '+str(len(accepted)))
  records.extend(accepted)
 print(json.dumps(records,ensure_ascii=False,indent=2)if a.format=='json'else'\n\n---\n\n'.join(map(markdown,records)))
