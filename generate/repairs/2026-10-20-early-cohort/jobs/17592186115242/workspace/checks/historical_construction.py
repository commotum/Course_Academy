"""Test current construction at historical parameters without waiving inventory.

Writes workspace evidence only. The separate strict inventory regression remains
authoritative for stored-pool remediation and must still be executed.
"""
import json
import subprocess
import sys

sys.dont_write_bytecode = True
from validate_repair import W, g, field, value, printed_check, probes

OUT = W / 'evidence/author-366/construction'
OUT.mkdir(parents=True, exist_ok=True)
REPO = W.parents[5]
commands = []


def save(name, obj):
    (OUT / name).write_text(json.dumps(obj, indent=2, default=str) + '\n')


def run(argv):
    result = subprocess.run(list(map(str, argv)), cwd=W, capture_output=True, text=True)
    commands.append(dict(command=list(map(str, argv)), exit_code=result.returncode,
                         stdout=result.stdout, stderr=result.stderr))
    save('commands.json', commands)
    assert result.returncode == 0, commands[-1]


historical = json.loads((W / 'evidence/generated-records.json').read_text())
records = []
groups = {}
for old in historical:
    generated = [g.generate('easy', seed=seed, parameters=old['generation']['parameters'])
                 for seed in (0, 2, 5)]
    for record in generated:
        assert record['question'][':question/problem'] == old['question'][':question/problem']
        assert printed_check(record) == printed_check(old)
    records.extend(generated)
    groups[old['question'][':question/id']] = generated


def witness(items):
    ranks = []
    positions = []
    for record in items:
        answer = printed_check(record)
        choices = field(record)[':answer-field/choices']
        ranks.append(sum(bool(value(choice) < answer) for choice in choices))
        positions.append(next(i for i, choice in enumerate(choices) if value(choice) == answer))
    assert set(ranks) & {0, 4} and set(ranks) & {1, 2, 3}, ranks
    assert len(set(positions)) > 1, positions
    return dict(correct_ranks=ranks, correct_positions=positions)


before = {qid: witness(items) for qid, items in groups.items()}
save('records.json', records)
run([sys.executable, '-B', REPO / 'generate/pipeline/check_delivery.py',
     '--input', OUT / 'records.json', '--source', W.parent / 'source/source.json',
     '--inventory', W.parent / 'source/inventory.json', '--difficulty', 'easy',
     '--output', OUT / 'delivery', '--asset-root', OUT / 'assets',
     '--math-root', '/media/jake/SSD/EDB/math'])
accepted = json.loads((OUT / 'delivery/accepted.json').read_text())
assert len(accepted) == len(records)
def signature(record):
    # Shared delivery assigns canonical identities; compare visible content.
    return (record['question'][':question/problem'],
            tuple(sorted(str(value(a)) for a in field(record)[':answer-field/choices'])))


by_content = {signature(r): r for r in accepted}
assert len(by_content) == len(accepted)
after = {qid: witness([by_content[signature(r)] for r in items])
         for qid, items in groups.items()}
assert before == after and probes(records) == probes(accepted)

save('grader-input.json', [dict(label=f'historical-control-{i}', record=r, checks=[
    dict(submitted_answer_id=a[':answer/id'],
         expected='accepted' if value(a) == printed_check(r) else 'rejected',
         purpose='Printed determinant and augmented-rank witness at historical parameters')
    for a in field(r)[':answer-field/choices']]) for i, r in enumerate(accepted)])
run([REPO / 'generate/runs/current/check-engine', OUT / 'grader-input.json', OUT / 'grader-report.json'])
grader = json.loads((OUT / 'grader-report.json').read_text())
assert grader['accepted_checks'] == 15 and grader['rejected_checks'] == 60
save('results.json', dict(current_construction_passed=True, mathematical_systems=5,
                         authored_banks=15, before=before, after=after,
                         native_accepted=15, native_rejected=60,
                         historical_inventory_remediated=False,
                         scope='Fixed-equation bank-role control, not a new delivered batch or stored-pool repair.'))
print(json.dumps(dict(current_construction_passed=True, mathematical_systems=5,
                      authored_banks=15, native_accepted=15, native_rejected=60,
                      historical_inventory_remediated=False)))
