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


def markdown_emphasis(body, marker):
    """Convert an HTML emphasis body without putting whitespace inside markers.

    HTML permits padded and empty emphasis elements; Markdown does not. Keep
    the padding outside the delimiters so adjacent words retain their spacing.
    Only use this for an explicit HTML emphasis node, never arbitrary Markdown.
    """
    core = body.strip()
    if not core:
        return body
    start = len(body) - len(body.lstrip())
    end = len(body.rstrip())
    return body[:start] + marker + body[start:end] + marker + body[end:]


def mathml_ruled_table(rows, attributes):
    """Preserve explicit MathML table rules and alignment as a TeX array.

    A table with no rules is outside this helper's scope: its caller must
    distinguish equation alignment, matrices and other layouts. Short MathML
    attribute lists repeat their last value. Missing cells remain empty.
    """
    def values(name, default='none'):
        return str(attributes.get(name) or default).split()

    rules = {name: values(name) for name in ('columnlines', 'rowlines', 'frame')}
    if all(v == 'none' for items in rules.values() for v in items):
        return None
    for name, items in rules.items():
        if any(v not in ('none', 'solid') for v in items):
            raise ValueError('Unsupported MathML table ' + name)
    align = values('columnalign', 'center')
    if any(v not in ('left', 'right', 'center') for v in align):
        raise ValueError('Unsupported MathML table columnalign')
    if not rows or not max(map(len, rows)):
        raise ValueError('Empty ruled MathML table')
    width = max(map(len, rows))
    at = lambda items, index: items[min(index, len(items) - 1)]
    frame = rules['frame'][0] == 'solid'
    if not frame and not any(at(rules['columnlines'], i) == 'solid' for i in range(width - 1)) \
            and not any(at(rules['rowlines'], i) == 'solid' for i in range(len(rows) - 1)):
        return None  # Extra attribute-list entries do not create columns/rows.
    columns = '|' if frame else ''
    for i in range(width):
        columns += {'left': 'l', 'right': 'r', 'center': 'c'}[at(align, i)]
        if (i < width - 1 and at(rules['columnlines'], i) == 'solid') or (i == width - 1 and frame):
            columns += '|'
    body = r'\hline ' if frame else ''
    for i, row in enumerate(rows):
        body += ' & '.join(row + [''] * (width - len(row)))
        if i < len(rows) - 1:
            body += r' \\ ' + (r'\hline ' if at(rules['rowlines'], i) == 'solid' else '')
    if frame:
        body += r' \\ \hline'
    return r'\begin{array}{' + columns + '}' + body + r'\end{array}'

def mathml_unruled_table(rows, attributes):
    """Keep explicit 1em column layout on an unfenced source data table.

    Callers handle fences and ruled tables first. Equation alignments normally
    declare zero spacing between their right/left pairs and stay aligned.
    """
    spacing = str(attributes.get('columnspacing') or '').split()
    if not spacing or any(value != '1em' for value in spacing):
        return None
    if not rows or max(map(len, rows)) < 2:
        return None
    alignment = str(attributes.get('columnalign') or 'center').split()
    if not alignment or any(value not in ('left', 'center', 'right') for value in alignment):
        raise ValueError('Unsupported MathML table columnalign')
    width = max(map(len, rows))
    columns = ''.join({'left': 'l', 'center': 'c', 'right': 'r'}[
        alignment[min(i, len(alignment) - 1)]] for i in range(width))
    body = r' \\ '.join(' & '.join(row + [''] * (width - len(row))) for row in rows)
    return r'\begin{array}{' + columns + '}' + body + r'\end{array}'


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


MATH = re.compile(r'(?<!\\)\\\[[\s\S]*?\\\]|(?<!\\)\\\([\s\S]*?\\\)|\$\$[\s\S]*?\$\$|(?<!\\)\$(?!\$)(?:\\[\s\S]|[^$\\])*?(?<!\\)\$')


def source_multiplication_tex(source):
    """Recover the explicit digit columns in an archived MA arithmetic table.

    Unlike ordinary algebra, these vertical bars separate digit columns. Check
    every supplied result/carry against integer arithmetic before rendering.
    Unsupported source layouts are rejected rather than converted as matrices.
    """
    parts = [p.strip() for p in source.split(';')]
    carries = []
    if parts and parts[0].startswith('_('):
        carries = re.findall(r'_\((\d)\)', parts.pop(0))
    if len(parts) < 3 or not re.fullmatch(r'\d(?:\|\d)+', parts[0]) or not re.fullmatch(r'[×⋅]\|\d', parts[1]):
        raise ValueError('Unsupported source multiplication layout')
    digits = parts[0].split('|');factor = int(parts[1][-1]);product = str(int(''.join(digits)) * factor)
    tokens = parts[2].split('|');result=[];caption=[]
    for i,t in enumerate(tokens):
        clean = re.sub(r'\[/?math\]', '', t).strip()
        if re.fullmatch(r'\d|\\phantom\{[\di]\}|\\color\{(?:red|blue)\}\d', clean):
            result.append(clean)
        else:
            caption = ['|'.join(tokens[i:])] + parts[3:];break
    if not result or len(result)>len(product):raise ValueError('Invalid source product width')
    for shown,actual in zip(result,product[-len(result):]):
        if r'\phantom{' not in shown and re.sub(r'\\color\{[^}]+\}', '', shown)!=actual:
            raise ValueError('Source multiplication digit disagrees with arithmetic')
    carry=0;expected=[]
    for digit in reversed(digits):
        carry=(int(digit)*factor+carry)//10;expected.append(str(carry))
    expected=list(reversed(expected[:-1]))
    if carries and carries!=expected[-len(carries):]:raise ValueError('Source multiplication carries disagree with arithmetic')
    width=len(product)
    def row(values,sign=''):
        return ' & '.join([sign]+['']*(width-len(values))+values)
    rows=[]
    if carries:rows.append(row([r'\scriptstyle '+v for v in carries]+['']))
    rows += [row(digits),row([str(factor)],r'\times'),r'\hline '+row(result)]
    tex=r'\begin{array}{'+'r'*(width+1)+'}'+r' \\ '.join(rows)+r'\end{array}'
    if caption:
        body='; '.join(caption).replace('×',r'\times ').replace('−','-')
        body=body.replace('and',r'\quad\text{and}\quad ')
        body=re.sub(r'\b(Carry|Write):',lambda m:r'\quad\text{'+m[1]+r': }',body)
        tex+=r'\qquad '+body
    return tex


