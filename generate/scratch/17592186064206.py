#!/usr/bin/env python3
"""Bounded source-faithful easy radio generator for linear rational integration."""
import argparse, hashlib, json, random, uuid
from pathlib import Path
import sympy as sp
KP_ID=17592186064206
KP_UUID='fc4294d6-3d60-5c9e-a862-863e1d129049'
TITLE='Integrating a Linear Rational Function'
VERSION='linear-rational-v1'
PACKAGE=Path(__file__).with_suffix('')
GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),'question-generator'))
PROFILES=json.loads((PACKAGE/'contract.json').read_text())['profiles']
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def ident(x):return str(uuid.uuid5(uuid.UUID(KP_UUID),digest(x)))
def tex(x):return sp.latex(sp.Rational(x)).replace('- ', '-')
def denom(a,b):
 if a==1:return 'x'+('+' if b>0 else '')+str(b)
 return str(b)+str(a)+'x'
def fingerprint(p):
 n,a,b=p
 return digest(['rational-integrand',str(sp.Rational(n,a)),str(sp.Rational(b,a))])
def bank(profile,n,a,b):
 d=denom(a,b);log=lambda c,arg:('-' if c==-1 else tex(c) if c!=1 else '')+r'\operatorname{ln}⁡|'+arg+'|+C'
 if profile=='coefficient':return [log(c,d) for c in (sp.Integer(n),sp.Rational(1,n),-sp.Integer(n),-sp.Rational(1,n),sp.Integer(1))]
 if profile=='negative-slope':return [log(c,d) for c in (sp.Rational(1,a),-sp.Rational(1,a),sp.Integer(a),-sp.Integer(a),sp.Integer(-1))]
 if profile=='negative-shift':return [log(1,d),log(-1,d),log(1,'x'),log(-1,'x'),log(-1,denom(a,-b))]
 if profile=='positive-shift':return [log(1,d),log(sp.Rational(1,b),d),log(b,d),log(1,'x'),log(b,'x')]
 raise ValueError('unknown source bank')
def allowed(profile,p):
 if len(p)!=3 or any(type(x)!=int for x in p):return False
 n,a,b=p
 if profile=='coefficient':return a==1 and 2<=n<=9 and 1<=b<=12
 if profile=='negative-slope':return n==1 and -9<=a<=-2 and 1<=b<=12
 if profile=='negative-shift':return n==a==1 and -12<=b<=-1
 if profile=='positive-shift':return n==a==1 and 2<=b<=12
 return False

def generate(difficulty='easy',seed=0,template=None,parameters=None):
 if difficulty!='easy':raise ValueError('Unsupported level in this bounded package; see capabilities.json')
 rng=random.Random(seed);sid=template or rng.choice(list(PROFILES));t=PROFILES[sid];profile=t['profile']
 if parameters is None:
  parameters=([rng.randint(2,9),1,rng.randint(1,12)] if profile=='coefficient' else [1,-rng.randint(2,9),rng.randint(1,12)] if profile=='negative-slope' else [1,1,-rng.randint(1,12)] if profile=='negative-shift' else [1,1,rng.randint(2,12)])
 if not allowed(profile,parameters):raise ValueError('Outside validated parameter bounds')
 n,a,b=parameters;values=bank(profile,n,a,b)
 if len(set(values))!=5:raise ValueError('Bank collision')
 def render(s):
  for k,v in {'@@D@@':denom(a,b),'@@N@@':str(n),'@@INV@@':tex(sp.Rational(1,a)),'@@A@@':str(a)}.items():s=s.replace(k,v)
  return s
 fp=fingerprint(parameters)
 # Bank identity matters for reproducible authoring; novelty never depends on it.
 qid=ident(['question',VERSION,fp,digest(sorted(values)),digest([t['prompt'],t['solution']])]);fid=ident([qid,'field','selection'])
 choices=[{':answer/id':ident([fid,v]),':answer/type':':answer.type/math',':answer/value':v} for v in values]
 q={':question/id':qid,':question/problem':render(t['prompt']),':question/worked-solution':render(t['solution']),':question/difficulty':':question.difficulty/easy',':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',choices[0][':answer/id']]}]}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'template':sid,'profile':profile,'parameters':parameters,'domain':f'x real; x != {sp.Rational(-b,a)}; antiderivative on each connected interval','source_ids':[sid],'mathematical_fingerprint':fp,'sympy':sp.__version__}}
def batch(difficulty,count,seed):
 if difficulty!='easy':raise ValueError('Unsupported level; see capabilities.json')
 if count<1:raise ValueError('positive count required')
 recs=[];used=set()
 for offset in range(max(2000,count*100)):
  r=generate(difficulty,seed+offset);fp=r['generation']['mathematical_fingerprint']
  if fp not in used:used.add(fp);recs.append(r)
  if len(recs)==count:return recs
 raise ValueError('Bounded finite family exhausted; shortage remains explicit')
def markdown(rec):
 q=rec['question'];f=q[':question/answer-fields'][0]
 return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$' for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--difficulty',default='easy');p.add_argument('--count',type=int,default=1);p.add_argument('--seed',type=int,default=0);p.add_argument('--format',choices=['json','markdown'],default='json');a=p.parse_args();rs=batch(a.difficulty,a.count,a.seed)
 print(json.dumps(rs,indent=2) if a.format=='json' else '\n\n---\n\n'.join(map(markdown,rs)))
