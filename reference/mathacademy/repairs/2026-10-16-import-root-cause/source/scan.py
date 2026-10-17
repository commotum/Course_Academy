"""Read-only, source-backed inventory of deterministic historical math loss.

No EDB writes and no edits to the original MA corpus. Counts describe source
occurrences; current database damage must be established by a separate join.
"""
from __future__ import annotations
import argparse
import bisect
from collections import Counter, defaultdict
import hashlib
import html
import importlib.util
import json
from pathlib import Path
import re
import sys
import time

from bs4 import BeautifulSoup

HERE = Path(__file__).resolve().parent
MA = Path('/home/jake/Developer/MA')
LEGACY = MA / 'PIPELINE/Math-Academy/3-Capture/1-Source/3-JSON/lesson-json.py'
MARKDOWN = MA / 'PIPELINE/Math-Academy/3-Capture/1-Source/5-MD/md.py'
TITLE = re.compile(r'<title\b[^>]*>([\s\S]*?)</title>')
MML = re.compile(r'<math\b[^>]*>[\s\S]*?</math>')
CONTAINER = re.compile(r'<mjx-container\b[\s\S]*?</mjx-container>')
MATH_SPAN = re.compile(r'<span\b[^>]*class="math"[^>]*>([\s\S]*?)</span>')
SPECIAL = re.compile(r'<(?:mtable|mfrac|mover|munder|munderover|mphantom|menclose|mpadded)\b|%')


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    obj = importlib.util.module_from_spec(spec)
    sys.modules[name] = obj
    spec.loader.exec_module(obj)
    return obj


legacy = module('forensic_legacy_lesson_json', LEGACY)
md = module('forensic_legacy_markdown', MARKDOWN)


def digest(value):
    return hashlib.sha256(value if isinstance(value, bytes) else value.encode()).hexdigest()


def compact(value):
    return re.sub(r'\s+', ' ', value).strip()


def title_info(content):
    containers = CONTAINER.findall(content)
    # Visible/assistive duplicates inside one rendered container are one
    # semantic fragment, not separate operands.
    fragments = [match[0] for container in containers if (match := MML.search(container))]
    if not containers:
        fragments = MML.findall(content)
    outer = CONTAINER.sub('FORMULA', content)
    visible_outer = BeautifulSoup(outer, 'html.parser').get_text('', strip=False) if '<' in outer else html.unescape(outer)
    semantic_outer = re.sub(r'\\require\s*\{[^{}]*\}', '', visible_outer)
    semantic_outer = re.sub(r'\\(?:displaystyle|textstyle|scriptstyle|scriptscriptstyle|quad|qquad|enspace)\b|\\[,!;:]', '', semantic_outer)
    residual = re.sub(r'FORMULA|[{}\s,.;:?!]', '', semantic_outer)
    mixed_loss = bool(fragments and (residual or len(fragments) > 1))
    comments = re.findall(r'(?m)^\s*%[^\r\n]*', visible_outer)
    return fragments, outer, mixed_loss, comments


def owner_end(raw, position):
    """Bound known JSON owner IDs to their actual div, not the page footer."""
    start = raw.rfind('<', 0, position)
    if not re.match(r'<div\b', raw[start:start + 20]):
        return None
    depth = 0
    for match in re.finditer(r'<!--[\s\S]*?-->|<script\b[^>]*>[\s\S]*?</script>|</?div\b[^>]*>', raw[start:], re.I):
        tag = match[0]
        if tag.startswith(('<!--', '<script', '<SCRIPT')):
            continue
        depth += -1 if tag.startswith('</') else 1
        if depth == 0:
            return start + match.end()
    return None


def item_fields(item):
    """Original JSON field identities, without inferring mathematical content."""
    if item.get('step_type') in ('tutorial', 'example'):
        for index, section in enumerate(item.get('sections', [])):
            attr = ':tutorial/content' if item['step_type'] == 'tutorial' else (
                ':question/problem' if section.get('section_type') == 'example_question'
                else ':question/worked-solution')
            yield attr, f'sections/{index}', section
    else:
        for key in ('prompt', 'body', 'graphic', 'calculator_instructions'):
            yield ':question/problem', key, item.get(key, {})
        for index, choice in enumerate(item.get('choices', [])):
            yield ':answer/value', f'choices/{index}', choice


