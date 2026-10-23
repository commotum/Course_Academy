import pathlib,sys,subprocess,json,hashlib,shutil,os
sys.dont_write_bytecode=True
root=pathlib.Path(__file__).resolve().parent; pkg=root.parent/'workspace';py='/home/jake/Developer/Course_Academy/.venv/bin/python'
m=json.load(open(pkg/'package.json'));before={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in pkg.iterdir() if p.is_file()}
copy=root/'relocated';copy.mkdir(exist_ok=True)
for name in ['package.json']+m['files']:shutil.copyfile(pkg/name,copy/name)
env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'}
cmd=[py,'-B',str(copy/'generator.py'),'--difficulty','easy','--count','5','--seed','928264887','--format','json']
r=subprocess.run(cmd,cwd=root,env=env,capture_output=True,text=True)
(root/'relocated-cli-records.json').write_text(r.stdout)
invalid=subprocess.run([py,'-B',str(copy/'generator.py'),'--count','26'],cwd=root,env=env,capture_output=True,text=True)
actual=json.loads(subprocess.check_output([py,'-B','-c','import sys,sympy,json;print(json.dumps({"python":sys.version.split()[0],"packages":{"sympy":sympy.__version__}}))'],text=True))
out={'command':cmd,'exit_code':r.returncode,'stderr':r.stderr,'relocated_equal_batch':json.loads(r.stdout)==json.load(open(root/'batch-records.json')),'dependencies_declared':m['dependencies'],'dependencies_actual':actual,'dependencies_exact_match':m['dependencies']==actual,'count26':{'returncode':invalid.returncode,'stderr':invalid.stderr},'package_files_before':before,'package_files_after':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in pkg.iterdir() if p.is_file()},'external_output':'CLI outputs JSON on stdout; generator does not write assets. Relocated from manifest files only and executed outside package.'}
(root/'packaging-results.json').write_text(json.dumps(out,indent=2))
print(json.dumps({k:v for k,v in out.items() if k not in ['package_files_before','package_files_after','stderr','command']},indent=2))
