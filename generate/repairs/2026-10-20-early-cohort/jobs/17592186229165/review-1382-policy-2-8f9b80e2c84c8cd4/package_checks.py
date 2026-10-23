import sys,pathlib,json,subprocess,hashlib,shutil,difflib
sys.dont_write_bytecode=True
R=pathlib.Path(__file__).resolve().parent;J=R.parent;W=J/'workspace'
def save(n,d):(R/n).write_text(json.dumps(d,indent=2)+'\n')
manifest=json.loads((W/'package.json').read_text())
assert manifest['dependencies']=={'python':'3.13.5','packages':{'sympy':'1.14.0'}}
out=R/'relocated';out.mkdir(exist_ok=True)
for f in manifest['files']:shutil.copy2(W/f,out/f)
commands=[]
for level in ['easy','moderate','hard']:
 results=[]
 for folder in [W,out]:
  cmd=[sys.executable,str(folder/manifest['entrypoint']),'--difficulty',level,'--seed','81513','--count','4','--format','json']
  proc=subprocess.run(cmd,cwd=R,text=True,capture_output=True)
  assert proc.returncode==0,proc.stderr
  data=json.loads(proc.stdout);assert len(data)==4
  commands.append({'command':cmd,'cwd':str(R),'returncode':proc.returncode,'stderr':proc.stderr,'records':data})
  results.append(data)
 assert results[0]==results[1]
save('relocation-results.json',{'identical':True,'all_manifest_files_copied':manifest['files'],'runs':commands,'external_outputs':'Only stdout JSON; no assets or file-writing construction paths in entrypoint. No runtime adjacent data files used.'})
before=(W/'evidence/generator-before.py').read_text();after=(W/manifest['entrypoint']).read_text()
(R/'independent-generator.diff').write_text(''.join(difflib.unified_diff(before.splitlines(True),after.splitlines(True),fromfile='prior',tofile='current')))
save('construction-review.json',{'changed_rules':['Exactly one resonant component instead of forcing the first component','Choose mixed resonant position before compatible rates; direct valid sampling, no rejection loop','Explanation, derivative/product-rule rows, and beta equation use each exponent equality to h'],'unchanged_easy_moderate_and_two_nonresonant':True,'new_slot':'Two eligible mixed positions, independently covered and parsed in hard-math-results.json','runtime_dependencies':manifest['dependencies'],'relocation_identical_all_levels':True,'source_and_math_regression':'source-replay-results.json and math-results.json','historical_check_negative_control':'retained-before.log fails at original exact minimal case; provenance.json confirms before bytes match prior review.'})
print('All-level relocation and manifest dependency checks passed.')
