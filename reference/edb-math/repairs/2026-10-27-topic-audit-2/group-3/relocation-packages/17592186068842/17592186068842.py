#!/usr/bin/env python3
"""Separate variables only; math basis 1356. No integration or database writes.

Ten observed radio templates/banks; six easy and four moderate. Hard is an
explicitly authored two-factor rearrangement at the same local separation step.
Observed banks deliberately include equivalent UNSEPARATED equations: eligibility
requires A(y)dy/dx=B(x), as the lesson defines. Compare complete equations modulo
nonzero scaling only AFTER checking that response criterion. No plots.

Profiles: observed (source wording/banks); standard (typo/domain repair,
authored quotient banks that remove the unique-fractionless-choice cue).
Parameter bounds apply identically to explicit inputs and sampled inputs. Source
replay uses these same parameterized formula/stage recipes, never copied records.
"""
from __future__ import annotations
import argparse, hashlib, json, random, uuid
from pathlib import Path
import sys
sys.dont_write_bytecode=True
from math_format import normalize_prose,normalize_tex
import sympy as sp
KP_ID=17592186068842
KP_UUID='c0d908f1-591e-5cb6-afc5-fa7ec44ec326'
TITLE='Separating the Variables in a Differential Equation'
VERSION='separation-3'
SOURCE={'database':'math','basis':7370,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}
D=r'\frac{\text{d}y}{\text{d}x}'
INTRO='A differentiable equation is *separable* if it can be written in the form\n\n$$\n'+D+'=h(x)g(y).\n$$\n\nIf an equation is separable, we say that the variables are *separated* when it is written in the form\n\n$$\n'+r'\frac{1}{g(y)}\cdot '+D+'=h(x).\n$$\n\nNotice that our differentiable equation is separable since it can be written as\n\n$$\n'
TEMPLATES={
 'rational_product':('easy','q-154678',{'n':2,'a':1}),
 'exp_sum':('moderate','q-157692',{'a':1,'b':1}),
 'exp_product':('easy','q-158022',{'a':1}),
 'polynomial_factor':('moderate','q-158023',{'a':1,'b':1,'n':2}),
 'base_exp':('moderate','q-158024',{'base':3,'a':1,'b':2}),
 'exp_quotient':('easy','q-158025',{'base':2,'a':1,'n':3}),
 'sqrt_quotient':('easy','q-158026',{'a':1,'n':2}),
 'trig_product':('easy','q-158027',{'a':1,'n':2}),
 'simple_quotient':('easy','q-158030',{'n':1}),
 'rational_factor':('moderate','q-158032',{'a':3,'b':5,'c':1}),
 'double_factor':('hard',None,{'a':2,'b':3,'c':2,'d':3,'n':2})}

def frac(a,b):return r'\frac{'+a+'}{'+b+'}'
def power(a,n):return a if n==1 else '{'+a+'}^{'+str(n)+'}'
def term(a,v):return v if a==1 else str(a)+v

