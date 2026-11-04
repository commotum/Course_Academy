"""Register the same verified generator with its explicit finite-capacity file."""
import json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path.insert(0,str(ROOT))
from scripts.generator_publish import Publisher,file_lock,StaleBasis
from scripts.generator_packages import publish_package,build_manifest,manifest_digest,verify_package
from capture.scripts.storage import atomic_json

def main():
    p=Publisher.from_environment(source=':agent/codex');kp=17592186059672
    folder=ROOT/'generate/repairs/2026-11-04-four-trig-lessons/sine-double'/str(kp)
    m=json.loads((folder/'runtime-manifest.json').read_text());built=build_manifest(folder,'generator.py',m['runtime_files'],dependencies=m['dependencies'])
    package=publish_package(folder,'generator.py',m['runtime_files'],p.config.math_root,dependencies=m['dependencies'],expected_digest=manifest_digest(built));verify_package(package.directory,package.digest)
    proof=json.loads((H/'verification.json').read_text());current=next(k for k in proof['kps'] if k['kp']==kp)
    d=H/'finite-capacity-registration';d.mkdir(exist_ok=True)
    lock=ROOT/'.local/learning/inventory/math/59d5cf13-351c-4114-be19-4c3bb64ee051'/f'kp-{kp}.lock'
    with file_lock(lock):
        for attempt in range(5):
            try:
                if not (d/'request.json').exists():
                    p.prepare(kp,[],package.reference,package.digest,d,
                        source_snapshot=json.loads((H/'source'/str(kp)/'source.json').read_text()),
                        expected_registered_generator=current['generator'])
                result=p.publish(d);break
            except StaleBasis:continue
        else:raise RuntimeError('Repeated basis races')
    atomic_json(d/'registration.json',{'passed':True,'generator':package.reference,'package_sha256':package.digest,'proof':result})
    current.update(generator=package.reference,package_sha256=package.digest,finite_capacity_registration=str((d/'registration.json').relative_to(ROOT)))
    atomic_json(H/'verification.json',proof)
    print(json.dumps({'registered':True,'kp':kp,'capacity':{'easy':4},'generator':package.reference}))

if __name__=='__main__':main()
