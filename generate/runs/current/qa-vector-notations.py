"""Parent whole-vector readback for brackets, columns and arrow labels."""
import importlib.util,json,re,sys,hashlib
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent;ROOT=R.parents[2]
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);g=importlib.util.module_from_spec(z);z.loader.exec_module(g);return g
p=load(R/'ode-scalar-parser.py','notationrootparser');proxies=(p.x,p.y,p.z);basis=(p.i,p.j)
variable_mapping={}
def equal(a,b):return s.expand(a-b)==0
def arrow(z):
 z=re.sub(r'\\overset\{\\to\s*\}\{([A-Za-z])\}',lambda m:m[1],z)
 return re.sub(r'([A-Za-z])\^\(→\)',r'\1',z)
def scalar(z):
 z=arrow(z).strip().rstrip('.,:?').replace(r'\,','')
 # A complete vector is replaced before scalar/row parsing; internal column
 # row delimiters cannot be mistaken for the outer solution's row boundaries.
 def pair(raw,sep=','):
  parts=raw.split(sep);assert len(parts)==2,raw
  return '(('+str(p.scalar(parts[0]))+')i+('+str(p.scalar(parts[1]))+')j)'
 z=re.sub(r'⟨([^⟩]*)⟩',lambda m:pair(m[1]),z)
 z=re.sub(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',lambda m:pair(m[1],r'\\'),z,flags=re.S)
 z=re.sub(r'\[\\begin\{aligned\}(.*?)\\end\{aligned\}\]',lambda m:pair(m[1],r'\\'),z,flags=re.S)
 parts=re.split(r'(\\[A-Za-z]+)',z)
 for j in range(0,len(parts),2):parts[j]=parts[j].translate(str.maketrans(variable_mapping))
 z=''.join(parts)
 return p.scalar(z)
def vectors(z):
 # Original substrings retain the individually printed component operations.
 out=[]
 pattern=r'⟨([^⟩]*)⟩|\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}|\[\\begin\{aligned\}(.*?)\\end\{aligned\}\]'
 for m in re.finditer(pattern,z,re.S):
  a=m[1] if m[1] is not None else m[2] if m[2] is not None else m[3];parts=a.replace(r'\,','').split(',' if m[1] is not None else r'\\');assert len(parts)==2;out.append(tuple(p.scalar(v.strip()) for v in parts))
 return out

def task(q):
 global variable_mapping
 text=arrow(q[':question/problem']);pieces=re.findall(r'(?<!\$)\$(?!\$)(.*?)\$(?!\$)',text,re.S);given={};variable_mapping={}
 for piece in pieces:
  m=re.match(r'([abcABCuvwUVW])\s*=\s*(.*)',piece)
  if m:
   index=len(given);assert index<3;variable_mapping[m[1]]='xyz'[index];given[proxies[index]]=scalar(m[2])
 assert given and set(given)<=set(proxies)
 if text.startswith('What is the sum'):operation=p.x+p.y;target='a+b'
 else:
  candidates=[z.strip().rstrip('=., ').strip() for z in pieces if not re.match(r'[abcABCuvwUVW]\s*=',z)]
  assert len(candidates)==1,(text,candidates);target=candidates[0];operation=scalar(target)
 assert operation.free_symbols<=set(given);weights=[s.diff(operation,a) for a in proxies[:len(given)]];assert all(not w.free_symbols for w in weights);assert equal(operation,sum(w*a for w,a in zip(weights,proxies)))
 answer=s.expand(operation.subs(given));return target,operation,given,weights,answer

def source(g,k):
 orig=json.loads((R/f'sources/{k}.json').read_text())['record'][':knowledge-point/questions'];cases=json.loads((ROOT/f'generate/scratch/{k}/source-cases.json').read_text());n=dict(prompts=0,solutions=0,fields=0,values=0,recorded_keys=0,inferred_unique_source_answers=0,fieldless_sources=0)
 for c in cases:
  q0=next(q for q in orig if c['source_id'] in (q[':db/id'],q[':question/id'],q[':question/math-academy-id']));q=g.generate(c.get('level','moderate'),template=c['template'],parameters=c['parameters'],profile=c['bank_profile'])['question']
  for key in (':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields'):
   assert (key in q)==(key in q0),(k,c,key)
   if key in q and key!=':question/answer-fields':assert q[key]==(q0[key].get(':db/ident') if isinstance(q0[key],dict) else q0[key]),(k,c,key)
  n['prompts']+=1;n['solutions']+=(':question/worked-solution' in q0);_,_,givens,_,answer=task(q0)
  if ':question/answer-fields' not in q0:n['fieldless_sources']+=1;continue
  assert len(q[':question/answer-fields'])==len(q0[':question/answer-fields'])
  for f,f0 in zip(q[':question/answer-fields'],q0[':question/answer-fields']):
   assert f[':answer-field/key']==f0[':answer-field/key'] and f[':answer-field/type']==f0[':answer-field/type'][':db/ident'];assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in f0[':answer-field/choices']);n['fields']+=1;n['values']+=len(f[':answer-field/choices']);assert (':answer-field/correct' in f)==(':answer-field/correct' in f0);assert sum(equal(scalar(a[':answer/value']),answer) for a in f0[':answer-field/choices'])==1;n['inferred_unique_source_answers']+=1
 return n

