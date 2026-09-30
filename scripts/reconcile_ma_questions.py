#!/usr/bin/env python3
"""Stage conservative, source-backed MA question corrections for EDB."""

import argparse
import collections
import csv
import hashlib
import json
import re
import sys
import uuid
from pathlib import Path

import yaml

from generate_ma_lesson_seed import ident, question_blocks, question_parts, answer_value, readable_value

DATA = Path('/home/jake/Developer/MA/DATA/Lessons')
CATALOG = Path('/home/jake/Developer/MA/DATA/Catalog.csv')
VAULTS = [Path('/home/jake/Developer/study/vault/MA'), Path('/home/jake/Developer/study/vault/SU26')]
OUT = Path('.local/edb/reconciliation/questions')
MIGRATION_DUPLICATES = Path('.local/edb/content-migration/fresh-plan/duplicate-answer-values.json')
COURSES = ('MF1', 'MF2', 'MF3', 'LAL', 'MVC', 'DEQ', 'CA1', 'CA2')
PILOT = {'1176', '1263'}
QUIZ = re.compile(r'```quiz\s*\n(.*?)\n```', re.S)
BLANK = re.compile(r'==([^=\n]+)==')
UNDERLINE = re.compile(r'\$\s*\\underline\{\\hspace\{[^}]*\}\}\s*\$')
IMG = re.compile(r'!\[[^]]*\]\(([^)]+)\)')


def quote(s):
    return json.dumps(s, ensure_ascii=False)


def uid(kind, qkey):
    return f'#uuid "{ident(kind, qkey)}"'


def brace_fraction(s):
    # Only explicit braced fractions are rewritten; no algebra is inferred.
    p = re.compile(r'\\(?:dfrac|tfrac|frac)\{([^{}]+)\}\{([^{}]+)\}')
    while True:
        n = p.sub(lambda m: f'({m[1]})/({m[2]})', s)
        if n == s:
            return s
        s = n


def norm(s, source=None):
    if not isinstance(s, str):
        return ''
    s = s.strip().replace('\u2212', '-').replace('−', '-').replace('\\,', '')
    s = re.sub(r'\[MATH:\s*(.*?)\]', r'\1', s, flags=re.S)
    s = re.sub(r'\$+', '', s)
    s = re.sub(r'\\(?:displaystyle|textstyle|left|right|limits)\b', '', s)
    s = s.replace('\\infty', '∞').replace('\\pi', 'π').replace('\\cdot', '⋅')
    s = brace_fraction(s)
    s = re.sub(r'\\sum_\{([^{}]+)\}\^\{([^{}]+)\}', r'∑_(\1)^(\2)', s)
    s = re.sub(r'\\sum\s*_\s*\(([^)]*)\)\s*\^\s*\(([^)]*)\)', r'∑_(\1)^(\2)', s)
    s = re.sub(r'\\lim_\{([^{}]+)\}', r'lim_(\1)', s)
    s = re.sub(r'\\(?:to|rightarrow)', '→', s)
    s = re.sub(r'\\(?:,|;|!|\s)', '', s)
    s = re.sub(r'\s+', '', s)
    s = re.sub(r'\{([A-Za-z0-9])\}', r'\1', s)
    return s


def clean_option(s):
    return re.sub(r'\n\s*---\s*\n\s*<a\s+id=[^>]+></a>\s*$', '', s).strip()


def image_sig(s, base):
    refs = IMG.findall(s)
    if not refs:
        return ()
    signatures = []
    for ref in refs:
        path = Path(ref.strip('<>'))
        if not path.is_absolute():
            path = base.parent / path
        if not path.is_file():
            return None
        signatures.append(hashlib.sha256(path.read_bytes()).hexdigest())
    return tuple(signatures)


def value_sig(s, base):
    s = clean_option(s)
    im = image_sig(s, base)
    return None if im is None else (norm(IMG.sub('[image]', s)), im)


def source_paths(topic):
    paths = set()
    for vault in VAULTS:
        for p in vault.rglob(f'{topic}.json'):
            if p.parent.parent.name != 'Source':
                continue
            for section in ('Lessons', 'Prerequisites'):
                md = p.parent.parent.parent / section / (p.parent.name + '.md')
                if md.is_file():
                    paths.add(md)
    return sorted(paths)


