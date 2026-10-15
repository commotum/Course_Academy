"""Product-trig identity integration: full source families and bounded exact slots.

Local draft only; no EDB access. Every bank profile is selected before parameters.
"""
import sys
sys.dont_write_bytecode = True
import argparse, functools, hashlib, importlib.util, json, random, re, uuid
from pathlib import Path
import sympy as s
HERE=Path(__file__).with_suffix('')
def private(name,file):
 spec=importlib.util.spec_from_file_location(name,HERE/file);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
fmt=private('product_format','math_format.py');P=private('product_scalar','ode-scalar-parser.py')
x,u=P.x,P.u; C=P.v
SOURCE=json.loads((HERE/'source.json').read_text());KP=SOURCE['record'];KP_ID=17592186064225;VERSION='product-trig-identities-1.0.0'
SOURCES={q[':question/math-academy-id']:q for q in KP[':knowledge-point/questions']}
# Source profile (one complete bank per profile), family, original parameters.
CASES=[('q-49070','tan-sum',dict(a=1,b=2)),('q-49271','cot-square',dict(a=1,b=1)),('q-114304','cos-tan',dict(k=1,l=0,h=3)),('q-352491','sec-difference',dict(a=8,b=1,k=5,l=-4,h=0)),('q-352703','cos-tan',dict(k=1,l=0,h=4)),('q-352708','reciprocal-sec',dict(a=2,b=1,l=0,h=3)),('q-352710','reciprocal-sec',dict(a=3,b=1,l=0,h=3)),('q-49258','cot-sin',dict(n=4)),('q-49272','cot-difference',dict(a=1,b=1)),('q-49274','tan-cos',dict(n=2)),('q-51109','scaled-cos-tan',dict(k=2,l=0,h=4)),('q-114301','cot-csc',dict(a=3,b=2)),('q-358219','sec-cos-square',dict(a=3,k=2,l=0,h=4)),('q-358220','reciprocal-cos-square',dict(a=9,k=3,l=3,h=4))]
PROFILES={q:(f,p)for q,f,p in CASES}
ANGLES={-4:-s.pi/3,-3:-s.pi/4,-2:-s.pi/6,0:s.Integer(0),2:s.pi/6,3:s.pi/4,4:s.pi/3}
SUPPORTED_LEVELS=('easy','moderate','hard')
def level(profile):return SOURCES[profile][':question/difficulty'][':db/ident'].split('/')[-1]
def tex(e):return fmt.normalize_tex(s.latex(s.sympify(e)))
def fn(f,z='x',power=1):return '\\'+f+(('^{'+str(power)+'}')if power!=1 else'')+'('+z+')'
def mul(c,t):
 if t=='1':return tex(c)
 if c==1:return t
 if c==-1:return '-'+t
 return tex(c)+r'\,'+t

def add(*terms):
 out=''
 for c,t in terms:
  if c==0:continue
  a=mul(c,t)
  out+=('+'if out and not a.startswith('-')else'')+a
 return out or '0'
def integ(body,var='x',lo=None,hi=None):return r'\int'+('_{'+tex(lo)+'}^{'+tex(hi)+'}'if lo is not None else'')+' '+body+r'\,\text{d}'+var

def aligned(stages):return '$$\n'+r'\begin{aligned}'+stages[0]+' &='+(' \\\\ &='.join(stages[1:]))+r'\end{aligned}'+'\n$$'
def scalar(t):return P.scalar(re.sub(r'(?<![A-Za-z])C(?![A-Za-z])','v',t))
def exact(e):
 # One rational parametrization for every *actual identical argument*;
 # all stages here use the same k*x or u, so this proves rational trig equality.
 args={z.args[0]for z in e.atoms(s.sin,s.cos,s.tan,s.cot,s.sec,s.csc)}
 for j,a in enumerate(args):
  z=s.Symbol('q'+str(j),real=True);sn=2*z/(1+z*z);co=(1-z*z)/(1+z*z)
  e=e.xreplace({s.sin(a):sn,s.cos(a):co,s.tan(a):sn/co,s.cot(a):co/sn,s.sec(a):1/co,s.csc(a):1/sn})
 return s.cancel(e)==0

