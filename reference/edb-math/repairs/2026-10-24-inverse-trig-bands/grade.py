"""Build the existing native grade_field harness against the current engine."""
import hashlib
import json
from pathlib import Path
import subprocess

H = Path(__file__).resolve().parent;ROOT = H.parents[3]


def main():
    deps = ROOT/'target/release/deps';source = ROOT/'generate/runs/current/check-engine.rs'
    libs = {name:max(deps.glob('lib'+name+'-*.rlib'),key=lambda p:p.stat().st_mtime_ns) for name in ('course_academy_engine','serde_json')}
    # Reuse existing up-to-date release libraries; never replace the service.
    output = Path('/tmp/inverse-trig-check-engine')
    command = ['rustc','--edition=2024','-O',str(source)]
    for name,path in libs.items():command += ['--extern',name+'='+str(path)]
    command += ['-L','dependency='+str(deps),'-o',str(output)]
    subprocess.run(command,check=True)
    subprocess.run([str(output),str(H/'grader-input.json'),str(H/'grader-verification.json')],check=True)
    report = json.loads((H/'grader-verification.json').read_text());assert report['documented_unresolved_checks'] == 0
    (H/'grader-build.json').write_text(json.dumps({'command':command,'binary':str(output),
        'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
        'input_sha256':hashlib.sha256((H/'grader-input.json').read_bytes()).hexdigest(),
        'libraries':{name:{'path':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()} for name,path in libs.items()}},indent=2)+'\n')


if __name__ == '__main__':main()
