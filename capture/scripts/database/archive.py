"""Compact completed batch records; retain live import snapshots unchanged."""
from __future__ import annotations

import copy
import hashlib
import json
import os
from pathlib import Path

from ..storage import atomic_bytes, read_json

FORMAT = 'completed-batch-record-v1'
FINAL = {'verified', 'no_changes'}


def content_digest(value):
    # Matches database.prepare.digest without importing the preparation pipeline.
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False, default=str).encode()).hexdigest()


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + '\n').encode()


def expand_record(directory, record):
    """Restore the completed result without reopening or replaying capture content."""
    directory = Path(directory)
    if record.get('archive_format') != FORMAT or record.get('status') not in FINAL:
        raise ValueError('Unsupported or unfinished compact batch record')
    members, activities = [], {}
    receipts = record['receipts']
    for descriptor in record['parts']:
        name = descriptor['path']
        if Path(name).name != name:
            raise ValueError('Batch part must be a filename in the batch directory')
        data = (directory / name).read_bytes()
        if hashlib.sha256(data).hexdigest() != descriptor['sha256']:
            raise ValueError(f'Batch part checksum mismatch: {name}')
        part = json.loads(data)
        if len(part['members']) != descriptor['members']:
            raise ValueError(f'Batch part member count mismatch: {name}')
        for entry in part['members']:
            member = copy.deepcopy(entry['member'])
            capture_directory = member['directory']
            if capture_directory in activities:
                raise ValueError('Duplicate activity in compact batch record')
            outcome = copy.deepcopy(entry['result'])
            outcome.update(receipts=[copy.deepcopy(receipts[i]) for i in entry['receipt_indices']],
                           batch_directory=record['result']['batch_directory'],
                           batch_activities=record['member_count'], content_sha256=member['content_sha256'])
            activities[capture_directory] = outcome
            members.append(member)
    if len(members) != record['member_count']:
        raise ValueError('Compact batch record is incomplete')
    result = copy.deepcopy(record['result'])
    result['activities'] = activities
    return {**record, 'members': members,
            'source_repairs': {m['directory']: copy.deepcopy(record.get('source_repairs', {}).get(m['directory'], []))
                               for m in members}, 'result': result}


def read_manifest(path):
    manifest = read_json(path)
    if manifest and 'archive_format' in manifest:
        return expand_record(Path(path).parent, manifest)
    return manifest


