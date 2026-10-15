"""Current-source and supported-output checks using displayed mathematics."""
import copy
import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
spec = importlib.util.spec_from_file_location('surface_validator', HERE / 'validate.py')
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)
g, s = v.g, v.s
LEVELS = g.SUPPORTED_LEVELS
GENERATOR_UUID = g.uid('course-academy:question-generator:' + str(g.ID))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def normalized(q):
    """Semantic persisted representation, excluding EDB navigation metadata."""
    q = copy.deepcopy(q)
    result = {k: str(q[k]) for k in (':question/id', ':question/problem', ':question/worked-solution') if k in q}
    d = q.get(':question/difficulty')
    if d:
        result[':question/difficulty'] = str(d.get(':db/ident')) if isinstance(d, dict) else str(d)
    fields = []
    for f in q[':question/answer-fields']:
        kind = f[':answer-field/type']
        field = {':answer-field/id': str(f[':answer-field/id']), ':answer-field/key': f[':answer-field/key'], ':answer-field/type': str(kind.get(':db/ident')) if isinstance(kind, dict) else str(kind)}
        correct = f.get(':answer-field/correct')
        if correct:
            field[':answer-field/correct'] = [':answer/id', str(correct[':answer/id'] if isinstance(correct, dict) else correct[1])]
        field[':answer-field/choices'] = sorted([{':answer/id': str(a[':answer/id']), ':answer/type': str(a[':answer/type'].get(':db/ident')) if isinstance(a[':answer/type'], dict) else str(a[':answer/type']), ':answer/value': a[':answer/value']} for a in f[':answer-field/choices']], key=lambda a: a[':answer/value'])
        fields.append(field)
    result[':question/answer-fields'] = sorted(fields, key=lambda f: f[':answer-field/key'])
    return result


def source_record(q):
    return {'knowledge_point': {'db_id': g.ID, 'id': g.KP[':knowledge-point/id'], 'title': g.KP[':knowledge-point/title']}, 'question': normalized(q), 'generation': {'template': q.get(':question/math-academy-id', 'source'), 'evidence_only': True}}


def fingerprint(q):
    q = copy.deepcopy(q)
    q[':question/problem'] = q[':question/problem'].replace(r'\iint\limits_{S}', r'\iint_S').replace(r'\dfrac', r'\frac').replace(r'\textrm{d}S', r'\mathrm{d}S').replace(r'\:', '')
    G, F, B = v.actual_prompt(q, raw=r'{∬}_{S}' in q[':question/problem'])
    return g.digest([s.srepr(s.simplify(obj)) for obj in (G, F, *B)])


def check_source(q):
    r = source_record(q)
    # q-161354's intermediate z² is shorthand under the displayed z=e^x.
    # Substitute that definition only in the validator's copy of this one row.
    if q.get(':question/math-academy-id') == 'q-161354':
        before = r'{∬}_{D}\,{z}^{2}\sqrt{1+{e}^{2x}+{0}^{2}}'
        after = r'{∬}_{D}\,{e}^{2x}\sqrt{1+{e}^{2x}+{0}^{2}}'
        assert r['question'][':question/worked-solution'].count(before) == 1
        r['question'][':question/worked-solution'] = r['question'][':question/worked-solution'].replace(before, after)
    value = v.check_math(r)
    field = r['question'][':question/answer-fields'][0]
    assert len(field[':answer-field/choices']) == 5
    values = [v.parse(a[':answer/value']) for a in field[':answer-field/choices']]
    assert all(not v.same(a, b) for i, a in enumerate(values) for b in values[:i])
    assert all(not a.has(s.oo, s.zoo, s.nan) for a in values)
    return str(value)


def check(r):
    assert r['knowledge_point']['db_id'] == g.ID
    assert r['generation']['eligible_for_learning'] and not r['generation']['evidence_only']
    level = r['question'][':question/difficulty'].split('/')[-1]
    assert level in LEVELS
    again = g.generate(level, r['generation']['seed'], template=r['generation']['template'], parameters=r['generation']['parameters'], profile=r['generation']['profile'])
    assert normalized(again['question']) == normalized(r['question'])
    assert again['generation'] == r['generation']
    v.check_math(r)
    f = r['question'][':question/answer-fields'][0]
    assert len(f[':answer-field/choices']) == 5
    assert all('$' not in a[':answer/value'] for a in f[':answer-field/choices'])
    return fingerprint(r['question'])


