#!/usr/bin/env python3
"""Rebuild this shard's semantic reviews and exact whole-field proposals.

Read-only inputs: census14355, fresh capture14371 and MA source HTML/JSON.
This script never calls EDB or changes question answer/grader metadata.
"""
import collections
import html
import json
from pathlib import Path
import re
import sys
from bs4 import BeautifulSoup

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / 'scripts/question_capture/math_format.py').exists())
sys.path.insert(0, str(ROOT))
from scripts.question_capture.math_format import matrix_equation, matrix_tex, matrix_operands

BASE = HERE.parent
assigned = json.loads((HERE / 'assigned.json').read_text())
fields = json.loads((BASE / 'snapshot-fields.json').read_text())
topics = {x[':db/id']: x for x in json.loads((BASE/'capture/topics.json').read_text())}
fresh = {x[':db/id']: x for name in ['questions', 'entities'] for x in json.loads((BASE/f'capture/{name}.json').read_text())}
sources = {}
for tid in sorted({x['topics'][0] for x in assigned}):
    ma = topics[tid][':topic/math-academy-id']
    path = Path(f'/home/jake/Developer/MA/DATA/Lessons/{ma}/Source/{ma}')
    sj = json.loads(path.with_suffix('.json').read_text())
    soup = BeautifulSoup(path.with_suffix('.html').read_text(), 'html.parser')
    # Record actual source styles; representative evidence is explicitly family
    # evidence, never an assertion that a historical variant is the exact source.
    samples = []
    for table in soup.select('table'):
        styles = [{'rowspan': td.get('rowspan'), 'width': td.get('width'), 'style': td.get('style')}
                  for td in table.select('td')]
        if any('hidden' in str(td['style']) for td in styles):
            samples.append(styles)
    sources[tid] = {'ma_topic_id': ma, 'json_path': str(path.with_suffix('.json')),
                    'html_path': str(path.with_suffix('.html')), 'soup': soup,
                    'question_ids': [str(i.get('question_id')) for i in sj['lesson']['items'] if i.get('question_id')],
                    'border_samples': samples[:3]}

def bare(cell):
    cell = html.unescape(cell.strip())
    if cell.startswith('$$') and cell.endswith('$$'): return cell[2:-2].strip()
    if cell.startswith('$') and cell.endswith('$') and cell.count('$') == 2: return cell[1:-1].strip()
    return cell

def get_rows(x, before):
    start, end = x['span']
    if x['format'] == 'html':
        soup = BeautifulSoup(before[start:end], 'html.parser')
        table = soup.find('table')
        return [[td.get_text().strip() for td in tr.find_all(['td','th'], recursive=False)]
                for tr in table.find_all('tr')], start, end
    # A display-math cell contains newlines; census spans can then cover only
    # part of the table. These questions have one final table: expand to its
    # actual boundaries, remove only the Markdown separator and parse complete
    # rows. Internal TeX vertical pipes occur only in disconfirmed labeled tables.
    starts = list(re.finditer(r'(?m)^\|', before))
    start = starts[0].start()
    end = before.rfind('|') + 1
    table = before[start:end]
    table = re.sub(r'(?m)^\|[ \t:|\-]+\|[ \t]*$\n?', '', table)
    row_strings = re.split(r'\|[ \t]*\n\|', table.strip()[1:-1])
    return [[cell.strip() for cell in row.split('|')] for row in row_strings], start, end

def equation(parts):
    # Scalar controls in a label are emitted as actual controls between TeX
    # spans, never embedded in TeX. Other operands use the shared helper.
    out = []
    for part in parts:
        if isinstance(part, list):
            rendered = matrix_equation([part])
            out.append(rendered[len('<div class="matrix-answer">\n'):-len('\n</div>')])
        else:
            for token in re.split(r'(\{\{[^{}]+\}\})', part):
                if not token.strip(): continue
                if token.startswith('{{'):
                    out.append('<span class="matrix-answer-scalar">'+token+'</span>')
                else:
                    # Mixed Markdown label cells preserve each original math
                    # expression independently around the scalar control.
                    token = bare(token.strip())
                    out.append('<span class="matrix-answer-label">$'+html.escape(token, quote=False)+'$</span>')
    return '<div class="matrix-answer">\n'+'\n'.join(out)+'\n</div>'

def convert(x, rows):
    ma = sources[x['topics'][0]]['ma_topic_id']
    nonempty = [[c for c in row if c.strip()] for row in rows]
    # Single matrix families: labels may occupy their own middle row or a
    # rowspanned cell. Supplied mathematical entries remain in source row order.
    single = ma in [6375, 5869, 2927, 6007, 933, 1724, 1725]
    if ma == 6691 and 'Formula for IVP' not in ' '.join(x['titles']): single = True
    if single:
        labels = [c for row in nonempty for c in row if '=' in c]
        assert len(labels) == 1, (x['candidate_index'], labels)
        grid = [[bare(c) for c in row if c not in labels] for row in nonempty]
        grid = [row for row in grid if row]
        assert len({len(row) for row in grid}) == 1, (x['candidate_index'], grid)
        return equation([bare(labels[0]), grid]), [grid]
    assert len(nonempty) == 2, (x['candidate_index'], nonempty)
    top, bottom = nonempty
    top = list(top); bottom = [bare(c) for c in bottom]
    parts, grids = [], []
    def label(): parts.append(bare(top.pop(0)))
    def grid(width=1):
        values = [[bare(top.pop(0)) for _ in range(width)], [bottom.pop(0) for _ in range(width)]]
        grids.append(values); parts.append(values)
    # First label; derivative/system forms have a 2x2 coefficient matrix.
    label()
    derivative = ma == 2086 or (ma == 3189 and ('′' in parts[0] or "'" in parts[0]))
    grid(2 if derivative else 1)
    if ma == 3187 and 'Φ' in parts[0]:
        # Two independent equalities share one source layout. A punctuation
        # comma and the second equation label are adjacent rowspanned cells.
        label()
        label()
        grid()
    while top:
        label()
        if top: grid()
    assert not bottom, (x['candidate_index'], bottom)
    return equation(parts), grids

