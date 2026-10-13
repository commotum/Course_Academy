#!/usr/bin/env python3
"""Creating Parallel Vectors, math basis1356. Steps3–7 only; no database calls.

Source families are single and paired scale diagrams (unrated, no solution/key).
Raw parameterized public profiles preserve all omissions and original assets at
original geometry; these are evidence only. Authored normal radio-image defaults
use full method-derived banks, exact scales, and inferred fixed solutions.
Easy: one positive integer enlargement; moderate: one negative noninteger scale;
hard: one positive integer and one negative noninteger vector together. Every
level repeats exactly its stated workload, without progression. Sample and
explicit inputs obey identical finite domains. Orientation has six geometric
variants; source common vector length does not inflate task fingerprints.

API generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None)
and generate_easy/moderate/hard. CLI --difficulty/--seed/--count/--format.
"""
from __future__ import annotations
import argparse,hashlib,json,math,os,random,subprocess,sys,tempfile,uuid
from pathlib import Path
import sympy as sp
KP_ID=17592186096649;KP_UUID='dc49f831-8e1d-5fb4-8952-1dd4ee3bfa02';TITLE='Creating Parallel Vectors';VERSION='parallel-creation-1'
HERE=Path(__file__).resolve().with_suffix('');ROOT=HERE.parents[2]
PLOT_DIR=HERE/'plots'
CAPTURE=json.loads((HERE/'source.json').read_text());SOURCES={q[':question/math-academy-id']:q for q in CAPTURE['record'][':knowledge-point/questions']}
ANGLES=(0,30,60,120,210,300);POS=(2,3,4);NEG=('-1/2','-2/3','-3/2','-4/3')
RAW={'observed_pair':('q-11324','pair',{'angle':30,'length':'1','scales':['3','-1']}),'observed_single':('q-12140','single',{'angle':60,'length':'2','scales':['-1/2']})}

def digest(obj):return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(obj):return str(uuid.uuid5(uuid.NAMESPACE_URL,digest(obj)))
def tex(x):return sp.latex(sp.Rational(x)).replace("- ","-")
def scalar(x):
 x=sp.Rational(x)
 return ('-' if x==-1 else '' if x==1 else tex(x))+ 'a'
def exact_vec(p):
 a=sp.pi*p['angle']/180;n=sp.Rational(p['length'])
 return (sp.simplify(n*sp.cos(a)),sp.simplify(n*sp.sin(a)))
def validate_parameters(level,template,p,raw=False):
 if set(p)!={'angle','length','scales'}:raise ValueError('Expected angle,length,scales')
 if p['angle'] not in ANGLES:raise ValueError('Orientation outside finite supported catalog')
 if sp.Rational(p['length']) not in (1,2):raise ValueError('Length must be1 or2')
 n=2 if template=='pair' else 1
 if len(p['scales'])!=n:raise ValueError('Wrong number of requested vectors')
 s=[sp.Rational(x) for x in p['scales']]
 if raw:
  if template=='pair' and not (s[0] in POS and s[1] in (-1,sp.Rational('-1/2'),sp.Rational('-3/2'))):raise ValueError('Raw paired evidence bounds')
  if template=='single' and s[0] not in [sp.Rational(x) for x in NEG]:raise ValueError('Raw single evidence bounds')
 elif level=='easy':
  if template!='single' or s[0] not in POS:raise ValueError('Easy is one positive integer enlargement')
 elif level=='moderate':
  if template!='single' or str(s[0]) not in NEG:raise ValueError('Moderate is one negative noninteger scaling')
 elif level=='hard':
  if template!='pair' or s[0] not in POS or str(s[1]) not in NEG:raise ValueError('Hard is paired integer/noninteger sign scaling')
 else:raise ValueError('Invalid difficulty')
 return {'angle':int(p['angle']),'length':str(sp.Rational(p['length'])),'scales':[str(x) for x in s]}

def bank_vectors(p,profile,template):
 """Choose full bank before parameters. Every wrong operation is one whole diagram."""
 a=exact_vec(p);s=[sp.Rational(x) for x in p['scales']]
 mul=lambda k:tuple(sp.simplify(k*x) for x in a)
 horizontal=lambda k:(sp.Rational(p['length'])*k,sp.Integer(0))
 if profile=='observed_pair':
  m,n=s
  return [[mul(m),mul(n)],[mul(m),horizontal(-n)],[mul(1),mul(2*n)],[mul(1),mul(n)],[mul(1),horizontal(2*n)]]
 if profile=='observed_single':
  k=s[0]
  return [[mul(k)],[mul(2*k)],[horizontal(-k)],[horizontal(k)],[mul(-2*k)]]
 if template=='single':
  k=s[0]
  return [[mul(k)],[mul(-k)],[mul(1/k)],[mul(-1/k)],[mul(1)]]
 m,n=s
 return [[mul(m),mul(n)],[mul(-m),mul(n)],[mul(m),mul(-n)],[mul(1/m),mul(n)],[mul(m),mul(1/n)]]

