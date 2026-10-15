"""Scoped additive inventory preparation, EDB commit, and exact-basis readback."""
import argparse
import copy
import fcntl
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import threading
from types import SimpleNamespace
import uuid

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
from capture.scripts.database.images import ImageLibrary
from capture.scripts.database.preview import preview_executable
sys.path[:0] = [str(ROOT / 'scripts'), str(ROOT / 'scripts/question_capture')]
from database import Database
from edn import dumps, loads, kw
from inventory_jobs import save
from serve_graph_explorer import database_environment
spec = importlib.util.spec_from_file_location('circle_validation', HERE / 'validate.py')
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)
g = v.g
KP = g.KP_ID
LEVELS = ('easy', 'moderate', 'hard')
LEARNER = '59d5cf13-351c-4114-be19-4c3bb64ee051'
LINEAGE = g.SOURCE['lineage']
SOURCE = ':application/ca-engine'
SCRIPT = str(HERE.with_suffix('.py').relative_to(ROOT))
JOB = ROOT / '.local/learning/inventory/math' / LEARNER / 'c7603d920d234754f578a73900363a5e60d084ca17c894d43727d0eea10925c0'
OUT = HERE / 'reference/replenishment'
OUT.mkdir(parents=True, exist_ok=True)
ENV = database_environment('math')
DB = Database(SimpleNamespace(edb_bin=str(ROOT / '.local/edb/capture-runtime/math-edb'), database='math', endpoint=ENV['EDB_ENDPOINT']))
DB.env = ENV
NATIVE = Path((HERE / 'reference/initial/native-path.txt').read_text())
QUERY = (HERE / 'reference/initial/kp-query.edn').read_text()
USAGE = '''[:find ?q :in $ ?kp ?learner :where
 [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q]
 (or-join [?q ?l]
  (and [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q])
  (and [?l :learner/activity ?t] [?t :learner-task/status ?status]
   (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused])
   [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]))]'''
HISTORY = '''[:find ?q :in $ ?kp ?learner :where
 [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q]
 [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q ?tx true]]'''


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def inventory(path):
    p = subprocess.run([str(NATIVE), 'math', LEARNER, DB.args.endpoint], input='{"action":"inventory"}', env=ENV, capture_output=True, text=True, check=True, timeout=90)
    x = json.loads(p.stdout)
    assert x['ok'] and x['data']['lineage'] == LINEAGE
    save(path, x['data'])
    return x['data']


def read_kp(path, basis):
    rows = DB.query(QUERY, [KP], path, 'kp', basis)
    assert len(rows) == 1 and str(rows[0][0][':knowledge-point/id']) == g.KP_UUID
    return rows[0][0]


def normalize(q):
    out = {k: str(q[k]) if k == ':question/id' else q[k] for k in (':question/id', ':question/problem', ':question/worked-solution') if k in q}
    if ':question/difficulty' in q:
        level = q[':question/difficulty']
        out[':question/difficulty'] = str(level.get(':db/ident')) if isinstance(level, dict) else str(level)
    out[':question/answer-fields'] = []
    for f in sorted(q[':question/answer-fields'], key=lambda f: f[':answer-field/key']):
        kind = f[':answer-field/type']
        ff = {':answer-field/id': str(f[':answer-field/id']), ':answer-field/key': f[':answer-field/key'], ':answer-field/type': str(kind.get(':db/ident')) if isinstance(kind, dict) else str(kind)}
        if ':answer-field/correct' in f:
            c = f[':answer-field/correct']
            ff[':answer-field/correct'] = [':answer/id', str(c[':answer/id']) if isinstance(c, dict) else str(c[1])]
        ff[':answer-field/choices'] = []
        for a in f[':answer-field/choices']:
            kind = a[':answer/type']
            ff[':answer-field/choices'].append({':answer/id': str(a[':answer/id']), ':answer/type': str(kind.get(':db/ident')) if isinstance(kind, dict) else str(kind), ':answer/value': a[':answer/value']})
        ff[':answer-field/choices'].sort(key=lambda a: a[':answer/id'])
        out[':question/answer-fields'].append(ff)
    return out


