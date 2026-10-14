#!/usr/bin/env python3
"""Independent displayed mathematics, complete banks, PNG geometry, native grader."""
from pathlib import Path
import importlib.util,json,re,hashlib,subprocess,sys,copy
from concurrent.futures import ThreadPoolExecutor
import numpy as np
from PIL import Image
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
sys.dont_write_bytecode=True
P=Path(__file__).parent
spec=importlib.util.spec_from_file_location('reciprocal',str(P)+'.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
x=sp.Symbol('x');TRANS=standard_transformations+(implicit_multiplication_application,)

def latex_expr(token):
 token=token.strip().strip(',.?').replace(' ','')
 def group(s,start):
  assert s[start]=='{';depth=0
  for i in range(start,len(s)):
   depth+=int(s[i]=='{')-int(s[i]=='}')
   if depth==0:return s[start+1:i],i+1
  raise AssertionError('unbalanced TeX')
 while '\\frac' in token:
  i=token.index('\\frac');n,j=group(token,i+5);d,end=group(token,j);token=token[:i]+'(('+n+')/('+d+'))'+token[end:]
 return parse_expr(token,local_dict={'x':x},transformations=TRANS)

def read_formula(text):
 m=re.search(r'\$y\s*=\s*(.*?)\$',text)
 assert m,text
 return latex_expr(m[1])
def form(t):
 a,h,k=map(sp.Rational,t);return a/(x-h)+k

def formatting(q):
 for text in [q[':question/problem'],q.get(':question/worked-solution','')]:
  assert not any(ord(c)<32 and c not in '\n\t' for c in text),'control character'
  assert text.count('$')%2==0
  depth=0
  for c in text:
   depth+=int(c=='{')-int(c=='}');assert depth>=0
  assert depth==0
  assert '--' not in text and '+-' not in text

def check_png(path,t):
 path=Path(path);data=json.loads(path.with_suffix('.json').read_text());im=np.asarray(Image.open(path).convert('RGB'));assert list(im.shape[:2][::-1])==[480,400]
 assert data['triple']==g.triple(*t)
 a,h,k=map(float,map(sp.Rational,t));xl,xh,yl,yh=data['bounds'];sx=384/(xh-xl);sy=324/(yh-yl);ox=67.2-xl*sx;oy=348+yl*sy
 blue=(im[:,:,0]<100)&(im[:,:,1]>80)&(im[:,:,2]>140)&(im[:,:,2]>im[:,:,1]*1.15)
 ys,xs=np.where(blue);xx=(xs-ox)/sx;yy=(oy-ys)/sy
 # Curve plus markers, no blue text: geometric implicit-distance checks catch stale/mixed pixels.
 residual=abs((xx-h)*(yy-k)-a)/np.sqrt(((yy-k)/sx)**2+((xx-h)/sy)**2)
 assert np.quantile(residual,.95)<2.6,(path,np.quantile(residual,.95))
 d=float(sp.Rational(data['distance']))
 for mx,my in [(h-d,k-a/d),(h+d,k+a/d)]:
  px=int(round(ox+sx*mx));py=int(round(oy-sy*my));assert blue[max(0,py-4):py+5,max(0,px-4):px+5].sum()>15,(path,mx,my)
 # Dark true-zero axes at independently computed pixels.
 dark=im.max(2)<100
 assert dark[round(oy),75:430].sum()>250
 assert dark[40:340,round(ox)].sum()>220

def check_record(r,raw=False):
 assert set(r['knowledge_point'])=={'db_id','id','title'}
 q=r['question'];formatting(q);f=q[':question/answer-fields'][0];assert f[':answer-field/type']==':answer-field.type/radio'
 assert len(f[':answer-field/choices'])==5
 actual=read_formula(q[':question/problem']);bank=[]
 for ans in f[':answer-field/choices']:
  assert ans[':answer/type']==':answer.type/image';t=r['generation']['bank_geometry'][ans[':answer/value']];bank.append((ans,form(t)))
  if not ans[':answer/value'].startswith('images/'):check_png(ans[':answer/value'],t)
 for i in range(5):
  for j in range(i):assert sp.cancel(bank[i][1]-bank[j][1])!=0,'wrong-wrong or correct-wrong equivalence'
 true=[ans[':answer/id'] for ans,eq in bank if sp.cancel(eq-actual)==0];assert len(true)==1
 if ':answer-field/correct' in f:assert f[':answer-field/correct']==[':answer/id',true[0]]
 if not raw:
  rows=[latex_expr(z) for z in re.findall(r'\$y\s*=\s*(.*?)\$',q[':question/worked-solution'])]
  a,h,k=[sp.Rational(r['generation']['parameters'][key]) for key in ['a','h','k']];sign=sp.sign(a)
  wanted=[actual,sign/x]
  if h:wanted+=[sign/(x-h),a/(x-h)] if abs(a)!=1 else [sign/(x-h)]
  else:wanted+=[a/x,actual] if abs(a)!=1 else [actual]
  assert len(rows)==len(wanted),(len(rows),len(wanted),q)
  assert all(sp.cancel(left-right)==0 for left,right in zip(rows,wanted)),'stale or missing teaching row'
  # Read final image rather than generation metadata alone.
  last_path=re.findall(r'!\[\]\((.*?)\)',q[':question/worked-solution'])[-1]
  lt=[g.SPECS[last_path][key] for key in ['a','h','k']] if last_path.startswith('images/') else json.loads(Path(last_path).with_suffix('.json').read_text())['triple']
  assert sp.cancel(form(lt)-actual)==0
 return True

def main():
 fidelity=[];inputs=[];review=[];raw_variants=[]
 for c,source in zip(g.CASES,g.QUESTIONS):
  r=g.generate(c['level'],parameters=c['parameters'],profile=c['bank_profile']);q=r['question'];f=q[':question/answer-fields'][0];sf=source[':question/answer-fields'][0]
  for key in [':question/problem',':question/worked-solution']:
   assert (key in q)==(key in source);assert q.get(key)==source.get(key)
  assert (':question/difficulty' in q)==(':question/difficulty' in source)
  assert (':answer-field/correct' in f)==(':answer-field/correct' in sf)
  assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in sf[':answer-field/choices'])
  if ':answer-field/correct' in sf:
   val=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert val==sf[':answer-field/correct'][':answer/value']
   checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'complete raw source bank ID grading'} for a in f[':answer-field/choices']]
   inputs.append({'label':'source:'+c['source_math_academy_id'],'record':r,'checks':checks})
  check_record(r,True);fidelity.append({'source_id':c['source_id'],'prompt_exact':True,'solution_exact_or_absent':True,'bank_matched':5,'difficulty_presence':True,'correct_designation_present':':answer-field/correct' in sf})
  p=dict(c['parameters']);p['a']=str(-sp.Rational(p['a']));p['h']=-p['h'];p['k']=-p['k']
  changed=g.generate(c['level'],seed=19,parameters=p,profile=c['bank_profile']);check_record(changed,True);raw_variants.append(changed)
 # All source pixels re-read independently. Printed anomalous graph remains excluded
 # from label-to-formula claims, while its h=-3 makes its incorrectness unambiguous.
 source_assets=0
 for path,s in g.SPECS.items():
  fp=Path('/media/jake/SSD/EDB/math')/path;assert hashlib.sha256(fp.read_bytes()).hexdigest()==s['sha256']
  im=np.asarray(Image.open(fp).convert('RGBA'));assert list(im.shape[:2][::-1])==s['native_size'];assert s['curve_residual_px_p95']<2.6
  if not s['anomaly']:
   a,h,k=map(sp.Rational,[s[t] for t in ['a','h','k']]);assert all((sp.Rational(px)-h)*(sp.Rational(py)-k)==a for px,py in s['printed_points'])
  # Independently remeasure actual source pixels under each asset's own calibration.
  rgba=np.asarray(Image.open(fp).convert('RGBA'));white=np.ones(rgba.shape[:2]+(3,))*255;alpha=rgba[:,:,3:4]/255
  rgb=rgba[:,:,:3]*alpha+white*(1-alpha)
  blue=(rgb[:,:,0]<100)&(rgb[:,:,1]>80)&(rgb[:,:,2]>140)&(rgb[:,:,2]>rgb[:,:,1]*1.15)
  ox,oy=s['origin_px'];sx,sy=s['units_px'];a,h,k=map(float,map(sp.Rational,[s[t] for t in ['a','h','k']]))
  ys,xs=np.where(blue);xx=(xs-ox)/sx;yy=(oy-ys)/sy;safe=abs(xx-h)>.15
  resid=abs((xx[safe]-h)*(yy[safe]-k)-a)/np.sqrt(((yy[safe]-k)/sx)**2+((xx[safe]-h)/sy)**2)
  assert np.quantile(resid,.95)<2.6
  for px,py in s['pixel_marker_centers']:
   px,py=round(px),round(py);assert blue[py-4:py+5,px-4:px+5].sum()>15
  source_assets+=1
 profiles=['authored:method']+['normal:'+c['source_math_academy_id'] for c in g.CASES if c['source_math_academy_id']!='q-113372']
 normal=0;observed_profile_coverage=set()
 for level in ['easy','moderate','hard']:
  validprofiles=[p for p in profiles if p=='authored:method' or next(c for c in g.CASES if c['source_math_academy_id']==p.split(':')[1])['level']==level]
  for profile in validprofiles:
   for seed in [1,7]:
    r=g.generate(level,seed=seed,profile=profile);check_record(r);review.append(r);normal+=1;observed_profile_coverage.add(profile)
    f=r['question'][':question/answer-fields'][0]
    inputs.append({'label':f'{level}:{profile}:{seed}','record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'correct and every wrong image radio choice'} for a in f[':answer-field/choices']]})
 # Every source pair must differ under actual visible evidence, including
 # wrong-wrong pairs. The anomalous plot uses its independently labelled h only.
 for source in g.QUESTIONS:
  facts=[g.SPECS[a[':answer/value']] for a in source[':question/answer-fields'][0][':answer-field/choices']]
  for i in range(5):
   for j in range(i):
    left,right=facts[i],facts[j]
    if left['anomaly'] or right['anomaly']:assert left['h']!=right['h']
    else:assert (left['h'],left['k'],left['printed_points'])!=(right['h'],right['k'],right['printed_points'])
 # Explicit boundary constraints, including easy/moderate/hard workload guards.
 rejected=0
 for level,p in [('easy',{'a':'2','h':1,'k':0}),('moderate',{'a':'1','h':0,'k':1}),('hard',{'a':'1/6','h':1,'k':0}),('hard',{'a':'2','h':1,'k':1}),('moderate',{'a':'2','h':0,'k':5})]:
  try:g.generate(level,parameters=p,profile='authored:method')
  except ValueError:rejected+=1
  else:raise AssertionError('explicit bounds not enforced')
 # Identities exclude seed/order/profile aliases but include complete actual banks.
 for level,p,t in [('easy',{'a':'1','h':-4,'k':0},'horizontal_then_scale'),('moderate',{'a':'1/5','h':0,'k':-4},'scale_then_vertical'),('hard',{'a':'-5/4','h':4,'k':0},'horizontal_then_scale')]:
  a=g.generate(level,seed=2,parameters=p,template=t,profile='authored:method');b=g.generate(level,seed=91,parameters=p,template=t,profile='authored:method');check_record(a);check_record(b)
  assert a['question'][':question/id']==b['question'][':question/id'];assert a['generation']['mathematical_fingerprint']==b['generation']['mathematical_fingerprint']
 # Fresh parallel render requests have no shared global Figure/input filenames.
 tasks=[['-5/3',4,0],['3/5',-4,0],['-5/3',4,0],['3/5',-4,0]]
 with ThreadPoolExecutor(4) as pool:paths=list(pool.map(lambda t:g.render_plot(t,force=True),tasks))
 assert paths[0]==paths[2] and paths[1]==paths[3] and paths[0]!=paths[1]
 for path,t in zip(paths,tasks):check_png(path,t)
 # Read actual generated prompt and rows: mutated coefficients, stages, control chars fail.
 mutations=0;base=copy.deepcopy(review[-1])
 for mode in ['prompt','solution','control','bank']:
  bad=copy.deepcopy(base)
  if mode=='prompt':bad['question'][':question/problem']=bad['question'][':question/problem'].replace('y=','y=2+')
  if mode=='solution':bad['question'][':question/worked-solution']=bad['question'][':question/worked-solution'].replace('Take the curve $y=','Take the curve $y=2+')
  if mode=='control':bad['question'][':question/problem']+='\x0c'
  if mode=='bank':
   vals=list(bad['generation']['bank_geometry']);bad['generation']['bank_geometry'][vals[1]]=bad['generation']['bank_geometry'][vals[0]]
  try:check_record(bad)
  except AssertionError:mutations+=1
  else:raise AssertionError('mutation escaped validation '+mode)
 default_profiles={g.generate(level,seed=s)['generation']['profile'] for level in ['moderate','hard'] for s in range(50)}
 assert set(profiles)<=default_profiles
 inp=P/'engine-input.json';inp.write_text(json.dumps(inputs,indent=2));engine=Path('generate/runs/current/check-engine');out=P/'engine-report.json'
 subprocess.run([str(engine),str(inp),str(out)],check=True)
 report={'status':'passed','runtime':review[0]['generation']['runtime'],'basis':1356,'source_question_count':10,'raw_fidelity':{'complete_banks':10,'options':50,'existing_correct_designations':8,'missing_correct_designations':2,'solutions_exact':8,'solutions_absent':2,'prompt_exact':10,'difficulty_presence_exact':10},'mathematical_source_exclusions':[{'source':'q-113372','choice_index':4,'reason':'inconsistent label/curve vertical coordinates; raw source preserved, opaque coefficient unidentifiable','criterion_wrong_from_visible_asymptote':True}],'solution_repairs':[{'source':'q-113372','raw_opening':'vertical offset1, prompt3','normal':'authored method profile correct opening'},{'source':'q-113369','raw_opening':'vertical offset1, prompt2','normal':'normal profile correct opening'}],'source_geometry_assets':source_assets,'coherent_source_label_geometry_assets':source_assets-1,'opaque_source_graphs_distinct_by_visible_vertical_asymptote':1,'source_all_pair_visible_comparisons':100,'max_source_implicit_distance_p95_px':max(s['curve_residual_px_p95'] for s in g.SPECS.values()),'normal_checked':normal,'profiles_checked':sorted(observed_profile_coverage),'default_profile_coverage':sorted(default_profiles),'raw_changed_profile_checks':10,'explicit_guard_rejections':rejected,'mutation_rejections':mutations,'concurrent_calls':4,'concurrent_fresh_writes':4,'finite_task_counts':{l:len(g.domain(l,'scale_then_vertical' if l=='moderate' else 'horizontal_then_scale'))*(2 if l=='easy' else 1) for l in ['easy','moderate','hard']},'native_grading':{'fixtures':len(inputs),'checks':sum(len(i['checks']) for i in inputs),'binary_sha256':hashlib.sha256(engine.read_bytes()).hexdigest(),'report':'engine-report.json','missing_raw_correct_fields_not_native_gradeable':2}}
 (P/'review.json').write_text(json.dumps({'normal':review,'raw_variants_evidence_only':raw_variants},indent=2));(P/'validation.json').write_text(json.dumps(report,indent=2))
 md='# Graphing a Transformed Reciprocal Function\n\nRaw evidence is ineligible for learning; originals retain omissions and anomalies. Normal records supply corrected solutions and inferred missing correct refs.\n\n'
 for c,source,r in zip(g.CASES,g.QUESTIONS,raw_variants):
  md+='## Original '+c['source_math_academy_id']+'\n\n'+source[':question/problem']+'\n\n'
  for ans in source[':question/answer-fields'][0][':answer-field/choices']:md+='![](/media/jake/SSD/EDB/math/'+ans[':answer/value']+')\n\n'
  md+=source.get(':question/worked-solution','Original worked solution absent.')+'\n\n### Changed parameter evidence recipe (ineligible)\n\n'+g.markdown(r)+'\n\n'
 for r in review:md+='## Generated '+r['generation']['difficulty']+' / '+r['generation']['profile']+'\n\n'+g.markdown(r)+'\n\n'
 (P/'review.md').write_text(md);print(json.dumps(report,indent=2))
if __name__=='__main__':main()
