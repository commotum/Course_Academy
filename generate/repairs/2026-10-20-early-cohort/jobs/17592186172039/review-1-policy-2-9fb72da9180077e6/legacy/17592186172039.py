#!/usr/bin/env python3
"""Quadrant slope signs, basis 1356; current checkbox source contract at basis 2771.

Observed bilinear/parity/numbered layouts and complete categorical banks replay
through the same parameterized renderer. No literal question-return branches.
Easy is a curriculum-anchored authored cx reduction. The authored default bank
complements all truth classifications or toggles exactly one statement, without
learner-facing diagnosis. authored_cycle is a compatibility alias for this bank,
not an adjacent-integer recipe. Hard varies exponent parity
only (1/2), not algebraic complexity. One fixed solution is stored per instance.
|c| is presentation variety, never mathematical-task variety. All quadrants are
open: axes are excluded. No translated rectangular regions or sums are admitted.
"""
from __future__ import annotations
import argparse, hashlib, json, random, subprocess, uuid
from pathlib import Path
import sympy as sp

KP_ID=17592186172039
KP_UUID='fd092f29-08bf-5425-88a4-8cba4f0a31c8'
TITLE='Identifying Quadrants Where a Slope Field Is Positive or Negative'
VERSION='quadrant-sign-checkbox-v3'
HERE=Path(__file__).resolve().parent / str(KP_ID)
SOURCE={'database':'math','basis':2771,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}
X,Y=sp.symbols('x y',real=True)
WORDS={1:'first',2:'second',3:'third',4:'fourth'}
POINTS={1:(1,1),2:(-1,1),3:(-1,-1),4:(1,-1)}
ROMAN=('I','II','III')
LABELS={0:'None of those listed',1:'I only',2:'II only',3:'I and II only',4:'III only',5:'I and III only',6:'II and III only',7:'I, II, and III'}
TEMPLATES={
 'single_coordinate':('easy',0,False,False),
 'bilinear_open_thin':('moderate',False,True,False),
 'bilinear_open':('moderate',False,False,False),
 'bilinear_closed':('moderate',True,False,False),
 'parity_open':('hard',False,False,False),
 'parity_closed':('hard',True,False,False),
 'parity_numbered':('hard',True,False,True),
}
# Categorical masks denote whole statement subsets, not guessed error intent.
PROFILES={
 'bank96767':(7,5,3,1,6), 'bank97483':(4,1,6,3,5),
 'bank119766':(3,6,1,7,2), 'bank119769':(0,2,1,4,3),
 'bank119774':(1,5,0,4,2), 'bank97477':(0,4,2,1,6),
 'bank97482':(4,1,2,6,5), 'bank97487':(4,6,7,1,3),
}
PLOT_REFS={
 (1,-1,1,-1):'images/6e/6ef852c9c15dc6f591119906abe479949f929edb6dc26f21588b4de545d02da2.png',
 (-1,1,-1,1):'images/2c/2c218c7df2bf4e159b4bffaccb4296beab8e3f44ab82d56b3589050af92ccf8e.png',
 (1,1,1,1):'images/d1/d1e4f48450a7f2032d755a5255d1a1e8a726dd16d273dae5dc1e587826d5ce58.png',
 (-1,1,1,-1):'images/96/96c937cf10d45d8870a4a56e257d184dcf2e4caf11312c05df9f385f9c5ee7a8.png',
}

def canonical(obj): return json.dumps(obj,sort_keys=True,separators=(',',':'))
def digest(obj): return hashlib.sha256(canonical(obj).encode()).hexdigest()
def uid(text): return str(uuid.uuid5(uuid.NAMESPACE_URL,f'{KP_ID}/{VERSION}/{text}'))
def monomial(p,numbered=False):
 c,a,b=p['c'],p['a'],p['b']
 coefficient=('-' if c<0 else '')+('' if abs(c)==1 else str(abs(c)))
 def term(v,n):
  if n==0:return ''
  if n==1:return v
  return v+'^{2}' if numbered else '{'+v+'}^{2}'
 return coefficient+term('x',a)+term('y',b)

