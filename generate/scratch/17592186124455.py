#!/usr/bin/env python3
"""Implicit-curve tangent vectors; immutable math basis 1356, local review only.

Observed profiles replay all 11 sources, including raw attribute omissions and legacy
fields. These opaque historical banks are evidence only, even after completions.
Authored easy/moderate/hard templates use the same f_y i-f_x j method; no lines,
normal-vector questions, unit vectors, parameterizations or additional branches.
Parameters affect the implicit curve and both displayed partial derivatives.
Source templates vary point coordinates and the level constant, retaining the full
shared prose and ordered solution masks. Original banks preserve their spelling;
opaque components are explicitly fixed observed components, not inferred errors.
"""
from __future__ import annotations
import argparse, copy, hashlib, json, platform, random, re, uuid
from pathlib import Path
import sympy as s
ROOT=Path(__file__).with_suffix('')
KP_ID=17592186124455
KP_UUID='348fa49f-2af8-5562-91f6-3f70bb93ea90'
TITLE='Finding a Tangent Vector to a Plane Curve'
VERSION='tangent-vector-1'
x,y=s.symbols('x y',real=True)
i,j=s.symbols('i j',real=True)
SNAP=json.loads((ROOT/'source.json').read_text())
QUESTIONS={q[':question/math-academy-id']:q for q in SNAP['record'][':knowledge-point/questions']}
# Each source is its own observed Markdown/value template. All fields are radio.
SOURCE_SPEC={
'q-36391':('x**2*y-x*y',2,2),
'q-65204':('cos(x)*cos(y)-sin(x*y)',0,'pi/2'),
'q-130198':('x*cos(y)+y*sin(x)','pi/2',0),
'q-130200':('x*exp(y**2+1)+y',1,0),
'q-37516':('2*x*log(y)-8*x*y',1,'E'),
'q-72400':('x**2+y**2-2*x*y',-1,2),
'q-72463':('2*x**3*y**2-4*x*y+3*x',1,1),
'q-130201':('x*y+x**2+y**3',-1,-1),
'q-72388':('x**2*y-x',1,2),
'q-130192':('x**2*y-y**2',2,1),
'q-130194':('x*log(y)-x**2',-1,1),
}
def sym(z):return s.sympify(z,locals={'x':x,'y':y,'E':s.E})
def tex(z):return s.latex(sym(z)).replace(r'\log',r'\ln')
def digest(z):return hashlib.sha256(json.dumps(z,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def uid(z):return str(uuid.uuid5(uuid.NAMESPACE_URL,VERSION+':'+z))
def expr(q):return sym(SOURCE_SPEC[q][0])
def vector(a,b):
 a,b=s.simplify(a),s.simplify(b)
 out=''
 for c,l in [(a,'i'),(b,'j')]:
  if c==0:continue
  neg=c.could_extract_minus_sign(); v=-c if neg else c
  term=l if v==1 else (r'\left('+tex(v)+r'\right)' if v.is_Add else tex(v))+r'\, '+l
  out+=('-' if neg else ('+' if out else ''))+term
 return out or '0'
def parse(z):
 """Parse displayed scalar/vector/equation TeX using balanced fraction groups."""
 from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,convert_xor
 z=z.replace('\\\\','\\').replace('⁡','').replace('π',r'\pi').replace('−','-')
 for name in ('cos','sin','ln'):z=z.replace('\\operatorname{'+name+'}',' '+name+' ')
 z=z.replace(r'\text{ }',' ').replace(r'\,',' ').replace(r'\left','').replace(r'\right','').replace(r'\cdot','*').replace(r'\pi','pi')
 for name in ('cos','sin','ln','log','exp'):z=z.replace('\\'+name,' '+name+' ')
 def group(t,at):
  if t[at]!='{':raise ValueError('fraction group required')
  depth=1;end=at+1
  while depth:
   if t[end]=='{':depth+=1
   elif t[end]=='}':depth-=1
   end+=1
  return t[at+1:end-1],end
 while r'\frac' in z:
  at=z.index(r'\frac');a,end=group(z,at+5);b,end2=group(z,end)
  z=z[:at]+'(('+a+')/('+b+'))'+z[end2:]
 z=z.replace('{','(').replace('}',')')
 z=re.sub(r'\b(cos|sin|ln)\s+([xy0-9]+)\b',r'\1(\2)',z)
 z=re.sub(r'(?<![a-zA-Z])e(?![a-zA-Z])','(E)',z)
 z=re.sub(r'(?<=\d)j(?![a-zA-Z])','*jbasis',z)
 z=re.sub(r'(?<![a-zA-Z])j(?![a-zA-Z])','jbasis',z)
 return parse_expr(z,local_dict={'x':x,'y':y,'i':i,'j':j,'jbasis':j,'e':s.E,'E':s.E,'pi':s.pi,'ln':s.log,'log':s.log,'cos':s.cos,'sin':s.sin,'exp':s.exp},transformations=standard_transformations+(implicit_multiplication_application,convert_xor))

def pair(z):
 e=parse(z); ii=next((a for a in e.free_symbols if str(a)=='i'),s.Symbol('i')); jj=next((a for a in e.free_symbols if str(a)=='j'),s.Symbol('j'))
 return (s.simplify(e.coeff(ii)),s.simplify(e.coeff(jj)))
def dot(a,b):return s.simplify(a[0]*b[0]+a[1]*b[1])
def same_direction(a,b):return s.simplify(a[0]*b[1]-a[1]*b[0])==0

def shape(q):
 q=copy.deepcopy(q);q.pop(':db/id',None)
 def cv(v):
  if isinstance(v,dict):
   if set(v)=={':db/ident'}:return v[':db/ident']
   return {k:cv(w) for k,w in v.items() if k!=':db/id'}
  if isinstance(v,list):return [cv(w) for w in v]
  return v
 q=cv(q)
 for f in q.get(':question/answer-fields',[]):
  if ':answer-field/correct' in f:f[':answer-field/correct']=[':answer/id',f[':answer-field/correct'][':answer/id']]
 return q

# Source masks store every raw component, bank and attribute, with complete prose.
# Their point/constant/substitution/final components are parameter slots, never a
# branch returning a source record. Build-source-evidence writes these audited masks.
def source_record(source_id,seed,parameters,profile):
 spec=json.loads((ROOT/'source-templates.json').read_text())[source_id]
 p=parameters or spec['parameters'];p={k:str(v) for k,v in p.items()}
 if set(p)!={'x0','y0'}:raise ValueError('Source parameters require x0 and y0')
 a,b=map(sym,(p['x0'],p['y0']));F=expr(source_id)
 guard_numbers(a,b,source=True)
 if source_id in ('q-65204','q-130198'):
  if (a,b) not in ((0,s.pi/2),(0,-s.pi/2),(s.pi/2,0),(-s.pi/2,0)):raise ValueError('familiar trig axis points required')
 elif source_id=='q-130200':
  if a not in (-2,-1,1,2) or b not in (-1,0,1):raise ValueError('familiar exponential evaluation points required')
 elif source_id in ('q-37516','q-130194'):
  if a not in (-2,-1,1,2) or b not in (1,s.E,s.E**2):raise ValueError('familiar logarithm evaluation points required')
 elif a not in (-2,-1,0,1,2) or b not in (-2,-1,0,1,2):raise ValueError('source polynomial points use integer coordinates of magnitude≤2')
 if F.has(s.log(y)) and b.is_positive is not True:raise ValueError('log domain y>0')
 fx,fy=s.diff(F,x),s.diff(F,y);X,Y=[s.simplify(z.subs({x:a,y:b})) for z in (fx,fy)]
 guard_numbers(X,Y,F.subs({x:a,y:b}),source=True)
 if X==Y==0:raise ValueError('regular point required')
 base_a,base_b=map(sym,(spec['parameters']['x0'],spec['parameters']['y0']))
 at=spec['coordinate_spellings'][0] if a==base_a else tex(a);bt=spec['coordinate_spellings'][1] if b==base_b else tex(b)
 vals={'x0':at,'y0':bt,'point':spec['point_template'].format(x0=at,y0=bt),
       'level':tex(s.simplify(F.subs({x:a,y:b}))),
       'vector':vector(Y,-X),
       'evaluation':spec['evaluation_template'].replace('{x0}',at if a==base_a else '('+at+')').replace('{y0}',bt if b==base_b else '('+bt+')')}
 for key,item in spec['constant_components'].items():
  computed=s.simplify(sym(item['expression']).subs({x:a,y:b}))
  if s.simplify(computed-parse(item['original']))==0:vals[key]=item['original']
  elif item['original'].startswith('-'):
   vals[key]=('+' if computed.is_nonnegative else '-')+tex(abs(computed))
  else:vals[key]=r'\left('+tex(computed)+r'\right)'
 for key,spelling in spec['vector_spellings'].items():
  original=pair(spelling)
  vals[key]=spelling if all(s.simplify(v-w)==0 for v,w in zip((Y,-X),original)) else vector(Y,-X)
 # Full component notation is retained at the source parameters by scalar spelling
 # templates, not whole-question lookup. The same masks render changed coordinates.
 for key,item in spec['spelling'].items():
  value=s.simplify(sym(item['expression']).subs({x:a,y:b}))
  vals[key]=item['template'].format(value=tex(value))
 vals['trigoffset']='' if s.simplify(F.subs({x:a,y:b}))==0 else '+('+vals['level']+')'
 vals['square']='0' if b==0 else tex(b**2)
 def render(t):
  for _ in range(2):t=re.sub(r'@@(\w+)@@',lambda m:vals[m[1]],t)
  return t
 q=shape(QUESTIONS[source_id]);q[':question/problem']=render(spec['prompt'])
 if ':question/worked-solution' in q:q[':question/worked-solution']=render(spec['solution'])
 # Banks contain explicit complete-component expressions; opaque literals remain
 # fixed observed components, not arbitrary fits or default learner distractors.
 for fi,f in enumerate(q.get(':question/answer-fields',[])):
  for ai,ans in enumerate(f[':answer-field/choices']):ans[':answer/value']=render(spec['banks'][fi][ai])
 repaired=profile=='completed:'+source_id
 repairs=[]
 if repaired:
  if source_id=='q-65204':q[':question/answer-fields']=q[':question/answer-fields'][1:];repairs.append('remove duplicate legacy selection field confirmed by original widget')
  if source_id=='q-36391':
   f=q[':question/answer-fields'][0]; valid=[ans for ans in f[':answer-field/choices'] if dot((X,Y),pair(ans[':answer/value']))==0]
   if len(valid)!=1:raise ValueError('cannot infer unique correct source choice')
   f[':answer-field/correct']=[':answer/id',valid[0][':answer/id']]
   q[':question/difficulty']=':question.difficulty/moderate';q[':question/worked-solution']=solution(F,a,b)
   repairs.append('authored moderate rating, inferred correct ref and supported full solution')
  if source_id=='q-72463':q[':question/worked-solution']=q[':question/worked-solution'].replace('f(x,y)=0.$','f(x,y)='+vals['level']+'.$');repairs.append('level constant corrected')
  if source_id=='q-130201':
   rawc=vals['constant_0'];q[':question/problem']=q[':question/problem'].replace('='+rawc+'-', '='+vals['level']+'-');q[':question/worked-solution']=q[':question/worked-solution'].replace('='+rawc, '='+vals['level']).replace('= '+rawc, '= '+vals['level']);repairs.append('point membership: constant 3 corrected to 1 at original point')
  # Presentation repairs are separate from raw string/value fidelity.
  def clean(v):
   if isinstance(v,str):return v.replace('\\\\frac','\\frac').replace('\\\\pi','\\pi').replace('\\\\,','\\,')
   if isinstance(v,list):return [clean(z) for z in v]
   if isinstance(v,dict):return {k:clean(z) for k,z in v.items()}
   return v
  cleaned=clean(q)
  if cleaned!=q:repairs.append('presentation normalization: doubled TeX backslashes in captured answer strings')
  q=cleaned
 for f in q.get(':question/answer-fields',[]):
  for ans in f[':answer-field/choices']:guard_numbers(*pair(ans[':answer/value']),source=True)
 if (a,b)!=(base_a,base_b):
  for fi,f in enumerate(q.get(':question/answer-fields',[])):
   old=f.get(':answer-field/correct',[None,None])[1];new_correct=None
   for ans in f[':answer-field/choices']:
    previous=ans[':answer/id'];ans[':answer/id']=uid(digest([q[':question/problem'],fi,ans[':answer/value']]))
    if previous==old:new_correct=ans[':answer/id']
   if old:f[':answer-field/correct']=[':answer/id',new_correct]
   f[':answer-field/id']=uid(digest([q[':question/problem'],fi]))
  q[':question/id']=uid(digest(q))
 return wrap(q,seed,source_id,p,profile,False,repairs)

def guard_numbers(*values,source=False):
 for z in values:
  z=s.simplify(z)
  if z.is_real is not True or z.is_finite is not True:raise ValueError('finite real arithmetic required')
  for atom in z.atoms(s.Rational):
   if abs(atom.p)>32 or atom.q>4:raise ValueError('reduced arithmetic exceeds supported bounds')
  if abs(float(z.evalf()))>32:raise ValueError('arithmetic magnitude exceeds32')

def solution(F,a,b):
 fx,fy=s.diff(F,x),s.diff(F,y);A,B=[s.simplify(z.subs({x:a,y:b})) for z in (fy,fx)]
 pt=f'({tex(a)},{tex(b)})';ft=tex(F);k=tex(F.subs({x:a,y:b}));sub=lambda z:tex(z).replace('x',r'\left('+tex(a)+r'\right)').replace('y',r'\left('+tex(b)+r'\right)')
 return ('First, if we set $f(x,y)='+ft+',$ our curve can be viewed as the level curve $f(x,y)='+k+'.$\n\n'
 'A tangent vector to the level curve that passes through the point $'+pt+'$ can be computed as follows:\n\n$$\nt'+pt+'=f_y'+pt+'i-f_x'+pt+'j\n$$\n\n'
 'So, we calculate $t(x,y)$ and evaluate it at $'+pt+':$\n\n$$\n'
 r'\begin{aligned}t(x,y)&=\frac{\partial}{\partial y}('+ft+r')\,i-\frac{\partial}{\partial x}('+ft+r')\,j \\ '
 r'&=('+tex(fy)+r')\,i-('+tex(fx)+r')\,j \\ t'+pt+r'&=('+sub(fy)+r')\,i-('+sub(fx)+r')\,j \\ '
 r'&=('+tex(A)+r')\,i-('+tex(B)+r')\,j \\ &='+vector(A,-B)+r'\end{aligned}'+'\n$$\n\nTherefore, our tangent vector is $'+vector(A,-B)+'.$')

def wrap(q,seed,template,p,profile,eligible,repairs=None):
 identity={k:copy.deepcopy(v) for k,v in q.items() if k not in (':question/id',':question/math-academy-id')}
 for f in identity.get(':question/answer-fields',[]):f[':answer-field/choices']=sorted(f[':answer-field/choices'],key=lambda a:a[':answer/value'])
 h=digest(identity)
 if eligible or repairs:q[':question/id']=uid(h)
 dependencies={'python':platform.python_version(),'sympy':s.__version__}
 curve=q[':question/problem'].split('$')[1].rstrip('.');lhs,rhs=curve.split('=');displayed_F=parse(lhs)-parse(rhs)
 point=re.findall(r'\$\((.*?)\)\.?\$',q[':question/problem'])[-1];u,v=map(parse,point.split(','));sub={x:u,y:v}
 gradient=tuple(s.simplify(s.diff(displayed_F,z).subs(sub)) for z in (x,y))
 domain={'variables':{'x':'real','y':'real'},'conditions':['y>0'] if displayed_F.has(s.log(y)) else [],'regular_point_condition':'grad F(x0,y0) != (0,0)','regular_point_verified':gradient!=(0,0),'point_membership_condition':'F(x0,y0)=0 for the displayed lhs-minus-rhs expression','point_membership_verified':s.simplify(displayed_F.subs(sub))==0}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'dependencies':dependencies,'domain':domain,'seed':seed,'template':template,'profile':profile,'parameters':p,'source':{k:SNAP[k] for k in ('database','basis','lineage')},'origin':'authored' if eligible else 'observed evidence replay','evidence_only':not eligible,'eligible_for_learning':eligible,'repairs':repairs or [],'content_fingerprint':h}}

