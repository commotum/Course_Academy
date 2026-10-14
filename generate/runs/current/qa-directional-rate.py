"""Root actual function, point/direction and individual gradient/dot stages."""
import importlib.util,json,re,hashlib,itertools,sys
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186124460;D=R.parents[2]/f'generate/scratch/{K}'
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
p=load(R/'divergence-readback.py','parent_directional');x,y,z=p.variables;i,j,k=p.basis
def math(t):return p.scalar(t.strip().rstrip('.,').replace(r'\text{ }',r'\,'))
def equal(a,b):return s.simplify(a-b)==0
def vector(t):
 t=t.strip().rstrip('.')
 def repl(m):
  a,b=m[1].replace(r'\,','').split(',');return '(('+s.latex(math(a))+r')\,i+('+s.latex(math(b))+r')\,j)'
 t=re.sub(r'⟨(.*?)⟩',repl,t).replace(r'\text{ }',r'\,');v=p.vector(t);assert v[2]==0;return s.Matrix(v[:2])
def rows(t):return [v.split(' & =',1)[1].strip().rstrip('.') for v in t.removeprefix(r'\begin{aligned}').removesuffix(r'\end{aligned}').split(chr(92)*2)]
def group(t,pos):
 assert t[pos]=='{';start=pos+1;depth=1;pos+=1
 while depth:depth+=(t[pos]=='{')-(t[pos]=='}');pos+=1
 return t[start:pos-1],pos
def veq(a,b):return len(a)==len(b) and all(equal(c,d) for c,d in zip(a,b))
def split(t,sep='+'):
 depth=0;start=0;out=[]
 for n,c in enumerate(t):
  depth+=(c in '({')-(c in ')}')
  if c==sep and not depth and n>start:out.append(t[start:n]);start=n+1
 out.append(t[start:]);return out
def terms(t):
 depth=0;start=0;out=[]
 for n,c in enumerate(t):
  depth+=(c in '({')-(c in ')}')
  if c in '+-' and not depth and n>start:out.append(t[start:n]);start=n
 out.append(t[start:]);return out
