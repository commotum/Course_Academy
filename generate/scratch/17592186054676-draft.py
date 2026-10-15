"""Point-line membership: full source replay, role-aware whole banks, local plots.

E/M are source-supported; H is an authored rational-coefficient extension using
exactly the same coordinate-reading and three substitution tests. No EDB access.
"""
import argparse, copy, hashlib, importlib.util, itertools, json, math, os, random, re, sys, uuid
from fractions import Fraction
from pathlib import Path
os.environ.setdefault('MPLCONFIGDIR','/tmp/kp17592186054676-draft-mpl')
HERE=Path(__file__).with_suffix(''); ROOT=HERE.parents[2]
_spec=importlib.util.spec_from_file_location('pointline_private_format',HERE/'math_format.py');_fmt=importlib.util.module_from_spec(_spec);_spec.loader.exec_module(_fmt)
try:
 import sympy as s
except ModuleNotFoundError:
 runtime=ROOT/'.venv/bin/python'
 if __name__=='__main__' and runtime.is_file():os.execv(str(runtime),[str(runtime),'-B',str(Path(__file__).resolve()),*sys.argv[1:]])
 raise
KP_ID=17592186054676;KP_UUID='3123f8ed-a1ca-52b7-8427-2f3b60d9e68a';VERSION='2.0.0-draft'
WRAPPER=json.loads((HERE/'source.json').read_text());SOURCES={q.get(':question/math-academy-id')or q[':question/id']:q for q in WRAPPER['record'][':knowledge-point/questions']}
SUPPORTED_LEVELS=('easy','moderate','hard');SOURCE_TEMPLATES={'easy':'q-71829','moderate':'q-102142','hard':'authored-rational'}
SOURCE_TEMPLATES_BY_LEVEL={l:[k for k,q in SOURCES.items() if q.get(':question/difficulty',{}).get(':db/ident','').endswith('/'+l)] for l in ('easy','moderate')}
ROLE_PERMUTATIONS=list(itertools.permutations('ABC'))
# Complete source bank first, then a role-preserving permutation. Never pool choices.
PROFILES={'easy':['A C','A','B','C','B C'],'moderate':['A C','C','A B','B','A'],'hard':['A C','C','A B','B','A']}
BASE_TRUTH={'easy':{0,2},'moderate':{2},'hard':{2},'unrated':{1}}
CAPACITY_LIMIT=10000 # Request guard is conservative; not a claim of exact finite capacity.

def _int(v,name):
 if type(v)is not int:raise TypeError(name+' must be a built-in int')
 return v

def _seed(seed):return _int(seed,'seed')
def _identity(value):return str(uuid.uuid5(uuid.UUID(KP_UUID),json.dumps(value,sort_keys=True,separators=(',',':'))))
def _frac(v):
 if type(v)is int:return Fraction(v)
 if type(v)is str:return Fraction(v)
 raise TypeError('coefficients must be built-in ints or exact rational strings')
def tex(v):
 v=_frac(v) if not isinstance(v,Fraction) else v
 return str(v.numerator) if v.denominator==1 else ('-' if v<0 else '')+r'\frac{'+str(abs(v.numerator))+'}{'+str(v.denominator)+'}'
def equation(p):
 m=_frac(p['m']);b=_frac(p['b']);coef='' if m==1 else '-'if m==-1 else tex(m)
 return coef+'x'+('+'+tex(b)if b>0 else tex(b)if b<0 else '')
def _defaults(q):
 sol=q[':question/worked-solution'];pairs=re.findall(r'([ABC])=?\((-?\d+),(-?\d+)\)',sol);points={a:[int(x),int(y)]for a,x,y in pairs}
 match=re.search(r'y\s*=\s*([^$?]+)',q[':question/problem']);e=match[1].rstrip('.').replace(' ','');m=re.match(r'(-?\d*)x([+-]\d+)?$',e)
 assert m,e
 return {'m':int(m[1])if m[1]not in('','-')else(-1 if m[1]=='-'else 1),'b':int(m[2]or 0),'points':[points[a]for a in'ABC']}
