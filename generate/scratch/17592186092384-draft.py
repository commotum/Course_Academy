#!/usr/bin/env python3
"""Basis-2275 private normal-slope draft; scalar power-rule tasks only."""
import argparse,copy,hashlib,importlib.util,json,random,sys,uuid
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
HERE=Path(__file__).with_suffix('');VERSION='2.0.0-draft';KP_ID=17592186092384
SOURCE=json.loads((HERE/'source.json').read_text());KP_UUID=SOURCE['record'][':knowledge-point/id'];TITLE=SOURCE['record'][':knowledge-point/title']
SOURCES={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
SUPPORTED_LEVELS=('easy','moderate','hard');x=s.Symbol('x',real=True)
SPECS={'q-308798':(x**2+3*x,-1),'q-342142':(4-3*x**2,1),'q-342147':(x**5/4-4*x**2,2),'q-342152':(2*x**3-x**-4,-1),'q-342153':(4-x**s.Rational(-1,2),s.Rational(1,4)),'q-103531':(2*x**s.Rational(3,2)-2*x**2,1),'q-103532':(x**3-4*x**s.Rational(5,2),1),'q-103543':(2*x**-5+7*x,1),'q-47449':(x**2+x,1),'q-71524':(x**2-5,2)}
EXCLUDED={'q-47407':'unrated; absent key and worked solution','q-47413':'unrated; absent key and worked solution','q-71525':'absent answer fields'}
AUTHORED={'authored-quadratic':('easy',2,1),'authored-cubic':('moderate',3,2),'authored-quartic':('hard',4,3)}
spec=importlib.util.spec_from_file_location('private_format',HERE/'math_format.py');fmt=importlib.util.module_from_spec(spec);spec.loader.exec_module(fmt)
def digest(o):return hashlib.sha256(json.dumps(o,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def tex(v):return s.latex(v)
def task_fingerprint(f,t):return digest([s.srepr(s.expand(s.powdenest(f,force=True))),str(t)])
RESERVED_TASKS={task_fingerprint(f,s.sympify(t)) for f,t in [*SPECS.values(),(s.sqrt(x)-2,1),(3*x**2-2*x,2),(2*x**3-x+3,1),(2*x**3-x**2,1)]}
def parameters_for(template):
 if template in SOURCES:return [{'scale':i} for i in range(1,13)] if template in SPECS else [{}]
 if template in AUTHORED:return [{'a':a,'b':b} for a in range(1,7) for b in range(-6,7) if b!=0 and AUTHORED[template][1]*a+AUTHORED[template][2]*b!=0]
 raise ValueError('Unknown template')
def bounds(template,p,raw=False):
 if not isinstance(p,dict) or any(type(v)!=int for v in p.values()):raise ValueError('Exact integer parameter mapping required')
 if raw:
  if p!=({'scale':1} if template in SPECS else {}):raise ValueError('Raw original parameters only')
 elif p not in parameters_for(template):raise ValueError('Outside declared finite domain')
def model(template,p):
 if template in SPECS:f,t=SPECS[template];f=s.expand(p['scale']*f)
 else:
  _,n,k=AUTHORED[template];f=p['a']*x**n+p['b']*x**k;t=s.Integer(1)
 d=s.diff(f,x);t=s.sympify(t);y=s.simplify(f.subs(x,t));m=s.simplify(d.subs(x,t));a=s.simplify(-1/m)
 if not m.is_finite or m==0:raise ValueError('Finite nonzero tangent slope required')
 return f,t,y,d,m,a

def bank(template,p,m,a):
 z=s.Integer(p.get('scale',1))
 if template=='q-103531':return [m,-s.Rational(5,2)*z,2/(5*z),a,-2/(5*z)]
 if template=='q-103532':return [-s.Integer(1),1/m,-m,m,a]
 if template=='q-103543':return [s.Integer(1),1/m,a,m,-m]
 if template=='q-47449':return [1/m,-s.Integer(1),1/(2*z),-1/(2*z),a]
 if template=='q-71524':return [a,s.Rational(4,5),m,-2*z,1/m]
 return [a]

def evaluation(d,t):
 # Unsimplified printed substitution is derived from exact derivative terms.
 def term(c,e):
  P='('+tex(t)+')';return tex(c)+r'\cdot '+P+(r'^{'+tex(e)+'}' if e!=1 else '') if e!=0 else tex(c)
 terms=[]
 for v in d.as_ordered_terms():
  c,e=v.as_coeff_exponent(x);terms.append(term(c,e))
 return '+'.join(terms).replace('+-','-')

def power_tex(expression):
 terms=[]
 for term in s.expand(expression).as_ordered_terms():
  c,e=term.as_coeff_exponent(x)
  if e==0:value=tex(c)
  else:value=('' if c==1 else '-' if c==-1 else tex(c))+('x' if e==1 else r'{x}^{'+tex(e)+'}')
  terms.append(value)
 return '+'.join(terms).replace('+-','-')
def term_evaluations(d,t):
 return '+'.join(tex(s.simplify(term.subs(x,t))) for term in d.as_ordered_terms()).replace('+-','-')

def displays(template,f,t,y,d,m,a):
 rewrite=s.expand(f)
 def chain(rows):return r'\begin{aligned}'+r' \\ '.join(A+' & ='+B for A,B in rows)+r'\end{aligned}'
 D=r'\frac{\text{d}}{\text{d}x}'
 if template in ('q-342152','q-342153','q-103531','q-103532','q-103543'):
  deriv=chain([(r"f'(x)",D+'('+tex(f)+')'),('',D+'('+power_tex(rewrite)+')'),('',power_tex(d)+'.')])
 if template=='q-342152':deriv=chain([(r"f'(x)",D+'('+tex(f)+')'),('',D+'('+power_tex(f)+')'),('',power_tex(d)),('',tex(d)+'.')])
 elif template not in ('q-342153','q-103531','q-103532','q-103543'):deriv=r"f'(x)="+D+'('+tex(f)+')='+tex(d)
 ev='m=f\'('+tex(t)+')='+evaluation(d,t)+'='+tex(m)
 if template in ('q-308798','q-342147'):ev='m=f\'('+tex(t)+')='+evaluation(d,t)+'='+term_evaluations(d,t)+'='+tex(m)
 if template in ('q-103531','q-103532','q-103543','q-71524'):ev=chain([(r"m=f'("+tex(t)+')',evaluation(d,t)+'='+tex(m)+'.')])
 normal=chain([(r"m'",r'-\frac{1}{m}'),('',r'-\frac{1}{('+tex(m)+')}'),('',tex(a)+'.')]) if template in ('q-308798','q-342142','q-342147','q-342152','q-342153') else r"m'=-\frac{1}{m}="+tex(a)+'.'
 return deriv,ev,normal

def source_strings(template,p):
 q=SOURCES[template]
 if p['scale']==1:
  # Exact source strings except narrow correction of unevaluated x in q342153.
  work=q[':question/worked-solution']
  if template=='q-342153':work=work.replace(r'=\frac{1}{2\sqrt{{x}^{3}}}=','=')
  return q[':question/problem'],work
 f,t,y,d,m,a=model(template,p);point='('+tex(t)+','+tex(y)+')'
 import re
 problem=re.sub(r'\$y=.*?\$',lambda _: '$y='+tex(f)+'$',q[':question/problem'],count=1)
 problem=re.sub(r'at the point \$.*?\$',lambda _: 'at the point $'+point+'.$',problem,count=1)
 work=re.sub(r'\$f\(x\)=.*?\$',lambda _: '$f(x)='+tex(f)+'.$',q[':question/worked-solution'],count=1)
 work=re.sub(r'point \$.*?\$',lambda _: 'point $'+point+':$',work,count=1)
 work=re.sub(r'\$\{f\}\^\{′\}\(.*?\)\$',lambda _: "$f'("+tex(t)+')$',work)
 blocks=list(re.finditer(r'\$\$\n.*?\n\$\$',work,re.S));assert len(blocks)==3
 for b,v in reversed(list(zip(blocks,displays(template,f,t,y,d,m,a)))):work=work[:b.start()]+'$$\n'+v+'\n$$'+work[b.end():]
 return problem,work

def authored_strings(template,p):
 f,t,y,d,m,a=model(template,p)
 problem="Find the slope $m'$ of the normal line to the curve $y="+tex(f)+'$ at the point $('+tex(t)+','+tex(y)+").$\n\n$m'=$\n{{field-1}}"
 parts=displays('q-308798',f,t,y,d,m,a)
 work='Let $f(x)='+tex(f)+'.$ First, we compute the derivative:\n\n$$\n'+parts[0]+'\n$$\n\nThen, we compute the slope of the tangent at the point $('+tex(t)+','+tex(y)+'):$\n\n$$\n'+parts[1]+"\n$$\n\nTherefore, the slope $m'$ of the normal line is\n\n$$\n"+parts[2]+'\n$$'
 return problem,work

def identity(q):
 obj=copy.deepcopy(q);obj.pop(':question/id',None)
 for f in obj.get(':question/answer-fields',[]):
  f.pop(':answer-field/id',None);ref=f.pop(':answer-field/correct',None)
  if ref:f['correct_value']=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==ref[1])
  for a in f[':answer-field/choices']:a.pop(':answer/id',None)
  f[':answer-field/choices']=sorted(f[':answer-field/choices'],key=lambda a:a[':answer/value'])
 return digest([VERSION,obj])
def package(q,template,p,level,seed,raw):
 if raw:q=copy.deepcopy(q);fp=digest(q)
 else:
  fmt.validate_generated_record({'question':q})
  fp=identity(q);qid=str(uuid.uuid5(uuid.UUID(KP_UUID),fp));q[':question/id']=qid
  for f in q[':question/answer-fields']:
   old=f[':answer-field/correct'][1];fid=str(uuid.uuid5(uuid.UUID(qid),f[':answer-field/key']));f[':answer-field/id']=fid
   for a in f[':answer-field/choices']:
    prior=a[':answer/id'];a[':answer/id']=str(uuid.uuid5(uuid.UUID(fid),a[':answer/value']))
    if prior==old:f[':answer-field/correct']=[':answer/id',a[':answer/id']]
   random.Random(seed).shuffle(f[':answer-field/choices'])
 task=task_fingerprint(*model(template,p)[:2]) if not raw else None
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'level':level,'template':template,'profile':'raw' if raw else 'source-bank' if template in SPECS else 'authored','parameters':p,'seed':seed,'content_sha256':fp,'parameter_fingerprint':task,'source_basis':SOURCE['basis'],'source_lineage':SOURCE['lineage'],'evidence_only':raw,'eligible_for_learning':not raw,'source_refs':[template] if template in SOURCES else ['e-148','q-47449'],'domain':'x>0' if template in ('q-342153','q-103531','q-103532') else 'x!=0' if template in ('q-342152','q-103543') else 'real x','python_version':sys.version.split()[0],'sympy_version':s.__version__}}

