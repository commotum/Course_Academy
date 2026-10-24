#!/usr/bin/env python3
"""Horizontal/vertical regular tangents; local draft, math basis1356.

Every observed family uses a complete component-slot recipe. Public raw profiles
preserve absent attributes and duplicate historical fields. They are evidence
only. Source profile banks with opaque scalar intent are never default banks.
No database writes, engine changes, or plots. See the adjacent evidence folder.
"""
from __future__ import annotations

# Standalone source eligibility: immutable policy ledger, seeded CLI guard.
import sys as _ca_sys, os as _ca_os
from pathlib import Path as _ca_Path
_ca_sys.path.insert(0,str(_ca_Path(__file__).resolve().parent))
if __name__ == "__main__" and not _ca_os.environ.get("_CA_SOURCE_POLICY_CHILD"):
    from ca_source_runtime import cli as _ca_source_cli
    _ca_source_cli(__file__,_ca_Path(__file__).with_name('17592186083278-source-policy.json'))
    raise SystemExit(0)

import argparse, hashlib, json, random, re, sys, uuid
from pathlib import Path
import sympy as sp

HERE=Path(__file__).with_suffix('')
SOURCE=json.loads((HERE/'source.json').read_text())
KP=SOURCE['record']; T=sp.Symbol('t',real=True)
VERSION='regular-tangents-1'
DEFS={
 'line_quadratic':('easy','q-20853',{'a':2,'b':4,'h':1,'s':0}),
 'line_cubic':('easy','q-21206',{'a':1,'b':1,'h':-1,'k':-2,'s':0}),
 'circle_horizontal':('easy','q-21072',{'a':3,'b':3,'h':5,'k':4,'m':0}),
 'polynomial_two':('easy','q-350359',{'r':-4,'u':-2,'c':'1/2','d':'1/2'}),
 'spiral_cos':('easy','q-350368',{'a':1,'b':1,'phase':0}),
 'spiral_sin':('easy','q-357255',{'a':1,'b':1,'phase':0}),
 'circle_vertical':('moderate','q-21081',{'a':4,'b':4,'h':7,'k':10,'m':0}),
 'power_line':('moderate','q-122726',{'a':4,'b':9,'n':5,'s':0}),
 'paired_cubics':('hard',None,{'r':-3,'s':1,'u':-1,'v':2,'a':1,'b':1}),
}
QUESTIONS={q[':question/math-academy-id']:q for q in KP[':knowledge-point/questions']}
def tex(v):
 return sp.latex(sp.sympify(v)).replace(r'\left', '').replace(r'\right','').replace(' ','').replace(r'\pi',r'\pi ').replace('e^{','{e}^{')
def poly(v):
 pieces=[]
 for (power,),coef in sp.Poly(sp.expand(v),T).terms():
  base=('{t}^{'+str(power)+'}' if power>1 else 't') if power else ''
  term=component(abs(coef),base) if power else nice(abs(coef))
  pieces.append(('-' if coef<0 else '+' if pieces else '')+term)
 return ''.join(pieces) or '0'
def nice(v): return tex(v).replace(' ','')
def component(a,base):
 return ('' if a==1 else '-' if a==-1 else nice(a))+base
def plus(v): return ('+' if v>=0 else '-')+nice(abs(v)) if v else ''
def shifted(s): return 't' if s==0 else '(t'+plus(-s)+')'
def pw(s,n): return ('{t}' if s==0 else shifted(s))+r'^{'+str(n)+'}'
def trig(name,phase=0,parens=False):
 arg='t'+plus(phase)
 return r'\operatorname{'+name+'}⁡'+('('+arg+')' if parens else arg)
def uid(value): return str(uuid.uuid5(uuid.NAMESPACE_URL,json.dumps(value,sort_keys=True,ensure_ascii=False)))
def digest(value): return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def e(v): return sp.sympify(v,locals={'t':T,'pi':sp.pi})
def task_key(dx,dy,domain,orientation):
 # The assessment requests parameter sets only: translations and nonzero common
 # derivative scales are incidental. Normalize each component separately.
 def normalize(v):
  expanded=sp.expand(v)
  coeff,_=expanded.as_coeff_Mul()
  if v.is_polynomial(T):return sp.srepr(sp.Poly(v,T).monic().as_expr())
  terms=sp.Add.make_args(expanded);coeff=terms[0].as_coeff_Mul()[0]
  return sp.srepr(sp.simplify(v/coeff))
 return digest([normalize(dx),normalize(dy),str(domain),orientation])

