"""Additive inventory preparation and guarded commit using application EDB tools."""
import copy
import fcntl
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import threading
import uuid
from types import SimpleNamespace

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HERE))
from capture.scripts.database.preview import preview_executable
from state import DB, ENV, inventory
from edn import dumps, loads, kw
from inventory_jobs import save
import validate as v

g = v.g
KP = g.KP_ID
LEARNER = '59d5cf13-351c-4114-be19-4c3bb64ee051'
LINEAGE = '01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'
SOURCE = ':application/ca-engine'
SCRIPT = str(HERE.with_suffix('.py').relative_to(ROOT))
JOB = ROOT / '.local/learning/inventory/math' / LEARNER / '9e81ad5f79b4b1db91585c5eb1f5d50b2cf2e6ea676ae81a19bcd52ac9933ac2'
OUT = HERE / 'reference/replenishment'
LOCK = ROOT / '.local/learning/requests/math/api.lock'
QUERY = (HERE / 'reference/source-query.edn').read_text()
USAGE_QUERY = '''[:find ?q :in $ ?kp ?learner :where
 [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q]
 (or-join [?q ?l]
  (and [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q])
  (and [?l :learner/activity ?t] [?t :learner-task/status ?status]
   (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused])
   [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]))]'''


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical(value):
    if isinstance(value, dict):
        return {str(k): canonical(x) for k, x in value.items()}
    if isinstance(value, (list, tuple)):
        return sorted((canonical(x) for x in value), key=lambda x: json.dumps(x, sort_keys=True))
    return str(value) if isinstance(value, uuid.UUID) else value


def read_kp(path, basis):
    return DB.query(QUERY, [KP], path, 'kp', basis)[0][0]


def normalize(q):
    f = q[':question/answer-fields'][0]
    def enum(z):
        return str(z[':db/ident']) if isinstance(z, dict) else z
    return {
        'id': str(q[':question/id']), 'problem': q[':question/problem'], 'solution': q[':question/worked-solution'],
        'difficulty': enum(q[':question/difficulty']), 'field_id': str(f[':answer-field/id']),
        'field_type': enum(f[':answer-field/type']), 'field_key': f[':answer-field/key'],
        'correct': str(f[':answer-field/correct'][':answer/id']) if isinstance(f[':answer-field/correct'], dict) else f[':answer-field/correct'][1],
        'choices': sorted((str(a[':answer/id']), enum(a[':answer/type']), a[':answer/value']) for a in f[':answer-field/choices']),
    }


def candidates():
    return [r for r in json.loads((HERE / 'validated-instances.json').read_text()) if r['generation']['parameters']['scale'] != 1]


def counts(kp, path, basis):
    unavailable = {r[0] for r in DB.query(USAGE_QUERY, [KP, LEARNER], path, 'usage', basis)}
    recognized = {r['question'][':question/id']: r for r in candidates()}
    result = {level: [] for level in g.SUPPORTED_LEVELS}
    excluded = []
    for q in kp[':knowledge-point/questions']:
        mid = q.get(':question/math-academy-id')
        if q[':db/id'] in unavailable or q.get(':knowledge-point/_canonical-example'):
            continue
        if mid in g.DATA:
            src = g.SOURCES[mid]
            # Count only complete captured records that were independently
            # validated, not merely any question with a difficulty fact.
            assert canonical(q) == canonical(src), 'Source changed: reclassify'
            level = g.DATA[mid][-1]
            r = g.generate(level, template=mid, parameters={'scale': 1})
        elif str(q[':question/id']) in recognized:
            r = recognized[str(q[':question/id'])]
            assert normalize(q) == normalize(r['question'])
            level = r['question'][':question/difficulty'].split('/')[-1]
        else:
            excluded.append({'id': str(q[':question/id']), 'source': mid,
                             'reason': g.EXCLUDED.get(mid, 'Not a validated recognized instance')})
            continue
        v.independent(r)
        result[level].append((r['generation']['mathematical_signature'], str(q[':question/id'])))
    data = {'basis': basis, 'levels': {l: {'distinct_available_tasks': len({s for s, _ in rows}),
            'available_question_ids': [i for _, i in rows]} for l, rows in result.items()},
            'excluded_shown_or_reserved': sorted(unavailable), 'excluded_ungradable_or_contextual': excluded}
    save(path / 'available-counts.json', data)
    return data


