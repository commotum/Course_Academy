#!/usr/bin/env python3
"""Unit reciprocal powers: observed replay and three bounded authored levels.

math basis 1356. No EDB operations, plots or additional dependencies. Sources,
complete bank extraction, missing-key parity and native grading evidence live in
17592186064169/. Raw profiles are evidence-only and preserve omitted fields,
correct refs, difficulty and solution keys. Their formulas are parameterized,
not literal payloads; opaque observed errors are never default learner banks.
Easy: negative rational powers -a/b, 0<a<b<=9 (source q-71100).
Moderate: reciprocal integer/rational powers and reciprocal square roots,
positive exponent >1 (observed q-113705/q-29633/q-29662). Hard: authored unit
reciprocal higher roots with primitive p/q>1, 3<=q<=7, q<p<=q+8.
Each instance has ONE power-rule integration, no sums, multiples, substitutions,
definite integration, initial conditions or logarithmic exception.
"""
from __future__ import annotations
import argparse, hashlib, json, math, random, uuid
from pathlib import Path
import sympy as sp

KP_ID=17592186064169
KP_UUID='3174cae9-484e-5ca3-8e5c-3c9cddc86145'
TITLE='Finding the Antiderivative of a Reciprocal Function'
VERSION='reciprocal-power-v1'
X=sp.Symbol('x', positive=True)
C=sp.Symbol('C', real=True)
PROVENANCE={'database':'math','basis':1356,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}
TEMPLATES={
 'negative_named_radio': {'level':'easy','source':'q-29987','form':'negative','layout':'old'},
 'reciprocal_named_radio': {'level':'easy','source':'q-29989','form':'reciprocal','layout':'old'},
 'negative_named': {'level':'easy','source':'q-71100','form':'negative','layout':'named'},
 'reciprocal_named': {'level':'moderate','source':'q-113705','form':'reciprocal','layout':'named'},
 'reciprocal_integer': {'level':'moderate','source':'q-29633','form':'reciprocal','layout':'integer'},
 'reciprocal_sqrt': {'level':'moderate','source':'q-29662','form':'sqrt','layout':'sqrt'},
 'reciprocal_root': {'level':'hard','source':None,'form':'root','layout':'root'},
}
ORIGINAL_PARAMETERS={'q-29987':{'p':2,'q':3},'q-29989':{'p':3,'q':5},
 'q-71100':{'p':1,'q':7},'q-113705':{'p':4,'q':3},
 'q-29633':{'p':4,'q':1},'q-29662':{'p':5,'q':2}}
RAW_PROFILES={f'raw_{v["source"]}':t for t,v in TEMPLATES.items() if v['source']}
OPENING="Remember that integration is the opposite of differentiation. So, if ${F}^{'}(x)=f(x),$ then integrating both sides of this equation gives\n\n$$\n\\begin{aligned}{F}^{'}(x) & =f(x) \\\\ \\int {F}^{'}(x)\\,\\text{d}x & =\\int f(x)\\,\\text{d}x \\\\ F(x) & =\\int f(x)\\,\\text{d}x.\\end{aligned}\n$$\n\n"

def slug(value):
 return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def ident(text): return str(uuid.uuid5(uuid.UUID(KP_UUID),text))
def rat(v):
 v=sp.Rational(v)
 return str(v) if v.q==1 else ('-' if v<0 else '')+r'\frac{'+str(abs(v.p))+'}{'+str(v.q)+'}'
def slash(v): return str(sp.Rational(v))
def power(e,braced=False): return ('{x}' if braced else 'x')+'^{'+slash(e)+'}'
def term(a,e,braced=False,space=False):
 a=sp.Rational(a)
 coefficient='' if a==1 else '-' if a==-1 else rat(a)
 return coefficient+power(e,braced)+(' + C' if space else '+C')
def reciprocal(a,e,braced=False):
 # e is negative; the absolute coefficient is folded into numerator/denominator.
 a=sp.Rational(a)
 denominator=(str(a.q) if a.q!=1 else '')+power(-e,braced)
 return ('-' if a<0 else '')+r'\frac{'+str(abs(a.p))+'}{'+denominator+'}+C'
