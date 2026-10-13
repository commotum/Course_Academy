"""Actual general-base function/fragment, separate chain operands and all banks."""
import json,re,hashlib,importlib.util
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent;ROOT=R.parents[2];K=17592186092261
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
p=load(R/'ode-scalar-parser.py','generalchainparser');x,y,u=p.x,p.y,p.u
def scalar(t):return p.scalar(t.strip().rstrip('.,'))
def same(a,b):return s.simplify(s.expand(a-b))==0
def rows(t):return t.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').strip().split(r'\\')
def rhs(t):return t.split('&',1)[1].lstrip(' =').strip().rstrip('.,') if '&' in t else t.split('=',1)[1].strip().rstrip('.,')
def function(q):
 t=q[':question/problem'];z=re.search(r'(?:f\(x\)|y)\s*=\s*([^$]*)\$',t);assert z;F=scalar(z[1]);D=s.diff(F,x);criterion='slope' if 'slope' in t else 'fragment' if '{{field-1}}$' in t and r'\cdot' in t.split('{{field-1}}',1)[1] else 'derivative';point=None
 if criterion=='slope':z=re.search(r'where \$x\s*=\s*(.*?)\$',t);assert z;point=scalar(z[1]);answer=D.subs(x,point)
 elif criterion=='fragment':factor=scalar(t.split('{{field-1}}',1)[1].replace('$','').strip().removeprefix(r'\cdot').strip());answer=s.simplify(D/factor)
 else:answer=D
 return F,criterion,point,answer
def restriction(t,at):
 t=t.strip().rstrip('.,');match=re.search(r'_\{x=(.*)\}$',t)
 if match:
  assert same(scalar(match[1]),at);t=t[:match.start()]
  if t.startswith('{((') and t.endswith('))|}'):t=t[2:-3]
  elif t.startswith('{(') and t.endswith(')|}'):t=t[2:-3]
  elif t.endswith(r'\big|'):t=t[:-5]
  elif t.endswith('|'):t=t[:-1]
  else:raise AssertionError(('restriction syntax',t))
 return scalar(t).subs(x,at)
def raw(g):
 original=json.loads((R/f'sources/{K}.json').read_text())['record'][':knowledge-point/questions'];C=dict(prompts=0,solutions=0,fields=0,values=0,keys=0,fieldless=0,unrated=0,missing_keys=0)
 for c in json.loads((ROOT/f'generate/scratch/{K}/source-cases.json').read_text()):
  old=next(z for z in original if c['source_id'] in (z[':db/id'],z[':question/id'],z[':question/math-academy-id']));level=old.get(':question/difficulty',{}).get(':db/ident',':question.difficulty/easy').split('/')[-1];q=g.generate(level,template=c['template'],parameters=c['parameters'],profile=c.get('bank_profile',c.get('profile')))['question'];assert q[':question/problem']==old[':question/problem'];C['prompts']+=1
  for key in (':question/difficulty',':question/worked-solution',':question/answer-fields'):assert (key in q)==(key in old)
  if ':question/worked-solution' in old:assert q[':question/worked-solution']==old[':question/worked-solution'];C['solutions']+=1
  if ':question/difficulty' in old:assert q[':question/difficulty']==old[':question/difficulty'][':db/ident']
  else:C['unrated']+=1
  if ':question/answer-fields' not in old:C['fieldless']+=1
  assert len(q.get(':question/answer-fields',[]))==len(old.get(':question/answer-fields',[]))
  for f,f0 in zip(q.get(':question/answer-fields',[]),old.get(':question/answer-fields',[])):
   assert f[':answer-field/type']==f0[':answer-field/type'][':db/ident'] and f[':answer-field/key']==f0[':answer-field/key'];remaining=[scalar(a[':answer/value']) for a in f[':answer-field/choices']]
   for a in f0[':answer-field/choices']:z=scalar(a[':answer/value']);i=next(i for i,w in enumerate(remaining) if same(w,z));remaining.pop(i);C['values']+=1
   assert not remaining and (':answer-field/correct' in f)==(':answer-field/correct' in f0)
   if ':answer-field/correct' in f0:actual=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert same(scalar(actual),scalar(f0[':answer-field/correct'][':answer/value']));C['keys']+=1
   else:C['missing_keys']+=1
   C['fields']+=1
 return C
