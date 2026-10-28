import json,re,subprocess,sys
from pathlib import Path
sys.path.insert(0,'scripts');from question_capture.math_format import validate_generated_record
H=Path(__file__).resolve().parent;G=json.loads((H/'generator-audit.json').read_text());report=[];allrecords=[]
for r in G:
 levels=re.search(r'--difficulty \{([^}]+)\}',r['help']);levels=levels[1].split(',') if levels else ['easy'];levels=[l for l in levels if l!='all'];
 if r['kp']==17592186184172:levels=['moderate','hard']
 if r['kp']==17592186100913:levels=['easy']
 for level in levels:
  p=subprocess.run([sys.executable,r['script'],'--difficulty',level,'--count','3','--seed','20261027','--format','json'],capture_output=True,text=True);item={'kp':r['kp'],'level':level,'exit':p.returncode,'errors':[]}
  if not p.returncode:
   try:
    data=json.loads(p.stdout);data=data if isinstance(data,list)else[data];item['count']=len(data)
    for n,record in enumerate(data):
     try:validate_generated_record(record)
     except Exception as ex:item['errors'].append({'record':n,'error':str(ex)})
     allrecords.append({'kp':r['kp'],'level':level,'record':record})
   except Exception as ex:item['errors'].append(str(ex))
  else:item['stderr']=p.stderr[-1500:]
  report.append(item)
(H/'generator-samples.json').write_text(json.dumps(allrecords,indent=2));(H/'generator-validation.json').write_text(json.dumps(report,indent=2));print('samples',len(allrecords),'errors',[r for r in report if r['exit']or r['errors']])
