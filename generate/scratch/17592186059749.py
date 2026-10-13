#!/usr/bin/env python3
"""Exact 2x2 determinants; captured math basis1356. No database writes.

Observed layouts and complete banks are explicit parameterized recipes. Opaque
scalar patterns are opt-in observed replay profiles, not recovered error intent.
Default radios use four defensible determinant operations. All bank members are
computed together and the entire instance is rejected on any collision.
Hard is an authored missing-level numerical workload: four reduced noninteger
fractions; both diagonal products remain fractional, with incomparable reduced
denominators. It adds arithmetic only, never an unknown-entry equation or branch.
"""
import argparse, hashlib, json, random, re, uuid
from pathlib import Path
import sympy as s
KP_ID=17592186059749
KP_UUID='26e8a6ff-e5ed-59a7-b31d-1981495bf26a'
TITLE='Calculating the Determinant of a 2x2 Matrix With Non-Integer Entries'
VERSION='determinant-noninteger-v1'
HERE=Path(__file__).with_suffix('')
x,y,z,r,t,u,v=s.symbols('x y z r t u v',real=True)
# Template name: level, response, layout, matrix name, source IDs.
TEMPLATES={
 'numeric_radical':('easy','radio','what','A',['q-1088']),
 'symbolic_radical':('easy','radio','calculate','Z',['q-1089']),
 'linear_power':('easy','radio','bare','A',['q-1083']),
 'easy_fraction':('easy','radio','calculate','T',['q-1087']),
 'shared_monomial':('moderate','radio','calculate','C',['q-127601']),
 'factored_polynomial':('moderate','radio','calculate','D',['q-127603']),
 'radical_blank':('easy','blank','evaluate','A',['q-275595','q-317374']),
 'two_fractions':('moderate','blank','given','D',['q-317367']),
 'one_fraction':('moderate','blank','given','E',['q-317368']),
 'polynomial_blank':('moderate','blank','given','D',['q-317372']),
 'radical_power':('easy','radio','bare','A',['q-69649']),
 'factored_bilinear':('moderate','radio','calculate','H',['q-69650']),
 'four_fractions':('hard','blank','given','A',[]),
}
DEFAULTS={
 'numeric_radical':{'n':2,'b':5,'c':1,'d':3},'symbolic_radical':{'k':2},
 'linear_power':{'a':2,'d':3,'k':2},'easy_fraction':{'q':2,'b':17,'c':1,'d':10},
 'shared_monomial':{'a':1,'b':2,'q':2,'d':5},'factored_polynomial':{'a':2,'b':5},
 'radical_blank':{'n':3,'c':2},'two_fractions':{'p':2,'q':5,'b':-3,'h':-1,'j':2,'d':2},
 'one_fraction':{'p':-3,'q':4,'b':5,'c':2,'d':-1},'polynomial_blank':{'a':3,'b':2,'c':5},
 'radical_power':{'a':3,'b':2,'k':2},'factored_bilinear':{'a':-2,'b':3},
 'four_fractions':{'p':2,'q':3,'b':-3,'j':4,'c':5,'k':6,'d':-7,'l':8}}