def field_math(item):
    found = defaultdict(list)
    for attr, key, field in item_fields(item):
        for index, match in enumerate(MATH_SPAN.finditer(field.get('normalized_html', ''))):
            value = html.unescape(match[1])
            if value.startswith('[MATH:') and value.endswith(']'):
                found[compact(value[6:-1])].append({'attribute': attr, 'json_field': key, 'math_index': index})
        for select in field.get('select_lists', []):
            for option_index, option in enumerate(select.get('options', [])):
                for match in MATH_SPAN.finditer(option.get('normalized_html', '')):
                    value = html.unescape(match[1])
                    if value.startswith('[MATH:') and value.endswith(']'):
                        found[compact(value[6:-1])].append({'attribute': ':answer/value',
                            'json_field': f'{key}/select_lists/{select.get("index")}/options/{option_index}'})
    return found


def rendered_math(value):
    # The EDB seed imports md.py with this same half-open interval fallback.
    placeholder = '[MATH: ' + value + ']'
    extracted = md.extract_math_placeholder(placeholder)
    if extracted is None:
        extracted = value.strip()
    return md.math_to_markdown(extracted, display=True)


def mathml_mechanisms(math, old, rendered):
    """Narrow semantic/structural mismatches with explicit source predicates."""
    issues = []
    for fraction in math.find_all('mfrac'):
        thickness = str(fraction.get('linethickness', '')).strip()
        if re.fullmatch(r'0(?:\.0+)?(?:px|pt|em|ex|%)?', thickness):
            issues.append({'code': 'mathml-zero-rule-fraction-made-visible',
                'source': str(fraction), 'reason': 'Source explicitly suppresses the fraction bar; legacy mfrac always becomes division.'})
    for node in math.find_all('mover'):
        children = node.find_all(recursive=False)
        if node.get('accent') == 'true' and len(children) >= 2:
            issues.append({'code': 'mathml-accent-replaced-with-script', 'source': str(node),
                'reason': 'Legacy mover produces overline(...) or a superscript; md.py does not reconstruct an accent.'})
    for node in math.find_all('mphantom'):
        if node.get_text(strip=True):
            issues.append({'code': 'mathml-hidden-phantom-made-visible', 'source': str(node),
                'reason': 'Legacy mphantom emits its normally invisible descendants as ordinary math.'})
    for node in math.find_all('menclose'):
        notation = set(str(node.get('notation', '')).split())
        if notation & {'updiagonalstrike', 'downdiagonalstrike', 'horizontalstrike', 'verticalstrike'}:
            issues.append({'code': 'mathml-cancellation-removed', 'source': str(node),
                'reason': 'Legacy menclose emits descendants and discards the explicit cancellation marks.'})
    for node in math.find_all('mpadded'):
        if node.find(['mfrac', 'msup', 'msub', 'msubsup', 'msqrt', 'mroot', 'mtable']):
            issues.append({'code': 'mathml-padded-structure-flattened', 'source': str(node),
                'reason': 'Unsupported mpadded falls back to get_text, discarding descendant fraction/script/table structure.'})
    for table in math.find_all('mtable'):
        siblings = [child for child in table.parent.children if getattr(child, 'name', None)]
        at = siblings.index(table)
        before = siblings[at - 1].get_text(strip=True) if at else ''
        after = siblings[at + 1].get_text(strip=True) if at + 1 < len(siblings) else ''
        rows = table.find_all(['mtr', 'mlabeledtr'], recursive=False)
        if len(rows) < 2:
            continue
        if before == '{' and '\\begin{cases}' not in rendered and '\\begin{aligned}' not in rendered:
            issues.append({'code': 'mathml-cases-row-layout-lost', 'source': str(table),
                'reason': 'Source uses a left brace and multirow table; legacy output has semicolons without cases/alignment.'})
        if before == '(' and after == ')' and '\\begin{pmatrix}' not in rendered:
            issues.append({'code': 'mathml-parenthesized-matrix-layout-lost', 'source': str(table),
                'reason': 'Legacy matrix reconstruction recognizes square brackets or determinant bars, not parenthesized tables.'})
        lines = str(table.get('columnlines', ''))
        if any(line not in ('none', '') for line in lines.split()):
            issues.append({'code': 'mathml-matrix-column-separator-lost', 'source': str(table),
                'reason': 'Source columnlines contains a visible separator; legacy mtable serialization discards it.'})
    if re.search(r'(?<!\\)%', old):
        issues.append({'code': 'mathml-literal-percent-not-escaped', 'source': str(math),
            'reason': 'A literal percent in rendered MathML becomes an unescaped TeX comment marker.'})
    return issues


