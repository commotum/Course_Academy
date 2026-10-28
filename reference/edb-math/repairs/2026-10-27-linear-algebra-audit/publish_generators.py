import json,sys,shutil
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];sys.path.insert(0,str(R))
from scripts.generator_packages import publish_package,check_dependencies,verify_package
from scripts.generator_publish import Publisher,StaleBasis
D=Path(sys.argv[1]);candidates=json.loads((D/'generator-candidates.json').read_text());assert json.loads((D/'verification.json').read_text())['committed']
publisher=Publisher.from_environment(source=':agent/codex');out=[]
for c in candidates:
 check_dependencies(c['dependencies'],sys.executable)
 package=publish_package(Path(c['directory']),c.get('entrypoint','generator.py'),c['files'],publisher.config.math_root,dependencies=c['dependencies'],expected_digest=c['approved_digest']);verify_package(package.directory,package.digest)
 directory=D/('generator-publication-'+str(c['kp']));directory.mkdir(exist_ok=True)
 if not(directory/'preparation.json').exists():publisher.prepare(c['kp'],[],package.reference,package.digest,directory,expected_registered_generator=c['old_reference'])
 for attempt in range(4):
  try:
   result=publisher.publish(directory);break
  except StaleBasis:
   # Before a request exists, or after a confirmed stale-basis rejection has
   # retired it, a fresh guarded preparation is safe. Never replace a pending
   # request whose commit outcome still needs reconciliation.
   if (directory/'request.json').exists()or attempt==3:raise
   prior=json.loads((directory/'preparation.json').read_text());archive=directory/'stale-preparations'/str(prior['basis']);archive.mkdir(parents=True,exist_ok=True)
   for name in ['preparation.json','preview.edn','transaction.edn']:
    if(directory/name).exists():shutil.copyfile(directory/name,archive/name)
   publisher.prepare(c['kp'],[],package.reference,package.digest,directory,expected_registered_generator=c['old_reference'])
 out.append({'kp':c['kp'],'old_reference':c['old_reference'],'new_reference':package.reference,'digest':package.digest,'result':result});(D/'generator-publications.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print('Registered replacement for',c['kp'],package.reference,flush=True)
