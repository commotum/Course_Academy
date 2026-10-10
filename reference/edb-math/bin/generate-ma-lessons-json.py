#!/usr/bin/env python3
"""Generate source-attributed lesson EDN from archived MA JSON and hashed images."""
import argparse
import collections
import importlib.util
import json
from pathlib import Path
import re
import sys
import uuid

sys.path.insert(0, '/home/jake/Developer/Course_Academy/scripts/question_capture')
from edn import dumps, loads, kw

MD_SCRIPT = Path('/home/jake/Developer/MA/PIPELINE/Math-Academy/3-Capture/1-Source/5-MD/md.py')
spec = importlib.util.spec_from_file_location('ma_markdown_renderer', MD_SCRIPT)
md = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = md
spec.loader.exec_module(md)
# Half-open intervals contain unmatched square brackets inside the outer marker.
# The HTML math span still supplies an unambiguous complete [MATH: ...] value.
original_math_placeholder = md.extract_math_placeholder

def extract_math_placeholder(raw):
    parsed = original_math_placeholder(raw)
    text = raw.strip()
    if parsed is None and text.startswith('[MATH:') and text.endswith(']') and text.count('[MATH:') == 1 and '[FREE_ENTRY' not in text and '[SELECT' not in text:
        return text[len('[MATH:'):-1].strip()
    return parsed

md.extract_math_placeholder = extract_math_placeholder
UNDERLINE = re.compile(r'\$\s*\\underline\{\\hspace\{[^}]*\}\}\s*\$')
IMAGE_LINK = re.compile(r'!\[[^\]]*\]\((images/[^)]+)\)')


def identity(kind, source):
    return uuid.uuid5(uuid.NAMESPACE_URL, f'course-academy:ma:{kind}:{source}')


def entity(tempid, **fields):
    return {kw('db/id'): tempid, **{kw(k.replace('__', '/').replace('_', '-')): v for k, v in fields.items()}}


class HashedImageResolver:
    def __init__(self, topic_id, mapping, math_root):
        self.paths = mapping['by_topic'].get(str(topic_id), {})
        self.math_root = math_root
        self.used = set()

    def relative_markdown_path(self, src):
        path = self.paths.get(src)
        if path is None:
            raise ValueError(f'Unmapped image reference: {src}')
        self.used.add(path)
        return path

    def resolve(self, src):
        path = self.relative_markdown_path(src)
        return self.math_root / path


def checked_content(text, math_root):
    text = text.strip()
    if not text:
        raise ValueError('Empty rendered content')
    if any(marker in text for marker in ('[MATH:', '[IMG:', '[Missing image:', 'Source/Images/', '/home/jake/Developer/MA/DATA')):
        raise ValueError('Unresolved source placeholder in: ' + text[:250])
    for path in IMAGE_LINK.findall(text):
        if not (math_root / path).is_file():
            raise ValueError('Missing stored image: ' + path)
    return text


def answer_representation(source, context, math_root):
    if source.get('content_type') == 'image':
        images = source.get('images', [])
        if len(images) != 1:
            raise ValueError('Image-only answer must reference one image')
        return 'image', context.image_resolver.relative_markdown_path(images[0]['src'])
    text = (md.render_select_option_markdown(source, context) if 'content_type' not in source else md.render_choice_markdown(source, context))
    text = checked_content(text, math_root)
    inline = re.fullmatch(r'\$([^$]+)\$', text, re.S)
    display = re.fullmatch(r'\$\$\s*(.*?)\s*\$\$', text, re.S)
    if inline or display:
        return 'math', (inline or display)[1].strip()
    return 'text', text


def answer_maps(sources, qkey, field_index, context, math_root, totals):
    result = []
    seen = set()
    for index, source in enumerate(sources, 1):
        representation, value = answer_representation(source, context, math_root)
        if (representation, value) in seen:
            continue
        seen.add((representation, value))
        result.append({kw('answer/id'): identity('answer', f'{qkey}:{field_index}:{index}'),
                       kw('answer/type'): kw('answer.type/' + representation),
                       kw('answer/value'): value, kw('db/ensure'): kw('answer/validate')})
    assert result
    totals['answer_values'] += len(result)
    return result


