"""Verify that retained replacement/render evidence still binds this candidate.

This is evidence consistency, not a waiver of the strict inventory regression.
No runtime files, services, or database content are modified.
"""
import hashlib
import json
import sys

sys.dont_write_bytecode = True
from validate_repair import W, g, printed_check, probes

E = W / 'evidence/repair-4'
E.mkdir(parents=True, exist_ok=True)

def read(path):
    return json.loads(path.read_text())

protected = read(W / 'evidence/repair-3/proposal-results.json')['protected_hashes']
for filename, expected in protected.items():
    from pathlib import Path
    assert hashlib.sha256(Path(filename).read_bytes()).hexdigest() == expected, filename

raw = read(W / 'evidence/repair-3/replacement-records.json')
assert raw == g.generate_batch('easy', 5, 1475864943)
delivered = read(W / 'evidence/repair-3/delivery/accepted.json')
for record in raw + delivered:
    printed_check(record)
assert probes(raw) == probes(delivered)
proposal = read(W / 'evidence/repair-3/inventory-repair-proposal.json')
assert proposal['replacement_records_sha256'] == hashlib.sha256(
    (W / 'evidence/repair-3/delivery/accepted.json').read_bytes()).hexdigest()
assert {m['proposed_replacement_id'] for m in proposal['mappings']} == {
    r['question'][':question/id'] for r in delivered}

historical = read(W / 'evidence/generated-records.json')
for finding in read(W / 'affected-inventory.json')['affected_questions']:
    target = (W.parent / 'author-4' / finding['evidence_path']).resolve()
    assert target == (W / 'evidence/generated-records.json').resolve()
    assert any(r['question'][':question/id'] == finding['question_id'] for r in read(target))
audit = read(W / 'evidence/inventory-audit.json')
assert audit['untested_inventory_ids'] == []
inventory_result = read(W / 'evidence/repair-2/inventory-results.json')
assert not inventory_result['passed']
assert len(inventory_result['affected_questions']) == len(historical) == 5

report = dict(
    evidence_consistent=True, runtime_and_captured_inputs_unchanged=True,
    protected_hashes=protected, replacements=5,
    current_batch_matches_proposal=True, before_and_after_delivery=probes(delivered),
    affected_inventory=5, untested_generated_inventory=0,
    stored_pool_resolved=False, strict_inventory_passed=False,
    retained_rendering='evidence/repair-3/render/rendering.json',
    final_status='unsupported',
    limitation='Five stored banks require separate inventory remediation; generator edits cannot modify them.')
(E / 'retained-evidence.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(dict(evidence_consistent=True, replacements=5, stored_pool_resolved=False)))
