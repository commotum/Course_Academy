"""Actual nonlinear exponent, supplied fragments, full chain and point arithmetic."""
import json,re,hashlib,importlib.util
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent;ROOT=R.parents[2];K=17592186092263
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
base=load(R/'qa-general-exponential-chain.py','nonlinearbase');p=base.p;x,y,u=p.x,p.y,p.u
def scalar(t):return p.scalar(re.sub(r'(?<![A-Za-z])h(?![A-Za-z])','u',t.strip().rstrip('.,')))
def same(a,b):return s.simplify(s.expand(a-b))==0
rows=base.rows;rhs=base.rhs
def restriction(t,at):
 t=t.strip().rstrip('.,');z=re.search(r'_\{x=(.*)\}$',t)
 if z:
  assert same(scalar(z[1]),at);t=t[:z.start()]
  if t.startswith('{(') and t.endswith(')|}'):t=t[2:-3]
  elif t.startswith('{') and t.endswith('|}'):t=t[1:-2]
  elif t.endswith('|'):t=t[:-1]
  else:raise AssertionError(('restriction syntax',t))
 return scalar(t).subs(x,at)
def function(q):
 t=q[':question/problem'];at=None
 if 'y=f(h(x))' in t:
  a=re.search(r'f\(h\)=(.*?)\$',t);b=re.search(r'h\(x\)=(.*?)\$',t);assert a and b;F=scalar(a[1]).subs(u,scalar(b[1]));factor=re.search(r'\$([^$]*)\$\s*$',t);assert factor;supplied=scalar(factor[1].removeprefix(r'\cdot').removeprefix(')/'));quotient=r'=-($' in t
  assert '{{field-1}}' in t and '|' not in t and not re.search(r'^ {4,}\S',t,re.M);answer=-s.diff(F,x)*supplied if quotient else s.diff(F,x)/supplied;criterion='quotient' if quotient else 'product'
 else:
  z=re.search(r'(?:f\(x\)|y)\s*=\s*([^$]*)\$',t);assert z;F=scalar(z[1]);criterion='slope' if 'slope' in t else 'derivative';answer=s.diff(F,x)
  if criterion=='slope':z=re.search(r'where \$x\s*=\s*(.*?)\$',t);assert z;at=scalar(z[1]);answer=answer.subs(x,at)
 return F,criterion,at,s.simplify(answer)
def check():
 g=load(ROOT/f'generate/scratch/{K}.py','nonlinearexpgenerator');base.K=K;source=base.raw(g);C=dict(records=0,composition_definitions=0,derivative_components=0,chain_stages=0,separate_product_operands=0,evaluation_stages=0,supplied_fragment_relations=0,choices=0,complete_method_banks=0)
 records=json.loads((R/f'qa/{K}-sampled.json').read_text());present={r['generation']['template'] for r in records}
 for template,level in [('q-48629','easy'),('q-340949','moderate')]:
  if template not in present:records.append(g.generate(level,seed=3,template=template))
 for r in records:
  q=r['question'];F,criterion,at,answer=function(q);blocks=re.findall(r'\$\$\s*(.*?)\s*\$\$',q[':question/worked-solution'],re.S);defs=re.split(r',\\,',blocks[0]);assert len(defs)==2;outer=scalar(rhs(defs[0]));inner=scalar(rhs(defs[1]));assert same(outer.subs(u,inner),F);C['composition_definitions']+=2;D=s.diff(outer,u);I=s.diff(inner,x)
  if criterion not in ('product','quotient'):P=s.Poly(inner,x);assert 2<=P.degree()<=6 and all(z.q==1 for z in P.all_coeffs())
  ds=re.split(r',\\,',blocks[1]);assert len(ds)==2 and same(scalar(rhs(ds[0])),D) and same(scalar(rhs(ds[1])),I);C['derivative_components']+=2
  chain=rows(blocks[2]);template=r['generation']['template'];assert len(chain)==(3 if template in ('q-48629','q-107452') else 4);assert r'\cdot' in rhs(chain[0]);operands=rhs(chain[1]).split(r'\cdot');assert len(operands)==2 and same(scalar(operands[0]),D) and same(scalar(operands[1]),I);C['separate_product_operands']+=2
  for z in chain[1:]:assert same(scalar(rhs(z)).subs(u,inner),s.diff(F,x));C['chain_stages']+=1
  assert not scalar(rhs(chain[-1])).has(u)
  if criterion=='slope':
   stage=rows(blocks[3]);assert len(stage)==(3 if template=='q-340949' else 4)
   for z in stage:assert same(restriction(rhs(z),at),answer);C['evaluation_stages']+=1
   for point in re.findall(r'at \$x=(.*?)\$',q[':question/worked-solution']):assert same(scalar(point),at)
  else:assert len(blocks)==3
  if q[':question/difficulty'].endswith('/hard'):
   P=s.Poly(inner,x);assert P.degree() in (3,4) and P.coeff_monomial(x**2)!=0 and P.coeff_monomial(1)!=0 and at in (-2,2) and abs(inner.subs(x,at))<=40 and 0<abs(I.subs(x,at))<=100
  field=q[':question/answer-fields'][0];vals=[]
  for a in field[':answer-field/choices']:
   value=scalar(a[':answer/value']);assert same(value,answer)==(a[':answer/id']==field[':answer-field/correct'][1]);assert all(not same(value,w) for w in vals);vals.append(value);C['choices']+=1
   if criterion in ('product','quotient'):
    # Reinsert the actual requested fragment into the actual displayed factor.
    suffix=re.search(r'\$([^$]*)\$\s*$',q[':question/problem'])[1];factor=scalar(suffix.removeprefix(r'\cdot').removeprefix(')/'));complete=-value/factor if criterion=='quotient' else value*factor;assert same(complete,s.diff(F,x));C['supplied_fragment_relations']+=1
  if len(vals)==5:
   if criterion=='slope':V=I.subs(x,at);W=inner.subs(x,at);bank=[V*s.exp(W),s.exp(W),V,V*s.exp(-W),-V*s.exp(W)]
   else:E=s.exp(inner);bank=[I*E,E,I,I+E,-I*E]
   assert all(any(same(v,w) for w in bank) for v in vals);C['complete_method_banks']+=1
  else:assert len(vals)==1
  C['records']+=1
 out=dict(status='passed',kp_id=K,source=source,readback=C,underdefined_originals=['q-167329','q-167783'],excluded_linear_source_exception='q-340955',script_sha256=hashlib.sha256((ROOT/f'generate/scratch/{K}.py').read_bytes()).hexdigest());(R/f'qa/{K}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
if __name__=='__main__':check()
