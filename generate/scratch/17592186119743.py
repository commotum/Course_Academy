#!/usr/bin/env python3
"""Arc-length integral setup, steps 3–7 only; never integrates or writes EDB.

Eight observed templates, nine observed banks including one legacy bank. Normal
banks are authored complete method-derived banks. Replay profiles generalize
all observed shapes without claiming recovery of underdetermined error intent.
Hard is explicitly authored: three differentiated components with bounded
product/chain rules and cancellation of paired trig squares, stopping at setup.
See the adjacent evidence folder for classification, extraction and validation.
"""
import argparse, hashlib, json, platform, random, subprocess, tempfile, uuid
from pathlib import Path
import sympy as s
KP_ID=17592186119743
KP_UUID='4fc0992a-423e-5023-98d5-9d53c3b77788'
TITLE='Finding an Integral Expression For the Arc Length of a Curve'
VERSION='arc-setup-1'
HERE=Path(__file__).resolve().with_suffix('')
t=s.Symbol('t',real=True)
TEMPLATES={
 'trig2':('easy','q-33728','g',False), 'exp_basis':('easy','q-33862','f',True),
 'trig3':('easy','q-127419','f',False), 'paired_exp':('moderate','q-127427','f',False),
 'quad_helix':('easy','q-33857','f',False), 'spiral':('moderate','q-33706','g',False),
 'helix_basis':('easy','q-64723','h',True), 'power_basis':('easy','q-64724','r',True),
 'exp_rotating':('hard',None,'r',False)}
ORIGINAL={
 'trig2':dict(a=1,b=1,n=2,m=3,lo='0',hi='pi'),
 'exp_basis':dict(a=1,b=2,c=1,lo='1',hi='2'),
 'trig3':dict(a=4,b=3,lo='pi/6',hi='pi/4'),
 'paired_exp':dict(a=1,n=1,c=1,k=1,lo='-1',hi='1'),
 'quad_helix':dict(a=1,n=2,c=1,lo='0',hi='1'),
 'spiral':dict(a=1,n=1,h=2,lo='0',hi='pi'),
 'helix_basis':dict(a=1,n=1,c=1,lo='0',hi='2*pi'),
 'power_basis':dict(a=1,b=3,c=1,p=3,q=4,lo='2',hi='5'),
 'exp_rotating':dict(a=1,b=2,c=1,k=1,n=1,lo='0',hi='1')}
PLOT_TEMPLATES={'trig2','spiral','helix_basis'}
def tex(x):return s.latex(s.sympify(x),fold_short_frac=False)
def add(*xs):return s.Add(*xs,evaluate=False)
def mul(*xs):return s.Mul(*xs,evaluate=False)
def sq(x):return s.Pow(x,2,evaluate=False)
def root(x):return s.Pow(x,s.Rational(1,2),evaluate=False)
def normsum(xs):return add(*(sq(x) for x in xs))
def vector(xs,basis=False):
 if not basis:return r'\langle '+r',\,'.join(tex(x) if not isinstance(x,str) else x for x in xs)+r'\rangle'
 return '+'.join('('+ (tex(x) if not isinstance(x,str) else x)+r')\,'+u for x,u in zip(xs,('i','j','k')))
def integral(v,lo,hi):return r'\int_{'+tex(lo)+'}^{'+tex(hi)+'}'+tex(v)+r'\,\mathrm{d}t'
def aligned(rows):return '$$\n'+r'\begin{aligned}'+r' \\ '.join(l+' & ='+v for l,v in rows)+r'\end{aligned}'+'\n$$'
def canonical(x):return s.srepr(s.trigsimp(s.expand(x)))
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def uid(x):return str(uuid.uuid5(uuid.NAMESPACE_URL,x))

