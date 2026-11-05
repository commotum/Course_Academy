"""Assemble candidate histories and reconcile selected repair receipts offline."""
import collections
import itertools
import json
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
sys.path.insert(0, str(ROOT))
from capture.scripts.database.edn import loads


def read(name):
    return json.loads((OUT / name).read_text())


def save(name, data):
    (OUT / name).write_text(json.dumps(data, indent=2, ensure_ascii=False)+'\n')


def logical_t(tx):
    # Verified against EDB src/model/identity.rs: EIDX_BITS=42, TX_PARTITION=3.
    assert tx >> 42 == 3
    return tx & ((1 << 42) - 1)


capture = read('capture.json')
current = {r[0][':db/id']: r[0] for r in read('evidence/current.json')}
registrations = read('evidence/registration-history.json')
scripts = read('evidence/script-history.json')
identities = {g: uid for g, uid, tx, source, added in read('evidence/generator-identities.json') if added}
by_kp, by_generator = collections.defaultdict(list), collections.defaultdict(list)
for row in registrations:
    by_kp[row[0]].append(row)
for row in scripts:
    by_generator[row[0]].append(row)


def script_at(generator, t):
    state = set()
    for _, path, tx, _, added, _ in sorted(by_generator[generator], key=lambda r: (r[2], r[4])):
        if logical_t(tx) <= t:
            (state.add if added else state.discard)(path)
    assert len(state) == 1, (generator, t, state)
    return next(iter(state))


def version(generator, t):
    script = script_at(generator, t)
    immutable = script.startswith('generators/')
    path = Path(capture['math_root'] if immutable else ROOT) / script
    return {'entity': generator, 'uuid': identities[generator], 'script': script,
            'package_sha256': script.split('/')[2] if immutable else None,
            'file_exists_now': path.is_file(),
            'historical_bytes_immutable': immutable}


transitions, records, event_index = [], [], {}
for kp, rows in sorted(by_kp.items()):
    state = set()
    events = []
    for tx, txrows in itertools.groupby(sorted(rows, key=lambda r: r[2]), key=lambda r: r[2]):
        group = list(txrows)
        previous = set(state)
        for _, g, _, _, added, _ in sorted(group, key=lambda r: r[4]):
            (state.add if added else state.discard)(g)
        assert len(state) <= 1
        if state != previous:
            t = logical_t(tx)
            event = {'kp': kp, 't': t, 'tx': tx, 'instant': group[0][5],
                     'source_entities': sorted({r[3] for r in group}),
                     'before': version(next(iter(previous)), t-1) if previous else None,
                     'after': version(next(iter(state)), t) if state else None,
                     'repair_evidence': []}
            events.append(event)
            event_index[kp, tx] = event
            if event['before'] and event['after']:
                transitions.append(event)
    live = current.get(kp)
    assert state == ({live[':knowledge-point/question-generator'][':db/id']} if live else set())
    if live:
        assert script_at(next(iter(state)), capture['basis']) == live[':knowledge-point/question-generator'][':question-generator/script']
    records.append({'kp': kp, 'title': live.get(':knowledge-point/title') if live else None,
        'topics': live.get(':topic/_knowledge-points', []) if live else [],
        'currently_registered': bool(live), 'distinct_generator_entities': len({r[1] for r in rows if r[4]}),
        'registration_events': events})

local = read('local-repair-evidence.json')
schema = {r[0][':db/ident']:r[0][':db/id'] for r in read('evidence/schema.json')}
history_keys = {tuple(r[:5]) for r in registrations}
matched, unmatched, receipt_errors = [], [], []
episodes = [dict(e, evidence_kind='selected_one_off') for e in local['one_off_episodes']]
for e in local['early_cohort']['candidates']:
    episodes.append({'directory':str(Path(e['job']).parent), 'knowledge_points':[e['kp']],
        'reason_heading':'Early-cohort review findings', 'finding_kinds':e['finding_kinds'],
        'receipt_paths':e['receipt_paths'], 'evidence_kind':'early_cohort_review',
        'repair_history':e['repair_history'], 'publication':e['publication']})

for episode in episodes:
    for receipt_path in episode['receipt_paths']:
        try:
            receipt = loads((ROOT / receipt_path).read_text())
            assert receipt[':edb/committed'] is True
            assert receipt[':edb/db-after-t'] <= capture['basis']
        except Exception as error:
            receipt_errors.append({'receipt':receipt_path,'error':str(error)})
            continue
        for kp, attr, generator, tx, source, added in receipt[':edb/tx-data']:
            if attr != schema[':knowledge-point/question-generator'] or not added:
                continue
            evidence = {'directory':episode['directory'], 'receipt':receipt_path,
                        'reason_heading':episode['reason_heading'],
                        'kind':episode['evidence_kind'], 'finding_kinds':episode.get('finding_kinds', [])}
            event = event_index.get((kp, tx))
            if (kp, generator, tx, source, added) not in history_keys or not event:
                unmatched.append({'kp':kp,'tx':tx, **evidence})
                continue
            assert logical_t(tx) == receipt[':edb/db-after-t']
            event['repair_evidence'].append(evidence)
            matched.append({'kp':kp,'t':logical_t(tx),'is_republication':bool(event['before']), **evidence})

