"""Execute the actual published entrypoints; no questions are transacted."""
import concurrent.futures,json,os,subprocess,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];sys.path[:0]=[str(R),str(R/'scripts/question_capture')]
from math_format import validate_generated_record
from scripts.generator_source_policy import reject_excluded_sources
D=H/'published-probe';D.mkdir(exist_ok=True);pubs=[p for g in range(1,4)for p in json.loads((H/f'commit-group-{g}'/'generator-publications.json').read_text())]
excluded=json.loads((H/'source-eligibility.json').read_text())['excluded_questions']
def run(p):
 script=Path('/media/jake/SSD/EDB/math')/p['new_reference'];out=D/str(p['kp']);out.mkdir(exist_ok=True)
 env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','COURSE_ACADEMY_GENERATOR_OUTPUT_DIR':str(out.resolve())}
 proc=subprocess.run([sys.executable,str(script),'--difficulty','moderate','--count','1','--seed','27102791','--format','json'],capture_output=True,text=True,env=env,timeout=100)
 (out/'stdout.json').write_text(proc.stdout);(out/'stderr.txt').write_text(proc.stderr);proc.check_returncode();value=json.loads(proc.stdout);records=value.get('records',[])if isinstance(value,dict)else value
 assert len(records)==1
 for record in records:validate_generated_record(record)
 reject_excluded_sources(records,excluded)
 return {'kp':p['kp'],'reference':p['new_reference'],'passed':True,'records':len(records)},records
reports=[];records=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=4)as pool:
 for report,rs in pool.map(run,pubs):reports.append(report);records.extend(rs)
(D/'records.json').write_text(json.dumps(records,indent=2)+'\n');(D/'verification.json').write_text(json.dumps({'passed':True,'actual_published_entrypoints':len(reports),'checks':reports,'source_eligibility_hits':0,'database_writes':0},indent=2)+'\n');print('Published entrypoint probes passed:',len(reports))
