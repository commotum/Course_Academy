"""Reproduce historical generated inventory using its archived implementation.

This archive is evidence, excluded from the repaired runtime manifest. No
historical question is regenerated using the v3 algorithm or assigned a new ID.
"""
import hashlib
import importlib.util
import json
import os
import pathlib
import sys
sys.dont_write_bytecode = True
from validate_repair import W, E, field, value, probes, printed_check, write

legacy = E/'historical-package/17592186115242.py'
assert hashlib.sha256(legacy.read_bytes()).hexdigest() == '4464440a6ce7b156c193c1667572b8443d13863f0f302052516fb90bf50dd6c5'
spec = importlib.util.spec_from_file_location('historical_generator', legacy)
old = importlib.util.module_from_spec(spec); spec.loader.exec_module(old)
inventory = json.loads((W.parent/'source/inventory.json').read_text())
original = json.loads((W.parent/'source/source.json').read_text())['material']['kp'][':knowledge-point/questions']
source_ids = {q[':question/id'] for q in original}
captured = json.loads((W/'17592186115242/reference/replenishment/basis-2699/generated.json').read_text())
records = []; findings = []; audits = []
for saved in captured:
    gen = saved['generation']
    r = old.generate('easy',seed=gen['seed'],template=gen['template'],parameters=gen['parameters'])
    assert all(gen[key] == val for key,val in r['generation'].items())
    # Captured publication metadata extends the independently replayed metadata.
    r['generation'] = gen
    q = next(q for q in inventory['questions'] if q[':question/id']==r['question'][':question/id'])
    assert q[':question/id'] not in source_ids
    assert q[':question/problem'] == r['question'][':question/problem']
    assert q[':question/worked-solution'] == r['question'][':question/worked-solution']
    f = q[':question/answer-fields'][0]; rf = field(r)
    assert {value(a) for a in f[':answer-field/choices']} == {value(a) for a in rf[':answer-field/choices']}
    assert sorted((a[':answer/id'],a[':answer/value']) for a in f[':answer-field/choices']) == sorted((a[':answer/id'],a[':answer/value']) for a in rf[':answer-field/choices'])
    assert f[':answer-field/correct'][':answer/id'] == rf[':answer-field/correct'][1]
    printed_check(r)
    z = next(iter(probes([r]).values()))
    assert z['sign_extremum_successes'] == 1
    records.append(r)
    findings.append(dict(question_id=q[':question/id'],entity_id=q[':db/id'],finding='Historical easy bank is solved by the sign-only extremal-choice action; no magnitude calculation required.',reproduction=f'/home/jake/Developer/Course_Academy/.venv/bin/python -B checks/inventory_audit.py (historical seed {gen["seed"]})',evidence_path=os.path.relpath(E/'generated-records.json',W.parent/'author-2')))
    audits.append(dict(question_id=q[':question/id'],matched_generation=True,matched_prompt_solution_bank_key=True))
write('generated-records.json',records)
(W/'affected-inventory.json').write_text(json.dumps(dict(affected_questions=findings),indent=2)+'\n')
write('inventory-audit.json',dict(basis=inventory['basis'],total=len(inventory['questions']),source_questions=len(original),reproduced_generated=len(records),cases=audits,untested_inventory_ids=[q[':question/id'] for q in inventory['questions'] if q[':question/id'] not in source_ids and q[':question/id'] not in {r['question'][':question/id'] for r in records}],limitations=['Only historical generated records are tagged affected; sources are not marked generated. Missing-family and zero-root findings concern generator reachability, not stored-item correctness. No database writes. evidence_path is relative to the requested author-2 evidence root; files remain in workspace.']))
print(json.dumps(dict(passed=True,affected=len(findings),inventory_total=len(inventory['questions']))))
