"""Prepare equivalent stored-question repairs and immutable package revisions."""
import copy
import importlib.util
import json
import sys
import uuid
from pathlib import Path
from checks import check_record, correct_value, displayed_rows, trivial
from scripts.generator_packages import build_manifest, manifest_digest, check_dependencies

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]

def save(name, value):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=False, default=str) + '\n')

def load_generator(kp):
    directory = HERE / 'packages' / str(kp)
    sys.path.insert(0, str(directory))
    sys.modules.pop('math_format', None)
    spec = importlib.util.spec_from_file_location('generator_' + str(kp), directory / 'generator.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def equivalent(before, after):
    for a, b in zip(before, after):
        pivot = next(i for i, value in enumerate(a) if value)
        ratio = b[pivot] / a[pivot]
        assert ratio != 0 and all(y == ratio*x for x, y in zip(a, b))

if __name__ == '__main__':
    kps = json.loads((HERE / 'knowledge-points.json').read_text())
    qs = json.loads((HERE / 'questions.json').read_text())
    owners = {q[':db/id']: kp[':db/id'] for kp in kps for q in kp[':knowledge-point/questions']}
    generators = {kp[':db/id']: load_generator(kp[':db/id']) for kp in kps}
    changes, repairs, records = [], [], []
    for q in qs:
        if ':question/math-academy-id' in q:
            continue  # Original difficulty is absent; do not invent source ratings.
        kp = owners[q[':db/id']]
        g = generators[kp]
        rows = displayed_rows(q)
        assert rows is not None
        old_level = q[':question/difficulty'][':db/ident'].split('/')[-1]
        level = old_level
        if kp == 17592186073776:
            p = dict(zip('abcdef', (int(v) for row in rows for v in row)))
            template = 'zero_rhs' if level == 'hard' else 'standard'
            try:
                g.validate_parameters(level, template, p)
                continue
            except ValueError as error:
                reason = str(error)
            candidates = [rows]
            for row in (0, 1):
                scaled = list(rows)
                scaled[row] = tuple(2*v for v in rows[row])
                candidates.append(scaled)
            eligible = []
            for candidate in candidates:
                pp = dict(zip('abcdef', (int(v) for row in candidate for v in row)))
                for band in ('easy', 'moderate') if template == 'standard' else ('hard',):
                    try: g.validate_parameters(band, template, pp)
                    except ValueError: continue
                    score = (band != 'easy', max(abs(v) for row in candidate for v in row[:2]),
                             max(abs(row[2]) for row in candidate))
                    eligible.append((score, band, pp))
            assert eligible, q[':db/id']
            _, level, p = min(eligible, key=lambda value: value[0])
            generated = g.generate(level, parameters=p)
        elif kp == 17592186073777 and trivial(rows):
            p = dict(zip('abcdef', (int(v) for row in rows for v in row)))
            for key in 'def': p[key] *= 2
            generated = g.generate(level, parameters=p)
            reason = 'Identical or sign-flipped equations'
        else:
            assert not trivial(rows), q[':db/id']
            continue
        new_rows = check_record(generated)
        equivalent(rows, new_rows)
        assert correct_value(q) == correct_value(generated['question'])
        updated = copy.deepcopy(q)
        # A difficulty-only correction need not rewrite an existing explanation.
        if rows != new_rows:
            for attr in (':question/problem', ':question/worked-solution'):
                if q[attr] != generated['question'][attr]:
                    changes.append({'entity': q[':db/id'], 'attribute': attr,
                                    'before': q[attr], 'after': generated['question'][attr]})
                    updated[attr] = generated['question'][attr]
        if old_level != level:
            attr = ':question/difficulty'
            changes.append({'entity': q[':db/id'], 'attribute': attr,
                            'before': q[attr][':db/id'], 'after': ':question.difficulty/' + level})
            updated[attr] = ':question.difficulty/' + level
        assert updated[':question/answer-fields'] == q[':question/answer-fields']
        record = {'knowledge_point': {'db_id': kp}, 'question': updated}
        check_record(record)
        records.append(record)
        repairs.append({'question': q[':db/id'], 'kp': kp, 'reason': reason,
                        'before_rows': rows, 'after_rows': new_rows,
                        'old_level': old_level, 'new_level': level,
                        'same_equation_solution_sets': True, 'answer_fields_unchanged': True})

    updates = []
    for kp in kps:
        eid = kp[':db/id']
        directory = HERE / 'packages' / str(eid)
        old = json.loads((HERE / 'original-packages' / str(eid) / 'generator-package.json').read_text())
        policy = ('Easy: standard form, multiplier magnitude 2, coefficients <=5, constants <=12.\n'
                  'Moderate: standard form, multiplier magnitude 2..4, coefficients <=10, constants <=30;\n'
                  'exclude every instance fitting easy. Hard: rearrange both zero-RHS equations;\n'
                  'nonunit multiplier 2..4, with the existing signed coefficient bounds.\n'
                  'All three outcomes are selected before instance sampling at every level.\n'
                  'These are authored bands; captured source practice questions have no ratings.\n') if eid == 17592186073776 else 'Existing difficulty workloads and source replay are retained.\n'
        (directory / 'practice-policy.md').write_text(
            '# Eligible linear systems\n\nIdentical equations and equations differing only by a sign are excluded.\n'
            'This applies to default sampling and explicit parameters for learner output.\n\n' + policy)
        manifest = build_manifest(directory, old['entrypoint'], [*old['files'], 'practice-policy.md'], dependencies=old['dependencies'])
        dependency_check = check_dependencies(manifest['dependencies'], str(ROOT / '.venv/bin/python'))
        digest = manifest_digest(manifest)
        registration = kp[':knowledge-point/question-generator']
        updates.append({'kp': eid, 'old_generator': registration, 'directory': str(directory),
                        'manifest': manifest, 'digest': digest,
                        'reference': f'generators/{digest[:2]}/{digest}/{manifest["entrypoint"]}',
                        'generator_uuid': str(uuid.uuid5(uuid.UUID(kp[':knowledge-point/id']), 'generator-package:' + digest)),
                        'dependencies': dependency_check})
    save('changes.json', changes)
    save('repairs.json', repairs)
    save('repair-records.json', records)
    save('package-updates.json', updates)
    all_records = [r for kp in kps for r in json.loads((HERE / ('samples-' + str(kp[':db/id']) + '.json')).read_text())] + records
    save('grading-records.json', all_records)
    # Original-parameter completions, controlled outcome cases and all repaired items.
    save('render-records.json', [r for r in all_records if r in records] +
         [r for r in all_records if r.get('generation', {}).get('seed') == 0][:12])
    print(json.dumps({'questions': len(repairs), 'field_changes': len(changes),
                      'equation_repairs': sum(r['before_rows'] != r['after_rows'] for r in repairs),
                      'rating_changes': sum(r['old_level'] != r['new_level'] for r in repairs),
                      'packages': len(updates)}))
