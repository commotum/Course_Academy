import importlib.util,json,subprocess
from pathlib import Path
H=Path(__file__).resolve().parent;s=importlib.util.spec_from_file_location('v',H/'validate.py');v=importlib.util.module_from_spec(s);s.loader.exec_module(v);g=v.g
report=[]
for c in range(1,21):
 p=g.defaults(g.case('q-132982'));p['c']=c;r=g.generate('easy',0,'q-132982',p);path=H/'blank-audit-input.json';path.write_text(json.dumps([v.engine_item('c='+str(c),r)]));proc=subprocess.run([str(H/'check-current-engine'),str(path),str(H/'blank-audit-report.json')],capture_output=True,text=True)
 report.append({'c':c,'passed':proc.returncode==0,'details':proc.stderr if proc.returncode else json.loads((H/'blank-audit-report.json').read_text())})
(H/'blank-domain-audit.json').write_text(json.dumps(report,indent=2));print('supported c',[x['c']for x in report if x['passed']]);print('excluded c',[x['c']for x in report if not x['passed']])
