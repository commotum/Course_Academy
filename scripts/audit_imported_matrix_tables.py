#!/usr/bin/env python3
"""Read-only census of imported tables that may encode matrices or vectors.

Consumes the captured native export in the audit directory. Every imported
table is retained, including exclusions, so heuristics cannot silently discard
an unfamiliar damaged layout. Classifications are review priorities, not proof
that every flagged table should be converted.
"""
import argparse
from collections import Counter, defaultdict
import csv
import gzip
import json
from pathlib import Path
import re
import sys

from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.question_capture.math_format import normalize_matrix_answer_tables

CONTENT = {'question/problem', 'question/worked-solution', 'tutorial/content',
           'answer/value', 'answer/feedback', 'answer-field/key', 'multistep/context'}
LINKS = {'question/answer-fields', 'answer-field/choices', 'answer-field/correct',
         'knowledge-point/questions', 'knowledge-point/canonical-example',
         'topic/knowledge-points', 'activity/steps', 'step/content', 'activity/scope',
         'multistep/steps', 'assigned-problem/content'}
META = {'question/id', 'question/math-academy-id', 'question/retired',
        'tutorial/id', 'tutorial/math-academy-id', 'tutorial/title',
        'knowledge-point/title', 'knowledge-point/question-generator',
        'topic/title', 'topic/math-academy-id', 'activity/title'}
MARKER = re.compile(r'\{\{(?:answer-field:)?[^{}]+\}\}')
MATRIX = re.compile(r'\\begin\{(?:[bpvVB]?matrix|array)\}|\\(?:matrix|pmatrix|eqalign)\{')
WORDS = re.compile(r'\b(?:matri(?:x|ces)|vectors?|eigen\w*|determinants?|standard basis|linear transformations?|row operations?|row.echelon|change of basis)\b', re.I)


def split_row(line):
    return [c.strip() for c in re.split(r'(?<!\\)\|', line.strip().strip('|'))]


def table_blocks(text):
    # Keep offsets in the original text, while ignoring fenced/inline code.
    searchable = re.sub(r'```[\s\S]*?```|`[^`\n]*`', lambda m: ' ' * len(m[0]), text)
    for match in re.finditer(r'(?m)^[^\n]*\|[^\n]*(?:\n[^\n]*\|[^\n]*)+', searchable):
        lines = text[match.start():match.end()].splitlines()
        separators = [i for i, line in enumerate(lines)
                      if all(re.fullmatch(r':?-{2,}:?', c) for c in split_row(line))]
        if not separators:
            continue
        rows = [split_row(line) for i, line in enumerate(lines) if i not in separators]
        yield {'format': 'markdown', 'start': match.start(), 'end': match.end(),
               'table': text[match.start():match.end()], 'rows': rows,
               'canonical': False}
    # HTML is a supplemental sweep for the same lost-border source editors.
    stack, spans = [], []
    for token in re.finditer(r'<table\b[^>]*>|</table\s*>', searchable, re.I):
        if not token[0].startswith('</'):
            stack.append(token.start())
        elif stack:
            spans.append((stack.pop(), token.end()))
    for start, end in sorted(spans):
        source = text[start:end]
        table = BeautifulSoup(source, 'html.parser').find('table')
        rows = [[cell.get_text(' ', strip=True) for cell in row.find_all(['td', 'th'], recursive=False)]
                for row in table.find_all('tr') if row.find_parent('table') is table]
        yield {'format': 'html', 'start': start, 'end': end,
               'table': source, 'rows': rows,
               'canonical': table.get('aria-label') in ('Answer matrix', 'Equation rows')}


