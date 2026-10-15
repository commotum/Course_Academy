#!/usr/bin/env python3
"""Private review draft: faithful repaired source replay, same-method extensions.
No database, registration, engine, or immutable numeric-tree writes.
"""
import sys
sys.dont_write_bytecode=True
import argparse,copy,hashlib,importlib.util,json,random,re,uuid
from pathlib import Path
import sympy as s
HERE=Path(__file__).with_suffix('')
def frozen(name):
 sp=importlib.util.spec_from_file_location('otherquotient_'+name,HERE/(name+'.py'));m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
FMT=frozen('math_format');PARSER=frozen('math_parser');CHAINS=frozen('family_chains');X=PARSER.x
RAW=json.loads((HERE/'source.json').read_text());KP=RAW['record'];KP_ID=17592186096621
VERSION='other-functions-private-2026-10-14-v1';SUPPORTED_LEVELS=('easy','moderate','hard');CAPACITY={'easy':192,'moderate':480,'hard':64}
SOURCES={q.get(':question/math-academy-id',q[':question/id']):q for q in KP[':knowledge-point/questions']}
# Original function operands and target, preserving the original domain.
SPEC={
'q-17921':(s.cos(X),s.log(X),None,'easy'),
'q-47999':(X**2,s.sin(X),None,'easy'),
'q-340318':(X,s.exp(3*X),s.Integer(1),'moderate'),
'q-9908':(s.cos(X),1+s.sin(X),s.pi/2,'moderate'),
'q-167328':(s.exp(X)/2,-4*s.sin(X),None,'easy'),
'q-167782':(s.exp(X)/2,-4*s.sin(X),None,'easy'),
'q-166075':(s.exp(X)/2,-4*s.sin(X),None,'easy'),
'q-2385':(s.cos(X),10*X**2,None,'easy'),
'q-340308':(s.tan(X),X,None,'easy'),
'q-340309':(X,s.sin(X),None,'easy'),
'q-340316':(2**X,X**2-1,s.Integer(0),'moderate'),
'q-47943':(s.exp(X),s.cos(X),None,'easy'),
'q-47998':(s.sin(X),X**2,None,'easy'),
'q-48504':(X**2,s.log(X),s.E,'moderate'),
'q-48507':(s.sin(X),2*X,s.pi,'moderate')}
HARD='authored-hard-sums'
RULE=r'\frac{u^{\prime}(x)\cdot v(x)-u(x)\cdot v^{\prime}(x)}{[v(x)]^{2}}'
def _namespace():
 from types import SimpleNamespace
 return SimpleNamespace(**globals())
def digest(z):return hashlib.sha256(json.dumps(z,sort_keys=True,ensure_ascii=False,default=str).encode()).hexdigest()
def uid(z):return str(uuid.uuid5(uuid.UUID(KP[':knowledge-point/id']),z))
def tex(z):return s.latex(z).replace(r'\log',r'\ln')
def frac(a,b):return r'\frac{'+a+'}{'+b+'}'
def gp(z):return '('+tex(z)+')'
def formal(u,v):return frac(gp(u)+r'^{\prime}\cdot '+gp(v)+'-'+gp(u)+r'\cdot '+gp(v)+r'^{\prime}',gp(v)+'^{2}')
def substitution(u,v):return frac(gp(s.diff(u,X))+r'\cdot '+gp(v)+'-'+gp(u)+r'\cdot '+gp(s.diff(v,X)),gp(v)+'^{2}')
def equivalent(a,b):
 z=(a-b).subs(s.tan(X),s.sin(X)/s.cos(X)).subs(s.sec(X),1/s.cos(X))
 n=s.expand(s.together(z).as_numer_denom()[0])
 if n==0:return True
 if n.has(s.sin(X)):
  try:n=s.rem(s.Poly(n,s.sin(X)),s.Poly(s.sin(X)**2+s.cos(X)**2-1,s.sin(X))).as_expr()
  except s.PolynomialError:pass
 return s.expand(n)==0

