#!/usr/bin/env python3
"""Upward Cartesian graph flux; local review generator, no database writes.

All 12 observed families have coefficient-weighted symbolic recipes. Observed
banks are explicit uniform-scaling shape profiles with unresolved error intent;
authored default banks use whole flux-operation errors. Easy is authored, not an
observed level. Source q-161481 has reversed bounds/empty described domain and is
quarantined to an explicit observed replay profile. Normal presentation repairs
that domain. q-161552 repairs its first substitution vector typo. See evidence.
"""
import argparse, hashlib, json, random, re, uuid
from pathlib import Path
from functools import lru_cache
import sympy as s
KP_ID=17592186198379
KP_UUID='aaa6b152-86d3-5f96-8a94-57f86a17a84d'
TITLE='Evaluating Flux Over a Surface'
VERSION='cartesian-flux-v1'
ROOT=Path(__file__).with_suffix('')
SOURCE=json.loads((ROOT/'source.json').read_text())
SOURCES={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
x,y,z=s.symbols('x y z',real=True)
# Symbols are real; radical family is simplified only on its strictly positive rectangle.
BASE={
'q-160888':(x-y,[z+y,2*y+z,x*y],[0,1,0,2]),
'q-161553':(-x-y,[s.exp(x),s.exp(y),z+1],[0,1,0,1]),
'q-161382':(2*x+y,[-x,-y,x*y*z],[0,1,0,1]),
'q-161435':(x+y,[x*y,x+y,s.exp(z)],[0,1,0,x]),
'q-161481':(s.cos(x+y),[1,0,y],[-s.pi,0,-x,0]),
'q-161536':(s.exp(x),[y,x+z,0],[-1,1,0,1]),
'q-161539':(s.tan(x*y),[s.cos(x*y)**2,s.cos(x*y)**2,1],[0,1,-x,0]),
'q-161541':(2*s.sqrt(x*y),[s.sqrt(x/y),s.sqrt(x/y),z*z+1],[3,4,1,2]),
'q-161542':(1+x*x+y*y,[x+y,y-x,z],[-1,1,-1,1]),
'q-161552':(2*x+y,[3*x**3*y,2*y*z,2*x*(y+z)],[0,2,0,1]),
'q-161447':(y-2*x,[y,x+z,z+2*x],[1,2,0,1]),
'q-161476':(s.exp(x-y),[1/z,x*y/z,z],[0,1,0,x]),
}
# Exact observed whole-bank expression shapes. These are never default error recipes.
OBSERVED={
'q-160888':['3','12','9/2','8','9/4'],
'q-161553':['3*E-2','E-3','2*E-2','2*E-3','E-2'],
'q-161382':['3','3/2','11/6','5/6','2'],
'q-161435':['(4*E**2-8*E)/8','(4*E**2-8*E-1)/8','(8*E-1)/8','(4*E**2-1)/8','(4*E**2+1)/8'],
'q-161481':['pi+pi**2/3','pi-pi**3/6','pi+pi**2/12','pi/4','pi/2'],
'q-161536':['(3*E-exp(-1))/4','(exp(-1)-E)/2','-(5*E+2*exp(-1))/4','(7*E-exp(-1))/2','-(3*E+exp(-1))/2'],
'q-161539':['1/3','pi/2','5/6','pi-1','0'],
'q-161541':['7*(3-log(2))/2','7*(2-log(4))/2','7*(3-log(4))/2','7*(6-log(2))/2','4*(3-log(2))/2'],
'q-161542':['2','4','8/3','0','4/3'],
'q-161552':['-8/3','7/3','-10/3','-2','-8'],
'q-161447':['7/2','5/2','1/2','1','0'],
'q-161476':['E**2-17/8','E**2+E-19/8','E-19/8','E-15/8','E**2-E-13/8'],
}
# Row stages explicitly extracted, keeping omission/duplication of source simplification stages.
STAGES={k:['formula','dot','distributed','iterated','primitive_y','evaluated_y','simplified_y','primitive_x','evaluated_x','answer'] for k in BASE}
for k in ['q-160888','q-161447']:
 STAGES[k]=['formula','dot','distributed','simplified','iterated','primitive_y','evaluated_y','primitive_x','evaluated_x','answer']
STAGES['q-161476']=['formula','dot','distributed','iterated','primitive_y','evaluated_y','primitive_x','evaluated_x','answer']
STAGES['q-161552']=['formula','dot','distributed','iterated','primitive_y','evaluated_y','primitive_x','evaluated_x','answer']
STAGES['q-161536']=['formula','dot','distributed','iterated','primitive_y','evaluated_y','primitive_x','answer']
STAGES['q-161541']=['formula','dot','distributed','simplified','iterated','primitive_y','evaluated_y','simplified_y','primitive_x','answer']
LEVELS={k:SOURCES[k][':question/difficulty'][':db/ident'].rsplit('/',1)[1] for k in BASE}
TEMPLATES={k:{'level':v,'plot':'none','source_ids':[k]} for k,v in LEVELS.items()}
TEMPLATES['easy_affine']={'level':'easy','plot':'none','source_ids':[]}
DEFAULT_BANKS={
'authored_signs':['correct','opposite','flip_P','flip_Q','omit_R'],
'authored_zero_normal':['correct','opposite','R_only','P_only','Q_only'],
'authored_zero_vertical':['correct','opposite','omit_P','R_only','P_only'],
}
def L(a):
 a=s.sympify(a).replace(lambda n:n.func in (s.sinh,s.cosh),lambda n:n.rewrite(s.exp))
 return s.latex(a)
def vec(a):return r'\left\langle '+r',\,'.join(L(v) for v in a)+r'\right\rangle'
@lru_cache(maxsize=16384)
def eq(a,b):return s.simplify(a-b)==0
@lru_cache(maxsize=4096)
def _integral(a,b):return s.simplify(s.integrate(s.integrate(a,(y,b[2],b[3])),(x,b[0],b[1])))
def integral(a,b):return _integral(s.sympify(a),tuple(map(s.sympify,b)))
def primitive(a,v):return s.integrate(a,v)
def bounded(a,v,lo,hi):return s.Add(a.subs(v,hi),-a.subs(v,lo),evaluate=False)
def intx(a,b):return r'\int_{'+L(b[0])+'}^{'+L(b[1])+r'}\left('+L(a)+r'\right)\,\mathrm{d}x'
def it(a,b):return r'\int_{'+L(b[0])+'}^{'+L(b[1])+r'}\int_{'+L(b[2])+'}^{'+L(b[3])+r'}\left('+L(a)+r'\right)\,\mathrm{d}y\,\mathrm{d}x'
def br(a,v,lo,hi):return r'\left['+L(a)+r'\right]_{'+v+'='+L(lo)+'}^{'+v+'='+L(hi)+'}'
def aligned(rows):return r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}'
def model(template,p,profile):return _model(template,tuple(sorted(p.items())),profile)
@lru_cache(maxsize=2048)
def _model(template,p_tuple,profile):
 p=dict(p_tuple)
 if template=='easy_affine':
  g=p['a']*x+p['b']*y+p['c'];F=[p['u']*y,p['v']*x,z+p['w']];b=[0,p['X'],0,p['Y']]
 else:
  g,F,b=BASE[template];F=[s.sympify(v)*p[k] for v,k in zip(F,['p','q','r'])];b=list(b)
  if template=='q-161481' and not profile.startswith('observed_'): b[2],b[3]=0,-x # minimal repair: swap reversed y bounds
 F=list(map(s.sympify,F));sub=[s.simplify(v.subs(z,g)) for v in F];gx=s.diff(g,x);gy=s.diff(g,y)
 terms=[s.expand(-sub[0]*gx),s.expand(-sub[1]*gy),s.expand(sub[2])]
 if template=='q-161541':terms=[-s.Integer(p['p']),-p['q']*x/y,p['r']*(4*x*y+1)]
 terms=[s.trigsimp(s.simplify(v)) for v in terms]
 h=s.simplify(sum(terms));Ay=s.integrate(h,y);ey=bounded(Ay,y,b[2],b[3]);iy=s.simplify(ey);Ax=s.integrate(iy,x);ex=bounded(Ax,x,b[0],b[1]);ans=s.simplify(ex)
 return dict(g=g,F=F,b=b,sub=sub,gx=gx,gy=gy,terms=terms,h=h,Ay=Ay,ey=ey,iy=iy,Ax=Ax,ex=ex,answer=ans)
