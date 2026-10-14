#!/usr/bin/env python3
"""Source-profile extrema transformations; finite exact domains, owned radio banks."""
import argparse,hashlib,json,random,uuid
from pathlib import Path
import sympy as sp
KP_ID=17592186059670
KP_UUID='e6eef35a-3502-5429-bd71-fb5bd0e8efc8'
TITLE='Identifying Extrema on Transformed Curves'
VERSION='1.0.0'
SUPPORTED_LEVELS=('easy','moderate')
D=Path(__file__).with_suffix('')
SOURCE=json.loads((D/'source.json').read_text())
ORIGINALS={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
# x,y denote the selected original extremum; u,v denote the other extremum.
# Opaque banks are literal parameterized value patterns, not inferred error intent.
CASES={
'q-121221':dict(level='easy',kind='shift_shift',scope='local',target='maximum',minimum=[-1,1],maximum=[2,3],p=dict(h=-2,k=1),bank=['(x-h,y+k)','(x+k,y-h)','(y-h,x+k)','(x+k,y-k)','(x+h,y+k)']),
'q-211288':dict(level='easy',kind='shift_scale',scope='global',target='minimum',minimum=[-2,-4],maximum=[2,2],p=dict(h=-5,s='1/2'),bank=['(x-h,s*y)','(x+h,s*y)','(x+h,y/s)','(x-h,y/s)','(s*x,s*v)']),
'q-186866':dict(level='moderate',kind='shift_scale_flip',scope='global',target='minimum',minimum=[2,-3],maximum=[-1,4],p=dict(h=1,s=2),bank=['(x-h,-s*y)','(u+h,-y)','(x-h,s*y)','(x+h,-y)','(-x+h,s*y)']),
'q-211303':dict(level='moderate',kind='scale_flip_shift',scope='local',target='maximum',minimum=[4,-1],maximum=[-3,6],p=dict(s=3,k=-1),bank=['(x,-s*y+k)','(-x,-s*y+k)','(x-s,y-k)','(x,s*y+2*k)','(x-s,s*y+2*k)']),
'q-211462':dict(level='moderate',kind='hscale_flip_shift',scope='global',target='maximum',minimum=[2,3],maximum=[-4,9],p=dict(t=2,k=3),bank=['(x/t,-y+k)','(x*t,y+k)','(x*t,-y+k)','(x/t,-y)','(x,y+k)']),
'q-211465':dict(level='moderate',kind='shift_flip_shift',scope='local',target='minimum',minimum=[-1,1],maximum=[2,3],p=dict(h=-1,k=-2),bank=['(x-h,-y+k)','(x-h,k)','(-(x-h),v)','(x,-y+k)','(x,v)']),
'q-211466':dict(level='moderate',kind='hscale_scale_flip',scope='global',target='minimum',minimum=[-3,-2],maximum=[3,1],p=dict(t=3,s=4),bank=['(x/t,-s*y)','(x/t,x)','(x,y)','(x,-s*y)','(0,x)']),
'q-211467':dict(level='moderate',kind='shift_flip_shift',scope='local',target='maximum',minimum=[1,-4],maximum=[-2,-1],p=dict(h=2,k=4),bank=['(x-h,-y+k)','(h,y+k)','(h,-v+k)','(x+h,-y+k)','(x-h,y+k)']),
}
FIELDLESS={
'q-211287':dict(kind='shift_shift',scope='local',target='maximum',minimum=[6,-7],maximum=[-2,6],p=dict(h=3,k=-2)),
'q-211304':dict(kind='hscale_shift',scope='global',target='minimum',minimum=[15,-5],maximum=[3,5],p=dict(t=3,k=4)),
'q-211305':dict(kind='hscale_scale',scope='local',target='maximum',minimum=[1,-4],maximum=[-2,-1],p=dict(t='1/2',s=3)),
'q-211461':dict(kind='scale_shift',scope='global',target='minimum',minimum=[4,-5],maximum=[-4,8],p=dict(s=2,k=5)),
}
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def val(x):return sp.Rational(x)
def tex(x):return sp.latex(val(x))
def pair(z):return '('+','.join(tex(x) for x in z)+')'
def opposite(x):return 'maximum' if x=='minimum' else 'minimum'
def shift(z):return ('+' if z>0 else '-')+tex(abs(z)) if z else ''
def coeff(z):return '' if z==1 else '-' if z==-1 else tex(z)
def env(case,p,target):
 source=opposite(target) if case['level']=='moderate' else target
 x,y=case[source];u,v=case[opposite(source)]
 return dict(x=val(x),y=val(y),u=val(u),v=val(v),**{key:val(p.get(key,default)) for key,default in [('h',0),('k',0),('s',1),('t',1)]})
def bank(case,p,target):
 e=env(case,p,target)
 return [tuple(sp.sympify(z,locals=e)) for z in case['bank']]
def expressions(case,p):
 e={key:val(p.get(key,default)) for key,default in [('h',0),('k',0),('s',1),('t',1)]};kind=case['kind']
 inside=(('x'+shift(e['h'])) if 'shift'==kind.split('_')[0] else (coeff(e['t'])+'x' if 'hscale'==kind.split('_')[0] else 'x'))
 base='f('+inside+')';steps=[]
 if kind.startswith('shift_'):steps.append(('hshift',base))
 elif kind.startswith('hscale_'):steps.append(('hscale',base))
 else:base='f(x)'
 if 'scale' in kind.split('_') or kind.startswith('scale_'):
  base=coeff(e['s'])+base;steps.append(('vscale',base))
 if case['level']=='moderate':base='-'+base;steps.append(('flip',base))
 if kind.endswith('_shift') or kind=='shift_flip_shift':base+=shift(e['k']);steps.append(('vshift',base))
 return base,steps

def render(case,p,target):
 e=env(case,p,target);x,y=e['x'],e['y'];expr,steps=expressions(case,p)
 import re
 image=re.search(r'!\[\]\((.*?)\)',ORIGINALS[case['source_id']][':question/problem'])[1]
 prompt=f'![]({image})\n\nThe diagram above shows the {case["scope"]} minimum and maximum of the function $y=f(x).$ What is the {case["scope"]} {target} of $y={expr}?$'
 point=(x,y);descriptions=[];calculations=[]
 for op,stage in steps:
  old=point
  if op=='hshift':
   point=(point[0]-e['h'],point[1]);desc=f'translating it by ${tex(abs(e["h"]))}$ '+('unit' if abs(e['h'])==1 else 'units')+' to the '+('left' if e['h']>0 else 'right');calc=f'({tex(old[0])}{shift(-e["h"])},{tex(old[1])})'
  elif op=='hscale':
   point=(point[0]/e['t'],point[1]);desc=f'stretching it by a scale factor of ${tex(1/e["t"])}$ parallel to the $x$-axis';calc=f'({tex(1/e["t"])}\\cdot ({tex(old[0])}),{tex(old[1])})'
  elif op=='vscale':
   point=(point[0],point[1]*e['s']);desc=f'stretching it by a scale factor of ${tex(e["s"])}$ parallel to the $y$-axis';calc=f'({tex(old[0])},{tex(e["s"])}\\cdot ({tex(old[1])}))'
  elif op=='flip':
   point=(point[0],-point[1]);desc='flipping it across the $x$-axis';calc=f'({tex(old[0])},-1\\cdot ({tex(old[1])}))'
  else:
   point=(point[0],point[1]+e['k']);desc=f'translating it by ${tex(abs(e["k"]))}$ '+('unit' if abs(e['k'])==1 else 'units')+' '+('up' if e['k']>0 else 'down');calc=f'({tex(old[0])},{tex(old[1])}{shift(e["k"])})'
  descriptions.append('- '+desc+'.')
  calculations.append(f'- Then, we apply the transformation by {desc.replace("it", "the graph",1)} and get the graph of $y={stage}.$ After this transformation, the point ${pair(old)}$ will be mapped to the point\n\n$$\n{calc}={pair(point)}.\n$$')
 source=opposite(target) if case['level']=='moderate' else target
 reflection=('one of these transformations flips' if case['level']=='moderate' else 'these transformations do not flip')
 sol=f'Notice that the graph of $y={expr}$ can be obtained from the graph of $y=f(x)$ by\n\n'+ '\n\n'.join(descriptions)+f'\n\nSince {reflection} the graph across the $x$-axis, the combined transformation maps the {case["scope"]} {source} of $y=f(x)$ to the {case["scope"]} {target} of $y={expr}.$ So, we need to find the image of ${pair((x,y))},$ the {case["scope"]} {source} of $y=f(x),$ under the transformation.\n\nTo plot $y={expr},$ we apply the following steps:\n\n- First, we take the graph $y=f(x)$ that passes through ${pair((x,y))}.$\n\n'+'\n\n'.join(calculations)+f'\n\nTherefore, the {case["scope"]} {target} of $y={expr}$ is ${pair(point)}.$'
 return prompt,sol,point,image

def generate(level,seed=0,template=None,parameters=None,profile=None):
 if level not in SUPPORTED_LEVELS:raise ValueError('Unsupported difficulty: '+level)
 rng=random.Random(seed);eligible=[sid for sid,c in CASES.items() if c['level']==level and (template is None or c['kind']==template)]
 if profile:eligible=[sid for sid in eligible if sid==profile]
 if not eligible:raise ValueError('Unsupported template/profile')
 sid=rng.choice(eligible);case=dict(CASES[sid],source_id=sid)
 for attempt in range(200):
  if parameters is None:
   p={key:rng.choice([-5,-4,-3,-2,-1,1,2,3,4,5] if key in ('h','k') else ['1/2','1/3',2,3,4] if level=='easy' else [2,3,4]) for key in case['p']};target=rng.choice(['minimum','maximum'])
  else:p=dict(parameters);target=p.pop('target',case['target'])
  if target not in ('minimum','maximum') or set(p)!=set(case['p']):raise ValueError('Invalid parameter keys or target')
  for key,z in p.items():
   allowed=[-5,-4,-3,-2,-1,1,2,3,4,5] if key in ('h','k') else ['1/2','1/3',2,3,4] if level=='easy' else [2,3,4]
   if val(z) not in [val(a) for a in allowed]:raise ValueError('Parameter outside supported finite domain')
  b=bank(case,p,target)
  if len(set(b))!=5:
   if parameters is not None:raise ValueError('Degenerate source bank')
   continue
  prompt,solution,correct,image=render(case,p,target);assert b[0]==correct
  p={key:str(val(z)) for key,z in p.items()};p['target']=target
  mathematical_fingerprint=fingerprint_prompt(prompt)
  qid=str(uuid.uuid5(uuid.UUID(KP_UUID),VERSION+':question:'+mathematical_fingerprint+':'+sid));fid=str(uuid.uuid5(uuid.UUID(qid),'selection'))
  answers=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),pair(z))),':answer/type':':answer.type/math',':answer/value':pair(z)} for z in b]
  aid=answers[0][':answer/id'];rng.shuffle(answers)
  q={':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',aid]}]}
  return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'generator_version':VERSION,'level':level,'template':case['kind'],'bank_profile':sid,'source_references':[sid],'seed':seed,'parameters':p,'mathematical_fingerprint':mathematical_fingerprint,'eligible_for_learning':True,'evidence_only':False,'asset':image,'asset_sha256':hashlib.sha256((Path('/media/jake/SSD/EDB/math')/image).read_bytes()).hexdigest(),'dependencies':{'sympy':sp.__version__},'recipe_operations':case['bank']}}
 raise ValueError('Finite sampler budget exhausted')

