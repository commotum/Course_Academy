import pathlib,json,shutil,subprocess,sys,hashlib,ast,importlib.metadata
E=pathlib.Path(__file__).resolve().parent;W=pathlib.Path('/home/jake/Developer/Course_Academy/generate/repairs/2026-10-20-early-cohort/jobs/17592186147456/workspace');A=E/'author-regression';A.mkdir(exist_ok=True)
m=json.loads((W/'package.json').read_text())
for n in m['files']+['package.json','checks/package_check.py','checks/reproduce_legacy_failure.py','evidence/legacy-relocated/17592186147456.py','evidence/legacy-relocated/17592186147456/reference/initial/source.json','evidence/legacy-relocated/17592186147456/reference/initial/inventory.json']:
 p=A/n;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(W/n,p)
# The original file searches ancestors for scripts/generator_policy.py before importing scripts.
# A local marker makes the retained check reach that exact import under E, without repo dependency.
p=A/'scripts/generator_policy.py';p.parent.mkdir(exist_ok=True);p.write_text('# Marker to reach the legacy undeclared import in the retained negative control.\n')
results=[]
for n in ['checks/reproduce_legacy_failure.py','checks/package_check.py']:
 cmd=[sys.executable,'-B',str(A/n)];r=subprocess.run(cmd,cwd=E,capture_output=True,text=True)
 results.append({'command':cmd,'returncode':r.returncode,'stdout':r.stdout,'stderr':r.stderr})
# Fresh relocation/seed, output mode and deterministic count checks.
dest=E/'relocated';dest.mkdir(exist_ok=True)
for n in m['files']:shutil.copyfile(W/n,dest/n)
cmd=[sys.executable,'-B',str(dest/m['entrypoint']),'--difficulty','easy','--seed','981726','--count','5','--format','json']
a=subprocess.run(cmd,cwd=E,capture_output=True,text=True);b=subprocess.run(cmd,cwd=E,capture_output=True,text=True)
(E/'relocation-records.json').write_text(a.stdout)
output=E/'cli-output.json';c=subprocess.run(cmd+['--output',str(output)],cwd=E,capture_output=True,text=True)
(E/'packaging.json').write_text(json.dumps({'retained_checks':results,'fresh_command':cmd,'returncodes':[a.returncode,b.returncode,c.returncode],'deterministic':a.stdout==b.stdout,'output_mode_matches':json.loads(a.stdout)==json.loads(output.read_text()),'runtime':{'python':sys.version.split()[0],'packages':{'sympy':importlib.metadata.version('sympy')}},'manifest_dependencies':m['dependencies'],'repair_history':'No retained findings; one event legacy_packaging_or_sampling. preflight absent.','package_check_limitation':'Retained failure reproduction needs local ancestor marker to reach its stated import; otherwise a fully detached legacy closure fails earlier on StopIteration.'},indent=2)+'\n')
print([(r['command'][-1],r['returncode']) for r in results],a.returncode,a.stdout==b.stdout)
