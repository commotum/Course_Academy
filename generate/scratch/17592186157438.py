#!/usr/bin/env python3
"""Rearrange a common-positive-exponential equation, then factor its quadratic.

Read-only snapshot: math basis 1356, lineage 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1.
This generator stops at guide step 7. No database writes or plot dependencies.
Whole mathematical components fill source prose/layout masks in layouts.json;
there is no literal-source replay branch. Observed scalar bank formula shapes
have limited interpretation and are available only through explicit profiles.
Default radio banks are authored operations. Missing source fields/correct refs
are mathematically repaired and never counted as matched original designations.
Hard is authored: collect repeated quadratic/linear terms across both sides,
then factor a bounded nonmonic quadratic into two linear factors. No logarithms,
exponent solving, hyperbolic notation, higher-degree polynomial, or branch added.
"""
from __future__ import annotations
import argparse, hashlib, json, math, random, re, uuid
from pathlib import Path
import sympy as sp

KP_ID=17592186157438
KP_UUID='8aaf12cf-8596-5960-bc68-5ca3eb5fab0f'
TITLE='Solving an Exponential Equation by Rearranging the Equation and Then Factoring'
VERSION='rearrange-exponential-1'
EVIDENCE=Path(__file__).with_suffix('')
X=sp.Symbol('x', real=True)
SOURCE={'database':'math','basis':1356,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}
# Separate layouts when source arithmetic stage or root notation differs.
TEMPLATES={
 'difference_integer_blank':('easy','blank','difference','q-264786'),
 'difference_rational_blank':('easy','blank','difference','q-264788'),
 'difference_unit_product':('easy','radio','difference','q-110803'),
 'difference_rational_product':('easy','radio','difference','q-88417'),
 'quadratic_right_const_linear_product':('moderate','radio','right_const_linear','q-88472'),
 'quadratic_right_linear_const_product':('moderate','radio','right_linear_const','q-100797'),
 'quadratic_left_const_negative_blank':('moderate','blank','left_const','q-264791'),
 'quadratic_left_const_positive_blank':('moderate','blank','left_const','q-264793'),
 'reverse_quadratic_product':('moderate','radio','reverse','q-88473'),
 'quadratic_left_const_product':('moderate','radio','left_const','q-88474'),
 'quadratic_unrated_blank':('moderate','blank','left_const','q-237949'),
 'collected_quadratic_blank':('hard','blank','collected',None),
 'collected_quadratic_product':('hard','radio','collected',None),
}
STYLE={
 'q-264786':{'dot':r'\cdot ','x2':r'{x}^{2}','factor':'integer_difference'},
 'q-264788':{'dot':r'\cdot ','x2':r'{x}^{2}','factor':'aligned_factors'},
 'q-110803':{'dot':'','x2':r'{x}^{2}','factor':'plain'},
 'q-88417':{'dot':'','x2':r'x^{2}','factor':'plain','bare_base':True},
 'q-88472':{'dot':'','x2':r'{x}^{2}','factor':'plain'},
 'q-100797':{'dot':r'\cdot ','x2':r'{x}^{2}','factor':'plain'},
 'q-264791':{'dot':r'\cdot ','x2':r'{x}^{2}','factor':'plain'},
 'q-264793':{'dot':r'\cdot ','x2':r'{x}^{2}','factor':'plain','second_x':True},
 'q-88473':{'dot':r'\cdot ','x2':r'{x}^{2}','factor':'plain'},
 'q-88474':{'dot':r'\cdot ','x2':r'{x}^{2}','factor':'aligned_no_amp','scalar':True},
 'q-237949':{'dot':r' \cdot ','x2':r'x^{2}','factor':'plain','bare_base':True,'spaced':True},
 None:{'dot':r'\cdot ','x2':r'{x}^{2}','factor':'plain'},
}

def tex(v):
 return sp.latex(sp.Rational(v)).replace('- \\frac','-\\frac')
def uid(text):return str(uuid.uuid5(uuid.UUID(KP_UUID),text))
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def coefficients(p):
 return p['g']*p['p']*p['r'],p['g']*(p['p']*p['s']+p['q']*p['r']),p['g']*p['q']*p['s']
