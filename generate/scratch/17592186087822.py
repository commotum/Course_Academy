#!/usr/bin/env python3
"""Identify c from the graph of y=b^x+c; draft, basis 1356, no database writes.

API generate(level, seed=0, template=None, field_type=None, parameters=None,
profile=None), plus three documented level entrypoints below. Source profiles
source:q-N expose exact historical banks/attribute omissions as evidence-only.
Defaults use complete method-derived banks, source-shaped radio equations and
one fixed two-paragraph worked solution. Hard is explicitly authored: read a
signed fractional asymptote from calibrated ticks, without changing the method.
Mathematical-task fingerprints exclude base (incidental to reading c) for labeled
plots, but retain c and hard tick increment. Content IDs retain all displayed data.
"""
from __future__ import annotations
import argparse, hashlib, json, os, random, subprocess, sys, tempfile, uuid
from pathlib import Path
import sympy as sp
KP=17592186087822
HERE=Path(__file__).resolve().with_suffix('')
VERSION='shift-asymptote-1.2'
TITLE='Identifying the Shift Applied to an Exponential Growth Curve'
SNAPSHOT=json.loads((HERE/'source.json').read_text())
KP_UUID=SNAPSHOT['record'][':knowledge-point/id']
SOURCES={q[':question/math-academy-id']:q for q in SNAPSHOT['record'][':knowledge-point/questions']}
# Every bank is specified as a WHOLE ordered list. Shift operations are affine
# in c; multiplication mistakes multiply b^x; base_plus changes the given base.
# Historical fractional offsets have unresolved error intent, never defaults.
SOURCE_SPECS={
'q-26807':('easy','17','-4','spaced',[('shift',1,0),('shift',1,1),('shift',-1,1),('shift',-1,-1),('shift',-1,0)]),
'q-7228':('easy','2','1','spaced',[('shift',1,1),('shift',1,0),('mul',1,2),('shift',0,0),('mul',1,1)]),
'q-170593':('moderate','13/6','-3/2','fraction_raw',[('shift',1,'5/6'),('shift',1,1),('shift',1,'11/6'),('shift',1,0),('shift',1,'7/3')]),
'q-26804':('easy','25','10','compact',[('shift',-1,0),('shift',-1,-1),('shift',1,1),('shift',1,0),('shift',1,5)]),
'q-99774':('easy','7','-5','compact',[('shift',-1,0),('mul',1,0),('shift',0,0),('mul',-1,0),('shift',1,0)]),
'q-99775':('easy','12','-3','compact',[('mul',1,0),('shift',-1,0),('shift',1,0),('mul',-1,0),('shift',0,0)]),
'q-7230':('easy','3','-2','compact',[('mul',1,-1),('shift',1,1),('shift',1,-1),('shift',1,0),('mul',1,0)]),
'q-7232':('easy','2','-3','compact',[('shift',1,1),('mul',1,0),('shift',1,0),('base_plus',1,-1),('mul',-1,0)]),
}
DEFAULT_BANKS={
'signed_intercept':[('shift',1,0),('shift',1,1),('shift',-1,1),('shift',-1,-1),('shift',-1,0)],
# Ignoring vertical translation / reflecting its sign / treating c as multiplier.
'confuse_shift_stretch':[('shift',1,0),('shift',-1,0),('shift',0,0),('mul',1,0),('mul',-1,0)],
# y-intercept is c+1: use it directly, subtract instead of add, or stretch.
'intercept_offset':[('shift',1,0),('shift',1,1),('shift',1,-1),('mul',1,0),('mul',1,-1)],
# Reading an adjacent tick / reversing the sign, rather than the dashed level.
'axis_reading':[('shift',1,0),('step',1,1),('step',1,-1),('shift',-1,0),('shift',0,0)],
}
X=sp.Symbol('x',real=True)
def digest(obj):return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(value):return str(uuid.uuid5(uuid.NAMESPACE_URL,'kp87822:'+value))
def rational(v):
 try:r=sp.Rational(str(v))
 except Exception as e:raise ValueError('Exact rational parameters required') from e
 return r
