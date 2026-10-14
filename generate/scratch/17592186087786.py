"""Finding Cartesian equations of parametrized circles. Public seeded JSON/Markdown contract.
Moderate: unshifted; hard: translated radio or three-blank equations. Easy unsupported.
Distinctness uses exact (radius, centre), excluding option order, field style and seed.
"""
import argparse,hashlib,json,random,re,uuid
from pathlib import Path
import sympy as sp
HERE=Path(__file__).with_suffix('');S=json.loads((HERE/'source.json').read_text())
KP_ID=17592186087786;KP_UUID=S['record'][':knowledge-point/id'];VERSION='circle-v1'
SPECS={x['source_id']:x for x in json.loads((HERE/'source-specs.json').read_text())}
SOURCES={q[':question/math-academy-id']:q for q in S['record'][':knowledge-point/questions']}
TEMPLATES=[t for t in SPECS if SPECS[t]['profile']!='unrated'];SUPPORTED_LEVELS=('moderate','hard')
EXCLUDED=[{'source':'q-15799','reason':'Unrated; missing correct-answer link and worked solution. Preserve unchanged; bank independently replayed as evidence only.'}]
x,y,theta=sp.symbols('x y theta',real=True)
def tex(a):return sp.latex(sp.sympify(a))
def fragment(v,c):
 c=sp.sympify(c);return v if c==0 else '('+v+('+' if c<0 else '-')+tex(abs(c))+')'
def eq(h,k,c,sign=1):return fragment('x',h)+'^{2}'+('+' if sign==1 else '-')+fragment('y',k)+'^{2}='+tex(c)
def recipes(profile,r,h,k):
 C=lambda a,b,c,s=1:(a,b,c,s)
 if profile=='origin-a':return [C(h,k,r*r,-1),C(h,k,r,-1),C(h,k,sp.sqrt(r)),C(h,k,r),C(h,k,r*r)]
 if profile=='origin-b':return [C(h,k,r*r),C(h,k,sp.sqrt(r),-1),C(h,k,2*r*r,-1),C(h,k,r),C(h,k,r**4)]
 if profile=='origin-c':return [C(h,k,2*r),C(h,k,r),C(h,k,r*r+r,-1),C(h,k,r*r),C(h,k,sp.sqrt(r),-1)]
 if profile=='translated-a':return [C(-h,-k,r*r),C(h,k,r*r),C(k,h,r*r),C(h,k,r),C(-h,-k,r)]
 if profile=='translated-b':return [C(h,k,sp.sqrt(r)),C(h,k,r*r),C(-h,-k,r),C(-h,-k,r*r),C(h,k,r)]
 if profile=='translated-c':return [C(h,k,r*r),C(k,h,r),C(h,k,r),C(-h,-k,r*r),C(k,-h,4*r)]
 if profile=='translated-d':return [C(-h,-k,r),C(h,k,r*r),C(-h,-k,2*r*r),C(h,k,r),C(-h,-k,r*r)]
 if profile=='translated-e':return [C(h,k,2*r),C(h,k,r*r),C(-h,-k,r*r),C(h,k,r),C(-h,-k,r)]
 if profile=='translated-f':return [C(h,k,r),C(-h,-k,r*r),C(h,r,r*r),C(h,k,r*r),C(-h,-r,r)]
 if profile=='unrated':return [C(h,k,r*r),C(h,k,r),C(-h,-k,r*r),C(-h,-k,2*r),C(h,k,2*r)]
 raise ValueError(profile)
def original(t):return {key:SPECS[t][key] for key in ('r','h','k')}
def parse_math(s):
 s=s.replace('⁡','').replace(' ', '').replace(r'\operatorname{cos}',r'\cos').replace(r'\operatorname{sin}',r'\sin')
 for _ in range(5):
  s=re.sub(r'\\frac\{([^{}]*)\}\{([^{}]*)\}',r'((\1)/(\2))',s)
  s=re.sub(r'\\sqrt\{([^{}]*)\}',r'sqrt(\1)',s)
 s=s.replace('{','(').replace('}',')').replace('^','**')
 from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
 return parse_expr(s,local_dict={'x':x,'y':y},transformations=standard_transformations+(implicit_multiplication_application,))
def polynomial(value):
 a,b=value.split('=');p=sp.Poly(sp.expand(parse_math(a)-parse_math(b)),x,y);return sp.expand(p.as_expr()/p.LC())
