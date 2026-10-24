#!/usr/bin/env python3
"""Constant times e^x plus a polynomial, math basis 1356, steps 3–7 only.

Observed families preserve the full radio bank, blank fragments, solution prose,
and ordered mathematical stages. Explicit observed profiles retain uncertain
scalar patterns and legacy extra blank bank values; default profiles use
method-derived errors. Contextual source prompts are reproduced in observed
profiles and made standalone in normal presentation. Hard is an authored bounded
extension of the canonical two-power polynomial, never chain/product rules.
Evidence, precise ranges, source corrections, and grading tests are in the same-ID
folder. Sampling uses exact SymPy math and rejects a whole collided bank.
"""
from __future__ import annotations

# Standalone source eligibility: immutable policy ledger, seeded CLI guard.
import sys as _ca_sys, os as _ca_os
from pathlib import Path as _ca_Path
_ca_sys.path.insert(0,str(_ca_Path(__file__).resolve().parent))
if __name__ == "__main__" and not _ca_os.environ.get("_CA_SOURCE_POLICY_CHILD"):
    from ca_source_runtime import cli as _ca_source_cli
    _ca_source_cli(__file__,_ca_Path(__file__).with_name('17592186096611-source-policy.json'))
    raise SystemExit(0)

import argparse, hashlib, json, random, re, uuid
from pathlib import Path
import sympy as sp

