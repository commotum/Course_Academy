#!/usr/bin/env python3
"""Seeded product-rule questions. Only source-supported easy practice is served.

Complete source banks and original masks are available through generate(replay=True).
Default radio banks check derivative coefficients without unique visual structures;
blank targets vary independently of factors. No filesystem or database writes.
"""
from __future__ import annotations
import argparse, hashlib, json, random, uuid, re
from math_format import normalize_tex, normalize_prose, checked_math_content, MATH
from functools import lru_cache
import sympy as s
X=s.Symbol('x',positive=True)
KP_ID=17592186096618
KP_UUID='f15a60dd-f6a7-577d-bdbc-148032de94c8'
TITLE='Differentiating a Product Containing an Exponential or Logarithmic Function'
VERSION='product-exp-log-2'
SOURCE={'database':'math','basis':3950,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}
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
 'tan_log_blank':('easy','blank',('q-320820',)),
 'polynomial_log_blank':('easy','blank',('q-320824',)),
 'base_cos_left_blank':('easy','blank',('q-311231',)),
 'sqrt_exp_radio':('easy','radio',('q-47954',)),
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
 expected=set(defaults(t))
 if set(p)!=expected:raise ValueError('parameter keys must match '+str(expected))
 if any(isinstance(v,bool) or not isinstance(v,int) for v in p.values()):raise ValueError('integer parameters required')
 for key,value in p.items():
  allowed = range(2,11) if key in ('b','d') else range(1,7) if key=='c' else range(0,6) if key=='h' else range(-4,0) if key=='n' and t=='power_log_radio' else range(2,5) if key=='n' else (-1,1) if key=='k' and t.startswith('base_log') else (1,) if key=='k' and t=='power_exp_radio' else (1,2,3)
  if value not in allowed:raise ValueError('out-of-bounds '+key)
 if t=='log_log_radio' and p['c']==1:raise ValueError('coefficient 1 collapses the observed bank')

def defaults(t):
 return {
 'log_log_radio':{'c':5,'b':3},'power_log_radio':{'n':-3,'b':2},
 'base_sin_left_blank':{'b':5},'power_exp_right_blank':{'c':1,'n':2,'k':2},
 'linear_base_radio':{'b':3,'c':1},'power_exp_radio':{'c':1,'n':2,'k':1},'cos_log_radio':{'b':10,'c':1},
 'base_tan_right_blank':{'b':4},'power_exp_left_blank':{'c':1,'n':3,'k':1},
 'base_log_left_blank':{'b':3,'d':3,'k':1},'base_log_right_blank':{'b':4,'d':4,'k':1},
 'base_log_negative_left_blank':{'b':5,'d':7,'k':-1},
 'tan_log_blank':{},'polynomial_log_blank':{'n':2,'h':3},
 'base_cos_left_blank':{'b':3},'sqrt_exp_radio':{'c':1,'k':1},
 }[t].copy()