def question_form(item, topic, duplicate_questions, context, math_root, totals):
    qid = str(item['question_id'])
    qkey = f'{topic}:{qid}' if qid in duplicate_questions else qid
    fragments = [md.prompt_blocks(item.get(k, {}), context) for k in ('prompt', 'body', 'graphic', 'calculator_instructions')]
    prompt, body, graphic, calculator = fragments
    simple = (item['question_format'] == 'multiple-choice' and not body and not graphic and not calculator
              and len(prompt) == 1 and prompt[0].kind in {'paragraph', 'display_math'}
              and all(c.get('content_type') == 'text' for c in item.get('choices', [])))
    problem = md.render_question_content_markdown(item, context, prompt, body, graphic, calculator, simple_inline_prompt=simple)
    kind = item['question_format']
    fields = []
    if kind == 'multiple-choice':
        fields.append({kw('answer-field/id'): identity('field', f'{qkey}:1'),
                       kw('answer-field/key'): 'selection', kw('answer-field/type'): kw('answer-field.type/radio'),
                       kw('answer-field/choices'): answer_maps(item['choices'], qkey, 1, context, math_root, totals)})
    else:
        assert kind in {'free-response', 'select-list'}, kind
        inputs = item['free_entry_blanks'] if kind == 'free-response' else item['select_lists']
        assert inputs
        field_number = iter(range(1, len(inputs) + 1))
        problem, replaced = UNDERLINE.subn(lambda _: '{{field-' + str(next(field_number)) + '}}', problem)
        assert replaced == len(inputs), (topic, qid, replaced, len(inputs))
        for index, source in enumerate(inputs, 1):
            field = {kw('answer-field/id'): identity('field', f'{qkey}:{index}'),
                     kw('answer-field/key'): f'field-{index}',
                     kw('answer-field/type'): kw('answer-field.type/' + ('blank' if kind == 'free-response' else 'select'))}
            if kind == 'select-list':
                field[kw('answer-field/choices')] = answer_maps(source['options'], qkey, index, context, math_root, totals)
            fields.append(field)
    form = entity('question-' + qkey, question__id=identity('question', qkey),
                  question__problem=checked_content(problem, math_root), question__answer_fields=fields,
                  db__ensure=kw('question/validate'))
    if qid not in duplicate_questions:
        form[kw('question/math-academy-id')] = 'q-' + qid
    if item.get('calculator_instructions', {}).get('readable_text', '').strip():
        form[kw('question/requires-calculator')] = True
    totals['questions'] += 1
    totals['fields'] += len(fields)
    # Missing answer keys are deliberate: never assert answer-field/correct or ensure complete fields.
    assert all(kw('answer-field/correct') not in field and kw('db/ensure') not in field for field in fields)
    return form, 'question-' + qkey


