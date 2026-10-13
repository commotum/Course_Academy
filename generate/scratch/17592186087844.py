#!/usr/bin/env python3
"""Complex denominator roots, basis 1356. Private generator; no database writes.

Every observed source is compiled into complete-component masks. Original profiles
retain captured banks and missing fields. Normal profiles supply supported radio
fields for the three fieldless records and repair q-39795's stray 2x factor.
Complete observed distractor operations are reproducible, but source intent is
underdetermined: they remain explicit evidence profiles. Defaults use authored
complete banks. No cancellation, radical root solving, or complex arithmetic is
added. Easy: quadratic/no real roots. Moderate: GCF or grouping + positive
quadratic. Hard: cubes (including quartic GCF) + negative discriminant.
"""
from __future__ import annotations
import argparse, hashlib, json, random, re, uuid
from pathlib import Path
import sympy as sp

ROOT=Path(__file__).with_suffix('')
CAPTURE=json.loads((ROOT/'source.json').read_text())
SOURCE=CAPTURE['record']
KP_ID=17592186087844
KP_UUID=SOURCE[':knowledge-point/id']
TITLE=SOURCE[':knowledge-point/title']
VERSION='complex-root-asymptotes-v1'
x=sp.Symbol('x', real=True)
QS={q[':question/math-academy-id']:q for q in SOURCE[':knowledge-point/questions']}
# Each source's separately retained layout, stage sequence, and field shape.
SPECS={
 'q-80679':('easy','quadratic',dict(a=1,b=-4,c=5,n=1)),
 'q-80680':('easy','quadratic',dict(a=1,b=3,c=4,n=1)),
 'q-6912':('easy','quadratic',dict(a=3,b=0,c=1,n=2)),
 'q-39795':('moderate','gcf',dict(a=1,b=1,c=1,n=5)),
 'q-113525':('moderate','gcf',dict(a=1,b=1,c=7,n=3)),
 'q-113523':('moderate','group',dict(a=1,c=3,r=1,n=2,s=2)),
 'q-278551':('moderate','group',dict(a=2,c=1,r=1,n=4)),
 'q-270003':('moderate','group',dict(a=1,c=5,r=4,n=2,s=3)),
 'q-80676':('moderate','group',dict(a=1,c=4,r=2,n=2,s=1)),
 'q-113527':('moderate','group',dict(a=1,c=6,r=2,s=3)),
 'q-4694':('hard','cube',dict(r=3,n=2)),
 'q-270004':('hard','cube',dict(r=1,n=2,s=3)),
 'q-4698':('hard','quartic_cube',dict(p=2,q=1,s=1)),
}

def poly(e):
 """Polynomial TeX retaining source compact coefficient and power conventions."""
 P=sp.Poly(sp.expand(e),x); terms=[]
 for (power,),c in P.terms():
  if not c:continue
  mag=abs(c); v=('x' if power==1 else '{x}^{'+str(power)+'}') if power else ''
  cv='' if mag==1 and power else scalar(mag)
  term=cv+v
  terms.append(('-' if c<0 else '+' if terms else '')+term)
 return ''.join(terms) or '0'

def scalar(v):
 v=sp.Rational(v)
 return str(v.p) if v.q==1 else ('-' if v<0 else '')+r'\frac{'+str(abs(v.p))+'}{'+str(v.q)+'}'
def lin(r,coefficient=1):return poly(coefficient*x-r)
def quad(a,b,c):return poly(a*x*x+b*x+c)
def numerator(t,p):
 if t=='q-80680':return x+p['n']
 if t in ('q-6912','q-4694'):return p['n']*x
 if t=='q-113523':return p['n']*(x+p['s'])
 if t in ('q-270003','q-80676'):return p['n']*x-p['s']
 if t in ('q-113527','q-270004','q-4698'):return x*x-p['s']**2
 return sp.Integer(p['n'])