def roots(p):return sorted([sp.Rational(-p['q'],p['p']),sp.Rational(-p['s'],p['r'])])
def coefficient(c, obj='', omit_one=True):
 if not obj:return str(c)
 return ('-' if c==-1 and omit_one else '' if c==1 and omit_one else str(c))+obj

def sumterms(terms,spaced=False):
 out=''
 for c,obj in terms:
  if not c:continue
  atom=coefficient(abs(c),obj,omit_one=not obj.lstrip().startswith(r'\cdot'))
  out+= ((' - ' if spaced else '-') if c<0 else (' + ' if spaced else '+') if out else '')+atom
 return out or '0'

def components(p,template):
 level,kind,family,layout=TEMPLATES[template];sty=STYLE[layout]
 A,B,C=coefficients(p);r1,r2=roots(p)
 u,v=p['u'],p['v'];base=p['base']
 if u==1:ex='x'
 elif u==-1:ex='-x'
 else:ex=str(u)+'x'
 if v:ex+=('+' if v>0 else '-')+str(abs(v))
 # The unit-product source orders its affine exponent as constant minus x.
 if layout=='q-110803' and u==-1:ex=str(v)+'-x'
 if sty.get('spaced'):ex=ex.replace('+',' + ').replace('-',' - ')
 ebase=str(base) if sty.get('bare_base') and base=='e' else '{'+str(base)+'}'
 E=ebase+'^{'+ex+'}'
 dot=sty['dot'];x2=sty['x2'];spaced=sty.get('spaced',False)
 poly=sumterms([(A,x2),(B,'x'),(C,'')])
 # Numeric constants next to numeric exponential bases need a visible product.
 def const(c):return (r'\cdot ' if not dot and base!='e' and abs(c)>1 else dot)+E
 dist=sumterms([(A,x2+dot+E),(B,'x'+dot+E),(C,const(C))])
 if family=='difference':left=[(A,x2+dot+E)];right=[(-C,const(-C))]
 elif family=='right_const_linear':left=[(A,x2+dot+E)];right=[(-C,const(-C)),(-B,'x'+dot+E)]
 elif family=='right_linear_const':left=[(A,x2+dot+E)];right=[(-B,'x'+dot+E),(-C,const(-C))]
 elif family=='left_const':left=[(A,x2+dot+E),(C,const(C))];right=[(-B,'x'+dot+E)]
 elif family=='reverse':left=[(B,'x'+dot+E)];right=[(-C,const(-C)),(-A,x2+dot+E)]
 else:
  d,l=p['split'],p['linear_split']
  left=[(A+d,x2+dot+E),(l,'x'+dot+E),(C,const(C))]
  right=[(d,x2+dot+E),(l-B,'x'+dot+E)]
 L=sumterms(left,spaced);R=sumterms(right,spaced)
 f1='('+sumterms([(p['p'],'x'),(p['q'],'')])+')'
 f2='('+sumterms([(p['r'],'x'),(p['s'],'')])+')'
 F=coefficient(p['g'],f1+f2)
 # Keep exact factor-stage structure, including unevaluated common scalar.
 if sty['factor']=='integer_difference':
  n=abs(p['q']);factor=(r'\begin{aligned}'+str(p['g'])+r'({x}^{2}-'+str(n*n)+r') & =0 \\ '+F+r' & =0,\end{aligned}')
 elif sty['factor']=='aligned_factors':factor=r'\begin{aligned}'+F+r' & =0,\end{aligned}'
 elif sty['factor']=='aligned_no_amp':factor=r'\begin{aligned}'+F+r'=0,\end{aligned}'
 else:factor=F+'=0,'
 ro=tex(r1)+(','+'x=' if sty.get('second_x') else ',')+tex(r2)
 product='('+tex(r1)+r')\cdot '+tex(r2)+'='+tex(r1*r2)
 moved=(sumterms(left+[(-c,obj) for c,obj in right])+r' & =0 \\ ') if family=='collected' else ''
 aligned=(r'\begin{aligned}'+L+' & ='+R+r' \\ '+moved+dist+r' & =0 \\ ('+poly+')'+dot+E+r' & =0\end{aligned}')
 return {'EQ':L+'='+R,'EQ_SPACED':L+' = '+R,'ALIGNED':aligned,'POLY':poly,'E':E,'FACTOR_STAGE':factor,
         'ROOTS':ro,'R1':tex(r1),'R2':tex(r2),'PRODUCT':product,'G':str(p['g'])},(A,B,C),[r1,r2]

