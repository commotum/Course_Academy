"""Refresh read-only evidence at the current basis; require identical repair scope."""
import json, runpy, shutil, subprocess, sys
from pathlib import Path
sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))
from scripts.generator_publish import Publisher
from capture.scripts.database.edn import loads
sys.path.insert(0,str(Path(__file__).resolve().parent))
from repair import structured_occurrences, FLATTENED
HERE = Path(__file__).resolve().parent
E = HERE / 'evidence'
publisher = Publisher.from_environment(source=':agent/codex')
status = publisher.client.status()
old_status = json.loads((E / 'status.json').read_text())
assert (status['database'], status['lineage']) == (old_status['database'], old_status['lineage'])
if status['basis'] != old_status['basis']:
    archive = HERE / ('evidence-b' + str(old_status['basis']))
    assert not archive.exists(), archive
    E.rename(archive)
    E.mkdir()
    shutil.copy(archive/'schema.edn',E/'schema.edn')
(E / 'status.json').write_text(json.dumps(status, indent=2) + '\n')
print('Current basis', status['basis'], flush=True)
result = subprocess.run([str(HERE / 'native/census'), str(E), str(status['basis'])],
                        env=publisher.client.environment, capture_output=True, text=True, check=True)
(E / 'census.stdout').write_text(result.stdout)
(E / 'census.stderr').write_text(result.stderr)
attrs = {i:str(a) for i,a,t,c in loads((HERE/'evidence-b3672/schema.edn' if (HERE/'evidence-b3672/schema.edn').exists() else E/'schema.edn').read_text())}
actual = {(e, attrs[a]): v for p in E.glob('current-*.edn')
          for e, a, v, tx, source, added in loads(p.read_text()) if added and (structured_occurrences(v) or FLATTENED.search(v))}
expected = {(c['entity'], c['attribute']): c['before']
            for c in json.loads((HERE / 'changes.json').read_text())}
assert actual == expected, 'Repair scope or before values changed; investigate before submission'
(E / 'scope-verification.json').write_text(json.dumps({
    'basis': status['basis'], 'all_current_defects_covered': True,
    'all_before_values_unchanged': True, 'affected_attributes': len(actual)}, indent=2) + '\n')
runpy.run_path(str(HERE / 'snapshot.py'), run_name='__main__')
runpy.run_path(str(HERE / 'prepare.py'), run_name='__main__')
