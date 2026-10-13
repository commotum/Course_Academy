#!/usr/bin/env python3
"""Inhibited-growth identification, math basis1356. Steps3–7 only; no writes to EDB.

Easy: authored level for an observed unrated factored equation (one sign/cap
recognition). Moderate: observed expanded equation, recover cap by factoring.
Hard: observed IVP, additionally compare initial value to the recovered cap.
All profiles are complete five-option banks, never pooled distractor sampling.
Raw observed profiles preserve missing attributes and duplicate legacy fields.
Default profiles use actual sign/swap/nonlinearity/initial-above-cap operations.
Heterogeneous original banks are independently parameterized linear IVPs; their
relative numbers do not support inferring an original error-generation algorithm.
See private extraction and validation evidence for exact/raw vs repaired counts.
"""
from __future__ import annotations
import argparse, hashlib, json, random, uuid
from pathlib import Path
import sympy as sp
KP_ID=17592186124673
KP_UUID='ade69467-c229-509d-9bdc-b28935b2d1d8'
TITLE='Identifying Inhibited Growth Equations and Initial Value Problems'
VERSION='inhibited-identification-v1'
HERE=Path(__file__).with_suffix('')
SOURCE={'database':'math','basis':1356,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}
TEMPLATES={'factored_equation':'easy','expanded_equation':'moderate','factored_ivp':'hard','expanded_ivp':'hard'}
PROFILES={'observed_106661':'factored_equation','observed_106662':'expanded_equation','observed_106663':'factored_ivp','observed_37176':'expanded_ivp','observed_37177':'expanded_ivp','observed_37180':'expanded_ivp','authored_factored':'factored_equation','authored_expanded':'expanded_equation','authored_ivp':'factored_ivp','authored_heterogeneous_2':'expanded_ivp','authored_heterogeneous_3':'expanded_ivp'}
NS=uuid.UUID('1a2411cf-ae8a-51cf-90a6-27ac690f9794')
def uid(s):return str(uuid.uuid5(NS,s))
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':'))
def fingerprint(x):return hashlib.sha256(canonical(x).encode()).hexdigest()
def rat(x):
 if isinstance(x,bool):raise ValueError('Boolean is not a numeric parameter')
 try:return sp.Rational(str(x))
 except Exception as exc:raise ValueError('Exact rational parameter required') from exc
def fmt(x,group=False):
 x=rat(x)
 # All workload domains require terminating decimal representations.
 den=int(x.q)
 while den%2==0:den//=2
 while den%5==0:den//=5
 if den!=1:raise ValueError('Nonterminating decimal exceeds workload')
 if 10**4 % int(x.q)!=0:raise ValueError('At most four decimal places allowed')
 s=str(int(x)) if x.q==1 else str(float(x)).rstrip('0').rstrip('.')
 if group:
  left,dot,right=s.partition('.'); sign='-' if left.startswith('-') else ''; left=left.lstrip('-'); chunks=[]
  while left:chunks.insert(0,left[-3:]);left=left[:-3]
  s=sign+r'\,'.join(chunks)+(dot+right if dot else '')
  if dot and len(right)>3:s=sign+r'\,'.join(chunks)+'.'+right[:3]+r'\,'+right[3:]
 return s
