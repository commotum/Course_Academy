#!/usr/bin/env python3
"""Draft: coefficient-slot masks for observed third/fourth derivative families.

Easy: exactly three successive derivatives of two elementary terms.
Moderate: exactly three derivatives, with the observed preliminary power/sum
rewrite where present. Hard: exactly four derivatives of two elementary terms.
Order, input powers, denominators and reasoning stages are structural constants.
All source masks are replayed with computed coefficients; raw evidence is an
explicit ineligible profile, never a learner sampler.
"""
from pathlib import Path
import argparse,copy,hashlib,importlib.util,itertools,json,random,re,sys,uuid
from functools import lru_cache
import sympy as s
ROOT=Path(__file__).resolve().with_suffix('');VERSION='higher-order-derivatives-2026-10-14-v1'
spec=importlib.util.spec_from_file_location('higher_private_parser',ROOT/'scalar_parser.py');P=importlib.util.module_from_spec(spec);spec.loader.exec_module(P)
x=s.Symbol('x',positive=True)
fspec=importlib.util.spec_from_file_location('higher_private_math_format',ROOT/'math_format.py');F=importlib.util.module_from_spec(fspec);fspec.loader.exec_module(F)
SOURCE=json.loads((ROOT/'source.json').read_text());KP=SOURCE['record'];SOURCES={q[':question/math-academy-id']:q for q in KP[':knowledge-point/questions']}
DER=r'\frac{\text{d}}{\text{d}x}'
BLOCK=re.compile(r'\$\$\n(.*?)\n\$\$',re.S)
MATH=re.compile(r'\$\$.*?\$\$|\$[^$]*\$',re.S)
# Whole mathematical operands; their term coefficients are the only numeric slots.
SPECS={
 'polynomial_reciprocal_radio':('q-28546','moderate',3,[3*x**2,-5*x,3/x]),
 'cubic_reciprocal_radio':('q-28550','moderate',3,[x**3/4,-4/x**2]),
 'quadratic_constant_reciprocal':('q-28551','moderate',3,[7*x**2,-s.Integer(1),1/(2*x)]),
 'polynomial_reciprocal_blank':('q-310170','moderate',3,[4*x**2,6*x,-2/x]),
 'log_radical':('q-104294','easy',3,[2*s.log(x),-8*x**s.Rational(5,2)]),
 'cos_log':('q-310171','hard',4,[s.cos(x),s.log(x)]),
 'polynomial':('q-343075','easy',3,[2*x**5,-3*x**3]),
 'quotient_sum':('q-343086','moderate',3,[x**3/4,-s.Rational(1,4),1/(4*x)]),
 'exponential_reciprocal':('q-343089','easy',3,[3*s.exp(x),-1/(3*x**2)]),
 'log_polynomial':('q-343114','easy',3,[2*s.log(x),x**4]),
 'sin_exponential':('q-343120','hard',4,[s.sin(x),-s.exp(x)]),
}
BY_SOURCE={v[0]:k for k,v in SPECS.items()}
PROFILES={'polynomial_reciprocal_radio':['observed-q-28546','authored-errors'], 'cubic_reciprocal_radio':['observed-q-28550','authored-errors'], 'log_radical':['observed-q-104294','authored-errors']}

def normalize(t):
 # Captured answer values contain genuinely doubled slashes. This is presentation,
 # not an alteration of the mathematical bank. Raw Pull always retains bytes.
 while '\\\\' in t:t=t.replace('\\\\','\\')
 t=t.replace('⁡','')
 return re.sub(r'(?<![A-Za-z\\])(sin|cos|ln)(?=x)',lambda m:'\\'+m[1]+' ',t)
def parse(t):return P.scalar(normalize(t)).subs(P.x,x)
def eq(a,b):
 delta=s.expand(a-b)
 return delta==0

def tex(v,negative_powers=False):
 if negative_powers:
  terms=s.Add.make_args(s.expand(v));pieces=[]
  # x-powers retain the power-rule teaching representation.
  for term in terms:
   c,p=term.as_coeff_exponent(x)
   if p and not c.has(x):
    ct=s.latex(c);pw='x' if p==1 else '{x}^{'+s.latex(p)+'}'
    pieces.append((c<0,('' if abs(c)==1 else s.latex(abs(c)))+pw))
   else:pieces.append((bool(term.could_extract_minus_sign()),s.latex(-term if term.could_extract_minus_sign() else term)))
  out=''.join(('-' if neg else '+' if i else '')+body for i,(neg,body) in enumerate(pieces))
 else:out=s.latex(v,order='lex')
 return out.replace(r'\log',r'\ln').replace(r'\left','').replace(r'\right','').replace(r'\,',' ').replace('e^{','{e}^{')

