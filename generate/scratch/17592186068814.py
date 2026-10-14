#!/usr/bin/env python3
"""Negative reciprocal-stretch image radios, frozen math basis 1356; steps 3–7.

Public raw_<source> profiles parameterize the complete observed prompt, two-stage
solution and every image-bank recipe. Original parameters retain native rasters;
changed parameters render the same recipes. The two unrated raw profiles retain
missing difficulty/solution/correct refs; raw_q-99068 has an opaque doubled
coefficient and is evidence-only. Default complete method banks are selected before
parameters. Explicit inputs obey the identical workload and visibility bounds.
No positive-reciprocal prompt, translations, unknown-coefficient or DB operations.
"""
from __future__ import annotations
import argparse,hashlib,json,random,sys,uuid,os,tempfile,threading
from pathlib import Path
from fractions import Fraction
import sympy as sp
import numpy as np
os.environ.setdefault('MPLCONFIGDIR', '/tmp/reciprocal-stretch-mpl')
import matplotlib
matplotlib.use('Agg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg

KP_ID=17592186068814
KP_UUID='52e11164-1929-594d-9f9e-460f6469421d'
TITLE='Graphing a Stretched Negative Reciprocal Function'
VERSION='negative-reciprocal-stretch-1'
HERE=Path(__file__).resolve().with_suffix('')
SOURCE=json.loads((HERE/'source.json').read_text())
QS={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
SOURCE_PARAMETERS={'q-97958':(3,2),'q-97963':(3,1),'q-113335':(1,6),'q-113337':(5,2),'q-113339':(7,3),'q-113341':(5,4),'q-113336':(6,1),'q-97949':(3,4),'q-99068':(1,4)}
PROFILES={
 'raw_q-97958':('moderate','rational',('-1','1','a','-numerator','-a')),
 'raw_q-97963':('easy','integer',('-a','-rounded_inverse','-1','1','a')),
 'raw_q-113335':('easy','unit_numerator',('-a','-1','-inverse','a','inverse')),
 'raw_q-113337':('moderate','rational',('-a','inverse','-inverse','-1','a')),
 'raw_q-113339':('moderate','rational',('a','-1','-denominator','-inverse','-a')),
 'raw_q-113341':('moderate','rational',('a','-inverse','-a','inverse','-1')),
 'raw_q-113336':('easy','integer',('inverse','-a','a','-inverse','-1')),
 'raw_q-97949':('moderate','rational',('-a','a','1','-numerator','-1')),
 'raw_q-99068':('easy','unit_numerator',('-1','-inverse','-a','inverse','-double')),
 'integer_reversal':('easy','integer',('inverse','-a','a','-inverse','-1')),
 'unit_numerator_reversal':('easy','unit_numerator',('-a','-1','-inverse','a','inverse')),
 'rational_reversal':('moderate','rational',('-a','inverse','-inverse','-1','a')),
 'rational_numerator':('moderate','rational',('-a','a','1','-numerator','-1')),
 'rational_denominator':('moderate','rational',('a','-1','-denominator','-inverse','-a')),
 'nonunit_point_reversal':('hard','nonunit_point',('-a','a','inverse','-inverse','-1')),
 'nonunit_point_numerator':('hard','nonunit_point',('-a','a','1','-numerator','-1')),
}
LOCK=threading.RLock()

def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def ident(x):return str(uuid.uuid5(uuid.NAMESPACE_URL,VERSION+':'+x))
def tex(v):
 v=Fraction(v)
 return str(v.numerator) if v.denominator==1 else ('-' if v<0 else '')+r'\frac{'+str(abs(v.numerator))+'}{'+str(v.denominator)+'}'
def expr(n,d):return r'-\frac{'+str(n)+'}{'+('' if d==1 else str(d))+'x}'
def recipe_values(p,profile):
 n,d=p['n'],p['d'];a=Fraction(n,d)
 values={'a':a,'-a':-a,'1':Fraction(1),'-1':Fraction(-1),'inverse':1/a,'-inverse':-1/a,'unit_denominator':Fraction(1,d),'-unit_denominator':Fraction(-1,d),'numerator':Fraction(n),'double':2*a,'-double':-2*a,'-numerator':Fraction(-n),'-denominator':Fraction(-d),'-rounded_inverse':-Fraction((200*d+n)//(2*n),100)}
 return [values[k] for k in PROFILES[profile][2]]

def domain(profile):
 level,t,_=PROFILES[profile]
 if t=='integer':return [{'n':n,'d':1} for n in range(2,13)]
 if t=='unit_numerator':return [{'n':1,'d':d} for d in range(2,13)]
 ds=range(2,6) if level=='moderate' else range(6,13)
 return [{'n':n,'d':d} for d in ds for n in range(2,25) if sp.gcd(n,d)==1 and Fraction(1,3)<=Fraction(n,d)<=4 and n!=d]

def checked(p,profile):
 if set(p)!= {'n','d'} or any(type(p[k]) is not int for k in p):raise ValueError('Parameters must be exactly integer n and d')
 if p not in domain(profile):raise ValueError('Outside this profile’s positive reduced workload bounds')
 vs=recipe_values(p,profile)
 if len(set(vs))!=5 or vs.count(-Fraction(p['n'],p['d']))!=1:raise ValueError('Whole bank has equivalent graph choices')
 return vs

def atomic(path,data):
 path.parent.mkdir(parents=True,exist_ok=True)
 fd,name=tempfile.mkstemp(prefix='render-',suffix='.tmp',dir=path.parent)
 try:
  with os.fdopen(fd,'wb') as f:f.write(data)
  os.replace(name,path)
 finally:
  if os.path.exists(name):os.unlink(name)

def render_curve(c,mark_x=1,out_dir=None):
 """Exact c/x branch geometry, separately rendered branches and coordinate marks.

 Independent x/y scaling centers the marked points in every image. Curve shape
 cannot alone encode c when scale changes: coordinate labels remain decisive,
 matching the original plots. All images use the same native size/typography.
 """
 c=Fraction(c);m=Fraction(mark_x)
 if c==0 or m<=0:raise ValueError('Nonzero reciprocal and positive mark required')
 out_dir=Path(out_dir or HERE/'plots');key=digest([VERSION,str(c),str(m),'marked-coordinate'])
 png=out_dir/(key+'.png');side=out_dir/(key+'.json')
 with LOCK:
  if png.exists() and side.exists():return str(png.relative_to(Path.cwd())) if png.is_relative_to(Path.cwd()) else str(png)
  xlim=float(m)*4.1;ylim=max(float(abs(c)/m)*2.6,0.1)
  fig=Figure(figsize=(3.6,3.04),dpi=100);FigureCanvasAgg(fig)
  ax=fig.add_axes([.07,.09,.86,.84]);ax.set_xlim(-xlim,xlim);ax.set_ylim(-ylim,ylim);ax.axis('off')
  ax.annotate('',(xlim,0),(-xlim,0),arrowprops={'arrowstyle':'->','lw':1,'color':'black'})
  ax.annotate('',(0,ylim),(0,-ylim),arrowprops={'arrowstyle':'->','lw':1,'color':'black'})
  axis_titles=[ax.text(xlim*1.08,0,'$x$',fontsize=11,ha='center',va='center'),ax.text(0,ylim*1.08,'$y$',fontsize=11,ha='center',va='center')]
  xmin=float(abs(c))/ylim*1.015
  xs=np.geomspace(xmin,xlim,600)
  branches=[]
  for sign in (-1,1):
   xx=sign*xs; yy=float(c)/xx;ax.plot(xx,yy,color='#287ab5',lw=1.5)
   branches.append({'sign_x':sign,'x_start':float(xx[0]),'x_end':float(xx[-1]),'y_start':float(yy[0]),'y_end':float(yy[-1])})
  points=[];labels=[]
  for sign in (-1,1):
   x=sign*m;y=c/x;ax.plot(float(x),float(y),'o',color='#287ab5',ms=4)
   label='$('+tex(x)+','+tex(y)+')$';off=(6,10) if sign==1 else (-6,-18)
   # Negative reciprocal choices require the label in the same branch-side role.
   if c<0:off=(6,-18) if sign==1 else (-6,10)
   artist=ax.annotate(label,(float(x),float(y)),xytext=off,textcoords='offset points',ha='left' if sign==1 else 'right',fontsize=10)
   points.append([str(x),str(y)]);labels.append(artist)
  fig.canvas.draw();renderer=fig.canvas.get_renderer();bbox=[list(t.get_window_extent(renderer).bounds) for t in labels]
  title_bbox=[list(t.get_window_extent(renderer).bounds) for t in axis_titles]
  for b in bbox+title_bbox:
   if b[0]<1 or b[1]<1 or b[0]+b[2]>359 or b[1]+b[3]>303:raise ValueError('Whole bank coordinate label clipped')
  from io import BytesIO
  buffer=BytesIO();fig.savefig(buffer,format='png',dpi=100)
  atomic(png,buffer.getvalue());atomic(side,json.dumps({'coefficient':str(c),'mark_x':str(m),'points':points,'xlim':[-xlim,xlim],'ylim':[-ylim,ylim],'branch_count':2,'branches':branches,'labels':bbox,'axis_titles':title_bbox,'python':sys.version.split()[0],'matplotlib':matplotlib.__version__},indent=2).encode())
 return str(png.relative_to(Path.cwd())) if png.is_relative_to(Path.cwd()) else str(png)

def image_bank(p,profile,vs):
 raw=profile.startswith('raw_');sid=profile.removeprefix('raw_');anchor=raw and tuple(p[k] for k in ('n','d'))==SOURCE_PARAMETERS[sid]
 m=2 if PROFILES[profile][0]=='hard' else 1
 if anchor:return [a[':answer/value'] for a in QS[sid][':question/answer-fields'][0][':answer-field/choices']]
 return [render_curve(v,m) for v in vs]

def solution(p,base,correct):
 e=expr(p['n'],p['d']);a=tex(Fraction(p['n'],p['d']))
 return 'To plot $y='+e+',$ we apply the following steps:\n\n- Take the curve $y='+r'-\frac{1}{x}.$'+'\n\n![]('+base+')\n\n- Stretch the result by a scale factor of $'+a+'$ parallel to the $y$-axis to get the graph of $y='+e+'.$\n\n![]('+correct+')'

def raw_masks(sid,p,bank):
 """Source strings become complete component masks, never literal return branches.
 Ordered source image roles are mapped to the source bank or base curve. Missing
 strings remain absent. Nonmath punctuation (including dollar placement) is fixed.
 """
 import re
 original=QS[sid];n,d=SOURCE_PARAMETERS[sid];old=expr(n,d);new=expr(p['n'],p['d'])
 prompt=original[':question/problem'].replace(old,new)
 if ':question/worked-solution' not in original:return prompt,None
 sol=original[':question/worked-solution'].replace(old,new)
 oldscale=tex(Fraction(n,d));newscale=tex(Fraction(p['n'],p['d']))
 sol=sol.replace('scale factor of $'+oldscale+'$', 'scale factor of $'+newscale+'$')
 paths=re.findall(r'!\[\]\(([^)]+)\)',original[':question/worked-solution'])
 anchor=(p['n'],p['d'])==(n,d)
 base=paths[0] if anchor else render_curve(-1)
 # Replace complete image slots; a base asset can also occur in the answer bank.
 newpaths=[base,bank[recipe_values(p,'raw_'+sid).index(-Fraction(p['n'],p['d']))]]
 it=iter(newpaths);sol=re.sub(r'!\[\]\([^)]+\)',lambda _: '![]('+next(it)+')',sol)
 return prompt,sol

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('Unknown level')
 if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Only observed image radio field')
 rng=random.Random(seed)
 if profile is None:
  eligible=[k for k,v in PROFILES.items() if v[0]==level and not k.startswith('raw_') and (template is None or v[1]==template)]
  if not eligible:raise ValueError('Unknown template for this level')
  profile=rng.choice(eligible)
 if profile not in PROFILES or PROFILES[profile][0]!=level:raise ValueError('Profile not applicable to level')
 actual_template=PROFILES[profile][1]
 if template not in (None,actual_template):raise ValueError('Template/profile mismatch')
 if parameters is not None:p=dict(parameters);vs=checked(p,profile)
 else:
  candidates=domain(profile);rng.shuffle(candidates)
  for p in candidates:
   try:vs=checked(p,profile);break
   except ValueError:continue
  else:raise ValueError('No eligible whole bank')
 bank=image_bank(p,profile,vs);a=-Fraction(p['n'],p['d']);ci=vs.index(a)
 raw=profile.startswith('raw_');sid=profile.removeprefix('raw_')
 if raw:prompt,sol=raw_masks(sid,p,bank)
 else:
  prompt='Which of the following is the graph of $y='+expr(p['n'],p['d'])+'?$'
  sol=solution(p,render_curve(-1,2 if level=='hard' else 1),bank[ci])
 missing=raw and sid in ('q-97958','q-97963')
 opaque=raw and sid=='q-99068'
 fp=digest(['negative-reciprocal-selection',str(a),2 if level=='hard' else 1])
 identity=digest([VERSION,None if missing else level,prompt,sol,sorted(bank),not missing])
 qid=ident(identity);fid=ident(identity+':selection')
 choices=[{':answer/id':ident(identity+':selection:'+value),':answer/type':':answer.type/image',':answer/value':value} for value in bank]
 correctid=choices[ci][':answer/id'];rng.shuffle(choices)
 field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices}
 if not missing:field[':answer-field/correct']=[':answer/id',correctid]
 q={':question/id':qid,':question/problem':prompt,':question/answer-fields':[field]}
 if sol is not None:q[':question/worked-solution']=sol
 if not missing:q[':question/difficulty']=':question.difficulty/'+level
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'template':actual_template,'bank_profile':profile,'parameters':p,'seed':seed,'level':level,'source':{k:SOURCE[k] for k in ('database','basis','lineage')},'raw_replay':raw,'evidence_only':missing or opaque,'eligible_for_learning':not(missing or opaque),'interpretation_unresolved':opaque,'mathematical_fingerprint':fp,'content_fingerprint':identity,'plot_coefficients':{image:str(v) for image,v in zip(bank,vs)},'mark_x':2 if level=='hard' else 1,'correct_plot':bank[ci],'python':sys.version.split()[0],'sympy':sp.__version__,'matplotlib':matplotlib.__version__}}

# EASY: negative integer stretch or unit-numerator contraction; direct x=1 marks.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE: reduced nonunit numerator/denominator (2 through 5), direct x=1 marks.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# HARD (authored): same negative rational stretch with d=6..12 and x=±2 marks.
# Mapping base ordinates ±1/2 demands one nonunit coordinate-scale comparison.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)

def markdown(r):
 q=r['question'];f=q[':question/answer-fields'][0];correct=f.get(':answer-field/correct',[None,None])[1]
 lines=[q[':question/problem'],'']
 for i,a in enumerate(f[':answer-field/choices']):lines+=['**'+chr(65+i)+'**'+(' (correct)' if a[':answer/id']==correct else ''),'![]('+a[':answer/value']+')','']
 if correct is None:lines+=['Raw evidence: source correct designation absent.','']
 if ':question/worked-solution' in q:lines+=[q[':question/worked-solution']]
 return '\n'.join(lines)

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
 if args.count<1:ap.error('Count must be positive')
 levels=['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]
 try:rows=[generate(l,args.seed+i,args.template,profile=args.profile) for l in levels for i in range(args.count)]
 except ValueError as e:ap.error(str(e))
 print(json.dumps(rows,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in rows))
if __name__=='__main__':main()
