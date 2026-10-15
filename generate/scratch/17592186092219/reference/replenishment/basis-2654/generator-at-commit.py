#!/usr/bin/env python3
"""Point information -> Cartesian coordinates. Validated scoped generator; database submission is separate.

Normal defaults serve every observed family, preserve field ordering and shared
source solution sentences, and use complete source-bank profiles under positive similarity scaling.
Historical distractor intent remains unresolved; explicit whole-coordinate
recipes and complete-bank replay establish fidelity without inventing intent. The source
scale masks are parameterized mathematical components, not literal-question
returns. Source styles preserve unreduced square roots and all ordered stages.

Easy is authored: infer a radius from an axis point, apply a nonunit positive
scale, evaluate a familiar nonaxis angle. Moderate retains observed radius
square/scale and positive-axis angle-offset families. Hard retains observed
nonaxis reference-angle/quadrant/offset method; no angle identities are needed.
Explicit calls obey the same bounds as sampling. See local README/validation.
"""
from __future__ import annotations
import argparse, hashlib, json, random, re, sys, uuid
from pathlib import Path
import sympy as s
HERE=Path(__file__).with_suffix('')
CAPTURE=json.loads((HERE/'source.json').read_text()); KP=CAPTURE['record']
VERSION='point-information-v2-source-banks'
GENERATOR_UUID='03d0366e-7600-5400-8ccd-2792f45436bc'
SUPPORTED_LEVELS=('easy','moderate','hard')
Q={q[':question/math-academy-id']:q for q in KP[':knowledge-point/questions']}
# x_A,y_A,theta_A/pi, radial operation, radial operand,theta_B/pi, inferred level.
SPEC={
 'q-40803':('sqrt(10)','sqrt(10)','1/4','scale','2','1/3','moderate'),
 'q-40806':('sqrt(2)','-sqrt(2)','7/4','angle','1','3/2','hard'),
 'q-120455':('-3','sqrt(3)','5/6','square','1','11/6','moderate'),
 'q-120468':('-sqrt(3)','-1','7/6','angle','4','3/2','hard'),
 'q-276803':('sqrt(3)','1','1/6','scale','1/3','5/6','moderate'),
 'q-276807':('2*sqrt(3)','2','1/6','scale','2','7/6','moderate'),
 'q-276838':('5','0','0','angle','5','1/6','moderate'),
 'q-40804':('-sqrt(5)','sqrt(5)','3/4','square','1','4/3','moderate'),
 'q-40826':('-1','-1','5/4','angle','8','1/4','hard'),
 'q-86619':('3*sqrt(2)','3*sqrt(2)','1/4','scale','1/2','5/6','moderate')}

def tex(v):
 return s.latex(s.simplify(v),mul_symbol=None).replace('\\frac','\\frac').replace('\\left','').replace('\\right','').replace(' ','')
def parse(t):
 """Restricted exact LaTeX arithmetic parser, also used by independent validator."""
 t=t.replace('π',r'\pi').replace('⁡','').replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\cdot','*').replace(r'\dfrac',r'\frac')
 t=t.replace(r'\operatorname{cos}',r'\cos').replace(r'\operatorname{sin}',r'\sin').replace(r'\operatorname{arctan}',r'\arctan')
 # Normalize only if adjacent slash bytes exist; serialization is not evidence.
 t=t.replace('\\\\','\\')
 def group(text,pos):
  if text[pos]!='{':
   m=re.match(r'\d+|[a-zA-Z]',text[pos:]); return m.group(),pos+len(m.group())
  n=1;j=pos+1
  while n:
   n+=(text[j]=='{')-(text[j]=='}');j+=1
  return text[pos+1:j-1],j
 def convert(t):
  out='';i=0
  while i<len(t):
   if t.startswith(r'\frac',i):
    a,j=group(t,i+5);b,j=group(t,j);out+='(('+convert(a)+')/('+convert(b)+'))';i=j
   elif t.startswith(r'\sqrt',i):
    a,j=group(t,i+5);out+='sqrt('+convert(a)+')';i=j
   elif t.startswith(r'\pi',i):out+='pi';i+=3
   elif any(t.startswith('\\'+f,i) for f in ['arctan','cos','sin']):
    f=next(f for f in ['arctan','cos','sin'] if t.startswith('\\'+f,i));out+=' '+('atan' if f=='arctan' else f)+' ';i+=len(f)+1
   else:out+=t[i];i+=1
  return out.replace('{','(').replace('}',')').replace('^','**')
 from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
 return s.simplify(parse_expr(convert(t), transformations=standard_transformations+(implicit_multiplication_application,),local_dict={'r':s.Symbol('r',positive=True),'theta':s.Symbol('theta',real=True)}))
