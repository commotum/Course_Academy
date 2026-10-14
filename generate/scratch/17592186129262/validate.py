"""Independent displayed-math, source, native-grader and concurrent-render audit."""
import concurrent.futures, copy, hashlib, importlib.util, itertools, json, os, re, subprocess, sys
from pathlib import Path
import sympy as sp
from PIL import Image
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
parser_spec=importlib.util.spec_from_file_location('readback',g.ROOT.parent/'runs/current/domain-math-parser.py');read=importlib.util.module_from_spec(parser_spec);parser_spec.loader.exec_module(read)
# Parser consumes learner strings, independently of generation metadata.
def scalar(x):return read.scalar(x).subs({read.x:g.X,read.y:g.Y,read.u:g.U,read.v:g.V})
def eqvalue(e):
 l,r=e.split('=');return scalar(l)-scalar(r)
def equal(a,b):return sp.simplify(sp.expand_log(a-b,force=True))==0

def read_prompt(r):
 q=r['question'];t=r['generation']['template'];math=list(g.MATH.finditer(q[':question/problem']))[-1];s=math.group(1) if math.group(1) is not None else math.group(2)
 equations=s.strip().split(r',\,') if r',\,' in s else s.strip().split(', ')
 assert len(equations)==4
 # Read each supplied equation and pair it with independently read substitution.
 sol=q[':question/worked-solution'];blocks=list(g.MATH.finditer(sol));change=blocks[11].group(1).strip().split(r',\,');f=scalar(change[0].split('=')[1]);h=scalar(change[1].split('=')[1]);assert f.free_symbols|h.free_symbols=={g.X,g.Y}
 boundaries=[]
 for expr,trans in zip(equations,[f,f,h,h]):
  e=eqvalue(expr); # Ratio of equation differences must be nonzero along boundary.
  numerator=sp.together(e).as_numer_denom()[0]
  constant=sp.Symbol('constant')
  # Recover constants using an algebraic ideal, independent source coefficients.
  for proposed in range(-4,9):
   cand=sp.together(trans-proposed).as_numer_denom()[0]
   if cand==0:continue
   ratio=sp.cancel(numerator/cand)
   if ratio!=0 and not ratio.free_symbols:boundaries.append(proposed);break
  else:raise AssertionError(('cannot read boundary',expr,trans))
 a,b,c,d=boundaries
 assert a<b and c<d
 det=sp.simplify(sp.det(sp.Matrix([[sp.diff(f,g.X),sp.diff(f,g.Y)],[sp.diff(h,g.X),sp.diff(h,g.Y)]])))
 expected_det=g.TEMPLATES[t]['det'].subs({g.U:f,g.V:h});assert equal(det,expected_det)
 jac=sp.Abs(1/g.TEMPLATES[t]['det']);A=sp.integrate(jac,(g.U,a,b),(g.V,c,d))
 # Every displayed transformed boundary, including upper row, must match.
 for index,variable,coords in [(18,'u',(a,b)),(20,'v',(c,d))]:
  block=blocks[index].group(1);found=list(map(int,re.findall(variable+r'=(-?\d+)',block)));assert found==list(coords),(index,found,coords)
 region=blocks[22].group(1);found=list(map(int,re.findall(r'(-?\d+)\\le [uv]\\le (-?\d+)',region)[0]+re.findall(r'(-?\d+)\\le [uv]\\le (-?\d+)',region)[1]));assert found==boundaries
 # Formal derivative matrix is fixed by the source mask; verify every entry.
 matrix_block=blocks[25].group(1);matrices=re.findall(r'\|\\begin\{aligned\}(.*?)\\end\{aligned\}\|',matrix_block,re.S);assert len(matrices)==2
 entries=[x.strip() for row in matrices[1].split(r'\\') for x in row.split('&')];assert len(entries)==4
 assert all(equal(scalar(e),v) for e,v in zip(entries,[sp.diff(f,g.X),sp.diff(f,g.Y),sp.diff(h,g.X),sp.diff(h,g.Y)]))
 if t!='product_ratio':assert matrix_block==list(g.MATH.finditer(g.QUESTIONS[g.TEMPLATES[t]['sid']][':question/worked-solution']))[25].group(1),'lost determinant teaching stage'
 for stage in matrix_block.split(' & =')[3:]:
  stage=stage.split(r'\\')[0].split(r'\end{aligned}')[0].strip().rstrip('.')
  assert equal(scalar(stage).subs({g.U:f,g.V:h}),det),('distributed determinant stage',stage)
 # Reduced determinant and reciprocal are independently checked.
 lastdet=matrix_block.rsplit(' & =',1)[1].split(r'\end{aligned}')[0].rstrip('.')
 assert equal(scalar(lastdet).subs({g.U:f,g.V:h}),det)
 inverse=blocks[28].group(1).strip().split('=')[-1].rstrip('.')
 assert equal(scalar(inverse).subs({g.U:f,g.V:h}),1/det)
 # Last chain contains formal Jacobian, absolute-value, factored integration,
 # endpoint logs/differences, then collection. Read actual integral bounds.
 final=blocks[33].group(1);integral_bounds=re.findall(r'\{\\int \}_\{(-?\d+)\}\^\{(-?\d+)\}',final);assert integral_bounds==[(str(a),str(b)),(str(c),str(d))]
 endpoint=final.split(' & =')[-2].strip();assert equal(scalar(endpoint),A),(endpoint,A)
 collected=final.rsplit(' & =',1)[1].split(r'\end{aligned}')[0].strip();assert equal(scalar(collected),A)
 fields=q[':question/answer-fields'];assert len(fields)==1
 ffield=fields[0];choices=ffield[':answer-field/choices'];vals=[scalar(z[':answer/value']) for z in choices]
 assert len(vals)==5
 for i,j in itertools.combinations(range(5),2):assert not equal(vals[i],vals[j]),('criterion collision',i,j)
 correct=[z[':answer/id'] for z,v in zip(choices,vals) if equal(v,A)];assert correct==[ffield[':answer-field/correct'][1]]
 return boundaries

