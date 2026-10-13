"""Root reads displayed field, coordinate substitution stages and all plot arrows."""
import importlib.util,json,re,hashlib
from pathlib import Path
R=Path(__file__).resolve().parent;K=17592186172083;D=R.parents[2]/f'generate/scratch/{K}'
def module(name,path):
 sp=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
p=module('root_sketch_reader',R/'planar-field-readback.py');g=module('root_sketch_generator',D.with_suffix('.py'));s=p.s;x,y=p.x,p.y
C=dict(instances=0,component_stages=0,plot_arrow_components=0,displayed_banks=0,source_questions=0,source_raw_banks=0,source_image_values=0,source_existing_refs=0,source_missing_refs=0,source_normalized_solution_sequences=0)

def check(r):
 q=r['question'];meta=r['generation'];field=p.vector(re.search(r'\$F\(x,y\)=(.*?)\$',q[':question/problem'])[1]);solution=q[':question/worked-solution'];block=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',solution,re.S)[1];rows=block.split(chr(92)*2);assert len(rows)==3
 points=[];vectors=[]
 for row in rows:
  label,stages=row.split('& =',1);point=re.fullmatch(r'\s*F\((.*)\)\s*',label);assert point,label;point=tuple(p.scalar(z) for z in point[1].split(','));assert len(point)==2;points.append(point)
  vector=tuple(s.simplify(z.subs({x:point[0],y:point[1]})) for z in field);assert all(z.is_Rational for z in vector);vectors.append(vector)
  stages=stages.split('=');assert len(stages)==2
  for stage in stages:
   printed=p.vector(stage);assert all(s.simplify(a-b)==0 for a,b in zip(printed,vector)),(stage,printed,vector);C['component_stages']+=2
 assert len(set(points))==3
 for point in points:
  assert abs(point[0])<=5 and abs(point[1])<=5
 level=q[':question/difficulty'].split('/')[-1];grid=1 if level=='easy' else s.Rational(1,2 if level=='moderate' else 4)
 if level!='easy':
  den=2 if level=='moderate' else 4;assert all(a.is_Integer and a!=0 and b.q==den and b!=0 for a,b in points);assert min(b for a,b in points)<0<max(b for a,b in points)
  assert all(s.Poly(z,x,y).total_degree()==2 for z in field) and set().union(*(z.free_symbols for z in field))=={x,y}
 f=q[':question/answer-fields'][0];correct=f[':answer-field/correct'][1];banks=[]
 geometry={z['path']:tuple(tuple(s.Rational(v) for v in pair) for pair in z['vectors']) for z in meta['plot_banks']}
 for a in f[':answer-field/choices']:
  path=Path(a[':answer/value']);assert path.exists();assert str(path) in geometry
  if meta['source_original_geometry']:arrows=geometry[str(path)]
  else:
   side=json.loads(path.with_suffix('.json').read_text());assert side['renderer']=='Matplotlib';tails=[tuple(s.Rational(z) for z in pair) for pair in side['exact_points']];arrows=tuple(tuple(s.Rational(z) for z in pair) for pair in side['exact_vectors']);assert tails==points and arrows==geometry[str(path)]
   assert s.Rational(str(side['grid_increment']))==grid
   for (tx,ty),(u,v) in zip(tails,arrows):
    assert side['bounds'][0]<tx<side['bounds'][1] and side['bounds'][0]<tx+u<side['bounds'][1] and side['bounds'][2]<ty<side['bounds'][3] and side['bounds'][2]<ty+v<side['bounds'][3];C['plot_arrow_components']+=2
  assert (arrows==tuple(vectors))==(a[':answer/id']==correct);banks.append(arrows)
 assert len(set(banks))==5
 if meta['bank_profile']=='authored_sign_swap':
  expected=[vectors,[(u,-v) for u,v in vectors],[(-u,v) for u,v in vectors],[(v,u) for u,v in vectors],[(-u,-v) for u,v in vectors]];assert set(banks)=={tuple(z) for z in expected}
 final_plot=re.findall(r'!\[\]\(([^)]+)\)',solution);assert len(final_plot)==1 and final_plot[0]==next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==correct)
 C['instances']+=1;C['displayed_banks']+=1;return q,field,points

def prose(text):
 text=re.sub(r'\$\$.*?\$\$','<math>',text,flags=re.S);text=re.sub(r'\$[^$]*\$','<math>',text);text=re.sub(r'!\[\]\([^)]*\)','<image>',text);return re.sub(r'\s+',' ',text).strip()
sources={q[':question/math-academy-id']:q for q in json.loads((R/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions']};seen=set()
for case in json.loads((D/'source-cases.json').read_text()):
 old=sources[case['source_id']];q,field,points=check(g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']))
 if case['source_id'] in seen:continue
 seen.add(case['source_id']);C['source_questions']+=1;rawfield=re.search(r'F\(x,\s*y\)\s*=\s*(.*?)\$',old[':question/problem'])[1];assert all(s.simplify(a-b)==0 for a,b in zip(p.vector(rawfield),field))
 fresh=q[':question/answer-fields'][0]
 for of in old[':question/answer-fields']:
  oldpaths=[str(Path('/media/jake/SSD/EDB/math')/a[':answer/value']) for a in of[':answer-field/choices']];assert sorted(oldpaths)==sorted(a[':answer/value'] for a in fresh[':answer-field/choices']);C['source_raw_banks']+=1;C['source_image_values']+=len(oldpaths)
  if of.get(':answer-field/correct'):
   actual=next(a[':answer/value'] for a in fresh[':answer-field/choices'] if a[':answer/id']==fresh[':answer-field/correct'][1]);assert actual==str(Path('/media/jake/SSD/EDB/math')/of[':answer-field/correct'][':answer/value']);C['source_existing_refs']+=1
  else:C['source_missing_refs']+=1
 if old.get(':question/worked-solution'):
  raw=old[':question/worked-solution'];assert prose(raw)==prose(q[':question/worked-solution']);oldrows=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',raw,re.S)[1].split(chr(92)*2);assert len(oldrows)==3
  for row,point in zip(oldrows,points):
   label,stages=row.split('& =',1);rawpoint=re.fullmatch(r'\s*F\((.*)\)\s*',label);assert tuple(p.scalar(z) for z in rawpoint[1].split(','))==point
   for stage in stages.split('='):assert all(s.simplify(a-b.subs({x:point[0],y:point[1]}))==0 for a,b in zip(p.vector(stage),field))
  C['source_normalized_solution_sequences']+=1
for item in json.loads((D/'review.json').read_text()):check(item.get('record',item))
for item in json.loads((R/'qa'/f'{K}-sampled.json').read_text()):check(item)
C['database_writes']=0;(R/'qa'/f'{K}-independent.json').write_text(json.dumps(C,indent=2)+'\n');print(C)