# EASY: canonical quadratic workload: first partial derivatives and one point.
# MODERATE: observed mixed polynomial product/power workload, both nonzero inputs.
# HARD: authored extension of q37516, same partial-derivative method, evaluated log
# and reciprocal terms at y=e or e² and signed nonzero x. No new method/branch.
TEMPLATES={'quadratic':'easy','mixed-polynomial':'moderate','log-product':'hard'}
def build(level,p):
 a,b,c,u,v=[sym(p[k]) for k in ('a','b','c','x0','y0')]
 guard_numbers(a,b,c,u,v)
 if any(z.is_Integer is not True or z==0 or abs(z)>4 for z in (a,b,c)):raise ValueError('nonzero integer coefficients of magnitude1..4')
 if s.igcd(s.igcd(int(a),int(b)),int(c))!=1:raise ValueError('primitive coefficients required')
 if u not in (-2,-1,1,2):raise ValueError('x0 must be±1 or±2')
 if level=='easy':
  if v not in (-2,-1,1,2):raise ValueError('easy y0 must be±1 or±2')
  F=a*x**2+b*x*y+c*y
 elif level=='moderate':
  if v not in (-2,-1,1,2):raise ValueError('moderate y0 must be±1 or±2')
  F=a*x**2*y+b*y**2+c*x*y
 elif level=='hard':
  if v not in (s.E,s.E**2):raise ValueError('hard y0 must be e or e²')
  F=a*x*s.log(y)+b*x*y+c*x**2
 else:raise ValueError(level)
 fx,fy=s.diff(F,x),s.diff(F,y);A,B=[s.simplify(z.subs({x:u,y:v})) for z in (fx,fy)]
 guard_numbers(A,B,F.subs({x:u,y:v}))
 if A==0 or B==0:raise ValueError('both partials must be nonzero')
 # Fixed complete five-operation bank, selected before parameter sampling.
 # correct; gradient; omit rotation minus; reverse derivative roles with same minus;
 # omit the family-defining a term before differentiating.
 first=a*x**2 if level=='easy' else a*x**2*y if level=='moderate' else a*x*s.log(y)
 G=F-first;C,D=[s.simplify(z.subs({x:u,y:v})) for z in (s.diff(G,x),s.diff(G,y))]
 bank=[(B,-A),(A,B),(B,A),(-A,B),(D,-C)]
 for pair_values in bank:guard_numbers(*pair_values)
 if any(z==(0,0) for z in bank):raise ValueError('zero vector bank')
 if any(same_direction(bank[ii],bank[jj]) for ii in range(5) for jj in range(ii)):raise ValueError('whole bank direction collision')
 if any(dot((A,B),z)==0 for z in bank[1:]):raise ValueError('ambiguous tangent bank')
 return F,u,v,bank

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if profile and (profile.startswith('raw:') or profile.startswith('completed:')):
  source_id=profile.split(':',1)[1]
  if level!='moderate':raise ValueError('observed sources are moderate or unrated; use moderate for evidence replay')
  if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('source field type is radio')
  if template not in (None,source_id):raise ValueError('source/profile mismatch')
  return source_record(source_id,seed,parameters,profile)
 template=template or next(t for t,l in TEMPLATES.items() if l==level)
 if TEMPLATES.get(template)!=level:raise ValueError('difficulty/template mismatch')
 if profile not in (None,'method-bank'):raise ValueError('unknown profile')
 if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('observed layout is radio')
 rng=random.Random(seed)
 for attempt in range(2000):
  p=parameters or dict(zip(('a','b','c','x0','y0'),[rng.choice([-4,-3,-2,-1,1,2,3,4]) for _ in range(3)]+[rng.choice([-2,-1,1,2]),rng.choice(['E','E**2'] if level=='hard' else [-2,-1,1,2])]))
  if set(p)!={'a','b','c','x0','y0'}:raise ValueError('invalid parameter keys')
  try:F,u,v,bank=build(level,p)
  except ValueError:
   if parameters is not None:raise
   continue
  break
 else:raise RuntimeError('no eligible whole bank found')
 pt=f'({tex(u)},{tex(v)})'
 prompt='Consider the plane curve $'+tex(F)+'='+tex(F.subs({x:u,y:v}))+'.$ Find a tangent vector to that curve at the point $'+pt+'.$'
 ans=[{':answer/id':uid(digest([prompt,'selection',vector(*z)])),':answer/type':':answer.type/math',':answer/value':vector(*z)} for z in bank]
 correct=ans[0][':answer/id'];rng.shuffle(ans)
 q={':question/problem':prompt,':question/worked-solution':solution(F,u,v),':question/difficulty':':question.difficulty/'+level,':question/answer-fields':[{':answer-field/id':uid(prompt+'selection'),':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':ans,':answer-field/correct':[':answer/id',correct]}]}
 rec=wrap(q,seed,template,{k:str(vv) for k,vv in p.items()},'method-bank',True)
 residual=s.expand(F-F.subs({x:u,y:v}));scale=F.as_ordered_terms()[0].as_coeff_Mul()[0]
 rec['generation']['mathematical_fingerprint']=digest([s.srepr(s.expand(residual/scale)),str(u),str(v)])
 return rec

def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)
def markdown(r):
 q=r['question'];m=r['generation'];lv=q.get(':question/difficulty','unrated')
 out=f"### {m['template']} — {lv} — {m['origin']}\n\nEvidence only: {m['evidence_only']}; profile: `{m['profile']}`\n\n"+q[':question/problem']+'\n\n'
 for f in q.get(':question/answer-fields',[]):
  out+=f"Field `{f[':answer-field/key']}` ({f[':answer-field/type']}):\n\n"
  for a in f[':answer-field/choices']:out+='- $'+a[':answer/value']+'$'+(' ✓' if f.get(':answer-field/correct',[None,None])[1]==a[':answer/id'] else '')+'\n'
 out+='\n'+q.get(':question/worked-solution','[Worked solution absent in raw source.]')+'\n'
 return out
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=2);ap.add_argument('--template');ap.add_argument('--profile');ap.add_argument('--format',choices=['markdown','json'],default='markdown');args=ap.parse_args()
 levels=['easy','moderate','hard'] if args.difficulty=='all' and not args.profile else ['moderate' if args.difficulty=='all' else args.difficulty]
 records=[generate(l,args.seed+n,template=args.template,profile=args.profile) for l in levels for n in range(args.count)]
 print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n'.join(map(markdown,records)))