def guards(template,p):
 expected=set(DEFS[template][2])
 if set(p)!=expected: raise ValueError('Explicit parameter keys must match '+str(expected))
 p={k:e(v) for k,v in p.items()}
 if any(not v.is_Rational for v in p.values()): raise ValueError('Parameters are exact rational numbers')
 if template in ('line_quadratic','line_cubic','power_line','circle_horizontal','circle_vertical','spiral_cos','spiral_sin'):
  for k in ('a','b'):
   if not p[k].is_Integer or not 1<=abs(p[k])<=10: raise ValueError('Nonzero integer scales, absolute value <=10')
 if template=='line_quadratic' and (not p['h'].is_Integer or not 1<=abs(p['h'])<=5): raise ValueError('Nonzero small shift')
 if template=='line_quadratic' and (not p['s'].is_Integer or abs(p['s'])>5): raise ValueError('Small assessed root shift')
 if template=='line_cubic' and any(not p[k].is_Integer or abs(p[k])>5 for k in ('h','k','s')): raise ValueError('Small integer shifts')
 if template.startswith('circle'):
  if any(not p[k].is_Integer or abs(p[k])>10 for k in ('h','k')) or not p['m'].is_Integer or abs(p['m'])>3: raise ValueError('Circle/domain bounds')
 if template=='power_line':
  if p['n'] not in (3,5,7) or not p['s'].is_Integer or abs(p['s'])>5: raise ValueError('Moderate odd power and small root shift')
 if template=='polynomial_two':
  if not p['r'].is_Integer or not 1<=abs(p['r'])<=5 or not p['u'].is_Integer or not 1<=abs(p['u'])<=8 or p['u']%3==0: raise ValueError('Integer/rational distinct roots')
  if abs(p['c'])>3 or p['c'].q>2 or abs(p['d'])>3 or p['d'].q>2: raise ValueError('Small half-integer x coefficients')
  if p['r']==p['u']/3 or any(2*z+p['c']==0 for z in (p['r'],p['u']/3)): raise ValueError('Only regular roots supported')
 if template.startswith('spiral') and p['phase'] not in (0,1,2,3): raise ValueError('Phase is a quarter-turn index 0..3')
 if template=='paired_cubics':
  if any(not p[k].is_Integer or not 1<=abs(p[k])<=4 for k in ('r','s','u','v')) or p['a'] not in (-2,-1,1,2) or p['b'] not in (-2,-1,1,2): raise ValueError('Hard small integer factors')
  if len({p[k] for k in ('r','s','u','v')})!=4: raise ValueError('Hard factors must have four distinct roots; stationary values excluded')
 return p

def sample(template,rng):
 while True:
  p=dict(DEFS[template][2])
  if template in ('line_quadratic','line_cubic'):
   p.update(a=rng.choice([-3,-2,1,2,3,4]),b=rng.choice([-3,-1,1,2,4]),h=rng.choice([-3,-2,-1,1,2,3]))
   p['s']=rng.randint(-5,5)
   if template=='line_cubic':p.update(k=rng.randint(-3,3))
  elif template.startswith('circle'):
   p.update(a=rng.choice([-5,-3,2,3,4,5]),b=rng.choice([-5,-3,2,3,4,5]),h=rng.randint(-5,8),k=rng.randint(-5,10),m=rng.randint(-3,3))
  elif template=='power_line':p.update(a=rng.randint(2,6),b=rng.randint(2,10),n=rng.choice([3,5,7]),s=rng.randint(-5,5))
  elif template=='polynomial_two':p.update(r=rng.choice([-5,-4,-3,-2,-1,1,2,3,4,5]),u=rng.choice([-8,-7,-5,-4,-2,-1,1,2,4,5,7,8]),c=str(sp.Rational(rng.randint(-6,6),2)),d=str(sp.Rational(rng.randint(-6,6),2)))
  elif template.startswith('spiral'):p.update(a=rng.choice([-3,-2,-1,1,2,3]),b=rng.choice([-3,-2,-1,1,2,3]),phase=rng.randint(0,3))
  else:
   values=rng.sample([-4,-3,-2,-1,1,2,3,4],4);p.update(zip(('r','s','u','v'),values));p.update(a=rng.choice([-2,-1,1,2]),b=rng.choice([-2,-1,1,2]))
  try:return guards(template,p)
  except ValueError:pass

