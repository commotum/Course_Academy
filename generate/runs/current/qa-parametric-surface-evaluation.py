"""Root actual surface integral, all displayed stages/bounds and full banks."""
import importlib.util,json,re,sys,hashlib,itertools
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186172131;D=R.parents[2]/f'generate/scratch/{K}'
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
b=load(R/'surface-calculus-reader.py','surface_eval_reader');p=b.p;x,y,z,u,v=b.x,b.y,b.z,b.u,b.v;math,eq=b.math,b.eq
def vector(raw):return s.Matrix([math(a) for a in raw.strip().rstrip('.,')[1:-1].split(r',\,')])
def shown_bounds(text,variable):
 # Bounds are complete components, including nested fraction groups.
 suffix='\\le '+variable+'\\le ';index=text.index(suffix);prefix=text[:index];lo=prefix.rsplit('$',1)[-1].rsplit(',',1)[-1].split(':')[-1].replace(r'\,','').strip()
 if lo.startswith(r'\{(u,v)'):lo=lo.split(':')[-1]
 pos=index+len(suffix);depth=0;end=pos
 while end<len(text):
  ch=text[end]
  if depth==0 and ch in '$,':break
  if depth==0 and text[end:].startswith(r'\}'):break
  depth+=(ch=='{')-(ch=='}');end+=1
 return math(lo),math(text[pos:end])
