"""Root domain-inferred coordinates, full banks and separate endpoint components."""
import json,re,sys,hashlib,importlib.util,itertools
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186198373;D=R.parents[2]/f'generate/scratch/{K}'
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
p=load(R/'ode-scalar-parser.py','domain_change_parent_scalar');x,y,u,v=p.x,p.y,p.u,p.v
def math(raw):return p.scalar(raw.replace(r'\operatorname{atan}',r'\arctan').replace(r'\quad','').replace(r'\qquad','').replace(r'\,','').strip().rstrip('.,'))
def eq(a,b):return s.simplify(s.trigsimp(a-b))==0
def group(text,pos,op='{',cl='}'):
 assert text[pos]==op;start=pos+1;depth=1;pos+=1
 while depth:depth+=(text[pos]==op)-(text[pos]==cl);pos+=1
 return text[start:pos-1],pos
def split_terms(raw):
 depth=0;start=0;terms=[]
 for i,c in enumerate(raw):
  depth+=(c in '({[')-(c in ')}]')
  if c in '+-' and depth==0 and i>start:terms.append(raw[start:i]);start=i
 terms.append(raw[start:]);return terms
class Reader:
 def __init__(self,F,inverse,bounds,jac,derivative=False):self.F=F;self.inverse=inverse;self.bounds=bounds;self.jac=jac;self.derivative=derivative;self.primitives=[];self.integrals=0
 def value(self,raw):
  raw=raw.strip().rstrip('.,').replace(r'\left','').replace(r'\right','').replace(r'\mathrm{d}','d').replace(r'\,','').replace(r'\cdot','*')
  raw=raw.replace(r'|\frac{\partial(x,y)}{\partial(u,v)}|','('+s.latex(self.jac)+')')
  m=re.search(r'\\iint_(D|\\Delta)',raw)
  if m:
   suffix='dxdy' if m[1]=='D' else 'dudv';end=raw.index(suffix,m.end());expr=math(raw[m.end():end]);expr=expr.subs(self.inverse,simultaneous=True)*self.jac if m[1]=='D' else expr
   val=s.integrate(expr,(u,*self.bounds[u]),(v,*self.bounds[v]));return self.value(raw[:m.start()]+'('+s.latex(val)+')'+raw[end+len(suffix):])
  m=re.search(r'\\int_',raw)
  if m:
   lo,pos=group(raw,m.end());assert raw[pos]=='^';hi,pos=group(raw,pos+1);matches=list(re.finditer(r'd([uv])',raw[pos:]));assert matches;last=matches[-1];var={'u':u,'v':v}[last[1]];body=raw[pos:pos+last.start()];expr=self.value(body);lo,hi=math(lo),math(hi);assert (lo,hi)==self.bounds[var]
   value=expr if self.derivative else s.integrate(expr,(var,lo,hi));self.integrals+=1;return self.value(raw[:m.start()]+'('+s.latex(value)+')'+raw[pos+last.end():])
  at=raw.find('[')
  if at>=0:
   body,pos=group(raw,at,'[',']')
   if pos==len(raw) or raw[pos]!='_':return self.value(raw[:at]+'('+body+')'+raw[pos:])
   lo,pos=group(raw,pos+1);assert raw[pos]=='^';hi,pos=group(raw,pos+1);expr=math(body);variables=[w for w in (u,v) if expr.has(w)];assert len(variables)==1;var=variables[0];lo,hi=math(lo),math(hi);assert (lo,hi)==self.bounds[var];self.primitives.append((expr,var,lo,hi,body))
   value=s.diff(expr,var) if self.derivative else expr.subs(var,hi)-expr.subs(var,lo);return self.value(raw[:at]+'('+s.latex(value)+')'+raw[pos:])
  return math(raw)
