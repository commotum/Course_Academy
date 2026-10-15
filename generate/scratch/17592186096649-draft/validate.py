"""Source bytes/presence, independent displayed raster math, finite scope, native grading."""

import copy,hashlib,importlib.util,itertools,json,math,re,subprocess,sys,tempfile,os

from concurrent.futures import ThreadPoolExecutor

from pathlib import Path

import sympy as sp
from functools import lru_cache

from PIL import Image,ImageDraw

sys.dont_write_bytecode=True

D=Path(__file__).resolve().parent;ROOT=D.parents[2];SCRIPT=D.with_suffix('.py')

spec=importlib.util.spec_from_file_location('generator',SCRIPT);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

def dump(name,obj):(D/name).write_text(json.dumps(obj,indent=2)+'\n')

def norm(q):
 q=copy.deepcopy(q)
 for f in q.get(':question/answer-fields',[]):
  f[':answer-field/type']=f[':answer-field/type'].get(':db/ident') if isinstance(f[':answer-field/type'],dict) else f[':answer-field/type']
  for a in f[':answer-field/choices']:
   if isinstance(a[':answer/type'],dict):a[':answer/type']=a[':answer/type'][':db/ident']
  f[':answer-field/choices']=sorted(f[':answer-field/choices'],key=lambda a:a[':answer/id'])
 return q

SOURCE_GEOMETRY={
'q-11324':[
 [('black',(0,50),(86,0))],
 [('blue',(0,149),(256,0)),('orange',(99,148),(14,197))],
 [('blue',(0,149),(256,0)),('orange',(99,148),(197,148))],
 [('blue',(72,50),(157,0)),('orange',(171,49),(0,148))],
 [('blue',(0,50),(85,0)),('orange',(99,49),(14,98))],
 [('blue',(98,50),(183,0)),('orange',(197,74),(0,74))]],
'q-12140':[
 [('black',(0,171),(99,0))],
 [('orange',(50,0),(0,86))],
 [('orange',(99,0),(0,171))],
 [('orange',(0,47),(99,47))],
 [('orange',(98,4),(0,4))],
 [('orange',(0,171),(100,0))]]}

def colored(px,color):
 r,bg,b,a=px
 if a<100:return False
 return max(r,bg,b)<90 if color=='black' else b>r+40 and b>bg+10 if color=='blue' else r>200 and 70<bg<210 and b<70

def parse_scalar(tex):
 tex=tex.removesuffix('a').strip()
 if tex=='':return sp.Integer(1)
 if tex=='-':return sp.Integer(-1)
 m=re.fullmatch(r'(-?)\\frac\{(\d+)\}\{(\d+)\}',tex)
 if m:return sp.Rational(('-' if m[1] else '')+m[2]+'/'+m[3])
 return sp.Rational(tex)

@lru_cache(maxsize=None)
def from_plot(path):
 data=json.loads((ROOT/path).with_suffix('.json').read_text());spec=data['spec']
 assert data['minimum_text_arrow_clearance_px']>3
 assert Image.open(ROOT/path).size==(data['width'],data['height'])
 width,height=data['width'],data['height']
 # Independent support of actual raster centerline and head direction using pixel transform.
 im=Image.open(ROOT/path).convert('RGBA')
 for v,(tail,tip) in zip(spec['vectors'],data['arrow_tail_tip_pixels']):
  # Matplotlib bottom-left pixels => PIL top-left pixels. Alpha opaque white background.
  c='black' if v['color']=='black' else 'blue' if v['color']=='#2c72ae' else 'orange'
  for t in [.15,.3,.5,.7,.85]:
   x=round(tail[0]+t*(tip[0]-tail[0]));y=height-round(tail[1]+t*(tip[1]-tail[1]))
   assert any(colored(im.getpixel((i,j)),c) for i in range(max(0,x-3),min(width,x+4)) for j in range(max(0,y-3),min(height,y+4))),(path,c,x,y)
  # Read the actual drawn patch path, not merely intended endpoints. Triangle
  # vertex4 is the tip;3/5 are its rear wings (Matplotlib -|> closed path).
  vertices=data['patch_vertices_pixels'][spec['vectors'].index(v)]
  codes=data['patch_codes'][spec['vectors'].index(v)]
  assert codes==[1,3,3,1,2,2,79]
  left,head,right=vertices[3:6];centre=[(left[i]+right[i])/2 for i in range(2)]
  direction=[tip[i]-tail[i] for i in range(2)]
  assert sum((head[i]-centre[i])*direction[i] for i in range(2))>0
  assert math.dist(head,tip)<4,'bounded stroke-width/arrowcap endpoint allowance'
  assert math.dist(vertices[0],tail)<1e-8
  # Actual rendered solid triangle must contain ink at its centroid and tip.
  for point in [head,[(left[i]+head[i]+right[i])/3 for i in range(2)]]:
   x,y=round(point[0]),height-round(point[1])
   assert any(colored(im.getpixel((i,j)),c) for i in range(max(0,x-2),min(width,x+3)) for j in range(max(0,y-2),min(height,y+3))),(path,'actual arrowhead ink')
 return spec

