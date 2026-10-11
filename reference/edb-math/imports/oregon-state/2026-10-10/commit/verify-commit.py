#!/usr/bin/env python3
"""Compare prepared EDN intent, actual committed receipts, and final live pulls.

Reads saved files only; never opens a database or submits a transaction.
Usage: verify-commit.py PREPARED_ROOT COMMIT_DIR BASELINE_DB_DIR
COMMIT_DIR also contains final-basis.json with the basis observed by a live read.
"""
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime
import hashlib
import json
import sys
import uuid

sys.path.insert(0, '/home/jake/Developer/Course_Academy/capture')
from scripts.database.edn import Keyword, loads

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('/tmp/osu-preparation')
PREVIEW = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(__file__).resolve().parent
BASELINE_DB = Path(sys.argv[3]) if len(sys.argv) > 3 else PREVIEW/'current-baseline/db'
ORDER = [
    ('oregon-state/1-oregon-state.edn', ':person/jake'),
    ('oregon-state/2-courses.edn', ':org/Oregon-State'),
    ('oregon-state/3-assignments.edn', ':org/Oregon-State'),
    ('oregon-state/4-assignment-study-content.edn', ':agent/gpt-6-astra-high'),
    ('local/chatgpt-6-pro.edn', ':person/jake'),
    ('oregon-state/5-course-maps.edn', ':agent/chatgpt-6-pro'),
    ('oregon-state/6-deadline-corrections.edn', ':person/jake'),
]
ALLOWED_NAMESPACES = {'course', 'course-group', 'course-outcome', 'tutorial', 'answer',
    'answer-field', 'question', 'step', 'multistep', 'assigned-problem', 'activity'}

def require(condition, message):
    if not condition:
        raise AssertionError(message)

def edn(path):
    return loads(path.read_text())

def identity_key(attribute, value):
    return (str(attribute), str(value) if isinstance(value, uuid.UUID) else value)

def row_identity(row):
    explicit = row.get(':db/id')
    identities = [identity_key(k, v) for k, v in row.items()
                  if (str(k).endswith('/id') and k != ':db/id') or k == ':db/ident']
    if isinstance(explicit, list):
        require(len(explicit) == 2, 'Malformed entity lookup reference')
        key = identity_key(*explicit)
        require(not identities or identities == [key], 'Conflicting explicit entity identity')
        return key
    require(len(identities) == 1, f'Expected exactly one identity: {identities!r}')
    return identities[0]