def fingerprint_prompt(prompt):
 # Canonicalize the transformation algebra so different profiles/notation cannot
 # create new inventory solely through identity or bank order.
 import re
 image=re.search(r'!\[\]\((.*?)\)',prompt)[1];scope,target=re.search(r'What is the (local|global) (minimum|maximum)',prompt).groups()
 expression=re.search(r'What is.*?\$y=(.*?)\?\$',prompt,re.S)[1].replace('\\frac{1}{2}','(1/2)').replace('\\frac{1}{3}','(1/3)').replace('\\frac{1}{4}','(1/4)')
 expression=re.sub(r'\\(?:d?frac)\s*\{([^{}]+)\}\s*\{([^{}]+)\}',r'((\1)/(\2))',expression)
 expression=re.sub(r'\s+','',expression)
 left,inside,right=re.fullmatch(r'(.*?)f\((.*)\)([^)]*)',expression).groups();x=sp.Symbol('x')
 def parse(z):return sp.sympify(re.sub(r'(?<=[\d)])(?=[x(])','*',z),locals={'x':x})
 a=sp.sympify(1 if left=='' else -1 if left=='-' else left);b=sp.expand(parse(inside));k=val(right or 0)
 return digest([image,scope,target,str(a),str(b.coeff(x)),str(b.subs(x,0)),str(k)])

def markdown(r):
 q=r['question'];return q[':question/problem']+'\n\n'+ '\n'.join('- $'+a[':answer/value']+'$' for a in q[':question/answer-fields'][0][':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)
def generate_hard(*a,**kw):raise ValueError('Hard unsupported by observed source backbone')
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',default='all',choices=['all','easy','moderate','hard']);ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--template');ap.add_argument('--profile');ap.add_argument('--parameters',type=json.loads);ap.add_argument('--format',choices=['json','markdown'],default='json');a=ap.parse_args()
 records=[generate(level,a.seed+i,a.template,a.parameters,a.profile) for level in (SUPPORTED_LEVELS if a.difficulty=='all' else [a.difficulty]) for i in range(a.count)]
 print(json.dumps(records,indent=2) if a.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