def components(template,p):
 a=p['a'];n=p.get('n',1);b=p.get('b',1);c=p.get('c',1);k=p.get('k',1)
 if template=='trig2':return [a*s.sin(n*t),b*s.cos(p['m']*t)]
 if template=='exp_basis':return [a*s.exp(t),b*s.exp(t),c*t*s.exp(t)]
 if template=='trig3':return [a*s.cos(t),b*s.sin(t),a*s.sin(t)]
 if template=='paired_exp':return [a*(s.cos(n*t)+s.sin(n*t)),c*s.exp(k*t),a*(s.sin(n*t)-s.cos(n*t))]
 if template=='quad_helix':return [a*s.sin(n*t),a*s.cos(n*t),c*t**2]
 if template=='spiral':return [a*t*s.sin(n*t),p['h']-a*t*s.cos(n*t)]
 if template=='helix_basis':return [a*s.cos(n*t),a*s.sin(n*t),c*t]
 if template=='power_basis':return [a*t**p['p'],b*t,c*t**p['q']]
 if template=='exp_rotating':return [s.exp(k*t)*(a*s.cos(n*t)+b*s.sin(n*t)),c*t*s.exp(k*t),s.exp(k*t)*(a*s.sin(n*t)-b*s.cos(n*t))]
 raise ValueError('Unknown template')

def mathematics(template,p):
 xs=components(template,p);ds=[s.diff(x,t) for x in xs];a=p['a'];b=p.get('b',1);c=p.get('c',1);n=p.get('n',1);k=p.get('k',1)
 expanded=add(*(s.expand(d*d) for d in ds))
 stages=[root(normsum(ds))]
 if template in ('trig2','power_basis'):stages+=[root(expanded)]
 elif template=='exp_basis':
  stages+=[root(add(a*a*s.exp(2*t),b*b*s.exp(2*t),mul(c*c*s.exp(2*t),add(t*t,2*t,1)))),root(mul(s.exp(2*t),add(a*a,b*b,c*c*t*t,2*c*c*t,c*c))),s.exp(t)*root(c*c*t*t+2*c*c*t+a*a+b*b+c*c)]
 elif template=='trig3':stages+=[root(expanded),root(add(mul(a*a,add(s.sin(t)**2,s.cos(t)**2)),b*b*s.cos(t)**2)),root(a*a+b*b*s.cos(t)**2)]
 elif template=='paired_exp':stages+=[root(expanded),root(add(c*c*k*k*s.exp(2*k*t),mul(2*a*a*n*n,add(s.cos(n*t)**2,s.sin(n*t)**2)))),root(c*c*k*k*s.exp(2*k*t)+2*a*a*n*n)]
 elif template=='quad_helix':stages+=[root(expanded),root(mul(a*a*n*n,add(s.cos(n*t)**2,s.sin(n*t)**2,s.Rational(4*c*c,a*a*n*n)*t*t))),root(a*a*n*n+4*c*c*t*t)]
 elif template=='spiral':stages+=[root(expanded),root(a*a*(1+n*n*t*t))]
 elif template=='helix_basis':stages+=[root(expanded),root(a*a*n*n+c*c)]
 elif template=='exp_rotating':stages+=[root(expanded),root(mul(s.exp(2*k*t),add((k*k+n*n)*(a*a+b*b),c*c*(k*t+1)**2))),s.exp(k*t)*root((k*k+n*n)*(a*a+b*b)+c*c*(k*t+1)**2)]
 speed=s.factor_terms(stages[-1]);return xs,ds,stages,speed

