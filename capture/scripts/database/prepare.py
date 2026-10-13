"""Prepare source content against one snapshot without changing the database."""
from __future__ import annotations
import copy
import hashlib
import json
import uuid
from .edn import kw, dumps
from .evidence import UnsupportedContent, authoritative_question
from .images import ImageLibrary, MissingImage
from .text import markdown
from .difficulty import calibrate
from ..activity.evidence import question_key
from ..activity.task_payload import semantic_identity, task_payload

MA_SOURCE = ':org/Math-Academy'
KINDS = ('topic', 'knowledge-point', 'question', 'answer-field', 'answer', 'tutorial',
         'activity', 'step', 'multistep', 'assigned-problem')
ALLOWED = {f'{kind}/{name}' for kind, names in {
    'topic': ('id', 'math-academy-id', 'title', 'knowledge-points', 'difficulty'),
    'knowledge-point': ('id', 'title', 'canonical-example', 'questions'),
    'question': ('id', 'math-academy-id', 'problem', 'worked-solution', 'difficulty', 'requires-calculator', 'answer-fields'),
    'answer-field': ('id', 'key', 'type', 'choices', 'correct'),
    'answer': ('id', 'type', 'value', 'feedback'),
    'tutorial': ('id', 'math-academy-id', 'title', 'content'),
    'activity': ('id', 'math-academy-id', 'title', 'type', 'scope', 'course', 'steps', 'first-step', 'time-limit-seconds', 'expected-seconds'),
    'step': ('id', 'math-academy-id', 'content', 'next', 'time-limit-seconds', 'expected-seconds'),
    'diagnostic-probe': ('on-correct', 'on-incorrect', 'on-skipped', 'on-silly-mistake'),
    'multistep': ('id', 'context', 'steps', 'first-step'),
    'assigned-problem': ('id', 'content', 'topic-coverage'),
}.items() for name in names}


def source_uuid(kind, value):
    return uuid.uuid5(uuid.NAMESPACE_URL, f'course-academy:ma:{kind}:{value}')

def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False, default=str).encode()).hexdigest()

def activity_identity(content, kind):
    """Use the same authored route identity for preparation and snapshot reads."""
    verified_id = content.get('activity_definition_id')
    # An unresolved capture key preserves the observed route without claiming a
    # Math Academy identity. Preparation omits structures that still use it.
    order = content.get('question_order') or [question_key(q) for q in content.get('questions', [])]
    route = [(mid, (content.get('question_outcomes') or {}).get(mid)) for mid in order]
    return source_uuid(kind, verified_id if verified_id else digest([content.get('course_id'), content.get('topic_id'), route]))


def scalar(value):
    return value.get(':db/id', value.get(':db/ident')) if isinstance(value, dict) else value


class Snapshot:
    def __init__(self, data):
        self.basis = data['basis']
        self.lineage = data.get('lineage')
        self.entities = {e[':db/id']: e for e in data.get('entities', [])}
        self.idents = {str(ident): eid for eid, ident in data.get('idents', [])}
        self.attributes = {str(r[1]).lstrip(':'): {'id': r[0], 'type': str(r[2]), 'many': str(r[3]) == ':db.cardinality/many'}
                           for r in data.get('attributes', [])}
        attr_names = {r[0]: str(r[1]).lstrip(':') for r in data.get('attributes', [])}
        self.facts = {(e, attr_names.get(a, a), dumps(v), s) for e, a, v, s in data.get('facts', [])}
        self.has_facts = 'facts' in data

    def find(self, attr, value):
        return [e for e in self.entities.values() if str(e.get(':' + attr)) == str(value)]

    def enum(self, value):
        if isinstance(value, str) and value.startswith(':'):
            return self.idents.get(value, value)
        return scalar(value)

    def sourced(self, entity, attr, value, source):
        return not self.has_facts or (entity, attr, dumps(self.enum(value)), self.idents.get(source)) in self.facts


class Plan:
    """Only explicit domain facts can enter a transaction; diff all removals."""
    def __init__(self, snapshot, source=MA_SOURCE):
        self.snapshot, self.source = snapshot, source
        self.forms, self.assertions, self.retractions = [], [], []
        self.local = {}
        self.updates = {}

    def entity(self, kind, identity, old=None):
        identity = uuid.UUID(str(identity))
        token = old[':db/id'] if old else f'{kind}-{identity}'
        self.local[(kind, str(identity))] = token
        if token not in self.updates:
            self.updates[token] = {kw('db/id'): token}
            if not old:
                self.set(token, old, kind + '/id', identity)
        return token

    def set(self, target, old, attr, desired, *, replace=False, many=False):
        if attr not in ALLOWED:
            raise ValueError('Attempt to prepare a non-content attribute: ' + attr)
        previous = (old or {}).get(':' + attr)
        if many:
            previous = previous or []
            wanted = list(dict.fromkeys(desired))
            old_values = {self.snapshot.enum(v): v for v in previous}
            for value in wanted:
                if self.snapshot.enum(value) not in old_values or not self.snapshot.sourced(target, attr, value, self.source):
                    self.updates.setdefault(target, {kw('db/id'): target}).setdefault(kw(attr), []).append(value)
                    self.assertions.append([target, kw(attr), value])
            if replace:
                wanted_values = {self.snapshot.enum(v) for v in wanted}
                for value in old_values.keys() - wanted_values:
                    self.retract(target, attr, value)
            return
        if desired is None:
            if replace and previous is not None:
                self.retract(target, attr, self.snapshot.enum(previous))
            return
        # A later observation supersedes an earlier planned scalar even when
        # it agrees with the snapshot. Otherwise successive preparations can
        # alternate between the two values forever.
        self.assertions = [row for row in self.assertions if not (row[0] == target and row[1] == kw(attr))]
        self.retractions = [row for row in self.retractions if not (row[0] == target and row[1] == kw(attr))]
        self.updates.setdefault(target, {kw('db/id'): target}).pop(kw(attr), None)
        if self.snapshot.enum(previous) != self.snapshot.enum(desired) or not self.snapshot.sourced(target, attr, desired, self.source):
            self.updates.setdefault(target, {kw('db/id'): target})[kw(attr)] = desired
            self.assertions.append([target, kw(attr), desired])
            if previous is not None and self.snapshot.enum(previous) != self.snapshot.enum(desired):
                self.retractions.append([target, kw(attr), self.snapshot.enum(previous)])

    def retract(self, target, attr, value):
        self.forms.append([kw('db/retract'), target, kw(attr), value])
        self.retractions.append([target, kw(attr), value])

    def finish(self):
        for update in self.updates.values():
            if len(update) > 1:
                old = self.snapshot.entities.get(update[kw('db/id')], {})
                kind = next((k for k in KINDS if ':' + k + '/id' in update or ':' + k + '/id' in old), None)
                if kind:
                    spec = kind + ('/identity-validate' if kind == 'topic' else '/validate')
                    if kind == 'knowledge-point' and not old:
                        required = ('knowledge-point/title', 'knowledge-point/canonical-example', 'knowledge-point/questions')
                        if any(not update.get(kw(a)) for a in required):
                            raise ValueError('New knowledge point is missing required supported content')
                    update[kw('db/ensure')] = [kw(spec)]
                self.forms.append(update)
        return {'source': self.source, 'forms': self.forms,
                'assertions': list({dumps(v): v for v in self.assertions}.values()),
                'retractions': list({dumps(v): v for v in self.retractions}.values())}