def semantic_tokens(rows):
    values = []
    for row in rows:
        for cell in row:
            if not cell.strip(): continue
            if re.search(r'\{\{field-[^{}]+\}\}', cell) and '$' in cell:
                values += [bare(token) for token in re.findall(r'\$[^$]+\$|\{\{field-[^{}]+\}\}', cell)]
            else:
                values.append(bare(cell))
    return collections.Counter(values)

reviews, proposals = [], []
for x in assigned:
    idx = x['candidate_index']
    key = f"{x['entity']}/{x['attribute']}"
    before = fields[key]
    assert fresh[x['entity']][':'+x['attribute']] == before, ('capture changed', idx)
    source = sources[x['topics'][0]]
    imported = [v.removeprefix('q-') for v in x['imported_ids'] if v.startswith('q-')]
    exact_ids = sorted(set(imported) & set(source['question_ids']))
    evidence = {'source_json': source['json_path'], 'source_html': source['html_path'],
                'exact_question_ids_present': exact_ids,
                'source_scope': 'Exact source widget present; source-family border styles also inspected.' if exact_ids else
                'Source-family only: no exact imported question ID present in local source; entries and geometry taken from stored field.',
                'stored_rows': x['rows'], 'stored_span': x['span']}
    review = {'candidate_index': idx, 'entity': x['entity'], 'attribute': x['attribute'], 'evidence': evidence}
    if source['ma_topic_id'] == 1972:
        review.update(status='disconfirmed', rationale='Polynomial long division with a longdiv enclosure and subtraction work; its layout is not a matrix or vector.')
    elif source['ma_topic_id'] in [1673, 4820]:
        review.update(status='disconfirmed', rationale='A labeled incidence/relation data table: row and column vertex/edge/domain labels are meaningful headers and must remain visible.')
    elif idx == 613:
        review.update(status='disconfirmed', rationale='Already a canonical matrix answer: enclosing matrix-answer and matrix-answer-brackets classes supply brackets around the 3x3 table; no imported layout table remains.')
    else:
        rows, start, end = get_rows(x, before)
        replacement, grids = convert(x, rows)
        rendered = BeautifulSoup(replacement, 'html.parser')
        rendered_cells = [[tag.get_text().strip() for tag in rendered.select('span.matrix-answer-label, span.matrix-answer-scalar, td')]]
        assert semantic_tokens(rows) == semantic_tokens(rendered_cells), ('mathematical token changed', idx)
        assert all('=' not in cell for grid in grids for row in grid for cell in row), ('label in grid', idx)
        after = before[:start] + replacement + before[end:]
        assert before != after
        markers = lambda v: collections.Counter(re.findall(r'\{\{[^{}]+\}\}', v))
        assert markers(before) == markers(after), ('marker changed', idx)
        assert all(not re.search(r'\{\{(?:answer-field:)?field-[^{}]+\}\}', tex)
                   for tex in replacement.split('$')[1::2]), ('control inside math', idx)
        rationale = 'Stored row/rowspan geometry and empty bracket-edge cells describe bracketed mathematical operands, not data headers. '
        if source['border_samples']:
            rationale += 'Source-family HTML has hidden interior borders and drawn bracket edges. '
        else:
            rationale += 'Local source uses fenced MathML matrices in this subject; the exact free-entry layout is absent. Stored problem and matrix dimensions establish the grid. '
        rationale += 'Preserve every supplied entry, scalar, sign, operator, equality and field in its original spatial operand.'
        if (start,end) != tuple(x['span']):
            rationale += ' Census cut a multiline display-math cell; replacement expands to the complete final Markdown table.'
        review.update(status='confirmed', rationale=rationale)
        evidence.update(replacement_span=[start,end], grids=grids)
        proposals.append({'entity': x['entity'], 'attribute': x['attribute'], 'before': before, 'after': after,
                          'candidate_indices': [idx], 'rationale': rationale,
                          'replacements': [{'start': start, 'end': end, 'before': before[start:end],
                                            'after': replacement, 'candidate_indices': [idx]}]})
    reviews.append(review)

assert len(reviews) == len(assigned)
assert len({(p['entity'],p['attribute']) for p in proposals}) == len(proposals)
for name, value in [('reviews', reviews), ('proposals', proposals),
                    ('source-evidence', {str(k): {a:b for a,b in v.items() if a != 'soup'} for k,v in sources.items()})]:
    (HERE/f'{name}.json').write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n')
print(json.dumps({'reviews': len(reviews), 'statuses': dict(collections.Counter(x['status'] for x in reviews)),
                  'proposals': len(proposals)}, indent=2))
