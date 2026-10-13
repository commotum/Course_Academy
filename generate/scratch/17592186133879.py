#!/usr/bin/env python3
"""Potential reconstruction followed by endpoint subtraction, basis 1356.

12 observed potential/path families; easy is authored, bounded by the canonical
reconstruction example and Calculating Potential Functions prerequisite. No
plots, database APIs or writes. Source prompts/solutions provide prose skeletons,
never answer payloads: every mathematical block is computed through the normal
builder at explicit parameters. Complete observed banks are homogeneous replay
profiles, with unresolved original error intent; normal banks use an explicitly
authored complete set of reconstruction and endpoint operations. Profiles are
selected whole before sampling and any collision rejects the whole instance.

API generate(level, seed=0, template=None, field_type=None, parameters=None,
profile=None), generate_easy/moderate/hard. JSON is local review data only.
"""
from __future__ import annotations
import argparse, hashlib, json, random, re, uuid
from pathlib import Path
import sympy as sp
from functools import lru_cache

KP_ID=17592186133879
KP_UUID='e8a1d966-b4a8-5af8-8b10-063cacea6526'
TITLE='Applying the Fundamental Theorem of Line Integrals When the Potential Function Is Not Given'
VERSION='potential-endpoints-v1'
ROOT=Path(__file__).with_suffix('')
PROVENANCE={'database':'math','basis':1356,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}
x,y,t=sp.symbols('x y t', real=True)
pi=sp.pi; E=sp.E
TEMPLATES={
 'easy_product':('easy',None), 'easy_separable':('easy',None),
 'quartic_trig':('moderate','q-98995'),
 'cubic_exponential':('moderate','q-104725'),
 'exponential_cosine':('moderate','q-104728'),
 'cubic_product':('moderate','q-104731'),
 'separable_cubic':('moderate','q-104733'),
 'cosine_product':('moderate','q-104732'),
 'radial_log':('hard','q-39349'),
 'sine_exponential':('hard','q-104739'),
 'mixed_exponential':('hard','q-104745'),
 'sine_product':('hard','q-104747'),
 'negative_exponential':('hard','q-104761'),
 'cubic_radical_path':('hard','q-104764'),
}
# Exact source parameters, also eligible for normal mathematical builders.
ORIGINAL={
 'quartic_trig':dict(a=1,r=1),
 'cubic_exponential':dict(a=1,b=1,c=2,r=1),
 'exponential_cosine':dict(a=1,h=1,n=2),
 'cubic_product':dict(a=1,b=1,r=2,h=1,u=2),
 'separable_cubic':dict(a=1,b=1,c=1,r=3,u=2),
 'cosine_product':dict(a=1,b=1,r=1,n=1),
 'radial_log':dict(a=1,k=1,h=1),
 'sine_exponential':dict(a=1,b=1,k=1),
 'mixed_exponential':dict(a=1,b=1,k=1),
 'sine_product':dict(a=1,k=1),
 'negative_exponential':dict(a=1,b=1,h=1),
 'cubic_radical_path':dict(a=2,b=1,n=1),
}
# Each restriction preserves its family's source workload. All nonzero signed
# potential coefficients have abs <=3. No zero term may erase a workload.
BOUNDS={
 'easy_product':dict(a=(-3,3),h=(-2,2),k=(-2,2),r=(1,2)),
 'easy_separable':dict(a=(1,3),b=(1,3),h=(-2,2),k=(-2,2),r=(1,2)),
 'quartic_trig':dict(a=(-3,3),r=(1,3)),
 'cubic_exponential':dict(a=(-3,3),b=(-3,3),c=(1,3),r=(1,2)),
 'exponential_cosine':dict(a=(-3,3),h=(1,3),n=(1,2)),
 'cubic_product':dict(a=(-3,3),b=(-3,3),r=(1,3),h=(1,2),u=(1,2)),
 'separable_cubic':dict(a=(-3,3),b=(-3,3),c=(1,3),r=(1,3),u=(2,3)),
 'cosine_product':dict(a=(-3,3),b=(-3,3),r=(1,3),n=(1,3)),
 'radial_log':dict(a=(-3,3),k=(1,3),h=(1,3)),
 'sine_exponential':dict(a=(-3,3),b=(-3,3),k=(1,3)),
 'mixed_exponential':dict(a=(-3,3),b=(-3,3),k=(1,3)),
 'sine_product':dict(a=(-3,3),k=(1,3)),
 'negative_exponential':dict(a=(-3,3),b=(-3,3),h=(1,3)),
 'cubic_radical_path':dict(a=(-3,3),b=(-3,3),n=(1,2)),
}
PROSE=json.loads((ROOT/'prose-templates.json').read_text())

