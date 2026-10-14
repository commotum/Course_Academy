"""Parent all displayed given maps, boundary images, matrix entries and area chains."""
import json,re,hashlib,importlib.util,sys,itertools
from pathlib import Path
import sympy as s
import numpy as np
from PIL import Image
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186129261;D=R.parents[2]/f'generate/scratch/{K}'
def load(path,n):
 z=importlib.util.spec_from_file_location(n,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
G=load(D.with_suffix('.py'),'root_rectg');P=load(R/'domain-math-parser.py','root_rectg_parse');fid=load(R/'root-source-fidelity.py','root_rectg_fid');O,S=fid.check(G,K,D)
X,Y,U,V=s.symbols('x y u v',positive=True)
def parse(t):return P.scalar(t.strip().rstrip('.,')).subs({P.x:X,P.y:Y,P.u:U,P.v:V})
def eq(a,b):return s.simplify(s.expand_log(a-b,force=True))==0
M=re.compile(r'\$\$(.*?)\$\$|(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)',re.S)
def islands(t):return [(m[1] if m[1] is not None else m[2]).strip() for m in M.finditer(t)]
def mask(t):return re.sub(r'!\[\]\(.*?\)','![](<PLOT>)',M.sub('<MATH>',t))
C=dict(records=0,actual_given_maps=0,actual_prompt_boundary_images=0,actual_solution_boundary_rows=0,actual_derivative_entries=0,determinant_rows=0,inverse_cancellation_components=0,actual_integral_kernels=0,separate_integrals=0,individual_endpoint_components=0,final_areas=0,choice_values=0,criterion_pairs=0,source_prose_masks=0,actual_rectangle_edges=0,actual_zero_axes=0,interior_zero_axes=0)
records=json.load(open(R/f'qa/{K}-sampled.json'))
for c in json.load(open(D/'source-cases.json')):records.append(G.generate(c['level'],template=c['template'],parameters=c['parameters']))
for t in ['linear','linear_legacy','quotient','reciprocal','reciprocal_scaled']:
 for seed in [47,69]:records.append(G.generate('easy' if t.startswith('linear') else 'moderate' if t in ['quotient','reciprocal'] else 'hard',seed,template=t))
for rec in records:
 q=rec['question'];gen=rec['generation'];t=gen['template'];p=[z for z in islands(q[':question/problem']) if z.startswith(('u=','y='))];assert len(p)==2
 given=p[0].rstrip(',').split(r',\qquad ');assert [z.split('=')[0] for z in given]==['u','v'];f,g=[parse(z.split('=')[1]) for z in given];C['actual_given_maps']+=2
 curves=p[1].rstrip('.').split(r',\qquad ');assert len(curves)==4
 bounds=[]
 for e,z in zip(curves,[f,f,g,g]):
  left,right=e.split('=');assert left=='y';v=s.simplify(z.subs(Y,parse(right)));assert v.is_Integer;bounds.append(int(v));C['actual_prompt_boundary_images']+=1
 a,b,c,d=bounds;assert a<b and c<d
 entries=[s.diff(f,X),s.diff(f,Y),s.diff(g,X),s.diff(g,Y)];det=s.expand(entries[0]*entries[3]-entries[1]*entries[2]);assert det!=0
 if not det.free_symbols:J=1/det
 else:
  cf=s.cancel(det/f)
  if not cf.free_symbols:J=1/(cf*U)
  else:factor=s.cancel(f**2*g/det);assert not factor.free_symbols;J=factor/(U**2*V)
 jac=s.Abs(J);A=s.integrate(jac,(U,a,b),(V,c,d));assert A>0
 if t.startswith('linear'):assert 'first quadrant' not in q[':question/problem'] and not det.free_symbols
 else:assert 'first quadrant' in q[':question/problem'] and a>0 and c>0
 sol=q[':question/worked-solution'];blocks=[z.strip() for z in re.findall(r'\$\$(.*?)\$\$',sol,re.S)];assert len(blocks)==11
 given2=blocks[3].split(r',\,');assert eq(parse(given2[0].split('=')[1]),f) and eq(parse(given2[1].split('=')[1]),g)
 for block,z,var,want in [(blocks[5],f,'u',[a,b]),(blocks[6],g,'v',[c,d])]:
  rows=block.removeprefix(r'\begin{aligned}').removesuffix(r'\end{aligned}').split(r'\\');assert len(rows)==2
  for row,val in zip(rows,want):
   components=row.split('& ⟹\\, & ');assert len(components)==3
   eqn=components[0].strip().removeprefix('&').strip();left,right=eqn.split('=');assert left=='y';curve=parse(right)
   middle=components[1].strip();lhs,rhs=middle.split('=');assert eq(parse(lhs),z) and parse(rhs)==val and eq(z.subs(Y,curve),s.Integer(val));assert components[2].strip()==var+'='+str(val);C['actual_solution_boundary_rows']+=1
 assert list(map(int,sum([list(z) for z in re.findall(r'(-?\d+)\\le [uv]\\le (-?\d+)',blocks[7])],[])))==bounds
 matrices=re.findall(r'\|\\begin\{aligned\}(.*?)\\end\{aligned\}\|',blocks[8],re.S);assert len(matrices)==2
 actual=[parse(z.strip()) for row in matrices[1].split(r'\\') for z in row.split('&')];assert all(eq(z,v) for z,v in zip(actual,entries));C['actual_derivative_entries']+=4
 last=blocks[8].rsplit(' & =',1)[1].split(r'\end{aligned}')[0];assert eq(parse(last),det);C['determinant_rows']+=1
 inverses=blocks[9].split('=')[2:];assert len(inverses)>=2
 for z in inverses:assert eq(parse(z).subs({U:f,V:g}),1/det),(t,z,det);C['inverse_cancellation_components']+=1
 final=blocks[10].removeprefix(r'\begin{aligned}').removesuffix(r'\end{aligned}');rows=final.split(r'\\');rhs=[z.split('& =',1)[1].strip() for z in rows];assert len(rhs)==6
 kernel=rhs[1].replace('{∬}_{Δ}','').replace(r'\,','').replace(r'\text{d}u','').replace(r'\text{d}v','');assert eq(parse(kernel),jac);C['actual_integral_kernels']+=1
 if t.startswith('linear'):
  reduced=rhs[2].replace('{∬}_{Δ}','').replace(r'\,','').replace(r'\text{d}u','').replace(r'\text{d}v','');assert eq(parse(reduced),jac)
  areaexpr=rhs[3].replace(r'\text{Area}(Δ)',str((b-a)*(d-c)));assert eq(parse(areaexpr),A)
  parts=rhs[4].split(r'\cdot');assert len(parts)==3;assert all(eq(parse(z),v) for z,v in zip(parts,[jac,b-a,d-c]));C['individual_endpoint_components']+=3
 else:
  ints=list(re.finditer(r'\\int_\{(-?\d+)\}\^\{(-?\d+)\}',rhs[2]));assert len(ints)==2;assert [tuple(map(int,z.groups())) for z in ints]==[(a,b),(c,d)]
  tail=rhs[2][ints[-1].end():];kernel=re.split(r'\\,\\mathrm d ',tail)[0];assert eq(parse(kernel),jac);assert rhs[2].endswith(r'\mathrm d v\,\mathrm d u');C['actual_integral_kernels']+=1
  sep=rhs[3];ints=list(re.finditer(r'\\int_\{(-?\d+)\}\^\{(-?\d+)\}',sep));assert len(ints)==2;coefficient=parse(sep[:ints[0].start()]) if ints[0].start() else s.Integer(1);parts=[];kernels=[]
  for i,z in enumerate(ints):
   tail=sep[z.end():ints[i+1].start() if i+1<len(ints) else len(sep)];diff=re.search(r'\\,\\mathrm d ([uv])',tail);assert diff;var=U if diff[1]=='u' else V;kernel=parse(tail[:diff.start()]);lo,hi=map(int,z.groups());assert (lo,hi)==((a,b) if var==U else (c,d));primitive=s.integrate(kernel,var);assert eq(s.diff(primitive,var),kernel);parts.append(primitive.subs(var,hi)-primitive.subs(var,lo));kernels.append(kernel);C['separate_integrals']+=1
  assert eq(coefficient*kernels[0]*kernels[1],jac) and eq(coefficient*parts[0]*parts[1],A)
  endpoint=rhs[4].split(r'\cdot');want=([coefficient] if len(endpoint)==3 else [])+parts;assert len(endpoint)==len(want)
  for z,value in zip(endpoint,want):assert eq(parse(z),value),(t,z,value);C['individual_endpoint_components']+=1
 assert eq(parse(rhs[-1]),A);C['final_areas']+=1
 field=q[':question/answer-fields'][0];choices=field[':answer-field/choices'];vals=[parse(z[':answer/value']) for z in choices];assert len(vals)==5
 for i,j in itertools.combinations(range(5),2):assert not eq(vals[i],vals[j]);C['criterion_pairs']+=1
 correct=next(z for z in choices if z[':answer/id']==field[':answer-field/correct'][1]);assert eq(parse(correct[':answer/value']),A);C['choice_values']+=5
 assert mask(sol)==mask(O['q-160870' if t.startswith('linear') else 'q-160891'][':question/worked-solution']);C['source_prose_masks']+=1
 # Original/changed marks are arithmetic values, not inferred from silhouette.
 plot=gen['plot'];im=np.asarray(Image.open(plot['path']).convert('RGB'));spec=plot['spec'];lo,hi,bot,top=spec['limits'];h,w=im.shape[:2];sx=w*.9/(hi-lo);sy=h*.84/(top-bot);ox=w*.04-lo*sx;oy=h-(h*.1-bot*sy)
 red=(im[:,:,0]>170)&(im[:,:,1]<100)&(im[:,:,2]<100);blue=(im[:,:,2]>170)&(im[:,:,0]<100)&(im[:,:,1]<100);black=im.max(2)<100
 for xx in np.linspace(a+(b-a)*.1,b-(b-a)*.1,5):
  ix=round(ox+xx*sx)
  for yy,color in [(c,blue if t.startswith('linear') else red),(d,red if t.startswith('linear') else blue)]:
   iy=round(oy-yy*sy);assert color[iy-3:iy+4,ix-3:ix+4].any(),(t,plot['path'],xx,yy)
 for xx in [a,b]:
  ix=round(ox+xx*sx);iy=round(oy-(c+d)/2*sy);inside=ix+3 if xx==a else ix-3;outside=ix-3 if xx==a else ix+3;assert np.allclose(im[iy,inside],[223,234,242],atol=10),(t,plot['path'],xx,im[iy,inside]);assert im[iy,outside].min()>245
 C['actual_rectangle_edges']+=4
 assert black[round(oy)-2:round(oy)+3,30:525].sum()>350 and black[35:420,round(ox)-2:round(ox)+3].sum()>250;C['actual_zero_axes']+=2
 if a<0<b:
  iy=round(oy-(c+d)*.5*sy);assert black[iy-3:iy+4,round(ox)-3:round(ox)+4].any();C['interior_zero_axes']+=1
 C['records']+=1
out=dict(status='passed',source=S,readback=C,original_assets_full_resolution=5,script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest());(R/f'qa/{K}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
