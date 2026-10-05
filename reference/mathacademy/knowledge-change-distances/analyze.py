"""Analyze saved display-band changes against an already exported read-only graph."""
import json
from collections import defaultdict, deque, Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
graph = json.loads((HERE / 'graph.json').read_text())
names = dict(graph['topics'])
down, up, either = defaultdict(set), defaultdict(set), defaultdict(set)
for a, b in graph['edges']:
    down[a].add(b); up[b].add(a); either[a].add(b); either[b].add(a)

def paths(origins, adjacency):
    result = {a: [a] for a in origins}
    queue = deque(sorted(origins))
    while queue:
        a = queue.popleft()
        for b in sorted(adjacency[a]):
            if b not in result:
                result[b] = result[a] + [b]; queue.append(b)
    return result

snapshots = []
for p in (ROOT / 'reference/mathacademy/question-capture').glob('*/knowledge-state/*-completed.json'):
    snapshot = json.loads(p.read_text())
    snapshots.append((snapshot['finished_at'], p, snapshot))
snapshots.sort()
rows, activities = [], []
for index, (finished, p, snapshot) in enumerate(snapshots):
    directory = p.parents[1]
    state = json.loads((directory / 'state.json').read_text())
    content_path = directory / 'content.json'
    content = json.loads(content_path.read_text()) if content_path.exists() else {}
    origins = {state['topic_id']} if state.get('topic_id') else {
        q['topic_id'] for q in content.get('questions', []) if q.get('topic_id')}
    previous_path = state.get('previous_activity_snapshot')
    previous_finished = (json.loads(Path(previous_path).read_text())['finished_at']
                         if previous_path and Path(previous_path).exists() else None)
    consecutive = previous_finished == snapshots[index-1][0] if index else False
    activity = {'task_id': snapshot['task_id'], 'type': state['task_type'],
        'activity_title': names.get(state.get('topic_id')) or content.get('title'),
        'origins': sorted(origins), 'snapshot': str(p), 'finished_at': finished,
        'comparison_available': snapshot.get('comparison_available', bool(snapshot['changes'])),
        'comparison_is_consecutive': consecutive,
        'recovered': snapshot.get('recovered_after_interruption', False),
        'changed_rows': len(snapshot['changes']), 'changed_topics': len({c['topic_id'] for c in snapshot['changes']})}
    activities.append(activity)
    distance_maps = {k: paths(origins, adjacency) for k, adjacency in
                     [('undirected', either), ('prerequisite', up), ('downstream', down)]}
    for change in snapshot['changes']:
        tid = change['topic_id']
        record = {**activity, **change, 'paths': {k: m.get(tid) for k, m in distance_maps.items()},
                  'topic_in_database': tid in names}
        record['distances'] = {k: len(path)-1 if path else None for k, path in record['paths'].items()}
        for kind, path in record['paths'].items():
            if path:
                adjacency = {'undirected': either, 'prerequisite': up, 'downstream': down}[kind]
                assert path[0] in origins and path[-1] == tid
                assert all(b in adjacency[a] for a, b in zip(path, path[1:]))
        rows.append(record)

summary = {'database_basis': graph['basis'], 'database_topics': len(names),
    'prerequisite_edges': len(graph['edges']), 'snapshot_count': len(activities),
    'activity_types': dict(Counter(a['type'] for a in activities)),
    'changed_course_rows': len(rows), 'changed_task_topic_pairs': len({(r['task_id'], r['topic_id']) for r in rows}),
    'snapshots_without_comparison': sum(not a['comparison_available'] for a in activities),
    'changes_missing_database_topic': sum(not r['topic_in_database'] for r in rows),
    'changes_without_undirected_path': sum(r['distances']['undirected'] is None for r in rows)}
