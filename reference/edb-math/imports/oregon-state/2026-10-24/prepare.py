"""Add the missing PRQ/GD assignments using the installed native free fields.

Derived from the reviewed 2026-10-21 F26 importer; never modifies the vault.
Use explicit per-problem lesson links, stable identities, and additive targets.
"""
from pathlib import Path
import collections,hashlib,json,re,sys
from datetime import date,datetime,time,timezone
from zoneinfo import ZoneInfo
import yaml
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT/'scripts'))
from f26_assignment_content import Builder,COURSES,LEGACY_SEEDS,QUIZ,NAV_LINE,NAV_SECTION,UniqueKeyLoader
from import_school_assignments import Import,PROBLEM,tidy,DEFAULT_LEARNER
from sync_f26_assignments import edn
OUT=Path(__file__).resolve().parent
VAULT=Path('/home/jake/Developer/study/vault')

class ReviewedBuilder(Builder):
    def canonical_question(self, source, key, quiz, path, context=''):
        assert set(quiz) <= {'id', 'content', 'fields', 'feedback', 'shuffle', 'gated'}
        prompt = self.render_text(quiz['content'], path, quiz['id'])
        fields, audits, notes = [], [], []
        keys = set()

        def answer(local, item):
            assert set(item) <= {'id', 'type', 'value', 'feedback'}
            assert item['type'] in ('text', 'math', 'image')
            # This batch has no image answer values; images remain in prompts.
            assert item['type'] != 'image'
            attrs = {'answer__type': ':answer.type/' + item['type'],
                     'answer__value': self.render_text(item['value'], path, local)}
            if item.get('feedback'):
                attrs['answer__feedback'] = self.render_text(item['feedback'], path, local + '/feedback')
            return self.entity(source, key + '/' + local, 'answer', **attrs)

        for field in quiz['fields']:
            fkey, kind = field['key'], field['type']
            assert fkey not in keys
            keys.add(fkey)
            assert set(field) <= {'key', 'type', 'correct', 'choices'}
            attrs = {'answer_field__key': fkey}
            if kind == 'checkbox' and 'correct' not in field:
                # A personal reflection has no canonical boolean choices.
                assert len(quiz['fields']) == 1
                labels = []
                for choice in field['choices']:
                    assert choice['type'] == 'text'
                    labels.append(choice['id'] + '. ' + self.render_text(choice['value'], path, quiz['id']))
                    if choice.get('feedback'):
                        notes.append('**' + choice['id'] + ':** ' + self.render_text(choice['feedback'], path, quiz['id']))
                prompt += '\n\n' + '\n\n'.join(labels)
                prompt += '\n\nList all applicable choices: {{' + fkey + '}}'
                kind = 'free'
                self.audit['grading_limitations'].append({'source': str(path.relative_to(self.vault)),
                    'quiz_id': quiz['id'], 'reason': 'Unkeyed personal checkbox reflection uses an ungraded free response; original options and feedback retained.'})
            elif kind in ('blank', 'free'):
                assert set(field) == {'key', 'type', 'correct'}
                correct = answer(fkey + '/canonical', field['correct'])
                attrs.update(answer_field__choices=[correct], answer_field__correct=correct)
            elif kind in ('radio', 'select'):
                assert set(field) == {'key', 'type', 'choices', 'correct'}
                choices = {c['id']: answer(fkey + '/option-' + c['id'], c) for c in field['choices']}
                assert len(choices) == len(field['choices']) >= 2
                attrs.update(answer_field__choices=list(choices.values()), answer_field__correct=choices[field['correct']])
            else:
                raise ValueError((path, quiz['id'], kind))
            attrs['answer_field__type'] = ':answer-field.type/' + kind
            fid = self.entity(source, key + '/' + fkey, 'answer-field', **attrs)
            fields.append(fid)
            audits.append({'field_id': fid, 'key': fkey, 'type': kind, 'source_type': field['type']})
            if kind != 'radio' and '{{' + fkey + '}}' not in prompt:
                prompt += '\n\nYour response: {{' + fkey + '}}'
        attrs = {'question__problem': tidy(context + '\n\n' + prompt), 'question__answer_fields': fields}
        if quiz.get('feedback'):
            notes.insert(0, self.render_text(quiz['feedback'], path, quiz['id'] + '/feedback'))
        if notes:
            attrs['question__worked_solution'] = '\n\n'.join(notes)
        qid = self.entity(source, key, 'question', **attrs)
        return qid, {'quiz_id': quiz['id'], 'type': 'fields', 'question_id': qid, 'fields': audits}

    def assignment(self, relative):
        path = self.vault / relative
        raw = path.read_text()
        code = re.fullmatch(r'\d{2}-\d{2}-\d{2}_((?:R|OHW|WHW|SG|PRQ|GD)-\d+)\.md', path.name)[1]
        source = LEGACY_SEEDS.get((path.parent.name, code), f'F26/{path.parent.name}/{code}')
        markers = list(PROBLEM.finditer(raw))
        assert [int(m[1]) for m in markers] == list(range(1, len(markers) + 1))
        intro = self.render_text(tidy(NAV_SECTION.sub('', raw[:markers[0].start()])), path, 'instructions')
        tutorial = self.entity(source, 'instructions', 'tutorial', tutorial__title='Assignment information', tutorial__content=intro)
        contents, problems, seen = [tutorial], [], set()
        for i, marker in enumerate(markers):
            number = marker[1]
            body = raw[marker.end():markers[i + 1].start() if i + 1 < len(markers) else len(raw)]
            blocks = list(QUIZ.finditer(body))
            questions, quizzes, parts, direct, supporting = [], [], [], set(), set()
            if not blocks:
                # PRQ-7 item 3 is the original optional video, with no response.
                assert code == 'PRQ-7' and number == '3' and 'No response is requested.' in body
                text = tidy(NAV_LINE.sub('', body))
                question = self.entity(source, f'problem-{number}/question', 'question',
                    question__problem=self.render_text(text, path, f'problem-{number}'))
                questions.append(question)
                mappings = self.topic_links(body, path)
                direct.update(x['topic_id'] for x in mappings['direct'])
                supporting.update(x['topic_id'] for x in mappings['supporting'])
                assert direct == {1169, 2201}, direct
                context = ''
            else:
                context = self.render_text(tidy(body[:blocks[0].start()]), path, f'problem-{number}/context')
                for j, block in enumerate(blocks):
                    quiz = yaml.load(block[1], Loader=UniqueKeyLoader)
                    assert quiz['id'] not in seen
                    seen.add(quiz['id'])
                    if code.startswith(('PRQ','GD')):
                        assert len(blocks) == 1 and re.fullmatch(r'canvas-\d+(?:-q\d+)?', quiz['id'])
                        part = ''
                    else:
                        part = re.fullmatch('q-' + number + r'([a-z]?|-[a-z][a-z0-9-]*)', quiz['id'])[1].lstrip('-')
                        assert len(blocks) == 1 or part
                    parts.append(part)
                    key = f'problem-{number}/part-{part}' if part else f'problem-{number}/question'
                    question, qa = self.question(source, key, quiz, path, context if len(blocks) == 1 else '')
                    questions.append(question)
                    tail = body[block.end():blocks[j+1].start() if j+1 < len(blocks) else len(body)]
                    assert not tidy(NAV_LINE.sub('', tail)), (relative, quiz['id'])
                    mappings = self.topic_links(tail, path)
                    direct.update(x['topic_id'] for x in mappings['direct'])
                    supporting.update(x['topic_id'] for x in mappings['supporting'])
                    qa['topics'] = mappings
                    quizzes.append(qa)
            if len(questions) > 1:
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
            contents.append(self.entity(source, f'problem-{number}', 'assigned-problem', **attrs))
            problems.append({'number': int(number), 'quizzes': quizzes, 'direct': sorted(direct),
                             'supporting': sorted(supporting), 'topics': topics})
        steps = self.sequence(source, ['instructions/step'] + [f'problem-{m[1]}/step' for m in markers], contents)
        day = date.fromisoformat(re.search(r'^Due:\s*(\d{4}-\d{2}-\d{2})\s*$', raw, re.M)[1])
        assert re.search(r'^Due time: 11:59 p\.m\. PDT$',raw,re.M)
        local_due=datetime.combine(day,time(23,59),ZoneInfo('America/Los_Angeles'))
        assert local_due.tzname()=='PDT'
        due=local_due.astimezone(timezone.utc).isoformat().replace('+00:00','Z')
        title = f'MTH {path.parent.name} — {code}'
        activity = self.entity(source, 'activity', 'activity', activity__title=title,
            activity__type=':activity.type/assignment', activity__steps=steps,
            activity__first_step=steps[0], activity__due={'$inst': due},
            activity__course={'$ref': [':course/id', {'$uuid': COURSES[path.parent.name]}]})
        self.audit['activities'].append({'source': relative, 'identity_source': source, 'activity_id': activity,
            'title': title, 'sha256': hashlib.sha256(raw.encode()).hexdigest(), 'due': due, 'problems': problems})
        return activity

    def validate(self):
        rows = {r[':db/id']: r for r in self.entities}
        assert len(rows) == len(self.entities)
        owners = collections.defaultdict(list)
        for uid, row in rows.items():
            for attr in (':activity/steps', ':multistep/steps', ':question/answer-fields', ':answer-field/choices'):
                for child in row.get(attr, []):
                    assert child in rows
                    owners[child].append(uid)
            if ':answer-field/id' in row:
                correct = row.get(':answer-field/correct')
                assert row[':answer-field/type'] == ':answer-field.type/free' or correct
                assert correct is None or correct in row[':answer-field/choices']
            if ':question/id' in row:
                assert row[':question/problem'].strip()
                fields = [rows[f] for f in row.get(':question/answer-fields', [])]
                keys = {f[':answer-field/key'] for f in fields}
                inline = set(re.findall(r'\{\{([^}]+)\}\}', row[':question/problem']))
                assert len(keys) == len(fields) and inline <= keys
                assert all(f[':answer-field/type'] == ':answer-field.type/radio' for f in fields if f[':answer-field/key'] not in inline)
            for kind in ('activity', 'multistep'):
                if f':{kind}/steps' in row:
                    owned, seen = set(row[f':{kind}/steps']), set()
                    cursor = row[f':{kind}/first-step']
                    while cursor:
                        assert cursor in owned and cursor not in seen
                        seen.add(cursor)
                        assert rows[cursor][':step/content'] in rows
                        cursor = rows[cursor].get(':step/next')
                    assert owned == seen
        for uid, row in rows.items():
            if any(k in row for k in (':step/id', ':answer/id', ':answer-field/id')):
                assert len(owners[uid]) == 1