def build(t,p):
 """Complete mathematical component masks; punctuation/row order stays source-specific."""
 n=p.get('n',1); yn=power('y',n); a=p.get('a',1); ax=term(a,'x')
 F=frac; eq=lambda A,B:A+r'\cdot '+D+'='+B
 if t=='rational_product':
  den='x+'+str(a);h=F('x',den);g=yn;rhs=F('x'+yn,den);factor='('+h+r')\cdot '+g+'.'
  vals=[eq(F('1','x'),F(yn,den)),eq(yn,h),eq(F('1',yn),h),eq(F(den,'x'),yn),eq('('+den+')','x'+yn)];correct=2;domain='y≠0; x≠-'+str(a)
 elif t=='exp_product':
  h=power('e',ax);g='y';rhs=g+h;factor=h+r'\cdot y.'
  vals=[eq('y',h),eq(F(power('e','-'+ax),'y'),'1'),eq(power('e','-'+ax),'y'),eq(h,'y'),eq(F('1','y'),h)];correct=4;domain='y≠0'
 elif t=='exp_sum':
  by=term(p['b'],'y');h=power('e',ax);g=power('e',by);rhs=power('e',ax+'+'+by);factor=h+r'\cdot '+g
  vals=[eq(h,g),eq(g,h),eq(power('e','-'+ax),power('e','-'+by)),eq(power('e','-'+by),h),eq(power('e','-'+ax),g)];correct=3;domain='all real x,y'
 elif t=='polynomial_factor':
  ay=term(p['b'],yn);gs=str(a)+'+'+ay;h='x';g='('+gs+')';rhs=term(a,'x')+'+'+term(p['b'],'x')+yn;factor='x'+r'\cdot '+g+'.'
  vals=[eq(g,h),eq(F('1',gs),h),eq(F('x',gs),'1'),eq(F('1',rhs),'1'),eq('('+rhs+')','1')];correct=1;domain='all real x,y' # positive constant + positive even power
 elif t=='base_exp':
  base=str(p['base']);by=term(p['b'],'y');h=power(base,ax);g=power(base,'-'+by);rhs=power(base,ax+'-'+by);factor=h+r'\cdot '+g
  vals=[eq(h,g),eq(g,h),eq(power(base,by+'-'+ax),'1'),eq(power(base,'-'+ax),g),eq(power(base,by),h)];correct=4;domain='all real x,y'
 elif t=='exp_quotient':
  base=str(p['base']);h=power(base,ax);g=F('1',yn);rhs=F(h,yn);factor=h+r'\cdot '+g+'.'
  vals=[eq(yn,h),eq(h,g),eq(g,h),eq(F(yn,h),'1'),eq(power(base,'-'+ax),g)];correct=0;domain='y≠0'
 elif t=='sqrt_quotient':
  gs=r'\sqrt{'+str(a)+'+'+yn+'}';h=F('1','x');g=gs;rhs=F(gs,'x');factor=h+r'\cdot '+g+'.'
  vals=[eq(F('x',gs),'1'),eq('x',gs),eq(gs,h),eq(h,gs),eq(F('1',gs),h)];correct=4;domain='x≠0'
 elif t=='trig_product':
  h=r'\operatorname{sin}⁡'+ax;ci=r'\operatorname{csc}⁡'+ax;g=yn;rhs=yn+h;factor=h+r'\cdot '+g+'.'
  vals=[eq(h,yn),eq(ci+r'\text{ }',yn),eq(yn,F('1',h)),eq(F(ci,yn),'1'),eq(F('1',yn),h)];correct=4;domain='y≠0; raw distractors containing csc additionally require sin('+ax+')≠0'
 elif t=='simple_quotient':
  h='x';g=F('1',yn);rhs=F('x',yn);factor='x'+r'\cdot '+g+'.'
  vals=[eq(yn,'x'),eq('x',g),eq(F(yn,'x'),'1'),eq(g,'x'),eq(F('1','x'),g)];correct=0;domain='y≠0'
 elif t=='rational_factor':
  den=term(p['b'],'x')+'+'+str(p['c']);num=ax;h=F(num,den);g=F('1','y');rhs=F(num,term(p['b'],'xy')+'+'+term(p['c'],'y'))
  factor=r'\begin{aligned}'+D+' & ='+F(num,'('+den+')y')+r' \\  & ='+h+r'\cdot '+g+r'.\end{aligned}'
  vals=[eq(g,h),eq(F(den,num),g),eq(F(term(p['b'],'xy')+'+'+term(p['c'],'y'),num),'1'),eq('y',F(den,num)),eq('y',h)];correct=4;domain='y≠0; '+den+'≠0'
 elif t=='double_factor':
  xd=term(p['b'],'x')+'+'+str(p['c']);yg=str(p['d'])+'+'+yn;h=F(ax,xd);g=F('1',yg)
  den=term(p['b']*p['d'],'x')+'+'+term(p['b'],'x')+yn+'+'+str(p['c']*p['d'])+'+'+term(p['c'],yn);rhs=F(ax,den)
  factor=r'\begin{aligned}'+D+' & ='+F(ax,'('+xd+')('+yg+')')+r' \\  & ='+h+r'\cdot '+g+r'.\end{aligned}'
  vals=[eq('('+yg+')',h),eq(g,h),eq('('+yg+')',F(xd,ax)),eq('('+xd+')',F(ax,yg)),eq(F('1',xd),F(ax,yg))];correct=0;domain=xd+'≠0'
 else:raise ValueError(t)
 sep=vals[correct]
 if t=='exp_sum':
  end=eq(F('1',g),h)+',\n$$\n\nor, equivalently,\n\n$$\n'+sep+'.'
 elif t=='base_exp':end=sep+r'\,.'
 else:end=sep
 middle=(factor if t in ('rational_factor','double_factor') else D+'='+factor)
 solution=INTRO+middle+'\n$$\n\nTherefore, we separate the variables as follows:\n\n$$\n'+end+'\n$$'
 return rhs,solution,vals,correct,domain

