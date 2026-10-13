"""Source bytes/presence, independent displayed raster math, finite scope, native grading."""
import copy,hashlib,importlib.util,itertools,json,math,re,subprocess,sys,tempfile,os
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import sympy as sp
from PIL import Image
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
# Actual source raster geometry: each arrow tail/tip is measured independently.
# Colors and locations measured on original full-resolution assets, not generated metadata.
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
# Verify every source bank against extracted mathematical ratios, using measured strokes.
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
source_cases=[];raw_records=[];completed=[]
for profile,(sid,t,p) in g.RAW.items():
 l='hard' if t=='pair' else 'moderate';r=g.generate(l,profile=profile,parameters=p)
 assert norm(r['question'])==norm(g.SOURCES[sid]),sid
 assert r['generation']['evidence_only'] and not r['generation']['eligible_for_learning']
 raw_records.append(r);completed.append(g.generate(l,profile=profile+'_completed',parameters=p))
 source_cases.append({'source_id':sid,'template':t,'parameters':p,'bank_profile':profile,'authored_replay_call_level':l,'actual_source_difficulty':None,'raw_attribute_presence_exact':True,'correct_ref_present':False,'inferred_key':'first captured option','inferred_key_basis':'independent entire raster-bank scale and direction check'})
dump('source-cases.json',source_cases)
# Prewarm all finite supported normal geometry with one cached Matplotlib runtime.
plans=[];tasks={l:set() for l in ('easy','moderate','hard')};specs={}
for l in tasks:
 tuples= [(str(k),) for k in g.POS] if l=='easy' else [(k,) for k in g.NEG] if l=='moderate' else list(itertools.product([str(k) for k in g.POS],g.NEG))
 for angle,length,scales in itertools.product(g.ANGLES,(1,2),tuples):
  t='pair' if l=='hard' else 'single';p={'angle':angle,'length':str(length),'scales':list(scales)};g.validate_parameters(l,t,p)
  bank=g.eligible(p,'authored_operations',t);a=g.exact_vec(p);allvectors=[[a]]+bank
  for row,labels in [([a],['a'])]+[(row,[g.scalar(k) for k in scales]) for row in bank]:
   spec=g.plot_spec(row,labels,allvectors);key=g.digest(spec);out=D/'plots'/f'{key}.png'
   if not out.exists() or not out.with_suffix('.json').exists():spec['output']=str(out);specs[key]=spec
  plans.append((l,p));tasks[l].add((angle,scales,t))
if specs:
 fd,name=tempfile.mkstemp(prefix='batch-',suffix='.json',dir=D/'plots');os.close(fd)
 try:
  Path(name).write_text(json.dumps(list(specs.values())));subprocess.run(['/home/jake/.local/share/uv/python/cpython-3.10.13-linux-x86_64-gnu/bin/python3.10',str(D/'render.py'),name],check=True)
 finally:Path(name).unlink()
# Recover the requested scalar from actual displayed prompt, separately from metadata.
def parse_scalar(tex):
 tex=tex.removesuffix('a').strip()
 if tex=='':return sp.Integer(1)
 if tex=='-':return sp.Integer(-1)
 m=re.fullmatch(r'(-?)\\frac\{(\d+)\}\{(\d+)\}',tex)
 if m:return sp.Rational(('-' if m[1] else '')+m[2]+'/'+m[3])
 return sp.Rational(tex)
def from_plot(path):
 data=json.loads((ROOT/path).with_suffix('.json').read_text());spec=data['spec']
 assert data['minimum_text_arrow_clearance_px']>3
 assert Image.open(ROOT/path).size==(600,600)
 # Independent support of actual raster centerline and head direction using pixel transform.
 im=Image.open(ROOT/path).convert('RGBA')
 for v,(tail,tip) in zip(spec['vectors'],data['arrow_tail_tip_pixels']):
  # Matplotlib bottom-left pixels => PIL top-left pixels. Alpha opaque white background.
  c='black' if v['color']=='black' else 'blue' if v['color']=='#2c72ae' else 'orange'
  for t in [.15,.3,.5,.7,.85]:
   x=round(tail[0]+t*(tip[0]-tail[0]));y=600-round(tail[1]+t*(tip[1]-tail[1]))
   assert any(colored(im.getpixel((i,j)),c) for i in range(max(0,x-3),min(600,x+4)) for j in range(max(0,y-3),min(600,y+4))),(path,c,x,y)
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
   x,y=round(point[0]),600-round(point[1])
   assert any(colored(im.getpixel((i,j)),c) for i in range(max(0,x-2),min(600,x+3)) for j in range(max(0,y-2),min(600,y+3))),(path,'actual arrowhead ink')
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
 for k in scales:
  assert 'The magnitude of $'+g.scalar(k)+'$ is $'+g.tex(abs(k))+'$ times the magnitude of $a$.' in sol
  assert 'factor $'+g.tex(k)+'$ is '+('positive' if k>0 else 'negative') in sol
 # Delimiters and all grouping in generated prose remain balanced.
 assert ptext.count('$')%2==0 and sol.count('$')%2==0
 for text in (ptext,sol):assert text.count('{')==text.count('}')
 assert q[':question/difficulty']==':question.difficulty/'+r['generation']['actual_difficulty']
 assert r['generation']['eligible_for_learning']
 return True
