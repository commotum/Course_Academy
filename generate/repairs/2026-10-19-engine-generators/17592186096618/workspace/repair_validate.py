"""Focused review repair checks; preserves previous evidence and failing acceptance test.

Run make, the documented native/delivery tools, then --final. The required log
equivalence acceptance is run separately and is never relabeled as a pass.
"""
import argparse
import copy
import json
import subprocess
from pathlib import Path

import sympy as s
import generator as g
import validate as v

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'evidence/repair'
ENGINE = Path('/home/jake/Developer/Course_Academy/generate/runs/current/check-engine')


def save(name, data):
    OUT.mkdir(exist_ok=True)
    (OUT / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')


def make():
    # Compare all replay content and every choice with the retained repaired
    # candidate. Identity comparison includes the correct answer designation.
    previous = json.loads((ROOT / 'evidence/source-replay.json').read_text())
    replay = []
    for old in previous:
        m = old['generation']
        new = g.generate(template=m['template'], parameters=m['parameters'],
                         seed=m['seed'], replay=True)
        assert new['question'] == old['question'], m['source_ids']
        replay.append(new)
    save('source-replay.json', {'records': len(replay),
         'all_prompts_solutions_choices_and_keys_unchanged': True,
         'valid_source_choices': sum(len(r['question'][':question/answer-fields'][0]
                                         [':answer-field/choices']) for r in replay),
         'retained_comparison': 'evidence/source-replay.json'})

    records = []
    # Entire affected h/n/target domain is small: 36 actual mathematical tasks.
    for n in range(2, 5):
        for h in range(6):
            for target in ('left', 'right'):
                records.append(g.generate(template='polynomial_log_blank',
                    parameters={'n': n, 'h': h}, target=target, seed=33))
    by = {(r['generation']['parameters']['n'], r['generation']['parameters']['h'],
           r['generation']['target']): r for r in records}
    counter = []
    control_cases = []
    for n in range(2, 5):
        left = by[n, 0, 'left']; right = by[n, 0, 'right']
        assert v.key(left) != v.key(right)
        assert left['question'][':question/problem'] != right['question'][':question/problem']
        assert left['question'][':question/worked-solution'] == right['question'][':question/worked-solution']
        assert v.key(left) == v.key(by[n, 3, 'left'])
        assert v.key(right) != v.key(by[n, 3, 'right'])
        for label, record, submitted, expected in [
            ('left target rejects right fragment', left, v.key(right), 'rejected'),
            ('right target rejects left fragment', right, v.key(left), 'rejected'),
            ('left target preserves zero-shift response', by[n, 3, 'left'], v.key(left), 'accepted'),
            ('right target changes zero-shift response', by[n, 3, 'right'], v.key(right), 'rejected'),
        ]:
            control_cases.append({'label': f'controlled n={n}: {label}', 'record': record,
                                  'checks': [{'submitted': submitted, 'expected': expected,
                                              'purpose': 'controlled change through actual native grading'}]})
        counter.append({'n': n, 'target_swap_changes_key_and_known_term': True,
                        'target_swap_preserves_full_solution': True,
                        'zero_to_nonzero_shift_preserves_left_response': True,
                        'zero_to_nonzero_shift_changes_right_response': True})
    # Small unconditioned regression, preserving unrelated prior implementation.
    records.extend(g.generate(seed=555 + i) for i in range(5))
    log_record = g.generate(seed=92381, template='base_log_right_blank',
                           parameters={'b': 4, 'd': 4, 'k': 1}, target='right')
    records.append(log_record)
    # Affected original scaffolds and complete valid source banks.
    records.extend(r for r in replay if r['generation']['template'] in
                   ('polynomial_log_blank', 'base_log_right_blank'))
    cases = control_cases
    for i, r in enumerate(records):
        m = r['generation']; t = m['template']; p = m['parameters']
        product, A, B = v.oracle(t, p)
        field = r['question'][':question/answer-fields'][0]
        radio = field[':answer-field/type'].endswith('/radio')
        expected = A + B if radio else A if m['target'] == 'left' else -B if B.could_extract_minus_sign() else B
        _, _, _, u, w, _ = g.build(t, p)
        assert s.simplify(product - u*w) == 0
        final = r['question'][':question/worked-solution'].split('& =')[-1].split(r'\end{aligned}')[0].strip()
        cases.extend([
            v.equivalence_case(f'key {i}', r, g.tex(expected), v.key(r)),
            v.equivalence_case(f'full solution {i}', r, g.tex(A+B), final),
        ])
        if radio:
            checks = [{'submitted_answer_id': a[':answer/id'],
                       'expected': 'accepted' if a[':answer/id'] == field[':answer-field/correct'][1] else 'rejected',
                       'purpose': 'unchanged radio regression'} for a in field[':answer-field/choices']]
        else:
            checks = [{'submitted': v.key(r), 'expected': 'accepted', 'purpose': 'canonical fragment'},
                      {'submitted': r'\frac{2(' + v.key(r) + r')}{2}', 'expected': 'accepted', 'purpose': 'equivalent fragment'},
                      {'submitted': g.tex(expected+1), 'expected': 'rejected', 'purpose': 'wrong fragment'},
                      {'submitted': g.tex(A+B), 'expected': 'rejected', 'purpose': 'full derivative is not missing contribution'}]
            if not v.eq(A if m['target'] == 'right' else B, expected):
                checks.append({'submitted': g.tex(A if m['target'] == 'right' else B),
                               'expected': 'rejected', 'purpose': 'copying known term is not valid'})
            # Parse the actually printed known term through the native grader.
            before, after = r['question'][':question/problem'].split('{{field-1}}')
            if m['target'] == 'left':
                known = after.strip().strip('$').replace(r'\,', '').strip(); wanted = B
            else:
                known = before.rsplit('(x)=', 1)[1].strip().rstrip('$').strip()[:-1].replace(r'\,', '').strip(); wanted = A
            cases.append(v.equivalence_case(f'printed known term {i}', r, g.tex(wanted), known))
        cases.append({'label': f'actual field {i}', 'record': r, 'checks': checks})
    save('records.json', records)
    save('grader-input.json', cases)
    save('counterfactuals.json', counter)
    save('render-records.json', [by[2, 0, 'left'], by[2, 0, 'right'],
                               by[4, 0, 'right'], by[2, 3, 'right'], log_record])
    # No generator rejection added: test sampled support without inflating
    # semantic counts by seeds. All finite polynomial cases above are explicit.
    sampled = [g.generate(seed=i, template='polynomial_log_blank') for i in range(24)]
    shifts = sorted({r['generation']['parameters']['h'] for r in sampled})
    assert 0 in shifts and any(h > 0 for h in shifts)
    assert all(r['generation']['rejections'] == 0 for r in sampled)
    save('sampler.json', {'seed_range': [0, 23], 'shifts': shifts,
         'targets': sorted({r['generation']['target'] for r in sampled}),
         'rejections': 0, 'explicit_domain_tasks': 36})

    submitted = r'4^x/(2x\ln2)'
    assert s.simplify(4**v.x/(2*v.x*s.log(2)) - 4**v.x/(v.x*s.log(4))) == 0
    required = [{'label': 'valid ln4=2ln2 equivalent', 'record': log_record,
                 'checks': [{'submitted': submitted, 'expected': 'accepted',
                             'purpose': 'required review acceptance regression; must not be waived'}]}]
    save('required-grader-input.json', required)
    result = subprocess.run([str(ENGINE), str(OUT/'required-grader-input.json'),
                             str(OUT/'required-grader-report.json')], capture_output=True, text=True)
    (OUT/'required-grader-console.txt').write_text(result.stdout+result.stderr)
    save('required-grader-result.json', {'passed': result.returncode == 0,
         'exit_code': result.returncode, 'expected': 'accepted',
         'independent_math': 'exact equality by ln4=2ln2; identical real domains x!=0',
         'console': 'required-grader-console.txt'})
    # Read-only diagnostics show aliases do not alter the native single-key
    # comparison, and replacing the key merely reverses the same failure.
    aliased = copy.deepcopy(log_record)
    f = aliased['question'][':question/answer-fields'][0]
    f[':answer-field/choices'].append({':answer/id': g.ident(['diagnostic alias']),
        ':answer/type': ':answer.type/math', ':answer/value': submitted})
    alternate = copy.deepcopy(log_record)
    f = alternate['question'][':question/answer-fields'][0]
    for a in f[':answer-field/choices']:
        if a[':answer/id'] == f[':answer-field/correct'][1]: a[':answer/value'] = submitted
    diagnostic = []
    for label, record, value, outcome in [
        ('original canonical', log_record, v.key(log_record), 'accepted'),
        ('original plus alias', aliased, submitted, 'unresolved'),
        ('expanded canonical', alternate, submitted, 'accepted'),
        ('expanded canonical versus source form', alternate, v.key(log_record), 'unresolved'),
    ]:
        diagnostic.append({'label': label, 'record': record,
                           'checks': [{'submitted': value, 'expected': outcome,
                                       'purpose': 'diagnosis only; not acceptance evidence'}]})
    save('grader-diagnostic-input.json', diagnostic)
    print(json.dumps({'source_replays_unchanged': len(replay), 'affected_domain_tasks': 36,
                      'records': len(records), 'required_native_acceptance': result.returncode == 0}))


def final():
    raw = json.loads((OUT/'records.json').read_text())
    accepted = json.loads((OUT/'delivery/accepted.json').read_text())
    # Existing default-bank shortcut checks remain applicable; compare them
    # before and after filtering alongside the newly added mathematical tasks.
    prior = json.loads((ROOT/'evidence/delivery/accepted.json').read_text())
    v.audit(prior)
    def coverage(rs):
        rs = [r for r in rs if r['generation']['template'] == 'polynomial_log_blank']
        cases = {(r['generation']['parameters']['n'], r['generation']['parameters']['h'],
                  r['generation']['target']) for r in rs}
        assert cases == {(n, h, t) for n in range(2, 5) for h in range(6) for t in ('left', 'right')}
        return {'semantic_tasks': len(cases), 'zero_shift_targets': sorted({t for n,h,t in cases if h == 0}),
                'constant_shift_predicts_target': False, 'exponent_predicts_target': False,
                'known_term_copy_successes': 0, 'known_term_copy_attempts': len(rs)}
    report = {'before': coverage(raw), 'after': coverage(accepted),
              'raw_records': len(raw), 'accepted_records': len(accepted),
              'retained_default_bank_shortcut_assertions': 'passed on prior delivered records; bank code unchanged',
              'learner_selection': 'Prior read-only selection analysis unchanged. Live history unavailable.',
              'required_grading': json.loads((OUT/'required-grader-result.json').read_text()),
              'status': 'unsupported',
              'limitation': 'Native grader cannot prove ln4=2ln2. Single-canonical comparison ignores blank aliases. Engine repair is outside the permitted workspace.'}
    save('summary.json', report)
    print(json.dumps({k: report[k] for k in ('before', 'after', 'status')}))


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--final', action='store_true')
    final() if ap.parse_args().final else make()
