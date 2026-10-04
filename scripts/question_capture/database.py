"""EDB reads, transaction previews, durable retry intents, and verification."""
import hashlib
import json
import os
import re
import subprocess
from pathlib import Path

from core import ALLOWED, atomic_json, build_transaction, journal
from edn import dumps, kw, loads

QUESTION_PULL = '''[* {:question/difficulty [:db/ident]}
 {:knowledge-point/_questions [:knowledge-point/id :knowledge-point/title]}
 {:knowledge-point/_canonical-example [:knowledge-point/id :knowledge-point/title]}
 {:question/answer-fields [* {:answer-field/type [:db/ident]}
 {:answer-field/correct [* {:answer/type [:db/ident]}]}
 {:answer-field/choices [* {:answer/type [:db/ident]}]}]}]'''
TOPIC_QUERY = '''[:find (pull ?topic [:topic/id :topic/title :topic/math-academy-id
 {:topic/knowledge-points [:knowledge-point/id :knowledge-point/title
 {:knowledge-point/canonical-example [:question/id :question/math-academy-id]}
 {:knowledge-point/questions [:question/id :question/math-academy-id]}]}])
 :in $ ?id :where [?topic :topic/math-academy-id ?id]]'''
PRIORITY_QUERY = '''[:find ?topic-id ?title ?priority
 :in $ ?learner-id
 :where [?learner :learner/id ?learner-id]
 [?learner :learner/activity ?task]
 [?task :learner-task/status :learner-task.status/unlocked]
 [?task :learner-task/priority ?priority]
 [?task :learner-task/activity ?activity]
 [?activity :activity/type :activity.type/lesson]
 [?activity :activity/scope ?topic]
 [?topic :topic/math-academy-id ?topic-id]
 [?topic :topic/title ?title]]'''
PROTECTED_PREFIXES = ('learner/', 'learner-task/', 'task-item/', 'progress/',
                      'performance/', 'policy/', 'question-weights/')


def fingerprint(rows):
    return hashlib.sha256('\n'.join(sorted(dumps(r) for r in rows)).encode()).hexdigest()


