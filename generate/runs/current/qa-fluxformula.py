"""Root reconstructs every completed displayed Cartesian flux formula."""
import importlib.util,json,re
from pathlib import Path
import sympy as s
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,convert_xor
R=Path(__file__).resolve().parent;K=17592186198392;D=R.parents[2]/f'generate/scratch/{K}'
x,y,z,P,Q,W=s.symbols('x y z P Q R',real=True);XYZ=(x,y,z);LOC={str(t):t for t in (*XYZ,P,Q,W)};LOC.update({f:s.Function(f) for f in 'ghkfsw'})
def module(name,p):
 q=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(q);q.loader.exec_module(m);return m
g=module('parent_fluxformula',D.with_suffix('.py'))
BOX=r'\bbox[3pt,border:1pt solid black]{\phantom{A}}'
LOC.update({'D'+f+str(v):s.Symbol('D'+f+str(v),real=True) for f in 'ghkfsw' for v in XYZ})
def math(text):
 text=text.strip().rstrip('.,').replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\cdot','*').replace(r'\end{aligned}','')
 for f in 'ghkfswPQR':
  for v in (*XYZ,P,Q,W):
   token='D'+f+str(v);LOC[token]=s.Symbol(token,real=True)
   text=text.replace(r'\frac{∂'+f+'}{∂'+str(v)+'}','('+token+')')
 text=text.replace('{','(').replace('}',')').replace('⁡','').rstrip().rstrip('\\')
 try:return parse_expr(text,local_dict=LOC,transformations=standard_transformations+(implicit_multiplication_application,convert_xor))
 except Exception as error:raise ValueError(('parent parse',text)) from error
def parts(value):
 text=re.sub(r'\\text\{[^}]*\}',' ',value).replace('$','').replace(r'\,',' ')
 return [v.strip() for v in re.split(r'\band\b|,',text) if v.strip()]
def vector_parts(raw):
 raw=raw.replace(r'\,','');out=[];start=0;depth=0
 for i,t in enumerate(raw):
  if t in '({':depth+=1
  elif t in ')}':depth-=1
  elif t==',' and depth==0:out.append(raw[start:i]);start=i+1
 out.append(raw[start:]);return [v for v in out if v.strip()]
def inner(prompt):return re.search(r'\{∬\}_\{D\}\((.*?)\)\\,\\text\{d\}A',prompt,re.S).group(1)
def completed(prompt,value):
 text=inner(prompt).replace(r'\boxed{}',BOX);values=parts(value)
 assert text.count(BOX)==len(values),(text,values)
 for v in values:text=text.replace(BOX,v,1)
 return math(text.rstrip('\\'))
def expected(prompt):
 m=re.search(r'given by \$([xyz])=(.*?)\$ for',prompt);assert m,prompt
 axis,graphtext=m.groups();u,v={'x':(y,z),'y':(x,z),'z':(x,y)}[axis]
 fm=re.fullmatch(r'([ghkfsw])\(([xyz]),([xyz])\)',graphtext)
 if fm:
  f=fm[1];graph=LOC[f](u,v);du=LOC['D'+f+str(u)];dv=LOC['D'+f+str(v)]
 else:graph=math(graphtext);du=s.diff(graph,u);dv=s.diff(graph,v)
 # Independent graph normals with selected positive dependent-axis component.
 normal={'x':s.Matrix([1,-du,-dv]),'y':s.Matrix([-du,1,-dv]),'z':s.Matrix([-du,-dv,1])}[axis]
 flux=s.expand(s.Matrix([P,Q,W]).dot(normal))
 return axis,graph,du,dv,normal,flux
counts={'source_banks':0,'source_values':0,'source_correct_designations':0,'normal_formula_instances':0,'printed_vector_rows':0}
def check(r):
 q=r['question'];prompt=q[':question/problem'];axis,graph,du,dv,n,flux=expected(prompt);field=q[':question/answer-fields'][0]
 truth=[]
 for ans in field[':answer-field/choices']:
  if s.simplify(completed(prompt,ans[':answer/value'])-flux)==0:truth.append(ans[':answer/id'])
 assert truth==[field[':answer-field/correct'][1]],(prompt,truth,flux)
 # All numerical/symbolic tangent and cross-product vector rows must belong
 # to the printed graph's actual geometry, including pre-reversal normals.
 u,v={'x':(y,z),'y':(x,z),'z':(x,y)}[axis];rr=s.Matrix([graph if str(t)==axis else t for t in XYZ]);ru=rr.diff(u);rv=rr.diff(v)
 if graph.has(s.Function):
  ru=ru.xreplace({s.diff(graph,u):du,s.diff(graph,v):dv});rv=rv.xreplace({s.diff(graph,u):du,s.diff(graph,v):dv})
 allowed=[rr,ru,rv,ru.cross(rv),n,s.Matrix([P,Q,W])]
 for raw in re.findall('⟨([^⟨⟩]+)⟩',q[':question/worked-solution']):
  vec=s.Matrix([math(e) for e in vector_parts(raw)]);assert len(vec)==3
  assert any(all(s.simplify(a-b)==0 for a,b in zip(vec,w)) for w in allowed),(raw,allowed);counts['printed_vector_rows']+=1
 counts['normal_formula_instances']+=1
raw=json.loads((R/'sources'/f'{K}.json').read_text())['record'];qs={q[':question/math-academy-id']:q for q in raw[':knowledge-point/questions']}
for c in json.loads((D/'source-cases.json').read_text()):
 name=c['template'];old=qs[name];r=g.generate(c['level'],template=name,parameters=c['parameters'],profile=c['bank_profile']);of=old[':question/answer-fields'][0];f=r['question'][':question/answer-fields'][0]
 assert sorted(a[':answer/value'] for a in of[':answer-field/choices'])==sorted(a[':answer/value'] for a in f[':answer-field/choices'])
 selected=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert selected==of[':answer-field/correct'][':answer/value']
 counts['source_banks']+=1;counts['source_values']+=len(f[':answer-field/choices']);counts['source_correct_designations']+=1
 normal=g.generate(c['level'],template=name,parameters=c['parameters']);check(normal)
for level in ('easy','moderate','hard'):
 for seed in range(40):check(g.generate(level,seed))
normals=set()
for coefficient in (-3,-2,2,3):
 for a in range(-2,3):
  for b in range(-2,3):
   params=dict(c=coefficient,m=1,n=1,a=a,b=b,h=0)
   r=g.generate('moderate',template='q-161456',parameters=params);check(r)
   normals.add(tuple(s.expand(v) for v in expected(r['question'][':question/problem'])[4]))
assert len(normals)==100
counts['distinct_shifted_bilinear_normals']=len(normals)
for h in (-2,2):
 r=g.generate('moderate',template='q-161456',parameters=dict(c=-3,m=1,n=1,a=-2,b=2,h=h));check(r)
for name in g.TEMPLATES:
 if g.DATA[name]['kind']=='symbolic':
  for function in ('g','h','k','f','s','w'):check(g.generate(g.TEMPLATES[name],template=name,parameters={'function':function}))
counts['database_writes']=0;(R/'qa'/f'{K}-independent.json').write_text(json.dumps(counts,indent=2)+'\n');print(counts)
