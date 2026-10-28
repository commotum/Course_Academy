#!/usr/bin/env python3
"""Seeded Bernoulli practice with coefficient-role banks and exact source replay."""
import argparse,hashlib,json,random,re,uuid,os,sys
from pathlib import Path
import sympy as sp
KP_ID=17592186147454
HERE=Path(__file__).resolve().with_suffix('')
SNAPSHOT=json.loads((HERE/'source.json').read_text())
NAMESPACE=uuid.UUID(SNAPSHOT['record'][':knowledge-point/id'])
GENERATOR_UUID=str(uuid.uuid5(NAMESPACE,'question-generator'))
VERSION='bernoulli-guided-three-bands-3'
TITLE=SNAPSHOT['record'][':knowledge-point/title']
SOURCES={q[':question/math-academy-id']:q for q in SNAPSHOT['record'][':knowledge-point/questions'] if ':question/worked-solution' in q and all(':answer-field/correct' in f for f in q.get(':question/answer-fields',[]))}
SUPPORTED_LEVELS=('easy','moderate','hard')
ORIGINAL={t:{'shift':0} for t in SOURCES}
SHIFTS=tuple(range(-6,0))+tuple(range(1,7))
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(x):return str(uuid.uuid5(NAMESPACE,x))
def translate(text,h):
 if h==0:return text
 # Protect derivative coordinates, function argument notation, and prose.
 protected={}
 def keep(m):
  key='ZZTOKEN'+str(len(protected))+'ZZ';protected[key]=m[0];return key
 def math(m):
  s=m[0]
  s=re.sub(r'\\text\{d\}x|\\mathrm\{d\}x|\\(?:,|!)?\\text\{d\}x|(?<![A-Za-z])dx|[pqPQIyz]\(x\)',keep,s)
  # x in x+y, 2x, powers, or a bare argument is an algebraic coordinate slot.
  s=re.sub(r'\\text\{[^}]*\}|\\[A-Za-z]+',keep,s)
  s=re.sub(r'x',lambda _:'(x'+('+' if h>0 else '-')+str(abs(h))+')',s)
  s=re.sub(r'(?<=[A-Za-z0-9])(?=\(x[+-])',lambda _:r'\cdot ',s)
  for k,v in protected.items():s=s.replace(k,v)
  return s
 text=text.replace('with respect to $x:$','with respect to ZZCOORDZZ')
 result=re.sub(r'\$\$[\s\S]*?\$\$|\$[^$]*\$',math,text)
 return result.replace('ZZCOORDZZ','$x:$')
def value_translate(value,h):
 # Answer values contain only mathematical expressions.
 return translate('$'+value+'$',h)[1:-1]
