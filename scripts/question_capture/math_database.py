"""Attributed, retry-safe imports into the math database."""
import hashlib
import json
from pathlib import Path

from core import ALLOWED, atomic_json
from edn import dumps, kw, loads
from math_content import build_math_content, resolve_knowledge_points

SOURCE = ':org/Math-Academy'


def digest(content):
    return hashlib.sha256(json.dumps(content, sort_keys=True, default=str).encode()).hexdigest()


def import_directory(directory, args=None):
    # Old receipts belong to course-academy-v2 and must never be replayed in math.
    name = 'edb-import-math' if getattr(args, 'source', None) else 'edb-import'
    return Path(directory) / name


def validate_receipt(receipt, attributes, source_id, retractions, immutable_answers=(), immutable_fields=()):
    from activities import ACTIVITY_ATTRIBUTES
    allowed = ALLOWED | set(ACTIVITY_ATTRIBUTES)
    names = {a: str(name) for a, name in attributes}
    approved = {dumps(r) for r in retractions}
    actual = set()
    old_answers = set(immutable_answers)
    old_fields = {(e, str(a)) for e, a in immutable_fields}
    for row in receipt[':edb/tx-data']:
        if len(row) != 6 or row[4] != source_id or type(row[5]) is not bool:
            raise ValueError('Every math transaction fact must have the Math Academy source')
        attribute = names.get(row[1], '')
        if attribute != ':db/txInstant' and attribute.lstrip(':') not in allowed:
            raise ValueError('Transaction changes non-content facts: ' + attribute)
        if row[5] is False:
            signature = dumps([row[0], kw(attribute), row[2]])
            if signature not in approved:
                raise ValueError('Transaction contains an unapproved retraction: ' + signature)
            actual.add(signature)
        if row[0] in old_answers and attribute in (':answer/id', ':answer/type', ':answer/value'):
            raise ValueError('Transaction changes an existing answer value')
        if (row[0], attribute) in old_fields:
            raise ValueError('Transaction changes an existing answer-field definition')
    if actual != approved:
        raise ValueError('Transaction did not perform exactly its planned retractions')


def plan(db, prepared, directory, basis):
    from activities import load_activity_snapshot, build_activity_transaction
    topics = db.content_topics(prepared, directory, basis)
    records = prepared.get('questions', []) + prepared.get('canonical_examples', [])
    existing = db.questions([q['math_academy_id'] for q in records], directory, basis=basis)
    resolved = resolve_knowledge_points(prepared, topics, existing)
    transaction, report = build_math_content(resolved, topics, existing)
    snapshot = load_activity_snapshot(db, resolved, directory, basis)
    forms, structures = build_activity_transaction(resolved, topics, snapshot, transaction)
    transaction.extend(forms)
    retractions = report['retractions'] + structures.get('retractions', [])
    retractions = list({dumps(r): r for r in retractions}.values())
    immutable_answers = sorted({a[':db/id'] for q in existing.values()
        for f in q.get(':question/answer-fields', []) for a in f.get(':answer-field/choices', [])})
    immutable_fields = [[f[':db/id'], kw(attr)] for q in existing.values()
        for f in q.get(':question/answer-fields', []) for attr in
        ('answer-field/id', 'answer-field/key', 'answer-field/type', 'answer-field/correct', 'answer-field/choices') if ':' + attr in f]
    return transaction, {'retractions': retractions, 'immutable_answers': immutable_answers,
        'immutable_fields': immutable_fields, 'questions': report['questions'], 'structures': structures}


def verify(db, receipt, prepared, raw_hash, directory, guards, source_id):
    before, after = receipt[':edb/db-before-t'], receipt[':edb/db-after-t']
    attributes = db.attributes(directory, before)
    validate_receipt(receipt, attributes, source_id, guards['retractions'],
                     guards['immutable_answers'], guards['immutable_fields'])
    remaining, _ = plan(db, prepared, directory / 'after', after)
    if remaining:
        raise ValueError('Committed source content does not reconcile to an idempotent import')
    ids = [q['math_academy_id'] for q in prepared.get('questions', []) + prepared.get('canonical_examples', [])]
    identity_attrs = {a for a, name in attributes if name == ':question/math-academy-id'}
    added = sorted({str(d[2]) for d in receipt[':edb/tx-data'] if d[1] in identity_attrs and d[-1] is True})
    result = {'committed': True, 'database': db.args.database, 'source': SOURCE,
              'basis_before': before, 'basis_after': after, 'content_sha256': raw_hash,
              'prepared_content_sha256': digest(prepared), 'question_count': len(ids),
              'imported_question_ids': ids, 'new_question_ids': added, 'new_question_count': len(added),
              'verification_method': 'source_receipt_and_content_replan',
              'learner_and_engine_facts_unchanged': True, 'reimport_is_noop': True}
    atomic_json(directory / 'verification.json', result)
    return result


