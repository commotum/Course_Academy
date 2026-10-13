#!/usr/bin/env python3
"""Direction-reversal scalar factors, math basis1356. Steps3–7 only.

All sources share one path-tracing solution. No coordinates are shown or solved:
the renderer's coordinates define exact grid geometry. Profiles q-* preserve
complete observed banks using documented expressions; their distractor intent is
not claimed. Normal banks are separately authored method-based operations.
Easy is authored, not observed: +b, integral reversed a, a along a grid axis.
Moderate retains positive known multiple; hard retains negative known multiple
and permits half-integral reversed magnitude. All explicit inputs obey bounds.
Source prompt layouts and solution final punctuation are separately named masks.
Content UUIDs depend on actual display and full bank, not seed or profile alias.
"""
from __future__ import annotations
import argparse,hashlib,json,random,re,subprocess,tempfile,uuid,os
from pathlib import Path
import sympy as sp
KP_ID=17592186235285
KP_UUID='58a49d00-cc58-5228-af38-9369cf31d8c8'
TITLE='Finding a Scalar Factor When Direction Reverses'
VERSION='direction-reversal-v1'
HERE=Path(__file__).resolve().parent/str(KP_ID)
SOURCE={'database':'math','basis':1356,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}
RUNTIME='/home/jake/.local/share/uv/python/cpython-3.10.13-linux-x86_64-gnu/bin/python3.10'
# Whole observed profiles; numerical intent remains underdetermined where noted.
PROFILES={
'q-120254':['r-1/2','-r-1','r','-r','-r+1/2'],
'q-120257':['r','-2*r','1/r','2*r','-r'],
'q-120260':['-r+3/2','-r+1/2','-r+2','-r','-r+1'],
'q-367051':['-r/k','k','r','-k','-r'],
'q-367052':['-r','r','-2*r','1','-1/r'],
'q-367060':['-r-1/2','-r','-r+1/2','-r+1','-r-1'],
'q-70148':['r-1','-r+1','-r','r','-r+1/2'],
'q-77451':['-r','3*r/2','1/r','-1/r','r'],
'authored':['-r','r','-1/r','1/r','-r-1'],
'blank':['-r']}
# Scope/layout tables are extracted masks, not source-payload branches.
TEMPLATES={'radio': 'radio','blank_standard':'blank','blank_inline':'blank','blank_runon':'blank'}
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(x):return str(uuid.uuid5(uuid.UUID(KP_UUID),str(x)))
def tex(x,style='fraction'):
 x=sp.Rational(x)
 if style=='decimal' and x.q in (1,2):return str(int(x)) if x.q==1 else str(float(x))
 return str(x) if x.q==1 else ('-' if x<0 else '')+rf'\frac{{{abs(x.p)}}}{{{x.q}}}'
def term(x,var,style='fraction'):
 x=sp.Rational(x);return ('-' if x==-1 else '' if x==1 else tex(x,style))+var
def parse(s):
 s=s.replace('\\\\','\\');s=re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}',r'(\1)/(\2)',s);return sp.Rational(sp.sympify(s))
def render_plots(p,output_dir=None):
 assets={}
 for role in ('prompt','solution'):
  data={'renderer_version':'grid-path-v1','a':p['a'],'b':p['b'],'k':str(p['k']),'r':str(p['r']),'k_label':('-' if p['k']==-1 else '' if p['k']==1 else tex(p['k'])),'role':role}
  out=(Path(output_dir) if output_dir is not None else HERE/'assets')/f'{digest(data)[:24]}-{role}.png'
  if not(out.exists() and out.with_suffix('.json').exists()):
   fd,inp=tempfile.mkstemp(prefix='render-input-',suffix='.json',dir=HERE)
   try:
    with os.fdopen(fd,'w') as f:json.dump(dict(data,out=str(out)),f)
    subprocess.run([RUNTIME,str(HERE/'render.py'),inp],check=True,capture_output=True)
   finally:os.unlink(inp)
  assets[role]=str(out)
 return assets