# Complete source profiles: every formula includes its bounds and differential.
# Intent of unexplained scalar changes is unresolved: explicit replay only.
def source_bank(template,p,legacy=False):
 a=p['a'];b=p.get('b',1);c=p.get('c',1);n=p.get('n',1);m=p.get('m',1);k=p.get('k',1)
 lo=s.sympify(p['lo']);hi=s.sympify(p['hi']);C=s.cos(n*t);S=s.sin(n*t)
 def I(x,l=lo,h=hi):return (x,l,h)
 correct=I(mathematics(template,p)[-1])
 if template=='trig2':return [I(root(a*a*n*C*C+b*b*m*m*s.sin(m*t)**2)),I(root(a*a*n*n*S*S+b*b*m*m*s.cos(m*t)**2)),correct,I(root(a*a*n*C*C+b*b*m*s.sin(m*t)**2),lo,1),I(root(a*a*n*S*S+b*b*m*m*s.cos(m*t)**2),lo,1)]
 if template=='exp_basis':
  common=c*c*(t*t+2*t);return [I(s.exp(t)*root(common+a*a+b*b)),I(s.exp(t)*root(common+2*c*c),lo-1,hi-1),I(s.exp(t)*root(common+b*b)),correct,I(s.exp(t)*(c*t+b),lo-1,hi-1)]
 if template=='trig3':return [I(root(a*a*s.cos(t)**2+b*b)),I(root(b*s.cos(t)**2+a)),I(root(b*b*s.sin(t)**2+a*a)),I(root(a*s.sin(t)**2+b)),correct]
 if template=='paired_exp':return [correct,I(root(2*c*s.exp(k*t)+a*a*n*n)),I(2*root(c*s.exp(k*t)+2*a*a*n*n)),I(2*root(2*c*c*k*k*s.exp(2*k*t)+a*a*n*n)),I(root(c*c*k*k*s.exp(2*k*t)+a*a*n*n))]
 if template=='quad_helix':return [I(root(a*a+4*c*c*t*t)),I(root(n)*root(a*a+c*c*t*t)),I(root(a*a+c*c*t*t)),correct,I(n*root(a*a*(s.cos(n*t)**2-s.sin(n*t)**2)+c*c*t*t))]
 if template=='spiral':return [correct,I(s.sqrt(2)*a*(s.sin(n*t)+n*t*s.cos(n*t))),I(root(a*a*(n*n*t*t+2*n*t*s.sin(2*n*t)))),I(root(a*a*(1+2*n*n*t*t))),I(root(a*a*(2+n*n*t*t)))]
 if template=='helix_basis':return [I(root(2*a*a*n*n*s.sin(n*t)**2+a*a*n*n*s.cos(n*t)**2)),I(root(3*a*a*n*n-a*a*n*n*s.sin(n*t)**2),lo,hi/2),I(root(a*a*n*n+c*c+a*a*n*n*s.sin(n*t)**2)),I(root(a*a*n*n+c*c+a*a*n*n*s.cos(n*t)**2)),correct]
 if template=='power_basis':
  u=a*p['p']*t**(p['p']-1);v=c*p['q']*t**(p['q']-1)
  return [correct,I(root(a*a*t**(2*p['p']-2)+c*c*t**(2*p['q']-2)+b*b)),I(root(2*c*p['q']*t**(2*p['q']-3)+a*p['p']**2*t**(2*p['p']-3)+2*b)),I(root(v*v+b*b),0,hi),I(root(u*u+v*v))]
 raise ValueError('No observed profile')

def sample(template,r):
 p=ORIGINAL[template].copy()
 for key in p:
  if key in ('a','b','c'):p[key]=r.randint(1,4 if TEMPLATES[template][0]!='hard' else 3)
  if key in ('n','m','k'):p[key]=r.randint(1,3)
 if template=='trig2' and p['n']==p['m']:p['m']=p['n']%3+1
 if template=='trig3' and p['a']==p['b']:p['b']=p['a']%4+1
 if template=='spiral':p['h']=r.randint(-3,3)
 if template=='power_basis':p['p'],p['q']=r.choice(((2,3),(3,4),(2,4)))
 if template=='exp_rotating' and p['k']*p['b']==p['n']*p['a']:p['b']=r.choice([b for b in (1,2,3) if p['k']*b!=p['n']*p['a']])
 return p

