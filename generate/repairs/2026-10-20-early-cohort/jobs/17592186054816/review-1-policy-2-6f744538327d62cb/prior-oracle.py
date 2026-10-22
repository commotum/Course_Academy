import sys,os,json,pathlib,hashlib,subprocess,shutil,re,math,random
from fractions import Fraction
from collections import Counter,defaultdict
ROOT=pathlib.Path(__file__).resolve().parent
JOB=ROOT.parent
PKG=JOB/'workspace'
sys.dont_write_bytecode=True
sys.path.insert(0,str(PKG))
import generator as g
from generator_policy import explicit_none_checkbox

def save(n,x): (ROOT/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def load(p):return json.loads(pathlib.Path(p).read_text())
def digest():return {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in PKG.iterdir() if p.is_file()}
def truth(f):
 ref=f[':answer-field/correct'];aid=ref.get(':answer/id') if isinstance(ref,dict) else ref[1]
 return next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==aid)
def sym(key):
 if key in ('None','None of the above'):return None
 m=re.search(r'\\mathbb\{([NZQRC])\}',key)
 if not m: raise ValueError(key)
 return m[1]+('0' if '_0' in key else '')+('+' if '+' in key else '-' if '-' in key else '')
# Independent semantic oracle, reading prompt/fields rather than generation categories.
def number(q):
 t=re.search(r'number \$(.*?)\$ belong',q)[1]; sign=-1 if t.startswith('-') else 1;t=t.lstrip('-')
 if '\\pi' in t:return (sign,False,False)
 if '\\sqrt' in t:
  n=int(re.search(r'\{(\d+)\}',t)[1]);v=math.isqrt(n)
  return (0 if n==0 else sign,v*v==n,v*v==n)
 if '\\frac' in t:
  n,d=map(int,re.findall(r'\{(\d+)\}',t));v=Fraction(sign*n,d)
 else:v=Fraction(('-' if sign<0 else '')+t)
 return (0 if not v else 1 if v>0 else -1,v.denominator==1,True)
def member(v,s):
 sign,integer,rational=v
 if s=='C':return True
 if s=='N':return integer and sign>0
 if s=='N0':return integer and sign>=0
 base=s[0]; suffix=s[1:]
 if base=='Z' and not integer:return False
 if base=='Q' and not rational:return False
 return {'':True,'+':sign>0,'-':sign<0,'0+':sign>=0,'0-':sign<=0}[suffix]
W=[(-1,True,True),(0,True,True),(1,True,True),(-1,False,True),(1,False,True),(-1,False,False),(1,False,False)]
def target(q):
 p=q[':question/problem']
 if 'do all the ' not in p:return [number(p)]
 group=re.search(r'do all the (.*?) belong',p)[1]
 # Independent witness partition suffices exactly for all taught candidate predicates.
 return [v for v in W if {'positive integers':v[0]>0 and v[1], 'natural numbers':v[0]>0 and v[1], 'negative integers':v[0]<0 and v[1], 'integers':v[1], 'nonnegative integers':v[0]>=0 and v[1], 'positive rational numbers':v[0]>0 and v[2], 'negative rational numbers':v[0]<0 and v[2], 'rational numbers':v[2], 'real numbers':True}[group]]
def expected(r):
 q=r['question'];vs=target(q);ordinary=[all(member(v,sym(f[':answer-field/key'])) for v in vs) for f in q[':question/answer-fields'] if sym(f[':answer-field/key']) is not None]
 it=iter(ordinary);return [not any(ordinary) if sym(f[':answer-field/key']) is None else next(it) for f in q[':question/answer-fields']]
def describe(r):
 return {'id':r['question'][':question/id'],'profile':r['generation']['profile'],'target':r['generation']['instance'],'candidates':r['generation']['candidates'],'correct':[truth(f) for f in r['question'][':question/answer-fields']]}
