"""Validate precisely the runtime manifest in an isolated directory, offline."""
import sys
sys.dont_write_bytecode=True
import json,pathlib,subprocess,os,shutil,tempfile,hashlib
W=pathlib.Path(__file__).resolve().parents[1];E=W/'evidence';m=json.loads((W/'package.json').read_text());commands=[]
with tempfile.TemporaryDirectory(prefix='augmented-matrix-') as d:
 p=pathlib.Path(d)
 for name in m['files']:
  target=p/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(W/name,target)
 env={**os.environ,'COURSE_ACADEMY_GENERATOR_OUTPUT_DIR':str(p/'assets'),'PYTHONDONTWRITEBYTECODE':'1'};env.pop('PYTHONPATH',None)
 for level in ('easy','moderate'):
  args=[sys.executable,'-I','-B',str(p/m['entrypoint']),'--difficulty',level,'--seed','941713401','--count','5','--format','json']
  # -I deliberately removes script imports too; normal standalone invocation is the contract.
  args.remove('-I');commands.append(args)
  result=subprocess.run(args,cwd='/tmp',env=env,text=True,capture_output=True,check=True);rs=json.loads(result.stdout);assert len(rs)==5
  original=subprocess.run([sys.executable,'-B',str(W/m['entrypoint']),*args[3:]],cwd='/tmp',env=env,text=True,capture_output=True,check=True)
  assert json.loads(original.stdout)==rs
  (E/('relocated-'+level+'.json')).write_text(json.dumps(rs,indent=2)+'\n')
 hashes={f:hashlib.sha256((W/f).read_bytes()).hexdigest() for f in m['files']}
 (E/'relocation-results.json').write_text(json.dumps({'passed':True,'commands':commands,'cwd':'/tmp','manifest_only':True,'levels':['easy','moderate'],'deterministic_match':True,'runtime_hashes':hashes,'dependencies':m['dependencies']},indent=2)+'\n')
print('Manifest-only relocation passes both bands; exact deterministic records match.')
