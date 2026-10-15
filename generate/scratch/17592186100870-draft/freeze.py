"""Whole-owned-tree freeze; no registration or shared-report mutations."""
import sys
sys.dont_write_bytecode=True
import hashlib
import importlib.util
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('private00870validation',HERE/'validate.py')
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
def main():
    v.verify_immutable();v.provenance()
    files=[HERE.with_suffix('.py'),*[p for p in sorted(HERE.rglob('*')) if p.is_file() and p!=HERE/'freeze.json']]
    hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    if '--check' in sys.argv:
        old=json.loads((HERE/'freeze.json').read_text())
        assert old['files']==hashes,'Owned pathset or hash changed'
        print(json.dumps({'passed':True,'owned_files':len(hashes),'generator_sha256':hashes[str(HERE.with_suffix('.py').relative_to(ROOT))]}))
        return
    validation=json.loads((HERE/'validation.json').read_text())
    assert validation['status']=='pass'
    assert validation['generator_sha256']==hashes[str(HERE.with_suffix('.py').relative_to(ROOT))]
    assert json.loads((HERE/'render-validation.json').read_text())['passed']
    manifest={'status':'step7 draft frozen; root approval pending','generator_path':str(HERE.with_suffix('.py').relative_to(ROOT)),'generator_sha256':hashes[str(HERE.with_suffix('.py').relative_to(ROOT))],'primary_source_basis':2275,'owned_files':len(hashes),'exclusion':'freeze.json only (self reference)','numeric_baseline_unchanged':True,'database_writes':0,'files':hashes}
    (HERE/'freeze.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps({k:v for k,v in manifest.items() if k!='files'}))
if __name__=='__main__':main()
