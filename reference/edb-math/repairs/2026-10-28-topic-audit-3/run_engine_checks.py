import json,re,subprocess
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3]
result=subprocess.run(['cargo','test','--offline','--lib'],cwd=R,capture_output=True,text=True)
(H/'engine-tests.stdout.txt').write_text(result.stdout);(H/'engine-tests.stderr.txt').write_text(result.stderr)
match=re.search(r'test result: (ok|FAILED)\. (\d+) passed; (\d+) failed',result.stdout)
report={'passed':result.returncode==0,'command':'cargo test --offline --lib','tests_passed':int(match[2])if match else None,'failures':int(match[3])if match else None,'database_writes':0}
(H/'engine-regressions.json').write_text(json.dumps(report,indent=2)+'\n');print(report,flush=True);result.check_returncode()