def validate_parameters(template,p):
 expected={'a','k'} if template.endswith('equation') else ({'a','k','initials'} if template=='factored_ivp' else {'options'})
 if set(p)!=expected:raise ValueError(f'Parameters must be exactly {sorted(expected)}')
 if template.endswith('equation') or template=='factored_ivp':
  a,k=rat(p['a']),rat(p['k']);fmt(a);fmt(k)
  if not (2<=a<=500 and sp.Rational(1,10)<=k<=20):raise ValueError('Equation/factored-IVP bounds: 2<=a<=500, .1<=k<=20')
  if template=='factored_equation' and a==k:raise ValueError('Coefficient and cap must differ')
  if template=='expanded_equation' and (a.q!=1 or k.q!=1 or k*a>10000):raise ValueError('Moderate uses integer cap/rate and product<=10000')
  if template=='factored_ivp':
   if len(p['initials'])!=5:raise ValueError('Five initial values required')
   vals=list(map(rat,p['initials']))
   if not all(0<=x<=1000 for x in vals) or not (vals[1]>a and vals[2]<a):raise ValueError('IVP initial bounds/above-below roles violated')
   for v in vals:fmt(v)
 else:
  opts=p['options']
  if len(opts)!=5:raise ValueError('Five complete independent IVPs required')
  for o in opts:
   if set(o)!={'c','b','initial'}:raise ValueError('Each option requires c,b,initial')
   c,b,n=map(rat,(o['c'],o['b'],o['initial']))
   if not (0<abs(c)<=100000 and sp.Rational(1,10000)<=abs(b)<=40 and 0<=n<=500000):raise ValueError('Hard affine bounds exceeded')
   if c*b>=0 or not (1<=-c/b<=500000):raise ValueError('Positive capacity1..500000 and opposite coefficient signs required')
   for v in (c,b,n,-c/b):fmt(v)
  good=[i for i,o in enumerate(opts) if rat(o['b'])<0 and rat(o['initial']) < -rat(o['c'])/rat(o['b'])]
  if len(good)!=1:raise ValueError('Exactly one below-cap negative-slope IVP required')
  if any(rat(o['b'])<0 and i!=good[0] and rat(o['initial'])<=-rat(o['c'])/rat(o['b']) for i,o in enumerate(opts)):raise ValueError('All excluded negative-slope IVPs require initial strictly above capacity')
  # Fixed bank structure guarantees two or three instructive above-cap options.
  negative=sum(bool(rat(o['b'])<0) for o in opts)
  if negative not in (3,4):raise ValueError('Hard bank requires 2 or3 above-cap competitors')
 return p

def sample(template,rng,profile):
 if template=='factored_equation':return {'a':rng.randrange(10,501,10),'k':str(rng.choice([sp.Rational(1,2),1,2,3,4,5]))}
 if template=='expanded_equation':return {'a':rng.randrange(10,201,10),'k':rng.randint(2,10)}
 if template=='factored_ivp':
  a=rng.randrange(50,451,50);return {'a':a,'k':rng.randint(1,8),'initials':[str(a*sp.Rational(4,5)),str(a*sp.Rational(8,5)),str(a*sp.Rational(3,5)),str(sp.Rational(a,5)),str(a*sp.Rational(2,5))]}
 three=profile in ('authored_heterogeneous_3','observed_37177')
 roles=['below','above','reverse','above','above'] if three else ['above','reverse','reverse','below','above']
 if profile=='observed_37177':roles=['above','above','reverse','above','below']
 if profile=='observed_37180':roles=['below','reverse','reverse','above','above']
 opts=[]
 for role in roles:
  k=rng.choice(list(map(sp.Rational,['0.0002','0.003','0.005','0.02','0.03','0.1','0.5','0.6','0.8','2','3','5','8','18','22','40']))); upper=min(500000,int(100000/k)); a=sp.Rational(rng.randrange(200,min(upper,100000)+1,100)) + rng.choice([0,sp.Rational(1,2)]); a=min(a,sp.Rational(upper)); gap=rng.randrange(5,51,5)
  opts.append({'c':str(k*a if role!='reverse' else -k*a),'b':str(-k if role!='reverse' else k),'initial':str(a-gap if role=='below' else a+gap)})
 if len({tuple(str(rat(o[k])) for k in ('c','b','initial')) for o in opts})!=5:
  # Reject the complete sampled instance rather than replace a single member.
  return sample(template,rng,profile)
 return {'options':opts}