def constraints(profile,p):
 if profile not in PROFILES:raise ValueError('unknown source profile')
 f,base=PROFILES[profile]
 if set(p)!=set(base)or any(type(v)is not int for v in p.values()):raise ValueError('exact builtin integer slots required')
 for v in ('a','b'):
  if v in p and not 1<=p[v]<=(9 if level(profile)=='hard' and v=='a'else 5):raise ValueError('coefficient outside declared bounds')
 if 'n'in p and not 2<=p['n']<=9:raise ValueError('denominator must be 2..9; 1 would duplicate omit-factor distractor')
 if 'k'in p and not (p['k']==1 if f=='cos-tan'else 2<=p['k']<=6):raise ValueError('frequency outside profile scope')
 if 'l'in p and (p['l']not in ANGLES or p['h']not in ANGLES or p['l']>=p['h']):raise ValueError('ordered pole-free angle slots required')
 return f

def easy(profile,p):
 f=constraints(profile,p);a=p.get('a',1);b=p.get('b',1);n=p.get('n',1)
 sn,co,ta,ct,se,cs=[fn(z)for z in ('sin','cos','tan','cot','sec','csc')]
 identity={'tan-sum':ta+'='+r'\frac{'+sn+'}{'+co+'}', 'cot-square':fn('cot',power=2)+'='+r'\frac{'+fn('cos',power=2)+'}{'+fn('sin',power=2)+'}', 'cot-sin':ct+'='+r'\frac{'+co+'}{'+sn+'}', 'tan-cos':ta+'='+r'\frac{'+sn+'}{'+co+'}', 'cot-difference':ct+'='+r'\frac{'+co+'}{'+sn+'},$ and $'+ta+'='+r'\frac{'+sn+'}{'+co+'}', 'cot-csc':ct+'='+r'\frac{'+co+'}{'+sn+'}'}[f]
 I=lambda z:integ(z)
 if f=='tan-sum':
  body=ta+'('+add((a,se),(b,co))+')';simple=add((a,se+ta),(b,sn));F=a*s.sec(x)-b*s.cos(x)
  stages=[I(body),I('('+add((a,ta+se),(b,ta+r'\cdot '+co))+')'),I('('+add((a,se+ta),(b,r'\frac{'+sn+'}{'+co+r'}\cdot '+co))+')'),I('('+simple+')'),add((a,I(se+ta)),(b,I(sn))),tex(F)+'+C']
  bank=[F,a*s.tan(x)-b*s.sin(x),-a*s.tan(x)+b*s.sin(x),a*s.sec(x)+b*s.cos(x)]
 elif f=='cot-square':
  factor=r'\frac{1}{'+fn('cos',power=2)+'}';term=fn('cos',power=2)+sn
  body=factor+'('+add((a,fn('cot',power=2)),(b,term))+')';F=-a*s.cot(x)-b*s.cos(x)
  stages=[I(body),I('('+add((a,factor+r'\cdot '+fn('cot',power=2)),(b,factor+r'\cdot '+term))+')'),I('('+add((a,factor+r'\cdot \frac{'+fn('cos',power=2)+'}{'+fn('sin',power=2)+'}'),(b,factor+r'\cdot '+term))+')'),I('('+add((a,r'\frac{1}{'+fn('sin',power=2)+'}'),(b,sn))+')'),I('('+add((a,fn('csc',power=2)),(b,sn))+')'),add((a,I(fn('csc',power=2))),(b,I(sn))),tex(F)+'+C']
  bank=[a*s.cot(x)+b*s.cos(x),a*s.tan(x)+b*s.cos(x),a*s.cot(x)-b*s.cos(x),-a*s.tan(x)-b*s.cos(x),F]
 elif f in ('cot-sin','tan-cos'):
  first,second,target=(ct,sn,co)if f=='cot-sin'else(ta,co,sn);body=r'\frac{'+first+second+'}{'+str(n)+'}';F=s.sin(x)/n if f=='cot-sin'else-s.cos(x)/n
  substitute=r'\frac{'+(co if f=='cot-sin'else sn)+'}{'+second+r'}\cdot \frac{'+second+'}{'+str(n)+'}'
  stages=[I(body),I(substitute),I(r'\frac{'+target+'}{'+str(n)+'}'),mul(s.Rational(1,n),I(target)),tex(F)+'+C']
  bank=[s.sin(x),F,s.tan(x)/n,s.sec(x),s.cos(x)/n]if f=='cot-sin'else[-s.cos(x),-s.sin(x)/n,s.sin(x),F,s.cos(x)/n]
 elif f=='cot-difference':
  body=ct+'('+add((a,sn),(-b,ta))+')';F=a*s.sin(x)-b*x
  stages=[I(body),I('('+add((a,ct+r'\cdot '+sn),(-b,ct+r'\cdot '+ta))+')'),I('('+add((a,r'\frac{'+co+'}{'+sn+r'}\cdot '+sn),(-b,r'\frac{'+co+'}{'+sn+r'}\cdot \frac{'+sn+'}{'+co+'}'))+')'),I('('+add((a,co),(-b,'1'))+')'),tex(F)+'+C']
  bank=[F,a*s.cos(x)-b*x,a*s.sin(x),-a*s.sin(x)-b*x,-a*s.cos(x)-b*x]
 elif f=='cot-csc':
  body=ct+'('+add((a,sn),(-b,cs))+')';F=a*s.sin(x)+b*s.csc(x)
  stages=[I(body),I('('+add((a,ct+r'\cdot '+sn),(-b,ct+r'\cdot '+cs))+')'),I('('+add((a,r'\frac{'+co+'}{'+sn+r'}\cdot '+sn),(-b,ct+r'\cdot '+cs))+')'),I('('+add((a,co),(-b,cs+ct))+')'),add((a,I(co)),(-b,I(cs+ct))),add((a,sn),(-b,'(-'+cs+')'))+'+C',tex(F)+'+C']
  bank=[-a*s.sin(x)-b*s.csc(x),F,a*s.cos(x)+b*s.sec(x),a*s.cos(x)-b*s.cot(x),a*s.sin(x)-b*s.cot(x)]
 prose=('We use the identity 'if f in('cot-sin','tan-cos')else'We multiply out the parentheses and then use the '+('identities 'if f=='cot-difference'else'identity '))+'$'+identity+',$ as follows:'
 prompt=('Calculate $'+I(body)+'.$')if f in('cot-sin','tan-cos')else'$'+I(body)+'=$'
 return prompt,prose+'\n\n'+aligned(stages),bank,F,(s.srepr(s.trigsimp(scalar(body).rewrite(s.sin))),None,None),{'exclusions':['sin(x)=0']if f in('cot-sin','cot-csc')else['cos(x)=0']if f in('tan-sum','tan-cos')else['sin(x)=0','cos(x)=0']}