def tex(expr):
 return sp.latex(sp.sympify(expr),ln_notation=True)

def simp(expr):
 return sp.expand_log(sp.simplify(expr),force=True)

def uid(value):
 return str(uuid.uuid5(uuid.NAMESPACE_URL,VERSION+':'+value))

def validate_parameters(template,p,profile):
 if not isinstance(p,dict):raise ValueError('parameters must be a dictionary')
 expected=set(BOUNDS[template])|{'s'}
 if set(p)!=expected:raise ValueError(f'Expected parameter keys {sorted(expected)}')
 for key,v in p.items():
  if type(v) is not int:raise ValueError('integer parameters required')
  lo,hi=(1,3) if key=='s' else BOUNDS[template][key]
  if not lo<=v<=hi:raise ValueError(f'{key} outside [{lo},{hi}]')
  if key in ('a','b','c') and v==0:raise ValueError('workload coefficients must be nonzero')
 if profile=='observed_homogeneous':
  if template not in ORIGINAL or {k:v for k,v in p.items() if k!='s'}!=ORIGINAL[template]:
   raise ValueError('Observed replay fixes path and relative coefficients; only homogeneous scale s varies')
 elif profile!='authored_operations':raise ValueError('Unknown profile')
 elif p['s']!=1:raise ValueError('Authored parameter bounds require s=1; homogeneous scaling belongs to observed replay')

def mathematics(template,p):
 return dict(_mathematics_cached(template,tuple(sorted(p.items()))))

@lru_cache(maxsize=2048)
def _mathematics_cached(template,items):
 p=dict(items)
 a=p['a'];b=p.get('b',1);c=p.get('c',1);r=p.get('r',1);h=p.get('h',1);k=p.get('k',1);n=p.get('n',1);u=p.get('u',1)
 lo=sp.Integer(0);hi=sp.Integer(1)
 if template=='easy_product':f=a*x*y; path=(t+h,r*t+k)
 elif template=='easy_separable':f=(a*x**2+b*y**2)/2;path=(t+h,r*t+k)
 elif template=='quartic_trig':f=a*x**2*y**2/2;path=(r*t+sp.sin(pi*t/2),t+sp.cos(pi*t/2))
 elif template=='cubic_exponential':f=a*x**3*y**3+b*x**2-c*y**2;path=(r*t,sp.exp(t))
 elif template=='exponential_cosine':f=a*sp.exp(x)*sp.cos(y);path=(t**2+h,t);hi=n*pi
 elif template=='cubic_product':f=a*x**2*y-b*x*y;path=(r*t,t**2-h);hi=sp.Integer(u)
 elif template=='separable_cubic':f=(a*x**3+b*y**3)/3-c*x*y;path=(r*sp.log(t),t**2);lo=sp.Integer(1);hi=sp.Integer(u)
 elif template=='cosine_product':f=a*x**2*sp.cos(y)+b*x*y;path=(r*sp.sin(pi*t),pi*t/2);hi=sp.Rational(n,2)
 elif template=='radial_log':f=a*sp.log(k+x**2+y**2)/2;path=(t,t**2*sp.log(t+h))
 elif template=='sine_exponential':f=a*y**2*sp.sin(x)+b*sp.exp(y);path=(t,t**2+k*sp.sin(t)**2);hi=pi
 elif template=='mixed_exponential':f=a*x*sp.exp(y)+b*y*sp.sin(x);path=(t,t+k*sp.cos(t));hi=pi
 elif template=='sine_product':f=a*sp.sin(x)*sp.sin(y);path=(t,sp.exp(sp.sin(t))+k*sp.cos(t));hi=pi/2
 elif template=='negative_exponential':f=a*x**2*sp.exp(-y)+b*y**2;path=(t,sp.log(t-h));lo=sp.Integer(h+1);hi=sp.Integer(h+2)
 elif template=='cubic_radical_path':f=a*x**3-b*x*y;path=(t,t**2-sp.exp(sp.sqrt(t+n*n)));hi=sp.Integer(2*n+1)
 else:raise ValueError('Unknown template')
 f=p['s']*f
 P=sp.diff(f,x);Q=sp.diff(f,y)
 start=tuple(simp(v.subs(t,lo)) for v in path);end=tuple(simp(v.subs(t,hi)) for v in path)
 fa=simp(f.subs({x:start[0],y:start[1]},simultaneous=True));fb=simp(f.subs({x:end[0],y:end[1]},simultaneous=True))
 return dict(f=f,P=P,Q=Q,path=path,lo=lo,hi=hi,start=start,end=end,fa=fa,fb=fb,I=simp(fb-fa),cross=sp.diff(P,y))

