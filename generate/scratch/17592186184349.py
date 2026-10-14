#!/usr/bin/env python3
"""Bounded substitution integrals p(v) exp(g(v)); local review only, steps 3–7.
Easy: positive quadratic derivative, including exact two-term derivative.
Moderate: signed/scaled cubic, with familiar power derivative and small ratio.
Hard: negative quartic exponent and nonunit negative multiplier.
Source profiles are complete mathematical banks. raw:<source> additionally retains
source omissions and literal masks. Explicit opaque legacy banks are evidence only;
normal legacy-family output uses a separately authored method-derived bank.
No integration by parts, logarithms, general bases, branches or definite integrals.
"""
from __future__ import annotations
import argparse, hashlib, json, random, sys, uuid
from pathlib import Path
import sympy as s
KP=17592186184349
VERSION='exp-substitution-1'
ROOT=Path(__file__).with_suffix('')
WRAPPER=json.loads((ROOT/'source.json').read_text())
SOURCE=WRAPPER['record']
QS={q[':question/math-academy-id']:q for q in SOURCE[':knowledge-point/questions']}
CONFIG={
 'quadratic_monomial':('easy','q-2382',dict(n=2,a=1,l=0,b=0,c=1,v='z')),
 'quadratic_exact':('easy','q-73662',dict(n=2,a=2,l=-1,b=0,c=1,v='x')),
 'cubic_negative':('moderate','q-73664',dict(n=3,a=-2,l=0,b=5,c=6,v='x')),
 'cubic_positive':('moderate','q-73798',dict(n=3,a=3,l=0,b=1,c=3,v='x')),
 'quartic_negative':('hard','q-113847',dict(n=4,a=-1,l=0,b=4,c=8,v='x')),
 'legacy_cubic':('moderate','q-13737',dict(n=3,a=1,l=0,b=2,c=4,v='x')),
 'legacy_quadratic':('moderate','q-73663',dict(n=2,a=-5,l=0,b=1,c=5,v='x')),
}
NAMESPACE=uuid.UUID('e803bd99-388f-5146-ab91-03fd7b658c2c')
def uid(text):return str(uuid.uuid5(NAMESPACE,text))
def tex(e):return s.latex(s.sympify(e)).replace(' ', '')
def objects(p):
 v=s.Symbol(p['v'],real=True);g=p['a']*v**p['n']+p['l']*v+p['b'];d=s.diff(g,v)
 poly=d if p['l'] else p['c']*v**(p['n']-1)
 r=s.Integer(1) if p['l'] else s.Rational(p['c'],p['a']*p['n'])
 return v,g,d,poly,r

def power(v,n):return '{'+v+'}^{'+str(n)+'}' if n!=1 else v

def mono(k,v,n):
 t=power(v,n)
 return ('' if k==1 else '-' if k==-1 else tex(k))+t

def exponent(p):
 # Preserve observed negative exponent order: constant before negative power.
 term=mono(p['a'],p['v'],p['n'])
 if p['a']<0 and not p['l']:return (str(p['b']) if p['b'] else '')+term
 if p['l']:term+=('+' if p['l']>0 else '')+mono(p['l'],p['v'],1)
 if p['b']:term+=('+' if p['b']>0 else '')+str(p['b'])
 return term

def components(p):
 v,g,d,poly,r=objects(p);G=exponent(p)
 P=('('+mono(p['a']*p['n'],p['v'],p['n']-1)+('+' if p['l']>0 else '')+str(p['l'])+')') if p['l'] else mono(p['c'],p['v'],p['n']-1)
 D=tex(d) if p['l'] else mono(p['a']*p['n'],p['v'],p['n']-1);E='{e}^{'+G+'}'
 return G,P,D,E,r

def coefficient(k):return '' if k==1 else '-' if k==-1 else tex(k)
def primitive(k,G):return coefficient(k)+'{e}^{'+G+'}+C'

