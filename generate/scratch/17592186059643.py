#!/usr/bin/env python3
"""Common denominator + Pythagorean identity, fixed math snapshot basis 1356.

Observed templates are complete parameterized prompt/solution/bank masks. The
argument and sine/cosine duality slots preserve every ordered source stage.
raw-observed is evidence only and retains missing attributes and source errors.
repaired-observed makes only documented corrections and remains evidence-only:
source shapes establish values, not the authors' distractor intention.
Default authored radio banks derive every wrong expression from a stated
operation and reject an entire ambiguous bank. No database or engine writes.

Easy: a F + a G²/F; one common denominator then identity. Missing level authored
from unrated q23522, canonical common-denominator example and prerequisites.
Moderate: a F/G + a G/F; two crossed numerators then identity and reciprocals.
Hard: (a+b G)/F + b F/G; rewrite quotient, cross-multiply, expand, collect
squares and use identity; nonzero independent a,b preserve the linear term.
All coefficients are reduced rationals |numerator|<=6, denominator<=3,
0<|coefficient|<=4; products/combined constants have numerator <=36 and
reduced denominator <=9. Sampling and explicit inputs use identical guards.
Signs and sine/cosine orientations are equal-workload alternatives, not stages
of a progression. Mathematical fingerprints exclude variables/banks/order.
"""
from __future__ import annotations
import argparse, hashlib, json, random, re, uuid
from functools import lru_cache
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
KP_ID=17592186059643
KP_UUID='1bc8c875-3393-5fd6-90cf-87737e16f2f2'
TITLE='Simplifying a Trigonometric Expression Using a Common Denominator and the Pythagorean Identity'
VERSION='common-denominator-pythagorean-1'
ROOT=Path(__file__).with_suffix('')
MASKS=json.loads((ROOT/'template-masks.json').read_text())
S,C=sp.symbols('S C',real=True)
TEMPLATES={**{k:v['level'] for k,v in MASKS.items()},'one_denominator':'easy','crossed_fractions':'moderate','squared_shift':'moderate','linear_plus_quotient':'hard'}
COEFFICIENTS=tuple(sorted({sp.Rational(n,d) for n in range(-6,7) for d in range(1,4) if n and abs(sp.Rational(n,d))<=4}))
ARGUMENTS=('x','t',r'\theta',r'\alpha')
PROVENANCE={k:json.loads((ROOT/'source.json').read_text())[k] for k in ('database','basis','lineage')}

def tex(q):
 return sp.latex(sp.Rational(q))
def frac(a,b): return r'\frac{'+a+'}{'+b+'}'
def mul(a,b): return '('+a+r')\cdot ('+b+')'

def equivalent(a,b):
 n=sp.cancel(a-b).as_numer_denom()[0]
 return sp.rem(sp.Poly(n,S,C),sp.Poly(S*S+C*C-1,S,C)).as_expr()==0

@lru_cache(maxsize=40000)
def parse_math(text):
 """Independent small TeX parser for displayed source/authored trig expressions.
 Read complete fractions, function applications, powers and implicit products.
 Does not use generation parameters or correct-answer identities.
 """
 text=text.strip().rstrip('.').rstrip('=').strip().replace('⁡','').replace(r'\left','').replace(r'\right','')
 text=re.sub(r'\\operatorname\{(sin|cos|tan|cot|sec|csc)\}',lambda m:'\\'+m[1],text)
 text=re.sub(r'\{(sin|cos|tan|cot|sec|csc)\}',lambda m:'\\'+m[1],text)
 text=text.replace(r'\dfrac',r'\frac').replace(r'\cdot','*')
 def group(i):
  assert text[i]=='{',(text,i)
  depth=1;j=i+1
  while depth:
   assert j<len(text),text
   depth+=(text[j]=='{')-(text[j]=='}');j+=1
  return text[i+1:j-1],j
 def convert():
  out='';i=0
  while i<len(text):
   if text.startswith(r'\frac',i):
    i+=5
    while text[i].isspace():i+=1
    a,i=group(i)
    while text[i].isspace():i+=1
    b,i=group(i);out+='('+str(parse_math(a))+')/('+str(parse_math(b))+')';continue
   if text.startswith(r'\cancel',i):
    i+=7;a,i=group(i);out+='('+str(parse_math(a))+')';continue
   m=re.match(r'\\(sin|cos|tan|cot|sec|csc)(?:\s*\^\s*(\{[^{}]+\}|[234]))?\s*(?:\{\s*(?:\\theta|\\alpha|θ|[xt])\s*\}|\\theta|\\alpha|θ|[xt])',text[i:])
   if m:
    val={'sin':'S','cos':'C','tan':'(S/C)','cot':'(C/S)','sec':'(1/C)','csc':'(1/S)'}[m[1]]
    if m[2]:val='('+val+')**('+m[2].strip('{}')+')'
    out+='('+val+')';i+=len(m[0]);continue
   if text[i]=='{':
    a,i=group(i);out+='('+str(parse_math(a))+')';continue
   if text[i]=='^':out+='**';i+=1;continue
   out+=text[i];i+=1
  return out
 return parse_expr(convert(),local_dict={'S':S,'C':C},transformations=standard_transformations+(implicit_multiplication_application,))