DEFAULTS={k:_defaults(q)for k,q in SOURCES.items()}

def _normal(q):
 q=copy.deepcopy(q);q.pop(':db/id',None)
 if ':question/difficulty'in q:q[':question/difficulty']=q[':question/difficulty'][':db/ident']
 for f in q.get(':question/answer-fields',[]):
  f.pop(':db/id',None);f[':answer-field/type']=f[':answer-field/type'][':db/ident'];f[':answer-field/correct']=[':answer/id',f[':answer-field/correct'][':answer/id']]
  for a in f[':answer-field/choices']:a.pop(':db/id',None);a[':answer/type']=a[':answer/type'][':db/ident']
 return q

def task_identity(p):
 # Label, source profile, choices, seed and display styling are not mathematical tasks.
 return hashlib.sha256(json.dumps({'equation':[str(_frac(p['m'])),str(_frac(p['b']))],'points':sorted(p['points']),'task':'identify all supplied points satisfying line'},sort_keys=True).encode()).hexdigest()

def replay_raw(source_id):
 """Exact original IDs, content and attribute presence; normalized enum/ref envelope."""
 if source_id not in SOURCES:raise ValueError('unknown source')
 q=_normal(SOURCES[source_id]);p=copy.deepcopy(DEFAULTS[source_id]);return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':WRAPPER['record'][':knowledge-point/title']},'question':q,'generation':{'version':VERSION,'source_id':source_id,'template':source_id,'source_basis':WRAPPER['basis'],'source_lineage':WRAPPER['lineage'],'parameters':p,'task_fingerprint':task_identity(p),'source_replay':True,'plot_path':re.search(r'!\[\]\((.*?)\)',q[':question/problem'])[1]}}

def sample(level,rng,permutation):
 """Independent numeric slots and eligible member/nonmember label positions."""
 true_labels={permutation[i]for i in BASE_TRUTH[level]}
 for _ in range(10000):
  m=rng.choice([1,2,3,4])if level=='easy'else rng.choice([-2,-3,-4,-5])if level=='moderate'else rng.choice([Fraction(a,b)for b in(2,3)for a in(-5,-4,-3,-2,-1,1,2,3,4,5)if math.gcd(a,b)==1])
  b=rng.randint(-4,6);xs=sorted(rng.sample(range(-4,5),3));points=[]
  for label,x in zip('ABC',xs):
   expected=m*x+b
   if label in true_labels:
    if Fraction(expected).denominator!=1:break
    y=int(expected)
   else:
    # Integral nonmember grid point. Rational slope still requires substitution.
    y=math.floor(expected)+rng.choice([-2,-1,1,2])
    if y==expected:y+=1
   points.append([x,y])
  if len(points)==3 and all(-10<=y<=10 for x,y in points):return {'m':str(m)if isinstance(m,Fraction)else m,'b':b,'points':points}
 raise RuntimeError('numeric slot sampler exhausted')

def _validate_parameters(p,level,permutation):
 if set(p)!= {'m','b','points'}:raise ValueError('parameters require m, b, points')
 m,b=_frac(p['m']),_frac(p['b']);points=p['points']
 if not m or len(points)!=3 or b.denominator!=1:raise ValueError('nonzero slope, integer intercept and three points required')
 for xy in points:
  if type(xy)not in(list,tuple)or len(xy)!=2:raise ValueError('point pair required')
  for v in xy:_int(v,'coordinate')
 if len({tuple(xy)for xy in points})!=3:raise ValueError('distinct points required')
 truth={label for label,(x,y)in zip('ABC',points)if Fraction(y)==m*x+b}
 expected={permutation[i]for i in BASE_TRUTH[level]}
 if truth!=expected:raise ValueError('point truth roles disagree with selected profile')
 if level=='easy'and (m<=0 or m.denominator!=1):raise ValueError('easy positive integral slope')
 if level=='moderate'and(m>=0 or m.denominator!=1):raise ValueError('moderate negative integral slope')
 if level=='hard'and m.denominator not in(2,3):raise ValueError('authored hard rational slope with denominator 2/3')
 return truth

