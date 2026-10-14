#!/usr/bin/env python3
"""Factoring quartics with two supplied real factors: local draft, no DB writes.

Every source family retains its own complete synthetic-division/prose sequence.
Raw observed profiles are evidence-only, preserving missing keys and source errors.
Normal profiles repair the easy denominator typo and expose supported inferred fields.
API: generate(level, seed=0, template=None, field_type=None, parameters=None,
profile=None); easy/moderate/hard helpers; deterministic CLI. See sibling evidence.
"""
from __future__ import annotations
import argparse, hashlib, json, random, re, sys, uuid
from pathlib import Path
import sympy as sp
ROOT=Path(__file__).resolve().parent/'17592186054805'
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts.question_capture.math_format import normalize_prose, normalize_tex, validate_generated_record
KP_ID=17592186054805
KP_UUID='cd03f31e-360e-5cc1-9118-f71f813d572e'
TITLE='Factoring a Quartic Polynomial With Only Two Real Factors'
VERSION='quartic-two-real-v1'
SOURCE=json.loads((ROOT/'source.json').read_text())
X=sp.Symbol('x')
# r1/r2 identify the ordered synthetic-division roles, not cosmetic factor order.
ANCHORS={
 'q-75798':dict(r1=-2,r2=1,a=1,b=0,c=1),
 'q-75803':dict(r1=5,r2=1,a=3,b=2,c=1),
 'q-76184':dict(r1=-1,r2=5,a=2,b=-2,c=1),
 'q-112651':dict(r1=5,r2=5,a=1,b=0,c=9),
 'q-18852':dict(r1=3,r2=-1,a=1,b=0,c=1),
 'q-75800':dict(r1=2,r2=-1,a=2,b=-1,c=1),
 'q-270972':dict(r1=-4,r2=6,a=2,b=-3,c=8),
 'q-328607':dict(r1=-3,r2=4,a=3,b=-1,c=5),
}
ORIGINALS={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
TEMPLATES={k:{'level':('easy' if k=='q-112651' else 'hard' if k in ('q-328607','q-75803') else 'moderate'),
 'kind':('blank' if k in ('q-270972','q-328607','q-76184') else 'radio'),
 'sign':(-1 if k in ('q-328607','q-75803') else 1)} for k in ANCHORS}
BANK_PROFILES={**{'observed_'+k:{'template':k,'origin':'observed opaque evidence','raw':True} for k in ANCHORS},
 **{'method_'+k:{'template':k,'origin':'authored method-derived' if TEMPLATES[k]['kind']=='radio' else 'observed/inferred blank','raw':False} for k in ANCHORS}}
class SampleRejected(ValueError):pass

def parse(text):
 s=text.replace('−','-').replace(' ', '').replace('{','').replace('}','').replace('^','**')
 s=re.sub(r'(\d)(x)',r'\1*\2',s)
 s=re.sub(r'\)\*\*',')**',s)
 return sp.expand(sp.sympify(s,locals={'x':X}))

def poly(expr,style='brace',spaces=False):
 p=sp.Poly(sp.expand(expr),X);terms=[]
 for (degree,),coeff in p.terms():
  if coeff==0:continue
  sign='-' if coeff<0 else '+';v=abs(coeff)
  var=('{'+'x}' if style=='brace' else 'x')+'^{'+str(degree)+'}' if degree>1 else 'x' if degree else ''
  term=('' if v==1 and degree else str(v))+var
  terms.append((sign,term))
 if not terms:return '0'
 s=('-' if terms[0][0]=='-' else '')+terms[0][1]
 for sign,term in terms[1:]:s+=(' '+sign+' ' if spaces else sign)+term
 return s

def factor(root,spaces=False):return poly(X-root,'plain',spaces)
def synthetic(coeffs,root):
 bottom=[coeffs[0]];products=[]
 for c in coeffs[1:]:
  products.append(root*bottom[-1]);bottom.append(c+products[-1])
 return products,bottom

def table(expr,root):
 coeffs=sp.Poly(expr,X).all_coeffs();n=len(coeffs)-1
 products,bottom=synthetic(coeffs,root)
 rows=[['']+['${x}^{'+str(i)+'}$' for i in range(n,-1,-1)],['---']*(n+2),
 ['$'+str(root)+'$']+['$'+str(c)+'$' for c in coeffs],['','$↓$']+['$'+str(c)+'$' for c in products],
 ['']+['$'+str(c)+'$' for c in bottom]]
 return '\n'.join('| '+' | '.join(row)+' |' for row in rows)

def data(p,name):
 sign=TEMPLATES[name]['sign'];P=p['a']*X**2+p['b']*X+p['c'];F=sp.expand(sign*(X-p['r1'])*(X-p['r2'])*P)
 Q1,rem1=sp.div(F,X-p['r1']);Q2,rem2=sp.div(Q1,X-p['r2'])
 assert rem1==rem2==0 and sp.expand(Q2-sign*P)==0
 return P,F,Q1,Q2,p['b']**2-4*p['a']*p['c']

def solution(p,name,raw=False):
 P,F,Q1,Q2,D=data(p,name);r1,r2=p['r1'],p['r2'];a,b,c=p['a'],p['b'],p['c']
 # Missing source solutions receive the corresponding method family in normal output.
 family='q-328607' if name=='q-75803' else 'q-75800' if name=='q-75798' else name
 f,q1,q2,pt=(poly(v) for v in (F,Q1,Q2,P));l1,l2=factor(r1),factor(r2)
 repeated=family=='q-112651';hard=family=='q-328607'
 tail='  ' if hard else ''
 def block(s):return '$$\n'+s+'\n$$'
 def para(s):return s+tail+'\n\n'
 supplied='('+l1+')^{2}' if repeated else '('+l1+')$ and $('+l2+')'
 s=para('Let $f(x)='+f+'.$ We know that $'+supplied+'$ is a factor of $f(x),$ and we need to find its other factors.' if repeated else
        'Let $f(x)='+f+'.$ We know that $'+supplied+'$ are factors of $f(x),$ and we need to find its other factors.')
 s+=para('Because $('+l1+')$ is a factor of $f(x),$ we know that $('+l1+')$ divides $f(x)$ with no remainder. So, to begin factoring $f(x),$ we can divide it by $('+l1+')$ using synthetic division:')
 s+=table(F,r1)+'\n\n'+para('Therefore,')+block(r'\frac{'+f+'}{'+l1+'}='+q1+',')+'\n\n'+para('which means that')+block(f+'=('+l1+')('+q1+').')+'\n\n'
 if family=='q-18852':s+='So we obtain \n\n'+block('f(x)=('+l1+')('+q1+').\\,')+'\n\n'
 if repeated:
  opening='Now, because $('+l1+')^{2}$ is a factor of $f(x),$ $('+l1+')$ must be also a factor of the quotient $('+q1+').$'
 else:opening='Now, because $('+l2+')$ is also a factor of $f(x),$ it must be a factor of the quotient $('+q1+').$'
 s+=para(opening+' So, we divide this quotient by $('+l2+')$ using synthetic division once more:')
 s+=table(Q1,r2)+'\n\n'+para('Therefore,')
 divisor=factor(r2-3) if raw and family=='q-112651' else l2
 s+=block(r'\frac{'+q1+'}{'+divisor+'}='+q2+',')+'\n\n'+para('which means that')
 product=('('+l1+')^{2}' if repeated else '('+l2+')('+l1+')' if family=='q-76184' else '('+l1+')('+l2+')')
 if hard:
  equality=r'\begin{aligned}'+f+' & ='+product+'('+q2+r') \\  & =-'+product+'('+pt+r').\end{aligned}'
 elif family=='q-270972':equality=r'\begin{aligned}'+f+' & ='+product+'('+pt+r')\end{aligned}'
 else:equality=f+'='+product+'('+pt+').'
 s+=block(equality)+'\n\n'+para('To see whether the quadratic polynomial $'+pt+'$ can be factored any further, we calculate its discriminant:')
 bterm=('('+str(b)+')' if b<0 else '{'+str(b)+'}')
 disc=r'{b}^{2}-4ac='+bterm+r'^{2}-4('+str(a)+')('+str(c)+')='+str(D)+'<0'+('.' if hard else '')
 s+=block(disc)+'\n\n'+para('So, the quadratic polynomial $'+pt+'$ cannot be factored over the real numbers since its discriminant is negative. ' if not hard else 'So, the quadratic polynomial $'+pt+'$ cannot be factored over the real numbers since its discriminant is negative.')
 fn='p' if raw and family=='q-18852' else 'f'
 s+=para('Therefore, the full factorization of $'+fn+'(x)$ over the real numbers is given by ' if not hard else 'Therefore, the full factorization of $'+fn+'(x)$ over the real numbers is given by')
 marked='{{('+pt+')}_{⏟}}_{P(x)}' if raw else r'\underbrace{('+pt+')}_{P(x)}'
 s+=block(f+'='+('-' if TEMPLATES[name]['sign']==-1 else '')+product+marked+'.')+'\n\nFinally, $P(x)='+pt+'.$'
 return s

def prompt(p,name):
 P,F,*_=data(p,name)
 spaced=name in ('q-75798','q-75803');style='plain' if spaced else 'brace'
 f=poly(F,style,spaced)
 if name=='q-112651':factors='('+factor(p['r1'])+')^{2}'
 else:
  # q75800's supplied factors are reversed relative to its first division.
  order=(p['r2'],p['r1']) if name in ('q-75800','q-76184') else (p['r1'],p['r2'])
  factors=''.join('('+factor(r,spaced)+')' for r in order)
 prefix='- ' if name=='q-75803' else '-' if TEMPLATES[name]['sign']==-1 else ''
 equation=f+(' = ' if spaced else '=')+prefix+factors+'P(x)'
 if spaced:return 'Find the polynomial $P(x)$ given that\n\n$'+equation+'$.'
 if name in ('q-270972','q-328607'):return 'Find the polynomial $P(x)$ given that $'+equation+'.$\n\n$P(x)=$\n{{field-1}}'
 return 'Find the polynomial $P(x)$ given that \n\n$$\n'+equation+'.\n$$'

def observed_bank(p,name):
 """Opaque historical coefficient recipes; reproduce all choices without claiming intent."""
 source=ORIGINALS[name];anchor=ANCHORS[name];a,b,c=p['a'],p['b'],p['c'];values=[]
 for choice in source.get(':question/answer-fields',[{}])[0].get(':answer-field/choices',[]):
  text=choice[':answer/value'];expr=parse(text)
  if text.startswith('('):
   value=a*(X+c)**2;render='('+poly(X+c,'plain',True)+')^{2}' if a==1 else str(a)+'('+poly(X+c,'plain',True)+')^{2}'
   recipe='a*(x+c)^2 (opaque observed square shape)'
  else:
   coeff=sp.Poly(expr,X);da=sp.Rational(coeff.coeff_monomial(X**2),anchor['a']);db=sp.Rational(coeff.coeff_monomial(X)-anchor['b'],anchor['a']);dc=sp.Rational(coeff.coeff_monomial(1),anchor['c'])
   value=da*a*X**2+(b+db*a)*X+dc*c
   render=poly(value,'brace' if '{x}' in text else 'plain',' + ' in text or ' - ' in text)
   recipe=f'({da})a*x^2+(b+({db})a)*x+({dc})c; opaque coefficient-role preservation'
  values.append((value,render,recipe))
 return values

def method_bank(p,name):
 """Complete five-option bank from specific synthetic-division arithmetic mistakes.

Correct; reverse sign of first multiplier for quadratic x coefficient;
omit the second multiplier for the quadratic x coefficient;
reverse the first multiplier's constant contribution; reverse final constant sign.
"""
 P,F,Q1,Q2,D=data(p,name);a,b,c=p['a'],p['b'],p['c'];r1,r2=p['r1'],p['r2']
 values=[(P,'correct'),(P-2*r1*a*X,'reverse_first_multiplier_in_quadratic_x_coefficient'),
 (P-r2*a*X,'omit_second_multiplier_in_quadratic_x_coefficient'),
 (P-2*r1*(b-r2*a),'reverse_first_multiplier_in_constant_contribution'),
 (a*X**2+b*X-c,'reverse_final_constant_sign')]
 return [(v,poly(v),recipe) for v,recipe in values]

def validate_parameters(level,p,name,raw=False):
 if set(p)!=set(ANCHORS[name]):raise ValueError('Parameters must be exactly r1,r2,a,b,c')
 if any(type(v)!=int for v in p.values()):raise ValueError('Integer coefficients and supplied integer roots required')
 r1,r2,a,b,c=(p[k] for k in ('r1','r2','a','b','c'))
 if not(1<=abs(r1)<=6 and 1<=abs(r2)<=6 and 1<=a<=3 and abs(b)<=4 and 1<=c<=9):raise ValueError('Outside source-grounded integer workload bounds')
 if b*b>=4*a*c:raise ValueError('Remaining quadratic must have negative discriminant')
 if level=='easy' and not(r1==r2 and a==1 and b==0):raise ValueError('Easy preserves repeated factor, monic even quadratic')
 if level!='easy' and r1==r2:raise ValueError('Moderate/hard require distinct roots')
 if not raw and level=='moderate' and TEMPLATES[name]['sign']!=1:raise ValueError('Moderate requires positive outside sign')
 if not raw and level=='hard' and TEMPLATES[name]['sign']!=-1:raise ValueError('Hard retains outside minus extraction')

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if profile:
  if profile not in BANK_PROFILES:raise ValueError('Unknown profile')
  matched=BANK_PROFILES[profile]['template']
  if template and template!=matched:raise ValueError('Profile/template mismatch')
  template=matched
 eligible=[k for k,v in TEMPLATES.items() if v['level']==level and (field_type is None or field_type==v['kind'])]
 if not eligible or template and template not in eligible:raise ValueError('Ineligible level/template/field combination')
 rng=random.Random(seed);name=template or rng.choice(eligible);spec=TEMPLATES[name]
 profile=profile or 'method_'+name;raw=BANK_PROFILES[profile]['raw']
 for _ in range(300):
  if parameters is None:
   if level=='easy':r=rng.choice([i for i in range(-6,7) if i]);p=dict(r1=r,r2=r,a=1,b=0,c=rng.randint(1,9))
   else:p=dict(r1=rng.choice([i for i in range(-6,7) if i]),r2=rng.choice([i for i in range(-6,7) if i]),a=rng.randint(1,3),b=rng.randint(-4,4),c=rng.randint(1,9))
  else:p=dict(parameters)
  try:
   validate_parameters(level,p,name,raw);P,F,Q1,Q2,D=data(p,name)
   bank=observed_bank(p,name) if raw else method_bank(p,name) if spec['kind']=='radio' else [(P,poly(P),'correct')]
   if bank and len({sp.srepr(sp.expand(v)) for v,_,_ in bank})!=len(bank):raise SampleRejected('Whole bank has equivalent choices')
   if bank and sum(sp.expand(v-P)==0 for v,_,_ in bank)!=1:raise SampleRejected('Whole bank lacks exactly one correct value')
   break
  except ValueError:
   if parameters is not None:raise
 else:raise SampleRejected('Bounded sampler exhausted')
 source=ORIGINALS[name];q={':question/problem':prompt(p,name)}
 if not raw or ':question/worked-solution' in source:q[':question/worked-solution']=solution(p,name,raw)
 if not raw or ':question/difficulty' in source:q[':question/difficulty']=':question.difficulty/'+level
 if not raw and name=='q-76184':q[':question/problem']+='\n\n$P(x)=$\n{{field-1}}'
 if not raw:
  q[':question/problem']=normalize_prose(q[':question/problem']);q[':question/worked-solution']=normalize_prose(q[':question/worked-solution'])
  bank=[(v,normalize_tex(t),r) for v,t,r in bank]
 # Identity includes all displayed stages and full bank, but not seed/order.
 mathematical={'polynomial':sp.srepr(F),'supplied':sorted([p['r1'],p['r2']]),'sign':spec['sign'],'demand':'quadratic_fragment'}
 ph=hashlib.sha256(json.dumps(mathematical,sort_keys=True).encode()).hexdigest()
 content={'version':VERSION,'level':q.get(':question/difficulty'),'prompt':q[':question/problem'],'solution':q.get(':question/worked-solution'),'bank':sorted(t for _,t,_ in bank),'field_presence':not raw or ':question/answer-fields' in source,'correct_presence':not raw or bool(source.get(':question/answer-fields',[{}])[0].get(':answer-field/correct'))}
 ch=hashlib.sha256(json.dumps(content,sort_keys=True).encode()).hexdigest()
 qid=uuid.uuid5(uuid.UUID(KP_UUID),ch);q[':question/id']=str(qid)
 recipes={}
 if not raw or ':question/answer-fields' in source:
  kind=spec['kind'];key='selection' if kind=='radio' else 'field-1';fid=uuid.uuid5(qid,key);answers=[];correct=None
  for value,text,recipe in bank:
   aid=str(uuid.uuid5(fid,text));answers.append({':answer/id':aid,':answer/type':':answer.type/math',':answer/value':text});recipes[aid]=recipe
   if sp.expand(value-P)==0:correct=aid
  random.Random(seed).shuffle(answers)
  field={':answer-field/id':str(fid),':answer-field/key':key,':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':answers}
  if not raw or ':answer-field/correct' in source.get(':question/answer-fields',[{}])[0]:field[':answer-field/correct']=[':answer/id',correct]
  q[':question/answer-fields']=[field]
 result={'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'python_version':sys.version.split()[0],'sympy_version':sp.__version__,'seed':seed,'template':name,'parameters':p,'bank_profile':profile,'bank_origin':BANK_PROFILES[profile]['origin'],'evidence_only':raw,'eligible_for_learning':not raw,'authored_extension':not raw,'parameter_fingerprint':ph,'content_fingerprint':ch,'source_analysis':{k:SOURCE[k] for k in ('database','basis','lineage')}|{'question_ids':[name]},'answer_math':{'fragment':str(P)},'distractor_recipes':recipes,'plot_rating':'none','plot_assets':{},'inferred_field':name=='q-76184' and not raw,'inferred_difficulty':name in ('q-75798','q-75803') and not raw}}

 return result if raw else validate_generated_record(result)

# EASY: repeated linear factor, monic even irreducible quadratic.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE: distinct supplied integer factors, two full synthetic divisions.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# HARD: retain signed intermediate quotient then extract the outside minus.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)

def markdown(record):
 q=record['question'];g=record['generation'];out=['### '+g['template']+' — '+('raw evidence' if g['evidence_only'] else 'generated '+q[':question/difficulty'].split('/')[-1]),q[':question/problem']]
 for f in q.get(':question/answer-fields',[]):
  for a in f[':answer-field/choices']:out.append('- $'+a[':answer/value']+'$'+(' **correct**' if f.get(':answer-field/correct',[None,None])[1]==a[':answer/id'] else ''))
 if ':question/worked-solution' in q:out+=['**Worked solution**',q[':question/worked-solution']]
 return '\n\n'.join(out)
def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=1);parser.add_argument('--format',choices=['markdown','json'],default='markdown');parser.add_argument('--template',choices=list(TEMPLATES));parser.add_argument('--profile',choices=list(BANK_PROFILES));parser.add_argument('--field-type',choices=['radio','blank']);args=parser.parse_args()
 if args.count<1:parser.error('Count must be positive')
 levels=['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]
 records=[generate(l,args.seed+i,args.template,args.field_type,profile=args.profile) for l in levels for i in range(args.count)]
 print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
if __name__=='__main__':main()
