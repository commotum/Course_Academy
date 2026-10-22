"""Read-only post-filter cue tests, learner-draw reproduction, relocation."""
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[1];E=ROOT/'evidence'
spec=importlib.util.spec_from_file_location('audit',ROOT/'checks/validate_repair.py')
audit=importlib.util.module_from_spec(spec);spec.loader.exec_module(audit)
records=json.loads((E/'delivery-fresh/accepted.json').read_text())
# Source/native selection sorts unique entity ids; offline surrogate ids 1..N
# preserve that operation without publishing or assigning database entities.
# Every candidate is easy: a positive easy weight chooses this pool, then the
# second SHA-derived uniform draw selects an index. Live history is unavailable.
selected=[]
for i in range(100):
    digest=hashlib.sha256(('course-academy/question-selection/v1/repair-'+str(i)).encode()).digest()
    u=(int.from_bytes(digest[8:16],'big')>>11)/(1<<53)
    selected.append(records[int(u*len(records))])
report=audit.shortcuts(selected);audit.assert_no_fixed_cue(report)
(E/'learner-selection.json').write_text(json.dumps({'passed':True,'algorithm_source':'engine/rust/question_selection.rs::select',
    'seeds':'repair-0 through repair-99','pool_count':len(records),'draws':100,'easy_positive_weight':True,
    'all_candidate_difficulties':'easy','sampling':'native SHA256 index rule, read-only surrogate ids in accepted order',
    'limitations':['No live learner history or actual future database entity ids are available.','A zero easy weight produces no eligible generated question; other pre-existing difficulties are outside this candidate capture.','Without configured weights the engine selects the smallest entity id; this capture cannot establish future ordering.'],
    'shortcut_report':report},indent=2)+'\n')
# Measure exactly the old three predeclared rank/coordinate strategies.
batch=json.loads((E/'delivery-batch/accepted.json').read_text())
rows=[]
for r in records+batch:
    sid=r['generation']['bank_profile'];vals,ix=audit.read_bank(r['question']);prediction=None
    if sid=='q-34601':prediction=sorted(range(5),key=lambda i:vals[i])[1];rule='second-smallest scalar'
    elif sid=='q-105161':prediction=sorted(range(5),key=lambda i:vals[i])[0];rule='smallest scalar'
    elif sid=='q-73933':
        matches=[i for i,v in enumerate(vals) if v[1]==min(z[1] for z in vals)]
        prediction=matches[0] if len(matches)==1 else None;rule='unique minimum second coordinate'
    else:continue
    rows.append({'id':r['question'][':question/id'],'profile':sid,'rule':rule,'attempted':prediction is not None,'success':prediction==ix,'is_batch':r in batch})
(E/'old-shortcut-probes.json').write_text(json.dumps({'chance_baseline':0.2,'records':rows,
    'summary':{sid:{'attempts':sum(x['attempted'] for x in rows if x['profile']==sid),
                    'successes':sum(x['success'] for x in rows if x['profile']==sid)} for sid in ('q-34601','q-105161','q-73933')}},indent=2)+'\n')
manifest=json.loads((ROOT/'package.json').read_text());declared=manifest['files']
assert all(not Path(f).is_absolute() and '..' not in Path(f).parts for f in declared)
assert 'package.json' not in declared
with tempfile.TemporaryDirectory(prefix='vector-relocation-',dir=E) as directory:
    dest=Path(directory)
    for filename in declared:
        p=dest/filename;p.parent.mkdir(exist_ok=True,parents=True);shutil.copy2(ROOT/filename,p)
    env=__import__('os').environ.copy();env['COURSE_ACADEMY_GENERATOR_OUTPUT_DIR']=str(dest/'generated-assets')
    cmd=[sys.executable,str(dest/manifest['entrypoint']),'--difficulty','easy','--count','5','--seed','48291','--format','json']
    result=subprocess.run(cmd,cwd='/tmp',env=env,capture_output=True,text=True,check=True)
    relocated=json.loads(result.stdout)
    assert relocated==json.loads((E/'batch.json').read_text())
    for r in relocated:audit.check(r)
    (E/'relocated-records.json').write_text(json.dumps(relocated,indent=2)+'\n')
    runtime_outputs=[str(p.relative_to(dest)) for p in dest.rglob('*') if p.is_file() and str(p.relative_to(dest)) not in declared]
    assert not runtime_outputs,runtime_outputs
(E/'packaging.json').write_text(json.dumps({'passed':True,'relocation_cwd':'/tmp','seed':48291,'count':5,'records_equal':True,
    'runtime_files':declared,'dependencies':manifest['dependencies'],'unexpected_runtime_writes':[],
    'runtime_hashes':{f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in declared}},indent=2)+'\n')
print(json.dumps({'passed':True,'learner_draws':100,'relocated_records':5,'runtime_files':len(declared)}))
