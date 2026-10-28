import json,subprocess,os,sys,hashlib
from pathlib import Path
H=Path(__file__).resolve().parent;G=json.loads((H/'generators.json').read_text());info=json.loads((H/'generator-full-invocations.json').read_text());env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','PYTHONPATH':'/tmp/course-academy-kp17592186192790-checkdeps'};samples=[];report=[]
for kp in[17592186064245,17592186192794,17592186124639]:
 g=next(g for g in G if g['kp']==kp);entry=H/'generators'/str(kp)/Path(g['path']).name;jobs=[j for i in info if i['kp']==kp for j in i['invocations']if j.get('passed')or(not j['args']and j['band']=='moderate')]
 for j in jobs:
  count=j.get('records',16 if kp==17592186192794 else 12);args=[sys.executable,str(entry),'--difficulty',j['band'],'--count',str(count),'--seed','271028','--format','json',*j['args']]
  p=subprocess.run(args,capture_output=True,text=True,env=env,timeout=180,check=True);records=json.loads(p.stdout)
  if not j['args']and j['band']=='moderate':
   again=subprocess.run(args,capture_output=True,text=True,env=env,timeout=180,check=True);assert again.stdout==p.stdout
  for r in records:samples.append({'kp':kp,'band':j['band'],'record':r,'kind':'staged-successor','arguments':j['args']})
  report.append({'kp':kp,'band':j['band'],'args':j['args'],'count':count,'passed':True,'retry':records[0]['generation'].get('batch_retry',0)});print(kp,j['band'],count,flush=True)
(H/'successor-samples.json').write_text(json.dumps(samples,indent=2)+'\n');(H/'successor-verification.json').write_text(json.dumps(report,indent=2)+'\n');print('samples',len(samples))
