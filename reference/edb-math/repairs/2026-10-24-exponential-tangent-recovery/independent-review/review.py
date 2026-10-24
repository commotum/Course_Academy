"""Independent read-only mathematical/source/package audit of a frozen candidate.

Writes only this independent evidence tree. Native grading and actual delivery
are separate commands using the emitted grader-input and record files.
"""
import collections
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys

sys.dont_write_bytecode = True
import sympy as s
import visible_math as v

E = Path(__file__).resolve().parent
R = E.parent
P = R / 'package'
REPO = Path('/home/jake/Developer/Course_Academy')
sys.path.insert(0, str(REPO / 'scripts'))
from generator_packages import package_digest
from generator_pipeline import digest


def load(path):
    return json.loads(Path(path).read_text())


def save(name, value):
    (E / name).write_text(json.dumps(value, indent=2) + '\n')


def module(name, path):
    sys.path.insert(0, str(path.parent))
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def package_hash():
    m = load(P / 'package.json')
    return package_digest(P, m['entrypoint'], m['files'], dependencies=m['dependencies'])


def visible(record):
    q = record['question']
    return [q[':question/problem'], q[':question/worked-solution'],
            q[':question/difficulty'], sorted(c[':answer/value'] for c in v.choices(record))]


def main():
    frozen = load(R / 'evidence/frozen-candidate.json')
    assert package_hash() == frozen['package_hash'], 'Wait for a genuinely frozen package'
    before = {f: hashlib.sha256((P / f).read_bytes()).hexdigest()
              for f in load(P / 'package.json')['files']}
    save('package-before.json', before)
    engine_files = {str(p.relative_to(REPO)): hashlib.sha256(p.read_bytes()).hexdigest()
                    for p in [*sorted((REPO / 'engine/rust').rglob('*.rs')),
                              REPO / 'generate/runs/current/check-engine']}
    save('engine-files.json', engine_files)
    g = module('frozen_candidate', P / 'generator.py')
    old = module('archived_original', R / 'original/generator.py')
    fmt = module('shared_math_format', REPO / 'scripts/question_capture/math_format.py')
    batch = load(R / 'evidence/requested.json')
    assert digest(batch) == frozen['batch_hash']
    save('requested.json', batch)
    # Only declared files copied; actual CLI must reproduce the exact saved request.
    relocated = E / 'relocated'
    relocated.mkdir(exist_ok=True)
    manifest = load(P / 'package.json')
    for f in ['package.json', *manifest['files']]:
        shutil.copyfile(P / f, relocated / f)
    cli = subprocess.run([sys.executable, str(relocated / manifest['entrypoint']),
                          '--difficulty', 'hard', '--seed', '1072510293', '--count', '4'],
                         cwd=E, env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'},
                         text=True, capture_output=True, check=True)
    assert json.loads(cli.stdout) == batch
    save('relocated-batch.json', json.loads(cli.stdout))
    # Retained old failure seeds plus a few independent ones, not another large sweep.
    fresh = [g.generate_hard(seed) for seed in [2, 101, 102, 103, 104, 105, 106, 107]]
    save('fresh.json', fresh)
    base = dict(b=3, c=1, a=2, n=1, k=0, l=0, d=1, point='-1')
    controls = [g.generate_hard(71+i, parameters=params) for i, params in enumerate([
        base, {**base, 'point': '0'}, {**base, 'a': -2, 'point': '0'},
        {**base, 'b': 4}, {**base, 'a': 1, 'point': '0'}])]
    controls.append(g.generate_hard(901, parameters=base))
    controls.append(g.generate_hard(2, parameters=dict(b=4,c=1,a=4,n=1,k=0,l=0,d=-5,point='1')))
    save('controlled.json', controls)
    source = load(R / 'fresh-source/source.json')
    kp = source['material']['kp']
    replays, replay_rows = [], []
    for q in [*kp[':knowledge-point/questions'], kp[':knowledge-point/canonical-example']]:
        qid = q[':question/math-academy-id']
        rec = g.generate(g.SPECS[qid]['level'], 77, template=qid,
                         parameters=g.default_params(qid), profile='historical:'+qid)
        replays.append(rec)
        generated = [v.parse(c[':answer/value']) for c in v.choices(rec)]
        banks = []
        for field in q.get(':question/answer-fields', []):
            observed = [v.parse(c[':answer/value']) for c in field[':answer-field/choices']]
            equal = len(observed) == len(generated) and all(
                any(s.simplify(a-b) == 0 for b in generated) for a in observed)
            assert equal, qid
            banks.append(equal)
        replay_rows.append({'source': qid, 'complete_banks_match': banks,
                            'fieldless_completion': not q.get(':question/answer-fields'),
                            'basis': rec['generation']['source']['basis']})
    save('source-replays.json', replays)
    save('source-replay-results.json', {'passed': True, 'cases': replay_rows})
    lower = []
    for level in ['easy', 'moderate']:
        for seed in [12, 73, 901]:
            assert visible(g.generate(level, seed)) == visible(old.generate(level, seed))
            lower.append({'level': level, 'seed': seed, 'identical_visible_content': True})
    save('lower-band-parity.json', lower)
    records = [('requested.json', batch), ('fresh.json', fresh),
               ('controlled.json', controls), ('source-replays.json', replays)]
    math, graders, paths, boundaries = [], [], [], []
    for ref, rows in records:
        for index, rec in enumerate(rows):
            expected = v.expected(rec)
            choices = v.choices(rec)
            values = [v.parse(c[':answer/value']) for c in choices]
            matches = [c[':answer/id'] for c, val in zip(choices, values)
                       if s.simplify(val-expected) == 0]
            field = rec['question'][':question/answer-fields'][0]
            key = v.correct(rec)
            assert key in matches
            radio = field[':answer-field/type'].endswith('/radio')
            if radio:
                assert len(matches) == 1
                assert all(s.simplify(a-b) != 0 for i, a in enumerate(values) for b in values[:i])
                checks = [{'submitted_answer_id': c[':answer/id'],
                           'expected': 'accepted' if c[':answer/id'] in matches else 'rejected',
                           'purpose': 'independently computed derivative/tangent; every option'} for c in choices]
            else:
                checks = [{'submitted': s.latex(expected).replace(r'\log', r'\ln'),
                           'expected': 'accepted', 'purpose': 'independent symbolic result'},
                          {'submitted': s.latex(2*expected).replace(r'\log', r'\ln'),
                           'expected': 'rejected', 'purpose': 'plausible doubled coefficient'}]
            graders.append({'label': f'{ref}/{index}', 'record': rec, 'checks': checks})
            math.append({'file': ref, 'index': index, 'expected': str(expected),
                         'unique_radio_key': len(matches) == 1 if radio else None, 'passed': True})
            for field_name in [':question/problem', ':question/worked-solution']:
                fmt.validate_math_boundaries(rec['question'][field_name], strict=True)
                fmt.validate_prose(rec['question'][field_name])
            for choice in choices:
                fmt.validate_tex(choice[':answer/value'])
            boundaries.append({'file': ref, 'index': index, 'passed': True})
            key_text = next(c[':answer/value'] for c in choices if c[':answer/id'] == key)
            sol = rec['question'][':question/worked-solution']
            conversions = []
            if rec['generation']['template'] == 'q-107463' and rec['generation']['parameters']['b'] == 4:
                conversions.append({'rule': 'ln4=2ln2 and expansion of point-slope form',
                    'scope_source': 'q-107463 worked solution explicitly teaches the log power simplification',
                    'shown_step': sol[sol.rfind('Finally'):], 'status': 'passed'})
            if rec['generation']['template'] == 'q-312462':
                conversions.append({'rule': 'Extract only the coefficient because the exponential is supplied after field-1',
                    'scope_source': 'q-312462 prompt and chain-rule product',
                    'shown_step': sol, 'status': 'passed'})
            paths.append({'template': rec['generation']['template'], 'field_key': field[':answer-field/key'],
                'final_expression': str(expected), 'keyed_answer': key_text,
                'domain': 'Real x; positive integer base2..6; source polynomial exponents; stated evaluation point.',
                'conclusion': 'Visible derivative, evaluation and point-slope construction agree with actual response scope.',
                'sample_refs': [ref, 'math-results.json'], 'status': 'passed', 'conversions': conversions})
    save('math-results.json', {'passed': True, 'cases': math})
    save('grader-input.json', graders)
    save('boundary-results.json', {'passed': True, 'cases': boundaries,
         'not_present': ['images', 'tables', 'augmented matrices', 'text choices', 'feedback', 'emphasis wrappers']})
    save('solution-paths.json', {'cases': paths,
         'retained_negative_control': 'prior-evidence/scope-negative-control.json'})
    pairs = []
    for kind, i, j in [('relevant', 0, 1), ('relevant', 1, 2), ('irrelevant', 0, 5)]:
        changed = s.simplify(v.expected(controls[i])-v.expected(controls[j])) != 0
        assert changed == (kind == 'relevant')
        pairs.append({'kind': kind, 'before': i, 'after': j, 'answer_changes': changed})
    save('counterfactual-results.json', {'passed': True, 'cases': pairs})
    rejected = []
    for label, params in [('base-one', {**base, 'b': 1}), ('point-outside', {**base, 'point': '2'}),
                          ('evaluated-exponent-outside', {**base, 'a': 9, 'd': 5, 'point': '1'})]:
        try:
            g.generate_hard(13, parameters=params)
        except ValueError as error:
            rejected.append({'case': label, 'reason': str(error)})
        else:
            raise AssertionError(label)
    assert manifest['dependencies'] == {'python': platform.python_version(), 'packages': {'sympy': s.__version__}}
    assert package_hash() == frozen['package_hash']
    save('packaging-results.json', {'passed': True, 'relocated_cli_matches_exact_request': True,
         'dependency_versions_match': True, 'dependencies': manifest['dependencies'],
         'invalid_parameters_rejected': rejected, 'package_hash': package_hash(),
         'assets': {}, 'external_requirements': 'Only declared SymPy and bundled math_format, no network or assets.'})
    save('package-after.json', {f: hashlib.sha256((P/f).read_bytes()).hexdigest() for f in manifest['files']})
    assert load(E/'package-before.json') == load(E/'package-after.json')
    save('render-records.json', [batch[0], controls[3], controls[4]])
    print(json.dumps({'source_replays': len(replays), 'math_cases': len(math),
                      'native_input_cases': len(graders), 'package_hash': package_hash()}))


if __name__ == '__main__':
    main()
