#!/usr/bin/env python3
"""Express flux as a parameter-domain double integral; never evaluate flux.

Basis 1356, math lineage 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1.
Nine observed source families with complete five-option replay banks; authored
method-error default banks and two explicitly authored missing-hard families.
Original-bank expressions generalize under uniform scaling of the vector field;
this is an expression-pattern replay convention, NOT recovered error intent.
Defaults vary independent field coefficients and existing surface coefficients.
Exact SymPy derivatives, substitution, ordered cross product, and dot product
feed prompts, banks and a single worked solution. No source-answer lookup and no
literal source-record return. Rendering normalizes legacy Unicode math while
retaining source sentences, demand, layout, and worked-solution stage sequence.
No plots, database clients, engine changes, or transactions.
"""
from __future__ import annotations
import argparse, hashlib, json, random, uuid
from pathlib import Path
import sympy as sp
u,v,x,y,z=sp.symbols('u v x y z',real=True)
KP_ID=17592186198378
KP_UUID='e9b46ce4-cfe0-5da6-bc91-65ae8c544393'
TITLE='Expressing Flux Through a Surface as a Double Integral'
VERSION='flux-integral-1'
PROVENANCE={'database':'math','basis':1356,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}
TEMPLATES={
 'product_affine':('moderate','q-160839',dict(a=1,b=2,c=1)),
 'quadratic_cancel':('easy','q-160840',dict(a=2,b=1,c=2,d=1,e=1)),
 'quadratic_diagonal':('easy','q-161249',dict(a=2,b=2,c=1)),
 'cubic_ruled':('moderate','q-161303',dict(a=1,b=2,c=2,d=3)),
 'exponential_sum':('moderate','q-161306',dict(a=1,b=1,k=1)),
 'ruled_square':('easy','q-161384',dict(a=1,b=1,c=1)),
 'polar_hint':('easy','q-161251',dict(a=3,b=3,c=1,h=1)),
 'bilinear_hint':('easy','q-161383',dict(a=1,b=1,c=1)),
 'graph_sum':('moderate','q-161304',dict(a=1,b=1,c=1,h=2)),
 'polar_unhinted':('hard',None,dict(a=2,b=3,c=1,h=1)),
 'exponential_unhinted':('hard',None,dict(a=1,b=2,c=1,p=1,q=1)),
}
# Each tuple preserves one WHOLE observed bank in its captured order.
# These formulas are expression-pattern evidence, not diagnoses. The factor s
# is uniform F scaling, applicable only to original parameter ratios.
OBSERVED={
 'product_affine':('4','2','5','8','3'),
 'quadratic_cancel':('8*u*v**3+8*u**3*v','8*u*v**3','2*u*v**3+4*u**3*v','4*u*v**3+2*u**3*v','8*u**3*v'),
 'quadratic_diagonal':('2*u**2*v**2','u**3*v+u*v**3','-2*u**3*v-2*u*v**3','6*u**2*v**2','u**2*v-2*u**2*v**2+u*v**2'),
 'cubic_ruled':('4','-2','0','-4','2'),
 'exponential_sum':('-2','-1','0','1','2'),
 'ruled_square':('2*u**2','u*v**2-2*v**3','2*u**2+u*v','u**2-v**2','2*u**3-u**2'),
 'polar_hint':('6*u**3','u**3*sin(v)*cos(v)','2*u**2*sin(v)*cos(v)','-5*u**3','-3*u**2'),
 'bilinear_hint':('u**2*v','u*v**2-u**2*v','u**2*v**2-2*u*v','u*v**2+u*v+2*u**2*v','u*v**2-u*v+u**2*v'),
 'graph_sum':('3','-2','-4','0','1'),
}
LOCALS={'u':u,'v':v,'sin':sp.sin,'cos':sp.cos,'exp':sp.exp}
def simplify(e):
 # Use only the source's Pythagorean identity, never introduce double angles.
 return sp.expand(sp.expand(e).subs(sp.cos(v)**2,1-sp.sin(v)**2))
