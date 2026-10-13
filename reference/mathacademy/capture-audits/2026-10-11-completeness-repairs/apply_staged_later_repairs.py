"""Consume restricted reviewed source candidates using normal locked recovery imports."""
from pathlib import Path
import argparse,hashlib,json,subprocess,sys,time
ROOT=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('offsets',type=int,nargs='+');a=p.parse_args();remaining=set(a.offsets)
while remaining:
    ready=[]
    for offset in sorted(remaining):
        path=ROOT/f'later-source-review-{offset}.json'
        if not path.exists():continue
        rows=json.loads(path.read_text())
        if not rows:continue
        row=rows[-1]
        if row['status'] in ('prepared','verified'):ready.append((row.get('completed_at',0),offset,row))
        elif row['status']=='error':
            print(json.dumps({'event':'source_review_failed','offset':offset,'error':row.get('error')}),flush=True);remaining.remove(offset)
    if not ready:
        if remaining:time.sleep(2)
        continue
    _,offset,row=min(ready)
    if row.get('status')=='prepared':
        directory=Path(row['directory']);protected=row['source_only_completion_assertions']['protected_sha256']
        if any(hashlib.sha256((directory/name).read_bytes()).hexdigest()!=sha for name,sha in protected.items()):
            print(json.dumps({'event':'source_changed_before_apply','offset':offset}),flush=True);remaining.remove(offset);continue
    print(json.dumps({'event':'apply_start','offset':offset,'task_id':row['task_id']}),flush=True)
    with (ROOT/f'later-repair-run-{offset}.log').open('w') as log:
        r=subprocess.run([sys.executable,str(ROOT/'run_later_repairs.py'),'--offset',str(offset),'--limit','1'],stdout=log,stderr=subprocess.STDOUT)
    print(json.dumps({'event':'apply_complete','offset':offset,'exit_code':r.returncode}),flush=True);remaining.remove(offset)
print(json.dumps({'event':'staged_apply_complete'}),flush=True)