def tuple_math(v):
 v=v.strip().replace('\\\\','\\').replace(r'\left','').replace(r'\right','')
 assert v[0]=='(' and v[-1]==')',v
 return tuple(parse(x) for x in v[1:-1].split(','))
def pair(v):return '('+','.join(tex(x) for x in v)+')'
def uid(text):return str(uuid.uuid5(uuid.NAMESPACE_URL,'KP-point:'+text))
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def data(name,scale):
 x,y,a,op,c,b,_=SPEC[name];x,y,a,c,b=map(s.sympify,(x,y,a,c,b));x*=scale;y*=scale
 r=s.sqrt(x*x+y*y);R=r*r if op=='square' else r*c if op=='scale' else c*scale
 return dict(x=x,y=y,a=a,op=op,c=c,b=b,r=s.simplify(r),R=s.simplify(R),correct=(s.simplify(R*s.cos(b*s.pi)),s.simplify(R*s.sin(b*s.pi))))

def render_mask(text,scale,degree=1):
 """Frozen source component mask: @N@ is an integer coefficient with power d.

Each replacement is explicitly authored and scoped to a complete mathematical
component in masks.json. Never replace numeric substrings across prose/angles.
The coefficient recipe is N*scale**d; all typography is retained at scale=1.
"""
 return re.sub(r'@(-?\d+):(\d+)@',lambda m:str(int(m[1])*scale**int(m[2])),text)
MASKS=json.loads((HERE/'masks.json').read_text())
def source_strings(name,scale):
 m=MASKS[name]
 return render_mask(m['problem'],scale),render_mask(m.get('solution',''),scale)

def aligned(rows):return '$$\n\\begin{aligned}'+r' \\  '.join(rows)+r'\end{aligned}'+'\n$$'
def generic_solution(d,kind,source=None):
 x,y,r,R,a,b=d['x'],d['y'],d['r'],d['R'],d['a'],d['b'];out=''
 if kind=='radius':
  out='First, we use the Cartesian coordinates of $A$ to find $r,$ the distance between $A$ and the origin:\n\n'
  out+=aligned([r'r & =\sqrt{{x}^{2}+{y}^{2}}',r' & =\sqrt{('+tex(x)+r')^{2}+('+tex(y)+r')^{2}}',r' & =\sqrt{'+tex(x*x+y*y)+'}',r' & ='+tex(r)])
 else:
  out='First, we use the Cartesian coordinates of $A$ to find its reference angle ${\\theta }_{R}:$\n\n'
  ref=s.atan(abs(y/x)) if x else s.pi/2
  out+=aligned([r'{\theta }_{R} & =\operatorname{arctan}(\frac{'+tex(abs(y))+'}{'+tex(abs(x))+'})',r' & =\operatorname{arctan}('+tex(abs(y/x))+')',r' & ='+tex(ref)])
  quadrant='third' if x<0 and y<0 else 'fourth' if x>0 and y<0 else 'second' if x<0 else 'first'
  if y==0:out+='\n\nSince the point $A$ lies on the positive $x$-axis, we have $\\theta=0.$'
  else:out+='\n\nSince the point $A$ lies in the '+quadrant+' quadrant, we have $\\theta='+tex(a*s.pi)+'.$'
 
 if kind=='radius':
  radial='('+tex(r)+')^{2}' if d['op']=='square' else tex(d['c'])+r'\cdot('+tex(r)+')'
  conversion='('+radial+','+tex(b*s.pi)+')=('+tex(R)+','+tex(b*s.pi)+')'
 else:
  conversion='('+tex(R)+','+tex(a*s.pi)+'+('+tex((b-a)*s.pi)+'))=('+tex(R)+','+tex(b*s.pi)+')'
 out+='\n\nConsequently, the polar coordinates of $B$ are\n\n$$\n'+conversion+'.\n$$'
 out+='\n\nNow, we convert $B$ to Cartesian coordinates. To convert from polar coordinates to Cartesian coordinates, we use\n\n$$\nx=r\\operatorname{cos}⁡\\theta ,\\,y=r\\operatorname{sin}⁡\\theta .\n$$'
 for i,(v,func,word) in enumerate([('x','cos','First'),('y','sin','Then')]):
  factor=s.cos(b*s.pi) if i==0 else s.sin(b*s.pi)
  out+='\n\n'+word+', we calculate the $'+v+'$-coordinate of $B:$\n\n'
  out+=aligned([v+r' & =r\operatorname{'+func+r'}⁡\theta ',r' & ='+tex(R)+r'\cdot\operatorname{'+func+'}('+tex(b*s.pi)+')',r' & ='+tex(R)+r'\cdot('+tex(factor)+')',r' & ='+tex(d['correct'][i])])
 return out+'\n\nTherefore, the Cartesian coordinates of $B$ are $'+pair(d['correct'])+'.$'

