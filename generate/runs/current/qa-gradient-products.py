"""Parent actual-factor, derivative and complete product-property bank readback."""
import importlib.util,json,re,hashlib
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent;ROOT=R.parents[2];K=17592186124447
sp=importlib.util.spec_from_file_location('productreadback',R/'qa-gradients.py');p=importlib.util.module_from_spec(sp);sp.loader.exec_module(p)
def scalar(t):return p.scalar(t.replace('[','(').replace(']',')').strip().rstrip('.,?'))
def vector(t):return p.vector(t.replace('[','(').replace(']',')'))
def equal(a,b):
 d=s.expand(a-b)
 if d==0:return True
 return s.cancel(d)==0 or s.simplify(d)==0
def same(v,w):return len(v)==len(w) and all(equal(a,b) for a,b in zip(v,w))
def factors(text):
 pattern=r'(?<!∇)([fgh])\(x,\s*y(?:,\s*z)?\)\s*(?:&\s*)?=\s*(.*?)(?=\$|,\\(?:,|quad)|\\end\{aligned\}|\\\\)'
 objects={m[1]:scalar(m[2]) for m in re.finditer(pattern,text,re.S)};assert len(objects)==2,(text,objects);n=3 if any(v.has(p.axes[2]) for v in objects.values()) else 2;return objects,n
def transform(text,objects,n,stats):
 def partial(m):return '('+s.latex(s.diff(objects[m[1]],p.axes['xyz'.index(m[2])]),ln_notation=True)+')'
 text=re.sub(r'\\frac\{∂([fgh])\}\{∂([xyz])\}',partial,text)
 def grad(m):return '('+s.latex(sum(s.diff(objects[m[1]],a)*b for a,b in zip(p.axes[:n],p.basis)),ln_notation=True)+')'
 text=re.sub(r'∇([fgh])\(x,\s*y(?:,\s*z)?\)',grad,text)
 text=re.sub(r'([fgh])\(x,\s*y(?:,\s*z)?\)',lambda m:'('+s.latex(objects[m[1]],ln_notation=True)+')',text)
 # A formal operator's operand is verified before substitution into a row.
 while (m:=re.search(r'\\frac\{∂\}\{∂([xyz])\}\(',text)):
  start=m.end()-1;depth=0
  for end in range(start,len(text)):
   depth+=(text[end]=='(')-(text[end]==')')
   if depth==0:break
  operand=scalar(text[start+1:end]);assert any(equal(operand,F) for F in objects.values());d=s.diff(operand,p.axes['xyz'.index(m[1])]);text=text[:m.start()]+'('+s.latex(d,ln_notation=True)+')'+text[end+1:];stats['formal_inputs']+=1
 return text
