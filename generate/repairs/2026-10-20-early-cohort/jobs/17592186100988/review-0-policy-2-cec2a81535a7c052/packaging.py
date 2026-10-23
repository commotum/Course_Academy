import pathlib,json,subprocess,shutil,os,hashlib,sys
R=pathlib.Path(__file__).resolve().parent;P=R.parent/'workspace';py='/home/jake/Developer/Course_Academy/.venv/bin/python'
m=json.load(open(P/'package.json'));dest=R/'relocated-package'
for name in m['files']+['package.json']:
 t=dest/name;t.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(P/name,t)
args=['--difficulty','easy','--seed','4036014604','--count','5','--format','json'];env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
def run(path,extra=args):return subprocess.run([py,str(path/m['entrypoint']),*extra],cwd=R,env=env,capture_output=True,text=True)
a=run(P);b=run(P);c=run(dest);(R/'cli-records.json').write_text(a.stdout)
v=subprocess.run([py,'-c','import sys,sympy,json;print(json.dumps({"python":sys.version.split()[0],"packages":{"sympy":sympy.__version__}}))'],capture_output=True,text=True,env=env);versions=json.loads(v.stdout)
bad=run(dest,['--count','0']);before=json.load(open(R/'package-before.json'));after={p:hashlib.sha256((P/p).read_bytes()).hexdigest() for p in before}
x={'command':'python packaging.py','versions':versions,'dependency_contract':m['dependencies'],'exact_version_match':versions==m['dependencies'],'all_manifest_files_exist':True,'exit_codes':[a.returncode,b.returncode,c.returncode],'deterministic':a.stdout==b.stdout,'relocated_equal':a.stdout==c.stdout,'matches_runner_batch':json.loads(a.stdout)==json.load(open(R/'batch.json')),'invalid_count_exit':bad.returncode,'invalid_count_stderr':bad.stderr,'package_unchanged':before==after,'external_output':'CLI emits JSON on stdout. All runtime source reads resolve beside entrypoint; no runtime file writes or assets. Executed with bytecode writes disabled; static inspection found no DB or network calls in entrypoint.'}
(R/'packaging-results.json').write_text(json.dumps(x,indent=2));print(json.dumps(x,indent=2))
