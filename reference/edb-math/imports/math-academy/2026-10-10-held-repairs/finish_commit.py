"""Publish verified completion metadata; contains no transaction operation."""
from datetime import datetime, timezone
from pathlib import Path
from prepare import ROOT, INDEX, read, sha, loads, Database, arguments
from core import atomic_json

manifest_path = ROOT / 'manifest.json'
m = read(manifest_path)
commits = read(ROOT / 'commit-verification.json')
audit = loads((ROOT / 'committed-history-verification/manifest.edn').read_text())
assert commits['all_stages_committed'] and len(commits['stages']) == 2
assert audit[':audit/verified'] and audit[':audit/committed-receipts-verified']
assert audit[':audit/originals-recovered-from-final-history']
before, after = commits['basis_before'], commits['basis_after']
assert audit[':audit/durable-basis-before'] == before
assert audit[':audit/durable-basis-after'] == after == before + 2
assert audit[':audit/question-count'] == 26
assert audit[':audit/retired-components'] == 12
db = Database(arguments(['run']))
assert db.args.database == 'math' and db.basis() == after
ids = sorted(read(ROOT / 'original-content.json'))
for stage in commits['stages']:
    directory = ROOT / 'commits' / ('stage-' + str(stage['stage']))
    assert read(directory / 'verification.json') == stage
    check = read(directory / 'readback/verification.json')
    assert check['verified'] and check['basis'] == stage['basis_after']
    assert sorted(q['id'] for q in check['questions']) == ids
    for q in check['questions']:
        assert all(q[k] for k in ['content', 'fields', 'source', 'knowledge_point', 'reimport_noop'])
for stage in m['stages']:
    assert sha(stage['ssd_file']) == sha(stage['reference_file']) == stage['sha256']

verification = {'verified': True, 'database': 'math', 'basis_before': before,
    'basis_after': after, 'questions_verified': 26, 'answer_fields_verified': 26,
    'original_stage_new_questions': 23, 'original_stage_existing_questions': 3,
    'stages': commits['stages'], 'question_identities_preserved': True,
    'knowledge_point_membership_verified': True, 'source_attribution_verified': True,
    'exact_retractions_verified': 92, 'both_receipts_verified_in_durable_history': True,
    'all_originals_recovered_from_final_as_of_stage1': True,
    'original_components_in_history': 174, 'retired_components': 12,
    'unaffected_original_components': 162, 'external_incoming_references_removed': 0,
    'repaired_content_reimport_is_noop': True,
    'history_audit': str(ROOT / 'committed-history-verification/manifest.edn')}
atomic_json(ROOT / 'committed-content-verification.json', verification)

index = read(INDEX)
assert sha(INDEX) == m['held_index_sha256'] or index.get('resolved_by_held_repairs', {}).get('basis_after') == after
if not index.get('resolved_by_held_repairs'):
    assert {q['math_academy_id'] for q in index['questions']} == set(ids)
    (ROOT / 'held-index-before-commit.json').write_bytes(INDEX.read_bytes())
    index['questions'] = [q for q in index['questions'] if q['math_academy_id'] not in ids]
    assert not index['questions']
    index['counts'].update(previous_held_remaining=0, latest_held=0, overlap_remaining=0,
        latest_only=0, unique_held_questions=0, resolved_by_held_repairs=26)
    index['database_basis_reviewed'] = after
    index['updated_at'] = datetime.now(timezone.utc).isoformat()
    index['resolved_by_held_repairs'] = {'basis_before': before, 'basis_after': after,
        'sources': [s['source'] for s in commits['stages']], 'question_ids': ids,
        'manifest': str(manifest_path), 'verification': str(ROOT / 'committed-content-verification.json')}
    index['remaining_content_reason_counts'] = {}
    index['remaining_pattern_counts'] = {key: 0 for key in index['remaining_pattern_counts']}
    index['remaining_pattern_counts_note'] = 'No held questions remain after verified original-content and repair commits.'
    index['remaining_analysis'] = {'basis': after, 'questions': str(ROOT / 'remaining-questions.json'),
        'summary': str(ROOT / 'remaining-summary.json'), 'note': 'Current held index is empty. Earlier analyses remain historical evidence.'}
    index['status_note'] = ('All held questions are resolved. The final 26 originals and separately attributed Astra/ultra repairs '
        f'were committed at bases {before + 1} and {after}, then verified against durable current state and history.')
    atomic_json(INDEX, index)
