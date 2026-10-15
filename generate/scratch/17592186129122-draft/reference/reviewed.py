#!/usr/bin/env python3
"""Period-only generator, frozen math capture 1356; steps 3–7 local review.

Eight observed source masks are unordered easy peers. Historical scalar banks
have no recovered error intention and are public evidence-only profiles. Default
banks apply actual frequency/base-period operations to the complete instance.
No EDB access, registration, writes, plots or question-source lookup shortcuts.
"""
from __future__ import annotations
import argparse, hashlib, json, math, pathlib, random, sys, uuid
import sympy as sp
HERE=pathlib.Path(__file__).with_suffix(''); VERSION='period-1356-v1'
CAPTURE=json.loads((HERE/'source.json').read_text()); SPECS=json.loads((HERE/'template-masks.json').read_text())
KP={'db_id':17592186129122,'id':'1eeb42af-74ee-53d7-af9f-be171f77968f','title':'Calculating the Period of a Transformed Sinusoidal Function'}
LEVELS=('easy','moderate','hard'); TEMPLATES={**{n:'easy' for n in SPECS},'signed_frequency':'moderate','factored_frequency':'hard'}
class SampleRejected(ValueError): pass

def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
def uid(v):return str(uuid.uuid5(uuid.NAMESPACE_URL,VERSION+':'+v))
def rat(n,d=1):return sp.Rational(n,d)
def texr(v):
 v=sp.Rational(v);n,d=int(v.p),int(v.q)
 return str(n) if d==1 else ('-' if n<0 else '')+r'\frac{'+str(abs(n))+'}{'+str(d)+'}'
def texperiod(v,unit,mode=None):
 v=sp.Rational(v);n,d=int(v.p),int(v.q)
 if unit=='degree':return '{'+texr(v)+'}^{∘}'
 if mode=='unicode_fraction':return r'\frac{'+str(n)+'}{'+str(d)+'}π'
 if mode in ('unicode_integer','pi_integer') and d!=1:raise ValueError('Integer source-option mask requires integer scalar')
 if mode=='unicode_integer':return ('' if n==1 else str(n))+'π'
 if mode=='pi_integer':return ('' if n==1 else str(n))+r'\pi '
 if d==1:return ('' if n==1 else str(n))+r'\pi '
 return r'\frac{'+('' if n==1 else str(n))+r'\pi }{'+str(d)+'}'
def unpack(p):return tuple(rat(p[n+'_n'],p[n+'_d']) for n in ('a','b','c'))
def allowed_frequencies(style):
 if style=='integer':return [(n,1) for n in range(3,13)]
 return [(n,d) for n in range(1,13) for d in range(2,7) if math.gcd(n,d)==1 and rat(n,d) not in (rat(1,2),1,2)]
RATIONAL_DOMAIN=allowed_frequencies('fraction')

