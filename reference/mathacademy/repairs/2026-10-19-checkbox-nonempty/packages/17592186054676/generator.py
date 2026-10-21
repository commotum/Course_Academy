"""Three point membership: source profiles, independent truth roles, local plots.
Derived from the supplied 17592186054676-draft; see instructional-account.md.
"""
import argparse, copy, hashlib, itertools, json, os, random, re, uuid
from fractions import Fraction
from pathlib import Path
import math_format as _fmt
from render import render_plot
HERE=Path(__file__).resolve().parent
KP_ID=17592186054676;KP_UUID='3123f8ed-a1ca-52b7-8427-2f3b60d9e68a';VERSION='3.0.1'
WRAPPER=json.loads((HERE/'source.json').read_text())
KP=WRAPPER['material']['kp']
SOURCES={q.get(':question/math-academy-id') or q[':question/id']:q for q in KP[':knowledge-point/questions']}
SUPPORTED_LEVELS=('easy','moderate','hard')
SOURCE_TEMPLATES_BY_LEVEL={level:[k for k,q in SOURCES.items() if q.get(':question/difficulty',{}).get(':db/ident')==':question.difficulty/'+level] for level in SUPPORTED_LEVELS}
CAPACITY_LIMIT=10000

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
 q=_normal(SOURCES[source_id]);p=copy.deepcopy(DEFAULTS[source_id]);return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':KP[':knowledge-point/title']},'question':q,'generation':{'version':VERSION,'source_id':source_id,'template':source_id,'source_basis':WRAPPER['basis'],'source_lineage':WRAPPER['lineage'],'parameters':p,'task_fingerprint':task_identity(p),'source_replay':True,'plot_path':re.search(r'!\[\]\((.*?)\)',q[':question/problem'])[1]}}

def source_bank(source_id):
 return [a[':answer/value'] for a in SOURCES[source_id][':question/answer-fields'][0][':answer-field/choices']]

def answer_set(value):return frozenset(re.findall(r'\$([ABC])\$',value))

def sample(level,rng,selected):
 """Requested subset is chosen BEFORE compatible numerical data."""
 members=set('ABC')-set(selected) if level=='hard' else set(selected)
 attempts=0
 while attempts<10000:
  attempts+=1
  m=rng.choice([1,2,3,4] if level=='easy' else [-2,-3,-4,-5])
  b=rng.randint(-6 if level=='hard' else -4,6)
  xs=rng.sample(range(-4,5),3)
  points=[[x,m*x+b+(0 if label in members else rng.choice([-3,-2,-1,1,2,3]))] for label,x in zip('ABC',xs)]
  if all(-9<=y<=9 for x,y in points):return {'m':m,'b':b,'points':points},attempts
 raise RuntimeError('numeric sampler exhausted')

def _validate_parameters(p,level,selected):
 if set(p)!={'m','b','points'}:raise ValueError('parameters require m,b,points')
 for key in ('m','b'):_int(p[key],key)
 if not p['m'] or len(p['points'])!=3:raise ValueError('nonzero slope and three points required')
 for xy in p['points']:
  if len(xy)!=2:raise ValueError('coordinate pair required')
  for v in xy:_int(v,'coordinate')
 if len({tuple(xy) for xy in p['points']})!=3:raise ValueError('distinct points required')
 if (p['m']>0)!=(level=='easy'):raise ValueError('slope sign disagrees with source band')
 members={a for a,(x,y) in zip('ABC',p['points']) if y==p['m']*x+p['b']}
 actual=set('ABC')-members if level=='hard' else members
 if actual!=set(selected):raise ValueError('coordinates disagree with requested subset')
 return members

def render_plots(p,output_dir=None):
 output_dir=output_dir or os.environ.get('COURSE_ACADEMY_GENERATOR_OUTPUT_DIR')
 if not output_dir:raise ValueError('COURSE_ACADEMY_GENERATOR_OUTPUT_DIR or explicit output_dir required')
 out=Path(output_dir).resolve();out.mkdir(parents=True,exist_ok=True)
 key=hashlib.sha256(('point-grid-v4:'+json.dumps(p['points'])).encode()).hexdigest()
 target=out/(key+'.png')
 if not target.exists():render_plot(p,target)
 return target

def _subset(labels):
 labels=sorted(labels);return ' and '.join('$'+x+'$'for x in labels)+' only'

