"""Parent graph readback: actual linked PNGs/endpoints, axes, field contexts and source banks."""
import sys,importlib.util,json,re,hashlib
from pathlib import Path
from PIL import Image,ImageDraw
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186138429;D=R.parents[2]/f'generate/scratch/{K}-draft';SCRIPT_SHA=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest()
spec=importlib.util.spec_from_file_location('parent_word_draft',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
# Source raster geometry reviewed separately; walker slopes are explicitly authored.
original={'cars':(80,s.Rational(-3,4),40,s.Rational(-1,4)),'trucks':(0,50,750,-75),'pools':(150,50,775,-75),'planes':(4,s.Rational(4,3),0,s.Rational(5,3)),'tanks':(25,s.Rational(-5,2),5,s.Rational(5,2)),'walkers':(0,s.Rational(300,11),960,-60)}
units={'cars':('Distance (m)','Speed (km/h)','meters'),'trucks':('Hours','Miles','hours'),'pools':('Days','Liters','days'),'planes':('Minutes','Feet (thousands)','minutes'),'tanks':('Minutes','Liters','minutes'),'walkers':('Time (minutes)','Distance (meters)','minutes')}
C=dict(records=0,linked_graphs=0,pixel_samples=0,source_banks=0,source_fields=0,source_values=0,source_keys=0,source_solutions=0);tasks={k:set() for k in units};visual={}
def check(r):
 q=r['question'];name=r['generation']['template'];assets=r['generation']['plot_assets'];graphs=[]
 for role,text in [('prompt',q[':question/problem']),('solution',q[':question/worked-solution'])]:
  refs=re.findall(r'!\[[^\]]*\]\(([^)]+)\)',text);assert len(refs)==1;png=D/refs[0];assert png==Path(assets[role]['path']) and png.read_bytes().startswith(b'\x89PNG')
  if png.with_suffix('.json').exists():
   v=json.loads(png.with_suffix('.json').read_text());par=v['parameters'];lines=[]
   assert v['annotated']==(role=='solution');assert (v['labels']['x_label'],v['labels']['y_label'])==units[name][:2]
   im=Image.open(png).convert('RGB');w,h=im.size;pixels=im.load()
   for key,color in zip(('a','b'),((0,0,255),(255,0,0)) if name=='walkers' else ((237,166,0),(36,116,180))):
    (x0,y0),(x1,y1)=[[s.Rational(z) for z in pair] for pair in v['plotted_line_endpoints'][key]];slope=(y1-y0)/(x1-x0);intercept=y0-slope*x0;lines.append((intercept,slope));assert y0>=0 and y1>=0
    assert (y0<s.Rational(par['ymax']) and y1<s.Rational(par['ymax'])) or name=='planes' and (intercept,slope) in ((s.Integer(4),s.Rational(4,3)),(s.Integer(0),s.Rational(5,3)))
    assert x0==0 and x1==(min(s.Rational(par['xmax']),-intercept/slope) if name=='walkers' and slope<0 else s.Rational(par['xmax']))
    # Raster samples prove linked image lines agree with independently read endpoint equations.
    hits=0;tested=0
    for fraction in (s.Rational(7,20),s.Rational(11,20),s.Rational(17,20)):
     x=x0+(x1-x0)*fraction;y=intercept+slope*x;px=round(w*(.14+.82*float(x/s.Rational(par['xmax']))));py=round(h*(.84-.77*float(y/s.Rational(par['ymax']))))
     if role=='solution' and abs(float(x-s.Rational(v['intersection'][0])))*w*.82/float(s.Rational(par['xmax']))<12:continue
     tested+=1;hit=any(sum(abs(pixels[i,j][k]-color[k]) for k in range(3))<70 for i in range(px-4,px+5) for j in range(py-4,py+5));hits+=hit;C['pixel_samples']+=int(hit)
    assert hits>=min(2,tested),(name,role,key,hits,tested)
   ticks=list(range(0,int(par['xmax'])+1,int(par['dx'])));assert v['grid_x_ticks']==ticks and v['numbered_x_ticks']==[x for x in ticks if x and x%int(par['xlabel_step'])==0]
   (a,b),(c,d)=lines;t=(c-a)/(b-d);y=a+b*t;assert tuple(map(s.Rational,v['intersection']))==(t,y)
   assert v['annotation_point']==([str(t),str(y)] if role=='solution' else None)
  else:
   assert assets[role]['renderer']=='captured PNG';a,b,c,d=map(s.Rational,original[name]);t=(c-a)/(b-d);y=a+b*t
   assert tuple(map(s.Rational,assets[role]['geometry']['intersection']))==(t,y),(name,role,assets[role]['geometry']['intersection'],t,y)
   sourcepng=Path('/media/jake/SSD/EDB/math/images')/Path(refs[0]).relative_to('images');assert hashlib.sha256(sourcepng.read_bytes()).digest()==hashlib.sha256(png.read_bytes()).digest()
  graphs.append((t,y));C['linked_graphs']+=1
 assert graphs[0]==graphs[1];t,y=graphs[0]
 sol=q[':question/worked-solution'];assert re.search(r'point \$\('+str(t)+','+str(y)+r'\)\.?\$',sol)
 assert units[name][2] in q[':question/problem'] and units[name][2] in sol
 assert sol.index('intersect')<sol.index('![]')<sol.index('In this case')<sol.index('So,')
 fields=q[':question/answer-fields'];assert len(fields)==(2 if name=='walkers' else 1)
 for f in fields:
  expected=y if name=='walkers' and f[':answer-field/key']=='field-2' else t
  choices=f[':answer-field/choices'];vals=[s.Rational(a[':answer/value'].removesuffix('h')) for a in choices];assert len(set(vals))==len(vals)
  assert [a[':answer/id'] for a,v in zip(choices,vals) if v==expected]==[f[':answer-field/correct'][1]]
  if f[':answer-field/type'].endswith('/blank'):
   assert '{{'+f[':answer-field/key']+'}}' in q[':question/problem'];assert len(choices)==1
   if name=='walkers':assert re.search(r'\{\{field-1\}\}[^{}]*minutes.*\{\{field-2\}\}[^{}]*meters',q[':question/problem'],re.S)
  else:
   assert len(choices)==5
   if r['generation']['bank_profile']=='adjacent_grid':assert set(vals)=={t+k*s.Rational(r['generation']['parameters']['dx']) for k in (-2,-1,0,1,2)}
 if name=='planes':assert f'{int(y)*1000:,}' in sol and f'${t}$ minutes' in sol
 if name=='tanks':assert f'$t={t}$ minutes' in sol and f'${y}\\,' in sol
 if name=='walkers':assert f'${t}$ minutes' in sol and f'${y}\\,' in sol and 'Mary and Sam met' in sol
 tasks[name].add(tuple(graphs[0])+tuple(s.Rational(r['generation']['parameters'][k]) for k in ('a0','a1','b0','b1')));C['records']+=1;visual.setdefault(name,Path(assets['solution']['path']));return q
source={q[':question/math-academy-id']:q for q in json.loads((D/'source.json').read_text())['record'][':knowledge-point/questions'] if ':question/math-academy-id' in q}
for case in json.loads((D/'source-cases.json').read_text()):
 q=check(g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']));old=source[case['source_id']];assert old[':question/problem']==q[':question/problem']
 for f in q[':question/answer-fields']:
  of=next(of for of in old[':question/answer-fields'] if of[':answer-field/key']==f[':answer-field/key'])
  assert f[':answer-field/key']==of[':answer-field/key'];assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in of[':answer-field/choices']);C['source_fields']+=1;C['source_values']+=len(f[':answer-field/choices'])
  if of.get(':answer-field/correct'):assert of[':answer-field/correct'][':answer/value']==next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);C['source_keys']+=1
 if old.get(':question/worked-solution'):
  normalize=lambda text:re.sub(r'!\[\]\(.*?\)','<PLOT>',text).replace('Mary and her brother','Mary and Sam');assert normalize(q[':question/worked-solution'])==normalize(old[':question/worked-solution']);C['source_solutions']+=1
 C['source_banks']+=1
