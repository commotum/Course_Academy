"""Independent visible-record parsers and exact arithmetic retained from review 0."""
import re
from fractions import Fraction as F
def scalar(s):
 s=s.strip().replace(' ','');s=re.sub(r'\\frac\{(\d+)\}\{(\d+)\}',r'(\1/\2)',s)
 if s.startswith('-('):return -F(s[2:-1])
 if s.startswith('('):s=s[1:-1]
 return F(s)
def matrix(tex):
 m=re.search(r'\\begin\{(?:bmatrix|array)\}(?:\{[^}]+\})?(.*?)\\end\{(?:bmatrix|array)\}',tex,re.S)
 return [[scalar(v) for v in row.split('&')] for row in re.split(r'\\\\',m[1])]
def coeff(expr):
 expr=expr.replace(' ','');vals=[F(0)]*4
 for m in re.finditer(r'([+-]?)(\d+(?:/\d+)?)?([xyz]?)',expr):
  if not m[0]:continue
  sign=-1 if m[1]=='-' else 1;v=F(m[2] or '1')*sign;vals['xyz'.index(m[3]) if m[3] else 3]+=v
 return vals
def equations(tex):
 body=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',tex,re.S)[1]
 rows=[]
 for s in re.split(r'\\\\',body):
  left,right=s.replace('&','').split('=');v=coeff(left);v[3]=scalar(right);rows.append(v)
 return rows
def rref(a):
 a=[r[:] for r in a];j=0
 for c in range(len(a[0])):
  i=next((i for i in range(j,len(a)) if a[i][c]),None)
  if i is None:continue
  a[j],a[i]=a[i],a[j];a[j]=[v/a[j][c] for v in a[j]]
  for k in range(len(a)):
   if k!=j:
    fac=a[k][c];a[k]=[x-fac*y for x,y in zip(a[k],a[j])]
  j+=1
  if j==len(a):break
 return a

def vector_parts(s):
 # Source captures double escape some TeX and Unicode notation.
 s=s.replace('\\\\begin','\\begin').replace('\\\\end','\\end')
 body=re.search(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',s,re.S)[1]
 return [coeff(v) for v in re.split(r'\\{2,}',body)]
def good_solution(v,rows):
 # Affine plane equality: substitution identity plus two independent direction vectors.
 for row in rows:
  if any(sum(row[j]*v[j][c] for j in range(3))!=(row[3] if c==3 else 0) for c in range(4)):return False
 directions=[[v[i][j] for j in (1,2)] for i in range(3)]
 return any(directions[i][0]*directions[j][1]-directions[i][1]*directions[j][0] for i in range(3) for j in range(i))
def analyze(rec):
 q=rec['question'];rows=equations(q[':question/problem']);rf=rref(rows);f=q[':question/answer-fields'][0];correct=f[':answer-field/correct'][1];goods=[]
 easy=q.get(':question/difficulty')==':question.difficulty/easy'
 for a in f[':answer-field/choices']:
  v=a[':answer/value'];valid=False
  if v!='No solution':valid=matrix(v)==rf if easy else good_solution(vector_parts(v),rows)
  if valid:goods.append(a[':answer/id'])
 errors=[]
 if goods!=[correct]:errors.append({'valid_ids':goods,'stored':correct})
 # Parse actual displayed intermediate matrices; verify row equivalence and final answer.
 mats=re.findall(r'\\begin\{array\}\{[^}]+\}.*?\\end\{array\}',q[':question/worked-solution'],re.S)
 for t in mats:
  if rref(matrix(t))!=rf:errors.append('non-equivalent solution matrix')
 if mats and matrix(mats[-1])!=rf:errors.append('final matrix not RREF')
 return {'id':q[':question/id'],'valid_choices':len(goods),'errors':errors,'rref':[[str(v) for v in r] for r in rf]}

