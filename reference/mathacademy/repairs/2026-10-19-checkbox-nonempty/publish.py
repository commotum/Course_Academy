"""Publish reviewed package revisions and spacing-only database corrections."""
import copy
import hashlib
import json
import subprocess
import sys
import uuid
from pathlib import Path
from read import DB, HERE, ROOT
from capture.scripts.database.client import QUESTION_PULL
from capture.scripts.database.edn import dumps, loads, kw
from scripts.generator_packages import build_manifest, manifest_digest, publish_package, resolve_registered_script

SOURCE = ':agent/codex'
IDENTS = dict(json.loads((ROOT / 'reference/mathacademy/repairs/2026-10-18-equation-chains/idents.json').read_text()))
NAMES = {value: key for key, value in IDENTS.items()}
READER = ROOT / 'reference/mathacademy/repairs/2026-10-17-import-source-bulk/native_read'
SUBMIT = ROOT / '.local/fraction-fence-audit/submit-cas'
KP_PATTERN = '[:db/id :knowledge-point/id :knowledge-point/title {:knowledge-point/question-generator [*]}]'

def save(name, value):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=False, default=str) + '\n')

def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def native_read(directory, basis, groups):
    directory.mkdir(parents=True, exist_ok=True)
    (directory / 'native-pulls.edn').write_text(dumps(groups) + '\n')
    result = subprocess.run([str(READER), str(directory), str(basis)], env=DB.environment,
                            capture_output=True, text=True, timeout=180)
    (directory / 'read.stderr').write_text(result.stderr)
    result.check_returncode()
    return {name: loads((directory / (name + '.edn')).read_text()) for name, _, _ in groups}

