"""Root independent whole geometric line and anchored-parameter QA."""
import importlib.util,json,re,hashlib
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent;ROOT=R.parents[2];K=17592186124464
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);g=importlib.util.module_from_spec(z);z.loader.exec_module(g);return g
G=load(R/'qa-gradient-readback.py','gradientroot');p=G.p;axes=(p.x,p.y,p.z);eq=G.equal;
def scalar(raw):return G.scalar(raw.replace('[','(').replace(']',')'))

def relation(z):
 a,b=z.strip().rstrip('.,').split('=');return scalar(a)-scalar(b)
def parallel(a,b):return any(not eq(a,0) for a in a) and all(eq(z,0) for z in s.Matrix(a).cross(s.Matrix(b)))
def equiv(A,B,t0=False):
 offset=s.Matrix(A[0])-s.Matrix(B[0]);return parallel(A[1],B[1]) and (all(eq(a,0) for a in offset) if t0 else all(eq(a,0) for a in offset.cross(s.Matrix(B[1]))))
def line(z):
 z=z.strip().rstrip('.,');pairs=re.findall(r'⟨([^⟩]*)⟩',z)
 if len(pairs)==2:return tuple(scalar(a) for a in re.split(r'(?<!\\),',pairs[0])),tuple(scalar(a) for a in re.split(r'(?<!\\),',pairs[1]))
 bits=z.split('=');assert len(bits)==3,z;P=[];D=[]
 for axis,raw in zip(axes,bits):
  expr=scalar(raw);a=s.diff(expr,axis);b=s.simplify(expr-a*axis);assert not a.free_symbols and not b.free_symbols and a!=0;assert expr.free_symbols=={axis};P.append(-b/a);D.append(1/a)
 return tuple(P),tuple(D)
def task(q):
 prompt=q[':question/problem'];m=re.search(r'(?:level )?surface \$(.*?)\$ at the point \$(.*?)\$',prompt);assert m,prompt
 curve=relation(m[1]);pt=tuple(scalar(z) for z in m[2].strip().rstrip('.,')[1:-1].split(','));assert len(pt)==3;subs=dict(zip(axes,pt));assert eq(curve.subs(subs),0)
 grad=tuple(s.simplify(s.diff(curve,z).subs(subs)) for z in axes);assert any(not eq(z,0) for z in grad);t0='parameter $t=0$' in prompt
 return curve,pt,grad,t0

