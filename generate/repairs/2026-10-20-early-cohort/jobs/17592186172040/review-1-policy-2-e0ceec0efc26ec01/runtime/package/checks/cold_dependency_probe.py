"""Retained 2c2cb894f9ccd977b988: strict, cold, relocated declared-only runtime."""
import hashlib,json,os,pathlib,shutil,subprocess,sys,tempfile
W=pathlib.Path(__file__).resolve().parents[1]
E=W/'evidence';E.mkdir(exist_ok=True)
manifest=json.loads((W/'package.json').read_text())
with tempfile.TemporaryDirectory(prefix='cold-',dir=E) as td:
 t=pathlib.Path(td);pk=t/'package';out=t/'output';out.mkdir();empty=t/'empty-cache';empty.mkdir()
 for name in manifest['files']:
  p=pk/name;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(W/name,p)
 def hashes():return {str(p.relative_to(pk)):hashlib.sha256(p.read_bytes()).hexdigest() for p in pk.rglob('*') if p.is_file()}
 before=hashes();blocked=t/'no-exec';blocked.write_text('undeclared Python deliberately unavailable\n')
 env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','COURSE_ACADEMY_GENERATOR_OUTPUT_DIR':str(out)}
 isolation=['bwrap','--unshare-net','--ro-bind','/','/','--dev-bind','/dev','/dev','--tmpfs','/tmp','--bind',str(out),str(out),'--ro-bind',str(pk),str(pk),'--ro-bind',str(blocked),'/home/jake/.local/share/uv/python/cpython-3.10.13-linux-x86_64-gnu/bin/python3.10','--ro-bind',str(empty),'/home/jake/.cache/uv','--']
 cmd=isolation+[sys.executable,str(pk/manifest['entrypoint']),'--difficulty','moderate','--seed','801239','--count','1','--format','json']
 r=subprocess.run(cmd,capture_output=True,text=True,env=env)
 report={'command':cmd,'returncode':r.returncode,'stdout':r.stdout,'stderr':r.stderr,'manifest':manifest,'package_unchanged':hashes()==before}
 (E/'cold-result.json').write_text(json.dumps(report,indent=2)+'\n')
 assert r.returncode==0,r.stderr[-2000:]
 records=json.loads(r.stdout);assert len(records)==1
 images=[p for p in out.rglob('*.png')];assert len(images)>=5
 for p in images:
  assert p.read_bytes().startswith(b'\x89PNG\r\n\x1a\n')
  side=json.loads(p.with_suffix('.json').read_text());assert len(side['points'])==225
 assert before==hashes(),'Runtime package was modified'
 # Repeat the exact cold counterexample and exercise a changed empirical bank
 # through the same cold-render rule. No plots are bundled in this snapshot.
 code="import importlib.util,json; s=importlib.util.spec_from_file_location('g',"+repr(str(pk/manifest['entrypoint']))+"); g=importlib.util.module_from_spec(s);s.loader.exec_module(g);print(json.dumps(g.generate('hard',seed=91,profile='q-98229',parameters={'scale':-.5})))"
 cmd2=isolation+[sys.executable,'-c',code];r2=subprocess.run(cmd2,capture_output=True,text=True,env=env)
 report['empirical_command']=cmd2;report['empirical_returncode']=r2.returncode;report['empirical_stderr']=r2.stderr
 assert r2.returncode==0,r2.stderr[-2000:]
 report['empirical_record']=json.loads(r2.stdout);report['png_count']=len(list(out.rglob('*.png')));report['package_unchanged']=hashes()==before
 # Retain complete records and regenerated assets before disposing the snapshot.
 saved=E/'cold-assets';saved.mkdir(exist_ok=True)
 shutil.copytree(out,saved,dirs_exist_ok=True)
 def localize(v):
  if isinstance(v,str):return v.replace(str(out),str(saved))
  if isinstance(v,list):return [localize(x) for x in v]
  if isinstance(v,dict):return {k:localize(x) for k,x in v.items()}
  return v
 (E/'cold-records.json').write_text(json.dumps(localize(records+[report['empirical_record']]),indent=2)+'\n')
 (E/'cold-result.json').write_text(json.dumps(report,indent=2)+'\n')
 assert before==hashes()
 print('PASS: seed 801239 and scaled empirical rendering; old interpreter/cache unavailable; read-only relocated package unchanged')