def generate(level,seed=0,template=None,parameters=None,profile=None,field_type=None):
 if level not in SUPPORTED_LEVELS:raise ValueError('Unknown difficulty')
 if type(seed)!=int:raise ValueError('Integer seed required')
 if profile not in (None,'default','source-bank','authored','raw','observed_raw'):raise ValueError('Unknown profile')
 raw=profile in ('raw','observed_raw');rng=random.Random(seed)
 eligible=list(SOURCES) if raw and level=='easy' else [] if raw else [m for m in SPECS if level=='easy']+[m for m,d in AUTHORED.items() if d[0]==level]
 if profile=='source-bank':eligible=[m for m in eligible if m in SPECS]
 if profile=='authored':eligible=[m for m in eligible if m in AUTHORED]
 if not eligible:raise ValueError('Unavailable difficulty/profile')
 template=template or rng.choice(eligible)
 if template not in eligible:raise ValueError('Template difficulty/profile mismatch')
 p=copy.deepcopy(parameters) if parameters is not None else ({'scale':1} if template in SPECS else {}) if raw else rng.choice(parameters_for(template));bounds(template,p,raw)
 q=SOURCES.get(template)
 expected=q[':question/answer-fields'][0][':answer-field/type'][':db/ident'] if q and q.get(':question/answer-fields') else ':answer-field.type/blank'
 if field_type not in (None,expected,expected.split('/')[-1]):raise ValueError('Unsupported field type')
 if raw:return package(q,template,p,level,seed,True)
 f,t,y,d,m,a=model(template,p);vals=[s.simplify(v) for v in bank(template,p,m,a)]
 if len(set(vals))!=len(vals) or vals.count(a)!=1:raise ValueError('Invalid whole bank')
 problem,work=source_strings(template,p) if template in SPECS else authored_strings(template,p)
 problem=fmt.normalize_prose(problem);work=fmt.normalize_prose(work)
 choices=[{':answer/id':str(i),':answer/type':':answer.type/math',':answer/value':fmt.normalize_tex(tex(v))} for i,v in enumerate(vals)]
 field={':answer-field/key':q[':question/answer-fields'][0][':answer-field/key'] if q else 'field-1',':answer-field/type':expected,':answer-field/choices':choices,':answer-field/correct':[':answer/id',str(vals.index(a))]}
 question={':question/problem':problem,':question/worked-solution':work,':question/difficulty':':question.difficulty/'+level,':question/answer-fields':[field]}
 return package(question,template,p,level,seed,False)
