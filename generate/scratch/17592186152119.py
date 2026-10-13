#!/usr/bin/env python3
"""Finding the LCM of three already factored polynomials (scratch, no DB writes).

Observed Easy: one primitive factor, three coefficients/powers, blank or radio.
Observed Moderate: two primitive factors (binomial/binomial or monomial/binomial).
Authored Hard: three displayed factors in the SAME two variables; one additional
maximum bookkeeping operation, with maxima distributed over all three inputs.
No expansion, factorization, roots, or coprimality work is asked of the learner.
Source masks slot COMPLETE mathematical components, not substring substitutions.
Raw erroneous source teaching prose is only available through an explicit profile.
Integers are interpreted over ZZ: LCM has positive integer content, NOT monic QQ
normalization. All profile/explicit inputs receive the same reduced-object bounds.
"""
from __future__ import annotations
import argparse,hashlib,json,math,random,re,uuid,itertools
from pathlib import Path
import sympy as sp
D=Path(__file__).with_suffix('')
MASKS=json.loads((D/'masks.json').read_text())
KP_ID=17592186152119
KP_UUID='57496436-8bd0-567e-8c37-ed584849ce1a'
TITLE='Finding the LCM of Three Polynomials'
VERSION='three-polynomial-lcm-v1'
SOURCE={'database':'math','basis':1356,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}
TEMPLATES={'single_blank':('easy','blank',1),'single_radio':('easy','radio',1),
 'single_legacy_blank':('easy','blank',1),'double_blank':('moderate','blank',2),
 'double_radio':('moderate','radio',2),'double_legacy_blank':('moderate','blank',2),
 'triple_blank':('hard','blank',3),'triple_radio':('hard','radio',3)}
PROFILES={'raw-q-218518':{'template':'single_legacy_blank','source':'q-218518','origin':'raw-omission'},
 'raw-q-218519':{'template':'double_legacy_blank','source':'q-218519','origin':'raw-omission'},
 'completion-q-218518':{'template':'single_legacy_blank','source':'q-218518','origin':'authored-completion'},
 'completion-q-218519':{'template':'double_legacy_blank','source':'q-218519','origin':'authored-completion'},**{'observed-'+sid:{'template':m['template'],'source':sid,'origin':'observed'} for sid,m in MASKS.items() if sid not in ('q-218518','q-218519')},
 'observed-q-222132-raw-error':{'template':'double_blank','source':'q-222132','origin':'raw-error'},
 'authored-single-bank':{'template':'single_radio','source':'q-76247','origin':'authored'},
 'authored-double-bank':{'template':'double_radio','source':'q-76475','origin':'authored'},
 'authored-triple-bank':{'template':'triple_radio','source':None,'origin':'authored'}}
class SampleRejected(ValueError): pass

def digest(value):return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def validate_parameters(level,p,n):
 if set(p)!={'coefficients','variables','shifts','powers'}:raise ValueError('Exactly coefficients, variables, shifts, powers required')
 c,v,h,e=(p[k] for k in ('coefficients','variables','shifts','powers'))
 if len(c)!=3 or len(v)!=n or len(h)!=n or len(e)!=3 or any(len(r)!=n for r in e):raise ValueError('Three input polynomials and correct factor dimensions required')
 if any(type(a)!=int for a in c+h+[a for r in e for a in r]):raise ValueError('Integral parameters required')
 if any(a not in ('x','y','u','v') for a in v):raise ValueError('Unsupported variables')
 if len(set(zip(v,h)))!=n:raise ValueError('Factors must be distinct primitive factors after reduction')
 if any(abs(a)>9 for a in h):raise ValueError('Shifts exceed source-scale workload')
 maxc=12 if level=='easy' else 20
 if any(not 2<=a<=maxc for a in c):raise ValueError('Coefficient bounds')
 if math.lcm(*c)>(60 if level=='easy' else 120):raise ValueError('Integer LCM workload bound')
 maxe=7 if level=='moderate' else 5
 if any(not 1<=a<=maxe for r in e for a in r):raise ValueError('Powers exceed level bounds or remove factors')
 if any(len({r[j] for r in e})<2 for j in range(n)):raise ValueError('Every factor requires substantive maximum selection')
 if level=='easy' and h[0]==0:raise ValueError('Easy observed binomial layout requires a shift')
 if level=='moderate' and len(set(v))!=2:raise ValueError('Moderate uses two independent variable classes')
 if level=='hard':
  if not (v[0]==v[2] and v[0]!=v[1]) or any(a==0 for a in h):raise ValueError('Hard: three displayed binomials in two variables x,y,x')
  dominant=[next(i for i in range(3) if e[i][j]==max(r[j] for r in e)) for j in range(3)]
  if len(set(dominant))!=3 or any(sum(r[j]==max(s[j] for s in e) for r in e)!=1 for j in range(3)):
   raise ValueError('Hard maxima must be unique and distributed over all three inputs')

