import os,sys,json,subprocess,shutil,hashlib,importlib.util
from pathlib import Path
sys.dont_write_bytecode=True
E=Path(__file__).resolve().parent;W=E.parent
manifest=json.loads((W/'package.json').read_text());dest=E/'relocated'
for name in manifest['files']:
 target=dest/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(W/name,target)
os.environ['COURSE_ACADEMY_GENERATOR_OUTPUT_DIR']=str(E/'cli-assets');os.environ['MPLCONFIGDIR']=str(E/'mpl-cache')
def hashes():return {n:hashlib.sha256((dest/n).read_bytes()).hexdigest() for n in manifest['files']}
before=hashes();cmd=[sys.executable,str(dest/manifest['entrypoint']),'--difficulty','easy','--count','5','--seed','20261022','--format','json']
r=subprocess.run(cmd,cwd=dest,capture_output=True,text=True);assert r.returncode==0,r.stderr
records=json.loads(r.stdout);assert len(records)==5
(E/'batch.json').write_text(r.stdout)
r2=subprocess.run(cmd,cwd=dest,capture_output=True,text=True);assert r2.returncode==0 and r2.stdout==r.stdout
assert hashes()==before
assert not (dest/'17592186129197/plots').exists()
spec=importlib.util.spec_from_file_location('relocated',dest/manifest['entrypoint']);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
guards=[]
for band,f,p in [('easy','simple',{'a':0,'h':1,'k':0}),('easy','simple',{'a':1,'h':2,'k':0}),('hard','hyper_y',{'a':1,'h':9,'k':3}),('hard','quartic',{'a':1,'h':4,'k':0})]:
 try:g.generate(band,17,template=f,parameters=p)
 except ValueError as exc:guards.append(str(exc))
 else:raise AssertionError('invalid parameters accepted')
# Final explicit-path metadata repair: each declared candidate really produces
# a displayed choice. Mathematical outputs were unchanged by this metadata fix.
r=g.generate('easy',8191,template='simple',parameters={'a':1,'h':1,'k':0})
vals=[g.parse(a[':answer/value']) for a in r['question'][':question/answer-fields'][0][':answer-field/choices']]
assert all(any(g.eq(g.model('simple',p)['A'],z) for z in vals) for p in r['generation']['bank_parameters'])
(E/'packaging-tests.json').write_text(json.dumps({'command':cmd,'records':len(records),'deterministic':True,'relocated':True,'runtime_files_unchanged':True,'external_output_dir':os.environ['COURSE_ACADEMY_GENERATOR_OUTPUT_DIR'],'guards':guards,'explicit_bank_provenance_valid':True,'manifest':manifest},indent=2))
print('Relocated CLI: five records, deterministic, no runtime writes; four boundary guards pass.')
