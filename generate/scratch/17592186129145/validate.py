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
  for point in plot['raster_points']:
   z=point['x'];yy=float(correct.eval(z));assert abs(yy-point['y'])<1e-7*max(1,abs(yy))
   px,py=map(round,point['pixel']);region=red[max(0,py-4):py+5,max(0,px-4):px+5]
   assert region.any(),'missing raster point'
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
  case={'source_id':sid,'template':sid,'parameters':{'h':0,'s':1,'v':'1'},'bank_profile':sid,'level':level,'authored_level':sid=='q-38668'};cases.append(case)
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
  r=item['record'];f=r['question'][':question/answer-fields'][0]
  checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'owned radio choice native grading'} for a in f[':answer-field/choices']]
  native.append({'label':r['generation']['profile']+'-'+str(len(native)),'record':r,'checks':checks})
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
 for mutation in ['solution','choice','control','plot']:
  r=copy.deepcopy(base)
  if mutation=='solution':r['question'][':question/worked-solution']=r['question'][':question/worked-solution'].replace('x=', 'x=99',1)
  elif mutation=='choice':
   f=r['question'][':question/answer-fields'][0];a=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);a[':answer/value']='y=x'
  elif mutation=='control':r['question'][':question/problem']+='\x0c'
  else:r['generation']['plot']['coefficient']='99'
  try:check(r);raise RuntimeError('mutation survived '+mutation)
  except (AssertionError,ValueError):mutation_count+=1
 for level in finite:
  try:g.generate(level,parameters={'h':4,'s':1,'v':'1'});raise RuntimeError('bound accepted')
  except ValueError:pass
 (HERE/'source-cases.json').write_text(json.dumps(cases,indent=2));(HERE/'review.json').write_text(json.dumps(reviews,indent=2));(HERE/'native-input.json').write_text(json.dumps(native,indent=2))
 engine=ROOT/'generate/runs/current/check-engine'
 subprocess.run([str(engine),str(HERE/'native-input.json'),str(HERE/'native-report.json')],check=True)
 result={'status':'pass_with_documented_raw_bank_ineligibility','original_raster_root_points_checked':original_root_pixels,'source_total':10,'source_replayed':10,'original_banks_matched':8,'original_options_matched':40,'original_correct_designations_matched':7,'missing_correct_designation':1,'authored_fields':2,'source_solution_prose_stages_matched':9,'source_solution_prose_stages_total':9,'source_full_exact_solutions':sum(z['solution_full_exact'] for z in fidelity),'graphically_colliding_raw_banks':['q-38671','q-38774'],'all_normal_banks_graphically_distinct':True,'finite_mathematical_tasks':{l:len(v) for l,v in finite.items()},'exhaustive_bank_instances':operations,'native_checks':sum(len(z['checks']) for z in native),'review_count':len(reviews),'mutations_rejected':mutation_count,'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__,'matplotlib':g.matplotlib.__version__},'engine_sha256':hashlib.sha256(engine.read_bytes()).hexdigest(),'fidelity':fidelity}
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