class Database:
    def __init__(self, args):
        self.args = args
        self.env = os.environ.copy()
        self.env.setdefault('EDB_POSTGRES_URL', 'host=/home/jake/Developer/Course_Academy/.local/edb/run dbname=course_academy user=edb_peer sslmode=disable')

    def command(self, command, *options):
        return subprocess.run([self.args.edb_bin, command, '--database', self.args.database, *map(str, options)],
                              env=self.env, check=True, capture_output=True, text=True, timeout=210).stdout

    def basis(self):
        result = self.command('status')
        match = re.search(r'\bbasis_t=(\d+)', result)
        if not match:
            raise ValueError('Could not determine EDB basis')
        return int(match[1])

    def query(self, query, inputs, directory, name, basis=None):
        directory = Path(directory)
        directory.mkdir(parents=True, exist_ok=True)
        source, input_file = directory / (name + '-query.edn'), directory / (name + '-inputs.edn')
        source.write_text(query)
        input_file.write_text(dumps(inputs))
        options = ['--file', source, '--inputs', input_file]
        if basis is not None:
            options += ['--as-of', basis]
        result = self.command('query', *options)
        (directory / (name + '.edn')).write_text(result)
        return loads(result)

    def priorities(self, learner_id, directory):
        rows = self.query(PRIORITY_QUERY, [learner_id], directory, 'priorities')
        # A topic can have multiple eligible task records; use its highest rating.
        return {topic: max(r[2] for r in rows if r[0] == topic) for topic, _, _ in rows}

    def topic(self, topic_id, directory, basis=None):
        rows = self.query(TOPIC_QUERY, [topic_id], directory, 'topic', basis)
        if len(rows) != 1:
            raise ValueError('Expected exactly one database topic: ' + str(topic_id))
        return rows[0][0]

    def questions(self, ids, directory, name='questions', basis=None):
        if not ids:
            return {}
        rows = self.query('[:find (pull ?q ' + QUESTION_PULL + ') :in $ [?id ...] :where [?q :question/math-academy-id ?id]]',
                          [ids], directory, name, basis)
        return {row[0][':question/math-academy-id']: row[0] for row in rows}

    def attributes(self, directory, basis):
        return self.query('[:find ?a ?ident :where [?a :db/ident ?ident] [?a :db/valueType _]]', [], directory, 'attributes', basis)

    def protected(self, attributes, directory, name, basis):
        ids = [a for a, ident in attributes if str(ident)[1:].startswith(PROTECTED_PREFIXES)]
        return self.query('[:find ?e ?a ?v :in $ [?a ...] :where [?e ?a ?v]]', [ids], directory, name, basis)

    def validate_datoms(self, receipt, attributes):
        allowed = {a for a, ident in attributes if str(ident)[1:] in ALLOWED or ident == ':db/txInstant'}
        for row in receipt[':edb/tx-data']:
            if row[1] not in allowed or row[-1] is not True:
                raise ValueError('Preview/receipt contains a retraction or non-content attribute')

    def import_content(self, content, directory, apply=True):
        directory = Path(directory)
        directory.mkdir(parents=True, exist_ok=True)
        content_hash = hashlib.sha256(json.dumps(content,sort_keys=True,default=str).encode()).hexdigest()
        intent_path, tx_path = directory / 'commit-intent.json', directory / 'transaction.edn'
        if intent_path.exists():
            # A timeout/interrupt may have committed. Never replan an unresolved intent.
            intent = json.loads(intent_path.read_text())
            if hashlib.sha256(tx_path.read_bytes()).hexdigest() != intent['sha256']:
                raise ValueError('Saved transaction differs from its original intent')
            if content_hash != intent['content_sha256']:
                raise ValueError('Retry must use the original captured content')
            if intent['database'] != self.args.database or intent['endpoint'] != self.args.endpoint:
                raise ValueError('Retry must use the original database and endpoint')
            if not apply:
                return intent
            receipt = self._commit(intent, tx_path, directory)
            return self._verify(receipt, content, directory)
        basis = self.basis()
        topic = self.topic(content['topic_id'], directory, basis)
        ids = [q['math_academy_id'] for q in content['questions'] + content.get('canonical_examples', [])]
        existing = self.questions(ids, directory, basis=basis)
        transaction, report = build_transaction(content, topic, existing)
        atomic_json(directory / 'matching-report.json', report)
        if not transaction:
            result = {'database_writes': 0, 'already_complete': True}
            atomic_json(directory / 'verification.json', result)
            return result
        tx_path.write_text(dumps(transaction) + '\n')
        preview_text = self.command('with', '--file', tx_path)
        (directory / 'preview.edn').write_text(preview_text)
        preview = loads(preview_text)
        if preview[':edb/db-before-t'] != basis:
            raise ValueError('Database changed during planning; rerun before any commit')
        attributes = self.attributes(directory, basis)
        self.validate_datoms(preview, attributes)
        result = {'previewed': True, 'basis': basis, 'transaction_entities': len(transaction), 'database_writes': 0}
        atomic_json(directory / 'preview.json', result)
        if not apply:
            return result
        digest = hashlib.sha256(tx_path.read_bytes()).hexdigest()
        intent = {'database': self.args.database, 'endpoint': self.args.endpoint, 'basis': basis,
                  'sha256': digest, 'content_sha256':content_hash, 'request_key': 'ma-question-capture-' + digest}
        atomic_json(intent_path, intent)
        receipt = self._commit(intent, tx_path, directory)
        return self._verify(receipt, content, directory)

    def _commit(self, intent, tx_path, directory):
        receipt_path = directory / 'commit.edn'
        if receipt_path.exists():
            try:
                previous = loads(receipt_path.read_text())
            except (ValueError,IndexError):
                previous = {}  # Truncated receipt: retry the exact saved request.
            if previous.get(':edb/committed') is True:
                return previous
        journal(directory / 'events.jsonl', 'commit_requested', **intent)
        text = self.command('transact', '--file', tx_path, '--endpoint', intent['endpoint'],
                            '--request-key', intent['request_key'], '--basis', intent['basis'], '--timeout-ms', 180000)
        receipt_path.write_text(text)
        receipt = loads(text)
        if receipt.get(':edb/committed') is not True:
            raise ValueError('Commit not confirmed. Retain and retry the exact saved intent.')
        return receipt

    def _verify(self, receipt, content, directory):
        before, after = receipt[':edb/db-before-t'], receipt[':edb/db-after-t']
        attributes = self.attributes(directory, before)
        self.validate_datoms(receipt, attributes)
        protected_before = self.protected(attributes, directory, 'protected-before', before)
        protected_after = self.protected(attributes, directory, 'protected-after', after)
        if fingerprint(protected_before) != fingerprint(protected_after):
            raise ValueError('Protected learner/engine facts changed in the committed transaction')
        topic_after = self.topic(content['topic_id'], directory / 'after', after)
        ids = [q['math_academy_id'] for q in content['questions'] + content.get('canonical_examples', [])]
        questions_after = self.questions(ids, directory, 'questions-after', after)
        remaining, _ = build_transaction(content, topic_after, questions_after)
        if remaining:
            raise ValueError('Committed content still has missing captured facts')
        result = {'committed': True, 'basis_before': before, 'basis_after': after,
                  'question_count': len(ids), 'protected_fact_count': len(protected_before),
                  'protected_facts_sha256': fingerprint(protected_before),
                  'learner_and_engine_facts_unchanged': True, 'reimport_is_noop': True}
        atomic_json(directory / 'verification.json', result)
        return result
