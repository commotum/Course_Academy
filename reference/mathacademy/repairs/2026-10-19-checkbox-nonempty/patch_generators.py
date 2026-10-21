"""Apply a common seeded nonempty policy to all registered checkbox generators."""
import ast
import hashlib
import json
import shutil
from pathlib import Path
from read import HERE, ROOT

POLICY = ROOT / 'scripts/generator_policy.py'

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def patch_source(text, packaged):
    tree = ast.parse(text)
    names = sorted({node.name for node in tree.body if isinstance(node, ast.FunctionDef)
                    and (node.name.startswith('generate') or node.name == 'batch')})
    guards = [node for node in tree.body if isinstance(node, ast.If)
              and '__name__' in ast.unparse(node.test) and '__main__' in ast.unparse(node.test)]
    assert guards, 'Registered generator needs a main guard'
    insertion = max(node.lineno for node in guards) - 1
    header = '\n# Every learner-facing checkbox question has a nonempty correct selection.\n'
    if not packaged:
        header += ('import sys as _policy_sys\nfrom pathlib import Path as _PolicyPath\n'
                   '_policy_sys.path.insert(0, str(next(p for p in _PolicyPath(__file__).resolve().parents if (p / "scripts/generator_policy.py").is_file())))\n'
                   'from scripts.generator_policy import nonempty_checkbox as _nonempty_checkbox\n')
    else:
        header += 'from generator_policy import nonempty_checkbox as _nonempty_checkbox\n'
    header += 'for _policy_name in ' + repr(names) + ':\n'
    header += '    globals()[_policy_name] = _nonempty_checkbox(globals()[_policy_name])\n\n'
    lines = text.splitlines(keepends=True)
    return ''.join(lines[:insertion]) + header + ''.join(lines[insertion:]), names

if __name__ == '__main__':
    candidates = json.loads((HERE / 'checkbox-generators.json').read_text())
    updates = json.loads((HERE / 'patched-generators.json').read_text()) if (HERE / 'patched-generators.json').exists() else []
    already = {record['kp'] for record in updates}
    for record in candidates:
        kp = record['kp']
        if kp in already: continue
        original = Path(record['runtime_script'])
        text = original.read_text()
        assert sha(original) == record['entrypoint_sha256'], ('Generator changed concurrently', kp)
        if record['packaged']:
            manifest = json.loads((original.parent / 'generator-package.json').read_text())
            directory = HERE / 'packages' / str(kp)
            for name in manifest['files']:
                target = directory / name
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(original.parent / name, target)
            shutil.copy2(POLICY, directory / 'generator_policy.py')
            target = directory / manifest['entrypoint']
        else:
            backup = HERE / 'legacy-before' / str(kp)
            backup.mkdir(parents=True, exist_ok=True)
            shutil.copy2(original, backup / original.name)
            directory = original.parent
            target = original
            manifest = None
        # This sampler supplies fixed numerical objects to its public renderer.
        # Exclude the empty membership mask before constructing those objects.
        if kp == 17592186054815:
            assert 'rng.randrange(16)' in text
            text = text.replace('rng.randrange(16)', 'rng.randrange(1,16)')
        patched, names = patch_source(text, record['packaged'])
        target.write_text(patched)
        updates.append({**record, 'updated_script': str(target), 'directory': str(directory),
                        'old_manifest': manifest, 'wrapped_functions': names,
                        'updated_sha256': sha(target), 'policy_sha256': sha(POLICY)})
    (HERE / 'patched-generators.json').write_text(json.dumps(updates, indent=2) + '\n')
    print(json.dumps({'generators': len(updates), 'legacy_scripts_patched': sum(not r['packaged'] for r in updates),
                      'immutable_package_revisions': sum(r['packaged'] for r in updates)}))
