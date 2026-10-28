import concurrent.futures,copy,json,os,re,shutil,subprocess,sys,tempfile,time
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'))
from question_capture.math_format import validate_generated_record
from generator_source_policy import reject_excluded_sources
cfg=json.loads((H/'generator-stage-config.json').read_text());original=json.loads((H/'generator-sample-report.json').read_text());bands={s['kp']:[r['difficulty']for r in original if r['kp']==s['kp']and r.get('returncode')==0]for s in cfg};ledger=json.loads((H.parent/'source-eligibility.json').read_text())['excluded_questions'];outside=Path(tempfile.mkdtemp(prefix='ca-topic3-g1-portable-'));env=dict(os.environ);env.pop('PYTHONPATH',None);env.pop('_CA_SOURCE_POLICY_CHILD',None);env['PYTHONDONTWRITEBYTECODE']='1';reports=[];records=[]
def test(spec):
 work=outside/str(spec['kp']);work.mkdir();src=Path(spec['directory'])
 for f in spec['files']:target=work/f;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src/f,target)
 out=[];rr=[]
 for band in bands[spec['kp']]:
  args=[str(R/'.venv/bin/python'),str(work/spec['entrypoint']),'--difficulty',band,'--count','3','--seed','28109837','--format','json'];start=time.monotonic()
  result=subprocess.run(args,cwd=outside,env={**env,'COURSE_ACADEMY_GENERATOR_OUTPUT_DIR':str(outside/'assets-a'/str(spec['kp'])/band)},text=True,capture_output=True,timeout=120)
  report={'kp':spec['kp'],'band':band,'command':args,'cwd':str(outside),'returncode':result.returncode,'stderr':result.stderr,'seconds':time.monotonic()-start,'validation_errors':[],'records':0}
  if result.returncode==0:
   value=json.loads(result.stdout);rs=value.get('records',value.get('instances',[]))if isinstance(value,dict)else value;report['records']=len(rs)
   for rec in rs:
    try:validate_generated_record(rec);reject_excluded_sources([rec],ledger)
    except Exception as ex:report['validation_errors'].append({'question':rec['question'][':question/id'],'error':str(ex)})
   rr.extend(rs)
  out.append(report)
 return out,rr
with concurrent.futures.ThreadPoolExecutor(max_workers=3)as pool:
 for out,rs in pool.map(test,cfg):
  reports.extend(out);records.extend(rs);(H/'generator-stage-test.json').write_text(json.dumps(reports,indent=2)+'\n');(H/'generator-stage-samples.json').write_text(json.dumps(records,indent=2)+'\n');print([(r['kp'],r['band'],r['returncode'],r['records'],r['validation_errors'],r['stderr'][-180:])for r in out],flush=True)
print('outside',outside,'records',len(records),'failures',sum(r['returncode']!=0 or bool(r['validation_errors'])for r in reports))
