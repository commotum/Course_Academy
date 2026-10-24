#!/usr/bin/env python3
"""Exact component-dot-product generator. Observed profiles are explicit replay
profiles; default radio banks are authored complete operation banks. No EDB writes.
See the adjacent evidence directory for observed/authored workload definitions.
"""

# Standalone source eligibility: immutable policy ledger, seeded CLI guard.
import sys as _ca_sys, os as _ca_os
from pathlib import Path as _ca_Path
_ca_sys.path.insert(0,str(_ca_Path(__file__).resolve().parent))
if __name__ == "__main__" and not _ca_os.environ.get("_CA_SOURCE_POLICY_CHILD"):
    from ca_source_runtime import cli as _ca_source_cli
    _ca_source_cli(__file__,_ca_Path(__file__).with_name('17592186059730-source-policy.json'))
    raise SystemExit(0)

import argparse
import hashlib
import json
from pathlib import Path
import random
import itertools
import uuid
import sys
sys.dont_write_bytecode = True
from math_format import checked_math_content, normalize_prose, normalize_tex
import sympy as sp

KP = {'db_id':17592186059730,'id':'68abb4f0-c532-5cb6-882c-dacfe6a945dc','title':'Calculating the Dot Product Using the General Formula'}
VERSION = '59730-v2'
EVIDENCE = Path(__file__).resolve().parent
NS = uuid.UUID('9ad6f695-feca-460a-80b5-181c270b92db')
TEMPLATES = {
 'let2_radio': {'dimension':2,'kind':'radio','names':['u','v'],'style':'let','levels':['easy']},
 'if3_arrow_radio': {'dimension':3,'kind':'radio','names':['a','b'],'style':'arrow','levels':['easy']},
 'if3_radio': {'dimension':3,'kind':'radio','names':['a','b'],'style':'spaced','levels':['easy']},
 'dependent3_blank': {'dimension':3,'kind':'blank','names':['q','r'],'style':'dependent','levels':['easy']},
 'if2_blank': {'dimension':2,'kind':'blank','names':['a','b'],'style':'blank','levels':['easy']},
 'let3_arrow_radio': {'dimension':3,'kind':'radio','names':['u','v'],'style':'let_arrow','levels':['easy']},
 'if4_radio': {'dimension':4,'kind':'radio','names':['v','w'],'style':'if','levels':['easy']},
 'if4_blank': {'dimension':4,'kind':'blank','names':['p','q'],'style':'blank','levels':['easy']},
 'if2_arrow_blank': {'dimension':2,'kind':'blank','names':['k','l'],'style':'blank_arrow','levels':['easy']},
}
# Complete profiles are retained together. These are numerical reconstructions,
# not claims about original distractor intent. They are excluded from defaults.
PROFILES = {'observed_1340':'let2_radio','observed_101406':'let2_radio',
 'observed_1341':'if3_arrow_radio','observed_1355':'if3_radio',
 'observed_168035':'dependent3_blank','observed_317910':'if2_blank','observed_317911':'if2_blank',
 'observed_1356':'let3_arrow_radio','observed_101408':'if4_radio',
 'observed_101405':'let2_radio','observed_317913':'if4_blank',
 'observed_317916':'if2_arrow_blank','observed_168042':'dependent3_blank',
 'observed_168028':'dependent3_blank','authored_operations':None,'authored_component_operations':None,'authored_blank':None}
