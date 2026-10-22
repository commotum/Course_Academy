import json,subprocess
from pathlib import Path
from targeted_review import audit
E=Path.cwd();J=E.parent;R=Path('/home/jake/Developer/Course_Academy')
rows=json.loads((E/'targeted-sampler-records.json').read_text());runs=json.loads((E/'targeted-results.json').read_text())['fresh_runs'];offset=0;reports=[]
for case in runs:
 count=case['count'];part=rows[offset:offset+count];offset+=count
 if count not in (5,24):continue
 name='sampler-'+str(case['seed'])+'-'+str(count);p=E/(name+'.json');p.write_text(json.dumps(part,indent=2)+'\n')
 cmd=[str(R/'.venv/bin/python'),'-B',str(R/'generate/pipeline/check_delivery.py'),'--input',str(p),'--source',str(J/'source/source.json'),'--inventory',str(J/'source/inventory.json'),'--difficulty','easy','--output',str(E/('delivery-'+name)),'--math-root','/media/jake/SSD/EDB/math']
 c=subprocess.run(cmd,capture_output=True,text=True);assert c.returncode==0,c.stdout+c.stderr
 accepted=json.loads((E/('delivery-'+name)/'accepted.json').read_text());a=audit(accepted)
 assert len(accepted)==count and not a['failures'],(name,a)
 reports.append({'command':cmd,'before':audit(part),'after':a,'count':count,'accepted':len(accepted),'records':name+'.json','delivery_report':'delivery-'+name+'/delivery.json'})
(E/'targeted-delivery-results.json').write_text(json.dumps(reports,indent=2)+'\n');print(json.dumps({'batches':len(reports),'all_survive':True,'conditional_failures':0}))
