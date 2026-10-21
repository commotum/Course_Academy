"""Run every declared retained-finding command and ensure runtime bytes stay fixed."""
import pathlib,json,hashlib,sys,subprocess
P=pathlib.Path(__file__).resolve().parents[1];m=json.loads((P/'package.json').read_text());findings=json.loads((P/'repair-regressions.json').read_text())['findings']
def hashes():return {f:hashlib.sha256((P/f).read_bytes()).hexdigest() for f in m['files']}
before=hashes();rows=[]
for f in findings:
 cmd=[sys.executable,str(P/f['script']),*f['args']];r=subprocess.run(cmd,cwd=P,text=True,capture_output=True)
 rows.append(dict(finding_id=f['id'],command=cmd,exit_code=r.returncode,output=r.stdout+r.stderr));assert r.returncode==0,rows[-1]
assert before==hashes()
(P/'evidence/registered-regressions.json').write_text(json.dumps({'runtime_unchanged':True,'findings':rows},indent=2));print('All four registered finding regressions passed; runtime hashes unchanged.')
