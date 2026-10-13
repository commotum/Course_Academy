#!/usr/bin/env python3
"""Solving inhibited growth: extracted five-choice text-radio templates.

Source math basis 1356. No database access. Templates retain original sentences,
math line order, numeric formatting, and field shape. Unknown-intent empirical
banks are EXPLICIT replay profiles only; defaults derive four method mistakes.
The evidence directory records extraction, recipes, original fidelity and native
checks. Explicit inputs are validated without resampling. Stop at guide step 7.
"""
from __future__ import annotations
import argparse, hashlib, json, random, re, uuid
from pathlib import Path
import sympy as sp
KP_ID=17592186124675
ROOT=Path(__file__).with_suffix('')
SOURCE=json.loads((ROOT/'source.json').read_text())
VERSION='inhibited-growth-1'
TITLE=SOURCE['record'][':knowledge-point/title']
NAMESPACE=uuid.UUID(SOURCE['record'][':knowledge-point/id'])
# ============================================================================
# Shared exact model and output helpers
# ============================================================================
def round_nearest(x): return int(sp.floor(sp.N(x,40)+sp.Rational(1,2)))
def tex(x):
 x=sp.sympify(x)
 if x.is_Rational and x.q!=1:
  if (x.q%2==0 or x.q%5==0) and float(x)*1000==int(float(x)*1000): return str(float(x)).rstrip('0').rstrip('.')
 return str(x) if x.is_Integer else sp.latex(x)
def frac(x):
 x=sp.Rational(x); return r'\frac{'+str(x.p)+'}{'+str(x.q)+'}'
def decimal(x,digits):
 return f'{float(sp.floor(sp.N(x,40)*10**digits))/10**digits:.{digits}f}'
def model(p):
 p={k:sp.Rational(str(v)) for k,v in p.items()}
 a=p['a']; n=p['n0'] if 'n0' in p else p['n1']; t0=p.get('t1',sp.S.Zero)
 if 'k' in p: k=p['k']
 else:
  t2=p.get('t2',p.get('tau')); n2=p['n2'] if 'n2' in p else p['n1']
  k=sp.log((a-n)/(a-n2))/(t2-t0)
 K=sp.simplify((a-n)*sp.exp(k*t0))
 result=sp.simplify(a-K*sp.exp(-k*p['time'])) if 'time' in p else sp.log(K/(a-p['target']))/k
 return {**p,'kval':k,'K':K,'D1':a-p.get('n1',n),'D0':a-n,'D2':a-p.get('n2',n),'DT':a-p.get('target',n),'delta':p.get('t2',0)-t0,'result':result,'answer':round_nearest(result)}
TEMPLATES=json.loads((ROOT/'templates.json').read_text()) if (ROOT/'templates.json').exists() else {}
def render(s,c):
 def repl(m):
  mode,expr=m.group(1).split(':',1); value=sp.sympify(expr,locals=c)
  if mode=='f':return frac(value)
  if mode=='r':return str(sp.Rational(value))
  if mode.startswith('d'):return decimal(value,int(mode[1:]))
  if mode=='i':return str(round_nearest(value))
  out=tex(value)
  if mode=='g' and value.is_Integer:out=f'{int(value):,}'.replace(',',r'\,')
  if mode=='c' and value.is_Integer:out=f'{int(value):,}'
  return out
 return re.sub(r'@@(.*?)@@',repl,s)
def validate_parameters(spec,p):
 expected=set(spec['parameters'])
 if set(p)!=expected:raise ValueError(f'Expected parameters {sorted(expected)}')
 c=model(p); a=c['a']; n=c.get('n0',c.get('n1'))
 if not 0<=n<a or not 0<c['K']<=a or c['kval']<=0:raise ValueError('Requires k>0 and 0<=population<a')
 if 'n2' in c and not 0<c['t1']<c['t2'] or 'n2' in c and not n<c['n2']<a:raise ValueError('Invalid observation order')
 if 'tau' in c and not c['tau']>0 or 'tau' in c and not n<c['n1']<a:raise ValueError('Invalid observation')
 if 'target' in c and not c.get('n2',c.get('n1',n))<c['target']<a:raise ValueError('Target must lie above observed values below capacity')
 if 'time' in c and c['time']<=c.get('t2',0):raise ValueError('Evaluation must follow observations')
 # Extracted hard algebra shape keeps t1/delta fixed: integer or square root K.
 if spec['shape']=='hard_value' and c['t2']!=2*c['t1']:raise ValueError('Hard-value template requires t2=2t1')
 if spec['shape']=='hard_time' and (c['t2']!=3*c['t1'] or not sp.sqrt(c['D0']/c['D2']).is_Rational):raise ValueError('Hard-time requires t2=3t1 and rational sqrt deficit ratio')
 if spec['shape']=='volume' and c['n0']!=a/2:raise ValueError('Volume skeleton requires n0=a/2')
 if spec['shape']=='soda' and (c['n0']!=a-c['n1'] or c['n1']!=a-c['n0']):raise ValueError('Soda skeleton keeps matching observation/initial deficits')
 return c

