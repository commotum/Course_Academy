#!/usr/bin/env python3
"""Leibniz quotient-rule families: basis2275 evidence and scoped variations.

All eleven MA records are accounted; raw profile preserves omissions exactly.
Normal solutions keep ordered source operative stages; completions are labeled.
No database operations. See private extraction, validation and freeze evidence.
"""
import argparse,copy,hashlib,importlib.util,json,random,uuid
from pathlib import Path
import sympy as s
HERE=Path(__file__).with_suffix('')
def frozen(name):
 spec=importlib.util.spec_from_file_location('leibniz_'+name,HERE/(name+'.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
FORMAT=frozen('math_format')
RAW=json.loads((HERE/'source.json').read_text());KP=RAW['record'];KP_ID=17592186096622;KP_UUID=KP[':knowledge-point/id']
TITLE=KP[':knowledge-point/title'];VERSION='leibniz-quotient-2026-10-14-v1';SUPPORTED_LEVELS=('easy','moderate','hard');X=s.Symbol('x',real=True)
SOURCES={q[':question/math-academy-id']:q for q in KP[':knowledge-point/questions'] if ':question/math-academy-id' in q}
TEMPLATES={
'q-340336':dict(level='easy',kind='tan-square',field='blank',p={'c':1}),
'q-340340':dict(level='easy',kind='exp-linear',field='blank',p={'c':1,'b':1}),
'q-340337':dict(level='easy',kind='linear-cos',field='blank',p={'c':1}),
'q-47994':dict(level='easy',kind='sin-linear',field='radio',p={'c':1}),
'q-11969':dict(level='moderate',kind='linear-linear',field='radio',p={'c':-1,'a':-2,'b':9}),
'q-340332':dict(level='moderate',kind='square-square',field='blank',p={'c':1,'b':1}),
'q-340341':dict(level='moderate',kind='linear-ln',field='blank',p={'c':1}),
'q-340343':dict(level='moderate',kind='log-power',field='blank',p={'b':3,'n':2}),
'q-340335':dict(level='hard',kind='sin-sin',field='blank',p={'a':1,'b':1}),
'q-11944':dict(level='moderate',kind='affine-ln',field='radio',p={'a':3,'b':5},authored_rating=True),
'q-9909':dict(level='hard',kind='cos-sin',field='radio',p={'c':1},authored_rating=True)}

def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def uid(v):return str(uuid.uuid5(uuid.UUID(KP_UUID),v))
def tex(z):return s.latex(z).replace(r'\log',r'\ln')
def fr(a,b):return r'\frac{'+a+'}{'+b+'}'
def par(z):return '('+tex(z)+')'
def eq(a,b):
 # Exact rational reduction modulo sin(x)^2+cos(x)^2=1; all trig arguments
 # in these bounded families are x. This avoids heuristic simplifier cost.
 z=(a-b).subs({s.tan(X):s.sin(X)/s.cos(X),s.sec(X):1/s.cos(X),s.csc(X):1/s.sin(X),s.cot(X):s.cos(X)/s.sin(X)},simultaneous=True)
 z=s.cancel(z)
 if z==0:return True
 sn,cs=s.symbols('_sin _cos');num=s.fraction(z)[0].subs({s.sin(X):sn,s.cos(X):cs})
 if num.has(cs):num=s.rem(num,cs**2+sn**2-1,cs)
 return s.cancel(num)==0

def parts(t,p):
 k=TEMPLATES[t]['kind'];c=p.get('c',1);a=p.get('a',1);b=p.get('b',1)
 if k=='tan-square':return c*s.tan(X),X**2
 if k=='exp-linear':return c*s.exp(X),X+b
 if k=='linear-cos':return c*X,s.cos(X)
 if k=='sin-linear':return c*s.sin(X),X
 if k=='linear-linear':return c*X,a*X+b
 if k=='square-square':return c*X**2,X**2+b
 if k=='linear-ln':return c*X,s.log(X)
 if k=='log-power':return s.log(X)/s.log(b),X**p['n']
 if k=='sin-sin':return a-b*s.sin(X),s.sin(X)
 if k=='affine-ln':return a*X+b,s.log(X)
 if k=='cos-sin':return c*(1+s.cos(X)),s.sin(X)
 raise ValueError(t)

def valid(t,level,p):
 if t not in TEMPLATES or TEMPLATES[t]['level']!=level:raise ValueError('template/level mismatch')
 if set(p)!=set(TEMPLATES[t]['p']) or any(type(z) is not int or abs(z)>12 for z in p.values()):raise ValueError('exact declared integer slots, absolute value <=12')
 if any(z==0 for z in p.values()):raise ValueError('substantive nonzero slots')
 if t=='q-340343' and not (2<=p['b']<=12 and 2<=p['n']<=4):raise ValueError('log base2..12, power2..4')
 if t=='q-340335' and not (1<=p['a']<=12 and 1<=p['b']<=12):raise ValueError('hard positive a,b1..12')

def sample(t,r):
 p={k:r.choice([i for i in range(-12,13) if i]) for k in TEMPLATES[t]['p']}
 if t=='q-340343':p={'b':r.randint(2,12),'n':r.randint(2,4)}
 if t=='q-340335':p={'a':r.randint(1,12),'b':r.randint(1,12)}
 return p

def answer_and_bank(t,p,profile):
 u,v=parts(t,p);du,dv=s.diff(u,X),s.diff(v,X);d=s.factor((v*du-u*dv)/v**2);c=p.get('c',1);a=p.get('a',1);b=p.get('b',1)
 if t=='q-340336':ans=c*(X*s.sec(X)**2-2*s.tan(X))
 elif t=='q-340337':ans=c*(s.cos(X)+X*s.sin(X))
 elif t=='q-340343':ans=1-p['n']*s.log(X)
 elif t=='q-340335':ans=-a*s.csc(X)*s.cot(X)
 else:ans=d
 if TEMPLATES[t]['field']=='blank':return [ans],ans
 if profile=='method':
  vals=[d,(v*du+u*dv)/v**2,-d,(v*du-u*dv)/v,du/dv]
 elif t=='q-47994':vals=[c*(X*s.cos(X)+s.sin(X))/X**2,c*X*(s.cos(X)-s.sin(X))/X**2,d,c*(s.cos(X)-X*s.sin(X))/X**2,c*(X*s.cos(X)-s.sin(X))/X]
 elif t=='q-11969':vals=[-c*b/v**2,d,c*(b+2*a*X)/v**2,-c*(b+a*X)/v**2,-c*(b+2*a*X)/v**2]
 elif t=='q-11944':vals=[(a*s.log(X)-(a*X+b))/(X*s.log(X)**2),(a*X*s.log(X)-(a*X+b))/s.log(X)**2,d,(X*s.log(X)-(a*X+b))/(X*s.log(X)**2),(a*s.log(X)-(a*X+b))/s.log(X)**2]
 elif t=='q-9909':vals=[c/s.sin(X)**2,c/(1-s.cos(X)),-c/s.sin(X)**2,-c/(1+s.cos(X)),-c/(1-s.cos(X))]
 else:raise ValueError('unknown bank')
 if sum(eq(z,ans) for z in vals)!=1 or any(eq(z,w) for i,z in enumerate(vals) for w in vals[:i]):raise ValueError('whole profile collision')
 return vals,ans

FORMAL=r'\frac{v\frac{\text{d}u}{\text{d}x}-u\frac{\text{d}v}{\text{d}x}}{v^{2}}'
DY=r'\frac{\text{d}y}{\text{d}x}'

def rows(t,p):
 u,v=parts(t,p);du,dv=s.diff(u,X),s.diff(v,X);c=p.get('c',1);a=p.get('a',1);b=p.get('b',1);n=p.get('n',2)
 den=par(v)+r'^{2}';sub=fr(par(v)+r'\cdot '+par(du)+'-'+par(u)+r'\cdot '+par(dv),den)
 final=tex(s.factor((v*du-u*dv)/v**2))
 if t=='q-340336':
  ans=c*(X*s.sec(X)**2-2*s.tan(X));extra=[fr('x('+tex(ans)+')',r'x^{4}'),fr('1',r'x^{3}')+r'\cdot ('+tex(ans)+')']
 elif t=='q-340340':
  extra=[fr(tex(c*s.exp(X))+'(x'+('+' if b>=0 else '')+str(b)+'-1)',den),final]
 elif t=='q-340337':extra=[fr('1',r'\cos^{2} x')+r'\cdot ('+tex(c*(s.cos(X)+X*s.sin(X)))+')']
 elif t=='q-47994':extra=[fr(tex(c*(X*s.cos(X)-s.sin(X))),r'x^{2}')]
 elif t=='q-11969':extra=[fr(tex(c*b)+'+'+tex(a*c*X)+'-'+par(a*c*X),den),final]
 elif t=='q-340332':extra=[fr(tex(2*c*X**3)+'+'+tex(2*b*c*X)+'-'+par(2*c*X**3),den),final]
 elif t=='q-340341':extra=[tex(c*(s.log(X)-1)/s.log(X)**2)]
 elif t=='q-340343':
  lx=tex(s.log(X));lb=tex(s.log(b));power=tex(X**(2*n));reduced=tex(X**(n+1)*s.log(b));a1=tex(X**(n-1));a2=tex(n*X**(n-1)*s.log(X))
  extra=[fr(fr(a1,lb)+'-'+fr(a2,lb),power),fr(a1+'-'+a2,power+lb),fr(a1+'('+tex(1-n*s.log(X))+')',power+lb),fr(tex(1-n*s.log(X)),reduced),'('+tex(1-n*s.log(X))+')'+r'\cdot '+fr('1',reduced)]
 elif t=='q-340335':
  sn=tex(s.sin(X));co=tex(s.cos(X));den=r'\sin^{2} x'
  inside=tex(-b*s.sin(X))+'-'+str(a)+'+'+tex(b*s.sin(X))
  extra=[fr(co+'('+inside+')',den),fr(co+r'\cdot ('+str(-a)+')',den),tex(-s.Integer(a))+fr('1',sn)+r'\cdot '+fr(co,sn),tex(-a*s.csc(X)*s.cot(X))]
 elif t=='q-11944':extra=[fr(tex(a*X*s.log(X)-(a*X+b)),tex(X*s.log(X)**2)),final]
 elif t=='q-9909':extra=[fr(tex(-c*s.sin(X)**2-c*s.cos(X)-c*s.cos(X)**2),r'\sin^{2}x'),tex(-c/(1-s.cos(X)))]
 else:raise ValueError(t)
 return [FORMAL,sub]+extra

def domain(t,p):
 _,v=parts(t,p)
 return ('x>0 and '+tex(v)+' !=0') if 'ln' in TEMPLATES[t]['kind'] or t=='q-340343' else tex(v)+' !=0'

def normal(t,p):
 u,v=parts(t,p);du,dv=s.diff(u,X),s.diff(v,X)
 numerator=(r'\log_{'+str(p['b'])+'}x') if t=='q-340343' else tex(u)
 prompt='Given that $y='+fr(numerator,tex(v))+'$, find $'+DY+'.$'
 if TEMPLATES[t]['field']=='blank':
  lhs=DY+'='
  if t=='q-340336':before=fr('1',r'x^{3}')+r'\cdot (';after=')'
  elif t=='q-340337':before=fr('1',r'\cos^{2}x')+r'\cdot (';after=')'
  elif t=='q-340343':before='(';after=r')\cdot '+fr('1',tex(X**(p['n']+1)*s.log(p['b'])))
  else:before=after=''
  prompt+='\n\n$'+lhs+before+'$\n{{field-1}}'+('\n$'+after+'.$' if after else '')
 definition=tex(u)
 if t=='q-340343':definition=r'\log_{'+str(p['b'])+'}x='+fr(r'\ln x',r'\ln '+str(p['b']))
 worked='Let $u='+definition+'$ and $v='+tex(v)+'.$ Then\n\n$$\n'+r'\begin{aligned}\frac{\text{d}u}{\text{d}x}&='+tex(du)+r'\,\text{and}\,\frac{\text{d}v}{\text{d}x}='+tex(dv)+r'.\end{aligned}'+'\n$$\n\nUsing the quotient rule, we get\n\n$$\n'+r'\begin{aligned}'+DY+'&='+r'\\ &='.join(rows(t,p))+r'.\end{aligned}'+'\n$$'
 return FORMAT.normalize_prose(prompt),FORMAT.normalize_prose(worked)

@FORMAT.checked_math_content
def checked_normal_output(record):return record

def generate(level,seed=0,template=None,parameters=None,profile=None,bank_profile=None):
 if level not in SUPPORTED_LEVELS:raise ValueError('unknown difficulty')
 if type(seed) is not int:raise ValueError('seed must be an integer')
 r=random.Random(seed);t=template or r.choice([t for t,d in TEMPLATES.items() if d['level']==level])
 if t not in TEMPLATES:raise ValueError('unknown template')
 if bank_profile is not None:
  if profile is not None and bank_profile!=profile:raise ValueError('profile mismatch')
  profile=bank_profile
 if profile=='raw':
  if parameters is not None and parameters!=TEMPLATES[t]['p']:raise ValueError('raw original parameters only')
  return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':copy.deepcopy(SOURCES[t]),'generation':{'version':VERSION,'template':t,'profile':'raw','parameters':TEMPLATES[t]['p'],'evidence_only':True,'eligible_for_learning':False,'source_basis':RAW['basis']}}
 radio=TEMPLATES[t]['field']=='radio';profile=profile or ('observed-'+t[2:] if radio else 'fragment')
 if profile not in (('observed-'+t[2:],'method') if radio else ('fragment',)):raise ValueError('inapplicable bank profile')
 for attempt in range(300):
  p=dict(parameters) if parameters is not None else sample(t,r);valid(t,level,p)
  try:vals,ans=answer_and_bank(t,p,'method' if profile=='method' else 'observed')
  except ValueError:
   if parameters is not None:raise
   continue
  break
 else:raise ValueError('cannot sample a valid complete profile')
 prompt,worked=normal(t,p);u,v=parts(t,p)
 domain_key=s.Poly(v,X).sqf_part().monic().as_expr() if v.is_polynomial(X) else v
 task=digest([s.srepr(s.cancel(u/v)),s.srepr(domain_key),'differentiate quotient in Leibniz notation'])
 content=digest([prompt,worked,sorted(tex(z) for z in vals),level,profile])
 qid=uid('question:'+content);fid=uid('field:'+content)
 choices=[{':answer/id':uid('answer:'+fid+':'+FORMAT.normalize_tex(tex(z))),':answer/type':':answer.type/math',':answer/value':FORMAT.normalize_tex(tex(z))} for z in vals]
 cid=next(a[':answer/id'] for a,z in zip(choices,vals) if eq(z,ans));r.shuffle(choices)
 field={':answer-field/id':fid,':answer-field/key':'selection' if radio else 'field-1',':answer-field/type':':answer-field.type/'+('radio' if radio else 'blank'),':answer-field/choices':choices,':answer-field/correct':[':answer/id',cid]}
 return checked_normal_output({'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':worked,':question/answer-fields':[field]},'generation':{'version':VERSION,'template':t,'profile':profile,'bank_profile':profile,'seed':seed,'parameters':p,'mathematical_fingerprint':task,'content_fingerprint':content,'source_ids':[t],'source_basis':RAW['basis'],'source_lineage':RAW['lineage'],'evidence_only':False,'eligible_for_learning':True,'authored_rating':TEMPLATES[t].get('authored_rating',False),'authored_solution':':question/worked-solution' not in SOURCES[t],'presentation_repairs':['normalize captured function macros/unicode','correct f(x)/dy mismatch to y'] if t=='q-340335' else ['normalize math notation'],'domain':domain(t,p),'plot_rating':'none','sympy_version':s.__version__}})

def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)
def generate_hard(seed=0,**kw):return generate('hard',seed,**kw)
def batch(level,count,seed=0,template=None,profile=None):
 if type(count) is not int or count<1:raise ValueError('count must be a positive integer')
 if type(seed) is not int:raise ValueError('seed must be an integer')
 if level not in SUPPORTED_LEVELS:raise ValueError('unknown difficulty')
 if profile=='raw':
  if count!=1 or template is None:raise ValueError('raw evidence batch requires explicit template and count1')
  return [generate(level,seed,template=template,profile='raw')]
 out=[];seen=set()
 for i in range(count*100+100):
  r=generate(level,seed+i,template=template,profile=profile);fp=r['generation']['mathematical_fingerprint']
  if fp not in seen:seen.add(fp);out.append(r)
  if len(out)==count:return out
 raise ValueError('requested batch exceeds bounded available tasks')

