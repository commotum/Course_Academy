import concurrent.futures,json,os,shutil,subprocess,tempfile
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4];cfg=json.loads((H/'generator-stage-config.json').read_text());bands={c['kp']:[b['band']for r in json.loads((H/'generator-relocation-proof.json').read_text())if r['kp']==c['kp']for b in r['bands']]for c in cfg};outside=Path(tempfile.mkdtemp(prefix='ca-topic3-g1-readonly-'));env=dict(os.environ);env.pop('PYTHONPATH',None);env.pop('_CA_SOURCE_POLICY_CHILD',None);env['PYTHONDONTWRITEBYTECODE']='1'
child=r'''
import importlib.util,json,sys
from pathlib import Path
p=Path(sys.argv[1]);sys.path.insert(0,str(p.parent));s=importlib.util.spec_from_file_location('domain_probe',p);m=importlib.util.module_from_spec(s);sys.modules[s.name]=m;s.loader.exec_module(m);out=[]
for profile,C,want in [('source:q-161636',4,False),('source:q-161636',7,True),('authored:method',4,True)]:
 try:
  record=m.generate('hard',seed=28109837,template='lower_zinverse',parameters={'a':3,'H':6,'C':C},profile=profile);accepted=True;detail=record['generation']
 except ValueError as ex:accepted=False;detail=str(ex)
 assert accepted==want,(profile,C,accepted,detail)
 out.append({'profile':profile,'a':3,'C':C,'expected_emission':want,'emitted':accepted,'detail':detail})
print(json.dumps(out))
'''
(outside/'domain_probe.py').write_text(child)
def run(c):
 root=outside/'package'/str(c['kp']);root.mkdir(parents=True)
 for f in c['files']:p=root/f;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(Path(c['directory'])/f,p);p.chmod(0o444)
 for d in sorted([p for p in root.rglob('*')if p.is_dir()],key=lambda p:len(p.parts),reverse=True):d.chmod(0o555)
 root.chmod(0o555);out=[]
 for band in bands[c['kp']]:
  output=outside/'output'/str(c['kp'])/band;output.mkdir(parents=True)
  args=[str(R/'.venv/bin/python'),str(root/c['entrypoint']),'--difficulty',band,'--count','1','--seed','28109837','--format','json'];r=subprocess.run(args,cwd=outside,env={**env,'COURSE_ACADEMY_GENERATOR_OUTPUT_DIR':str(output)},text=True,capture_output=True,timeout=120);out.append({'band':band,'returncode':r.returncode,'stderr':r.stderr,'records':len(json.loads(r.stdout))if r.returncode==0 and isinstance(json.loads(r.stdout),list)else 1 if r.returncode==0 else 0})
 domains=None
 if c['kp']==17592186129268:
  r=subprocess.run([str(R/'.venv/bin/python'),str(outside/'domain_probe.py'),str(root/c['entrypoint'])],cwd=outside,env={**env,'COURSE_ACADEMY_GENERATOR_OUTPUT_DIR':str(outside/'domain-output')},text=True,capture_output=True,timeout=120);domains={'returncode':r.returncode,'cases':json.loads(r.stdout)if r.returncode==0 else None,'stderr':r.stderr}
 return {'kp':c['kp'],'package':str(root),'files_mode':'0444','directory_mode':'0555','bands':out,'source_kernel_domain_cases':domains,'passed':all(r['returncode']==0 for r in out)and(domains is None or domains['returncode']==0)}
rs=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=3)as pool:
 for r in pool.map(run,cfg):rs.append(r);(H/'generator-readonly-proof.json').write_text(json.dumps(rs,indent=2)+'\n');print(r['kp'],r['passed'],[(b['band'],b['returncode'],b['stderr'][-100:])for b in r['bands']],r['source_kernel_domain_cases'],flush=True)
