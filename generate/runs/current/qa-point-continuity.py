"""Root graph-object continuity and original per-option predicates, actual PNG markers."""
import importlib.util,json,re,hashlib,sys,itertools
from pathlib import Path
import sympy as s
import numpy as np
from PIL import Image
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186068695;D=R.parents[2]/f'generate/scratch/{K}'
def load(p,n):
 z=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
p=load(R/'ode-scalar-parser.py','point_continuity_parser');x=p.x
fidelity=load(R/'root-source-fidelity.py','point_continuity_fidelity');g=load(D.with_suffix('.py'),'point_continuity_g');originals,S=fidelity.check(g,K,D)
def coordinates(text):return [p.scalar(m[1].strip().rstrip('.,?')) for m in re.finditer(r'x=([^$]+)\$',text)]
def status(graph,a):
 left=[];right=[];values=[];a=s.Rational(a)
 for piece in graph['segments']:
  lo,hi=map(s.Rational,(piece['lo'],piece['hi']));raw=s.sympify(piece['expr'],locals={'x':x},evaluate=False);excluded=set(map(s.Rational,piece.get('raw_excluded',[])))|set(map(s.Rational,graph['holes']+graph['poles']))
  if lo<a<=hi:left.append(s.limit(raw,x,a,dir='-'))
  if lo<=a<hi:right.append(s.limit(raw,x,a,dir='+'))
  if lo<a<hi and a not in excluded:
   v=raw.subs(x,a)
   if v.is_finite:values.append(v)
 if str(a) in graph['values']:values=[s.Rational(graph['values'][str(a)])]
 assert all(s.simplify(v-values[0])==0 for v in values) if values else True
 assert all(s.simplify(v-left[0])==0 for v in left[1:]) and all(s.simplify(v-right[0])==0 for v in right[1:])
 value=values[0] if values else None;l=left[0] if left else None;r=right[0] if right else None
 return l,r,value,bool(l is not None and r is not None and value is not None and l.is_finite is True and r.is_finite is True and s.simplify(l-r)==0 and s.simplify(l-value)==0)
# Independently read source shapes, including every wrong graph and source poles.
original_points={'q-48039':(-2,{'4020dd89':False,'4a009c92':False,'56576892':False,'f4a28f88':True,'29ff22e9':False}),'q-48081':(2,{'0a31db89':False,'8c2cca8f':False,'fdd6b61f':True,'56a689e2':False,'4ad2a8ae':False}),'q-69782':(5,{'42e1d990':False,'d124370f':True,'17fc3c79':False,'76a1b2ca':False,'135973e3':False}),'q-48082':(0,{'c6f0914f':True,'c2f85d1a':False,'14349b3d':False,'3073f651':False,'c95d9944':False})}
original_subsets={'q-102106':([-1,2,4],[True,True,False]),'q-78133':([-7,-4,-1],[False,True,False]),'q-102115':([-1,1,3],[False,False,True]),'q-78131':([-2,0,2],[False,True,True]),'q-78132':([-2,1,3],[True,False,True])}
C=dict(records=0,source_option_predicates=0,source_subset_predicates=0,source_pole_limits=0,actual_side_limits=0,actual_values=0,choices=0,response_pair_checks=0,solution_coordinate_components=0,source_prose_masks=0,raster_open_markers=0,raster_filled_markers=0,zero_axes=0,hard_midpoint_readings=0)
for sid,(a,options) in original_points.items():
 for prefix,want in options.items():assert status(g.G[prefix],a)[3]==want;C['source_option_predicates']+=1
for sid,(targets,want) in original_subsets.items():
 for a,expect in zip(targets,want):assert status(g.G[g.SPECS[sid]['graph']],a)[3]==expect;C['source_subset_predicates']+=1
for prefix,a,ls,rs in [('4020dd89',-2,-s.oo,s.oo),('29ff22e9',-2,-s.oo,-s.oo),('8c2cca8f',2,-s.oo,s.oo),('56a689e2',2,s.oo,s.oo),('17fc3c79',5,-s.oo,s.oo),('135973e3',5,-s.oo,-s.oo),('c2f85d1a',0,-s.oo,s.oo),('c95d9944',0,s.Rational(3,2),s.oo)]:
 st=status(g.G[prefix],a);assert all(a==b or a.is_finite is True and b.is_finite is True and s.simplify(a-b)==0 for a,b in zip(st[:2],(ls,rs))),(prefix,st,(ls,rs));C['source_pole_limits']+=2
