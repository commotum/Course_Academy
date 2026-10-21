"""Freeze independently reviewed generator closures and publish immutable bytes."""
import argparse,hashlib,json,sys
from pathlib import Path
sys.dont_write_bytecode=True
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'Cargo.toml').exists());sys.path.insert(0,str(ROOT))
from scripts.generator_packages import build_manifest,manifest_digest,publish_package,check_dependencies
from scripts.generator_publish import Publisher
HERE=Path(__file__).resolve().parent
def save(name,value):(HERE/name).write_text(json.dumps(value,indent=2)+'\n')
def main():
    parser=argparse.ArgumentParser();parser.add_argument('action',choices=['prepare','publish']);args=parser.parse_args()
    publisher=Publisher.from_environment(source=':agent/gpt-6.1-sol-high')
    if args.action=='prepare':
        inputs=json.loads((HERE/'generators/package-inputs.json').read_text());packages=[]
        for rec in inputs:
            review=json.loads(Path(rec['review_path']).read_text());assert review['passed']
            reviewed=next(g for g in review['generators'] if g['kp_id']==rec['kp_id'])
            assert reviewed['generator_sha256']==rec['generator_sha256']
            manifest=build_manifest(Path(rec['source_root']),rec['entrypoint'],rec['files'],dependencies=rec['dependencies'])
            assert manifest['files'][rec['entrypoint']]['sha256']==rec['generator_sha256']
            digest=manifest_digest(manifest)
            packages.append({**rec,'manifest':manifest,'digest':digest,'reference':f'generators/{digest[:2]}/{digest}/{rec["entrypoint"]}',
                'observed_dependencies':check_dependencies(rec['dependencies'],sys.executable),
                'review_sha256':hashlib.sha256(Path(rec['review_path']).read_bytes()).hexdigest()})
        save('packages-plan.json',{'packages':packages});print(json.dumps({'prepared':True,'packages':[{'kp':p['kp_id'],'digest':p['digest']} for p in packages]}))
    else:
        plan=json.loads((HERE/'packages-plan.json').read_text())
        for rec in plan['packages']:
            assert hashlib.sha256(Path(rec['review_path']).read_bytes()).hexdigest()==rec['review_sha256']
            package=publish_package(Path(rec['source_root']),rec['entrypoint'],rec['files'],publisher.config.math_root,
                dependencies=rec['dependencies'],expected_digest=rec['digest'])
            assert package.reference==rec['reference']
        save('published-packages.json',{**plan,'verified':True});print(json.dumps({'published':True,'packages':len(plan['packages'])}))
if __name__=='__main__':main()
