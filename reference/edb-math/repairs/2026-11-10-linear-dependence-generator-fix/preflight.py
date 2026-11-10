"""Check relocated packages and actual refill survivors without publication."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

H=Path(__file__).resolve().parent
ROOT=H.parents[3]
sys.path[:0]=[str(ROOT),str(ROOT/'scripts')]
from scripts.generator_publish import Publisher,prepare_records
from scripts.generator_refill import validate_survivors
from scripts.generator_refill_plan import validate_refill_plan

publisher=Publisher.from_environment(source=':agent/codex')
summary=[]
for kp in [17592186119924,17592186119925]:
    package=H/'packages'/str(kp);manifest=json.loads((package/'package.json').read_text())
    findings=[dict(id=i) for i in ['subset-radio-response','redundant-none','empty-subset-support']]
    plan=validate_refill_plan(package,manifest,findings,H/'review')
    inventory=publisher.extract_inventory(kp,H/'delivery'/str(kp)/'inventory')
    source=json.loads((H/'sources'/str(kp)/'source.json').read_text())
    kp_uuid=source['material']['kp'][':knowledge-point/id']
    with tempfile.TemporaryDirectory(prefix='checkbox-package-relocation-',dir='/tmp') as temporary:
        relocated=Path(temporary)
        for name in manifest['files']:
            target=relocated/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(package/name,target)
        for band in ['easy','moderate','hard']:
            records=json.loads((H/'verification'/str(kp)/(band+'.json')).read_text())
            replay=json.loads(subprocess.check_output([sys.executable,str(relocated/manifest['entrypoint']),
                '--difficulty',band,'--count','30','--seed','20261110','--format','json'],cwd=relocated,timeout=60))
            assert records==replay,'Relocation changed sampled content or identities'
            accepted,duplicates=prepare_records(records,kp,kp_uuid,inventory['fingerprints'],publisher.config.math_root,package)
            assert accepted,'No distinct survivor available for verification'
            result=validate_survivors(accepted,inventory,H/'delivery'/str(kp)/band,root=package,
                manifest=manifest,band=band,python=sys.executable,repo_root=ROOT,
                environment=publisher.client.environment,expected_plan=plan)
            assert result['status']=='passed'
            summary.append(dict(kp=kp,band=band,sampled=len(records),survivors=len(accepted),duplicates=duplicates,
                relocated_identical=True,passed=True,refill_plan=plan,evidence=str((H/'delivery'/str(kp)/band/'result.json').relative_to(H))))
            print(kp,band,'passed',len(accepted),'actual survivors',flush=True)
(H/'preflight-verification.json').write_text(json.dumps(dict(passed=True,database_writes=0,checks=summary),indent=2)+'\n')
