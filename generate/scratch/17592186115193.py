#!/usr/bin/env python3
"""Source-bank faithful bounded slope generator; no database operations."""
import argparse,hashlib,json,random,re,sys,uuid
from pathlib import Path
try:import sympy as sp
except ModuleNotFoundError:
 for p in (Path(__file__).resolve().parents[2]/'.venv/lib').glob('python*/site-packages'):sys.path.insert(0,str(p))
 import sympy as sp
PACKAGE=Path(__file__).with_suffix('');SOURCE=json.loads((PACKAGE/'source.json').read_text())
KP_ID=17592186115193;KP_UUID=SOURCE['record'][':knowledge-point/id'];TITLE=SOURCE['record'][':knowledge-point/title']
GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),'question-generator'));VERSION='reciprocal-trig-slope-v1'
SOURCES={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
PROFILES={sid:{'level':q[':question/difficulty'][':db/ident'].split('/')[-1],'observed':{'q-1886':11,'q-1904':5,'q-340660':4}.get(sid,1),'domain':list(range(1,25)) if sid in ['q-1886','q-1904','q-340660'] else [1]} for sid,q in SOURCES.items() if q.get(':question/answer-fields')}
def fingerprint(problem):return hashlib.sha256(problem.replace('⁡','').replace(' ','').encode()).hexdigest()
def uid(data):return str(uuid.uuid5(uuid.UUID(KP_UUID),json.dumps(data,sort_keys=True)))
def adapt(text,sid,n):
 if sid=='q-1886':return text.replace('11',str(n))
 if sid=='q-340660':return text.replace('4',str(n))
 if sid=='q-1904':return text.replace('10','@@DOUBLE@@').replace('5',str(n)).replace('@@DOUBLE@@',str(2*n))
 return text

def generate(difficulty,seed=0,template=None,parameter=None):
 eligible=[s for s,t in PROFILES.items() if t['level']==difficulty]
 if not eligible:raise ValueError('unsupported difficulty: '+difficulty)
 rng=random.Random(seed);sid=template or rng.choice(eligible)
 if sid not in eligible:raise ValueError('Template difficulty mismatch')
 t=PROFILES[sid];n=rng.choice(t['domain']) if parameter is None else parameter
 if type(n)!=int or n not in t['domain']:raise ValueError('Parameter outside validated finite domain')
 src=SOURCES[sid];p=adapt(src[':question/problem'],sid,n);sol=adapt(src[':question/worked-solution'],sid,n)
 key=fingerprint(p);qid=uid([VERSION,key]);fields=[]
 for old in src[':question/answer-fields']:
  fid=uid([qid,old[':answer-field/key']]);bank=[];correct=None
  for a in old[':answer-field/choices']:
   value=adapt(a[':answer/value'],sid,n);aid=uid([fid,value]);bank.append({':answer/id':aid,':answer/type':a[':answer/type'][':db/ident'],':answer/value':value})
   if a[':answer/id']==old[':answer-field/correct'][':answer/id']:correct=aid
  fields.append({':answer-field/id':fid,':answer-field/key':old[':answer-field/key'],':answer-field/type':old[':answer-field/type'][':db/ident'],':answer-field/choices':bank,':answer-field/correct':[':answer/id',correct]})
 q={':question/id':qid,':question/problem':p,':question/worked-solution':sol,':question/difficulty':':question.difficulty/'+difficulty,':question/answer-fields':fields}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'template':sid,'profile':sid+'-observed-bank','seed':seed,'parameter':n,'source_basis':SOURCE['basis'],'mathematical_fingerprint':key,'dependencies':{'sympy':sp.__version__},'domain':'Source real domain excluding poles; positive integer coefficient 1..24 for three variable families; other families replay only','extensions':['Coefficient sampling 1..24'] if len(t['domain'])>1 else []}}
def batch(difficulty,count,seed):
 cases=[(s,n) for s,t in PROFILES.items() if t['level']==difficulty for n in t['domain']]
 if difficulty not in ['easy','moderate']:raise ValueError('unsupported difficulty')
 if not 1<=count<=len(cases):raise ValueError('finite-limit: '+str(len(cases))+' tasks')
 random.Random(seed).shuffle(cases);return [generate(difficulty,seed,s,n) for s,n in cases[:count]]
def markdown(r):
 q=r['question'];return q[':question/problem']+'\n\n'+'\n'.join('$'+a[':answer/value']+'$' for f in q[':question/answer-fields'] for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--difficulty',required=True);p.add_argument('--count',type=int,default=1);p.add_argument('--seed',type=int,default=0);p.add_argument('--format',choices=['json','markdown'],default='json');a=p.parse_args()
 try:rows=batch(a.difficulty,a.count,a.seed)
 except ValueError as e:p.error(str(e))
 print(json.dumps(rows,indent=2) if a.format=='json' else '\n\n---\n\n'.join(map(markdown,rows)))
