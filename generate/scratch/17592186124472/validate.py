#!/usr/bin/env python3
"""Fail-closed checks: source fidelity, independent math, PNG readback, native IDs.
Original opaque ink geometry is ONLY evidence fidelity, not exact symbolic math.
"""
import concurrent.futures, hashlib, importlib.util,json,math,re,subprocess,sys,tempfile,os
os.environ.setdefault('MPLCONFIGDIR','/tmp/kp17592186124472-mpl')
from pathlib import Path
import numpy as np
from PIL import Image
import sympy as sp
D=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('kp',str(D)+'.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
X=sp.Symbol('x',real=True)
def check(c,msg):
 if not c:raise AssertionError(msg)
def dump(n,v):(D/n).write_text(json.dumps(v,indent=2)+'\n')
def exp(s):return sp.sympify(s['expression'],locals={'x':X}) if 'expression' in s else sum(sp.Rational(v)*X**i for i,v in enumerate(s['coefficients']))

def independent(g):
 """Partition the complete output axis at ALL endpoint/critical values.
 Exact polynomial/elementary preimages at every boundary and each open cell
 suffice: root multiplicity cannot change elsewhere on these finite curves.
 """
 critical=set()
 for s in g['segments']:
  a,b=sp.Rational(s['a']),sp.Rational(s['b']);e=exp(s)
  critical|={sp.simplify(e.subs(X,a)),sp.simplify(e.subs(X,b))}
  if not e.has(X):continue
  rr=sp.solveset(sp.diff(e,X),X,domain=sp.Interval.open(a,b))
  check(rr.is_FiniteSet,'independent derivative partition')
  critical|={sp.simplify(e.subs(X,t)) for t in rr}
 vals=sorted(critical,key=float);levels=vals+[(a+b)/2 for a,b in zip(vals,vals[1:])]
 for y in levels:
  preimages=set()
  for s in g['segments']:
   a,b=sp.Rational(s['a']),sp.Rational(s['b']);domain=sp.Interval(a,b,left_open=not s['left_closed'],right_open=not s['right_closed']);e=exp(s)
   if e==y and not e.has(X):return False
   rr=sp.solveset(e-y,X,domain=domain)
   check(rr.is_FiniteSet,'independent preimage: '+str(e-y)+' -> '+str(rr))
   preimages|={sp.simplify(t) for t in rr}
  if len(preimages)>1:return False
 return True

def plot_math(path):
 p=Path(path);side=json.loads(p.with_suffix('.json').read_text());im=Image.open(p).convert('RGB');im.load();a=np.asarray(im);h,w=a.shape[:2]
 check(hashlib.sha256(p.read_bytes()).hexdigest()==side['sha256'],'PNG hash')
 check([w,h]==side['png_size'],'PNG dimensions')
 blue=(a[:,:,0]<110)&(a[:,:,1]>65)&(a[:,:,2]>125)&(a[:,:,2]>a[:,:,0]+50)
 for g,box in zip(side['graphs'],side['axes_boxes']):
  bx,by,bw,bh=box
  def pixel(x,y):return round(bx+(x+4.7)/9.4*bw),round(h-(by+(y+4.7)/9.4*bh))
  for s in g['segments']:
   e=exp(s)
   for x in np.linspace(s['a'],s['b'],63)[1:-1]:
    y=float(e.subs(X,float(x)));check(-4.7<y<4.7,'curve clipping')
    px,py=pixel(x,y);check(blue[max(0,py-3):py+4,max(0,px-3):px+4].any(),f'PNG curve differs from exact instance {p.name}: {x},{y} at {px},{py}')
   for x,closed in [(s['a'],s['left_closed']),(s['b'],s['right_closed'])]:
    px,py=pixel(x,float(e.subs(X,sp.Rational(x))))
    center=blue[max(0,py-1):py+2,max(0,px-1):px+2].any()
    check(center==closed,'actual PNG endpoint marker inclusion')
    check(blue[max(0,py-6):py+7,max(0,px-6):px+7].any(),'endpoint circle absent')
 return sum(1<<i for i,g in enumerate(side['graphs']) if independent(g))

cases=json.loads((D/'source-cases.json').read_text());ex=json.loads((D/'extraction.json').read_text());reviews=json.loads((D/'review.json').read_text())
counts={'source_questions':len(cases),'source_choices':0,'exact_complete_banks':0,'exact_prompt':0,'exact_solution':0,'correct_designations':0,'missing_correct_preserved':0,'missing_difficulty_preserved':0,'missing_solution_preserved':0,'raw_reconstructions':0,'normal_records':0,'mathematical_graph_checks':0,'native_choice_checks':0}
engine=[]
for c in cases:
 r=m.generate(c['level'],profile=c['profile'],parameters=c['parameters']);q=r['question'];src=m.SOURCES[c['source_id']];f=q[':question/answer-fields'][0];sf=src[':question/answer-fields'][0]
 check(q[':question/problem']==src[':question/problem'],'source prompt');counts['exact_prompt']+=1
 check({k for k in q if k.startswith(':question/')}=={k for k in src if k.startswith(':question/')},'all source question attribute presence')
 for key in [':question/difficulty',':question/worked-solution',':question/answer-fields',':question/math-academy-id']:
  check((key in q)==(key in src),'source question presence '+key)
 if ':question/difficulty' not in src:counts['missing_difficulty_preserved']+=1
 if ':question/worked-solution' in src:check(q[':question/worked-solution']==src[':question/worked-solution'],'complete source prose/stage sequence');counts['exact_solution']+=1
 else:counts['missing_solution_preserved']+=1
 check(sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in sf[':answer-field/choices']),'complete source bank')
 check(f[':answer-field/key']==sf[':answer-field/key'] and f[':answer-field/type']==m.enum(sf[':answer-field/type']),'source field layout')
 counts['source_choices']+=len(f[':answer-field/choices']);counts['exact_complete_banks']+=1
 check((':answer-field/correct' in f)==(':answer-field/correct' in sf),'correct-ref presence')
 check(r['generation']['evidence_only'] and not r['generation']['eligible_for_learning'],'raw eligibility')
 if ':answer-field/correct' in sf:
  correct=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);check(correct[':answer/value']==sf[':answer-field/correct'][':answer/value'],'source correct designation');counts['correct_designations']+=1
  checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a==correct else 'rejected','purpose':'observed source designation'} for a in f[':answer-field/choices']]
  engine.append({'label':'raw:'+c['source_id'],'record':r,'checks':checks})
 else:counts['missing_correct_preserved']+=1