def mathematics(template,p):
 orientation='vertical' if template in ('power_line','circle_vertical') else 'horizontal'
 domain=sp.S.Reals
 if template=='line_quadratic':x=p['a']*(T+p['h']);y=p['b']*(T-p['s'])**2;roots=[p['s']]
 elif template=='line_cubic':x=p['a']*(T+p['h']);y=p['b']*(T-p['s'])**3+p['k'];roots=[p['s']]
 elif template=='power_line':x=p['a']*(T-p['s'])**p['n'];y=p['b']*T;roots=[p['s']]
 elif template.startswith('circle'):
  x=p['a']*sp.sin(T)+p['h'];y=p['b']*sp.cos(T)+p['k'];lo=p['m']*sp.pi
  if orientation=='horizontal':roots=[lo,lo+sp.pi];domain=sp.Interval(lo,lo+sp.pi)
  else:roots=[lo+sp.pi/2,lo+3*sp.pi/2];domain=sp.Interval.Ropen(lo,lo+2*sp.pi)
 elif template=='polynomial_two':
  x=T**2+p['c']*T+p['d'];y=T**3-(3*p['r']+p['u'])*T**2/2+p['r']*p['u']*T;roots=sorted([p['r'],p['u']/3],key=float)
 elif template.startswith('spiral'):
  phase=p['phase']*sp.pi/2;arg=T+phase
  x=p['a']*sp.exp(T)*(sp.cos(arg) if template=='spiral_cos' else sp.sin(arg));y=p['b']*sp.exp(T)*(sp.sin(arg) if template=='spiral_cos' else sp.cos(arg))
  base=3*sp.pi/4 if template=='spiral_cos' else sp.pi/4
  roots=sorted([sp.simplify(base-phase+j*sp.pi) for j in range(-2,5) if 0<=base-phase+j*sp.pi<=2*sp.pi],key=float);domain=sp.Interval(0,2*sp.pi)
 else:
  dx=p['a']*(T-p['u'])*(T-p['v']);dy=3*p['b']*(T-p['r'])*(T-p['s'])
  x=sp.integrate(dx,T);y=sp.integrate(dy,T);roots=sorted([p['r'],p['s']],key=float)
 return x,y,sp.diff(x,T),sp.diff(y,T),roots,orientation,domain

def blocks(s):return re.findall(r'\$\$(.*?)\$\$',s,re.S)
def fill_blocks(s,replacements):
 i=-1
 def f(m):
  nonlocal i;i+=1
  return '$$'+replacements.get(i,m.group(1))+'$$'
 return re.sub(r'\$\$(.*?)\$\$',f,s,flags=re.S)
def chain(exprs):return r'\begin{aligned}'+r' \\ '.join(exprs)+r'\end{aligned}'
def rootword(roots,punctuation=False):
 vals=['$t='+tex(z)+('.' if punctuation and i==len(roots)-1 else '')+'$' for i,z in enumerate(roots)]
 return ' and '.join(vals)
