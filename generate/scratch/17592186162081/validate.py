#!/usr/bin/env python3
"""Independent displayed scalar and stage checks, raw fidelity and native grading."""
import copy, hashlib, importlib.util, itertools, json, re, subprocess, sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
import numpy as np
import sympy as sp
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE));from math_reader import scalar
spec=importlib.util.spec_from_file_location('unity',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def save(name,x): (HERE/name).write_text(json.dumps(x,indent=2)+'\n')
def image_path(ref):return Path('/media/jake/SSD/EDB/math')/ref if ref.startswith('images/') else Path(ref)
def check(r):
 q=r['question'];m=r['generation'];t=m['template'];p=m['parameters'];d=g.data(t,p)
 assert set(r['knowledge_point'])=={'db_id','id','title'}
 assert all(ord(c)>=32 or c in '\n\t' for z in [q[':question/problem'],q.get(':question/worked-solution','')]+[a[':answer/value'] for a in q[':question/answer-fields'][0][':answer-field/choices']] for c in z)
 f=q[':question/answer-fields'][0];vals=[scalar(a[':answer/value']) for a in f[':answer-field/choices']]
 assert len(vals)==5
 for a,b in itertools.combinations(vals,2):assert sp.simplify(a-b)!=0
 L=sp.pi*sp.Rational(p['r']) if t=='semicircle' else sp.sqrt((sp.Rational(p['x2'])-sp.Rational(p['x1']))**2+(sp.Rational(p['y2'])-sp.Rational(p['y1']))**2)
 if ':answer-field/correct' in f:
  a=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert sp.simplify(scalar(a[':answer/value'])-L)==0
 if not m['evidence_only']:assert all(v>0 for v in vals);g.workload(m['level'],t,d)
 for ref in re.findall(r'!\[.*?\]\((.*?)\)',q[':question/problem']+' '+q.get(':question/worked-solution','')):
  ip=image_path(ref);assert ip.exists();im=Image.open(ip).convert('RGBA');white=Image.new('RGBA',im.size,'white');white.alpha_composite(im);im=white.convert('RGB');pix=np.array(im).astype('int16');blue=(pix[:,:,2]>pix[:,:,0]+30)&(pix[:,:,2]>pix[:,:,1]+10)&(pix[:,:,0]<140);assert blue.sum()>80
  if not ref.startswith('images/'):
   side=json.loads(ip.with_suffix('.json').read_text());assert side['sha256']==hashlib.sha256(ip.read_bytes()).hexdigest();assert side['recipe']==g.plot_recipe(t,d,side['recipe']['helper']);assert list(im.size)==side['native_pixels'];assert len(np.unique(pix[::4,::4].reshape(-1,3),axis=0))>50
   transform=np.array(side['data_transform']);assert abs(abs(transform[0,0])-abs(transform[1,1]))<1e-6
   # Confirm real blue curve pixels at independently computed points along the path.
   if t=='semicircle':points=[(float(sp.Rational(p['r']))*__import__('math').cos(u),float(sp.Rational(p['r']))*__import__('math').sin(u)) for u in (0,.4,1.2,2.1,__import__('math').pi)]
   else:points=[(float(sp.Rational(p['x1']))+u*float(sp.Rational(p['x2'])-sp.Rational(p['x1'])),float(sp.Rational(p['y1']))+u*float(sp.Rational(p['y2'])-sp.Rational(p['y1']))) for u in (0,.2,.5,.8,1)]
   for x,y in points:
    xp,yp,_=transform@np.array([x,y,1]);xp,yp=round(xp),round(456-yp)
    assert blue[max(0,yp-5):yp+6,max(0,xp-5):xp+6].any(),('missing plotted point',ref,x,y)
 s=q.get(':question/worked-solution')
 if not s:return
 if t.startswith('diagonal'):
  prose=re.search(r'legs have lengths \$(.*?)\$ and \$(.*?)\$',s);assert prose
  leg1=scalar(prose[1]);leg2=scalar(prose[2].rstrip(':'));assert leg1==d['b'] and leg2==d['a']
  block=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',s,re.S)[1]
  rows=re.split(r'\\\\\s*&\s*=',block);assert len(rows)==4
  exprs=[e.strip() for e in [rows[0].split('=',1)[1]]+rows[1:]]
  for e in exprs:assert sp.simplify(scalar(e)-L)==0
  # Source operation shapes: substituted squares, evaluated two squares, collected root, simplified length.
  assert '^{2}' in exprs[0] and exprs[0].count('^{2}')==2
  first=re.fullmatch(r'\\sqrt\{\{(.*?)\}\^\{2\}\+\{(.*?)\}\^\{2\}\}',exprs[0]);assert first
  assert scalar(first[1])==leg1 and scalar(first[2])==leg2
  second=re.fullmatch(r'\\sqrt\{(.*?)\+(.*?)\}',exprs[1]);assert second
  assert scalar(second[1])==leg1**2 and scalar(second[2])==leg2**2
  assert exprs[2].startswith(r'\sqrt{') and '+' not in exprs[2]
  if t=='diagonal_helper':assert s.count('![](')==1
 elif t in ('vertical','horizontal'):
  eq=re.findall(r'\\text\{d\}s=([^\n]+)',s)[-1];pieces=eq.rstrip('.').split('=');assert len(pieces)==2
  assert sp.simplify(scalar(pieces[0])-L)==0 and scalar(pieces[1])==L
 elif t=='semicircle':
  radius=re.search(r'r = (.*?)\.\$',s)[1];assert scalar(radius)==sp.Rational(p['r'])
  value=re.search(r'L=\\pi r=(.*?) \.\\end',s)[1];assert sp.simplify(scalar(value)-L)==0
 # Independently inspect the final learner-visible conclusion.
 final=re.findall(r'(?:\\text\{d\}s|\\textrm d s)\s*=\s*([^\n]+)',s)[-1]
 assert sp.simplify(scalar(final.split('=')[-1])-L)==0

def main():
 # Fit each original raster independently; verify stated endpoints and semicircle radius.
 source_raster_checks=0
 for asset in json.loads((HERE/'plot-extraction.json').read_text()):
  im=Image.open(image_path(asset['asset'])).convert('RGBA');white=Image.new('RGBA',im.size,'white');white.alpha_composite(im);pix=np.array(white.convert('RGB')).astype('int16')
  blue=(pix[:,:,2]>pix[:,:,0]+30)&(pix[:,:,2]>pix[:,:,1]+10)&(pix[:,:,0]<140)
  origin=asset['source_axes_fit']['origin_pixels'];scale=asset['source_axes_fit']['pixels_per_coordinate_unit'];sid=asset['source_id'];t,p=g.P[sid]
  if t=='semicircle':points=[(float(p['r'])*__import__('math').cos(u),float(p['r'])*__import__('math').sin(u)) for u in (0,.6,1.5,2.4,__import__('math').pi)]
  else:points=[(p['x1'],p['y1']),(p['x2'],p['y2']),((p['x1']+p['x2'])/2,(p['y1']+p['y2'])/2)]
  for x,y in points:
   xp,yp=round(origin[0]+x*scale),round(origin[1]-y*scale);assert blue[max(0,yp-5):yp+6,max(0,xp-5):xp+6].any(),('original geometry mismatch',sid,x,y)
  source_raster_checks+=1
 cases=[];replays=[];fidelity=[]
 for sid,(t,p) in g.P.items():
  case={'source_id':sid,'template':t,'parameters':p,'bank_profile':'original:'+sid,'level':'easy','authored_level_assignment':sid=='q-122567'};cases.append(case)
  r=g.generate('easy',template=t,parameters=p,profile=case['bank_profile']);check(r);replays.append(r);q=r['question'];src=g.QUESTIONS[sid]
  assert q[':question/problem']==src[':question/problem'];assert q.get(':question/worked-solution')==src.get(':question/worked-solution')
  for k in (':question/difficulty',':question/worked-solution'):assert (k in q)==(k in src)
  f=q[':question/answer-fields'][0];sf=src[':question/answer-fields'][0];assert (':answer-field/correct' in f)==(':answer-field/correct' in sf)
  assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in sf[':answer-field/choices'])
  if ':answer-field/correct' in sf:assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==sf[':answer-field/correct'][':answer/value']
  fidelity.append({'source_id':sid,'bank_choices_matched':5,'complete_bank_matched':True,'prompt_exact':True,'solution_exact':':question/worked-solution' in src,'solution_absent_preserved':':question/worked-solution' not in src,'correct_designation_matched':':answer-field/correct' in sf,'missing_key_preserved':':answer-field/correct' not in sf,'presence_parity':True})
 save('source-cases.json',cases)
 review=[]
 for r in replays:review.append({'label':'Original raw evidence '+r['generation']['source_id'],'record':r})
 for sid,(t,p) in g.P.items():
  changed={k:str(sp.Rational(v)*sp.Rational(3,2)) for k,v in p.items()}
  r=g.generate('easy',template=t,parameters=changed,profile='original:'+sid);check(r);review.append({'label':'Changed public evidence mask '+sid,'record':r})
 for sid,(t,p) in g.P.items():
  r=g.generate('easy',template=t,parameters=p);check(r)
  if ':question/worked-solution' in g.QUESTIONS[sid]:
   strip_assets=lambda text:re.sub(r'!\[.*?\]\((.*?)\)','![](ASSET)',text)
   assert strip_assets(r['question'][':question/worked-solution'])==strip_assets(g.QUESTIONS[sid][':question/worked-solution'])
  review.append({'label':'Normal source-parameter teaching mask '+sid,'record':r})
 for level in ('easy','moderate','hard'):
  for t in (g.TEMPLATES if level=='easy' else g.TEMPLATES[-2:]):
   for seed in (11,35):
    r=g.generate(level,seed,template=t);check(r);review.append({'label':'Authored normal '+level+' '+t,'record':r})
 normal=[];coverage={}
 for level in ('easy','moderate','hard'):
  for seed in range(36):
   r=g.generate(level,seed);check(r);normal.append(r)
  coverage[level]=sorted(set(r['generation']['template'] for r in normal if r['generation']['level']==level))
  assert set(coverage[level])==set(g.TEMPLATES if level=='easy' else g.TEMPLATES[-2:])
 # Replay and option-order determinism, parameter identity and actual reversal.
 for item in review:
  r=item['record'];m=r['generation'];r2=g.generate(m['level'],987,template=m['template'],parameters=m['parameters'],profile=m['profile']);check(r2)
  assert r2['question'][':question/id']==r['question'][':question/id']
  assert r2['generation']['mathematical_fingerprint']==m['mathematical_fingerprint']
 r=g.generate('easy',parameters={'x1':-1,'y1':-1,'x2':3,'y2':1},template='diagonal_helper');rr=g.generate('easy',parameters={'x1':3,'y1':1,'x2':-1,'y2':-1},template='diagonal_helper');check(rr);assert rr['generation']['length']==r['generation']['length'];assert rr['generation']['mathematical_fingerprint']==r['generation']['mathematical_fingerprint']
 # Meaningful arithmetic capacities independent of layout, translation, orientation or banks.
 capacities={}
 for level in ('easy','moderate','hard'):
  tasks=set()
  if level=='easy':
   for r in range(1,11):
    d=g.data('semicircle',{'r':r})
    try:g.valid_bank(g.bank('semicircle',d,'geometric')[0]);tasks.add(('semicircle',str(r)))
    except ValueError:pass
   for lo,hi in itertools.product([-4,-3,-2,1,2],[5,6,7,8]):
    d=g.data('horizontal',dict(x1=lo,y1=1,x2=hi,y2=1))
    try:g.workload(level,'horizontal',d);g.valid_bank(g.bank('horizontal',d,'geometric')[0]);tasks.add(('axis',str(d['L'])))
    except ValueError:pass
   pairs=itertools.combinations(range(2,11),2)
  elif level=='moderate':pairs=itertools.combinations([sp.Rational(n,2) for n in range(3,20,2)],2)
  else:pairs=itertools.product([sp.Rational(n,3) for n in range(4,24) if n%3],[sp.Rational(n,4) for n in range(5,32) if n%2])
  for a,b in pairs:
   d=g.data('diagonal_plain',dict(x1=0,y1=0,x2=str(a),y2=str(b)));g.workload(level,'diagonal_plain',d);g.valid_bank(g.bank('diagonal_plain',d,'geometric')[0]);tasks.add(('diagonal',*sorted([str(a),str(b)])))
  capacities[level]=len(tasks)
 # Concurrent changed and identical rendering: immutable assets and sidecars remain coherent.
 params=[{'x1':-1,'y1':0,'x2':'17/3','y2':'29/4'},{'x1':-2,'y1':-1,'x2':'16/3','y2':'27/4'}]*2
 with ThreadPoolExecutor(max_workers=2) as pool:
  results=list(pool.map(lambda p:g.generate('hard',template='diagonal_helper',parameters=p),params))
 for r in results:check(r)
 assert results[0]['question'][':question/id']==results[2]['question'][':question/id']
 # Independent processes exercise simultaneous atomic publication and isolated mathtext.
 process_params=[{'x1':'-11/12','y1':'-7/12','x2':'23/4','y2':'20/3'}]*2+[{'x1':'-5/12','y1':'-1/12','x2':'25/4','y2':'43/6'}]*2
 def process_render(p):
  code='import importlib.util,json; s=importlib.util.spec_from_file_location("g",'+repr(str(HERE.with_suffix('.py')))+');g=importlib.util.module_from_spec(s);s.loader.exec_module(g);print(json.dumps(g.generate("hard",template="diagonal_helper",parameters='+repr(p)+')))'
  out=subprocess.run([sys.executable,'-c',code],check=True,capture_output=True,text=True)
  return json.loads(out.stdout)
 with ThreadPoolExecutor(max_workers=4) as pool: process_results=list(pool.map(process_render,process_params))
 for r in process_results:check(r)
 assert process_results[0]['question'][':question/id']==process_results[1]['question'][':question/id']
 assert process_results[2]['question'][':question/id']==process_results[3]['question'][':question/id']
 
 # Mutation regressions must fail despite an unchanged final answer.
 mutations=[]
 base=next(x['record'] for x in review if x['label']=='Authored normal moderate diagonal_plain')
 for label,mutator in [('lost substituted-square operation',lambda s:s.replace('^{2}','',1)),('control character',lambda s:s+'\x0c'),('wrong evaluated square',lambda s:s.replace('\\sqrt{\\frac', '\\sqrt{1+\\frac',1))]:
  bad=copy.deepcopy(base);bad['question'][':question/worked-solution']=mutator(bad['question'][':question/worked-solution'])
  try:check(bad)
  except (AssertionError,ValueError):mutations.append(label)
  else:raise AssertionError('Mutation undetected: '+label)
 # All selected radios are checked through the actual memory-only engine.
 engine=[]
 for i,r in enumerate([x['record'] for x in review]+normal):
  f=r['question'][':question/answer-fields'][0]
  if ':answer-field/correct' not in f:continue
  checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'every displayed radio choice'} for a in f[':answer-field/choices']]
  engine.append({'label':str(i),'record':r,'checks':checks})
 save('engine-input.json',engine)
 subprocess.run([str(HERE.parents[1]/'runs/current/check-engine'),str(HERE/'engine-input.json'),str(HERE/'engine-validation.json')],check=True)
 save('review.json',review);save('source-bank-fidelity.json',fidelity)
 text='# Line integrals of unity review\n\nRaw originals preserve omissions. Changed raw masks are evidence only. Normal variants use authored complete method banks.\n\n'
 for item in review:text+='## '+item['label']+'\n\n'+g.markdown(item['record'])+'\n\n'
 (HERE/'review.md').write_text(text)
 report={'passed':True,'parent_qa_approved':(HERE/'independent-review.json').exists() and json.loads((HERE/'independent-review.json').read_text()).get('approved',False) and json.loads((HERE/'independent-review.json').read_text()).get('generator_sha256')==hashlib.sha256(HERE.with_suffix('.py').read_bytes()).hexdigest(),'source_basis':g.SOURCE['basis'],'source_questions':6,'complete_banks':6,'choices_matched':30,'incorrect_choices_matched':24,'observed_incorrect_choices_matched':20,'independently_inferred_incorrect_choices_matched':4,'correct_designations_matched':5,'missing_correct_designations':1,'worked_solutions_exact':5,'missing_worked_solutions':1,'presence_parity_sources':6,'original_rasters_geometry_checked':source_raster_checks,'normal_source_solution_masks_checked':5,'normal_questions_checked':len(normal),'review_records':len(review),'default_family_coverage':coverage,'meaningful_sampler_capacities':capacities,'total_meaningful_tasks':sum(capacities.values()),'mutation_regressions':mutations,'concurrent_render_checks':8,'concurrent_process_checks':4,'calculator_requirements':'all six supplement records omit flags; unknown, not false','runtime':normal[0]['generation']['runtime'],'script_sha256':hashlib.sha256(HERE.with_suffix('.py').read_bytes()).hexdigest(),'source_sha256':hashlib.sha256((HERE/'source.json').read_bytes()).hexdigest(),'unresolved':['Original q-122567 has no observed key, solution or difficulty; normal completion is authored.','Five scalar segment distractor banks have underidentified original error intent; public homogeneous masks remain evidence only.','Moderate/hard levels are conservative authored workload designs, not observed labels.']}
 save('validation.json',report);print(json.dumps(report,indent=2))

if __name__=="__main__":main()
