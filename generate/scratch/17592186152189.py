#!/usr/bin/env python3
"""General-center ellipse parametrization, basis 1356. Stop at guide step 7.

Observed source masks and complete banks are compiled into private specs.json.
Raw observed replay preserves absent attributes and legacy field layouts, and is
marked evidence-only when incomplete. All recipes are mathematical operations,
never literal answer lookups. Source profiles have interpretation limits described
in extraction. Normal easy supplies center/radii; moderate reads them from a graph;
hard additionally enforces rightmost starting point and CCW traversal, and supports
the observed two-expression blank layout. Integer radii 1..8, shifts -6..6,
a != b, center != origin. No restricted arcs or Cartesian conversion are assessed.
"""
from __future__ import annotations
import argparse,hashlib,json,random,re,sys,uuid,subprocess,tempfile,os
from pathlib import Path
import sympy as sp
D=Path(__file__).with_suffix('');SPECS={x['id']:x for x in json.loads((D/'specs.json').read_text())}
KP_ID=17592186152189;KP_UUID='6d82541c-40ca-5df9-aa17-c20b201fadd4';TITLE='The Parametric Equations of an Ellipse Centered at a General Point';VERSION='ellipse-general-1'
T=sp.Symbol('theta',real=True)
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def uid(x):return str(uuid.uuid5(uuid.NAMESPACE_URL,'kp17592186152189:'+str(x)))
def val(e,p):return sp.sympify(e).subs({sp.Symbol(k):v for k,v in p.items()})
def number(x):return str(x) if sp.denom(x)==1 else sp.latex(x)
def expr(c,f,z,style=None):
 if style is None:style={'prefix':'','function':r'\{FUNC}\theta','space':'','explicit_one':False,'sign_space':'','zero_space':''}
 coef='' if c==1 and not style['explicit_one'] else number(c)
 tail=style['space']+('+' if z>0 else '-')+style.get('sign_space','')+number(abs(z)) if z else style.get('zero_space','')
 return style['prefix']+coef+style['function'].replace('{FUNC}',f)+tail

def answer(recipe,p,styles=None):
 if len(recipe)==3:
  c,z,f=recipe;return expr(val(c,p),f,val(z,p),styles[0] if styles else None)
 a,b,h,k,f,g=recipe;ss=styles or [None,None]
 x=expr(val(a,p),f,val(h,p),ss[0]);y=expr(val(b,p),g,val(k,p),ss[1]);return x+y if styles else 'x='+x+r',\,y='+y

def displayed_pair(v):
 """Parse the rendered two equations before accepting a complete radio bank."""
 def parse(s):
  s=s.replace('⁡','').replace('θ','theta').replace(r'\theta','theta').replace(' ','').replace(r'\,','').replace(r'\operatorname{cos}','cos').replace(r'\operatorname{sin}','sin').replace(r'\cos','cos').replace(r'\sin','sin')
  s=re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}',r'(\1)/(\2)',s)
  s=re.sub(r'(cos|sin)theta',r'\1(theta)',s);s=re.sub(r'(?<=[0-9)])(?=(?:cos|sin)\()', '*',s)
  return sp.sympify(s,locals={'theta':T})
 parts=re.split(r',\s*(?:\\,)?y\s*=\s*',v)
 if len(parts)!=2:raise ValueError('Two complete parametric equations required')
 return parse(re.sub(r'^x\s*=\s*','',parts[0])),parse(parts[1])

def require_bank(values,p,oriented):
 pairs=[displayed_pair(v) for v in values]
 valid=[]
 for x,y in pairs:
  locus=sp.trigsimp(((x-p['h'])/p['a'])**2+((y-p['k'])/p['b'])**2-1)==0
  valid.append(bool(locus and (not oriented or (x.subs(T,0)==p['h']+p['a'] and y.subs(T,0)==p['k'] and sp.diff(y,T).subs(T,0)>0))))
 if sum(valid)!=1:raise ValueError('Reject whole instance: ambiguous or incorrect response bank')
 for i,(x,y) in enumerate(pairs):
  for xx,yy in pairs[:i]:
   if sp.trigsimp(x-xx)==0 and sp.trigsimp(y-yy)==0:raise ValueError('Reject whole instance: equivalent displayed options')

