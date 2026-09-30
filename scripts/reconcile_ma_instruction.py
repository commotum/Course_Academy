#!/usr/bin/env python3
"""Propose conservative, step-level MA tutorial/example text repairs.

Reads captured lessons and vault copies, but writes only staged EDN and a JSON
audit trail. The imported entity UUIDs are exactly those of the seed generator.
"""

import argparse
import collections
import csv
import difflib
import hashlib
import json
import re
import uuid
from pathlib import Path


DATA = Path('/home/jake/Developer/MA/DATA/Lessons')
VAULT = Path('/home/jake/Developer/study/vault')
ORDER = ('MF1', 'MF2', 'MF3', 'LAL', 'MVC', 'DEQ', 'CA1', 'CA2')
HEADING = re.compile(r'^## (.+)$', re.M)
QUIZ = re.compile(r'```quiz\b|\*\*Question\s+\d+', re.I)
BAD_MATH = re.compile(r'∑_|∫_|lim_\(|√\(|[_^]\([^)]*[→∞][^)]*\)')
IMAGE = re.compile(r'(!\[[^\]]*\]\()(<[^>]+>|[^)]+)(\))')


def ident(kind, source):
    return uuid.uuid5(uuid.NAMESPACE_URL, f'course-academy:ma:{kind}:{source}')


def json_string(value):
    return json.dumps(value, ensure_ascii=False)


def cleaned(text):
    return re.sub(r'\s+', ' ', IMAGE.sub(lambda m: m[1] + Path(m[2].strip('<>')).name + m[3], text)).strip()


def malformed(text):
    return len(BAD_MATH.findall(text))


def source_markdown(json_path):
    if json_path.is_relative_to(DATA):
        return DATA / json_path.stem / f'{json_path.stem}.md'
    section = json_path.parent.parent.parent
    name = json_path.parent.name
    for folder in ('Lessons', 'Prerequisites'):
        path = section / folder / (name + '.md')
        if path.exists():
            return path
    return None


def step_bodies(markdown, steps):
    """Match ordered source step headings, allowing unrelated headings in a copy."""
    heads = list(HEADING.finditer(markdown))
    pos = -1
    matches = []
    for step in steps:
        title = step['title'].strip()
        found = next((i for i in range(pos + 1, len(heads)) if heads[i][1].strip() == title), None)
        if found is None:
            return None
        matches.append(found)
        pos = found
    result = []
    for index, current in enumerate(matches):
        start = heads[current].end()
        # End at the next heading, not the next matched step: a new heading
        # within a step should never be silently included as lesson prose.
        end = heads[current + 1].start() if current + 1 < len(heads) else len(markdown)
        body = markdown[start:end].split('\n---\n', 1)[0].strip()
        body = re.sub(r'^<a\s+id="[^"]+"></a>\s*', '', body).strip()
        result.append(body)
    return result


def resolve_images(value, md_path, topic):
    """Prefer canonical DATA images; accept only existing local alternatives."""
    missing = []
    canonical = DATA / topic / 'Source' / 'Images'

    def replace(match):
        raw = match[2].strip('<>')
        # Image links may carry an Obsidian size suffix.
        raw_path = raw.split('|', 1)[0]
        name = Path(raw_path).name
        data_file = canonical / name
        local = Path(raw_path)
        if not local.is_absolute():
            local = (md_path.parent / local).resolve()
        if (not local.exists() or not local.is_file()) and data_file.exists():
            # Vault copies frequently omit their Images directory. The
            # captured DATA asset is a real, canonical target for that name.
            chosen = data_file
        elif not local.exists() or not local.is_file():
            missing.append(raw)
            return match[0]
        elif data_file.exists() and hashlib.sha256(local.read_bytes()).digest() == hashlib.sha256(data_file.read_bytes()).digest():
            chosen = data_file
        else:
            chosen = local
        return match[1] + str(chosen) + match[3]

    return IMAGE.sub(replace, value), missing


def extract(md_path, data, topic):
    steps = [item for item in data['lesson']['items'] if item['item_type'] == 'step']
    markdown = md_path.read_text(encoding='utf-8')
    bodies = step_bodies(markdown, steps)
    if bodies is None:
        return None, 'step headings do not match JSON order'
    components = {}
    for step, body in zip(steps, bodies):
        sid = step['step_id']
        if QUIZ.search(body):
            # A quiz before the separator means the section cannot be parsed
            # safely as instruction.
            return None, f'quiz text in step {sid}'
        if step['step_type'] == 'tutorial':
            parts = {'content': body}
        else:
            match = re.match(r'\*\*Example:\*\*\s*(.*?)\n\s*\*\*Explanation\*\*\s*(.*)', body, re.S)
            if not match:
                return None, f'example labels absent in step {sid}'
            parts = {'problem': match[1].strip(), 'explanation': match[2].strip()}
        for field, value in parts.items():
            value, missing = resolve_images(value, md_path, topic)
            if not value or missing:
                return None, f'empty text or missing images in step {sid}/{field}: {missing}'
            components[(sid, field)] = value
    return components, None