# Changes to a script attribute on an existing registered generator are separate
# from replacing the generator entity. Preserve these even when KPs overlap.
script_changes = []
for g, rows in by_generator.items():
    times = sorted({logical_t(r[2]) for r in rows})
    for t in times[1:]:
        before, after = script_at(g, t-1), script_at(g, t)
        if before == after:
            continue
        for record in records:
            prior = [e for e in record['registration_events'] if e['t'] < t]
            if prior and prior[-1]['after'] and prior[-1]['after']['entity'] == g:
                script_changes.append({'kp':record['kp'],'generator':g,'t':t,
                                       'before_script':before,'after_script':after})

selected_transitions = [e for e in transitions if any(x['kind']=='selected_one_off' for x in e['repair_evidence'])]
cohort_transitions = [e for e in transitions if any(x['kind']=='early_cohort_review' for x in e['repair_evidence'])]
changed = {r['kp'] for r in records if r['distinct_generator_entities'] > 1}
legacy = [17592186068814, 17592186105887]
script_changed_kps = {e['kp'] for e in script_changes}
one_off_kps = {kp for episode in local['one_off_episodes'] for kp in episode['knowledge_points']}
for record in records:
    kp = record['kp']
    record['candidate_reasons'] = (
        (['multiple_published_generator_identities'] if kp in changed else [])
        + (['registered_script_attribute_changed'] if kp in script_changed_kps else [])
        + (['legacy_git_change_needs_publication_byte_evidence'] if kp in legacy else []))
    record['script_attribute_changes'] = [e for e in script_changes if e['kp'] == kp]
    record['selected_one_off_evidence'] = [e for e in local['one_off_episodes'] if kp in e['knowledge_points']]
summary = {**capture, 'currently_registered_kps':len(current), 'ever_registered_kps':len(records),
    'kps_with_multiple_generator_identities':len(changed), 'registration_replacements':len(transitions),
    'registered_script_attribute_changes':len(script_changes),
    'kps_with_registered_script_attribute_changes':len({e['kp'] for e in script_changes}),
    'kps_with_edb_recorded_generator_change':len(changed | script_changed_kps),
    'broad_candidates_including_uncertain_legacy_git_changes':len(changed | script_changed_kps | set(legacy)),
    'selected_one_off_republication_events_receipt_matched':len(selected_transitions),
    'selected_one_off_republication_kps_receipt_matched':len({e['kp'] for e in selected_transitions}),
    'early_cohort_republication_events_receipt_matched':len(cohort_transitions),
    'early_cohort_republication_kps_receipt_matched':len({e['kp'] for e in cohort_transitions}),
    'repair_evidence_republication_kps_union':len({e['kp'] for e in selected_transitions+cohort_transitions}),
    'selected_one_off_review_group_including_documented_in_place_repair':len(one_off_kps),
    'selected_first_publication_events':len({(e['kp'],e['t']) for e in matched if not e['is_republication']}),
    'receipt_errors':receipt_errors, 'unmatched_registration_receipt_datoms':unmatched,
    'legacy_additional_candidates':legacy,
    'limitations':['Evidence selection is not exhaustive; unlabelled changes are unclassified, not known nonrepairs.',
       'Repair evidence records a past repair claim and committed publication, not a fresh pedagogical acceptance test.',
       'Legacy mutable path edits require Git and saved original files; database registration alone misses them.',
       'Package changes include mechanical migrations, helpers, metadata and dependencies.',
       'Duplicate evidence directories are deduplicated by KP and transaction.']}
save('summary.json', summary)
save('generator-histories.json', records)
save('candidate-kps.json', [r for r in records if r['candidate_reasons']])
save('one-off-review-group.json', [{'kp':r['kp'],'title':r['title'],'topics':r['topics'],
    'evidence_status':('receipt_matched_republication' if any(e['kp']==r['kp'] for e in selected_transitions)
                       else 'documented_in_place_repair_no_registration_transition'),
    'republished_at_t':sorted({e['t'] for e in selected_transitions if e['kp']==r['kp']}),
    'evidence_directories':[e['directory'] for e in r['selected_one_off_evidence']]}
    for r in records if r['kp'] in one_off_kps])
save('repair-evidence-transitions.json', [e for e in transitions if e['repair_evidence']])
save('script-attribute-changes.json', script_changes)
print(json.dumps(summary, indent=2))
