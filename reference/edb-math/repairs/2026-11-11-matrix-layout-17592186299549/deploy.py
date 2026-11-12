"""Apply reviewed matrix-layout repairs with durable CAS and exact readback."""
import copy
import json
import sys
from contextlib import ExitStack
from pathlib import Path

H = Path(__file__).resolve().parent
ROOT = H.parents[3]
sys.path.insert(0, str(ROOT))
from scripts.generator_publish import Publisher, QUESTION_PULL, StaleBasis, digest, dumps, loads, kw, file_lock, jsonable
from capture.scripts.database.commit import Committer
from capture.scripts.storage import atomic_json


def read_questions(p, ids, directory, label, basis):
    return [r[0] for r in p.client.query(
        '[:find (pull ?q ' + QUESTION_PULL + ') :in $ [?q ...] :where [?q :question/id _]]',
        [ids], directory, label, basis)]


def patch(value, proposals):
    result = copy.deepcopy(value)
    def walk(v):
        if isinstance(v, dict):
            for row in proposals:
                key = kw(row['attribute'])
                if v.get(':db/id') == row['entity'] and key in v:
                    assert v[key] == row['before']
                    v[key] = row['after']
            for child in v.values():
                walk(child)
        elif isinstance(v, list):
            for child in v:
                walk(child)
    walk(result)
    return result


def canonical(value):
    if isinstance(value, dict):
        return {str(k): canonical(v) for k, v in value.items()}
    if isinstance(value, list):
        return sorted([canonical(v) for v in value], key=lambda v: dumps(v))
    return value


def prepare(p, work, rows, kps):
    status = p.client.status()
    basis = status['basis']
    before = read_questions(p, sorted({r['entity'] for r in rows}), work, 'before', basis)
    assert len(before) == len({r['entity'] for r in rows})
    expected = patch(before, rows)
    parents = {str(k): p.read_kp(k, work/'kp-before'/str(k), basis) for k in kps}
    attrs = p.client.query('[:find ?a ?ident ?type :where [?a :db/ident ?ident] [?a :db/valueType ?v] [?v :db/ident ?type]]', [], work, 'attributes', basis)
    idents = p.client.query('[:find ?e ?ident :where [?e :db/ident ?ident]]', [], work, 'idents', basis)
    forms = [[kw('db/cas'), r['entity'], kw(r['attribute']), r['before'], r['after']] for r in rows]
    forms += [[kw('db/ensure'), q[':db/id'], kw('question/validate')] for q in before]
    batch = {'source': p.config.source, 'forms': forms,
             'assertions': [[r['entity'], kw(r['attribute']), r['after']] for r in rows],
             'retractions': [[r['entity'], kw(r['attribute']), r['before']] for r in rows]}
    snapshot = {'basis': basis, 'lineage': status['lineage'], 'attributes': attrs, 'idents': idents}
    prepared = {'before_edn': dumps(before), 'expected_edn': dumps(expected), 'parents_edn': dumps(parents),
                'rows': rows, 'batch_edn': dumps(batch), 'snapshot_edn': dumps(snapshot)}
    atomic_json(work/'preparation.json', prepared)
    c = Committer(p.config, p.client, work)
    c.preview(batch, snapshot)
    return prepared, c, c.save_request(batch, snapshot, digest(prepared))


def apply(p, work, prepared, c, request):
    assert request['content_sha256'] == digest(prepared)
    receipt = c.submit(request)
    proof = c.verify_receipt(request, receipt)
    basis = receipt[':edb/db-after-t']
    before = loads(prepared['before_edn'])
    ids = sorted(q[':db/id'] for q in before)
    after = read_questions(p, ids, work, 'after', basis)
    assert canonical(after) == canonical(loads(prepared['expected_edn']))
    historical = read_questions(p, ids, work, 'historical', request['basis'])
    assert canonical(historical) == canonical(before)
    for kp, parent in loads(prepared['parents_edn']).items():
        now = p.read_kp(int(kp), work/'kp-after'/kp, basis)
        assert canonical(now) == canonical(patch(parent, prepared['rows']))
    result = {'passed': True, 'committed': True, 'questions_repaired': len(ids),
              'basis_before': request['basis'], 'basis_after': basis,
              'only_reviewed_problem_layouts_changed': True,
              'answer_fields_keys_solutions_identities_and_history_preserved': True, **proof}
    atomic_json(work/'verification.json', result)
    atomic_json(work/'after.json', jsonable(canonical(after)))
    c.retire(request, 'verified', result)
    print(json.dumps(result, indent=2))


def main():
    stage = sys.argv[1] if len(sys.argv) > 1 else 'initial'
    rows = json.loads((H/('proposals.json' if stage == 'initial' else stage+'-proposals.json')).read_text())
    kps = json.loads((H/(stage+'-kps.json')).read_text())
    assert json.loads((H/'render/rendering.json').read_text())['passed']
    if stage == 'lesson':
        for path in ('lesson-render/rendering.json', 'lesson-native-report.json', 'math-verification.json', 'layout-verification.json'):
            assert json.loads((H/path).read_text())['passed']
    p = Publisher.from_environment(source=':agent/codex')
    work = H/(stage+'-publication')
    with ExitStack() as stack:
        for kp in sorted(kps):
            stack.enter_context(file_lock(ROOT/'.local/learning/inventory/math/59d5cf13-351c-4114-be19-4c3bb64ee051'/f'kp-{kp}.lock'))
        stack.enter_context(file_lock(Path(p.config.request_directory)/'api.lock'))
        c = Committer(p.config, p.client, work)
        request = c.pending()
        if request:
            apply(p, work, json.loads((work/'preparation.json').read_text()), c, request)
        elif not (work/'verification.json').exists():
            for _ in range(5):
                request = None
                try:
                    prepared, c, request = prepare(p, work, rows, kps)
                    apply(p, work, prepared, c, request)
                    break
                except StaleBasis:
                    if request:
                        c.retire(request, 'rejected_stale_basis', {'reason': 'Confirmed basis rejection'})
            else:
                raise RuntimeError('Repeated basis races; repair remains incomplete')


if __name__ == '__main__':
    main()