def format_check(r):
 assert set(r['knowledge_point'])=={'db_id','id','title'}
 for s in [r['question'][':question/problem'],r['question'][':question/worked-solution']]+[z[':answer/value'] for f in r['question'][':question/answer-fields'] for z in f[':answer-field/choices']]:
  assert all(ord(c)>=32 or c in '\n\t' for c in s),'control character'
  assert s.count('$')%2==0
  # TeX invisible group braces must balance; literal set glyphs are escaped.
  balance=0
  for m in re.finditer(r'(?<!\\)[{}]',s):
   balance+=1 if m.group()=='{' else -1;assert balance>=0
  assert balance==0

def source_fidelity():
 cases=[];total_choices=0;present_correct=0;solutions=0
 for t,cfg in g.TEMPLATES.items():
  r=g.generate(cfg['level'],template=t,parameters=cfg['anchor'],profile=f"source_{cfg['sid']}");raw=g.QUESTIONS[cfg['sid']];q=r['question']
  assert set(q)==set(raw)-{':db/id'} # exact omission parity, not assumed defaults
  assert q[':question/problem']==raw[':question/problem']
  assert q.get(':question/worked-solution')==raw.get(':question/worked-solution')
  solutions+=int(':question/worked-solution' in raw)
  assert len(q[':question/answer-fields'])==len(raw[':question/answer-fields'])
  for f,original in zip(q[':question/answer-fields'],raw[':question/answer-fields']):
   assert set(f)==set(original)-{':db/id'}
   assert f[':answer-field/key']==original[':answer-field/key'];assert f[':answer-field/type']==original[':answer-field/type'][':db/ident']
   assert [z[':answer/value'] for z in f[':answer-field/choices']]==[z[':answer/value'] for z in original[':answer-field/choices']]
   total_choices+=len(f[':answer-field/choices'])
   if ':answer-field/correct' in original:assert f[':answer-field/correct'][1]==original[':answer-field/correct'][':answer/id'];present_correct+=1
  cases.append({'source_id':cfg['sid'],'template':t,'difficulty':cfg['level'],'authored_level':cfg['level']=='easy','parameters':dict(zip('abcd',cfg['anchor'])),'bank_profile':f"source_{cfg['sid']}",'evidence_only':True})
 (HERE/'source-cases.json').write_text(json.dumps(cases,indent=2))
 return {'questions':len(cases),'complete_banks':len(cases),'fields_including_legacy':7,'choices':total_choices,'present_correct_designations':present_correct,'missing_correct_designations':2,'worked_solutions':solutions,'absent_worked_solutions':1,'key_presence_parity':True}