def math_data(t,p):
 family=SPECS[t][1]
 if family=='quadratic':a,b,c=(p[k] for k in ('a','b','c')); Q=a*x*x+b*x+c; D=Q;roots=[]
 elif family=='gcf':a,b,c=(p[k] for k in ('a','b','c'));Q=a*x*x+b*x+c; D=x*Q;roots=[sp.Integer(0)]
 elif family=='group':a,c,r=(p[k] for k in ('a','c','r'));b=0;Q=a*x*x+c;D=(x-r)*Q;roots=[sp.Integer(r)]
 elif family=='cube':r=p['r'];a=1;b=r;c=r*r;Q=x*x+r*x+r*r;D=(x-r)*Q*(p['n'] if t=='q-270004' else 1);roots=[sp.Integer(r)]
 else:
  v,w=p['p'],p['q'];a=v*v;b=-v*w;c=w*w;Q=a*x*x+b*x+c;D=x*(v*x+w)*Q;roots=[sp.Integer(0),-sp.Rational(w,v)]
 return numerator(t,p),sp.expand(D),Q,roots,(a,b,c)

def factor_num(t,p):
 if t=='q-113523':return str(p['n'])+'('+poly(x+p['s'])+')'
 if t=='q-113527':return '('+poly(x+p['s'])+')('+lin(p['s'])+')'
 if t in ('q-270004','q-4698'):return '('+lin(p['s'])+')('+poly(x+p['s'])+')' if t=='q-270004' else '('+poly(x+p['s'])+')('+lin(p['s'])+')'
 return poly(numerator(t,p))

def components(t,p):
 """Only whole polynomial/factor/equation components become slots; never digits."""
 N,D,Q,roots,(a,b,c)=math_data(t,p);family=SPECS[t][1]
 v={'num':poly(N),'den':poly(D),'Q':poly(Q),'factnum':factor_num(t,p)}
 if family=='quadratic':v['eq']=poly(Q)+'=0'
 if family=='gcf':v['factden']='x('+poly(Q)+')'
 if family=='group':
  L=lin(p['r']);v['factden']='('+poly(Q)+')('+L+')'
  v['groupden']=poly(a*x*x)+'('+L+')'+('+'+str(c) if c!=1 else '+')+'('+L+')'
 if family=='cube':
  r=p['r'];v['factden']=(''+str(p['n']) if t=='q-270004' else '')+'('+lin(r)+')('+poly(Q)+')'
  v['cube_exp']=('{x}^{3}-{'+str(r)+'}^{3}')
  if t=='q-270004':
   v['gcfden']=str(p['n'])+'('+poly(x**3-r**3)+')'
   v['cube_exp']=str(p['n'])+'('+v['cube_exp']+')'
   v['num_square']='{x}^{2}-{'+str(p['s'])+'}^{2}'
 if family=='quartic_cube':
  P,R=p['p'],p['q'];v['factden']='x('+poly(P*x+R)+')('+poly(Q)+')'
  v['gcfden']='x('+poly(P**3*x**3+R**3)+')'
  v['cube_exp']='x[('+poly(P*x)+')^{3}+{'+str(R)+'}^{3}]'
 # Full root equations and quadratic no-real-root equation.
 for i,r in enumerate(roots):v['root_'+str(i)]='x='+scalar(r)
 v['Qeq']=poly(Q)+'=0'
 if family in ('group','cube'):
  v['Leq']=lin(p['r'])+'=0';v['parenthesized_linear']='('+lin(p['r'])+')'
 if family=='quartic_cube':v['Leq']=poly(p['p']*x+p['q'])+'=0'
 return v

MATH_SPANS=re.compile(r'\$\$[\s\S]*?\$\$|\$[^$]*?\$')
def disc_block(t,p):
 _,_,_,_,(a,b,c)=math_data(t,p)
 old=QS[t][':question/worked-solution']
 found=[m.group(0) for m in MATH_SPANS.finditer(old) if r'\begin{aligned}D' in m.group(0)]
 if not found:return None
 base=SPECS[t][2]; _,_,_,_,(aa,bb,cc)=math_data(t,base)
 original=found[0]
 # Full arithmetic row masks preserve the source's exact number grouping style.
 start=original.split(r' \\  & =')
 assert len(start)==4
 if b<0:
  first=('('+str(b)+'{)}^{2}' if t=='q-80679' else '('+str(b)+')^{2}')+'-4('+str(a)+')('+str(c)+')'
 else:first='{'+str(b)+'}^{2}-4('+str(a)+')('+str(c)+')'
 return start[0]+r' \\  & ='+first+r' \\  & ='+str(b*b)+'-'+str(4*a*c)+r' \\  & ='+str(b*b-4*a*c)+('.' if start[3].startswith(str(bb*bb-4*aa*cc)+'.') else '')+r'\end{aligned}'+'\n$$'