def render_plot(p,oriented=False,spec=None):
 if spec and p==spec['parameters']:
  return spec['asset']
 rh=hashlib.sha256((D/'render.py').read_bytes()).hexdigest();key=digest([p,oriented,rh]);out=D/'plots'/f'{key}.png';meta=out.with_suffix('.json')
 if not(out.exists() and meta.exists() and json.loads(meta.read_text()).get('png_sha256')==hashlib.sha256(out.read_bytes()).hexdigest()):
  D.joinpath('plots').mkdir(exist_ok=True);fd,tmp=tempfile.mkstemp(prefix='input-',suffix='.json',dir=D/'plots');os.close(fd)
  try:
   Path(tmp).write_text(json.dumps({'parameters':p,'oriented':oriented,'target':str(out)}));subprocess.run([sys.executable,str(D/'render.py'),tmp],check=True)
  finally:Path(tmp).unlink()
 return str(out.resolve())

GENERAL='The parametric equations of an ellipse centered at the point $(h,k)$ with a horizontal radius of length $a$ and a vertical radius of length $b$ are\n\n$$\nx=a\\cos\\theta+h,\\,y=b\\sin\\theta+k,\\,\\theta \\in [0,2\\pi ).\n$$'
ORIENTATION='Under this parametrization, the ellipse is traversed once in the counterclockwise direction, starting from $(h+a,k).$'
BANK=[('a','b','h','k','cos','sin'),('2*a','2*b','h','k','cos','sin'),('b','a','h','k','cos','sin'),('a','b','-h','-k','cos','sin'),('b**2','a**2','h','k','cos','sin')]
HARD_BANK=[('a','b','h','k','cos','sin'),('a','b','h','k','sin','cos'),('2*a','2*b','h','k','sin','cos'),('b','a','h','k','cos','sin'),('a','b','-h','-k','cos','sin')]

