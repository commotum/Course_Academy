#!/usr/bin/env python3
"""First-order Cartesian-to-cylindrical chain rule, math snapshot basis 1356.

Seven observed radio templates (four easy, three moderate), seven complete
observed expression banks; two explicitly authored hard templates. All levels
also have a complete authored operation bank. Source expression patterns are
replay profiles, not claims to have recovered distractor authoring intent.
Only polynomial Cartesian inputs and first derivatives in r/theta/z are used.
Stages keep derivative, substitution, distribution, and collection separate.
No plots, engine changes, database writes or registration. Stops at step 7.
Evidence/validation: generate/scratch/17592186124596/README.md.
"""
from __future__ import annotations
import argparse, hashlib, json, random, re, uuid
from pathlib import Path
import sympy as sp

KP_ID=17592186124596
KP_UUID='2ee45610-e14c-593e-9002-e2b2fcdb4517'
TITLE='Calculating the Derivative of a Cartesian Function With Respect to Cylindrical Polar Coordinates'
VERSION='cylindrical-chain-rule-1'
HERE=Path(__file__).with_suffix('')
CAPTURE=json.loads((HERE/'source.json').read_text())
SOURCES={q[':db/id']:q for q in CAPTURE['record'][':knowledge-point/questions']}
x,y,z,r,t=sp.symbols('x y z r theta',real=True)
sn,cs=sp.sin(t),sp.cos(t)
SUB={x:r*cs,y:r*sn}
TEMPLATES={
 'z_mixed':('easy','z',17592186125248,{'a':1,'b':1,'c':1},'f'),
 'z_square_cross':('easy','z',17592186360581,{'a':1,'b':1,'c':1},'u'),
 'z_single':('easy','z',17592186360583,{'a':2,'b':1,'c':4},'h'),
 'z_square_linear':('easy','z',17592186367921,{'a':1,'b':1},'f'),
 'theta_cancellation':('moderate','theta',17592186125243,{'a':1,'b':2},'f'),
 'theta_linear':('moderate','theta',17592186360582,{'a':2,'b':1},'v'),
 'r_cubic':('moderate','r',17592186368892,{'a':1,'b':1,'p':4,'q':2},'g'),
 'theta_coupled':('hard','theta',None,{'a':1,'b':2,'c':3,'k':3},'w'),
 'r_coupled':('hard','r',None,{'a':1,'b':2,'c':3,'p':3,'q':2},'w'),
}

def tex(e):
 """Small controlled printer: explicit products, grouped signed factors."""
 e=sp.sympify(e)
 if e.is_Integer: return str(e)
 if e.is_Rational: return (('-' if e<0 else '')+r'\frac{'+str(abs(e.p))+'}{'+str(e.q)+'}')
 if e.is_Symbol: return r'\theta' if e==t else str(e)
 if e.func in (sp.sin,sp.cos):
  fn=r'\sin' if e.func==sp.sin else r'\cos'
  return fn+(r'\theta' if e.args[0]==t else '('+tex(e.args[0])+')')
 if e.is_Add:
  out=''
  for v in e.args:
   s=tex(v);out+=('+' if out and not s.startswith('-') else '')+s
  return out
 if e.is_Mul:
  neg=e.could_extract_minus_sign()
  args=sp.Mul.make_args(-e if neg else e)
  vals=[]
  for v in args:
   if v==1:continue
   s=tex(v)
   vals.append('('+s+')' if v.is_Add or v.is_negative else s)
  return ('-' if neg else '')+r'\cdot '.join(vals)
 if e.is_Pow:
  b,n=e.args
  if b.func in (sp.sin,sp.cos) and b.args[0]==t:
   return (r'\sin' if b.func==sp.sin else r'\cos')+'^{'+tex(n)+r'}\theta'
  return ('('+tex(b)+')' if not b.is_Symbol else tex(b))+'^{'+tex(n)+'}'
 raise ValueError(('unsupported expression',e))

