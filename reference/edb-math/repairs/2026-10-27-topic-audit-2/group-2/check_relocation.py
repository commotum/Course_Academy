import json,subprocess,sys,os,shutil,hashlib
from pathlib import Path
H=Path(__file__).resolve().parent;G=json.loads((H/'generators.json').read_text());candidate={c['kp']:c for c in json.loads((H/'generator-candidates.json').read_text())};out=[]
for g in G:
 kp=g['kp'];entry=Path(g['path']);base=entry.parent
 if kp in candidate:base=Path(candidate[kp]['directory']);entry=base/candidate[kp]['entrypoint']
 manifest=json.loads((base/'generator-package.json').read_text());dest=H/'relocation-check'/str(kp);dest.mkdir(parents=True,exist_ok=True)
 for name in manifest['files']:
  to=dest/name;to.parent.mkdir(parents=True,exist_ok=True)
  if to.exists():to.chmod(0o644)
  shutil.copyfile(base/name,to)
 outputs=[];created=[]
 for directory,script in[(base,entry),(dest,dest/entry.name)]:
  output=H/'relocation-check'/('output-'+str(kp)+'-'+str(len(outputs)));output.mkdir(parents=True,exist_ok=True);env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','PYTHONPATH':'/tmp/course-academy-kp17592186192790-checkdeps','COURSE_ACADEMY_GENERATOR_OUTPUT_DIR':str(output.resolve()),'COURSE_ACADEMY_REPO_ROOT':str(H.parents[4])};args=[sys.executable,str(script.resolve()),'--difficulty','easy','--count','1','--seed','271029','--format','json'];p=subprocess.run(args,cwd=directory,capture_output=True,text=True,env=env,timeout=180,check=True);r=json.loads(p.stdout);outputs.append(r);created.append([str(p.relative_to(output))for p in output.rglob('*')if p.is_file()])
 a=outputs[0]if isinstance(outputs[0],list)else[outputs[0]];b=outputs[1]if isinstance(outputs[1],list)else[outputs[1]];same=[r['question']for r in a]==[r['question']for r in b];assert same,kp;assert not any(r.get('assets')for r in a+b)
 out.append({'kp':kp,'passed':True,'question_and_all_field_answer_UUIDs_identical':same,'full_output_identical':outputs[0]==outputs[1],'output_dir_artifacts':created,'asset_payloads_empty':True});print(kp,'passed',flush=True)
(H/'generator-relocation-verification.json').write_text(json.dumps(out,indent=2)+'\n')
