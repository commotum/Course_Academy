#!/usr/bin/env python3
import json,pathlib,shutil,subprocess,sys,os,hashlib
P=pathlib.Path(__file__).resolve().parent;E=P/'evidence';m=json.loads((P/'package.json').read_text());target=E/'relocated-package';target.mkdir(exist_ok=True)
for f in m['files']:
 p=pathlib.Path(f);assert not p.is_absolute() and '..' not in p.parts
 assert p.name!='package.json'
 (target/p).parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(P/p,target/p)
args=[sys.executable,'-B',str(target/m['entrypoint']),'--difficulty','moderate','--count','5','--seed','4077425948','--format','json']
env={**os.environ,'PYTHONPATH':'','PYTHONDONTWRITEBYTECODE':'1','COURSE_ACADEMY_GENERATOR_OUTPUT_DIR':str(E/'assets')}
a=subprocess.check_output(args,cwd='/tmp',env=env);b=subprocess.check_output(args,cwd='/tmp',env=env);assert a==b
original=subprocess.check_output([sys.executable,'-B',str(P/m['entrypoint']),*args[3:]],cwd='/tmp',env=env);assert a==original
records=json.loads(a);assert len(records)==5
import sympy
assert m['dependencies']=={'python':sys.version.split()[0],'packages':{'sympy':sympy.__version__}}
report={'relocation':'passed','deterministic_replay':'passed','count':len(records),'runtime_hashes':{f:hashlib.sha256((P/f).read_bytes()).hexdigest() for f in m['files']},'dependencies':m['dependencies']}
(E/'packaging-results.json').write_text(json.dumps(report,indent=2));(E/'relocated-records.json').write_bytes(a);print('Relocation, deterministic CLI, count and dependency checks passed')