def add(terms):return sp.Add(*terms,evaluate=False) if len(terms)>1 else (terms[0] if terms else sp.Integer(0))
def pieces(e):return list(e.args) if e.is_Add else [e]
def polynomial(key,p):
 a,b,c=p['a'],p['b'],p.get('c',1)
 return add({
  'z_mixed':[a*x*y,b*y**2*z,c*x*z**2],
  'z_square_cross':[a*x**2*z**2,b*x**2*y**2,c*x*y*z],
  'z_single':[a*x**2,b*y**2,c*x**2*z**2],
  'z_square_linear':[a*y**2*z**2,b*x*z],
  'theta_cancellation':[a*x**2,a*y**2,b*y*z],
  'theta_linear':[a*y,-b*x*z],
  'r_cubic':[a*x**3*z**p.get('p',4),b*y**3*z**p.get('q',2)],
  'theta_coupled':[z**p.get('k',3)*add([a*x**2,b*x*y,c*y**2])],
  'r_coupled':[a*x**2*z**p.get('p',3),b*x*y*z**p.get('q',2),c*y**2*z**p.get('p',3)],
 }[key])

def check_parameters(key,p):
 expected=set(TEMPLATES[key][3])|{'name'}
 if set(p)!=expected:raise ValueError(f'Expected parameter keys {sorted(expected)}')
 if p['name'] not in ('f','g','h','u','v','w'):raise ValueError('unsupported function name')
 for k in expected-{'name'}:
  if type(p[k]) is not int:raise ValueError('integer parameters required')
  if k in ('a','b','c') and not 1<=abs(p[k])<=5:raise ValueError('nonzero signed coefficients with absolute value 1..5 required')
 if key=='r_cubic' and not 1<=p['q']<p['p']<=4:raise ValueError('radial cubic requires 1 <= q < p <= 4')
 if key=='theta_coupled' and not 2<=p['k']<=4:raise ValueError('hard angular requires 2 <= k <= 4')
 if key in ('theta_coupled','r_coupled') and p['a']==p['c']:raise ValueError('hard coupled terms require unequal a,c')
 if key=='r_coupled' and not (2<=p['p']<=4 and 1<=p['q']<=3 and p['p']!=p['q']):raise ValueError('hard radial requires p=2..4, q=1..3, p != q')

def sample(key,rng):
 p={k:rng.choice([-5,-4,-3,-2,-1,1,2,3,4,5]) for k in TEMPLATES[key][3]}
 p['name']=rng.choice(('f','g','h','u','v','w'))
 if key=='r_cubic':p['p'],p['q']=rng.choice([(2,1),(3,1),(3,2),(4,1),(4,2),(4,3)])
 if key=='theta_coupled':p['k']=rng.randint(2,4)
 if key=='r_coupled':p['p'],p['q']=rng.choice([(a,b) for a in range(2,5) for b in range(1,4) if a!=b])
 return p

def math_data(key,p):
 target=TEMPLATES[key][1];F=polynomial(key,p)
 deriv={v:sp.diff(F,v) for v in (x,y,z)}
 sub={v:d.subs(SUB) for v,d in deriv.items()}
 branches=[sub[z]] if target=='z' else ([-r*sn*sub[x],r*cs*sub[y]] if target=='theta' else [cs*sub[x],sn*sub[y]])
 distributed=[]
 if target!='z':
  for d,factor in ((sub[x],-r*sn if target=='theta' else cs),(sub[y],r*cs if target=='theta' else sn)):
   distributed.extend([term*factor for term in pieces(sp.expand(d))])
 else:distributed=pieces(sub[z])
 final=sp.expand(add(branches))
 if key=='z_square_cross':final=r**2*add([2*p['a']*z*cs**2,sp.Rational(1,2)*p['c']*sp.sin(2*t)])
 if key=='r_cubic':final=3*r**2*z**p['q']*add([p['a']*z**(p['p']-p['q'])*cs**3,p['b']*sn**3])
 if key=='theta_coupled':final=r**2*z**p['k']*add([(p['c']-p['a'])*sp.sin(2*t),p['b']*sp.cos(2*t)])
 return F,deriv,sub,branches,distributed,final