def component_map(value,parts,newparts,order):
 """Linearly transform every displayed scalar using the stage's actual operand.
 A coefficient is tied to its complete basis term, never blind text replacement.
 """
 original=s.expand(value);result=s.Integer(0);remaining=original
 for a,b in zip(parts,newparts):
  old=s.expand(s.diff(a,x,order));new=s.expand(s.diff(b,x,order))
  if old==0:continue
  coefficient,basis=old.as_coeff_Mul()
  present=remaining.coeff(basis) if basis!=1 else s.Integer(0)
  # The constant term of a Laurent/elementary sum is extracted separately.
  if basis==1:present=sum(t for t in s.Add.make_args(remaining) if not t.has(x))
  if present:
   result+=present/coefficient*new;remaining-=present*basis
 assert eq(remaining,0),('unmapped source stage',value,order,remaining)
 return s.expand(result)

def spell(raw,parts,newparts,order,family):
 value=parse(raw);changed=component_map(value,parts,newparts,order)
 # The source's expression spelling is an operative mask at its anchor; all
 # its values, including the final answer, are independently calculated first.
 if eq(changed,value):return normalize(raw)
 if family=='quotient_sum' and order==0 and raw.startswith(r'\frac') and '{x}^{5}' in raw:
  a,b,c=[s.simplify(t/u) for t,u in zip(newparts,parts)]
  numerator=a*x**5-b*x**2+c*x
  return r'\frac{'+tex(numerator)+'}{4{x}^{2}}'
 if family=='log_radical' and order==0 and r'\sqrt' in raw:
  a,b=[s.simplify(t/u) for t,u in zip(newparts,parts)]
  return tex(2*a*s.log(x))+('+' if -8*b>0 else '-')+tex(abs(-8*b))+r'\sqrt{{x}^{5}}'
 if family=='quadratic_constant_reciprocal' and ('(2)' in raw or '(-1)' in raw or '(-2)' in raw or '0+(-3)' in raw):
  a,b,c=[s.simplify(t/u) for t,u in zip(newparts,parts)]
  if order==1:return tex(7*a)+r'\cdot 2x+0-'+tex(c/2)+r'{x}^{-2}' if c>0 else tex(7*a)+r'\cdot 2x+0+'+tex(-c/2)+r'{x}^{-2}'
  if order==2:return tex(14*a)+'+'+tex(c)+r'{x}^{-3}' if c>0 else tex(14*a)+'-'+tex(-c)+r'{x}^{-3}'
  if order==3:return r'0+('+tex(-3*c)+r'){x}^{-4}'
 return tex(changed,negative_powers=('{x}^{-' in raw))

def stages(family,parts,newparts):
 source=SOURCES[SPECS[family][0]]
 text=source.get(':question/worked-solution')
 if text is None:
  # q-28550's absent solution is explicitly authored, with the usual three
  # formal-operator/reduction stages; no claim of recovered wording.
  text='\n\n'.join(('Finally, computing the third derivative, we get' if n==3 else 'Computing the '+['','first','second'][n]+' derivative, we get')+'\n\n$$\n'+r'\begin{aligned}'+derivative_label('y',n)+' & ='+DER+'('+tex(s.diff(sum(parts),x,n-1))+r') \\ & ='+tex(s.diff(sum(parts),x,n))+r'.\end{aligned}'+'\n$$' for n in range(1,4))
 out=[];last=0;order=0
 for block in BLOCK.finditer(text):
  out.append(text[last:block.start()]);body=block.group(1)
  label=body.split(' & =')[0].replace(r'\begin{aligned}','').strip()
  if DER in body:order+=1
  rows=body.split(' & =');built=[rows[0]]
  for row in rows[1:]:
   ending='';rhs=row
   if r'\\' in rhs:rhs,ending=rhs.split(r'\\',1);ending=r'\\'+ending
   if r'\end{aligned}' in rhs:rhs,ending=rhs.split(r'\end{aligned}',1);ending=r'\end{aligned}'+ending
   leading=rhs[:len(rhs)-len(rhs.lstrip())];trailing=rhs[len(rhs.rstrip()):];rhs=rhs.strip();punct='.' if rhs.endswith('.') else '';rhs=rhs.rstrip('.')
   if rhs.startswith(DER):
    operand=rhs[len(DER):].strip();assert operand.startswith('(') and operand.endswith(')'),rhs
    rendered=DER+'('+spell(operand[1:-1],parts,newparts,order-1,family)+')'
   else:rendered=spell(rhs,parts,newparts,order,family)
   built.append(leading+rendered+punct+trailing+ending)
  out.append('$$\n'+' & ='.join(built)+'\n$$');last=block.end()
 out.append(text[last:]);result=''.join(out)
 # q-28551's h(x) is a source naming error; supplied function is y.
 if family=='quadratic_constant_reciprocal':result=result.replace('h(x)','y')
 return result

