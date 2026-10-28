import json,subprocess,sys,os
from pathlib import Path
H=Path(__file__).resolve().parent;G=json.loads((H/'generator-audit.json').read_text());out=[]
for g in G:
 try:
  p=subprocess.run([sys.executable,str(H/'inspect_generator_module.py'),g['script']],capture_output=True,text=True,timeout=35);r={'kp':g['kp'],'script':g['script'],'exit':p.returncode,'stderr':p.stderr[-1200:]};r.update(json.loads(p.stdout))if p.returncode==0 else r.update(stdout=p.stdout[:300]);out.append(r)
 except Exception as ex:out.append({'kp':g['kp'],'script':g['script'],'error':str(ex)})
 (H/'generator-template-inventory.json').write_text(json.dumps(out,indent=2));print(g['kp'],r.get('version'),list(r.get('pools',{})),flush=True)
