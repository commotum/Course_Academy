"""Root actual gradients and criterion-aware whole direction banks."""
import importlib.util,json,re,hashlib,itertools,sys
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186124459;D=R.parents[2]/f'generate/scratch/{K}'
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
p=load(R/'divergence-readback.py','parent_max_direction');x,y,z=p.variables;i,j,k=p.basis
def math(t):return p.scalar(t.strip().rstrip('.,').replace(r'\text{ }',r'\,'))
def eq(a,b):return s.simplify(s.trigsimp(a-b))==0
def veq(a,b):return len(a)==len(b) and all(eq(c,d) for c,d in zip(a,b))
def vector(t,n):
 t=t.strip().rstrip('.')
 def repl(m):
  vals=m[1].replace(r'\,','').split(',');return '('+'+'.join('('+s.latex(math(v))+r')\,'+basis for v,basis in zip(vals,'ijk'))+')'
 t=re.sub(r'⟨(.*?)⟩',repl,t).replace(r'\text{ }',r'\,');out=p.vector(t);assert n==3 or out[2]==0;return s.Matrix(out[:n])
def rows(text):return [m[1].strip() for m in re.finditer(r'&\s*=(.*?)(?=\\\\|\\end\{aligned\}|$)',text,re.S)]
def group(text,pos):
 assert text[pos]=='{';start=pos+1;depth=1;pos+=1
 while depth:depth+=(text[pos]=='{')-(text[pos]=='}');pos+=1
 return text[start:pos-1],pos
def parallel(a,b):
 assert any(v!=0 for v in b);axis=next(j for j,v in enumerate(b) if v!=0);ratio=s.simplify(a[axis]/b[axis]);return ratio.is_positive is True and veq(a,ratio*b)
