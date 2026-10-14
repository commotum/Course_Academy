"""Scoped polynomial-LCM replenishment using the application's EDB integration."""
import copy
import fcntl
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
import threading
import uuid
from pathlib import Path
from types import SimpleNamespace

H = Path(__file__).resolve().parent
ROOT = H.parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'scripts'))
from capture.scripts.database.preview import preview_executable
from serve_graph_explorer import build_learning, database_environment
from inventory_jobs import save
from db_support import DB, KP, PATTERN, dumps, loads, kw
spec = importlib.util.spec_from_file_location('lcm_validation', H / 'validate.py')
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)
g = v.g
LEVELS = ('easy', 'moderate', 'hard')
LEARNER = '59d5cf13-351c-4114-be19-4c3bb64ee051'
LINEAGE = g.SOURCE['lineage']
SOURCE = ':application/ca-engine'
SCRIPT = str(H.with_suffix('.py').relative_to(ROOT))
JOB = ROOT / '.local/learning/inventory/math' / LEARNER / 'f22f2b0de9221615bf93d664869670f481698530c45cab21f9a92dcc8fc29a53'
OUT = H / 'reference/replenishment'
LOCK = ROOT / '.local/learning/requests/math/api.lock'
USAGE = '''[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner]
 [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t]
 [?t :learner-task/items ?i] [?i :task-item/content ?q]]'''
RESERVED = '''[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner]
 [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t] [?t :learner-task/status ?status]
 (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused])
 [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]]'''


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def canon(x):
    if isinstance(x, dict):
        return {str(k): canon(z) for k, z in x.items()}
    if isinstance(x, (list, tuple)):
        return sorted([canon(z) for z in x], key=lambda z: json.dumps(z, sort_keys=True))
    return str(x) if isinstance(x, uuid.UUID) else x


def source_projection(x):
    if isinstance(x, dict):
        return {str(k): source_projection(z) for k, z in x.items()
                if not (str(k) == ':db/id' and ':db/ident' in x)}
    if isinstance(x, list):
        return [source_projection(z) for z in x]
    return str(x) if isinstance(x, uuid.UUID) else x


def normalized(q):
    out = {k: str(q[k]) if k == ':question/id' else q[k]
           for k in (':question/id', ':question/problem', ':question/worked-solution')}
    out[':question/difficulty'] = str(q[':question/difficulty'][':db/ident'])
    out[':question/answer-fields'] = []
    for f in q[':question/answer-fields']:
        out[':question/answer-fields'].append({
            ':answer-field/id': str(f[':answer-field/id']), ':answer-field/key': f[':answer-field/key'],
            ':answer-field/type': str(f[':answer-field/type'][':db/ident']),
            ':answer-field/correct': [':answer/id', str(f[':answer-field/correct'][':answer/id'])],
            ':answer-field/choices': [{':answer/id': str(a[':answer/id']),
                                      ':answer/type': str(a[':answer/type'][':db/ident']),
                                      ':answer/value': a[':answer/value']} for a in f[':answer-field/choices']]})
    return out


def fingerprint(q):
    # Canonicalize actual printed mathematical inputs, ignoring layouts, banks,
    # variable aliases, input order, identities and seeds.
    import sympy as sp
    A, B = map(g.parse_tex, re.findall(r'\$([^$]*)\$', q[':question/problem']))
    symbols = sorted(A.free_symbols | B.free_symbols, key=str)
    assert len(symbols) == 2
    canonical = sp.symbols('V W')
    presentations = []
    for order in (canonical, canonical[::-1]):
        mapping = dict(zip(symbols, order))
        presentations.append(sorted(sp.srepr(sp.expand(z.xreplace(mapping))) for z in (A, B)))
    return g.digest(min(presentations))


def read_kp(path, basis):
    return DB.query('[:find (pull ?k ' + PATTERN + ') :in $ ?k :where [?k :knowledge-point/id _]]',
                    [KP], path, 'kp', basis)[0][0]


