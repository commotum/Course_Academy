"""Read-only offline delivery, conditional-cue, selection and inventory probes."""
import collections
import hashlib
import json
import sys
from pathlib import Path
from repair_checks import E, ROOT, answer_signature, bank, correct_value, equations, g, independent, save


def outcome(r): return correct_value(r) == 'No solution'


def cues(records):
    groups = collections.defaultdict(list)
    for r in records:
        a = equations(r['question'])
        # These cues deliberately exclude the decisive second constant.
        identities = {
            'coefficient_signature': tuple(str(v) for v in a[:, :2]),
            'first_equation': tuple(str(v) for v in a[0, :]),
            'complete_visible_bank': tuple(sorted(bank(r))),
            'bank_layout_types': tuple(v[':answer/type'] for v in r['question'][':question/answer-fields'][0][':answer-field/choices']),
            'position_of_No_solution': bank(r).index('No solution'),
            'choice_count': len(bank(r)),
            'profile': r['generation']['template'],
        }
        for name, cue in identities.items(): groups[(name, str(cue))].append(r)
    output = []
    for (name, cue), rs in groups.items():
        decisions = collections.Counter('no_solution' if outcome(r) else 'infinite' for r in rs)
        assert len(decisions) == 2, ('incidental cue fixes consistency', name, cue, decisions)
        output.append({'cue': name, 'value': cue, 'counts': dict(decisions)})
    return {'records': len(records), 'semantic_instances': len({g.fingerprint(r['question']) for r in records}), 'all_cue_groups_have_both_outcomes': True, 'groups': output}


def signature(r): return tuple(str(v) for v in equations(r['question'])[:, :2])


def old_shortcut(r, training):
    if training[signature(r)]: return 'No solution'
    a = equations(r['question']); answers = []
    for value in bank(r):
        sig = answer_signature(value)
        if sig != ('none',) and sig[1] == g.y and g.sp.expand(a[0, 0]*sig[0]+a[0, 1]*sig[1]-a[0, 2]) == 0:
            answers.append(value)
    assert len(answers) == 1
    return answers[0]


def measure(rs, training):
    successes = sum(old_shortcut(r, training) == correct_value(r) for r in rs)
    return {'successes': successes, 'records': len(rs), 'outcomes': dict(collections.Counter('no_solution' if outcome(r) else 'infinite' for r in rs))}


def main():
    raw = json.loads((E/'delivery-input.json').read_text())
    accepted = json.loads((E/'delivery/accepted.json').read_text())
    batch = json.loads((E/'delivery-batch/accepted.json').read_text())
    raw_cues, delivered_cues = cues(raw), cues(accepted)
    for r in accepted + batch: independent(r)
    training = {signature(g.generate('easy', 7331, sid, {'rhs_scale': 1})): outcome(g.generate('easy', 7331, sid, {'rhs_scale': 1}))
                for sid,q in g.CASES.items() if q[':question/difficulty'][':db/ident'].endswith('/easy')}
    measurements = {'paired_before_delivery': measure(raw, training), 'paired_after_delivery': measure(accepted, training), 'five_question_batch': measure(batch, training)}
    assert measurements['paired_after_delivery']['successes'] * 2 == len(accepted)
    # Actual constructor rejects only repeated mathematical fingerprints. Test a
    # small default sample, preserving original branch probabilities and histories.
    constructed = g.batch('easy', 24, 105746)
    for r in constructed: independent(r)
    assert len({g.fingerprint(r['question']) for r in constructed}) == len(constructed)
    save('constructor-records.json', constructed)
    measurements['constructor_after_internal_dedup'] = measure(constructed, training)
    save('shortcut-results.json', {'passed': True, 'training': 'source-original consistency per visible coefficient signature; for predicted consistent cases use only first equation', 'measurements': measurements, 'before_delivery': raw_cues, 'after_delivery': delivered_cues, 'limits': 'Paired probes disprove deterministic cue strategies. The small random five-question batch is not a balance guarantee or a statistical mastery measure.'})
    # Captured inventory has complete question fields but no generation metadata.
    # Establish source membership before declaring an absence of generated defects.
    inv = json.loads((ROOT.parent/'source/inventory.json').read_text())
    source = json.loads((ROOT.parent/'source/source.json').read_text())['material']['kp'][':knowledge-point/questions']
    source_ids = {q[':question/id'] for q in source}
    non_sources = [q for q in inv['questions'] if q[':question/id'] not in source_ids]
    assert not non_sources, 'Non-source inventory requires reproduction against stored metadata'
    metadata = sum(any('generation' in k for k in q) for q in inv['questions'])
    assert metadata == 0
    (ROOT/'affected-inventory.json').write_text(json.dumps({'affected_questions': []}, indent=2)+'\n')
    save('inventory-audit.json', {'basis': inv['basis'], 'questions_examined': len(inv['questions']), 'original_source_questions': len(inv['questions']), 'non_source_questions': len(non_sources), 'generation_metadata_count': metadata, 'verified_absence': 'All 17 captured stored questions are original source records. No stored generated instances of the demonstrated construction weakness exist in this captured inventory. Originals were not marked generated.', 'source_question_ids': sorted(source_ids), 'inventory_sha256': hashlib.sha256((ROOT.parent/'source/inventory.json').read_bytes()).hexdigest(), 'limit': 'Captured basis only, not a live database read.'})
    # Read-only fixture of select()'s easy-only positively weighted branch. No
    # engine edits; unavailable task histories and published IDs are not invented.
    fixture = [{'entity_id': 1000000+i, 'record': r} for i,r in enumerate(accepted)]
    draws = []
    for seed in ['repair-selection-'+str(i) for i in range(16)]:
        h = hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest()
        u = (int.from_bytes(h[8:16], 'big') >> 11) / (1 << 53)
        selected = fixture[int(u*len(fixture))]
        r = selected['record']
        draws.append({'seed': seed, 'fixture_entity_id': selected['entity_id'], 'question_id': r['question'][':question/id'], 'outcome': 'no_solution' if outcome(r) else 'infinite', 'old_shortcut_succeeds': old_shortcut(r, training)==correct_value(r)})
    assert len({r['outcome'] for r in draws}) == 2 and not all(r['old_shortcut_succeeds'] for r in draws)
    save('selection-results.json', {'engine': 'engine/rust/question_selection.rs:select and seen_before_task', 'weights': [1,0,0], 'fixture_only': True, 'draws': draws, 'interpretation': 'The selector removes seen items, chooses a band, then a fresh question. It does not inspect coefficient signatures or outcomes. Source-matched inventory removal was tested by actual check_delivery. All paired outcome cases survive that filtering. Arbitrary learner histories can exhaust one case type; no guarantee about live user-specific frequencies is made.', 'unweighted_fallback': 'No distribution uses the first fixture ID; a single draw alone does not establish within-profile coverage.', 'limits': ['Live policy weights and learner history are unavailable.', 'Fixture entity IDs stand in for unpublished records; no database operations.']})
    print(json.dumps({'passed': True, 'controlled_after_delivery': len(accepted), 'both_outcomes_every_cue_group': True, 'old_shortcut': measurements, 'inventory_originals': len(inv['questions'])}))

if __name__ == '__main__': main()
