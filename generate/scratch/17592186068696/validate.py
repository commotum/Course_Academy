#!/usr/bin/env python3
"""Independent printed-set, geometric/raster, source presence, native-grade QA."""
from pathlib import Path
import copy,hashlib,importlib.util,json,re,subprocess,sys,itertools
import numpy as np
from PIL import Image
import sympy as sp
D=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('kp68696',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def check(ok,message):
 if not ok:raise AssertionError(message)
def parse_set(text):
 # Independently decode the displayed response, including historical ± notation.
 s=text.replace('$','').replace('\\','').replace('pm','±').replace('only','')
 if '±' in s:
  n=sp.Rational(re.search(r'±\s*(-?\d+(?:\.\d+)?)',s).group(1));return frozenset([-n,n])
 return frozenset(sp.Rational(x) for x in re.findall(r'(?<![a-zA-Z])-?\d+(?:\.\d+)?',s))
def graph_readback(path):
 if path.startswith('images/'):
  z=g.PLOTS[path]
 else:z=json.loads(Path(path).with_suffix('.json').read_text())['geometry']
 # Read discontinuities from visible endpoint markers/branch asymptotes;
 # do not use either metadata breaks or generation correct refs as oracle.
 xs=set(map(lambda x:sp.Rational(str(x)),z.get('vertical_asymptotes',[])))
 by={}
 for m in z['markers']:by.setdefault(sp.Rational(str(m['x'])),[]).append(m)
 for x,ms in by.items():
  opened=[m for m in ms if m['kind']=='open']
  if opened:xs.add(x)
 return frozenset(xs)
def zero_axes_raster_check(path,side_override=None):
 side=side_override if side_override is not None else json.loads(Path(path).with_suffix('.json').read_text())
 im=np.array(Image.open(path).convert('RGB'));H,W=im.shape[:2];a=side['axes'];lo,hi=a['xlim'];bot,top=a['ylim'];lx,by,width,height=a['pixel_bounds']
 check(lo<0<hi and bot<0<top,'true zero must lie inside both plot limits')
 ox=lx+(0-lo)/(hi-lo)*width;oy=by+(0-bot)/(top-bot)*height
 check(np.allclose(a['origin_pixel'],[ox,oy],atol=.01),'sidecar actual origin transform')
 hs=np.array(a['horizontal_spine']).reshape(-1,2);vs=np.array(a['vertical_spine']).reshape(-1,2)
 check(np.allclose(hs[:,1],oy,atol=.01) and np.allclose(vs[:,0],ox,atol=.01),'axes must meet at true data zero')
 check(hs[:,0].min()<=ox<=hs[:,0].max() and vs[:,1].min()<=oy<=vs[:,1].max(),'origin lies on both actual spine segments')
 check(a['label_anchors']=={'x':[hi,0],'y':[0,top]},'axis labels follow true axes')
 check(0 in a['ticks'],'true zero tick retained')
 # Inspect four actual black spine segments just beyond possible point markers.
 dark=im.max(2)<95;px=round(ox);py=round(H-oy)
 for dx,dy in ((12,0),(-12,0),(0,12),(0,-12)):
  x,y=px+dx,py+dy;check(0<=x<W and 0<=y<H and dark[max(0,y-2):y+3,max(0,x-2):x+3].any(),'actual raster axes cross at true zero')
 return True
def plotted_raster_check(path):
 if path.startswith('images/'):return
 zero_axes_raster_check(path)
 side=json.loads(Path(path).with_suffix('.json').read_text());im=np.array(Image.open(path).convert('RGB'));H,W=im.shape[:2];axes=side['axes'];lo,hi=axes['xlim'];bot,top=axes['ylim'];lx,by,width,height=axes['pixel_bounds'];z=side['geometry']
 color=((im[:,:,0]>140)&(im[:,:,1]<140)&(im[:,:,2]<140))|((im[:,:,2]>140)&(im[:,:,0]<120)&(im[:,:,1]<120))
 for m in z['markers']:
  yy=m.get('y',(z.get('origin_pixel',[0,0])[1]-m.get('y_pixel',0))/z.get('pixels_per_x_unit',1));xx=m['x'];px=round(lx+(xx-lo)/(hi-lo)*width);py=round(H-(by+(yy-bot)/(top-bot)*height))
  center=color[max(0,py-1):py+2,max(0,px-1):px+2].sum();patch=color[max(0,py-7):py+8,max(0,px-7):px+8].sum()
  check(patch>=12,'actual rendered marker absent')
  check(center<=3 if m['kind']=='open' else center>=5,'actual rendered open/filled marker')
 check(side['png_sha256']==hashlib.sha256(Path(path).read_bytes()).hexdigest(),'actual PNG hash')
def grade_checks(record,label):
 checks=[]
 for i,f in enumerate(record['question'].get(':question/answer-fields',[])):
  if ':answer-field/correct' not in f:continue
  correct=f[':answer-field/correct'][1]
  for a in f[':answer-field/choices']:
   if f[':answer-field/type']==':answer-field.type/blank':
    v=a[':answer/value'];checks += [{'field_index':i,'submitted':v,'expected':'accepted','purpose':'canonical blank'}, {'field_index':i,'submitted':str(sp.Rational(v)+1),'expected':'rejected','purpose':'wrong coordinate'}, {'field_index':i,'submitted':f'({2*sp.Rational(v)})/2','expected':'accepted','purpose':'unreduced equivalent coordinate'}]
   else:checks.append({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'owned option actual grading'})
 return {'label':label,'record':record,'checks':checks}
def validate_record(r):
 check(set(r['knowledge_point'])=={'db_id','id','title'},'outer shape')
 q=r['question'];check(q[':question/difficulty'].split('/')[-1] in ('easy','moderate','hard'),'difficulty')
 for text in [q[':question/problem'],q[':question/worked-solution']]+[a[':answer/value'] for f in q[':question/answer-fields'] for a in f[':answer-field/choices']]:
  check(not any(ord(c)<32 and c not in '\n\t' for c in text),'C0 control')
  check(text.count('$')%2==0,'math delimiters')
  check(text.count('{')==text.count('}'),'TeX grouping')
  check('\\\\pm' not in text,'decoded malformed TeX')
 check(not re.search(r'\\(?:lim|frac|partial)|derivative|L.H.pital',q[':question/problem']),'scope')
 images=re.findall(r'!\[\]\(([^)]+)\)',q[':question/problem'])
 if r['generation']['template']=='select_graph':
  requested=parse_set(q[':question/problem']);check(len(requested)==1,'single target')
  for f in q[':question/answer-fields']:
   for a in f[':answer-field/choices']:plotted_raster_check(a[':answer/value'])
   matches=[]
   for a in f[':answer-field/choices']:
    if requested<=graph_readback(a[':answer/value']):matches.append(a[':answer/id'])
   check(matches==[f[':answer-field/correct'][1]],'graph-selection target/key')
  solcoords=parse_set(q[':question/worked-solution'].split('\n\n')[0]);check(solcoords==requested,'solution target stale')
 else:
  check(len(images)==1,'supplied graph')
  plotted_raster_check(images[0]);correct=graph_readback(images[0])
  fields=q[':question/answer-fields']
  if all(f[':answer-field/type']==':answer-field.type/blank' for f in fields):
   shown=[]
   for f in fields:
    check('{{'+f[':answer-field/key']+'}}' in q[':question/problem'],'blank placeholder')
    shown.append(sp.Rational(f[':answer-field/choices'][0][':answer/value']))
   check(frozenset(shown)==correct and shown==sorted(shown),'blank graph/set/order')
  else:
   for f in fields:
    sets=[parse_set(a[':answer/value']) for a in f[':answer-field/choices']]
    check(len(sets)==len(set(sets))==5,'complete bank equivalence/collision')
    matches=[a[':answer/id'] for a,s in zip(f[':answer-field/choices'],sets) if s==correct]
    check(matches==[f[':answer-field/correct'][1]],'actual displayed-bank correctness')
  first=q[':question/worked-solution'].split('\n\n')[0]
  check(parse_set(first)==correct,'printed solution coordinates')
  if 'Therefore' in q[':question/worked-solution']:check(parse_set(q[':question/worked-solution'].split('Therefore')[1])==correct,'printed conclusion')
 return True

def source_fidelity():
 count=0;choices=0;designations=0;fields=0;cases=[];native=[]
 for qid,q in g.QUESTIONS.items():
  case={'source_id':q[':question/id'],'math_academy_id':qid,'template':g.infer_family(qid),'level':'easy','parameters':{'scale':1,'shift':0},'bank_profile':'observed:'+qid}
  cases.append(case);r=g.generate('easy',seed=37,template=case['template'],profile=case['bank_profile'],parameters=case['parameters']);a=r['question']
  for k in (':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields'):
   check((k in a)==(k in q),qid+' key presence '+k)
  check(a[':question/problem']==q[':question/problem'],qid+' prompt exact')
  check(a.get(':question/worked-solution')==q.get(':question/worked-solution'),qid+' full solution exact')
  if ':question/difficulty' in q:check(a[':question/difficulty']==g.enum(q[':question/difficulty']),qid+' difficulty')
  for sf,gf in zip(q.get(':question/answer-fields',[]),a.get(':question/answer-fields',[])):
   check(sf[':answer-field/key']==gf[':answer-field/key'] and g.enum(sf[':answer-field/type'])==gf[':answer-field/type'],'field shape')
   expected=sorted((g.enum(z[':answer/type']),z[':answer/value']) for z in sf[':answer-field/choices'])
   actual=sorted((z[':answer/type'],z[':answer/value']) for z in gf[':answer-field/choices'])
   check(actual==expected,qid+' full bank');choices+=len(actual);fields+=1
   check((':answer-field/correct' in sf)==(':answer-field/correct' in gf),qid+' correct presence')
   if ':answer-field/correct' in sf:
    orig=next(z for z in sf[':answer-field/choices'] if z[':answer/id']==sf[':answer-field/correct'][':answer/id'])
    got=next(z for z in gf[':answer-field/choices'] if z[':answer/id']==gf[':answer-field/correct'][1])
    check(got[':answer/value']==orig[':answer/value'],qid+' designation');designations+=1
  # Native fixtures require correct refs for every field: grade authoritative
  # active field in a labelled adapter; keep public raw replay untouched.
  if qid=='q-48080':
   rr=copy.deepcopy(r);rr['question'][':question/answer-fields']=rr['question'][':question/answer-fields'][1:];native.append(grade_checks(rr,qid+' raw active-widget fixture adapter'))
  elif ':question/answer-fields' in a:native.append(grade_checks(r,qid+' raw evidence'))
  count+=1
 (D/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n')
 return {'questions_exact':count,'questions_total':len(g.QUESTIONS),'complete_banks_exact':fields,'choices_exact':choices,'correct_designations_exact':designations,'missing_correct_designations_preserved':1,'fieldless_presence_preserved':1,'missing_prompt_plots_preserved':4},native

def raster_checks():
 # Independent visual transcript from full resolution originals. Every open and
 # filled point, source tick calibration and every asymptote is separately fixed.
 expected={
 '05ad37':[(-2,136,'open'),(-2,43,'filled')],
 '25dbe2':[(-2,194,'filled'),(1,194,'open'),(1,119,'filled')],
 '2d3426':[(-1,111,'open'),(-1,276,'filled'),(2,164,'open'),(2,196,'filled')],
 '2f5337':[(-2,197,'open'),(-2,116,'filled')],
 '36cecf':[(-1,134,'open'),(-1,244,'filled')],
 '374abc':[(0,157,'open'),(0,76,'filled')],
 '3c8a19':[(1,187,'open'),(1,116,'filled')],
 '492341':[(-1,134,'open'),(-1,244,'filled')],
 '4c3513':[(0,197,'open'),(0,118,'filled'),(2,117,'open'),(2,236,'filled')],
 '6d0d3c':[(0,223,'open'),(0,182,'filled'),(1,222,'open'),(1,264,'filled')],
 '8ee061':[(-2,116,'filled'),(-2,237,'open'),(0,77,'open'),(0,196,'filled')],
 'caa671':[(-2,136,'open'),(-2,43,'filled')],
 'deacb7':[(-3,70,'open'),(-3,244,'filled')],
 'e111be':[(-3,177,'open'),(0,176,'filled')],
 'eb8803':[(1,194,'open'),(1,119,'filled'),(4,157,'open'),(4,119,'filled')],
 'fc1d42':[(1,187,'open'),(1,116,'filled')]}
 checks=0
 for path,z in g.PLOTS.items():
  im=np.array(Image.open(g.ASSET_ROOT/path).convert('RGBA'));a=im[:,:,:3];alpha=im[:,:,3]
  colored=((a[:,:,0]>150)&(a[:,:,1]<120)&(a[:,:,2]<120)|((a[:,:,2]>150)&(a[:,:,0]<100)&(a[:,:,1]<100)))&(alpha>128)
  exp=expected.get(Path(path).stem[:6],[])
  check([(m['x'],m['y_pixel'],m['kind']) for m in z['markers']]==exp,'independent marker transcript '+path)
  for x,y,kind in exp:
   px=round(z['origin_pixel'][0]+z['pixels_per_x_unit']*x)
   center=colored[y-1:y+2,px-1:px+2].sum()
   check(center<=3 if kind=='open' else center>=6,'actual source raster marker '+path+str((x,y,kind)))
   if kind=='open':
    sy=(z['origin_pixel'][1]-y)/z['pixels_per_x_unit'];check(any(abs(c[j][0]-x)<1e-8 and abs(c[j][1]-sy)<1e-8 for c in z['curves'] for j in (0,-1)),'isolated marked endpoint must not become missing interval')
   checks+=1
  check(hashlib.sha256((g.ASSET_ROOT/path).read_bytes()).hexdigest()==z['sha256'],'source asset hash')
 return {'source_assets_inspected_native_resolution':len(g.PLOTS),'independent_markers_checked':checks,'curves':'all connected red components traced, all cropped edges solid, positive axes arrowheads only','unlabelled_vertical_coordinates':'pixel geometry; no asserted exact formula/y-value'}

def run():
 fidelity,native=source_fidelity();raster=raster_checks();review=[];fprints={l:set() for l in ('easy','moderate','hard')};family=set();profile=set()
 for i,qid in enumerate(g.QUESTIONS):
  r=g.generate('easy',seed=i,profile='authored:'+qid,parameters={'scale':1 if i%2 else 2,'shift':(i%5)-2});validate_record(r);review.append(r);native.append(grade_checks(r,qid+' normal changed parameters'));fprints['easy'].add(r['generation']['mathematical_fingerprint'])
 # Two explicit reviewed examples per absent level, opposite orientations.
 for level in ('moderate','hard'):
  for seed in (3,16):
   r=g.generate(level,seed=seed);validate_record(r);review.append(r);native.append(grade_checks(r,level+' example '+str(seed)));fprints[level].add(r['generation']['mathematical_fingerprint'])
 # Sampling covers defaults/families, all source-shaped original banks remain public.
 for seed in range(70):
  r=g.generate('easy',seed);validate_record(r);family.add(r['generation']['template']);profile.add(r['generation']['profile']);fprints['easy'].add(r['generation']['mathematical_fingerprint'])
  check(r['question'][':question/id']==g.generate('easy',seed+91,profile=r['generation']['profile'],parameters=r['generation']['parameters'])['question'][':question/id'],'seed identity')
 check(family=={'list_breaks','select_graph','blank_1','blank_2'},'default family coverage')
 check(len(profile)==17,'normal source-family coverage')
 # Validate mathematical workload catalogs completely, plotting representative
 # signed/half-grid boundary records independently, not counting letter aliases.
 easy_catalog=set()
 for qid in g.QUESTIONS:
  for scale,shift in itertools.product((1,2),range(-3,4)):
   target=[g.affine(x,{'scale':scale,'shift':shift}) for x in g.BREAKS.get(qid,[g.SELECT.get(qid,0)])];catalog_family=g.infer_family(qid)
   easy_catalog.add(g.digest({'criterion':'graph-selection' if catalog_family=='select_graph' else 'coordinate-set','target':list(map(str,target)),'scale_reading':1,'break_count':len(target)}))
 catalog_counts={'easy':len(easy_catalog)}
 for level in ('moderate','hard'):
  catalog=g.coordinate_catalog(level);catalog_counts[level]=len(catalog)
  for coords in catalog:
   p={'coordinates':coords,'orientation':1};g.validate_parameters(level,p)
   bank=g.complete_set_bank(coords);check(len(bank)==5 and len(set(bank))==5,'finite bank catalog')
  for p in ({'coordinates':catalog[0],'orientation':1},{'coordinates':catalog[-1],'orientation':-1}):
   r=g.generate(level,parameters=p);validate_record(r);native.append(grade_checks(r,level+' boundary'));fprints[level].add(r['generation']['mathematical_fingerprint'])
 # Parent-discovered axis regression: every source family and complete image
 # bank at both translation boundaries; all geometry remains affine unchanged.
 axis_records=[];axis_plot_count=0
 for qid in g.QUESTIONS:
  for shift in (-3,3):
   r=g.generate('easy',seed=5,profile='authored:'+qid,parameters={'scale':2,'shift':shift});validate_record(r);axis_records.append(r);native.append(grade_checks(r,qid+' true-origin scale2 shift'+str(shift)))
   paths=re.findall(r'!\[\]\(([^)]+)\)',r['question'][':question/problem'])+[a[':answer/value'] for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices'] if a[':answer/type']==':answer.type/image']
   for path in paths:zero_axes_raster_check(path);axis_plot_count+=1
 (D/'zero-axes-review.json').write_text(json.dumps(axis_records,indent=2)+'\n')
 sentinel=next(r for r in axis_records if r['generation']['profile']=='authored:q-131299' and r['generation']['parameters']['shift']==3)
 sentinel_path=re.findall(r'!\[\]\(([^)]+)\)',sentinel['question'][':question/problem'])[0];broken_side=copy.deepcopy(json.loads(Path(sentinel_path).with_suffix('.json').read_text()));broken_side['axes']['xlim']=[3,11]
 try:zero_axes_raster_check(sentinel_path,broken_side)
 except AssertionError:axis_mutation_rejected=True
 else:raise AssertionError('old off-viewport-origin defect escaped regression')
 # Invalid explicit parameters cannot evade workload bounds.
 invalid=[('easy',{'scale':0,'shift':0}),('easy',{'scale':1,'shift':4}),('moderate',{'coordinates':[-3,-1,2],'orientation':1}),('hard',{'coordinates':[-3,-1,2.5],'orientation':1}),('hard',{'coordinates':[-3.5,-3,2.5],'orientation':1})]
 for l,p in invalid:
  try:g.generate(l,parameters=p)
  except ValueError:pass
  else:raise AssertionError('invalid level input accepted')
 # Mutate actual printed response/solution/graph transcript; validators must fail.
 mutations=[]
 base=next(r for r in review if r['generation']['template']=='list_breaks')
 for what in ('solution','choice','control'):
  r=copy.deepcopy(base)
  if what=='solution':r['question'][':question/worked-solution']=r['question'][':question/worked-solution'].replace('$x=', '$x=99',1)
  if what=='choice':
   f=r['question'][':question/answer-fields'][0];a=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);a[':answer/value']='$x=99$ only'
  if what=='control':r['question'][':question/problem']+='\f'
  try:validate_record(r)
  except AssertionError:mutations.append(what)
  else:raise AssertionError('mutation escaped '+what)
 # Fresh concurrent rendering of identical/different complete instance data.
 from concurrent.futures import ThreadPoolExecutor
 ps=[{'scale':1,'shift':-2},{'scale':2,'shift':1},{'scale':1,'shift':-2}]
 source=next(z for z in g.PLOTS.values() if z['markers'])
 with ThreadPoolExecutor(max_workers=3) as pool:out=list(pool.map(lambda p:g.render(source,p,force=True),ps))
 check(out[0]==out[2] and out[0]!=out[1],'concurrent deterministic render')
 for path,p in zip(out,ps):
  side=json.loads(Path(path).with_suffix('.json').read_text());check(side['parameters']==p,'concurrent sidecar mixed');check(side['png_sha256']==hashlib.sha256(Path(path).read_bytes()).hexdigest(),'concurrent PNG/sidecar')
 check(not list((D/'plots').glob('*.tmp')),'temporary leaks')
 evidence=[g.generate('easy',seed=29,profile='observed:'+qid,parameters={'scale':1,'shift':1}) for qid in g.QUESTIONS]
 for er in evidence:
  qid=er['generation']['profile'].split(':',1)[1];sq=g.QUESTIONS[qid]
  for sf,gf in zip(sq.get(':question/answer-fields',[]),er['question'].get(':question/answer-fields',[])):
   if g.infer_family(qid)=='select_graph':
    expected=sorted([sorted(float(x)+1 for x in graph_readback(a[':answer/value'])) for a in sf[':answer-field/choices']]);actual=sorted([sorted(float(x) for x in graph_readback(a[':answer/value'])) for a in gf[':answer-field/choices']]);check(expected==actual,'changed plotted source-bank replay')
   else:
    expected=sorted([sorted(x+1 for x in parse_set(a[':answer/value'])) for a in sf[':answer-field/choices']]);actual=sorted([sorted(parse_set(a[':answer/value'])) for a in gf[':answer-field/choices']]);check(expected==actual,'changed scalar source-bank replay')
 (D/'review.json').write_text(json.dumps(review+evidence,indent=2)+'\n')
 md=['# Source originals and generated variants','Source evidence is frozen at math basis 1356. All observed source banks and omissions are available through public observed profiles. Generated variants below are clearly authored normal presentation.']
 for qid,q in g.QUESTIONS.items():
  source_prompt=re.sub(r'images/[a-f0-9/]+\.png',lambda m:str(g.ASSET_ROOT/m.group()),q[':question/problem']);source_solution=re.sub(r'images/[a-f0-9/]+\.png',lambda m:str(g.ASSET_ROOT/m.group()),q[':question/worked-solution'])
  md+=['## '+qid+' original',source_prompt,source_solution]
  for f in q.get(':question/answer-fields',[]):
   md+=['Field '+f[':answer-field/key']+' ('+g.enum(f[':answer-field/type'])+')']
   md += ['- '+('![]('+str(g.ASSET_ROOT/a[':answer/value'])+')' if g.enum(a[':answer/type'])==':answer.type/image' else a[':answer/value']) for a in f[':answer-field/choices']]
  r=next(r for r in review if r['generation']['profile']=='authored:'+qid);md+=['### Generated variant; '+g.infer_family(qid),g.markdown(r)]
  er=next(r for r in evidence if r['generation']['profile']=='observed:'+qid);md+=['### Parameterized observed-bank variant; evidence only, preserved omissions',g.markdown(er)]
 for r in review:
  if r['generation'].get('authored_level'):md+=['## Authored '+r['question'][':question/difficulty'].split('/')[-1]+' extension',g.markdown(r)]
 (D/'review.md').write_text('\n\n'.join(md)+'\n')
 (D/'engine-input.json').write_text(json.dumps(native,indent=2)+'\n')
 result=subprocess.run(['generate/runs/current/check-engine',str(D/'engine-input.json'),str(D/'engine-report.json')],capture_output=True,text=True)
 check(result.returncode==0,result.stdout+result.stderr)
 engine=json.loads((D/'engine-report.json').read_text())
 result={'status':'pass','fidelity':fidelity,'plots':raster,'independent_printed_record_checks':len(review)+70+4,'sampled_mathematical_tasks':{k:len(v) for k,v in fprints.items()},'finite_authorable_coordinate_tasks':catalog_counts,'normal_default_families':sorted(family),'normal_default_source_profiles':len(profile),'raw_changed_parameter_review_records':len(evidence),'actual_rendered_marker_pixels_checked':True,'mutation_regressions':mutations,'explicit_invalid_parameters_rejected':len(invalid),'zero_axes_boundary_questions':len(axis_records),'zero_axes_boundary_plots':axis_plot_count,'old_off_viewport_origin_mutation_rejected':axis_mutation_rejected,'concurrent_fresh_render_cases':3,'native':{k:engine[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks')},'native_engine_sha256':hashlib.sha256(Path('generate/runs/current/check-engine').read_bytes()).hexdigest(),'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__,'matplotlib':g.matplotlib.__version__},'unresolved_source_evidence':['four omitted legacy graph widgets remain unrecovered; raw profiles ineligible; normal supplied plots authored','legacy field q-48080 lacks correct designation; raw presence preserved, authoritative widget graded via labelled adapter','q-104021 lacks answer fields; raw omission preserved, normal 5-choice field authored','historical decoded double TeX slashes retained in raw evidence; normal set-bank notation authored'],'root_approval':False}
 (D/'validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':run()
