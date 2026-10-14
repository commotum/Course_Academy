"""Root inferred affine maps, all vertices, separate primitives and full banks."""
import importlib.util,json,re,sys,hashlib,itertools
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186198374;D=R.parents[2]/f'generate/scratch/{K}'
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
b=load(R/'qa-domain-change.py','integrand_parent_base');x,y,u,v=b.x,b.y,b.u,b.v;eq,group=b.eq,b.group
def math(raw):
 raw=re.sub(r'\|([^|]+)\|',r'Abs(\1)',raw);return b.math(raw)
class Reader(b.Reader):
 def value(self,raw):
  raw=raw.strip().rstrip('.,').replace(r'\left','').replace(r'\right','').replace(r'\mathrm{d}','d').replace(r'\,','').replace(r'\cdot','*')
  raw=raw.replace(r'|\frac{\partial(x,y)}{\partial(u,v)}|','('+s.latex(self.jac)+')');raw=re.sub(r'\|([^|]+)\|',r'Abs(\1)',raw)
  depth=0;start=0;parts=[]
  for i,c in enumerate(raw):
   depth+=(c in '({[')-(c in ')}]')
   if c=='*' and depth==0:parts.append(raw[start:i]);start=i+1
  if parts and ('\\int' in raw or '[' in raw):
   parts.append(raw[start:]);return s.Mul(*(self.value(z) for z in parts))
  if '\\int' not in raw and '\\iint' not in raw and '[' not in raw:return math(raw)
  return super().value(raw)
C={k:0 for k in ('records','integrands','inferred_coordinates','inverse_definitions','original_vertices','substituted_vertex_components','mapped_vertices','jacobian_entries','inverse_jacobians','solution_rows','separate_primitive_derivatives','individual_endpoint_components','choices','whole_banks','plot_geometry','factorization_stages')}
def tuple2(raw):
 parts=raw.strip().split(',');assert len(parts)==2;return tuple(math(z) for z in parts)
