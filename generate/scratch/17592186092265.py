#!/usr/bin/env python3
"""Basis 2275 general-base logarithm chain rule; private, unregistered generator.
Observed banks are complete profiles. Raw replay is evidence only. Source-specific
stages and cancellation lines are retained; completions are explicitly authored.
"""
import sys
sys.dont_write_bytecode=True
import argparse,copy,hashlib,importlib.util,json,random,re,uuid
from pathlib import Path
try:import sympy as s
except ImportError:
 import os
 runtime=Path(__file__).resolve().parents[2]/'.venv/bin/python';os.execv(str(runtime),[str(runtime),str(Path(__file__).resolve()),*sys.argv[1:]])
H=Path(__file__).with_suffix('');ROOT=Path(__file__).resolve().parents[2]
def load(path,name):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
fmt=load(H/'private_math_format.py','general_log_private_format')
SOURCE=json.loads((H/'source.json').read_text());KP=SOURCE['record'];KP_ID=17592186092265;VERSION='general-log-chain-2275-v1'
X=s.Symbol('x',real=True);U=s.Symbol('u',real=True)
ROWS={q[':question/math-academy-id']:q for q in KP[':knowledge-point/questions']}
# source ID: shape, difficulty, b,a,c,n,k,t, original response contract.
SPECS={
'q-1948':('sqrt','hard',2,1,0,1,0,None,'radio'),
'q-48008':('affine','easy',3,5,-2,1,0,None,'radio'),
'q-1949':('affine','easy',5,5,0,1,0,None,'absent'),
'q-310148':('affine','easy',5,-6,7,1,0,None,'blank'),
'q-341686':('affine','easy',7,4,-9,1,0,None,'blank'),
'q-341688':('affine','easy',10,8,0,1,0,None,'blank'),
'q-48001':('affine','easy',2,-2,3,1,0,None,'absent'),
'q-71479':('affine','easy',4,-5,2,1,0,None,'absent'),
'q-310145':('tangent','moderate',4,6,-2,1,7,'1','blank'),
'q-310149':('power','moderate',10,1,-2,5,0,None,'blank'),
'q-341691':('power','moderate',6,-3,0,3,0,None,'blank'),
'q-341694':('sqrt','hard',4,7,0,1,0,None,'blank'),
'q-48559':('power','moderate',2,1,0,3,0,None,'radio'),
'q-48656':('tangent','moderate',3,5,-2,1,5,'7/15','radio'),
'q-51317':('affine','easy',10,-1,1,1,0,None,'radio'),
'q-71478':('sqrt','hard',3,2,0,1,0,None,'radio')}
TEMPLATES=tuple(SPECS);SUPPORTED_LEVELS=('easy','moderate','hard')
def original(t):
 shape,lev,b,a,c,n,k,pt,ft=SPECS[t];return dict(b=b,a=a,c=c,n=n,k=k,t=pt)