def fingerprint(q):
    if not q.get(':question/answer-fields'):
        rows = re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}', q[':question/worked-solution'], re.S)[1].split(r'\\')
        eq = rows[-1].replace('&', '').strip().rstrip('.')
        return str(g.polynomial(eq).monic().as_expr())
    f = q[':question/answer-fields'][0]
    c = f.get(':answer-field/correct')
    if c:
        eq = c[':answer/value'] if isinstance(c, dict) else next(a[':answer/value'] for a in f[':answer-field/choices'] if str(a[':answer/id']) == str(c[1]))
        # Complete equation modulo nonzero scalar; ignores identities, bank order,
        # renderer orientation, difficulty, and seed.
        return str(g.polynomial(eq).monic().as_expr())
    sid = q.get(':question/math-academy-id')
    assert sid in g.ORIGINAL, 'Unknown unkeyed question requires reconciliation'
    p = g.ORIGINAL[sid]
    return str(g.polynomial(g.equation(g.exact(p['h']), g.exact(p['k']), g.exact(p['r'])**2)).monic().as_expr())


def run_native(records, path):
    path.mkdir(parents=True, exist_ok=True)
    save(path / 'native-input.json', v.native_cases(records))
    p = subprocess.run([str(ROOT / 'generate/runs/current/check-engine'), str(path / 'native-input.json'), str(path / 'native-report.json')], capture_output=True, text=True)
    (path / 'native.log').write_text(p.stdout + p.stderr)
    assert p.returncode == 0, p.stdout + p.stderr
    report = json.loads((path / 'native-report.json').read_text())
    assert report['documented_unresolved_checks'] == 0
    assert report['accepted_checks'] == len(records)
    assert report['rejected_checks'] == len(records) * 4
    return {k: report[k] for k in ('accepted_checks', 'rejected_checks', 'documented_unresolved_checks')}


def validate_record(r):
    assert r['knowledge_point']['db_id'] == KP and r['knowledge_point']['id'] == g.KP_UUID
    meta = r['generation']
    assert meta['eligible_for_learning'] and meta['grading_compatibility']['supported'] and not meta['evidence_only']
    assert r['question'][':question/answer-fields'][0][':answer-field/type'] == ':answer-field.type/radio'
    assert ':question/math-academy-id' not in r['question']
    v.independent_from_display(r)
    replay = g.generate(r['question'][':question/difficulty'].split('/')[-1], seed=meta['seed'], template=meta['template'], parameters=meta['parameters'], profile=meta['bank_profile'])
    assert normalize(replay['question']) == normalize(r['question'])
    assert fingerprint(replay['question']) == fingerprint(r['question'])


def counts(kp, path, basis):
    path.mkdir(parents=True, exist_ok=True)
    unavailable = {r[0] for r in DB.query(USAGE, [KP, LEARNER], path, 'unavailable', basis)}
    unavailable.update(r[0] for r in DB.query(HISTORY, [KP, LEARNER], path, 'ever-shown', basis, history=True))
    retention = DB.query('[:find ?ident :in $ [?ident ...] :where [?a :db/ident ?ident] [?a :db/noHistory true]]', [[kw(a) for a in ('learner/activity', 'learner-task/items', 'task-item/content')]], path, 'history-retention', basis)
    assert not retention, 'Cannot establish freshness without retained presentations'
    known = {r['question'][':question/id']: r for p in OUT.glob('basis-*/generated.json') for r in json.loads(p.read_text())}
    tasks = {l: set() for l in LEVELS}
    ids = {l: [] for l in LEVELS}
    excluded, records = [], []
    for q in kp[':knowledge-point/questions']:
        sid = q.get(':question/math-academy-id')
        if sid:
            assert sid in g.QUESTIONS and normalize(q) == normalize(g.QUESTIONS[sid]), 'Source changed; reclassification required'
        level = normalize(q).get(':question/difficulty', '').split('/')[-1]
        if q[':db/id'] in unavailable or q.get(':knowledge-point/_canonical-example'):
            excluded.append({'question_id': str(q[':question/id']), 'reason': 'ever shown or reserved or canonical'})
            continue
        if level not in LEVELS or not all(':answer-field/correct' in f for f in q[':question/answer-fields']):
            excluded.append({'question_id': str(q[':question/id']), 'reason': 'unrated or missing correct answer'})
            continue
        if sid == 'q-167932':
            excluded.append({'question_id': str(q[':question/id']), 'reason': 'missing source diagram; full-equation blank grading unsupported'})
            continue
        if sid:
            r = g.generate(level, parameters=g.ORIGINAL[sid], profile='raw:' + sid)
            v.independent_from_display(r)
        else:
            r = known[str(q[':question/id'])]
            assert normalize(q) == normalize(localized_records([r])[0][0]['question'])
            validate_record(r)
        records.append(r)
        tasks[level].add(fingerprint(q))
        ids[level].append(str(q[':question/id']))
    native = run_native(records, path)
    result = {'basis': basis, 'distinct_available': {l: len(tasks[l]) for l in LEVELS}, 'question_ids': ids, 'excluded': excluded, 'unavailable_entity_ids': sorted(unavailable), 'native_grading': native}
    save(path / 'counts.json', result)
    return result


