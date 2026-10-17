"""Read-only, fixed-basis focused scan of current MTH 341 target questions."""
import collections
import concurrent.futures
import json
import re
import threading
from pathlib import Path

from scripts.config import Config
from scripts.database.client import EDBClient
from scripts.database.edn import dumps, kw, loads


ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'wide-mth341'
OUT.mkdir(exist_ok=True)
SNAPSHOT = json.loads((ROOT / 'snapshot.json').read_text())
BASIS = SNAPSHOT['basis']
DB = EDBClient(Config(), threading.Event())
PATTERN = '''[:db/id :topic/title
 {[:topic/knowledge-points :limit nil]
  [:db/id :knowledge-point/title
   {:knowledge-point/canonical-example
    [:db/id :question/math-academy-id :question/problem :question/worked-solution]}
   {[:knowledge-point/questions :limit nil]
    [:db/id :question/math-academy-id :question/problem :question/worked-solution]}]}]'''
(OUT / 'question-pull.edn').write_text(PATTERN + '\n')
(OUT / 'snapshot.json').write_text(json.dumps(SNAPSHOT, indent=2) + '\n')
current = dict(loads((ROOT / 'current-targets.edn').read_text()))
old = json.loads((ROOT.parent / '2026-10-16-mth341' / 'topic-ids.json').read_text())
added = json.loads((ROOT.parent / '2026-10-16-mth341-added-targets' / 'topic-ids.json').read_text())
candidates = set(old) | set(added) | {17592186048146, 17592186049044}
ids = sorted(candidates & current.keys())
(OUT / 'scope-inputs.json').write_text(json.dumps({
    'original_topic_ids': old, 'added_topic_ids': added,
    'determinant_topic_ids': [17592186048146, 17592186049044],
    'selected_current_topic_ids': ids,
    'noncurrent_candidates_excluded': sorted(candidates - current.keys()),
}, indent=2) + '\n')


def one(eid):
    path = OUT / f'{eid}.edn'
    reused = ROOT / f'{eid}.edn'
    if path.exists():
        text = path.read_text()
        origin = 'retained wide-scan pull at recorded basis'
    elif reused.exists():
        # The pre-existing full Pull is already fixed at this audit's basis.
        full = loads(reused.read_text())
        compact = {kw(k): full[k] for k in [':db/id', ':topic/title']}
        compact[kw(':topic/knowledge-points')] = []
        for kp in full.get(':topic/knowledge-points', []):
            k = {kw(key): kp[key] for key in [':db/id', ':knowledge-point/title'] if key in kp}
            for attr in [':knowledge-point/canonical-example', ':knowledge-point/questions']:
                if attr not in kp:
                    continue
                qlist = kp[attr] if isinstance(kp[attr], list) else [kp[attr]]
                selected = [{kw(key): q[key] for key in [':db/id', ':question/math-academy-id', ':question/problem', ':question/worked-solution'] if key in q} for q in qlist]
                k[kw(attr)] = selected if isinstance(kp[attr], list) else selected[0]
            compact[':topic/knowledge-points'].append(k)
        text = dumps(compact) + '\n'
        path.write_text(text)
        origin = str(reused.relative_to(ROOT))
    else:
        text = DB.command('pull', '--as-of', BASIS, '--file', OUT / 'question-pull.edn',
                          '--entity', eid, '--max-depth', '20', '--max-entities', '50000')
        path.write_text(text)
        origin = 'fresh minimal pull at recorded basis'
    return loads(text), origin


with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    topics = list(pool.map(one, ids))

flat = re.compile(r'(?<!\\left)\\\{[^$\n]*=[^$\n]*;[^$\n]*=')
double = re.compile(r'\\mid\s*\\mid\s*\\cdot\s*\([^)]*\)')
unescaped = re.compile(r'(?<![\\\w])\{[^{}$\n]*=[^{}$\n]*;[^{}$\n]*=')
all_fields, findings, scope = [], [], []
for topic, origin in topics:
    qmap = {}
    kpmap = collections.defaultdict(set)
    canonical, practice = set(), set()
    for kp in topic.get(':topic/knowledge-points', []):
        for kind in [':knowledge-point/canonical-example', ':knowledge-point/questions']:
            vals = kp.get(kind, [])
            if not isinstance(vals, list):
                vals = [vals]
            for q in vals:
                eid = q[':db/id']
                qmap.setdefault(eid, {}).update(q)
                kpmap[eid].add(kp[':db/id'])
                (canonical if kind.endswith('canonical-example') else practice).add(eid)
    fields = []
    for eid, question in sorted(qmap.items()):
        for attr in [':question/problem', ':question/worked-solution']:
            if attr not in question:
                continue
            value = question[attr]
            field = {'topic': topic[':db/id'], 'topic_title': topic.get(':topic/title'),
                     'entity': eid, 'knowledge_points': sorted(kpmap[eid]),
                     'attribute': attr, 'ma_id': question.get(':question/math-academy-id'),
                     'value': value}
            fields.append(field)
            issues = []
            for name, pattern in [('flattened_equation_system', flat),
                                  ('duplicated_elimination_annotation', double),
                                  ('unescaped_flat_system_candidate', unescaped)]:
                for match in pattern.finditer(value):
                    issues.append({'category': name, 'exact_match': match.group(),
                                   'start': match.start(), 'end': match.end()})
            if issues:
                findings.append({**field, 'issues': issues})
    all_fields.extend(fields)
    topic_findings = [f for f in findings if f['topic'] == topic[':db/id']]
    scope.append({'topic': topic[':db/id'], 'title': topic.get(':topic/title'),
                  'source': origin, 'kps': len(topic.get(':topic/knowledge-points', [])),
                  'practice_questions': len(practice), 'canonical_examples': len(canonical),
                  'questions': len(qmap), 'fields': len(fields),
                  'affected_fields': len(topic_findings),
                  'affected_questions': len({f['entity'] for f in topic_findings}),
                  'occurrences_by_category': dict(collections.Counter(i['category'] for f in topic_findings for i in f['issues']))})
summary = {'snapshot': SNAPSHOT, 'read_only': True,
           'topics': len(scope), 'kps': sum(s['kps'] for s in scope),
           'questions': sum(s['questions'] for s in scope),
           'practice_questions': sum(s['practice_questions'] for s in scope),
           'canonical_examples': sum(s['canonical_examples'] for s in scope),
           'fields': len(all_fields), 'affected_fields': len(findings),
           'affected_questions': len({f['entity'] for f in findings}),
           'affected_topics': [s for s in scope if s['affected_fields']],
           'occurrences_by_category': dict(collections.Counter(i['category'] for f in findings for i in f['issues'])),
           'scope_limit': 'Targeted content scan of question prompts and existing worked solutions only. The four named topics separately have complete content and UI-render audits.'}
for name, value in [('scope.json', scope), ('fields.json', all_fields), ('findings.json', findings), ('summary.json', summary)]:
    (OUT / name).write_text(json.dumps(value, indent=2) + '\n')
print(json.dumps(summary, indent=2))