RAW = json.loads((EVIDENCE/'source.json').read_text())
SOURCES = {q[':question/math-academy-id']:q for q in RAW['material']['kp'][':knowledge-point/questions'] if ':question/math-academy-id' in q}
BATCH_LIMIT = 1000  # Conservative service cap, below the finite parameter-domain capacity.


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
 if len(names)!=2 or any(n not in tuple('abuvpqrwckl') for n in names) or names[0]==names[1]: raise ValueError('invalid names')
 if level!='easy': raise ValueError('unsupported difficulty: source supports easy only')
 if any(x.q!=1 or abs(x)>12 for x in a+b): raise ValueError('easy integral bound +/-12')
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
 elif profile=='observed_1356':
  vals=[t[0]+t[2],c,t[0]+t[1]-t[2],sp.Integer(0),t[2]]
  ops=['omit_second','correct','reverse_third','constant_zero_replay','only_third']
 elif profile=='observed_101408':
  vals=[t[0]-t[2],c,3*t[0],c+t[0]-t[2],t[2]]
  ops=['first_minus_third','correct','triple_first','dot_plus_first_minus_third','only_third']
 elif profile=='observed_101405':
  vals=[b[1],t[0],sum(a)*sum(b),a[0]*b[1],c]
  ops=['second_b_component','only_first','product_of_sums','cross_first_second','correct']
 elif profile=='authored_operations':
  vals=[c,sum(a)+sum(b),sum(a)*sum(b),sum(t[1:]),sum(t[:-1])]
  ops=['correct','add_all_components_instead_of_multiply','multiply_component_sums_all_pair_products','omit_first_product','omit_last_product']
 elif profile=='authored_component_operations':
  vals=[c,sum(a)+sum(b),sum(a)+2*sum(b),sum(a)-sum(b),sum(a[i]*b[(i+1)%len(a)] for i in range(len(a)))]
  ops=['correct','add_all_components','add_first_sum_and_twice_second_sum','subtract_component_sums','cyclic_wrong_coordinate_products']
 else: vals,ops=[c],['correct']
 if len(set(vals))!=len(vals): raise ValueError('whole bank rejected: equivalent choices')
 return vals,ops,c


def notation(spec,names):
 if spec['style'] in ('arrow','let_arrow','blank_arrow'):
  return [r'\overset{\to }{'+n+'}' for n in names]
 return names

def prompt(spec,p,a,b,names,profile):
 x,y=notation(spec,names)
 va='⟨'+','.join(number(z) for z in a)+'⟩'; vb='⟨'+','.join(number(z) for z in b)+'⟩'
 style=spec['style']
 if style=='spaced':
  vasp='⟨ '+', '.join(('- '+number(-z) if z<0 and i==0 else number(z)) for i,z in enumerate(a))+'⟩'
  vbsp='⟨'+', '.join(number(z) for z in b[:2])+','+number(b[2])+'⟩'
  return f'If ${x} = {vasp}$ and ${y} = {vbsp}$, then ${x} \\cdot {y} =$'
 if style=='dependent':
  return f'Given ${x}={va}$ and ${y}={vb}.$\n\nFind the dot product of the vectors ${x}$ and ${y}.$\n\n${x}\\cdot {y}=\\,$ {{{{field-1}}}}'
 if style=='blank' and len(a)==4:
  return f'If ${x}={va}$ and ${y}={vb}$, then ${x}\\cdot {y}=${{{{field-1}}}}.'
 if style in ('blank','blank_arrow'):
  return f'If ${x}={va}$ and ${y}={vb},$ then ${x}\\cdot {y}=${{{{field-1}}}}.'
 if style in ('arrow','if'):
  return f'If ${x}={va}$ and ${y}={vb}$, then ${x}\\cdot {y}=$'
 return f'Let ${x}={va}$ and ${y}={vb}.$ Find ${x}\\cdot {y}.$'


def aligned(lhs,rows):
 return '$$\n\\begin{aligned}'+lhs+' & ='+rows[0]+''.join(' \\\\  & ='+s for s in rows[1:])+r'\end{aligned}'+'\n$$'


def solution(spec,a,b,names,profile):
 x,y=names; t=[v*w for v,w in zip(a,b)]; c=sum(t)
 nx,ny=notation(spec,names)
 lhs=nx+r'\cdot '+ny
 formal='+'.join('{'+x+'}_{'+k+r'}\cdot {'+y+'}_{'+k+'}' for k in ('xyz'[:len(a)] if len(a)<4 else '1234'))
 multiply='+'.join(factor(v)+r'\cdot '+factor(w) for v,w in zip(a,b))
 addition=sum_tex(t,spec['style']=='arrow')
 period='.' if spec['kind']=='blank' else ''
 if spec['style']=='dependent':
  va='⟨'+','.join(number(z) for z in a)+'⟩'; vb='⟨'+','.join(number(z) for z in b)+'⟩'
  context='For these vectors'
  return 'The dot product of two vectors given in component form can be computed by summing up the products of corresponding components of vectors:\n\n'+aligned(lhs,[formal])+f'\n\n{context}, we have ${x}={va}$ and ${y}={vb}.$ Therefore, the formula for the dot product gives\n\n'+aligned(lhs,[multiply,addition,number(c)+'.'])
 opening='Summing up the products of corresponding components, we obtain'+('' if spec['kind']=='blank' else ':')+'\n\n'
 return opening+aligned(lhs,[formal,multiply,addition,number(c)+period])


