#!/usr/bin/env python3
"""Read learner strings and independent raster geometry, then actual native grading."""
import concurrent.futures, copy, hashlib, importlib.util, json, math, re, subprocess, sys, tempfile
from pathlib import Path
import numpy as np
from PIL import Image
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
SCRIPT=HERE.with_suffix('.py')
spec=importlib.util.spec_from_file_location('draft',SCRIPT);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
x=sp.Symbol('x')
def parse(s):
 s=s.strip().rstrip('.').replace(r'\,','').replace('?', '')
 for command in ['frac','dfrac']:
  s=re.sub(r'\\'+command+r'\{(-?\d+)\}\{(-?\d+)\}',r'(\1/\2)',s)
 return parse_expr(s,local_dict={'x':x},transformations=standard_transformations+(implicit_multiplication_application,),evaluate=True)
def equation(q):
 match=re.search(r'\$y\s*=\s*(.*?)\$',q[':question/problem']);assert match
 expression=parse(match[1]);assert sp.Poly(expression,x).degree()<=1
 return sp.expand(expression).coeff(x),expression.subs(x,0)
def clustered(indices):
 groups=[]
 for i in indices:
  if not groups or i-groups[-1][-1]>1:groups.append([i])
  else:groups[-1].append(i)
 return np.array([float(np.mean(v)) for v in groups])
def raster_fit(path,half_grid=False):
 """Independently fit each raster's black axes, gray grid and red whole straight line."""
 arr=np.array(Image.open(path).convert('RGB'));r,gg,b=arr[:,:,0],arr[:,:,1],arr[:,:,2]
 black=(r<75)&(gg<75)&(b<75);gray=(abs(r.astype(int)-gg.astype(int))<3)&(abs(gg.astype(int)-b.astype(int))<3)&(r>180)&(r<235)
 bx=black.sum(axis=0);by=black.sum(axis=1)
 xc=float(np.mean(np.flatnonzero(bx>max(bx)*.9)));yc=float(np.mean(np.flatnonzero(by>max(by)*.9)))
 cx=gray.sum(axis=0);cy=gray.sum(axis=1);xs=clustered(np.flatnonzero(cx>max(cx)*.65));ys=clustered(np.flatnonzero(cy>max(cy)*.65))
 def step(v):
  gaps=np.diff(v);rough=float(np.median(gaps));indices=np.r_[0,np.cumsum(np.rint(gaps/rough))];return float(np.polyfit(indices,v,1)[0])
 dx=step(xs);dy=step(ys)
 if half_grid:dx*=2;dy*=2
 red=(r>170)&(gg<100)&(b<100);yp,xp=np.where(red);a,c=np.polyfit(xp,yp,1)
 m=-a*dx/dy;intercept=(yc-(a*xc+c))/dy
 # Stroke tolerances cover source anti-alias and axes halfpixel center, not wrong integer shifts.
 return {'native_size':[arr.shape[1],arr.shape[0]],'origin_pixel':[xc,yc],'unit_pixels':[dx,dy],'fit_line':[m,intercept],'red_pixels':len(xp),'max_residual_pixels':float(np.max(abs(yp-(a*xp+c))))}
def closefit(fit,line):
 assert fit['red_pixels']>30 and abs(fit['fit_line'][0]-float(line[0]))<.035 and abs(fit['fit_line'][1]-float(line[1]))<max(.065,.7*(abs(float(line[0]))+1)/min(fit['unit_pixels'])),(fit,line)