C=dict(records=0,actual_functions=0,points=0,directions=0,formal_operands=0,generic_components=0,substitution_components=0,intermediate_components=0,individual_trig_terms=0,evaluated_components=0,norm_square_components=0,unit_components=0,dot_components=0,dot_product_terms=0,rate_rows=0,signed_conclusions=0,choices=0,whole_method_banks=0,source_operation_masks=0)
g=load(D.with_suffix('.py'),'root_rate_generator');f=load(R/'root-source-fidelity.py','root_rate_source');originals,S=f.check(g,K,D)
records=json.load(open(R/f'qa/{K}-sampled.json'))
for family,level in g.TEMPLATES.items():records.extend(g.generate(level,seed=n,template=family) for n in (631,917))
for rec in records:
 q=rec['question'];prompt=q[':question/problem'];sol=q[':question/worked-solution'];family=rec['generation']['template'];F=math(re.search(r'\$[fg]\(x, ?y\)\s*=\s*(.*?)\$',prompt)[1]);coords=[math(t) for t in re.search(r'at the point \$\((.*?)\)\$',prompt)[1].split(',')];G=s.Matrix([s.diff(F,v) for v in (x,y)]);E=G.subs(dict(zip((x,y),coords))).applyfunc(s.simplify);C['actual_functions']+=1;C['points']+=2
 m=re.search(r'v\s*=\s*⟨([^⟩]+)⟩',prompt);direction=s.Matrix([math(t) for t in m[1].split(',')]) if m else None;sign=-1 if 'decreases' in prompt else 1
 if direction is not None:N=s.sqrt(direction.dot(direction));unit=direction/N;target=s.simplify(E.dot(unit));C['directions']+=2
 else:N=s.sqrt(E.dot(E));target=sign*N
 B=re.findall(r'\$\$\s*(.*?)\s*\$\$',sol,re.S);assert len(B)==(3 if direction is not None else 2);gradblock=B[1] if direction is not None else B[0];rr=rows(gradblock);assert len(rr)==(5 if family in ('sine_quotient','tangent') else 4)
 _,ops=p.derivative_inputs(rr[0]);assert len(ops)==2
 for axis,(v,arg,*_) in zip((x,y),ops):assert str(axis)==v and equal(math(arg),F);C['formal_operands']+=1
 assert veq(vector(rr[1]),sign*G) and veq(vector(rr[2]),sign*E) and veq(vector(rr[-1]),sign*E);C['generic_components']+=2;C['substitution_components']+=2;C['evaluated_components']+=2
 if len(rr)==5:
  assert veq(vector(rr[3]),E);C['intermediate_components']+=2
  left=re.search('⟨(.*?)⟩',rr[2])[1].replace(r'\,','').split(',');right=re.search('⟨(.*?)⟩',rr[3])[1].replace(r'\,','').split(',')
  for a,b in zip(left,right):
   aa,bb=terms(a),terms(b);assert len(aa)==len(bb)==2
   for va,vb in zip(aa,bb):assert equal(math(va),math(vb));C['individual_trig_terms']+=1
 if direction is not None:
  nr=rows(B[0]);assert len(nr)==2;a,b=nr[0].split('=');assert equal(math(a),N) and equal(math(b),N)
  body,end=group(a,len(r'\sqrt'));squares=split(body);assert len(squares)==2
  for raw,v in zip(squares,direction):assert equal(math(raw),v*v);C['norm_square_components']+=1
  assert veq(vector(nr[1]),unit);C['unit_components']+=2
  calc=rows(B[-1]);assert len(calc)==(5 if family=='tangent' else 4);a,b=calc[1].split(r'\cdot',1);assert veq(vector(a),E) and veq(vector(b),unit);C['dot_components']+=4
  numerator,pos=group(calc[2],len(r'\frac'));den,pos=group(calc[2],pos);assert pos==len(calc[2]);den=math(den);products=split(numerator);assert len(products)==2
  for raw,v,w in zip(products,E,unit):assert equal(math(raw),v*w*den);C['dot_product_terms']+=1
  for raw in calc[2:]:assert equal(math(raw),target);C['rate_rows']+=1
 else:
  calc=rows(B[-1]);assert len(calc)==3;inside=calc[0].removeprefix('‖').removesuffix('‖');assert veq(vector(inside),sign*E)
  body,end=group(calc[1],len(r'\sqrt'));squares=split(body);assert len(squares)==2
  for raw,v in zip(squares,E):assert equal(math(raw),v*v);C['norm_square_components']+=1
  assert equal(math(calc[1]),N) and equal(math(calc[2]),N)
  if sign<0:
   conclusion=re.search(r'Therefore, the signed rate.*?is \$(.*?)\.\$',sol,re.S);assert conclusion and equal(math(conclusion[1]),target);C['signed_conclusions']+=1
  else:assert equal(math(calc[-1]),target)
 f=q[':question/answer-fields'][0];choices=f[':answer-field/choices'];values=[math(a[':answer/value']) for a in choices];assert len(values)==5 and all(not equal(a,b) for a,b in itertools.combinations(values,2));assert [a[':answer/id'] for a,v in zip(choices,values) if equal(v,target)]==[f[':answer-field/correct'][1]]
 A,Bv=E;h,k=coords
 dot=lambda a,b:s.simplify(s.Matrix([a,b]).dot(unit))
 if family=='quotient':c=s.cancel(F*y/x**2);want=[target,dot(-A,Bv),dot(A,-Bv),E.dot(direction),dot(A,-c*h/k**2)]
 elif family=='ratio_sum':want=[target,dot(1/k+k/h**2,Bv),dot(A,1/h+h/k**2),dot(1/k+k/h**2,1/h+h/k**2),N]
 elif family=='sine_quotient':c=s.cancel(F.coeff(s.sin(s.pi*x))*y);b=s.cancel((F-c*s.sin(s.pi*x)/y)/(s.pi*x*y));want=[target,E.dot(direction),-target,dot(b*s.pi*k,Bv),E.dot(direction)/N**2]
 elif family=='tangent':c=s.cancel(F.coeff(s.tan(y))/x);want=[target,E.dot(direction),-target,dot(c*s.tan(k),-c*s.tan(h)),dot(-2*c*k,2*c*h)]
 elif family=='exp_bilinear':ex=next(iter(F.atoms(s.exp)));b=s.diff(ex.args[0],x);a=s.cancel((F-ex)/(x*y));want=[target,-target,-s.sqrt((a*k+1)**2+(a*h-1)**2),-s.sqrt(b*b+1),-abs(A)]
 elif family=='sumlog':want=[target,-target,0,-abs(A),-(A+Bv)]
 else:c=s.simplify(F/s.sin(y*s.log(x)));n=s.log(h);want=[target,c*s.sqrt(k*k+n*n),c*s.sqrt((k/h)**2+h*h),abs(A)+abs(Bv),abs(A)]
 assert all(sum(equal(v,w) for w in want)==1 for v in values);C['choices']+=5;C['whole_method_banks']+=1
 source=originals[g.FAMILY_SOURCE[family]].get(':question/worked-solution')
 if source:
  old=re.findall(r'\$\$\s*(.*?)\s*\$\$',source,re.S);assert [len(rows(t)) for t in old]==[len(rows(t)) for t in re.findall(r'\$\$\s*(.*?)\s*\$\$',sol,re.S)];C['source_operation_masks']+=1
  prose=lambda t:re.sub(r'\s+',' ',re.sub(r'\$\$.*?\$\$|\$.*?\$','',t,flags=re.S)).strip()
  if sign>0:assert prose(sol)==prose(source)
 C['records']+=1
out=dict(status='passed',source=S,readback=C,script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest());(R/f'qa/{K}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