def raster_geometry(path,p,image_override=None):
 # Recover independently from native pixels: each edge, origin and both scales.
 im=image_override if image_override is not None else Image.open(path).convert('RGB');pixels=im.load();red={};blue={};blackcols={};blackrows={}
 for y in range(im.height):
  for x in range(im.width):
   rr,gg,bb=pixels[x,y]
   if rr>170 and gg<90 and bb<90:red.setdefault(y,[]).append(x)
   if bb>170 and rr<90 and gg<90:blue.setdefault(y,[]).append(x)
   if max(rr,gg,bb)<70:
    blackcols[x]=blackcols.get(x,0)+1;blackrows[y]=blackrows.get(y,0)+1
 def longest_run(xs):
  runs=[];start=previous=xs[0]
  for x in xs[1:]:
   if x>previous+4:runs.append((start,previous));start=x
   previous=x
  runs.append((start,previous));return max(runs,key=lambda z:z[1]-z[0])
 lower=max(red,key=lambda y:longest_run(red[y])[1]-longest_run(red[y])[0]);upper=max(blue,key=lambda y:longest_run(blue[y])[1]-longest_run(blue[y])[0]);left,right=longest_run(red[lower]);bl,br=longest_run(blue[upper]);assert abs(left-bl)<=2 and abs(right-br)<=2
 a,b,c,d=(p[k] for k in 'abcd');sx=(right-left)/(b-a);sy=(lower-upper)/(d-c)
 assert abs(sx-sy)<=2,'unequal rendered coordinate scales'
 x0=max(blackcols,key=blackcols.get);y0=max(blackrows,key=blackrows.get)
 assert abs((left-x0)-a*sy)<=3+2*abs(a)/(d-c) and abs((y0-lower)-c*sy)<=3+2*abs(c)/(d-c),('axes do not locate actual bounds',path,p,x0,y0,left,lower,sx,sy)
 assert any(y<upper-2 for y in blue) and any(y>lower+2 for y in red),'missing boundary labels'
 assert any(y>y0+3 for y in blackrows),'missing u bound tick labels'
 # Fill center has the actual pale-blue region color, not the white background.
 center=((left+right)//2,(lower+upper)//2);assert any(pixels[x,y][2]>pixels[x,y][0] and pixels[x,y][0]>180 for x in range(center[0]-3,center[0]+4) for y in range(center[1]-3,center[1]+4))
 axis_checks={}
 def dark_near(x,y):return any(max(pixels[xx,yy])<70 for xx in range(max(0,x-1),min(im.width,x+2)) for yy in range(max(0,y-1),min(im.height,y+2)))
 # Check actual continuous black strokes through fill, not only axes outside D.
 if c<0<d:
  probes=[(round(left+(right-left)*f),y0) for f in [.15,.3,.45,.6,.75,.9]]
  assert all(dark_near(x,y) for x,y in probes),'horizontal zero axis erased inside rectangle'
  axis_checks['horizontal_interior_black_probes']=probes
 if a<=0<=b:
  probes=[(x0,round(upper+(lower-upper)*f)) for f in [.15,.3,.45,.6,.75,.9]]
  assert all(dark_near(x,y) for x,y in probes),'vertical zero axis erased inside rectangle'
  axis_checks['vertical_interior_black_probes']=probes
 return {'origin_pixels':[x0,y0],'lower_edge':[left,lower,right,lower],'upper_edge':[left,upper,right,upper],'scales':[sx,sy],**axis_checks}

def run():
 report={'source_fidelity':source_fidelity(),'failures':[],'scope':'steps 3–7; no EDB writes'}
 records=[];coverage={};boundary_slots={};seen={};fixtures=[]
 for t,c in g.TEMPLATES.items():
  coverage[t]=0;boundary_slots[t]={k:set() for k in 'abcd'};seen[t]=set()
  for seed in range(30):
   r=g.generate(c['level'],seed,template=t);format_check(r);bounds=read_prompt(r)
   coverage[t]+=1;seen[t].add(r['generation']['mathematical_fingerprint'])
   for k,v in zip('abcd',bounds):boundary_slots[t][k].add(v)
   # Seed/order changes at fixed parameters preserve content identity.
   rr=g.generate(c['level'],seed+999,template=t,parameters=r['generation']['parameters'])
   assert r['generation']['content_identity']==rr['generation']['content_identity']
   if seed<2:records.append(r)
   f=r['question'][':question/answer-fields'][0]
   fixtures.append({'label':t+'-'+str(seed),'record':r,'checks':[{'submitted_answer_id':z[':answer/id'],'expected':'accepted' if z[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'actual radio grading; math checked independently'} for z in f[':answer-field/choices']]})
  assert len(seen[t])>=25
 # Mutations must fail actual displayed mathematics/form, even with metadata intact.
 original=records[0]
 mutations=[]
 for bad in [original['question'][':question/worked-solution'].replace('v=','v=9',1),original['question'][':question/worked-solution']+'\x0c']:
  mutant=copy.deepcopy(original);mutant['question'][':question/worked-solution']=bad
  try:format_check(mutant);read_prompt(mutant)
  except Exception:mutations.append('rejected')
  else:raise AssertionError('displayed mutation passed')
 # Algebraically equal but missing source distribution stage must also fail.
 mutant=copy.deepcopy(records[2]);mutant['question'][':question/worked-solution']=mutant['question'][':question/worked-solution'].replace(r' \\  & =-10+12','')
 try:read_prompt(mutant)
 except AssertionError:mutations.append('missing distribution rejected')
 else:raise AssertionError('missing source operation stage passed')
 # Scope guard and complete-bank collision tests on explicit inputs.
 invalid=0
 for level,t,params in [('easy','product_ratio',[0,2,1,2]),('moderate','linear_5_3',[-10,2,0,3]),('hard','square_product',[1,10,1,3]),('moderate','linear_4_3',[1,3,1,3])]:
  try:g.generate(level,template=t,parameters=params)
  except ValueError:invalid+=1
  else:raise AssertionError('invalid explicit inputs admitted')
 defaults={level:set() for level in ['easy','moderate','hard']}
 for level in defaults:
  for seed in range(35):defaults[level].add(g.generate(level,seed)['generation']['template'])
  assert defaults[level]=={t for t,c in g.TEMPLATES.items() if c['level']==level}
 # Fresh simultaneous renders with identical and distinct instances, unique inputs.
 commands=[]
 for p in [{'a':-2,'b':2,'c':0,'d':3},{'a':1,'b':4,'c':1,'d':3},{'a':-2,'b':2,'c':0,'d':3}]:
  code="import importlib.util; s=importlib.util.spec_from_file_location('g',"+repr(str(HERE.with_suffix('.py')))+");g=importlib.util.module_from_spec(s);s.loader.exec_module(g);g.render_plot("+repr(p)+",force=True)"
  commands.append([sys.executable,'-c',code])
 with concurrent.futures.ThreadPoolExecutor(3) as pool:
  for proc in pool.map(lambda cmd:subprocess.run(cmd,capture_output=True,text=True),commands):assert proc.returncode==0,proc.stderr
 pixel_checks=[]
 for r in records:
  ref=re.search(r'!\[\]\(([^)]+)\)',r['question'][':question/worked-solution']).group(1);path=Path(ref);side=json.loads(path.with_suffix('.json').read_text());im=Image.open(path)
  assert im.size==tuple(side['pixel_dimensions']);assert side['png_sha256']==hashlib.sha256(path.read_bytes()).hexdigest();assert side['bounds']==r['generation']['parameters'];pixel_checks.append(raster_geometry(path,side['bounds']))
 # Parent native finding: both interior zero axes must be visibly continuous.
 interior_axes=[];axis_mutations=[]
 for p in [{'a':0,'b':3,'c':-1,'d':3},{'a':-2,'b':2,'c':-1,'d':3},{'a':-2,'b':2,'c':-2,'d':2}]:
  path=Path(g.render_plot(p,force=True));geom=raster_geometry(path,p);side=json.loads(path.with_suffix('.json').read_text())
  assert side['renderer_version']=='rectangle-v4';assert side['draw_order']=={'fill':0,'zero_axes':1,'colored_edges':2,'labels':3}
  interior_axes.append({'path':str(path),'parameters':p,'png_sha256':side['png_sha256'],'geometry':geom})
  # Erase actual interior PNG pixels while preserving outside axes and all metadata.
  for axis in ['horizontal','vertical']:
   if axis=='vertical' and not p['a']<0<p['b']:continue
   bad=Image.open(path).convert('RGB');pix=bad.load();x0,y0=geom['origin_pixels'];left,lower,right,_=geom['lower_edge'];upper=geom['upper_edge'][1]
   if axis=='horizontal':
    for x in range(left+5,right-4):
     for y in range(y0-3,y0+4):pix[x,y]=(220,233,241)
   else:
    for y in range(upper+5,lower-4):
     for x in range(x0-3,x0+4):pix[x,y]=(220,233,241)
   try:raster_geometry(path,p,image_override=bad)
   except AssertionError as exc:axis_mutations.append({'axis':axis,'parameters':p,'rejected':True,'reason':str(exc)})
   else:raise AssertionError('erased interior zero axis passed raster regression')
 (HERE/'native-fixtures.json').write_text(json.dumps(fixtures,indent=2))
 subprocess.run([str(g.ROOT.parent/'runs/current/check-engine'),str(HERE/'native-fixtures.json'),str(HERE/'native-report.json')],check=True)
 report.update({'passed':True,'generated_displayed_math_checks':sum(coverage.values()),'families':coverage,'distinct_sampled_tasks':{t:len(v) for t,v in seen.items()},'slot_coverage':{t:{k:sorted(v) for k,v in row.items()} for t,row in boundary_slots.items()},'default_family_coverage':{k:sorted(v) for k,v in defaults.items()},'format_control_character_regression':mutations,'explicit_invalid_inputs_rejected':invalid,'concurrent_fresh_renders':3,'native_pixel_geometry':pixel_checks,'interior_zero_axis_geometry':interior_axes,'erased_interior_axis_regressions':axis_mutations,'generator_sha256':hashlib.sha256(HERE.with_suffix('.py').read_bytes()).hexdigest(),'renderer_version':'rectangle-v4','python':sys.version.split()[0],'sympy':sp.__version__,'native':json.loads((HERE/'native-report.json').read_text()),'native_provenance':{name:hashlib.sha256((g.ROOT.parent/'runs/current'/name).read_bytes()).hexdigest() for name in ['check-engine','check-engine.rs']}})
 (HERE/'review.json').write_text(json.dumps(records,indent=2,ensure_ascii=False));(HERE/'validation.json').write_text(json.dumps(report,indent=2,ensure_ascii=False))
 return report
if __name__=='__main__':
 try:report=run();print('PASS:',report['generated_displayed_math_checks'],'displayed instances; complete source replay; native fixtures')
 except Exception as exc:
  (HERE/'validation.json').write_text(json.dumps({'passed':False,'failure':repr(exc)},indent=2));raise