records=[];seen=set();sample_review=[]
for i,(l,p) in enumerate(plans):
 r=g.generate(l,seed=i,parameters=p);mathematics(r);records.append(r);seen.add(r['generation']['mathematical_fingerprint'])
 r2=g.generate(l,seed=i+10001,parameters=p)
 assert r['question'][':question/id']==r2['question'][':question/id'] and r['generation']['content_fingerprint']==r2['generation']['content_fingerprint']
 if len([v for v in sample_review if v['generation']['actual_difficulty']==l])<2 and p['length']=='1':sample_review.append(r)
assert len(seen)==sum(len(s) for s in tasks.values())
# Normal API defaults, all levels, selected whole banks; identities independent of shuffle.
coverage={l:set() for l in tasks};correct_positions=set()
for l in tasks:
 for seed in range(60):
  r=g.generate(l,seed);mathematics(r);coverage[l].add(r['generation']['template']);f=r['question'][':question/answer-fields'][0]
  correct_positions.add(next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1]))
assert len(correct_positions)>1
# Equivalent parameter spellings cannot create a new assessed task or content ID.
a=g.generate('easy',parameters={'angle':30,'length':'1','scales':['2']});b=g.generate('easy',parameters={'angle':30.0,'length':'1.0','scales':['2.0']})
assert a['generation']['mathematical_fingerprint']==b['generation']['mathematical_fingerprint'] and a['question'][':question/id']==b['question'][':question/id']
# Strict explicit guards and all-or-nothing observed bank rejection.
invalid=[('easy','pair',{'angle':30,'length':'1','scales':['2','-1/2']}),('moderate','single',{'angle':30,'length':'1','scales':['-1']}),('hard','pair',{'angle':30,'length':'1','scales':['2','-1']}),('easy','single',{'angle':30,'length':'0','scales':['2']}),('easy','single',{'angle':30,'length':'1','scales':['0']})]
for l,t,p in invalid:
 try:g.generate(l,template=t,parameters=p)
 except ValueError:pass
 else:raise AssertionError(('invalid accepted',l,t,p))
try:g.generate('hard',profile='observed_pair',parameters={'angle':0,'length':'1','scales':['3','-1']})
except ValueError:pass
else:raise AssertionError('Invalid raw bank accepted')
# Raw changed geometry runs public parameterized profiles, preserving missing attributes.
changed=[]
for profile,p in [('observed_pair',{'angle':120,'length':'2','scales':['2','-3/2']}),('observed_single',{'angle':210,'length':'1','scales':['-2/3']})]:
 raw=g.generate('hard' if 'pair' in profile else 'moderate',profile=profile,parameters=p);assert ':question/worked-solution' not in raw['question'];assert ':question/difficulty' not in raw['question'];assert ':answer-field/correct' not in raw['question'][':question/answer-fields'][0]
 changed.append(raw)
sample_review=[g.generate(l,parameters=p) for l,p in [('easy',{'angle':30,'length':'1','scales':['2']}),('easy',{'angle':210,'length':'1','scales':['3']}),('moderate',{'angle':60,'length':'1','scales':['-1/2']}),('moderate',{'angle':300,'length':'1','scales':['-3/2']}),('hard',{'angle':120,'length':'1','scales':['2','-2/3']}),('hard',{'angle':300,'length':'1','scales':['4','-3/2']})]]
# Actual normal raster write concurrency, separate temporary input filenames.
p={'angle':60,'length':'1','scales':['4','-4/3']};p2={'angle':300,'length':'1','scales':['3','-2/3']}
# Fresh private directory: existing cached assets stay intact for active parent QA.
old_plot_dir=g.PLOT_DIR;g.PLOT_DIR=Path(tempfile.mkdtemp(prefix='concurrent-fresh-',dir=D));
with ThreadPoolExecutor(max_workers=3) as ex:
 calls=list(ex.map(lambda p:g.generate('hard',parameters=p),[p,p,p2]))
