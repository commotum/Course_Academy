"""Shared Course Academy math-content convention for capture and generators.

Prose uses $inline$ / $$display$$; math answers contain bare TeX. Matrices use
matrix environments, augmented matrices carry explicit array column rules,
and equation systems use a scalable brace with equals-aligned rows.
"""
import copy
import functools
import html
import re

FORMAT_VERSION = 'course-academy-tex-v1'

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

def _equality_position(text):
    """Find an equality outside groups and visible parentheses/brackets."""
    braces, delimiters, i = 0, [], 0
    while i < len(text):
        if text[i] == '\\': i += 2; continue
        if text[i] == '{': braces += 1
        elif text[i] == '}': braces -= 1
        elif not braces:
            if text[i] in '([': delimiters.append(text[i])
            elif text[i] in ')]':
                if not delimiters or delimiters.pop() != {')': '(', ']': '['}[text[i]]: return None
            elif text[i] == '=' and not delimiters: return i
        i += 1
    return None


def _whole_equation_expression(text):
    """An equation in parentheses, optionally multiplied as a whole.

    Splitting its equality into alignment cells would leave a scalable fence
    unpaired or make a multiplier appear to apply to just the right-hand side.
    """
    opening = re.match(r'(?:\\left\s*)?\(', text)
    if not opening: return False
    braces, parentheses, i = 0, 1, opening.end()
    while i < len(text):
        if text[i] == '\\': i += 2; continue
        if text[i] == '{': braces += 1
        elif text[i] == '}': braces -= 1
        elif not braces:
            if text[i] == '(': parentheses += 1
            elif text[i] == ')':
                parentheses -= 1
                if not parentheses:
                    inner = re.sub(r'\\right\s*$', '', text[opening.end():i]).strip()
                    suffix = text[i + 1:].strip()
                    position = _equality_position(inner)
                    return (position is not None and bool(inner[:position].strip())
                            and bool(inner[position + 1:].strip())
                            and (not suffix or bool(re.fullmatch(r'\\(?:cdot|times)\s*\S[\s\S]*', suffix))))
        if braces < 0: return False
        i += 1
    return False


def _system_row(row):
    """Recover an equation and optional annotation from alignment cells."""
    while len(row) > 1 and not row[0]: row = row[1:]
    annotation, aligned = None, None
    if len(row) == 4 and not row[2]: row, annotation = row[:2], row[3]
    elif len(row) == 3 and not row[1]: row, annotation = row[:1], row[2]
    if len(row) == 2 and row[1].startswith('='):
        text = ''.join(row)
        aligned = row[0] + ' &' + row[1]
    elif len(row) == 2 and row[0].endswith('='):
        text = ''.join(row)
        aligned = row[0][:-1].strip() + ' &=' + row[1]
    elif len(row) == 3 and row[1] == '=':
        text = ''.join(row)
        aligned = row[0] + ' &=' + row[2]
    elif len(row) == 2 and annotation is None: text, annotation = row
    elif len(row) == 1: text = row[0]
    else: return None
    if r'\begin{' in text: return None
    position = _equality_position(text)
    if position is not None and text[:position].strip() and text[position + 1:].strip():
        if aligned is None: aligned = text[:position].strip() + ' &=' + text[position + 1:].strip()
    elif _whole_equation_expression(text): aligned = None
    else: return None
    return text, annotation, aligned


def equation(row):
    parsed = _system_row(row)
    if not parsed or parsed[2] is None: return None
    return parsed[2] + (' && ' + parsed[1] if parsed[1] is not None else '')

def system(body):
    rows = cells(body)
    if not rows: return None
    parsed = [_system_row(row) for row in rows]
    if not all(parsed): return None
    intact = any(row[2] is None for row in parsed)
    equations = [(('&' + text) if intact else aligned) + (' && ' + annotation if annotation is not None else '')
                 for text, annotation, aligned in parsed]
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