def repair(tid,text):
 if text is None:return None
 if tid=='observed_q_70783':pass
 sid=MASKS[tid]['source_id']
 if sid==17592186253599:text=text.replace(r'{2+\operatorname{sin}',r'{1+\operatorname{sin}')
 if sid==17592186253600:text=text.replace(r'{1+{sin}^{2}}',r'{1+{sin}^{2}⁡\theta }')
 if sid==17592186329718:text=text.replace(r'\operatorname{cos}⁡\theta ',r'\operatorname{cos}⁡t')
 if sid==17592186335821:text=text.replace(r'  & \frac',r'  & =\frac')
 return text

def render_mask(text,old,arg,dual):
 if text is None:return None
 # Complete argument tokens and complete function names only; never short global slots.
 if old.startswith('\\'):text=text.replace(old,arg)
 else:text=re.sub(r'(?<![A-Za-z])'+re.escape(old)+r'(?![A-Za-z])',lambda _:arg,text)
 if dual:
  swap={'sin':'cos','cos':'sin','tan':'cot','cot':'tan','sec':'csc','csc':'sec'}
  text=re.sub(r'(?<![A-Za-z])(sin|cos|tan|cot|sec|csc)(?![A-Za-z])',lambda m:swap[m[0]],text)
 return text

def source_payload(tid,p,profile):
 m=MASKS[tid]; raw=profile=='raw-observed'
 def r(text):return render_mask(text if raw else repair(tid,text),m['argument'],p['argument'],p['dual'])
 prompt=r(m['problem']); solution=r(m['solution']); bank=[r(v) for v in m['bank']]
 idx=m['correct']
 if not raw and idx is None:
  expr=parse_math(prompt.split('$')[1]); idx=next(i for i,v in enumerate(bank) if equivalent(expr,parse_math(v)))
  arg=p['argument'];F=(r'\sin ' if p['dual'] else r'\cos ')+arg;G=(r'\cos ' if p['dual'] else r'\sin ')+arg
  F2=(r'\sin^{2} ' if p['dual'] else r'\cos^{2} ')+arg;G2=(r'\cos^{2} ' if p['dual'] else r'\sin^{2} ')+arg
  if m['source_id']==17592186060072:
   den='(1-'+G+r')\cdot '+F
   rows=[frac(F,'1-'+G)+'-'+frac(G,F),frac(F2,den)+'-'+frac(G+r'\cdot (1-'+G+')',den),frac(F2+'-'+G+'+'+G2,den),frac('1-'+G,den),frac('1',F),bank[idx]]
   opening='First, we rewrite the second term using the definition of the quotient ratio. This gives:'
  else:
   rows=[frac(F2,F)+'+'+frac(G2,F),frac(F2+'+'+G2,F),frac('1',F),bank[idx]]
   opening='We put both terms over a common denominator, and combine the two fractions:'
  solution=opening+'\n\n$$\n'+prompt.split('$')[1]+'='+rows[0]+'\n$$\n\nWe put both terms over a common denominator, and combine the two fractions:\n\n$$\n'+r'\begin{aligned}'+rows[0]+''.join(r' & ='+v+r' \\ ' for v in rows[1:])+r'\end{aligned}'+'\n$$\n\nThe simplification uses $'+F2+'+'+G2+'=1$. Therefore, we conclude that\n\n$$\n'+prompt.split('$')[1]+'='+bank[idx]+'.\n$$'
 return prompt,solution,bank,idx,not raw or m['difficulty_present'],not raw or m['solution_present']