def group(s,i):
 depth=0
 for j in range(i,len(s)):
  if s[j]=='{':depth+=1
  if s[j]=='}':
   depth-=1
   if depth==0:return s[i+1:j],j+1
 raise ValueError('Unbalanced source math group')

def render_text(t,key,p,raw):
 old=QS[t][key];base=SPECS[t][2];oldc=components(t,base);newc=components(t,p)
 # Fractions have complete independently masked numerator/denominator slots.
 # A scalar numerator MUST NOT replace a matching digit in a polynomial power.
 numerator_keys=('num','factnum','num_square')
 denominator_keys=('den','factden','groupden','gcfden','cube_exp')
 other_keys=[k for k in oldc if k not in numerator_keys]
 pairs={oldc[k]:newc[k] for k in other_keys if oldc[k]!=newc[k]}
 for k in other_keys:
  if oldc[k] in pairs:assert pairs[oldc[k]]==newc[k],(t,k)
 disc=disc_block(t,p)
 def span(m):
  txt=m.group(0)
  if r'\begin{aligned}D' in txt:return disc
  protected={}; edits=[]
  for f in re.finditer(r'\\(?:d?frac)\{',txt):
   n,i=group(txt,f.end()-1);d,end=group(txt,i)
   nk=next((k for k in numerator_keys if k in oldc and oldc[k]==n),None)
   dk=next((k for k in denominator_keys if k in oldc and oldc[k]==d),None)
   if nk is None or dk is None:continue
   token='@@FRACTION_'+str(len(protected))+'@@'
   protected[token]=txt[f.start():f.end()]+newc[nk]+'}{'+newc[dk]+'}'
   edits.append((f.start(),end,token))
  for start,end,token in reversed(edits):txt=txt[:start]+token+txt[end:]
  if pairs:
   pat=re.compile('|'.join(re.escape(k) for k in sorted(pairs,key=len,reverse=True)))
   txt=pat.sub(lambda z:pairs[z.group(0)],txt)
  for token,value in protected.items():txt=txt.replace(token,value)
  if t=='q-39795' and not raw:txt=txt.replace('$2x=0$','$x=0$')
  return txt
 return MATH_SPANS.sub(span,old)

# Parameterized complete observed banks. Meaning/intent of scalar error recipes
# remains unresolved; source banks are opt-in evidence, not inferred defaults.
def bank_sets(t,p):
 if t=='q-80679':return [[-1,p['c']],[],[1,p['c']],[1],[p['c']]]
 if t=='q-6912':
  a=p['a'];return [[-a,sp.Rational(1,a)],[-a,a],[-sp.Rational(1,a),a],[-sp.Rational(1,a),sp.Rational(1,a)],[]]
 if t=='q-39795':
  b=p['b'];return [[b,0],[0],[sp.Rational(b,2)],[-b,-sp.Rational(b,2)],[b,-b]]
 if t=='q-113525':
  b,c=p['b'],p['c'];return [[-b,0],[0],[-b],[-c,0],[b]]
 if t=='q-4694':
  r=p['r'];return [[],[r],[r*r],[-r,0,r],[-r]]
 if t=='q-80676':
  r=p['r'];return [[r],[-r,0],[-r,r],[-r],[0,r]]
 if t=='q-113527':
  r,c=p['r'],p['c'];return [[0,r],[c],[r],[-c],[r,c]]
 if t in ('q-278551','q-270003','q-270004'):return [[p['r']]]
 return []

def root_set(v):return tuple(sorted(set(sp.Rational(n) for n in v)))
def replace_option(t,value,values,p):
 """Whole x=value assignments are slots, retaining text/math separators."""
 base_sets=bank_sets(t,SPECS[t][2]);src=QS[t].get(':question/answer-fields',[])
 if not src:return value
 # position-specific equation substitution handles every complete root set.
 positions=list(re.finditer(r'x\s*=\s*(-?\\frac\{\d+\}\{\d+\}|-?\d+)',value))
 assert len(positions)==len(values),(t,value,values)
 out=value
 for m,v in reversed(list(zip(positions,values))):out=out[:m.start()]+'x='+scalar(v)+out[m.end():]
 return out