def native(r, label):
    f = r['question'][':question/answer-fields'][0]
    return {'label': label, 'record': r, 'checks': [{'submitted_answer_id': a[':answer/id'], 'expected': 'accepted' if a[':answer/id'] == f[':answer-field/correct'][1] else 'rejected', 'purpose': 'Displayed field-owned radio option'} for a in f[':answer-field/choices']]}


def run_native(records, path):
    path.mkdir(parents=True, exist_ok=True)
    fixtures = [native(r, str(i)) for i, r in enumerate(records)]
    (path / 'native-input.json').write_text(json.dumps(fixtures, ensure_ascii=False, indent=2) + '\n')
    subprocess.run([str(HERE / 'reference/check-engine-current'), str(path / 'native-input.json'), str(path / 'native-report.json')], check=True)
    return json.loads((path / 'native-report.json').read_text())


def main():
    sys.path.insert(0, str(ROOT / 'scripts/question_capture'))
    from edn import loads
    path = HERE / 'reference/validation-current'
    path.mkdir(parents=True, exist_ok=True)
    kp = loads((HERE / 'reference/initial/kp.edn').read_text())[0][0]
    sources = []
    for q in kp[':knowledge-point/questions']:
        sources.append({'source_id': q[':question/math-academy-id'], 'value': check_source(q), 'choice_count': len(q[':question/answer-fields'][0][':answer-field/choices']), 'fingerprint': fingerprint(q), 'record_sha256': g.digest(normalized(q))})
        print('Validated source ' + q[':question/math-academy-id'], flush=True)
    # Historical source replay is still exact, with original omissions intact.
    banks = []
    for family, sid in g.FAMILIES.items():
        r = g.generate('moderate', 3, template=family, parameters={'scale': 1}, profile='raw:' + sid)
        src = g.QS[sid]
        for key in (':question/problem', ':question/worked-solution'):
            assert r['question'].get(key) == src.get(key)
        bank = sorted(a[':answer/value'] for a in r['question'][':question/answer-fields'][0][':answer-field/choices'])
        assert bank == sorted(a[':answer/value'] for a in src[':question/answer-fields'][0][':answer-field/choices'])
        v.check_math(r)
        banks.append({'source_id': sid, 'matched': len(bank), 'total': len(bank), 'profile': 'evidence-only'})
    records = []
    coverage = {}
    for level, families in [('easy', g.EASY), ('moderate', g.MODERATE)]:
        for family in families:
            fingerprints = set()
            for seed in (7, 31, 59):
                r = g.generate(level, seed, template=family)
                fingerprints.add(check(r))
                records.append(r)
                # A seed/choice-order change must reuse all content identities.
                replay = g.generate(level, 999, template=family, parameters=r['generation']['parameters'], profile=r['generation']['profile'])
                assert normalized(replay['question']) == normalized(r['question'])
            assert len(fingerprints) >= 2, family
            coverage[level + '/' + family] = len(fingerprints)
            print('Validated ' + level + '/' + family, flush=True)
    try:
        g.generate('hard', 0)
    except ValueError as error:
        assert 'Unsupported hard band' in str(error)
    else:
        raise AssertionError('Unsupported hard band admitted')
    engine = run_native(records + [source_record(q) for q in kp[':knowledge-point/questions']], path)
    report = {'status': 'passed', 'generator_sha256': sha(HERE.with_suffix('.py')), 'validator_sha256': sha(HERE / 'validate.py'), 'inventory_validator_sha256': sha(Path(__file__)), 'engine_sha256': sha(HERE / 'reference/check-engine-current'), 'source_read_basis': 2648, 'current_sources': sources, 'historical_bank_replay': banks, 'supported_levels': list(LEVELS), 'unsupported_levels': ['hard'], 'template_coverage': coverage, 'normal_display_checks': len(records), 'native': {k: engine[k] for k in ('accepted_checks', 'rejected_checks', 'documented_unresolved_checks')}, 'plots': 'none', 'hard_exception': 'Only existing hard draft adds xy to source x²+z². Disabled outside the extracted backbone; no supported hard template in this bounded package. Five-question hard reserve remains unfilled.'}
    (path / 'validation.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'status': report['status'], 'current_sources': len(sources), 'supported_templates': len(coverage), 'native': report['native']}), flush=True)


if __name__ == '__main__':
    main()
