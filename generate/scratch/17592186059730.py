#!/usr/bin/env python3
"""Exact component-dot-product generator. Observed profiles are explicit replay
profiles; default radio banks are authored complete operation banks. No EDB writes.
See the adjacent evidence directory for observed/authored workload definitions.
"""
import argparse
import hashlib
import json
from pathlib import Path
import random
import uuid
# The inventory worker uses system Python; reuse the repository dependency environment.
try:
 import sympy as sp
except ModuleNotFoundError:
 import os, sys
 runtime = Path(__file__).resolve().parents[2] / '.venv/bin/python'
 if not runtime.is_file() or Path(sys.executable).absolute() == runtime.absolute():
  raise
 os.execv(str(runtime), [str(runtime), str(Path(__file__).resolve()), *sys.argv[1:]])

KP = {'db_id':17592186059730,'id':'68abb4f0-c532-5cb6-882c-dacfe6a945dc','title':'Calculating the Dot Product Using the General Formula'}
VERSION = '59730-v1'
GENERATOR_UUID = '4e729dd4-b331-5f5b-8c36-7bc58a5536ca'
EVIDENCE = Path(__file__).with_suffix('')
NS = uuid.UUID('9ad6f695-feca-460a-80b5-181c270b92db')
TEMPLATES = {
 'let2_radio': {'dimension':2,'kind':'radio','names':['u','v'],'style':'let','levels':['easy']},
 'if3_arrow_radio': {'dimension':3,'kind':'radio','names':['a','b'],'style':'arrow','levels':['easy']},
 'if3_radio': {'dimension':3,'kind':'radio','names':['a','b'],'style':'spaced','levels':['easy']},
 'dependent3_blank': {'dimension':3,'kind':'blank','names':['q','r'],'style':'dependent','levels':['easy']},
 'if2_blank': {'dimension':2,'kind':'blank','names':['a','b'],'style':'blank','levels':['easy']},
 'components3_radio': {'dimension':3,'kind':'radio','names':['a','b'],'style':'let','levels':['moderate','hard']},
 'components3_blank': {'dimension':3,'kind':'blank','names':['a','b'],'style':'blank','levels':['moderate','hard']},
}
# Complete profiles are retained together. These are numerical reconstructions,
# not claims about original distractor intent. They are excluded from defaults.
PROFILES = {'observed_1340':'let2_radio','observed_101406':'let2_radio',
 'observed_1341':'if3_arrow_radio','observed_1355':'if3_radio',
 'observed_168035':'dependent3_blank','observed_317910':'if2_blank','observed_317911':'if2_blank',
 'authored_operations':None,'authored_blank':None}
RAW = json.loads((EVIDENCE/'source.json').read_text())
SOURCES = {q[':question/math-academy-id']:q for q in RAW['record'][':knowledge-point/questions']}