def canonical(value):
    if isinstance(value, dict): return {str(k): canonical(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return sorted([canonical(v) for v in value], key=lambda v: json.dumps(v, sort_keys=True))
    return value if isinstance(value, (str, int, float, bool)) or value is None else str(value)

def prepare():
    patches = json.loads((HERE / 'patched-generators.json').read_text())
    modern = [p for p in patches if p['packaged']]
    registry = {kp: (entity, reference) for kp, entity, reference in json.loads((HERE / 'registry.json').read_text())}
    entity, reference = registry[17592186073777]
    modern.append({'kp': 17592186073777, 'entity': entity, 'reference': reference,
                   'directory': str(HERE / 'formatting/package'),
                   'old_manifest': json.loads((HERE / 'formatting/original/generator-package.json').read_text())})
    identity = DB.status()
    qids = [q[':db/id'] for q in json.loads((HERE / 'formatting/questions.json').read_text())]
    groups = [['questions', QUESTION_PULL, qids], ['knowledge-points', KP_PATTERN, [r['kp'] for r in modern]]]
    before = native_read(HERE / 'preparation', identity['basis'], groups)
    kps = {r[':db/id']: r for r in before['knowledge-points']}
    updates = []
    for record in modern:
        old = kps[record['kp']][':knowledge-point/question-generator']
        assert old[':db/id'] == record['entity'] and old[':question-generator/script'] == record['reference'], ('Concurrent generator revision', record['kp'])
        manifest = record['old_manifest']
        files = list(manifest['files'])
        if record['kp'] != 17592186073777 and 'generator_policy.py' not in files: files.append('generator_policy.py')
        candidate = build_manifest(Path(record['directory']), manifest['entrypoint'], files, dependencies=manifest['dependencies'])
        digest = manifest_digest(candidate)
        updates.append({'kp': record['kp'], 'old_generator': old, 'directory': record['directory'],
                        'manifest': candidate, 'digest': digest,
                        'reference': f'generators/{digest[:2]}/{digest}/{manifest["entrypoint"]}',
                        'generator_uuid': str(uuid.uuid5(uuid.UUID(str(kps[record['kp']][':knowledge-point/id'])), 'generator-package:' + digest))})
    changes = json.loads((HERE / 'formatting/changes.json').read_text())
    questions = {q[':db/id']: q for q in before['questions']}
    for change in changes:
        assert questions[change['entity']][change['attribute']] == change['before'], 'Concurrent question edit'
    save('publication-identity.json', identity)
    save('package-updates.json', updates)
    save('publication-groups.json', groups)
    print(json.dumps({'package_revisions': len(updates), 'legacy_script_revisions': len(patches)-len(modern)+1,
                      'formatting_questions': len(changes), 'basis': identity['basis']}))

def check_report(report, committed, updates, changes):
    assert report[':edb/committed'] is committed
    expected = set()
    guards = set()
    for c in changes:
        expected.add((c['entity'], c['attribute'], c['before'], False))
        expected.add((c['entity'], c['attribute'], c['after'], True))
    for u in updates:
        new = report[':edb/tempids']['generator-' + str(u['kp'])]
        old = u['old_generator']
        expected.update({(new, ':question-generator/id', uuid.UUID(u['generator_uuid']), True),
                         (new, ':question-generator/script', u['reference'], True),
                         (u['kp'], ':knowledge-point/question-generator', old[':db/id'], False),
                         (u['kp'], ':knowledge-point/question-generator', new, True)})
        guards.add((old[':db/id'], ':question-generator/script', old[':question-generator/script'], True))
    observed = set()
    times = 0
    for e, a, value, tx, source, added in report[':edb/tx-data']:
        assert source == NAMES[SOURCE]
        if IDENTS[a] == ':db/txInstant': times += 1; assert added
        else: observed.add((e, IDENTS[a], value, added))
    assert times == 1 and expected <= observed and observed-expected <= guards, (observed-expected-guards, expected-observed)

def commit():
    assert json.loads((HERE / 'quality-verification.json').read_text())['passed']
    updates = json.loads((HERE / 'package-updates.json').read_text())
    changes = json.loads((HERE / 'formatting/changes.json').read_text())
    request_path = HERE / 'request.json'
    if not request_path.exists():
        assert DB.status()['lineage'] == json.loads((HERE / 'publication-identity.json').read_text())['lineage']
        forms = []
        for u in updates:
            m = u['manifest']
            package = publish_package(Path(u['directory']), m['entrypoint'], m['files'], Path(DB.config.math_root),
                                      dependencies=m['dependencies'], expected_digest=u['digest'])
            assert package.reference == u['reference']
            temp = 'generator-' + str(u['kp'])
            forms.append({kw('db/id'): temp, kw('question-generator/id'): uuid.UUID(u['generator_uuid']), kw('question-generator/script'): u['reference']})
            forms.append([kw('db/cas'), u['kp'], kw('knowledge-point/question-generator'), u['old_generator'][':db/id'], temp])
            old = u['old_generator']
            forms.append([kw('db/cas'), old[':db/id'], kw('question-generator/script'), old[':question-generator/script'], old[':question-generator/script']])
        for c in changes:
            forms.append([kw('db/cas'), c['entity'], kw(c['attribute']), c['before'], c['after']])
            forms.append([kw('db/ensure'), c['entity'], kw('question/validate')])
        tx = HERE / 'transaction.edn'
        tx.write_text(dumps(forms) + '\n')
        preview_text = DB.command('with', '--file', tx, '--source', SOURCE, timeout=180)
        (HERE / 'preview.edn').write_text(preview_text)
        check_report(loads(preview_text), False, updates, changes)
        identity = json.loads((HERE / 'publication-identity.json').read_text())
        save('request.json', {'source': SOURCE, 'database': identity['database'], 'lineage': identity['lineage'],
                              'endpoint': DB.config.endpoint, 'transaction_file': str(tx), 'transaction_sha256': sha(tx),
                              'updates_sha256': sha(HERE / 'package-updates.json'), 'quality_sha256': sha(HERE / 'quality-verification.json'),
                              'request_key': 'checkbox-nonempty-and-line-spacing-' + sha(tx)})
    request = json.loads(request_path.read_text())
    assert sha(request['transaction_file']) == request['transaction_sha256']
    assert sha(HERE / 'package-updates.json') == request['updates_sha256']
    assert sha(HERE / 'quality-verification.json') == request['quality_sha256']
    receipt = HERE / 'receipt.edn'
    if not receipt.exists():
        result = subprocess.run([str(SUBMIT), 'transact', '--database', request['database'], '--file', request['transaction_file'],
                                 '--endpoint', request['endpoint'], '--request-key', request['request_key'], '--source', SOURCE,
                                 '--timeout-ms', '180000'], env=DB.environment, capture_output=True, text=True, timeout=210)
        (HERE / 'submission.stderr').write_text(result.stderr)
        result.check_returncode()
        receipt.write_text(result.stdout)
    report = loads(receipt.read_text())
    check_report(report, True, updates, changes)
    groups = json.loads((HERE / 'publication-groups.json').read_text())
    before = native_read(HERE / 'committed-before', report[':edb/db-before-t'], groups)
    after = native_read(HERE / 'committed-after', report[':edb/db-after-t'], groups)
    expected = copy.deepcopy(before)
    for q in expected['questions']:
        for c in changes:
            if q[':db/id'] == c['entity']:
                assert q[c['attribute']] == c['before']
                q[c['attribute']] = c['after']
    assert canonical(expected['questions']) == canonical(after['questions'])
    updated = {u['kp']: u for u in updates}
    for kp in after['knowledge-points']:
        u = updated[kp[':db/id']]
        gen = kp[':knowledge-point/question-generator']
        assert gen[':question-generator/script'] == u['reference'] and str(gen[':question-generator/id']) == u['generator_uuid']
        resolve_registered_script(u['reference'], ROOT, DB.config.math_root)
    verification = {'committed': True, 'basis_after': report[':edb/db-after-t'], 'package_revisions': len(updates),
                    'spacing_questions_repaired': len(changes), 'exact_receipt_and_readback': True,
                    'learner_records_and_answer_keys_unchanged': True}
    save('verification.json', verification)
    print(json.dumps(verification, indent=2))

if __name__ == '__main__':
    {'prepare': prepare, 'commit': commit}[sys.argv[1]]()
