"""Exact offline fingerprint projection bundled from scripts/generator_publish.py. No delivery filtering."""
import hashlib, json, uuid

def jsonable(value):
    if isinstance(value, dict):
        return {str(k): jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [jsonable(v) for v in value]
    return str(value) if isinstance(value, uuid.UUID) else value

def digest(value):
    return hashlib.sha256(json.dumps(jsonable(value), sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()).hexdigest()

def enum(value):
    return str(value[':db/ident'] if isinstance(value, dict) else value)

def answer_id(value):
    if isinstance(value, dict):
        return str(value[':answer/id'])
    if isinstance(value, (list, tuple)) and len(value) == 2 and str(value[0]) == ':answer/id':
        return str(value[1])
    return str(value)

def normalized_question(question, *, identity=True):
    """Strip Pull metadata; preserve full authored content and response semantics."""
    q = question
    result = {k: q[k] for k in (':question/problem', ':question/worked-solution', ':question/requires-calculator') if k in q}
    if identity:
        result[':question/id'] = str(q[':question/id'])
    if ':question/difficulty' in q:
        result[':question/difficulty'] = enum(q[':question/difficulty'])
    fields = []
    for field in q.get(':question/answer-fields', []):
        item = {':answer-field/key': field[':answer-field/key'], ':answer-field/type': enum(field[':answer-field/type'])}
        if identity:
            item[':answer-field/id'] = str(field[':answer-field/id'])
        choices = []
        correct = answer_id(field.get(':answer-field/correct'))
        for a in field.get(':answer-field/choices', []):
            choice = {':answer/type': enum(a[':answer/type']), ':answer/value': a[':answer/value']}
            if ':answer/feedback' in a:
                choice[':answer/feedback'] = a[':answer/feedback']
            if identity:
                choice[':answer/id'] = str(a[':answer/id'])
            choices.append(choice)
            if str(a[':answer/id']) == correct:
                item[':answer-field/correct'] = str(a[':answer/id']) if identity else {k: choice[k] for k in (':answer/type', ':answer/value')}
        item[':answer-field/choices'] = sorted(choices, key=lambda a: json.dumps(a, sort_keys=True))
        fields.append(item)
    result[':question/answer-fields'] = sorted(fields, key=lambda f: f[':answer-field/key'])
    return jsonable(result)

def content_fingerprint(question):
    value = normalized_question(question, identity=False)
    value.pop(':question/worked-solution', None)
    value.pop(':question/difficulty', None)
    for field in value[':question/answer-fields']:
        for answer in field[':answer-field/choices']:
            answer.pop(':answer/feedback', None)
        if field[':answer-field/type'] in (':answer-field.type/blank', ':answer-field.type/free'):
            # Entered responses accumulate in these owned banks. They must not
            # turn the same mathematical prompt into a new practice identity.
            field.pop(':answer-field/choices', None)
    return digest(value)