def sample(level,spec,rng):
 # Select contributing roles and signs before numerical factors.
 d=spec['dimension']
 pattern=rng.choice([p for p in itertools.product((-1,0,1),repeat=d) if any(p)])
 return sample_pattern(pattern,rng)

def sample_pattern(pattern,rng):
 a=[]; b=[]
 for sign in pattern:
  u=rng.choice((-1,1))*rng.randint(1,12)
  v=rng.randint(1,12)*(sign if u>0 else -sign)
  if sign==0:
   side=rng.choice(('a','b','both'))
   v=rng.choice((-1,1))*rng.randint(1,12)
   if side in ('a','both'): u=0
   if side in ('b','both'): v=0
  a.append(str(u)); b.append(str(v))
 return {'a':a,'b':b}


@checked_math_content
def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None,product_pattern=None):
 if type(seed) is not int: raise TypeError('seed must be a built-in int')
 if level!='easy': raise ValueError('unsupported difficulty: source supports easy only')
 rng=random.Random(seed)
 if profile is not None and profile not in PROFILES: raise ValueError('unknown profile')
 observed=bool(profile and profile.startswith('observed_'))
 if observed:
  implied=PROFILES[profile]
  if template is not None and template!=implied: raise ValueError('profile/template mismatch')
  template=implied
  replay=json.loads((EVIDENCE/'source-cases.json').read_text())
  source=next(z for z in replay if z['bank_profile']==profile)
  if parameters is None: parameters=source['parameters']
  if any([str(v) for v in parameters[k]] != [str(v) for v in source['parameters'][k]] for k in ('a','b')):
   raise ValueError('observed numerical reconstructions are finite source replay profiles')
  parameters=dict(parameters, names=source['parameters'].get('names',TEMPLATES[template]['names']))
 eligible=[k for k,v in TEMPLATES.items() if level in v['levels'] and (field_type is None or field_type==v['kind'])]
 if template is None: template=rng.choice(eligible) if eligible else None
 if template not in eligible: raise ValueError('template, level or field mismatch')
 spec=TEMPLATES[template]
 if parameters is None:
  product_pattern=product_pattern or rng.choice([p for p in itertools.product((-1,0,1),repeat=spec['dimension']) if any(p)])
  if len(product_pattern)!=spec['dimension'] or any(s not in (-1,0,1) for s in product_pattern) or not any(product_pattern): raise ValueError('invalid product pattern')
 if profile is None:
  if spec['kind']=='blank': profile='authored_blank'
  elif product_pattern is not None and (product_pattern[0]==0 or product_pattern[-1]==0): profile='authored_component_operations'
  else: profile=rng.choice(('authored_operations','authored_component_operations'))
 if (profile=='authored_blank' and spec['kind']!='blank') or (profile in ('authored_operations','authored_component_operations') and spec['kind']!='radio'): raise ValueError('profile field mismatch')
 for attempt in range(1000):
  p=dict(parameters) if parameters is not None else sample_pattern(product_pattern,rng)
  try:
   a,b,names=validate_parameters(level,spec,p,observed)
   vals,ops,c=bank(a,b,profile)
  except ValueError:
   if parameters is not None: raise
   continue
  p={'a':[str(v) for v in a],'b':[str(v) for v in b],'names':names}
  prob=normalize_prose(prompt(spec,p,a,b,names,profile)); sol=normalize_prose(solution(spec,a,b,names,profile))
  # Commutativity and simultaneous coordinate permutation are mathematical aliases.
  pairs=sorted(tuple(sorted((str(v),str(w)))) for v,w in zip(a,b))
  fingerprint=digest({'skill':'sum_corresponding_products','coordinate_pairs':pairs})
  identity=digest({'version':VERSION,'level':level,'problem':prob,'solution':sol,'bank':sorted(number(v) for v in vals),'kind':spec['kind']})
  qid=uid('question:'+identity); fid=uid('field:'+identity)
  choices=[{':answer/id':uid('answer:'+fid+':'+number(v)),':answer/type':':answer.type/math',':answer/value':normalize_tex(number(v))} for v in vals]
  correct=next(z[':answer/id'] for z,v in zip(choices,vals) if v==c)
  if spec['kind']=='radio': rng.shuffle(choices)
  q={':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prob,':question/worked-solution':sol,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection' if spec['kind']=='radio' else 'field-1',':answer-field/type':':answer-field.type/'+spec['kind'],':answer-field/choices':choices,':answer-field/correct':[':answer/id',correct]}]}
  return {'knowledge_point':KP.copy(),'question':q,'generation':{'version':VERSION,'template':template,'seed':seed,'parameters':p,'bank_profile':profile,'recipes':dict(zip((number(v) for v in vals),ops)),'mathematical_fingerprint':fingerprint,'canonical_task_key':fingerprint,'content_identity':identity,'basis':RAW['basis'],'lineage':RAW['lineage'],'origin':'observed bank reconstruction' if observed else 'authored complete bank','level_origin':'source-supported easy; q-1355 replay assigned easy' if profile=='observed_1355' else 'source-supported easy','plot_requirement':'none','rejections':attempt,'product_sign_pattern':[int(sp.sign(v*w)) for v,w in zip(a,b)]}}
 raise ValueError('bounded whole-bank sampling exhausted')