def normalize_source_arithmetic(value):
    text=str(value);offset=0
    while (start:=text.find('[MATH:',offset))>=0:
        depth,end=1,start+6
        while end<len(text) and depth:
            depth+=(text[end]=='[')-(text[end]==']');end+=1
        if depth:raise ValueError('Unclosed source math placeholder')
        body=text[start+6:end-1].strip()
        if not re.search(r';\s*[×⋅]\|\d',body):
            offset=end;continue
        replacement='$$\n'+source_multiplication_tex(body)+'\n$$'
        text=text[:start]+replacement+text[end:];offset=start+len(replacement)
    return text


def _normalize_math_boundary_pass(value, *, wrap_environments=False):
    """Recover explicit legacy math boundaries without changing equations.

    This is deliberately narrower than normalize_tex: authored content, answer
    identities, and algebra are untouched. Raw source environments must survive
    Markdown before MathJax can see them. Historical currency glyphs and empty
    table cells must not become display-math delimiters.
    """
    text = str(value)
    # An empty source formula was sometimes prepended to an ordinary prompt.
    # Restrict this repair to explicit prose openers, never a TeX expression.
    text = re.sub(r'\A\$\$[ \t]*\n\s*(?=(?:Find|If|The|Calculate|Evaluate|First|Given|Consider|Note|Which)\b|[A-Z][a-z]+ (?:has|is|uses|buys)\b)', '', text)
    # The legacy dollar-to-[math] substitution also touched escaped currency.
    text = re.sub(r'\\\[/?math\]', lambda _: r'\$', text)
    protected = [(m.start(), m.end()) for m in MATH.finditer(text)]
    for match in reversed(list(re.finditer(r'\$-\s*\$((?:\\,\s*)*\d[^$\n]*)\$', text))):
        if not any(start < match.start() < end for start, end in protected):
            text = text[:match.start()] + '$-' + r'\$' + match[1] + '$' + text[match.end():]
    text = re.sub(r'\$-\$\$(?=\s*\{\{)', lambda _: '$-$' + r'\$', text)
    text = re.sub(r'\(\$(?=\))', lambda _: '(' + r'\$', text)
    if re.search(r'\b(?:investment|savings|account|money|pay|dollars|price|profit|cost|charge|paid|worth|bank|policy)\b', text, re.I):
        text = re.sub(r'(\$\d[\d.,{}]*\\(?:cdot|times)\s*)\$(\d[^$=\n]*=)\$(\d[^$\n]*)\$',
                      lambda m: m[1] + r'\$' + m[2] + r'\$' + m[3] + '$', text)
        text = re.sub(r'(?<![\\$])(\$(?:\\.|[^$\\\n])*=\s*)\$((?:\\,\s*)*\d[^$\n]*)\$',
                      lambda m: m[1] + r'\$' + m[2] + '$', text)
    text = re.sub(r'\\\$(?= and \$[01]\s*\\land)', '$', text)
    protected = [(m.start(), m.end()) for m in MATH.finditer(text)]
    for match in reversed(list(re.finditer(r'(?<!\\)\$(?=\s*\{\{[^{}]+\}\}\$(?:\\[,!])+\$)', text))):
        if not any(start < match.start() < end for start, end in protected):
            text = text[:match.start()] + r'\$' + text[match.end():]
    # A source math box containing a dollar sign was wrapped once more in $...$.
    currency_or_math = re.compile(
        r'(?<!\\)\\\[[\s\S]*?\\\]|(?<!\\)\\\([\s\S]*?\\\)|'
        r'(?<!\\)\$\$(?P<currency>(?:\\,\s*)*\d[^$\n]*?)(?<!\\)\$(?!\$)|'
        r'\$\$[\s\S]*?\$\$|(?<!\\)\$(?!\$)(?:\\[\s\S]|[^$\\])*?(?<!\\)\$')
    text = currency_or_math.sub(lambda m: ('$' + r'\$' + m['currency'] + '$')
                                if m['currency'] is not None else m[0], text)
    text = re.sub(r'(?m)(\|[ \t]*)\$\$(?=[ \t]*\|)', lambda m: m[1], text)
    text = re.sub(r'(?m)(\|[ \t]*)\$\$\?(?=[ \t]*\|)', lambda m: m[1] + '?', text)
    text = re.sub(r'(?m)(\|[ \t]*)\$\$([.:])(?=[ \t]*\|)', lambda m: m[1] + m[2], text)
    text = re.sub(r'(\{\{[^{}]+\}\}[ \t\n]*)\$\$(?=[,;:])', lambda m: m[1], text)
    text = re.sub(r'\A\$\$[ \t]*\n[ \t\n]*(\$(?!\$)[^$\n]+\$)(?=\n|$)',
                  lambda m: '$$\n' + m[1][1:-1] + '\n$$', text)
    # Triple dollars on their own lines are duplicated display wrappers. Other
    # triple-dollar uses in this corpus are a currency glyph beside a widget or
    # in a table header; do not reinterpret general unmatched dollars.
    text = re.sub(r'(?m)^[ \t]*\${3}[ \t]*$', '$$', text)
    text = re.sub(r'\${3,}(?=[ \t\n]*\{\{)', lambda _: r'\$', text)
    text = re.sub(r'\${3}(?=[ \t]*(?:\)|\(\$))', lambda _: r'\$', text)
    # Adjacent closing inline/opening display delimiters need a paragraph break.
    text = re.sub(r'(?<=[^$\n])\${3}(?=\n\\)', '$\n\n$$', text)

    def inner_markers(match):
        return re.sub(r'\[/?(?:math|latex|tex|displaymath)\]', '', match[0])
    text = MATH.sub(inner_markers, text)
    def bracket_math(match):
        body = match[2]
        display = match[1] == 'displaymath' or r'\begin{' in body
        return ('$$\n' + body.strip() + '\n$$') if display else '$' + body.strip() + '$'
    text = re.sub(r'\[(math|latex|tex|displaymath)\]([\s\S]*?)\[/\1\]', bracket_math, text)

    # Legacy flattened HTML tables used TeX row breaks between separately
    # delimited formulas. A break outside math is HTML, not part of the next
    # dollar opener. Do not touch any row break inside a recognized expression.
    pieces, offset = [], 0
    for match in MATH.finditer(text):
        pieces += [re.sub(r'\\\\(?=\$)', '<br>', text[offset:match.start()]), match[0]]
        offset = match.end()
    pieces.append(re.sub(r'\\\\(?=\$)', '<br>', text[offset:]))
    text = ''.join(pieces)

    spans = [(m.start(), m.end()) for m in MATH.finditer(text)]
    changes, consumed = [], -1
    for match in ENV.finditer(text):
        if not wrap_environments:
            break
        if match[1] != 'begin' or match.start() < consumed:
            continue
        if any(start <= match.start() < end for start, end in spans):
            continue
        span = environment(text, match.start())
        if not span:
            continue
        name = match[2]
        if name not in {'align', 'align*', 'aligned', 'alignedat', 'alignat', 'alignat*',
                        'eqnarray', 'eqnarray*', 'gather', 'gather*', 'gathered',
                        'equation', 'equation*', 'multline', 'multline*', 'split',
                        'matrix', 'bmatrix', 'pmatrix', 'vmatrix', 'Bmatrix', 'Vmatrix',
                        'smallmatrix', 'cases', 'array'}:
            continue
        tex = text[match.start():span[2]]
        mapping = {'align': 'aligned', 'align*': 'aligned', 'alignat': 'alignedat',
                   'alignat*': 'alignedat', 'eqnarray': 'aligned', 'eqnarray*': 'aligned',
                   'gather': 'gathered', 'gather*': 'gathered', 'equation': 'gathered',
                   'equation*': 'gathered', 'multline': 'gathered', 'multline*': 'gathered',
                   'split': 'aligned'}
        if name in mapping:
            tex = r'\begin{' + mapping[name] + '}' + text[span[0]:span[1]] + r'\end{' + mapping[name] + '}'
        tex = _legacy_commands(tex)
        # Remove only a redundant whole inner alignment, keeping its rows exact.
        body_match = re.match(r'\\begin\{aligned\}\s*(?=\\begin\{aligned\})', tex)
        if body_match:
            inner = environment(tex, body_match.end())
            if inner and re.fullmatch(r'\s*\\end\{aligned\}', tex[inner[2]:]):
                tex = tex[body_match.end():inner[2]]
        changes.append((match.start(), span[2], '$$\n' + tex + '\n$$'))
        consumed = span[2]
    for start, end, replacement in reversed(changes):
        text = text[:start] + replacement + text[end:]

    # Fix only explicit numeric percentage glyphs, not arbitrary TeX comments.
    # The MathML converters emitted e.g. 12%=12/100, silently commenting out
    # the rest of that formula in MathJax.
    def percentages(match):
        value = re.sub(r'(?<=\d)(?<!\\)%|(?<!\\)%(?=\\,error\b)', lambda _: r'\%', match[0])
        return re.sub(r'(?<!\\)#(?=\s+[A-Za-z])', lambda _: r'\#', value)
    text = MATH.sub(percentages, text)
    def spacing(match):
        whole = match[0]
        size = 2 if whole.startswith(('$$', r'\[', r'\(')) else 1
        body = whole[size:-size]
        fixed = _label_row_spacing(body)
        length = r'\[\s*[+-]?(?:\d+(?:\.\d*)?|\.\d+)\s*(?:pt|pc|in|bp|cm|mm|dd|cc|sp|ex|em)\s*\]'
        gap = re.compile(r'(?<!\\)\\(' + length + ')')
        if gap.search(fixed):
            if not gap.sub('', fixed).strip().strip('\\ '):
                fixed = gap.sub(lambda m: r'\rule{0pt}{' + m[1][1:-1].strip() + '}', fixed)
            elif gap.search(fixed.rstrip()) and gap.search(fixed.rstrip()).end() == len(fixed.rstrip()):
                fixed = gap.sub('', fixed)
            else:
                fixed = gap.sub(lambda m: r'\\' + m[1], fixed)
                if r'\begin{' not in fixed:
                    fixed = r'\begin{gathered}' + fixed + r'\end{gathered}'
        return whole[:size] + fixed + whole[-size:]
    text = MATH.sub(spacing, text)
    # An indented formula opener otherwise becomes <pre><code>, which MathJax
    # explicitly skips. Indentation within a protected formula remains exact.
    text = re.sub(r'(?m)^[ \t]{4,}(?=(?:\$|\\\[|\\\())', '', text)
    saved = []
    prefix = 'CABOUNDARYMATHTOKEN'
    while prefix in text:
        prefix += 'X'
    def protect_for_indent(match):
        saved.append(match[0])
        return prefix + str(len(saved) - 1) + 'END'
    protected_text = MATH.sub(protect_for_indent, text)
    protected_text = re.sub(r'(?m)^[ \t]{4,}(?=[^\n]*(?:' + prefix + r'|\{\{|\\\$))', '', protected_text)
    text = re.sub(prefix + r'(\d+)END', lambda m: saved[int(m[1])], protected_text)
    # Empty formula artifacts outside complete math spans carry no equation.
    spans = [(m.start(), m.end()) for m in MATH.finditer(text)]
    changes = []
    for match in re.finditer(r'(?<!\\)\$\$', text):
        if any(start <= match.start() < end for start, end in spans):
            continue
        before, after = text[:match.start()], text[match.end():]
        if (not before.rsplit('\n', 1)[-1].strip() and not after.split('\n', 1)[0].strip()
                or after.startswith(('?', ',"', '\n- '))
                or before.endswith('.') and after.startswith('\n\n|')):
            changes.append((match.start(), match.end(), ''))
    for start, end, replacement in reversed(changes):
        text = text[:start] + replacement + text[end:]
    # A literal currency sign immediately before a widget has no closing math
    # delimiter. Work only outside complete spans to preserve e.g. $x=$ {{x}}.
    pieces, offset = [], 0
    for match in MATH.finditer(text):
        pieces += [re.sub(r'(?<!\\)\$(?=\s*\{\{)', lambda _: r'\$', text[offset:match.start()]), match[0]]
        offset = match.end()
    pieces.append(re.sub(r'(?<!\\)\$(?=\s*\{\{)', lambda _: r'\$', text[offset:]))
    text = ''.join(pieces)
    return text


