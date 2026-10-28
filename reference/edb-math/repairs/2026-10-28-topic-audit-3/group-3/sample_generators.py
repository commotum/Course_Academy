import ast,concurrent.futures,json,os,re,subprocess,sys,time
from pathlib import Path
sys.path.insert(0,'scripts');from question_capture.math_format import validate_generated_record
from generator_source_policy import reject_excluded_sources
H=Path(__file__).resolve().parent;G=json.loads((H/'generator-audit.json').read_text());excluded=json.loads((H.parent/'source-eligibility.json').read_text())['excluded_questions']
def run(g,level):
 script=Path(g['script']);out=H/'generator-assets'/str(g['kp'])/level;out.mkdir(parents=True,exist_ok=True);r={'kp':g['kp'],'level':level,'script':str(script)};records=[];env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','COURSE_ACADEMY_GENERATOR_OUTPUT_DIR':str(out.resolve()),'MPLCONFIGDIR':str((H/'mpl-cache'/str(g['kp'])).resolve())};start=time.monotonic()
 try:
  p=subprocess.run([sys.executable,str(script),'--difficulty',level,'--count','2','--seed','983728','--format','json'],capture_output=True,text=True,timeout=100,env=env);r.update(exit=p.returncode,stderr=p.stderr[-1600:])
  if p.returncode==0:
   data=json.loads(p.stdout);data=data.get('instances',data)if isinstance(data,dict)else data;data=data if isinstance(data,list)else[data];r['records']=len(data);r['format_errors']=[];r['eligibility_errors']=[]
   for record in data:
    try:validate_generated_record(record)
    except Exception as ex:r['format_errors'].append(str(ex))
    try:reject_excluded_sources([record],excluded)
    except Exception as ex:r['eligibility_errors'].append(str(ex))
    records.append({'kp':g['kp'],'level':level,'record':record,'kind':'fresh-band-sample'})
  else:r['classification']='nonzero CLI result; stderr reviewed separately for unsupported source bands vs actual failures'
 except Exception as ex:r['exception']=str(ex)
 r['seconds']=round(time.monotonic()-start,2);return r,records
tasks=[]
for g in G:
 m=re.search(r'--difficulty \{([^}]+)\}',g.get('help',''));levels=m[1].split(',')if m else[]
 if not levels:
  text=Path(g['script']).read_text()
  for literal in re.findall(r'choices\s*=\s*([\[(][^\]\n)]+[\])])',text):
   try:
    v=ast.literal_eval(literal)
    if set(v)&{'easy','moderate','hard'}:levels=list(v);break
   except Exception:pass
 if not levels:levels=['easy','moderate','hard']
 tasks.extend((g,level)for level in levels if level!='all')
reports=[];samples=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=3)as pool:
 future=[pool.submit(run,g,l)for g,l in tasks]
 for completed in concurrent.futures.as_completed(future):
  r,rows=completed.result();reports.append(r);samples+=rows;print(r['kp'],r['level'],r.get('exit'),len(rows),flush=True)
  (H/'generator-validation.json').write_text(json.dumps(reports,indent=2));(H/'generator-samples.json').write_text(json.dumps(samples,indent=2))
print('packages',len(G),'invocations',len(reports),'records',len(samples))
