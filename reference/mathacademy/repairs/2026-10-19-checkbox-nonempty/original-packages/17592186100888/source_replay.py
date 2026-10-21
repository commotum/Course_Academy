"""Verifying one proposed first-order ODE solution; local records only, version 1.

Observed masks preserve complete source wording, ordered rows, punctuation, and
banks. Slots are whole mathematical components, never short character replaces.
Hard is authored affine-chain verification; no ODE solving or initial conditions.
"""
from pathlib import Path
import argparse, hashlib, json, random, re, uuid, sys, itertools
import sympy as sp
HERE=Path(__file__).with_suffix('')
VERSION='1.3.0-draft'
CURRENT_VERSION=VERSION
SUPPORTED_LEVELS=('easy','moderate','hard')
RAW_DOMAIN_PHRASE="for all values of $x$ in the equation's domain."
NORMAL_DOMAIN_PHRASE="for all values of $x$ in an interval where the function is defined and the equation is valid."
KP={'db_id':17592186100888,'id':'201edc93-37b4-556a-aaea-4fcf9a01077a','title':'Identifying a Solution to a First-Order Differential Equation'}
x=sp.Symbol('x',positive=True); y=sp.Symbol('y',real=True)
MASKS=json.loads((HERE/'masks.json').read_text())
DEFAULTS={
'power_easy':{'n':4}, 'exp_true':{'k':2}, 'sin_none':{'k':2},
'cos_i':{'k':2}, 'log_all':{'h':0}, 'inverse_none':{'n':2},
'exp_none':{'a':3,'k':1,'b':3}, 'log_scaled':{'m':2},
'power_moderate':{'a':-3,'n':2},
}
LEVELS={t:('moderate' if t=='power_moderate' else 'easy') for t in DEFAULTS}
LEVELS['affine_log']='hard'
ANSWERS={(True,True):'I, II, and III',(False,True):'II and III only',(True,False):'I only',(False,False):'None'}

def power(n):
 return 'x' if n==1 else '{x}^{'+str(n)+'}' if n else '1'
def coeff(a,z):
 return z if a==1 else '-'+z if a==-1 else str(a)+z
def exp(k):
 return '{e}^{'+coeff(k,'x')+'}'
def trig(name,k):
 return r'\operatorname{'+name+'}⁡'+coeff(k,'x')
def frac(a,b): return r'\frac{'+str(a)+'}{'+str(b)+'}'
def tex(v): return sp.latex(v).replace(r'\log',r'\ln')
def uid(v): return str(uuid.uuid5(uuid.NAMESPACE_URL,'ode-verify:'+v))
def truth(f,d,r): return sp.simplify(sp.diff(f,x)-d)==0, sp.simplify(sp.diff(f,x)-r.subs(y,f))==0