def markdown(record):
 q=record['question'];lines=[q[':question/problem']]
 for field in q.get(':question/answer-fields',[]):
  lines.append('Field `'+field[':answer-field/key']+'` (`'+str(field[':answer-field/type'])+'`).')
  correct=field.get(':answer-field/correct')
  for answer in field.get(':answer-field/choices',[]):
   mark=' [correct]' if isinstance(correct,list) and answer[':answer/id']==correct[1] else ''
   if isinstance(correct,dict) and answer[':answer/id']==correct.get(':answer/id'):mark=' [captured correct]'
   lines.append('- $'+answer[':answer/value']+'$'+mark+' — `'+answer[':answer/id']+'`')
 lines.append(q.get(':question/worked-solution','[Worked solution absent in source.]'))
 lines.append('```json\n'+json.dumps(record['generation'],ensure_ascii=False,indent=2)+'\n```')
 return '\n\n'.join(lines)

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=(*SUPPORTED_LEVELS,'all'),default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--template');ap.add_argument('--profile');ap.add_argument('--format',choices=('json','markdown'),default='json');a=ap.parse_args()
 if a.count<1:ap.error('positive count required')
 levels=SUPPORTED_LEVELS if a.difficulty=='all' else (a.difficulty,);rs=[r for level in levels for r in batch(level,a.count,a.seed,a.template,a.profile)]
 print(json.dumps(rs,indent=2,ensure_ascii=False) if a.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in rs))