def validate_parameters(level,name,p,raw=False):
 expected={k for n in ('a','b','c') for k in (n+'_n',n+'_d')}
 if level=='hard':expected|={'k','unit','trig'}
 if level=='moderate':expected|={'unit','trig'}
 if raw:expected|={f'o{i}_{t}' for i in range(len(SPECS[name]['banks'])) for t in ('n','d')}
 if set(p)!=expected:raise ValueError('Exact parameter keys required: '+str(sorted(expected)))
 for key,v in p.items():
  if key in ('unit','trig'):continue
  if not isinstance(v,int) or isinstance(v,bool):raise ValueError('Integer components required')
 for n in ('a','b','c'):
  if p[n+'_d']<=0 or math.gcd(p[n+'_n'],p[n+'_d'])!=1:raise ValueError('Reduced positive-denominator rational required')
 a,b,c=unpack(p)
 if a==0 or abs(a)>6 or p['a_d']>6:raise ValueError('Amplitude scope')
 if b==0 or abs(b)>12 or abs(p['b_n'])>12 or p['b_d']>(12 if level=='hard' else 6):raise ValueError('Frequency scope')
 if abs(c)>90 or p['c_d']>6:raise ValueError('Shift scope')
 if level=='easy':
  s=SPECS[name]
  if b<=0:raise ValueError('Easy frequency is positive')
  if s['bstyle']=='integer' and p['b_d']!=1:raise ValueError('Integer-frequency family')
  if s['bstyle']!='integer' and p['b_d']==1:raise ValueError('Rational-frequency family')
  if s['a_style']=='unit' and a!=1:raise ValueError('Unit-amplitude mask')
  if s['a_style']=='fraction' and not 0<a<1:raise ValueError('Proper amplitude fraction')
  if s['a_style']=='integer' and p['a_d']!=1:raise ValueError('Integer-amplitude mask')
  if name=='rad_cos_fraction' and c!=0:raise ValueError('No shift in this mask')
  if name!='rad_cos_fraction' and c==0:raise ValueError('Nonzero shifted mask')
 elif level=='moderate':
  if b>=0 or p['b_d']==1:raise ValueError('Moderate requires negative noninteger reduced B')
 elif level=='hard':
  if b>=0 or p['b_d']==1 or not 2<=p['k']<=6 or math.gcd(p['k'],p['b_d'])<=1 or (b*p['k']).q==1:
   raise ValueError('Hard requires negative noninteger fraction, 2..6 multiplier, cancellation and noninteger product')
  if abs(p['b_n'])>12 or abs(b*p['k'])>12 or abs((b*p['k']).p)>60:raise ValueError('Hard arithmetic ceiling')
 if level!='easy' and (p['unit'] not in ('rad','degree') or p['trig'] not in ('sin','cos') or c==0):raise ValueError('Authored unit/function/nonzero shift')
 if raw:
  for i in range(len(SPECS[name]['banks'])):
   if p[f'o{i}_d']<=0 or p[f'o{i}_n']<=0:raise ValueError('Evidence options positive')


def substitutions(s,p):
 a,b,c=unpack(p);bn,bd=p['b_n'],p['b_d'];an,ad=p['a_n'],p['a_d']
 bx=str(bn)+'x' if bd==1 else r'\frac{'+str(bn)+'x}{'+str(bd)+'}' if s['bstyle']=='fraction' else texr(b)+'x'
 ac=texr(a);ct=(('+' if c>0 else '-')+(texperiod(abs(c),'degree') if s['unit']=='degree' else texperiod(abs(c),'rad'))) if c else ''
 base=360 if s['unit']=='degree' else 2;value=rat(base)/b
 btex=texr(b);den=btex if bd==1 else '('+btex+')'
 stage=(r'\frac{{360}^{∘}}{'+den+'}' if s['unit']=='degree' else r'\frac{2\pi }{'+den+'}')+'='+texperiod(value,s['unit'])+'.'
 return {'A':ac,'BX':bx,'C':ct,'B':btex,'PERIOD_STAGE':stage}
def mask(text,slots):
 if text is None:return None
 for k,v in slots.items():text=text.replace('@'+k+'@',v)
 if '@' in text:raise ValueError('Unfilled complete component')
 return text

def authored_solution(unit,trig,b,B,hard,k=None):
 base=r'{360}^{∘}' if unit=='degree' else r'2\pi '
 intro='Given a function in the form $y=A\\'+trig+'(Bx+C)+D,$ the period is $\\frac{'+base+'}{|B|}.$'
 if hard:intro+='\n\nThe coefficient of $x$ in the argument is $B=('+texr(b)+')('+str(k)+')='+texr(B)+'.$'
 intro+='\n\nIn our case, we have that $B='+texr(B)+'.$ Therefore, the period is $\\frac{'+base+'}{|'+texr(B)+'|}=\\frac{'+base+'}{'+texr(abs(B))+'}='+texperiod(rat(360 if unit=='degree' else 2)/abs(B),unit)+'.$'
 return intro