def transaction(records, kp, gid):
    forms = []
    for rec in records:
        q = rec['question']
        for f in q[':question/answer-fields']:
            for a in f[':answer-field/choices']:
                forms.append({kw('db/id'):a[':answer/id'], kw('answer/id'):uuid.UUID(a[':answer/id']), kw('answer/type'):kw(a[':answer/type']), kw('answer/value'):a[':answer/value'], kw('db/ensure'):kw('answer/validate')})
            forms.append({kw('db/id'):f[':answer-field/id'], kw('answer-field/id'):uuid.UUID(f[':answer-field/id']), kw('answer-field/key'):f[':answer-field/key'], kw('answer-field/type'):kw(f[':answer-field/type']), kw('answer-field/choices'):[a[':answer/id'] for a in f[':answer-field/choices']], kw('answer-field/correct'):f[':answer-field/correct'][1], kw('db/ensure'):kw('answer-field/validate')})
        forms.append({kw('db/id'):q[':question/id'], kw('question/id'):uuid.UUID(q[':question/id']), kw('question/problem'):q[':question/problem'], kw('question/worked-solution'):q[':question/worked-solution'], kw('question/difficulty'):kw(q[':question/difficulty']), kw('question/answer-fields'):[f[':answer-field/id'] for f in q[':question/answer-fields']], kw('db/ensure'):kw('question/validate')})
    gen = kp.get(':knowledge-point/question-generator')
    if gen is None:
        forms.extend([{kw('db/id'):'generator', kw('question-generator/id'):uuid.UUID(gid), kw('question-generator/script'):SCRIPT}, [kw('db/add'), KP, kw('knowledge-point/question-generator'), 'generator']])
    else:
        assert str(gen[':question-generator/id']) == gid and gen[':question-generator/script'] == SCRIPT
    if records:
        forms.append({kw('db/id'):KP, kw('knowledge-point/questions'):[r['question'][':question/id'] for r in records]})
    if forms:
        forms.append([kw('db/ensure'), KP, kw('knowledge-point/validate')])
    return forms


def check_report(report, path, source):
    attrs = {e:str(a) for e,a in DB.attributes(path, report[':edb/db-before-t'])}
    new = set(report[':edb/tempids'].values())
    allowed = {':question/id', ':question/problem', ':question/worked-solution', ':question/difficulty', ':question/answer-fields', ':answer-field/id', ':answer-field/key', ':answer-field/type', ':answer-field/choices', ':answer-field/correct', ':answer/id', ':answer/type', ':answer/value', ':question-generator/id', ':question-generator/script'}
    for e,a,value,tx,s,added in report[':edb/tx-data']:
        assert s == source and added, 'Unexpected attribution or retraction'
        name = attrs[a]
        if e == KP:
            assert name in (':knowledge-point/questions', ':knowledge-point/question-generator')
        elif name != ':db/txInstant':
            assert e in new and name in allowed, name


def localized_records(records):
    library = ImageLibrary(Path(ENV['EDB_MATH_ROOT']), HERE)
    result = copy.deepcopy(records)
    for r in result:
        for key in (':question/problem', ':question/worked-solution'):
            r['question'][key] = library.text(r['question'][key])
    for item in library.saved.values():
        assert sha(Path(ENV['EDB_MATH_ROOT']) / item['path']) == item['sha256']
    return result, library.saved