C={key:0 for key in ('records','printed_integrands','inferred_components','jacobian_entries','inverse_stages','inverse_definitions','actual_domains','solution_rows','complete_choices','whole_banks','primitive_derivatives','individual_endpoint_components','operative_checks')}
def check(rec):
 q=rec['question'];prompt=q[':question/problem'];sol=q[':question/worked-solution'];family=rec['generation']['template'];assert sol.count('**Step')==5
 assert not re.search(r'(?<!\\)\{\([xu],\s*[yv]\)',prompt+sol)
 F=math(re.search(r'\\iint_D (.*?)\\,\\mathrm\{d\}x',prompt,re.S)[1]);C['printed_integrands']+=1
 constraints=re.findall(r'([^:,$]*?)\\le (.*?)\\le ([^,]+)',prompt.split('(x,y):')[1].split(r'\}')[0]);assert len(constraints)==2
 U,V=[math(m[1]) for m in constraints];bounds={w:(math(m[0].replace(r'\quad','')),math(m[2])) for w,m in zip((u,v),constraints)};J=s.Matrix([U,V]).jacobian((x,y));det=J.det()
 step1=sol.split('**Step 1**')[1].split('**Step 2**')[0];coords=re.search(r'\bu=(.*?)\\,\\text\{and\}\\,v=(.*?)\.',step1,re.S);assert coords and eq(math(coords[1]),U) and eq(math(coords[2]),V);C['inferred_components']+=2
 invtext=re.search(r'Solving the transformation equations gives \$x=(.*?),\\ y=(.*?)\$',sol,re.S);assert invtext;X,Y=math(invtext[1]),math(invtext[2]);inverse={x:X,y:Y};assert eq(U.subs(inverse,simultaneous=True),u) and eq(V.subs(inverse,simultaneous=True),v);C['inverse_definitions']+=2
 j=s.simplify(1/det.subs(inverse,simultaneous=True));metric=s.Abs(j)
 if family=='radical':
  rad=s.expand(j*j);assert not rad.has(u);assert min(rad.subs(v,end) for end in bounds[v])>0;metric=j
 density=s.simplify(F.subs(inverse,simultaneous=True)*metric);answer=s.integrate(density,(u,*bounds[u]),(v,*bounds[v]));C['actual_domains']+=1
 domain=sol.split('**Step 2**')[1].split('**Step 3**')[0]
 for var in (u,v):
  rawdomain=domain.split('(u,v):',1)[1].split(r'\}',1)[0]
  bit=rawdomain.replace(r'\,','').split(',')[0 if var==u else 1]
  m=re.fullmatch(r'(.*?)\\le '+str(var)+r'\\le (.*)',bit.strip());assert m and all(eq(a,b) for a,b in zip((math(m[1]),math(m[2])),bounds[var])),(var,bit,m.groups() if m else None,bounds[var])
 section=sol.split('**Step 3**')[1].split('**Step 4**')[0];matrices=re.findall(r'\\begin\{matrix\}(.*?)\\end\{matrix\}',section,re.S);assert len(matrices)==2
 M=s.Matrix([[math(c) for c in row.split('&')] for row in matrices[1].split(r'\\')]);assert M==J;C['jacobian_entries']+=4
 tail=section.rsplit('&=',1)[1].split(r'\end{aligned}')[0];assert eq(math(tail),det)
 sec4=sol.split('**Step 4**')[1].split('Solving the transformation equations')[0].split('$$')[1];parts=sec4.split('=')[-2:];assert eq(math(parts[0]),1/det) and eq(math(parts[1]),j);C['inverse_stages']+=2
 chain=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol.split('**Step 5**')[1],re.S)[1];rows=chain.split(r'\\');reader=Reader(F,inverse,bounds,metric);primitive_sequence=[]
 for i,row in enumerate(rows):
  body=(row.split('=',1)[1] if '=' in row else row).replace('&','').strip();value=reader.value(body);assert eq(value,answer),(family,body,value,answer);C['solution_rows']+=1
  if re.search(r'\]_\{',body.replace(r'\right','')):
   derivative=Reader(F,inverse,bounds,metric,True);got=derivative.value(body);assert len(derivative.primitives)==1;prim,var,lo,hi,rawprim=derivative.primitives[0];other=v if var==u else u
   expected=density if len(primitive_sequence)==0 else s.integrate(density,(other,*bounds[other]));assert eq(got,expected),(family,'primitive derivative',got,expected);primitive_sequence.append(var);C['primitive_derivatives']+=1
   nextbody=rows[i+1].split('=',1)[1].replace('&','').replace(r'\left','').replace(r'\right','');endpoint_pattern=re.search(r'\(\((.*)\)-\((.*)\)\)',nextbody);assert endpoint_pattern,(family,nextbody)
   high,low=endpoint_pattern.groups();high='('+high+')';parts=[math(t) for t in split_terms(rawprim.replace(r'\left','').replace(r'\right',''))]
   for text,bound in ((high,hi),(low,lo)):
    text=text.strip()
    observed=[math(z) for z in split_terms(text)];wanted=[t.subs(var,bound) for t in parts];assert len(observed)==len(wanted) and all(eq(a,b) for a,b in zip(observed,wanted)),(family,text,observed,wanted);C['individual_endpoint_components']+=len(observed)
 assert len(primitive_sequence)==2
 values=[math(a[':answer/value']) for a in q[':question/answer-fields'][0][':answer-field/choices']];assert len(values)==5 and all(not eq(a,b) for a,b in itertools.combinations(values,2));f=q[':question/answer-fields'][0];assert [a[':answer/id'] for a,val in zip(f[':answer-field/choices'],values) if eq(val,answer)]==[f[':answer-field/correct'][1]]
 # Separate the actual density into its independent u and v components.
 A=s.Integer(1) if not density.has(u) else u if family in ('radical','sine') else s.simplify(density/(metric*s.Mul(*density.atoms(s.exp)))) if family=='linear_exp' else s.exp(u) if family=='quadratic_exp' else s.Integer(1)
 B=s.simplify(density/(A if family=='radical' else metric*A));Au=s.integrate(A,u);Bv=s.integrate(B,v);a,b=bounds[u];c,d=bounds[v];du=Au.subs(u,b)-Au.subs(u,a);dv=Bv.subs(v,d)-Bv.subs(v,c)
 if family=='radical':R0=s.expand(j*j).subs(v,0);wrongs=[du*s.integrate(R0*v*v,(v,c,d)),du*s.integrate(R0*v*v+v**4,(v,c,d)),2*answer,Au.subs(u,b)*dv if a!=0 else (b-a)*dv]
 elif family=='sine':cosint=s.sin(d)-s.sin(c);wrongs=[metric*du*cosint,-metric*du*cosint,metric*Au.subs(u,b)*cosint,metric*(b-a)*(d-c)*s.sin(d)]
 elif family=='linear' or family=='arctan' and c==0:wrongs=[metric*dv,-answer,metric*du*(s.atan(d*d) if family=='arctan' else d/2),metric*(b-a)*(d-c)*B.subs(v,d)]
 elif family=='gaussian':wrongs=[du*dv,metric*du*(s.exp(d)-s.exp(c))/2,metric*du*(s.exp(d*d)+s.exp(c*c))/2,metric*du*s.exp(d*d)/2]
 else:wrongs=[metric*du*Bv.subs(v,d),metric*du*(Bv.subs(v,d)+Bv.subs(v,c)),metric*(b-a)*(d-c)*B.subs(v,d)*A.subs(u,b),metric*du*(d-c)]
 assert all(sum(eq(z,w) for w in [answer]+wrongs)==1 for z in values),(family,values,[answer]+wrongs);C['complete_choices']+=5;C['whole_banks']+=1;C['records']+=1;C['operative_checks']+=1