def build(level,name,p,raw):
 a,b,c=unpack(p)
 if level=='easy':
  s=SPECS[name];unit=s['unit'];trig=s['trig'];B=b;slots=substitutions(s,p)
  prompt=mask(s['prompt_mask'],slots);solution=mask(s['solution_mask'],slots)
  if not raw:
   if solution is None:solution=authored_solution(unit,trig,b,B,False)
   if name=='degree_cos_integer':solution=solution.replace('the period is ${360}^{∘}.$',r'the period is $\frac{{360}^{∘}}{B}.$')
 else:
  unit=p['unit'];trig=p['trig'];B=b*(p['k'] if level=='hard' else 1)
  ctex=(('+' if c>0 else '-')+(texperiod(abs(c),unit)))
  inside=texr(b)+('x'+ctex if level=='moderate' else r'\left('+str(p['k'])+'x'+ctex+r'\right)')
  prompt='Calculate the period of the function $f(x)='+texr(a)+'\\'+trig+r'\left('+inside+r'\right).$'
  solution=authored_solution(unit,trig,b,B,level=='hard',p.get('k'))
 base=rat(360 if unit=='degree' else 2);correct=base/abs(B)
 if raw:
  opts=[texperiod(rat(p[f'o{i}_n'],p[f'o{i}_d']),unit,z['mode']) for i,z in enumerate(SPECS[name]['banks'])]
  # Historical scalar slots describe evidence, never an inferred error operation.
  values=[rat(p[f'o{i}_n'],p[f'o{i}_d']) for i in range(len(opts))]
 else:
  # Complete bank chosen before parameters: correct, multiply by frequency,
  # tangent base-period, reciprocal twice, ignore horizontal scaling.
  values=[correct,base*abs(B),base/(2*abs(B)),2*base/abs(B),base]
  if len(set(values))!=5:raise SampleRejected('Reject complete bank: equivalent operations')
  opts=[texperiod(v,unit) for v in values]
 return prompt,solution,opts,values,correct,B,unit


def sample(level,name,rng,raw):
 if raw:return dict(SPECS[name]['source_parameters'])
 if level=='easy':
  s=SPECS[name];bn,bd=rng.choice(allowed_frequencies(s['bstyle']));a=rat(1,rng.randint(2,6)) if s['a_style']=='fraction' else rat(rng.choice([-6,-5,-4,-3,-2,2,3,4,5,6])) if s['a_style']=='integer' else rat(1)
  c=rat(0) if name=='rad_cos_fraction' else rat(rng.choice([-1,1]),rng.randint(2,6)) if s['unit']=='rad' else rat(rng.choice([-90,-60,-45,-30,-20,-15,-1,1,15,20,30,45,60,90]))
 elif level=='moderate':
  bn,bd=rng.choice(RATIONAL_DOMAIN);bn=-bn;a=rat(rng.choice([-6,-4,-3,-2,2,3,4,6]));c=rat(rng.choice([-1,1]),rng.randint(2,6));
 else:
  bn,bd,k=rng.choice(HARD_DOMAIN);a=rat(rng.choice([-6,-4,-3,-2,2,3,4,6]));c=rat(rng.choice([-1,1]),rng.randint(2,6))
 p={'a_n':int(a.p),'a_d':int(a.q),'b_n':bn,'b_d':bd,'c_n':int(c.p),'c_d':int(c.q)}
 if level!='easy':
  p.update(unit=rng.choice(['rad','degree']),trig=rng.choice(['sin','cos']))
  if p['unit']=='degree':p.update(c_n=rng.choice([-90,-60,-45,-20,20,45,60,90]),c_d=1)
 if level=='hard':p['k']=k
 return p
HARD_DOMAIN=[(-n,d,k) for n in range(1,13) for d in range(2,13) for k in range(2,7) if math.gcd(n,d)==1 and math.gcd(k,d)>1 and (rat(n*k,d)).q>1 and rat(n*k,d)<=12 and (rat(n*k,d)).p<=60]