def check(k):
 g=load(ROOT/f'generate/scratch/{k}.py','ng'+str(k));src=source(g,k);records=json.loads((R/f'qa/{k}-sampled.json').read_text());n=dict(records=0,solution_stages=0,individually_printed_components=0,choices=0,complete_method_banks=0)
 for r in records:
  q=r['question'];target,operation,given,weights,answer=task(q);sol=q[':question/worked-solution']
  # Convert inner matrices first, so their \\ rows remain vector components.
  rendered=re.sub(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}|\[\\begin\{aligned\}(.*?)\\end\{aligned\}\]',lambda m:'⟨'+(m[1] if m[1] is not None else m[2]).replace(r'\\',',')+'⟩',sol,flags=re.S)
  b=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',rendered,re.S);assert b,sol;rows=b[1].split(r'\\')
  for row in rows:
   lhs,rhs=re.split(r'&\s*=',row,maxsplit=1)
   if lhs.strip():assert equal(scalar(lhs),operation)
   assert equal(scalar(rhs).subs(given),answer),(k,target,row,answer);n['solution_stages']+=1
   n['individually_printed_components']+=2*len(vectors(rhs))
  # Read separately printed operands/products/inner vectors before accepting
  # a combined equality; equal and opposite component errors could cancel.
  actual_slots=[vectors(re.split(r'&\s*=',row,maxsplit=1)[1]) for row in rows]
  inputs=[given[a] for a in proxies[:len(given)]]
  pair=lambda value:tuple(s.expand(value).coeff(b) for b in basis)
  A0=inputs[0];B0=inputs[1] if len(inputs)>1 else None
  if k==17592186059712:
   if len(inputs)==2:
    w=weights[1];wanted=[[A0,B0],[A0,w*B0],[answer]]
   else:
    target0=target.replace(' ','');m=re.fullmatch(r'.*a([+-])\((.*)\)',target0);assert m
    o=1 if m[1]=='+' else -1;tail=m[2][m[2].index('b')+1:];inside=1 if tail[0]=='+' else -1
    a,b,c=weights;C0=inputs[2];ka=a*A0;qb=b*B0/o;rc=c*C0/(o*inside)
    wanted=[[A0,B0,C0],[ka,qb,rc],[ka,qb+inside*rc],[answer]]
  elif k==17592186059711:
   kind=r['generation']['template']
   if kind=='sum':wanted=[[A0,B0],[answer]]
   elif kind=='scalar':wanted=[[A0],[answer],[answer]]
   elif kind=='subtract':wanted=[[A0,B0],[answer],[answer]]
   else:
    a,b=weights;wanted=[[A0,B0],[a*A0,abs(b)*B0],[answer],[answer]]
  else:
   kind=r['generation']['template']
   if kind.startswith('sum') or kind=='subtract':wanted=[[A0,B0],[answer],[answer]]
   elif kind=='scalar':wanted=[[A0],[answer],[answer]]
   elif kind=='linear_combination':wanted=[[A0,B0],[answer],[answer],[answer]]
   else:
    a,b,c=weights;C0=inputs[2];wanted=[[A0,B0,C0],[answer],[a*A0,(-b)*B0,abs(c)*C0],[a*A0,-b*B0-c*C0],[answer],[answer]]
  assert len(actual_slots)==len(wanted),(k,target,actual_slots,wanted)
  for actual,want in zip(actual_slots,wanted):
   assert len(actual)==len(want),(k,target,actual,want)
   for xy,w in zip(actual,want):assert all(equal(a,b) for a,b in zip(xy,pair(w))),(k,target,xy,pair(w))
  n['ordered_vector_operands']=n.get('ordered_vector_operands',0)+sum(map(len,wanted))
  vals=[];f=q[':question/answer-fields'][0]
  for option in f[':answer-field/choices']:
   z=scalar(option[':answer/value']);assert equal(z,answer)==(option[':answer/id']==f[':answer-field/correct'][1]);assert not any(equal(z,v) for v in vals);vals.append(z);n['choices']+=1
  A=given.get(p.x,0);B=given.get(p.y,0);C=given.get(p.z,0);kind=r['generation']['template'];coord=lambda z:(s.expand(z).coeff(p.i),s.expand(z).coeff(p.j));xy=lambda X,Y:X*p.i+Y*p.j;ax,ay=coord(A);bx,by=coord(B);X,Y=coord(answer)
  if k==17592186059711:
   if kind=='sum':expected=[answer,xy(ax-bx,Y),xy(X,ay-by),A-B,xy(Y,X)]
   elif kind=='subtract':expected=[answer,xy(ax-bx,ay+by),xy(-(ax-bx),ay-by),xy(ax+bx,ay-by),A+B]
   elif kind=='scalar':w=weights[0];expected=[answer,xy(w*ax,ay),xy(ax,w*ay),-answer,xy(ax+w,ay+w)]
   elif kind=='linear':w=weights[1];expected=[answer,xy(-ax+w*bx,Y),-A+w*B,xy(X,-ay+w*by),xy(X,-Y)]
   else:a,b=weights;expected=[answer,A+b*B,a*A+B,a*A-b*B,xy(a*ax+b*by,a*ay+b*bx)]
  elif k==17592186059713:
   if kind.startswith('sum'):expected=[answer,A-B,B-A,xy(ax+bx,ay-by),xy(ax-bx,ay+by)]
   elif kind=='subtract':expected=[answer,A+B,B-A,xy(ax-bx,ay+by),xy(ax+bx,ay-by)]
   elif kind=='scalar':w=weights[0];expected=[answer,-answer,xy(ax+w,ay+w),xy(-X,Y),xy(-ax-w,-ay-w)]
   elif kind=='linear_combination':a,b=weights;expected=[answer,a*A-b*B,A+b*B,a*A+s.sign(b)*B,xy(X,ay+s.sign(b)*by)]
   else:
    a,b,c=weights;expected=[answer,a*A+b*B-c*C,a*A-b*B-c*C,A+b*B+c*C,a*A+s.sign(b)*B+s.sign(c)*C]
  else:
   if kind=='two_vectors':w=weights[1];expected=[answer,A-w*B,A+B,A+xy(w*bx,by),A+xy(bx,w*by)]
   else:
    a,b,c=weights;inner=b*B+c*C
    m=re.fullmatch(r'.*a([+-])\((.*)\)',target.replace(' ',''));assert m,target
    outer=1 if m[1]=='+' else -1;tail=m[2][m[2].index('b')+1:];assert tail[0] in '+-';inside=1 if tail[0]=='+' else -1
    omit= A+inner if kind=='nested_minus_plus_left_scaled' else a*A+outer*B+c*C;expected=[answer,a*A-inner,a*A+b*B-c*C,omit,a*A+b*B+outer*inside*C]
  assert all(any(equal(z,w) for w in expected) for z in vals),(k,kind,vals,expected);n['complete_method_banks']+=1;n['records']+=1
 out=dict(status='passed',kp_id=k,source=src,readback=n,script_sha256=hashlib.sha256((ROOT/f'generate/scratch/{k}.py').read_bytes()).hexdigest());(R/f'qa/{k}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
if __name__=='__main__':
 for k in map(int,sys.argv[1:]):check(k)