def check():
 g=p.load(ROOT/f'generate/scratch/{K}.py','productg');src=json.loads((R/f'sources/{K}.json').read_text())['record'][':knowledge-point/questions'];counts=dict(prompts=0,solutions=0,values=0,keys=0)
 for c in json.loads((ROOT/f'generate/scratch/{K}/source-cases.json').read_text()):
  q0=next(q for q in src if c['source_id'] in (q[':db/id'],q[':question/id'],q[':question/math-academy-id']));q=g.generate(c.get('level','moderate'),template=c['template'],parameters=c['parameters'],profile=c.get('bank_profile',c.get('profile')))['question'];assert q[':question/problem']==q0[':question/problem'];counts['prompts']+=1
  for key in (':question/worked-solution',':question/difficulty'):
   assert (key in q)==(key in q0)
   if key in q:assert q[key]==(q0[key].get(':db/ident') if isinstance(q0[key],dict) else q0[key]),(c,key,q[key],q0[key])
  counts['solutions']+=(':question/worked-solution' in q0);f=q[':question/answer-fields'][0];f0=q0[':question/answer-fields'][0];assert f[':answer-field/key']==f0[':answer-field/key'] and f[':answer-field/type']==f0[':answer-field/type'][':db/ident'];assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in f0[':answer-field/choices']);assert (':answer-field/correct' in f)==(':answer-field/correct' in f0);counts['values']+=len(f[':answer-field/choices']);objects,n=factors(q0[':question/problem']);F,G=objects.values();D=tuple(s.diff(F*G,a) for a in p.axes[:n])+(s.S.Zero,)*(3-n)
  if ':answer-field/correct' in f0:assert same(vector(f0[':answer-field/correct'][':answer/value']),D);counts['keys']+=1
 stats=dict(records=0,formal_inputs=0,scalar_stages=0,vector_stages=0,supplied_gradients=0,choices=0,complete_method_banks=0,translated_contribution_masks=0)
 records=json.loads((R/f'qa/{K}-sampled.json').read_text())
 for family in g.FAMILIES:
  for profile in (('method',) if family in g.OPAQUE else ('observed','method')):
   records.append(g.generate(g.FAMILY_LEVELS[family],seed=38,template=family,profile=profile))
 for r in records:
  q=r['question'];objects,n=factors(q[':question/problem']);F,G=objects.values();A=tuple(s.diff(F,a) for a in p.axes[:n]);B=tuple(s.diff(G,a) for a in p.axes[:n]);D=tuple(s.diff(F*G,a) for a in p.axes[:n]);full=lambda v:tuple(v)+(s.S.Zero,)*(3-n)
  for m in re.finditer(r'∇([fgh])\(x,\s*y(?:,\s*z)?\)=([^\n]*?)(?=,\s*&|\s*&|\\\\|\\end\{aligned\})',q[':question/problem']):
   assert same(vector(m[2]),full(tuple(s.diff(objects[m[1]],a) for a in p.axes[:n])));stats['supplied_gradients']+=1
  current=None
  for block in re.findall(r'\$\$\s*(.*?)\s*\$\$',q[':question/worked-solution'],re.S):
   if r'\begin{aligned}' not in block:continue
   for row in block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\'):
    lhs,rhs=re.split(r'&\s*=',row,maxsplit=1)
    if lhs.strip():
     m=re.search(r'\\frac\{∂([fgh])\}\{∂([xyz])\}',lhs)
     if m:current=('scalar',s.diff(objects[m[1]],p.axes['xyz'.index(m[2])]))
     else:
      m=re.search(r'∇([fgh])\(',lhs);current=('vector',full(tuple(s.diff(objects[m[1]],a) for a in p.axes[:n])) if m else full(D))
    assert current is not None
    for expr in rhs.split('='):
     text=transform(expr.strip().rstrip('.,'),objects,n,stats)
     if current[0]=='scalar':assert equal(scalar(text),current[1]),(r['generation']['template'],row,current);stats['scalar_stages']+=1
     else:assert same(vector(text),current[1]),(r['generation']['template'],row,current);stats['vector_stages']+=1
  f=q[':question/answer-fields'][0];vals=[vector(a[':answer/value']) for a in f[':answer-field/choices']]
  for a,v in zip(f[':answer-field/choices'],vals):assert same(v,full(D))==(a[':answer/id']==f[':answer-field/correct'][1]);stats['choices']+=1
  if r['generation']['profile']=='method':
   expected=[full(D),full(tuple(G*a for a in A)),full(tuple(F*b for b in B)),full(tuple(G*a-F*b for a,b in zip(A,B))),full((D[1],D[0],*D[2:]))];assert len(vals)==5 and all(any(same(v,w) for w in expected) for v in vals);stats['complete_method_banks']+=1
  else:
   family=r['generation']['template']
   if family=='cancel':
    a,b=D;expected=[full((a*p.axes[1],b*p.axes[0])),full((a*p.axes[0],b*p.axes[1])),full(D),full((-a,b)),full((a,-b))]
   else:
    q0=next(q0 for q0 in src if q0[':question/math-academy-id']==g.FAMILIES[family]);original,n0=factors(q0[':question/problem']);offsets=r['generation']['parameters'];sub={a:a-offsets.get(str(a)+'0',0) for a in p.axes[:n]}
    assert all(equal(objects[name],obj.subs(sub,simultaneous=True)) for name,obj in original.items())
    expected=[tuple(e.subs(sub,simultaneous=True) for e in vector(a[':answer/value'])) for a in q0[':question/answer-fields'][0][':answer-field/choices']]
   assert len(vals)==5 and all(any(same(v,w) for w in expected) for v in vals);stats['complete_observed_banks']=stats.get('complete_observed_banks',0)+1
  if r['generation']['template']=='log_product':
   last=re.findall(r'\$\$\s*(.*?)\s*\$\$',q[':question/worked-solution'],re.S)[-1];termrow=last.split(r'\\')[-2];assert len(re.findall(r'\)[ij](?=\+|$)',termrow.strip()))==4,termrow
   args=sorted(F.atoms(s.log),key=str);assert len(args)==2
   for atom in args:assert s.latex(atom.args[0]**2) in termrow,('incidental expanded-coordinate workload',termrow,atom)
   stats['translated_contribution_masks']+=1
  stats['records']+=1
 out=dict(status='passed',kp_id=K,source=counts,readback=stats,script_sha256=hashlib.sha256((ROOT/f'generate/scratch/{K}.py').read_bytes()).hexdigest());(R/f'qa/{K}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
if __name__=='__main__':check()
