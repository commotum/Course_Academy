import ast,collections,json,re,subprocess,sys,time
from pathlib import Path
sys.path.insert(0,'scripts');from question_capture.math_format import validate_generated_record
H=Path(__file__).resolve().parent;G=json.loads((H/'generator-audit.json').read_text());report=[];records=[]
for g in G:
 text=Path(g['script']).read_text();m=re.search(r'--difficulty \{([^}]+)\}',g['help']);levels=m[1].split(',')if m else[]
 if not levels:
  # Policy wrappers consume --help rather than exposing the child's parser.
  matches=re.findall(r'choices\s*=\s*([\[(][^\]\n)]+[\])])',text)
  for literal in matches:
   try:
    v=ast.literal_eval(literal)
    if set(v)&{'easy','moderate','hard'}:levels=list(v);break
   except Exception:pass
 if not levels:levels=['easy','moderate','hard']
 levels=[l for l in levels if l!='all']
 for level in levels:
  start=time.monotonic();r={'kp':g['kp'],'script':g['script'],'level':level,'errors':[]}
  try:p=subprocess.run([sys.executable,g['script'],'--difficulty',level,'--count','2','--seed','912227','--format','json'],capture_output=True,text=True,timeout=100);r['exit']=p.returncode;r['stderr']=p.stderr[-2000:]
  except Exception as ex:r['exception']=str(ex);report.append(r);continue
  if not p.returncode:
   try:
    out=json.loads(p.stdout);out=out if isinstance(out,list)else[out];r['count']=len(out)
    for i,record in enumerate(out):
     try:validate_generated_record(record)
     except Exception as ex:r['errors'].append({'record':i,'error':str(ex)})
     records.append({'kp':g['kp'],'level':level,'record':record})
   except Exception as ex:r['errors'].append(str(ex));r['stdout_head']=p.stdout[:300]
  r['seconds']=round(time.monotonic()-start,2);report.append(r)
 (H/'generator-samples.json').write_text(json.dumps(records,indent=2));(H/'generator-validation.json').write_text(json.dumps(report,indent=2));print('kp',g['kp'],'levels',levels,'records',len(records),flush=True)
print('fresh samples',len(records),'issues',[(r['kp'],r['level'],r.get('exit'),r['errors'],r.get('stderr','')[-200:])for r in report if r.get('exit')or r['errors']or r.get('exception')])
