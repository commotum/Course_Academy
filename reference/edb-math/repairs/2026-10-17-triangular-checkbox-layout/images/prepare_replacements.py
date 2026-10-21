"""Prepare faithful TeX transcriptions; no database or source-asset writes."""
from pathlib import Path
from bs4 import BeautifulSoup
import hashlib
import json
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
CAPTURE = HERE / 'capture-3479'
snapshot = json.loads((CAPTURE / 'snapshot.json').read_text())
fields = json.loads((CAPTURE / 'image-fields.json').read_text())['image_fields']
MATH = Path('/media/jake/SSD/EDB/math')


def matrix(rows, name=None, blue=(), red=()):
    def cell(i, j, value):
        color = 'blue' if (i, j) in blue else 'red' if (i, j) in red else None
        return r'{\color{' + color + '}' + str(value) + '}' if color else str(value)
    body = r' \\ '.join(' & '.join(cell(i, j, value) for j, value in enumerate(row)) for i, row in enumerate(rows))
    return '$$\n' + (name + ' = ' if name else '') + r'\begin{bmatrix}' + body + r'\end{bmatrix}' + '\n$$'


A3 = [[-2, 0, 0], [6, -1, 0], [0, 0, 0]]
A4 = [[0, 0, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0], [0, 0, 1, 2]]
DIFFERENCE = [[A4[j][i] - A4[i][j] for j in range(4)] for i in range(4)]
assert DIFFERENCE == [[0, 0, 0, 0], [0, 0, 1, 0], [0, -1, 0, 1], [0, 0, -1, 0]]
upper_region = lambda n: {(i, j) for i in range(n) for j in range(i + 1, n)}
transcriptions = {
    'fc2ed708d717844ca73b7ecbfd8467923fad091ae524153350e7e2fb3df1ea4e': matrix(A3, 'A'),
    '5260137f2dbf20b44400659be8467da333ff228e5bff323465f920a9505ee5f2': matrix(A3, 'A', blue=upper_region(3)),
    'ad9636de9b8c93338350a6b99d88476b481ed1bf03a5dd64935abedbdb626524': '\n\n'.join([
        matrix([[0, 0, 0], [0, 0, 1], [0, 0, 0]], 'A'),
        matrix([[0, 0, 0], [0, 0, 0], [1, 0, 0]], 'B'),
        matrix([[1, 0, 1], [0, 0, 0], [1, 0, 1]], 'C'),
    ]),
    '4dd9b1c1b3d789c166ecd8f6d2a909609c7f4324705c84115cce84a29181bf32': matrix(A4, 'A'),
    'c1ec838cd30cca8fbb2e3996d5a7d84dadb233e1951d05b532a9d606d887eb2f': matrix(A4, 'A', red={(2, 1), (3, 2)}),
    'f39c68a9b1f5e16caffbf159b629a958e147e14099334b049bdfcd857eef84d2': matrix(A4, 'A', blue=upper_region(4)),
    'f4415c87201f5b92f23e3320c313cd58ac4e720135928645896f976614c5eaa0': matrix(DIFFERENCE, 'A^T-A', red={(1, 2), (2, 3)}),
}
changes, evidence = [], []
for field in fields:
    after = field['value']
    for path in field['images']:
        key = Path(path).stem
        actual = MATH / path
        assert hashlib.sha256(actual.read_bytes()).hexdigest() == key
        after = after.replace('![](' + path + ')', '\n' + transcriptions[key] + '\n')
        evidence.append({'entity': field['entity'], 'attribute': field['attribute'], 'source_asset': str(actual),
                         'sha256': key, 'visually_inspected': True, 'replacement': transcriptions[key]})
    after = re.sub(r'\n{3,}', '\n\n', after).strip()
    assert '![' not in after and '<img' not in after
    changes.append({'entity': field['entity'], 'attribute': field['attribute'], 'before': field['value'], 'after': after,
                    'reason': 'Replace raster matrix mathematics with native TeX, preserving entries, labels and colored teaching cues.'})

source_path = Path('/home/jake/Developer/MA/DATA/Lessons/1777/Source/1777.html')
source = BeautifulSoup(source_path.read_text(), 'html.parser').find(id='step-16111')
tutorial_matrices = []
for math in source.select('mjx-assistive-mml math'):
    table = math.find('mtable')
    if not table:
        continue
    rows, blue = [], set()
    for i, row in enumerate(table.find_all('mtr', recursive=False)):
        values = []
        for j, cell in enumerate(row.find_all('mtd', recursive=False)):
            values.append(int(cell.get_text('', strip=True).replace('−', '-')))
            style = cell.find(attrs={'mathcolor': True})
            if style:
                assert style['mathcolor'] == 'blue'
                blue.add((i, j))
        rows.append(values)
    tutorial_matrices.append({'rows': rows, 'blue_cells': sorted(blue), 'tex': matrix(rows, blue=blue)})
assert [len(item['rows']) for item in tutorial_matrices] == [2, 3, 4, 2, 3, 4]
for i, item in enumerate(tutorial_matrices):
    n = len(item['rows'])
    region = {(r, c) for r in range(n) for c in range(n) if (r > c if i < 3 else r < c)}
    assert set(map(tuple, item['blue_cells'])) == region
    assert all(item['rows'][r][c] == 0 for r, c in region)

tutorial = next(step[':step/content'] for activity in snapshot['topic'][':activity/_scope']
                for step in activity[':activity/steps'] if ':tutorial/content' in step[':step/content'])
before = tutorial[':tutorial/content']
blocks = re.findall(r'\$\$[\s\S]*?\$\$', before)
assert len(blocks) == 2
after = before.replace(blocks[0], '\n\n'.join(item['tex'] for item in tutorial_matrices[:3]))
after = after.replace(blocks[1], '\n\n'.join(item['tex'] for item in tutorial_matrices[3:]))
changes.append({'entity': tutorial[':db/id'], 'attribute': ':tutorial/content', 'before': before, 'after': after,
                'reason': 'Restore four omitted source matrices and original blue zero-region highlights; stack all six matrices vertically.'})

plan = {'basis': snapshot['basis'], 'database': 'math', 'topic': 17592186050283,
        'changes': changes, 'image_transcriptions': evidence,
        'tutorial_source': {'file': str(source_path), 'dom_id': 'step-16111', 'source_lines': [1253, 1476],
                            'original_matrices': tutorial_matrices, 'matrices_restored': 4},
        'database_writes': 0}
(HERE / 'replacements.json').write_text(json.dumps(plan, indent=2) + '\n')
print(json.dumps({'basis': plan['basis'], 'changed_fields': len(changes), 'canonical_examples': 3,
                  'raster_references_replaced': len(evidence), 'tutorial_matrices_before': 2,
                  'tutorial_matrices_after': 6, 'ready_for_root_transaction': True}, indent=2))
