import json,os,subprocess,sys
from pathlib import Path
H=Path(__file__).resolve().parent;G=json.loads((H/'generator-audit.json').read_text());stages={r['kp']:r for r in json.loads((H/'generator-candidates.json').read_text())};out=[];calls=[]
for g in G:
 kp=g['kp'];p=Path(stages[kp]['directory'])/stages[kp]['entrypoint']if kp in stages else Path(g['script']);root=H/'generator-assets'/str(kp)/'api';root.mkdir(parents=True,exist_ok=True);env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','COURSE_ACADEMY_GENERATOR_OUTPUT_DIR':str(root.resolve()),'MPLCONFIGDIR':str((H/'mpl-cache').resolve())}
 try:
  r=subprocess.run([sys.executable,str(H/'generator_api_worker.py'),str(p)],capture_output=True,text=True,env=env,timeout=180);data=json.loads(r.stdout);out.extend({'kp':kp,**x}for x in data['records']);calls.extend({'kp':kp,**x}for x in data['calls']);print(kp,'samples',len(data['records']),flush=True)
 except Exception as ex:calls.append({'kp':kp,'worker_error':str(ex),'stderr':r.stderr[-1200:]if'r'in locals()else''});print('workererror',kp,str(ex),flush=True)
 (H/'generator-api-samples.json').write_text(json.dumps(out,indent=2));(H/'generator-api-invocations.json').write_text(json.dumps(calls,indent=2))
