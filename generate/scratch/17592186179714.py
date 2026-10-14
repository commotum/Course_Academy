#!/usr/bin/env python3
"""Gradient vector fields: eight source-backed templates, E/M; no database I/O.

Each template retains its entire observed five-choice bank. Fixed variable
order x,y[,z] and derivative/assembly stages are instructional constraints.
Integer coefficient slots preserve the source operations and workload.
"""
import argparse, functools, hashlib, itertools, json, random, sys, uuid
from pathlib import Path
import sympy as s
from sympy.simplify.fu import fu
sys.dont_write_bytecode=True
HERE=Path(__file__).with_suffix('')
RAW=json.loads((HERE/'source.json').read_text());KP=RAW['kp']
VERSION='gradient-vector-fields-1.0.0'
NS=uuid.UUID(KP[':knowledge-point/id'])
x,y,z=s.symbols('x y z',real=True)
TEMPLATES={
 'separate_roots':('easy','q-122607',dict(a=2,b=-1,c=4,d=1)),
 'linear_log':('easy','q-122599',dict(a=2,b=4)),
 'linear_tan':('easy','q-122608',dict(a=1,b=-2)),
 'product_log':('moderate','q-122404',dict(a=2)),
 'radial_root':('moderate','q-122596',dict(a=1,b=1,c=1)),
 'product_sine':('moderate','q-122600',dict(a=2)),
 'product_arctan':('moderate','q-122601',dict(a=1)),
 'mixed_polynomial':('moderate','q-122617',dict(a=1,b=1,c=1)),
}
SOURCES={q[':question/math-academy-id']:q for q in KP[':knowledge-point/questions']}
DOMAINS={
 'separate_roots':'a*x+b>0 and c*y+d>0 (differentiable real domain)',
 'linear_log':'a*x+b*y>0',
 'linear_tan':'cos(a*x+b*y)!=0',
 'product_log':'z-a*y>0',
 'radial_root':'(x,y,z)!=(0,0,0); positive weights',
 'product_sine':'R^3','product_arctan':'R^3','mixed_polynomial':'R^3',
}
BOUNDS={
 'separate_roots':dict(a=list(range(2,7)),b=list(range(-3,4)),c=list(range(2,7)),d=list(range(-3,4))),
 'linear_log':dict(a=list(range(2,7)),b=list(range(2,7))),
 'linear_tan':dict(a=list(range(1,5)),b=list(range(-6,-1))),
 'product_log':dict(a=list(range(2,7))),
 'radial_root':dict(a=list(range(1,5)),b=list(range(1,5)),c=list(range(1,5))),
 'product_sine':dict(a=list(range(2,7))),
 'product_arctan':dict(a=list(range(1,7))),
 'mixed_polynomial':dict(a=list(range(1,5)),b=list(range(1,5)),c=list(range(1,5))),
}
def digest(o):return hashlib.sha256(json.dumps(o,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def tex(v):return s.latex(v).replace(r'\log',r'\ln').replace(r'\operatorname{atan}',r'\arctan')
@functools.lru_cache(maxsize=10000)
def equal(a,b):
 if a==b:return True
 d=s.expand(a-b)
 if d==0:return True
 if d.has(s.tan,s.sec,s.sin,s.cos):
  for point in ({x:0,y:0,z:1},{x:s.pi/3,y:0,z:1},{x:0,y:s.pi,z:0}):
   value=s.simplify(d.subs(point))
   if value.is_zero is False and value.is_finite is True:return False
  return fu(d)==0
 return s.simplify(d)==0
def vector_tex(v):
 out=''
 for e,unit in zip(v,('i','j','k')):
  term=tex(e)
  if isinstance(e,s.Add):term=r'\left('+term+r'\right)'
  out+=('+' if out and not term.startswith('-') else '')+term+r'\,'+unit
 return out
def model(template,p):
 a=p['a'];b=p.get('b');c=p.get('c');d=p.get('d')
 variables=(x,y) if TEMPLATES[template][0]=='easy' else (x,y,z)
 if template=='separate_roots':
  A=s.sqrt(a*x+b);C=s.sqrt(c*y+d);AA=s.sqrt(c*x+b);CC=s.sqrt(a*y+d)
  f=A-C;bank=[(c/(2*AA),-a/(2*CC)),(a/(2*A),c/C),(a/(2*AA),-a/CC),(a/A,a/(2*C)),(a/(2*A),-c/(2*C))]
 elif template=='linear_log':
  u=a*x+b*y;f=s.log(u);bank=[(a/u,b/u),(1/u,1/u),(b/u,a/u),(b/(x+y),a/(x+y)),(a/(a*x+y),1/(a*x+y))]
 elif template=='linear_tan':
  u=a*x+b*y;f=s.tan(u);h=s.sec(u)**2;v=s.sec(u)
  bank=[(a*h,-a*h),(a*x*h,b*y*h),(a*v,b*v),(b*v,a*v),(a*h,b*h)]
 elif template=='product_log':
  u=z-a*y;f=x*s.log(u);bank=[(s.log(u),-a*x/u,x/u),(a*s.log(u),x/u,a*x/u),(s.log(u),-x/u,-x/u),(a*s.log(u),-a*x/u,x/u),(s.log(u),a*x/u,a*x/u)]
 elif template=='radial_root':
  u=a*x*x+b*y*y+c*z*z;v=s.sqrt(u);f=v
  bank=[(a*y*z/v,b*x*z/v,c*x*y/v),(a*y*z*v,b*x*z*v,c*x*y*v),(a*x/v,b*y/v,c*z/v),(2*a*y*z/u,2*b*x*z/u,2*c*x*y/u),(2*a*x*v,2*b*y*v,2*c*z*v)]
 elif template=='product_sine':
  u=x*z+a*y;f=s.sin(u);h=s.cos(u);v=s.sin(u)
  bank=[((z+a*y)*h,a*h,(x+a*y)*h),(z*h,a*h,x*h),(x*h,a*h,z*h),(x*h,a*y*h,z*h),(z*v,a*v,x*v)]
 elif template=='product_arctan':
  u=a*x*y*z;v=1+u*u;f=s.atan(u)
  bank=[(a*y*z/(u+1),a*z*z/(u+1),a*x*y/(u+1)),(a*x*y*z/v,)*3,(a*x/v,a*y/v,a*z/v),(a*y*z/v,a*x*z/v,a*x*y/v),(a/v,)*3]
 elif template=='mixed_polynomial':
  f=a*z*x*x+b*x*y**3-c*y*z**4
  bank=[(2*a*x*z+b*y**3,6*b*x*y*y+c*z**4,a*x-4*c*y*z**3),(a*x*z+b*y**3,3*b*y*y-c*z**4,a*x*x-4*c*z**3),(2*a*x*z+b*y**3,3*b*x*y*y-c*z**4,a*x*x-4*c*y*z**3),(2*a*x*z+b*y*y,6*b*x*y-c*z**4,a*x*x-8*c*y**3),(2*a*x+b*y*y,3*b*x*y-c*z**4,a*x*x-8*c*y*z*z)]
 else:raise ValueError(template)
 grad=tuple(s.diff(f,v) for v in variables)
 if template=='linear_tan':grad=(a*s.sec(u)**2,b*s.sec(u)**2)
 # Compare vector components, never vector magnitudes or separate equation sides.
 matches=[i for i,w in enumerate(bank) if all(equal(v,q) for v,q in zip(w,grad))]
 if len(matches)!=1 or any(all(equal(v,q) for v,q in zip(A,B)) for A,B in itertools.combinations(bank,2)):
  raise ValueError('Ambiguous complete bank')
 return f,variables,grad,bank,matches[0]
def guard(template,p):
 if set(p)!=set(BOUNDS[template]) or any(type(v) is not int or v not in BOUNDS[template][k] for k,v in p.items()):raise ValueError('Parameter bounds')
 if template in ('separate_roots','linear_log') and p['a']==p.get('c',p.get('b')):raise ValueError('Distinct chain coefficients required')
 if template=='linear_tan' and p['b']==-p['a']:raise ValueError('Duplicate source recipe')
def generate(difficulty,seed=0,template=None,parameters=None,profile='observed'):
 if difficulty not in ('easy','moderate'):raise ValueError('Unsupported difficulty: no hard source-backed backbone')
 rng=random.Random(seed)
 template=template or rng.choice([t for t,q in TEMPLATES.items() if q[0]==difficulty])
 if template not in TEMPLATES or TEMPLATES[template][0]!=difficulty:raise ValueError('Wrong template level')
 if profile!='observed':raise ValueError('Unknown bank profile')
 for _ in range(200):
  p=dict(parameters) if parameters is not None else {k:rng.choice(v) for k,v in BOUNDS[template].items()}
  try:guard(template,p);f,variables,grad,bank,ci=model(template,p);break
  except ValueError:
   if parameters is not None:raise
 else:raise ValueError('Bounded sampler exhausted')
 identity_function=f
 if template=='linear_log':identity_function=s.log((p['a']*x+p['b']*y)/s.igcd(p['a'],p['b']))
 signature=digest({'function':s.srepr(identity_function),'domain':DOMAINS[template],'level':difficulty})
 # The bank is deterministic per task; seed and option order do not enter identity.
 bank_identity=digest([[s.srepr(s.cancel(e)) for e in v] for v in bank])
 qid=str(uuid.uuid5(NS,'gradient:'+signature+':bank:'+bank_identity));fid=str(uuid.uuid5(uuid.UUID(qid),'field:selection'))
 choices=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),'recipe:'+str(i))),':answer/type':':answer.type/math',':answer/value':vector_tex(v)} for i,v in enumerate(bank)]
 args=','.join(map(str,variables));fn=tex(f)
 partial=[]
 for v,e in zip(variables,grad):partial.extend([r'f_{'+str(v)+r'}('+args+r')&=\frac{\partial}{\partial '+str(v)+'}'+r'\left('+fn+r'\right)',r'&='+tex(e)])
 deriv=r'\begin{aligned}'+r' \\ '.join(partial)+r'\end{aligned}'
 assembly='+'.join('f_{'+str(v)+'}('+args+r')\,'+unit for v,unit in zip(variables,('i','j','k')))
 sol='The gradient vector field of a function $f$ is given by $\\nabla f.$\n\nFirst, we find the partial derivatives:\n\n$$\n'+deriv+'\n$$\n\nTherefore, the gradient vector field of $f('+args+')$ is\n\n$$\n'+r'\begin{aligned}\nabla f('+args+')&='+assembly+r' \\ &= '+vector_tex(grad)+r'.\end{aligned}'+'\n$$'
 q={':question/id':qid,':question/problem':'Find the gradient vector field of the function $f('+args+')='+fn+'.$',':question/worked-solution':sol,':question/difficulty':':question.difficulty/'+difficulty,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',choices[ci][':answer/id']]}]}
 return {'knowledge_point':{'db_id':KP[':db/id'],'id':KP[':knowledge-point/id'],'title':KP[':knowledge-point/title']},'question':q,'generation':{'generator_version':VERSION,'dependency_versions':{'sympy':s.__version__},'seed':seed,'template':template,'profile':profile,'parameters':p,'source_id':TEMPLATES[template][1],'source_basis':RAW['basis'],'lineage':RAW['lineage'],'domain':DOMAINS[template],'mathematical_fingerprint':signature,'recipe_indices':list(range(5)),'eligible_for_learning':True}}
def replay(template):
 """Original parameters and complete bank; mathematical fidelity is checked externally."""
 return generate(TEMPLATES[template][0],template=template,parameters=TEMPLATES[template][2])
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--template',choices=list(TEMPLATES));ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['json','markdown'],default='json');a=ap.parse_args()
 levels=['easy','moderate'] if a.difficulty=='all' else [a.difficulty]
 if a.count<1:ap.error('count must be positive')
 records=[];seen=set()
 for level in levels:
  n=0
  for attempt in range(a.count*100):
   if n==a.count:break
   r=generate(level,a.seed+attempt,template=a.template);fp=r['generation']['mathematical_fingerprint']
   if fp in seen:continue
   seen.add(fp);records.append(r);n+=1
  if n!=a.count:raise ValueError('Finite validated domain exhausted; shortage remains explicit')
 if a.format=='json':print(json.dumps(records,indent=2))
 else:print('\n\n---\n\n'.join(r['question'][':question/problem']+'\n\n'+r['question'][':question/worked-solution']+'\n\n'+json.dumps(r['question'][':question/answer-fields'],indent=2) for r in records))
if __name__=='__main__':main()
