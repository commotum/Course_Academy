"""Execute the actual published entrypoints; no questions are transacted."""
import concurrent.futures,json,os,subprocess,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];sys.path[:0]=[str(R),str(R/'scripts/question_capture')]
from math_format import validate_generated_record
from scripts.generator_source_policy import reject_excluded_sources
D=H/'published-probe';D.mkdir(exist_ok=True);pubs={p['kp']:p for g in range(1,4)for p in json.loads((H/f'commit-group-{g}'/'generator-publications.json').read_text())}
if(H/'corrective-generators/generator-publications.json').exists():pubs.update({p['kp']:p for p in json.loads((H/'corrective-generators/generator-publications.json').read_text())})
excluded=json.loads((H/'source-eligibility.json').read_text())['excluded_questions']
prior={c['kp']:c for c in json.loads((D/'verification.json').read_text()).get('checks',[])}if(D/'verification.json').exists()else{}
def run(p):
 script=Path('/media/jake/SSD/EDB/math')/p['new_reference'];out=D/str(p['kp']);out.mkdir(exist_ok=True)
 env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','COURSE_ACADEMY_GENERATOR_OUTPUT_DIR':str(out.resolve())}
 band='easy'if p['kp']in [17592186096617,17592186096618]else'moderate'
 cached=prior.get(p['kp'],{}).get('passed')and prior[p['kp']]['reference']==p['new_reference']and(out/'stdout.json').exists()
 if cached:value=json.loads((out/'stdout.json').read_text())
 else:
  proc=subprocess.run([sys.executable,str(script),'--difficulty',band,'--count','1','--seed','27102791','--format','json'],capture_output=True,text=True,env=env,timeout=100)
  (out/'stdout.json').write_text(proc.stdout);(out/'stderr.txt').write_text(proc.stderr)
  if proc.returncode:return {'kp':p['kp'],'reference':p['new_reference'],'band':band,'passed':False,'stderr':proc.stderr},[]
  value=json.loads(proc.stdout)
 records=value.get('records',[])if isinstance(value,dict)else value
 assert len(records)==1
 for record in records:validate_generated_record(record)
 reject_excluded_sources(records,excluded)
 return {'kp':p['kp'],'reference':p['new_reference'],'band':band,'passed':True,'records':len(records)},records
reports=[];records=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=4)as pool:
 for report,rs in pool.map(run,pubs.values()):reports.append(report);records.extend(rs)
passed=all(p['passed']for p in reports)
(D/'records.json').write_text(json.dumps(records,indent=2)+'\n');(D/'verification.json').write_text(json.dumps({'passed':passed,'actual_published_entrypoints':len(reports),'checks':reports,'source_eligibility_hits':0,'database_writes':0},indent=2)+'\n');print('Published entrypoint probes:',len(reports),'failures:',[r['kp']for r in reports if not r['passed']]);assert passed
