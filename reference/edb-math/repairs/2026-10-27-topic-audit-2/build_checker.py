import hashlib,json,subprocess
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];source=R/'reference/edb-math/repairs/2026-10-24-percent-escaping/check-engine.rs';libs=list((R/'target/release/deps').glob('libserde_json-*.rlib'));assert len(libs)==1,libs
subprocess.run(['cargo','build','--offline','--release','--lib'],cwd=R,check=True)
subprocess.run(['rustc','--edition=2024',str(source),'-L','dependency='+str(R/'target/release/deps'),'--extern','course_academy_engine='+str(R/'target/release/libcourse_academy_engine.rlib'),'--extern','serde_json='+str(libs[0]),'-O','-o',str(H/'check-engine')],check=True)
report={'binary':str((H/'check-engine').resolve()),'engine_library_sha256':hashlib.sha256((R/'target/release/libcourse_academy_engine.rlib').read_bytes()).hexdigest(),'fixture_source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'old_checker_path':'.local/edb/html-table-repair/check-engine','old_checker_stale':True,'database_writes':0};(H/'checker-build.json').write_text(json.dumps(report,indent=2)+'\n');print(report)
