"""Restore only the queue envelope whose committed result replaced its bytes."""
import fcntl
import hashlib
import json
from pathlib import Path
import sys
import time
ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT/'scripts'))
from inventory_jobs import save
JOBS=ROOT/'.local/learning/inventory/math/59d5cf13-351c-4114-be19-4c3bb64ee051'
KEY='9286c43cb50951ccc02554f93c61e6b96164762708ddd3ce2780f2a3795f2192'
path=JOBS/(KEY+'.json')
with (JOBS/'kp-17592186096671.lock').open('a') as kp_lock:
    fcntl.flock(kp_lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    with (JOBS/'jobs.lock').open('a') as jobs_lock:
        fcntl.flock(jobs_lock,fcntl.LOCK_EX)
        before=path.read_bytes();outcome=json.loads(before)
        if 'state' in outcome:
            raise SystemExit('Queue envelope already restored; no change.')
        state=json.loads((JOBS/(KEY+'.pipeline')/'1/job.json').read_text())
        assert state['stage']=='verified' and state['request']['job_kind']=='refill'
        assert state['request']['kp']==17592186096671 and state['request']['difficulty']=='hard'
        assert outcome['publication']==state['publication'] and state['publication']['passed']
        assert state['publication']['request_key']=='capture-9b17e87c-f16b-48cd-b4f2-347eb83c886f'
        sibling=json.loads((JOBS/'e1219785f462e272e132a75941fc7c264b72c3c31d555748b4a03a81b95c24c0.json').read_text())
        assert sibling['request']['knowledgePoint']==state['request']['kp']
        learner=sibling['learner']; count=state['request']['count']
        assert hashlib.sha256(json.dumps([learner,state['request']['kp'],'refill','hard']).encode()).hexdigest()==KEY
        request={**sibling['request'],'difficulty':'hard','missing':count,'available':5-count,
                 'shortage':count,'stage':'generate','script':state['registration'],
                 'basis':state['publication']['basis_after']}
        restored={'key':KEY,'learner':learner,'lineage':sibling['lineage'],'request':request,
                  'state':'awaiting-verification','cycle':1,'attempts':1,'processFailures':0,
                  'replenishments':1,'completedAt':state['completed'],'retryAt':time.time()+300,
                  'exitCode':0,'outcome':outcome,'error':None,'recoveryOnly':False,
                  'metadata_recovery':{'time':time.time(),'reason':'Result/job temporary-file collision; committed receipt retained; inventory must confirm stock.'}}
        archive=Path(__file__).with_name('refill-metadata-before.json')
        archive.write_bytes(before)
        save(path,restored)
        save(Path(__file__).with_name('refill-metadata-recovery.json'),{'passed':True,'path':str(path),
             'request_key':state['publication']['request_key'],'basis_after':state['publication']['basis_after'],
             'new_transactions':0,'state':restored['state'],'cycle':1})
print('Restored queue metadata; retained acknowledged publication; no database writes.')
