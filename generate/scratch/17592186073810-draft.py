#!/usr/bin/env python3
"""Axis distance only. Raw profiles are opaque historical evidence; normal banks
are complete method-derived recipes. No database access or registration."""
import argparse, hashlib, json, os, random, re, sys, uuid
from pathlib import Path
import sympy as sp
KP_ID=17592186073810
KP_UUID='522b66f4-8a46-5dd0-a9d7-3b081c0ed157'
TITLE='Finding the Distance Between a Point and a Horizontal or Vertical Line'
VERSION='axis-distance-draft-v3'
PACKAGE=Path(__file__).with_suffix('');ROOT=PACKAGE.parents[2]
sys.path.insert(0,str(ROOT/'scripts/question_capture'))
from math_format import normalize_tex,normalize_prose,validate_generated_record
SOURCE=json.loads((PACKAGE/'source.json').read_text())
SOURCES={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
PROFILES=('coordinate-errors','origin-errors')
TEMPLATES=tuple(SOURCES)

def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def ident(x):return str(uuid.uuid5(uuid.UUID(KP_UUID),digest(x)))
def tex(x):return normalize_tex(sp.latex(sp.Rational(x)))
def geometry(q):
 p=re.search(r'point \$\(([-\d]+),\s*([-\d]+)\)\$',q[':question/problem']);l=re.search(r'line \$([xy])\s*=\s*([-\d]+)',q[':question/problem']);return l[1],sp.Rational(p[1]),sp.Rational(p[2]),sp.Rational(l[2])
def fingerprint(axis,x,y,c):return digest(['axis-distance',axis,str(x if axis=='x' else y),str(c)])
def bank(axis,x,y,c,profile):
 t,o=(x,y) if axis=='x' else (y,x);d=abs(t-c)
 if profile=='coordinate-errors':return [d,abs(o-c),abs(t+c),abs(t),abs(c)]
 if profile=='origin-errors':return [d,abs(o-c),abs(t+c),abs(o),abs(c)]
 raise ValueError('Unknown complete bank profile')
def valid_level(level,x,y,c,axis):
 t=x if axis=='x' else y
 if any(abs(z)>8 for z in (x,y,c)) or not 1<=abs(t-c)<=12:return False
 if level=='easy':return all(z.q==1 for z in (x,y,c))
 if level=='moderate':return t.q==c.q==2 and y.q<=2 and x.q<=2
 if level=='hard':return t.q!=c.q and t.q in (2,3,4) and c.q in (2,3,4) and x.q<=4 and y.q<=4
 return False

def sample(level,rng,axis,profile):
 for _ in range(20000):
  if level=='easy':x,y,c=[sp.Rational(rng.randint(-8,8)) for _ in range(3)]
  elif level=='moderate':x,y,c=[sp.Rational(rng.randrange(-15,16,2),2) for _ in range(3)]
  else:x,y,c=[sp.Rational(rng.randint(-20,20),rng.choice((2,3,4))) for _ in range(3)]
  vs=bank(axis,x,y,c,profile)
  if valid_level(level,x,y,c,axis) and len(set(vs))==5 and all(v>0 for v in vs):return axis,x,y,c
 raise RuntimeError('Complete bank sampler exhausted')

def render_plots(z):
 os.environ.setdefault('MPLCONFIGDIR',str(PACKAGE/'matplotlib-cache'))
 import matplotlib;matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 from matplotlib.ticker import MaxNLocator
 axis,x,y,c=z;fx,fy=(c,y) if axis=='x' else (x,c);d=abs((x if axis=='x' else y)-c)
 h=digest([VERSION,list(map(str,z))]);out=PACKAGE/'plots';out.mkdir(exist_ok=True);p=out/(h+'.png')
 if not p.exists():
  fig,ax=plt.subplots(figsize=(5,5),layout='constrained');bounds=[float(min(0,x,fx)-3),float(max(0,x,fx)+3),float(min(0,y,fy)-3),float(max(0,y,fy)+3)]
  span=max(bounds[1]-bounds[0],bounds[3]-bounds[2]);cx=(bounds[0]+bounds[1])/2;cy=(bounds[2]+bounds[3])/2;bounds=[cx-span/2,cx+span/2,cy-span/2,cy+span/2]
  ax.set(xlim=bounds[:2],ylim=bounds[2:],aspect='equal',xlabel='$x$',ylabel='$y$');ax.grid(color='#cccccc',lw=.6);ax.xaxis.set_major_locator(MaxNLocator(7));ax.yaxis.set_major_locator(MaxNLocator(7))
  ax.axhline(0,color='black',lw=1);ax.axvline(0,color='black',lw=1)
  if axis=='x':ax.axvline(float(c),color='#2373b8',lw=1.8)
  else:ax.axhline(float(c),color='#2373b8',lw=1.8)
  ax.plot([float(x),float(fx)],[float(y),float(fy)],'k--',lw=1.3);ax.plot(float(x),float(y),'o',color='red',ms=6);ax.plot(float(fx),float(fy),'o',color='#2373b8',ms=5)
  ax.annotate('$('+tex(x)+','+tex(y)+')$',(float(x),float(y)),xytext=(-10,0) if axis=='y' else ((-7,-20) if float(x)>(bounds[0]+bounds[1])/2 else (7,-20)),ha='right' if axis=='y' or float(x)>(bounds[0]+bounds[1])/2 else 'left',textcoords='offset points',fontsize=11,bbox=dict(facecolor='white',edgecolor='none',alpha=.95))
  ax.annotate('$'+tex(d)+'$ units',(float((x+fx)/2),float((y+fy)/2)),xytext=(8,12) if axis=='x' else (12,0),textcoords='offset points',fontsize=11,bbox=dict(facecolor='white',edgecolor='none',alpha=.95))
  ax.set_title('$'+axis+'='+tex(c)+'$',fontsize=12);fig.canvas.draw()
  display=ax.transData.transform([[float(x),float(y)],[float(fx),float(fy)]]);pixels=float(sum((display[0]-display[1])**2)**.5)
  if pixels<12:plt.close(fig);raise ValueError('Shortest segment unreadable at native pixels')
  fig.savefig(p,dpi=120);plt.close(fig)
  p.with_suffix('.json').write_text(json.dumps(dict(parameters=list(map(str,z)),foot=list(map(str,(fx,fy))),distance=str(d),bounds=bounds,segment_pixels_at_100dpi=pixels,renderer='Matplotlib',matplotlib=matplotlib.__version__),indent=2)+'\n')
 return {'path':str(p.resolve()),'local_path':str(p.resolve()),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'role':'worked-solution','renderer':'Matplotlib','matplotlib':matplotlib.__version__}

def prompt(old,z):
 axis,x,y,c=z
 # Preserve every source spelling/space/punctuation, changing only defined slots.
 text=old[':question/problem'];text=re.sub(r'\$\([-\d]+,\s*[-\d]+\)\$',lambda m:'$('+tex(x)+(','+' ' if ', ' in m[0] else ',')+tex(y)+')$',text)
 text=re.sub(r'line \$[xy](\s*)=(\s*)[-\d]+',lambda m:'line $'+axis+m[1]+'='+m[2]+tex(c),text);return text

def solution(old,z,asset):
 axis,x,y,c=z;t=x if axis=='x' else y;d=abs(t-c)
 base=old if ':question/worked-solution' in old else SOURCES['q-114323']
 text=base[':question/worked-solution'];oa,ox,oy,oc=geometry(base)
 text=re.sub(r'!\[\]\((.*?)\)',lambda m:'![]('+asset['path']+')',text)
 text=text.replace('$('+str(ox)+','+str(oy)+')$','$('+tex(x)+','+tex(y)+')$')
 text=text.replace('$'+oa+'='+str(oc)+'$','$'+axis+'='+tex(c)+'$').replace('$'+oa+'$-coordinate','$'+axis+'$-coordinate').replace('$'+str(oc)+'.$','$'+tex(c)+'.$')
 text=text.replace('horizontal line','__ORIENTATION__ line').replace('vertical line','__ORIENTATION__ line').replace('__ORIENTATION__','vertical' if axis=='x' else 'horizontal')
 term='('+tex(c)+')' if c<0 else tex(c)
 text=re.sub(r'\$\$.*?\$\$',lambda m:'$$\nd=|'+tex(t)+'-'+term+'|='+tex(d)+'.\n$$',text,flags=re.S)
 return text

def generate(level='easy',seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('Unknown difficulty')
 if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Only source radio field supported')
 rng=random.Random(seed);sid=template or rng.choice(TEMPLATES)
 if sid not in SOURCES:raise ValueError('Unknown template')
 old=SOURCES[sid];raw=bool(profile and profile.startswith('raw:'))
 if raw:
  if profile!='raw:'+sid:raise ValueError('Raw profile belongs to its source template')
  if parameters is None:parameters={'dilation':rng.randint(1,3)}
  if set(parameters)!={'dilation'} or type(parameters['dilation']) is not int or not 1<=parameters['dilation']<=3:raise ValueError('Raw dilation is an integer 1..3')
  k=parameters['dilation'];a,x,y,c=geometry(old);z=(a,k*x,k*y,k*c);vals=[k*sp.Rational(v[':answer/value']) for v in old[':question/answer-fields'][0][':answer-field/choices']]
 else:
  profile=profile or rng.choice(PROFILES)
  if profile not in PROFILES:raise ValueError('Unknown normal profile')
  axis=geometry(old)[0] if parameters is None else parameters.get('axis')
  if parameters is None:z=sample(level,rng,axis,profile);parameters=dict(zip(('axis','x','y','c'),map(str,z)))
  else:
   if set(parameters)!={'axis','x','y','c'} or axis not in ('x','y'):raise ValueError('Exact axis/x/y/c parameters required')
   try:z=(axis,*(sp.Rational(parameters[k]) for k in ('x','y','c')))
   except Exception as e:raise ValueError('Exact rational coordinates required') from e
  a,x,y,c=z
  if not valid_level(level,x,y,c,a):raise ValueError('Outside the declared level scope')
  vals=bank(a,x,y,c,profile)
  if len(set(vals))!=5 or any(v<=0 for v in vals):raise ValueError('Whole bank is ambiguous or nonpositive')
 a,x,y,c=z;d=abs((x if a=='x' else y)-c);assets=[]
 if raw and k==1:
  problem=prompt(old,z)  # Still parameterized; source whitespace survives.
  if ':question/worked-solution' in old:
   worked=solution(old,z,{'path':re.search(r'!\[\]\((.*?)\)',old[':question/worked-solution'])[1]})
   ref=re.search(r'!\[\]\((.*?)\)',worked)[1];p=Path('/media/jake/SSD/EDB/math')/ref;assets=[dict(path=ref,local_path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),role='worked-solution',unchanged_source_asset=True)]
 else:
  problem=prompt(old,z)
  if not raw or ':question/worked-solution' in old:
   asset=render_plots(z);assets=[asset];worked=solution(old,z,asset)
 has_solution=not raw or ':question/worked-solution' in old
 has_grade=not raw or ':question/difficulty' in old
 has_key=not raw or ':answer-field/correct' in old[':question/answer-fields'][0]
 if not raw:
  problem=normalize_prose(problem);worked=normalize_prose(worked)
 actual_grade=(old[':question/difficulty'][':db/ident'] if raw else ':question.difficulty/'+level) if has_grade else None
 identity=[VERSION,actual_grade,problem,worked if has_solution else None,sorted(map(tex,vals)),tex(d) if has_key else None,'selection',':answer-field.type/radio']
 qid=ident(identity);fid=ident([qid,'selection']);choices=[{':answer/id':ident([fid,tex(v)]),':answer/type':':answer.type/math',':answer/value':tex(v)} for v in vals];rng.shuffle(choices)
 field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices}
 if has_key:field[':answer-field/correct']=[':answer/id',next(v[':answer/id'] for v in choices if v[':answer/value']==tex(d))]
 q={':question/id':qid,':question/problem':problem,':question/answer-fields':[field]}
 if has_solution:q[':question/worked-solution']=worked
 if has_grade:q[':question/difficulty']=actual_grade
 record={'knowledge_point':dict(db_id=KP_ID,id=KP_UUID,title=TITLE),'question':q,'generation':dict(version=VERSION,seed=seed,template=sid,profile=profile,parameters=parameters,source_ids=[sid],basis=2275,evidence_only=raw,eligible_for_learning=not raw,mathematical_fingerprint=fingerprint(*z),content_fingerprint=digest(identity),assets=assets,python=sys.version.split()[0],sympy=sp.__version__,domain='Axis-parallel line; exact bounded rational coordinates; positive distance',grade_origin='captured or omitted' if raw else 'authored design; moderate/hard uncertain')}
 if not raw:validate_generated_record(record)
 return record

def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)
def generate_hard(seed=0,**kw):return generate('hard',seed,**kw)
def markdown(r):
 q=r['question'];return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$' for a in q[':question/answer-fields'][0][':answer-field/choices'])+'\n\n'+q.get(':question/worked-solution','')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');p.add_argument('--seed',type=int,default=0);p.add_argument('--count',type=int,default=1);p.add_argument('--format',choices=['markdown','json'],default='json');p.add_argument('--template');p.add_argument('--profile');a=p.parse_args();levels=['easy','moderate','hard'] if a.difficulty=='all' else [a.difficulty];rs=[generate(l,a.seed+i,template=a.template,profile=a.profile) for l in levels for i in range(a.count)];print(json.dumps(rs,indent=2) if a.format=='json' else '\n\n---\n\n'.join(map(markdown,rs)))
