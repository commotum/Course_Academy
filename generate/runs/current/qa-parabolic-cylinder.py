"""Root reads actual cylinder equations, parameter roles, banks and graph stages."""
import hashlib,importlib.util,itertools,json,re,sys
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent;K=17592186175972;D=R.parents[2]/f'generate/scratch/{K}'
def mod(n,p):
 sp=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(sp);sys.modules[n]=m;sp.loader.exec_module(m);return m
P=mod('root_parabolic_scalar',R/'ode-scalar-parser.py');G=mod('root_parabolic_gen',D.with_suffix('.py'));F=mod('root_parabolic_source',R/'root-source-fidelity.py');O,Fid=F.check(G,K,D)
axes=[P.x,P.y,P.z]
def scalar(t):return P.scalar(t.strip().rstrip('.,').replace(r'\,',''))
def vec(t):return tuple(scalar(v) for v in t.replace(r'\,','').split(','))
def same(a,b):return s.expand(a-b)==0
C=dict(records=0,choice_values=0,bank_pairs=0,geometry_substitutions=0,direct_coordinate_constraints=0,full_graph_vectors=0,conclusions=0,normalization_sides=0,source_prose_masks=0,covering_scaled_free_distractors=0)
rows=json.load(open(R/f'qa/{K}-sampled.json'))
# Every named axis can occupy the requested dependent/free role, with fixed coefficient.
for base,dep in itertools.permutations('xyz',2):
 for profile in ('q-164443','q-164440'):
  free=next(z for z in 'xyz' if z not in (base,dep));role='dependent' if profile=='q-164443' else 'free'
  p=dict(base=base,dependent=dep,a=3,target=dep if role=='dependent' else free,argument_order='base_first',relation_order='dependent_first')
  rows.append(G.generate('easy',profile=profile,parameters=p))
for rec in rows:
 q,m=rec['question'],rec['generation'];prompt=q[':question/problem'];sol=q[':question/worked-solution']
 match=re.search(r'([fgh])\(([^)]+)\)\s*=\s*⟨([^⟩]+)⟩',prompt);assert match;fn,args,body=match.groups();args=[z.strip() for z in args.split(',')];parts=body.replace(r'\,','').split(',');assert len(parts)==3
 target=next(i for i,z in enumerate(parts) if '{{selection}}' in z);assert sum('{{selection}}' in z for z in parts)==1
 ords=('first','second','third');assert 'What is the '+ords[target]+' component' in prompt
 rel=re.search(r'coordinates as \$([^$]+)\$',prompt)[1];left,right=map(scalar,rel.split('='));eq=s.expand(left-right);poly=s.Poly(eq,*axes)
 dep=next(a for a in axes if poly.coeff_monomial(a));base=next(a for a in axes if poly.coeff_monomial(a*a));free=next(a for a in axes if a not in (dep,base));c=-poly.coeff_monomial(base*base)/poly.coeff_monomial(dep)
 assert c>0 and same(eq,poly.coeff_monomial(dep)*(dep-c*base**2));assert set(args)=={str(base),str(free)}
 expected=tuple(c*base**2 if a==dep else a for a in axes);want=expected[target]
 f=q[':question/answer-fields'][0];values=[scalar(a[':answer/value']) for a in f[':answer-field/choices']];assert len(values)==5
 assert [a[':answer/id'] for a,v in zip(f[':answer-field/choices'],values) if same(v,want)]==[f[':answer-field/correct'][1]]
 for i,v in enumerate(values):
  for w in values[i+1:]:assert not same(v,w);C['bank_pairs']+=1
  filled=tuple(v if j==target else scalar(z) for j,z in enumerate(parts));res=eq.subs(dict(zip(axes,filled)),simultaneous=True);C['geometry_substitutions']+=1
  if axes[target]==dep:assert same(res,0)==same(v,want)
  else:
   assert same(res,0);assert 'named parameters directly' in prompt
   if v.is_polynomial(free) and s.Poly(v,free).degree()==1 and not v.has(base):C['covering_scaled_free_distractors']+=not same(v,want)
  C['direct_coordinate_constraints']+=1
 # Graph inverse is exactly the two unrestricted coordinate parameters.
 assert expected[axes.index(base)]==base and expected[axes.index(free)]==free
 rendered=re.findall(r'⟨([^⟩]+)⟩',sol);assert len(rendered)==2 and vec(rendered[0])==tuple(axes) and vec(rendered[1])==expected;C['full_graph_vectors']+=2
 arg_sol=re.search(r'\\begin\{aligned\}([fgh])\(([^)]+)\)',sol);assert arg_sol and arg_sol[1]==fn and [z.strip() for z in arg_sol[2].split(',')]==args
 domains=re.findall(r'\$([xyz])\\in \(-\\infty ,\\infty [).,]+',sol);assert set(domains)==set(args)
 final=re.search(r'Therefore, the (first|second|third) component of \$([fgh])\$ is \$([^$]+)\$',sol);assert final and final[1]==ords[target] and final[2]==fn and same(scalar(final[3]),want);C['conclusions']+=1
 if q[':question/difficulty'].endswith('/hard'):
  assert c.q in (2,3,4,5);block=re.findall(r'\$\$(.*?)\$\$',sol,re.S)[0];a,b=block.split(r'\quad\Longrightarrow\quad');ll,rr=map(scalar,a.split('='));l2,r2=map(scalar,b.split('='));assert same(ll-rr,eq) and l2==dep and same(r2,c*base**2);C['normalization_sides']+=2
 # Shared graph-copy wording survives axis/target changes and the explicit normal repair.
 core=sol[sol.index('For any point'):];core=re.sub(r'\$\$.*?\$\$','@DISPLAY@',core,flags=re.S);core=re.sub(r'\$[^$]*\$','@MATH@',core);core=re.sub(r'\b(first|second|third)\b','@ORDINAL@',core);core=re.sub(r'\s+',' ',core).strip()
 source=O['q-164443'][':question/worked-solution'];old=re.sub(r'\$\$.*?\$\$','@DISPLAY@',source,flags=re.S);old=re.sub(r'\$[^$]*\$','@MATH@',old);old=re.sub(r'\b(first|second|third)\b','@ORDINAL@',old);old=re.sub(r'\s+',' ',old).strip();assert core==old;C['source_prose_masks']+=1
 C['choice_values']+=5;C['records']+=1
out={'passed':True,'source_fidelity':Fid,'readback':C,'script_sha256':hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),'database_writes':0};(R/f'qa/{K}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
