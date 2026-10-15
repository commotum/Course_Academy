#!/usr/bin/env python3
"""Private basis-2275 draft; no database or registration operations.
Source records are immutable raw evidence. Normal output supplies explicitly
attributed completions/corrections and same-method bounded variations.
"""
import sys
sys.dont_write_bytecode=True
import argparse,copy,hashlib,importlib.util,itertools,json,random,re,uuid
from functools import lru_cache
from pathlib import Path
try: import sympy as s
except ImportError:
 import os
 runtime=Path(__file__).resolve().parents[2]/'.venv/bin/python'
 os.execv(str(runtime),[str(runtime),str(Path(__file__).resolve()),*sys.argv[1:]])
HERE=Path(__file__).with_suffix(''); VERSION='ln-chain-private-2275-v1';X=s.Symbol('x',real=True)
fs=importlib.util.spec_from_file_location('ln_draft_math_format',HERE/'math_format.py');fmt=importlib.util.module_from_spec(fs);fs.loader.exec_module(fmt)
SOURCE=json.loads((HERE/'source.json').read_text());KP=SOURCE['record'];KP_ID=17592186092264
ROWS={q.get(':question/math-academy-id','nonMA-'+str(q[':db/id'])):q for q in KP[':knowledge-point/questions']}
# Family is a Markdown/operative-stage contract, profile is a COMPLETE bank.
SPECS={
 'q-11934':('shift-power-radio','moderate',dict(n=3,b=4)),
 'q-28632':('scale-legacy-radio','moderate',dict(a=2)),
 'q-107469':('tangent-affine','hard',dict(a=2,b=2,t=1)),
 'q-341676':('polynomial-blank','moderate',dict(a=3,b=5,n=6)),
 'q-11930':('scale-radio','moderate',dict(a=8)),
 'q-11932':('power-radio','moderate',dict(n=2)),
 'q-150014':('tangent-origin','hard',dict(a=3,t=0)),
 'q-150015':('tangent-shift','hard',dict(t=1)),
 'q-310144':('slope-polynomial','moderate',dict(a=5,b=4,t=1)),
 'q-341671':('scale-blank','moderate',dict(a=9)),
 'q-341679':('slope-affine','moderate',dict(a=4,b=7,t=-1)),
 'q-48654':('tangent-scaled','hard',dict(c=4,a=2,t=4)),
 'nonMA-17592186490400':('tangent-scaled','hard',dict(c=12,a=2,t=12)),
 'nonMA-17592186490408':('tangent-shift','hard',dict(t=20)),
 'authored-easy':('affine-blank','easy',dict(a=2,b=1))}
FAMILY_SOURCE={}
for k,v in SPECS.items():FAMILY_SOURCE.setdefault(v[0],k)
SUPPORTED_LEVELS=('easy','moderate','hard')
GENERATOR_ID=str(uuid.uuid5(uuid.UUID(KP[':knowledge-point/id']),'private-draft-generator'))
def tex(e):return s.latex(e,order='lex').replace(r'\left','').replace(r'\right','').replace(r'\log',r'\ln')
def uid(v):return str(uuid.uuid5(uuid.UUID(GENERATOR_ID),v))
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
def raw_replay(source_id):return {'source_id':source_id,'basis':SOURCE['basis'],'eligible':False,'raw_question':copy.deepcopy(ROWS[source_id])}
def allowed(f):
 a=(-6,-4,-2,-1,1,2,3,4,6,8,9);b=(-5,-2,0,1,2,3,4,5,7);t=(-3,-2,-1,0,1,2,3,4)
 return {
 'affine-blank':dict(a=a,b=b), 'scale-radio':dict(a=a),'scale-legacy-radio':dict(a=a),'scale-blank':dict(a=a),
 'shift-power-radio':dict(n=(3,4,5,6),b=(1,2,3,4,5,7)), 'power-radio':dict(n=(2,3,4,5,6)),
 'polynomial-blank':dict(a=(1,2,3,4,5,7),b=(1,2,3,4,5,6),n=(2,3,4,5,6)),
 'slope-polynomial':dict(a=(1,2,3,4,5,6),b=(1,2,3,4,5,7),t=t),
 'slope-affine':dict(a=(1,2,3,4,5,6),b=b,t=t),
 'tangent-origin':dict(a=(2,3,4,5,6,8),t=t),
 'tangent-shift':dict(t=(-5,-3,-2,-1,0,1,2,3,4,5,7,12,20)),
 'tangent-affine':dict(a=(1,2,3,4,5,6),b=(1,2,3,4,5,7),t=t),
 'tangent-scaled':dict(c=(1,2,3,4,5,6,8,12),a=(1,2,3,4,5),t=(1,2,3,4,5,6,8,12))}[f]
