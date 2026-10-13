"""Read saved capture output for the dashboard; never query or write the database."""
from datetime import datetime
import hashlib
import math
from pathlib import Path
import re

from .database.edn import loads
from .storage import read_json

KINDS = ('lesson', 'review', 'assessment', 'multistep', 'diagnostic')
_YIELD_CACHE = {}
_RECEIPT_CACHE = {}


def number(value):
    return value if isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value) else None


def capture_integrity(items):
    """Separate missing source evidence from deliberately preserved corrections."""
    gaps, activities, protected = set(), set(), set()
    for item in items:
        directory = item.get('capture_directory') or item.get('account') or 'unknown capture'
        omissions = item.get('result', {}).get('omissions', [])
        for omission in omissions:
            if omission.get('constraint') == 'separately_attributed_correction':
                protected.add(omission.get('id'))
            elif omission.get('kind') == 'question' or omission.get('kind') is None and omission.get('id'):
                activities.add(directory)
                gaps.add(omission.get('id') or omission.get('observed_math_academy_id') or
                         (directory, omission.get('capture_key') or omission.get('reason')))
        # A missing wrapper without a protected correction or a question gap is
        # still incomplete capture, rather than a successful complete import.
        if any(o.get('kind') in ('lesson','review','assessment','multistep','diagnostic') for o in omissions) and not any(
                o.get('constraint') == 'separately_attributed_correction' for o in omissions):
            activities.add(directory)
    return {'capture_gap_items': len(gaps), 'capture_gap_activities': len(activities),
            'preserved_corrections': len(protected - {None})}


def _read(path):
    try:
        return read_json(path, {}) or {}
    except (OSError, ValueError, UnicodeError):
        return {}


def output_metrics(config, completed, today, course_id):
    ledger = _read(config.state_root / 'xp.json')
    counts = dict.fromkeys(KINDS, 0)
    for task, item in completed.items():
        try:
            date = datetime.fromtimestamp(item['capture_completed_at']).astimezone().date().isoformat()
        except (KeyError, TypeError, ValueError, OverflowError, OSError):
            continue
        kind = item.get('kind') or ledger.get(task, {}).get('kind')
        if date == today and kind in counts:
            counts[kind] += 1
    # XP accounting can precede the runner's final completed marker.
    for task, item in ledger.items():
        if task not in completed and item.get('date') == today and item.get('kind') in counts:
            counts[item['kind']] += 1
    entries = sorted(ledger.values(), key=lambda item: number(
        completed.get(str(item.get('task_id')), {}).get('capture_completed_at'))
        or number(item.get('observed_at')) or 0)
    daily = [item for item in entries if item.get('date') == today]
    bases = [number(item.get('base_xp')) for item in daily]
    base = sum(value for value in bases if value is not None) if any(value is not None for value in bases) else None
    recent = [{'task_id': item.get('task_id'), 'earned_xp': number(item.get('earned_xp')),
               'base_xp': number(item.get('base_xp'))} for item in entries[-20:]]
    percent, observed_at = None, None
    # The dashboard observation holds MA's percentage; topic colors don't imply it.
    for item in reversed(entries[-20:]):
        if not item.get('source'):
            continue
        post = _read(Path(item['source']) / 'post-activity.json')
        observation = post.get('observations', {})
        progress = observation.get('dashboard', {}).get('course_progress', {})
        if str(progress.get('course_id')) != str(course_id):
            continue
        match = re.fullmatch(r'\s*(\d+(?:\.\d+)?)\s*%\s*', str(progress.get('displayed_progress') or ''))
        if match and 0 <= float(match[1]) <= 100:
            percent, observed_at = float(match[1]), observation.get('observed_at')
            break
    return {'activity_counts': counts, 'today_base_xp': base,
            'base_xp_unknown_tasks': sum(value is None for value in bases),
            'recent_activities': recent, 'percent_complete': percent,
            'progress_observed_at': observed_at}