def source_render(template,p,data,raw):
 """Fill complete math components and complete concluding sentences, never short global numeric replacement."""
 x,y,dx,dy,roots,o,domain=data; sid=DEFS[template][1];source=QUESTIONS[sid]
 prompt=source[':question/problem'];solution=source.get(':question/worked-solution');a=p.get('a');b=p.get('b')
 if template=='line_quadratic':
  formula='x='+component(a,'(t'+plus(p['h'])+')')+r',\,y='+component(b,pw(p['s'],2))+r',\,-\infty <t<\infty .'
  deriv=r'{x}^{′}(t)='+nice(a)+r',\,{y}^{′}(t)='+component(2*b,shifted(p['s']))+'.'
  solve=component(2*b,shifted(p['s']))+r'=0\,⟹\,t='+tex(p['s'])+'.'
  note='Note that ${x}^{′}('+tex(p['s'])+')='+nice(a)+r'\ne 0.$ Therefore, we conclude that when $t='+tex(p['s'])+',$ the tangent to the curve is horizontal.'
 elif template=='power_line':
  formula='x='+component(a,pw(p['s'],int(p['n'])))+r',\,y='+component(b,'t')+r',\,-\infty <t<\infty .'
  deriv=r'{x}^{′}(t)='+component(a*p['n'],pw(p['s'],int(p['n']-1)))+r',\,{y}^{′}(t)='+nice(b)+'.'
  solve=component(a*p['n'],pw(p['s'],int(p['n']-1)))+r'=0\,⟹\,t='+tex(p['s'])+'.'
  note='Note that ${y}^{′}('+tex(p['s'])+')='+nice(b)+r'\ne 0.$ Therefore, we conclude that when $t='+tex(p['s'])+',$ the tangent to the curve is vertical.'
 elif template=='line_cubic':
  # This source has no displayed solution or difficulty; raw preserves that absence.
  fmt=lambda v:tex(v).replace('+',' + ').replace('-',' - ')
  formula='x = '+fmt(x)+', y = '+fmt(y)+r', - ∞ < t < ∞'
  prompt=re.sub(r'\$x = .*?\$',lambda _: '$'+formula+'$',prompt)
  if not raw:solution=normal_solution(data)
  return prompt,solution
 elif template.startswith('circle'):
  lo=p['m']*sp.pi;upper=lo+(sp.pi if o=='horizontal' else 2*sp.pi)
  interval=('0' if lo==0 else tex(lo))+r'\le t'+(r'\le ' if o=='horizontal' else '<')+tex(upper)
  formula='x='+component(a,trig('sin'))+plus(p['h'])+r',\,y='+component(b,trig('cos'))+plus(p['k'])+r',\,'+interval+'.'
  deriv=r'{x}^{′}(t)='+component(a,trig('cos'))+r',\,{y}^{′}(t)='+component(-b,trig('sin'))+'.'
  target=component(-b,trig('sin')) if o=='horizontal' else component(a,trig('cos'))
  solve=target+r'=0\,⟹\,t='+','.join(tex(z) for z in roots)+'.'
  other=dx if o=='horizontal' else dy;letter='x' if o=='horizontal' else 'y'
  checks=chain([r'{'+letter+r'}^{′}('+tex(z)+') & ='+tex(sp.simplify(other.subs(T,z)))+r'\ne 0,' for z in roots])
 elif template=='polynomial_two':
  formula='x='+poly(x)+r',\,y='+poly(y)+r',\,-\infty <t<\infty .'
  deriv=r'{x}^{′}(t)='+poly(dx)+r',\,{y}^{′}(t)='+poly(dy)
  f1='(3t'+plus(-p['u'])+')';f2='(t'+plus(-p['r'])+')'
  solve=chain([poly(dy)+' & =0',f1+f2+' & =0','t & ='+','.join(tex(z) for z in roots)+'.'])
  checks=chain([r'{x}^{′}('+tex(z)+') & =2('+tex(z)+')'+plus(p['c'])+'='+tex(sp.simplify(dx.subs(T,z)))+r'\ne 0,' for z in roots])
 else:
  phase=p['phase']*sp.pi/2;first='cos' if template=='spiral_cos' else 'sin';second='sin' if first=='cos' else 'cos'
  ex=r'{e}^{t}';sx=trig(first,phase,True);sy=trig(second,phase,True)
  formula='x='+component(a,ex+sx)+r',\,y='+component(b,ex+sy)+r',\,0\le t\le 2\pi .'
  sin=trig('sin',phase,True);cos=trig('cos',phase,True)
  dxi=(cos+'-'+sin) if first=='cos' else (sin+'+'+cos)
  dyi=(sin+'+'+cos) if first=='cos' else (cos+'-'+sin)
  deriv=r'{x}^{′}(t)='+component(a,ex+'('+dxi+')')+r',\,{y}^{′}(t)='+component(b,ex+'('+dyi+')')
  # Division by cos is legal here: cos=0 cannot solve sin +/- cos=0.
  sign='-1' if first=='cos' else '1';arg='t'+plus(phase)
  solve=chain([component(b,ex+'('+dyi+')')+' & =0',dyi+' & =0',sin+' & ='+('-' if first=='cos' else '')+cos,r'\frac{'+sin+'}{'+cos+'} & ='+sign,trig('tan',phase,True)+('=-1' if first=='cos' else ' & =1'),'t & ='+','.join(tex(z) for z in roots)+'.'])
  rows=[]
  for z in roots:
   argz=tex(z+phase);sz=r'\operatorname{sin}⁡('+argz+')';cz=r'\operatorname{cos}⁡('+argz+')';inside=cz+'-'+sz if first=='cos' else sz+'+'+cz
   rows.append(r'{x}^{′}('+tex(z)+') & ='+component(a,r'{e}^{'+tex(z)+'}['+inside+']')+'='+tex(sp.simplify(dx.subs(T,z)))+r'\ne 0,')
  checks=chain(rows)
 prompt=fill_blocks(prompt,{0:'\n'+formula+'\n'})
 if solution:
  solution=fill_blocks(solution,{1:'\n'+deriv+'\n',2:'\n'+solve+'\n',**({3:'\n'+checks+'\n'} if len(roots)==2 else {})})
  if len(roots)==1:
   solution=solution[:solution.index('Note that')]+note
  else:
   # Complete conclusion includes all parameter values; no stale original values.
   at='when' if template.startswith('circle') else 'at'
   solution=solution[:solution.index('which confirms')]+f'which confirms that the tangent to the curve is indeed {o} {at} '+rootword(roots,True)
 if not raw:prompt=prompt.replace('Do not round the answers.','Give exact answers.')
 return prompt,solution

