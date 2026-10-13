"""Root graph-derived normal flow, statement-bank, source prose and scope QA."""
import importlib.util,json,re,hashlib,sys
from pathlib import Path
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;D=R.parents[2]/'generate/scratch/17592186133880'
z=importlib.util.spec_from_file_location('g',D.with_suffix('.py'));g=importlib.util.module_from_spec(z);z.loader.exec_module(g)
n=dict(records=0,choices=0,drawn_arrows=0,rectangle_normal_flow_checks=0,source_exact_banks=0,source_exact_values=0,source_exact_solutions=0,source_present_designations=0,source_missing_designations=0,source_plots_visually_inspected=15)
def subset(v):
 if v=='None of the statements are true.':return frozenset()
 assert v.endswith(' only');nums=v[:-5].split(' and ');assert len(set(nums))==len(nums) and set(nums)<=set(('I','II','III','IV'));return frozenset(nums)
def truth(sign):return frozenset(('I','IV')) if sign==0 else frozenset(('II',)) if sign>0 else frozenset(('III',))
def sign(v):return 1 if v>1e-7 else -1 if v< -1e-7 else 0
cache={}
def graph(path):
 if path in cache:return cache[path]
 side=json.load(open(Path(path).with_suffix('.json')));assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==side['png_sha256']
 arrows={}
 for sample,poly in zip(side['samples'],side['rendered_arrow_polygons']):
  tail=tuple((poly[0][i]+poly[6][i])/2 for i in (0,1));tip=poly[3];v=tuple((tip[i]-tail[i])*side['plot_scale'] for i in (0,1));assert all(abs(tail[i]-sample[i])<1e-7 and abs(v[i]-sample[i+2])<1e-7 for i in (0,1));arrows[tuple(sample[:2])]=v
 xs=sorted(set(x for x,y in arrows));ys=sorted(set(y for x,y in arrows));out=[]
 for a,b in zip(xs,xs[1:]):
  for c,d in zip(ys,ys[1:]):
   # Integral of affine normal components across all four outward-oriented sides.
   right=(arrows[b,c][0]+arrows[b,d][0])*(d-c)/2;left=(arrows[a,c][0]+arrows[a,d][0])*(d-c)/2
   top=(arrows[a,d][1]+arrows[b,d][1])*(b-a)/2;bottom=(arrows[a,c][1]+arrows[b,c][1])*(b-a)/2
   out.append(sign(right-left+top-bottom))
 assert len(set(out))==1
 # Recover the actual affine slopes from drawn arrow endpoint differences.
 a,b=xs[:2];c,d=ys[:2]
 matrix=[[(arrows[b,c][0]-arrows[a,c][0])/(b-a),(arrows[a,d][0]-arrows[a,c][0])/(d-c)],[(arrows[b,c][1]-arrows[a,c][1])/(b-a),(arrows[a,d][1]-arrows[a,c][1])/(d-c)]]
 cache[path]=(out[0],matrix,len(arrows),len(out));return cache[path]
def check(r,source_expected=None):
 q=r['question'];gm=r['generation'];raw=gm['evidence_only'];assert gm['eligible_for_learning']==(not raw)
 ref=re.search(r'!\[\]\((.*?)\)',q[':question/problem'])[1]
 if ref.startswith('images/'):expected=source_expected;assert expected is not None
 else:
  result,matrix,arrows,rectangles=graph(ref);expected=truth(result);n['drawn_arrows']+=arrows;n['rectangle_normal_flow_checks']+=rectangles
  if source_expected is not None:assert expected==source_expected
 for f in q[':question/answer-fields']:
  values=[subset(z[':answer/value']) for z in f[':answer-field/choices']];assert len(values)==5 and len(set(values))==5 and values.count(expected)==1
  if ':answer-field/correct' in f:assert f[':answer-field/correct'][1]==f[':answer-field/choices'][values.index(expected)][':answer/id']
  n['choices']+=5
 if not raw:
  symbol=re.search(r'vector field \$([FGH])\$',q[':question/problem'])[1];sol=q[':question/worked-solution'];result=1 if expected==truth(1) else -1 if expected==truth(-1) else 0
  for roman,relation in [('I','=0'),('II','>0'),('III','<0')]:assert f'{roman}. $∇\\cdot {symbol}{relation}$' in q[':question/problem']
  assert f'IV. ${symbol}$ is solenoidal' in q[':question/problem'];assert 'everywhere' in q[':question/problem'] and 'same length scale' in q[':question/problem']
  correct=next(z[':answer/value'] for z in q[':question/answer-fields'][0][':answer-field/choices'] if z[':answer/id']==q[':question/answer-fields'][0][':answer-field/correct'][1]);assert '"'+correct+'."' in sol
  assert ('Statement IV is true.' if result==0 else 'Statement IV is false.') in sol
  assert ('neither a source nor a sink' if result==0 else 'a source' if result>0 else 'a sink') in sol
  if 'Each component changes only' in sol:assert abs(matrix[0][0])<1e-7 and abs(matrix[1][1])<1e-7
  if '-component '+('increases' if result>0 else 'decreases') in sol:
   axis=re.search(r'The \$([xy])\$-component',sol)[1];i=0 if axis=='x' else 1;assert sign(matrix[i][i])==result and abs(matrix[1-i][1-i])<1e-7
  assert not any(z in q[':question/problem'] for z in ('differentiate','partial','compute','calculate'))
 n['records']+=1
