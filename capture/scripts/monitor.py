"""Read-only account cards from capture checkpoints and supervisor records."""
from datetime import datetime
import json
from pathlib import Path
import shutil
import time
import math
import re
import unicodedata
import textwrap

from .outbox import FINAL, target_id
from .courses import course_label, current_course, ORIGINAL_COURSE_CODES
from .storage import read_json
from .profiles import account_profile
from .monitor_data import log_tail, number, output_metrics, question_yield, capture_integrity

STAGES = {'activity': 'Answering', 'history': 'Reviewing history', 'complete': 'Capture saved',
          'capturing': 'Capturing', 'selecting': 'Selecting', 'waiting_for_queue': 'Waiting for queue',
          'recovering': 'Recovering', 'stopped': 'Stopped', 'starting': 'Starting',
          'pacing': 'Resting between activities',
          'waiting_for_context': 'Reading course topics',
          'waiting_for_solver_dependency': 'Waiting for solver recovery'}


def process_running(record):
    """A matching Linux process start token prevents stale PID reuse."""
    try:
        pid = int(record['pid'])
        if pid <= 1 or record.get('process_token') is None:
            return False
        fields = Path(f'/proc/{pid}/stat').read_text().rsplit(')', 1)[1].split()
        return fields[0] not in ('Z', 'X') and fields[19] == str(record['process_token'])
    except (KeyError, OSError, ValueError, IndexError, TypeError):
        return False


def _read(path, errors):
    try:
        value = read_json(path, {})
        if value is None:  # active.json is deliberately cleared to null.
            return {}
        if not isinstance(value, dict):
            raise ValueError('Expected a JSON object')
        return value
    except (OSError, ValueError, UnicodeError):
        errors.append(f'Cannot read {Path(path).name}')
        return {}


def _error(value):
    if isinstance(value, dict):
        return ': '.join(str(value.get(key)) for key in ('type', 'message') if value.get(key))
    return str(value) if value else ''


