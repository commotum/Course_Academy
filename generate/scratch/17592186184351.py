#!/usr/bin/env python3
"""Frozen basis2275 exponential substitution families, local review only.

Every normal family uses its recovered full prompt and ordered solution mask.
Each bank is a complete empirical expression profile; historical error intent
is not inferred. Slots change the substituted function and proportional scale.
"""
from __future__ import annotations
import argparse, functools, hashlib, importlib.util, itertools, json, random, re, uuid
from pathlib import Path
import sympy as s
HERE=Path(__file__).with_suffix('')
sp=importlib.util.spec_from_file_location('kp17592186184351_math_format',HERE/'reference/math_format.py')
mf=importlib.util.module_from_spec(sp);sp.loader.exec_module(mf)
KP_ID=17592186184351
KP_UUID='ed3b6c3d-b840-50ef-9e6b-584bf14877b3'
TITLE='More Complex Cases'
VERSION='exponential-complex-substitution-1'
CAPTURE=json.loads((HERE/'source.json').read_text())
SOURCES={q[':question/math-academy-id']:q for q in CAPTURE['record'][':knowledge-point/questions']}
LEVELS=('easy','moderate','hard')
TEMPLATES={'positive_integer_power':'q-113852','base_inverse_root':'q-73670','natural_positive_root':'q-49577','shifted_base_positive_root':'q-73669','derivative_ratio':'q-113873','base_ratio_linear_bank':'q-31478','base_ratio_log_bank':'q-31480','shifted_base_inverse_root':'q-113876'}
STYLE={sid:name for name,sid in TEMPLATES.items()}
ANCHORS={'q-113852':dict(a=2,k=3,b=2),'q-73670':dict(base=2,b=9),'q-49577':dict(a=5,b=4),'q-73669':dict(base=2,b=5),'q-113873':dict(k=2,c=1),'q-31478':dict(base=5,b=1),'q-31480':dict(base=4,b=2),'q-113876':dict(base=3,b=1)}
DIFFICULTY={sid:q.get(':question/difficulty',{}).get(':db/ident',':question.difficulty/moderate').split('/')[-1] for sid,q in SOURCES.items()}
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
def number(v):return mf.normalize_tex(s.latex(s.Rational(v)))
def product(c,t):
 c=s.Rational(c)
 if c==1:return t
 if c.denominator==1:return str(c.numerator)+t
 return r'\frac{'+('' if c.numerator==1 else str(c.numerator))+t+'}{'+str(c.denominator)+'}'
def frac(n,d):return r'\frac{'+n+'}{'+d+'}'
def exp(k=1,var='x',base='e'):return '{'+str(base)+'}^{'+('' if k==1 else str(k))+var+'}'
def ln(base):return r'\operatorname{ln}⁡'+str(base)
def power(t,n):return '{('+t+')}^{'+str(n)+'}'
def root(t,n=1):return r'\sqrt{'+(t if n==1 else '('+t+')^{'+str(n)+'}')+'}'
def swap(text,pairs):
 # Simultaneous longest-token replacement; inserted values cannot be rematched.
 keys=sorted(pairs,key=len,reverse=True)
 return re.sub('|'.join(re.escape(k) for k in keys),lambda m:pairs[m[0]],text) if keys else text
def domain(name,p):
 if name in ('base_inverse_root','shifted_base_positive_root'):
  variable='z' if name=='base_inverse_root' else 'x'
  return f"real {variable}; {p['base']}^{variable} - {p['b']} > 0"
 if name=='derivative_ratio':return f"real x on each connected interval where exp({p['k']}x)-{p['k']*p['c']}x != 0"
 return 'all real values of the displayed integration variable; substituted expression positive'
def parameters_for(name):
 if name=='positive_integer_power':return [dict(a=a,k=k,b=b) for a,k,b in itertools.product(range(2,7),range(2,7),range(1,9)) if a!=k and 3*a!=4*k]
 if name=='natural_positive_root':return [dict(a=a,b=b) for a,b in itertools.product(range(3,8),range(1,9))]
 if name=='derivative_ratio':return [dict(k=k,c=c) for k,c in itertools.product(range(2,8),range(1,7))]
 if name=='shifted_base_inverse_root':return [dict(base=base,b=b) for base,b in itertools.product(range(3,8),range(1,9))]
 return [dict(base=base,b=b) for base,b in itertools.product(range(2,8),range(1,10))]
