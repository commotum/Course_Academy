"""Choose from the queue using activity status and downstream targets."""
from collections import deque

from .models import normalize_activity


def _ids(values):
    return {str(v.get("topic_id", v.get("id"))) if isinstance(v, dict) else str(v) for v in values}


def target_support(topic_id, graph, targets):
    targets = _ids(targets)
    pending = deque([(str(topic_id), 0)]) if topic_id is not None else deque()
    distances = {}
    while pending:
        topic, distance = pending.popleft()
        if topic in distances:
            continue
        distances[topic] = distance
        pending.extend((str(next_topic), distance + 1) for next_topic in graph.get(topic, ()))
    support = {topic: distances[topic] for topic in sorted(targets & distances.keys())}
    nearest = min(support.values(), default=None)
    return {"supporting_targets": list(support), "target_distances": support,
            "target_count": len(support), "nearest_target_steps": nearest,
            "score": len(support) + (1 / (1 + nearest) / 1000 if nearest is not None else 0)}


def level(activity):
    kind = activity["kind"]
    if activity.get("started"):
        return {"assessment": 0, "diagnostic": 1, "lesson": 2, "review": 2, "multistep": 3}.get(kind, 3)
    return {"diagnostic": 4, "lesson": 5, "review": 5, "multistep": 6, "assessment": 7}.get(kind, 8)


def choose(queue, context=None, completed=()):
    context = context or {}
    completed = set(map(str, completed))
    graph = {str(k): [str(v) for v in values] for k, values in context.get("graph", {}).items()}
    candidates = []
    for position, raw in enumerate(queue):
        activity = normalize_activity(raw, position)
        if activity["task_id"] in completed:
            continue
        score = target_support(activity.get("topic_id"), graph, context.get("targets", []))
        priority = level(activity)
        # Count target support first, then proximity; equal scores preserve MA order.
        ranked_score = score["score"] if activity["kind"] in ("lesson", "review") else 0
        candidates.append(((priority, -ranked_score, activity["position"]), activity, score))
    if not candidates:
        return None
    _, selected, score = min(candidates, key=lambda candidate: candidate[0])
    selected["selection"] = {"priority_level": level(selected) + 1, **score,
        "context_basis": context.get("basis"), "target_origins": context.get("target_origins", {}),
        "score_reason": "downstream_target_support" if context.get("targets") else "no_target_configuration_queue_order"}
    return selected