def main():
    state = json.loads((BASELINE_DB/'state.json').read_text())
    manifest = json.loads((ROOT/'prepared-manifest.json').read_text())
    schema = {str(name): (eid, str(typ), str(card)) for eid, name, typ, card in state['attributes']}
    names = {item[0]: name for name, item in schema.items()}
    baseline_idents = {str(name): eid for eid, name in edn(BASELINE_DB/'idents.edn')}
    idents = dict(baseline_idents)
    lookups = {identity_key(':db/ident', name): eid for name, eid in idents.items()}
    topic_eids = set()
    topic_pairs = {int(ma): str(uid) for ma, uid in state['topics']}
    for eid, ma, uid in edn(BASELINE_DB/'topics-with-eids.edn'):
        require(topic_pairs[int(ma)] == str(uid), f'Changed topic identity {ma}')
        lookups[identity_key(':topic/math-academy-id', ma)] = eid
        lookups[identity_key(':topic/id', uid)] = eid
        topic_eids.add(eid)
    require(len(topic_eids) == len(topic_pairs), 'Incomplete external topic EID mapping')

    reports = [edn(PREVIEW/f'stage{i}-commit.edn') for i in range(1, len(ORDER)+1)]
    # New source identities are not among the root pulls; their whole state is
    # checked through the exact stage datom comparison below.
    for report in reports:
        for entity, attribute, value, tx, source, added in report[':edb/tx-data']:
            if attribute == schema[':db/ident'][0] and added:
                key = identity_key(':db/ident', value)
                require(key not in lookups or lookups[key] == entity, 'Ident remapped to a new EID')
                lookups[key] = entity
                idents[str(value)] = entity

    pull_rows = edn(PREVIEW/'final-pull1.edn')
    pulled = {}
    for raw_identity, value in pull_rows:
        require(isinstance(raw_identity, list) and len(raw_identity) == 2, 'Unexpected pull identity')
        key = identity_key(*raw_identity)
        require(key not in pulled, f'Duplicate pulled identity {key}')
        require(value.get(raw_identity[0]) == raw_identity[1], f'Pulled identity mismatch: {key}')
        pulled[key] = value
        require(key not in lookups or lookups[key] == value[':db/id'], f'EID changed: {key}')
        lookups[key] = value[':db/id']
    require(len({x[':db/id'] for x in pulled.values()}) == len(pulled), 'Two identities share one EID')
    expected_pull_keys = {identity_key(*raw) for raw in edn(ROOT/'pull-identities.edn')}
    require(set(pulled) == expected_pull_keys, 'Pull output does not cover exactly requested identities')

    stages, declared = [], set()
    def flatten(row, flattened):
        require(isinstance(row, dict), 'Only reviewed map transactions are allowed')
        key = row_identity(row)
        declared.add(key)
        flattened.append((key, row))
        for attribute, value in row.items():
            if attribute in (':db/id', ':db/ensure'):
                continue
            require(attribute in schema, f'Unknown attribute {attribute}')
            namespace = str(attribute)[1:].split('/')[0]
            require(namespace in ALLOWED_NAMESPACES or attribute in (':db/ident', ':db/doc'),
                    f'Forbidden content, learner, or schema write: {attribute}')
            require('math-academy-id' not in str(attribute), 'Math Academy identity write')
            typ = schema[attribute][1]
            if typ == ':db.type/ref':
                values = value if schema[attribute][2] == ':db.cardinality/many' else [value]
                for child in values:
                    if isinstance(child, dict):
                        flatten(child, flattened)
    require(len(manifest['transactions']) == len(ORDER), 'Unexpected transaction count')
    for index, ((relative, source), entry) in enumerate(zip(ORDER, manifest['transactions']), 1):
        path = ROOT/'output/seeds'/relative
        require(entry['path'] == 'seeds/'+relative and entry['source'] == source, 'Stage order/source mismatch')
        require(hashlib.sha256(path.read_bytes()).hexdigest() == entry['sha256'], f'Input changed: {relative}')
        rows = edn(path)
        require(len(rows) == entry['maps'], f'Map count mismatch: {relative}')
        flattened = []
        for row in rows:
            flatten(row, flattened)
        stage_temps = {}
        for key, row in flattened:
            raw = row.get(':db/id')
            if type(raw) is str:
                require(raw not in stage_temps or stage_temps[raw] == key, 'Tempid reused for distinct identity')
                stage_temps[raw] = key
                require(reports[index-1][':edb/tempids'].get(raw) == lookups[key],
                        f'Tempid maps to wrong entity: {relative}: {raw}')
        stages.append((relative, source, flattened, stage_temps))
    source_keys = {identity_key(':db/ident', ':org/Oregon-State'),
                   identity_key(':db/ident', ':agent/chatgpt-6-pro')}
    require(declared - source_keys == set(pulled), 'Declared entities do not exactly match final pulls')
    declared_eids = {lookups[key] for key in declared}
    require(not declared_eids.intersection(topic_eids), 'A write targets existing Math Academy topic content')
    require(not declared_eids.intersection(baseline_idents.values()), 'A write targets an existing schema/source/enum entity')

    def reference(value, temps, actual=False):
        if isinstance(value, dict):
            return value[':db/id'] if actual else lookups[row_identity(value)]
        if isinstance(value, Keyword):
            return idents[str(value)]
        if isinstance(value, list):
            require(len(value) == 2, 'Malformed reference lookup')
            return lookups[identity_key(*value)]
        if type(value) is str:
            return lookups[temps[value]]
        require(actual and type(value) is int, f'Unexpected reference {value!r}')
        return value

    def scalar(value, attribute, temps=None, actual=False):
        typ = schema[attribute][1]
        if typ == ':db.type/ref':
            return ('ref', reference(value, temps or {}, actual))
        if typ == ':db.type/instant':
            instant = datetime.fromisoformat(value.replace('Z', '+00:00'))
            require(instant.tzinfo is not None, 'Instant must have explicit timezone')
            return ('instant', round(instant.timestamp() * 1000))
        if typ == ':db.type/uuid':
            require(isinstance(value, uuid.UUID), f'Expected UUID for {attribute}')
            return ('uuid', str(value))
        if typ == ':db.type/keyword':
            require(isinstance(value, Keyword), f'Expected keyword for {attribute}')
            return ('keyword', str(value))
        return (typ, value)

    current = defaultdict(dict)  # (entity, attr) -> normalized value -> asserting sources
    stage_summaries = []
    total_refs = 0
    for i, (relative, source, flattened, temps) in enumerate(stages, 1):
        requested = defaultdict(set)
        for key, row in flattened:
            for attribute, value in row.items():
                if attribute in (':db/id', ':db/ensure'):
                    continue
                attr_eid, typ, cardinality = schema[attribute]
                values = value if cardinality == ':db.cardinality/many' else [value]
                for v in values:
                    requested[(lookups[key], attr_eid)].add(scalar(v, attribute, temps))
                    total_refs += typ == ':db.type/ref'
        source_eid = idents[source]
        expected_delta = set()
        for (entity, attribute), values in requested.items():
            name = names[attribute]
            if schema[name][2] == ':db.cardinality/one':
                require(len(values) == 1, f'Conflicting cardinality-one input: {relative}: {name}')
                for old in set(current[(entity, attribute)]) - values:
                    expected_delta.add((entity, attribute, old, source_eid, False))
                    del current[(entity, attribute)][old]
            for value in values:
                sources = current[(entity, attribute)].setdefault(value, set())
                if source_eid not in sources:
                    expected_delta.add((entity, attribute, value, source_eid, True))
                    sources.add(source_eid)
        report = reports[i-1]
        require(report[':edb/committed'] is True and not report.get(':edb/speculative', False), 'Receipt is not committed')
        require(report[':edb/basis-t'] == report[':edb/db-after-t'], 'Receipt basis disagrees with report')
        tx_hash = report[':edb/tx-hash']
        require(isinstance(tx_hash, str) and len(tx_hash) == 64 and all(c in '0123456789abcdef' for c in tx_hash), 'Receipt has invalid transaction hash')
        require(report[':edb/db-before-t'] == state['basis'] + i - 1, 'Incorrect sequential db-before')
        require(report[':edb/db-after-t'] == state['basis'] + i, 'Incorrect sequential db-after')
        material, timestamps = [], []
        txs = set()
        for entity, attribute, value, tx, asserted_source, added in report[':edb/tx-data']:
            require(asserted_source == source_eid, f'Wrong factual attribution: {relative}: {names.get(attribute)}')
            txs.add(tx)
            if attribute == schema[':db/txInstant'][0]:
                timestamps.append((entity, value, tx, added))
                continue
            require(entity in declared_eids, f'Unexpected write target {entity} in {relative}')
            require(attribute in names, f'Unknown written attribute {attribute}')
            material.append((entity, attribute, scalar(value, names[attribute], actual=True), asserted_source, added))
        require(len(timestamps) == 1 and timestamps[0][0] == timestamps[0][2] and timestamps[0][3] is True,
                f'Incorrect transaction timestamp: {relative}')
        require(len(txs) == 1, 'Datoms span multiple transaction coordinates')
        require(len(material) == len(set(material)), 'Duplicate material datom')
        actual_delta = set(material)
        missing, unexpected = expected_delta - actual_delta, actual_delta - expected_delta
        require(not missing and not unexpected,
                f'Stage {i} exact datom mismatch: missing={len(missing)}, unexpected={len(unexpected)}; '
                f'examples={repr(list(missing)[:1])[:300]} / {repr(list(unexpected)[:1])[:300]}')
        stage_summaries.append({'stage': i, 'source': source, 'material_datoms': len(material),
                                'additions': sum(x[-1] for x in material),
                                'retractions': sum(not x[-1] for x in material)})

    checked_attrs, checked_facts = 0, 0
    for key, row in pulled.items():
        entity = lookups[key]
        expected_attrs = {names[attr]: set(values) for (eid, attr), values in current.items() if eid == entity}
        actual_attrs = set(row) - {':db/id'}
        require(actual_attrs == set(expected_attrs), f'Attribute presence mismatch: {key}: {actual_attrs ^ set(expected_attrs)}')
        for attribute, expected_values in expected_attrs.items():
            raw = row[attribute]
            values = raw if schema[attribute][2] == ':db.cardinality/many' else [raw]
            actual_values = {scalar(v, attribute, actual=True) for v in values}
            require(actual_values == expected_values, f'Final value/reference mismatch: {key}: {attribute}')
            checked_attrs += 1
            checked_facts += len(expected_values)
    # Check attribution on the live current facts, including multiple surviving
    # sources for an identical fact. This independently checks receipt replay.
    pulled_eids = {value[':db/id'] for value in pulled.values()}
    expected_current_facts = {
        (entity, attribute, value, source)
        for (entity, attribute), values in current.items() if entity in pulled_eids
        for value, sources in values.items() for source in sources
    }
    actual_current_facts = set()
    current_rows = edn(PREVIEW/'final-facts.edn')
    for entity, attribute, value, source in current_rows:
        require(entity in pulled_eids, f'Unexpected entity in current facts: {entity}')
        require(attribute in names, f'Unknown current-fact attribute: {attribute}')
        actual_current_facts.add((entity, attribute, scalar(value, names[attribute], actual=True), source))
    require(len(actual_current_facts) == len(current_rows), 'Duplicate current fact in saved read')
    missing_current = expected_current_facts - actual_current_facts
    unexpected_current = actual_current_facts - expected_current_facts
    require(not missing_current and not unexpected_current,
            f'Current fact/provenance mismatch: missing={len(missing_current)}, '
            f'unexpected={len(unexpected_current)}; '
            f'examples={repr(list(missing_current)[:1])[:300]} / {repr(list(unexpected_current)[:1])[:300]}')
    final_basis = json.loads((PREVIEW/'final-basis.json').read_text())['basis']
    require(final_basis == state['basis'] + len(ORDER) == reports[-1][':edb/basis-t'],
            'Final live basis does not equal the last committed receipt')
    counts = Counter(key[0].split('/')[0].lstrip(':') for key in pulled)
    for kind, expected in manifest['assignment_counts'].items():
        require(counts[kind] == expected, f'Wrong entity count for {kind}')
    require(counts['course'] == 6 and counts['course-group'] == 1 and counts['course-outcome'] == 62, 'Wrong course graph counts')
    result = {'ok': True, 'read_only_verifier': True, 'durable_basis_before': state['basis'], 'durable_basis_after': final_basis,
        'pulled_entities_checked': len(pulled), 'source_entities_checked_by_complete_deltas': len(source_keys),
        'attributes_checked': checked_attrs, 'final_facts_checked': checked_facts,
        'current_facts_with_provenance_checked': len(actual_current_facts),
        'input_reference_values_checked': total_refs, 'entity_counts': dict(counts),
        'exact_stage_deltas_and_attribution': stage_summaries,
        'no_learner_or_math_academy_content_writes': True,
        'committed_transactions_checked': len(ORDER)}
    print(json.dumps(result, indent=2))
    return result

if __name__ == '__main__':
    try:
        main()
    except (AssertionError, KeyError, ValueError) as error:
        print(f'COMMIT VERIFICATION FAILED: {error}', file=sys.stderr)
        raise SystemExit(1)