def run(args):
    started = time.monotonic()
    paths = sorted(args.lessons_root.glob('*/Source/*.html'), key=lambda path: int(path.stem))
    if args.topic:
        paths = [path for path in paths if path.stem in args.topic]
    HERE.mkdir(parents=True, exist_ok=True)
    records = []
    catalog = []
    errors = []
    counts = Counter()
    primary_output = (HERE / 'primary-mixed-title.jsonl').open('w')
    for number, path in enumerate(paths, 1):
        raw = path.read_text(errors='replace')
        try:
            data = json.loads(path.with_suffix('.json').read_text())
        except Exception as error:
            errors.append({'path': str(path), 'error': str(error)})
            continue
        items = data.get('lesson', {}).get('items', [])
        owners = sorted((raw.find('id="' + item['dom_id'] + '"'), item)
                        for item in items if item.get('dom_id') and raw.find('id="' + item['dom_id'] + '"') >= 0)
        positions = [p for p, _ in owners]
        owner_ends = {item['dom_id']: owner_end(raw, position) for position, item in owners}
        field_index = {item['dom_id']: field_math(item) for _, item in owners}
        title_matches = list(TITLE.finditer(raw))
        title_starts = [m.start() for m in title_matches]
        title_ends = [m.end() for m in title_matches]
        candidates = []
        for title_index, title in enumerate(title_matches):
            content = title[1]
            fragments, outer, mixed_loss, source_comments = title_info(content)
            counts['title_occurrences'] += 1
            if fragments:
                counts['titles_containing_mathml'] += 1
            if not (mixed_loss or source_comments or (fragments and SPECIAL.search(fragments[0]))):
                continue
            candidates.append((title.start(), title_index, title[0], fragments[0] if fragments else None,
                               mixed_loss, source_comments, outer, len(fragments)))
        for match in MML.finditer(raw):
            counts['mathml_occurrences'] += 1
            at = bisect.bisect_right(title_starts, match.start()) - 1
            if at >= 0 and match.end() <= title_ends[at]:
                continue
            if SPECIAL.search(match[0]):
                candidates.append((match.start(), None, match[0], match[0], False, [], None, 1))
        for offset, title_index, source, math_source, mixed_loss, comments, outer, fragment_count in candidates:
            which = bisect.bisect_right(positions, offset) - 1
            if which < 0:
                continue
            start, item = owners[which]
            if owner_ends[item['dom_id']] is None or offset >= owner_ends[item['dom_id']]:
                counts['unowned_source_occurrences_rejected'] += 1
                continue
            if item.get('step_type') == 'tutorial':
                kind, source_id = 'tutorial', int(item['content_id'])
            elif item.get('step_type') == 'example':
                kind, source_id = 'question', 'e-' + str(item['content_id'])
            elif item.get('item_type') == 'question':
                kind, source_id = 'question', 'q-' + str(item['question_id'])
            else:
                continue
            issues = []
            if math_source:
                math = BeautifulSoup(math_source, 'html.parser').find('math')
                old = legacy.mathml_to_text(math)
            else:
                math = None
                title_node = BeautifulSoup(source, 'html.parser').find('title')
                old = legacy.clean_svg_title_math(title_node.get_text('', strip=False))
            try:
                rendered = rendered_math(old)
            except Exception as error:
                errors.append({'path': str(path), 'offset': offset, 'stage': 'legacy Markdown', 'error': repr(error)})
                continue
            if mixed_loss:
                issues.append({'code': 'mixed-title-first-fragment',
                    'reason': 'extract_math_from_node returns the first descendant assistive MathML before reading the complete SVG title.',
                    'fragment_count': fragment_count, 'discarded_outer_template': outer})
            if comments and not math_source:
                issues.append({'code': 'source-tex-comment-line-scope-lost', 'source_comments': comments,
                    'reason': 'Source line-start TeX comments are retained in JSON then extract_math_placeholder normalizes every newline into a space.'})
            if math is not None:
                issues.extend(mathml_mechanisms(math, old, rendered))
            if not issues:
                continue
            stored = field_index[item['dom_id']].get(compact(old), [])
            prefix = raw[start:offset]
            attr = ':tutorial/content' if kind == 'tutorial' else ':question/problem'
            if item.get('step_type') == 'example' and re.search(r'class="[^"]*\bexampleExplanation\b', prefix):
                attr = ':question/worked-solution'
            if item.get('item_type') == 'question' and 'questionWidget-choiceLetterCircle' in prefix:
                attr = ':answer/value'
            attrs = {f['attribute'] for f in stored}
            if len(attrs) == 1:
                attr = next(iter(attrs))
            record = {'id': f'{path.stem}:{item["dom_id"]}:{offset}', 'topic_id': int(path.stem),
                'topic_title': data.get('topic_title'), 'kind': kind, 'source_id': source_id,
                'attribute': attr, 'dom_id': item['dom_id'], 'owner_title': item.get('title'),
                'source_file': str(path), 'source_offset': offset, 'source_line': raw.count('\n', 0, offset) + 1,
                'source_title_index': title_index, 'source_html': source, 'source_sha256': digest(source),
                'legacy_text': old, 'legacy_markdown': rendered, 'stored_json_matches': stored,
                'legacy_output_confirmed_in_archived_json': bool(stored), 'mechanisms': issues}
            records.append(record)
            if mixed_loss and stored and len(attrs) == 1:
                primary_output.write(json.dumps(record, ensure_ascii=False) + '\n')
                primary_output.flush()
            counts.update(set(issue['code'] for issue in issues))
        catalog.append({'topic_id': int(path.stem), 'topic_title': data.get('topic_title'),
            'html': str(path), 'html_sha256': digest(raw), 'json': str(path.with_suffix('.json')),
            'json_sha256': digest(path.with_suffix('.json').read_bytes()),
            'items': [{key: item.get(key) for key in ('item_type', 'step_type', 'content_id', 'question_id', 'step_id', 'dom_id')}
                      for item in items], 'source_occurrences': len(records) - sum(c['source_occurrences'] for c in catalog)})
        if number % 200 == 0:
            progress = {'files_scanned': number, 'files_total': len(paths), 'occurrences': len(records),
                        'seconds': round(time.monotonic() - started, 1)}
            (HERE / 'progress.json').write_text(json.dumps(progress, indent=2) + '\n')
            print(json.dumps(progress), flush=True)
    primary_output.close()
    by_mechanism = {}
    for code in sorted({m['code'] for r in records for m in r['mechanisms']}):
        group = [r for r in records if any(m['code'] == code for m in r['mechanisms'])]
        by_mechanism[code] = {'occurrences': len(group), 'topics': len({r['topic_id'] for r in group}),
            'owner_fields': len({(r['kind'], str(r['source_id']), r['attribute']) for r in group}),
            'confirmed_archived_json_occurrences': sum(r['legacy_output_confirmed_in_archived_json'] for r in group)}
    with (HERE / 'occurrences.jsonl').open('w') as output:
        for record in records:
            output.write(json.dumps(record, ensure_ascii=False) + '\n')
    (HERE / 'catalog.json').write_text(json.dumps(catalog, indent=2) + '\n')
    summary = {'scope': 'All archived lesson HTML files, source title and selected MathML loss predicates; this is not a general content lint or a current EDB defect count.',
        'files_scanned': len(paths), 'files_catalogued': len(catalog), 'occurrences': len(records),
        'counts': dict(counts), 'mechanisms': by_mechanism, 'errors': errors,
        'elapsed_seconds': round(time.monotonic() - started, 2),
        'code': {str(LEGACY): digest(LEGACY.read_bytes()), str(MARKDOWN): digest(MARKDOWN.read_bytes()),
                 str(Path(__file__).resolve()): digest(Path(__file__).read_bytes())}}
    (HERE / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps(summary, indent=2), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--lessons-root', type=Path, default=MA / 'DATA/Lessons')
    parser.add_argument('--topic', action='append')
    run(parser.parse_args())