def _source_ids(value):
    ids = set()
    if isinstance(value, dict):
        if value.get(':question/math-academy-id'):
            ids.add(str(value[':question/math-academy-id']))
        for child in value.values():
            ids.update(_source_ids(child))
    elif isinstance(value, list):
        for child in value:
            ids.update(_source_ids(child))
    return ids


def _receipt_ids(request, receipt_text):
    """Parse a shared batch snapshot/receipt once across its activity archives."""
    key = (request.get('request_key'),
        hashlib.sha256(request['snapshot_edn'].encode()).hexdigest(),
        hashlib.sha256(receipt_text.encode()).hexdigest())
    if key in _RECEIPT_CACHE:
        return _RECEIPT_CACHE[key]
    snapshot = loads(request['snapshot_edn'])
    receipt = loads(receipt_text)
    if receipt.get(':edb/committed') is not True:
        raise ValueError('Uncommitted receipt cannot establish question yield')
    aid = next(a[0] for a in snapshot['attributes'] if str(a[1]) == ':question/math-academy-id')
    before = _source_ids(snapshot.get('entities',[]))
    added = {str(d[2]) for d in receipt.get(':edb/tx-data',[])
             if d[1] == aid and d[-1] is True and str(d[2]) not in before}
    if len(_RECEIPT_CACHE)>=128:
        _RECEIPT_CACHE.pop(next(iter(_RECEIPT_CACHE)))
    _RECEIPT_CACHE[key] = added
    return added


def _import_ids(item):
    root = Path(item['capture_directory']) / 'database'
    preparation = root / 'preparation.json'
    archives = sorted((root / 'requests').glob('*/request.json'))
    paths = [preparation, *archives, *[path.with_name('receipt.edn') for path in archives]]
    stamp = tuple((str(path), path.stat().st_mtime_ns, path.stat().st_size) for path in paths if path.exists())
    key = str(root)
    cached = _YIELD_CACHE.get(key)
    if cached and cached[0] == stamp:
        return cached[1]
    prepared = _read(preparation)
    if not prepared.get('content'):
        return None
    omitted = {str(o['id']) for o in prepared.get('omissions', []) if o.get('kind') == 'question' and o.get('id')}
    content = prepared['content']
    imported = {str(q['math_academy_id']) for q in content.get('questions', []) + content.get('canonical_examples', [])
                if q.get('math_academy_id')} - omitted
    added = set()
    for path in archives:
        status = _read(path.with_name('result.json')).get('status')
        if status not in ('verified', 'confirmed_needs_reconciliation'):
            continue
        request = _read(path)
        try:
            added.update(_receipt_ids(request,path.with_name('receipt.edn').read_text()))
        except (OSError, ValueError, KeyError, TypeError, IndexError, StopIteration):
            return None
    if item.get('status') == 'verified' and not archives:
        return None
    result = (imported, added & imported)
    _YIELD_CACHE[key] = (stamp, result)
    return result


def question_yield(items, today):
    imported, added, unavailable = set(), set(), 0
    for item in items:
        try:
            date = datetime.fromtimestamp(item['last_attempt_at']).astimezone().date().isoformat()
            if date != today:
                continue
            result = _import_ids(item)
            if result is None:
                unavailable += 1
                continue
            imported.update(result[0])
            added.update(result[1])
        except (KeyError, OSError, ValueError, TypeError, OverflowError):
            unavailable += 1
    return {'added': len(added), 'existing': len(imported - added), 'unknown_imports': unavailable}


def log_tail(path, limit=80):
    try:
        path = Path(path)
        with path.open('rb') as stream:
            stream.seek(0, 2)
            size = stream.tell()
            start = max(0, size - 32768)
            stream.seek(start)
            data = stream.read()
        lines = data.decode('utf-8', errors='replace').splitlines()
        if start and lines:
            lines.pop(0)
        return lines[-limit:], path.stat().st_mtime
    except (OSError, TypeError):
        return [], None
