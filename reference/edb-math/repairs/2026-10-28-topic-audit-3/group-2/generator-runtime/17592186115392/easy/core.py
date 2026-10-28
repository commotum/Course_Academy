import json
from pathlib import Path
import re
import sympy as S
t,u=S.symbols('t u',real=True)
U=S.Function('u')(t)
QUESTIONS={q[':question/math-academy-id']:q for q in json.loads((Path(__file__).parent/'source-data.json').read_text())}
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
 D=[S.sec(u)**2 if x==S.tan(u) else S.diff(x,u) for x in f];hp=S.diff(h,t)
 C=[x.subs(u,h)*hp if x.has(S.sin,S.cos,S.tan,S.sec) else S.simplify(x.subs(u,h)*hp) for x in D]
 if name=='mixed_cubic_inner':C[2]=S.expand(C[2])
 return f,h,D,hp,C

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

def tex(x):
 x=S.sympify(x)
 x=x.xreplace({S.diff(U,t):S.Symbol('innerslope'),U:S.Symbol('innerinput')})
 return S.latex(x,fold_short_frac=False,inv_trig_style='full').replace(r'\log',r'\ln').replace('innerinput','u(t)').replace('innerslope',r'u^{′}(t)')

def vector(v,style,force_zero=False):
 if style=='matrix':return r'\begin{bmatrix}'+r' \\ '.join(tex(x) for x in v)+r'\end{bmatrix}'
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
 if style=='matrix':return r'\begin{bmatrix}'+r' \\ '.join(parts)+r'\end{bmatrix}'
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
