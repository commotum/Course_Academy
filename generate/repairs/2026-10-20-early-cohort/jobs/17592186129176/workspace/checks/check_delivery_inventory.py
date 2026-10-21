"""Independent witnesses after actual delivery; read-only captured inventory audit."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
from validate_repair import ROOT, E, save, coverage, shortcuts
from source_coverage import read_task, witness


def main():
    before = json.loads((E/'normal-records.json').read_text())
    accepted = json.loads((E/'delivery/accepted.json').read_text())
    batch = json.loads((E/'delivery-batch/accepted.json').read_text())
    assert [witness(r) for r in before] == [witness(r) for r in accepted]
    assert coverage(before) == coverage(accepted)
    assert shortcuts(before) == shortcuts(accepted)
    save('coverage-after-delivery.json', {'before': coverage(before), 'after': coverage(accepted),
                                        'relevant_coverage_preserved': True,
                                        'new_profile_after': coverage([r for r in accepted if r['generation']['bank_profile']=='q-129207']),
                                        'runner_batch': coverage(batch)})
    save('shortcuts-after.json', shortcuts(accepted))
    # Recheck normalized UUID selections with native grading: every new rank,
    # an old two-row record, and the five-question CLI batch.
    chosen = []
    for rank in range(5):
        chosen.append(next(r for r in accepted if r['generation']['bank_profile']=='q-129207' and witness(r)['rank']==rank))
    chosen.append(next(r for r in accepted if len(witness(r)['rows'])==2))
    cases = []
    for i, record in enumerate(chosen+batch):
        total = witness(record)['total']
        cases.append({'label': f'delivered record {i}: {total}', 'record': record,
                      'checks': [{'submitted_answer_id': c[':answer/id'],
                                  'expected': 'accepted' if int(c[':answer/value'])==total else 'rejected',
                                  'purpose': 'delivered IDs with independent mathematical key'}
                                 for c in record['question'][':question/answer-fields'][0][':answer-field/choices']]})
    save('grader-delivered-input.json', cases)
    save('render-delivered-records.json', [chosen[0]])

    # Inventory is data, never a database connection. Missing generation metadata
    # is reported explicitly; source UUIDs are not designated generated.
    inventory_path = ROOT.parent/'source/inventory.json'
    inventory = json.loads(inventory_path.read_text())
    sources = json.loads((E/'source-cases.json').read_text())
    originals = {q[':question/id'] for q in sources}
    audit = []
    for q in inventory['questions']:
        matrix, rows = read_task(q[':question/problem'])
        total = sum(next(x for x in matrix[r] if x) for r in rows)
        field = q[':question/answer-fields'][0]
        bank = [int(a[':answer/value']) for a in field[':answer-field/choices']]
        key = field.get(':answer-field/correct')
        actual = int(key[':answer/value']) if key else None
        assert bank.count(total) == 1 and len(set(bank)) == len(bank) == 5
        assert actual is None or actual == total
        audit.append({'question_id': q[':question/id'], 'entity_id': q[':db/id'],
                      'original_source': q[':question/id'] in originals,
                      'visible_sum': total, 'bank': bank, 'stored_key': actual,
                      'generation_metadata_available': any('generat' in k for k in q)})
    save('inventory-audit.json', {'basis': inventory['basis'], 'records': audit,
                                 'source_count': sum(x['original_source'] for x in audit),
                                 'other_count': sum(not x['original_source'] for x in audit),
                                 'conclusion': 'No stored generated instance demonstrated affected by omitted source-profile coverage. All visible banks include the computed sum; all available keys agree.',
                                 'limits': 'Five nonsource records have no generation metadata, so their original seeds/profiles cannot be replayed. Two original sources lack stored keys. This is not a verified absence of every historical defect.'})
    save('affected-inventory.json', {'affected_questions': []})

    # Read-only selection rule for an all-easy pool: uniform(8) chooses index.
    # Configured positive easy weights do not inspect rows, banks, or signs.
    selection_path = Path('/home/jake/Developer/Course_Academy/engine/rust/question_selection.rs')
    def select(pool, seed, configured=True, easy_enabled=True):
        if not pool or not easy_enabled:
            return None
        if not configured:
            return pool[0]
        digest = hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest()
        u = (int.from_bytes(digest[8:16], 'big') >> 11) / 2**53
        return pool[int(u*len(pool))]
    results = {}
    for label, pool, configured, enabled in [('positive_easy', list(range(5)), True, True),
                                          ('first_two_seen', list(range(2,5)), True, True),
                                          ('unconfigured', list(range(5)), False, True),
                                          ('easy_disabled', list(range(5)), True, False)]:
        draws = [select(pool, 'repair-selection-'+str(i), configured, enabled) for i in range(64)]
        if configured and enabled:
            assert set(draws) == set(pool)
        results[label] = {'draws': 64, 'counts': dict(Counter(str(x) for x in draws))}
    save('selection-results.json', {'engine_sha256': hashlib.sha256(selection_path.read_bytes()).hexdigest(),
                                   'method': 'Read-only exact all-easy specialization of select; candidate IDs ordered before assigning indexes. Configured positive easy band has uniform candidate probability.',
                                   'scenarios': results,
                                   'limits': 'Hypothetical fresh captured candidates; actual live weights, IDs and learner histories are unavailable. Histories may remove candidates. Unconfigured policy takes earliest ID; disabled easy band excludes all these questions.'})
    print(f'Delivery preserves all {len(accepted)} records and their shortcut/coverage results; {len(audit)} inventory questions inspected; {len(cases)*5} delivered native checks prepared.')


if __name__ == '__main__':
    main()