def check_parameters(t,p):
 expected=TEMPLATES[t][2]
 if set(p)!=set(expected):raise ValueError('exact parameter keys required: '+str(list(expected)))
 if any(type(v)!=int for v in p.values()):raise ValueError('integer parameters required')
 for k,v in p.items():
  lo,hi={'n':(1,4),'base':(2,5),'a':(1,5),'b':(1,5),'c':(1,5),'d':(1,5)}[k]
  if not lo<=v<=hi:raise ValueError('parameter outside authored bounds')
 if t in ('polynomial_factor','sqrt_quotient','double_factor') and p['n'] not in (2,4):raise ValueError('positive even power required')

def quotient_bank(t,p,bank_profile):
 """Same visible bank for every supported target power; only the key changes.

 All four separated rows are eligible targets. Never use the correct power to
 construct distractors: that leaks the target through component multiplicities.
 Observed replay always uses build's original bank.
 """
 h=power(str(p['base']),term(p['a'],'x')) if t=='exp_quotient' else 'x'
 eq=lambda A,B:A+r'\cdot '+D+'='+B
 bank=[eq(power('y',n),h) for n in range(1,5)]
 if bank_profile=='quotient-power-ladder-exchange':
  bank.append(eq(h,'y'))
 elif bank_profile=='quotient-power-ladder-independent':
  bank.append(eq('x',h))
 else:raise ValueError('unknown quotient bank')
 return bank


