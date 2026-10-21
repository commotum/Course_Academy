"""Exercise each package independently; no database writes."""
import importlib.util
import json
import random
import sys
from collections import Counter
from pathlib import Path
from checks import check_record, displayed_rows, trivial

HERE = Path(__file__).resolve().parent
kp = int(sys.argv[1])
directory = HERE / 'packages' / str(kp)
sys.path.insert(0, str(directory))
spec = importlib.util.spec_from_file_location('generator_under_test', directory / 'generator.py')
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)

counts = {}
records = []
structural_per_level = 1000 if kp == 17592186073778 else 10000
for level in g.LEVELS:
    outcomes = Counter()
    for seed in range(structural_per_level):
        rng = random.Random(seed)
        if kp == 17592186073776:
            branch = rng.choice(g.VALUES)
            p = g.sample(level, rng, branch)
            assert g.result(p) == branch
            outcomes[branch] += 1
            rows = [tuple(p[k] for k in 'abc'), tuple(p[k] for k in 'def')]
        elif kp == 17592186073777:
            p = g.sample(level, rng)
            p = g.validate_parameters(level, g.LEVELS[level], p)
            outcomes[g.relation(p)[0]] += 1
            rows = [tuple(p[k] for k in 'abc'), tuple(p[k] for k in 'def')]
        else:
            p, _, _, details = g.sample_instance(level, rng, 'radio_family')
            rows = g.rows(p)
            outcomes[details['fractional_case']] += 1
        assert not trivial(rows), (level, seed, p)
    if kp != 17592186073778:
        assert len(outcomes) == 3
    counts[level] = dict(outcomes)
    templates = g.TEMPLATES if kp == 17592186073778 else [None]
    for template in templates:
        for seed in range(30):
            record = g.generate(level, seed=seed, template=template)
            check_record(record)
            if seed == 0:
                assert record == g.generate(level, seed=seed, template=template)
            records.append(record)

rejections = []
for sign in (1, -1):
    try:
        if kp == 17592186073776:
            g.generate('easy', parameters=dict(zip('abcdef', (2,-1,4,2*sign,-sign,4*sign))))
        elif kp == 17592186073777:
            g.generate('hard', parameters=dict(zip('abcdef', (5,-2,-1,5*sign,-2*sign,-sign))))
        else:
            p = g.parameters(dict(a=2,b=1,c=3,r=sign,variable='x'))
            g.build_record('easy', p, 'blank_coordinate', [], 0, 0, {})
    except ValueError as error:
        rejections.append(str(error))
    else:
        raise AssertionError('Explicit trivial parameters accepted')

source_checks = []
if kp == 17592186073776:
    sources = [
        ('moderate', 'raw_211984', (6,4,6,-2,-1,5)),
        ('hard', 'raw_237043', (-3,1,2,-12,4,8)),
        ('moderate', 'raw_237046', (2,-5,15,4,-10,-10)),
    ]
    for level, profile, values in sources:
        record = g.generate(level, profile=profile, parameters=dict(zip('abcdef', values)))
        check_record(record)
        records.append(record)
        source_checks.append(profile)
    # Each level has the same coefficients/constants across controlled cases;
    # only the evidence needed to change the correct classification changes.
    for level in g.LEVELS:
        base = (1,1,1,2,2,2) if level == 'easy' else (2,1,2,6,3,6)
        for branch in ('infinite', 'none', 'one'):
            values = list(base)
            if branch == 'none': values[-1] += 1
            if branch == 'one': values[-2] += 1 if level != 'hard' else -1
            record = g.generate(level, parameters=dict(zip('abcdef', values)))
            check_record(record)
            records.append(record)
else:
    source_ids = ('q-211986', 'q-237095') if kp == 17592186073777 else ('q-25524', 'q-208832')
    for source_id in source_ids:
        g.replay_source(source_id)
        source_checks.append(source_id)

(HERE / ('samples-' + str(kp) + '.json')).write_text(json.dumps(records, indent=2) + '\n')
report = {'passed': True, 'kp': kp, 'version': g.VERSION,
          'structural_instances': 3*structural_per_level, 'level_counts': counts,
          'public_records': len(records), 'trivial_instances': 0,
          'explicit_trivial_rejections': rejections, 'source_profiles': source_checks,
          'deterministic_replay': True}
(HERE / ('audit-' + str(kp) + '.json')).write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report), flush=True)