@lru_cache(maxsize=4096)
def _data(f,items):
 p=dict(items)
 if set(p)!=set(allowed(f)):raise ValueError('Wrong parameter slots')
 if any(type(v)!=int or v not in allowed(f)[k] for k,v in p.items()):raise ValueError('Outside bounded parameter slots')
 a=p.get('a',1);b=p.get('b',0);n=p.get('n',1);t=p.get('t');c=p.get('c',1)
 if f in ('scale-radio','scale-legacy-radio','scale-blank'):inner=a*X
 elif f=='affine-blank':inner=a*X+b
 elif f=='shift-power-radio':inner=X**n-b
 elif f=='power-radio':inner=X**n
 elif f=='polynomial-blank':inner=a-b*X**n
 elif f=='slope-polynomial':inner=a*X**2+b
 elif f=='slope-affine':inner=b-a*X
 elif f=='tangent-origin':inner=a*(X-t)+1
 elif f=='tangent-shift':inner=t+1-X
 elif f=='tangent-affine':inner=a*(b-X)
 elif f=='tangent-scaled':inner=a*X
 else:raise ValueError(f)
 fun=c*s.log(inner);du=s.diff(inner,X);der=s.factor(c*du/inner)
 point=s.Integer(t) if t is not None else None
 if point is not None and inner.subs(X,point)<=0:raise ValueError('Point outside real logarithm domain')
 yp=c*s.log(inner.subs(X,point)) if point is not None else None
 m=s.simplify(der.subs(X,point)) if point is not None else None
 target=s.expand(m*(X-point)+yp) if f.startswith('tangent-') else m if f.startswith('slope-') else der
 domain=s.solve_univariate_inequality(inner>0,X,relational=False)
 return dict(inner=s.expand(inner),function=fun,du=du,derivative=der,point=point,yp=yp,m=m,target=target,c=c,domain=domain)
def data(f,p):return _data(f,tuple(sorted(p.items())))
def complete_bank(f,p,d):
 # Profiles are chosen BEFORE parameters. Never select a subset of recipes.
 a=p.get('a');n=p.get('n');b=p.get('b');t=p.get('t');u=d['inner'];z=d['target'];m=d['m'];yp=d['yp'];c=d['c']
 if f=='scale-radio':return [a/X,a*s.log(a*X),1/s.log(a*X),1/X,1/(a*X)]
 if f=='scale-legacy-radio':return [1/(a*X),a/X+1,1/X,1/X+a,a/X]
 if f=='power-radio':return [n*X**(n-1)*s.log(X**n),1/X,n/X**n,n/X,1/X**n]
 if f=='shift-power-radio':return [n*X**(n-1)/u,n*(n-1)/u,(n-1)*X*s.log(u),X/u,X**(n-1)/u]
 if f=='tangent-origin':return [a*(X-t)+1,a*(X-t),X-t,X-t+a,a*(X-t)+s.log(a)]
 if f in ('tangent-shift','tangent-affine'):return [-m*X+m*t+yp,-m*X-m*t+yp,z,m*X+yp,-2*m*X+yp]
 if f=='tangent-scaled':return [2*m*X-s.Rational(c,2)-s.log(a*t),2*m*X-2*c+yp,m*X-c,z,m*X+c]
 return [z]
def equivalent(a,b):return s.simplify(s.sympify(a)-s.sympify(b))==0
def bank_indices(vals,target):
 if any(equivalent(a,b) for i,a in enumerate(vals) for b in vals[:i]):raise ValueError('Whole profile rejected: equivalent options')
 hits=[i for i,v in enumerate(vals) if equivalent(v,target)]
 if len(hits)!=1:raise ValueError('Whole profile rejected: unique correct answer required')
 return hits[0]
@lru_cache(maxsize=4096)
def instance(f,items):
 d=_data(f,items);values=complete_bank(f,dict(items),d)
 return d,values,bank_indices(values,d['target'])