def legacy_system_rows(text):
    """Recognize a flattened, unclosed system without reinterpreting a set.

    Keep row text verbatim: a suffix such as ``0(1)`` can be multiplication or
    a captured equation label, and only source evidence can distinguish them.
    """
    text = str(text).strip()
    opening = re.match(r'(?:\\\{|\{)', text)
    if not opening or ';' not in text: return None
    body, rows, start, depth, delimiters, i = text[opening.end():], [], 0, 0, [], 0
    while i < len(body):
        if body[i] == '\\':
            # An escaped closing brace makes this a closed set, not the
            # historical missing-right-fence system representation.
            if body[i:i + 2] == r'\}' and not depth and not delimiters: return None
            i += 2; continue
        if body[i] == '{': depth += 1
        elif body[i] == '}': depth -= 1
        elif not depth:
            if body[i] in '([': delimiters.append(body[i])
            elif body[i] in ')]':
                if not delimiters or delimiters.pop() != {')': '(', ']': '['}[body[i]]: return None
            elif body[i] == ';' and not delimiters:
                rows.append(body[start:i].strip()); start = i + 1
        if depth < 0: return None
        i += 1
    if depth or delimiters: return None
    rows.append(body[start:].strip())
    if len(rows) < 2 or not all(_system_row([row]) for row in rows): return None
    return rows


def legacy_choice(text):
    """The old extractor flattened system rows in prompts, solutions and choices."""
    rows = legacy_system_rows(text)
    return system(r' \\ '.join(rows)) if rows else text


MATH = re.compile(r'\\\[[\s\S]*?\\\]|\\\([\s\S]*?\\\)|\$\$[\s\S]*?\$\$|(?<!\\)\$(?!\$)(?:\\[\s\S]|[^$\\])*?(?<!\\)\$')


def matrix_tex(rows, *, augmented=False):
    rows = [list(map(str, row)) for row in rows]
    if not rows or not rows[0] or len({len(row) for row in rows}) != 1:
        raise ValueError('A matrix must have rectangular, nonempty rows')
    body = r' \\ '.join(' & '.join(row) for row in rows)
    if augmented:
        if len(rows[0]) < 2: raise ValueError('An augmented matrix needs coefficients and a right-hand side')
        return r'\left[\begin{array}{' + 'c' * (len(rows[0]) - 1) + '|c}' + body + r'\end{array}\right]'
    return r'\begin{bmatrix}' + body + r'\end{bmatrix}'


def matrix_operands(expressions, *, stacked=False):
    """Centered, independently wrapping given matrices; expressions are bare TeX."""
    expressions = list(expressions)
    if not expressions or any(not str(value).strip() or '$' in str(value) for value in expressions):
        raise ValueError('Matrix operands require nonempty, delimiter-free TeX')
    classes = 'matrix-operands matrix-operands-stacked' if stacked else 'matrix-operands'
    return '<div class="' + classes + '">\n' + '\n'.join(
        '<div>$' + str(value) + '$</div>' for value in expressions
    ) + '\n</div>'


def matrix_answer(expression, rows):
    """A borderless rectangular answer matrix with external brackets and label.

    Cells contain bare TeX or an exact {{answer-field-key}} placeholder. Field
    identities, row order, supplied entries, and grading are owned by the caller.
    """
    rows = [list(map(str, row)) for row in rows]
    if not expression.strip() or '$' in expression:
        raise ValueError('Matrix answer label requires delimiter-free TeX')
    if not rows or not rows[0] or len({len(row) for row in rows}) != 1 or any(not cell.strip() for row in rows for cell in row):
        raise ValueError('A matrix answer must have rectangular, nonempty cells')
    def entry(value):
        escaped = html.escape(value, quote=False)
        return escaped if re.fullmatch(r'\{\{(?:answer-field:)?[^{}]+\}\}', value) else '$' + value + '$'
    return ('<div class="matrix-answer">\n'
            '<span class="matrix-answer-label">$' + expression + '=$</span>\n'
            '<div class="matrix-answer-brackets">\n'
            '<table aria-label="Answer matrix"><tbody>\n' + '\n'.join(
                '<tr>' + ''.join('<td>' + entry(value) + '</td>' for value in row) + '</tr>' for row in rows
            ) + '\n</tbody></table>\n</div>\n</div>')