def source_index():
    index = collections.defaultdict(set)
    for vault in VAULTS:
        for p in vault.rglob('*.json'):
            if p.parent.parent.name != 'Source' or not p.stem.isdigit():
                continue
            for section in ('Lessons', 'Prerequisites'):
                md = p.parent.parent.parent / section / (p.parent.name + '.md')
                if md.is_file():
                    index[p.stem].add(md)
    return {k: sorted(v) for k, v in index.items()}


def quizzes(path):
    result = []
    raw = path.read_text(encoding='utf-8')
    for m in QUIZ.finditer(raw):
        try:
            q = yaml.load(m[1], Loader=getattr(yaml, 'CSafeLoader', yaml.SafeLoader))
            if isinstance(q, dict) and q.get('type') in ('radio', 'blank', 'select'):
                q['_line'] = raw.count('\n', 0, m.start()) + 1
                result.append(q)
        except yaml.YAMLError:
            pass
    return result


def source_record(q, block, topic, duplicates):
    qid = q['question_id']
    qkey = f'{topic}:{qid}' if qid in duplicates else qid
    prompt, md_opts = question_parts(block, q, topic)
    if q['question_format'] == 'multiple-choice':
        opts = [answer_value(c, md_opts[i] if md_opts else None, topic) for i, c in enumerate(q['choices'])]
    elif q['question_format'] == 'select-list':
        opts = [[readable_value(o['readable_text'], topic) for o in sl['options']] for sl in q['select_lists']]
    else:
        opts = []
    return dict(topic=topic, id=qid, key=qkey, format=q['question_format'], prompt=prompt, options=opts,
                fields=1 if q['question_format'] == 'multiple-choice' else len(q['free_entry_blanks'] or q['select_lists']))


def match_radio(quiz, rec, path):
    if rec['format'] != 'multiple-choice' or quiz.get('type') != 'radio':
        return None
    opts = quiz.get('options') or []
    if len(opts) != len(rec['options']) or not opts:
        return None
    source_sigs = [value_sig(f'${v}$' if t == 'math' else f'![](<{v}>)' if t == 'image' else v,
                             DATA / rec['topic'] / f'{rec["topic"]}.md') for t, v in rec['options']]
    quiz_sigs = [value_sig(str(o.get('content', '')), path) for o in opts]
    if None in source_sigs or None in quiz_sigs or collections.Counter(source_sigs) != collections.Counter(quiz_sigs):
        return None
    quiz_prompt = IMG.sub('[image]', quiz.get('content', ''))
    source_prompt = IMG.sub('[image]', rec['prompt'])
    qimage = image_sig(quiz.get('content', ''), path)
    simage = image_sig(rec['prompt'], DATA / rec['topic'] / f'{rec["topic"]}.md')
    if qimage is None or simage is None or norm(quiz_prompt) != norm(source_prompt) or qimage != simage:
        return None
    correct = [o for o in opts if o.get('correct') is True]
    if len(correct) != 1:
        return {'problem': 'nonunique-key'}
    chosen = value_sig(correct[0].get('content', ''), path)
    positions = [i for i, sig in enumerate(source_sigs, 1) if sig == chosen]
    if len(positions) != 1:
        return {'problem': 'ambiguous-choice'}
    return {'choice': positions[0], 'prompt': quiz['content'].strip(),
            'option_updates': {str(source_sigs.index(sig) + 1): str(o.get('content', '')).strip()
                               for sig, o in zip(quiz_sigs, opts)}}


def match_blank(quiz, rec, path):
    if rec['format'] != 'free-response' or quiz.get('type') != 'blank':
        return None
    prompt = quiz.get('content', '')
    answers = BLANK.findall(prompt)
    if len(answers) != rec['fields'] or not answers or any(not x.strip() for x in answers):
        return None
    # Reconcile the actual question stem after erasing only response locations.
    stripped = BLANK.sub(lambda _: '{{field-' + str(len(BLANK.findall(prompt[:_.start()])) + 1) + '}}', prompt)
    stripped = re.sub(r'\bAnswer:\s*', '', stripped)
    source = clean_option(rec['prompt'])
    left, right = norm(stripped), norm(source)
    if left.endswith('{{field-' + str(rec['fields']) + '}}.') and right.endswith('{{field-' + str(rec['fields']) + '}}'):
        left = left[:-1]
    if left != right or image_sig(stripped, path) is None or image_sig(source, DATA / rec['topic'] / f'{rec["topic"]}.md') is None or image_sig(stripped, path) != image_sig(source, DATA / rec['topic'] / f'{rec["topic"]}.md'):
        return None
    return {'answers': [a.strip() for a in answers], 'prompt': stripped.strip()}


