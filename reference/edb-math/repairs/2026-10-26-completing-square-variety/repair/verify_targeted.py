"""Check the changed sampler and final outputs using retained independent math checks."""
import ast
import copy
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
from fractions import Fraction as F

import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

D = Path(__file__).resolve().parent
R = next(p for p in D.parents if (p / 'scripts/generator_pipeline.py').is_file())
E = D / 'review'
sys.path.insert(0, str(R / 'scripts'))
from generator_pipeline import digest

def read(path):
    return json.loads(Path(path).read_text())

def save(name, value):
    (E / name).write_text(json.dumps(value, indent=2) + '\n')

spec = importlib.util.spec_from_file_location('shared_math_format', R / 'scripts/question_capture/math_format.py')
mf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mf)
# Reuse the previous verifier's visible-prompt, displayed-step, and field-scope
# checks, rather than deriving expected answers from generator metadata.
tree = ast.parse((E / 'prior/independent-audit.py').read_text())
names = {'enum', 'key', 'expr', 'shown', 'boundaries', 'path'}
functions = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name in names]
assert {node.name for node in functions} == names
exec(compile(ast.Module(body=functions, type_ignores=[]), 'retained-independent-math', 'exec'))

state = read(D / 'job.json')
binding = read(E / 'final-binding.json')
all_records, observations, paths, cases, delivery = [], {}, [], [], {}
for band, batch in state['verification_batches'].items():
    records = read(batch['batch_file'])
    assert digest(records) == binding['verification_batches'][band]['batch_hash']
    ref = 'final-' + band + '.json'
    save(ref, records)
    checked = []
    for index, record in enumerate(records):
        observation, answer_paths = path(record, ref)
        checked.append(observation)
        paths.extend(answer_paths)
        checks = []
        for field_index, field in enumerate(record['question'][':question/answer-fields']):
            value = expr(key(field))
            for submitted, expected, purpose in (
                (str(value), 'accepted', 'Exact independently checked value'),
                (str(float(value)), 'accepted', 'Equivalent decimal'),
                (f'{2 * value.p}/{2 * value.q}', 'accepted', 'Equivalent unreduced fraction'),
                (str(value + F(1, 4)), 'rejected', 'Nearby wrong value'),
                (str(-value) if value else '1', 'rejected', 'Sign error or nonzero answer for zero'),
            ):
                checks.append({'field_index': field_index, 'submitted': submitted,
                               'expected': expected, 'purpose': purpose})
        cases.append({'label': band + ':' + str(index), 'record': record, 'checks': checks})
    assert len({row['m'] for row in checked}) == len(checked)
    assert {row['case'] for row in checked[:3]} == {'negative', 'zero', 'positive'}
    observations[band] = checked
    all_records.extend(records)
    output = E / ('delivery-' + band)
    command = [sys.executable, str(R / 'generate/pipeline/check_delivery.py'),
               '--input', str(E / ref), '--source', str(D / 'source/source.json'),
               '--inventory', str(D / 'source/inventory.json'), '--difficulty', band,
               '--output', str(output), '--asset-root', batch['assets_directory'],
               '--math-root', '/media/jake/SSD/EDB/math']
    result = subprocess.run(command, text=True, capture_output=True, check=True)
    survivors = read(output / 'accepted.json')
    survivor_coefficients = [str(shown(record)[2]) for record in survivors]
    assert len(set(survivor_coefficients)) == len(survivor_coefficients)
    delivery[band] = {'generated': len(records), 'survived': len(survivors),
                      'distinct_coefficients': survivor_coefficients,
                      'report': 'delivery-' + band + '/delivery.json'}

save('final-records.json', all_records)
save('independent-math.json', observations)
save('solution-paths.json', {'cases': paths})
save('delivery-summary.json', delivery)
save('grading-input.json', cases)
result = subprocess.run([str(R / 'generate/runs/current/check-engine'),
                         str(E / 'grading-input.json'), str(E / 'grading-report.json')],
                        text=True, capture_output=True, check=True)
save('grading-command.json', {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode})
print(json.dumps({'passed': True, 'final_records': len(all_records), 'native_checks': sum(len(c['checks']) for c in cases),
                  'delivery': delivery}, indent=2))
