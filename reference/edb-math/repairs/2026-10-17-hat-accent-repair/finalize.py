"""Refresh affected records, preview, verify, and submit the authorized repair.

The full audit remains pinned in its saved census. This final fast refresh reads
all affected records at the current basis; post_commit_scan.py audits every
string attribute again at the receipt's exact basis. No unknown outcome rebasing.
"""
import json, runpy, shutil, subprocess, sys
from pathlib import Path
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT))
from scripts.generator_publish import Publisher
HERE=Path(__file__).resolve().parent
E=HERE/'evidence'
publisher=Publisher.from_environment(source=':agent/codex')
if (HERE/'commit-intent.json').exists():
    # Submission recovery must retain exact source, bytes, basis, and request key.
    runpy.run_path(str(HERE/'submit.py'),run_name='__main__')
    raise SystemExit(0)
status=publisher.client.status()
old=json.loads((E/'status.json').read_text())
assert (old['database'],old['lineage'])==(status['database'],status['lineage'])
if status['basis']!=old['basis']:
    archive=HERE/('evidence-b'+str(old['basis']))
    assert not archive.exists()
    E.rename(archive)
    E.mkdir()
    for path in archive.glob('current-*'):
        shutil.copy(path,E/path.name)
    shutil.copy(archive/'schema.edn',E/'schema.edn')
(E/'status.json').write_text(json.dumps(status,indent=2)+'\n')
audit_bases=sorted({json.loads(p.read_text())['as_of_basis'] for p in E.glob('current-*-stats.json')})
(E/'final-refresh.json').write_text(json.dumps({'records_basis':status['basis'],'full_census_bases':audit_bases,
    'post_commit_full_census_required':True},indent=2)+'\n')
print('Final record refresh at basis',status['basis'],flush=True)
runpy.run_path(str(HERE/'snapshot.py'),run_name='__main__')
runpy.run_path(str(HERE/'prepare.py'),run_name='__main__')
runpy.run_path(str(HERE/'validate_browser.py'),run_name='__main__')
preview=ROOT/'reference/edb-math/imports/authored-checkboxes/2026-10-16/lesson-17592186492056/native/preview'
result=subprocess.run([str(preview),str(HERE),':agent/codex',str(status['basis'])],
    env=publisher.client.environment,capture_output=True,text=True)
(HERE/'preview.stderr').write_text(result.stderr)
if result.returncode:
    raise RuntimeError('Native preview failed before any submission: '+result.stderr)
(HERE/'preview.edn').write_text(result.stdout)
runpy.run_path(str(HERE/'verify.py'),run_name='__main__')
runpy.run_path(str(HERE/'submit.py'),run_name='__main__')