def lesson_forms(data, duplicate_questions, duplicate_contents, mapping, math_root, topic_ids, totals):
    topic = str(data['topic_id'])
    assert int(topic) in topic_ids, ('unknown topic', topic)
    context = md.MarkdownContext(image_resolver=HashedImageResolver(topic, mapping, math_root))
    question_context = md.MarkdownContext(image_resolver=context.image_resolver, standalone_math_display=False)
    items = data['lesson']['items']
    steps = [item for item in items if item['item_type'] == 'step']
    assert steps
    forms = []
    content_refs = {}
    questions_per_step = collections.defaultdict(list)
    previous = None
    for item in items:
        if item['item_type'] == 'step':
            previous = item
        else:
            assert item['item_type'] == 'question' and previous and previous['step_type'] == 'example'
            form, ref = question_form(item, topic, duplicate_questions, question_context, math_root, totals)
            forms.append(form)
            questions_per_step[str(previous['step_id'])].append(ref)
    kp_refs = []
    for step in steps:
        sid, cid = str(step['step_id']), str(step['content_id'])
        kind = step['step_type']
        key = sid if (kind, cid) in duplicate_contents else cid
        if kind == 'tutorial':
            content = checked_content('\n'.join(md.render_tutorial_step(step, context)), math_root)
            form = entity('tutorial-' + key, tutorial__id=identity('tutorial', key),
                          tutorial__title=step['title'], tutorial__content=content, db__ensure=kw('tutorial/validate'))
            if (kind, cid) not in duplicate_contents:
                form[kw('tutorial/math-academy-id')] = int(cid)
            forms.append(form)
            content_refs[sid] = 'tutorial-' + key
            totals['tutorials'] += 1
        else:
            assert kind == 'example'
            prompt_context = md.MarkdownContext(image_resolver=context.image_resolver, standalone_math_display=False)
            prompt_blocks = []; explanation_blocks = []
            for section in step['sections']:
                if section['section_type'] == 'example_question':
                    prompt_blocks.extend(md.prompt_blocks(section, prompt_context))
                elif md.normalize_ws(section.get('readable_text', '')).upper() != 'EXPLANATION':
                    explanation_blocks.extend(md.html_fragment_to_blocks(section.get('normalized_html', ''), context))
            form = entity('example-' + key, question__id=identity('example', key),
                          question__problem=checked_content(md.blocks_to_markdown(prompt_blocks), math_root),
                          question__worked_solution=checked_content(md.blocks_to_markdown(explanation_blocks), math_root),
                          db__ensure=kw('question/validate'))
            if (kind, cid) not in duplicate_contents:
                form[kw('question/math-academy-id')] = 'e-' + cid
            forms.append(form)
            assert questions_per_step[sid]
            kp = entity('knowledge-point-' + sid, knowledge_point__id=identity('kp', sid),
                        knowledge_point__title=step['title'], knowledge_point__canonical_example='example-' + key,
                        knowledge_point__questions=questions_per_step[sid], db__ensure=kw('knowledge-point/validate'))
            prereqs = sorted({int(ref['topic_id']) for ref in step.get('key_prerequisites', [])})
            assert all(mid in topic_ids for mid in prereqs), ('unknown key prerequisite', topic, sid, prereqs)
            if prereqs:
                kp[kw('knowledge-point/key-prerequisites')] = [[kw('topic/math-academy-id'), mid] for mid in prereqs]
            totals['key_prerequisites'] += len(prereqs)
            forms.append(kp)
            kp_refs.append('knowledge-point-' + sid)
            content_refs[sid] = 'knowledge-point-' + sid
            totals['examples'] += 1
            totals['knowledge_points'] += 1
    step_refs = []
    for index, step in enumerate(steps):
        sid = str(step['step_id'])
        ref = 'step-' + sid
        form = entity(ref, step__id=identity('step', sid), step__math_academy_id=int(sid),
                      step__content=content_refs[sid], db__ensure=kw('step/validate'))
        if index + 1 < len(steps):
            form[kw('step/next')] = 'step-' + str(steps[index + 1]['step_id'])
        forms.append(form)
        step_refs.append(ref)
        totals['steps'] += 1
    assert kp_refs
    forms.append(entity('lesson-' + topic, activity__id=identity('lesson', topic), activity__title=data['topic_title'],
                        activity__type=kw('activity.type/lesson'), activity__scope=[kw('topic/math-academy-id'), int(topic)],
                        activity__steps=step_refs, activity__first_step=step_refs[0], db__ensure=kw('activity/validate')))
    forms.append({kw('db/id'): [kw('topic/math-academy-id'), int(topic)], kw('topic/knowledge-points'): kp_refs,
                  kw('db/ensure'): kw('topic/validate')})
    totals['lessons'] += 1
    return forms, context.image_resolver.used


