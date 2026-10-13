#!/usr/bin/env python3
"""Exact product-rule generator, math basis 1356; local review data only.

Observed easy templates retain original prose, full banks, fragments and stages.
Unrated log_log_radio/power_log_radio have authored easy assignment and solutions.
Moderate/hard are authored binomial/trinomial factor peers, no new chain/quotient
or tangent task. All explicit parameters obey the same bounds as sampling.
No EDB imports, transactions, images, registration, or source-payload return path.
"""
from __future__ import annotations
import argparse, hashlib, json, random, uuid
from functools import lru_cache
import sympy as s
X=s.Symbol('x',positive=True)
KP_ID=17592186096618
KP_UUID='f15a60dd-f6a7-577d-bdbc-148032de94c8'
TITLE='Differentiating a Product Containing an Exponential or Logarithmic Function'
VERSION='product-exp-log-1'
SOURCE={'database':'math','basis':1356,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}
# Shared helpers and immutable observed template specifications.
TEMPLATES={
 'log_log_radio':('easy','radio',('q-1933',)),
 'power_log_radio':('easy','radio',('q-47966',)),
 'base_sin_left_blank':('easy','blank',('q-319421',)),
 'power_exp_right_blank':('easy','blank',('q-319909','q-319903')),
 'linear_base_radio':('easy','radio',('q-11841',)),
 'power_exp_radio':('easy','radio',('q-1916',)),
 'cos_log_radio':('easy','radio',('q-1934',)),
 'base_tan_right_blank':('easy','blank',('q-319425',)),
 'power_exp_left_blank':('easy','blank',('q-319902',)),
 'base_log_left_blank':('easy','blank',('q-320814',)),
 'base_log_right_blank':('easy','blank',('q-320815',)),
 'base_log_negative_left_blank':('easy','blank',('q-320816',)),
 'binomial_exp_blank':('moderate','blank',()),
 'binomial_log_blank':('moderate','blank',()),
 'trinomial_exp_blank':('hard','blank',()),
 'trinomial_log_blank':('hard','blank',()),
}
# Complete banks, selected together; not first-valid pools.
PROFILES={t:t.removesuffix('_radio')+'_observed' for t,v in TEMPLATES.items() if v[1]=='radio'}
def tex(e):return s.latex(e,ln_notation=True).replace(r'\log',r'\ln')
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
def ident(v):return str(uuid.uuid5(uuid.NAMESPACE_URL,digest(v)))
@lru_cache(maxsize=1024)
def task_fingerprint(product):
 # Positive fixed bases normalize b^(kx) and exact log-base scalar identities.
 # Presentation, profiles and banks are deliberately absent from this key.
 return digest(s.srepr(s.expand(s.simplify(product))))
def coeff(c,z):return z if c==1 else '-'+z if c==-1 else str(c)+z
def xp(n):return 'x' if n==1 else '1' if n==0 else '{x}^{'+str(n)+'}'
def poly(c,n):return str(c) if n==0 else coeff(c,xp(n))
def exp(k=1):return '{e}^{'+coeff(k,'x')+'}'
def base(b,k=1):return '{'+str(b)+'}^{'+coeff(k,'x')+'}'
def op(f,arg):return r'\operatorname{'+f+'}('+str(arg)+')'
def logbase(b):return '{log}_{'+str(b)+'}⁡(x)'
def aligned(rows,prime='′'):
 return '$$\n\\begin{aligned}{f}^{'+prime+'}(x) & ='+r' \\  & ='.join(rows)+r'\end{aligned}'+'\n$$'
def opening(u,v,two=False):return 'Here, we have the product of '+('the two' if two else 'two')+' functions $u(x)='+u+'$ and $v(x)='+v+'.$ So, we apply the product rule:\n\n'
def prompt(product,prime='′'):return 'Given that $f(x)='+product+',$ find ${f}^{'+prime+'}(x).$'
def blank_prompt(pr,left=None,right=None):
 return pr+'\n\n${f}^{'+("'" if "{f}^{'}" in pr else '′')+'}(x)='+(''+left+r'\,+$'+'\n{{field-1}}' if left is not None else '$\n{{field-1}} $+\\,'+right+'$')
