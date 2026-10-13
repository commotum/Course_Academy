#!/usr/bin/env python3
"""Constant-volume dilution. Frozen math basis 1356; stops at step 7.

Normal easy: construct/solve Q(t) from equal rates (observed expression layout).
Normal moderate: same construction, then Q(T) rounded to two decimals (observed).
Authored hard: moderate demand with feed concentration in g/L and amount in kg;
a single declared unit conversion, supported by the lesson introduction in grams.
No changing volume, overflow, target-time inversion, or extra differential method.

Observed masks and complete banks are explicit public ineligible evidence profiles.
Opaque historical coefficients are scaled by dimensional similarity; their error
operations are NOT claimed recovered. Defaults instead use complete method-derived
five-option banks and reject an entire instance on collisions. Raw omissions remain
omissions. JSON is local review data; this module has no database dependencies.
"""
from __future__ import annotations
import argparse,hashlib,json,random,re,sys,uuid
from pathlib import Path
import sympy as sp
KP_ID=17592186229181
KP_UUID='1403309b-bb10-5ce3-bd8f-97915bb837ca'
TITLE='Constructing and Solving a Dilution Model: Inflow Equals Outflow'
VERSION='equal-flow-dilution-1'
DIR=Path(__file__).with_suffix('')
MASKS=json.loads((DIR/'masks.json').read_text())
T=sp.Symbol('t',real=True)
LEVELS=('easy','moderate','hard')
CONTEXTS={
 'coolant':('coolant tank','tank','liquid','additive'),
 'disinfectant':('storage tank','tank','liquid','disinfectant'),
 'dye':('dye vat','vat','liquid','dye'),
 'supplement':('nutrient-mixing tank','tank','solution','supplement'),
 'sugar':('brewing tank','tank','liquid','sugar'),
 'salt':('fish hatchery tank','tank','water','salt'),
 'pollutant':('wastewater basin','basin','water','pollutant')}
def rat(v):return sp.Rational(str(v))
def num(v):
 v=sp.Rational(v)
 if v.q==1:return str(v.p)
 # All rendered decimal slots use terminating rational inputs.
 d=v.q
 for prime in (2,5):
  while d%prime==0:d//=prime
 if d!=1:return sp.latex(v)
 return format(float(v),'.10f').rstrip('0').rstrip('.')
def rounded(v):return format(float(sp.N(v,30)),'.2f')
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
def uid(v):return str(uuid.uuid5(uuid.NAMESPACE_URL,'equal-flow:'+v))
def fill(mask,values):
 def f(m):
  if m.group(1) not in values:raise ValueError('unmapped mask '+m.group(1))
  return str(values[m.group(1)])
 return re.sub(r'⟦([^⟧]+)⟧',f,mask)
def expr_tex(E,A,k,t='t',braced=False):
 e='{e}' if braced else 'e'
 coefficient='' if abs(A)==1 else num(abs(A))
 exponent=('-' if k>0 else '')+str(t)+'/'+num(1/abs(k))
 return num(E)+('+' if A>0 else '-')+coefficient+e+'^{'+exponent+'}'
