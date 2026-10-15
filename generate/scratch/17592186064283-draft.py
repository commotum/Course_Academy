#!/usr/bin/env python3
"""Basis-2275 private power-of-trig draft. Complete source component masks."""
import argparse,copy,hashlib,importlib.util,json,random,sys,uuid
from pathlib import Path
import sympy as s
KP_ID=17592186064283;KP_UUID='3ec11481-cea2-514b-aa78-707fcf8838cc';TITLE='Differentiating a Power of a Trigonometric Function Using the Chain Rule'
HERE=Path(__file__).with_suffix('');VERSION='trig-power-v2-draft';SUPPORTED_LEVELS=('easy','moderate','hard')
spc=importlib.util.spec_from_file_location('math_format',HERE.parents[2]/'scripts/question_capture/math_format.py');math_format=importlib.util.module_from_spec(spc);spc.loader.exec_module(math_format)
T=json.loads((HERE/'template-components.json').read_text());LEVELS={m:t['level'] for m,t in T.items()};LEVELS['authored-csc-power']='hard'
x,u=s.symbols('x u',real=True)
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def tex(e):return s.latex(e)
def parameters_for(m):
 if m=='authored-csc-power':return [{'c':c,'n':n} for c in range(-9,-1) for n in range(3,9)]
 t=T[m];c0=t['defaults']['c'];n0=t['defaults']['n'];cs=[1] if c0==1 else range(2,10) if c0>0 else range(-9,-1)
 ns=[n0] if m in ('q-72154','q-48560','q-143516','q-167568') else range(3,9)
 return [{'c':c,'n':n} for c in cs for n in ns]
def render(text,p):
 for a,b in {'C':abs(p['c']),'N':p['n'],'M':p['n']-1,'K':abs(p['c']*p['n'])}.items():text=text.replace('@@'+a+'@@',str(b))
 return text

def authored(p):
 c,n=p['c'],p['n'];inner=s.csc(x);outer=c*u**n;od=s.diff(outer,u);di=s.diff(inner,x);df=s.diff(c*inner**n,x)
 prompt=f'Given that $f(x)={c}\\csc^{{{n}}}(x),$ we have\n\n$f\'(x)=$\n{{{{field-1}}}}.'
 sol=('First, we express\n\n$$\nf(x)='+tex(c*inner**n)+'.\n$$\n\nNow, we see that $f(x)$ can be expressed as the composite function\n\n$$\nf='+tex(outer)+r',\qquad u='+tex(inner)+'.\n$$\n\nDifferentiating, we get\n\n$$\n'+r'\frac{\text{d}f}{\text{d}u}='+tex(od)+r',\qquad \frac{\text{d}u}{\text{d}x}='+tex(di)+'.\n$$\n\nWe now apply the chain rule, and get\n\n$$\n'+r'\begin{aligned}f\'(x)&=\frac{\text{d}f}{\text{d}u}\cdot\frac{\text{d}u}{\text{d}x}\\&=('+tex(od)+r')\cdot('+tex(di)+r')\\&='+tex(df)+r'.\end{aligned}'+'\n$$')
 return prompt,sol,[tex(df)]
def completed_cos_solution(p):
 c,n=p['c'],p['n'];inner=s.cos(x);outer=c*u**n;od=s.diff(outer,u);di=s.diff(inner,x)
 return ('First, we express\n\n$$\nf(x)='+tex(c*inner**n)+'.\n$$\n\nNow, we see that $f(x)$ can be expressed as the composite function\n\n$$\nf='+tex(outer)+r',\qquad u='+tex(inner)+'.\n$$\n\nDifferentiating, we get\n\n$$\n'+r'\frac{\text{d}f}{\text{d}u}='+tex(od)+r',\qquad \frac{\text{d}u}{\text{d}x}='+tex(di)+'.\n$$\n\nWe now apply the chain rule, and get\n\n$$\n'+r'\begin{aligned}f\'(x)&=\frac{\text{d}f}{\text{d}u}\cdot\frac{\text{d}u}{\text{d}x}\\&=('+tex(od)+r')\cdot('+tex(di)+r')\\&='+tex(s.diff(c*inner**n,x))+r'.\end{aligned}'+'\n$$')
