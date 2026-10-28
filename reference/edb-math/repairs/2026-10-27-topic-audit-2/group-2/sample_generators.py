import json,subprocess,sys,os,re,collections
from pathlib import Path
H=Path(__file__).resolve().parent;G=json.loads((H/'generators.json').read_text());out=[];report=[];env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','PYTHONPATH':'/tmp/course-academy-kp17592186192790-checkdeps'}
for g in G:
 info={'kp':g['kp'],'path':g['path'],'bands':[]}
 for band in ['easy','moderate','hard']:
  args=[sys.executable,g['path'],'--difficulty',band,'--count','3','--seed','271027','--format','json'];p=subprocess.run(args,capture_output=True,text=True,env=env,timeout=180)
  try:
   if p.returncode:raise ValueError(p.stderr)
   data=json.loads(p.stdout);data=data if isinstance(data,list)else[data]
   for r in data:out.append({'kp':g['kp'],'band':band,'record':r,'kind':'fresh-default'})
   info['bands'].append({'band':band,'records':len(data),'passed':True})
  except Exception as ex:info['bands'].append({'band':band,'passed':False,'error':str(ex)[-2500:]})
 report.append(info);print(g['kp'],[(b['band'],b.get('records'),b['passed'])for b in info['bands']],flush=True)
(H/'generator-samples.json').write_text(json.dumps(out,indent=2)+'\n');(H/'generator-invocations.json').write_text(json.dumps(report,indent=2)+'\n');print('records',len(out))