def full(record,level,template,profile,p,values,correct,solution,prompt,raw=False,presence=None,recipes=None):
 q={':question/problem':prompt}
 if solution is not None:q[':question/worked-solution']=solution
 if presence is None or presence['difficulty_present']:q[':question/difficulty']=':question.difficulty/'+level
 identity=digest({'version':VERSION,'question':q,'bank':sorted(values),'correct':values[correct] if correct is not None else None})
 q[':question/id']=uid(identity)
 fieldid=uid(identity+':selection')
 answers=[{':answer/id':uid(fieldid+':'+v),':answer/type':':answer.type/math',':answer/value':v} for v in values]
 f={':answer-field/id':fieldid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers}
 if correct is not None:f[':answer-field/correct']=[':answer/id',answers[correct][':answer/id']]
 random.Random(record).shuffle(answers)
 q[':question/answer-fields']=[f]
 math_params=({'equilibrium':str(p['V']*p['c']),'removal_coefficient':str(p['r']/p['V']),'initial_amount':str(p['q0']),**({'time':str(p['time'])} if 'time' in p else {})} if not raw else {k:str(v) for k,v in p.items()})
 task=digest({'model':'constant-volume','demand':level,'parameters':math_params})
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':record,'template':template,'profile':profile,'parameters':{k:str(v) for k,v in p.items()},'mathematical_fingerprint':task,'content_fingerprint':identity,'source':{'database':'math','basis':1356,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'},'evidence_only':raw,'eligible_for_learning':not raw,'origin':'observed dimensional-similarity evidence' if raw else ('authored missing-level extension' if level=='hard' else 'observed layout, authored complete bank'),'recipes':recipes or [],'domain':'t >= 0; positive constant volume; equal inflow/outflow; homogeneous mixture','dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__}}}
def replay(level,seed,template,profile,parameters):
 sid=template.removeprefix('source_')
 if sid not in MASKS:raise ValueError('unknown source template')
 s=MASKS[sid]
 if level!=s['level']:raise ValueError('source level mismatch; unrated source assignment is authored')
 if profile not in (None,'raw_'+sid):raise ValueError('source requires complete original bank')
 p={'mass_scale':'1','flow_scale':'1'} if parameters is None else parameters
 if set(p)!={'mass_scale','flow_scale'}:raise ValueError('raw replay accepts dimensional mass_scale and flow_scale only')
 m,f=rat(p['mass_scale']),rat(p['flow_scale'])
 if not (1<=m<=4 and m.q==1 and 1<=f<=3 and f.q==1):raise ValueError('raw dimensional scale outside documented bounds')
 b=s['base'];V=rat(b['V'])*f;r=rat(b['r'])*f;c=rat(b['c'])*m/f;q0=rat(b['q0'])*m;E=V*c;B=q0-E;time=rat(b['T']) if b['T'] else None
 val={'V':num(V),'r':num(r),'c':num(c),'q0':num(q0),'E':num(E),'F':num(r*c),'F_fraction':sp.latex(r*c),'B':num(B),'absB':num(abs(B)),'Bterm':('+' if B>0 else '-')+('' if abs(B)==1 else num(abs(B))),'T':num(time) if time else ''}
 if time:val['rounded']=rounded(E+B*sp.exp(-r*time/V))
 values=[]
 for a in s['bank']:
  v={'mass_'+str(i):num(rat(x)*m) for i,x in enumerate(a['mass_values'])}
  if time:
   original_correct=rounded((E+B*sp.exp(-r*time/V))/m)
   v['mass_0']=val['rounded'] if a['mass_values'][0]==original_correct else format(float(rat(a['mass_values'][0])*m),'.2f')
  values.append(fill(a['mask'],v))
 solution=fill(s['solution_mask'],val) if s['solution_mask'] is not None else None
 out=full(seed,level,template,'raw_'+sid,{'mass_scale':m,'flow_scale':f},values,s['correct_index'] if s['has_correct'] else None,solution,fill(s['prompt_mask'],val),raw=True,presence=s,recipes=['opaque observed dimensional scaling; no inferred error intent'])
 mathp={'equilibrium':str(E),'removal_coefficient':str(r/V),'initial_amount':str(q0)}
 if time:mathp['time']=str(time)
 out['generation']['mathematical_fingerprint']=digest({'model':'constant-volume','demand':level,'parameters':mathp})
 return out
def check_params(level,p):
 keys={'V','r','c','q0','context'}|({'time'} if level!='easy' else set())
 if set(p)!=keys:raise ValueError('parameters must be '+str(sorted(keys)))
 p={k:(v if k=='context' else rat(v)) for k,v in p.items()}
 if p['context'] not in CONTEXTS:raise ValueError('unknown context')
 V,r,c,q0=p['V'],p['r'],p['c'],p['q0']
 if not (300<=V<=1000 and V.q==1 and 10<=r<=50 and r.q==1 and 10<=V/r<=80 and (V/r).q==1 and sp.Rational(1,100)<=c<=sp.Rational(6,100) and (100*c).q==1 and 1<=q0<=25 and q0.q==1):raise ValueError('outside equal-flow arithmetic bounds')
 E=V*c
 if q0==E or q0>=2*E:raise ValueError('non-equilibrium initial amount must be below twice feed equilibrium')
 if level!='easy' and not (2<=p['time']<=12 and p['time'].q==1):raise ValueError('evaluation time outside [2,12] integer minutes')
 return p
