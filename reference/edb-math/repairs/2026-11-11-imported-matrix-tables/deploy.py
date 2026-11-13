"""Preview, commit and reconcile the exact reviewed global repair transaction."""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import uuid

H = Path(__file__).resolve().parent
ROOT = H.parents[3]
sys.path.insert(0, str(ROOT))
from scripts.generator_publish import Publisher, QUESTION_PULL, StaleBasis, digest, dumps, loads, kw, file_lock, jsonable
from capture.scripts.database.commit import Committer
from capture.scripts.storage import atomic_json

PARENTS = '[:db/id :knowledge-point/id :knowledge-point/title {[:knowledge-point/questions :limit nil] [:db/id]} {:knowledge-point/canonical-example [:db/id]} {:knowledge-point/question-generator [*]}]'


def read(path):
    return json.loads((H/path).read_text())


def canonical(value):
    if isinstance(value, dict):
        return {str(k): canonical(v) for k,v in value.items()}
    if isinstance(value, list):
        return sorted([canonical(v) for v in value], key=lambda v: json.dumps(v, sort_keys=True))
    return jsonable(value)


def native_read(p, directory, basis, plan):
    directory.mkdir(parents=True, exist_ok=True)
    entities = sorted({r['entity'] for r in plan['mutations']} |
                      {r['field_entity'] for r in plan['answer_creations']} |
                      {r['field_entity'] for r in plan['field_unlinks']})
    parents = [r[':db/id'] for r in read('capture/parents.json')]
    groups = [['questions', QUESTION_PULL, plan['question_ids']], ['entities', '[*]', entities],
              ['parents', PARENTS, parents]]
    (directory/'native-pulls.edn').write_text(dumps(groups)+'\n')
    result = subprocess.run([str(ROOT/'reference/mathacademy/repairs/2026-10-17-import-source-bulk/native_read'),
        str(directory), str(basis)], env=p.client.environment, capture_output=True, text=True, timeout=300)
    (directory/'read.log').write_text(result.stdout+result.stderr)
    result.check_returncode()
    values = {name: loads((directory/(name+'.edn')).read_text()) for name,_,_ in groups}
    return values


def prepare(p, work, plan):
    status = p.client.status()
    basis = status['basis']
    before = native_read(p, work/'before', basis, plan)
    original = {r[':db/id']: r for r in read('capture/questions.json')}
    for q in before['questions']:
        assert canonical(q) == canonical(original[q[':db/id']]), ('Concurrent question content changed', q[':db/id'])
    nodes = {r[':db/id']: r for r in before['entities']}
    forms, assertions, retractions = [], [], []
    def add(e, attr, value):
        forms.append([kw('db/add'), e, kw(attr), value])
        assertions.append([e, kw(attr), value])
    def cas(e, attr, old, new):
        assert canonical(nodes[e].get(':'+attr)) == canonical(old), (e, attr, 'CAS source changed')
        forms.append([kw('db/cas'), e, kw(attr), old, new])
        assertions.append([e, kw(attr), new])
        if old is not None:
            retractions.append([e, kw(attr), old])
    for row in plan['mutations']:
        cas(row['entity'], row['attribute'], row['before'], row['after'])
    for row in plan['answer_creations']:
        answer = row['answer_tempid']
        add(answer, 'answer/id', uuid.UUID(row['answer_uuid']))
        add(answer, 'answer/type', kw(row['answer_type']))
        add(answer, 'answer/value', row['answer_value'])
        add(row['field_entity'], 'answer-field/choices', answer)
        cas(row['field_entity'], 'answer-field/correct', None, answer)
        forms.append([kw('db/ensure'), answer, kw('answer/validate')])
    for row in plan['field_unlinks']:
        e, f = row['question_entity'], row['field_entity']
        assert any(v[':db/id'] == f for v in nodes[e][':question/answer-fields'])
        forms.append([kw('db/retract'), e, kw('question/answer-fields'), f])
        retractions.append([e, kw('question/answer-fields'), f])
    expected = read('questions-after.json')
    fields = {f[':db/id'] for q in expected for f in q.get(':question/answer-fields', [])}
    forms += [[kw('db/ensure'), f, kw('answer-field/validate')] for f in sorted(fields)]
    forms += [[kw('db/ensure'), q, kw('question/validate')] for q in plan['question_ids']]
    attrs = p.client.query('[:find ?a ?ident ?type :where [?a :db/ident ?ident] [?a :db/valueType ?v] [?v :db/ident ?type]]', [], work, 'attributes', basis)
    idents = p.client.query('[:find ?e ?ident :where [?e :db/ident ?ident]]', [], work, 'idents', basis)
    snapshot = {'basis': basis, 'lineage': status['lineage'], 'attributes': attrs, 'idents': idents}
    batch = {'source': plan['source'], 'forms': forms, 'assertions': assertions, 'retractions': retractions}
    prepared = {'basis': basis, 'plan_sha256': digest(plan), 'before_edn': dumps(before),
                'expected_questions': expected, 'batch_edn': dumps(batch), 'snapshot_edn': dumps(snapshot)}
    atomic_json(work/'preparation.json', prepared)
    c = Committer(p.config, p.client, work)
    c.preview(batch, snapshot)
    request = c.save_request(batch, snapshot, digest(prepared))
    print(json.dumps({'prepared': True, 'basis': basis, 'forms': len(forms),
                      'transaction_bytes': len(request['transaction'].encode()), 'request_key': request['request_key']}), flush=True)
    return prepared, c, request


