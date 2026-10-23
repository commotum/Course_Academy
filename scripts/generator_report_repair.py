"""Route retained review/report work without turning it into author approval."""
from generator_review import evidence_only_review


def generator_repair_findings(history):
    """Return executable generator regressions, leaving runner work in history.

    Evidence repair belongs to the independent reviewer. Stored-pool changes
    belong to the runner and must be checked after the inventory repair. Neither
    can be satisfied by changing the generator's package or its author tests.
    """
    return [row for row in history.get("findings", [])
            if row["finding"]["kind"] not in {"evidence", "inventory"}]


def pending_report_repair(state, history, current_binding=None):
    """Find a misrouted evidence-only review of the exact retained candidate.

    The caller must verify the candidate, batch and source bytes before using
    this route, and run an independent reviewer again. No saved acceptance or
    author-staged report is installed by this helper. In particular, scanning
    stops at the newest review: an older report defect cannot mask a later
    generator defect.
    """
    previous = state.get("previous_review")
    if not isinstance(previous, dict) or not isinstance(previous.get("binding"), dict):
        return None
    if current_binding is None:
        # State-only callers can discover pending work. The pipeline must still
        # compare the returned binding with current policy and verified bytes.
        keys = ("package_hash", "batch_hash", "source_hash", "inventory_hash", "assets", "effective_difficulty")
        current_binding = {"policy_version": previous["binding"].get("policy_version"),
                           **{key: state.get(key) for key in keys}}
        if "engine_hash" in state:
            current_binding["engine_hash"] = state["engine_hash"]
    if previous["binding"] != current_binding:
        return None
    for event in reversed(history.get("events", [])):
        reason = event.get("reason")
        if not isinstance(reason, dict) or reason.get("verdict") not in {"accepted", "revise", "unsupported"}:
            continue
        if (not evidence_only_review(reason)
                or event.get("package_hash") != current_binding.get("package_hash")
                or not previous.get("directory")
                or event.get("review_directory") != previous["directory"]):
            return None
        return {"directory": previous["directory"], "binding": dict(current_binding), "reason": reason}
    return None