class Preparation:
    def __init__(self, snapshot, *, resolve=None, record_source_evidence=None):
        self.snapshot = Snapshot(snapshot)
        self.resolve = resolve
        self.record_source_evidence = record_source_evidence
        self.decisions, self.omissions = [], []
        self.gap_judgments = {}

    def identity_candidate(self, entity):
        """Relevant authored content without entire topic practice pools."""
        reference_keys = {'step/next', 'activity/first-step', 'multistep/first-step',
                          'activity/scope', 'activity/course', 'topic/knowledge-points',
                          'assigned-problem/topic-coverage'}
        identity_keys = {':db/id', ':db/ident'} | {':' + k + '/' + name for k in KINDS + ('course',)
                                                for name in ('id', 'math-academy-id', 'title')}
        def reference(value):
            if isinstance(value, dict):
                return {key: val for key, val in value.items() if key in identity_keys}
            if isinstance(value, list):
                return [reference(item) for item in value]
            return value
        def summarize(value):
            if isinstance(value, list):
                return [summarize(item) for item in value]
            if not isinstance(value, dict):
                return value
            full = self.snapshot.entities.get(value.get(':db/id'), value)
            result = {}
            for key, child in full.items():
                attr = str(key).lstrip(':')
                if attr == 'knowledge-point/questions':
                    result['practice_question_count'] = len(child)
                elif key in identity_keys or attr in ALLOWED:
                    result[key] = reference(child) if attr in reference_keys or attr.startswith('diagnostic-probe/') else summarize(child)
            return result
        return summarize(entity)

    def choose(self, kind, captured, candidates):
        if captured.get('math_academy_id') and ('problem' in captured or 'answer_fields' in captured):
            from ..activity.task_payload import compact_question
            compact = compact_question(captured)
            compact.update({key: captured[key] for key in ('topic_id', 'knowledge_point_id', 'kp_id', 'knowledge_point', 'kp_title', 'title') if key in captured})
            captured = compact
        payload = {'kind': kind, 'captured': captured, 'candidates': [self.identity_candidate(candidate) for candidate in candidates],
                   'instruction': 'Choose a supported existing identity, new only for distinct new content, or unavailable. Do not invent evidence.'}
        if self.resolve is None:
            raise ValueError('Identity judgment required: ' + kind)
        result = self.resolve('resolve_identity', payload)
        choice = result.get('decision')
        self.decisions.append({'kind': kind, 'result': result})
        if choice in ('unavailable', 'unsupported'):
            raise UnsupportedContent(result.get('reasoning') or result.get('reason') or 'Identity unavailable')
        if choice == 'new':
            return None
        eid = str(result.get('entity_id', result.get('entity_uuid', '')))
        found = [e for e in candidates if str(e[':db/id']) == eid or any(str(e.get(':' + k + '/id')) == eid for k in KINDS)]
        if choice not in ('existing', 'match') or len(found) != 1 or not (result.get('evidence') or result.get('reasoning')):
            raise ValueError('Agent returned an invalid identity resolution')
        return found[0]

    def exact(self, attr, value):
        matches = self.snapshot.find(attr, value)
        if len(matches) > 1:
            return self.choose(attr, {'source_id': value}, matches)
        return matches[0] if matches else None

    def existing_ma_answer(self, question, judgment):
        """Corroborate a contradictory worksheet against an existing MA key."""
        if (judgment.get('status') != 'source_error' or not self.record_source_evidence
                or not self.snapshot.has_facts or not self.snapshot.lineage):
            return None
        mid = question.get('math_academy_id')
        matches = self.snapshot.find('question/math-academy-id', mid)
        if not mid or len(matches) != 1:
            return None
        old = matches[0]
        # Only the exact gray sizing placeholder dropped by the legacy
        # extractor may differ; preserve all other math, cells and prose.
        blank = r'\bbox[2pt,lightgray]{\phantom{a}}'
        if markdown(question.get('problem', '')).replace(blank, '') != str(old.get(':question/problem', '')).replace(blank, ''):
            return None
        if not self.snapshot.sourced(old[':db/id'], 'question/math-academy-id', mid, MA_SOURCE):
            return None
        fields = question.get('answer_fields', question.get('fields', []))
        existing = {str(f.get(':answer-field/key')):f for f in old.get(':question/answer-fields', [])}
        answers = {str(a.get('key')):a for a in judgment.get('answers', [])}
        if not fields or len(existing) != len(fields):
            return None
        bound = []
        for field in fields:
            previous, answer = existing.get(str(field.get('key'))), answers.get(str(field.get('key')), {})
            if not previous or field.get('type') not in ('radio', 'select'):
                return None
            old_type = previous.get(':answer-field/type') or {}
            if not isinstance(old_type, dict) or str(old_type.get(':db/ident', '')).rsplit('/', 1)[-1] != field['type']:
                return None
            choices = [(c.get('type'), c.get('value')) for c in field.get('choices', [])]
            old_choices = [(str(c.get(':answer/type', {}).get(':db/ident', '')).rsplit('/', 1)[-1],
                            c.get(':answer/value')) for c in previous.get(':answer-field/choices', [])]
            if (any(t not in ('math', 'text') or not isinstance(v, str) for t,v in choices + old_choices)
                    or len(choices) != len(old_choices) or len(set(choices)) != len(choices)
                    or set(choices) != set(old_choices)):
                return None
            correct = previous.get(':answer-field/correct') or {}
            value_type = str(correct.get(':answer/type', {}).get(':db/ident', '')).rsplit('/', 1)[-1]
            value = correct.get(':answer/value')
            if (answer.get('disagrees') is not True or answer.get('ma_value') is None
                    or (answer.get('value_type'), answer['ma_value']) in choices
                    or (value_type, value) != (answer.get('value_type'), answer.get('correct_value'))
                    or (value_type, value) not in choices
                    or scalar(correct) not in [scalar(c) for c in previous.get(':answer-field/choices', [])]):
                return None
            if not all(self.snapshot.sourced(eid, attr, val, MA_SOURCE) for eid, attr, val in (
                    (previous[':db/id'], 'answer-field/correct', correct),
                    (correct[':db/id'], 'answer/value', value),
                    (correct[':db/id'], 'answer/type', correct[':answer/type']))):
                return None
            bound.append((previous, correct, value_type, value))
        ids = {old[':db/id'], *(p[':db/id'] for p,_,_,_ in bound), *(c[':db/id'] for _,c,_,_ in bound)}
        proof = {'basis':self.snapshot.basis, 'lineage':self.snapshot.lineage, 'source':MA_SOURCE,
                 'question':old, 'facts':[list(f) for f in sorted(self.snapshot.facts, key=str) if f[0] in ids],
                 'source_id':mid, 'judgment':copy.deepcopy(judgment)}
        source_file = self.record_source_evidence(proof)
        repaired = copy.deepcopy(question)
        for field, (previous, correct, value_type, value) in zip(
                repaired.get('answer_fields', repaired.get('fields', [])), bound):
            field.update(correct_value=value, value_type=value_type, correct_type=value_type,
                evidence={'kind':'ma_answer', 'value':value, 'source_file':source_file,
                          'source_kind':'existing_edb_math_academy_answer', 'basis':self.snapshot.basis,
                          'lineage':self.snapshot.lineage, 'question_eid':old[':db/id'],
                          'field_eid':previous[':db/id'], 'answer_eid':correct[':db/id']})
        return repaired

    def prepare(self, content, library=None, derived_source=None):
        content = copy.deepcopy(content)
        if not content.get('question_order'):
            content['question_order'] = [question_key(q) for q in content.get('questions', [])]
        if not content.get('lesson_workload_sample'):
            groups = {}
            for q in content.get('questions', []):
                kp = str(q.get('knowledge_point_id') or q.get('kp_id') or '')
                ids = groups.setdefault(kp, [])
                identity = question_key(q)
                if identity not in ids and len(ids) < 2:
                    ids.append(identity)
            content['lesson_workload_sample'] = {'questions_by_knowledge_point': groups,
                'selection': 'first-two-distinct-practice-questions-in-captured-order', 'base_xp': content.get('base_xp')}
        records, source_repairs = [], []
        for bucket, example in (('questions', False), ('canonical_examples', True)):
            seen = set()
            kept = []
            for original in content.get(bucket, []):
                capture_key = question_key(original)
                if capture_key in seen:
                    continue
                seen.add(capture_key)
                try:
                    q = authoritative_question(original, example=example)
                    if library:
                        q = library.question(q)
                    for key in ('problem', 'worked_solution', 'local_problem'):
                        if isinstance(q.get(key), str):
                            q[key] = markdown(q[key])
                    kept.append(q)
                    records.append((q, example))
                except (UnsupportedContent, MissingImage) as error:
                    judgment = self.final_judgment(content, original, error, record_kind=bucket)
                    repaired = copy.deepcopy(original)
                    answers = {a.get('key'): a for a in judgment.get('answers', [])}
                    for field in repaired.get('answer_fields', repaired.get('fields', [])):
                        answer = answers.get(field.get('key'), {})
                        evidence = answer.get('ma_evidence') or answer.get('evidence')
                        if isinstance(evidence, dict) and evidence and answer.get('ma_value') is not None:
                            field.update(correct_value=answer['ma_value'], evidence=evidence)
                        elif (answer.get('ma_basis') == 'worked_solution' and isinstance(evidence, str)
                              and evidence.strip() and evidence in repaired.get('worked_solution', '')
                              and answer.get('ma_value') is not None):
                            source = repaired.get('solution_evidence') or repaired.get('source_file') or repaired.get('html_path')
                            field.update(correct_value=answer['ma_value'], evidence={
                                'kind': 'worked_solution', 'value': answer['ma_value'],
                                'solution_quote': evidence, 'source_file': source, 'matches_worked_solution': True})
                    corroborated = self.existing_ma_answer(repaired, judgment)
                    if corroborated is not None:
                        repaired = corroborated
                    try:
                        q = authoritative_question(repaired, example=example)
                        source_q = copy.deepcopy(q)
                        if library:
                            q = library.question(q)
                        for key in ('problem', 'worked_solution', 'local_problem'):
                            if isinstance(q.get(key), str):
                                q[key] = markdown(q[key])
                        kept.append(q)
                        records.append((q, example))
                        source_repairs.append({'record_kind': bucket, 'capture_key': capture_key,
                            'source_evidence_hash': semantic_identity('preparation_source', original),
                            'question': source_q, 'judgment': copy.deepcopy(judgment)})
                    except (UnsupportedContent, MissingImage) as final_error:
                        # A checked answer repair can expose a different source
                        # gap. Close that finding too, without another repair loop.
                        judgment = self.final_judgment(content, repaired, final_error, record_kind=bucket)
                        self.omissions.append({'kind': 'question', 'id': original.get('math_academy_id'),
                            'capture_key': capture_key, 'record_kind': bucket,
                            'observed_math_academy_id': original.get('observed_math_academy_id'),
                            'reason': str(final_error), 'judgment': judgment, 'final': True})
            content[bucket] = kept
        # A missing dependency removes the affected structure, never imports a partial question.
        plan = Plan(self.snapshot)
        topic_map, point_map, question_targets = {}, {}, {}
        for q, _ in records:
            tid = q.get('topic_id') or content.get('topic_id')
            if tid is None:
                self.omit_or_resolve(content, q, UnsupportedContent('Question topic unavailable'))
                continue
            tid = int(tid)
            topic = topic_map.get(tid) or self.exact('topic/math-academy-id', tid)
            if not topic:
                definition = content.get('lesson_definition', {})
                title = definition.get('title') if definition.get('complete') and int(definition.get('topic_id') or 0) == tid else None
                if not title:
                    self.omit_or_resolve(content, q, UnsupportedContent('Question topic is absent from the catalog and has no complete source definition'))
                    continue
                identity = source_uuid('topic', tid)
                target = plan.entity('topic', identity)
                plan.set(target, None, 'topic/math-academy-id', tid)
                plan.set(target, None, 'topic/title', title)
                topic = {':db/id': target, ':topic/id': identity, ':topic/math-academy-id': tid,
                         ':topic/title': title, ':topic/knowledge-points': []}
            topic_map[tid] = topic
        # Resolve KPs and example revisions before emitting dependent question facts.
        resolved = []
        examples = {str(q.get('knowledge_point_id') or q.get('kp_id')): q for q, ex in records if ex}
        for q, example in sorted(records, key=lambda row: not row[1]):
            tid = int(q.get('topic_id') or content.get('topic_id') or 0)
            topic = topic_map.get(tid)
            if not topic:
                continue
            kid = str(q.get('knowledge_point_id') or q.get('kp_id') or '')
            points = [self.snapshot.entities.get(scalar(p), p) for p in topic.get(':topic/knowledge-points', [])]
            points = [p for p in points if isinstance(p, dict)]
            existing = self.exact('question/math-academy-id', q['math_academy_id'])
            # History can omit the KP identity. An empty key must not make
            # different question owners share the first resolved point.
            point = point_map.get((tid, kid)) if kid else None
            source_example = q['math_academy_id'] if example else examples.get(kid, {}).get('math_academy_id')
            if not kid and not example:
                # A captured canonical example is stronger identity evidence
                # than a possibly stale practice-pool membership.
                title = q.get('knowledge_point') or q.get('kp_title')
                matching_examples = [r for r, ex in records if ex and title
                    and int(r.get('topic_id') or content.get('topic_id') or 0) == tid
                    and (r.get('knowledge_point') or r.get('kp_title')) == title]
                if len(matching_examples) == 1:
                    source_example = matching_examples[0]['math_academy_id']
            try:
                if point is None:
                    candidates = [p for p in points if str(p.get(':knowledge-point/id')) == kid]
                    if not candidates and source_example:
                        candidates = [p for p in points if p.get(':knowledge-point/canonical-example', {}).get(':question/math-academy-id') == source_example]
                    if not candidates and existing:
                        owners = {scalar(p) for p in existing.get(':knowledge-point/_questions', []) + existing.get(':knowledge-point/_canonical-example', [])}
                        candidates = [p for p in points if p[':db/id'] in owners]
                    if not candidates:
                        title = q.get('knowledge_point') or q.get('kp_title')
                        candidates = [p for p in points if title and p.get(':knowledge-point/title') == title]
                        if candidates and source_example and any(p.get(':knowledge-point/canonical-example', {}).get(':question/math-academy-id') != source_example for p in candidates):
                            point = self.choose('knowledge-point revision', q, candidates)
                        elif len(candidates) == 1:
                            point = candidates[0]
                    if point is None and candidates:
                        point = candidates[0] if len(candidates) == 1 else self.choose('knowledge-point', q, candidates)
                    if point is None:
                        siblings = [r for r, ex in records if not ex and str(r.get('knowledge_point_id') or r.get('kp_id') or '') == kid]
                        if not source_example or not siblings or not content.get('lesson_definition', {}).get('complete'):
                            raise UnsupportedContent('New KP lacks a complete example and practice pool')
                        identity = source_uuid('knowledge-point', f'{tid}:{source_example}')
                        point = {':knowledge-point/id': identity, ':knowledge-point/title': q.get('knowledge_point') or q.get('kp_title') or ''}
                        if not point[':knowledge-point/title']:
                            raise UnsupportedContent('New KP title unavailable')
                    if kid:
                        point_map[(tid, kid)] = point
                if example and not existing and ':db/id' in point:
                    previous = point.get(':knowledge-point/canonical-example')
                    if previous:
                        previous = self.snapshot.entities.get(scalar(previous), previous)
                        # A reused KP and a changed canonical ID require a separate content identity decision.
                        existing = self.choose('canonical-example revision', q, [previous])
                resolved.append((q, example, topic, point, existing))
            except UnsupportedContent as error:
                self.omissions.append({'kind': 'question', 'id': q['math_academy_id'], 'reason': str(error), 'final': True})
        canonical_ids = {scalar(p.get(':knowledge-point/canonical-example')) for p in self.snapshot.entities.values() if p.get(':knowledge-point/canonical-example')}
        accepted, example_targets = [], {}
        for q, example, topic, point, existing in resolved:
            if not example and existing and (existing[':db/id'] in canonical_ids or existing.get(':knowledge-point/_canonical-example')):
                self.omissions.append({'kind': 'question', 'id': q['math_academy_id'], 'reason': 'Canonical example cannot enter a practice pool', 'final': True})
                continue
            try:
                self.check_source_attribution(existing)
            except UnsupportedContent as error:
                self.omissions.append({'kind': 'question', 'id': q['math_academy_id'],
                    'reason': str(error), 'constraint': 'separately_attributed_correction', 'final': True})
                if not example and existing and existing.get(':question/math-academy-id') == q['math_academy_id']:
                    # The corrected entity is usable as an activity reference.
                    # Preserve every corrected fact and learner response; only
                    # point the complete activity at its existing question ID.
                    question_targets[q['math_academy_id']] = existing[':db/id']
                elif (example and existing and ':db/id' in point
                        and scalar(point.get(':knowledge-point/canonical-example')) == existing[':db/id']):
                    example_targets[q['math_academy_id']] = (point[':db/id'],point)
                continue
            try:
                self.check_response_ownership(q, existing)
            except UnsupportedContent as error:
                # This is a proven database-history constraint, not a missing
                # mathematical judgment or a transient writer failure. Do not
                # mutate the question/KP plan or keep retrying this package.
                self.omissions.append({'kind': 'question', 'id': q['math_academy_id'],
                    'reason': str(error), 'constraint': 'historical_response_ownership', 'final': True})
                continue
            old_point = point if ':db/id' in point else None
            pt = plan.entity('knowledge-point', point[':knowledge-point/id'], old_point)
            plan.set(pt, old_point, 'knowledge-point/title', q.get('knowledge_point') or q.get('kp_title') or point.get(':knowledge-point/title'))
            plan.set(topic[':db/id'], topic, 'topic/knowledge-points', [pt], many=True)
            qt = self.question(plan, q, existing, example)
            plan.set(pt, old_point, 'knowledge-point/canonical-example' if example else 'knowledge-point/questions', qt if example else [qt], many=not example)
            q['knowledge_point_id'] = str(point[':knowledge-point/id'])
            q['topic_id'] = int(topic[':topic/math-academy-id'])
            question_targets[q['math_academy_id']] = qt
            if example:
                example_targets[q['math_academy_id']] = (pt, point)
            accepted.append((q, example))
        if not content.get('question_order'):
            content['question_order'] = [q['math_academy_id'] for q in content.get('questions', [])]
        content['questions'] = [q for q, ex in accepted if not ex]
        content['canonical_examples'] = [q for q, ex in accepted if ex]
        if content.get('lesson_definition'):
            try:
                candidate_plan = copy.deepcopy(plan)
                self.lesson(candidate_plan, content, topic_map, example_targets, library)
                plan = candidate_plan
            except (UnsupportedContent, MissingImage) as error:
                self.omissions.append({'kind': 'lesson', 'reason': str(error), 'final': True})
        kind = content.get('task_type') or content.get('kind')
        if kind in ('multistep', 'review', 'assessment', 'diagnostic'):
            try:
                candidate_plan = copy.deepcopy(plan)
                if kind == 'multistep':
                    self.multistep(candidate_plan, content, topic_map, question_targets, library)
                else:
                    self.activity(candidate_plan, content, topic_map, question_targets, kind)
                plan = candidate_plan
            except (UnsupportedContent, MissingImage) as error:
                self.omissions.append({'kind': kind, 'reason': str(error), 'final': True})
        batches = [plan.finish()]
        calibration = None
        if kind == 'lesson':
            try:
                calibration = calibrate(content)
                topic = topic_map.get(int(content.get('topic_id', 0)))
                if derived_source and topic:
                    if derived_source == MA_SOURCE:
                        raise ValueError('Calculated difficulty cannot use the Math Academy source')
                    derived = Plan(self.snapshot, derived_source)
                    derived.set(topic[':db/id'], topic, 'topic/difficulty', calibration['multiplier'])
                    batches.append(derived.finish())
                else:
                    calibration['not_transacted'] = 'Configure derived_source to attribute the calculated multiplier'
            except ValueError as error:
                calibration = {'not_transacted': str(error)}
        return {'basis': self.snapshot.basis, 'batches': [b for b in batches if b['forms']],
                'content': content, 'omissions': self.omissions, 'identity_decisions': self.decisions,
                'calibration': calibration, 'images': library.saved if library else {},
                'source_repairs': source_repairs}

    def final_judgment(self, content, question, error, record_kind=None):
        judgments = content.get('judgments', [])
        if isinstance(judgments, dict):
            judgments = list(judgments.values())
        identity = question.get('math_academy_id') or None
        capture_key = question_key(question)
        record_kind = record_kind or ('canonical_examples' if str(identity).startswith('e-') else 'questions')
        payload = task_payload('judge_question', {'question': question, 'gap': str(error),
            'source_limitations': content.get('source_limitations', [])})
        # Preparation can find gaps beyond answer correctness. Keep their scope
        # in the existing solver contract and bind even omitted compact metadata
        # (for example legacy fields_complete or original asset errors).
        payload.update(record_kind=record_kind, capture_key=capture_key,
                       source_evidence_hash=semantic_identity('preparation_source', question))
        payload['question'].update({key: copy.deepcopy(question[key]) for key in
            ('fields_complete', 'topic_id', 'knowledge_point_id', 'kp_id', 'difficulty',
             'observed_math_academy_id', 'source_errors_resolved', 'asset_errors') if key in question})
        evidence_hash = semantic_identity('judge_question', payload)
        judgment = self.gap_judgments.get(evidence_hash) or next((j for j in judgments if
                         j.get('record_kind') == record_kind and j.get('gap') == str(error) and
                         j.get('evidence_hash') == evidence_hash and
                         ((identity is not None and str(j.get('question_id')) == str(identity)) or
                          (identity is None and j.get('capture_key') == capture_key)) and
                         j.get('status') in ('confirmed', 'source_error', 'unavailable', 'ambiguous')), None)
        if not judgment:
            if self.resolve is None:
                raise ValueError('Source gap requires a final capture judgment: ' + str(error))
            judgment = self.resolve('judge_question', payload)
        if judgment.get('status') not in ('confirmed', 'source_error', 'unavailable', 'ambiguous'):
            raise ValueError('Agent returned no final source judgment')
        judgment = {**judgment, 'question_id': identity, 'capture_key': capture_key,
                    'record_kind': record_kind, 'gap': str(error), 'evidence_hash': evidence_hash, 'final': True}
        self.gap_judgments[evidence_hash] = judgment
        return judgment

    def omit_or_resolve(self, content, question, error):
        judgment = self.final_judgment(content, question, error)
        self.omissions.append({'kind': 'question', 'id': question.get('math_academy_id'),
                               'reason': str(error), 'judgment': judgment, 'final': True})

    def check_source_attribution(self, old):
        """Original-content imports cannot replace separately authored content."""
        if not old or not self.snapshot.has_facts:
            return
        current = set()
        def include(reference, kind):
            eid = scalar(reference)
            entity = self.snapshot.entities.get(eid, reference if isinstance(reference, dict) else {})
            for attr in ALLOWED:
                if not attr.startswith(kind + '/') or attr == kind + '/id':
                    continue  # UUID attribution alone does not establish a correction.
                value = entity.get(':' + attr)
                if value is None:
                    continue
                values = value if isinstance(value, list) else [value]
                current.update((eid, attr, dumps(self.snapshot.enum(v))) for v in values)
            return entity
        question = include(old, 'question')
        for reference in question.get(':question/answer-fields', []):
            field = include(reference, 'answer-field')
            for answer in field.get(':answer-field/choices', []):
                include(answer, 'answer')
            if field.get(':answer-field/correct') is not None:
                include(field[':answer-field/correct'], 'answer')
        ma_source = self.snapshot.idents.get(MA_SOURCE)
        for eid, attr, value, source in self.snapshot.facts:
            if (eid, attr, value) in current and source != ma_source:
                ident = next((name for name, entity_id in self.snapshot.idents.items() if entity_id == source), str(source))
                raise UnsupportedContent('Existing question has separately attributed content from ' + ident + ' on ' + attr)

    def check_response_ownership(self, question, old):
        # Response answers retain field ownership. A changed authored option
        # cannot orphan an existing learner response during a content import.
        incoming = {field['key']: field for field in question.get('answer_fields', [])}
        complete = question.get('answer_fields_complete', question.get('fields_complete', False))
        previous_fields = (old or {}).get(':question/answer-fields', [])
        by_identity = {}
        for candidate in previous_fields:
            ctype = candidate.get(':answer-field/type', {})
            ctype = ctype.get(':db/ident') if isinstance(ctype, dict) else next((k for k,v in self.snapshot.idents.items() if v == ctype), '')
            identity = (candidate.get(':answer-field/key'), str(ctype).rsplit('/',1)[-1])
            by_identity.setdefault(identity, []).append(candidate)
        for (key, ctype), candidates in by_identity.items():
            field = incoming.get(key)
            if (field is not None and field['type'] == ctype and len(candidates) > 1
                    and any(answer.get(':task-item/_responses') for candidate in candidates
                            for answer in candidate.get(':answer-field/choices', []))):
                # Even an exact match would detach the other same-key fields
                # from the question. Their response owners cannot be guessed.
                raise UnsupportedContent('Source field revision has ambiguous historical response ownership in field ' + str(key))
        for candidate in previous_fields:
            key = candidate.get(':answer-field/key')
            field = incoming.get(key)
            if field is None and not complete:
                continue  # Partial source updates retain unobserved fields.
            ctype = candidate.get(':answer-field/type', {})
            ctype = ctype.get(':db/ident') if isinstance(ctype, dict) else next((k for k,v in self.snapshot.idents.items() if v == ctype), '')
            continuing = field is not None and str(ctype).rsplit('/',1)[-1] == field['type']
            if continuing and field['type'] == 'blank':
                continue  # Entered values keep their existing field ownership.
            if continuing:
                by_choice = {}
                for answer in candidate.get(':answer-field/choices', []):
                    signature = (answer[':answer/type'][':db/ident'].rsplit('/',1)[-1], answer[':answer/value'])
                    by_choice.setdefault(signature, []).append(answer)
                if any(len(answers) > 1 and any(answer.get(':task-item/_responses') for answer in answers)
                       for answers in by_choice.values()):
                    # Radio/select replacement keeps one entity per typed
                    # value. A typed match cannot establish which duplicate
                    # owns history, so refuse before any Plan mutation.
                    raise UnsupportedContent('Source field revision has ambiguous historical response ownership among duplicate choices in field ' + str(key))
            wanted = {(c['type'], c['value']) for c in field['choices']} if continuing else set()
            for answer in candidate.get(':answer-field/choices', []):
                signature = (answer[':answer/type'][':db/ident'].rsplit('/',1)[-1], answer[':answer/value'])
                if signature not in wanted and answer.get(':task-item/_responses'):
                    raise UnsupportedContent('Source field revision would orphan a historical response in field ' + str(key))

    def question(self, plan, question, old, example):
        self.check_source_attribution(old)
        self.check_response_ownership(question, old)
        mid = question['math_academy_id']
        identity = old[':question/id'] if old else source_uuid('question', mid)
        target = plan.entity('question', identity, old)
        values = {'question/math-academy-id': mid, 'question/problem': question['problem']}
        if question.get('worked_solution'):
            values['question/worked-solution'] = question['worked_solution']
        if question.get('difficulty'):
            values['question/difficulty'] = kw('question.difficulty/' + question['difficulty'])
        if question.get('requires_calculator') is not None:
            values['question/requires-calculator'] = bool(question['requires_calculator'])
        for attr, value in values.items():
            plan.set(target, old, attr, value)
        fields = []
        for field in question.get('answer_fields', []):
            signature = [field['key'], field['type'], sorted({(c['type'], c['value']) for c in field['choices']}), field['correct_type'], field['correct_value']]
            previous = None
            compatible = []
            for candidate in (old or {}).get(':question/answer-fields', []):
                ctype = candidate.get(':answer-field/type', {})
                ctype = ctype.get(':db/ident') if isinstance(ctype, dict) else next((k for k,v in self.snapshot.idents.items() if v == ctype), '')
                correct = candidate.get(':answer-field/correct', {})
                choices = [(c[':answer/type'][':db/ident'].rsplit('/',1)[-1], c[':answer/value']) for c in candidate.get(':answer-field/choices', [])]
                correct_type = correct.get(':answer/type', {}).get(':db/ident', '').rsplit('/',1)[-1]
                stored = [candidate.get(':answer-field/key'), str(ctype).rsplit('/',1)[-1], sorted(set(choices)), correct_type, correct.get(':answer/value')]
                if stored[:2] == signature[:2]:
                    compatible.append(candidate)
                if stored == signature:
                    previous = candidate
                    break
            if previous is None and compatible:
                previous = compatible[0] if len(compatible) == 1 else self.choose(
                    'answer-field', {'question_id': mid, **field}, compatible)
            fid = previous[':answer-field/id'] if previous else source_uuid('answer-field', str(identity) + ':' + digest(signature[:2]))
            ft = plan.entity('answer-field', fid, previous)
            choices, correct = [], None
            for ctype, value in signature[2]:
                previous_answer = next((a for a in (previous or {}).get(':answer-field/choices', []) if a[':answer/value'] == value and a[':answer/type'][':db/ident'] == ':answer.type/' + ctype), None)
                aid = previous_answer[':answer/id'] if previous_answer else source_uuid('answer', str(fid) + ':' + digest([ctype,value]))
                at = plan.entity('answer', aid, previous_answer)
                plan.set(at, previous_answer, 'answer/type', kw('answer.type/' + ctype))
                plan.set(at, previous_answer, 'answer/value', value)
                choices.append(at)
                if ctype == field['correct_type'] and value == field['correct_value']:
                    correct = at
            for attr, value in (('answer-field/key',field['key']), ('answer-field/type',kw('answer-field.type/' + field['type'])), ('answer-field/correct',correct)):
                plan.set(ft, previous, attr, value)
            # Blank choices include distinct entered values, not display
            # options. Keep their ownership when the canonical answer changes.
            plan.set(ft, previous, 'answer-field/choices', choices, many=True, replace=field['type'] != 'blank')
            fields.append(ft)
        if fields or not example:
            if not question.get('answer_fields_complete', question.get('fields_complete', False)):
                # Missing captured fields do not establish that MA removed them.
                incoming_keys = {f['key'] for f in question.get('answer_fields', [])}
                fields.extend(f[':db/id'] for f in (old or {}).get(':question/answer-fields', [])
                              if f.get(':answer-field/key') not in incoming_keys)
            plan.set(target, old, 'question/answer-fields', fields, many=True, replace=True)
        return target

    def ordered(self, owner, kind):
        if not owner:
            return []
        steps = {scalar(s): self.snapshot.entities.get(scalar(s), s) for s in owner.get(':' + kind + '/steps', [])}
        current = scalar(owner.get(':' + kind + '/first-step'))
        ordered, visited = [], set()
        while current is not None:
            if current not in steps or current in visited:
                raise UnsupportedContent('Existing structure has an invalid step route')
            step = steps[current]
            visited.add(current)
            ordered.append(step)
            current = scalar(step.get(':step/next'))
        return ordered

    def sequence(self, plan, kind, identity, old, values, children, *, diagnostic=False):
        """Children contain source placement IDs only when independently verified."""
        target = plan.entity(kind, identity, old)
        refs = []
        for key, content, previous, source_id in children:
            sid = previous[':step/id'] if previous else source_uuid('step', f'{identity}:{key}')
            refs.append(plan.entity('step', sid, previous))
        for index, ((key, content, previous, source_id), step) in enumerate(zip(children, refs)):
            plan.set(step, previous, 'step/content', content)
            if source_id is not None:
                occupied = self.exact('step/math-academy-id', source_id)
                if occupied and (not previous or occupied[':db/id'] != previous[':db/id']):
                    raise UnsupportedContent('Source placement already belongs to another step')
                plan.set(step, previous, 'step/math-academy-id', int(source_id))
            if not diagnostic:
                plan.set(step, previous, 'step/next', refs[index + 1] if index + 1 < len(refs) else None, replace=True)
        for attr, value in values.items():
            plan.set(target, old, attr, value)
        plan.set(target, old, kind + '/steps', refs, many=True, replace=True)
        plan.set(target, old, kind + '/first-step', refs[0])
        # Remove continuation links of detached steps while retaining their historical entities.
        for previous in ([] if diagnostic else self.ordered(old, kind)):
            if previous[':db/id'] not in refs and previous.get(':step/next'):
                plan.retract(previous[':db/id'], 'step/next', scalar(previous[':step/next']))
        return target, refs

    def lesson(self, plan, content, topics, examples, library):
        definition = content['lesson_definition']
        tid = int(definition.get('topic_id') or content.get('topic_id') or 0)
        topic = topics.get(tid)
        if not definition.get('complete') or not definition.get('steps') or not topic:
            raise UnsupportedContent('Full lesson definition or topic unavailable')
        candidates = [e for e in self.snapshot.entities.values() if e.get(':activity/type', {}).get(':db/ident') == ':activity.type/lesson' and scalar(e.get(':activity/scope')) == topic[':db/id']]
        old = candidates[0] if len(candidates) == 1 else self.choose('lesson', definition, candidates) if candidates else None
        previous_steps = self.ordered(old, 'activity')
        tutorials = {int(t['math_academy_id']): t for t in content.get('tutorials', [])}
        children, used = [], set()
        for index, step in enumerate(definition['steps']):
            sid, cid, kind = step.get('math_academy_id'), int(step['content_id']), step['type']
            if sid is not None:
                sid = int(sid)
            previous = next((s for s in previous_steps if sid is not None and s.get(':step/math-academy-id') == sid), None)
            if kind == 'tutorial':
                tutorial = tutorials.get(cid)
                if not tutorial or not tutorial.get('content'):
                    raise UnsupportedContent('Lesson tutorial missing: ' + str(cid))
                existing = self.exact('tutorial/math-academy-id', cid)
                if not existing and previous:
                    candidate = previous.get(':step/content', {})
                    if isinstance(candidate, dict) and ':tutorial/id' in candidate:
                        existing = self.choose('tutorial revision', tutorial, [self.snapshot.entities.get(candidate[':db/id'], candidate)])
                if not existing:
                    candidates = [s[':step/content'] for s in previous_steps if isinstance(s.get(':step/content'), dict)
                        and ':tutorial/id' in s[':step/content'] and s[':db/id'] not in used
                        and (s[':step/content'].get(':tutorial/title') == tutorial.get('title') or len(previous_steps) == len(definition['steps']) and previous_steps[index] is s)]
                    if candidates:
                        existing = self.choose('tutorial revision', tutorial, candidates)
                if existing and not previous:
                    previous = next((s for s in previous_steps if scalar(s.get(':step/content')) == existing[':db/id']), None)
                text = markdown(library.text(tutorial['content']) if library else tutorial['content'])
                identity = existing[':tutorial/id'] if existing else source_uuid('tutorial', cid)
                target = plan.entity('tutorial', identity, existing)
                for attr, value in (('tutorial/math-academy-id',cid),('tutorial/title',tutorial.get('title') or step.get('title')),('tutorial/content',text)):
                    if not value:
                        raise UnsupportedContent('Tutorial title or content unavailable')
                    plan.set(target, existing, attr, value)
                tutorial['content'] = text
            elif kind in ('example', 'knowledge-point'):
                example = examples.get('e-' + str(cid))
                if not example:
                    raise UnsupportedContent('Lesson example or knowledge point unavailable: e-' + str(cid))
                target, point = example
                if not previous and ':db/id' in point:
                    previous = next((s for s in previous_steps if scalar(s.get(':step/content')) == point[':db/id']), None)
            else:
                raise UnsupportedContent('Unknown source lesson step: ' + kind)
            if previous:
                if previous[':db/id'] in used:
                    raise UnsupportedContent('Lesson source maps multiple placements to one existing step')
                used.add(previous[':db/id'])
            children.append((str(sid) if sid else f'{index}:{kind}:{cid}', target, previous, sid))
        aid = old[':activity/id'] if old else source_uuid('lesson', tid)
        values = {'activity/title': definition.get('title') or content.get('title'), 'activity/type': kw('activity.type/lesson'), 'activity/scope': topic[':db/id']}
        base = content.get('base_xp') or definition.get('base_xp')
        if isinstance(base, (int, float)) and base > 0:
            values['activity/expected-seconds'] = float(base * 60)
        self.sequence(plan, 'activity', aid, old, values, children)
        if definition.get('title'):
            plan.set(topic[':db/id'], topic, 'topic/title', definition['title'])

    def multistep(self, plan, content, topics, questions, library=None):
        source = content.get('multistep_id')
        order = content.get('question_order') or [q['math_academy_id'] for q in content['questions']]
        if not source or not order or any(mid not in questions for mid in order) or len(set(order)) != len(order):
            raise UnsupportedContent('Multistep requires all parts and its verified content identity')
        if any(q.get('local_problem') and q['problem'] != q['local_problem'] for q in content['questions']):
            raise UnsupportedContent('Multistep question contains duplicated shared context')
        uid = source_uuid('multistep', source)
        old = self.exact('multistep/id', uid)
        old_steps = self.ordered(old, 'multistep')
        children = []
        for index, mid in enumerate(order):
            target = questions[mid]
            previous = next((s for s in old_steps if scalar(s.get(':step/content')) == target), None)
            children.append((f'{index}:{mid}', target, previous, None))
        contexts = content.get('shared_contexts', [])
        context = content.get('shared_context') or '\n\n'.join(c.get('problem', c.get('content', '')) for c in contexts)
        context = markdown(library.text(context) if library else context)
        content['shared_context'] = context
        multi, _ = self.sequence(plan, 'multistep', uid, old, {'multistep/context': context or None}, children)
        pid = source_uuid('multistep-assigned-problem', source)
        pold = self.exact('assigned-problem/id', pid)
        assigned = plan.entity('assigned-problem', pid, pold)
        plan.set(assigned, pold, 'assigned-problem/content', multi)
        plan.set(assigned, pold, 'assigned-problem/topic-coverage', [t[':db/id'] for t in topics.values()], many=True)
        aid = source_uuid('multistep-activity', source)
        aold = self.exact('activity/id', aid)
        old_steps = self.ordered(aold, 'activity')
        if len(old_steps) > 1:
            raise UnsupportedContent('Existing multistep wrapper contains other authored steps')
        self.sequence(plan, 'activity', aid, aold, {'activity/title': content.get('title') or 'Multistep',
            'activity/type': kw('activity.type/assignment')}, [('problem', assigned, old_steps[0] if old_steps else None, None)])

    def activity(self, plan, content, topics, questions, kind):
        order = content.get('question_order') or [q['math_academy_id'] for q in content['questions']]
        if not order or any(mid not in questions for mid in order):
            raise UnsupportedContent('Activity contains a question whose content is unavailable')
        # Task IDs identify attempts, not definitions. An observed route variant has
        # its own stable internal identity and no invented MA definition identifier.
        verified_id = content.get('activity_definition_id')
        aid = activity_identity(content, kind)
        old = self.exact('activity/math-academy-id', int(verified_id)) if verified_id else self.exact('activity/id', aid)
        if old:
            aid = old[':activity/id']
        old_steps = self.ordered(old, 'activity') if kind != 'diagnostic' else [self.snapshot.entities.get(scalar(s), s) for s in (old or {}).get(':activity/steps', [])]
        children = []
        for index, mid in enumerate(order):
            prior = next((s for s in old_steps if scalar(s.get(':step/content')) == questions[mid] and s[':db/id'] not in {c[2][':db/id'] for c in children if c[2]}), None)
            children.append((f'{index}:{mid}', questions[mid], prior, None))
        values = {'activity/title': content.get('title') or kind.title(), 'activity/type': kw('activity.type/' + kind)}
        if verified_id:
            values['activity/math-academy-id'] = int(verified_id)
        tid = int(content.get('topic_id') or 0)
        if tid in topics:
            values['activity/scope'] = topics[tid][':db/id']
        course = self.exact('course/math-academy-id', int(content['course_id'])) if content.get('course_id') else None
        if course:
            values['activity/course'] = course[':db/id']
            if kind == 'diagnostic':
                values['activity/scope'] = course[':db/id']
        if kind == 'diagnostic' and 'activity/scope' not in values:
            raise UnsupportedContent('Diagnostic curriculum scope is unavailable')
        if content.get('time_limit_seconds'):
            values['activity/time-limit-seconds'] = float(content['time_limit_seconds'])
        _, refs = self.sequence(plan, 'activity', aid, old, values, children, diagnostic=kind == 'diagnostic')
        if kind == 'diagnostic':
            outcomes = content.get('question_outcomes', {})
            for index, mid in enumerate(order[:-1]):
                outcome = outcomes.get(mid)
                suffix = {'correct': 'on-correct', 'incorrect': 'on-incorrect', 'dont_know': 'on-skipped', 'skipped': 'on-skipped'}.get(outcome)
                if suffix:
                    plan.set(refs[index], children[index][2], 'diagnostic-probe/' + suffix, refs[index + 1])
