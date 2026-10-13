#!/usr/bin/env python3
"""Source-bank faithful fractional substitution integrals, bounded shift variants."""
import argparse,hashlib,json,random,uuid
from pathlib import Path
import sympy as sp
KP_ID=17592186068786
KP_UUID='03e934c8-da65-5615-9717-a50eee3577fd'
TITLE='Integrating Other Fractional Expressions'
VERSION='fractional-shift-v1'
PACKAGE=Path(__file__).with_suffix('')
GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),'question-generator'))
PROFILES=json.loads((PACKAGE/'contract.json').read_text())['profiles']
LEVELS=('moderate','hard')
def digest(obj):return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def ident(obj):return str(uuid.uuid5(uuid.UUID(KP_UUID),digest(obj)))
def integrand(t,b):
 x=sp.Symbol('x',real=True);return t['k']*x**(t['n']-1)/(b+t['sign']*x**t['n'])**sp.Rational(t['power'])
def fingerprint(t,b):return digest(['integrand',sp.srepr(sp.cancel(integrand(t,b)))])
def generate(difficulty='moderate',seed=0,template=None,parameters=None):
 if difficulty not in LEVELS:raise ValueError('Unsupported level: see capabilities.json')
 rng=random.Random(seed);sid=template or rng.choice([s for s,t in PROFILES.items() if t['level']==difficulty]);t=PROFILES[sid]
 if t['level']!=difficulty:raise ValueError('Template level mismatch')
 p=parameters if parameters is not None else [rng.randint(1,12)]
 if len(p)!=1 or type(p[0])!=int or not 1<=p[0]<=12:raise ValueError('Outside validated bounds')
 b=p[0];render=lambda text:text.replace('@@B@@',str(b));values=list(map(render,t['bank']));fp=fingerprint(t,b)
 qid=ident(['question',VERSION,fp,digest(values),sid]);fid=ident([qid,'field','selection'])
 choices=[{':answer/id':ident([fid,v]),':answer/type':':answer.type/math',':answer/value':v} for v in values]
 q={':question/id':qid,':question/problem':render(t['prompt']),':question/worked-solution':render(t['solution']),':question/difficulty':':question.difficulty/'+difficulty,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',choices[0][':answer/id']]}]}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'template':sid,'profile':sid,'parameters':p,'domain':f"{t['variable']} real; {b} {'+' if t['sign']==1 else '-'} {t['variable']}^{t['n']} {'> 0' if t['power']=='1/2' else '!= 0'}; on each connected interval",'source_ids':[sid],'mathematical_fingerprint':fp,'sympy':sp.__version__}}
def batch(difficulty,count,seed):
 if difficulty not in LEVELS:raise ValueError('Unsupported level: see capabilities.json')
 rng=random.Random(seed);pairs=[(sid,b) for sid,t in PROFILES.items() if t['level']==difficulty for b in range(1,13)];rng.shuffle(pairs);used=set();out=[]
 for sid,b in pairs:
  r=generate(difficulty,seed,sid,[b]);fp=r['generation']['mathematical_fingerprint']
  if fp not in used:used.add(fp);out.append(r)
  if len(out)==count:return out
 raise ValueError('Finite variant limit exceeded; shortage remains explicit')
def markdown(rec):
 q=rec['question'];return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$' for a in q[':question/answer-fields'][0][':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--difficulty',default='moderate');p.add_argument('--count',type=int,default=1);p.add_argument('--seed',type=int,default=0);p.add_argument('--format',choices=['json','markdown'],default='json');a=p.parse_args();rs=batch(a.difficulty,a.count,a.seed)
 print(json.dumps(rs,indent=2) if a.format=='json' else '\n\n---\n\n'.join(map(markdown,rs)))