def bank(template,p,profile,legacy=False):
 d=r'\frac{dy}{dt}' if template!='expanded_ivp' else r'\frac{dP}{dt}'
 if template=='factored_equation':
  a,k=fmt(p['a']),fmt(p['k']);rhs=[f'-{k}(y + {a})',f'{a}(y + {k})',f'{a}(y - {k})',f'{k}({a} - y)',f'{k}(y - {a})']
  return [d+(' ='+r if i==0 else ' = '+r) for i,r in enumerate(rhs)],3
 if template=='expanded_equation':
  a,k=fmt(p['a']),fmt(p['k']);c=fmt(rat(p['a'])*rat(p['k']))
  rhs=[f'{k}-'+c+'y',f'{k}y-'+c,c+'-'+k+'y',f'{k}'+r'{y}^{2}-'+c,c+'-'+k+r'{y}^{2}']
  if legacy:return [d+' = '+s.replace('{y}^{2}','y^{2}').replace('-',' - ') for s in [rhs[3],rhs[0],rhs[2],rhs[1],rhs[4]]],2
  return [d+'='+s for s in rhs],2
 if template=='factored_ivp':
  a,k=fmt(p['a']),fmt(p['k']);rhs=[f'{k}(y-{a})',f'{k}({a}-y)',f'{k}({a}-y)',f'{k}y(y-{a})',f'-{k}(y+{a})']
  return [d+'='+s+r',\,y(0)='+fmt(v) for s,v in zip(rhs,p['initials'])],2
 vals=[];correct=[]
 for i,o in enumerate(p['options']):
  c,b,n=map(rat,(o['c'],o['b'],o['initial']));ct,bt=fmt(abs(c),True),fmt(abs(b),True)
  if profile=='observed_37180' and i==1:
   raw=fmt(abs(c));ct=raw[0]+r'\,'+raw[1:] if len(raw)==3 else ct
  rhs=ct+'-'+bt+'P' if b<0 else bt+'P-'+ct
  vals.append(d+'='+rhs+r',\,P(0)='+fmt(n,True))
  if b<0 and n < -c/b:correct.append(i)
 return vals,correct[0]

def formal(ivp=False,var='y'):
 return r'\frac{d'+var+r'}{dt}=k(a-'+var+')'+(r',\,'+var+r'(0)={'+var+r'}_{0}' if ivp else '')
def equation_solution(template,p,values,correct):
 a,k=fmt(p['a']),fmt(p['k']); val=values[correct]
 factoring=("To see this, let's factor the right-hand side of the equation. This gives\n\n$$\n"+r'\frac{dy}{dt}='+k+'('+a+'-y).\n$$\n\n') if template=='expanded_equation' else ''
 return 'An inhibited growth equation has the form\n\n$$\n'+formal()+',\n$$\n\nwhere $k>0$ is a constant of proportionality, and $a>y$ for all $t\\ge 0.$\n\nFrom the given options, the only inhibited growth equation is\n\n$$\n'+val+'.\n$$\n\n'+factoring+'In this case, the constant of proportionality is $k='+k+',$ and $a='+a+'.$ Note that for inhibited growth, we must have $y<'+a+'$ for all $t\\ge 0.$'
