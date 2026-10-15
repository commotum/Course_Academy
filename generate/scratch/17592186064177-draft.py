#!/usr/bin/env python3
"""Local, unregistered termwise exponential-sum generator; no database operations."""
import argparse, copy, hashlib, importlib.util, itertools, json, os, random, re, sys, uuid
from pathlib import Path
sys.dont_write_bytecode=True
try:
 import sympy as sp
except ModuleNotFoundError:
 runtime=Path(__file__).resolve().parents[2]/'.venv/bin/python'
 os.execv(str(runtime),[str(runtime),str(Path(__file__).resolve()),*sys.argv[1:]])
HERE=Path(__file__).with_suffix('');KP_ID=17592186064177
KP_UUID='980bb2fb-4bb5-5cbb-aea8-87010493c013';TITLE='Integrating a Sum of Exponential Functions';VERSION='2.0.0-draft'
spec=importlib.util.spec_from_file_location('expsum_private_math_format',HERE/'math_format.py');fmt=importlib.util.module_from_spec(spec);spec.loader.exec_module(fmt)
SUPPORTED_LEVELS=('easy','moderate','hard');X=sp.Symbol('x',real=True);C=sp.Symbol('C',real=True)
SOURCE=json.loads((HERE/'source.json').read_text());TEMPLATES=json.loads((HERE/'templates.json').read_text())
MA={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions'] if ':question/math-academy-id' in q}
SPECS={'q-31311':('easy',2),'q-51102':('moderate',4),'q-31261':('moderate',8),'q-167332':('moderate',None),'q-167786':('moderate',None),'q-166079':('moderate',None)}
for k,t in TEMPLATES.items():SPECS[k]=(t['difficulty'],t['parameters']['base'])
AUTHORED={'authored-easy':'easy','authored-moderate':'moderate','authored-hard':'hard'}
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(s):return str(uuid.uuid5(uuid.UUID(KP_UUID),s))
def integer(n,name,minimum=None):
 if type(n) is not int or minimum is not None and n<minimum:raise ValueError(name+' must be a built-in integer'+(' >= '+str(minimum) if minimum is not None else ''))
 return n

def expression(text, extra=None):
 """Private TeX reader, separate from rendering; supports exactly the bounded grammar."""
 from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
 text=text.strip().rstrip('.,').replace('\u2061','').replace(r'\operatorname{ln}',r'\ln')
 text=re.sub(r'(?<![A-Za-z\\])ln',lambda _:r'\ln',text)
 for a,b in [(r'\displaystyle',''),(r'\left',''),(r'\right',''),(r'\cdot','*'),(r'\,',''),(r'\!',''),(r'\mid','|'),(r'\log',r'\ln')]:text=text.replace(a,b)
 def group(s,pos):
  if pos>=len(s) or s[pos]!='{':raise ValueError('Expected TeX group: '+s[pos:])
  depth=1;i=pos+1
  while depth and i<len(s):
   if s[i]=='{':depth+=1
   elif s[i]=='}':depth-=1
   i+=1
  if depth:raise ValueError('Unbalanced TeX')
  return s[pos+1:i-1],i
 def fractions(s):
  while (m:=re.search(r'\\d?frac',s)):
   a,i=group(s,m.end());b,j=group(s,i);s=s[:m.start()]+'(('+fractions(a)+')/('+fractions(b)+'))'+s[j:]
  return s
 text=fractions(text)
 text=re.sub(r'\\ln\s*\|\s*x\s*\|',lambda _:'log(Abs(x))',text)
 # Authored formatter uses logarithms only of positive rational bases or |x|.
 text=re.sub(r'\\ln\s*\{([^{}]*)\}',lambda m:'log('+m[1]+')',text)
 text=re.sub(r'\\ln\s*\(\s*([^()]*)\s*\)',lambda m:'log('+m[1]+')',text)
 text=re.sub(r'\\ln\s*(\d+|x)',lambda m:'log('+m[1]+')',text)
 text=text.replace('{','(').replace('}',')').replace('^','**')
 if '\\' in text or '|' in text:raise ValueError('Unsupported TeX '+text)
 env={'x':X,'C':C,'e':sp.E,'log':sp.log,'Abs':sp.Abs,'f':sp.Function('f'),'g':sp.Function('g')};env.update(extra or {})
 return parse_expr(text,local_dict=env,transformations=standard_transformations+(implicit_multiplication_application,))

def tex(v):
 """Finite exact expression printer; no floating point or logarithm expansion."""
 if v==X:return 'x'
 if v==C:return 'C'
 if v==sp.E:return 'e'
 if v.is_Integer:return str(v)
 if v.is_Rational:return ('-' if v<0 else '')+r'\frac{'+str(abs(v.p))+'}{'+str(v.q)+'}'
 if v.func==sp.exp:return 'e^{'+tex(v.args[0])+'}'
 if v.func==sp.log:
  return r'\ln|x|' if v.args[0]==sp.Abs(X) else r'\ln{'+tex(v.args[0])+'}'
 if v.is_Add:
  out=''
  for a in v.as_ordered_terms():
   s=tex(a);out+=('' if not out or s.startswith('-') else '+')+s
  return out
 if v.is_Mul:
  num,den=sp.fraction(v)
  if den!=1:return r'\frac{'+tex(num)+'}{'+tex(den)+'}'
  coef,terms=v.as_coeff_Mul();out='' if coef==1 else '-' if coef==-1 else tex(coef)+r'\cdot '
  fs=terms.args if terms.is_Mul else (terms,)
  return out+r'\cdot '.join('('+tex(f)+')' if f.is_Add else tex(f) for f in fs)
 if v.is_Pow:
  a,b=v.args
  return ('('+tex(a)+')' if a.is_Add or a.is_Mul or a.is_Rational and not a.is_Integer else tex(a))+'^{'+tex(b)+'}'
 raise ValueError('Unsupported expression '+str(v))

def primitive(v):
 return sp.integrate(v,X).replace(sp.log(X),sp.log(sp.Abs(X)))
def mathclean(s):
 s=s.replace('\u2061','').replace(r'\operatorname{ln}',r'\ln')
 s=re.sub(r'(?<![A-Za-z\\])ln',lambda _:r'\ln',s)
 return s

def normalize(q):
 q=copy.deepcopy(q)
 for k in (':db/id',':question/math-academy-id'):q.pop(k,None)
 q[':question/problem']=fmt.normalize_prose(mathclean(q[':question/problem']))
 q[':question/worked-solution']=fmt.normalize_prose(mathclean(q[':question/worked-solution']))
 if isinstance(q[':question/difficulty'],dict):q[':question/difficulty']=q[':question/difficulty'][':db/ident']
 for f in q[':question/answer-fields']:
  f.pop(':db/id',None)
  if isinstance(f[':answer-field/type'],dict):f[':answer-field/type']=f[':answer-field/type'][':db/ident']
  for a in f[':answer-field/choices']:
   a.pop(':db/id',None)
   if isinstance(a[':answer/type'],dict):a[':answer/type']=a[':answer/type'][':db/ident']
   a[':answer/value']=fmt.normalize_tex(mathclean(a[':answer/value']))
  if isinstance(f[':answer-field/correct'],dict):f[':answer-field/correct']=[':answer/id',f[':answer-field/correct'][':answer/id']]
 return q

def fields(values,correct_index=0,kind='radio',key='selection'):
 return [{':answer-field/key':key,':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':[{':answer/type':':answer.type/math',':answer/value':v} for v in values],':answer-field/correct-index':correct_index}]

def source_instance(template,p):
 """Retain observed wording and operative rows; authored repairs are explicit."""
 q=copy.deepcopy(MA[template]);repairs=[]
 if template in TEMPLATES:
  t=TEMPLATES[template];render=lambda s:s.replace('@@B@@',str(p['base']))
  q[':question/problem']=render(t['prompt']);q[':question/worked-solution']=render(t['solution'])
  q[':question/answer-fields']=fields([render(v) for v in t['choices']],t['correct_index'],key=t['field_key'])
 elif template in ('q-31311','q-51102'):
  base=p['base'];original=SPECS[template][1]
  def render(s):return s.replace(str(original)+'^{x}',str(base)+'^{x}').replace(r'\ln '+str(original),r'\ln '+str(base))
  q[':question/problem']=render(q[':question/problem'])
  vals=[render(a[':answer/value']) for a in q[':question/answer-fields'][0][':answer-field/choices']]
  q[':question/answer-fields']=fields(vals,0 if template=='q-31311' else 4)
  expr=base**X-10*sp.exp(X) if template=='q-31311' else 2*sp.exp(X)+base**X-2*X
  q[':question/worked-solution']=direct_solution(expr)
  repairs=['Missing source key, solution and difficulty completed by differentiation and same-method authored stages.']
 elif template=='q-31261':
  base=p['base'];q[':question/problem']=q[':question/problem'].replace('{8}', '{'+str(base)+'}')
  q[':question/worked-solution']=q[':question/worked-solution'].replace('{8}', '{'+str(base)+'}').replace(r'\operatorname{ln}8',r'\ln{'+str(base)+'}')
  q[':question/problem']+=' {{field-1}}'
  q[':question/answer-fields']=fields([tex(sp.exp(X)+base**X/sp.log(base)+3*sp.log(sp.Abs(X)))+'+C'],kind='blank',key='field-1')
  repairs=['Missing source field completed as an authored blank returning the whole primitive including C.']
 else:
  # Original f/g operands are preserved; supplying definitions fixes source underdetermination.
  q[':question/problem']='Let $f(x)=\\frac{1}{2}e^x$ and $g(x)=8x-\\frac{2}{3}x^3$.\n\n'+q[':question/problem']
  repairs=['Source prompt leaves f and g undefined; definitions inferred from the first solution row are supplied explicitly.']
 q[':question/difficulty']=':question.difficulty/'+SPECS[template][0]
 return q,repairs

def integral(s):return r'\int ('+s+r')\,\text{d}x'
def direct_solution(expr):
 terms=expr.as_ordered_terms();split=[];evaluated=[]
 for term in terms:
  c,f=term.as_coeff_Mul();coef='' if c==1 else '-' if c==-1 else tex(c)
  split.append(coef+integral(tex(f)))
  evaluated.append(tex(primitive(term)))
 def join(ss):return ''.join(('' if i==0 or s.startswith('-') else '+')+s for i,s in enumerate(ss))
 return 'Here, we combine the sum rule and our exponential rules to get\n\n$$\n'+r'\begin{aligned}'+integral(tex(expr))+' &='+join(split)+r' \\ &='+join(evaluated)+'+C'+r' \\ &='+tex(primitive(expr))+'+C.'+r'\end{aligned}'+'\n$$'

def authored_parameters(difficulty,rng):
 # Every normal item within a level has this fixed workload; no level-internal progression.
 p={'base':rng.choice([2,3,4,5,6,7,8,9,10,11,12]),'a':rng.choice([-5,-4,-3,-2,2,3,4,5]),'b':rng.choice([-4,-3,-2,2,3,4])}
 if difficulty!='easy':p.update(tail=rng.choice(['power','constant','reciprocal']),c=rng.choice([-4,-3,-2,2,3,4]),power=rng.choice([1,2,3]))
 if difficulty=='hard':p.update(second_base=rng.choice([n for n in range(2,13) if n!=p['base']]),d=rng.choice([-3,-2,2,3]))
 return p

def check_parameters(template,p):
 level=AUTHORED.get(template)
 if level:
  keys={'base','a','b'} | ({'tail','c','power'} if level!='easy' else set()) | ({'second_base','d'} if level=='hard' else set())
  if set(p)!=keys:raise ValueError('Unexpected authored parameter slots')
  allowed={'base':range(2,13),'a':(-5,-4,-3,-2,2,3,4,5),'b':(-4,-3,-2,2,3,4),'c':(-4,-3,-2,2,3,4),'power':(1,2,3),'second_base':range(2,13),'d':(-3,-2,2,3)}
  for k,v in p.items():
   if k=='tail':
    if v not in ('power','constant','reciprocal'):raise ValueError('Invalid tail')
   elif type(v) is not int or v not in allowed[k]:raise ValueError('Invalid '+k)
  if p.get('second_base')==p['base']:raise ValueError('Distinct general bases required')
 else:
  keys={'base'} if SPECS[template][1] is not None else set()
  if set(p)!=keys or keys and (type(p['base']) is not int or not 2<=p['base']<=12):raise ValueError('Source base must be built-in integer 2..12')

def authored_instance(level,p,profile):
 expr=p['a']*sp.exp(X)+p['b']*sp.Integer(p['base'])**X
 if level!='easy':expr+=p['c']*({'power':X**p['power'],'constant':sp.Integer(1),'reciprocal':1/X}[p['tail']])
 if level=='hard':expr+=p['d']*sp.Integer(p['second_base'])**X
 answer=primitive(expr)
 # Select the entire bank before constructing it. Both profiles have fixed complete recipes.
 if profile=='authored-omit-log':
  wrong=[answer-p['b']*p['base']**X/sp.log(p['base'])+p['b']*p['base']**X,answer-2*p['a']*sp.exp(X),answer+p['a']*sp.exp(X),answer-p['b']*p['base']**X/sp.log(p['base'])]
 elif profile=='authored-multiply-log':
  wrong=[answer-p['b']*p['base']**X/sp.log(p['base'])+p['b']*p['base']**X*sp.log(p['base']),answer-2*p['b']*p['base']**X/sp.log(p['base']),answer-2*p['a']*sp.exp(X),answer-p['a']*sp.exp(X)]
 else:raise ValueError('Unknown complete profile')
 vals=[tex(answer)+'+C',*[tex(w)+'+C' for w in wrong]]
 q={':question/problem':'$'+integral(tex(expr))+'=$',':question/worked-solution':direct_solution(expr),':question/difficulty':':question.difficulty/'+level,':question/answer-fields':fields(vals)}
 return q,[]

def profile_recipes(template,profile):
 if template in TEMPLATES:return list(TEMPLATES[template]['choices'])
 if template in AUTHORED:
  if profile=='authored-omit-log':return ['A+C','A-b*base^x/log(base)+b*base^x+C','A-2*a*e^x+C','A+a*e^x+C','A-b*base^x/log(base)+C']
  return ['A+C','A-b*base^x/log(base)+b*base^x*log(base)+C','A-2*b*base^x/log(base)+C','A-2*a*e^x+C','A-a*e^x+C']
 if template in ('q-31311','q-51102'):
  original=SPECS[template][1]
  return [a[':answer/value'].replace(str(original)+'^{x}','@@base@@^{x}').replace(r'\ln '+str(original),r'\ln @@base@@') for a in MA[template][':question/answer-fields'][0][':answer-field/choices']]
 return []

@fmt.checked_math_content
def generate(difficulty,seed=0,template=None,parameters=None,bank_profile=None):
 integer(seed,'seed')
 if difficulty not in SUPPORTED_LEVELS:raise ValueError('Unsupported difficulty')
 rng=random.Random(seed);eligible=[k for k,v in SPECS.items() if v[0]==difficulty]+[k for k,v in AUTHORED.items() if v==difficulty]
 template=template or rng.choice(eligible)
 if template not in eligible:raise ValueError('Unsupported template for difficulty')
 authored=template in AUTHORED
 profiles=('authored-omit-log','authored-multiply-log') if authored else (template,)
 profile=bank_profile or rng.choice(profiles)
 if profile not in profiles:raise ValueError('Bank profile incompatible with template')
 p=copy.deepcopy(parameters) if parameters is not None else authored_parameters(difficulty,rng) if authored else {'base':rng.randint(2,12)} if SPECS[template][1] is not None else {}
 check_parameters(template,p)
 q,repairs=authored_instance(difficulty,p,profile) if authored else source_instance(template,p)
 # Newly constructed fields use an index until the content-based identity boundary.
 for f in q[':question/answer-fields']:
  if ':answer-field/correct-index' in f:
   index=f.pop(':answer-field/correct-index')
   for i,a in enumerate(f[':answer-field/choices']):a[':answer/id']=str(i)
   f[':answer-field/correct']=[':answer/id',str(index)]
 q=normalize(q)
 # Whole content/profile identity prevents distinct authored banks colliding. Task ID ignores bank/order.
 if template in ('q-167332','q-167786','q-166079'):
  task_expr=2*sp.exp(X)+24*X-2*X**3
 else:
  m=re.search(r'\\int\s*',q[':question/problem']);d=re.search(r'(?:\\,)?\\text\{d\}x|(?<![A-Za-z])dx',q[':question/problem'][m.end():])
  task_expr=expression(q[':question/problem'][m.end():m.end()+d.start()])
 task=digest({'difficulty':difficulty,'integrand':sp.srepr(sp.expand(task_expr))})
 skeleton=copy.deepcopy(q);skeleton.pop(':question/id',None)
 for f in skeleton[':question/answer-fields']:
  f.pop(':answer-field/id',None)
  cid=f[':answer-field/correct'][1]
  for a in f[':answer-field/choices']:
   a['correct']=a[':answer/id']==cid;a.pop(':answer/id')
  f.pop(':answer-field/correct')
 content=digest({'content':skeleton,'profile':profile});q[':question/id']=uid('draft-v2:'+content)
 for f in q[':question/answer-fields']:
  fid=uid(content+':field:'+f[':answer-field/key']);f[':answer-field/id']=fid;cid=f[':answer-field/correct'][1]
  for i,a in enumerate(f[':answer-field/choices']):
   old=a[':answer/id'];a[':answer/id']=uid(fid+':answer:'+str(i)+':'+a[':answer/value'])
   if old==cid:f[':answer-field/correct']=[':answer/id',a[':answer/id']]
 domain='x real' if r'\frac{1}{x}' not in q[':question/problem'] and not ('reciprocal'==p.get('tail')) and template not in ('q-31256','q-31261') else 'x real, x != 0; each connected interval has its own arbitrary constant'
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'generator_id':uid('question-generator-draft-v2'),'version':VERSION,'source_basis':SOURCE['basis'],'lineage':SOURCE['lineage'],'seed':seed,'template':template,'bank_profile':profile,'recipes':profile_recipes(template,profile),'parameters':p,'task_id':uid('task:'+task),'content_fingerprint':content,'domain':domain,'source_references':[] if authored else [template],'authored_extension':authored,'source_repairs':repairs,'dependencies':{'sympy':sp.__version__,'math_format':'private copy'}}}

