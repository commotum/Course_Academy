"""Executable regression for the retained legacy packaging/sampling event."""
import json,os,shutil,subprocess,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
 m=json.loads((ROOT/'package.json').read_text())
 with tempfile.TemporaryDirectory(prefix='ca-relocate-') as td:
  d=Path(td)
  for f in m['files']:
   out=d/f;out.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/f,out)
  env={k:v for k,v in os.environ.items() if k not in ['PYTHONPATH','COURSE_ACADEMY_GENERATOR_OUTPUT_DIR']};env['COURSE_ACADEMY_GENERATOR_OUTPUT_DIR']=str(d/'assets');env['PYTHONDONTWRITEBYTECODE']='1'
  batches=[]
  for band in ['easy','moderate','hard']:
   cmd=[sys.executable,str(d/m['entrypoint']),'--difficulty',band,'--count','5','--seed','0','--format','json']
   a=subprocess.run(cmd,cwd=d,env=env,capture_output=True,text=True,check=True);b=subprocess.run(cmd,cwd=d,env=env,capture_output=True,text=True,check=True)
   assert a.stdout==b.stdout
   records=json.loads(a.stdout);assert len(records)==5
   for r in records:
    assert r['question'][':question/difficulty'].endswith('/'+band)
    for f in r['question'][':question/answer-fields']:
     assert f[':answer-field/correct'][1] in [a[':answer/id'] for a in f[':answer-field/choices']]
   batches.extend(records)
  assert sorted(str(p.relative_to(d)) for p in d.rglob('*') if p.is_file())==sorted(m['files']), 'Runtime wrote into package'
 report={'passed':True,'records':len(batches),'bands':['easy','moderate','hard'],'deterministic':True,'files':m['files'],'command':'python checks/package_relocation.py','legacy_failure':'Repository walk raised StopIteration outside repository; scripts import absent from runtime closure.'}
 (ROOT/'evidence/relocation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