KP_ID=17592186096611
KP_UUID='8b7d0153-6e0a-5e19-83f1-960811dc5205'
TITLE='Differentiating the Product of a Constant and the Exponential Function, Plus a Polynomial'
VERSION='exp-polynomial-1'
HERE=Path(__file__).with_suffix('')
SOURCE=json.loads((HERE/'source.json').read_text())
QS={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
x=sp.Symbol('x', real=True)
D=r'\frac{\text{d}}{\text{d}x}'

# Easy: one power/linear reduction, or two-power slope at a familiar input.
# Each observed shape is a parallel family; original degree-seven at -1 stays easy.
# Moderate: quadratic plus linear plus constant; branch context is supplied.
# Hard: authored canonical two higher powers, both exponents reduced (n>m>=2).
TEMPLATES={
 'direct_quadratic':('easy','radio','q-11728'),
 'difference':('easy','blank','q-167636'),
 'slope_quad':('easy','radio','q-140431'),
 'slope_polyfirst':('easy','radio','q-140432'),
 'slope_zero':('easy','radio','q-17247'),
 'slope_seventh':('easy','blank','q-304035'),
 'direct_extended':('moderate','radio','q-11730'),
 'branch':('moderate','blank','q-167694'),
 'slope_extended':('moderate','radio','q-17255'),
 'two_powers':('hard','blank',None),
}
ORIGINAL={
 'direct_quadratic':dict(a=5,b=2,d=-3,name='f'),
 'difference':dict(A=2,B=3,name='k'),
 'slope_quad':dict(a=2,b=4,d=-3,t=1,name='f'),
 'slope_polyfirst':dict(a=6,b=1,c=2,t=0,name='f'),
 'slope_zero':dict(a=2,b=-3,t=0,name='f'),
 'slope_seventh':dict(a=2,b=6,n=7,t=-1,name='f'),
 'direct_extended':dict(a=9,b=-9,c=11,d=-20,name='f'),
 'branch':dict(a=1,b=1,c=1,h=1,name='f'),
 'slope_extended':dict(a=11,b=8,c=-12,d=-20,t=0,name='f'),
}

def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(v):return str(uuid.uuid5(uuid.NAMESPACE_URL,'exp-polynomial:'+digest(v)))
def latex(v):
 return sp.latex(sp.sympify(v)).replace('e^{x}',r'{e}^{x}')
def power(n):return 'x' if n==1 else (str(1) if n==0 else '{x}^{'+str(n)+'}')
def term(c,base):
 c=sp.sympify(c)
 if c==0:return '0'
 if not base:return latex(c)
 return ('-' if c<0 else '')+('' if abs(c)==1 else latex(abs(c)))+base

def joined(parts):
 out=''
 for c,base in parts:
  if c==0:continue
  v=term(c,base)
  out+=('+' if out and not v.startswith('-') else '')+v
 return out or '0'
def deriv(s):return D+'('+s+')'
def grouped(v):return '('+str(v)+')' if v<0 else str(v)
def shape(template,p):
 a=p.get('a',p.get('B')); n=p.get('n',2)
 if template=='difference':return p['B'],[(-1,3),(-p['A'],1)],False
 terms=[(p['b'],n)]
 if 'c' in p:terms.append((p['c'],p.get('m',1)))
 if 'd' in p:terms.append((p['d'],0))
 return a,terms,template in ('slope_polyfirst','slope_seventh')
def parts(template,p):
 a,terms,polyfirst=shape(template,p)
 ep=(a,r'{e}^{x}')
 pp=[(c,'' if n==0 else power(n)) for c,n in terms]
 return pp+[ep] if polyfirst else [ep]+pp

def func(template,p):return joined(parts(template,p))
def derivative_parts(template,p):
 a,terms,pf=shape(template,p)
 ep=(a,r'{e}^{x}')
 pp=[(c*n,'' if n==1 else power(n-1)) for c,n in terms if n]
 return pp+[ep] if pf else [ep]+pp

def expr(template,p):
 a,terms,_=shape(template,p)
 return a*sp.exp(x)+sum(c*x**n for c,n in terms)

def expanded_derivatives(template,p,negative_inside=False):
 out=[]
 for c,base in parts(template,p):
  if negative_inside:out.append((1,deriv(term(c,base))))
  else:out.append((sp.sign(c),deriv(term(abs(c),base))))
 return joined(out)
def factored_derivatives(template,p):
 a,terms,pf=shape(template,p)
 ep=(a,deriv(r'{e}^{x}'))
 pp=[]
 for c,n in terms:
  pp.append((c,deriv(power(n)))) if n else pp.append((sp.sign(c),deriv(str(abs(c)))))
 return joined(pp+[ep] if pf else [ep]+pp)
def evaluated_derivatives(template,p):
 a,terms,pf=shape(template,p)
 ep=(a,r'{e}^{x}')
 pp=[(c,'('+term(n,'' if n==1 else power(n-1))+')') if n else (sp.sign(c),'0') for c,n in terms]
 return joined(pp+[ep] if pf else [ep]+pp)

def slope_stages(template,p):
 a,terms,pf=shape(template,p);t=p['t']
 ds=joined(derivative_parts(template,p))
 base='{('+ds+r')\,|}_{x='+str(t)+'}'
 ev=[(a,r'{e}^{'+str(t)+'}')]
 for c,n in terms:
  if n:
   b=grouped(t)+(('^{'+str(n-1)+'}') if n>2 else '') if n>1 else ''
   ev.append((c*n,(r'\cdot '+b) if b else ''))
 if pf:ev=ev[1:]+ev[:1]
 row2=joined(ev)
 slope=sp.diff(expr(template,p),x).subs(x,t)
 final=latex(slope)
 if template=='slope_quad':return [base,row2,final]
 if template=='slope_polyfirst':return [base,row2,joined([(p['c'],''),(a,r'\cdot 1')]),final]
 if template=='slope_zero':return [base,row2,term(a,r'\cdot 1')+'-0',final]
 if template=='slope_seventh':
  val=p['b']*p['n']*t**(p['n']-1)
  return [base,row2,term(val,r'\cdot 1')+'+'+latex(a/sp.E),final]
 if template=='slope_extended':
  # Source has a distinct explicit e^0 stage, followed by collection.
  return [base,row2,joined([(a,r'\cdot 1'),(1,'0'),(p['c'],'')]),joined([(a,''),(p['c'],'')]),final]
 raise ValueError(template)

def stages(template,p):
 fs=func(template,p);ds=joined(derivative_parts(template,p))
 if template=='difference':
  A,B=p['A'],p['B'];inner=joined([(1,power(3)),(A,'x')])
  pre=[r'g(x)-f(x)',term(B,r'{e}^{x}')+'-('+inner+')',fs]
  return [pre,[deriv(fs),expanded_derivatives(template,p),factored_derivatives(template,p),ds]]
 if template=='branch':return [[deriv(fs),expanded_derivatives(template,p),ds]]
 rs=[deriv(fs),expanded_derivatives(template,p,template=='slope_quad'),factored_derivatives(template,p)]
 if template=='slope_quad':rs[2]=joined([(p['a'],deriv(r'{e}^{x}')),(p['b'],deriv(power(2))),(1,'0')])
 if template in ('slope_zero','slope_extended','slope_seventh','two_powers','direct_quadratic','direct_extended'):
  rs.append(evaluated_derivatives(template,p))
 rs.append(ds)
 return [rs,slope_stages(template,p)] if template.startswith('slope_') else [rs]

def replace_blocks(source,blocks):
 """Replace only complete RHS components in each aligned row; preserve scaffolding."""
 i=0
 def repl(match):
  nonlocal i
  rows=re.split(r'(\\\\)',match.group(1));want=blocks[i];i+=1
  assert len(want)==(len(rows)+1)//2,(i,len(want),rows)
  for j,math in enumerate(want):
   row=rows[2*j]
   prefix=re.match(r'(.*?&\s*=\s*)',row,re.S).group(1)
   suffix=re.search(r'(\.?\s*)$',row).group(1)
   rows[2*j]=prefix+math+suffix
  return r'\begin{aligned}'+''.join(rows)+r'\end{aligned}'
 out=re.sub(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',repl,source,flags=re.S)
 assert i==len(blocks)
 return out

def solution(template,p,observed=False):
 source_id=TEMPLATES[template][2]
 blocks=stages(template,p)
 if source_id and ':question/worked-solution' in QS[source_id]:
  s=QS[source_id][':question/worked-solution']
  if template=='difference':
   s=s.replace('$A=2$','$A='+str(p['A'])+'$').replace('$B=3$','$B='+str(p['B'])+'$')
   if not observed:s=s.replace('We found that '+ '$A='+str(p['A'])+'$ and $B='+str(p['B'])+'$ in steps 3 and 4, respectively. Therefore, we have','Using the given definitions, we have')
  if template=='branch':
   s=s.replace('$x<1,$','$x<'+str(p['h'])+',$').replace('$f(x)={e}^{x}+{x}^{2}+x,$','$'+p['name']+'(x)='+func(template,p)+',$')
  s=replace_blocks(s,blocks)
  if template=='difference' and not observed:s=s.replace(r'\begin{aligned}y &',r'\begin{aligned}k(x) &')
  if template!='difference':s=s.replace('{f}^{′}', '{'+p['name']+'}^{′}').replace(r'\text{d}f',r'\text{d}'+p['name'])
  return s
 label=p['name']+"'(x)"
 rows=blocks[0]
 body=(label+r' & ='+rows[0])+''.join(r' \\ & ='+v for v in rows[1:])+'.'
 return 'Using the addition and the power rules, we get\n\n$$\n'+r'\begin{aligned}'+body+r'\end{aligned}'+'\n$$'

def prompt(template,p,observed=False):
 sid=TEMPLATES[template][2]; name=p['name'];fs=func(template,p)
 if template=='difference':
  if observed:
   return QS[sid][':question/problem'].replace('$A=2$','$A='+str(p['A'])+'$').replace('$B=3,$','$B='+str(p['B'])+',$')
  inner=joined([(1,power(3)),(p['A'],'x')])
  return 'Let $f(x)='+inner+'$ and $g(x)='+term(p['B'],r'{e}^{x}')+'$. If $k(x)=g(x)-f(x)$, then $'+r'\frac{\text{d}k}{\text{d}x}'+'=$ {{field-1}}.'
 if template=='branch':
  if observed:return QS[sid][':question/problem'].replace('$x<1,$','$x<'+str(p['h'])+',$')
  return 'For $x<'+str(p['h'])+'$, let $'+name+'(x)='+fs+'$. Then $'+name+"'(x)=$ {{field-1}}."
 if template in ('direct_quadratic','direct_extended'):
  # Source spacing and f-prime syntax preserved; mathematical TeX is normalized.
  spaced=fs.replace('+',' + ').replace('-',' - ')
  if spaced.startswith(' - '):spaced='-'+spaced[3:]
  return 'Given that $'+name+'(x) = '+spaced+'$, find $'+name+'^{′}(x)$.'
 if template=='two_powers':return 'Given that $'+name+'(x)='+fs+'$, find $'+name+"'(x)=$ {{field-1}}."
 if template=='slope_seventh':return 'Given that $'+name+'(x)='+fs+'$, the exact value of the slope of the tangent line at $x='+str(p['t'])+'$ is{{field-1}}.'
 return 'Given that $'+name+'(x)='+fs+'$, find the slope of the tangent at $x='+str(p['t'])+'.$'

def bank(template,p,profile):
 """Complete bank selected before sampling. No pooled first-valid substitutions."""
 f=expr(template,p);df=sp.diff(f,x);a,terms,_=shape(template,p)
 if template.startswith('slope_'):correct=df.subs(x,p['t'])
 else:correct=df
 b=p.get('b');c=p.get('c');d=p.get('d')
 if TEMPLATES[template][1]=='blank':
  if template=='slope_seventh' and profile.startswith('observed_'):
   return correct,[correct,df],['correct_fragment','legacy_unevaluated_derivative']
  return correct,[correct],['correct_fragment']
 if profile.startswith('observed_'):
  if template=='direct_quadratic':
   vals=[df, a*sp.exp(x)+2*b*x**2+d,a*sp.exp(x)+2*b*x**2,df+d,sp.exp(x)+2*b*x]
   labels=['correct','retain_exponent_constant','retain_exponent','retain_constant','omit_exponential_coefficient']
  elif template=='direct_extended':
   vals=[df, sp.exp(x)+2*b*x+c,a*sp.exp(x)+2*b*x**2+c*x,a*sp.exp(x)+2*b*x**2+c,a*sp.exp(x)+2*b*x**2+c*x+d]
   labels=['correct','omit_exponential_coefficient','retain_both_powers','retain_quadratic_power','retain_powers_constant']
  elif template=='slope_quad':
   t=p['t'];vals=[correct,sp.exp(t)+b*t,sp.exp(t)+2*b*t,a*sp.exp(t),a*sp.exp(t)+b*t]
   labels=['correct','omit_exp_scale_power_factor','omit_exp_scale','omit_polynomial_derivative','omit_power_factor']
  elif template=='slope_polyfirst':
   vals=[correct,(c+a)*sp.E,c+a*sp.E,b+a*sp.E,a*sp.E]
   labels=['correct','multiply_linear_and_exp_by_e','evaluate_exp_at_one','treat_linear_as_quadratic_scale','omit_linear_evaluate_at_one']
  elif template=='slope_zero':
   vals=[correct,a*sp.E+2*b,sp.Integer(1),(a+2*b)*sp.E,sp.Integer(0)]
   labels=['correct','evaluate_at_one','unit_exp_omit_polynomial','merge_coefficients_times_e','omit_exp_evaluate_zero']
  elif template=='slope_extended':
   vals=[correct,sp.Integer(0),a+sp.Rational(c,2),sp.Rational(c,4),-correct]
   labels=['correct','observed_zero','observed_half_linear','observed_quarter_linear','observed_negated_result']
  else:raise ValueError(profile)
 else:
  if template.startswith('direct_'):
   poly=sum(c*x**n for c,n in terms)
   vals=[df, df-a*sp.exp(x),a*sp.exp(x)+sum(co*n*x**n for co,n in terms if n),df-2*sp.diff(poly,x),f]
   labels=['correct','omit_exponential','retain_polynomial','reverse_polynomial_derivative_sign','return_original_function']
  else:
   t=p['t'];poly=sum(co*x**n for co,n in terms)
   vals=[correct,sp.diff(poly,x).subs(x,t),sp.diff(f,x).subs(x,1 if t==0 else 0),f.subs(x,1 if template=='slope_zero' else t),correct-a*sp.exp(t)+sp.exp(t)]
   labels=['correct','omit_exponential_derivative','evaluate_wrong_input','return_function_value','omit_exp_scale']
 return correct,[sp.sympify(v) for v in vals],labels

def validate_parameters(template,p,observed=False):
 required=set(ORIGINAL[template]) if template in ORIGINAL else {'a','b','c','n','m','name'}
 if set(p)!=required:raise ValueError('Expected exact parameter keys '+str(sorted(required)))
 if p['name'] not in ('f','g','h','k'):raise ValueError('Unsupported function name')
 for k,v in p.items():
  if k!='name' and (not isinstance(v,int) or isinstance(v,bool)):raise ValueError('Integer components required')
 if template=='difference':
  if p['name']!='k' or not (1<=p['A']<=9 and 1<=p['B']<=9):raise ValueError('Difference bounds A,B 1..9, name k')
  return
 for k in ('a','b','c','d'):
  if k in p and (p[k]==0 or abs(p[k])>(20 if k=='d' else 12)):raise ValueError('Nonzero signed coefficient bounds')
 if template in ('direct_quadratic','slope_quad','slope_zero','slope_polyfirst','slope_seventh'):
  if any(abs(p[k])>9 for k in ('a','b','c') if k in p):raise ValueError('Easy coefficients max magnitude 9')
 if template=='slope_seventh' and (p['n'] not in (3,5,7) or p['t']!=-1 or p['a']<=0 or p['b']<=0):raise ValueError('Odd degree 3,5,7 at -1; positive scales')
 if template in ('slope_quad','slope_polyfirst','slope_zero','slope_extended') and p['t']!=ORIGINAL[template]['t']:raise ValueError('Source arithmetic input retained')
 if template=='branch' and (not -3<=p['h']<=3):raise ValueError('Branch threshold bound')
 if template=='two_powers':
  if not(3<=p['n']<=7 and 2<=p['m']<=3 and p['n']>p['m']):raise ValueError('Hard two nonconstant power reductions')
  if any(abs(p[k])>7 for k in ('a','b','c')):raise ValueError('Hard coefficient max magnitude 7')
 if observed and p['name']!=ORIGINAL[template]['name']:raise ValueError('Observed layout retains actual function name')

def sample(template,r):
 p=dict(ORIGINAL[template]) if template in ORIGINAL else dict(a=3,b=2,c=-1,n=4,m=2,name='f')
 for k in p:
  if k in ('a','b','c'):p[k]=r.choice([v for v in range(-7,8) if v and (k!='a' or abs(v)>1)])
  elif k=='d':p[k]=r.choice([v for v in range(-20,21) if v])
 if template=='difference':p.update(A=r.randint(1,9),B=r.randint(1,9))
 if template=='branch':p['h']=r.randint(-3,3)
 if template=='slope_seventh':p.update(a=r.randint(2,7),b=r.randint(1,7),n=r.choice([3,5,7]))
 if template=='two_powers':p.update(n=r.randint(4,7),m=r.choice([2,3]))
 if template!='difference':p['name']=r.choice(['f','g','h'])
 return p

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('Unknown difficulty')
 r=random.Random(seed)
 eligible=[k for k,v in TEMPLATES.items() if v[0]==level and (field_type is None or v[1]==field_type)]
 if template is None:
  if profile and profile.startswith('observed_'):template=profile[len('observed_'):]
  else:template=r.choice(eligible) if eligible else None
 if template not in eligible:raise ValueError('Template/field/difficulty mismatch')
 source_id=TEMPLATES[template][2]
 profile=profile or ('fragment' if TEMPLATES[template][1]=='blank' else 'authored_method')
 if profile not in ('fragment','authored_method','observed_'+template):raise ValueError('Unknown bank profile')
 observed=profile.startswith('observed_')
 if observed and source_id is None:raise ValueError('No observed hard bank')
 if TEMPLATES[template][1]=='radio' and profile=='fragment':raise ValueError('Radio needs complete bank')
 if TEMPLATES[template][1]=='blank' and profile=='authored_method':raise ValueError('Blank uses fragment profile')
 for attempt in range(1000):
  p=dict(parameters) if parameters is not None else sample(template,r)
  if observed and parameters is None:p['name']=ORIGINAL[template]['name']
  validate_parameters(template,p,observed)
  correct,vals,labels=bank(template,p,profile)
  collision=any(sp.simplify(vals[i]-vals[j])==0 for i in range(len(vals)) for j in range(i))
  if not collision:break
  if parameters is not None:raise ValueError('Reject whole equivalent/ambiguous bank')
 else:raise ValueError('Unable to sample eligible complete bank')
 kind=TEMPLATES[template][1];key='selection' if kind=='radio' else 'field-1'
 raw=[latex(v) for v in vals]
 if template.startswith('direct_'):raw=[p['name']+'^{′}(x) = '+v for v in raw]
 problem=prompt(template,p,observed);worked=solution(template,p,observed)
 task=digest([sp.srepr(sp.diff(expr(template,p),x)), 'slope' if template.startswith('slope_') else 'derivative',p.get('t')])
 identity=[VERSION,problem,worked,kind,key,sorted(raw),raw[0]]
 qid=uid(identity);fid=uid([qid,key])
 answers=[{':answer/id':uid([fid,v]),':answer/type':':answer.type/math',':answer/value':v} for v in raw]
 cid=answers[0][':answer/id']
 if kind=='radio':r.shuffle(answers)
 question={':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':problem,':question/worked-solution':worked,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+kind,':answer-field/correct':[':answer/id',cid],':answer-field/choices':answers}]}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':question,'generation':{'version':VERSION,'template':template,'profile':profile,'seed':seed,'parameters':p,'source_id':source_id,'provenance':{k:SOURCE[k] for k in ('database','basis','lineage')},'math_fingerprint':task,'content_fingerprint':digest(identity),'bank_recipes':labels,'authored_level':template=='two_powers' or template in ('direct_quadratic','direct_extended'),'presentation_repairs':['q-167636 malformed derivative sum repaired'] if template=='difference' else [],'source_designation_inferred':template in ('direct_quadratic','direct_extended')}}

