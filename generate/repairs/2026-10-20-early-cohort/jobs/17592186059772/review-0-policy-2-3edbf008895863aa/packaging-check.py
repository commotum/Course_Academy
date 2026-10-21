import sys
sys.dont_write_bytecode=True
from audit import *
import shutil,platform

def main():
 manifest=json.load(open(PKG/'package.json'));rel=OUT/'relocated-package';rel.mkdir(exist_ok=True)
 for n in manifest['files']:shutil.copy2(PKG/n,rel/n)
 shutil.copy2(PKG/'package.json',rel/'package.json')
 env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1');commands=[]
 for d in ['easy','moderate','hard']:
  outputs=[]
  for root in [PKG,PKG,rel]:
   cmd=[str(ROOT/'.venv/bin/python'),str(root/'generator.py'),'--difficulty',d,'--seed','974341','--count','3']
   p=subprocess.run(cmd,env=env,cwd=OUT,capture_output=True,text=True)
   commands.append({'command':cmd,'cwd':str(OUT),'returncode':p.returncode,'stderr':p.stderr})
   outputs.append(json.loads(p.stdout));
  save('cli-'+d+'.json',outputs[0]);commands[-1]['deterministic_and_relocatable']=outputs[0]==outputs[1]==outputs[2]
 save('packaging-results.json',{'commands':commands,'runtime':platform.python_version(),'manifest':manifest,'declared_dependencies_match':manifest['dependencies']=={'python':platform.python_version(),'packages':{}},'package_unchanged':digest()==json.load(open(OUT/'package-hashes-before.json')),'external_assets':False,'package_files':sorted(p.name for p in PKG.iterdir()),'imports':'Only standard library and bundled local modules; checked generator.py, moderate_ops.py, hard_ops.py and math_format.py imports.'})
 print('relocation replay',all(x.get('deterministic_and_relocatable',True) for x in commands),'unchanged',digest()==json.load(open(OUT/'package-hashes-before.json')))
if __name__=='__main__':main()
