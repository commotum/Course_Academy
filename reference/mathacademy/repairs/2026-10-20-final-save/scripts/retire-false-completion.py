from pathlib import Path
import hashlib,shutil,os,time
from scripts.storage import read_json,atomic_json,file_lock
from scripts.config import Config
from scripts.outbox import target_id
c=Config();p=c.output_root/'14352901';root=c.repo_root/'reference/mathacademy/repairs/2026-10-20-final-save/false-completion';root.mkdir(exist_ok=True)
raw=p/'observations/complete-94157a301ae97a744c15.html';markup=raw.read_text()
assert 'taskAlreadyCompleted = false' in markup
assert '<div id="finalScreen-completionMessage"></div>'in markup
assert '<div id="finalScreen-pointsMessage"></div>'in markup
checkpoint=read_json(p/'checkpoint.json');assert not checkpoint['presentations']and not checkpoint['steps']and not checkpoint['judgments']
assert not read_json(p/'content.json')['questions']
with file_lock(c.database_lock):
 assert not(p/'database/request.json').exists()
 matches=[f for f in c.spool_root.glob('*.json')if(read_json(f,{})or{}).get('capture_directory')==str(p)]
 assert len(matches)==1
 queue=read_json(matches[0]);assert queue['status']=='verified'
 from scripts.database.edn import loads
 from scripts.database.prepare import activity_identity
 from scripts.database.client import EDBClient
 import threading
 assert not loads((p/'database/prepared-batches.edn').read_text())
 client=EDBClient(c,threading.Event());basis=client.basis()
 found=client.query('[:find ?a :in $ ?id :where [?a :activity/id ?id]]',[activity_identity(read_json(p/'content.json'),'review')],root,'no-activity',basis)
 assert not found,found
 files=[matches[0],p/'capture-complete.json',p/'handoff-complete.json',p/'import-status.json',c.state_root/'completed.json',c.state_root/'xp.json']
 hashes={}
 for f in files:
  destination=root/('outbox.json'if f==matches[0]else('state-'+f.name if f.parent==c.state_root else f.name))
  if not destination.exists():shutil.copyfile(f,destination)
  hashes[str(f)]=hashlib.sha256(f.read_bytes()).hexdigest()
 atomic_json(root/'original-hashes.json',hashes)
 for name in ('completed.json','xp.json'):
  path=c.state_root/name;data=read_json(path);entry=data.pop('14352901',None);assert entry is not None
  atomic_json(path,data)
 proof={'status':'withdrawn_false_completion','task_id':'14352901','reason':'A 502 stylesheet failure exposed an empty final-screen template while Question 1 was unanswered. The original script says taskAlreadyCompleted=false, the source queue card remains Start at 0%, and no attempts, grade, XP or completion message were observed.','source_file':str(raw),'source_sha256':hashlib.sha256(raw.read_bytes()).hexdigest(),'original_capture_preserved':True,'database_activity_or_learner_changes':0,'actual_attempts':0,'retired_at':time.time(),'outbox_archive':str(root/'outbox.json')}
 atomic_json(root/'verification.json',proof);atomic_json(p/'capture-suspended.json',proof)
 for f in [matches[0],p/'capture-complete.json',p/'handoff-complete.json',p/'import-status.json']:f.unlink()
 print(proof)