def verify(rec,plots=True):
 q=rec['question'];gen=rec['generation'];assert set(rec['knowledge_point'])=={'db_id','id','title'}
 for s in [q[':question/problem'],q.get(':question/worked-solution','')]+[a[':answer/value'] for a in q[':question/answer-fields'][0][':answer-field/choices']]:
  assert not any(ord(c)<32 and c not in '\n\t\r' for c in s)
  assert s.count('$')%2==0
  assert s.count('{')==s.count('}')
 m,b=equation(q);bank=[]
 for path in gen['choice_paths']:
  idx=gen['choice_paths'].index(path);bank.append(tuple(map(g.rat,gen['choice_lines'][idx])))
 assert len(set(bank))==5 and bank.count((m,b))==1
 f=q[':question/answer-fields'][0];assert len(q[':question/answer-fields'])==1 and f[':answer-field/type']==':answer-field.type/radio' and len(f[':answer-field/choices'])==5
 uuids={a[':answer/id'] for a in f[':answer-field/choices']};assert len(uuids)==5
 for z in uuids|{q[':question/id'],f[':answer-field/id']}:g.uuid.UUID(z)
 if ':answer-field/correct' in f:
  answer=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);idx=gen['choice_paths'].index(answer[':answer/value']);assert bank[idx]==(m,b)
 if ':question/worked-solution' in q:
  sol=q[':question/worked-solution'];point_matches=re.findall(r'So, the (first|second) point is \$\((.*?),(.*?)\)\.\$',sol)
  assert len(point_matches)==2
  points=[(parse(a),parse(c)) for word,a,c in point_matches];assert points[0][0]==0 and points[0][0]!=points[1][0]
  assert all(sp.simplify(y-m*xx-b)==0 for xx,y in points)
  chosen=re.findall(r'coordinate be \$x=(.*?)\.\$',sol);assert [parse(v) for v in chosen]==[p[0] for p in points]
  blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S);assert len(blocks)==2
  for (xx,y),block in zip(points,blocks):
   rows=re.split(r'\\\\',block);rs=[re.sub(r'^.*?&\s*=','',row).strip() for row in rows]
   assert len(rs)==(3 if b==0 else 4)
   assert sp.simplify(parse(rs[0])-(m*x+b))==0
   assert '('+g.tex(xx)+')' in rs[1] # substitution stage cannot collapse into a result
   assert all(sp.simplify(parse(row).subs(x,xx)-y)==0 for row in rs)
   if b!=0:
    expected=g.tex(b)+('+' if m*xx>0 or m*xx==0 and m>0 else '-')+g.tex(abs(m*xx)) if gen['parameters']['layout']=='constant-first' else g.tex(m*xx)+('+'+g.tex(b) if b>0 else g.tex(b))
    assert rs[2]==expected # retain evaluated product plus shift, not merely algebraic equivalence
  final=re.search(r'This is the graph of \$y=(.*?)\.\$',sol);assert final and sp.simplify(parse(final[1])-(m*x+b))==0
  if not gen['evidence_only']:assert [list(map(str,p)) for p in points]==gen['formal_points']
  if plots and gen['assets']:
   solution_asset=gen['assets'][-1];assert solution_asset['line']==[str(m),str(b)] and solution_asset['points']==[list(map(str,p)) for p in points]
 if not gen['evidence_only']:
  level=q[':question/difficulty'].split('/')[-1];assert g.normal_domain(level,m,b,g.rat(gen['parameters']['x2']))
  if level=='hard':assert all(sp.denom(parse(c))==2 for word,a,c in point_matches) and gen['reading_grid']=='1/2'
 if plots:
  for inf in gen['assets']:
   assert hashlib.sha256(Path(inf['local']).read_bytes()).hexdigest()==inf['sha256']
   fit=raster_fit(inf['local'],inf['reading_grid']=='1/2');closefit(fit,list(map(g.rat,inf['line'])))
   if inf['points']:
    arr=np.array(Image.open(inf['local']).convert('RGB'));blue=(arr[:,:,2]>150)&(arr[:,:,0]<100)&(arr[:,:,1]<130)
    ox,oy=fit['origin_pixel'];ux,uy=fit['unit_pixels']
    for px,py in inf['points']:
     cx=ox+float(g.rat(px))*ux;cy=oy-float(g.rat(py))*uy
     assert blue[max(0,int(cy)-5):int(cy)+6,max(0,int(cx)-5):int(cx)+6].sum()>8
 return True

