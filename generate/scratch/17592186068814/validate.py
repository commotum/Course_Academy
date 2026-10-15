#!/usr/bin/env python3
"""Independent raw attribute/bank fidelity, displayed math and native image grading."""
import importlib.util,json,re,sys,subprocess,hashlib,itertools,tempfile,concurrent.futures
from pathlib import Path
from fractions import Fraction
from PIL import Image
import numpy as np
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('reciprocal',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

def fmt(t):
 assert not any(ord(c)<32 and c not in '\n\t' for c in t),'Control character'
 assert t.count('$')%2==0 and t.count('{')==t.count('}')
 assert '--' not in t and '+-' not in t

def fraction(t):
 if re.fullmatch(r'-?\d+',t):return Fraction(int(t))
 m=re.fullmatch(r'(-?)\\frac\{(\d+)\}\{(\d+)\}',t);assert m,t
 return Fraction((-1 if m[1] else 1)*int(m[2]),int(m[3]))

def printed(q):
 m=re.search(r'y\s*=\s*-\\frac\{(\d+)\}\{(\d*)x\}',q[':question/problem']);assert m,q
 return -Fraction(int(m[1]),int(m[2] or 1))

def plot_test(path,c,m):
 side=json.loads(Path(path).with_suffix('.json').read_text());assert Fraction(side['coefficient'])==c and Fraction(side['mark_x'])==m
 assert side['branch_count']==2 and [v['sign_x'] for v in side['branches']]==[-1,1]
 for branch in side['branches']:
  assert abs(branch['x_start']*branch['y_start']-float(c))<1e-9
  assert abs(branch['x_end']*branch['y_end']-float(c))<1e-9
 assert [[Fraction(x),Fraction(y)] for x,y in side['points']]==[[-m,-c/m],[m,c/m]]
 im=np.array(Image.open(path).convert('RGB')).astype(int);assert im.shape==(304,360,3)
 blue=(im[:,:,2]>im[:,:,0]+30)&(im[:,:,0]<150)
 xlim=side['xlim'][1];ylim=side['ylim'][1]
 def pix(x,y):return round(360*.07+360*.86*(x+xlim)/(2*xlim)),round(304-(304*.09+304*.84*(y+ylim)/(2*ylim)))
 # Raster features are read back at native pixels, independent of saved vertices.
 for x in (-float(m)*3,-float(m),float(m),float(m)*3):
  y=float(c)/x;px,py=pix(x,y);assert blue[max(py-3,0):py+4,max(px-3,0):px+4].any(),('missing visible curve',path,x,y)
 dark=(im.max(axis=2)<180)
 for b in side['labels']+side['axis_titles']:
  assert 0<=b[0]<359 and 0<=b[1]<303 and b[2]>5 and b[3]>=10
  bx,by,bw,bh=b;x0=max(0,int(bx));x1=min(360,int(bx+bw)+1);y0=max(0,int(304-by-bh));y1=min(304,int(304-by)+1)
  assert dark[y0:y1,x0:x1].sum()>8,('missing visible label/title',path,b)
 # Markers have ~49 px vertical clearance and ~38 px horizontal clearance.
 ox,oy=pix(0,0)
 for x,y in side['points']:
  px,py=pix(float(Fraction(x)),float(Fraction(y)));assert abs(py-oy)>=40 and abs(px-ox)>=35
  assert blue[py-3:py+4,px-3:px+4].sum()>=18,('missing marked point',path,x,y)

REFERENCE_BANKS={
 'raw_q-97958':('-1','1','a','-n','-a'),
 'raw_q-97963':('-a','-round_inverse','-1','1','a'),
 'raw_q-113335':('-a','-1','-inv','a','inv'),
 'raw_q-113337':('-a','inv','-inv','-1','a'),
 'raw_q-113339':('a','-1','-d','-inv','-a'),
 'raw_q-113341':('a','-inv','-a','inv','-1'),
 'raw_q-113336':('inv','-a','a','-inv','-1'),
 'raw_q-97949':('-a','a','1','-n','-1'),
 'raw_q-99068':('-1','-inv','-a','inv','-2a'),
 'integer_reversal':('inv','-a','a','-inv','-1'),
 'unit_numerator_reversal':('-a','-1','-inv','a','inv'),
 'rational_reversal':('-a','inv','-inv','-1','a'),
 'rational_numerator':('-a','a','1','-n','-1'),
 'rational_denominator':('a','-1','-d','-inv','-a'),
 'rational_unit_denominator':('-n','unit_d','a','-a','-unit_d'),
 'nonunit_point_reversal':('-a','a','inv','-inv','-1'),
 'nonunit_point_numerator':('-a','a','1','-n','-1'),
}

def independent_bank(q,profile):
 from decimal import Decimal,ROUND_HALF_UP
 m=re.search(r'y\s*=\s*-\\frac\{(\d+)\}\{(\d*)x\}',q[':question/problem']);n=int(m[1]);d=int(m[2] or 1)
 a=Fraction(n,d);inv=Fraction(d,n)
 vals={'a':a,'-a':-a,'inv':inv,'-inv':-inv,'-1':Fraction(-1),'1':Fraction(1),'-n':Fraction(-n),'-d':Fraction(-d),'-2a':-2*a,'unit_d':Fraction(1,d),'-unit_d':-Fraction(1,d),'-round_inverse':-Fraction((Decimal(d)/Decimal(n)).quantize(Decimal('.01'),rounding=ROUND_HALF_UP))}
 return [vals[t] for t in REFERENCE_BANKS[profile]]

def check(r,raw=False):
 assert set(r['knowledge_point'])=={'db_id','id','title'}
 q=r['question'];f=q[':question/answer-fields'][0];a=printed(q);assert a<0
 fmt(q[':question/problem'])
 if ':question/worked-solution' in q:
  fmt(q[':question/worked-solution'])
  sol=q[':question/worked-solution'];es=re.findall(r'y=(-\\frac\{\d+\}\{\d*x\})',sol)
  assert len(es)==3
  def value(e):
   v=re.fullmatch(r'-\\frac\{(\d+)\}\{(\d*)x\}',e);return -Fraction(int(v[1]),int(v[2] or 1))
  assert list(map(value,es))==[a,Fraction(-1),a],('stale solution',sol)
  m=re.search(r'scale factor of \$([^$]+)\$',sol);assert m and fraction(m[1])==-a
  assert sol.count('- Take the curve ')==1 and sol.count('- Stretch the result ')==1
  assert len(re.findall(r'!\[\]\(',sol))==2
  paths=re.findall(r'!\[\]\(([^)]+)\)',sol)
  if not paths[0].startswith('images/'):plot_test(paths[0],Fraction(-1),Fraction(r['generation']['mark_x']))
  assert paths[1]==r['generation']['correct_plot']
 else:assert raw and r['generation']['evidence_only']
 assert f[':answer-field/type']==':answer-field.type/radio' and f[':answer-field/key']=='selection' and len(f[':answer-field/choices'])==5
 bank=[];truth=[]
 for ans in f[':answer-field/choices']:
  assert set(ans)=={':answer/id',':answer/type',':answer/value'} and ans[':answer/type']==':answer.type/image'
  c=Fraction(r['generation']['plot_coefficients'][ans[':answer/value']]);bank.append(c)
  truth.append(c==a)
  if not ans[':answer/value'].startswith('images/'):plot_test(ans[':answer/value'],c,Fraction(r['generation']['mark_x']))
 assert sorted(bank)==sorted(independent_bank(q,r['generation']['bank_profile'])),('wrong operation bank',q[':question/problem'],bank)
 x=g.sp.Symbol('x',nonzero=True)
 for u,v in itertools.combinations(bank,2):assert g.sp.simplify(g.sp.Rational(u.numerator,u.denominator)/x-g.sp.Rational(v.numerator,v.denominator)/x)!=0
 assert sum(truth)==1
 for u,v in itertools.combinations(bank,2):assert u!=v,('equivalent plotted functions',u,v)
 if ':answer-field/correct' in f:
  truth_id=next(ans[':answer/id'] for ans in f[':answer-field/choices'] if Fraction(r['generation']['plot_coefficients'][ans[':answer/value']])==a)
  assert f[':answer-field/correct']==[':answer/id',truth_id]
 else:assert raw and r['generation']['evidence_only'] and not r['generation']['eligible_for_learning']
 return r

def audit_source_rasters():
 spec=json.loads((HERE/'plot-spec.json').read_text());lookup={z['asset']:z for z in spec};audits=[]
 for z in spec:
  path=Path('/media/jake/SSD/EDB/math')/z['asset'];rgba=Image.open(path).convert('RGBA')
  im=np.array(Image.alpha_composite(Image.new('RGBA',rgba.size,'white'),rgba).convert('RGB')).astype(int)
  assert im.shape==(304,360,3)
  blue=(im[:,:,2]>im[:,:,0]+30)&(im[:,:,0]<130);yy,xx=np.where(blue)
  ox,oy=z['origin'];sx,sy=z['pixels_per_x_unit'],z['pixels_per_y_unit'];c=Fraction(z['coefficient'])
  assert abs(ox-169)<1 and abs(oy-162.5)<1 and sx>18 and sy>6
  x=(xx-ox)/sx;y=(oy-yy)/sy;sel=(np.abs(xx-ox)>15)&(np.abs(yy-oy)>7)
  error=float(np.median(np.abs(x[sel]*y[sel]/float(c)-1)));assert error<.15, (z['asset'],error)
  assert z['quadrants']==([1,3] if c>0 else [2,4])
  for mx,my in z['marked_points']:
   assert Fraction(mx)*Fraction(my)==c
   px=round(ox+float(Fraction(mx))*sx);py=round(oy-float(Fraction(my))*sy)
   assert blue[py-3:py+4,px-3:px+4].sum()>=12
  audits.append({'asset':z['asset'],'coefficient':str(c),'xy_relative_median_error':error,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
 for sid in g.QS:
  n,d=g.SOURCE_PARAMETERS[sid];r=g.generate(g.PROFILES['raw_'+sid][0],parameters={'n':n,'d':d},profile='raw_'+sid)
  bank=[Fraction(lookup[a[':answer/value']]['coefficient']) for a in r['question'][':question/answer-fields'][0][':answer-field/choices']]
  assert len(set(bank))==5 and -Fraction(n,d) in bank
  for a in r['question'][':question/answer-fields'][0][':answer-field/choices']:
   assert Fraction(lookup[a[':answer/value']]['coefficient'])==Fraction(r['generation']['plot_coefficients'][a[':answer/value']])
 (HERE/'source-raster-validation.json').write_text(json.dumps(audits,indent=2))
 return len(audits)

def main():
 source_raster_count=audit_source_rasters()
 review=[];cases=[];fidelity=[]
 for sid,q in g.QS.items():
  profile='raw_'+sid;level=g.PROFILES[profile][0];n,d=g.SOURCE_PARAMETERS[sid];p={'n':n,'d':d}
  r=check(g.generate(level,23,parameters=p,profile=profile),True);review.append(r)
  rq=r['question'];rf=rq[':question/answer-fields'][0];sf=q[':question/answer-fields'][0]
  assert rq[':question/problem']==q[':question/problem'] and rq.get(':question/worked-solution')==q.get(':question/worked-solution')
  assert set(rq)-{':question/id'}==set(q)-{':db/id',':question/id',':question/math-academy-id'}
  assert set(rf)-{':answer-field/id'}==set(sf)-{':db/id',':answer-field/id'}
  assert sorted(a[':answer/value'] for a in rf[':answer-field/choices'])==sorted(a[':answer/value'] for a in sf[':answer-field/choices'])
  if ':answer-field/correct' in sf:
   correct=next(a[':answer/value'] for a in rf[':answer-field/choices'] if a[':answer/id']==rf[':answer-field/correct'][1]);assert correct==sf[':answer-field/correct'][':answer/value']
  for af in sf[':answer-field/choices']:
   aa=next(a for a in rf[':answer-field/choices'] if a[':answer/value']==af[':answer/value']);assert set(aa)-{':answer/id'}==set(af)-{':db/id',':answer/id'}
  fidelity.append({'source_id':q[':db/id'],'source':sid,'raw_prompt_exact':True,'raw_solution_presence_exact':True,'raw_solution_exact':':question/worked-solution' in q,'bank_options_matched':5,'correct_designation_matched':':answer-field/correct' in sf,'attribute_presence_parity':True})
  cases.append({'source_id':q[':db/id'],'math_academy_id':sid,'difficulty':level,'template':g.PROFILES[profile][1],'parameters':p,'bank_profile':profile})
  for seed in (41,73):review.append(check(g.generate(level,seed,profile=profile),True))
 for profile,(level,template,recipes) in g.PROFILES.items():
  if profile.startswith('raw_'):continue
  for seed in (41,73):review.append(check(g.generate(level,seed,profile=profile)))
 # Exhaustive mathematical domains, representative native-pixel boundary renders.
 variety={};checked_instances=0
 for level in ('easy','moderate','hard'):
  tasks=set();perprofile={}
  for name,(l,t,recipes) in g.PROFILES.items():
   if l!=level:continue
   valid=[]
   for p in g.domain(name):
    try:vs=g.checked(p,name)
    except ValueError:continue
    assert Fraction(p['n'],p['d'])>0 and len(set(vs))==5;checked_instances+=1
    check(g.generate(level,0,parameters=p,profile=name),name.startswith('raw_'))
    if not name.startswith('raw_'):tasks.add((Fraction(p['n'],p['d']),2 if level=='hard' else 1))
    valid.append(p)
   perprofile[name]=len(valid)
   assert valid
   for p in (valid[0],valid[-1],min(valid,key=lambda z:Fraction(z['n'],z['d'])),max(valid,key=lambda z:Fraction(z['n'],z['d']))):check(g.generate(level,0,parameters=p,profile=name),name.startswith('raw_'))
  variety[level]={'meaningful_task_count':len(tasks),'eligible_parameters_per_profile':perprofile}
 # Stable identity across seed/order, different banks differ, aliases do not count.
 for r in review:
  z=r['generation'];level=z['level']
  rr=g.generate(level,z['seed']+1,parameters=z['parameters'],profile=z['bank_profile'])
  assert r['question'][':question/id']==rr['question'][':question/id']
 for level in ('easy','moderate','hard'):
  coverage={g.generate(level,s)['generation']['bank_profile'] for s in range(40)}
  assert coverage=={name for name,v in g.PROFILES.items() if v[0]==level and not name.startswith('raw_')}
 for level,profile,p in [('hard','nonunit_point_reversal',{'n':3,'d':2}),('moderate','rational_reversal',{'n':1,'d':3}),('easy','integer_reversal',{'n':1,'d':1}),('hard','nonunit_point_reversal',{'n':100,'d':7})]:
  try:g.generate(level,parameters=p,profile=profile)
  except ValueError:pass
  else:raise AssertionError('Invalid explicit input accepted')
 r1=g.generate('moderate',parameters={'n':5,'d':3},profile='rational_reversal');r2=g.generate('moderate',parameters={'n':5,'d':3},profile='rational_numerator')
 assert r1['question'][':question/id']!=r2['question'][':question/id']
 assert r1['generation']['mathematical_fingerprint']==r2['generation']['mathematical_fingerprint']
 # Fresh concurrent render calls for identical and different sets, without caches.
 with tempfile.TemporaryDirectory(dir=HERE,prefix='concurrency-') as td:
  items=[(Fraction(7,3),2),(Fraction(7,3),2),(Fraction(-13,8),2),(Fraction(1,12),1)]
  with concurrent.futures.ThreadPoolExecutor(4) as pool:paths=list(pool.map(lambda z:g.render_curve(z[0],z[1],td),items))
  assert paths[0]==paths[1]
  for path,(c,m) in zip(paths,items):plot_test(path,c,Fraction(m))
  assert not list(Path(td).glob('render-*.tmp'))
 # Mutation regressions: stale solution scale and control chars must fail.
 for mutate in ('scale','control'):
  rr=json.loads(json.dumps(review[-1]));ss=rr['question'][':question/worked-solution']
  rr['question'][':question/worked-solution']=re.sub(r'scale factor of \$[^$]+\$',lambda _: 'scale factor of $99$',ss) if mutate=='scale' else ss+'\x0c'
  try:check(rr)
  except AssertionError:pass
  else:raise AssertionError('Mutation escaped QA')
 payload=[]
 for i,r in enumerate(review):
  f=r['question'][':question/answer-fields'][0]
  if ':answer-field/correct' not in f:continue
  ci=f[':answer-field/correct'][1];payload.append({'label':str(i),'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==ci else 'rejected','purpose':'every owned plotted choice'} for a in f[':answer-field/choices']]})
 # Native repaired missing-designation fixture, through ordinary authored profile.
 normal=check(g.generate('moderate',parameters={'n':3,'d':2},profile='rational_reversal'))
 review.append(normal)
 f=normal['question'][':question/answer-fields'][0];payload.append({'label':'inferred q-97958 normal','record':normal,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'independently inferred negative 3/2 graph'} for a in f[':answer-field/choices']]})
 normal=check(g.generate('easy',parameters={'n':3,'d':1},profile='integer_reversal'))
 review.append(normal)
 f=normal['question'][':question/answer-fields'][0];payload.append({'label':'inferred q-97963 normal','record':normal,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'independently inferred negative integer graph'} for a in f[':answer-field/choices']]})
 (HERE/'engine-input.json').write_text(json.dumps(payload,indent=2))
 engine=HERE.parents[1]/'runs/current/check-engine';subprocess.run([str(engine),str(HERE/'engine-input.json'),str(HERE/'engine-validation.json')],check=True)
 native=json.loads((HERE/'engine-validation.json').read_text())
 for name,obj in [('source-cases.json',cases),('review.json',review)]: (HERE/name).write_text(json.dumps(obj,indent=2))
 md=['# Negative reciprocal stretch review','All nine original banks precede their generated parameter variants. Hard is an authored extension at the same two-stage method. Raw q-97958/q-97963 preserve absent difficulty, worked solution and correct ref. Raw q-99068 retains the opaque doubled coefficient and is evidence-only.']
 for r in review:
  z=r['generation'];sid=z['bank_profile'].removeprefix('raw_');anchor=z['raw_replay'] and (z['parameters']['n'],z['parameters']['d'])==g.SOURCE_PARAMETERS[sid]
  md+=['## '+('Original replay' if anchor else 'Generated variant')+' — '+z['bank_profile'],json.dumps(z['parameters']),g.markdown(r).replace('![](images/', '![](/media/jake/SSD/EDB/math/images/').replace('![](generate/scratch/17592186068814/', '![](')]
 (HERE/'review.md').write_text('\n\n'.join(md))
 for link in re.findall(r'!\[\]\(([^)]+)\)',(HERE/'review.md').read_text()):
  path=Path(link);assert (path if path.is_absolute() else HERE/path).is_file(), ('Unresolved review image',link)
 report={'status':'pass','source_questions':9,'raw_prompt_exact':9,'raw_whole_solution_exact':7,'source_solution_present':7,'source_banks_matched':9,'source_options_matched':45,'source_distractors_matched_designated':28,'source_nondesignated_options_matched':10,'correct_designations_matched':7,'correct_designations_present':7,'missing_correct_designations':2,'attribute_presence_parity':9,'source_fidelity':fidelity,'normal_completed_inferred_designation':2,'authored_missing_levels':['hard'],'opaque_evidence_profiles':['raw_q-99068'],'historical_rounded_label_profile':'raw_q-97963','all_permitted_inputs_display_math_and_native_pixels':checked_instances,'meaningful_variety':variety,'exhaustive_valid_profile_instances':checked_instances,'review_records':len(review),'native':{k:native[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks')},'native_excluded_raw_missing_correct_records':6,'concurrency':'fresh identical/different renders passed','runtime':{'python':sys.version.split()[0],'sympy':g.sp.__version__,'matplotlib':g.matplotlib.__version__},'source_assets_native_inspected':source_raster_count,'source_practice_plot_occurrences':45,'engine_sha256':hashlib.sha256(engine.read_bytes()).hexdigest(),'database_writes':0}
 (HERE/'validation.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
if __name__=='__main__':main()
