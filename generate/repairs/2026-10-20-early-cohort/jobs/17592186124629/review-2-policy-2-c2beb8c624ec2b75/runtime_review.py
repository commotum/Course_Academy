import ast,hashlib,json,os,shutil,subprocess,sys
from pathlib import Path
E=Path(__file__).resolve().parent;W=E.parent/'workspace';P='/home/jake/Developer/Course_Academy/.venv/bin/python'
manifest=json.load(open(W/'package.json'));dest=E/'relocated-package';dest.mkdir(exist_ok=True)
for name in manifest['files']:
 target=dest/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(W/name,target)
launcher='import runpy,sys;sys.path.insert(0,sys.argv.pop(1));sys.argv=sys.argv[1:];runpy.run_path(sys.argv[0],run_name="__main__")'
def run(args):
 cmd=[P,'-B','-I','-c',launcher,str(dest),str(dest/manifest['entrypoint'])]+args
 p=subprocess.run(cmd,cwd=E,capture_output=True,text=True)
 return {'command':cmd,'exit_code':p.returncode,'stderr':p.stderr,'stdout':p.stdout}
base=['--difficulty','moderate','--count','5','--seed','763019','--format','json']
a=run(base);b=run(base);assert a['exit_code']==b['exit_code']==0
rows=json.loads(a.pop('stdout'));rows2=json.loads(b.pop('stdout'));assert rows==rows2
(E/'relocation-records.json').write_text(json.dumps(rows,indent=2))
invalid=[run(['--difficulty','hard']),run(['--count','-1'])]
for x in invalid:assert x['exit_code']!=0;x.pop('stdout')
zero=run(['--count','0']);assert json.loads(zero.pop('stdout'))==[]
imports=set()
for name in manifest['files']:
 if name.endswith('.py'):
  for node in ast.walk(ast.parse((dest/name).read_text())):
   if isinstance(node,ast.Import):imports.update(n.name.split('.')[0] for n in node.names)
   if isinstance(node,ast.ImportFrom) and node.module:imports.add(node.module.split('.')[0])
local={Path(n).stem for n in manifest['files'] if n.endswith('.py')};unresolved=sorted(imports-local-sys.stdlib_module_names);assert not unresolved
version=subprocess.run([P,'-B','-c','import platform;print(platform.python_version())'],capture_output=True,text=True).stdout.strip()
assert version==manifest['dependencies']['python'];assert manifest['dependencies']['packages']=={}
# Exercise the retained legacy failing example in a separate closure.
old=E/'legacy-package';old.mkdir(exist_ok=True)
shutil.copyfile(W/'evidence/pre-repair-generator.py',old/'17592186124629.py')
# Its sibling source directory is read-only evidence copied locally.
(old/'17592186124629').mkdir(exist_ok=True)
shutil.copyfile(W/'17592186124629/source.json',old/'17592186124629/source.json')
legacy_launcher='import pathlib,runpy,sys; target=pathlib.Path(sys.argv[1]); original=pathlib.Path.resolve; pathlib.Path.resolve=lambda self,*a,**kw: pathlib.Path("/review-isolation/17592186124629.py") if self==target else original(self,*a,**kw); sys.argv=sys.argv[1:]; runpy.run_path(str(target),run_name="__main__")'
cmd=[P,'-B','-I','-c',legacy_launcher,str(old/'17592186124629.py'),'--difficulty','moderate','--count','5','--seed','24629','--format','json']
f=subprocess.run(cmd,cwd=E,capture_output=True,text=True)
assert f.returncode!=0
report={'relocation':a,'deterministic_replay':rows==rows2,'invalid_requests':invalid,'zero_count':zero,'declared_python':version,'undeclared_imports':unresolved,'external_output_files':[], 'retained_failure_isolation':'Only legacy script resolve() ancestry is mapped outside repo, since evidence_root itself lies inside repository. Source reads remain inside evidence_root; reproduces absent scripts ancestor.', 'retained_failure':{'command':cmd,'exit_code':f.returncode,'stderr':f.stderr},'note':'Author check_relocation.py was read but not run because it writes inside package. Equivalent independent test exercises manifest-only relocated closure with isolated import path.'}
(E/'runtime-results.json').write_text(json.dumps(report,indent=2))
print(json.dumps({'relocated':len(rows),'deterministic':True,'python':version,'legacy_stderr':f.stderr[-1000:]}))
