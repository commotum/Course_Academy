#!/usr/bin/env python3
"""Circle slope generator, immutable math basis 1356; local review only.

Observed five-option banks are parameterized literal algebra patterns. Their error
intent is incompletely identifiable; use them as evidence profiles, not defaults.
Raw profiles preserve missing solution/difficulty/correct attributes. Default
banks apply the actual derivative operations: lose minus, invert, omit the x
power-rule factor, omit the y power-rule factor. Whole banks precede sampling.
Easy reads an origin-centered circle. Moderate reads signed integral center
coordinates. Authored hard reads two nonintegral half-coordinate shifts, retaining
exactly the same equation, linearity, chain rule, rearrangement, division method.
See sibling evidence README and template-extraction for domains and limitations.
"""
from __future__ import annotations
import argparse, hashlib, json, random, re, subprocess, sys, tempfile, uuid
from pathlib import Path
import sympy as sp
HERE=Path(__file__).with_suffix(''); KP=17592186166865
VERSION='circle-slope-1'; X,Y=sp.symbols('x y',real=True)
SOURCE=json.loads((HERE/'source.json').read_text()); R=SOURCE['record']
GEOMETRY={'q-127359':(0,0,2),'q-127360':(1,-1,3),'q-127493':(0,0,4),'q-127497':(1,0,2),'q-127499':(-1,1,1),'q-127500':(-3,-2,2),'q-127502':(0,-2,3)}
QUESTIONS={q[':question/math-academy-id']:q for q in R[':knowledge-point/questions']}
PROFILES={i:i for i in QUESTIONS}
TEMPLATES=('origin','shifted','fractional_shifted')
D=r'\frac{\text{d}y}{\text{d}x}'; OP=r'\frac{\text{d}}{\text{d}x}'

def tex(v):return sp.latex(sp.sympify(v))
def compact(v):return tex(v).replace(' ','')
def shift(var,c):
 c=sp.sympify(c)
 return var if c==0 else var+('+' if c<0 else '-')+compact(abs(c))
def group(v):return '('+v+')'
def square(var,c):return '{'+var+'}^{2}' if c==0 else group(shift(var,c))+'^{2}'
def frac(a,b,negative=False):return ('-' if negative else '')+r'\frac{'+a+'}{'+b+'}'
def numeric_group(v):return group(tex(v)) if v<0 else tex(v)
def raw_square(var,c):return '('+var+'-'+numeric_group(c)+')^{2}'

def solution(h,k,r,style):
 u,v=shift('x',h),shift('y',k); a,b=square('x',h),square('y',k)
 U=u if h==0 else group(u); V=v if k==0 else group(v)
 center='the origin' if h==k==0 else '$('+tex(h)+','+tex(k)+')$'
 intro='Since our circle is centered at '+center+' and has a radius of $'+tex(r)+',$ its equation is given by'
 eq=(a+'+'+b if h==k==0 else raw_square('x',h)+'+'+raw_square('y',k))+'={'+tex(r)+'}^{2}'+r'\,⟹\,'+a+'+'+b+'='+tex(r**2)+'.'
 end=frac(u,v,True)
 if style=='q-127497':end=frac(tex(h)+'-x','y')
 rows=[OP+'('+a+'+'+b+') & ='+OP+'('+tex(r**2)+')', OP+'('+a+')+'+OP+'('+b+') & =0', '2'+U+'+2'+V+D+' & =0','2'+V+D+' & =-2'+U,D+' & ='+(frac(u,v,True) if style=='q-127499' else end)]
 if style=='q-127499':rows.append(D+' & ='+frac(u,shift('y',k).replace('y-'+compact(k),compact(k)+'-y') if k>0 else tex(k)+'-y'))
 return intro+'\n\n$$\n'+eq+'\n$$\n\nNow, to calculate $'+D+',$ we use implicit differentiation:\n\n$$\n'+r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}'+'\n$$'