def source_replay(difficulty,seed=0,template=None,parameters=None,profile=None):
 if difficulty not in SUPPORTED_LEVELS:raise ValueError('Unsupported difficulty: '+difficulty)
 eligible=[t for t,q in SOURCES.items() if q[':question/difficulty'][':db/ident']==':question.difficulty/'+difficulty and True]
 rng=random.Random(seed);t=template or rng.choice(eligible)
 assert t in SOURCES and SOURCES[t][':question/difficulty'][':db/ident']==':question.difficulty/'+difficulty
 p=dict(parameters) if parameters is not None else {'shift':rng.choice(SHIFTS)}
 assert set(p)=={'shift'} and p['shift'] in (0,*SHIFTS)
 h=p['shift'];assert t!='q-109029' or h==0
 q=SOURCES[t];original=h==0;identity=digest([VERSION,t,p])
 qid=uid('question:'+identity);fields=[]
 for f in q[':question/answer-fields']:
  fid=uid('field:'+identity+':'+f[':answer-field/key']);answers=[];correct=None
  for a in f[':answer-field/choices']:
   value=value_translate(a[':answer/value'],h);aid=uid('answer:'+fid+':'+value)
   answers.append({':answer/id':aid,':answer/type':':answer.type/math',':answer/value':value})
   if a[':answer/id']==f[':answer-field/correct'][':answer/id']:correct=aid
  fields.append({':answer-field/id':fid,':answer-field/key':f[':answer-field/key'],':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]})
 problem=translate(q[':question/problem'],h)
 solution_source=q[':question/worked-solution']
 if h:
  solution_source=solution_source.replace('(1/4x)',r'(\frac{1}{4x})').replace('(3/2x)',r'(\frac{3}{2x})')
 solution=translate(solution_source,h)
 if not original:
  # Restrict the question to the nonzero family obtained by Bernoulli division.
  problem=problem.replace('Find the general solution','Find the general nonzero real solution')
  domain='x'+('+' if h>0 else '-')+str(abs(h))
  problem+='\n\nWork on an interval where $'+domain+'>0$. Choose constants and intervals on which all displayed real expressions are defined.'
  if t in ('q-109170','q-109177'):problem+=' Take $y>0$.'
  solution+='\n\nThese are the nonzero real solutions on the specified intervals; exclude denominator zeros and restrict constants and intervals to the real branches used above.'
  if t=='q-109170':solution+=' Since $z=y^{1/4}>0$, retain only intervals where the displayed expression for $z$ is positive.'
  if t=='q-109177':solution+=' Since $z=y^{3/2}>0$, retain only intervals where the displayed expression for $z$ is positive.'
 return {'knowledge_point':{'db_id':KP_ID,'id':str(NAMESPACE),'title':TITLE},'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+difficulty,':question/problem':problem,':question/worked-solution':solution,':question/answer-fields':fields},'generation':{'version':VERSION,'template':t,'profile':'observed:'+t,'parameters':p,'seed':seed,'source_question_id':q[':question/id'],'source_math_academy_id':t,'source_basis':SNAPSHOT['basis'],'evidence_only':original,'domains':'translated coordinate positive; nonzero real branches; exclude singularities','sympy':sp.__version__}}
# Production extensions. All neighboring coefficient pairs have comparable
# elementary integrals. The bank is independent of which pair is the question.
u=sp.Symbol('u',positive=True)
C=sp.Symbol('C',real=True)
FAMILIES={
 'q-106073':(sp.Rational(2),'exp'),
 'q-109026':(sp.Rational(2),'linear'),
 'q-109027':(sp.Rational(-4),'quadratic'),
 'q-109028':(sp.Rational(3),'constant-linear'),
 'q-109029':(sp.Rational(1,2),'autonomous'),
 'q-109154':(sp.Rational(2),'power'),
 'q-109170':(sp.Rational(3,4),'power'),
 'q-109172':(sp.Rational(2),'power'),
 'q-109177':(sp.Rational(-1,2),'power'),
 'q-109158':(sp.Rational(2),'power'),
}
B_VALUES=(-3,-2,-1,1,2,3)
def coefficient_domain(t):
 return tuple((a,b) for a in ((2,3,4) if t=='q-109172' else (1,2,3)) for b in B_VALUES)
def family_math(t,a,b):
 """Return p,q,n, integrating factor, integral of I*Q, and z."""
 a,b=sp.Rational(a),sp.Rational(b);n,kind=FAMILIES[t];m=1-n
 if kind=='exp':
  p=-a;q=b*sp.exp(u);mu=sp.exp(-m*a*u)
  integ=m*b*sp.exp((1-m*a)*u)/(1-m*a)
 elif kind=='linear':
  p=a*u;q=b*u;mu=sp.exp(m*a*u**2/2);integ=b*mu/a
 elif kind=='quadratic':
  p=-a*u**2;q=b*u**2;mu=sp.exp(-m*a*u**3/3);integ=-b*mu/a
 elif kind=='constant-linear':
  p=a;q=b*u;mu=sp.exp(m*a*u);integ=b*mu/a*(u-1/(m*a))
 elif kind=='autonomous':
  p=-a;q=b;mu=sp.exp(-m*a*u);integ=-b*mu/a
 else:
  pc={'q-109154':-a,'q-109170':a,'q-109172':-a,'q-109177':a,'q-109158':-a}[t]
  r={'q-109154':sp.Rational(1,2),'q-109170':1,'q-109172':-2,'q-109177':-2,'q-109158':1}[t]
  p=pc/u;q=b*u**r;A=m*pc;mu=u**A
  integ=m*b*u**(A+r+1)/(A+r+1)
 z=sp.expand(C/mu+sp.cancel(integ/mu))
 return p,q,n,mu,integ,z

def tex(expr,h):
 text=sp.latex(expr,mul_symbol='dot')
 coordinate='x' if h==0 else r'\left(x'+('+' if h>0 else '-')+str(abs(h))+r'\right)'
 return re.sub(r'\bu\b',lambda _:coordinate,text)
def recover(z,n,h):
 if n==2:return tex(sp.factor(1/z),h)
 if n==-4:return r'\sqrt[5]{'+tex(z,h)+'}'
 if n==3:return r'\pm\sqrt{'+tex(sp.factor(1/z),h)+'}'
 if n==sp.Rational(1,2):return r'\left('+tex(z,h)+r'\right)^{2}'
 if n==sp.Rational(3,4):return r'\left('+tex(z,h)+r'\right)^{4}'
 if n==sp.Rational(-1,2):return r'\left('+tex(z,h)+r'\right)^{2/3}'
 raise ValueError('Unknown inverse')

def generate(difficulty,seed=0,template=None,parameters=None,profile=None):
 if difficulty not in SUPPORTED_LEVELS:raise ValueError('Unsupported difficulty: '+difficulty)
 rng=random.Random(seed)
 eligible=['q-106073','q-109026'] if difficulty=='easy' else [t for t,q in SOURCES.items() if q[':question/difficulty'][':db/ident']==':question.difficulty/'+difficulty]
 t=template or rng.choice(eligible)
 if t not in eligible:raise ValueError('Unsupported template for difficulty')
 requested=dict(parameters) if parameters is not None else {}
 # Explicit original-parameter replay keeps every original choice and stage.
 if requested=={'shift':0} and difficulty!='easy':
  return source_replay(difficulty,seed,t,requested,profile)
 allowed={'shift','bank','target','a','b','q_scale'}
 if set(requested)-allowed:raise ValueError('Unknown parameters')
 domain=coefficient_domain(t)
 if 'bank' in requested:
  bank=[tuple(v) for v in requested['bank']]
  if len(bank)!=5 or len(set(bank))!=5 or any(v not in domain for v in bank):raise ValueError('Invalid coefficient bank')
 else:
  bank=rng.sample(domain,5)
 if 'a' in requested or 'b' in requested or 'q_scale' in requested:
  base_a=3 if t=='q-109027' else 2 if t=='q-109172' else 1
  base_b=-1 if t=='q-109028' else 1
  pair=(requested.get('a',base_a),requested.get('b',base_b*requested.get('q_scale',1)))
  if pair not in domain:raise ValueError('Coefficient outside supported domain')
  if pair not in bank:
   if 'bank' in requested:raise ValueError('Target missing from explicit bank')
   bank[0]=pair
  target=bank.index(pair)
  if 'target' in requested and requested['target']!=target:raise ValueError('Conflicting target')
 else:target=requested.get('target',rng.randrange(5))
 if type(target)!=int or not 0<=target<5:raise ValueError('Invalid target')
 h=requested.get('shift',0 if difficulty=='easy' or t=='q-109029' else rng.choice(SHIFTS))
 if type(h)!=int or h not in (0,*SHIFTS):raise ValueError('Invalid shift')
 a,b=bank[target];p,q,n,mu,integ,z=family_math(t,a,b);m=1-n
 params={'shift':h,'bank':[list(v) for v in bank],'target':target,'a':a,'b':b}
 identity=digest([VERSION,t,params]);qid=uid('question:'+identity);fid=uid('field:'+identity+':selection')
 choices=[];correct=None
 for i,(aa,bb) in enumerate(bank):
  zz=family_math(t,aa,bb)[-1];value='y='+recover(zz,n,h);aid=uid('answer:'+fid+':'+value)
  choices.append({':answer/id':aid,':answer/type':':answer.type/math',':answer/value':value})
  if i==target:correct=aid
 # Do not couple original array position to the key. The learner UI also shuffles.
 random.Random(int(identity,16)).shuffle(choices)
 xY=sp.Symbol('y',positive=True);dy=r'\frac{\mathrm{d}y}{\mathrm{d}x}'
 def T(expr):return tex(expr,h)
 if difficulty in ('easy','moderate'):equation=dy+'+'+T(p*xY)+'='+T(q*xY**n)
 elif t=='q-109170':equation=T(u)+r'\,'+dy+'+'+T(a*xY)+'='+T(b*u**2*xY**n)
 elif t=='q-109172':equation=dy+'='+T((b*xY**2+a*u*xY)/u**2)
 elif t=='q-109177':equation=T(u**2)+r'\,'+dy+'='+T(b*xY**n-a*u*xY)
 else:equation=T(u**2)+r'\,'+dy+'='+T(b*u**3*xY**2+a*u*xY)
 equation=equation.replace('+-','-').replace('+ -','-')
 problem='Find the general nonzero real solution to the differential equation\n\n$$\n'+equation+'.\n$$'
 if difficulty=='easy':problem+='\n\nUse the substitution $z=y^{-1}$.'
 if t!='q-109029':problem+='\n\nWork on an interval where $'+T(u)+'>0$.'
 if n in (sp.Rational(1,2),sp.Rational(3,4),sp.Rational(-1,2)):
  problem+=' Take $y>0$. For even powers and powers of $2/3$ in the choices, retain only intervals where the base is positive.'
 problem+=' Choose constants and intervals on which the displayed expressions are real and finite.'
 solution=''
 if difficulty=='hard':solution+='First, rearrange and divide by the coefficient of the derivative:\n\n$$'+dy+'+'+T(p*xY)+'='+T(q*xY**n)+'. $$\n\n'
 solution+='This is a Bernoulli equation with\n\n$$'+r'\begin{aligned}p(x)&='+T(p)+r'\\ q(x)&='+T(q)+r'\\ n&='+T(n)+r'.\end{aligned}$$'+'\n\n'
 solution+='Divide by $y^{'+T(n)+'}$ and set $z=y^{'+T(m)+'}$. The chain rule gives\n\n$$'+r'\frac{\mathrm{d}z}{\mathrm{d}x}='+T(m*xY**(-n))+r'\frac{\mathrm{d}y}{\mathrm{d}x}'+'.$$\n\n'
 solution+='Hence the linear equation in standard form is\n\n$$'+r'\frac{\mathrm{d}z}{\mathrm{d}x}+\left('+T(m*p)+r'\right)z='+T(m*q)+'.$$\n\n'
 solution+='An integrating factor is\n\n$$I(x)=e^{'+r'\int '+T(m*p)+r'\,\mathrm{d}x}='+T(mu)+'.$$\n\n'
 solution+='Multiplying through and using the product rule gives\n\n$$'+r'\frac{\mathrm{d}}{\mathrm{d}x}\left('+T(mu)+r'\,z\right)='+T(sp.simplify(mu*m*q))+'.$$\n\n'
 solution+='Integrating with respect to $x$, we obtain\n\n$$'+T(mu)+'z='+T(integ)+'+C.$'+'$\n\n'
 solution+='Thus\n\n$$z='+T(z)+'.$$\n\n'
 solution+='Finally, substitute $z=y^{'+T(m)+'}$ and solve for $y$:\n\n$$y='+recover(z,n,h)+'.$$\n\n'
 solution+='Here $C$ is an arbitrary real constant; exclude singularities and restrict to the stated real intervals.'
 if n in (sp.Rational(1,2),sp.Rational(3,4),sp.Rational(-1,2)):
  solution+=' The displayed expression for $z$ must be positive because $z=y^{'+T(m)+'}>0$.'
 if n==3:solution+=' Both signs are retained wherever the radicand is positive.'
 return {'knowledge_point':{'db_id':KP_ID,'id':str(NAMESPACE),'title':TITLE},'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+difficulty,':question/problem':problem,':question/worked-solution':solution,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',correct]}]},'generation':{'version':VERSION,'template':t,'profile':'neighboring-equations:'+t,'parameters':params,'seed':seed,'source_question_id':SOURCES[t][':question/id'],'source_math_academy_id':t,'source_basis':SNAPSHOT['basis'],'evidence_only':False,'domains':'nonzero real solutions; explicit positive-coordinate and positive-z conditions where needed','sympy':sp.__version__}}

def markdown(r):
 q=r['question'];f=q[':question/answer-fields'][0]
 return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$'+(' [key]' if a[':answer/id']==f[':answer-field/correct'][1] else '') for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
def main():
 p=argparse.ArgumentParser();p.add_argument('--difficulty',required=True);p.add_argument('--seed',type=int,default=0);p.add_argument('--count',type=int,default=1);p.add_argument('--format',choices=('json','markdown'),default='json');a=p.parse_args()
 if a.count<1:raise ValueError('count must be positive')
 records=[];seen=set()
 for seed in range(a.seed,a.seed+1000):
  r=generate(a.difficulty,seed);fp=digest([r['generation']['template'],r['generation']['parameters']])
  if fp not in seen:records.append(r);seen.add(fp)
  if len(records)>=a.count:break
 if len(records)!=a.count:raise ValueError('Finite variant limit; '+str(len(records))+' distinct available in this package')
 print(json.dumps(records,indent=2) if a.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
if __name__=='__main__':main()
