"""Conservative repair of the observed system wrappers; equation tokens stay intact."""
import re

ENV = re.compile(r'\\(begin|end)\{([^{}]+)\}')

def environment(text, start):
    first = ENV.match(text, start)
    if not first or first[1] != 'begin': return None
    stack = [first[2]]
    for token in ENV.finditer(text, first.end()):
        if token[1] == 'begin': stack.append(token[2])
        elif not stack or stack.pop() != token[2]: return None
        if not stack: return first.end(), token.start(), token.end()
    return None

def cells(body):
    rows, row, cell, depth, i, stack = [], [], [], 0, 0, []
    while i < len(body):
        token = ENV.match(body, i)
        if token:
            if token[1] == 'begin': stack.append(token[2])
            elif not stack or stack.pop() != token[2]: return None
            cell.append(token[0]); i = token.end(); continue
        if body[i:i + 2] == '\\\\' and not depth and not stack:
            row.append(''.join(cell).strip()); rows.append(row); row, cell = [], []
            i += 2; continue
        if body[i] == '\\' and i + 1 < len(body):
            cell.append(body[i:i + 2]); i += 2; continue
        if body[i] == '{': depth += 1
        elif body[i] == '}': depth -= 1
        elif body[i] == '&' and not depth and not stack:
            row.append(''.join(cell).strip()); cell = []; i += 1; continue
        if depth < 0: return None
        cell.append(body[i]); i += 1
    if depth or stack: return None
    row.append(''.join(cell).strip()); rows.append(row)
    return rows

def equation(row):
    while len(row) > 1 and not row[0]: row = row[1:]
    if len(row) == 2 and row[1].startswith('='): return row[0] + ' &' + row[1]
    if len(row) == 2 and row[0].endswith('='): return row[0][:-1].strip() + ' &=' + row[1]
    if len(row) == 3 and row[1] == '=': return row[0] + ' &=' + row[2]
    if len(row) == 2:
        first = equation([row[0]])
        if first: return first + ' && ' + row[1]
    if len(row) != 1 or r'\begin{' in row[0]: return None
    text, depth, i = row[0], 0, 0
    while i < len(text):
        if text[i] == '\\': i += 2; continue
        if text[i] == '{': depth += 1
        elif text[i] == '}': depth -= 1
        elif text[i] == '=' and not depth:
            return text[:i].strip() + ' &=' + text[i + 1:].strip()
        i += 1
    return None

def system(body):
    rows = cells(body)
    if not rows: return None
    equations = [equation(row) for row in rows]
    if not all(equations): return None
    return r'\left\{\begin{aligned}' + r' \\ '.join(equations) + r'\end{aligned}\right.'

def repair(text, include_cases=False):
    changes = []
    # This exact old capture has one literal opening brace, not a TeX group.
    pattern = re.compile(r'\\begin\{aligned\}\s*\{\s*(?=\\begin\{aligned\})')
    for match in list(pattern.finditer(text))[::-1]:
        inner = environment(text, match.end())
        if not inner: continue
        suffix = re.match(r'\s*\\end\{aligned\}', text[inner[2]:])
        if not suffix: continue
        replacement = system(text[inner[0]:inner[1]])
        if replacement: changes.append((match.start(), inner[2] + suffix.end(), replacement))
    for start, end, value in sorted(changes, reverse=True): text = text[:start] + value + text[end:]
    changes = []
    for match in re.finditer(r'\\\{\s*(?=\\begin\{aligned\})', text):
        if re.search(r'\\(?:left|[Bb]igg?)\s*$', text[:match.start()]): continue
        span = environment(text, match.end())
        if not span: continue
        replacement = system(text[span[0]:span[1]])
        if replacement: changes.append((match.start(), span[2], replacement))
    for start, end, value in sorted(changes, reverse=True): text = text[:start] + value + text[end:]
    changes = []
    # In old answer choices the visible brace was emitted as an unmatched
    # TeX group opener. A balanced ordinary group must remain a group.
    for match in re.finditer(r'(?<!\\)\{\s*(?=\\begin\{aligned\})', text):
        span = environment(text, match.end())
        if not span or text[span[2]:].lstrip().startswith('}'): continue
        replacement = system(text[span[0]:span[1]])
        if replacement: changes.append((match.start(), span[2], replacement))
    for start, end, value in sorted(changes, reverse=True): text = text[:start] + value + text[end:]
    if include_cases:
        changes = []
        for match in re.finditer(r'\\begin\{cases\}', text):
            span = environment(text, match.start())
            if not span: continue
            replacement = system(text[span[0]:span[1]])
            if replacement: changes.append((match.start(), span[2], replacement))
        for start, end, value in sorted(changes, reverse=True): text = text[:start] + value + text[end:]
    return text

def legacy_choice(text):
    """The seed import also flattened system rows to semicolons in math choices."""
    if not text.startswith('{') or text.endswith('}') or ';' not in text: return text
    body, rows, start, depth, i = text[1:], [], 0, 0, 0
    while i < len(body):
        if body[i] == '\\': i += 2; continue
        if body[i] == '{': depth += 1
        elif body[i] == '}': depth -= 1
        elif body[i] == ';' and not depth:
            rows.append(body[start:i].strip()); start = i + 1
        if depth < 0: return text
        i += 1
    if depth: return text
    rows.append(body[start:].strip())
    return system(r' \\ '.join(rows)) or text