def bank(h,k,r,profile):
 u,v=shift('x',h),shift('y',k); up,vp=shift('x',-h),shift('y',-k)
 f=frac
 if profile=='q-127359':return [f('x^{2}','y^{2}',True),f('y','x',True),f('x','y',True),f('x','y'),'yx^{2}']
 if profile=='q-127360':
  # Original source deliberately spaces each complete affine component.
  u,v,up,vp=[z.replace('+',' + ').replace('-',' - ') for z in (u,v,up,vp)]
  return [f(vp,up,True),f(up,vp,True),f(vp,up),f(u,v,True),f(up,v)]
 if profile=='q-127493':return [f('2x','y'),f(compact(r)+'x','y',True),f('y','x'),f('x','y',True),f('{x}^{2}','y',True)]
 if profile=='q-127497':
  n=tex(h)+'-x';return [group(n)+'y',f(up,'y',True),f(n,'y'),'-'+group(up)+'y',f(up,'y')]
 if profile=='q-127499':return ['2'+group(u)+group(vp),f(tex(-h)+'-x',vp),f(u,tex(k)+'-y'),f('2'+group(u),v),group(u)+group(tex(k)+'-y')]
 if profile=='q-127500':return [f(v,u),f(u,v,True),f('2'+group(up),vp),f(v,up),f('2'+group(v),u,True)]
 if profile=='q-127502':return [f('y',shift('x',k)),f(v,'x',True),f(shift('x',k),compact(r)+'y',True),f('x',v,True),f(shift('x',r),v)]
 if profile=='method':
  U=u if h==0 else group(u);V=v if k==0 else group(v)
  return [f(u,v,True),f(u,v),f(v,u,True),f('2'+U,v,True),f(u,'2'+V,True)]
 raise ValueError('unknown complete bank')

def validate_parameters(level,p,profile):
 if set(p)!={'h','k','r'}:raise ValueError('parameters must be h,k,r')
 h,k,r=[sp.sympify(p[t]) for t in ('h','k','r')]
 if any(not z.is_real or not z.is_number for z in (h,k,r)) or r<=0:raise ValueError('real numeric center and positive radius required')
 if profile in PROFILES:
  if profile in ('q-127359','q-127493') and (h!=0 or k!=0):raise ValueError('origin profile requires origin')
  if profile=='q-127497' and (k!=0 or h==0):raise ValueError('x-shift bank requires k=0,h!=0')
  if profile=='q-127502' and (h!=0 or k==0):raise ValueError('y-shift bank requires h=0,k!=0')
  if profile in ('q-127360','q-127499','q-127500') and (h==0 or k==0):raise ValueError('two-shift bank requires both nonzero')
 # Evidence profiles retain their source-shape guards in addition to the same
 # finite arithmetic workload used by learning profiles. Explicit replay cannot
 # use arbitrary real/irrational shifts or large-denominator fractions.
 if level=='easy' and (h!=0 or k!=0 or r not in EASY_RADII):raise ValueError('easy origin/familiar radius bounds')
 if level=='moderate' and (not h.is_Integer or not k.is_Integer or h==k==0 or max(abs(h),abs(k))>4 or r not in MOD_RADII):raise ValueError('moderate signed integer center bounds')
 if level=='hard' and (h not in HARD_CENTERS or k not in HARD_CENTERS or r not in HARD_RADII):raise ValueError('hard requires two nonintegral half centers')
 return h,k,r
EASY_RADII=tuple(map(sp.sympify,[1,2,3,4,5,6]))+(sp.sqrt(2),sp.sqrt(5))
MOD_RADII=tuple(map(sp.Integer,range(1,5)))
HARD_CENTERS=tuple(sp.Rational(n,2) for n in (-7,-5,-3,-1,1,3,5,7))
HARD_RADII=tuple(sp.Rational(n,2) for n in range(2,9))