def system_tex(equations, *, annotations=None):
    r"""Canonical system rows, with optional equation labels or row operations.

    Annotations occupy their own column. Whole-equation expressions such as
    ``(x+y=1)\cdot(-1)`` stay intact, with all rows left aligned in that system.
    """
    equations = [str(row).strip() for row in equations]
    if not equations or any(not row or '$' in row or r'\\' in row for row in equations):
        raise ValueError('A system needs nonempty, delimiter-free equation rows')
    if annotations is not None:
        annotations = ['' if annotation is None else str(annotation).strip() for annotation in annotations]
        if len(annotations) != len(equations): raise ValueError('A system needs one annotation per equation')
        if any('$' in annotation or r'\\' in annotation or '&' in annotation for annotation in annotations):
            raise ValueError('System annotations require delimiter-free TeX')
        equations = [row + (' & ' + annotation if annotation else '')
                     for row, annotation in zip(equations, annotations)]
    value = system(r' \\ '.join(equations))
    if value is None: raise ValueError('A system needs explicit equations')
    return value


def _legacy_commands(text):
    for command, layout in [('matrix', 'matrix'), ('eqalign', 'aligned')]:
        offset = 0
        while match := re.search(r'\\' + command + r'\s*\{', text[offset:]):
            start = offset + match.start(); opening = offset + match.end() - 1
            depth, i = 1, opening + 1
            while i < len(text) and depth:
                if text[i] == '\\' and i + 1 < len(text) and text[i + 1] in '\\{}': i += 2; continue
                if text[i] == '{': depth += 1
                elif text[i] == '}': depth -= 1
                i += 1
            if depth: raise ValueError('Unclosed legacy TeX ' + command)
            body = text[opening + 1:i - 1]
            body = re.sub(r'\\cr\b', lambda _: r'\\', body)
            body = re.sub(r'(?<!\\)\\[ \t]*\r?\n', lambda _: r'\\' + '\n', body)
            # Legacy source SVG titles can wrap a row separator in a span,
            # leaving one backslash before its optional vertical spacing.
            # This is a row break only inside the legacy layout command and
            # with a concrete TeX length; ordinary math delimiters stay invalid.
            body = re.sub(r'(?<!\\)\\(?=\[\s*[+-]?(?:\d+(?:\.\d*)?|\.\d+)\s*'
                          r'(?:pt|pc|in|bp|cm|mm|dd|cc|sp|ex|em)\s*\])',
                          lambda _: r'\\', body)
            body = re.sub(r'\\\\\s*$', '', body)
            replacement = r'\begin{' + layout + '}' + body + r'\end{' + layout + '}'
            text = text[:start] + replacement + text[i:]
            offset = start + len(r'\begin{' + layout + '}')
    return text


def _matrix_layouts(text):
    for _ in range(256):
        stack, pairs = [], []
        for token in ENV.finditer(text):
            if token[1] == 'begin': stack.append(token)
            elif stack and stack[-1][2] == token[2]:
                opening = stack.pop()
                if token[2] in ['aligned', 'matrix']: pairs.append((opening, token))
        changed = False
        for opening, closing in pairs:
            left = re.search(r'(?:\\left\s*)?([\[|(])\s*$', text[:opening.start()])
            right = re.match(r'\s*(?:\\right\s*)?([\]|)])', text[closing.end():])
            if not left or not right or (left[1], right[1]) not in [('[', ']'), ('(', ')'), ('|', '|')]: continue
            body = text[opening.end():closing.start()]; rows = cells(body)
            if not rows or any(_system_row([cell]) for row in rows for cell in row): continue
            width = min(map(len, rows))
            if any(len(row) != width for row in rows):
                if not all(not cell for row in rows for cell in row[width:]): continue
                body = r' \\ '.join(' & '.join(row[:width]) for row in rows)
            layout = {'[': 'bmatrix', '(': 'pmatrix', '|': 'vmatrix'}[left[1]]
            text = text[:left.start()] + r'\begin{' + layout + '}' + body + r'\end{' + layout + '}' + text[closing.end() + right.end():]
            changed = True; break
        if not changed: return text
    raise ValueError('Excessive matrix nesting')


