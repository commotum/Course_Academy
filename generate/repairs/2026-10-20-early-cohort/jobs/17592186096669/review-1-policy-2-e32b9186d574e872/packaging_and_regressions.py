from review_lib import *
import os
rel=ROOT/'relocated';rel.mkdir(exist_ok=True);manifest=load(PACKAGE/'package.json')
for f in manifest['files']:
 dst=rel/f;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(PACKAGE/f,dst)
cmd=[sys.executable,str(rel/manifest['entrypoint']),'--seed','82067','--count','12'];env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'}
def run(cmd):return subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True,env=env)
a=run(cmd);b=run(cmd);orig=run([sys.executable,str(PACKAGE/manifest['entrypoint']),*cmd[2:]])
assert a.returncode==b.returncode==orig.returncode==0 and a.stdout==b.stdout==orig.stdout
save('cli-samples.json',json.loads(a.stdout))
bounds=[]
for args in [['--scale','0'],['--scale','10'],['--difficulty','hard'],['--count','0'],['--profile','q-20450','--replay','--count','2'],['--profile','q-20450','--template','angle']]:
 r=run([sys.executable,str(rel/manifest['entrypoint']),*args]);assert r.returncode!=0;bounds.append({'args':args,'exit_code':r.returncode,'stderr':r.stderr[-450:]})
# Actual CLI retry deduplication, compared to its unfiltered stream.
spec=importlib.util.spec_from_file_location('rg',rel/manifest['entrypoint']);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
raw=[g.generate(seed=s,profile='q-20450') for s in range(82067,82097)]
ret=run([sys.executable,str(rel/manifest['entrypoint']),'--profile','q-20450','--seed','82067','--count','30']);assert ret.returncode==0
save('rejection-records.json',{'raw':raw,'cli':json.loads(ret.stdout),'command':ret.args})
# Author regression copied and redirected to reviewer evidence. No package evidence writes.
ad=ROOT/'author-regression';ad.mkdir(exist_ok=True);(ad/'output').mkdir(exist_ok=True)
script=(PACKAGE/'checks/regressions.py').read_text().replace("ROOT=Path(__file__).resolve().parents[1]",f"ROOT=Path({str(PACKAGE)!r})").replace("OUT=ROOT/'evidence'",f"OUT=Path({str(ad/'output')!r})")
(ad/'regressions.py').write_text(script);shutil.copy2(PACKAGE/'checks/math_witness.py',ad/'math_witness.py')
old=load(ROOT/'prior-counterexamples.json')['old_record'];(ad/'output/before-shortcut.json').write_text(json.dumps([old]))
r=run([sys.executable,str(ad/'regressions.py')]);(ad/'execution.log').write_text(r.stdout+'\n'+r.stderr);assert r.returncode==0
save('regression-verification.json',{'retained_findings':['2e7dea1482373ff8e888','13e0c7585323475ad032'],'preflight_claim':load(JOB/'repair-preflight.json'),'author_check_rerun':{'command':r.args,'exit_code':r.returncode,'output':r.stdout},'prior_failures':'Independently reproduced both on previous review relocated package in prior-counterexamples.json. Author regression additionally asserts saved old shortcut is present. Current bank-role and replay checks rerun independently.'})
assert manifest['dependencies']=={'python':platform.python_version(),'packages':{'sympy':sp.__version__}}
save('packaging-results.json',{'dependencies':manifest['dependencies'],'exact_versions_verified':True,'deterministic':True,'relocation_identical':True,'command':cmd,'boundaries':bounds,'rejection_stream_counts':{'raw':len(raw),'unique_raw':len({r['generation']['mathematical_fingerprint'] for r in raw}),'cli':len(json.loads(ret.stdout))},'external_outputs':'JSON stdout only; no assets. Manifest contains entrypoint, source JSON, exact requirements.','package_unchanged':hashpkg()==load(ROOT/'package-before.json')})
print('Packaging and redirected author regressions passed')
