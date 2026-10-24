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
from capture.scripts.database.edn import dumps, kw, loads
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
COUNTS_QUERY = '''[:find ?kp ?band (count-distinct ?q) :in $ [?band ...]
 :where [?d :db/ident ?band] [?q :question/difficulty ?d]
 [?q :question/math-academy-id _] [?q :question/problem _]
 [?q :question/worked-solution _] [?q :question/answer-fields _]
 [?kp :knowledge-point/questions ?q]]'''
OBSERVED_QUERY = '''[:find ?kp ?band :in $ [?band ...]
 :where [?d :db/ident ?band] [?q :question/difficulty ?d]
 [?q :question/math-academy-id _]
 (or-join [?kp ?q] [?kp :knowledge-point/questions ?q]
                         [?kp :knowledge-point/canonical-example ?q])]
'''


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
    summary = {'database': source['database'], 'lineage': source['lineage'], 'basis': basis,
               'kp_id': int(source['kp_id']), 'observed_coverage': observed_coverage(coverage_questions),
               'complete_examples': {b: complete[b] for b in BANDS},
               'incomplete_imports': observations,
               'construction_needed': bool(observations) or any(not complete[b] for b in BANDS)}
    reference_file = directory / 'reference.json'
    # All phases receive a progression reference, including source-rich jobs.
    rows = publisher.client.query(COUNTS_QUERY, [[kw('question.difficulty/' + b) for b in BANDS]],
                                  directory, 'candidate-counts', basis)
    counts = defaultdict(dict)
    for kp, band, count in rows:
        counts[int(kp)][str(band).rsplit('/', 1)[-1]] = int(count)
    candidates = sorted(kp for kp, bands in counts.items() if all(bands.get(b, 0) >= 2 for b in BANDS))
    if not candidates:
        raise ValueError('No imported KP with at least two complete candidates per level; inspect candidate-counts.edn')
    metadata = []
    pattern = '[:db/id :knowledge-point/title {:knowledge-point/key-prerequisites [:db/id]}]'
    for start in range(0, len(candidates), 100):
        metadata += [r[0] for r in publisher.client.query(
            '[:find (pull ?kp ' + pattern + ') :in $ [?kp ...] :where [?kp :knowledge-point/id _]]',
            [candidates[start:start + 100]], directory, f'candidate-kps-{start}', basis)]
    for point in sorted(metadata, key=lambda value: _rank(value, target)):
        kp = int(point[':db/id'])
        ids = sorted({r[0] for r in publisher.client.query(
            '''[:find ?q :in $ ?kp :where [?kp :knowledge-point/questions ?q]
             [?q :question/math-academy-id _] [?q :question/worked-solution _]
             [?q :question/difficulty _] [?q :question/answer-fields _]]''',
            [kp], directory, f'reference-question-ids-{kp}', basis)})
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


def coverage_plan(client, directory, basis):
    """Compute an exact many-ref set replacement, without changing imports."""
    directory = Path(directory)
    rows = client.query('[:find ?kp :where [?kp :knowledge-point/id _]]', [], directory, 'coverage-kps', basis)
    current = defaultdict(set)
    for kp, ident in client.query('''[:find ?kp ?ident :where [?kp :knowledge-point/level-coverage ?d]
                                   [?d :db/ident ?ident]]''', [], directory, 'coverage-before', basis):
        current[int(kp)].add(str(ident))
    observed = defaultdict(set)
    for kp, band in client.query(OBSERVED_QUERY, [[kw('question.difficulty/' + b) for b in BANDS]],
                                directory, 'coverage-observed', basis):
        observed[int(kp)].add(str(band))
    expected, forms = {}, []
    for (kp,) in sorted(rows):
        wanted = observed[kp] or {':question.difficulty/unobserved'}
        expected[str(kp)] = sorted(wanted)
        for ident in sorted(current[kp] - wanted):
            forms.append([kw('db/retract'), kp, kw(COVERAGE), kw(ident)])
        for ident in sorted(wanted - current[kp]):
            forms.append([kw('db/add'), kp, kw(COVERAGE), kw(ident)])
    return forms, expected