def validate_parameters(template,p):
 if set(p)!=set(ORIGINAL[template]):raise ValueError('Exact complete parameter keys required')
 for key in set(p)-{'lo','hi','h'}:
  bound=3 if TEMPLATES[template][0]=='hard' or key in ('n','m','k') else 4
  if type(p[key]) is not int or not 1<=p[key]<=bound:raise ValueError('Coefficient/degree bound: '+key)
 if 'h'in p and (type(p['h']) is not int or abs(p['h'])>3):raise ValueError('Shift bound')
 if template=='power_basis' and (p['p'],p['q']) not in ((2,3),(3,4),(2,4)):raise ValueError('Power workload bound')
 if template=='exp_rotating' and p['k']*p['b']==p['n']*p['a']:raise ValueError('Hard derivative workload requires both paired trig coefficients nonzero')
 lo=s.sympify(p['lo']);hi=s.sympify(p['hi'])
 if lo.has(s.Float) or hi.has(s.Float) or lo.free_symbols or hi.free_symbols or not -2<=float(lo)<float(hi)<=7:raise ValueError('Ordered exact bounded interval required')


def render_plots(template,p,xs):
 if template not in PLOT_TEMPLATES:return {}
 key=digest({'template':template,'parameters':p});path=HERE/'plots'/(key+'.png');side=path.with_suffix('.json')
 if not path.exists() or not side.exists():
  path.parent.mkdir(exist_ok=True)
  data={'template':template,'parameters':p,'components':[str(x) for x in xs],'endpoint_tex':[tex(s.sympify(p['lo'])),tex(s.sympify(p['hi']))],'output':str(path)}
  with tempfile.NamedTemporaryFile(mode='w',suffix='.json',prefix='arc-plot-',dir=HERE,delete=False) as f:json.dump(data,f);name=f.name
  try:subprocess.run([str(Path('/home/jake/.local/share/uv/python/cpython-3.10.13-linux-x86_64-gnu/bin/python3.10')),str(HERE/'render_plot.py'),name],check=True,capture_output=True)
  finally:Path(name).unlink(missing_ok=True)
 return {'prompt':str(path),'sidecar':str(side),'renderer':'Matplotlib'}


def build_solution(template,p,xs,ds,stages,speed):
 level,source,name,basis=TEMPLATES[template];lo=s.sympify(p['lo']);hi=s.sympify(p['hi'])
 derivative_slots=[r'\frac{\mathrm{d}}{\mathrm{d}t}('+tex(x)+')' for x in xs]
 # Preserve observed product-rule unsimplified derivative row.
 shown=ds.copy()
 if template=='exp_basis':shown[-1]=add(p['c']*t*s.exp(t),p['c']*s.exp(t))
 rows=[(name+"'(t)",vector(derivative_slots,basis)),('',vector(shown,basis)),(r'\|'+name+r"'(t)\|",tex(stages[0]))]+[('',tex(x)) for x in stages[1:]]
 first='First, we find $'+name+"'(t)$ and $\\|"+name+"'(t)\\|:$"
 colon=template in ('quad_helix','spiral','helix_basis','power_basis')
 conclusion='Therefore, the arc length of the curve is'+(':' if colon else '')
 generic=r'\int_{'+tex(lo)+'}^{'+tex(hi)+r'}\|'+name+r"'(t)\|\,\mathrm{d}t"
 if template=='spiral':end=aligned([('L',generic+'='+integral(speed,lo,hi))])
 elif template in ('quad_helix','helix_basis','power_basis'):end=aligned([('L',generic+'='+integral(speed,lo,hi))])
 else:end=aligned([('L',generic),('',integral(speed,lo,hi)+'.')])
 return first+'\n\n'+aligned(rows)+'\n\n'+conclusion+'\n\n'+end

