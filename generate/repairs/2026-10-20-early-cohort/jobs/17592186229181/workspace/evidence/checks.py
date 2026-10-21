"""Independent visible-record checks; no services or runtime-package writes."""
import sys
sys.dont_write_bytecode=True
import collections,importlib.util,json,pathlib,re
import sympy as sp
ROOT=pathlib.Path(__file__).resolve().parent.parent
EVIDENCE=ROOT/'evidence'
def load():
 manifest=json.loads((ROOT/'package.json').read_text())
 spec=importlib.util.spec_from_file_location('candidate',ROOT/manifest['entrypoint'])
 g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g);return g
T=sp.Symbol('t',real=True)
EX=re.compile(r'Q\(t\)=([+-]?\d+(?:\.\d+)?)([+-])(\d+(?:\.\d+)?)?(?:\{e\}|e)\^\{(-?)t/([0-9.]+)\}')
def ex(value):
 m=EX.fullmatch(re.sub(r'\s+','',value));assert m,value
 e,s,a,n,tau=m.groups();return sp.Rational(e),sp.Rational(a or 1)*(1 if s=='+' else -1),sp.Rational(1)/sp.Rational(tau)*(1 if n else -1)
def key(q):
 v=q[':question/answer-fields'][0].get(':answer-field/correct')
 return v.get(':answer/id') if isinstance(v,dict) else (v[1] if v else None)
def params(q):
 ns=[sp.Rational(x) for x in re.findall(r'\$([0-9]+(?:\.[0-9]+)?)',q[':question/problem'])]
 V,q0,c,r,rout=ns[:5];assert r==rout and r>0 and V>0
 if r'\text{g/L}' in q[':question/problem']:c/=1000
 return V,q0,c,r,ns[5] if len(ns)>5 else None

def shortcut(q):
 opts=q[':question/answer-fields'][0][':answer-field/choices'];triples=[ex(o[':answer/value']) for o in opts]
 ec=collections.Counter(x[0] for x in triples);qc=collections.Counter(e+a for e,a,k in triples)
 dup=[e for e,n in ec.items() if n==2];modal=[q for q,n in qc.items() if n==4]
 if len(dup)!=1 or len(modal)!=1:return None
 hits=[o[':answer/id'] for o,(e,a,k) in zip(opts,triples) if e==dup[0] and e+a==modal[0]]
 return hits[0] if len(hits)==1 else None

def visible_math(record,source=False):
 q=record['question'];V,q0,c,r,time=params(q);expected=V*c+(q0-V*c)*sp.exp(-r*T/V)
 opts=q[':question/answer-fields'][0][':answer-field/choices'];truth=[]
 assert len(opts)==5 and len({a[':answer/value'] for a in opts})==5
 for a in opts:
  value=a[':answer/value']
  if time is None:
   e,b,k=ex(value);f=e+b*sp.exp(-k*T)
   correct=(sp.expand(sp.diff(f,T)-(r*c-r*f/V))==0 and f.subs(T,0)==q0)
  else:
   n=sp.Rational(re.match(r'([0-9.]+)',value)[1]);correct=abs(float(n)-float(expected.subs(T,time)))<.005
  if correct:truth.append(a[':answer/id'])
 assert len(truth)==1,truth
 if key(q):assert truth==[key(q)]
 sol=q.get(':question/worked-solution')
 if sol:
  matches=list(EX.finditer(re.sub(r'\s+','',sol)));assert matches,'missing final expression'
  e,b,k=ex(matches[-1][0]);assert sp.expand(e+b*sp.exp(-k*T)-expected)==0
  if not source:
   assert sol.count('**Step ')==4 and 'first-order linear equation with constant coefficients' in sol
   def num(v):return format(float(v),'.10f').rstrip('0').rstrip('.')
   assert r'\frac{Q}{'+num(V)+'}' in sol
   assert r'\frac{dQ}{dt}+\frac{1}{'+num(V/r)+'}Q=' in sol
   ic=re.search(r'A & =(-?[\d.]+)\\end',sol);assert ic and sp.Rational(ic[1])==q0-V*c
   assert all(sp.Rational(x)==r*c for x in re.findall(r' & =([\d.]+)\\,\\frac\{\\text\{kg\}\}\{\\text\{min\}\}',sol)[:1])
   if time:
    ev=re.search(r'Q\(([\d.]+)\)=[^≈\n]+≈([\d.]+)',sol);assert ev and sp.Rational(ev[1])==time and abs(float(ev[2])-float(expected.subs(T,time)))<.005
 return {'id':q[':question/id'],'parameters':[str(x) if x is not None else None for x in (V,q0,c,r,time)],'truth':truth[0],'solution_checked':bool(sol),'passed':True}
def save(name,obj):(EVIDENCE/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
