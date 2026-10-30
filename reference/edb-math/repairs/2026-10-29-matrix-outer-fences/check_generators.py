"""Probe actual affected immutable entrypoints; never publishes records."""
import concurrent.futures,json,os,subprocess,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];sys.path.insert(0,str(R/'scripts'));from generator_publish import validate_question
items=json.loads((H/'affected-generators.json').read_text());D=H/'generator-probes';D.mkdir(exist_ok=True)
def run(pair):
 g,band=pair;script=Path('/media/jake/SSD/EDB/math')/g['reference'];d=D/(str(g['kp'])+'-'+band);d.mkdir(exist_ok=True);env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','COURSE_ACADEMY_GENERATOR_OUTPUT_DIR':str(d.resolve()),'TMPDIR':str(d.resolve())};p=subprocess.run([sys.executable,str(script),'--difficulty',band,'--count','3','--seed','29102977','--format','json'],env=env,capture_output=True,text=True,timeout=100);(d/'stdout.json').write_text(p.stdout);(d/'stderr.txt').write_text(p.stderr)
 result={'kp':g['kp'],'reference':g['reference'],'band':band,'returncode':p.returncode,'errors':[]}
 if p.returncode:result['errors'].append(p.stderr);return result
 raw=json.loads(p.stdout);rs=raw.get('records',[])if isinstance(raw,dict)else raw;result['records']=len(rs)
 for i,record in enumerate(rs):
  try:validate_question(record['question'])
  except Exception as e:result['errors'].append({'record':i,'error':str(e)})
 return result
with concurrent.futures.ThreadPoolExecutor(max_workers=4)as pool:results=list(pool.map(run,[(g,b)for g in items for b in ['easy','moderate','hard']]))
report={'passed':all(not r['errors']for r in results),'generators':len(items),'invocations':len(results),'records':sum(r.get('records',0)for r in results),'checks':results,'database_writes':0};(H/'generator-verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2));assert report['passed']