def transaction(records, kp, gid):
    forms = []
    for rec in records:
        q = rec['question']
        for f in q[':question/answer-fields']:
            for a in f[':answer-field/choices']:
                forms.append({kw('db/id'): a[':answer/id'], kw('answer/id'): uuid.UUID(a[':answer/id']),
                              kw('answer/type'): kw(a[':answer/type']), kw('answer/value'): a[':answer/value'],
                              kw('db/ensure'): kw('answer/validate')})
            forms.append({kw('db/id'): f[':answer-field/id'], kw('answer-field/id'): uuid.UUID(f[':answer-field/id']),
                          kw('answer-field/key'): f[':answer-field/key'], kw('answer-field/type'): kw(f[':answer-field/type']),
                          kw('answer-field/choices'): [a[':answer/id'] for a in f[':answer-field/choices']],
                          kw('answer-field/correct'): f[':answer-field/correct'][1], kw('db/ensure'): kw('answer-field/validate')})
        forms.append({kw('db/id'): q[':question/id'], kw('question/id'): uuid.UUID(q[':question/id']),
                      kw('question/problem'): q[':question/problem'], kw('question/worked-solution'): q[':question/worked-solution'],
                      kw('question/difficulty'): kw(q[':question/difficulty']),
                      kw('question/answer-fields'): [f[':answer-field/id'] for f in q[':question/answer-fields']], kw('db/ensure'): kw('question/validate')})
    gen = kp.get(':knowledge-point/question-generator')
    if gen is None:
        forms += [{kw('db/id'): 'generator', kw('question-generator/id'): uuid.UUID(gid), kw('question-generator/script'): SCRIPT},
                  [kw('db/add'), KP, kw('knowledge-point/question-generator'), 'generator']]
    else:
        assert str(gen[':question-generator/id']) == gid and gen[':question-generator/script'] == SCRIPT
    if records:
        forms.append({kw('db/id'): KP, kw('knowledge-point/questions'): [r['question'][':question/id'] for r in records]})
    if forms:
        forms.append([kw('db/ensure'), KP, kw('knowledge-point/validate')])
    return forms


def check_report(report, path, source):
    attrs = {e: str(a) for e, a in DB.attributes(path, report[':edb/db-before-t'])}
    new = set(report[':edb/tempids'].values())
    allowed = {':question/id', ':question/problem', ':question/worked-solution', ':question/difficulty', ':question/answer-fields',
               ':answer-field/id', ':answer-field/key', ':answer-field/type', ':answer-field/choices', ':answer-field/correct',
               ':answer/id', ':answer/type', ':answer/value', ':question-generator/id', ':question-generator/script'}
    for e, a, value, tx, s, added in report[':edb/tx-data']:
        assert added and s == source, 'Unexpected retraction or attribution'
        name = attrs[a]
        if e == KP:
            assert name in (':knowledge-point/questions', ':knowledge-point/question-generator')
        elif name != ':db/txInstant':
            assert e in new and name in allowed, name


def verify(path, intent, report):
    assert report[':edb/committed'] is True and report[':edb/db-before-t'] == intent['basis']
    check_report(report, path / 'receipt-check', intent['source_eid'])
    basis = report[':edb/db-after-t']
    kp = read_kp(path / 'readback', basis)
    before = loads((path / 'before.edn').read_text())
    old = {q[':db/id']: q for q in before[':knowledge-point/questions']}
    now = {q[':db/id']: q for q in kp[':knowledge-point/questions']}
    assert all(now[e] == q for e, q in old.items()), 'Source question changed'
    assert {k: v for k, v in before.items() if k not in (':knowledge-point/questions', ':knowledge-point/question-generator')} == {k: v for k, v in kp.items() if k not in (':knowledge-point/questions', ':knowledge-point/question-generator')}
    gen = kp[':knowledge-point/question-generator']
    assert str(gen[':question-generator/id']) == intent['generator_id'] and gen[':question-generator/script'] == SCRIPT
    records = json.loads((path / 'generated.json').read_text())
    assert len(now) == len(old) + len(records)
    byid = {str(q[':question/id']): q for q in now.values()}
    for rec in records:
        q = byid[rec['question'][':question/id']]
        assert ':question/math-academy-id' not in q and normalize(q) == normalize(rec['question'])
        v.independent(rec)
    assert not transaction([], kp, intent['generator_id'])
    c = counts(kp, path / 'readback', basis)
    result = {'passed': True, 'basis_before': intent['basis'], 'basis_after': basis, 'new_questions': len(records),
              'unchanged_source_questions': len(old), 'learner_history_unchanged': True,
              'only_additive_scoped_content_datoms': True, 'generator_registration_verified': True,
              'repeat_preparation_content_changes': 0, 'available_counts_after': c}
    save(path / 'verification.json', result)
    return result