def authored_bank(t,roots,p,family):
 """Complete operation bank. Every wrong set is the real zero set of an
 explicitly malformed factorization or an erroneous numerator-zero selection.
 Return operations alongside sets; no diagnosis is added to learner content.
 """
 N,D,Q,_,abc=math_data(t,p);operations=[];polynomials=[]
 def add(label,polynomial):
  polynomials.append(sp.expand(polynomial));operations.append({'operation':label,'zeros_of':poly(sp.expand(polynomial))})
 add('correct_real_denominator_zeros',D)
 if not roots:
  operations=[];polynomials=[];add('correct_real_denominator_zeros',D)
  a,b,c=abc
  if b==0:
   for u,v in ((1,-1),(1,1),(-1,-1),(-1,1)):
    add('incorrect_sum_factorization_(x%+da)(ax%+d1)'%(u,v),(x+u*a)*(a*x+v))
  else:
   for u,v in ((1,1),(-1,1),(1,-1),(-1,-1)):
    add('incorrect_coefficient_as_factor_constants_signs_'+str((u,v)),(a*x+u*b)*(x+v*c))
 elif family=='gcf':
  b,c=p['b'],p['c']
  add('omit_real_GCF_factor_x',Q)
  add('incorrect_quadratic_factors_omit_x',(x+b)*(x+c))
  add('incorrect_quadratic_factors_retain_x',x*(x+b)*(x+c))
  add('incorrect_quadratic_factors_reverse_both_signs',x*(x-b)*(x-c))
 elif family=='group':
  r=p['r'];a,c=p['a'],p['c']
  add('omit_real_linear_factor',Q)
  add('reverse_real_linear_factor_sign',(x+r)*Q)
  add('replace_quadratic_power_by_linear_power',(x-r)*(a*x+c))
  add('replace_quadratic_power_and_reverse_constant_sign',(x-r)*(a*x-c))
 elif family=='cube':
  r=p['r']
  add('omit_real_cube_linear_factor',Q)
  add('reverse_real_cube_linear_factor_sign',(x+r)*Q)
  add('incorrectly_include_numerator_zeros',N*D)
  add('incorrectly_use_numerator_zeros_only',N)
 else:
  P,R=p['p'],p['q']
  add('omit_outer_GCF_x',(P*x+R)*Q)
  add('omit_cube_linear_factor',x*Q)
  add('omit_both_real_factors',Q)
  add('reverse_cube_linear_factor_sign',x*(P*x-R)*Q)
 # Exact operation roots, never random answer offsets or a source lookup.
 bank=[list(sorted(sp.polys.polytools.ground_roots(polynomial,x))) for polynomial in polynomials]
 if len(set(map(root_set,bank)))!=5:raise ValueError('Whole authored bank has equivalent choices')
 return bank,operations

