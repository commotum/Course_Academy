"""Re-admit the diagnosed interrupted-draft failure after its runner fix."""
import fcntl
import json
from pathlib import Path
import sys
import time
ROOT=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT/'scripts'))
from inventory_jobs import save
JOBS=ROOT/'.local/learning/inventory/math/59d5cf13-351c-4114-be19-4c3bb64ee051'
path=JOBS/'072f348a02f7e198295324528d4e0da28b4722d3240bdbe4afd832dabe3bb391.json'
with (JOBS/'kp-17592186100992.lock').open('a') as kp_lock:
    fcntl.flock(kp_lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    with (JOBS/'jobs.lock').open('a') as jobs_lock:
        fcntl.flock(jobs_lock,fcntl.LOCK_EX)
        value=json.loads(path.read_text())
        if value['state']!='blocked':raise SystemExit('Job is no longer blocked; no change.')
        assert value['cycle']==6 and value['request']['knowledgePoint']==17592186100992
        assert value['outcome']['reason']['code']=='pipeline_process_failed'
        job=path.with_suffix('.pipeline')/'6/job.json';before=job.read_bytes();state=json.loads(before)
        assert state['stage']=='validate' and state.get('active_review_directory') and not state.get('review')
        assert not (job.parent/'publication/request.json').exists()
        archive=Path(__file__).with_name('interrupted-verifier-before.json');save(archive,value)
        event={'time':time.time(),'reason':'Resume unfinalized verifier draft after runner recovery fix; source/batch integrity and strict finalization still required.',
               'previous_error':value.get('error'),'previous_outcome':value.get('outcome'),'previous_process_failures':value.get('processFailures')}
        save(path,{**value,'state':'pending','processFailures':0,'retryAt':0,'error':None,'outcome':{},
                   'recovery_events':[*value.get('recovery_events',[]),event]})
        assert job.read_bytes()==before
        save(Path(__file__).with_name('interrupted-verifier-requeue.json'),{'passed':True,'cycle':6,'pipeline_checkpoint_unchanged':True,'job':str(path),'time':time.time()})
print('Re-admitted cycle 6; preserved repaired draft, verifier thread, and budgets.')
