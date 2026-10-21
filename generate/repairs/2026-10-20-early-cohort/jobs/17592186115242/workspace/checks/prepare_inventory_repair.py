"""Prepare and verify offline replacement records. Never applies the proposal.

The strict captured-inventory regression is a separate mandatory failure while
the old pool remains unchanged; this script cannot satisfy or waive it.
"""
import hashlib
import json
import subprocess
import sys

sys.dont_write_bytecode = True
from validate_repair import W, g, field, value, root, printed_check, probes
from batch_regressions import contrasts

E = W / 'evidence/repair-3'
E.mkdir(parents=True, exist_ok=True)
REPO = W.parents[5]
commands = []


def write(name, data):
    (E / name).write_text(json.dumps(data, indent=2, default=str) + '\n')


def run(args, expected=0):
    p = subprocess.run([str(a) for a in args], cwd=W, text=True, capture_output=True)
    commands.append(dict(command=[str(a) for a in args], exit_code=p.returncode,
                         stdout=p.stdout, stderr=p.stderr))
    write('commands.json', commands)
    assert p.returncode == expected, commands[-1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


manifest = json.loads((W / 'package.json').read_text())
protected = [W / 'package.json', *(W / f for f in manifest['files']),
             W.parent / 'source/source.json', W.parent / 'source/inventory.json']
before_hashes = {str(p): digest(p) for p in protected}

# Confirm the exact current failure rather than assuming the previous report.
run([sys.executable, '-B', W / 'checks/batch_regressions.py', '--finding', 'inventory'], expected=1)
old = json.loads((W / 'evidence/generated-records.json').read_text())
inventory = json.loads((W.parent / 'source/inventory.json').read_text())
source = json.loads((W.parent / 'source/source.json').read_text())
stored = {q[':question/id']: q for q in inventory['questions']}
source_ids = {q[':question/id'] for q in source['material']['kp'][':knowledge-point/questions']}
source_ids.add(source['material']['kp'][':knowledge-point/canonical-example'][':question/id'])
assert len(old) == 5
assert not source_ids.intersection(r['question'][':question/id'] for r in old)

replacement = g.generate_batch('easy', 5, 1475864943)
for r in replacement:
    printed_check(r)
    assert r == g.generate('easy', seed=r['generation']['seed'])
assert not set(stored).intersection(r['question'][':question/id'] for r in replacement)
before = contrasts(replacement)
write('replacement-records.json', replacement)
run([sys.executable, '-B', REPO / 'generate/pipeline/check_delivery.py',
     '--input', E / 'replacement-records.json', '--source', W.parent / 'source/source.json',
     '--inventory', W.parent / 'source/inventory.json', '--difficulty', 'easy',
     '--output', E / 'delivery', '--asset-root', E / 'assets',
     '--math-root', '/media/jake/SSD/EDB/math'])
accepted = json.loads((E / 'delivery/accepted.json').read_text())
assert len(accepted) == 5
after = contrasts(accepted)
assert before == after
accepted_ids = {r['question'][':question/id'] for r in accepted}
assert len(accepted_ids) == 5 and not accepted_ids.intersection(stored)
accepted_by_seed = {r['generation']['seed']: r for r in accepted}
assert len(accepted_by_seed) == 5
for raw in replacement:
    delivered = accepted_by_seed[raw['generation']['seed']]
    assert delivered['generation'] == raw['generation']
    for key in [':question/problem', ':question/worked-solution', ':question/difficulty']:
        assert delivered['question'][key] == raw['question'][key]
    assert [a[':answer/value'] for a in field(delivered)[':answer-field/choices']] == [
        a[':answer/value'] for a in field(raw)[':answer-field/choices']]
    assert printed_check(delivered) == printed_check(raw)

# Every replacement is tested with every selectable response, with the key
# independently derived from the visible system's determinant and ranks.
write('grader-input.json', [dict(label=f'proposed-replacement-{i}', record=r, checks=[
    dict(submitted_answer_id=a[':answer/id'],
         expected='accepted' if value(a) == root(r) else 'rejected',
         purpose='Independent determinant, rank and visible bank witness')
    for a in field(r)[':answer-field/choices']]) for i, r in enumerate(accepted)])
run([REPO / 'generate/runs/current/check-engine', E / 'grader-input.json', E / 'grader-report.json'])

mapping = []
for historical, new in zip(sorted(old, key=lambda r: stored[r['question'][':question/id']][':db/id']),
                           replacement):
    old_id = historical['question'][':question/id']
    delivered = accepted_by_seed[new['generation']['seed']]
    mapping.append(dict(question_id=old_id, entity_id=stored[old_id][':db/id'],
                        historical_seed=historical['generation']['seed'],
                        generator_question_id=new['question'][':question/id'],
                        proposed_replacement_id=delivered['question'][':question/id'],
                        proposed_replacement_seed=new['generation']['seed']))
assert len({m['question_id'] for m in mapping}) == len({m['proposed_replacement_id'] for m in mapping}) == 5
assert {m['question_id'] for m in mapping} == {
    q['question_id'] for q in json.loads((W / 'affected-inventory.json').read_text())['affected_questions']}

write('inventory-repair-proposal.json', dict(
    format=1, status='proposed_only_not_applied', finding_id='591f580cadb749294588',
    knowledge_point=17592186115242, inventory_basis=inventory['basis'],
    source_sha256=digest(W.parent / 'source/source.json'),
    inventory_sha256=digest(W.parent / 'source/inventory.json'),
    historical_records='../generated-records.json', generator_records='replacement-records.json',
    replacement_records='delivery/accepted.json',
    replacement_records_sha256=digest(E / 'delivery/accepted.json'), mappings=mapping,
    required_external_actions=[
        'Independently review the current package, five replacements and exact captured old identities.',
        'Through the separately authorized inventory-remediation workflow, remove only the five affected generated questions from future selection and publish the reviewed replacements.',
        'Preserve all original source questions, completed learner items and historical answer semantics.',
        'Recapture inventory and rerun the strict stored-pool and delivery checks before claiming resolution.'
    ],
    applies_database_changes=False, publication_performed=False,
    limits=['No future entity IDs or actual learner histories are available.',
            'The proposed pool is not the captured or live selectable pool.',
            'The strict retained inventory check still fails; passing proposal checks do not waive it.']))

# Read back the actual complete replacement records referenced by the proposal.
proposal = json.loads((E / 'inventory-repair-proposal.json').read_text())
readback = json.loads((E / proposal['replacement_records']).read_text())
assert digest(E / proposal['replacement_records']) == proposal['replacement_records_sha256']
assert {m['proposed_replacement_id'] for m in proposal['mappings']} == {
    r['question'][':question/id'] for r in readback}
for r in readback:
    printed_check(r)
assert before_hashes == {str(p): digest(p) for p in protected}
write('proposal-results.json', dict(
    proposal_validated=True, stored_pool_resolved=False, replacements=len(accepted),
    captured_affected_records=len(old), strict_inventory_exit_code=1,
    before_delivery=before, after_delivery=after,
    historical_shortcut=probes(old), runtime_and_source_files_unchanged=True,
    protected_hashes=before_hashes,
    limits=['Read-only proposal; no database writes or publication.']))
print(json.dumps(dict(proposal_validated=True, stored_pool_resolved=False,
                      replacements=len(accepted), strict_inventory_exit_code=1)))
