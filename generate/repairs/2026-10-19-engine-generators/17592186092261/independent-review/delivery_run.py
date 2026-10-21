import json,subprocess,sys,concurrent.futures
from pathlib import Path
E=Path(__file__).resolve().parent;ROOT=Path('/home/jake/Developer/Course_Academy');py=str(ROOT/'.venv/bin/python')
rs=json.load(open('records.json')); commands=[]
for level in ['easy','moderate','hard']:
 p=E/(level+'.json');p.write_text(json.dumps([r for r in rs if r['question'][':question/difficulty'].endswith('/'+level)]));commands.append((level,p))
commands.append(('batch',E/'runner-batch.json'))
def run(z):
 name,p=z;cmd=[py,str(ROOT/'generate/pipeline/check_delivery.py'),'--input',str(p),'--source',str((E/'../source/source.json').resolve()),'--inventory',str((E/'../source/inventory.json').resolve()),'--difficulty','easy' if name=='batch' else name,'--output',str(E/('delivery-'+name)),'--asset-root',str(E),'--math-root','/media/jake/SSD/EDB/math']
 r=subprocess.run(cmd,capture_output=True,text=True);(E/('delivery-'+name+'.log')).write_text(json.dumps(cmd)+'\n'+r.stdout+r.stderr);return {'name':name,'exit':r.returncode,'summary':r.stdout[-1200:]}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:results=list(ex.map(run,commands))
(E/'delivery-commands.json').write_text(json.dumps(results,indent=2));print(json.dumps(results,indent=2))
pairs=json.load(open('pairs.json'));selected=[]
for kind,qid in [('relevant','q-107458'),('irrelevant','q-312462'),('irrelevant','q-107459')]:
 p=next(p for p in pairs if p['kind']==kind and p['template']==qid);selected.extend([p['before'],p['after']])
selected.extend([next(r for r in rs if r['generation']['template']==qid) for qid in ['q-71881','q-48565','q-340969','q-107463']]);(E/'render-records.json').write_text(json.dumps(selected))
cmd=[py,str(ROOT/'generate/pipeline/render_preview.py'),'--input',str(E/'render-records.json'),'--output',str(E/'render'),'--asset-root',str(E)]
r=subprocess.run(cmd,capture_output=True,text=True);(E/'render.log').write_text(json.dumps(cmd)+'\n'+r.stdout+r.stderr);print(r.returncode,r.stdout[-500:],r.stderr[-1000:])