def dfrac(name,variable):return r'\frac{\text{d}'+name+r'}{\text{d}'+variable+'}'
def fraction(num,den):return r'\frac{'+str(num)+'}{'+str(den)+'}'
def display(v):return '$$\n'+v+'\n$$'
def aligned_equal(lhs,rhs):return r'\begin{aligned}'+lhs+' &='+r' \\ &='.join(rhs)+r'\end{aligned}'
def solution_blocks(f,p,d,name):
 L=tex;u=L(d['inner']);du=L(d['du']);c=d['c'];cf='' if c==1 else str(c);of=fraction(c,'u');dx=dfrac(name,'x');dfdu=dfrac(name,'u');dudx=dfrac('u','x')
 first=name+'='+cf+r'\ln u,\,u='+u+'.'
 second=dfdu+'='+of+r',\,'+dudx+'='+du+'.'
 rhs=[dfdu+r'\cdot '+dudx,of+r'\cdot ('+du+')',fraction(c,u)+r'\cdot ('+du+')']
 raw=fraction(L(c*d['du']),u)
 if f in ('scale-radio','scale-legacy-radio','scale-blank','power-radio','tangent-scaled','tangent-affine'):
  rhs.append(raw)
  if f=='power-radio':cancel=fraction(str(p['n'])+r'\cancel{x^{'+str(p['n']-1)+'}}',r'x\cdot\cancel{x^{'+str(p['n']-1)+'}}')
  elif f=='tangent-affine':cancel='-'+fraction(r'\cancel{'+str(p['a'])+'}',r'\cancel{'+str(p['a'])+r'}\cdot('+tex(p['b']-X)+')')
  elif f=='tangent-scaled':cancel=fraction(r'\cancel{'+str(p['a'])+r'}\cdot '+str(c),r'\cancel{'+str(p['a'])+r'}\cdot x')
  else:cancel=fraction(r'\cancel{'+str(p['a'])+'}',r'\cancel{'+str(p['a'])+'}x')
  rhs.extend([cancel,L(d['derivative'])+'.'])
 else:rhs.append((L(d['derivative']) if f=='tangent-shift' else raw)+'.')
 blocks=[first,second,aligned_equal(dx,rhs)]
 if d['point'] is not None:
  pt=L(d['point']);der=L(d['derivative']);ev=lambda e:r'\left.('+e+r')\right|_{x='+pt+'}'
  # The substituted fraction is printed without simplifying its operands.
  sub=fraction('('+L(c*d['du']) .replace('x','('+pt+')')+')','('+u.replace('x','('+pt+')')+')')
  left=('m=' if f.startswith('slope-') else '')+ev(dx)
  blocks.append(aligned_equal(left,[ev(der),sub,L(d['m'])+'.']))
  if f.startswith('tangent-'):
   blocks.append(aligned_equal('y-y_1',['m(x-x_1)', # generic point-slope stage
    # Retain the full supplied point and slope, including zero and one.
    ]))
   blocks[-1]=r'\begin{aligned}y-y_1 &=m(x-x_1) \\ y-('+L(d['yp'])+') &=('+L(d['m'])+')(x-('+pt+')) '+r'\\ y &='+L(d['target'])+r'\end{aligned}'
 return blocks