def clean(text):
 text=text.replace('⁡','').replace('′',r'\prime').replace(r'\dfrac',r'\frac')
 text=re.sub(r'\\operatorname\{(sin|cos|tan|sec|ln|cos|log)\}',lambda m:'\\'+m[1]+' ',text)
 text=re.sub(r'\{(sin|cos|tan|sec|ln)\}',lambda m:'\\'+m[1]+' ',text)
 text=re.sub(r'(?<![A-Za-z\\])(sin|cos|tan|sec|ln)(?![A-Za-z])',lambda m:'\\'+m[1]+' ',text)
 # Bare captured sinx/cosx have no word boundary after the name.
 text=re.sub(r'(?<![A-Za-z\\])(sin|cos|tan|sec|ln)(?=x)',lambda m:'\\'+m[1]+' ',text)
 while r'\begin{aligned}\begin{aligned}' in text:text=text.replace(r'\begin{aligned}\begin{aligned}',r'\begin{aligned}').replace(r'\end{aligned}\end{aligned}',r'\end{aligned}')
 return text

def source_solution(q,u,v):
 text=clean(q[':question/worked-solution'])
 def block(m):
  body=m[1];rows=[]
  for row in body.split(r'\\'):
   if '&' not in row:continue
   lhs,rhs=row.split('&',1);rhs=rhs.strip().removeprefix('=').strip()
   if r'\prime' in rhs or "'" in rhs:
    rhs=RULE if any(z in rhs for z in ['u(x)','h(x)','v(x)']) else formal(u,v)
   rows.append((lhs.strip() if not rows else '')+'&='+rhs)
  return r'\begin{aligned}'+r'\\ '.join(rows)+r'\end{aligned}'
 text=re.sub(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',block,text,flags=re.S)
 return FMT.normalize_prose(text)

def original_parameters(t):
 if t==HARD:return {'a':1,'b':1}
 return {'scale':1,**({'target':tex(SPEC[t][2])} if SPEC[t][2] is not None else {})}

def domain(u,v):
 # Real original operands, rather than only the cancelled rational expression.
 req=[]
 for z in [u,v]:
  for f in z.atoms(s.log):req.append(['positive',s.srepr(f.args[0])])
  for f in z.atoms(s.tan,s.sec):req.append(['nonzero',s.srepr(s.cos(f.args[0]))])
 # Normalize nonzero scalar factors, preserving all holes before cancellation.
 vv=s.factor(v);coeff,base=vv.as_coeff_Mul();req.append(['nonzero',s.srepr(base)])
 return sorted(set(map(tuple,req)))
def task_identity(u,v,t):return digest([s.srepr(s.cancel(u/v)),domain(u,v),None if t is None else s.srepr(t)])

def generic_solution(u,v,t):
 du,dv=s.diff(u,X),s.diff(v,X);n=du*v-u*dv
 rows=[RULE,formal(u,v),substitution(u,v),frac(tex(s.expand(n)),tex(v**2)),tex(s.factor(n)/v**2)]
 text='In this case, the expression for $'+('y' if t is not None else 'f(x)')+'$ is a quotient $\\frac{u(x)}{v(x)}$ with $u(x)='+tex(u)+'$ and $v(x)='+tex(v)+'.$\n\nTherefore, we apply the quotient rule as follows:\n\n$$\n'+r'\begin{aligned}f^{\prime}(x)&='+r'\\ &='.join(rows)+r'\end{aligned}'+'\n$$'
 if t is not None:
  derivative=(du*v-u*dv)/v**2;ans=s.simplify(derivative.subs(X,t))
  substituted=frac(gp(du.subs(X,t))+r'\cdot '+gp(v.subs(X,t))+'-'+gp(u.subs(X,t))+r'\cdot '+gp(dv.subs(X,t)),gp(v.subs(X,t))+'^{2}')
  text+='\n\nTo find the slope of the tangent line, we now substitute $x='+tex(t)+'$ into the formula and get\n\n$$\n'+r'\begin{aligned}f^{\prime}('+tex(t)+')&='+substituted+r'\\ &='+tex(ans)+r'\end{aligned}'+'\n$$\n\nTherefore, the slope of the tangent line is $'+tex(ans)+'.$'
 return text

HARD_COEFFICIENTS=(-3,-2,-1,1,2,3,4,5)
TARGETS={'q-340318':['0','1','2','-1',r'\frac{1}{3}'],'q-9908':[r'\frac{\pi}{2}','0',r'\pi',r'\frac{5\pi}{2}'],'q-340316':['0','2','-2','3'],'q-48504':['e',r'e^2',r'\frac{1}{e}',r'\sqrt{e}'],'q-48507':[r'\pi',r'2\pi',r'3\pi',r'-\pi']}
def parameters(t,r):
 if t==HARD:return {'a':r.choice(HARD_COEFFICIENTS),'b':r.choice(HARD_COEFFICIENTS)}
 p={'scale':r.choice(list(range(-12,0))+list(range(1,13)))}
 if SPEC[t][2] is not None:p['target']=r.choice(TARGETS[t])
 return p

def instance(t,p):
 if t==HARD:
  if set(p)!={'a','b'} or any(type(z)is not int or z not in HARD_COEFFICIENTS for z in p.values()):raise ValueError('hard a,b in -3,-2,-1,1,2,3,4,5; two substantive terms required')
  return X**2+p['a']*s.sin(X),s.exp(X)+p['b']*s.cos(X),None
 if t not in SPEC:raise ValueError('unknown source family')
 if set(p)!=set(original_parameters(t)) or type(p['scale'])is not int or not 0<abs(p['scale'])<=12:raise ValueError('nonzero integer scale absolute value <=12; source target key required')
 u,v,target,_=SPEC[t];u=p['scale']*u
 if target is not None:
  target=PARSER.scalar(p['target'])
  vv=v.subs(X,target)
  if target.free_symbols or vv==0 or any(z.subs(X,target).has(s.zoo,s.nan,s.oo,-s.oo) for z in [u,v]) or target.is_real is False:raise ValueError('undefined real target')
  if u.has(s.log) or v.has(s.log):
   if target.is_positive is not True:raise ValueError('logarithmic target must be positive')
  if not any(equivalent(target,PARSER.scalar(z)) for z in TARGETS[t]):raise ValueError('target outside declared exact-point slot')
 return u,v,target

def source_profile(t):
 q=SOURCES[t];fs=q.get(':question/answer-fields',[])
 return t+'-complete-observed' if fs and fs[0][':answer-field/type'][':db/ident'].endswith('/radio') else 'blank'

@FMT.checked_math_content
def generate(difficulty,seed=0,template=None,parameters=None,bank_profile=None,profile=None):
 if type(seed)is not int:raise ValueError('builtin integer seed required')
 if difficulty not in SUPPORTED_LEVELS:raise ValueError('difficulty')
 r=random.Random(seed);template=template or (HARD if difficulty=='hard' else r.choice([t for t in SPEC if SPEC[t][3]==difficulty]));t=template
 if t!=HARD and (t not in SPEC or SPEC[t][3]!=difficulty) or t==HARD and difficulty!='hard':raise ValueError('template difficulty mismatch')
 # Choose the entire eligible bank before parameters. No pooled first-valid recipes.
 selected=bank_profile or profile or ('authored-operations' if t==HARD else source_profile(t))
 eligible=['authored-operations'] if t==HARD else [source_profile(t)]
 if selected not in eligible:raise ValueError('ineligible whole bank profile')
 supplied=parameters is not None
 for attempt in range(100):
  p=copy.deepcopy(parameters) if supplied else globals()['parameters'](t,r)
  u,v,target=instance(t,p);du,dv=s.diff(u,X),s.diff(v,X);der=(du*v-u*dv)/v**2;answer=s.simplify(der.subs(X,target)) if target is not None else s.factor(der)
  original=t!=HARD and p==original_parameters(t);q=SOURCES.get(t,{})
  fragment=t=='q-167782';field_type='blank' if selected=='blank' else 'radio';key=q.get(':question/answer-fields',[{':answer-field/key':'field-1'}])[0][':answer-field/key'] if t!=HARD and q.get(':question/answer-fields') else ('selection' if field_type=='radio' else 'field-1')
  if fragment:answer=s.cos(X)-s.sin(X)
  if field_type=='radio':
   if t==HARD:values=[der,(du*v+u*dv)/v**2,(du*v-u*dv)/v,du/dv,(du*v-u*dv)/u**2]
   elif t=='q-48504':values=[answer,s.Rational(p['scale'],4),s.Rational(2*p['scale'],3),s.Integer(p['scale']),answer/2]
   elif t=='q-48507':values=[s.Rational(p['scale'],4)/target,-p['scale']*target,2*p['scale']*target,-s.Rational(p['scale'],2),answer]
   else:values=[p['scale']*PARSER.scalar(clean(a[':answer/value'])) for a in q[':question/answer-fields'][0][':answer-field/choices']]
  else:
   values=([p['scale']*PARSER.scalar(clean(q[':question/answer-fields'][0][':answer-field/choices'][0][':answer/value']))] if target is None and not fragment and t!=HARD and q.get(':question/answer-fields') else [answer])
  if sum(equivalent(z,answer) for z in values)!=1 or any(equivalent(z,y) for i,z in enumerate(values) for y in values[:i]) or any(z.has(s.zoo,s.nan) for z in values):
   if supplied:raise ValueError('complete bank rejected for collision/undefined option')
   continue
  break
 else:raise ValueError('no noncolliding complete bank')
 repairs=[]
 if original:
  prompt=clean(q[':question/problem'])
  if ':question/worked-solution' in q:worked=source_solution(q,u,v)
  else:worked=generic_solution(u,v,target);repairs.append('missing solution authored with canonical quotient stages')
  if ':question/difficulty' not in q:repairs.append('missing difficulty assigned easy from comparable lesson tasks')
  if not q.get(':question/answer-fields'):repairs.append('missing answer fields completed as blank');prompt+='\n\nThe slope is {{'+key+'}}.'
  if q.get(':question/answer-fields') and ':answer-field/correct' not in q[':question/answer-fields'][0]:repairs.append('missing correct reference independently derived from function')
  if fragment:
   repairs.append('missing shared definitions supplied; broken table fraction repaired, same inner fragment blank')
  elif t in ('q-167328','q-166075'):
   prompt='Given $f(x)='+tex(u)+'$ and $h(x)='+tex(v)+'.$\n\n'+prompt;repairs.append('missing shared function definitions supplied from worked solution')
 else:
  if fragment:
   # Preserve the partial response contract, moving its scale to the supplied context.
   prompt='' # Supplied below as a complete equation table with an embedded field.
  elif t in ['q-167328','q-166075']:
   prompt='Given $f(x)='+tex(u)+'$ and $h(x)='+tex(v)+'.$\n\n'+clean(q[':question/problem'])
  elif target is None:prompt='If $f(x)='+frac(tex(u),tex(v))+r'$, find $f^{\prime}(x)$ wherever the original quotient is defined.'
  else:prompt='If a curve $C$ is given by $y='+frac(tex(u),tex(v))+'$, calculate the slope of the tangent line to the curve at the point where $x='+tex(target)+'.$'
  if field_type=='blank' and not fragment and '{{'+key+'}}' not in prompt:prompt+='\n\n'+('$f^{\\prime}(x)=$' if target is None else 'The slope is')+' {{'+key+'}}.'
  worked=(generic_solution(u,v,target) if t==HARD else CHAINS.family_solution(sys.modules[__name__] if __name__ in sys.modules else _namespace(),t,u,v,target,p['scale']))
 if fragment:
  coefficient=s.Integer(p['scale'])
  prompt='Given $f(x)='+tex(u)+'$ and $h(x)='+tex(v)+r'$, calculate $\frac{\mathrm{d}}{\mathrm{d}x}(\frac{f}{h})$.'+'\n\n'+r'| $\frac{\mathrm{d}}{\mathrm{d}x}(\frac{f}{h})=$ | $'+tex(coefficient*s.exp(X))+'($ {{field-1}} $)$ |\n| --- | --- |\n|  | $8\\sin^2 x$ |'
 # Fragment answer alone is insufficient context: retain final whole derivative.
 task=task_identity(u,v,target)
 rendered_values=([FMT.normalize_tex(clean(a[':answer/value'])) for a in q[':question/answer-fields'][0][':answer-field/choices']] if original and q.get(':question/answer-fields') else [FMT.normalize_tex(tex(z)) for z in values])
 content=digest([FMT.normalize_prose(prompt),FMT.normalize_prose(worked),field_type,key,sorted(rendered_values),FMT.normalize_tex(tex(answer)),selected])
 qid=uid('question:'+content);fid=uid('field:'+content+':'+key)
 choices=[]
 for z,value in zip(values,rendered_values):
  choices.append({':answer/id':uid('answer:'+fid+':'+s.srepr(z)),':answer/type':':answer.type/math',':answer/value':value})
 correct=next(a[':answer/id'] for a,z in zip(choices,values) if equivalent(z,answer));r.shuffle(choices)
 rec={'knowledge_point':{'db_id':KP_ID,'id':KP[':knowledge-point/id'],'title':KP[':knowledge-point/title']},'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+difficulty,':question/problem':FMT.normalize_prose(prompt),':question/worked-solution':FMT.normalize_prose(worked),':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+field_type,':answer-field/choices':choices,':answer-field/correct':[':answer/id',correct]}]},'generation':{'version':VERSION,'seed':seed,'template':t,'parameters':p,'bank_profile':selected,'source_ids':[t] if t!=HARD else ['e-3638','q-47943','q-47998'],'source_basis':2275,'source_lineage':RAW['lineage'],'mathematical_fingerprint':task,'domain':domain(u,v),'authored_extension':not original,'evidence_only':False,'eligible':True,'raw_exact_eligible':False,'source_repairs':repairs,'authored_repair':bool(repairs),'supported_normalization':['canonical TeX function names and prime notation','redundant nested aligned wrappers flattened with operative rows retained'] if original else [],'plot_rating':'none','sympy_version':s.__version__}}
 rec['generation']['content_fingerprint']=content;return rec