def sample(t,r):
 p=defaults(t)
 for key in p:
  if key in ('b','d'):p[key]=r.randint(2,10)
  elif key=='c':p[key]=r.randint(2 if t=='log_log_radio' else 1,6)
  elif key=='h':p[key]=r.randint(0,5)
  elif key=='n':p[key]=r.randint(-4,-1) if t=='power_log_radio' else r.randint(2,4)
  elif key=='k':p[key]=r.choice([-1,1]) if t.startswith('base_log') else 1 if t=='power_exp_radio' else r.randint(1,3)
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
  u=c*X;v=b**X;U=poly(c,1);V=base(b);ln=r'\operatorname{ln}⁡'+str(b)
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
 elif t in ('base_sin_left_blank','base_tan_right_blank','base_cos_left_blank'):
  u=b**X;v=s.sin(X) if 'sin' in t else s.cos(X) if 'cos' in t else s.tan(X);U=base(b)
  if 'sin' in t:
   V=op('sin','x');D=U+op('ln',b);DV=op('cos','x');prime="'"
   rows=['{('+U+')}^{\'}'+V+'+'+U+'{('+V+')}^{\'}','('+D+')'+V+'+'+U+'('+DV+')',D+V+'+'+U+DV]
   pr=blank_prompt(prompt(U+V,prime),right=U+DV);bank=[(D+V,s.diff(u,X)*v,'fragment')]
  elif 'cos' in t:
   V=r'\cos(x)';D=U+op('ln',b);DV=r'-\sin(x)'
   rows=['('+U+')^{′}'+V+'+'+U+'('+V+')^{′}','('+D+')'+V+'+'+U+'('+DV+')',D+V+'-'+U+r'\sin(x)']
   pr=prompt(U+V)+'\n\n${f}^{′}(x)=$\n{{field-1}} $-\\,'+U+r'\sin(x)$';bank=[(D+V,s.diff(u,X)*v,'fragment')]
  else:
   V='tan⁡(x)';D=U+'ln⁡('+str(b)+')';DV='{sec}^{2}⁡(x)'
   rows=['{('+U+')}^{′}'+V+'+'+U+'{('+V+')}^{′}','('+D+')'+V+'+'+U+'('+DV+')',D+V+'+'+U+DV]
   pr=blank_prompt(prompt(U+V),left=D+V);bank=[(U+'{sec}^{2}(x)',u*s.diff(v,X),'fragment')]
 elif t=='cos_log_radio':
  u=c*s.cos(X);v=s.log(X)/s.log(b);U=coeff(c,'cos⁡x');V='log⁡x' if b==10 else 'log_{'+str(b)+'}⁡x';ln='ln⁡'+str(b);sin='sin⁡x'
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
 elif t=='tan_log_blank':
  u=s.tan(X);v=s.log(X)/s.log(10);U=r'\tan(x)';V=r'\log(x)'
  A=r'\sec^{2}(x)\log(x)';B=r'\frac{\tan(x)}{x\ln(10)}'
  rows=['('+U+')^{′}'+V+'+'+U+'('+V+')^{′}',r'(\sec^{2}(x))('+V+')+('+U+r')(\frac{1}{x\ln(10)})',A+'+'+B]
  pr=blank_prompt(prompt(U+V)+'\n\n**Hint:** $\\log(x)=\\log_{10}(x)$',right=B)
  bank=[(A,s.diff(u,X)*v,'fragment')]
 elif t=='polynomial_log_blank':
  u=X**n+p['h'];v=s.log(X)
  U='('+xp(n)+'+'+str(p['h'])+')' if p['h'] else xp(n)
  V=r'\ln(x)'
  A=poly(n,n-1)+V;B=r'\frac{'+xp(n)+'+'+str(p['h'])+'}{x}' if p['h'] else xp(n-1)
  rows=['('+U+')^{′}'+V+'+'+U+'('+V+')^{′}','('+poly(n,n-1)+')('+V+')+'+U+r'(\frac{1}{x})',A+'+'+B]
  pr=blank_prompt(prompt(U+V),left=A);bank=[(B,u/X,'fragment')]
 elif t=='sqrt_exp_radio':
  u=c*s.sqrt(X);v=s.exp(k*X);U=coeff(c,r'\sqrt{x}');V=exp(k)
  E=s.exp(k*X);R=s.sqrt(X)
  bank=[('1+'+r'\frac{'+V+r'}{2\sqrt{x}}',1+E/(2*R),'observed_compound_1'),
   ('x+'+r'\frac{2'+V+r'}{\sqrt{x}}',X+2*E/R,'observed_compound_2'),
   (r'\frac{1+2'+V+r'}{2\sqrt{x}}',(1+2*E)/(2*R),'observed_compound_3'),
   (r'\frac{'+V+'+2x'+V+r'}{2\sqrt{x}}',(E+2*X*E)/(2*R),'correct'),
   (r'\frac{'+V+'+x'+V+r'}{\sqrt{x}}',(E+X*E)/R,'observed_compound_4')]
  pr=prompt(U+V)
  rows=['('+U+')^{′}'+V+'+'+U+'('+V+')^{′}',r'\frac{1}{2\sqrt{x}}'+V+r'+\sqrt{x}'+V,bank[3][0]]
 else:raise ValueError('unknown template')
 # Missing-source solutions: authored, preserve common formal/component stages.
 if not rows:
  rows=['{u}^{′}(x)\\cdot v(x)+u(x)\\cdot {v}^{′}(x)','('+U+')^{′}'+V+'+'+U+'('+V+')^{′}','('+tex(s.diff(u,X))+')('+V+')+('+U+')('+tex(s.diff(v,X))+')',next(vv for vv,e,label in bank if label=='correct')]
 return pr,opening(U,V,two)+aligned(rows,prime),bank,u,v,rows


def clean_tex(value):
 value=re.sub(r'\\operatorname\{(sin|cos|tan|sec|ln|log)\}',r'\\\1 ',value)
 value=re.sub(r'\{(log|sec)\}',r'\\\1 ',value)
 value=value.replace('\u2061',' ')
 # This operates only inside math, never on prose words.
 value=re.sub(r'(?<!\\)(sin|cos|tan|sec|ln|log)',r'\\\1 ',value)
 return value

def clean(value):
 return MATH.sub(lambda m:clean_tex(m[0]),value) if '$' in value else clean_tex(value)