def tex(v):return sp.latex(rational(v)).replace('- ','-')
def base_tex(b,style):
 if style=='fraction_raw':return '{('+tex(b)+')}^{x}'
 if style=='spaced':return str(b)+'^{x}'
 return '{'+tex(b)+'}^{x}' if b.q==1 else '{('+tex(b)+')}^{x}'
def equation(b,c,style='compact',kind='shift'):
 pre='y = ' if style=='spaced' else 'y='
 bt=base_tex(b,style)
 if kind=='mul':return pre+tex(c)+('('+bt+')')
 if c==0:return pre+bt
 sign=' + ' if c>0 and style=='spaced' else ' - ' if c<0 and style=='spaced' else '+' if c>0 else '-'
 t=tex(abs(c)); t=t
 return pre+bt+sign+t

def options(b,c,step,recipes,style):
 result=[]; objects=[]
 for kind,a,d in recipes:
  v=rational(a)*c+rational(d)*(step if kind=='step' else 1)
  bb=b+1 if kind=='base_plus' else b
  rendered=equation(bb,v,style,'mul' if kind=='mul' else 'shift')
  expression=v*bb**X if kind=='mul' else bb**X+v
  result.append(rendered);objects.append(expression)
 for i,e in enumerate(objects):
  if any(sp.simplify(e-f)==0 for f in objects[:i]):raise ValueError('Whole bank rejected: equivalent options')
 return result,objects

def domain(level,p,raw=False):
 if set(p)-{'b','c','step'}:raise ValueError('Unknown parameter')
 b,c=rational(p['b']),rational(p['c']);step=rational(p.get('step','1/2' if level=='hard' else '1'))
 if not (1<b<=25) or b.q>6 or abs(c)>12 or c==0:raise ValueError('Outside shared scope')
 if level!='hard' and step!=1:raise ValueError('Labelled plots have no variable calibration step')
 if level=='easy' and (b.q!=1 or c.q!=1):raise ValueError('Easy requires integer base and shift')
 if level=='moderate' and (c.q==1 or c.q>6):raise ValueError('Moderate requires noninteger fractional shift')
 if level=='hard' and (c.q==1 or step not in (sp.Rational(1,2),sp.Rational(1,3),sp.Rational(1,4)) or abs(c/step)>8 or (c/step).q!=1):raise ValueError('Hard requires signed fractional tick reading, <=8 steps')
 return b,c,step

def plot_data(b,c,level):
 # Exact curve values and axis bounds. Hard uses one tick per grid interval;
 # only alternate ticks labeled so the dashed level itself is not named.
 step=sp.Rational(1,2)
 lo=min(sp.Integer(-2),c-2);hi=max(sp.Integer(3),c+4)
 return {'b':str(b),'c':str(c),'level':level,'xmin':-4,'xmax':str(max(1.5,float(sp.log(hi-c,b)))), 'ymin':str(lo),'ymax':str(hi)}

def render_plots(b,c,level,step,output_dir=None):
 data=plot_data(b,c,level);data.update(step=str(step),version=VERSION)
 key=digest(data);folder=Path(output_dir) if output_dir else HERE/'plots'/VERSION;folder.mkdir(parents=True,exist_ok=True)
 png=folder/(key+'.png');side=folder/(key+'.json')
 if not (png.exists() and side.exists()):
  fd,name=tempfile.mkstemp(prefix='input-',suffix='.json',dir=folder)
  try:
   with os.fdopen(fd,'w') as f:json.dump(dict(data,output=str(png)),f)
   subprocess.run([sys.executable,str(HERE/'render.py'),name],check=True,capture_output=True)
  finally:Path(name).unlink(missing_ok=True)
 return png,json.loads(side.read_text())