def bank(d,kind):
 """A complete operation bank selected before parameters, never pooled.

Radius: correct, swapped trig assignments, omit scale/square, reverse x sign,
reverse y sign. Angle: correct, omit offset, subtract instead of add offset,
reverse the target ray, exchange x/y. Reject complete bank on any collision.
"""
 x,y=d['correct'];r,R,a,b=d['r'],d['R'],d['a'],d['b']
 if kind=='radius':return [(x,y),(y,x),(s.simplify(r*s.cos(b*s.pi)),s.simplify(r*s.sin(b*s.pi))),(-x,y),(x,-y)]
 if s.Mod(b-a,2)==1:
  return [(x,y),(s.simplify(R*s.cos(a*s.pi)),s.simplify(R*s.sin(a*s.pi))),(s.simplify(r*s.cos(b*s.pi)),s.simplify(r*s.sin(b*s.pi))),(-x,y),(x,-y)]
 return [(x,y),(s.simplify(R*s.cos(a*s.pi)),s.simplify(R*s.sin(a*s.pi))),(s.simplify(R*s.cos((2*a-b)*s.pi)),s.simplify(R*s.sin((2*a-b)*s.pi))),(-x,-y),(y,x)]
def unique_bank(values):return len({tuple(s.simplify(x) for x in v) for v in values})==len(values)

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('difficulty')
 rng=random.Random(seed);raw=bool(profile and profile.startswith('raw_'));observed=bool(profile and profile.startswith('observed_'));source_profile=bool(profile and profile.startswith('source_'))
 if raw or observed or source_profile:
  name=profile.split('_',1)[1]
  if template is not None and template!=name:raise ValueError('profile/template mismatch')
  template=name
 candidates=[n for n,z in SPEC.items() if z[-1]==level]
 if template is None:template='axis_radius' if level=='easy' else rng.choice(candidates)
 if template=='axis_radius':
  if level!='easy' or raw or observed:raise ValueError('easy authored only')
  if field_type not in (None,'radio','blank'):raise ValueError('field type')
  profile='authored_radius' if profile is None else profile;ft=field_type or rng.choice(['radio','blank'])
  if profile!='authored_radius':raise ValueError('bank profile')
  p=parameters if parameters is not None else {'radius':rng.randint(1,12),'factor':rng.choice([2,3,4,5]),'angle':rng.choice(['1/6','1/3','2/3','5/6','7/6','4/3','5/3','11/6'])}
  if set(p)!={'radius','factor','angle'}:raise ValueError('parameters')
  r,c,b=map(s.sympify,(p['radius'],p['factor'],p['angle']))
  if r not in range(1,13) or c not in [2,3,4,5] or b not in map(s.Rational,['1/6','1/3','2/3','5/6','7/6','4/3','5/3','11/6']):raise ValueError('easy bounds')
  d=dict(x=r,y=s.Integer(0),r=r,R=r*c,a=s.Integer(0),b=b,op='scale',c=c,correct=(s.simplify(r*c*s.cos(b*s.pi)),s.simplify(r*c*s.sin(b*s.pi))))
  problem='The point $A$ has polar coordinates $(r,0)$ and the point $B$ has polar coordinates $('+tex(c)+'r,'+tex(b*s.pi)+')$. Find the Cartesian coordinates of $B$ given that the Cartesian coordinates of $A$ are $('+tex(r)+',0)$.'
  solution=generic_solution(d,'radius');kind='radius';source=None;keys=['selection'] if ft=='radio' else ['field-2','field-1']
 else:
  if template not in SPEC or SPEC[template][-1]!=level:raise ValueError('template/level')
  name=template;source=Q[name];kind='angle' if SPEC[name][3]=='angle' else 'radius'
  source_ft=source[':question/answer-fields'][0][':answer-field/type'][':db/ident'].split('/')[-1]
  if field_type not in (None,source_ft):raise ValueError('source-shaped field type')
  ft=source_ft;keys=[f[':answer-field/key'] for f in source[':question/answer-fields']]
  profile='source_'+name if profile is None else profile;source_profile=profile=='source_'+name
  if profile not in ('authored_'+kind,'raw_'+name,'observed_'+name,'source_'+name):raise ValueError('profile')
  p=parameters if parameters is not None else {'scale':rng.randint(1,16 if level=='hard' else 8)}
  if set(p)!={'scale'} or isinstance(p['scale'],bool) or s.sympify(p['scale']) not in range(1,17 if level=='hard' else 9):raise ValueError('source scale outside level bounds')
  scale=int(p['scale']);d=data(name,scale)
  problem,solution=source_strings(name,scale)
  if not solution and not raw:solution=generic_solution(d,kind)
  # q-276838 incorrectly calls an axis point first-quadrant. Preserve raw; repair normal.
  if not raw:solution=solution.replace('lies in the first quadrant','lies on the positive $x$-axis')
 if ft=='blank' and template=='axis_radius':problem+='\n\nThe Cartesian coordinates of $B$ are $(${{field-1}}$,$\n{{field-2}}$).$'
 if raw or observed or source_profile:
  scale=int(p['scale']);values=[]
  for f in source[':question/answer-fields']:
   vals=[]
   for recipe in MASKS[template]['banks'][f[':answer-field/key']]:
    original=recipe['original'];factor=scale**recipe['degree']
    if factor==1: value=original
    elif ft=='radio': value=pair(tuple(factor*v for v in tuple_math(original)))
    else:value=tex(factor*parse(original))
    vals.append(value)
   values.append(vals)
 elif ft=='radio':
  opts=bank(d,kind)
  if not unique_bank(opts):raise ValueError('whole bank ambiguous; choose another instance/profile')
  values=[[pair(v) for v in opts]]
 else:values=[[tex(d['correct'][0 if k=='field-1' else 1])] for k in keys]
 # Content identity excludes aliases/seed/order, includes all rendered learner content.
 identity=digest([VERSION,level if not raw or ':question/difficulty' in source else None,problem,solution if solution else None,keys,ft,[sorted(v) for v in values]])
 task=digest([kind,tuple(str(d[k]) for k in ('x','y','a','b')),d['op'],str(d['c']),str(d['R'])])
 q={':question/id':uid(identity),':question/problem':problem}
 if not raw or ':question/difficulty' in source:q[':question/difficulty']=':question.difficulty/'+level
 if not raw or ':question/worked-solution' in source:q[':question/worked-solution']=solution
 fields=[]
 for fi,(key,vals) in enumerate(zip(keys,values)):
  fid=uid(identity+key);answers=[{':answer/id':uid(fid+v),':answer/type':':answer.type/math',':answer/value':v} for v in vals]
  f={':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+ft,':answer-field/choices':answers}
  if raw or observed or source_profile:
   sf=source[':question/answer-fields'][fi]
   if ':answer-field/correct' in sf:ci=next(i for i,a in enumerate(sf[':answer-field/choices']) if a[':answer/id']==sf[':answer-field/correct'][':answer/id'])
   elif raw:ci=None
   else:ci=next(i for i,v in enumerate(vals) if tuple_math(v)==d['correct'])
  else:ci=0
  if ci is not None:f[':answer-field/correct']=[':answer/id',answers[ci][':answer/id']]
  if ft=='radio':rng.shuffle(answers)
  fields.append(f)
 q[':question/answer-fields']=fields
 return {'knowledge_point':{'db_id':KP[':db/id'],'id':KP[':knowledge-point/id'],'title':KP[':knowledge-point/title']},'question':q,'generation':{'version':VERSION,'seed':seed,'template':template,'profile':profile,'parameters':p,'source':{k:CAPTURE[k] for k in ('database','basis','lineage')},'difficulty_claim':'observed' if source and ':question/difficulty' in source else 'authored','evidence_only':raw or observed or (ft=='radio' and template!='axis_radius' and not source_profile),'eligible_for_learning':not(raw or observed) and (source_profile or ft=='blank' or template=='axis_radius'),'mathematical_fingerprint':task,'content_fingerprint':identity,'python':sys.version.split()[0],'sympy':s.__version__}}

# Easy: authored axis-to-radius family, 12*4*8=384 mathematical tasks.
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
# Moderate: source scale/square or axis-offset recipes; all source layouts served.
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
# Hard: familiar nonaxis angle recovery, quadrant selection and offset.
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)
def markdown(r):
 q=r['question'];out=q[':question/problem']+'\n\n'
 for f in q.get(':question/answer-fields',[]):out+=f[':answer-field/key']+': '+', '.join('$'+a[':answer/value']+'$' for a in f[':answer-field/choices'])+'\n'
 return out+'\n'+q.get(':question/worked-solution','[Original solution absent]')+'\n'
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['json','markdown'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');a=ap.parse_args()
 rows=[generate(l,a.seed+i,template=a.template,profile=a.profile) for l in (['easy','moderate','hard'] if a.difficulty=='all' else [a.difficulty]) for i in range(a.count)]
 print(json.dumps(rows,indent=2,ensure_ascii=False) if a.format=='json' else '\n---\n'.join(markdown(r) for r in rows))