def _label_row_spacing(text):
    length = r'\[\s*[+-]?(?:\d+(?:\.\d*)?|\.\d+)\s*(?:pt|pc|in|bp|cm|mm|dd|cc|sp|ex|em)\s*\]'
    def repair_spacing(value):
        return re.sub(r'(?<!\\)\\(?=' + length + ')', lambda _: r'\\', value)
    if re.fullmatch(r'(?:\\ )?\\' + length, text):
        return repair_spacing(text)
    # Restrict repairs to the explicit multiline label, leaving arbitrary
    # malformed aligned environments subject to the normal validation errors.
    for match in list(re.finditer(r'\\substack\s*\{', text))[::-1]:
        depth, end = 1, match.end()
        while end < len(text) and depth:
            if text[end] == '\\' and end + 1 < len(text):
                end += 2
                continue
            depth += (text[end] == '{') - (text[end] == '}')
            end += 1
        if depth == 0:
            text = text[:match.start()] + repair_spacing(text[match.start():end]) + text[end:]
    return text


def normalize_tex(value):
    text = str(value).strip()
    if MATH.fullmatch(text):
        size = 2 if text.startswith(('$$', r'\[', r'\(')) else 1
        text = text[size:-size].strip()
    # Archived SVG titles spell optional row spacing with one backslash,
    # including in substack labels and standalone spacing formulas. A concrete
    # TeX length distinguishes this from an actual display-math delimiter.
    text = _label_row_spacing(text)
    text = text.replace(r'\lbrack', '[').replace(r'\rbrack', ']')
    text = text.replace(r'\lbrace', r'\{').replace(r'\rbrace', r'\}')
    text = _matrix_layouts(_legacy_commands(text))
    # Arrays retain explicit column rules; make their existing fences scalable.
    for match in list(re.finditer(r'(?<!\\left)\[\s*(?=\\begin\{array\})', text))[::-1]:
        span = environment(text, match.end())
        if not span: continue
        closing = re.match(r'\s*\]', text[span[2]:])
        if closing:
            text = text[:match.start()] + r'\left[' + text[match.end():span[2]] + r'\right]' + text[span[2] + closing.end():]
    text = repair(text, include_cases=True)
    text = legacy_choice(text)
    changes = []
    for match in re.finditer(r'\\left\\\{\s*(?=\\begin\{aligned\})', text):
        span = environment(text, match.end())
        if not span: continue
        closing = re.match(r'\s*\\right\s*\.', text[span[2]:])
        if not closing: continue
        normalized = system(text[span[0]:span[1]])
        end = span[2] + closing.end()
        # Canonical alignment needs no incidental whitespace rewrite. In
        # particular, preserve existing empty annotation cells in other lessons.
        if normalized and re.sub(r'\s+', '', normalized) != re.sub(r'\s+', '', text[match.start():end]):
            changes.append((match.start(), end, normalized))
    for start, end, new in sorted(changes, reverse=True): text = text[:start] + new + text[end:]
    changes = []
    for match in re.finditer(r'\\begin\{aligned\}', text):
        span = environment(text, match.start())
        if not span: continue
        rows = cells(text[span[0]:span[1]])
        if rows and all(len(row) == 1 and equation(row) for row in rows):
            changes.append((match.start(), span[2], r'\begin{aligned}' + r' \\ '.join(equation(row) for row in rows) + r'\end{aligned}'))
    for start, end, new in sorted(changes, reverse=True): text = text[:start] + new + text[end:]
    # A redundant outer equation table adds no mathematical structure.
    for _ in range(32):
        changed = False
        for match in re.finditer(r'\\begin\{aligned\}', text):
            span = environment(text, match.start())
            if not span: continue
            body = text[span[0]:span[1]].strip()
            if body.startswith(r'\left\{\begin{aligned}') and body.endswith(r'\end{aligned}\right.'):
                text = text[:match.start()] + body + text[span[2]:]; changed = True; break
        if not changed: break
    return text


def normalize_source_tex(value):
    """Prepare a complete source TeX title before HTML whitespace collapsing.

    Comments depend on physical line endings. Remove them while those endings
    are present, retaining escaped percent signs, then canonicalize legacy
    matrix row breaks. Existing authored Markdown does not pass this boundary.
    """
    value = str(value)
    parts, index = [], 0
    while index < len(value):
        if value[index] == '\\' and index + 1 < len(value):
            parts.append(value[index:index + 2])
            index += 2
        elif value[index] == '%':
            while index < len(value) and value[index] not in '\r\n':
                index += 1
        else:
            parts.append(value[index])
            index += 1
    return normalize_tex(''.join(parts))