def definite(profile,p):
 f=constraints(profile,p);a=p.get('a',1);b=p.get('b',1);k=p.get('k',1);L,H=ANGLES[p['l']],ANGLES[p['h']];lo,hi=L/k,H/k;z=tex(k*x);J=lambda t:integ(t,'x',lo,hi)
 sn,co,ta,se=[fn(t,z)for t in('sin','cos','tan','sec')];sub=f in('scaled-cos-tan','sec-difference','sec-cos-square','reciprocal-cos-square')
 if f in('cos-tan','scaled-cos-tan'):
  body=co+ta;simple=sn;G=-s.cos(u);first=[J(body),J(co+r'\cdot \frac{'+sn+'}{'+co+'}'),J(sn)]
  identity=ta+'='+r'\frac{'+sn+'}{'+co+'}'
 elif f=='reciprocal-sec':
  body=r'\frac{1}{'+se+'}('+add((a,'1'),(-b,ta))+')';simple=add((a,co),(-b,sn));G=a*s.sin(u)+b*s.cos(u)
  first=[J(body),J(co+'('+add((a,'1'),(-b,r'\frac{'+sn+'}{'+co+'}'))+')'),J('('+simple+')')];identity=(r'\frac{1}{'+se+'}='+co if profile=='q-352710'else se+'='+r'\frac{1}{'+co+'}')+'$ and $'+ta+'='+r'\frac{'+sn+'}{'+co+'}'
 elif f=='sec-difference':
  body=mul(a,se+'('+add((1,ta),(-b,fn('cos',z,2)))+')');simple=add((1,se+ta),(-b,co));G=s.Rational(a,k)*(s.sec(u)-b*s.sin(u))
  first=[J(body),mul(a,J('('+add((1,se+ta),(-b,r'\frac{1}{'+co+r'}\cdot '+fn('cos',z,2)))+')')),mul(a,J('('+simple+')'))];identity=r'\sec(x)=\frac{1}{\cos(x)}'
 elif f=='sec-cos-square':
  body=mul(a,se+fn('cos',z,2));simple=co;G=s.Rational(a,k)*s.sin(u)
  first=[J(body),mul(a,J(r'\frac{1}{'+co+r'}\cdot '+fn('cos',z,2))),mul(a,J(co))];identity=r'\sec(x)=\frac{1}{\cos(x)}'
 else:
  body=r'\frac{'+str(a)+'}{'+fn('cos',z,2)+'}';simple=fn('sec',z,2);G=s.Rational(a,k)*s.tan(u)
  first=[J(body),J(mul(a,r'(\frac{1}{'+co+'})^{2}')),J(mul(a,simple)),mul(a,J(simple))];identity=r'\frac{1}{'+co+'}='+se
 if f=='scaled-cos-tan':G/=k
 answer=s.simplify(G.subs(u,H)-G.subs(u,L));coefficient=a if f in('sec-difference','sec-cos-square','reciprocal-cos-square')else 1
 simple_u=simple.replace(z,'u');Iu=integ('('+simple_u+')'if f=='sec-difference'else simple_u,'u',L,H)
 variable=u if sub else x;gv=G if sub else G.subs(u,x);bl,bh=(L,H)if sub else(lo,hi)
 primitive=tex(gv)+r'\big|_{'+tex(bl)+'}^{'+tex(bh)+'}'
 # Preserve each source's endpoint factoring and arithmetic, including its
 # unevaluated individual primitive components before collection.
 def uneval_primitive(arg):
  sn_,co_,se_,ta_=[fn(z,tex(arg))for z in('sin','cos','sec','tan')]
  if f in('cos-tan','scaled-cos-tan'):return co_
  if f=='reciprocal-sec':return add((a,sn_),(b,co_))
  if f=='sec-difference':return add((1,se_),(-b,sn_))
  return sn_ if f=='sec-cos-square'else ta_
 def evaluated_primitive(arg):
  if f in('cos-tan','scaled-cos-tan'):return tex(s.cos(arg))
  if f=='reciprocal-sec':return add((a,'('+tex(s.sin(arg))+')'),(b,'('+tex(s.cos(arg))+')'))
  if f=='sec-difference':return add((1,'('+tex(s.sec(arg))+')'),(-b,'('+tex(s.sin(arg))+')'))
  return tex(s.sin(arg))if f=='sec-cos-square'else tex(s.tan(arg))
 scale=-s.Rational(1,k)if f in('cos-tan','scaled-cos-tan')else s.Integer(1)if f=='reciprocal-sec'else s.Rational(a,k)
 if f in('cos-tan','scaled-cos-tan','sec-cos-square','reciprocal-cos-square'):
  endpoint=mul(scale,'('+uneval_primitive(H)+'-'+uneval_primitive(L)+')')
  evaluated=mul(scale,'('+evaluated_primitive(H)+'-'+evaluated_primitive(L)+')')
 else:
  endpoint=mul(scale,'('+uneval_primitive(H)+')')+'-'+mul(scale,'('+uneval_primitive(L)+')')
  evaluated=mul(scale,'('+evaluated_primitive(H)+')')+'-'+mul(scale,'('+evaluated_primitive(L)+')')
 tail=[primitive,endpoint,evaluated]
 if profile=='q-114304':
  A,B=s.cos(L),s.cos(H);tail += [tex(s.Add(A,-B,evaluate=False)),r'\frac{'+tex(s.Add(2*A,-2*B,evaluate=False))+'}{2}']
 else:tail.append(tex(answer))

 if sub:
  body_u=Iu+r'\cdot \frac{1}{'+str(k)+r'}'
  # Put differential factor inside the integral as in the source.
  body_u=integ(('('+simple_u+')'if f=='sec-difference'else simple_u)+r'\cdot \frac{1}{'+str(k)+'}','u',L,H)
  stages=[mul(coefficient,J('('+simple+')'if f=='sec-difference'else simple)),mul(coefficient,body_u),mul(s.Rational(coefficient,k),Iu),*tail]
  prose=('First, we multiply out the parentheses and then use the identity 'if f=='sec-difference'else'First, we use the identity 'if f=='reciprocal-cos-square'else'We use the identity ')+'$'+identity+'$ as follows:'
  sol=prose+'\n\n'+aligned(first)+'\n\nWe can solve this by substitution. Let $u='+tex(k*x)+r'.$ Then $\text{d}x=\frac{1}{'+str(k)+r'}\text{d}u.$'+'\n\nNow, we fill the table for the limits of integration, according to the rule $u='+tex(k*x)+'.$\n\n| $x$ | $'+tex(lo)+'$ | $'+tex(hi)+'$ |\n| --- | --- | --- |\n| $u$ | $'+tex(L)+'$ | $'+tex(H)+'$ |\n\nTherefore, the integral in terms of the new variable is\n\n'+aligned(stages)
 else:
  sol='We use the identity $'+identity+',$ as follows:\n\n'+aligned(first+tail)
 if profile=='q-114304':
  A,B=s.cos(L),s.cos(H);bank=[A-B,A-2*B,A/2-B,4*B-2*A,2*B+2*A]
 elif profile=='q-51109':
  D=s.cos(L)-s.cos(H);bank=[D,-2*D,-D,D/k,-D/k]
 else:bank=[answer]
 field=SOURCES[profile][':question/answer-fields'][0];blank=field[':answer-field/type'][':db/ident'].endswith('/blank');prompt=('Evaluate the following integral. Do not round the answer.\n\n'if blank else'')+'$'+J(body)+'=$'+('\n{{field-1}}'if blank else'')
 return prompt,sol,bank,answer,(s.srepr(s.trigsimp(scalar(body).rewrite(s.sin))),s.srepr(lo),s.srepr(hi)),{'exclusions':['cos('+tex(k*x)+')=0'],'interval':[tex(lo),tex(hi)],'transformed_interval':[tex(L),tex(H)]}

