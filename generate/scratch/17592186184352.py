#!/usr/bin/env python3
"""Definite exponential substitution, frozen math basis2275; local draft only.

Easy: quadratic natural exponent with a logarithmic endpoint, optionally shifted.
Moderate: quadratic/linear other-base exponent, with its logarithmic primitive.
Hard: exponential numerator proportional to the denominator derivative.
Each family keeps its own complete source chain, including regrouping and
endpoint arithmetic. Numeric slots are bounded; no new operators or branches.
"""
from __future__ import annotations
import argparse, hashlib, importlib.util, itertools, json, random, sys, uuid
from pathlib import Path
import sympy as s
HERE=Path(__file__).with_suffix('')
spec=importlib.util.spec_from_file_location('definite_integrals_math_format',HERE/'reference/math_format.py')
mf=importlib.util.module_from_spec(spec);spec.loader.exec_module(mf)
KP_ID=17592186184352
KP_UUID='114e3660-63d9-511d-b89c-e71081ffa1e5'
TITLE='Evaluating Definite Integrals'
VERSION='definite-exponential-substitution-1'
LEVELS=('easy','moderate','hard')
SOURCE=json.loads((HERE/'source.json').read_text())
SOURCES={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
TEMPLATES={'natural_integer_radio':'q-13751','natural_fraction_radio':'q-30953','shifted_natural_blank':'q-350740','quadratic_scaled_base_radio':'q-30977','square_base_radio':'q-30978','quadratic_base_blank':'q-346400','linear_base_blank':'q-350743','exponential_ratio_blank':'q-350751'}
ANCHORS={'natural_integer_radio':dict(c=5,b=3),'natural_fraction_radio':dict(d=5,b=5),'shifted_natural_blank':dict(b=2,k=3),'quadratic_scaled_base_radio':dict(b=2,k=3),'square_base_radio':dict(b=2),'quadratic_base_blank':dict(b=3),'linear_base_blank':dict(b=3,k=2,h=1),'exponential_ratio_blank':dict(a=3,c=4,h=1,l=2,r=5)}
DIFFICULTY={n:('moderate' if sid=='q-30977' else SOURCES[sid][':question/difficulty'][':db/ident'].split('/')[-1]) for n,sid in TEMPLATES.items()}
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def tex(v):return mf.normalize_tex(s.latex(s.sympify(v),ln_notation=True))
def fr(n,d):return r'\frac{'+str(n)+'}{'+str(d)+'}'
def ln(v):return r'\ln('+str(v)+')'
def power(b,v):return str(b)+'^{'+str(v)+'}'
def mul(c,v):return v if c==1 else tex(c)+v
def integral(lo,hi,body,var='x'):return r'\int_{'+lo+'}^{'+hi+'}'+body+r'\,\mathrm{d}'+var
def bar(prim,lo,hi):return prim+r'\big|_{'+lo+'}^{'+hi+'}'
def parameters_for(name):
 if name=='natural_integer_radio':return [dict(c=c,b=b) for c,b in itertools.product(range(2,10),range(2,10))]
 if name=='natural_fraction_radio':return [dict(d=d,b=b) for d,b in itertools.product(range(2,10),range(2,10))]
 if name=='shifted_natural_blank':return [dict(b=b,k=k) for b,k in itertools.product(range(2,7),range(2,5))]
 if name=='quadratic_scaled_base_radio':return [dict(b=b,k=k) for b,k in itertools.product(range(2,7),range(2,5))]
 if name=='square_base_radio':return [dict(b=b) for b in range(2,10)]
 if name=='quadratic_base_blank':return [dict(b=b) for b in range(2,13)]
 if name=='linear_base_blank':return [dict(b=b,k=k,h=h) for b,k,h in itertools.product(range(2,7),range(2,5),range(1,4))]
 if name=='exponential_ratio_blank':return [dict(a=a,c=c,h=h,l=l,r=r) for a,c,h,l,r in itertools.product(range(2,6),range(2,7),range(1,4),range(2,5),range(5,9))]
 raise ValueError('Unknown family')
def layout(name,p):
 """The operative source rows; each RHS is a distinct retained source stage."""
 b=p.get('b');k=p.get('k',1);field='radio' if name.endswith('radio') else 'blank'
 if name in ('natural_integer_radio','natural_fraction_radio','shifted_natural_blank'):
  c=p['c'] if name=='natural_integer_radio' else s.Rational(1,p['d']) if name=='natural_fraction_radio' else s.Integer(1)
  k=1 if name=='natural_integer_radio' else 2 if name=='natural_fraction_radio' else p['k']
  shift=ln(b) if name=='shifted_natural_blank' else ''
  exp=mul(k,'x^{2}')+('+'+shift if shift else '')
  lo='0';hi=r'\sqrt{'+ln(b)+'}';ul=shift or '0';uh=mul(k+1 if shift else k,ln(b));der=mul(2*k,'x');scale=s.Rational(c,2*k)
  body=mul(c,'x')+power('e',exp);I=integral(lo,hi,body);A=s.Rational(c,2*k)*(b**k-1)*(b if shift else 1)
  diff=tex(s.Rational(1,2*k))+r'\,\mathrm{d}u=x\,\mathrm{d}x'
  rows=[]
  if name=='natural_integer_radio':rows.append(integral(lo,hi,tex(c)+power('e',exp)+r'\cdot x'))
  if name=='natural_fraction_radio':rows.append(tex(c)+integral(lo,hi,power('e',exp)+r'\cdot x'))
  if name=='natural_integer_radio':rows.append(integral(ul,uh,tex(c)+power('e','u')+r'\cdot '+tex(s.Rational(1,2*k)), 'u'))
  elif name=='natural_fraction_radio':rows.append(tex(c)+integral(ul,uh,power('e','u')+r'\cdot '+tex(s.Rational(1,2*k)),'u'))
  else:rows.append(integral(ul,uh,power('e','u')+r'\cdot '+tex(s.Rational(1,2*k)),'u'))
  rows += [tex(scale)+integral(ul,uh,power('e','u'),'u'),bar(tex(scale)+power('e','u'),ul,uh),tex(scale)+'('+power('e',uh)+'-'+power('e',ul)+')',tex(scale)+'('+str(b**(k+1 if shift else k))+'-'+str(b if shift else 1)+')']
  if name=='natural_integer_radio':rows.append(tex(scale)+'('+str(b-1)+')')
  elif name=='natural_fraction_radio':rows.append(fr(b**k-1,2*k*p['d']))
  rows.append(tex(A));u=exp
 elif name in ('quadratic_scaled_base_radio','square_base_radio','quadratic_base_blank','linear_base_blank'):
  base=b*b if name=='square_base_radio' else b
  linear=name=='linear_base_blank';k=p['k'] if name in ('quadratic_scaled_base_radio','linear_base_blank') else 1
  h=p.get('h',0);u=mul(k,'x')+'+'+str(h) if linear else mul(k,'x^{2}')
  lo='0';hi='1';ul=str(h);uh=str(k+h);der=str(k) if linear else mul(2*k,'x')
  matched=name in ('quadratic_base_blank','linear_base_blank');c=k if linear else 2 if matched else 1
  body=(tex(c)+r'\cdot ' if linear else mul(c,'x')+(r'\cdot ' if matched else ''))+power(base,u)
  I=integral(lo,hi,body);scale=s.Integer(1) if matched else s.Rational(1,2*k)
  diff=r'\mathrm{d}u='+tex(c)+(r'\,\mathrm{d}x' if linear else r'x\,\mathrm{d}x') if matched else tex(scale)+r'\,\mathrm{d}u=x\,\mathrm{d}x'
  A=scale*(base**(k+h)-base**h)/s.log(base)
  prim=fr(power(base,'u'),ln(base));rows=[]
  if not matched:rows += [integral(lo,hi,power(base,u)+r'\cdot x'),integral(ul,uh,power(base,'u')+r'\cdot '+tex(scale),'u'),tex(scale)+integral(ul,uh,power(base,'u'),'u')]
  else:rows.append(integral(ul,uh,power(base,'u'),'u'))
  rows.append(bar(('' if matched else tex(scale))+prim,ul,uh))
  if matched:rows.append(fr(1,ln(base))+'('+power(base,uh)+'-'+power(base,ul)+')')
  rows.append(('' if matched else tex(scale))+fr(1,ln(base))+'('+str(base**(k+h))+'-'+str(base**h)+')')
  if name=='square_base_radio':rows.append(fr(base-1,'2'+ln(base)))
  rows.append(tex(s.expand_log(A,force=True)) if name=='square_base_radio' else tex(A))
 else:
  a,c,h,l,r=(p[z] for z in ('a','c','h','l','r'));lo=ln(l);hi=ln(r);u=mul(a,power('e','x'))+'+'+str(h);ul=str(a*l+h);uh=str(a*r+h);der=mul(a,power('e','x'))
  body=fr(mul(a*c,power('e','x')),u);I=integral(lo,hi,body);diff=r'\mathrm{d}u='+der+r'\,\mathrm{d}x';A=c*s.log(s.Rational(a*r+h,a*l+h))
  rows=[integral(lo,hi,fr(c,u)+r'\cdot '+der),integral(ul,uh,fr(c,'u'),'u'),str(c)+integral(ul,uh,fr(1,'u'),'u'),bar(str(c)+r'\ln|u|',ul,uh),str(c)+'('+ln(uh)+'-'+ln(ul)+')',tex(A)]
 sol="Let's introduce the new variable $u="+u+'.$ Differentiating gives\n\n$$\n'+fr(r'\mathrm{d}u',r'\mathrm{d}x')+'='+der+r'\quad\Longrightarrow\quad '+diff+'.\n$$\n\nNext, we determine the new limits of integration:\n\n| $x$ | $'+lo+'$ | $'+hi+'$ |\n| --- | --- | --- |\n| $u$ | $'+ul+'$ | $'+uh+'$ |\n\nTherefore, we get\n\n$$\n'+r'\begin{aligned}'+I+' &= '+r' \\ & = '.join(rows)+r'.\end{aligned}'+'\n$$'
 prompt=('Evaluate the integral $'+I+'.$') if field=='radio' else 'Evaluate the following integral. Give an exact answer.\n\n$'+I+'=$\n{{field-1}}'
 return prompt,sol,A,field
def bank(name,p,A,profile):
 b=p.get('b');k=p.get('k',1)
 if not name.endswith('radio'):return [A]
 if profile=='authored_method_bank':
  # Complete method-derived bank: correct, omitted lower endpoint, ignored
  # differential factor, reversed bounds, doubled differential factor.
  if name=='natural_integer_radio':upper=s.Rational(p['c']*b,2);ignored=2*A
  elif name=='natural_fraction_radio':upper=s.Rational(b*b,4*p['d']);ignored=4*A
  else:
   base=b*b if name=='square_base_radio' else b;k=1 if name=='square_base_radio' else k
   upper=base**k/(2*k*s.log(base));ignored=2*k*A
  return [A,upper,ignored,-A,A/2]
 if profile!='source_bank':raise ValueError('Unknown bank profile')
 if name=='natural_integer_radio':return [s.Rational(p['c']*b,2),s.Integer(b),2*s.log(b),A,s.log(b)]
 if name=='natural_fraction_radio':return [s.Rational(1,4*p['d']),A,s.Rational(1,p['d']),b+1,s.Rational(b-2,4*p['d'])]
 if name=='quadratic_scaled_base_radio':return [(b**k-1)/(k*s.log(b)),A,1/(2*k*s.log(b)),(b**k-1)/(2*s.log(b)),1/(b**k*s.log(b))]
 B=b*b;return [B/((B-1)*s.log(b)),B*s.log(b)/(B-1),(B-1)*s.log(b)/B,A,(B-1)/s.log(b)]
def valid_bank(values,A):
 for i,a in enumerate(values):
  for b in values[:i]:
   if s.simplify(a-b)==0:return False
 return sum(s.simplify(a-A)==0 for a in values)==1
def task_fingerprint(name,p):
 """Canonical given, independent of layout/profile and common ratio scaling."""
 x=s.Symbol('x',real=True);b=p.get('b')
 if name=='natural_integer_radio':F=p['c']*x*s.exp(x*x);L=0;H=s.sqrt(s.log(b))
 elif name=='natural_fraction_radio':F=x*s.exp(2*x*x)/p['d'];L=0;H=s.sqrt(s.log(b))
 elif name=='shifted_natural_blank':F=b*x*s.exp(p['k']*x*x);L=0;H=s.sqrt(s.log(b))
 elif name=='exponential_ratio_blank':F=s.cancel(p['a']*p['c']*s.exp(x)/(p['a']*s.exp(x)+p['h']));L=s.log(p['l']);H=s.log(p['r'])
 else:
  base=b*b if name=='square_base_radio' else b;k=p.get('k',1);lb=s.expand_log(s.log(base),force=True)
  if name=='linear_base_blank':F=k*base**p['h']*s.exp(s.expand(k*x*lb))
  else:F=(2 if name=='quadratic_base_blank' else 1)*x*s.exp(s.expand(k*x*x*lb))
  L=0;H=1
 return digest([s.srepr(s.cancel(F)),s.srepr(s.sympify(L)),s.srepr(s.sympify(H))])
@mf.checked_math_content
def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in LEVELS:raise ValueError('Unknown difficulty')
 rng=random.Random(seed);eligible=[n for n in TEMPLATES if DIFFICULTY[n]==level and (field_type is None or ('radio' if n.endswith('radio') else 'blank')==field_type)]
 if template is None:
  if not eligible:raise ValueError('No family for field type')
  template=rng.choice(eligible)
 if template not in eligible:raise ValueError('Family outside difficulty/field contract')
 profile=profile or ('authored_method_bank' if template.endswith('radio') else 'source_blank')
 if not template.endswith('radio') and profile not in ('source_blank','source_presentation'):raise ValueError('Blank profile')
 candidates=parameters_for(template)
 if profile=='source_presentation':
  if parameters is None:parameters=dict(ANCHORS[template])
  if parameters!=ANCHORS[template]:raise ValueError('Source presentation replay is restricted to the original anchor')
 if parameters is not None and parameters not in candidates:raise ValueError('Parameters outside bounded family domain')
 for attempt in range(500):
  p=dict(parameters) if parameters is not None else rng.choice(candidates)
  prompt,sol,A,field=layout(template,p);values=bank(template,p,A,profile)
  if valid_bank(values,A):break
  if parameters is not None:raise ValueError('Complete bank ambiguous at parameters')
 else:raise ValueError('No eligible bank')
 if profile=='source_presentation':prompt=prompt.replace('Give an exact answer.','Do not round the answer.')
 prompt=mf.normalize_prose(prompt);sol=mf.normalize_prose(sol);valtexts=[tex(v) for v in values]
 key='selection' if field=='radio' else 'field-1';basis=dict(version=VERSION,template=template,prompt=prompt,solution=sol,bank=sorted(valtexts),field=field)
 identity=digest(basis);qid=str(uuid.uuid5(uuid.NAMESPACE_URL,identity));fid=str(uuid.uuid5(uuid.UUID(qid),key))
 answers=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),v)),':answer/type':':answer.type/math',':answer/value':v} for v in valtexts]
 correct=answers[next(i for i,v in enumerate(values) if s.simplify(v-A)==0)][':answer/id']
 rng.shuffle(answers)
 record={'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':qid,':question/problem':prompt,':question/worked-solution':sol,':question/difficulty':':question.difficulty/'+level,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+field,':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]}]},'generation':{'version':VERSION,'seed':seed,'template':template,'bank_profile':profile,'parameters':p,'source_ids':[TEMPLATES[template]],'basis':SOURCE['basis'],'lineage':SOURCE['lineage'],'domain':'real x on the finite displayed interval; positive exponential bases and denominator','fingerprint':digest({'template':template,'parameters':p}),'task_fingerprint':digest({'prompt':prompt.replace('Do not round the answer.','Give an exact answer.')}),'python':sys.version.split()[0],'sympy':s.__version__,'plots':[],'authorship':'observed source family; bounded numeric slots; unrated q-30977 assigned moderate; method bank separately authored when selected'}}
 record['generation']['task_fingerprint']=task_fingerprint(template,p)
 return record
def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)
def generate_hard(seed=0,**kw):return generate('hard',seed,**kw)
def markdown(r):
 q=r['question'];f=q[':question/answer-fields'][0]
 return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$' for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=(*LEVELS,'all'),default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=('json','markdown'),default='markdown');ap.add_argument('--template');ap.add_argument('--profile');a=ap.parse_args()
 if a.count<1:ap.error('count must be positive')
 records=[generate(l,a.seed+i,template=a.template,profile=a.profile) for l in (LEVELS if a.difficulty=='all' else (a.difficulty,)) for i in range(a.count)]
 print(json.dumps(records,ensure_ascii=False,indent=2) if a.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
if __name__=='__main__':main()