def recipes(template,p,profile):
 """Compute correct first; each following full expression is a method operation.
 Historical scalar recipes have explicit pattern recovery, not inferred intent.
 """
 v,g,d,poly,r=objects(p);E=s.exp(g);a,n,c=p['a'],p['n'],p['c'];correct=r*E
 qid=CONFIG[template][1]
 if profile=='authored_method':
  return [('correct',correct),('reverse_multiplier_sign',-correct),('omit_derivative_division',c*E),('multiply_by_derivative_coefficient',a*n*E),('drop_exponent_power',r*s.exp(v))]
 banks={
 'q-2382':[('correct',correct),('use_derivative_factor',a*n*E),('omit_multiplier',E),('drop_exponent_power',r*s.exp(v)),('reverse_multiplier_sign',-correct)],
 'q-73662':[('retain_partial_derivative',a*v*E),('correct',correct),('add_power_primitive',E+a*v**2),('retain_derivative_coefficient',a*n*E),('retain_substitution',g*E)],
 'q-73664':[('omit_outside_coefficient',s.Rational(1,a*n)*E),('omit_inner_scale',s.Rational(-1,n)*E),('correct',correct),('retain_outside_coefficient',c*E),('reverse_and_omit_power_factor',s.Rational(-1,a)*E)],
 'q-73798':[('omit_outside_coefficient',s.Rational(1,a*n)*E),('apply_inner_scale_twice',s.Rational(1,a*a*n)*E),('correct',correct),('omit_multiplier',E),('multiply_by_inner_scale',a*E)],
 'q-113847':[('correct',correct),('invert_multiplier',E/r),('omit_multiplier',E),('reverse_multiplier_sign',-correct),('invert_and_reverse_multiplier',-E/r)],
 'q-13737':[('correct',correct),('opaque_reciprocal_outside',E/c),('invert_multiplier',E/r),('omit_derivative_division',c*E),('omit_outside_and_inner_scale',E/n)],
 'q-73663':[('opaque_outside_coefficient',c*E),('omit_outside_and_sign',E/abs(a*n)),('opaque_power_coefficient',n*E),('correct',correct),('omit_outside_and_power_factor',E/a)]}
 return banks[qid]

def answer_text(expr,p,prototype=None):
 v,g,d,poly,r=objects(p);G,P,D,E,_=components(p)
 # Recipe expression interpreted before rendering, never answer-literal lookup.
 k=s.simplify(expr/s.exp(g))
 if s.simplify(expr-r*s.exp(v))==0:
  k=r;G=p['v'];E='{e}^{'+G+'}'
 if v not in k.free_symbols:
  if prototype and r'\frac{{e}^' in prototype:
   sign='-' if k<0 else '';z=abs(k)
   if z.p==1:return sign+r'\frac{'+E+'}{'+str(z.q)+'}+C'
  out=primitive(k,G)
 elif s.simplify(expr-r*s.exp(v))==0:out=primitive(r,p['v'])
 elif s.simplify(expr-(s.exp(g)+p['a']*v**2))==0:out=E+'+'+mono(p['a'],p['v'],2)+'+C'
 elif s.simplify(expr-g*s.exp(g))==0:out='('+G+')'+E+'+C'
 else:out=tex(k)+E+'+C'
 if prototype and ' + C' in prototype:out=out[:-2]+' + C'
 # Unrated legacy formatting is recovered as a presentation mask.
 if prototype and 'e^{' in prototype and '{e}^' not in prototype:
  legacy_g=s.latex(g)
  if p['a']<0:legacy_g=str(p['b'])+' - '+str(abs(p['a']))+p['v']+'^{'+str(p['n'])+'}'
  out=out.replace('{e}^{'+G+'}','e^{'+legacy_g+'}')
 return out

def source_prompt(template,p):
 G,P,D,E,r=components(p);qid=CONFIG[template][1]
 if qid=='q-13737':return 'What is $'+r'\displaystyle \int'+P.replace('{x}', 'x')+'e^{'+s.latex(objects(p)[1])+'}dx$?'
 if qid=='q-73663':return 'What is $'+r'\displaystyle \int'+P+'e^{'+str(p['b'])+' - '+str(abs(p['a']))+p['v']+'^{2}}d'+p['v']+'$?'
 return '$'+r'\int '+P+E+r'\,\text{d}'+p['v']+'=$'

