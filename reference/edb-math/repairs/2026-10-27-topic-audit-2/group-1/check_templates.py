import concurrent.futures,json,os,subprocess
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4];D=json.loads((H/'current.json').read_text());G=dict(D['generators']);inventory=json.loads((H/'generator-template-inventory.json').read_text());stages={c['kp']:c for c in json.loads((H/'format-generator-stage-config.json').read_text())};stage=json.loads((H/'generator-stage-config.json').read_text());stages[17592186172038]={'directory':stage['directory'],'entrypoint':stage['old_manifest']['entrypoint']};tasks=[]
for entry in inventory:
 k=entry['kp'];templates=(entry['result']or{}).get('TEMPLATES',{})
 if k==17592186064167:templates={'easy':['integral_thin','function'],'moderate':['integral_thin','function'],'hard':['function']}
 if isinstance(templates,dict):
  for name,meta in templates.items():
   if name in['easy','moderate','hard']:
    tasks.extend((k,name,t)for t in meta);continue
   if isinstance(meta,dict):bands=meta.get('levels',[meta.get('level','easy')])
   elif isinstance(meta,list):bands=[meta[0]]
   else:continue
   tasks.extend((k,b,name)for b in bands if b in['easy','moderate','hard'])
 elif isinstance(templates,list):
  tasks.extend((k,b,t)for b in['easy','moderate','hard']for t in templates if k!=17592186172038 or b!='hard'or t in['two_quadratic','rational_square','affine_fraction'])
def run(task):
 k,b,t=task;c=stages.get(k);p=Path(c['directory'])/c['entrypoint']if c else Path('/media/jake/SSD/EDB/math')/G[k][':question-generator/script'];p=p if p.exists()else R/G[k][':question-generator/script'];assets=H/'template-assets'/str(k)/b/t;assets.mkdir(parents=True,exist_ok=True);args=[str(R/'.venv/bin/python'),str(p),'--difficulty',b,'--count','1','--seed','27102031','--format','json','--template',t]
 try:
  r=subprocess.run(args,text=True,capture_output=True,timeout=90,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','COURSE_ACADEMY_GENERATOR_OUTPUT_DIR':str(assets)});data=json.loads(r.stdout)if r.returncode==0 else[];data=data.get('records',[])if isinstance(data,dict)else data;return {'kp':k,'difficulty':b,'requested_template':t,'returncode':r.returncode,'stderr':r.stderr,'records':len(data)},data
 except Exception as ex:return {'kp':k,'difficulty':b,'requested_template':t,'error':str(ex)},[]
out=[];records=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=4)as pool:
 for r,rs in pool.map(run,tasks):out.append(r);records.extend(rs);print(r['kp'],r['difficulty'],r['requested_template'],r.get('returncode'),r.get('error',''),r.get('stderr','')[-120:],flush=True)
(H/'template-sample-report.json').write_text(json.dumps(out,indent=2));(H/'template-samples.json').write_text(json.dumps(records,indent=2));print('template tasks',len(tasks),'successful',sum(r.get('returncode')==0 for r in out),'records',len(records))