def normalize_math_boundaries(value):
    """Normalize explicit source encodings to a stable Markdown math boundary."""
    text = normalize_source_arithmetic(value)
    # Settle delimiter/currency encodings before deciding which environments
    # are bare. A transient malformed delimiter must not cause double wrapping.
    for phase in (False, True, False):
        if phase and not ENV.search(MATH.sub('', text)):
            continue
        for _ in range(4):
            result = _normalize_math_boundary_pass(text, wrap_environments=phase)
            if result == text:
                break
            text = result
        else:
            if _normalize_math_boundary_pass(text, wrap_environments=phase) != text:
                raise ValueError('Math boundary normalization did not converge')
    spans = [(m.start(), m.end()) for m in MATH.finditer(text)]
    for match in reversed(list(re.finditer(r'(?m)^([^\n$]+)$', text))):
        line = match[1].strip()
        if not ('=' in line or '≈' in line) or not re.search(r'\\(?:frac|dfrac|sqrt|sum|int)\b', line):
            continue
        if any(start <= match.start() < end for start, end in spans):
            continue
        residual = re.sub(r'\\text\{[^{}]*\}|\\[A-Za-z]+', '', line)
        if re.search(r'[A-Za-z]{4,}', residual) or r'\begin{' in line or r'\end{' in line:
            continue
        try:
            validate_tex(line)
        except ValueError:
            continue
        text = text[:match.start()] + '$$\n' + line + '\n$$' + text[match.end():]
    return text


