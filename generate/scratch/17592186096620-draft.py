#!/usr/bin/env python3
"""Draft polynomial quotient generator; immutable basis2275 evidence, no DB calls.

Easy: source-shaped polynomial quotients. Moderate: authored affine/quadratic
with two denominator terms. Hard: authored two-term quadratic numerator and
quadratic denominator, six distributed products. No new derivative rules.
Observed historical radio banks are opaque bounded transport, evidence only.
"""
import argparse, copy, hashlib, importlib.util, json, random, sys, uuid
from pathlib import Path
import sympy as s
HERE=Path(__file__).with_suffix('')
def frozen(name):
 spec=importlib.util.spec_from_file_location('quotient_draft_'+name,HERE/(name+'.py'))
 mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod
FORMAT=frozen('math_format')
RAW=json.loads((HERE/'source.json').read_text());KP=RAW['record']
KP_ID=17592186096620;KP_UUID=KP[':knowledge-point/id'];TITLE=KP[':knowledge-point/title']
VERSION='polynomial-quotients-draft-2026-10-14-v1';SUPPORTED_LEVELS=('easy','moderate','hard')
X,K=s.symbols('x k',real=True)
SOURCES={q[':question/math-academy-id']:q for q in KP[':knowledge-point/questions'] if ':question/math-academy-id' in q}
TEMPLATES={
'q-11955':dict(p={'c':-2,'a':4,'b':-9},kind='constant-linear',field='radio'),
'q-11966':dict(p={'c':-5,'a':2,'b':-1},kind='linear-linear',field='radio'),
'q-104305':dict(p={'c':10,'a':-1,'d':3},kind='constant-quadratic',field='blank'),
'q-104309':dict(p={'c':-2,'e':3,'a':2,'d':-2},kind='affine-quadratic',field='blank'),
'q-340290':dict(p={'c':2},kind='constant-square',field='blank'),
'q-128235':dict(p={'e':-2,'b':4},kind='symbolic',field='blank'),
'q-128335':dict(p={'c':7,'a':2,'b':-5,'d':-3},kind='constant-three',field='blank'),
'q-340287':dict(p={'c':1,'b':1},kind='constant-unit',field='blank'),
'q-340297':dict(p={'c':6,'a':-3,'b':1},kind='linear-linear',field='blank'),
'q-340298':dict(p={'c':1,'b':1},kind='square-linear',field='blank'),
'q-340303':dict(p={'c':1,'b':1},kind='linear-square',field='blank'),
'authored-moderate':dict(p={'c':2,'e':3,'a':1,'d':2},kind='affine-quadratic',field='blank'),
'authored-hard':dict(p={'c':2,'e':3,'a':1,'d':2},kind='quadratic-pair',field='blank')}

def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def uid(v):return str(uuid.uuid5(uuid.UUID(KP_UUID),v))
def tex(v):return s.latex(v)
def frac(n,d):return r'\frac{'+n+'}{'+d+'}'
def group(v):return '('+tex(v)+')'
def product(a,b):return group(a)+r'\cdot '+group(b)
def exact_int(v):return type(v) is int

def parts(t,p):
 kind=TEMPLATES[t]['kind'];c=p.get('c',1);a=p.get('a',1);b=p.get('b',0);d=p.get('d',0);e=p.get('e',0)
 if kind=='constant-linear':return s.Integer(c),a*X+b
 if kind=='linear-linear':return c*X,a*X+b
 if kind=='constant-quadratic':return s.Integer(c),a*X**2+d
 if kind=='affine-quadratic':return c*X+e,a*X**2+d
 if kind=='constant-square':return s.Integer(c),X**2
 if kind=='symbolic':return X+e,X**2+b*X+K
 if kind=='constant-three':return s.Integer(c),a*X**2+b*X+d
 if kind=='constant-unit':return s.Integer(c),X+b
 if kind=='square-linear':return c*X**2,X+b
 if kind=='linear-square':return c*X,X**2+b
 if kind=='quadratic-pair':return c*X**2+e*X,a*X**2+d
 raise ValueError(t)

def allowed(t,level,p):
 if t not in TEMPLATES:raise ValueError('unknown template')
 if set(p)!=set(TEMPLATES[t]['p']):raise ValueError('parameter keys do not match family')
 if any(not exact_int(v) or abs(v)>12 for v in p.values()):raise ValueError('builtin integer coefficients, absolute value <=12 required')
 if any(p[k]==0 for k in ('a','c','b','d','e') if k in p):raise ValueError('all declared substantive coefficients must be nonzero')
 if level=='moderate' and (t!='authored-moderate' or any(abs(v)>4 for v in p.values())):raise ValueError('moderate affine/two-term-quadratic coefficients 1..4 in magnitude')
 if level=='hard' and (t!='authored-hard' or any(abs(v)>3 for v in p.values())):raise ValueError('hard two-term-quadratic coefficients 1..3 in magnitude')
 if level=='easy' and t.startswith('authored-'):raise ValueError('authored template belongs to its named level')
 if t=='q-104309' and (p['a']%2 or p['d']%2 or p['c']%2):raise ValueError('source denominator cancellation family requires even a,d,c')
 u,v=parts(t,p)
 if s.diff(u/v,X)==0:raise ValueError('constant quotient excluded')
 return u,v

