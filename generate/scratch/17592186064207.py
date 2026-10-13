#!/usr/bin/env python3
"""Bounded source-bank generator for linear rational integrals with positive K."""
import argparse,hashlib,json,random,uuid
from pathlib import Path
import sympy as sp
KP_ID=17592186064207
KP_UUID='bdbfa506-08a1-5e43-b958-2ae373df775d'
TITLE='Integrating a Linear Rational Function and Simplifying the Arbitrary Constant'
VERSION='linear-rational-constant-v1'
PACKAGE=Path(__file__).with_suffix('')
GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),'question-generator'))
PROFILES=json.loads((PACKAGE/'contract.json').read_text())['profiles']
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def ident(v):return str(uuid.uuid5(uuid.UUID(KP_UUID),digest(v)))
def tex(v):return '' if v==1 else '-' if v==-1 else sp.latex(v).replace('- ','-')
def denominator(p):
 n,a,b=p
 return str(a)+'x+'+str(b) if a>0 else str(b)+'-'+('' if a==-1 else str(-a))+'x'
def fingerprint(p):
 n,a,b=p;x=sp.Symbol('x');return digest(str(sp.cancel(n/(a*x+b))))
def allowed(sid,p):
 if len(p)!=3 or any(type(z)!=int for z in p):return False
 n,a,b=p;t=PROFILES[sid]['style']
 if t=='negative-unit':return n==1 and a==-1 and 3<=b<=9
 if t=='negative-slope':return n==1 and -6<=a<=-2 and 2<=b<=9
 if t in ('positive-unit','moderate-unit'):return n==1 and 2<=a<=6 and 2<=b<=9 and a!=b and b!=a*a and a!=b*b
 if t=='positive-scaled':return 2<=n<=6 and 2<=a<=6 and n!=a and n!=a*a and a!=n*n and 1<=b<=9
 if t=='negative-scaled':return 2<=n<=6 and -6<=a<=-2 and 1<=b<=9
 return False
def candidates(sid):return [[n,a,b] for n in range(1,7) for a in range(-6,7) for b in range(1,10) if allowed(sid,[n,a,b])]
def bank(sid,p):
 n,a,b=map(sp.Integer,p);d=denominator(p);L=r'\operatorname{ln}⁡';normal=lambda c:tex(c)+L+'(K|'+d+'|)'
 if sid=='q-113532':return [normal(1/b),normal(a/b),L+r'(\frac{|'+d+'|}{K})',normal(1/a),r'\frac{K}{'+str(a)+'}'+L+'(|'+d+'|)'],3,['1/b','a/b','1:log(D/K)','1/a','K/a:log(D)']
 if sid=='q-30368':return list(map(normal,[b/a,a,1/b,1/a,a/b])),3,['b/a','a','1/b','1/a','a/b']
 if sid=='q-113537':return list(map(normal,[n,1/a,-n/a,a/n,n/a])),4,['n','1/a','-n/a','a/n','n/a']
 if sid=='q-113538':return [tex(-n/(2*a))+L+r'(\frac{K}{|'+d+'|})',normal(n/a),normal(-n/a),normal(1/(2*a)),normal(n)],1,['-n/(2a):log(K/D)','n/a','-n/a','1/(2a)','n']
 if sid=='q-72445':return list(map(normal,[-1,-1/b,sp.Rational(1,2),1,1/b])),0,['-1','-1/b','1/2:observed fixed','1','1/b']
 if sid=='q-72446':return list(map(normal,[-1/a,-a,1,1/a,a])),3,['-1/a','-a','1','1/a','a']
 raise ValueError(sid)
def generate(difficulty='easy',seed=0,template=None,parameters=None):
 if difficulty not in ('easy','moderate'):raise ValueError('Unsupported hard band; see capabilities.json')
 rng=random.Random(seed);sid=template or rng.choice([k for k,t in PROFILES.items() if t['difficulty']==difficulty]);t=PROFILES[sid]
 if t['difficulty']!=difficulty:raise ValueError('source difficulty mismatch')
 p=list(parameters) if parameters is not None else rng.choice(candidates(sid))
 if not allowed(sid,p):raise ValueError('Outside validated bounded policy')
 n,a,b=p
 def render(text):
  for key,z in {'D':denominator(p),'R':tex(sp.Rational(n,a)),'J':tex(sp.Rational(1,a)),'N':str(n),'A':str(a)}.items():text=text.replace('@@'+key+'@@',z)
  return text
 values,ci,recipes=bank(sid,p);fp=fingerprint(p);qid=ident(['question',VERSION,fp,sid,digest(sorted(values))]);fid=ident([qid,'selection'])
 choices=[{':answer/id':ident([fid,z]),':answer/type':':answer.type/math',':answer/value':z} for z in values]
 q={':question/id':qid,':question/problem':render(t['prompt']),':question/worked-solution':render(t['solution']),':question/difficulty':':question.difficulty/'+difficulty,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',choices[ci][':answer/id']]}]}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'template':sid,'profile':sid,'parameters':p,'source_ids':[sid],'domain':f'x real excluding {-sp.Rational(b,a)}; K>0; C arbitrary real on each connected interval','mathematical_fingerprint':fp,'recipes':recipes,'sympy':sp.__version__}}
def batch(difficulty,count,seed):
 if difficulty not in ('easy','moderate'):raise ValueError('Unsupported band')
 if count<1:raise ValueError('positive count required')
 pairs=[(sid,p) for sid,t in PROFILES.items() if t['difficulty']==difficulty for p in candidates(sid)];random.Random(seed).shuffle(pairs);used=set();rs=[]
 for i,(sid,p) in enumerate(pairs):
  rec=generate(difficulty,seed+i,sid,p);fp=rec['generation']['mathematical_fingerprint']
  if fp not in used:rs.append(rec);used.add(fp)
  if len(rs)==count:return rs
 raise ValueError('Finite validated family exhausted; shortage explicit')
def markdown(rec):
 q=rec['question'];return q[':question/problem']+'\n\n'+'\n'.join('- $'+z[':answer/value']+'$' for z in q[':question/answer-fields'][0][':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--difficulty',default='easy');p.add_argument('--count',type=int,default=1);p.add_argument('--seed',type=int,default=0);p.add_argument('--format',choices=['json','markdown'],default='json');a=p.parse_args();rs=batch(a.difficulty,a.count,a.seed);print(json.dumps(rs,indent=2) if a.format=='json' else '\n\n---\n\n'.join(map(markdown,rs)))