def ivp_solution(template,p,values,correct,raw=False,profile=''):
 var='y' if template=='factored_ivp' else 'P'; generic='y' if raw else var
 out='An inhibited growth initial value problem has the form\n\n$$\n'+formal(True,generic)+'\n$$\n\nwhere $k>0$ is a constant of proportionality, and $a>'+generic+'$ for all $t\\ge 0.$\n\nFrom the given options, the only inhibited growth problem is\n\n$$\n'+values[correct]+('.' if template=='factored_ivp' else ',')+'\n$$\n\n'
 if template=='factored_ivp':
  a,k,n=fmt(p['a']),fmt(p['k']),fmt(p['initials'][correct]);bad=fmt(p['initials'][1])
  return out+'In this case, $k='+k+',a='+a+',$ and ${y}_{0}='+n+'.$ Notice that $a>{y}_{0},$ which is required for inhibited growth. \n\nThe other options do not represent inhibited growth. In particular, the initial value problem\n\n$$\n'+values[1]+',\n$$\n\ndoes *not* represent inhibited growth model because ${y}_{0}='+bad+'>a='+a+'.$'
 opts=p['options'];o=opts[correct];k=fmt(-rat(o['b']),True);a=fmt(-rat(o['c'])/rat(o['b']),True);n=fmt(o['initial'],True)
 def expanded(i,with_initial=False):
  o=opts[i];k=fmt(-rat(o['b']),True);a=fmt(-rat(o['c'])/rat(o['b']),True);rhs=values[i].split(r',\,')[0]+'='+k+'('+a+'-P)'
  return rhs+(r',\,P(0)='+fmt(o['initial'],True) if with_initial else '')
 out+='since\n\n$$\n'+expanded(correct)+'.\n$$\n\nIn this case, $k='+k+',a='+a+',$ and ${y}_{0}='+n+'.$ Notice that $a>{y}_{0},$ which is required for inhibited growth. \n\nThe other options do not represent inhibited growth. In particular, the initial value problems\n\n'
 bad=[i for i,o in enumerate(opts) if rat(o['b'])<0 and i!=correct]
 if profile=='observed_37177':bad=[0,3,1]
 if len(bad)==2:bad=bad[::-1] if profile in ('observed_37176','observed_37180','authored_heterogeneous_2') else bad
 for j,i in enumerate(bad):
  if j==len(bad)-1:out+='and\n\n'
  out+='$$\n'+expanded(i,True)+(',' if j<len(bad)-1 else '')+'\n$$\n\n'
 statements=[r'${y}_{0}='+fmt(opts[i]['initial'],True)+'>a='+fmt(-rat(opts[i]['c'])/rat(opts[i]['b']),True) for i in bad]
 if len(bad)==2:tail=statements[0]+',$ and '+statements[1]+'.$'
 else:tail=statements[0]+',$ '+statements[1]+',$ and '+statements[2]+'.$'
 result=out+'do *not* represent an inhibited growth model because '+tail
 return result if raw else result.replace('{y}_{0}','{P}_{0}')