def observed_bank(key,p,correct):
 """Parameterized observed expression shapes; unresolved intent stays metadata."""
 a,b,c=p['a'],p['b'],p.get('c',1)
 if key=='z_mixed':return [b*r**2*sn+2*c*r*cs,a*r*cs+2*c*r*z*sn,correct,b*r**2*sp.sin(2*t)+c*r*z**2*cs,a*r*sn+c*z**2]
 if key=='z_square_cross':return [r**2*(2*a*z*sp.cos(2*t)+sp.Rational(1,2)*c*sn**2),2*r**2*(a*z*cs**2+c*sp.sin(2*t)),2*a*z*cs**2+sp.Rational(1,2)*c*sp.sin(2*t),a*sp.cos(2*t)+c*r**2*z*sp.sin(2*t),correct]
 if key=='z_single':return [2*c*z,2*c*z+b*r**2*cs**2,correct,2*c*z+b*r**2*sn**2,2*c*r**2*z*sn**2]
 if key=='z_square_linear':return [r*(a*sn**2+b*cs),correct,2*a*z+b*r**2*cs**2,2*a*r**2*z*cs**2+b*sn,b*r**2*cs+a*sn**2]
 if key=='theta_cancellation':return [b*r*z*sn**2,a*r**2*sp.sin(2*t)-a*r*cs,correct+a*r**2*sn,a*r**2*sn,correct]
 if key=='theta_linear':return [a*r*sn+b*z*cs,b*z*sp.cos(2*t)+a*r*sn**2,correct,b*z*cs**2+a*r*sp.sin(2*t),b*z*sn**2+a*r*cs**2]
 if key=='r_cubic':return [3*r**2*(a*z**(p['p']-p['q'])*cs**2+b*sn**2),3*r**2*z**p['q']*(a*sp.cos(3*t)+b*sp.sin(3*t)),a*z**(p['p']-p['q'])*cs**3+b*sn**3,r**2*z*(a*z**(p['p']-1)*cs**3+b*z**(p['q']-1)*sn**3),correct]
 raise ValueError('No observed bank for authored template')

def authored_bank(key,p,data):
 F,deriv,sub,branches,distributed,correct=data
 if TEMPLATES[key][1]=='z':
  return [correct,-correct,deriv[z].subs({x:r*sn,y:r*cs}),deriv[z].subs({x:cs,y:sn}),2*correct]
 return [correct,-branches[0]+branches[1],branches[0],branches[1],sub[x]+sub[y]]

def equal(a,b):
 # All eligible expressions are polynomials in sin(theta),cos(theta),r,z.
 # Reduce the exact expanded polynomial modulo C^2+S^2=1; unlike repeated
 # general trig simplification this gives a quick complete bank guard.
 diff=sp.expand(sp.expand_trig(a-b))
 if diff==0:return True
 C,S=sp.symbols('_cos _sin')
 diff=diff.xreplace({cs:C,sn:S})
 return sp.Poly(diff,C,S,domain='EX').rem(sp.Poly(C**2+S**2-1,C,S,domain='EX')).is_zero
def guard_bank(bank):
 if len(bank)!=5 or any(v.has(sp.zoo,sp.nan,sp.oo,-sp.oo) for v in bank):raise ValueError('invalid complete bank')
 if any(equal(a,b) for i,a in enumerate(bank) for b in bank[i+1:]):raise ValueError('ambiguous complete bank')

def derivative(name,v):return r'\frac{\partial '+name+r'}{\partial '+(r'\theta' if v=='theta' else v)+'}'
def aligned(rows):return r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}'
def solution_blocks(key,p,data):
 name=p['name'];target=TEMPLATES[key][1];F,deriv,sub,branches,dist,final=data
 D=lambda v:derivative(name,v)
 chain='+'.join(D(v)+r'\cdot '+derivative(v,target) for v in ('x','y','z'))
 formula=D('z') if target=='z' else ('-'+D('x')+r'\cdot r\cdot \sin\theta+'+D('y')+r'\cdot r\cdot \cos\theta' if target=='theta' else D('x')+r'\cdot \cos\theta+'+D('y')+r'\cdot \sin\theta')
 block0=aligned([D(target)+' & ='+chain,' & ='+formula+'.'])
 rawvars=('z',) if target=='z' else ('x','y')
 block1=aligned([r',\,'.join(D(v)+'='+tex(deriv[{'x':x,'y':y,'z':z}[v]]) for v in rawvars)])
 if target=='z':
  rows=[D('z')+' & ='+tex(sub[z])]
  if key=='z_square_cross':rows.append(' & ='+tex(final))
  rows[-1]+='.'
  return [block0,block1,aligned(rows)]
 block2=aligned([D(v)+' & ='+tex(sub[{'x':x,'y':y}[v]])+('.' if i==1 else ',') for i,v in enumerate(rawvars)])
 first=('-('+tex(sub[x])+r')\cdot r\cdot \sin\theta+('+tex(sub[y])+r')\cdot r\cdot \cos\theta') if target=='theta' else ('('+tex(sub[x])+r')\cdot \cos\theta+('+tex(sub[y])+r')\cdot \sin\theta')
 rows=[D(target)+' & ='+first]
 # Source linear/cubic solutions directly collect after their substituted sum.
 if key not in ('theta_linear','r_cubic'):rows.append(' & ='+tex(add(dist)))
 rows.append(' & ='+tex(final)+'.')
 return [block0,block1,block2,aligned(rows)]