def guard(t,p):
 if set(p)!=set(SPECS[t][2]):raise ValueError('Exact parameter keys required')
 if any(type(v)!=int for v in p.values()):raise ValueError('Integer parameters required')
 level,family,_=SPECS[t]
 if any(abs(v)>125 for v in p.values()):raise ValueError('Coefficient scope exceeded')
 if family=='quadratic':
  if not (1<=p['a']<=5 and abs(p['b'])<=7 and 1<=p['c']<=12 and 1<=p['n']<=6):raise ValueError('Easy bounds')
  if t=='q-6912' and (p['b']!=0 or p['c']!=1 or p['a']<2):raise ValueError('Positive quadratic source workload')
  if t!='q-6912' and (p['a']!=1 or p['b']==0):raise ValueError('Monic discriminant workload required')
 if family=='gcf':
  if not (p['a']==1 and 1<=p['b']<=4 and 1<=p['c']<=9 and 1<=p['n']<=6):raise ValueError('Moderate GCF bounds')
 if family=='group':
  if not (1<=p['a']<=3 and 1<=p['c']<=9 and 1<=p['r']<=5):raise ValueError('Moderate grouping bounds')
  if t=='q-278551' and not (2<=p['a']<=3 and p['c']==1):raise ValueError('Preserve nonunit quadratic coefficient')
  if t!='q-278551' and p['a']!=1:raise ValueError('Monic grouping workload')
  if 'n' in p and not (2 if t=='q-113523' else 1)<=p['n']<=6:raise ValueError('Numerator bounds')
  if 's' in p and not 1<=p['s']<=5:raise ValueError('Numerator bounds')
 if family=='cube':
  if not (1<=p['r']<=5 and 1<=p['n']<=5):raise ValueError('Hard cube bounds')
  if t=='q-4694' and p['r']<2:raise ValueError('Observed bank collision and cube workload')
  if 's' in p and not (1<=p['s']<=5 and p['n']>=2):raise ValueError('Hard numerator/GCF bounds')
 if family=='quartic_cube':
  if not (2<=p['p']<=3 and 1<=p['q']<=2 and 1<=p['s']<=4 and sp.gcd(p['p'],p['q'])==1):raise ValueError('Primitive rational-root cube bounds')
 N,D,Q,roots,(a,b,c)=math_data(t,p)
 if b*b-4*a*c>=0:raise ValueError('Quadratic factor must have complex roots')
 if sp.degree(sp.gcd(N,D),x)!=0:raise ValueError('Canceled holes belong to sibling KP')
 if not all(N.subs(x,r)!=0 for r in roots):raise ValueError('Numerator cancels real root')

def sample(t,rng):
 p=dict(SPECS[t][2]);family=SPECS[t][1]
 for _ in range(1000):
  if family=='quadratic':
   p['n']=rng.randint(1,6)
   if t=='q-6912':p['a']=rng.randint(2,5)
   else:p['b']=rng.choice([n for n in range(-7,8) if n]);p['c']=rng.randint(1,12)
  if family=='gcf':p.update(b=rng.randint(1,4),c=rng.randint(1,9),n=rng.randint(1,6))
  if family=='group':
   p.update(r=rng.randint(1,5),c=rng.randint(1,9))
   if t=='q-278551':p.update(a=rng.randint(2,3),c=1)
   if 'n' in p:p['n']=rng.randint(2 if t=='q-113523' else 1,6)
   if 's' in p:p['s']=rng.randint(1,5)
  if family=='cube':
   p.update(r=rng.randint(2 if t=='q-4694' else 1,5),n=rng.randint(2 if t=='q-270004' else 1,5))
   if 's' in p:p['s']=rng.randint(1,5)
  if family=='quartic_cube':p.update(p=rng.randint(2,3),q=rng.randint(1,2),s=rng.randint(1,4))
  try:guard(t,p);return dict(p)
  except ValueError:continue
 raise ValueError('No eligible parameter set')