def main():
    snapshot=json.loads((ROOT/'.local/edb/f26-new-2026-10-23/before.json').read_text())
    rows={int(e):r for e,r in snapshot['entities'].items()}
    missing=json.loads((OUT/'missing-sources.json').read_text())
    activities_by_id={r['activity/id']['$uuid']:e for e,r in rows.items() if 'activity/id' in r}
    builder=ReviewedBuilder(VAULT)
    sources=[r['path'] for r in missing]
    assert all(r['activity_uuid'] not in activities_by_id for r in missing)
    activities=[builder.assignment(source) for source in sources]
    builder.validate()
    assert len(activities)==2 and sum(':question/id' in r for r in builder.entities)==6
    model=Import(VAULT,{});model.entities=builder.entities
    forms=model.transaction(snapshot,DEFAULT_LEARNER,activities)
    learner=next(e for e,r in rows.items() if r.get('learner/id')==DEFAULT_LEARNER)
    topics={r['topic/math-academy-id']:e for e,r in rows.items() if 'topic/math-academy-id' in r}
    direct={n for a in builder.audit['activities'] for p in a['problems'] for n in p['direct']}
    explicit={n for a in builder.audit['activities'] for p in a['problems'] for n in p['supporting']}
    # Also independently check the assignment navigation lists against the
    # per-problem maps. Neither local file paths nor titles create new topics.
    navigation={}
    for source in sources:
        p=VAULT/source;raw=p.read_text();mappings=builder.topic_links(raw,p)
        navigation[source]=mappings
        assert {r['topic_id'] for r in mappings['direct']} <= direct
        assert {r['topic_id'] for r in mappings['supporting']} <= explicit
    assert direct|explicit <= topics.keys()
    roots={topics[n] for n in direct|explicit}
    prerequisites=collections.defaultdict(set)
    for e,r in rows.items():
        if 'topic/id' not in r:continue
        for dependent in r.get('topic/next',[]):prerequisites[dependent].add(e)
    closure=set(roots);pending=list(roots)
    while pending:
        for prerequisite in prerequisites[pending.pop()]:
            if prerequisite not in closure:closure.add(prerequisite);pending.append(prerequisite)
    assert all('topic/id' in rows[e] and rows[e].get('topic/title') for e in closure)
    requested=closure if '--all-prerequisite-ancestors' in sys.argv else roots
    before_targets=set(rows[learner].get('learner/targets',[]))
    target_forms=[f for f in forms if isinstance(f,list) and f[2]==':learner/targets']
    added={f[3] for f in target_forms}
    for e in sorted(requested-before_targets-added):forms.append([':db/add',learner,':learner/targets',e]);added.add(e)
    assert added==requested-before_targets
    for f in forms:
        if isinstance(f,list):assert f[0]==':db/add' and f[2] in {':learner/assignments',':learner/targets'}
    payload='[\n'+'\n '.join(edn(f) for f in forms)+'\n]\n'
    (OUT/'transaction.edn').write_text(payload)
    (OUT/'entities.json').write_text(json.dumps(builder.entities,ensure_ascii=False,indent=2)+'\n')
    audit=builder.audit
    def describe(ids):return [{'entity':e,'math_academy_id':rows[e]['topic/math-academy-id'],'title':rows[e]['topic/title'],'new_target':e not in before_targets} for e in sorted(ids)]
    audit.update(database='math',basis_t=snapshot['basis_t'],learner_uuid=DEFAULT_LEARNER,learner_entity=learner,
        selected_sources=sources,activity_ids=activities,assets=list(builder.assets.values()),navigation=navigation,
        direct_topic_ids=sorted(direct),explicit_prerequisite_ids=sorted(explicit),
        topic_roots=describe(roots),all_requested_targets=describe(requested),prerequisite_ancestor_closure=describe(closure),added_targets=describe(added),
        old_target_count=len(before_targets),expected_target_count=len(before_targets|requested),
        old_assignment_eids=sorted(rows[learner].get('learner/assignments',[])),old_target_eids=sorted(before_targets),
        counts=dict(collections.Counter(next(k[1:-3] for k in r if k.endswith('/id') and k!=':db/id') for r in builder.entities)),
        forms=len(forms),sha256=hashlib.sha256(payload.encode()).hexdigest(),source=':course-academy.source/editor',
        prerequisite_rule='Explicit per-problem topic and prerequisite links are the target set by default; --all-prerequisite-ancestors selects the separately audited reverse topic/next closure. Only additive target links.')
    (OUT/'source-audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:audit[k] for k in ['basis_t','selected_sources','counts','old_target_count','expected_target_count','forms','sha256']},indent=2))
    print('Topics:',len(direct),'explicit prerequisites:',len(explicit),'closure:',len(closure),'new targets:',len(added))

if __name__=='__main__':main()