C={n:0 for n in ('records','actual_functions','actual_points','formal_partial_inputs','generic_partial_components','chain_partial_components','substituted_components','intermediate_angle_components','evaluated_components','normalization_components','norm_square_components','concluding_components','choices','criterion_pair_checks','whole_method_banks','shared_source_masks','magnitude_identity_checks')}
def check(rec,old):
 q=rec['question'];prompt=q[':question/problem'];sol=q[':question/worked-solution'];family=rec['generation']['template'];function=re.search(r'\$([fg])\((.*?)\)\s*=(.*?)\$',prompt);name=function[1];axes=tuple(dict(zip('xyz',(x,y,z)))[v.strip()] for v in function[2].split(','));n=len(axes);F=math(function[3]);point=re.search(r'at the point \$\((.*?)\)',prompt);coords=[math(v) for v in point[1].split(',')];assert len(coords)==n;subs=dict(zip(axes,coords));gradient=s.Matrix([s.diff(F,v) for v in axes]);G=gradient.subs(subs).applyfunc(s.simplify);sign=-1 if 'decrease most rapidly' in prompt else 1;unit='unit direction' in prompt;N=s.sqrt(G.dot(G));assert N!=0;target=sign*G/N if unit else sign*G;C['actual_functions']+=1;C['actual_points']+=n
 B=re.findall(r'\$\$\s*(.*?)\s*\$\$',sol,re.S);assert len(B)==(2 if unit else 1);rr=rows(B[0]);_,ops=p.derivative_inputs(rr[0]);assert len(ops)==n
 for axis,(v,arg,*_) in zip(axes,ops):assert str(axis)==v and eq(math(arg),F);C['formal_partial_inputs']+=1
 if unit:
  assert len(rr)==5 and rr[1].count(r'\cdot')==3;assert veq(vector(rr[1],n),gradient);C['chain_partial_components']+=n;rr.pop(1)
 assert len(rr)==(5 if family in ('linear_sin','mixed_sin') else 4)
 assert veq(vector(rr[1],n),gradient);C['generic_partial_components']+=n
 assert veq(vector(rr[2],n),G);C['substituted_components']+=n
 if family in ('linear_sin','mixed_sin'):assert veq(vector(rr[3],n),G);C['intermediate_angle_components']+=n
 assert veq(vector(rr[-1],n),G);C['evaluated_components']+=n
 # The evaluation label must describe the actual prompt point, including the
 # minimally repaired exponential source label.
 label='∇'+name+'('+','.join(str(c) for c in coords)+')';assert label+' &' in B[0]
 if unit:
  norms=rows(B[1]);assert len(norms)==3 and label in norms[0];assert ('-' in norms[0])==(sign<0)
  numerator,pos=group(norms[1],len(r'\frac'));den,pos=group(norms[1],pos);assert math(numerator)==sign and eq(math(den),N);assert den.startswith(r'\sqrt{');squares,end=group(den,len(r'\sqrt'));assert end==len(den)
  parts=squares.split('+');assert len(parts)==n
  for raw,val in zip(parts,G):assert eq(math(raw),val*val);C['norm_square_components']+=1
  assert veq(sign*vector(norms[1][pos:],n)/N,target) and veq(vector(norms[-1],n),target);C['normalization_components']+=2*n
 conclusion=re.search(r'(?:unit )?direction of \$(.*?)\.\$',sol)[1];assert veq(vector(conclusion,n),target);C['concluding_components']+=n
 assert ('function decreases most rapidly' in sol)==(sign<0)
 choices=q[':question/answer-fields'][0][':answer-field/choices'];values=[vector(a[':answer/value'],n) for a in choices];assert len(values)==5
 valid=[a[':answer/id'] for a,val in zip(choices,values) if parallel(val,target) and (not unit or eq(val.dot(val),1))];assert valid==[q[':question/answer-fields'][0][':answer-field/correct'][1]]
 for a,b in itertools.combinations(values,2):assert not (veq(a,b) if unit else parallel(a,b));C['criterion_pair_checks']+=1
 u,v=coords[:2];w=coords[2] if n==3 else 1
 if family=='cosxy':
  a=F.coeff(s.cos(x));b=F.coeff(x*x*y);errors=[s.Matrix([2*b*u*v,b*u*u]),s.Matrix([-a*s.sin(u),b*u*u]),s.Matrix([G[0],2*b*u*v])]
 elif family=='quadratic':
  a,b,c=F.coeff(x*x),F.coeff(x*y),F.coeff(y*y);errors=[s.Matrix([2*a*u,G[1]]),s.Matrix([G[0],2*c*v]),s.Matrix([a*u+b*v,b*u+c*v])]
 elif family=='linear_sin':
  a=F.coeff(y*y);arg=next(iter(F.atoms(s.sin))).args[0];b,c=s.diff(arg,x)/s.pi,s.diff(arg,z)/s.pi;co=s.cos(arg.subs(subs));errors=[s.Matrix([s.pi*co,G[1],G[2]]),s.Matrix([G[0],a*v,G[2]]),s.Matrix([G[0],G[1],co])]
 elif family=='mixed_sin':
  arg=next(iter(F.atoms(s.sin))).args[0];a=s.diff(arg,x)/s.pi;b=F.coeff(z*z*x);co=s.cos(arg.subs(subs));errors=[s.Matrix([b*w*w,co,G[2]]),s.Matrix([a*s.pi*co+b*w*w,co,b*u*w]),s.Matrix([co+b*w*w,co,G[2]])]
 elif family=='exp':
  a,b,c=F.coeff(x*s.log(y)),F.coeff(y*s.exp(x)),-F.coeff(x*y);errors=[s.Matrix([a*s.log(v)+b*v*s.exp(u)+c*v,G[1]]),s.Matrix([G[0],b*s.exp(u)-c*u]),s.Matrix([a*s.log(v)+b*v*s.exp(-u)-c*v,a*u/v+b*s.exp(-u)-c*u])]
 elif family=='trig_product':
  a,b=F.coeff(x*x*s.sin(y)),-F.coeff(y*s.cos(x))
  if u==0:errors=[s.Matrix([b*v*s.sin(u)+2*a*s.sin(v),G[1]]),s.Matrix([G[1],G[0]]),s.Matrix([-b*v*s.cos(u)+2*a*u*s.sin(v),G[1]])]
  else:errors=[s.Matrix([2*a*u*s.sin(v),G[1]]),s.Matrix([G[0],a*u*u*s.cos(v)+b*s.cos(u)]),s.Matrix([G[1],G[0]])]
 else:
  assert unit and all(c>0 for c in coords);h=s.Matrix([1/u,G[1],G[2]]);errors=[G,G/(N*N),h/s.sqrt(h.dot(h))]
 wanted=[target,-target,*[sign*e for e in errors]];assert all(sum(veq(value,e) for e in wanted)==1 for value in values);C['choices']+=5;C['whole_method_banks']+=1
 if old and ':question/worked-solution' in old:
  assert len(rows(re.findall(r'\$\$\s*(.*?)\s*\$\$',old[':question/worked-solution'],re.S)[0]))==len(rows(B[0]))
  original=old[':question/worked-solution']
  if sign<0:original=original.replace('increases most rapidly in the direction of its gradient at that point.','decreases most rapidly in the direction opposite to that of its gradient.').replace('Therefore, the function increases most rapidly','Therefore, the function decreases most rapidly')
  prose=lambda text:re.sub(r'\s+',' ',re.sub(r'\$\$.*?\$\$|\$.*?\$','',text,flags=re.S)).strip()
  assert prose(sol)==prose(original);C['shared_source_masks']+=1
 C['records']+=1