def sample(level,rng,profile):
 if profile in PROFILES:
  h,k,r=GEOMETRY[profile]
  if h: h=rng.choice([-4,-3,-2,-1,1,2,3,4])
  if k: k=rng.choice([-4,-3,-2,-1,1,2,3,4])
  r=rng.choice([1,2,3,4]);return dict(h=h,k=k,r=r)
 if level=='easy':return dict(h=0,k=0,r=str(rng.choice(EASY_RADII)))
 if level=='moderate':
  h,k=rng.choice([(h,k) for h in range(-4,5) for k in range(-4,5) if h or k]);return dict(h=h,k=k,r=rng.choice(MOD_RADII))
 return dict(h=str(rng.choice(HARD_CENTERS)),k=str(rng.choice(HARD_CENTERS)),r=str(rng.choice(HARD_RADII)))

def parse(value):
 # Independent parse is provided by validation; this parser prevents full-bank collisions.
 import importlib.util
 path=HERE.parent.parent/'runs/current/ode-scalar-parser.py'
 spec=importlib.util.spec_from_file_location('circle_bank_parser',path);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
 return mod.scalar(value)

def render_plots(p,output_dir=None):
 out=Path(output_dir or HERE/'plots');out.mkdir(parents=True,exist_ok=True)
 key=hashlib.sha256(json.dumps(p,sort_keys=True).encode()).hexdigest()[:24]
 png=out/(key+'.png'); side=out/(key+'.json')
 if not (png.exists() and side.exists()):
  with tempfile.TemporaryDirectory(prefix='circle-render-',dir=out) as tmp:
   inp=Path(tmp)/'input.json';inp.write_text(json.dumps(p))
   subprocess.run([sys.executable,str(HERE/'render.py'),str(inp),str(png),str(side)],check=True,stdout=subprocess.DEVNULL)
 return str(png.resolve())

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('unsupported level')
 if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('radio only')
 if template is None:template={'easy':'origin','moderate':'shifted','hard':'fractional_shifted'}[level]
 if template not in TEMPLATES:raise ValueError('unknown template')
 if template!={'easy':'origin','moderate':'shifted','hard':'fractional_shifted'}[level] and profile not in PROFILES:raise ValueError('template/level mismatch')
 profile=profile or 'method' # Whole profile selected before any sample.
 if profile not in ('method',*PROFILES):raise ValueError('unknown profile')
 if profile in PROFILES and level != ('easy' if profile in ('q-127359','q-127493') else 'moderate'):raise ValueError('observed profile level mismatch')
 rng=random.Random(seed)
 for attempt in range(100):
  p=parameters if parameters is not None else sample(level,rng,profile)
  h,k,r=validate_parameters(level,p,profile);values=bank(h,k,r,profile)
  expressions=[parse(z) for z in values];f=(X-h)**2+(Y-k)**2-r**2
  # Validity is on the requested locus, not only formal rational-expression spelling.
  # The curve may have rational coefficients even when a complete bank uses
  # an allowed algebraic radius (e.g. -sqrt(2)*x/y). The exact expression
  # coefficient domain includes those bank coefficients, rather than inferring
  # a narrower integer field from the circle polynomial alone.
  gb=sp.groebner([f],X,Y,domain=sp.EX)
  def same(a,b):return sp.simplify(gb.reduce(sp.together(a-b).as_numer_denom()[0].expand())[1])==0
  if any(same(a,b) for i,a in enumerate(expressions) for b in expressions[i+1:]):
   if parameters is not None:raise ValueError('whole bank rejected: equivalent choices')
   continue
  matches=[i for i,z in enumerate(expressions) if same(z,-(X-h)/(Y-k))]
  if len(matches)!=1:
   if parameters is not None:raise ValueError('whole bank rejected: ambiguous key')
   continue
  break
 else:raise RuntimeError('cannot sample complete bank')
 params={a:str(z) for a,z in zip(('h','k','r'),(h,k,r))}
 plot=render_plots(params)
 old=QUESTIONS.get(profile)
 prompt='![]('+plot+')\n\nFind $'+(r'\frac{dy}{dx}' if profile in ('q-127359','q-127360') else D)+'$ for the circle shown above.'
 worked=solution(h,k,r,profile)
 raw=profile in PROFILES
 if raw and ':question/worked-solution' not in old:worked=None
 # Exact source-image substitution is only valid at recovered original geometry.
 original=raw and (h,k,r)==tuple(map(sp.sympify,GEOMETRY[profile]))
 if original:prompt=re.sub(r'!\[\]\([^)]*\)',old[':question/problem'].split('\n\n')[0],prompt,count=1)
 content={'version':VERSION,'prompt':prompt,'solution':worked,'bank':sorted(values),'difficulty':level if not raw or ':question/difficulty' in old else None}
 digest=hashlib.sha256(json.dumps(content,sort_keys=True).encode()).hexdigest();uid=lambda role:str(uuid.uuid5(uuid.NAMESPACE_URL,digest+':'+role))
 answers=[{':answer/id':uid('answer:'+v),':answer/type':':answer.type/math',':answer/value':v} for v in values]
 correct=answers[matches[0]][':answer/id'];rng.shuffle(answers)
 field={':answer-field/id':uid('field:selection'),':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers}
 if not raw or ':answer-field/correct' in old[':question/answer-fields'][0]:field[':answer-field/correct']=[':answer/id',correct]
 question={':question/id':uid('question'),':question/problem':prompt,':question/answer-fields':[field]}
 if not raw or ':question/difficulty' in old:question[':question/difficulty']=':question.difficulty/'+level
 if worked is not None:question[':question/worked-solution']=worked
 return {'knowledge_point':{'db_id':KP,'id':R[':knowledge-point/id'],'title':R[':knowledge-point/title']},'question':question,'generation':{'version':VERSION,'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__,'plot_renderer_sidecar':str(Path(plot).with_suffix('.json'))},'seed':seed,'parameters':params,'template':template,'bank_profile':profile,'origin':'observed parameterized evidence' if raw else 'authored method bank','eligible_for_learning':not raw,'evidence_only':raw,'source_id':profile if raw else None,'source':{k:SOURCE[k] for k in ('database','basis','lineage')},'content_fingerprint':digest,'mathematical_fingerprint':hashlib.sha256(str(sp.expand(f)).encode()).hexdigest(),'derivative_fingerprint':str(sp.cancel(-(X-h)/(Y-k))),'domain':{'circle':str(f),'finite_slope_excludes':str(Y-k)},'plot':plot,'inferred_correct_answer_id':correct if raw and ':answer-field/correct' not in field else None}}

# Easy: source origin template, no center shifts; radius affects circle equation,
# not the generic derivative. Eight meaningful curves, one derivative structure.
def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
# Moderate: same formal five stages, one or two signed integral center shifts.
def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)
# Hard: authored fractional signed two-coordinate centers, no new calculus branch.
def generate_hard(seed=0,**kw):return generate('hard',seed,**kw)

def markdown(record):
 q=record['question'];g=record['generation'];f=q[':question/answer-fields'][0]
 level=q.get(':question/difficulty','unrated raw').split('/')[-1]
 lines=['## '+level+' | '+g['origin']+' | '+g['bank_profile'],q[':question/problem']]
 for i,a in enumerate(f[':answer-field/choices']):
  mark=' **correct**' if f.get(':answer-field/correct',[None,None])[1]==a[':answer/id'] else (' **inferred correct; absent source key**' if g['inferred_correct_answer_id']==a[':answer/id'] else '')
  lines.append(f'{chr(65+i)}. $'+a[':answer/value']+'$'+mark)
 lines.append(q.get(':question/worked-solution','_Worked solution absent from raw source._'))
 return '\n\n'.join(lines)
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');a.add_argument('--seed',type=int,default=0);a.add_argument('--count',type=int,default=1);a.add_argument('--format',choices=['markdown','json'],default='markdown');a.add_argument('--template');a.add_argument('--profile');z=a.parse_args()
 records=[generate(l,z.seed+i,template=z.template,profile=z.profile) for l in (['easy','moderate','hard'] if z.difficulty=='all' else [z.difficulty]) for i in range(z.count)]
 print(json.dumps(records,indent=2) if z.format=='json' else '\n\n'.join(markdown(x) for x in records))
