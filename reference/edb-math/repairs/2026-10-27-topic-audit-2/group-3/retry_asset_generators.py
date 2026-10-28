import json,os,subprocess,sys,time
from pathlib import Path
sys.path.insert(0,'scripts');from question_capture.math_format import validate_generated_record
H=Path(__file__).resolve().parent;report=json.loads((H/'generator-validation.json').read_text());records=json.loads((H/'generator-samples.json').read_text())
for r in report:
 if r.get('exit')and 'OUTPUT_DIR'in r.get('stderr',''):
  folder=H/'generator-assets'/str(r['kp'])/r['level'];folder.mkdir(parents=True,exist_ok=True);env=dict(os.environ,COURSE_ACADEMY_GENERATOR_OUTPUT_DIR=str(folder.resolve()),MPLCONFIGDIR=str((folder/'mpl-config').resolve()));p=subprocess.run([sys.executable,r['script'],'--difficulty',r['level'],'--count','2','--seed','912227','--format','json'],capture_output=True,text=True,env=env,timeout=90);r['prior_protocol_failure']=r['stderr'];r.update(exit=p.returncode,stderr=p.stderr[-1800:],errors=[])
  if p.returncode==0:
   out=json.loads(p.stdout);r['count']=len(out);r['asset_directory']=str(folder)
   for i,record in enumerate(out):
    try:validate_generated_record(record)
    except Exception as ex:r['errors'].append({'record':i,'error':str(ex)})
    records.append({'kp':r['kp'],'level':r['level'],'record':record})
 if r.get('exit')and any(s in r.get('stderr','').lower()for s in ['unsupported','unknown difficulty','no source','only source-justified']):r['classification']='advertised band lacks supported source workload; not a generator failure'
(H/'generator-validation.json').write_text(json.dumps(report,indent=2));(H/'generator-samples.json').write_text(json.dumps(records,indent=2));print('fresh samples',len(records),'remaining execution failures',[(r['kp'],r['level'],r.get('classification'),r.get('stderr','')[-100:])for r in report if r.get('exit')])