def practice(t,p,direction,rng):
 """Two-by-two error bank: neither component multiplicity identifies the key.

 The adjacent exponent/constant is a misread factor, while inversion tests the
 reciprocal transfer. The complete rectangle makes both components of the key
 occur exactly twice, like the other three corners. Its fifth row inverts both.
 """
 rhs,solution,old,ci,domain=build(t,p)
 A,B=old[ci].split(r'\cdot '+D+'=')
 n=p.get('n',1); a=p.get('a',1); yn=power('y',n)
 near=lambda v: rng.choice([w for w in (v-1,v+1) if w>=1])
 eq=lambda u,v:u+r'\cdot '+D+'='+v
 # A second plausible value of the y factor, kept in the same visual form.
 pp=dict(p)
 if 'n' in pp:
  pp['n']= (4 if n==2 else 2) if t in ('sqrt_quotient','polynomial_factor','double_factor') else near(n)
 elif t in ('exp_sum','base_exp'):pp['b']=near(pp['b'])
 elif t=='rational_factor':
  # Missing a power on the dependent variable in the denominator.
  pass
 _,_,other,oi,_=build(t,pp)
 A1=other[oi].split(r'\cdot '+D+'=')[0]
 if A1==A:A1=power('y',2) if A=='y' else frac('1',power('y',2))
 # An x-factor error: misread a coefficient, exponent or denominator constant.
 if t in ('rational_product','rational_factor','double_factor'):
  alt=dict(p); k='a' if t=='rational_product' else 'c';alt[k]=near(alt[k])
  _,_,v,ix,_=build(t,alt);B1=v[ix].split(r'\cdot '+D+'=')[1]
 elif t in ('exp_product','exp_sum','base_exp','exp_quotient','trig_product'):
  alt=dict(p);alt['a']=near(a);_,_,v,ix,_=build(t,alt);B1=v[ix].split(r'\cdot '+D+'=')[1]
 else:B1=frac('1',power('x',2)) if t=='sqrt_quotient' else power('x',2)
 inv=lambda v: frac('1',v)
 if direction==-1:
  if t=='rational_product':rhs=frac('x','(x+'+str(a)+')'+yn)
  elif t in ('exp_product','exp_quotient'):rhs=frac(B,'y') if t=='exp_product' else B+yn
  elif t=='sqrt_quotient':rhs=frac('1','x'+r'\cdot \sqrt{'+str(a)+'+'+yn+'}')
  elif t=='trig_product':rhs=frac(B,yn)
  elif t=='simple_quotient':rhs='x'+yn
  elif t in ('exp_sum','base_exp'):
   base='e' if t=='exp_sum' else str(p['base']);sign='-' if t=='exp_sum' else '+'
   rhs=power(base,term(a,'x')+sign+term(p['b'],'y'))
  elif t=='double_factor':
   xd=term(p['b'],'x')+'+'+str(p['c']);yg=str(p['d'])+'+'+yn
   den=term(p['b']*p['d'],'x')+'+'+term(p['b'],'x')+yn+'+'+str(p['c']*p['d'])+'+'+term(p['c'],yn)
   rhs=frac(den,term(a,'x'));B=frac(xd,term(a,'x'));B1=frac(term(p['b'],'x')+'+'+str(alt['c']),term(a,'x'))
  else:raise ValueError('direction is fixed for this factoring exercise')
  # Simplify reciprocal transfers explicitly rather than leave nested fractions.
  if t in ('rational_product','trig_product'):A=yn;A1=power('y',pp['n'])
  elif t=='exp_product':A='y';A1=power('y',2)
  elif t in ('exp_quotient','simple_quotient'):A=frac('1',yn);A1=frac('1',power('y',pp['n']))
  elif t=='sqrt_quotient':A=r'\sqrt{'+str(a)+'+'+yn+'}';A1=r'\sqrt{'+str(a)+'+'+power('y',pp['n'])+'}'
  elif t in ('exp_sum','base_exp'):
   base='e' if t=='exp_sum' else str(p['base']);sign='' if t=='exp_sum' else '-'
   A=power(base,sign+term(p['b'],'y'));A1=power(base,sign+term(pp['b'],'y'))
  elif t=='double_factor':A=frac('1',yg);A1=frac('1',str(p['d'])+'+'+power('y',pp['n']))
  product=B+r'\cdot '+inv(A)
  if t=='double_factor':
   grouping=term(p['b'],'x')+'('+yg+')+'+str(p['c'])+'('+yg+')'
   product=B+r'\cdot ('+yg+')'
   stage=r'\begin{aligned}'+D+' & ='+rhs+r' \\ & ='+frac(grouping,term(a,'x'))+r' \\ & ='+frac('('+xd+')('+yg+')',term(a,'x'))+r' \\ & ='+product+r'.\end{aligned}'
  else:stage=product
  shown=stage if t=='double_factor' else D+'='+rhs+'='+stage+'.'
  solution='Expose the independent-variable and dependent-variable factors:\n\n$$\n'+shown+'\n$$\n\nMultiply both sides by the reciprocal of the dependent-variable factor. On the stated domain, this gives\n\n$$\n'+eq(A,B)+'.\n$$\n\nThe derivative multiplier depends only on $y$ and the right-hand side only on $x$.'
 # All five choices have separated variables. Checking format cannot select one.
 last=eq(inv(A),inv(B))
 if t=='double_factor':
  xd=term(p['b'],'x')+'+'+str(p['c']);yg=str(p['d'])+'+'+yn
  last=eq('('+yg+')',frac(term(a,'x'),xd)) if direction==-1 else eq(frac('1',yg),frac(xd,term(a,'x')))
 bank=[eq(A,B),eq(A1,B),eq(A,B1),eq(A1,B1),last]
 return rhs,solution,bank,0,domain

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None,direction=None):
 if level not in ('easy','moderate','hard'):raise ValueError('unknown difficulty')
 if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('radio only')
 rng=random.Random(seed);eligible=[t for t,s in TEMPLATES.items() if s[0]==level]
 t=template or rng.choice(eligible)
 if t not in eligible:raise ValueError('template difficulty mismatch')
 profile=profile or 'standard'
 if profile not in ('standard','observed'):raise ValueError('unknown profile')
 if profile=='observed' and TEMPLATES[t][1] is None:raise ValueError('hard has no observed bank')
 bank_profile=(rng.choice(['quotient-power-ladder-exchange','quotient-power-ladder-independent'])
               if profile=='standard' and t in ('exp_quotient','simple_quotient') else 'observed')
 p=dict(parameters) if parameters is not None else {k:rng.randint(*( (2,5) if k=='base' else (1,4) if k=='n' else (1,5))) for k in TEMPLATES[t][2]}
 if parameters is None and t in ('polynomial_factor','sqrt_quotient','double_factor'):p['n']=rng.choice([2,4])
 check_parameters(t,p);rhs,solution,bank,correct,domain=build(t,p)
 chosen_direction=1
 if profile=='standard':
  chosen_direction=direction if direction is not None else (1 if t in ('polynomial_factor','rational_factor') else rng.choice([-1,1]))
  if chosen_direction not in (-1,1):raise ValueError('direction must be -1 or 1')
  rhs,solution,bank,correct,domain=practice(t,p,chosen_direction,rng)
  bank_profile='factor-rectangle'
  domain='Open real domain where every displayed expression is defined and the dependent-variable factor is nonzero.'

 if profile=='observed' and bank_profile!='observed':bank=quotient_bank(t,p,bank_profile);correct=p['n']-1
 prompt='Separate the variables in the following differential equation: \n\n$$\n'+D+'='+rhs+'\n$$'
 if profile=='standard':
  solution=solution.replace('differentiable equation','differential equation')
  # State the local division restriction without requiring singular solutions.
  prompt+='\n\nWork on an open domain where all displayed expressions are defined and the dependent-variable factor is nonzero. Choose an equivalent equation in the form $A(y)\\, '+D+'=B(x)$, with a multiplier depending only on $y$ and a right-hand side depending only on $x$.'
 if profile!='observed':
  prompt=normalize_prose(prompt);solution=normalize_prose(solution);bank=[normalize_tex(v)for v in bank]
 # Semantic response validity/deduplication from the ACTUAL rendered values.
 from importlib.util import spec_from_file_location,module_from_spec
 spec=spec_from_file_location('separation_math',Path(__file__).with_suffix('')/'math_check.py');m=module_from_spec(spec);spec.loader.exec_module(m)
 m.validate_bank(prompt,solution,bank,correct)
 fingerprint=hashlib.sha256(m.fingerprint(prompt).encode()).hexdigest()
 identity=hashlib.sha256(json.dumps([VERSION,prompt,solution,sorted(bank)],ensure_ascii=False).encode()).hexdigest()
 uid=lambda name:str(uuid.uuid5(uuid.NAMESPACE_URL,'KP68842/'+identity+'/'+name))
 answers=[{':answer/id':uid('answer/'+v),':answer/type':':answer.type/math',':answer/value':v} for v in bank]
 correct_id=answers[correct][':answer/id'];rng.shuffle(answers)
 field={':answer-field/id':uid('selection'),':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct_id]}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':uid('question'),':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':[field]},'generation':{'direction':chosen_direction,'version':VERSION,'template':t,'profile':profile,'bank_profile':bank_profile,'seed':seed,'parameters':p,'domain':domain,'source':SOURCE,'source_ids':[TEMPLATES[t][1]] if TEMPLATES[t][1] else [],'origin':'observed-template' if TEMPLATES[t][1] else 'authored-missing-hard','mathematical_fingerprint':fingerprint,'content_fingerprint':identity,'plot_rating':'none'}}

# EASY: explicit product or quotient; one reciprocal transfer, no hidden factoring.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE: one exponent law or one common-factor extraction, then separation.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# HARD (authored): recover two independent factors from four denominator terms.
# It still ends at separation; no integration/general solution/IVP branch.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)
def markdown(r):
 q=r['question'];f=q[':question/answer-fields'][0]
 return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$' for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
def main():
 a=argparse.ArgumentParser();a.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');a.add_argument('--seed',type=int,default=0);a.add_argument('--count',type=int,default=1);a.add_argument('--format',choices=['markdown','json'],default='markdown');a.add_argument('--template');a.add_argument('--profile');v=a.parse_args()
 records=[generate(l,v.seed+i,v.template,profile=v.profile) for l in (['easy','moderate','hard'] if v.difficulty=='all' else [v.difficulty]) for i in range(v.count)]
 print(json.dumps(records,indent=2,ensure_ascii=False) if v.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
if __name__=='__main__':main()