def check():
 g=load(ROOT/f'generate/scratch/{K}.py','generalexpgenerator');source=raw(g);C=dict(records=0,composition_definitions=0,derivative_components=0,chain_stages=0,individual_chain_operands=0,evaluation_stages=0,prose_conclusions=0,choices=0,complete_method_banks=0)
 for r in json.loads((R/f'qa/{K}-sampled.json').read_text()):
  q=r['question'];F,criterion,at,answer=function(q);sol=q[':question/worked-solution'];blocks=re.findall(r'\$\$\s*(.*?)\s*\$\$',sol,re.S);defs=re.split(r',\\,',blocks[0]);assert len(defs)==2;outer=scalar(rhs(defs[0]));inner=scalar(rhs(defs[1]));assert same(outer.subs(u,inner),F);C['composition_definitions']+=2;D=s.diff(outer,u);I=s.diff(inner,x)
  ds=re.split(r',\\,',blocks[1]);assert len(ds)==2 and same(scalar(rhs(ds[0])),D) and same(scalar(rhs(ds[1])),I);C['derivative_components']+=2
  chain=rows(blocks[2]);template=r['generation']['template'];assert len(chain)==(3 if template in ('q-107459','q-340969') else 4);assert r'\cdot' in rhs(chain[0]);operands=rhs(chain[1]).split(r'\cdot');assert len(operands)>=2
  # The outer scale may itself use a multiplication glyph: the last operand
  # remains the independently printed inner derivative in all source masks.
  assert same(scalar(r'\cdot'.join(operands[:-1])),D) and same(scalar(operands[-1]),I);C['individual_chain_operands']+=2
  for z in chain[1:]:assert same(scalar(rhs(z)).subs(u,inner),s.diff(F,x));C['chain_stages']+=1
  assert not scalar(rhs(chain[-1])).has(u)
  if criterion=='slope':
   stage=rows(blocks[3]);assert len(stage)==(4 if template=='q-340969' else 3)
   for z in stage:assert same(restriction(rhs(z),at),answer);C['evaluation_stages']+=1
   for point in re.findall(r'(?:at|where) \$x=(.*?)\$',sol):assert same(scalar(point),at)
   if 'Therefore,' in sol:
    ending=sol.split('Therefore,',1)[1];point=re.search(r'where \$x=(.*?)\$',ending);stated=re.search(r'is \$(.*?)\$',ending);assert point and stated and same(scalar(point[1]),at) and same(scalar(stated[1]),answer);C['prose_conclusions']+=1
  else:assert len(blocks)==3
  if q[':question/difficulty'].endswith('/hard'):
   P=s.Poly(inner,x);assert P.degree()==3 and all(P.coeff_monomial(x**n)!=0 for n in (1,2,3)) and at in (-1,1);assert all(abs(P.coeff_monomial(x**n))<=3 for n in (1,2,3)) and inner.subs(x,at) in (-1,0,1,2)
  field=q[':question/answer-fields'][0];vals=[]
  for a in field[':answer-field/choices']:
   V=scalar(a[':answer/value']);assert same(V,answer)==(a[':answer/id']==field[':answer-field/correct'][1]);assert all(not same(V,w) for w in vals);vals.append(V);C['choices']+=1
  if len(vals)==5:
   power=next(z for z in outer.atoms(s.Pow) if z.exp==u);base=power.base;c=s.simplify(outer/power);B=base**inner;L=s.log(base);bank=[c*I*B*L,c*I*B,c*B*L,-c*I*B*L,c*I*inner*base**(inner-1)]
   if criterion=='slope':bank=[z.subs(x,at) for z in bank]
   assert all(any(same(V,w) for w in bank) for V in vals);C['complete_method_banks']+=1
  else:assert len(vals)==1
  C['records']+=1
 out=dict(status='passed',kp_id=K,source=source,readback=C,script_sha256=hashlib.sha256((ROOT/f'generate/scratch/{K}.py').read_bytes()).hexdigest());(R/f'qa/{K}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
if __name__=='__main__':check()