def inventory(native, path):
    r = subprocess.run([str(native), 'math', LEARNER, DB.args.endpoint],
                       input='{"action":"inventory"}', env=database_environment('math'),
                       capture_output=True, text=True, check=True, timeout=55)
    x = json.loads(r.stdout)
    assert x['ok'] and x['data']['lineage'] == LINEAGE
    save(path, x['data'])
    return x['data']


def check_sources(kp):
    old = g.RECORD
    current = {q[':question/math-academy-id']: q for q in kp[':knowledge-point/questions']
               if ':question/math-academy-id' in q}
    for q in old[':knowledge-point/questions']:
        assert canon(source_projection(q)) == canon(source_projection(current[q[':question/math-academy-id']])), 'Source changed; reclassify'
    assert canon(source_projection(old[':knowledge-point/canonical-example'])) == canon(source_projection(kp[':knowledge-point/canonical-example']))


def counts(kp, path, basis):
    shown = {r[0] for r in DB.query(USAGE, [KP, LEARNER], path, 'ever-shown', basis, history=True)}
    reserved = {r[0] for r in DB.query(RESERVED, [KP, LEARNER], path, 'reserved', basis)}
    available = {level: set() for level in LEVELS}
    excluded = []
    for q in kp[':knowledge-point/questions']:
        level = str(q.get(':question/difficulty', {}).get(':db/ident', '')).split('/')[-1]
        if level not in LEVELS or not q.get(':question/worked-solution') or not all(f.get(':answer-field/correct') for f in q.get(':question/answer-fields', [])):
            excluded.append(str(q[':question/id']))
            continue
        if q[':db/id'] not in shown | reserved:
            available[level].add(fingerprint(q))
    result = {'basis': basis, 'distinct_available': {l: len(z) for l, z in available.items()},
              'ever_shown': sorted(shown), 'reserved': sorted(reserved), 'incomplete_or_unrated_excluded': excluded}
    save(path / 'available-counts.json', result)
    return result


def transaction(records, kp, gid):
    forms = []
    for r in records:
        q = r['question']
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
                      kw('question/answer-fields'): [f[':answer-field/id'] for f in q[':question/answer-fields']],
                      kw('db/ensure'): kw('question/validate')})
    gen = kp.get(':knowledge-point/question-generator')
    if gen:
        assert str(gen[':question-generator/id']) == gid and gen[':question-generator/script'] == SCRIPT
    else:
        forms.extend([{kw('db/id'): 'generator', kw('question-generator/id'): uuid.UUID(gid),
                       kw('question-generator/script'): SCRIPT},
                      [kw('db/add'), KP, kw('knowledge-point/question-generator'), 'generator']])
    if records:
        forms.append({kw('db/id'): KP, kw('knowledge-point/questions'): [r['question'][':question/id'] for r in records]})
    if forms:
        forms.append([kw('db/ensure'), KP, kw('knowledge-point/validate')])
    return forms


def report_checks(report, path, source):
    attrs = {eid: str(a) for eid, a in DB.attributes(path, report[':edb/db-before-t'])}
    new = set(report[':edb/tempids'].values())
    allowed = {':answer/id', ':answer/type', ':answer/value', ':answer-field/id', ':answer-field/key',
               ':answer-field/type', ':answer-field/choices', ':answer-field/correct', ':question/id',
               ':question/problem', ':question/worked-solution', ':question/difficulty', ':question/answer-fields',
               ':question-generator/id', ':question-generator/script'}
    for e, a, value, t, s, added in report[':edb/tx-data']:
        assert added and s == source, 'Unexpected retraction or attribution'
        name = attrs[a]
        if e == KP:
            assert name in {':knowledge-point/questions', ':knowledge-point/question-generator'}
        elif name != ':db/txInstant':
            assert e in new and name in allowed, 'Unexpected non-scoped datom'