for direction in distance_maps:
    reachable = [r for r in rows if r['distances'][direction] is not None]
    maximum = max((r['distances'][direction] for r in reachable), default=None)
    winners = [r for r in reachable if r['distances'][direction] == maximum]
    summary[direction] = {'maximum': maximum, 'winners': winners}
    clean = [r for r in reachable if r['comparison_is_consecutive'] and not r['recovered']]
    clean_max = max((r['distances'][direction] for r in clean), default=None)
    summary[direction]['consecutive_unrecovered_maximum'] = clean_max
    summary[direction]['consecutive_unrecovered_winners'] = [r for r in clean if r['distances'][direction] == clean_max]

(HERE / 'results.json').write_text(json.dumps({'summary': summary, 'topic_names': names,
                                            'activities': activities, 'changes': rows}, indent=2)+'\n')
lines = ['# Distance of logged knowledge changes from activity topics', '',
    f"Read-only database basis: {graph['basis']}. Graph: {len(names)} topics and {len(graph['edges'])} direct `:topic/next` edges.", '',
    f"Analyzed {len(activities)} completed-activity snapshots and {len(rows)} changed course/topic rows.", '',
    'Distance means the shortest path, then the maximum among changed topics. Prerequisite distance traces edges backward from the activity; downstream follows them forward; undirected permits either direction. For assessments/multisteps the origin is the nearest of their actually captured question topics. No encompassing or KP remediation edges are included.', '',
    'These are changes in displayed bands between snapshots, not exact repetitions or proof that the activity caused every change. Recovered or nonconsecutive comparisons are retained and identified in results.json.', '']
for direction in ('prerequisite', 'undirected', 'downstream'):
    lines += [f"## Maximum {direction} distance: {summary[direction]['maximum']} edges", '']
    seen = set()
    for r in summary[direction]['winners']:
        key = r['task_id'], r['topic_id']
        if key in seen: continue
        seen.add(key)
        lines += [f"Task {r['task_id']} ({r['type']}): {r['activity_title'] or 'multiple captured topics'} → {r['title']}; band {r['before_band']} → {r['after_band']}.", '',
            ' → '.join(names[t] for t in r['paths'][direction]), '']
lines += ['## Per-activity maxima', '',
    '| Task | Activity | Changed topics | Upstream prerequisite edges | Either direction | Farthest upstream changed topic |',
    '|---|---|---:|---:|---:|---|']
by_task = defaultdict(list)
for r in rows: by_task[r['task_id']].append(r)
for a in activities:
    selected = by_task[a['task_id']]
    distances = {k: max((r['distances'][k] for r in selected if r['distances'][k] is not None), default=None)
                 for k in ('prerequisite', 'undirected')}
    farthest = sorted({r['title'] for r in selected if distances['prerequisite'] is not None and
                       r['distances']['prerequisite'] == distances['prerequisite']})
    d = {k: str(v) if v is not None else '—' for k,v in distances.items()}
    lines.append(f"| {a['task_id']} | {a['type']}: {a['activity_title'] or 'multiple captured topics'} | {a['changed_topics']} | {d['prerequisite']} | {d['undirected']} | {'; '.join(farthest)} |")
(HERE / 'report.md').write_text('\n'.join(lines)+'\n')
print(json.dumps({k: v for k,v in summary.items() if k not in distance_maps}, indent=2))
for kind in distance_maps:
    print(kind, 'max', summary[kind]['maximum'], 'consecutive max', summary[kind]['consecutive_unrecovered_maximum'])
    seen = set()
    for r in summary[kind]['winners']:
        key = r['task_id'], r['topic_id']
        if key in seen: continue
        seen.add(key)
        print(json.dumps({'activity': r['activity_title'], 'task': r['task_id'], 'changed': names.get(r['topic_id']),
                          'band': [r['before_band'], r['after_band']], 'consecutive': r['comparison_is_consecutive'],
                          'recovered': r['recovered'], 'path': [(t, names.get(t)) for t in r['paths'][kind]]}, ensure_ascii=False))
