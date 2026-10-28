import json,subprocess,sys,os
from pathlib import Path
H=Path(__file__).resolve().parent;G=json.loads((H/'generators.json').read_text());env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','PYTHONPATH':'/tmp/course-academy-kp17592186192790-checkdeps'};out=[]
for kp,band in[(17592186217248,'easy'),(17592186217249,'hard')]:
 path=next(g['path']for g in G if g['kp']==kp);p=subprocess.run([sys.executable,path,'--difficulty',band,'--count','8','--seed','271028','--format','json'],capture_output=True,text=True,check=True,env=env,timeout=180)
 for r in json.loads(p.stdout):out.append({'kp':kp,'band':band,'record':r,'kind':'full-finite-supported-band'})
(H/'finite-band-samples.json').write_text(json.dumps(out,indent=2)+'\n');print(len(out));print(out[-1]['record']['question'][':question/problem'][:500]);print(out[-1]['record']['question'][':question/answer-fields'])