def digest(x):
 return hashlib.sha256(json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
def uid(x): return str(uuid.uuid5(NS,x))
def exact(x):
 if isinstance(x,(bool,float)): raise ValueError('Use exact integers or decimal/fraction strings, never binary floats')
 z=sp.Rational(x)
 if not z.is_finite: raise ValueError('finite rational required')
 return z

def number(x):
 """Finite terminating decimals retain arithmetic form; other rationals use TeX."""
 x=exact(x)
 if x.q==1: return str(x.p)
 if 10 % x.q == 0 or 100 % x.q == 0:
  return format(float(x),'.2f').rstrip('0').rstrip('.')
 return sp.latex(x)

def factor(x):
 v=number(x)
 return '('+v+')' if x<0 else v

def sum_tex(xs,parenthesized=False):
 if parenthesized: return '+'.join(factor(x) for x in xs)
 out=number(xs[0])
 for x in xs[1:]: out+=('-'+number(-x) if x<0 else '+'+number(x))
 return out

def vectors(p):
 return [exact(x) for x in p['a']],[exact(x) for x in p['b']]

def validate_parameters(level,spec,p,observed):
 if set(p)-{'a','b','names'}: raise ValueError('unknown parameters')
 a,b=vectors(p)
 if len(a)!=spec['dimension'] or len(b)!=len(a): raise ValueError('dimension mismatch')
 names=p.get('names',spec['names'])
 if len(names)!=2 or any(n not in ('a','b','u','v','p','q','r') for n in names) or names[0]==names[1]: raise ValueError('invalid names')
 if observed:
  if level!='easy' or any(x.q!=1 or abs(x)>12 for x in a+b): raise ValueError('observed easy profile requires small integral components')
 elif level=='easy':
  if any(x.q!=1 or abs(x)>12 for x in a+b): raise ValueError('easy integral bound +/-12')
 elif level=='moderate':
  if any(x.q!=1 or not 2<=abs(x)<=12 for x in a+b): raise ValueError('moderate: three nonzero integral products; all magnitudes 2..12')
  if not any(x*y<0 for x,y in zip(a,b)) or not any(x*y>0 for x,y in zip(a,b)): raise ValueError('moderate requires mixed signed products')
 else:
  t=[x*y for x,y in zip(a,b)]
  if any(not 1<=abs(x)<=6 or 10 % x.q for x in a+b): raise ValueError('hard exact tenths, nonzero magnitudes 1..6')
  if sum(x.q!=1 for x in t)<2 or not any(x<0 for x in t) or not any(x>0 for x in t): raise ValueError('hard requires at least two nonintegral products and mixed signs')
 return a,b,names


def bank(a,b,profile):
 t=[x*y for x,y in zip(a,b)]; c=sum(t)
 if profile=='observed_1340':
  vals=[b[0]*b[1],2*c,-t[0]+t[1],c,a[0]*a[1]+b[0]*b[1]]
  ops=['within_b_product','double_dot','reverse_first_product','correct','sum_within_vector_products']
 elif profile=='observed_101406':
  vals=[t[1]-t[0],c,2*t[0],t[1],-t[0]]
  ops=['reverse_first_product','correct','double_first_omit_second','omit_first','negate_first_omit_second']
 elif profile=='observed_1341':
  vals=[t[0],t[0]+t[2],t[0]-2*t[1],t[0]-t[2],c]
  ops=['only_first','omit_second','reverse_double_second_omit_third','omit_second_reverse_third','correct']
 elif profile=='observed_1355':
  vals=[t[2]-t[0],c,-t[0],-c,t[0]-t[2]]
  ops=['reverse_first_omit_second','correct','negate_first_only','negate_dot','reverse_third_omit_second']
 elif profile=='authored_operations':
  vals=[c,sum(a)+sum(b),sum(a)*sum(b),sum(t[1:]),sum(t[:-1])]
  ops=['correct','add_all_components_instead_of_multiply','multiply_component_sums_all_pair_products','omit_first_product','omit_last_product']
 else: vals,ops=[c],['correct']
 if len(set(vals))!=len(vals): raise ValueError('whole bank rejected: equivalent choices')
 return vals,ops,c


def prompt(spec,p,a,b,names,profile):
 x,y=names; va='⟨'+','.join(number(z) for z in a)+'⟩'; vb='⟨'+','.join(number(z) for z in b)+'⟩'
 style=spec['style']
 if style=='arrow':
  nx=r'\overset{\to }{'+x+'}'; ny=r'\overset{\to }{'+y+'}'
  return f'If ${nx}={va}$ and ${ny}={vb}$, then ${nx}\\cdot {ny}=$'
 if style=='spaced':
  # Source spacing is a complete vector slot, never a global text replacement.
  vasp='⟨ '+', '.join(('- '+number(-z) if z<0 and i==0 else number(z)) for i,z in enumerate(a))+'⟩'
  vbsp='⟨'+', '.join(number(z) for z in b[:2])+','+number(b[2])+'⟩'
  return f'If ${x} = {vasp}$ and ${y} = {vbsp}$, then ${x} \\cdot {y} =$'
 if style=='dependent':
  # Preserve the raw source prompt, adding the omitted part-1 data for standalone use.
  intro=f'Given ${x}={va}$ and ${y}={vb}.$\n\n'
  if profile=='observed_168035':
   if names!=['q','r']: raise ValueError('observed dependent layout fixes q,r labels')
   return intro+SOURCES['q-168035'][':question/problem']
  return intro+f'Find the dot product of the vectors ${x}$ and ${y}.$\n\n${x}\\cdot {y}=\\,$ {{{{field-1}}}}'
 if style=='blank': return f'If ${x}={va}$ and ${y}={vb},$ then ${x}\\cdot {y}=${{{{field-1}}}}.'
 return f'Let ${x}={va}$ and ${y}={vb}.$ Find ${x}\\cdot {y}.$'


def aligned(lhs,rows):
 return '$$\n\\begin{aligned}'+lhs+' & ='+rows[0]+''.join(' \\\\  & ='+s for s in rows[1:])+r'\end{aligned}'+'\n$$'


def solution(spec,a,b,names,profile):
 x,y=names; t=[v*w for v,w in zip(a,b)]; c=sum(t)
 lhs=x+r'\cdot '+y
 if spec['style']=='arrow': lhs=r'\overset{\to }{'+x+r'}\cdot \overset{\to }{'+y+'}'
 formal='+'.join('{'+x+'}_{'+k+r'}\cdot {'+y+'}_{'+k+'}' for k in 'xyz'[:len(a)])
 multiply='+'.join(factor(v)+r'\cdot '+factor(w) for v,w in zip(a,b))
 addition=sum_tex(t,spec['style']=='arrow')
 period='.' if spec['kind']=='blank' else ''
 if spec['style']=='dependent':
  va='⟨'+','.join(number(z) for z in a)+'⟩'; vb='⟨'+','.join(number(z) for z in b)+'⟩'
  context='From part 1' if profile=='observed_168035' else 'For these vectors'
  return 'The dot product of two vectors given in component form can be computed by summing up the products of corresponding components of vectors:\n\n'+aligned(lhs,[formal])+f'\n\n{context}, we have ${x}={va}$ and ${y}={vb}.$ Therefore, the formula for the dot product gives\n\n'+aligned(lhs,[multiply,addition,number(c)+'.'])
 opening='Summing up the products of corresponding components, we obtain'+('' if spec['kind']=='blank' else ':')+'\n\n'
 return opening+aligned(lhs,[formal,multiply,addition,number(c)+period])


def sample(level,spec,rng):
 d=spec['dimension']
 if level=='hard':
  entries=[sp.Rational(s*n,10) for n in range(10,61) for s in [-1,1]]
 elif level=='moderate': entries=[s*n for n in range(2,13) for s in [-1,1]]
 else: entries=list(range(-12,13))
 return {'a':[str(rng.choice(entries)) for _ in range(d)],'b':[str(rng.choice(entries)) for _ in range(d)]}


def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'): raise ValueError('invalid level')
 rng=random.Random(seed)
 if profile is not None and profile not in PROFILES: raise ValueError('unknown profile')
 observed=bool(profile and profile.startswith('observed_'))
 if observed:
  implied=PROFILES[profile]
  if template is not None and template!=implied: raise ValueError('profile/template mismatch')
  template=implied
 eligible=[k for k,v in TEMPLATES.items() if level in v['levels'] and (field_type is None or field_type==v['kind'])]
 if template is None: template=rng.choice(eligible) if eligible else None
 if template not in eligible: raise ValueError('template, level or field mismatch')
 spec=TEMPLATES[template]
 profile=profile or ('authored_operations' if spec['kind']=='radio' else 'authored_blank')
 if (profile=='authored_blank' and spec['kind']!='blank') or (profile=='authored_operations' and spec['kind']!='radio'): raise ValueError('profile field mismatch')
 for _ in range(1000):
  p=dict(parameters) if parameters is not None else sample(level,spec,rng)
  try:
   a,b,names=validate_parameters(level,spec,p,observed)
   vals,ops,c=bank(a,b,profile)
  except ValueError:
   if parameters is not None: raise
   continue
  p={'a':[str(v) for v in a],'b':[str(v) for v in b],'names':names}
  prob=prompt(spec,p,a,b,names,profile); sol=solution(spec,a,b,names,profile)
  # Commutativity and simultaneous coordinate permutation are mathematical aliases.
  pairs=sorted(tuple(sorted((str(v),str(w)))) for v,w in zip(a,b))
  fingerprint=digest({'skill':'sum_corresponding_products','coordinate_pairs':pairs})
  identity=digest({'version':VERSION,'level':level,'problem':prob,'solution':sol,'bank':sorted(number(v) for v in vals),'kind':spec['kind']})
  qid=uid('question:'+identity); fid=uid('field:'+identity)
  choices=[{':answer/id':uid('answer:'+fid+':'+number(v)),':answer/type':':answer.type/math',':answer/value':number(v)} for v in vals]
  correct=next(z[':answer/id'] for z,v in zip(choices,vals) if v==c)
  if spec['kind']=='radio': rng.shuffle(choices)
  q={':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prob,':question/worked-solution':sol,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection' if spec['kind']=='radio' else 'field-1',':answer-field/type':':answer-field.type/'+spec['kind'],':answer-field/choices':choices,':answer-field/correct':[':answer/id',correct]}]}
  return {'knowledge_point':KP.copy(),'question':q,'generation':{'version':VERSION,'template':template,'seed':seed,'parameters':p,'bank_profile':profile,'recipes':dict(zip((number(v) for v in vals),ops)),'mathematical_fingerprint':fingerprint,'content_identity':identity,'basis':RAW['basis'],'lineage':RAW['lineage'],'origin':'observed bank reconstruction' if observed else 'authored complete bank','level_origin':'observed easy or explicitly authored easy unrated repair' if level=='easy' else 'authored missing level','plot_requirement':'none'}}
 raise ValueError('bounded whole-bank sampling exhausted')

