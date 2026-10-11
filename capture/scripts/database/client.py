"""EDB CLI transport and reads pinned to one immutable database basis."""
from __future__ import annotations
import hashlib
import os
import re
import subprocess
import tempfile
from pathlib import Path
from .edn import dumps, loads, kw
from ..storage import atomic_text

QUESTION_PULL = '''[* {:question/difficulty [:db/id :db/ident]}
 {:knowledge-point/_questions [:db/id :knowledge-point/id :knowledge-point/title]}
 {:knowledge-point/_canonical-example [:db/id :knowledge-point/id :knowledge-point/title]}
 {:question/answer-fields [* {:answer-field/type [:db/id :db/ident]}
 {:answer-field/correct [* {:answer/type [:db/id :db/ident]}]}
 {:answer-field/choices [* {:answer/type [:db/id :db/ident]}]}]}]'''
CONTENT_PULL = '''[* {:knowledge-point/canonical-example [:db/id :question/id :question/math-academy-id]}
 {:assigned-problem/content [* {:multistep/steps [* {:step/content [:db/id :question/id :question/math-academy-id]}]}]}]'''
ACTIVITY_PULL = '[* {:activity/type [:db/id :db/ident]} {:activity/scope [:db/id :topic/id :topic/math-academy-id]} {:activity/steps [* {:step/content ' + CONTENT_PULL + '}]}]'