def factor(p,j,notation='compact',power=None):
 v,h=p['variables'][j],p['shifts'][j]
 gap=' ' if notation=='spaced' else ''
 if h:base='('+v+gap+('+' if h>0 else '-')+gap+str(abs(h))+')'
 else:base=v if power in (None,1) or notation=='spaced' else '{'+v+'}'
 return base if power in (None,1) else base+'^{'+str(power)+'}'
def variable_part(p,i,notation='compact'):return ''.join(factor(p,j,notation,p['powers'][i][j]) for j in range(len(p['variables'])))
def poly(p,i,notation='compact'):return str(p['coefficients'][i])+variable_part(p,i,notation)
def result(p,c=None,powers=None,notation='compact',dots=False):
 c=math.lcm(*p['coefficients']) if c is None else c
 powers=powers or [max(row[j] for row in p['powers']) for j in range(len(p['variables']))]
 parts=[factor(p,j,notation,a) for j,a in enumerate(powers)]
 return (str(c)+r'\cdot '+r'\cdot '.join(parts)) if dots else str(c)+''.join(parts)
def prompt_math(sid,p):
 note=MASKS[sid]['notation']; rows=[poly(p,i,note) for i in range(3)]
 if sid=='q-218519':return [rows[0]+', '+rows[1],rows[2]]
 if sid=='q-218518':return rows
 if sid=='q-222132':return [rows[0]+r',\,'+rows[1]+',',rows[2]]
 return [rows[0]+',',r'\,'+rows[1]+',',rows[2]+('.' if TEMPLATES[MASKS[sid]['template']][1]=='radio' else '')]

def multiples(sid,i,p):
 """Source list layouts: full first-through-LCM lists, or first two / tail lists.
 Full list length follows changed LCM/coefficient; ellipses never hide the LCM.
 Exact observed comma/spacing conventions are retained at original parameters.
 """
 c=p['coefficients'][i]; L=math.lcm(*p['coefficients']); n=L//c
 original=MASKS[sid]['parameters']; n0=math.lcm(*original['coefficients'])//original['coefficients'][i]
 specs={'q-112230':[(1,'…'),(1,'…'),(1,None)],'q-222127':[(1,None),(1,None),(1,None)],
 'q-222129':[(1,None),(1,'…'),(1,None)],'q-222132':[(1,None),(1,None),(1,'⋯')],
 'q-76247':[(0,None),(0,None),(1,None)],'q-76475':[(2,None),(1,None),(1,None)]}
 extra,ellipsis=specs[sid][i]
 if ellipsis and n>=5:
  indices=[1,2,'ellipse',n-1,n,n+1]
 else:indices=list(range(1,n+extra+1))
 text=r'\,'
 for k,index in enumerate(indices):
  if k:
   sep=',' if index=='ellipse' else r',\,'
   if sid=='q-222127' and i==0 and index==4:sep=','
   if sid=='q-222129' and i==1 and k and indices[k-1]=='ellipse':sep=','
   if sid=='q-222132' and i==2 and index=='ellipse':sep=r',\,'
   text+=sep
  text+=(ellipsis if index=='ellipse' else str(c*index))
 # Source lists have independent visible punctuation around the final ellipsis.
 tail=r',\,…' if sid in ('q-76475','q-112230') and (sid=='q-76475' and i<2 or sid=='q-112230' and i==0) else ',…'
 return text+tail