def admissible(name,p):
 if any(type(v)!=int for v in p.values()):raise ValueError('Parameter values must be integers')
 if p not in parameters_for(name):raise ValueError('Parameters outside explicit bounded family domain')
def level_templates(level):return [name for name,sid in TEMPLATES.items() if DIFFICULTY[sid]==level]
def masks(name,p):
 """Parameter transports for each full observed prompt/solution stage sequence."""
 sid=TEMPLATES[name];q=SOURCES[sid];old=ANCHORS[sid]
 if name=='positive_integer_power':
  a,k,b=p['a'],p['k'],p['b'];E=exp(k);U=E+'+'+str(b);O=exp(3)+'+2';P=power(U,4)
  pairs={power(O,4)+'/':P+'/',frac(power(O,4),'6'):product(s.Rational(a,4*k),P),frac('2','3'):number(s.Rational(a,k)),frac('2'+power(O,4),'3'):product(s.Rational(a,k),P),O:U,exp(3):E,'3'+exp(3):str(k)+E,'2'+exp(3):str(a)+E}
  bank=[frac(P,'4')+'+C',frac(power(U,3),'3')+'+C',product(s.Rational(a,4*k),P)+'+C',product(s.Rational(a,4*k),power(U,3))+'+C',product(s.Rational(a,k),P)+'+C'];correct=2
 elif name=='natural_positive_root':
  a,b=p['a'],p['b'];U=exp()+'+'+str(b);O=exp()+'+4'
  pairs={frac('10','3'):number(s.Rational(2*a,3)),O:U,'5':str(a)}
  # Whole option patterns, not pooled recipes. The first empirical coefficient
  # a-2 and 1/a pattern are recorded as unresolved historical interpretations.
  bank=[str(a-2)+root(U,5)+'+C',frac('1',str(a))+root(U,3)+'+C',str(a)+root(U,3)+'+C',str(2*a)+r'\sqrt[3]{('+U+')^{2}}+C',number(s.Rational(2*a,3))+root(U,3)+'+C'];correct=4
 elif name in ('base_inverse_root','shifted_base_positive_root'):
  base,b=p['base'],p['b'];var='z' if name=='base_inverse_root' else 'x';E=exp(var=var,base=base);U=E+'-'+str(b);O=exp(var=var,base=2)+('-9' if var=='z' else '-5');L=ln(base)
  pairs={O:U,exp(var=var,base=2):E,ln(2):L}
  if name=='base_inverse_root':
   R=root(U);bank=[frac(R,'2')+'+C','2'+R+'+C',frac('2'+R,L)+'+C',frac(R,'2'+L)+'+C','2'+L+R+'+C'];correct=2
  else:
   pairs.update({'{2}^{x+1}':'{'+str(base)+'}^{x+1}',frac('4','3'+ln(2)):frac(str(2*base),'3'+L),frac('2',ln(2)):frac(str(base),L),'2'+exp(base=2):str(base)+E,'2'+r'\int':str(base)+r'\int',r'\int 2\cdot':r'\int '+str(base)+r'\cdot'})
   R=root(U,3);bank=[str(base)+root(U)+'+C',frac(str(3*base),L)+R+'+C',frac(str(2*base),'3'+L)+R+'+C',frac(str(base),'3'+L)+root(U)+'+C',number(s.Rational(base,3))+R+'+C'];correct=2
 elif name=='derivative_ratio':
  k,c=p['k'],p['c'];E=exp(k);U=E+'-'+str(k*c)+'x';O=exp(2)+'-2x';N=E+'-'+str(c);J=r'\operatorname{ln}⁡|'+U+'|'
  pairs={O:U,exp(2)+'-1':N,'2'+exp(2)+'-2':str(k)+E+'-'+str(k*c),'2('+exp(2)+'-1)':str(k)+'('+N+')',frac('1','2'):frac('1',str(k)),frac(r'\operatorname{ln}⁡|'+O+'|','2'):frac(J,str(k)),exp(2):E}
  bank=[frac(str(k)+J,E)+'+C',frac(J,str(k*k))+'+C',frac(J,str(k)+E)+'+C',frac(J,E)+'+C',frac(J,str(k))+'+C'];correct=4
 elif name in ('base_ratio_linear_bank','base_ratio_log_bank'):
  base,b=p['base'],p['b'];ob=old['base'];E=exp(base=base);U=E+'+'+str(b);O=exp(base=ob)+'+'+str(old['b']);L=ln(base);J=r'\operatorname{ln}⁡('+U+')'
  pairs={O:U,exp(base=ob):E,ln(ob):L}
  first=frac(str(base)+'x',L) if name=='base_ratio_linear_bank' else frac(r'\operatorname{ln}⁡('+E+')',L)
  bank=[first+'+C',frac(J,L)+'+C',frac(str(base)+J,L)+'+C',frac('1',E+L)+'+C',frac(J,str(base)+L)+'+C']
  if name=='base_ratio_log_bank':bank=[bank[0],bank[3],bank[4],bank[1],bank[2]];correct=3
  else:correct=1
 else:
  base,b=p['base'],p['b'];U=str(base)+'^{x} + '+str(b);R=r'\sqrt{'+U+'}';L=r'\ln '+str(base)
  pairs={'3^{x + 1}':str(base)+'^{x + 1}','3^{x} + 1':U}
  bank=[frac(str(2*base)+R,L)+' + C',frac(R,str(2*base)+L)+' + C',frac('2'+R,str(base)+L)+' + C',frac(R,L)+' + C',frac(str(base)+R,'2'+L)+' + C'];correct=0
 return swap(q[':question/problem'],pairs),swap(q.get(':question/worked-solution',''),pairs),bank,correct