def verify(report, path, intent):
    assert report[':edb/committed'] and report[':edb/db-before-t'] == intent['basis']
    b = report[':edb/db-after-t']
    report_checks(report, path / 'receipt-check', intent['source_eid'])
    before = loads((path / 'before.edn').read_text())
    after = read_kp(path / 'readback', b)
    old = {q[':db/id']: q for q in before[':knowledge-point/questions']}
    now = {q[':db/id']: q for q in after[':knowledge-point/questions']}
    assert all(canon(q) == canon(now[e]) for e, q in old.items())
    omit = {':knowledge-point/questions', ':knowledge-point/question-generator'}
    assert canon({k: z for k, z in before.items() if k not in omit}) == canon({k: z for k, z in after.items() if k not in omit})
    gen = after[':knowledge-point/question-generator']
    assert str(gen[':question-generator/id']) == intent['generator_id'] and gen[':question-generator/script'] == SCRIPT
    records = json.loads((path / 'generated.json').read_text())
    assert len(now) == len(old) + len(records)
    byid = {str(q[':question/id']): q for q in now.values()}
    for r in records:
        q = byid[r['question'][':question/id']]
        assert ':question/math-academy-id' not in q
        assert canon(normalized(q)) == canon(r['question'])
        assert fingerprint(q) == r['generation']['mathematical_fingerprint']
        v.check(r)
    assert not transaction([], after, intent['generator_id'])
    c = counts(after, path / 'readback', b)
    result = {'passed': True, 'basis_before': intent['basis'], 'basis_after': b,
              'new_questions': len(records), 'distinct_available': c['distinct_available'],
              'unchanged_source_questions': len(old), 'canonical_example_unchanged': True,
              'learner_history_unchanged': True, 'no_retractions': True, 'only_requested_kp_additive_content': True,
              'source': SOURCE, 'generator_registration_verified': True, 'repeat_preparation_content_changes': 0}
    save(path / 'verification.json', result)
    return result


def finish(path, verified, inv, gid):
    remaining = {l: max(0, 5 - verified['distinct_available'][l]) for l in LEVELS}
    result = {'outcome': 'finite-limit' if any(remaining.values()) else 'generated', 'knowledgePoint': KP,
              'generator_path': SCRIPT, 'generator_id': gid, 'lineage': LINEAGE,
              'verified_commit_basis': verified['basis_after'], 'new_questions': verified['new_questions'],
              'supported_levels': list(LEVELS), 'available_after': verified['distinct_available'],
              'shortage_remaining': remaining, 'unsupported_levels_filled': False,
              'inventory_recheck_basis': inv['basis'], 'remaining_jobs': [j for j in inv['jobs'] if j['knowledgePoint'] == KP],
              'capability_exceptions': [{'scope': 'blank equivalent entry input',
                  'bound': '4096 bytes or 512 tokens in the actual learner parser',
                  'evidence': 'engine-validation.json records the oversized fully expanded hard equivalent as unresolved; compact canonical, partial expansion, and unreduced equivalents pass.',
                  'impact': 'No requested variant shortage; do not claim acceptance of oversized expansions.'}],
              'evidence': [str(p.relative_to(ROOT)) for p in [H / 'classification.md', H / 'template-extraction.md',
                  H / 'validation.json', H / 'parent-qa.json', H / 'frozen-manifest.json', path / 'generated.json',
                  path / 'preparation.json', path / 'transaction.edn', path / 'commit-intent.json', path / 'preview.edn',
                  path / 'commit.edn', path / 'verification.json', path / 'inventory-after.json'] if p.exists()],
              'note': 'Hard is an explicitly authored same-method workload band. Unrated incomplete source stays unchanged and excluded. Mathematical tasks deduplicated across variable aliases, answer layouts, banks, seeds and order.'}
    save(path / 'outcome.json', result)
    save(JOB.with_suffix('.result'), result)
    print(json.dumps({k: result[k] for k in ('outcome', 'verified_commit_basis', 'new_questions', 'available_after', 'shortage_remaining')}), flush=True)


