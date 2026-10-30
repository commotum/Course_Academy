#!/usr/bin/env python3
"""Relocatable column-vector package, adapted from existing KP entry point.
No database access, publication, or generated images. See instructional-account.md.
"""
from __future__ import annotations
import argparse, copy, hashlib, itertools, json, random, sys, uuid
from pathlib import Path
from math_format import matrix_operands, matrix_answer, checked_math_content

KP_ID=17592186059712
KP_UUID='8a21360f-af5f-5730-85b2-b617de30eaf6'
TITLE='Calculating Sums and Scalar Multiplication of Column Vectors'
VERSION='column-vectors-2'
SOURCE=json.loads((Path(__file__).parent/'source-questions.json').read_text())
ORIGINALS={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
CANONICAL=SOURCE['record'][':knowledge-point/canonical-example']
ORIGINALS[CANONICAL[':question/math-academy-id']]=CANONICAL
OPENING='To compute the result, we just need to perform the required operations with each component separately:'
# outer, inner, unit-left, unit-first-inner, notation, source
TEMPLATES={
 'nested_minus_minus':(-1,-1,1,0,'bmatrix','q-18040'),
 'nested_minus_plus':(-1,1,1,0,'bmatrix','q-18041'),
 'nested_minus_plus_left_scaled':(-1,1,0,1,'bmatrix','q-70412'),
 'nested_plus_minus':(1,-1,1,0,'bmatrix','q-70414'),
 'negative_inner':(1,1,0,0,'bmatrix','q-318151'),
 'all_scaled':(-1,-1,0,0,'bmatrix','q-318154'),
 'canonical_minus_minus_left_scaled':(-1,-1,0,1,'bmatrix','e-4294'),
}
SOURCE_PARAMETERS={
 'q-18040':dict(a=[4,-2],b=[3,3],c=[-8,4],k=1,q=2,r=3,order='abc'),
 'q-18041':dict(a=[1,1],b=[4,1],c=[-1,2],k=1,q=2,r=5,order='abc'),
 'q-70412':dict(a=[4,-7],b=[2,4],c=[4,-6],k=3,q=1,r=4,order='abc'),
 'q-70414':dict(a=[-1,1],b=[2,5],c=[1,2],k=1,q=2,r=2,order='abc'),
 # a,b,c below are expression-role operands; order maps them to displayed names.
 'q-318151':dict(a=[3,-2],b=[-4,1],c=[-2,7],k=2,q=-3,r=1,order='bac'),
 'q-318154':dict(a=[-5,3],b=[2,-4],c=[-1,6],k=4,q=3,r=2,order='abc'),
 'e-4294':dict(a=[1,-5],b=[2,4],c=[-3,7],k=2,q=1,r=5,order='abc'),
}
SOURCE_TEMPLATE={v[-1]:k for k,v in TEMPLATES.items()}
RESIDUALS={'q-18040':[(0,0),(5,2),(60,-12),(60,0),(0,-12)],
           'q-18041':[(0,-2),(6,24),(1,0),(-2,0),(0,0)]}
NORMAL_PROFILE='authored-role-substitutions'
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(x):return str(uuid.uuid5(uuid.NAMESPACE_URL,x))
def matrix(v,style='bmatrix'):
 if style=='bmatrix':return r'\begin{bmatrix}'+str(v[0])+r' \\ '+str(v[1])+r'\end{bmatrix}'
 return r'[\begin{aligned}'+str(v[0])+r' \\ '+str(v[1])+r'\end{aligned}]'
def scale(k,v):return [int(k*x) for x in v]
def add(a,b,s=1):return [int(x+s*y) for x,y in zip(a,b)]
def coefficient(k,symbol):
 if k==1:return symbol
 return ('('+str(k)+')' if k<0 else str(k))+symbol

def expression(t,p):
 o,i,*_=TEMPLATES[t]
 space=' ' if TEMPLATES[t][4]=='bmatrix' else ''
 return coefficient(p['k'],p.get('order','abc')[0])+space+('+' if o==1 else '-')+space+'('+coefficient(p['q'],p.get('order','abc')[1])+space+('+' if i==1 else '-')+space+coefficient(p['r'],p.get('order','abc')[2])+')'

def product(k,v,style):
 m=matrix(v,style)
 return m if k==1 else ('('+str(k)+')' if k<0 else str(k))+r'\cdot '+m

def stages(t,p):
 o,i,*_=TEMPLATES[t];style=TEMPLATES[t][4]; a,b=p['a'],p['b'];q=p['q'];os='+' if o==1 else '-'
 k,r=p['k'],p['r']; c=p['c'];ins='+' if i==1 else '-';ka,qb,rc=scale(k,a),scale(q,b),scale(r,c);inner=add(qb,rc,i)
 return [product(k,a,style)+os+'('+product(q,b,style)+ins+product(r,c,style)+')',
         matrix(ka,style)+os+'('+matrix(qb,style)+ins+matrix(rc,style)+')',
         matrix(ka,style)+os+matrix(inner,style),matrix(add(ka,inner,o),style)]

def solution(t,p):
 rows=stages(t,p);ex=expression(t,p)
 if TEMPLATES[t][4]=='aligned':
  return OPENING+'\n\n$$\n'+r'\begin{aligned}'+ex+' & ='+rows[0]+''.join(r' \\  & ='+s for s in rows[1:])+r'\end{aligned}'+'\n$$'
 return OPENING+'\n\n$$\n'+r'\begin{aligned}'+'\n'+ex+' &= '+rows[0]+''.join(' '+r'\\'+'\n&= '+s for s in rows[1:])+'\n'+r'\end{aligned}'+'\n$$'


def _correct(t,p):
 o,i,*_=TEMPLATES[t]
 return add(scale(p['k'],p['a']),add(scale(p['q'],p['b']),scale(p['r'],p['c']),i),o)

def bank(t,p,profile=NORMAL_PROFILE,excluded_order=None):
 good=_correct(t,p)
 if profile.startswith('source-'):
  sid=profile.removeprefix('source-')
  if sid not in RESIDUALS:raise ValueError('Unknown historical bank')
  return [add(good,d) for d in RESIDUALS[sid]],['opaque_residual_'+str(n) for n in range(5)]
 if profile!=NORMAL_PROFILE:raise ValueError('Unknown bank profile')
 orders=[''.join(x) for x in itertools.permutations('abc')]
 if excluded_order not in orders or excluded_order==p['order']:raise ValueError('Bank exclusion must be a different role assignment')
 named=dict(zip(p['order'],[p[x] for x in 'abc']))
 # Five whole substitution computations, not a set of offsets centered on the key.
 # Conditional on the same named vectors, coefficients and five assignments,
 # every included assignment has equal chance to be the actual prompt target.
 included=[p['order']]+[order for order in orders if order not in (p['order'],excluded_order)]
 values=[]
 for order in included:
  altered=dict(p)
  altered.update({key:named[name] for key,name in zip('abc',order)})
  values.append(_correct(t,altered))
 return values,['substitute_roles_'+order for order in included]

def validate_parameters(t,p):
 if set(p)!={'a','b','c','k','q','r','order'}:raise ValueError('Exact parameter keys required')
 if p['order'] not in [''.join(x) for x in itertools.permutations('abc')]:raise ValueError('Invalid role permutation')
 for key in 'abc':
  if not isinstance(p[key],(list,tuple)) or len(p[key])!=2 or any(type(x)!=int or abs(x)>8 for x in p[key]):raise ValueError('Two integer components in -8..8 required')
 _,_,ku,qu,*_=TEMPLATES[t]
 for key,unit in [('k',ku),('q',qu),('r',t=='negative_inner')]:
  val=p[key]
  if type(val)!=int:raise ValueError('Integer scalar required')
  if unit:
   if val!=1:raise ValueError('Unit coefficient required by workload profile')
  elif key=='q' and t=='negative_inner':
   if not -5<=val<=-2:raise ValueError('Negative inner scalar required')
  elif not 2<=val<=5:raise ValueError('Positive scalar in 2..5 required')

def sample(t,rng,order):
 _,_,ku,qu,*_=TEMPLATES[t]
 return dict(a=[rng.randint(-8,8) for _ in range(2)],b=[rng.randint(-8,8) for _ in range(2)],c=[rng.randint(-8,8) for _ in range(2)],
             k=1 if ku else rng.randint(2,5),q=1 if qu else -rng.randint(2,5) if t=='negative_inner' else rng.randint(2,5),
             r=1 if t=='negative_inner' else rng.randint(2,5),order=order)

def prompt(t,p,mode):
 named=dict(zip(p['order'],[p[x] for x in 'abc']))
 ex=expression(t,p)
 given=matrix_operands([x+'='+matrix(named[x]) for x in 'abc'])
 text='Let the column vectors be\n\n'+given+'\n\nFind $'+ex+'$.'
 if mode=='blank':text+='\n\n'+matrix_answer(ex,[['{{field-1}}'],['{{field-2}}']])
 return text

def task_components(t,p):
 o,i,*_=TEMPLATES[t]
 # Include actual named operand assignment; exclude IDs and option ordering.
 return {'vectors':dict(zip(p['order'],[p[x] for x in 'abc'])),
         'expression_roles':p['order'],'coefficients':[p['k'],o*p['q'],o*i*p['r']]}

@checked_math_content
def generate(level='moderate',seed=0,template=None,parameters=None,mode=None,profile=None,source_id=None):
 if level!='moderate':raise ValueError('Only source-justified moderate difficulty is supported')
 rng=random.Random(seed)
 if source_id:
  if source_id not in ORIGINALS:raise ValueError('Unknown source')
  template=SOURCE_TEMPLATE[source_id];parameters=copy.deepcopy(SOURCE_PARAMETERS[source_id])
  mode='blank' if source_id in ('q-318151','q-318154') else 'radio'
  profile='source-'+source_id if source_id in RESIDUALS else NORMAL_PROFILE
 template=template or rng.choice(list(TEMPLATES))
 if template not in TEMPLATES:raise ValueError('Unknown template')
 mode=mode or rng.choice(['radio','blank'])
 if mode not in ('radio','blank'):raise ValueError('Unsupported response layout')
 profile=profile or NORMAL_PROFILE
 # Answer-bearing profile and role assignment selected before vector entries.
 order=parameters['order'] if parameters else ''.join(rng.sample('abc',3))
 eligible=[''.join(x) for x in itertools.permutations('abc') if ''.join(x)!=order]
 excluded_order=random.Random(f'bank/{seed}/{template}').choice(eligible)
 for attempt in range(10000):
  p=copy.deepcopy(parameters) if parameters else sample(template,rng,order)
  validate_parameters(template,p)
  values,recipes=bank(template,p,profile,excluded_order) if mode=='radio' else ([_correct(template,p)],['component_blanks'])
  if mode=='blank' or len(set(map(tuple,values)))==5:break
  if parameters:raise ValueError('Whole-bank collision')
 else:raise RuntimeError('Sampler exhausted')
 q={':question/problem':prompt(template,p,mode),':question/worked-solution':solution(template,p),
    ':question/difficulty':':question.difficulty/moderate'}
 good=_correct(template,p)
 fields=[]
 if mode=='radio':
  fields=[{':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',
           ':answer-field/choices':[{':answer/type':':answer.type/math',':answer/value':matrix(v)} for v in values]}]
 else:
  fields=[{':answer-field/key':'field-'+str(j+1),':answer-field/type':':answer-field.type/blank',
           ':answer-field/choices':[{':answer/type':':answer.type/math',':answer/value':str(v)}]} for j,v in enumerate(good)]
  if source_id=='q-318154':fields.reverse()
 content=digest({'version':VERSION,'question':q,'fields':fields,'correct':good})
 q[':question/id']=uid(content);q[':question/answer-fields']=fields
 for f in fields:
  key=f[':answer-field/key'];f[':answer-field/id']=uid(content+'/'+key)
  for a in f[':answer-field/choices']:a[':answer/id']=uid(content+'/'+key+'/'+a[':answer/value'])
  correct_value=matrix(good) if mode=='radio' else str(good[int(key[-1])-1])
  answer=next(a for a in f[':answer-field/choices'] if a[':answer/value']==correct_value)
  f[':answer-field/correct']=[':answer/id',answer[':answer/id']]
  if mode=='radio':rng.shuffle(f[':answer-field/choices'])
 original=ORIGINALS.get(source_id,{})
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,
         'generation':{'version':VERSION,'seed':seed,'level':level,'template':template,'mode':mode,
          'parameters':p,'bank_profile':profile,'excluded_bank_assignment':excluded_order if mode=='radio' and profile==NORMAL_PROFILE else None,'recipe_operations':recipes,'source_id':source_id,
          'source_refs':[TEMPLATES[template][-1],'e-4294','tutorial-2915'],
          'source_basis':SOURCE['basis'],'source_difficulty':original.get(':question/difficulty'),
          'completed_source_attributes':[x for x in (':question/answer-fields',':question/worked-solution',':question/difficulty') if source_id and x not in original],
          'semantic_instance':digest(task_components(template,p)),'rejections':attempt,
          'domain':{'component_bounds':[-8,8],'positive_scales':[2,5],'negative_inner_scales':[-5,-2]},
          'dependencies':{'python':sys.version.split()[0]}}}

def replay(source_id):return generate(source_id=source_id)

def main():
 parser=argparse.ArgumentParser()
 parser.add_argument('--difficulty',default='moderate',choices=['easy','moderate','hard'])
 parser.add_argument('--count',type=int,default=5);parser.add_argument('--seed',type=int,default=0)
 parser.add_argument('--format',choices=['json'],default='json')
 parser.add_argument('--template',choices=list(TEMPLATES));parser.add_argument('--mode',choices=['radio','blank'])
 args=parser.parse_args()
 if args.count<1:parser.error('--count must be positive')
 if args.difficulty!='moderate':parser.error('Only source-justified moderate difficulty is supported')
 print(json.dumps([generate(args.difficulty,args.seed+n,template=args.template,mode=args.mode) for n in range(args.count)],indent=2))
if __name__=='__main__':main()
