"""Seven explicitly authorized original statements, without invented controls."""
from pathlib import Path
import argparse
import hashlib
import json
import threading
import time
import uuid

from .config import Config
from .storage import atomic_json, atomic_text, read_json, file_lock
from .database.client import EDBClient, QUESTION_PULL
from .database.commit import Committer
from .database.edn import kw, loads, dumps
from .database.prepare import Plan, Snapshot, MA_SOURCE, digest
from .database.text import markdown

IDS = {'q-122027', 'q-122033', 'q-124400', 'q-124403', 'q-73003', 'q-73005', 'q-73014'}
INPUT = Path('reference/mathacademy/factorials-13831129/repairs/fieldless-original-content-inputs/source-inputs.json')
ROOT = INPUT.parent
# Root and independent source reviewer approved this complete immutable input,
# including each exact extraction, owning DOM ID, raw HTML hash and KP binding.
REVIEWED_INPUT_SHA256 = '53b5460082f7067d6eb202047b0fcaf404cdee52e631787fca8547692ea51815'
QUESTION_ATTRS = {'question/id', 'question/math-academy-id', 'question/problem', 'question/worked-solution'}


def inputs():
    if hashlib.sha256(INPUT.read_bytes()).hexdigest() != REVIEWED_INPUT_SHA256:
        raise ValueError('Frozen independently source-reviewed seven-question input changed')
    data = read_json(INPUT)
    questions = data['questions']
    if len(questions) != 7 or {q['math_academy_id'] for q in questions} != IDS:
        raise ValueError('Only the seven explicitly authorized missing-control originals are permitted')
    from .browser.adapter import EXTRACT
    if hashlib.sha256(EXTRACT.encode()).hexdigest() != data['extractor_sha256']:
        raise ValueError('Original extraction generation changed; source inputs need renewed validation')
    for source in (data['history_capture_source'], data['original_completed_history_source']):
        if hashlib.sha256(Path(source['file']).read_bytes()).hexdigest() != source['sha256']:
            raise ValueError('Immutable owning history source changed')
    for q in questions:
        if any(key in q for key in ('answer_fields', 'fields', 'choices', 'correct_value')):
            raise ValueError('Fieldless source package contains response data')
        if q['topic_id'] != 774 or not q['problem'] or not q['worked_solution']:
            raise ValueError('Unexpected or incomplete original content')
        if {b['part'] for b in q['source_bindings']} != {'problem', 'worked_solution'}:
            raise ValueError('Each original must bind both complete authored sections')
        for binding in q['source_bindings']:
            if hashlib.sha256(Path(binding['source_file']).read_bytes()).hexdigest() != binding['source_sha256']:
                raise ValueError('Original authored HTML hash changed')
            if hashlib.sha256(q[binding['part']].encode()).hexdigest() != binding['extracted_text_sha256']:
                raise ValueError('Prepared text differs from source-checked extraction')
    return data