def candidates_index():
    out = collections.defaultdict(list)
    for root in (VAULT / 'MA', VAULT / 'SU26'):
        for path in root.rglob('Source/*/[0-9]*.json'):
            out[path.stem].append(path)
    return out


def compatible(base, other):
    a, b = cleaned(base), cleaned(other)
    if a == b:
        return True, 1.0
    ratio = difflib.SequenceMatcher(None, a, b, autojunk=False).ratio()
    # Added detail is acceptable, but removal of existing instruction is not.
    minimum = max(0.86, 1 - 0.03 * malformed(base))
    return ratio >= minimum and len(b) >= len(a) * 0.97, ratio


def meaning_preserved(base, other):
    """Defer edits that change prose, numerical values, or math variables."""
    def prose(value):
        return cleaned(re.sub(r'\$\$.*?\$\$|\$.*?\$', '<math>', value, flags=re.S))

    def numbers(value):
        return collections.Counter(re.findall(r'\d+(?:\.\d+)?', value))

    def variables(value):
        without_commands = re.sub(r'\\[a-zA-Z]+', ' ', value)
        return collections.Counter(re.findall(r'(?<![A-Za-z])[A-Za-z](?![A-Za-z])', without_commands))

    def image_hashes(value):
        paths = [Path(match[2].strip('<>')) for match in IMAGE.finditer(value)]
        if any(not path.is_file() for path in paths):
            return None
        return [hashlib.sha256(path.read_bytes()).hexdigest() for path in paths]

    return (prose(base) == prose(other)
            and numbers(base) == numbers(other)
            and variables(base) == variables(other)
            and image_hashes(base) == image_hashes(other))


