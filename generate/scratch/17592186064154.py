#!/usr/bin/env python3
"""Determining a Rate of Change — immutable math basis 1356.

All source prose/stage masks are parameterized in templates.json. Source banks
with unidentified author intent are explicit observed-scale profiles, never the
default bank. E/M retain supplied-rate evaluation and entry-minus-exit; H is an
authored same-method extension adding clock conversion and nonzero familiar sine
values. No differentiation, integration, plots, or database access. See evidence.
"""
from __future__ import annotations

# Standalone source eligibility: immutable policy ledger, seeded CLI guard.
import sys as _ca_sys, os as _ca_os
from pathlib import Path as _ca_Path
_ca_sys.path.insert(0,str(_ca_Path(__file__).resolve().parent))
if __name__ == "__main__" and not _ca_os.environ.get("_CA_SOURCE_POLICY_CHILD"):
    from ca_source_runtime import cli as _ca_source_cli
    _ca_source_cli(__file__,_ca_Path(__file__).with_name('17592186064154-source-policy.json'))
    raise SystemExit(0)

import argparse, hashlib, json, random, uuid, sys
from pathlib import Path
try:
 import sympy as S
except ModuleNotFoundError:
 if __name__!='__main__':raise
 import os
 runner=Path(__file__).resolve().parents[2]/'.venv/bin/python'
 if not runner.is_file():raise
 os.execv(str(runner),[str(runner),str(Path(__file__).resolve()),*sys.argv[1:]])
KP_ID=17592186064154
KP_UUID='c7df31c9-b27a-5ce2-93c8-178ba96da000'
TITLE='Determining a Rate of Change'
VERSION='rate-change-1'
ROOT=Path(__file__).with_suffix('')
DATA=json.loads((ROOT/'templates.json').read_text())
TEMPLATES={k:v['level'] for k,v in DATA.items()}
TEMPLATES['clock_factory']='hard'

def exact(v): return S.sympify(v, rational=True)

def tex(v): return S.latex(exact(v))
def num(v):
 v=exact(v)
 if v.q==1 if v.is_Rational else False:return str(v)
 if v.is_Rational and v.q in (2,4,5,8,10,20,25,40,50,100):return str(float(v)).rstrip('0').rstrip('.')
 return tex(v)
def rnd(v,d=0):
 # All exact values first; 40 digits guard binary rounding boundaries.
 z=S.N(v,40); scale=S.Integer(10)**d
 n=S.floor(z*scale+S.Rational(1,2)) if z>=0 else -S.floor(-z*scale+S.Rational(1,2))
 return S.Rational(n,scale)
def display(v,d=None):
 if d is None:return tex(v)
 return str(int(v)) if d==0 else f'{float(v):.{d}f}'
def sub(mask,slots):
 for k,v in slots.items():mask=mask.replace('@@'+k+'@@',str(v))
 if '@@' in mask:raise ValueError('unfilled complete-component mask')
 return mask

def values(template,p):
 a,b,k,t=[exact(p.get(z,0)) for z in ['a','b','k','t']]
 base=exact(p.get('base',2)); d=DATA.get(template,{}).get('round')
 e=k*t
 if template in ['drug','battery','bacteria','krill','muons']:
  r=a*(S.exp(e) if template=='muons' else base**e); exit=S.Integer(0)
 elif template in ['stock_h','stock_g']:r=1/(a*S.sqrt(t));exit=S.Integer(0)
 elif template=='crocodiles':r=a*S.exp(e);exit=b*S.exp(e)
 elif template=='pool':r=a*t*t-b*t;exit=k*t*t
 elif template=='elephants':r=a*base**e;exit=b*S.Integer(p['exit_base'])**e
 elif template in ['factory','clock_factory']:
  r=a*t*S.exp(e);exit=b+S.Integer(p['amp'])*S.sin(2*S.pi*t/S.Integer(p['period']));d=0
 else:raise ValueError(template)
 result=S.simplify(r-exit);answer=rnd(result,d) if d is not None else result
 return r,exit,result,answer,d