def tex(e):return sp.latex(sp.expand(e)).replace(r'\left(',r'\left(')
def vec(items):return r'\left\langle '+r',\,'.join(tex(e) for e in items)+r'\right\rangle'
def block(t):return '$$\n'+t+'\n$$'
def align(rows):return block(r'\begin{aligned}'+r' \\ '.join(a+' & ='+b for a,b in rows)+r'\end{aligned}')
def digest(value):return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(key):return str(uuid.uuid5(uuid.UUID(KP_UUID),key))
class SampleRejected(ValueError):pass

# Shared exact mathematical builders, with easy/moderate/hard rendering below.
def objects(name,p):
 a,b,c=p.get('a',1),p.get('b',1),p.get('c',1)
 if name=='product_affine':F=[a*x*z,b*y,c];r=[u*v,u+v,1-v];basis=[u*v**2,v**2,u*v];residual=c*(v-u)
 elif name=='quadratic_cancel':F=[a*x+b*y,c*z,p['d']*y+p['e']*z];r=[-u**2,2*u**2-v**2,v**2];basis=None;residual=0
 elif name=='quadratic_diagonal':F=[a*x,b*y,c*z];r=[u**2,-u*v,v**2];basis=None;residual=0
 elif name=='cubic_ruled':F=[a,0,b];r=[u+v,u**2+c*v,u**3+p['d']*v];basis=[u**2,u,sp.Integer(1)];residual=0
 elif name=='exponential_sum':F=[p['k']*x-a/z,p['k']*y+b/z,p['k']*z];r=[u*sp.exp(v),u*sp.exp(-v),u];basis=[sp.exp(v),sp.exp(-v)];residual=0
 elif name=='ruled_square':F=[a*z**2,b*y**2,c*x];r=[u**2,v,u];basis=None;residual=0
 elif name in ('polar_hint','polar_unhinted'):F=[a*x,b*y,c*z];r=[u*sp.cos(v),u*sp.sin(v),p['h']*u**2];basis=None;residual=0
 elif name=='bilinear_hint':F=[a*x*z,b*y,c*x*z];r=[u,u*v,v];basis=None;residual=0
 elif name=='graph_sum':F=[a*x**2,b*x*y,c*z];r=[u,v,p['h']*u*v];basis=[u*v,u**2*v];residual=0
 elif name=='exponential_unhinted':F=[a*x-p['p']/z,b*y+p['q']/z,c*z];r=[u*sp.exp(v),u*sp.exp(-v),u];basis=None;residual=0
 else:raise ValueError(name)
 F=sp.Matrix([sp.sympify(t) for t in F]);r=sp.Matrix(r)
 ru,rv=r.diff(u),r.diff(v);cross=ru.cross(rv).applyfunc(simplify)
 pulled=F.subs(dict(zip((x,y,z),r)),simultaneous=True).applyfunc(simplify)
 contributions=[simplify(f*n) for f,n in zip(pulled,cross)]
 integrand=simplify(sum(contributions))
 coeffs=[]
 if basis:
  rem=sp.expand(integrand-residual)
  for term in basis:
   if term==sp.exp(v):coeff=sp.expand(rem).coeff(sp.exp(v))
   elif term==sp.exp(-v):coeff=sp.expand(rem).coeff(sp.exp(-v))
   elif term==1:coeff=rem.subs({u:0,v:0})
   else:coeff=rem.coeff(u,sp.degree(term,u)).coeff(v,sp.degree(term,v))
   coeffs.append(simplify(coeff))
  if simplify(rem-sum(k*t for k,t in zip(coeffs,basis)))!=0:raise SampleRejected('Coefficient basis incomplete')
 return {'F':F,'r':r,'ru':ru,'rv':rv,'cross':cross,'pulled':pulled,'contributions':contributions,'integrand':integrand,'basis':basis,'residual':residual,'coefficients':coeffs,'correct':sum(coeffs) if basis else integrand}