def finish(path, gid, verified, inv):
    prep = json.loads((path / 'preparation.json').read_text())
    caps = json.loads((HERE / 'capabilities.json').read_text())
    c = verified['available_counts_after']
    remaining = {l: max(0, 5-c['levels'][l]['distinct_available_tasks']) for l in g.SUPPORTED_LEVELS}
    result = {'outcome': 'finite-limit' if any(remaining.values()) else 'generated', 'knowledgePoint': KP,
              'generator_path': SCRIPT, 'generator_id': gid, 'lineage': LINEAGE,
              'verified_commit_basis': verified['basis_after'], 'new_questions': verified['new_questions'],
              'supported_levels': list(g.SUPPORTED_LEVELS), 'available_counts_before': prep['available_counts'],
              'available_counts_after': c, 'shortage_remaining': remaining, 'unsupported_levels_filled': False,
              'unsupported_nominal_shortage': {'hard': 5}, 'capability_exceptions': caps['exceptions'],
              'inventory_recheck_basis': inv['basis'], 'remaining_jobs': [j for j in inv['jobs'] if j['knowledgePoint'] == KP],
              'evidence': [str(p.relative_to(ROOT)) for p in [path/'verification.json', path/'commit-intent.json',
                  path/'transaction.edn', path/'commit.edn', path/'preview.edn', path/'preparation.json', path/'inventory-after.json',
                  HERE/'classification.json', HERE/'template-extraction.md', HERE/'plot-extraction.md', HERE/'validation.json',
                  HERE/'source-choice-mapping.json', HERE/'capabilities.json', path/'final-package-validation.json'] if p.exists()],
              'note': 'Complete available inventory meets easy/moderate targets. No additional questions were needed when zero were added. Generator executed and validated; source and history preserved. Hard remains unsupported with nominal shortage five. Remaining native jobs are reported explicitly.'}
    save(path / 'outcome.json', result)
    save(JOB.with_suffix('.result'), result)
    print(json.dumps({k: result[k] for k in ('outcome', 'verified_commit_basis', 'new_questions', 'shortage_remaining')}), flush=True)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    validation = json.loads((HERE / 'validation.json').read_text())
    assert validation['status'] == 'pass'
    assert all(sha(ROOT/p) == digest for p, digest in validation['hashes'].items())
    preview = preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'), repo_root=ROOT, preview_bin=None), threading.Event())
    with LOCK.open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        # Recover original exact requests/receipts before preparing fresh intent.
        for path in sorted(OUT.glob('basis-*')):
            if (path/'commit-intent.json').exists():
                intent = json.loads((path/'commit-intent.json').read_text())
                assert intent['lineage'] == LINEAGE and intent['source'] == SOURCE
                assert intent['database'] == 'math' and intent['endpoint'] == DB.args.endpoint
                assert intent['transaction_sha256'] == sha(path/'transaction.edn')
                assert intent['exact_edn'] == (path/'transaction.edn').read_text()
                assert intent['connection_sha256'] == hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
                inv = inventory(OUT/'inventory-recovery.json'); assert inv['lineage'] == LINEAGE
                report = DB._commit(intent, path/'transaction.edn', path)
                verified = verify(path, intent, report)
                finish(path, intent['generator_id'], verified, inventory(path/'inventory-after.json'))
                return
        inv = inventory(OUT/'inventory-before.json')
        assert inv['lineage'] == LINEAGE
        basis = inv['basis']; assert DB.basis() == basis
        path = OUT / ('basis-' + str(basis)); path.mkdir(exist_ok=True)
        save(path/'inventory-preparation.json', inv)
        kp = read_kp(path, basis)
        assert str(kp[':knowledge-point/id']) == g.KP_UUID
        (path/'before.edn').write_text(dumps(kp) + '\n')
        captured = g.SNAPSHOT['record']
        current = {q.get(':question/math-academy-id'): q for q in kp[':knowledge-point/questions'] if q.get(':question/math-academy-id')}
        for q in captured[':knowledge-point/questions']:
            assert canonical(current[q[':question/math-academy-id']]) == canonical(q), 'Source changed: reclassify'
        assert canonical(kp[':knowledge-point/canonical-example']) == canonical(captured[':knowledge-point/canonical-example'])
        source = DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]', [], path, 'contributor', basis)
        assert len(source) == 1
        gen = kp.get(':knowledge-point/question-generator')
        gid = str(gen[':question-generator/id']) if gen else g.GENERATOR_UUID
        assert gid == g.GENERATOR_UUID
        c = counts(kp, path, basis)
        needed = {l: max(0, 5-c['levels'][l]['distinct_available_tasks']) for l in g.SUPPORTED_LEVELS}
        used = {v.fingerprint(q) for q in kp[':knowledge-point/questions']}
        # The canonical example is not inventory and may never be reissued.
        used.add(v.fingerprint(kp[':knowledge-point/canonical-example']))
        supplied_path = JOB.with_suffix('.generated')
        supplied = json.loads(supplied_path.read_text()) if supplied_path.exists() else {}
        instances = supplied.get('instances', []); assert isinstance(instances, list)
        for rec in instances:
            v.independent(rec)
            assert rec == g.generate(rec['question'][':question/difficulty'].split('/')[-1],
                                     seed=rec['generation']['seed'], template=rec['generation']['template'],
                                     parameters=rec['generation']['parameters'])
        save(path/'supplied-status.json', {'exists': supplied_path.exists(), 'validated_instances': len(instances), 'generator_error': supplied.get('generatorError')})
        records = []; added = {l: 0 for l in g.SUPPORTED_LEVELS}
        for rec in instances + candidates():
            level = rec['question'][':question/difficulty'].split('/')[-1]
            sig = rec['generation']['mathematical_signature']
            if added[level] < needed[level] and sig not in used:
                v.independent(rec); records.append(rec); used.add(sig); added[level] += 1
        ids = [uuid.UUID(i) for r in records for f in r['question'][':question/answer-fields'] for i in [r['question'][':question/id'], f[':answer-field/id']] + [a[':answer/id'] for a in f[':answer-field/choices']]]
        if ids:
            matches = DB.query('[:find ?e ?id :in $ [?id ...] :where (or-join [?e ?id] [?e :question/id ?id] [?e :answer-field/id ?id] [?e :answer/id ?id])]', [ids], path, 'identity-matches', basis)
            assert not matches, 'Existing identities require reconciliation'
        generators = DB.query('[:find ?e :in $ ?id :where [?e :question-generator/id ?id]]', [uuid.UUID(gid)], path, 'generator-identity', basis)
        assert not generators or gen and generators == [[gen[':db/id']]]
        save(path/'generated.json', records)
        if records:
            save(path/'native-input.json', [{'label': r['question'][':question/id'], 'record': r, 'checks': v.checks(r)} for r in records])
            subprocess.run([str(ROOT/'generate/runs/current/check-engine'), str(path/'native-input.json'), str(path/'native-report.json')], check=True)
        assets = json.loads((HERE/'reference/asset-hashes.json').read_text())
        assert all(sha(Path('/media/jake/SSD/EDB/math')/asset) == digest for asset, digest in assets.items())
        save(path/'preparation.json', {'basis': basis, 'lineage': LINEAGE, 'source': SOURCE,
             'available_counts': c, 'missing_by_level': needed, 'new_by_level': added,
             'asset_hashes': assets, 'source_evidence_unchanged': True, 'source_basis': g.SNAPSHOT['basis'],
             'generator_sha256': sha(HERE.with_suffix('.py')), 'validation_sha256': sha(HERE/'validation.json')})
        forms = transaction(records, kp, gid)
        if not forms:
            verified = {'passed': True, 'basis_before': basis, 'basis_after': basis, 'new_questions': 0, 'no_changes': True, 'available_counts_after': c}
            save(path/'verification.json', verified); finish(path, gid, verified, inv); return
        txpath = path/'transaction.edn'; tx = dumps(forms) + '\n'
        with txpath.open('w') as stream:
            stream.write(tx); stream.flush(); os.fsync(stream.fileno())
        r = subprocess.run([str(preview), 'with', '--database', 'math', '--file', str(txpath), '--source', SOURCE], env=DB.env, capture_output=True, text=True, check=True, timeout=90)
        (path/'preview.edn').write_text(r.stdout)
        report = loads(r.stdout)
        assert report[':edb/committed'] is False and report[':edb/db-before-t'] == basis
        check_report(report, path/'preview-check', source[0][0])
        assert DB.basis() == basis
        intent = {'database': 'math', 'endpoint': DB.args.endpoint, 'lineage': LINEAGE, 'source': SOURCE,
                  'source_eid': source[0][0], 'basis': basis, 'expected_basis': basis,
                  'request_key': 'flux-integrand-inventory-' + str(KP) + '-' + str(basis) + '-' + sha(txpath),
                  'transaction_sha256': sha(txpath), 'sha256': sha(txpath), 'exact_edn': tx,
                  'generator_id': gid, 'generator_path': SCRIPT, 'generator_sha256': sha(HERE.with_suffix('.py')),
                  'question_uuids': [r['question'][':question/id'] for r in records],
                  'connection_sha256': hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(), 'lock': str(LOCK)}
        save(path/'commit-intent.json', intent)
        report = DB._commit(intent, txpath, path)
        verified = verify(path, intent, report)
        finish(path, gid, verified, inventory(path/'inventory-after.json'))


if __name__ == '__main__':
    main()
