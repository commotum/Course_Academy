"""Save current backlog status and track the original pending packages."""
from collections import Counter
from pathlib import Path
import time
from scripts.config import Config
from scripts.outbox import target_id
from scripts.storage import atomic_json, read_json

root=Path(__file__).resolve().parent
config=Config()
items=[]
for path in sorted(config.spool_root.glob('*.json')):
 item=read_json(path,{})
 if item.get('target_id')!=target_id(config):continue
 directory=Path(item['capture_directory'])
 result=item.get('result') or read_json(directory/'database/result.json',{}) or {}
 items.append({'spool':str(path),'account':item.get('account'),'task_id':directory.name,
  'directory':str(directory),'status':item.get('status'),'attempts':item.get('attempts'),
  'last_attempt_at':item.get('last_attempt_at'),'next_attempt_at':item.get('next_attempt_at'),
  'reason':item.get('error') or result.get('reason'),
  'unresolved_request':(directory/'database/request.json').exists(),
  'capture_only':bool(item.get('capture_only')),
  'omissions':[{'id':o.get('id'),'capture_key':o.get('capture_key'),'kind':o.get('kind'),
               'reason':o.get('reason')} for o in result.get('omissions',[])]})
initial=read_json(root/'initial-inventory.json',[])
by_path={item['spool']:item for item in items}
pending_before=[item for item in initial if item['status']=='pending']
transitions=[{'account':old['account'],'task_id':old['task_id'],
             'status':by_path.get(old['spool'],{}).get('status','missing'),
             'omissions':by_path.get(old['spool'],{}).get('omissions',[])} for old in pending_before]
summary={'observed_at':time.time(),'items':len(items),'statuses':dict(Counter(i['status'] for i in items)),
 'pending':sum(i['status'] not in ('verified','no_changes') and not i['capture_only'] for i in items),
 'pending_errors':sum(bool(i['reason']) for i in items if i['status'] not in ('verified','no_changes')),
 'unresolved_requests':sum(i['unresolved_request'] for i in items),
 'terminal_with_omissions':sum(bool(i['omissions']) for i in items if i['status'] in ('verified','no_changes')),
 'initial_pending':len(pending_before),
 'initial_pending_now_terminal':sum(t['status'] in ('verified','no_changes') for t in transitions),
 'initial_pending_transitions':transitions}
atomic_json(root/'current-inventory.json',{'summary':summary,'items':items})
print({k:v for k,v in summary.items() if k!='initial_pending_transitions'})
