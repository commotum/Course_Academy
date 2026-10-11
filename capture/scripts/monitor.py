"""Read-only account cards from capture checkpoints and supervisor records."""
from datetime import datetime
import json
from pathlib import Path
import shutil
import time

from .outbox import FINAL, target_id
from .courses import course_label, current_course
from .storage import read_json

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


def snapshot(config, running=None):
    errors = []
    worker = _read(config.state_root / 'worker.json', errors)
    status = _read(config.state_root / 'status.json', errors)
    is_running = process_running(worker) if running is None else bool(running)
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
    pending = []
    target = target_id(config)
    for path in config.spool_root.glob('*.json'):
        item = _read(path, errors)
        if (item.get('account') == config.account and item.get('target_id') == target
                and item.get('status') not in FINAL and not item.get('capture_only')):
            pending.append(item)
    stage = status.get('status', 'not_started')
    if stage == 'capturing' and checkpoint.get('stage'):
        stage = checkpoint['stage']
    if directory and (directory / 'capture-complete.json').exists() and active:
        stage = 'Post-activity processing' if not (directory / 'post-activity.json').exists() else 'Saving capture'
    if stale_status:
        stage = 'starting'
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
        if item.get('error'):
            errors.append('Import: ' + _error(item['error']))
            break
    return {'account': config.account, 'label': course_label(config), 'course_id': current_course(config).get('course_id'),
            'running': is_running, 'status': 'RUNNING' if is_running else 'STOPPED',
            'pid': worker.get('pid'), 'uptime': max(0, int(time.time() - started))
                if is_running and isinstance(started, (int, float)) else None,
            'task_id': activity.get('task_id') or status.get('task_id'),
            'kind': activity.get('kind') or status.get('kind'), 'title': activity.get('title', ''),
            'stage': STAGES.get(stage, stage.replace('_', ' ').capitalize()),
            'today_xp': daily.get('earned_xp'), 'xp_unknown_tasks': daily.get('unknown_tasks', 0),
            'today_completed': today_completed, 'pending_imports': len(pending),
            'errors': list(dict.fromkeys(error for error in errors if error)),
            'updated_at': status.get('at'), 'capture_only': config.capture_only}


def _text(value):
    # Source titles and error messages must not inject terminal escape sequences.
    return ''.join(char if char.isprintable() else ' ' for char in str(value)).strip()


def render(rows, compact=False, color=False):
    rows = list(rows)
    running = sum(bool(row.get('running')) for row in rows)
    pending = sum(row.get('pending_imports', 0) for row in rows)
    if compact:
        return f'MA {running}/{len(rows)} running · {pending} imports pending'
    width = max(60, min(shutil.get_terminal_size().columns, 150))
    stamp = datetime.now().astimezone().strftime('%H:%M:%S %Z')
    heading = f' MATH ACADEMY · {running}/{len(rows)} running '
    lines = [(heading + ' ' * max(1, width - len(heading) - len(stamp)) + stamp)[:width].ljust(width)]

    def contents(row):
        xp = row.get('today_xp')
        xp = f'{xp:g}' if isinstance(xp, (int, float)) else '—'
        if row.get('xp_unknown_tasks'):
            xp += '*'
        task = ' '.join(str(value) for value in (row.get('kind', '').capitalize() if row.get('kind') else None,
                                                 row.get('task_id')) if value)
        result = [f'Today {xp} XP · Done {row.get("today_completed", 0)} · Imports {row.get("pending_imports", 0)}',
                  ' · '.join(str(value) for value in (task, row.get('stage')) if value) or 'No activity yet',
                  row.get('title') or '—']
        if row.get('errors'):
            result.append('Error: ' + ' | '.join(row['errors']))
        return result

    def card(row, card_width, height):
        inner = card_width - 4
        def line(text):
            text = _text(text)
            if len(text) > inner:
                text = text[:inner - 1] + '…'
            return '│ ' + text.ljust(inner) + ' │'
        label = ('● ' if row.get('running') else '○ ') + _text(row.get('label', row.get('account', 'Account')))
        state = row.get('status', 'STOPPED')
        available = max(5, inner - len(state) - 2)
        if len(label) > available:
            tail = min(12, available // 2)
            label = label[:available - tail - 1] + '…' + label[-tail:]
        first = label + ' ' * max(2, inner - len(label) - len(state)) + state
        body = contents(row)
        body += [''] * (height - len(body))
        return ['╭' + '─' * (card_width - 2) + '╮', line(first), *map(line, body),
                '╰' + '─' * (card_width - 2) + '╯']

    columns = 2 if width >= 80 else 1
    widths = [(width - 1) // 2, width // 2] if columns == 2 else [width]
    for index in range(0, len(rows), columns):
        group = rows[index:index + columns]
        height = max(len(contents(row)) for row in group)
        cards = [card(row, widths[column], height) for column, row in enumerate(group)]
        lines.extend(' '.join(parts).ljust(width) for parts in zip(*cards))
    footer = ' Checkpoints retained · Ctrl+b d detach'
    if any(row.get('xp_unknown_tasks') for row in rows):
        footer += ' · XP* = partial total'
    lines.append(footer[:width].ljust(width))
    if color:
        lines = [text.replace('RUNNING', '\033[38;5;150mRUNNING\033[0m')
                     .replace('STOPPED', '\033[38;5;245mSTOPPED\033[0m')
                     .replace('Error:', '\033[38;5;221mError:\033[0m') for text in lines]
    return '\n'.join(lines)