def completed_solution(p):
 b,h=p['base'],p['b'];E=str(b)+'^{x}';U=E+' + '+str(h);L=r'\ln '+str(b)
 return "Let's introduce the new variable $u="+U+'.$ Differentiating gives\n\n$$\n'+r'\frac{\text{d}u}{\text{d}x}='+E+L+r'\,⟹\,\frac{'+str(b)+'}{'+L+r'}\,\text{d}u='+str(b)+r'^{x+1}\,\text{d}x.'+'\n$$\n\nTherefore,\n\n$$\n'+r'\begin{aligned}\int\frac{'+str(b)+r'^{x+1}}{\sqrt{'+U+r'}}\,\text{d}x & =\int\frac{1}{\sqrt{u}}\cdot\frac{'+str(b)+'}{'+L+r'}\,\text{d}u \\ & =\frac{'+str(b)+'}{'+L+r'}\int u^{-1/2}\,\text{d}u \\ & =\frac{'+str(2*b)+r'\sqrt{u}}{'+L+r'}+C \\ & =\frac{'+str(2*b)+r'\sqrt{'+U+'}}{'+L+r'}+C.\end{aligned}'+'\n$$'

OPAQUE={'natural_positive_root','shifted_base_positive_root','shifted_base_inverse_root'}
def authored_bank(name,p,correct):
 """One whole operation-based bank; empirical opaque constants stay replay-only."""
 if name=='natural_positive_root':
  U=exp()+'+'+str(p['b']);K=s.Rational(2*p['a'],3);scale=number(K);inverse=number(1/K);n=3
 else:
  base=p['base'];U=exp(base=base)+('-' if name=='shifted_base_positive_root' else '+')+str(p['b']);L=ln(base);n=3 if name=='shifted_base_positive_root' else 1
  divisor='3'+L if n==3 else L;scale=frac(str(2*base),divisor);inverse=frac(divisor,str(2*base))
 wrong_exponent=scale+root(U)+'+C' if n==3 else frac(scale,root(U))+'+C'
 return [correct,scale+root(U,n+2)+'+C',inverse+root(U,n)+'+C','-'+scale+root(U,n)+'+C',wrong_exponent],0