atomic_json(ROOT / 'remaining-questions.json', {})
atomic_json(ROOT / 'remaining-summary.json', {'basis': after, 'held': 0, 'content_reason_counts': {},
    'final_batch_questions_resolved': 26, 'committed_and_verified': True})
atomic_json(ROOT / 'held-index-update-verification.json', {'verified': True, 'basis': after,
    'before': 26, 'removed_verified_ids': ids, 'remaining': 0, 'index_sha256': sha(INDEX)})

if not (ROOT / 'manifest-before-commit.json').exists():
    (ROOT / 'manifest-before-commit.json').write_bytes(manifest_path.read_bytes())
m.update(transacted=True, verified=True, database_writes=2, basis_revalidated_against=before,
    basis_before_commit=before, basis_after=after, held_index_unchanged_during_preparation=True,
    held_index_updated_after_verified_commit=True, held_index_remaining=0,
    held_index_sha256_after_commit=sha(INDEX),
    committed_content_verification=str(ROOT / 'committed-content-verification.json'),
    commit_note='Both exact prepared EDNs committed under their separate sources; durable readbacks and history verified before held-index removal.',
    submission_note='Already committed and verified. Do not resubmit as new transactions. Preserve saved request keys for exact receipt recovery.',
    preview_note='Original preparation at187 and precommit validation at%d were speculative; actual commits advanced%d through%d to%d.' % (before, before, before+1, after))
m.pop('held_index_unchanged', None)
for stage, committed in zip(m['stages'], commits['stages']):
    stage.update(transacted=True, verified=True, committed_basis_before=committed['basis_before'],
        committed_basis_after=committed['basis_after'], committed_datoms=committed['datoms'],
        commit_receipt=str(ROOT / 'commits' / ('stage-' + str(stage['stage'])) / 'commit.edn'))
atomic_json(manifest_path, m)

report = ROOT / 'process-report.txt'
report_before = ROOT / 'process-report-before-commit.txt'
if not report_before.exists():
    report_before.write_bytes(report.read_bytes())
text = report_before.read_text()
title, date, rest = text.split('\n', 2)
update = (f'Completion update: After this preparation report was finished, the user authorized both commits. '
    f'The unchanged EDNs were revalidated against basis {before}, committed in order at bases {before+1} and {after}, '
    'and verified against durable current state and history. All 26 questions are now resolved and the held index is empty. '
    'The account below records the preparation process; references to uncommitted previews describe that earlier phase. '
    'committed-content-verification.json and commits/ contain the final evidence.')
report.write_text(title + '\n' + date + '\n\n' + update + '\n' + rest)
(ROOT / 'README-before-commit.txt').write_bytes((ROOT / 'README.txt').read_bytes()) if not (ROOT / 'README-before-commit.txt').exists() else None
(ROOT / 'README.txt').write_text(f'''TWO TRANSACTIONS COMMITTED AND VERIFIED

All 26 final held questions are resolved. The held index is empty.

1. 001-math-academy-original.edn
   Source :org/Math-Academy; durable basis {before} -> {before+1}.
   23 new questions and 3 existing updates; original captured content retained.

2. 002-astra-surgical-repairs.edn
   Source :agent/gpt-6-astra-ultra; durable basis {before+1} -> {after}.
   25 prompt edits, 11 solution edits, and 2 choice edits across the same26 questions.
   Two superseded fields and ten answers retracted and replaced; originals
   recovered from final durable history as of basis {before+1}.

Both receipts, every answer field, source attribution, exact retractions,
question UUIDs, knowledge-point membership, and historical recovery passed.
174 original component entities remain recoverable from history; 162 remain
unchanged in current state and 12 were retired. No external incoming refs were
removed. The held index was updated only after all durable verification passed.

The EDNs are already committed. Do not submit them again as new requests.
commits/ retains exact request keys, intents, receipts and per-stage readbacks.
committed-history-verification/ holds the independent durable history audit.
committed-content-verification.json and manifest.json summarize completion.
repair-diff.txt and process-report.txt explain the changes and workflow.

Original preparation was against basis187; unrelated later transactions
advanced the live basis to{before}. The scope and exact prepared EDNs remained
unchanged, and a fresh sequential preview passed before the authorized commits.
Historical preparation records remain intact in validation/ and the
*-before-commit files. The SSD directory contains transaction EDNs only.
'''.replace('same26', 'same 26').replace('basis187', 'basis 187').replace('to'+str(before), 'to '+str(before)))
assert not read(INDEX)['questions'] and db.basis() == after
print(f'COMMITTED AND VERIFIED: 26 resolved; 0 held; durable basis {after}.')