def integrand(t,p):
 r=sp.Rational(p['p'],p['q']); conf=TEMPLATES[t]
 if conf['form']=='negative': return power(-r,conf['layout']=='named')
 if conf['form']=='sqrt': return r'\frac{1}{\sqrt{{x}^{'+str(p['p'])+'}}}'
 if conf['form']=='root': return r'\frac{1}{\sqrt['+str(p['q'])+']{{x}^{'+str(p['p'])+'}}}'
 return r'\frac{1}{'+power(r,conf['layout']!='old')+'}'
def prompt(t,p):
 i=integrand(t,p); layout=TEMPLATES[t]['layout']
 if layout=='old': return 'Given that $f(x) = '+i+'$ and that $F^{′}(x) = f(x)$, calculate $F(x)$.'
 if layout=='named': return "Given that $f(x)="+i+"$ and that ${F}^{'}(x)=f(x)$, calculate $F(x).$"
 if layout=='integer': return 'What is the antiderivative of $'+i+'?$'
 return 'Calculate the integral of $'+i+'$'

def solution(t,p,raw=False):
 r=sp.Rational(p['p'],p['q']); n=-r; m=n+1; a=1/m
 i=integrand(t,p); layout=TEMPLATES[t]['layout']; b=layout!='old'
 if layout=='old':
  # No source solution exists. This is an explicitly authored completion.
  note=('We can use the power rule with $n='+rat(n)+'$ and get' if TEMPLATES[t]['form']=='negative' else 'Note that $'+i+'='+power(n)+'.$ So, we can use the power rule with $n='+rat(n)+'$ and get')
  return OPENING+note+'\n\n$$\n\\begin{aligned}F(x) & =\\int f(x)\\,\\text{d}x \\\\ & =\\int '+power(n)+r'\,\text{d}x \\ & =\frac{'+('x^{'+slash(n)+'+1}')+'}{('+rat(n)+'+1)}+C \\\\ & ='+term(a,m)+'.\\end{aligned}\n$$'
 note='We can use the power rule with $n='+rat(n)+'$ and get' if TEMPLATES[t]['form']=='negative' else 'Note that $'+i+'='+(r'\frac{1}{'+power(r,True)+'}=' if layout in ('sqrt','root') else '')+power(n,True)+'.$ So, we can use the power rule with $n='+rat(n)+'$ and get'
 if layout=='named':
  rows=[r'F(x) & =\int f(x)\,\text{d}x',r' & =\int '+power(n,True)+r'\,\text{d}x',r' & =\frac{{x}^{'+slash(n)+'+1}}{('+rat(n)+'+1)}+C',r' & =\frac{'+power(m,True)+'}{('+rat(m)+')}+C',r' & ='+term(a,m,True)]
  if m<0: rows.append(r' & ='+reciprocal(a,m,True)+'.')
  else: rows[-1]+='.'
  return OPENING+note+'\n\n$$\n\\begin{aligned}'+r' \\ '.join(rows)+'\\end{aligned}\n$$'
 first=r'\int '+i+(r'\,\text{d}x' if layout!='sqrt' or not raw else '')+r' & =\int '+power(n,True)+r'\,\text{d}x'
 rows=[first,r' & =\frac{{x}^{'+slash(n)+'+1}}{'+rat(n)+'+1}+C']
 if layout=='integer':
  rows.append(r' & =-\frac{'+power(m,True)+'}{'+str(abs(1/a))+'}+C')
 else: rows.append(r' & ='+term(a,m,True))
 rows.append(r' & ='+reciprocal(a,m,True)+'.')
 return note+'\n\n$$\n\\begin{aligned}'+r' \\ '.join(rows)+'\\end{aligned}\n$$'

