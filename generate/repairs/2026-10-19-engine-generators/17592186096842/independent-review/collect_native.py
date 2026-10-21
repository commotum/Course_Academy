from pathlib import Path
import subprocess,json,re,hashlib
repo=Path('/home/jake/Developer/Course_Academy');orig=repo/'generate/runs/current/check-engine.rs';src=orig.read_text()
old='if outcome!=expected{return Err(format!("{} field {}: {:?} expected {}, got {} ({:?})",item["label"],i,submitted,expected,outcome,result).into())}'
assert old in src
src=src.replace(old,'// Review-only change: retain every native outcome instead of aborting at the first mismatch.')
src=src.replace('"outcome":outcome,"reason":result.err()', '"outcome":outcome,"expected":expected,"matched":outcome==expected,"reason":result.err()')
Path('check-engine-collect.rs').write_text(src)
deps=repo/'target/debug/deps';libs=sorted(deps.glob('libcourse_academy_engine*.rlib'),key=lambda p:p.stat().st_mtime,reverse=True)
serde=next(deps.glob('libserde_json*.rlib'))
cmd=['rustc','--edition=2024','--crate-name','review_native','check-engine-collect.rs','-o','check-engine-collect','-L','dependency='+str(deps),'--extern','course_academy_engine='+str(libs[0]),'--extern','serde_json='+str(serde)]
p=subprocess.run(cmd,capture_output=True,text=True);Path('native-compile.log').write_text(p.stdout+p.stderr)
Path('native-harness-provenance.json').write_text(json.dumps({'original_source':str(orig),'sha256':hashlib.sha256(orig.read_bytes()).hexdigest(),'change':'Only replace first-mismatch abort with continued collection; log expected/matched. Every outcome is still computed by course_academy_engine::learning::grade_field.','compile_command':cmd,'exit_code':p.returncode},indent=2))
print('compile exit',p.returncode)
if p.returncode==0:
 p=subprocess.run(['./check-engine-collect','grader-input.json','grader-results.json'],capture_output=True,text=True);Path('grader-collect.stdout').write_text(p.stdout);Path('grader-collect.stderr').write_text(p.stderr);print(p.stdout,p.stderr)