def batch(difficulty,count=5,seed=0):
 integer(seed,'seed');integer(count,'count',0)
 if difficulty not in SUPPORTED_LEVELS and difficulty!='all':raise ValueError('Unsupported difficulty')
 levels=SUPPORTED_LEVELS if difficulty=='all' else (difficulty,)
 out=[]
 for level in levels:
  seen=set();i=0
  while len(seen)<count:
   if i>max(10000,count*100):raise ValueError('Requested count exceeds available unique task space')
   z=generate(level,seed+i);i+=1
   if z['generation']['task_id'] in seen:continue
   seen.add(z['generation']['task_id']);out.append(z)
 return out

def markdown(r):
 q=r['question'];f=q[':question/answer-fields'][0]
 return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$' for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=(*SUPPORTED_LEVELS,'all'),required=True);ap.add_argument('--count',type=int,default=5);ap.add_argument('--seed',type=int,default=0);ap.add_argument('--format',choices=('json','markdown'),default='json');ap.add_argument('--output');a=ap.parse_args()
 try:r=batch(a.difficulty,a.count,a.seed)
 except ValueError as e:ap.error(str(e))
 s=json.dumps(r,indent=2) if a.format=='json' else '\n\n---\n\n'.join(markdown(z) for z in r)
 if a.output:Path(a.output).write_text(s+'\n')
 else:print(s)