def match_select(quiz, rec, path):
    if rec['format'] != 'select-list' or quiz.get('type') != 'select':
        return None
    if rec['fields'] != 1:
        return None
    # A select quiz may represent one of several fields; exact option values and
    # field location are required before a key can be transferred.
    opts = quiz.get('options') or []
    sigs = [value_sig(str(o.get('content', '')), path) for o in opts]
    if None in sigs or not sigs:
        return None
    matches = []
    for fi, field in enumerate(rec['options'], 1):
        expected = [value_sig(f'${v}$' if t == 'math' else f'![](<{v}>)' if t == 'image' else v,
                              DATA / rec['topic'] / f'{rec["topic"]}.md') for t, v in field]
        if None not in expected and collections.Counter(sigs) == collections.Counter(expected):
            matches.append((fi, expected))
    if len(matches) != 1:
        return None
    fi, expected = matches[0]
    keys = [x.get('correct_option') for x in quiz.get('questions', []) if isinstance(x, dict)]
    if len(keys) != 1:
        return {'problem': 'select-key-structure'}
    chosen = [o for o in opts if o.get('id') == keys[0]]
    if len(chosen) != 1:
        return {'problem': 'missing-select-choice'}
    index = [i for i, sig in enumerate(expected, 1) if sig == value_sig(str(chosen[0].get('content', '')), path)]
    if len(index) != 1:
        return {'problem': 'ambiguous-select-choice'}
    # Require the copied stem to contain the same non-placeholder text.
    if norm(UNDERLINE.sub('{{field-1}}', quiz.get('content', ''))) != norm(rec['prompt']):
        return None
    return {'field': fi, 'choice': index[0]}


def topic_records(topic, duplicates):
    source = DATA / topic / 'Source' / f'{topic}.json'
    md = DATA / topic / f'{topic}.md'
    if not source.is_file() or not md.is_file():
        return []
    data = json.loads(source.read_text())
    qs = [q for q in data['lesson']['items'] if q['item_type'] == 'question']
    return [source_record(q, block, topic, duplicates) for q, block in zip(qs, question_blocks(md.read_text(), qs))]


def choose(occurrences):
    if not occurrences:
        return None, 'unmatched'
    groups = collections.defaultdict(list)
    for o in occurrences:
        m = o['match']
        signature = (m.get('choice'), m.get('field'), tuple(m.get('answers', [])))
        groups[signature].append(o)
    if len(groups) != 1:
        return None, 'conflicting-keys'
    return min(occurrences, key=lambda o: (0 if '/MA/' in o['path'] else 1, len(o['path']), o['path'])), None


def seeded_choice_index(rec, field, index):
    """Resolve a choice to its surviving UUID in the migrated or fresh seed."""
    if MIGRATION_DUPLICATES.is_file():
        if not hasattr(seeded_choice_index, '_uuid_remap'):
            seeded_choice_index._uuid_remap = json.loads(MIGRATION_DUPLICATES.read_text())['uuid_remap']
        source_uuid = str(ident('answer', f'{rec["key"]}:{field}:{index}'))
        target_uuid = seeded_choice_index._uuid_remap.get(source_uuid, source_uuid)
        options = rec['options'] if rec['format'] == 'multiple-choice' else rec['options'][field - 1]
        matches = [position for position in range(1, len(options) + 1)
                   if str(ident('answer', f'{rec["key"]}:{field}:{position}')) == target_uuid]
        assert len(matches) == 1, (rec['key'], field, index, target_uuid)
        return matches[0]
    options = rec['options'] if rec['format'] == 'multiple-choice' else rec['options'][field - 1]
    value = options[index - 1]
    return next(position for position, candidate in enumerate(options, 1) if candidate == value)


