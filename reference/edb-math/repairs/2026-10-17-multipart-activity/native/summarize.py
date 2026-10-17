"""Validate native speculative application results for this concrete repair."""
from pathlib import Path
import hashlib
import json
import math
import sys

directory = Path(sys.argv[1])
before = json.loads((directory / 'api-preview-before.json').read_text())
after = json.loads((directory / 'api-preview-after.json').read_text())
scenarios = json.loads((directory / 'api-preview-resume-continue.json').read_text())
expected = {
    17592186489498: (2, 17592186059675, {17592186576138, 17592186576139}),
    17592186576141: (10, 17592186096619, {17592186576154}),
}
old = {task['task']: task for task in before['tasks']}
continued = {scenario['task']: scenario['preview'] for scenario in scenarios['scenarios']}
assert scenarios['committed'] is False and scenarios['speculative'] is True
results = []
for task in after['tasks']:
    task_id = task['task']
    count, kp, removed = expected[task_id]
    assert len(task['chain']) == count
    old_items = {item['item']: item for item in old[task_id]['chain']}
    retained = {item['item']: item for item in task['chain']}
    assert set(old_items) - set(retained) == removed
    assert set(retained) <= set(old_items)
    for item_id, item in retained.items():
        original = dict(old_items[item_id]['record'])
        current = dict(item['record'])
        original.pop('task-item/next', None)
        current.pop('task-item/next', None)
        assert original == current, f'Retained item changed: {item_id}'
        assert item['isMultistepQuestion'] is False
    assert task['taskJson']['ok'] and task['position']['ok']
    position = task['position']['value']
    assert position['next'] and not position['passed'] and not position['failed']
    assert position['shortage'] is None and position['deferred'] == []
    assert task['record']['learner-task/status'] == old[task_id]['record']['learner-task/status']
    assert math.isclose(task['record']['learner-task/elapsed-seconds'],
                        sum(item['record'].get('task-item/elapsed-seconds', 0) for item in retained.values()),
                        rel_tol=1e-12, abs_tol=1e-8)
    scenario = continued[task_id]
    assert scenario['ok'], scenario
    fresh = scenario['value']
    assert fresh['nextQuestionIsMultistep'] is False
    assert fresh['nextQuestionWasPreviouslyUnavailable'] is False
    assert fresh['taskJson']['step']['knowledgePoint']['id'] == kp
    assert fresh['taskJson']['step']['contentId'] == fresh['nextQuestion']
    results.append({
        'task_id': task_id, 'retained_item_count': count, 'removed_item_ids': sorted(removed),
        'retained_item_records_and_responses_preserved': True,
        'remaining_answered_count': task['taskJson']['value']['progress']['answered'],
        'view_rendered': True, 'continued_with_fresh_standalone_question': True,
        'next_question_id_in_speculation': fresh['nextQuestion'], 'knowledge_point_id': kp,
    })
assert {r['task_id'] for r in results} == set(expected)
report = {
    'passed': True,
    'transaction_sha256': hashlib.sha256((directory / 'transaction.edn').read_bytes()).hexdigest(),
    'basis_before': before['basis'], 'speculative_basis_after': after['basis'],
    'committed': False, 'speculative': True,
    'allResumeContinuePassed': True, 'retained_item_count': sum(r['retained_item_count'] for r in results),
    'tasks': results,
    'note': 'Resume and continue were speculative only. Both repaired tasks remain paused in the repair itself. Accuracy changes are verified separately by the counterfactual credit replay.',
}
(directory / 'application-preview.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
