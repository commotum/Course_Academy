import hashlib,json,os,pathlib,shutil,subprocess,sys
E=pathlib.Path(__file__).resolve().parent; P=E.parent/'workspace'; REPO=pathlib.Path('/home/jake/Developer/Course_Academy')
def save(n,x):(E/n).write_text(json.dumps(x,indent=2)+'\n')
env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','PYTHONPATH':'','COURSE_ACADEMY_GENERATOR_OUTPUT_DIR':str(E/'external-assets'),'TMPDIR':str(E/'tmp')};(E/'tmp').mkdir(exist_ok=True)
manifest=json.load(open(P/'package.json')); target=E/'relocated'; target.mkdir(exist_ok=True)
for rel in manifest['files']:
 p=pathlib.Path(rel);assert not p.is_absolute() and '..' not in p.parts
 (target/p).parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(P/p,target/p)
bootstrap="import runpy,sys;sys.dont_write_bytecode=True;sys.path.insert(0,sys.argv.pop(1));runpy.run_path(sys.argv.pop(1),run_name='__main__')"
cmd=[sys.executable,'-I','-c',bootstrap,str(target),str(target/manifest['entrypoint']),'--count','5','--seed','98477','--difficulty','moderate']
r=subprocess.run(cmd,cwd=E,env=env,text=True,capture_output=True);assert r.returncode==0,r.stderr
rows=json.loads(r.stdout);save('relocated-records.json',rows)
# Replay the old repository-dependent import failure in an isolated historical closure.
legacy=E/'legacy-failing';(legacy/'17592186124511').mkdir(parents=True,exist_ok=True)
shutil.copyfile(REPO/'generate/scratch/17592186124511.py',legacy/'17592186124511.py')
shutil.copyfile(REPO/'generate/scratch/17592186124511/source.json',legacy/'17592186124511/source.json')
isolated_bootstrap="from pathlib import Path;original_is_file=Path.is_file;Path.is_file=lambda p: False if str(p).endswith('scripts/generator_policy.py') else original_is_file(p);"+bootstrap
oldcmd=[sys.executable,'-I','-c',isolated_bootstrap,str(legacy),str(legacy/'17592186124511.py'),'--count','1']
f=subprocess.run(oldcmd,cwd=E,env=env,text=True,capture_output=True);assert f.returncode!=0
save('historical-failure.json',{'command':oldcmd,'returncode':f.returncode,'stderr':f.stderr,'reason':'legacy code searches ancestors for scripts/generator_policy.py; relocated closure has none','code_sha256':hashlib.sha256((legacy/'17592186124511.py').read_bytes()).hexdigest()})
# Execute retained author event check verbatim except its ROOT, output and temp locations.
text=(P/'checks/check_runtime.py').read_text();original_hash=hashlib.sha256(text.encode()).hexdigest()
text=text.replace("ROOT=Path(__file__).resolve().parents[1]","ROOT=Path("+repr(str(P))+")")
text=text.replace("tempfile.TemporaryDirectory(prefix='imt-relocation-')","tempfile.TemporaryDirectory(prefix='imt-relocation-', dir="+repr(str(E/'tmp'))+")")
text=text.replace("ROOT/'evidence/relocation.json'","Path("+repr(str(E/'retained-runtime-results.json'))+")")
script=E/'retained-check-runtime.py';script.write_text(text)
c=subprocess.run([sys.executable,str(script)],cwd=E,env=env,text=True,capture_output=True);assert c.returncode==0,c.stderr
# Ensure that the executable guard really fails on the historical closure.
mut=text.replace(repr(str(P)),repr(str(legacy))).replace("import runpy,sys;sys.path.insert", "from pathlib import Path;original_is_file=Path.is_file;Path.is_file=lambda p: False if str(p).endswith('scripts/generator_policy.py') else original_is_file(p);import runpy,sys;sys.path.insert")
(legacy/'package.json').write_text(json.dumps({'files':['17592186124511.py','17592186124511/source.json'],'entrypoint':'17592186124511.py'}))
(E/'retained-check-historical.py').write_text(mut)
m=subprocess.run([sys.executable,str(E/'retained-check-historical.py')],cwd=E,env=env,text=True,capture_output=True);assert m.returncode!=0
save('runtime-results.json',{'manifest':manifest,'installed_versions':{'python':sys.version.split()[0],'sympy':__import__('sympy').__version__,'mpmath':__import__('mpmath').__version__},'declared_exact_versions_match':manifest['dependencies']=={'python':sys.version.split()[0],'packages':{'sympy':__import__('sympy').__version__,'mpmath':__import__('mpmath').__version__}},'relocated_command':cmd,'relocated_returncode':r.returncode,'count':len(rows),'external_output_directory':str(E/'external-assets'),'assets_needed':False,'retained_event_check':{'source_sha256':original_hash,'current_returncode':c.returncode,'current_stdout':c.stdout,'historical_returncode':m.returncode,'historical_stderr':m.stderr},'repair_history_findings':[],'repair_preflight_exists':(E.parent/'repair-preflight.json').exists()})
print('Relocation and exact versions passed; retained event check passes current and fails historical closure.')
