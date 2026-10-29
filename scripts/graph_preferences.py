"""Shared graph display settings, stored in a local JSON file outside EDB."""
import fcntl
import json
from pathlib import Path


DEFAULTS = {
    'colorCode': True,
    'courses': ['255', '256', '341'],
    'includeQueue': True,
    'splitByCourse': False,
    'weeks': {'kind': 'all'},
}


def validate(changes):
    if not isinstance(changes, dict) or changes.keys() - DEFAULTS.keys():
        raise ValueError('Unknown graph display setting')
    for key, value in changes.items():
        if key in {'colorCode', 'includeQueue', 'splitByCourse'}:
            if type(value) is not bool:
                raise ValueError(f'{key} must be a boolean')
        elif key == 'courses':
            if not isinstance(value, list) or any(code not in DEFAULTS['courses'] for code in value):
                raise ValueError('Invalid graph course filter')
            changes = {**changes, key: sorted(set(value))}
        elif key == 'weeks':
            if not isinstance(value, dict):
                raise ValueError('Invalid graph week filter')
            if value.get('kind') in ('all', 'unscheduled') and set(value) == {'kind'}:
                continue
            if (set(value) != {'kind', 'start', 'end', 'anchor'} or value.get('kind') != 'range'
                    or any(type(value[name]) is not int or abs(value[name]) > 1_000_000 for name in ('start', 'end', 'anchor'))
                    or not value['start'] <= value['anchor'] <= value['end']):
                raise ValueError('Invalid graph week range')
    return changes


def read_preferences(path):
    try:
        saved = validate(json.loads(Path(path).read_text()))
    except FileNotFoundError:
        saved = {}
    return {**DEFAULTS, **saved}


def update_preferences(path, changes, save):
    changes = validate(changes)
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    # A separate lock keeps cosmetic changes independent of database writes.
    with path.with_suffix('.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        value = {**read_preferences(path), **changes}
        save(path, value)
        return value