def sample(level,rng,field):
 # Easy: single known unit term; moderate: positive repeated known term;
 # hard: reversed known term and half/integer unknown. No within-level progression.
 k=1 if level=='easy' else rng.choice([2,3,4] if level=='moderate' else [1,2,3,4])*(1 if level=='moderate' else -1)
 rs=[1,2,3,4] if level!='hard' else [sp.Rational(1,2),1,sp.Rational(3,2),2,sp.Rational(5,2),3,sp.Rational(7,2),4]
 if field=='radio':rs=[r for r in rs if r!=1]
 r=rng.choice(rs);a=rng.choice([[0,-2],[0,2],[-2,0],[2,0]]) if level=='easy' else rng.choice([[0,-2],[-2,0],[2,0],[2,-2]])
 b=rng.choice([[1,1],[1,2],[-1,2],[-1,-1]])
 while sp.det(sp.Matrix.hstack(sp.Matrix(a),sp.Matrix(b)))==0:b=rng.choice([[1,1],[1,2],[-1,2],[-1,-1]])
 return {'r':str(r),'k':str(k),'a':a,'b':b}

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('Unknown level')
 rng=random.Random(seed)
 field=field_type or (TEMPLATES.get(template) if template else None) or ('blank' if profile=='blank' else 'radio' if profile else None) or rng.choice(['radio','blank'])
 field=field.rsplit('/',1)[-1]
 if field not in ('radio','blank'):raise ValueError('Unsupported field')
 template=template or ('radio' if field=='radio' else 'blank_runon')
 if template not in TEMPLATES or TEMPLATES[template]!=field:raise ValueError('Incompatible template')
 profile=profile or ('authored' if field=='radio' else 'blank')
 if profile not in PROFILES or (field=='blank')!=(profile=='blank'):raise ValueError('Incompatible profile')
 explicit=parameters is not None
 for _ in range(500):
  p=dict(parameters) if explicit else sample(level,rng,field)
  if set(p)-{'r','k','a','b','ratio_style','answer_style','final_dot','source_assets'}:raise ValueError('Unknown parameter')
  p['r']=sp.Rational(p['r']);p['k']=sp.Rational(p['k']);r=p['r'];k=p['k']
  if not(0<r<=4 and r.q in (1,2)):raise ValueError('Unknown magnitude outside level scope')
  if level=='easy' and (k!=1 or r.q!=1):raise ValueError('Easy requires +b and integral magnitude')
  if level=='moderate' and (k not in (2,3,4) or r.q!=1):raise ValueError('Moderate requires positive 2–4b and integral magnitude')
  if level=='hard' and k not in (-1,-2,-3,-4):raise ValueError('Hard requires negative known coefficient')
  a=sp.Matrix(p['a']);b=sp.Matrix(p['b'])
  if len(a)!=2 or len(b)!=2 or any(not x.is_Integer or abs(x)>6 for x in list(a)+list(b)) or sp.det(sp.Matrix.hstack(a,b))==0:raise ValueError('Vectors must be independent integer grid displacements of magnitude at most6')
  if level=='easy' and sum(x!=0 for x in a)!=1:raise ValueError('Easy a must follow grid axis')
  if any(not x.is_Integer for x in -r*a):raise ValueError('Residual must fall on grid intersections')
  values=[sp.Rational(sp.sympify(expr,locals={'r':r,'k':k})) for expr in PROFILES[profile]]
  if len(set(values))==len(values) and values.count(-r)==1:break
  if explicit:raise ValueError('Whole bank is ambiguous')
 else:raise ValueError('Unable to sample eligible whole bank')
 ratio_style=p.get('ratio_style','fraction');answer_style=p.get('answer_style','fraction');dot=p.get('final_dot',False)
 if 'source_assets' in p:
  cases=json.loads((HERE/'source-cases.json').read_text())
  comparable=dict(p,r=str(r),k=str(k))
  if not any(c['parameters']==comparable and c['level']==level and c['template']==template for c in cases):raise ValueError('Source assets require an original verified geometry/layout')
 assets=render_plots(p) if 'source_assets' not in p else p['source_assets']
 kb=term(k,'b');rb=term(-r,'a',ratio_style);eq=r'c=\lambda a'+('+' if k>0 else '')+kb
 if template=='radio':end=rf'Consider the picture above. Given that ${eq},$ find $\lambda .$'
 elif template=='blank_standard':end=rf'Consider the picture above. If ${eq},$ then'+'\n\n'+r'$\lambda =$'+'\n{{field-1}}.'
 elif template=='blank_inline':end=rf'Consider the picture above. If ${eq},$ then$\,\lambda =$'+'\n{{field-1}}.'
 else:end=rf'Consider the picture above. If ${eq},$ then$\,\lambda =$'+'\n{{field-1}}.'
 prompt=f'![]({assets["prompt"]})\n\n'+end
 mag='' if r==1 else tex(r,ratio_style)
 decomp=kb+rb
 final=rb+('+' if k>0 else '')+kb
 solution=rf'''To find $\lambda ,$ we want to match the expression

$$
{eq}.
$$

We are given that one of the components is ${kb}.$ So, we first draw the vector ${kb}$ from the origin. Then we complete the path to the point $C.$

![]({assets['solution']})

Let $P$ be the endpoint of the vector ${kb}.$ Then

$$
c=\overset{{\to }}{{OP}}+\overset{{\to }}{{PC}}.
$$

In $△OPC,$ we have:

- $PC={mag}|a|$

- $\overset{{\to }}{{PC}}$ and $a$ have opposite directions

Hence, $\overset{{\to }}{{PC}}={rb}.$

Additionally,

$$
\begin{{aligned}}c & =\overset{{\to }}{{OP}}+\overset{{\to }}{{PC}} \\  & ={decomp}.\end{{aligned}}
$$

Consequently, ${eq}={final}.$

Since $a∦b,$ the linear combination can only be written in one way. Equating the coefficients of $a,$ we get:

$$
\lambda ={tex(-r,ratio_style)}{'.' if dot else ''}
$$'''
 if isinstance(answer_style,list) and len(answer_style)!=len(values):raise ValueError('Style profile must cover whole bank')
 answer_values=[tex(v,answer_style[i] if isinstance(answer_style,list) else answer_style) for i,v in enumerate(values)] if field=='radio' else [str(-r)]
 identity=digest({'version':VERSION,'prompt':prompt,'solution':solution,'field':field,'values':sorted(answer_values)})
 fid=uid(identity+':field');answers=[{':answer/id':uid(fid+':'+str(v)),':answer/type':':answer.type/math',':answer/value':t} for v,t in zip(values,answer_values)]
 correct=answers[values.index(-r)][':answer/id'];rng.shuffle(answers)
 f={':answer-field/id':fid,':answer-field/key':'selection' if field=='radio' else 'field-1',':answer-field/type':':answer-field.type/'+field,':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]}
 q={':question/id':uid(identity),':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':[f]}
 # Grid displacement ratio and known coefficient are substantive. Common scale is removed.
 vector_gcd=sp.gcd_list(list(a)+list(b));geom=[str(x/vector_gcd) for x in list(a)+list(b)]
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'template':template,'bank_profile':profile,'parameters':dict(p,r=str(r),k=str(k)),'recipes':PROFILES[profile],'source':SOURCE,'authored_easy':level=='easy','authored_bank':profile=='authored','plot_assets':assets,'mathematical_fingerprint':digest([str(r),str(k),geom]),'content_fingerprint':identity}}

# Easy: explicitly authored one-unit known term, integer reversal.
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
# Moderate: observed positive known multiples, integral reversal.
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
# Hard: observed negative known multiples, integer or half-integer reversal.
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=2);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template',choices=list(TEMPLATES));ap.add_argument('--profile',choices=list(PROFILES));ns=ap.parse_args()
 rs=[generate(level,ns.seed+i,template=ns.template,profile=ns.profile) for level in (['easy','moderate','hard'] if ns.difficulty=='all' else [ns.difficulty]) for i in range(ns.count)]
 if ns.format=='json':print(json.dumps(rs,indent=2))
 else:
  for obj in rs:
   print(obj['question'][':question/problem']);print('\nOptions:',[a[':answer/value'] for a in obj['question'][':question/answer-fields'][0][':answer-field/choices']]);print('\n'+obj['question'][':question/worked-solution']+'\n')
