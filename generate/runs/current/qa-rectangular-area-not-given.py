"""Root displayed transformation/bounds/Jacobian/all kernels/separate endpoints/banks."""
import json,re,hashlib,importlib.util,sys,itertools
from pathlib import Path
import sympy as s
import numpy as np
from PIL import Image
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186129262;D=R.parents[2]/f'generate/scratch/{K}'
def load(path,n):
 z=importlib.util.spec_from_file_location(n,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
G=load(D.with_suffix('.py'),'root_rectng');P=load(R/'domain-math-parser.py','root_rectng_parse');fid=load(R/'root-source-fidelity.py','root_rectng_fid');O,S=fid.check(G,K,D)
X,Y,U,V=s.symbols('x y u v',positive=True)
def parse(t):return P.scalar(t.strip().rstrip('.,')).subs({P.x:X,P.y:Y,P.u:U,P.v:V})
def eq(a,b):return s.simplify(s.expand_log(a-b,force=True))==0
M=re.compile(r'\$\$(.*?)\$\$|(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)',re.S)
def islands(t):return [(m[1] if m[1] is not None else m[2]).strip() for m in M.finditer(t)]
def mask(t):return re.sub(r'!\[\]\(.*?\)','![](<PLOT>)',M.sub('<MATH>',t))
C=dict(records=0,actual_prompt_boundaries=0,actual_substitution_equations=0,actual_transformed_boundaries=0,actual_matrix_entries=0,determinant_distribution_rows=0,inverse_determinants=0,integral_kernels=0,separate_definite_integrals=0,separate_endpoint_components=0,final_areas=0,choice_values=0,criterion_pairs=0,source_prose_masks=0,actual_rectangle_edges=0,actual_zero_axes=0,actual_interior_zero_axes=0)
records=json.load(open(R/f'qa/{K}-sampled.json'))
for template in ['product_ratio','linear_5_3','linear_3_1','linear_4_3','square_product','product_square_ratio']:
 for vals in [[2,5,1,4],[1,5,2,5],[-2,3,-1,2]] if template.startswith('linear') else [[2,5,1,4],[1,5,2,5]]:
  try:records.append(G.generate('moderate' if template.startswith('linear') else 'easy' if template=='product_ratio' else 'hard',template=template,parameters=dict(zip('abcd',vals))))
  except ValueError:continue
for rec in records:
 q=rec['question'];gen=rec['generation'];t=gen['template'];sol=q[':question/worked-solution'];blocks=islands(sol)
 prompt=islands(q[':question/problem'])[-1];equations=prompt.split(r',\,') if r',\,' in prompt else prompt.split(', ');assert len(equations)==4
 transformations=blocks[11].split(r',\,');assert [v.split('=')[0] for v in transformations]==['u','v'];f,g=[parse(v.split('=')[1]) for v in transformations];assert f.free_symbols|g.free_symbols=={X,Y};C['actual_substitution_equations']+=2
 bounds=[]
 for e,z in zip(equations,[f,f,g,g]):
  left,right=e.split('=');e=s.together(parse(left)-parse(right)).as_numer_denom()[0]
  valid=[]
  for val in range(-4,9):
   diff=s.together(z-val).as_numer_denom()[0];ratio=s.cancel(e/diff)
   if ratio!=0 and not ratio.free_symbols:valid.append(val)
  assert len(valid)==1,(equations,z,valid);bounds.append(valid[0]);C['actual_prompt_boundaries']+=1
 a,b,c,d=bounds;assert a<b and c<d
 assert list(gen['parameters'].values())==bounds
 for index,variable,want in [(18,'u',[a,b]),(20,'v',[c,d])]:
  block=blocks[index];values=list(map(int,re.findall(variable+r'=(-?\d+)',block)));assert values==want
  equations_in_row=re.findall(r'& (.*?)\\,⟹\\,',block);assert len(equations_in_row)==2
  z=f if variable=='u' else g
  for e,val in zip(equations_in_row,want):
   left,right=e.split('=');ratio=s.cancel(s.together(parse(left)-parse(right)).as_numer_denom()[0]/s.together(z-val).as_numer_denom()[0]);assert ratio!=0 and not ratio.free_symbols
  C['actual_transformed_boundaries']+=2
 assert list(map(int,sum([list(z) for z in re.findall(r'(-?\d+)\\le [uv]\\le (-?\d+)',blocks[22])],[])))==bounds
 entries=[s.diff(f,X),s.diff(f,Y),s.diff(g,X),s.diff(g,Y)];det=s.expand(entries[0]*entries[3]-entries[1]*entries[2]);assert det!=0
 if not det.free_symbols:duv=det
 else:
  cf=s.cancel(det/f);cg=s.cancel(det/g)
  if not cf.free_symbols:duv=cf*U
  else:assert not cg.free_symbols;duv=cg*V
 jac=s.Abs(1/duv);A=s.integrate(jac,(U,a,b),(V,c,d));assert A>0
 mb=blocks[25];matrices=re.findall(r'\|\\begin\{aligned\}(.*?)\\end\{aligned\}\|',mb,re.S);assert len(matrices)==2
 displayed=[parse(z.strip()) for row in matrices[1].split(r'\\') for z in row.split('&')];assert len(displayed)==4 and all(eq(e,z) for e,z in zip(displayed,entries));C['actual_matrix_entries']+=4
 rest=mb[mb.rfind(r'\end{aligned}|')+len(r'\end{aligned}|'):];stages=re.findall(r'& =(.*?)(?:\\\\|\\end\{aligned\})',rest,re.S);assert len(stages)>=2
 for e in stages:assert eq(parse(e).subs({U:f,V:g}),det),(t,e,det);C['determinant_distribution_rows']+=1
 inv=parse(blocks[28].split('=')[-1]);assert eq(inv,1/duv);C['inverse_determinants']+=1
 final=blocks[33];rows=final.removeprefix(r'\begin{aligned}').removesuffix(r'\end{aligned}').split(r'\\');rhs=[z.split('& =',1)[1].strip() for z in rows]
 assert '|'+r'\frac{∂(x,y)}{∂(u,v)}'+'|' in rhs[0]
 integralrow=None
 for row in rhs[1:-2]:
  if '{∬}_{Δ}' in row:
   kernel=re.sub(r'\\,|\\text\{d\}[uv]','',row.replace('{∬}_{Δ}',''));assert eq(parse(kernel) if kernel.strip() else s.Integer(1),jac),(t,kernel,jac);C['integral_kernels']+=1
  elif r'{\int }_' in row:integralrow=row
  else:raise AssertionError(('unexpected integral teaching row',row))
 assert integralrow is not None
 ints=list(re.finditer(r'\{\\int \}_\{(-?\d+)\}\^\{(-?\d+)\}',integralrow));assert len(ints)==2
 coefficient=parse(integralrow[:ints[0].start()]) if ints[0].start() else s.Integer(1);parts=[];kernels=[]
 for i,z in enumerate(ints):
  tail=integralrow[z.end():ints[i+1].start() if i+1<len(ints) else len(integralrow)];diff=re.search(r'\\text\{d\}([uv])',tail);assert diff
  var=U if diff[1]=='u' else V;body=tail[:diff.start()].replace(r'\,','').strip();kernel=parse(body) if body else s.Integer(1)
  lo,hi=map(int,z.groups());assert (lo,hi)==((a,b) if var==U else (c,d));primitive=s.integrate(kernel,var);assert eq(s.diff(primitive,var),kernel)
  evaluated=s.simplify(primitive.subs(var,hi)-primitive.subs(var,lo));parts.append(evaluated);kernels.append(kernel);C['separate_definite_integrals']+=1
 assert eq(coefficient*kernels[0]*kernels[1],jac) and eq(coefficient*parts[0]*parts[1],A)
 endpoint=rhs[-2].split(r'\cdot');expected=([coefficient] if len(endpoint)==3 else [])+parts
 assert len(endpoint)==len(expected)
 for text,value in zip(endpoint,expected):assert eq(parse(text),value),(t,text,value);C['separate_endpoint_components']+=1
 assert eq(parse(rhs[-1]),A);C['final_areas']+=1
 ffield=q[':question/answer-fields'][0];vals=[parse(z[':answer/value']) for z in ffield[':answer-field/choices']];assert len(vals)==5
 for i,j in itertools.combinations(range(5),2):assert not eq(vals[i],vals[j]);C['criterion_pairs']+=1
 correct=next(z for z in ffield[':answer-field/choices'] if z[':answer/id']==ffield[':answer-field/correct'][1]);assert eq(parse(correct[':answer/value']),A);C['choice_values']+=5
 sid=next(q for q in O.values() if q[':db/id']==gen['source_id'])
 if t!='product_ratio':assert mask(sol)==mask(sid[':question/worked-solution']);C['source_prose_masks']+=1
 # Native rectangle edges determine both scales independently; colored boundary
 # labels/Delta are not confused with the longest continuous horizontal runs.
 path=re.findall(r'!\[\]\((.*?)\)',sol)[-1];im=np.asarray(Image.open(path).convert('RGB'));red=(im[:,:,0]>170)&(im[:,:,1]<90)&(im[:,:,2]<90);blue=(im[:,:,2]>170)&(im[:,:,0]<90)&(im[:,:,1]<90);black=im.max(2)<70
 def longest(mask):
  best=None
  for yy in np.where(mask.sum(1)>8)[0]:
   xx=np.where(mask[yy])[0];splits=np.split(xx,np.where(np.diff(xx)>4)[0]+1)
   for line in splits:
    candidate=(line[-1]-line[0],int(yy),int(line[0]),int(line[-1]))
    if best is None or candidate[0]>best[0]:best=candidate
  return best
 _,lower,left,right=longest(red);_,upper,bl,br=longest(blue);assert abs(left-bl)<3 and abs(right-br)<3;C['actual_rectangle_edges']+=4
 sx=(right-left)/(b-a);sy=(lower-upper)/(d-c);assert abs(sx-sy)<2
 predx=left-a*sx;predy=lower+c*sy;ox=int(np.argmax(black.sum(0)));oy=int(np.argmax(black.sum(1)));assert abs(ox-predx)<=3+2*abs(a)/(b-a) and abs(oy-predy)<=3+2*abs(c)/(d-c),(path,bounds,ox,oy,predx,predy)
 assert black[:,round(ox)-2:round(ox)+3].sum()>90 and black[round(oy)-2:round(oy)+3,:].sum()>90;C['actual_zero_axes']+=2
 if a<0<b:
  for yy in [upper+int((lower-upper)*.25),upper+int((lower-upper)*.75)]:assert black[yy-2:yy+3,round(ox)-2:round(ox)+3].any(),('hidden interior v-axis',path,bounds)
  C['actual_interior_zero_axes']+=1
 if c<0<d:
  for xx in [left+int((right-left)*.25),left+int((right-left)*.75)]:assert black[round(oy)-2:round(oy)+3,xx-2:xx+3].any(),('hidden interior u-axis',path,bounds)
  C['actual_interior_zero_axes']+=1
 C['records']+=1
out=dict(status='passed',source=S,readback=C,original_assets_full_resolution=8,script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest());(R/f'qa/{K}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