def signs(p):
 f=sp.Integer(p['c'])*X**p['a']*Y**p['b']
 return tuple(int(sp.sign(f.subs({X:x,Y:y}))) for x,y in POINTS.values())

def truth_mask(p):
 ss=signs(p)
 return sum(1<<i for i,(q,claim) in enumerate(zip(p['quadrants'],p['claims'])) if ss[q-1]==claim)

def validate_parameters(level,p):
 if set(p)!={'c','a','b','quadrants','claims'}:raise ValueError('Exact parameter keys required')
 if any(type(p[k]) is not int for k in ('c','a','b')):raise ValueError('Integer coefficient/exponents required')
 if not 1<=abs(p['c'])<=9:raise ValueError('Nonzero coefficient magnitude 1..9')
 if level=='easy' and (p['a'],p['b'])!=(1,0):raise ValueError('Easy is cx only')
 if level=='moderate' and (p['a'],p['b'])!=(1,1):raise ValueError('Moderate is cxy only')
 if level=='hard' and (p['a'],p['b']) not in ((1,2),(2,1),(2,2)):raise ValueError('Hard has at least one squared factor, powers 1/2 only')
 if len(p['quadrants'])!=3 or len(set(p['quadrants']))!=3 or any(type(v) is not int or v not in WORDS for v in p['quadrants']):raise ValueError('Three distinct open quadrants required')
 if len(p['claims'])!=3 or any(type(v) is not int or v not in (-1,1) for v in p['claims']):raise ValueError('Three strict sign claims required')

def render_plots(p):
 """Finite sign maps reuse immutable source images; missing patterns use MPL.
 The renderer accepts this exact map, never samples. Fixed final filenames are
 atomic; immutable identical maps allow concurrent calls safely.
 """
 ss=signs(p)
 if ss in PLOT_REFS and p['b']>0:return PLOT_REFS[ss]
 rel='images/generated/signs-'+''.join('p' if s>0 else 'n' for s in ss)+('-zero-x' if p['b']==0 else '-zero-xy')+'.png'
 path=HERE/rel
 if not (path.exists() and path.with_suffix('.json').exists()): subprocess.run([str(Path(__file__).resolve().parents[2]/'.venv/bin/python'),str(HERE/'render.py'),json.dumps({'signs':ss,'zero_axes':['x'] if p['b']==0 else ['x','y']}),str(path)],check=True,capture_output=True,text=True)
 return rel

def sample(level,rng,profile):
 for _ in range(10000):
  a,b=(1,0) if level=='easy' else (1,1) if level=='moderate' else rng.choice([(1,2),(2,1),(2,2)])
  p={'c':rng.choice([-1,1])*rng.randint(1,9),'a':a,'b':b,'quadrants':rng.sample([1,2,3,4],3),'claims':[rng.choice([-1,1]) for _ in range(3)]}
  if profile in ('authored_sign_errors','authored_cycle') or truth_mask(p) in PROFILES[profile]: return p
 raise RuntimeError('No eligible whole bank')

