"""Parent actual given maps/xy boundaries/type-I domain/each integration component/PNG."""
import json,re,hashlib,sys,importlib.util,itertools
from pathlib import Path
import sympy as s
import numpy as np
from PIL import Image
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186129197;D=R.parents[2]/f'generate/scratch/{K}'
def load(path,n):
 z=importlib.util.spec_from_file_location(n,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
G=load(D.with_suffix('.py'),'root_typei');P=load(R/'ode-scalar-parser.py','root_typei_parse');fid=load(R/'root-source-fidelity.py','root_typei_fid');O,S=fid.check(G,K,D)
x,y,u,v=P.x,P.y,P.u,P.v
parse=lambda t:P.scalar(t.strip().rstrip('.,'))
def eq(a,b):return s.simplify(s.expand_log(a-b,force=True))==0
C=dict(records=0,actual_maps=0,actual_xy_boundaries=0,actual_transformed_boundary_equations=0,intersection_constraints=0,actual_partial_entries=0,inverse_determinants=0,inner_integral_bounds=0,operative_outer_rows=0,primitive_derivatives=0,individual_endpoint_components=0,collected_endpoint_differences=0,final_areas=0,choice_values=0,criterion_pairs=0,source_prose_masks=0,actual_curve_png_probes=0,actual_zero_axes=0,actual_plot_labels=0,actual_slice_arrow_constraints=0)
records=json.load(open(R/f'qa/{K}-sampled.json'))
# Exercise every source family, including hyper_x absent from the18-seed hard sample.
for f in ['simple','mixed','quartic','hyper_y','down','up','vertical','hyper_x']:
 for seed in [45,77]:records.append(G.generate('easy' if f=='simple' else 'moderate' if f=='mixed' else 'hard',seed,template=f))
records.append(G.generate('hard',template='hyper_x',parameters={'a':5,'h':10,'k':3}))
def mask(t):
 t=re.sub(r'\$\$[\s\S]*?\$\$|\$[^$]*\$','<MATH>',t);t=re.sub(r'!\[\]\(.*?\)','<PLOT>',t);return re.sub(r'\s+',' ',t).strip()
for rec in records:
 q=rec['question'];gen=rec['generation'];f=gen['template'];sol=q[':question/worked-solution'];pr=q[':question/problem']
 maps=re.search(r'\$\$\nu=(.*?),\\,v=(.*?),\n\$\$',pr);assert maps;F,H=map(parse,maps.groups());matrix=s.Matrix([[s.diff(F,x),s.diff(F,y)],[s.diff(H,x),s.diff(H,y)]]);det=s.expand(matrix.det());assert det!=0;J=s.Abs(1/det);inverse=s.solve([u-F,v-H],(x,y));assert set(inverse)=={x,y};C['actual_maps']+=2
 equations=[]
 for text in re.findall(r'\$([^$]+)\$',pr[pr.index('bounded by'):]):
  left,right=text.rstrip(',.').split('=');equations.append(parse(left)-parse(right));C['actual_xy_boundaries']+=1
 projected=[s.simplify(z.subs(inverse,simultaneous=True)) for z in equations]
 dom=re.search(r'Δ=\\\{\(u,v\)\\,:\\,(.*?)\\le u\\le (.*?),\\,(.*?)\\le v\\le (.*?)\\\}\.',sol);assert dom;lo,hi,low,high=map(parse,dom.groups());assert float(hi-lo)>0 and float((high-low).subs(u,(lo+hi)/2))>0
 if f.startswith('hyper'):
  ub=projected[1] if f=='hyper_x' else projected[0];vb=projected[0] if f=='hyper_x' else projected[1];assert eq(ub.subs(u,lo),0) and eq(vb.subs(v,low),0) and eq(projected[2].subs(v,high),0);C['actual_transformed_boundary_equations']+=3
  assert low==lo and eq(hi,high.subs(u,lo));C['intersection_constraints']+=3
  assert 'first line' in sol and 'second line' in sol and 'Substituting ' in sol
 else:
  assert len(projected)==2;curve=high if f=='down' else low;line=low if f=='down' else high
  assert eq(projected[0].subs(v,curve),0) and eq(projected[1].subs(v,line),0);C['actual_transformed_boundary_equations']+=2
  for z in [lo,hi]:assert eq(low.subs(u,z),high.subs(u,z));C['intersection_constraints']+=1
 if f=='quartic':
  block=re.search(r'Now,\n\n\$\$(.*?)\$\$',sol,re.S)[1];actual_y=block.split('y=')[-1].split(r'\end{aligned}')[0];assert eq(parse(actual_y),inverse[y]);assert r'\frac{u-v}' in actual_y
  factor=re.search(r'u\(u\^\{3\}-(.*?)\)=0',sol);assert factor and eq(hi**3,parse(factor[1]))
 area=s.simplify(J*s.integrate(high-low,(u,lo,hi)));assert float(area)>0
 step2=sol[sol.index('**Step 2**'):sol.index('**Step 3**')];mats=re.findall(r'\\begin\{matrix\}(.*?)\\end\{matrix\}',step2,re.S);assert len(mats)==2;actual=[parse(z) for z in re.split(r'&|\\\\',mats[1])];assert actual==list(matrix);C['actual_partial_entries']+=4
 displayed=parse(re.search(r'&=(.*?)\\end\{aligned\}',step2,re.S)[1].rsplit('&=',1)[-1]);assert eq(displayed,det)
 step3=sol[sol.index('**Step 3**'):sol.index('**Step 4**')];block=re.search(r'\$\$\n(.*?)\n\$\$',step3,re.S)[1];assert eq(parse(block.split('=')[-1]),1/det);C['inverse_determinants']+=1
 chain=sol[sol.index('**Step 4**'):];rows=chain.split(r' \\ ');assert len(rows)==(9 if f.startswith('hyper') or f=='quartic' else 10)
 numeric=re.search(r'\\iint_Δ \|(.*?)\|\\,dudv',rows[1]);assert numeric and eq(s.Abs(parse(numeric[1])),J)
 inner=re.search(r'\[\\int_\{(.*?)\}\^\{(.*?)\}dv',rows[2]);assert inner and eq(parse(inner[1]),low) and eq(parse(inner[2]),high);C['inner_integral_bounds']+=2
 outer=r'\int_{'+s.latex(lo)+'}^{'+s.latex(hi)+'}'
 assert outer in rows[2] and r'[v]_{'+s.latex(low)+'}^{'+s.latex(high)+'}' in rows[3]
 for row in rows[2:-4]:
  assert outer in row;weight=parse(row.split('&=')[1].split(r'\int')[0]);assert eq(weight,J);C['operative_outer_rows']+=1
 width=rows[4].split(outer,1)[1].removesuffix('du');assert eq(parse(width),high-low)
 pm=re.search(r'&=(.*?)\[(.*?)\](.*)$',rows[-4]);assert pm and pm[3]=='_{'+s.latex(lo)+'}^{'+s.latex(hi)+'}';weight,primitive=map(parse,pm.groups()[:2]);assert eq(weight,J) and eq(s.diff(primitive,u),high-low);C['primitive_derivatives']+=1
 endpoint=re.search(r'&=(.*?)\((.*)\)$',rows[-3]);assert endpoint and eq(parse(endpoint[1]),J)
 # Each of the two primitive terms at EACH endpoint is verified separately.
 components=[];depth=0;start=None
 for i,ch in enumerate(endpoint[2]):
  if ch=='(':
   depth+=1
   if depth==2:start=i+1
  elif ch==')':
   if depth==2:components.append(endpoint[2][start:i])
   depth-=1
 assert len(components)==4
 terms=s.Add.make_args(primitive);assert len(terms)==2
 terms=sorted(terms,key=lambda z:0 if z.has(s.log) else s.degree(z,u));want=[z.subs(u,p) for p in [hi,lo] for z in terms]
 for text,value in zip(components,want):assert eq(parse(text),value),(f,text,value);C['individual_endpoint_components']+=1
 assert eq(parse(endpoint[2]),primitive.subs(u,hi)-primitive.subs(u,lo))
 collected=re.search(r'&=(.*?)\((.*)\)$',rows[-2]);assert collected and eq(parse(collected[1]),J) and eq(parse(collected[2]),primitive.subs(u,hi)-primitive.subs(u,lo));C['collected_endpoint_differences']+=1
 final=rows[-1].split('&=')[1].split(r'\end{aligned}')[0];assert eq(parse(final),area);C['final_areas']+=1
 fld=q[':question/answer-fields'][0];choices=fld[':answer-field/choices'];vals=[parse(a[':answer/value']) for a in choices];assert len(vals)==5
 for a,b in itertools.combinations(vals,2):assert not eq(a,b);C['criterion_pairs']+=1
 correct=next(a for a in choices if a[':answer/id']==fld[':answer-field/correct'][1]);assert eq(parse(correct[':answer/value']),area);C['choice_values']+=5
 sid=gen['source_question']
 if sid and sid in O and ':question/worked-solution' in O[sid]:assert mask(sol)==mask(O[sid][':question/worked-solution']),(f,'provided prose mismatch');C['source_prose_masks']+=1
 path=Path(re.findall(r'!\[\]\((.*?)\)',sol)[-1]);im=np.asarray(Image.open(path).convert('RGB'));side=json.load(open(path.with_suffix('.json')));A=np.array(side['data_to_pixel_matrix']);assert side['python']==sys.version.split()[0];bbox=side['axes_pixel_bbox'];xl,xh=side['axis_calibration']['xlim'];yl,yh=side['axis_calibration']['ylim']
 assert np.allclose(A@np.array([xl,yh,1]),[bbox[0],bbox[1],1]) and np.allclose(A@np.array([xh,yl,1]),[bbox[0]+bbox[2],bbox[1]+bbox[3],1])
 expected_colors={'lower':'blue' if f=='quartic' else 'red','upper':'red' if f=='quartic' else 'blue'};assert all(side['boundary_colors'][z]==value for z,value in expected_colors.items())
 red=(im[:,:,0]>150)&(im[:,:,1]<110)&(im[:,:,2]<110);blue=(im[:,:,2]>140)&(im[:,:,0]<120)&(im[:,:,1]<140);black=im.max(2)<100
 for fraction in [.08,.2,.35,.5,.7,.88,.96]:
  xx=float(lo+(hi-lo)*s.Rational(str(fraction)))
  for role,z in [('lower',low),('upper',high)]:
   yy=float(z.subs(u,xx));px,py,_=A@np.array([xx,yy,1]);ix,iy=round(px),round(py);color=blue if expected_colors[role]=='blue' else red;assert color[iy-4:iy+5,ix-4:ix+5].any(),(f,role,path,xx,yy);C['actual_curve_png_probes']+=1
 ox,oy,_=A@np.array([0,0,1]);valid_x=np.arange(int(bbox[0])+4,int(bbox[0]+bbox[2])-4);valid_y=np.arange(int(bbox[1])+4,int(bbox[1]+bbox[3])-4)
 detail=side.get('detail_view')
 if detail:
  box=detail['axes_pixel_bbox'];assert detail['title']=='Same region: local view' and detail['same_region'];assert all(eq(s.sympify(z,locals={'u':u}),v0) for z,v0 in zip(detail['bounds'],[lo,hi,low,high]));B=np.array(detail['data_to_pixel_matrix'])
  valid_y=valid_y[(valid_y<box[1]-20)|(valid_y>box[1]+box[3]+20)] if box[0]-20<ox<box[0]+box[2]+20 else valid_y
  valid_x=valid_x[(valid_x<box[0]-20)|(valid_x>box[0]+box[2]+20)] if box[1]-20<oy<box[1]+box[3]+20 else valid_x
  for fraction in [.08,.2,.35,.5,.7,.88,.96]:
   xx=float(lo+(hi-lo)*s.Rational(str(fraction)))
   for role,z in [('lower',low),('upper',high)]:
    yy=float(z.subs(u,xx));px,py,_=B@np.array([xx,yy,1]);ix,iy=round(px),round(py);color=blue if expected_colors[role]=='blue' else red;assert color[iy-4:iy+5,ix-4:ix+5].any();C['actual_curve_png_probes']+=1
 assert black[round(oy)-2:round(oy)+3,valid_x].any(0).mean()>.7 and black[valid_y,round(ox)-2:round(ox)+3].any(1).mean()>.7;C['actual_zero_axes']+=2
 labels={z['role']:z for z in side['artist_labels'] if z['role'] not in ['u_tick','v_tick']}
 for role,z in [('lower_boundary',low),('upper_boundary',high)]:
  label=labels[role];assert label['text'].startswith('$v=') and eq(parse(label['text'][3:-1]),z);assert label['color']==expected_colors[role.split('_')[0]];C['actual_plot_labels']+=1
 for z in side['artist_labels']:
  l,t,w,h=z['bbox_pixel'];assert 0<=l<l+w<=im.shape[1] and 0<=t<t+h<=im.shape[0]
 arrow=side['slice_arrow'];assert arrow['tail_data'][0]==arrow['head_data'][0] and arrow['tail_data'][1]<arrow['head_data'][1]
 for role in ['tail','head']:
  au,av=arrow[role+'_data'];assert float(lo)<au<float(hi) and float(low.subs(u,au))<av<float(high.subs(u,au));assert np.allclose((np.array(arrow['data_to_pixel_matrix'])@np.array([au,av,1]))[:2],arrow[role+'_pixel']);C['actual_slice_arrow_constraints']+=1

 region=labels['region'];rl,rt,rw,rh=region['bbox_pixel']
 annotation_A=np.array(arrow['data_to_pixel_matrix']);zx,zy,_=annotation_A@np.array([0,0,1]);assert not rl-4<=zx<=rl+rw+4,(f,'Delta overlaps vertical zero axis',path);assert not rt-4<=zy<=rt+rh+4,(f,'Delta overlaps horizontal zero axis',path)
 al,at,aw,ah=arrow['artist_bbox_pixel'];assert rl>=al+aw or al>=rl+rw or rt>=at+ah or at>=rt+rh,(f,'arrow overlaps Delta',path)
 assert black[max(0,int(at)):int(at+ah)+2,max(0,int(al)):int(al+aw)+2].sum()>15
 C['records']+=1
out=dict(status='passed',source=S,readback=C,original_assets_full_resolution=9,script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest());(R/f'qa/{K}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