def uid(t):return str(uuid.uuid5(uuid.UUID(KP[':knowledge-point/id']),t))

def sample_parameters(profile,rng):
 f,base=PROFILES[profile];p={}
 for key in base:
  if key in('a','b'):p[key]=rng.randint(1,9 if level(profile)=='hard'and key=='a'else 5)
  elif key=='n':p[key]=rng.randint(2,9)
  elif key=='k':p[key]=1 if f=='cos-tan'else rng.randint(2,6)
 if 'l'in base:p['l'],p['h']=sorted(rng.sample(list(ANGLES),2))
 return p

def generate(difficulty,seed=0,template=None,parameters=None,bank_profile=None,profile=None):
 if difficulty not in SUPPORTED_LEVELS:raise ValueError('unsupported difficulty')
 if type(seed)is not int:raise ValueError('seed must be a builtin integer')
 if profile is not None and bank_profile is not None and profile!=bank_profile:raise ValueError('conflicting profile arguments')
 rng=random.Random(seed);profile=profile or bank_profile or template or rng.choice([q for q in PROFILES if level(q)==difficulty])
 if profile not in PROFILES or level(profile)!=difficulty or template not in(None,profile,PROFILES[profile][0]):raise ValueError('profile/difficulty mismatch')
 explicit=parameters is not None
 for attempt in range(200):
  p=dict(parameters)if explicit else sample_parameters(profile,rng);f=constraints(profile,p)
  prompt,solution,bank,correct,assessed_math,domain=easy(profile,p)if difficulty=='easy'else definite(profile,p)
  compare=(lambda a,b:exact(s.diff(a-b,x)))if difficulty=='easy'else(lambda a,b:s.simplify(a-b)==0)
  chosen=[i for i,z in enumerate(bank)if compare(z,correct)]
  if len(chosen)==1 and all(not compare(a,b)for i,a in enumerate(bank)for b in bank[i+1:]):break
  if explicit:raise ValueError('whole selected profile collides at parameters')
 else:raise ValueError('no eligible instance')
 prompt=fmt.normalize_prose(prompt);solution=fmt.normalize_prose(solution);values=[fmt.normalize_tex(tex(z)+(r'+C'if difficulty=='easy'else''))for z in bank]
 task=hashlib.sha256(json.dumps([difficulty,assessed_math,domain],sort_keys=True).encode()).hexdigest();identity=hashlib.sha256(json.dumps([task,profile,values],sort_keys=True).encode()).hexdigest();qid=uid(identity);fid=uid(qid+':field')
 answers=[{':answer/id':uid(fid+':'+v),':answer/type':':answer.type/math',':answer/value':v}for v in values]
 oldf=SOURCES[profile][':question/answer-fields'][0]
 q={':question/id':qid,':question/problem':prompt,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+difficulty,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':oldf[':answer-field/key'],':answer-field/type':oldf[':answer-field/type'][':db/ident'],':answer-field/choices':answers,':answer-field/correct':[':answer/id',answers[chosen[0]][':answer/id']]}]}
 rec={'knowledge_point':{'db_id':KP_ID,'id':KP[':knowledge-point/id'],'title':KP[':knowledge-point/title']},'question':q,'generation':{'version':VERSION,'seed':seed,'template':profile,'family':f,'bank_profile':profile,'parameters':p,'source_basis':SOURCE['basis'],'source_lineage':SOURCE['lineage'],'source_question':profile,'domain':domain,'task_fingerprint':task,'mathematical_task_fingerprint':task,'content_fingerprint':identity,'dependencies':{'python':sys.version.split()[0],'sympy':s.__version__},'eligible_for_learning':True,'recipe_policy':'One complete observed profile; symbolic slots; opaque interpretations explicitly unresolved in ledger.'}}
 for text in(prompt,solution,*values):
  if any(ord(c)<32 and c not in'\n\t\r'for c in text):raise ValueError('unintended control byte')
 return fmt.validate_generated_record(rec)

def batch(difficulty,count=1,seed=0):
 if difficulty not in(*SUPPORTED_LEVELS,'all'):raise ValueError('unsupported difficulty')
 if type(count)is not int or count<1:raise ValueError('count must be a positive builtin integer')
 if type(seed)is not int:raise ValueError('seed must be a builtin integer')
 out=[]
 for lev in SUPPORTED_LEVELS if difficulty=='all'else(difficulty,):
  seen=set();made=[];rng=random.Random(str(seed)+lev)
  for attempt in range(max(2000,count*300)):
   rec=generate(lev,rng.randrange(2**63));fp=rec['generation']['task_fingerprint']
   if fp not in seen:seen.add(fp);made.append(rec)
   if len(made)==count:break
  if len(made)!=count:raise ValueError('requested batch exceeds bounded task capacity')
  out.extend(made)
 return out
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=(*SUPPORTED_LEVELS,'all'),default='all');ap.add_argument('--count',type=int,default=1);ap.add_argument('--seed',type=int,default=0);ap.add_argument('--format',choices=('json','markdown'),default='json');a=ap.parse_args();rows=batch(a.difficulty,a.count,a.seed)
 print(json.dumps(rows,indent=2)if a.format=='json'else'\n\n'.join(r['question'][':question/problem']+'\n\n'+r['question'][':question/worked-solution']for r in rows))
