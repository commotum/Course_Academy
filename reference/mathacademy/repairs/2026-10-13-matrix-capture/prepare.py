"""Prepare guarded matrix repairs; original cell contents remain unchanged.

The database-wide query results live in /tmp/matrix-capture-audit. Saved source
MathML supports additional repairs within the four explicitly requested topics.
This script prepares transactions only; it does not submit them.
"""
import collections
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / 'scripts/question_capture'))
from edn import dumps, loads, kw

HERE = Path(__file__).resolve().parent
ATTRS = ['tutorial/content', 'question/problem', 'question/worked-solution',
         'answer/value', 'answer/feedback', 'multistep/context']
TOPICS = [17592186050765, 17592186049120, 17592186048980, 17592186049422]
fields, ownership, source_ids, augmented = {}, {}, {}, set()
topics = {}

def collect(node, records):
    if isinstance(node, list):
        for child in node:
            collect(child, records)
    elif isinstance(node, dict):
        if ':db/id' in node:
            records.setdefault(node[':db/id'], {}).update(node)
        for child in node.values():
            collect(child, records)

for index, eid in enumerate(TOPICS):
    topic = loads((HERE / f'{eid}.edn').read_text())
    records = {}
    collect(topic, records)
    topics[eid] = {'title': topic[':topic/title'], 'fields_repaired': 0}
    for entity, record in records.items():
        mid = record.get(':tutorial/math-academy-id', record.get(':question/math-academy-id'))
        if mid is not None:
            source_ids[entity] = (topic[':topic/math-academy-id'], str(mid))
        for attr in ATTRS:
            value = record.get(':' + attr)
            if isinstance(value, str):
                key = (entity, attr)
                fields[key] = value
                ownership[key] = (index, eid)
    for entity, record in records.items():
        if re.search(r'\baugmented\s+matri(?:x|ces)\b', record.get(':question/problem', ''), re.I):
            augmented.add(entity)
            for field in record.get(':question/answer-fields', []):
                for answer in field.get(':answer-field/choices', []):
                    augmented.add(answer[':db/id'])

for attr in ATTRS:
    path = Path('/tmp/matrix-capture-audit') / (attr.replace('/', '-') + '.edn')
    for entity, value in loads(path.read_text()):
        fields.setdefault((entity, attr), value)

source = collections.defaultdict(lambda: collections.defaultdict(set))
for record in json.loads((HERE / 'source-reextraction.json').read_text()):
    old, new = record['old'], record['new']
    if not old['errors'] and not new['errors'] and old['text'] != new['text'] and r'\begin{aligned}' in old['text']:
        source[(record['topic'], record['owner'])][old['text']].add(new['text'])

def cells(body):
    """Split only TeX's top-level row and column separators."""
    rows, row, cell, depth, index, environments = [], [], [], 0, 0, []
    while index < len(body):
        char = body[index]
        if char == '\\':
            environment = re.match(r'\\(begin|end)\{([^{}]+)\}', body[index:])
            if environment:
                if environment[1] == 'begin': environments.append(environment[2])
                elif not environments or environments.pop() != environment[2]: return None
                cell.extend(environment[0]); index += len(environment[0]); continue
            if body[index:index + 2] == '\\\\' and depth == 0 and not environments:
                row.append(''.join(cell)); rows.append(row); row, cell = [], []
                index += 2; continue
            # Escaped braces are glyphs, not grouping boundaries.
            if index + 1 < len(body):
                cell.extend(body[index:index + 2]); index += 2; continue
        if char == '{': depth += 1
        elif char == '}': depth -= 1
        elif char == '&' and depth == 0 and not environments:
            row.append(''.join(cell)); cell = []; index += 1; continue
        cell.append(char); index += 1
    row.append(''.join(cell)); rows.append(row)
    return rows if depth == 0 and not environments else None