def derivative(e):
 if e==s.tan(X):return s.sec(X)**2
 return s.diff(e,X)


def coefficient_bank(t,p,u,v,r,decision=None):
 """Whole-product banks: neither contribution alone identifies the key."""
 c=p.get('c',1);n=p.get('n',2);k=p.get('k',1);b=p.get('b',3)
 if t=='log_log_radio':
  truth=2*c;rank=decision[1];window=list(range(truth-rank,truth-rank+5));unit=s.log(X)/(X*s.log(b))
  bank=[(r'\left('+str(a)+r'\right)\left('+tex(unit)+r'\right)',a*unit,'correct' if a==truth else 'total_coefficient_error') for a in window]
  return bank,{'tested_role':'total','true_coefficient':truth,'coefficient_rank':rank,'window':window}
 if t=='power_log_radio':a=n;bb=1;L=X**(n-1)*v;R=X**(n-1)/s.log(b);stepA=1;stepB=1
 elif t=='linear_base_radio':a=c;bb=c;L=v;R=X*s.log(b)*v;stepA=1;stepB=1
 elif t=='power_exp_radio':a=c*n;bb=c;L=X**(n-1)*v;R=X**n*v;stepA=n;stepB=1
 elif t=='cos_log_radio':a=-c;bb=c;L=s.sin(X)*v;R=s.cos(X)/(X*s.log(b));stepA=-1;stepB=1
 elif t=='sqrt_exp_radio':a=c;bb=c*k;L=v/(2*s.sqrt(X));R=s.sqrt(X)*v;stepA=1;stepB=k
 else:raise ValueError(t)
 direction=1 if decision[0]=='left' else -1
 da=direction*stepA;db=direction*stepB
 far=2 if decision[1]%2 else -1
 extra_a=a if decision[2]==0 else a+da
 pairs=[(a,bb),(a+da,bb),(a,bb+db),(a+da,bb+db),(extra_a,bb+far*db)]
 def form(aa,bbb):return r'\left('+str(aa)+r'\right)\left('+tex(L)+r'\right)+\left('+str(bbb)+r'\right)\left('+tex(R)+r'\right)'
 bank=[(form(aa,bbb),aa*L+bbb*R,'correct' if (aa,bbb)==(a,bb) else 'left_coefficient_error' if bbb==bb else 'right_coefficient_error' if aa==a else 'both_coefficients_error') for aa,bbb in pairs]
 return bank,{'tested_role':'both','true_coefficients':[a,bb],'coefficient_pairs':[list(pair) for pair in pairs],'coefficient_rank':sorted(pairs).index((a,bb)),'error_direction':direction,'far_error_multiplier':far,'extra_row':decision[2]}


def remask(pr,u,v,target):
 A=derivative(u)*v;B=u*derivative(v)
 prefix=pr.split('\n\n${f}')[0]
 # Source prompt may use an ASCII prime; split by derivative line rather than copying its old mask.
 prefix=prefix.split('\n\n$f')[0]
 if '\n\n' in pr and 'Hint:' not in pr:prefix=pr.split('\n\n')[0]
 negative= B.could_extract_minus_sign()
 if target=='left':
  tail=' $-\\,'+tex(-B)+'$' if negative else ' $+\\,'+tex(B)+'$'
  prompt_text=prefix+'\n\n$f^{\\prime}(x)=$\n{{field-1}}'+tail
  answer=A
 else:
  prompt_text=prefix+'\n\n$f^{\\prime}(x)='+tex(A)+('\\,-$' if negative else '\\,+$')+'\n{{field-1}}'
  answer=-B if negative else B
 return prompt_text,[(tex(answer),answer,'fragment')]