# Easy/moderate/hard sections expose one common exact construction path.
def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if field_type not in (None,'radio'):raise ValueError('Observed layout is radio')
 if profile and profile.startswith('observed:'):
  implied=profile.split(':')[1];template=template or implied
 if template is None:template=random.Random(seed).choice([x for x,v in TEMPLATES.items() if v[0]==level])
 if template not in TEMPLATES or TEMPLATES[template][0]!=level:raise ValueError('Template/level mismatch')
 if profile not in (None,'authored_method','observed:'+template,'observed:trig2:legacy'):raise ValueError('Invalid complete bank profile')
 if profile=='observed:trig2:legacy' and template!='trig2':raise ValueError('Legacy template mismatch')
 if profile=='observed:exp_rotating':raise ValueError('Hard has no source bank')
 profile=profile or 'authored_method';r=random.Random(seed)
 for attempt in range(100):
  p=dict(parameters) if parameters is not None else sample(template,r)
  validate_parameters(template,p);xs,ds,stages,speed=mathematics(template,p)
  lo=s.sympify(p['lo']);hi=s.sympify(p['hi'])
  if profile.startswith('observed:'):bank=source_bank(template,p,profile.endswith('legacy'))
  else:
   R=s.expand(sum(x*x for x in ds));bank=[(speed,lo,hi),(root(sum(x*x for x in xs)),lo,hi),(root(sum(x*x for x in ds[:-1])),lo,hi),(R,lo,hi),(speed,lo,hi+1)]
  canonical_bank=[(canonical(v*v), 'signed' if v.is_nonnegative is not True and not (v.is_Pow and v.exp==s.Rational(1,2)) else 'nonnegative',str(l),str(h)) for v,l,h in bank]
  if len(set(canonical_bank))<5:
   if parameters is not None:raise ValueError('Whole bank rejected: equivalent choices')
   continue
  break
 else:raise ValueError('No eligible complete instance')
 solution=build_solution(template,p,xs,ds,stages,speed);name=TEMPLATES[template][2];basis=TEMPLATES[template][3]
 curve=vector(xs,basis)
 if template=='exp_basis':curve=tex(s.exp(t))+r'\big('+vector([p['a'],p['b'],p['c']*t],True)+r'\big)'
 prompt='Which integral '+(' expression' if template in ('exp_basis','quad_helix','spiral','helix_basis') else 'expression')+' gives the arc length of the curve $'+name+'(t)='+curve+'$'+ ('\nfrom  ' if template in ('quad_helix','spiral') else ' from ')+'$t='+tex(lo)+'$ to $t='+tex(hi)+'?$'
 plots=render_plots(template,p,xs)
 if plots:prompt='![]('+plots['prompt']+')\n\n'+prompt
 # Canonical assessed speed squared + interval excludes bank, layout and shifts.
 fp=digest({'R':canonical(speed**2),'lo':str(lo),'hi':str(hi),'differential':'dt'})
 displayed=[integral(v,l,h) for v,l,h in bank]
 identity=digest({'version':VERSION,'prompt':prompt,'solution':solution,'bank':sorted(displayed),'fingerprint':fp})
 qid=uid(identity);fid=uid(qid+'/selection');answers=[{':answer/id':uid(fid+'/'+value),':answer/type':':answer.type/math',':answer/value':value} for value in displayed]
 target=integral(speed,lo,hi);correct=answers[displayed.index(target)][':answer/id'];r.shuffle(answers)
 record={'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]}]},'generation':{'version':VERSION,'dependencies':{'python':platform.python_version(),'sympy':s.__version__},'seed':seed,'template':template,'bank_profile':profile,'parameters':p,'source_id':TEMPLATES[template][1],'authored_level':level=='hard','mathematical_fingerprint':fp,'content_identity':identity,'source':{'database':'math','basis':1356,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'},'plots':plots,'components':[str(x) for x in xs],'derivatives':[str(x) for x in ds],'speed':str(speed),'stages':[str(x) for x in stages],'bank_objects':[{'speed':str(v),'lower':str(l),'upper':str(h),'differential':'dt'} for v,l,h in bank]}}
 return record

def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)
def markdown(r):
 q=r['question'];f=q[':question/answer-fields'][0]
 return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$'+(' **correct**' if a[':answer/id']==f[':answer-field/correct'][1] else '') for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
if __name__=='__main__':
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--difficulty',choices=['all','easy','moderate','hard'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template',choices=list(TEMPLATES));ap.add_argument('--profile');args=ap.parse_args()
 if args.count<1:ap.error('Positive count required')
 levels=['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]
 records=[generate(level,args.seed+i,template=args.template,profile=args.profile) for level in levels for i in range(args.count)]
 print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