def observed_bank(template,m,p):
 """Complete source-shaped formulas, not claims about the original error code.

 Relative parameters fixed by profile; homogeneous scale applies to every value.
 Wrong values are expressed through source method quantities/constants. This is
 evidence replay, never the default sampler, and is not used to claim variety.
 """
 L=sp.log(2);e=E;I=m['I']/p['s']
 banks={
 'quartic_trig':[4,6,sp.Rational(1,2),1,I],
 'cubic_exponential':[e**2+e**2+1,0,e**3+e**2,I,1+e**2],
 'exponential_cosine':[sp.exp(pi**2+1),I,sp.exp(4*pi),0,e*(sp.exp(2*pi)-1)],
 'cubic_product':[12,48,0,I,24],
 'separable_cubic':[I,L**2+9,L**3-63,L**3+L-9,0],
 'cosine_product':[I,(2*sp.sqrt(2)-pi)/2,sp.sqrt(2)/2,0,sp.sqrt(2)/2+1],
 'radial_log':[sp.log(2+L)/2,sp.log(1+L**2)/2,sp.log(4)/2,sp.log(2)/2,I],
 'sine_exponential':[I,sp.exp(pi-1),pi**2,e**2+pi,0],
 'mixed_exponential':[sp.exp(pi)+1,sp.exp(pi**2-1),I,2*pi,pi**2+1],
 'sine_product':[sp.sin(2)*sp.sin(e-1),sp.sin(e)-sp.sin(2),I,2*sp.sin(e)-1,sp.sin(2*e)-sp.sin(e**2)],
 'negative_exponential':[1-L,I,1+sp.log(3)**2,L**2/3,sp.Rational(1,2)+sp.log(3)],
 'cubic_radical_path':[3*e**2-1,3*(e+3),e**2+27,9*(3*e-1),I],
 }
 # All profiles scale an entire field/potential, a real assessed change. Their
 # constants are contextual source-shape evidence, not fitted perturbations.
 return [simp(p['s']*sp.sympify(v)) for v in banks[template]]

def vector(v):return r'\langle '+','.join(tex(e) for e in v)+r'\rangle'
def coord(v):return '('+','.join(tex(e) for e in v)+')'
def aligned(rows):return r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}'
def fieldmath(m,underbrace=False):
 if underbrace:return r'F(x,y)=\underbrace{\left('+tex(m['P'])+r'\right)}_{P(x,y)}\,i+\underbrace{\left('+tex(m['Q'])+r'\right)}_{Q(x,y)}\,j.'
 return r'F(x,y)=\left('+tex(m['P'])+r'\right)\,i+\left('+tex(m['Q'])+r'\right)\,j'
def pathmath(m):return 'r(t)='+vector(m['path'])+r',\,t\in ['+tex(m['lo'])+','+tex(m['hi'])+'].'
def theorem():return r'\int_C\nabla f\cdot\mathrm{d}r=f(r(b))-f(r(a)).'
def substitution(f,v):
 # Mathematical nodes, never text replacement. Protects products, function args,
 # basis-vector labels and TeX commands; parentheses preserve signed powers.
 return sp.latex(f,ln_notation=True,symbol_names={x:r'\left('+tex(v[0])+r'\right)',y:r'\left('+tex(v[1])+r'\right)'})