def render_plots(p,output_dir=None):
 """Matplotlib plot only; coordinates and labels are supplied, never resampled."""
 output_dir=Path(output_dir or HERE/'assets');output_dir.mkdir(parents=True,exist_ok=True)
 key=hashlib.sha256(('renderer-v3:'+json.dumps(p,sort_keys=True)).encode()).hexdigest();target=output_dir/(key+'.png')
 if not target.exists():
  import subprocess
  request={'parameters':p,'output':str(target.resolve())};inp=output_dir/(key+'-request.json');inp.write_text(json.dumps(request))
  try:subprocess.run([sys.executable,'-B',str(HERE/'render.py'),str(inp)],check=True,text=True)
  finally:inp.unlink(missing_ok=True)
 return target.resolve()

def _subset(labels):
 labels=sorted(labels);return ' and '.join('$'+x+'$'for x in labels)+' only'

def _solution(old,p,level):
 sol=old[':question/worked-solution'];op=_defaults(old);eq=equation(p);oeq=equation(op);truth=[Fraction(y)==_frac(p['m'])*x+_frac(p['b'])for x,y in p['points']]
 # Shared wording and layout remain source-authored. Each operative stage is replaced.
 for label,(x,y),(ox,oy)in zip('ABC',p['points'],op['points']):sol=sol.replace(label+'('+str(ox)+','+str(oy)+')',label+'('+str(x)+','+str(y)+')')
 sol=sol.replace(oeq,eq)
 for label,ok in zip('ABC',truth):
  sol=re.sub(r'(Substituting the point \$'+label+r'\([^$]+\)\$ results in )(?:a )?(?:true|false) statement:',lambda m:m[1]+('a true'if ok else'a false')+' statement:',sol)
  sol=re.sub(r'Therefore, the point \$'+label+r'\$ does (?:\*not\* |not )?lie on the line\.',lambda m:'Therefore, the point $'+label+'$ does '+(''if ok else('*not* 'if level=='moderate'and label=='A'else'not '))+'lie on the line.',sol)
 blocks=iter(zip(p['points'],truth))
 def block(_):
  (x,y),ok=next(blocks);b=_frac(p['b']);rhs=tex(p['m'])+'('+str(x)+')'+('+'+tex(b)if b>=0 else tex(b));v=_frac(p['m'])*x+b
  return r'\begin{aligned}y & ='+eq+r' \\ ('+str(y)+') & ='+rhs+r' \\ '+str(y)+' & ='+tex(v)+r'\,'+('✓'if ok else r'\times ')+r'\end{aligned}'
 sol=re.sub(r'\\begin\{aligned\}.*?\\end\{aligned\}',block,sol,flags=re.S)
 yes=[label for label,ok in zip('ABC',truth)if ok]
 sol=re.sub(r'Finally, only points? .*? lie(?:s)? on the line\.',lambda _:'Finally, only '+('point 'if len(yes)==1 else'points ')+' and '.join('$'+x+'$'for x in yes)+(' lies'if len(yes)==1 else' lie')+' on the line.',sol)
 # Preserve source's missing article in easy C sentence only at exact source replay.
 return sol

