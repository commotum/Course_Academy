from pathlib import Path
import subprocess,json,sys
r=Path(__file__).resolve().parent;j=r.parent;repo=Path('/home/jake/Developer/Course_Academy');py=str(repo/'.venv/bin/python')
commands=[]
for file,difficulty,name in [('batch.json','easy','delivery-batch'),('easy-grid.json','easy','delivery-easy'),('moderate-delivery-input.json','moderate','delivery-moderate'),('hard-delivery-input.json','hard','delivery-hard')]:
 cmd=[py,str(repo/'generate/pipeline/check_delivery.py'),'--input',str(r/file),'--source',str(j/'source/source.json'),'--inventory',str(j/'source/inventory.json'),'--difficulty',difficulty,'--output',str(r/name),'--asset-root',str(r)]
 p=subprocess.run(cmd,capture_output=True,text=True);commands.append({'command':cmd,'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr});print(name,p.returncode,p.stdout.strip(),p.stderr[-300:])
(r/'delivery-commands.json').write_text(json.dumps(commands,indent=2))
