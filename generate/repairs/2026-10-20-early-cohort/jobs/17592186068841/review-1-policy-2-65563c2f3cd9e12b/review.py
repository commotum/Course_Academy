import sys,json,hashlib,importlib.util,shutil,re,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parent
JOB=ROOT.parent
REPO=Path('/home/jake/Developer/Course_Academy')
PKG=JOB/'workspace'
sys.dont_write_bytecode=True
sys.path.insert(0,str(REPO))
def save(n,x):
 p=ROOT/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def load(n):return json.loads((ROOT/n).read_text())
def module():
 spec=importlib.util.spec_from_file_location('reviewed_generator',PKG/'17592186068841.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def sample():
 save('package-before.json',{str(p.relative_to(PKG)):hashlib.sha256(p.read_bytes()).hexdigest() for p in PKG.rglob('*') if p.is_file()})
 m=module(); batch=json.loads((JOB/'samples.json').read_text());save('batch.json',batch)
 records=[]; errors=[]
 # Entire small easy domain, a justified sign/boundary/shape grid, not random uniqueness counts.
 for name in ['easy_linear','easy_constant']:
  for a in [-12,-2,-1,1,2,12]:
   try:records.append(m.generate('easy',seed=730031,template=name,parameters={'a':a}))
   except Exception as e:errors.append({'template':name,'a':a,'error':repr(e)})
 save('easy-grid.json',records)
 # Source defaults plus a boundary for every captured family; fresh seed, default banks.
 normal=[]; replay=[]; replay_results=[]
 src=json.loads((JOB/'source/source.json').read_text())
 for q in src['material']['kp'][':knowledge-point/questions']:
  name=q[':question/math-academy-id'];level=q[':question/difficulty'][':db/ident'].split('/')[-1]
  default=m.SOURCE_DEFAULTS.get(name,1)
  try:
   r=m.generate(level,seed=730033,template=name,parameters={'a':default},profile='observed');replay.append(r)
   normal.append(m.generate(level,seed=730033,template=name,parameters={'a':default}))
   normal.append(m.generate(level,seed=730039,template=name,parameters={'a':4 if name=='q-128191' else 8}))
   replay_results.append({'source_id':q[':question/id'],'template':name,'prompt_exact':r['question'][':question/problem']==q[':question/problem'],'solution_exact':r['question'][':question/worked-solution']==q[':question/worked-solution'],'status':'generated'})
  except Exception as e:replay_results.append({'source_id':q[':question/id'],'template':name,'status':'failed','error':repr(e)})
 save('source-replay.json',replay);save('normal-cases.json',normal);save('source-replay-results.json',replay_results)
 save('sampling-errors.json',errors)
 rejects=[]
 for args in [dict(level='easy',parameters={'a':0}),dict(level='easy',parameters={'a':13}),dict(level='easy',parameters={'a':True}),dict(level='easy',parameters={'a':1,'b':2}),dict(level='moderate',template='q-128191',parameters={'a':5}),dict(level='moderate',template='q-8303',parameters={'a':-1}),dict(level='easy',template='q-8305')]:
  try:m.generate(seed=730041,**args);out='unexpected acceptance'
  except Exception as e:out=repr(e)
  rejects.append({'args':args,'outcome':out})
 deterministic=[m.generate_easy(730057),m.generate_easy(730057)]
 save('runtime.json',{'python':sys.version.split()[0],'sympy':m.sp.__version__,'replay_equal':deterministic[0]==deterministic[1],'invalid_inputs':rejects,'sample_command':f'{sys.executable} {ROOT}/review.py sample','history_present':(JOB/'repair-history.json').exists(),'preflight_present':(JOB/'repair-preflight.json').exists()})
 # Pairs: relevant a sign in linear; irrelevant seed option permutation. Leak template coefficient varies too.
 pairs=[]
 for name,level,a,b in [('q-128198','moderate',1,8),('q-128191','moderate',1,4),('easy_linear','easy',2,-2),('q-79665','moderate',1,2),('q-8303','moderate',1,2),('q-8304','moderate',1,2)]:
  pairs.append({'kind':'relevant','template':name,'before':m.generate(level,730061,name,parameters={'a':a}),'after':m.generate(level,730061,name,parameters={'a':b})})
 pairs.append({'kind':'irrelevant','template':'easy_linear','before':m.generate_easy(730061,'easy_linear',parameters={'a':2}),'after':m.generate_easy(730067,'easy_linear',parameters={'a':2})})
 save('pairs.json',pairs)
 # Four default samples for leak family, avoid wide audit beyond the demonstrated gap.
 leak=[m.generate_moderate(730071+i,name,parameters={'a':a}) for name in ['q-8303','q-79665','q-8304'] for i,a in enumerate([1,2,7,8])]
 save('leak-cases.json',leak)
 save('moderate-delivery-input.json',[r for r in normal+leak if r['question'][':question/difficulty'].endswith('/moderate')])
 save('hard-delivery-input.json',[r for r in normal if r['question'][':question/difficulty'].endswith('/hard')])
 render=batch[:1]+[r for p in pairs for r in [p['before'],p['after']]]+[r for r in normal if r['generation']['template']=='q-128191']
 save('render-input.json',render)
 print({'easy':len(records),'normal':len(normal),'source_replayed':len(replay),'source_failures':[x for x in replay_results if x['status']=='failed'],'sampling_errors':len(errors)})

if __name__=='__main__':
 if sys.argv[1]=='sample':sample()
