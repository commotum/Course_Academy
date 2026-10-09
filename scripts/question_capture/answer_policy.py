"""Separate a best-effort submission from mathematical and source-key confidence."""
import hashlib
import json

BEST_EFFORT = 'best-effort-submission-v1'
SOURCE_ANSWER = 'revealed-ma-answer-v1'


def binding(item, *, feedback=False):
    # Restored pages may shuffle letters/order. Bind to the actual values and roles.
    fields = sorted([{'key': f['key'], 'type': f['type'], 'tag': f.get('tag'),
                      'choices': sorted((c['type'], c['value']) for c in f.get('choices', []))}
                     for f in item.get('fields', [])], key=lambda f: f['key'])
    source = {'problem': item.get('source_problem', item.get('problem', '')), 'fields': fields}
    if feedback:
        source['worked_solution'] = item.get('worked_solution', '')
    return hashlib.sha256(json.dumps(source, sort_keys=True).encode()).hexdigest()


def best_effort(result, item):
    policy = result.get('submission_policy', {})
    return (policy.get('version') == BEST_EFFORT and
            policy.get('question_sha256') == binding(item) and
            policy.get('mathematical_assessment', {}).get('confident') is False and
            not item.get('diagnostic_policy'))


def source_answer(result, item):
    policy = result.get('source_answer_policy', {})
    return (result.get('confident') is True and policy.get('version') == SOURCE_ANSWER and
            bool(item.get('worked_solution')) and
            policy.get('feedback_sha256') == binding(item, feedback=True))


def soften_sequence(record):
    if best_effort(record['decision'], record['before']):
        record.setdefault('desired_intended', record['intended'])
        record['intended'] = 'C'
        record['sequence_deviation'] = 'Best supported submission after mathematical uncertainty'
        record['mathematical_assessment'] = record['decision']['submission_policy']['mathematical_assessment']


def recovery_available(diagnostic):
    """Old permanent uncertainty exclusions now have a bounded submission action."""
    from pathlib import Path
    try:
        report = json.loads(Path(diagnostic).read_text())
        directory = Path(diagnostic).parents[2]
        state = json.loads((directory/'state.json').read_text())
        if (report.get('message') != 'Solver is uncertain; question saved for review' or
                state.get('task_type') not in ('lesson', 'review')):
            return False
        for path in directory.glob('*/solve-input.json'):
            saved = json.loads(path.read_text())
            answer = json.loads(path.with_name('solve-answer.json').read_text())
            # Once a recovery was attempted, its own error/evidence owns the retry budget.
            if (answer.get('confident') is False and saved.get('problem') and saved.get('fields')
                    and not (path.parent/'best-effort-input.json').exists()):
                return True
    except (OSError, ValueError, KeyError, TypeError):
        pass
    return False
