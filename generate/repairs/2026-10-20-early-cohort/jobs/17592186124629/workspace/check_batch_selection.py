"""Offline regression for 7ce5456a67dba2e42f32; inspect actual visible records."""
import collections
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import types

sys.dont_write_bytecode = True
from validate_repair import g, decode, native_checks

ROOT = Path(__file__).resolve().parent
REPO = Path('/home/jake/Developer/Course_Academy')
JOB = ROOT.parent
E = ROOT/'evidence/batch-repair'


def save(name, value):
    (E/name).write_text(json.dumps(value, indent=2)+'\n')


def family(record):
    q = record['question']
    fields = q[':question/answer-fields']
    statements = ([f[':answer-field/key'] for f in fields] if len(fields)==3
                  else re.findall(r'^I{1,3}\. (.+)$', q[':question/problem'], re.M))
    concepts = []
    for statement in statements:
        if 'basis' in statement: concept = 'basis'
        elif 'Ax=0' in statement: concept = 'null-solution'
        elif 'nullity' in statement: concept = 'nullity'
        elif 'Null' in statement: concept = 'null'
        elif 'Col' in statement: concept = 'col'
        elif 'rank' in statement: concept = 'rank'
        elif 'det' in statement: concept = 'det'
        elif 'pivot' in statement: concept = 'pivot'
        elif 'invertible' in statement: concept = 'inv'
        else: raise AssertionError(statement)
        concepts.append(concept)
    return (fields[0][':answer-field/type'], tuple(concepts))


def inspect(rows, require_complete=False):
    groups = collections.defaultdict(list)
    for r in rows:
        groups[family(r)].append((decode(r), r))
    report = []
    for key, values in groups.items():
        masks = collections.Counter(bits for bits, _ in values)
        assert len(masks)==len(values), ('Repeated family decision in selection prefix', key, masks)
        positions = collections.Counter()
        for bits, r in values:
            fields = r['question'][':question/answer-fields']
            pos = tuple(i for i, b in enumerate(bits) if b) if len(fields)==3 else tuple(
                i for i, a in enumerate(fields[0][':answer-field/choices'])
                if a[':answer/id']==fields[0][':answer-field/correct'][1])
            positions[pos] += 1
        counts = collections.Counter(sum(bits) for bits, _ in values)
        if require_complete:
            assert len(masks)==(7 if len(values[0][1]['question'][':question/answer-fields'])==3 else 5)
            assert len(positions)>1 and len(counts)>1, (key, positions, counts)
        report.append({'family':str(key), 'attempts':len(values),
            'subsets':[list(bits) for bits in masks], 'correct_counts':dict(counts),
            'best_constant_subset_successes':max(masks.values()),
            'best_constant_position_successes':max(positions.values())})
    return report


def delivery(name, rows):
    save(name+'.json', rows)
    command = [sys.executable, '-B', str(REPO/'generate/pipeline/check_delivery.py'),
        '--input', str(E/(name+'.json')), '--source', str(JOB/'source/source.json'),
        '--inventory', str(JOB/'source/inventory.json'), '--difficulty', 'moderate',
        '--output', str(E/(name+'-delivery')), '--math-root', '/media/jake/SSD/EDB/math']
    subprocess.run(command, check=True, stdout=subprocess.DEVNULL)
    accepted = json.loads((E/(name+'-delivery/accepted.json')).read_text())
    assert len(accepted)==len(rows), ('Delivery unexpectedly removed records', name)
    return accepted


def semantic(record):
    q = record['question']
    return (q[':question/problem'], tuple(sorted(f[':answer-field/key'] for f in q[':question/answer-fields'])))