def components(t,p):
 """Compute exact f, asserted derivative, RHS and all displayed stage components."""
 if t=='power_easy':
  n=p['n']; F=power(n); D=coeff(n,power(n-1)); C=coeff(n+1,power(n+1)); R=frac(coeff(n,'y'),'x')
  v={'F':F,'D':D,'C':C,'R':R,'S':frac(str(n)+'('+F+')','x')}; f=x**n; d=(n+1)*x**(n+1); r=n*y/x
 elif t=='exp_true':
  k=p['k']; F=exp(k); D=coeff(k,F); v={'F':F,'D':D,'R':coeff(k,'y')}; f=sp.exp(k*x); d=k*f;r=k*y
 elif t=='sin_none':
  k=p['k']; F=frac(1,k)+trig('sin',k); D=trig('cos',k); C=coeff(k,D)
  v={'F':F,'D':D,'C':C,'R':coeff(k,'y'),'S':str(k)+'('+F+')','E':trig('sin',k),'P':frac(1,k)+r'\cdot '+str(k)+D}; f=sp.sin(k*x)/k;d=k*sp.cos(k*x);r=k*y
 elif t=='cos_i':
  k=p['k']; F=trig('cos',k); D=coeff(-k,trig('sin',k));v={'F':F,'D':D,'R':'y'+F,'S':F+r'\cdot '+F,'E':'{cos}^{2}⁡'+coeff(k,'x')};f=sp.cos(k*x);d=-k*sp.sin(k*x);r=y*sp.cos(k*x)
 elif t=='log_all':
  h=p['h']; z='x' if h==0 else 'x+'+str(h) if h>0 else 'x'+str(h)
  F=r'\operatorname{ln}⁡'+(z if h==0 else '('+z+')');D=frac(1,z)
  v={'F':F,'D':D,'R':frac(1,'{e}^{y}'),'S':frac(1,'{e}^{'+F+'}')};f=sp.log(x+h);d=1/(x+h);r=sp.exp(-y)
 elif t=='inverse_none':
  n=p['n'];F='-'+frac(1,power(n));D=frac(n,power(n+1));C='-'+D
  v={'F':F,'D':D,'C':C,'R':frac('y',power(n)),'S':frac('('+F+')',power(n)),'E':'-'+frac(1,power(2*n))};f=-x**(-n);d=-n*x**(-n-1);r=y/x**n
 elif t=='exp_none':
  a,k,b=p['a'],p['k'],p['b'];F=coeff(a,exp(-k));D=coeff(-a*k,exp(-k))
  v={'F':F,'D':D,'R':coeff(-b,'y'),'S':str(-b)+'('+F+')','E':coeff(-a*b,exp(-k))};f=a*sp.exp(-k*x);d=f;r=-b*y
 elif t=='log_scaled':
  m=p['m'];a=2*m;F=coeff(a,r'\operatorname{ln}⁡x');D=frac(a,'x');C=frac(1,str(a)+'x');numer=str(a)+'x'
  v={'F':F,'D':D,'C':C,'R':frac(numer,'{e}^{y/'+str(m)+'}'),'S':frac(numer,'{e}^{('+F+')/'+str(m)+'}'),'H':frac(numer,r'{e}^{2\operatorname{ln}⁡x}'),'J':frac(numer,r'{e}^{\operatorname{ln}⁡{x}^{2}}'),'K':frac(numer,'{x}^{2}')};f=a*sp.log(x);d=1/(a*x);r=a*x*sp.exp(-y/m)
 elif t=='power_moderate':
  a,n=p['a'],p['n'];F=coeff(a,power(n));D=coeff(a*n,power(n-1));C=coeff(a-n,power(n-1));R=frac(coeff(n,'y'),'x')
  v={'F':F,'D':D,'C':C,'R':R,'S':frac(str(n)+'('+F+')','x'),'P':str(a)+r'\cdot '+coeff(n,power(n-1))};f=a*x**n;d=(a-n)*x**(n-1);r=n*y/x
 else: raise ValueError(t)
 return v,f,d,r

def fill(mask,slots):
 return re.sub(r'@@(\w+)@@',lambda m:slots[m.group(1)],mask)

def validate_parameters(level,t,p):
 if t=='affine_log':
  if set(p)!={'a','b','c','solution','claim'} or any(type(p[k]) is not int for k in ['a','b','c']):raise ValueError('Hard requires integer a,b,c and boolean solution,claim')
  if not(2<=abs(p['a'])<=4 and 2<=p['b']<=4 and 1<=abs(p['c'])<=4) or any(type(p[k]) is not bool for k in ['solution','claim']):raise ValueError('Hard bounds: |a|=2..4,b=2..4,|c|=1..4')
  return
 if set(p)!=set(DEFAULTS[t]) or any(type(v) is not int for v in p.values()):raise ValueError('Unexpected or noninteger parameters')
 if 'n' in p and not 2<=p['n']<=5:raise ValueError('n must be 2..5')
 if 'k' in p and not 1<=p['k']<=4:raise ValueError('k must be 1..4')
 if t=='sin_none' and p['k']==1:raise ValueError('k=1 removes false derivative claim')
 if 'm' in p and not 1<=p['m']<=4:raise ValueError('m must be 1..4')
 if 'h' in p and not -4<=p['h']<=4:raise ValueError('h must be -4..4')
 if t=='exp_none' and not(2<=p['a']<=5 and 1<=p['b']<=5 and p['b']!=p['k']):raise ValueError('Requires positive nonunit amplitude and b!=k')
 if t=='power_moderate' and not(-9<=p['a']<=-2 and p['a']-p['n']!=p['a']*p['n']):raise ValueError('Requires a=-9..-2 and unequal derivative assertion')