for r in json.loads((D/'revalidation-sampled.json').read_text())+json.loads((R/'qa'/f'{K}-sampled.json').read_text()):check(r)
assert {r['generation']['template'] for r in g.batch('easy',count=18,seed=42)}=={'trucks','planes','tanks','walkers'}
for level,n in [('moderate',22),('hard',24)]:
 batch=g.batch(level,count=n,seed=42);assert len({r['generation']['parameter_fingerprint'] for r in batch})==n
 for r in batch:check(r)
for fn in [lambda:g.generate('easy',True),lambda:g.batch('easy',count=True),lambda:g.batch('moderate',count=23),lambda:g.batch('hard',count=25)]:
 try:fn()
 except ValueError:pass
 else:raise AssertionError('strict guard failed')
# Compact source/normal solution contact sheets for independent visual inspection.
for label,files in [('solutions',list(visual.items())),('originals',[(name,D/re.search(r'!\[\]\((.*?)\)',source[next(c['source_id'] for c in json.loads((D/'source-cases.json').read_text()) if c['template']==name)][':question/problem'])[1]) for name in ('cars','trucks','planes','tanks','walkers')])]:
 sheet=Image.new('RGB',(1200,3*490),'white');draw=ImageDraw.Draw(sheet)
 for i,(name,path) in enumerate(files):
  im=Image.open(path).convert('RGB');im.thumbnail((590,460));x=(i%2)*600;y=(i//2)*490;draw.text((x+5,y+3),name,fill='black');sheet.paste(im,(x,y+25))
 sheet.save(R/'qa'/f'{K}-root-{label}.png')
assert hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest()==SCRIPT_SHA
proof={'status':'passed','script_sha256':SCRIPT_SHA,'source_and_readback':C,'sampled_actual_tasks':{k:len(v) for k,v in tasks.items()},'scope':'All source contexts read line intersections with contextual units, no learner algebra solving. Authored M/H tick-reading workloads retain graph-reading skill; exact walker slopes explicitly authored, captured point and colors preserved.','database_writes':0};(R/'qa'/f'{K}-root-readback.json').write_text(json.dumps(proof,indent=2)+'\n');print(proof)
