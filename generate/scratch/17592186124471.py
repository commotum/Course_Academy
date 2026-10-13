#!/usr/bin/env python3
"""Pointwise multivariable chain-rule generator, math basis 1356.

Source recipes are extracted math/prose masks, with a genuine whole-function
scale parameter. All original banks are retained as explicit evidence profiles;
scaling their complete banks is a defined equivariant replay operation, not a
claim that arbitrary source scalars identify the original mistaken operations.
Default banks instead apply a complete, explicit set of chain-rule mistakes to
varied functions and curves. A collision rejects the whole instance.

No database reads/writes, plots, or engine changes. See the private evidence
folder for observed/authored scope, raw notation anomalies and test results.
"""
from __future__ import annotations
import argparse, hashlib, json, random, re, uuid
from pathlib import Path
import sympy as sp

KP_ID=17592186124471
KP_UUID='ea1e5a55-a957-52cd-b693-0e48770672a6'
TITLE='Computing the Rate of Change of a Multivariable Function at a Point Using the Chain Rule'
VERSION='point-chain-1.0'
HERE=Path(__file__).with_suffix('')
CAPTURE=json.loads((HERE/'source.json').read_text())
SOURCES={q[':question/math-academy-id']:q for q in CAPTURE['record'][':knowledge-point/questions']}
x,y,z,t=sp.symbols('x y z t',real=True)
VARS=(x,y,z)
SOURCE_SPECS={
 'q-36247':('mixed_product','hard',dict(a=1,b=3,c=1,d=1,e=-1,t0=1)),
 'q-36253':('sine_difference','moderate',dict(a=1,b=2,c=4,t0=1)),
 'q-167499':('quotient','moderate',dict(a=1,b=2,c=1,t0=9)),
 'q-36227':('trig_powers','moderate',dict(a=1,b=1,c=1,d=1,t0='pi/4')),
 'q-94884':('square_difference','moderate',dict(a=1,b=1,c=1,d=2,e=-1,t0=0)),
 'q-94887':('triple_product','hard',dict(a=1,b=2,c=1,d=3,e=-1,t0=1)),
 'q-94888':('radical_square','hard',dict(a=1,b=1,c=1,d=4,e=3,t0=2)),
 'q-94891':('log_norm','hard',dict(a=1,b=1,c=-1,d=3,e=2,t0=0)),
}
TEMPLATES={v[0]:v[1] for v in SOURCE_SPECS.values()}
TEMPLATES['quadratic_affine']='easy'
BANK_PROFILES={sid+'_raw':{'source':sid,'template':v[0],'level':v[1],'origin':'observed-equivariant-replay','parameters':dict(v[2],scale=1)} for sid,v in SOURCE_SPECS.items()}
for _sid in ('q-36247','q-36253'):
 BANK_PROFILES[_sid+'_raw_omission']={**BANK_PROFILES[_sid+'_raw'],'origin':'observed-raw-omission'}
BANK_PROFILES.update({name+'_operations':{'template':name,'level':level,'origin':'authored-method-operations'} for name,level in TEMPLATES.items()})

class SampleRejected(ValueError): pass

def tex(v): return sp.latex(sp.sympify(v),order='lex').replace(r'\log',r'\ln')
def group(s): return r'\left('+s+r'\right)'
def vec(parts): return '⟨'+','.join(parts)+'⟩'
def block(s): return '$$\n'+s+'\n$$'
def aligned(lhs,rows):
 return block(r'\begin{aligned}'+lhs+' & ='+r' \\  & ='.join(rows)+r'\end{aligned}')
def join_sum(parts):
 return ''.join(('+' if i and not p.startswith('-') else '')+p for i,p in enumerate(parts))
