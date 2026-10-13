"""Root parses printed equations/three ordered rows and audits all plotted banks."""
import importlib.util,json,re,math,sys
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent;K=17592186172038;D=R.parents[2]/f'generate/scratch/{K}';ROOT=R.parents[2]
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);return m
p=module('parent_isolated_math',R/'vector-math-parser.py');g=module('parent_isolated_gen',D.with_suffix('.py'))
qs={q[':question/math-academy-id']:q for q in json.loads((R/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions']}
counts=dict(source_questions=0,source_option_geometries=0,source_designations=0,source_missing_designations=0,source_prompts=0,source_prose_sequences=0,source_ordered_math_stages=0,printed_instances=0,bank_plots=0,segment_endpoints=0,substitution_rows=0,substitution_stages=0,authored_bank_operations=0,authored_bank_separation_pairs=0)
def equation(q):return p.scalar(q[':question/problem'].split('=',1)[1].rstrip('$?'))
def stages(q):
 block=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',q[':question/worked-solution'],re.S).group(1);rows=block.split(r'\\');assert len(rows)==3
 result=[]
 for row in rows:
  match=re.search(r'\|\}_\{\((.*?)\)\}',row);assert match,row
  pt=tuple(p.scalar(v) for v in match.group(1).split(','));assert len(pt)==2
  vals=[p.scalar(v) for v in row.split('=',1)[1].split('=')];result.append((pt,vals))
 return result

def check(r):
 q=r['question'];expr=equation(q);rows=stages(q);pts=[pt for pt,vals in rows];correct=[]
 assert len(set(pts))==3
 for pt,vals in rows:
  value=s.simplify(expr.subs(dict(zip((p.x,p.y),pt))));assert len(vals)==(3 if r['generation']['bank_profile']=='authored' and not q[':question/difficulty'].endswith('/easy') else 2)
  assert all(s.simplify(v-value)==0 for v in vals),(q[':question/id'],pt,vals,value);correct.append(value);counts['substitution_rows']+=1;counts['substitution_stages']+=len(vals)
 f=q[':question/answer-fields'][0];banks=[];correct_ids=[]
 for a in f[':answer-field/choices']:
  path=ROOT/a[':answer/value'];assert path.is_file();meta=json.loads(path.with_suffix('.json').read_text());assert len(meta['segments'])==3
  centerpts=[tuple(s.Rational(v) for v in v) for v in meta['exact_points']];assert centerpts==pts
  bank=[]
  for pt,seg in zip(pts,meta['segments']):
   center=list(map(float,pt));assert seg['center']==center;ends=seg['endpoints'];assert len(ends)==2
   assert all(math.isclose((ends[0][i]+ends[1][i])/2,center[i],abs_tol=1e-12) for i in (0,1))
   dx=ends[1][0]-ends[0][0];dy=ends[1][1]-ends[0][1];assert math.isclose(math.hypot(dx,dy),.8,abs_tol=1e-12)
   slope=s.oo if seg['slope']=='inf' else s.Rational(seg['slope']);assert abs(dx)<1e-12 if slope==s.oo else math.isclose(dy,float(slope)*dx,abs_tol=1e-12)
   assert all(meta['bounds'][0]<x<meta['bounds'][1] and meta['bounds'][2]<y<meta['bounds'][3] for x,y in ends)
   bank.append(slope);counts['segment_endpoints']+=2
  banks.append(tuple(bank));counts['bank_plots']+=1
  if bank==correct:correct_ids.append(a[':answer/id'])
 assert len(banks)==len(set(banks))==5 and correct_ids==[f[':answer-field/correct'][1]]
 correctpath=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==correct_ids[0]);assert re.findall(r'!\[\]\((.*?)\)',q[':question/worked-solution'])==[correctpath]
 if r['generation']['bank_profile']=='authored':
  expected=[tuple(correct),tuple(-v for v in correct),tuple(s.simplify(expr.subs({p.x:x,p.y:x},simultaneous=True)) for x,y in pts),tuple(s.simplify(expr.subs({p.x:x,p.y:0})) for x,y in pts)]
  # The fifth constant-product operation omits its constant; remaining forms
  # omit the x term / denominator input using x=1 for a rational field.
  constant=expr.subs({p.x:0,p.y:0})
  if s.Poly(s.together(expr*p.x if expr.has(p.x**-1) else expr),p.x,p.y).total_degree()==2 and s.diff(expr,p.x,p.y)!=0 and s.diff(expr,p.x,2)==0:
   expected.append(tuple(v-constant for v in correct))
  else:expected.append(tuple(s.simplify(expr.subs({p.x:1 if expr.has(p.x**-1) else 0,p.y:y})) for x,y in pts))
  assert set(expected)==set(banks),(expr,expected,banks);counts['authored_bank_operations']+=5
  for i,row in enumerate(banks):
   for other in banks[:i]:
    ds=[]
    for a,b in zip(row,other):
     aa=math.pi/2 if a==s.oo else math.atan(float(a));bb=math.pi/2 if b==s.oo else math.atan(float(b));delta=abs(aa-bb);ds.append(min(delta,math.pi-delta))
    assert max(ds)>=math.radians(8);counts['authored_bank_separation_pairs']+=1
  level=q[':question/difficulty'].rsplit('/',1)[1]
  if level=='easy':assert all(v.q==1 for pt in pts for v in pt)
  elif level=='moderate':assert all(v.q==1 for pt in pts for v in pt) and any(v.q>1 for v in s.Poly(expr*p.x if expr.has(p.x**-1) else expr,p.x,p.y).coeffs())
  else:assert all(v.q==2 for pt in pts for v in pt)
 counts['printed_instances']+=1
 return banks,rows
raster=json.loads((D/'source-raster.json').read_text())
for case in json.loads((D/'source-cases.json').read_text()):
 sid=case['source_id'];old=qs[sid];r=g.generate(case['difficulty'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);banks,rows=check(r)
 assert old[':question/problem']==r['question'][':question/problem'];assert s.simplify(equation(old)-equation(r['question']))==0;counts['source_prompts']+=1
 # Each original image index maps one-to-one through the observed bank recipes;
 # the raw files and independent raster directions corroborate all three segments.
 _,originalbank=g.banks(case['template'],case['parameters'],case['bank_profile']);assert set(map(tuple,originalbank))==set(banks)
 oldfield=old[':question/answer-fields'][0];rr=[v for v in raster if v['source_id']==sid];assert len(rr)==len(oldfield[':answer-field/choices'])==5
 for i,(observed,bank) in enumerate(zip(rr,originalbank)):
  assert observed['asset']==oldfield[':answer-field/choices'][i][':answer/value'];assert (Path('/media/jake/SSD/EDB/math')/observed['asset']).is_file()
  for a,b in zip(bank,observed['raster_slopes']):
   if a==s.oo:assert b=='inf'
   else:assert abs(math.atan(float(a))-math.atan(b))<.06
  counts['source_option_geometries']+=1
 if oldfield.get(':answer-field/correct'):
  ci=next(i for i,a in enumerate(oldfield[':answer-field/choices']) if a[':answer/id']==oldfield[':answer-field/correct'][':answer/id']);assert list(originalbank[ci])==[v[-1] for pt,v in rows];counts['source_designations']+=1
 else:counts['source_missing_designations']+=1
 if old.get(':question/worked-solution'):
  normalize=lambda text:re.sub(r'!\[\]\([^)]*\)','<PLOT>',re.sub(r'\\begin\{aligned\}.*?\\end\{aligned\}','<ROWS>',text,flags=re.S))
  assert normalize(old[':question/worked-solution'])==normalize(r['question'][':question/worked-solution']);oldrows=stages(old);assert oldrows==rows;counts['source_prose_sequences']+=1;counts['source_ordered_math_stages']+=sum(len(v) for pt,v in rows)
 counts['source_questions']+=1
for item in json.loads((D/'review.json').read_text()):check(item)
for item in json.loads((R/'qa'/f'{K}-sampled.json').read_text()):check(item)
counts['database_writes']=0;(R/'qa'/f'{K}-independent.json').write_text(json.dumps(counts,indent=2)+'\n');print(counts)