def parameters_ok(template,p,profile):
 if template=='easy_affine':
  expected={'a','b','c','u','v','w','X','Y'}
  if set(p)!=expected or any(type(v)!=int for v in p.values()):raise ValueError('Exact integer easy parameters required')
  if any(not 1<=abs(p[k])<=2 for k in ['a','b','u','v']) or any(abs(p[k])>2 for k in ['c','w']) or any(not 1<=p[k]<=2 for k in ['X','Y']):raise ValueError('Easy workload bounds exceeded')
 else:
  if set(p)!={'p','q','r'} or any(type(v)!=int or not 1<=abs(v)<=3 for v in p.values()):raise ValueError('Component weights must be nonzero integers of absolute magnitude ≤3')
  if profile.startswith('observed_') and not p['p']==p['q']==p['r']:raise ValueError('Observed expression-shape profiles require uniform scaling; intent unresolved')
def build_bank(m,profile,template,p):
 ans=m['answer'];A,B,C=[integral(t,m['b']) for t in m['terms']]
 if profile.startswith('observed_'):
  if profile!='observed_'+template:raise ValueError('Wrong source profile')
  values=[s.sympify(v)*p['p'] for v in OBSERVED[template]];recipes=['observed_shape_'+str(i) for i in range(5)]
 else:
  if profile not in DEFAULT_BANKS:raise ValueError('Unknown profile')
  recipes=DEFAULT_BANKS[profile];operations={'correct':ans,'opposite':-ans,'flip_P':-A+B+C,'flip_Q':A-B+C,'omit_R':A+B,'omit_P':B+C,'R_only':C,'positive_sum':-A-B+C}
  if 'P_only' in recipes:operations['P_only']=integral(m['sub'][0],m['b'])
  if 'Q_only' in recipes:operations['Q_only']=integral(m['sub'][1],m['b'])
  values=[s.simplify(operations[k]) for k in recipes]
 if len(values)!=5 or any(eq(a,b) for i,a in enumerate(values) for b in values[:i]) or sum(eq(v,ans) for v in values)!=1:raise ValueError('Complete bank rejected: collision/missing correct value')
 return values,recipes