# EASY: observed two/three-component integer calculation, radio/blank layouts.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):
 return generate('easy',seed,template,field_type,parameters,profile)

# MODERATE: authored three nonzero mixed-sign integer products, magnitudes 2..12.
# Both layouts have identical arithmetic demand; there is no within-level progression.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):
 return generate('moderate',seed,template,field_type,parameters,profile)

# HARD: authored three products with >=2 nonintegral contributions; exact tenths.
# Same formula, no unknown coordinates, angles, orthogonality or vector algebra.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):
 return generate('hard',seed,template,field_type,parameters,profile)


def markdown(rec):
 q=rec['question']; f=q[':question/answer-fields'][0]
 out=q[':question/problem']+'\n\n'
 if f[':answer-field/type'].endswith('/radio'):
  out+='\n'.join('- $'+a[':answer/value']+'$'+(' **correct**' if a[':answer/id']==f[':answer-field/correct'][1] else '') for a in f[':answer-field/choices'])
 else: out+='Correct entry: $'+f[':answer-field/choices'][0][':answer/value']+'$'
 return out+'\n\n'+q[':question/worked-solution']

def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all'); p.add_argument('--seed',type=int,default=0); p.add_argument('--count',type=int,default=1); p.add_argument('--format',choices=['markdown','json'],default='markdown'); p.add_argument('--template',choices=TEMPLATES); p.add_argument('--profile',choices=PROFILES); p.add_argument('--field-type',choices=['radio','blank'])
 args=p.parse_args()
 if args.count<1 or args.difficulty=='all' and (args.template or args.profile): p.error('positive count; specific difficulty for template/profile')
 levels=['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]
 records=[generate(l,args.seed+i,args.template,args.field_type,profile=args.profile) for l in levels for i in range(args.count)]
 print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
if __name__=='__main__': main()