def integer(value,label):
 if type(value)!=int:raise ValueError(label+' must be an integer')
 return value
@functools.lru_cache(maxsize=2048)
def semantic_key(prompt):
 """Read the actual displayed integrand; ignore bank, seed and TeX aliases."""
 if not hasattr(semantic_key,'reader'):
  spec=importlib.util.spec_from_file_location('kp17592186184351_semantic_reader',HERE/'reference/separable-ode-parser.py')
  semantic_key.reader=importlib.util.module_from_spec(spec);spec.loader.exec_module(semantic_key.reader)
 reader=semantic_key.reader
 body=next(b for b in reader.blocks(prompt) if r'\int' in b).replace(r'\displaystyle','')
 body=body.replace(r'\text{d}','d').replace(r'\,','').strip().rstrip('.,')
 match=re.fullmatch(r'\\int\s*(.*?)\s*d([xz])',body,re.S)
 if not match:raise ValueError('Unrecognized displayed integral for semantic catalog')
 expression=reader.scalar(match[1])
 normalized=s.factor_terms(s.cancel(s.expand_power_exp(expression)))
 return digest({'integrand':s.srepr(normalized),'integration_variable':match[2],'method_target':'whole indefinite primitive modulo additive constant'})

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 integer(seed,'seed')
 if level not in LEVELS:raise ValueError('Unknown difficulty')
 if field_type not in (None,'radio'):raise ValueError('Only observed radio fields supported')
 rng=random.Random(seed)
 if profile:
  if ':' in profile:
   origin,sid=profile.split(':',1)
   if origin not in ('observed','completed') or sid not in STYLE:raise ValueError('Unknown profile')
   selected=STYLE[sid]
   if template not in (None,selected):raise ValueError('Template/profile mismatch')
   template=selected
  elif profile not in ('empirical','method_errors'):raise ValueError('Unknown profile')
 names=level_templates(level)
 if profile=='method_errors':names=[n for n in names if n in OPAQUE]
 if not names:raise ValueError('No eligible template for difficulty/profile')
 name=template or rng.choice(names);sid=TEMPLATES.get(name)
 if sid is None or DIFFICULTY[sid]!=level:raise ValueError('Template/difficulty mismatch')
 origin='observed' if profile and profile.startswith('observed:') else 'completed'
 p=dict(parameters) if parameters is not None else rng.choice(parameters_for(name));admissible(name,p)
 prompt,worked,bank,ci=masks(name,p)
 selected_profile=profile or ('method_errors' if name in OPAQUE else 'empirical')
 if selected_profile=='method_errors':
  if name not in OPAQUE:raise ValueError('Method-error bank restricted to opaque source profiles')
  bank,ci=authored_bank(name,p,bank[ci])
 if sid=='q-113876' and origin=='completed':worked=completed_solution(p)
 prompt=mf.normalize_prose(prompt);worked=mf.normalize_prose(worked);bank=[mf.normalize_tex(v) for v in bank]
 complete=not (sid=='q-113876' and origin=='observed')
 q={':question/problem':prompt}
 if worked:q[':question/worked-solution']=worked
 if sid!='q-113876' or complete:q[':question/difficulty']=':question.difficulty/'+level
 content=digest([VERSION,q,sorted(bank),'radio','selection',bank[ci] if complete else None])
 qid=str(uuid.uuid5(uuid.UUID(KP_UUID),content));fid=str(uuid.uuid5(uuid.UUID(qid),'selection'))
 answers=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),v)),':answer/type':':answer.type/math',':answer/value':v} for v in bank]
 correct=answers[ci][':answer/id'];rng.shuffle(answers)
 f={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers}
 if complete:f[':answer-field/correct']=[':answer/id',correct]
 q[':question/id']=qid;q[':question/answer-fields']=[f]
 record={'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'template':name,'profile':selected_profile,'bank_profile':('authored:method_errors' if selected_profile=='method_errors' else 'empirical:'+sid),'bank_interpretation':('wrong power, inverted scale, sign, omitted power increment' if selected_profile=='method_errors' else 'complete observed expression patterns; historical error intent unresolved'),'parameters':p,'seed':seed,'source_ids':[sid],'basis':CAPTURE['basis'],'lineage':CAPTURE['lineage'],'domain':domain(name,p),'plot_rating':'none','content_fingerprint':content,'mathematical_fingerprint':semantic_key(prompt),'eligible_for_learning':complete,'authored_extension':selected_profile=='method_errors' or p!=ANCHORS[sid] or sid=='q-113876' and complete,'python_sampling':'single finite parameter tuple; batch samples semantic catalog without replacement'}}
 if complete:mf.validate_generated_record(record)
 else:
  mf.validate_prose(prompt)
  for value in bank:mf.validate_tex(value)
 return record
def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)
def generate_hard(seed=0,**kw):return generate('hard',seed,**kw)
@functools.lru_cache(maxsize=64)
def _catalog(level,template,field_type,profile,parameter_items):
 if level not in LEVELS:raise ValueError('Unknown difficulty')
 names=level_templates(level)
 if profile and ':' in profile:
  origin,sid=profile.split(':',1)
  if origin not in ('observed','completed') or sid not in STYLE:raise ValueError('Unknown profile')
  name=STYLE[sid]
  if template not in (None,name):raise ValueError('Template/profile mismatch')
  names=[name] if name in names else []
 elif profile=='method_errors':names=[n for n in names if n in OPAQUE]
 elif profile not in (None,'empirical'):raise ValueError('Unknown profile')
 if template is not None:
  if template not in names:raise ValueError('Template/difficulty/profile mismatch')
  names=[template]
 if not names:raise ValueError('No eligible template for difficulty/profile')
 groups={}
 for name in names:
  params=[dict(parameter_items)] if parameter_items is not None else parameters_for(name)
  for p in params:
   r=generate(level,0,template=name,field_type=field_type,parameters=p,profile=profile)
   groups.setdefault(r['generation']['mathematical_fingerprint'],[]).append((name,tuple(sorted(p.items()))))
 return tuple((key,tuple(alternatives)) for key,alternatives in sorted(groups.items()))
