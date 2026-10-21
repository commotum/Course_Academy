import audit as a
E=a.E;manifest=a.json.loads((a.PKG/'package.json').read_text());target=E/'relocated';target.mkdir(exist_ok=True)
for name in ['package.json']+manifest['files']:
 src=a.PKG/name;dst=target/name;dst.parent.mkdir(parents=True,exist_ok=True);a.shutil.copyfile(src,dst)
cmd=[str(a.PY),str(target/manifest['entrypoint']),'--difficulty','easy','--count','5','--seed','18031'];env=dict(a.os.environ,PYTHONDONTWRITEBYTECODE='1');out=a.subprocess.run(cmd,cwd=E,env=env,capture_output=True,text=True,timeout=90);(E/'relocated-stdout.json').write_text(out.stdout);(E/'relocated-stderr.txt').write_text(out.stderr or '(empty)\n')
original=a.subprocess.run([str(a.PY),str(a.PKG/manifest['entrypoint']),*cmd[2:]],cwd=E,env=env,capture_output=True,text=True,timeout=90);a.save('relocation-results.json',{'command':cmd,'cwd':str(E),'exit_code':out.returncode,'record_count':len(a.json.loads(out.stdout)) if out.returncode==0 else None,'matches_original':out.stdout==original.stdout,'external_output':'No images or other runtime files produced; generator communicates questions via stdout.','declared_dependencies':manifest['dependencies'],'actual_python':a.platform.python_version(),'actual_sympy':a.S.__version__})
a.save('package-after.json',a.hashfiles());a.save('package-integrity.json',{'equal':a.json.loads((E/'package-before.json').read_text())==a.hashfiles(),'file_count':len(a.hashfiles()),'basis':'all files under package_root, sha256 before and after'})
print('relocation exit',out.returncode,'matches',out.stdout==original.stdout)
