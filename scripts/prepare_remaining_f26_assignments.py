#!/usr/bin/env python3
"""Prepare an additive import of F26 assignments absent from an EDB snapshot.

Existing assignment content and explicit learner targets are preserved. Writes
EDN and a source audit only; preview and transact separately using EDB's CLI.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

from f26_assignment_content import Builder, LEGACY_SEEDS
from import_school_assignments import DEFAULT_LEARNER, Import, ROOT, VAULT, stable_id
from sync_f26_assignments import edn


def prepare(snapshot, vault=VAULT, learner=DEFAULT_LEARNER, sources=None):
    existing = {row['activity/id']['$uuid'] for row in snapshot['entities'].values()
                if 'activity/id' in row}
    builder = Builder(vault)
    selected, skipped, activities = [], [], []
    files = sorted((builder.vault / 'F26').glob('[0-9]*/*.md'))
    for path in files:
        relative = str(path.relative_to(builder.vault))
        if sources is not None and relative not in sources:
            continue
        code = path.stem.split('_', 1)[1]
        seed = LEGACY_SEEDS.get((path.parent.name, code), f'F26/{path.parent.name}/{code}')
        if sources is None and stable_id(seed, 'activity') in existing:
            skipped.append(relative)
            continue
        activities.append(builder.assignment(relative))
        selected.append(relative)
    if sources is not None and set(selected) != set(sources):
        raise ValueError('Previously selected source files are missing')
    builder.validate()
    # Reuse the original add-only transaction builder: it resolves all shared
    # references and rejects conflicting records instead of reconciling them.
    model = Import(vault, {})
    model.entities = builder.entities
    forms = model.transaction(snapshot, learner, activities)
    audit = builder.audit
    audit.update({'basis': snapshot['basis_t'], 'learner': learner,
                  'selected_sources': selected, 'skipped_existing_sources': skipped,
                  'assets': list(builder.assets.values()),
                  'counts': dict(Counter(next(k[1:-3] for k in row if k.endswith('/id') and k != ':db/id')
                                         for row in builder.entities)),
                  'forms': len(forms),
                  'target_union': sorted({t for a in audit['activities'] for p in a['problems'] for t in p['topics']}),
                  'import_policy': 'Add missing definitions and learner/assignments links only; preserve existing content, targets, tasks, responses, progress, and engine configuration.'})
    return builder.entities, forms, audit


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--snapshot', type=Path, required=True)
    parser.add_argument('--vault', type=Path, default=VAULT)
    parser.add_argument('--learner', default=DEFAULT_LEARNER)
    parser.add_argument('--output', type=Path, default=ROOT / '.local/edb/f26-remaining-2026-10-07')
    args = parser.parse_args()
    snapshot = json.loads(args.snapshot.read_text())
    entities, forms, audit = prepare(snapshot, args.vault, args.learner)
    args.output.mkdir(parents=True, exist_ok=True)
    transaction = '[\n' + '\n '.join(edn(f) for f in forms) + '\n]\n'
    audit['transaction_sha256'] = hashlib.sha256(transaction.encode()).hexdigest()
    (args.output / 'transaction.edn').write_text(transaction)
    for name, value in [('entities', entities), ('audit', audit)]:
        (args.output / (name + '.json')).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: audit[k] for k in ('basis', 'selected_sources', 'counts', 'forms', 'transaction_sha256')}, indent=2))


if __name__ == '__main__':
    main()
