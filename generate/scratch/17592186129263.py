#!/usr/bin/env python3
"""Evaluate 2x2 Jacobian determinants at stated points; local JSON only.

Observed scalar banks have underdetermined error intent. Explicit observed
profiles apply normalized scalar patterns to the independently derived value;
these are not promoted to default generation. Default five-option banks use
whole derivative/evaluation error operations. Moderate and hard are authored
level assignments grounded in the owning route and sibling canonical powers.
All levels differentiate four entries, compute ad-bc, and evaluate one point.
"""
from __future__ import annotations
import argparse,hashlib,json,random,uuid
import sympy as sp
KP_ID=17592186129263
KP_UUID='ab643519-92a4-5ccf-b826-fb2a68b36534'
TITLE='Evaluating a Jacobian Determinant'
VERSION='evaluated-jacobian-1'
PROVENANCE={'database':'math','basis':1356,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}
u,v=sp.symbols('u v',real=True)
TEMPLATES={
 'polar':('easy',{'a':2,'b':3,'U':'1','V':'2'}),
 'exp_pair':('easy',{'a':1,'b':1,'U':'0','V':'-5'}),
 'quotient':('easy',{'a':1,'b':1,'U':'-2','V':'3'}),
 'exp_log':('easy',{'a':1,'b':1,'U':'1','V':'1'}),
 'square_pair':('easy',{'a':1,'b':1,'U':'-2','V':'1'}),
 'complex_square':('easy',{'a':1,'b':1,'U':'-1','V':'-2'}),
 'mixed_linear':('easy',{'a':1,'b':1,'U':'8','V':'-2'}),
 'diagonal_trig':('easy',{'a':1,'b':1,'U':'pi/6','V':'0'}),
 'coupled_trig':('easy',{'a':1,'b':1,'U':'pi/4','V':'pi/4'}),
 'quadratic_linear':('easy',{'a':3,'b':2,'c':1,'d':2,'U':'1','V':'1'}),
 'scaled_exp_log':('moderate',{'a':2,'b':3,'U':'3','V':'2'}),
 'scaled_coupled_trig':('moderate',{'a':2,'b':1,'c':1,'d':2,'U':'pi/6','V':'pi/6'}),
 'powers':('hard',{'a':1,'b':1,'m':3,'n':2,'U':'2','V':'1'}),
}
# Ratios describe the complete observed scalar pattern; intent is unresolved.
# No literal source payload or answer lookup occurs in generation.
OBSERVED={
 'observed_polar':('polar','q-160380',['0','2/3','2','4/3','1']),
 'observed_exp_pair':('exp_pair','q-160394',['-3/2','1','1/2','-1/2','3/2']),
 'observed_quotient':('quotient','q-160383',['4/3','1','-1','-1/3','-2/3']),
 'observed_exp_log':('exp_log','q-160402',['1','0','1/2','3/2','-1/2']),
 'observed_square_pair':('square_pair','q-160427',['1','-1/2','7/8','3/4','9/8']),
 'observed_complex_square':('complex_square','q-160428',['1','-2/5','2/5','3/5','8/5']),
 'observed_mixed_linear':('mixed_linear','q-160431',['2','3','1/2','1','3/2']),
 'observed_diagonal_trig':('diagonal_trig','q-160440',['2','0','-1','-2','1']),
 'observed_diagonal_trig_scaled':('diagonal_trig','q-160445',['1','2/3','2','4/3','-2']),
 'observed_coupled_trig':('coupled_trig','q-160434',['1','1/2','2','-1/2','-1']),
 'observed_quadratic_linear':('quadratic_linear','q-160387',['10/11','12/11','6/11','1','8/11']),
}
BANK_PROFILES={**{k:{'template':t,'source':s,'origin':'observed normalized scalar pattern; error intent unresolved'} for k,(t,s,_) in OBSERVED.items()},**{'authored_'+t:{'template':t,'source':None,'origin':'authored determinant and evaluation operations'} for t in TEMPLATES}}
class SampleRejected(ValueError):pass