# ---------------------------------------------------------------------------
# Easy: observed simple derivatives, function difference, and familiar-input
# slopes. Degree-seven-at-minus-one retains the observed easy label.
def generate_easy(seed=0,**kwargs):
 """Generate a parallel easy family, preserving its observed field layout.

 Six families: one authored difficulty assignment for the unrated quadratic
 radio, and five observed easy families. Integer coefficient magnitudes <=9,
 constants <=20; difference A/B 1..9. Slopes retain original input 0, 1, or -1.
 The positive polynomial-first -1 family uses odd degree 3/5/7, so its derivative
 power evaluates to one without extra arithmetic. No compositions or products.
 """
 return generate('easy',seed,**kwargs)

# ---------------------------------------------------------------------------
# Moderate: quadratic plus nonzero linear component; the contextual branch
# derivative supplies its expression in normal output and never tests a join.
def generate_moderate(seed=0,**kwargs):
 """Generate a moderate derivative/branch/slope with its fixed source stages.

 Three families: one authored assignment for the unrated four-term radio,
 plus the observed branch and four-term slope. a/b/c magnitudes <=12, d <=20;
 all defining coefficients are nonzero. The branch threshold stays -3..3 and
 does not enter mathematical identity. The slope input remains zero. Complete
 authored method banks are default; uncertain scalar banks are observed-only.
 """
 return generate('moderate',seed,**kwargs)

# ---------------------------------------------------------------------------
# Hard: authored missing-level extension anchored to canonical e-3625. Every
# instance has two actual polynomial coefficient/exponent reductions.
def generate_hard(seed=0,**kwargs):
 """Generate ae^x+bx^n+cx^m -> derivative RHS, an authored hard blank.

 All three coefficients are nonzero signed integers with magnitude <=7;
 3<=n<=7, 2<=m<=3, n>m. These guards also apply to explicit parameters. Formal
 derivative, distributed terms, extracted constants, two unevaluated power-rule
 products, then reduction are retained. No extra branch or later-KP rule occurs.
 """
 return generate('hard',seed,**kwargs)

def markdown(rec):
 q=rec['question'];f=q[':question/answer-fields'][0]
 return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$' for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']

from ca_source_runtime import install as _ca_source_install
_ca_source_install(globals(),_ca_Path(__file__).with_name('17592186096611-source-policy.json'))

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
 levels=['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]
 results=[generate(level,args.seed+i,template=args.template,profile=args.profile) for level in levels for i in range(args.count)]
 print(json.dumps(results,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(v) for v in results))
