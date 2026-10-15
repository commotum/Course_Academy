#!/usr/bin/env python3
"""Frozen draft, basis 2275. Two reciprocal linear terms and one logarithm."""
import sys
sys.dont_write_bytecode=True
import argparse,copy,hashlib,importlib.util,itertools,json,random,uuid
from pathlib import Path
import sympy as sp
PACKAGE=Path(__file__).with_suffix('')
def private(name):
 spec=importlib.util.spec_from_file_location('kp64208_draft_'+name,PACKAGE/(name+'.py'));mod=importlib.util.module_from_spec(spec);sys.modules[spec.name]=mod;spec.loader.exec_module(mod);return mod
fmt=private('math_format');parser=private('parser')
KP_ID=17592186064208;KP_UUID='af32f07f-fa65-5ede-a506-735dc2d3a5ef'
TITLE='Integrating a Combination of Linear Rational Functions Using the General Formula'
VERSION='combined-linear-rational-b2275-draft-v2'
PROFILES=json.loads((PACKAGE/'contract.json').read_text())['profiles']
SOURCE=json.loads((PACKAGE/'source.json').read_text())['record']
LEVELS=('easy','moderate','hard')
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def ident(v):return str(uuid.uuid5(uuid.UUID(KP_UUID),digest(v)))
def tex(v):return '' if v==1 else '-' if v==-1 else sp.latex(v).replace('- ', '-')
def coefficient(r,p):
 a,b,c=map(sp.Integer,p)
 return {'inv_a':1/a,'neg_inv_a':-1/a,'a':a,'neg_a':-a,'inv_b':1/b,'neg_inv_b':-1/b,'b':b,'neg_b':-b,'one':sp.Integer(1),'two':sp.Integer(2),'quarter':sp.Rational(1,4),'two_inv_a':2/a}[r]
def denominators(style,p):
 a,b,c=p;ax='x' if a==1 else str(a)+'x'
 def linear(d):return ax+('+' if d>0 else '')+str(d)
 if style.startswith('opposite') and style!='opposite-asymmetric':return [str(b)+'+'+ax,str(c)+'-'+ax]
 if style=='opposite-asymmetric':return [linear(b),str(c)+'-'+ax]
 return [linear(b),linear(c)]
def allowed(sid,p,difficulty='hard'):
 if len(p)!=3 or any(type(z)!=int for z in p):return False
 a,b,c=p;style=PROFILES[sid]['style']
 if a<1 or a>8 or b==0 or c==0 or abs(b)>9 or abs(c)>9:return False
 if b==c and style.startswith('same') or b+c==0 and style.startswith('opposite'):return False
 if sid.startswith('authored'):
  return a==1 if difficulty=='easy' else 2<=a<=4 if difficulty=='moderate' else 2<=a<=8
 if sid=='q-49521-completed':return a==1 and b==c and b>=2
 if style=='opposite-unit':return a==1 and b==c and b>=1
 if style=='same-unit':return a==1 and b>=2 and c==-b
 if style=='opposite-symmetric':return 2<=a<=8 and b>=1 and c==b
 if style=='same-symmetric':return 2<=a<=8 and b>=1 and c==-b
 if style=='opposite-asymmetric':return 2<=a<=8 and -9<=b<=-2 and 1<=c<=9
 return False

def _render(sid,p):
 t=PROFILES[sid];ds=denominators(t['style'],p)
 def render(z):
  for k,v in {'@@D1@@':ds[0],'@@D2@@':ds[1],'@@INV@@':tex(sp.Rational(1,p[0]))}.items():z=z.replace(k,v)
  return z
 return render(t['prompt']),render(t['solution']),[fmt.normalize_tex(render(z['value']).replace('@@COEF@@',tex(coefficient(z['recipe'].split(':')[0],p)))) for z in t['bank']]
def _bank_valid(sid,p):
 _,_,values=_render(sid,p);expr=[parser.scalar(v) for v in values];derivs=[parser.derivative(v) for v in expr]
 t=PROFILES[sid];a,b,c=map(sp.Integer,p);x=parser.x;d=-a if t['style'].startswith('opposite') else a;integrand=1/(a*x+b)+1/(d*x+c)
 # Full profile rejection includes wrong/wrong equivalence modulo arbitrary C.
 for i,j in itertools.combinations(range(len(values)),2):
  if sp.cancel(derivs[i]-derivs[j])==0:return False
 return [sp.cancel(v-integrand)==0 for v in derivs]==[v['correct'] for v in t['bank']]
def profiles(difficulty):return ['authored-same','authored-opposite'] if difficulty in ('easy','moderate') else list(PROFILES)
def source_case(source_id):
 """Raw public evidence; incomplete/canonical records never eligible for serving."""
 raw=SOURCE[':knowledge-point/canonical-example'] if source_id=='e-451' else next(q for q in SOURCE[':knowledge-point/questions'] if q[':question/math-academy-id']==source_id)
 fields=raw.get(':question/answer-fields',[])
 eligible=bool(fields and raw.get(':question/difficulty') and raw.get(':question/worked-solution') and all(f.get(':answer-field/correct') for f in fields))
 return {'source_id':source_id,'public_replay_eligible':eligible,'raw':copy.deepcopy(raw)}