class StaleBasis(RuntimeError):
    pass

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
        args = [str(self.config.edb_bin), command, '--database', str(self.config.database), *map(str, options)]
        result = subprocess.run(args, env=self.environment, capture_output=True, text=True, timeout=timeout)
        if result.returncode:
            # Only an explicit stale-basis rejection proves the saved request did not commit.
            diagnostic = result.stderr
            if re.search(r'(?:code=|remote_code=)postgres/stale-basis(?:\s|$)', diagnostic):
                raise StaleBasis(diagnostic)
            raise subprocess.CalledProcessError(result.returncode, args, result.stdout, diagnostic)
        return result.stdout

    def basis(self):
        match = re.search(r'\bbasis_t=(\d+)', self.command('status', timeout=30))
        if not match:
            raise ValueError('EDB status omitted the current basis')
        return int(match[1])

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
        topics = {int(q.get('topic_id') or content.get('topic_id')) for q in
                  content.get('questions', []) + content.get('canonical_examples', [])
                  if q.get('topic_id') or content.get('topic_id')}
        if content.get('topic_id'):
            topics.add(int(content['topic_id']))
        topic_rows = []
        for tid in sorted(topics):
            topic_rows += self.query('''[:find (pull ?t [* {:topic/knowledge-points [*
              {:knowledge-point/canonical-example [:db/id :question/id :question/math-academy-id]}
              {:knowledge-point/questions [:db/id :question/id :question/math-academy-id]}]}])
              :in $ ?id :where [?t :topic/math-academy-id ?id]]''', [tid], directory, 'topic-' + str(tid), basis)
        mids = {q['math_academy_id'] for q in content.get('questions', []) + content.get('canonical_examples', [])}
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
        for tid in sorted(topics):
            activities += self.query('[:find (pull ?a ' + ACTIVITY_PULL + ''') :in $ ?id
              :where [?t :topic/math-academy-id ?id] [?a :activity/scope ?t]]''', [tid], directory, 'activities-' + str(tid), basis)
        definition_id = content.get('activity_definition_id')
        if definition_id:
            activities += self.query('[:find (pull ?a ' + ACTIVITY_PULL + ') :in $ ?id :where [?a :activity/math-academy-id ?id]]',
                                     [int(definition_id)], directory, 'activity-definition', basis)
        if content.get('multistep_id'):
            from .prepare import source_uuid
            identity = source_uuid('multistep-activity', content['multistep_id'])
            activities += self.query('[:find (pull ?a ' + ACTIVITY_PULL + ') :in $ ?id :where [?a :activity/id ?id]]',
                                     [identity], directory, 'multistep-activity', basis)
        course_rows = []
        if content.get('course_id'):
            course_rows = self.query('[:find (pull ?c [:db/id :course/id :course/math-academy-id]) :in $ ?id :where [?c :course/math-academy-id ?id]]',
                                     [int(content['course_id'])], directory, 'course', basis)
        tutorial_ids = [int(t['math_academy_id']) for t in content.get('tutorials', [])]
        tutorials = self.query('[:find (pull ?t [*]) :in $ [?id ...] :where [?t :tutorial/math-academy-id ?id]]',
                               [tutorial_ids], directory, 'tutorials', basis) if tutorial_ids else []
        attributes = self.query('[:find ?a ?ident ?type ?card :where [?a :db/ident ?ident] [?a :db/valueType ?vt] [?vt :db/ident ?type] [?a :db/cardinality ?c] [?c :db/ident ?card]]',
                                [], directory, 'attributes', basis)
        sources = self.query('[:find ?e ?ident :where [?e :db/ident ?ident]]', [], directory, 'idents', basis)
        entities = {}
        def collect(value):
            if isinstance(value, dict):
                if ':db/id' in value:
                    entities.setdefault(value[':db/id'], {}).update(value)
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
        return {'basis': basis, 'entities': list(entities.values()), 'attributes': attributes,
                'idents': sources, 'facts': facts}

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
        targets = list(self.config.targets)
        origins = {'configured': list(map(str, targets)), 'learner_targets': [], 'assignment_targets': [], 'active_assignments': 0}
        if getattr(self.config, 'learner_id', None):
            def content_pattern(depth):
                base = '[:db/id {:assigned-problem/topic-coverage [:topic/math-academy-id]}'
                if depth:
                    inner = content_pattern(depth - 1)
                    base += ' {:assigned-problem/content ' + inner + '} {:multistep/steps [{:step/content ' + inner + '}]}'
                return base + ']'
            query = '''[:find (pull ?l [{:learner/targets [:topic/math-academy-id]}
                {:learner/activity [{:learner-task/status [:db/ident]} {:learner-task/activity [:db/id]}]}
                {:learner/assignments [:db/id :activity/title {:activity/steps [{:step/content ''' + content_pattern(3) + '''}]}]}])
                :in $ ?id :where [?l :learner/id ?id]]'''
            rows = self.query(query, [self.config.learner_id], directory, 'target-configuration', basis)
            for [learner] in rows:
                origins['learner_targets'].extend(str(t[':topic/math-academy-id']) for t in learner.get(':learner/targets', []))
                completed = {task[':learner-task/activity'][':db/id'] for task in learner.get(':learner/activity', [])
                    if task.get(':learner-task/status', {}).get(':db/ident') == ':learner-task.status/completed'}
                def coverage(value):
                    found = set()
                    if isinstance(value, dict):
                        for t in value.get(':assigned-problem/topic-coverage', []):
                            if t.get(':topic/math-academy-id') is not None:
                                found.add(str(t[':topic/math-academy-id']))
                        for child in value.values():
                            found.update(coverage(child))
                    elif isinstance(value, list):
                        for child in value:
                            found.update(coverage(child))
                    return found
                for assignment in learner.get(':learner/assignments', []):
                    if assignment[':db/id'] not in completed:
                        origins['active_assignments'] += 1
                        origins['assignment_targets'].extend(sorted(coverage(assignment)))
            if not targets:
                targets = origins['learner_targets'] + origins['assignment_targets']
        targets = list(dict.fromkeys(map(str, targets)))
        return {'basis': basis, 'topics': [{'id': str(t), 'title': title} for t, title in topics],
                'course_topics': [str(r[0]) for r in course_topics], 'graph': graph,
                'targets': targets, 'target_origins': origins, 'question_topics': bindings}
