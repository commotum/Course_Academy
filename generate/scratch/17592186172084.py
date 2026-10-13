#!/usr/bin/env python3
"""Identify a planar vector field from its qualitative diagram (basis 1356).

Nine complete observed five-choice banks; one unrated source receives an
explicitly authored moderate label, designation, and solution. One erroneous
eliminated formula in q-122629 is repaired, retaining raw evidence. No calculus.
Easy: constant direction. Moderate: one position-dependent component. Hard:
authored two position-dependent components; distinguish both signs/dependencies.
Each level is a finite catalog of qualitative tasks, not numerical progression.
Signed coordinate isometries produce genuinely parameterized observed recipes;
Positive magnitude of common scale is incidental and excluded from task
fingerprints. Explicit level bounds apply to callers as well as samplers.
All changed plots use Matplotlib, exact instance data, unique render inputs,
atomic PNG/sidecars. Unchanged meaningful geometry reuses captured assets.
No database access. JSON is local review data. See the adjacent evidence folder.
"""
from __future__ import annotations
import argparse, hashlib, json, os, random, re, subprocess, tempfile, uuid
from pathlib import Path
import sympy as sp

KP_ID=17592186172084
KP_UUID='a9734fc0-9789-5a9c-8ae0-806f87052875'
TITLE='Identifying a Two-Dimensional Vector Field'
VERSION='planar-identification-1'
HERE=Path(__file__).resolve().with_suffix('')
SOURCE=json.loads((HERE/'source.json').read_text())
QUESTIONS={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
X,Y,A=sp.symbols('x y a',real=True)
PROMPT='Which of the following could be the function that generates the vector field above?'
# Whole-bank expression recipes. Names are labels; their error intentions are
# unknown. They are not promoted to inferred cognitive diagnoses.
PROFILES={
 'q-122296':('moderate','horizontal_linear_vertical_constant',('a*x','-a'),[
  ('F','a*x','-a'),('H','a','2*a'),('G','-a*x','a*y'),('K','a','-2*a')]),
 'q-122463':('easy','constant_signs',('-a','a'),[
  ('F','a','-2*a'),('G','-a','a'),('K','0','-a'),('H','a','0')]),
 'q-122629':('moderate','horizontal_constant_vertical_cross',('a','a*x'),[
  ('H','2*a','-a'),('F','-a','-a'),('K','a','a*x'),('G','a','2*a')]),
 'q-122631':('moderate','vertical_linear_inward',('0','-a*y'),[
  ('K','0','-2*a'),('G','-a','2*a'),('H','a*x','-a*y'),('F','0','-a*y')]),
 'q-122632':('moderate','vertical_cross',('0','a*x'),[
  ('K','-a','-2*a'),('H','0','a*x'),('G','0','5*a'),('F','a','a')]),
 'q-122633':('moderate','horizontal_cross',('a*y','0'),[
  ('H','a*y','a'),('F','a*x','0'),('G','a*y','0'),('K','-a','0')]),
 'q-122634':('easy','constant_horizontal',('a','0'),[
  ('K','a','0'),('F','0','-a'),('H','-a','0'),('G','0','a')]),
 'q-122637':('easy','constant_vertical',('0','-5*a'),[
  ('K','-3*a','0'),('G','0','2*a'),('F','4*a','0'),('H','0','-5*a')]),
 'q-122630':('moderate','horizontal_constant_vertical_linear',('-2*a','a*y'),[
  ('K','a*x','a'),('H','-2*a','a*y'),('G','a','a'),('F','-a','a')]),
}
TEMPLATES={spec[1]:spec[0] for spec in PROFILES.values()}
TEMPLATES['two_variable']='hard'

def stable(data):
 return hashlib.sha256(json.dumps(data,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def uid(data): return str(uuid.uuid5(uuid.NAMESPACE_URL,stable(data)))

def expressions(pair):
 return tuple(sp.sympify(e,locals={'x':X,'y':Y,'a':A}) for e in pair)

def transform(pair,p):
 """Signed permutation: V_new = R V_old(R^-1 [x,y])."""
 sx,sy=p['sx'],p['sy']; swap=p['swap'];a=p['a']
 xx,yy=(Y,X) if swap else (X,Y)
 u,v=(e.subs({X:sx*xx,Y:sy*yy,A:a},simultaneous=True) for e in expressions(pair))
 u,v=sp.expand(sx*u),sp.expand(sy*v)
 return (v,u) if swap else (u,v)

def vector_tex(pair,compact=False):
 """Source-compatible component masks; signs, units, zero terms kept coherent."""
 parts=[]
 for e,basis in zip(pair,('i','j')):
  e=sp.expand(e)
  if e==0:continue
  negative=e.could_extract_minus_sign(); value=-e if negative else e
  c='' if value==1 else sp.latex(value)
  # All eligible expressions are a monomial or a constant.
  separator='' if compact or not c else r'\,'
  atom=c+separator+basis
  parts.append(('-' if negative else '+' if parts else '')+atom)
 return ''.join(parts) or '0'

def formula(name,pair,profile):
 if profile=='q-122296':
  rhs=vector_tex(pair,True)
  rhs=re.sub(r'(?<=\w)([+-])',r' \1 ',rhs)
  return name+'(x, y)'+(' =' if name=='G' else ' = ')+rhs
 return name+'(x,y)='+vector_tex(pair)

def generated_solution(profile,p,values):
 """Complete source prose/stage skeletons, with whole-formula slots.

 Transform prose outside those slots, so changing basis letters never corrupts
 function arguments or coordinate symbols. q629's raw nonbank F expression is
 explicitly replaced with the real F choice, a recorded mathematical repair.
 """
 q=QUESTIONS[profile]
 if ':question/worked-solution' not in q:
  text=("We notice the following:\n\n"
   "- As we move away from the origin in the horizontal direction, our vectors' horizontal components (i.e., the $i$ components) get longer. Therefore, we can rule out the following options:\n\n$$\n{H},\\,{K}\n$$\n\n"
   "- The vertical component (i.e., the $j$ component) is negative for each vector in our vector field. Therefore, we can rule out the following option:\n\n$$\n{G}\n$$\n\n"
   "Therefore, we conclude that the diagram corresponds to the vector field ${F}.$")
 else:
  text=q[':question/worked-solution']
  original={name:formula(name,transform((u,v),dict(a=1,sx=1,sy=1,swap=False)),profile) for name,u,v in PROFILES[profile][3]}
  if profile=='q-122629':text=text.replace(r'F(x,y)=-i+x\,j',original['F'])
  for name,value in sorted(original.items(),key=lambda z:-len(z[1])):
   text=text.replace(value,'{'+name+'}')
 # Only English/basis tokens are transformed. Formula slots remain masked.
 lines=[]
 for line in text.split('\n'):
  old_axis='horizontal' if 'horizontal component' in line else 'vertical' if 'vertical component' in line else None
  if old_axis:
   factor=(p['sx'] if old_axis=='horizontal' else p['sy'])*(1 if p['a']>0 else -1)
   if factor==-1:
    line=re.sub(r'positive|negative',lambda m:'negative' if m[0]=='positive' else 'positive',line)
  if p['swap']:
   line=re.sub(r'horizontal|vertical',lambda m:'vertical' if m[0]=='horizontal' else 'horizontal',line)
   line=re.sub(r'\$(i|j)\$',lambda m:'$'+('j' if m[1]=='i' else 'i')+'$',line)
  lines.append(line)
 text='\n'.join(lines)
 for name,value in values.items():text=text.replace('{'+name+'}',value)
 return text

def render_plots(pair,profile,p):
 """Reuse only unchanged full meaningful geometry; changed data are rendered."""
 original=profile in PROFILES and p==dict(a=1,sx=1,sy=1,swap=False)
 if original:
  raw=re.search(r'!\[\]\(([^)]+)\)',QUESTIONS[profile][':question/problem'])[1]
  path=HERE/'source-images'/Path(raw).name
  return {'prompt':str(path),'renderer':'captured-source','logical_reference':raw}
 # Data, not independently sampled formulas, cross the renderer boundary.
 key=stable({'pair':[str(e) for e in pair],'style':'qualitative-field-1'})
 folder=HERE/'plots';folder.mkdir(exist_ok=True)
 png=folder/(key+'.png');sidecar=folder/(key+'.json')
 if not(png.exists() and sidecar.exists()):
  points=[]
  for x in range(-9,10,2):
   for y in range(-9,10,2):
    xx,yy=sp.Rational(x,2),sp.Rational(y,2)
    u,v=[e.subs({X:xx,Y:yy}) for e in pair]
    points.append([str(xx),str(yy),str(u),str(v)])
  payload={'output':str(png),'sidecar':str(sidecar),'field':[str(e) for e in pair],
   'points':points,'key':key,'bounds':[-5.7,5.7],'style':'qualitative-field-1'}
  with tempfile.NamedTemporaryFile(mode='w',prefix='render-',suffix='.json',dir=folder,delete=False) as f:
   json.dump(payload,f);input_path=f.name
  try:subprocess.run([os.sys.executable,str(HERE/'render.py'),input_path],check=True,capture_output=True)
  finally:Path(input_path).unlink(missing_ok=True)
 return {'prompt':str(png),'renderer':'Matplotlib','sidecar':str(sidecar)}

def validate_parameters(level,p):
 keys={'sx','sy','swap','a'}
 if set(p)!=keys:raise ValueError('Expected exactly '+str(sorted(keys)))
 if type(p['swap']) is not bool:raise ValueError('swap must be Boolean')
 if type(p['sx']) is not int or type(p['sy']) is not int or p['sx'] not in (-1,1) or p['sy'] not in (-1,1):raise ValueError('signs must be +/-1')
 if type(p['a']) is not int or not 1<=abs(p['a'])<=3:raise ValueError('nonzero common signed scale magnitude must be 1..3')
 if level=='hard' and p['a']!=1:raise ValueError('hard has unit linear components only')

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('difficulty')
 if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('radio only')
 rng=random.Random(seed)
 if template is None:
  template=PROFILES[profile][1] if profile in PROFILES else rng.choice([k for k,v in TEMPLATES.items() if v==level])
 if TEMPLATES.get(template)!=level:raise ValueError('template not eligible at level')
 if level=='hard':
  profile=profile or 'authored_two_variable'
  if profile!='authored_two_variable':raise ValueError('hard profile')
 else:
  eligible=[name for name,spec in PROFILES.items() if spec[0]==level and spec[1]==template]
  profile=profile or rng.choice(eligible)
  if profile not in eligible:raise ValueError('profile not eligible at level')
 p=dict(parameters) if parameters is not None else dict(a=1 if level=='hard' else rng.choice((-1,1)),sx=rng.choice((-1,1)),sy=rng.choice((-1,1)),swap=rng.choice((False,True)))
 validate_parameters(level,p)
 if level=='hard':
  # Two independently varying components, both nonzero and unit linear.
  u,v=(Y,X) if p['swap'] else (X,Y)
  pair=(p['sx']*u,p['sy']*v)
  bank=[('F',pair),('G',(-pair[0],pair[1])),('H',(pair[0],-pair[1])),('K',(p['sx']*v,p['sy']*u))]
  values={name:formula(name,b,'hard') for name,b in bank}
  xdep='vertical' if p['swap'] else 'horizontal';ydep='horizontal' if p['swap'] else 'vertical'
  hp='positive' if p['sx']==1 else 'negative';vp='positive' if p['sy']==1 else 'negative'
  solution=("We notice the following:\n\n"
   f"- As we move away from the origin in the {xdep} direction, our vectors' horizontal components (i.e., the $i$ components) get longer. As we move away from the origin in the {ydep} direction, their vertical components (i.e., the $j$ components) get longer. Therefore, we can rule out the following option:\n\n$$\n{values['K']}\n$$\n\n"
   f"- The horizontal component is {hp} where ${'y' if p['swap'] else 'x'}>0,$ and the vertical component is {vp} where ${'x' if p['swap'] else 'y'}>0.$ Therefore, we can rule out the following options:\n\n$$\n{values['G']},\\,{values['H']}\n$$\n\n"
   f"Therefore, we conclude that the diagram corresponds to the vector field ${values['F']}.$")
 else:
  spec=PROFILES[profile];pair=transform(spec[2],p)
  bank=[(name,transform((u,v),p)) for name,u,v in spec[3]]
  values={name:formula(name,b,profile) for name,b in bank}
  solution=generated_solution(profile,p,values)
 # Complete bank first, reject the whole instance if any duplicates/ambiguity.
 if len({tuple(map(str,b)) for _,b in bank})!=4:raise ValueError('duplicate bank')
 matching=[name for name,b in bank if all(sp.expand(z-t)==0 for z,t in zip(b,pair))]
 if len(matching)!=1:raise ValueError('ambiguous or unmatched field')
 correct_name=matching[0];plots=render_plots(pair,profile,p)
 problem='![]('+plots['prompt']+')\n\n'+PROMPT
 # Different complete banks distinguish content; order and seed do not.
 content={'version':VERSION,'problem':problem,'solution':solution,'choices':sorted(values.values())+['None of the listed'],'level':level}
 qid=uid(content);fid=uid([qid,'selection'])
 choices=[{':answer/id':uid([fid,value]),':answer/type':':answer.type/math',':answer/value':value} for value in values.values()]
 choices.append({':answer/id':uid([fid,'None of the listed']),':answer/type':':answer.type/text',':answer/value':'None of the listed'})
 correct=uid([fid,values[correct_name]]);rng.shuffle(choices)
 # Task is qualitative geometry (component dependencies/signs), not length scale.
 primitive=[sp.expand(e/abs(p['a'])) for e in pair]
 coefficients=[c for e in primitive for c in sp.Poly(e,X,Y).coeffs() if c]
 common=sp.gcd_list(coefficients)
 task_pair=[str(sp.expand(e/abs(common))) for e in primitive]
 question={':question/id':qid,':question/difficulty':':question.difficulty/'+level,
  ':question/problem':problem,':question/worked-solution':solution,
  ':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',
  ':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,
  ':answer-field/correct':[':answer/id',correct]}]}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':question,
  'generation':{'version':VERSION,'seed':seed,'template':template,'bank_profile':profile,'parameters':p,
   'source':{k:SOURCE[k] for k in ('database','basis','lineage')},'source_ids':[profile] if profile in PROFILES else [],
   'authored':profile=='authored_two_variable','field':[str(e) for e in pair],'domain':'R^2',
   'mathematical_fingerprint':stable(task_pair),'content_fingerprint':stable(content),'plots':plots,
   'repairs':['missing source designation/solution; authored moderate label'] if profile=='q-122296' else ['solution eliminated F formula corrected to actual bank value'] if profile=='q-122629' else []}}

# Easy: constant directions, including signed and zero components; 3 source banks.
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
# Moderate: one nonconstant component, constant/zero other; 6 source banks.
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
# Hard (authored missing level): both linear components must be identified.
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)

def markdown(r):
 q=r['question'];f=q[':question/answer-fields'][0]
 return q[':question/problem']+'\n\n'+'\n\n'.join('- '+('$'+a[':answer/value']+'$' if a[':answer/type'].endswith('/math') else a[':answer/value']) for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']

def main():
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all')
 parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=1)
 parser.add_argument('--format',choices=['json','markdown'],default='markdown')
 parser.add_argument('--template');parser.add_argument('--profile')
 args=parser.parse_args()
 if args.count<1:parser.error('positive count required')
 levels=['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]
 records=[generate(level,args.seed+i,template=args.template,profile=args.profile) for level in levels for i in range(args.count)]
 print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))

if __name__=='__main__':main()
