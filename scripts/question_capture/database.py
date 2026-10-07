"""EDB reads, transaction previews, durable retry intents, and verification."""
import hashlib
import json
import os
import re
import subprocess
from collections import defaultdict
from datetime import datetime
from pathlib import Path

from core import ALLOWED, ROOT, atomic_json, build_content_transaction, journal
from edn import dumps, kw, loads
from provenance import Reconciler, ReconciliationReview, authoring_records, source_records, field_value, value_hash

QUESTION_PULL = '''[* {:question/difficulty [:db/id :db/ident]}
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

    def query(self, query, inputs, directory, name, basis=None, history=False):
        directory = Path(directory)
        directory.mkdir(parents=True, exist_ok=True)
        source, input_file = directory / (name + '-query.edn'), directory / (name + '-inputs.edn')
        source.write_text(query)
        input_file.write_text(dumps(inputs))
        options = ['--file', source, '--inputs', input_file]
        if basis is not None:
            options += ['--as-of', basis]
        if history:
            options += ['--history']
        result = self.command('query', *options)
        (directory / (name + '.edn')).write_text(result)
        return loads(result)

    def priorities(self, learner_id, directory, topic_ids=None, knowledge_snapshot=None):
        # learner/id is a string even when the identifier looks like a UUID.
        rows = self.query(PRIORITY_QUERY, [str(learner_id)], directory, 'priorities')
        # Multiple task records can refer to a topic; keep its highest stored score.
        scores = {topic: max(r[2] for r in rows if r[0] == topic) for topic, _, _ in rows}
        if topic_ids:
            from priorities import capture_scores
            context = self.capture_priority_context(learner_id,Path(directory)/'capture-priorities')
            snapshot = json.loads(Path(knowledge_snapshot).read_text()) if knowledge_snapshot else None
            report = capture_scores(topic_ids,context,snapshot)
            atomic_json(Path(directory)/'capture-priorities.json', {
                'source':'directed targets and assignments; remote availability; no personal task eligibility',
                'knowledge_snapshot':str(knowledge_snapshot) if knowledge_snapshot else None,
                'context_basis':context['basis'],'topics':report})
            scores.update({mid:item['priority'] for mid,item in report.items()})
        return scores

    def capture_priority_context(self, learner_id, directory):
        """Read configuration and curriculum once per batch; never write learner state."""
        from priorities import assignment_topics
        if hasattr(self,'_capture_priority_context'):
            return self._capture_priority_context
        basis = self.basis()
        def content_pattern(depth):
            base = '[:db/id {:assigned-problem/topic-coverage [:topic/math-academy-id]}'
            if depth:
                inner = content_pattern(depth-1)
                base += ' {:assigned-problem/content '+inner+'} {:multistep/steps [{:step/content '+inner+'}]}'
            return base+']'
        query = '''[:find (pull ?l [:learner/self-directed
          {:learner/targets [:topic/math-academy-id]}
          {:learner/activity [{:learner-task/status [:db/ident]} {:learner-task/activity [:db/id]}]}
          {:learner/assignments [:db/id :activity/title :activity/due
            {:activity/steps [{:step/content '''+content_pattern(3)+'''}]}]}])
          :in $ ?id :where [?l :learner/id ?id]]'''
        learners = self.query(query,[str(learner_id)],directory,'configuration',basis)
        if len(learners)!=1:
            raise ValueError('Expected one learner configuration for capture priorities')
        learner = learners[0][0]
        completed = {t[':learner-task/activity'][':db/id'] for t in learner.get(':learner/activity',[])
                     if t.get(':learner-task/status',{}).get(':db/ident') == ':learner-task.status/completed'}
        assignments = []
        for assignment in learner.get(':learner/assignments',[]):
            due = assignment.get(':activity/due')
            assignments.append({'topics':assignment_topics(assignment),'due':due if isinstance(due,datetime)
                else datetime.fromisoformat(due.replace('Z','+00:00')) if due else None,
                'completed':assignment[':db/id'] in completed})
        ids = [r[0] for r in self.query('[:find ?mid :where [_ :topic/math-academy-id ?mid]]',
                                       [],directory,'topic-ids',basis)]
        query = '''[:find (pull ?t [:topic/math-academy-id
          {:topic/next [:topic/math-academy-id]}
          {:topic/knowledge-points [{:knowledge-point/key-prerequisites [:topic/math-academy-id]}]}])
          :in $ [?mid ...] :where [?t :topic/math-academy-id ?mid]]'''
        prerequisites = defaultdict(set)
        for start in range(0,len(ids),200):
            for row in self.query(query,[ids[start:start+200]],directory,'graph-'+str(start),basis):
                topic = row[0]; mid = topic[':topic/math-academy-id']
                for after in topic.get(':topic/next',[]):
                    prerequisites[after[':topic/math-academy-id']].add(mid)
                for kp in topic.get(':topic/knowledge-points',[]):
                    prerequisites[mid].update(t[':topic/math-academy-id'] for t in kp.get(':knowledge-point/key-prerequisites',[]))
        self._capture_priority_context = {'basis':basis,'self_directed':learner.get(':learner/self-directed',False),
            'targets':[t[':topic/math-academy-id'] for t in learner.get(':learner/targets',[])],
            'assignments':assignments,'prerequisites':dict(prerequisites)}
        return self._capture_priority_context

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
        # Protect all non-content domain facts, including engine configuration,
        # weights, policies and activity data whose namespaces may expand.
        ids = [a for a, ident in attributes if str(ident)[1:] not in ALLOWED and not str(ident).startswith(':db/')]
        # Bind one scalar attribute before scanning. A collection binding can
        # allocate the broad EAV relation before joining, even for small lists.
        # Every read uses the same immutable basis; no protected facts are omitted.
        rows = []
        for attribute in sorted(set(ids)):
            stop = getattr(self.args, 'stop_event', None)
            if stop is not None and stop.is_set():
                raise KeyboardInterrupt('Stopped during protected-fact verification')
            try:
                part = self.query('[:find ?e ?a ?v :in $ ?a :where [?e ?a ?v]]',
                                  [attribute], directory, name+'-'+str(attribute), basis)
            except subprocess.CalledProcessError as error:
                if 'query/value-byte-limit' not in (error.stderr or ''):
                    raise
                # Large text attributes need entity-bounded reads as well.
                # Enumerating just subjects avoids allocating their text values.
                subjects = sorted(r[0] for r in self.query(
                    '[:find ?e :in $ ?a :where [?e ?a]]',[attribute],directory,
                    name+'-'+str(attribute)+'-subjects',basis))
                def read_subjects(group):
                    if stop is not None and stop.is_set():
                        raise KeyboardInterrupt('Stopped during protected-fact verification')
                    label=name+'-'+str(attribute)+'-entities-'+str(group[0])+'-'+str(group[-1])
                    try:
                        values=self.query('[:find ?e ?a ?v :in $ ?a [?e ...] :where [?e ?a ?v]]',
                                          [attribute,group],directory,label,basis)
                    except subprocess.CalledProcessError as failure:
                        if 'query/value-byte-limit' not in (failure.stderr or '') or len(group)==1:
                            raise
                        middle=len(group)//2
                        return read_subjects(group[:middle])+read_subjects(group[middle:])
                    if {r[0] for r in values} != set(group) or any(r[1]!=attribute for r in values):
                        raise ValueError('Incomplete protected-fact entity partition')
                    return values
                part=[]
                for offset in range(0,len(subjects),64):
                    part.extend(read_subjects(subjects[offset:offset+64]))
            rows.extend(part)
        (Path(directory)/(name+'.edn')).write_text(dumps(rows)+'\n')
        return rows

    def validate_datoms(self, receipt, attributes, retractions=(), immutable_answers=(), immutable_fields=()):
        allowed = {a for a, ident in attributes if str(ident)[1:] in ALLOWED or ident == ':db/txInstant'}
        names = dict(attributes)
        approved = {dumps(r) for r in retractions}
        actual = set()
        field_facts = {(e, str(a)) for e,a in immutable_fields}
        for row in receipt[':edb/tx-data']:
            if row[1] not in allowed:
                raise ValueError('Preview/receipt contains a non-content attribute')
            if row[-1] is not True:
                signature = dumps([row[0], names[row[1]], row[2]])
                if row[-1] is not False or signature not in approved:
                    raise ValueError('Preview/receipt contains an unapproved retraction')
                actual.add(signature)
            if row[0] in immutable_answers and names[row[1]] in (':answer/id', ':answer/type', ':answer/value'):
                raise ValueError('Preview/receipt mutates a preexisting answer entity')
            if (row[0], str(names[row[1]])) in field_facts:
                raise ValueError('Preview/receipt mutates a preexisting field definition')
        if actual != approved:
            raise ValueError('Preview/receipt did not perform the approved replacements')

    def reconciliation(self, content, directory, existing, basis):
        ids = set(existing)
        records = authoring_records(ROOT/'reference/mathacademy', ids)
        # A later exact MA capture of a locally authored value makes that value
        # authoritative too. Do not overwrite it as if it were still invented.
        for capture in (ROOT/'reference/mathacademy/question-capture').glob('*/content.json'):
            verification = capture.parent/'edb-import/verification.json'
            if not verification.exists():
                continue
            proof = json.loads(verification.read_text())
            if not proof.get('committed'):
                continue
            saved = json.loads(capture.read_text())
            saved = {**saved, 'questions':[q for q in saved.get('questions', []) if q['math_academy_id'] in ids],
                     'canonical_examples':[q for q in saved.get('canonical_examples', []) if q['math_academy_id'] in ids]}
            if not saved['questions'] and not saved['canonical_examples']:
                continue
            for r in source_records(saved, capture.parent):
                if r['category'].startswith('ma_') and r['attribute'] != 'answer-field/choices':
                    records.append({**r, 'basis':proof['basis_after'], 'verification':str(verification)})
                elif r['category'] == 'ma_complete_choices':
                    for kind, value in r['value']:
                        records.append({**r, 'attribute':'answer/value', 'value':[kw('answer.type/'+kind), value],
                                        'category':'ma_capture', 'basis':proof['basis_after'], 'verification':str(verification)})
        snapshots = {}
        for t in sorted({r['basis'] for r in records if r['basis'] <= basis}):
            mids = sorted({r['question'] for r in records if r['basis'] == t})
            snapshots[t] = self.questions(mids, directory/'evidence', 'basis-'+str(t), t)
        attested = []
        for r in records:
            old = snapshots.get(r['basis'], {}).get(r['question'])
            current = existing.get(r['question'])
            if not old or not current or old[':question/id'] != current[':question/id']:
                continue
            if r['field'] is None:
                value = old.get(':'+r['attribute'])
                if r['attribute'] == 'question/difficulty':
                    value = (value or {}).get(':db/ident')
            else:
                fields = [f for f in old.get(':question/answer-fields', []) if f[':answer-field/key'] == r['field']]
                current_fields = [f for f in current.get(':question/answer-fields', []) if f[':answer-field/key'] == r['field']]
                if len(fields) != 1 or len(current_fields) != 1 or fields[0][':db/id'] != current_fields[0][':db/id']:
                    continue
                f = fields[0]
                if r['attribute'] == 'answer/value':
                    values = [[a[':answer/type'][':db/ident'], a[':answer/value']] for a in f[':answer-field/choices']]
                    value = next((v for v in values if value_hash(v) == value_hash(r['value'])), None)
                else:
                    value = field_value(f, r['attribute'])
            if value_hash(value) == value_hash(r['value']):
                attested.append(r)
        usage = {mid: [] for mid in ids}
        retention = []
        if ids:
            retention = self.query('[:find ?ident :in $ [?ident ...] :where [?a :db/ident ?ident] [?a :db/noHistory true]]',
                [[kw(a) for a in ('task-item/content','task-item/responses','question/answer-fields','answer-field/choices',
                                 'question/problem','question/worked-solution','question/difficulty')]],
                directory, 'usage-retention', basis)
            if retention:
                for mid in ids:
                    usage[mid].append({'kind':'unavailable_history', 'attributes':retention})
            # Query retained history, including responses or presentations later
            # retracted. Historical joins include detached field ownership.
            for name, where in [('presentations', '[?item :task-item/content ?q ?tx true]'),
                ('responses', '[?q :question/answer-fields ?f] [?f :answer-field/choices ?a] [?item :task-item/responses ?a ?tx true]')]:
                rows = self.query('[:find ?mid ?item :in $ [?mid ...] :where [?q :question/math-academy-id ?mid] '+where+']',
                                  [sorted(ids)], directory, 'historical-'+name, basis, history=True)
                for mid, item in rows:
                    usage[mid].append({'kind':name, 'entity':item})
        return Reconciler(attested, source_records(content, directory.parent), basis, usage, [r[0] for r in retention])

    def replacement_guards(self, reconciler, existing):
        retractions = []
        for d in reconciler.decisions:
            if d.get('action') != 'replace':
                continue
            q = existing[d['question']]
            attr = d['attribute']
            if attr in ('question/problem', 'question/worked-solution', 'question/difficulty'):
                value = q[':'+attr]
                if attr == 'question/difficulty':
                    value = value[':db/id']
                retractions.append([q[':db/id'], kw(attr), value])
            elif attr == 'question/answer-fields':
                f = next(f for f in q[':question/answer-fields'] if
                         f[':db/id'] == d.get('previous_field_id') or f[':answer-field/key'] == d['field'])
                retractions.append([q[':db/id'], kw(attr), f[':db/id']])
        return retractions

    def content_topics(self, content, directory, basis):
        if content.get('task_type') in ('assessment','multistep'):
            ids = {q['topic_id'] for q in content['questions']}
            if not ids or any(not isinstance(t,int) or t < 1 for t in ids):
                raise ValueError('Assessment questions require source topic IDs')
            return {tid:self.topic(tid,Path(directory)/'topics'/str(tid),basis) for tid in sorted(ids)}
        return {content['topic_id']:self.topic(content['topic_id'],directory,basis)}

    def import_content(self, content, directory, apply=True):
        # Another app may transact between our read and preview. Replan this
        # pre-commit race locally rather than spending a model repair turn.
        for attempt in range(3):
            try:
                return self._import_content(content,directory,apply)
            except ValueError as error:
                if str(error) != 'Database changed during planning; rerun before any commit' or attempt == 2:
                    raise

    def _import_content(self, content, directory, apply=True):
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
            if intent.get('reconciliation_sha256') and hashlib.sha256((directory/'reconciliation.edn').read_bytes()).hexdigest() != intent['reconciliation_sha256']:
                raise ValueError('Saved reconciliation differs from its original intent')
            if not apply:
                return intent
            receipt = self._commit(intent, tx_path, directory)
            return self._verify(receipt, content, directory)
        basis = self.basis()
        topics = self.content_topics(content, directory, basis)
        ids = [q['math_academy_id'] for q in content['questions'] + content.get('canonical_examples', [])]
        existing = self.questions(ids, directory, basis=basis)
        reconciler = self.reconciliation(content, directory, existing, basis)
        planning_error = None
        try:
            transaction, report = build_content_transaction(content, topics, existing, reconciler)
        except ValueError as error:
            planning_error = str(error)
            raise
        finally:
            atomic_json(directory/'replacement-report.json', {'basis':basis, 'decisions':reconciler.decisions,
                        'review_required':reconciler.needs_review or planning_error is not None,
                        'planning_error':planning_error, 'database_writes':0})
        atomic_json(directory / 'matching-report.json', report)
        if reconciler.needs_review:
            raise ReconciliationReview('Content provenance needs review: '+str(directory/'replacement-report.json'))
        retractions = self.replacement_guards(reconciler, existing)
        immutable_answers = sorted({a[':db/id'] for q in existing.values() for f in q.get(':question/answer-fields', []) for a in f.get(':answer-field/choices', [])})
        immutable_fields = sorted([f[':db/id'],kw(attr)] for q in existing.values() for f in q.get(':question/answer-fields', [])
            for attr in ('answer-field/id','answer-field/key','answer-field/type','answer-field/correct') if ':'+attr in f)
        frozen = {'authored':reconciler.authored, 'sources':reconciler.sources, 'usage':reconciler.usage,
                  'basis':basis, 'retractions':retractions, 'immutable_answers':immutable_answers,
                  'immutable_fields':immutable_fields, 'no_history':sorted(reconciler.no_history)}
        (directory/'reconciliation.edn').write_text(dumps(frozen)+'\n')
        if not transaction:
            result = {'database_writes': 0, 'already_complete': True, 'content_sha256':content_hash}
            atomic_json(directory / 'verification.json', result)
            return result
        tx_path.write_text(dumps(transaction) + '\n')
        preview_text = self.command('with', '--file', tx_path)
        (directory / 'preview.edn').write_text(preview_text)
        preview = loads(preview_text)
        if preview[':edb/db-before-t'] != basis:
            raise ValueError('Database changed during planning; rerun before any commit')
        attributes = self.attributes(directory, basis)
        self.validate_datoms(preview, attributes, retractions, immutable_answers, immutable_fields)
        result = {'previewed': True, 'basis': basis, 'transaction_entities': len(transaction), 'database_writes': 0}
        atomic_json(directory / 'preview.json', result)
        if not apply:
            return result
        digest = hashlib.sha256(tx_path.read_bytes()).hexdigest()
        intent = {'database': self.args.database, 'endpoint': self.args.endpoint, 'basis': basis,
                  'sha256': digest, 'content_sha256':content_hash, 'request_key': 'ma-question-capture-' + digest,
                  'reconciliation_sha256':hashlib.sha256((directory/'reconciliation.edn').read_bytes()).hexdigest()}
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
        intent_path = directory/'commit-intent.json'
        intent = json.loads(intent_path.read_text()) if intent_path.exists() else {}
        if intent and before != intent['basis']:
            raise ValueError('Receipt basis differs from original intent')
        frozen = loads((directory/'reconciliation.edn').read_text()) if intent.get('reconciliation_sha256') else {}
        attributes = self.attributes(directory, before)
        self.validate_datoms(receipt, attributes, frozen.get('retractions', []), frozen.get('immutable_answers', []), frozen.get('immutable_fields', []))
        # EDB's committed receipt lists every actual assertion and retraction,
        # including derived changes. validate_datoms rejects non-content effects;
        # scanning the entire database again adds no per-import protection.
        topics_after = self.content_topics(content, directory / 'after', after)
        ids = [q['math_academy_id'] for q in content['questions'] + content.get('canonical_examples', [])]
        questions_after = self.questions(ids, directory, 'questions-after', after)
        reconciler = Reconciler(frozen.get('authored', []), frozen.get('sources', []), after, frozen.get('usage', {}), frozen.get('no_history', [])) if frozen else None
        remaining, _ = build_content_transaction(content, topics_after, questions_after, reconciler)
        if remaining or reconciler and reconciler.needs_review:
            raise ValueError('Committed content does not reconcile to an idempotent import')
        result = {'committed': True, 'basis_before': before, 'basis_after': after,
                  'content_sha256':hashlib.sha256(json.dumps(content,sort_keys=True,default=str).encode()).hexdigest(),
                  'question_count': len(ids),
                  'verification_method': 'committed_transaction_and_content',
                  'learner_and_engine_facts_unchanged': True, 'reimport_is_noop': True}
        atomic_json(directory / 'verification.json', result)
        if frozen:
            report_path = directory/'replacement-report.json'
            report = json.loads(report_path.read_text())
            report.update(transaction_receipt=str(directory/'commit.edn'), basis_after=after, committed=True)
            for decision in report['decisions']:
                decision.update(transaction_receipt=str(directory/'commit.edn'), basis_after=after)
            atomic_json(report_path, report)
        return result
