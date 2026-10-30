"""Preserve the source generator's mathematics and repair table fence typography.

The original entrypoint and its declared input closure remain byte-identical.
Both CLI and Python callers format complete expressions before deriving new
content identities. Nothing is published or written to the EDB here.
"""
import contextlib
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import runpy
import sys
import uuid
from table_fences import MATH, scalable_table_fences

ORIGINAL_ENTRYPOINT = '17592186119806.py'
spec = importlib.util.spec_from_file_location('original_table_generator', Path(__file__).with_name(ORIGINAL_ENTRYPOINT))
original = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = original
spec.loader.exec_module(original)


def presentation(value, bare=False):
    if not isinstance(value, str):
        return value
    return scalable_table_fences(value) if bare else MATH.sub(lambda m: scalable_table_fences(m[0]), value)


def repair(record):
    record = json.loads(json.dumps(record))
    q = record['question']
    before = json.dumps(q, sort_keys=True)
    for key in (':question/problem', ':question/worked-solution'):
        if key in q:
            q[key] = presentation(q[key])
    fields = q.get(':question/answer-fields', [])
    for field in fields:
        if field.get(':answer-field/type') == ':answer-field.type/checkbox':
            field[':answer-field/key'] = presentation(field[':answer-field/key'])
        for key in (':answer-field/feedback',):
            if key in field:
                field[key] = presentation(field[key])
        for answer in field.get(':answer-field/choices', []):
            answer[':answer/value'] = presentation(answer[':answer/value'], answer.get(':answer/type') == ':answer.type/math')
            if ':answer/feedback' in answer:
                answer[':answer/feedback'] = presentation(answer[':answer/feedback'])
    after = json.dumps(q, sort_keys=True)
    if before == after:
        return record
    old_qid = q[':question/id']
    digest = hashlib.sha256(after.encode()).hexdigest()
    qid = uuid.uuid5(uuid.UUID(old_qid), 'scalable-table-fences-v1:' + digest)
    q[':question/id'] = str(qid)
    for field in fields:
        field_id = uuid.uuid5(qid, 'field:' + field[':answer-field/id'])
        field[':answer-field/id'] = str(field_id)
        answers = {}
        for answer in field.get(':answer-field/choices', []):
            old = answer[':answer/id']
            answer[':answer/id'] = str(uuid.uuid5(field_id, 'answer:' + old))
            answers[old] = answer[':answer/id']
        correct = field.get(':answer-field/correct')
        if correct:
            assert isinstance(correct, list) and correct[0] == ':answer/id'
            correct[1] = answers[correct[1]]
    generation = record.setdefault('generation', {})
    generation['formatting_repair'] = 'scalable-table-fences-v1'
    generation['version'] = str(generation.get('version', '')) + '+table-fences.1'
    return record


def result(value):
    if isinstance(value, list):
        return [repair(record) for record in value]
    if 'records' in value:
        return {**value, 'records': [repair(record) for record in value['records']]}
    return repair(value)


def generate(*args, **kwargs):
    return result(original.generate(*args, **kwargs))


def batch(*args, **kwargs):
    return result(original.batch(*args, **kwargs))


def main():
    buffer = io.StringIO()
    # Keep every existing CLI flag, including Markdown, while formatting the
    # same complete JSON records used by the player.
    args = sys.argv[:]
    markdown = '--format' in args and args[args.index('--format') + 1] == 'markdown'
    if markdown:
        sys.argv[sys.argv.index('--format') + 1] = 'json'
    with contextlib.redirect_stdout(buffer):
        if hasattr(original, 'main'):
            original.main()
        else:
            runpy.run_path(str(Path(__file__).with_name(ORIGINAL_ENTRYPOINT)), run_name='__main__')
    sys.argv[:] = args
    records = result(json.loads(buffer.getvalue()))
    if markdown:
        rows = records if isinstance(records, list) else records.get('records', [records])
        print('\n\n---\n\n'.join(original.markdown(row) for row in rows))
    else:
        print(json.dumps(records, indent=2))


if __name__ == '__main__':
    main()