def generate_legacy(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('Unknown level')
 if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Only observed radio layout is supported')
 rng=random.Random(seed)
 template=template or {'easy':'single_coordinate','moderate':'bilinear_closed','hard':'parity_closed'}[level]
 if template not in TEMPLATES or TEMPLATES[template][0]!=level:raise ValueError('Template is not eligible for level')
 profile=profile or 'authored_sign_errors'
 if profile not in PROFILES and profile not in ('authored_sign_errors','authored_cycle'):raise ValueError('Unknown profile')
 p=json.loads(json.dumps(parameters)) if parameters is not None else sample(level,rng,profile)
 validate_parameters(level,p)
 mask=truth_mask(p)
 authored=profile in ('authored_sign_errors','authored_cycle')
 bank=(mask,mask^7,mask^1,mask^2,mask^4) if authored else PROFILES[profile]
 operations=('correct truth subset','complement all three statement classifications','toggle only statement I','toggle only statement II','toggle only statement III') if authored else tuple('select statements encoded by this categorical bit mask' for _ in bank)
 if len(set(bank))!=5 or mask not in bank:raise ValueError('Whole bank is ineligible for this truth mask')
 _,closed,thin,numbered=TEMPLATES[template]
 expr=monomial(p,numbered)
 fraction=r'\frac{dy}{dx} = ' if numbered else r'\frac{\text{d}y}{\text{d}x}='
 prompt='Consider the differential equation $'+fraction+expr+'$ and its slope field. Which of the following statements are true?\n\n'
 prompt+='\n'.join((str(i+1)+'. ' if numbered else '- ')+'At every point in the '+WORDS[q]+' quadrant, the slope of the slope field is '+('positive' if claim>0 else 'negative') for i,(q,claim) in enumerate(zip(p['quadrants'],p['claims'])))
 # Exactly preserve the observed ordered shared solution; the missing source
 # numbered solution is explicitly authored from the same instructional sequence.
 solution='First, we define $f(x,y)='+expr+'.$ Then, our differential equation is $'+r'\frac{\text{d}y}{\text{d}x}=f(x,y).$ '+'\n\n'
 if level=='easy':
  solution+='Notice that $f(x,y)=0$ when $x=0.$ In each open quadrant, $x$ has a fixed nonzero sign. The lines $x=0$ and $y=0$ divide the plane into the usual four quadrants.\n\n'
 else:solution+='Notice that $f(x,y)=0$ when $x=0$ or $y=0.$ The lines $x=0$ and $y=0$ divide the plane into the usual four quadrants.\n\n'
 if authored and level=='hard':solution+='In an open quadrant, each squared coordinate is positive, so the remaining coordinate factors and coefficient determine the sign.\n\n'
 solution+='If we compute the sign of $f(x,y)$ in each quadrant (by considering some test points, for example), we get the following:\n\n![]('+render_plots(p)+')\n\nWith that in mind, let\'s check each statement:\n\n'
 ss=signs(p)
 blocks=[]
 for i,q in enumerate(p['quadrants']):
  s=ss[q-1]
  blocks.append('- Statement '+ROMAN[i]+' is '+('true' if mask&(1<<i) else 'false')+'. If $(x,y)$ is in the '+WORDS[q]+' quadrant, then according to our diagram, we have\n\n$$\n'+r'{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)'+('>' if s>0 else '<')+'0.'+(r'\,' if thin else '')+'\n$$\n\nThis implies that the slope of the slope field is '+('positive' if s>0 else 'negative')+' for any point $(x,y)$ in the '+WORDS[q]+' quadrant.')
 solution+='\n\n'.join(blocks)
 if closed:solution+='\n\nTherefore, the correct answer is "'+LABELS[mask]+'."'
 values=[LABELS[m] for m in bank]
 mathematical={'coefficient_sign':1 if p['c']>0 else -1,'exponents':[p['a'],p['b']],'statements':sorted(zip(p['quadrants'],p['claims']))}
 identity=digest({'version':VERSION,'level':level,'template':template,'parameters':p,'prompt':prompt,'solution':solution,'bank':sorted(values),'domain':'open quadrants'})
 qid=uid('question/'+identity);fid=uid(qid+'/selection')
 answers=[{':answer/id':uid(fid+'/'+value),':answer/type':':answer.type/text',':answer/value':value} for value in values]
 correct=next(a[':answer/id'] for a in answers if a[':answer/value']==LABELS[mask])
 rng.shuffle(answers)
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]}]},'generation':{'version':VERSION,'source':SOURCE,'template':template,'level':level,'seed':seed,'parameters':p,'bank_profile':profile,'bank_recipes':[{'mask':m,'operation':op} for m,op in zip(bank,operations)],'truth_mask':mask,'mathematical_fingerprint':digest(mathematical),'content_identity':identity,'domain':'Four open quadrants: x and y are nonzero, axes excluded.','plot':{'role':'solution','asset':render_plots(p),'signs':ss,'renderer':'immutable source asset' if ss in PLOT_REFS and p['b']>0 else 'Matplotlib cached fallback'},'authored':authored or level=='easy' or template=='parity_numbered','dependencies':{'sympy':sp.__version__}}}

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 """Current source contract: one checkbox per statement, with boolean banks.
 Legacy five-option banks are retained only for historical evidence replay.
 """
 if field_type not in (None,'checkbox',':answer-field.type/checkbox'):
  raise ValueError('Current source contract requires three checkbox fields')
 if template=='parity_numbered':
  if parameters is None:
   parameters=sample(level,random.Random(seed),profile or 'authored_sign_errors');parameters.update(a=1,b=2)
  if (parameters['a'],parameters['b'])!=(1,2):raise ValueError('Numbered source uses cx times y squared')
 r=generate_legacy(level,seed,template,None,parameters,profile)
 q=r['question'];gen=r['generation']
 if gen['template']=='parity_numbered':
  p=gen['parameters'];ss=signs(p);expr=monomial(p,True).replace('{','').replace('}','')
  q[':question/worked-solution']='For '+expr+', y^2 is positive in every open quadrant, so the slope has '+('the sign of x' if p['c']>0 else 'the opposite sign to x')+'. '
  groups=[]
  for sign in (-1,1):
   names=[('I','II','III','IV')[q-1] for q in sorted(p['quadrants']) if ss[q-1]==sign]
   if names:groups.append(('negative' if sign<0 else 'positive')+' in quadrant'+('s ' if len(names)>1 else ' ')+(' and '.join(names) if len(names)<3 else ', '.join(names[:-1])+', and '+names[-1]))
  q[':question/worked-solution']+='It is '+', and '.join(groups)+'.'
 lines=q[':question/problem'].splitlines()
 claims=[line[line.index('At every point'):] for line in lines if 'At every point' in line]
 q[':question/problem']=lines[0]+'\n\nSelect all that apply.\n\n'+'\n'.join('- **'+roman+'.** '+claim for roman,claim in zip(ROMAN,claims))
 identity=digest({'version':VERSION,'level':level,'prompt':q[':question/problem']})
 qid=uid('question/'+identity);q[':question/id']=qid;fields=[]
 for i,key in enumerate(ROMAN):
  fid=uid(qid+'/'+key)
  answers=[{':answer/id':uid(fid+'/'+value),':answer/type':':answer.type/text',':answer/value':value} for value in ('false','true')]
  correct=answers[1 if gen['truth_mask']&(1<<i) else 0][':answer/id']
  fields.append({':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/checkbox',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]})
 q[':question/answer-fields']=fields
 gen['legacy_bank_profile']=gen['bank_profile'];gen['bank_profile']='checkbox_boolean'
 gen['bank_recipes']=[{'field':key,'values':['false','true'],'correct':bool(gen['truth_mask']&(1<<i))} for i,key in enumerate(ROMAN)]
 gen['content_identity']=identity
 return r

def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)

def markdown(record):
 q=record['question'];f=q[':question/answer-fields'][0]
 return q[':question/problem']+'\n\n'+'\n'.join('- '+a[':answer/value'] for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']

def main():
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=1);parser.add_argument('--format',choices=['markdown','json'],default='markdown');parser.add_argument('--template');parser.add_argument('--profile')
 args=parser.parse_args()
 if args.count<1:parser.error('count must be positive')
 levels=['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]
 records=[generate(level,args.seed+i,template=args.template,profile=args.profile) for level in levels for i in range(args.count)]
 print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))

# Every learner-facing checkbox question has a nonempty correct selection.
import sys as _policy_sys
from pathlib import Path as _PolicyPath
_policy_sys.path.insert(0, str(next(p for p in _PolicyPath(__file__).resolve().parents if (p / "scripts/generator_policy.py").is_file())))
from scripts.generator_policy import nonempty_checkbox as _nonempty_checkbox
for _policy_name in ['generate', 'generate_easy', 'generate_hard', 'generate_legacy', 'generate_moderate']:
    globals()[_policy_name] = _nonempty_checkbox(globals()[_policy_name], none_label='None of the above')

if __name__=='__main__':main()