# Authored solution for absent source worked solutions and missing-level hard.
SHARED='We can now apply the zero product property, which states that $ab=0$ if and only if $a=0$ or $b=0.$ This gives us two equations,'
def authored_solution(c,kind):
 ending=('Therefore, in ascending order, the original equation has the solutions \n\n$$\nx='+c['R1']+r'\,\text{and}\,x='+c['R2']+'.\n$$' if kind=='blank' else
 'Therefore, the original equation has the solutions $x='+c['ROOTS']+',$ and their product is $'+c['PRODUCT']+'.$')
 return ('First, we factor the equation:\n\n$$\n'+c['ALIGNED']+'\n$$\n\n'+SHARED+'\n\n$$\n'+c['POLY']+r'=0\,\text{and}\,'+c['E']+'=0.\n$$\n\nWe now solve each of these equations separately.\n\n- The equation $'+c['POLY']+'=0$ can be factored as\n\n$$\n'+c['FACTOR_STAGE']+'\n$$\n\nwhich leads to the solutions $x='+c['ROOTS']+'.$\n\n- The equation $'+c['E']+'=0$ has no solutions because $'+c['E']+'$ is positive for every real number $x.$\n\n'+ending)

def fill(mask,c):
 return re.sub(r'<<([A-Z0-9_]+)>>',lambda m:c[m[1]],mask)

# Complete observed banks, parameterized expression patterns. Their numerical
# shapes are recoverable; author intent is not, so they never become defaults.
def bank_values(profile,p,rs):
 A,B,C=coefficients(p);r1,r2=rs;t=r1*r2
 if profile=='observed:q-88417':return [t,-1/t,-1/sp.Integer(-C),1/sp.Integer(A),-C]
 if profile=='observed:q-100797':return [A*(-C),t,1/t,-1/sp.Integer(A),1/sp.Integer(C)]
 if profile=='observed:q-88473':return [sp.Integer(A),-sp.Rational(A-1,A),sp.Rational(A-C,A),t,sp.Integer(C)]
 if profile=='observed:q-88474':return [2*r2,-r2,r2/A,-sp.Integer(A)**2/r2,t]
 if profile=='observed:q-110803':return [r2-r1,r2,sp.Integer(0),t,r1-r2]
 if profile!='authored:product-errors':raise ValueError('Unknown or ineligible profile: '+str(profile))
 # Same five-operation bank: product, wrong sign, reciprocal, sum, omit A.
 return [t,-t,1/t,r1+r2,(r2-r1 if A==1 else sp.Integer(C))]

