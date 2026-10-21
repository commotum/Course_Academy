"""One ordering policy for generator discovery and the durable workers.

The numeric score remains useful for diagnostics, but cannot express the hard
boundaries between relevance, purpose, and lesson order.
"""
from datetime import datetime, timezone


PRIORITY_POLICY = "relevance-v5"
PRIORITY_FIELDS = (
    "priority_policy", "relevance_tier", "baseline_relevance_tier", "topic_layer",
    "selected_support_count", "engine_priority", "review_due_at",
    "first_studied_at", "waiting_since",
)
PURPOSE_ORDER = {
    "lesson-shortage": 0,
    "review-shortage": 1,
    "assessment-shortage": 2,
    "hard-variety": 3,
    "moderate-variety": 4,
    "easy-variety": 5,
    "advance-build": 6,
    "routine-replenishment": 6,
}


def timestamp(value):
    if not value:
        return float("inf")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return parsed.replace(tzinfo=parsed.tzinfo or timezone.utc).timestamp()
    except (AttributeError, TypeError, ValueError):
        return float("inf")


def priority_key(record):
    """Order a finder KP/reason or a worker request with the same comparison.

    Topic identity precedes KP deficit so one lesson's deficient KPs stay
    together. Legacy durable jobs retain their previous relative order but wait
    behind refreshed jobs until discovery supplies their new policy metadata.
    """
    purpose = record.get("purpose", "advance-build")
    topic = record.get("topic_entity", record.get("topic", 0))
    kp = record.get("db/id", record.get("knowledgePoint", 0))
    band = record.get("generated_band", record.get("difficulty", ""))
    waiting = timestamp(record.get("waiting_since"))
    if "priority_policy" not in record and "relevance_tier" not in record:
        return (5, 0, -record.get("score", 0),
                timestamp(record.get("first_studied_at")) if purpose == "assessment-shortage" else float("inf"),
                0, waiting, topic, 0, kp, band)

    engine = -float(record.get("engine_priority") or 0)
    if purpose == "lesson-shortage":
        layer = record.get("topic_layer")
        topic_order = (float("inf") if layer is None else layer,
                       -(record.get("selected_support_count") or 0), engine)
    elif purpose == "review-shortage":
        topic_order = (timestamp(record.get("review_due_at")), 0, engine)
    elif purpose == "assessment-shortage":
        topic_order = (timestamp(record.get("first_studied_at")), 0, engine)
    else:
        topic_order = (0, 0, engine)
    return (record.get("relevance_tier", 4), PURPOSE_ORDER.get(purpose, 7),
            *topic_order, waiting, topic, -record.get("shortage", 0), kp,
            band)