def validate_math_boundaries(value, *, strict=False):
    """Catch unparsed TeX as well as errors inside recognized math spans."""
    text = str(value)
    # Markdown code spans/fences suppress MathJax even when the TeX inside
    # has valid delimiters. Inspect those bodies before removing math spans.
    def code_has_math(body):
        return MATH.search(body) or re.search(r'\\(?:begin|end)\{|\\(?:frac|dfrac|sqrt|sum|int)\b', body)

    fenced = []
    cursor = 0
    opener = re.compile(r'(?m)^[ \t]{0,3}(`{3,}|~{3,})[^\n]*\n')
    while match := opener.search(text, cursor):
        marker = match[1]
        closing = re.search(r'(?m)^[ \t]{0,3}' + re.escape(marker[0])
                            + '{' + str(len(marker)) + r',}[ \t]*$', text[match.end():])
        end = match.end() + closing.start() if closing else len(text)
        if code_has_math(text[match.end():end]):
            raise ValueError('Fenced math becomes a Markdown code block')
        cursor = match.end() + closing.end() if closing else len(text)
        fenced.append((match.start(), cursor))
    for match in re.finditer(r'(?<!`)(`+)(?!`)(.*?)(?<!`)\1(?!`)', text, re.S):
        if any(start <= match.start() < end for start, end in fenced):
            continue
        if code_has_math(match[2]):
            raise ValueError('Math inside a Markdown code span is not rendered')
    outside = MATH.sub('', text)
    if strict and re.search(r'\\(?:frac|dfrac|sqrt|eqalign)\b', outside):
        raise ValueError('Unprotected TeX expression outside math delimiters')
    if re.search(r'\\(?:begin|end)\{|\\(?:eqalign|matrix)\s*\{', outside):
        raise ValueError('Unprotected TeX environment; use a delimited display block')
    if re.search(r'\[/?(?:math|latex|tex|displaymath)\]', text):
        raise ValueError('Legacy math delimiter; use $ or $$')
    if '[MATH:' in text or re.search(r'\\lef\b', text):
        raise ValueError('Unresolved or damaged legacy source layout')
    if re.search(r'(?<!\\)\$', outside):
        raise ValueError('Unpaired math dollar delimiter; escape literal currency')
    if re.search(r'(?m)^[ \t]{4,}(?=(?:\$|\\\[|\\\())', text):
        raise ValueError('Indented math becomes a Markdown code block')
    for match in MATH.finditer(text):
        if re.search(r'(?<=\d)(?<!\\)%', match[0]):
            raise ValueError('Unescaped percentage glyph comments out math')
    return text


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


def normalize_matrix_answer_tables(value):
    """Recover blank-only answer grids in an explicitly known matrix question."""
    text = str(value)
    if not re.search(r'\\begin\{(?:bmatrix|pmatrix|matrix)\}', text):
        return text
    def replace(match):
        rows, labels = [], []
        for line in match[0].splitlines():
            entries = [cell.strip() for cell in line.strip().strip('|').split('|')]
            if all(re.fullmatch(r':?-+:?', cell) for cell in entries):
                continue
            fields = []
            for cell in entries:
                if not cell:
                    continue
                if re.fullmatch(r'\{\{(?:answer-field:)?[^{}]+\}\}', cell):
                    fields.append(cell)
                    continue
                label = re.fullmatch(r'\$([^$]+?)=\s*(?:\\,\s*)*\$', cell)
                if not label:
                    return match[0]
                labels.append(label[1].strip())
            if fields:
                rows.append(fields)
        if len(labels) != 1 or not rows or len({len(row) for row in rows}) != 1:
            return match[0]
        keys = [cell for row in rows for cell in row]
        if len(keys) != len(set(keys)):
            return match[0]
        return matrix_answer(labels[0], rows)
    return re.sub(r'(?m)^\|[^\n]*\|[ \t]*(?:\n\|[^\n]*\|[ \t]*)+', replace, text)


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
            # An empty alignment column plus an explicit binary continuation
            # denotes a wrapped scalar expression, not matrix cells. Preserve
            # the author's aligned layout; explicit matrix environments still
            # carry matrix semantics regardless of their cell contents.
            if opening[2] == 'aligned' and all(len(row) == 2 and not row[0].strip() for row in rows) \
                    and any(re.match(r'\s*\{\}\s*\+', row[1]) for row in rows[1:]):
                continue
            width = min(map(len, rows))
            if any(len(row) != width for row in rows):
                if not all(not cell for row in rows for cell in row[width:]): continue
                body = r' \\ '.join(' & '.join(row[:width]) for row in rows)
            layout = {'[': 'bmatrix', '(': 'pmatrix', '|': 'vmatrix'}[left[1]]
            text = text[:left.start()] + r'\begin{' + layout + '}' + body + r'\end{' + layout + '}' + text[closing.end() + right.end():]
            changed = True; break
        if not changed: return text
    raise ValueError('Excessive matrix nesting')


