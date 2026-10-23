#!/usr/bin/env python3
import importlib.util,json,os,shutil,subprocess,sys
from pathlib import Path
W=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('check',W/'check_repair.py');c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
manifest=json.loads((W/'package.json').read_text());dest=W/'evidence/relocated';dest.mkdir(exist_ok=True)
for name in manifest['files']:
 src=W/name;target=dest/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,target)
assert manifest['dependencies']=={'python':sys.version.split()[0],'packages':{'sympy':c.g.sp.__version__}}
args=[sys.executable,'-B',dest/manifest['entrypoint'],'--difficulty','easy','--count','5','--seed','3782988951','--format','json']
result=subprocess.run(list(map(str,args)),cwd=dest,env=dict(os.environ,PYTHONPATH='',COURSE_ACADEMY_GENERATOR_OUTPUT_DIR=str(W/'evidence/relocated-assets')),capture_output=True,text=True)
assert result.returncode==0,result.stderr
assert json.loads(result.stdout)==json.loads((W/'evidence/prospective-batch.json').read_text())
invalid=[]
for extra in [['--count','0'],['--difficulty','unknown'],['--profile','missing']]:
 r=subprocess.run([sys.executable,'-B',str(dest/manifest['entrypoint']),*extra],capture_output=True,text=True);assert r.returncode!=0
 invalid.append({'args':extra,'exit_code':r.returncode})
small=[]
for seed in (0,1,2):
 rs=c.cli(seed);c.group_roles(rs,True);small+=rs
accepted=c.delivery(small,'small-default-sample',allow_duplicates=True)
c.group_roles(accepted,True)
# Grade only new incidental-entry controls and this small fresh sample.
controls=json.loads((W/'evidence/irrelevant-entry-controls.json').read_text())
c.grading_check(controls+small)
# Preserve distinct report names; the broader prior grader report is retained separately.
c.save('packaging-results.json',{'relocated':True,'command':list(map(str,args)),'deterministic_replay':True,'exact_dependencies':manifest['dependencies'],'invalid_input_rejections':invalid,'small_sample_count':len(small),'small_sample_delivered':len(accepted)})
c.save('commands-package.json',c.COMMANDS)
print('Relocation, exact dependencies, invalid inputs, and 15 fresh records passed.')