def answer_tex(u,v):
 n=s.expand(s.diff(u,X)*v-u*s.diff(v,X));content=s.Poly(v,X).content();base=s.cancel(v/content);top=s.cancel(n/content**2)
 if s.degree(s.gcd(top,base),X)>0:
  reduced=s.cancel(n/v**2);reduced_den=s.fraction(reduced)[1]
  # A rational expression must retain every originally excluded denominator
  # root. Cancel powers only when the excluded set remains identical.
  if s.Poly(reduced_den,X).sqf_part().monic()==s.Poly(v,X).sqf_part().monic():return tex(s.factor(reduced))
 return frac(tex(top),tex(s.Pow(base,2,evaluate=False)))

def bank(t,p,profile,u,v,field):
 du,dv=s.diff(u,X),s.diff(v,X);answer=s.cancel((du*v-u*dv)/v**2)
 if field=='blank':return [answer],answer
 if profile=='observed-11955':
  c,a,b=map(s.Integer,(p['c'],p['a'],p['b']));values=[-c*a/(-b)/v**2,-c/v**2,-c*a/v**2,-c/2/v**2,-a/v**2]
 elif profile=='observed-11966':
  c,a,b=map(s.Integer,(p['c'],p['a'],p['b']));values=[(-c*a*X+c*b)/v**2,(-2*c*a*X+c*b)/v**2,c*b/v**2,(c*b+c*a*X)/v**2,-c*b/v**2]
 elif profile=='method':
  # Complete operation bank: correct; reversed subtraction; added products;
  # unsquared denominator; quotient of polynomial derivatives (when defined).
  if dv==0:raise ValueError('bank requires nonzero denominator derivative')
  values=([answer,-answer,-u/v**2,-u*dv/v,s.Integer(0)] if du==0 else [answer,-answer,(du*v+u*dv)/v**2,(du*v-u*dv)/v,du/dv])
 else:raise ValueError('unknown complete bank')
 if sum(s.cancel(z-answer)==0 for z in values)!=1 or any(s.cancel(z-y)==0 for i,z in enumerate(values) for y in values[:i]):raise ValueError('complete bank collision')
 return values,answer

RULE=r'\frac{u^{\prime}(x)\cdot v(x)-u(x)\cdot v^{\prime}(x)}{[v(x)]^{2}}'
def polynomial_terms(z):
 return [coef*X**power[0] for power,coef in s.Poly(s.expand(z),X).terms()]
def expanded_product(a,b):
 terms=[s.expand(i*j) for i in polynomial_terms(a) for j in polynomial_terms(b)]
 return terms

def sum_tex(terms):
 out=''
 for i,z in enumerate(terms):
  if z==0:continue
  neg=z.could_extract_minus_sign();v=-z if neg else z
  out+= ('-' if neg else '+' if out else '')+tex(v)
 return out or '0'

def final_tex(t,u,v):
 if t=='q-128335':return frac(product(u,-s.diff(v,X)),tex(s.Pow(v,2,evaluate=False)))
 if t=='q-340287' and u>0:return '-'+frac(tex(u),tex(s.Pow(v,2,evaluate=False)))
 return answer_tex(u,v)