def source_solution_math(sid,p,raw=False):
 c=p['coefficients']; n=len(p['variables']); v=[variable_part(p,i) for i in range(3)]; polys=[poly(p,i) for i in range(3)]; mx=[max(r[j] for r in p['powers']) for j in range(n)];L=math.lcm(*c)
 lcm=r'\text{LCM}'; nums=','.join(map(str,c)); out=[lcm,lcm+'('+nums+'):',str(c[0])+':',multiples(sid,0,p),str(c[1])+':',multiples(sid,1,p),str(c[2])+':',multiples(sid,2,p),lcm+'('+nums+')='+str(L)+'.',lcm]
 if n==1:
  out += [v[0]+',',v[1]+',',v[2]+',',factor(p,0),str(mx[0])+'.']
  out += ['\n'+lcm+'('+r',\,'.join(v)+')='+factor(p,0,power=mx[0])+'.\n']
  out += ['\n'+lcm+'('+r',\,'.join(polys)+')='+result(p,dots=True)+'='+result(p)+('.' if sid=='q-76247' else '')+'\n']
 else:
  out += [v[0]+','+v[1]+',',v[2]+',',('(x-y)' if sid=='q-222132' and raw else factor(p,0)),factor(p,1)]
  for j in range(n):
   sep=r',\,' if sid=='q-76475' and j==0 else ','
   out += [factor(p,j,power=p['powers'][0][j])+sep+factor(p,j,power=p['powers'][1][j])+',',factor(p,j,power=p['powers'][2][j])+',',str(mx[j])+'.']
  out += [factor(p,0),factor(p,1)]
  sep=',' if sid=='q-222132' else r',\,'
  out += ['\n'+lcm+'('+sep.join(v)+')='+r'\cdot '.join(factor(p,j,power=mx[j]) for j in range(n))+'.\n']
  ending=r' & \end{aligned}' if sid=='q-222132' else r' & .\end{aligned}'
  out += ['\n'+r'\begin{aligned}'+lcm+'('+r',\,'.join(polys)+r') & = \\ '+result(p,dots=True)+r' & = \\ '+result(p)+ending+'\n']
 return out

def fill(segments,values):
 it=iter(values);parts=[]
 for s in segments:
  if isinstance(s,str):parts.append(s)
  else:
   math_text=next(it); d='$$' if s['display'] else '$';parts.append(d+math_text+d)
 try:next(it);raise ValueError('Too many math slots')
 except StopIteration:pass
 return ''.join(parts)

