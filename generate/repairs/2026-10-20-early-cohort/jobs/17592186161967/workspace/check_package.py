"""Relocation, CLI replay, sampling-mode and package-dependency checks."""
import hashlib,json,os,shutil,subprocess,sys
from pathlib import Path
from check_repair import g,HERE,OUT,save,inspect
manifest=json.loads((HERE/'package.json').read_text())
rel=OUT/'relocated';rel.mkdir(exist_ok=True)
for name in manifest['files']:
 src=HERE/name;dst=rel/name;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst)
args=['--difficulty','easy','--count','5','--seed','20261022','--format','json']
env=dict(os.environ,COURSE_ACADEMY_GENERATOR_OUTPUT_DIR=str(OUT/'generated-assets'),PYTHONDONTWRITEBYTECODE='1')
run=subprocess.run([sys.executable,'-B',str(rel/manifest['entrypoint']),*args],cwd=rel,env=env,text=True,capture_output=True,check=True)
rows=json.loads(run.stdout);expected=json.loads((OUT/'candidate-batch.json').read_text());assert rows==expected
assert all(r['generation']['bank_mode']=='independent-signs' for r in rows)
for r in rows:inspect(r)
save('relocated-batch.json',rows)
for difficulty in ('moderate','hard'):
 r=subprocess.run([sys.executable,'-B',str(rel/manifest['entrypoint']),'--difficulty',difficulty,'--count','1','--seed','0','--format','json'],cwd=rel,text=True,capture_output=True)
 assert r.returncode!=0 and 'Unsupported difficulty' in r.stderr
# Even a sampled exact original matrix must use the generalized bank, while
# explicit original-parameter replay remains intact. Force only the sampler RNG.
p=g.ORIGINAL['q-42531'];A=p['A'];targets=[i for i in range(3) if i!=p['pivot']]
class SampleOriginal:
 def __init__(self):self.coords=iter((p['pivot'],p['column']));self.entries=iter(x for row in A for x in row);self.values=iter([p['ks'][i] for i in targets]+[A[p['pivot']][p['column']]])
 def randrange(self,n):return next(self.coords)
 def randint(self,a,b):return next(self.entries)
 def choice(self,values):return next(self.values)
original_random=g.random.Random
g.random.Random=lambda seed:original_random(seed) if isinstance(seed,str) else SampleOriginal()
try:r=g.generate(seed=12,bank_profile='q-42531')
finally:g.random.Random=original_random
assert r['generation']['parameters']==p and r['generation']['bank_mode']=='independent-signs';inspect(r)
save('sampled-original-record.json',r)
save('packaging-report.json',{'status':'pass','relocated_cli_records':5,'relocated_exact_match':True,'unsupported_bands_rejected':['moderate','hard'],'sampled_original_uses_generalized_bank':True,'explicit_source_replays':'evidence/source-replay-report.json','runtime_files':manifest['files'],'dependencies':manifest['dependencies'],'hashes':{name:hashlib.sha256((HERE/name).read_bytes()).hexdigest() for name in manifest['files']}})
print('Relocated CLI: exact 5-record replay; unsupported bands rejected; sampled-original path uses repaired bank.')