def prepare(data, snapshot):
    snap = Snapshot(snapshot); plan = Plan(snap)
    chosen = {}; points = {}; ma = snap.idents[MA_SOURCE]
    names = {row[0]: str(row[1]).lstrip(':') for row in snapshot['attributes']}
    for q in data['questions']:
        matches = snap.find('question/math-academy-id', q['math_academy_id'])
        if len(matches) > 1: raise ValueError('Ambiguous current question identity')
        old = matches[0] if matches else None
        identity = old[':question/id'] if old else uuid.UUID(q['question_uuid'])
        collisions = snap.find('question/id', identity)
        if any(e[':db/id'] != (old or {}).get(':db/id') for e in collisions):
            raise ValueError('Historical UUID now identifies different content')
        if old:
            if old.get(':question/answer-fields'):
                raise ValueError('A requested fieldless original now has controls; preserve current content')
            facts = [row for row in snapshot['facts'] if row[0] == old[':db/id'] and names.get(row[1]) in QUESTION_ATTRS - {'question/id'}]
            if any(row[3] != ma for row in facts):
                raise ValueError('Current question has separately attributed authored content')
        kp_matches = snap.find('knowledge-point/id', q['knowledge_point_uuid'])
        if len(kp_matches) != 1: raise ValueError('Original knowledge-point identity is not uniquely present')
        point = kp_matches[0]
        if point.get(':knowledge-point/title') != q['knowledge_point']:
            raise ValueError('Original knowledge-point title does not match current identity')
        if not any(point[':db/id'] == p[':db/id'] for topic in snapshot['entities']
                   if topic.get(':topic/math-academy-id') == 774
                   for p in topic.get(':topic/knowledge-points', [])):
            raise ValueError('Original knowledge point is not owned by the original topic')
        if not snap.sourced(point[':db/id'], 'knowledge-point/title', point[':knowledge-point/title'], MA_SOURCE):
            raise ValueError('Original knowledge-point title lacks active Math Academy provenance')
        target = plan.entity('question', identity, old)
        plan.set(target, old, 'question/math-academy-id', q['math_academy_id'])
        plan.set(target, old, 'question/problem', markdown(q['problem']))
        plan.set(target, old, 'question/worked-solution', markdown(q['worked_solution']))
        # Add only this exact source-owned practice link. Keep every old member.
        plan.set(point[':db/id'], point, 'knowledge-point/questions', [target], many=True)
        chosen[q['math_academy_id']] = {'uuid': str(identity), 'old_eid': (old or {}).get(':db/id'), 'target': target,
                                      'kp_eid': point[':db/id'], 'kp_uuid': str(point[':knowledge-point/id'])}
        points[point[':db/id']] = point
    batch = plan.finish()
    for entity, attr, value in batch['assertions'] + batch['retractions']:
        name = str(attr).lstrip(':')
        if name not in QUESTION_ATTRS | {'knowledge-point/questions'}:
            raise ValueError('Fieldless transaction changes an unauthorized attribute')
        if name == 'knowledge-point/questions' and (entity not in points or value not in {q['target'] for q in chosen.values()}):
            raise ValueError('Fieldless transaction changes an unrelated knowledge-point link')
    if any(str(attr) == ':knowledge-point/questions' for _, attr, _ in batch['retractions']):
        raise ValueError('Original partial-content import cannot remove knowledge-point membership')
    return batch, chosen, points


def verify(client, data, snapshot, chosen, points, directory, basis):
    rows = client.query('[:find (pull ?q ' + QUESTION_PULL + ') :in $ [?mid ...] :where [?q :question/math-academy-id ?mid]]',
                        [sorted(IDS)], directory, 'questions', basis)
    actual = {r[0][':question/math-academy-id']: r[0] for r in rows}
    if set(actual) != IDS: raise ValueError('Pinned readback lacks one or more originals')
    for q in data['questions']:
        old = chosen[q['math_academy_id']]; entity = actual[q['math_academy_id']]
        if str(entity[':question/id']) != old['uuid'] or entity.get(':question/answer-fields'):
            raise ValueError('Question identity changed or response controls appeared')
        if entity[':question/problem'] != markdown(q['problem']) or entity[':question/worked-solution'] != markdown(q['worked_solution']):
            raise ValueError('Pinned original text differs from exact source')
        if old['old_eid'] is not None and entity[':db/id'] != old['old_eid']:
            raise ValueError('Existing question entity was replaced')
        if old['kp_eid'] not in {p[':db/id'] for p in entity.get(':knowledge-point/_questions', [])}:
            raise ValueError('Original knowledge-point link is missing')
    kp_rows = client.query('[:find (pull ?kp [* {:knowledge-point/questions [:db/id]}]) :in $ [?kp ...] :where [?kp :knowledge-point/id ?uuid]]',
                           [sorted(points)], directory, 'knowledge-points', basis)
    if len(kp_rows) != len(points): raise ValueError('Pinned knowledge-point readback incomplete')
    for row in kp_rows:
        point = row[0]; before = points[point[':db/id']]
        wanted = {p[':db/id'] for p in before.get(':knowledge-point/questions', [])}
        wanted.update(actual[mid][':db/id'] for mid, item in chosen.items() if item['kp_eid'] == point[':db/id'])
        if {p[':db/id'] for p in point.get(':knowledge-point/questions', [])} != wanted:
            raise ValueError('Knowledge-point membership changed outside exact original links')
        # Snapshot has deeper reference pulls; compare all other native scalar facts.
        for key, value in before.items():
            if key == ':knowledge-point/questions': continue
            observed = point.get(key)
            def scalar(v): return v.get(':db/id') if isinstance(v, dict) else v
            if scalar(observed) != scalar(value): raise ValueError('Knowledge-point metadata changed')
    return actual


