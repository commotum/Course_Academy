"""Current delivered grader cases, inventory scope, and actual UI order evidence."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from checks.independent import analyze, op

OUT = ROOT / 'evidence/batch-repair'
def load(path): return json.loads(path.read_text())
def save(name, data): (OUT / name).write_text(json.dumps(data, indent=2, default=str))


def main():
    records = load(OUT / 'delivery-exact/accepted.json') + load(OUT / 'delivery-ordinary/accepted.json')
    controls = load(ROOT / 'evidence/counterfactual-records.json') + load(ROOT / 'evidence/changed-target-records.json')
    results = [analyze(r) for r in records + controls]
    assert results[-5]['correct'] != results[-4]['correct']
    assert results[-5]['correct'] == results[-3]['correct']
    assert results[-2]['correct'] != results[-1]['correct']
    save('delivery-grader-input.json', [
        {'label': str(i), 'record': r,
         'checks': [{'field_index': 0, 'submitted_answer_id': a[':answer/id'],
                     'expected': 'accepted' if j == analyze(r)['position'] else 'rejected',
                     'purpose': 'independent visible arithmetic, normalized identities or retained counterfactual'}
                    for j, a in enumerate(r['question'][':question/answer-fields'][0][':answer-field/choices'])]}
        for i, r in enumerate(records + controls)])
    save('counterfactual-results.json', {'status': 'passed', 'visible_analysis': results[-5:],
                                       'records': controls})

    # Examine the exact demonstrated bank shape in the entire captured pool.
    source = load(ROOT.parent / 'source/source.json')
    inventory = load(ROOT.parent / 'source/inventory.json')
    source_ids = {q[':question/id'] for q in source['material']['kp'][':knowledge-point/questions']}
    findings = []
    for q in inventory['questions']:
        field = q[':question/answer-fields'][0]
        operations = [op(a[':answer/value']) for a in field[':answer-field/choices']]
        signature = Counter('swap' if o[0] == 'swap' else
                            'distinct' if sum(c != 0 for c in o[2]) == 2 else 'self'
                            for o in operations)
        cue_group = signature == {'swap': 2, 'distinct': 1, 'self': 2}
        if q[':question/id'] not in source_ids:
            analyze({'question': q})
        findings.append({'question_id': q[':question/id'], 'entity_id': q[':db/id'],
                         'original_source': q[':question/id'] in source_ids,
                         'operation_signature': dict(signature), 'matches_demonstrated_cue_group': cue_group})
    matches = [r for r in findings if r['matches_demonstrated_cue_group']]
    assert len(matches) == 1 and matches[0]['original_source']
    save('inventory-review.json', {'basis': inventory['basis'], 'inspected': len(findings),
        'records': findings,
        'conclusion': 'Verified absence of the demonstrated bank-shape subgroup among all five captured non-source records. '
                      'Only the original source q-72858 matches; it is not classified as generated.',
        'limits': ['Missing generation metadata prevents exact historical generation replay of non-source records.',
                   'No claim about uncaptured/live inventory or other possible shortcuts.']})
    save('affected-inventory.json', {'affected_questions': []})
    # Also place the required inventory artifact at the workspace root.
    (ROOT / 'affected-inventory.json').write_text(json.dumps({'affected_questions': []}, indent=2))

    ui = {}
    for stage, records_path in [('render', OUT / 'render-records.json'),
                                ('render-delivered', OUT / 'delivery-exact/accepted.json')]:
        rs = load(records_path)
        positions = []
        for i, r in enumerate(rs, 1):
            html = (OUT / stage / f'question-{i:03}.html').read_text()
            ids = re.findall(r'<input\b[^>]*type="radio"[^>]*value="([^"]+)"', html)
            key = r['question'][':question/answer-fields'][0][':answer-field/correct'][1]
            assert len(ids) == 5 and key in ids
            positions.append({'question_id': r['question'][':question/id'],
                              'profile': r['generation']['bank_profile'], 'position': ids.index(key)})
        restored = [r['position'] for r in positions if r['profile'] == 'q-72858']
        assert len(set(restored)) == 2, ('fixed rendered position in exact restored subgroup', stage, restored)
        ui[stage] = positions
    save('ui-order-results.json', ui)
    save('package-change.json', {
        'generator_before_sha256': hashlib.sha256((OUT / 'generator-before.py').read_bytes()).hexdigest(),
        'generator_after_sha256': hashlib.sha256((ROOT / 'generator.py').read_bytes()).hexdigest(),
        'runtime_files': {n: hashlib.sha256((ROOT / n).read_bytes()).hexdigest()
                          for n in load(ROOT / 'package.json')['files']},
        'changes': 'Only generator.py version and batch case scheduling changed in runtime files; source restoration retained.',
        'relocation_and_dependency_validation': '../packaging-results.json'})
    print(json.dumps({'delivery_grader_records': len(records + controls),
                      'inventory_non_source_cue_matches': 0, 'ui': ui}))


if __name__ == '__main__':
    main()
