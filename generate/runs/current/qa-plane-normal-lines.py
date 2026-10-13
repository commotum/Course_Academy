"""Parent full-relation checks for plane normal lines and printed stages."""
import importlib.util,json,re,sys,hashlib
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent;ROOT=R.parents[2]
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);g=importlib.util.module_from_spec(z);z.loader.exec_module(g);return g
G=load(R/'qa-gradient-readback.py','rootgradient');p=G.p;x,y=p.x,p.y
scalar=G.scalar
def relation(raw):
 raw=raw.strip().rstrip('.,');assert raw.count('=')==1,raw;a,b=raw.split('=');return s.expand(scalar(a)-scalar(b))
def equivalent(a,b):
 if G.equal(a,b):return True
 ratio=s.cancel(a/b);return not ratio.free_symbols and ratio!=0 and ratio.is_finite and G.equal(a-ratio*b,0)
def linecoef(expr):
 expr=s.expand(expr);a,b,c=expr.coeff(x),expr.coeff(y),expr.subs({x:0,y:0});assert G.equal(expr-a*x-b*y-c,0);assert a!=0 or b!=0;return s.Matrix([a,b,c])
def valid(expr,pt,grad):
 a,b,c=linecoef(expr);return G.equal(a*pt[0]+b*pt[1]+c,0) and G.equal(a*grad[0]+b*grad[1],0)
def source(g,k):
 originals=json.loads((R/f'sources/{k}.json').read_text())['record'][':knowledge-point/questions'];cases=json.loads((ROOT/f'generate/scratch/{k}/source-cases.json').read_text());counts=dict(prompts=0,solutions=0,fields=0,values=0,keys=0,independent_keys=0,duplicate_wrong_pairs=0)
 for c in cases:
  q0=next(q for q in originals if c['source_id'] in (q[':db/id'],q[':question/id'],q[':question/math-academy-id']));level=q0.get(':question/difficulty',{}).get(':db/ident',':question.difficulty/moderate').split('/')[-1];q=g.generate(level,template=c['template'],parameters=c['parameters'],profile=c['bank_profile'])['question']
  for key in (':question/problem',':question/worked-solution',':question/difficulty'):
   assert (key in q)==(key in q0)
   if key in q:assert q[key]==(q0[key].get(':db/ident') if isinstance(q0[key],dict) else q0[key]),(c,key)
  counts['prompts']+=1;counts['solutions']+=(':question/worked-solution' in q0)
  curve=relation(re.findall(r'(?<!\$)\$(?!\$)(.*?)\$(?!\$)',q0[':question/problem'])[0]);last=re.findall(r'(?<!\$)\$(?!\$)(.*?)\$(?!\$)',q0[':question/problem'])[-1].strip().rstrip('.');pt=tuple(map(scalar,last[1:-1].split(',')));grad=s.Matrix([s.diff(curve,z).subs(dict(zip((x,y),pt))) for z in (x,y)])
  for f,f0 in zip(q[':question/answer-fields'],q0[':question/answer-fields']):
   assert f[':answer-field/key']==f0[':answer-field/key'] and f[':answer-field/type']==f0[':answer-field/type'][':db/ident'];assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in f0[':answer-field/choices']);counts['fields']+=1;counts['values']+=len(f[':answer-field/choices']);assert (':answer-field/correct' in f)==(':answer-field/correct' in f0)
   vals=[relation(a[':answer/value']) for a in f0[':answer-field/choices']];assert sum(valid(z,pt,grad) for z in vals)==1
   counts['duplicate_wrong_pairs']+=sum(equivalent(a,b) for j,a in enumerate(vals) for b in vals[:j])
   if ':answer-field/correct' in f:
    selected=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert selected[':answer/value']==f0[':answer-field/correct'][':answer/value'];assert valid(relation(selected[':answer/value']),pt,grad);counts['keys']+=1;counts['independent_keys']+=1
 return counts

def check():
 k=17592186124462;g=load(ROOT/f'generate/scratch/{k}.py','normalg');src=source(g,k);records=json.loads((R/f'qa/{k}-sampled.json').read_text());n=dict(records=0,formal_partials=0,gradient_stages=0,line_stages=0,rearrangement_stages=0,prose_claims=0,choices=0)
 for r in records:
  q=r['question'];prompt=q[':question/problem'];sol=q[':question/worked-solution'];math=re.findall(r'(?<!\$)\$(?!\$)(.*?)\$(?!\$)',prompt);curve=relation(math[0]);point=tuple(map(scalar,math[-1].strip().rstrip('.')[1:-1].split(',')));subs=dict(zip((x,y),point));assert G.equal(curve.subs(subs),0)
  curvegrad=s.Matrix([s.diff(curve,z).subs(subs) for z in (x,y)]);assert curvegrad.dot(curvegrad)>0
  definition=re.search(r'If we set \$f\(x,y\)=(.*?)\$',sol);assert definition,sol;function=scalar(definition[1]);level=scalar(re.search(r'level curve \$f\(x,y\)=(.*?)\$',sol)[1]);assert equivalent(function-level,curve);grad=s.Matrix([s.diff(function,z).subs(subs) for z in (x,y)])
  want=s.expand(grad[1]*(x-point[0])-grad[0]*(y-point[1]))
  for m in re.finditer(r'∇f\(([^()]*)\)',sol):
   if m[1]=='x,y':continue
   pt=tuple(map(scalar,m[1].split(',')));assert len(pt)==2 and all(G.equal(a,b) for a,b in zip(pt,point));n['prose_claims']+=1
  normalprose=re.search(r'Hence, \$∇f\([^()]*\)=(.*?)\$',sol);assert normalprose;assert all(G.equal(a,b) for a,b in zip(G.vector(normalprose[1])[:2],grad));n['prose_claims']+=1
  blocks=re.findall(r'\$\$\s*(.*?)\s*\$\$',sol,re.S)
  for block in blocks:
   rows=block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\')
   if '∇f' in block:
    evaluated=False
    for row in rows:
     lhs,rhs=re.split(r'&\s*=',row,maxsplit=1)
     if lhs.strip() and '(x,y)' not in lhs:evaluated=True
     z,c=G.transform(rhs,function,point,grad,2);v=G.vector(z);wantvector=list(grad) if evaluated else [s.diff(function,x),s.diff(function,y)];assert all(G.equal(a,b) for a,b in zip(v[:2],wantvector)) and v[2]==0,(r['generation']['template'],z,wantvector);n['formal_partials']+=c;n['gradient_stages']+=1
   else:
    for j,row in enumerate(rows):
     lhs,rhs=re.split(r'&\s*=',row,maxsplit=1)
     if '{v}' in row or '{x}_{0}' in row:
      assert j==0 and (r'\frac{x-{x}_{0}}{{v}_{x}}' in row or '(x-{x}_{0}){v}_{y}' in row);continue
     actual=relation(lhs+'='+rhs)
     if equivalent(actual,curve):n['rearrangement_stages']+=1
     else:assert equivalent(actual,want),(r['generation']['template'],row,want);n['line_stages']+=1
  f=q[':question/answer-fields'][0];vals=[]
  for option in f[':answer-field/choices']:
   actual=relation(option[':answer/value']);assert valid(actual,point,curvegrad)==(option[':answer/id']==f[':answer-field/correct'][1]);assert not any(equivalent(actual,z) for z in vals);vals.append(actual);n['choices']+=1
  n['records']+=1
 report=dict(status='passed',kp_id=k,source=src,readback=n,script_sha256=hashlib.sha256((ROOT/f'generate/scratch/{k}.py').read_bytes()).hexdigest());(R/f'qa/{k}-root-readback.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':check()