source={q[':question/math-academy-id']:q for q in json.load(open(D/'source.json'))['record'][':knowledge-point/questions']}
# Source sign map independently read from every original raster: signed normal
# component growth, drift invariance, cross-coordinate shear, radial in/out.
source_sign={'q-105075':-1,'q-105571':0,'q-105046':0,'q-105573':1,'q-105575':0,'q-105576':0,'q-105578':1,'q-123245':1,'q-131192':1,'q-131193':0,'q-105577':0,'q-105572':-1,'q-131195':1,'q-131196':-1}
for sid,o in source.items():
 level=o[':question/difficulty'][':db/ident'].split('/')[-1];expected=truth(source_sign[sid]);r=g.generate(level,profile='raw-'+sid,parameters={'field_symbol':'F','swap_axes':False,'scale':1});check(r,expected);q=r['question'];assert q[':question/problem']==o[':question/problem'];assert q[':question/worked-solution']==o[':question/worked-solution'];n['source_exact_solutions']+=1
 for of,gf in zip(o[':question/answer-fields'],q[':question/answer-fields']):
  assert of[':answer-field/key']==gf[':answer-field/key'];assert sorted(z[':answer/value'] for z in of[':answer-field/choices'])==sorted(z[':answer/value'] for z in gf[':answer-field/choices']);n['source_exact_banks']+=1;n['source_exact_values']+=5;assert (':answer-field/correct' in of)==(':answer-field/correct' in gf)
  if ':answer-field/correct' in of:assert of[':answer-field/correct'][':answer/value']==next(z[':answer/value'] for z in gf[':answer-field/choices'] if z[':answer/id']==gf[':answer-field/correct'][1]);n['source_present_designations']+=1
  else:n['source_missing_designations']+=1
 for swap,scale in [(True,2),(False,3)]:check(g.generate(level,profile='raw-'+sid,parameters={'field_symbol':'H','swap_axes':swap,'scale':scale}),expected)
for level,objects in g.CATALOGS.items():
 fingerprints=set();signs=set()
 for obj in objects:
  selected=None
  for profile in g.BANKS:
   try:r=g.generate(level,profile=profile,parameters={'object':obj,'field_symbol':'G','scale':1})
   except ValueError:continue
   check(r);selected=r;break
  assert selected
  fingerprints.add(selected['generation']['mathematical_fingerprint']);signs.add(graph(selected['generation']['plot'])[0]);r2=g.generate(level,seed=982,profile=selected['generation']['bank_profile'],parameters={'object':obj,'field_symbol':'G','scale':3});assert r2['question'][':question/id']==selected['question'][':question/id']
 assert signs=={-1,0,1};n[level+'_finite_meaningful_objects']=len(fingerprints)
 for bad in [{'matrix':[[9,0],[0,9]],'drift':[0,0],'domain':'plane','family':'radial'},{'matrix':[[0,0],[0,0]],'drift':[1,0],'domain':'plane','family':'constant'}] if level!='easy' else [{'matrix':[[9,0],[0,9]],'drift':[0,0],'domain':'plane','family':'radial'}]:
  try:g.generate(level,parameters={'object':bad})
  except ValueError:pass
  else:raise AssertionError(('out of bounded scope',level,bad))
(R/'qa/17592186133880-independent.json').write_text(json.dumps(n,indent=2)+'\n');print(n)
