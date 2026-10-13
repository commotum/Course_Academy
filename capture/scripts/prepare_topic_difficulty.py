"""Prepare, never submit, topic workload multipliers from recorded lessons.

Use the documented first-two-question-per-KP calibration. All observations remain
separate; choose one latest eligible lesson for each shared topic. Run with the
MA virtualenv (BeautifulSoup is used for the legacy tutorial HTML).
"""
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import argparse
import copy
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess
import threading
import uuid

from .database.client import EDBClient
from .database.commit import connection_identity
from .database.difficulty import calibrate, prose_words
from .database.edn import dumps, kw, loads
from .database.pipeline import DatabasePipeline
from .config import Config
from .storage import atomic_json, atomic_text

SOURCE = ':agent/gpt-6.1-sol-high'
DEFAULT_FOLDER = 'reference/edb-math/imports/topic-difficulty/2026-10-12'


def read(path):
    return json.loads(path.read_text())


def manifest(path, root):
    return dict(path=str(path.relative_to(root)), sha256=hashlib.sha256(path.read_bytes()).hexdigest())


def legacy_base(text):
    match = re.search(r"(?:of|all of) the task's (\d+) XP", text)
    if not match:
        match = re.search(r'-?\d+\s*/\s*(\d+)\s*XP', text)
    if not match:
        raise ValueError('Missing authoritative lesson base denominator')
    return int(match[1])


def tutorial_prose(html):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    for tag in soup.select('style, script, svg, math, mjx-container, .mjpage, .stepHeader, .helpButton'):
        tag.decompose()
    return soup.get_text(' ', strip=True)


def validate_definition(content):
    definition = content.get('lesson_definition', {})
    if not definition.get('complete'):
        raise ValueError('Incomplete lesson definition')
    steps = definition.get('steps', [])
    if not steps:
        raise ValueError('Missing complete lesson step inventory')
    expected_examples = {'e-' + str(s['content_id']) for s in steps if s['type'] in ('example', 'knowledge-point')}
    actual_examples = {q.get('math_academy_id') for q in content.get('canonical_examples', [])}
    if expected_examples != actual_examples:
        raise ValueError('Canonical examples do not cover the full lesson definition')
    expected_tutorials = {str(s['content_id']) for s in steps if s['type'] == 'tutorial'}
    actual_tutorials = {str(t.get('math_academy_id')) for t in content.get('tutorials', [])}
    if expected_tutorials != actual_tutorials:
        raise ValueError('Tutorials do not cover the full lesson definition')
    if any(not t.get('content', '').strip() for t in content.get('tutorials', [])):
        raise ValueError('Empty captured tutorial')


