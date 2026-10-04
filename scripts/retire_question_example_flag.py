#!/usr/bin/env python3
"""Prepare and verify retirement of question/is-example from captured live exports.

This program writes reviewable transaction files, never submits them. EDB cannot
uninstall attributes. The definition remains documented as retired; canonical KP
references supply the role. Other domain facts must compare byte-for-byte after
normalization, including all content and learner state added since old imports.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts/question_capture'))
from edn import dumps, kw, loads

RETIRED = 'question/is-example'
CONTENT_IDS = {'activity/id', 'step/id', 'tutorial/id', 'question/id', 'example/id',
               'knowledge-point/id', 'answer-field/id', 'answer/id', 'multistep/id',
               'assigned-problem/id', 'topic/id', 'unit/id', 'module/id', 'course/id',
               'course-outcome/id'}


def capture(path):
    manifest = json.loads(path.with_suffix('.manifest.json').read_text())
    identities, canonical, pools, solutions, flags = {}, {}, set(), set(), {}
    counts = Counter()
    digest = hashlib.sha256()
    for line in path.open():
        row = json.loads(line)
        eid, attr = row['e'], row['a']
        counts[attr] += 1
        if attr == RETIRED:
            if row['value_edn'] not in ('true', 'false'):
                raise ValueError('Nonboolean example flag')
            flags[eid] = row['value_edn']
        else:
            digest.update((json.dumps(row, sort_keys=True, ensure_ascii=False) + '\n').encode())
        if attr in CONTENT_IDS:
            if eid in identities:
                raise ValueError('Multiple content identities on one entity')
            identities[eid] = (attr, row['uuid'])
        if attr == 'knowledge-point/canonical-example':
            canonical[eid] = row['ref_eid']
        if attr == 'knowledge-point/questions':
            pools.add(row['ref_eid'])
        if attr == 'question/worked-solution' and (row['raw_string'] or '').strip():
            solutions.add(eid)
    if dict(counts) != manifest['attribute_counts'] or sum(counts.values()) != manifest['domain_datoms']:
        raise ValueError('Export counts differ from its manifest')
    return dict(manifest=manifest, identities=identities, canonical=canonical,
                pools=pools, solutions=solutions, flags=flags, counts=counts,
                preserved_sha256=digest.hexdigest())


def check_roles(state, *, flag_required):
    examples = set(state['canonical'].values())
    questions = {eid for eid, (attr, _) in state['identities'].items() if attr == 'question/id'}
    if examples - questions or examples - state['solutions'] or examples & state['pools']:
        raise ValueError('Canonical references must target solved questions outside every practice pool')
    if state['pools'] - questions:
        raise ValueError('Practice pool contains a nonquestion')
    if flag_required:
        flagged = {eid for eid, value in state['flags'].items() if value == 'true'}
        if flagged != examples or set(state['flags']) != questions:
            raise ValueError('Flagged roles differ from canonical references; resolve before retiring')
    elif state['flags']:
        raise ValueError('Current example flags remain')
    return {'questions': len(questions), 'canonical_examples': len(examples),
            'ordinary_questions': len(questions - examples), 'practice_pool_questions': len(state['pools'])}


def legacy_coverage(legacy, current, replacements, legacy_path):
    target = set(current['identities'].values())
    missing, mapped_answers, retired_placeholders = [], 0, []
    for attr, uid in legacy['identities'].values():
        attr = 'question/id' if attr == 'example/id' else attr
        if attr == 'answer/id' and uid in replacements:
            uid = replacements[uid]
            mapped_answers += 1
        if (attr, uid) not in target:
            # Self-directed study moved to learner/self-directed. The former
            # course was an unreferenced title/identity placeholder, not content.
            if (attr, uid) == ('course/id', '67da3710-807d-5a34-adef-0b3982c2531e'):
                eid = next(e for e, identity in legacy['identities'].items() if identity == (attr, uid))
                facts, referenced = [], False
                for line in legacy_path.open():
                    r = json.loads(line)
                    if r['e'] == eid:
                        facts.append(r)
                    referenced |= r['ref_eid'] == eid
                if ({r['a'] for r in facts} == {'course/id', 'course/title'}
                    and any(r['raw_string'] == 'Self-Directed' for r in facts)
                    and not referenced):
                    retired_placeholders.append([attr, uid])
                    continue
            missing.append([attr, uid])
    if missing:
        raise ValueError(f'Legacy content is missing from active database: {missing[:10]} ({len(missing)} total)')
    return {'legacy_basis': legacy['manifest']['basis_t'],
            'legacy_content_identities': len(legacy['identities']),
            'verified_answer_uuid_replacements': mapped_answers,
            'previously_retired_empty_course_placeholders': retired_placeholders,
            'missing_content_identities': 0}


def prepare(args):
    current = capture(args.before)
    roles = check_roles(current, flag_required=True)
    legacy = capture(args.legacy)
    replacements = json.loads(args.duplicate_map.read_text())['uuid_remap']
    coverage = legacy_coverage(legacy, current, replacements, args.legacy)
    baseline = capture(args.baseline)
    old_questions = {uid for attr, uid in baseline['identities'].values() if attr == 'question/id'}
    now_questions = {uid for attr, uid in current['identities'].values() if attr == 'question/id'}
    if old_questions - now_questions:
        raise ValueError('Questions from the earlier active export are missing')
    output = args.output
    output.mkdir(parents=True, exist_ok=True)
    schema = [[kw('db/retract'), kw('question/validate'), kw('db.entity/attrs'), kw(RETIRED)],
              {kw('db/id'): kw(RETIRED), kw('db/doc'):
               'Retired. Derive worked-example roles from knowledge-point/canonical-example. Do not write this attribute.'}]
    # Reassert definitions/docs, but explicitly retract the old required-key fact:
    # cardinality-many schema maps add members rather than replacing their sets.
    for file in ['schema/content/4-question.edn', 'schema/data/6-knowledge-point.edn']:
        text = '\n'.join(line for line in (ROOT / file).read_text().splitlines()
                         if not line.lstrip().startswith(';'))
        schema.extend(loads(text))
    rows = [[kw('db/retract'), eid, kw(RETIRED), value == 'true']
            for eid, value in sorted(current['flags'].items())]
    if len(schema) + len(rows) >= 100_000:
        raise ValueError('Migration exceeds one native transaction; prepare bounded transactions explicitly')
    batches = [('retire.edn', schema + rows)]
    files = []
    for name, forms in batches:
        text = dumps(forms) + '\n'
        (output / name).write_text(text)
        digest = hashlib.sha256(text.encode()).hexdigest()
        files.append({'file': name, 'sha256': digest, 'forms': len(forms),
                      'basis': current['manifest']['basis_t'] + len(files),
                      'request_key': 'retire-question-example-' + digest})
    report = {'before': str(args.before), 'database': current['manifest']['database'],
              'basis_before': current['manifest']['basis_t'], 'roles': roles,
              'legacy_coverage': coverage, 'added_questions_since_previous_export': len(now_questions-old_questions),
              'preserved_domain_facts_sha256': current['preserved_sha256'],
              'flag_facts_to_retract': len(rows), 'batches': files}
    (output / 'plan.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k:v for k,v in report.items() if k != 'batches'}, indent=2))


def verify(args):
    before, after = capture(args.before), capture(args.after)
    roles = check_roles(after, flag_required=False)
    expected_counts = before['counts'].copy()
    expected_counts.pop(RETIRED, None)
    if (after['counts'] != expected_counts or before['preserved_sha256'] != after['preserved_sha256']):
        raise ValueError('Other domain facts changed; compare exports before declaring migration complete')
    report = {'ok': True, 'basis_before': before['manifest']['basis_t'],
              'basis_after': after['manifest']['basis_t'], 'roles': roles,
              'retracted_example_flags': len(before['flags']),
              'all_other_domain_facts_unchanged': True,
              'preserved_domain_facts': sum(after['counts'].values()),
              'preserved_domain_facts_sha256': after['preserved_sha256']}
    args.report.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    p = commands.add_parser('prepare')
    p.add_argument('--before', type=Path, required=True)
    p.add_argument('--legacy', type=Path, required=True)
    p.add_argument('--baseline', type=Path, required=True)
    p.add_argument('--duplicate-map', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    p = commands.add_parser('verify')
    p.add_argument('--before', type=Path, required=True)
    p.add_argument('--after', type=Path, required=True)
    p.add_argument('--report', type=Path, required=True)
    args = parser.parse_args()
    (prepare if args.command == 'prepare' else verify)(args)


if __name__ == '__main__':
    main()