def has_relation(cell):
    depth = 0
    for token in re.findall(r'\\[A-Za-z]+|\\.|.', cell, re.S):
        if token == '{': depth += 1
        elif token == '}': depth -= 1
        elif depth == 0 and token in ('=', r'\le', r'\leq', r'\ge', r'\geq', r'\approx', r'\equiv'): return True
    return False

def repair_matrices(text):
    """Resolve innermost fenced environments first, including cofactor matrices."""
    for _ in range(256):
        stack, pairs = [], []
        for token in re.finditer(r'\\(begin|end)\{([^{}]+)\}', text):
            if token[1] == 'begin': stack.append(token)
            elif stack and stack[-1][2] == token[2]:
                opening = stack.pop()
                if token[2] == 'aligned': pairs.append((opening, token))
        changed = False
        for opening, closing in pairs:
            left = re.search(r'(?:\\left)?([\[|])$', text[:opening.start()])
            right = re.match(r'(?:\\right)?([\]|])', text[closing.end():])
            if not left or not right or (left[1], right[1]) not in (('[', ']'), ('|', '|')): continue
            body = text[opening.end():closing.start()]
            rows = cells(body)
            if not rows or any(has_relation(cell) for row in rows for cell in row): continue
            width = min(map(len, rows))
            if any(len(row) != width for row in rows):
                if not all(not cell.strip() for row in rows for cell in row[width:]): continue
                body = r'\\'.join('&'.join(row[:width]) for row in rows)
                counts['empty_source_cells_removed'] += sum(len(row) - width for row in rows)
            layout = 'bmatrix' if left[1] == '[' else 'vmatrix'
            replacement = '\\begin{' + layout + '}' + body + '\\end{' + layout + '}'
            text = text[:left.start()] + replacement + text[closing.end() + right.end():]
            counts['matrices_fixed'] += 1
            changed = True
            break
        if not changed: return text
    raise ValueError('Unexpected matrix nesting/repetition')

MATRIX = re.compile(r'(?:\\left)?\[\\begin\{aligned\}((?:(?!\\(?:begin|end)\{)[\s\S])*?)\\end\{aligned\}(?:\\right)?\]')
BMATRIX = re.compile(r'\\begin\{bmatrix\}((?:(?!\\(?:begin|end)\{)[\s\S])*?)\\end\{bmatrix\}')
MATH = re.compile(r'\$\$[\s\S]*?\$\$|(?<!\\)\$(?!\$)(?:\\.|[^$\\])*?(?<!\\)\$')

def system(match):
    whole = match[0]; delimiter = '$$' if whole.startswith('$$') else '$'
    body = whole[len(delimiter):-len(delimiter)].strip()
    if body.startswith('{') and ';' in body:
        equations = body[1:].split(';')
        if 2 <= len(equations) <= 4 and all('=' in equation for equation in equations) and body.count('{') == body.count('}') + 1:
            return delimiter + r'\begin{cases}' + r' \\ '.join(equation.strip() for equation in equations) + r'\end{cases}' + delimiter
    for prefix, suffix in [
        (r'\begin{aligned}\{\begin{aligned}', r'\end{aligned}\end{aligned}'),
        (r'{\begin{aligned}', r'\end{aligned}'),
    ]:
        if body.startswith(prefix) and body.endswith(suffix):
            equations = body[len(prefix):-len(suffix)]
            if '=' in equations:
                return delimiter + r'\begin{cases}' + equations + r'\end{cases}' + delimiter
    return whole

