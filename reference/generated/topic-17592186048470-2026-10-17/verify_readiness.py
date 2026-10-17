"""Read-only bounded readiness verification; never submits or starts an attempt.

Run from repo root with --label after --require-ready after publication.
Each read saves a new basis-named input/result and preserves the before evidence.
"""
from pathlib import Path
import argparse,json,subprocess,sys,threading
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT/'capture'))
from scripts.config import Config
from scripts.database.client import EDBClient

def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--label',default='check');parser.add_argument('--require-ready',action='store_true');args=parser.parse_args()
 if not args.label or any(c not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_' for c in args.label):raise ValueError('Invalid output label')
 db=EDBClient(Config(capture_only=True),threading.Event());identity=db.status()
 before=json.loads((HERE/'read-input.json').read_text())
 assert identity['database']==before['database'] and identity['lineage']==before['lineage'],'Database lineage changed'
 payload={**identity,'learner':before['learner'],'topic':before['topic']}
 source=HERE/'readiness.rs';command=json.loads((HERE/'readiness-build-command.json').read_text());binary=ROOT/command[-1]
 linked=[Path(arg.split('=',1)[1]) for arg in command if '=' in arg and Path(arg.split('=',1)[1]).is_file()]
 if not binary.exists() or binary.stat().st_mtime_ns<max(p.stat().st_mtime_ns for p in [source,*linked]):subprocess.run(command,cwd=ROOT,check=True)
 input_path=HERE/(args.label+'-input-'+str(identity['basis'])+'.json');output=HERE/(args.label+'-readiness-'+str(identity['basis'])+'.json')
 input_path.write_text(json.dumps(payload,indent=2)+'\n')
 subprocess.run([str(binary),str(input_path),str(output)],cwd=ROOT,env=db.environment,check=True)
 result=json.loads(output.read_text());assert result['database_writes']==0 and result['learner_attempts_created']==0
 if args.require_ready and not result['lesson_ready']:raise SystemExit('Lesson still has an inventory shortage; see '+str(output))

if __name__=='__main__':main()
