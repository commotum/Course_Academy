"""Parent reads actual component-vector expressions, ordered terms and banks."""
import importlib.util,json,re,hashlib
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent;ROOT=R.parents[2];K=17592186059710
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);g=importlib.util.module_from_spec(z);z.loader.exec_module(g);return g
p=load(R/'ode-scalar-parser.py','rootcomponentparser');proxies=(p.x,p.y,p.z);basis=(p.i,p.j,p.k)
def scalar(z):
 z=z.strip().rstrip('.,');bits=re.split(r'(\\[A-Za-z]+)',z)
 for j in range(0,len(bits),2):bits[j]=bits[j].translate(str.maketrans({'a':'x','b':'y','c':'z'}))
 return p.scalar(''.join(bits))
def vector(expr):
 expr=s.expand(expr);out=tuple(expr.coeff(z) for z in basis);assert s.expand(expr-sum(a*b for a,b in zip(out,basis)))==0;return out
def same(a,b):return s.expand(a-b)==0
def task(q):
 prompt=q[':question/problem'];m=re.search(r'Find \$(.*?)\$',prompt);assert m;op=m[1];operation=scalar(op);givens={}
 for tag,raw in re.findall(r'\$([abc])\s*=\s*(.*?)\$',prompt):givens[tag]=scalar(raw)
 assert set(givens)==({'a','b','c'} if 'c' in op else {'a','b'});subs={proxy:givens[tag] for proxy,tag in zip(proxies,'abc') if tag in givens};answer=s.expand(operation.subs(subs));weights=[s.diff(operation,proxy) for proxy in proxies[:len(givens)]];assert not any(w.free_symbols for w in weights);assert same(operation,sum(w*proxy for w,proxy in zip(weights,proxies)));return op,operation,givens,subs,weights,answer

def check():
 g=load(ROOT/f'generate/scratch/{K}.py','componentg');originals=json.loads((R/f'sources/{K}.json').read_text())['record'][':knowledge-point/questions'];cases=json.loads((ROOT/f'generate/scratch/{K}/source-cases.json').read_text());src=dict(prompts=0,solutions=0,fields=0,values=0,recorded_keys=0,inferred_unique_source_answers=0,fieldless_sources=0)
 for c in cases:
  q0=next(q for q in originals if q[':question/math-academy-id']==c['source_id']);q=g.generate(c['level'],template=c['template'],parameters=c['parameters'],profile=c['bank_profile'])['question']
  for key in (':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields'):
   assert (key in q)==(key in q0),(c,key)
   if key in q and key!=':question/answer-fields':assert q[key]==(q0[key].get(':db/ident') if isinstance(q0[key],dict) else q0[key])
  src['prompts']+=1;src['solutions']+=(':question/worked-solution' in q0);op,operation,givens,subs,weights,answer=task(q0)
  if ':question/answer-fields' not in q0:src['fieldless_sources']+=1;continue
  for f,f0 in zip(q[':question/answer-fields'],q0[':question/answer-fields']):
   assert f[':answer-field/key']==f0[':answer-field/key'] and f[':answer-field/type']==f0[':answer-field/type'][':db/ident'];assert sorted(z[':answer/value'] for z in f[':answer-field/choices'])==sorted(z[':answer/value'] for z in f0[':answer-field/choices']);src['fields']+=1;src['values']+=len(f[':answer-field/choices']);assert (':answer-field/correct' in f)==(':answer-field/correct' in f0);assert sum(same(scalar(z[':answer/value']),answer) for z in f0[':answer-field/choices'])==1;src['inferred_unique_source_answers']+=1
 records=json.loads((R/f'qa/{K}-sampled.json').read_text());n=dict(records=0,solution_stages=0,individual_distributed_terms=0,choices=0,complete_method_banks=0,prose_operation_claims=0)
 for r in records:
  q=r['question'];op,operation,givens,subs,weights,answer=task(q);sol=q[':question/worked-solution'];prose=re.search(r'To compute \$(.*?)\$',sol);assert prose and same(scalar(prose[1]),operation);n['prose_operation_claims']+=1
  block=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S);assert block;rows=block[1].split(r'\\');distributed=None
  for row in rows:
   lhs,rhs=re.split(r'&\s*=',row,maxsplit=1)
   if lhs.strip():assert same(scalar(lhs),operation)
   actual=scalar(rhs).subs(subs);assert same(actual,answer),(op,row,answer);n['solution_stages']+=1
   # The distributed source stage has only signed coefficient*basis terms,
   # before parenthesized component collection and final reduction.
   if distributed is None and '(' not in rhs and ')' not in rhs and len(re.findall('[ij]',rhs))==2*len(givens):distributed=rhs
  assert distributed is not None,(op,rows)
  terms=[scalar(z) for z in re.findall(r'[+-]?\s*\d*\s*[ij]',distributed)];want=[]
  for w,tag in zip(weights,'abc'):
   if tag not in givens:break
   comp=vector(givens[tag]);want.extend([w*comp[0]*p.i,w*comp[1]*p.j])
  assert len(terms)==len(want) and all(same(a,b) for a,b in zip(terms,want)),(terms,want);n['individual_distributed_terms']+=len(terms)
  field=q[':question/answer-fields'][0];vals=[]
  for option in field[':answer-field/choices']:
   actual=scalar(option[':answer/value']);vector(actual);assert same(actual,answer)==(option[':answer/id']==field[':answer-field/correct'][1]);assert not any(same(actual,z) for z in vals);vals.append(actual);n['choices']+=1
  vs=[vector(givens[tag]) for tag in givens];X,Y=vector(answer)[:2];ax,ay=vs[0][:2];bx,by=vs[1][:2]
  profile=r['generation'].get('profile',r['generation'].get('bank_profile'))
  if profile=='observed-add':expected=[(X,Y),(ax-bx,-ay-by),(X,-Y),(bx-ax,ay-by),(ax-bx,Y)]
  elif '(' in op:
   m=re.fullmatch(r'([+-]?\d*)a-(\d+)\(b-(.*)\)',op);assert m,op;P=int(m[1]);Q=int(m[2]);Z=scalar(m[3]).coeff(p.z);cx,cy=vs[2][:2];expected=[(X,Y),(P*ax-Q*bx-Q*Z*cx,P*ay-Q*by-Q*Z*cy),(P*ax-Q*bx+Z*cx,P*ay-Q*by+Z*cy),(P*ax-Q*bx+Q*cx,P*ay-Q*by+Q*cy),(X,ay+by+cy)]
  elif weights==[1,1]:expected=[(X,Y),(ax-bx,ay-by),(X,-Y),(ax-bx,Y),(X,ay-by)]
  else:
   idx=next(j for j,w in enumerate(weights) if abs(w)>1);w=weights[idx];vv=vs[idx];expected=[(X,Y),(X+(1-w)*vv[0],Y+(1-w)*vv[1]),(X-2*weights[-1]*vs[-1][0],Y-2*weights[-1]*vs[-1][1]),(X,sum(vv[1] for vv in vs)),(sum(vv[0] for vv in vs),Y)]
  assert all(any(same(z,w[0]*p.i+w[1]*p.j) for w in expected) for z in vals),(profile,op,vals,expected);n['complete_method_banks']+=1;n['records']+=1
 out=dict(status='passed',kp_id=K,source=src,readback=n,script_sha256=hashlib.sha256((ROOT/f'generate/scratch/{K}.py').read_bytes()).hexdigest());(R/f'qa/{K}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
if __name__=='__main__':check()