@_fmt.checked_math_content
def generate(level,seed=0,template=None,parameters=None,bank_profile=None,output_dir=None):
 _seed(seed)
 if level not in SUPPORTED_LEVELS:raise ValueError('Unsupported level: '+str(level))
 template=template or SOURCE_TEMPLATES[level]
 if template not in SOURCE_TEMPLATES_BY_LEVEL.get(level,[]) and not(level=='hard'and template=='authored-rational'):raise ValueError('template/level mismatch')
 # Profile is selected as a complete object BEFORE numbers. Permutation maps roles.
 rng=random.Random(seed)
 if bank_profile is None and template in SOURCES and parameters==DEFAULTS[template]:permutation=tuple('ABC')
 else:permutation=tuple(rng.choice(ROLE_PERMUTATIONS))if bank_profile is None else tuple(bank_profile.split(':')[-1])
 if permutation not in ROLE_PERMUTATIONS:raise ValueError('unknown role profile')
 profile=level+'-source-bank:'+''.join(permutation)
 if bank_profile is not None and bank_profile!=profile:raise ValueError('unknown complete bank profile')
 p=copy.deepcopy(parameters)if parameters is not None else sample(level,rng,permutation)
 truth=_validate_parameters(p,level,permutation)
 if template in SOURCES and p==DEFAULTS[template]and permutation==tuple('ABC'):
  rec=replay_raw(template);rec['generation'].update({'bank_profile':profile,'seed':seed,'math_format':_fmt.FORMAT_VERSION});return rec
 old=SOURCES['q-102142'if level=='hard'else template];eq=equation(p);old_eq=equation(_defaults(old))
 asset=str(render_plots(p,output_dir));prompt=re.sub(r'!\[\]\(.*?\)',lambda _:'![]('+asset+')',old[':question/problem']).replace(old_eq,eq)
 solution=_solution(old,p,'moderate'if level=='hard'else level)
 rolemap=dict(zip('ABC',permutation));bank=[_subset({rolemap[a]for a in expr.split()})for expr in PROFILES[level]]
 sets=[frozenset(re.findall(r'\$([ABC])\$',v))for v in bank]
 if len(set(sets))!=5 or sum(v==truth for v in sets)!=1:raise ValueError('whole-bank collision or ambiguous key')
 # Content identity includes whole bank; mathematical dedup remains bank-independent.
 qid=_identity({'problem':prompt.split('\n\n',1)[1],'solution':solution,'bank':sorted(bank),'field':'radio selection'});fid=str(uuid.uuid5(uuid.UUID(qid),'selection'))
 answers=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),v)),':answer/type':':answer.type/text',':answer/value':_fmt.normalize_prose(v)}for v in bank]
 correct=next(a[':answer/id']for a in answers if frozenset(re.findall(r'\$([ABC])\$',a[':answer/value']))==truth)
 field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':WRAPPER['record'][':knowledge-point/title']},'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':_fmt.normalize_prose(prompt),':question/worked-solution':_fmt.normalize_prose(solution),':question/answer-fields':[field]},'generation':{'version':VERSION,'source_basis':WRAPPER['basis'],'source_lineage':WRAPPER['lineage'],'template':template,'source_id':None if level=='hard'else template,'authored_extension':level=='hard','bank_profile':profile,'role_permutation':''.join(permutation),'seed':seed,'parameters':p,'task_fingerprint':task_identity(p),'plot_path':asset,'plot_renderer':'Matplotlib','dependencies':{'sympy':s.__version__}}}

def easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
def moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
def hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)
def batch(level,count=1,seed=0,exclude=None):
 _seed(seed);_int(count,'count')
 if level not in(*SUPPORTED_LEVELS,'all'):raise ValueError('unsupported difficulty')
 if count<1 or count>CAPACITY_LIMIT:raise ValueError('count outside conservative bounded request capacity 1..10000')
 out=[];seen=set(exclude or [])
 for current in SUPPORTED_LEVELS if level=='all'else(level,):
  got=0
  for i in range(max(100,count*50)):
   r=generate(current,seed+i);key=r['generation']['task_fingerprint']
   if key in seen:continue
   seen.add(key);out.append(r);got+=1
   if got==count:break
  if got!=count:raise ValueError('bounded unique sampling exhausted for '+current)
 return out

def markdown(rec):
 q=rec['question'];fields=q[':question/answer-fields'];parts=[q[':question/problem']]
 for f in fields:parts.append('\n'.join('- '+a[':answer/value']for a in f[':answer-field/choices']))
 return '\n\n'.join(parts+[q[':question/worked-solution']])
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=(*SUPPORTED_LEVELS,'all'),default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=('json','markdown'),default='json');ap.add_argument('--output',type=Path);args=ap.parse_args()
 try:records=batch(args.difficulty,args.count,args.seed)
 except(ValueError,TypeError)as e:ap.error(str(e))
 output=json.dumps(records,indent=2)+'\n'if args.format=='json'else'\n\n---\n\n'.join(markdown(r)for r in records)+'\n'
 if args.output:args.output.write_text(output)
 else:print(output,end='')