def ordered_terms(template,p):
 a=p['a'];b=p.get('b',1);c=p.get('c',1);k=p.get('k',1)
 terms={
  'easy_product':[a*x*y], 'easy_separable':[a*x**2/2,b*y**2/2],
  'quartic_trig':[a*x**2*y**2/2],
  'cubic_exponential':[a*x**3*y**3,b*x**2,-c*y**2],
  'exponential_cosine':[a*sp.exp(x)*sp.cos(y)],
  'cubic_product':[a*x**2*y,-b*x*y],
  'separable_cubic':[a*x**3/3,b*y**3/3,-c*x*y],
  'cosine_product':[a*x**2*sp.cos(y),b*x*y],
  'radial_log':[a*sp.log(k+x**2+y**2)/2],
  'sine_exponential':[a*y**2*sp.sin(x),b*sp.exp(y)],
  'mixed_exponential':[a*x*sp.exp(y),b*y*sp.sin(x)],
  'sine_product':[a*sp.sin(x)*sp.sin(y)],
  'negative_exponential':[a*x**2*sp.exp(-y),b*y**2],
  'cubic_radical_path':[a*x**3,-b*x*y],
 }
 return [p['s']*v for v in terms[template]]

def signed_sum(values,keep_zero=False):
 parts=[]
 for value in values:
  if value==0 and not keep_zero:continue
  part=tex(value)
  parts.append(('+' if parts and not part.startswith('-') else '')+part)
 return ''.join(parts) or '0'

def finalmath(template,m,p):
 terms=ordered_terms(template,p)
 # Keep complete substitution products in source order, then simplify each term
 # separately, never collapse evaluated endpoint arithmetic into the answer.
 end_terms=[simp(v.subs({x:m['end'][0],y:m['end'][1]},simultaneous=True)) for v in terms]
 start_terms=[simp(v.subs({x:m['start'][0],y:m['start'][1]},simultaneous=True)) for v in terms]
 sub_end=signed_sum([0]) if not terms else ''.join(('+' if i and not substitution(v,m['end']).startswith('-') else '')+substitution(v,m['end']) for i,v in enumerate(terms))
 sub_start=''.join(('+' if i and not substitution(v,m['start']).startswith('-') else '')+substitution(v,m['start']) for i,v in enumerate(terms))
 # Source single-term polynomial/log/exp products subtract without redundant
 # outer endpoint parentheses; multicomponent potentials preserve grouping.
 if template in ('quartic_trig','radial_log','exponential_cosine'):
  subst=sub_end+'-'+(r'\left('+sub_start+r'\right)' if sub_start.startswith('-') else sub_start)
 else:subst=r'\left('+sub_end+r'\right)-\left('+sub_start+r'\right)'
 if template in ('quartic_trig','radial_log','exponential_cosine'):
  stage=tex(m['fb'])+'-'+r'\left('+tex(m['fa'])+r'\right)'
 elif template=='sine_exponential':
  stage=r'\left('+signed_sum(end_terms,True)+r'\right)-\left('+signed_sum(start_terms,True)+r'\right)'
 elif template=='mixed_exponential':
  stage=r'\left('+signed_sum(end_terms,True)+r'\right)-\left('+tex(m['fa'])+r'\right)'
 elif template=='sine_product':
  factor=tex(p['s']*p['a'])+r'\cdot ' if p['s']*p['a']!=1 else ''
  stage=factor+tex(sp.sin(m['end'][0]))+r'\cdot '+tex(sp.sin(m['end'][1]))+'-'+factor+tex(sp.sin(m['start'][0]))+r'\cdot '+tex(sp.sin(m['start'][1]))
 elif template=='cubic_radical_path':
  u=m['end'][0];n=p['n'];scale=p['s'];a=p['a'];b=p['b']
  pieces=[scale*a*u**3,-scale*b*u**3,scale*b*u*sp.exp(n+1)]
  stage=r'\left('+signed_sum(pieces)+r'\right)-\left('+tex(m['fa'])+r'\right)'
 else:stage=signed_sum(end_terms+[-v for v in start_terms])
 if template=='exponential_cosine':
  final=p['s']*p['a']*sp.exp(p['h'])*((-1)**p['n']*sp.exp((p['n']*pi)**2)-1)
 else:final=sp.factor(m['I']) if template=='cubic_radical_path' else sp.together(m['I']) if template=='cosine_product' else m['I']
 lines=[r'\int_C F\cdot\mathrm{d}r & =\int_C\nabla f\cdot\mathrm{d}r',
 ' & =f'+coord(m['end'])+'-f'+coord(m['start']), ' & ='+subst,' & ='+stage]
 if template=='cubic_radical_path':
  collected=signed_sum([p['s']*(p['a']-p['b'])*m['end'][0]**3,p['s']*p['b']*m['end'][0]*sp.exp(p['n']+1)])
  lines+=[' & ='+r'\left('+collected+r'\right)-\left('+tex(m['fa'])+r'\right)']
 lines+=[' & ='+tex(final)+'.']
 return aligned(lines)