forms, changes, unchanged = [], [], []
counts = collections.Counter()
for key in sorted(fields, key=lambda key: (*ownership.get(key, (4, 0)), *key)):
    entity, attr = key; old = fields[key]; new = old
    if entity == 17592186272048 and attr == 'question/worked-solution':
        # q-140306 solves (A + 2I)x = 0. Its first augmented matrix omits the
        # second row's RHS; the stated row operation produces a zero row only
        # when that missing entry is 0. The other RHS entries are also 0.
        missing = r'[\begin{aligned}-1 & -1 & 1 & 0 \\ 1 & 1 & -1 \\ 2 & 2 & -2 & 0\end{aligned}]'
        complete = r'[\begin{aligned}-1 & -1 & 1 & 0 \\ 1 & 1 & -1 & 0 \\ 2 & 2 & -2 & 0\end{aligned}]'
        assert new.count(missing) == 1
        new = new.replace(missing, complete)
        counts['missing_homogeneous_rhs_zero_restored'] += 1
    new, hats = re.subn(r'\\overset\{\^\}\{([^{}]*)\}', lambda match: r'\hat{' + match[1] + '}', new)
    counts['invalid_hat_accents_fixed'] += hats
    if entity in source_ids:
        for old_math, replacements in source[source_ids[entity]].items():
            if len(replacements) != 1: continue  # Source repeats a value with different styles.
            tokens = re.findall(r'\\[A-Za-z]+|\\.|[^\s]', old_math)
            pattern = re.compile(r'\s*'.join(re.escape(token) for token in tokens))
            new, count = pattern.subn(lambda _: next(iter(replacements)), new)
            counts['source_formulas_restored'] += count
    new = repair_matrices(new)
    if key in ownership:
        new = MATH.sub(system, new)
        if entity in augmented:
            def augment(match):
                if attr == 'question/worked-solution':
                    # A worked solution can show the coefficient matrix before
                    # its augmented matrix. Question-level context is too broad.
                    opening = new.rfind('$$', 0, match.start())
                    paragraph = new[:opening].rstrip().split('\n\n')[-1] if opening >= 0 else ''
                    if re.search(r'\bcoefficient\s+matrix\b', paragraph, re.I) and not re.search(r'\baugment', paragraph, re.I):
                        return match[0]
                rows = cells(match[1])
                if not rows or len(rows[0]) < 2 or any(len(row) != len(rows[0]) for row in rows): return match[0]
                columns = len(rows[0]); counts['augmented_dividers_restored'] += 1
                return r'\left[\begin{array}{' + 'c' * (columns - 1) + '|c}' + match[1] + r'\end{array}\right]'
            new = BMATRIX.sub(augment, new)
    if new != old:
        forms.append([kw('db/cas'), entity, kw(attr), old, new])
        changes.append({'entity': entity, 'attribute': attr, 'topic': ownership.get(key, (None, None))[1]})
        if key in ownership: topics[ownership[key][1]]['fields_repaired'] += 1
    elif r'[\begin{aligned}' in old:
        unchanged.append({'entity': entity, 'attribute': attr, 'text': old})

# Keep transport frames and CLI input files comfortably below their limits.
directory = HERE / 'batches'; directory.mkdir(exist_ok=True)
batches, batch, size = [], [], 0
def save_batch():
    global batch, size
    path = directory / f'{len(batches) + 1:03}.edn'; text = dumps(batch) + '\n'; path.write_text(text)
    digest = hashlib.sha256(text.encode()).hexdigest()
    batches.append({'file': str(path.resolve()), 'sha256': digest, 'request_key': 'matrix-capture-' + digest, 'fields': len(batch)})
    batch, size = [], 0
for form in forms:
    length = len(dumps(form).encode()) + 1
    if batch and size + length > 750_000: save_batch()
    batch.append(form); size += length
if batch: save_batch()
summary = {'database': 'math', 'source': ':application/ca-engine', 'endpoint': '/tmp/edb-math/writer.sock',
           'requested_topics_in_order': [{'id': eid, **topics[eid]} for eid in TOPICS],
           'fields_repaired': len(forms), 'entities_repaired': len({form[1] for form in forms}),
           'counts': counts, 'unchanged_candidates': len(unchanged), 'batches': batches}
(HERE / 'commit-intent.json').write_text(json.dumps(summary, indent=2) + '\n')
(HERE / 'changes.json').write_text(json.dumps(changes, indent=2) + '\n')
(HERE / 'skipped.json').write_text(json.dumps(unchanged, indent=2) + '\n')
print(json.dumps({key: value for key, value in summary.items() if key != 'batches'}, indent=2))
print('Batches:', len(batches))
