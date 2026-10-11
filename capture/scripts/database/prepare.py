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

MA_SOURCE = ':org/Math-Academy'
KINDS = ('topic', 'knowledge-point', 'question', 'answer-field', 'answer', 'tutorial',
         'activity', 'step', 'multistep', 'assigned-problem')
ALLOWED = {f'{kind}/{name}' for kind, names in {
    'topic': ('id', 'math-academy-id', 'title', 'knowledge-points', 'difficulty'),
    'knowledge-point': ('id', 'title', 'canonical-example', 'questions'),
    'question': ('id', 'math-academy-id', 'problem', 'worked-solution', 'difficulty', 'requires-calculator', 'answer-fields'),
    'answer-field': ('id', 'key', 'type', 'presentation', 'choices', 'correct'),
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

def scalar(value):
    return value.get(':db/id', value.get(':db/ident')) if isinstance(value, dict) else value


class Snapshot:
    def __init__(self, data):
        self.basis = data['basis']
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
        if self.snapshot.enum(previous) != self.snapshot.enum(desired) or not self.snapshot.sourced(target, attr, desired, self.source):
            self.updates.setdefault(target, {kw('db/id'): target})[kw(attr)] = desired
            # Several questions can name the same KP. Only the final scalar
            # value is emitted by the entity map, so its guard must match it.
            self.assertions = [row for row in self.assertions if not (row[0] == target and row[1] == kw(attr))]
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
    def __init__(self, snapshot, *, resolve=None):
        self.snapshot = Snapshot(snapshot)
        self.resolve = resolve
        self.decisions, self.omissions = [], []

    def choose(self, kind, captured, candidates):
        payload = {'kind': kind, 'captured': captured, 'candidates': candidates,
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

    def prepare(self, content, library=None, derived_source=None):
        content = copy.deepcopy(content)
        if not content.get('question_order'):
            content['question_order'] = [q['math_academy_id'] for q in content.get('questions', [])]
        if not content.get('lesson_workload_sample'):
            groups = {}
            for q in content.get('questions', []):
                kp = str(q.get('knowledge_point_id') or q.get('kp_id') or '')
                ids = groups.setdefault(kp, [])
                if q['math_academy_id'] not in ids and len(ids) < 2:
                    ids.append(q['math_academy_id'])
            content['lesson_workload_sample'] = {'questions_by_knowledge_point': groups,
                'selection': 'first-two-distinct-practice-questions-in-captured-order', 'base_xp': content.get('base_xp')}
        records = []
        for bucket, example in (('questions', False), ('canonical_examples', True)):
            seen = set()
            kept = []
            for original in content.get(bucket, []):
                mid = original.get('math_academy_id')
                if mid in seen:
                    continue
                seen.add(mid)
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
                    judgment = self.final_judgment(content, original, error)
                    repaired = copy.deepcopy(original)
                    answers = {a.get('key'): a for a in judgment.get('answers', [])}
                    for field in repaired.get('answer_fields', repaired.get('fields', [])):
                        answer = answers.get(field.get('key'), {})
                        evidence = answer.get('ma_evidence') or answer.get('evidence')
                        if evidence and answer.get('ma_value') is not None:
                            field.update(correct_value=answer['ma_value'], evidence=evidence)
                    try:
                        q = authoritative_question(repaired, example=example)
                        if library:
                            q = library.question(q)
                        for key in ('problem', 'worked_solution', 'local_problem'):
                            if isinstance(q.get(key), str):
                                q[key] = markdown(q[key])
                        kept.append(q)
                        records.append((q, example))
                    except (UnsupportedContent, MissingImage) as final_error:
                        self.omissions.append({'kind': 'question', 'id': original.get('math_academy_id'),
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
            point = point_map.get((tid, kid))
            source_example = q['math_academy_id'] if example else examples.get(kid, {}).get('math_academy_id')
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
                    self.multistep(candidate_plan, content, topic_map, question_targets)
                else:
                    self.activity(candidate_plan, content, topic_map, question_targets, kind)
                plan = candidate_plan
            except UnsupportedContent as error:
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
                'calibration': calibration, 'images': library.saved if library else {}}

    def final_judgment(self, content, question, error):
        judgments = content.get('judgments', [])
        if isinstance(judgments, dict):
            judgments = list(judgments.values())
        judgment = next((j for j in judgments if j.get('question_id') == question.get('math_academy_id')
                         and j.get('status') in ('confirmed', 'source_error', 'unavailable', 'ambiguous')), None)
        if not judgment:
            if self.resolve is None:
                raise ValueError('Source gap requires a final capture judgment: ' + str(error))
            judgment = self.resolve('judge_question', {'question': question, 'gap': str(error),
                'instruction': 'Resolve from saved source evidence now. Return final status confirmed/source_error/ambiguous/unavailable, reasoning, and answers with checked ma_evidence. Never invent a Math Academy fact.'})
        if judgment.get('status') not in ('confirmed', 'source_error', 'unavailable', 'ambiguous'):
            raise ValueError('Agent returned no final source judgment')
        return judgment

    def omit_or_resolve(self, content, question, error):
        judgment = self.final_judgment(content, question, error)
        self.omissions.append({'kind': 'question', 'id': question.get('math_academy_id'),
                               'reason': str(error), 'judgment': judgment, 'final': True})

    def question(self, plan, question, old, example):
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
            signature = [field['key'], field['type'], sorted({(c['type'], c['value']) for c in field['choices']}), field['correct_type'], field['correct_value'], field.get('presentation')]
            previous = None
            for candidate in (old or {}).get(':question/answer-fields', []):
                ctype = candidate.get(':answer-field/type', {})
                ctype = ctype.get(':db/ident') if isinstance(ctype, dict) else next((k for k,v in self.snapshot.idents.items() if v == ctype), '')
                correct = candidate.get(':answer-field/correct', {})
                choices = [(c[':answer/type'][':db/ident'].rsplit('/',1)[-1], c[':answer/value']) for c in candidate.get(':answer-field/choices', [])]
                correct_type = correct.get(':answer/type', {}).get(':db/ident', '').rsplit('/',1)[-1]
                stored = [candidate.get(':answer-field/key'), str(ctype).rsplit('/',1)[-1], sorted(set(choices)), correct_type, correct.get(':answer/value'), candidate.get(':answer-field/presentation')]
                if stored == signature:
                    previous = candidate
                    break
            fid = previous[':answer-field/id'] if previous else source_uuid('answer-field', str(identity) + ':' + digest(signature))
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
            if field.get('presentation'):
                plan.set(ft, previous, 'answer-field/presentation', field['presentation'])
            plan.set(ft, previous, 'answer-field/choices', choices, many=True)
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

    def multistep(self, plan, content, topics, questions):
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
        route = [(mid, (content.get('question_outcomes') or {}).get(mid)) for mid in order]
        aid = source_uuid(kind, verified_id if verified_id else digest([content.get('course_id'), content.get('topic_id'), route]))
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