def coefficient_value(data,expression):
 """Same response projection applied to a mathematically wrong integrand."""
 basis=data['basis']
 if not basis:return simplify(expression)
 e=sp.expand(expression-data['residual']);out=0
 for term in basis:
  if term==sp.exp(v) or term==sp.exp(-v):out+=e.coeff(term)
  elif term==1:out+=e.subs({u:0,v:0})
  else:out+=e.coeff(u,sp.degree(term,u)).coeff(v,sp.degree(term,v))
 return simplify(out)

def authored_bank(data):
 """Complete authored bank: reversed cross, wrong cofactor sign, omission,
 and substitution omitted (F(u,v,1)). Reject the whole bank on any collision.
 Alternative complete banks are deterministic and explicitly named below.
 """
 t=data['contributions'];G=data['integrand'];F=data['F'];N=data['cross']
 recipes={
  'reverse_cross':-G,
  'wrong_middle_cofactor':t[0]-t[1]+t[2],
  'wrong_first_cofactor':-t[0]+t[1]+t[2],
  'wrong_third_cofactor':t[0]+t[1]-t[2],
  'omit_first_component':t[1]+t[2],
  'omit_second_component':t[0]+t[2],
  'omit_third_component':t[0]+t[1],
  'omit_surface_substitution':F.subs({x:u,y:v,z:1},simultaneous=True).dot(N),
  'add_components_instead_of_dot':sum(data['pulled']),
  'use_tangent_u_instead_of_cross':data['pulled'].dot(data['ru']),
  'use_tangent_v_instead_of_cross':data['pulled'].dot(data['rv']),
 }
 # A complete bank is chosen first. No pooling of the first distinct candidates.
 patterns={
  'authored_cubic':('reverse_cross','wrong_first_cofactor','wrong_third_cofactor','use_tangent_v_instead_of_cross'),
  'authored_cofactor':('reverse_cross','wrong_middle_cofactor','omit_surface_substitution','add_components_instead_of_dot'),
  'authored_tangents':('reverse_cross','use_tangent_u_instead_of_cross','use_tangent_v_instead_of_cross','omit_surface_substitution'),
 }
 return recipes,patterns

def validate_parameters(name,p):
 expected=set(TEMPLATES[name][2])|{'scale'}
 if set(p)!=expected:raise ValueError(f'Parameters must be exactly {sorted(expected)}')
 if any(type(k) is not int or not 1<=k<=6 for k in p.values()):raise ValueError('All coefficients and scale must be integers in 1..6')
 if name=='polar_unhinted' and p['a']==p['b']:raise ValueError('Hard polar family uses unequal radial coefficients')
 if name=='exponential_unhinted' and p['a']+p['b']==2*p['c']:raise ValueError('Hard exponential family retains a nonzero u^2 term')

