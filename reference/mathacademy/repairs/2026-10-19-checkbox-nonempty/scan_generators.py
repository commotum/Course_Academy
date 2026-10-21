"""Read every registered generator's declared code for checkbox capability."""
import ast
import hashlib
import json
from pathlib import Path
from capture.scripts.config import Config
from scripts.generator_packages import resolve_registered_script, materialize_package

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
config = Config()
registry = json.loads((HERE / 'registry.json').read_text())
records, candidates = [], []
for kp, entity, reference in registry:
    script = resolve_registered_script(reference, ROOT, Path(config.math_root))
    manifest_path = script.parent / 'generator-package.json'
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else None
    files = [script.parent / name for name in manifest['files'] if name.endswith('.py')] if manifest else [script]
    hits = [str(path.relative_to(script.parent)) for path in files if 'checkbox' in path.read_text()]
    tree = ast.parse(script.read_text())
    functions = [{ 'name': node.name, 'args': [a.arg for a in node.args.args] }
                 for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name.startswith('generat')]
    record = {'kp': kp, 'entity': entity, 'reference': reference, 'script': str(script),
              'packaged': manifest is not None, 'checkbox_code': hits,
              'entrypoint_sha256': hashlib.sha256(script.read_bytes()).hexdigest(), 'functions': functions}
    records.append(record)
    if hits:
        if manifest:
            directory = HERE / 'original-packages' / str(kp)
            if not directory.exists(): materialize_package(reference, Path(config.math_root), directory)
            record['runtime_script'] = str(directory / manifest['entrypoint'])
        else:
            record['runtime_script'] = str(script)
        candidates.append(record)
(HERE / 'generator-scan.json').write_text(json.dumps(records, indent=2) + '\n')
(HERE / 'checkbox-generators.json').write_text(json.dumps(candidates, indent=2) + '\n')
print(json.dumps({'registered': len(records), 'checkbox_candidates': len(candidates),
                  'legacy_candidates': sum(not r['packaged'] for r in candidates)}))
for record in candidates:
    print(record['kp'], 'package' if record['packaged'] else 'legacy', record['functions'])
