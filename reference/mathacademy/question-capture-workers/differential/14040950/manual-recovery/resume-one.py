import json,subprocess
from pathlib import Path
root=Path('reference/mathacademy/question-capture-workers/differential/14040950').resolve()
command=json.loads(Path('.local/question_capture-workers/differential/supervision/fleet-worker.json').read_text())['command']
command+=['--resume',str(root),'--limit','1','--no-capture-repair','--edb-bin','/home/jake/Developer/EDB/target/release/edb','--database','course-academy-v2','--endpoint','/tmp/course-academy-edb-v2/writer.sock']
(root/'manual-recovery/resume-command.json').write_text(json.dumps(command,indent=2)+'\n')
with (root/'manual-recovery/resume.log').open('w') as log:
 result=subprocess.run(command,stdout=log,stderr=subprocess.STDOUT)
print('Recovery returncode',result.returncode)
