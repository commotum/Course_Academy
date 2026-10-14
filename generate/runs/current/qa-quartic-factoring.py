"""Root independently reads quartics, every synthetic cell and all printed identities."""
import hashlib,importlib.util,json,re,sys
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent
K=int(sys.argv[1]);D=R.parents[2]/f'generate/scratch/{K}';assert K in (17592186054804,17592186054805)
def mod(n,p):
 sp=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(sp);sys.modules[n]=m;sp.loader.exec_module(m);return m
P=mod('root_quartic_scalar',R/'ode-scalar-parser.py');G=mod('root_quartic_gen',D.with_suffix('.py'));F=mod('root_quartic_source',R/'root-source-fidelity.py');O,Fid=F.check(G,K,D);x=P.x

def scalar(t):return P.scalar(t.replace('&','').replace(r'\,','').strip().rstrip('.,'))
def equal(a,b):return s.cancel(a-b)==0
def spans(t):return re.findall(r'(?<!\$)\$(?!\$)([^$]+)\$(?!\$)',t)
def unpack_underbrace(z):
 # Keep the complete mathematical object; labels underneath are presentation.
 m=re.search(r'\\underbrace\{',z)
 if not m:return z
 j=m.end();depth=1;k=j
 while depth:depth+=(z[k]=='{')-(z[k]=='}');k+=1
 assert z[k:k+2]=='_{';h=k+2;depth=1;end=h
 while depth:depth+=(z[end]=='{')-(z[end]=='}');end+=1
 return z[:m.start()]+z[j:k-1]+z[end:]
def mask(text):
 text=re.sub(r'(?:^\|[^\n]*\n){5}','@TABLE@\n',text,flags=re.M);text=re.sub(r'\$\$.*?\$\$','@DISPLAY@',text,flags=re.S);text=re.sub(r'\$[^$]*\$','@MATH@',text);return re.sub(r'\s+',' ',text).strip()
C=dict(records=0,source_prose_masks=0,synthetic_cells=0,synthetic_divisions=0,quotient_factor_identities=0,root_evaluations=0,answer_values=0,bank_pairs=0,discriminant_sides=0,conclusions=0)
rows=json.load(open(R/f'qa/{K}-sampled.json'))
# All source-shaped normal templates and changed target roots are exercised.
for c in json.load(open(D/'source-cases.json')):
 try:rows.append(G.generate(c.get('level',c.get('difficulty')),template=c['template'],parameters=c['parameters']))
 except ValueError:pass
