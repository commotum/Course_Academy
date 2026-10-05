#!/usr/bin/env python3
"""Prepare initial content-only activity durations; --apply commits the plan.

Only activity/expected-seconds is written. Existing durations and all learner
facts are preserved. Formula arithmetic and content measurements run in Rust.
The saved plan lists activities whose content or duration model is unavailable.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts/question_capture'))
from database import Database, fingerprint
from edn import dumps, loads, kw


def build_native():
    subprocess.run(['cargo', 'build', '--release', '--lib', '--offline'], cwd=ROOT, check=True)
    deps = ROOT / 'target/release/deps'
    edb_deps = ROOT.parent / 'EDB/target/release/deps'
    binary = ROOT / '.local/edb/initialize-activity-xp'
    command = ['rustc', '--edition=2024', '-O', str(ROOT / 'scripts/initialize_activity_xp.rs')]
    for name, directory in [('edb_core', edb_deps), ('serde_json', deps), ('course_academy_engine', deps)]:
        library = max(directory.glob(f'lib{name}-*.rlib'), key=lambda p: p.stat().st_mtime_ns)
        command += ['--extern', f'{name}={library}']
    command += ['-L', f'dependency={edb_deps}', '-L', f'dependency={deps}', '-o', str(binary)]
    subprocess.run(command, cwd=ROOT, check=True)
    return binary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    out = args.output.resolve(); out.mkdir(parents=True, exist_ok=True)
    db = Database(SimpleNamespace(edb_bin=str(ROOT.parent / 'EDB/target/release/edb'),
        database='course-academy-v2', endpoint='/tmp/course-academy-edb-v2/writer.sock'))
    intent_path = out / 'intent.json'
    tx_path = out / 'transaction.edn'
    if not intent_path.exists():
        subprocess.run([str(build_native()), db.args.database, str(out / 'plan.json')], env=db.env, check=True)
        plan = json.loads((out / 'plan.json').read_text())
        if not plan['forms']:
            print(json.dumps({'already_complete': True, 'skipped': plan['skipped_count']})); return
        tx_path.write_text(dumps([{kw(k):v for k,v in form.items()} for form in plan['forms']]) + '\n')
        attributes = db.attributes(out, plan['basis'])
        before = db.protected(attributes, out, 'protected-before', plan['basis'])
        preview = loads(db.command('with', '--file', tx_path))
        assert preview[':edb/db-before-t'] == plan['basis'], 'Database changed; use a fresh output directory'
        ids = {str(name): eid for eid, name in attributes}
        permitted = {ids[':activity/expected-seconds'], ids[':db/txInstant']}
        assert all(d[1] in permitted and d[-1] is True for d in preview[':edb/tx-data'])
        assert sum(d[1] == ids[':activity/expected-seconds'] for d in preview[':edb/tx-data']) == plan['estimated_count']
        intent = {'basis': plan['basis'], 'sha256': hashlib.sha256(tx_path.read_bytes()).hexdigest(),
            'protected_sha256': fingerprint(before), 'protected_count': len(before)}
        intent_path.write_text(json.dumps(intent, indent=2) + '\n')
    intent = json.loads(intent_path.read_text())
    assert hashlib.sha256(tx_path.read_bytes()).hexdigest() == intent['sha256']
    plan = json.loads((out / 'plan.json').read_text())
    if not args.apply:
        print(json.dumps({'previewed': True, 'estimated': plan['estimated_count'], 'skipped': plan['skipped_count']})); return
    receipt = loads(db.command('transact', '--file', tx_path, '--endpoint', db.args.endpoint,
        '--basis', intent['basis'], '--request-key', 'initial-activity-xp-' + intent['sha256']))
    (out / 'receipt.edn').write_text(dumps(receipt) + '\n')
    after_basis = receipt[':edb/db-after-t']
    attributes = db.attributes(out, after_basis)
    after = db.protected(attributes, out, 'protected-after', after_basis)
    assert fingerprint(after) == intent['protected_sha256'], 'Protected facts changed'
    ids = {str(name): eid for eid, name in attributes}
    assert all(d[1] in (ids[':activity/expected-seconds'], ids[':db/txInstant']) and d[-1] is True for d in receipt[':edb/tx-data'])
    actual = db.query('[:find ?a ?seconds :in $ [?a ...] :where [?a :activity/expected-seconds ?seconds]]',
        [[f['db/id'] for f in plan['forms']]], out, 'durations-after', after_basis)
    assert dict(actual) == {f['db/id']: f['activity/expected-seconds'] for f in plan['forms']}
    report = {'committed': True, 'basis_before': intent['basis'], 'basis_after': after_basis,
        'estimated_count': plan['estimated_count'], 'skipped_count': plan['skipped_count'],
        'learner_and_policy_facts_unchanged': True, 'protected_fact_count': len(after)}
    (out / 'verification.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