def snapshot(config, running=None, *, details=True):
    errors = []
    worker = _read(config.state_root / 'worker.json', errors)
    status = _read(config.state_root / 'status.json', errors)
    supervised = process_running(worker)
    child_running = process_running({'pid': worker.get('child_pid'), 'process_token': worker.get('child_token')})
    is_running = (supervised or child_running) if running is None else bool(running)
    if running is None and child_running and not supervised:
        errors.append('Supervisor exited; capture process is still running')
    started = worker.get('started_at')
    stale_status = (is_running and isinstance(started, (int, float))
                    and (status.get('at') or 0) < started)
    active = _read(config.state_root / 'active.json', errors)
    activity = active.get('activity') or {}
    directory = Path(active['directory']) if active.get('directory') else None
    checkpoint = _read(directory / 'checkpoint.json', errors) if directory else {}
    today = datetime.now().astimezone().date().isoformat()
    daily = _read(config.state_root / 'daily-xp.json', errors).get(today, {})
    daily = daily if isinstance(daily, dict) else {}
    completed = _read(config.state_root / 'completed.json', errors)
    today_completed = 0
    for item in completed.values():
        try:
            date = datetime.fromtimestamp(item['capture_completed_at']).astimezone().date().isoformat()
            today_completed += date == today
        except (KeyError, TypeError, ValueError, OverflowError, OSError):
            continue
    pending, partial, verified, imports = [], [], [], []
    target = target_id(config)
    for path in config.spool_root.glob('*.json'):
        item = _read(path, errors)
        if (item.get('account') == config.account and item.get('target_id') == target and not item.get('capture_only')):
            imports.append(item)
            if item.get('status') not in FINAL:
                pending.append(item)
            else:
                verified.append(item)
            if item.get('status') in FINAL and item.get('result', {}).get('omissions'):
                partial.append(item)
    stage = status.get('status', 'not_started')
    if stage == 'capturing' and checkpoint.get('stage'):
        stage = checkpoint['stage']
    if directory and (directory / 'capture-complete.json').exists() and active:
        stage = 'Post-activity processing' if not (directory / 'post-activity.json').exists() else 'Saving capture'
    if stale_status:
        stage = 'starting'
    if not stale_status and checkpoint.get('stage') == 'activity':
        blocker = checkpoint.get('pending_capture_blocker')
        failure = checkpoint.get('pending_browser_error')
        if blocker:
            stage = 'Waiting for capture recovery'
            errors.append('Capture: ' + blocker['error'])
        elif failure:
            errors.append('Capture: ' + failure['error'])
    if not stale_status and status.get('status') in ('recovering', 'waiting_for_solver_dependency') and status.get('error_type'):
        errors.append(str(status.get('detail') or status['error_type']))
    if directory:
        try:
            with (directory / 'activity-events.jsonl').open('rb') as events:
                events.seek(0, 2)
                events.seek(max(0, events.tell() - 8192))
                event = json.loads(events.read().splitlines()[-1])
            if event.get('error'):
                errors.append('Capture: ' + _error(event['error']))
        except (OSError, ValueError, IndexError, UnicodeError):
            pass
    if worker.get('error'):
        errors.append(_error(worker['error']))
    elif worker.get('exit_code'):
        errors.append('Worker exited with code ' + str(worker['exit_code']))
    for item in sorted(pending, key=lambda value: value.get('last_attempt_at', 0), reverse=True):
        if item.get('error') or item.get('result', {}).get('reason'):
            errors.append('Import: ' + (_error(item['error']) if item.get('error') else item['result']['reason']))
            break
    course_id = current_course(config).get('course_id') or config.course_id
    integrity = capture_integrity(imports)
    if integrity['capture_gap_activities']:
        errors.append(f"Capture gaps: {integrity['capture_gap_items']} items in {integrity['capture_gap_activities']} activities")
    progress_health = _read(config.state_root / 'progress-health.json', errors).get(str(course_id), {})
    progress_warning = progress_health.get('warning')
    if progress_warning:
        errors.append(progress_warning)
    metrics = output_metrics(config, completed, today, course_id) if details else {}
    logs, log_updated_at = log_tail(worker.get('log') or config.state_root / 'console.log') if details else ([], None)
    return {**metrics, **integrity, 'progress_warning': progress_warning,
            'database_questions': question_yield(verified, today) if details else {},
            'log_lines': logs, 'log_path': str(worker.get('log') or config.state_root / 'console.log'),
            'log_age': max(0, int(time.time() - log_updated_at)) if log_updated_at else None,
            'account': config.account, 'label': course_label(config), 'course_id': course_id,
            'original_course_code': ORIGINAL_COURSE_CODES.get(config.account),
            'answer_profile': account_profile(config),
            'running': is_running, 'status': 'RUNNING' if is_running else 'STOPPED',
            'pid': worker.get('pid'), 'uptime': max(0, int(time.time() - started))
                if is_running and isinstance(started, (int, float)) else None,
            'task_id': activity.get('task_id') or status.get('task_id'),
            'kind': activity.get('kind') or status.get('kind'), 'title': activity.get('title', ''),
            'stage': STAGES.get(stage, stage.replace('_', ' ').capitalize()),
            'today_xp': daily.get('earned_xp'), 'xp_unknown_tasks': daily.get('unknown_tasks', 0),
            'today_completed': today_completed, 'pending_imports': len(pending),
            'captures_with_omissions': len(partial),
            'errors': list(dict.fromkeys(error for error in errors if error)),
            'updated_at': status.get('at'), 'capture_only': config.capture_only}


def _text(value):
    # Source titles and error messages must not inject terminal escape sequences.
    value = re.sub(r'\x1b\][^\x07]*(?:\x07|\x1b\\)|\x1b\[[0-?]*[ -/]*[@-~]', '', str(value))
    return ''.join(char if char.isprintable() else ' ' for char in value).strip()


def _width(value):
    return sum(0 if unicodedata.combining(c) else 2 if unicodedata.east_asian_width(c) in ('W', 'F') else 1 for c in value)


def _fit(value, width):
    value = _text(value)
    if _width(value) > width:
        clipped = ''
        for char in value:
            if _width(clipped + char) > width - 1:
                break
            clipped += char
        value = clipped + '…'
    return value + ' ' * max(0, width - _width(value))


def xp_bars(activities, length=20):
    values = [number(a.get('earned_xp')) for a in activities[-length:]]
    scale = max([v for v in values if v is not None] + [1])
    shades = '▁▂▃▄▅▆▇█'
    chart = ''.join('?' if value is None else '↓' if value < 0 else '·' if value == 0 else
                    shades[min(7, max(0, math.ceil(value / scale * 8) - 1))] for value in values)
    return chart.rjust(length), scale