def check_params(p):
 if set(p)!={'a','b','h','k'} or any(not isinstance(x,int) or isinstance(x,bool) for x in p.values()):raise ValueError('Four integer parameters a,b,h,k required')
 if not(1<=p['a']<=8 and 1<=p['b']<=8 and p['a']!=p['b'] and abs(p['h'])<=6 and abs(p['k'])<=6 and (p['h'] or p['k'])):raise ValueError('Outside documented general-center ellipse domain')

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('Unknown level')
 rng=random.Random(seed);spec=None;raw=bool(profile and profile.startswith('observed:'))
 if raw:
  id=profile.split(':',1)[1];spec=SPECS[id]
  if template not in (None,id) or level!=spec['level']:raise ValueError('Source profile/template/level mismatch')
  template=id
 elif template not in (None,'supplied','graph','oriented_radio','oriented_blank'):raise ValueError('Unsupported normal template')
 if not raw:
  template=template or ('supplied' if level=='easy' else 'graph' if level=='moderate' else ('oriented_'+field_type if field_type in ('radio','blank') else rng.choice(['oriented_radio','oriented_blank'])))
  if template not in {'easy':['supplied'],'moderate':['graph'],'hard':['oriented_radio','oriented_blank']}[level]:raise ValueError('Template workload does not belong to level')
  profile=profile or ('authored-orientation' if level=='hard' else 'authored-locus')
  if profile!=('authored-orientation' if level=='hard' else 'authored-locus'):raise ValueError('Unsupported profile')
 p=dict(parameters) if parameters is not None else dict(spec['parameters']) if raw else None
 if p is None:
  while True:
   p={x:rng.randint(1,8) if x in ('a','b') else rng.randint(-6,6) for x in ('a','b','h','k')}
   try:check_params(p);break
   except ValueError:pass
 check_params(p);a,b,h,k=[p[x] for x in ('a','b','h','k')];slots={'{CENTER}':f'({h},{k})','{START}':f'({h+a},{k})','{A}':str(a),'{B}':str(b)}
 def mask(s):
  for old,new in slots.items():s=s.replace(old,new)
  return s
 oriented=level=='hard';plot=None;definitions=[]
 if raw:
  plot=render_plot(p,oriented,spec);prompt=mask(spec['prompt']).replace('{PLOT}',plot);solution=spec['solution']
  if solution:solution=mask(solution).replace('{FINAL}',answer(BANK[0],p,spec['final_style']))
  for f in spec['fields']:
   vs=[answer(r,p,st) for r,st in zip(f['recipes'],f['styles'])];definitions.append((f['key'],f['type'],vs,f['correct_index']))
 else:
  if level=='moderate' or level=='hard':plot=render_plot(p,oriented)
  if level=='moderate':prompt=f'![]({plot})\n\nWhich of the following sets of parametric equations, defined for $\\theta \\in [0,2\\pi ),$ generate the ellipse shown above?'
  else:
   prompt=(f'![]({plot})\n\n' if plot else '')+f'Consider the ellipse centered at $({h},{k})$ with horizontal radius ${a}$ and vertical radius ${b}.$ '
   if level=='easy':prompt+='Which of the following sets of parametric equations, defined for $\\theta \\in [0,2\\pi ),$ generate the ellipse?'
   else:prompt+=('Construct a set' if template=='oriented_blank' else 'Which of the following sets')+f' of parametric equations, defined for $\\theta \\in [0,2\\pi ),$ '+('that traverse' if template=='oriented_blank' else 'traverse')+f' the ellipse once in the counterclockwise direction starting at the point $A({h+a},{k})'+('.$' if template=='oriented_blank' else '?$')
  solution=GENERAL+'\n\n'+(ORIENTATION+'\n\n' if oriented else '')+f'In our case, the ellipse is centered at the point $({h},{k}),$ $a={a}$ and $b={b}.$ Therefore, the parametric equations of the ellipse are\n\n$$\n'+answer(BANK[0],p)+r',\,\theta \in [0,2\pi ).'+'\n$$'
  if template=='oriented_blank':
   prompt+='\n\n$x=$ {{field-1}}$,\\,y=$ {{field-2}}$,\\,\\theta \\in [0,2\\pi ).$';definitions=[('field-1',':answer-field.type/blank',[expr(a,'cos',h)],0),('field-2',':answer-field.type/blank',[expr(b,'sin',k)],0)]
  else:definitions=[('selection',':answer-field.type/radio',[answer(r,p) for r in (HARD_BANK if oriented else BANK)],0)]
 if field_type and any(t.rsplit('/',1)[1]!=field_type for _,t,_,_ in definitions):raise ValueError('Unsupported field type')
 for _,typ,vs,_ in definitions:
  if typ.endswith('/radio'):require_bank(vs,p,oriented)
  if len(vs)!=len(set(vs)):raise ValueError('Whole bank collision')
 content=digest([VERSION,level if not(raw and spec['unrated']) else None,prompt,solution,[(k,t,sorted(vs),vs[ci] if ci is not None else None) for k,t,vs,ci in definitions]])
 fields=[]
 for i,(key,typ,values,ci) in enumerate(definitions):
  fid=uid([content,key,i]);choices=[{':answer/id':uid([fid,v]),':answer/type':':answer.type/math',':answer/value':v} for v in values]
  f={':answer-field/id':fid,':answer-field/key':key,':answer-field/type':typ,':answer-field/choices':choices}
  if ci is not None:f[':answer-field/correct']=[':answer/id',choices[ci][':answer/id']]
  if typ.endswith('/radio'):rng.shuffle(choices)
  fields.append(f)
 q={':question/id':uid(content),':question/problem':prompt,':question/answer-fields':fields}
 if not(raw and spec['unrated']):q[':question/difficulty']=':question.difficulty/'+level
 if solution is not None:q[':question/worked-solution']=solution
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'template':template,'profile':profile,'bank_profile':profile,'parameters':p,'seed':seed,'source':{'database':'math','basis':1356,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'},'mathematical_fingerprint':digest([p,'rightmost-CCW' if oriented else 'locus','given' if level in ('easy','hard') else 'graph']),'evidence_only':raw,'eligible_for_learning':not raw,'python':sys.version.split()[0],'sympy':sp.__version__,'plot':plot}}

# Easy: authored missing-level direct substitution of supplied center/radii.
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
# Moderate: observed graph reading of center and both semiaxes.
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
# Hard: observed supplied-data traversal/start criterion; radio or two blanks.
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)

def markdown(r):
 q=r['question'];meta=r['generation'];s='### '+('ORIGINAL SOURCE EVIDENCE / parameterized replay' if meta['evidence_only'] else 'GENERATED')+' — '+q.get(':question/difficulty','unrated (raw capture)')+('; authored easy level' if not meta['evidence_only'] and q[':question/difficulty'].endswith('/easy') else '; source-supported level and authored bank' if not meta['evidence_only'] else '')+'\n\n'+q[':question/problem']+'\n\n'
 for f in q.get(':question/answer-fields',[]):
  s+=f[':answer-field/key']+':\n'+''.join('- $'+a[':answer/value']+'$'+(' (correct)' if a[':answer/id']==f.get(':answer-field/correct',[None,None])[1] else '')+'\n' for a in f[':answer-field/choices'])
 text=s+'\n'+q.get(':question/worked-solution','[Source worked solution absent]')
 return re.sub(r'!\[\]\((images/[^)]+)\)',lambda m:'![]('+str(Path('/media/jake/SSD/EDB/math')/m[1])+')',text)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args();records=[generate(l,args.seed+i,template=args.template,profile=args.profile) for l in (['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]) for i in range(args.count)];print(json.dumps(records,ensure_ascii=False,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(x) for x in records))