C={key:0 for key in ('records','actual_coordinates','actual_integrands','actual_domains','hint_metrics','formal_partial_operands','derivative_components','cross_input_matrices','cofactor_minors','metric_stages','pullback_stages','complete_solution_rows','primitive_bounds','individual_primitive_derivatives','individual_endpoint_components','choices','whole_banks','operative_source_sequences')}
def check(rec):
 q=rec['question'];prompt=q[':question/problem'];sol=q[':question/worked-solution'];family=rec['generation']['template'];level=q[':question/difficulty'].rsplit('/',1)[1];charge=family=='q-167649'
 if charge:
  raw=re.search(r'r\(x,\\theta\)=(⟨.*?)\$',prompt)[1];coords=s.Matrix([math(a) for a in raw[1:-1].split(',')]);F=math(re.search(r'd\(x,y,z\)=(.*?)\$',prompt)[1]);aa,bb=x,v;bounds={u:shown_bounds(prompt,'x'),v:(s.Integer(0),2*s.pi)}
 else:
  m=re.search(r'r\(u,v\)=(⟨[^⟩]+⟩)',prompt)
  if m:coords=vector(m[1])
  else:coords=s.Matrix([math(re.search(r'\b'+axis+r'=(.*?)(?=,\\,|\n)',prompt)[1]) for axis in 'xyz'])
  F=math(re.search(r'(?:\{∬\}_\{S\}|\\iint_S)(.*?)\\,\\text\{d\}S',prompt,re.S)[1]);aa,bb=u,v;bounds={u:shown_bounds(prompt,'u'),v:shown_bounds(prompt,'v')}
 ru,rv=coords.diff(aa),coords.diff(bb);cross=ru.cross(rv);metric=s.sqrt(s.trigsimp(cross.dot(cross)));pull=s.trigsimp(s.simplify(F.subs(dict(zip((x,y,z),coords)),simultaneous=True)))
 if charge:pull=pull.subs(x,u);metric=metric.subs(x,u)
 density=s.simplify(s.trigsimp(pull*metric));answer=s.integrate(density,(u,*bounds[u]),(v,*bounds[v]));C['actual_coordinates']+=3;C['actual_integrands']+=1;C['actual_domains']+=1
 blocks=re.findall(r'\$\$\s*(.*?)\s*\$\$',sol,re.S)
 if level!='hard':
  raw=prompt.split('‖')[-1].split('=')[1].split('$')[0].rstrip('.');shown=math(raw);shown=shown.subs(x,u) if charge else shown;assert eq(shown,metric),(family,shown,metric);C['hint_metrics']+=1
 else:
  derivative=next(block for block in blocks if '{r}_{u}^{′} & =' in block)
  operated=re.findall(r'\\frac\{∂\}\{∂([uv])\}\((.*?)\)(?=,\\,|⟩)',derivative);assert len(operated)==6
  for index,((axis,raw),coordinate) in enumerate(zip(operated,list(coords)*2)):assert axis==('u' if index<3 else 'v') and eq(math(raw),coordinate);C['formal_partial_operands']+=1
  evaluated=[raw for raw in re.findall(r' & =(⟨[^⟩]+⟩)',derivative) if '∂' not in raw];assert len(evaluated)==2 and vector(evaluated[0])==ru and vector(evaluated[1])==rv;C['derivative_components']+=6
  crossblock=next(block for block in blocks if '{r}_{u}^{′}\\times {r}_{v}^{′} & =' in block);arrays=re.findall(r'\|\\begin\{aligned\}(.*?)\\end\{aligned\}\|',crossblock,re.S);assert len(arrays)==4;matrices=[s.Matrix([[math(a) for a in row.split('&')] for row in raw.split(r'\\')]) for raw in arrays]
  assert list(matrices[0][0,:])==[p.i,p.j,p.k] and matrices[0][1:,:]==s.Matrix([list(ru),list(rv)]);C['cross_input_matrices']+=1
  for M,(i,j) in zip(matrices[1:],((1,2),(0,2),(0,1))):assert M==s.Matrix([[ru[i],ru[j]],[rv[i],rv[j]]]);C['cofactor_minors']+=1
  assert vector(re.findall(r' & =(⟨[^⟩]+⟩)',crossblock)[-1])==cross
  normblock=next(block for block in blocks if '‖' in block and ' & =' in block)
  for raw in normblock.split(' & =')[2:]:assert eq(math(raw.split(r'\\')[0].split(r'\end{aligned}')[0]),metric);C['metric_stages']+=1
 if family=='canonical_hint':
  pullblock=next(block for block in blocks if block.startswith('f(r(u,v))='));parts=pullblock.split('=')[1:];assert all(eq(math(raw),pull) for raw in parts);C['pullback_stages']+=len(parts)
 else:
  pb=next(block for block in blocks if re.match(r'\\begin\{aligned\}[fd]\(r',block));parts=pb.split(' & =')[1:]
  if charge:
   for raw in parts[1:]:assert eq(math(raw.split(r'\\')[0].split(r'\end{aligned}')[0]).subs(x,u),pull);C['pullback_stages']+=1
  else:
   raw,restriction=parts[0].split(r'\,{|}_{',1);assert eq(math(raw),F)
   restriction=restriction.split(r'\\')[0].strip().removesuffix('}');assert all(eq(math(part.split('=')[1]),coordinate) for part,coordinate in zip(restriction.split(r'\,'),coords))
   for raw in parts[1:]:assert eq(math(raw.split(r'\\')[0].split(r'\end{aligned}')[0]),pull);C['pullback_stages']+=1
 if family!='canonical_hint':
  original=json.loads((R/f'sources/{K}.json').read_text())['record'][':knowledge-point/questions']
  original=next(o for o in original if o[':question/math-academy-id']==family)[':question/worked-solution']
  prose=lambda text:re.sub(r'\s+',' ',re.sub(r'\$\$.*?\$\$|\$.*?\$','[MATH]',text,flags=re.S)).strip()
  assert prose(sol)==prose(original)
  originalchain=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',original.rsplit('$$',2)[1],re.S)[1]
  currentchain=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',blocks[-1],re.S)[1]
  added=0 if charge else 1 if family in ('q-160834','q-160835','q-161212','q-161242','q-161185') else 2
  assert len(currentchain.split(chr(92)*2))==len(originalchain.split(chr(92)*2))+added
  if family=='q-161185':assert currentchain.count(r'{\int }')==originalchain.count(r'{\int }')
  if charge:assert '{cos}^{2}' in sol and '{sin}^{2}' in sol and r'\sqrt{16' in sol
  C['operative_source_sequences']+=1
 reader=b.Reader(pull,metric,bounds,charge=charge);final=blocks[-1];body=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',final,re.S)[1];rows=body.split(r'\\');primitives=[]
 for rowindex,row in enumerate(rows):
  rhs=re.split(r'&\s*=',row,maxsplit=1)[1];value=reader.value(rhs);assert eq(value,answer),(family,rhs,value,answer);C['complete_solution_rows']+=1
  if reader.primitives and len(reader.primitives)>len(primitives):
   new=reader.primitives[len(primitives):];primitives.extend(new);C['primitive_bounds']+=len(new)
   # Individually compare each primitive with the density/factor from the
   # actual surface, rather than multiplying their derivatives together.
   for primitive,var,lo,hi,raw in new:
    derivative=s.diff(primitive,var)
    if family in ('q-160835','q-161212','q-161242'):expected=2*var
    elif family=='q-161185':expected=var
    elif family=='q-160834':expected=pull if var==u else 1
    elif family=='canonical_hint':expected=pull if var==v else 1
    elif charge:expected=density if var==u else 1
    else:
     coefficient=math(rhs.split(r'{\int }',1)[0].split('[',1)[0].strip().removesuffix(r'{').strip()) if False else None
     # Source constant factor is read from the actual final integral stage.
     first_integral=next(r for r in rows if r'{\int }' in r);prefix=re.split(r'&\s*=',first_integral,maxsplit=1)[1].split(r'{\int }',1)[0];factor=math(prefix.rstrip('(').rstrip(r'\cdot ').strip());normalized=s.simplify(density/factor)
     expected=normalized if var==u else s.integrate(normalized,(u,*bounds[u]))
    assert eq(derivative,expected) and eq(primitive,s.integrate(expected,var)),(family,var,primitive,derivative,expected);C['individual_primitive_derivatives']+=1
  cleaned=reader.clean(rhs)
  details=list(re.finditer(r'\[\((.*?)\)-\((.*?)\)\]',cleaned))
  for detailindex,detail in enumerate(details):
   assert primitives;primitive,var,lo,hi,_=primitives[detailindex] if len(details)==2 else primitives[-1]
   terms=sorted(s.Poly(primitive,var).terms(),key=lambda item:item[0][0])
   for raw,end in zip(detail.groups(),(hi,lo)):
    actual=[math(part) for part in b.split_terms(raw)];expected=[coefficient*end**powers[0] for powers,coefficient in terms]
    assert len(actual)==len(expected) and all(eq(a,e) for a,e in zip(actual,expected)),(family,raw,actual,expected);C['individual_endpoint_components']+=len(actual)
  if '[' in rhs and ']_' in reader.clean(rhs) and (charge or family=='canonical_hint'):
   nextrow=reader.clean(re.split(r'&\s*=',rows[rowindex+1],maxsplit=1)[1]);evaluations=re.findall(r'\(([^()]*?)-([^()]*)\)',nextrow);assert len(evaluations)==2
   for (high,low),(primitive,var,lo,hi,_) in zip(evaluations,primitives):assert eq(math(high),primitive.subs(var,hi)) and eq(math(low),primitive.subs(var,lo));C['individual_endpoint_components']+=2
 assert len(primitives)==2
 f=q[':question/answer-fields'][0];values=[math(a[':answer/value']) for a in f[':answer-field/choices']];assert all(not eq(a,b) for a,b in itertools.combinations(values,2));assert [a[':answer/id'] for a,val in zip(f[':answer-field/choices'],values) if eq(val,answer)]==[f[':answer-field/correct'][1]]
 if len(values)==5:
  integral=lambda expr:s.integrate(expr,(u,*bounds[u]),(v,*bounds[v]));wrong=[integral(pull),integral(pull*metric**2)]
  if family in ('q-160835','q-161212','q-161242','q-161185'):wrong += [integral(u*v*metric),integral(4*pull*metric)]
  elif family=='q-161181':wrong=[integral(pull),integral((u-v)*metric),0,-answer]
  elif family=='q-161209':wrong += [integral((u*u+v*v)*metric),3*answer]
  else:
   terms=s.Add.make_args(s.expand(pull))
   if family in ('q-161127','q-161182','q-161179'):nodiv=sum(coef*(powers[0]+1)*(powers[1]+1)*u**powers[0]*v**powers[1] for powers,coef in s.Poly(pull,u,v).terms());wrong += [integral((pull-terms[0])*metric),integral(nodiv*metric)]
   else:wrong += [integral((pull-terms[0])*metric),integral((pull-terms[-1])*metric)]
  assert all(sum(eq(val,t) for t in [answer]+wrong)==1 for val in values);C['whole_banks']+=1
 else:assert len(values)==1 and '{{'+f[':answer-field/key']+'}}' in prompt
 C['choices']+=len(values);C['records']+=1
