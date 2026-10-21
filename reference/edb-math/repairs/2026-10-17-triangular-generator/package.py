"""Freeze the reviewed runtime closure and install the content-addressed copy."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
sys.dont_write_bytecode=True
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'Cargo.toml').exists())
sys.path.insert(0,str(ROOT))
from scripts.generator_packages import build_manifest,manifest_digest,publish_package,check_dependencies
from scripts.generator_publish import Publisher
HERE=Path(__file__).resolve().parent
ENTRY='17592186119771.py'
FILES=[ENTRY,'17592186119771/source.json']
def main():
    parser=argparse.ArgumentParser();parser.add_argument('action',choices=['prepare','publish']);parser.add_argument('--review',type=Path);args=parser.parse_args()
    publisher=Publisher.from_environment(source=':agent/gpt-6.1-sol-high')
    if args.action=='prepare':
        review=json.loads(args.review.read_text())
        assert review.get('passed') is True or review.get('status')=='passed'
        manifest=build_manifest(ROOT/'generate/scratch',ENTRY,FILES,dependencies={'python':'3.13.5','packages':{'sympy':'1.14.0'}})
        assert manifest['files'][ENTRY]['sha256']==review['generator_sha256'], 'Generator changed since independent review'
        plan={'manifest':manifest,'digest':manifest_digest(manifest),'review':str(args.review),'review_sha256':hashlib.sha256(args.review.read_bytes()).hexdigest(),
              'observed_dependencies':check_dependencies(manifest['dependencies'],sys.executable)}
        (HERE/'package-plan.json').write_text(json.dumps(plan,indent=2)+'\n')
        print(json.dumps({'prepared':True,'digest':plan['digest']}))
    else:
        plan=json.loads((HERE/'package-plan.json').read_text());manifest=plan['manifest']
        assert hashlib.sha256(Path(plan['review']).read_bytes()).hexdigest()==plan['review_sha256']
        package=publish_package(ROOT/'generate/scratch',ENTRY,FILES,publisher.config.math_root,
            dependencies=manifest['dependencies'],expected_digest=plan['digest'])
        result={**plan,'reference':package.reference,'verified':True}
        (HERE/'published-package.json').write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps({'published':True,'reference':package.reference}))
if __name__=='__main__':main()
