#!/usr/bin/env python3
"""Whole-field identification by equation type; steps 3–7, math basis 1356.

Observed complete image banks are explicit empirical-geometry replay profiles.
Their unknown distractor authoring intent is not promoted to normal generation.
Normal banks are complete authored symbolic fields; all images use identical
Matplotlib styling, bounds and sampling. No differential equation is solved.
The categorical assessed task domain is finite: possible/both (1), impossible
x-invariant or y-invariant (2). Coefficients and source aliases do not inflate it.

Use .venv/bin/python; the plot subprocess uses frozen read-only cached MPL.
API generate(level, seed=0, template=None, field_type=None, parameters=None,
profile=None), plus generate_easy/moderate/hard. Explicit inputs never resample.
"""
from __future__ import annotations
import argparse,hashlib,json,random,re,subprocess,tempfile,uuid,os,math
from pathlib import Path
import sympy as sp
KP_ID=17592186172040
KP_UUID='a2334101-5266-5853-aedf-04c85746b5cc'
TITLE='Identifying a Possible Slope Field Based on the Type of Equation'
VERSION='whole-field-type-v1'
HERE=Path(__file__).resolve().parent/str(KP_ID)
X,Y=sp.symbols('x y',real=True)
SOURCE=json.loads((HERE/'source.json').read_text())
QS={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
GEOMETRY=json.loads((HERE/'source-geometry.json').read_text())
RENDERER='/home/jake/.local/share/uv/python/cpython-3.10.13-linux-x86_64-gnu/bin/python3.10'
PROVENANCE=json.loads((HERE/'render-provenance.json').read_text())
FREEZE=json.loads((HERE/'renderer-freeze.json').read_text())
for name,key in [('render.py','renderer_sha256'),('render-provenance.json','provenance_sha256'),('source-geometry.json','source_geometry_sha256')]:
 if hashlib.sha256((HERE/name).read_bytes()).hexdigest()!=FREEZE[key]:raise RuntimeError('Frozen renderer/source geometry changed: '+name)
SPECS={
 'q-96476':('moderate','possible_product','x*y','xy',1),
 'q-119369':('moderate','possible_mixed','y-x**2',r'y-{x}^{2}',4),
 'q-119372':('moderate','possible_exp','exp(x*y)',r'{e}^{xy}',2),
 'q-96477':('hard','impossible_y',None,None,1),
 'q-98229':('hard','impossible_x',None,None,1),
 'q-98233':('hard','impossible_y',None,None,4),
 'q-119383':('hard','impossible_y',None,None,3),
 'q-98231':('hard','impossible_y',None,None,4),
}
TEMPLATES={'easy':['possible_linear'],'moderate':['possible_product','possible_mixed','possible_exp'],'hard':['impossible_x','impossible_y']}

def digest(obj):return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(s):return str(uuid.uuid5(uuid.UUID(KP_UUID),s))
def sym(expr):return sp.sympify(expr,locals={'x':X,'y':Y,'exp':sp.exp})
def depends(expr):
 e=sym(expr);return ('x' if sp.diff(e,X)!=0 else '')+('y' if sp.diff(e,Y)!=0 else '')
def formula(template,p):
 a,b=p['a'],p['b'];
 if template=='possible_linear':return a*X+b*Y+p['c']
 if template=='possible_product':return a*X**p['px']*Y**p['py']
 if template=='possible_mixed':return a*Y+b*X**2 if p['orientation']=='y' else a*X+b*Y**2
 if template=='possible_exp':return sp.exp(a*X*Y)
 return None

def validate_parameters(level,template,p,source_profile=False):
 if source_profile:
  if set(p)!={'scale'} or p['scale'] not in (-1,-.5,.5,1,1.5):raise ValueError('Replay scale must be -1,-.5,.5,1,1.5')
  return
 if set(p)!={'a','b','c','px','py','orientation','single'}:raise ValueError('Expected a,b,c,px,py,orientation,single')
 if any(type(p[k]) is not int for k in ('a','b','c','px','py')):raise ValueError('Normal coefficient/offset/power slots require integers')
 if p['c'] not in (-2,-1,0,1,2) or (level!='easy' and p['c']!=0):raise ValueError('Affine offset c must be integer -2..2; only easy uses it')
 if p['a'] not in (-2,-1,1,2) or p['b'] not in (-2,-1,1,2):raise ValueError('Nonzero a,b must have absolute value 1 or 2')
 if p['px'] not in (1,2) or p['py'] not in (1,2) or p['orientation'] not in ('x','y') or p['single'] not in ('linear','quadratic','exp'):raise ValueError('Invalid finite field family')
 # No easy nonlinear, or new algebraic demand hidden in explicit inputs.
 if level=='easy' and (p['px']!=1 or p['py']!=1 or p['single']!='linear'):raise ValueError('Easy supports linear fields only')

def points(expr,bounds=(-2,2,-2,2)):
 f=sp.lambdify((X,Y),expr,'math');x0,x1,y0,y1=bounds
 return [[x0+(x1-x0)*i/16,y0+(y1-y0)*j/16,float(f(x0+(x1-x0)*i/16,y0+(y1-y0)*j/16))] for j in range(1,16) for i in range(1,16)]

def render_plots(objects):
 """Exact-instance input, unique temp file and atomic PNG/JSON sidecars."""
 out=HERE/'plots';out.mkdir(exist_ok=True);todo=[];result=[]
 for o in objects:
  key=digest({'renderer':PROVENANCE,'version':VERSION,**o});path=out/(key+'.png');result.append(str(path.resolve()))
  if not path.exists() or not path.with_suffix('.json').exists():todo.append({'path':str(path.resolve()),**o})
 if todo:
  with tempfile.NamedTemporaryFile(mode='w',suffix='.json',prefix='render-input-',dir=HERE,delete=False) as f:json.dump(todo,f);tmp=Path(f.name)
  try:subprocess.run([RENDERER,str(HERE/'render.py'),str(tmp)],check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
  finally:tmp.unlink(missing_ok=True)
  for o in todo:
   path=Path(o['path']).with_suffix('.json')
   with tempfile.NamedTemporaryFile(mode='w',dir=out,delete=False,suffix='.json') as f:json.dump({'renderer':PROVENANCE,**o},f,sort_keys=True);temp=Path(f.name)
   os.replace(temp,path)
 return result

def empirical_points(value,dependence,scale):
 # Reconstruction is explicitly empirical, not a recovered symbolic formula.
 # Robust invariant-band projection suppresses raster/PCA fragments that cannot
 # belong to the independently established x-only/y-only source fields.
 cloud=GEOMETRY[value]['segments_normalized']
 if dependence=='xy':
  cells={}
  for u,w,m in cloud:cells.setdefault((round(u*16),round(w*16)),[]).append(math.atan(m))
  # Use a robust observed orientation medoid in each cell; unlike averaging
  # angles this respects unoriented near-vertical segments modulo pi.
  def gap(a,b):
   d=abs(a-b);return min(d,math.pi-d)
  measured={cell:min(angles,key=lambda a:sum(gap(a,b) for b in angles)) for cell,angles in cells.items()}
  return [[-2+i/4,-2+j/4,scale*math.tan(measured[min(measured,key=lambda c:(c[0]-i)**2+(c[1]-j)**2)])] for j in range(1,16) for i in range(1,16)]
 k=0 if dependence=='x' else 1;groups={}
 for p in cloud:groups.setdefault(round(p[k]*16),[]).append(math.atan(p[2]))
 def median(values):
  values=sorted(values);return values[len(values)//2]
 measured={key:median(values) for key,values in groups.items() if len(values)>5}
 if not measured:raise ValueError('Insufficient empirical invariant-band evidence')
 out=[]
 for j in range(1,16):
  for i in range(1,16):
   index=i if k==0 else j;angle=measured[min(measured,key=lambda key:abs(key-index))]
   out.append([-2+i/4,-2+j/4,scale*math.tan(angle)])
 return out

def source_bank(profile,scale):
 q=QS[profile];level,template,expr,tex,correct=SPECS[profile];objects=[];values=[];metadata=[]
 for i,a in enumerate(q[':question/answer-fields'][0][':answer-field/choices']):
  v=a[':answer/value'];g=GEOMETRY[v];dep=('y' if template=='impossible_y' else 'x') if i==correct and level=='hard' else ('xy' if level=='hard' or i==correct else SOURCE_TYPES[profile][i])
  metadata.append({'recipe':'empirical captured slope geometry (intent unresolved)','source_asset':v,'dependence':dep,'source_sha256':g['source_sha256']})
  # Empirical pixel geometry is immutable source evidence. At scale=1 reuse
  # exact captured geometry; changes re-render its complete slope cloud.
  if scale==1:values.append(v)
  else:
   if i==correct and level=='moderate':
    objects.append({'bounds':[-2,2,-2,2],'points':points(sym(expr)*sp.Rational(str(scale)))})
   else:objects.append({'bounds':[-2,2,-2,2],'points':empirical_points(v,dep,scale)})
   values.append(None)
 if objects:
  rendered=iter(render_plots(objects));values=[next(rendered) if v is None else v for v in values]
 return values,metadata,correct
SOURCE_TYPES={'q-96476':['x','xy','y','x','y'],'q-119369':['x','y','y','x','xy'],'q-119372':['x','y','xy','x','y']}

# Fixed worked wording follows observed step sequence; guides select non-axis
# lines so a product's exceptional zero axes cannot misstate dependence.
def solution(template,correct_image,guide_image,source_profile=None):
 possible=template.startswith('possible');single=template.split('_')[-1]
 if possible:
  text='The right-hand side is a function of $x$ and $y.$ This means that the slope varies with both $x$ and $y.$'
  selection='Of the given slope fields, the only one that varies with both $x$ and $y$ is the following:'
  last='To see this more clearly, notice that if we draw a vertical line and a horizontal line, the slopes vary if we move along either of the two lines.'
 else:
  text='The right-hand side is a function of $x$ and $y.$ This means that the slope field varies with both $x$ and $y.$'
  variable,fixed,line=('y','x','vertical') if single=='x' else ('x','y','horizontal')
  selection=f'Of the given slope fields, we note the following slope field does not vary with ${variable}$ given a fixed value of ${fixed}.$'
  last=f'To see this more clearly, notice that if we draw a {line} line, the slopes do not vary.'
 whitespace='  ' if source_profile in ('q-119369','q-119372') else ' '
 return 'Notice that we are given an equation of the form\n\n$$\n'+r'\frac{\text{d}y}{\text{d}x}=f(x,y).'+ '\n$$\n\n'+text+'\n\n'+selection+'\n\n![]('+correct_image+')\n\n'+whitespace+'\n\n'+last+'\n\n![]('+guide_image+')'

# Easy: authored canonical linear instance. Moderate: observed nonlinear
# operators. Hard: observed inverse classification with four both-variable fields.
def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in TEMPLATES:raise ValueError('Invalid level')
 if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Only radio')
 rng=random.Random(seed);observed=profile in SPECS
 if profile is not None and not observed and profile!='authored_method':raise ValueError('Unknown bank profile')
 if observed:
  expected,t,base,base_tex,correct=SPECS[profile]
  if level!=expected or template not in (None,t):raise ValueError('Profile not eligible at this level/template')
  template=t;p={'scale':1} if parameters is None else dict(parameters);validate_parameters(level,template,p,True)
  values,objects,correct=source_bank(profile,p['scale']);expr=sym(base)*sp.Rational(str(p['scale'])) if base else None
  # Structured equation slot, never replacement across unrelated prose.
  if level=='moderate':
   tex=base_tex if p['scale']==1 else sp.latex(expr)
   prompt=r'Which of the following could be the slope field for the differential equation $\frac{\text{d}y}{\text{d}x}='+tex+'?$'
  elif profile=='q-96477':prompt=r'Given that $f(x, y)$ varies with both $x$ and $y$, which of the following **cannot** be the slope field for the differential equation $\frac{dy}{dx} = f(x, y)$?'
  else:prompt=r'Given that $f(x,y)$ varies with both $x$ and $y,$ which of the following **cannot** be the slope field for the differential equation $\frac{\text{d}y}{\text{d}x}=f(x,y)?$'
  guides=re.findall(r'!\[\]\((.*?)\)',QS[profile].get(':question/worked-solution',''))
  if p['scale']==1 and guides:guide=guides[-1]
  else:
   v=QS[profile][':question/answer-fields'][0][':answer-field/choices'][correct][':answer/value'];g=GEOMETRY[v]
   guide_points=points(expr) if level=='moderate' else empirical_points(v,template[-1],p['scale'])
   guide=render_plots([{'bounds':[-2,2,-2,2],'points':guide_points,'guide':'both' if level=='moderate' else template[-1]}])[0]
  bank_profile=profile
 else:
  template=template or rng.choice(TEMPLATES[level])
  if template not in TEMPLATES[level]:raise ValueError('Template outside level')
  p={'a':rng.choice([-2,-1,1,2]),'b':rng.choice([-2,-1,1,2]),'c':rng.choice([-2,-1,0,1,2]) if level=='easy' else 0,'px':rng.choice([1,2]) if level!='easy' else 1,'py':rng.choice([1,2]) if level!='easy' else 1,'orientation':rng.choice(['x','y']),'single':rng.choice(['linear','quadratic','exp']) if level!='easy' else 'linear'} if parameters is None else dict(parameters)
  # Earlier explicit fixtures without c canonicalize to the affine baseline c=0.
  if 'c' not in p:p['c']=0
  validate_parameters(level,template,p);expr=formula(template,p)
  if level!='hard':
   a,b=p['a'],p['b'];fields=([expr,a*X+p['c'],b*Y+p['c'],-a*X+p['c'],-b*Y+p['c']] if level=='easy' else [expr,a*X,b*Y,a*X**2,b*Y**2]);correct=0
   prompt=r'Which of the following could be the slope field for the differential equation $\frac{\text{d}y}{\text{d}x}='+sp.latex(expr)+'?$'
  else:
   a,b=p['a'],p['b'];z=X if template=='impossible_x' else Y
   single=a*z if p['single']=='linear' else (a*z**2 if p['single']=='quadratic' else sp.exp(a*z))
   fields=[a*X+b*Y,a*X*Y,a*Y+b*X**2,sp.exp(a*X*Y),single];correct=4
   prompt=r'Given that $f(x,y)$ varies with both $x$ and $y,$ which of the following **cannot** be the slope field for the differential equation $\frac{\text{d}y}{\text{d}x}=f(x,y)?$'
  # Complete bank rejection: no replacement options or first-valid pool.
  if len(set(map(str,fields)))!=5:raise ValueError('Equivalent bank members')
  deps=[depends(f) for f in fields]
  targets=[i for i,d in enumerate(deps) if (d=='xy')==(level!='hard')]
  if targets!=[correct]:raise ValueError('Ambiguous complete bank')
  objects=[{'expression':str(f),'dependence':depends(f),'recipe':'authored complete equation-type bank'} for f in fields]
  values=render_plots([{'bounds':[-2,2,-2,2],'points':points(f)} for f in fields])
  guide=render_plots([{'bounds':[-2,2,-2,2],'points':points(fields[correct]),'guide':'both' if level!='hard' else template[-1]}])[0]
  bank_profile='authored_method'
 worked=solution(template,values[correct],guide,profile if observed else None)
 # Display parameters and bank geometry are presentation identity; task identity
 # is the finite assessed category, with no incidental coefficient magnitudes.
 mathematical=digest({'demand':'possible_both' if level!='hard' else template,'assessed':'whole-field dependence'})
 identity=digest({'version':VERSION,'prompt':prompt,'solution':worked,'bank':sorted(values)})
 qid=uid(identity);fid=uid(identity+'/selection');answers=[{':answer/id':uid(fid+'/'+v),':answer/type':':answer.type/image',':answer/value':v} for v in values]
 correct_id=answers[correct][':answer/id'];rng.shuffle(answers)
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':worked,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct_id]}]},'generation':{'version':VERSION,'asset_root':str(HERE.resolve()),'seed':seed,'template':template,'parameters':p,'bank_profile':bank_profile,'source':{k:SOURCE[k] for k in ('database','basis','lineage')},'source_id':profile if observed else None,'authored':not observed,'authored_level_assignment':profile=='q-96477' or level=='easy','mathematical_fingerprint':mathematical,'content_identity':identity,'equation':str(expr) if expr is not None else None,'plot_objects':objects,'renderer':PROVENANCE,'renderer_freeze':FREEZE,'domain':'whole plane; shown window [-2,2]² for authored plots','categorical_task_domain':{'possible_both':1,'impossible_invariance':2}}}

def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)

def markdown(r):
 q=r['question'];f=q[':question/answer-fields'][0]
 return q[':question/problem']+'\n\n'+'\n\n'.join('![]('+a[':answer/value']+')' for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
 levels=list(TEMPLATES) if args.difficulty=='all' else [args.difficulty];records=[generate(l,args.seed+i,template=args.template,profile=args.profile) for l in levels for i in range(args.count)]
 print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