def source_text(sid,b,c):
 q=SOURCES[sid];spec=SOURCE_SPECS[sid];ob,oc=rational(spec[1]),rational(spec[2])
 # Complete base components, not single-letter/short-digit global replacements.
 oldbase=base_tex(ob,'compact');newbase=base_tex(b,'compact')
 if sid=='q-26807' or sid=='q-7228':oldbase=base_tex(ob,'spaced');newbase=base_tex(b,'spaced')
 if sid=='q-170593':oldbase='{('+tex(ob)+')}^{x}';newbase='{('+tex(b)+')}^{x}'
 problem=q[':question/problem'].replace(oldbase,newbase)
 solution=q.get(':question/worked-solution')
 if solution is not None:
  solution=solution.replace(oldbase,newbase).replace('y='+tex(oc)+'.$','y='+tex(c)+'.$').replace('c='+tex(oc)+'.$','c='+tex(c)+'.$')
 return problem,solution

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('Unknown difficulty')
 if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Only source radio fields supported')
 rng=random.Random(seed);raw=bool(profile and profile.startswith('source:'));sid=profile.split(':',1)[1] if raw else None
 if raw:
  if sid not in SOURCE_SPECS:raise ValueError('Unknown source profile')
  spec=SOURCE_SPECS[sid]
  if spec[0]!=level:raise ValueError('Source profile has different supported level')
  recipes=spec[4];style=spec[3];profile=profile
  if parameters is None:parameters={'b':spec[1],'c':spec[2]}
 else:
  style='compact'
  eligible=list(DEFAULT_BANKS) if level=='hard' else ['signed_intercept','confuse_shift_stretch','intercept_offset']
  profile=profile or rng.choice(eligible) # complete bank BEFORE parameters
  if profile not in eligible:raise ValueError('Axis-reading bank requires calibrated hard graph')
  if profile not in DEFAULT_BANKS:raise ValueError('Unknown bank profile')
  recipes=DEFAULT_BANKS[profile]
 expected={'easy':'labelled_integer','moderate':'labelled_fraction','hard':'read_fraction_grid'}[level]
 if template not in (None,expected,'source' if raw else expected):raise ValueError('Template incompatible with level')
 template='source' if raw else expected
 for attempt in range(500):
  p=parameters
  if p is None:
   if level=='easy':p={'b':rng.randint(2,25),'c':rng.choice([i for i in range(-12,13) if i])}
   elif level=='moderate':p={'b':str(rng.choice(sorted({sp.Rational(n,d) for d in range(1,7) for n in range(d+1,26*d) if sp.Rational(n,d)<=25},key=float))),'c':str(rng.choice(sorted({sp.Rational(n,d) for d in range(2,7) for n in range(-12*d,12*d+1) if n and sp.Rational(n,d).q>1},key=float)))}
   else:
    step=rng.choice(['1/2','1/3','1/4']);p={'b':rng.randint(2,12),'c':str(rational(step)*rng.choice([i for i in range(-8,9) if i and (rational(step)*i).q>1])),'step':step}
  try:
   b,c,step=domain(level,p,raw);values,objects=options(b,c,step,recipes,style)
   if sum(sp.simplify(o-(b**X+c))==0 for o in objects)!=1:raise ValueError('Missing/ambiguous correct option')
   break
  except ValueError:
   if parameters is not None:raise
 else:raise RuntimeError('No valid whole bank')
 asset=None
 if raw:
  problem,solution=source_text(sid,b,c)
  spec=SOURCE_SPECS[sid]
  original=(b==rational(spec[1]) and c==rational(spec[2]))
  if not original:
   png,asset=render_plots(b,c,level,step)
   import re
   problem=re.sub(r'!\[\]\(.*?\)','![]('+str(png)+')',problem)
 else:
  png,asset=render_plots(b,c,level,step)
  bt=base_tex(b,'compact')
  problem='![]('+str(png)+')\n\nThe graph above shows the curve $y='+bt+'+c.$ Determine the value of $c$ and find the equation of the curve.'
  solution='The horizontal asymptote of $y='+bt+'$ is $y=0.$ The vertical translation $y='+bt+'+c$ shifts the asymptote to $y=c.$\n\nIn the graph above, the horizontal asymptote is $y='+tex(c)+'.$ Therefore, $c='+tex(c)+'.$'
 # Key-presence parity is preserved on raw source replay, including absent correct.
 present_correct=not raw or ':answer-field/correct' in SOURCES[sid][':question/answer-fields'][0]
 q={':question/problem':problem}
 if not raw or ':question/difficulty' in SOURCES[sid]:q[':question/difficulty']=':question.difficulty/'+level
 if solution is not None:q[':question/worked-solution']=solution
 fingerprint=digest({'c':str(c),'reading':'label' if level!='hard' else 'grid','step':str(step) if level=='hard' else None})
 content=digest({'version':VERSION,'level':q.get(':question/difficulty'),'prompt':problem,'solution':solution,'bank':sorted(values),'correct_present':present_correct})
 qid=uid(content);fid=uid(qid+':selection');answers=[{':answer/id':uid(fid+':'+v),':answer/type':':answer.type/math',':answer/value':v} for v in values]
 correct_index=next(i for i,o in enumerate(objects) if sp.simplify(o-(b**X+c))==0)
 correct_id=answers[correct_index][':answer/id'];rng.shuffle(answers)
 f={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers}
 if present_correct:f[':answer-field/correct']=[':answer/id',correct_id]
 q.update({':question/id':qid,':question/answer-fields':[f]})
 return {'knowledge_point':{'db_id':KP,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'template':template,'bank_profile':profile,'parameters':{'b':str(b),'c':str(c),'step':str(step)},'mathematical_fingerprint':fingerprint,'content_fingerprint':content,'source':{k:v for k,v in SNAPSHOT.items() if k!='record'},'source_id':sid,'evidence_only':raw,'eligible_for_learning':not raw,'inferred_correct_value':equation(b,c,'compact'),'recipes':recipes,'plot':asset,'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__},'authored_level':level=='hard' or raw and ':question/difficulty' not in SOURCES[sid]}}

# EASY: observed integer asymptote label. One direct c read; integer bases 2..25,
# nonzero integer shifts -12..12. Sign varies with unchanged source workload.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE: observed signed fractional asymptote label. Same one read, fraction
# denominators 2..6, base >1 <=25 denominator <=6; no root/logarithm solving.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# HARD: authored SAME shift-reading skill, calibrated fractional grid (1/2,1/3,
# 1/4); alternate ticks labeled. Noninteger c within eight steps; infer one
# unlabelled tick level, identify c, select equation. Never identify a stretch.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)

def markdown(r):
 q=r['question'];g=r['generation'];s='\n\n**'+('SOURCE EVIDENCE '+g['source_id'] if g['evidence_only'] else 'GENERATED')+'; actual difficulty: '+q.get(':question/difficulty','unrated (raw capture)')+('; authored level' if g['authored_level'] else '')+'**\n\n'+q[':question/problem']+'\n\n'
 f=q[':question/answer-fields'][0]
 for a in f[':answer-field/choices']:s+='- $'+a[':answer/value']+'$'+(' (correct)' if a[':answer/id']==f.get(':answer-field/correct',[None,None])[1] else '')+'\n'
 return s+'\n'+q.get(':question/worked-solution','[Original worked solution absent.]')+'\n'
if __name__=='__main__':
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');a=ap.parse_args()
 if a.count<1:ap.error('count must be positive')
 levels=['easy','moderate','hard'] if a.difficulty=='all' else [a.difficulty]
 records=[generate(l,a.seed+i,a.template,profile=a.profile) for l in levels for i in range(a.count)]
 print(json.dumps(records,indent=2) if a.format=='json' else ''.join(markdown(r) for r in records))
