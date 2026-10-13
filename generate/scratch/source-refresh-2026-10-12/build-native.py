"""Build a local read-only native grader against the existing application library."""
import argparse,hashlib,json,subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--target-dir',type=Path,default=ROOT/'target',help='Existing Cargo target directory to link; no engine rebuild is performed')
args=parser.parse_args();deps=args.target_dir.resolve()/'debug/deps'
lib=max(deps.glob('libcourse_academy_engine*.rlib'),key=lambda p:p.stat().st_mtime_ns)
serde=max(deps.glob('libserde_json*.rlib'),key=lambda p:p.stat().st_mtime_ns)
source=HERE/'check-checkbox-engine.rs';binary=HERE/'check-checkbox-engine'
command=['rustc','--edition=2024','-O',str(source),'-L','dependency='+str(deps),'--extern','course_academy_engine='+str(lib),'--extern','serde_json='+str(serde),'-o',str(binary)]
subprocess.run(command,check=True)
report={'database_writes':0,'rustc':subprocess.check_output(['rustc','--version'],text=True).strip(),'command':command,'source_sha256':digest(source),'binary_sha256':digest(binary),'application_library':{'path':str(lib),'sha256':digest(lib)},'serde_json_library':{'path':str(serde),'sha256':digest(serde)},'entry_points':['course_academy_engine::learning::grade_field','course_academy_engine::learning::grade'],'note':'Uses the existing application library; does not modify or rebuild engine source.'}
(HERE/'native-build.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'built':True,'database_writes':0,'binary_sha256':report['binary_sha256']}))
