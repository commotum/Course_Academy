"""Build imported-content ownership from the pinned, read-only native export."""
import gzip
import json
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
META = {'question/math-academy-id', 'question/retired', 'tutorial/math-academy-id',
        'tutorial/title', 'knowledge-point/title', 'topic/title', 'topic/math-academy-id'}
LINKS = {'question/answer-fields', 'answer-field/choices', 'answer-field/correct',
         'knowledge-point/questions', 'knowledge-point/canonical-example',
         'topic/knowledge-points', 'activity/steps', 'step/content', 'activity/scope'}
CONTENT = {'question/problem': 'prompt', 'question/worked-solution': 'solution',
           'tutorial/content': 'tutorial', 'answer-field/key': 'label',
           'answer/value': 'answer', 'answer/feedback': 'feedback'}
meta = defaultdict(dict)
links = defaultdict(lambda: defaultdict(set))
parents = defaultdict(set)
fields = defaultdict(list)
answer_types = {}
source = HERE / 'snapshot.jsonl'
stream = source.open() if source.exists() else gzip.open(source.with_suffix('.jsonl.gz'), 'rt')
with stream:
    for line in stream:
        row = json.loads(line)
        eid, attr = row['e'], row['a']
        if attr == 'answer/type':
            answer_types[eid] = row.get('ref_ident')
        if attr in META:
            value = row['raw_string']
            if value is None:
                value = row['value_edn'] == 'true' if attr == 'question/retired' else int(row['value_edn'])
            meta[eid][attr] = value
        if attr in LINKS and row['ref_eid'] is not None:
            links[eid][attr].add(row['ref_eid'])
            parents[row['ref_eid']].add((eid, attr))
        if attr in CONTENT and isinstance(row['raw_string'], str):
            fields[eid].append({'entity': eid, 'attribute': attr, 'value': row['raw_string'], 'role': CONTENT[attr]})


def context(eid):
    seen, frontier, topics, kps = set(), {eid}, {}, {}
    for _ in range(5):
        nxt = set()
        for child in frontier - seen:
            seen.add(child)
            record = meta[child]
            if 'knowledge-point/title' in record:
                kps[child] = {'entity': child, 'title': record['knowledge-point/title']}
            if 'topic/title' in record:
                topics[child] = {'entity': child, 'title': record['topic/title']}
            for parent, attr in parents[child]:
                if attr in {'knowledge-point/questions', 'knowledge-point/canonical-example', 'topic/knowledge-points', 'step/content', 'activity/steps'}:
                    nxt.add(parent)
            nxt.update(links[child].get('activity/scope', set()))
        frontier = nxt
    return sorted(topics.values(), key=lambda x: x['entity']), sorted(kps.values(), key=lambda x: x['entity'])


questions, tutorials = [], []
for eid, metadata in list(meta.items()):
    qid, tid = metadata.get('question/math-academy-id'), metadata.get('tutorial/math-academy-id')
    if qid is None and tid is None:
        continue
    topics, kps = context(eid)
    own = { (f['entity'], f['attribute']): f for f in fields[eid] }
    for field_id in links[eid].get('question/answer-fields', set()):
        for f in fields[field_id]:
            own[f['entity'], f['attribute']] = f
        for answer_id in links[field_id].get('answer-field/choices', set()) | links[field_id].get('answer-field/correct', set()):
            for f in fields[answer_id]:
                own[f['entity'], f['attribute']] = f
    for f in own.values():
        if f['attribute'] == 'answer/value':
            f['math_type'] = answer_types.get(f['entity'])
            f['bare_math'] = f['math_type'] == 'answer.type/math'
    record = {'entity': eid, 'ma_id': str(qid) if qid is not None else 't-' + str(tid),
              'retired': metadata.get('question/retired', False), 'topics': topics,
              'knowledge_points': kps, 'fields': sorted(own.values(), key=lambda f: (f['entity'], f['attribute']))}
    (questions if qid is not None else tutorials).append(record)
manifest = json.loads((HERE / 'snapshot.manifest.json').read_text())
result = {'basis': manifest['basis_t'], 'questions': sorted(questions, key=lambda q: q['entity']),
          'tutorials': sorted(tutorials, key=lambda t: t['entity'])}
(HERE / 'current.json').write_text(json.dumps(result, ensure_ascii=False) + '\n')
print(json.dumps({'basis': result['basis'], 'questions': len(questions), 'tutorials': len(tutorials),
                  'fields': sum(len(q['fields']) for q in questions + tutorials)}))