def guard(level,p,observed=False,tid=None):
 allowed={'argument','dual'} if observed else {'argument','dual','a','b'}
 if set(p)-allowed:raise ValueError('unknown parameters')
 if p['argument'] not in (*ARGUMENTS,'θ'):raise ValueError('unsupported argument')
 if type(p['dual']) is not bool:raise ValueError('dual must be boolean')
 if observed:return
 for name in ('a','b'):
  q=sp.Rational(p[name])
  if q not in COEFFICIENTS:raise ValueError('reduced coefficient exceeds workload ceiling or is zero')
  p[name]=str(q)
 if level!='hard' and tid!='squared_shift' and p['b']!='1':raise ValueError('unused b must be 1')
 if tid=='squared_shift' and sp.Rational(p['b'])<=0:raise ValueError('squared shift requires positive b')
 if level=='hard' or tid=='squared_shift':
  a,b=map(sp.Rational,(p['a'],p['b']))
  for q in (a*b,a+b,a-b):
   if abs(q.p)>36 or q.q>9:raise ValueError('combined arithmetic ceiling')

def authored_payload(level,p,tid):
 arg=p['argument']; f=(r'\cos ' if p['dual'] else r'\sin ')+arg;g=(r'\sin ' if p['dual'] else r'\cos ')+arg
 a,b=tex(p['a']),tex(p['b']); F,G=(C,S) if p['dual'] else (S,C)
 if level=='easy':
  prompt=mul(a,g)+'+'+frac(mul(a,f+'^{2}'),g)
  # Powers attach to function, not its argument.
  f2=(r'\cos^{2} ' if p['dual'] else r'\sin^{2} ')+arg;g2=(r'\sin^{2} ' if p['dual'] else r'\cos^{2} ')+arg
  prompt=mul(a,g)+'+'+frac(mul(a,f2),g)
  rows=[frac(mul(a,g2),g)+'+'+frac(mul(a,f2),g),frac(mul(a,g2+'+'+f2),g),frac(a,g)]
  correct=sp.Rational(p['a'])/G
  bank=[frac(a,g),a,frac(a,f),frac(mul(a,g2+'-'+f2),g),frac(mul(a,g2+f2),g)]
  # Last operation drops the plus: use a*G²*F² / G.
  bank[-1]=frac(mul(a,g2+r'\cdot '+f2),g)
 elif tid=='squared_shift':
  f2=(r'\cos^{2} ' if p['dual'] else r'\sin^{2} ')+arg;g2=(r'\sin^{2} ' if p['dual'] else r'\cos^{2} ')+arg
  den=b+'+'+f2
  prompt=a+'+'+frac(mul(a,g2),den)
  final=tex(sp.Rational(p['a'])*(sp.Rational(p['b'])+1))
  rows=[frac(mul(a,'('+den+')'),den)+'+'+frac(mul(a,g2),den),frac(mul(a,b)+'+'+mul(a,f2)+'+'+mul(a,g2),den),frac(mul(a,b+'+1'),den),frac(final,den)]
  correct=sp.Rational(p['a'])*(sp.Rational(p['b'])+1)/(sp.Rational(p['b'])+F*F)
  bank=[rows[-1],frac(mul(a,g2),den),frac(final,b+'+'+f),frac(tex(sp.Rational(p['a'])*sp.Rational(p['b'])),den),mul(a,den)]
 elif level=='moderate':
  f2=(r'\cos^{2} ' if p['dual'] else r'\sin^{2} ')+arg;g2=(r'\sin^{2} ' if p['dual'] else r'\cos^{2} ')+arg
  den=f+r'\cdot '+g
  prompt=frac(mul(a,f),g)+'+'+frac(mul(a,g),f)
  rows=[frac(mul(a,f2),den)+'+'+frac(mul(a,g2),den),frac(mul(a,f2+'+'+g2),den),frac(a,den)]
  correct=sp.Rational(p['a'])/(F*G)
  bank=[frac(a,den),frac(a,g),frac(a,f),frac(mul(a,f2+'-'+g2),den),frac(mul(a,f2+r'\cdot '+g2),den)]
 else:
  f2=(r'\cos^{2} ' if p['dual'] else r'\sin^{2} ')+arg;g2=(r'\sin^{2} ' if p['dual'] else r'\cos^{2} ')+arg
  quotient=(r'\cot ' if p['dual'] else r'\tan ')+arg;den=f+r'\cdot '+g
  numerator=a+'+'+mul(b,g)
  prompt=frac(numerator,f)+'+'+mul(b,quotient)
  correct=(sp.Rational(p['a'])*G+sp.Rational(p['b']))/(F*G)
  rows=[frac(numerator,f)+'+'+frac(mul(b,f),g),frac('('+numerator+r')\cdot '+g,den)+'+'+frac(mul(b,f2),den),frac(mul(a,g)+'+'+mul(b,g2)+'+'+mul(b,f2),den),frac(mul(a,g)+'+'+mul(b,'('+g2+'+'+f2+')'),den),frac(mul(a,g)+'+('+b+')',den)]
  bank=[rows[-1],frac(b,den),frac(mul(a,g)+'-('+b+')',den),frac(mul(a,g)+'+'+mul(b,g2+'-'+f2),den),frac(mul(a,g),den)]
 opening='First, we rewrite the second term using the definition of the quotient ratio. This gives:' if level=='hard' else 'We put both terms over a common denominator, and combine the two fractions:'
 solution=opening+'\n\n$$\n'+prompt+'='+rows[0]+'\n$$\n\n'+('We put both terms over a common denominator, and combine the two fractions:\n\n' if level=='hard' else '')+'$$\n'+r'\begin{aligned}'+rows[0]+''.join(r' & ='+row+r' \\ ' for row in rows[1:])+r'\end{aligned}'+'\n$$\n\nFinally, we simplify using the Pythagorean identity $'+f2+'+'+g2+'=1$. Therefore, we conclude that\n\n$$\n'+prompt+'='+bank[0]+'.\n$$'
 values=[parse_math(v) for v in bank]
 if not equivalent(parse_math(prompt),correct):raise ValueError('printed prompt differs from answer')
 for i,v in enumerate(values):
  if any(equivalent(v,w) for w in values[:i]):raise ValueError('ambiguous complete bank')
 for row in rows:
  if not equivalent(parse_math(row),correct):raise ValueError('wrong displayed stage')
 return 'Simplify the trigonometric expression $'+prompt+'.$',solution,bank,0,True,True

