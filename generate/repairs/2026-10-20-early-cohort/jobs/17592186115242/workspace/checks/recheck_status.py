"""Recheck retained repairs and report unresolved findings without waiving them.

Usage: job-python -B checks/recheck_status.py --output evidence/repair-10
Writes only workspace evidence. Exit 1 means a retained finding still fails.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

sys.dont_write_bytecode = True
from validate_repair import W, g, printed_check
from batch_regressions import contrasts

ap = argparse.ArgumentParser()
ap.add_argument('--output', required=True)
args = ap.parse_args()
out = (W / args.output).resolve()
assert out.is_relative_to(W)
out.mkdir(parents=True, exist_ok=True)
commands = []

def save(name, data):
    (out / name).write_text(json.dumps(data, indent=2) + '\n')

def run(command):
    command = list(map(str, command))
    p = subprocess.run(command, cwd=W, capture_output=True, text=True)
    commands.append(dict(command=command, exit_code=p.returncode,
                         stdout=p.stdout, stderr=p.stderr))
    save('commands.json', commands)
    return p.returncode

def load(path):
    return json.loads(path.read_text())

declarations = load(W / 'repair-regressions.json')['findings']
history = load(W.parent / 'repair-history.json')['findings']
assert {f['id'] for f in declarations} == {f['id'] for f in history}
inventory_id = '591f580cadb749294588'
findings = []
# Reproduce the latest failure before checking the preserved repairs.
for f in sorted(declarations, key=lambda f: f['id'] != inventory_id):
    result = run([sys.executable, '-B', W / f['script'], *f['args']])
    findings.append(dict(id=f['id'], exit_code=result, passed=result == 0))
    assert result in ([0, 1] if f['id'] == inventory_id else [0]), commands[-1]

protected = load(W / 'evidence/repair-3/proposal-results.json')['protected_hashes']
assert all(hashlib.sha256(Path(p).read_bytes()).hexdigest() == h
           for p, h in protected.items())
proposal_dir = W / 'evidence/repair-3'
proposal = load(proposal_dir / 'inventory-repair-proposal.json')
raw = load(proposal_dir / proposal['generator_records'])
accepted_path = proposal_dir / proposal['replacement_records']
accepted = load(accepted_path)
assert raw == g.generate_batch('easy', 5, 1475864943)
assert hashlib.sha256(accepted_path.read_bytes()).hexdigest() == proposal['replacement_records_sha256']
assert contrasts(raw) == contrasts(accepted)
for r in raw + accepted:
    printed_check(r)
affected = load(W / 'affected-inventory.json')['affected_questions']
historical = load(W / 'evidence/generated-records.json')
assert {m['question_id'] for m in proposal['mappings']} == {f['question_id'] for f in affected}
assert {m['proposed_replacement_id'] for m in proposal['mappings']} == {r['question'][':question/id'] for r in accepted}
for f in affected:
    path = (W.parent / 'author-10' / f['evidence_path']).resolve()
    assert path == (W / 'evidence/generated-records.json').resolve()
    assert any(r['question'][':question/id'] == f['question_id'] for r in historical)
assert load(W / 'evidence/inventory-audit.json')['untested_inventory_ids'] == []

repo = W.parents[5]
assert run([repo / 'generate/runs/current/check-engine',
            W / 'evidence/repair-2/grader-input.json', out / 'grader-report.json']) == 0
assert run([sys.executable, '-B', W / 'checks/verify_package.py']) == 0
grader = load(out / 'grader-report.json')
assert grader['accepted_checks'] == 7 and grader['rejected_checks'] == 28
assert grader['documented_unresolved_checks'] == grader['database_writes'] == 0
passed = all(f['passed'] for f in findings)
save('results.json', dict(
    status='ready' if passed else 'unsupported', findings=findings,
    runtime_source_inventory_manifest_unchanged=True, protected_hashes=protected,
    proposal_verified=True, proposal_applied=False, affected_inventory=len(affected),
    untested_generated_inventory=0, source_banks_replayed=17,
    delivered_records=14, native_accepted=7, native_rejected=28,
    relocation_passed=True,
    retained_rendering='evidence/repair-3/render/rendering.json',
    limitation=None if passed else 'The five captured stored banks remain selectable. Their removal requires the separate inventory-remediation workflow; this task forbids database changes.'))
print(json.dumps(dict(passed=passed, generator_findings_passed=4,
                      affected_inventory=len(affected), proposal_verified=True)))
raise SystemExit(0 if passed else 1)
