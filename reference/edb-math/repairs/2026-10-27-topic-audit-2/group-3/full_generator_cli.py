import json,os,re,subprocess,sys,time
from pathlib import Path
sys.path.insert(0,'scripts');from question_capture.math_format import validate_generated_record
H=Path(__file__).resolve().parent;G=json.loads((H/'generator-audit.json').read_text());I={x['kp']:x for x in json.loads((H/'generator-template-inventory.json').read_text())};old=json.loads((H/'generator-validation.json').read_text());stages={x['kp']:x for x in json.loads((H/'generator-candidates.json').read_text())};records=[];calls=[]
for g in G:
 kp=g['kp'];script=Path(stages[kp]['directory'])/stages[kp]['entrypoint']if kp in stages else Path(g['script']);helptext=g['help'];levels=sorted({x['level']for x in old if x['kp']==kp and x.get('exit')==0});templates=I[kp].get('pools',{}).get('TEMPLATES',[])
 inv=[]
 if '--template'in helptext:
  for t in templates:
   for level in ([t['level']]if t['level']in levels else levels):inv.append((level,['--template',t['name']],'fresh-template'))
 for flag in ['--replay','--profile']:
  m=re.search(re.escape(flag)+r' \{([^}]+)\}',helptext)
  if m:
   for val in m[1].split(','):
    if flag=='--profile'and not val.startswith(('q-','e-')):continue
    inv.append((levels[0]if levels else'easy',[flag,val],'source-replay'))
 if '--replay-source]'in helptext:inv.append((levels[0],['--replay-source'],'source-replay'))
 # Raw evidence profiles available via documented profile API.
 if kp in [17592186092260,17592186092261,17592186064171]:
  pool='CASES'if kp==17592186092260 else'SOURCES'
  for r in I[kp].get('pools',{}).get(pool,[]):
   if r['name'].startswith(('q-','e-')):inv.append((r['level']or levels[0],['--profile','raw:'+r['name']],'raw-source-evidence'))
 for level,args,kind in inv:
  root=H/'generator-assets'/str(kp)/'full';root.mkdir(parents=True,exist_ok=True);env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','COURSE_ACADEMY_GENERATOR_OUTPUT_DIR':str(root.resolve()),'MPLCONFIGDIR':str((H/'mpl-cache').resolve())};call={'kp':kp,'level':level,'args':args,'kind':kind,'staged':kp in stages}
  try:
   p=subprocess.run([sys.executable,str(script),'--difficulty',level,'--count','1','--seed','912229','--format','json',*args],env=env,capture_output=True,text=True,timeout=70);call['exit']=p.returncode;call['stderr']=p.stderr[-900:]
   if p.returncode==0:
    out=json.loads(p.stdout);out=out if isinstance(out,list)else[out];call['records']=len(out);call['format_errors']=[]
    for record in out:
     try:validate_generated_record(record)
     except Exception as ex:call['format_errors'].append(str(ex))
     records.append({'kp':kp,'level':level,'kind':kind,'arguments':args,'record':record})
   else:call['classification']='unsupported template/band or source-policy exclusion; review stderr individually'
  except Exception as ex:call['exception']=str(ex)
  calls.append(call)
 (H/'generator-full-samples.json').write_text(json.dumps(records,indent=2));(H/'generator-full-invocations.json').write_text(json.dumps(calls,indent=2));print(kp,'calls',len(inv),'samples',len(records),flush=True)
print('full-template/replay records',len(records),'calls',len(calls))