def eligible(p,profile,template):
 b=bank_vectors(p,profile,template)
 keys=[tuple(tuple(v) for v in row) for row in b]
 if len(set(keys))!=5:raise ValueError('Reject entire bank: duplicate/equivalent diagrams')
 target=keys[0]
 if sum(k==target for k in keys)!=1:raise ValueError('Ambiguous target')
 return b

def plot_spec(vectors,labels,allvectors):
 # Shared viewport and unit scale for prompt and EVERY choice. Translation is incidental.
 base=allvectors[0][0];norm=math.hypot(float(base[0]),float(base[1]));normal=(-float(base[1])/norm,float(base[0])/norm)
 paired=[(2.5*normal[0],2.5*normal[1]),(-2.5*normal[0],-2.5*normal[1])]
 tails=paired if len(vectors)==2 else [(0,0)]
 points=[(0,0)]
 for row in allvectors:
  ts=paired if len(row)==2 else [(0,0)]
  for t,v in zip(ts,row):points.extend([t,(t[0]+float(v[0]),t[1]+float(v[1]))])
 xs=[x for x,y in points];ys=[y for x,y in points];cx=(min(xs)+max(xs))/2;cy=(min(ys)+max(ys))/2
 extent=max(max(xs)-min(xs),max(ys)-min(ys))+4.0
 # Large separation of paired labels; no backgrounds/masks are used.
 return {'renderer_version':'3','bounds':[[cx-extent/2,cx+extent/2],[cy-extent/2,cy+extent/2]],'label_offset':1.0,'vectors':[{'tail':list(t),'vector':[float(x) for x in v],'label':label,'color':('black' if label=='a' else '#2c72ae' if i==0 else '#e69f00')} for i,(t,v,label) in enumerate(zip(tails,vectors,labels))]}

def render(vectors,labels,allvectors):
 spec=plot_spec(vectors,labels,allvectors);key=digest(spec);out=PLOT_DIR/f'{key}.png'
 if not out.exists() or not out.with_suffix('.json').exists():
  out.parent.mkdir(exist_ok=True);spec['output']=str(out)
  fd,path=tempfile.mkstemp(prefix='input-',suffix='.json',dir=out.parent);os.close(fd)
  try:
   Path(path).write_text(json.dumps(spec));runtime='/home/jake/.local/share/uv/python/cpython-3.10.13-linux-x86_64-gnu/bin/python3.10'
   subprocess.run([runtime,str(HERE/'render.py'),path],check=True)
  finally:Path(path).unlink(missing_ok=True)
 return str(out.relative_to(ROOT))

