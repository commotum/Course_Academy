#!/usr/bin/env python3
"""Subtracting Matrices: source-faithful easy integer templates; no higher bands."""
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
KP_ID=17592186054649;KP_UUID=S['record'][':knowledge-point/id'];VERSION='1.0.0'
SOURCES={q[':question/math-academy-id']:q for q in S['record'][':knowledge-point/questions']}
TEMPLATES=tuple(SOURCES)
MATRIX=re.compile(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',re.S)
def parse(text):
 return [[int(x.strip()) for x in row.split('&')] for row in text.split(r'\\')]
def matrices(text):return [parse(m) for m in MATRIX.findall(text)]
def latex(rows):return r'\begin{bmatrix}'+r' \\ '.join(' & '.join(map(str,row)) for row in rows)+r'\end{bmatrix}'
def flat(m):return [x for row in m for x in row]
def shape(t):
 a,b=matrices(SOURCES[t][':question/problem']);return len(a),len(a[0])
def original(t):
 a,b=matrices(SOURCES[t][':question/problem']);p={'a':flat(a),'b':flat(b)}
 if t=='q-319625':p['targets']=[0,1,4,5,6,8]
 return p
def difference(p):return [int(x) for x in sp.Matrix(p['a'])-sp.Matrix(p['b'])]
def bank(t,p):
 a,b=p['a'],p['b'];c=difference(p)
 def changed(index,value):
  d=c.copy();d[index]=value;return d
 if t=='q-108':return [changed(0,a[0]+b[0]),c,changed(2,a[2]+b[2]),changed(1,-(a[1]+b[1])),changed(3,a[3]+b[3])]
 if t=='q-11478':return [[a[0]-a[3],a[0]-a[3],c[2],c[3]], [c[2],c[3],c[1],c[0]],c,[c[2],c[3],c[0],c[1]], [c[0],c[1],-c[2],-c[3]]]
 if t=='q-11441':return [changed(3,-c[3]),[a[0]]*4,changed(1,c[0]),[c[3]]*4,c]
 if t=='q-69603':return [[a[0]+b[0],a[1]+b[1],a[2]+b[2],c[3],a[4]+b[4],a[5]+b[5]],c[3:]+c[:3],c,[c[0],-(a[1]+b[1]),c[2],c[3],a[4]+b[4],b[5]],[c[0],c[2],c[1],c[3],c[5],c[4]]]
 return None
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(parent,x):return str(uuid.uuid5(uuid.UUID(parent),str(x)))
def fingerprint(q):
 ms=matrices(q[':question/problem'])
 if len(ms)!=2:ms=[parse(m) for m in MATRIX.findall(q.get(':question/worked-solution',''))[:2]]
 if len(ms)!=2:return digest(q[':question/problem'])
 a,b=ms;return digest([a,b])
def generate(difficulty='easy',seed=0,template=None,parameters=None,replay=False):
 if difficulty!='easy':raise ValueError('Unsupported band: no source-backed increase in method/workload')
 rng=random.Random(seed);t=template or rng.choice(TEMPLATES);source=SOURCES[t];nr,nc=shape(t);n=nr*nc
 if parameters is None:
  for _ in range(1000):
   p={'a':[rng.randint(-12,12) for _ in range(n)],'b':[rng.randint(-12,12) for _ in range(n)]}
   if t=='q-11441':p={'a':[rng.randint(0,9) for _ in range(n)],'b':[rng.randint(0,9) for _ in range(n)]}
   if t=='q-319625':p['targets']=sorted(rng.sample(range(9),6))
   values=bank(t,p)
   if values is None or len({tuple(v) for v in values})==5:break
  else:raise ValueError('No nonambiguous bank found')
 else:p=copy.deepcopy(parameters)
 assert len(p['a'])==len(p['b'])==n and all(type(x)==int and -12<=x<=12 for x in p['a']+p['b'])
 c=difference(p);values=bank(t,p)
 if values is not None:assert len({tuple(v) for v in values})==5
 targets=p.get('targets',list(range(n)));assert len(targets)==6 if t=='q-319625' else targets==list(range(n))
 assert len(set(targets))==len(targets) and all(0<=i<n for i in targets)
 def mat(v):return latex([v[i:i+nc] for i in range(0,n,nc)])
 oldm=MATRIX.findall(source[':question/problem']);sub=iter((mat(p['a']),mat(p['b'])))
 prompt=MATRIX.sub(lambda _:next(sub),source[':question/problem'])
 if t=='q-319625':
  stem=prompt.split('\n\n|')[0];cells={i:'{{field-'+str(j+1)+'}}' for j,i in enumerate(targets)}
  rows=[[cells.get(i,'$'+str(c[i])+'$') for i in range(r*nc,(r+1)*nc)] for r in range(nr)]
  prompt=stem+'\n\n| $P-Q=\\,\\,$ |  | '+' | '.join(rows[0])+' |  |\n| --- | --- | --- | --- | --- | --- |\n'+ '\n'.join('|  | '+' | '.join(row)+' |  |  |' for row in rows[1:])
 if t=='q-108':lhs='A-B'
 elif t=='q-69603':lhs=mat(p['a'])+'-'+mat(p['b'])
 else:lhs={'q-11478':'P-Q','q-11441':'A-B','q-319618':'C-D','q-319622':'G-H','q-319625':'P-Q'}[t]
 calculations=[str(a)+'-'+('('+str(b)+')' if b<0 else str(b)) for a,b in zip(p['a'],p['b'])]
 # Preserve the source's alignment sequence (inline-expression source has two stages).
 expanded=mat(calculations);result=mat(c)
 if t=='q-319625':result=result.replace('-7 & 12', '-7 & \\,\\,12') if replay else result
 if t=='q-319625' and replay:result=result.replace('11 &',r'\,\,\,11 &')
 stages=(lhs+' & ='+expanded) if t=='q-69603' else (lhs+' & ='+mat(p['a'])+'-'+mat(p['b'])+r' \\  & ='+expanded)
 solution='We subtract the corresponding entries:\n\n$$\n'+r'\begin{aligned}'+stages+r' \\  & ='+result+r'\end{aligned}'+'\n$$'
 ident=uid(KP_UUID,VERSION+':'+digest([t,p,values]));fields=[]
 isradio=values is not None
 for j,idx in enumerate([0] if isradio else targets):
  key='selection' if isradio else 'field-'+str(j+1);fid=uid(ident,key)
  strings=[mat(v) for v in values] if isradio else [str(c[idx])]
  answers=[{':answer/id':uid(fid,v),':answer/type':':answer.type/math',':answer/value':v} for v in strings]
  correct=mat(c) if isradio else str(c[idx])
  fields.append({':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+('radio' if isradio else 'blank'),':answer-field/choices':answers,':answer-field/correct':[':answer/id',uid(fid,correct)]})
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':S['record'][':knowledge-point/title']},'question':{':question/id':ident,':question/problem':prompt,':question/worked-solution':solution,':question/difficulty':':question.difficulty/easy',':question/answer-fields':fields},'generation':{'version':VERSION,'seed':seed,'template':t,'profile':t if isradio else None,'parameters':p,'replay':replay,'source':source[':db/id'],'source_basis':S['basis'],'dependency_versions':{'sympy':sp.__version__},'mathematical_fingerprint':digest([[p['a'][i:i+nc] for i in range(0,n,nc)],[p['b'][i:i+nc] for i in range(0,n,nc)]]),'assets':[]}}
def batch(difficulty,count,seed):
 out=[];seen=set()
 for k in range(count*100+1):
  if len(out)==count:return out
  r=generate(difficulty,seed+k,TEMPLATES[k%len(TEMPLATES)])
  fp=r['generation']['mathematical_fingerprint']
  if fp not in seen:out.append(r);seen.add(fp)
 raise ValueError('Finite sampling bound reached')
def markdown(r):
 q=r['question'];return q[':question/problem']+'\n\n'+ '\n\n'.join(f[':answer-field/key']+': '+', '.join(a[':answer/value'] for a in f[':answer-field/choices']) for f in q[':question/answer-fields'])+'\n\n'+q[':question/worked-solution']
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--difficulty',default='easy');a.add_argument('--seed',type=int,default=0);a.add_argument('--count',type=int,default=1);a.add_argument('--template');a.add_argument('--format',choices=['json','markdown'],default='json');args=a.parse_args()
 records=[generate(args.difficulty,args.seed,args.template)] if args.template else batch(args.difficulty,args.count,args.seed)
 print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