def normalize_prose(value):
    def replace(match):
        whole = match[0]; display = whole.startswith(('$$', r'\['))
        normalized = normalize_tex(whole)
        return ('$$\n' + normalized + '\n$$') if display else ('$' + normalized + '$')
    text = MATH.sub(replace, str(value))
    # Browser indentation is not a Markdown code-block instruction.
    if '{{field-' in text:
        text = re.sub(r'(?m)^[ \t]{4,}(?=\$(?!\$))', '', text)
    return text


def validate_tex(value):
    """Validate structural invariants; the UI's MathJax checks rendering."""
    text = str(value); depth = 0; stack = []
    if legacy_system_rows(text):
        raise ValueError('Flattened equation system; use explicit system rows')
    for token in re.findall(r'\\(?:begin|end)\{[^{}]+\}|\\[A-Za-z]+|\\.|.', text, re.S):
        env = ENV.fullmatch(token)
        if env:
            if env[1] == 'begin': stack.append(env[2])
            elif not stack or stack.pop() != env[2]: raise ValueError('Mismatched TeX environment')
        elif token == '{': depth += 1
        elif token == '}': depth -= 1
        if depth < 0: raise ValueError('Unmatched closing TeX brace')
        if token in [r'\matrix', r'\eqalign']: raise ValueError('Legacy TeX layout command')
        if token in [r'\[', r'\]', r'\(', r'\)']:
            raise ValueError('Nested math delimiter in a TeX expression')
        if token == r'\=':
            raise ValueError('Unsupported TeX equality command; use =')
        if token == '$': raise ValueError('Math fields must not contain nested dollar delimiters')
    if depth or stack: raise ValueError('Unclosed TeX group or environment')
    for match in re.finditer(r'\\begin\{(bmatrix|pmatrix|vmatrix|Bmatrix|Vmatrix|matrix)\}', text):
        span = environment(text, match.start())
        if not span: continue
        body = text[span[0]:span[1]]
        if re.search(r'\\(?:multicolumn|hdotsfor)\b', body): continue
        rows = cells(body)
        if not rows or len({len(row) for row in rows}) != 1:
            raise ValueError('Ragged matrix rows')
    return text


def validate_prose(value):
    text = str(value)
    for match in MATH.finditer(text):
        size = 2 if match[0].startswith(('$$', r'\[', r'\(')) else 1
        validate_tex(match[0][size:-size])
    outside = MATH.sub('', text)
    if re.search(r'(?<!\\)\$', outside): raise ValueError('Unpaired math dollar delimiter')
    return text


def validate_generated_record(record):
    question = record['question']
    for key in [':question/problem', ':question/worked-solution']:
        value = question[key]
        validate_prose(value)
        if normalize_prose(value) != value: raise ValueError('Noncanonical math content in ' + key)
    for field in question.get(':question/answer-fields', []):
        for answer in field.get(':answer-field/choices', []):
            value = answer[':answer/value']
            if answer[':answer/type'] == ':answer.type/math':
                validate_tex(value)
                if normalize_tex(value) != value: raise ValueError('Noncanonical math answer')
            elif answer[':answer/type'] == ':answer.type/text': validate_prose(value)
    record.setdefault('generation', {})['math_format'] = FORMAT_VERSION
    return record


def checked_math_content(generator):
    """Require every public generator call to satisfy the shared UI contract."""
    @functools.wraps(generator)
    def checked(*args, **kwargs):
        return validate_generated_record(generator(*args, **kwargs))
    return checked


def normalize_capture_question(question):
    result = copy.deepcopy(question)
    for name in ['problem', 'worked_solution']:
        if result.get(name): result[name] = validate_prose(normalize_prose(result[name]))
    for field in result.get('answer_fields', []):
        original_correct = field.get('correct_value')
        for choice in field.get('choices', []):
            original_value = choice.get('value')
            if choice.get('type') == 'math': choice['value'] = validate_tex(normalize_tex(choice['value']))
            elif choice.get('type') == 'text': choice['value'] = validate_prose(normalize_prose(choice['value']))
            if original_correct is not None and original_value == original_correct:
                field['correct_value'] = choice['value']
            if choice.get('feedback') is not None:
                choice['feedback'] = validate_prose(normalize_prose(choice['feedback']))
    return result