for rec in rows:
 q,m=rec['question'],rec['generation'];md=q[':question/problem'];sol=q[':question/worked-solution']
 if K==17592186054804:
  f=scalar(re.search(r'p\(x\)\s*=\s*(.*?)\$',md)[1]);given=[scalar(z) for z in re.findall(r'p\(([^)]+)\)',md) if z!='x'];assert len(given)==2
  roots=s.roots(f,x);assert len(roots)==4 and all(v==1 for v in roots.values()) and all(z.is_real for z in roots);ordered=sorted(roots)
  expected=sum(roots) if q[':question/answer-fields'][0][':answer-field/type'].endswith('/radio') else None
 else:
  equality=next(z for z in re.findall(r'\$\$(.*?)\$\$|(?<!\$)\$(?!\$)([^$]+)\$(?!\$)',md,re.S) for z in [z[0] or z[1]] if '= ' in z or '=' in z and 'P(x)' in z and not z.startswith('P(x)'))
  left,right=equality.split('=');f=scalar(left);factor=scalar(right.replace('P(x)','1'));given=[root for root,mult in s.roots(factor,x).items() for _ in range(mult)];assert len(given)==2
  expected=s.cancel(f/factor);assert s.Poly(expected,x).degree()==2 and not s.denom(expected).has(x)
  a,b,c=s.Poly(expected,x).all_coeffs();disc=b*b-4*a*c;assert disc<0
  # The two known linear factors can be repeated; exactly two real factors by multiplicity.
  assert sum(s.roots(f,x).get(z,0) for z in set(given))==2
 assert s.Poly(f,x).degree()==4 and all(f.subs(x,z)==0 for z in given);C['root_evaluations']+=2
 tables=re.findall(r'(?:^\|[^\n]*\n){5}',sol,re.M);assert len(tables)==2
 actual=f;divisors=[]
 for table in tables:
  lines=table.strip().splitlines();cells=[line.strip().strip('|').split('|') for line in lines]
  r=scalar(spans(cells[2][0])[0]);top=[scalar(spans(z)[0]) for z in cells[2][1:]];bottom=[scalar(spans(z)[0]) for z in cells[4][1:]];products=[scalar(spans(z)[0]) for z in cells[3][2:]]
  assert top==s.Poly(actual,x).all_coeffs();assert len(bottom)==len(top) and len(products)==len(top)-1
  carry=top[0];assert bottom[0]==carry
  for i,(v,prod,out) in enumerate(zip(top[1:],products,bottom[1:])):assert prod==r*carry and out==v+prod;carry=out
  assert bottom[-1]==0;quotient=s.Poly.from_list(bottom[:-1],x).as_expr();assert equal(actual,(x-r)*quotient);actual=quotient;divisors.append(r)
  C['synthetic_cells']+=len(top)+len(bottom)+len(products)+1;C['synthetic_divisions']+=1
 assert sorted(divisors)==sorted(given)
 # Every quotient, intermediate factorization and final equation is independently equal.
 blocks=re.findall(r'\$\$(.*?)\$\$',sol,re.S)
 for block in blocks:
  z=unpack_underbrace(block).replace(r'\begin{aligned}','').replace(r'\end{aligned}','').replace('&','').replace(r'\,','')
  if '{b}' in z and '<0' in z:
   parts=z.split('=')[1:]
   for part in parts:assert scalar(part.split('<')[0])==disc;C['discriminant_sides']+=1
   continue
  if re.search(r'\bx\s*=',z):
   found=[scalar(v) for v in re.findall(r'x\s*=\s*([^,]+)',z)];assert sorted(found)==ordered;C['conclusions']+=1;continue
  z=z.replace('f(x)','('+s.latex(f)+')').replace('p(x)','('+s.latex(f)+')').replace('P(x)','('+s.latex(expected)+')' if K==17592186054805 else 'P(x)')
  last=None
  for row in z.split(chr(92)*2):
   for side in row.split('='):
    if not side.strip():continue
    v=scalar(side)
    if last is not None:assert equal(v,last),(K,m['template'],side,last);C['quotient_factor_identities']+=1
    last=v
 for field in q[':question/answer-fields']:
  vals=[scalar(z[':answer/value']) for z in field[':answer-field/choices']]
  if K==17592186054804 and field[':answer-field/type'].endswith('/blank'):
   key=field[':answer-field/key'];idx=int(key.split('-')[-1])-1;assert '{{'+key+'}}' in md;want=ordered[idx]
  else:want=expected
  assert [a[':answer/id'] for a,v in zip(field[':answer-field/choices'],vals) if equal(v,want)]==[field[':answer-field/correct'][1]]
  for i,v in enumerate(vals):
   for w in vals[i+1:]:assert not equal(v,w);C['bank_pairs']+=1
  C['answer_values']+=len(vals)
 if K==17592186054804 and len(q[':question/answer-fields'])==1:
  new=[z for z in roots if z not in given];known=sum(given);total=sum(roots);profile=m['bank_profile'];bank=[total,known,-total,*new] if profile.endswith('opposite_method') else [total,known,sum(new),known-sum(new),known+scalar(m['parameters']['remaining'][0])]
  assert all(any(equal(v,w) for w in vals) for v in bank)
 if K==17592186054805:
  final=re.search(r'Finally, \$P\(x\)=([^$]+)\$',sol);assert final and equal(scalar(final[1]),expected);C['conclusions']+=1
  if q[':question/answer-fields'][0][':answer-field/type'].endswith('/radio'):
   a,b,c=s.Poly(expected,x).all_coeffs();r1,r2=divisors;bank=[expected,expected-2*r1*a*x,expected-r2*a*x,expected-2*r1*(b-r2*a),a*x*x+b*x-c]
   assert all(any(equal(v,w) for w in vals) for v in bank)
 sid=G.SPECS[m['template']]['source'] if K==17592186054804 else m['template']
 if ':question/worked-solution' in O[sid]:
  old=O[sid][':question/worked-solution']
  if sid=='q-112638':old=old.replace('three roots','four roots')
  assert mask(sol)==mask(old),(K,sid,mask(sol),mask(old));C['source_prose_masks']+=1
 C['records']+=1
out={'passed':True,'source_fidelity':Fid,'readback':C,'script_sha256':hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),'database_writes':0};(R/f'qa/{K}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