def sample(t,rng):
 if t=='affine_log':return {'a':rng.choice([-4,-3,-2,2,3,4]),'b':rng.randint(2,4),'c':rng.choice([-4,-3,-2,-1,1,2,3,4]),'solution':rng.choice([True,False]),'claim':rng.choice([True,False])}
 p={k:rng.randint(2,5) if k=='n' else rng.randint(1,4) if k in ('k','m') else rng.randint(-4,4) if k=='h' else -rng.randint(2,9) if t=='power_moderate' else rng.randint(2,5) for k in DEFAULTS[t]}
 if t=='sin_none':p['k']=rng.randint(2,4)
 return p

def hard(p):
 a,b,c=p['a'],p['b'],p['c'];z=b*x+c;f=a*sp.log(z);df=a*b/z;claimed=df if p['claim'] else b/(a*z);q=a*b if p['solution'] else -a*b;r=q*sp.exp(-y/a)
 F=tex(f);D=tex(df);C=tex(claimed);R=str(q)+r'{e}^{-y/('+str(a)+')}'
 # Unsimplified exponent substitution and chain derivative remain separate stages.
 formal=tex(a)+r'\cdot '+frac(b,tex(z));sub=str(q)+r'{e}^{-('+F+')/('+str(a)+')}'
 evaluated=str(q)+r'{e}^{-\ln('+tex(z)+')}';final=tex(q/z)
 prompt='Consider the following differential equation.\n\n$$\n'+"{y}^{′}="+R+'\n$$\n\nLet $f(x)='+F+',$ on $'+tex(z)+'>0.$ Which of the following statements are true?\n\n- ${f}^{′}(x)='+C+'$\n- Substituting $y=f(x)$ and ${y}^{′}={f}^{′}(x)$ into the differential equation gives a true statement\n- The function $y=f(x)$ is a solution of the differential equation'
 i,ii=truth(f,claimed,r);status=lambda v:'true' if v else 'false'
 solution=MASKS['exp_true']['solution'].split('- Statement I')[0]
 rows=r'\begin{aligned}{f}^{′}(x) & ={('+F+r')}^{′} \\ & ='+formal+r' \\ & ='+D
 if not i:rows+=r' \\ & \ne '+C
 rows+=r'.\end{aligned}'
 solution+='- Statement I is '+status(i)+'. Differentiating $f(x)='+F+',$ we get \n\n$$\n'+rows+'\n$$\n\n'
 rows=r'\begin{aligned}{y}^{′} & \overset{?}{=}'+R+r' \\ '+D+r' & \overset{?}{=}'+sub+r' \\ '+D+r' & \overset{?}{=}'+evaluated+r' \\ '+D+(' & =' if ii else r' & \ne ')+final+(r'\,✓' if ii else r'\,\times ')+r'\end{aligned}'
 solution+='- Statement II is '+status(ii)+'. Substituting $y='+F+'$ and ${y}^{′}='+D+'$ into the original equation, we get a '+status(ii)+' statement:\n\n$$\n'+rows+'\n$$\n\n'
 solution+='- Statement III is '+status(ii)+'. Since statement II is '+status(ii)+', the function $y='+F+'$ is '+('' if ii else 'not ')+'a solution to our differential equation.\n\nTherefore, the correct answer is "'+ANSWERS[i,ii]+'."'
 return prompt,solution,f,claimed,r

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard') or field_type not in (None,'checkbox',':answer-field.type/checkbox'):raise ValueError('Unsupported level or field type')
 raw=bool(profile and profile.startswith('raw_'))
 normalized_profile=profile[4:] if raw else profile
 if normalized_profile=='boolean_statements':normalized_profile=None
 if raw and normalized_profile=='authored':raise ValueError('Raw profiles are restricted to captured source banks')
 if normalized_profile and normalized_profile!='authored':
  matched=[t for t,v in MASKS.items() if v['profile']==normalized_profile]
  if not matched:raise ValueError('Unknown observed profile')
  if template and template!=matched[0]:raise ValueError('Profile/template mismatch')
  template=matched[0]
 eligible=[t for t in LEVELS if LEVELS[t]==level];rng=random.Random(seed)
 t=template or rng.choice(eligible)
 if t not in eligible:raise ValueError('Template level mismatch')
 for _ in range(100):
  p=dict(parameters) if parameters is not None else sample(t,rng)
  try:validate_parameters(level,t,p)
  except ValueError:
   if parameters is not None:raise
   continue
  if t=='affine_log':prompt,solution,f,d,r=hard(p)
  else:
   slots,f,d,r=components(t,p);prompt=fill(MASKS[t]['prompt'],slots);solution=fill(MASKS[t]['solution'],slots)
  if t=='affine_log':
   head,tail=prompt.split('\n\n- ',1)
   statements=['- '+z for z in tail.split('\n- ')]
   prompt=head+'\n\nSelect all that apply.\n\n'+'\n'.join(z.replace('- ','- **'+key+'.** ',1) for key,z in zip(('I','II','III'),statements,strict=True))
  repairs=[]
  if not raw:
   assert RAW_DOMAIN_PHRASE in solution
   solution=solution.replace(RAW_DOMAIN_PHRASE,NORMAL_DOMAIN_PHRASE)
   repairs.append('solution_interval_wording')
   if t in ('log_all','log_scaled'):
    h=p.get('h',0);z='x' if h==0 else 'x+'+str(h) if h>0 else 'x'+str(h)
    prompt=prompt.replace(' Which of the following statements are true?', ' On the interval $'+z+'>0,$ which of the following statements are true?')
    repairs.append('explicit_logarithm_interval')
  i,ii=truth(f,d,r);correct=ANSWERS[i,ii]
  bank=MASKS[t]['bank'] if t in MASKS else {'I':['false','true'],'II':['false','true'],'III':['false','true']}
  domain=tex(p['b']*x+p['c'])+'>0' if t=='affine_log' else 'x'+('+'+str(p['h']) if p.get('h',0)>0 else str(p['h']) if p.get('h',0)<0 else '')+'>0' if t in ('log_all','log_scaled') else 'x != 0' if t in ('power_easy','power_moderate','inverse_none') else 'all real x'
  mathkey=hashlib.sha256(json.dumps([sp.srepr(f),sp.srepr(d),sp.srepr(r),domain],sort_keys=True).encode()).hexdigest()
  bits={'I':i,'II':ii,'III':ii}
  contract=[[key,':answer-field.type/checkbox',sorted(values)] for key,values in sorted(bank.items())]
  content=json.dumps([VERSION,level,prompt,solution,contract],ensure_ascii=False)
  qid=uid(content);fields=[]
  for key in ('I','II','III'):
   values=bank[key]
   if sorted(values)!=['false','true']:raise ValueError('Whole Boolean bank must contain false and true exactly once')
   fid=uid(qid+':'+key)
   choices=[{':answer/id':uid(fid+':'+value),':answer/type':':answer.type/text',':answer/value':value} for value in values]
   # The observed Boolean widget contract is stable; no option-order aliases.
   fields.append({':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/checkbox',':answer-field/choices':choices,':answer-field/correct':[':answer/id',uid(fid+':'+str(bits[key]).lower())]})
  q={':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':fields}
  return {'knowledge_point':KP.copy(),'question':q,'generation':{'version':VERSION,'template':t,'bank_profile':profile or (MASKS[t]['profile'] if t in MASKS else 'authored'),'seed':seed,'parameters':p,'origin':'authored_missing_level' if t=='affine_log' else 'observed_template_parameterization','bank_origin':'authored_missing_level' if t=='affine_log' else 'observed_current_boolean_contract','assertion_recipe_origin':'authored_inferred_operation' if t=='power_moderate' else 'authored' if t=='affine_log' else 'observed_expression_parameterization','eligible_for_learning':not raw,'evidence_only':raw,'raw_evidence_profile':raw,'presentation_repairs':repairs,'mathematical_fingerprint':mathkey,'content_fingerprint':hashlib.sha256(content.encode()).hexdigest(),'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__},'source_analysis':{'database':'math','basis':2275,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1','question_ids':[MASKS[t]['source_id']] if t in MASKS else []},'domain':domain,'plot_rating':'none','parameter_extension_from_registered':t=='power_moderate' and p['a'] < -5}}
 raise ValueError('Bounded sampling exhausted')