def _solution(old,p,level):
 # Preserve source's coordinate-reading, rule, three tests and final decision stages.
 eq=equation(p);m=p['m'];b=p['b'];members=[]
 intro='The plotted points correspond to the $xy$-pairs '+', '.join('$'+a+'('+str(x)+','+str(y)+')$' for a,(x,y) in zip('ABC',p['points']))+'.'
 rule='To check whether a point lies on the line, we substitute the coordinates of the point into the equation and determine whether the resulting statement is true.'
 parts=[intro,rule]
 for a,(x,y) in zip('ABC',p['points']):
  val=m*x+b;ok=y==val
  if ok:members.append(a)
  rhs=('' if m==1 else '-' if m==-1 else str(m))+'('+str(x)+')'+('+'+str(b) if b>0 else str(b) if b<0 else '')
  parts.extend(['- Substituting the point $'+a+'('+str(x)+','+str(y)+')$ results in a '+('true' if ok else 'false')+' statement:',
   '$$\n'+r'\begin{aligned}y &= '+eq+r' \\ ('+str(y)+r') &= '+rhs+r' \\ '+str(y)+' &= '+str(val)+r' && '+(r'\checkmark' if ok else r'\times')+r'\end{aligned}'+'\n$$',
   'Therefore, the point $'+a+'$ does '+('' if ok else 'not ')+'lie on the line.'])
 selected=[a for a in 'ABC' if (a not in members if level=='hard' else a in members)]
 subject=('point ' if len(selected)==1 else 'points ')+' and '.join('$'+a+'$' for a in selected)
 verb=('does not lie' if len(selected)==1 else 'do not lie') if level=='hard' else ('lies' if len(selected)==1 else 'lie')
 parts.append('Finally, only '+subject+' '+verb+' on the line.')
 return '\n\n'.join(parts)

@_fmt.checked_math_content
def generate(level,seed=0,template=None,parameters=None,selected=None,output_dir=None,choice_order=None):
 _seed(seed)
 if level not in SUPPORTED_LEVELS:raise ValueError('Unsupported difficulty: '+str(level))
 rng=random.Random(seed)
 template=template or rng.choice(SOURCE_TEMPLATES_BY_LEVEL[level])
 if template not in SOURCE_TEMPLATES_BY_LEVEL[level]:raise ValueError('template/level mismatch')
 bank=source_bank(template)
 if selected is None:
  if parameters is not None:
   members={a for a,(x,y) in zip('ABC',parameters['points']) if y==parameters['m']*x+parameters['b']}
   selected=set('ABC')-members if level=='hard' else members
  else:selected=answer_set(rng.choice(bank))
 selected=frozenset(selected)
 if selected not in list(map(answer_set,bank)):raise ValueError('selected subset is absent from profile')
 p,attempts=(copy.deepcopy(parameters),0) if parameters is not None else sample(level,rng,selected)
 _validate_parameters(p,level,selected)
 # Exact captured provenance belongs only to replay_raw. Original numerical
 # parameters use this same publishable path and normal delivery deduplication.
 old=SOURCES[template];eq=equation(p)
 asset=str(render_plots(p,output_dir))
 prompt=re.sub(r'!\[\]\(.*?\)',lambda _:'![]('+asset+')',old[':question/problem'])
 prompt=prompt.replace(equation(DEFAULTS[template]),eq)
 prompt=prompt.replace('$y='+eq+'.$','$y='+eq+'$.').replace('$y='+eq+'?$','$y='+eq+'$?')
 solution=_solution(old,p,level)
 if choice_order is None:rng.shuffle(bank)
 else:
  if sorted(choice_order)!=list(range(5)):raise ValueError('choice_order must permute 0..4')
  bank=[bank[i] for i in choice_order]
 # Asset directory must not affect content identity.
 content={'parameters':p,'profile':template,'bank':sorted(bank),'level':level}
 qid=_identity(content);fid=str(uuid.uuid5(uuid.UUID(qid),'selection'))
 answers=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),v)),':answer/type':':answer.type/text',':answer/value':_fmt.normalize_prose(v)} for v in bank]
 correct=next(a[':answer/id'] for a in answers if answer_set(a[':answer/value'])==selected)
 field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':KP[':knowledge-point/title']},'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':_fmt.normalize_prose(prompt),':question/worked-solution':_fmt.normalize_prose(solution),':question/answer-fields':[field]},'generation':{'version':VERSION,'source_basis':WRAPPER['basis'],'source_lineage':WRAPPER['lineage'],'template':template,'source_id':template,'bank_profile':template,'seed':seed,'parameters':p,'selected':sorted(selected),'attempts':attempts,'task_fingerprint':task_identity(p),'plot_path':asset,'plot_renderer':'Matplotlib'}}

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

# Every learner-facing checkbox question has a nonempty correct selection.
from generator_policy import nonempty_checkbox as _nonempty_checkbox
for _policy_name in ['batch', 'generate']:
    globals()[_policy_name] = _nonempty_checkbox(globals()[_policy_name])

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=(*SUPPORTED_LEVELS,'all'),default='easy');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=('json','markdown'),default='json');ap.add_argument('--output',type=Path);args=ap.parse_args()
 try:records=batch(args.difficulty,args.count,args.seed)
 except(ValueError,TypeError)as e:ap.error(str(e))
 output=json.dumps(records,indent=2)+'\n'if args.format=='json'else'\n\n---\n\n'.join(markdown(r)for r in records)+'\n'
 if args.output:args.output.write_text(output)
 else:print(output,end='')
