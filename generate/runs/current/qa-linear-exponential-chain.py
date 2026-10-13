"""Parent actual-function, component, complete-bank and tangent readback."""
import json,re,hashlib,importlib.util
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent;ROOT=R.parents[2];K=17592186092260
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
p=load(R/'ode-scalar-parser.py','linearchainparser');x,y,u=p.x,p.y,p.u
def scalar(t):return p.scalar(t.strip().rstrip('.,'))
def same(a,b):return s.simplify(s.expand(a-b))==0
def stages(t):return t.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').strip().split(r'\\')
def rhs(t):return t.replace('&','').split('=',1)[1].strip().rstrip('.,')
def function(q):
 text=q[':question/problem'];z=re.search(r'(?:f\(x\)|y)\s*=\s*([^$]*)\$',text);assert z;F=scalar(z[1]);criterion='line' if 'equation of the tangent' in text else 'slope' if 'slope' in text else 'derivative';at=None
 if criterion!='derivative':
  z=re.search(r'where \$x\s*=\s*(.*?)\$',text);assert z;at=scalar(z[1]);answer=s.diff(F,x).subs(x,at)
  if criterion=='line':answer=s.expand(answer*(x-at)+F.subs(x,at))
 else:answer=s.diff(F,x)
 return F,criterion,at,answer
def evaluation(t,at):
 t=t.strip().rstrip('.,')
 # Remove and independently verify a source evaluation marker, retaining its
 # actual preceding expression rather than replacing it with a metadata value.
 z=re.search(r'_\{x=(.*)\}$',t)
 if z:
  assert same(scalar(z[1]),at);t=t[:z.start()]
  if t.endswith('{|}'):t=t[:-3]
  elif t.endswith(')|}') and t.startswith('{('):t=t[2:-3]
  else:raise AssertionError(('unknown evaluation marker',t))
 return scalar(t).subs(x,at)
def raw(g):
 originals=json.loads((R/f'sources/{K}.json').read_text())['record'][':knowledge-point/questions'];C=dict(prompts=0,solutions=0,values=0,fields=0,keys=0,unrated=0,fieldless=0,missing_keys=0)
 for case in json.loads((ROOT/f'generate/scratch/{K}/source-cases.json').read_text()):
  old=next(z for z in originals if case['source_id'] in (z[':db/id'],z[':question/id'],z[':question/math-academy-id']));q=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile'])['question'];assert q[':question/problem']==old[':question/problem'];C['prompts']+=1
  for key in (':question/difficulty',':question/worked-solution',':question/answer-fields'):assert (key in q)==(key in old)
  if ':question/worked-solution' in old:assert q[':question/worked-solution']==old[':question/worked-solution'];C['solutions']+=1
  if ':question/difficulty' in old:assert q[':question/difficulty']==old[':question/difficulty'][':db/ident']
  else:C['unrated']+=1
  if ':question/answer-fields' not in old:C['fieldless']+=1
  assert len(q.get(':question/answer-fields',[]))==len(old.get(':question/answer-fields',[]))
  for f,f0 in zip(q.get(':question/answer-fields',[]),old.get(':question/answer-fields',[])):
   assert f[':answer-field/key']==f0[':answer-field/key'] and f[':answer-field/type']==f0[':answer-field/type'][':db/ident'];assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in f0[':answer-field/choices']);assert (':answer-field/correct' in f)==(':answer-field/correct' in f0)
   if ':answer-field/correct' in f0:assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==f0[':answer-field/correct'][':answer/value'];C['keys']+=1
   else:C['missing_keys']+=1
   C['fields']+=1;C['values']+=len(f[':answer-field/choices'])
 return C