def wrong_operations(c):
 a,K,k=c['a'],c['K'],c['kval']
 if 'time' in c:
  t=c['time']; n=c.get('n0',c.get('n1'))
  return [('use_initial_as_integration_constant',a-n*sp.exp(-k*t)),('omit_initial_deficit',a*(1-sp.exp(-k*t))),('omit_time_from_exponent',a-K*sp.exp(-k)),('treat_quantity_as_exponential_decay',n*sp.exp(-k*t))]
 y=c['target']; n=c.get('n0',c.get('n1')); t0=c.get('t1',0)
 return [('omit_division_by_rate',sp.log(K/(a-y))),('use_target_ratio_instead_of_deficit',sp.log(y/n)/k),('linearize_exponential',(y-n)/(k*(a-n))+t0),('replace_logarithm_by_one',1/k)]
def bank(spec,c,profile):
 correct=c['answer']
 if profile=='authored_operations':
  rows=[('correct',c['result'])]+wrong_operations(c)
 else:
  if profile!=spec['source_id']+'_empirical':raise ValueError('Profile does not belong to selected template')
  # Explicit unknown-intent numerical replay: scale original rounded option by
  # the ratio of independently computed rounded answers. NEVER a default bank.
  original=model(spec['parameters'])['answer']
  rows=[('correct',c['result']) if v==original else ('empirical_unknown_intent_'+str(v),sp.Rational(v,original)*correct) for v in spec['bank']]
 rounded=[round_nearest(v) for _,v in rows]
 if any(not v.is_real or not v.is_finite or v<0 for _,v in rows):raise ValueError('Reject complete nonphysical bank')
 if 'time' in c and (any(v>=c['a'] for _,v in rows) or any(v>round_nearest(c['a']) for v in rounded)):raise ValueError('Reject capacity-violating bank')
 if len(set(rounded))!=5 or rounded.count(correct)!=1:raise ValueError('Reject complete ambiguous bank')
 return rows,rounded