def _tex_nonspace_before(text, position):
    while position and text[position - 1].isspace(): position -= 1
    return position


def _tex_command_before(text, position):
    end = _tex_nonspace_before(text, position); start = end
    while start and text[start - 1].isalpha(): start -= 1
    return text[start:end] if start and text[start - 1] == '\\' else ''


def _tex_sizing_command(name):
    return name in ('left', 'right') or bool(re.fullmatch(r'(?:big|Big|bigg|Bigg)[lrm]?', name))


def _scalable_composite_fences(text, environments):
    """Size balanced expression fences containing tables in the same TeX scope.

    A table may be one operand in a matrix sum, or appear inside a formatting
    group. Tables in subscripts and teaching labels do not enlarge unrelated
    proposition parentheses. Alignment cells are independent fence scopes.
    """
    optional = {'sqrt', 'xrightarrow', 'xleftarrow', 'xleftrightarrow',
                'xRightarrow', 'xLeftarrow', 'xLeftrightarrow'}
    candidates = re.finditer(r'\\(?:lparen|lbrack|lbrace|langle)(?![A-Za-z])|\\\{|(?<!\\)[(\[]', text)
    if not any(not _tex_sizing_command(_tex_command_before(text, m.start()))
               and _tex_command_before(text, m.start()) not in optional for m in candidates):
        return text
    tokens = re.compile(r'\\(?:begin|end)\{[^{}]+\}|\\[A-Za-z]+|\\.|[{}()\[\]&.]')
    opening = {'(': 'paren', '[': 'bracket', r'\{': 'brace', r'\lparen': 'paren',
               r'\lbrack': 'bracket', r'\lbrace': 'brace', r'\langle': 'angle'}
    closing = {')': 'paren', ']': 'bracket', r'\}': 'brace', r'\rparen': 'paren',
               r'\rbrack': 'bracket', r'\rbrace': 'brace', r'\rangle': 'angle'}
    annotation = {'underset', 'overset', 'stackrel', 'substack', 'text', 'textrm', 'operatorname'} | (optional - {'sqrt'})
    groups, frames, stacks, edits = [], [], {}, []
    def scope():
        return (tuple(g[0] for g in groups), tuple((f[0], f[1], f[3]) for f in frames))
    for token in tokens.finditer(text):
        value = token[0]; env = ENV.fullmatch(value)
        if env:
            if env[1] == 'begin':
                if env[2] in environments:
                    group_path, frame_path = scope()
                    for (old_groups, old_frames), entries in stacks.items():
                        if old_frames == frame_path and group_path[:len(old_groups)] == old_groups \
                                and not any(role for _, role in groups[len(old_groups):]):
                            for entry in entries: entry['table'] = True
                frames.append([env[2], token.start(), tuple(g[0] for g in groups), 0])
            elif frames and frames[-1][0] == env[2]: frames.pop()
            continue
        if value == '{':
            end = _tex_nonspace_before(text, token.start())
            script = end and text[end - 1] in '_^' and (end < 2 or text[end - 2] != '\\')
            groups.append((token.start(), bool(script or _tex_command_before(text, token.start()) in annotation))); continue
        if value == '}':
            if groups: groups.pop()
            continue
        if value in ('&', r'\\'):
            if frames and tuple(g[0] for g in groups) == frames[-1][2]: frames[-1][3] += 1
            continue
        if value not in opening and value not in closing and value != '.': continue
        key = scope(); stack = stacks.setdefault(key, [])
        command = _tex_command_before(text, token.start()); explicit = _tex_sizing_command(command)
        if value == '.' and explicit:
            if command == 'left': stack.append({'kind': '*', 'explicit': True, 'table': False})
            elif command == 'right' and stack and stack[-1]['explicit']:
                stack.pop()
                if not stack: stacks.pop(key, None)
            continue
        if value in opening:
            stack.append({'kind': opening[value], 'start': token.start(), 'explicit': explicit,
                          'optional': value == '[' and command in optional, 'table': False})
        elif value in closing and stack:
            entry = stack[-1]
            if entry['kind'] != closing[value] and not (entry['kind'] == '*' and command == 'right'): continue
            stack.pop()
            if not stack: stacks.pop(key, None)
            if entry['table'] and not entry['explicit'] and not explicit and not entry.get('optional'):
                edits.extend([(entry['start'], r'\left'), (token.start(), r'\right')])
    for position, command in sorted(edits, reverse=True): text = text[:position] + command + text[position:]
    return text