records=json.load(open(R/f'qa/{K}-sampled.json'))
for sid,spec in g.SPECS.items():records.extend(g.generate(spec['level'],template=sid,seed=n) for n in (631,917))
for sid in ('q-78133','q-102115'):records.extend(g.generate_hard(template=sid,seed=n) for n in (631,917))
for rec in records:
 q=rec['question'];prompt=q[':question/problem'];sol=q[':question/worked-solution'];sid=rec['generation']['source_id'];level=q[':question/difficulty'].split('/')[-1];targets=coordinates(prompt);assert len(targets)==(1 if level=='easy' else 3)
 paths=re.findall(r'!\[\]\((.*?)\)',prompt);f=q[':question/answer-fields'][0]
 if level=='easy':
  flags=[];objects=[]
  for a in f[':answer-field/choices']:
   side=json.load(open(Path(a[':answer/value']).with_suffix('.json')));st=status(side['graph'],targets[0]);flags.append(st[3]);objects.append(side['graph']);C['actual_side_limits']+=2;C['actual_values']+=1
  for a,b in itertools.combinations(objects,2):
   knots=sorted({s.Rational(part[k]) for obj in (a,b) for part in obj['segments'] for k in ('lo','hi')}|{s.Rational(v) for obj in (a,b) for v in obj['holes']+obj['poles']+list(obj['values'])})
   different=False
   for lo,hi in zip(knots,knots[1:]):
    m=(lo+hi)/2
    def on(obj):return [s.sympify(part['expr'],locals={'x':x}) for part in obj['segments'] if s.Rational(part['lo'])<m<s.Rational(part['hi'])]
    aa,bb=on(a),on(b)
    if bool(aa)!=bool(bb) or aa and s.simplify(aa[0]-bb[0])!=0:different=True;break
   if not different:
    for point in knots:
     va,vb=status(a,point)[2],status(b,point)[2]
     if (va is None)!=(vb is None) or va is not None and s.simplify(va-vb)!=0:different=True;break
   assert different,'mathematically equivalent complete graph objects';C['response_pair_checks']+=1
  assert sum(flags)==1 and [a[':answer/id'] for a,flag in zip(f[':answer-field/choices'],flags) if flag]==[f[':answer-field/correct'][1]]
 else:
  side=json.load(open(Path(paths[0]).with_suffix('.json')));flags=[status(side['graph'],a)[3] for a in targets];C['actual_side_limits']+=6;C['actual_values']+=3
  want=tuple(i for i,flag in enumerate(flags) if flag)
  choices=[tuple(i for i,label in enumerate(('I','II','III')) if re.search(r'\b'+label+r'\b',a[':answer/value'])) for a in f[':answer-field/choices']];assert len(choices)==len(set(choices))==5;C['response_pair_checks']+=10
  assert [a[':answer/id'] for a,choice in zip(f[':answer-field/choices'],choices) if choice==want]==[f[':answer-field/correct'][1]]
  bullets=[b for b in sol.split('\n\n') if b.startswith('- ')]
  assert len(bullets)==3
  for a,flag,b in zip(targets,flags,bullets):assert coordinates(b) and all(v==a for v in coordinates(b)) and ('not continuous' not in b)==flag,(sid,a,flag,b);C['solution_coordinate_components']+=len(coordinates(b))
  conclusion=re.search(r'"(.*?)"',sol)[1];assert tuple(i for i,label in enumerate(('I','II','III')) if re.search(r'\b'+label+r'\b',conclusion))==want
  if level=='hard':assert sum(a.q==2 for a in targets)>=2 and all(s.Rational(t).q==1 for t in side['tick_values']);C['hard_midpoint_readings']+=sum(a.q==2 for a in targets)
 clean=lambda z:re.sub(r'\s+',' ',re.sub(r'!\[\]\([^)]+\)|\$\$.*?\$\$|\$.*?\$','',z,flags=re.S)).strip()
 original=originals[sid][':question/worked-solution'].replace('continuous $x=','continuous at $x=');assert clean(sol)==clean(original);C['source_prose_masks']+=1
 for path in set(re.findall(r'!\[\]\((.*?)\)',sol)+paths+[a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/type']==':answer.type/image']):
  side=json.load(open(Path(path).with_suffix('.json')));graph=side['graph'];lo,hi,bottom,top=map(float,side['render_bounds']);assert lo<=0<=hi and bottom<=0<=top;C['zero_axes']+=1
  arr=np.array(Image.open(path).convert('RGB'));red=(arr[:,:,0]>160)&(arr[:,:,1]<120)&(arr[:,:,2]<120);tr=side['pixel_transform']
  def hit(a,v,filled):
   px=round(tr['x_offset']+float(a)*tr['x_scale']);py=round(tr['y_offset']+float(v)*tr['y_scale']);assert 8<px<arr.shape[1]-8 and 8<py<arr.shape[0]-8
   center=red[py-1:py+2,px-1:px+2].sum();ring=red[py-7:py+8,px-7:px+8].sum();assert ring>12 and (center>=5 if filled else center<=3);C['raster_filled_markers' if filled else 'raster_open_markers']+=1
  for a,v in graph['values'].items():
   st=status(graph,a)
   if not st[3] or a in graph.get('marked_values',[]):hit(s.Rational(a),s.Rational(v),True)
  for a in graph['holes']:
   for piece in graph['segments']:
    if s.Rational(piece['lo'])<=s.Rational(a)<=s.Rational(piece['hi']):
     v=s.sympify(piece['expr'],locals={'x':x}).subs(x,s.Rational(a))
     if v.is_finite:hit(s.Rational(a),v,False);break
 C['choices']+=5;C['records']+=1
out=dict(status='passed',source=S,readback=C,script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest());(R/f'qa/{K}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
