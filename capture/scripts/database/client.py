"""EDB CLI transport and reads pinned to one immutable database basis."""
from __future__ import annotations
import hashlib
import copy
from concurrent.futures import Future
import os
import re
import shlex
import subprocess
import tempfile
import threading
import uuid
from pathlib import Path
from .edn import dumps, loads, kw
from ..storage import atomic_text

QUESTION_PULL = '''[* {:question/difficulty [:db/id :db/ident]}
 {:knowledge-point/_questions [:db/id :knowledge-point/id :knowledge-point/title]}
 {:knowledge-point/_canonical-example [:db/id :knowledge-point/id :knowledge-point/title]}
 {:question/answer-fields [* {:answer-field/type [:db/id :db/ident]}
 {:answer-field/correct [* {:answer/type [:db/id :db/ident]}]}
 {:answer-field/choices [* {:answer/type [:db/id :db/ident]}
 {:task-item/_responses [:db/id]}]}]}]'''
CONTENT_PULL = '''[* {:knowledge-point/canonical-example [:db/id :question/id :question/math-academy-id]}
 {:assigned-problem/content [* {:multistep/steps [* {:step/content [:db/id :question/id :question/math-academy-id]}]}]}]'''
ACTIVITY_PULL = '[* {:activity/type [:db/id :db/ident]} {:activity/scope [:db/id :topic/id :topic/math-academy-id]} {:activity/steps [* {:step/content ' + CONTENT_PULL + '}]}]'

class StaleBasis(RuntimeError):
    pass


class EDBCommandError(subprocess.CalledProcessError):
    """Keep full transport diagnostics without putting argv on status cards."""
    def __str__(self):
        diagnostic = self.stderr or ''
        remote = re.search(r'^remote_code=([a-z][a-z0-9_.-]*/[a-z][a-z0-9_.-]*)$', diagnostic, re.M)
        code = re.search(r'\bcode=([a-z][a-z0-9_.-]*/[a-z][a-z0-9_.-]*)', diagnostic)
        reason = remote.group(1) if remote else code.group(1) if code else 'command failed'
        return f'EDB {self.cmd[1]}: {reason} (exit {self.returncode}; saved request retained)'


class SnapshotReads:
    """Reuse identical readonly queries within one immutable batch value."""
    def __init__(self, client, basis):
        self.client, self.basis = client, basis
        self.identity = client.status()
        self.cache, self.lock = {}, threading.Lock()

    def status(self):
        return dict(self.identity)

    def snapshot(self, content, directory, basis):
        if basis != self.basis:
            raise ValueError('Cached snapshot reads require their original basis')
        return EDBClient.snapshot(self, content, directory, basis)

    def query(self, source, inputs, directory, name, basis=None):
        from ..runtime import check_stop
        stop = getattr(self.client, 'stop_event', None)
        if stop is not None:
            check_stop(stop)
        if basis != self.basis:
            raise ValueError('Cached queries require an explicit matching basis')
        key = (source, dumps(inputs))
        with self.lock:
            owner = key not in self.cache
            future = self.cache.setdefault(key, Future())
        directory = Path(directory)
        directory.mkdir(parents=True, exist_ok=True)
        if owner:
            try:
                result = self.client.query(source, inputs, directory, name, basis)
                path = directory / (name + '.edn')
                text = path.read_text() if path.exists() else dumps(result)
                future.set_result((result, text))
            except BaseException as error:
                future.set_exception(error)
                raise
        result, text = future.result()
        if stop is not None:
            check_stop(stop)
        if not owner:
            atomic_text(directory / (name + '-query.edn'), source)
            atomic_text(directory / (name + '-inputs.edn'), dumps(inputs))
            atomic_text(directory / (name + '.edn'), text)
        # Pull structures may be enriched during preparation; never let one
        # activity mutate the cached value used to prepare another activity.
        return copy.deepcopy(result)