def check(rec):
 q=rec['question'];prompt=q[':question/problem'];sol=q[':question/worked-solution'];family=rec['generation']['template'];F=math(re.search(r'\\iint_D (.*?)\\,\\mathrm\{d\}x',prompt,re.S)[1]);C['integrands']+=1
 vertices=[tuple2(t) for t in re.findall(r'\$\((.*?)\)\$',prompt.split('vertices')[1])];assert len(vertices)==4
 section=sol.split('**Step 1**')[1].split('**Step 2**')[0];defs=re.search(r'u=(.*?),\\qquad v=(.*?)\.',section,re.S);assert defs;U,V=math(defs[1]),math(defs[2]);J=s.Matrix([U,V]).jacobian((x,y));det=J.det();assert not det.has(x,y) and det!=0;C['inferred_coordinates']+=2
 fdef=re.search(r'f\(x,y\)=(.*?)\$\$',section,re.S)[1];equalities=fdef.split('=');assert all(eq(math(z),F) for z in equalities)
 if family=='cosine_square':assert '(x-y)(x+y)' in fdef;C['factorization_stages']+=1
 inverse_text=re.search(r'\$\$\s*x=(.*?),\\qquad y=(.*?)\.\s*\$\$',sol,re.S);assert inverse_text;inverse={x:math(inverse_text[1]),y:math(inverse_text[2])};assert eq(U.subs(inverse,simultaneous=True),u) and eq(V.subs(inverse,simultaneous=True),v);C['inverse_definitions']+=2
 mapped=[tuple(s.simplify(t.subs({x:a,y:b},simultaneous=True)) for t in (U,V)) for a,b in vertices];us=sorted(set(a for a,b in mapped));vs=sorted(set(b for a,b in mapped));assert len(us)==len(vs)==2 and set(mapped)==set(itertools.product(us,vs));bounds={u:tuple(us),v:tuple(vs)};C['original_vertices']+=4
 vertex_section=sol.split('**Step 2**')[1].split('**Step 3**')[0];chain=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',vertex_section,re.S)[1];rows=chain.split(r'\\');assert len(rows)==8
 for pos,(vertex,point) in enumerate(zip(vertices,mapped)):
  m=re.fullmatch(r'T\^\{-1\}\((.*?)\)&=\((.*)\)',rows[2*pos].strip());assert m and all(eq(a,b) for a,b in zip(tuple2(m[1]),vertex));assert all(eq(a,b) for a,b in zip(tuple2(m[2]),point));C['substituted_vertex_components']+=2
  target=re.fullmatch(r'&=\((.*?)\)',rows[2*pos+1].strip());assert target and all(eq(a,b) for a,b in zip(tuple2(target[1]),point));C['mapped_vertices']+=1
 domain=vertex_section.split('(u,v):')[1].split(r'\}')[0].replace(r'\ ','')
 for var,part in zip((u,v),domain.split(',')):
  lo,shown,hi=part.split(r'\le');assert shown.strip()==str(var) and all(eq(a,b) for a,b in zip((math(lo),math(hi)),bounds[var]))
 path=Path(re.search(r'!\[\]\((.*?)\)',vertex_section)[1]);side=json.loads(path.with_suffix('.json').read_text());assert [math(z) for z in side['bounds']]==[us[0],us[1],vs[0],vs[1]] and side['image_sha256']==hashlib.sha256(path.read_bytes()).hexdigest();C['plot_geometry']+=1
 matrices=re.findall(r'\\begin\{vmatrix\}(.*?)\\end\{vmatrix\}',sol.split('**Step 3**')[1].split('**Step 4**')[0],re.S);assert len(matrices)==2;M=s.Matrix([[math(z) for z in row.split('&')] for row in matrices[1].split(r'\\')]);assert M==J;C['jacobian_entries']+=4
 step3=sol.split('**Step 3**')[1].split('**Step 4**')[0];printed_det=step3.rsplit('&=',1)[1].split(r'\end{aligned}')[0];assert eq(math(printed_det),det)
 sec4=sol.split('**Step 4**')[1].split('Solving these affine')[0];raw=sec4.split('$$')[1].rsplit('=',1)[1];assert eq(math(raw),1/det);C['inverse_jacobians']+=1
 metric=abs(1/det);density=s.simplify(F.subs(inverse,simultaneous=True)*metric)
 if family in ('polynomial','shifted_polynomial'):fu,fv=u,v*v
 elif family=='rational':fu,fv=u*u,1/v
 elif family=='sine':fu,fv=u,s.sin(s.pi*v)
 elif family=='exponential':fu,fv=u,s.exp(v)
 elif family=='exponential_square':fu,fv=s.Integer(1),v*s.exp(v*v)
 elif family=='cosine_square':fu,fv=u,v*s.cos(v*v)
 else:raise AssertionError(family)
 coefficient=s.simplify(density/(fu*fv));assert not coefficient.free_symbols;Au,Av=s.integrate(fu,u),s.integrate(fv,v);a,b0=bounds[u];c,d=bounds[v];Iu=Au.subs(u,b0)-Au.subs(u,a);Iv=Av.subs(v,d)-Av.subs(v,c);answer=coefficient*Iu*Iv
 chain=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol.split('**Step 5**')[1],re.S)[1];rows=chain.split(r'\\');reader=Reader(F,inverse,bounds,metric);prims=[]
 for i,row in enumerate(rows):
  body=row.split('&=',1)[1];got=reader.value(body);assert eq(got,answer),(family,body,got,answer);C['solution_rows']+=1
  if '[' in body:
   assert len(reader.primitives)==2
   for primitive,var,lo,hi,raw in reader.primitives:
    assert eq(s.diff(primitive,var),fu if var==u else fv);C['separate_primitive_derivatives']+=1
   pairs=reader.primitives[:];assert [z[1] for z in pairs]==([u,v] if family=='rational' else [v,u])
   evaluated=rows[i+2].split('&=',1)[1].replace(r'\left','').replace(r'\right','');factors=evaluated.split(r'\cdot')[1:];assert len(factors)==2
   for factor,(primitive,var,lo,hi,_) in zip(factors,pairs):
    factor=factor.strip();inside,end=group(factor,0,'(',')');assert end==len(factor);pieces=b.split_terms(inside);assert len(pieces)==2
    assert eq(math(pieces[0]),primitive.subs(var,hi)) and eq(-math(pieces[1]),primitive.subs(var,lo));C['individual_endpoint_components']+=2
 assert len(reader.primitives)==2
 if family=='cosine_square':assert '(x-y)(x+y)' in rows[0];C['factorization_stages']+=1
 f=q[':question/answer-fields'][0];values=[math(a[':answer/value']) for a in f[':answer-field/choices']];assert len(values)==5 and all(not eq(a,b) for a,b in itertools.combinations(values,2));assert [a[':answer/id'] for a,val in zip(f[':answer-field/choices'],values) if eq(val,answer)]==[f[':answer-field/correct'][1]]
 width=b0-a
 if family in ('polynomial','shifted_polynomial'):wrong=[-answer,2*answer,3*answer,coefficient*width*Iv]
 elif family=='rational':wrong=[-answer,3*answer,coefficient*width*Iv,coefficient*Iu*(d-c)]
 elif family=='sine':wrong=[-answer,s.pi*answer,s.pi*s.pi*answer,coefficient*width*Iv]
 elif family=='exponential':wrong=[-answer,2*answer,coefficient*width*Iv,coefficient*Iu*(Av.subs(v,d)+Av.subs(v,c))]
 elif family=='exponential_square':wrong=[-answer,2*answer,coefficient*width*(s.exp(d)-s.exp(c)),coefficient*width*(Av.subs(v,d)+Av.subs(v,c))]
 else:wrong=[-answer,2*answer,coefficient*Iu*(s.sin(d)-s.sin(c)),coefficient*width*Iv]
 assert all(sum(eq(val,t) for t in [answer]+wrong)==1 for val in values);C['choices']+=5;C['whole_banks']+=1;C['records']+=1
if __name__=='__main__':
 g=load(D.with_suffix('.py'),'root_integrand_gen');old={q[':question/math-academy-id']:q for q in json.load(open(R/f'sources/{K}.json'))['record'][':knowledge-point/questions']};source=dict(prompts=0,solutions=0,fields=0,values=0,refs=0,missing_refs=0,missing_ratings=0)
 for case in json.load(open(D/'source-cases.json')):
  q=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile'])['question'];o=old[case['source_id']]
  for key in (':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields'):assert (key in q)==(key in o)
  assert q[':question/problem']==o[':question/problem'];source['prompts']+=1
  if ':question/worked-solution' in o:assert q[':question/worked-solution']==o[':question/worked-solution'];source['solutions']+=1
  source['missing_ratings']+=int(':question/difficulty' not in o)
  for f,of in zip(q[':question/answer-fields'],o[':question/answer-fields']):
   assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in of[':answer-field/choices']);source['fields']+=1;source['values']+=len(of[':answer-field/choices']);assert (':answer-field/correct' in f)==(':answer-field/correct' in of)
   if ':answer-field/correct' in of:assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==of[':answer-field/correct'][':answer/value'];source['refs']+=1
   else:source['missing_refs']+=1
 records=json.load(open(R/f'qa/{K}-sampled.json'))
 for family,level in g.FAMILIES.items():records.append(g.generate(level,seed=761,template=family))
 for rec in records:check(rec)
 out=dict(status='passed',source=source,readback=C,script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest());(R/f'qa/{K}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