def check():
 g=load(ROOT/f'generate/scratch/{K}.py','linearexpgenerator');source=raw(g);C=dict(records=0,composite_definitions=0,derivative_components=0,chain_stages=0,individual_chain_operands=0,sum_stages=0,evaluation_stages=0,tangent_equations=0,choices=0,whole_banks=0)
 for r in json.loads((R/f'qa/{K}-sampled.json').read_text()):
  q=r['question'];F,criterion,at,answer=function(q);blocks=re.findall(r'\$\$\s*(.*?)\s*\$\$',q[':question/worked-solution'],re.S);defs=re.split(r',\\,',blocks[0]);assert len(defs)==2;outer=scalar(rhs(defs[0]));inner=scalar(rhs(defs[1]));assert s.diff(inner,x,2)==0 and s.diff(inner,x)!=0
  helper=outer.subs(u,inner);expterms=[a for a in s.Add.make_args(F) if a.has(s.exp)];assert len(expterms)==1;is_sum=not same(helper,F)
  if is_sum:assert helper in (expterms[0],-expterms[0])
  C['composite_definitions']+=2;D=s.diff(outer,u);I=s.diff(inner,x);components=re.split(r',\\,',blocks[1]);assert len(components)==2 and same(scalar(rhs(components[0])),D) and same(scalar(rhs(components[1])),I);C['derivative_components']+=2
  chain=stages(blocks[2]);assert len(chain)==4 and r'\cdot' in rhs(chain[0]);operands=rhs(chain[1]).split(r'\cdot');assert len(operands)==2 and same(scalar(operands[0]),D) and same(scalar(operands[1]),I);C['individual_chain_operands']+=2
  for z in chain[1:]:assert same(scalar(rhs(z)).subs(u,inner),s.diff(helper,x));C['chain_stages']+=1
  assert 'u' in rhs(chain[2]) and 'x' in rhs(chain[3]);tail=blocks[3:]
  if is_sum:
   rows=stages(tail.pop(0));assert len(rows)==3;operand=rhs(rows[0]).split(r'\frac{\text{d}}{\text{d}x}',1)[1];assert same(scalar(operand),F)
   for z in rows[1:]:assert same(scalar(rhs(z)),s.diff(F,x));C['sum_stages']+=1
  if criterion=='slope':
   rows=stages(tail.pop(0));assert len(rows)==4
   for z in rows:assert same(scalar(z.split('&',1)[1].lstrip(' =')),answer);C['evaluation_stages']+=1
   for z in re.findall(r'\$x=(.*?)\$',q[':question/worked-solution']):assert same(scalar(z),at)
  elif criterion=='line':
   for block,want in zip(tail[:2],(s.diff(F,x).subs(x,at),F.subs(x,at))):
    rows=stages(block);assert len(rows)==3
    for z in rows:assert same(evaluation(z.split('&',1)[1].lstrip(' =').rstrip('.'),at),want);C['evaluation_stages']+=1
   rows=stages(tail[2]);assert len(rows)==4;assert rows[0].replace('{','').replace('}','').strip().startswith('y-y_1')
   for z in rows[1:]:
    L,D0=z.replace('&','').split('=',1);assert same((scalar(L)-scalar(D0)).subs(y,answer),0);C['tangent_equations']+=1
   assert same(scalar(rhs(rows[-1])),answer);tail=[]
   level=q[':question/difficulty'].split('/')[-1];assert same(at,(1-inner.subs(x,0))/I)
   if level=='hard':assert inner.subs(x,0)!=0 and not same(F-expterms[0],0) and inner.subs(x,0)!=1
  assert not tail
  for f in q[':question/answer-fields']:
   vals=[]
   for a in f[':answer-field/choices']:
    value=scalar(a[':answer/value'].split('=',1)[-1]);assert same(value,answer)==(a[':answer/id']==f[':answer-field/correct'][1]);assert all(not same(value,w) for w in vals);vals.append(value);C['choices']+=1
   assert len(vals)==(5 if f[':answer-field/type'].endswith('/radio') else 1)
   if len(vals)==5:
    a=s.diff(inner,x);b=inner.subs(x,0);c=s.diff(outer,u)/s.exp(u);assert not c.has(u);E=s.exp(inner);d=s.simplify(F-c*E);template=r['generation']['template']
    if criterion=='line':
     v=F.subs(x,at);m=s.diff(F,x).subs(x,at);expected=[answer,c*s.E*x,s.E*x,a*s.E*x,c*a*s.E*x*s.log(c)] if template=='q-48657' else [answer,m*x+v,c*s.E*(x-at)+v,-m*(x-at)+v,m*(x-at)+c*s.E]
    elif criterion=='slope':
     k=s.simplify(s.exp(inner.subs(x,at)));expected=[answer,c*k,-k,-c*s.exp(b),-c*s.exp(k)]
    elif template=='q-48007':expected=[answer,c*E,c*E/a,-c*a*E,c*a*E+d]
    elif template=='q-11816':expected=[answer,E/a,x*E,a*x*E,E]
    elif template=='q-11817':expected=[answer,E/a,a*x*E,E,(a*x+b)*E]
    elif template=='q-48003':expected=[answer,c*E,c*a*x*E,c*a*s.exp(a*x),c*a*s.exp(x+b)]
    elif template=='q-107420':
     n=s.degree(F+E,x);expected=[answer,n*x**(n-1)-E,n*x**(n-1)+a*E,x**n-a*E,-a*E]
    elif template=='q-340496':
     rr=s.expand(F-E).coeff(x);expected=[answer,rr+E,rr+E/a,rr-a*E,a*E]
    else:raise AssertionError(template)
    assert all(any(same(v,w) for w in expected) for v in vals),(template,vals,expected)
   C['whole_banks']+=1
  C['records']+=1
 out=dict(status='passed',kp_id=K,source=source,readback=C,script_sha256=hashlib.sha256((ROOT/f'generate/scratch/{K}.py').read_bytes()).hexdigest());(R/f'qa/{K}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
if __name__=='__main__':check()
