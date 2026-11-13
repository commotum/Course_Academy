"""Merge independently reviewed patches against one exact captured value."""
from collections import Counter, defaultdict
import json
from pathlib import Path
import re
import sys

H = Path(__file__).resolve().parent
ROOT = H.parents[3]
sys.path.insert(0, str(ROOT))
from scripts.question_capture.math_format import MATH, validate_prose

def load(path):
    return json.loads((H/path).read_text())

decisions = []
inputs = [('root', load('recoverable-reviews.json'), load('recoverable-proposals.json'))]
inputs += [(f'review-{i}', load(f'review-{i}/reviews.json'), load(f'review-{i}/proposals.json')) for i in range(1,4)]
inputs += [(f'review-{i}-supplemental', [], load(f'review-{i}/supplemental-proposals.json'))
           for i in range(1,4) if (H/f'review-{i}/supplemental-proposals.json').exists()]
fields = load('snapshot-fields.json')
current = {r[':db/id']: r for r in load('capture/entities.json')}
groups = defaultdict(list)
duplicates = set()
for reviewer, reviews, proposals in inputs:
    for row in reviews:
        decisions.append({**row, 'status': row.get('status', row.get('decision')), 'reviewer': reviewer})
    for proposal in proposals:
        key = (proposal['entity'], proposal['attribute'])
        before = fields[f'{key[0]}/{key[1]}']
        assert proposal['before'] == before == current[key[0]][':'+key[1]], key
        replay = before
        for patch in sorted(proposal['replacements'], key=lambda r: r['start'], reverse=True):
            assert before[patch['start']:patch['end']] == patch['before']
            replay = replay[:patch['start']]+patch['after']+replay[patch['end']:]
        assert replay == proposal['after'], (key, 'Proposal patch replay mismatch')
        groups[key].extend([{**p, 'reviewer': reviewer} for p in proposal['replacements']])
        duplicates.update(proposal.get('duplicate_import_artifact_candidates', []))
by_index = {r['candidate_index']: r for r in decisions}
assert len(by_index) == len(decisions) == 727
assert all(r['status'] in ('confirmed', 'disconfirmed') for r in decisions)
supplemental = []
for key, value in fields.items():
    entity, attribute = key.split('/', 1)
    if (int(entity), attribute) not in groups:
        continue
    for math in MATH.finditer(value):
        if not re.search(r'\{\{(?:answer-field:)?[^{}]+\}\}', math[0]):
            continue
        match = re.fullmatch(r'\$\$\s*(\{\{field-3\}\})\.\s*\$\$', math[0])
        assert match, (key, 'Unexpected embedded-control form requires review', math[0])
        patch = {'start': math.start(), 'end': math.end(), 'before': math[0],
                 'after': '<div class="matrix-answer">'+match[1]+'.</div>',
                 'candidate_indices': [], 'reviewer': 'root',
                 'rationale': 'A whole-equation selector is an interactive control, not TeX. Preserve the field and punctuation outside the math delimiters.'}
        groups[(int(entity), attribute)].append(patch)
        supplemental.append({'entity': int(entity), 'attribute': attribute, **patch})
proposals = []
covered = set()
for (entity, attribute), patches in sorted(groups.items()):
    before = fields[f'{entity}/{attribute}']
    after = before
    end = len(before)
    for patch in sorted(patches, key=lambda r: r['start'], reverse=True):
        assert 0 <= patch['start'] < patch['end'] <= end, (entity, 'Overlapping review patches', patch)
        assert before[patch['start']:patch['end']] == patch['before']
        assert all(by_index[index]['status'] == 'confirmed' for index in patch['candidate_indices'])
        after = after[:patch['start']] + patch['after'] + after[patch['end']:]
        end = patch['start']
        covered.update(patch['candidate_indices'])
    keys = lambda value: Counter(re.findall(r'\{\{(?:answer-field:)?[^{}]+\}\}', value))
    indices = sorted({i for p in patches for i in p['candidate_indices']})
    assert set(keys(before)) == set(keys(after)), (entity, 'Changed field identities')
    if not duplicates.intersection(indices):
        assert keys(before) == keys(after), (entity, 'Changed field multiplicities')
    else:
        assert all(v == 1 for v in keys(after).values()), (entity, 'Duplicate controls remain')
    for math in MATH.finditer(after):
        assert not keys(math[0]), (entity, 'Controls placed inside math')
    validate_prose(after)
    proposals.append({'entity': entity, 'attribute': attribute, 'before': before, 'after': after,
                      'candidate_indices': indices, 'replacements': sorted(patches, key=lambda r:r['start']),
                      'duplicate_artifact_candidates': sorted(duplicates.intersection(indices))})
confirmed = {r['candidate_index'] for r in decisions if r['status'] == 'confirmed'}
assert confirmed == covered, (confirmed-covered, covered-confirmed)
summary = {'passed': True, 'reviewed_candidates': len(decisions),
           'decisions': dict(Counter(r['status'] for r in decisions)),
           'changed_fields': len(proposals), 'changed_entities': len({r['entity'] for r in proposals}),
           'by_attribute': dict(Counter(r['attribute'] for r in proposals)),
           'duplicate_artifact_candidates': sorted(duplicates),
           'embedded_selector_controls_repaired': len(supplemental),
           'additional_confirmed_layouts': sum(not p['candidate_indices'] and p['reviewer'] != 'root'
                                              for ps in groups.values() for p in ps),
           'all_confirmed_decisions_covered': True, 'exact_before_and_nonoverlapping_patches': True,
           'field_identities_preserved': True, 'controls_outside_math': True}
for path, data in [('reviews.json', sorted(decisions, key=lambda r:r['candidate_index'])),
                   ('proposals.json', proposals), ('supplemental-control-repairs.json', supplemental), ('preflight.json', summary)]:
    (H/path).write_text(json.dumps(data, indent=2, ensure_ascii=False)+'\n')
print(json.dumps(summary, indent=2))