def presentation(key,p,data):
 level,target,sid,_,base_name=TEMPLATES[key]
 F=data[0];name=p['name'];blocks=solution_blocks(key,p,data)
 if sid:
  src=SOURCES[sid]
  # Slot boundaries are complete RHS/function components, never short symbols.
  prompt=re.sub(r'(\$)[fghuvw]\(x,y,z\)=.*?(,\$)',lambda m:'$'+name+'(x,y,z)='+tex(F)+',$',src[':question/problem'],count=1)
  prompt=prompt.replace('∂'+base_name,'∂'+name)
  chunks=src[':question/worked-solution'].split('$$')
  if len(blocks)!=(len(chunks)-1)//2:raise AssertionError('source stage count')
  for i,b in enumerate(blocks):chunks[2*i+1]='\n'+b+'\n'
  sol='$$'.join(chunks)
  sol=sol.replace('$'+base_name+'(', '$'+name+'(').replace('$'+base_name+'$', '$'+name+'$')
 else:
  prompt='Given that $'+name+'(x,y,z)='+tex(F)+',$ find $'+derivative(name,target)+',$ where $(x,y,z)$ are Cartesian coordinates and $(r,\\theta,z)$ are the corresponding cylindrical polar coordinates.'
  opening='Applying the multivariable chain rule for the function $'+name+'(x,y,z)$ with three independent variables $r,\\theta,$ and $z,$ where $x=r\\cos\\theta,y=r\\sin\\theta,$ and $z=z,$ we have'
  prose=[opening,'First, we find the partial derivatives of $'+name+'$ with respect to $x$ and $y:$','Writing the above results in terms of $r,\\theta,$ and $z,$ we get','Finally, substituting these into our chain rule formula, we get']
  sol='\n\n'.join(s+'\n\n$$\n'+b+'\n$$' for s,b in zip(prose,blocks,strict=True))
 return prompt,sol