def stages(template,p):
 a,b,k,t=[exact(p.get(z,0)) for z in ['a','b','k','t']]
 base=p.get('base',2);r,ex,res,answer,d=values(template,p);n=lambda z:num(z)
 power=lambda e:'{'+str(base)+'}^{'+(e if isinstance(e,str) else n(e))+'}'
 ap=n(a)+r'\cdot '
 if template in ['drug','battery','bacteria','krill']:
  rows=[ap+power(n(k)+'('+n(t)+')'),ap+power(k*t)]
  if template=='battery':rows.append(r'\frac{'+n(a)+'}{'+tex(S.Integer(base)**(-k*t))+'}')
  if template=='bacteria':rows.append(ap+tex(S.Integer(base)**(k*t)))
 elif template=='muons':rows=[ap+'{e}^{'+n(k)+'('+n(t)+')}',ap+'{e}^{'+n(k*t)+'}']
 elif template.startswith('stock'):
  if a==1:rows=[r'\frac{1}{\sqrt{'+n(t)+'}}']
  else:rows=[r'\frac{1}{'+n(a)+r'\sqrt{'+n(t)+'}}',r'\frac{1}{'+n(a)+r'\cdot '+tex(S.sqrt(t))+'}']
 elif template=='elephants':
  eb=p['exit_base'];rows=[ap+power(n(k)+'('+n(t)+')')+'-'+n(b)+r'\cdot {'+str(eb)+'}^{'+n(k)+'('+n(t)+')}',ap+tex(S.Integer(base)**(k*t))+'-'+n(b)+r'\cdot '+tex(S.Integer(eb)**(k*t))]
 elif template=='crocodiles':rows=[ap+'e^{'+n(k)+'('+n(t)+')}-'+n(b)+r'\cdot e^{'+n(k)+'('+n(t)+')}',n(a-b)+r'\cdot e^{'+n(k*t)+'}']
 elif template=='pool':rows=[n(a)+'('+n(t)+')^{2}-'+n(b)+'('+n(t)+')-'+tex(k)+'('+n(t)+')^{2}',tex(r)+'-'+tex(ex)]
 else:
  amp=p['amp'];period=p['period'];angle=2*S.pi*t/period
  trig=r'sin⁡' if template=='factory' else r'\sin'
  rows=[n(a)+'('+n(t)+'){e}^{'+n(k)+'('+n(t)+')}-('+n(b)+'+'+str(amp)+trig+r'(\frac{2\pi }{'+str(period)+'}('+n(t)+')))',n(a)+'('+n(t)+'){e}^{'+n(k*t)+'}-'+n(b)+'-'+str(amp)+trig+'('+tex(angle)+')',n(a)+'('+n(t)+'){e}^{'+n(k*t)+'}-'+tex(ex)]
 label=DATA.get(template,{}).get('label','O(@@t@@)-C(@@t@@)')
 label=sub(label,{'t':n(t)})
 last=display(answer,d)
 return r'\begin{aligned}'+label+' & ='+rows[0]+''.join(r' \\  & ='+v for v in rows[1:])+r' \\  & '+(('≈' if template in ['muons','factory'] else r'\approx ') if d is not None else '=')+last+r'.\end{aligned}',rows

def sample(template,rng):
 p=dict(DATA.get(template,{}).get('parameters',{}))
 if template.startswith('stock'):p.update(a=(1 if template=='stock_g' else rng.randint(2,5)),t=rng.choice([n*n for n in range(2,21 if template=='stock_g' else 13)]))
 elif template in ['drug','battery','bacteria','krill']:
  t=rng.choice([2,4,5,6,8,10]);e=rng.choice([1,2,3,4])*(-1 if template in ['drug','battery'] else 1)
  p.update(a=rng.randrange(5,101)*5,base=rng.choice([2,3,4,5]),t=t,k=str(S.Rational(e,t)))
  if template=='battery':p['a']=100
  if template=='drug':p['k']=str(-rng.choice([S.Rational(3,2),S.Rational(5,2),S.Rational(7,2)])/t)
 elif template=='muons':p.update(a=rng.randint(2,15),t=str(rng.choice([S.Rational(1,2),1,S.Rational(3,2),2])),k=str(-rng.choice([1,2,3,4])))
 elif template=='crocodiles':p.update(a=rng.randint(4,12),b=rng.randint(1,3),t=rng.choice([4,8,12,16]),k='1/4')
 elif template=='pool':p.update(a=rng.randint(1,4),b=rng.randint(1,3),k=str(rng.choice([S.Rational(1,4),S.Rational(1,2),S.Rational(3,4)])),t=rng.randint(3,8))
 elif template=='elephants':
  t=rng.choice([4,5,8,10]);p.update(a=rng.randrange(10,101)*10,b=rng.randrange(10,101)*10,t=t,k=str(S.Rational(rng.choice([1,2]),t)),base=rng.choice([2,3]),exit_base=rng.choice([3,4]))
 elif template in ['factory','clock_factory']:
  period=rng.choice([4,6,8,10,12,14]) if template=='factory' else rng.choice([2,6,10,14])
  t=period*rng.randint(1,4) if template=='factory' else S.Rational(period*rng.choice([1,3]),4)
  p.update(a=rng.randrange(4,21)*10,b=rng.randrange(2,10)*10,k=str(-rng.choice([S.Rational(1,10),S.Rational(1,5)])),t=str(t),amp=rng.randint(1,4)*5,period=period)
  if template=='clock_factory':p['start']=8
 if 'year' in p:p['target']=int(p['year'])+int(p['t'])
 return p