def mathematics(r):
 q=r['question'];assert set(r['knowledge_point'])=={'db_id','id','title'}
 ptext=q[':question/problem'];pimage=re.findall(r'!\[\]\((.*?)\)',ptext)[0]
 pplot=from_plot(pimage);a=pplot['vectors'][0]['vector']
 tail=ptext.split('Which of the following diagrams shows ')[1]
 scales=[parse_scalar(x) for x in re.findall(r'\$(.*?)\$',tail)]
 # Complete criterion is labelled specified multiples, not mere parallelism.
 f=q[':question/answer-fields'][0];valid=[];bank=[]
 for ans in f[':answer-field/choices']:
  plot=from_plot(ans[':answer/value']);vs=plot['vectors'];assert len(vs)==len(scales)
  assert [parse_scalar(v['label']) for v in vs]==scales
  assert plot['bounds']==pplot['bounds'],'scale must agree between prompt and all choices'
  key=tuple(tuple(round(c,8) for c in v['vector']) for v in vs);bank.append(key)
  valid.append(all(math.dist(v['vector'],[float(k)*c for c in a])<1e-8 for v,k in zip(vs,scales)))
  if valid[-1]:assert ans[':answer/id']==f[':answer-field/correct'][1]
 assert sum(valid)==1 and len(set(bank))==5
 sol=q[':question/worked-solution'];assert sol.count('- The magnitude')==len(scales)
 for i,k in enumerate(scales):
  assert ('Now' if i==0 else 'Next')+', for the vector $'+g.scalar(k)+'$ we have the following:' in sol
  assert 'The magnitude of $'+g.scalar(k)+'$ is $'+g.tex(abs(k))+'$ times the magnitude of $a$.' in sol
  assert 'Vectors $a$ and $'+g.scalar(k)+'$ have '+('the same direction' if k>0 else 'opposite directions')+' since the factor $'+g.tex(k)+'$ is '+('positive' if k>0 else 'negative')+'.' in sol
 # Delimiters and all grouping in generated prose remain balanced.
 assert ptext.count('$')%2==0 and sol.count('$')%2==0
 for text in (ptext,sol):assert text.count('{')==text.count('}')
 assert q[':question/difficulty']==':question.difficulty/'+r['generation']['actual_difficulty']
 assert r['generation']['eligible_for_learning']
 return True