def sample(spec,rng,profile='authored_operations'):
 p=dict(spec['parameters']); shape=spec['shape']
 if profile!='authored_operations':
  # Explicit replay-bank variants scale quantities and time units together.
  # This keeps the original dimensionless decay ratio, avoiding unsupported
  # empirical extrapolation beyond the observed physical bank conditions.
  quantity_scale=rng.randint(2,4);time_scale=rng.randint(2,4)
  for key,value in p.items():
   if key in ('a','n0','n1','n2','target'):p[key]=str(sp.Rational(str(value))*quantity_scale)
   elif key in ('time','tau','t1','t2'):p[key]=str(sp.Rational(str(value))*time_scale)
   elif key=='k':p[key]=str(sp.Rational(str(value))/time_scale)
  return p
 if shape=='school':
  p.update(a=rng.randrange(1000,4001,100),n0=rng.randrange(100,901,50),k=str(sp.Rational(rng.randint(10,40),1000)),time=rng.randint(2,12))
 elif shape=='volume':
  a=rng.choice([3,4,5,6,8]);p.update(a=a,n0=str(sp.Rational(a,2)),target=str(sp.Rational(a,2)+sp.Rational(a,rng.choice([4,5]))),k=str(sp.Rational(rng.randint(1,6),10)))
 elif shape=='soda':
  a=rng.randint(20,35);n0=rng.randint(3,8);p.update(a=a,n0=n0,n1=a-n0,tau=rng.randint(3,10),target=a-rng.randint(1,n0-1))
 elif shape=='moderate':
  a=rng.randrange(800,2401,100);n0=rng.randrange(50,a//3,50);n1=rng.randrange(n0+100,a*2//3,50);target=rng.randrange(max(n1+50,((a*2//3+49)//50)*50),a,50)
  p.update(a=a,n0=n0,n1=n1,tau=rng.randint(3,12),target=target)
 else:
  a=rng.randrange(500,1201,100);t1=rng.randint(2,6);D1=rng.choice([100,120,180,200]);D2=rng.choice([40,50,60,80]);
  if shape=='hard_time':D1,D2=rng.choice([(180,80),(200,50),(100,25),(160,40),(225,81)])
  p.update(a=a,n1=a-D1,n2=a-D2,t1=t1,t2=t1*(3 if shape=='hard_time' else 2))
  if 'time' in p:p['time']=rng.randint(6,14)*t1
  else:p['target']=a-rng.choice([10,20,30])
 return p

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Only observed radio fields are supported')
 if profile and profile!='authored_operations':
  if profile not in [n+'_empirical' for n in TEMPLATES]:raise ValueError('Unknown complete bank profile')
  implied=profile.removesuffix('_empirical')
  if template and template!=implied:raise ValueError('Template/profile mismatch')
  template=implied
 eligible=[n for n,s in TEMPLATES.items() if s['level']==level]
 if level not in ('easy','moderate','hard') or template and template not in eligible:raise ValueError('Invalid level/template')
 rng=random.Random(seed); name=template or rng.choice(eligible);spec=TEMPLATES[name];profile=profile or 'authored_operations'
 for attempt in range(200):
  p=dict(parameters) if parameters is not None else sample(spec,rng,profile)
  try:c=validate_parameters(spec,p);rows,values=bank(spec,c,profile)
  except ValueError:
   if parameters is not None:raise
   continue
  problem=render(spec['prompt'],c); solution=render(spec['solution'],c)
  if 'time' not in c:
   for singular,plural in [('minute','minutes'),('hour','hours'),('day','days')]:
    solution=solution.replace(r'\text{'+(singular if c['answer']!=1 else plural)+'}',r'\text{'+(plural if c['answer']!=1 else singular)+'}')
  strings=[spec['choice_pattern'].replace('@@value@@',str(v)) for v in values]
  if 'time' not in c and spec['shape']!='hard_time':
   plural={'volume':'minutes','soda':'minutes'}.get(spec['shape'],'hours' if name=='q-335578' else 'days')
   singular={'minutes':'minute','hours':'hour','days':'day'}[plural]
   strings=[f'${v}$ '+(singular if v==1 else plural) for v in values]
  if spec['shape']=='hard_time':
   def suffix(v):return 'th' if abs(v)%100 in (11,12,13) else {1:'st',2:'nd',3:'rd'}.get(abs(v)%10,'th')
   strings=[f'${v}\\text{{{suffix(v)}}}$ day' for v in values]
  canonical={'level':level,'template':name,'parameters':{k:str(sp.Rational(str(v))) for k,v in sorted(p.items())},'profile':profile,'bank':sorted(strings),'problem':problem,'solution':solution}
  digest=hashlib.sha256(json.dumps(canonical,sort_keys=True).encode()).hexdigest(); qid=uuid.uuid5(NAMESPACE,digest);fid=uuid.uuid5(qid,'selection')
  answers=[{':answer/id':str(uuid.uuid5(fid,value)),':answer/type':':answer.type/text',':answer/value':value} for value in strings]
  correct=next(a[':answer/id'] for a,v in zip(answers,values) if v==c['answer']);random.Random(seed).shuffle(answers)
  return {'knowledge_point':{'db_id':KP_ID,'id':str(NAMESPACE),'title':TITLE},'question':{':question/id':str(qid),':question/difficulty':':question.difficulty/'+level,':question/problem':problem,':question/worked-solution':solution,':question/answer-fields':[{':answer-field/id':str(fid),':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]}]},'generation':{'version':VERSION,'seed':seed,'template':name,'parameters':p,'profile':profile,'bank_origin':'authored' if profile=='authored_operations' else 'observed empirical; intent unknown','parameter_fingerprint':hashlib.sha256(json.dumps(canonical['parameters'],sort_keys=True).encode()).hexdigest(),'content_fingerprint':digest,'source':{k:SOURCE[k] for k in ['database','basis','lineage']},'source_id':spec['source_id'],'authored_level':name=='q-37389','plot_rating':'none','domain':'t>=0, k>0, 0<=quantity<a','calculations':{k:str(v) for k,v in c.items()},'recipes':[{'name':r,'expression':str(v),'rounded':round_nearest(v)} for r,v in rows]}}
 raise ValueError('No valid complete bank in bounded sampling')
# EASY: supplied equation; known rate or one calibration; three observed layouts.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE: infer equation, initial deficit, calibrate rate, solve target time.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# HARD: two nonzero observations; ratio to find rate, then recover K and evaluate.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)
def markdown(r):
 q=r['question']; f=q[':question/answer-fields'][0]
 return '\n\n'.join([q[':question/problem'],'\n'.join('- '+a[':answer/value']+(' **correct**' if a[':answer/id']==f[':answer-field/correct'][1] else '') for a in f[':answer-field/choices']),q[':question/worked-solution']])
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['json','markdown'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');a=ap.parse_args()
 if a.count<1:ap.error('positive count required')
 levels=['easy','moderate','hard'] if a.difficulty=='all' else [a.difficulty]
 records=[generate(l,a.seed+i,template=a.template,profile=a.profile) for l in levels for i in range(a.count)]
 print(json.dumps(records,indent=2,ensure_ascii=False) if a.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
if __name__=='__main__':main()
