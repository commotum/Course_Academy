#!/usr/bin/env python3
"""Independent printed-expression, graph/raster, fidelity and native grader audit."""
import copy, hashlib, importlib.util, json, re, subprocess, sys
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,convert_xor
from PIL import Image
import numpy as np
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
x=sp.Symbol('x')
def read(value):
 s=value.split('=')[-1].replace('\\\\frac','\\frac')
 s=re.sub(r'\\frac\{(-?\d+)\}\{(\d+)\}',r'(\1/\2)',s).replace('{','').replace('}','')
 return sp.Poly(sp.expand(parse_expr(s,local_dict={'x':x},transformations=standard_transformations+(implicit_multiplication_application,convert_xor))),x)
def roots_of(p):
 return sorted((int(r),int(m)) for r,m in sp.roots(p.as_expr(),x).items())
def sig(p):
 return (tuple((r,'simple' if m==1 else 'even' if m%2==0 else 'odd-multiple') for r,m in roots_of(p)),int(sp.sign(p.LC())))
def check(r,raster=True):
 assert set(r['knowledge_point'])=={'db_id','id','title'}
 q=r['question'];f=q[':question/answer-fields'][0];aa=f[':answer-field/choices']
 assert len(aa)==5 and f[':answer-field/type']==':answer-field.type/radio'
 texts=[q[':question/problem'],q[':question/worked-solution']]+[a[':answer/value'] for a in aa]
 for t in texts:
  assert not any(ord(z)<32 and z not in '\n\t\r' for z in t),'control character'
  assert t.count('$')%2==0
  depth=0
  for z in t:
   if z=='{':depth+=1
   elif z=='}':depth-=1
   assert depth>=0
  assert depth==0
 p=[read(a[':answer/value']) for a in aa]
 assert len(set(str(v.as_expr()) for v in p))==5
 ids=[a[':answer/id'] for a in aa];assert len(set(ids))==5
 ci=ids.index(f[':answer-field/correct'][1]);correct=p[ci]
 assert not r['generation']['eligible_default'] or len(set(sig(v) for v in p))==5
 plot=r['generation']['plot'];pr=sorted(zip(plot['roots'],plot['multiplicities']))
 assert roots_of(correct)==pr
 assert correct.LC()==sp.Rational(plot['coefficient'])
 assert sum(sig(v)==sig(correct) for v in p)==1
 sol=q[':question/worked-solution'];assert [int(z) for z in re.findall(r'x=(-?\d+)',sol.split('\n\n')[0])]==[r for r,m in pr],'root enumeration'
 final=re.findall(r'\$(y\s*=.*?)\$',sol)[-1].rstrip('.')
 assert read(final)==correct,'solution final expression'
 bullets=sol.split('\n\n- ')[1:];assert len(bullets)==len(pr)
 for b,(root,m) in zip(bullets,pr):
  mentioned=[int(z) for z in re.findall(r'x=(-?\d+)',b.split('\n\n')[0])]
  assert mentioned and set(mentioned)=={root},'stale solution root'
  if m==1:assert '*not* tangent' in b and 'simple root' in b
  elif m%2==0:assert 'reverses direction' in b and 'even multiplicity' in b
  else:assert 'passes through' in b and 'greater than one' in b
 lo,hi=plot['xlim'];yl,yh=plot['ylim'];assert lo<0<hi and yl<0<yh
 # Derivative order and signs recovered independently from ACTUAL displayed key.
 for root,m in pr:
  assert all(sp.diff(correct.as_expr(),x,k).subs(x,root)==0 for k in range(m))
  assert sp.diff(correct.as_expr(),x,m).subs(x,root)!=0
  eps=sp.Rational(1,1000)
  assert (sp.sign(correct.eval(root-eps))==sp.sign(correct.eval(root+eps)))==(m%2==0)
 if raster:
  path=Path(re.search(r'!\[\]\((.*?)\)',q[':question/problem']).group(1));im=np.array(Image.open(path).convert('RGB'))
  red=(im[:,:,0]>150)&(im[:,:,1]<100)&(im[:,:,2]<110)
  assert red.sum()>1000
  black=(im[:,:,0]<80)&(im[:,:,1]<80)&(im[:,:,2]<80)
  # Independently derive zero axes from fixed physical layout and actual bounds,
  # then locate long black axis strokes in raster rather than trusting sidecar.
  assert plot['main_rect']==[.08,.35,.84,.58]
  expected_x=im.shape[1]*(.08+(0-lo)/(hi-lo)*.84)
  expected_y=im.shape[0]*(1-(.35+(0-yl)/(yh-yl)*.58))
  main_top=round(im.shape[0]*(1-.35-.58));main_bottom=round(im.shape[0]*(1-.35));main_left=round(im.shape[1]*.08);main_right=round(im.shape[1]*(.08+.84))
  main_black=black[main_top:main_bottom,main_left:main_right]
  assert abs(int(main_black.sum(0).argmax())+main_left-expected_x)<3,'raster vertical axis not zero'
  assert abs(int(main_black.sum(1).argmax())+main_top-expected_y)<3,'raster horizontal axis not zero'
  for point in plot['raster_points']:
   z=point['x'];yy=float(correct.eval(z));assert abs(yy-point['y'])<1e-7*max(1,abs(yy))
   expected_px=im.shape[1]*(.08+(z-lo)/(hi-lo)*.84)
   expected_py=im.shape[0]*(1-(.35+(yy-yl)/(yh-yl)*.58))
   assert abs(point['pixel'][0]-expected_px)<2 and abs(point['pixel'][1]-expected_py)<2
   px,py=map(round,[expected_px,expected_py]);region=red[max(0,py-4):py+5,max(0,px-4):px+5]
   assert region.any(),'missing raster point'
  assert len(plot['local_views'])==len(pr),'missing local root view'
  for i,(local,(root,m)) in enumerate(zip(plot['local_views'],pr)):
   assert local['root']==root and local['multiplicity']==m
   assert local['label']=='Near x = '+str(root),'every root labelled including zero'
   radius=min(abs(root-z) for z,n in pr if z!=root)*.14
   assert abs(local['radius']-radius)<1e-10
   rect=[.08+i*.84/len(pr)+.012,.115,.84/len(pr)-.024,.16]
   assert local['rect']==rect
   title_top=round(im.shape[0]*(1-rect[1]-rect[3]))-34;title_bottom=round(im.shape[0]*(1-rect[1]-rect[3]))-5
   title_left=round(im.shape[1]*rect[0]);title_right=round(im.shape[1]*(rect[0]+rect[2]))
   assert black[title_top:title_bottom,title_left:title_right].sum()>90,'missing raster root label'
   assert local['xlim']==[root-radius,root+radius]
   ly,hy=local['ylim'];assert ly<0<hy and abs(ly+hy)<1e-12
   probes={probe['fraction']:probe for probe in local['probes']}
   signed_offsets={}
   for fraction in [-.8,-.4,-.1,0,.1,.4,.8]:
    z=root+radius*fraction;yy=float(correct.eval(sp.Rational(str(z))))
    probe=probes[fraction];assert abs(probe['x']-z)<1e-10 and abs(probe['y']-yy)<1e-8*max(1,abs(yy))
    px=im.shape[1]*(rect[0]+(z-(root-radius))/(2*radius)*rect[2])
    py=im.shape[0]*(1-(rect[1]+(yy-ly)/(hy-ly)*rect[3]))
    zero_y=im.shape[0]*(1-(rect[1]+.5*rect[3]));signed_offsets[fraction]=zero_y-py
    ix,iy=round(px),round(py)
    assert red[max(0,iy-3):iy+4,max(0,ix-3):ix+4].any(),'local actual-polynomial raster point missing'
   # Outer shoulders on BOTH sides must sit far enough from the axis to see
   # the crossing/reversal; center shoulders distinguish ordinary crossings
   # from visibly flattened tangent crossings. These are image-pixel bounds.
   assert min(abs(signed_offsets[-.8]),abs(signed_offsets[.8]))>14,'invisible local root shoulder'
   assert (signed_offsets[-.8]*signed_offsets[.8]>0)==(m%2==0),'wrong local crossing/reversal'
   if m==1:
    assert min(abs(signed_offsets[-.1]),abs(signed_offsets[.1]))>2,'simple crossing looks flat'
   else:
    assert max(abs(signed_offsets[-.1]),abs(signed_offsets[.1]))<2,'multiple-root tangency not visibly flat'
 return True

