"""Verify preparation integrity and publish EDN files only; never transact."""
import collections
import difflib
import json
from pathlib import Path

from prepare import (ROOT, REPO, SNAP, TX, VALID, DEST, INDEX, SOURCE, REPAIR_SOURCE,
                     read, save, sha, loads, authors, snapshot, Database, arguments)

start, existing, topics = snapshot()
verification = read(ROOT / 'verification.json')
assert verification['valid'] and verification['database_writes'] == 0 and not verification['transacted']
proposals = authors()
assert proposals == read(ROOT / 'repair-plan.json'), 'Author files changed after assembly.'
peer_files = ['peer-review-multiple.json', 'peer-review-defects.json']
for name in peer_files:
    peer = read(ROOT / 'review' / name)
    assert peer.get('status', peer.get('overall_status')) == 'pass'
    assert peer['reviewer_model'] == 'gpt-6-astra' and peer['reasoning_effort'] == 'ultra'
    assert sha(peer['reviewed_file']) == peer.get('reviewed_file_sha256', peer.get('reviewed_sha256'))
assert sum(read(ROOT / 'review' / f)['question_count'] for f in peer_files) == 26

db = Database(arguments(['run']))
assert db.args.database == 'math' and db.args.source == SOURCE
assert db.basis() == start['basis'], 'Live basis changed; replan before publishing preparations.'
original = read(ROOT / 'original-content.json')
repaired = read(ROOT / 'repaired-content.json')
retirement = loads((VALID / 'stage2-retirement.edn').read_text())
assert retirement[':retirement/questions'] == ['q-79044', 'q-79945']
assert retirement[':retirement/external-incoming-references'] == 0
assert retirement[':retirement/all-current-facts-retracted']
assert retirement[':retirement/all-originals-recovered-from-history']
assert retirement[':retirement/unaffected-components-unchanged']

# Readable diff is between the exact normalized contents of the two EDNs.
lines = ['SURGICAL REPAIR DIFF — PREPARED ONLY, NOT COMMITTED',
         'All 26 repairs authored and independently reviewed by GPT-6-astra / ultra.',
         'Old = Math Academy content from stage 1; new = agent repair in stage 2.',
         'Original choice labels below identify their captured positions.', '']
counts = collections.Counter()
for mid, proposal in sorted(proposals.items()):
    lines += [mid, 'MA intended choice: ' + chr(65 + proposal['ma_choice_index']), '']
    for repair in proposal['repairs']:
        attr = repair['attribute']
        counts[attr] += 1
        if attr == 'choice':
            index = repair['choice_index']
            old_field = next(f for f in original[mid]['answer_fields'] if f['key'] == repair['field_key'])
            new_field = next(f for f in repaired[mid]['answer_fields'] if f['key'] == repair['field_key'])
            before, after = old_field['choices'][index]['value'], new_field['choices'][index]['value']
            label = 'choice ' + chr(65 + index)
        else:
            before, after = original[mid][attr], repaired[mid][attr]
            label = attr
        assert before != after
        lines += [label + ': ' + repair['reason']]
        lines += list(difflib.unified_diff(before.splitlines(), after.splitlines(),
                      fromfile=mid + '/' + label + '/Math-Academy',
                      tofile=mid + '/' + label + '/gpt-6-astra-ultra', lineterm='', n=2))
        lines += ['']
    lines += ['']
(ROOT / 'repair-diff.txt').write_text('\n'.join(lines) + '\n')
assert dict(counts) == {'problem': 25, 'worked_solution': 11, 'choice': 2}

stages = []
DEST.mkdir(parents=True, exist_ok=True)
for i, name, source in [(1, '001-math-academy-original.edn', SOURCE),
                        (2, '002-astra-surgical-repairs.edn', REPAIR_SOURCE)]:
    path = TX / name
    receipt = loads((VALID / ('stage%d-preview.edn' % i)).read_text())
    destination = DEST / name
    if destination.exists():
        assert destination.read_bytes() == path.read_bytes(), 'Refuse to overwrite different prepared EDN.'
    else:
        destination.write_bytes(path.read_bytes())
    assert sha(destination) == sha(path)
    stages.append({'stage': i, 'source': source, 'reference_file': str(path), 'ssd_file': str(destination),
                   'sha256': sha(path), 'bytes': path.stat().st_size, 'questions': 26,
                   'forms': len(loads(path.read_text())), 'preview_datoms': len(receipt[':edb/tx-data']),
                   'planned_retractions': verification['stages'][i-1]['exact_retractions'],
                   'speculative_basis_before': receipt[':edb/db-before-t'],
                   'speculative_basis_after': receipt[':edb/db-after-t'], 'transacted': False})
