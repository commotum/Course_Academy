"""Root verifies actual hyperbola sheets, full banks and every source-shaped stage."""
import hashlib,importlib.util,itertools,json,re,sys
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent;K=17592186175973;D=R.parents[2]/f'generate/scratch/{K}'
def mod(n,p):
 sp=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(sp);sys.modules[n]=m;sp.loader.exec_module(m);return m
P=mod('root_hyp_parser',R/'ode-scalar-parser.py');G=mod('root_hyp_gen',D.with_suffix('.py'));F=mod('root_hyp_source',R/'root-source-fidelity.py');O,Fid=F.check(G,K,D);t=P.t;axes=[P.x,P.y,P.z]
def scalar(z):return P.scalar(z.strip().rstrip('.,').replace('&','').replace(r'\,',''))
def vec(z):return tuple(scalar(v) for v in z.replace(r'\,','').split(','))
def same(a,b):return s.trigsimp(s.expand(a-b))==0
def veq(a,b):return len(a)==len(b) and all(same(v,w) for v,w in zip(a,b))
def mask(z):
 z=re.sub(r'\$\$.*?\$\$','@DISPLAY@',z,flags=re.S);z=re.sub(r'\$[^$]*\$','@MATH@',z);z=re.sub(r'\b(first|second|third|xy|xz|yz)\b','@ROLE@',z);return re.sub(r'\s+',' ',z).strip()
C=dict(records=0,choice_values=0,whole_bank_pairs=0,geometric_witnesses=0,positive_sheet_tests=0,normalization_relations=0,identity_sides=0,planar_components=0,full_graph_vectors=0,conclusions=0,source_prose_masks=0,negative_tan_covering_regressions=0)
rows=json.load(open(R/f'qa/{K}-sampled.json'))
# Every family at fixed mathematical scales must support all six Cartesian permutations.
for name,spec in G.SPECS.items():
 for permutation in itertools.permutations('xyz'):
  p={'a':spec['a'],'b2':spec['b2'],'axes':''.join(permutation)};rows.append(G.generate(spec['level'],template=name,parameters=p))