def solution(t,u,v):
 du,dv=s.diff(u,X),s.diff(v,X);den=tex(s.Pow(v,2,evaluate=False));n=s.expand(du*v-u*dv)
 substituted=frac(product(du,v)+'-'+product(u,dv),den)
 left=expanded_product(du,v);right=expanded_product(u,dv)
 if t=='q-104309':right=list(reversed(right))
 expanded=frac(sum_tex(left+[-z for z in right]),den)
 combined=frac(tex(n),den);final=final_tex(t,u,v)
 rows=[RULE,substituted]
 if t in ('q-11955','q-104305'):rows+=[final]
 elif t=='q-128235':
  # Source explicitly expands each product while retaining subtraction groups.
  rows += [frac('('+tex(s.expand(du*v))+')-('+tex(s.expand(u*dv))+')',den),final]
 elif t=='q-128335':
  rows += [frac('-'+product(u,dv),den),final]
 elif t=='q-104309':
  content=s.Poly(v,X).content();base=s.cancel(v/content)
  # Source keeps the common factor4 in the denominator before cancellation.
  rows += [expanded,frac(tex(n),(tex(content**2) if content**2!=1 else '')+tex(s.Pow(base,2,evaluate=False))),final]
 elif t in ('q-340290','q-340287'):
  rows += [frac(tex(n),tex(s.expand(v**2))) if t=='q-340290' else combined,final]
 else:rows += [expanded,final]
 prose='The numerator and denominator are $u(x)='+tex(u)+'$ and $v(x)='+tex(v)+',$ respectively. Their derivatives are given by\n\n'
 if t=='q-128335':prose+='$$\n'+r'u^{\prime}(x)='+tex(du)+r',\,v^{\prime}(x)='+tex(dv)+'.\n$$'
 else:prose+='$$\n'+r'\begin{aligned}u^{\prime}(x)&='+tex(du)+r',\\v^{\prime}(x)&='+tex(dv)+r'.\end{aligned}'+'\n$$'
 prose+='\n\nApplying the quotient rule, we have\n\n$$\n'+r'\begin{aligned}f^{\prime}(x)&='+r'\\ &='.join(rows)+r'.\end{aligned}'+'\n$$'
 return prose

def normalize(q):
 for k in (':question/problem',':question/worked-solution'):
  if k in q:q[k]=FORMAT.normalize_prose(q[k])
 for f in q.get(':question/answer-fields',[]):
  for a in f[':answer-field/choices']:a[':answer/value']=FORMAT.normalize_tex(a[':answer/value'])
 return q

def assemble(level,seed,t,p,profile,field,u,v):
 values,answer=bank(t,p,profile,u,v,field)
 prompt='Given that $f(x)='+frac(tex(u),tex(v))+r'$, find $f^{\prime}(x).$'
 if t=='q-128235':prompt='Find the derivative of $f(x)='+frac(tex(u),tex(v))+'.$ Treat $k$ as a constant.'
 if t=='q-128335':prompt=r'Calculate $f^{\prime}(x)$ for $f(x)='+frac(tex(u),tex(v))+'.$'
 key='selection' if field=='radio' else 'field-1'
 if field=='blank':prompt+='\n\n'+r'$f^{\prime}(x)=$'+'\n{{field-1}}'
 q=normalize({':question/problem':prompt,':question/worked-solution':solution(t,u,v),':question/difficulty':':question.difficulty/'+level})
 rendered=[FORMAT.normalize_tex(tex(z)) for z in values] if field=='radio' else [FORMAT.normalize_tex(final_tex(t,u,v))]
 content=digest([VERSION,level,q,field,sorted(rendered),FORMAT.normalize_tex(tex(answer))]);qid=uid('question:'+content);fid=uid('field:'+qid+key)
 choices=[{':answer/id':uid('answer:'+fid+s.srepr(s.cancel(z))),':answer/type':':answer.type/math',':answer/value':val} for z,val in zip(values,rendered)]
 cid=next(a[':answer/id'] for a,z in zip(choices,values) if s.cancel(z-answer)==0)
 random.Random(seed).shuffle(choices)
 q.update({':question/id':qid,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+field,':answer-field/choices':choices,':answer-field/correct':[':answer/id',cid]}]})
 # Original denominator zeros survive rational cancellation; monic square-free
 # polynomial records that excluded set independently of multiplicities/scaling.
 domain=s.Poly(v,X).sqf_part().monic().as_expr()
 task=digest([s.srepr(s.cancel(u/v)),s.srepr(domain),'find fprime'])
 evidence=profile.startswith('observed-')
 result={'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'template':t,'profile':profile,'parameters':p,'source_ids':[t] if t in SOURCES else ['e-3637','q-104309','q-340298'],'source_basis':RAW['basis'],'source_lineage':RAW['lineage'],'math_fingerprint':task,'content_fingerprint':content,'domain':tex(v)+r'\ne0','evidence_only':evidence,'eligible_for_learning':not evidence,'source_repairs':({'q-11966':['authored easy placement, correct designation and worked solution'],'q-104305':['authored supported blank field'],'q-104309':['authored supported blank field'],'q-128235':['restore supplied function from solution'],'q-128335':['restore supplied function from solution']}.get(t,[])),'origin':'observed family with method-derived authored bank' if profile=='method' else 'opaque observed bank transport' if evidence else 'source-shaped blank' if t in SOURCES else 'authored missing-level extension','python_version':sys.version.split()[0],'sympy_version':s.__version__,'plot_rating':'none'}}

 FORMAT.validate_generated_record(result)
 for text in [q[":question/problem"],q[":question/worked-solution"],*rendered]:
  if any(ord(ch)<32 and ch not in "\n\t\r" for ch in text):raise ValueError("unintended control character")
 return result

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in SUPPORTED_LEVELS:raise ValueError('unknown difficulty')
 if not exact_int(seed):raise ValueError('seed must be builtin int')
 r=random.Random(seed)
 candidates=list(SOURCES) if level=='easy' else ['authored-'+level]
 t=template or r.choice(candidates)
 if t not in TEMPLATES:raise ValueError('unknown template')
 field=TEMPLATES[t]['field'] if field_type is None else field_type
 if field not in ('blank','radio') or field!=TEMPLATES[t]['field']:raise ValueError('field type must preserve the family contract')
 profile=profile or ('method' if field=='radio' else 'fragment')
 if profile not in ('method','fragment','observed-11955','observed-11966','raw') or (profile.startswith('observed-') and profile!='observed-'+t[2:]):raise ValueError('ineligible profile')
 if profile=='raw':
  if parameters is not None and parameters!=TEMPLATES[t]['p']:raise ValueError('raw immutable evidence uses captured parameters; use observed profile for parameterized banks')
  if level!='easy' or t not in SOURCES:raise ValueError('raw source evidence requires source family')
  return raw_record(t,seed)
 if field=='blank' and profile!='fragment':raise ValueError('blanks have no radio bank')
 if field=='radio' and profile=='fragment':raise ValueError('radio needs a complete bank')
 if parameters is not None:
  p=dict(parameters);u,v=allowed(t,level,p);return assemble(level,seed,t,p,profile,field,u,v)
 bound=4 if level=='moderate' else 3 if level=='hard' else 12
 # Select a complete profile/family before parameters; never pool distractors.
 for _ in range(1000):
  p={k:r.choice([z for z in range(-bound,bound+1) if z]) for k in TEMPLATES[t]['p']}
  try:
   u,v=allowed(t,level,p);return assemble(level,seed,t,p,profile,field,u,v)
  except ValueError:continue
 raise ValueError('no eligible complete instance in bounded sampler')

def raw_record(t,seed=0):
 """Immutable captured evidence, explicitly not a generated learning instance.

Exact source originals and omissions are retained here; separately parameterized
observed profiles transport all banks through normal generation.
"""
 q=copy.deepcopy(SOURCES[t])
 def enums(o):
  if isinstance(o,dict):
   if set(o)=={':db/ident'}:return o[':db/ident']
   return {k:enums(v) for k,v in o.items()}
  if isinstance(o,list):return [enums(v) for v in o]
  return o
 q=enums(q)
 for f in q.get(':question/answer-fields',[]):
  if ':answer-field/correct' in f:f[':answer-field/correct']=[':answer/id',f[':answer-field/correct'][':answer/id']]
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'template':t,'profile':'raw','parameters':TEMPLATES[t]['p'],'source_basis':RAW['basis'],'source_lineage':RAW['lineage'],'evidence_only':True,'eligible_for_learning':False,'source_raw_exact':True}}