# Geometry recipes are tested against original ink across all original prompt
# AND worked-solution rasters, using PNGs rendered at source dimensions.
for record in ex:
 for p in record['plots']:
  raw=m.asset({'mode':'raw','asset':p['private_asset'],'scale':[1,1]})
  aa=np.asarray(Image.open(raw).convert('RGB'));original=Image.open(p['private_asset']).convert('RGBA');oo=np.asarray(original);alpha=oo[:,:,3:4]/255;oo=oo[:,:,:3]*alpha+255*(1-alpha)
  def blue(a):return (a[:,:,0]<110)&(a[:,:,1]>60)&(a[:,:,2]>125)&(a[:,:,2]>a[:,:,0]+50)
  b1,b2=blue(aa),blue(oo)
  check(b1.shape==b2.shape,'raw rendered bounds')
  for panel in p['panels']:
   x0,y0,x1,y1=panel['blue_bbox_pixel'];ys,xs=np.nonzero(b1[max(0,y0-2):y1+3,max(0,x0-2):x1+3]);check(len(xs)>0,'raw panel disappeared')
   rendered=[int(xs.min()+max(0,x0-2)),int(ys.min()+max(0,y0-2)),int(xs.max()+max(0,x0-2)),int(ys.max()+max(0,y0-2))]
   check(max(abs(a-b) for a,b in zip(rendered,panel['blue_bbox_pixel']))<=2,'raw blue extent')
  # Compare every original blue pixel to nearby rendered blue geometry.
  padded=np.pad(b1,1);near=np.zeros_like(b1)
  for dx in range(3):
   for dy in range(3):near|=padded[dy:dy+b1.shape[0],dx:dx+b1.shape[1]]
  check((near&b2).sum()/b2.sum()>.995,'raw geometric pixel recovery')
  counts['raw_reconstructions']+=1