def generate(args):
    math_root = args.math_root.resolve()
    mapping = json.loads((math_root / 'images/math-academy-map.json').read_text())
    assert not mapping['missing']
    topics_text = (math_root / 'seeds/math-academy/6-topics.edn').read_text()
    topics_text = re.sub(r'("(?:\\.|[^"\\])*")|;[^\n]*', lambda m: m.group(1) or '', topics_text)
    topic_ids = {m[kw('topic/math-academy-id')] for m in loads(topics_text)}
    paths = sorted(args.lessons_root.glob('*/Source/*.json'), key=lambda p: int(p.stem))
    questions = collections.Counter(); contents = collections.Counter()
    for path in paths:
        for item in json.loads(path.read_text())['lesson']['items']:
            if item['item_type'] == 'question':
                questions[str(item['question_id'])] += 1
            else:
                contents[(item['step_type'], str(item['content_id']))] += 1
    duplicate_questions = {key for key, count in questions.items() if count > 1}
    duplicate_contents = {key for key, count in contents.items() if count > 1}
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    assert not list(output.glob('lessons-*.edn')), 'Choose an empty output directory.'
    totals = collections.Counter(); batches = []; used_images = set(); batch = []; batch_topics = []
    all_uuids = set()
    def check_uuid_maps(value):
        if isinstance(value, dict):
            for key, field in value.items():
                if str(key).endswith('/id') and isinstance(field, uuid.UUID):
                    assert field not in all_uuids, ('duplicate generated identity', key, field)
                    all_uuids.add(field)
                check_uuid_maps(field)
        elif isinstance(value, list):
            for field in value: check_uuid_maps(field)
    def emit():
        name = f'lessons-{len(batches) + 1:04d}.edn'
        text = ';; MA JSON baseline: answer keys remain unset; image links use hashed SSD storage.\n[\n' + ''.join(' ' + dumps(m) + '\n' for m in batch) + ']\n'
        assert ':answer-field/correct ' not in text and 'Source/Images/' not in text
        parsed = loads(text[text.index('[\n'):])
        assert parsed == batch
        path = output / name
        path.write_text(text)
        batches.append({'file': name, 'topics': list(batch_topics), 'bytes': path.stat().st_size,
                        'request_key': str(uuid.uuid4()), 'source': ':org/Math-Academy'})
        print(f'Prepared {name}: {len(batch_topics)} lessons; total {totals["lessons"]}/{len(paths)}.', flush=True)
    for index, path in enumerate(paths):
        data = json.loads(path.read_text())
        assert str(data['topic_id']) == path.stem
        try:
            forms, images = lesson_forms(data, duplicate_questions, duplicate_contents, mapping, math_root, topic_ids, totals)
        except Exception as exc:
            raise ValueError(f'Topic {path.stem}: {exc}') from exc
        for form in forms: check_uuid_maps(form)
        batch.extend(forms); batch_topics.append(int(path.stem)); used_images.update(images)
        # One complete lesson first, then batches of 75.
        if index == 0 or len(batch_topics) == args.chunk_topics or index + 1 == len(paths):
            emit(); batch = []; batch_topics = []
    expected = {'lessons': 2964, 'tutorials': 6016, 'examples': 9636, 'knowledge_points': 9636,
                'questions': 19646, 'fields': 22840, 'steps': 15652, 'key_prerequisites': 9167}
    for key, count in expected.items():
        assert totals[key] == count, (key, totals[key], count)
    manifest = {'source': ':org/Math-Academy', 'lessons_root': str(args.lessons_root.resolve()),
                'renderer': str(MD_SCRIPT), 'image_map': str(math_root / 'images/math-academy-map.json'),
                'totals': dict(totals), 'rendered_unique_images': len(used_images),
                'duplicate_question_ids': sorted(duplicate_questions),
                'duplicate_content_ids': sorted([list(key) for key in duplicate_contents]), 'batches': batches}
    (output / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print('Ready: ' + json.dumps(dict(totals)), flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--lessons-root', type=Path, default=Path('/home/jake/Developer/MA/DATA/Lessons'))
    parser.add_argument('--math-root', type=Path, default=Path('/media/jake/SSD/EDB/math'))
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--chunk-topics', type=int, default=75)
    args = parser.parse_args()
    assert args.chunk_topics > 0
    generate(args)


if __name__ == '__main__':
    main()