def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)
def generate_hard(seed=0,**kw):return generate('hard',seed,**kw)
def generate_profile(template,scale,seed=0):return generate('easy',seed,template,{'scale':scale},'source-bank')
def batch(level,count,seed=0):
 if level not in SUPPORTED_LEVELS or type(count)!=int or count<1 or type(seed)!=int:raise ValueError('Invalid batch request')
 domain=[(m,p) for m in SPECS if level=='easy' for p in parameters_for(m)]+[(m,p) for m,d in AUTHORED.items() if d[0]==level for p in parameters_for(m)]
 rng=random.Random(seed);rng.shuffle(domain);out=[];seen=set()
 for m,p in domain:
  try:r=generate(level,seed,template=m,parameters=p)
  except ValueError:continue
  fp=r['generation']['parameter_fingerprint']
  if fp in seen or fp in RESERVED_TASKS:continue
  seen.add(fp);out.append(r)
  if len(out)==count:return out
 raise ValueError('Requested count exceeds unique eligible capacity')
def markdown(r):
 q=r['question'];parts=[q[':question/problem']]
 for f in q.get(':question/answer-fields',[]):parts+=['Choices ('+str(f[':answer-field/type'])+'):',*['- $'+a[':answer/value']+'$' for a in f[':answer-field/choices']]]
 parts.append(q.get(':question/worked-solution','[No captured worked solution.]'));return '\n\n'.join(parts)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--difficulty',choices=[*SUPPORTED_LEVELS,'all'],default='all');p.add_argument('--count',type=int,default=1);p.add_argument('--seed',type=int,default=0);p.add_argument('--format',choices=['json','markdown'],default='json');p.add_argument('--template');p.add_argument('--profile');a=p.parse_args();
 if a.count<1:raise ValueError('Positive count required')
 rows=[generate(l,a.seed+i,template=a.template,profile=a.profile) for l in (SUPPORTED_LEVELS if a.difficulty=='all' else [a.difficulty]) for i in range(a.count)];print(json.dumps(rows,indent=2,ensure_ascii=False) if a.format=='json' else '\n\n---\n\n'.join(map(markdown,rows)))