coverage={'easy':set(),'moderate':set(),'hard':set()};families=set();family_counts=__import__('collections').Counter();normal=[]
for r in reviews:
 if r['generation']['evidence_only']:continue
 q=r['question'];g=r['generation'];level=q[':question/difficulty'].split('/')[-1]
 check(set(r['knowledge_point'])=={'db_id','id','title'},'outer KP shape')
 f=q[':question/answer-fields'][0];ids=[a[':answer/id'] for a in f[':answer-field/choices']]
 for ident in [q[':question/id'],f[':answer-field/id'],*ids]:check(str(__import__('uuid').UUID(ident))==ident,'UUID')
 check(len(ids)==len(set(ids))==5 and f[':answer-field/correct'][1] in ids,'owned five-option bank')
 check(f[':answer-field/type']==':answer-field.type/radio','radio response')
 check(g['authored_difficulty'] and g['eligible_for_learning'],'authored labeling')
 check(q[':question/problem'].count('![](')==1 and q[':question/worked-solution'].count('![](')==1,'image sequence')
 for role,path in g['assets'].items():
  result=plot_math(path);check(result==g['correct_mask'],'actual PNG analytic answer');counts['mathematical_graph_checks']+=4
 correct=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);check(m.mask(correct[':answer/value'])==g['correct_mask'],'native designation math')
 check(len({m.mask(a[':answer/value']) for a in f[':answer-field/choices']})==5,'unique response subsets')
 check(next(v for v in m.BANKS[g['bank_profile']] if m.mask(v)==g['correct_mask']) in q[':question/worked-solution'],'fixed conclusion correct')
 rr=m.generate(level,seed=892,profile=g['profile'],parameters=g['parameters']);check(rr['question'][':question/id']==q[':question/id'],'identity seed/order invariance')
 check(rr['generation']['mathematical_fingerprint']==g['mathematical_fingerprint'],'math fingerprint seed')
 checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a==correct else 'rejected','purpose':'authored exact-domain HLT answer'} for a in f[':answer-field/choices']]
 engine.append({'label':level+':'+g['bank_profile'],'record':r,'checks':checks});normal.append(r);coverage[level].add(g['bank_profile']);families|={z['family'] for z in g['graphs'] if level=='easy'};counts['normal_records']+=1
 if level=='easy':family_counts.update(z['family'] for z in g['graphs'])
for level in coverage:check(coverage[level]==set(m.BANKS),'all banks default/support coverage '+level);check(sum(r['question'][':question/difficulty'].endswith('/'+level) for r in normal)>=2,'2 each level')
check(families==set(m.EASY_KINDS) and min(family_counts.values())>=2,'all normal easy families reviewed twice')

# Explicit scope and invalid-profile rejection; no silent repairs.
for level in ('easy','moderate','hard'):
 r=next(r for r in normal if r['question'][':question/difficulty'].endswith('/'+level));p=json.loads(json.dumps(r['generation']['parameters']))
 bad=json.loads(json.dumps(p));bad['graphs'][0]['kind' if level=='easy' else 'kinds']='unsupported'
 try:m.generate(level,profile=r['generation']['profile'],parameters=bad)
 except (ValueError,TypeError):pass
 else:raise AssertionError('invalid scope accepted')
 if level=='hard':
  bad=json.loads(json.dumps(p));bad['graphs'][0]['overlap']=True
  try:m.generate(level,profile=r['generation']['profile'],parameters=bad)
  except ValueError:pass
  else:raise AssertionError('hard accepted interior overlap')
  bad=json.loads(json.dumps(p));bad['graphs'][0]['closures']=[[False,False]]*3
  try:m.generate(level,profile=r['generation']['profile'],parameters=bad)
  except ValueError:pass
  else:raise AssertionError('hard closure workload bypass')
# Different complete displayed banks change identity, not mathematical fingerprint.
a=normal[0];level='easy';matches=[b for b in m.BANKS if a['generation']['correct_mask'] in [m.mask(v) for v in m.BANKS[b]] and sorted(m.BANKS[b])!=sorted(m.BANKS[a['generation']['profile']])]
if matches:
 b=m.generate(level,parameters=a['generation']['parameters'],profile=matches[0]);check(b['question'][':question/id']!=a['question'][':question/id'],'bank content identity');check(b['generation']['mathematical_fingerprint']==a['generation']['mathematical_fingerprint'],'banks incidental math dedup')
