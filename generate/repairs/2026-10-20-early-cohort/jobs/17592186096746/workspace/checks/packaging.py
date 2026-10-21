import json,os,platform,random,shutil,subprocess,sys,tempfile
from pathlib import Path
W=Path(__file__).resolve().parents[1];sys.path.insert(0,str(W));import generator as g
manifest=json.loads((W/'package.json').read_text());assert platform.python_version()==manifest['dependencies']['python'];assert manifest['dependencies']['packages']=={}
with tempfile.TemporaryDirectory(prefix='kp17592186096746-') as t:
    root=Path(t);pkg=root/'pkg';pkg.mkdir();out=root/'assets';out.mkdir()
    for file in manifest['files']:
        dest=pkg/file;dest.parent.mkdir(exist_ok=True,parents=True);shutil.copyfile(W/file,dest)
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',COURSE_ACADEMY_GENERATOR_OUTPUT_DIR=str(out));env.pop('PYTHONPATH',None)
    args=['--difficulty','easy','--count','5','--seed','4221100018','--format','json']
    x=subprocess.run([sys.executable,str(pkg/manifest['entrypoint']),*args],cwd='/tmp',env=env,capture_output=True,text=True,check=True)
    assert json.loads(x.stdout)==g.generate('easy',5,4221100018)
    for args in (['--count','-1'],['--difficulty','hard']):
        y=subprocess.run([sys.executable,str(pkg/manifest['entrypoint']),*args],cwd='/tmp',env=env,capture_output=True,text=True);assert y.returncode!=0
    assert sorted(str(p.relative_to(pkg)) for p in pkg.rglob('*') if p.is_file())==sorted(manifest['files'])
    assert not list(out.iterdir()),'No diagram assets expected'
# Exercise duplicate rejection in memory; no runtime files are changed.
original=g.sample_parameters;one=original(random.Random(7729),'easy');two=original(random.Random(3219),'easy');draws=iter([one,one,two]);g.sample_parameters=lambda rng,band:next(draws)
try:
    rs=g.generate('easy',2,39);assert rs[1]['generation']['draw']==3 and rs[1]['generation']['rejections']==1
finally:g.sample_parameters=original
g.sample_parameters=lambda rng,band:one
try:
    try:g.generate('easy',2,39)
    except RuntimeError:pass
    else:raise AssertionError('duplicate loop unbounded')
finally:g.sample_parameters=original
assert g.generate('easy',0,1)==[]
report={'passed':True,'python':platform.python_version(),'relocation_cli_determinism':True,'runtime_files_only':True,'negative_count_hard_rejected':True,'duplicate_resample_and_bounded_failure':True,'output_assets':0}
(W/'evidence/packaging.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