COMPLETION_WORDS=['First, we express $f(x)$ as the composite function','Differentiating gives','We now apply the chain rule, and we get']
def normal_solution(source_id,f,p,d,name):
 blocks=solution_blocks(f,p,d,name)
 if source_id.startswith("nonMA-"):
  if f=="tangent-scaled":
   blocks[2]=aligned_equal(dfrac(name,"x"),[dfrac(name,"u")+r"\cdot "+dfrac("u","x"),fraction(d["c"],"u")+r"\cdot ("+tex(d["du"])+")",fraction(d["c"],tex(d["inner"]))+r"\cdot ("+tex(d["du"])+")",tex(d["derivative"])+"."])
  blocks[3]="m="+r"\left.("+tex(d["derivative"])+r")\right|_{x="+tex(d["point"])+"}="+tex(d["m"])+"."
 if source_id in ROWS and ':question/worked-solution' in ROWS[source_id]:
  raw=ROWS[source_id][':question/worked-solution']
  # Correct only the observed stale g-name and joined prose in q-11930.
  raw=raw.replace('rule.First','rule. First').replace('express $g(x)$','express $f(x)$') if source_id=='q-11930' else raw
  if source_id=='q-11930':raw=re.sub(r'Here \$.*?\$ is a function',lambda _: 'Here $'+name+'(x)='+function_tex(d)+'$ is a function',raw,count=1)
  sections=re.split(r'\$\$.*?\$\$',raw,flags=re.S)
  if len(sections)!=len(blocks)+1:raise ValueError(('Source stage mismatch',source_id,len(sections),len(blocks)))
  # Parameterize the actual targets in shared prose; all dependent prose agrees.
  for i,w in enumerate(sections):
   w=re.sub(r'\$x=.*?\$',lambda _:'$x='+tex(d['point'])+'$',w) if d['point'] is not None else w
   if f.startswith('tangent-'):
    w=re.sub(r'\$\(.*?\)\$',lambda _:'$('+tex(d['point'])+','+tex(d['yp'])+')$',w)
    w=re.sub(r'\$m=.*?\$',lambda _:'$m='+tex(d['m'])+'.$',w)
   sections[i]=w
  return ''.join(sections[i]+display(v) for i,v in enumerate(blocks))+sections[-1]
 words=[w.replace('$f(x)$','$'+name+'(x)$') for w in COMPLETION_WORDS]
 if f.startswith('tangent-'):
  words.extend(['Therefore, the slope $m$ of the tangent line at the point where $x='+tex(d['point'])+'$ is','Hence, the slope of the tangent line at the point $('+tex(d['point'])+','+tex(d['yp'])+')$ is $m='+tex(d['m'])+'.$ Now, we find the equation of the tangent at that point:'])
 return '\n\n'.join(w+'\n\n'+display(v) for w,v in zip(words,blocks))
def function_tex(d):return ('' if d['c']==1 else str(d['c']))+r'\ln('+tex(d['inner'])+')'
def normal_prompt(source_id,f,p,d,name):
 fl=name+'(x)='+function_tex(d)
 if f.startswith('tangent-'):return 'Find the equation of the tangent to the curve $'+fl+'$ at the point $('+tex(d['point'])+','+tex(d['yp'])+').$'
 if f.startswith('slope-'):return 'Find the slope $m$ of the tangent to the curve $'+fl+'$ at the point where $x='+tex(d['point'])+'.$\n\n$m=$\n{{field-1}}'
 request=(name+'^{′}(x)' if f=='scale-legacy-radio' else r'\frac{df}{dx}' if f=='shift-power-radio' else dfrac(name,'x'))
 text=('For $' if f=='scale-legacy-radio' else 'Given that $')+fl+'$, find $'+request+'.$'
 if f.endswith('blank'):text+='\n\n$'+dfrac(name,'x')+'=$\n{{field-1}}'
 return text

def task_identity(d,f):
 # Actual function, original real domain, requested role and point. No seed,
 # profile, option order, difficulty, or synthetic template tags.
 kind='tangent equation' if f.startswith('tangent-') else 'tangent slope' if f.startswith('slope-') else 'derivative'
 return digest([s.srepr(d['function']),s.srepr(d['domain']),kind,s.srepr(d['point'])])