def compact_completed_batch(directory):
    """Deduplicate one verified archive and split its members into two equal groups."""
    directory = Path(directory).resolve()
    path = directory / 'manifest.json'
    original_bytes = path.read_bytes()
    manifest = json.loads(original_bytes)
    if manifest.get('archive_format') == FORMAT:
        expand_record(directory, manifest)
        return {'directory': str(directory), 'already_compact': True}
    if manifest.get('status') not in FINAL or manifest.get('result', {}).get('status') != manifest['status']:
        raise ValueError('Only completed batch records may be compacted')
    if (directory / 'request.json').exists():
        raise ValueError('Batch still has a pending exact request')
    active = read_json(directory.parent / 'active.json', {})
    if active.get('directory') and Path(active['directory']).resolve() == directory:
        raise ValueError('Batch is still active')
    verification = read_json(directory / 'verification.json', {})
    if manifest['status'] == 'verified' and (verification.get('status') != 'verified'
                                           or verification.get('reimport_is_noop') is not True):
        raise ValueError('Batch verification must confirm that reimport is a no-op')
    previous_path = path.with_name(path.name + '.previous')
    previous_bytes = previous_path.read_bytes() if previous_path.exists() else None
    if previous_bytes is not None:
        previous = json.loads(previous_bytes)
        without_completion = lambda value: {k: v for k, v in value.items() if k not in {'status', 'result'}}
        if without_completion(previous) != without_completion(manifest):
            raise ValueError('Previous manifest contains distinct capture data; preserve it separately')
        if 'result' in previous and previous['result'] != manifest['result']:
            raise ValueError('Previous manifest contains a distinct result; preserve it separately')
    members = manifest['members']
    if len(members) < 2:
        raise ValueError('At least two activities are required for a two-part record')
    if set(manifest['result']['activities']) != {m['directory'] for m in members}:
        raise ValueError('Completed outcomes do not match batch membership')
    receipts, entries = [], []
    for member in members:
        source_path = Path(member['directory']) / 'content.json'
        source = json.loads(source_path.read_text())
        if source != member['content']:
            raise ValueError(f'Capture differs from archived snapshot; cannot discard it: {source_path}')
        outcome = copy.deepcopy(manifest['result']['activities'][member['directory']])
        sha = content_digest(member['content'])
        if outcome.get('content_sha256') != sha:
            raise ValueError(f'Imported content hash mismatch: {source_path}')
        if outcome.get('batch_directory') != manifest['result']['batch_directory'] or outcome.get('batch_activities') != len(members):
            raise ValueError('Activity has distinct batch metadata; retain the full record')
        receipt_indices = []
        for receipt in outcome.pop('receipts'):
            if receipt not in receipts:
                receipts.append(receipt)
            receipt_indices.append(receipts.index(receipt))
        for key in ('batch_directory', 'batch_activities', 'content_sha256'):
            outcome.pop(key)
        reference = {k: v for k, v in member.items() if k != 'content'}
        reference.update(content_ref=os.path.relpath(source_path, directory), content_sha256=sha)
        entries.append({'member': reference, 'result': outcome, 'receipt_indices': receipt_indices})
    record = {k: v for k, v in manifest.items() if k not in {'members', 'result', 'source_repairs'}}
    record.update(archive_format=FORMAT, member_count=len(members), receipts=receipts,
                  result={k: v for k, v in manifest['result'].items() if k != 'activities'}, parts=[])
    repairs = {k: v for k, v in manifest.get('source_repairs', {}).items() if v}
    if repairs:
        record['source_repairs'] = repairs
    middle = (len(entries) + 1) // 2
    part_data = []
    for number, group in enumerate((entries[:middle], entries[middle:]), 1):
        name = f'manifest.part-{number}.json'
        data = encoded({'members': group})
        if len(data) >= 64 * 1024**2:
            raise ValueError('Compact part is still too large for the default push chunk')
        existing = directory / name
        if existing.exists() and existing.read_bytes() != data:
            raise ValueError(f'Refusing to replace a distinct existing part: {existing}')
        part_data.append((existing, data))
        record['parts'].append({'path': name, 'sha256': hashlib.sha256(data).hexdigest(), 'members': len(group)})
    for part_path, data in part_data:
        atomic_bytes(part_path, data)
    expanded = expand_record(directory, record)
    if expanded['result'] != manifest['result'] or expanded['source_repairs'] != manifest['source_repairs']:
        raise ValueError('Compact record does not preserve the original completed result')
    # Publish the index only after both parts are complete and validated.
    # Avoid atomic_json here: it would recreate the oversized .previous copy.
    if path.read_bytes() != original_bytes or (directory / 'request.json').exists():
        raise ValueError('Batch changed while compacting; original manifest preserved')
    active = read_json(directory.parent / 'active.json', {})
    if active.get('directory') and Path(active['directory']).resolve() == directory:
        raise ValueError('Batch became active while compacting; original manifest preserved')
    atomic_bytes(path, encoded(record))
    if previous_bytes is not None:
        if previous_path.read_bytes() != previous_bytes:
            raise ValueError('Previous backup changed; leaving it in place')
        previous_path.unlink()
    return {'directory': str(directory), 'members': len(members),
            'before_bytes': len(original_bytes) + len(previous_bytes or b''),
            'after_bytes': path.stat().st_size + sum(len(data) for _, data in part_data),
            'parts': [{'path': str(p), 'bytes': len(data)} for p, data in part_data]}