def tex(z):return sp.latex(z)
def clean(z):return sp.factor(sp.trigsimp(sp.simplify(z)))
def eq(a,b):return sp.simplify(sp.trigsimp(a-b))==0
def block(s):return '$$\n'+s+'\n$$'
def matrix(a,b,c,d):return r'\left|\begin{matrix}'+a+'&'+b+r'\\'+c+'&'+d+r'\end{matrix}\right|'
J=r'\frac{\partial(x,y)}{\partial(u,v)}'
PARTIALS=[r'\frac{\partial x}{\partial u}',r'\frac{\partial x}{\partial v}',r'\frac{\partial y}{\partial u}',r'\frac{\partial y}{\partial v}']

def coordinates(p):return sp.sympify(p['U'],locals={'pi':sp.pi}),sp.sympify(p['V'],locals={'pi':sp.pi})
def validate_parameters(t,p):
 if set(p)!=set(TEMPLATES[t][1]):raise ValueError('Exact template parameter keys required')
 for k,z in p.items():
  if k not in ('U','V') and (type(z) is not int or not -8<=z<=8 or z==0):raise ValueError('Small nonzero integer coefficients required')
 U,V=coordinates(p)
 allowed_ints=[sp.Integer(z) for z in range(-8,9)]
 allowed_angles=[z*sp.pi/12 for z in range(-12,13)]
 if t in ('diagonal_trig','coupled_trig','scaled_coupled_trig'):
  if U not in allowed_angles or V not in allowed_angles:raise ValueError('Familiar twelfth-turn angles required')
 elif U not in allowed_ints or V not in allowed_ints:raise ValueError('Small signed integer point required')
 if t in ('diagonal_trig','coupled_trig','scaled_coupled_trig'):
  angles=[U,V] if t=='diagonal_trig' else [U+V,U-V] if t=='coupled_trig' else [p['a']*U+p['b']*V,p['c']*U-p['d']*V]
  if any(sp.denom(sp.cancel(z/sp.pi)) not in (1,2,3,4,6) for z in angles):raise ValueError('All evaluated trig arguments must use familiar sixth/quarter turns')
 if t=='scaled_exp_log' and (not all(2<=p[k]<=7 for k in ('a','b')) or p['a']==p['b']):raise ValueError('Moderate exp/log requires unequal chain coefficients between 2 and 7')
 if t=='scaled_coupled_trig' and any(p[k] not in (1,2,3) for k in ('a','b','c','d')):raise ValueError('Moderate trig chain coefficients must be between 1 and 3')
 if t=='scaled_coupled_trig' and sum(p[k]>1 for k in ('a','b','c','d'))<2:raise ValueError('Moderate trig requires at least two nonunit chain coefficients')
 if t=='quotient' and U==0:raise ValueError('u cannot be zero')
 if t in ('exp_log','scaled_exp_log') and U*V<=0:raise ValueError('uv must be positive')
 if t=='powers' and (abs(U)>4 or abs(V)>4 or max(abs(p['a']),abs(p['b']))>3):raise ValueError('Hard point/scale arithmetic bounds exceeded')
 if t=='powers' and (p['m'],p['n']) not in [(3,2),(2,3),(3,3)]:raise ValueError('Canonical comparable power bounds required')

