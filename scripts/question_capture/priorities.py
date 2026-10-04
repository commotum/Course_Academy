"""Directed content-capture priorities, independent of personal task eligibility."""
from collections import defaultdict, deque
from datetime import datetime, timezone


def assignment_topics(node):
    result = set()
    if isinstance(node, dict):
        result.update(t[':topic/math-academy-id'] for t in node.get(':assigned-problem/topic-coverage', []))
        for value in node.values():
            result.update(assignment_topics(value))
    elif isinstance(node, list):
        for value in node:
            result.update(assignment_topics(value))
    return result


def capture_scores(topic_ids, context, snapshot, at=None):
    """Mirror learning.rs target support/scoring without personal eligibility gates.

    The snapshot is the capture account's displayed state, not learner credit.
    Graph color conflicts remain unknown. No memory or task history is invented.
    """
    at = at or datetime.now(timezone.utc)
    bands = defaultdict(list)
    for course in (snapshot or {}).get('courses', []):
        for topic in course['topics']:
            bands[topic['topic_id']].append(topic['display_band'])
    ready = {mid for mid, observations in bands.items() if all(observations)}
    targets = {}
    if context['self_directed']:
        targets.update({mid:None for mid in context['targets']})
        for assignment in context['assignments']:
            if assignment['completed']:
                continue
            due = assignment['due']
            for mid in assignment['topics']:
                previous = targets.get(mid)
                targets[mid] = min(previous,due) if previous and due else previous or due
    support = defaultdict(lambda:dict(targets=set(),remaining=None,distance=None,due=None))
    for target, due in targets.items():
        distances, pending = {}, deque([(target,0)])
        while pending:
            mid, distance = pending.popleft()
            if mid in distances:
                continue
            distances[mid] = distance
            if mid not in ready:
                pending.extend((before,distance+1) for before in context['prerequisites'].get(mid,()))
        remaining = sum(mid not in ready for mid in distances)
        for mid, distance in distances.items():
            item = support[mid]
            item['targets'].add(target)
            for key,value in (('remaining',remaining),('distance',distance)):
                item[key] = min(item[key],value) if item[key] is not None else value
            if due:
                item['due'] = min(item['due'],due) if item['due'] else due
    report = {}
    for mid in topic_ids:
        item = support[mid]
        count = len(item['targets'])
        priority = 1.0
        if count:
            priority += 1000*count/(1+count)+100/(1+item['remaining'])+100/(1+item['distance'])
        if item['due']:
            hours = max(0,int((item['due']-at).total_seconds()/3600))
            priority += 250/(1+hours/24)
        report[mid] = dict(priority=priority,target_count=count,
            supporting_targets=sorted(item['targets']),remaining_topics=item['remaining'],
            nearest_target_steps=item['distance'],due=item['due'].isoformat() if item['due'] else None)
    return report
