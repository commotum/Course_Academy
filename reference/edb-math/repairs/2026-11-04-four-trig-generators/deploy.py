"""Install reviewed generators and atomically replace superseded generated stock.

Retirement changes future eligibility only; saved question/answer identities,
keys, KP membership and learner task items are retained.
"""
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys

H = Path(__file__).resolve().parent
ROOT = H.parents[3]
sys.path.insert(0, str(ROOT))
from scripts.generator_publish import (Publisher, GeneratorCommitter, StaleBasis, digest,
    dumps, loads, kw, file_lock, normalized_question)
from scripts.generator_packages import publish_package, build_manifest, manifest_digest, verify_package, check_dependencies
from capture.scripts.storage import atomic_json


def prepare(p, kid, package, capture):
    work = H / 'publication' / kid
    prepared = p.prepare(int(kid), json.loads((H / 'pools' / f'{kid}.json').read_text()),
        package.reference, package.digest, work,
        source_snapshot=json.loads((H / 'source' / kid / 'source.json').read_text()), assets_directory=H,
        expected_registered_generator=capture['kps'][kid][':knowledge-point/question-generator'][':question-generator/script'])
    # A duplicate means the pool plan must be reviewed, never silently reduced.
    assert prepared['duplicates'] == 0, (kid, prepared['duplicates'])
    before, batch = loads(prepared['before_edn']), loads(prepared['batch_edn'])
    old = [q for q in before[':knowledge-point/questions']
           if not q.get(':question/math-academy-id') and not q.get(':question/retired')]
    retired = []
    for q in old:
        eid = q[':db/id']; previous = q.get(':question/retired'); retired.append(eid)
        batch['forms'].append([kw('db/cas'), eid, kw('question/retired'), previous, True])
        batch['assertions'].append([eid, kw('question/retired'), True])
        if previous is False: batch['retractions'].append([eid, kw('question/retired'), False])
    usage = p.client.query('[:find (pull ?q [:db/id {:task-item/_content [:db/id]}]) :in $ [?q ...] :where [?q :question/id _]]',
                           [retired], work, 'retired-history', prepared['basis']) if retired else []
    prepared.update(batch_edn=dumps(batch), retired_questions=sorted(retired),
        retired_with_preserved_task_items=[r[0][':db/id'] for r in usage if r[0].get(':task-item/_content')])
    atomic_json(work / 'preparation.json', prepared)
    committer = GeneratorCommitter(p.config, p.client, work)
    committer.preview(batch, loads(prepared['snapshot_edn']))
    request = committer.save_request(batch, loads(prepared['snapshot_edn']), digest(prepared))
    return prepared, committer, request


def apply(p, kid, prepared, committer, request):
    assert request['content_sha256'] == digest(prepared)
    receipt = committer.submit(request)
    proof = committer.verify_receipt(request, receipt)
    basis = receipt[':edb/db-after-t']
    after = p.read_kp(int(kid), H / 'publication' / kid / 'after', basis)
    before = loads(prepared['before_edn'])
    now = {str(q[':question/id']): q for q in after[':knowledge-point/questions']}
    assert len(now) == len(before[':knowledge-point/questions']) + prepared['new_questions']
    for q in before[':knowledge-point/questions']:
        expected = dict(q)
        if q[':db/id'] in prepared['retired_questions']: expected[kw('question/retired')] = True
        assert now[str(q[':question/id'])] == expected, q[':db/id']
    new = []
    for record in prepared['records']:
        q = now[record['question'][':question/id']]
        assert normalized_question(q) == normalized_question(record['question'])
        new.append({'entity': q[':db/id'], 'id': str(q[':question/id']),
                    'level': str(q[':question/difficulty'][':db/ident']).split('/')[-1]})
    excluded = {':knowledge-point/questions', ':knowledge-point/question-generator'}
    assert {k: v for k, v in before.items() if k not in excluded} == {k: v for k, v in after.items() if k not in excluded}
    assert after[':knowledge-point/question-generator'][':question-generator/script'] == prepared['generator_path']
    result = {'passed': True, 'committed': True, 'kp': int(kid), 'basis_before': request['basis'], 'basis_after': basis,
              'package_sha256': prepared['package_sha256'], 'generator': prepared['generator_path'],
              'retired': prepared['retired_questions'], 'new_questions': new,
              'retired_with_preserved_task_items': prepared['retired_with_preserved_task_items'],
              'originals_canonical_keys_ids_and_saved_history_preserved': True,
              'request_key': request['request_key'], **proof}
    atomic_json(H / 'publication' / kid / 'verification.json', result)
    committer.retire(request, 'verified', result)
    return result