def render(name,p,data):
 level,source,base=TEMPLATES[name]
 F,r,N,P=data['F'],data['r'],data['cross'],data['pulled']
 symbols=sp.symbols('a b c')[:len(data['coefficients'])]
 coefficient_prompt=sum(symbol*t for symbol,t in zip(symbols,data['basis'] or []))+data['residual']
 integral_lhs=r'\iint_S F\cdot\mathrm{d}\mathbf S'
 integral_rhs=r'\iint_D '+(tex(coefficient_prompt) if data['basis'] else r'\boxed{}')+r'\,\mathrm{d}A'
 prompt='Consider the vector field $F$ and the surface $S$ with parametrization $r(u,v),$ where\n\n'+block('F(x,y,z)='+vec(F)+r',\quad r(u,v)='+vec(r)+r',\quad (u,v)\in D\subset\mathbb R^2.')
 if name=='cubic_ruled' and 4*p['d']==3*p['c']**2:prompt+='\n\n'+r'Assume $D$ excludes $u='+tex(sp.Rational(p['c'],2))+'$, where the parametrization is singular.'
 if name.startswith('exponential'):prompt+='\n\n'+r'Assume $D\subset\{(u,v):u>0\}$, so the vector field is defined on $S$.'
 if name.startswith('polar'):prompt+='\n\n'+r'Assume $D\subset\{(u,v):u>0,\ 0<v<2\pi\}$.'
 if name in ('quadratic_cancel','quadratic_diagonal'):prompt+='\n\n'+r'Assume $D\subset\{(u,v):u>0,\ v>0\}$.'
 prompt+='\n\nIf the flux of $F$ across $S$ with respect to $n$ is given by\n\n'+block(integral_lhs+'='+integral_rhs)
 if data['basis']:prompt+='\n\nwhat is the value of $'+'+'.join(str(t) for t in symbols)+'?$'
 else:prompt+='\n\nwhat is the missing expression?'
 if level=='easy':prompt+='\n\n*Hint: You can use the fact that $'+r"r'_u\times r'_v="+vec(N)+'.$*'
 formula=integral_lhs+r"=\iint_S F\cdot n\,\mathrm{d}S=\iint_D F(r(u,v))\cdot (r'_u\times r'_v)\,\mathrm{d}A."
 solution='For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\\in D,$ the flux of a vector field $F$ over $S$ is given by\n\n'+block(formula)
 if level=='easy':solution+='\n\nNotice we are told that the fundamental vector product for our surface is\n\n'+block(r"r'_u\times r'_v="+vec(N)+'.')
 else:
  tangent_rows=[]
  for variable,tangent in ((u,data['ru']),(v,data['rv'])):
   lhs="r'_"+str(variable)
   derivative_vec=r'\left\langle '+r',\,'.join(r'\frac{\partial}{\partial '+str(variable)+'}('+tex(e)+')' for e in r)+r'\right\rangle'
   tangent_rows.extend([(lhs,r'\left\langle '+r',\,'.join(r'\frac{\partial '+str(e)+r'}{\partial '+str(variable)+'}' for e in (x,y,z))+r'\right\rangle'),('',derivative_vec),('',vec(tangent))])
  solution+='\n\nWe first compute the tangent vectors to the grid curves:\n\n'+align(tangent_rows)
  determinant=r'\begin{vmatrix}\mathbf i&\mathbf j&\mathbf k\\'+ '&'.join(tex(e) for e in data['ru'])+r'\\'+'&'.join(tex(e) for e in data['rv'])+r'\end{vmatrix}'
  minors=[]
  for i,(j,k) in enumerate(((1,2),(0,2),(0,1))):
   minors.append(('-' if i==1 else '')+r'\begin{vmatrix}'+tex(data['ru'][j])+'&'+tex(data['ru'][k])+r'\\'+tex(data['rv'][j])+'&'+tex(data['rv'][k])+r'\end{vmatrix}')
  solution+='\n\nNow, the fundamental vector product is\n\n'+align([(r"r'_u\times r'_v",determinant),('',r'\left\langle '+','.join(minors)+r'\right\rangle'),('',vec(N)+'.')])
 substitutions=r'\big|_{'+r',\,'.join(str(coordinate)+'='+tex(e) for coordinate,e in zip((x,y,z),r))+'}'
 # Unsimplified substitution is rendered explicitly before simplification.
 raw=[]
 for expression in F:
  text=tex(expression)
  for coordinate,e in zip((x,y,z),r):text=text.replace(str(coordinate),r'\left('+tex(e)+r'\right)')
  raw.append(text)
 solution+='\n\nNext, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$\n\n'+align([('F(r(u,v))',vec(F)+substitutions),('',r'\left\langle '+r',\,'.join(raw)+r'\right\rangle'),('',vec(P))])
 dot_sum='+'.join(r'\left('+tex(f)+r'\right)\cdot\left('+tex(n)+r'\right)' for f,n in zip(P,N))
 expanded_sum='+'.join(r'\left('+tex(t)+r'\right)' for t in data['contributions'])
 solution+='\n\nFinally, we calculate the dot product of $F$ and ${r}_{u}^{′}\\times {r}_{v}^{′}:$\n\n'+align([(r"F(r(u,v))\cdot (r'_u\times r'_v)",vec(P)+r'\cdot '+vec(N)),('',dot_sum),('',expanded_sum)]+([('',tex(-2*p['h']*p['a']*p['scale']*u**3)+r'\left(\cos^2 v+\sin^2 v\right)+'+tex(p['h']*p['c']*p['scale']*u**3))] if name in ('polar_hint','polar_unhinted') and p['a']==p['b'] else [])+[('',tex(data['integrand'])+'.')])
 solution+='\n\nTherefore, the surface integral can be written as\n\n'+align([(integral_lhs,r"\iint_D F(r(u,v))\cdot(r'_u\times r'_v)\,\mathrm{d}A"),('',r'\iint_D '+tex(data['integrand'])+r'\,\mathrm{d}A.')])
 if data['basis']:
  equation='+'.join(str(t) for t in symbols)+'='+ '+'.join('('+tex(k)+')' for k in data['coefficients'])+'='+tex(data['correct'])+'.'
  solution+='\n\nFinally, \n\n'+block(equation)
 return prompt,solution

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if field_type not in (None,'radio'):raise ValueError('Only observed radio fields are supported')
 eligible=[n for n,spec in TEMPLATES.items() if spec[0]==level]
 if template is not None and template not in eligible:raise ValueError('Template does not belong to level')
 rng=random.Random(seed);name=template or rng.choice(eligible)
 if profile not in (None,'observed', 'authored_cofactor','authored_tangents','authored_cubic'):raise ValueError('Unknown complete bank profile')
 if profile=='observed' and name not in OBSERVED:raise ValueError('No observed hard bank')
 # Fixed parameters use a fixed default complete bank independent of seed.
 default_profile=('authored_cubic' if name=='cubic_ruled' else 'authored_tangents' if level=='moderate' or name=='ruled_square' else 'authored_cofactor')
 if profile not in (None,'observed',default_profile):raise ValueError('Authored complete bank is not eligible for this template')
 profile=profile or default_profile
 for attempt in range(200):
  if parameters is not None:p=dict(parameters)
  elif profile=='observed':p={**TEMPLATES[name][2],'scale':rng.choice((1,2,3,4))}
  else:p={k:rng.randint(1,4) for k in TEMPLATES[name][2]};p['scale']=1
  try:
   validate_parameters(name,p)
   if profile=='observed' and any(p[k]!=val for k,val in TEMPLATES[name][2].items()):raise ValueError('Observed expression-pattern bank requires captured parameter ratios')
   data=objects(name,p)
   scale=p['scale']
   # Uniform F scaling preserves observed bank patterns; no unrelated offsets.
   for key in ('F','pulled'):data[key]=data[key]*scale
   for key in ('integrand','correct','residual'):data[key]=data[key]*scale
   for key in ('contributions','coefficients'):data[key]=[t*scale for t in data[key]]
   if profile=='observed':options=[sp.sympify(e,locals=LOCALS)*scale for e in OBSERVED[name]];recipes=['observed_expression_pattern_'+str(i) for i in range(5)]
   else:
    mistakes,patterns=authored_bank(data);chosen=patterns[profile]
    options=[data['correct']]+[coefficient_value(data,mistakes[key]) for key in chosen];recipes=['correct',*chosen]
   options=[simplify(e) for e in options]
   if any(simplify(a-b)==0 for i,a in enumerate(options) for b in options[i+1:]):raise SampleRejected('Whole complete bank is ambiguous')
   matches=[i for i,e in enumerate(options) if simplify(e-data['correct'])==0]
   if len(matches)!=1:raise SampleRejected('Complete bank must have exactly one mathematically correct answer')
   prompt,solution=render(name,p,data)
   canonical={'template':name,'parameters':p,'domain':domain(name,p)};paramfp=digest(canonical)
   contentfp=digest({**canonical,'prompt':prompt,'solution':solution,'bank':sorted(sp.srepr(e) for e in options)})
   qid=uid(contentfp);fid=uid(contentfp+':selection')
   answers=[{':answer/id':uid(fid+':'+sp.srepr(e)),':answer/type':':answer.type/math',':answer/value':tex(e)} for e in options]
   answer_math={a[':answer/id']:str(e) for a,e in zip(answers,options)}
   correct=answers[matches[0]][':answer/id'];rng.shuffle(answers)
   return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]}]},'generation':{'version':VERSION,'sympy_version':sp.__version__,'seed':seed,'template':name,'parameters':p,'bank_profile':profile,'bank_origin':'observed-pattern-replay' if profile=='observed' else 'authored','authored_extension':profile!='observed' or level=='hard','source_analysis':{**PROVENANCE,'question_ids':[TEMPLATES[name][1]] if TEMPLATES[name][1] else ['q-161251' if name=='polar_unhinted' else 'q-161306'],'canonical':'e-12355'},'parameter_fingerprint':paramfp,'content_fingerprint':contentfp,'domain':domain(name,p),'plot_rating':'none','plot_assets':{},'recipes':recipes,'answer_math':answer_math,'mathematics':{key:[str(t) for t in value] if isinstance(value,(list,sp.MatrixBase)) else str(value) for key,value in data.items() if key!='basis'},'basis':[str(t) for t in data['basis']] if data['basis'] else None}}
  except SampleRejected:
   if parameters is not None:raise
  except ValueError:
   if parameters is not None or profile=='observed':raise
 raise SampleRejected('No eligible whole bank after bounded sampling')