def bank(t,p,profile):
 n=-sp.Rational(p['p'],p['q']); m=n+1
 correct=(1/m,m)
 if profile in ('raw_q-29987','observed_q-29987'):
  entries=[('omit_coefficient_reverse_input_power',1,-n),('opaque_sum_parts_reverse_result_power',p['p']+p['q'],-m),('opaque_negate_result_coefficient_add_one_to_positive_input',-m,1-n),('correct',*correct),('use_result_power_as_coefficient_reverse_power',m,-m)]
 elif profile in ('raw_q-29989','observed_q-29989'):
  entries=[('opaque_input_coefficient_input_over_remaining_parts',n,sp.Rational(p['p'],p['q']-p['p'])),('negate_unit_coefficient',-1,m),('result_power_as_coefficient_invert_power',m,1/m),('multiply_by_result_power',m,m),('correct',*correct)]
 else:
  entries=[('correct',*correct),('use_input_power_as_coefficient',n,m),('omit_increment',1/m,n),('differentiate_instead',n,n-1),('reverse_sign',-1/m,m)]
 values=[(recipe,sp.Rational(a)*X**sp.Rational(e),term(a,e,space=True)) for recipe,a,e in entries]
 # Equality of derivatives is equality of antiderivative families modulo C.
 derivatives=[sp.diff(v,X) for _,v,_ in values]
 if any(sp.simplify(a-b)==0 for k,a in enumerate(derivatives) for b in derivatives[k+1:]): raise ValueError('whole bank has equivalent families')
 if sum(sp.simplify(v-X**n)==0 for v in derivatives)!=1: raise ValueError('bank has wrong correct count')
 return values

def domain(level,t):
 if level=='easy': return [{'p':p,'q':q} for q in range(2,10) for p in range(1,q) if math.gcd(p,q)==1]
 if t=='reciprocal_integer': return [{'p':p,'q':1} for p in range(2,10)]
 if t=='reciprocal_sqrt': return [{'p':p,'q':2} for p in range(3,10,2)]
 if level=='moderate': return [{'p':p,'q':q} for q in range(2,6) for p in range(q+1,10) if math.gcd(p,q)==1]
 return [{'p':p,'q':q} for q in range(3,8) for p in range(q+1,q+9) if math.gcd(p,q)==1]