class EDBClient:
    def __init__(self, config, stop_event):
        self.config, self.stop_event = config, stop_event
        self.environment = os.environ.copy()
        if config.postgres_url:
            self.environment['EDB_POSTGRES_URL'] = config.postgres_url

    def command(self, command, *options, timeout=210):
        from ..runtime import StopRequested
        if self.stop_event.is_set():
            raise StopRequested()
        if getattr(self.config, 'capture_only', False) and command not in ('status', 'query', 'pull', 'with'):
            raise ValueError('Capture-only mode does not submit transactions')
        executable = self.config.edb_bin
        if command == 'with':
            executable = getattr(self.config, 'preview_bin', None)
            if executable is None:
                from .preview import preview_executable
                executable = preview_executable(self.config, self.stop_event)
        elif command == 'transact':
            from .preview import submission_executable
            executable = submission_executable(self.config, self.stop_event)
        args = [str(executable), command, '--database', str(self.config.database), *map(str, options)]
        result = subprocess.run(args, env=self.environment, capture_output=True, text=True, timeout=timeout)
        if result.returncode:
            # Only an explicit stale-basis rejection proves the saved request did not commit.
            diagnostic = result.stderr
            if re.search(r'(?:code=|remote_code=)postgres/stale-basis(?:\s|$)', diagnostic):
                raise StaleBasis(diagnostic)
            raise EDBCommandError(result.returncode, args, result.stdout, diagnostic)
        return result.stdout

    def status(self):
        """Read the immutable database lineage alongside its current basis."""
        lines = re.findall(r'^STATUS\s+(.+)$', self.command('status', timeout=30), re.M)
        if len(lines) != 1:
            raise ValueError('EDB status omitted an unambiguous database identity')
        pairs = [token.split('=', 1) for token in shlex.split(lines[0]) if '=' in token]
        for key in ('database', 'lineage', 'basis_t'):
            if sum(name == key for name, value in pairs) != 1:
                raise ValueError('EDB status omitted an unambiguous ' + key)
        values = dict(pairs)
        if values['database'] != str(self.config.database):
            raise ValueError('EDB status returned a different database')
        if not re.fullmatch(r'\d+', values['basis_t']):
            raise ValueError('EDB status returned an invalid basis')
        try:
            lineage = str(uuid.UUID(values['lineage']))
        except ValueError as error:
            raise ValueError('EDB status returned an invalid database lineage') from error
        return {'database': values['database'], 'lineage': lineage, 'basis': int(values['basis_t'])}

    def basis(self):
        return self.status()['basis']

    def snapshot_reader(self, basis):
        return SnapshotReads(self, basis)

    def query(self, source, inputs, directory, name, basis=None):
        directory = Path(directory)
        directory.mkdir(parents=True, exist_ok=True)
        query, args = directory / (name + '-query.edn'), directory / (name + '-inputs.edn')
        atomic_text(query, source)
        atomic_text(args, dumps(inputs))
        options = ['--file', query, '--inputs', args]
        if basis is not None:
            options += ['--as-of', basis]
        text = self.command('query', *options, timeout=60)
        atomic_text(directory / (name + '.edn'), text)
        return loads(text)

    def snapshot(self, content, directory, basis):
        # Numeric entity IDs and transaction bases only identify facts within
        # one lineage. Bind the reads before preparing a durable write request.
        identity = self.status()
        topics = {int(q.get('topic_id') or content.get('topic_id')) for q in
                  content.get('questions', []) + content.get('reference_questions', []) + content.get('canonical_examples', [])
                  if q.get('topic_id') or content.get('topic_id')}
        if content.get('topic_id'):
            topics.add(int(content['topic_id']))
        topic_rows = []
        topic_ids = sorted(topics)
        # Assessments can span hundreds of topics. Read bounded relations at
        # the same immutable basis instead of launching two CLI calls per topic.
        for start in range(0, len(topic_ids), 25):
            group = topic_ids[start:start + 25]
            topic_rows += self.query('''[:find (pull ?t [* {:topic/knowledge-points [*
              {:knowledge-point/canonical-example [:db/id :question/id :question/math-academy-id]}
              {:knowledge-point/questions [:db/id :question/id :question/math-academy-id]}]}])
              :in $ [?id ...] :where [?t :topic/math-academy-id ?id]]''', [group], directory, 'topic-batch-' + str(start), basis)
        # Unreconciled live originals remain capture evidence. They have no
        # verified source identity to query and will receive explicit omissions.
        mids = {q['math_academy_id'] for q in content.get('questions', []) + content.get('reference_questions', []) + content.get('canonical_examples', [])
                if isinstance(q.get('math_academy_id'), str) and re.fullmatch(r'[qe]-\d+', q['math_academy_id'])}
        # Existing examples can be revisions with changed MA IDs; include them in the complete pull.
        if content.get('canonical_examples'):
            for row in topic_rows:
                for point in row[0].get(':topic/knowledge-points', []):
                    example = point.get(':knowledge-point/canonical-example', {})
                    if example.get(':question/math-academy-id'):
                        mids.add(example[':question/math-academy-id'])
        questions = []
        for start in range(0, len(mids), 100):
            questions += self.query('[:find (pull ?q ' + QUESTION_PULL + ') :in $ [?id ...] :where [?q :question/math-academy-id ?id]]',
                                    [sorted(mids)[start:start + 100]], directory, 'questions-' + str(start), basis)
        activities = []
        for start in range(0, len(topic_ids), 25):
            activities += self.query('[:find (pull ?a ' + ACTIVITY_PULL + ''') :in $ [?id ...]
              :where [?t :topic/math-academy-id ?id] [?a :activity/scope ?t]]''',
              [topic_ids[start:start + 25]], directory, 'activities-batch-' + str(start), basis)
        definition_id = content.get('activity_definition_id')
        if definition_id:
            activities += self.query('[:find (pull ?a ' + ACTIVITY_PULL + ') :in $ ?id :where [?a :activity/math-academy-id ?id]]',
                                     [int(definition_id)], directory, 'activity-definition', basis)
        if content.get('multistep_id'):
            from .prepare import source_uuid
            multistep_identity = source_uuid('multistep-activity', content['multistep_id'])
            activities += self.query('[:find (pull ?a ' + ACTIVITY_PULL + ') :in $ ?id :where [?a :activity/id ?id]]',
                                     [multistep_identity], directory, 'multistep-activity', basis)
        kind = content.get('task_type') or content.get('kind')
        if kind in ('review', 'assessment', 'diagnostic') and not definition_id:
            from .prepare import activity_identity
            activities += self.query('[:find (pull ?a ' + ACTIVITY_PULL + ') :in $ ?id :where [?a :activity/id ?id]]',
                                     [activity_identity(content, kind)], directory, 'activity-route', basis)
        course_rows = []
        if content.get('course_id'):
            course_rows = self.query('[:find (pull ?c [:db/id :course/id :course/math-academy-id]) :in $ ?id :where [?c :course/math-academy-id ?id]]',
                                     [int(content['course_id'])], directory, 'course', basis)
        # Older multistep captures also listed their shared context as a
        # tutorial with a DOM ID (step-1). It belongs to multistep/context,
        # never the tutorial catalog. Read lesson tutorials only so those
        # saved captures remain importable without rewriting source evidence.
        tutorial_ids = [int(t['math_academy_id']) for t in content.get('tutorials', [])] if kind == 'lesson' else []
        tutorials = self.query('[:find (pull ?t [*]) :in $ [?id ...] :where [?t :tutorial/math-academy-id ?id]]',
                               [tutorial_ids], directory, 'tutorials', basis) if tutorial_ids else []
        attributes = self.query('[:find ?a ?ident ?type ?card :where [?a :db/ident ?ident] [?a :db/valueType ?vt] [?vt :db/ident ?type] [?a :db/cardinality ?c] [?c :db/ident ?card]]',
                                [], directory, 'attributes', basis)
        sources = self.query('[:find ?e ?ident :where [?e :db/ident ?ident]]', [], directory, 'idents', basis)
        entities = {}
        def merge(previous, incoming):
            # Pulls at one basis can describe the same reference at different
            # depths. Keep complete answer fields when an activity later pulls
            # only their IDs, while respecting the incoming member set.
            if isinstance(previous, dict) and isinstance(incoming, dict):
                result = dict(previous)
                for key, value in incoming.items():
                    result[key] = merge(result[key], value) if key in result else value
                return result
            if isinstance(previous, list) and isinstance(incoming, list):
                by_id = {v[':db/id']: v for v in previous if isinstance(v, dict) and ':db/id' in v}
                return [merge(by_id[v[':db/id']], v) if isinstance(v, dict) and v.get(':db/id') in by_id else v
                        for v in incoming]
            if isinstance(previous, dict) and incoming == previous.get(':db/id'):
                return previous
            return incoming
        def collect(value):
            if isinstance(value, dict):
                if ':db/id' in value:
                    eid = value[':db/id']
                    entities[eid] = merge(entities.get(eid, {}), value)
                for child in value.values():
                    collect(child)
            elif isinstance(value, list):
                for child in value:
                    collect(child)
        collect(topic_rows + questions + activities + tutorials + course_rows)
        facts = []
        # Question-bank membership pulls include thousands of shallow references.
        # Their content is untouched: read provenance only for captured questions
        # and revision candidates, not every question in their topics' pools.
        ids = sorted(eid for eid, entity in entities.items()
                     if ':question/math-academy-id' not in entity or entity[':question/math-academy-id'] in mids)
        for start in range(0, len(ids), 100):
            facts += self.query('[:find ?e ?a ?v ?s :in $ [?e ...] :where [?e ?a ?v _ ?s]]',
                                [ids[start:start + 100]], directory, 'facts-' + str(start), basis)
        return {'basis': basis, 'lineage': identity['lineage'], 'entities': list(entities.values()), 'attributes': attributes,
                'idents': sources, 'facts': facts}

    def question_topic(self, question_id, directory):
        """Read one exact MA question binding, including topics outside the course."""
        if not isinstance(question_id, str) or not re.fullmatch(r'[qe]-\d+', question_id):
            return None
        basis = self.basis()
        rows = self.query("""[:find ?id :in $ ?question :where
            [?source :db/ident :org/Math-Academy]
            [?q :question/math-academy-id ?question _ ?source]
            (or [?kp :knowledge-point/questions ?q]
                [?kp :knowledge-point/canonical-example ?q])
            [?t :topic/knowledge-points ?kp] [?t :topic/math-academy-id ?id]]""",
            [question_id], directory, 'question-topic', basis)
        topics = {str(row[0]) for row in rows}
        if len(topics) != 1:
            return None
        return {'question_id': question_id, 'topic_id': topics.pop(), 'basis': basis,
                'source': 'database_math_academy_question_binding'}

    def targets(self, directory):
        basis = self.basis()
        learner_id = self.config.learner_id
        rows = self.query('''[:find ?target :in $ ?id :where
            [?l :learner/id ?id] [?l :learner/targets ?t]
            [?t :topic/math-academy-id ?target]]''',
            [learner_id], directory, 'learner-targets', basis) if learner_id else []
        targets = sorted({str(row[0]) for row in rows})
        return {'target_basis': basis, 'learner_id': learner_id, 'targets': targets,
                'target_origins': {'learner_targets': targets}}

    def source_dependencies(self, questions, directory):
        """Find captured topics/KP titles that need their original lesson source."""
        required = {}
        for question in questions:
            tid = question.get('topic_id')
            if tid is not None:
                required.setdefault(int(tid), set()).add(question.get('knowledge_point') or question.get('kp_title'))
        if not required:
            return []
        rows = self.query('''[:find (pull ?t [:topic/math-academy-id
            {:topic/knowledge-points [:knowledge-point/title]}])
            :in $ [?id ...] :where [?t :topic/math-academy-id ?id]]''',
            [sorted(required)], directory, 'source-dependencies', self.basis())
        known = {int(topic[':topic/math-academy-id']):
                 {point.get(':knowledge-point/title') for point in topic.get(':topic/knowledge-points', [])}
                 for [topic] in rows}
        return [str(tid) for tid, titles in sorted(required.items())
                if tid not in known or any(title and title not in known[tid] for title in titles)]

    def context(self, activity, directory):
        basis = self.basis()
        topic_rows = self.query('[:find ?e ?id ?title :where [?e :topic/math-academy-id ?id] [?e :topic/title ?title]]',
                            [], directory, 'topics', basis)
        topics = [(mid, title) for eid, mid, title in topic_rows]
        topic_ids = {eid: str(mid) for eid, mid, title in topic_rows}
        # Fetch small single-attribute relations and join them in Python. This
        # avoids materializing an unbounded multi-way Datalog intermediate.
        edges = self.query('[:find ?a ?b :where [?a :topic/next ?b]]', [], directory, 'edges', basis)
        bindings = {}
        graph = {mid: [] for mid in topic_ids.values()}
        for before, after in edges:
            if before in topic_ids and after in topic_ids:
                graph[topic_ids[before]].append(topic_ids[after])
        course = activity.get('course_id') or self.config.course_id
        course_topics = []
        if course:
            course_topics = self.query('''[:find ?id :in $ ?course :where [?c :course/math-academy-id ?course]
              [?c :course/units ?u] [?u :unit/modules ?m] [?m :module/topics ?t] [?t :topic/math-academy-id ?id]]''',
                                       [int(course)], directory, 'course-topics', basis)
        # Bindings are an optimization, not a prerequisite classifier. Read the
        # active course and current topic in bounded pulls; the complete topic
        # graph below still includes external prerequisites for agent matching.
        binding_topics = {r[0] for r in course_topics}
        if activity.get('topic_id'):
            binding_topics.add(int(activity['topic_id']))
        binding_topics = sorted(binding_topics)
        for offset in range(0, len(binding_topics), 100):
            rows = self.query('''[:find (pull ?t [:topic/math-academy-id
                {:topic/knowledge-points [{:knowledge-point/questions [:question/math-academy-id]}]}])
                :in $ [?id ...] :where [?t :topic/math-academy-id ?id]]''',
                [binding_topics[offset:offset + 100]], directory, 'bindings-' + str(offset), basis)
            for [topic] in rows:
                for point in topic.get(':topic/knowledge-points', []):
                    for question in point.get(':knowledge-point/questions', []):
                        if question.get(':question/math-academy-id'):
                            bindings[question[':question/math-academy-id']] = str(topic[':topic/math-academy-id'])
        return {'basis': basis, 'topics': [{'id': str(t), 'title': title} for t, title in topics],
                'course_topics': [str(r[0]) for r in course_topics], 'graph': graph,
                'question_topics': bindings}
