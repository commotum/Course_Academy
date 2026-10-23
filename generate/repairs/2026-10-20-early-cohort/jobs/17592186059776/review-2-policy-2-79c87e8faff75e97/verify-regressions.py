import sys,json,pathlib,shutil,subprocess,importlib.util
sys.dont_write_bytecode=True
R=pathlib.Path(__file__).resolve().parent; W=R.parent/'workspace'; P=R.parent/'review-1-policy-2-33f27ec8b7c41b11'
def load(path):
 s=importlib.util.spec_from_file_location('tested',path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
# Run the exact author predicates on copied code and source dependencies. All writes local.
reports=[]
for name,gen in [('before1',pathlib.Path('/home/jake/Developer/Course_Academy/generate/scratch/17592186059776.py')),('before2',W/'evidence/repair-2/before/generator.py'),('current',W/'17592186059776.py')]:
 if not gen.exists():
  reports.append({'name':name,'missing':str(gen)});continue
 dest=R/'regression-fixtures'/name;dest.mkdir(parents=True,exist_ok=True)
 shutil.copy2(gen,dest/'17592186059776.py')
 for f in ['source.json','reference/initial/basis.json','validate.py']:
  d=dest/'17592186059776'/f;d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(W/'17592186059776'/f,d)
 for script in ['check_repair.py','check_batch_selection.py']:
  s=(W/script).read_text().replace("str(ROOT.parent/'source/source.json')",repr(str((R.parent/'source/source.json').resolve()))).replace("str(ROOT.parent/'source/inventory.json')",repr(str((R.parent/'source/inventory.json').resolve())))
  (dest/script).write_text(s)
 script='check_repair.py' if name=='before1' else 'check_batch_selection.py'
 proc=subprocess.run([sys.executable,str(dest/script)],capture_output=True,text=True)
 reports.append({'name':name,'script':script,'exit_code':proc.returncode,'stdout':proc.stdout,'stderr':proc.stderr})
 if name=='current':
  proc=subprocess.run([sys.executable,str(dest/'check_repair.py')],capture_output=True,text=True);reports.append({'name':name,'script':'check_repair.py','exit_code':proc.returncode,'stdout':proc.stdout,'stderr':proc.stderr})
(R/'repair-verification.json').write_text(json.dumps(reports,indent=2))
print(json.dumps([{k:v for k,v in r.items() if k not in ['stdout','stderr']} for r in reports]))