def observation(path, root, legacy=False):
    content = read(path)
    kind = content.get('task_type') or content.get('kind')
    if kind != 'lesson':
        return None
    files = [path]
    account = path.parts[-3] if not legacy else 'legacy-unlabelled'
    state = None
    if legacy:
        state_path = path.parent / 'state.json'
        state = read(state_path)
        files.append(state_path)
        if state.get('task_type', 'lesson') != 'lesson' or not state.get('activity_complete') or not state.get('lesson_complete'):
            raise ValueError('Legacy lesson is incomplete')
        if str(state.get('task_id')) != str(content.get('task_id')) or str(state.get('topic_id')) != str(content.get('topic_id')):
            raise ValueError('Legacy state and content identities disagree')
        kps = set(state.get('kps', {}))
        examples = {str(q.get('knowledge_point_id')) for q in content.get('canonical_examples', [])}
        questions = {str(q.get('knowledge_point_id')) for q in content.get('questions', [])}
        if not kps or kps != examples or kps != questions:
            raise ValueError('Legacy KP inventory lacks full question/example coverage')
        content = copy.deepcopy(content)
        content['base_xp'] = legacy_base(state.get('completion', ''))
        content['lesson_definition'] = {'complete': True}
        tutorials = sorted(path.parent.glob('tutorial-*.html'))
        files.extend(tutorials)
        content['tutorials'] = [{'content': tutorial_prose(t.read_text())} for t in tutorials]
        base_evidence = {'source_file': str(state_path.relative_to(root)), 'source_text': state.get('completion')}
        coverage_evidence = 'completed legacy lesson and exact state KP/question/example inventories'
    else:
        validate_definition(content)
        original_base = content.get('base_xp')
        content = DatabasePipeline._with_post_activity_base(None, content, path.parent)
        if original_base is None and content.get('base_xp_evidence'):
            files.append(path.parent / 'post-activity.json')
            base_evidence = content['base_xp_evidence']
        else:
            base_evidence = {'source_file': str(path.relative_to(root)), 'field': 'base_xp or lesson_workload_sample.base_xp'}
        coverage_evidence = 'complete captured lesson definition; exact canonical-example and tutorial inventories'
    result = calibrate(content)
    if not math.isfinite(result['unscaled_score']) or result['unscaled_score'] <= 0 or not math.isfinite(result['multiplier']) or result['multiplier'] <= 0:
        raise ValueError('Invalid calibration score or multiplier')
    if max(7, math.floor(result['unscaled_score'] * result['multiplier'] + .5)) != result['base_xp']:
        raise ValueError('Calibrated score does not reproduce the observed denominator')
    definitions = content.get('lesson_definition', {}).get('steps', [])
    version = [(s['type'], s['content_id']) for s in definitions]
    return dict(account=account, task_id=str(content['task_id']), topic_id=int(content['topic_id']),
                captured_at=content.get('captured_at'), source_file=str(path.relative_to(root)),
                source_files=[manifest(p, root) for p in files], base_evidence=base_evidence,
                complete_kp_coverage=coverage_evidence, lesson_structure=version,
                canonical_examples=[q['math_academy_id'] for q in content['canonical_examples']],
                tutorial_words=sum(prose_words(t['content']) for t in content['tutorials']),
                floor_limited=result['base_xp'] == 7, **result)


def collect(root, folder):
    if (folder / 'request.json').exists():
        raise ValueError('Preserve the exact prepared request; use a new folder to refresh evidence')
    current = sorted((root / 'reference/mathacademy/capture').glob('*/*/content.json'))
    legacy = sorted((root / 'reference/mathacademy/question-capture').glob('*/content.json'))
    candidates = [(p, False) for p in current] + [(p, True) for p in legacy]
    def evaluate(pair):
        path, old = pair
        try:
            return observation(path, root, old), None
        except (ValueError, KeyError, TypeError, OSError) as error:
            return None, dict(source_file=str(path.relative_to(root)), reason=str(error))
    rows, exclusions = [], []
    with ThreadPoolExecutor(max_workers=4) as pool:
        for row, exclusion in pool.map(evaluate, candidates):
            if row:
                rows.append(row)
            if exclusion:
                exclusions.append(exclusion)
    # Same task may have been retained in both formats. Prefer the explicit new
    # lesson definition, retaining the other observation in the evidence archive.
    by_task = defaultdict(list)
    for row in rows:
        by_task[row['task_id']].append(row)
    observations = [min(group, key=lambda r: (r['account'] == 'legacy-unlabelled', r['source_file']))
                    for group in by_task.values()]
    observations.sort(key=lambda r: int(r['task_id']))
    requests = [dict(op='calibrate_lesson_xp', features=r['features'], base_xp=r['base_xp'], weights=[60., 30., 10.])
                for r in observations]
    native = subprocess.run([str(root / 'target/debug/fire'), 'batch'],
                            input=''.join(json.dumps(r) + '\n' for r in requests),
                            text=True, capture_output=True, check=True, timeout=60)
    native_results = [json.loads(line) for line in native.stdout.splitlines()]
    assert len(native_results) == len(observations)
    for row, native_row in zip(observations, native_results):
        assert 'ok' in native_row, native_row
        result = native_row['ok']
        assert result['base_xp'] == row['base_xp']
        assert math.isclose(result['unscaled_score'], row['unscaled_score'], rel_tol=1e-12)
        assert math.isclose(result['multiplier'], row['multiplier'], rel_tol=1e-12)
        row['native_round_trip_verified'] = True
    atomic_json(folder / 'observations.json', observations)
    atomic_json(folder / 'all-observations-including-duplicate-formats.json', rows)
    atomic_json(folder / 'excluded-captures.json', exclusions)
    atomic_json(folder / 'native-calibration-results.json', native_results)
    info = dict(collected_at=datetime.now(timezone.utc).isoformat(), eligible_observations=len(observations),
                eligible_topics=len({r['topic_id'] for r in observations}),
                observations_by_account=dict(Counter(r['account'] for r in observations)),
                excluded_captures=len(exclusions), exclusion_counts=dict(Counter(r['reason'] for r in exclusions)),
                native_round_trips_passed=len(observations),
                formula_sources=[manifest(root / path, root) for path in
                                 ('capture/scripts/database/difficulty.py', 'engine/rust/base_xp.rs',
                                  'reference/THE_PLAN/README.md', 'reference/xp-docs/expected-distribution-base-xp.md')])
    atomic_json(folder / 'collection-summary.json', info)
    print(json.dumps(info, indent=2))


