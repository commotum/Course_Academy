from review import module,save,ROOT,JOB,REPO
import subprocess,json
m=module();records=[m.generate_easy(730101+i) for i in range(16)];save('fresh-seed-samples.json',records)
cmd=[str(REPO/'.venv/bin/python'),str(REPO/'generate/pipeline/check_delivery.py'),'--input',str(ROOT/'fresh-seed-samples.json'),'--source',str(JOB/'source/source.json'),'--inventory',str(JOB/'source/inventory.json'),'--difficulty','easy','--output',str(ROOT/'delivery-fresh')];p=subprocess.run(cmd,capture_output=True,text=True);save('fresh-seed-delivery-command.json',{'command':cmd,'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr})
from coverage import coverage
save('fresh-seed-coverage.json',{'command':'PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python natural_sample.py','seeds':list(range(730101,730117)),'raw':coverage(records),'accepted':coverage(json.loads((ROOT/'delivery-fresh/accepted.json').read_text())),'note':'Fixed-seed easy-grid held option permutation constant deliberately and cannot establish a positional shortcut. This independent ordinary-sampler control varies seeds.'})
print(json.loads((ROOT/'fresh-seed-coverage.json').read_text()))
