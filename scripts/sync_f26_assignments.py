#!/usr/bin/env python3
"""Prepare current F26 assignments and replace explicit learner targets in EDB.

Reads a native EntitySnapshot and writes one reviewable transaction. Does not
write to the database or vault. Source aliases preserve the original imports.
"""

from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

from f26_assignment_content import build
from import_school_assignments import DEFAULT_LEARNER, ROOT, VAULT


def edn(value):
    if value is None:
        return 'nil'
    if isinstance(value, bool):
        return 'true' if value else 'false'
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, str):
        return value if value.startswith(':') else json.dumps(value, ensure_ascii=False)
    if isinstance(value, list):
        return '[' + ' '.join(edn(v) for v in value) + ']'
    if isinstance(value, dict):
        if '$uuid' in value:
            return '#uuid ' + json.dumps(value['$uuid'])
        if '$keyword' in value:
            return ':' + value['$keyword'].lstrip(':')
        if '$inst' in value:
            return '#inst ' + json.dumps(value['$inst'])
        if '$instant' in value:
            instant = value['$instant']
            if isinstance(instant, (int, float)):
                instant = datetime.fromtimestamp(instant / 1000, timezone.utc).isoformat().replace('+00:00', 'Z')
            return '#inst ' + json.dumps(instant)
        if '$ref' in value:
            return edn(value['$ref'])
        return '{' + '\n  '.join(f'{key} {edn(v)}' for key, v in value.items()) + '}'
    raise TypeError(value)


# Only these links traverse assignment-owned/authored content. Coverage, scope,
# learner records, and other shared curriculum are deliberately not traversed.
CONTENT_LINKS = (
    'activity/steps', 'step/content', 'multistep/steps',
    'assigned-problem/content', 'question/answer-fields', 'answer-field/choices',
)
OPTIONAL_MANAGED = {
    'activity': ('activity/due', 'activity/course', 'activity/scope'),
    'step': ('step/next',),
    'multistep': ('multistep/context',),
    'assigned-problem': ('assigned-problem/topic-coverage',),
    'question': ('question/answer-fields', 'question/worked-solution'),
}