def derivative_label(name,n):
 if name=='y':return r'\frac{\text{d}'+('y' if n==1 else '^{'+str(n)+'}y')+r'}{\text{d}x'+('' if n==1 else '^{'+str(n)+'}')+'}'
 return '{'+name+'}^{'+["","′","″","‴","(4)"][n]+'}(x)'

def source_function(q):
 math=next(t[1:-1] for t in MATH.findall(q[':question/problem']) if '=' in t)
 return math.split('=',1)[1].rstrip(',.')

def prompt(family,parts,newparts):
 q=SOURCES[SPECS[family][0]];old=source_function(q);new=spell(old,parts,newparts,0,family)
 text=q[':question/problem'].replace(old,new)
 return text

def stable_id(t):return str(uuid.uuid5(uuid.NAMESPACE_URL,VERSION+':'+t))
def profile_bank(family,profile,parts,newparts):
 _,_,n,_=SPECS[family];correct=s.diff(sum(newparts),x,n)
 if family not in PROFILES:return [correct],['correct']
 a,b,*rest=[s.simplify(t/u) for t,u in zip(newparts,parts)]
 if profile=='observed-q-28546':
  c=rest[0];return [-6*c/x**3,-18*c/x**4,6*c/x**3,-6*c/x**4+6*a,18*c/x**4],['observed shortened order','correct','observed sign/order','observed retained polynomial plus short factor','observed sign']
 if profile=='observed-q-28550':
  return [s.Rational(3,2)*a+24*b/x**4,s.Rational(3,2)*a*x-24*b/x**4,s.Rational(3,2)*a*x+24*b/x**5,s.Rational(3,2)*a-96*b/x**5,s.Rational(3,2)*a+96*b/x**5],['observed incomplete reciprocal chain','observed mixed order','observed x retention and missed factor','observed sign','correct']
 if profile=='observed-q-104294':
  return [-6*a/x**3-60*b*x,4*a/x**2-60*b*x,-6*a/x**3+15*b/s.sqrt(x),a/x**2-b/s.sqrt(x),4*a/x**3-15*b/s.sqrt(x)],['observed compound log/radical pattern','observed altered powers','observed log factor/radical sign','observed unscaled power pattern','correct']
 assert profile=='authored-errors'
 # Complete, method-related errors chosen together: stop one differentiation
 # early, stop two early, negate final derivative, omit the final derivative
 # contribution of the first nonvanishing term.
 nonzero=[s.diff(t,x,n) for t in newparts if s.diff(t,x,n)!=0]
 if len(nonzero)>=2:omitted=nonzero[-1]
 else:omitted=s.diff(sum(newparts),x,n-1)-s.diff(newparts[-1],x,n-1)
 return [correct,s.diff(sum(newparts),x,n-1),s.diff(sum(newparts),x,n-2),-correct,omitted],['correct','stopped one stage early','stopped two stages early','reversed final sign','omitted term contribution']

def validate_parameters(family,parameters):
 if not isinstance(parameters,dict):raise ValueError('parameters must be an object')
 if set(parameters)-{'scales'}:raise ValueError('unknown parameter')
 scales=parameters.get('scales',[1]*len(SPECS[family][3]))
 if not isinstance(scales,list) or len(scales)!=len(SPECS[family][3]):raise ValueError('one scale per component required')
 if any(type(k)!=int or k==0 or abs(k)>6 for k in scales):raise ValueError('scales must be nonzero integers of magnitude <=6')
 return scales

