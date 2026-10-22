import json,subprocess
from pathlib import Path
E=Path(__file__).resolve().parent;J=E.parent;R=Path('/home/jake/Developer/Course_Academy');reports=[]
for name in ['batch','sampler-93827-5','sampler-57209-5','sampler-57209-24','exact-prefix-repaired','catalog','counterfactual-records']:
 cmd=[str(R/'.venv/bin/python'),'-B',str(R/'generate/pipeline/check_delivery.py'),'--input',str(E/(name+'.json')),'--source',str(J/'source/source.json'),'--inventory',str(J/'source/inventory.json'),'--difficulty','easy','--output',str(E/('delivery-'+name)),'--math-root','/media/jake/SSD/EDB/math']
 c=subprocess.run(cmd,capture_output=True,text=True);assert c.returncode==0,c.stderr+c.stdout
 reports.append({'name':name,'command':cmd,'returncode':c.returncode,'report':'delivery-'+name+'/delivery.json'})
(E/'delivery-execution.json').write_text(json.dumps(reports,indent=2)+'\n');print('Delivery completed',len(reports))