@checked_math_content
def generate(level='easy',seed=0,template=None,parameters=None,profile=None,target=None,replay=False):
 if level!='easy':raise ValueError('only source-justified easy difficulty is supported')
 r=random.Random(seed)
 if template is None:template=r.choice(list(TEMPLATES))
 if template not in TEMPLATES:raise ValueError('unknown template')
 ft=TEMPLATES[template][1]
 if target not in (None,'left','right') or (target is not None and ft!='blank'):raise ValueError('invalid target')
 if profile not in (None,'observed','coefficient_check'):raise ValueError('unknown profile')
 if profile=='observed' and not replay:raise ValueError('observed banks are available only with replay=True')
 if replay and parameters is None:parameters=defaults(template)
 # Select decision roles/sign cases before incidental base and coefficient values.
 if ft=='blank' and target is None and not replay:target=r.choice(['left','right'])
 decision=(r.choice(['left','right']),r.randrange(5),r.randrange(2)) if ft=='radio' else None
 sign=r.choice([-1,1]) if template.startswith('base_log') and parameters is None else None
 p=dict(parameters) if parameters is not None else sample(template,r)
 if sign is not None:p['k']=sign
 bounds(template,p)
 pr,sol,bank,u,v,rows=build(template,p)
 details={};used_profile='observed' if replay or profile=='observed' else 'coefficient_check' if ft=='radio' else 'fragment'
 if ft=='radio' and used_profile=='coefficient_check':
  bank,details=coefficient_bank(template,p,u,v,r,decision)
  # All rows derive from the exact factors; original source layouts are retained by replay.
  if (template in ('linear_base_radio','cos_log_radio') and p.get('c',1)!=1) or template=='sqrt_exp_radio':
   sol=opening(tex(u),tex(v))+aligned(['('+tex(u)+')^{′}('+tex(v)+')+('+tex(u)+')('+tex(v)+')^{′}', '('+tex(s.diff(u,X))+')('+tex(v)+')+('+tex(u)+')('+tex(s.diff(v,X))+')',tex(s.diff(u*v,X))])
 elif ft=='radio' and template in ('linear_base_radio','cos_log_radio','sqrt_exp_radio') and p!=defaults(template):
  raise ValueError('observed profile requires source parameters for this bank')
 if ft=='blank' and target is not None:pr,bank=remask(pr,u,v,target)
 # Retain both mathematically valid captured alias values in exact replay.
 if replay and template=='power_exp_left_blank' and p==defaults(template):bank.append(('3x^2e^{x}',bank[0][1],'alias'))
 if replay and template=='base_log_negative_left_blank' and p==defaults(template):bank.append((r'-5^{-x}\ln5\left(\log_7x\right)',bank[0][1],'alias'))
 if ft=='radio' and any(s.simplify(a[1]-bb[1])==0 for i,a in enumerate(bank) for bb in bank[i+1:]):raise ValueError('ambiguous complete bank')
 if ft=='blank' and target is None:
  target='right' if template in ('power_exp_right_blank','base_tan_right_blank','base_log_right_blank','polynomial_log_blank') else 'left'
 pr=normalize_prose(clean(pr));sol=normalize_prose(clean(sol));bank=[(normalize_tex(clean(z)),e,key) for z,e,key in bank]
 identity={'version':VERSION,'prompt':pr,'solution':sol,'field_type':ft,'bank':sorted(z for z,e,key in bank)}
 qid=ident(identity);fid=ident([qid,'field'])
 answers=[{':answer/id':ident([fid,z]),':answer/type':':answer.type/math',':answer/value':z} for z,e,key in bank]
 correct=next(i for i,(z,e,key) in enumerate(bank) if key in ('correct','fragment'))
 aid=answers[correct][':answer/id'];r.shuffle(answers)
 q={':question/id':qid,':question/difficulty':':question.difficulty/easy',':question/problem':pr,':question/worked-solution':sol,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection' if ft=='radio' else 'field-1',':answer-field/type':':answer-field.type/'+ft,':answer-field/choices':answers,':answer-field/correct':[':answer/id',aid]}]}
 if replay and template in ('log_log_radio','power_log_radio'):q.pop(':question/difficulty')
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'template':template,'profile':used_profile,'parameters':p,'target':target,'source':SOURCE,'source_ids':list(TEMPLATES[template][2]),'source_difficulty':'unclassified' if template in ('log_log_radio','power_log_radio') else 'easy','domain':'x > 0 and cos(x) != 0' if template=='tan_log_blank' else 'cos(x) != 0' if template=='base_tan_right_blank' else 'x > 0' if u.has(s.log(X)) or v.has(s.log(X)) or template in ('power_log_radio','sqrt_exp_radio') else 'x real','mathematical_fingerprint':task_fingerprint(u*v),'content_fingerprint':digest(identity),'recipes':[key for z,e,key in bank],'rejections':0,**details}}

def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)

def markdown(rec):
 q=rec['question'];f=q[':question/answer-fields'][0]
 return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$' for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']

if __name__=='__main__':
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--difficulty',choices=['easy','moderate','hard'],default='easy');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='json');ap.add_argument('--template');ap.add_argument('--profile',choices=['coefficient_check','observed']);a=ap.parse_args()
 if a.count<0:ap.error('count must be nonnegative')
 if a.difficulty!='easy':ap.error('unsupported difficulty: only easy has source evidence')
 records=[generate(a.difficulty,a.seed+i,template=a.template,profile=a.profile) for i in range(a.count)]
 print(json.dumps(records,ensure_ascii=False,indent=2) if a.format=='json' else '\n\n---\n\n'.join(markdown(rec) for rec in records))