def render(template,m,p):
 level,sid=TEMPLATES[template]
 gradient=aligned(['f_x(x,y) & ='+tex(m['P'])+',','f_y(x,y) & ='+tex(m['Q'])+'.'])
 endpoints=aligned(['r('+tex(m['lo'])+') & ='+vector(m['start'])+',','r('+tex(m['hi'])+') & ='+vector(m['end'])+'.'])
 potential='f(x,y)='+tex(m['f'])+'.'
 if sid:
  raw=PROSE[sid]
  blocks=[theorem()]
  if level=='hard':blocks += [fieldmath(m,True),r'\frac{\partial P}{\partial y}=\frac{\partial Q}{\partial x}='+tex(m['cross'])+'.']
  blocks += [gradient,potential]
  if level=='hard':blocks += [pathmath(m)]
  blocks += [endpoints,finalmath(template,m,p)]
  j=iter(blocks)
  solution=re.sub(r'\$\$(.*?)\$\$',lambda _: '$$\n'+next(j)+'\n$$',raw['solution'],flags=re.S)
  assert next(j,None) is None
  # Replace only the complete endpoint-prose sentence, preserving surrounding
  # source prose exactly and repairing the q-104747 endpoint typo.
  solution=re.sub(r'Therefore, the coordinates of the endpoints of the path defined by \$C\$ are .*?\n\n',
     lambda _: 'Therefore, the coordinates of the endpoints of the path defined by $C$ are $'+coord(m['start'])+'$ and $'+coord(m['end'])+'.$\n\n',solution,flags=re.S)
  if level=='moderate':
   prompt='Consider the curve $C,$ defined parametrically as\n\n$$\n'+pathmath(m)+'\n$$\n\nEvaluate ${\\int }_{C}F\\cdot \\text{d}r$ for $'+fieldmath(m)+'.$ \n\n*Hint: You may wish to use the fact that $F$ is conservative.*'
  else:
   curve=tex(m['path'][1].subs(t,x))
   prompt='Consider the vector field $F,$ defined as\n\n$$\n'+fieldmath(m)+'.\n$$\n\nEvaluate ${\\int }_{C}F\\cdot \\text{d}r,$ where $C$ is the curve $y='+curve+'$ for $x\\in ['+tex(m['lo'])+','+tex(m['hi'])+'].$'
  return prompt,solution
 prompt='Consider the curve $C$, defined parametrically as\n\n$$\n'+pathmath(m)+'\n$$\n\nEvaluate $\\int_C F\\cdot\\mathrm{d}r$ for $'+fieldmath(m)+'.$\n\n*Hint: You may wish to use the fact that $F$ is conservative.*'
 opening=re.split(r'\$\$',PROSE['q-98995']['solution'])[0]
 solution=opening+'$$\n'+theorem()+'\n$$\n\nTo apply the fundamental theorem for line integrals, we must first find a potential function $f$ such that $F=\\nabla f.$ Since $F$ is conservative, we must have\n\n$$\n'+gradient+'\n$$\n\nReconstructing the function $f$ from its gradient in the usual way, we get\n\n$$\n'+potential+'\n$$\n\nNote that we set $C=0$ for the arbitrary constant since we can use any function $f$ that satisfies $\\nabla f=F.$\n\nThe position vectors of the endpoints of the curve are given by\n\n$$\n'+endpoints+'\n$$\n\nFinally, applying the fundamental theorem for line integrals, we have\n\n$$\n'+finalmath(template,m,p)+'\n$$'
 return prompt,solution

