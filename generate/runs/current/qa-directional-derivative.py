"""Root actual function, point/direction and individual gradient/dot stages."""
import importlib.util,json,re,hashlib,itertools,sys
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186124458;D=R.parents[2]/f'generate/scratch/{K}'
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
p=load(R/'divergence-readback.py','parent_directional');x,y,z=p.variables;i,j,k=p.basis
def math(t):return p.scalar(t.strip().rstrip('.,'))
def equal(a,b):return s.simplify(a-b)==0
def vector(t):
 t=t.strip().rstrip('.')
 def repl(m):
  a,b=m[1].replace(r'\,','').split(',');return '(('+s.latex(math(a))+r')\,i+('+s.latex(math(b))+r')\,j)'
 t=re.sub(r'⟨(.*?)⟩',repl,t);v=p.vector(t);assert v[2]==0;return s.Matrix(v[:2])
def rows(t):return [v.split(' & =',1)[1].strip().rstrip('.') for v in t.removeprefix(r'\begin{aligned}').removesuffix(r'\end{aligned}').split(chr(92)*2)]
def group(t,pos):
 assert t[pos]=='{';start=pos+1;depth=1;pos+=1
 while depth:depth+=(t[pos]=='{')-(t[pos]=='}');pos+=1
 return t[start:pos-1],pos
C={name:0 for name in ('records','actual_functions','supplied_gradients','evaluation_points','actual_directions','formal_held_operands','symbolic_gradient_components','substituted_gradient_components','evaluated_gradient_components','unit_vector_stages','direction_norm_values','dot_operands','individual_dot_factors','dot_arithmetic_values','choices','complete_method_banks','shared_prose','scale_identity_checks')}
def check(rec,original):
 q=rec['question'];prompt=q[':question/problem'];sol=q[':question/worked-solution'];family=rec['generation']['template'];point=re.search(r'at the point \$A?\((.*?)\)\$',prompt)[1];A=s.Matrix([math(v) for v in point.split(',')]);C['evaluation_points']+=2
 if family=='supplied_gradient':
  datum=re.search(r'is \$∇f\((.*?)\)=(.*?)\$',prompt);assert s.Matrix([math(v) for v in datum[1].split(',')])==A;E=vector(datum[2]);G=None;F=None;C['supplied_gradients']+=1
 else:
  F=math(re.search(r'\$f\(x,y\)=(.*?)\$',prompt)[1]);G=s.Matrix([s.diff(F,v) for v in (x,y)]);E=G.subs(dict(zip((x,y),A)));C['actual_functions']+=1
 if family in ('exp','chain_square'):
  B=s.Matrix([math(v) for v in re.search(r'\$B\((.*?)\)\.\$',prompt)[1].split(',')]);direction=B-A
 else:direction=vector(re.search(r'\$v=(.*?)\$',prompt)[1])
 N=s.sqrt(direction.dot(direction));assert N!=0;unit=direction/N;answer=s.simplify(E.dot(unit));T=[E[a]*direction[a] for a in range(2)];C['actual_directions']+=2
 blocks=re.findall(r'\$\$\s*(.*?)\s*\$\$',sol,re.S);assert len(blocks)==4 and blocks[0]==r'{f}_{u}^{′}(a,b)=∇f(a,b)\cdot u'
 normal=rows(blocks[1])
 if family in ('exp','chain_square'):
  assert len(normal)==5 and vector(normal[0])==direction and vector(normal[1])==direction
  assert normal[2]==r'\frac{\overset{\to }{AB}}{‖\overset{\to }{AB}‖}'
  for t in normal[3:]:assert vector(t)==unit;C['unit_vector_stages']+=1
 else:
  assert len(normal)==2
  for t in normal[0].split('='):assert equal(math(t),N);C['direction_norm_values']+=1
  assert vector(normal[1])==unit;C['unit_vector_stages']+=1
 if G is None:
  assert vector(blocks[2].split('=',1)[1])==E and '('+point+')' in blocks[2]
 else:
  gradient=rows(blocks[2]);_,ops=p.derivative_inputs(gradient[0]);assert len(ops)==2
  for var,(axis,arg,*_) in zip((x,y),ops):assert str(var)==axis and equal(math(arg),F);C['formal_held_operands']+=1
  if family=='chain_square':assert len(gradient)==5 and gradient[1].count(r'\cdot')==2;assert all(equal(a,b) for a,b in zip(vector(gradient[1]),G)),(family,gradient[1],G,vector(gradient[1]));gradient.pop(1)
  assert len(gradient)==(3 if family=='xy' else 4);assert all(equal(a,b) for a,b in zip(vector(gradient[1]),G)),(family,gradient[1],G,vector(gradient[1]));C['symbolic_gradient_components']+=2
  if family!='xy':assert vector(gradient[2])==E;C['substituted_gradient_components']+=2
  assert vector(gradient[-1])==E;C['evaluated_gradient_components']+=2
  assert ('∇f('+point+') & =') in blocks[2]
 dot=rows(blocks[3]);assert len(dot)==(3 if family=='exp' else 4) and dot[0]=='∇f('+point+r')\cdot u'
 operands=dot[1].split(r'\cdot');assert len(operands)==2 and vector(operands[0])==E and vector(operands[1])==unit;C['dot_operands']+=4
 if family!='exp':
  numerator,end=group(dot[2],len(r'\frac'));denominator,end=group(dot[2],end);assert end==len(dot[2]) and equal(math(denominator),N)
  # Two complete grouped component products, each checked against actual data.
  factors=re.fullmatch(r'\((.*?)\)\\cdot \((.*?)\)\+\((.*?)\)\\cdot \((.*?)\)',numerator);assert factors
  for t,v in zip(factors.groups(),(E[0],direction[0],E[1],direction[1])):assert equal(math(t),v);C['individual_dot_factors']+=1
  assert equal(math(dot[2]),answer);C['dot_arithmetic_values']+=1
 assert equal(math(dot[-1]),answer);C['dot_arithmetic_values']+=1
 field=q[':question/answer-fields'][0];choices=field[':answer-field/choices'];values=[math(a[':answer/value']) for a in choices];assert [a[':answer/id'] for a,v in zip(choices,values) if equal(v,answer)]==[field[':answer-field/correct'][1]]
 if field[':answer-field/type'].endswith('/radio'):
  assert len(values)==5 and all(not equal(a,b) for a,b in itertools.combinations(values,2))
  wanted=[answer,T[0]/N,(T[0]-T[1])/N,sum(T),sum(T)/N**2] if rec['generation']['profile']=='method' else [answer,T[0]/N,T[1]/N,T[0]-T[1],N*(T[0]-T[1])]
  assert all(sum(equal(v,w) for w in wanted)==1 for v in values);C['complete_method_banks']+=1
 else:assert len(values)==1 and '{{'+field[':answer-field/key']+'}}' in prompt
 C['choices']+=len(values)
 if original and ':question/worked-solution' in original and family!='supplied_gradient':
  prose=lambda t:re.sub(r'\s+',' ',re.sub(r'\$\$.*?\$\$|\$.*?\$','',t,flags=re.S)).strip();assert prose(sol)==prose(original[':question/worked-solution']);C['shared_prose']+=1
 C['records']+=1