def fingerprint(data,target):
 # Incidental z-independent coefficients do not affect z-derivative demand.
 deriv=data[1]
 demands=[deriv[z]] if target=='z' else [deriv[x],deriv[y]]
 return hashlib.sha256(json.dumps({'target':target,'partials':[sp.srepr(sp.expand(v)) for v in demands]},sort_keys=True).encode()).hexdigest()

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('unknown difficulty')
 if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('only observed radio layout supported')
 rng=random.Random(seed);keys=[k for k,v in TEMPLATES.items() if v[0]==level]
 if template is None:template=rng.choice(keys)
 if template not in keys:raise ValueError('template/difficulty mismatch')
 sid=TEMPLATES[template][2]
 if profile is None:profile='authored_operations'
 if profile not in ('authored_operations','observed') or profile=='observed' and sid is None:raise ValueError('profile unavailable')
 for attempt in range(1000):
  p=dict(parameters) if parameters is not None else sample(template,rng)
  try:
   check_parameters(template,p);data=math_data(template,p)
   bank=observed_bank(template,p,data[-1]) if profile=='observed' else authored_bank(template,p,data)
   guard_bank(bank)
  except ValueError:
   if parameters is not None:raise
   continue
  break
 else:raise RuntimeError('no eligible complete bank')
 prompt,sol=presentation(template,p,data)
 if profile=='authored_operations' and TEMPLATES[template][1]=='z':
  # The same letter z denotes two coordinates; state the two holding rules.
  convention='The derivative requested holds $r$ and $\\theta$ fixed. In the Cartesian partial derivative on the right of the chain rule, $x$ and $y$ are held fixed; we then substitute $x=r\\cos\\theta$ and $y=r\\sin\\theta$.'
  sol=sol.replace('First, we find',convention+'\n\nFirst, we find',1)
 values=[tex(v) for v in bank];correct=next(i for i,v in enumerate(bank) if equal(v,data[-1]))
 identity={'version':VERSION,'prompt':prompt,'solution':sol,'bank':sorted(values),'correct':values[correct]}
 digest=hashlib.sha256(json.dumps(identity,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
 qid=str(uuid.uuid5(uuid.NAMESPACE_URL,'cylindrical:'+digest));fid=str(uuid.uuid5(uuid.UUID(qid),'selection'))
 answers=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),value)),':answer/type':':answer.type/math',':answer/value':value} for value in values]
 cid=answers[correct][':answer/id'];rng.shuffle(answers)
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':sol,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',cid]}]},'generation':{'version':VERSION,'seed':seed,'template':template,'profile':profile,'parameters':p,'content_sha256':digest,'mathematical_fingerprint':fingerprint(data,TEMPLATES[template][1]),'source_ids':[sid] if sid else [],'authored_template':sid is None,'bank_interpretation':'observed parameterized shapes; original error intent unresolved' if profile=='observed' else 'complete authored method-operation bank','domain':'r >= 0; theta,z real; x=r cos(theta), y=r sin(theta), Cartesian z=cylindrical z','provenance':{k:CAPTURE[k] for k in ('database','basis','lineage')},'dependencies':{'sympy':sp.__version__},'plot_rating':'none','source_solution_repairs':['17592186360582: replace dy factor numerator v by y in initial chain row'] if sid==17592186360582 else []}}

# Easy: four observed z-derivative families; z stays the same coordinate.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):
 """Differentiate in the unchanged z coordinate, then substitute x/y.

 Four observed polynomial families retain one or two surviving z terms;
 one collects a sin(2 theta) expression. Cartesian x/y are fixed during
 differentiation, cylindrical r/theta are fixed in the requested derivative.
 All coefficients are nonzero signed integers with absolute value 1..5;
 original powers are fixed, including square z terms. No inverse transforms,
 evaluation points or higher derivatives. Exactly one five-option radio.
 """
 return generate('easy',seed,template,field_type,parameters,profile)
# Moderate: two angular families and a radial cubic family; two chain paths.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):
 """Use the two first-order r/theta branches after Cartesian differentiation.

 Observed peers: angular cancellation, angular linear mixed z term, and
 radial cubic powers. Preserve substitution before distribution/collection.
 Nonzero signed coefficients have absolute value 1..5; radial z exponents
 obey 1 <= q < p <= 4. No new branch or progression within this level.
 Exactly one five-option radio; no inverse, spherical or higher derivatives.
 """
 return generate('moderate',seed,template,field_type,parameters,profile)
# Hard: authored coupled quadratic terms, four nonzero distributed contributions.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):
 """Authored canonical peers with four nonzero distributed chain products.

 Angular z^k(a x^2+bxy+c y^2): 2 <= k <= 4. Radial heterogeneous z-power
 quadratic: p=2..4, q=1..3 and p != q. Both require a != c and all a,b,c
 nonzero signed integers with absolute value 1..5. The cross term cannot
 disappear. Collection uses the existing first-order cylindrical method,
 without inverse transforms, spherical coordinates or higher derivatives.
 Exactly one five-option radio. This missing-level scope is authored,
 not an observed source difficulty classification.
 """
 return generate('hard',seed,template,field_type,parameters,profile)

def markdown(rec):
 q=rec['question'];f=q[':question/answer-fields'][0]
 return q[':question/problem']+'\n\n'+'\n'.join(f'{i}. ${a[":answer/value"]}$' for i,a in enumerate(f[':answer-field/choices'],1))+'\n\n'+q[':question/worked-solution']
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile',choices=['observed','authored_operations']);args=ap.parse_args()
 levels=['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]
 out=[generate(l,args.seed+i,args.template,profile=args.profile) for l in levels for i in range(args.count)]
 print(json.dumps(out,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(markdown(v) for v in out))
if __name__=='__main__':main()