def tex(z):return s.latex(z).replace(r'\log',r'\ln').replace(r'\left','').replace(r'\right','')
def digest(z):return hashlib.sha256(json.dumps(z,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(z):return str(uuid.uuid5(uuid.UUID(KP[':knowledge-point/id']),z))
def math_data(t,p):
 shape=SPECS[t][0];b,a,c,n,k=(p[z] for z in ('b','a','c','n','k'))
 if any(type(v)!=int for v in (b,a,c,n,k)) or not 2<=b<=10 or not -9<=a<=9 or a==0 or not -12<=c<=12 or not 1<=n<=7 or not -9<=k<=9:raise ValueError('Outside declared bounds')
 if t in ('q-341691','q-48559','q-1949','q-341688') and c!=0:raise ValueError('Zero-shift cancellation family requires c=0')
 if t in ('q-48559','q-310149') and a!=1:raise ValueError('Unit power coefficient family')
 if t=='q-310149' and c==0:raise ValueError('Shifted-power family requires a nonzero shift')
 if t=='q-48008' and (a<2 or c>=0):raise ValueError('Swapped-operand bank requires a>1 and c<0')
 if t=='q-51317' and (a!=-1 or b!=10):raise ValueError('Common-log negative-unit affine family')
 if t=='q-310145' and (a%2 or c%2):raise ValueError('Even-coefficient tangent reduction family')
 if shape=='sqrt':
  if c!=0 or n!=1 or k!=0:raise ValueError('Root backbone is sqrt(ax)')
  g=s.sqrt(a*X);domain=('x>0' if a>0 else 'x<0')
 elif shape=='power':
  if n<2 or k!=0:raise ValueError('Power backbone')
  g=a*X**n+c;domain=str(g)+'>0'
  if c==0 and n%2==0 and a<0:raise ValueError('Empty real logarithm domain')
 else:
  if n!=1 or (shape=='affine' and k!=0):raise ValueError('Affine backbone')
  g=a*X+c;domain=str(g)+'>0'
 gp=s.diff(g,X);d=s.cancel(gp/g)/s.log(b);point=None if p['t'] is None else s.Rational(p['t'])
 if shape=='tangent':
  if point is None or not (g.subs(X,point)>0):raise ValueError('Tangent point outside domain')
  innervalue=g.subs(X,point)
  if not innervalue.is_Rational or not 1<=innervalue.p<=5 or not 1<=innervalue.q<=5:raise ValueError('Tangent inner value outside bounded rational slot')
 elif point is not None:raise ValueError('Unexpected evaluation point')
 answer=s.simplify(d.subs(X,point)) if point is not None else d
 return g,gp,d,answer,domain,point

def profile(t):return 'observed-'+t if SPECS[t][-1]=='radio' else 'blank'
def bank(t,p):
 g,gp,d,ans,domain,pt=math_data(t,p);b,a,c,n=(p[z] for z in ('b','a','c','n'));L=s.log(b)
 if t=='q-1948':return [1/(g*L),a/(2*g*L),d,2*d,d*L]
 if t=='q-48008':return [a/((-c*X-a)*L),1/(g*s.log(a)),a/(g*s.log(a)),d,a/g]
 if t=='q-48559':return [1/(g*L),n/X,d,n/X**(n-1),1/(n*X*L)]
 if t=='q-48656':return [a/L,a/(b*L),s.Rational(b,a)/L,ans,b/L]
 if t=='q-51317':return [d,b/g,a/g,g*L,L/g]
 if t=='q-71478':return [2*d,d*L,4*d*L,4*d,d]
 return [ans]

def normalize_source_text(z):
 z=z.replace('⁡','').replace('ln',r'\ln') if 'ln⁡' in z else z.replace('⁡','')
 # Avoid corrupting already canonical operatorname{ln}; only plain captured tokens.
 z=re.sub(r'(?<![A-Za-z\\])log(?=\(|\s)',r'\\log',z).replace('{log}',r'\log')
 z=z.replace(r'\operatorname{\ln}',r'\operatorname{ln}')
 z=z.replace(r'\begin{aligned}\begin{aligned}',r'\begin{aligned}').replace(r'\end{aligned}\end{aligned}',r'\end{aligned}')
 return fmt.normalize_prose(z)
def raw_replay(source_id):
 return {'question':copy.deepcopy(ROWS[source_id]),'knowledge_point':{'db_id':KP_ID,'title':KP[':knowledge-point/title']},'generation':{'template':source_id,'source_id':source_id,'parameters':original(source_id),'bank_profile':profile(source_id),'profile':'observed_raw','source_basis':2275,'evidence_only':True,'eligible_for_learning':False,'seed':0}}
def derivative(symbol,den):return r'\frac{\mathrm{d}'+symbol+r'}{\mathrm{d}'+den+'}'
def product(a,b):return a+r'\cdot ('+b+')'
def display(z):return '$$\n'+z+'\n$$'
def align(rows,lhs):return r'\begin{aligned}'+lhs+' &='+r'\\ &='.join(rows)+r'.\end{aligned}'
def logtex(b,arg):return (r'\log('+arg+')') if b==10 else r'\log_{'+str(b)+'}('+arg+')'
def stages(t,p):
 """Concrete ordered stages, including equal-valued cancellation stages."""
 g,gp,d,ans,dom,pt=math_data(t,p);shape=SPECS[t][0];a,b,c,n,k=(p[z] for z in ('a','b','c','n','k'));L=r'\ln('+str(b)+')';G=(r'\sqrt{'+tex(a*X)+'}') if shape=='sqrt' else tex(g);GP=(r'\frac{'+str(a)+r'}{2\sqrt{'+tex(a*X)+'}}') if shape=='sqrt' else tex(gp);sym='f' if t in ('q-310148','q-341686','q-341688','q-48001') else 'y'
 dy=derivative(sym,'x');du=derivative(sym,'u');dx=derivative('u','x');outside=logtex(b,'u')+(('+' if k>=0 else '')+str(k) if shape=='tangent' else '')
 composite=(sym+'(x)' if sym=='f' else sym)+'='+outside+r',\quad u='+G+'.'
 if t=='q-51317' and b!=10:raise ValueError('Common-log conversion profile requires base10')
 if t=='q-51317':composite='y='+r'\log(u)=\log_{10}(u),\quad u='+G+'.'
 one=r'\frac{1}{u'+L+'}'
 gpsteps=[GP]
 if t=='q-71478':gpsteps=[r'\frac{\sqrt{'+str(abs(a))+r'}}{2\sqrt{'+('x' if a>0 else '-x')+'}}'+('' if a>0 else r'\cdot(-1)'),GP]
 factors=du+'='+one+r',\quad '+dx+'='+'='.join(gpsteps)+'.'
 rows=[du+r'\cdot '+dx,product(one,GP)]
 substituted=product(r'\frac{1}{('+G+')'+L+'}',GP)
 if t in ('q-310149',):rows.append(tex(gp)+r'\frac{1}{('+G+')'+L+'}')
 elif t in ('q-341691','q-48559'):
  rows.append(r'\frac{'+GP+'}{('+G+')'+L+'}')
  common=a*X**(n-1)
  rows.append(r'\frac{\cancel{'+tex(common)+r'}\cdot '+str(n)+r'}{\cancel{'+tex(common)+r'}\cdot x'+L+'}')
  rows.append(tex(d))
 elif t in ('q-1949','q-341688'):
  rows.append(substituted if t=='q-1949' else r'\frac{'+str(a)+'}{('+G+')'+L+'}')
  rows.append(r'\frac{\cancel{'+str(a)+r'}}{\cancel{'+str(a)+'}x'+L+'}')
  rows.append(tex(d))
 elif t=='q-341694':
  rows.append(substituted);rows.append(r'\frac{'+str(a)+'}{2('+tex(a*X)+')'+L+'}')
  rows.append(r'\frac{\cancel{'+str(a)+r'}}{2\cdot \cancel{'+str(a)+'}x'+L+'}');rows.append(tex(d))
 else:
  rows.append(substituted)
  rows.append(tex(gp/g)+r'\frac{1}{'+L+'}')
  if t=='q-310145':rows.append(tex(d))
 chain=align(rows,dy)
 evaluation=None
 if pt is not None:
  val=tex(g.subs(X,pt));subst=tex(d).replace('x','('+tex(pt)+')')
  erows=[r'\left.('+tex(d)+r')\right|_{x='+tex(pt)+'}',subst,tex(ans)]
  if t=='q-48656':erows.insert(-1,r'\frac{'+str(a)+'}{('+val+')'+L+'}')
  evaluation=align(erows,'m='+dy+r'\big|_{x='+tex(pt)+'}')
 return composite,factors,chain,evaluation,sym

def solution(t,p):
 co,fa,ch,ev,sym=stages(t,p);noun='$f(x)$' if sym=='f' else '$y$'
 z='First, we express '+noun+' as the composite function\n\n'+display(co)+'\n\nDifferentiating gives\n\n'+display(fa)+'\n\nWe now apply the chain rule, and get\n\n'+display(ch)
 if ev:z+='\n\nTherefore, the slope $m$ of the tangent line at the point where $x='+tex(s.Rational(p['t']))+'$ is\n\n'+display(ev)
 return z

def prompt(t,p,ft):
 g,gp,d,ans,dom,pt=math_data(t,p);shape=SPECS[t][0];a,b,c,n,k=(p[z] for z in ('a','b','c','n','k'));co,fa,ch,ev,sym=stages(t,p);f=logtex(b,(r'\sqrt{'+tex(a*X)+'}') if shape=='sqrt' else tex(g))
 if shape=='tangent':
  f+=('+' if k>=0 else '')+str(k)
  text='Find the slope '+('$m$ ' if t=='q-310145' else '')+'of the tangent to the curve $y='+f+'$ at the point where $x='+tex(pt)+'.$';target='m'
 elif t in ('q-1948','q-48008','q-71478'):text='Calculate $'+derivative('y','x')+'$ for $y='+f+'.$';target=derivative('y','x')
 elif t in ('q-1949','q-71479','q-51317'):text="Find $y'$ for $y="+f+'.$';target="y'"
 elif t=='q-48001':text="Find $f'(x)$ for $f(x)="+f+'.$';target="f'(x)"
 else:
  target="f'(x)" if sym=='f' else derivative('y','x');text='Given that $'+('f(x)' if sym=='f' else 'y')+'='+f+',$ find $'+target+'$'+(' in terms of $x.$' if sym=='y' and t!='q-48559' else '.')
 if ft=='blank':text+='\n\n$'+target+'=$\n{{field-1}}'
 return text

def finish(q,t,p,seed,prof,authored):
 q=copy.deepcopy(q);q[':question/problem']=fmt.normalize_prose(q[':question/problem']);q[':question/worked-solution']=fmt.normalize_prose(q[':question/worked-solution'])
 for f in q[':question/answer-fields']:
  for a in f[':answer-field/choices']:a[':answer/value']=fmt.normalize_tex(a[':answer/value'])
 g,gp,d,ans,dom,pt=math_data(t,p)
 # Mathematical task identity is independent of source alias, seed and option order.
 identity=digest([s.srepr(s.log(g)/s.log(p['b'])+p['k']),str(pt),dom,'slope' if pt is not None else 'derivative'])
 fields_signature=[(f[':answer-field/key'],f[':answer-field/type'],sorted(a[':answer/value'] for a in f[':answer-field/choices']),f[':answer-field/choices'][f['_correct_index']][':answer/value']) for f in q[':question/answer-fields']]
 content=digest([q[':question/problem'],q[':question/worked-solution'],q[':question/difficulty'],fields_signature])
 q[':question/id']=uid('content:'+content)
 for f in q[':question/answer-fields']:
  f[':answer-field/id']=uid('field:'+content+':'+f[':answer-field/key']);correct_index=f.pop('_correct_index')
  for a in f[':answer-field/choices']:a[':answer/id']=uid(f[':answer-field/id']+':answer:'+a[':answer/value'])
  f[':answer-field/correct']=[':answer/id',f[':answer-field/choices'][correct_index][':answer/id']]
 out={'question':q,'knowledge_point':{'db_id':KP_ID,'id':KP[':knowledge-point/id'],'title':KP[':knowledge-point/title']},'generation':{'version':VERSION,'source_basis':2275,'lineage':SOURCE['lineage'],'template':t,'source_id':t,'parameters':copy.deepcopy(p),'seed':seed,'profile':prof,'bank_profile':prof,'domain':dom,'excluded_holes':[str(z) for z in s.solve(s.denom(d),X)],'mathematical_fingerprint':identity,'content_hash':content,'evidence_only':False,'authored_completion':authored,'sympy':s.__version__,'eligible_for_learning':True}}
 fmt.validate_generated_record(out);return out

def source_replay(source_id,profile='observed_raw'):
 if profile=='observed_raw':return raw_replay(source_id)
 if profile not in ('observed_served','served'):raise ValueError('Unknown replay profile')
 return generate(SPECS[source_id][1],template=source_id,parameters=original(source_id),profile='source')

def sample(t,r):
 shape=SPECS[t][0];p=original(t);p['b']=r.randint(2,10)
 if shape=='sqrt':p['a']=r.choice(tuple(range(-9,0))+tuple(range(1,10)))
 elif shape=='power':
  p['n']=r.randint(2,7);p['a']=1 if t in ('q-48559','q-310149') else r.choice((-9,-7,-5,-3,-1,1,2,3,5,7));p['c']=0 if t!='q-310149' else r.choice((-9,-7,-5,-3,-2,-1,1,2,3,5,7,9))
 elif t=='q-48008':p['a']=r.randint(2,9);p['c']=-r.randint(1,12)
 elif t=='q-51317':p['b']=10;p['a']=-1;p['c']=r.randint(-12,12)
 elif t in ('q-1949','q-341688'):p['a']=r.choice(tuple(range(-9,0))+tuple(range(1,10)));p['c']=0
 else:
  p['a']=r.choice(tuple(range(-9,0))+tuple(range(1,10)));p['c']=r.randint(-12,12)
 if shape=='tangent':
  if t=='q-310145':p['a']=r.choice((-8,-6,-4,-2,2,4,6,8));p['c']=r.choice((-12,-10,-8,-6,-4,-2,0,2,4,6,8,10,12))
  p['k']=r.randint(-9,9);value=s.Rational(r.randint(1,5),r.randint(1,5));p['t']=str((value-p['c'])/p['a'])
 return p

@fmt.checked_math_content
def generate(level,seed=0,template=None,parameters=None,profile='source',field_type=None):
 if level not in SUPPORTED_LEVELS or type(seed)!=int:raise ValueError('Invalid difficulty/seed')
 r=random.Random(seed);eligible=[t for t in TEMPLATES if SPECS[t][1]==level];t=template or r.choice(eligible)
 if t not in eligible:raise ValueError('Template/difficulty mismatch')
 shape,lev,b,a,c,n,k,pt,source_ft=SPECS[t];ft=field_type or ('blank' if source_ft=='absent' else source_ft)
 if ft not in ('blank','radio'):raise ValueError('Unsupported response type')
 if ft=='radio' and source_ft!='radio':raise ValueError('No observed complete radio bank')
 prof=profile
 if profile=='source':prof=globals()['profile'](t) if ft==source_ft else 'authored-blank-completion'
 if ft=='radio' and prof!=globals()['profile'](t):raise ValueError('Unknown whole bank profile')
 for attempt in range(1000):
  p=copy.deepcopy(parameters) if parameters is not None else sample(t,r)
  try:
   g,gp,d,ans,dom,point=math_data(t,p);values=bank(t,p) if ft=='radio' else [ans]
   if any(v.has(s.zoo,s.nan,s.oo,-s.oo) for v in values):raise ValueError('Undefined bank')
   if any(s.simplify(v-w)==0 for i,v in enumerate(values) for w in values[i+1:]):raise ValueError('Whole bank collision')
   correct=[i for i,v in enumerate(values) if s.simplify(v-ans)==0]
   if len(correct)!=1:raise ValueError('Ambiguous bank')
   break
  except ValueError:
   if parameters is not None:raise
 else:raise ValueError('No valid whole bank in 1000 draws')
 q={':question/difficulty':':question.difficulty/'+level,':question/problem':prompt(t,p,ft),':question/worked-solution':solution(t,p),':question/answer-fields':[{':answer-field/key':'selection' if ft=='radio' else 'field-1',':answer-field/type':':answer-field.type/'+ft,':answer-field/choices':[{':answer/type':':answer.type/math',':answer/value':tex(v)} for v in values],'_correct_index':correct[0]}]}
 return finish(q,t,p,seed,prof,source_ft=='absent' or ':answer-field/correct' not in (ROWS[t].get(':question/answer-fields') or [{}])[0])

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--template');ap.add_argument('--format',choices=('json','markdown'),default='json');ap.add_argument('--source-id');ap.add_argument('--profile',default='source');args=ap.parse_args()
 if args.source_id:records=[source_replay(args.source_id,'observed_raw' if args.profile=='source' else args.profile)]
 else:records=[generate(level,args.seed+i,args.template) for level in (SUPPORTED_LEVELS if args.difficulty=='all' else (args.difficulty,)) for i in range(args.count)]
 if args.format=='json':print(json.dumps(records,indent=2))
 else:print('\n\n---\n\n'.join(r['question'][':question/problem']+'\n\n'+r['question'][':question/worked-solution'] for r in records))