def check():
 g=load(ROOT/f'generate/scratch/{K}.py','g464');originals=json.loads((R/f'sources/{K}.json').read_text())['record'][':knowledge-point/questions'];cases=json.loads((ROOT/f'generate/scratch/{K}/source-cases.json').read_text());src=dict(prompts=0,solutions=0,fields=0,values=0,keys=0,missing_legacy_keys=0,geometric_duplicates_disambiguated_by_t0=0)
 for c in cases:
  q0=next(z for z in originals if z[':question/math-academy-id']==c['source_id']);q=g.generate(c['level'],template=c['template'],parameters=c['parameters'],profile=c['bank_profile'])['question']
  assert q[':question/problem']==q0[':question/problem'] and q[':question/worked-solution']==q0[':question/worked-solution'];src['prompts']+=1;src['solutions']+=1;curve,pt,grad,t0=task(q0)
  assert len(q[':question/answer-fields'])==len(q0[':question/answer-fields'])
  for f,f0 in zip(q[':question/answer-fields'],q0[':question/answer-fields']):
   assert f[':answer-field/key']==f0[':answer-field/key'] and f[':answer-field/type']==f0[':answer-field/type'][':db/ident'];assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in f0[':answer-field/choices']);src['fields']+=1;src['values']+=len(f[':answer-field/choices']);assert (':answer-field/correct' in f)==(':answer-field/correct' in f0)
   vals=[line(a[':answer/value']) for a in f0[':answer-field/choices']];valid=[equiv(v,(pt,grad),t0) for v in vals];assert sum(valid)==1
   if t0:src['geometric_duplicates_disambiguated_by_t0']+=sum(equiv(v,(pt,grad)) for v in vals)-1
   if ':answer-field/correct' in f:
    chosen=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert chosen[':answer/value']==f0[':answer-field/correct'][':answer/value'];assert equiv(line(chosen[':answer/value']),(pt,grad),t0);src['keys']+=1
   else:src['missing_legacy_keys']+=1
 records=json.loads((R/f'qa/{K}-sampled.json').read_text());n=dict(records=0,formal_partials=0,gradient_stages=0,rearrangement_relations=0,line_stages=0,prose_points=0,choices=0)
 # Exercise the actual explicit-origin source absent from the 18-seed sample.
 c=next(c for c in cases if c['source_id']=='q-36754');records.append(g.generate(c['level'],template=c['template'],parameters={'translation':[1,-1,2],'signs':[-1,1,-1]}))
 for r in records:
  q=r['question'];curve,point,curvegrad,t0=task(q);sol=q[':question/worked-solution'];m=re.search(r'f\(x,y,z\)=(.*?)\$',sol);assert m;function=scalar(m[1]);level=scalar(re.search(r'level surface \$f\(x,y,z\)=(.*?)\$',sol)[1]);delta=s.simplify((function-level)/curve);assert not delta.free_symbols and delta!=0 and eq(function-level-delta*curve,0)
  grad=tuple(s.simplify(s.diff(function,z).subs(dict(zip(axes,point)))) for z in axes)
  for m in re.finditer(r'∇f\(([^()]*)\)',sol):
   if m[1]=='x,y,z':continue
   pt=tuple(map(scalar,m[1].split(',')));assert len(pt)==3 and all(eq(a,b) for a,b in zip(pt,point));n['prose_points']+=1
  blocks=re.findall(r'\$\$\s*(.*?)\s*\$\$',sol,re.S)
  for block in blocks:
   body=block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','');rows=body.split(r'\\')
   if '∇f(x,y,z)' in block:
    evaluated=False
    for row in rows:
     lhs,rhs=re.split(r'&\s*=',row,maxsplit=1)
     if lhs.strip() and '(x,y,z)' not in lhs:evaluated=True
     raw,c=G.transform(rhs.replace('[','(').replace(']',')'),function,point,grad,3);n['formal_partials']+=c;got=G.vector(raw.replace(r'\,',''));want=grad if evaluated else tuple(s.diff(function,z) for z in axes);assert all(eq(a,b) for a,b in zip(got,want)),(r['generation']['template'],raw,want);n['gradient_stages']+=1
   elif '⟨' in block:
    # Construction stages with gradient label have one explicit basepoint.
    for row in rows:
     chunks=row.replace('&','').split('=')
     for chunk in chunks:
      if chunk.strip()=='r':continue
      if '⟨' not in chunk:continue
      if '∇f' in chunk:
       P=tuple(map(scalar,re.search(r'⟨([^⟩]*)⟩',chunk)[1].split(',')));assert all(eq(a,b) for a,b in zip(P,point));n['line_stages']+=1
      elif len(re.findall(r'⟨([^⟩]*)⟩',chunk))==1:
       actual=tuple(scalar(z) for z in re.split(r'(?<!\\),',re.search(r'⟨([^⟩]*)⟩',chunk)[1]));assert all(eq(a,b) for a,b in zip(actual,grad));n['gradient_stages']+=1
      else:assert equiv(line(chunk),(point,grad),t0),(chunk,point,grad);n['line_stages']+=1
   else:
    for row in rows:
     if '{x}_{0}' in row or '{v}_{x}' in row:continue
     parts=[z.strip().rstrip('.,') for z in row.replace('&','').split('=')]
     if len(parts)==3:assert equiv(line('='.join(parts)),(point,grad),t0);n['line_stages']+=1
     else:
      assert len(parts)==2,row;actual=relation('='.join(parts));ratio=s.simplify(actual/curve);assert not ratio.free_symbols and ratio!=0 and eq(actual-ratio*curve,0),(row,curve);n['rearrangement_relations']+=1
  f=q[':question/answer-fields'][0];vals=[]
  for option in f[':answer-field/choices']:
   actual=line(option[':answer/value']);assert equiv(actual,(point,curvegrad),t0)==(option[':answer/id']==f[':answer-field/correct'][1]);assert not any(equiv(actual,z,t0) for z in vals);vals.append(actual);n['choices']+=1
  n['records']+=1
 out=dict(status='passed',kp_id=K,source=src,readback=n,script_sha256=hashlib.sha256((ROOT/f'generate/scratch/{K}.py').read_bytes()).hexdigest());(R/f'qa/{K}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
if __name__=='__main__':check()