def domain(name,p=None):
 if name=='cubic_ruled' and p is not None and 4*p['d']==3*p['c']**2:return f"u > 0, u != {sp.Rational(p['c'],2)}, v real; orientation r_u cross r_v"
 if name.startswith('exponential'):return 'u > 0, v real; z=u nonzero; orientation r_u cross r_v'
 if name.startswith('polar'):return 'u > 0, 0 < v < 2*pi; orientation r_u cross r_v'
 if name in ('quadratic_cancel','quadratic_diagonal'):return 'u > 0, v > 0; orientation r_u cross r_v'
 return 'u > 0, v real; orientation r_u cross r_v'

# EASY — given cross product, substitution and dot product.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE — derive tangents/cross product, substitute, collect coefficients.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# HARD — authored; derive same cross product, keep full trig/exp integrand.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)

def markdown(record):
 q,g=record['question'],record['generation'];field=q[':question/answer-fields'][0]
 rows=['### '+g['template']+' — '+q[':question/difficulty'].split('/')[-1],f"Author metadata: {g['bank_profile']}; parameters `{g['parameters']}`.",'',q[':question/problem'],'']
 for a in field[':answer-field/choices']:rows.append('- $'+a[':answer/value']+'$'+(' **correct**' if a[':answer/id']==field[':answer-field/correct'][1] else ''))
 rows+=['','Worked solution:',q[':question/worked-solution']]
 return '\n'.join(rows)
def main():
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=1);parser.add_argument('--format',choices=['markdown','json'],default='markdown');parser.add_argument('--template',choices=list(TEMPLATES));parser.add_argument('--profile',choices=['observed','authored_cofactor','authored_tangents','authored_cubic'])
 args=parser.parse_args()
 if args.count<1:parser.error('count must be positive')
 levels=['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]
 records=[generate(level,args.seed+i,args.template,profile=args.profile) for level in levels for i in range(args.count)]
 print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
if __name__=='__main__':main()
