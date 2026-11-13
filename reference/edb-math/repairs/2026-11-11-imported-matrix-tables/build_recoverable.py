"""Review and restore the closed, blank-only matrix answer-grid family."""
import json
from collections import defaultdict
from pathlib import Path
import re
import sys

H = Path(__file__).resolve().parent
ROOT = H.parents[3]
sys.path.insert(0, str(ROOT))
from scripts.question_capture.math_format import normalize_matrix_answer_tables

rows = json.loads((H/'recoverable.json').read_text())
fields = json.loads((H/'snapshot-fields.json').read_text())
current = {r[':db/id']: r for r in json.loads((H/'capture/entities.json').read_text())}
grouped = defaultdict(list)
reviews = []
for row in rows:
    key = f"{row['entity']}/{row['attribute']}"
    before = fields[key]
    assert current[row['entity']][':'+row['attribute']] == before
    assert before[row['span'][0]:row['span'][1]] == row['table']
    given = re.search(r'\\begin\{(bmatrix|pmatrix|matrix)\}[\s\S]*?\\end\{\1\}', before)
    prefix = given[0] + '\n\n' if given else ''
    probe = prefix + row['table']
    converted = normalize_matrix_answer_tables(probe)
    assert converted != probe and converted.startswith(prefix)
    after = converted[len(prefix):]
    markers = lambda value: re.findall(r'\{\{[^{}]+\}\}', value)
    assert markers(row['table']) == markers(after)
    assert 'class="matrix-answer-brackets"' in after
    # This closed family has exactly one mathematical label and blank cells.
    field_rows = [[cell for cell in r if re.fullmatch(r'\{\{[^{}]+\}\}', cell)] for r in row['rows']]
    field_rows = [r for r in field_rows if r]
    assert len(field_rows) >= 2 and len({len(r) for r in field_rows}) == 1
    for cells in field_rows:
        assert '<tr>'+''.join('<td>'+cell+'</td>' for cell in cells)+'</tr>' in after
    grouped[(row['entity'], row['attribute'])].append((row, after))
    reviews.append({'candidate_index': row['candidate_index'], 'entity': row['entity'],
                    'attribute': row['attribute'], 'decision': 'confirmed',
                    'evidence': 'Explicit matrix in question; only a mathematical equality/mapping label, blank border cells and a rectangular grid of answer markers. Empty edge cells and rowspan/offset Markdown rows are bracket decoration, not data columns.',
                    'expected_grid': field_rows, 'replacement': after})
proposals = []
for (entity, attr), blocks in grouped.items():
    before = fields[f'{entity}/{attr}']
    after = before
    end = len(before)
    for row, replacement in sorted(blocks, key=lambda r: r[0]['span'][0], reverse=True):
        start, stop = row['span']
        assert stop <= end
        after = after[:start]+replacement+after[stop:]
        end = start
    proposals.append({'entity': entity, 'attribute': attr, 'before': before, 'after': after,
                      'candidate_indices': [r['candidate_index'] for r,_ in blocks],
                      'replacements': [{'start': r['span'][0], 'end': r['span'][1],
                          'before': r['table'], 'after': replacement,
                          'candidate_indices': [r['candidate_index']]} for r,replacement in blocks],
                      'rationale': 'Restore blank-only matrix/vector brackets and source row-major answer positions.'})
for name, value in [('recoverable-reviews.json', reviews), ('recoverable-proposals.json', proposals)]:
    (H/name).write_text(json.dumps(value, indent=2, ensure_ascii=False)+'\n')
print(json.dumps({'confirmed_blocks': len(reviews), 'field_repairs': len(proposals)}))