def profile_for(f):return None if f.endswith('blank') or f.startswith('slope-') else f+'-complete'
@fmt.checked_math_content
def generate(level=None,seed=0,template=None,parameters=None,bank_profile=None,source_id=None,difficulty=None):
 if type(seed) is not int:raise ValueError('Seed requires a builtin integer')
 if level is not None:
  if difficulty is not None and difficulty!=level:raise ValueError("Conflicting difficulty")
  difficulty=level
 if source_id is None:
  if template is None:
   if difficulty not in SUPPORTED_LEVELS:raise ValueError('Specify a supported difficulty')
   sources=[k for k,(f,l,p) in SPECS.items() if l==difficulty and not k.startswith('nonMA-')]
   source_id=random.Random(seed).choice(sources)
  else:source_id=FAMILY_SOURCE.get(template,template)
 if source_id not in SPECS:raise ValueError('Unknown source/template')
 f,level,original=SPECS[source_id];profile=profile_for(f)
 if template is not None and template not in (f,source_id):raise ValueError('Source/template mismatch')
 if bank_profile is not None and bank_profile!=profile:raise ValueError('Complete profile mismatch')
 if difficulty is not None and difficulty!=level:raise ValueError('Difficulty is a family contract')
 rng=random.Random(seed)
 for attempt in range(2000):
  p=copy.deepcopy(parameters) if parameters is not None else {k:rng.choice(v) for k,v in allowed(f).items()}
  try:d,values,correct=instance(f,tuple(sorted(p.items())))
  except ValueError:
   if parameters is not None:raise
   continue
  break
 else:raise ValueError('No valid complete bank')
 name='g' if f in ('power-radio','scale-legacy-radio') else 'f';isblank=profile is None
 prompt=fmt.normalize_prose(normal_prompt(source_id,f,p,d,name));solution=fmt.normalize_prose(normal_solution(source_id,f,p,d,name))
 rendered=[fmt.normalize_tex(('y=' if f.startswith('tangent-') else '')+tex(v)) for v in values]
 task=task_identity(d,f)
 content=digest([prompt,solution,rendered,correct,'blank' if isblank else 'radio',level])
 qid=uid('question:'+content);key='field-1' if isblank else 'selection';fid=uid(qid+':'+key)
 answers=[{':answer/id':uid(fid+':'+str(i)+':'+value),':answer/type':':answer.type/math',':answer/value':value} for i,value in enumerate(rendered)]
 field={':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+('blank' if isblank else 'radio'),':answer-field/choices':answers,':answer-field/correct':[':answer/id',answers[correct][':answer/id']]}
 q={':question/id':qid,':question/problem':prompt,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+level,':question/answer-fields':[field]}
 authored=[]
 if source_id in ('q-11934','q-28632'):authored=['Missing source key and solution completed from actual derivative; unrated source assigned moderate conservatively.']
 if source_id=='q-107469':authored=['Missing source fields completed with authored five-option tangent bank: horizontal/vertical translation of observed tangent-shift profile.']
 if source_id=='q-11930':authored=['Corrected stale g(x) to f(x) in composite-function prose and separated joined sentence.']
 if source_id=='authored-easy':authored=['Easy extension: introductory affine inner function and observed derivative-RHS blank contract; same three chain-rule stages.']
 return {'knowledge_point':{'id':KP[':knowledge-point/id'],'db_id':KP_ID,'title':KP[':knowledge-point/title']},'question':q,'generation':{'generator_id':GENERATOR_ID,'version':VERSION,'source_basis':SOURCE['basis'],'source_id':source_id,'template':f,'difficulty':level,'parameters':p,'bank_profile':profile,'seed':seed,'mathematical_key':task,'domain':str(d['domain']),'dependencies':{'sympy':s.__version__},'authored_changes':authored,'eligible':True}}
def generate_easy(seed=0,template=None,parameters=None,**kw):return generate('easy',seed,template,parameters,**kw)
def generate_moderate(seed=0,template=None,parameters=None,**kw):return generate('moderate',seed,template,parameters,**kw)
def generate_hard(seed=0,template=None,parameters=None,**kw):return generate('hard',seed,template,parameters,**kw)
def source_case(source_id):return generate(source_id=source_id,parameters=SPECS[source_id][2])
def batch(difficulty,count=5,seed=0):
 if difficulty not in SUPPORTED_LEVELS or type(count)!=int or count<0 or type(seed) is not int:raise ValueError('Invalid batch')
 out=[];seen=set();rng=random.Random(seed)
 sources=[k for k,(f,l,p) in SPECS.items() if l==difficulty and not k.startswith('nonMA-')]
 for i in range(max(200,count*50)):
  if len(out)==count:return out
  src=rng.choice(sources);r=generate(source_id=src,seed=rng.randrange(2**32));key=r['generation']['mathematical_key']
  if key not in seen:seen.add(key);out.append(r)
 raise ValueError('Bounded policy exhausted; requested distinct actual tasks unavailable')
def markdown(record):
 q=record['question'];f=q[':question/answer-fields'][0]
 return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$' for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=(*SUPPORTED_LEVELS,'all'),default='moderate');ap.add_argument('--count',type=int,default=5);ap.add_argument('--seed',type=int,default=0);ap.add_argument('--format',choices=('json','markdown'),default='json');ap.add_argument('--source-id');ap.add_argument('--raw',action='store_true');a=ap.parse_args()
 rows=[raw_replay(a.source_id)] if a.raw else [source_case(a.source_id)] if a.source_id else [r for level in (SUPPORTED_LEVELS if a.difficulty=='all' else (a.difficulty,)) for r in batch(level,a.count,a.seed)]
 print(json.dumps(rows,ensure_ascii=False,indent=2) if a.format=='json' else '\n\n---\n\n'.join(map(markdown,rows)))