def render(template,m,observed=False):
 g,F,b=m['g'],m['F'],m['b'];sub=m['sub'];gx,gy=m['gx'],m['gy']
 vector=vec(F);flux=r'\iint_S '+vector+r'\cdot\mathrm{d}\mathbf{S}'
 formula=r'\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A'
 dot=r'-\left('+L(sub[0])+r'\right)\left('+L(gx)+r'\right)-\left('+L(sub[1])+r'\right)\left('+L(gy)+r'\right)+\left('+L(sub[2])+r'\right)'
 # Preserve first distributed sum as a full unevaluated sum, so signs cannot vanish.
 distributed=s.Add(*[t for term in m['terms'] for t in s.Add.make_args(term)],evaluate=False)
 stages={
 'formula':flux+' & ='+formula,
 'dot':' & ='+r'\iint_D\left('+dot+r'\right)\,\mathrm{d}A',
 'distributed':' & ='+r'\iint_D\left('+L(distributed)+r'\right)\,\mathrm{d}A',
 'simplified':' & ='+r'\iint_D\left('+L(m['h'])+r'\right)\,\mathrm{d}A',
 'iterated':' & ='+it(m['h'],b),
 'primitive_y':' & ='+r'\int_{'+L(b[0])+'}^{'+L(b[1])+'}'+br(m['Ay'],'y',b[2],b[3])+r'\,\mathrm{d}x',
 'evaluated_y':' & ='+intx(m['ey'],b),
 'simplified_y':' & ='+intx(m['iy'],b),
 'primitive_x':' & ='+br(m['Ax'],'x',b[0],b[1]),
 'evaluated_x':' & ='+L(m['ex']),
 'answer':' & ='+L(m['answer']),}
 partial=aligned([r'\frac{\partial g}{\partial x} & =\frac{\partial}{\partial x}\left('+L(g)+r'\right)='+L(gx),r'\frac{\partial g}{\partial y} & =\frac{\partial}{\partial y}\left('+L(g)+r'\right)='+L(gy)])
 substitution=['F(x,y,g(x,y)) & ='+vector+r'\big|_{z='+L(g)+'}']
 if template=='easy_affine' or (template in SOURCES and SOURCES[template][':question/worked-solution'].split('Next,')[1].split('Therefore,')[0].count(r' \\ ')==2):
  substitution.append(' & ='+r'\left\langle '+r',\,'.join(re.sub(r'\bz\b',lambda match:r'\left('+L(g)+r'\right)',L(v)) for v in F)+r'\right\rangle')
 substitution.append(' & ='+r'\left\langle '+r',\,'.join(r'\underbrace{'+L(v)+'}_{'+n+'}' for v,n in zip(sub,['P','Q','R']))+r'\right\rangle')
 blocks=[r'\iint_S F\cdot\mathrm{d}\mathbf{S}='+formula+'.',partial]
 if template in SOURCES:
  src=SOURCES[template];parts=re.split(r'\$\$\n.*?\n\$\$',src[':question/worked-solution'],flags=re.S)
  if 'In this case,' in src[':question/worked-solution']:blocks.append(flux)
  blocks +=[aligned(substitution),aligned([stages[k] for k in STAGES[template]])]
  assert len(parts)==len(blocks)+1
  solution=''.join(parts[i]+'$$\n'+blk+'\n$$' for i,blk in enumerate(blocks))+parts[-1]
  problem=src[':question/problem'];problem=re.sub(r'\$\$\n.*?\n\$\$',lambda match:'$$\n'+(flux if LEVELS[template]=='moderate' else 'F(x,y,z)='+vector+',')+'\n$$',problem,flags=re.S)
  problem=re.sub(r'\$z=.*?\$',lambda match:'$z='+L(g)+'$',problem)
  # Replace the entire domain component; no short-expression global replacement.
  problem=problem[:problem.index(' for $')]+f' for ${L(b[0])}\\le x\\le {L(b[1])}$ and ${L(b[2])}\\le y\\le {L(b[3])}.$'
 else:
  problem='Calculate the flux of the vector field\n\n$$\nF(x,y,z)='+vector+',\n$$\n\nwhere the upward-oriented surface $S$ is defined by $z='+L(g)+f'$ for $0\\le x\\le {L(b[1])}$ and $0\\le y\\le {L(b[3])}.$'
  prose=['For a surface $S$ given by $z=g(x,y)$ for $(x,y)\\in D,$ the flux of a vector field $F(x,y,z)=⟨P,\\,Q,\\,R⟩$ over $S$ is given by','We first compute the partial derivatives of the graph $z=g(x,y):$','Next, we substitute the equation $z=g(x,y)$ into $F(x,y,z):$','Therefore, we can evaluate our surface integral as follows:']
  blocks +=[aligned(substitution),aligned([stages[k] for k in ['formula','dot','distributed','iterated','primitive_y','evaluated_y','primitive_x','evaluated_x','answer']])]
  solution='\n\n'.join(t+'\n\n$$\n'+b+'\n$$' for t,b in zip(prose,blocks))
 if not observed and template in SOURCES:problem=problem.replace('where the surface $S$', 'where the upward-oriented surface $S$')
 return problem,solution

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ['easy','moderate','hard']:raise ValueError('Unknown level')
 if field_type not in [None,'radio',':answer-field.type/radio']:raise ValueError('Only observed radio layout supported')
 rng=random.Random(seed);eligible=[k for k,v in TEMPLATES.items() if v['level']==level]
 if template is None:template=rng.choice(eligible)
 if template not in eligible:raise ValueError('Template outside difficulty scope')
 if profile and profile.startswith('observed_') and profile!='observed_'+template:raise ValueError('Mismatched profile')
 # Choose a complete eligible authored bank before sampling; reject whole instances.
 default_profile=('authored_zero_normal' if template in ['q-161536','q-161481'] else 'authored_zero_vertical' if template=='q-161553' else 'authored_signs')
 if profile is None:profile=default_profile
 if profile not in ([default_profile,'observed_'+template] if template in SOURCES else [default_profile]):raise ValueError('Bank profile outside template eligibility')
 for attempt in range(100):
  if parameters is None:
   if template=='easy_affine':p={k:rng.choice([-2,-1,1,2]) for k in ['a','b','u','v']};p.update({k:rng.randint(-2,2) for k in ['c','w']});p.update({k:rng.randint(1,2) for k in ['X','Y']})
   elif profile.startswith('observed_'):p=dict.fromkeys(['p','q','r'],rng.choice([-3,-2,-1,1,2,3]))
   else:p={k:rng.choice([-3,-2,-1,1,2,3]) for k in ['p','q','r']}
  else:p=dict(parameters)
  parameters_ok(template,p,profile);m=model(template,p,profile)
  try:values,recipes=build_bank(m,profile,template,p)
  except ValueError:
   if parameters is not None:raise
   continue
  break
 else:raise ValueError('Sampling exhausted complete bank')
 problem,solution=render(template,m,profile.startswith('observed_'))
 fingerprint=hashlib.sha256(json.dumps([s.srepr(m['g']),[s.srepr(v) for v in m['F']],[s.srepr(s.sympify(v)) for v in m['b']],'upward'],sort_keys=True).encode()).hexdigest()
 identity=hashlib.sha256(json.dumps([VERSION,problem,solution,sorted(L(v) for v in values),profile],sort_keys=True).encode()).hexdigest()
 qid=str(uuid.uuid5(uuid.NAMESPACE_URL,'flux-question:'+identity));fid=str(uuid.uuid5(uuid.UUID(qid),'selection'))
 answers=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),s.srepr(s.simplify(v)))),':answer/type':':answer.type/math',':answer/value':L(v)} for v in values]
 correct=next(a[':answer/id'] for a,v in zip(answers,values) if eq(v,m['answer']));rng.shuffle(answers)
 field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':problem,':question/worked-solution':solution,':question/answer-fields':[field]},'generation':{'version':VERSION,'seed':seed,'template':template,'profile':profile,'parameters':p,'mathematical_fingerprint':fingerprint,'content_fingerprint':identity,'source':{k:SOURCE[k] for k in ['database','basis','lineage']},'plot':'none','orientation':'upward','recipes':recipes,'scope':'authored missing easy' if level=='easy' else 'observed family with authored coefficient variation','quarantined_source_domain':template=='q-161481' and profile.startswith('observed_'),'source_solution_repair':template=='q-161552','dependency_versions':{'sympy':s.__version__},'mathematics':{k:([str(v) for v in a] if isinstance(a,list) else str(a)) for k,a in m.items()}}}
def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)
def generate_hard(seed=0,**kw):return generate('hard',seed,**kw)
def markdown(r):
 q=r['question'];f=q[':question/answer-fields'][0];return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$' for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
if __name__=='__main__':
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args();levels=['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty];records=[generate(level,args.seed+i,template=args.template,profile=args.profile) for level in levels for i in range(args.count)];print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
