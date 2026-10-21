"""Targeted independent checks for the newly restored complete bank."""
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

sys.dont_write_bytecode = True
E = Path(__file__).resolve().parent
J = E.parent
P = J / 'workspace'
sys.path.insert(0, str(P))
import generator as g
from oracle import oracle, unpack

def save(name, value):
    (E/name).write_text(json.dumps(value, indent=2)+'\n')

commands = []
for path in ['regression-failing/checks/source_coverage.py',
             'regression-current/checks/source_coverage.py', 'assert_source_coverage.py']:
    command = [sys.executable, '-B', str(E/path)]
    result = subprocess.run(command, capture_output=True, text=True)
    commands.append(dict(command=command, exit_code=result.returncode,
                         stdout=result.stdout, stderr=result.stderr))
assert commands[0]['exit_code'] != 0
assert commands[1]['exit_code'] == commands[2]['exit_code'] == 0
# Identify the failing case independently, rather than infer from generic exceptions.
old_spec = importlib.util.spec_from_file_location('old_generator', E/'regression-failing/generator.py')
old = importlib.util.module_from_spec(old_spec)
old_spec.loader.exec_module(old)
source = json.load(open(J/'source/source.json'))['material']['kp'][':knowledge-point/questions']
q = next(q for q in source if q[':question/math-academy-id'] == 'q-129207')
params = {'matrix': [[2,-5,9,3],[0,7,0,8],[0,0,3,1],[0,0,-7,-1]], 'rows': [1,2,3]}
try:
    old.generate(seed=817, profile='q-129207', parameters=params, replay=True)
except ValueError as ex:
    failure = dict(profile='q-129207', source_id=q[':question/id'], seed=817,
                   parameters=params, expected_bank=[3,12,9,-3,1], expected_answer=3,
                   old_exception=str(ex))
else:
    raise AssertionError('Old package did not reproduce prior failure')
repaired = g.generate(seed=817, profile='q-129207', parameters=params, replay=True)
assert oracle(repaired)['total'] == 3
assert sorted(unpack(repaired)['bank']) == [-3,1,3,9,12]
failure['current_record'] = repaired
save('prior-counterexample.json', failure)
save('repair-regression-verification.json', commands)

# Each rank of the new numeric bank profile, with fresh reproducible seeds.
new_records = [g.generate(seed=420371+100*rank+k, profile='q-129207', anchor_rank=rank)
               for rank in range(5) for k in range(6)]
for r in new_records:
    assert oracle(r)['rank'] == r['generation']['bank_anchor_rank']
save('new-profile-records.json', new_records)

# Three-row controlled pairs for the repaired family. Keep seed, bank anchor,
# and all matrix cells constant except the named evidence change.
base = {'matrix': [[0,2,5,-1],[0,0,-3,7],[4,0,6,-2],[0,0,0,6]], 'rows': [0,1,2]}
parameters = [('base', base)]
p = copy.deepcopy(base); p['matrix'][0][1] = 3; parameters.append(('leading_value', p))
p = copy.deepcopy(base); p['matrix'][0][0] = 5; parameters.append(('earlier_nonzero', p))
p = copy.deepcopy(base); p['rows'] = [0,1,3]; parameters.append(('target_rows', p))
p = copy.deepcopy(base); p['matrix'][0][2] = 9; parameters.append(('trailing_value', p))
p = copy.deepcopy(base); p['matrix'][3] = [-9,8,7,6]; parameters.append(('unselected_row', p))
pairs = [g.generate(seed=712931, profile='q-129207', parameters=p, anchor_rank=2)
         for label,p in parameters]
expected = [3,4,6,5,3,3]
results = []
for (label,p),r,total in zip(parameters,pairs,expected):
    actual = oracle(r)
    assert actual['total'] == total
    results.append(dict(case=label, expected=total, observed=actual,
                        prompt=r['question'][':question/problem'],
                        solution=r['question'][':question/worked-solution']))
save('new-counterfactual-records.json', pairs)
save('new-counterfactual-results.json', results)

fresh = json.load(open(E/'fresh-records.json')) + new_records
save('fresh-records.json', fresh)
grade = json.load(open(E/'grader-input.json'))
for i,r in enumerate(new_records+pairs):
    answer=oracle(r)['total']; f=r['question'][':question/answer-fields'][0]
    grade.append(dict(label=f'new-profile-{i}', record=r, checks=[
        dict(submitted_answer_id=c[':answer/id'],
             expected='accepted' if int(c[':answer/value'])==answer else 'rejected',
             purpose='Independent visible first-nonzero sum, including controlled pairs')
        for c in f[':answer-field/choices']]))
save('grader-input.json', grade)
save('render-records.json', json.load(open(E/'batch-records.json')) + pairs + [repaired])
save('supplemental-results.json', dict(new_profile_samples=len(new_records),
     new_profile_math_pass=True, counterfactuals=results,
     old_counterexample_reproduced=True, current_counterexample_pass=True,
     sampling_attempts=[r['generation']['value_sampling_attempts'] for r in new_records],
     command=[sys.executable,'-B',str(E/'supplemental.py')]))
(E/'session-state.md').write_text('All 15 source banks replay independently. Retained author regression fails on old package and passes on current disposable copy; independent regression also passes. 90 small regression samples, 30 new-profile samples, 44 boundary cases, 12 controlled records and exact batch math checked. Native grading, delivery, actual UI and decision analysis pending. Package unchanged.\n')
print(json.dumps({'source_banks':15, 'new_profile_samples':len(new_records),
                  'controlled_answers':expected, 'native_grader_records':len(grade)}))
