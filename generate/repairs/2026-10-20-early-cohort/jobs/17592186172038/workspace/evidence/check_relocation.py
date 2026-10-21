from pathlib import Path
import json,os,subprocess,sys,shutil,hashlib
W=Path(__file__).resolve().parents[1];E=W/'evidence';manifest=json.loads((W/'package.json').read_text());runs=[]
for name in ('relocated-a','deep/relocated-b'):
 root=E/name
 if root.exists():shutil.rmtree(root)
 root.mkdir(parents=True)
 for file in manifest['files']:
  dest=root/file;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(W/file,dest)
 before={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob('*') if p.is_file()}
 assets=E/(root.name+'-assets');assets.mkdir(exist_ok=True)
 cmd=[sys.executable,str(root/manifest['entrypoint']),'--difficulty','easy','--count','5','--seed','71','--format','json']
 result=subprocess.run(cmd,cwd=root,env={**os.environ,'COURSE_ACADEMY_GENERATOR_OUTPUT_DIR':str(assets),'PYTHONPATH':''},text=True,capture_output=True,check=True)
 records=json.loads(result.stdout);assert len(records)==5
 for r in records:
  for c in r['question'][':question/answer-fields'][0][':answer-field/choices']:
   value=c[':answer/value'];assert Path(value).name==value and (assets/value).is_file()
 after={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob('*') if p.is_file()};assert before==after
 (E/(root.name+'-records.json')).write_text(json.dumps(records,indent=2)+'\n');runs.append({'command':cmd,'package_root':str(root.relative_to(W)),'asset_root':str(assets.relative_to(W)),'records':5,'closure_unchanged':True,'records_data':records})
assert runs[0].pop('records_data')==runs[1].pop('records_data')
(E/'relocation.json').write_text(json.dumps({'passed':True,'manifest_files':len(manifest['files']),'runs':runs,'identical_across_roots':True,'hard_coded_runtime_paths':False},indent=2)+'\n');print('Relocation: two package roots, 5 records each, deterministic records, no package writes')
