"""Reproduce runner binding and regress only the asset-reference repair.
Run with the job's Python; all mutations remain in this workspace.
"""
import copy
import hashlib
import importlib.metadata
import json
import math
import os
from pathlib import Path
import shutil
import subprocess
import sys
from fractions import Fraction as F

from verify_record import g, check
from probe_banks import probes

W = Path(__file__).resolve().parents[1]
E = W / 'evidence'
OUT = E / 'asset-reference-repair'
REPO = Path('/home/jake/Developer/Course_Academy')
SOURCE = REPO / 'generate/repairs/2026-10-20-early-cohort/jobs/17592186172038/source'
MATH = Path('/media/jake/SSD/EDB/math')
sys.path.insert(0, str(REPO / 'scripts'))
# Import only; invoking this read-only helper cannot publish or open the DB.
from generator_pipeline import asset_hashes

OUT.mkdir(exist_ok=True)
manifest = json.loads((W / 'package.json').read_text())
assert manifest['dependencies'] == {'python': sys.version.split()[0], 'packages': {
    p: importlib.metadata.version(p) for p in ('sympy', 'matplotlib')}}

def save(name, value):
    (OUT / name).write_text(json.dumps(value, indent=2) + '\n')

def field(record):
    return record['question'][':question/answer-fields'][0]

def portable(record):
    """Normalize only configured asset locations, including geometry metadata keys."""
    mapping = {a[':answer/value']: Path(a[':answer/value']).name
               for a in field(record)[':answer-field/choices']}
    def visit(value):
        if isinstance(value, dict):
            return {visit(k): visit(v) for k, v in value.items()}
        if isinstance(value, list):
            return [visit(v) for v in value]
        if isinstance(value, str):
            for before, after in mapping.items():
                value = value.replace(before, after)
        return value
    return visit(record)

def semantics(record):
    value = portable(record)
    # Replaying sampled parameters explicitly skips RNG consumption by sampling.
    # The complete choice bank and IDs must match; its display order may change.
    field(value)[':answer-field/choices'].sort(key=lambda a: a[':answer/id'])
    return value

def exact(template, p):
    a, b, d = F(p['a']), F(p.get('b', 1)), F(p.get('d', 1))
    result = []
    for x, y in p['points']:
        x, y = F(x), F(y)
        result.append({'constant_product': lambda: a-b*x*y,
                       'quadratic_linear': lambda: a*x*x-b*y,
                       'rational_square': lambda: a*y*y/x,
                       'two_quadratic': lambda: a*x*x-b*y*y,
                       'affine_fraction': lambda: (a*x+b*y)/d,
                       'affine': lambda: a*x+b*y}[template]())
    return list(map(str, result))

def geometry(record):
    f = field(record)
    a = next(a for a in f[':answer-field/choices']
             if a[':answer/id'] == f[':answer-field/correct'][1])
    return record['generation']['choice_geometry'][a[':answer/value']]

def verify(record):
    check(record)
    m = record['generation']
    assert exact(m['template'], m['parameters']) == m['exact_slopes'] == geometry(record)
    return record