def scalable_table_fences(text, *, environments=None):
    r"""Stretch existing table fences without changing cells or rules.

    Arrays need their explicit column specification, so replacing them with a
    bmatrix would discard augmentation rules. Respect deliberate delimiter
    sizes and optional macro arguments, whose brackets are not visible fences.
    """
    if r'\begin{' not in text: return text
    environments = environments or {'array', 'aligned', 'alignedat', 'gathered', 'matrix',
                                    'bmatrix', 'pmatrix', 'vmatrix', 'Bmatrix', 'Vmatrix', 'cases'}
    # Resolve paired composite expressions before deciding that a leading
    # condition brace is one-sided.
    text = _scalable_composite_fences(text, environments)
    groups = [('[', r'\lbrack', ']', r'\rbrack'),
              ('(', r'\lparen', ')', r'\rparen'),
              (r'\{', r'\lbrace', r'\}', r'\rbrace'),
              ('|', r'\vert', r'\lvert', r'\rvert'),
              (r'\Vert', r'\lVert', r'\rVert'),
              (r'\langle', r'\rangle')]
    families = {token: i for i, tokens in enumerate(groups) for token in tokens}
    opening = ['[', r'\lbrack', '(', r'\lparen', r'\{', r'\lbrace',
               '|', r'\vert', r'\lvert', r'\Vert', r'\lVert', r'\langle']
    closing = [']', r'\rbrack', ')', r'\rparen', r'\}', r'\rbrace',
               '|', r'\vert', r'\rvert', r'\Vert', r'\rVert', r'\rangle']
    def pattern(tokens):
        return '(?:' + '|'.join(re.escape(t) + (r'(?![A-Za-z])' if t[-1].isalpha() else '')
                               for t in sorted(tokens, key=len, reverse=True)) + ')'
    spacing = r'(?:\s|\\[,;! ]|\\(?:quad|qquad)(?![A-Za-z])|\\hspace\{[^{}]*\})*'
    left_pattern = re.compile('(' + pattern(opening) + ')' + spacing + r'(?=\\begin\{)')
    right_pattern = re.compile(spacing + '(' + pattern(closing) + ')')
    optional = {'sqrt', 'xrightarrow', 'xleftarrow', 'xleftrightarrow', 'xRightarrow', 'xLeftarrow', 'xLeftrightarrow'}
    right_sizing = re.compile(spacing + r'\\right(?![A-Za-z])')
    changes = []
    for left in left_pattern.finditer(text):
        command = _tex_command_before(text, left.start(1))
        if _tex_sizing_command(command) or command in optional: continue
        token = ENV.match(text, left.end())
        if not token or token[1] != 'begin' or token[2] not in environments: continue
        span = environment(text, left.end())
        if not span: continue
        right = right_pattern.match(text, span[2])
        # A literal bracket immediately after a backslash is a math boundary,
        # not a visible delimiter; named/escaped fence tokens are matched whole.
        if left[1] in '[(' and left.start(1) and text[left.start(1) - 1] == '\\': continue
        # A condition table may have only its visible opening brace, including
        # before an implication, a second function, or an outer alignment end.
        # Close its local scope invisibly; never consume an outer right fence.
        if left[1] in (r'\{', r'\lbrace') and (not right or families[right[1]] != 2) \
                and not right_sizing.match(text, span[2]):
            changes.extend([(left.start(1), r'\left'), (span[2], r'\right.')])
            continue
        if not right or families[left[1]] != families[right[1]]: continue
        changes.extend([(left.start(1), r'\left'), (right.start(1), r'\right')])
    for position, command in sorted(changes, reverse=True):
        text = text[:position] + command + text[position:]
    return _scalable_composite_fences(text, environments) if changes else text


def scalable_array_fences(text):
    """Array-only entry point for callers examining explicit column rules."""
    return scalable_table_fences(text, environments={'array'})


def validate_matrix_layouts(value, *, bare_math=False):
    """Reject fenced equation alignments that need actual matrix spacing.

    Inspect only protected formulas (or an explicitly typed math answer).
    Ordinary derivations and wrapped scalar continuations remain unchanged.
    This guard does not rewrite authored content or answer identities.
    """
    spans = [str(value)] if bare_math else [m[0] for m in MATH.finditer(str(value))]
    if any(_matrix_layouts(span) != span for span in spans):
        raise ValueError('Fenced matrix needs a matrix environment; normalize its complete formula')
    if any(scalable_table_fences(span) != span for span in spans):
        raise ValueError('Fenced table needs scalable delimiters; normalize its complete formula')
    return value


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


def normalize_equality_chains(text):
    """Repair explicitly connected expression chains without guessing a RHS.

    MathML tables sometimes put the relation at the end of the preceding
    row. A final continuation can duplicate that relation, and punctuation
    can occupy its own cell. Complete equations and unfilled proof templates
    must retain their independent rows.
    """
    changes = []
    for opening in ENV.finditer(text):
        if opening[1] != 'begin' or opening[2] != 'aligned':
            continue
        span = environment(text, opening.start())
        if not span:
            continue
        rows = cells(text[span[0]:span[1]])
        if not rows or len(rows) < 2:
            continue
        expressions, spacing, trailing, leading = [], [], [], []
        annotation = ''
        for row in rows:
            if len(row) > 2:
                break
            expression, before, after = row[0].strip(), '', ''
            gap = re.match(r'^\[\s*[+-]?(?:\d+(?:\.\d*)?|\.\d+)\s*(?:pt|pc|in|bp|cm|mm|dd|cc|sp|ex|em)\s*\]', expression)
            spacing.append(gap[0] if gap else '')
            expression = expression[gap.end():].strip() if gap else expression
            if len(row) == 2:
                rhs = row[1].strip()
                if not expression:
                    relation = re.match(r'^(=|≈|\\approx)\s*(\S[\s\S]*)$', rhs)
                    if not relation:
                        break
                    before, expression = relation[1], relation[2]
                elif rhs in ('=', '≈', r'\approx'):
                    after = rhs
                elif rhs in ('.', ','):
                    expression += rhs
                elif row is rows[-1] and re.fullmatch(r'[.,]?(?:\\,|\\quad|\\qquad|\\hspace\{\d+(?:\.\d+)?(?:em|ex|pt|px)\}|\s|[{}]|\\color\{[A-Za-z]+\})*(?:✓|\\checkmark|\\times)(?:\s|[{}])*', rhs):
                    annotation = rhs
                elif rhs:
                    break  # A complete equation or an annotation is not a chain.
            relation = re.search(r'(=|≈|\\approx)\s*$', expression)
            if relation:
                if after or before:
                    break
                expression, after = expression[:relation.start()].strip(), relation[1]
            # A bare complete equation is not a single chain expression.
            condition = re.split(r'⇒|\\Rightarrow\b', expression)
            if not expression or _equality_position(condition[-1]) is not None:
                break
            expressions.append(expression); leading.append(before); trailing.append(after)
        if len(expressions) != len(rows) or trailing[-1] or leading[0] or not any(trailing):
            continue
        relations = []
        for index in range(1, len(rows)):
            previous, current = trailing[index - 1], leading[index]
            if not (previous or current) or previous and current and previous != current:
                break
            relations.append(previous or current)
        if len(relations) != len(rows) - 1:
            continue
        body = expressions[0] + ' &' + relations[0] + ' ' + expressions[1]
        for index in range(2, len(expressions)):
            body += r' \\' + spacing[index] + ' &' + relations[index - 1] + ' ' + expressions[index]
        if annotation:
            body += ' && ' + annotation
        changes.append((opening.start(), span[2], r'\begin{aligned}' + body + r'\end{aligned}'))
    for start, end, replacement in sorted(changes, reverse=True):
        text = text[:start] + replacement + text[end:]
    return text