def prepare(snapshot, entities, activities, target_ids, learner):
    rows = {int(k): v for k, v in snapshot['entities'].items()}
    identities = {}
    for eid, row in rows.items():
        for attr, value in row.items():
            if attr.endswith('/id') or attr in ('db/ident', 'topic/math-academy-id'):
                identities[attr, json.dumps(value, sort_keys=True)] = eid

    def lookup(attr, value):
        return identities.get((attr.lstrip(':'), json.dumps(value, sort_keys=True)))

    generated = {r[':db/id']: r for r in entities}
    assert len(generated) == len(entities), 'Duplicate generated identity'
    present = {}
    for identity, row in generated.items():
        attr = next(k for k in row if k.endswith('/id') and k != ':db/id')
        present[identity] = lookup(attr, row[attr])

    def reference(value):
        if isinstance(value, dict):
            if '$ref' in value:
                found = lookup(*value['$ref'])
                if found is None:
                    raise ValueError(f'Unresolved reference: {value}')
                return found
            if '$inst' in value:
                at = datetime.fromisoformat(value['$inst'].replace('Z', '+00:00'))
                return {'$instant': int(at.timestamp() * 1000)}
            return value
        if isinstance(value, list):
            return [reference(v) for v in value]
        if isinstance(value, str):
            if value in generated:
                return present[value] or value
            if value.startswith(':'):
                found = lookup('db/ident', {'$keyword': value[1:]})
                if found is None:
                    raise ValueError(f'Uninstalled enum/spec: {value}')
                return found
        return value

    def normalized(value):
        if isinstance(value, dict) and '$instant' in value and isinstance(value['$instant'], str):
            return {'$instant': int(datetime.fromisoformat(value['$instant'].replace('Z', '+00:00')).timestamp() * 1000)}
        return value

    def values(value):
        return {json.dumps(normalized(v), sort_keys=True): normalized(v) for v in value}

    learner_eid = lookup('learner/id', learner)
    if learner_eid is None:
        raise ValueError('Learner not found')
    old_activities = rows[learner_eid].get('learner/assignments', [])
    old_content = set()

    def visit(eid):
        if eid in old_content:
            return
        old_content.add(eid)
        for attr in CONTENT_LINKS:
            linked = rows[eid].get(attr, [])
            for child in linked if isinstance(linked, list) else [linked]:
                visit(child)

    for activity in old_activities:
        # The requested replacement concerns this learner's current schoolwork.
        visit(activity)

    retained = {eid for eid in present.values() if eid is not None}
    stale = old_content - retained
    # Keep any obsolete material referenced by history or by unrelated content.
    # Recursively retain its children, without altering those records.
    protected = set()
    submitted_answers = {answer for row in rows.values() for answer in row.get('task-item/responses', [])}
    for eid, row in rows.items():
        if eid in old_content:
            continue
        for value in row.values():
            for candidate in value if isinstance(value, list) else [value]:
                if isinstance(candidate, int) and not isinstance(candidate, bool) and candidate in stale:
                    protected.add(candidate)
    changed = True
    while changed:
        size = len(protected)
        for eid in list(protected):
            for attr in CONTENT_LINKS:
                linked = rows[eid].get(attr, [])
                protected.update(child for child in (linked if isinstance(linked, list) else [linked]) if child in stale)
        # A retained response also needs its owning field and question. Keep
        # the obsolete containing route, not just a detached answer value.
        for eid in stale:
            for attr in CONTENT_LINKS:
                linked = rows[eid].get(attr, [])
                if any(child in protected for child in (linked if isinstance(linked, list) else [linked])):
                    protected.add(eid)
        changed = len(protected) != size
    removable = stale - protected

    forms, edits = [], []
    for identity, row in generated.items():
        eid = present[identity]
        if eid is None:
            forms.append({k: (v if k in (':db/id', ':db/ensure') else reference(v)) for k, v in row.items()})
            continue
        stored = rows[eid]
        kind = next(k[1:-3] for k in row if k.endswith('/id') and k != ':db/id')
        attributes = {k[1:] for k in row if k not in (':db/id', ':db/ensure')} | set(OPTIONAL_MANAGED.get(kind, ()))
        altered = False
        for attr in sorted(attributes):
            old = normalized(stored.get(attr))
            desired = reference(row[':' + attr]) if ':' + attr in row else None
            if isinstance(old, list) or isinstance(desired, list):
                before, after = values(old or []), values(desired or [])
                removed_values = [before[key] for key in before.keys() - after.keys()]
                if attr == 'answer-field/choices' and any(v in submitted_answers for v in removed_values):
                    raise ValueError(f'Cannot detach a submitted answer from field {eid}; review history first')
                if attr == 'question/answer-fields' and any(
                    set(rows[field].get('answer-field/choices', [])) & submitted_answers for field in removed_values
                ):
                    raise ValueError(f'Cannot detach a historically used field from question {eid}')
                for key in before.keys() - after.keys():
                    forms.append([':db/retract', eid, ':' + attr, before[key]])
                for key in after.keys() - before.keys():
                    forms.append([':db/add', eid, ':' + attr, after[key]])
                different = before != after
            else:
                different = old != desired
                if different:
                    if eid in submitted_answers and attr in ('answer/value', 'answer/type'):
                        raise ValueError(f'Cannot rewrite submitted answer {eid}; review history first')
                    if desired is None:
                        forms.append([':db/retract', eid, ':' + attr, old])
                    else:
                        # The caller also commits against this snapshot basis.
                        forms.append([':db/cas', eid, ':' + attr, old, desired])
            if different:
                altered = True
                edits.append({'entity': eid, 'attribute': attr, 'before': old, 'after': desired})
        if altered:
            forms.append({':db/id': eid, ':db/ensure': row[':db/ensure']})

    def replace_set(attr, desired):
        old = values(rows[learner_eid].get(attr, []))
        new = values(desired)
        for key in old.keys() - new.keys():
            forms.append([':db/retract', learner_eid, ':' + attr, old[key]])
        for key in new.keys() - old.keys():
            forms.append([':db/add', learner_eid, ':' + attr, new[key]])

    target_eids = []
    for target in sorted(set(target_ids)):
        eid = lookup('topic/math-academy-id', target)
        if eid is None:
            raise ValueError(f'Missing target topic {target}')
        target_eids.append(eid)
    replace_set('learner/assignments', [reference(a) for a in activities])
    replace_set('learner/targets', target_eids)
    # The learner's identity and knowledge-profile are unchanged. Its native
    # profile predicate is unrelated to these validated target/assignment refs.
    # Explicit fact retractions avoid component cascade accidentally reaching
    # shared or historically referenced material.
    for eid in sorted(removable):
        for attr, value in rows[eid].items():
            if attr.startswith('db/'):
                continue
            for item in value if isinstance(value, list) else [value]:
                forms.append([':db/retract', eid, ':' + attr, normalized(item)])
    report = {
        'basis': snapshot['basis_t'], 'learner_eid': learner_eid,
        'old_assignment_eids': old_activities, 'activity_ids': activities,
        'old_target_count': len(rows[learner_eid].get('learner/targets', [])),
        'target_ids': sorted(set(target_ids)), 'target_eids': sorted(target_eids),
        'created': sum(eid is None for eid in present.values()),
        'reused': len(retained), 'removed_obsolete_entities': sorted(removable),
        'preserved_historical_entities': sorted(protected),
        'edits': edits, 'forms': len(forms),
    }
    return forms, report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--snapshot', type=Path, required=True)
    parser.add_argument('--vault', type=Path, default=VAULT)
    parser.add_argument('--learner', default=DEFAULT_LEARNER)
    parser.add_argument('--output', type=Path, default=ROOT / '.local/edb/f26-refresh')
    args = parser.parse_args()
    entities, activities, audit = build(args.vault)
    snapshot = json.loads(args.snapshot.read_text())
    forms, report = prepare(snapshot, entities, activities, audit['target_union'], args.learner)
    args.output.mkdir(parents=True, exist_ok=True)
    transaction = '[\n' + '\n '.join(edn(f) for f in forms) + '\n]\n'
    (args.output / 'refresh.edn').write_text(transaction)
    (args.output / 'entities.json').write_text(json.dumps(entities, ensure_ascii=False, indent=2) + '\n')
    report.update({'source_audit': audit, 'sha256': hashlib.sha256(transaction.encode()).hexdigest()})
    (args.output / 'refresh-audit.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k not in ('edits', 'source_audit')}, indent=2))


if __name__ == '__main__':
    main()
