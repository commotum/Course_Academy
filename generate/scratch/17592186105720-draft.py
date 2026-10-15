#!/usr/bin/env python3
"""Local unregistered draft: reciprocal primitives with logarithmic constants.

Easy: authored integer reciprocal coefficient (no negative-power recognition).
Moderate: observed rational reciprocal, negative power, and linear numerator.
Hard: observed binomial square, expansion then termwise integration then logs.
Every complete source bank remains public through profile='source'.
"""
import argparse,hashlib,importlib.util,json,math,random,re,sys,uuid
from pathlib import Path
import sympy as sp
sys.dont_write_bytecode=True
D=Path(__file__).resolve().with_suffix('')
def load(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
FORMAT=load('kp5720_frozen_format',D/'math_format.py')
TEMPLATES=json.loads((D/'templates.json').read_text());SOURCE=json.loads((D/'source.json').read_text())
KP_ID=17592186105720;KP_UUID=SOURCE['record'][':knowledge-point/id'];TITLE=SOURCE['record'][':knowledge-point/title'];VERSION='2.0.0-draft';SUPPORTED_LEVELS=('easy','moderate','hard')
X=sp.Symbol('x',real=True);K=sp.Symbol('K',positive=True)
def uid(s):return str(uuid.uuid5(uuid.UUID(KP_UUID),s))
def normalize(s):
 s=s.replace('\u2061','').replace(r'\operatorname{ln}',r'\ln');s=re.sub(r'(?<![a-z\\])ln',lambda _:r'\ln',s);s=re.sub(r'\\ln(?=[A-Za-z])',lambda _:r'\ln ',s)
 return s

def domain(t):
 """Finite workload bounds apply identically to samplers and explicit inputs."""
 if t=='easy_integer':return [{'n':n}for n in range(-24,25)if abs(n)>=2]
 k=TEMPLATES[t]['kind']
 if k=='square':return [{'n':n}for n in range(3,32,2)]
 if k=='integer_square':return [{'n':n}for n in range(1,16)]
 if k in ('linear','power'):return [{'n':n}for n in range(2,32)]
 if k=='sum':return [{'a':a,'b':b}for a in range(2,13)for b in range(2,13)]
 d=int(k[-1]);return [{'n':n}for n in range(d+1,32)if math.gcd(n,d)==1]

def substitute(text,p):
 if text is None:return None
 slots={**p}
 if 'n'in p:slots.update(square=p['n']**2,twice=2*p['n'],squarecoef=''if p['n']==1 else str(p['n']**2),ncoef=''if p['n']==1 else str(p['n']))
 for k,v in slots.items():text=text.replace('@@'+k+'@@',str(v))
 if '@@'in text:raise ValueError('unfilled mask')
 return text

def log_solution(integral,coef,first):
 """Shared source constant-rewrite prose and the ordered factor/log-sum rows."""
 return first+"\n\nLastly, let's rewrite the constant so that we can combine it with the natural logarithm. For any constant $C,$ we can always write $C="+coef+r'\ln K$ where $K$ is some other positive constant. Doing this allows us to combine the constant with $'+coef+r'\ln|x|$ term, and we get'+"\n\n$$\n"+r'\begin{aligned}\int '+integral+r'\,\text{d}x & ='+coef+r'\ln|x|+C \\ & ='+coef+r'\ln|x|+'+('('+coef+')'if coef.startswith('-')else coef)+r'\ln K \\ & ='+coef+r'(\ln|x|+\ln K) \\ & ='+coef+r'\ln(K|x|).\end{aligned}'+"\n$$"

def build(t,p,raw):
 if t=='easy_integer':
  n=p['n'];integral=(str(n)if n>0 else '-'+str(-n));f=r'\frac{'+str(abs(n))+'}{x}';f=('-'if n<0 else '')+f;c=str(n)
  first='First, we apply the constant factor rule and take the coefficient $'+c+r'$ out of the integral. Then we compute the integral of $\frac{1}{x},$ and get'+"\n\n$$\n"+r'\begin{aligned}\int '+f+r'\,\text{d}x & ='+c+r'\int \frac{1}{x}\,\text{d}x \\ & ='+c+r'\ln|x|+C.\end{aligned}'+"\n$$"
  sol=log_solution(f,c,first);cwrap='('+c+')'if n<0 else c
  values=[c+r'\ln(K|x|)',str(-n)+r'\ln(K|x|)',r'\frac{1}{'+str(n)+r'}\ln(K|x|)',r'\ln(K|x|)',c+r'\ln(|x|+K)']
  return 'What is the antiderivative of $'+f+'?$',sol,values,0
 v=TEMPLATES[t];problem=substitute(v['problem'],p);sol=substitute(v['solution'],p);values=[substitute(a,p)for a in v['values']]
 if t=='q-49067'and not raw:values=[s.replace('|K|x','K|x|')for s in values]
 if t=='q-103603'and not raw:values[4]=r'-\ln(K|x|)' # replace one duplicate constant-family distractor
 if t=='q-49096'and not raw:
  a,b=p['a'],p['b'];f=r'\frac{'+str(a)+' + '+str(b)+r'x}{x}';A=str(a);B=str(b)
  sol='We separate the integrand into the sum of two fractions so that we can simplify each term. So, we get\n\n$$\n'+r'\begin{aligned}\int '+f+r'\,\text{d}x & =\int (\frac{'+A+r'}{x}+\frac{'+B+r'x}{x})\,\text{d}x \\ & =\int (\frac{'+A+r'}{x}+'+B+r')\,\text{d}x \\ & ='+A+r'\int \frac{1}{x}\,\text{d}x+'+B+r'\int \,\text{d}x \\ & ='+A+r'\ln|x|+'+B+r'x+C.\end{aligned}'+'\n$$\n\n'+"Lastly, let's rewrite the constant so that we can combine it with the natural logarithm. For any constant $C,$ we can always write $C="+A+r'\ln K$ where $K$ is some other positive constant. Doing this allows us to combine the constant with $'+A+r'\ln|x|$ term, and we get'+'\n\n$$\n'+r'\begin{aligned}\int '+f+r'\,\text{d}x & ='+A+r'\ln|x|+'+B+r'x+C \\ & ='+A+r'\ln|x|+'+B+r'x+'+A+r'\ln K \\ & ='+A+r'\ln(K|x|)+'+B+r'x.\end{aligned}'+'\n$$'
 return problem,sol,values,v['correct_index']

def primitive(t,p):
 """Compute the correct arbitrary-constant family before constructing its bank."""
 n=sp.Integer(p.get('n',0));L=sp.log(K*sp.Abs(X))
 if t=='easy_integer':return n*L
 k=TEMPLATES[t]['kind']
 if k=='square':return X-n**2/(4*X)+n*L
 if k=='integer_square':return X-n**2/X+2*n*L
 if k=='linear':return n*X-L
 if k=='power':return n*L
 if k=='sum':return p['a']*L+p['b']*X
 return (-1 if k.startswith('negative')else 1)*sp.Rational(n,int(k[-1]))*L

def integral(t,p):
 n=sp.Integer(p.get('n',0))
 if t=='easy_integer':return n/X
 kind=TEMPLATES[t]['kind']
 if kind=='square':return (1+n/(2*X))**2
 if kind=='integer_square':return (1+n/X)**2
 if kind=='power':return n/X
 if kind=='linear':return n-1/X
 if kind=='sum':return p['a']/X+p['b']
 return (-1 if kind.startswith('negative')else 1)*n/(int(kind[-1])*X)

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if type(level)!=str or level not in SUPPORTED_LEVELS:raise ValueError('difficulty must be easy, moderate or hard')
 if type(seed)!=int:raise TypeError('seed must be an integer, not bool')
 if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('only observed radio fields supported')
 if profile not in (None,'source','normal'):raise ValueError('profile must be source or normal')
 if template is not None and type(template)!=str:raise TypeError('template must be a string')
 rng=random.Random(seed);available=['easy_integer']if level=='easy'else[t for t,v in TEMPLATES.items()if v['level']==level]
 if template is None:
  if parameters is not None:raise ValueError('explicit parameters require an explicit template')
  template=rng.choice(available)
 if template not in available:raise ValueError('template/difficulty mismatch')
 raw=profile=='source'
 if raw and template=='easy_integer':raise ValueError('easy is authored, no source profile')
 if parameters is not None:
  if type(parameters)!=dict or any(type(v)!=int for v in parameters.values()):raise TypeError('parameters must be a dictionary of strict integers')
  p=dict(parameters)
 else:p=dict(rng.choice(domain(template)))
 if p not in domain(template):raise ValueError('parameters outside finite workload domain')
 correct_family=primitive(template,p)
 problem,sol,values,ci=build(template,p,raw)
 # Raw strings remain evidence; normal strings are normalized with the frozen formatter.
 if not raw:
  problem=FORMAT.normalize_prose(normalize(problem));sol=FORMAT.normalize_prose(normalize(sol));values=[FORMAT.normalize_tex(normalize(v))for v in values]
 key=json.dumps([VERSION,level,problem,sol,sorted(values),values[ci]],sort_keys=True);qid=uid('question:'+key);fid=uid('field:'+qid)
 answers=[{':answer/id':uid('answer:'+fid+':'+v),':answer/type':':answer.type/math',':answer/value':v}for v in values]
 correct=answers[ci][':answer/id'];rng.shuffle(answers)
 f={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers}
 if not(raw and template=='q-49096'):f[':answer-field/correct']=[':answer/id',correct]
 q={':question/id':qid,':question/problem':problem,':question/answer-fields':[f]}
 if sol is not None:q[':question/worked-solution']=sol
 if not(raw and template=='q-49096'):q[':question/difficulty']=':question.difficulty/'+level
 fp=hashlib.sha256(sp.srepr(sp.cancel(integral(template,p))).encode()).hexdigest()
 r={'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'template':template,'bank_profile':'source'if raw else 'normal','parameters':p,'correct_family':str(correct_family),'parameter_fingerprint':fp,'mathematical_fingerprint':fp,'source_basis':SOURCE['basis'],'lineage':SOURCE['lineage'],'evidence_only':raw,'eligible_for_learning':not raw,'authorship':'authored easy extension'if template=='easy_integer'else'parameterized original MA family; normal repairs documented','domain':{'x':'either connected interval (-infinity,0) or (0,infinity)','K':'arbitrary positive constant; independent constant on each interval'},'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__},'plot_requirements':'none'}}
 if not raw:FORMAT.validate_generated_record(r)
 return r