def solution(template,p,raw=False):
 G,P,D,E,r=components(p);v=p['v'];I=r'\int '+P+E+r'\,\text{d}'+v
 qid=CONFIG[template][1];du=r'\text{d}u';dv=r'\text{d}'+v
 # Original masks preserve distinct spacings and conditional operative stages.
 gap=' ' if qid=='q-2382' else ''
 relation=(coefficient(r)+du+'='+P+r'\,'+dv) if qid=='q-2382' or p['l'] else coefficient(r)+du+'='+P+dv
 opening="Let's introduce the new variable $u="+G+'.$ Differentiating gives'+gap+'\n\n$$\n'+r'\frac{\text{d}u}{\text{d}'+v+'}='+D+r'\,⟹\,'+relation+'.\n$$\n\nTherefore,\n\n$$\n'
 reordered=r'\int '+E+r'\cdot '+P+(r'\text{d}' if p['l'] else r'\,\text{d}')+v
 if p['l']:
  rows=[I+' & ='+reordered,r' & =\int {e}^{u}\,\text{d}u',' & ='+E+'+C']
 else:
  inside='(-'+du+')' if r==-1 else '('+tex(r)+')'+r'\,\text{d}u' if r<0 else tex(r)+r'\,\text{d}u'
  rows=[I+' & ='+reordered,r' & =\int {e}^{u}\cdot '+(r'\,' if r==-1 else '')+inside,' & ='+coefficient(r)+r'\int {e}^{u}\,\text{d}u',' & ='+coefficient(r)+(r'\cdot ' if qid=='q-2382' else '')+'{e}^{u}+C',' & ='+answer_text(r*s.exp(objects(p)[1]),p,QS[qid][':question/answer-fields'][0][':answer-field/choices'][0][':answer/value'] if qid=='q-2382' else None)+'.']
 inner=r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}'
 if raw and qid=='q-2382':inner=r'\begin{aligned}'+inner+r'\end{aligned}'
 return opening+inner+'\n$$'

def guard(template,p):
 base=CONFIG[template][2]
 if set(p)!=set(base):raise ValueError('parameters must exactly match '+str(sorted(base)))
 if p['v'] not in ('x','z','t'):raise ValueError('unsupported variable')
 for k in ('n','a','l','b','c'):
  if not isinstance(p[k],int) or isinstance(p[k],bool):raise ValueError('integer parameters required')
 if p['n']!=base['n'] or not -5<=p['b']<=5:raise ValueError('fixed familiar power / small integer shift')
 if template=='quadratic_exact':valid=1<=p['a']<=5 and 1<=abs(p['l'])<=5 and p['c']==1
 elif template=='quadratic_monomial':valid=1<=p['a']<=4 and p['l']==0 and p['c']==1
 elif template=='cubic_positive':valid=2<=p['a']<=5 and p['l']==0 and p['c']==3
 elif template=='cubic_negative':valid=-5<=p['a']<=-2 and p['l']==0 and p['c']==-3*p['a']
 elif template=='quartic_negative':valid=-3<=p['a']<=-1 and p['l']==0 and 5<=p['c']<=16 and 1<abs(s.Rational(p['c'],4*p['a']))<=4
 elif template=='legacy_cubic':valid=p['a']==1 and p['l']==0 and 2<=p['c']<=8 and p['c']!=3
 else:valid=-5<=p['a']<=-2 and p['l']==0 and 2<=p['c']<=8
 if not valid:raise ValueError('outside documented same-level workload')

def sample(template,rng):
 p=dict(CONFIG[template][2]);p['v']=rng.choice(['x','z','t']);p['b']=rng.randint(-5,5)
 if template=='quadratic_exact':p.update(a=rng.randint(1,5),l=rng.choice([-5,-4,-3,-2,-1,1,2,3,4,5]))
 elif template=='quadratic_monomial':p['a']=rng.randint(1,4)
 elif template=='cubic_positive':p['a']=rng.randint(2,5)
 elif template=='cubic_negative':p.update(a=rng.randint(-5,-2));p['c']=-3*p['a']
 elif template=='quartic_negative':p.update(a=rng.randint(-3,-1),c=rng.randint(5,16))
 elif template=='legacy_cubic':p['c']=rng.choice([2,4,5,6,7,8])
 else:p.update(a=rng.randint(-5,-2),c=rng.randint(2,8))
 return p

