"""Withdraw unused all-false generated questions; preserve all learner history."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import copy
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import uuid
sys.dont_write_bytecode = True
ROOT = next(p for p in Path(__file__).resolve().parents if (p / 'Cargo.toml').exists())
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'reference/edb-math/repairs/2026-10-16-checkbox-statement-labels'))
from audit_scope import PATTERNS, KP, SOURCE
from scripts.generator_publish import Publisher
from scripts.generator_packages import resolve_registered_script
from capture.scripts.database.edn import dumps, loads, kw, Tagged
from capture.scripts.database.client import StaleBasis

HERE = Path(__file__).resolve().parent
PUBLISHER = Publisher.from_environment(source=SOURCE)
DB = PUBLISHER.client
NATIVE = ROOT / 'reference/edb-math/imports/authored-checkboxes/2026-10-16/lesson-17592186492056/native/preview'

def save(path, value): path.write_text(json.dumps(value, indent=2, default=str) + '\n')
def normalize(value):
    if isinstance(value, dict): return {str(k): normalize(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, set)): return sorted((normalize(v) for v in value), key=lambda v: json.dumps(v, sort_keys=True))
    return str(value) if isinstance(value, uuid.UUID) else value

def prepare(directory):
    identity = DB.status()
    basis = identity['basis']
    def read(name, query, inputs): return DB.query(query, inputs, directory / 'evidence', name, basis)
    scope = read('scope', '[:find (pull ?kp ' + PATTERNS['scope'] + ') :in $ ?kp :where [?kp :knowledge-point/id _]]', [KP])
    kp = scope[0][0]
    generator = kp[':knowledge-point/question-generator']
    path = resolve_registered_script(generator[':question-generator/script'], ROOT, PUBLISHER.config.math_root)
    checked = json.loads((HERE / 'generator-verification.json').read_text())
    generator_sha = hashlib.sha256(path.read_bytes()).hexdigest()
    assert generator_sha == '4fbf0b567cc05bb4ff3b6c8f102f089406874769b5638b4ae06f058906bdefb5'
    ids = sorted({q[':db/id'] for q in kp[':knowledge-point/questions']} | {kp[':knowledge-point/canonical-example'][':db/id']})
    queries = {
        'questions': ('[:find (pull ?q ' + PATTERNS['questions'] + ') :in $ [?q ...] :where [?q :question/id _]]', [ids]),
        'items': ('[:find ?q (pull ?i ' + PATTERNS['items'] + ') :in $ [?q ...] :where [?i :task-item/content ?q]]', [ids]),
        'attributes': ('[:find ?a ?ident :where [?a :db/ident ?ident] [?a :db/valueType _]]', []),
        'source': ('[:find ?s :in $ ?ident :where [?s :db/ident ?ident]]', [kw(SOURCE)]),
    }
    with ThreadPoolExecutor(max_workers=3) as pool:
        futures = {name: pool.submit(read, name, *args) for name, args in queries.items()}
        data = {name: future.result() for name, future in futures.items()}
    assert len(data['source']) == 1
    audit, candidates, target_owner = [], {}, {}
    for [q] in data['questions']:
        if not q.get(':question/answer-fields'): continue
        matrices = re.findall(r'([A-Z])=\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}', q[':question/problem'], re.S)
        dims = {name: (len(body.split(r'\\')), len(body.split(r'\\')[0].split('&'))) for name, body in matrices}
        products, truth = [], []
        for field in q[':question/answer-fields']:
            match = re.fullmatch(r'The product \$([A-Z])([A-Z])\$ is well defined\.', field[':answer-field/key'])
            if not match:
                assert field[':answer-field/key'] == 'None of these products is well defined.'
                continue
            good = dims[match[1]][1] == dims[match[2]][0]
            assert field[':answer-field/correct'][':answer/value'] == str(good).lower()
            products.append(match[1] + match[2]); truth.append(good)
        assert len(products) == 3
        row = {'question': q[':db/id'], 'source_id': q.get(':question/math-academy-id'), 'products': products, 'truth': truth, 'all_false': not any(truth)}
        audit.append(row)
        if row['source_id'] is None and row['all_false']:
            assert not q.get(':knowledge-point/_canonical-example')
            candidates[q[':db/id']] = q
            for entity in [q, *q[':question/answer-fields'], *(a for f in q[':question/answer-fields'] for a in f[':answer-field/choices'])]:
                target_owner[entity[':db/id']] = q[':db/id']
    targets = [Tagged('edb/ref', e) for e in sorted(target_owner)]
    query = '[:find ?e ?a ?target :in $ [?target ...] :where [?e ?a ?target]]'
    current = read('incoming', query, [targets]) if targets else []
    historical = []
    if targets:
        history_query = '[:find ?e ?a ?target ?tx ?source ?added :in $ [?target ...] :where [?e ?a ?target ?tx ?source ?added]]'
        qfile, ifile = directory / 'history-query.edn', directory / 'history-inputs.edn'
        qfile.write_text(history_query + '\n'); ifile.write_text(dumps([targets]) + '\n')
        text = DB.command('query', '--file', qfile, '--inputs', ifile, '--as-of', basis, '--history', timeout=60)
        (directory / 'history.edn').write_text(text)
        historical = loads(text)
    names = dict(data['attributes'])
    uses = {qid: [] for qid in candidates}
    structural = {':knowledge-point/questions', ':question/answer-fields', ':answer-field/choices', ':answer-field/correct'}
    for origin, rows in [('current', current), ('history', historical)]:
        for row in rows:
            e, a, target = row[:3]
            attr = str(names[a])
            if attr not in structural:
                uses[target_owner[target]].append({'origin': origin, 'entity': e, 'attribute': attr, 'target': target})
            elif attr == ':knowledge-point/questions':
                assert e == KP, 'Question has another KP membership'
    retired = sorted(qid for qid in candidates if not uses[qid])
    retained = sorted(set(candidates) - set(retired))
    for qid in retired:
        assert all(owner != qid for owner, _ in data['items'])
    forms = [[kw('db/retract'), KP, kw('knowledge-point/questions'), qid] for qid in retired]
    if forms: forms.append([kw('db/ensure'), KP, kw('knowledge-point/validate')])
    (directory / 'transaction.edn').write_text(dumps(forms) + '\n')
    groups = [['scope', PATTERNS['scope'], [KP]], ['questions', PATTERNS['questions'], ids], ['items', PATTERNS['items'], sorted(i[':db/id'] for _, i in data['items'])]]
    (directory / 'native-pulls.edn').write_text(dumps(groups) + '\n')
    (directory / 'snapshot.edn').write_text(dumps({**identity, **data, 'scope': scope, 'incoming': current, 'historical_incoming': historical}) + '\n')
    sha = hashlib.sha256((directory / 'transaction.edn').read_bytes()).hexdigest()
    plan = {**identity, 'source': SOURCE, 'source_eid': data['source'][0][0], 'attributes': names, 'audited': audit, 'retired': retired, 'retained_used': retained, 'uses': uses, 'generator_path': str(path), 'generator_sha256': generator_sha, 'sha256': sha, 'request_key': f'retire-unused-conformability-empty-b{basis}-{sha}', 'endpoint': DB.config.endpoint, 'transaction_file': str(directory / 'transaction.edn')}
    save(directory / 'plan.json', plan)
    return plan

def verify_report(report, plan, committed):
    assert report[':edb/committed'] is committed and report[':edb/db-before-t'] == plan['basis']
    expected = {(KP, ':knowledge-point/questions', qid, False) for qid in plan['retired']}
    actual = set()
    for e, a, v, tx, source, added in report[':edb/tx-data']:
        assert source == plan['source_eid']
        attr = str(plan['attributes'][str(a)])
        if attr == ':db/txInstant': assert added
        else: actual.add((e, attr, v, added))
    assert actual == expected

def preview(directory, plan):
    run = subprocess.run([str(NATIVE), str(directory), SOURCE, str(plan['basis'])], env=DB.environment, capture_output=True, text=True, timeout=150)
    (directory / 'preview.stderr').write_text(run.stderr)
    run.check_returncode()
    (directory / 'preview.edn').write_text(run.stdout)
    # Normalize the JSON map keys exactly as they will be after request recovery.
    plan = json.loads((directory / 'plan.json').read_text())
    verify_report(loads(run.stdout), plan, False)
    for name in ('scope', 'questions', 'items'):
        before = loads((directory / f'preview-{name}-before.edn').read_text())
        after = loads((directory / f'preview-{name}-after.edn').read_text())
        expected = copy.deepcopy(before)
        if name == 'scope': expected[0][':knowledge-point/questions'] = [q for q in expected[0][':knowledge-point/questions'] if q[':db/id'] not in plan['retired']]
        if name == 'questions':
            for q in expected:
                if q[':db/id'] in plan['retired']:
                    q.pop(':knowledge-point/_questions', None)
        assert normalize(expected) == normalize(after), name
    save(directory / 'preview-verification.json', {'passed': True, 'only_practice_memberships_retracted': plan['retired'], 'all_content_and_learner_items_preserved': True, 'current_and_retained_history_usage_checked': True})

def execute(directory, commit):
    directory.mkdir(exist_ok=True)
    intent = directory / 'commit-intent.json'
    if intent.exists():
        plan = json.loads(intent.read_text())
    else:
        if not (directory / 'preview-verification.json').exists():
            plan = prepare(directory)
            if not plan['retired']:
                save(directory / 'verification.json', {'committed': False, 'no_unused_all_false_questions': True, 'retained_used': plan['retained_used']})
                print(json.dumps({'retired': [], 'retained_used': plan['retained_used']})); return
            preview(directory, plan)
        plan = json.loads((directory / 'plan.json').read_text())
        if not commit:
            print(json.dumps({'prepared': True, 'basis': plan['basis'], 'retired': plan['retired'], 'retained_used': plan['retained_used'], 'questions_audited': len(plan['audited'])})); return
        save(intent, plan)
    assert hashlib.sha256((directory / 'transaction.edn').read_bytes()).hexdigest() == plan['sha256']
    assert DB.status()['lineage'] == plan['lineage']
    receipt = directory / 'receipt.edn'
    if not receipt.exists():
        try:
            text = DB.command('transact', '--source', SOURCE, '--file', plan['transaction_file'], '--basis', plan['basis'], '--endpoint', plan['endpoint'], '--request-key', plan['request_key'], '--timeout-ms', '120000', timeout=150)
        except StaleBasis as error:
            save(directory / 'rejected.json', {'confirmed_stale_basis': True, 'reason': str(error)}); raise
        receipt.write_text(text)
    report = loads(receipt.read_text()); verify_report(report, plan, True)
    basis = report[':edb/db-after-t']
    def verify_group(group):
        name, pattern, ids = group
        query = '[:find (pull ?e ' + pattern + ') :in $ [?e ...] :where [?e _ _]]'
        for at, stage in [(basis, 'after'), (plan['basis'], 'before')]:
            rows = DB.query(query, [ids], directory / 'readback', name + '-' + stage, at)
            expected = loads((directory / f'preview-{name}-{stage}.edn').read_text())
            assert normalize([q for [q] in rows]) == normalize(expected), (name, stage)
    with ThreadPoolExecutor(max_workers=3) as pool:
        list(pool.map(verify_group, loads((directory / 'native-pulls.edn').read_text())))
    assert hashlib.sha256(Path(plan['generator_path']).read_bytes()).hexdigest() == plan['generator_sha256']
    result = {'committed': True, 'lineage': plan['lineage'], 'basis_before': plan['basis'], 'basis_after': basis, 'retired_unused_questions': plan['retired'], 'preserved_attempted_questions': plan['retained_used'], 'questions_audited': len(plan['audited']), 'source': SOURCE, 'request_key': plan['request_key'], 'transaction_sha256': plan['sha256'], 'exact_committed_and_historical_readback': True, 'only_practice_pool_memberships_retracted': True, 'question_content_and_learner_state_preserved': True, 'generator_sha256': plan['generator_sha256'], 'generator_verification': str((HERE / 'generator-verification.json').relative_to(ROOT)), 'evidence_directory': str(directory.relative_to(ROOT))}
    save(directory / 'verification.json', result); save(HERE / 'verification.json', result); print(json.dumps(result))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--attempt', required=True); parser.add_argument('--commit', action='store_true')
    args = parser.parse_args(); execute(HERE / args.attempt, args.commit)
