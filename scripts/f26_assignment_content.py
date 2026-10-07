#!/usr/bin/python3
"""Build canonical content for the current F26 assignments without writing a DB.

Public API: build(vault: Path) -> (entities, activity_ids, audit).
Entities use the colon-key / $uuid / $ref / $inst convention of
import_school_assignments.py. Source quiz grading controls are recorded in the
audit; Course Academy applies its own existing grading rules.
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import json
import re
from datetime import date, datetime, time, timezone
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit
from zoneinfo import ZoneInfo

import yaml

from import_school_assignments import LINK, PROBLEM, stable_id, tidy


ALIASES = {
    'F26/255/09-29-26_R-1.md': 'F26/255/W1 09-27/R1 09-29/R1 09-29.md',
    'F26/256/09-29-26_R-1.md': 'F26/256/W1 09-27/R1 09-29/R1 09-29.md',
    'F26/256/10-02-26_OHW-1.md': 'F26/256/W1 09-27/OHW-1/OHW-1.md',
    'F26/256/10-02-26_WHW-1.md': 'F26/256/W1 09-27/WHW-1/WHW-1.md',
}
COURSES = {
    '255': 'c37c596e-77c4-5554-8295-443fb5da076b',
    '256': 'fa274c9b-ca65-5fde-b8ed-49681698e235',
    '341': '3ace2150-672f-50e7-9c2c-027b6d4272d7',
}
LEGACY_SEEDS = {(Path(path).parent.name, Path(path).stem.split('_', 1)[1]): seed
                for path, seed in ALIASES.items()}
QUIZ = re.compile(r'^```quiz[ \t]*\n(.*?)^```[ \t]*$', re.M | re.S)
BLANK = re.compile(r'==(.+?)==', re.S)
NAV_LINE = re.compile(r'^\*\*(Topics|Prerequisites):\*\*([^\n]*)$', re.M)
NAV_SECTION = re.compile(r'^## (?:Topics|Prerequisites|Lessons)\s*\n.*?(?=^## |\Z)', re.M | re.S)
MATH = re.compile(r'\\\[[\s\S]*?\\\]|\\\([\s\S]*?\\\)|\$\$[\s\S]*?\$\$|(?<!\\)\$(?!\$)(?:\\.|[^$\\])*?(?<!\\)\$')


class UniqueKeyLoader(yaml.SafeLoader):
    """Reject duplicate YAML keys instead of silently losing quiz content."""


def _mapping(loader, node, deep=False):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in result:
            raise ValueError(f'Duplicate quiz YAML key: {key}')
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


UniqueKeyLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _mapping)


def text(value):
    if isinstance(value, bool):
        return 'true' if value else 'false'
    if isinstance(value, (str, int, float)):
        return str(value)
    raise ValueError(f'Expected source text, got {type(value).__name__}')


class Builder:
    def __init__(self, vault):
        self.vault = Path(vault).resolve()
        self.entities = []
        self.assets = {}
        self.topic_cache = {}
        self.audit = {'activities': [], 'source_repairs': [], 'grading_limitations': [],
                      'non_exact_question_ids': [], 'target_math_academy_ids': [], 'assets': []}

    def entity(self, source, key, kind, **attrs):
        uid = stable_id(source, key)
        row = {':db/id': uid, f':{kind}/id': {'$uuid': uid}}
        row.update({':' + k.replace('__', '/').replace('_', '-'): v for k, v in attrs.items()})
        row[':db/ensure'] = f':{kind}/validate'
        self.entities.append(row)
        return uid

    def local_link(self, target, source):
        split = urlsplit(target)
        if split.scheme or target.startswith('#'):
            return None, split
        path = (source.parent / unquote(split.path)).resolve()
        if not path.is_relative_to(self.vault) or not path.is_file():
            raise ValueError(f'Missing or external source asset: {source}: {target}')
        return path, split

    def render_text(self, value, source, location):
        value = text(value).strip()

        def fix_math(match):
            before = match[0]
            after = re.sub(r'\n[ \t]*abla\b', lambda _: r'\nabla', before)
            if after != before:
                self.audit['source_repairs'].append({'source': str(source.relative_to(self.vault)), 'location': location,
                                                     'before': before, 'after': after,
                                                     'reason': 'Repair newline + abla caused by a lost LaTeX nabla escape; all other source text retained.'})
            return after

        value = MATH.sub(fix_math, value)

        def replace(match):
            image, label, angled, plain = match.groups()
            target = angled or plain
            path, split = self.local_link(target, source)
            if path is None:
                return match[0]
            kind = 'image' if image else 'pdf'
            allowed = {'.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg'} if image else {'.pdf'}
            if path.suffix.lower() not in allowed:
                raise ValueError(f'Unexpected link in assignment content: {source}: {target}')
            self.assets[str(path)] = {'path': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'kind': kind}
            route = '/api/asset?path=' if image else '/api/source?path='
            url = route + quote(str(path), safe='')
            if split.fragment:
                url += '#' + split.fragment
            return f'{image}[{label}]({url})'

        return LINK.sub(replace, value)

    def topic_links(self, tail, source):
        result = {'direct': [], 'supporting': [], 'notes': []}
        for match in NAV_LINE.finditer(tail):
            kind = 'direct' if match[1] == 'Topics' else 'supporting'
            links = list(LINK.finditer(match[2]))
            if not links:
                result['notes'].append({'kind': kind, 'text': match[2].strip()})
            for link in links:
                target = link[3] or link[4]
                path, _ = self.local_link(target, source)
                if path is None or path.suffix.lower() != '.md':
                    raise ValueError(f'Topic mapping is not a local lesson: {target}')
                if path not in self.topic_cache:
                    identity = re.search(r'^lesson-id:\s*(\d+)\s*$', path.read_text(), re.M)
                    if not identity:
                        raise ValueError(f'Topic link has no verified lesson-id: {path}')
                    self.topic_cache[path] = int(identity[1])
                result[kind].append({'topic_id': self.topic_cache[path], 'source': str(path), 'label': link[2]})
        return result

    def sequence(self, source, keys, contents):
        ids = [stable_id(source, key) for key in keys]
        for i, (key, content) in enumerate(zip(keys, contents)):
            attrs = {'step__content': content}
            if i + 1 < len(ids):
                attrs['step__next'] = ids[i + 1]
            self.entity(source, key, 'step', **attrs)
        return ids

    def option(self, source, key, option, path, location):
        value = self.render_text(option['content'], path, location + '/content')
        image = LINK.fullmatch(value)
        math = MATH.fullmatch(value)
        if image and image[1]:
            kind, value = 'image', image[3] or image[4]
        elif math:
            n = 2 if value.startswith(('$$', r'\(', r'\[')) else 1
            kind, value = 'math', value[n:-n].strip()
        else:
            kind = 'text'
        attrs = {'answer__type': ':answer.type/' + kind, 'answer__value': value}
        if option.get('feedback'):
            attrs['answer__feedback'] = self.render_text(option['feedback'], path, location + '/feedback')
        return self.entity(source, key, 'answer', **attrs), (kind, value)

    def question(self, source, key, quiz, path, context=''):
        if 'fields' in quiz:
            return self.canonical_question(source, key, quiz, path, context)
        qid, kind = quiz['id'], quiz['type']
        common = {'type', 'id', 'content', 'gated', 'shuffle'}
        allowed = {'radio': common | {'options'}, 'blank': common | {'input_mode', 'require_exact', 'feedback'},
                   'free': common | {'correct', 'feedback'}}
        if kind not in allowed or set(quiz) - allowed[kind]:
            raise ValueError(f'Unsupported quiz structure at {path}#{qid}: {kind}, {set(quiz) - allowed.get(kind, set())}')
        prompt = self.render_text(quiz['content'], path, qid + '/content')
        fields, field_audit = [], []
        attrs = {}
        worked = ''
        if kind == 'radio':
            options = quiz['options']
            if len(options) < 2 or sum(o.get('correct') is True for o in options) != 1:
                raise ValueError(f'Radio requires exactly one explicit correct option: {qid}')
            if len({o['id'] for o in options}) != len(options):
                raise ValueError(f'Duplicate option IDs: {qid}')
            choices, values, option_map, correct = [], {}, {}, None
            for option in options:
                if set(option) - {'id', 'content', 'correct', 'feedback'} or not isinstance(option['id'], str):
                    raise ValueError(f'Unsupported option: {qid}')
                aid, value = self.option(source, key + '/selection/option-' + option['id'], option, path, qid + '/' + option['id'])
                if value in values:
                    raise ValueError(f'Duplicate field-owned answer values require a reviewed merge: {qid}')
                values[value] = aid
                choices.append(aid)
                option_map[option['id']] = aid
                if option.get('correct') is True:
                    correct = aid
                    worked = self.render_text(option.get('feedback', ''), path, qid + '/correct-feedback')
            fid = self.entity(source, key + '/selection', 'answer-field', answer_field__key='selection',
                              answer_field__type=':answer-field.type/radio', answer_field__choices=choices, answer_field__correct=correct)
            fields.append(fid)
            field_audit.append({'field_id': fid, 'key': 'selection', 'options': option_map, 'correct_answer_id': correct})
        elif kind == 'blank':
            mode = quiz.get('input_mode', 'text')
            if mode not in ('text', 'math') or not isinstance(quiz.get('require_exact', True), bool):
                raise ValueError(f'Invalid blank grading settings: {qid}')
            hidden = list(BLANK.finditer(prompt))
            if not hidden:
                raise ValueError(f'Blank has no answer slots: {qid}')
            for i, match in enumerate(hidden, 1):
                answer = match[1].strip()
                if not answer:
                    raise ValueError(f'Empty canonical blank: {qid}')
                fkey = f'field-{i}'
                aid = self.entity(source, key + '/' + fkey + '/canonical', 'answer',
                                  answer__type=':answer.type/' + mode, answer__value=answer)
                fid = self.entity(source, key + '/' + fkey, 'answer-field', answer_field__key=fkey,
                                  answer_field__type=':answer-field.type/blank', answer_field__choices=[aid], answer_field__correct=aid)
                fields.append(fid)
                field_audit.append({'field_id': fid, 'key': fkey, 'correct_answer_id': aid, 'canonical_value': answer, 'answer_type': mode})
            indices = iter(range(1, len(hidden) + 1))
            prompt = BLANK.sub(lambda _: '{{field-' + str(next(indices)) + '}}', prompt)
            worked = self.render_text(quiz.get('feedback', ''), path, qid + '/feedback')
        else:
            worked = '\n\n'.join(self.render_text(quiz[field], path, qid + '/' + field) for field in ('correct', 'feedback') if quiz.get(field))
        attrs['question__problem'] = tidy(context + '\n\n' + prompt) if context else prompt
        if fields:
            attrs['question__answer_fields'] = fields
        if worked:
            attrs['question__worked_solution'] = worked
        identity = self.entity(source, key, 'question', **attrs)
        if kind == 'blank' and not quiz.get('require_exact', True):
            self.audit['non_exact_question_ids'].append(identity)
        return identity, {'quiz_id': qid, 'type': kind, 'question_id': identity, 'identity_key': key,
                          'input_mode': quiz.get('input_mode'), 'require_exact': quiz.get('require_exact'),
                          'shuffle': quiz.get('shuffle'), 'gated': quiz.get('gated'), 'fields': field_audit}

    def canonical_question(self, source, key, quiz, path, context=''):
        """Convert explicit vault fields to the existing EDB content schema.

        EDB has no free field type. Preserve those reference responses in the
        worked solution, as for legacy free quizzes, and record the limitation.
        """
        qid = quiz['id']
        if set(quiz) - {'id', 'content', 'fields', 'feedback', 'shuffle', 'gated'}:
            raise ValueError(f'Unsupported canonical question: {path}#{qid}')
        if not isinstance(quiz['fields'], list) or not quiz['fields']:
            raise ValueError(f'Canonical question requires fields: {qid}')
        prompt = self.render_text(quiz['content'], path, qid + '/content')
        fields, audit, free, keys = [], [], [], set()

        def answer(answer_key, value, location):
            if not isinstance(value, dict) or set(value) - {'id', 'type', 'value', 'feedback'}:
                raise ValueError(f'Unsupported canonical answer: {qid}/{location}')
            kind = value['type']
            if kind not in ('math', 'text', 'image'):
                raise ValueError(f'Unsupported answer representation: {kind}')
            rendered = self.render_text(value['value'], path, location)
            if kind == 'image':
                image = LINK.fullmatch(rendered)
                if image and image[1]:
                    rendered = image[3] or image[4]
                else:
                    rendered = self.render_text(f'![answer]({rendered})', path, location)
                    image = LINK.fullmatch(rendered)
                    if not image:
                        raise ValueError(f'Invalid image answer: {qid}/{location}')
                    rendered = image[3] or image[4]
            attrs = {'answer__type': ':answer.type/' + kind, 'answer__value': rendered}
            if value.get('feedback'):
                attrs['answer__feedback'] = self.render_text(value['feedback'], path, location + '/feedback')
            return self.entity(source, answer_key, 'answer', **attrs), (kind, rendered)

        for field in quiz['fields']:
            fkey, kind = field['key'], field['type']
            if not isinstance(fkey, str) or not fkey or fkey in keys:
                raise ValueError(f'Missing or duplicate field key: {qid}/{fkey}')
            keys.add(fkey)
            if kind == 'free':
                if set(field) != {'key', 'type', 'correct'}:
                    raise ValueError(f'Unsupported free field: {qid}/{fkey}')
                value = field['correct']
                if set(value) != {'type', 'value'} or value['type'] not in ('text', 'math'):
                    raise ValueError(f'Unsupported free reference: {qid}/{fkey}')
                reference = self.render_text(value['value'], path, qid + '/' + fkey)
                if value['type'] == 'math':
                    reference = '$' + reference + '$'
                free.append(f'**{fkey}:** {reference}')
                audit.append({'key': fkey, 'type': kind, 'reference': reference, 'field_id': None})
                continue
            if kind == 'blank':
                if set(field) != {'key', 'type', 'correct'}:
                    raise ValueError(f'Unsupported blank field: {qid}/{fkey}')
                correct, _ = answer(key + '/' + fkey + '/canonical', field['correct'], qid + '/' + fkey)
                choices = [correct]
                option_map = {}
            elif kind in ('radio', 'select'):
                if set(field) != {'key', 'type', 'correct', 'choices'} or len(field['choices']) < 2:
                    raise ValueError(f'Unsupported selection field: {qid}/{fkey}')
                choices, option_map, values = [], {}, set()
                for option in field['choices']:
                    oid = option['id']
                    if not isinstance(oid, str) or not oid or oid in option_map:
                        raise ValueError(f'Missing or duplicate option ID: {qid}/{fkey}')
                    aid, value = answer(key + '/' + fkey + '/option-' + oid, option, qid + '/' + fkey + '/' + oid)
                    if value in values:
                        raise ValueError(f'Duplicate answer value: {qid}/{fkey}')
                    values.add(value)
                    choices.append(aid)
                    option_map[oid] = aid
                if field['correct'] not in option_map:
                    raise ValueError(f'Correct answer outside choices: {qid}/{fkey}')
                correct = option_map[field['correct']]
            else:
                raise ValueError(f'Unsupported field type: {qid}/{fkey}: {kind}')
            fid = self.entity(source, key + '/' + fkey, 'answer-field', answer_field__key=fkey,
                              answer_field__type=':answer-field.type/' + kind,
                              answer_field__choices=choices, answer_field__correct=correct)
            fields.append(fid)
            audit.append({'field_id': fid, 'key': fkey, 'type': kind, 'options': option_map,
                          'correct_answer_id': correct})
        # Free responses are reference-only in the current EDB schema. Remove
        # only their widget markers; keep the task and its response label.
        for field in audit:
            if field['type'] == 'free':
                prompt = prompt.replace('{{' + field['key'] + '}}', '[' + field['key'] + ': written response]')
        worked = '\n\n'.join(free + ([self.render_text(quiz['feedback'], path, qid + '/feedback')] if quiz.get('feedback') else []))
        attrs = {'question__problem': tidy(context + '\n\n' + prompt) if context else prompt}
        if fields:
            attrs['question__answer_fields'] = fields
        if worked:
            attrs['question__worked_solution'] = worked
        identity = self.entity(source, key, 'question', **attrs)
        if free:
            self.audit['grading_limitations'].append({'question_id': identity, 'quiz_id': qid,
                'source': str(path.relative_to(self.vault)),
                'reason': 'Free fields are written-response references in worked-solution; EDB does not automatically grade them, including in questions with other fields.'})
        return identity, {'quiz_id': qid, 'type': 'fields', 'question_id': identity, 'identity_key': key,
                          'shuffle': quiz.get('shuffle'), 'gated': quiz.get('gated'), 'fields': audit}

    def assignment(self, relative):
        path = self.vault / relative
        raw = path.read_text()
        filename = re.fullmatch(r'(?:\d{2}-\d{2}-\d{2}|Undated)_((?:R|OHW|WHW)-\d+)\.md', path.name)
        if not filename or path.parent.name not in COURSES:
            raise ValueError(f'Unrecognized F26 assignment identity: {path}')
        code = filename[1]
        source = LEGACY_SEEDS.get((path.parent.name, code), f'F26/{path.parent.name}/{code}')
        markers = list(PROBLEM.finditer(raw))
        if not markers or [int(m[1]) for m in markers] != list(range(1, len(markers) + 1)):
            raise ValueError(f'Nonconsecutive assignment problems: {path}')
        title = f'MTH {path.parent.name} — {code}'
        intro = NAV_SECTION.sub('', raw[:markers[0].start()])
        intro = self.render_text(tidy(intro), path, 'instructions')
        tutorial = self.entity(source, 'instructions', 'tutorial', tutorial__title='Assignment information', tutorial__content=intro)
        contents, problems, seen = [tutorial], [], set()
        for i, marker in enumerate(markers):
            number = marker[1]
            body = raw[marker.end():markers[i + 1].start() if i + 1 < len(markers) else len(raw)]
            blocks = list(QUIZ.finditer(body))
            if not blocks:
                raise ValueError(f'Problem has no quiz: {path}#{number}')
            context = self.render_text(tidy(body[:blocks[0].start()]), path, f'problem-{number}/context')
            questions, quizzes, parts, direct, supporting = [], [], [], set(), set()
            for j, match in enumerate(blocks):
                quiz = yaml.load(match[1], Loader=UniqueKeyLoader)
                if not isinstance(quiz, dict) or not isinstance(quiz.get('id'), str) or quiz['id'] in seen:
                    raise ValueError(f'Missing or duplicate stable quiz ID: {path}#{number}')
                seen.add(quiz['id'])
                label = re.fullmatch(r'q-' + number + r'([a-z]?|-[a-z][a-z0-9-]*)', quiz['id'])
                if not label or (len(blocks) > 1 and not label[1]):
                    raise ValueError(f'Quiz ID does not identify its problem/part: {path}#{quiz["id"]}')
                part = label[1].lstrip('-')
                parts.append(part)
                key = f'problem-{number}/part-{part}' if part else f'problem-{number}/question'
                question, qa = self.question(source, key, quiz, path, context if len(blocks) == 1 else '')
                questions.append(question)
                tail = body[match.end():blocks[j + 1].start() if j + 1 < len(blocks) else len(body)]
                if tidy(NAV_LINE.sub('', tail)):
                    raise ValueError(f'Unowned prose after quiz must be reviewed: {path}#{quiz["id"]}')
                mappings = self.topic_links(tail, path)
                direct.update(x['topic_id'] for x in mappings['direct'])
                supporting.update(x['topic_id'] for x in mappings['supporting'])
                qa['topics'] = mappings
                quizzes.append(qa)
            if len(blocks) > 1:
                if len(set(parts)) != len(parts):
                    raise ValueError(f'Duplicate part labels: {path}#{number}')
                steps = self.sequence(source, [f'problem-{number}/part-{p}/step' for p in parts], questions)
                attrs = {'multistep__steps': steps, 'multistep__first_step': steps[0]}
                if context:
                    attrs['multistep__context'] = context
                content = self.entity(source, f'problem-{number}/multistep', 'multistep', **attrs)
            else:
                content = questions[0]
            topics = sorted(direct | supporting)
            attrs = {'assigned_problem__content': content}
            if topics:
                attrs['assigned_problem__topic_coverage'] = [{'$ref': [':topic/math-academy-id', n]} for n in topics]
            assigned = self.entity(source, f'problem-{number}', 'assigned-problem', **attrs)
            contents.append(assigned)
            problems.append({'number': int(number), 'assigned_problem_id': assigned, 'content_id': content,
                             'parts': [p for p in parts if p], 'quizzes': quizzes, 'direct': sorted(direct),
                             'supporting': sorted(supporting), 'topics': topics})
        steps = self.sequence(source, ['instructions/step'] + [f'problem-{m[1]}/step' for m in markers], contents)
        attrs = {'activity__title': title, 'activity__type': ':activity.type/assignment',
                 'activity__steps': steps, 'activity__first_step': steps[0],
                 'activity__course': {'$ref': [':course/id', {'$uuid': COURSES[path.parent.name]}]}}
        due_match = re.search(r'^Due:\s*(\d{4}-\d{2}-\d{2})\s*$', raw, re.M)
        due = None
        if due_match:
            due = datetime.combine(date.fromisoformat(due_match[1]), time(23, 59, 59), ZoneInfo('America/Los_Angeles')).astimezone(timezone.utc).isoformat().replace('+00:00', 'Z')
            attrs['activity__due'] = {'$inst': due}
        activity = self.entity(source, 'activity', 'activity', **attrs)
        self.audit['activities'].append({'source': relative, 'identity_source': source, 'title': title,
                                         'activity_id': activity, 'sha256': hashlib.sha256(raw.encode()).hexdigest(),
                                         'due': due, 'due_source': due_match[0] if due_match else None,
                                         'due_convention': 'Explicit date-only deadline interpreted as 23:59:59 America/Los_Angeles.',
                                         'problems': problems})
        return activity

    def validate(self):
        records = {r[':db/id']: r for r in self.entities}
        if len(records) != len(self.entities):
            raise ValueError('Duplicate generated entity IDs')
        owners = collections.defaultdict(list)
        for uid, row in records.items():
            for attr in (':activity/steps', ':multistep/steps', ':question/answer-fields', ':answer-field/choices'):
                for child in row.get(attr, []):
                    assert child in records, (uid, attr, child)
                    owners[child].append((uid, attr))
            if ':question/id' in row:
                assert row[':question/problem']
                fields = [records[f] for f in row.get(':question/answer-fields', [])]
                keys = [f[':answer-field/key'] for f in fields]
                assert len(keys) == len(set(keys))
                inline = re.findall(r'\{\{([^}]+)\}\}', row[':question/problem'])
                unplaced = set(keys) - set(inline)
                assert set(inline) <= set(keys), (uid, inline, keys)
                assert all(f[':answer-field/type'] == ':answer-field.type/radio'
                           for f in fields if f[':answer-field/key'] in unplaced), (uid, inline, keys)
            if ':answer-field/id' in row:
                assert row[':answer-field/correct'] in row[':answer-field/choices']
            if ':answer/id' in row:
                assert row[':answer/value'] and row[':answer/type'] in (':answer.type/math', ':answer.type/text', ':answer.type/image')
            if ':step/id' in row:
                assert row[':step/content'] in records
            for kind in ('activity', 'multistep'):
                if f':{kind}/steps' not in row:
                    continue
                owned, visited = set(row[f':{kind}/steps']), set()
                cursor = row[f':{kind}/first-step']
                while cursor:
                    assert cursor in owned and cursor not in visited
                    visited.add(cursor)
                    cursor = records[cursor].get(':step/next')
                assert visited == owned
        for uid, row in records.items():
            if any(k in row for k in (':step/id', ':answer-field/id', ':answer/id')):
                assert len(owners[uid]) == 1, (uid, owners[uid])


def build(vault: Path):
    builder = Builder(vault)
    files = sorted(path for path in (builder.vault / 'F26').glob('[0-9]*/*.md') if path.parent.name.isdigit())
    if not files:
        raise ValueError('No F26 assignment Markdown found')
    activities = [builder.assignment(str(path.relative_to(builder.vault))) for path in files]
    builder.validate()
    builder.audit['assets'] = list(builder.assets.values())
    builder.audit['target_math_academy_ids'] = sorted({topic for a in builder.audit['activities'] for p in a['problems'] for topic in p['topics']})
    builder.audit['target_union'] = builder.audit['target_math_academy_ids']
    builder.audit['files'] = [{'path': a['source'], 'sha256': a['sha256']} for a in builder.audit['activities']]
    builder.audit['quizzes'] = [dict(q, source=a['source'], problem=p['number'], activity_id=a['activity_id'])
                               for a in builder.audit['activities'] for p in a['problems'] for q in p['quizzes']]
    builder.audit['counts'] = dict(collections.Counter(next(k[1:-3] for k in row if k.endswith('/id') and k != ':db/id') for row in builder.entities))
    builder.audit['quiz_types'] = dict(collections.Counter(q['type'] for a in builder.audit['activities'] for p in a['problems'] for q in p['quizzes']))
    builder.audit['grading_limitations'] += [
        'Free-response references remain fieldless questions with the authored correct response and feedback in worked-solution.',
        'Quiz require_exact, input_mode, shuffle, and gated settings are retained in the audit; the current content schema has no corresponding policy attributes.',
        'Canonical blank values retain their source math/text representation. Runtime grading eligibility must be checked using the existing validator; no symbolic equivalence is asserted.',
        'Source controls with require_exact:false may become numerically gradable under Course Academy rules; their question IDs are listed in non_exact_question_ids.',
    ]
    return builder.entities, activities, builder.audit


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--vault', type=Path, default=Path(__file__).resolve().parents[2] / 'study/vault')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    entities, activities, audit = build(args.vault)
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / 'entities.json').write_text(json.dumps(entities, ensure_ascii=False, indent=2) + '\n')
    (args.output / 'audit.json').write_text(json.dumps(audit, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'activities': activities, 'counts': audit['counts'], 'quiz_types': audit['quiz_types'],
                      'source_repairs': len(audit['source_repairs']), 'non_exact_questions': len(audit['non_exact_question_ids'])}, indent=2))
