import json,subprocess,sys,os,shutil,concurrent.futures,collections
from pathlib import Path
H=Path(__file__).resolve().parent;G=json.loads((H/'generators.json').read_text());env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','MPLBACKEND':'Agg','COURSE_ACADEMY_REPO_ROOT':str(H.parents[4])}
def worker(g):
 out=[];report=[];old=Path(g['path'])
 for band in ['easy','moderate','hard']:
  directory=H/'generator-runtime'/str(g['kp'])/band;directory.mkdir(parents=True,exist_ok=True)
  for name in g['files']:
   if name=='generator-package.json':continue
   target=directory/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(old.parent/name,target)
  output=directory/'output';output.mkdir(exist_ok=True);args=[sys.executable,'-E','-s','-B',str((directory/old.name).resolve()),'--difficulty',band,'--count','3','--seed','9837','--format','json']
  try:
   p=subprocess.run(args,cwd=directory,capture_output=True,text=True,env={**env,'COURSE_ACADEMY_GENERATOR_OUTPUT_DIR':str(output.resolve())},timeout=180);(directory/'run.stderr').write_text(p.stderr)
   if p.returncode:raise ValueError(p.stderr[-2000:])
   data=json.loads(p.stdout);data=data if isinstance(data,list)else[data]
   for r in data:out.append({'kp':g['kp'],'band':band,'record':r,'kind':'fresh-default','runtime':str(directory.resolve()),'output':str(output.resolve())})
   report.append({'band':band,'passed':True,'records':len(data)})
  except Exception as ex:report.append({'band':band,'passed':False,'error':str(ex)})
 return out,{'kp':g['kp'],'path':g['path'],'bands':report}
out=[];report=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=6)as pool:
 futures={pool.submit(worker,g):g for g in G}
 for f in concurrent.futures.as_completed(futures):
  records,info=f.result();out.extend(records);report.append(info);print(info['kp'],[(b['band'],b.get('records'),b['passed'])for b in info['bands']],flush=True);(H/'generator-samples.json').write_text(json.dumps(out,indent=2)+'\n');(H/'generator-invocations.json').write_text(json.dumps(report,indent=2)+'\n')
print('records',len(out),'generators',len(report))