if __name__=='__main__':
 g=load(D.with_suffix('.py'),'root_surface_eval');source={q[':question/math-academy-id']:q for q in json.load(open(R/f'sources/{K}.json'))['record'][':knowledge-point/questions']};counts=dict(prompts=0,solutions=0,fields=0,values=0,refs=0)
 for case in json.load(open(D/'source-cases.json')):
  level=source[case['source_id']][':question/difficulty'][':db/ident'].rsplit('/',1)[1];q=g.generate(level,template=case['template'],parameters=case['parameters'],profile=case['bank_profile'])['question'];o=source[case['source_id']];assert q[':question/problem']==o[':question/problem'] and q[':question/worked-solution']==o[':question/worked-solution'];counts['prompts']+=1;counts['solutions']+=1
  for f,of in zip(q[':question/answer-fields'],o[':question/answer-fields']):assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in of[':answer-field/choices']);assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==of[':answer-field/correct'][':answer/value'];counts['fields']+=1;counts['values']+=len(of[':answer-field/choices']);counts['refs']+=1
 records=json.load(open(R/f'qa/{K}-sampled.json'))
 for family,level in g.LEVEL.items():records.append(g.generate(level,template=family,seed=819))
 for rec in records:check(rec)
 out=dict(status='passed',source=counts,readback=C,script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest());(R/f'qa/{K}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