def sample(level,rng):
 # Each candidate is a whole bank; no replacement of individual options.
 r=rng.choice([10,12,15,20,25,30,40,50]);tau=rng.choice([10,12,14,15,16,20,24,25,30,35,40,50,60,70,80]);V=r*tau
 p={'V':V,'r':r,'c':sp.Rational(rng.randint(1,6),100),'q0':rng.randint(1,25),'context':rng.choice(list(CONTEXTS))}
 if level!='easy':p['time']=rng.randint(2,12)
 return check_params(level,p)
def make(level,seed,template,p,profile):
 V,r,c,q0=p['V'],p['r'],p['c'],p['q0'];E=V*c;A=q0-E;k=r/V
 name,container,liquid,substance=CONTEXTS[p['context']]
 unit_c='g/L' if level=='hard' else 'kg/L';display_c=c*1000 if level=='hard' else c
 prompt=rf'A {name} initially holds ${num(V)}\,\text{{L}}$ of {liquid} containing ${num(q0)}\,\text{{kg}}$ of dissolved {substance}.'+'\n'+rf'A feed solution containing ${num(display_c)}\,\text{{{unit_c}}}$ of the {substance} is pumped into the {container} at a rate of ${num(r)}\,\text{{L/min}},$ while the completely mixed liquid is drained out at a rate of ${num(r)}\,\text{{L/min}}.$'
 if level=='easy':prompt+=rf' Which expression gives the amount of {substance} $Q(t),$ in kilograms, in the {container} $t$ minutes after pumping begins?'
 else:prompt+='\n'+rf'Find, rounded to two decimal places, the amount of {substance} in the {container} ${num(p["time"])}$ minutes after pumping begins.'
 # All options follow operations from the displayed linear ODE, chosen as one bank.
 models=[(E,A,k),(E/2,q0-E/2,2*k),(2*E,q0-2*E,k/2),(r*c,q0-r*c,k),(E,-A,k)]
 if any(a==0 for _,a,_ in models):raise ValueError('zero complementary term in complete bank')
 recipes=['solve IVP','add equal inflow and outflow as mass-removal rates then solve the erroneous IVP','double the mixed-volume denominator then solve the erroneous IVP','use forcing as particular constant without dividing by coefficient','reverse initial-condition subtraction']
 functions=[e+a*sp.exp(-rate*T) for e,a,rate in models]
 if any(sp.expand(a-b)==0 for i,a in enumerate(functions) for b in functions[:i]):raise ValueError('ambiguous complete function bank')
 if level=='easy':values=['Q(t)='+expr_tex(*model) for model in models]
 else:
  ts=p['time'];vals=[rounded(x.subs(T,ts)) for x in functions]
  if len(set(vals))!=5 or any(float(x)<=0 for x in vals):raise ValueError('invalid complete rounded bank')
  # A common number-form prevents correct-answer length from identifying the key.
  if len({len(v.split('.')[0]) for v in vals})!=1:raise ValueError('unequal numeric-option number forms')
  values=[v+r'\,\text{kg}' for v in vals]
 # Shared full source solution mask; vary complete mathematical components and context.
 sourceid='17592186377286' if A>0 and level!='easy' else ('17592186377242' if level!='easy' else '17592186377279')
 s=MASKS[sourceid];v={'V':num(V),'r':num(r),'c':num(c),'q0':num(q0),'E':num(E),'F':num(r*c),'F_fraction':sp.latex(r*c),'B':num(A),'absB':num(abs(A)),'Bterm':('+' if A>0 else '-')+('' if abs(A)==1 else num(abs(A))),'T':num(p.get('time',0)),'rounded':values[0].split('\\')[0] if level!='easy' else ''}
 solution=fill(s['solution_mask'],v)
 oldtau=num(rat(s['base']['V'])/rat(s['base']['r']))
 # Only denominator/exponent components are replaced; fixed numbers never global slots.
 solution=solution.replace('/'+oldtau+'}', '/'+num(1/k)+'}').replace('{'+oldtau+'}', '{'+num(1/k)+'}')
 # Replace whole final expressions, including coefficient omission/sign conditions.
 solution=re.sub(r'Q\(t\)=[0-9][^\n]+(?=\n\$\$)', 'Q(t)='+expr_tex(E,A,k,braced=True)+('.' if level=='easy' else ''),solution)
 if level!='easy':
  solution=re.sub(r'Q\('+re.escape(num(p['time']))+r'\)=[^\n]+(?=\n\$\$)',lambda _: 'Q('+num(p['time'])+')='+expr_tex(E,A,k,num(p['time']),True)+'≈'+values[0]+',',solution)
 for old,new in [('supplements enter',substance+' enters'),('supplements leave',substance+' leaves'),('supplements exit',substance+' exits'),('supplement',substance),('sugar',substance),('dye',substance)]:
  solution=re.sub(r'\b'+old+r'\b',new,solution)
 solution=solution.replace('additives enter',substance+' enters').replace('additives exit',substance+' exits')
 solution=re.sub(r'\bvat\b',container,solution);solution=re.sub(r'\btank\b',container,solution)
 if level=='hard':
  conversion=rf'The feed concentration must use kilograms: ${num(display_c)}\,\text{{g/L}}\cdot\frac{{1\,\text{{kg}}}}{{1000\,\text{{g}}}}={num(c)}\,\text{{kg/L}}.$'+'\n\n'
  solution=conversion+solution
 return full(seed,level,template,profile,p,values,0,solution,prompt,recipes=recipes)