# EASY: observed single power/elementary-chain verification, eight source layouts.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE: signed nonunit power coefficient; explicit coefficient-product row.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# HARD: authored affine logarithm, outer scale and chain coefficient, nonlinear substitution.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)

CAPACITIES={'power_easy':4,'exp_true':4,'sin_none':3,'cos_i':4,'log_all':9,'inverse_none':4,'exp_none':64,'log_scaled':4,'power_moderate':31,'affine_log':576}

def batch(level,count,seed=0,template=None,profile=None):
 """Bounded semantic sampling; seeds, profiles and order cannot inflate capacity."""
 normalized=profile[4:] if profile and profile.startswith('raw_') else profile
 implied=next((t for t,m in MASKS.items() if m['profile']==normalized),None)
 selected=template or implied
 capacity=CAPACITIES[selected] if selected in CAPACITIES else sum(CAPACITIES[t] for t in LEVELS if LEVELS[t]==level)
 if type(count) is not int or not 1<=count<=capacity:raise ValueError('Finite semantic capacity: '+str(capacity))
 records=[];seen=set()
 for offset in range(20000):
  rec=generate(level,seed+offset,template,profile=profile)
  fp=rec['generation']['mathematical_fingerprint']
  if fp not in seen:records.append(rec);seen.add(fp)
  if len(records)==count:return records
 raise ValueError('Distinct sampling failed within the declared finite capacity')

def markdown(rec):
 q=rec['question'];answers=[]
 for f in q.get(':question/answer-fields',[]):
  value=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
  answers.append('- '+f[':answer-field/key']+': '+value)
 label='**Raw evidence — ineligible for learning.**\n\n' if rec['generation']['evidence_only'] else ''
 return '## '+q.get(':question/difficulty',':question.difficulty/unrated').split('/')[-1].title()+'\n\n'+label+q[':question/problem']+'\n\nAuthor key:\n'+'\n'.join(answers)+'\n\n'+q.get(':question/worked-solution','')

def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=1);parser.add_argument('--format',choices=['markdown','json'],default='markdown');parser.add_argument('--template');parser.add_argument('--profile');a=parser.parse_args()
 if a.count<1:parser.error('Count must be positive')
 if a.difficulty=='all' and (a.template or a.profile):parser.error('Select one difficulty when selecting a template/profile')
 levels=['easy','moderate','hard'] if a.difficulty=='all' else [a.difficulty]
 try:records=[r for l in levels for r in batch(l,a.count,a.seed,a.template,a.profile)]
 except ValueError as exc:parser.error(str(exc))
 print(json.dumps(records,indent=2,ensure_ascii=False) if a.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
if __name__=='__main__':main()
