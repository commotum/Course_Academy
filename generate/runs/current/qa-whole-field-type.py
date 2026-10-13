"""Root independently audits whole-field invariance, original banks and plot grids."""
import importlib.util,json,re,sys,math,hashlib
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent;K=17592186172040;D=R.parents[2]/f'generate/scratch/{K}'
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);return m
p=module('parent_whole_math',R/'vector-math-parser.py');g=module('parent_whole_gen',D.with_suffix('.py'))
qs={q[':question/math-academy-id']:q for q in json.loads((R/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions']}
geom=json.loads((D/'source-geometry.json').read_text());counts=dict(source_questions=0,source_values=0,source_designations=0,source_missing_designations=0,source_prompts=0,source_solutions=0,printed_instances=0,source_plot_instances=0,authored_plot_instances=0,grid_slopes=0,worked_sequences=0,guide_lines=0)
def symbolic(expr):return s.sympify(expr,locals={'x':p.x,'y':p.y,'exp':s.exp})
def dependence(expr):return ('x' if s.diff(expr,p.x)!=0 else '')+('y' if s.diff(expr,p.y)!=0 else '')
def raster_dep(asset):
 values=geom[asset]['segments_normalized'];angles=[(x,y,math.atan(m)) for x,y,m in values]
 # Median within columns/rows discriminates invariant families; pixel centering
 # can shift mildly with antialiasing, so use coordinate bands, not exact equality.
 spreads=[]
 for axis in (0,1):
  coords=sorted(v[axis] for v in angles);groups=[]
  for value in coords:
   if not groups or value-groups[-1][-1]>.025:groups.append([value])
   else:groups[-1].append(value)
  bands=[(min(v),max(v)) for v in groups if len(v)>=4];ranges=[]
  for lo,hi in bands:
   aa=[v[2] for v in angles if lo<=v[axis]<=hi]
   if len(aa)>=4:ranges.append(max(aa)-min(aa))
  assert ranges,asset;spreads.append(sorted(ranges)[len(ranges)//2])
 # Fixed x means vertical line: y variation. Fixed y means horizontal line:
 # x variation. Only count clear separation from source antialiasing noise.
 assert any(v>.2 for v in spreads),(asset,spreads)
 if spreads[0]<.15:return 'x'
 if spreads[1]<.15:return 'y'
 return 'xy'
source_deps={asset:raster_dep(asset) for asset in geom}
def check(record):
 q=record['question'];m=record['generation'];hard='**cannot**' in q[':question/problem'];f=q[':question/answer-fields'][0];bank=f[':answer-field/choices'];deps=[];choice_points={};choice_expressions={}
 expr=None if hard else p.scalar(q[':question/problem'].split('=',1)[1].rstrip('?$'));assert expr is None or dependence(expr)=='xy'
 known={}
 if m['bank_profile']=='authored_method':
  assert len(m['plot_objects'])==5
  # Main rendering passes the same symbolic object list in owned bank order.
  for obj in m['plot_objects']:
   e=symbolic(obj['expression']);known.setdefault(dependence(e),[]).append(e)
 for answer in bank:
  val=answer[':answer/value']
  if val in geom:
   path=D/val;assert path.is_file();assert hashlib.sha256(path.read_bytes()).hexdigest()==geom[val]['source_sha256'];dep=source_deps[val];counts['source_plot_instances']+=1
  else:
   path=Path(val);assert path.is_file();side=json.loads(path.with_suffix('.json').read_text());points=side['points'];assert len(points)>=100;dep=None;choice_points[val]=points
   # Determine which exact symbolic field generated this displayed grid, using
   # every sampled actual slope, not a stored category assertion.
   candidates=[e for vv in known.values() for e in vv]
   if expr is not None:candidates.append(expr)
   matches=[]
   for e in candidates:
    fun=s.lambdify((p.x,p.y),e,'math')
    if all(math.isclose(fun(x,y),z,rel_tol=1e-10,abs_tol=1e-10) for x,y,z in points):matches.append(e)
   if m['bank_profile']=='authored_method':
    assert matches,(val,points[:2]);dep=dependence(matches[0]);choice_expressions[val]=matches[0];assert all(dependence(e)==dep for e in matches);counts['grid_slopes']+=len(points)
   else:
    # Changed empirical replay banks retain source geometry and category; no
    # inferred symbolic distractor intent is counted as source recovery.
    grid=points;bands={}
    for x,y,z in grid:bands.setdefault(round(x,1),[]).append(math.atan(z))
    vx=max(max(v)-min(v) for v in bands.values());bands={}
    for x,y,z in grid:bands.setdefault(round(y,1),[]).append(math.atan(z))
    vy=max(max(v)-min(v) for v in bands.values());dep='x' if vx<.2 else ('y' if vy<.2 else 'xy')
   counts['authored_plot_instances']+=1
  deps.append(dep)
 targets=[a[':answer/id'] for a,d in zip(bank,deps) if (d!='xy' if hard else d=='xy')];assert targets==[f[':answer-field/correct'][1]],(deps,m['source_id'])
 text=q[':question/worked-solution'];plots=re.findall(r'!\[\]\((.*?)\)',text);assert len(plots)==2;correct=next(a[':answer/value'] for a in bank if a[':answer/id']==targets[0]);assert plots[0]==correct
 assert 'Notice that we are given an equation of the form' in text and r'=f(x,y).' in text
 if hard:
  dep=deps[next(i for i,a in enumerate(bank) if a[':answer/id']==targets[0])];variable='y' if dep=='x' else 'x';fixed='x' if dep=='x' else 'y';line='vertical' if dep=='x' else 'horizontal'
  assert f'does not vary with ${variable}$ given a fixed value of ${fixed}.$' in text and f'draw a {line} line, the slopes do not vary.' in text
 else:assert 'only one that varies with both $x$ and $y$' in text and 'vertical line and a horizontal line' in text
 guidepath=Path(plots[1]) if Path(plots[1]).is_absolute() else D/plots[1];assert guidepath.is_file()
 if plots[1].startswith('images/'):
  assert guidepath.read_bytes()==(Path('/media/jake/SSD/EDB/math')/plots[1]).read_bytes()
 else:
  guideside=json.loads(guidepath.with_suffix('.json').read_text());assert guideside['guide']==('both' if not hard else dep)
  if m['bank_profile']=='authored_method':
   assert guideside['points']==choice_points[correct];e=choice_expressions[correct]
   vertical=s.simplify(e.subs(p.x,s.Rational(3,4)));horizontal=s.simplify(e.subs(p.y,s.Rational(-3,4)))
   if hard:assert (s.diff(vertical,p.y)==0 if dep=='x' else s.diff(horizontal,p.x)==0)
   else:assert s.diff(vertical,p.y)!=0 and s.diff(horizontal,p.x)!=0
 counts['worked_sequences']+=1;counts['guide_lines']+=1 if hard else 2;counts['printed_instances']+=1
 return deps
for case in json.loads((D/'source-cases.json').read_text()):
 sid=case['source_id'];old=qs[sid];r=g.generate(case.get('level',case.get('difficulty')),template=case['template'],parameters=case['parameters'],profile=case.get('bank_profile',case.get('profile')));check(r)
 assert old[':question/problem']==r['question'][':question/problem'];counts['source_prompts']+=1
 of=old[':question/answer-fields'][0];f=r['question'][':question/answer-fields'][0];assert sorted(a[':answer/value'] for a in of[':answer-field/choices'])==sorted(a[':answer/value'] for a in f[':answer-field/choices']);counts['source_values']+=5
 if of.get(':answer-field/correct'):
  v=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert v==of[':answer-field/correct'][':answer/value'];counts['source_designations']+=1
 else:counts['source_missing_designations']+=1
 if old.get(':question/worked-solution'):assert old[':question/worked-solution']==r['question'][':question/worked-solution'];counts['source_solutions']+=1
 counts['source_questions']+=1
for item in json.loads((D/'review.json').read_text()):check(item.get('record',item))
for item in json.loads((R/'qa'/f'{K}-sampled.json').read_text()):check(item)
counts['source_unique_geometries']=len(source_deps);counts['database_writes']=0;(R/'qa'/f'{K}-independent.json').write_text(json.dumps(counts,indent=2)+'\n');print(counts)
