"""Freeze current visible content for the existing 19-topic study list; read only."""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'scripts'))
from migrate_learner_history import connection

IDS = [17592186000000 + n for n in [
    48535, 48459, 48202, 50537, 50677, 50032, 50426, 48257, 50150,
    49102, 50895, 49370, 50522, 48391, 50557, 48289, 50433, 50040, 49099]]
BASE = ROOT / 'reference/edb-math/audits/2026-11-08-topic-17592186048459'
db = connection()
basis = db.basis()
fields = {}
summaries = []


def add(entity, attribute, value, topic, role='prose', bare_math=False, bindings=None):
    if not isinstance(value, str) or not value.strip():
        return
    key = entity, attribute
    if key not in fields:
        fields[key] = dict(entity=entity, attribute=attribute, value=value, topics=[],
                           role=role, bare_math=bare_math)
        if bindings:
            fields[key]['fields'] = bindings
    if topic not in fields[key]['topics']:
        fields[key]['topics'].append(topic)


for tid in IDS:
    out = HERE / 'snapshot' / str(tid)
    topic = db.query((BASE / 'topic-before-query.edn').read_text(), [tid], out, 'topic', basis)[0][0]
    lessons = db.query((BASE / 'lessons-before-query.edn').read_text(), [tid], out, 'lessons', basis)
    questions = {}
    for kp in topic[':topic/knowledge-points']:
        for q in [kp.get(':knowledge-point/canonical-example')] + kp.get(':knowledge-point/questions', []):
            if q:
                questions[q[':db/id']] = q
    tutorials = set()
    for row in lessons:
        for step in row[0].get(':activity/steps', []):
            c = step[':step/content']
            if ':tutorial/content' in c:
                tutorials.add(c[':db/id'])
                add(c[':db/id'], ':tutorial/content', c[':tutorial/content'], tid)
    for q in questions.values():
        fs = q.get(':question/answer-fields', [])
        bindings = [dict(id=str(f[':db/id']), key=f[':answer-field/key'],
                         type=f[':answer-field/type'][':db/ident'].split('/')[-1]) for f in fs]
        add(q[':db/id'], ':question/problem', q.get(':question/problem'), tid, bindings=bindings)
        add(q[':db/id'], ':question/worked-solution', q.get(':question/worked-solution'), tid, 'solution')
        for f in fs:
            if f[':answer-field/type'][':db/ident'] == ':answer-field.type/checkbox':
                add(f[':db/id'], ':answer-field/key', f[':answer-field/key'], tid, 'choice')
            for a in f.get(':answer-field/choices', []) + [f.get(':answer-field/correct', {})]:
                if ':answer/value' not in a:
                    continue
                typ = a[':answer/type'][':db/ident']
                if typ in [':answer.type/math', ':answer.type/text']:
                    add(a[':db/id'], ':answer/value', a[':answer/value'], tid, 'choice',
                        typ == ':answer.type/math')
                add(a[':db/id'], ':answer/feedback', a.get(':answer/feedback'), tid, 'feedback')
    summaries.append(dict(entity=tid, title=topic[':topic/title'], questions=len(questions), tutorials=len(tutorials)))
    print(topic[':topic/title'], len(questions), flush=True)

(HERE / 'fields.json').write_text(json.dumps(list(fields.values()), indent=2) + '\n')
(HERE / 'snapshot.json').write_text(json.dumps(dict(basis=basis, read_only=True, topics=summaries,
    visible_fields=len(fields)), indent=2) + '\n')
print(f'Frozen basis {basis}: {len(fields)} visible fields in {len(IDS)} topics.', flush=True)
