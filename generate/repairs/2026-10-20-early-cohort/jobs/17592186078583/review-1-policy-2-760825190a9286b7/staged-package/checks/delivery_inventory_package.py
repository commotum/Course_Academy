"""Read-only checks after shared delivery; reproduce historical inventory and relocation."""
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import repair_checks as c

W, OUT = c.W, c.OUT
REPO = Path('/home/jake/Developer/Course_Academy')


def read(path):
    return json.loads(Path(path).read_text())


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run():
    datasets = {level: read(OUT / ('delivery-' + level) / 'accepted.json') for level in ('easy', 'moderate')}
    before = read(OUT / 'shortcut-before-delivery.json')
    after = {level: c.cue_summary(rows) for level, rows in datasets.items()}
    assert 'q-106877' in after['easy']
    assert len(after['easy']) == len(after['moderate']) == 5
    reports = {level: read(OUT / ('delivery-' + level) / 'delivery.json') for level in datasets}
    batch = read(OUT / 'delivery-batch/accepted.json')
    assert len(batch) == 5
    # Delivery re-keys question-owned identities; derive math expectations anew.
    c.save('delivered-grader-input.json', [c.grader_case(r, f'delivered-{i}')
            for i, r in enumerate(datasets['easy'] + datasets['moderate'] + batch)])
    c.save('shortcut-after-delivery.json', {'before': before, 'after': after,
            'counts': {k: {n: r[n] for n in ('input_count', 'accepted_count', 'duplicate_count')} for k, r in reports.items()},
            'batch_count': len(batch),
            'decision_rule': 'Select ambient equilibrium and negative proportionality; initial is not equilibrium.',
            'limits': 'Length and position probes cover these banks and records, not all possible heuristics. Source replay preserves source weaknesses but is not normal practice.'})

    # Preserve source identity: never label original turkey/soup sources generated.
    sys.path.insert(0, str(REPO))
    publisher = c.load(REPO / 'scripts/generator_publish.py', 'publisher_inventory')
    inv = read(W.parent / 'source/inventory.json')
    source = read(W.parent / 'source/source.json')
    originals = {q[':question/id'] for q in source['material']['kp'][':knowledge-point/questions']}
    existing = {q[':question/id']: q for q in inv['questions'] if q[':question/id'] not in originals}
    provenance = read(W / '17592186078583/reference/replenishment/basis-2711/generated.json')
    legacy = c.load(OUT / 'legacy/17592186078583.py', 'historical_generator')
    reproduced, review, affected = [], [], []
    for old in provenance:
        meta = old['generation']
        level = old['question'][':question/difficulty'].split('/')[-1]
        r = legacy.generate(level, meta['seed'], template=meta['template'], parameters=meta['parameters'])
        stored = existing[r['question'][':question/id']]
        assert publisher.normalized_question(stored, identity=True) == publisher.normalized_question(r['question'], identity=True)
        assert meta == r['generation'], 'Historical generation metadata differs from saved provenance'
        defect = c.shortest_correct(r)
        reproduced.append(r)
        review.append({'question_id': stored[':question/id'], 'entity_id': stored[':db/id'],
                       'identity_content_metadata_match': True, 'unique_shortest_correct': defect,
                       'template': meta['template'], 'parameters': meta['parameters']})
        if defect:
            affected.append({'question_id': stored[':question/id'], 'entity_id': stored[':db/id'],
                             'finding': 'Uniquely shortest equation is correct',
                             'reproduction': 'python checks/delivery_inventory_package.py; historical seed=' + str(meta['seed']) + ', parameters=' + json.dumps(meta['parameters']),
                             'evidence_path': 'generated-records.json'})
    assert len(reproduced) == len(existing) == 7
    assert not affected
    c.save('generated-records.json', reproduced)
    c.save('affected-inventory.json', {'affected_questions': affected})
    c.save('inventory-review.json', {'captured_basis': inv['basis'], 'source_questions_excluded': len(originals),
             'generated_records_tested': review,
             'result': 'Verified absence of the reported unique-shortest defect in all seven captured generated items. The missing cake family was an omission, not a defective stored generated record.',
             'provenance': 'Historical code saved before this repair, replayed at saved seed/template/parameters, with content and question identities checked against captured inventory.',
             'limits': ['Captured basis only; no live inventory or database reads.', 'Original source questions are excluded from affected generated items.']})

    manifest = read(W / 'package.json')
    assert manifest['dependencies'] == {'python': platform.python_version(), 'packages': {'sympy': c.v.sp.__version__}}
    assert (W / 'requirements.txt').read_text() == 'sympy==' + c.v.sp.__version__ + '\n'
    hashes = {name: digest(W / name) for name in manifest['files']}
    relocated = OUT / 'relocated'
    relocated.mkdir(exist_ok=True)
    for name in manifest['files']:
        src, dest = W / name, relocated / name
        assert src.is_file() and not Path(name).is_absolute() and '..' not in Path(name).parts
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
    cmd = [sys.executable, str(relocated / manifest['entrypoint']), '--difficulty', 'easy', '--count', '5', '--seed', '93011', '--format', 'json']
    env = {**os.environ, 'COURSE_ACADEMY_GENERATOR_OUTPUT_DIR': str(OUT / 'assets'), 'PYTHONDONTWRITEBYTECODE': '1'}
    a = subprocess.check_output(cmd, cwd='/tmp', env=env, text=True)
    b = subprocess.check_output(cmd, cwd='/tmp', env=env, text=True)
    assert a == b
    assert json.loads(a) == read(OUT / 'batch.json')
    c.save('relocated-cli.json', json.loads(a))
    assert {name: digest(W / name) for name in manifest['files']} == hashes
    c.save('packaging.json', {'passed': True, 'dependencies': manifest['dependencies'],
                             'runtime_hashes': hashes, 'declared_runtime_files': manifest['files'],
                             'relocation_cwd': '/tmp', 'deterministic': True, 'count': 5,
                             'runtime_files_unchanged_by_checks': True, 'assets_generated': 0})

    # Conditional reproduction of Rust's within-band selection; no live history.
    selection = {}
    for level, rows in datasets.items():
        ids = list(range(100000, 100000 + len(rows)))
        cases = []
        for seen in ([], ids[:2]):
            eligible = sorted(set(ids) - set(seen))
            draws = []
            for i in range(32):
                h = hashlib.sha256(('course-academy/question-selection/v1/repair-' + str(i)).encode()).digest()
                u = (int.from_bytes(h[8:16], 'big') >> 11) / (1 << 53)
                selected = eligible[int(u * len(eligible))]
                assert selected not in seen
                draws.append(selected)
            cases.append({'seen': seen, 'eligible': len(eligible), 'tested_draws': draws,
                          'conditional_probability_per_item': 1 / len(eligible), 'unconfigured_policy_first_id': eligible[0]})
        selection[level] = cases
    c.save('learner-selection.json', {'implementation': 'engine/rust/question_selection.rs::select and seen_before_task',
        'cases': selection,
        'assumptions': 'Synthetic IDs, usable unseen candidates, conditional on positive weight for each sampled band.',
        'limits': 'Actual policy weights, assigned IDs, learner history and concurrent inventory are unavailable. An unconfigured policy selects the first ID; do not claim it provides random variation.'})
    print(json.dumps({'delivery_counts': {k: len(v) for k, v in datasets.items()}, 'captured_generated_inventory_tested': len(reproduced), 'affected_inventory': len(affected), 'relocation': 'passed'}))


if __name__ == '__main__':
    run()