def generate_easy(seed=0,**kwargs):
 """Authored integer reciprocal coefficients, absolute values 2..24."""
 return generate('easy',seed,**kwargs)
def generate_moderate(seed=0,**kwargs):
 """Observed rational/power/linear numerator families, source coefficient ceiling31."""
 return generate('moderate',seed,**kwargs)
def generate_hard(seed=0,**kwargs):
 """Observed integer and half-integer binomial-square families, same expansion workload."""
 return generate('hard',seed,**kwargs)
def batch(level,count,seed=0,template=None,profile=None):
 if type(count)!=int or count<0:raise ValueError('count must be a nonnegative integer')
 if type(seed)!=int:raise TypeError('seed must be integer')
 if level not in SUPPORTED_LEVELS:raise ValueError('invalid level')
 if template is not None and (type(template)!=str or template not in (['easy_integer']if level=='easy'else[t for t,v in TEMPLATES.items()if v['level']==level])):raise ValueError('unsupported template/level')
 ts=([template]if template else ['easy_integer']if level=='easy'else[t for t,v in TEMPLATES.items()if v['level']==level]);pool=[(t,p)for t in ts for p in domain(t)];random.Random(seed).shuffle(pool);rows=[];seen=set()
 for t,p in pool:
  r=generate(level,seed,t,parameters=p,profile=profile);fp=r['generation']['parameter_fingerprint']
  if fp not in seen:rows.append(r);seen.add(fp)
  if len(rows)==count:break
 if count==0:return []
 if len(rows)<count:raise ValueError('requested count exceeds finite mathematical task capacity')
 return rows

def markdown(r):
 q=r['question'];return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$'for a in q[':question/answer-fields'][0][':answer-field/choices'])+'\n\n'+q.get(':question/worked-solution','[Captured source omits a worked solution.]')
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=(*SUPPORTED_LEVELS,'all'),default='all');ap.add_argument('--count',type=int,default=2);ap.add_argument('--seed',type=int,default=0);ap.add_argument('--format',choices=('json','markdown'),default='json');ap.add_argument('--template');ap.add_argument('--profile',choices=('source','normal'));a=ap.parse_args();rows=[r for level in(SUPPORTED_LEVELS if a.difficulty=='all'else[a.difficulty])for r in batch(level,a.count,a.seed,a.template,a.profile)];print(json.dumps(rows,indent=2)if a.format=='json'else'\n\n---\n\n'.join(map(markdown,rows)))