def main():
 s=json.loads((HERE/'source.json').read_text());originals=s['record'][':knowledge-point/questions'][:4];cases=json.loads((HERE/'source-cases.json').read_text());sourcefits=[];records=[]
 for source,case in zip(originals,cases):
  rec=g.generate('easy',seed=11,template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);verify(rec,False);records.append(rec)
  q=rec['question'];f=q[':question/answer-fields'][0];sf=source[':question/answer-fields'][0]
  assert q[':question/problem']==source[':question/problem']
  for key in [':question/difficulty',':question/worked-solution']:assert (key in q)==(key in source)
  if ':question/worked-solution' in source:assert q[':question/worked-solution']==source[':question/worked-solution']
  assert (':answer-field/correct' in f)==(':answer-field/correct' in sf)
  assert set(a[':answer/value'] for a in f[':answer-field/choices'])==set(a[':answer/value'] for a in sf[':answer-field/choices'])
  if ':answer-field/correct' in sf:assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==sf[':answer-field/correct'][':answer/value']
  # Every source occurrence, including repeated assets, fitted independently.
  for i,a in enumerate(sf[':answer-field/choices']):
   fit=raster_fit('/media/jake/SSD/EDB/math/'+a[':answer/value']);line=list(map(g.rat,rec['generation']['choice_lines'][i]));closefit(fit,line)
   sourcefits.append({'source_id':case['source_id'],'choice_index':i,'path':a[':answer/value'],'sha256':hashlib.sha256(Path('/media/jake/SSD/EDB/math/'+a[':answer/value']).read_bytes()).hexdigest(),'whole_line':[str(z) for z in line],'calibration':fit,'inspection':'Native full-resolution visual inspection independently confirms labelled tick scale, red whole-line direction/intercept, no choice markers; pixel fit independently confirms every option.'})
 (HERE/'source-plot-inspection.json').write_text(json.dumps(sourcefits,indent=2)+'\n')
 solutionfits=[]
 for sid,t in g.PROFILES.items():
  if not t['solution_present']:continue
  path=Path('/media/jake/SSD/EDB/math')/t['solution_path'];fit=raster_fit(path);m,b,xx,layout=g.values(t['parameters']);closefit(fit,[m,b])
  arr=np.array(Image.open(path).convert('RGB'));blue=(arr[:,:,2]>150)&(arr[:,:,0]<100)&(arr[:,:,1]<130)
  pointchecks=[]
  for px,py in [(0,b),(xx,m*xx+b)]:
   ux,uy=fit['unit_pixels'];ox,oy=fit['origin_pixel'];cx=ox+float(px)*ux;cy=oy-float(py)*uy
   crop=blue[max(0,int(cy)-5):int(cy)+6,max(0,int(cx)-5):int(cx)+6];assert crop.sum()>8
   pointchecks.append({'coordinate':[str(px),str(py)],'calibrated_pixel':[cx,cy],'blue_pixels_within_5px':int(crop.sum())})
  solutionfits.append({'source_id':sid,'path':t['solution_path'],'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'calibration':fit,'actual_source_points':pointchecks})
 (HERE/'source-solution-inspection.json').write_text(json.dumps(solutionfits,indent=2)+'\n')
 changed_historical=[]
 for sid,p in {'q-54286':{'m':'3','b':'-3','x2':'1'},'q-59678':{'m':'1/3','b':'-3','x2':'3'},'q-102054':{'m':'-3','b':'0','x2':'2'},'q-109055':{'m':'-1/3','b':'3','x2':'6','layout':'constant-first'}}.items():
  rec=g.generate('easy',seed=77,profile=sid,parameters=p);verify(rec);changed_historical.append(rec)
 for level,entry in [('easy',g.generate_easy),('moderate',g.generate_moderate),('hard',g.generate_hard)]:assert entry(seed=1)['question'][':question/id']==g.generate(level,seed=1)['question'][':question/id']
 inventory=json.loads((HERE/'independent-inventory.json').read_text());assert inventory['basis']==s['basis'] and inventory['lineage']==s['lineage'];assert [v['record'] for v in inventory['questions']]==s['record'][':knowledge-point/questions'][4:]
 scope_counts={};normal=[];coverage={}
 for level in ['easy','moderate','hard']:
  templates=['homogeneous','coefficient-first','constant-first'] if level=='easy' else ['coefficient-first','constant-first'];scope_counts[level]={};coverage[level]={}
  for template in templates:
   domain=g.parameter_domain(level,template);scope_counts[level][template]=len(domain);assert len(domain)>=40
   # Hold slope and shift constant, change eligible x2; substantive point-role slot varies.
   for p in [domain[0],domain[-1]]:
    rec=g.generate(level,seed=5,template=template,parameters=p);verify(rec);normal.append(rec)
   coverage[level][template]={'second_x_values':sorted({p['x2'] for p in domain}),'slope_values':sorted({p['m'] for p in domain}),'shift_values':sorted({p['b'] for p in domain})}
  for seed in range(18):
   rec=g.generate(level,seed=seed);verify(rec);normal.append(rec)
  shown={r['generation']['template'] for r in normal if r['question'].get(':question/difficulty')==':question.difficulty/'+level};assert shown==set(templates)
 # Explicit level guards: M must reject observed unit numerator half slope; H must reject integer intercept.
 for level,p in [('moderate',{'m':'1/2','b':'2','x2':'2'}),('hard',{'m':'3/2','b':'2','x2':'2'}),('easy',{'m':'3/2','b':'2','x2':'2'})]:
  try:g.generate(level,parameters=p)
  except ValueError:pass
  else:raise AssertionError('scope guard missing')
 # Seed/order identity unchanged for same actual information and bank.
 a=g.generate('moderate',seed=1,parameters={'m':'3/2','b':'1','x2':'2'},template='coefficient-first');brec=g.generate('moderate',seed=991,parameters={'m':'3/2','b':'1','x2':'2'},template='coefficient-first');verify(a);assert a['question'][':question/id']==brec['question'][':question/id']
 changed=g.generate('moderate',parameters={'m':'3/2','b':'1','x2':'-2'},template='coefficient-first');verify(changed);assert a['generation']['mathematical_fingerprint']==changed['generation']['mathematical_fingerprint'];assert a['question'][':question/id']!=changed['question'][':question/id']
 # Fresh concurrent writes exercise separate parameters plus identical inputs, without cache reuse.
 old=g.PACKAGE
 with tempfile.TemporaryDirectory(prefix='concurrency-',dir=HERE) as td:
  g.PACKAGE=Path(td)
  jobs=[(sp.Rational(3,2),sp.Rational(1,2)),(sp.Rational(-3,2),sp.Rational(-1,2)),(sp.Rational(3,2),sp.Rational(1,2))]
  with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:results=list(pool.map(lambda p:g.render_plot(*p,points=[(0,p[1]),(2,2*p[0]+p[1])],reading=sp.Rational(1,2)),jobs))
  assert results[0][0]==results[2][0] and results[0][0]!=results[1][0]
  for path,info in results:closefit(raster_fit(info['local'],True),list(map(g.rat,info['line'])))
  assert not list((Path(td)/'assets').glob('render-*'))
 g.PACKAGE=old
 # Mutations ensure independent readback catches stale final point, collapsed arithmetic stage, control bytes.
 mutations=[]
 for kind in ['point','stage','control','plot']:
  bad=copy.deepcopy(a)
  if kind=='point':bad['question'][':question/worked-solution']=bad['question'][':question/worked-solution'].replace('So, the second point is $(2,4).$','So, the second point is $(2,3).$')
  if kind=='stage':bad['question'][':question/worked-solution']=bad['question'][':question/worked-solution'].replace('3+1','4')
  if kind=='control':bad['question'][':question/problem']+='\x0c'
  if kind=='plot':bad['generation']['assets'][-1]['line'][1]='2'
  try:verify(bad)
  except AssertionError:mutations.append(kind)
  else:raise AssertionError('mutation was not rejected '+kind)
 engine=[]
 for i,rec in enumerate(records+normal+[a,changed]+changed_historical):
  f=rec['question'][':question/answer-fields'][0]
  if ':answer-field/correct' not in f:continue
  checks=[{'submitted_answer_id':ans[':answer/id'],'expected':'accepted' if ans[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Actual radio ID grading; separately checked full graph mathematics'} for ans in f[':answer-field/choices']]
  engine.append({'label':f'record-{i}','record':rec,'checks':checks})
 (HERE/'engine-input.json').write_text(json.dumps(engine,indent=2)+'\n');subprocess.run([str(Path('generate/runs/current/check-engine').resolve()),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
 engine_report=json.loads((HERE/'engine-report.json').read_text());result={'status':'passed','database_writes':0,'source_basis':s['basis'],'source_lineage':s['lineage'],'script_sha256':hashlib.sha256(SCRIPT.read_bytes()).hexdigest(),'source_sha256':hashlib.sha256((HERE/'source.json').read_bytes()).hexdigest(),'context_hashes':{kind:hashlib.sha256((Path('generate/runs/current/refresh-2026-10-14')/kind/'17592186050790.json').read_bytes()).hexdigest() for kind in ['topics','lessons']},'available_source_solution_marker_rasters_checked':2,'original_questions':4,'exact_prompts':4,'complete_banks_matched':4,'options_matched':20,'distractors_matched':16,'available_correct_designations_matched':2,'missing_correct_designations_preserved':2,'available_exact_solutions_matched':2,'missing_solutions_preserved':2,'raw_difficulty_presence_matches':4,'source_option_native_inspections':20,'source_unique_option_plots':15,'independent_inventory_exact_records':3,'changed_historical_profile_checks':4,'entrypoint_parity_checks':3,'normal_records_verified':len(normal)+2,'normal_rendered_plot_geometry_checks':6*(len(normal)+2),'normal_solution_blue_marker_checks':2*(len(normal)+2),'native_grading':{k:v for k,v in engine_report.items() if k!='records'},'scope_domain_counts':scope_counts,'distinct_graph_selection_tasks':{level:len({(p['m'],p['b']) for t in (['homogeneous','coefficient-first'] if level=='easy' else ['coefficient-first']) for p in g.parameter_domain(level,t)}) for level in ['easy','moderate','hard']},'slot_coverage':coverage,'mutation_regressions_rejected':mutations,'concurrent_fresh_renders':3,'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__,'matplotlib':g.matplotlib.__version__},'engine_binary_sha256':hashlib.sha256(Path('generate/runs/current/check-engine').read_bytes()).hexdigest(),'engine_source_sha256':hashlib.sha256(Path('generate/runs/current/check-engine.rs').read_bytes()).hexdigest(),'unresolved':['Historical distractor mathematical transformations recovered; original author intent is underdetermined. Historical raw profiles are evidence-only, normal profiles are separately authored method-derived banks.','Two original MA records omit solution/correct reference/difficulty. Exact raw omissions preserved; normal completions are authored, not recovered.']}
 (HERE/'validation.json').write_text(json.dumps(result,indent=2)+'\n')
 review=records+[next(r for r in normal if r['question'].get(':question/difficulty')==':question.difficulty/'+lev and r['generation']['template']==t and ((g.rat(r['generation']['parameters']['m'])<0) if t=='coefficient-first' else (g.rat(r['generation']['parameters']['m'])>0))) for lev in ['easy','moderate','hard'] for t in ['coefficient-first','constant-first']]
 (HERE/'review.json').write_text(json.dumps(review,indent=2)+'\n')
 (HERE/'review.md').write_text('# Original replay and authored variants\n\n'+ '\n\n---\n\n'.join(('## Original evidence: '+r['generation']['profile'] if r['generation']['evidence_only'] else '## Authored '+r['question'][':question/difficulty'].split('/')[-1]+': '+r['generation']['template'])+'\n\n'+g.markdown(r) for r in review)+'\n')
 print(json.dumps(result,indent=2))
if __name__=='__main__':main()
