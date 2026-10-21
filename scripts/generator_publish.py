"""Deterministic generated-content preparation and recoverable EDB publication.

Agents produce candidate records; this adapter alone assembles and submits EDB
forms. A saved request is always recovered before reading a fresh preparation.
"""
from __future__ import annotations

import copy
import hashlib
import json
import os
import re
from pathlib import Path
import sys
import threading
from types import SimpleNamespace
import uuid

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from capture.scripts.database.client import EDBClient, StaleBasis
from capture.scripts.database.commit import Committer, VerificationError
from capture.scripts.database.edn import dumps, loads, kw
from capture.scripts.database.images import ImageLibrary
from capture.scripts.storage import atomic_json, atomic_text, file_lock, read_json
from scripts.generator_packages import resolve_registered_script


class SourceChanged(ValueError):
    """The original instructional evidence changed and requires a fresh review."""


QUESTION_PULL = '''[* {:question/difficulty [:db/ident]}
 {:question/answer-fields [* {:answer-field/type [:db/ident]}
 {:answer-field/correct [* {:answer/type [:db/ident]}]}
 {:answer-field/choices [* {:answer/type [:db/ident]}]}]}]'''
KP_PULL = ('[* {:knowledge-point/key-prerequisites [*]}'
           ' {:knowledge-point/question-generator [*]}'
           ' {:knowledge-point/canonical-example ' + QUESTION_PULL + '}'
           ' {[:knowledge-point/questions :limit nil] ' + QUESTION_PULL + '}]')
KP_QUERY = '[:find (pull ?kp ' + KP_PULL + ') :in $ ?kp :where [?kp :knowledge-point/id _]]'
ALLOWED = {
    'question/id', 'question/problem', 'question/worked-solution', 'question/difficulty', 'question/retired',
    'question/requires-calculator', 'question/answer-fields', 'answer-field/id',
    'answer-field/key', 'answer-field/type', 'answer-field/choices', 'answer-field/correct',
    'answer/id', 'answer/type', 'answer/value', 'answer/feedback',
    'question-generator/id', 'question-generator/script',
    'knowledge-point/questions', 'knowledge-point/question-generator',
}


