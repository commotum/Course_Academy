#!/usr/bin/env python3
"""Vector composition chain rule, math basis 1356; generator stages 3–7 only.
Twelve source sequences/banks are explicit parameterized mathematical recipes.
Default banks are authored method errors; observed compound banks are opt-in.
No EDB clients, transactions, registration, plots, or answer lookup branches.
"""
from __future__ import annotations
import argparse, hashlib, json, random, re, uuid
from pathlib import Path
import sympy as S

KP_ID=17592186115392
KP_UUID='a146d5d3-2562-5b8b-886e-4cf6519d3282'
TITLE='Using the Chain Rule for Differentiation'
VERSION='vector-chain-v1'
ROOT=Path(__file__).with_suffix('')
SOURCE=json.loads((ROOT/'source.json').read_text())
QUESTIONS={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
t,u=S.symbols('t u',real=True)
U=S.Function('u')(t)

# Bounds apply to explicit calls as well as deterministic samples. n is fixed
# per source family: easy does not invent a multi-term inner or fourth component.
SPECS={
 'linear_quadratic_affine':('q-32498','matrix',dict(a=2,b=2,c=2,d=3)),
 'cos_quadratic_power':('q-32866','basis',dict(a=1,n=3,c=1,d=12)),
 'sin_log_tan_power':('q-128563','angle',dict(a=1,n=2,c=2)),
 'linear_quadratic_exp':('q-128572','matrix',dict(a=1,c=1,d=6)),
 'linear_vector_power':('q-32502','basis',dict(a=1,n=2,c=1,d=2,e=3)),
 'log_quadratic_log':('q-32860','matrix',dict(a=1,c=5)),
 'log_reciprocal_exp':('q-32869','angle',dict(a=2)),
 'two_exp_power':('q-33260','basis',dict(a=2,n=2,b=1,c=2)),
 'sin_cos_exp_affine':('q-71222','matrix',dict(a=4,b=-3)),
 'log_power_root_exp':('q-128561','basis',dict(a=-1)),
 'reciprocal_log_reciprocal':('q-128570','angle',dict(a=1,b=1,c=1)),
 'cos_cube_log_exp':('q-70695','matrix',dict(a=1)),
}
TEMPLATES={k:'easy' for k in SPECS}|{'mixed_quadratic_inner':'moderate','mixed_cubic_inner':'hard'}
REPAIRS={
 'q-32866':'The prompt f(t) contains u; change the function label to f(u).',
 'q-32502':'Outer derivative of 3u incorrectly shows d/dt; change it to d/du.',
 'q-32860':'The opening chain rule labels f, while the displayed function is g; use g.',
 'q-33260':'The outer derivative row e^(u+1)+2e^(2t) incorrectly changes the variable; use 2e^(2u).',
}

def math_data(name,p):
 a=S.Integer(p['a'])
 if name=='linear_quadratic_affine':f=[p['c']*u,u**2,S.Integer(p['d'])];h=a*t+p['b']
 elif name=='cos_quadratic_power':f=[S.cos(u),p['c']-u**2,S.Integer(p['d'])];h=a*t**p['n']
 elif name=='sin_log_tan_power':f=[S.sin(u),S.log(p['c']*u),S.tan(u)];h=a*t**p['n']
 elif name=='linear_quadratic_exp':f=[p['c']*u,u**2,S.Integer(p['d'])];h=S.exp(a*t)
 elif name=='linear_vector_power':f=[p['c']*u,p['d']*u,p['e']*u];h=a*t**p['n']
 elif name=='log_quadratic_log':f=[S.log(u),S.Integer(p['c']),u**2];h=a*S.log(t)
 elif name=='log_reciprocal_exp':f=[S.log(u),S.Integer(0),1/u];h=S.exp(a*t)
 elif name=='two_exp_power':f=[S.exp(u+p['b']),S.exp(p['c']*u),1/S.E];h=a*t**p['n']
 elif name=='sin_cos_exp_affine':f=[S.sin(u),S.cos(u),S.exp(u)];h=a*t+p['b']
 elif name=='log_power_root_exp':f=[S.log(u),u**2,S.sqrt(u)];h=S.exp(a*t)
 elif name=='reciprocal_log_reciprocal':f=[1/u,S.log(u+p['b']),S.Integer(p['c'])];h=a/t
 elif name=='cos_cube_log_exp':f=[S.cos(u),u**3,S.log(u)];h=S.exp(a*t)
 else:
  # Both missing levels have exactly three active outer components, each a
  # prerequisite elementary derivative, and exactly one scalar composition.
  f=[p['c']*S.sin(u),p['d']*S.exp(u),p['e']*u**2]
  h=a*t**(2 if name=='mixed_quadratic_inner' else 3)+p['b']*t+p['h']
 D=[S.diff(x,u) for x in f];hp=S.diff(h,t)
 C=[S.simplify(x.subs(u,h)*hp) for x in D]
 if name=='mixed_cubic_inner':C[2]=S.expand(C[2])
 return f,h,D,hp,C

# Complete observed banks; entries are operations on components, never isolated
# scalar normalizations or fitted ratios. Residual unusual operations are named
# literal symbolic patterns and restricted to replay profiles (see extraction).
def observed_bank(name,p,D,h,hp,C):
 a=S.Integer(p['a']); at=lambda v:[S.simplify(x.subs(u,v)) for x in D]
 if name=='linear_quadratic_affine':
  b,c=p['b'],p['c'];return [C,at(h),[c*a,2*a*a*t,0],at(t),[c*a,2*h,0]]
 if name=='cos_quadratic_power':
  n=p['n'];return [[-S.sin(hp),-2*hp,0],C,[-(n-1)*a*t**(n-1)*S.sin(h),-(n-1)*a*a*t**(2*n-1),0],D,[-S.sin(h),-2*n*h,0]]
 if name=='sin_log_tan_power':
  n=p['n'];return [[S.cos(h),1/h,hp*S.sec(h)**2/n],[S.cos(h),1/t,hp],[hp*S.sin(h),1/t,hp*S.cos(h)**2],[hp*S.sec(h),1/t,hp*S.sin(h)],C]
 if name=='linear_quadratic_exp':
  c=p['c'];return [at(h),C,[c*hp,2*h,0],[c*t,2*h,0],[c,3*h,0]]
 if name=='linear_vector_power':
  c,d,e=p['c'],p['d'],p['e'];return [C,[2*hp]*3,[2*x for x in C],[c*h,d*h,e*h],D]
 if name=='log_quadratic_log':return [at(h),D,[1/h,0,C[2]],C,[u,p['c'],2*u]]
 if name=='log_reciprocal_exp':return [[a,0,-a*h],at(h),C,[a,0,a*h],[1/h,0,1/h**2]]
 if name=='two_exp_power':
  b,c,n=p['b'],p['c'],p['n'];return [[t*S.exp(a*t+b),c*t*S.exp(c*a*t),0],[t*S.exp(t+b),c*t*S.exp(c*t),0],C,[hp*S.exp(t+b),(c+1)*a*t*S.exp(c*t),0],[a*n*S.exp(h+b),-a*n*c*S.exp(c*h),0]]
 if name=='sin_cos_exp_affine':return [[a*S.sin(h),-a*S.cos(h),a*S.exp(h)],[-S.sin(h),S.cos(h),h*S.exp(t) ],C,[-2*a*S.sin(h),2*a*S.cos(h),h*S.exp(t)],at(h)]
 if name=='log_power_root_exp':return [[-a,4*a*h**2,2*a*h**S.Rational(3,2)],[a,a*h**2,2*a*S.sqrt(h)],[-a,2*a*h,a*S.sqrt(h)/4],C,[a,2*a/h**2,a/(2*h)]]
 if name=='reciprocal_log_reciprocal':
  b=p['b'];return [[-1/a,-a*t/(2*b+t*t),0],[-a/t**2,-t*t/(b+t*t),0],C,[a/t,C[1],0],[1/a,-a*t/(b+t*t),0]]
 if name=='cos_cube_log_exp':return [[-hp*S.cos(h),3*h,1],[-S.sin(h*h),3*h*h,1],[hp*S.cos(h),C[1],h*h],[S.sin(h*h),h**3,1/(h*h)],C]
 raise ValueError(name)

RECIPES=['correct','omit inner derivative','omit substitution','apply inner derivative twice','apply inner derivative only to first component']
def authored_bank(D,h,hp,C,f):
 if all(not x.has(u) for x in D):
  # Constant outer derivative needs its own complete bank: omitting substitution
  # is indistinguishable from omitting the inner derivative.
  return [C,D,[x.subs(u,h) for x in f],[2*x for x in C],[D[0]*hp]*3]
 return [C,[x.subs(u,h) for x in D],D,[x.subs(u,h)*hp**2 for x in D],[C[0],D[1].subs(u,h),D[2].subs(u,h)]]

def tex(x):
 x=S.sympify(x)
 x=x.xreplace({S.diff(U,t):S.Symbol('innerslope'),U:S.Symbol('innerinput')})
 return S.latex(x,fold_short_frac=False,inv_trig_style='full').replace('innerinput','u(t)').replace('innerslope',r'u^{′}(t)')
def vector(v,style,force_zero=False):
 if style=='matrix':return r'[\begin{aligned}'+r' \\ '.join(tex(x) for x in v)+r'\end{aligned}]'
 if style=='angle':return '⟨'+r',\,'.join(tex(x) for x in v)+'⟩'
 parts=[]
 for x,label in zip(v,'ijk'):
  x=S.sympify(x)
  if x==0 and not force_zero:continue
  z=tex(x); sign=''
  if z.startswith('-'):sign='-';z=z[1:].lstrip()
  elif parts:sign='+'
  if x in (1,-1):z=''
  if x.is_Add:z=r'\left('+z+r'\right)'
  parts.append(sign+z+r'\,'+label)
 return ''.join(parts) or '0'
def block(s):return '$$\n'+s+'\n$$'
def aligned(rows):return r'\begin{aligned}'+r' \\ '.join(l+' & ='+r for l,r in rows)+r'\end{aligned}'
def times(v,hp,style):
 z=vector(v,style)
 return (r'\left('+z+r'\right)' if style=='basis' else z)+r'\cdot '+r'\left('+tex(hp)+r'\right)'
def derivative_vector(f,style):
 parts=[r'\frac{\text{d}}{\text{d}u}\left('+tex(x)+r'\right)' for x in f]
 if style=='matrix':return r'[\begin{aligned}'+r' \\ '.join(parts)+r'\end{aligned}]'
 if style=='angle':return '⟨'+r',\,'.join(parts)+'⟩'
 return '+'.join(x+r'\,'+label for x,label in zip(parts,'ijk'))

def build_text(name,p,f,h,D,hp,C,style):
 source=SPECS[name][0] if name in SPECS else None
 q=QUESTIONS[source] if source else None
 fn='g' if source in ('q-128563','q-32860','q-32869','q-128570') else 'f'
 comp='('+fn+'∘u)^{′}(t)'; rule=fn+'′(u(t))u′(t)'
 # Replace complete inline function-definition slots only, never variable names
 # across arbitrary prose or scalar substrings inside vector coordinates.
 if q:
  prompt=q[':question/problem'];matches=list(re.finditer(r'\$[^$]*\$',prompt))
  repl=[fn+'(u)='+vector(f,style),'u(t)='+tex(h),comp+'=']
  # Each source has exactly three complete inline formulas.
  for m,value in reversed(list(zip(matches,repl,strict=True))):prompt=prompt[:m.start()]+'$'+value+'$'+prompt[m.end():]
 else:prompt='If $'+fn+'(u)='+vector(f,style)+'$ and $u(t)='+tex(h)+'$, then $'+comp+'=$'
 if name=='mixed_cubic_inner':prompt+=' Write the polynomial component in expanded form.'
 first=comp+'='+rule
 outer=fn+'^{′}(u)'; inner=r'u^{′}(t)'
 deriv=r'\frac{\text{d}}{\text{d}t}\left('+tex(h)+r'\right)'
 rows=[]
 if style=='matrix':rows.append((outer,derivative_vector(f,style)+'='+vector(D,style)))
 else:
  rows=[(outer,derivative_vector(f,style)),('',vector(D,style,force_zero=source in ('q-32866','q-33260')))]
  if source in ('q-32866','q-33260'):rows.append(('',vector(D,style)))
 if source=='q-32502':rows.extend([(inner,deriv),('',tex(hp))])
 else:rows.append((inner,deriv+'='+tex(hp)))
 derivblock=aligned(rows)
 su=[x.subs(u,U) for x in D]; sub=[x.subs(u,h) for x in D]
 solrows=[(comp,rule)]
 if source=='q-32502':solrows.append(('',times(D,hp,style)))
 elif source=='q-33260':solrows.append((comp,times(sub,hp,style)))
 else:
  solrows.append(('',times(su,S.diff(U,t),style)))
  solrows.append(('',times(sub,hp,style)))
  if source=='q-32869':solrows.append(('',vector([S.Mul(x,hp,evaluate=False) for x in sub],style)))
  if source in ('q-128561','q-70695'):solrows.append(('',times([S.simplify(x) for x in sub],hp,style)))
 solrows.append(('',vector(C,style)))
 solutionblock=aligned(solrows)
 if q:
  # Preserve complete shared prose and exact display-block count. Math stages
  # are rebuilt from differentiated components; notation is normalized.
  prose=q[':question/worked-solution'];blocks=list(re.finditer(r'\$\$.*?\$\$',prose,re.S))
  for m,value in reversed(list(zip(blocks,[first,derivblock,solutionblock],strict=True))):prose=prose[:m.start()]+block(value)+prose[m.end():]
  solution=prose
 else:solution='Using the chain rule, we can write\n\n'+block(first)+"\n\nLet's now find the derivatives of each function.\n\n"+block(derivblock)+'\n\nTherefore, we obtain:\n\n'+block(solutionblock)
 return prompt,solution,{'outer':D,'inner':hp,'substituted':sub,'distributed':C,'composition':C,'solution_rows':[1,len(rows),len(solrows)]}

def validate_parameters(name,p):
 base=SPECS[name][2] if name in SPECS else dict(a=1,b=1,h=0,c=1,d=1,e=1)
 if set(p)!=set(base) or any(type(v) is not int for v in p.values()):raise ValueError('Supply exactly the documented integer parameter keys')
 for k,v in p.items():
  if k=='n':
   if v!=base[k]:raise ValueError('The observed easy power is fixed per template')
  elif name in SPECS:
   if k=='a':
    if v==0 or abs(v)>4:raise ValueError('Easy |a| is 1..4')
    if name not in ('linear_quadratic_affine','sin_cos_exp_affine','linear_quadratic_exp','log_reciprocal_exp','log_power_root_exp','cos_cube_log_exp') and v<0:raise ValueError('Positive inner coefficient required by this family domain')
   elif k=='b':
    if abs(v)>4 or name in ('reciprocal_log_reciprocal',) and v<=0:raise ValueError('b outside supported shift bounds')
   elif k in ('c','d','e') and not 1<=v<=12:raise ValueError('Outer constants/coefficients are 1..12')
  else:
   bound=2 if name=='mixed_quadratic_inner' else 3
   if k=='h':
    if abs(v)>2 or name=='mixed_cubic_inner' and v==0:raise ValueError('Inner constant magnitude <=2 and hard constant nonzero')
   elif not 1<=abs(v)<=bound:raise ValueError('Nonzero coefficient magnitude exceeds the level bound')
 return dict(p)

def sample(name,rng):
 if name in SPECS:
  p=dict(SPECS[name][2]);p['a']=rng.choice([1,2,3,4])
  if name in ('linear_quadratic_affine','sin_cos_exp_affine','linear_quadratic_exp','log_reciprocal_exp','log_power_root_exp','cos_cube_log_exp'):p['a']*=rng.choice([-1,1])
  for k in ('b','c','d','e'):
   if k in p:p[k]=rng.randint(1,4) if k!='b' or name=='reciprocal_log_reciprocal' else rng.choice([-4,-3,-2,-1,1,2,3,4])
  return p
 bound=2 if name=='mixed_quadratic_inner' else 3
 return {k:((rng.choice([-2,-1,1,2]) if name=='mixed_cubic_inner' else rng.randint(-2,2)) if k=='h' else rng.choice([i for i in range(-bound,bound+1) if i])) for k in ('a','b','h','c','d','e')}

def equivalent(v,w):return all(S.simplify(S.trigsimp(S.sympify(x)-S.sympify(y)))==0 for x,y in zip(v,w,strict=True))
def canonical(v):return [S.srepr(S.simplify(x)) for x in v]
def natural_domain(name,p):
 if name=='sin_log_tan_power':return 't != 0; cos('+str(p['a'])+'*t^2) != 0'
 if name=='log_quadratic_log':return 't > 1'
 if name=='reciprocal_log_reciprocal':return 't != 0 and '+str(p['a'])+'/t + '+str(p['b'])+' > 0'
 if name=='cos_quadratic_power':return 'all real t'
 return 'all real t'

def assemble(name,p,seed,profile):
 f,h,D,hp,C=math_data(name,p)
 style=SPECS[name][1] if name in SPECS else 'matrix'
 values=observed_bank(name,p,D,h,hp,C) if profile=='observed' else authored_bank(D,h,hp,C,f)
 values=[[S.sympify(x) for x in v] for v in values]
 if name=='mixed_cubic_inner':values=[[v[0],v[1],S.expand(v[2])] for v in values]
 if any(equivalent(v,w) for i,v in enumerate(values) for w in values[:i]):raise ValueError('Complete bank rejected: equivalent vector choices')
 correct=[i for i,v in enumerate(values) if equivalent(v,C)]
 if len(correct)!=1:raise ValueError('Complete bank rejected: correct vector not unique')
 prompt,solution,stages=build_text(name,p,f,h,D,hp,C,style)
 paramkey=hashlib.sha256(json.dumps({'derivative':canonical(C),'domain':natural_domain(name,p)},sort_keys=True).encode()).hexdigest()
 recipe_labels=([item['recipe'] for item in next(x for x in json.loads((ROOT/'bank-extraction.json').read_text())['sources'] if x['template']==name)['bank']] if profile=='observed' else (['correct','omit inner derivative','return undifferentiated composition','extra constant factor2','erase unequal component coefficients'] if all(not x.has(u) for x in D) else RECIPES))
 content=hashlib.sha256(json.dumps([VERSION,TEMPLATES[name],prompt,solution,sorted(vector(v,style) for v in values)],ensure_ascii=False).encode()).hexdigest()
 qid=uuid.uuid5(uuid.UUID(KP_UUID),content);fid=uuid.uuid5(qid,'selection')
 answers=[{':answer/id':str(uuid.uuid5(fid,vector(v,style))),':answer/type':':answer.type/math',':answer/value':vector(v,style)} for v in values]
 cid=answers[correct[0]][':answer/id'];random.Random(seed).shuffle(answers)
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':str(qid),':question/difficulty':':question.difficulty/'+TEMPLATES[name],':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':[{':answer-field/id':str(fid),':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',cid]}]},'generation':{'version':VERSION,'template':name,'seed':seed,'parameters':p,'bank_profile':profile,'bank_origin':'observed' if profile=='observed' else 'authored','authored_level':TEMPLATES[name]!='easy','parameter_fingerprint':paramkey,'content_fingerprint':content,'source_analysis':{'database':'math','basis':1356,'lineage':SOURCE['lineage'],'question_ids':[SPECS[name][0]] if name in SPECS else [],'method_reference':'e-2479'},'repairs':[REPAIRS[SPECS[name][0]]] if name in SPECS and SPECS[name][0] in REPAIRS else [],'notation_normalization':True,'domain':natural_domain(name,p),'plot_rating':'none','plot_assets':{},'outer_function':[S.sstr(x) for x in f],'inner_function':S.sstr(h),'stages':{k:[S.sstr(x) for x in v] if isinstance(v,list) and k!='solution_rows' else S.sstr(v) if k!='solution_rows' else v for k,v in stages.items()},'choice_math':{a[':answer/id']:[S.sstr(x) for x in values[next(i for i,v in enumerate(values) if vector(v,style)==a[':answer/value'])]] for a in answers},'distractor_recipes':[{ 'operation':label, 'complete_vector':[S.sstr(x) for x in v], 'origin':profile} for label,v in zip(recipe_labels,values,strict=True)],'sympy_version':S.__version__}}

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('Unknown difficulty')
 if field_type not in (None,'radio'):raise ValueError('This KP preserves radio fields only')
 if profile not in (None,'observed','authored'):raise ValueError('Unknown complete bank profile')
 eligible=[k for k,v in TEMPLATES.items() if v==level]
 if template is not None and template not in eligible:raise ValueError('Template is not applicable at this level')
 name=template or random.Random(seed).choice(eligible)
 profile=profile or 'authored'
 if profile=='observed' and name not in SPECS:raise ValueError('No observed source bank at authored levels')
 if parameters is not None:return assemble(name,validate_parameters(name,dict(parameters)),seed,profile)
 rng=random.Random(seed)
 for _ in range(100):
  p=validate_parameters(name,sample(name,rng))
  try:return assemble(name,p,seed,profile)
  except ValueError as e:
   if not str(e).startswith('Complete bank rejected'):raise
 raise ValueError('Bounded sampler did not produce a complete eligible bank')

# EASY: observed family workload and layouts; authored method-error defaults.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE: three active elementary components, quadratic + linear + constant
# inner, derivative has two terms; distribute it without expanding trig/exp.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# HARD: same three active components, cubic + linear + constant inner, then
# expand the polynomial component (five nonzero powers at generic parameters).
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)

def markdown(r):
 q=r['question'];g=r['generation'];f=q[':question/answer-fields'][0]
 return '## '+g['template']+' — '+q[':question/difficulty'].split('/')[-1]+' ('+g['bank_profile']+')\n\n'+q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$'+(' **correct**' if a[':answer/id']==f[':answer-field/correct'][1] else '') for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');p.add_argument('--seed',type=int,default=0);p.add_argument('--count',type=int,default=1);p.add_argument('--format',choices=['markdown','json'],default='markdown');p.add_argument('--template',choices=list(TEMPLATES));p.add_argument('--profile',choices=['observed','authored']);a=p.parse_args()
 if a.count<1 or a.difficulty=='all' and a.template:p.error('Positive count and specific level with template required')
 try:rs=[generate(level,a.seed+i,a.template,profile=a.profile) for level in (['easy','moderate','hard'] if a.difficulty=='all' else [a.difficulty]) for i in range(a.count)]
 except ValueError as e:p.error(str(e))
 print(json.dumps(rs,indent=2,ensure_ascii=False) if a.format=='json' else '\n\n---\n\n'.join(map(markdown,rs)))
if __name__=='__main__':main()
