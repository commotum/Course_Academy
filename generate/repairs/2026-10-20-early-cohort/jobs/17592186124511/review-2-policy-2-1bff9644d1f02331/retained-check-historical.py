"""The original failure must not recur when only manifest files are relocated."""
import json, os
from pathlib import Path
import shutil, subprocess, sys, tempfile
ROOT=Path('/home/jake/Developer/Course_Academy/generate/repairs/2026-10-20-early-cohort/jobs/17592186124511/review-2-policy-2-1bff9644d1f02331/legacy-failing')
def main():
 manifest=json.loads((ROOT/'package.json').read_text())
 with tempfile.TemporaryDirectory(prefix='imt-relocation-', dir='/home/jake/Developer/Course_Academy/generate/repairs/2026-10-20-early-cohort/jobs/17592186124511/review-2-policy-2-1bff9644d1f02331/tmp') as d:
  target=Path(d)
  for rel in manifest['files']:
   p=Path(rel);assert not p.is_absolute() and '..' not in p.parts
   (target/p).parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/p,target/p)
  env={**os.environ,'PYTHONPATH':'','COURSE_ACADEMY_GENERATOR_OUTPUT_DIR':str(target/'assets')}
  cmd=[sys.executable,'-I',str(target/manifest['entrypoint']),'--difficulty','moderate','--count','5','--seed','0','--format','json']
  # -I also removes the script directory, so explicitly use runpy with only this package added.
  cmd=[sys.executable,'-I','-c',"from pathlib import Path;original_is_file=Path.is_file;Path.is_file=lambda p: False if str(p).endswith('scripts/generator_policy.py') else original_is_file(p);import runpy,sys;sys.path.insert(0,sys.argv.pop(1));runpy.run_path(sys.argv.pop(1),run_name='__main__')",str(target),str(target/manifest['entrypoint']),*cmd[3:]]
  r=subprocess.run(cmd,cwd=target,env=env,text=True,capture_output=True)
  assert r.returncode==0,r.stderr
  records=json.loads(r.stdout);assert len(records)==5
  for rec in records:
   q=rec['question'];assert q[':question/answer-fields'] and q[':question/worked-solution']
   assert rec['knowledge_point']['db_id']==17592186124511
  report={'passed':True,'isolated_runtime_files':manifest['files'],'command':cmd[:3]+['<isolated runpy bootstrap>','<temporary package>','17592186124511.py','--difficulty','moderate','--count','5','--seed','0','--format','json'],'count':len(records),'runtime_writes':[str(p.relative_to(target)) for p in target.rglob('*') if p.is_file() and str(p.relative_to(target)) not in manifest['files']]}
  (Path('/home/jake/Developer/Course_Academy/generate/repairs/2026-10-20-early-cohort/jobs/17592186124511/review-2-policy-2-1bff9644d1f02331/retained-runtime-results.json')).write_text(json.dumps(report,indent=2)+'\n')
 print('Relocation passed: 5 complete records from the declared runtime files.')
if __name__=='__main__':main()