def normal_solution(data):
 x,y,dx,dy,roots,o,domain=data;target=dy if o=='horizontal' else dx;other=dx if o=='horizontal' else dy;letter='y' if o=='horizontal' else 'x';otherletter='x' if o=='horizontal' else 'y'
 return ('The slope $m$ of a tangent line to a curve defined parametrically is given by\n\n$$\nm=\\frac{y\'(t)}{x\'(t)}.\n$$\n\n'
  +f'The tangent line is {o} if ${letter}\'(t)=0$ while ${otherletter}\'(t)\\ne 0.$\n\nSo, we first find the derivatives of $x$ and $y:$\n\n$$\n'
  +f"x'(t)={poly(dx)},\\qquad y'(t)={poly(dy)}.\n$$\n\nSolving ${letter}'(t)=0$ gives\n\n$$\n"
  +chain([poly(target)+' & =0',tex(sp.factor(target))+' & =0','t & ='+','.join(tex(z) for z in roots)+'.'])+'\n$$\n\nNow, we note that\n\n$$\n'
  +chain([otherletter+"'("+tex(z)+') & ='+poly(other.subs(T,z))+r'\ne 0,' for z in roots])+'\n$$\n\nwhich confirms that the tangent to the curve is indeed '+o+' at '+rootword(roots)+'.')

def bank_objects(template,p,data,profile):
 """Complete banks selected before sampling. Opaque historical scalar operations are evidence only."""
 roots=data[4];o=data[5]
 if template.startswith('circle'):
  lo=p['m']*sp.pi
  if o=='horizontal':return [[lo,lo+sp.pi/2],[lo+sp.pi/4,lo+sp.pi/2],roots,[lo+sp.pi/4,lo+sp.pi],[lo+sp.pi/2,lo+sp.pi]]
  return [[lo+3*sp.pi/2],roots,[lo+sp.pi/4],[lo+sp.pi/4,lo+3*sp.pi/4],[lo+sp.pi/2]]
 if template=='line_quadratic':
  return [data[4],[-p['a']],[p['h']],[p['a']+p['h']],[-p['h']]] if profile in ('raw','observed') else [data[4],[-p['h']],[p['h']],[p['b']],[2*p['b']]]
 if template=='line_cubic':
  return [[p['s']],[p['s']-p['h']],[p['s']+3*p['h']],[p['s']+p['h']],[p['s']-3*p['h']]] if profile in ('raw','observed') else [data[4],[-p['h']],[-3*p['b']],[p['h']],[3*p['b']]]
 if template=='power_line':
  return [[p['a']*p['n']],[p['a']],[p['b']],[-1],roots] if profile in ('raw','observed') else [roots,[p['s']+1],[p['s']-1],[p['n']-1],[p['n']]]
 return [[z] for z in roots]