@fmt.checked_math_content
def generate(difficulty='hard',seed=0,template=None,parameters=None,bank_profile=None):
 if difficulty not in LEVELS:raise ValueError('difficulty must be easy, moderate, or hard')
 rng=random.Random(seed);sid=bank_profile or template or rng.choice(profiles(difficulty))
 if sid not in PROFILES:raise ValueError('unknown bank profile')
 if difficulty!='hard' and not sid.startswith('authored'):raise ValueError('source profiles retain their hard band')
 if parameters is None:
  for attempt in range(500):
   a=1 if difficulty=='easy' else rng.randint(2,4) if difficulty=='moderate' else rng.randint(1,8);p=[a,rng.choice(list(range(-9,0))+list(range(1,10))),rng.choice(list(range(-9,0))+list(range(1,10)))]
   style=PROFILES[sid]['style']
   if not sid.startswith('authored'):
    if style=='opposite-unit' or sid=='q-49521-completed':p=[1,rng.randint(2,9),0];p[2]=p[1]
    elif style=='same-unit':p=[1,rng.randint(2,9),0];p[2]=-p[1]
    elif style in ('same-symmetric','opposite-symmetric'):p=[rng.randint(2,8),rng.randint(1,9),0];p[2]=-p[1] if style.startswith('same') else p[1]
    elif style=='opposite-asymmetric':p=[rng.randint(2,8),-rng.randint(2,9),rng.randint(1,9)]
   if allowed(sid,p,difficulty) and _bank_valid(sid,p):break
  else:raise ValueError('whole-profile sampler exhausted')
 else:
  p=list(parameters)
  if not allowed(sid,p,difficulty) or not _bank_valid(sid,p):raise ValueError('invalid parameters or colliding complete bank')
 prompt,solution,values=_render(sid,p);prompt=fmt.normalize_prose(prompt);solution=fmt.normalize_prose(solution)
 # IDs depend on complete normalized content and unordered bank, never seed/profile.
 content={'problem':prompt,'solution':solution,'difficulty':difficulty,'bank':sorted((v,bool(r['correct'])) for v,r in zip(values,PROFILES[sid]['bank']))}
 qid=ident(content);fid=ident([qid,'selection']);choices=[{':answer/id':ident([fid,v]),':answer/type':':answer.type/math',':answer/value':v} for v in values]
 correct=next(c[':answer/id'] for c,r in zip(choices,PROFILES[sid]['bank']) if r['correct'])
 q={':question/id':qid,':question/problem':prompt,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+difficulty,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',correct]}]}
 integrand=parser.integral_operands(prompt)[0];rational=sp.cancel(integrand);poles=sorted(set([-sp.Rational(p[1],p[0]),sp.Rational(p[2],p[0]) if PROFILES[sid]['style'].startswith('opposite') else -sp.Rational(p[2],p[0])]))
 gen={'version':VERSION,'seed':seed,'template':'two-linear-reciprocals-single-log','bank_profile':sid,'profile':sid,'parameters':p,'source_ids':[PROFILES[sid].get('source_id',sid)] if not sid.startswith('authored') else [],'origin':'authored_extension' if sid.startswith('authored') else 'authored_completion' if sid.endswith('completed') else 'observed_template','source_basis':2275,'constant_mapping':'C = log(K)/'+str(p[0]),'domain':{'variable':'x real','excluded_poles':list(map(str,poles)),'K':'positive arbitrary separately on each real connected component'},'mathematical_fingerprint':digest(str(rational)),'recipes':[r['recipe'] for r in PROFILES[sid]['bank']],'sympy':sp.__version__}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':gen}
def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)
def generate_hard(seed=0,**kw):return generate('hard',seed,**kw)
def batch(difficulty,count=1,seed=0):
 if count<1:raise ValueError('positive count required')
 out=[];used=set()
 for attempt in range(count*200):
  z=generate(difficulty,seed+attempt);fp=z['generation']['mathematical_fingerprint']
  if fp in used:continue
  out.append(z);used.add(fp)
  if len(out)==count:return out
 raise ValueError('unique mathematical task domain exhausted')
def markdown(z):
 q=z['question'];f=q[':question/answer-fields'][0]
 return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$' for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=(*LEVELS,'all'),default='all');ap.add_argument('--count',type=int,default=1);ap.add_argument('--seed',type=int,default=0);ap.add_argument('--format',choices=('json','markdown'),default='json');a=ap.parse_args();rows=[z for d in LEVELS if a.difficulty in (d,'all') for z in batch(d,a.count,a.seed)]
 print(json.dumps(rows,indent=2) if a.format=='json' else '\n\n---\n\n'.join(map(markdown,rows)))