def process(apply=False):
    data = inputs(); config = Config(); client = EDBClient(config, threading.Event())
    directory = ROOT / 'native-fieldless-content'; directory.mkdir(exist_ok=True)
    authorization = {'scope': 'Exactly seven original questions; statement and worked solution plus original KP link only',
        'user_authorized_fieldless_content_only': True, 'controls_not_captured': sorted(IDS),
        'activity_import_or_completion_claim': False, 'source_inputs_sha256': REVIEWED_INPUT_SHA256}
    old_authorization = read_json(directory / 'authorization.json')
    if old_authorization is not None and old_authorization != authorization:
        raise ValueError('Existing fieldless repair authorization changed; retain it unchanged')
    if old_authorization is None: atomic_json(directory / 'authorization.json', authorization)
    with file_lock(config.database_lock):
        committer = Committer(config, client, directory)
        pending = committer.pending()
        if pending:
            if not apply: raise ValueError('Saved exact request requires recovery before another preview')
            if pending['content_sha256'] != digest(data): raise ValueError('Pending exact request source changed')
            snapshot = loads(pending['snapshot_edn']); batch = loads(pending['batch_edn'])
            before = read_json(directory / 'prepared-identities.json'); chosen = before['questions']
            points = {e[':db/id']: e for e in snapshot['entities'] if e[':db/id'] in before['knowledge_point_eids']}
            receipt = committer.submit(pending)
        else:
            identity = client.status()
            snapshot = client.snapshot({'questions': data['questions'], 'content_only': True}, directory / 'before', identity['basis'])
            # Recheck both the MA IDs and historical UUIDs, even when absent.
            collision_rows = client.query('[:find (pull ?q ' + QUESTION_PULL + ') :in $ [?uuid ...] :where [?q :question/id ?uuid]]',
                                          [[uuid.UUID(q['question_uuid']) for q in data['questions']]], directory / 'before', 'historical-uuids', identity['basis'])
            for row in collision_rows:
                if row[0][':db/id'] not in {e[':db/id'] for e in snapshot['entities']}:
                    snapshot['entities'].append(row[0])
            batch, chosen, points = prepare(data, snapshot)
            atomic_json(directory / 'prepared-identities.json', {'questions': chosen, 'knowledge_point_eids': sorted(points)})
            atomic_text(directory / 'snapshot.edn', dumps(snapshot))
            atomic_text(directory / 'batch.edn', dumps(batch))
            if not batch['forms']:
                return {'status': 'no_changes', 'basis': snapshot['basis'], 'questions': 7, 'answer_fields': 0}
            committer.preview(batch, snapshot)
            proof = {'status': 'previewed', 'basis': snapshot['basis'], 'lineage': snapshot['lineage'], 'questions': chosen,
                     'assertions': len(batch['assertions']), 'retractions': len(batch['retractions']),
                     'answer_fields_choices_keys_calibration_activity_learner_facts': 'No changes', 'source_sha256': digest(data)}
            atomic_json(directory / 'preview-proof.json', proof)
            if not apply: return proof
            pending = committer.save_request(batch, snapshot, digest(data))
            receipt = committer.submit(pending)
        receipt_proof = committer.verify_receipt(pending, receipt)
        after = receipt[':edb/db-after-t']
        verify(client, data, snapshot, chosen, points, directory / 'after', after)
        fresh = client.snapshot({'questions': data['questions'], 'content_only': True}, directory / 'second-prepare', after)
        second, _, _ = prepare(data, fresh)
        if second['forms'] or second['assertions'] or second['retractions']:
            raise ValueError('Repeat fieldless preparation is not a no-op')
        proof = {'status': 'verified', 'basis_before': snapshot['basis'], 'basis_after': after,
                 'questions': 7, 'answer_fields': 0, 'receipt': receipt_proof,
                 'checks': {'exact_source_text': True, 'question_UUIDs_preserved': True, 'original_KP_links': True,
                            'existing_KP_metadata_and_memberships_preserved': True, 'no_controls_or_keys': True,
                            'learner_engine_facts_unchanged': True, 'second_prepare_noop': True}}
        atomic_json(directory / 'verification.json', proof)
        committer.retire(pending, 'verified', proof)
        return proof


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--apply', action='store_true')
    print(json.dumps(process(parser.parse_args().apply), default=str), flush=True)