def validate_parameters(p,template):
 level,kind,family,layout=TEMPLATES[template]
 keys={'g','p','q','r','s','base','u','v'}|({'split','linear_split'} if level=='hard' else set())
 if set(p)!=keys:raise ValueError('Parameter keys must equal '+str(sorted(keys)))
 if any(type(p[k]) is not int for k in keys-{'base'}):raise ValueError('Exact integer components required')
 if p['base']!='e' and (type(p['base']) is not int or p['base'] not in range(2,11)):raise ValueError('Positive base e or integer 2..10 required')
 if not 1<=abs(p['u'])<=5 or abs(p['v'])>6:raise ValueError('Affine exponent bounds exceeded')
 if not 1<=p['g']<=6 or not 1<=p['p']<=6 or not 1<=p['r']<=6:raise ValueError('Positive factor/scalar bounds exceeded')
 bound=12 if level=='easy' else 8
 if not 1<=abs(p['q'])<=bound or not 1<=abs(p['s'])<=bound:raise ValueError('Nonzero factor constants of bounded magnitude required')
 A,B,C=coefficients(p);rs=roots(p)
 if rs[0]==rs[1]:raise ValueError('Two distinct real roots required')
 if level=='easy':
  if B!=0 or p['q']!=-p['s'] or p['p']!=p['r'] or p['q']<=0:raise ValueError('Easy requires a difference of squares')
  if layout=='q-264786' and (p['p']!=1 or p['g']<2):raise ValueError('Integer-root scalar factor stage required')
  if layout=='q-264788' and (p['g']!=1 or p['p']<2):raise ValueError('Squared nonunit leading factor required')
  if layout=='q-110803' and (p['g']!=1 or p['p']!=1 or p['u']!=-1 or p['v']<1):raise ValueError('Unit-leading reversed exponent source family required')
  if layout=='q-88417' and (p['g']!=1 or p['p']<2):raise ValueError('Square-leading product family required')
  if layout in ['q-264788','q-88417'] and math.gcd(p['p'],abs(p['q']))!=1:raise ValueError('Primitive nonunit factors preserve rational-root workload')
 elif level=='moderate':
  if not B or not C or A>6 or abs(B)>30 or abs(C)>60:raise ValueError('Moderate bounded nonzero trinomial required')
  if layout=='q-88472' and (p['g']!=1 or p['p']!=p['r'] or p['p']<2):raise ValueError('Equal leading-factor template required')
  if layout=='q-88474' and (p['p']!=1 or p['r']!=1 or p['g']<2):raise ValueError('Scalar times monic quadratic required')
  if layout not in ('q-88472','q-88474') and (p['g']!=1 or p['r']!=1 or p['p']<2):raise ValueError('One nonunit linear-factor coefficient required')
  if math.gcd(p['p'],abs(p['q']))!=1 or math.gcd(p['r'],abs(p['s']))!=1:raise ValueError('Primitive factors required; extra scalar GCF would change the moderate workload')
  if layout=='q-264791' and not (rs[1]<0):raise ValueError('Both roots negative in this observed bank family')
  if layout=='q-264793' and not (rs[0]>0):raise ValueError('Both roots positive in this observed bank family')
 else:
  if not(p['g']==1 and 2<=p['p']<=4 and 2<=p['r']<=4 and abs(p['q'])<=6 and abs(p['s'])<=6 and B and A<=16 and abs(B)<=48 and abs(C)<=36 and 1<=p['split']<=4 and 1<=p['linear_split']<=6 and p['linear_split']!=B):raise ValueError('Authored hard workload bounds exceeded')
  if math.gcd(p['p'],abs(p['q']))!=1 or math.gcd(p['r'],abs(p['s']))!=1:raise ValueError('Both hard linear factors must be primitive and nonunit')

def sample(rng,template):
 level,_,_,layout=TEMPLATES[template]
 p={'g':1,'p':rng.randint(2,6),'q':rng.randint(1,8),'r':1,'s':rng.choice([-1,1])*rng.randint(1,7),'base':rng.choice(['e',2,3,4,5,6,7,8,9,10]),'u':rng.choice([-2,-1,1,2,3]),'v':rng.randint(-6,6)}
 if level=='easy':
  p['q']=rng.randint(1,12)
  p['r']=p['p'];p['s']=-p['q']
  if layout=='q-264786':p.update(g=rng.randint(2,6),p=1,r=1)
  if layout=='q-110803':p.update(p=1,r=1,u=-1,v=rng.randint(1,6))
 elif level=='moderate':
  p['q']=rng.choice([-1,1])*rng.randint(1,7)
  if layout=='q-88472':p.update(p=2,r=2,q=rng.choice([-1,1])*rng.randint(1,7),s=rng.choice([-1,1])*rng.randint(1,7))
  if layout=='q-88474':p.update(g=rng.randint(2,5),p=1,r=1,q=rng.randint(1,6),s=-rng.randint(1,6))
  if layout=='q-264791':p.update(q=rng.randint(1,7),s=rng.randint(1,7))
  if layout=='q-264793':p.update(q=-rng.randint(1,7),s=-rng.randint(1,7))
 else:p.update(p=rng.randint(2,4),r=rng.randint(2,4),q=rng.choice([-1,1])*rng.randint(1,6),s=rng.choice([-1,1])*rng.randint(1,6),split=rng.randint(1,4),linear_split=rng.randint(1,6))
 return p