def classify(block, text, titles):
    if block['canonical']:
        return 'canonical', ['Existing native bracketed input matrix or equation layout']
    rows = block['rows']
    cells = [cell for row in rows for cell in row]
    nonempty = [cell for cell in cells if cell]
    fields = [cell for cell in nonempty if MARKER.fullmatch(cell)]
    labels = [cell for cell in nonempty if not MARKER.fullmatch(cell)]
    blanks = len(cells) - len(nonempty)
    reasons = []
    explicit = bool(MATRIX.search(text))
    semantic = bool(WORDS.search(text + ' ' + ' '.join(titles)))
    if fields:
        reasons.append(f'{len(fields)} answer placeholders in table cells')
    if blanks:
        reasons.append(f'{blanks} empty layout cells')
    if explicit:
        reasons.append('Explicit matrix notation in the containing content')
    if semantic:
        reasons.append('Matrix/vector context in content or lesson titles')
    # Labeled row/column axes are meaningful data, even when their entries
    # form a mathematical matrix (distance matrices, sign tables, etc.).
    # Numeric entries alone are not headings; a fully populated numeric matrix
    # must stay in the review queue even though it looks rectangular.
    axes = bool(rows) and any(re.search(r'[A-Za-z]', c) and '=' not in c and not MATRIX.search(c)
                             for c in rows[0] if not MARKER.search(c))
    assignment_label = any(re.search(r'=\s*(?:\\,\s*)*\$\s*$|≈|\\approx\b|⟶|→|\\longrightarrow', c) for c in (rows[0] if rows else []))
    headered = (axes and not assignment_label and len(rows) > 1 and len(rows[0]) > 1 and all(rows[0][1:])
                and all(row and row[0] for row in rows[1:])
                and len({len(row) for row in rows}) == 1)
    directional_headers = any(re.fullmatch(r'(?:\*\*)?(?:from|to):?(?:\*\*)?', c, re.I) for c in cells)
    if headered or directional_headers:
        return 'headered_table', reasons + ['Complete column headings and row labels; retain as a table unless source evidence says otherwise']
    given = re.search(r'\\begin\{(bmatrix|pmatrix|matrix)\}[\s\S]*?\\end\{\1\}', text)
    probe = (given[0] + '\n\n' if given else '') + block['table']
    if normalize_matrix_answer_tables(probe) != probe and fields and not any(
            not (MARKER.fullmatch(cell) or re.fullmatch(r'\$[\s\S]+\$', cell)) for cell in nonempty):
        return 'recoverable_layout', reasons + ['Existing matrix-grid formatter recognizes the layout']
    # No prose headers/data cells: a few math labels plus blank editor slots.
    math_labels = bool(labels) and all(re.fullmatch(r'\$[\s\S]+\$', c) for c in labels)
    if fields and blanks and (explicit or semantic) and (math_labels or not labels):
        return 'strong_layout_candidate', reasons + ['Only math labels, placeholders and empty cells; no data headers']
    if (fields and (explicit or semantic)) or (blanks and (explicit or semantic)):
        return 'needs_review', reasons + ['Source or visual inspection needed to establish the table role']
    if any(MATRIX.search(cell) for cell in cells):
        return 'needs_review', reasons + ['Matrix notation inside table cells; could be an intentional comparison table']
    if fields and blanks and math_labels:
        return 'other_math_layout', reasons + ['Possible fraction/system layout; no matrix/vector evidence yet']
    if semantic:
        return 'needs_review', reasons + ['Unlabeled table in matrix/vector context; source inspection needed']
    if len(rows) >= 2 and nonempty and all(re.fullmatch(r'\$[\s\S]+\$|[+−-]?\d+(?:\.\d+)?', c) for c in nonempty):
        return 'unlabeled_math_array', reasons + ['Unlabeled mathematical array, even without matrix/vector keywords']
    return 'other_table', reasons or ['No matrix/vector layout evidence']