def apply(p, work, plan, prepared, c, request):
    assert request['content_sha256'] == digest(prepared)
    assert digest(plan) == prepared['plan_sha256']
    receipt = c.submit(request)
    proof = c.verify_receipt(request, receipt)
    basis = receipt[':edb/db-after-t']
    current = native_read(p, work/'after', basis, plan)
    tempids = {str(k): v for k,v in receipt.get(':edb/tempids', {}).items()}
    def resolve(v):
        if isinstance(v, dict):
            return {k: resolve(x) for k,x in v.items()}
        if isinstance(v, list):
            return [resolve(x) for x in v]
        return tempids.get(v, v) if isinstance(v, str) else v
    assert canonical(current['questions']) == canonical(resolve(prepared['expected_questions']))
    before = loads(prepared['before_edn'])
    assert canonical(current['parents']) == canonical(before['parents'])
    # Orphan entities and their historical values remain intact after unlinking.
    old_nodes = {r[':db/id']: r for r in before['entities']}
    new_nodes = {r[':db/id']: r for r in current['entities']}
    for row in plan['field_unlinks']:
        f = row['field_entity']
        assert canonical(new_nodes[f]) == canonical(old_nodes[f])
    historical = native_read(p, work/'historical', request['basis'], plan)
    assert canonical(historical) == canonical(before)
    atomic_json(H/'questions-committed.json', jsonable(current['questions']))
    result = {'passed': True, 'committed': True, 'basis_before': request['basis'], 'basis_after': basis,
              'question_layouts_repaired': len(plan['question_ids']),
              'new_field_owned_answers': len(plan['answer_creations']),
              'empty_duplicate_field_links_removed': len(plan['field_unlinks']),
              'worked_solutions_added': sum(r['attribute'] == 'question/worked-solution' and r['before'] is None for r in plan['mutations']),
              'worked_solution_notation_repairs': sum(r['attribute'] == 'question/worked-solution' and r['before'] is not None for r in plan['mutations']),
              'all_question_and_field_identities_preserved': True, 'parent_memberships_and_generators_unchanged': True,
              'orphan_entities_and_retained_history_preserved': True, 'request_key': request['request_key'], **proof}
    atomic_json(H/'commit-verification.json', result)
    c.retire(request, 'verified', result)
    print(json.dumps(result, indent=2), flush=True)


def main():
    gate = read('verification-precommit.json')
    assert gate['passed']
    assert gate['plan_sha256'] == hashlib.sha256((H/'plan.json').read_bytes()).hexdigest()
    plan = read('plan.json')
    p = Publisher.from_environment(source=':agent/codex')
    work = H/'publication'
    # Generation remains off. This lock serializes the app's authored-content API.
    with file_lock(Path(p.config.request_directory)/'api.lock'):
        c = Committer(p.config, p.client, work)
        request = c.pending()
        if request:
            try:
                apply(p, work, plan, read('publication/preparation.json'), c, request)
            except StaleBasis:
                c.retire(request, 'rejected_stale_basis', {'reason': 'Confirmed basis rejection during exact recovery'})
        if not (H/'commit-verification.json').exists():
            for _ in range(10):
                request = None
                try:
                    prepared, c, request = prepare(p, work, plan)
                    apply(p, work, plan, prepared, c, request)
                    break
                except StaleBasis:
                    if request:
                        c.retire(request, 'rejected_stale_basis', {'reason': 'Confirmed basis rejection; refreshed exact state'})
            else:
                raise RuntimeError('Repeated basis races; repair remains uncommitted')


if __name__ == '__main__':
    main()