# Easy entrypoint: both observed quadratic families sampled normally.
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
# Moderate entrypoint: scaled/signed cubic and legacy monomial families.
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
# Hard entrypoint: negative nonunit quartic multiplier only.
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('unknown level')
 if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('source fields are radio only')
 rng=random.Random(seed)
 if template is None:template=rng.choice([t for t,c in CONFIG.items() if c[0]==level])
 if template not in CONFIG or CONFIG[template][0]!=level:raise ValueError('template/level mismatch')
 qid=CONFIG[template][1];raw=profile=='raw:'+qid
 if profile is None:profile='authored_method' if template.startswith('legacy_') else 'observed:'+qid
 if profile not in ('observed:'+qid,'raw:'+qid,'authored_method'):raise ValueError('ineligible whole bank')
 if profile=='authored_method' and not template.startswith('legacy_'):raise ValueError('authored legacy bank only')
 for attempt in range(500):
  p=dict(parameters) if parameters is not None else sample(template,rng)
  try:
   guard(template,p);bank=recipes(template,p,profile);v,g,d,poly,r=objects(p)
   # Antiderivatives compared modulo arbitrary C, including wrong/wrong pairs.
   for i,(_,e) in enumerate(bank):
    if e.has(s.zoo,s.nan,s.oo) or e.free_symbols-{v}:raise ValueError('invalid expression domain')
    for _,f in bank[:i]:
     if s.simplify(s.diff(e-f,v))==0:raise ValueError('ambiguous whole bank')
   break
  except ValueError:
   if parameters is not None:raise
 else:raise ValueError('no eligible whole instance')
 prototypes=QS[qid][':question/answer-fields'][0][':answer-field/choices']
 texts=[answer_text(e,p,prototypes[i][':answer/value'] if profile!='authored_method' else None) for i,(_,e) in enumerate(bank)]
 problem=source_prompt(template,p);sol=solution(template,p,raw)
 legacy=template.startswith('legacy_')
 payload={':question/problem':problem,':question/answer-fields':[]}
 if not(raw and legacy):payload.update({':question/difficulty':':question.difficulty/'+level,':question/worked-solution':sol})
 identity_data=[VERSION,level if ':question/difficulty' in payload else None,problem,payload.get(':question/worked-solution'),sorted(texts),not(raw and legacy)]
 identity=json.dumps(identity_data,ensure_ascii=False,sort_keys=True);qid_new=uid(identity);fid=uid(qid_new+'/selection')
 answers=[{':answer/id':uid(fid+'/'+t),':answer/type':':answer.type/math',':answer/value':t} for t in texts]
 correct_index=next(i for i,(label,e) in enumerate(bank) if label=='correct')
 f={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers}
 if not(raw and legacy):f[':answer-field/correct']=[':answer/id',answers[correct_index][':answer/id']]
 rng.shuffle(answers);payload[':question/id']=qid_new;payload[':question/answer-fields']=[f]
 canonical=s.Symbol('x',real=True)
 fingerprint=hashlib.sha256(s.srepr(poly*s.exp(g)).replace("Symbol('"+p['v']+"', real=True)","Symbol('x', real=True)").encode()).hexdigest()
 return {'knowledge_point':{'db_id':KP,'id':SOURCE[':knowledge-point/id'],'title':SOURCE[':knowledge-point/title']},'question':payload,'generation':{'version':VERSION,'seed':seed,'template':template,'profile':profile,'parameters':p,'source_id':qid,'source_basis':WRAPPER['basis'],'source_lineage':WRAPPER['lineage'],'mathematical_fingerprint':fingerprint,'domain':'all real '+p['v'],'eligible_for_learning':not raw,'evidence_only':raw,'inferred_correct':legacy and not raw,'bank_recipes':[l for l,e in bank],'runtime':{'python':sys.version.split()[0],'sympy':s.__version__}}}

def markdown(record):
 q=record['question'];out=q[':question/problem']+'\n\n'
 out+='\n'.join('- $'+a[':answer/value']+'$' for a in q[':question/answer-fields'][0][':answer-field/choices'])
 return out+'\n\n'+q.get(':question/worked-solution','[Source solution absent]')
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
 records=[generate(level,args.seed+i,template=args.template,profile=args.profile) for level in (['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]) for i in range(args.count)]
 print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
