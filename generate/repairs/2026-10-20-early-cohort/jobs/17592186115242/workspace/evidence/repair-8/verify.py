"""Recheck the unchanged candidate; retain the stored-pool failure as a failure."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

sys.dont_write_bytecode = True
W = Path(__file__).resolve().parents[2]
E = Path(__file__).resolve().parent
REPO = W.parents[5]
commands = []


def save(name, value):
    (E / name).write_text(json.dumps(value, indent=2) + '\n')


def run(args, expected=0):
    p = subprocess.run([str(a) for a in args], cwd=W, capture_output=True, text=True)
    commands.append(dict(command=[str(a) for a in args], exit_code=p.returncode,
                         stdout=p.stdout, stderr=p.stderr))
    save('commands.json', commands)
    assert p.returncode == expected, commands[-1]


PY = sys.executable
run([PY, '-B', 'checks/batch_regressions.py', '--finding', 'inventory'], expected=1)
declarations = json.loads((W / 'repair-regressions.json').read_text())['findings']
history = json.loads((W.parent / 'repair-history.json').read_text())['findings']
assert {f['id'] for f in declarations} == {f['id'] for f in history}
for f in declarations:
    if f['id'] != '591f580cadb749294588':
        run([PY, '-B', f['script'], *f['args']])
run([PY, '-B', 'checks/verify_retained_evidence.py'])
run([PY, '-B', 'checks/verify_package.py'])
run([REPO / 'generate/runs/current/check-engine',
     W / 'evidence/repair-2/grader-input.json', E / 'grader-report.json'])

protected = json.loads((W / 'evidence/repair-3/proposal-results.json').read_text())['protected_hashes']
assert all(hashlib.sha256(Path(p).read_bytes()).hexdigest() == h for p, h in protected.items())
inventory = json.loads((W / 'evidence/repair-2/inventory-results.json').read_text())
audit = json.loads((W / 'evidence/inventory-audit.json').read_text())
grader = json.loads((E / 'grader-report.json').read_text())
batch = json.loads((W / 'evidence/repair-2/batch-results.json').read_text())
source = json.loads((W / 'evidence/regression-source.json').read_text())
affected = json.loads((W / 'affected-inventory.json').read_text())['affected_questions']
records = json.loads((W / 'evidence/generated-records.json').read_text())
for f in affected:
    assert (W.parent / 'author-8' / f['evidence_path']).resolve() == (W / 'evidence/generated-records.json').resolve()
    assert any(r['question'][':question/id'] == f['question_id'] for r in records)
assert len(affected) == 5 and not inventory['passed'] and not audit['untested_inventory_ids']
assert grader['accepted_checks'] == 7 and grader['rejected_checks'] == 28
assert grader['documented_unresolved_checks'] == grader['database_writes'] == 0
save('results.json', dict(
    status='unsupported', generator_findings_passed=4, strict_inventory_passed=False,
    affected_inventory=5, untested_generated_inventory=0,
    source_replay=source, delivery_trials=len(batch['trials']),
    delivered=sum(t['count'] for t in batch['trials']),
    native_grading={k: grader[k] for k in ['accepted_checks', 'rejected_checks', 'documented_unresolved_checks', 'database_writes']},
    runtime_source_inventory_and_manifest_unchanged=True, protected_hashes=protected,
    relocation_passed=True, replacement_proposal='evidence/repair-3/inventory-repair-proposal.json',
    retained_rendering='evidence/repair-3/render/rendering.json',
    limitation='Five captured stored banks remain selectable. Repair requires the separate inventory-remediation workflow; database changes are prohibited in this job. No strict failure was waived.'))
print(json.dumps(dict(generator_findings_passed=4, strict_inventory_passed=False,
                      affected_inventory=5, delivered=14, correct_accepted=7, wrong_rejected=28)))