def audit(snapshot, output):
    output.mkdir(parents=True, exist_ok=True)
    meta = defaultdict(dict)
    parents = defaultdict(set)
    content = []
    stream = gzip.open(snapshot, 'rt') if snapshot.suffix == '.gz' else snapshot.open()
    for line in stream:
        row = json.loads(line)
        entity, attribute = row['e'], row['a']
        if attribute in META:
            value = row.get('raw_string') or row.get('uuid') or row.get('ref_eid')
            if value is None and re.fullmatch(r'\d+', row['value_edn']):
                value = int(row['value_edn'])
            if attribute == 'question/retired':
                value = row['value_edn'] == 'true'
            meta[entity][attribute] = value
        if attribute in LINKS:
            parents[row['ref_eid']].add((entity, attribute))
        if attribute in CONTENT and isinstance(row.get('raw_string'), str):
            content.append(row)
    stream.close()

    def context(entity):
        seen, frontier, records = set(), {entity}, []
        for _ in range(9):
            next_frontier = set()
            for item in frontier - seen:
                seen.add(item)
                if item in meta:
                    records.append({'entity': item, **meta[item]})
                next_frontier.update(p for p, _ in parents.get(item, ()))
            frontier = next_frontier
        return records

    ledger, counts, questions, tutorials = [], Counter(), set(), set()
    for row in content:
        text = row['raw_string']
        blocks = list(table_blocks(text))
        if not blocks:
            continue
        ctx = context(row['e'])
        imported = [r for r in ctx if r.get('question/math-academy-id') or r.get('tutorial/math-academy-id')]
        if not imported:
            continue
        qs = [r for r in imported if r.get('question/math-academy-id')]
        ts = [r for r in imported if r.get('tutorial/math-academy-id')]
        questions.update(r['entity'] for r in qs)
        tutorials.update(r['entity'] for r in ts)
        titles = [r[key] for r in ctx for key in ('knowledge-point/title', 'topic/title', 'tutorial/title') if r.get(key)]
        for block in blocks:
            priority, reasons = classify(block, text, titles)
            active_questions = [r['entity'] for r in qs if not r.get('question/retired')]
            retired_only = bool(qs) and not active_questions and not ts
            record = {'entity': row['e'], 'attribute': row['a'],
                      'format': block['format'], 'priority': priority,
                      'retired_only': retired_only, 'question_ids': sorted(r['entity'] for r in qs),
                      'active_question_ids': sorted(active_questions),
                      'pooled_question_ids': sorted(q for q in active_questions if any(a == 'knowledge-point/questions' for _,a in parents.get(q, ()))),
                      'canonical_question_ids': sorted(q for q in active_questions if any(a == 'knowledge-point/canonical-example' for _,a in parents.get(q, ()))),
                      'imported_ids': sorted({str(r.get('question/math-academy-id') or r.get('tutorial/math-academy-id')) for r in imported}),
                      'knowledge_points': sorted({r['entity'] for r in ctx if r.get('knowledge-point/title')}),
                      'topics': sorted({r['entity'] for r in ctx if r.get('topic/title')}),
                      'generator_ids': sorted({r['knowledge-point/question-generator'] for r in ctx if r.get('knowledge-point/question-generator')}),
                      'titles': sorted(set(titles)), 'reasons': reasons,
                      'rows': block['rows'], 'table': block['table'],
                      'span': [block['start'], block['end']],
                      'context_before': text[max(0, block['start']-600):block['start']],
                      'context_after': text[block['end']:block['end']+250]}
            ledger.append(record)
            counts[(block['format'], priority, 'retired' if retired_only else 'current')]+=1
    priorities = ['recoverable_layout', 'strong_layout_candidate', 'needs_review']
    candidates = [r for r in ledger if r['priority'] in priorities and not r['retired_only']]
    candidates.sort(key=lambda r: (priorities.index(r['priority']), r['entity'], r['span'][0]))
    question_records = {}
    for index, row in enumerate(candidates):
        for qid in row['active_question_ids']:
            entry = question_records.setdefault(qid, {'question_id': qid,
                'imported_id': meta[qid]['question/math-academy-id'], 'priority': row['priority'],
                'markdown_priority': None, 'html_priority': None,
                'candidate_indices': [], 'formats': set(), 'titles': set(), 'knowledge_points': set(),
                'topics': set(), 'generator_ids': set()})
            entry['candidate_indices'].append(index)
            entry['formats'].add(row['format'])
            if entry[row['format'] + '_priority'] is None:
                entry[row['format'] + '_priority'] = row['priority']
            for key in ('titles', 'knowledge_points', 'topics', 'generator_ids'):
                entry[key].update(row[key])
    question_rows = [{k: sorted(v) if isinstance(v, set) else v for k,v in row.items()}
                     for row in question_records.values()]
    question_rows.sort(key=lambda r: (priorities.index(r['priority']), r['question_id']))
    topics = {}
    for q in question_rows:
        for tid in q['topics']:
            t = topics.setdefault(tid, {'topic_id': tid, 'title': meta[tid].get('topic/title'),
                'math_academy_id': meta[tid].get('topic/math-academy-id'), 'question_ids': [], 'priorities': Counter()})
            t['question_ids'].append(q['question_id'])
            t['priorities'][q['priority']] += 1
    topic_rows = sorted(topics.values(), key=lambda r: (-len(r['question_ids']), r['topic_id']))
    manifest_path = snapshot.with_suffix('') if snapshot.suffix == '.gz' else snapshot
    manifest = json.loads(manifest_path.with_suffix('.manifest.json').read_text())
    summary = {'basis': manifest['basis_t'], 'database_writes': 0,
               'imported_questions_in_database': sum('question/math-academy-id' in v for v in meta.values()),
               'imported_tutorials_in_database': sum('tutorial/math-academy-id' in v for v in meta.values()),
               'all_content_fields_scanned': manifest['all_content_attribute_counts'],
               'imported_questions_with_tables': len(questions), 'imported_tutorials_with_tables': len(tutorials),
               'imported_table_blocks': len(ledger), 'candidate_blocks': len(candidates),
               'candidate_questions': len({q for r in candidates for q in r['active_question_ids']}),
               'question_priority_counts_disjoint': dict(Counter(r['priority'] for r in question_rows)),
               'markdown_question_priority_counts_disjoint': dict(Counter(r['markdown_priority'] for r in question_rows if r['markdown_priority'])),
               'topics_with_candidate_questions': len(topic_rows),
               'candidate_pooled_questions': len({q for r in candidates for q in r['pooled_question_ids']}),
               'candidate_canonical_examples': len({q for r in candidates for q in r['canonical_question_ids']}),
               'markdown_candidate_blocks': sum(r['format'] == 'markdown' for r in candidates),
               'markdown_candidate_questions': len({q for r in candidates if r['format'] == 'markdown' for q in r['active_question_ids']}),
               'by_format_priority_status': {'/'.join(k): v for k,v in sorted(counts.items())},
               'candidate_priorities': dict(Counter(r['priority'] for r in candidates)),
               'supplemental_unlabeled_arrays': sum(r['priority'] == 'unlabeled_math_array' for r in ledger),
               'supplemental_other_math_layouts': sum(r['priority'] == 'other_math_layout' for r in ledger),
               'scope': 'Current imported prompts, solutions, answer options/feedback/keys, tutorials and multipart contexts; Markdown plus supplemental HTML sweep',
               'limitations': ['Heuristic candidate census, not proof of corruption; source comparison needed for ambiguous tables',
                               'Every imported table is retained in the ledger, including low-signal and canonical tables',
                               'Pure images, flattened prose without any table markup, and detached answer entities without imported ownership are outside this table search']}
    for name, data in [('candidates.json', candidates), ('candidate-questions.json', question_rows),
                       ('topics.json', topic_rows), ('summary.json', summary),
                       ('other-math-layouts.json', [r for r in ledger if r['priority'] == 'other_math_layout']),
                       ('weak-array-candidates.json', [r for r in ledger if r['priority'] == 'unlabeled_math_array'])]:
        (output/name).write_text(json.dumps(data, indent=2, ensure_ascii=False)+'\n')
    with (output/'all-imported-tables.jsonl').open('w') as target:
        for row in ledger:
            target.write(json.dumps(row, ensure_ascii=False)+'\n')
    with (output/'candidates.csv').open('w', newline='') as target:
        columns = ['entity', 'attribute', 'format', 'priority', 'question_ids', 'knowledge_points', 'titles', 'reasons']
        writer = csv.DictWriter(target, fieldnames=columns, lineterminator='\n')
        writer.writeheader()
        for row in candidates:
            writer.writerow({key: '; '.join(map(str, row[key])) if isinstance(row[key], list) else row[key] for key in columns})
    with (output/'candidate-questions.csv').open('w', newline='') as target:
        columns = ['question_id', 'imported_id', 'priority', 'markdown_priority', 'html_priority', 'formats', 'knowledge_points', 'topics', 'titles', 'generator_ids']
        writer = csv.DictWriter(target, fieldnames=columns, lineterminator='\n')
        writer.writeheader()
        for row in question_rows:
            writer.writerow({key: '; '.join(map(str, row[key])) if isinstance(row[key], list) else row[key] for key in columns})
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--snapshot', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    audit(args.snapshot, args.output)