def functions(t,p):
 a,b=p['a'],p['b']
 if t=='polar':return a*u*sp.cos(v),b*u*sp.sin(v),'R^2'
 if t=='exp_pair':return sp.exp(a*u+b*v),sp.exp(a*u-b*v),'R^2'
 if t=='quotient':return a*u*v,b*v/u,'u != 0'
 if t in ('exp_log','scaled_exp_log'):return sp.exp(a*u-b*v),sp.log(u*v),'uv > 0'
 if t=='square_pair':return a*u**2+b*v**2,a*u**2-b*v**2,'R^2'
 if t=='complex_square':return a*(u**2-v**2)/2,b*u*v,'R^2'
 if t=='mixed_linear':return a*v**2+b*u*v,v-u,'R^2'
 if t=='diagonal_trig':return a*sp.cos(u),b*sp.sin(v),'R^2'
 if t=='coupled_trig':return a*sp.cos(u+v),b*sp.sin(u-v),'R^2'
 if t=='scaled_coupled_trig':return sp.cos(a*u+b*v),sp.sin(p['c']*u-p['d']*v),'R^2'
 if t=='quadratic_linear':return a*u**2+b*v,p['c']*u+p['d']*v**2,'R^2'
 if t=='powers':return a*(u+v)**p['m'],b*(u-v)**p['n'],'R^2'
 raise ValueError(t)

def authored_bank(t,p,ds,j,U,V):
 A,B,C,D=ds;at=lambda z:clean(z.subs({u:U,v:V}))
 P,Q=at(A*D),at(B*C);answer=at(j)
 if t=='diagonal_trig':
  return [('correct',answer),('reverse_sign',-answer),('omit_trig_evaluation',-p['a']*p['b']),('wrong_cos_derivative',at(p['a']*p['b']*sp.cos(u)*sp.cos(v))),('wrong_sin_derivative',at(p['a']*p['b']*sp.sin(u)*sp.sin(v)))]
 if t in ('polar','exp_pair','exp_log','square_pair','coupled_trig','scaled_exp_log','scaled_coupled_trig','powers','quotient'):
  # These matrices can have cancelling equal products; use evaluated matrix
  # entries rather than an add-products bank that would duplicate zero options.
  return [('correct',answer),('reverse_subtraction',-answer),('omit_cross_product',P),('omit_second_diagonal_factor',at(A)-Q),('omit_first_diagonal_factor',at(D)-Q)]
 return [('correct',answer),('add_products',P+Q),('reverse_subtraction',-answer),('omit_cross_product',P),('omit_diagonal_product',-Q)]

