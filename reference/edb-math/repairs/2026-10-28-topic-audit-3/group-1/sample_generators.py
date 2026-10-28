"""Exercise actual registered entrypoints with cwd outside repository ancestry."""
import concurrent.futures,json,os,subprocess,tempfile,time
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4];inventory=json.loads((H/'generator-inventory.json').read_text())
cwd=Path(tempfile.mkdtemp(prefix='ca-audit3-generators-'));env=dict(os.environ);env.pop('PYTHONPATH',None);env.pop('_CA_SOURCE_POLICY_CHILD',None);env['PYTHONDONTWRITEBYTECODE']='1'
def run(task):
    spec,band=task;start=time.monotonic();assets=H/'generated-assets'/str(spec['kp'])/band;assets.mkdir(parents=True,exist_ok=True)
    command=[str(R/'.venv/bin/python'),spec['path'],'--difficulty',band,'--count','3','--seed','28109837','--format','json']
    try:
        result=subprocess.run(command,cwd=cwd,env={**env,'COURSE_ACADEMY_GENERATOR_OUTPUT_DIR':str(assets)},text=True,capture_output=True,timeout=100)
        value=json.loads(result.stdout)if result.returncode==0 else[];records=value.get('records',value.get('instances',[]))if isinstance(value,dict)else value
        return {'kp':spec['kp'],'reference':spec['reference'],'difficulty':band,'returncode':result.returncode,'stderr':result.stderr,'records':len(records),'duration':time.monotonic()-start,'cwd':str(cwd),'packaged_outside_repository':bool(spec['manifest'])},records
    except Exception as ex:return {'kp':spec['kp'],'reference':spec['reference'],'difficulty':band,'error':str(ex),'duration':time.monotonic()-start},[]
reports=[];records=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=4)as pool:
    for report,rs in pool.map(run,[(s,b)for s in inventory for b in['easy','moderate','hard']]):
        reports.append(report);records.extend(rs);print(report['kp'],report['difficulty'],report.get('returncode'),report.get('records'),report.get('stderr','')[-120:],report.get('error',''),flush=True)
        (H/'generator-sample-report.json').write_text(json.dumps(reports,indent=2));(H/'generator-samples.json').write_text(json.dumps(records,indent=2))
print('Completed',len(reports),'band requests;',len(records),'fresh records')
