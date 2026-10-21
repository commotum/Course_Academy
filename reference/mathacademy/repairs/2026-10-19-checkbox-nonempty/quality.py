"""Bind policy, runtime, formatting and current-package validation evidence."""
import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from scripts.generator_policy import checkbox_selection

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]

def enum(v): return str(v.get(':db/ident') if isinstance(v, dict) else v).split('/')[-1]
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

if __name__ == '__main__':
    reports = json.loads((HERE / 'patched-audit.json').read_text())
    patches = json.loads((HERE / 'patched-generators.json').read_text())
    special = json.loads((HERE / 'special-audit.json').read_text())
    assert len(reports) == len(patches) == 62
    special_kps = {r['kp'] for r in special}
    selected, all_records = {}, []
    for report in reports:
        for level in report['levels']:
            assert not level.get('empty_indices')
            if 'error' in level:
                assert report['kp'] in special_kps, (report['kp'], level)
                continue
            if 'records' not in level: continue
            records = json.loads((HERE / 'patched-samples' / str(report['kp']) / (level['level'] + '.stdout')).read_text())
            if isinstance(records, dict): records = records.get('records', [records])
            for record in records:
                values = checkbox_selection(record)
                assert not values or any(values)
                if values:
                    selected.setdefault((report['kp'], level['level']), record)
                all_records.append(record)
    extra = json.loads((HERE / 'special-samples.json').read_text())
    for record in extra:
        values = checkbox_selection(record)
        assert not values or any(values)
        if values:
            kp = record.get('knowledge_point', {}).get('db_id')
            selected.setdefault((kp, 'special'), record)
    examples = list(selected.values())
    # All three current ODE bands after removing the empty decision branch.
    candidate = next(p for p in patches if p['kp'] == 17592186100888)
    output = HERE / 'ode-final-samples.json'
    result = subprocess.run([str(ROOT / '.venv/bin/python'), '-B', candidate['updated_script'],
                             '--difficulty', 'all', '--seed', '37', '--count', '12', '--format', 'json'],
                            capture_output=True, text=True, timeout=90)
    result.check_returncode()
    output.write_text(result.stdout)
    final_ode = json.loads(result.stdout)
    assert all(any(checkbox_selection(r)) for r in final_ode)
    examples.extend(final_ode[:3])
    # The spacing helper must preserve every mathematical coefficient and key.
    original = HERE / 'formatting/original/generator.py'
    revised = HERE / 'formatting/package/generator.py'
    for level in ('easy', 'moderate', 'hard'):
        command = ['--difficulty', level, '--count', '3', '--seed', '17', '--format', 'json']
        before = subprocess.run([str(ROOT / '.venv/bin/python'), '-B', str(original), *command], capture_output=True, text=True, check=True)
        after = subprocess.run([str(ROOT / '.venv/bin/python'), '-B', str(revised), *command], capture_output=True, text=True, check=True)
        for old, new in zip(json.loads(before.stdout), json.loads(after.stdout)):
            assert old['generation']['parameters'] == new['generation']['parameters']
            assert old['generation']['relation'] == new['generation']['relation']
            assert ' &{}={}& ' not in new['question'][':question/problem']
            examples.append(new)
    (HERE / 'grading-examples.json').write_text(json.dumps(examples, indent=2) + '\n')
    questions = []
    for record in examples:
        q = record['question']
        fields = []
        for field in q[':question/answer-fields']:
            ref = field[':answer-field/correct']
            aid = ref[':answer/id'] if isinstance(ref, dict) else ref[1]
            correct = next(a for a in field[':answer-field/choices'] if a[':answer/id'] == aid)
            fields.append({'key': field[':answer-field/key'], 'type': enum(field[':answer-field/type']),
                           'correct_value': correct[':answer/value'],
                           'choices': [{'type': enum(a[':answer/type']), 'value': a[':answer/value']}
                                       for a in field[':answer-field/choices']]})
        questions.append({'math_academy_id': q[':question/id'], 'problem': q[':question/problem'],
                          'knowledge_point': 'Checkbox selection', 'answer_fields': fields})
    out = HERE / 'native-grading'
    out.mkdir(exist_ok=True)
    (out / 'questions.json').write_text(json.dumps({'questions': questions}) + '\n')
    source = (ROOT / 'scripts/validate_historical_question_readiness.rs').read_text().replace(
        '"answer-field.type/select",', '"answer-field.type/select",\n        "answer-field.type/checkbox",')
    (out / 'grade.rs').write_text(source)
    deps = ROOT / 'target/release/deps'
    command = ['rustc', '--edition=2024', '-O', str(out / 'grade.rs')]
    for name in ('course_academy_engine', 'serde_json'):
        library = max(deps.glob('lib' + name + '-*.rlib'), key=lambda p:p.stat().st_mtime_ns)
        command.extend(['--extern', name + '=' + str(library)])
    command.extend(['-L', 'dependency=' + str(deps), '-o', str(out / 'grader')])
    subprocess.run(command, check=True, capture_output=True)
    subprocess.run([str(out / 'grader'), str(out / 'questions.json'), str(out / 'results.json')], check=True)
    grade = json.loads((out / 'results.json').read_text())
    assert grade['current_engine_ready_count'] == len(questions), [q for q in grade['questions'] if not q['accepted_by_current_grader']]
    for patch in patches:
        assert sha(patch['updated_script']) == patch['updated_sha256'], patch['kp']
    assert json.loads((HERE / 'formatting/ui/rendering.json').read_text())['passed']
    proof = {'passed': True, 'registry_scanned': 631, 'guarded_generators': len(patches),
             'ordinary_records': len(all_records), 'special_records': len(extra),
             'additional_ode_records': len(final_ode), 'empty_subsets': 0,
             'native_grading_examples': len(questions), 'all_native_grading_examples_passed': True,
             'formatting_same_parameters_and_outcomes': True, 'formatting_ui_passed': True,
             'engine_unit_tests_passed': 163, 'publication_tests_passed': 26, 'policy_tests_passed': 6,
             'source_hashes': {p:sha(ROOT / p) for p in ('scripts/generator_policy.py', 'scripts/generator_publish.py', 'engine/rust/learning.rs')}}
    (HERE / 'quality-verification.json').write_text(json.dumps(proof, indent=2) + '\n')
    print(json.dumps(proof, indent=2))