def prepare(root, folder):
    if (folder / 'request.json').exists():
        raise ValueError('Preserve the exact saved request; use a new folder for a refreshed proposal')
    observations = read(folder / 'observations.json')
    client = EDBClient(Config(capture_only=True), threading.Event())
    identity = client.status()
    queries = {
        'topics': ('[:find (pull ?t [:db/id :topic/id :topic/math-academy-id :topic/title :topic/difficulty]) :where [?t :topic/id _]]', []),
        'idents': ('[:find ?e ?ident :where [?e :db/ident ?ident]]', []),
        'lesson-weights': ('[:find ?p ?w ?e ?m ?h :where [?p :policy/id _] [?p :policy/question-selection-weights ?w] [?w :question-weights/activity-type :activity.type/lesson] [?w :question-weights/initial-easy ?e] [?w :question-weights/initial-moderate ?m] [?w :question-weights/initial-hard ?h]]', []),
        'lesson-durations': ('[:find ?a ?mid (pull ?a [:db/id :activity/id :activity/expected-seconds]) :where [?a :activity/type :activity.type/lesson] [?a :activity/scope ?t] [?t :topic/math-academy-id ?mid]]', [])}
    def export(name):
        query, inputs = queries[name]
        rows = client.query(query, inputs, folder, name, identity['basis'])
        atomic_json(folder / (name + '.json'), json.loads(json.dumps(rows, default=str)))
        return name, rows
    with ThreadPoolExecutor(max_workers=3) as pool:
        data = dict(pool.map(export, queries))
    assert len(data['lesson-weights']) == 1, 'Expected one active lesson policy'
    policy, weight_entity, *weights = data['lesson-weights'][0]
    requests = [dict(op='calibrate_lesson_xp', features=r['features'], base_xp=r['base_xp'], weights=weights)
                for r in observations]
    native = subprocess.run([str(root / 'target/debug/fire'), 'batch'],
                            input=''.join(json.dumps(r) + '\n' for r in requests),
                            text=True, capture_output=True, check=True, timeout=60)
    native_results = [json.loads(line) for line in native.stdout.splitlines()]
    assert len(native_results) == len(observations)
    calibrated = []
    for row, response in zip(observations, native_results):
        assert 'ok' in response, response
        result = response['ok']
        assert result['base_xp'] == row['base_xp']
        assert math.isfinite(result['multiplier']) and result['multiplier'] > 0
        assert max(7, math.floor(result['unscaled_score'] * result['multiplier'] + .5)) == row['base_xp']
        calibrated.append({**row, **result, 'native_round_trip_verified': True,
                           'policy_entity': policy, 'question_weights_entity': weight_entity,
                           'policy_weights': weights})
    observations = calibrated
    atomic_json(folder / 'current-policy-calibrations.json', observations)
    atomic_json(folder / 'current-policy-native-results.json', native_results)
    idents = {ident: eid for eid, ident in data['idents']}
    assert SOURCE in idents
    assert ':topic/difficulty' in idents and ':topic/difficulty-validate' in idents
    topics = {r[0][':topic/math-academy-id']: r[0] for r in data['topics'] if ':topic/math-academy-id' in r[0]}
    grouped = defaultdict(list)
    for row in observations:
        grouped[row['topic_id']].append(row)
    selected, omitted, forms, expected = [], [], [], []
    for mid, rows in sorted(grouped.items()):
        if mid not in topics:
            omitted.append(dict(topic_id=mid, reason='Topic not present in current database'))
            continue
        # Increasing MA task IDs order recorded assignments. A later archive read
        # of an older task is not a newer lesson observation.
        row = max(rows, key=lambda r: (int(r['task_id']), float(r.get('captured_at') or 0), r['account'], r['source_file']))
        topic = topics[mid]
        value = float(row['multiplier'])
        same = topic.get(':topic/difficulty') == value
        selected.append(dict(**row, topic_entity=topic[':db/id'], topic_title=topic.get(':topic/title'),
                             previous_multiplier=topic.get(':topic/difficulty'), no_change=same,
                             other_eligible_task_ids=[r['task_id'] for r in rows if r is not row]))
        if not same:
            forms.append({kw('db/id'): [kw('topic/math-academy-id'), mid], kw('topic/difficulty'): value,
                          kw('db/ensure'): kw('topic/difficulty-validate')})
            expected.append((topic[':db/id'], idents[':topic/difficulty'], value))
    assert forms, 'No difficulty values require a transaction'
    difficulty_to_write = len(forms)
    selected_by_topic = {r['topic_id']: r for r in selected}
    duration_audit = []
    expected_retractions = [(r['topic_entity'], idents[':topic/difficulty'], r['previous_multiplier'])
                            for r in selected if not r['no_change'] and r['previous_multiplier'] is not None]
    for activity, mid, current in data['lesson-durations']:
        if mid in selected_by_topic:
            row = selected_by_topic[mid]
            seconds = current.get(':activity/expected-seconds')
            agrees = seconds == row['expected_seconds']
            duration_audit.append(dict(activity_entity=activity, topic_id=mid,
                stored_expected_seconds=seconds, captured_expected_seconds=row['expected_seconds'], agrees=agrees))
            if not agrees:
                forms.append({kw('db/id'): activity, kw('activity/expected-seconds'): row['expected_seconds'],
                              kw('db/ensure'): kw('activity/validate')})
                expected.append((activity, idents[':activity/expected-seconds'], row['expected_seconds']))
                if seconds is not None:
                    expected_retractions.append((activity, idents[':activity/expected-seconds'], seconds))
    for row in selected:
        for source_file in row['source_files']:
            assert hashlib.sha256((root / source_file['path']).read_bytes()).hexdigest() == source_file['sha256'], 'Captured evidence changed during preparation'
    transaction = dumps(forms) + '\n'
    digest = hashlib.sha256(transaction.encode()).hexdigest()
    request = dict(**connection_identity(Config(capture_only=True)), database_lineage=identity['lineage'],
                   basis=identity['basis'], source=SOURCE, source_ident=SOURCE,
                   request_key='topic-workload-2026-10-12-' + str(uuid.uuid4()),
                   transaction=transaction, transaction_sha256=digest, status='prepared; not submitted',
                   evidence_sha256=hashlib.sha256((folder / 'observations.json').read_bytes()).hexdigest(),
                   intended_topics=difficulty_to_write, intended_duration_updates=len(forms) - difficulty_to_write)
    request['lesson_policy_entity'] = policy
    request['lesson_question_weights_entity'] = weight_entity
    request['lesson_initial_weights'] = weights
    request['current_policy_evidence_sha256'] = hashlib.sha256((folder / 'current-policy-calibrations.json').read_bytes()).hexdigest()
    atomic_json(folder / 'database-identity.json', identity)
    atomic_json(folder / 'selected-calibrations.json', selected)
    atomic_json(folder / 'activity-duration-audit.json', duration_audit)
    atomic_json(folder / 'omitted-topics.json', omitted)
    atomic_text(folder / 'transaction.edn', transaction)
    atomic_json(folder / 'request.json', request)
    output = client.command('with', '--file', folder / 'transaction.edn', '--source', SOURCE)
    atomic_text(folder / 'preview.edn', output)
    report = loads(output)
    assert report[':edb/committed'] is False and report[':edb/speculative'] is True
    assert report[':edb/db-before-t'] == identity['basis'], 'Database advanced before preview; preserve this request and prepare a new bundle'
    observed, retracted, timestamps = [], [], []
    for entity, attr, value, tx, source, added in report[':edb/tx-data']:
        assert source == idents[SOURCE]
        if attr == idents[':db/txInstant']:
            assert added and entity == tx
            timestamps.append(tx)
        else:
            assert attr in (idents[':topic/difficulty'], idents[':activity/expected-seconds']), 'Unexpected protected attribute change'
            (observed if added else retracted).append((entity, attr, value))
    assert Counter(observed) == Counter(expected) and Counter(retracted) == Counter(expected_retractions)
    assert len(timestamps) == 1 and not report[':edb/tempids']
    verification = dict(status='verified noncommitting preview', committed=False,
                        read_basis=identity['basis'], speculative_after_basis=report[':edb/db-after-t'],
                        source_ident=SOURCE, source_entity=idents[SOURCE], assertions=len(observed),
                        retractions=len(retracted), exact_expected_facts_match=True,
                        domain_attributes=[':topic/difficulty', ':activity/expected-seconds'],
                        learner_and_policy_facts_unchanged=True,
                        transaction_sha256=digest, database_writes=0,
                        preview_sha256=hashlib.sha256(output.encode()).hexdigest())
    atomic_json(folder / 'preview-verification.json', verification)
    values = sorted(r['multiplier'] for r in selected)
    import statistics
    summary = dict(status='prepared and previewed; not submitted', database=identity,
                   source_ident=SOURCE, total_database_topics=len(data['topics']),
                   calibrated_topics=len(selected), topics_to_write=difficulty_to_write,
                   lesson_duration_updates=len(forms) - difficulty_to_write,
                   unchanged_topics=sum(r['no_change'] for r in selected), uncalibrated_topics=len(data['topics']) - len(selected),
                   floor_limited_topics=sum(r['floor_limited'] for r in selected),
                   neutral_multiplier_topics=sum(v == 1. for v in values),
                   min_multiplier=min(values), median_multiplier=statistics.median(values), max_multiplier=max(values),
                   selected_account_counts=dict(Counter(r['account'] for r in selected)),
                   lesson_initial_weights=weights,
                   selection='Most recent eligible MA task ID per topic; one complete observation, no blending of accounts or lesson versions',
                   native_round_trips_passed=len(observations), transaction_sha256=digest,
                   matching_lesson_duration_records=len(duration_audit),
                   lesson_duration_disagreements=sum(not r['agrees'] for r in duration_audit),
                   preview_verification='preview-verification.json', prepared_at=datetime.now(timezone.utc).isoformat())
    atomic_json(folder / 'summary.json', summary)
    print(json.dumps(summary, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('collect', 'prepare'))
    parser.add_argument('--folder', type=Path, default=Path(DEFAULT_FOLDER))
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    folder = args.folder if args.folder.is_absolute() else root / args.folder
    folder.mkdir(parents=True, exist_ok=True)
    (collect if args.action == 'collect' else prepare)(root, folder)


if __name__ == '__main__':
    main()