def verify(path, intent, report):
    assert report[':edb/committed'] is True and report[':edb/db-before-t'] == intent['basis']
    check_report(report, path / 'receipt-check', intent['source_eid'])
    basis = report[':edb/db-after-t']
    kp = read_kp(path / 'readback', basis)
    before = loads((path / 'before.edn').read_text())
    old = {q[':db/id']: q for q in before[':knowledge-point/questions']}
    now = {q[':db/id']: q for q in kp[':knowledge-point/questions']}
    assert all(now[e] == q for e, q in old.items()), 'Existing pool or source questions changed'
    assert {k: x for k, x in before.items() if k not in (':knowledge-point/questions', ':knowledge-point/question-generator')} == {k: x for k, x in kp.items() if k not in (':knowledge-point/questions', ':knowledge-point/question-generator')}
    gen = kp[':knowledge-point/question-generator']
    assert str(gen[':question-generator/id']) == intent['generator_id'] and gen[':question-generator/script'] == SCRIPT
    records = json.loads((path / 'generated.json').read_text())
    stored = json.loads((path / 'database-records.json').read_text())
    assert len(now) == len(old) + len(records)
    byid = {str(q[':question/id']): q for q in now.values()}
    for r in stored:
        q = byid[r['question'][':question/id']]
        assert ':question/math-academy-id' not in q and normalize(q) == normalize(r['question'])
    for r in records:
        validate_record(r)
    assert not transaction([], kp, intent['generator_id']), 'Repeat preparation must be empty'
    after = counts(kp, path / 'readback', basis)
    result = {'passed': True, 'basis_before': intent['basis'], 'basis_after': basis, 'new_questions': len(records), 'unchanged_source_questions': len(old), 'learner_history_unchanged': True, 'only_additive_scoped_content_datoms': True, 'configured_contributor_verified': True, 'generator_registration_verified': True, 'repeat_preparation_content_changes': 0, 'available_counts_after': after}
    save(path / 'verification.json', result)
    return result


def finish(path, gid, verified, inv):
    prep = json.loads((path / 'preparation.json').read_text())
    after = verified['available_counts_after']
    remaining = {l: max(0, 5 - after['distinct_available'][l]) for l in LEVELS}
    result = {'outcome': 'finite-limit' if any(remaining.values()) else 'generated', 'knowledgePoint': KP, 'generator_path': SCRIPT, 'generator_id': gid, 'lineage': LINEAGE, 'verified_commit_basis': verified['basis_after'], 'new_questions': verified['new_questions'], 'new_by_level': prep['new_by_level'], 'supported_levels': list(LEVELS), 'available_counts_before': prep['available_counts']['distinct_available'], 'available_counts_after': after['distinct_available'], 'shortage_remaining': remaining, 'unsupported_levels': [], 'unsupported_levels_filled': False, 'capability_exceptions': [{'response_shape': 'full-equation blank', 'supported': False, 'reason': 'Existing native symbolic grader returns unconsumed mathematical notation for full equations; source blank also lacks its diagram.', 'handling': 'Blank output remains evidence-only and is excluded from inventory. Supported radio fields are available at all three levels.'}], 'inventory_recheck_basis': inv['basis'], 'remaining_jobs': [j for j in inv['jobs'] if j['knowledgePoint'] == KP], 'evidence': [str(p.relative_to(ROOT)) for p in [path / 'verification.json', path / 'commit-intent.json', path / 'transaction.edn', path / 'commit.edn', path / 'preview.edn', path / 'preparation.json', path / 'inventory-after.json', path / 'native-report.json', path / 'review.md', path / 'visual-review.json', HERE / 'reference/initial/approved-package-verification.json', HERE / 'classification.md', HERE / 'template-extraction.md', HERE / 'validation.json', HERE / 'capabilities.json']], 'note': 'Original eight source questions and all learner history preserved. Moderate/hard are validated authored rational-number workloads within the same circle-equation substitution method. Unrated and malformed source records remain excluded.'}
    save(path / 'outcome.json', result)
    save(JOB.with_suffix('.result'), result)
    print(json.dumps({k: result[k] for k in ('outcome', 'verified_commit_basis', 'new_questions', 'available_counts_after', 'shortage_remaining')}), flush=True)