# Copy only manifest runtime inputs; fresh outputs in differently related directories.
runs = []
roots = []
old_batch = json.loads((E / 'classification-repair/batch.json').read_text())
for label in ('a', 'b'):
    root = OUT / ('runtime-a' if label == 'a' else 'nested/runtime-b')
    output = OUT / ('outputs-a' if label == 'a' else 'separate/deep/outputs-b')
    for path in (root, output):
        if path.exists(): shutil.rmtree(path)
        path.mkdir(parents=True)
    for filename in manifest['files']:
        target = root / filename
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(W / filename, target)
    before = {n: hashlib.sha256((root/n).read_bytes()).hexdigest() for n in manifest['files']}
    cmd = [sys.executable, '-E', '-s', '-B', str(root/manifest['entrypoint']),
           '--difficulty', 'easy', '--count', '5', '--seed', '71', '--format', 'json']
    env = {**os.environ, 'COURSE_ACADEMY_GENERATOR_OUTPUT_DIR': str(output),
           'MPLBACKEND': 'Agg', 'PYTHONDONTWRITEBYTECODE': '1'}
    repetitions = []
    hashes = []
    for repetition in range(2):
        result = subprocess.run(cmd, cwd=root, env=env, text=True, capture_output=True, check=True)
        records = json.loads(result.stdout)
        assert len(records) == 5
        for record in records:
            verify(record)
            for answer in field(record)[':answer-field/choices']:
                path = Path(answer[':answer/value'])
                assert path.is_absolute() and path.is_relative_to(output) and path.is_file()
        repetitions.append(records)
        hashes.append(asset_hashes(records, root, MATH))
    assert repetitions[0] == repetitions[1] and hashes[0] == hashes[1]
    assert {n: hashlib.sha256((root/n).read_bytes()).hexdigest() for n in manifest['files']} == before
    assert {str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()} == set(manifest['files'])
    assert list(map(portable, records)) == list(map(portable, old_batch))
    save(f'relocated-{label}.json', records)
    runs.append({'command': cmd, 'runtime': str(root.relative_to(W)),
                 'output_dir': str(output.relative_to(W)), 'repetitions': 2,
                 'bound_assets': len(hashes[0]), 'binding_passed': True,
                 'repeat_identical': True, 'package_unchanged': True,
                 'prior_semantics_and_ids_preserved': True})
    roots.append(records)
assert list(map(portable, roots[0])) == list(map(portable, roots[1]))
print('Actual runner binding: 2 relocated packages × 2 deterministic runs × 5 records', flush=True)

# All 7 complete source banks and the previous bounded math/control sample.
os.environ['COURSE_ACADEMY_GENERATOR_OUTPUT_DIR'] = str(E / 'assets')
source_records = []
supplied = json.loads((SOURCE/'source.json').read_text())
raw = {q[':question/math-academy-id']: q for q in supplied['material']['kp'][':knowledge-point/questions']}
raster = json.loads((W/'17592186172038/source-raster.json').read_text())
for old in json.loads((E/'source-replays.json').read_text()):
    m = old['generation']; sid = m['bank_profile']
    record = verify(g.generate('easy', m['seed'], profile=sid, parameters=m['parameters']))
    assert portable(record) == portable(old)
    assert record['question'][':question/problem'] == raw[sid][':question/problem']
    _, bank = g.banks(m['template'], m['parameters'], sid)
    observed = [v for v in raster if v['source_id'] == sid]
    assert {v['asset'] for v in observed} == {a[':answer/value'] for a in raw[sid][':question/answer-fields'][0][':answer-field/choices']}
    for row, obs in zip(bank, observed):
        for value, measured in zip(row, obs['raster_slopes']):
            assert measured == 'inf' if value == g.sp.oo else abs(math.atan(float(value))-math.atan(measured)) < .06
    key = raw[sid][':question/answer-fields'][0].get(':answer-field/correct')
    if key: assert key[':answer/value'] == observed[bank.index(g.banks(m['template'],m['parameters'],sid)[0])]['asset']
    source_records.append(record)
save('source-replays.json', source_records)

records = []
for old in json.loads((E/'generated.json').read_text()):
    m = old['generation']
    record = verify(g.generate('easy', m['seed'], template=m['template'],
                               profile=m['bank_profile'], parameters=m['parameters']))
    assert semantics(record) == semantics(old)
    records.append(record)
byid = {r['question'][':question/id']: r for r in records}
controls = json.loads((E/'counterfactuals.json').read_text())
for case in controls:
    a,b,c = [byid[case[k]] for k in ('base_id','negated_equation_id','changed_point_id')]
    assert geometry(b) == [str(-F(v)) for v in geometry(a)] != geometry(a)
    index = case['changed_index']
    assert geometry(c)[index] != geometry(a)[index]
    assert all(geometry(c)[i] == geometry(a)[i] for i in range(3) if i != index)