def bounds(t,p):
 """Guard reduced mathematical workload on explicit calls as well as samples."""
 expected=set(defaults(t));assert set(p)==expected,(t,'parameter keys',expected)
 if any(isinstance(v,bool) or not isinstance(v,int) for v in p.values()):raise ValueError('integer parameters required')
 for k in ('b','d'):
  if k in p and not 2<=p[k]<=10:raise ValueError('base must be 2..10')
 if t.startswith(('binomial','trinomial')):
  if not 2<=p['n']<=4 or not 1<=p['m']<p['n']:raise ValueError('distinct powers 1 <= m < n <= 4 required')
  for k in ('a','c','h'):
   if k in p and not 1<=abs(p[k])<=5:raise ValueError('all factor coefficients nonzero, magnitude <= 5')
  return
 if 'c' in p and not 1<=p['c']<=6:raise ValueError('coefficient 1..6')
 if 'n' in p:
  if t=='power_exp_radio' and not 2<=p['n']<=4:raise ValueError('power 2..4')
  if t=='power_log_radio' and not -4<=p['n']<=-1:raise ValueError('negative power -4..-1')
  if t.startswith('power_exp_') and not 2<=p['n']<=4:raise ValueError('power 2..4')
 if 'k' in p:
  if t=='base_log_negative_left_blank' and p['k']!=-1:raise ValueError('negative source template uses -x')
  if t=='power_exp_radio' and p['k']!=1:raise ValueError('observed radio bank uses e^x')
  if t!='base_log_negative_left_blank' and p['k'] not in (1,2,3):raise ValueError('scale 1..3')

def defaults(t):
 return {
 'log_log_radio':{'c':5,'b':3},'power_log_radio':{'n':-3,'b':2},
 'base_sin_left_blank':{'b':5},'power_exp_right_blank':{'c':1,'n':2,'k':2},
 'linear_base_radio':{'b':3},'power_exp_radio':{'c':1,'n':2,'k':1},'cos_log_radio':{'b':10},
 'base_tan_right_blank':{'b':4},'power_exp_left_blank':{'c':1,'n':3,'k':1},
 'base_log_left_blank':{'b':3,'d':3,'k':1},'base_log_right_blank':{'b':4,'d':4,'k':1},
 'base_log_negative_left_blank':{'b':5,'d':7,'k':-1},
 'binomial_exp_blank':{'a':2,'n':3,'c':3,'m':1},
 'binomial_log_blank':{'a':2,'n':3,'c':3,'m':1,'b':3},
 'trinomial_exp_blank':{'a':2,'n':3,'c':3,'m':1,'h':4},
 'trinomial_log_blank':{'a':2,'n':3,'c':3,'m':1,'h':4,'b':3},
 }[t].copy()
def sample(t,r):
 p=defaults(t)
 for k in p:
  if k in ('b','d'):p[k]=r.randint(2,10)
  elif k in ('a','h'):p[k]=r.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
  elif k=='c':p[k]=r.choice([-5,-4,-3,-2,-1,1,2,3,4,5]) if t.startswith(('binomial','trinomial')) else r.randint(1,6)
  elif k=='n':p[k]=r.randint(-4,-1) if t=='power_log_radio' else r.randint(2,4)
  elif k=='k' and t not in ('power_exp_radio','base_log_negative_left_blank'):p[k]=r.choice([1,2,3])
 if 'm' in p:p['m']=r.randint(1,p['n']-1)
 return p