def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in LEVELS:raise ValueError('unknown difficulty')
 if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('this KP observes radio only')
 if profile and profile.startswith('raw_') and template is None:template='source_'+profile[4:]
 if template and template.startswith('source_'):return replay(level,seed,template,profile,parameters)
 expected={'easy':'expression','moderate':'amount','hard':'amount_unit_conversion'}[level]
 if template not in (None,expected):raise ValueError('template/difficulty mismatch')
 if profile not in (None,'method_bank'):raise ValueError('unsupported complete bank')
 rng=random.Random(seed)
 for _ in range(2000):
  try:return make(level,seed,expected,check_params(level,parameters) if parameters is not None else sample(level,rng),'method_bank')
  except ValueError:
   if parameters is not None:raise
 raise ValueError('unable to sample eligible whole bank')
# EASY: observed function selection; complete constant-coefficient IVP.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE: observed IVP plus finite-time substitution and rounding.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# HARD: authored unit bookkeeping followed by precisely the moderate IVP method.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)
def markdown(record,label='GENERATED VARIANT'):
 q=record['question'];lines=[f'## {label}: {record["generation"]["template"]}',q[':question/problem'],'']
 for f in q.get(':question/answer-fields',[]):
  correct=f.get(':answer-field/correct',[None,None])[1]
  for a in f[':answer-field/choices']:lines.append('- $'+a[':answer/value']+'$'+(' [correct]' if a[':answer/id']==correct else ''))
 if ':question/worked-solution' in q:lines+=['',q[':question/worked-solution']]
 else:lines+=['','[Original worked solution omitted.]']
 if record['generation']['evidence_only']:lines+=['','**Evidence only; ineligible for learning.**']
 return '\n'.join(lines)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=(*LEVELS,'all'),default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=('markdown','json'),default='markdown');ap.add_argument('--template');ap.add_argument('--profile');a=ap.parse_args()
 if a.count<1:ap.error('count must be positive')
 records=[generate(level,a.seed+i,a.template,profile=a.profile) for level in (LEVELS if a.difficulty=='all' else [a.difficulty]) for i in range(a.count)]
 print(json.dumps(records,indent=2,ensure_ascii=False) if a.format=='json' else '\n\n'.join(markdown(r,'ORIGINAL PROFILE REPLAY' if r['generation']['evidence_only'] else 'GENERATED VARIANT') for r in records))
if __name__=='__main__':main()
