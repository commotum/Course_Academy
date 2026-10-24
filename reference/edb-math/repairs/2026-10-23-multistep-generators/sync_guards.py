"""Refresh staged helpers and hashes without reinstrumenting retained originals."""
import hashlib
import json
from pathlib import Path
import shutil
import sys
H=Path(__file__).resolve().parent;ROOT=H.parents[3]
sys.path.insert(0,str(ROOT))
from scripts.generator_packages import build_manifest,manifest_digest

def main():
    p=json.loads((H/'installation-plan.json').read_text())
    for folder in {Path(r['entrypoint']).parent for r in p}:
        for target,source in [('ca_source_policy.py','generator_source_policy.py'),('ca_source_runtime.py','generator_source_runtime.py')]:
            shutil.copyfile(ROOT/'scripts'/source,folder/target)
    for r in p:
        r['new_sha256']=hashlib.sha256(Path(r['entrypoint']).read_bytes()).hexdigest()
        if r['packaged']:
            m=r['manifest'];r['manifest']=build_manifest(H/'packages'/str(r['kp']),m['entrypoint'],m['files'],dependencies=m['dependencies'])
            r['digest']=manifest_digest(r['manifest'])
    (H/'installation-plan.json').write_text(json.dumps(p,indent=2)+'\n')

if __name__=='__main__':main()
