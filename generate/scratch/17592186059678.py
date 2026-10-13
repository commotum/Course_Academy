#!/usr/bin/env python3
"""Bounded linear-scaling extension of the captured second-derivative profiles.

CLI: --difficulty easy|moderate --count N --seed N --format json|markdown.
No writes. Source syntax and sequence replay exactly at k=1. k=2..6 scales
all prompt coefficients, every intermediate derivative and the complete bank.
This conservative extension retains signed/fractional terms and field fragments;
it does not infer independent coefficient recipes from sparse source evidence.
"""
import argparse, hashlib, json, random, re, uuid
from pathlib import Path
try:
 import sympy as sp
except ModuleNotFoundError:
 import os,sys
 runtime=Path(__file__).resolve().parents[2]/'.venv/bin/python'
 os.execv(str(runtime),[str(runtime),str(Path(__file__).resolve()),*sys.argv[1:]])
KP_ID=17592186059678
KP_UUID='6afb4058-908a-5983-9c1e-78ee3fbadf44'
HERE=Path(__file__).with_suffix('')
SOURCE=json.loads((HERE/'source.json').read_text())
GENERATOR_UUID=str(SOURCE['record'].get(':knowledge-point/question-generator',{}).get(':question-generator/id',uuid.uuid5(uuid.UUID(KP_UUID),'question-generator')))
VERSION='1.0.0';SUPPORTED_LEVELS=('easy','moderate')
SOURCE_BASIS=SOURCE['basis'];LINEAGE=SOURCE['lineage'];TITLE=SOURCE['record'][':knowledge-point/title']
SOURCES={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
PROFILES={sid:(q[':question/difficulty'][':db/ident'].split('/')[-1],{'k':1}) for sid,q in SOURCES.items() if q.get(':question/answer-fields') and q.get(':question/worked-solution') and q.get(':question/difficulty') and all(f.get(':answer-field/correct') for f in q[':question/answer-fields'])}
x=sp.Symbol('x',positive=True)
FUNCTIONS={
 'q-10903':5*x**4+4*x**2,
 'q-342868':x**8/4+x-4/sp.sqrt(x),
 'q-104191':sp.log(x)+1/(6*x**2),
 'q-104192':4/sp.sqrt(x)+2*sp.sin(x),
 'q-10884':3*x**5+4*x**3-10*x**2,
 'q-342877':(6*x**3+2*x**2-8)/(2*x),
 'q-342966':6*sp.sqrt(x)+5*sp.cos(x),
 'q-342970':x**5+3*sp.sin(x)-1/x**2,
}
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(v):return str(uuid.uuid5(uuid.UUID(KP_UUID),v))
def candidates(sid):return [{'k':k} for k in range(1,7)]
def scale(t,k):
 """Scale one complete expression, retaining original internal notation."""
 if k==1:return t
 t=t.strip();tail=''
 while t.endswith(('.',r'\,',',')):
  if t.endswith(r'\,'):tail=r'\,'+tail;t=t[:-2]
  else:tail=t[-1]+tail;t=t[:-1]
 return str(k)+r'\left('+t+r'\right)'+tail

def problem(sid,k):
 t=SOURCES[sid][':question/problem']
 if k==1:return t
 # Scale the entire displayed function. Keep partial-response suffix separate.
 t=re.sub(r'(y\s*=\s*)(.*?)(\$)',lambda m:m[1]+scale(m[2],k)+m[3],t,count=1)
 if sid=='q-342970':t=t.replace(r'$-\,\frac{6}{{x}^{4}}$',r'$-\,\frac{'+str(6*k)+r'}{{x}^{4}}$')
 return t

def solution(sid,k):
 t=SOURCES[sid][':question/worked-solution']
 if k==1:return t
 def row(m):
  rhs=m[2]
  prefix=r'\frac{\text{d}}{\text{d}x}('
  if rhs.startswith(prefix) and rhs.endswith(')'):
   rhs=prefix+scale(rhs[len(prefix):-1],k)+')'
  else:rhs=scale(rhs,k)
  return m[1]+rhs
 # Preserve every original aligned row, operator, sentence and ordering.
 return re.sub(r'(& =)(.*?)(?= \\\\|\\end\{aligned\})',row,t,flags=re.S)

def generate(level,seed=0,template=None,parameters=None):
 if level not in SUPPORTED_LEVELS:raise ValueError('Unsupported difficulty: '+level)
 rng=random.Random(seed);sid=template or rng.choice([s for s,(l,_) in PROFILES.items() if l==level])
 if sid not in PROFILES or PROFILES[sid][0]!=level:raise ValueError('Unsupported profile')
 p=parameters or rng.choice(candidates(sid))
 if p not in candidates(sid):raise ValueError('Parameters outside bounded integer scale 1..6')
 k=p['k'];old=SOURCES[sid];correct=sp.diff(k*FUNCTIONS[sid],x,2)
 if sid=='q-342970':correct=sp.simplify(correct+6*k/x**4)
 first_derivative=sp.diff(k*FUNCTIONS[sid],x);task=digest([sid,k])
 qid=uid('question:'+VERSION+':'+task);fields=[]
 for of in old[':question/answer-fields']:
  fid=uid('field:'+qid+':'+of[':answer-field/key']);choices=[]
  for oa in of[':answer-field/choices']:
   aid=uid('answer:'+fid+':'+oa[':answer/id']);choices.append({':answer/id':aid,':answer/type':':answer.type/math',':answer/value':scale(oa[':answer/value'],k)})
  idx=next(i for i,a in enumerate(of[':answer-field/choices']) if a[':answer/id']==of[':answer-field/correct'][':answer/id'])
  fields.append({':answer-field/id':fid,':answer-field/key':of[':answer-field/key'],':answer-field/type':of[':answer-field/type'][':db/ident'],':answer-field/choices':choices,':answer-field/correct':[':answer/id',choices[idx][':answer/id']]})
 q={':question/id':qid,':question/problem':problem(sid,k),':question/worked-solution':solution(sid,k),':question/difficulty':':question.difficulty/'+level,':question/answer-fields':fields}
 # Mathematical identity is independent of seed, choice order and template identity.
 raw_fingerprint=digest(str(sp.expand(sp.diff(k*FUNCTIONS[sid],x,2))))
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'generator_id':GENERATOR_UUID,'version':VERSION,'seed':seed,'template':sid,'profile':sid,'parameters':p,'source_basis':SOURCE_BASIS,'lineage':LINEAGE,'source_question':old[':question/id'],'computed_correct':str(sp.expand(correct)),'computed_first_derivative':str(sp.expand(first_derivative)),'domain':'x>0 for radicals and logarithms; x!=0 for rational terms; otherwise real x','mathematical_fingerprint':raw_fingerprint,'dependencies':{'sympy':sp.__version__},'sampling_policy':'Explicit common positive integer scaling extension k=1..6; all source signs/exponents fixed; no independent-coefficient inference'}}

def batch(level,count,seed):
 if count<1:raise ValueError('Positive count required')
 if level not in SUPPORTED_LEVELS:raise ValueError('Unsupported difficulty: '+level)
 options=[(s,p) for s,(l,_) in PROFILES.items() if l==level for p in candidates(s)]
 if count>len(options):raise ValueError('finite-limit: '+str(len(options)))
 random.Random(seed).shuffle(options)
 return [generate(level,seed,s,p) for s,p in options[:count]]
def markdown(r):
 q=r['question'];return q[':question/problem']+'\n\n'+'\n'.join(a[':answer/value'] for f in q[':question/answer-fields'] for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',required=True);ap.add_argument('--count',type=int,default=1);ap.add_argument('--seed',type=int,default=0);ap.add_argument('--format',choices=['json','markdown'],default='json');a=ap.parse_args();rs=batch(a.difficulty,a.count,a.seed)
 print(json.dumps({'instances':rs},indent=2,ensure_ascii=False) if a.format=='json' else '\n\n'.join(map(markdown,rs)))
