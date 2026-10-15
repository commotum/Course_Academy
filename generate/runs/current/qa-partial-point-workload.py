import sys
sys.dont_write_bytecode=True
import json,hashlib,importlib.util
from pathlib import Path
R=Path(__file__).resolve().parent;K=17592186124644;D=R.parents[2]/f'generate/scratch/{K}-draft'
sp=importlib.util.spec_from_file_location('root_point_math_helpers',R/'qa-partial-point-draft.py');q=importlib.util.module_from_spec(sp);sp.loader.exec_module(q);s=q.s
HEIGHTS={'tan-reciprocal':(9,4),'base-exponential-tan':(6,4),'sin-cos-linear':(3,1),'power-log-root':(9,4),'exp-log-power':(4,2),'polynomial':(24,1),'sec-power':(8,1),'root-reciprocal':(32,4),'cross-roots':(24,4),'cos-log-sin':(6,2),'cot-polynomial':(3,1),'log-power-exp':(30,1),'easy-polynomial':(16,1)}
counts={'records':0,'actual_bound_checks':0,'option_coefficient_height_checks':0,'families':{}}
def check(record):
 if record['generation'].get('evidence_only'):return
 Q=record['question'];family=record['generation']['template'];F,u,pt=q.prompt(Q);v=q.p.y if u==q.p.x else q.p.x;U,V=pt[u],pt[v];parts=[]
 for term in s.Add.make_args(F):
  held,active=term.as_independent(u,as_Add=False);der=s.diff(active,u);parts.append({'g':active,'h':held,'hv':held.subs(v,V),'dv':der.subs(u,U),'t':s.simplify(s.diff(term,u).subs(pt))})
 assert len(parts)==2
 def pick(predicate):
  found=[z for z in parts if predicate(z['g'])];assert len(found)==1,(family,parts);return found[0]
 def primitive(f):return pick(lambda g:g.func==f)
 def power():return pick(lambda g:g.is_Pow and g.base==u and g.exp.is_Integer)
 def cap(value,maximum):
  value=s.simplify(value);assert s.Abs(value)<=maximum,(family,value,maximum,Q[':question/problem']);counts['actual_bound_checks']+=1
 def height(value,maxn,maxd):
  for t in s.Add.make_args(s.expand_mul(value)):
   coeff=t.as_coeff_Mul(rational=True)[0];assert abs(coeff.p)<=maxn and coeff.q<=maxd,(family,value,coeff,maxn,maxd)
   counts['option_coefficient_height_checks']+=1
 if family=='tan-reciprocal':
  A=primitive(s.tan);B=power();cap(V**2,9);cap(A['t'],9);cap((U/s.pi)**2,4);cap(B['hv'],8);cap(B['t']*s.pi**2,4)
 elif family=='base-exponential-tan':
  A=pick(lambda g:g.is_Pow and g.base==2);B=power();cap(2**U,2);cap(U**(1-B['g'].exp),1);cap(A['t']/s.log(2),6);cap(B['g'].exp,3);cap(B['t'],3);height(B['t'],6,4)
 elif family=='sin-cos-linear':
  A=primitive(s.sin);B=pick(lambda g:g==u);cap(A['t'],3);cap(B['t']/s.pi,3)
 elif family=='power-log-root':
  A=power();B=pick(lambda g:g==s.sqrt(u));n=A['g'].exp;cap(U**(n-1),4);cap(A['dv'],8);cap(s.log(V),2);cap(A['t'],9);cap(2*s.sqrt(U),4);cap(B['t']/V,2)
 elif family=='exp-log-power':
  A=primitive(s.log);B=pick(lambda g:g==u);n=s.Poly(B['h'],v).degree();cap(V**n,4);cap(B['t'],4);cap(A['dv'],2);cap(A['t']/s.exp(V),4);height(A['t']/s.exp(V),4,2)
 elif family=='polynomial':
  A=pick(lambda g:g==u);B=power();n=B['g'].exp;cap(U**(n-1),2);cap(V**2,4);cap(B['hv']/V*B['dv'],4);cap(A['t'],16);cap(B['t'],8);cap(abs(A['t'])+abs(B['t']),24)
 elif family=='sec-power':
  A=primitive(s.sec);B=pick(lambda g:g==u);n=s.Poly(B['h'],v).degree();cap(V**n,4);cap(A['t'],6);cap(B['t'],4);cap(abs(A['t'])+abs(B['t']),8)
 elif family=='root-reciprocal':
  A=pick(lambda g:g.is_Pow and g.base==u and g.exp>0);B=pick(lambda g:g==1/u);cap(A['dv'],4);cap(A['hv'],4);cap(B['hv'],8);cap(U**2,4);cap(A['t'],12);cap(B['t'],4);cap(abs(A['t'])+abs(B['t']),12);height(A['t']+B['t'],24,4)
 elif family=='cross-roots':
  A=pick(lambda g:g==u);B=pick(lambda g:g==s.sqrt(u));cap(s.sqrt(U),2);cap(s.sqrt(V),2);cap(B['hv'],16);cap(2*s.sqrt(U),4);cap(A['t'],8);cap(B['t'],8);cap(abs(A['t'])+abs(B['t']),12);height(A['t']+B['t'],24,4)
 elif family=='cos-log-sin':
  A=primitive(s.log);B=primitive(s.sin);cap(A['t']*s.pi,6);cap(B['hv']/s.pi,4);cap(B['t']/s.pi,2)
 elif family=='cot-polynomial':
  A=primitive(s.cot);B=power();n=s.Poly(A['h'],v).degree();m=s.Poly(B['h'],v).degree();cap(V**n,1);cap(V**m,1);cap(B['dv']/s.pi,3);cap(A['t'],3);cap(B['t']/s.pi,3)
 elif family=='log-power-exp':
  A=primitive(s.log);B=power();n=B['g'].exp;cap(U**(n-1),1);cap(A['t']/V,4);cap(B['hv'],6);cap(B['dv']*B['hv']/s.exp(V),10);cap(B['t'],30)
 elif family=='easy-polynomial':
  A=power();B=pick(lambda g:g==u);cap(V**2,4);cap(A['hv'],4);cap(A['dv'],6);cap(A['t'],12);cap(B['t'],4);cap(abs(A['t'])+abs(B['t']),16);assert A['t']!=0 and B['t']!=0
 else:raise AssertionError(family)
 for f in Q[':question/answer-fields']:
  for a in f[':answer-field/choices']:height(q.math(a[':answer/value']),*HEIGHTS[family])
 counts['records']+=1;counts['families'][family]=counts['families'].get(family,0)+1
if __name__=='__main__':
 for r in json.loads((D/'samples.json').read_text()):check(r)
 for r in json.loads((R/'qa'/f'{K}-sampled.json').read_text()):check(r)
 counts.update(status='passed',script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),database_writes=0)
 (R/'qa'/f'{K}-root-workload.json').write_text(json.dumps(counts,indent=2)+'\n');print(counts)
