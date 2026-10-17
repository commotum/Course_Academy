"""Read-only structural audit of the four immutable topic Pull snapshots.

Run with PYTHONPATH=capture and the MA Python environment. This writes evidence
files beside this script; it performs no database reads or mutations.
"""
import collections
import json
import re
from pathlib import Path

from scripts.database.edn import loads


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
DISPLAY_ATTRS = (
    ':tutorial/content', ':question/problem', ':question/worked-solution',
    ':answer/value', ':answer/feedback', ':answer-field/feedback',
    ':knowledge-point/description', ':topic/description',
)
FLAT = re.compile(r'(?<!\\left)\\\{[^$\n]*=[^$\n]*;[^$\n]*=')
DOUBLE_MID = re.compile(r'\\mid\s*\\mid\s*\\cdot\s*\([^)]*\)')
CANONICAL_SYSTEM = re.compile(r'\\left\\\{\\begin\{aligned\}')


def save(name, value):
    (HERE / name).write_text(json.dumps(value, indent=2, default=str) + '\n')


def collect_entities(node, entities):
    if isinstance(node, dict):
        if ':db/id' in node:
            entities.setdefault(node[':db/id'], {}).update(node)
        for value in node.values():
            collect_entities(value, entities)
    elif isinstance(node, list):
        for value in node:
            collect_entities(value, entities)


fields, scope, findings, reviewed_questions = [], [], [], []
tutorial_evidence = {
    item['entity']: item
    for item in json.loads((ROOT / 'source' / 'tutorial-findings.json').read_text())
}
for path in sorted(ROOT.glob('175*.edn')):
    topic = loads(path.read_text())
    topic_id = topic[':db/id']
    entities = {}
    collect_entities(topic, entities)
    question_kps = collections.defaultdict(list)
    canonical_ids, practice_ids = set(), set()
    kps = [e for e in entities.values() if ':knowledge-point/title' in e]
    for kp in kps:
        canonical = kp.get(':knowledge-point/canonical-example', {}).get(':db/id')
        if canonical:
            canonical_ids.add(canonical)
            question_kps[canonical].append(kp[':db/id'])
        for question in kp.get(':knowledge-point/questions', []):
            question_id = question[':db/id']
            practice_ids.add(question_id)
            question_kps[question_id].append(kp[':db/id'])

    topic_fields = []
    for eid, entity in sorted(entities.items()):
        if ':question/problem' in entity:
            reviewed_questions.append({
                'topic': topic_id, 'entity': eid,
                'knowledge_points': sorted(set(question_kps[eid])),
                'canonical': eid in canonical_ids,
                'practice': eid in practice_ids,
                'math_academy_id': entity.get(':question/math-academy-id'),
                'has_worked_solution': ':question/worked-solution' in entity,
            })
        for attr in DISPLAY_ATTRS:
            value = entity.get(attr)
            if not isinstance(value, str):
                continue
            field = {
                'topic': topic_id, 'entity': eid, 'attribute': attr,
                'value': value,
                'source': ('captured_question' if entity.get(':question/math-academy-id')
                           else 'generated_or_authored_question' if ':question/problem' in entity
                           else 'captured_tutorial' if entity.get(':tutorial/math-academy-id')
                           else 'non_question_content'),
                'ma_id': entity.get(':question/math-academy-id', entity.get(':tutorial/math-academy-id')),
            }
            topic_fields.append(field)
            issues = []
            for match in FLAT.finditer(value):
                issues.append({
                    'category': 'flattened_equation_system',
                    'severity': 'display_error',
                    'exact_match': match.group(),
                    'reason': 'An escaped literal left brace and semicolons are '
                              'valid TeX but encode a single row, not a stacked '
                              'system. No aligned environment or row breaks '
                              'are present in this system.',
                    'start': match.start(), 'end': match.end(),
                })
            for match in DOUBLE_MID.finditer(value):
                issues.append({
                    'category': 'duplicated_elimination_annotation',
                    'severity': 'notation_cleanup',
                    'exact_match': match.group(),
                    'reason': 'Two literal relation bars are emitted before '
                              'the multiplier; canonical repaired lessons use '
                              'a readable multiply-by row annotation.',
                    'start': match.start(), 'end': match.end(),
                })
            if attr == ':tutorial/content' and eid in tutorial_evidence:
                evidence = tutorial_evidence[eid]
                issues.append({
                    'category': ('lost_numbered_list_hierarchy' if eid == 17592186097842
                                 else 'lost_display_math_blocks'),
                    'severity': 'display_error',
                    'reason': evidence['finding'],
                    'source_boundary': evidence['boundary'],
                    'original_source_html': evidence['original_html'],
                    'original_source_screenshot': evidence['source_screenshot'],
                    'normalized_source_json': evidence['normalized_json'],
                })
            if issues:
                findings.append({
                    **field, 'knowledge_points': sorted(set(question_kps[eid])),
                    'issues': issues,
                })

    scope.append({
        'topic': topic_id, 'title': topic.get(':topic/title'),
        'entities': len(entities),
        'questions': len(practice_ids | canonical_ids),
        'practice_questions': len(practice_ids),
        'canonical_examples': len(canonical_ids),
        'kps': len(kps),
        'tutorials': sum(':tutorial/content' in e for e in entities.values()),
        'fields': len(topic_fields),
        'fields_by_attr': dict(collections.Counter(f['attribute'] for f in topic_fields)),
        'generated_or_authored_questions': sum(
            ':question/problem' in e and ':question/math-academy-id' not in e
            for e in entities.values()),
        'canonical_system_occurrences': sum(len(CANONICAL_SYSTEM.findall(f['value'])) for f in topic_fields),
        'flat_system_occurrences': sum(len(FLAT.findall(f['value'])) for f in topic_fields),
        'duplicated_multiplier_occurrences': sum(len(DOUBLE_MID.findall(f['value'])) for f in topic_fields),
        'kps_details': [{
            'entity': kp[':db/id'], 'title': kp.get(':knowledge-point/title'),
            'question_count': len(kp.get(':knowledge-point/questions', [])),
            'canonical': kp.get(':knowledge-point/canonical-example', {}).get(':db/id'),
            'generator': kp.get(':knowledge-point/question-generator', {}).get(':question-generator/script'),
        } for kp in sorted(kps, key=lambda e: e[':db/id'])],
    })
    fields.extend(topic_fields)
    save(f'{topic_id}-entities.json', entities)

