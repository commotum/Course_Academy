"""Keep historical multipart questions out of standalone content imports.

This is source provenance, not a new question attribute. Runtime membership is
still represented by multistep/steps -> step/content in EDB.
"""
import json
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


@lru_cache(maxsize=256)
def _source_kind(path, modified_ns):
    record = json.loads(Path(path).read_text())
    kind = record.get('task_type') or record.get('activity-type')
    if kind:
        return str(kind).lower()
    text = record.get('task_text', '').strip()
    return text.splitlines()[0].strip().lower() if text else None


def historical_task_type(question, root=ROOT):
    provenance = question.get('provenance', {})
    explicit = provenance.get('task_type') or provenance.get('activity_type')
    if explicit:
        return str(explicit).lower()
    if provenance.get('source_kind') != 'completed historical activity':
        return None
    source = provenance.get('source_file')
    if not source:
        return None
    path = (root / source).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError('Historical source must be inside the repository')
    if not path.is_file():
        if provenance.get('source_kind') == 'completed historical activity':
            raise ValueError('Historical activity provenance cannot be verified: ' + source)
        return None
    return _source_kind(str(path), path.stat().st_mtime_ns)


def require_activity_context(content):
    """Full multistep imports build containment in the same transaction.

Older historical exports omitted task_type; resolve their saved source too.
Question-only importers must defer these records, not flatten their prompts.
"""
    if content.get('task_type') == 'multistep':
        return
    for question in content.get('questions', []):
        if historical_task_type(question) == 'multistep':
            raise ValueError('Historical multistep part requires its complete activity: '
                             + question['math_academy_id'])