def digest(o):return hashlib.sha256(json.dumps(o,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def ident(text):return str(uuid.uuid5(uuid.UUID(KP_UUID),text))
def tex(e):
 out=s.latex(e,order='lex').replace(' ','')
 return re.sub(r'([xyzrstu])\^\{(\d+)\}',r'{\1}^{\2}',out)
def mul(a,b):return a+r'\cdot '+('('+b+')' if b.startswith('-') else b)
def diff(a,b):return a+'-'+('('+b+')' if b.startswith('-') else b)
def add(a,b):return a+('' if b.startswith('-') else '+')+b
def matrix(e):return r'\begin{aligned}'+e[0]+' & '+e[1]+r' \\ '+e[2]+' & '+e[3]+r'\end{aligned}'
def signed(n,var):return ('' if n==1 else '-' if n==-1 else tex(n))+var

# Bounds are workload guards, applied equally to sampler and explicit parameters.
def guard(template,p):
 if set(p)!=set(DEFAULTS[template]):raise ValueError('Exact parameter keys required')
 if any(type(a)!=int for a in p.values()):raise ValueError('Integer recipe parameters required')
 if any(abs(a)>24 or a==0 for a in p.values()):raise ValueError('Nonzero bounded parameters required')
 if 'n' in p and p['n'] not in (2,3,5,6,7,10,11,13):raise ValueError('Squarefree positive nonsquare radicand required')
 if template=='symbolic_radical' and not 2<=p['k']<=5:raise ValueError('Power workload')
 if template in ('linear_power','radical_power') and not (2<=p['k']<=4 and 2<=p['a']<=6 and 2<=p.get('b',p.get('d'))<=6):raise ValueError('Easy monomial workload')
 if template=='easy_fraction' and not (2<=p['q']<=6 and 2<=p['d']<=20 and p['d']%p['q']==0 and 2<=p['b']<=24 and 1<=p['c']<=4):raise ValueError('Easy fraction must cancel to integer product')
 if template in ('one_fraction','two_fractions'):
  if not (2<=p['q']<=8 and abs(p['p'])<p['q'] and s.gcd(p['p'],p['q'])==1):raise ValueError('Reduced noninteger fraction required')
  if template=='one_fraction' and not (p['p']<0 and p['d']<0 and 1<=abs(p['d'])<=5 and 1<=p['b']<=8 and 1<=p['c']<=5 and (s.Rational(p['p'],p['q'])*p['d']).q>1):raise ValueError('One-fraction moderate workload')
  if template=='two_fractions' and not (p['p']>0 and p['b']<0 and p['h']<0 and p['d']>0 and 2<=p['j']<=8 and abs(p['h'])<p['j'] and s.gcd(p['h'],p['j'])==1 and abs(p['b'])<=8 and p['d']<=8):raise ValueError('Two-fraction signs/workload')
  if template=='two_fractions':
   aa=s.Rational(p['p']*p['d'],p['q']);bb=s.Rational(p['b']*p['h'],p['j'])
   if aa.q==1 or bb.q==1 or aa.q==bb.q:raise ValueError('Both products fractional with unlike denominators')
 if template=='shared_monomial' and not (1<=p['a']<=4 and 2<=p['b']<=8 and 2<=p['q']<=6 and p['b']%p['q']==0 and 2<=p['d']<=8 and p['a']*p['d']!=p['b']//p['q']):raise ValueError('Like-product collection with cancelling fraction required')
 if template in ('factored_polynomial','factored_bilinear','polynomial_blank'):
  if any(not 2<=abs(a)<=8 for a in p.values()):raise ValueError('Nonunit moderate coefficients')
  if template=='factored_bilinear' and not (p['a']<0<p['b']):raise ValueError('Bilinear source sign pattern')
  if template!='factored_bilinear' and any(a<0 for a in p.values()):raise ValueError('Source monomial signs')
 if template=='radical_blank' and not 1<=p['c']<=8:raise ValueError('Easy integer coefficient')
 if template=='numeric_radical' and not (1<=p['c']<=4 and 2<=p['b']<=9 and 2<=p['d']<=7):raise ValueError('Easy one radical product')
 if template=='four_fractions':
  pairs=[(p['p'],p['q']),(p['b'],p['j']),(p['c'],p['k']),(p['d'],p['l'])]
  if any(not (2<=abs(a)<=9 and 2<=b<=9 and s.gcd(a,b)==1 and abs(a)%b!=0) for a,b in pairs):raise ValueError('Four reduced noninteger fractions required')
  aa=s.Rational(p['p'],p['q'])*s.Rational(p['d'],p['l']);bb=s.Rational(p['b'],p['j'])*s.Rational(p['c'],p['k'])
  if min(aa.q,bb.q)<=1 or aa.q%bb.q==0 or bb.q%aa.q==0 or aa==bb:raise ValueError('Hard requires two fractional products and substantive common denominator')

def build(template,p):
 # Keep arithmetic stages as ordered TeX masks rather than eagerly simplifying.
 if template=='numeric_radical':E=[s.sqrt(p['n']),p['b'],p['c'],p['d']]
 elif template=='symbolic_radical':E=[s.sqrt(x),y,y**p['k'],s.sqrt(x)]
 elif template=='linear_power':E=[p['a']*x,y**p['k'],z,-p['d']]
 elif template=='easy_fraction':E=[s.Rational(1,p['q']),p['b'],p['c'],p['d']]
 elif template=='shared_monomial':E=[-p['a']*x,-p['b']*y,x/p['q'],p['d']*y]
 elif template=='factored_polynomial':E=[p['a']*x,y,-p['b'],x*y]
 elif template=='radical_blank':E=[s.sqrt(p['n']),y,p['c'],s.sqrt(p['n'])]
 elif template=='two_fractions':E=[s.Rational(p['p'],p['q']),p['b'],s.Rational(p['h'],p['j']),p['d']]
 elif template=='one_fraction':E=[s.Rational(p['p'],p['q']),p['b'],p['c'],p['d']]
 elif template=='polynomial_blank':E=[p['a']*x,p['b']*y,-p['c'],x]
 elif template=='radical_power':E=[p['a']*s.sqrt(x),z**p['k'],p['b']*y,-s.sqrt(x)]
 elif template=='factored_bilinear':E=[p['a']*r,p['b']*s.Symbol('s',real=True),p['a']*t,p['b']*u]
 else:E=[s.Rational(p['p'],p['q']),s.Rational(p['b'],p['j']),s.Rational(p['c'],p['k']),s.Rational(p['d'],p['l'])]
 E=list(map(s.sympify,E));et=list(map(tex,E));ad=s.expand(E[0]*E[3]);bc=s.expand(E[1]*E[2]);answer=s.simplify(ad-bc)
 final=(diff(tex(ad),tex(bc)) if template=='numeric_radical' else tex(answer));stages=[mul(et[0],et[3])+'-'+mul('('+et[1]+')' if et[1].startswith('-') else et[1],et[2])]
 if template=='numeric_radical':stages+=[final]
 elif template in ('easy_fraction','one_fraction','two_fractions','four_fractions'):stages+=[diff(tex(ad),tex(bc)),final]
 elif template=='shared_monomial':stages+=[add(tex(ad),tex(-bc)),final]
 elif template=='factored_polynomial':final='y('+str(p['a'])+r'{x}^{2}+'+str(p['b'])+')';stages+=[add(tex(ad),tex(-bc)),final]
 elif template=='factored_bilinear':
  aa=p['a']*p['b'];final=str(-aa)+'(st-ru)';stages+=[diff(tex(ad),tex(bc)),add(tex(ad),tex(-bc)),final]
 elif template=='radical_power':final=tex(ad)+'-'+str(p['b'])+'y'+tex(z**p['k']);stages+=[final]
 elif template=='linear_power':final=tex(ad)+'-'+tex(y**p['k'])+'z';stages+=[final]
 elif template=='symbolic_radical':final='x-'+tex(y**(p['k']+1));stages+=[final]
 elif template=='radical_blank':final=str(p['n'])+'-'+signed(p['c'],'y');stages+=[final]
 else:stages+=[final]
 return E,et,ad,bc,answer,final,stages

def parse(text):
 from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
 text=text.strip().rstrip('.').replace(r'\left','').replace(r'\right','')
 def group(pos):
  if pos>=len(text) or text[pos]!='{':raise ValueError('Expected TeX group')
  depth=1;end=pos+1
  while end<len(text) and depth:
   depth+=(text[end]=='{')-(text[end]=='}');end+=1
  if depth:raise ValueError('Unbalanced group')
  return text[pos+1:end-1],end
 out='';i=0
 while i<len(text):
  if text.startswith(r'\frac',i):
   a,j=group(i+5);b,i=group(j);out+='(('+str(parse(a))+')/('+str(parse(b))+'))'
  elif text.startswith(r'\sqrt',i):
   a,i=group(i+5);out+='sqrt('+str(parse(a))+')'
  elif text.startswith(r'\cdot',i):out+='*';i+=5
  elif text[i] in '{}':out+= '(' if text[i]=='{' else ')';i+=1
  elif text[i]=='^':out+='**';i+=1
  else:out+=text[i];i+=1
 return parse_expr(out,local_dict={a:s.Symbol(a,real=True) for a in 'xyzrstu'},transformations=standard_transformations+(implicit_multiplication_application,))

def observed_bank(template,p,ad,bc,answer,final):
 # These explicit full-bank algebraic patterns preserve observations; their
 # psychological explanations are underdetermined. Never used by default.
 if template=='numeric_radical':return [tex(p['c']),tex(s.sqrt(p['n']*p['d'])+bc),final,tex(-p['n']),tex(s.sqrt(p['n']*p['d'])-bc)]
 if template=='symbolic_radical':return ['x-2'+tex(y**p['k']),'2'+tex(s.sqrt(x))+'-'+tex(y**(p['k']+1)),final,tex(s.sqrt(x))+'-2'+tex(y**(p['k']+1)),'x-'+tex(y**p['k'])]
 if template=='linear_power':return [tex(p['d']+p['a']),tex(p['d']-p['a']),tex(-ad-bc/z),tex(-ad-bc),final]
 if template=='easy_fraction':return [tex(s.Rational(3,5)*ad),tex(s.Rational(7,5)*ad),tex(-bc),final,tex(ad+bc)]
 if template=='shared_monomial':return [tex(-ad),tex(s.Rational(3,2)*bc),final,tex(-ad/2),tex(ad)]
 if template=='factored_polynomial':
  a,b=p['a'],p['b'];return [str(a+1)+r'{y}^{2}x-'+str(b),final,str(a+1)+r'{x}^{2}y+'+str(a+1),tex(a*a*x*x*y*y),'y('+str(a)+r'{x}^{2}-'+str(a+1)+')']
 if template=='radical_power':return [final,tex(-ad)+'-'+str(p['b'])+tex(z**p['k'])+'y',tex(-p['b']*x-p['a']*y*z**p['k']),tex(ad-p['b']*y**p['k']*z),tex(p['b']*x+p['a']*y*z**p['k'])]
 if template=='factored_bilinear':
  n=-p['a']*p['b'];return [str(n)+'(ru-st)',tex(-ad)+tex(bc/2),final,tex(ad)+'+'+tex(-bc/2),str(p['b'])+'('+str(-p['a'])+'st-ru)']
 raise ValueError('No observed radio bank')

def render(template,p,et,stages):
 level,kind,layout,name,_=TEMPLATES[template];m=matrix(et)
 if layout=='what':prompt='What is $'+m.replace('aligned','vmatrix')+'$?'
 elif layout=='bare':prompt='$|'+m+'|=$'
 elif layout=='evaluate':prompt='Evaluate the determinant:\n\n$|'+m+'|=$\n'+(' ' if p['n']==3 and p['c']==2 else '')+'{{field-1}}'
 elif layout=='given':prompt='Calculate $det('+name+')$ given that\n$'+name+'=['+m+'].$\n\n$det('+name+')=$\n{{field-1}}'
 else:prompt='Calculate $det('+name+')$, if\n'+(' ' if template=='symbolic_radical' else '    ')+'$'+name+'=['+m+'].$'
 opening='For a $2\\times 2$ matrix, the determinant is given by the formula\n\n$$\n|'+matrix(['a','b','c','d'])+'|=ad-bc.\n$$\n\nUsing the formula, we have'+(':' if kind=='radio' else '')+'\n\n$$\n\\begin{aligned}'
 if layout in ('bare','evaluate'):rows=['|'+m+'| & ='+stages[0]];tail=stages[1:]
 else:rows=[r'\text{det}('+name+') & =|'+m+'|'];tail=stages
 rows+=[' & ='+a+('.' if kind=='blank' and i==len(tail)-1 else '') for i,a in enumerate(tail)]
 solution=opening+r' \\ '.join(rows)+'\\end{aligned}\n$$'
 return prompt,solution

def sample(template,rng):
 p=dict(DEFAULTS[template])
 if template=='four_fractions':
  for a,b in [('p','q'),('b','j'),('c','k'),('d','l')]:p[a]=rng.choice([-1,1])*rng.randint(2,9);p[b]=rng.randint(2,9)
 elif template=='easy_fraction':p.update(q=rng.randint(2,6),b=rng.randint(2,24),c=rng.randint(1,4));p['d']=p['q']*rng.randint(1,3)
 elif template in ('one_fraction','two_fractions'):
  p['q']=rng.randint(2,8);p['p']=rng.randint(1,p['q']-1)*(-1 if template=='one_fraction' else 1)
  p['b']=rng.randint(1,8)*(-1 if template=='two_fractions' else 1)
  if template=='one_fraction':p.update(c=rng.randint(1,5),d=-rng.randint(1,5))
  else:p.update(h=-rng.randint(1,4),j=rng.randint(2,8),d=rng.randint(1,8))
 else:
  for k in p:
   if k=='n':p[k]=rng.choice([2,3,5,6,7,10,11,13])
   elif k=='k':p[k]=rng.randint(2,4)
   elif k=='q':p[k]=rng.randint(2,6)
   elif template=='factored_bilinear':p[k]=rng.randint(2,8)*(-1 if k=='a' else 1)
   elif template=='shared_monomial':p[k]=rng.randint(1 if k=='a' else 2,4 if k=='a' else 8)
   else:p[k]=rng.randint(2,6)
 return p

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('Unknown level')
 if field_type and field_type not in ('radio','blank'):raise ValueError('Unknown field type')
 rng=random.Random(seed)
 if profile and profile.startswith('observed-'):
  sid=profile[len('observed-'):];eligible=[n for n,ss in TEMPLATES.items() if sid in ss[4]]
  if len(eligible)!=1:raise ValueError('Unknown observed profile')
  if template and template!=eligible[0]:raise ValueError('Profile/template mismatch')
  template=eligible[0]
 if template is None:
  eligible=[n for n,ss in TEMPLATES.items() if ss[0]==level and (field_type is None or ss[1]==field_type)]
  if not eligible:raise ValueError('No eligible templates')
  template=rng.choice(eligible)
 if template not in TEMPLATES:raise ValueError('Unknown template')
 spec=TEMPLATES[template]
 if spec[0]!=level or field_type and field_type!=spec[1]:raise ValueError('Level/field mismatch')
 if profile is None:profile='authored-operations' if spec[1]=='radio' else 'blank'
 if profile not in ('authored-operations','blank') and not profile.startswith('observed-'):raise ValueError('Unknown profile')
 if spec[1]=='blank' and profile!='blank':raise ValueError('Blank has no bank profile')
 if spec[1]=='radio' and profile=='blank':raise ValueError('Radio requires a complete radio bank')
 for attempt in range(2000):
  p=dict(parameters) if parameters is not None else sample(template,rng)
  try:
   guard(template,p);E,et,ad,bc,answer,final,stages=build(template,p)
   if spec[1]=='blank':values=[final]
   elif profile.startswith('observed-'):values=observed_bank(template,p,ad,bc,answer,final)
   else:values=[final,tex(ad+bc),tex(-answer),tex(ad),tex(-bc)]
   # Parse actual answer strings via SymPy LaTeX for full-bank equivalence.
   exprs=[parse(a) for a in values]
   if any(s.simplify(a-b)==0 for i,a in enumerate(exprs) for b in exprs[i+1:]):raise ValueError('Whole bank collision')
   if sum(s.simplify(a-answer)==0 for a in exprs)!=1:raise ValueError('Correct answer ambiguous/missing')
   break
  except ValueError:
   if parameters is not None:raise
 else:raise ValueError('No valid instance in bounded sampler')
 prompt,solution=render(template,p,et,stages)
 identity=digest({'version':VERSION,'prompt':prompt,'solution':solution,'kind':spec[1],'bank':sorted(values)})
 qid=ident(identity);fid=ident(qid+'/field');answers=[{':answer/id':ident(fid+'/'+a),':answer/type':':answer.type/math',':answer/value':a} for a in values]
 correct=answers[values.index(final)][':answer/id'];rng.shuffle(answers)
 field={':answer-field/id':fid,':answer-field/key':'selection' if spec[1]=='radio' else 'field-1',':answer-field/type':':answer-field.type/'+spec[1],':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]}
 fingerprint=digest([s.srepr(a) for a in E])
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':[field]},'generation':{'version':VERSION,'seed':seed,'template':template,'parameters':p,'bank_profile':profile,'source_ids':spec[4],'provenance':{'database':'math','basis':1356,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'},'domain':'real variables; x≥0 in symbolic radical templates','math_fingerprint':fingerprint,'content_hash':identity,'plot_rating':'none','authored_level':level=='hard','sympy':s.__version__}}

# Easy: one radical or cancelling fraction product, or two elementary monomials.
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
# Moderate: signed fractional products, like-term collection or GCF factoring.
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
# Hard: authored four-fraction arithmetic; both denominators need conversion.
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)
def markdown(rec):
 q=rec['question'];f=q[':question/answer-fields'][0]
 return q[':question/problem']+'\n\n'+ '\n'.join('- $'+a[':answer/value']+'$' for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');a.add_argument('--seed',type=int,default=0);a.add_argument('--count',type=int,default=1);a.add_argument('--format',choices=['markdown','json'],default='markdown');a.add_argument('--template');a.add_argument('--profile');args=a.parse_args()
 records=[generate(level,args.seed+i,template=args.template,profile=args.profile) for level in (['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]) for i in range(args.count)]
 print(json.dumps(records,indent=2) if args.format=='json' else '\n\n'.join(markdown(a) for a in records))
