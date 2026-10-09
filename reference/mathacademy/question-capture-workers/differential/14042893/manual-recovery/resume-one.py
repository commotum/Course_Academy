import json,subprocess,sys,time
from pathlib import Path
repo=Path('/home/jake/Developer/Course_Academy');audit=Path(__file__).resolve().parent;directory=audit.parent
sys.path.insert(0,str(repo/'scripts/question_capture'));from fleet import config,selected,capture_running,supervisor_running
worker=selected(config(),['differential'])[0]
assert not capture_running(worker) and not supervisor_running(worker),'DE account is already owned'
command=json.loads((audit/'normal-command.json').read_text())+['--resume',str(directory),'--limit','1','--no-capture-repair','--edb-bin','/home/jake/Developer/EDB/target/release/edb','--database','course-academy-v2','--endpoint','/tmp/course-academy-edb-v2/writer.sock']
(audit/'resume-command.json').write_text(json.dumps(command,indent=2)+'\n')
(audit/'recovery-start.json').write_text(json.dumps({'started_at':time.time(),'capture_lock_released':True,'normal_profile':str(worker['profile']),'original_solver_session_retained':True},indent=2)+'\n')
with (audit/'resume.log').open('w') as log:result=subprocess.run(command,cwd=repo,stdout=log,stderr=subprocess.STDOUT)
(audit/'recovery-exit.json').write_text(json.dumps({'finished_at':time.time(),'returncode':result.returncode},indent=2)+'\n')
print('Recovery exit',result.returncode)
