import ast,concurrent.futures,json,os,subprocess,tempfile
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4];inv=json.loads((H/'generator-inventory.json').read_text());cwd=Path(tempfile.mkdtemp(prefix='ca-topic3-contracts-'))
probe=r'''
import importlib.util,inspect,json,os,sys
from pathlib import Path
p=Path(sys.argv[1]);sys.path.insert(0,str(p.parent));s=importlib.util.spec_from_file_location('audit_contract_'+p.stem,p);m=importlib.util.module_from_spec(s);sys.modules[s.name]=m;s.loader.exec_module(m)
out={'public':{},'selectors':{}}
for name in ['generate','generate_easy','generate_moderate','generate_hard','batch','generate_batch']:
 f=getattr(m,name,None)
 if callable(f):out['public'][name]=str(inspect.signature(f))
for name in ['TEMPLATES','FAMILIES','CASES','DATA','MODELS','BASE','PROFILES','SPECS']:
 v=getattr(m,name,None)
 if isinstance(v,dict):out['selectors'][name]={str(k):repr(x)[:1200]for k,x in v.items()}
 elif isinstance(v,(tuple,list))and len(v)<100:out['selectors'][name]=[repr(x)[:1200]for x in v]
print(json.dumps(out))
'''
(cwd/'probe.py').write_text(probe);env=dict(os.environ);env.pop('PYTHONPATH',None);env.pop('_CA_SOURCE_POLICY_CHILD',None);env['PYTHONDONTWRITEBYTECODE']='1'
def run(s):
 r=subprocess.run([str(R/'.venv/bin/python'),str(cwd/'probe.py'),s['path']],cwd=cwd,env=env,text=True,capture_output=True,timeout=60)
 return {'kp':s['kp'],'reference':s['reference'],'returncode':r.returncode,'stderr':r.stderr,'contract':json.loads(r.stdout)if r.returncode==0 else None}
rs=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=4)as pool:
 for r in pool.map(run,inv):rs.append(r);(H/'generator-contracts.json').write_text(json.dumps(rs,indent=2));print(r['kp'],r['returncode'],flush=True)