# EASY: observed two/three-component integer calculation, radio/blank layouts.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):
 return generate('easy',seed,template,field_type,parameters,profile)



def markdown(rec):
 q=rec['question']; f=q[':question/answer-fields'][0]
 out=q[':question/problem']+'\n\n'
 if f[':answer-field/type'].endswith('/radio'):
  out+='\n'.join('- $'+a[':answer/value']+'$'+(' **correct**' if a[':answer/id']==f[':answer-field/correct'][1] else '') for a in f[':answer-field/choices'])
 else: out+='Correct entry: $'+f[':answer-field/choices'][0][':answer/value']+'$'
 return out+'\n\n'+q[':question/worked-solution']

def generate_batch(difficulty='easy',seed=0,count=1,template=None,field_type=None,profile=None):
 if type(seed) is not int or type(count) is not int: raise TypeError('seed/count must be built-in int')
 if count<1 or count>BATCH_LIMIT: raise ValueError('count must be in 1..'+str(BATCH_LIMIT))
 if difficulty!='easy': raise ValueError('unsupported difficulty: source supports easy only')
 if difficulty=='all' and (template or profile): raise ValueError('select one difficulty for a template/profile')
 levels=[difficulty]
 records=[]; seen=set()
 for level in levels:
  selected=0
  for offset in range(count*100):
   r=generate(level,seed+offset,template,field_type,profile=profile)
   key=r['generation']['canonical_task_key']
   if key in seen: continue
   seen.add(key); records.append(r); selected+=1
   if selected==count: break
  if selected<count: raise ValueError('bounded unique sampling exhausted; reduce count')
 return records

def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='easy'); p.add_argument('--seed',type=int,default=0); p.add_argument('--count',type=int,default=1); p.add_argument('--format',choices=['markdown','json'],default='json'); p.add_argument('--template',choices=TEMPLATES); p.add_argument('--profile',choices=PROFILES); p.add_argument('--field-type',choices=['radio','blank'])
 args=p.parse_args()
 try: records=generate_batch(args.difficulty,args.seed,args.count,args.template,args.field_type,args.profile)
 except (ValueError,TypeError) as error: p.error(str(error))
 print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))

from ca_source_runtime import install as _ca_source_install
_ca_source_install(globals(),_ca_Path(__file__).with_name('17592186059730-source-policy.json'))

if __name__=='__main__': main()
