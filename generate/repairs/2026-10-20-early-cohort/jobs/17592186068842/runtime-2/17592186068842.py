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
import sympy as sp
KP_ID=17592186068842
KP_UUID='c0d908f1-591e-5cb6-afc5-fa7ec44ec326'
TITLE='Separating the Variables in a Differential Equation'
VERSION='separation-1'
SOURCE={'database':'math','basis':1356,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}
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
 if t=='double_factor' and not(p['b']>=2 and p['c']>=2 and p['d']>=2):raise ValueError('hard requires four substantive denominator terms')

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

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
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
 p=dict(parameters) if parameters is not None else {k:rng.randint(*( (2,4) if k in ('c','d','b') and t=='double_factor' else (2,5) if k=='base' else (1,4) if k=='n' else (1,5))) for k in TEMPLATES[t][2]}
 if parameters is None and t in ('polynomial_factor','sqrt_quotient','double_factor'):p['n']=rng.choice([2,4])
 check_parameters(t,p);rhs,solution,bank,correct,domain=build(t,p)
 if bank_profile!='observed':bank=quotient_bank(t,p,bank_profile);correct=p['n']-1
 if profile=='standard' and t=='sqrt_quotient':
  # Neither component frequency nor layout may encode the target radical.
  roots={n:r'\sqrt{'+str(p['a'])+'+'+power('y',n)+'}' for n in (2,4)}
  eq=lambda A,B:A+r'\cdot '+D+'='+B
  h=frac('1','x')
  bank=[eq(frac('1',roots[4]),h),eq('x',roots[2]),
        eq(roots[2],h),eq(roots[4],h),eq(frac('1',roots[2]),h)]
  correct=4 if p['n']==2 else 0
  bank_profile='radical-transfer'
 prompt='Separate the variables in the following differential equation: \n\n$$\n'+D+'='+rhs+'\n$$'
 if profile=='standard':
  solution=solution.replace('differentiable equation','differential equation')
  # State the local division restriction without requiring singular solutions.
  prompt+='\n\nWork on a domain where all displayed expressions are defined.'
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
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':uid('question'),':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':[field]},'generation':{'version':VERSION,'template':t,'profile':profile,'bank_profile':bank_profile,'seed':seed,'parameters':p,'domain':domain,'source':SOURCE,'source_ids':[TEMPLATES[t][1]] if TEMPLATES[t][1] else [],'origin':'observed-template' if TEMPLATES[t][1] else 'authored-missing-hard','mathematical_fingerprint':fingerprint,'content_fingerprint':identity,'plot_rating':'none'}}

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