def product(a,b): return group(a)+r'\cdot '+group(b)
def fingerprint(v): return hashlib.sha256(json.dumps(v,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def serial(p): return {k:str(v) if isinstance(v,sp.Basic) else v for k,v in p.items()}

def model(name,p):
 a,b,c=[sp.sympify(p[k]) for k in ('a','b','c')]
 d,e=sp.sympify(p.get('d',0)),sp.sympify(p.get('e',0))
 if name=='quadratic_affine': F=a*x*x+b*y*y; curve=[c*t+d,e*t+p['h']]
 elif name=='quotient': F=a*x/y; curve=[b*t,c*sp.sqrt(t)]
 elif name=='trig_powers': F=a*x**3+b*y*y; curve=[c*sp.sin(t),d*sp.cos(t)]
 elif name=='square_difference': F=a*x*x-b*y*y; curve=[c*t*t,d*t+e]
 elif name=='triple_product': F=a*x*y*z; curve=[b*t,c*sp.sqrt(t),d*t+e]
 elif name=='radical_square': F=a*x*z*z+b*y**3; curve=[c*t,sp.sympify(d),sp.sqrt(t*t-e)]
 elif name=='log_norm': F=a*sp.log(x*x+y*y+z*z); curve=[b*t+c,sp.sympify(d),e*t]
 elif name=='mixed_product': F=a*x*x+b*x*y*z; curve=[c*t*t,d*t+1,e*t]
 elif name=='sine_difference': F=a*sp.sin(x-y); curve=[b*sp.sqrt(t),c*t]
 else: raise ValueError('Unknown template')
 scale=sp.sympify(p.get('scale',1)); F=scale*F
 return F,curve

def check_parameters(name,p,raw=False):
 expected=set(next(v[2] for v in SOURCE_SPECS.values() if v[0]==name)) if name!='quadratic_affine' else set('a b c d e h t0'.split())
 if set(p)!=expected|({'scale'} if raw else set()): raise ValueError('Wrong parameter keys')
 for k,v in p.items():
  vv=sp.sympify(v)
  if k!='t0' and (not vv.is_Integer or abs(vv)>6): raise ValueError('Integer coefficient magnitude must be at most 6')
 if raw:
  base=next(v[2] for v in SOURCE_SPECS.values() if v[0]==name)
  if any(sp.sympify(p[k])!=sp.sympify(v) for k,v in base.items()): raise ValueError('Raw banks fix the source curve and evaluation point; vary scale only')
  if p['scale'] not in (1,2,3,4): raise ValueError('Replay scale must be 1..4')
 else:
  # Same-level bounds apply to explicit inputs, not just the sampler.
  if any(abs(sp.sympify(p[k]))>4 for k in p if k not in ('t0',)): raise ValueError('Authored coefficient bounds are -4..4')
  required={'quadratic_affine':'a b c e','quotient':'a b c','trig_powers':'a b c d','square_difference':'a b c d e','triple_product':'a b c d e','radical_square':'a b c d e','log_norm':'a b c d e','mixed_product':'a b c d e','sine_difference':'a b c'}[name].split()
  if any(sp.sympify(p[k])==0 for k in required): raise ValueError('A defining component cannot vanish')
  v=sp.sympify(p['t0'])
  if name=='trig_powers':
   if v not in (sp.pi/6,sp.pi/4,sp.pi/3,2*sp.pi/3,3*sp.pi/4): raise ValueError('Familiar nonzero trig evaluation angle required')
  elif name in ('quotient','triple_product','sine_difference'):
   if v not in (1,4,9): raise ValueError('Positive perfect-square evaluation time required')
  elif name=='radical_square':
   if v!=2 or v*v-p['e']!=1: raise ValueError('Hard radical needs positive perfect-square radicand')
  elif v not in (-2,-1,0,1,2): raise ValueError('Evaluation time must be -2..2')
 F,r=model(name,p); point=[q.subs(t,sp.sympify(p['t0'])) for q in r]
 if any(q.is_real is not True for q in point): raise ValueError('Non-real point')
 if name=='quotient' and point[1]==0: raise ValueError('Zero denominator')
 if name=='log_norm' and sum(q*q for q in point)==0: raise ValueError('Logarithm domain failure')

def sample(name,rng):
 s=lambda:rng.choice([-3,-2,-1,1,2,3])
 p={'a':s(),'b':s(),'c':s(),'t0':rng.choice([-2,-1,0,1,2])}
 if name=='quadratic_affine': p.update(d=rng.randint(-3,3),e=s(),h=rng.randint(-3,3))
 elif name=='trig_powers': p.update(d=s(),t0=str(rng.choice([sp.pi/6,sp.pi/4,sp.pi/3,2*sp.pi/3,3*sp.pi/4])))
 elif name in ('square_difference','mixed_product','triple_product','log_norm'): p.update(d=s(),e=s())
 elif name=='radical_square':
  p.update(d=s(),t0=2,e=3)
 if name in ('quotient','triple_product','sine_difference'): p['t0']=rng.choice([1,4,9])
 return p

D=r'\frac{\text{d}}{\text{d}t}'
LHS=D+'[f(r(t))]'
GR=r'∇f(r(t))'
VEL=r'{r}^{′}(t)'
CHAIN=GR+r'\cdot '+VEL

def generic_solution(name,p,F,r):
 variables=VARS[:len(r)]; labels=','.join(map(str,variables)); grad=[sp.diff(F,v) for v in variables]
 mapping=dict(zip(variables,r)); comp=[sp.expand(q.subs(mapping,simultaneous=True)) for q in grad]
 vel=[sp.diff(q,t) for q in r]; terms=[sp.simplify(g*v) for g,v in zip(comp,vel)]
 deriv=sp.simplify(sum(terms)); at=sp.sympify(p['t0']); value=sp.simplify(deriv.subs(t,at))
 formal=vec([r'\frac{∂}{∂'+str(v)+'}('+tex(F)+')' for v in variables])
 grad_tex=vec([tex(q) for q in grad]); comp_tex=vec([tex(q) for q in comp]); vel_tex=vec([tex(q) for q in vel])
 # Unevaluated substitutions retain the primitive product/power operations.
 def subs_keep(q):
  if q in mapping:return mapping[q]
  if not q.args:return q
  return q.func(*[subs_keep(a) for a in q.args],evaluate=False)
 uns=[tex(subs_keep(q)) for q in grad]
 comp_rows=[vec(uns),comp_tex]
 if name in ('quotient','trig_powers'): comp_rows=[comp_tex]
 dot_rows=[CHAIN,comp_tex+r'\cdot '+vel_tex,join_sum([product(tex(g),tex(v)) for g,v in zip(comp,vel)])]
 evaluated_terms=join_sum([tex(q) for q in terms])
 if name in ('quotient','triple_product','radical_square','log_norm'): dot_rows.append(evaluated_terms)
 dot_rows.append(tex(deriv)+'.')
 # For two-term source families this is their single reduction stage.
 substitution=tex(deriv.xreplace({t:sp.Symbol('EVALTIME')})).replace('EVALTIME','('+tex(at)+')')
 endpoint_parts=join_sum([tex(q.subs(t,at)) for q in terms])
 eval_rows=[substitution]
 if name=='trig_powers':
  # Preserve evaluation of individual gradient and velocity factors, then the
  # uncollected sum, before radical collection. Do not emit duplicate CAS rows.
  eval_rows.append(join_sum([product(tex(g.subs(t,at)),tex(v.subs(t,at))) for g,v in zip(comp,vel)]))
  eval_rows.append(endpoint_parts)
 elif name in ('radical_square','log_norm'):eval_rows.append(endpoint_parts)
 eval_rows.append(tex(value)+'.')
 prose=(f'The rate of change of $f({labels})$ with respect to $t$ along the curve $r(t)$ is given by ${LHS}.$ To calculate this, we can use the chain rule.\n\n'
  'The chain rule in vector form states that\n\n'+block(LHS+'='+CHAIN+'.')+
  '\n\nFirst, we need to compute $∇f('+labels+'):$\n\n'+aligned('∇f('+labels+')',[formal,grad_tex])+
  '\n\nNext, we substitute '+', '.join('$'+str(v)+'='+tex(q)+'$' for v,q in zip(variables,r))+' into the above to find $'+GR+':$\n\n'+aligned(GR,comp_rows)+
  '\n\nNow, we calculate the derivative of $r(t),$ which is\n\n'+aligned(VEL,[vec([D+'('+tex(q)+')' for q in r]),vel_tex+'.'])+
  '\n\nApplying the chain rule, we get\n\n'+aligned(LHS,dot_rows)+
  '\n\nTherefore, the rate of change of $f$ along the curve $r(t)$ at $t='+tex(at)+'$ is\n\n'+aligned(D+'[f(r('+tex(at)+'))]',eval_rows))
 return prose,grad,comp,vel,terms,deriv,value

def scaled(s,c):
 """Complete mathematical-component slot; neutral scale elides the operator."""
 return s if c==1 else str(c)+r'\left('+s+r'\right)'

def source_mask_solution(source,scale):
 """Extract six blocks into fixed prose and independent RHS operation masks.

 Every gradient/composition and explicit dot/evaluation RHS is scaled once.
 The formal chain row already references f, so receives no second multiplier.
 Curve derivatives are invariant. This is an actual parameterized mathematical
 transformation, applied to every source stage, never a literal payload branch.
 """
 raw=SOURCES[source].get(':question/worked-solution')
 if raw is None:return None
 block_index=-1
 def change(match):
  nonlocal block_index
  block_index+=1; content=match.group(1)
  if block_index in (0,3): return '$$'+content+'$$'
  rows=content.split(r' \\  & =')
  first=rows[0].split(' & =',1)
  if len(first)!=2:raise ValueError('Unexpected source stage mask')
  rhs=[first[1]]+rows[1:]; output=[]
  for i,s in enumerate(rhs):
   ending=''; core=s
   if r'\end{aligned}' in core:core,ending=core.split(r'\end{aligned}',1); ending=r'\end{aligned}'+ending
   period='.' if core.endswith('.') else ''; core=core[:-1] if period else core
   # The chain-rule references f itself; all explicit arithmetic is base-F math.
   new=core if block_index==4 and i==0 else scaled(core,scale)
   output.append(new+period+ending)
  return '$$'+first[0]+' & ='+r' \\  & ='.join(output)+'$$'
 return re.sub(r'\$\$([\s\S]*?)\$\$',change,raw)

def source_prompt(source,scale):
 prompt=SOURCES[source][':question/problem']
 # Extract exactly the complete f-expression span, preserving prose and curve.
 match=re.search(r'(\$f\([^$]*?=\s*)([^$]+)(\$)',prompt)
 if not match:raise ValueError('Missing complete function slot')
 return prompt[:match.start(2)]+scaled(match.group(2),scale)+prompt[match.end(2):]

def source_bank(source,scale):
 # Exact mathematical base values, a complete bank with known correct math.
 bases={
 'q-36247':[-17,1,-15,9,3],
 'q-36253':[5*sp.cos(2),-3*sp.cos(8),0,-3*sp.cos(2),sp.cos(2)],
 'q-167499':[-sp.sqrt(3),-sp.Rational(1,9),1/sp.sqrt(3),sp.Rational(1,3),1],
 'q-36227':[(sp.sqrt(3)-2)/2,2*sp.sqrt(3)-1,sp.Rational(3,8),(3*sp.sqrt(2)-4)/4,0],
 'q-94884':[-1,4,-3,5,2], 'q-94887':[-8,15,6,12,-10],
 'q-94888':[-12,10,6,9,-7],
 'q-94891':[sp.Rational(3,10),sp.Rational(8,13),-sp.Rational(12,17),-sp.Rational(1,5),sp.Rational(2,3)],
 }
 raw=SOURCES[source][':question/answer-fields'][0][':answer-field/choices']
 return [(scaled(a[':answer/value'],scale),scale*sp.sympify(v),'observed-equivariant-slot-'+str(i)) for i,(a,v) in enumerate(zip(raw,bases[source]))]

def operation_bank(name,comp,vel,terms,value,at):
 """Choose an entire fixed method-operation bank before any validity check."""
 n=len(comp)
 if name in ('radical_square','log_norm'):
  wrong=[terms[0],terms[-1],sum(comp),sum(g*v*v for g,v in zip(comp,vel))]
  labels=['omit-final-moving-coordinate','omit-first-moving-coordinate','omit-curve-derivatives','square-curve-derivatives']
 elif n==2:
  wrong=[terms[0],terms[1],sum(comp),terms[0]-terms[1]]
  labels=['omit-second-term','omit-first-term','omit-curve-derivatives','reverse-second-term-sign']
 else:
  wrong=[sum(terms[1:]),sum(terms[:-1]),sum(comp),sum(terms[:-1])-terms[-1]]
  labels=['omit-first-term','omit-last-term','omit-curve-derivatives','reverse-last-term-sign']
 values=[value]+[sp.simplify(q.subs(t,at)) for q in wrong]
 return [(tex(v),v,l) for v,l in zip(values,['correct']+labels)]

def assemble(level,name,p,seed,profile):
 F,r=model(name,p)
 solution,grad,comp,vel,terms,deriv,value=generic_solution(name,p,F,r)
 at=sp.sympify(p['t0']); raw=profile.endswith(('_raw','_raw_omission')); source=BANK_PROFILES[profile].get('source')
 if raw:
  prompt=source_prompt(source,p['scale']); solution=source_mask_solution(source,p['scale']) or solution
  bank=source_bank(source,p['scale'])
 else:
  prompt=f'Compute the rate of change of the function $f({",".join(map(str,VARS[:len(r)]))})={tex(F)}$ with respect to $t$ along the curve $r(t)={vec([tex(q) for q in r])}$ at the point $t={tex(at)}.$'
  bank=operation_bank(name,comp,vel,terms,value,at)
 vals=[q[1] for q in bank]
 if any(v.has(sp.nan,sp.zoo,sp.oo) or v.is_real is not True for v in vals):raise SampleRejected('Invalid whole bank')
 if any(sp.simplify(a-b)==0 for i,a in enumerate(vals) for b in vals[i+1:]):raise SampleRejected('Ambiguous whole bank')
 correct_indices=[i for i,v in enumerate(vals) if sp.simplify(v-value)==0]
 if len(correct_indices)!=1:raise SampleRejected('Incorrect bank designation')
 # Canonical task fingerprint excludes bank/profile, seed, and variable spelling.
 task=fingerprint({'f':sp.srepr(F),'curve':[sp.srepr(q) for q in r],'t0':sp.srepr(at)})
 omission=profile.endswith('_raw_omission')
 identity=fingerprint({'version':VERSION,'level':None if omission else level,'prompt':prompt,'solution':None if omission else solution,'bank':sorted(q[0] for q in bank),'correct':None if omission else bank[correct_indices[0]][0]})
 qid=uuid.uuid5(uuid.NAMESPACE_URL,identity); fid=uuid.uuid5(qid,'selection')
 answers=[{':answer/id':str(uuid.uuid5(fid,q[0])),':answer/type':':answer.type/math',':answer/value':q[0]} for q in bank]
 correct=answers[correct_indices[0]][':answer/id']; random.Random(seed).shuffle(answers)
 result={'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':str(qid),':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':[{':answer-field/id':str(fid),':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]}]},'generation':{'version':VERSION,'seed':seed,'template':name,'parameters':serial(p),'bank_profile':profile,'bank_origin':BANK_PROFILES[profile]['origin'],'parameter_fingerprint':task,'content_fingerprint':identity,'plot_rating':'none','source_provenance':{k:CAPTURE[k] for k in ('database','basis','lineage')},'source_ids':[source] if source else [sid for sid,v in SOURCE_SPECS.items() if v[0]==name],'authored_level':level=='easy' or source in ('q-36247','q-36253'),'source_missing_correct':source in ('q-36247','q-36253'),'raw_source_notation':raw,'evidence_only':raw,'eligible_for_learning':not raw,'math':{'function':str(F),'curve':[str(q) for q in r],'gradient':[str(q) for q in grad],'composition':[str(q) for q in comp],'velocity':[str(q) for q in vel],'terms':[str(q) for q in terms],'derivative':str(deriv),'answer':str(value)},'recipes':{a:recipe for a,_,recipe in bank},'scope':'rate with respect to t, not arclength; gradient supplied nowhere','sympy_version':sp.__version__}}

 if omission:
  result['question'].pop(':question/difficulty')
  result['question'].pop(':question/worked-solution')
  result['question'][':question/answer-fields'][0].pop(':answer-field/correct')
  result['generation']['raw_omitted_fields']=[':question/difficulty',':question/worked-solution',':answer-field/correct']
 return result

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if field_type not in (None,'radio'):raise ValueError('Only observed radio layout is supported')
 if level not in ('easy','moderate','hard'):raise ValueError('Unknown difficulty')
 if profile:
  if profile not in BANK_PROFILES:raise ValueError('Unknown bank profile')
  spec=BANK_PROFILES[profile]
  if template and template!=spec['template']:raise ValueError('Profile/template mismatch')
  template=spec['template']
 rng=random.Random(seed)
 names=[name for name,difficulty in TEMPLATES.items() if difficulty==level]
 name=template or rng.choice(names)
 if name not in names:raise ValueError('Template/level mismatch')
 profile=profile or name+'_operations'; raw=profile.endswith(('_raw','_raw_omission'))
 if raw:
  p=dict(BANK_PROFILES[profile]['parameters']) if parameters is None else dict(parameters)
  if parameters is None:p['scale']=rng.choice([1,2,3,4])
  check_parameters(name,p,True)
  return assemble(level,name,p,seed,profile)
 for _ in range(256):
  p=dict(parameters) if parameters is not None else sample(name,rng)
  check_parameters(name,p)
  try:return assemble(level,name,p,seed,profile)
  except SampleRejected:
   if parameters is not None:raise
 raise SampleRejected('No unambiguous complete bank after bounded rejection')

# EASY — authored two-variable quadratic, affine nonconstant curve, two dot terms.
# Both terms are retained before reduction; coefficients -4..4; t0 -2..2.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):
 return generate('easy',seed,template,field_type,parameters,profile)

# MODERATE — observed quotient/sqrt, familiar trig powers, shifted quadratic;
# unrated sine-composition layout receives an explicit authored moderate label.
# Each variant computes the full gradient, curve velocity, and point evaluation.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):
 return generate('moderate',seed,template,field_type,parameters,profile)

# HARD — three-variable product/cross-power/log functions, nonlinear curves or
# three contributions. Constant coordinates keep their zero dot contributions.
# Unrated mixed-product layout receives an explicitly authored hard assignment.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):
 return generate('hard',seed,template,field_type,parameters,profile)

def markdown(record):
 q=record['question']; g=record['generation']; f=q[':question/answer-fields'][0]
 if ':answer-field/correct' not in f:
  return f"### {g['template']} / {g['bank_profile']} (raw missing assessment)\n\n"+q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$' for a in f[':answer-field/choices'])+'\n\nOriginal difficulty, correct designation, and worked solution are absent.'
 return f"### {g['template']} / {g['bank_profile']}\n\n"+q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$'+(' **correct**' if a[':answer/id']==f[':answer-field/correct'][1] else '') for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']

def main():
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all')
 parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=1)
 parser.add_argument('--format',choices=['markdown','json'],default='markdown')
 parser.add_argument('--template',choices=list(TEMPLATES));parser.add_argument('--profile',choices=list(BANK_PROFILES))
 args=parser.parse_args()
 if args.count<1:parser.error('Positive count required')
 if args.difficulty=='all' and (args.template or args.profile):parser.error('Select a difficulty for template/profile')
 levels=['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]
 records=[generate(l,args.seed+i,args.template,profile=args.profile) for l in levels for i in range(args.count)]
 print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
if __name__=='__main__':main()