def validate_parameters(level,t,p,raw):
 if set(p)!={'p','q'} or any(type(v)!=int for v in p.values()): raise ValueError('parameters must be exactly integer p,q')
 if p['p']<=0 or p['q']<=0 or p['p']==p['q'] or math.gcd(p['p'],p['q'])!=1: raise ValueError('primitive positive exponent other than one required')
 if p not in domain(level,t): raise ValueError('explicit parameters exceed documented level/template bounds')
 if t=='reciprocal_integer' and p['q']!=1: raise ValueError('integer template needs q=1')
 if t=='reciprocal_sqrt' and p['q']!=2: raise ValueError('square root template needs q=2')

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'): raise ValueError('unknown level')
 rng=random.Random(seed)
 raw=profile in RAW_PROFILES
 if raw:
  expected=RAW_PROFILES[profile]
  if template and template!=expected: raise ValueError('raw profile/template mismatch')
  template=expected
 if profile and profile.startswith('observed_'):
  expected=RAW_PROFILES.get('raw_'+profile[len('observed_'):])
  if expected not in ('negative_named_radio','reciprocal_named_radio'): raise ValueError('unknown observed profile')
  if template and template!=expected: raise ValueError('observed profile/template mismatch')
  template=expected
 if template is None:
  template=rng.choice({'easy':['negative_named'],'moderate':['reciprocal_named','reciprocal_integer','reciprocal_sqrt'],'hard':['reciprocal_root']}[level])
 if template not in TEMPLATES or TEMPLATES[template]['level']!=level: raise ValueError('template outside level')
 if field_type not in (None,'radio',':answer-field.type/radio'): raise ValueError('only radio supported; fieldless raw sources omit fields')
 if profile not in (None,'authored_power_errors',*RAW_PROFILES,'observed_q-29987','observed_q-29989'): raise ValueError('unknown profile')
 profile=profile or 'authored_power_errors'
 params=dict(parameters) if parameters is not None else rng.choice(domain(level,template))
 validate_parameters(level,template,params,raw)
 text=prompt(template,params)
 if not raw:
  if not text.endswith(('.', '.$', '?$')): text+='.'
  text+=' Assume $x>0$.'
 worked=solution(template,params,raw=raw)
 source=TEMPLATES[template]['source']; raw_radio=raw and template.endswith('_radio')
 entries=bank(template,params,profile)
 include_fields=not raw or raw_radio
 include_solution=not raw_radio
 include_difficulty=not raw_radio
 rendered_bank=sorted(v for _,_,v in entries) if include_fields else []
 # Identity excludes profile aliases and omitted generated solution/bank content.
 identity=slug({'version':VERSION,'prompt':text,'solution':worked if include_solution else None,'bank':rendered_bank,'field_type':'radio' if include_fields else None,'difficulty':level if include_difficulty else None})
 q={':question/id':ident(identity),':question/problem':text}
 if include_difficulty: q[':question/difficulty']=':question.difficulty/'+level
 if include_solution: q[':question/worked-solution']=worked
 if include_fields:
  fid=ident(identity+'/selection'); answers=[{':answer/id':ident(fid+'/'+value),':answer/type':':answer.type/math',':answer/value':value} for _,_,value in entries]
  correct_id=answers[[a[0] for a in entries].index('correct')][':answer/id']
  rng.shuffle(answers)
  field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers}
  if not raw: field[':answer-field/correct']=[':answer/id',correct_id]
  q[':question/answer-fields']=[field]
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'source':PROVENANCE,'template':template,'profile':profile,'level':level,'seed':seed,'parameters':params,'domain':'x>0; primitives on this connected real interval; p/q != 1','source_references':[source] if source else [],'origin':'raw observed evidence' if raw else 'observed bank with authored completion' if profile.startswith('observed_') else 'authored assessment completion/extension','evidence_only':raw or profile.startswith('observed_'),'eligible_for_learning':not(raw or profile.startswith('observed_')),'mathematical_fingerprint':slug({'integrand_exponent':str(-sp.Rational(params['p'],params['q'])),'domain':'x>0','criterion':'antiderivative family modulo additive constant'}),'content_fingerprint':identity,'recipes':[e[0] for e in entries] if include_fields else [],'dependency_versions':{'sympy':sp.__version__}}}

# EASY: direct negative rational-power integration, with no reciprocal rewrite.
def generate_easy(seed=0,**kwargs): return generate('easy',seed,**kwargs)
# MODERATE: reciprocal power (including square root) -> negative power -> rule.
def generate_moderate(seed=0,**kwargs): return generate('moderate',seed,**kwargs)
# HARD (AUTHORED): reciprocal higher root -> rational power -> negative power;
# rational n+1 and reciprocal final form. The assessed operation stays one rule.
def generate_hard(seed=0,**kwargs): return generate('hard',seed,**kwargs)

def markdown(record):
 q=record['question']; meta=record['generation']
 difficulty=q.get(':question/difficulty','unrated source (authored '+meta['level']+' routing)').replace(':question.difficulty/','')
 out=['**Difficulty:** '+difficulty+'  \n**Origin:** '+meta['origin'],q[':question/problem']]
 for f in q.get(':question/answer-fields',[]):
  correct=f.get(':answer-field/correct',[None,None])[1]
  out.extend('- '+('✓ ' if a[':answer/id']==correct else '')+'$'+a[':answer/value']+'$' for a in f[':answer-field/choices'])
  if correct is None:out.append('(No correct designation captured in raw evidence.)')
 if ':question/worked-solution' in q: out.extend(['',q[':question/worked-solution']])
 return '\n\n'.join(out)
def main():
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all'); parser.add_argument('--seed',type=int,default=0); parser.add_argument('--count',type=int,default=1); parser.add_argument('--format',choices=['markdown','json'],default='markdown'); parser.add_argument('--template');parser.add_argument('--profile')
 args=parser.parse_args()
 if args.count<1: parser.error('count must be positive')
 records=[generate(level,args.seed+i,template=args.template,profile=args.profile) for level in (['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]) for i in range(args.count)]
 print(json.dumps(records,ensure_ascii=False,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
if __name__=='__main__': main()