def fingerprint(q):
 # Read supplied geometric data; source and generated prompts both supported.
 text=q[':question/problem'].replace(r'\quad',' ').replace('⁡','').replace(r'\operatorname{cos}',r'\cos').replace(r'\operatorname{sin}',r'\sin').replace('θ',r'\theta')
 a=re.search(r'x\s*=\s*(.*?)\\cos\s*\\theta\s*(.*?),\s*(?:\\,)?\s*y\s*=',text,re.S)
 if not a:return 'unparsed:'+hashlib.sha256(q[':question/problem'].encode()).hexdigest()
 b=re.search(r'y\s*=\s*(.*?)\\sin\s*\\theta\s*(.*?),',text,re.S)
 assert b
 r=parse_math(a[1]);h=parse_math(a[2]) if a[2].strip() else sp.Integer(0);k=parse_math(b[2]) if b[2].strip() else sp.Integer(0)
 assert r==parse_math(b[1]) and r>0
 return '|'.join(str(z) for z in (r,h,k))
def shifted(c):return '' if c==0 else ('+' if c>0 else '-')+tex(abs(c))
def sample(t,rng):
 s=SPECS[t];r=rng.choice([sp.Rational(n,d) for n in range(1,15) for d in (1,2) if sp.Rational(n,d)!=1]);h=k=sp.Integer(0)
 if s['difficulty']=='hard':
  # Observed zero/nonzero shift roles stay fixed; nonzero slots vary magnitude and sign.
  vals=[sp.Rational(n,d) for n in range(-13,14) if n for d in (1,2,4)]
  h=rng.choice(vals) if sp.sympify(s['h'])!=0 else sp.Integer(0)
  k=rng.choice(vals) if sp.sympify(s['k'])!=0 else sp.Integer(0)
 return dict(r=str(r),h=str(h),k=str(k))
