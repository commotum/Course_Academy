#!/usr/bin/env python3
"""Prepare the nine new MTH 341 activities. No durable database writes.

Reuse canonical conversion and deterministic identities, but retain the newly
supported free fields and resolve verified file links into the study repository.
The source, authored study content, and learner enrollment are separate requests.
"""
from pathlib import Path
import copy
import hashlib
import json
import re
import sys
import threading
import uuid
from urllib.parse import unquote, urlsplit, parse_qs

ROOT = Path(__file__).resolve().parents[5]
OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'scripts'))
from f26_assignment_content import Builder, COURSES, NAV_SECTION, PROBLEM, QUIZ, UniqueKeyLoader
from import_school_assignments import tidy
import yaml
from datetime import datetime, date, time, timezone
from zoneinfo import ZoneInfo
from import_school_assignments import VAULT, DEFAULT_LEARNER
from question_markers import repair_problem
sys.path.insert(0, str(ROOT / 'capture'))
from scripts.config import Config
from scripts.database.client import EDBClient
from scripts.database.edn import kw, Keyword, Tagged, dumps
from scripts.database.images import ImageLibrary

FILES = ['F26/341/10-02-26_GD-1.md', 'F26/341/10-02-26_PRQ-1.md', 'F26/341/10-06-26_PRQ-2.md', 'F26/341/10-07-26_PRQ-3.md', 'F26/341/10-09-26_GD-2.md', 'F26/341/10-09-26_PRQ-4.md', 'F26/341/10-13-26_PRQ-5.md', 'F26/341/10-14-26_PRQ-6.md', 'F26/341/10-16-26_SG-1.md']

