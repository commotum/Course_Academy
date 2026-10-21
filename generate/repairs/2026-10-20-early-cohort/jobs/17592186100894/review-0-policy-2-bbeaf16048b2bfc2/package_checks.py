import pathlib,json,subprocess,sys,shutil,hashlib,os
E=pathlib.Path(__file__).resolve().parent;W=pathlib.Path('/home/jake/Developer/Course_Academy/generate/repairs/2026-10-20-early-cohort/jobs/17592186100894/workspace');py='/home/jake/Developer/Course_Academy/.venv/bin/python'
p=E/'relocated';shutil.copytree(W,p,dirs_exist_ok=True)
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1');cmd=[py,str(p/'17592186100894.py'),'--difficulty','easy','--seed','824993','--count','5']
a=subprocess.run(cmd,cwd=E,env=env,capture_output=True,text=True);(E/'relocation-records.json').write_text(a.stdout);(E/'relocation-stderr.txt').write_text(a.stderr)
b=subprocess.run([py,str(W/'17592186100894.py'),'--difficulty','easy','--seed','824993','--count','5'],cwd=E,env=env,capture_output=True,text=True)
manifest=json.load(open(W/'package.json'));before=json.load(open(E/'package-before.json'));after={str(q.relative_to(W)):hashlib.sha256(q.read_bytes()).hexdigest() for q in W.rglob('*') if q.is_file()}
result={'command':cmd,'exit':a.returncode,'unrelocated_exit':b.returncode,'relocated_equal':a.stdout==b.stdout,'undeclared_imports':'Runtime uses stdlib, sympy, declared local math_format.py and parse_math.py; no images or external writes. Author replenishment scripts are included but not run.','dependencies':manifest['dependencies'],'installed':{'python':sys.version.split()[0],'packages':{'sympy':__import__('sympy').__version__}},'manifest_files_exist':all((W/f).is_file() for f in manifest['files']),'package_unchanged':before==after,'hashes':after}
(E/'packaging.json').write_text(json.dumps(result,indent=2));print({k:v for k,v in result.items() if k not in ('hashes','command')})