def raw_evidence(source_id,level):
 if source_id not in SOURCES:raise ValueError('unknown original source ID')
 return {'knowledge_point':{'db_id':KP[':db/id'],'id':KP[':knowledge-point/id'],'title':KP[':knowledge-point/title']},'question':copy.deepcopy(SOURCES[source_id]),'generation':{'version':VERSION,'template':BY_SOURCE[source_id],'parameters':{'source_id':source_id},'profile':'raw-evidence','source_id':source_id,'source_basis':SOURCE['basis'],'source_lineage':SOURCE['lineage'],'evidence_only':True,'eligible_for_learning':False,'requested_level':level}}

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('unknown difficulty')
 if type(seed)!=int:raise ValueError('seed must be an integer')
 if profile=='raw-evidence':
  if field_type is not None or template is not None or not isinstance(parameters,dict) or set(parameters)!={'source_id'}:raise ValueError('raw evidence accepts only an original source_id parameter')
  return raw_evidence(parameters['source_id'],level)
 if profile is not None and not isinstance(profile,str):raise ValueError('profile must be a string')
 eligible=[k for k,v in SPECS.items() if v[1]==level]
 if template is not None and template not in eligible:raise ValueError('template not eligible at this difficulty')
 if field_type not in (None,'radio','blank'):raise ValueError('unsupported field type')
 if field_type:eligible=[k for k in eligible if (k in PROFILES)==(field_type=='radio')]
 if template:eligible=[template] if template in eligible else []
 if not eligible:raise ValueError('no eligible family')
 if profile is not None:
  eligible=[k for k in eligible if profile in PROFILES.get(k,['blank'])]
  if not eligible:raise ValueError('profile is not eligible for requested template/field')
 rng=random.Random(seed);family=rng.choice(eligible);sid,_,n,parts=SPECS[family]
 chosen=profile or ('authored-errors' if family in PROFILES else 'blank')
 # Whole bank chosen before parameters. Explicit invalid calls fail closed.
 for attempt in range(200):
  scales=validate_parameters(family,parameters if parameters is not None else {'scales':[rng.choice([i for i in range(-6,7) if i]) for _ in parts]})
  newparts=[a*k for a,k in zip(parts,scales)];bank,recipes=profile_bank(family,chosen,parts,newparts)
  if not any(eq(a,b) for i,a in enumerate(bank) for b in bank[i+1:]):break
  if parameters is not None:raise ValueError('whole bank has equivalent options')
 else:raise ValueError('cannot sample eligible whole bank')
 correct=s.diff(sum(newparts),x,n);assert sum(eq(a,correct) for a in bank)==1
 qsource=SOURCES[sid];problem=prompt(family,parts,newparts);solution=stages(family,parts,newparts)
 problem=F.normalize_prose(problem);solution=F.normalize_prose(solution)
 typ='radio' if family in PROFILES else 'blank';key='selection' if typ=='radio' else 'field-1'
 if typ=='blank' and '{{'+key+'}}' not in problem:problem+='\n\n$'+derivative_label('y',n)+'=$\n{{'+key+'}}'
 values=[]
 for i,val in enumerate(bank):
  rawchoices=qsource.get(':question/answer-fields',[{}])[0].get(':answer-field/choices',[])
  # The observed expression masks are used for formatting only; profile values
  # come from complete parameterized algebraic recipes above.
  if chosen.startswith('observed-') and i<len(rawchoices):
   raw=normalize(rawchoices[i][':answer/value']);values.append(raw if eq(val,parse(raw)) else tex(val))
  else:values.append(tex(val))
 values=[F.normalize_tex(v) for v in values]
 canonical=json.dumps({'level':level,'problem':problem,'solution':solution,'values':sorted(values),'field_type':typ},sort_keys=True)
 qid=stable_id(canonical);fid=stable_id(qid+':'+key)
 choices=[{':answer/id':stable_id(fid+':'+v),':answer/type':':answer.type/math',':answer/value':v} for v in values]
 correctid=next(a[':answer/id'] for a,b in zip(choices,bank) if eq(b,correct));rng.shuffle(choices)
 field={':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+typ,':answer-field/choices':choices,':answer-field/correct':[':answer/id',correctid]}
 question={':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':problem,':question/worked-solution':solution,':question/answer-fields':[field]}
 # Final derivative coefficients carry the numerical assessed task. Killed
 # polynomial coefficients and function-letter aliases never inflate capacity.
 task=json.dumps({'order':n,'operand_structure':[s.srepr(t.as_coeff_Mul()[1]) for t in parts],'derivative':s.srepr(s.simplify(correct))},sort_keys=True)
 for t in [problem,solution,*values]:
  if any(ord(c)<32 and c not in '\n\t' for c in t):raise ValueError('control character in learner content')
 return F.validate_generated_record({'knowledge_point':{'db_id':KP[':db/id'],'id':KP[':knowledge-point/id'],'title':KP[':knowledge-point/title']},'question':question,'generation':{'version':VERSION,'template':family,'profile':chosen,'seed':seed,'parameters':{'scales':scales},'source_id':sid,'source_basis':SOURCE['basis'],'source_lineage':SOURCE['lineage'],'order':n,'domain':'x>0' if any(t.has(s.log) or any(p.q!=1 for p in t.atoms(s.Rational)) and t.has(x**s.Rational(5,2)) for t in parts) else 'x!=0' if any(t.has(x**-1) or t.has(x**-2) for t in parts) else 'real x','recipes':recipes,'evidence_only':False,'eligible_for_learning':True,'mathematical_fingerprint':hashlib.sha256(task.encode()).hexdigest(),'dependencies':{'python':sys.version.split()[0],'sympy':s.__version__},'source_repairs':['inferred missing correct answer and authored missing solution'] if sid=='q-28550' else ['authored blank field; h(x) changed to supplied y'] if sid=='q-28551' else []}})

# Individually documented public sections; all enforce the observed order.
def generate_easy(seed=0,**kw):
 """Third derivative, observed elementary two-term easy families."""
 return generate('easy',seed,**kw)
def generate_moderate(seed=0,**kw):
 """Third derivative, observed power/sum rewrite and rational families."""
 return generate('moderate',seed,**kw)
def generate_hard(seed=0,**kw):
 """Fourth derivative, observed two-term trigonometric families."""
 return generate('hard',seed,**kw)

@lru_cache(maxsize=64)
def task_catalog(level,template=None,field_type=None,profile=None):
 """Finite meaningful tasks; killed coefficients/labels/banks never inflate it."""
 if level not in ('easy','moderate','hard'):raise ValueError('unknown difficulty')
 if field_type not in (None,'blank','radio'):raise ValueError('unsupported field type')
 families=[k for k,v in SPECS.items() if v[1]==level]
 if template is not None:
  if template not in families:raise ValueError('template not eligible at this difficulty')
  families=[template]
 if field_type:families=[k for k in families if (k in PROFILES)==(field_type=='radio')]
 if profile is not None:families=[k for k in families if profile in PROFILES.get(k,['blank'])]
 if not families:raise ValueError('no eligible family/profile')
 seen=set();catalog=[];domain=[i for i in range(-6,7) if i]
 for family in families:
  sid,lev,n,parts=SPECS[family];active=[i for i,v in enumerate(parts) if s.diff(v,x,n)!=0]
  bankprofile=profile or ('authored-errors' if family in PROFILES else 'blank')
  for coeffs in itertools.product(domain,repeat=len(active)):
   scales=[1]*len(parts)
   for i,v in zip(active,coeffs):scales[i]=v
   newparts=[v*k for v,k in zip(parts,scales)];bank,_=profile_bank(family,bankprofile,parts,newparts)
   if any(eq(a,b) for i,a in enumerate(bank) for b in bank[i+1:]):continue
   key=json.dumps({'order':n,'operand_structure':[s.srepr(v.as_coeff_Mul()[1]) for v in parts],'derivative':s.srepr(s.expand(s.diff(sum(newparts),x,n)))},sort_keys=True)
   if key in seen:continue
   seen.add(key);catalog.append((family,bankprofile,tuple(scales)))
 return tuple(catalog)

def capacity(level,template=None,field_type=None,profile=None):
 return len(task_catalog(level,template,field_type,profile))

def generate_many(level,count=1,seed=0,template=None,field_type=None,profile=None):
 if type(count)!=int or count<1:raise ValueError('count must be a positive integer')
 if type(seed)!=int:raise ValueError('seed must be an integer')
 catalog=list(task_catalog(level,template,field_type,profile))
 if count>len(catalog):raise ValueError('count exceeds meaningful finite capacity')
 rng=random.Random(seed);rng.shuffle(catalog)
 return [generate(level,seed+i,template=family,field_type=field_type,profile=bankprofile,parameters={'scales':list(scales)}) for i,(family,bankprofile,scales) in enumerate(catalog[:count])]

def preview(records):
 chunks=[]
 for r in records:
  q=r['question'];chunks.append(q[':question/problem'])
  for f in q.get(':question/answer-fields',[]):
   chunks.extend('- $'+a[':answer/value']+'$' for a in f.get(':answer-field/choices',[]))
  chunks.append(q.get(':question/worked-solution','[Original worked solution absent.]'))
 return '\n\n---\n\n'.join(chunks)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
 if args.count<1:ap.error('count must be positive')
 if args.profile=='raw-evidence':ap.error('raw evidence requires public API original-ID parameters')
 levels=['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]
 try:
  for level in levels:
   if args.count>capacity(level,template=args.template,profile=args.profile):raise ValueError('count exceeds meaningful finite capacity')
  records=[record for level in levels for record in generate_many(level,args.count,args.seed,template=args.template,profile=args.profile)]
 except ValueError as e:ap.error(str(e))
 print(json.dumps(records,indent=2) if args.format=='json' else preview(records))
if __name__=='__main__':main()