def sample(t,rng):
 p=dict(TEMPLATES[t][1]);p['a']=rng.randint(1,5);p['b']=rng.randint(1,5)
 if t in ('diagonal_trig','coupled_trig','scaled_coupled_trig'):
  p['U']=rng.choice(['pi/6','pi/4','pi/3','-pi/6','-pi/4']);p['V']=rng.choice(['0','pi/6','pi/4','-pi/6'])
 else:p['U']=str(rng.choice([-4,-3,-2,-1,1,2,3,4]));p['V']=str(rng.choice([-4,-3,-2,-1,1,2,3,4]))
 if t=='exp_pair':p['U']='0'
 if t=='scaled_exp_log':p['a']=rng.randint(2,7);p['b']=rng.randint(2,7)
 if t in ('exp_log','scaled_exp_log'):
  p['U']=str(p['b']*rng.choice([-2,-1,1,2] if t=='scaled_exp_log' else [1,2]));p['V']=str(int(p['U'])*p['a']//p['b'])
 if t in ('quadratic_linear','scaled_coupled_trig'):p['c']=rng.randint(1,3);p['d']=rng.randint(1,3)
 if t=='scaled_coupled_trig':p['a']=rng.randint(1,3);p['b']=rng.randint(1,3)
 if t=='powers':p['m'],p['n']=rng.choice([(3,2),(2,3),(3,3)]);p['a']=rng.randint(1,3);p['b']=rng.randint(1,3)
 return p

def solution(t,x,y,ds,j,U,V):
 d=list(map(tex,ds));val=clean(j.subs({u:U,v:V}));at=sp.Subs(j,(u,v),(U,V)).doit()
 out='Given a transformation \n\n'+block(r'T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},')+'\n\nthe Jacobian determinant of $T,$ denoted $'+J+'$, is given by\n\n'+block(J+'='+matrix(*PARTIALS)+'.')
 out+='\n\nHere, we have $x(u,v)='+tex(x)+'$ and $y(u,v)='+tex(y)+'.$\n\nFirst, we find the partial derivatives:\n\n'
 out+=block(r'\begin{aligned}'+PARTIALS[0]+'&='+d[0]+r'&\quad '+PARTIALS[1]+'&='+d[1]+r'\\'+PARTIALS[2]+'&='+d[2]+r'&\quad '+PARTIALS[3]+'&='+d[3]+r'\end{aligned}')
 out+='\n\nTherefore, the corresponding Jacobian determinant is\n\n'
 rows=[J+'&='+matrix(*PARTIALS),'&='+matrix(*d),'&='+r'\left('+d[0]+r'\right)\cdot\left('+d[3]+r'\right)-\left('+d[1]+r'\right)\cdot\left('+d[2]+r'\right)']
 if t=='polar':rows+=['&='+tex(clean(j))+r'\left(\cos^2 v+\sin^2 v\right)']
 elif t in ('square_pair','coupled_trig','exp_pair','mixed_linear'):
  rows+=['&='+tex(ds[0]*ds[3])+'-'+r'\left('+tex(ds[1]*ds[2])+r'\right)']
 rows+=['&='+tex(j)+'.'];out+=block(r'\begin{aligned}'+r'\\'.join(rows)+r'\end{aligned}')
 out+='\n\nFinally, when $'+r'\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}'+tex(U)+r'\\'+tex(V)+r'\end{bmatrix}'+',$ the value of our Jacobian determinant is\n\n'
 # Unevaluated substitution is rendered explicitly, preserving powers/signs.
 substituted=j.xreplace({u:sp.Symbol('UPOINT'),v:sp.Symbol('VPOINT')})
 substitution_tex=tex(substituted).replace('UPOINT',r'\left('+tex(U)+r'\right)').replace('VPOINT',r'\left('+tex(V)+r'\right)')
 out+=block(r'\left.'+J+r'\right|_{('+tex(U)+','+tex(V)+')}='+substitution_tex+'='+tex(val)+'.')
 return out

def assemble(level,seed,t,p,profile):
 validate_parameters(t,p);U,V=coordinates(p);x,y,domain=functions(t,p)
 ds=[sp.diff(x,u),sp.diff(x,v),sp.diff(y,u),sp.diff(y,v)];j=clean(ds[0]*ds[3]-ds[1]*ds[2]);value=clean(j.subs({u:U,v:V}))
 if profile in OBSERVED:bank=[('correct' if k=='1' else 'observed_scalar_pattern_'+str(i),clean(sp.Rational(k)*value)) for i,k in enumerate(OBSERVED[profile][2])]
 else:bank=authored_bank(t,p,ds,j,U,V)
 bank=[(recipe,sp.sympify(z)) for recipe,z in bank]
 if any(z.has(sp.zoo,sp.nan,sp.oo,-sp.oo) for _,z in bank):raise SampleRejected('Nonfinite bank')
 if len(bank)!=5 or any(eq(a,b) for i,(_,a) in enumerate(bank) for _,b in bank[i+1:]):raise SampleRejected('Complete bank rejected: equivalent choices')
 if sum(eq(z,value) for _,z in bank)!=1:raise SampleRejected('Ambiguous correct answer')
 prompt='For the transformation $T,$ defined as\n\n'+block(r'T:\begin{bmatrix}u\\v\end{bmatrix}\longrightarrow\begin{bmatrix}'+tex(x)+r'\\'+tex(y)+r'\end{bmatrix}.')+'\n\ncompute the value of the Jacobian determinant at the point where $'+r'\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}'+tex(U)+r'\\'+tex(V)+r'\end{bmatrix}'+'.$'
 worked=solution(t,x,y,ds,j,U,V)
 finger=hashlib.sha256(json.dumps([sp.srepr(x),sp.srepr(y),sp.srepr(U),sp.srepr(V),domain]).encode()).hexdigest()
 content=hashlib.sha256(json.dumps([VERSION,level,prompt,worked,sorted(tex(z) for _,z in bank)]).encode()).hexdigest()
 qid=uuid.uuid5(uuid.UUID(KP_UUID),content);fid=uuid.uuid5(qid,'selection');answers=[];maths={};correct=None
 for recipe,z in bank:
  aid=str(uuid.uuid5(fid,tex(z)));answers.append({':answer/id':aid,':answer/type':':answer.type/math',':answer/value':tex(z)});maths[aid]={'expression':sp.srepr(z),'recipe':recipe}
  if eq(z,value):correct=aid
 random.Random(seed).shuffle(answers)
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':str(qid),':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':worked,':question/answer-fields':[{':answer-field/id':str(fid),':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]}]},'generation':{'version':VERSION,'sympy_version':sp.__version__,'seed':seed,'template':t,'parameters':p,'parameter_fingerprint':finger,'content_fingerprint':content,'bank_profile':profile,'bank_origin':BANK_PROFILES[profile]['origin'],'difficulty_origin':'observed' if level=='easy' else 'authored missing level','authored_extension':level!='easy' or profile.startswith('authored_'),'source_analysis':{**PROVENANCE,'question_ids':[BANK_PROFILES[profile]['source']] if BANK_PROFILES[profile]['source'] else [],'canonical_id':'e-11156','sibling_canonical_id':'e-6810'},'domain':domain,'plot_rating':'none','plot_assets':{},'functions':[sp.srepr(x),sp.srepr(y)],'partial_derivatives':list(map(sp.srepr,ds)),'determinant':sp.srepr(j),'evaluated_value':sp.srepr(value),'answer_math':maths}}

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('Unknown difficulty')
 if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Only radio field supported')
 if profile:
  if profile not in BANK_PROFILES:raise ValueError('Unknown profile')
  pt=BANK_PROFILES[profile]['template']
  if template and pt!=template:raise ValueError('Profile/template mismatch')
  template=pt
 eligible=[t for t,(l,_) in TEMPLATES.items() if l==level]
 if template and template not in eligible:raise ValueError('Template/level mismatch')
 rng=random.Random(seed);t=template or rng.choice(eligible);profile=profile or 'authored_'+t
 for _ in range(200):
  p=dict(parameters) if parameters is not None else sample(t,rng)
  try:return assemble(level,seed,t,p,profile)
  except ValueError:
   if parameters is not None:raise
 raise SampleRejected('No complete eligible bank within sampling bound')