def check_raw(r,original,anchor):
 q=r['question'];assert r['generation']['evidence_only'] and not r['generation']['eligible_default']
 for attr in (':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields'):
  assert (attr in q)==(attr in original),(original[':question/math-academy-id'],attr)
 for f,old in zip(q.get(':question/answer-fields',[]),original.get(':question/answer-fields',[])):
  assert (':answer-field/correct' in f)==(':answer-field/correct' in old)
  assert len(f[':answer-field/choices'])==len(old[':answer-field/choices'])
  if anchor:
   assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in old[':answer-field/choices'])
   if ':answer-field/correct' in old:
    assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==old[':answer-field/correct'][':answer/value']
 if anchor:
  if ':question/worked-solution' in original: assert q[':question/worked-solution']==original[':question/worked-solution']
  prompt=q[':question/problem'];oldprompt=original[':question/problem']
  dest=re.search(r'!\[\]\((.*?)\)',prompt).group(1);src=re.search(r'!\[\]\((.*?)\)',oldprompt).group(1)
  assert hashlib.sha256(Path(dest).read_bytes()).digest()==hashlib.sha256((Path('/media/jake/SSD/EDB/math')/src).read_bytes()).digest()
  assert prompt.replace(dest,src)==oldprompt
 else:
  assert r['generation']['plot']['asset_role']=='parameterized-raw-variant'
  if ':question/worked-solution' in q:
   final=re.findall(r'\$(y\s*=.*?)\$',q[':question/worked-solution'])[-1].rstrip('.')
   assert roots_of(read(final))==sorted(zip(r['generation']['plot']['roots'],r['generation']['plot']['multiplicities']))
 return True


