#!/usr/bin/env python3
"""Transform a supplied curve point back through f and onto a reflected curve.

Only complete captured source banks are supported. Opaque coordinate recipes
are retained as value patterns; no recovered misconception intent is claimed.
"""
import argparse, hashlib, json, random, re, uuid
from pathlib import Path
import sympy as sp

KP_ID=17592186059669
KP_UUID='38b450bd-b43a-507c-9bbe-0aaf7a64a3ed'
TITLE='Finding a Point That Lies on a Transformed Curve Given Another Transformed Curve'
VERSION='1.0.0'
SUPPORTED_LEVELS=('moderate','hard')
D=Path(__file__).with_suffix('')
SOURCE=json.loads((D/'source.json').read_text())
ORIGINALS={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
CASES={
 'q-119308':dict(level='moderate',kind='vertical_shift',p=dict(x=2,y=3,h=-1,k=4),bank=['(x,c-1)','(x,c)','(x,c+2)','(x,c+1)','(x,c-3)']),
 'q-121407':dict(level='moderate',kind='horizontal_shift',p=dict(x=-3,y=4,h=1,k=2),bank=['(h,c)','(u,c)','(u,y-h)','(-u,x)','(-h,k)']),
 'q-26408':dict(level='moderate',kind='vertical_shift',p=dict(x=-1,y=3,h=1,k=2),bank=['(x,c)','(x,y)','(x,-y)','(x,h)','(x,-h)']),
 'q-26596':dict(level='moderate',kind='vertical_shift',p=dict(x=3,y=2,h=-2,k=2),bank=['(x,c+k)','(x,w)','(x,y)','(x,c)','(-x,c)']),
 'q-26726':dict(level='moderate',kind='vertical_shift',p=dict(x=4,y=2,h=2,k=4),bank=['(-x,c)','(x,c)','(x,-c)','(x,-y-h-k)','(x,w)']),
 'q-121414':dict(level='hard',kind='vertical_scale',p=dict(x=4,y=8,a=4,k=3),bank=['(x,c)','(x,w)','(x,-c)','(x,k)','(x,a)']),
 'q-121418':dict(level='hard',kind='vertical_scale',p=dict(x=2,y=3,a='1/3',k=5),bank=['(-x,c)','(x,c)','(x,-2*c)','(-x,2*c)','(x,c/2)']),
}
FIELDLESS={sid:ORIGINALS[sid] for sid in ['q-121431','q-158542','q-158546','q-26597']}
def digest(z):return hashlib.sha256(json.dumps(z,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def val(z):return sp.Rational(z)
def tex(z):return sp.latex(val(z))
def pair(z):return '('+','.join(tex(a) for a in z)+')'
def shift(z):return ('+' if z>0 else '-')+tex(abs(z)) if z else ''
def coefficient(z):return '' if z==1 else '-' if z==-1 else tex(z)
def environment(case,p):
 e={key:val(z) for key,z in p.items()};x,y=e['x'],e['y']
 e['u']=x+e['h'] if case['kind']=='horizontal_shift' else x
 e['w']=y-e['h'] if case['kind']=='vertical_shift' else y/e['a'] if case['kind']=='vertical_scale' else y
 e['c']=-e['w']+e['k'];return e
def domain(case,key):
 if key=='a':return ['1/2','1/3','1/4',2,3,4,5]
 return list(range(-8,9)) if key in ('x','y') else [-5,-4,-3,-2,-1,1,2,3,4,5]
def curves(case,p):
 if case['kind']=='vertical_shift':source='f(x)'+shift(p['h'])
 elif case['kind']=='horizontal_shift':source='f(x'+shift(p['h'])+')'
 else:source=coefficient(p['a'])+'f(x)'
 return source,'-f(x)'+shift(p['k'])
def render(case,p):
 e=environment(case,p);x,y,u,w,c=[e[key] for key in ('x','y','u','w','c')];src,dst=curves(case,e)
 prompt=f'The point ${pair((x,y))}$ lies on the curve $y={src}.$ Which of the following points **must** lie on $y={dst}?$'
 if case['kind']=='vertical_shift':
  undo=f'shift the graph vertically by ${tex(abs(e["h"]))}$ '+('unit' if abs(e['h'])==1 else 'units')+' '+('down' if e['h']>0 else 'up')
  calculation=f'({tex(x)},{tex(y)}{shift(-e["h"])})'
  equation=f'f({tex(x)}){shift(e["h"])}={tex(y)}'
 elif case['kind']=='horizontal_shift':
  undo=f'shift the graph horizontally by ${tex(abs(e["h"]))}$ '+('unit' if abs(e['h'])==1 else 'units')+' to the '+('right' if e['h']>0 else 'left')
  calculation=f'({tex(x)}{shift(e["h"])},{tex(y)})'
  equation=f'f({tex(x)}{shift(e["h"])})={tex(y)}'
 else:
  undo=f'stretch the graph by a scale factor of ${tex(1/e["a"])}$ parallel to the $y$-axis'
  calculation=f'({tex(x)},{tex(1/e["a"])}\\cdot ({tex(y)}))'
  equation=f'{coefficient(e["a"])}f({tex(x)})={tex(y)}'
 sol=f'''**Method 1**

We first find a point corresponding to ${pair((x,y))}$ on $y=f(x).$ Then, we find a corresponding point on $y={dst}:$

- First, take the graph $y={src}.$

- Then, we {undo} and get the graph of $y=f(x).$ After this transformation, the point ${pair((x,y))}$ will be mapped to the point

$$
{calculation}={pair((u,w))}.
$$

- Next, we reflect the result across the $x$-axis and get the graph of $y=-f(x).$ After this transformation, the point ${pair((u,w))}$ will be mapped to the point

$$
({tex(u)},-({tex(w)}))={pair((u,-w))}.
$$

- Next, we shift the result vertically by ${tex(abs(e['k']))}$ {'unit' if abs(e['k'])==1 else 'units'} {'up' if e['k']>0 else 'down'} and obtain the graph of $y={dst}.$ After this transformation, the point ${pair((u,-w))}$ will be mapped to the point

$$
({tex(u)},{tex(-w)}{shift(e['k'])})={pair((u,c))}.
$$

**Method 2**

Since the point ${pair((x,y))}$ lies on the graph of $y={src},$ we have that

$$
{equation}\\quad\\Longrightarrow\\quad f({tex(u)})={tex(w)}.
$$

Now consider the graph of $y={dst}.$ Substituting $x={tex(u)},$ we get

$$
\\begin{{aligned}}y&=-f({tex(u)}){shift(e['k'])}\\\\&=-({tex(w)}){shift(e['k'])}\\\\&={tex(c)}.\\end{{aligned}}
$$

Therefore, the point ${pair((u,c))}$ must lie on $y={dst}.$'''
 return prompt,sol,(u,c)
def bank(case,p):
 e=environment(case,p);return [tuple(sp.sympify(recipe,locals=e)) for recipe in case['bank']]
def fingerprint_prompt(prompt):
 # Full supplied and requested mathematical objects, never seed, labels or bank order.
 from importlib.util import spec_from_file_location,module_from_spec
 spec=spec_from_file_location('point_reader',D/'math_reader.py');m=module_from_spec(spec);spec.loader.exec_module(m)
 point,source,target=m.read_prompt(prompt)
 return digest([list(map(str,point)),str(source),str(target)])
def generate(level,seed=0,template=None,parameters=None,profile=None):
 if level not in SUPPORTED_LEVELS:raise ValueError('Unsupported difficulty: '+level)
 rng=random.Random(seed);eligible=[sid for sid,c in CASES.items() if c['level']==level and (template is None or c['kind']==template) and (profile is None or sid==profile)]
 if not eligible:raise ValueError('Unsupported template/profile')
 sid=rng.choice(eligible);case=CASES[sid]
 for attempt in range(300):
  p={key:rng.choice(domain(case,key)) for key in case['p']} if parameters is None else dict(parameters)
  if set(p)!=set(case['p']):raise ValueError('Parameter keys differ from declared slots')
  if any(val(p[key]) not in [val(z) for z in domain(case,key)] for key in p):
   # Original scale source y=8 is replayable outside the narrow normal domain.
   if {key:val(z) for key,z in p.items()}!={key:val(z) for key,z in case['p'].items()}:raise ValueError('Parameter outside supported domain')
  p={key:val(z) for key,z in p.items()};b=bank(case,p);prompt,sol,good=render(case,p)
  if len(set(b))!=5 or b.count(good)!=1:
   if parameters is not None:raise ValueError('Degenerate source bank')
   continue
  fp=fingerprint_prompt(prompt);qid=str(uuid.uuid5(uuid.UUID(KP_UUID),VERSION+':question:'+fp+':'+sid));fid=str(uuid.uuid5(uuid.UUID(qid),'selection'))
  answers=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),pair(z))),':answer/type':':answer.type/math',':answer/value':pair(z)} for z in b]
  correct=answers[b.index(good)][':answer/id'];rng.shuffle(answers)
  q={':question/id':qid,':question/problem':prompt,':question/worked-solution':sol,':question/difficulty':':question.difficulty/'+level,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]}]}
  return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'generator_version':VERSION,'level':level,'template':case['kind'],'bank_profile':sid,'source_references':[sid],'seed':seed,'parameters':{k:str(z) for k,z in p.items()},'mathematical_fingerprint':fp,'eligible_for_learning':True,'evidence_only':False,'dependencies':{'sympy':sp.__version__},'recipe_operations':case['bank']}}
 raise ValueError('Finite sampler budget exhausted')
def markdown(r):
 q=r['question'];return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$' for a in q[':question/answer-fields'][0][':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)
def generate_hard(seed=0,**kw):return generate('hard',seed,**kw)
def generate_easy(*a,**kw):raise ValueError('Easy unsupported: no classified complete source')
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',default='all',choices=['all','easy','moderate','hard']);ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--template');ap.add_argument('--profile');ap.add_argument('--parameters',type=json.loads);ap.add_argument('--format',choices=['json','markdown'],default='json');a=ap.parse_args()
 records=[generate(level,a.seed+i,a.template,a.parameters,a.profile) for level in (SUPPORTED_LEVELS if a.difficulty=='all' else [a.difficulty]) for i in range(a.count)]
 print(json.dumps(records,indent=2) if a.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
