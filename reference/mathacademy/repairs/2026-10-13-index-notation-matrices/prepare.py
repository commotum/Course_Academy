"""Prepare CAS repairs from the retained complete lesson Pull; no database writes."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / 'scripts/question_capture'))
from edn import loads, dumps, kw

HERE = Path(__file__).resolve().parent
POSITIONS = {
    17592186100685: (1, 3), 17592186101126: (1, 2),
    17592186101127: (3, 3), 17592186235399: (3, 2),
    17592186269009: (1, 1), 17592186295091: (1, 1),
    17592186295092: (2, 3), 17592186400198: (4, 2),
    17592186400702: (3, 4),
}
lesson = loads((HERE / 'before.edn').read_text())
forms, changes, visited = [], [], set()
matrix = re.compile(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}', re.S)

def walk(node):
    if isinstance(node, list):
        for child in node:
            walk(child)
    elif isinstance(node, dict):
        eid = node.get(':db/id')
        if eid and eid not in visited:
            visited.add(eid)
            for attr, old in node.items():
                if attr not in (':tutorial/content', ':question/problem',
                                ':question/worked-solution', ':answer/value', ':answer/feedback'):
                    continue
                if not isinstance(old, str):
                    continue
                new = old.replace(r'[\begin{aligned}', r'\begin{bmatrix}').replace(
                    r'\end{aligned}]', r'\end{bmatrix}')
                if eid == 17592186101953:
                    new = new.replace('…', r'\cdots').replace('⋮', r'\vdots').replace('⋱', r'\ddots')
                if eid in POSITIONS and attr == ':question/problem':
                    i, j = POSITIONS[eid]
                    def highlight(match):
                        cells = [row.split('&') for row in match[1].split(r'\\')]
                        cell = cells[i - 1][j - 1].strip()
                        assert r'\boxed' not in match[1] and r'\bbox' not in match[1]
                        cells[i - 1][j - 1] = r' \boxed{' + cell + '} '
                        return r'\begin{bmatrix}' + r'\\'.join('&'.join(row) for row in cells) + r'\end{bmatrix}'
                    new, count = matrix.subn(highlight, new)
                    assert count == 1
                if eid == 17592186235399 and attr == ':question/problem':
                    new = re.sub(r'\n{3,}', '\n\n', '\n'.join(line.strip() for line in new.splitlines()))
                if eid == 17592186398270 and attr == ':question/worked-solution':
                    new = new.replace('E=', 'R=')
                if new != old:
                    forms.append([kw('db/cas'), eid, kw(attr), old, new])
                    changes.append({'entity': eid, 'attribute': attr})
                    node[attr] = new
        for child in node.values():
            walk(child)

walk(lesson)
(HERE / 'transaction.edn').write_text(dumps(forms) + '\n')
(HERE / 'expected.edn').write_text(dumps(lesson) + '\n')
(HERE / 'changes.json').write_text(json.dumps({
    'activity_id': 17592186101034, 'title': 'Index Notation for Matrices',
    'source': ':application/ca-engine', 'changes': changes,
    'highlight_positions': POSITIONS,
}, indent=2) + '\n')
print(f'{len(forms)} CAS updates across {len({f[1] for f in forms})} entities; {len(POSITIONS)} highlights restored')
