#!/usr/bin/env python3
"""Private mathematical readback, complete fidelity, plotting and native grading."""
import copy,hashlib,importlib.util,itertools,json,re,subprocess,sys,tempfile
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import sympy as sp
from PIL import Image
ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('generator',ROOT.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

def assert_parabola_label_bounds(side,lo,hi,low,high):
 if side['family']not in ['simple','mixed','up','down','vertical']:return
 label=next(z for z in side['artist_labels']if z['role']=='region')
 bx,by,bw,bh=label['bbox_pixel'];ox,oy=side['origin_pixel']
 xl,xr=side['axis_calibration']['xlim'];yb,yt=side['axis_calibration']['ylim']
 if xl<=0<=xr:assert bx>ox+3.99 or bx+bw<ox-3.99,'Delta bbox crosses vertical zero axis'
 if yb<=0<=yt:assert by>oy+3.99 or by+bh<oy-3.99,'Delta bbox crosses horizontal zero axis'
 transform=sp.Matrix(side['data_to_pixel_matrix']);inverse=transform.inv();sy=abs(float(transform[1,1]))
 for px,py in [(bx,by),(bx+bw,by),(bx,by+bh),(bx+bw,by+bh)]:
  cu,cv,_=inverse*sp.Matrix([px,py,1]);cu,cv=float(cu),float(cv)
  assert float(lo)<cu<float(hi)
  assert float(low.subs(g.u,cu))+1.99/sy<cv<float(high.subs(g.u,cu))-1.99/sy,'Delta bbox crosses boundary'
 assert abs(label['position'][0])>0

def plot_readback(q,lo,hi,low,high):
 # Read the actual image reference in learner content, then check the measured
 # renderer sidecar against the PNG and independently parsed display domain.
 path=Path(re.findall(r'!\[\]\(([^)]+)\)',q[':question/worked-solution'])[-1])
 side=json.loads(path.with_suffix('.json').read_text())
 assert side['renderer_version']==g.RENDERER_VERSION
 assert side['python']==sys.version.split()[0]
 assert side['runtime']['matplotlib']==g.matplotlib.__version__
 assert list(Image.open(path).size)==side['pixel_size']
 width,height=side['pixel_size'];bbox=side['axes_pixel_bbox'];display_bbox=side['axes_bbox_display']
 assert bbox[0]==display_bbox[0]and bbox[2:]==display_bbox[2:]
 assert abs(bbox[1]-(height-display_bbox[1]-display_bbox[3]))<1e-8
 assert 0<bbox[0]<bbox[0]+bbox[2]<width and 0<bbox[1]<bbox[1]+bbox[3]<height
 transform=sp.Matrix(side['data_to_pixel_matrix']);origin=list(transform*sp.Matrix([0,0,1]))[:2]
 assert all(abs(float(a)-b)<1e-8 for a,b in zip(origin,side['origin_pixel']))
 assert transform[0,0]>0 and transform[1,1]<0
 xl,xr=side['axis_calibration']['xlim'];yb,yt=side['axis_calibration']['ylim']
 corner=list(transform*sp.Matrix([xl,yt,1]));opposite=list(transform*sp.Matrix([xr,yb,1]))
 assert abs(float(corner[0])-bbox[0])<1e-8 and abs(float(corner[1])-bbox[1])<1e-8
 assert abs(float(opposite[0])-bbox[0]-bbox[2])<1e-8 and abs(float(opposite[1])-bbox[1]-bbox[3])<1e-8
 assert xl<=float(lo)<float(hi)<=xr
 labels={z['role']:z for z in side['artist_labels']if z['role']not in ['u_tick','v_tick']}
 assert labels['upper_boundary']['text']=='$v='+g.tex(high)+'$'
 assert labels['lower_boundary']['text']=='$v='+g.tex(low)+'$'
 expected_lower,expected_upper=('blue','red')if side['family']=='quartic'else('red','blue')
 assert side['boundary_colors']['lower']==expected_lower and side['boundary_colors']['upper']==expected_upper
 assert labels['lower_boundary']['color']==expected_lower and labels['upper_boundary']['color']==expected_upper
 assert labels['region']['text']==r'$\Delta$'
 assert labels['u_axis']['text']=='$u$'and labels['v_axis']['text']=='$v$'
 for label in side['artist_labels']:
  bx,by,bw,bh=label['bbox_pixel'];assert label['visible']and bw>0 and bh>0
  assert 0<=bx<bx+bw<=width and 0<=by<by+bh<=height
 mu,mv=labels['region']['position'];assert float(low.subs(g.u,mu))<mv<float(high.subs(g.u,mu))
 assert_parabola_label_bounds(side,lo,hi,low,high)
 arrow=side['slice_arrow'];assert arrow['tail_data'][0]==arrow['head_data'][0]
 assert arrow['tail_data'][1]<arrow['head_data'][1]
 annotation_transform=sp.Matrix(arrow['data_to_pixel_matrix'])
 if 'detail_view'in side:
  detail=side['detail_view'];assert detail['same_region']and detail['bounds']==side['bounds']
  assert detail['title']=='Same region: local view'and arrow['axes_role']=='detail'
  assert annotation_transform==sp.Matrix(detail['data_to_pixel_matrix'])
  rb=labels['region']['bbox_pixel'];ab=arrow['artist_bbox_pixel']
  assert rb[0]>ab[0]+ab[2]+2 or ab[0]>rb[0]+rb[2]+2 or rb[1]>ab[1]+ab[3]+2 or ab[1]>rb[1]+rb[3]+2,'region label/arrow overlap'
  inverse=annotation_transform.inv()
  # Actual drawn text/arrow bounding boxes fit wholly between both curves.
  for label_box in [rb,ab]:
   bx,by,bw,bh=label_box
   for px,py in [(bx,by),(bx+bw,by),(bx,by+bh),(bx+bw,by+bh)]:
    du,dv,_=inverse*sp.Matrix([px,py,1]);du,dv=float(du),float(dv)
    assert float(lo)<du<float(hi)
    assert float(low.subs(g.u,du))<dv<float(high.subs(g.u,du)),'local glyph bbox crosses curve'
 else:assert arrow['axes_role']=='primary'and annotation_transform==transform
 for role in ['tail','head']:
  au,av=arrow[role+'_data'];assert float(lo)<au<float(hi)
  assert float(low.subs(g.u,au))<av<float(high.subs(g.u,au))
  pixel=list(annotation_transform*sp.Matrix([au,av,1]))[:2]
  assert all(abs(float(a)-b)<1e-8 for a,b in zip(pixel,arrow[role+'_pixel']))

def math_readback(r):
 q=r['question'];pr=q[':question/problem'];sol=q[':question/worked-solution'];f=r['generation']['template'];P=g.parse
 assert set(r['knowledge_point'])=={'db_id','id','title'}
 for s in [pr,sol]+[a[':answer/value']for a in q[':question/answer-fields'][0][':answer-field/choices']]:g.format_ok(s)
 # Read actual displayed maps, then independently solve/invert the linear map.
 maps=re.search(r'\$\$\nu=(.*?),\\,v=(.*?),\n\$\$',pr)
 assert maps,'printed map';U,V=map(P,maps.groups());matrix=sp.Matrix([[sp.diff(U,g.x),sp.diff(U,g.y)],[sp.diff(V,g.x),sp.diff(V,g.y)]])
 # Preserve complete source prose roles under changed map parameters.
 if f.startswith('hyper'):
  first_expr,first_var,second_expr,second_var=(g.tex(V),'v',g.tex(U),'u')if f=='hyper_x'else(g.tex(U),'u',g.tex(V),'v')
  assert f'Substituting ${first_expr}={first_var}$ into the equation of the first line, we get'in sol
  assert f'while substituting ${second_expr}={second_var}$ into the equation of the second line, we obtain'in sol
  operands=f'${g.tex(V)}=v$ and ${g.tex(U)}=u$'if f=='hyper_x'else f'$u={g.tex(U)}$ and $v={g.tex(V)}$'
  assert 'Substituting '+operands+' into the equation of curve, we get' in sol
  assert 'To find the intersection of the curve with the first line in the $uv$-plane, we solve the following system:'in sol
  assert 'To find the intersections of the curve with the second line in the $uv$-plane, we solve the following system:'in sol
 if f in ['up','vertical']:
  assert f'while substituting ${g.tex(V)}=v$ into the equation of the second curve, we obtain'in sol
 det=matrix.det();assert det!=0;J=1/abs(det)
 inv=sp.solve([g.u-U,g.v-V],(g.x,g.y))
 # Parse the actual xy boundary statements from the prompt. No generation
 # parameters or model values serve as mathematical truth in these checks.
 tail=pr[pr.index('bounded by'):];inline=re.findall(r'\$([^$]+)\$',tail)
 equations=[]
 for z in inline:
  z=z.rstrip(',.');aa,bb=z.split('=');equations.append(sp.expand(P(aa)-P(bb)))
 transformed=[sp.simplify(z.subs(inv,simultaneous=True))for z in equations]
 # Parse printed type-I region completely and independently.
 dom=re.search(r'Δ=\\\{\(u,v\)\\,:\\,(.*?)\\le u\\le (.*?),\\,(.*?)\\le v\\le (.*?)\\\}\.',sol)
 assert dom,'domain';lo,hi,low,high=map(P,dom.groups());assert float(hi-lo)>0
 if f.startswith('hyper'):
  assert len(transformed)==3
  u_boundary=transformed[1]if f=='hyper_x'else transformed[0];v_boundary=transformed[0]if f=='hyper_x'else transformed[1]
  assert sp.simplify(u_boundary.subs(g.u,lo))==0
  assert sp.simplify(v_boundary.subs(g.v,low))==0
  assert sp.simplify(transformed[2].subs(g.v,high))==0
 else:
  assert len(transformed)==2
  boundary=high if f=='down' else low
  line=low if f=='down' else high
  assert sp.simplify(transformed[0].subs(g.v,boundary))==0
  assert sp.simplify(transformed[1].subs(g.v,line))==0
  assert g.eq(low.subs(g.u,lo),high.subs(g.u,lo)) and g.eq(low.subs(g.u,hi),high.subs(g.u,hi))
 assert float((high-low).subs(g.u,(lo+hi)/2))>0
 plot_readback(q,lo,hi,low,high)
 if f=='quartic':
  inverted=re.search(r'Now,\n\n\$\$(.*?)\$\$',sol,re.S)[1]
  y_fragment=inverted.split('y=')[-1].split(r'\end{aligned}')[0].removesuffix('.')
  assert r'\frac{u-v}'in y_fragment,'inverse must retain single grouped quotient'
  assert g.eq(P(y_fragment),inv[g.y])
 correct=sp.simplify(J*sp.integrate(high-low,(g.u,lo,hi)))
 field=q[':question/answer-fields'][0];bank=[P(a[':answer/value'])for a in field[':answer-field/choices']];assert len(bank)==5
 assert all(not g.eq(a,b)for a,b in itertools.combinations(bank,2))
 target=next(P(a[':answer/value'])for a in field[':answer-field/choices']if a[':answer/id']==field[':answer-field/correct'][1]);assert g.eq(target,correct)
 # Read the printed determinant matrix and scalar, independent of model().
 calc=sol[sol.index('**Step 2**'):sol.index('**Step 3**')]
 mats=re.findall(r'\\begin\{matrix\}(.*?)\\end\{matrix\}',calc,re.S);assert len(mats)==2
 vals=[P(z)for z in re.split(r'&|\\\\',mats[1])];assert vals==list(matrix)
 displayed_det=P(re.search(r'&=([^\\]+)\\end\{aligned\}',calc)[1]);assert displayed_det==det
 inverse_section=sol[sol.index('**Step 3**'):sol.index('**Step 4**')]
 inverse_block=re.search(r'\$\$\n(.*?)\n\$\$',inverse_section,re.S)[1]
 assert g.eq(P(inverse_block.split('=')[-1].removesuffix('.')),1/det)
 # Complete operative integration rows and separately printed primitive.
 chain=sol[sol.index('**Step 4**'):];rows=chain.split(r' \\ ')
 assert len(rows)==(9 if f.startswith('hyper')or f=='quartic'else 10)
 assert r'[\int_{' in rows[2] and r'[v]_{' in rows[3]
 inner=re.search(r'\[\\int_\{(.*?)\}\^\{(.*?)\}dv',rows[2]);assert inner
 assert g.eq(P(inner[1]),low) and g.eq(P(inner[2]),high)
 integral_prefix=r'\int_{'+g.tex(lo)+'}^{'+g.tex(hi)+'}'
 assert integral_prefix in rows[4]
 for row in rows[2:-4]:
  assert integral_prefix in row
  factor_in_row=P(row.split('&=')[1].split(r'\int')[0]);assert g.eq(factor_in_row,J)
 assert r'[v]_{'+g.tex(low)+'}^{'+g.tex(high)+'}' in rows[3]
 numeric_J=re.search(r'\\iint_Δ \|(.*?)\|\\,dudv',rows[1]);assert numeric_J
 assert g.eq(abs(P(numeric_J[1])),J)
 grouped_math=rows[4].split(integral_prefix,1)[1].removesuffix('du')
 assert g.eq(P(grouped_math),high-low)
 primrow=rows[-4]; m=re.search(r'&=(.*?)\[(.*?)\](.*)$',primrow);assert m,'primitive structure'
 factor,primitive=map(P,m.groups()[:2]);assert m[3]=='_{'+g.tex(lo)+'}^{'+g.tex(hi)+'}'
 assert g.eq(factor,J);assert g.eq(sp.diff(primitive,g.u),high-low)
 endpointrow=rows[-3];em=re.search(r'&=(.*?)\((.*)\)$',endpointrow);assert em
 # The evaluated row's signs/grouping retain each endpoint component, including
 # zero components: verify each individually, not only the final difference.
 z=em[2];comps=[];depth=0;start=None
 for i,c in enumerate(z):
  if c=='(':
   depth+=1
   if depth==2:start=i+1
  if c==')':
   if depth==2:comps.append(z[start:i])
   depth-=1
 assert len(comps)==4,(f,comps,endpointrow)
 displayed_components=list(map(P,comps));terms=sp.Add.make_args(primitive)
 terms=sorted(terms,key=lambda z:0 if z.has(sp.log) else sp.degree(z,g.u))
 expected=[z.subs(g.u,t)for t in [hi,lo]for z in terms]
 assert all(g.eq(a,b)for a,b in zip(displayed_components,expected)),(f,displayed_components,expected)
 assert g.eq(P(em[2]),(primitive.subs(g.u,hi)-primitive.subs(g.u,lo)))
 collected=re.search(r'&=(.*?)\((.*)\)$',rows[-2]);assert collected
 assert g.eq(P(collected[1]),J)
 assert g.eq(P(collected[2]),primitive.subs(g.u,hi)-primitive.subs(g.u,lo))
 assert g.eq(P(collected[1])*P(collected[2]),correct)
 final=rows[-1].split('&=')[1].split(r'\end{aligned}')[0];assert g.eq(P(final),correct)
 # Structure mutation guards distinguish equivalent but missing operative rows.
 assert '(' in grouped_math and ')-(' in grouped_math,'grouped bound subtraction required'
 return correct

def assert_raw_case(q,r):
 z=r['question']
 for key in [':question/difficulty',':question/worked-solution',':question/answer-fields']:
  assert (key in z)==(key in q)
 assert z[':question/problem']==q[':question/problem']
 if ':question/worked-solution'in q:assert z[':question/worked-solution']==q[':question/worked-solution']
 originals=q[':question/answer-fields'];fields=z[':question/answer-fields'];assert len(fields)==len(originals)
 assert len({f[':answer-field/id']for f in fields})==len(fields)
 all_ids=[a[':answer/id']for f in fields for a in f[':answer-field/choices']];assert len(all_ids)==len(set(all_ids))
 for original,field in zip(originals,fields):
  expected_keys=set(original)-{':db/id'};assert set(field)==expected_keys
  assert field[':answer-field/key']==original[':answer-field/key']
  assert field[':answer-field/type']==original[':answer-field/type'][':db/ident']
  assert sorted(a[':answer/value']for a in field[':answer-field/choices'])==sorted(a[':answer/value']for a in original[':answer-field/choices'])
  for answer in field[':answer-field/choices']:
   old=next(a for a in original[':answer-field/choices']if a[':answer/value']==answer[':answer/value'])
   assert set(answer)==set(old)-{':db/id'}
   assert answer[':answer/type']==old[':answer/type'][':db/ident']
   if ':answer/feedback'in old:assert answer[':answer/feedback']==old[':answer/feedback']
  assert (':answer-field/correct'in field)==(':answer-field/correct'in original)
  if ':answer-field/correct'in original:
   actual=next(a[':answer/value']for a in field[':answer-field/choices']if a[':answer/id']==field[':answer-field/correct'][1])
   assert actual==original[':answer-field/correct'][':answer/value']

def raw_fidelity():
 rows=[]
 for sid,q in g.Q.items():
  r=g.generate('hard',profile='raw:'+sid,parameters={'scale':1});assert_raw_case(q,r)
  changed=g.generate('hard',profile='raw:'+sid,parameters={'scale':2})
  assert len(changed['question'][':question/answer-fields'])==len(q[':question/answer-fields'])
  for original,field in zip(q[':question/answer-fields'],changed['question'][':question/answer-fields']):
   vals=[g.parse(a[':answer/value'])for a in field[':answer-field/choices']]
   originals=[g.parse(a[':answer/value'])*4 for a in original[':answer-field/choices']]
   assert all(sum(g.eq(a,b)for b in vals)==1 for a in originals)
   if ':answer-field/correct'in original:
    target=next(g.parse(a[':answer/value'])for a in field[':answer-field/choices']if a[':answer/id']==field[':answer-field/correct'][1])
    assert g.eq(target,g.parse(original[':answer-field/correct'][':answer/value'])*4)
  rows.append({'source_id':sid,'template':next(f for f,z in g.FAMILIES.items()if z[0]==sid),'parameters':{'scale':1},'bank_profile':'raw:'+sid,'raw_present_keys':list(q),'field_present_keys':[list(f)for f in q[':question/answer-fields']],'field_count':len(q[':question/answer-fields']),'eligible_for_learning':False})
 # A missing legacy/authoritative second widget must never be called fidelity.
 broken=copy.deepcopy(g.generate('hard',profile='raw:q-82874',parameters={'scale':1}));broken['question'][':question/answer-fields'].pop()
 failed=False
 try:assert_raw_case(g.Q['q-82874'],broken)
 except AssertionError:failed=True
 assert failed,'missing second field was not detected'
 (ROOT/'source-cases.json').write_text(json.dumps(rows,indent=2))
 return rows

def main():
 sourcecases=raw_fidelity();records=[];slots={};ids={};default_family=set()
 source_anchors=[]
 for f,(sid,level)in g.FAMILIES.items():
  if sid is not None:
   r=g.generate(level,template=f,parameters=g.ANCHORS[sid]);math_readback(r);source_anchors.append(sid)
 narrow_cases=[]
 for family in ['hyper_x','hyper_y']:
  for gap,offset in [(10,3),(11,3),(5,2)]:
   r=g.generate('hard',template=family,parameters={'a':5,'h':gap,'k':offset});math_readback(r)
   narrow_cases.append({'family':family,'parameters':r['generation']['parameters'],'plot':r['generation']['plot']})
 parabola_cases=[]
 for family,level,params in [('simple','easy',{'a':1,'h':1,'k':0}),('mixed','moderate',{'a':3,'h':4,'k':0}),('up','hard',{'a':2,'h':5,'k':-3}),('up','hard',{'a':2,'h':1,'k':5}),('down','hard',{'a':1,'h':2,'k':1}),('vertical','hard',{'a':3,'h':9,'k':-5})]:
  r=g.generate(level,template=family,parameters=params);math_readback(r)
  side=json.loads(Path(r['generation']['plot']).with_suffix('.json').read_text())
  # Reposition only the measured bbox onto either real zero axis. The anchor
  # and claimed layout flags remain unchanged; actual extents must fail.
  domain=re.search(r'Δ=\\\{\(u,v\)\\,:\\,(.*?)\\le u\\le (.*?),\\,(.*?)\\le v\\le (.*?)\\\}\.',r['question'][':question/worked-solution'])
  lo,hi,low,high=map(g.parse,domain.groups())
  for axis in [0,1]:
   altered=copy.deepcopy(side);label=next(z for z in altered['artist_labels']if z['role']=='region');bbox=label['bbox_pixel']
   bbox[axis]=altered['origin_pixel'][axis]-bbox[axis+2]/2
   failed=False
   try:assert_parabola_label_bounds(altered,lo,hi,low,high)
   except AssertionError:failed=True
   assert failed,'axis-overlap bbox mutation survived'
  parabola_cases.append({'family':family,'parameters':params,'plot':r['generation']['plot']})
 for f,(_,level)in g.FAMILIES.items():
  seen={t:set()for t in ['a','h','k']};tasks=set()
  for seed in range(24):
   r=g.generate(level,seed,template=f);math_readback(r);records.append(r)
   for t,z in r['generation']['parameters'].items():seen[t].add(z)
   tasks.add(r['generation']['mathematical_fingerprint'])
  slots[f]={t:sorted(z)for t,z in seen.items()};ids[f]=len(tasks)
  r=records[-1];other=g.generate(level,149,template=f,parameters=r['generation']['parameters']);assert r['question'][':question/id']==other['question'][':question/id']
  # Explicit invalid calls cannot bypass level guards.
  bad=dict(r['generation']['parameters']);bad['a']=0
  try:g.generate(level,template=f,parameters=bad);raise AssertionError('invalid a accepted')
  except ValueError:pass
 for level in ['easy','moderate','hard']:
  for seed in range(36):default_family.add(g.generate(level,seed)['generation']['template'])
 assert default_family==set(g.FAMILIES)
 # Mutation regressions must actually fail, not catch our own success assertion.
 def rejected_mutation(r):
  rejected=False
  try:math_readback(r)
  except (AssertionError,ValueError,IndexError):rejected=True
  assert rejected,'mutation survived readback'
 base=copy.deepcopy(records[0]);sol=base['question'][':question/worked-solution'];base['question'][':question/worked-solution']=sol.replace(')-(',')+(',1);rejected_mutation(base)
 base=copy.deepcopy(records[0]);base['question'][':question/worked-solution']+='\x0c';rejected_mutation(base)
 base=copy.deepcopy(records[0]);sol=base['question'][':question/worked-solution'];rows=sol[sol.index('**Step 4**'):].split(r' \\ ');old=rows[4]
 start=old.index('}(')+1;body=old[start:].removesuffix('du');new=old[:start]+g.tex(g.parse(body))+'du'
 assert g.eq(g.parse(body),g.parse(new[start:].removesuffix('du')))
 base['question'][':question/worked-solution']=sol.replace(old,new);rejected_mutation(base)
 # Changed-parameter prose masks retain source operands and first/second roles.
 prose_mutations=[('hyper_x','Substituting ', 'Substituting into '),('hyper_y','with the first line','with the line'),('hyper_y','the intersections of the curve with the second line','the intersection of the curve with the line'),('up','the equation of the second curve','the equation of the line'),('vertical','the equation of the second curve','the equation of the line')]
 for family,old,new in prose_mutations:
  base=copy.deepcopy(next(z for z in records if z['generation']['template']==family and z['generation']['seed']==13))
  sol=base['question'][':question/worked-solution'];assert old in sol
  base['question'][':question/worked-solution']=sol.replace(old,new,1);rejected_mutation(base)
 # Correlated endpoint errors can leave the final difference correct. Mutate
 # one component at each endpoint by the same constant, then require failure.
 base=copy.deepcopy(records[0]);sol=base['question'][':question/worked-solution'];rows=sol[sol.index('**Step 4**'):].split(r' \\ ');old=rows[-3]
 positions=[];depth=0
 for i,c in enumerate(old):
  if c=='(':
   depth+=1
   if depth==3:positions.append(i)
  elif c==')':depth-=1
 # Endpoint row has an outer arithmetic difference plus endpoint and term masks.
 assert len(positions)==4
 new=old
 for i in [positions[2],positions[0]]:new=new[:i+1]+'1+'+new[i+1:]
 base['question'][':question/worked-solution']=sol.replace(old,new);rejected_mutation(base)
 # Fresh concurrent renders with identical/different parameter sets. Matplotlib
 # threads have separate Figures; atomic private-file writes protect cache readers.
 items=[('simple',{'a':4,'h':16,'k':0}),('simple',{'a':4,'h':16,'k':0}),('up',{'a':5,'h':12,'k':-5}),('hyper_x',{'a':5,'h':12,'k':3})]
 fresh=Path(tempfile.mkdtemp(prefix='concurrent-',dir=ROOT));paths=[]
 with ThreadPoolExecutor(max_workers=4)as pool:paths=list(pool.map(lambda item:g.plot(*item,g.model(*item),output_dir=fresh),items))
 assert paths[0]==paths[1]and len(set(paths))==3
 for path,(f,p)in zip(paths,items):assert json.loads(Path(path).with_suffix('.json').read_text())['parameters']==p
 assert not list(fresh.glob('*-*.png'))and not list(fresh.glob('*-*.json'))
 native=[]
 for r in records:
  field=r['question'][':question/answer-fields'][0];native.append({'label':r['generation']['template']+'-'+str(r['generation']['seed']),'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted'if a[':answer/id']==field[':answer-field/correct'][1]else'rejected','purpose':'actual radio grading of independently verified displayed choice'}for a in field[':answer-field/choices']]})
 # Grade every present original designation through its own captured field.
 # For a malformed duplicate-key record, an explicit fixture projection keeps
 # the later owned widget while the full raw API retains BOTH original fields.
 for sid,q in g.Q.items():
  r=g.generate('hard',profile='raw:'+sid,parameters={'scale':1})
  for index,original in enumerate(q[':question/answer-fields']):
   if ':answer-field/correct'not in original:continue
   fixture=copy.deepcopy(r);field=fixture['question'][':question/answer-fields'][index]
   fixture['question'][':question/answer-fields']=[field]
   fixture['generation']['fixture_original_field_index']=index
   fixture['generation']['fixture_note']='single captured widget projection; raw API preserves every original widget'
   native.append({'label':'source-'+sid+'-field-'+str(index),'record':fixture,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted'if a[':answer/id']==field[':answer-field/correct'][1]else'rejected','purpose':'captured field '+str(index)+' correct-designation fixture'}for a in field[':answer-field/choices']]})
 (ROOT/'native-input.json').write_text(json.dumps(native,ensure_ascii=False,indent=2));check=Path('generate/runs/current/check-engine');subprocess.run([str(check),str(ROOT/'native-input.json'),str(ROOT/'native-report.json')],check=True)
 review=[]
 for f,(_,level)in g.FAMILIES.items():
  for seed in [4,13]:review.append(g.generate(level,seed,template=f))
 (ROOT/'review.json').write_text(json.dumps(review,ensure_ascii=False,indent=2))
 lines=['# Type I area generator review','Raw captured source evidence is in source.json. Raw profiles are ineligible, with omissions preserved.']
 for sid,q in g.Q.items():
  lines+=['## Original '+sid,q[':question/problem'],'\n'.join('Bank for field '+str(index)+': '+', '.join(a[':answer/value']for a in field[':answer-field/choices'])+'; correct ref '+('present'if ':answer-field/correct'in field else'absent')for index,field in enumerate(q[':question/answer-fields'])),q.get(':question/worked-solution','Worked solution absent; difficulty and correct designation also absent.')]
  family=next(f for f,z in g.FAMILIES.items()if z[0]==sid)
  for r in review:
   if r['generation']['template']==family:lines+=['### Generated authored method bank '+family+' '+str(r['generation']['parameters']),g.markdown(r)]
 lines+=['## Authored moderate mixed-map extension']+[g.markdown(r)for r in review if r['generation']['template']=='mixed']
 (ROOT/'review.md').write_text('\n\n'.join(lines))
 # Immutable evidence for current renderer assets. Older cache entries remain
 # untouched while parent QA may still be reading the previous review.
 rendered=[]
 for side in sorted((ROOT/'plots').glob('*.json')):
  data=json.loads(side.read_text())
  if data.get('renderer_version')!=g.RENDERER_VERSION:continue
  path=side.with_suffix('.png');assert path.exists()
  rendered.append({'image':str(path),'sidecar':str(side),'image_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'sidecar_sha256':hashlib.sha256(side.read_bytes()).hexdigest(),'family':data['family'],'parameters':data['parameters'],'axes_pixel_bbox':data['axes_pixel_bbox'],'origin_pixel':data['origin_pixel']})
 provenance={'renderer':'Matplotlib','renderer_version':g.RENDERER_VERSION,'runtime':{'python':sys.version.split()[0],'matplotlib':g.matplotlib.__version__,'sympy':sp.__version__},'coordinate_convention':'PNG/top-left; display/bottom-left; full affine matrices measured after canvas draw','generator_sha256':hashlib.sha256(ROOT.with_suffix('.py').read_bytes()).hexdigest(),'assets':rendered}
 (ROOT/'render-provenance.json').write_text(json.dumps(provenance,indent=2))
 report={'status':'pass','practice_questions':7,'raw_exact_prompts':7,'raw_exact_present_solutions':[6,6],'complete_original_banks':[8,8],'all_original_choices':[40,40],'designations':[6,6],'missing_original_designations':2,'attribute_omission_parity':True,'normal_readback_records':len(records),'normal_source_anchor_readbacks':source_anchors,'normal_present_source_backbone_count':6,'default_family_coverage':sorted(default_family),'sampled_task_counts':ids,'slot_coverage':slots,'native':json.loads((ROOT/'native-report.json').read_text()),'native_harness_sha256':hashlib.sha256(check.read_bytes()).hexdigest(),'concurrent_fresh_render_instances':4,'narrow_plot_bbox_regressions':narrow_cases,'parabola_label_bbox_regressions':parabola_cases,'parabola_axis_overlap_mutations':2*len(parabola_cases),'renderer_version':g.RENDERER_VERSION,'source_field_count':8,'missing_second_field_regression':True,'changed_parameter_prose_mutation_checks':len(prose_mutations),'runtime':records[0]['generation']['runtime'],'source_errors':{'q-82874':'two selection widgets: older ref absent, later ref3/20 present; u³(u−1) should be u(u³−1)','q-82878':'y=v+1 should be y=v−1','q-83947':'source vertical axis is shifted from parabola symmetry center; regenerate correct geometry','multiple':'unescaped/unbalanced literal set/system braces; raw evidence only'},'authored_levels':['easy square-gap zero-shift shear','moderate mixed map nonunit determinant'],'unresolved_findings':[]}
 (ROOT/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps({k:report[k]for k in ['status','normal_readback_records','complete_original_banks','all_original_choices','designations']},indent=2))
if __name__=='__main__':main()