# Easy source-backed families and original radio layouts.
def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
# Moderate authored affine/two-term-quadratic, four polynomial products.
def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)
# Hard authored two-term quadratics, six polynomial products; degrees remain2.
def generate_hard(seed=0,**kw):return generate('hard',seed,**kw)

def batch(level,count,seed=0,template=None,profile=None):
 if not exact_int(count) or not 0<=count<=1000:raise ValueError('count builtin int0..1000')
 records=[];seen=set()
 for i in range(max(1000,count*100)):
  if len(records)==count:return records
  rec=generate(level,seed+i,template=template,profile=profile)
  fp=rec['generation'].get('math_fingerprint')
  if fp is None:raise ValueError('raw evidence cannot form a learning batch')
  if fp not in seen:seen.add(fp);records.append(rec)
 raise ValueError('finite bounded search exhausted at '+str(len(records)))

def markdown(r):
 q=r['question'];return q[':question/problem']+'\n\n'+'\n'.join('$'+a[':answer/value']+'$' for f in q.get(':question/answer-fields',[]) for a in f[':answer-field/choices'])+'\n\n'+q.get(':question/worked-solution','[Source solution absent.]')
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=(*SUPPORTED_LEVELS,'all'),default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=('json','markdown'),default='json');ap.add_argument('--template');ap.add_argument('--profile');a=ap.parse_args()
 try:
  if a.profile=='raw':
   if a.count!=1 or a.difficulty not in ('easy','all'):raise ValueError('raw CLI evidence requires count1 and easy difficulty')
   targets=[a.template] if a.template else list(SOURCES)
   out=[generate('easy',a.seed,template=t,profile='raw') for t in targets]
  else:out=[r for level in SUPPORTED_LEVELS if a.difficulty in (level,'all') for r in batch(level,a.count,a.seed,a.template,a.profile)]
 except ValueError as e:ap.error(str(e))
 print(json.dumps(out,indent=2) if a.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in out))