if __name__=='__main__':
 g=load(D.with_suffix('.py'),'root_domain_change');old={q[':question/math-academy-id']:q for q in json.load(open(R/f'sources/{K}.json'))['record'][':knowledge-point/questions']};source=dict(prompts=0,solutions=0,fields=0,values=0,refs=0,missing_refs=0,missing_ratings=0)
 for case in json.load(open(D/'source-cases.json')):
  q=g.generate('moderate',template=case['template'],parameters=case['parameters'],profile=case['bank_profile'])['question'];o=old[case['source_id']]
  for key in (':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields'):assert (key in q)==(key in o)
  assert q[':question/problem']==o[':question/problem'];source['prompts']+=1
  if ':question/worked-solution' in o:assert q[':question/worked-solution']==o[':question/worked-solution'];source['solutions']+=1
  source['missing_ratings']+=int(':question/difficulty' not in o)
  for f,of in zip(q[':question/answer-fields'],o[':question/answer-fields']):
   assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in of[':answer-field/choices']);source['fields']+=1;source['values']+=len(of[':answer-field/choices']);assert (':answer-field/correct' in f)==(':answer-field/correct' in of)
   if ':answer-field/correct' in of:assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==of[':answer-field/correct'][':answer/value'];source['refs']+=1
   else:source['missing_refs']+=1
 records=json.load(open(R/f'qa/{K}-sampled.json'))
 for level,families in g.LEVEL_FAMILIES.items():
  for family in families:records.append(g.generate(level,seed=739,template=family))
 for rec in records:check(rec)
 out=dict(status='passed',source=source,readback=C,script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest());(R/f'qa/{K}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