def course_title(row, width):
    name = _text(row.get('label') or row.get('account') or 'Account')
    code = _text(row.get('original_course_code') or ORIGINAL_COURSE_CODES.get(row.get('account'), '')).upper()
    suffix = f' ({code})' if code else ''
    if _width(name + suffix) <= width:
        return name + suffix
    # Preserve the identifying ending; shorten the opening of long titles.
    physical = re.search(r'Physical Sciences [IV]+$', name)
    tail = physical[0] if physical else ' '.join(name.split()[-2:])
    if _width(tail + suffix) + 5 > width:
        tail = name.split()[-1]
    if _width(tail + suffix) + 3 > width:
        return _fit(name, max(1, width - _width(suffix))).rstrip() + suffix
    head = _fit(name, width - _width(tail + suffix) - 1).rstrip()
    return head + ' ' + tail + suffix


def _metrics(row, inner):
    percent = number(row.get('percent_complete'))
    progress = '—%' if percent is None else f'{percent:g}%'
    if row.get('progress_warning'):
        progress += ' ?'
    elif inner >= 55:
        filled = 0 if percent is None else max(0, min(8, int(percent * 8 / 100)))
        progress = '█' * filled + '░' * (8 - filled) + ' ' + progress
    profile = f'Profile {row.get("answer_profile", "capture")} · Course {progress}'
    earned, base = number(row.get('today_xp')), number(row.get('today_base_xp'))
    points = '—' if earned is None and base is None else f'{earned:g}' if earned is not None else '—'
    if base is not None:
        points += f'/{base:g}'
    elif earned is not None:
        points += '/—'
    if row.get('xp_unknown_tasks') or row.get('base_xp_unknown_tasks'):
        points += '*'
    daily = f'Today {points} XP · Done {row.get("today_completed", 0)}'
    counts = row.get('activity_counts', {})
    mix = ' '.join(f'{label}{counts.get(kind, 0)}' for label, kind in
                   [('L', 'lesson'), ('R', 'review'), ('Q', 'assessment'), ('M', 'multistep'), ('D', 'diagnostic')])
    db = row.get('database_questions', {})
    suffix = '*' if db.get('unknown_imports') else ''
    yield_line = f'DB +{db.get("added", 0)} new / {db.get("existing", 0)} existing{suffix}'
    backlog = f'Pending imports {row.get("pending_imports", 0)} · Gaps {row.get("capture_gap_items", 0)}'
    if row.get('preserved_corrections'):
        backlog += f' · Protected {row["preserved_corrections"]}'
    if inner < 55:
        yield_line += f' · P{row.get("pending_imports", 0)} G{row.get("capture_gap_items", 0)}'
    chart, scale = xp_bars(row.get('recent_activities', []))
    recent = f'Last 20 {chart} 0–{scale:g} XP'
    task = ' '.join(str(v) for v in (str(row.get('kind') or '').capitalize(), row.get('task_id')) if v)
    phase = ' · '.join(v for v in (task, str(row.get('stage') or '')) if v) or 'No activity yet'
    result = [profile, daily, mix, yield_line]
    if inner >= 55:
        result.append(backlog)
    result.extend([recent, phase, row.get('title') or '—'])
    result.append('Error: ' + ' | '.join(row['errors']) if row.get('errors') else '')
    return result


