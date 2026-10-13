#!/usr/bin/env python3
"""Source-faithful bounded hard radio generator: sums of two linear reciprocals."""
import argparse, hashlib, json, random, uuid
from pathlib import Path
import sympy as sp
KP_ID=17592186064208
KP_UUID='af32f07f-fa65-5ede-a506-735dc2d3a5ef'
TITLE='Integrating a Combination of Linear Rational Functions Using the General Formula'
VERSION='combined-linear-rational-v1'
PACKAGE=Path(__file__).with_suffix('')
GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),'question-generator'))
PROFILES=json.loads((PACKAGE/'contract.json').read_text())['profiles']
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def ident(v):return str(uuid.uuid5(uuid.UUID(KP_UUID),digest(v)))
def tex(v):return '' if v==1 else '-' if v==-1 else sp.latex(v).replace('- ', '-')
def denominators(style,p):
 a,b,c=p;ax='x' if a==1 else str(a)+'x'
 if style.startswith('opposite') and style!='opposite-asymmetric':return [str(b)+'+'+ax,str(c)+'-'+ax]
 def term(d):return ax+('+' if d>0 else '')+str(d)
 if style=='opposite-asymmetric':return [term(b),str(c)+'-'+ax]
 return [term(b),term(c)]
def allowed(sid,p):
 if len(p)!=3 or any(type(z)!=int for z in p):return False
 a,b,c=p;t=PROFILES[sid]['style']
 if t=='opposite-unit':return a==1 and 1<=b<=6 and c==b
 if t=='same-unit':return a==1 and 2<=b<=6 and c==-b
 if t=='opposite-symmetric':return 2<=a<=6 and 1<=b<=6 and c==b
 if t=='same-symmetric':
  return 2<=a<=6 and 1<=b<=6 and c==-b and (sid!='q-113540' or b>=2 and a!=b)
 if t=='opposite-asymmetric':return 2<=a<=6 and -6<=b<=-2 and 1<=c<=6 and b+c!=0
 return False
def candidates(sid):
 return [[a,b,c] for a in range(1,7) for b in range(-6,7) for c in range(-6,7) if allowed(sid,[a,b,c])]
def fingerprint(p,style):
 a,b,c=p;d= -a if style.startswith('opposite') else a;x=sp.Symbol('x')
 return digest(str(sp.cancel(1/(a*x+b)+1/(d*x+c))))
def coefficient(recipe,p):
 a,b,c=map(sp.Integer,p)
 return {'inv_a':1/a,'neg_inv_a':-1/a,'a':a,'neg_a':-a,'inv_b':1/b,'neg_inv_b':-1/b,'b':b,'neg_b':-b,'one':sp.Integer(1),'two':sp.Integer(2),'quarter':sp.Rational(1,4)}[recipe]
# Hard: retain every eligible whole source bank. Easy/moderate have no validated
# templates in this package; capabilities.json documents the bounded exception.
def generate(difficulty='hard',seed=0,template=None,parameters=None):
 if difficulty!='hard':raise ValueError('Unsupported band in bounded package; see capabilities.json')
 rng=random.Random(seed);sid=template or rng.choice(list(PROFILES));t=PROFILES[sid]
 p=list(parameters) if parameters is not None else rng.choice(candidates(sid))
 if not allowed(sid,p):raise ValueError('Outside validated bounds or collision conditions')
 a,b,c=p;ds=denominators(t['style'],p)
 def render(s):
  for k,z in {'@@D1@@':ds[0],'@@D2@@':ds[1],'@@INV@@':sp.latex(sp.Rational(1,a))}.items():s=s.replace(k,z)
  return s
 values=[render(z['value']).replace('@@COEF@@',tex(coefficient(z['recipe'].split(':')[0],p))) for z in t['bank']]
 fp=fingerprint(p,t['style']);qid=ident(['question',VERSION,fp,sid,digest(sorted(values))]);fid=ident([qid,'field','selection'])
 choices=[{':answer/id':ident([fid,z]),':answer/type':':answer.type/math',':answer/value':z} for z in values]
 correct=[z[':answer/id'] for z,recipe in zip(choices,t['bank']) if recipe['correct']];assert len(correct)==1
 q={':question/id':qid,':question/problem':render(t['prompt']),':question/worked-solution':render(t['solution']),':question/difficulty':':question.difficulty/hard',':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',correct[0]]}]}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'template':sid,'profile':sid,'parameters':p,'source_ids':[sid],'domain':f'x real excluding {-sp.Rational(b,a)} and {sp.Rational(c,a) if t["style"].startswith("opposite") else -sp.Rational(c,a)}; K>0; each connected interval separately','mathematical_fingerprint':fp,'recipes':[z['recipe'] for z in t['bank']],'sympy':sp.__version__}}
def batch(difficulty,count,seed):
 if difficulty!='hard':raise ValueError('Unsupported band; see capabilities.json')
 if count<1:raise ValueError('positive count required')
 r=[];used=set();rng=random.Random(seed);pairs=[(sid,p) for sid in PROFILES for p in candidates(sid)];rng.shuffle(pairs)
 for i,(sid,p) in enumerate(pairs):
  z=generate(difficulty,seed+i,sid,p);fp=z['generation']['mathematical_fingerprint']
  if fp not in used:r.append(z);used.add(fp)
  if len(r)==count:return r
 raise ValueError('Finite validated family exhausted; shortage remains explicit')
def markdown(rec):
 q=rec['question'];return q[':question/problem']+'\n\n'+'\n'.join('- $'+z[':answer/value']+'$' for z in q[':question/answer-fields'][0][':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--difficulty',default='hard');p.add_argument('--count',type=int,default=1);p.add_argument('--seed',type=int,default=0);p.add_argument('--format',choices=['json','markdown'],default='json');a=p.parse_args();rs=batch(a.difficulty,a.count,a.seed)
 print(json.dumps(rs,indent=2) if a.format=='json' else '\n\n---\n\n'.join(map(markdown,rs)))
