"""Reuse the prior reviewer's independent visible-record parser and arithmetic witness."""
import sys,os,json,re,importlib.util,copy,hashlib,platform,shutil,subprocess
from pathlib import Path
from fractions import Fraction
from collections import Counter,defaultdict
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parent
JOB=ROOT.parent
REPO=Path('/home/jake/Developer/Course_Academy')
def save(name,x): (ROOT/name).write_text(json.dumps(x,indent=2,default=str)+'\n')
def load_generator(path):
 spec=importlib.util.spec_from_file_location('reviewed',path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def matrices(text):
 text=re.sub(r'\\color\{[^}]*\}','',text);text=text.replace(r'\bbox[lightgray,2pt]','')
 return [[[int(v.replace('{','').replace('}','').strip()) for v in row.split('&')] for row in raw.split(r'\\')] for raw in re.findall(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',text,re.S)]
def ops(text):
 t=re.sub(r'\s|\$|\\,','',text).replace('{C}','C')
 return [(int(a)-1,int(p)-1,int(s+(n or '1'))) for a,b,s,n,p in re.findall(r'C_\{?(\d)\}?:=C_\{?(\d)\}?([+-])(\d*)C_\{?(\d)\}?',t) if a==b]
def field(rec):return rec['question'][':question/answer-fields'][0]
def correct_index(rec):
 f=field(rec);return next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1])
def coefficients(rec):return [tuple(o[2] for o in ops(a[':answer/value'])) for a in field(rec)[':answer-field/choices']]
def shortcut(rec):
 pairs=coefficients(rec); counts=Counter(tuple(map(abs,p)) for p in pairs)
 if sorted(counts.values())!=[1,4]:return None
 odd=next(p for p in pairs if counts[tuple(map(abs,p))]==1)
 main=next(p for p,c in counts.items() if c==4)
 if tuple(map(abs,odd))!=main[::-1] or main[0]==main[1]:return None
 predicted=(-odd[1],-odd[0]);return pairs.index(predicted) if predicted in pairs else None
def inspect(rec):
 q=rec['question'];A,B=matrices(q[':question/problem']);given=ops(q[':question/problem']);assert len(given)==1
 g,p,k=given[0]; assert all(A[i][p]==B[i][p] for i in range(4))
 ks={}
 for c in range(4):
  if c==p:continue
  ratios={Fraction(B[i][c]-A[i][c],A[i][p]) for i in range(4) if A[i][p]}
  assert len(ratios)==1;ks[c]=ratios.pop();assert ks[c].denominator==1
  assert all(A[i][c]+ks[c]*A[i][p]==B[i][c] for i in range(4))
 assert k==ks[g]
 expected=[(c,p,int(ks[c])) for c in sorted(ks) if c!=g]
 bank=[ops(a[':answer/value']) for a in field(rec)[':answer-field/choices']]
 assert len(bank)==5 and len(set(map(tuple,bank)))==5
 assert bank.count(expected)==1 and bank[correct_index(rec)]==expected
 stages=matrices(q[':question/worked-solution']);assert len(stages)==4 and stages[0]==A
 cur=copy.deepcopy(A)
 for j,c in enumerate(sorted(ks)):
  for i in range(4):cur[i][c]+=ks[c]*cur[i][p]
  assert cur==stages[j+1]
 assert stages[-1]==B
 so=ops(q[':question/worked-solution']);assert so[:3]==[(c,p,int(ks[c])) for c in sorted(ks)] and so[3:]==expected
 return {'id':q[':question/id'],'seed':rec['generation']['seed'],'profile':rec['generation']['bank_profile'],'correct_index':correct_index(rec),'pair':[o[2] for o in expected],'shortcut':shortcut(rec),'rows':[i for i in range(4) if A[i][p] and all(B[i][c]==0 for c in ks)]}