def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in LEVELS:raise ValueError('Unknown level')
 if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Only observed radio layout')
 raw=bool(profile and profile.startswith('raw:'))
 if profile not in (None,'method') and not raw:raise ValueError('Profile must be method or raw:<source-id>')
 if raw:
  candidates=[n for n,s in SPECS.items() if s['source_id']==profile[4:]]
  if len(candidates)!=1 or level!='easy':raise ValueError('Raw profiles are source easy masks; unrated inferred API routing only')
  if template and template!=candidates[0]:raise ValueError('Profile/template mismatch')
  template=candidates[0]
 rng=random.Random(seed);eligible=[n for n,l in TEMPLATES.items() if l==level]
 name=template or rng.choice(eligible)
 if name not in eligible:raise ValueError('Template outside level')
 # A complete family/profile is selected before parameter sampling.
 profile=profile or 'method'
 for _ in range(256):
  p=dict(parameters) if parameters is not None else sample(level,name,rng,raw)
  validate_parameters(level,name,p,raw)
  try:prompt,solution,opts,values,correct,B,unit=build(level,name,p,raw)
  except SampleRejected:
   if parameters is not None:raise
   continue
  break
 else:raise SampleRejected('No collision-free whole instance')
 s=SPECS.get(name);q={':question/problem':prompt}
 if solution is not None:q[':question/worked-solution']=solution
 if not raw or ':question/difficulty' in s['keys']:q[':question/difficulty']=':question.difficulty/'+level
 hasfield=not raw or s['field'] is not None
 # Canonical task excludes trig aliases, amplitude, shift and bank; factored
 # presentation counts one frequency-recovery demand, not each spelling/product.
 task=digest({'level':level,'demand':'factor_then_period' if level=='hard' else 'signed_period' if level=='moderate' else 'direct_period','unit':unit,'B':str(B)})
 content=digest({'version':VERSION,'difficulty':q.get(':question/difficulty'),'prompt':prompt,'solution':solution,'bank':sorted(opts),'field_present':hasfield,'correct_present':not raw or (s['field'] is not None and ':answer-field/correct' in s['field']['keys'])})
 q[':question/id']=uid(content)
 if hasfield:
  field={':answer-field/id':uid(content+':selection'),':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio'}
  answers=[{':answer/id':uid(content+':selection:'+v),':answer/type':':answer.type/math',':answer/value':v} for v in opts]
  if raw:
   for ans,z in zip(answers,s['banks']):ans[':db/id']=z['db_id']
   field[':db/id']=s['field']['db_id']
  if not raw or ':answer-field/correct' in s['field']['keys']:
   matches=[i for i,v in enumerate(values) if v==correct]
   if len(matches)!=1:raise SampleRejected('Correct value not uniquely in complete bank')
   field[':answer-field/correct']=[':answer/id',answers[matches[0]][':answer/id']]
  random.Random(seed).shuffle(answers);field[':answer-field/choices']=answers;q[':question/answer-fields']=[field]
 if raw:q.update({':db/id':s['db_id'],':question/math-academy-id':s['source_id']})
 return {'knowledge_point':dict(KP),'question':q,'generation':{'version':VERSION,'python_version':sys.version.split()[0],'sympy_version':sp.__version__,'seed':seed,'template':name,'parameters':p,'bank_profile':profile,'bank_origin':'opaque source evidence' if raw and opts else 'raw fieldless evidence' if raw else 'authored method operations','evidence_only':raw,'eligible_for_learning':not raw,'authored_extension':level!='easy' or not raw,'source_analysis':{k:CAPTURE[k] for k in ('database','basis','lineage')},'source_ids':[s['source_id']] if s else ['e-15610'],'parameter_fingerprint':task,'mathematical_task_fingerprint':task,'content_fingerprint':content,'plot_rating':'none','plot_assets':{},'domain_policy':{'frequency_numerator_max':12,'frequency_denominator_max':12 if level=='hard' else 6,'frequency_magnitude_max':12,'hard_multiplier_range':[2,6] if level=='hard' else None,'mandatory_cancellation':level=='hard'},'period_coefficient':str(correct),'unit':unit,'frequency':str(B),'recipes':[] if raw else ['base/abs(B)','base*abs(B)','base/(2*abs(B))','2*base/abs(B)','base']}}

# EASY — eight observed source-shaped peers: identify positive B and divide.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE — authored negative reduced rational B, one absolute value then divide.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# HARD — authored single factored affine argument; multiply, cancel, abs, divide.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)

def markdown(r):
 q=r['question'];lines=[q[':question/problem'],'']
 for f in q.get(':question/answer-fields',[]):
  for a in f[':answer-field/choices']:lines.append('- $'+a[':answer/value']+'$'+(' (correct)' if f.get(':answer-field/correct',[None,None])[1]==a[':answer/id'] else ''))
 if ':question/worked-solution' in q:lines+=['','Worked solution:',q[':question/worked-solution']]
 return '\n'.join(lines)
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--difficulty',choices=(*LEVELS,'all'),default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=('markdown','json'),default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
 if args.count<1:ap.error('Positive count required')
 levels=LEVELS if args.difficulty=='all' else [args.difficulty]
 records=[generate(l,args.seed+i,args.template,profile=args.profile) for l in levels for i in range(args.count)]
 print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
if __name__=='__main__':main()
