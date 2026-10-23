import sys, json, re, importlib.util, pathlib, hashlib, platform, shutil, subprocess
from collections import Counter, defaultdict
import sympy as S
ROOT=pathlib.Path(__file__).resolve().parent
JOB=ROOT.parent
REPO=pathlib.Path('/home/jake/Developer/Course_Academy')
sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location('reviewed',JOB/'workspace/17592186059776.py'); g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def save(name,obj): (ROOT/name).write_text(json.dumps(obj,indent=2,default=str))
def read(name): return json.loads((JOB/name).read_text())
def rat(t):
 t=t.strip().replace(' ','');t=re.sub(r'\\(?:d?frac)\{(-?\d+)\}\{(\d+)\}',r'(\1/\2)',t);return S.sympify(t)
def mats(t):
 return [S.Matrix([[rat(v) for v in row.split('&')] for row in b.split(r'\\')]) for b in re.findall(r'\\begin\{array\}\{cc\|c\}(.*?)\\end\{array\}',t,re.S)]
def prompt_matrix(t):
 b=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',t,re.S)[1];out=[]
 for row in b.split(r'\\'):
  l,r=row.split('&=');l=re.sub(r'\\frac\{(-?\d+)\}\{(\d+)\}',r'(\1/\2)',l);l=re.sub(r'(?<=[\d)])(?=[xy])','*',l);e=S.sympify(l);out.append([e.coeff(S.Symbol('x')),e.coeff(S.Symbol('y')),rat(r.rstrip('.,'))])
 return S.Matrix(out)
def field(rec):return rec['question'][':question/answer-fields'][0]
def choices(rec):return field(rec)[':answer-field/choices']
def correct(rec):return field(rec)[':answer-field/correct'][1]
def idx(rec):return next(i for i,a in enumerate(choices(rec)) if a[':answer/id']==correct(rec))
def sig(rec):return str(list(prompt_matrix(rec['question'][':question/problem'])[:,:2]))
def ranks(rec):
 vals=[mats(a[':answer/value'])[0][1,2] for a in choices(rec)]
 return vals, sorted(vals).index(vals[idx(rec)])+1
