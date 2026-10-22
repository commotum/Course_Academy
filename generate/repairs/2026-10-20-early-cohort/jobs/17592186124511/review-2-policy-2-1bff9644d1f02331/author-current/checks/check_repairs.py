"""Executable retained findings, using visible math and actual delivery survivors.

Run with the job Python: checks/check_repairs.py source|batch.
Evidence writes stay in this workspace; runtime files and services are untouched.
"""
import collections
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
REPO = Path('/home/jake/Developer/Course_Academy')
JOB = Path('/home/jake/Developer/Course_Academy/generate/repairs/2026-10-20-early-cohort/jobs/17592186124511')
OUT = ROOT / 'evidence/repair-2'
OUT.mkdir(parents=True, exist_ok=True)
spec = importlib.util.spec_from_file_location('content', ROOT / 'checks/check_content.py')
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)
g = v.g

def save(name, value):
    (OUT / name).write_text(json.dumps(value, indent=2) + '\n')

def source():
    supplied = json.loads((JOB / 'source/source.json').read_text())
    originals = {q[':question/math-academy-id']: q for q in supplied['material']['kp'][':knowledge-point/questions']}
    src = originals['q-142367']
    assert src[':question/id'] == '9fbccd10-1c43-51a4-ad8b-36063e11427d'
    assert [a[':answer/value'] for a in src[':question/answer-fields'][0][':answer-field/choices']] == ['II and III only', 'III only', 'I and II only', 'lI only', 'I only']
    replays = []
    for t, src in originals.items():
        if t == 'q-34936':
            assert not src.get(':question/worked-solution')
            continue
        r = g.generate(template=t, replay=True)
        v.inspect(r)
        q = r['question']
        assert q[':question/problem'] == src[':question/problem']
        assert q[':question/worked-solution'] == src[':question/worked-solution']
        assert len(q[':question/answer-fields']) == len(src[':question/answer-fields'])
        for f, old in zip(q[':question/answer-fields'], src[':question/answer-fields']):
            assert f[':answer-field/key'] == old[':answer-field/key']
            values = [a[':answer/value'] for a in old[':answer-field/choices']]
            if t == 'q-142367':
                values = ['II only' if x == 'lI only' else x for x in values]
            assert [a[':answer/value'] for a in f[':answer-field/choices']] == values
            assert v.correct(f) == old[':answer-field/correct'][':answer/value']
        replays.append(r)
    rows = []
    expected = {(1,0,0), (0,1,0), (0,0,1), (1,1,0), (0,1,1)}
    # Target just the restored family; stop once all five banks/positions appear.
    for seed in range(80):
        r = g.generate(template='q-142367', seed=seed)
        v.inspect(r)
        rows.append(r)
        if {v.inspect(x)[0] for x in rows} == expected and {v.inspect(x)[1] for x in rows} == set(range(5)):
            break
    else:
        raise AssertionError('Restored source bank or key positions unreachable')
    # Retained controlled tests: reconstruct current records, rather than copy keys.
    pairs = [g.generate(template=r['generation']['template'], parameters=r['generation']['parameters'], seed=r['generation']['seed']) for r in json.loads((ROOT / 'evidence/counterfactual-records.json').read_text())]
    masks = [v.inspect(r)[0] for r in pairs]
    assert masks[:3] == [(True,True,False), (False,False,True), (True,False,True)]
    assert masks[0] == masks[3] and masks[4] == masks[5]
    save('source-replays.json', replays)
    save('restored-profile.json', rows)
    save('counterfactuals.json', pairs)
    save('source-native-input.json', [v.native(r, 'source-' + str(i)) for i, r in enumerate(replays + rows + pairs)])
    save('source-results.json', {'passed': True, 'complete_replayed_profiles': len(replays), 'restored_samples': len(rows), 'restored_coverage': v.summarize(rows, True), 'typo_correction': 'q-142367: lI only -> II only; source preserved', 'controlled_pairs': 4})
    print('Source regression passed:', len(replays), 'complete replays;', len(rows), 'restored-profile samples; four retained controlled pairs.')

def cue(r):
    fs = r['question'][':question/answer-fields']
    return all((v.correct(f) == 'true') == ('invertible' in f[':answer-field/key']) for f in fs)