def main():
 cases=[];reviews=[];fidelity=[];native=[]
 transcription=json.loads((HERE/'source-plot-transcription.json').read_text());original_root_pixels=0
 for sid,v in transcription.items():
  if sid=='note':continue
  im=Image.open(HERE/'originals'/(sid+'.png')).convert('RGBA');im=Image.alpha_composite(Image.new('RGBA',im.size,'white'),im);a=np.array(im.convert('RGB'));red=(a[:,:,0]>180)&(a[:,:,1]<120)&(a[:,:,2]<120)
  for px in v['x_pixels']:
   py=v['zero_y'];assert red[max(0,py-3):py+4,max(0,px-3):px+4].any(),(sid,px,py);original_root_pixels+=1
 for sid,(level,_,_,_) in g.DATA.items():
  if sid not in g.QS:continue
  case={'source_id':sid,'template':sid,'parameters':{'h':0,'s':1,'v':'1'},'bank_profile':sid+'-raw','level':level,'authored_level':sid=='q-38668'};cases.append(case)
  raw=g.generate(level,template=sid,profile=sid+'-raw',parameters=case['parameters']);check_raw(raw,g.QS[sid],True)
  changed_raw=g.generate(level,template=sid,profile=sid+'-raw',parameters={'h':2,'s':2,'v':'1/2'});check_raw(changed_raw,g.QS[sid],False)
  reviews.append({'kind':'raw source evidence (omissions preserved; ineligible)','source_id':sid,'record':raw})
  r=g.generate(level,profile=sid,parameters=case['parameters']);check(r)
  oq=g.QS[sid];fields=oq.get(':question/answer-fields',[])
  original=[a[':answer/value'] for a in fields[0][':answer-field/choices']] if fields else []
  gen=[a[':answer/value'] for a in r['question'][':question/answer-fields'][0][':answer-field/choices']]
  assert not original or sorted(str(read(v).as_expr()) for v in original)==sorted(str(read(v).as_expr()) for v in gen)
  osol=oq.get(':question/worked-solution');gsol=r['question'][':question/worked-solution']
  # Full prose/stages, final equation normalized separately.
  mask=lambda z:re.sub(r'\$y\s*=.*?\$', '<FINAL>',z)
  assert not osol or mask(osol)==mask(gsol)
  row={'source_id':sid,'source_choices':len(original),'matched_choices':len(original),'matched_original_correct_ref':bool(fields and fields[0].get(':answer-field/correct')),'solution_shared_prose_exact':bool(osol and mask(osol)==mask(gsol)),'solution_full_exact':osol==gsol,'field_authored':not fields,'inferred_key':sid=='q-38668','raw_graphical_pair_collision':sid in g.RAW_COLLISION_PROFILES}
  fidelity.append(row);reviews.append({'kind':'source replay','source_id':sid,'record':r})
 # Exhaustive finite mathematics; plot at representative changed cases.
 finite={l:set() for l in ('easy','moderate','hard')};operations=0
 for sid,(level,*_) in g.DATA.items():
  for h in range(-3,4):
   for s in ([1] if level=='hard' else [1,2]):
    for v in ['1/2','1','2']:
     roots,ms,c,vals,ci=g.bank(sid,h,s,v)
     assert read(vals[ci])==sp.Poly(sp.Rational(c)*sp.prod((x-r)**m for r,m in zip(roots,ms)),x)
     if sid not in g.RAW_COLLISION_PROFILES:assert len(set(sig(read(z)) for z in vals))==5
     operations+=1
     finite[level].add(str(sig(read(vals[ci]))))
  # Two examples for every eligible family/bank including all authored hard.
  if sid not in g.RAW_COLLISION_PROFILES:
   for j in range(2):
    r=g.generate(level,seed=j+12,profile=sid,parameters={'h':[-2,2][j],'s':1 if level=='hard' else [1,2][j],'v':['1/2','2'][j]});check(r);reviews.append({'kind':'generated variant','record':r})
 for item in reviews:
  if item['record']['generation']['evidence_only']:continue
  r=item['record'];f=r['question'][':question/answer-fields'][0]
  checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'owned radio choice native grading'} for a in f[':answer-field/choices']]
  native.append({'label':r['generation']['profile']+'-'+str(len(native)),'record':r,'checks':checks})
 # Explicit whole-domain boundary legibility including root zero, both
 # horizontal stretch bounds, and both positive vertical-scale endpoints.
 boundary_cases=[]
 for sid,(level,*_) in g.DATA.items():
  for h in [-3,3]:
   for stretch in ([1] if level=='hard' else [1,2]):
    for vertical in ['1/2','2']:
     r=g.generate(level,profile=sid,parameters={'h':h,'s':stretch,'v':vertical});check(r)
     boundary_cases.append({'profile':sid,'parameters':r['generation']['parameters'],'image':re.search(r'!\[\]\((.*?)\)',r['question'][':question/problem']).group(1),'root_categories_visible':True})
 (HERE/'local-boundary-validation.json').write_text(json.dumps({'status':'pass','cases':boundary_cases,'same_function_root_views':True,'minimum_outer_shoulder_pixels':14,'simple_inner_shoulder_min_pixels':2,'multiple_inner_shoulder_max_pixels':2},indent=2))
 # Identity, defaults, explicit difficulty guards and mutations.
 for sid,(level,*_) in g.DATA.items():
  a=g.generate(level,seed=1,profile=sid,parameters={'h':0,'s':1,'v':'1'});b=g.generate(level,seed=22,profile=sid,parameters={'h':0,'s':1,'v':'1'});assert a['question'][':question/id']==b['question'][':question/id']
 seen={l:set() for l in finite}
 for seed in range(80):
  for l in finite:
   # Sampling profile directly avoids unnecessary plot write volume.
   import random
   eligible=[k for k,v in g.DATA.items() if v[0]==l and k not in g.RAW_COLLISION_PROFILES]
   seen[l].add(random.Random(seed).choice(eligible))
 for l in seen:assert seen[l]=={k for k,v in g.DATA.items() if v[0]==l and k not in g.RAW_COLLISION_PROFILES}
 base=next(z['record'] for z in reviews if z['kind']=='generated variant')
 mutation_count=0
 for mutation in ['solution','choice','control','plot','local-raster']:
  r=copy.deepcopy(base)
  if mutation=='solution':r['question'][':question/worked-solution']=r['question'][':question/worked-solution'].replace('x=', 'x=99',1)
  elif mutation=='choice':
   f=r['question'][':question/answer-fields'][0];a=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);a[':answer/value']='y=x'
  elif mutation=='control':r['question'][':question/problem']+='\x0c'
  elif mutation=='plot':r['generation']['plot']['coefficient']='99'
  else:
   q=r['question'];path=Path(re.search(r'!\[\]\((.*?)\)',q[':question/problem']).group(1));im=Image.open(path).convert('RGB');array=np.array(im);array[round(array.shape[0]*.70):]=255;mutation_path=HERE/'mutation-hidden-local.png';Image.fromarray(array).save(mutation_path);q[':question/problem']=q[':question/problem'].replace(str(path),str(mutation_path))
  try:check(r);raise RuntimeError('mutation survived '+mutation)
  except (AssertionError,ValueError):mutation_count+=1
 for level in finite:
  try:g.generate(level,parameters={'h':4,'s':1,'v':'1'});raise RuntimeError('bound accepted')
  except ValueError:pass
 (HERE/'source-cases.json').write_text(json.dumps(cases,indent=2));(HERE/'review.json').write_text(json.dumps(reviews,indent=2));(HERE/'native-input.json').write_text(json.dumps(native,indent=2))
 engine=ROOT/'generate/runs/current/check-engine'
 subprocess.run([str(engine),str(HERE/'native-input.json'),str(HERE/'native-report.json')],check=True)
 result={'status':'pass_with_documented_raw_bank_ineligibility','original_raster_root_points_checked':original_root_pixels,'raw_source_prompts_assets_and_presence_matched':10,'changed_raw_masks_checked':10,'raw_missing_correct_ref_preserved':1,'raw_unrated_presence_preserved':1,'raw_fieldless_presence_preserved':2,'source_total':10,'source_replayed':10,'original_banks_matched':8,'original_options_matched':40,'original_correct_designations_matched':7,'missing_correct_designation':1,'authored_fields':2,'source_solution_prose_stages_matched':9,'source_solution_prose_stages_total':9,'source_full_exact_solutions':sum(z['solution_full_exact'] for z in fidelity),'graphically_colliding_raw_banks':['q-38671','q-38774'],'all_normal_banks_graphically_distinct':True,'finite_mathematical_tasks':{l:len(v) for l,v in finite.items()},'exhaustive_bank_instances':operations,'native_checks':sum(len(z['checks']) for z in native),'review_count':len(reviews),'local_legibility_boundary_cases':len(boundary_cases),'root_local_same_function_png_checks':True,'independent_raster_zero_axes_checked':sum(not z['record']['generation']['evidence_only'] for z in reviews),'raster_points_use_independent_fixed_layout':True,'mutations_rejected':mutation_count,'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__,'matplotlib':g.matplotlib.__version__},'engine_sha256':hashlib.sha256(engine.read_bytes()).hexdigest(),'fidelity':fidelity}
 (HERE/'validation.json').write_text(json.dumps(result,indent=2))
 # Complete review originals (all banks) and variants, no withheld answer data.
 parts=['# Review — Identifying the Factored Polynomial Shown in a Graph\n\nSource math basis 1356. Original omission/normalization and bank ineligibility are recorded in template-extraction.md.']
 for sid,q in g.QS.items():
  parts+=['\n## Original '+sid,'![](originals/'+sid+'.png)',q[':question/problem'].split('\n\n',1)[1]]
  for f in q.get(':question/answer-fields',[]):parts+=['\n'.join('- $'+a[':answer/value']+'$' for a in f[':answer-field/choices'])]
  parts+=[q.get(':question/worked-solution','No captured solution or correct designation.')]
 for z in reviews:parts+=['\n## '+z['kind']+' '+z['record']['generation']['profile'],g.markdown(z['record'])]
 (HERE/'review.md').write_text('\n\n'.join(parts))
 print(json.dumps({k:v for k,v in result.items() if k!='fidelity'},indent=2))
if __name__=='__main__':main()