def sample(template,rng,profile):
 if profile=='observed_homogeneous':return dict(ORIGINAL[template],s=rng.randint(1,3))
 p={k:rng.choice([v for v in range(lo,hi+1) if k not in ('a','b','c') or v!=0]) for k,(lo,hi) in BOUNDS[template].items()}
 p['s']=1 # s retained for replay scaling; authored variety is relative coefficients and endpoints.
 return p

@lru_cache(maxsize=4096)
def distinct_bank(values):
 return all(simp(v-w)!=0 for i,v in enumerate(values) for w in values[:i])

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('Unknown difficulty')
 if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Only observed radio layout supported')
 rng=random.Random(seed)
 if template is None:template=rng.choice([k for k,v in TEMPLATES.items() if v[0]==level])
 if template not in TEMPLATES or TEMPLATES[template][0]!=level:raise ValueError('Template and difficulty mismatch')
 profile=profile or 'authored_operations'
 for attempt in range(200):
  p=dict(parameters) if parameters is not None else sample(template,rng,profile)
  validate_parameters(template,p,profile);m=mathematics(template,p)
  values=observed_bank(template,m,p) if profile=='observed_homogeneous' else [m['I'],-m['I'],2*m['I'],m['I']/2,sp.Integer(0)]
  distinct=distinct_bank(tuple(values))
  if not distinct:
   if parameters is not None:raise ValueError('Whole complete bank rejected for collision')
   continue
  prompt,solution=render(template,m,p)
  bank=[tex(v) for v in values]
  domain='F is smooth on R^2; path interval lies in its real domain.'
  # Assessed task = actual displayed vector field and ordered endpoints. Curve
  # parameters invisible at endpoints never inflate mathematical diversity.
  fingerprint=hashlib.sha256(json.dumps([sp.srepr(m['P']),sp.srepr(m['Q']),[sp.srepr(v) for v in m['start']],[sp.srepr(v) for v in m['end']]],sort_keys=True).encode()).hexdigest()
  identity=hashlib.sha256(json.dumps([VERSION,level,prompt,solution,sorted(bank),domain],sort_keys=True).encode()).hexdigest()
  qid=uid(identity);fid=uid(qid+':selection')
  answers=[{':answer/id':uid(fid+':'+v),':answer/type':':answer.type/math',':answer/value':v} for v in bank]
  correct_idx=next(i for i,v in enumerate(values) if simp(v-m['I'])==0)
  field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',answers[correct_idx][':answer/id']]}
  return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':[field]},'generation':{'version':VERSION,'seed':seed,'template':template,'parameters':p,'bank_profile':profile,'bank_origin':'observed source shapes; homogeneous replay only' if profile=='observed_homogeneous' else 'authored','source_id':TEMPLATES[template][1],'source_analysis':PROVENANCE,'domain':domain,'plot_rating':'none','plot_assets':{},'mathematical_fingerprint':fingerprint,'content_identity':identity,'math':{k:([str(v) for v in val] if isinstance(val,tuple) else str(val)) for k,val in m.items()},'recipes': ['original source-shape expression, scaled homogeneously']*5 if profile=='observed_homogeneous' else ['endpoint difference','reverse endpoints','double reconstructed potential','halve reconstructed potential','use same endpoint twice']}}
 raise ValueError('No eligible whole-bank instance found')

def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)
def markdown(record):
 q=record['question'];f=q[':question/answer-fields'][0]
 return q[':question/problem']+'\n\n'+'\n'.join(f"- ${a[':answer/value']}$" for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
 if args.count<1:ap.error('count must be positive')
 records=[generate(level,args.seed+i,template=args.template,profile=args.profile) for level in (['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]) for i in range(args.count)]
 print(json.dumps(records,ensure_ascii=False,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
if __name__=='__main__':main()