def save(name, value):
    (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

class CurrentBuilder(Builder):
    def assignment(self, relative):
        path = self.vault / relative
        raw = path.read_text()
        code = re.fullmatch(r'\d{2}-\d{2}-\d{2}_((?:PRQ|GD|SG)-\d+)\.md', path.name)[1]
        source = f'F26/{path.parent.name}/{code}'
        markers = list(PROBLEM.finditer(raw))
        assert [int(m[1]) for m in markers] == list(range(1, len(markers) + 1))
        title = re.search(r'^\*\*(MTH 341[^\n]+)\*\*\s*$', raw, re.M)[1]
        intro = self.render_text(tidy(NAV_SECTION.sub('', raw[:markers[0].start()])), path, 'instructions')
        tutorial = self.entity(source, 'instructions', 'tutorial', tutorial__title='Assignment information', tutorial__content=intro)
        contents, problems, seen = [tutorial], [], set()
        for i, marker in enumerate(markers):
            number = marker[1]
            body = raw[marker.end():markers[i+1].start() if i+1 < len(markers) else len(raw)]
            blocks = list(QUIZ.finditer(body))
            if not blocks:
                assert code=='SG-1' and number=='1' and 'study direction' in body
                direction=re.sub(r'^\*\*(Topics|Prerequisites):\*\*.*$', '',body,flags=re.M)
                tutorial=self.entity(source,f'problem-{number}/direction','tutorial',tutorial__title='Study direction',tutorial__content=self.render_text(tidy(direction),path,f'problem-{number}/direction'))
                contents.append(tutorial)
                problems.append({'number':int(number),'kind':'study-direction','content_id':tutorial,'quizzes':[],'topics':[]})
                continue
            context = self.render_text(tidy(body[:blocks[0].start()]), path, f'problem-{number}/context')
            questions, quizzes, direct, supporting = [], [], set(), set()
            for j, match in enumerate(blocks):
                quiz = yaml.load(match[1], Loader=UniqueKeyLoader)
                assert quiz['id'] not in seen
                seen.add(quiz['id'])
                key = f'problem-{number}/quiz-{quiz["id"]}'
                question, qa = self.question(source, key, quiz, path, context if len(blocks)==1 else '')
                questions.append(question); quizzes.append(qa)
                tail = body[match.end():blocks[j+1].start() if j+1<len(blocks) else len(body)]
                mapping = self.topic_links(tail, path)
                direct.update(x['topic_id'] for x in mapping['direct'])
                # Self-reports and peer comments are not mathematical coverage.
                if not any(f.get('correct') is None for f in quiz['fields']) and 'peer' not in quiz['id']:
                    supporting.update(x['topic_id'] for x in mapping['supporting'])
            if len(questions)>1:
                steps = self.sequence(source, [f'problem-{number}/quiz-{q["quiz_id"]}/step' for q in quizzes], questions)
                attrs = {'multistep__steps': steps, 'multistep__first_step': steps[0]}
                if context: attrs['multistep__context'] = context
                content = self.entity(source, f'problem-{number}/multistep', 'multistep', **attrs)
            else:
                content = questions[0]
            topics = sorted(direct | supporting)
            attrs = {'assigned_problem__content': content}
            if topics: attrs['assigned_problem__topic_coverage'] = [{'$ref':[':topic/math-academy-id', t]} for t in topics]
            assigned = self.entity(source, f'problem-{number}', 'assigned-problem', **attrs)
            contents.append(assigned)
            problems.append({'number':int(number), 'assigned_problem_id':assigned, 'content_id':content,
                             'quizzes':quizzes, 'direct':sorted(direct), 'supporting':sorted(supporting), 'topics':topics})
        steps = self.sequence(source, ['instructions/step']+[f'problem-{m[1]}/step' for m in markers], contents)
        attrs = {'activity__title':title, 'activity__type':':activity.type/assignment', 'activity__steps':steps,
                 'activity__first_step':steps[0], 'activity__course':{'$ref':[':course/id',{'$uuid':COURSES[path.parent.name]}]}}
        due_match = re.search(r'^Due:\s*(\d{4}-\d{2}-\d{2})\s*$',raw,re.M)
        due = None
        if due_match:
            due = datetime.combine(date.fromisoformat(due_match[1]),time(23,59,59),ZoneInfo('America/Los_Angeles')).astimezone(timezone.utc).isoformat().replace('+00:00','Z')
            attrs['activity__due'] = {'$inst':due}
        activity = self.entity(source,'activity','activity',**attrs)
        self.audit['activities'].append({'source':relative,'identity_source':source,'title':title,'activity_id':activity,
            'sha256':hashlib.sha256(raw.encode()).hexdigest(),'due':due,'due_source':due_match[0] if due_match else None,
            'problems':problems})
        return activity

    def local_link(self, target, source):
        parsed = urlsplit(target)
        if parsed.scheme == 'file':
            path = Path(unquote(parsed.path)).resolve()
            if parsed.netloc or not path.is_relative_to(VAULT.parent / 'MA') or not path.is_file() or path.suffix != '.md':
                raise ValueError(f'Unverified study lesson link: {target}')
            return path, parsed
        return super().local_link(target, source)

    def canonical_question(self, source, key, quiz, path, context=''):
        if any(f['type']=='checkbox' and f.get('correct') is not None for f in quiz['fields']):
            assert len(quiz['fields']) == 1, 'Review mixed checkbox questions before conversion'
            field = quiz['fields'][0]
            correct = set(field['correct'])
            assert correct <= {c['id'] for c in field['choices']}
            prompt = self.render_text(quiz['content'],path,quiz['id']+'/content')
            fields, field_audit = [], []
            for choice in field['choices']:
                fkey = field['key']+'-'+choice['id']
                prompt += '\n\n'+choice['id']+'. '+self.render_text(choice['value'],path,quiz['id']+'/'+choice['id'])+': {{'+fkey+'}}'
                bank = [self.entity(source,key+'/'+fkey+'/'+value,'answer',answer__type=':answer.type/text',answer__value=value) for value in ('true','false')]
                canonical = bank[0] if choice['id'] in correct else bank[1]
                fid = self.entity(source,key+'/'+fkey,'answer-field',answer_field__key=fkey,answer_field__type=':answer-field.type/checkbox',answer_field__choices=bank,answer_field__correct=canonical)
                fields.append(fid);field_audit.append({'field_id':fid,'key':fkey,'type':'checkbox','correct_answer_id':canonical})
            attrs={'question__problem':tidy(context+'\n\n'+prompt),'question__answer_fields':fields}
            if quiz.get('feedback'):attrs['question__worked_solution']=self.render_text(quiz['feedback'],path,quiz['id']+'/feedback')
            uid=self.entity(source,key,'question',**attrs)
            return uid,{'quiz_id':quiz['id'],'question_id':uid,'identity_key':key,'type':'fields','fields':field_audit}
        if any(f.get('correct') is None for f in quiz['fields']):
            assert len(quiz['fields']) == 1, 'Review mixed keyed/unkeyed questions before conversion'
            field = quiz['fields'][0]
            assert field['type'] in ('radio','checkbox')
            prompt = self.render_text(quiz['content'],path,quiz['id']+'/content')
            for choice in field['choices']:
                prompt += '\n\n' + choice['id'] + '. ' + self.render_text(choice['value'],path,quiz['id']+'/'+choice['id'])
            fid = self.entity(source,key+'/'+field['key'],'answer-field',answer_field__key=field['key'],answer_field__type=':answer-field.type/free')
            attrs = {'question__problem':tidy(context+'\n\n'+prompt),'question__answer_fields':[fid]}
            feedback = list(dict.fromkeys([quiz.get('feedback','')]+[c.get('feedback','') for c in field['choices']]))
            worked = '\n\n'.join(self.render_text(v,path,quiz['id']+'/feedback') for v in feedback if v)
            if worked: attrs['question__worked_solution'] = worked
            uid = self.entity(source,key,'question',**attrs)
            self.audit.setdefault('unkeyed_self_reports',[]).append({'question_id':uid,'source':str(path.relative_to(self.vault)),
                'quiz_id':quiz['id'],'source_control':field['type'],'conversion':'Choice text preserved in prompt; free response editor; no canonical answer, grading, or correctness evidence.'})
            return uid, {'quiz_id':quiz['id'],'question_id':uid,'identity_key':key,'type':'fields',
                         'fields':[{'field_id':fid,'key':field['key'],'type':'free'}]}
        # Use the existing canonical answer conversion. Free references have
        # the same owned bank shape, but never assert correctness at runtime.
        converted = copy.deepcopy(quiz)
        free = {f['key'] for f in converted['fields'] if f['type'] == 'free'}
        for field in converted['fields']:
            if field['key'] in free:
                field['type'] = 'blank'
        uid, audit = super().canonical_question(source, key, converted, path, context)
        for field in audit['fields']:
            if field['key'] in free:
                field['type'] = 'free'
                row = next(r for r in self.entities if r[':db/id'] == field['field_id'])
                row[':answer-field/type'] = ':answer-field.type/free'
        question = next(r for r in self.entities if r[':db/id'] == uid)
        answer_fields = [r for r in self.entities if r[':db/id'] in question[':question/answer-fields']]
        question[':question/problem'] = repair_problem(question[':question/problem'], answer_fields)
        return uid, audit

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    b = CurrentBuilder(VAULT)
    activities = [b.assignment(f) for f in FILES]
    # Free fields may have no bank or reference under the current schema.
    unkeyed = {f['field_id'] for a in b.audit['activities'] for p in a['problems'] for q in p['quizzes']
               for f in q['fields'] if 'correct_answer_id' not in f and f['type']=='free'}
    for row in b.entities:
        if row[':db/id'] in unkeyed:
            # Existing structural validation expects canonical membership; its
            # remaining checks run below, and native preview validates free fields.
            row[':answer-field/choices'] = []
    records = {r[':db/id']:r for r in b.entities}
    assert len(records)==len(b.entities)
    for row in b.entities:
        if ':question/id' in row:
            fields = [records[f] for f in row.get(':question/answer-fields',[])]
            assert len({f[':answer-field/key'] for f in fields})==len(fields)
            assert set(re.findall(r'\{\{([^}]+)\}\}',row[':question/problem'])) <= {f[':answer-field/key'] for f in fields}
        if ':answer-field/correct' in row: assert row[':answer-field/correct'] in row[':answer-field/choices']
    owners = {}
    for uid,row in records.items():
        for attr in (':activity/steps', ':multistep/steps', ':question/answer-fields', ':answer-field/choices'):
            for child in row.get(attr,[]):
                assert child in records, (uid,attr,child)
                assert child not in owners, ('Shared component',child)
                owners[child] = uid
        if ':step/content' in row: assert row[':step/content'] in records
        if ':answer/id' in row: assert row[':answer/value'].strip()
        for kind in ('activity','multistep'):
            if ':'+kind+'/steps' not in row: continue
            members=set(row[':'+kind+'/steps']); visited=set(); cursor=row[':'+kind+'/first-step']
            while cursor:
                assert cursor in members and cursor not in visited
                visited.add(cursor); cursor=records[cursor].get(':step/next')
            assert visited==members
    for uid,row in records.items():
        if any(attr in row for attr in (':step/id', ':answer-field/id', ':answer/id')): assert uid in owners
    full = copy.deepcopy(b.entities)
    ids = {r[':db/id']: next((k, v) for k, v in r.items() if k.endswith('/id') and k != ':db/id') for r in full}
    config = Config()
    c = EDBClient(config, threading.Event())
    dbdir = OUT / 'db'
    dbdir.mkdir(parents=True, exist_ok=True)
    identity = c.status()
    basis = identity['basis']
    save('db/identity.json', identity)

    def query(name, text, args):
        return c.query(text, args, dbdir, name, basis)

    attrs = query('attributes', '''[:find ?a ?ident ?typ ?card :where
      [?a :db/ident ?ident] [?a :db/valueType ?t] [?t :db/ident ?typ]
      [?a :db/cardinality ?c] [?c :db/ident ?card]]''', [])
    schema = {str(name): (eid, str(typ), str(card)) for eid, name, typ, card in attrs}
    references = {v for r in full for k, v in r.items() if isinstance(v, str) and v.startswith(':')}
    references |= {':org/Oregon-State', ':agent/gpt-6.1-sol-high', ':person/jake'}
    enums = query('idents', '[:find ?e ?ident :in $ [?ident ...] :where [?e :db/ident ?ident]]', [[kw(x) for x in sorted(references)]])
    found = {str(name) for _, name in enums}
    assert references <= found, references - found
    pairs = [[kw(a), uuid.UUID(v['$uuid'])] for a, v in ids.values()]
    existing = query('candidate-identities', '''[:find ?e ?attr ?id :in $ [[?attr ?id]] :where [?e ?attr ?id]]''', [pairs])
    assert not existing, 'Selected content already exists; reconcile explicitly instead of replacing it.'
    topic_ids = sorted({t for a in b.audit['activities'] for p in a['problems'] for t in p['topics']})
    topics = query('topics', '[:find ?e ?mid ?id :in $ [?mid ...] :where [?e :topic/math-academy-id ?mid] [?e :topic/id ?id]]', [topic_ids])
    assert {mid for _, mid, _ in topics} == set(topic_ids), 'Unresolved coverage topics'
    courses = sorted({r[':activity/course']['$ref'][1]['$uuid'] for r in full if ':activity/course' in r})
    course_rows = query('courses', '[:find ?e ?id :in $ [?id ...] :where [?e :course/id ?id]]', [[uuid.UUID(x) for x in courses]])
    assert {str(uid) for _, uid in course_rows} == set(courses)
    learners = query('learner', '''[:find (pull ?l [:db/id :learner/id
      {[:learner/assignments :limit nil] [:db/id]}
      {[:learner/targets :limit nil] [:db/id]}])
      :in $ ?id :where [?l :learner/id ?id]]''', [DEFAULT_LEARNER])
    assert len(learners) == 1
    learner = learners[0][0]
    assigned = {v[':db/id'] for v in learner.get(':learner/assignments', [])}
    targets = {v[':db/id'] for v in learner.get(':learner/targets', [])}

    # Original images and authored diagrams are staged by hash, never installed
    # into the live image library by this preparation command.
    images = ImageLibrary(OUT / 'assets', OUT)
    def localize(value):
        def replace(m):
            path = Path(parse_qs(urlsplit(m[0]).query)['path'][0])
            relative = images.store(path.read_bytes(), str(path))
            return relative
        return images.text(re.sub(r'/api/asset\?path=[^\s)"<>]+', replace, value))
    def convert(value, attr=''):
        if isinstance(value, dict):
            if '$uuid' in value: return uuid.UUID(value['$uuid'])
            if '$inst' in value: return Tagged('inst', value['$inst'])
            if '$ref' in value: return [kw(value['$ref'][0]), convert(value['$ref'][1], value['$ref'][0])]
            return {kw(k): convert(v, k) for k, v in value.items()}
        if isinstance(value, list): return [convert(v, attr) for v in value]
        if isinstance(value, str):
            if attr == ':db/ensure' or schema.get(attr, ('', '', ''))[1] in (':db.type/ref', ':db.type/keyword'):
                return kw(value) if value.startswith(':') else value
            if schema.get(attr, ('', '', ''))[1] == ':db.type/string': return localize(value)
        return value

    original, authored, transformations = [], [], []
    generated_records = {r[':db/id']:r for r in full}
    for r in full:
        uid = r[':db/id']
        if ':answer/id' in r or ':answer-field/id' in r:
            authored.append(r)
            continue
        base = copy.deepcopy(r)
        patch = {':db/id': {'$ref': list(ids[uid])}, ':db/ensure': r[':db/ensure']}
        for attr in (':question/worked-solution', ':question/answer-fields', ':assigned-problem/topic-coverage'):
            if attr in base: patch[attr] = base.pop(attr)
        if ':question/problem' in base:
            before = base[':question/problem']
            after = re.sub(r'\n\nWritten response: \{\{[^}]+\}\}\s*$', '', before)
            after = re.sub(r'\{\{[^}]+\}\}', '____', after)
            for field_id in r.get(':question/answer-fields',[]):
                field=generated_records[field_id]
                if field[':answer-field/type'] not in (':answer-field.type/radio',':answer-field.type/select'): continue
                for n,answer_id in enumerate(field[':answer-field/choices'],1):
                    answer=generated_records[answer_id]
                    value=answer[':answer/value']
                    if answer[':answer/type']==':answer.type/math': value='$'+value+'$'
                    elif answer[':answer/type']==':answer.type/image': value=f'![Choice {n}]({value})'
                    after+='\n\n'+str(n)+'. '+value
            if after != before:
                base[':question/problem'] = after
                patch[':question/problem'] = before
                transformations.append({'id': uid, 'change': 'Move response editors to agent layer; source layer contains unfilled prompts.'})
        if ':tutorial/content' in base and base.get(':tutorial/title')=='Assignment information':
            before = base[':tutorial/content']
            header = before.split('\n\n## Instructions', 1)[0]
            kept = [line for line in header.splitlines() if line.startswith(('**MTH', 'Due:', 'Due time:', 'Source:', 'Textbook:', 'Question PDF:', 'Supplied solutions:', 'Test date:', 'Exam window:', 'Exam deadline:', 'Referenced reading:'))]
            base[':tutorial/content'] = '\n\n'.join(kept)
            if base[':tutorial/content'] != before: patch[':tutorial/content'] = before
        original.append(base)
        if set(patch) - {':db/id', ':db/ensure'}: authored.append(patch)

    # Later-stage refs use installed unique identities, never preview tempids.
    original_ids = {r[':db/id'] for r in original}
    def refs(value):
        if isinstance(value, dict):
            if any(k.startswith('$') for k in value): return value
            return {k: refs(v) for k, v in value.items()}
        if isinstance(value, list): return [refs(v) for v in value]
        if isinstance(value, str) and value in original_ids:
            return {'$ref': list(ids[value])}
        return value
    authored = [refs(r) for r in authored]
    learner_forms = [[kw('db/add'), [kw('learner/id'), DEFAULT_LEARNER], kw('learner/assignments'),
                      [kw('activity/id'), uuid.UUID(ids[a][1]['$uuid'])]] for a in activities]
    added_topics = [(eid, mid, uid) for eid, mid, uid in topics if eid not in targets]
    learner_forms += [[kw('db/add'), [kw('learner/id'), DEFAULT_LEARNER], kw('learner/targets'),
                       [kw('topic/id'), uid]] for _, _, uid in added_topics]
    transactions = []
    for name, source, forms in [('1-assigned-material.edn', ':org/Oregon-State', original),
                                ('2-authored-study-content.edn', ':agent/gpt-6.1-sol-high', authored),
                                ('3-learner-links.edn', ':person/jake', learner_forms)]:
        text = dumps(convert(forms)) + '\n'
        (OUT / name).write_text(text)
        transactions.append({'file': name, 'source': source, 'forms': len(forms),
                             'sha256': hashlib.sha256(text.encode()).hexdigest(),
                             'request_key': 'f26-341-oct13-' + str(uuid.uuid4())})
    # Fixed output projections query only the prepared entities at db-after.
    (OUT / 'pull-pattern.edn').write_text('[:db/id *]\n')
    (OUT / 'pull-identities.edn').write_text(dumps([[kw(a), uuid.UUID(v['$uuid'])] for a, v in ids.values()]) + '\n')
    b.audit.update({'assets': list(b.assets.values()), 'basis': basis,
                    'selected_sources': FILES, 'added_target_math_academy_ids': [mid for _, mid, _ in added_topics],
                    'response_fields': 'Free fields collect written responses without automatic correctness or mastery evidence.',
                    'image_map': images.saved, 'source_transformations': transformations})
    save('audit.json', b.audit)
    save('entities.json', full)
    save('prepared-manifest.json', {'database': identity['database'], 'lineage': identity['lineage'],
        'basis_read': basis, 'committed': False, 'transactions': transactions,
        'learner_id': DEFAULT_LEARNER, 'existing_assignments': len(assigned),
        'new_assignments': len(activities), 'new_targets': len(added_topics),
        'counts': {kind: sum(':' + kind + '/id' in r for r in full) for kind in
                   ['activity', 'assigned-problem', 'question', 'multistep', 'step', 'tutorial', 'answer-field', 'answer']},
        'sources': 'OSU is the assigning institution. Author references and explanations use the verified writing-session model. Publisher/PDF links remain in content.',
        'policy': 'Add definitions, assignments and their verified coverage targets. Preserve existing assignments, targets, learner history, progress, and engine configuration.'})
    print(json.dumps(json.loads((OUT / 'prepared-manifest.json').read_text()), indent=2))

if __name__ == '__main__': main()