def build(level,seed,tid,p,profile):
 observed=tid in MASKS
 prompt,solution,bank,idx,diff_present,sol_present=source_payload(tid,p,profile) if observed else authored_payload(level,p,tid)
 content={'version':VERSION,'prompt':prompt,'solution':solution if sol_present else None,'bank':sorted(bank),'correct':bank[idx] if idx is not None else None,'difficulty':level if diff_present else None}
 identity=hashlib.sha256(json.dumps(content,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
 qid=str(uuid.uuid5(uuid.NAMESPACE_URL,identity));fid=str(uuid.uuid5(uuid.UUID(qid),'selection'))
 answers=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),v)),':answer/type':':answer.type/math',':answer/value':v} for v in bank]
 field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers}
 if idx is not None:field[':answer-field/correct']=[':answer/id',answers[idx][':answer/id']]
 random.Random(seed).shuffle(answers)
 q={':question/id':qid,':question/problem':prompt,':question/answer-fields':[field]}
 if diff_present:q[':question/difficulty']=':question.difficulty/'+level
 if sol_present:q[':question/worked-solution']=solution
 expr=parse_math(prompt.split('$')[1]);fingerprint=hashlib.sha256(str(sp.cancel(expr.subs(S*S,1-C*C))).encode()).hexdigest()
 # Rational-circle substitution gives canonical task identity, independent of notation.
 u=sp.Symbol('u');canonical=sp.cancel(expr.subs({S:2*u/(1+u*u),C:(1-u*u)/(1+u*u)}))
 fingerprint=hashlib.sha256(str(canonical).encode()).hexdigest()
 domain='All denominators of the original expression are nonzero; retain original exclusions after cancellation.'
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'source':PROVENANCE,'template':tid,'profile':profile,'seed':seed,'parameters':p,'domain':domain,'mathematical_fingerprint':fingerprint,'content_fingerprint':identity,'evidence_only':observed,'eligible_for_learning':not observed,'source_id':MASKS[tid]['source_id'] if observed else None,'authored':not observed,'distractor_recipes':('observed parameterized shapes; intentions unresolved' if observed else ['correct','drop crossed term / denominator','wrong reciprocal / sign','subtract identity components','multiply instead of add / omit identity term'])}}

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('unknown difficulty')
 if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('only observed radio layout supported')
 tid=template or {'easy':'one_denominator','moderate':'crossed_fractions','hard':'linear_plus_quotient'}[level]
 if template is None and level=='moderate':tid=random.Random(seed).choice(('crossed_fractions','squared_shift'))
 if tid not in TEMPLATES or TEMPLATES[tid]!=level:raise ValueError('template difficulty mismatch')
 observed=tid in MASKS;profile=profile or ('repaired-observed' if observed else 'authored-operations')
 if profile not in (('raw-observed','repaired-observed') if observed else ('authored-operations',)):raise ValueError('unknown profile')
 rng=random.Random(seed)
 if parameters is not None:
  p=({'argument':MASKS[tid]['argument'],'dual':False} if observed else {'argument':'x','dual':False,'a':'1','b':'1'})|parameters
  guard(level,p,observed,tid);return build(level,seed,tid,p,profile)
 for _ in range(1000):
  p={'argument':rng.choice(ARGUMENTS),'dual':rng.choice((False,True))}
  if not observed:p.update(a=str(rng.choice(COEFFICIENTS)),b=str(rng.choice(COEFFICIENTS)) if level=='hard' else (str(rng.choice([q for q in COEFFICIENTS if q>0])) if tid=='squared_shift' else '1'))
  guard(level,p,observed,tid)
  try:return build(level,seed,tid,p,profile)
  except ValueError:
   if observed:raise
 raise ValueError('no eligible complete bank')