def build(t,p):
 """Parameterized source masks. Every bank recipe computes a whole displayed value."""
 b=p.get('b',3);c=p.get('c',1);n=p.get('n',2);k=p.get('k',1)
 bank=[];rows=[];prime='′';two=False
 if t=='log_log_radio':
  u=c*s.log(X)/s.log(b);v=s.log(X);U=str(c)+r'\log_{'+str(b)+'} x';V=r'\ln x'
  A=c*s.log(X)/(X*s.log(b));B=c*s.log(X)/(X*s.log(b))
  # Source expressions intentionally retain two equal correct summands, not merged.
  L=r'\log_{'+str(b)+'} x';lb=r'\ln '+str(b)
  bank=[(r'\frac{'+str(c)+L+r'}{x} + \frac{'+str(c)+r'\ln x}{x}',A+c*s.log(X)/X,'omit_base_scale'),
   (r'\frac{'+str(c)+r'}{x} + \frac{'+str(c)+r'\ln x}{x'+lb+'}',c/X+B,'drop_log_first'),
   (r'\frac{'+str(c)+L+r'}{x} + \frac{\ln x}{x'+lb+'}',A+B/c,'drop_coefficient_second'),
   (r'\frac{'+str(c)+L+r'}{x} + \frac{'+str(c)+r'\ln x}{x'+lb+'}',A+B,'correct'),
   (r'\frac{'+str(c)+L+r'}{x} + \frac{'+str(c)+r'}{x'+lb+'}',A+c/(X*s.log(b)),'drop_log_second')]
  pr='Given that $f(x) = '+U+V+'$, find $f^{′}(x)$.'
 elif t=='power_log_radio':
  u=X**n;v=s.log(X)/s.log(b);U='x^{'+str(n)+'}';V=r'\log_{'+str(b)+'} x'
  NP=str(n)+'x^{'+str(n-1)+'}';lb=r'\ln '+str(b)
  bank=[(NP+V+' + '+U+r' \cdot \frac{1}{x}',s.diff(u,X)*v+u/X,'omit_base_scale'),
   (NP+r' \cdot \frac{1}{x'+lb+'}',s.diff(u,X)/(X*s.log(b)),'multiply_derivatives'),
   (U+'('+str(-n)+V+r' - \frac{1}{'+lb+'})',u*(-n*v-1/s.log(b)),'negate_and_wrong_power'),
   (NP+r' + \frac{1}{x'+lb+'}',s.diff(u,X)+1/(X*s.log(b)),'sum_derivatives'),
   ('x^{'+str(n-1)+'}('+str(n)+V+r' + \frac{1}{'+lb+'})',X**(n-1)*(n*v+1/s.log(b)),'correct')]
  pr='Given that $f(x) = '+U+V+'$, find $f^{′}(x)$.'
 elif t=='linear_base_radio':
  u=X;v=b**X;U='x';V=base(b);ln=r'\operatorname{ln}⁡'+str(b)
  bank=[(ln+r'\cdot '+V,s.log(b)*v,'omit_x_and_first'),('(1+'+ln+')'+V,(1+s.log(b))*v,'omit_x'),('(1+x'+ln+')'+V,(1+X*s.log(b))*v,'correct'),(V,v,'omit_second'),('(x'+ln+')'+V,X*s.log(b)*v,'omit_first')]
  pr=prompt(U+r'\cdot '+V)
  rows=['(x)^{′}\\cdot '+V+'+x\\cdot ('+V+')^{′}',V+'+(x)('+ln+r'\cdot '+V+')',V+'+x'+ln+r'\cdot '+V,bank[2][0]]
 elif t.startswith('power_exp'):
  u=c*X**n;v=s.exp(k*X);U=poly(c,n);V=exp(k);D=poly(c*n,n-1);DV=coeff(k,V)
  if t=='power_exp_radio':
   factor=xp(n-1);bank=[(coeff(c,'(x+'+str(n)+')'+factor+V),c*(X+n)*X**(n-1)*v,'correct'),(str(c*n)+xp(n)+V,c*n*X**n*v,'power_not_decreased'),(coeff(c,factor+'('+str(n)+V+'+x)'),c*X**(n-1)*(n*v+X),'omit_exp_second'),(coeff(c,'(x+'+str(n-1)+')'+factor+V),c*(X+n-1)*X**(n-1)*v,'wrong_power_coefficient'),(coeff(c,factor+'(x'+V+'+'+str(n)+')'),c*X**(n-1)*(X*v+n),'omit_exp_first')]
  if t=='power_exp_right_blank' and k!=1:prime="'"
  pr=prompt(U+V,prime)
  rows=['('+U+')^{'+prime+'}'+V+'+'+U+'('+V+')^{'+prime+'}', '('+D+')('+V+')+('+U+')('+DV+')',D+V+'+'+coeff(k*c,xp(n))+V]
  if t=='power_exp_radio':rows.append(bank[0][0])
  if t.endswith('blank'):
   answer=s.diff(u,X)*v if 'left' in t else u*s.diff(v,X)
   answer_tex=D+V if 'left' in t else coeff(c*k,xp(n))+V
   pr=blank_prompt(pr,right=U+DV) if 'left' in t else blank_prompt(pr,left=D+V)
   bank=[(answer_tex,answer,'fragment')]
 elif t in ('base_sin_left_blank','base_tan_right_blank'):
  u=b**X;v=s.sin(X) if 'sin' in t else s.tan(X);U=base(b)
  if 'sin' in t:
   V=op('sin','x');D=U+op('ln',b);DV=op('cos','x');prime="'"
   rows=['{('+U+')}^{\'}'+V+'+'+U+'{('+V+')}^{\'}','('+D+')'+V+'+'+U+'('+DV+')',D+V+'+'+U+DV]
   pr=blank_prompt(prompt(U+V,prime),right=U+DV);bank=[(D+V,s.diff(u,X)*v,'fragment')]
  else:
   V='tan⁡(x)';D=U+'ln⁡('+str(b)+')';DV='{sec}^{2}⁡(x)'
   rows=['{('+U+')}^{′}'+V+'+'+U+'{('+V+')}^{′}','('+D+')'+V+'+'+U+'('+DV+')',D+V+'+'+U+DV]
   pr=blank_prompt(prompt(U+V),left=D+V);bank=[(U+'{sec}^{2}(x)',u*s.diff(v,X),'fragment')]
 elif t=='cos_log_radio':
  u=s.cos(X);v=s.log(X)/s.log(b);U='cos⁡x';V='log⁡x' if b==10 else 'log_{'+str(b)+'}⁡x';ln='ln⁡'+str(b);sin='sin⁡x'
  bank=[(r'\frac{cos⁡x}{'+ln+'}-'+sin+V,u/s.log(b)-s.sin(X)*v,'omit_x'),(r'\frac{cos⁡x}{x}-'+sin+V,u/X-s.sin(X)*v,'omit_base_scale'),(r'\frac{cos⁡x}{x'+ln+'}+'+sin+V,u/(X*s.log(b))+s.sin(X)*v,'wrong_trig_sign'),(r'\frac{cos⁡x}{x'+ln+'}-'+sin+V,u/(X*s.log(b))-s.sin(X)*v,'correct'),(r'\frac{cos⁡x}{x}-'+sin,u/X-s.sin(X),'drop_log_and_base_scale')]
  pr=prompt(U+V);rows=['{('+U+')}^{′}'+V+'+'+U+'{('+V+')}^{′}','(-'+sin+')('+V+')+('+U+')(\\frac{1}{x'+ln+'})',bank[3][0]]
 elif t.startswith('base_log'):
  d=p['d'];u=b**(k*X);v=s.log(X)/s.log(d);U=base(b,k);V=logbase(d);two=True
  neg=k<0
  Ln=('ln⁡' if neg else r'\operatorname{ln}⁡')+'('+str(b)+')';Ld=('ln⁡' if neg else r'\operatorname{ln}⁡')+'('+str(d)+')'
  D=coeff(k,U+Ln);DV=r'\frac{1}{x'+Ld+'}';A=D+V;B=r'\frac{'+U+'}{x'+Ld+'}'
  rows=['{u}^{′}(x)\\cdot v(x)+u(x)\\cdot {v}^{′}(x)','{('+U+')}^{′}'+V+'+'+U+'{('+V+')}^{′}','('+D+')('+V+')+('+U+')('+DV+')',A+'+'+B]
  pr=blank_prompt(prompt(U+V),left=A) if 'right' in t else blank_prompt(prompt(U+V),right=B)
  val=u*s.diff(v,X) if 'right' in t else s.diff(u,X)*v
  bank=[((r'\frac{'+U+'}{x'+op('ln',d)+'}') if 'right' in t else coeff(k,U+op('ln',b)+'{log}_{'+str(d)+'}(x)'),val,'fragment')]
 else:
  # Authored moderate: two nonzero monomials. Hard: same product, three terms.
  u=p['a']*X**p['n']+p['c']*X**p['m']+(p.get('h',0));v=s.exp(X) if '_exp_' in t else s.log(X)/s.log(b)
  U='\\left('+tex(u)+'\\right)';V=exp() if '_exp_' in t else r'\log_{'+str(b)+'} x';D='\\left('+tex(s.diff(u,X))+'\\right)';DV=exp() if '_exp_' in t else r'\frac{1}{x\ln '+str(b)+'}'
  terms=[]
  for co,power in [(p['a']*p['n'],p['n']-1),(p['c']*p['m'],p['m']-1)]:terms.append(poly(co,power)+V)
  for co,power in [(p['a'],p['n']),(p['c'],p['m'])]+([(p['h'],0)] if 'h' in p else []):
   if '_exp_' in t:terms.append(poly(co,power)+V)
   else:
    numerator=poly(abs(co),power)
    denominator=r'x\ln '+str(b)
    terms.append(('-' if co<0 else '')+r'\frac{'+numerator+'}{'+denominator+'}')
  distributed=''.join(('+' if i and not z.startswith('-') else '')+z for i,z in enumerate(terms))
  rows=['{u}^{′}(x)\\cdot v(x)+u(x)\\cdot {v}^{′}(x)','('+U+')^{′}'+V+'+'+U+'('+V+')^{′}',D+V+'+'+U+DV,distributed]
  pr=prompt(U+V)+'\n\n${f}^{′}(x)=$\n{{field-1}}';bank=[(rows[-1],s.diff(u*v,X),'full_derivative')]
 # Missing-source solutions: authored, preserve common formal/component stages.
 if not rows:
  rows=['{u}^{′}(x)\\cdot v(x)+u(x)\\cdot {v}^{′}(x)','('+U+')^{′}'+V+'+'+U+'('+V+')^{′}','('+tex(s.diff(u,X))+')('+V+')+('+U+')('+tex(s.diff(v,X))+')',next(vv for vv,e,label in bank if label=='correct')]
 return pr,opening(U,V,two)+aligned(rows,prime),bank,u,v,rows

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('unknown difficulty')
 r=random.Random(seed)
 eligible=[t for t,(l,f,_) in TEMPLATES.items() if l==level and (field_type is None or f==field_type.removeprefix(':answer-field.type/')) and (profile is None or profile==PROFILES.get(t) or profile=='observed')]
 if template is None:
  if not eligible:raise ValueError('no eligible template/profile')
  template=r.choice(eligible)
 if template not in TEMPLATES or TEMPLATES[template][0]!=level:raise ValueError('template not in requested level')
 ft=TEMPLATES[template][1]
 if field_type and field_type.removeprefix(':answer-field.type/')!=ft:raise ValueError('field type mismatch')
 if profile not in (None,'observed',PROFILES.get(template)):raise ValueError('unsupported bank profile')
 for attempt in range(100):
  p=dict(parameters) if parameters is not None else sample(template,r);bounds(template,p)
  pr,sol,bank,u,v,rows=build(template,p)
  valid=all(s.simplify(a[1]-b[1])!=0 for i,a in enumerate(bank) for b in bank[i+1:])
  if valid:break
  if parameters is not None:raise ValueError('complete bank ambiguous at these parameters')
 else:raise ValueError('no eligible unambiguous instance')
 correct=next((i for i,(_,e,k) in enumerate(bank) if k in ('correct','fragment','full_derivative')),None)
 assert correct is not None
 identity={'version':VERSION,'prompt':pr,'solution':sol,'field_type':ft,'bank':sorted(vv for vv,e,k in bank)}
 qid=ident(identity);fid=ident([qid,'field']);answers=[{':answer/id':ident([fid,vv]),':answer/type':':answer.type/math',':answer/value':vv} for vv,e,k in bank]
 aid=answers[correct][':answer/id'];r.shuffle(answers)
 key='selection' if ft=='radio' else 'field-1'
 q={':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':pr,':question/worked-solution':sol,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+ft,':answer-field/choices':answers,':answer-field/correct':[':answer/id',aid]}]}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'template':template,'profile':PROFILES.get(template),'parameters':p,'source':SOURCE,'source_ids':list(TEMPLATES[template][2]),'authored':not bool(TEMPLATES[template][2]),'domain':'x > 0' if v.has(s.log(X)) or u.has(s.log(X)) or template=='power_log_radio' else ('cos(x) != 0' if v==s.tan(X) else 'x real'),'mathematical_fingerprint':task_fingerprint(u*v),'content_fingerprint':digest(identity),'recipes':[k for vv,e,k in bank],'sympy':s.__version__}}
# Easy: observed atomic factors and original fragment/full radio layouts.
def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
# Moderate: authored two nonzero polynomial terms, a single unchanged exp/log factor.
def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)
# Hard: authored three nonzero polynomial terms, the same product-rule operation.
def generate_hard(seed=0,**kw):return generate('hard',seed,**kw)
def markdown(rec):
 q=rec['question'];f=q[':question/answer-fields'][0]
 return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$' for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');a=ap.parse_args()
 records=[generate(l,a.seed+i,template=a.template,profile=a.profile) for l in (['easy','moderate','hard'] if a.difficulty=='all' else [a.difficulty]) for i in range(a.count)]
 print(json.dumps(records,ensure_ascii=False,indent=2) if a.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