def main():
 import shutil
 source_plots=[]

 for sid,shapes in SOURCE_GEOMETRY.items():
  q=g.SOURCES[sid];paths=re.findall(r'!\[\]\((.*?)\)',q[':question/problem'])+[a[':answer/value'] for a in q[':question/answer-fields'][0][':answer-field/choices']]
  for path,arrows in zip(paths,shapes):
   im=Image.open('/media/jake/SSD/EDB/math/'+path).convert('RGBA');checks=[]
   for color,tail,tip in arrows:
    # Every sampled centerline point is supported by the actual raster stroke.
    for t in [i/20 for i in range(2,19)]:
     x=round(tail[0]+t*(tip[0]-tail[0]));y=round(tail[1]+t*(tip[1]-tail[1]))
     assert any(colored(im.getpixel((i,j)),color) for i in range(max(0,x-2),min(im.width,x+3)) for j in range(max(0,y-2),min(im.height,y+3))),(path,color,t)
    # Tip has the wider arrow head; tail has no corresponding flared head.
    vx,vy=tip[0]-tail[0],tip[1]-tail[1];n=math.hypot(vx,vy);nx,ny=-vy/n,vx/n
    def flare(end,inward):
     count=0
     for back in range(3,10):
      cx=end[0]+inward*vx/n*back;cy=end[1]+inward*vy/n*back
      for side in (-1,1):
       for off in range(3,6):
        x,y=round(cx+side*nx*off),round(cy+side*ny*off)
        if 0<=x<im.width and 0<=y<im.height and colored(im.getpixel((x,y)),color):count+=1
     return count
    head,tailhead=flare(tip,-1),flare(tail,1)
    assert head>tailhead,(path,color,'arrow direction',head,tailhead)
    checks.append({'color':color,'tail':tail,'tip':tip,'head_flare_pixels':head,'tail_flare_pixels':tailhead})
   source_plots.append({'path':path,'size':im.size,'sha256':hashlib.sha256(Path('/media/jake/SSD/EDB/math/'+path).read_bytes()).hexdigest(),'arrows':checks})

 for sid,shapes in SOURCE_GEOMETRY.items():
  raw=shapes[0][0];base=(raw[2][0]-raw[1][0],-(raw[2][1]-raw[1][1]));unit=math.hypot(*base)
  p=g.RAW['observed_pair' if sid=='q-11324' else 'observed_single'][2];a=g.exact_vec(p)
  bank=g.bank_vectors(p,'observed_pair' if sid=='q-11324' else 'observed_single','pair' if sid=='q-11324' else 'single')
  for measured,expected in zip(shapes[1:],bank):
   for arrow,v in zip(measured,expected):
    got=((arrow[2][0]-arrow[1][0])/unit,-(arrow[2][1]-arrow[1][1])/unit)
    want=(float(v[0])/float(sp.Rational(p['length'])),float(v[1])/float(sp.Rational(p['length'])))
    assert math.dist(got,want)<.035,(sid,got,want)

 dump('source-raster-checks.json',source_plots)

 capture=json.loads((D/'source.json').read_text());original=[q for q in capture['record'][':knowledge-point/questions'] if ':question/math-academy-id' in q];ind=[q for q in capture['record'][':knowledge-point/questions'] if ':question/math-academy-id' not in q]
 assert json.loads((D/'source-cases.json').read_text())==[{'source_id':q[':question/math-academy-id'],'record':q} for q in original]
 assert [q['record'] for q in json.loads((D/'independent-inventory.json').read_text())['questions']]==ind
 raw=[];completed=[]
 for profile,(sid,t,p) in g.RAW.items():
  l='hard' if t=='pair' else 'moderate';r=g.generate(l,profile=profile,parameters=p);assert norm(r['question'])==norm(g.SOURCES[sid]);raw.append(r);completed.append(g.generate(l,profile=profile+'_completed',parameters=p))
 # Render all owned compact assets in one Matplotlib process.
 specs={};(D/'plots').mkdir(exist_ok=True)
 for l in ('easy','moderate','hard'):
  scales=[(str(k),) for k in g.POS] if l=='easy' else [(k,) for k in g.NEG] if l=='moderate' else list(itertools.product([str(k) for k in g.POS],g.NEG))
  for angle,length,ks in itertools.product(g.ANGLES,('1','2'),scales):
   p={'angle':angle,'length':length,'scales':list(ks)};t='pair' if l=='hard' else 'single';a=g.exact_vec(p);b=g.eligible(p,'authored_operations',t);allvectors=[[a]]+b
   for row,labels in [([a],['a'])]+[(row,[g.scalar(k) for k in ks]) for row in b]:
    spec=g.plot_spec(row,labels,allvectors);key=g.digest(spec);out=D/'plots'/f'{key}.png'
    if not out.exists() or not out.with_suffix('.json').exists():spec['output']=str(out.resolve());specs[key]=spec
 if specs:
  dump('render-input.json',list(specs.values()));subprocess.run(['/home/jake/.local/share/uv/python/cpython-3.10.13-linux-x86_64-gnu/bin/python3.10',str(D/'render.py'),str(D/'render-input.json')],check=True)
 records=[];tasks={l:set() for l in ('easy','moderate','hard')};positions=set()
 for l in tasks:
  scales=[(str(k),) for k in g.POS] if l=='easy' else [(k,) for k in g.NEG] if l=='moderate' else list(itertools.product([str(k) for k in g.POS],g.NEG))
  for angle,length,ks in itertools.product(g.ANGLES,('1','2'),scales):
   p={'angle':angle,'length':length,'scales':list(ks)};r=g.generate(l,parameters=p);mathematics(r);assert Image.open(ROOT/re.findall(r'!\[\]\((.*?)\)',r['question'][':question/problem'])[0]).size==(180,180);records.append(r);tasks[l].add(r['generation']['mathematical_fingerprint'])
   r2=g.generate(l,seed=999,parameters=p);assert r['question'][':question/id']==r2['question'][':question/id'];f=r2['question'][':question/answer-fields'][0];positions.add(next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1]))
 assert {k:len(v) for k,v in tasks.items()}=={'easy':18,'moderate':24,'hard':72}
 # Full previous saved normal records must retain their exact public questions.
 prior=json.loads((D.with_name('17592186096649')/'review.json').read_text());preserved=0
 for old in prior:
  if old['generation']['evidence_only']:continue
  new=g.generate(old['generation']['actual_difficulty'],seed=old['generation']['seed'],parameters=old['generation']['parameters']);assert new['generation']['parameters']==old['generation']['parameters'];assert new['question'][':question/problem'].split('\n\n',1)[1]==old['question'][':question/problem'].split('\n\n',1)[1];preserved+=1
 invalid=0
 for bad in (True,False,0.5,'1',None):
  for call in (lambda:g.generate('easy',seed=bad),lambda:g.batch('easy',1,seed=bad),lambda:g.batch('easy',bad)):
   try:call()
   except ValueError:invalid+=1
   else:raise AssertionError(('invalid seed/count accepted',bad))
 try:g.batch('easy',-1)
 except ValueError:invalid+=1
 else:raise AssertionError('negative count')
 assert len(g.batch('easy',1000))==18 and g.batch('easy',0)==[]
 for l in tasks:
  assert len({r['generation']['mathematical_fingerprint'] for r in g.batch(l,1000)})==len(tasks[l])
 for fmt in ('json','markdown'):
  cmd=[sys.executable,str(SCRIPT),'--difficulty','all','--count','1','--format',fmt];out=subprocess.check_output(cmd,text=True)
  (D/('cli-all-1.'+('json' if fmt=='json' else 'md'))).write_text(out)
  if fmt=='json':assert len(json.loads(out))==3
 # Finite domain boundaries and whole-bank collisions are rejected before rendering.
 for l,t,p in [('easy','pair',{'angle':30,'length':'1','scales':['2','-1/2']}),('moderate','single',{'angle':30,'length':'1','scales':['-1']}),('hard','pair',{'angle':30,'length':'1','scales':['2','-1']}),('easy','single',{'angle':30,'length':'0','scales':['2']}),('easy','single',{'angle':30,'length':'1','scales':['0']})]:
  try:g.generate(l,template=t,parameters=p)
  except ValueError:pass
  else:raise AssertionError('out-of-domain instance accepted')
 try:g.generate('hard',profile='observed_pair',parameters={'angle':0,'length':'1','scales':['3','-1']})
 except ValueError:pass
 else:raise AssertionError('colliding complete bank accepted')
 for count in ('0','-1'):
  out=subprocess.run([sys.executable,str(SCRIPT),'--count',count,'--format','json'],capture_output=True,text=True)
  assert (out.returncode==0 and json.loads(out.stdout)==[]) if count=='0' else out.returncode!=0
 # Negative controls keep the final answer ID unchanged.
 sample=next(r for r in records if r['generation']['actual_difficulty']=='hard');mutations=[]
 for name,before,after in [('magnitude','times the magnitude','plus the magnitude'),('direction','opposite directions','the same direction'),('intermediate-vector','Next, for the vector $','Next, for the vector $7')]:
  r=copy.deepcopy(sample);r['question'][':question/worked-solution']=r['question'][':question/worked-solution'].replace(before,after)
  try:mathematics(r)
  except AssertionError:mutations.append(name)
  else:raise AssertionError(('uncaught mutation',name))
 # A full correct-key vector geometry or label substitution must fail.
 for name in ('label','scaled-length','plot-geometry'):
  r=copy.deepcopy(sample);f=r['question'][':question/answer-fields'][0];a=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);path=ROOT/a[':answer/value'];bad=D/('negative-'+name+'.png');shutil.copy2(path,bad);data=json.loads(path.with_suffix('.json').read_text())
  if name=='label':data['spec']['vectors'][0]['label']='7a'
  elif name=='scaled-length':data['spec']['vectors'][0]['vector'][0]+=1
  else:
   im=Image.open(bad).convert('RGBA');im.paste('white',(0,0,180,180));im.save(bad)
  bad.with_suffix('.json').write_text(json.dumps(data));a[':answer/value']=str(bad.relative_to(ROOT))
  try:mathematics(r)
  except AssertionError:mutations.append(name)
  else:raise AssertionError(('uncaught mutation',name))
 checks=[];diagnostics=[]
 for r in records+completed:
  f=r['question'][':question/answer-fields'][0];answers=f[':answer-field/choices'];ci=next(i for i,a in enumerate(answers) if a[':answer/id']==f[':answer-field/correct'][1]);n=100+ci
  cs=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if i==ci else 'rejected','purpose':'Every displayed full-image option'} for i,a in enumerate(answers)]
  cs += [{'submitted':str(n).zfill(6),'expected':'accepted','purpose':'Equivalent decimal ID with leading zeros'},{'submitted':'+'+str(n),'expected':'accepted','purpose':'Equivalent decimal ID explicit plus'},{'submitted':'999999','expected':'unresolved','purpose':'Unknown image choice ID'},{'submitted':'a','expected':'unresolved','purpose':'Unsupported typed-math diagnostic; image radio has no typed-math interface'}]
  checks.append({'label':r['question'][':question/id'],'record':r,'checks':cs[:7]})
  diagnostics.append({'label':r['question'][':question/id'],'record':r,'checks':cs[7:]})
 dump('native-diagnostics-input.json',diagnostics);subprocess.run([str(D/'check-engine'),str(D/'native-diagnostics-input.json'),str(D/'native-diagnostics-report.json')],check=True)
 dump('native-input.json',checks);subprocess.run([str(D/'check-engine'),str(D/'native-input.json'),str(D/'native-report.json')],check=True)
 review=[g.generate(l,parameters=p) for l,p in [('easy',{'angle':30,'length':'1','scales':['2']}),('easy',{'angle':210,'length':'1','scales':['3']}),('moderate',{'angle':60,'length':'1','scales':['-1/2']}),('moderate',{'angle':300,'length':'1','scales':['-3/2']}),('hard',{'angle':120,'length':'1','scales':['2','-2/3']}),('hard',{'angle':300,'length':'1','scales':['4','-3/2']})]]
 dump('review.json',review);dump('all-records.json',records);dump('source-completions.json',completed)
 (D/'review.md').write_text('\n\n---\n\n'.join(g.markdown(r) for r in raw+completed+review))
 dump('validation.json',{'status':'pass','basis':2275,'original_MA_sources':2,'exact_raw_source_banks':2,'exact_raw_source_options':10,'matched_captured_correct_refs':0,'missing_source_keys_solutions_difficulty':2,'independent_inventory_exact_records':len(ind),'exhaustive_normal_records':len(records),'meaningful_tasks':{k:len(v) for k,v in tasks.items()},'prior_saved_normal_math_and_prose_preserved_with_presentation_repair':preserved,'strict_invalid_seed_count_rejections':invalid,'negative_controls_detected':mutations,'canonical_illustration_adaptation':'Both ordered magnitude/direction stages retained. Existing generated combined final illustration preserved; not exact canonical stage-image replay.','source_raster_checks':len(source_plots),'parent_QA':'pending'})
 print('PASS',len(records),'normal presentations,',sum(len(v) for v in tasks.values()),'tasks;',len(mutations),'negative controls')

if __name__=='__main__':main()
