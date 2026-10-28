import ast,collections,hashlib,json,re,subprocess,sys,os
from pathlib import Path
H=Path(__file__).resolve().parent;root=Path('/media/jake/SSD/EDB/math');G=json.loads((H/'generators.json').read_text());report=[]
for kp,e,path in G:
 script=root/path if (root/path).exists()else Path(path).resolve();r={'kp':kp,'entity':e,'script':str(script),'exists':script.exists()}
 if script.exists():
  text=script.read_text();r['sha256']=hashlib.sha256(script.read_bytes()).hexdigest();r['helpers']=[str(p.name)for p in script.parent.glob('*.py')];r['source_loss_signals']=[]
  for pattern,reason in [(r'"\| |\'\| ','Markdown table'),(r'begin\{aligned\}','aligned environment'),(r'full matrix product','repeated operands')]:
   if re.search(pattern,text):r['source_loss_signals'].append(reason)
  out=H/'generator-help-assets'/str(kp);out.mkdir(parents=True,exist_ok=True)
  p=subprocess.run([sys.executable,str(script),'--help'],capture_output=True,text=True,timeout=40,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','COURSE_ACADEMY_GENERATOR_OUTPUT_DIR':str(out.resolve()),'MPLCONFIGDIR':str((H/'mpl-cache').resolve())});r['help']=p.stdout[:5000];r['help_exit']=p.returncode
 report.append(r)
(H/'generator-audit.json').write_text(json.dumps(report,indent=2));print(json.dumps([{'kp':r['kp'],'exists':r['exists'],'help_exit':r.get('help_exit'),'signals':r.get('source_loss_signals')}for r in report],indent=1))