def generic_solution(p):
 """Shared source prose plus all coefficient/factor/formal/product stages."""
 c=p['coefficients'];L=math.lcm(*c);n=len(p['variables']); nums=','.join(map(str,c)); v=[variable_part(p,i) for i in range(3)]
 opening='To find the least common multiple ($\\text{LCM}$) of three polynomials that are made up of products of binomials, we find the least common multiple of the constants and the least common multiple of '+('the variable part' if n==1 else 'each variable part')+'. Then, we multiply all of the results together.'
 s=opening+'\n\nSo first, we find $\\text{LCM}('+nums+'):$'
 for a in c:
  multiples_values=list(range(a,L+a,a))+[L+a]
  if len(multiples_values)>10:multiples_values=[a,2*a,'…',L-a,L,L+a]
  s+='\n\n- Multiples of $'+str(a)+':$ $\\,'+r',\,'.join(map(str,multiples_values))+',…$'
 s+='\n\nSo, $\\text{LCM}('+nums+')='+str(L)+'.$'
 s+='\n\nTo find the $\\text{LCM}$ of $'+','.join(v)+',$ we find the largest powers for '+', '.join('$'+factor(p,j)+'$' for j in range(n))+' that appear in all these expressions:'
 for j in range(n):s+='\n\n- For $'+factor(p,j,power=p['powers'][0][j])+',$ $'+factor(p,j,power=p['powers'][1][j])+',$ and $'+factor(p,j,power=p['powers'][2][j])+',$ the largest power is $'+str(max(r[j] for r in p['powers']))+'.$'
 s+='\n\nNow, we raise '+', '.join('$'+factor(p,j)+'$' for j in range(n))+' to the corresponding largest powers. Therefore,\n\n$$\n'+r'\text{LCM}('+r',\,'.join(v)+')='+r'\cdot '.join(factor(p,j,power=max(r[j] for r in p['powers'])) for j in range(n))+'.\n$$'
 s+='\n\nFinally, we multiply all of our results together:\n\n$$\n'+r'\begin{aligned}\text{LCM}('+r',\,'.join(poly(p,i) for i in range(3))+r') & = \\ '+result(p,dots=True)+r' & = \\ '+result(p)+r' & .\end{aligned}'+'\n$$'
 return s

def bank(p,profile):
 c=p['coefficients'];L=math.lcm(*c);e=p['powers'];n=len(p['variables']); mx=[max(r[j] for r in e) for j in range(n)];mn=[min(r[j] for r in e) for j in range(n)];sm=[sum(r[j] for r in e) for j in range(n)]
 if profile=='observed-q-76247':
  # Exact observed expression patterns, interpretation of last three is limited.
  components=[(L,mx),(2*L,mx),(L,[2*e[1][0]]),(2*L,[2*e[1][0]]),(max(c)**2,sm)]
 elif profile=='observed-q-112230':
  partial=math.lcm(c[0],c[1]);replay_sum=[sm[0],sm[1]-1]
  components=[(L,mx),(partial,mx),(L+partial,mx),(L,replay_sum),(L+partial,replay_sum)]
 elif profile=='observed-q-76475':
  components=[(L,mx),(2*L,mn),(2*L,mx),(L,sm),(L,mn)]
 elif profile in ('authored-single-bank','authored-double-bank','authored-triple-bank'):
  components=[(L,mx),(math.gcd(*c),mx),(math.prod(c),mx),(L,mn),(L,sm)]
 else:components=[(L,mx)]
 values=[result(p,a,b) for a,b in components]
 if len(set(values))!=len(values):raise SampleRejected('The complete selected bank collides')
 return values

def sample(level,n,rng):
 # Uniform meaningful coefficient triples then complete-object rejection.
 c=[rng.randint(2,12 if level=='easy' else 20) for _ in range(3)]
 v=([rng.choice(['x','y'])] if n==1 else ['x','y'] if n==2 else ['x','y','x'])
 h=[rng.choice([a for a in range(-9,10) if a]) for _ in range(n)]
 if n==2 and rng.random()<0.35:h[0]=0
 e=[[rng.randint(1,7 if level=='moderate' else 5) for j in range(n)] for i in range(3)]
 if n==3:
  for j in range(3):
   peak=rng.randint(3,5)
   for i in range(3):e[i][j]=peak if i==j else rng.randint(1,peak-1)
 return {'coefficients':c,'variables':v,'shifts':h,'powers':e}