def scalable_fraction_parentheses(text):
    """Size parentheses enclosing a signed fraction, including nested groups."""
    changes = []
    for opening in re.finditer(r'\(\s*[+-]?\s*\\(?:dfrac|tfrac|frac)\s*(?=\{)', text):
        # Respect explicitly chosen delimiter sizes. Already scalable pairs
        # also have a \\right before the closing parenthesis and do not match.
        if re.search(r'\\(?:left|big|Big|bigg|Bigg)[lr]?\s*$', text[:opening.start()]):
            continue
        end = opening.end()
        for _ in range(2):
            while end < len(text) and text[end].isspace():
                end += 1
            if end >= len(text) or text[end] != '{':
                break
            depth = 1
            end += 1
            while end < len(text) and depth:
                if text[end] == '\\':
                    command = re.match(r'\\(?:[A-Za-z]+|.)', text[end:])
                    end += len(command[0]) if command else 1
                    continue
                depth += (text[end] == '{') - (text[end] == '}')
                end += 1
            if depth:
                break
        else:
            while end < len(text) and text[end].isspace():
                end += 1
            if end < len(text) and text[end] == ')':
                changes.extend([(opening.start(), r'\left'), (end, r'\right')])
    for position, command in sorted(changes, reverse=True):
        text = text[:position] + command + text[position:]
    return text


def normalize_sized_bars(text):
    """A sizing command needs a delimiter glyph, not the relation macro mid."""
    return re.sub(r'(\\(?:left|right|middle|[Bb]ig(?:g)?[lrm]?)\s*)\\mid(?![A-Za-z])',
                  lambda m: m[1] + r'\vert', text)


def normalize_piecewise_cases(text):
    """Recover a literal, unmatched left brace on value/condition rows."""
    changes = []
    condition = re.compile(r'[<>=]|\\(?:leq?|geq?|in|notin|neq?)(?![A-Za-z])|\\text\{\s*(?:otherwise|else)\s*\}')
    for match in re.finditer(r'(?<!\\)\{\s*(?=\\begin\{aligned\})', text):
        span = environment(text, match.end())
        if not span or text[span[2]:].lstrip().startswith('}'): continue
        rows = cells(text[span[0]:span[1]])
        if not rows or len(rows) < 2 or any(len(row) != 2 or not all(row) or
                not condition.search(row[1]) or '=' in row[0] for row in rows): continue
        changes.append((match.start(), span[2], r'\begin{cases}' + text[span[0]:span[1]] + r'\end{cases}'))
    for start, end, value in reversed(changes): text = text[:start] + value + text[end:]
    return text


def normalize_limit_operators(text):
    """Recover a limit's role from a balanced, explicit tendency condition."""
    text = re.sub(r'\\lim_\\limits(?=\s*\{)', lambda _: r'\lim_', text)
    def end_group(opening, left='{', right='}'):
        depth, cursor = 1, opening + 1
        while cursor < len(text):
            if text[cursor] == '\\' and cursor + 1 < len(text):
                cursor += 2
                continue
            depth += (text[cursor] == left) - (text[cursor] == right)
            cursor += 1
            if not depth:
                return cursor
        return None
    protected = []
    for match in re.finditer(r'\\(?:text|textrm|mathrm|mathit|mathbf|mathbfit|operatorname\*?)\s*\{', text):
        end = end_group(match.end() - 1)
        if end: protected.append((match.start(), end))
    tendency = re.compile(r'\\(?:to|rightarrow|longrightarrow|uparrow|downarrow)(?![A-Za-z])|[→⟶↑↓]')
    edits = []
    pattern = re.compile(r'(?P<operator>\{(?:lim|\\lim)\}|(?<![\\A-Za-z])lim)\s*_\s*(?P<opening>[{(])')
    for match in pattern.finditer(text):
        if any(a <= match.start() < b for a, b in protected): continue
        preceding = re.search(r'\\([A-Za-z]+)\*?\s*$', text[:match.start()])
        if preceding and preceding[1] not in ('displaystyle', 'textstyle', 'scriptstyle', 'scriptscriptstyle', 'quad', 'qquad'):
            continue
        left = match['opening']; end = end_group(match.end() - 1, left, '}' if left == '{' else ')')
        if not end: continue
        body = text[match.end():end - 1]
        if not tendency.search(body): continue
        if left == '{':
            edits.append((match.start('operator'), match.end('operator'), r'\lim'))
        else:
            body = body.replace('→', r'\to ').replace('⟶', r'\longrightarrow ').replace('∞', r'\infty')
            edits.append((match.start(), end, r'\lim_{' + body.strip() + '}'))
    for start, end, value in reversed(edits): text = text[:start] + value + text[end:]
    return text