# Easy: inferred source level; factored sign/cap identification only.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# Moderate: observed expanded integer equation; factoring a single linear RHS.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# Hard: observed initial-condition comparison; no solving/integration introduced.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)
def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('Unknown level')
 if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Only radio supported')
 rng=random.Random(seed)
 if profile is not None:
  if profile not in PROFILES:raise ValueError('Unknown complete profile')
  pt=PROFILES[profile]
  if template and template!=pt:raise ValueError('Profile/template mismatch')
  template=pt
 template=template or rng.choice([t for t,l in TEMPLATES.items() if l==level])
 if template not in TEMPLATES or TEMPLATES[template]!=level:raise ValueError('Template/level mismatch')
 profile=profile or {'factored_equation':'authored_factored','expanded_equation':'authored_expanded','factored_ivp':'authored_ivp','expanded_ivp':rng.choice(['authored_heterogeneous_2','authored_heterogeneous_3'])}[template]
 p=json.loads(json.dumps(parameters)) if parameters is not None else sample(template,rng,profile)
 validate_parameters(template,p)
 if template=='expanded_ivp':
  os=p['options']; expected_negative=4 if profile in ('observed_37177','authored_heterogeneous_3') else 3
  if sum(bool(rat(o['b'])<0) for o in os)!=expected_negative:raise ValueError('Complete profile requires its fixed negative-slope count')
  if len({tuple(str(rat(o[k])) for k in ('c','b','initial')) for o in os})!=5:raise ValueError('Equivalent complete IVP options')
  if profile in ('observed_37176','observed_37177','observed_37180'):
   required={'observed_37176':3,'observed_37177':4,'observed_37180':0}[profile]
   good=[i for i,o in enumerate(os) if rat(o['b'])<0 and rat(o['initial']) < -rat(o['c'])/rat(o['b'])]
   if good!=[required]:raise ValueError('Raw profile correct-role index must be retained')
  if profile=='observed_37177' and [i for i,o in enumerate(os) if rat(o['b'])<0]!=[0,1,3,4]:raise ValueError('Raw profile role positions must be retained')
 raw=profile.startswith('observed_');values,correct=bank(template,p,profile)
 if template.endswith('equation'):
  a=fmt(p['a']);prompt=('Given that $y < '+a+'$ and $t \\ge 0$, which of the following is an inhibited growth equation?') if template=='factored_equation' else 'Given that $y<'+a+'$ and $t\\ge 0,$ which of the following is an inhibited growth equation?'
  solution=equation_solution(template,p,values,correct)
 else:prompt='Which of the following initial value problems is an inhibited growth problem?';solution=ivp_solution(template,p,values,correct,raw,profile)
 # Source missing attributes remain absent in public raw replay; normal output completes them.
 question={':question/problem':prompt}
 if profile!='observed_106661':question.update({':question/difficulty':':question.difficulty/'+level,':question/worked-solution':solution})
 elif not raw:raise AssertionError('unreachable')
 if not raw:question.update({':question/difficulty':':question.difficulty/'+level,':question/worked-solution':solution})
 field_specs=[(values,correct,profile!='observed_106661')]
 if profile=='observed_106662':field_specs.insert(0,(*bank(template,p,profile,True),False))
 content={'question':question,'banks':[(sorted(v),v[c] if has else None) for v,c,has in field_specs]}
 identity=fingerprint({'version':VERSION,**content});qid=uid(identity);fields=[]
 for ix,(v,c,has) in enumerate(field_specs):
  fid=uid(qid+f'/field/{ix}');choices=[{':answer/id':uid(fid+'/'+val),':answer/type':':answer.type/math',':answer/value':val} for val in v]
  field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices}
  if has:field[':answer-field/correct']=[':answer/id',choices[c][':answer/id']]
  rng.shuffle(choices);fields.append(field)
 question[':question/id']=qid;question[':question/answer-fields']=fields
 # Task fingerprint includes mathematical prompt conditions and assessed correct
 # model/initial condition, excluding distractors/profile/order and numeric spelling.
 if template.endswith('equation'):task={'kind':template,'a':str(rat(p['a'])),'k':str(rat(p['k']))}
 elif template=='factored_ivp':task={'kind':'ivp','c':str(rat(p['a'])*rat(p['k'])),'b':str(-rat(p['k'])),'initial':str(rat(p['initials'][correct]))}
 else:task={'kind':'ivp',**{key:str(rat(v)) for key,v in p['options'][correct].items()}}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':question,'generation':{'version':VERSION,'seed':seed,'template':template,'profile':profile,'parameters':p,'source':SOURCE,'origin':'raw-observed-replay' if raw else 'authored-actual-method','evidence_only':raw,'eligible_for_learning':not raw,'difficulty_basis':'authored-inferred' if level=='easy' else 'observed','mathematical_fingerprint':fingerprint(task),'content_sha256':identity,'plot_rating':'none','scope':'identify form and initial-below-cap; no ODE solving'}}

def markdown(r):
 q=r['question'];lines=[q[':question/problem']]
 for i,f in enumerate(q.get(':question/answer-fields',[])):
  lines += ['']+[f'- ${a[":answer/value"]}$'+(' **Correct**' if f.get(':answer-field/correct',[None,None])[1]==a[':answer/id'] else '') for a in f[':answer-field/choices']]
 if ':question/worked-solution' in q:lines+=['','Worked solution:',q[':question/worked-solution']]
 return '\n'.join(lines)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');a=ap.parse_args()
 if a.count<1:ap.error('count must be positive')
 levels=['easy','moderate','hard'] if a.difficulty=='all' else [a.difficulty];records=[generate(l,a.seed+i,template=a.template,profile=a.profile) for l in levels for i in range(a.count)]
 print(json.dumps(records,indent=2) if a.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
if __name__=='__main__':main()