def bank_value(template,values,index,field_index,profile):
 raw=profile=='raw';sid=DEFS[template][1]
 if template.startswith('circle'):
  if raw and template=='circle_vertical' and field_index==0:
   # Legacy notation uses the Unicode pi glyph; the operative component is identical.
   v=['$t = '+tex(z).replace(r'\pi ','π')+'$' for z in values]
  else:v=['$t='+tex(z)+'$' for z in values]
  return ' and '.join(v)+(' only' if template=='circle_vertical' and len(v)==1 else '')
 if template=='line_cubic':return 't ='+(' ' if values[0]>=0 else '')+tex(values[0])
 return 't='+tex(values[0])

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('Unknown level')
 rng=random.Random(seed)
 eligible=[k for k,v in DEFS.items() if v[0]==level and (field_type is None or field_type==('blank' if k in ('polynomial_two','spiral_cos','spiral_sin','paired_cubics') else 'radio'))]
 if template is None:
  if not eligible:raise ValueError('Unsupported field type')
  template=rng.choice(eligible)
 if template not in eligible:raise ValueError('Template/difficulty/field type mismatch')
 profile=profile or 'method'
 if profile not in ('raw','observed','method'):raise ValueError('Unknown complete bank profile')
 if template=='paired_cubics' and profile!='method':raise ValueError('Hard is authored only')
 explicit=parameters is not None
 for attempt in range(500):
  p=guards(template,parameters) if explicit else sample(template,rng)
  data=mathematics(template,p);objects=bank_objects(template,p,data,profile)
  normalized=[tuple(sorted(map(e,v),key=str)) for v in objects]
  if len(set(normalized))==len(normalized):break
  if explicit:raise ValueError('Reject entire colliding bank')
 else:raise ValueError('No eligible whole bank')
 x,y,dx,dy,roots,o,domain=data;raw=profile=='raw';sid=DEFS[template][1]
 if sid:
  prompt,solution=source_render(template,p,data,raw)
  source=QUESTIONS[sid];fielddefs=source[':question/answer-fields'] if raw else [f for f in source[':question/answer-fields'] if template!='circle_vertical' or ':answer-field/correct' in f]
 else:
  prompt='A curve is defined by the parametric equations\n\n$$\nx='+poly(x)+r',\,y='+poly(y)+r',\,-\infty<t<\infty.'+'\n$$\n\nDetermine the values of $t$ at which the tangent to the curve is horizontal. Give exact answers.\n\nIn **ascending order**, the tangent to the curve is horizontal at $t=$\n{{field-1}}\nand $t=$\n{{field-2}}.'
  solution=normal_solution(data);fielddefs=[{':answer-field/key':'field-'+str(i+1),':answer-field/type':{':db/ident':':answer-field.type/blank'},':answer-field/choices':[{}],':answer-field/correct':{}} for i in range(2)]
 # Preserve field ordering/key ownership (q357255 capture order is field2,field1).
 fields=[]
 for fi,f in enumerate(fielddefs):
  key=f[':answer-field/key'];kind=f[':answer-field/type'][':db/ident'];choices=[];correct_index=None
  if kind.endswith('/blank'):
   rootindex=int(key.split('-')[-1])-1;vals=[tex(roots[rootindex])];atype=':answer.type/math';correct_index=0
  else:
   vals=[bank_value(template,v,i,fi,profile) for i,v in enumerate(objects)];atype=':answer.type/text' if template.startswith('circle') else ':answer.type/math'
   correct_index=next(i for i,v in enumerate(objects) if tuple(v)==tuple(roots))
   if raw and template=='circle_vertical' and fi==0:
    # Raw legacy bank has its own order, recovered as whole operations.
    order=[4,1,0,3,2];vals=[vals[i] for i in order];correct_index=1
  for value in vals:choices.append({':answer/value':value,':answer/type':atype})
  fields.append({':answer-field/key':key,':answer-field/type':kind,':answer-field/choices':choices,'_correct':correct_index,'_present':not raw or ':answer-field/correct' in f})
 q={':question/problem':prompt,':question/answer-fields':fields}
 if solution is not None:q[':question/worked-solution']=solution
 if not raw or ':question/difficulty' in QUESTIONS[sid]:q[':question/difficulty']=':question.difficulty/'+level
 # Profiles/unused aliases/seed do not manufacture content identity.
 content={'version':VERSION,'problem':prompt,'solution':solution,'difficulty':q.get(':question/difficulty'),'fields':fields}
 identity=digest(content);qid=uid(['question',identity]);q[':question/id']=qid
 for f in fields:
  f[':answer-field/id']=uid([qid,f[':answer-field/key'],f[':answer-field/type'],len(fields),fields.index(f)])
  for answer in f[':answer-field/choices']:answer[':answer/id']=uid([f[':answer-field/id'],answer[':answer/value']])
  ci=f.pop('_correct');present=f.pop('_present')
  if present:f[':answer-field/correct']=[':answer/id',f[':answer-field/choices'][ci][':answer/id']]
  if f[':answer-field/type'].endswith('/radio'):rng.shuffle(f[':answer-field/choices'])
 if raw:
  # Missing raw attributes remain genuinely absent, not null-valued.
  q[':question/math-academy-id']=sid
 regular=all(sp.simplify((dx if o=='horizontal' else dy).subs(T,z))!=0 for z in roots)
 if not regular:raise ValueError('Stationary roots are outside supported scope')
 return {'knowledge_point':{'db_id':KP[':db/id'],'id':KP[':knowledge-point/id'],'title':KP[':knowledge-point/title']},'question':q,'generation':{
  'version':VERSION,'seed':seed,'template':template,'profile':profile,'source_id':sid,'parameters':{k:str(v) for k,v in p.items()},'source':{k:SOURCE[k] for k in ('database','basis','lineage')},
  'evidence_only':raw or (profile=='observed' and template in ('line_quadratic','line_cubic','power_line')),'eligible_for_learning':not raw and not (profile=='observed' and template in ('line_quadratic','line_cubic','power_line')),
  'authored_level':level=='hard' or template=='line_cubic','domain':str(domain),'regular_only':True,'orientation':o,'roots':[str(z) for z in roots],
  'curve':{'x':str(x),'y':str(y),'dx':str(dx),'dy':str(dy)},'task_fingerprint':task_key(dx,dy,domain,o),'content_fingerprint':identity,
  'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__},'plot_rating':'none','bank_objects':[[str(z) for z in v] for v in objects]}}

# Easy: observed linear/power, half-circle, quadratic-factor and spiral masks.
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
# Moderate: observed full-circle vertical and odd-power/linear masks.
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
# Hard: authored both-component cubic, two regular roots with two nonconstant checks.
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)
def markdown(record):
 q=record['question'];rows=[q[':question/problem']]
 for f in q.get(':question/answer-fields',[]):rows.append('\n'+f[':answer-field/key']+'\n'+'\n'.join('- '+a[':answer/value'] for a in f[':answer-field/choices']))
 if ':question/worked-solution' in q:rows.append('\n'+q[':question/worked-solution'])
 return '\n'.join(rows)

# Every learner-facing checkbox question has a nonempty correct selection.
import sys as _policy_sys
from pathlib import Path as _PolicyPath
_policy_sys.path.insert(0, str(next(p for p in _PolicyPath(__file__).resolve().parents if (p / "scripts/generator_policy.py").is_file())))
from scripts.generator_policy import nonempty_checkbox as _nonempty_checkbox
for _policy_name in ['generate', 'generate_easy', 'generate_hard', 'generate_moderate']:
    globals()[_policy_name] = _nonempty_checkbox(globals()[_policy_name])


from ca_source_runtime import install as _ca_source_install
_ca_source_install(globals(),_ca_Path(__file__).with_name('17592186083278-source-policy.json'))

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=1);parser.add_argument('--format',choices=['markdown','json'],default='markdown');parser.add_argument('--template');parser.add_argument('--profile')
 args=parser.parse_args();levels=['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]
 records=[generate(level,args.seed+i,template=args.template,profile=args.profile) for level in levels for i in range(args.count)]
 print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
