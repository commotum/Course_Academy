"""Summarize only completed, normally verified finite archive repairs."""
from pathlib import Path
import hashlib, json, time
from scripts.storage import atomic_json, read_json
from scripts.browser.adapter import EXTRACT
from scripts.database.text import markdown

ROOT = Path(__file__).resolve().parent
summary = read_json(ROOT/'later-verified-repairs.json')
assert summary['captures'] == summary['verified'] == summary['zero_omission_captures'] == 43
assert summary['omissions'] == 0
manifest = read_json(ROOT/'reviewed21-apply-manifest.json')
applied = read_json(ROOT/'later-repair-run-reviewed21.json')
assert len(applied) == 21 and all(r['status']=='verified' and not r['omissions'] for r in applied)
for entry in manifest['entries']:
    for name, digest in entry['protected_files'].items():
        assert hashlib.sha256(Path(name).read_bytes()).hexdigest() == digest, name
values = read_json(ROOT/'final-archive-authored-pinned-values.json')
assert values['all_values_match']
ordered = read_json(ROOT/'later-ordered-list-extraction-comparison.json')
assert len(ordered['records']) == 100 and all(r['matches'] for r in ordered['records'])
tables = read_json(ROOT/'later-complex-table-pinned-readbacks.json')
assert len(tables['records']) == 4 and all(all(v['matches'] for v in r['values'].values()) for r in tables['records'])
attribution = read_json(ROOT/'later-attribution-receipt-audit.json')
assert not attribution['errors'] and not attribution['collisions'] and attribution['non_ma_retractions'] == 0
ownership = read_json(ROOT/'later-choice-ownership-final-native-audit.json')
assert all(r['no_response_owner_before'] and r['answer_entity_preserved'] for r in ownership['checks'])

original_ids = {Path(r['directory']).parents[1].name for r in read_json(ROOT/'later-source-candidates.json')} | {'14120884'}
additional_ids = {'14121715','14121869','14121047'}
groups = [('original36', original_ids), ('additional3', additional_ids),
          ('frozen318', {r['task_id'] for r in summary['results']} - original_ids - additional_ids)]
for name, ids in groups:
    rows = [r for r in summary['results'] if r['task_id'] in ids]
    counts = {'questions': [], 'canonical_examples': []}
    generations = []
    for row in rows:
        assert row['normal_reimport_is_noop'] and row['pinned_readback']['supported_records_present'], row['task_id']
        assert all(row['preservation'].values()), row['task_id']
        outbox = row['completed_package_outbox']
        assert outbox['capture_directory_matches'] and outbox['omissions_match_current_database'] and not outbox['omissions']
        assert outbox['terminal_status'] in ('verified','no_changes')
        content = read_json(Path(row['directory'])/'content.json')
        hashes = {}
        for bucket in counts:
            for record in content.get(bucket, []):
                counts[bucket].append(record['math_academy_id'])
                digest = record.get('recovery', {}).get('extractor_sha256', 'not-recorded')
                hashes[digest] = hashes.get(digest, 0) + 1
        generations.append({'task_id': row['task_id'], 'recorded_extractor_sha256_counts': hashes,
                            'repair': row['repair'], 'review_version': row.get('version')})
    output = {'created_at': time.time(), 'captures': len(rows), 'verified': len(rows), 'omissions': 0,
              'source_record_counts': {'unique_questions':len(set(counts['questions'])), 'question_occurrences':len(counts['questions']),
                                       'unique_examples':len(set(counts['canonical_examples'])), 'example_occurrences':len(counts['canonical_examples'])},
              'normal_reimport_noop': True, 'all_preservation_assertions_pass': True,
              'all_accepted_records_pinned_present_with_matching_field_count': True,
              'current_extractor_sha256': hashlib.sha256(EXTRACT.encode()).hexdigest(),
              'current_text_sha256': hashlib.sha256(Path(markdown.__code__.co_filename).read_bytes()).hexdigest(),
              'actual_reviewed_generations': generations, 'results': rows,
              'final21_authored_value_audit': 'final-archive-authored-pinned-values.json',
              'exact_source_equivalence': manifest['equivalence_certificate'],
              'native_choice_ownership_audit':'later-choice-ownership-final-native-audit.json'}
    atomic_json(ROOT/(name+'-final-verification.json'), output)
    print(json.dumps({'group': name, 'captures': len(rows), **output['source_record_counts']}))