def choose(base, copies):
    """Only migrate a clear math-markup repair that remains close to DATA."""
    before = malformed(base)
    if before == 0:
        differing = [{'source': str(path), 'reason': 'text differs without a detected DATA markup defect'}
                     for path, value in copies if cleaned(value) != cleaned(base)]
        return None, 'no detected malformed math in DATA', differing
    viable = []
    differing = []
    for path, value in copies:
        good, similarity = compatible(base, value)
        after = malformed(value)
        if good and after < before and meaning_preserved(base, value):
            viable.append((after, -similarity, path, value))
        elif cleaned(value) != cleaned(base):
            differing.append({'source': str(path), 'reason': 'unclear, incomplete, or semantically unverified change', 'similarity': round(similarity, 4), 'malformed': after})
    if not viable:
        return None, 'no close candidate with repaired math', differing
    viable.sort(key=lambda item: (item[0], item[1], str(item[2])))
    best = viable[0]
    # Independent copies may disagree about the substantive replacement.
    peers = [x for x in viable if x[0] == best[0] and abs(x[1] - best[1]) < 0.01]
    if any(cleaned(x[3]) != cleaned(best[3]) for x in peers):
        differing.extend({'source': str(x[2]), 'reason': 'competing repaired text'} for x in peers)
        return None, 'competing high-quality repairs', differing
    return best, None, differing


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--scope', type=Path, default=Path('.local/edb/reconciliation/scope.json'))
    parser.add_argument('--output', type=Path, default=Path('.local/edb/reconciliation/instruction'))
    parser.add_argument('--courses', nargs='+', choices=ORDER, default=ORDER)
    parser.add_argument('--batch-size', type=int, default=100)
    args = parser.parse_args()
    scope = json.loads(args.scope.read_text())
    selected = set(args.courses)
    scope_by_course = {course: scope['topics_by_first_course'][course] for course in ORDER if course in selected}
    all_topics = {topic for topics in scope_by_course.values() for topic in topics}
    index = candidates_index()

    content_counts = collections.Counter()
    for path in DATA.glob('*/Source/*.json'):
        source = json.loads(path.read_text())
        content_counts.update((i['step_type'], i['content_id']) for i in source['lesson']['items'] if i['item_type'] == 'step')
    collisions = {key for key, count in content_counts.items() if count > 1}
    assert len(collisions) == 4, collisions

    output = args.output
    output.mkdir(parents=True, exist_ok=True)
    for old in output.glob('*.edn'):
        old.unlink()
    report = {'courses': list(scope_by_course), 'scope_topics': len(all_topics), 'content_id_collisions': sorted([list(x) for x in collisions]), 'selected': [], 'unresolved': [], 'source_errors': [], 'counts': {}}
    by_course = collections.defaultdict(list)
    pilot = collections.defaultdict(list)
    counts = collections.Counter()
    for course, topics in scope_by_course.items():
        for topic in topics:
            source_path = DATA / topic / 'Source' / f'{topic}.json'
            md_path = DATA / topic / f'{topic}.md'
            if not source_path.exists() or not md_path.exists():
                report['source_errors'].append({'topic': topic, 'reason': 'DATA lesson absent'})
                continue
            data = json.loads(source_path.read_text())
            base, error = extract(md_path, data, topic)
            if error:
                report['source_errors'].append({'topic': topic, 'source': str(md_path), 'reason': error})
                continue
            steps = [i for i in data['lesson']['items'] if i['item_type'] == 'step']
            copies = collections.defaultdict(list)
            for json_path in index[topic]:
                vault_md = source_markdown(json_path)
                if vault_md is None:
                    report['source_errors'].append({'topic': topic, 'source': str(json_path), 'reason': 'Markdown absent'})
                    continue
                try:
                    vault_data = json.loads(json_path.read_text())
                    vault_steps = [i for i in vault_data['lesson']['items'] if i['item_type'] == 'step']
                    # Match source JSON to captured step IDs and content IDs,
                    # not merely equal headings or the topic number.
                    anchors = [(x['step_id'], x['step_type'], x['content_id'], x['title']) for x in steps]
                    others = [(x['step_id'], x['step_type'], x['content_id'], x['title']) for x in vault_steps]
                    if anchors != others:
                        raise ValueError('JSON step identity differs from DATA')
                    values, error = extract(vault_md, vault_data, topic)
                    if error:
                        raise ValueError(error)
                    for key, value in values.items():
                        copies[key].append((vault_md, value))
                except (ValueError, KeyError, OSError) as exc:
                    report['source_errors'].append({'topic': topic, 'source': str(json_path), 'reason': str(exc)})
            for step in steps:
                sid, cid, kind = step['step_id'], step['content_id'], step['step_type']
                key = sid if (kind, cid) in collisions else cid
                fields = ('content',) if kind == 'tutorial' else ('problem', 'explanation')
                for field in fields:
                    value = base[(sid, field)]
                    result, reason, differences = choose(value, copies[(sid, field)])
                    counts['components_reviewed'] += 1
                    if result is None:
                        if differences or malformed(value):
                            report['unresolved'].append({'topic': topic, 'course': course, 'step_id': sid, 'content_id': cid, 'component': f'{kind}/{field}', 'reason': reason, 'data_malformed': malformed(value), 'differences': differences[:12]})
                        continue
                    after, neg_similarity, path, replacement = result
                    uid = ident(kind, key)
                    entity = 'question' if kind == 'example' else 'tutorial'
                    attribute = ('worked-solution' if field == 'explanation' else field)
                    form = (f'{{:db/id [:{entity}/id #uuid "{uid}"] '
                            f':{entity}/{attribute} {json_string(replacement)} '
                            f':db/ensure :{entity}/validate}}')
                    by_course[course].append(form)
                    if topic in ('1176', '1263'):
                        pilot[topic].append(form)
                    counts[f'{kind}/{field}'] += 1
                    report['selected'].append({'topic': topic, 'course': course, 'step_id': sid, 'content_id': cid, 'entity_id': str(uid), 'component': f'{kind}/{field}', 'source': str(path), 'data_malformed': malformed(value), 'selected_malformed': after, 'similarity': round(-neg_similarity, 4), 'other_differences': differences[:12]})
    batch_files = []
    for course in scope_by_course:
        forms = by_course[course]
        for index, start in enumerate(range(0, len(forms), args.batch_size), 1):
            name = f'{course}-{index:04}.edn'
            (output / name).write_text('[\n ' + '\n '.join(forms[start:start + args.batch_size]) + '\n]\n')
            batch_files.append(name)
    for topic, forms in pilot.items():
        (output / f'pilot-{topic}.edn').write_text('[\n ' + '\n '.join(forms) + '\n]\n')
    all_pilot = [form for course in scope_by_course for form in by_course[course]
                 if form in {pilot_form for topic_forms in pilot.values() for pilot_form in topic_forms}]
    (output / 'pilot.edn').write_text('[\n ' + '\n '.join(all_pilot) + '\n]\n')
    report['counts'] = dict(sorted(counts.items()))
    report['course_update_counts'] = {course: len(by_course[course]) for course in scope_by_course}
    report['apply_batches_in_order'] = batch_files
    report['pilot_preview_only'] = ['pilot.edn'] + [f'pilot-{topic}.edn' for topic in pilot]
    (output / 'report.json').write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps({'counts': report['counts'], 'courses': report['course_update_counts'], 'unresolved': len(report['unresolved']), 'source_errors': len(report['source_errors']), 'output': str(output)}, indent=2))


if __name__ == '__main__':
    main()