if __name__=='__main__':
 g=load(D.with_suffix('.py'),'parent_directional_generator');frozen=json.load(open(R/f'sources/{K}.json'));assert json.load(open(D/'source.json'))==frozen;originals={str(q[':db/id']):q for q in frozen['record'][':knowledge-point/questions']};S=dict(prompts=0,solutions=0,fields=0,values=0,refs=0,missing_refs=0,unrated=0)
 for case in json.load(open(D/'source-cases.json')):
  q=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile'])['question'];o=originals[str(case['source_id'])];assert q[':question/problem']==o[':question/problem'];assert (':question/difficulty' in q)==(':question/difficulty' in o);assert (':question/worked-solution' in q)==(':question/worked-solution' in o);S['prompts']+=1;S['unrated']+=(':question/difficulty' not in o)
  if ':question/worked-solution' in o:assert q[':question/worked-solution']==o[':question/worked-solution'];S['solutions']+=1
  for f,of in zip(q[':question/answer-fields'],o[':question/answer-fields']):
   assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in of[':answer-field/choices']);S['fields']+=1;S['values']+=len(of[':answer-field/choices']);assert (':answer-field/correct' in f)==(':answer-field/correct' in of)
   if ':answer-field/correct' in of:assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==of[':answer-field/correct'][':answer/value'];S['refs']+=1
   else:S['missing_refs']+=1
 records=json.load(open(R/f'qa/{K}-sampled.json'))
 for family,level in g.FAMILIES.items():records.extend(g.generate(level,seed=seed,template=family) for seed in (631,917))
 for rec in records:check(rec,originals[rec['generation']['source_id']])
 # Explicit equivalent positive directions must not create assessed tasks.
 for family,level in g.FAMILIES.items():
  for a in range(1,5):
   params=dict(a=a,b=1,c=1,d=1,x0=1,y0=0 if family=='exp' else 1,dx=1,dy=2)
   try:one=g.generate(level,template=family,parameters=params);other=g.generate(level,template=family,parameters=params|dict(dx=2,dy=4))
   except ValueError:continue
   assert one['generation']['mathematical_fingerprint']==other['generation']['mathematical_fingerprint'];C['scale_identity_checks']+=1;break
 out=dict(status='passed',source=S,readback=C,script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest());(R/f'qa/{K}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