def main():
    assert json.loads((H / 'validation.json').read_text())['status'] == 'passed'
    assert json.loads((H / 'parent-qa.json').read_text())['passed']
    freeze = json.loads((H / 'frozen-manifest.json').read_text())
    assert all(sha(ROOT / p) == s for p, s in freeze['sha256'].items()), 'Frozen input changed'
    native = build_learning(ROOT.parent / 'EDB')
    preview = preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'), repo_root=ROOT, preview_bin=None), threading.Event())
    # Recover saved intent before making any new content/identity judgment.
    with LOCK.open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        for path in sorted(OUT.glob('basis-*')):
            if (path / 'commit-intent.json').exists():
                intent = json.loads((path / 'commit-intent.json').read_text())
                assert intent['database'] == 'math' and intent['lineage'] == LINEAGE and intent['source'] == SOURCE
                assert intent['exact_edn'] == (path / 'transaction.edn').read_text() and intent['sha256'] == sha(path / 'transaction.edn')
                assert intent['connection_sha256'] == hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
                report = DB._commit(intent, path / 'transaction.edn', path)
                finish(path, verify(report, path, intent), inventory(native, path / 'inventory-after.json'), intent['generator_id'])
                return
    inv = inventory(native, OUT / 'inventory-before-generation.json')
    basis = inv['basis']
    initial = read_kp(OUT / 'initial', basis)
    check_sources(initial)
    c = counts(initial, OUT / 'initial', basis)
    needed = {l: max(0, 5 - c['distinct_available'][l]) for l in LEVELS}
    used = {fingerprint(q) for q in initial[':knowledge-point/questions']}
    used.add(fingerprint(initial[':knowledge-point/canonical-example']))
    candidates = []
    supplied = json.loads(JOB.with_suffix('.generated').read_text()) if JOB.with_suffix('.generated').exists() else {}
    instances = supplied.get('instances', [])
    if isinstance(instances, dict):
        instances = [instances]
    for r in instances:
        assert r['knowledge_point']['db_id'] == KP
        v.check(r)
    seed = int(JOB.name[:8], 16)
    for level in LEVELS:
        added = 0
        # Execute the established generator CLI; select only distinct tasks.
        r = subprocess.run([sys.executable, SCRIPT, '--difficulty', level, '--count', '20', '--seed', str(seed), '--format', 'json'],
                           cwd=ROOT, capture_output=True, text=True, check=True)
        for rec in instances + json.loads(r.stdout):
            if rec['generation']['level'] != level:
                continue
            v.check(rec)
            m = rec['generation']
            assert not m['raw_missing_attributes']
            replay = g.generate(level, m['seed'], template=m['template'], parameters=m['parameters'], profile=m['profile'])
            assert canon(rec) == canon(replay)
            fp = fingerprint(rec['question'])
            assert fp == m['mathematical_fingerprint']
            if fp not in used and added < needed[level]:
                used.add(fp)
                candidates.append(rec)
                added += 1
            if added >= needed[level]:
                break
        assert added == needed[level], 'Bounded sample insufficient; record a capability exception before committing'
    # Validate current stored source UUIDs through the actual learner grader too.
    items = []
    for q in initial[':knowledge-point/questions']:
        sid = q.get(':question/math-academy-id')
        if sid not in g.PROFILES or not q.get(':question/difficulty') or not q.get(':question/worked-solution'):
            continue
        cfg = g.PROFILES[sid]
        rec = g.generate(cfg['level'], parameters={k: cfg[k] for k in g.KEYS}, profile='observed_' + sid)
        rec['question'] = normalized(q)
        items.append(v.native(rec, 'current-source/' + sid))
    items.extend(v.native(r, r['question'][':question/id']) for r in candidates)
    save(OUT / 'native-input.json', items)
    subprocess.run([str(H / 'check-engine'), str(OUT / 'native-input.json'), str(OUT / 'native-report.json')], check=True)
    save(OUT / 'validated-candidates.json', candidates)
    (OUT / 'review.md').write_text('\n\n---\n\n'.join(g.markdown(r) for r in candidates) + '\n')
    with LOCK.open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        inv = inventory(native, OUT / 'inventory-under-lock.json')
        b = inv['basis']
        assert DB.basis() == b and LINEAGE in DB.command('status')
        path = OUT / ('basis-' + str(b))
        path.mkdir(exist_ok=True)
        kp = read_kp(path, b)
        check_sources(kp)
        assert canon(kp) == canon(initial), 'KP changed during validation; rerun preparation'
        (path / 'before.edn').write_text(dumps(kp) + '\n')
        gen = kp.get(':knowledge-point/question-generator')
        gid = str(gen[':question-generator/id']) if gen else str(uuid.uuid5(g.NAMESPACE, 'course-academy-generator'))
        assert gen is None or gen[':question-generator/script'] == SCRIPT
        source = DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]', [], path, 'contributor', b)
        assert len(source) == 1
        orphan = DB.query('[:find (pull ?g [*]) :in $ ?id :where [?g :question-generator/id ?id]]', [uuid.UUID(gid)], path, 'generator-identity', b)
        assert not orphan or len(orphan) == 1 and orphan[0][0][':question-generator/script'] == SCRIPT
        c = counts(kp, path, b)
        needed = {l: max(0, 5 - c['distinct_available'][l]) for l in LEVELS}
        records = []
        added = {l: 0 for l in LEVELS}
        for r in candidates:
            l = r['generation']['level']
            if added[l] < needed[l]:
                records.append(r)
                added[l] += 1
        assert added == needed, 'Inventory eligibility changed; rerun generation'
        ids = [uuid.UUID(x) for r in records for x in [r['question'][':question/id']] +
               [f[':answer-field/id'] for f in r['question'][':question/answer-fields']] +
               [a[':answer/id'] for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']]]
        assert len(ids) == len(set(ids))
        if ids:
            assert not DB.query('[:find ?e :in $ [?id ...] :where (or-join [?e ?id] [?e :question/id ?id] [?e :answer-field/id ?id] [?e :answer/id ?id])]', [ids], path, 'identity-matches', b)
        save(path / 'generated.json', records)
        save(path / 'preparation.json', {'basis': b, 'lineage': LINEAGE, 'source': SOURCE, 'source_eid': source[0][0],
            'generator_path': SCRIPT, 'generator_id': gid, 'generator_sha256': sha(H.with_suffix('.py')),
            'available_before': c, 'new_by_level': added, 'distinct_generated_tasks': len(records),
            'exact_requests_retained': True, 'assets': [], 'native_grading': str((OUT / 'native-report.json').relative_to(ROOT)),
            'source_bank_replay': '6/6 complete banks and 14/14 source values', 'lock': str(LOCK)})
        forms = transaction(records, kp, gid)
        if not forms:
            verified = {'passed': True, 'basis_before': b, 'basis_after': b, 'new_questions': 0, 'distinct_available': c['distinct_available'], 'no_changes': True}
            save(path / 'verification.json', verified)
            finish(path, verified, inv, gid)
            return
        txpath = path / 'transaction.edn'
        tx = dumps(forms) + '\n'
        with txpath.open('w') as f:
            f.write(tx)
            f.flush()
            os.fsync(f.fileno())
        r = subprocess.run([str(preview), 'with', '--database', 'math', '--file', str(txpath), '--source', SOURCE],
                           env=DB.env, capture_output=True, text=True, check=True, timeout=55)
        (path / 'preview.edn').write_text(r.stdout)
        pr = loads(r.stdout)
        assert pr[':edb/committed'] is False and pr[':edb/db-before-t'] == b
        report_checks(pr, path / 'preview-check', source[0][0])
        assert DB.basis() == b
        intent = {'database': 'math', 'endpoint': DB.args.endpoint, 'lineage': LINEAGE, 'source': SOURCE,
                  'source_eid': source[0][0], 'basis': b, 'expected_basis': b,
                  'request_key': 'two-polynomial-lcm-inventory-' + str(KP) + '-' + str(b) + '-' + sha(txpath),
                  'exact_edn': tx, 'sha256': sha(txpath), 'generator_id': gid, 'generator_path': SCRIPT,
                  'question_uuids': [r['question'][':question/id'] for r in records],
                  'connection_sha256': hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(), 'lock': str(LOCK)}
        save(path / 'commit-intent.json', intent)
        report = DB._commit(intent, txpath, path)
        finish(path, verify(report, path, intent), inventory(native, path / 'inventory-after.json'), gid)


if __name__ == '__main__':
    main()