def guard(template,p,profile=None):
 required=set(DATA.get(template,{}).get('parameters',{})) if template!='clock_factory' else {'a','b','k','t','amp','period','start'}
 if set(p)!=required:raise ValueError('exact parameter keys required '+str(required))
 a=exact(p['a']);t=exact(p['t'])
 if not (a>0 and t>0 and a<=2000 and t<=(400 if template.startswith('stock') else 100)):raise ValueError('positive coefficient/time within bounds')
 if template.startswith('stock'):
  if template=='stock_g' and a!=1:raise ValueError('g endpoint pattern has unit denominator coefficient')
  if a!=int(a) or not (2 if template=='stock_h' else 1)<=a<=5 or S.sqrt(t)!=int(S.sqrt(t)) or not 4<=t<=(400 if template=='stock_g' else 144):raise ValueError('familiar positive square weeks and integer divisor')
 else:
  k=exact(p['k'])
  if abs(k)>4 or k==0:raise ValueError('nonzero bounded supplied exponent/coefficient')
  if template in ['drug','battery','muons','factory','clock_factory'] and k>=0:raise ValueError('decay exponent must be negative')
  if template in ['bacteria','krill','crocodiles','elephants'] and k<=0:raise ValueError('growth exponent must be positive')
  if template in ['battery','bacteria','krill','elephants'] and k*t!=int(k*t):raise ValueError('familiar integer exponent')
  if template=='battery' and a!=100:raise ValueError('fully charged battery percentage must be 100')
  if 'base' in p and p['base'] not in [2,3,4,5]:raise ValueError('familiar base')
  if 'b' in p and not 0<exact(p['b'])<=2000:raise ValueError('positive exit coefficient')
  if 'year' in p and (not 1900<=int(p['year'])<=2100 or p['target']!=int(p['year'])+int(t)):raise ValueError('calendar shift mismatch')
 if template in ['factory','clock_factory']:
  if not 1<=p['amp']<exact(p['b']) or p['period'] not in [2,4,6,7,8,10,12,14]:raise ValueError('positive completion rate')
  angle=2*t/p['period']
  if template=='factory' and angle!=int(angle):raise ValueError('moderate whole-period sine workload')
  if template=='clock_factory' and (p['start']!=8 or angle not in [S.Rational(1,2),S.Rational(3,2)] or t.q!=2 or t>15):raise ValueError('hard fractional clock conversion and nonzero familiar sine required')
 # Bounds apply to explicit inputs, too; observed scale profiles admit the
 # documented proportional evidence extensions but never another skill.
 if template in ['drug','battery','bacteria','krill']:
  if not 2<=t<=10 or not 5<=a<=750:raise ValueError('easy exponential workload bounds')
  e=exact(p['k'])*t
  eligible=[-S.Rational(3,2),-S.Rational(5,2),-S.Rational(7,2)] if template=='drug' else ([-1,-2,-3,-4] if template=='battery' else [1,2,3,4,7])
  if e not in eligible:raise ValueError('familiar easy exponent required')
 if template=='muons' and (not 2<=a<=23 or t not in [S.Rational(1,2),1,S.Rational(3,2),2] or exact(p['k']) not in [-1,-2,-3,-4]):raise ValueError('muon workload bounds')
 if template=='crocodiles' and (not 4<=a<=18 or not 1<=exact(p['b'])<=6 or t not in [4,8,12,16] or exact(p['k'])!=S.Rational(1,4)):raise ValueError('crocodile workload bounds')
 if template=='pool' and (not 1<=a<=6 or not 1<=exact(p['b'])<=5 or not 2<=t<=8 or exact(p['k']) not in [S.Rational(1,4),S.Rational(1,2),S.Rational(3,4),S.Rational(3,8)]):raise ValueError('polynomial rate workload bounds')
 if template=='elephants' and (not 100<=a<=1000 or not 100<=exact(p['b'])<=1000 or not 4<=t<=10 or exact(p['k'])*t not in [1,2] or p['exit_base'] not in [3,4]):raise ValueError('familiar two-exponential workload bounds')
 if template in ['factory','clock_factory']:
  if not 40<=a<=200 or not 20<=exact(p['b'])<=90 or exact(p['k']) not in [-S.Rational(1,10),-S.Rational(1,5)] or not 5<=p['amp']<=20:raise ValueError('factory coefficient workload bounds')
  if template=='factory' and t/exact(p['period']) not in [1,2,3,4]:raise ValueError('moderate one to four whole periods')
 r,ex,res,_,_=values(template,p)
 if r<=0 or ex<0:raise ValueError('nonnegative physical supplied rates')

