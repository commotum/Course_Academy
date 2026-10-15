"""Basis-2275 private repeated-chain-rule draft; preserves registered baseline.

The normal observed families retain source prose and ordered operative stages
through simultaneous full-component masks. Unrated trig-cubic sources receive
explicit authored keys, solutions, and tentative easy ratings. The fieldless
question is raw-only; nested-trig blank serving is bounded to shifts1..24
whose ordinary-wrong probes all resolve in the native grader. The zero-at-origin exponential family retains a faithful fixed-base
normal compatibility profile; base changes are not counted as inventory. No DB writes.
"""
import argparse, copy, hashlib, importlib.util, json, random, sys, uuid
from pathlib import Path
import sympy as s
KP_ID=17592186096742
KP_UUID='f3ee0d5d-0821-5f6b-b613-6b814e65df50'
TITLE='Calculating a Derivative Using Multiple Instances of the Chain Rule'
VERSION='repeated-chain-rule-basis2275-draft-2'
HERE=Path(__file__).with_suffix('')
LEVELS=('easy','moderate','hard')
x=s.Symbol('x',real=True);u=s.Symbol('u',real=True);v=s.Symbol('v',real=True)
def helper(name):
 spec=importlib.util.spec_from_file_location('kp96742_'+name,HERE/(name+'.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
math_format=helper('math_format')
SOURCES={q[':question/math-academy-id']:q for q in json.loads((HERE/'source.json').read_text())['record'][':knowledge-point/questions'] if ':question/math-academy-id' in q}
DEFAULTS={'q-48569':{'a':3},'q-48570':{'a':4},'q-16699':{'a':5,'b':2},'q-312907':{'a':5},'q-2397':{'a':9},'q-28655':{'a':5},'q-31352':{'b':6},'q-31361':{'a':5,'b':1},'q-342927':{'b':1}}
DIFFICULTIES={'q-48569':'easy','q-48570':'easy','q-16699':'hard','q-312907':'moderate','q-2397':'moderate','q-28655':'hard','q-31352':'moderate','q-31361':'hard','q-342927':'moderate'}
RAW_ONLY={'q-16699':'Captured question has no answer fields.'}
GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),VERSION))
def digest(o):return hashlib.sha256(json.dumps(o,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def tex(e):return s.latex(e).replace(r'\log',r'\ln')
def parameters_for(m,raw=False):
 if m in ('q-48569','q-48570'):return [{'a':a} for a in range(2,32)]
 if m in ('q-312907','q-2397'):return [{'a':a} for a in range(1,32)]
 if m=='q-31352':return [{'b':b} for b in range(1,32)]
 if m=='q-342927':return [{'b':b} for b in range(1,32 if raw else 25)]
 if m=='q-31361':return [{'a':a,'b':b} for a in range(1,17) for b in range(1,7)]
 if m=='q-16699':return [{'a':a,'b':b} for a in range(1,17) for b in range(1,7)]
 if m=='q-28655':return [{'a':a} for a in range(2,17)]
 raise ValueError('Unknown template')
def model(m,p):
 a=p.get('a');b=p.get('b');point=None
 if m=='q-48569':components=(u**3,s.cos(v),a*x)
 elif m=='q-48570':components=(u**3,s.sin(v),a*x)
 elif m=='q-312907':components=(u**8,s.cos(v),a*x**3)
 elif m=='q-2397':components=(u**3,s.sin(v),a*x**2-1)
 elif m=='q-31352':components=(s.cot(u),v**2,x+b)
 elif m=='q-31361':components=(u**4,s.cot(v),a*x-b);point=0
 elif m=='q-16699':components=(u**3,s.cos(v),a*x**2+b);point=1
 elif m=='q-28655':components=(s.Integer(a)**u,s.log(v),s.cos(x));point=0
 elif m=='q-342927':components=(s.sqrt(u),s.cos(v),2*x-b)
 else:raise ValueError('Unknown template')
 outer,middle,inner=components;fun=outer.subs(u,middle).subs(v,inner)
 # Derive the complete correct value first; fragments follow from this instance.
 full=s.diff(fun,x);answer=full.subs(x,point) if point is not None else full
 if m=='q-312907':answer=-24*a*x**2
 if m=='q-342927':answer=-s.sin(inner)
 derivatives=(s.diff(outer,u),s.diff(middle,v),s.diff(inner,x))
 return {'components':components,'derivatives':derivatives,'function':fun,'derivative':full,'answer':answer,'point':point}

def masks(m,p):
 """Mask complete mathematical components simultaneously; never global digits."""
 a=p.get('a');b=p.get('b')
 if m=='q-48569':return [('3x',f'{a}x'),('-9',str(-3*a)),('9\\sin',str(3*a)+r'\sin')]
 if m=='q-48570':return [('4x',f'{a}x'),('12\\sin',str(3*a)+r'\sin')]
 if m=='q-312907':return [('5{x}^{3}',f'{a}'+r'{x}^{3}'),('15{x}^{2}',str(3*a)+r'{x}^{2}'),('-120{x}^{2}',str(-24*a)+r'{x}^{2}')]
 if m=='q-2397':return [('9{x}^{2}-1',f'{a}'+r'{x}^{2}-1'),('18x',f'{2*a}x'),('54x',f'{6*a}x')]
 if m=='q-31352':return [('x+6',f'x+{b}')]
 if m=='q-342927':return [('2x-1',f'2x-{b}')]
 if m=='q-28655':return [('{5}',f'{{{a}}}'),('⁡5','⁡'+str(a))]
 if m=='q-16699':return [('5{x}^{2}+2',f'{a}'+r'{x}^{2}+'+str(b)),('5(1)^{2}+2',f'{a}(1)^{{2}}+{b}'),('10x',f'{2*a}x'),('-30x',f'{-6*a}x'),('-30(1)',f'{-6*a}(1)'),('-30{cos}^{2}7',f'{-6*a}'+r'{cos}^{2}'+str(a+b)),('sin}7','sin}'+str(a+b))]
 if m=='q-31361':return [('5x-1',f'{a}x-{b}'),('5(0)-1',f'{a}(0)-{b}'),('(-1)',f'(-{b})'),('⁡1','⁡'+str(b)),('=-20',f'={-4*a}'),('=20',f'={4*a}'),('-20{',f'{-4*a}'+'{'),('20{',f'{4*a}'+'{'),('20\\',f'{4*a}'+"\\"),('5{cot}',str(a)+'{cot}'),('=5.',f'={a}.'),('\\cdot 5',r'\cdot '+str(a))]
 raise ValueError(m)
def transform(t,m,p):
 if m=='q-28655' and t in ('5','-5'):return str(p['a'] if t=='5' else -p['a'])
 for i,(old,new) in enumerate(masks(m,p)):t=t.replace(old,f'@@M{i}@@')
 for i,(old,new) in enumerate(masks(m,p)):t=t.replace(f'@@M{i}@@',new)
 return t

def bank(m,p):
 """Exactly one complete observed profile, mathematical recipes in source order."""
 a=p.get('a');b=p.get('b');M=model(m,p);c=M['answer'];z=M['components'][2]
 if m=='q-48569':return [c,-3*a*s.cos(x)**2*s.sin(x),-3*s.sin(z)**2,3*a*s.sin(z)**2*s.cos(z),3*s.cos(z)**2*s.sin(z)]
 if m=='q-48570':return [c,3*s.sin(z)**2*s.cos(z),3*a*s.sin(x)**2*s.cos(x),3*a*s.sin(z)*s.cos(z),3*s.sin(x)*s.cos(x)]
 if m=='q-2397':return [c,3*x*s.sin(z)**2*s.cos(z)**2,2*a*x*s.sin(z)**2*s.cos(z)**2,2*a*x*s.sin(z)**2*s.cos(z),6*a*x*s.sin(z)**3*s.cos(z)**3]
 if m=='q-31352':return [c,-s.csc((x+b)**2)**2,2*x*s.csc((x+b)**2)**2,-2*(x+b)*s.csc(x+b),4*(x+b)]
 if m=='q-31361':return [c,a*s.cot(b)**3*s.sec(b)**2,-4*s.cot(b)**2*s.csc(b)**2,4*a*s.cot(b)*s.sec(b)**2,-4*s.cot(b)**3*s.csc(b)**2]
 if m=='q-28655':return [c,-1,-a,a,1]
 if m in ('q-312907','q-342927'):return [c]
 return []

def domain(m,p):
 inner=model(m,p)['components'][2]
 if m in ('q-31352','q-31361'):return {'real_x':True,'radians':True,'restriction':tex(inner if m=='q-31361' else inner**2)+r'\notin\pi\mathbb{Z}'}
 if m=='q-28655':return {'real_x':True,'radians':True,'restriction':r'\cos(x)>0'}
 if m=='q-342927':return {'real_x':True,'radians':True,'restriction':r'\cos('+tex(inner)+')>0'}
 return {'real_x':True,'radians':True,'restriction':'all real x'}

def authored_easy(m,p):
 """Only missing source solutions authored, with all observed method stages."""
 a=p['a'];trig='cos' if m=='q-48569' else 'sin';du=r'-\sin v' if trig=='cos' else r'\cos v'
 final=transform(SOURCES[m][':question/answer-fields'][0][':answer-field/choices'][0][':answer/value'],m,p)
 text=r"""First, we express $f$ as the composite function

$$
f=u^3,\,u=\TRIG v,\,v=FREQx.
$$

Differentiating gives

$$
\frac{\text{d}f}{\text{d}u}=3u^2,\,\frac{\text{d}u}{\text{d}v}=MIDDER,\,\frac{\text{d}v}{\text{d}x}=FREQ.
$$

Applying now the chain rule twice, we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} & =\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\ & =\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}v}\cdot \frac{\text{d}v}{\text{d}x} \\ & =3u^2\cdot (MIDDER)\cdot FREQ \\ & =3(\TRIG(FREQx))^2\cdot (SUBMIDDER)\cdot FREQ \\ & =FINAL.\end{aligned}
$$"""
 return text.replace('TRIG',trig).replace('SUBMIDDER',du.replace(' v','('+str(a)+'x)')).replace('MIDDER',du).replace('FREQ',str(a)).replace('FINAL',final)

def task_fingerprint(m,p):
 M=model(m,p)
 if m=='q-28655':return digest({'assessed_value':s.srepr(M['answer']),'response':'point-value','reason':'base does not change assessment at origin'})
 return digest({'function':s.srepr(M['function']),'point':M['point'],'response':'polynomial-prefactor' if m=='q-312907' else 'radical-numerator' if m=='q-342927' else 'complete-derivative','domain':domain(m,p)})

@math_format.checked_math_content
def _checked_normal_record(record):return record

def generate(level,seed=0,template=None,parameters=None,profile=None,field_type=None):
 if level not in LEVELS:raise ValueError('Unsupported difficulty')
 rng=random.Random(seed);raw=profile=='observed_raw' or bool(profile and profile.startswith('raw-'))
 if profile and profile.startswith('raw-'):
  if template is not None and template!=profile[4:]:raise ValueError('Profile/template mismatch')
  template=profile[4:]
 eligible=[m for m in SOURCES if DIFFICULTIES[m]==level and (raw or (m not in RAW_ONLY and m!='q-28655') or (m=='q-28655' and profile=='source-compatibility'))]
 m=template or rng.choice(eligible)
 if m not in eligible:raise ValueError('Unsupported template/level or raw-only serving exclusion')
 if profile not in (None,'default','source-bank','source-blank','source-compatibility','observed_raw','raw-'+m):raise ValueError('Unknown profile')
 canonical_profile='observed_raw' if raw else 'source-compatibility' if m=='q-28655' else 'source-blank' if m in ('q-312907','q-342927') else 'source-bank'
 if not raw and profile=='source-compatibility' and m!='q-28655':raise ValueError('Compatibility profile belongs to q28655 only')
 if not raw and profile in ('source-bank','source-blank') and profile!=canonical_profile:raise ValueError('Profile/field mismatch')
 p=copy.deepcopy(parameters) if parameters is not None else (copy.deepcopy(DEFAULTS[m]) if raw or m=='q-28655' else rng.choice(parameters_for(m)))
 if m=='q-28655' and not raw and p!=DEFAULTS[m]:raise ValueError('Compatibility profile keeps original base; varied-base raw evidence is not inventory')
 if p not in parameters_for(m,raw) or any(type(t)!=int for t in p.values()):raise ValueError('Outside documented bounded parameter domain')
 src=SOURCES[m];M=model(m,p);vals=bank(m,p)
 # A complete bank was selected above, then tested as a whole; never pool recipes.
 if not raw and len(vals)>1:
  for i,a in enumerate(vals):
   for b in vals[i+1:]:
    diff=s.sympify(a)-s.sympify(b)
    witnesses=(s.Rational(1,7),s.Rational(2,7)) if diff.has(x) else (s.Rational(0),)
    if any(abs(complex(s.N(diff.subs(x,t),50)))>1e-20 for t in witnesses):continue
    if s.simplify(s.trigsimp(diff))==0:raise ValueError('Entire chosen bank rejected: equivalent choices')
 prompt=transform(src[':question/problem'],m,p)
 worked=transform(src.get(':question/worked-solution',''),m,p)
 if not raw and not worked:worked=authored_easy(m,p)
 has_solution=not raw or ':question/worked-solution' in src;has_grade=not raw or ':question/difficulty' in src
 old_fields=src.get(':question/answer-fields',[]);fields_data=[]
 for of in old_fields:
  ft=of[':answer-field/type'][':db/ident'];key=of[':answer-field/key']
  if field_type is not None and field_type not in (ft,ft.split('/')[-1]):raise ValueError('Cannot change observed field contract')
  values=[transform(a[':answer/value'],m,p) for a in of[':answer-field/choices']]
  correct=of.get(':answer-field/correct');has_correct=not raw or correct is not None
  ci=next(i for i,a in enumerate(of[':answer-field/choices']) if a[':answer/id']==correct[':answer/id']) if correct else 0
  if not raw:values=[math_format.normalize_tex(t) for t in values]
  fields_data.append((of,ft,key,values,ci,has_correct))
 if not old_fields and field_type is not None:raise ValueError('Captured question has no field')
 if not raw:prompt=math_format.normalize_prose(prompt);worked=math_format.normalize_prose(worked)
 body={'version':VERSION,'problem':prompt,'solution':worked if has_solution else None,'level':level if has_grade else None,'domain':domain(m,p),'fields':[{'type':ft,'key':key,'values':sorted(vs),'correct':vs[ci] if hc else None} for of,ft,key,vs,ci,hc in fields_data]}
 content_id=digest(body);uid=lambda text:str(uuid.uuid5(uuid.UUID(KP_UUID),text));qid=uid(content_id)
 fields=[]
 for of,ft,key,values,ci,hc in fields_data:
  fid=uid(qid+'|'+key);answers=[{':answer/id':uid(fid+'|'+val),':answer/type':a[':answer/type'][':db/ident'],':answer/value':val} for a,val in zip(of[':answer-field/choices'],values)]
  for a,old in zip(answers,of[':answer-field/choices']):
   if ':answer/feedback' in old:a[':answer/feedback']=transform(old[':answer/feedback'],m,p)
  f={':answer-field/id':fid,':answer-field/key':key,':answer-field/type':ft,':answer-field/choices':answers}
  if hc:f[':answer-field/correct']=[':answer/id',answers[ci][':answer/id']]
  if not raw and ft.endswith('/radio'):random.Random(seed).shuffle(answers)
  fields.append(f)
 q={':question/id':qid,':question/problem':prompt}
 if ':question/answer-fields' in src:q[':question/answer-fields']=fields
 if has_solution:q[':question/worked-solution']=worked
 if has_grade:q[':question/difficulty']=':question.difficulty/'+level
 metadata={'generator_id':GENERATOR_UUID,'version':VERSION,'level':level,'seed':seed,'template':m,'profile':canonical_profile,'bank_profile':canonical_profile,'parameters':p,'mathematical_fingerprint':task_fingerprint(m,p),'content_identity':content_id,'domain':domain(m,p),'source_basis':2275,'source_lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1','source_references':[m],'dependencies':{'python':sys.version.split()[0],'sympy':s.__version__,'math_format':'private frozen helper'},'plots':'none','evidence_only':raw,'eligible_for_learning':not raw,'difficulty_provenance':'tentative authored easy rating for unrated MA source' if m in ('q-48569','q-48570') else 'observed MA rating','authored_missing_key':not raw and m in ('q-48569','q-48570'),'authored_missing_solution':not raw and m in ('q-48569','q-48570'),'raw_only_exclusion':RAW_ONLY.get(m)}
 record={'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':metadata}
 if not raw:return _checked_normal_record(record)
 for k in (':question/problem',':question/worked-solution'):
  if k in q:math_format.validate_prose(q[k])
 for f in fields:
  for a in f[':answer-field/choices']:math_format.validate_tex(a[':answer/value'])
 metadata['math_format']=math_format.FORMAT_VERSION
 return record

def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)
def batch(level,count,seed=0):
 pairs=[(m,p) for m in SOURCES if DIFFICULTIES[m]==level and m not in RAW_ONLY and m!='q-28655' for p in parameters_for(m)];random.Random(seed).shuffle(pairs)
 if type(count)is not int or not 0<=count<=len(pairs):raise ValueError('Finite batch capacity exceeded')
 return [generate(level,seed+i,m,p) for i,(m,p) in enumerate(pairs[:count])]
def markdown(rec):
 q=rec['question'];parts=[q[':question/problem']]
 for f in q.get(':question/answer-fields',[]):
  ci=f.get(':answer-field/correct',[None,None])[1];parts.append('\n'.join(('* ' if a[':answer/id']==ci else '- ')+a[':answer/value'] for a in f[':answer-field/choices']))
 if ':question/worked-solution' in q:parts.append(q[':question/worked-solution'])
 return '\n\n'.join(parts)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--difficulty',choices=(*LEVELS,'all'),required=True);p.add_argument('--seed',type=int,default=0);p.add_argument('--count',type=int,default=1);p.add_argument('--format',choices=('json','markdown'),default='json');p.add_argument('--template');p.add_argument('--profile');a=p.parse_args()
 records=[generate(l,a.seed+i,template=a.template,profile=a.profile) for l in (LEVELS if a.difficulty=='all' else [a.difficulty]) for i in range(a.count)]
 print(json.dumps(records,indent=2) if a.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
