"""Script-owned imported coverage, reference selection, and schema migration.

Reads for one investigation use the source's immutable EDB basis. Missing
imported fields are observations, never repair requests for those records.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from capture.scripts.database.client import StaleBasis
from capture.scripts.database.commit import Committer, connection_identity
from capture.scripts.database.edn import Symbol, dumps, kw, loads
from capture.scripts.storage import atomic_json, atomic_text

BANDS = ('easy', 'moderate', 'hard')
COVERAGE = ':knowledge-point/level-coverage'
SCHEMA_FILES = ('schema/data/6-knowledge-point.edn', 'schema/content/4-question.edn')
ANSWER_PULL = '[:db/id :answer/id :answer/value {:answer/type [:db/ident]}]'
QUESTION_PULL = '''[:db/id :question/id :question/math-academy-id :question/problem
 :question/worked-solution :question/requires-calculator :question/retired
 {:question/difficulty [:db/ident]}
 {:knowledge-point/_canonical-example [:db/id]}
 {[:question/answer-fields :limit nil] [:db/id :answer-field/id :answer-field/key
  {:answer-field/type [:db/ident]}
  {:answer-field/correct ''' + ANSWER_PULL + '''}
  {[:answer-field/choices :limit nil] ''' + ANSWER_PULL + '''}]}]'''
COUNTS_QUERY = """[:find ?kp ?band (count-distinct ?q) :in $ [?kp ...]
 :where [?q :question/difficulty ?d] [?d :db/ident ?band]
 [?q :question/math-academy-id _] [?kp :knowledge-point/questions ?q]]"""
OBSERVED_QUERY = """[:find ?kp ?band :in $ [?kp ...]
 :where [?q :question/difficulty ?d] [?d :db/ident ?band]
 [?q :question/math-academy-id _]
 (or-join [?kp ?q] [?kp :knowledge-point/questions ?q]
                         [?kp :knowledge-point/canonical-example ?q])]"""


def _enum(value):
    return str(value.get(':db/ident', '') if isinstance(value, dict) else value or '')


def _band(question):
    return _enum(question.get(':question/difficulty')).rsplit('/', 1)[-1]


def _json(value):
    if isinstance(value, dict):
        return {str(k): _json(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json(v) for v in value]
    return value if value is None or isinstance(value, (str, int, float, bool)) else str(value)


def _hash(value):
    return hashlib.sha256(json.dumps(_json(value), sort_keys=True).encode()).hexdigest()


def observed_coverage(questions):
    """An incomplete imported question still establishes its captured label."""
    observed = {_band(q) for q in questions if q.get(':question/math-academy-id')}
    return [band for band in BANDS if band in observed] or ['unobserved']


def completeness(question):
    """Return missing usable evidence, checking every required response field."""
    missing = []
    for attribute in (':question/problem', ':question/worked-solution'):
        if not isinstance(question.get(attribute), str) or not question[attribute].strip():
            missing.append(attribute)
    if _band(question) not in BANDS:
        missing.append(':question/difficulty')
    fields = question.get(':question/answer-fields', [])
    if not fields:
        missing.append(':question/answer-fields')
    keys = set()
    for index, field in enumerate(fields):
        prefix = f'answer-fields[{index}]'
        key = field.get(':answer-field/key')
        if not isinstance(key, str) or not key or key in keys:
            missing.append(prefix + '.key')
        keys.add(key)
        kind = _enum(field.get(':answer-field/type')).rsplit('/', 1)[-1]
        if kind not in ('radio', 'select', 'blank', 'checkbox', 'free'):
            missing.append(prefix + '.type')
        choices = field.get(':answer-field/choices', [])
        correct = field.get(':answer-field/correct')
        # A complete donor needs a reference solution even for an ungraded
        # free field; partial free prompts remain useful target evidence.
        def identity(value):
            if isinstance(value, dict):
                return str(value.get(':answer/id') or value.get(':db/id') or '')
            if isinstance(value, (list, tuple)) and len(value) == 2:
                return str(value[1])
            return str(value or '')
        ids = {identity(choice) for choice in choices}
        if not choices or not identity(correct) or identity(correct) not in ids:
            missing.append(prefix + '.correct')
        for choice in choices:
            if (_enum(choice.get(':answer/type')) not in
                    (':answer.type/math', ':answer.type/text', ':answer.type/image')
                    or not isinstance(choice.get(':answer/value'), str)
                    or not choice[':answer/value'].strip()):
                missing.append(prefix + '.answer-value')
        if kind in ('radio', 'select') and len(choices) < 2:
            missing.append(prefix + '.choices')
        if kind == 'checkbox' and ({c.get(':answer/value') for c in choices} != {'true', 'false'}
                                   or any(_enum(c.get(':answer/type')) != ':answer.type/text' for c in choices)):
            missing.append(prefix + '.checkbox-bank')
    return missing


def _rank(point, target):
    words = lambda text: set(re.findall(r'[a-z]{3,}', str(text).lower())) - {'the', 'and', 'with', 'from', 'using', 'for'}
    overlap = len(words(point.get(':knowledge-point/title')) & words(target.get(':knowledge-point/title')))
    prereqs = lambda value: {v[':db/id'] for v in value.get(':knowledge-point/key-prerequisites', [])}
    shared = len(prereqs(point) & prereqs(target))
    return (-shared, -overlap, int(point[':db/id']))


def prepare_investigation(publisher, source, directory):
    """Select a complete single-KP reference without agent database searches."""
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    basis = int(source['basis'])
    target = source['material']['kp']
    questions = [q for q in target.get(':knowledge-point/questions', []) if q.get(':question/math-academy-id')]
    canonical = target.get(':knowledge-point/canonical-example')
    coverage_questions = questions + ([canonical] if canonical else [])
    complete = Counter(_band(q) for q in questions if not completeness(q))
    observations = [{'question_id': str(q.get(':question/id', '')), 'entity_id': q.get(':db/id'),
                     'missing': completeness(q)} for q in questions if completeness(q)]
    recorded = {_enum(value).rsplit('/', 1)[-1] for value in target.get(COVERAGE, [])}
    coverage = [b for b in BANDS if b in recorded] or (['unobserved'] if 'unobserved' in recorded else observed_coverage(coverage_questions))
    summary = {'database': source['database'], 'lineage': source['lineage'], 'basis': basis,
               'kp_id': int(source['kp_id']), 'observed_coverage': coverage,
               'complete_examples': {b: complete[b] for b in BANDS},
               'incomplete_imports': observations,
               'construction_needed': bool(observations) or any(not complete[b] for b in BANDS)}
    reference_file = directory / 'reference.json'
    preparation_key = _hash(source)
    input_file = directory / 'investigation-input.json'
    if input_file.exists() and reference_file.exists():
        saved = json.loads(input_file.read_text())
        if saved.get('preparation_key') == preparation_key:
            return {**saved, 'investigation_file': str(input_file), 'reference_file': str(reference_file)}
    summary['preparation_key'] = preparation_key
    summary['needs_exemplars'] = summary['construction_needed']
    # Metadata and observed coverage are small. Never join the whole corpus to
    # worked-solution strings or form a KP x difficulty collection cross-product.
    pattern = ('[:db/id :knowledge-point/title {:knowledge-point/key-prerequisites [:db/id]}'
               ' {:knowledge-point/level-coverage [:db/ident]}]')
    metadata = [r[0] for r in publisher.client.query(
        '[:find (pull ?kp ' + pattern + ') :where [?kp :knowledge-point/id _]]',
        [], directory, 'reference-kp-metadata', basis)]
    metadata = [point for point in metadata if all(
        ':question.difficulty/' + band in {_enum(v) for v in point.get(COVERAGE, [])} for band in BANDS)]
    metadata.sort(key=lambda value: _rank(value, target))
    def qualified_points():
        for start in range(0, len(metadata), 25):
            group = metadata[start:start + 25]
            rows = publisher.client.query(COUNTS_QUERY, [[point[':db/id'] for point in group]],
                                          directory, f'candidate-counts-{start}', basis)
            counts = defaultdict(dict)
            for kp, band, count in rows:
                counts[int(kp)][str(band).rsplit('/', 1)[-1]] = int(count)
            yield from (point for point in group if all(counts[point[':db/id']].get(b, 0) >= 2 for b in BANDS))
    for point in qualified_points():
        kp = int(point[':db/id'])
        ids = sorted({r[0] for r in publisher.client.query(
            '''[:find ?q :in $ ?kp :where [?kp :knowledge-point/questions ?q]
             [?q :question/math-academy-id _] [?q :question/worked-solution _]
             [?q :question/difficulty _] [?q :question/answer-fields _]]''',
            [kp], directory, f'reference-question-ids-{kp}', basis)})
        excluded = {q[':db/id'] for q in publisher.source_exclusions(directory / f'eligibility-{kp}', basis, ids)}
        ids = [eid for eid in ids if eid not in excluded]
        selected = {b: [] for b in BANDS}
        for start in range(0, len(ids), 100):
            pulled = publisher.client.query('[:find (pull ?q ' + QUESTION_PULL +
                ') :in $ [?q ...] :where [?q :question/id _]]',
                [ids[start:start + 100]], directory, f'reference-questions-{kp}-{start}', basis)
            for row in sorted(pulled, key=lambda r: int(r[0][':db/id'])):
                question = row[0]
                band = _band(question)
                if (band in BANDS and len(selected[band]) < 2 and not question.get(':question/retired')
                        and not question.get(':knowledge-point/_canonical-example') and not completeness(question)):
                    selected[band].append(question)
            if all(len(selected[b]) == 2 for b in BANDS):
                reference = {**summary, 'reference_kp': point, 'questions': selected}
                atomic_json(reference_file, _json(reference))
                summary['reference_kp_id'] = kp
                atomic_json(directory / 'investigation-input.json', _json(summary))
                return {**summary, 'investigation_file': str(directory / 'investigation-input.json'),
                        'reference_file': str(reference_file)}
    raise ValueError('Imported reference candidates had incomplete response fields; inspect retained query evidence')


def _schema_forms():
    wanted = {COVERAGE, ':question.difficulty/unobserved'}
    return [form for name in SCHEMA_FILES for form in loads((ROOT / name).read_text())
            if str(form.get(':db/ident')) in wanted]


def _coverage_rows(client, directory, basis, kp_ids, prefix):
    """Bind KPs first so enum lookup cannot scan the entire ident dictionary."""
    query = ('[:find ?kp ?ident :in $ [?kp ...] :where [?d :db/ident ?ident] '
             '[?kp :knowledge-point/level-coverage ?d]]')
    kp_ids = sorted(set(map(int, kp_ids)))
    for start in range(0, len(kp_ids), 100):
        yield from client.query(query, [kp_ids[start:start + 100]], directory,
                                f'{prefix}-{basis}-{start}', basis)


def coverage_plan(client, directory, basis):
    """Compute an exact many-ref set replacement, without changing imports."""
    directory = Path(directory)
    identity = client.status()
    cache_path = directory / 'coverage-plan.json'
    if cache_path.exists():
        cached = json.loads(cache_path.read_text())
        if (cached.get('database') == identity['database'] and cached.get('lineage') == identity['lineage']
                and coverage_inputs_unchanged(client, directory, cached['basis'], basis)):
            return loads(cached['forms_edn']), cached['expected']
    rows = client.query('[:find ?kp :where [?kp :knowledge-point/id _]]', [], directory, 'coverage-kps', basis)
    kp_ids = sorted(row[0] for row in rows)
    current = defaultdict(set)
    for kp, ident in _coverage_rows(client, directory, basis, kp_ids, 'coverage-before'):
        current[int(kp)].add(str(ident))
    observed = defaultdict(set)
    for start in range(0, len(kp_ids), 100):
        for kp, band in client.query(OBSERVED_QUERY, [kp_ids[start:start + 100]],
                                    directory, f'coverage-observed-{start}', basis):
            if str(band).rsplit('/', 1)[-1] in BANDS:
                observed[int(kp)].add(str(band))
    expected, forms = {}, []
    for (kp,) in sorted(rows):
        wanted = observed[kp] or {':question.difficulty/unobserved'}
        expected[str(kp)] = sorted(wanted)
        for ident in sorted(current[kp] - wanted):
            forms.append([kw('db/retract'), kp, kw(COVERAGE), kw(ident)])
        for ident in sorted(wanted - current[kp]):
            forms.append([kw('db/add'), kp, kw(COVERAGE), kw(ident)])
    atomic_json(cache_path, {'database': identity['database'], 'lineage': identity['lineage'],
        'basis': basis, 'forms_edn': dumps(forms), 'expected': expected})
    return forms, expected


COVERAGE_INPUTS = (
    'knowledge-point/id', 'knowledge-point/questions', 'knowledge-point/canonical-example',
    'knowledge-point/level-coverage', 'question/math-academy-id', 'question/difficulty',
    'db/ident', 'db/valueType', 'db/cardinality',
)


def coverage_inputs_unchanged(client, directory, before, after):
    """Prove a rebase from committed log events, including all retractions."""
    if before == after:
        return True
    if before > after:
        raise ValueError('Coverage cannot rebase backward')
    directory = Path(directory) / f'changes-{before}-{after}'
    directory.mkdir(parents=True, exist_ok=True)
    attributes = client.query('[:find ?a ?ident :in $ [?ident ...] :where [?a :db/ident ?ident]]',
        [[kw(name) for name in COVERAGE_INPUTS]], directory, 'attributes', before)
    names = {int(eid): str(ident) for eid, ident in attributes}
    if len(names) != len(COVERAGE_INPUTS):
        raise ValueError('Coverage dependency attribute dictionary is incomplete')
    query = ('[:find ?e ?a ?tx ?op :in $log ?start ?end :where '
             '[(tx-ids $log ?start ?end) [?tx ...]] '
             '[(tx-data $log ?tx) [[?e ?a ?v ?tx ?s ?op]]]]')
    atomic_text(directory / 'query.edn', query)
    atomic_text(directory / 'inputs.edn', dumps([before + 1, after + 1]))
    atomic_text(directory / 'sources.edn', dumps({Symbol('$log'): {
        kw('database'): str(client.config.database), kw('log'): True}}))
    text = client.command('query', '--file', directory / 'query.edn', '--inputs', directory / 'inputs.edn',
                          '--sources', directory / 'sources.edn')
    atomic_text(directory / 'log.edn', text)
    relevant = [row for row in loads(text) if row[1] in names]
    atomic_json(directory / 'verification.json', {'before': before, 'after': after,
        'unchanged': not relevant, 'relevant_changes': [
            {'entity': row[0], 'attribute': names[row[1]], 'transaction': row[2], 'added': row[3]}
            for row in relevant]})
    return not relevant


def _transact(publisher, directory, forms, basis, source, apply, *, coverage_rebase=False):
    """Persist exact intent; unrelated learner writes may safely rebase coverage."""
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    committer = Committer(publisher.config, publisher.client, directory)
    for attempt in range(4):
        request = committer.pending()
        if request is None:
            status = publisher.client.status()
            if status['basis'] != basis and not coverage_rebase:
                raise StaleBasis('Coverage migration basis advanced before preview')
            transaction = dumps(forms) + '\n'
            atomic_text(directory / 'transaction.edn', transaction)
            preview_text = publisher.client.command('with', '--file', directory / 'transaction.edn', '--source', source)
            atomic_text(directory / 'preview.edn', preview_text)
            preview = loads(preview_text)
            preview_basis = int(preview[':edb/db-before-t'])
            if preview_basis != basis:
                if not coverage_rebase or not coverage_inputs_unchanged(publisher.client, directory, basis, preview_basis):
                    raise StaleBasis('Coverage inputs changed during preparation; recompute from fresh source')
            request = {**connection_identity(publisher.config), 'basis': preview_basis, 'source': source,
                       'database_lineage': status['lineage'], 'transaction': transaction,
                       'transaction_sha256': hashlib.sha256(transaction.encode()).hexdigest()}
            request['request_key'] = 'kp-level-coverage-' + _hash(request)
            atomic_json(committer.intent_path, request)
        if not apply:
            return {'prepared': True, 'request_key': request['request_key'], 'basis': request['basis']}
        try:
            receipt = committer.submit(request)
        except StaleBasis:
            committer.retire(request, 'rejected_stale_basis', {'reason': 'Confirmed basis rejection; recheck source dependencies'})
            if coverage_rebase and attempt < 3:
                continue
            raise
        if receipt.get(':edb/db-before-t') != request['basis']:
            raise ValueError('Coverage receipt does not match its saved basis')
        after = int(receipt[':edb/db-after-t'])
        source_rows = publisher.client.query('[:find ?s :in $ ?ident :where [?s :db/ident ?ident]]',
            [kw(request['source'])], directory, 'transaction-source', after)
        if len(source_rows) != 1 or any(row[4] != source_rows[0][0] for row in receipt.get(':edb/tx-data', [])):
            raise ValueError('Coverage receipt contributor differs from the requested agent')
        return {'committed': True, 'basis': after, 'request_key': request['request_key']}


def _verify_schema(publisher, directory, basis):
    rows = publisher.client.query('[:find (pull ?a [* {:db/valueType [:db/ident]} {:db/cardinality [:db/ident]}])'
        ' :in $ [?i ...] :where [?a :db/ident ?i]]', [[kw(COVERAGE), kw('question.difficulty/unobserved')]],
        directory, 'schema-readback', basis)
    declaration = next((r[0] for r in rows if str(r[0][':db/ident']) == COVERAGE), {})
    if len(rows) != 2 or _enum(declaration.get(':db/valueType')) != ':db.type/ref' or _enum(declaration.get(':db/cardinality')) != ':db.cardinality/many':
        raise ValueError('Coverage schema readback differs from many/ref declaration')


def _verify_coverage(publisher, directory, basis, expected):
    actual = defaultdict(list)
    for kp, ident in _coverage_rows(publisher.client, directory, basis, expected, 'coverage-readback'):
        actual[str(kp)].append(str(ident))
    if {k: sorted(v) for k, v in actual.items()} != expected:
        raise ValueError('Coverage readback differs from the prepared sets')


def _retire(publisher, directory, result):
    committer = Committer(publisher.config, publisher.client, directory)
    committer.retire(committer.pending(), 'verified', result)


def migrate_coverage(publisher, directory, *, apply=False, source=':agent/codex'):
    """Install declarations and backfill; recover each saved request first."""
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    status = publisher.client.status()
    rows = publisher.client.query('[:find ?ident :in $ [?ident ...] :where [_ :db/ident ?ident]]',
        [[kw(COVERAGE), kw('question.difficulty/unobserved')]], directory, 'schema-before', status['basis'])
    existing = {str(row[0]) for row in rows}
    schema_dir, backfill_dir = directory / 'schema', directory / 'backfill'
    if len(existing) < 2 or (schema_dir / 'request.json').exists():
        result = _transact(publisher, schema_dir,
            [form for form in _schema_forms() if str(form[kw('db/ident')]) not in existing],
            status['basis'], source, apply)
        if not apply:
            return {'stage': 'schema', **result}
        _verify_schema(publisher, schema_dir, result['basis'])
        _retire(publisher, schema_dir, result)
    else:
        _verify_schema(publisher, schema_dir, status['basis'])
    # A lost reply is reconciled against the original expected sets before any
    # fresh source reads may replace the saved plan.
    if (backfill_dir / 'request.json').exists():
        result = _transact(publisher, backfill_dir, [], status['basis'], source, apply, coverage_rebase=True)
        if not apply:
            return {'stage': 'backfill', **result}
        expected = json.loads((backfill_dir / 'expected-coverage.json').read_text())
        _verify_coverage(publisher, backfill_dir, result['basis'], expected)
        _retire(publisher, backfill_dir, result)
        atomic_json(directory / 'coverage-plan.json', {'database': status['database'], 'lineage': status['lineage'],
            'basis': result['basis'], 'forms_edn': '[]', 'expected': expected})
    status = publisher.client.status()
    forms, expected = coverage_plan(publisher.client, directory, status['basis'])
    if forms:
        atomic_json(backfill_dir / 'expected-coverage.json', expected)
        result = _transact(publisher, backfill_dir, forms, status['basis'], source, apply, coverage_rebase=True)
        if not apply:
            return {'stage': 'backfill', 'knowledge_points': len(expected), 'changes': len(forms), **result}
        after = result['basis']
        _verify_coverage(publisher, backfill_dir, after, expected)
        _retire(publisher, backfill_dir, result)
        atomic_json(directory / 'coverage-plan.json', {'database': status['database'], 'lineage': status['lineage'],
            'basis': after, 'forms_edn': '[]', 'expected': expected})
    else:
        after = status['basis']
    result = {'verified': True, 'basis': after, 'knowledge_points': len(expected), 'changes': len(forms)}
    atomic_json(directory / 'verification.json', result)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--directory', type=Path, required=True)
    parser.add_argument('--apply', action='store_true')
    parser.add_argument('--source', default=':agent/codex')
    args = parser.parse_args()
    from scripts.generator_publish import Publisher
    publisher = Publisher.from_environment(source=args.source)
    for attempt in range(3):
        try:
            result = migrate_coverage(publisher, args.directory, apply=args.apply, source=args.source)
            break
        except StaleBasis:
            if attempt == 2:
                raise
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