def render(rows, compact=False, color=False, *, include_logs=False, width=None, height=None):
    rows = list(rows)
    running = sum(bool(row.get('running')) for row in rows)
    pending = sum(row.get('pending_imports', 0) for row in rows)
    if compact:
        return f'MA {running}/{len(rows)} running · {pending} imports pending'
    size = shutil.get_terminal_size()
    width = max(40, width if width is not None else size.columns)
    height = max(12, height if height is not None else size.lines)
    stamp = datetime.now().astimezone().strftime('%H:%M:%S %Z')
    heading = f' MATH ACADEMY · {running}/{len(rows)} running · {pending} imports '
    lines = [_fit(heading + ' ' * max(1, width - _width(heading) - len(stamp)) + stamp, width)]

    def card(row, card_width, panel_height=None):
        inner = card_width - 4
        def line(text):
            return '│ ' + _fit(text, inner) + ' │'
        state = row.get('status', 'STOPPED')
        available = max(5, inner - _width(state) - 2)
        marker = '● ' if row.get('running') else '○ '
        physical = re.search(r'Physical Sciences [IV]+$', _text(row.get('label', '')))
        code = row.get('original_course_code') or ORIGINAL_COURSE_CODES.get(row.get('account'))
        separate_state = physical and _width(physical[0]) + (len(code) + 3 if code else 0) + 5 > available - 2
        label = marker + course_title(row, (inner if separate_state else available) - 2)
        first = label + ' ' * max(2, inner - _width(label) - _width(state)) + state
        header = [state, label] if separate_state else [first]
        body = _metrics(row, inner)
        if include_logs:
            capacity = max(3, panel_height - 2 - len(header))
            # Keep the primary metrics and any blocker visible on small screens.
            metric_budget = max(2, capacity - 2)
            if len(body) > metric_budget:
                primary = body[:5] if inner < 55 else body[:6]
                task = ' '.join(str(v) for v in (str(row.get('kind') or '').capitalize(), row.get('task_id')) if v)
                tail = ('Error: ' + ' | '.join(row['errors'])) if row.get('errors') else ' · '.join(v for v in (task, row.get('stage')) if v)
                body = (primary + [tail])[:metric_budget - 1] + [tail]
            available = capacity - len(body) - 1
            age = row.get('log_age')
            log_label = ' Logs' + (f' · last write {age}s ago' if age is not None else '')
            body.append(log_label)
            logs = []
            for raw in row.get('log_lines', []):
                text = re.sub(r'^\d{4}-\d\d-\d\d ', '', _text(raw))
                text = re.sub(r'^(\d\d:\d\d:\d\d),\d+ ', r'\1 ', text)
                logs.extend(('› ' if i == 0 else '↳ ') + part for i, part in enumerate(
                    textwrap.wrap(text, max(8, inner - 2), break_long_words=True, break_on_hyphens=False) or ['']))
            logs = logs[-available:] if available > 0 else []
            if available and not logs:
                logs = ['› No log messages yet']
            body += [''] * max(0, available - len(logs)) + logs
            body = body[:capacity]
        result = ['╭' + '─' * (card_width - 2) + '╮', *map(line, header), *map(line, body),
                  '╰' + '─' * (card_width - 2) + '╯']
        return result

    columns = 2 if len(rows) > 1 and (width >= 120 or (width >= 80 and (not include_logs or height < len(rows) * 13 + 2))) else 1
    widths = [(width - 1) // 2, width // 2] if columns == 2 else [width]
    groups = max(1, math.ceil(len(rows) / columns))
    panel_height = (height - 2) // groups if include_logs else None
    if include_logs and panel_height < 8:
        for row in rows:
            status = f' · {row.get("status")} · {row.get("answer_profile", "capture")}'
            lines.append(_fit(course_title(row, width - _width(status)) + status, width))
            logs = row.get('log_lines') or ['No log messages yet']
            lines.append(_fit('› ' + _text(logs[-1]), width))
        lines.append(_fit(' Enlarge the terminal for full metrics and longer log tails · Ctrl+b d detach', width))
        return '\n'.join(lines[:height])
    for index in range(0, len(rows), columns):
        group = rows[index:index + columns]
        cards = [card(row, widths[column], panel_height) for column, row in enumerate(group)]
        tallest = max(len(c) for c in cards)
        cards = [c + [' ' * widths[i]] * (tallest - len(c)) for i, c in enumerate(cards)]
        lines.extend(_fit(' '.join(parts), width) for parts in zip(*cards))
    footer = ' L lesson R review Q assessment M multistep D diagnostic · XP oldest → newest · ↓ penalty · Ctrl+b d detach'
    if width < 110:
        footer = ' L/R/Q/M/D · XP oldest → newest · ↓ penalty · Ctrl+b d detach'
    if any(row.get('xp_unknown_tasks') or row.get('base_xp_unknown_tasks') or row.get('database_questions', {}).get('unknown_imports') for row in rows):
        footer = ' * partial/unknown totals ·' + footer
    lines.append(_fit(footer, width))
    if include_logs:
        lines = lines[:height]
    if color:
        lines = [text.replace('RUNNING', '\033[38;5;150mRUNNING\033[0m')
                     .replace('STOPPED', '\033[38;5;245mSTOPPED\033[0m')
                     .replace('Error:', '\033[38;5;221mError:\033[0m') for text in lines]
    return '\n'.join(lines)
