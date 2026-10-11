"""Read-only audit using the legacy engine's own source-evidence policy."""
import collections, hashlib, json, sys, time
from pathlib import Path
ROOT = Path('/home/jake/Developer/Course_Academy')
sys.path.insert(0, str(ROOT / 'scripts/question_capture'))
from authoritative import prepare_authoritative_content

def read(path, default=None):
    return json.loads(path.read_text()) if path.is_file() else default

rows, reasons, origins, structural, asset_findings = [], collections.Counter(), collections.Counter(), [], []
asset_count, checked_assets = 0, set()
paths = sorted((ROOT / 'reference/mathacademy/question-capture').glob('[0-9]*/content.json'))
for index, path in enumerate(paths):
    directory = path.parent
    content = read(path)
    state = read(directory / 'state.json', {})
    row = {'task_id': directory.name, 'kind': content.get('task_type'), 'questions': len(content.get('questions', [])),
           'examples': len(content.get('canonical_examples', [])),
           'activity_complete': bool(state.get('activity_complete') or state.get('lesson_complete')),
           'history_complete': bool(state.get('history_complete')), 'import_complete': bool(state.get('import_complete'))}
    try:
        prepared, review = prepare_authoritative_content(content, directory, state=state)
        row.update(held=review['held_questions'], disagreements=review['disagreements'], observations=review['observations'],
                   prepared_questions=review['prepared_questions'], prepared_examples=review['prepared_canonical_examples'])
        reasons.update(reason.split(':')[0] for held in row['held'] for reason in held['reasons'])
    except Exception as error:
        row['checker_error'] = type(error).__name__ + ': ' + str(error)
    for bucket in ('questions', 'canonical_examples'):
        ids = []
        for q in content.get(bucket, []):
            identity = q.get('math_academy_id'); ids.append(identity)
            missing = []
            if not q.get('problem'): missing.append('problem')
            if not q.get('worked_solution'): missing.append('worked_solution')
            fields = q.get('answer_fields', [])
            if bucket == 'questions' and not fields: missing.append('answer_fields')
            keys = [f.get('key') for f in fields]
            if len(set(keys)) != len(keys): missing.append('duplicate_field_keys')
            for field in fields:
                origins[field.get('correct_origin', 'unspecified')] += 1
                if field.get('correct_value') is None: missing.append('correct_value')
                if field.get('type') in ('radio', 'select') and not field.get('choices'): missing.append('choices')
            if missing: structural.append({'task_id': directory.name, 'id': identity, 'bucket': bucket, 'missing': sorted(set(missing))})
        if len(set(ids)) != len(ids): structural.append({'task_id': directory.name, 'bucket': bucket, 'missing': ['duplicate_question_identity']})
    verification = read(directory / 'edb-import/verification.json', {})
    row['legacy_commit_verified'] = bool(verification.get('committed'))
    row['legacy_database_basis'] = verification.get('basis_after')
    manifest = read(directory / 'assets/manifest.json', {})
    for asset in manifest.values() if isinstance(manifest, dict) else manifest:
        if not isinstance(asset, dict): continue
        file = asset.get('path') or asset.get('stored_path'); digest = asset.get('sha256')
        if not file or not digest: continue
        if file in checked_assets: continue
        checked_assets.add(file); asset_count += 1
        p = Path(file)
        if not p.is_file(): asset_findings.append({'task_id': directory.name, 'path': file, 'reason': 'missing_original'})
        elif hashlib.sha256(p.read_bytes()).hexdigest() != digest: asset_findings.append({'task_id': directory.name, 'path': file, 'reason': 'hash_mismatch'})
    rows.append(row)
    if (index + 1) % 100 == 0: print('AUDITED', index + 1, 'of', len(paths), flush=True)
summary = {'captures': len(rows), 'questions': sum(r['questions'] for r in rows), 'examples': sum(r['examples'] for r in rows),
           'captures_with_held_source_records': sum(bool(r.get('held')) for r in rows),
           'held_practice_occurrences': sum(sum(not h['canonical'] for h in r.get('held', [])) for r in rows),
           'held_example_occurrences': sum(sum(h['canonical'] for h in r.get('held', [])) for r in rows),
           'checker_errors': sum('checker_error' in r for r in rows), 'held_reasons': dict(reasons),
           'field_origins': dict(origins), 'structural_findings': len(structural),
           'checked_manifest_assets': asset_count, 'asset_findings': len(asset_findings),
           'commits_with_local_verification': sum(r['legacy_commit_verified'] for r in rows),
           'completion_flags': {key: sum(r[key] for r in rows) for key in ('activity_complete', 'history_complete', 'import_complete')}}
result = {'audited_at': time.time(), 'scope': 'Every top-level numeric legacy task with content.json; nested repairs excluded',
          'method': 'Read-only prepare_authoritative_content, structural checks, and original manifest SHA-256 checks. Held means this strict source checker cannot confirm; it does not mean the mathematical answer is wrong or current database is missing it.',
          'summary': summary, 'captures': rows, 'structural_findings': structural, 'asset_findings': asset_findings}
Path('/tmp/legacy-capture-completeness.json').write_text(json.dumps(result, indent=2) + '\n')
print('SUMMARY', json.dumps(summary), flush=True)