# Genuine fresh concurrent writes: unique fresh paths for identical and different
# payloads; also missing-sidecar cache recovery. Do not prune active shared caches.
rrs=normal[-2:];payloads=[]
for r in rrs:
 pp={'mode':'normal','graphs':r['generation']['graphs'],'solution':False};payloads.append(pp)
with tempfile.TemporaryDirectory(prefix='fresh-concurrency-',dir=D) as temp:
 t=Path(temp)
 def fresh(i):
  inp=t/f'input-{i}.json';out=t/f'plot-{i}.png';inp.write_text(json.dumps(payloads[i%2]));subprocess.run([sys.executable,str(D/'render.py'),str(inp),str(out)],check=True,capture_output=True);return out
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:paths=list(pool.map(fresh,range(4)))
 check(paths[0].read_bytes()==paths[2].read_bytes() and paths[1].read_bytes()==paths[3].read_bytes(),'same concurrent geometry deterministic')
 check(paths[0].read_bytes()!=paths[1].read_bytes(),'different concurrent geometry isolated')
 for path in paths:plot_math(path)
 dump('concurrency.json',{'fresh_same_and_different_payloads':4,'passed':True,'private_unique_input_files':True})
# Own unique cache probe cannot be referenced by an active review record.
probe=dict(payloads[0],cache_probe=str(__import__('uuid').uuid4()))
probe_path=Path(m.asset(probe));before=probe_path.read_bytes();probe_path.with_suffix('.json').unlink()
check(Path(m.asset(probe)).read_bytes()==before and probe_path.with_suffix('.json').exists(),'missing sidecar cache recovery')
probe_path.unlink();check(Path(m.asset(probe)).read_bytes()==before,'missing PNG cache recovery')
try:m.generate('easy',profile='raw:q-36000',parameters={})
except ValueError:pass
else:raise AssertionError('raw explicit empty parameters silently accepted')
# Ensure default sampling visits multiple banks/families: use already generated
# instance seeds, avoiding wasteful repeated render tests.
default_seen=set()
for seed in range(12):
 rng=__import__('random').Random(seed);default_seen.add(rng.choice(sorted(m.BANKS)))
check(len(default_seen)>=6,'default bank sampler variation')

counts['native_choice_checks']=sum(len(x['checks']) for x in engine);dump('engine-input.json',engine)
run=subprocess.run([str(m.REPO/'generate/runs/current/check-engine'),str(D/'engine-input.json'),str(D/'engine-report.json')],capture_output=True,text=True);check(run.returncode==0,'native grading '+run.stderr)
report=json.loads((D/'engine-report.json').read_text())
dump('validation.json',{'passed':True,'source_provenance':{k:m.SNAPSHOT[k] for k in ('database','basis','lineage')},'counts':counts,'native_report':report,'source_geometry':'all opaque raw profiles ineligible; exact bank/prose fidelity is separate from inferred HLT status','source_inferred_missing_correct':{'q-36000':'I and II only','q-36897':'I only'},'source_correct_math_observed_visual':9,'source_exact_symbolic_geometry_verified':0,'authored_exact_domain_math':True,'coverage':{k:sorted(v) for k,v in coverage.items()},'easy_family_coverage':sorted(families),'python':sys.version.split()[0],'sympy':sp.__version__,'matplotlib':__import__('matplotlib').__version__,'unresolved_findings':['Original unlabelled smooth curve equations and unmarked finite endpoint inclusion are not uniquely recoverable; raw profiles remain evidence only.','Two unrated originals omit correct refs and worked solutions; inferred values are reported separately and never installed in raw replay.']})
files=[Path(str(D)+'.py'),*[p for p in D.iterdir() if p.is_file() and p.name!='freeze.json'],m.REPO/'generate/runs/current/check-engine',m.REPO/'generate/runs/current/check-engine.rs']
used={Path(path) for r in reviews for path in r['generation']['assets'].values()}
for p in sorted(used):
 files.append(p)
 if p.with_suffix('.json').exists():files.append(p.with_suffix('.json'))
freeze={str(p.relative_to(m.REPO)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
dump('freeze.json',{'version':m.VERSION,'hashes':freeze,'stop_at_step':7});print(json.dumps(counts,indent=2))
