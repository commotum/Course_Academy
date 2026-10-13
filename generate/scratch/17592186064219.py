#!/usr/bin/env python3
"""Source-bank inverse-tangent integrals; bounded, exact, deterministic variants."""
import argparse, hashlib, json, random, re, uuid
from pathlib import Path
import sympy as sp
from functools import lru_cache
KP_ID=17592186064219
KP_UUID='227abe29-6e31-5afd-b0ca-3b8ed7d8c287'
TITLE='Calculating Indefinite Integrals Using Substitution with Inverse Tangent'
VERSION='inverse-tangent-substitution-v1'
PACKAGE=Path(__file__).with_suffix('')
GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),'question-generator'))
PROFILES=json.loads((PACKAGE/'contract.json').read_text())['profiles']
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def ident(v):return str(uuid.uuid5(uuid.UUID(KP_UUID),digest(v)))
def tex(z):return sp.latex(sp.simplify(z)).replace(' ','')
def coefficient(z):return '' if z==1 else tex(z)
def function(z,fn,k,quotient=False):
 arg='x' if k==1 else (r'\frac{x}{'+tex(1/k)+'}' if k.is_Rational and 0<k<1 else tex(k)+'x')
 if k.is_Rational is False and tex(k).startswith(r'\frac'):
  arg=tex(k).replace('}{','x}{',1)
 arg='('+arg+')'
 f=(r'\text{arcsec}' if fn=='asec' else r'\operatorname{'+{'atan':'arctan','asin':'arcsin'}[fn]+'}⁡')+arg
 if quotient and z.is_Rational and z.p==1:return r'\frac{'+f+'}{'+str(z.q)+'}+C'
 return coefficient(z)+f+'+C'
def bank(sid,p):
 n,b=map(sp.Integer,p);s=sp.sqrt(b);c=n/s
 A=lambda z,k=s,fn='atan',q=False:function(z,fn,k,q)
 if sid=='q-49540':values=[A(n),A(1/s,q=True),A(c,fn='asin'),A(c),A(1/s,fn='asin',q=True)];ci=3
 elif sid=='q-114033':values=[A(1,1/s),A(s/n),A(c,sp.Integer(1)),A(c,1/s),A(c)];ci=4
 elif sid=='q-114035':values=[A(b),A(c),A(s),A(c,sp.Integer(1)),A(c,1/b)];ci=1
 elif sid=='q-114036':values=[A(c,sp.Integer(1)),A(s),A(b),A(1,1/s),A(c)];ci=4
 elif sid=='q-114040':values=[A(c),A(n/b),A(s),A(c,b),A(n)];ci=0
 elif sid=='q-2504':values=[A(1/s,q=True),A(s),A(1/b,b,q=True),A(1/b,q=True),A(1/(2*s),2*s,q=True)];ci=0
 elif sid=='q-2507':values=[A(1/b,sp.Integer(1),q=True),A(1/s,q=True),A(1/b,b,'asec',True),A(1/s,s,'asin',True),A(1/b,b,q=True)];ci=1
 elif sid=='q-73713':values=[A(1/c,q=True),A(1/c,fn='asin',q=True),A(c,sp.Integer(1)),A(c,fn='asin'),A(c)];ci=4
 elif sid=='q-114039':values=[A(c),A(b),A(s),A(c,b),A(c,sp.Integer(1))];ci=0
 elif sid=='q-49548':values=[A(1/b,1/b),A(1,1/s),A(c,1/s),A(c,1/b),A(1,1/b)];ci=2
 elif sid=='q-114045':values=[A(c),A(1,1/s),A(1/s,1/s),A(c,1/s),A(n/b,1/s)];ci=3
 elif sid=='q-114046':values=[A(1/s,sp.Integer(1)),A(1),A(1/s,1/s),A(1,1/s),A(s,1/s)];ci=3
 elif sid=='q-49505':values=[A(c,1/s),A(1,1/s),A(c,sp.Integer(1)),A(1),A(s)];ci=0
 elif sid=='q-49550':values=[A(c,1/s),A(c,s,'asin'),A(c,1/s,'asin'),A(c),A(1,1/s)];ci=0
 elif sid=='q-49551':values=[A(c,1/s,'asin',True),A(c,c,q=True),A(1/s,s,'asin',True),A(c,1/s,q=True),A(1/s,1/s,q=True)];ci=3
 elif sid=='q-73714':values=[A(s/n),A(c,1/s),A(1/n,1/s),A(c),A(s/n,1/s)];ci=1
 else:raise ValueError(sid)
 # Two sources omit parentheses around the unit argument. Preserve that notation.
 if sid in ('q-73713','q-49505'):values=[v.replace('⁡(x)','⁡x') for v in values]
 return values,ci

@lru_cache(None)
def candidates(sid):
 t=PROFILES[sid];n,b=t['parameters']
 # Retain omitted unit coefficients and the observed n=s cancellation exactly.
 # Other profiles vary only n, preserving observed scale and radical structure.
 ns=[n] if t['fixed_numerator'] else list(range(2,31))
 return [[z,b] for z in ns if admissible(sid,[z,b])]
