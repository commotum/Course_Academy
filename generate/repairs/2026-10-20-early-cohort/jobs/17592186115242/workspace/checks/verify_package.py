"""Relocate declared runtime files and exercise the repaired CLI from /tmp."""
import hashlib
import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
from validate_repair import W, g, s, printed_check

E = W/'evidence/repair-2'
manifest = json.loads((W/'package.json').read_text())
assert manifest['dependencies'] == {'python':sys.version.split()[0],'packages':{'sympy':s.__version__}}
assert (W/'requirements.txt').read_text().strip() == 'sympy=='+s.__version__
files = manifest['files']
assert 'package.json' not in files
assert all(not pathlib.Path(f).is_absolute() and '..' not in pathlib.Path(f).parts for f in files)
args = ['--difficulty','easy','--count','5','--seed','1475864943','--format','json']
with tempfile.TemporaryDirectory(prefix='relocated-',dir=E) as tmp:
    dest = pathlib.Path(tmp).resolve()
    for rel in files:
        target=dest/rel;target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(W/rel,target)
    command=[sys.executable,'-B',str(dest/manifest['entrypoint']),*args]
    proc = subprocess.run(command,cwd='/tmp',capture_output=True,text=True,check=True,
        env={**os.environ,'PYTHONPATH':'','COURSE_ACADEMY_GENERATOR_OUTPUT_DIR':str((E/'assets').resolve())})
    records=json.loads(proc.stdout)
    assert records==json.loads((E/'batch.json').read_text())
    for r in records: printed_check(r)
# One smaller request verifies the documented unchanged single-seed path.
assert g.generate_batch('easy',1,1475864945)==[g.generate('easy',1475864945)]
report=dict(passed=True,relocated_cli=True,records=len(records),single_seed_replay=True,
            dependencies=manifest['dependencies'],command=command,
            runtime_hashes={f:hashlib.sha256((W/f).read_bytes()).hexdigest() for f in files})
(E/'packaging.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(passed=True,relocation=True,records=len(records),dependencies=manifest['dependencies'])))