def main():
    review = json.loads((H / 'pool-review.json').read_text()); assert review['passed']
    for mode in ('desktop', 'phone'):
        assert json.loads((H / mode / 'rendering.json').read_text())['passed']
    capture = json.loads((H / 'capture.json').read_text())
    p = Publisher.from_environment(source=':agent/codex'); results = []
    for kid, inventory in review['inventory'].items():
        folder = ROOT / inventory['workspace']
        files = list(inventory['runtime_sha256'])
        for name, expected in inventory['runtime_sha256'].items():
            assert hashlib.sha256((folder / name).read_bytes()).hexdigest() == expected, (kid, name)
        requirements = folder / 'requirements.txt'
        packages = dict(line.strip().split('==') for line in requirements.read_text().splitlines() if line.strip() and not line.startswith('#')) if requirements.exists() else {}
        dependencies = {'python': platform.python_version(), 'packages': packages}
        dep_check = check_dependencies(dependencies, sys.executable)
        manifest = build_manifest(folder, 'generator.py', files, dependencies=dependencies)
        package = publish_package(folder, 'generator.py', files, p.config.math_root,
                                  dependencies=dependencies, expected_digest=manifest_digest(manifest))
        verify_package(package.directory, package.digest)
        # The installed immutable closure must reproduce every published batch.
        for band in ('easy', 'moderate', 'hard'):
            sample = inventory['sampling'][band]
            installed = subprocess.run([sys.executable, str(package.script), '--difficulty', band,
                         '--count', str(sample['count']), '--seed', str(sample['seed']), '--format', 'json'], check=True, capture_output=True, text=True, timeout=180)
            original = subprocess.run([sys.executable, str(folder / 'generator.py'), '--difficulty', band,
                         '--count', str(sample['count']), '--seed', str(sample['seed']), '--format', 'json'], check=True, capture_output=True, text=True, timeout=180)
            assert installed.stdout == original.stdout, (kid, band)
        work = H / 'publication' / kid; work.mkdir(parents=True, exist_ok=True)
        atomic_json(work / 'dependencies.json', dep_check)
        lock = ROOT / '.local/learning/inventory/math/59d5cf13-351c-4114-be19-4c3bb64ee051' / f'kp-{kid}.lock'
        with file_lock(lock), file_lock(Path(p.config.request_directory) / 'api.lock'):
            c = GeneratorCommitter(p.config, p.client, work)
            pending = c.pending()
            if pending:
                result = apply(p, kid, json.loads((work / 'preparation.json').read_text()), c, pending)
            elif (work / 'verification.json').exists():
                result = json.loads((work / 'verification.json').read_text())
                assert result['package_sha256'] == package.digest
            else:
                for attempt in range(5):
                    request = None
                    try:
                        prepared, c, request = prepare(p, kid, package, capture)
                        result = apply(p, kid, prepared, c, request)
                        break
                    except StaleBasis:
                        if request: c.retire(request, 'rejected_stale_basis', {'reason': 'Confirmed rejection; refresh original state'})
                else: raise RuntimeError('Repeated basis races: publication incomplete')
        results.append(result)
        print(json.dumps({'kp': kid, 'registered': True, 'retired': len(result['retired']),
                          'new': len(result['new_questions']), 'basis': result['basis_after']}), flush=True)
    atomic_json(H / 'verification.json', {'passed': True, 'registered': len(results),
        'retired': sum(len(r['retired']) for r in results),
        'new': sum(len(r['new_questions']) for r in results), 'kps': results})


if __name__ == '__main__': main()