def main():
    E.mkdir(exist_ok=True)
    # Keep the exact reviewer's assertion executable, without editing its rule.
    completed = subprocess.run([sys.executable, '-B', str(ROOT/'failing_batch_check.py'),
        str(ROOT/'17592186124629.py')], capture_output=True, text=True)
    save('strict-regression.json', {'command':completed.args, 'returncode':completed.returncode,
        'stdout':completed.stdout, 'stderr':completed.stderr})
    assert completed.returncode==0, completed.stderr
    before = types.ModuleType('before_batch_repair')
    before.__file__ = str(ROOT/'17592186124629.py')
    exec(compile((E/'before-generator.py').read_text(), 'before-generator.py', 'exec'), before.__dict__)
    seed = 2086806769
    old_batch = before.batch(count=5, seed=seed)
    save('before-records.json', old_batch)
    old_vectors = [decode(r) for r in old_batch if family(r)[1]==('det','col','pivot')]
    assert old_vectors==[(False,True,False)]*2, old_vectors
    batch = g.batch(count=5, seed=seed)
    assert batch==g.batch(count=5, seed=seed)
    before_delivery = inspect(batch)
    accepted = delivery('reported-batch', batch)
    after_delivery = inspect(accepted)
    small = []
    for sample_seed in (24629, 0, 1, 42):
        rows = g.batch(count=5, seed=sample_seed)
        small.append({'seed':sample_seed, 'groups':inspect(rows)})
    # One complete decision pass exercises every family and legal subset.
    expected_families = {family(g.generate(template=sid, parameters=g.domain(sid)[0])) for sid in g.CASES}
    first_pass_count = sum(7 if kind.endswith('/checkbox') else 5 for kind, _ in expected_families)
    prefix = g.batch(count=first_pass_count, seed=seed)
    assert {family(r) for r in prefix}==expected_families
    prefix_before = inspect(prefix, require_complete=True)
    prefix_accepted = delivery('decision-prefix', prefix)
    prefix_after = inspect(prefix_accepted, require_complete=True)
    # The changed design must reorder, never discard, the original finite domain.
    original_full = before.batch(count=10000, seed=seed)
    repaired_full = g.batch(count=10000, seed=seed)
    old_set, new_set = {semantic(r) for r in original_full}, {semantic(r) for r in repaired_full}
    assert old_set==new_set and len(new_set)==len(repaired_full)
    assert g.batch(count=0)==[]
    save('domain-preservation.json', {'status':'pass','before_semantic_instances':len(old_set),
        'after_semantic_instances':len(new_set),'lost':len(old_set-new_set),'added':len(new_set-old_set),
        'semantic_set_sha256':hashlib.sha256(json.dumps(sorted(new_set)).encode()).hexdigest(),
        'criterion':'Visible prompt plus conclusion labels; ignores metadata, seed, UUID and radio order.'})
    # Reuse independent witnesses; only the sampler changed, so compare all source
    # replay records to their retained, fully checked question bodies.
    source = json.loads((JOB/'source/source.json').read_text())['material']['kp']
    assert source==g.SOURCE, 'Source evidence changed'
    retained = json.loads((ROOT/'evidence/source-replays.json').read_text())
    current = [g.generate(template=r['generation']['template'], parameters={'premise':'replay'}) for r in retained]
    assert [r['question'] for r in current]==[r['question'] for r in retained]
    for r in current: decode(r)
    save('source-replay.json', {'status':'pass','banks':len(current), 'source_snapshot_unchanged':True,
        'criterion':'Exact retained question bodies, including full choices and source corrections; independent rank witnesses.'})
    controls = []
    seen_types = set()
    for c in json.loads((ROOT/'evidence/counterfactuals.json').read_text()):
        if c['type'] in seen_types: continue
        pair = [g.generate(seed=r['generation']['seed'], template=r['generation']['template'],
                    parameters=r['generation']['parameters']) for r in (c['before'],c['after'])]
        a, b = map(decode, pair)
        if c['type']=='equivalent_hypothesis': assert a==b
        else: assert a!=b
        assert [r['question'] for r in pair]==[c['before']['question'], c['after']['question']]
        seen_types.add(c['type'])
        controls.append({'type':c['type'], 'before':pair[0], 'after':pair[1]})
    assert seen_types=={'conclusion_polarity','equivalent_hypothesis','hypothesis_status_same_conclusions'}
    save('counterfactuals.json', controls)
    grader_rows = batch + [r for c in controls for r in (c['before'],c['after'])]
    # A few prefix examples ensure radio and checkbox selection are both graded.
    grader_rows += [next(r for r in prefix if len(r['question'][':question/answer-fields'])==1)]
    checks = [{'label':'batch repair '+str(i),'record':r,'checks':native_checks(r)} for i,r in enumerate(grader_rows)]
    save('native-input.json', checks)
    subprocess.run([str(REPO/'generate/runs/current/check-engine'),str(E/'native-input.json'),
                    str(E/'native-report.json')],check=True,stdout=subprocess.DEVNULL)
    report = {'status':'pass','finding':'7ce5456a67dba2e42f32','seed':seed,
        'before_failure_vectors':[list(v) for v in old_vectors],
        'reported_batch_before_delivery':before_delivery,'reported_batch_after_delivery':after_delivery,
        'small_regression_batches':small,'decision_prefix_records':len(prefix),
        'decision_prefix_before_delivery':prefix_before,'decision_prefix_after_delivery':prefix_after,
        'source_banks_replayed':len(current),'native_records':len(checks),
        'native_responses':sum(len(c['checks']) for c in checks),
        'limitations':['Offline captured inventory only; live learner history and weighted draws are not exercised.',
                      'A singleton family in a five-item batch cannot establish within-family variation; the complete decision prefix does.']}
    save('validation.json', report)
    print(json.dumps({k:report[k] for k in ('status','finding','seed','decision_prefix_records','source_banks_replayed','native_records','native_responses')}))


if __name__=='__main__': main()