# Easy: ten observed transformation/evaluation families, eleven explicit banks.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# Moderate: authored familiar-point evaluations of scaled exp/log and trig pairs.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# Hard: sibling canonical powers, then small signed-point arithmetic only.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)

def markdown(r):
 q=r['question'];g=r['generation'];f=q[':question/answer-fields'][0]
 lines=[f"## Generated {q[':question/difficulty'].split('/')[-1]} — {g['template']}",f"Review metadata: `{g['bank_profile']}`, `{g['parameters']}`, {g['difficulty_origin']}.",'',q[':question/problem'],'']
 for a in f[':answer-field/choices']:lines+=['- $'+a[':answer/value']+'$'+(' **correct**' if a[':answer/id']==f[':answer-field/correct'][1] else '')]
 return '\n'.join(lines+['','Worked solution:',q[':question/worked-solution'],''])
def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=1);parser.add_argument('--template',choices=list(TEMPLATES));parser.add_argument('--profile',choices=list(BANK_PROFILES));parser.add_argument('--format',choices=['markdown','json'],default='markdown');args=parser.parse_args()
 if args.count<1 or args.difficulty=='all' and (args.template or args.profile):parser.error('Positive count and specific difficulty for template/profile required')
 records=[generate(l,args.seed+i,args.template,profile=args.profile) for l in (['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]) for i in range(args.count)]
 print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
if __name__=='__main__':main()