def solution(p,images):
 s=[sp.Rational(x) for x in p['scales']];parts=[]
 if len(s)==2:parts.append('First, notice that both $'+scalar(s[0])+'$ and $'+scalar(s[1])+'$ must be parallel to $a$.')
 else:parts.append('First, notice that $'+scalar(s[0])+'$ must be parallel to $a$.')
 for i,k in enumerate(s):
  parts.append(('Now' if i==0 else 'Next')+', for the vector $'+scalar(k)+'$ we have the following:\n\n- The magnitude of $'+scalar(k)+'$ is $'+tex(abs(k))+'$ times the magnitude of $a$.\n- Vectors $a$ and $'+scalar(k)+'$ have '+('the same direction' if k>0 else 'opposite directions')+' since the factor $'+tex(k)+'$ is '+('positive' if k>0 else 'negative')+'.')
 parts.append('The required vectors are shown below.\n\n![]('+images[0]+')')
 return '\n\n'.join(parts)

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('difficulty')
 if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Only observed image radio fields are supported')
 rng=random.Random(seed);completed=bool(profile and profile.endswith('_completed'));public_profile=profile
 if completed:profile=profile.removesuffix('_completed')
 raw=profile in RAW
 if completed and not raw:raise ValueError('Unknown completed source profile')
 if profile and profile not in RAW and profile!='authored_operations':raise ValueError('Unknown profile')
 if raw:
  sourceid,t,defaults=RAW[profile];template=template or t
  if template!=t:raise ValueError('Profile/template mismatch')
  p=validate_parameters(level,template,defaults if parameters is None else parameters,True)
 else:
  template=template or ('pair' if level=='hard' else 'single');profile=profile or 'authored_operations'
  p=parameters if parameters is not None else {'angle':rng.choice(ANGLES),'length':rng.choice((1,2)),'scales':[str(rng.choice(POS))] if level=='easy' else [rng.choice(NEG)] if level=='moderate' else [str(rng.choice(POS)),rng.choice(NEG)]}
  p=validate_parameters(level,template,p)
 b=eligible(p,profile,template);a=exact_vec(p);labels=[scalar(k) for k in p['scales']];allvectors=[[a]]+b
 # Raster replay is licensed ONLY when semantic geometry matches the extracted original.
 original=raw and p==validate_parameters(level,template,RAW[profile][2],True)
 if original:
  src=SOURCES[sourceid];promptimage=src[':question/problem'].split('![](')[1].split(')')[0]
  images=[x[':answer/value'] for x in src[':question/answer-fields'][0][':answer-field/choices']]
 else:
  promptimage=render([a],['a'],allvectors);images=[render(row,labels,allvectors) for row in b]
 if template=='pair':prompt='![]('+promptimage+')\n\nThe vector $a$ is depicted above. Which of the following diagrams shows the vectors $'+labels[0]+'$ and $'+labels[1]+'$?'
 else:prompt='![]('+promptimage+')\n\nThe diagram above shows the vector $a$. Which of the following diagrams shows the vector $'+labels[0]+'$?'
 sol=solution(p,images)
 identity={'version':VERSION,'prompt':prompt,'solution':None if raw and not completed else sol,'bank':sorted(images),'difficulty':None if raw and not completed else level}
 qid=uid(identity);fid=uid([qid,'selection']);choices=[{':answer/id':uid([fid,path]),':answer/type':':answer.type/image',':answer/value':path} for path in images]
 field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices}
 q={':question/id':qid,':question/problem':prompt,':question/answer-fields':[field]}
 if raw:
  src=SOURCES[sourceid]
  q[':question/math-academy-id']=sourceid;q[':db/id']=src[':db/id']
  # Preserve source IDs/DB attributes independently of original image-path selection.
  q[':question/id']=src[':question/id'] if original and not completed else qid;field[':answer-field/id']=src[':question/answer-fields'][0][':answer-field/id'] if original and not completed else fid;field[':db/id']=src[':question/answer-fields'][0][':db/id']
  for new,old in zip(choices,src[':question/answer-fields'][0][':answer-field/choices']):new[':answer/id']=old[':answer/id'] if original and not completed else new[':answer/id'];new[':db/id']=old[':db/id']
 if not raw or completed:
  q[':question/difficulty']=':question.difficulty/'+level;q[':question/worked-solution']=sol
  field[':answer-field/correct']=[':answer/id',choices[0][':answer/id']]
 correct=choices[0][':answer/id'];rng.shuffle(choices)
 task={'angle':p['angle'],'scales':p['scales'],'template':template,'response':'specified scalar multiple diagrams'}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'parameters':p,'template':template,'bank_profile':public_profile if completed else profile,'source':{k:CAPTURE[k] for k in ('database','basis','lineage')},'actual_difficulty':None if raw and not completed else level,'difficulty_origin':'authored_inferred_completion' if completed else 'source_unrated' if raw else 'authored_missing_level','evidence_only':raw,'eligible_for_learning':not raw,'inferred_correct_answer_id':correct if raw else None,'inferred_worked_solution':sol if raw else None,'source_completion':completed,'mathematical_fingerprint':digest(task),'content_fingerprint':digest(identity),'python':sys.version.split()[0],'sympy':sp.__version__,'plot_geometry':[[[str(x) for x in v] for v in row] for row in b]}}

# Easy: one positive integer enlargement, no direction reversal.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# Moderate: one negative rational scale, reversal and fractional magnitude.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# Hard: two independently requested vectors, positive integer and negative fraction.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)

def markdown(r):
 q=r['question'];gen=r['generation'];raw=gen['evidence_only'];level=gen['actual_difficulty'] or 'unrated'
 label='Original source evidence' if raw and not gen['source_completion'] else 'Authored source completion' if raw else 'Generated variant'
 out='## '+label+' — '+level+'\n\n'
 out+=('Difficulty is authored.\n\n' if gen['actual_difficulty'] else 'Original difficulty, correct designation and solution are absent.\n\n')
 out+=q[':question/problem']+'\n\n';f=q[':question/answer-fields'][0]
 correct=f.get(':answer-field/correct',[':answer/id',gen['inferred_correct_answer_id']])[1]
 for i,a in enumerate(f[':answer-field/choices']):
  marker=' **(inferred correct)**' if raw else ' **(correct)**'
  out+=f'{chr(65+i)}. ![]('+a[':answer/value']+')'+(marker if a[':answer/id']==correct else '')+'\n\n'
 out+='Worked solution'+(' (authored inference; absent in source)' if raw else ' (authored)')+':\n\n'+q.get(':question/worked-solution',gen['inferred_worked_solution'])
 # Preview-only absolute paths; stored question and choice values are untouched.
 out=out.replace('![](images/','![](/media/jake/SSD/EDB/math/images/').replace('![](generate/','![]('+str(ROOT)+'/generate/')
 return out
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
 levels=('easy','moderate','hard') if args.difficulty=='all' else (args.difficulty,)
 records=[generate(l,args.seed+i,template=args.template,profile=args.profile) for l in levels for i in range(args.count)]
 print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