def generate(level,seed=0,template=None,parameters=None,profile=None,field_type=None):
 if level not in SUPPORTED_LEVELS:raise ValueError('Unknown level')
 rng=random.Random(seed);m=template or rng.choice([m for m in LEVELS if LEVELS[m]==level])
 if m not in LEVELS or LEVELS[m]!=level:raise ValueError('Template/level mismatch')
 raw=profile=='observed_raw' or bool(profile and profile.startswith('raw-'))
 if profile not in (None,'default','observed_raw','source-complete-bank','authored-power-bank','raw-'+m):raise ValueError('Unknown profile')
 if raw and m not in T:raise ValueError('Authored template has no raw evidence')
 if profile=='authored-power-bank' and m!='authored-csc-power' or profile=='source-complete-bank' and m not in T:raise ValueError('Profile/template mismatch')
 p=copy.deepcopy(parameters) if parameters is not None else copy.deepcopy(T[m]['defaults']) if raw else rng.choice(parameters_for(m))
 if not isinstance(p,dict) or set(p)!= {'c','n'} or any(type(v)!=int for v in p.values()) or p not in parameters_for(m):raise ValueError('Outside all API validated bounds')
 if m in T:
  t=T[m];q=copy.deepcopy(t['source']);prompt=render(t['prompt'],p);sol=render(t['solution'],p);values=[render(v,p) for v in t['values']];ft=t['field_type'];key=t['field_key'];fn=t['function']
 else:prompt,sol,values=authored(p);ft=':answer-field.type/blank';key='field-1';fn='csc'
 if field_type not in (None,ft,ft.split('/')[-1]):raise ValueError('Cannot change field contract')
 var=s.Symbol('t',real=True) if fn=='csc' and m!='authored-csc-power' else x
 fun=p['c']*getattr(s,fn)(var)**p['n'];derivative=s.diff(fun,var);expected=derivative/s.cot(var) if fn=='csc' and m!='authored-csc-power' else derivative
 domain={'variable':str(var),'restriction':'sin('+str(var)+') != 0' if fn=='csc' else 'all real '+str(var)}
 if raw:
  q[':question/problem']=prompt
  if ':question/worked-solution' in q:q[':question/worked-solution']=sol
  for a,v in zip(q[':question/answer-fields'][0][':answer-field/choices'],values):a[':answer/value']=v
  f=q[':question/answer-fields'][0]
  if ':answer-field/correct' in f:
   a=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][':answer/id']);f[':answer-field/correct']=copy.deepcopy(a)
 else:
  if m in ('q-143516','q-167568'):prompt='Given that the velocity is $v(t)='+tex(fun)+',$ '+prompt[0].lower()+prompt[1:]
  if not sol:sol=completed_cos_solution(p)
  sol=sol.replace(r"f\'","f'")
  prompt=math_format.normalize_prose(prompt);sol=math_format.normalize_prose(sol);values=[math_format.normalize_tex(v.strip('$')) for v in values]
  # Whole source bank selected by template before parameter construction.
  if ft.endswith('/radio'):
   signs=[-1 if v.startswith('-') else 1 for v in values]
   ci=1 if m=='q-48562' else next(i for i,a in enumerate(T[m]['source'][':question/answer-fields'][0][':answer-field/choices']) if a[':answer/id']==T[m]['source'][':question/answer-fields'][0][':answer-field/correct'][':answer/id'])
  else:ci=0
  body={'prompt':prompt,'solution':sol,'values':sorted(values),'key':values[ci],'field':ft,'domain':domain,'version':VERSION};identity=digest(body);uid=lambda v:str(uuid.uuid5(uuid.UUID(KP_UUID),v));qid=uid(identity);fid=uid(qid+'|'+key)
  choices=[{':answer/id':uid(fid+'|'+v),':answer/type':':answer.type/math',':answer/value':v} for v in values];correct=choices[ci][':answer/id'];rng.shuffle(choices)
  q={':question/id':qid,':question/problem':prompt,':question/worked-solution':sol,':question/difficulty':':question.difficulty/'+level,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':key,':answer-field/type':ft,':answer-field/choices':choices,':answer-field/correct':[':answer/id',correct]}]}
 # Runtime bank eligibility uses a private frozen parser, never root QA.
 if not raw:
  spec=importlib.util.spec_from_file_location('private_scalar',HERE/'scalar_parser.py');parser=importlib.util.module_from_spec(spec);spec.loader.exec_module(parser)
  bank=[parser.scalar(v) for v in values]
  def eq(a,b):return s.simplify(s.trigsimp(a-b))==0
  if any(eq(a,b) for i,a in enumerate(bank) for b in bank[i+1:]):raise ValueError('Reject entire complete bank collision')
  if not eq(bank[ci],expected):raise ValueError('Wrong complete bank key')
  math_format.validate_generated_record({'question':q})
 fp=digest({'function':s.srepr(fun),'response':s.srepr(expected),'domain':domain})
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'level':level,'seed':seed,'template':m,'profile':'observed_raw' if raw else 'authored-power-bank' if m=='authored-csc-power' else 'source-complete-bank','parameters':p,'source_ids':[m] if m in T else [],'domain':domain,'mathematical_fingerprint':fp,'parameter_fingerprint':fp,'authored':m=='authored-csc-power','completion':m in ('q-48562','q-143516','q-167568') and not raw,'evidence_only':raw,'eligible_for_learning':not raw,'dependencies':{'python':sys.version.split()[0],'sympy':s.__version__}}}
def markdown(r):
 q=r['question'];return q[':question/problem']+'\n\n'+ '\n'.join('- '+a[':answer/value'] for a in q[':question/answer-fields'][0][':answer-field/choices'])+'\n\n'+q.get(':question/worked-solution','[Source solution omitted]')
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--difficulty',default='all');a.add_argument('--count',type=int,default=1);a.add_argument('--seed',type=int,default=0);a.add_argument('--format',choices=['json','markdown'],default='json');o=a.parse_args();levels=SUPPORTED_LEVELS if o.difficulty=='all' else (o.difficulty,);rs=[generate(l,o.seed+i) for l in levels for i in range(o.count)];print(json.dumps(rs,indent=2) if o.format=='json' else '\n\n---\n\n'.join(map(markdown,rs)))