def normalize_tex(value):
    text = str(value).strip()
    if MATH.fullmatch(text):
        size = 2 if text.startswith(('$$', r'\[', r'\(')) else 1
        text = text[size:-size].strip()
    # An initial [A|I] is visible content, not aligned's optional position.
    # MathJax accepts arbitrary text as that option and silently drops it.
    text = re.sub(r'(\\begin\{aligned\})(?=\s*\[(?!\s*[tbc]\s*\]))',
                  lambda match: match[1] + '{}', text)
    # Archived SVG titles spell optional row spacing with one backslash,
    # including in substack labels and standalone spacing formulas. A concrete
    # TeX length distinguishes this from an actual display-math delimiter.
    text = normalize_piecewise_cases(normalize_sized_bars(normalize_limit_operators(_label_row_spacing(text))))
    # These extensions are loaded by the application's MathJax configuration.
    # Its restricted TeX input does not enable the runtime \\require command.
    text = re.sub(r'\\require\s*\{(?:cancel|enclose|boldsymbol)\}\s*', '', text)
    text = text.replace(r'\lbrack', '[').replace(r'\rbrack', ']')
    text = text.replace(r'\lbrace', r'\{').replace(r'\rbrace', r'\}')
    text = scalable_fraction_parentheses(_matrix_layouts(_legacy_commands(text)))
    text = scalable_table_fences(text)
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
    return normalize_equality_chains(text)


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
        line = text[text.rfind('\n', 0, match.start()) + 1:match.start()]
        quote = re.match(r'^(?: {0,3}>[\t ]?)+', line)
        if quote:
            depth = quote[0].count('>')
            marker = r'^(?: {0,3}>[\t ]?){' + str(depth) + '}'
            whole = re.sub(r'\n([^\n]*)', lambda m: '\n' + re.sub(marker, '', m[1]), whole)
        normalized = normalize_tex(whole)
        result = ('$$\n' + normalized + '\n$$') if display else ('$' + normalized + '$')
        return result.replace('\n', '\n' + quote[0]) if quote else result
    text = normalize_math_boundaries(value)
    text = MATH.sub(replace, text)
    # Browser indentation is not a Markdown code-block instruction.
    if '{{field-' in text:
        text = re.sub(r'(?m)^[ \t]{4,}(?=\$(?!\$))', '', text)
    return text


def validate_tex(value):
    """Validate structural invariants; the UI's MathJax checks rendering."""
    text = str(value); depth = 0; stack = []; fences = []
    if re.search(r'\\begin\{aligned\}\s*\[(?!\s*[tbc]\s*\])', text):
        raise ValueError('Visible initial bracket in aligned is consumed as placement; insert {} or use scalable fences')
    if re.search(r'\\(?:left|right|middle)(?![A-Za-z])\s*$', text):
        raise ValueError('Missing left/right delimiter glyph')
    check_fences = not re.search(r'\\(?:newcommand|renewcommand|def)(?![A-Za-z])', text)
    if re.search(r'\\[Bb]ig(?:g)?[lrm]?\s*\\(?:left|right|middle)(?![A-Za-z])', text):
        raise ValueError('Sizing command cannot take a left/right command as its delimiter')
    if legacy_system_rows(text):
        raise ValueError('Flattened equation system; use explicit system rows')
    for token in re.findall(r'\\(?:begin|end)\{[^{}]+\}|\\[A-Za-z]+|\\.|.', text, re.S):
        env = ENV.fullmatch(token)
        if env:
            if env[1] == 'begin': stack.append(env[2])
            elif not stack or stack.pop() != env[2]: raise ValueError('Mismatched TeX environment')
        elif token == '{': depth += 1
        elif token == '}': depth -= 1
        elif check_fences and token == r'\left': fences.append((depth, tuple(stack)))
        elif check_fences and token == r'\right':
            if not fences or fences.pop() != (depth, tuple(stack)):
                raise ValueError('Crossed or unmatched left/right fence scope')
        if depth < 0: raise ValueError('Unmatched closing TeX brace')
        if token in [r'\matrix', r'\eqalign']: raise ValueError('Legacy TeX layout command')
        if token in [r'\[', r'\]', r'\(', r'\)']:
            raise ValueError('Nested math delimiter in a TeX expression')
        if token == r'\=':
            raise ValueError('Unsupported TeX equality command; use =')
        if token == r'\require':
            raise ValueError('Runtime TeX extension loading is unsupported; use a preloaded extension')
        if token == '$': raise ValueError('Math fields must not contain nested dollar delimiters')
    if depth or stack: raise ValueError('Unclosed TeX group or environment')
    if fences: raise ValueError('Unclosed left/right fence scope')
    for match in re.finditer(r'\\begin\{aligned\}', text):
        span = environment(text, match.start())
        rows = cells(text[span[0]:span[1]]) if span else None
        if rows and any(len(row) == 2 and row[0] and row[1] in ('=', '≈', r'\approx') for row in rows):
            raise ValueError('Empty equation RHS; normalize the chain or recover its missing source content')
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
    text = validate_math_boundaries(value)
    for match in MATH.finditer(text):
        size = 2 if match[0].startswith(('$$', r'\[', r'\(')) else 1
        validate_tex(match[0][size:-size])
    outside = MATH.sub('', text)
    if re.search(r'(?<!\\)\$', outside): raise ValueError('Unpaired math dollar delimiter')
    return text


def validate_math_structure(value, *, bare_math=False):
    """Check groups, environments and grids at an authoring boundary."""
    validate_matrix_layouts(value, bare_math=bare_math)
    spans = [str(value)] if bare_math else [m[0] for m in MATH.finditer(str(value))]
    for span in spans:
        if MATH.fullmatch(span):
            size = 2 if span.startswith(('$$', r'\[', r'\(')) else 1
            span = span[size:-size]
        validate_tex(span)
        if normalize_limit_operators(span) != span:
            raise ValueError('Malformed limit operator; normalize the tendency condition')
        if normalize_sized_bars(span) != span:
            raise ValueError('Sized bar needs a delimiter glyph, not mid')
    return value


def validate_generated_record(record):
    question = record['question']
    for key in [':question/problem', ':question/worked-solution']:
        value = question[key]
        validate_prose(value)
        if normalize_prose(value) != value: raise ValueError('Noncanonical math content in ' + key)
    field_keys = set()
    for field in question.get(':question/answer-fields', []):
        key = field.get(':answer-field/key')
        if key is not None:
            if not isinstance(key, str) or not key or key in field_keys:
                raise ValueError('Answer-field keys must be present and unique')
            field_keys.add(key)
        kind = field.get(':answer-field/type')
        if isinstance(kind, dict): kind = kind.get(':db/ident')
        if kind == ':answer-field.type/checkbox':
            validate_prose(key)
            if normalize_prose(key) != key:
                raise ValueError('Noncanonical math content in checkbox statement')
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
