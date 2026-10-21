import os,sys,json,re,hashlib,platform,importlib.metadata,collections,subprocess,shutil
from pathlib import Path
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parent; JOB=ROOT.parent; PKG=JOB/'workspace'; REPO=Path('/home/jake/Developer/Course_Academy')
sys.dont_write_bytecode=True;sys.path.insert(0,str(PKG));import generator as g

def save(n,v): (ROOT/n).write_text(json.dumps(v,indent=2,default=str))
def mats(s):
 return [[[F(re.sub(r'\\frac\{(-?\d+)\}\{(\d+)\}',r'\1/\2',v.replace(r'\,','').replace(' ','').strip())) for v in row.split('&')] for row in body.split(r'\\')] for body in re.findall(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',s,re.S)]
def target(s):
 x=re.search(r'a\}?_\{(\d)(\d)\}',s);return int(x[1])-1,int(x[2])-1

def op(s):
 s=s.replace(' ',''); rows=[int(x)-1 for x in re.findall(r'(?:\{R\}|R)_\{([123])\}',s)]
 if '↔' in s or r'\leftrightarrow' in s:return ('swap',*rows)
 lhs,rhs=s.split(':='); t=rows[0]
 rhs=re.sub(r'(?:\{R\}|R)_\{([123])\}',r'r\1',rhs)
 rhs=re.sub(r'\\frac\{(-?\d+)\}\{(\d+)\}',r'(\1/\2)',rhs).replace(r'\cdot','*')
 # Parse a linear combination using signed row terms, no generator parser or sympy.
 terms=re.findall(r'([+-]?(?:\([^()]+\)|[\d/]+)?\*?)r([123])',rhs)
 cs=[F(0)]*3
 for k,r in terms:
  k=k.rstrip('*').replace('(','').replace(')',''); k=k.replace('+-','-').replace('++','+'); cs[int(r)-1]+=F(k if k not in ('','+','-') else {'':'1','+':'1','-':'-1'}[k])
 assert len(terms)==rhs.count('r'),rhs
 return ('linear',t,cs)
def apply(a,o):
 b=[row[:] for row in a]
 if o[0]=='swap':b[o[1]],b[o[2]]=b[o[2]],b[o[1]]
 else:b[o[1]]=[sum(o[2][i]*a[i][c] for i in range(3)) for c in range(3)]
 return b

def analyze(r):
 q=r['question']; a=mats(q[':question/problem'])[0];t,c=target(q[':question/problem']);f=q[':question/answer-fields'][0];vs=f[':answer-field/choices'];key=f[':answer-field/correct'];kid=key[1] if isinstance(key,list) else key[':answer/id'];oks=[]
 for i,v in enumerate(vs):
  o=op(v[':answer/value']);b=apply(a,o)
  if b[t][c]==0:oks.append(i)
 assert len(oks)==1,(q[':question/id'],oks)
 i=oks[0];assert vs[i][':answer/id']==kid
 b=apply(a,op(vs[i][':answer/value'])); sol=mats(q[':question/worked-solution']);assert sol[0]==a and sol[-1]==b,(q[':question/id'],'solution mismatch')
 return {'id':q[':question/id'],'profile':r.get('generation',{}).get('bank_profile'),'target':f'{t+1}{c+1}','position':i,'correct':vs[i][':answer/value'],'kind':op(vs[i][':answer/value'])[0],'row_outcome':b,'choice_count':len(vs)}
