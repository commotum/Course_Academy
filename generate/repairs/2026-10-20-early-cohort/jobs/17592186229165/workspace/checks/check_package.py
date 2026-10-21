"""Check declared runtime closure, relocation, seeded CLI and preservation of easy output."""
import sys,json,pathlib,subprocess,shutil,hashlib,importlib.util
sys.dont_write_bytecode=True
ROOT=pathlib.Path(__file__).resolve().parents[1]
manifest=json.loads((ROOT/'package.json').read_text());out=ROOT/'evidence/relocated';out.mkdir(exist_ok=True)
assert manifest['files']==['17592186229165.py','requirements.txt']
import sympy
assert manifest['dependencies']=={'python':sys.version.split()[0],'packages':{'sympy':sympy.__version__}}
assert (ROOT/'requirements.txt').read_text()=='sympy=='+sympy.__version__+'\n'
for name in manifest['files']:shutil.copyfile(ROOT/name,out/name)
cmd=[sys.executable,str(out/manifest['entrypoint']),'--difficulty','easy','--count','5','--seed','901','--format','json']
a=subprocess.run(cmd,cwd='/tmp',capture_output=True,text=True,check=True).stdout
b=subprocess.run(cmd,cwd='/tmp',capture_output=True,text=True,check=True).stdout
assert a==b
records=json.loads(a);assert records==json.loads((ROOT/'evidence/easy-batch.json').read_text())
spec=importlib.util.spec_from_file_location('old',ROOT/'evidence/generator-before.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
assert records==[g.generate('easy',seed=i) for i in range(901,906)],'Repair changed unaffected easy output'
hcmd=[sys.executable,str(out/manifest['entrypoint']),'--difficulty','hard','--count','5','--seed','67031','--format','json']
h=json.loads(subprocess.run(hcmd,cwd='/tmp',capture_output=True,text=True,check=True).stdout);assert len(h)==5
bad=subprocess.run(cmd[:-5]+['--count','0','--format','json'],cwd='/tmp',capture_output=True,text=True);assert bad.returncode!=0
report={'status':'passed','runtime_files':manifest['files'],'runtime_hashes':{n:hashlib.sha256((out/n).read_bytes()).hexdigest() for n in manifest['files']},'relocation_cwd':'/tmp','commands':[cmd,hcmd],'seeded_cli_repeat_exact':True,'requested_easy_five':len(records),'easy_records_unchanged':True,'hard_cli_five':len(h),'invalid_count_rejected':True,'dependencies':manifest['dependencies']}
(ROOT/'evidence/package-results.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