def bank(template,p,profile,answer,d):
 a=exact(p['a']);r,ex,res,_,_=values(template,p)
 if profile.startswith('observed_'):
  if profile!='observed_'+template:raise ValueError('profile belongs to another template')
  spec=DATA[template]
  out=[]
  for item in spec['bank']:
   if item['recipe']=='correct':v=answer
   elif item['recipe']=='coefficient-scale':v=rnd(a*S.Rational(item['ratio']),item.get('decimals',0))
   elif item['recipe']=='omit-exponent-scale':v=a*S.Integer(p['base'])**exact(p['t'])
   else:raise ValueError('bank recipe')
   s=display(v,item.get('decimals')) if item['recipe']=='coefficient-scale' else display(v,d)
   if item.get('math_mask'):s=sub(item['math_mask'],{'a':num(a),'t':num(p['t']),'base':p['base']})
   unit=spec['units'];unit='liter per minute' if template=='pool' and v==1 else unit
   out.append((v,'$'+s+'$ '+unit,item['recipe']))
 else:
  if profile!='authored_operations':raise ValueError('unknown bank profile')
  if ex:
   vals=[answer,rnd(r+ex,d) if d is not None else r+ex,rnd(ex-r,d) if d is not None else ex-r,rnd(r,d) if d is not None else r,rnd(-ex,d) if d is not None else -ex]
   recipes=['correct','add-exit','reverse-subtraction','omit-exit','omit-entry']
  else:
   vals=[answer,rnd(2*res,d) if d is not None else 2*res,rnd(res/2,d) if d is not None else res/2,rnd(a,d) if d is not None else a,rnd(a*exact(p['t']),d) if d is not None else a*exact(p['t'])]
   recipes=['correct','double-coefficient','halve-coefficient','omit-exponential','replace-exponential-by-time']
  units=DATA.get(template,{}).get('units','cars per hour')
  out=[(v,'$'+display(v,d)+'$ '+units,recipe) for v,recipe in zip(vals,recipes)]
 for i,(v,_,_) in enumerate(out):
  if not v.is_real or not v.is_finite:raise ValueError('invalid bank value')
  if any(S.simplify(v-w)==0 for w,_,_ in out[:i]):raise ValueError('whole bank collision')
 return out

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 rng=random.Random(seed)
 eligible=[k for k,v in TEMPLATES.items() if v==level and (field_type is None or DATA.get(k,{}).get('field','radio')==field_type.removeprefix(':answer-field.type/'))]
 if template is None:
  if not eligible:raise ValueError('unsupported level/layout')
  template=rng.choice(eligible)
 if template not in eligible:raise ValueError('template does not belong to requested level/layout')
 spec=DATA.get(template,{})
 profile=profile or ('blank' if spec.get('field')=='blank' else 'authored_operations')
 if spec.get('field')=='blank' and profile!='blank':raise ValueError('blank has no bank profile')
 for _ in range(1000):
  p=parameters.copy() if parameters is not None else sample(template,rng)
  try:
   guard(template,p,profile);r,ex,res,answer,d=values(template,p)
   options=[(answer,str(answer),'correct')] if spec.get('field')=='blank' else bank(template,p,profile,answer,d)
   break
  except ValueError:
   if parameters is not None:raise
 else:raise ValueError('sampler failed to create an eligible complete instance')
 block,rows=stages(template,p)
 slots={z:num(v) for z,v in p.items()};slots.update(answer=display(answer,d),block=block,ktex=tex(p.get('k',0)),plural='' if answer==1 else 's',poly=('' if exact(p['a'])==1 else num(p['a']))+'t^{2} - '+('' if exact(p.get('b',0))==1 else num(p.get('b',0)))+'t')
 if template=='clock_factory':
  total=int(exact(p['t'])*60)+480; clock=f'{total//60}:{total%60:02d}'
  problem=(f'A factory begins work at $8\\text{{:}}00$ am. Its order rate is $O(t)={p["a"]}t e^{{{num(p["k"])}t}}$ cars per hour and its completion rate is $C(t)={p["b"]}+{p["amp"]}\\sin(2\\pi t/{p["period"]})$ cars per hour, where $t$ is hours after work begins. What is the rate of change in the number of cars under construction at the 24-hour time ${clock.replace(":",r"\text{:}")}$? Orders enter construction immediately. Round your answer to the nearest integer.')
  solution=f'The rate of change is the order rate minus the completion rate. The elapsed time is $t=({total}-480)/60={num(p["t"])}$ hours.\n\n$$\n{block}\n$$\n\nTherefore, the rate of change is ${display(answer,d)}$ cars per hour.'
 else:
  problem=sub(spec['problem'],slots);solution=sub(spec['solution'],slots)
  if template.startswith('stock'):
   name='h' if template=='stock_h' else 'g'
   rate=r'\frac{1}{'+(num(p['a']) if exact(p['a'])!=1 else '')+r'\sqrt{x}}'
   problem=f'The supplied rate function is ${name}\'(x)={rate}$ thousand dollars per week, for $x>0$.\n\n'+problem
 # Missing source fields get minimal supported supplied-fragment presentation.
 if spec.get('field')=='blank' and '{{field-1}}' not in problem:problem+='\n\n{{field-1}}$\\,$ '+spec['units']+'.'
 payload=[VERSION,problem,solution,sorted(v for _,v,_ in options)]
 digest=hashlib.sha256(json.dumps(payload,ensure_ascii=False).encode()).hexdigest()
 uid=lambda label:str(uuid.uuid5(uuid.NAMESPACE_URL,f'{KP_ID}/{digest}/{label}'))
 answers=[{':answer/id':uid('answer/'+v),':answer/type':':answer.type/math' if spec.get('field')=='blank' else ':answer.type/text',':answer/value':v} for _,v,_ in options]
 correct=next(a[':answer/id'] for a,(_,_,recipe) in zip(answers,options) if recipe=='correct');rng.shuffle(answers)
 field={':answer-field/id':uid('field'),':answer-field/key':'field-1' if spec.get('field')=='blank' else 'selection',':answer-field/type':':answer-field.type/'+spec.get('field','radio'),':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]}
 kind='stock' if template.startswith('stock') else ('single_base' if template in ['drug','battery','bacteria','krill'] else template)
 mathkey=[kind,{z:str(exact(v)) for z,v in p.items() if z not in ['year','target','start']},d]
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':uid('question'),':question/difficulty':':question.difficulty/'+level,':question/problem':problem,':question/worked-solution':solution,':question/answer-fields':[field]},'generation':{'version':VERSION,'dependencies':{'python':sys.version.split()[0],'sympy':S.__version__},'template':template,'parameters':p,'profile':profile,'seed':seed,'provenance':{'database':'math','basis':1356,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'},'source_ids':spec.get('sources',[]),'authored':template=='clock_factory','stock_context_status':'authored reciprocal-root family inferred from one displayed endpoint; global source function unavailable' if template.startswith('stock') else None,'domain':'positive elapsed time; supplied rates nonnegative; signed net rate; positive magnitude of decrease','ordered_rows':rows,'exact_components':[str(r),str(ex)],'exact_result':str(res),'answer':str(answer),'round_digits':d,'recipes':[z for _,_,z in options],'mathematical_fingerprint':hashlib.sha256(json.dumps(mathkey).encode()).hexdigest(),'content_fingerprint':digest}}

# EASY: one supplied rate evaluation, square-root denominator or exponential.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE: two supplied rates, entry minus exit, calendar/elapsed-time evaluation.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# HARD (authored): same entry-minus-exit; fractional clock conversion and sine ±1.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)

def markdown(record):
 q=record['question'];s=q[':question/problem']+'\n\n'
 for f in q[':question/answer-fields']:
  if f[':answer-field/type'].endswith('/radio'):s+='\n'.join('- '+a[':answer/value'] for a in f[':answer-field/choices'])+'\n\n'
 return s+'Worked solution:\n\n'+q[':question/worked-solution']
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['json','markdown'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
 records=[generate(l,args.seed+i,args.template,profile=args.profile) for l in (['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]) for i in range(args.count)]
 print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))

from ca_source_runtime import install as _ca_source_install
_ca_source_install(globals(),_ca_Path(__file__).with_name('17592186064154-source-policy.json'))

if __name__=='__main__':main()
