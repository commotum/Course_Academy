"""Keep fresh theorem generation unchanged; restore distinct source replay roles.

Original source input bytes are retained as evidence. Corrections are keyed by
source answer UUID, never by brace-insensitive mathematical normalization.
"""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import uuid
sys.dont_write_bytecode = True
_spec = importlib.util.spec_from_file_location('original_scalar_role_generator', Path(__file__).with_name('17592186124630.py'))
original = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(original)
_original_replay = original.replay
CORRECTIONS = {
    'q-140766': {'6b1a034d-0611-5f21-a47f-fb41d7d10986': '0'},
    'q-141192': {
        '10e2978f-44c4-5ccc-a792-625eb51d9546': '1',
        '9d9fdfe6-8dc9-510f-9c18-69a49e29297b': 'n',
    },
}
def replay(source_id):
    if source_id not in CORRECTIONS:
        return _original_replay(source_id)
    q = copy.deepcopy(original.SOURCES[source_id])
    for f in q[':question/answer-fields']:
        for a in f[':answer-field/choices']:
            if a[':answer/id'] in CORRECTIONS[source_id]:
                a[':answer/value'] = CORRECTIONS[source_id][a[':answer/id']]
    content = {k: q[k] for k in [':question/problem', ':question/worked-solution', ':question/answer-fields']}
    digest = hashlib.sha256(json.dumps(content, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    qid = uuid.uuid5(uuid.UUID(original.KP_UUID), 'source-role-replay-v1:' + source_id + ':' + digest)
    fields = []
    for f in q[':question/answer-fields']:
        fid = uuid.uuid5(qid, 'field:' + f[':answer-field/id'])
        source_correct = f[':answer-field/correct'][':answer/id']
        choices = []
        links = {}
        for a in f[':answer-field/choices']:
            kind = a[':answer/type'][':db/ident']
            aid = str(uuid.uuid5(fid, 'source-answer:' + a[':answer/id'] + ':' + kind + ':' + a[':answer/value']))
            links[a[':answer/id']] = aid
            choices.append({':answer/id': aid, ':answer/type': kind, ':answer/value': a[':answer/value']})
        assert len({a[':answer/id'] for a in choices}) == len(choices)
        fields.append({':answer-field/id': str(fid), ':answer-field/key': f[':answer-field/key'],
                       ':answer-field/type': f[':answer-field/type'][':db/ident'], ':answer-field/choices': choices,
                       ':answer-field/correct': [':answer/id', links[source_correct]]})
    result = _original_replay(source_id)
    result['question'] = {':question/id': str(qid), ':question/problem': q[':question/problem'],
                          ':question/worked-solution': q[':question/worked-solution'],
                          ':question/difficulty': ':question.difficulty/easy', ':question/answer-fields': fields}
    result['generation']['version'] += '+source-scalar-roles.1'
    result['generation']['source_role_corrections'] = CORRECTIONS[source_id]
    result['generation']['content_identity'] = 'Final problem, solution, corrected banks, and source answer roles'
    return result
original.replay = replay
generate = original.generate
make_record = original.make_record
if __name__ == '__main__':
    original.main()
