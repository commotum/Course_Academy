"""Stage a self-contained successor; never publish or mutate installed packages."""
import difflib,hashlib,json,shutil,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4]
OLD='generators/16/16d9bf0859532bdc42d1416549b7eaab4e739f0ac2a1a0599e07a3b1deadf642/17592186176047.py'
old=Path('/media/jake/SSD/EDB/math')/OLD;manifest=json.loads((old.parent/'generator-package.json').read_text())
dest=H/'generator-policy-portable-17592186176047';dest.mkdir(exist_ok=True)
for name in manifest['files']:
    target=dest/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(old.parent/name,target);target.chmod(0o644)
shutil.copyfile(R/'scripts/generator_policy.py',dest/'generator_policy.py')
path=dest/old.name;before=path.read_text()
obsolete='''import sys as _policy_sys
from pathlib import Path as _PolicyPath
_policy_sys.path.insert(0, str(next(p for p in _PolicyPath(__file__).resolve().parents if (p / "scripts/generator_policy.py").is_file())))
from scripts.generator_policy import nonempty_checkbox as _nonempty_checkbox'''
replacement='''# The complete policy implementation is a declared package-local dependency.
# This must work outside any repository, including disposable execution copies.
from generator_policy import nonempty_checkbox as _nonempty_checkbox'''
assert obsolete in before;after=before.replace(obsolete,replacement);path.write_text(after)
evidence={'classification':'Runtime dependency portability repair; authored mathematics/content identity unchanged.',
    'kp':17592186176047,'old_reference':OLD,
    'defect':'Published entrypoint searched ancestors for scripts/generator_policy.py; outside repository this raises StopIteration before generation.',
    'repair':'Bundle unchanged standalone generator_policy.py and import locally. Existing nonempty-checkbox wrapper and source-eligibility wrapper remain installed in the same order.',
    'preserved':'All authored templates, bands, data, source-policy ledger, question/field/answer identities, content hashes, source PNG bytes and asset-output/asset-identity logic.',
    'identity':'No version bump: this repair changes dependency resolution, not generated content. Same supported inputs must preserve authored output UUIDs.',
    'validation':'outside-repository-validation.json; package copied to /tmp outside every repository ancestor, cwd=/tmp, ordinary environment without PYTHONPATH/_CA_SOURCE_POLICY_CHILD injection; all supported bands and source/nonempty guards checked.'}
(dest/'repair-evidence.json').write_text(json.dumps(evidence,indent=2)+'\n')
(H/'cosine-policy-portability.diff').write_text(''.join(difflib.unified_diff(before.splitlines(True),after.splitlines(True),fromfile=str(old),tofile=str(path))))
files=sorted(set(manifest['files'])|{'generator_policy.py'})
(H/'policy-portability-stage.json').write_text(json.dumps({'kp':17592186176047,'old_reference':OLD,'directory':str(dest),'entrypoint':old.name,'files':files,'dependencies':manifest['dependencies']},indent=2)+'\n')
print(dest)