def import_math(db, content, directory, apply=True):
    from authoritative import prepare_authoritative_content, AuthoritativeReview
    from image_library import ImageLibrary
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    if db.args.source != SOURCE:
        raise ValueError('Original MA captures require :org/Math-Academy as transaction source')
    raw_hash = digest(content)
    intent_path = directory / 'commit-intent.json'
    tx_path = directory / 'transaction.edn'
    prepared_path = directory / 'prepared-content.json'
    guard_path = directory / 'reconciliation.edn'
    if intent_path.exists():
        intent = json.loads(intent_path.read_text())
        if (intent.get('database') != db.args.database or intent.get('endpoint') != db.args.endpoint or
                intent.get('source') != SOURCE or intent.get('content_sha256') != raw_hash):
            raise ValueError('Exact retry requires its original database, endpoint, source, and captured content')
        if (hashlib.sha256(tx_path.read_bytes()).hexdigest() != intent['sha256'] or
                hashlib.sha256(guard_path.read_bytes()).hexdigest() != intent['reconciliation_sha256']):
            raise ValueError('Saved transaction or validation differs from its original intent')
        prepared = json.loads(prepared_path.read_text())
        if digest(prepared) != intent['prepared_content_sha256']:
            raise ValueError('Prepared content differs from its original intent')
        if not apply:
            return {'pending_commit': True, 'database_writes': 0, **intent}
        receipt = db._commit(intent, tx_path, directory)
        if receipt[':edb/db-before-t'] != intent['basis']:
            raise ValueError('Commit receipt differs from its original basis')
        return verify(db, receipt, prepared, raw_hash, directory, loads(guard_path.read_text()), intent['source_eid'])
    prepared, review = prepare_authoritative_content(content, directory.parent)
    atomic_json(directory / 'answer-review.json', review)
    if review.get('held_questions'):
        raise AuthoritativeReview('MA answer evidence is incomplete; see ' + str(directory / 'answer-review.json'))
    prepared = ImageLibrary(Path(db.args.math_root)).prepare_content(prepared, directory.parent)
    atomic_json(prepared_path, prepared)
    basis = db.basis()
    sources = db.query('[:find ?e :where [?e :db/ident :org/Math-Academy]]', [], directory, 'source', basis)
    if len(sources) != 1:
        raise ValueError('math must already contain the :org/Math-Academy source entity')
    source_id = sources[0][0]
    transaction, guards = plan(db, prepared, directory, basis)
    atomic_json(directory / 'matching-report.json', guards['questions'])
    atomic_json(directory / 'activity-report.json', guards['structures'])
    guard_path.write_text(dumps(guards) + '\n')
    if not transaction:
        result = {'database_writes': 0, 'already_complete': True, 'database': db.args.database,
                  'source': SOURCE, 'basis': basis, 'content_sha256': raw_hash,
                  'prepared_content_sha256': digest(prepared)}
        atomic_json(directory / 'verification.json', result)
        return result
    tx_path.write_text(dumps(transaction) + '\n')
    preview_text = db.command('with', '--file', tx_path, '--source', SOURCE)
    (directory / 'preview.edn').write_text(preview_text)
    preview = loads(preview_text)
    if preview[':edb/db-before-t'] != basis:
        raise ValueError('Database changed during planning; rerun before any commit')
    attributes = db.attributes(directory, basis)
    validate_receipt(preview, attributes, source_id, guards['retractions'],
                     guards['immutable_answers'], guards['immutable_fields'])
    result = {'previewed': True, 'database': db.args.database, 'source': SOURCE, 'basis': basis,
              'transaction_entities': len(transaction), 'database_writes': 0}
    atomic_json(directory / 'preview.json', result)
    if not apply:
        return result
    tx_hash = hashlib.sha256(tx_path.read_bytes()).hexdigest()
    intent = {'database': db.args.database, 'endpoint': db.args.endpoint, 'basis': basis,
              'source': SOURCE, 'source_eid': source_id, 'sha256': tx_hash, 'content_sha256': raw_hash,
              'prepared_content_sha256': digest(prepared),
              'request_key': 'ma-source-capture-' + str(basis) + '-' + tx_hash,
              'reconciliation_sha256': hashlib.sha256(guard_path.read_bytes()).hexdigest()}
    atomic_json(intent_path, intent)
    receipt = db._commit(intent, tx_path, directory)
    return verify(db, receipt, prepared, raw_hash, directory, guards, source_id)