# EASY: authored missing level, single nontrivial common denominator.
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
# MODERATE: two nontrivial crossed denominators; a!=0.
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
# HARD: quotient rewrite, independent linear coefficient, expanded crossed numerator.
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)

def markdown(r,origin=None):
 """Annotated author preview; never inserts inferred keys into a raw record."""
 q=r['question'];meta=r['generation'];tid=meta['template'];m=MASKS.get(tid)
 raw=meta['profile']=='raw-observed';unrated=m is not None and not m['difficulty_present']
 level=q.get(':question/difficulty','').split('/')[-1].title()
 label='Unrated (raw source)' if raw and unrated else level+(' (inferred; original source unrated)' if unrated else '')
 origin=origin or ('Raw source evidence-only' if raw else ('Repaired source evidence-only' if m is not None else 'Normal authored practice'))
 field=q[':question/answer-fields'][0];ref=field.get(':answer-field/correct')
 correct_id=ref[1] if ref is not None else None
 if correct_id is None:
  expr=parse_math(q[':question/problem'].split('$')[1])
  inferred=[a[':answer/id'] for a in field[':answer-field/choices'] if equivalent(expr,parse_math(a[':answer/value']))]
  if len(inferred)!=1:raise ValueError('review cannot infer a unique correct answer')
  correct_id=inferred[0]
 correct_note=('Inferred correct (original correct key absent)' if m is not None and m['correct'] is None else ('Correct (source designation)' if m is not None else 'Correct (computed)'))
 statuses=[]
 for key,present in ((':question/difficulty',':question/difficulty' in q),(':question/worked-solution',':question/worked-solution' in q),(':answer-field/correct',ref is not None)):
  if not present:status='absent in raw record'
  elif unrated:
   status='present (authored supported solution)' if key==':question/worked-solution' else 'present (inferred)'
  else:status='present (captured source attribute)' if m is not None else 'present (authored)'
  statuses.append('`'+key+'` '+status)
 out='**Level:** '+label+'.\n\n**Origin:** '+origin+'.\n\n**Attributes:** '+'; '.join(statuses)+'.\n\n'+q[':question/problem']+'\n\n'
 for a in field[':answer-field/choices']:
  mark=' — **'+correct_note+'**' if a[':answer/id']==correct_id else ''
  out+='- $'+a[':answer/value']+'$'+mark+'\n'
 if ':question/worked-solution' in q:out+='\n'+q[':question/worked-solution']+'\n'
 return out
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
 levels=['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]
 records=[generate(l,args.seed+i,template=args.template,profile=args.profile) for l in levels for i in range(args.count)]
 print(json.dumps(records,ensure_ascii=False,indent=2) if args.format=='json' else '\n\n'.join(markdown(r) for r in records))