assert {p.name for p in DEST.iterdir()} == {s['ssd_file'].rsplit('/', 1)[1] for s in stages}
assert sha(INDEX) == start['held_index_sha256']
assert db.basis() == start['basis']
manifest = {'database': 'math', 'basis_prepared_against': start['basis'],
    'basis_after_previews': start['basis'], 'transacted': False, 'database_writes': 0,
    'prepared_questions': 26, 'prepared_answer_fields': 26, 'unprepared_questions': 0,
    'original_stage_new_questions': 23, 'original_stage_existing_questions': 3,
    'held_index_questions': 26, 'held_index_unchanged': True, 'held_index_sha256': sha(INDEX),
    'repair_author_model': 'gpt-6-astra', 'repair_author_reasoning_effort': 'ultra',
    'independent_peer_review_passed': True, 'logical_repairs_by_attribute': dict(counts),
    'all_original_ma_choice_indices_retained': True,
    'retired_fields': 2, 'retired_answer_entities': 10,
    'originals_read_back_from_stage2_as_of_stage1': True,
    'exact_retractions_verified': True, 'source_attribution_verified': True,
    'unchanged_question_uuids_and_kp_membership_verified': True,
    'sequential_speculative_validation_passed': True, 'stages': stages,
    'preview_note': '188 and 189 are in-memory hypothetical successors only; durable basis remains 187.',
    'submission_note': 'Preparation only. Sources are separately supplied transaction options, not EDN attributes. Submit 001 with :org/Math-Academy, then 002 with :agent/gpt-6-astra-ultra only after new authorization. Recheck basis and repeat previews if durable state changed. Never submit stage 2 before stage 1.',
    'artifacts': {'readable_diff': str(ROOT / 'repair-diff.txt'),
                  'mathematical_evidence': str(ROOT / 'repair-plan.json'),
                  'source_evidence': str(ROOT / 'source-evidence.json'),
                  'verification': str(ROOT / 'verification.json'),
                  'retirement_verification': str(VALID / 'stage2-retirement.edn')},
    'preparation_sha256': {str(p.relative_to(ROOT)): sha(p) for p in
        [ROOT / 'prepare.py', ROOT / 'finalize.py', ROOT / 'preview-helper/sequential-preview.rs',
         ROOT / 'review/multiple.json', ROOT / 'review/defects.json',
         ROOT / 'review/peer-review-multiple.json', ROOT / 'review/peer-review-defects.json']}}
save(ROOT / 'manifest.json', manifest)
(ROOT / 'README.txt').write_text('''TWO PREPARED TRANSACTIONS — NOTHING COMMITTED

All 26 remaining held questions are prepared and validated against math basis 187.

1. 001-math-academy-original.edn
   Required transaction source: :org/Math-Academy
   23 new questions, 3 existing question updates. Original prompts, solutions,
   answer choices and MA-intended keys are preserved, including known errors.
   Normalization restores original Roman list labels and canonical image paths.

2. 002-astra-surgical-repairs.edn
   Required transaction source: :agent/gpt-6-astra-ultra
   All repairs authored and independently checked by GPT-6-astra / ultra.
   Changes: 25 prompts, 11 worked solutions, 2 choice values.
   Text repairs use compare-and-swap: EDB retracts the exact original value and
   asserts its replacement. Two superseded fields and their ten answer
   components are retracted from current state and replaced. Both historical
   MA assertions and agent-attributed retractions remain in history. No source
   entity, schema, question identity, or knowledge-point membership is changed.

These are sequential stages concerning the same 26 questions. Sources are
passed separately to EDB; they are not attributes embedded in the EDN file.
The held index still contains all 26 because no commit has occurred.

Both stages were applied only to an in-memory database branch (187 -> 188 ->
189). Full content and history readbacks passed, exact retractions and sources
were verified, and an independent live read remained at basis 187. The old
Math Academy question and answer graphs were recovered from the repaired
speculative database using as-of 188. No external incoming references exist
to the twelve retired component entities.

Review repair-diff.txt for the precise text/option changes. repair-plan.json
contains author reasoning and checks; review/ contains the independently
authored proposals, peer reviews and EDB conventions. validation/ contains
both speculative receipts, readbacks and history. manifest.json records exact
paths, hashes, counts and required sources. The SSD directory contains only
the two transaction EDNs; evidence and metadata remain here.

Do not submit without new authorization. Before any later commit, check the
current basis and revalidate the sequence if it has changed. Use stage 1
before stage 2. Remove questions from the held index only after verified commit.
''')
print(json.dumps({'prepared': 26, 'stages': 2, 'basis': start['basis'], 'database_writes': 0,
                  'logical_repairs': dict(counts), 'retired_entities': 12, 'manifest': str(ROOT / 'manifest.json')}, indent=2))