def build(level,name,p,seed,profile):
 spec=TEMPLATES[name];kind=spec[1];sid=PROFILES.get(profile,{}).get('source')
 # Authored banks retain the closest observed complete prompt/solution layout.
 if level=='hard':sid=None
 if profile=='authored-double-bank':sid='q-76475' if p['shifts'][0]==0 else 'q-112230'
 if sid:
  prompt=fill(MASKS[sid]['problem'],prompt_math(sid,p))
  solution=fill(MASKS[sid]['worked-solution'],source_solution_math(sid,p,profile.endswith('raw-error'))) if 'worked-solution' in MASKS[sid] else generic_solution(p)
 else:
  inputs=[poly(p,i) for i in range(3)]
  prompt=('Find the least common multiple of the polynomials $'+inputs[0]+',$ $\\,'+inputs[1]+',$ and $'+inputs[2]+'.$') if kind=='radio' else ('The least common multiple of the polynomials $'+inputs[0]+r',\,'+inputs[1]+',$ and $'+inputs[2]+'$ is {{field-1}}.')
  solution=generic_solution(p)
 raw_omission=PROFILES.get(profile,{}).get('origin')=='raw-omission'
 if raw_omission:solution=None
 values=[] if raw_omission else bank(p,profile) if kind=='radio' else [result(p)]
 # The fingerprint uses the integer-content polynomials, not presentation/banks.
 expressions=[]
 for i in range(3):
  expr=sp.Integer(p['coefficients'][i])
  for j in range(len(p['variables'])):expr *= (sp.Symbol(p['variables'][j])+p['shifts'][j])**p['powers'][i][j]
  expressions.append(str(sp.expand(expr)))
 all_symbols=sorted(set().union(*(sp.sympify(a).free_symbols for a in expressions)),key=str)
 aliases=[sp.Symbol('v'+str(i)) for i in range(len(all_symbols))]
 canonical_sets=[sorted(str(sp.expand(sp.sympify(a).xreplace(dict(zip(all_symbols,perm))))) for a in expressions) for perm in itertools.permutations(aliases)]
 fingerprint=digest(min(canonical_sets))
 content=digest({'version':VERSION,'prompt':prompt,'solution':solution,'bank':sorted(values),'field_type':kind,'mathematical_task':fingerprint})
 qid=uuid.uuid5(uuid.NAMESPACE_URL,KP_UUID+'/'+content);key='selection' if kind=='radio' else 'field-1';fid=uuid.uuid5(qid,key)
 choices=[{':answer/id':str(uuid.uuid5(fid,v)),':answer/type':':answer.type/math',':answer/value':v} for v in values]
 correct=choices[0][':answer/id'] if choices else None;random.Random(seed).shuffle(choices)
 record={'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':str(qid),':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':[{':answer-field/id':str(fid),':answer-field/key':key,':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':choices,':answer-field/correct':[':answer/id',correct]}]},'generation':{'version':VERSION,'sympy_version':sp.__version__,'seed':seed,'template':name,'parameters':p,'bank_profile':profile,'bank_origin':PROFILES.get(profile,{}).get('origin','authored'),'parameter_fingerprint':fingerprint,'content_fingerprint':content,'authored_extension':level=='hard' or PROFILES.get(profile,{}).get('origin') in ('authored','authored-completion'),'source_analysis':SOURCE,'source_ids':[sid] if sid else [],'source_completion':sid in ('q-218518','q-218519') and not raw_omission,'preserves_source_omissions':raw_omission,'raw_source_error':profile.endswith('raw-error') if profile else False,'source_prose_repair':sid=='q-222132' and not profile.endswith('raw-error'),'evidence_only':raw_omission or PROFILES.get(profile,{}).get('origin')=='raw-error' or (kind=='radio' and PROFILES.get(profile,{}).get('origin')=='observed'),'eligible_for_learning':not (raw_omission or PROFILES.get(profile,{}).get('origin')=='raw-error' or (kind=='radio' and PROFILES.get(profile,{}).get('origin')=='observed')),'plot_rating':'none','plot_assets':{},'domain':'positive integer coefficients, primitive distinct displayed linear factors over ZZ; positive integer-content LCM'}}

 if raw_omission:
  for attr in (':question/difficulty',':question/worked-solution'):record['question'].pop(attr)
  for attr in (':answer-field/choices',':answer-field/correct'):record['question'][':question/answer-fields'][0].pop(attr)
 return record

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('Invalid difficulty')
 if profile:
  if profile not in PROFILES:raise ValueError('Unknown profile')
  implied=PROFILES[profile]['template']
  if template and template!=implied:raise ValueError('Profile/template mismatch')
  template=implied
 names=[a for a,s in TEMPLATES.items() if s[0]==level and (field_type is None or s[1]==field_type)]
 if template and template not in names or not names:raise ValueError('Template/level/field mismatch')
 if profile and profile.endswith('raw-error') and parameters!=MASKS[PROFILES[profile]['source']]['parameters']:
  raise ValueError('Raw error profile is evidence-only at original explicit parameters')
 rng=random.Random(seed);name=template or rng.choice([a for a in names if 'legacy' not in a]);n=TEMPLATES[name][2];kind=TEMPLATES[name][1]
 if profile is None:
  if kind=='radio':profile={'easy':'authored-single-bank','moderate':'authored-double-bank','hard':'authored-triple-bank'}[level]
  elif name=='single_blank':profile='observed-q-222127'
  elif name=='double_blank':profile='observed-q-222132'
  elif 'legacy' in name:profile='completion-'+('q-218518' if level=='easy' else 'q-218519')
 for _ in range(2000):
  p=dict(parameters) if parameters is not None else sample(level,n,rng)
  if parameters is None and profile in ('observed-q-76475','observed-q-218519','completion-q-218519','raw-q-218519'):p['shifts'][0]=0
  if parameters is None and profile in ('observed-q-112230','observed-q-222132') and p['shifts'][0]==0:continue
  try:
   if profile in ('observed-q-76475','observed-q-218519','completion-q-218519','raw-q-218519') and (p['shifts'][0]!=0 or p['shifts'][1]==0):raise ValueError('Observed monomial/binomial profile factor layout')
   if profile in ('observed-q-112230','observed-q-222132') and any(a==0 for a in p['shifts']):raise ValueError('Observed binomial/binomial profile factor layout')
   validate_parameters(level,p,n)
   return build(level,name,p,seed,profile)
  except ValueError:
   if parameters is not None:raise
 raise SampleRejected('Bounded full-instance sampling exhausted')

