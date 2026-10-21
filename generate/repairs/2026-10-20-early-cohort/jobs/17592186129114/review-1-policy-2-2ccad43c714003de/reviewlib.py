import sys,os,json,re,hashlib,importlib.util,random,subprocess,shutil,platform
from pathlib import Path
from collections import Counter,defaultdict
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parent
JOB=ROOT.parent
REPO=Path('/home/jake/Developer/Course_Academy')
PKG=JOB/'workspace'
sys.path.insert(0,str(PKG))
import generator as g

def save(n,v): (ROOT/n).write_text(json.dumps(v,indent=2)+'\n')
def enum(v):return v.get(':db/ident') if isinstance(v,dict) else v
def ms(text):
 return [[[int(x.strip()) for x in row.split('&')] for row in body.split(r'\\')] for body in re.findall(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',text,re.S)]
def ref(m):
 # Independent direct search of nonzero cells, then all pairwise row comparisons.
 leading=[min([j for j,x in enumerate(row) if x] or [len(row)]) for row in m]
 width=len(m[0]); valid=all(a<b or a==b==width for a,b in zip(leading,leading[1:]))
 return valid,leading

def value(f):
 c=f[':answer-field/correct'];id=c[1] if isinstance(c,list) else c[':answer/id']
 return next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==id)
def examine(r):
 q=r['question']; neg='**not**' in q[':question/problem']; rows=[];errors=[]
 sm=ms(q[':question/worked-solution'])
 fields=q[':question/answer-fields']
 for f in fields:
  m=ms(f[':answer-field/key'])[0]; label=re.search(r'\$([ABC])\s*=',f[':answer-field/key'])[1]
  valid,pivots=ref(m);expected=valid!=neg
  if value(f)!=str(expected).lower():errors.append(label+' key mismatch')
  if sm['ABC'.index(label)]!=m:errors.append(label+' solution matrix mismatch')
  status=f'- The matrix ${label}$ is '+('in' if valid else 'not in')+' row echelon form'
  if status not in re.sub(r'\s+', ' ', q[':question/worked-solution']):errors.append(label+' solution classification mismatch')
  rows.append({'label':label,'shape':[len(m),len(m[0])],'pivots':pivots,'valid':valid,'selected':expected})
 return {'id':q[':question/id'],'profile':r['generation']['profile'],'negate':neg,'selected':''.join(x['label'] for x in sorted(rows,key=lambda x:x['label']) if x['selected']),'rows':rows,'errors':errors}

