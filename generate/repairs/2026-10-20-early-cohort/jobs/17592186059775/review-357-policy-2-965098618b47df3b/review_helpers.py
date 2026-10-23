import sys
sys.dont_write_bytecode=True
import json,re,subprocess,importlib.util,hashlib,pathlib,shutil,os,platform,copy
import sympy as S
E=pathlib.Path(__file__).resolve().parent; J=E.parent; W=J/'workspace'; PY='/home/jake/Developer/Course_Academy/.venv/bin/python'
def save(n,x): (E/n).write_text(json.dumps(x,indent=2,default=str)+'\n')
def loadmod(n,p):
 sp=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
sys.path.insert(0,str(W));g=loadmod('current',W/'17592186059775.py')
pat=re.compile(r'\\begin\{(?:array|bmatrix)\}(?:\{cc\|c\})?(.*?)\\end\{(?:array|bmatrix)\}',re.S)
num=r'-?(?:\\frac\{-?\d+\}\{\d+\}|\d+)'
def rat(x):
 x=x.strip();sgn=-1 if x.startswith('-') else 1
 if x.startswith('-'): x=x[1:]
 m=re.fullmatch(r'\\frac\{(-?\d+)\}\{(\d+)\}',x)
 return sgn*(S.Rational(*map(int,m.groups())) if m else S.Rational(x))
def mats(t):return [S.Matrix([[rat(c) for c in row.split('&')] for row in m.split(r'\\')]) for m in pat.findall(t)]
def xy(t):return [rat(z) for z in re.findall(r'\b[xy]\s*=\s*('+num+')',t)]
def q(r):return r['question']
def f(r):return q(r)[':question/answer-fields'][0]
def key(r):return next(a for a in f(r)[':answer-field/choices'] if a[':answer/id']==f(r)[':answer-field/correct'][1])
def rank(r):
 vals=[mats(a[':answer/value'])[0][1,2] for a in f(r)[':answer-field/choices']]
 return sorted(vals).index(mats(key(r)[':answer/value'])[0][1,2])
def normalize(m):
 first=m[0,:]/m[0,0]; second=m[1,:]-m[1,0]*first;second/=second[0,1]
 return first.col_join(second)
def verify(r):
 qq=q(r);a=mats(qq[':question/problem'])[0];ref=normalize(a);correct=[]
 for ch in f(r)[':answer-field/choices']:
  cm=mats(ch[':answer/value'])[0]; pair=xy(ch[':answer/value'])
  good=cm==ref
  if pair:good=good and len(pair)==2 and a[:,:2]*S.Matrix(pair)==a[:,2]
  if good:correct.append(ch[':answer/id'])
 assert correct==[key(r)[':answer/id']],(qq[':question/id'],correct)
 stages=mats(qq[':question/worked-solution']);assert stages[0]==a and stages[-1]==ref
 for z in stages:assert z[:,:2].det()!=0 and z.rref()[0]==a.rref()[0]
 # Check every explicit intermediate matrix is the next forward-elimination stage.
 expected=[a];z=a.copy()
 if z[0,0]!=1:z[0,:]=z[0,:]/z[0,0];expected.append(z.copy())
 z[1,:]=z[1,:]-z[1,0]*z[0,:];expected.append(z.copy())
 if z[1,1]!=1:z[1,:]=z[1,:]/z[1,1];expected.append(z.copy())
 # Some source traces omit already-normalized operations; no invented stages.
 assert stages==expected,(r['generation']['parameters'],'stages',stages,expected)
 tail=xy(qq[':question/worked-solution'])
 if 'and then solve' in qq[':question/problem']:
  assert tail[-2:]==[ref[0,2]-ref[0,1]*ref[1,2],ref[1,2]],tail
 return {'id':qq[':question/id'],'parameters':r['generation']['parameters'],'rank':rank(r),'answer':str(ref),'passed':True}