def prepare():
    inv = inventory(OUT / 'inventory-before.json')
    basis = inv['basis']
    assert DB.basis() == basis
    path = OUT / ('basis-' + str(basis))
    path.mkdir(exist_ok=True)
    kp = read_kp(path, basis)
    (path / 'before.edn').write_text(dumps(kp) + '\n')
    source = DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]', [], path, 'contributor', basis)
    assert len(source) == 1
    gen = kp.get(':knowledge-point/question-generator')
    script_matches = DB.query('[:find (pull ?g [*]) :in $ ?script :where [?g :question-generator/script ?script]]', [SCRIPT], path, 'generator-script', basis)
    assert len(script_matches) <= 1
    gid = str(gen[':question-generator/id']) if gen else str(script_matches[0][0][':question-generator/id']) if script_matches else str(uuid.uuid5(uuid.UUID(g.KP_UUID), 'question-generator'))
    identities = DB.query('[:find (pull ?g [*]) :in $ ?id :where [?g :question-generator/id ?id]]', [uuid.UUID(gid)], path, 'generator-identity', basis)
    assert not identities or identities[0][0][':question-generator/script'] == SCRIPT
    if gen:
        assert str(gen[':question-generator/id']) == gid and gen[':question-generator/script'] == SCRIPT
    c = counts(kp, path / 'counts-before', basis)
    needed = {l: max(0, 5 - c['distinct_available'][l]) for l in LEVELS}
    used = {fingerprint(q) for q in kp[':knowledge-point/questions']}
    used.add(fingerprint(kp[':knowledge-point/canonical-example']))
    supplied_path = JOB.with_suffix('.generated')
    supplied = json.loads(supplied_path.read_text()) if supplied_path.exists() else {}
    instances = supplied.get('instances', [])
    assert isinstance(instances, list)
    for r in instances:
        validate_record(r)
    save(path / 'supplied-status.json', {'exists': supplied_path.exists(), 'validated_instances': len(instances), 'generator_error': supplied.get('generatorError')})
    records = []
    added = {l: 0 for l in LEVELS}
    def accept(r):
        level = r['question'][':question/difficulty'].split('/')[-1]
        assert level in LEVELS
        fp = fingerprint(r['question'])
        if added[level] < needed[level] and fp not in used:
            validate_record(r)
            records.append(r)
            used.add(fp)
            added[level] += 1
    for r in instances:
        accept(r)
    # Only generate still-needed tasks. Distinct center and radius equations,
    # never seed, bank, choice-order, diagram-orientation, or identity aliases.
    for level in LEVELS:
        for seed in range(1000, 1500):
            if added[level] >= needed[level]:
                break
            accept(g.generate(level, seed=seed))
        assert added[level] == needed[level], 'Bounded search exhausted; leave explicit shortage before committing'
    ids = [uuid.UUID(i) for r in records for i in [r['question'][':question/id']] + [f[':answer-field/id'] for f in r['question'][':question/answer-fields']] + [a[':answer/id'] for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']]]
    matches = DB.query('[:find ?e ?id :in $ [?id ...] :where (or-join [?e ?id] [?e :question/id ?id] [?e :answer-field/id ?id] [?e :answer/id ?id])]', [ids], path, 'identity-matches', basis) if ids else []
    assert not matches, 'Existing generated identities require reconciliation'
    save(path / 'generated.json', records)
    native = run_native(records, path)
    stored, assets = localized_records(records)
    save(path / 'database-records.json', stored)
    save(path / 'assets.json', assets)
    (path / 'review.md').write_text('\n\n---\n\n'.join(g.markdown(r) for r in records) + '\n')
    prep = {'basis': basis, 'lineage': LINEAGE, 'source': SOURCE, 'available_counts': c, 'missing_by_level': needed, 'new_by_level': added, 'distinct_generated_tasks': len({fingerprint(r['question']) for r in records}), 'asset_hashes': assets, 'native_grading': native, 'source_evidence_unchanged': True, 'source_basis': g.SOURCE['basis'], 'generator_sha256': sha(HERE.with_suffix('.py')), 'capability_counts': json.loads((HERE / 'capabilities.json').read_text()), 'unsupported_full_equation_blanks_excluded': True}
    save(path / 'preparation.json', prep)
    print(json.dumps({'prepared_basis': basis, 'fresh_available': c['distinct_available'], 'new_by_level': added, 'native': native, 'generator_id': gid, 'review': str(path / 'review.md')}), flush=True)
    return path, kp, gid, source[0][0], stored, inv


def main():
    a = argparse.ArgumentParser()
    a.add_argument('--commit', action='store_true')
    args = a.parse_args()
    validation = json.loads((HERE / 'validation.json').read_text())
    freeze = json.loads((HERE / 'freeze.json').read_text())
    assert validation['passed'] and validation['native_radio_passed'] and freeze['generator_sha256'] == sha(HERE.with_suffix('.py'))
    preview = preview_executable(SimpleNamespace(math_root=Path(ENV['EDB_MATH_ROOT']), repo_root=ROOT, preview_bin=None), threading.Event()) if args.commit else None
    with (ROOT / '.local/learning/requests/math/api.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        for path in sorted(OUT.glob('basis-*')):
            if (path / 'commit-intent.json').exists():
                assert args.commit, 'Recover pending exact commit before new preparation'
                intent = json.loads((path / 'commit-intent.json').read_text())
                assert intent['database'] == 'math' and intent['lineage'] == LINEAGE and intent['source'] == SOURCE and intent['endpoint'] == DB.args.endpoint
                assert intent['connection_sha256'] == hashlib.sha256(ENV['EDB_POSTGRES_URL'].encode()).hexdigest()
                assert intent['exact_edn'] == (path / 'transaction.edn').read_text() and intent['sha256'] == sha(path / 'transaction.edn')
                report = DB._commit(intent, path / 'transaction.edn', path)
                verified = verify(path, intent, report)
                finish(path, intent['generator_id'], verified, inventory(path / 'inventory-after.json'))
                return
        path, kp, gid, source, records, inv = prepare()
        if not args.commit:
            return
        basis = inv['basis']
        assert DB.basis() == basis, 'Basis changed during preparation: repeat from current inventory'
        forms = transaction(records, kp, gid)
        if not forms:
            verified = {'passed': True, 'basis_before': basis, 'basis_after': basis, 'new_questions': 0, 'no_changes': True, 'available_counts_after': counts(kp, path / 'readback', basis)}
            save(path / 'verification.json', verified)
            finish(path, gid, verified, inv)
            return
        txpath = path / 'transaction.edn'
        tx = dumps(forms) + '\n'
        with txpath.open('w') as f:
            f.write(tx)
            f.flush()
            os.fsync(f.fileno())
        p = subprocess.run([str(preview), 'with', '--database', 'math', '--file', str(txpath), '--source', SOURCE], env=ENV, capture_output=True, text=True, check=True, timeout=90)
        (path / 'preview.edn').write_text(p.stdout)
        report = loads(p.stdout)
        assert report[':edb/committed'] is False and report[':edb/db-before-t'] == basis
        check_report(report, path / 'preview-check', source)
        assert DB.basis() == basis
        intent = {'database': 'math', 'endpoint': DB.args.endpoint, 'lineage': LINEAGE, 'source': SOURCE, 'source_eid': source, 'basis': basis, 'expected_basis': basis, 'request_key': 'circle-center-radius-inventory-' + str(KP) + '-' + str(basis) + '-' + sha(txpath), 'sha256': sha(txpath), 'transaction_sha256': sha(txpath), 'exact_edn': tx, 'generator_id': gid, 'generator_path': SCRIPT, 'generator_sha256': sha(HERE.with_suffix('.py')), 'question_uuids': [r['question'][':question/id'] for r in records], 'connection_sha256': hashlib.sha256(ENV['EDB_POSTGRES_URL'].encode()).hexdigest(), 'lock': str(ROOT / '.local/learning/requests/math/api.lock')}
        save(path / 'commit-intent.json', intent)
        report = DB._commit(intent, txpath, path)
        verified = verify(path, intent, report)
        finish(path, gid, verified, inventory(path / 'inventory-after.json'))


if __name__ == '__main__':
    main()