def semantic_catalog(level,template=None,field_type=None,parameters=None,profile=None):
 """Finite normalized-integrand groups, with original bank alternatives."""
 items=None
 if parameters is not None:
  if any(type(v)!=int for v in parameters.values()):raise ValueError('Parameter values must be integers')
  items=tuple(sorted(parameters.items()))
 return [{'semantic_key':key,'alternatives':[{'template':name,'parameters':dict(p)} for name,p in alternatives]} for key,alternatives in _catalog(level,template,field_type,profile,items)]
def capacity(level,**kwargs):return len(semantic_catalog(level,**kwargs))
def generate_batch(level,count=1,seed=0,template=None,field_type=None,parameters=None,profile=None):
 """Sample mathematical tasks without replacement, even across bank profiles."""
 integer(seed,'seed');integer(count,'count')
 if count<1:raise ValueError('count must be positive')
 catalog=semantic_catalog(level,template,field_type,parameters,profile)
 if count>len(catalog):raise ValueError('count '+str(count)+' exceeds finite semantic capacity '+str(len(catalog)))
 rng=random.Random(seed);chosen=rng.sample(catalog,count);records=[]
 for group in chosen:
  alternative=rng.choice(group['alternatives'])
  records.append(generate(level,rng.randrange(2**63),template=alternative['template'],field_type=field_type,parameters=alternative['parameters'],profile=profile))
 return records
generate_many=generate_batch
def markdown(record):
 q=record['question'];f=q[':question/answer-fields'][0];return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$' for a in f[':answer-field/choices'])+'\n\n'+q.get(':question/worked-solution','')
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=(*LEVELS,'all'),default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=('json','markdown'),default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
 try:records=[r for level in (LEVELS if args.difficulty=='all' else (args.difficulty,)) for r in generate_batch(level,count=args.count,seed=args.seed,template=args.template,profile=args.profile)]
 except ValueError as error:ap.error(str(error))
 print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
if __name__=='__main__':main()
