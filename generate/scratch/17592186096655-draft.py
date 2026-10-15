#!/usr/bin/env python3
"""Private natural-exponential linear substitution generator at math basis2275.
The registered numeric script and its entire evidence tree are immutable.
Source masks expose complete translated-coordinate slots, not literal replay
branches. Normal source families keep their formal stages with documented
minimal differential repairs and complete method-derived banks.
"""
import argparse,hashlib,importlib.util,json,random,re,sys,uuid
from pathlib import Path
sys.dont_write_bytecode=True
import sympy as s
HERE=Path(__file__).with_suffix('')
def local(n):
 spec=importlib.util.spec_from_file_location('natural96655_'+n,HERE/(n+'.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
fmt=local('math_format');parser=local('scalar_parser');x=parser.X;u=s.Symbol('u');C=s.Symbol('C')
VERSION='natural-affine-private-2275-v1';KP_ID=17592186096655
SOURCE=json.loads((HERE/'source.json').read_text());KP=SOURCE['record'];CASES=json.loads((HERE/'source-cases.json').read_text());CA={c['template']:c for c in CASES};QS={q[':question/math-academy-id']:q for q in KP[':knowledge-point/questions']if ':question/math-academy-id'in q}
SUPPORTED_LEVELS=('easy','moderate','hard')
def digest(o):return hashlib.sha256(json.dumps(o,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(t):return str(uuid.uuid5(uuid.UUID(KP[':knowledge-point/id']),t))
def tex(z):
 text=s.latex(s.sympify(z),ln_notation=True).replace(r'\left','').replace(r'\right','').replace('e^{','{e}^{')
 return re.sub(r'(?<=[0-9}]) e(?![A-Za-z])',lambda m:r'\cdot e',text)
def strict_int(v,n):
 if type(v)is not int:raise ValueError(n+' must be a built-in integer')
 return v

def task_fingerprint(f,limits,var=x):
 f=f.subs(var,x);rate=s.cancel(s.diff(f,x)/f);amp=s.expand_power_exp(f).subs(x,0)
 return digest([s.srepr(rate),s.srepr(amp),[s.srepr(z)for z in limits]if limits is not None else None,'primitive family'if limits is None else'exact definite value'])

def source_parameters(t,p):
 if type(p)is not dict or set(p)!={'shift'}:raise ValueError('Source coordinate slot accepts exactly shift')
 r=strict_int(p['shift'],'shift')
 if not -4<=r<=4:raise ValueError('Source coordinate shift -4..4')
 return {'shift':r}

def shift_string(text,r,var='x',table=False):
 """Fill complete independent-coordinate and endpoint slots. Commands and
 differentials are protected; transformed-u endpoints stay fixed. Zero is the
 identity of this coordinate recipe, rather than a source-payload return path.
 """
 if text is None:return None
 coordinate=var if r==0 else '('+var+('-'if r>0 else'+')+str(abs(r))+')'
 # Mark bounds of integrals still written in the independent coordinate.
 pat=re.compile(r'(?:\{\\int \}|\\int)\s*_')
 marks=[]
 for m in pat.finditer(text):
  lo,j=parser.group(text,m.end());assert text[j]=='^';hi,k=parser.group(text,j+1)
  end=re.search(r'\\(?:text|textrm)\{d\}[xzu]|d[xzu]',text[k:])
  if end is None:continue
  body=text[k:k+end.start()]
  if re.search(r'(?<![A-Za-z])'+var+r'(?![A-Za-z])',body):marks.append((m.end(),k,lo,hi))
 for start,end,lo,hi in reversed(marks):
  def endpoint(z):
   # preserve the anchor's notation as a component; translate its value.
   return z if r==0 else tex(parser.scalar(z)+r)
  text=text[:start]+'{'+endpoint(lo)+'}^{'+endpoint(hi)+'}'+text[end:]
 # The x-row lists supplied independent-coordinate endpoints; the u-row does not.
 if table:
  patrow=re.compile(r'\| \$'+var+r'\$ \| \$(.*?)\$ \| \$(.*?)\$ \|')
  text=patrow.sub(lambda m:'| $§LABEL§$ | $'+(m[1]if r==0 else tex(parser.scalar(m[1])+r))+'$ | $'+(m[2]if r==0 else tex(parser.scalar(m[2])+r))+'$ |',text)
 protects={}
 def protect(m):
  key='§P'+str(len(protects))+'§';protects[key]=m[0];return key
 text=re.sub(r'\\(?:text|textrm)\{d\}'+var+r'|d'+var,protect,text)
 text=re.sub(r'(?<![A-Za-z])'+var+r'(?![A-Za-z])',coordinate,text)
 for key,value in protects.items():text=text.replace(key,value)
 return text.replace('§LABEL§',var)

def source_render(t,r,normal=False):
 q=QS[t];var='z'if t=='q-51160'else'x';prompt=shift_string(q[':question/problem'],r,var);sol=shift_string(q.get(':question/worked-solution'),r,var,True)
 values=[shift_string(a[':answer/value'],r,var)for a in q[':question/answer-fields'][0][':answer-field/choices']]
 if normal:
  prompt=prompt.replace('Do not round the answer.','Give an exact answer.')
  if t in('q-13775','q-30922'):
   # The source's first extracted-factor row has x-integrand/bounds but du.
   sol=sol.replace(r'\text{d}u \\',r'\text{d}x \\',1)
  if t=='q-51160':
   # Explicitly write z as u/2 in the first two intermediate integrals;
   # this retains both source operations while giving each du operand meaning.
   zslot='z'if r==0 else '(z'+('-'if r>0 else'+')+str(abs(r))+')'
   sol=sol.replace('{e}^{2'+zslot+'}'+r'\cdot \frac{1}{2}\,\text{d}u','{e}^{2(u/2)}'+r'\cdot \frac{1}{2}\,\text{d}u')
   sol=sol.replace(r'\int {e}^{2'+zslot+r'}\,\text{d}u',r'\int {e}^{2(u/2)}\,\text{d}u')
 return prompt,sol,values

def source_math(t,r):
 p=CA[t]['anchor_parameters'];a=s.Rational(p['a']);k=s.Rational(p['k']);b=s.Rational(p['b']);var=s.Symbol('z')if t=='q-51160'else x;z=k*(var-r)+b;f=a*s.exp(z);F=a*s.exp(z)/k
 limits=None
 if 'L'in p:limits=(s.sympify(p['L'],locals={'log':s.log})+r,s.sympify(p['H'],locals={'log':s.log})+r)
 return f,F if limits is None else s.expand(F.subs(var,limits[1])-F.subs(var,limits[0])),limits,var,z

def check_bank(values,correct,limits,var=x):
 vals=[parser.scalar(v.replace('z','x')).subs(C,0)for v in values];correct=correct.subs(var,x)
 def equal(a,b):
  d=a-b if limits is not None else s.diff(a-b,x)
  return s.cancel(s.expand_power_exp(d))==0
 if any(equal(a,b)for i,a in enumerate(vals)for b in vals[:i]):raise ValueError('Whole-bank equivalent values or primitive families')
 if sum(equal(a,correct)for a in vals)!=1:raise ValueError('Unique mathematical correct required')
 return next(i for i,a in enumerate(vals)if equal(a,correct))

def record(level,seed,t,profile,p,prompt,sol,values,index,kind,raw=False):
 if not raw:
  prompt=fmt.normalize_prose(prompt);sol=fmt.normalize_prose(sol);values=[fmt.normalize_tex(z)for z in values]
 presence={'difficulty':not raw or ':question/difficulty'in QS[t],'solution':sol is not None,'correct':index is not None}
 content=digest([VERSION,prompt,sol,kind,sorted(values),presence,level if presence['difficulty']else None,values[index]if index is not None else None]);qid=uid(content);fid=uid(qid+'/field')
 answers=[{':answer/id':uid(fid+'/'+v),':answer/type':':answer.type/math',':answer/value':v}for v in values]
 field={':answer-field/id':fid,':answer-field/key':'field-1'if kind=='blank'else'selection',':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':answers}
 if index is not None:field[':answer-field/correct']=[':answer/id',answers[index][':answer/id']]
 random.Random(seed).shuffle(answers)
 q={':question/id':qid,':question/problem':prompt,':question/answer-fields':[field]}
 if presence['difficulty']:q[':question/difficulty']=':question.difficulty/'+level
 if sol is not None:q[':question/worked-solution']=sol
 if t in CA:f,_,limits,var,_=source_math(t,p['shift'])
 else:f,_,limits,z=authored_math(p);var=x
 fp=task_fingerprint(f,limits,var)
 result={'knowledge_point':{'db_id':KP_ID,'id':KP[':knowledge-point/id'],'title':KP[':knowledge-point/title']},'question':q,'generation':{'version':VERSION,'seed':seed,'template':t,'profile':profile,'parameters':p,'math_fingerprint':fp,'mathematical_fingerprint':fp,'content_hash':content,'source_ids':[t]if t in CA else[],'domain':'real independent variable; nonzero linear exponent slope; ordered finite limits','evidence_only':raw,'eligible_for_learning':not raw,'authored_level':t=='affine'or(t=='q-13733'and not raw),'provenance':{k:v for k,v in SOURCE.items()if k!='record'},'dependencies':{'python':sys.version.split()[0],'sympy':s.__version__,'formatter':fmt.FORMAT_VERSION}}}
 if not raw:fmt.validate_generated_record(result)
 return result

def method_source(t,r):
 prompt,sol,_=source_render(t,r,True);f,F,limits,var,z=source_math(t,r);a=s.Rational(CA[t]['anchor_parameters']['a']);k=s.Rational(CA[t]['anchor_parameters']['k']);E=s.exp(z);kind=CA[t]['field_type']
 if sol is None:
  p=dict(a=int(a),kn=int(k),kd=1,b=-int(k)*r);prompt,sol=worked(p,False,'radio')
 if limits is None:
  if t=='q-113833':wrong=[s.exp(var-r-1)/k,-F,k*E,E]
  elif t=='q-13732':wrong=[k/a*E,a*E,k*E,a/k*s.exp(a*(var-r))]
  elif t=='q-51160':wrong=[k*E,-s.exp((var-r)**2)/k,E,s.exp(var-r)/k]
  else:wrong=[k*E,-E,E,-F]
  values=[tex(z)+'+C'for z in[F,*wrong]]
 elif kind=='blank':values=[tex(F)]
 else:
  lo=z.subs(var,limits[0]);hi=z.subs(var,limits[1]);A=a/k
  # Complete bank from omitted slope, endpoint sign and omitted endpoint.
  if t=='q-30923':
   width=limits[1]-limits[0];wrong=[s.exp(-hi),s.exp(hi),width,1/width]
  else:wrong=[k*F,-F,A*s.exp(hi),A*(s.exp(hi)+s.exp(lo))]
  values=[tex(v)for v in[F,*wrong]]
 check_bank(values,F,limits,var)
 return prompt,sol,values,kind

def authored_bounds(level,p):
 keys={'a','kn','kd','b'}|({'L','H'}if level!='easy'else set())
 if type(p)is not dict or set(p)!=keys:raise ValueError('Exact authored parameter shape required')
 for key,value in p.items():strict_int(value,key)
 a,kn,kd,b=[p[k]for k in('a','kn','kd','b')]
 if not(1<=abs(a)<=6 and 1<=abs(kn)<=4 and 1<=kd<=4 and abs(b)<=3):raise ValueError('Bounded coefficients')
 if kd!=1 and abs(kn)!=1:raise ValueError('Slope integer or reciprocal only')
 if level!='easy':
  if kd!=1 or not(-2<=p['L']<p['H']<=2):raise ValueError('Definite integer slope/limits')
  lo=kn*p['L']+b;hi=kn*p['H']+b
  if max(abs(lo),abs(hi))>10:raise ValueError('Endpoint exponent ceiling10')
  if level=='moderate'and p['L']!=0 and p['H']!=0:raise ValueError('Moderate has a zero supplied endpoint')
  if level=='hard'and(p['L']==0 or p['H']==0 or min(abs(lo),abs(hi))<2 or abs(a)<2 or abs(kn)<2 or b==0):raise ValueError('Hard requires two nonzero supplied and nonunit transformed endpoints, scales and offset')
 return p

def authored_math(p):
 a=s.Integer(p['a']);k=s.Rational(p['kn'],p['kd']);z=k*x+p['b'];f=a*s.exp(z);F=a*s.exp(z)/k;limits=(s.Integer(p['L']),s.Integer(p['H']))if'L'in p else None
 return f,s.expand(F.subs(x,limits[1])-F.subs(x,limits[0]))if limits else F,limits,z

def integral(z,a=1,limits=None,var='x'):
 lim=''if limits is None else '_{'+tex(limits[0])+'}^{'+tex(limits[1])+'}'
 return r'\int'+lim+' '+(''if a==1 else '('+tex(a)+r')\cdot ')+'{e}^{'+tex(z)+r'}\,\text{d}'+var

def worked(p,definite,kind='blank'):
 a=s.Integer(p['a']);k=s.Rational(p['kn'],p['kd']);f,F,limits,z=authored_math(p);I=integral(z,a,limits)
 prompt=('Evaluate the following integral. Give an exact answer.\n\n$'+I+'=$  \n{{field-1}}')if kind=='blank'else'What is $'+I+'$?'
 sol='If we let $u='+tex(z)+',$ then\n\n$$\n'+r'\frac{\text{d}u}{\text{d}x}='+tex(k)+r'\quad\Longrightarrow\quad '+r'\text{d}x=('+tex(1/k)+r')\,\text{d}u.'+'\n$$\n\n'
 factor='('+tex(a/k)+')'
 if definite:
  lo=z.subs(x,limits[0]);hi=z.subs(x,limits[1]);ulimits=(lo,hi)
  sol+='Computing our limits of integration, we get the following:\n\n| $x$ | $'+tex(limits[0])+'$ | $'+tex(limits[1])+'$ |\n| --- | --- | --- |\n| $u$ | $'+tex(lo)+'$ | $'+tex(hi)+'$ |\n\n'
  rows=[I+' & =('+tex(a)+')'+integral(z,1,limits),' & =('+tex(a)+')'+integral(u,1,ulimits,'u').replace(r'\,\text{d}u',r'\cdot ('+tex(1/k)+r')\,\text{d}u'),' & ='+factor+integral(u,1,ulimits,'u'),' & ='+factor+r'{e}^{u}|_{'+tex(lo)+'}^{'+tex(hi)+'}',' & ='+factor+'({e}^{'+tex(hi)+'}-{e}^{'+tex(lo)+'})',' & =('+tex(a/k*s.exp(hi))+')-('+tex(a/k*s.exp(lo))+')',' & ='+tex(F)]
 else:
  rows=[I+' & ='+integral(u,a,var='u').replace(r'\,\text{d}u',r'\cdot ('+tex(1/k)+r')\,\text{d}u'),' & ='+factor+integral(u,var='u'),' & ='+factor+r'{e}^{u}+C',' & ='+tex(F)+'+C']
 sol+='Then, we can write the integral in terms of $u$ and evaluate:\n\n$$\n'+r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}'+'\n$$'
 return prompt,sol

# EASY: observed indefinite substitution, integer/reciprocal slopes and outside
# integer scale. Exactly four integral/primitive/substitution stages.
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
# MODERATE: observed definite/log-bound and product-exponential families. Expanded
# definite family has one supplied zero endpoint; all source families stay served.
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
# HARD: authored same linear substitution with two nonzero supplied endpoints and
# two nonunit transformed exponents. Both signed endpoint components are retained.
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)

def generate(level='easy',seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in SUPPORTED_LEVELS:raise ValueError('Unknown difficulty')
 strict_int(seed,'seed')
 if template not in(None,'affine',*CA):raise ValueError('Unknown template')
 if profile not in(None,'observed_raw','method'):raise ValueError('Unknown profile')
 if field_type not in(None,'blank','radio'):raise ValueError('Unknown field type')
 rng=random.Random(seed)
 if template is None:
  eligible=[t for t,c in CA.items()if c['level']==level and field_type in(None,c['field_type'])]
  if field_type in(None,'radio'if level=='easy'else'blank'):eligible+=['affine']
  if not eligible:raise ValueError('Unsupported field contract')
  template=rng.choice(eligible)
 raw=profile=='observed_raw'
 if template in CA:
  c=CA[template]
  if level!=c['level']or field_type not in(None,c['field_type']):raise ValueError('Source family level/field contract')
  p=source_parameters(template,parameters if parameters is not None else{'shift':rng.randint(-4,4)});r=p['shift'];kind=c['field_type']
  if raw:
   prompt,sol,values=source_render(template,r);sf=QS[template][':question/answer-fields'][0];correct=sf.get(':answer-field/correct');idx=next((i for i,a in enumerate(sf[':answer-field/choices'])if correct and a[':answer/id']==correct[':answer/id']),None)
  else:prompt,sol,values,kind=method_source(template,r);idx=0
  return record(level,seed,template,'observed_raw'if raw else'method',p,prompt,sol,values,idx,kind,raw)
 if raw:raise ValueError('Raw profile requires original template')
 kind='radio'if level=='easy'else'blank'
 if field_type not in(None,kind):raise ValueError('Expanded family field contract')
 for _ in range(3000):
  p=parameters if parameters is not None else dict(a=rng.choice([v for v in range(-6,7)if v]),kn=rng.choice([-4,-3,-2,-1,1,2,3,4]),kd=1,b=rng.randint(-3,3))
  if parameters is None:
   if level=='easy'and rng.randrange(3)==0:p.update(kn=rng.choice([-1,1]),kd=rng.randint(2,4))
   if level!='easy':p.update(L=rng.randint(-2,1),H=rng.randint(-1,2))
  try:
   authored_bounds(level,p);prompt,sol=worked(p,level!='easy',kind);f,F,limits,z=authored_math(p)
   if kind=='blank':values=[tex(F)]
   else:
    a=s.Integer(p['a']);k=s.Rational(p['kn'],p['kd']);E=s.exp(z)
    # Choose the complete coefficient bank before assessing eligibility; no pool.
    bank=[F,a*k*E,a*E,-F,a/k*s.exp(-z)]
    values=[tex(v)+'+C'for v in bank]
   check_bank(values,F,limits)
   return record(level,seed,'affine','method',dict(p),prompt,sol,values,0,kind)
  except ValueError:
   if parameters is not None:raise
 raise ValueError('Whole-instance sampling exhausted')

def batch(level,count,seed=0,template=None,profile=None):
 strict_int(count,'count')
 if count<1:raise ValueError('Positive count')
 result=[];seen=set()
 for n in range(max(200,count*100)):
  r=generate(level,seed+n,template,profile=profile);fp=r['generation']['math_fingerprint']
  if fp not in seen:result.append(r);seen.add(fp)
  if len(result)==count:return result
 raise ValueError('Requested batch exceeds available mathematical tasks')
def markdown(r):
 q=r['question'];return q[':question/problem']+'\n\n'+'\n'.join(a[':answer/value']for f in q.get(':question/answer-fields',[])for a in f[':answer-field/choices'])+'\n\n'+q.get(':question/worked-solution','[No worked solution in captured evidence]')
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=(*SUPPORTED_LEVELS,'all'),default='all');ap.add_argument('--count',type=int,default=1);ap.add_argument('--seed',type=int,default=0);ap.add_argument('--template');ap.add_argument('--profile');ap.add_argument('--format',choices=('markdown','json'),default='json');args=ap.parse_args();out=[r for level in(SUPPORTED_LEVELS if args.difficulty=='all'else[args.difficulty])for r in batch(level,args.count,args.seed,args.template,args.profile)];print(json.dumps(out,indent=2)if args.format=='json'else'\n\n'.join(map(markdown,out)))