# Boundary/invalid inputs and whole-bank rejection remain strict.
for template,p in [
    ('rational_square', {'a':1,'points':[[0,1],[1,2],[2,3]]}),
    ('affine', {'a':1,'b':2,'points':[[1,1],[1,1],[2,2]]}),
    ('affine', {'a':1,'b':2,'points':[[5,1],[1,2],[2,3]]}),
    ('affine', {'a':1,'b':2,'points':[[-1,-1],[0,0],[1,1]]})]:
    try: g.generate('easy', template=template, parameters=p)
    except ValueError: pass
    else: raise AssertionError('Expected rejection')
records += roots[0]
save('delivery-input.json', records)
command = [sys.executable, str(REPO/'generate/pipeline/check_delivery.py'),
           '--input',str(OUT/'delivery-input.json'),'--source',str(SOURCE/'source.json'),
           '--inventory',str(SOURCE/'inventory.json'),'--difficulty','easy',
           '--output',str(OUT/'delivery'),'--asset-root',str(E/'assets'),'--math-root',str(MATH)]
subprocess.run(command, check=True, capture_output=True, text=True)
accepted = json.loads((OUT/'delivery/accepted.json').read_text())
assert {r['generation']['mathematical_fingerprint'] for r in records} == {r['generation']['mathematical_fingerprint'] for r in accepted}
# Recover normalized-path geometry by image hash, not answer IDs.
geom = {hashlib.sha256(Path(name).read_bytes()).hexdigest(): slopes
        for r in records for name,slopes in r['generation']['choice_geometry'].items()}
for record in accepted:
    for a in field(record)[':answer-field/choices']:
        record['generation']['choice_geometry'][a[':answer/value']] = geom[Path(a[':answer/value']).stem]
variation = {'before_delivery':probes(records), 'after_delivery':probes(accepted),
             'counterfactual_forms':len(controls),'semantic_instances_before':len({r['generation']['mathematical_fingerprint'] for r in records}),
             'semantic_instances_after':len({r['generation']['mathematical_fingerprint'] for r in accepted}),
             'normal_bank_probe_evidence':'../bank-probes-before.json',
             'limits':'Bounded regression of unchanged sampling/banks. Prior normal 40-per-form probe retained; these controlled samples do not estimate population frequencies. Captured inventory filtering exercised; live learner history/weighted selection unavailable.'}
# No strategy may be a deterministic predictor across the tested records within a form.
for stage in ('before_delivery','after_delivery'):
    for template, report in variation[stage].items():
        assert report['records'] >= 3
        assert all(stat['successes'] < stat['attempts'] for stat in report['strategies'].values()), (stage, template)
save('pedagogical-variation.json', variation)
cases = []
for i,record in enumerate(source_records+records+accepted):
    f = field(record)
    cases.append({'label':f'asset repair {i}', 'record':record, 'checks':[
        {'submitted_answer_id':a[':answer/id'],
         'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected',
         'purpose':'Complete bank, source replay, controlled evidence changes, normalized delivery'}
        for a in f[':answer-field/choices']]})
save('engine-input.json', cases)
grader = [str(REPO/'generate/runs/current/check-engine'),str(OUT/'engine-input.json'),str(OUT/'engine-report.json')]
subprocess.run(grader, check=True, capture_output=True, text=True)
# A fresh relocated record, changed target, and original vertical distractors.
save('render-records.json', [roots[1][0],byid[controls[0]['changed_point_id']],source_records[3]])
save('result.json', {'passed':True,'repair':'Explicit configured asset references; IDs/semantics unchanged',
                    'runs':runs,'source_banks':7,'source_choices':35,
                    'regression_records':len(records),'controlled_forms':6,'invalid_cases':4,
                    'native_checks':len(cases)*5,'accepted':len(accepted),
                    'runtime_hashes':{n:hashlib.sha256((W/n).read_bytes()).hexdigest() for n in manifest['files']},
                    'commands':[command,grader], 'filter_report':'delivery/delivery.json',
                    'variation_report':'pedagogical-variation.json'})
print(json.dumps({'passed':True,'source_banks':7,'regression_records':len(records),
                  'delivered':len(accepted),'native_checks':len(cases)*5}))