for rec in rows:
 q,m=rec['question'],rec['generation'];md=q[':question/problem'];sol=q[':question/worked-solution']
 head=re.search(r'f\(([^)]+)\)\s*=\s*⟨([^⟩]+)⟩',md);assert head;args=[z.strip() for z in head[1].split(',')];parts=head[2].replace(r'\,','').split(',');target=next(i for i,z in enumerate(parts) if '_' in z);assert sum('_' in z for z in parts)==1
 rel=re.search(r'coordinates as \$([^$]+)\$',md)[1];lhs,rhs=map(scalar,rel.split('='));E=s.Poly(s.expand(lhs-rhs),*axes)
 branch=re.search(r'for \$([xyz])\s*\\ge\s*([^$]+)\$',md);assert branch;secaxis=next(z for z in axes if str(z)==branch[1]);threshold=scalar(branch[2]);assert threshold>0
 tanaxis=next(z for z in axes if E.coeff_monomial(z*z)<0);free=next(z for z in axes if z not in (secaxis,tanaxis));A=E.coeff_monomial(secaxis*secaxis);B=-E.coeff_monomial(tanaxis*tanaxis);constant=-E.coeff_monomial(1);a=s.sqrt(constant/A);b=s.sqrt(constant/B);assert threshold==a and A>0 and B>0
 assert set(args)=={'t',str(free)}
 interval=re.search(r't\s*(?:\\in|∈)\s*\(([^,]+),([^)]*)\)',md);assert interval and scalar(interval[1])==-s.pi/2 and scalar(interval[2])==s.pi/2
 assert E.as_expr()==A*secaxis**2-B*tanaxis**2-constant
 want=tuple(a*s.sec(t) if z==secaxis else b*s.tan(t) if z==tanaxis else z for z in axes);requested=want[target]
 for i,part in enumerate(parts):
  if i!=target:assert same(scalar(part),want[i])
 # tan spans R on the open interval; positive sec then covers the full prescribed sheet.
 assert s.limit(s.tan(t),t,-s.pi/2,dir='+')==-s.oo and s.limit(s.tan(t),t,s.pi/2,dir='-')==s.oo
 field=q[':question/answer-fields'][0];vals=[scalar(z[':answer/value']) for z in field[':answer-field/choices']];assert len(vals)==5
 assert [z[':answer/id'] for z,v in zip(field[':answer-field/choices'],vals) if same(v,requested)]==[field[':answer-field/correct'][1]]
 maps=[]
 for value in vals:
  candidate=tuple(value if i==target else scalar(part) for i,part in enumerate(parts));maps.append(candidate);res=E.as_expr().subs(dict(zip(axes,candidate)),simultaneous=True)
  geometry=all(s.simplify(res.subs(t,p))==0 for p in (0,s.pi/6,s.pi/4));sheet=all(candidate[axes.index(secaxis)].subs(t,p)>=a for p in (0,s.pi/6,s.pi/4));C['geometric_witnesses']+=3;C['positive_sheet_tests']+=3
  assert bool(geometry and sheet)==same(value,requested)
 for i,left in enumerate(maps):
  for right in maps[i+1:]:
   assert not veq(left,right)
   # With a supplied sec component, t reversal can describe the same complete curve.
   if axes[target]==tanaxis:assert not veq(left,tuple(z.subs(t,-t) for z in right))
   C['whole_bank_pairs']+=1
 if axes[target]==tanaxis:
  negative=tuple(-z if axis==tanaxis else z for axis,z in zip(axes,want));assert all(s.simplify(E.as_expr().subs(dict(zip(axes,negative)),simultaneous=True).subs(t,p))==0 for p in (0,s.pi/6,s.pi/4));assert veq(negative,tuple(z.subs(t,-t) if z.has(t) else z for z in want));C['negative_tan_covering_regressions']+=1
 ords=('first','second','third');assert 'What is the '+ords[target]+' component' in md
 # Read the planar and full Cartesian tuples, keeping conventional basis order.
 tuples=re.findall(r'⟨([^⟩]+)⟩',sol);assert len(tuples)==4
 plane=tuple(sorted((secaxis,tanaxis),key=lambda z:'xyz'.index(str(z))));assert ''.join(map(str,plane))+'$-plane' in sol or ''.join(map(str,plane))+'-plane' in sol
 assert vec(tuples[0])==plane
 expectedplane=tuple(want[axes.index(z)] for z in plane);assert veq(vec(tuples[1]),expectedplane);C['planar_components']+=2
 assert vec(tuples[2])==tuple(axes) and veq(vec(tuples[3]),want);C['full_graph_vectors']+=2
 blocks=re.findall(r'\$\$(.*?)\$\$',sol,re.S)
 for block in blocks:
  if '⇒' in block:
   for relation in block.split('⇒'):
    relation=relation.replace(r'\,','');ll,rr=map(scalar,relation.split('='));assert same((ll-rr).subs(dict(zip(axes,want)),simultaneous=True),0);C['normalization_relations']+=1
  elif r'\begin{aligned}' in block and '⟨' not in block:
   text=block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').replace('&','');previous=None
   for row in text.split(chr(92)*2):
    for side in row.split('='):
     if not side.strip():continue
     value=scalar(side).subs(dict(zip(axes,want)),simultaneous=True)
     if previous is not None:assert same(value,previous);C['identity_sides']+=1
     previous=value
 final=re.search(r'Therefore, the (first|second|third) component of \$f\$ is \$([^$]+)\$',sol);assert final and final[1]==ords[target] and same(scalar(final[2]),requested);C['conclusions']+=1
 sid=G.SPECS[m['template']]['source']
 if ':question/worked-solution' in O[sid]:assert mask(sol)==mask(O[sid][':question/worked-solution']);C['source_prose_masks']+=1
 C['choice_values']+=5;C['records']+=1
out={'passed':True,'source_fidelity':Fid,'readback':C,'script_sha256':hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),'database_writes':0};(R/f'qa/{K}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
