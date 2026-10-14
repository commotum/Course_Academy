"""Root reads surface/partial/cofactor/norm mathematics from learner output."""
import hashlib,importlib.util,itertools,json,re,sys
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent;K=17592186119887;D=R.parents[2]/f'generate/scratch/{K}'
def mod(n,p):
 sp=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(sp);sys.modules[n]=m;sp.loader.exec_module(m);return m
P=mod('root_fvp_parser',R/'ode-scalar-parser.py');G=mod('root_fvp_gen',D.with_suffix('.py'));F=mod('root_fvp_fidelity',R/'root-source-fidelity.py');O,Fid=F.check(G,K,D);u,v=P.u,P.v;x=s.Symbol('x',nonnegative=True);P.locals_['x']=x

def scalar(z):return P.scalar(z.replace(r'\theta','t').strip().rstrip('.,'))
def vec(z):return s.Matrix([scalar(t) for t in z.strip().strip('⟨⟩').replace(r'\,','').split(',')])
def same(a,b):return s.simplify(s.trigsimp(s.expand(a-b)))==0
def veq(a,b):return len(a)==len(b) and all(same(z,w) for z,w in zip(a,b))
def mask(text):return re.sub(r'\s+',' ',re.sub(r'\$[^$]*\$','@MATH@',re.sub(r'\$\$.*?\$\$','@DISPLAY@',text,flags=re.S))).strip()
BASE={'q-105606':s.Matrix([s.sin(u),v*v,4*v*s.cos(u)]),'q-105607':s.Matrix([u+v,v*v+s.sin(u),u*v]),'q-109904':s.Matrix([u,v,u*u-v*v]),'q-109909':s.Matrix([u,v,u-s.exp(v)]),'q-109911':s.Matrix([u*u+1,v**3+1,2*u+v]),'q-109912':s.Matrix([u,u*s.sin(v),v*s.cos(u)])}
source_math={'banks':0,'values':0,'existing_keys':0,'independently_inferred_missing_keys':0}
for sid,o in O.items():
 if sid=='q-167648':truth=2*x*x*s.sqrt(16*x*x+1)
 else:truth=BASE[sid].diff(u).cross(BASE[sid].diff(v))
 for field in o[':question/answer-fields']:
  choices=field[':answer-field/choices'];values=[scalar(a[':answer/value']) if sid=='q-167648' else vec(a[':answer/value']) for a in choices]
  good=lambda value:same(value,truth) if sid=='q-167648' else veq(value,truth)
  assert sum(good(a) for a in values)==1
  if ':answer-field/correct' in field:
   selected=next(a[':answer/value'] for a in choices if a[':answer/id']==field[':answer-field/correct'][':answer/id']);assert good(scalar(selected) if sid=='q-167648' else vec(selected));source_math['existing_keys']+=1
  else:source_math['independently_inferred_missing_keys']+=1
  source_math['banks']+=1;source_math['values']+=len(values)
C=dict(records=0,actual_surface_components=0,partial_inputs=0,partial_values=0,determinant_cells=0,minor_cells=0,cofactor_signs=0,cross_conclusions=0,choice_values=0,bank_pairs=0,norm_stages=0,source_prose_masks=0,level_workload_checks=0)
rows=json.load(open(R/f'qa/{K}-sampled.json'))
# Default random samples omitted some source shapes at some levels; explicit supplements cover all.
for level in ('easy','moderate','hard'):
 for sid in BASE:
  template=sid if level=='easy' else level+':'+sid;rows.append(G.generate(level,seed=331,template=template))