def stable(v):return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False)
def uid(v):return str(uuid.uuid5(uuid.UUID(KP_UUID),stable(v)))

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('Unknown level')
 rng=random.Random(seed)
 eligible=[t for t,s in SPECS.items() if s[0]==level and (field_type is None or (QS[t].get(':question/answer-fields',[{':answer-field/type':{':db/ident':':answer-field.type/radio'}}])[0][':answer-field/type'][':db/ident'].endswith('/'+field_type)))]
 if not eligible:raise ValueError('No matching template/field layout')
 t=template or rng.choice(eligible)
 if t not in eligible:raise ValueError('Template/level/field mismatch')
 profile=profile or 'authored'
 if profile not in ('authored','original','supported-observed'):raise ValueError('Unknown profile')
 raw=profile=='original'; observed=profile!='authored'
 explicit=parameters is not None
 for _ in range(1000):
  p=dict(parameters) if explicit else sample(t,rng)
  guard(t,p);N,D,Q,roots,abc=math_data(t,p)
  src=QS[t];srcfields=src.get(':question/answer-fields',[])
  shape=srcfields[0][':answer-field/type'][':db/ident'].rsplit('/',1)[-1] if srcfields else 'radio'
  operations=[]
  try:
   if srcfields and shape=='blank':bank=[[roots[0]]];values=[scalar(roots[0])];types=[':answer.type/math'];correct=0
   elif observed and srcfields:
    bank=bank_sets(t,p);values=[replace_option(t,a[':answer/value'],b,p) for a,b in zip(srcfields[0][':answer-field/choices'],bank)]
    types=[a[':answer/type'][':db/ident'] for a in srcfields[0][':answer-field/choices']]
    orig_id=srcfields[0][':answer-field/correct'][':answer/id'];correct=next(i for i,a in enumerate(srcfields[0][':answer-field/choices']) if a[':answer/id']==orig_id)
   elif raw and not srcfields:bank=[];values=[];types=[];correct=None
   else:
    bank,operations=authored_bank(t,roots,p,SPECS[t][1]);values=['The function has no vertical asymptotes' if not b else ' and '.join('$x='+scalar(v)+'$' for v in b)+(' only' if len(b)==1 else '') for b in bank];types=[':answer.type/text']*5;correct=0
   if bank:
    if len(set(map(root_set,bank)))!=len(bank):raise ValueError('Ambiguous complete bank')
    if root_set(bank[correct])!=root_set(roots):raise ValueError('Incorrect complete designation')
   break
  except ValueError:
   if explicit:raise
 else:raise ValueError('No valid whole bank')
 prompt=render_text(t,':question/problem',p,raw)
 solution=render_text(t,':question/worked-solution',p,raw)
 body={'prompt':prompt,'solution':solution,'bank':sorted(zip(types,values)),'shape':shape if bank else None}
 content=hashlib.sha256(stable({'version':VERSION,**body}).encode()).hexdigest()
 question={':question/id':uid(['question',content]),':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution}
 if bank:
  key=srcfields[0][':answer-field/key'] if srcfields else 'selection'
  fid=uid(['field',content,key]); answers=[{':answer/id':uid(['answer',fid,ty,v]),':answer/type':ty,':answer/value':v} for ty,v in zip(types,values)]
  field={':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+shape,':answer-field/choices':answers,':answer-field/correct':[':answer/id',answers[correct][':answer/id']]}
  if srcfields and ':answer-field/prefix' in srcfields[0]:field[':answer-field/prefix']=srcfields[0][':answer-field/prefix']
  rng.shuffle(answers);question[':question/answer-fields']=[field]
 # Preserve absence of source fields in raw replay, not an artificial empty vector.
 # Source metadata is outside learner content; original profiles retain source IDs.
 if raw:
  for k,v in src.items():
   if k not in (':db/id',':question/id',':question/problem',':question/worked-solution',':question/answer-fields'):question[k]=v if not isinstance(v,dict) else v.get(':db/ident',v)
 task={'denominator_monic':str(sp.Poly(D,x).monic().as_expr())}
 if t in ('q-113523','q-113527','q-270004','q-4698'):task['factored_numerator_monic']=str(sp.Poly(N,x).monic().as_expr())
 fingerprint=hashlib.sha256(stable(task).encode()).hexdigest()
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':question,'generation':{'version':VERSION,'seed':seed,'level':level,'template':t,'profile':profile,'parameters':p,'source_id':src[':question/id'],'source_math_academy_id':t,'source_provenance':{k:CAPTURE[k] for k in ('database','basis','lineage')},'content_fingerprint':content,'mathematical_fingerprint':fingerprint,'authored_bank':bool(operations),'bank_operations':operations,'evidence_only':raw or (observed and bool(srcfields) and shape=='radio'),'eligible_for_learning':not raw and not (observed and bool(srcfields) and shape=='radio'),'supported_field_completion':not srcfields and not raw,'source_error_retained':t=='q-39795' and raw,'domain':'real x; quadratic discriminant < 0; numerator/denominator coprime'}}

# Easy: direct quadratic, no real denominator roots. No roots/cancellation branch.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# Moderate: exactly one real factor, GCF/grouping before excluding quadratic roots.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# Hard: cube identity, optional outer x/GCF, discriminant; primitive rational root.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)

def markdown(r):
 q=r['question'];out=q[':question/problem']+'\n\n'
 for f in q.get(':question/answer-fields',[]):
  correct=f[':answer-field/correct'][1]
  out+='\n'.join(('* ' if a[':answer/id']==correct else '- ')+a[':answer/value'] for a in f[':answer-field/choices'])+'\n\n'
 return out+q[':question/worked-solution']
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
 records=[generate(level,args.seed+i,args.template,profile=args.profile) for level in (['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]) for i in range(args.count)]
 print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
