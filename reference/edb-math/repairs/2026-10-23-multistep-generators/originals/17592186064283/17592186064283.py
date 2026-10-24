#!/usr/bin/env python3
"""Bounded source-faithful trigonometric power chain-rule generator. No plots."""
import argparse,hashlib,json,random,uuid
from pathlib import Path
import sympy as sp
KP_ID=17592186064283
KP_UUID='3ec11481-cea2-514b-aa78-707fcf8838cc'
TITLE='Differentiating a Power of a Trigonometric Function Using the Chain Rule'
VERSION='trig-power-v1'
PACKAGE=Path(__file__).with_suffix('')
GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),'question-generator'))
PROFILES=json.loads((PACKAGE/'contract.json').read_text())['profiles']
x=sp.Symbol('x',real=True)
def digest(a):return hashlib.sha256(json.dumps(a,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def ident(a):return str(uuid.uuid5(uuid.UUID(KP_UUID),digest(a)))
def expression(func,c,n):return c*getattr(sp,func)(x)**n
def fingerprint(parameters,func):return digest(['trig-power-derivative',str(sp.expand_trig(sp.diff(expression(func,*parameters),x)))])
def domain(t):
 p=t['profile']
 if p=='cos-unit':return [[1,n] for n in range(3,10)]
 if p=='sin-unit':return [[1,2]]
 if p=='sin-scaled':return [[c,2] for c in range(2,10)]
 if p.startswith('cos-scaled'):return [[c,n] for c in range(2,10) for n in range(3,10)]
 if p=='sin-blank':return [[1,n] for n in range(2,10)]
 if p=='cos-blank':return [[c,n] for c in range(-9,-1) for n in range(3,10)]
 raise ValueError('unknown profile')
def bank(t,c,n):
 m=n-1;k=c*n;s=r'\operatorname{sin}⁡x';co=r'\operatorname{cos}⁡x'
 cp='{cos}^{'+str(m)+'}⁡x';si='{sin}^{'+str(m)+'}⁡x'
 p=t['profile']
 if p=='cos-unit':return ['-'+str(n)+cp+r'\,'+s,'-'+str(n)+si,str(n)+co+r'\,'+si,str(n)+cp+r'\,'+s,str(n)+cp]
 if p=='sin-unit':return [str(2)+s+r'\,'+co,'-'+s+r'\,'+co,'-2{cos}^{2}⁡x','-2'+s+r'\,'+co,'{cos}^{2}⁡x']
 if p=='sin-scaled':return [str(k)+s+co,'-'+str(c)+s+co,'-'+str(c)+'{cos}^{2}⁡x',str(k)+s+'{cos}^{2}⁡x',str(k)+s]
 if p=='cos-scaled-a':return ['-'+str(k)+cp+s,'-'+str(c)+si,str(c)+co+si,'-'+str(k)+co+si,str(k)+cp]
 if p=='cos-scaled-b':return ['-'+str(k)+cp+s,'-'+str(k)+co+si,'-'+str(k)+si,str(c)+co+si,str(c)+cp]
 if p=='sin-blank':return [str(n)+'{sin}^{'+str(m)+'}(x)'+r'\operatorname{cos}(x)']
 if p=='cos-blank':return [str(-k)+'{cos}^{'+str(m)+'}(x)'+r'\operatorname{sin}(x)']
 raise ValueError('unknown profile')
def generate(difficulty='easy',seed=0,template=None,parameters=None):
 if difficulty not in ('easy','moderate'):raise ValueError('Unsupported level; see capabilities.json')
 rng=random.Random(seed);sid=template or rng.choice([sid for sid,t in PROFILES.items() if t['level']==difficulty]);t=PROFILES[sid]
 if t['level']!=difficulty:raise ValueError('template difficulty mismatch')
 p=parameters if parameters is not None else rng.choice(domain(t))
 if p not in domain(t):raise ValueError('outside bounded validated domain')
 c,n=p;k=c*n;values=bank(t,c,n)
 def render(text):
  for a,b in {'@@C@@':c,'@@N@@':n,'@@M@@':n-1,'@@K@@':k,'@@NK@@':-k}.items():text=text.replace(a,str(b))
  return text
 fp=fingerprint(p,t['function']);prompt=render(t['prompt']);solution=render(t['solution'])
 qid=ident(['question',VERSION,fp,digest(sorted(values)),prompt,solution]);fid=ident([qid,'field',t['field_key']])
 choices=[{':answer/id':ident([fid,v]),':answer/type':':answer.type/math',':answer/value':v} for v in values]
 q={':question/id':qid,':question/problem':prompt,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+difficulty,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':t['field_key'],':answer-field/type':t['field_type'],':answer-field/choices':choices,':answer-field/correct':[':answer/id',choices[0][':answer/id']]}]}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'template':sid,'profile':t['profile'],'parameters':p,'function':t['function'],'domain':'x real','source_ids':[sid],'mathematical_fingerprint':fp,'sympy':sp.__version__}}
def batch(difficulty,count,seed):
 if difficulty not in ('easy','moderate'):raise ValueError('Unsupported level; see capabilities.json')
 if count<1:raise ValueError('positive count required')
 candidates=[(sid,p) for sid,t in PROFILES.items() if t['level']==difficulty for p in domain(t)];random.Random(seed).shuffle(candidates)
 records=[];used=set()
 for sid,p in candidates:
  r=generate(difficulty,seed,sid,p);fp=r['generation']['mathematical_fingerprint']
  if fp not in used:used.add(fp);records.append(r)
  if len(records)==count:return records
 raise ValueError(f'Finite bounded domain exhausted at {len(records)} distinct tasks; shortage remains explicit')
def markdown(r):
 q=r['question'];f=q[':question/answer-fields'][0]
 return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$' for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',default='easy');ap.add_argument('--count',type=int,default=1);ap.add_argument('--seed',type=int,default=0);ap.add_argument('--format',choices=['json','markdown'],default='json');a=ap.parse_args();rs=batch(a.difficulty,a.count,a.seed)
 print(json.dumps(rs,indent=2) if a.format=='json' else '\n\n---\n\n'.join(map(markdown,rs)))