# EASY: observed single shifted factor, coefficients2..12, powers1..5, LCM≤60.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE: observed two independent variable factors, coeff2..20, powers1..7, LCM≤120.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# HARD: authored three primitive binomials x+a,y+b,x+c, distinct a/c, same content
# arithmetic scale; one extra highest-power column, distributed unique maxima.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)

def markdown(r):
 q=r['question'];g=r['generation'];f=q[':question/answer-fields'][0]
 if ':question/difficulty' not in q:return '## Raw evidence — '+str(g['bank_profile'])+'\n\n'+q[':question/problem']+'\n\nOriginal answer bank, correct ref, difficulty and worked solution are absent.'
 s='## Generated '+q[':question/difficulty'].split('/')[-1]+' — '+g['template']+'\n\nProfile: `'+str(g['bank_profile'])+'`; origin: '+g['bank_origin']+('; evidence only, ineligible for learning' if g.get('evidence_only') else '; eligible for learning')+'.\n\n'+q[':question/problem']+'\n\n'
 for a in f[':answer-field/choices']:s+='- $'+a[':answer/value']+'$'+(' (correct)' if a[':answer/id']==f[':answer-field/correct'][1] else '')+'\n'
 return s+'\nWorked solution:\n\n'+q[':question/worked-solution']
if __name__=='__main__':
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--template',choices=list(TEMPLATES));ap.add_argument('--profile',choices=list(PROFILES));ap.add_argument('--format',choices=['markdown','json'],default='markdown');a=ap.parse_args()
 if a.count<1 or a.difficulty=='all' and (a.profile or a.template):ap.error('Use positive count and specific difficulty with profile/template')
 records=[generate(level,a.seed+i,a.template,profile=a.profile) for level in (['easy','moderate','hard'] if a.difficulty=='all' else [a.difficulty]) for i in range(a.count)]
 print(json.dumps(records,indent=2) if a.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