def forms(rec, chosen):
    m = chosen['match']; key = rec['key']; output = []
    qref = f'[:question/id {uid("question", key)}]'
    # Every map changes one entity attribute. Existing UUIDs are lookup refs.
    if 'choice' in m:
        fi = m.get('field', 1)
        fref = f'[:answer-field/id {uid("field", f"{key}:{fi}")}]'
        choice = seeded_choice_index(rec, fi, m['choice'])
        aref = f'[:answer/id {uid("answer", f"{key}:{fi}:{choice}")}]'
        output.append(f'{{:db/id {fref} :answer-field/correct {aref}}}')
        output.append(f'{{:db/id {aref} :db/ensure :answer/validate}}')
        output.append(f'{{:db/id {fref} :db/ensure :answer-field/validate}}')
        if 'option_updates' in m and len(m['option_updates']) == len(rec['options']):
            for ci, candidate in m['option_updates'].items():
                ci = int(ci)
                if seeded_choice_index(rec, fi, ci) != ci:
                    continue
                old_type, old_value = rec['options'][ci - 1]
                if IMG.search(candidate):
                    continue  # asset signatures were checked; retain the canonical absolute asset path
                new_type, new_value = ('math', candidate[1:-1].strip()) if re.fullmatch(r'\$[^$]+\$', candidate, re.S) else ('text', candidate)
                choice_ref = f'[:answer/id {uid("answer", f"{key}:{fi}:{ci}")}]'
                if old_type != new_type:
                    output.append(f'{{:db/id {choice_ref} :answer/type :answer.type/{new_type}}}')
                if old_value != new_value:
                    output.append(f'{{:db/id {choice_ref} :answer/value {quote(new_value)}}}')
                if old_type != new_type or old_value != new_value:
                    output.append(f'{{:db/id {choice_ref} :db/ensure :answer/validate}}')
    elif 'answers' in m:
        for fi, answer in enumerate(m['answers'], 1):
            fref = f'[:answer-field/id {uid("field", f"{key}:{fi}")}]'
            aid = uid('answer', f'{key}:{fi}:expected')
            tempid = f'expected-answer-{key}-{fi}'
            if answer.startswith('$') and answer.endswith('$'):
                kind, value = 'math', answer[1:-1]
            elif re.fullmatch(r'[0-9A-Za-z_+\-*/^().| {}]+', answer) and (re.search(r'[0-9]|[+\-*/^|]', answer)):
                kind, value = 'math', re.sub(r'(?<![A-Za-z\\])pi(?![A-Za-z])', r'\\pi', answer)
                value = re.sub(r'(?<![A-Za-z\\])ln(?![A-Za-z])', r'\\ln', value)
                value = re.sub(r'(?<![A-Za-z\\])log(?![A-Za-z])', r'\\log', value)
                value = re.sub(r'(?<![A-Za-z\\])sqrt\(([^()]+)\)', r'\\sqrt{\1}', value)
                value = re.sub(r'\^\(([^()]*)\)', r'^{\1}', value)
                value = re.sub(r'^(\d+)\s+(\d+)/(\d+)$',
                               lambda m: '\\frac{' + str(int(m[1])*int(m[3])+int(m[2])) + '}{' + m[3] + '}', value)
            else:
                kind, value = 'text', answer
            output.append(f'{{:db/id {quote(tempid)} :answer/id {aid} :answer/type :answer.type/{kind} :answer/value {quote(value)} :db/ensure :answer/validate}}')
            output.append(f'{{:db/id {fref} :answer-field/choices [{quote(tempid)}]}}')
            output.append(f'{{:db/id {fref} :answer-field/correct {quote(tempid)}}}')
            output.append(f'{{:db/id {fref} :db/ensure :answer-field/validate}}')
    if m.get('prompt') and m['prompt'] != rec['prompt'] and '{{field-' not in m['prompt'] and not IMG.search(m['prompt']):
        output.append(f'{{:db/id {qref} :question/problem {quote(m["prompt"])}}}')
    output.append(f'{{:db/id {qref} :db/ensure :question/validate}}')
    return output


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--courses', nargs='+', default=list(COURSES))
    ap.add_argument('--batch-size', type=int, default=250)
    args = ap.parse_args()
    selected = tuple(args.courses)
    by_course = collections.defaultdict(list)
    with CATALOG.open(newline='') as f:
        for row in csv.DictReader(f):
            code = row['topic-code'].split('.', 1)[0]
            if code in selected and (DATA / row['topic-id'] / 'Source' / f'{row["topic-id"]}.json').is_file():
                by_course[code].append(row['topic-id'])
    order = []; seen = set()
    for code in selected:
        for topic in by_course[code]:
            if topic not in seen:
                order.append((code, topic)); seen.add(topic)
    # Preview pilots separately; scoped pilot topics also enter their course batches.
    for topic in sorted(PILOT):
        if topic not in seen:
            order.append(('pilot', topic)); seen.add(topic)
    duplicate_ids = {'56649', '156726'}  # established by lesson seed CSV inventory
    manifest = {'courses': list(selected), 'topics': len(order), 'counts': collections.Counter(), 'keyed': [], 'unresolved': []}
    pilot = []; batches = collections.defaultdict(list)
    index = source_index()
    for code, topic in order:
        records = topic_records(topic, duplicate_ids)
        if not records:
            continue
        paths = index.get(topic, [])
        candidates = [(path, q) for path in paths for q in quizzes(path)]
        for rec in records:
            matches = []
            for path, q in candidates:
                match = (match_radio(q, rec, path) or match_blank(q, rec, path) or match_select(q, rec, path))
                if match and 'problem' not in match:
                    matches.append({'path': str(path), 'line': q['_line'], 'quiz_id': q.get('id'), 'match': match})
            chosen, issue = choose(matches)
            if issue:
                manifest['unresolved'].append({'topic': topic, 'question': rec['id'], 'reason': issue,
                     'source': str(DATA / topic / 'Source' / f'{topic}.json'),
                     'candidate_files': [str(p) for p in paths]})
                manifest['counts'][issue] += 1
                continue
            ent = {'topic': topic, 'course': code, 'question': rec['id'], 'format': rec['format'],
                   'selected': {'path': chosen['path'], 'line': chosen['line'], 'quiz_id': chosen['quiz_id']},
                   'all_matching_sources': [{'path': o['path'], 'line': o['line'], 'quiz_id': o['quiz_id']} for o in matches],
                   'key': chosen['match'].get('choice', chosen['match'].get('answers')),
                   'math_verified': topic in PILOT}
            manifest['keyed'].append(ent)
            manifest['counts']['keyed_questions'] += 1
            manifest['counts']['keyed_fields'] += len(chosen['match'].get('answers', [])) or 1
            if 'answers' in chosen['match']:
                manifest['counts']['new_blank_answers'] += len(chosen['match']['answers'])
            statements = forms(rec, chosen)
            if any(':question/problem ' in x for x in statements):
                manifest['counts']['text_repairs'] += 1
            if topic in PILOT:
                pilot.extend(statements)
            if code in selected:
                batches[code].append(statements)
    OUT.mkdir(parents=True, exist_ok=True)
    for stale in OUT.glob('bulk-*.edn'):
        stale.unlink()
    (OUT / 'pilot.edn').write_text('[\n' + '\n'.join(pilot) + '\n]\n')
    files = []
    for course in selected:
        groups = batches[course]
        chunks = []; current = []
        for group in groups:
            if current and len(current) + len(group) > args.batch_size:
                chunks.append(current); current = []
            current.extend(group)
        if current:
            chunks.append(current)
        for index, statements in enumerate(chunks, 1):
            name = f'bulk-{selected.index(course)+1:02d}-{course}-{index:04d}.edn'
            (OUT / name).write_text('[\n' + '\n'.join(statements) + '\n]\n')
            files.append(name)
    manifest['counts'] = dict(manifest['counts']); manifest['pilot_file'] = 'pilot.edn'; manifest['bulk_files'] = files
    (OUT / 'manifest.json').write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps({'topics': len(order), 'pilot_statements': len(pilot), 'bulk_files': len(files), 'counts': manifest['counts']}))


if __name__ == '__main__':
    main()