for rec in rows:
 q,m=rec['question'],rec['generation'];md=q[':question/problem'];sol=q[':question/worked-solution'];source=m['source_ids'][0];level=q[':question/difficulty'].split('/')[-1]
 fields=q[':question/answer-fields'];assert len(fields)==1
 if source=='q-167648':
  supplied=vec(re.search(r'⟨([^⟩]+)⟩',md)[0]);want=s.simplify(s.sqrt(s.trigsimp(supplied.dot(supplied))))
  vals=[scalar(a[':answer/value']) for a in fields[0][':answer-field/choices']];assert len(vals)==1 and same(vals[0],want);assert '{{field-1}}' in md and level=='easy'
  rows0=re.findall(r'&\s*=\s*(.*?)(?=\\\\|\\end\{aligned\})',sol,re.S);assert len(rows0)==5
  for z in rows0:assert same(scalar(z),want),(z,scalar(z),want,s.simplify(scalar(z)-want));C['norm_stages']+=1
  assert '({cos}^{2}' in rows0[2] and '{sin}^{2}' in rows0[2];assert '({cos}^{2}' not in rows0[3]
  old=O[source][':question/worked-solution'];old=old[old.index('Finally, the corresponding norm is'):];assert mask(sol)==mask(old);C['source_prose_masks']+=1;C['choice_values']+=1;C['records']+=1;continue
 if '⟨' in md:surface=vec(re.search(r'⟨([^⟩]+)⟩',md)[0])
 else:
  matches=re.findall(r'\$\$(.*?)\$\$|(?<!\$)\$(?!\$)([^$]+)\$(?!\$)',md,re.S);body=next(a or b for a,b in matches if re.match(r'x\s*=',(a or b).strip()));parts=body.replace(r'\,','').strip().rstrip('.').split(',');assert [z.split('=')[0].strip() for z in parts]==list('xyz');surface=s.Matrix([scalar(z.split('=')[1]) for z in parts])
 scales=[s.simplify(a/b) for a,b in zip(surface,BASE[source])];assert all(z in (1,2,3,4) for z in scales);nonunit=sum(z!=1 for z in scales)
 assert nonunit<=1 if level=='easy' else nonunit==(2 if level=='moderate' else 3);C['level_workload_checks']+=1
 du,dv=surface.diff(u),surface.diff(v);cross=du.cross(dv);C['actual_surface_components']+=3
 vectors=re.findall(r'⟨[^⟨⟩]*⟩',sol)
 # Read complete formal differentiated inputs and collected partial vectors.
 derivative_inputs=[z for z in vectors if r'\frac{∂}{∂' in z];assert len(derivative_inputs)==2
 for raw,axis,want in zip(derivative_inputs,(u,v),(du,dv)):
  parts=raw[1:-1].replace(r'\,','').split(',');assert len(parts)==3
  for part,component,derivative in zip(parts,surface,want):
   prefix=r'\frac{∂}{∂'+str(axis)+'}';assert part.strip().startswith(prefix);inside=part.strip()[len(prefix):];assert inside[0]=='(' and inside[-1]==')';expected_input=component-scales[0] if source=='q-109911' and axis==v and component==surface[0] else component;assert same(scalar(inside[1:-1]),expected_input) and same(s.diff(scalar(inside[1:-1]),axis),derivative),(source,axis,inside,scalar(inside[1:-1]),component,derivative);C['partial_inputs']+=1
 for raw,want in zip(derivative_inputs,(du,dv)):
  idx=vectors.index(raw);assert veq(vec(vectors[idx+1]),want);C['partial_values']+=3
 # Stack matching recovers actual nested determinant/minor cells, independent of sidecar metadata.
 spans=[];stack=[]
 for match in re.finditer(r'\\(?:begin|end)\{aligned\}',sol):
  if match[0].startswith(r'\begin'):stack.append(match)
  else:
   begin=stack.pop();body=sol[begin.end():match.start()]
   if r'\begin{aligned}' not in body and '=' not in body and ' & ' in body:spans.append((begin.start(),body))
 spans.sort();assert len(spans)==4
 det=[row.strip().split('&') for row in spans[0][1].split(chr(92)*2)];assert len(det)==3 and [z.strip() for z in det[0]]==list('ijk')
 assert veq(s.Matrix([scalar(z) for z in det[1]]),du) and veq(s.Matrix([scalar(z) for z in det[2]]),dv);C['determinant_cells']+=6
 for j,((start,body),cols) in enumerate(zip(spans[1:],((1,2),(0,2),(0,1)))):
  mat=[[scalar(z) for z in row.split('&')] for row in body.split(chr(92)*2)];assert mat==[[du[c] for c in cols],[dv[c] for c in cols]];C['minor_cells']+=4
  before=sol[:start];assert bool(re.search(r',\\,-\|$',before))==(j==1);C['cofactor_signs']+=1
 final=next(z for z in reversed(vectors) if r'\begin' not in z and r'\frac{∂' not in z);assert veq(vec(final),cross);C['cross_conclusions']+=1
 field=fields[0];values=[vec(a[':answer/value']) for a in field[':answer-field/choices']];assert len(values)==5
 assert [a[':answer/id'] for a,vv in zip(field[':answer-field/choices'],values) if veq(vv,cross)]==[field[':answer-field/correct'][1]]
 wrong_middle=s.Matrix([cross[0],-cross[1],cross[2]]);expected=[cross,-cross,wrong_middle,du,dv];assert all(any(veq(a,b) for b in values) for a in expected)
 for i,a in enumerate(values):
  for b in values[i+1:]:assert not veq(a,b);C['bank_pairs']+=1
 if ':question/worked-solution' in O[source]:assert mask(sol)==mask(O[source][':question/worked-solution']);C['source_prose_masks']+=1
 C['choice_values']+=5;C['records']+=1
out={'passed':True,'source_fidelity':Fid,'source_math':source_math,'readback':C,'script_sha256':hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),'database_writes':0};(R/f'qa/{K}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
