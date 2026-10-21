"""One-time clean reload after the already-running repair finishes.

The marker is owned by this maintenance operation. A changed/removed marker
means somebody intervened, so this helper must not restart the campaign.
"""
import json
from pathlib import Path
import subprocess
import sys
import time

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[2]/'scripts'))
from generator_services import start_cohort
SERVICE='course-academy-generator-cohort-20261020.service'
TOKEN='load-tested-cohort-guards-20261020'
marker=HERE/'stop-after-current'
deadline=time.monotonic()+21600
result={'restarted':False,'reason':'deadline exceeded'}
while time.monotonic()<deadline:
    if not marker.exists() or marker.read_text().strip()!=TOKEN:
        result['reason']='maintenance marker changed; no restart';break
    status=subprocess.run(['systemctl','--user','is-active',SERVICE],capture_output=True,text=True).stdout.strip()
    if status not in {'active','activating','deactivating'}:
        marker.unlink()
        try:
            run=start_cohort(HERE)
            result={'restarted':True,'reason':'completed in-flight repair boundary','exit_code':0,'error':''}
        except subprocess.CalledProcessError as error:
            result={'restarted':False,'reason':'persistent service start failed','exit_code':error.returncode,'error':error.stderr}
        break
    time.sleep(5)
(HERE/'reload-verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