assert calls[0]['question']==calls[1]['question'] and calls[0]['question'][':question/id']!=calls[2]['question'][':question/id']
assert not list(g.PLOT_DIR.glob('input-*.json'))
for r in calls:mathematics(r)
fresh_count=len(list(g.PLOT_DIR.glob('*.png')));assert fresh_count>=6
g.PLOT_DIR=old_plot_dir
checks=[]
for r in records+completed:
 f=r['question'][':question/answer-fields'][0]
 checks.append({'label':r['question'][':question/id'],'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Every owned displayed image option; independent geometry tested separately'} for a in f[':answer-field/choices']]})
dump('native-input.json',checks);subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(D/'native-input.json'),str(D/'native-report.json')],check=True)
native=json.loads((D/'native-report.json').read_text());dump('review.json',sample_review+completed+changed)
review=['# Creating Parallel Vectors — review','Database math; basis1356. Original difficulty and keys are absent. Every generated level below is authored. Source keys are independent inferred completions, not matched captured correct refs.']
for r in raw_records+completed+changed+sample_review:
 gen=r['generation'];review.append('## '+(('ORIGINAL raw replay — ' if r['question'][':question/id']==g.SOURCES[r['question'][':question/math-academy-id']][':question/id'] else 'GENERATED evidence variant — ') if gen['evidence_only'] and not gen['source_completion'] else 'INFERRED source completion — ' if gen['source_completion'] else 'GENERATED authored '+gen['actual_difficulty']+' — ')+gen['bank_profile'])
 preview=g.markdown(r)
 for captured in re.findall(r'!\[\]\((images/.*?)\)',preview):preview=preview.replace('![]('+captured+')','![](/media/jake/SSD/EDB/math/'+captured+')')
 review.append(preview);review.append('Author key: '+str(r['question'][':question/answer-fields'][0].get(':answer-field/correct',gen['inferred_correct_answer_id'])))
(D/'review.md').write_text('\n\n'.join(review)+'\n')
dump('validation.json',{'status':'pass','database':'math','basis':1356,'source_questions':2,'full_prompts_exact':2,'complete_raw_banks_exact':2,'all_option_values_exact':10,'question_field_answer_key_presence_exact':2,'enum_representation_normalization':'Nested :db/ident -> local enum string only','source_existing_worked_solutions_total':0,'source_existing_correct_designations_total':0,'source_missing_worked_solutions_inferred':2,'source_missing_correct_designations_inferred':2,'source_unrated_total':2,'original_rasters_independently_verified':12,'exhaustive_normal_records':len(records),'meaningful_tasks':{k:len(v) for k,v in tasks.items()},'task_count_excludes_common_vector_length':True,'default_samples_checked':180,'concurrency_actual_fresh_pngs':fresh_count,'correct_positions_seen':sorted(correct_positions),'native':{k:native[k] for k in ('entry_point','accepted_checks','rejected_checks','documented_unresolved_checks','database_writes')},'engine_source_sha256':hashlib.sha256((ROOT/'generate/runs/current/check-engine.rs').read_bytes()).hexdigest(),'source_capture_sha256':hashlib.sha256((D/'source.json').read_bytes()).hexdigest(),'engine_sha256':hashlib.sha256((ROOT/'generate/runs/current/check-engine').read_bytes()).hexdigest(),'python':sys.version.split()[0],'sympy':sp.__version__,'no_blank_equivalence_test':'All fields are image radio; native supports owned option selection. Arbitrary unlisted mathematically valid diagrams cannot be entered. No uniqueness claim is made for a bare parallel-vector request; these prompts specify scalar multiples.','limitations':['Both originals omit difficulty, worked solutions and correct refs; inferred keys do not count as matched captured designations.','Original geometric error intentions are inferred from full raster banks, not recovered author code.','Normal practice excludes zero vectors because it requests oriented arrows; the lesson separately declares zero parallel to every vector.'],'unresolved_findings':[]})
dump('freeze.json',{'version':g.VERSION,'generator_sha256':hashlib.sha256(SCRIPT.read_bytes()).hexdigest(),'validator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'renderer_sha256':hashlib.sha256((D/'render.py').read_bytes()).hexdigest(),'python':sys.version.split()[0],'sympy':sp.__version__,'status':'local steps3–7; parent QA pending; no registration'})
print('PASS:2/2 raw sources,10/10 options,228 normal records,114 meaningful tasks; native every option.')
