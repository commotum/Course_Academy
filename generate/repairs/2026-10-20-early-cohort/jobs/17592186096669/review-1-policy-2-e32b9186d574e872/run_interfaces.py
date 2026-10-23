import subprocess,json,concurrent.futures,os
from pathlib import Path
ROOT=Path(__file__).resolve().parent;JOB=ROOT.parent;REPO=Path('/home/jake/Developer/Course_Academy');PY=REPO/'.venv/bin/python'
commands={}
for name in ['samples','controlled','batch']:
 commands['delivery-'+name]=[str(PY),str(REPO/'generate/pipeline/check_delivery.py'),'--input',str(ROOT/(name+'.json')),'--source',str(JOB/'source/source.json'),'--inventory',str(JOB/'source/inventory.json'),'--difficulty','easy','--output',str(ROOT/('delivery-'+name)),'--asset-root',str(ROOT),'--math-root','/media/jake/SSD/EDB/math']
commands['grader']=[str(REPO/'generate/runs/current/check-engine'),str(ROOT/'grader-input.json'),str(ROOT/'grader-report.json')]
commands['render']=[str(PY),str(REPO/'generate/pipeline/render_preview.py'),'--input',str(ROOT/'render-records.json'),'--output',str(ROOT/'render'),'--asset-root',str(ROOT)]
def run(item):
 name,cmd=item;r=subprocess.run(cmd,capture_output=True,text=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
 (ROOT/(name+'.log')).write_text(r.stdout+'\n'+r.stderr)
 return name,{'command':cmd,'exit_code':r.returncode,'log':name+'.log'}
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:results=dict(pool.map(run,commands.items()))
(ROOT/'interface-execution.json').write_text(json.dumps(results,indent=2));print(json.dumps(results,indent=2))