save('fields.json', fields)
save('scope.json', scope)
save('findings.json', findings)
save('reviewed-questions.json', reviewed_questions)
summary = {
    'database_snapshot': json.loads((ROOT / 'snapshot.json').read_text()),
    'read_only': True,
    'topics': len(scope),
    'knowledge_points': sum(t['kps'] for t in scope),
    'practice_questions': sum(t['practice_questions'] for t in scope),
    'canonical_examples': sum(t['canonical_examples'] for t in scope),
    'tutorials': sum(t['tutorials'] for t in scope),
    'display_fields': len(fields),
    'affected_fields': len(findings),
    'affected_entities': len({f['entity'] for f in findings}),
    'affected_questions': len({f['entity'] for f in findings if f['attribute'].startswith(':question/')}),
    'affected_tutorials': len({f['entity'] for f in findings if f['attribute'] == ':tutorial/content'}),
    'findings_by_topic': [{
        'topic': item['topic'], 'title': item['title'],
        'affected_fields': sum(f['topic'] == item['topic'] for f in findings),
        'issues_by_category': dict(collections.Counter(
            issue['category'] for f in findings if f['topic'] == item['topic'] for issue in f['issues'])),
    } for item in scope],
    'issues_by_category': dict(collections.Counter(i['category'] for f in findings for i in f['issues'])),
    'flat_system_questions': sorted({f['entity'] for f in findings if any(i['category'] == 'flattened_equation_system' for i in f['issues'])}),
    'double_mid_questions': sorted({f['entity'] for f in findings if any(i['category'] == 'duplicated_elimination_annotation' for i in f['issues'])}),
    'scope_notes': [
        'Display fields are deduplicated by entity and attribute within each topic.',
        'Missing worked solutions are counted but not treated as display errors.',
        'Nine encompassing-rationale metadata strings were inspected separately; they contain provenance prose, not learner question content.',
        'No bare fixed-size matrix fences, raw HTML, indented code blocks, or unpaired bare escaped system braces outside the 30 identified flat system occurrences were found.',
        'Rendering is independently checked in ../ui; passing TeX syntax does not prove system layout is semantically correct.',
        'No flat systems or duplicate multiplier bars occur in the three comparison topics at this basis.',
    ],
}
save('summary.json', summary)
print(json.dumps(summary, indent=2))
