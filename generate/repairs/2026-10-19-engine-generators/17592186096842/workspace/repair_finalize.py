"""Post-filter native controls, workspace-contained relocation and provenance."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from repair_validate import E, ENGINE, REPO, save
from validate import independent, grading

records = json.loads((E/'accepted-records.json').read_text())
controls = [r for r in records if
            (r['generation']['template']=='slope_sum_radio' and r['generation']['seed'] in [17,21]) or
            (r['generation']['template']=='sqrt_quadratic_blank' and
             r['generation']['parameters'] in [dict(a=-1,b=0,c=1),dict(a=-1,b=0,c=4)])]
# One changed-evidence starting item duplicates an already delivered role control.
assert len(controls)==23
cases = [grading(r, independent(r), 'post-filter control '+str(i)) for i,r in enumerate(controls)]
save('post-delivery-grader-input.json', cases)
cmd = [str(ENGINE),str(E/'post-delivery-grader-input.json'),str(E/'post-delivery-grader-report.json')]
result = subprocess.run(cmd,capture_output=True,text=True)
save('post-delivery-grader-command.json',dict(command=cmd,exit_code=result.returncode,
                                            stdout=result.stdout,stderr=result.stderr))
assert result.returncode==0, result.stderr

manifest = json.loads(Path('package.json').read_text())
with tempfile.TemporaryDirectory(dir=E) as tmp:
    dest = Path(tmp).resolve()
    for name in manifest['files']:
        (dest/name).parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(name,dest/name)
    args = ['--difficulty','moderate','--count','5','--seed','4221317821','--format','json']
    original = subprocess.check_output([sys.executable,'generator.py',*args])
    relocated = subprocess.check_output([sys.executable,str(dest/'generator.py'),*args],cwd=dest)
    assert original==relocated
save('final-provenance.json',{
    'python':sys.version.split()[0],
    'sympy':__import__('sympy').__version__,
    'declared_file_relocation':'passed; temporary package remained inside workspace',
    'hashes':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in
              [ENGINE,REPO/'generate/runs/current/check-engine.rs',REPO/'engine/rust/symbolic.rs',
               REPO/'engine/rust/question_selection.rs',Path('../source/source.json'),Path('../source/inventory.json')]},
    'native_harness':'supplied executable and harness unchanged; no replacement grader',
    'key_matrix':'../repair-key-probes.json and ../repair-key-results.json; diagnostic observed outcomes, not successful equivalence validation',
    'selection_limit':'Configured uniform within-band draw with synthetic entity ordering. Live history, database IDs and policy unavailable; unconfigured legacy policy chooses first candidate.',
})
summary=json.loads((E/'summary.json').read_text())
summary['native_regression_checks']=418
summary['post_delivery_control_records']=len(controls)
summary['post_delivery_native_checks']=sum(len(c['checks']) for c in cases)
summary['rendering']={'records':6,'DOM':'passed','visual_inspection':'visual-inspection.md'}
save('summary.json',summary)
print(json.dumps({k:summary[k] for k in ['status','post_delivery_control_records','post_delivery_native_checks','rendering']}))
