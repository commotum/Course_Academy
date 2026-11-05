"""Route retained review/report work without turning it into author approval."""
from generator_review import evidence_only_review
import json
from pathlib import Path


def generator_repair_findings(history, superseded=()):
    """Return executable generator regressions, leaving runner work in history.

    Evidence repair belongs to the independent reviewer. Stored-pool changes
    belong to the runner and must be checked after the inventory repair. Neither
    can be satisfied by changing the generator's package or its author tests.
    """
    return [row for row in history.get("findings", [])
            if row["finding"]["kind"] not in {"evidence", "inventory"}
            and row['id'] not in superseded]


def finding_supersessions(path, history):
    """Validate explicit reviewer corrections; never erase original findings."""
    path = Path(path)
    value = json.loads(path.read_text())
    if (not isinstance(value, dict) or value.get('format') != 'course-academy-finding-dispositions-v1'
            or not isinstance(value.get('findings'), list)):
        raise ValueError('Invalid finding-dispositions.json')
    known = {row['id'] for row in history.get('findings', [])}
    ids = set()
    for row in value['findings']:
        if (not isinstance(row, dict) or row.get('id') not in known or row['id'] in ids
                or row.get('disposition') != 'superseded'
                or not isinstance(row.get('reason'), str) or not row['reason'].strip()
                or not isinstance(row.get('source_refs'), list) or not row['source_refs']
                or any(not isinstance(ref, str) or not ref.strip() for ref in row['source_refs'])
                or not isinstance(row.get('evidence_paths'), list) or not row['evidence_paths']
                or not isinstance(row.get('counterexample_path'), str)):
            raise ValueError('Supersession needs a known finding, source-backed reason and retained counterexample')
        for name in [*row['evidence_paths'], row['counterexample_path']]:
            if not isinstance(name, str) or not name:
                raise ValueError('Supersession evidence path must be nonempty')
            evidence = (path.parent / name).resolve()
            if (Path(name).is_absolute() or not evidence.is_relative_to(path.parent.resolve())
                    or not evidence.is_file() or not evidence.stat().st_size):
                raise ValueError('Supersession evidence is missing or escapes the review directory')
        ids.add(row['id'])
    return ids


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