# Shared assembly. Explicit invalid input always raises; random input retries
# the complete preselected bank, never replaces an individual option.
def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('Unknown difficulty')
 rng=random.Random(seed)
 eligible=[k for k,v in TEMPLATES.items() if v[0]==level and (field_type is None or field_type==v[1])]
 if template is None:
  if not eligible:raise ValueError('Unsupported field type')
  template=rng.choice(eligible)
 if template not in eligible:raise ValueError('Template/difficulty/field mismatch')
 _,kind,_,layout=TEMPLATES[template]
 profile=profile or ('authored:product-errors' if kind=='radio' else 'blank')
 if kind=='blank' and profile!='blank':raise ValueError('Blank profile required')
 if profile.startswith('observed:') and profile!='observed:'+str(layout):raise ValueError('Profile does not belong to this template')
 if kind=='radio' and profile not in {'authored:product-errors'}|{'observed:'+s for s in ['q-88417','q-100797','q-88473','q-88474','q-110803']}:
  raise ValueError('Unsupported complete bank profile')
 for _ in range(10000):
  p=dict(parameters) if parameters is not None else sample(rng,template)
  try:
   validate_parameters(p,template)
   c,abc,rs=components(p,template)
   vals=bank_values(profile,p,rs) if kind=='radio' else rs
   if len(set(vals))!=len(vals):raise ValueError('Entire complete bank rejected for equivalent values')
   break
  except ValueError:
   if parameters is not None:raise
 else:raise ValueError('No eligible instance for complete bank')
 layouts=json.loads((EVIDENCE/'layouts.json').read_text())
 if layout:
  prompt=fill(layouts[layout]['prompt'],c)
  solution=fill(layouts[layout]['solution'],c) if layouts[layout]['solution'] else authored_solution(c,kind)
 else:
  prompt=('In **ascending order,** the solutions of the equation $'+c['EQ']+'$ are\n\n$x=$\n{{field-1}}$\\,$ and $\\,x=$\n{{field-2}}.' if kind=='blank' else 'What is the product of solutions of the equation $'+c['EQ']+'?$')
  solution=authored_solution(c,kind)
 fieldkeys=['field-1','field-2'] if kind=='blank' else ['selection']
 if layout=='q-237949' or layout=='q-264788':fieldkeys.reverse() # Original Pull layout; placeholders determine ordering.
 banks={key:([rs[0] if key=='field-1' else rs[1]] if kind=='blank' else vals) for key in fieldkeys}
 identity=digest({'version':VERSION,'prompt':prompt,'solution':solution,'banks':{k:sorted(map(str,v)) for k,v in banks.items()}})
 fields=[]
 for key in fieldkeys:
  answers=[{':answer/id':uid(identity+key+str(v)),':answer/type':':answer.type/math',':answer/value':tex(v)} for v in banks[key]]
  correct=(rs[0] if key=='field-1' else rs[1]) if kind=='blank' else rs[0]*rs[1]
  correct_id=next(a[':answer/id'] for a,v in zip(answers,banks[key]) if v==correct)
  if kind=='radio':rng.shuffle(answers)
  fields.append({':answer-field/id':uid(identity+key),':answer-field/key':key,':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct_id]})
 repairs={'q-237949':['missing values/correct designations independently derived','missing solution authored'],
          'q-88417':['missing correct designation independently derived','missing solution authored'],
          'q-88472':['fieldless source; product radio field/bank authored'],
          'q-264791':['trailing plus in source rearrangement row removed']}.get(layout,[])
 record={'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':uid(identity),':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':fields},'generation':{'version':VERSION,'seed':seed,'template':template,'profile':profile,'parameters':p,'source':SOURCE,'source_layout':layout,'source_repairs':repairs,'source_level':'unrated' if layout in ['q-237949','q-88417'] else level if layout else None,'authored_level':level=='hard' or layout in ['q-237949','q-88417'],'authored_solution':layout in ['q-237949','q-88417',None],'authored_bank':profile.startswith('authored:'),'content_sha256':identity,'mathematical_fingerprint':digest({'quadratic_monic_coefficients':[str(sp.Rational(abc[1],abc[0])),str(sp.Rational(abc[2],abc[0]))],'response':kind,'rearrangement':TEMPLATES[template][2]}),'domain':'x real; common exponential is strictly positive','sympy_version':sp.__version__}}
 return record

def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)
def markdown(record):
 q=record['question'];lines=[q[':question/problem']]
 for f in q[':question/answer-fields']:
  lines.append('\n'+f[':answer-field/key']+': '+', '.join('$'+a[':answer/value']+'$' for a in f[':answer-field/choices']))
 lines+=['\n'+q[':question/worked-solution']]
 return '\n'.join(lines)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=2);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
 levels=['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]
 records=[generate(level,args.seed+i,template=args.template,profile=args.profile) for level in levels for i in range(args.count)]
 print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