if __name__=='__main__':
 g=load(D.with_suffix('.py'),'parent_max_direction_generator');frozen=json.load(open(R/f'sources/{K}.json'));assert json.load(open(D/'source.json'))==frozen;originals={q[':db/id']:q for q in frozen['record'][':knowledge-point/questions']};S=dict(prompts=0,solutions=0,fields=0,values=0,refs=0,missing_refs=0,unrated=0)
 for case in json.load(open(D/'source-cases.json')):
  o=originals[case['source_id']];q=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile'])['question'];assert q[':question/problem']==o[':question/problem'];assert (':question/worked-solution' in q)==(':question/worked-solution' in o) and (':question/difficulty' in q)==(':question/difficulty' in o);S['prompts']+=1;S['unrated']+=(':question/difficulty' not in o)
  if ':question/worked-solution' in o:assert q[':question/worked-solution']==o[':question/worked-solution'];S['solutions']+=1
  for f,of in zip(q[':question/answer-fields'],o[':question/answer-fields']):
   assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in of[':answer-field/choices']);S['fields']+=1;S['values']+=len(of[':answer-field/choices']);assert (':answer-field/correct' in f)==(':answer-field/correct' in of)
   if ':answer-field/correct' in of:assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==of[':answer-field/correct'][':answer/value'];S['refs']+=1
   else:S['missing_refs']+=1
 records=json.load(open(R/f'qa/{K}-sampled.json'))
 for family,(level,_,params) in g.FAMILIES.items():records.extend(g.generate(level,seed=seed,template=family) for seed in (631,917))
 records.append(g.generate_easy(template='trig_product',parameters=dict(a=3,b=1,u=0,v=1),profile='axis_method'))
 for rec in records:check(rec,originals.get(g.FAMILIES[rec['generation']['template']][1]))
 for params in (dict(a=2,b=1,c=1,u=3,v=3,w=3),):
  a=g.generate_hard(template='log_unit',parameters=params);b=g.generate_hard(template='log_unit',parameters=params|dict(a=4,b=2,c=2));assert a['generation']['mathematical_fingerprint']==b['generation']['mathematical_fingerprint'];C['magnitude_identity_checks']+=1
 out=dict(status='passed',source=S,readback=C,script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest());(R/f'qa/{K}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