def _transact(publisher, directory, forms, basis, source, apply):
    """Persist exact intent before submission; recover unknown outcomes first."""
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    committer = Committer(publisher.config, publisher.client, directory)
    request = committer.pending()
    if request is None:
        status = publisher.client.status()
        if status['basis'] != basis:
            raise StaleBasis('Coverage migration basis advanced before preview')
        transaction = dumps(forms) + '\n'
        atomic_text(directory / 'transaction.edn', transaction)
        preview_text = publisher.client.command('with', '--file', directory / 'transaction.edn', '--source', source)
        atomic_text(directory / 'preview.edn', preview_text)
        preview = loads(preview_text)
        if preview.get(':edb/db-before-t') != basis:
            raise StaleBasis('Coverage migration basis advanced during preview')
        request = {**connection_identity(publisher.config), 'basis': basis, 'source': source,
                   'database_lineage': status['lineage'], 'transaction': transaction,
                   'transaction_sha256': hashlib.sha256(transaction.encode()).hexdigest()}
        request['request_key'] = 'kp-level-coverage-' + _hash(request)
        atomic_json(committer.intent_path, request)
    if not apply:
        return {'prepared': True, 'request_key': request['request_key'], 'basis': request['basis']}
    receipt = committer.submit(request)
    if receipt.get(':edb/db-before-t') != request['basis']:
        raise ValueError('Coverage receipt does not match its saved basis')
    after = int(receipt[':edb/db-after-t'])
    # Verify all transaction datoms have the requested contributor. Schema
    # changes have generated metadata, so final shape is read back separately.
    source_rows = publisher.client.query('[:find ?s :in $ ?ident :where [?s :db/ident ?ident]]',
        [kw(source)], directory, 'transaction-source', after)
    if len(source_rows) != 1 or any(row[4] != source_rows[0][0] for row in receipt.get(':edb/tx-data', [])):
        raise ValueError('Coverage receipt contributor differs from the requested agent')
    return {'committed': True, 'basis': after, 'request_key': request['request_key']}


def migrate_coverage(publisher, directory, *, apply=False, source=':agent/codex'):
    """Install the two declarations, then backfill every KP at a guarded basis."""
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    status = publisher.client.status()
    rows = publisher.client.query('[:find (pull ?a [* {:db/valueType [:db/ident]} {:db/cardinality [:db/ident]}])'
        ' :in $ [?i ...] :where [?a :db/ident ?i]]',
        [[kw(COVERAGE), kw('question.difficulty/unobserved')]], directory, 'schema-before', status['basis'])
    existing = {str(row[0][':db/ident']): row[0] for row in rows}
    pending_schema = (directory / 'schema/request.json').exists()
    if len(existing) < 2 or pending_schema:
        result = _transact(publisher, directory / 'schema',
            [form for form in _schema_forms() if str(form[kw('db/ident')]) not in existing],
            status['basis'], source, apply)
        if not apply:
            return {'stage': 'schema', **result}
        status = {**status, 'basis': result['basis']}
    forms, expected = coverage_plan(publisher.client, directory, status['basis'])
    atomic_json(directory / 'expected-coverage.json', expected)
    pending = (directory / 'backfill/request.json').exists()
    if forms or pending:
        result = _transact(publisher, directory / 'backfill', forms, status['basis'], source, apply)
        if not apply:
            return {'stage': 'backfill', 'knowledge_points': len(expected), 'changes': len(forms), **result}
        after = result['basis']
        saved_expected = json.loads((directory / 'expected-coverage.json').read_text())
        verify = defaultdict(list)
        for kp, ident in publisher.client.query('''[:find ?kp ?ident :where [?kp :knowledge-point/level-coverage ?d]
                                                [?d :db/ident ?ident]]''', [], directory, 'coverage-readback', after):
            verify[str(kp)].append(str(ident))
        if {k: sorted(v) for k, v in verify.items()} != saved_expected:
            raise ValueError('Coverage readback differs from the prepared sets')
    else:
        after = status['basis']
    schema = publisher.client.query('[:find (pull ?a [* {:db/valueType [:db/ident]} {:db/cardinality [:db/ident]}])'
        ' :in $ [?i ...] :where [?a :db/ident ?i]]', [[kw(COVERAGE), kw('question.difficulty/unobserved')]],
        directory, 'schema-readback', after)
    declaration = next((r[0] for r in schema if str(r[0][':db/ident']) == COVERAGE), {})
    if len(schema) != 2 or _enum(declaration.get(':db/valueType')) != ':db.type/ref' or _enum(declaration.get(':db/cardinality')) != ':db.cardinality/many':
        raise ValueError('Coverage schema readback differs from many/ref declaration')
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
    print(json.dumps(migrate_coverage(publisher, args.directory, apply=args.apply, source=args.source), sort_keys=True))


if __name__ == '__main__':
    main()