def replay_raw(source_id):
 q=copy.deepcopy(SOURCES[source_id])
 return {'knowledge_point':{'db_id':KP_ID,'id':KP[':knowledge-point/id'],'title':KP[':knowledge-point/title']},'question':q,'generation':{'template':source_id,'source_id':source_id,'source_basis':2275,'evidence_only':True,'eligible':False,'raw_exact':True}}

def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)
def generate_hard(seed=0,**kw):return generate('hard',seed,**kw)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['all',*SUPPORTED_LEVELS],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--template');ap.add_argument('--format',choices=['json','markdown'],default='json');a=ap.parse_args();out=[];seen=set()
 if type(a.count)is not int or a.count<1:ap.error('positive builtin integer count required')
 for level in SUPPORTED_LEVELS if a.difficulty=='all' else [a.difficulty]:
  if a.count>CAPACITY[level]:ap.error('requested count exceeds finite '+level+' task capacity')
  count=0
  for i in range(a.count*1000):
   rec=generate(level,a.seed+i,a.template);fp=rec['generation']['mathematical_fingerprint']
   if fp in seen:continue
   seen.add(fp);out.append(rec);count+=1
   if count==a.count:break
  if count!=a.count:raise ValueError('unique capacity exhausted')
 print(json.dumps(out,indent=2) if a.format=='json' else '\n\n---\n\n'.join(z['question'][':question/problem']+'\n\n'+z['question'][':question/worked-solution'] for z in out))
