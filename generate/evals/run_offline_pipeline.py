#!/usr/bin/env python3
"""Run real pipeline agents and gates on synthetic source, stopping before publish.

No fake agent/tool evidence is supplied. The only adapter is the fixed local
source provider. Every database query, publication and transaction method raises.
"""
import argparse
import copy
import json
import os
from pathlib import Path
import sys
import time
from types import SimpleNamespace
import uuid

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
sys.path.insert(0, str(ROOT))
from generator_pipeline import Pipeline, CodexSession, RunnerChanged
from generator_publish import digest, inventory_fingerprints
from generator_source_policy import POLICY_VERSION
from inventory_jobs import save

KP = 900001
FIXTURES = ROOT / 'generate/pipeline/fixtures'


def identity(name):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, 'course-academy-offline-matrix:' + name))


def source_material():
    lesson = (FIXTURES / 'source.md').read_text()
    cases = json.loads((FIXTURES / 'source-cases.json').read_text())
    records = []
    for number, case in enumerate(cases):
        name = case['id']
        row, column = case['parameters']['row'] + 1, case['parameters']['column'] + 1
        answer = case['answer']
        question = {':db/id': 910011 + number, ':question/id': identity(name),
            ':question/problem': 'For $A=\\begin{pmatrix}2&-3\\\\0&7\\end{pmatrix}$, find $a_{'
                + str(row) + str(column) + '}$.\n\n{{answer}}',
            ':question/worked-solution': f'The first index is {row}, so use row {row}. '
                f'The second index is {column}, so use column {column} of that row. '
                + '$a_{' + str(row) + str(column) + '}=' + answer + '$.',
            ':question/difficulty': ':question.difficulty/easy',
            ':question/answer-fields': [{':answer-field/id': identity(name + ':field'),
                ':answer-field/key': 'answer', ':answer-field/type': ':answer-field.type/blank',
                ':answer-field/correct': [':answer/id', identity(name + ':answer')],
                ':answer-field/choices': [{':answer/id': identity(name + ':answer'),
                    ':answer/type': ':answer.type/math', ':answer/value': answer}]}]}
        records.append({'source_id': name, 'parameters': case['parameters'], 'question': question})
    canonical = copy.deepcopy(records[1]['question'])
    canonical[':db/id'] = 910000
    canonical[':question/id'] = identity('canonical')
    kp = {':db/id': KP, ':knowledge-point/id': identity('kp'),
          ':knowledge-point/title': 'Read an entry of a two-by-two integer matrix',
          ':knowledge-point/questions': [row['question'] for row in records],
          ':knowledge-point/canonical-example': canonical,
          ':knowledge-point/key-prerequisites': []}
    # Synthetic evidence is explicit. Do not fabricate Math Academy import IDs
    # to circumvent instructional_material's genuine-import filter.
    return {'kp': kp, 'topics': [{':db/id': 900000, ':topic/id': identity('topic'),
            ':topic/title': 'Synthetic matrix entries', ':topic/knowledge-points': [kp]}],
        'lessons': [{':db/id': 920000, ':activity/id': identity('lesson'),
            ':activity/type': ':activity.type/lesson', ':activity/title': 'Synthetic matrix entry lesson',
            ':activity/steps': [{':step/id': identity('lesson-step'), ':step/content': {
                ':tutorial/id': identity('tutorial'), ':tutorial/content': lesson}}]}],
        'prerequisites': [], 'synthetic_source_cases': records,
        'synthetic_source_notice': 'Authored offline evaluation source from generate/pipeline/fixtures/source.md; '
            'fixture-q11/q12/q21/q22 are synthetic source IDs, never Math Academy imports. '
            'synthetic_source_cases and the complete lesson are authoritative for this offline task.',
        'source_eligibility': {'policy_version': POLICY_VERSION, 'excluded_questions': []}}


class OfflinePublisher:
    def __init__(self, directory):
        self.directory = Path(directory)
        self.config = SimpleNamespace(math_root=self.directory / 'math', repo_root=ROOT)
        self.config.math_root.mkdir(parents=True, exist_ok=True)
        self.client = self
        self.material = source_material()

    def status(self):
        return {'database': 'offline-synthetic-matrix', 'lineage': 'offline-synthetic-matrix-v1', 'basis': 1}

    def extract_inventory(self, kp, directory):
        assert kp == KP
        questions = copy.deepcopy(self.material['kp'][':knowledge-point/questions'])
        canonical = copy.deepcopy(self.material['kp'][':knowledge-point/canonical-example'])
        value = {**self.status(), 'kp_id': KP, 'questions': questions,
                 'canonical_example': canonical,
                 'fingerprints': sorted(inventory_fingerprints([*questions, canonical]))}
        save(Path(directory) / 'inventory.json', value)
        return value

    def extract_source(self, kp, directory, **kwargs):
        assert kp == KP
        value = {**self.status(), 'kp_id': KP, 'material': copy.deepcopy(self.material),
            'source_sha256': digest(self.material), 'registered_generator': None,
            'available_difficulties': ['easy']}
        save(Path(directory) / 'source.json', value)
        Path(directory, 'source.md').write_text((FIXTURES / 'source.md').read_text())
        save(Path(directory) / 'source-cases.json', json.loads((FIXTURES / 'source-cases.json').read_text()))
        self.extract_inventory(kp, directory)
        return value

    def forbidden(self, *args, **kwargs):
        raise RuntimeError('Offline evaluation forbids every database query, transaction and publication')

    query = prepare = publish = publish_exemplars = prepare_exemplars = transact = submit = forbidden


