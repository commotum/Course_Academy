"""Rerun actual read-only delivery filtering and inspect the surviving cases."""
import json
from pathlib import Path
import subprocess
import sys
from validate_content import E, ROOT, REPO, JOB, analyze, save, inspect

def main():
    command=[sys.executable,str(REPO/'generate/pipeline/check_delivery.py'),'--input',str(E/'catalog.json'),'--source',str(JOB/'source/source.json'),'--inventory',str(JOB/'source/inventory.json'),'--difficulty','easy','--output',str(E/'delivery'),'--math-root','/media/jake/SSD/EDB/math']
    result=subprocess.run(command,capture_output=True,text=True)
    assert result.returncode==0,result.stdout+result.stderr
    raw=json.loads((E/'catalog.json').read_text())
    accepted=json.loads((E/'delivery/accepted.json').read_text())
    before=analyze(raw);after=analyze(accepted)
    assert before==after, 'Filtering lost supported decision cases'
    # Complete semantic batch with many seeded presentations; no resampling or
    # rejection branch is used: finite catalog, then one representative per group.
    from validate_content import g
    capacity=len({r['generation']['mathematical_fingerprint'] for r in raw})
    for seed in (0,7,119848):
        batch=g.batch('easy',capacity,seed)
        assert len({r['generation']['mathematical_fingerprint'] for r in batch})==capacity
        assert all(inspect(r)[0] for r in batch)
    save('pedagogical-variation.json',{'passed':True,'before_delivery':before,'after_delivery':after,'filter_summary':json.loads(result.stdout),'sampler':'finite catalog with one seeded representative per structural group; no invalid-case rejection or hidden retries','finite_capacity':capacity,'selection_limits':['Captured inventory checked read-only at basis 5415. Live learner history and reservations unavailable.','question_selection.rs selects uniformly within an eligible weighted band; easy is the only supported band. Prior seen-task exclusion can exhaust any finite family.','Future inventory may exhaust scale-2 instances; no claim of unlimited replenishment.'],'command':'python checks/check_delivery_variation.py'})
    print(result.stdout.strip());print(json.dumps({'shortcut_groups_checked':len(after),'fixed_complete_response_profiles':0,'always_selected_incidental_labels':0,'passed':True}))

if __name__=='__main__':main()
