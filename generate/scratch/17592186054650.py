#!/usr/bin/env python3
"""Adding Non-Square Matrices: small signed integer entrywise addition."""
import argparse,copy,hashlib,json,random,re,uuid
from pathlib import Path
try:
 import sympy as sp
except ModuleNotFoundError:
 import os,sys
 executable=Path(__file__).resolve().parents[2]/'.venv/bin/python'
 if __name__=='__main__' and executable.is_file():os.execv(str(executable),[str(executable),str(Path(__file__).resolve()),*sys.argv[1:]])
 raise
HERE=Path(__file__).with_suffix('');S=json.loads((HERE/'source.json').read_text())
KP_ID=17592186054650;KP_UUID=S['record'][':knowledge-point/id'];VERSION='1.0.0'
SOURCES={q[':question/math-academy-id']:q for q in S['record'][':knowledge-point/questions']}
TEMPLATES=tuple(SOURCES)
MATRIX=re.compile(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',re.S)
def parse(text):return [[int(x.strip()) for x in row.split('&')] for row in text.split(r'\\')]
def matrices(text):return [parse(m) for m in MATRIX.findall(text)]
def latex(rows):return r'\begin{bmatrix}'+r' \\ '.join(' & '.join(map(str,row)) for row in rows)+r'\end{bmatrix}'
def flat(m):return [x for row in m for x in row]
def shape(t):
 a,b=matrices(SOURCES[t][':question/problem']);return len(a),len(a[0])
def original(t):
 a,b=matrices(SOURCES[t][':question/problem']);return {'a':flat(a),'b':flat(b)}
def total(p):return [int(x) for x in sp.Matrix(p['a'])+sp.Matrix(p['b'])]
def bank(t,p):
 a,b=p['a'],p['b'];c=total(p)
 def changed(updates):
  d=c.copy()
  for i,value in updates.items():d[i]=value
  return d
 if t=='q-103':return [changed({2:a[2]-b[2],5:-c[5]}),c,changed({3:-a[3]+b[3],5:-c[5]}),changed({0:-c[0],4:-a[4]+b[4]}),changed({1:-c[1],2:-c[2]})]
 if t=='q-105':return [changed({0:-c[0],4:b[3]}),c,changed({4:b[3],5:-c[5]}),changed({1:-c[1],4:b[3]}),changed({3:-c[3],4:b[3]})]
 if t=='q-125722':return [c,changed({0:b[0],1:a[1]}),changed({2:b[2]-c[2]+a[2]+b[2],5:c[2]}),changed({4:b[4]-a[4],5:b[5]-a[5]}),changed({2:a[3]})]
 if t=='q-69622':return [changed({0:a[0]+2*b[0],1:2*a[1]+b[1],2:0,3:a[3]+3*b[2],4:a[1]+b[1],5:a[5]}),changed({1:a[3]+a[2],2:a[3]*b[2],3:a[3]+a[5],5:a[3]*b[2]}),changed({2:0,3:-a[3]+b[5]*b[2],5:a[5]}),[c[2],c[0],c[1],c[5],c[4],b[3]],c]
 if t=='q-69635':return [changed({3:a[1]-a[4]+a[5]*b[0]*b[2],4:-c[4],5:-c[5]}),changed({0:a[0]-b[0],2:-c[2],5:a[5]-b[5]}),c,changed({2:a[2]+b[5]-a[2],3:a[3]-a[2]+a[4]-a[5],4:-c[4],5:-c[5]}),changed({2:-c[2],3:a[1]-b[3],5:-c[5]})]
 if t=='q-106':return [changed({3:-c[3]}),c,changed({1:-c[1]}),changed({5:-a[4]+b[4]}),changed({1:-c[1],4:-c[4]})]
 if t=='q-319601':return None
 raise ValueError(t)
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(parent,x):return str(uuid.uuid5(uuid.UUID(parent),str(x)))
def fingerprint(q):
 ms=matrices(q[':question/problem'])
 if len(ms)!=2:ms=[parse(m) for m in MATRIX.findall(q.get(':question/worked-solution',''))[:2]]
 if len(ms)!=2:return digest(q[':question/problem'])
 # Addition is commutative: reversed operands cannot replenish the same problem.
 return digest(sorted(ms,key=lambda m:json.dumps(m)))
def generate(difficulty='easy',seed=0,template=None,parameters=None,replay=False):
 if difficulty!='easy':raise ValueError('Unsupported band: no validated same-KP moderate/hard backbone')
 rng=random.Random(seed);t=template or rng.choice(TEMPLATES);source=SOURCES[t];nr,nc=shape(t);n=nr*nc
 if parameters is None:
  for _ in range(1000):
   p={'a':[rng.randint(-16,16) for _ in range(n)],'b':[rng.randint(-16,16) for _ in range(n)]};values=bank(t,p)
   if values is None or len({tuple(v) for v in values})==5:break
  else:raise ValueError('No nonambiguous bank found within 1000 attempts')
 else:p=copy.deepcopy(parameters)
 assert len(p['a'])==len(p['b'])==n and all(type(x)==int and -16<=x<=16 for x in p['a']+p['b'])
 c=total(p);values=bank(t,p)
 if values is not None:assert len({tuple(v) for v in values})==5
 def mat(v):return latex([v[i:i+nc] for i in range(0,n,nc)])
 sub=iter((mat(p['a']),mat(p['b'])));prompt=MATRIX.sub(lambda _:next(sub),source[':question/problem'])
 lhs={'q-103':mat(p['a'])+'+'+mat(p['b']),'q-105':'X+Y','q-125722':'P+Q','q-319601':'P+Q','q-69622':mat(p['a'])+'+'+mat(p['b']),'q-69635':mat(p['a'])+'+'+mat(p['b']),'q-106':'M+N'}[t]
 # q-125722 wraps negative first addends; other observed solutions do not.
 def first(a):return '('+str(a)+')' if t=='q-125722' and a<0 else str(a)
 calculations=[first(a)+'+'+('('+str(b)+')' if b<0 else str(b)) for a,b in zip(p['a'],p['b'])]
 expanded=mat(calculations);result=mat(c)
 inline=t in ('q-103','q-69622','q-69635')
 stages=(lhs+' & ='+expanded) if inline else (lhs+' & ='+mat(p['a'])+'+'+mat(p['b'])+r' \\  & ='+expanded)
 lead='We add the corresponding entries: '+('\n\n' if t=='q-69635' else '') if t=='q-69635' else 'We add the corresponding entries:\n\n'
 solution=lead+'$$\n'+r'\begin{aligned}'+stages+r' \\  & ='+result+r'\end{aligned}'+'\n$$'
 ident=uid(KP_UUID,VERSION+':'+digest([t,p,values]));fields=[];isradio=values is not None
 for j in range(1 if isradio else n):
  key='selection' if isradio else 'field-'+str(j+1);fid=uid(ident,key)
  strings=[mat(v) for v in values] if isradio else [str(c[j])]
  answers=[{':answer/id':uid(fid,v),':answer/type':':answer.type/math',':answer/value':v} for v in strings];correct=mat(c) if isradio else str(c[j])
  fields.append({':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+('radio' if isradio else 'blank'),':answer-field/choices':answers,':answer-field/correct':[':answer/id',uid(fid,correct)]})
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':S['record'][':knowledge-point/title']},'question':{':question/id':ident,':question/problem':prompt,':question/worked-solution':solution,':question/difficulty':':question.difficulty/easy',':question/answer-fields':fields},'generation':{'version':VERSION,'seed':seed,'template':t,'profile':t if isradio else None,'parameters':p,'replay':replay,'source':source[':db/id'],'source_basis':S['basis'],'dependency_versions':{'sympy':sp.__version__},'mathematical_fingerprint':fingerprint({':question/problem':prompt}),'assets':[]}}
def batch(difficulty,count,seed):
 out=[];seen=set()
 for k in range(count*100+1):
  if len(out)==count:return out
  r=generate(difficulty,seed+k,TEMPLATES[k%len(TEMPLATES)]);fp=r['generation']['mathematical_fingerprint']
  if fp not in seen:out.append(r);seen.add(fp)
 raise ValueError('Finite sampling bound reached')
def markdown(r):
 q=r['question'];return q[':question/problem']+'\n\n'+'\n\n'.join(f[':answer-field/key']+': '+', '.join(a[':answer/value'] for a in f[':answer-field/choices']) for f in q[':question/answer-fields'])+'\n\n'+q[':question/worked-solution']
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--difficulty',default='easy');a.add_argument('--seed',type=int,default=0);a.add_argument('--count',type=int,default=1);a.add_argument('--template');a.add_argument('--format',choices=['json','markdown'],default='json');args=a.parse_args()
 records=[generate(args.difficulty,args.seed,args.template)] if args.template else batch(args.difficulty,args.count,args.seed)
 print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