def audit_batch(rows):
    groups = collections.defaultdict(list)
    radio = []
    for r in rows:
        v.inspect(r)
        fs = r['question'][':question/answer-fields']
        if fs[0][':answer-field/type'].endswith('/checkbox'):
            groups[len(fs)].append(r)
        else:
            radio.append((v.inspect(r)[1], v.correct(fs[0])))
    report = {}
    for size, sub in groups.items():
        counts = [sum(v.correct(f) == 'true' for f in r['question'][':question/answer-fields']) for r in sub]
        responses = [''.join('1' if v.correct(f) == 'true' else '0' for f in r['question'][':question/answer-fields']) for r in sub]
        if len(sub) > 1:
            assert len(set(counts)) > 1, ('fixed correct-choice count', size, counts)
            assert len(set(responses)) > 1, ('fixed displayed positions', size)
            assert not all(cue(r) for r in sub), 'Select only the invertibility statement solves every recurring checkbox item'
        report[str(size)] = {'items': len(sub), 'selected_counts': counts, 'responses': responses, 'invertibility_only_successes': sum(map(cue, sub)), 'random_nonempty_subset_baseline': 1 / (2 ** size - 1)}
    if len(radio) > 1:
        assert len({p for p, key in radio}) > 1, 'Fixed radio position'
        assert len({key for p, key in radio}) > 1, 'Fixed radio subset'
    report['radio'] = {'positions': [p for p, key in radio], 'subsets': [key for p, key in radio]}
    return report

def delivery(name, rows):
    infile = OUT / (name + '.json')
    infile.write_text(json.dumps(rows, indent=2) + '\n')
    cmd = [sys.executable, str(REPO / 'generate/pipeline/check_delivery.py'), '--input', str(infile), '--source', str(JOB / 'source/source.json'), '--inventory', str(JOB / 'source/inventory.json'), '--difficulty', 'moderate', '--output', str(OUT / (name + '-delivery')), '--asset-root', str(OUT / 'assets'), '--math-root', '/media/jake/SSD/EDB/math']
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    accepted = json.loads((OUT / (name + '-delivery/accepted.json')).read_text())
    return accepted, cmd

def batch():
    # Reproduce the exact seed/template counterexample under the current generator.
    original = [g.generate(template=t, seed=4126872122 + j) for j, t in enumerate(['q-141200', 'q-142474'])]
    for r in original:
        v.inspect(r)
    assert all(cue(r) for r in original), 'Update explanation if the underlying counterexample changes'
    save('historical-pair-current-generator.json', original)
    old_order = ['q-141200', 'q-142474', 'q-142472', 'q-142358', 'q-141198']
    batches = {'original-order': g._batch_records('moderate', 5, 4126872122, old_order)}
    commands = []
    for seed in (4126872122, 0, 1, 99, 2026):
        cmd = [sys.executable, str(ROOT / '17592186124511.py'), '--difficulty', 'moderate', '--count', '5', '--seed', str(seed), '--format', 'json']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True, env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1', 'COURSE_ACADEMY_GENERATOR_OUTPUT_DIR': str(OUT / 'assets')})
        batches['cli-' + str(seed)] = json.loads(result.stdout)
        commands.append(cmd)
    reports = {}
    native = []
    delivered = []
    for name, rows in batches.items():
        assert len(rows) == 5
        before = audit_batch(rows)
        accepted, cmd = delivery(name, rows)
        commands.append(cmd)
        assert len(accepted) == 5, ('delivery lost a decision', name, len(accepted))
        after = audit_batch(accepted)
        assert before == after
        reports[name] = {'before': before, 'after': after, 'accepted': len(accepted), 'templates': [r['generation']['template'] for r in rows]}
        native += [v.native(r, name + '-' + str(i)) for i, r in enumerate(accepted)]
        delivered += accepted
    # The original profile order is retained; resampling must defeat the exact pair.
    forced = batches['original-order']
    assert [r['generation']['template'] for r in forced] == old_order
    assert not cue(forced[1])
    save('batch-results.json', {'passed': True, 'batches': reports, 'commands': commands, 'selection_limits': ['Captured inventory only; no live learner history or weighted draws.', 'A layout represented once cannot establish within-group variation.']})
    save('batch-native-input.json', native)
    save('batch-accepted.json', delivered)
    # Inventory is fully inspected; do not reinterpret source originals as generated.
    inventory = json.loads((JOB / 'source/inventory.json').read_text())
    supplied = json.loads((JOB / 'source/source.json').read_text())
    source_ids = {q[':question/id'] for q in supplied['material']['kp'][':knowledge-point/questions']}
    assert all(q[':question/id'] in source_ids and q.get(':question/math-academy-id') and not q.get(':question/generation') for q in inventory['questions'])
    (ROOT / 'affected-inventory.json').write_text('{"affected_questions": []}\n')
    save('inventory-results.json', {'status': 'verified absence of stored generated instances', 'inspected': len(inventory['questions']), 'generated': 0, 'source_originals': len(inventory['questions']), 'basis': inventory['basis'], 'originals_not_marked_generated': True})
    print('Batch regression passed: exact original order plus five CLI batches; all 30 delivery survivors retain contrasting recurring checkbox decisions.')

if __name__ == '__main__':
    {'source': source, 'batch': batch}[sys.argv[1]]()