def admissible(sid,p):return _admissible_cached(sid,tuple(p))
@lru_cache(None)
def _admissible_cached(sid,p):
 t=PROFILES[sid]
 if len(p)!=2 or any(type(z)!=int for z in p) or p[1]!=t['parameters'][1]:return False
 if t['fixed_numerator']:return list(p)==t['parameters']
 n,b=p;s=sp.sqrt(b)
 if not 2<=n<=30:return False
 # Integer source simplification layouts remain integer layouts.
 if sid in ('q-49540','q-73713','q-114045') and not (sp.Integer(n)/s).is_Integer:return False
 if sid=='q-114040' and n%2:return False
 if sid=='q-49551' and not (s/sp.Integer(n)).is_Integer:return False
 values,ci=bank(sid,p)
 # Complete profiles must retain five different mathematical objects.
 from sympy.parsing.sympy_parser import parse_expr
 vals=[parse_value(z) for z in values]
 target=sp.Integer(n)/(1+b*x*x) if t['difficulty']=='easy' else sp.Integer(n)/(b+x*x)
 derivatives=[sp.diff(z,x) for z in vals]
 if any(sp.simplify(derivatives[i]-derivatives[j])==0 for i in range(5) for j in range(i)):return False
 return [i for i,z in enumerate(derivatives) if sp.simplify(z-target)==0]==[ci]
x=sp.Symbol('x',real=True)
def parse_value(value):
 from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
 value=value.replace('⁡','').replace('+C','').replace(r'\operatorname{arctan}','atan').replace(r'\operatorname{arcsin}','asin').replace(r'\text{arcsec}','asec')
 def group(t,i):
  assert t[i]=='{',t
  depth=1;j=i+1
  while depth:
   if t[j]=='{':depth+=1
   if t[j]=='}':depth-=1
   j+=1
  return t[i+1:j-1],j
 def rewrite(t):
  out='';i=0
  while i<len(t):
   if t.startswith(r'\frac',i):
    a,j=group(t,i+5);b,j=group(t,j);out+='(('+rewrite(a)+')/('+rewrite(b)+'))';i=j
   elif t.startswith(r'\sqrt',i):
    a,j=group(t,i+5);out+='sqrt('+rewrite(a)+')';i=j
   else:out+=t[i];i+=1
  return out
 value=rewrite(value).replace('atanx','atan(x)').replace('asinx','asin(x)')
 return parse_expr(value,local_dict={'x':x,'atan':sp.atan,'asin':sp.asin,'asec':sp.asec,'sqrt':sp.sqrt},transformations=standard_transformations+(implicit_multiplication_application,))
def generate(difficulty='easy',seed=0,template=None,parameters=None):
 if difficulty not in ('easy','moderate'):raise ValueError('Unsupported hard level; see capabilities.json')
 rng=random.Random(seed);sid=template or rng.choice([sid for sid,t in PROFILES.items() if t['difficulty']==difficulty]);t=PROFILES[sid]
 if t['difficulty']!=difficulty:raise ValueError('profile level mismatch')
 p=list(parameters) if parameters is not None else rng.choice(candidates(sid))
 if not admissible(sid,p):raise ValueError('Outside validated bounded capability')
 n,b=map(sp.Integer,p);s=sp.sqrt(b)
 vals,ci=bank(sid,p)
 repl={'N':str(n),'C':coefficient(n/s),'R':tex(n/b),'RAW_R':r'\frac{'+str(n)+'}{'+str(b)+'}', 'ROOT_R':r'\frac{'+str(n)+r'\sqrt{'+str(b)+'}}{'+str(b)+'}', 'OVER_ROOT':r'\frac{'+str(n)+r'}{\sqrt{'+str(b)+'}}'}
 def render(txt):
  for k,z in repl.items():txt=txt.replace('@@'+k+'@@',z)
  return txt
 fp=fingerprint_parameters(difficulty,p);qid=ident(['question',VERSION,fp,sid,digest(sorted(vals))]);fid=ident([qid,'selection'])
 choices=[{':answer/id':ident([fid,z]),':answer/type':':answer.type/math',':answer/value':z} for z in vals]
 q={':question/id':qid,':question/problem':render(t['prompt']),':question/worked-solution':render(t['solution']),':question/difficulty':':question.difficulty/'+difficulty,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',choices[ci][':answer/id']]}]}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'template':sid,'profile':sid,'parameters':p,'source_ids':[sid],'recipes':t['recipes'],'domain':'x real; C arbitrary real; positive denominator','mathematical_fingerprint':fp,'sympy':sp.__version__,'sampling_policy':'fixed observed denominator; bounded source-profile numerator; unit/cancellation templates fixed'}}
def fingerprint_parameters(difficulty,p):
 n,b=p;return digest(str(sp.cancel(sp.Integer(n)/(1+b*x*x) if difficulty=='easy' else sp.Integer(n)/(b+x*x))))
def batch(difficulty,count,seed):
 if difficulty not in ('easy','moderate'):raise ValueError('Unsupported level')
 if count<1:raise ValueError('positive count required')
 pairs=[(sid,p) for sid,t in PROFILES.items() if t['difficulty']==difficulty for p in candidates(sid)];random.Random(seed).shuffle(pairs);out=[];seen=set()
 for sid,p in pairs:
  rec=generate(difficulty,seed,sid,p);fp=rec['generation']['mathematical_fingerprint']
  if fp not in seen:out.append(rec);seen.add(fp)
  if len(out)==count:return out
 raise ValueError('Finite bounded family exhausted; leave shortage explicit')
def markdown(r):
 q=r['question'];return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$' for a in q[':question/answer-fields'][0][':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--difficulty',default='easy');p.add_argument('--count',type=int,default=1);p.add_argument('--seed',type=int,default=0);p.add_argument('--format',choices=['json','markdown'],default='json');a=p.parse_args();rs=batch(a.difficulty,a.count,a.seed);print(json.dumps(rs,indent=2,ensure_ascii=False) if a.format=='json' else '\n\n---\n\n'.join(map(markdown,rs)))