def generate(difficulty,seed,template=None,parameters=None,replay=False):
 if difficulty not in SUPPORTED_LEVELS:raise ValueError('Unsupported difficulty: '+difficulty)
 rng=random.Random(seed);t=template or rng.choice([t for t in TEMPLATES if SPECS[t]['difficulty']==difficulty]);s=SPECS[t]
 assert s['difficulty']==difficulty
 for _ in range(1000):
  p=parameters or sample(t,rng);r,h,k=[sp.sympify(p[a]) for a in ('r','h','k')]
  assert r>0 and (difficulty!='moderate' or h==k==0)
  if difficulty=='hard':assert h!=0 or k!=0
  bank=[] if s['profile']=='blank' else [eq(*rec) for rec in recipes(s['profile'],r,h,k)]
  if not bank or len(set(map(polynomial,bank)))==len(bank) and sum(polynomial(v)==polynomial(eq(h,k,r*r)) for v in bank)==1:break
  if parameters:raise ValueError('Colliding bank')
 else:raise ValueError('No valid parameters')
 identity=VERSION+'|'+str(r)+'|'+str(h)+'|'+str(k)+'|'+s['profile'];qid=str(uuid.uuid5(uuid.UUID(KP_UUID),identity));fields=[]
 def field(key,kind,vals,correct):
  fid=str(uuid.uuid5(uuid.UUID(qid),'field:'+key));answers=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),'value:'+v)),':answer/type':':answer.type/math',':answer/value':v} for v in vals]
  aid=next(a[':answer/id'] for a in answers if a[':answer/value']==correct)
  fields.append({':answer-field/id':fid,':answer-field/key':key,':answer-field/type':kind,':answer-field/choices':answers,':answer-field/correct':[':answer/id',aid]})
 head=('Calculate' if difficulty=='moderate' else 'Determine')+' the Cartesian equation of the circle\n\n$$\nx='+tex(r)+r'\cos\theta'+shifted(h)+r',\quad y='+tex(r)+r'\sin\theta'+shifted(k)+r',\quad 0\leq\theta<2\pi.'+'\n$$'
 if s['profile']=='blank':
  head='The Cartesian equation of the circle defined by the parametric equations\n\n'+head.split('\n\n',1)[1]+'\n\nis given by\n\n$(x'+('-' if h>=0 else '+')+'$ {{field-1}} $)^{2}+(y'+('-' if k>=0 else '+')+'$ {{field-2}} $)^{2}=$ {{field-3}}.'
  for key,v in zip(('field-1','field-2','field-3'),(abs(h),abs(k),r*r)):field(key,':answer-field.type/blank',[tex(v)],tex(v))
 else:field('selection',':answer-field.type/radio',bank,eq(h,k,r*r))
 intro=r'To find the Cartesian equation of the circle, we need to eliminate the parameter $\theta.$ We can do this using the Pythagorean identity:'+'\n\n$$'+r'\cos^2\theta+\sin^2\theta=1.'+'$$'
 A,B=fragment('x',h),fragment('y',k)
 if difficulty=='moderate':
  sol=intro+'\n\nBy squaring the $x$-equation, we get\n\n$$'+r'\begin{aligned}x&='+tex(r)+r'\cos\theta\\x^2&=('+tex(r)+r'\cos\theta)^2\\&='+tex(r*r)+r'\cos^2\theta.\end{aligned}$$'+'\n\nBy squaring the $y$-equation, we get\n\n$$'+r'\begin{aligned}y&='+tex(r)+r'\sin\theta\\y^2&=('+tex(r)+r'\sin\theta)^2\\&='+tex(r*r)+r'\sin^2\theta.\end{aligned}$$'+'\n\nAdding the two equations and using the identity, we get\n\n$$'+r'\begin{aligned}x^2+y^2&='+tex(r*r)+r'\cos^2\theta+'+tex(r*r)+r'\sin^2\theta\\&='+tex(r*r)+r'(\cos^2\theta+\sin^2\theta)\\&='+tex(r*r)+r'(1)\\&='+tex(r*r)+r'.\end{aligned}$$'
 else:
  sol=intro
  for v,F,fn in [('x',A,'cos'),('y',B,'sin')]:
   sol+='\n\nBy isolating the $\\'+fn+r'\theta$ term in the $'+v+'$-equation and squaring, we get\n\n$$'+r'\begin{aligned}'+F+'&='+tex(r)+'\\'+fn+r'\theta\\'+tex(1/r)+F+'&=\\'+fn+r'\theta\\'+tex(1/(r*r))+F+'^{2}&=\\'+fn+r'^2\theta.\end{aligned}$$'
  sol+='\n\nAdding the two equations and using the identity, we get\n\n$$'+r'\begin{aligned}'+tex(1/(r*r))+A+'^{2}+'+tex(1/(r*r))+B+r'^{2}&=\cos^2\theta+\sin^2\theta\\&=1\\'+A+'^{2}+'+B+'^{2}&='+tex(r*r)+r'.\end{aligned}$$'
 sol+='\n\nTherefore the Cartesian equation is $'+eq(h,k,r*r)+'.$'
 q={':question/id':qid,':question/problem':head,':question/worked-solution':sol,':question/difficulty':':question.difficulty/'+difficulty,':question/answer-fields':fields}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':S['record'][':knowledge-point/title']},'question':q,'generation':{'version':VERSION,'seed':seed,'template':t,'profile':s['profile'],'parameters':{a:str(p[a]) for a in ('r','h','k')},'replay':replay,'assets':[],'domain':'r>0, full 0<=theta<2pi; no ellipse or partial arc','mathematical_fingerprint':fingerprint(q),'dependencies':{'sympy':sp.__version__}}}
def batch(difficulty,count,seed):
 if difficulty not in SUPPORTED_LEVELS:raise ValueError('Unsupported difficulty: '+difficulty)
 out=[];seen=set()
 for n in range(count*100+1):
  if len(out)>=count:break
  r=generate(difficulty,seed+n);fp=r['generation']['mathematical_fingerprint']
  if fp not in seen:out.append(r);seen.add(fp)
 if len(out)<count:raise ValueError('Finite sampling limit')
 return out
def markdown(r):return r['question'][':question/problem']+'\n\n'+'\n\n'.join(f[':answer-field/key']+': '+', '.join(a[':answer/value'] for a in f[':answer-field/choices']) for f in r['question'][':question/answer-fields'])+'\n\n'+r['question'][':question/worked-solution']
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--difficulty',required=True);a.add_argument('--count',type=int,default=5);a.add_argument('--seed',type=int,default=0);a.add_argument('--format',choices=['json','markdown'],default='json');p=a.parse_args();rs=batch(p.difficulty,p.count,p.seed);print(json.dumps(rs,indent=2) if p.format=='json' else '\n\n---\n\n'.join(map(markdown,rs)))