def prepare_investigation(publisher, source, directory):
    summary = {'database': source['database'], 'lineage': source['lineage'], 'basis': 1,
        'kp_id': KP, 'needs_exemplars': True, 'construction_needed': True,
        'observed_coverage': ['easy'], 'complete_examples': {'easy': 4, 'moderate': 0, 'hard': 0},
        'missing_example_bands': ['moderate', 'hard'], 'incomplete_imports': [],
        'reference_candidates': [],
        'note': 'Synthetic source supports the target operation; no donors exist or are needed. '
                'Do not invent Math Academy provenance. Author coherent bands within the same two-by-two entry-reading task.'}
    path = Path(directory) / 'investigation-input.json'
    save(path, summary)
    return {**summary, 'investigation_file': str(path), 'reference_file': None}


class OfflinePipeline(Pipeline):
    def session_call(self, role, context, directory):
        context = {**context, 'offline_evaluation': {
            'synthetic_source': True, 'database_access': 'forbidden', 'publication': 'forbidden',
            'edit_scope': str(self.directory),
            'instructions': 'This is a genuine offline evaluation of the production pipeline. '
                'Use actual grading, rendering, delivery and report tools; never fabricate evidence. '
                'Write only under this evaluation directory or disposable /tmp test directories. '
                'Do not edit shared production code, prompts, tests or policies; report a concrete shared defect to the parent instead. '
                'No database access, service restart, publication or external messaging is authorized. '
                'Use only source.md/source-cases.json as synthetic source; do not inspect the prebuilt generator, '
                'build.py or decision_variation.py in generate/pipeline/fixtures or another evaluation solution. '
                'Normal source-first accounts, independent exemplar gate, authoring and final review all remain required.'}}
        # A production session call may reuse cached output or reject an
        # exhausted budget. Its execution.json/events.jsonl record real launches.
        event = {'event': 'pipeline_session_call', 'role': role, 'phase': context.get('phase', role),
                 'directory': str(directory), 'at': time.time()}
        print(json.dumps(event), flush=True)
        with (self.directory / 'offline-events.jsonl').open('a') as output:
            output.write(json.dumps(event) + '\n')
        result = super().session_call(role, context, directory)
        print(json.dumps({'event': 'pipeline_session_return', 'role': role, 'phase': context.get('phase', role),
                          'status': result.get('status', result.get('verdict')), 'at': time.time()}), flush=True)
        return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--directory', type=Path, default=Path('/tmp/generator-live-pipeline'))
    parser.add_argument('--seed', type=int, default=60419)
    parser.add_argument('--resume-reason', help='Explicit recorded production allowance for a blocked job; never resets counters')
    args = parser.parse_args()
    directory = args.directory.resolve()
    if not directory.is_relative_to(Path('/tmp')):
        parser.error('Offline live-agent evidence must remain under /tmp')
    directory.mkdir(parents=True, exist_ok=True)
    # Authentication/runtime environment remains available to Codex. Live EDB
    # coordinates are removed; the only math root is this disposable directory.
    environment = {key: value for key, value in os.environ.items()
                   if not key.startswith('EDB_') and key not in ('LEARNING_REQUEST_DIR', 'COURSE_ACADEMY_GENERATOR_LOCK_FDS')}
    environment.update(EDB_MATH_ROOT=str(directory / 'math'),
                       COURSE_ACADEMY_GENERATOR_PYTHON=str(ROOT / '.venv/bin/python'),
                       PYTHONDONTWRITEBYTECODE='1')
    request = {'kp': KP, 'difficulty': 'easy', 'count': 3, 'existing_entrypoint': None}
    publisher = OfflinePublisher(directory)
    pipeline = OfflinePipeline(directory, request, publisher, root=ROOT, environment=environment,
        session=CodexSession(ROOT, environment), investigation_preparer=prepare_investigation)
    if pipeline.state['stage'] == 'source':
        pipeline.persist(seed=args.seed)
    result = pipeline.run(stop_after='validate', resume_reason=args.resume_reason)
    save(directory / 'offline-result.json', result)
    print(json.dumps({'event': 'offline_pipeline_result', 'stage': result['stage'],
        'review': result.get('review'), 'exemplar_gate': result.get('exemplar_gate', {}).get('report'),
        'database_writes': 0, 'publication_attempted': False}), flush=True)
    if result['stage'] != 'prepare' or not result.get('review'):
        raise SystemExit(1)


if __name__ == '__main__':
    main()