def jsonable(value):
    if isinstance(value, dict):
        return {str(k): jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [jsonable(v) for v in value]
    return str(value) if isinstance(value, uuid.UUID) else value


def digest(value):
    return hashlib.sha256(json.dumps(jsonable(value), sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()).hexdigest()


def instructional_material(material):
    """Ignore operational pool/registration links while preserving source evidence."""
    material = copy.deepcopy(material)
    kp = material.get('kp', {})
    kp.pop(':knowledge-point/question-generator', None)
    kp[':knowledge-point/questions'] = [q for q in kp.get(':knowledge-point/questions', []) if q.get(':question/math-academy-id')]
    for lesson in material.get('lessons', []):
        for step in lesson.get(':activity/steps', []):
            content = step.get(':step/content', {})
            if ':knowledge-point/id' in content:
                content.pop(':knowledge-point/question-generator', None)
                content.pop(':knowledge-point/questions', None)
    return material


def enum(value):
    return str(value[':db/ident'] if isinstance(value, dict) else value)


def answer_id(value):
    if isinstance(value, dict):
        return str(value[':answer/id'])
    if isinstance(value, (list, tuple)) and len(value) == 2 and str(value[0]) == ':answer/id':
        return str(value[1])
    return str(value)


def normalized_question(question, *, identity=True):
    """Strip Pull metadata; preserve full authored content and response semantics."""
    q = question
    result = {k: q[k] for k in (':question/problem', ':question/worked-solution', ':question/requires-calculator') if k in q}
    if identity:
        result[':question/id'] = str(q[':question/id'])
    if ':question/difficulty' in q:
        result[':question/difficulty'] = enum(q[':question/difficulty'])
    fields = []
    for field in q.get(':question/answer-fields', []):
        item = {':answer-field/key': field[':answer-field/key'], ':answer-field/type': enum(field[':answer-field/type'])}
        if identity:
            item[':answer-field/id'] = str(field[':answer-field/id'])
        choices = []
        correct = answer_id(field.get(':answer-field/correct'))
        for a in field.get(':answer-field/choices', []):
            choice = {':answer/type': enum(a[':answer/type']), ':answer/value': a[':answer/value']}
            if ':answer/feedback' in a:
                choice[':answer/feedback'] = a[':answer/feedback']
            if identity:
                choice[':answer/id'] = str(a[':answer/id'])
            choices.append(choice)
            if str(a[':answer/id']) == correct:
                item[':answer-field/correct'] = str(a[':answer/id']) if identity else {k: choice[k] for k in (':answer/type', ':answer/value')}
        item[':answer-field/choices'] = sorted(choices, key=lambda a: json.dumps(a, sort_keys=True))
        fields.append(item)
    result[':question/answer-fields'] = sorted(fields, key=lambda f: f[':answer-field/key'])
    return jsonable(result)


def content_fingerprint(question):
    value = normalized_question(question, identity=False)
    value.pop(':question/worked-solution', None)
    value.pop(':question/difficulty', None)
    for field in value[':question/answer-fields']:
        for answer in field[':answer-field/choices']:
            answer.pop(':answer/feedback', None)
        if field[':answer-field/type'] in (':answer-field.type/blank', ':answer-field.type/free'):
            # Entered responses accumulate in these owned banks. They must not
            # turn the same mathematical prompt into a new practice identity.
            field.pop(':answer-field/choices', None)
    return digest(value)


def localize_record(record, math_root, assets_directory, *, library=None):
    """Use the shared byte-addressed image library for every authored image slot."""
    library = library if library is not None else ImageLibrary(Path(math_root), Path(assets_directory))
    result = copy.deepcopy(record)
    q = result['question']
    for key in (':question/problem', ':question/worked-solution'):
        if key in q:
            q[key] = library.text(q[key])
    for field in q.get(':question/answer-fields', []):
        for answer in field.get(':answer-field/choices', []):
            value = answer[':answer/value']
            if enum(answer[':answer/type']) == ':answer.type/image' and not any(tag in value for tag in ('<img', '![')):
                answer[':answer/value'] = library.resolve(value)
            else:
                answer[':answer/value'] = library.text(value)
            if ':answer/feedback' in answer:
                answer[':answer/feedback'] = library.text(answer[':answer/feedback'])
    result['assets'] = library.saved
    return result


def validate_knowledge_point(value, kp_id, kp_uuid):
    """Accept legacy scalar IDs and the existing generator metadata envelope."""
    if isinstance(value, dict):
        if not any(key in value for key in ('db_id', 'id')):
            raise ValueError('Knowledge-point metadata requires db_id or id')
        if 'db_id' in value:
            db_id = value['db_id']
            if (type(db_id) is not int and not (isinstance(db_id, str) and db_id.isdigit())) or int(db_id) != int(kp_id):
                raise ValueError('Candidate belongs to another knowledge point (db_id)')
        if 'id' in value:
            try:
                identity = uuid.UUID(str(value['id']))
            except (ValueError, TypeError, AttributeError) as error:
                raise ValueError('Knowledge-point metadata id must be a UUID') from error
            if identity != uuid.UUID(str(kp_uuid)):
                raise ValueError('Candidate belongs to another knowledge point (UUID)')
    elif value not in (None, int(kp_id), str(kp_id)):
        raise ValueError('Candidate belongs to another knowledge point')


def validate_question(q):
    for key in (':question/problem', ':question/worked-solution'):
        if not isinstance(q.get(key), str) or not q[key].strip():
            raise ValueError('Generated question requires nonempty ' + key)
    if ':question/math-academy-id' in q:
        raise ValueError('Generated content cannot claim a Math Academy source identity')
    if enum(q.get(':question/difficulty')) not in {':question.difficulty/' + x for x in ('easy', 'moderate', 'hard')}:
        raise ValueError('Generated question requires a supported difficulty')
    fields = q.get(':question/answer-fields')
    if not isinstance(fields, list) or not fields:
        raise ValueError('Generated practice requires gradable answer fields')
    keys = set()
    checkbox_correct_values = []
    for field in fields:
        key = field.get(':answer-field/key')
        if not isinstance(key, str) or not key or key in keys:
            raise ValueError('Answer-field keys must be nonempty and unique')
        keys.add(key)
        kind = enum(field.get(':answer-field/type'))
        if kind not in {':answer-field.type/' + x for x in ('radio', 'select', 'blank', 'checkbox')}:
            raise ValueError('Generated practice requires automatically gradable fields')
        choices = field.get(':answer-field/choices', [])
        typed_values, ids = set(), set()
        for a in choices:
            aid = str(a[':answer/id'])
            uuid.UUID(aid)
            value, atype = a.get(':answer/value'), enum(a.get(':answer/type'))
            if not isinstance(value, str) or not value.strip() or atype not in {':answer.type/' + x for x in ('math', 'text', 'image')}:
                raise ValueError('Generated answer is empty or has an unsupported type')
            if aid in ids or (atype, value) in typed_values:
                raise ValueError('Answer bank contains duplicate identities or typed values')
            ids.add(aid)
            typed_values.add((atype, value))
        if answer_id(field.get(':answer-field/correct')) not in ids:
            raise ValueError('Canonical answer must belong to its field bank')
        if kind in (':answer-field.type/radio', ':answer-field.type/select') and len(choices) < 2:
            raise ValueError('Selection field requires alternatives')
        if kind == ':answer-field.type/blank' and next(enum(a[':answer/type']) for a in choices if str(a[':answer/id']) == answer_id(field[':answer-field/correct'])) not in (':answer.type/math', ':answer.type/text'):
            raise ValueError('Blank canonical answer must be math or text')
        if kind == ':answer-field.type/checkbox' and typed_values != {(':answer.type/text', 'true'), (':answer.type/text', 'false')}:
            raise ValueError('Checkbox bank requires exactly true and false text answers')
        if kind == ':answer-field.type/checkbox':
            checkbox_correct_values.append(next(a[':answer/value'] for a in choices
                                                if str(a[':answer/id']) == answer_id(field[':answer-field/correct'])))
    if checkbox_correct_values and 'true' not in checkbox_correct_values:
        raise ValueError('Generated checkbox questions require at least one correct selectable option')


def stable_identities(question, kp_uuid):
    """Content identities survive changed seeds and option ordering."""
    validate_question(question)
    q = copy.deepcopy(question)
    qid = uuid.uuid5(uuid.UUID(str(kp_uuid)), 'generated-question:' + content_fingerprint(q))
    q[':question/id'] = str(qid)
    for field in q[':question/answer-fields']:
        fid = uuid.uuid5(qid, 'field:' + field[':answer-field/key'])
        old_correct = answer_id(field[':answer-field/correct'])
        field[':answer-field/id'] = str(fid)
        for a in field[':answer-field/choices']:
            old_id = str(a[':answer/id'])
            a[':answer/id'] = str(uuid.uuid5(fid, digest([enum(a[':answer/type']), a[':answer/value']])))
            if old_id == old_correct:
                field[':answer-field/correct'] = [':answer/id', a[':answer/id']]
    return q


def prepare_records(records, kp_id, kp_uuid, fingerprints, math_root, assets_directory, *, localizer=localize_record):
    """Shared preparation/filtering for publication and offline delivery audits.

    No database operations. The localizer controls where image bytes are staged.
    Invalid records fail the batch; only content duplicates are skipped.
    """
    seen = set(fingerprints)
    accepted, duplicate_count = [], 0
    for rec in records:
        validate_knowledge_point(rec.get('knowledge_point'), kp_id, kp_uuid)
        localized = localizer(rec, math_root, assets_directory)
        localized['question'] = stable_identities(localized['question'], kp_uuid)
        fingerprint = content_fingerprint(localized['question'])
        if fingerprint in seen:
            duplicate_count += 1
            continue
        accepted.append(localized)
        seen.add(fingerprint)
    from scripts.integration_batch_policy import validate_delivery_batch
    validate_delivery_batch(accepted, kp_id)
    return accepted, duplicate_count


def verify_assets(records, math_root):
    for record in records:
        for asset in record.get('assets', {}).values():
            relative = Path(asset['path'])
            if relative.is_absolute() or relative.parts[0] != 'images' or '..' in relative.parts:
                raise VerificationError('Asset escaped the image store')
            data = (Path(math_root) / relative).read_bytes()
            if hashlib.sha256(data).hexdigest() != asset['sha256'] or len(data) != asset['bytes']:
                raise VerificationError('Published image bytes differ from preparation')


def validate_report(report, batch, snapshot, *, committed=False):
    """Compare every receipt datom, including the sole permitted registration replacement."""
    if committed and report.get(':edb/committed') is not True:
        raise VerificationError('EDB did not confirm a commit')
    names = {r[0]: str(r[1]).lstrip(':') for r in snapshot['attributes']}
    types = {str(r[1]).lstrip(':'): str(r[2]) for r in snapshot['attributes']}
    idents = {str(ident): eid for eid, ident in snapshot['idents']}
    source = idents.get(batch['source'])
    if source is None:
        raise VerificationError('Configured generated-content contributor is absent')
    tempids = report.get(':edb/tempids', {})
    def entity(value):
        return tempids.get(value, idents.get(str(value), value)) if isinstance(value, str) else value
    def expected(rows):
        return {(entity(e), str(a).lstrip(':'), dumps(entity(v) if types.get(str(a).lstrip(':')) == ':db.type/ref' else v)) for e, a, v in rows}
    observed = {True: set(), False: set()}
    for row in report.get(':edb/tx-data', []):
        if len(row) != 6 or type(row[-1]) is not bool:
            raise VerificationError('Malformed receipt datom')
        eid, aid, value, tx, contributor, added = row
        if contributor != source:
            raise VerificationError('Receipt contributor differs from prepared source')
        name = names.get(aid)
        if name == 'db/txInstant' and added:
            continue
        if name not in ALLOWED:
            raise VerificationError('Receipt changes protected or unknown content: ' + str(name))
        observed[added].add((eid, name, dumps(value)))
    if observed[True] != expected(batch['assertions']) or observed[False] != expected(batch['retractions']):
        raise VerificationError('Receipt differs from the exact prepared assertions and retractions')
    return {'learner_and_engine_facts_unchanged': True, 'source_eid': source}


class GeneratorCommitter(Committer):
    def submit(self, request):
        envelope_path = self.directory / 'receipt-request.json'
        envelope = read_json(envelope_path)
        if envelope and envelope.get('request_key') == request['request_key']:
            receipt = loads(envelope['receipt_edn'])
            if receipt.get(':edb/committed') is True and (receipt.get(':edb/report-error') or not all(
                key in receipt for key in (':edb/db-before-t', ':edb/db-after-t', ':edb/tempids', ':edb/tx-data')
            )):
                # A receipt can confirm the write while report materialization fails.
                # Preserve that evidence and recover the full report with the same request.
                atomic_json(self.directory / 'receipt-incomplete.json', envelope)
                envelope_path.unlink()
        return super().submit(request)

    def preview(self, batch, snapshot):
        atomic_text(self.directory / 'transaction.edn', dumps(batch['forms']) + '\n')
        result = self.client.command('with', '--file', self.directory / 'transaction.edn', '--source', batch['source'])
        atomic_text(self.directory / 'preview.edn', result)
        report = loads(result)
        if report.get(':edb/committed') is not False:
            raise VerificationError('Preview did not identify a speculative transaction')
        if report.get(':edb/db-before-t') != snapshot['basis']:
            raise StaleBasis('Database advanced during preparation')
        validate_report(report, batch, snapshot)
        return report

    def verify_receipt(self, request, receipt):
        if receipt.get(':edb/db-before-t') != request['basis']:
            raise VerificationError('Receipt basis differs from saved request')
        return validate_report(receipt, loads(request['batch_edn']), loads(request['snapshot_edn']), committed=True)


class Publisher:
    def __init__(self, config, client):
        self.config, self.client = config, client

    @classmethod
    def from_environment(cls, database='math', source=':application/ca-engine', *, environment=None, repo_root=ROOT):
        # Same environment resolver as the running learner application.
        if str(ROOT / 'scripts') not in sys.path:
            sys.path.insert(0, str(ROOT / 'scripts'))
        from serve_graph_explorer import database_environment
        environment = database_environment(database) if environment is None else dict(environment)
        repo_root = Path(repo_root)
        config = SimpleNamespace(database=database, source=source, endpoint=environment['EDB_ENDPOINT'],
            postgres_url=environment['EDB_POSTGRES_URL'], math_root=Path(environment['EDB_MATH_ROOT']),
            repo_root=repo_root, request_directory=Path(environment.get('LEARNING_REQUEST_DIR', repo_root / '.local/learning/requests' / database)),
            edb_bin=Path(environment.get('EDB_BIN', repo_root / '.local/edb/capture-runtime/math-edb')),
            preview_bin=None, capture_only=False)
        client = EDBClient(config, threading.Event())
        client.environment = environment
        return cls(config, client)

    def read_kp(self, kp_id, directory, basis):
        rows = self.client.query(KP_QUERY, [int(kp_id)], directory, 'kp', basis)
        if len(rows) != 1:
            raise ValueError('Expected one knowledge point')
        return rows[0][0]

    def save_inventory(self, kp_id, kp, status, basis, directory):
        """Read-only delivery evidence, separate from instructional identity."""
        questions = kp.get(':knowledge-point/questions', [])
        canonical = kp.get(':knowledge-point/canonical-example')
        fingerprints = {content_fingerprint(q) for q in questions}
        if canonical:
            fingerprints.add(content_fingerprint(canonical))
        inventory = {'database': status['database'], 'lineage': status['lineage'],
                     'basis': basis, 'kp_id': int(kp_id), 'questions': jsonable(questions),
                     'canonical_example': jsonable(canonical), 'fingerprints': sorted(fingerprints)}
        atomic_json(Path(directory) / 'inventory.json', inventory)
        return inventory

    def extract_inventory(self, kp_id, directory):
        status = self.client.status()
        kp = self.read_kp(kp_id, Path(directory), status['basis'])
        return self.save_inventory(kp_id, kp, status, status['basis'], directory)

    def extract_source(self, kp_id, directory, *, basis=None):
        directory = Path(directory)
        status = self.client.status()
        basis = status['basis'] if basis is None else basis
        kp = self.read_kp(kp_id, directory, basis)
        return self._source_from_kp(kp_id, directory, status, basis, kp)

    def _source_from_kp(self, kp_id, directory, status, basis, kp):
        """Finish a source capture using the KP already read at this exact basis."""
        self.save_inventory(kp_id, kp, status, basis, directory)
        topic_pattern = '[* {:topic/knowledge-points [:db/id :knowledge-point/id :knowledge-point/title {:knowledge-point/canonical-example ' + QUESTION_PULL + '}]}]'
        topics = self.client.query('[:find (pull ?t ' + topic_pattern + ') :in $ ?kp :where [?t :topic/knowledge-points ?kp]]', [int(kp_id)], directory, 'topics', basis)
        content = '[* {:knowledge-point/canonical-example ' + QUESTION_PULL + '}]'
        lesson_pattern = '[* {:activity/type [:db/ident]} {:activity/steps [* {:step/content ' + content + '}]}]'
        lessons = self.client.query('[:find (pull ?a ' + lesson_pattern + ') :in $ [?t ...] :where [?a :activity/scope ?t] [?a :activity/type :activity.type/lesson]]', [[r[0][':db/id'] for r in topics]], directory, 'lessons', basis) if topics else []
        prerequisites = self.client.query('[:find (pull ?t ' + topic_pattern + ') :in $ [?t ...] :where [?t :topic/id _]]',
            [[p[':db/id'] for p in kp.get(':knowledge-point/key-prerequisites', [])]], directory, 'prerequisites', basis) if kp.get(':knowledge-point/key-prerequisites') else []
        material = {'kp': copy.deepcopy(kp), 'topics': [r[0] for r in topics], 'lessons': [r[0] for r in lessons],
                    'prerequisites': [r[0] for r in prerequisites]}
        material = instructional_material(material)
        # Pull cardinality-many collection order is not instructional order; step/next is.
        def canonical(value):
            if isinstance(value, dict):
                return {str(k): canonical(v) for k, v in value.items()}
            if isinstance(value, (list, tuple)):
                children = [canonical(v) for v in value]
                # Lookup refs are positional; ordinary Pull collections are sets.
                if value and isinstance(value[0], str) and value[0].startswith(':'):
                    return children
                return sorted(children, key=lambda v: json.dumps(v, sort_keys=True))
            return jsonable(value)
        material = canonical(material)
        image_sources = set()
        def find_images(value):
            if isinstance(value, dict):
                if ':answer/type' in value and enum(value[':answer/type']) == ':answer.type/image':
                    source = value.get(':answer/value', '')
                    if '<img' not in source and '![' not in source:
                        image_sources.add(source)
                for child in value.values():
                    find_images(child)
            elif isinstance(value, list):
                for child in value:
                    find_images(child)
            elif isinstance(value, str):
                image_sources.update(re.findall(r'!\[[^\]]*\]\(<?([^\s)>]+)', value))
                image_sources.update(re.findall(r'<img\b[^>]*?\bsrc=["\']([^"\']+)', value, re.I))
        find_images(material)
        images = []
        for source in sorted(image_sources):
            path = Path(source)
            if not path.is_absolute():
                path = Path(self.config.math_root) / path
            item = {'source': source, 'path': str(path)}
            if path.is_file():
                data = path.read_bytes()
                item.update(sha256=hashlib.sha256(data).hexdigest(), bytes=len(data))
            else:
                item['missing'] = True
            images.append(item)
        material['images'] = images
        result = {'database': status['database'], 'lineage': status['lineage'], 'basis': basis,
                  'kp_id': int(kp_id), 'material': material, 'source_sha256': digest(material),
                  'registered_generator': jsonable(kp.get(':knowledge-point/question-generator')),
                  'available_difficulties': [band for band in ('easy', 'moderate', 'hard')
                      if any(enum(q.get(':question/difficulty')) == ':question.difficulty/' + band
                             for q in kp.get(':knowledge-point/questions', []))]}
        atomic_json(directory / 'source.json', result)
        return result

    def prepare(self, kp_id, records, generator_path, package_hash, directory, *, source_snapshot=None, assets_directory=None,
                expected_registered_generator=None):
        directory = Path(directory)
        directory.mkdir(parents=True, exist_ok=True)
        if (directory / 'request.json').exists():
            raise ValueError('Recover pending publication before preparing new content')
        status = self.client.status()
        basis = status['basis']
        kp = self.read_kp(kp_id, directory / 'before', basis)
        if expected_registered_generator is not None:
            registered = (kp.get(':knowledge-point/question-generator') or {}).get(':question-generator/script')
            if registered != expected_registered_generator:
                raise SourceChanged('Registered generator changed; refresh the refill job')
        if source_snapshot is not None:
            fresh = self._source_from_kp(kp_id, directory / 'source-check', status, basis, kp)
            if source_snapshot.get('source_sha256') != digest(source_snapshot.get('material')):
                raise SourceChanged('Saved instructional source evidence failed its integrity check')
            if (any(source_snapshot.get(k) != fresh[k] for k in ('database', 'lineage'))
                    or digest(instructional_material(source_snapshot['material'])) != digest(instructional_material(fresh['material']))):
                raise SourceChanged('Original instructional source changed; review the generator again')
        if len(package_hash) != 64 or any(c not in '0123456789abcdef' for c in package_hash):
            raise ValueError('Invalid package SHA-256')
        package_path = Path(generator_path)
        if package_path.is_absolute() or '..' in package_path.parts or package_path.parts[:2] != ('generators', package_hash[:2]) or package_hash not in package_path.parts:
            raise ValueError('Registration must identify the immutable generator package')
        existing = kp.get(':knowledge-point/questions', [])
        seen = {content_fingerprint(q) for q in existing}
        canonical = kp.get(':knowledge-point/canonical-example')
        if canonical:
            seen.add(content_fingerprint(canonical))
        accepted, duplicate_count = prepare_records(
            records, kp_id, kp[':knowledge-point/id'], seen,
            self.config.math_root, assets_directory or directory)
        identities = [uuid.UUID(qid) for rec in accepted for qid in [rec['question'][':question/id']] + [f[':answer-field/id'] for f in rec['question'][':question/answer-fields']] + [a[':answer/id'] for f in rec['question'][':question/answer-fields'] for a in f[':answer-field/choices']]]
        if identities:
            collisions = self.client.query('[:find ?e ?id :in $ [?id ...] :where (or-join [?e ?id] [?e :question/id ?id] [?e :answer-field/id ?id] [?e :answer/id ?id])]', [identities], directory, 'identity-collisions', basis)
            if collisions:
                raise ValueError('Existing identities require reconciliation; no served content may be overwritten')
        generator_uuid = uuid.uuid5(uuid.UUID(str(kp[':knowledge-point/id'])), 'generator-package:' + package_hash)
        generator_rows = self.client.query('[:find (pull ?g [*]) :in $ ?id :where [?g :question-generator/id ?id]]', [generator_uuid], directory, 'generator-identity', basis)
        old_generator = kp.get(':knowledge-point/question-generator')
        forms, assertions, retractions = [], [], []
        def add(entity, attr, value):
            forms.append([kw('db/add'), entity, kw(attr), value])
            assertions.append([entity, kw(attr), value])
        for rec in accepted:
            q = rec['question']
            for field in q[':question/answer-fields']:
                for a in field[':answer-field/choices']:
                    aid = a[':answer/id']
                    add(aid, 'answer/id', uuid.UUID(aid))
                    add(aid, 'answer/type', kw(enum(a[':answer/type'])))
                    add(aid, 'answer/value', a[':answer/value'])
                    if ':answer/feedback' in a:
                        add(aid, 'answer/feedback', a[':answer/feedback'])
                    forms.append([kw('db/ensure'), aid, kw('answer/validate')])
                fid = field[':answer-field/id']
                add(fid, 'answer-field/id', uuid.UUID(fid))
                add(fid, 'answer-field/key', field[':answer-field/key'])
                add(fid, 'answer-field/type', kw(enum(field[':answer-field/type'])))
                for a in field[':answer-field/choices']:
                    add(fid, 'answer-field/choices', a[':answer/id'])
                add(fid, 'answer-field/correct', answer_id(field[':answer-field/correct']))
                forms.append([kw('db/ensure'), fid, kw('answer-field/validate')])
            qid = q[':question/id']
            add(qid, 'question/id', uuid.UUID(qid))
            for name in ('problem', 'worked-solution', 'requires-calculator'):
                if ':question/' + name in q:
                    add(qid, 'question/' + name, q[':question/' + name])
            add(qid, 'question/difficulty', kw(enum(q[':question/difficulty'])))
            for field in q[':question/answer-fields']:
                add(qid, 'question/answer-fields', field[':answer-field/id'])
            forms.append([kw('db/ensure'), qid, kw('question/validate')])
            add(int(kp_id), 'knowledge-point/questions', qid)
        if generator_rows:
            if len(generator_rows) != 1 or generator_rows[0][0].get(':question-generator/script') != generator_path:
                raise ValueError('Immutable generator identity has different registered content')
            generator_entity = generator_rows[0][0][':db/id']
        else:
            generator_entity = 'generator'
            add(generator_entity, 'question-generator/id', generator_uuid)
            add(generator_entity, 'question-generator/script', generator_path)
        if not old_generator or str(old_generator.get(':question-generator/id')) != str(generator_uuid):
            add(int(kp_id), 'knowledge-point/question-generator', generator_entity)
            if old_generator:
                retractions.append([int(kp_id), kw('knowledge-point/question-generator'), old_generator[':db/id']])
        if forms:
            forms.append([kw('db/ensure'), int(kp_id), kw('knowledge-point/validate')])
        attributes = self.client.query('[:find ?a ?ident ?type :where [?a :db/ident ?ident] [?a :db/valueType ?v] [?v :db/ident ?type]]', [], directory, 'attributes', basis)
        idents = self.client.query('[:find ?e ?ident :where [?e :db/ident ?ident]]', [], directory, 'idents', basis)
        if self.config.source not in {str(i) for e, i in idents}:
            raise ValueError('Configured generated-content contributor does not exist')
        snapshot = {'basis': basis, 'lineage': status['lineage'], 'attributes': attributes, 'idents': idents}
        batch = {'source': self.config.source, 'forms': forms, 'assertions': assertions, 'retractions': retractions}
        prepared = {'database': status['database'], 'lineage': status['lineage'], 'basis': basis, 'kp_id': int(kp_id),
                    'package_sha256': package_hash, 'generator_path': generator_path, 'generator_id': str(generator_uuid),
                    'new_questions': len(accepted), 'duplicates': duplicate_count,
                    'batch_edn': dumps(batch), 'snapshot_edn': dumps(snapshot), 'before_edn': dumps(kp), 'records': jsonable(accepted)}
        atomic_json(directory / 'preparation.json', prepared)
        verify_assets(accepted, self.config.math_root)
        return prepared

    def publish(self, directory):
        directory = Path(directory)
        # This is the same learner API lock used by prior generator publication.
        request_directory = Path(getattr(self.config, 'request_directory', Path(self.config.repo_root) / '.local/learning/requests' / self.config.database))
        with file_lock(request_directory / 'api.lock'):
            committer = GeneratorCommitter(self.config, self.client, directory)
            prepared = read_json(directory / 'preparation.json')
            if prepared is None:
                raise ValueError('Publication requires a saved preparation')
            if prepared['database'] != self.config.database:
                raise ValueError('Preparation belongs to a different database')
            request = committer.pending()
            if request is None:
                resolve_registered_script(prepared['generator_path'], Path(self.config.repo_root), Path(self.config.math_root))
                verify_assets(prepared['records'], self.config.math_root)
                verified = read_json(directory / 'verification.json')
                if verified and verified.get('package_sha256') == prepared['package_sha256'] and verified.get('preparation_sha256') == digest(prepared):
                    return verified
                batch, snapshot = loads(prepared['batch_edn']), loads(prepared['snapshot_edn'])
                if not batch['forms']:
                    status = self.client.status()
                    if status['lineage'] != prepared['lineage']:
                        raise VerificationError('No-change preparation belongs to a different database lineage')
                    if status['basis'] != prepared['basis']:
                        raise StaleBasis('Database advanced after no-change preparation')
                    current = self.read_kp(prepared['kp_id'], directory / 'readback', prepared['basis'])
                    gen = current.get(':knowledge-point/question-generator', {})
                    if str(gen.get(':question-generator/id')) != prepared['generator_id'] or gen.get(':question-generator/script') != prepared['generator_path']:
                        raise VerificationError('No-change registration differs from the approved package')
                    result = {'status': 'no_changes', 'passed': True, 'basis_after': prepared['basis'], 'new_questions': 0,
                              'package_sha256': prepared['package_sha256'], 'preparation_sha256': digest(prepared)}
                    atomic_json(directory / 'verification.json', result)
                    return result
                committer.preview(batch, snapshot)
                request = committer.save_request(batch, snapshot, digest(prepared))
            if request['content_sha256'] != digest(prepared):
                raise VerificationError('Saved preparation changed after request creation')
            try:
                receipt = committer.submit(request)
            except StaleBasis:
                committer.retire(request, 'rejected_stale_basis', {'reason': 'confirmed writer rejection; prepare at a fresh basis'})
                raise
            committer.verify_receipt(request, receipt)
            basis = receipt[':edb/db-after-t']
            kp = self.read_kp(prepared['kp_id'], directory / 'readback', basis)
            before = loads(prepared['before_edn'])
            old = {str(q[':question/id']): q for q in before.get(':knowledge-point/questions', [])}
            now = {str(q[':question/id']): q for q in kp.get(':knowledge-point/questions', [])}
            if len(now) != len(old) + prepared['new_questions'] or any(now.get(qid) != q for qid, q in old.items()):
                raise VerificationError('Readback changed existing question content or pool membership')
            excluded = {':knowledge-point/questions', ':knowledge-point/question-generator'}
            if {k: v for k, v in before.items() if k not in excluded} != {k: v for k, v in kp.items() if k not in excluded}:
                raise VerificationError('Readback changed unrelated knowledge-point content')
            gen = kp.get(':knowledge-point/question-generator', {})
            if str(gen.get(':question-generator/id')) != prepared['generator_id'] or gen.get(':question-generator/script') != prepared['generator_path']:
                raise VerificationError('Registered generator does not identify the approved package')
            for rec in prepared['records']:
                qid = rec['question'][':question/id']
                actual = now.get(qid)
                if actual is None or ':question/math-academy-id' in actual or normalized_question(actual) != normalized_question(rec['question']):
                    raise VerificationError('Readback question differs from prepared content')
            verify_assets(prepared['records'], self.config.math_root)
            resolve_registered_script(prepared['generator_path'], Path(self.config.repo_root), Path(self.config.math_root))
            result = {'status': 'verified', 'passed': True, 'basis_before': request['basis'], 'basis_after': basis,
                      'new_questions': prepared['new_questions'], 'package_sha256': prepared['package_sha256'],
                      'preparation_sha256': digest(prepared), 'request_key': request['request_key'],
                      'generator_registration_verified': True, 'learner_and_engine_facts_unchanged': True}
            atomic_json(directory / 'verification.json', result)
            committer.retire(request, 'verified', result)
            return result
