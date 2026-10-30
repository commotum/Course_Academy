"""Narrow shared table fence normalizer; no algebra or identity changes."""

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

MATH = re.compile(r'(?<!\\)\\\[[\s\S]*?\\\]|(?<!\\)\\\([\s\S]*?\\\)|\$\$[\s\S]*?\$\$|(?<!\\)\$(?!\$)(?:\\[\s\S]|[^$\\])*?(?<!\\)\$')

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
    candidates = re.finditer(r'\\(?:lparen|lbrack|lbrace|langle|lvert|lVert|vert|Vert)(?![A-Za-z])|\\\{|(?<!\\)[(\[|∣‖∥⟨]', text)
    if not any(not _tex_sizing_command(_tex_command_before(text, m.start()))
               and _tex_command_before(text, m.start()) not in optional for m in candidates):
        return text
    tokens = re.compile(r'\\(?:begin|end)\{[^{}]+\}|\\[A-Za-z]+|\\.|[{}()\[\]&.|∣‖∥⟨⟩]')
    opening = {'(': 'paren', '[': 'bracket', r'\{': 'brace', r'\lparen': 'paren',
               r'\lbrack': 'bracket', r'\lbrace': 'brace', r'\langle': 'angle', '⟨': 'angle',
               r'\lvert': 'bar', r'\lVert': 'doublebar'}
    closing = {')': 'paren', ']': 'bracket', r'\}': 'brace', r'\rparen': 'paren',
               r'\rbrack': 'bracket', r'\rbrace': 'brace', r'\rangle': 'angle', '⟩': 'angle',
               r'\rvert': 'bar', r'\rVert': 'doublebar'}
    symmetric = {'|': 'bar', '∣': 'bar', r'\vert': 'bar', '‖': 'doublebar', '∥': 'doublebar', r'\Vert': 'doublebar'}
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
        if value not in opening and value not in closing and value not in symmetric and value != '.': continue
        key = scope(); stack = stacks.setdefault(key, [])
        command = _tex_command_before(text, token.start()); explicit = _tex_sizing_command(command)
        if value == '.' and explicit:
            if command == 'left': stack.append({'kind': '*', 'explicit': True, 'table': False})
            elif command == 'right' and stack and stack[-1]['explicit']:
                stack.pop()
                if not stack: stacks.pop(key, None)
            continue
        if value in symmetric:
            kind = symmetric[value]
            if stack and (stack[-1]['kind'] == kind or stack[-1]['kind'] == '*' and command == 'right'):
                entry = stack.pop()
                if not stack: stacks.pop(key, None)
                if entry['table'] and not entry['explicit'] and not explicit:
                    edits.extend([(entry['start'], r'\left'), (token.start(), r'\right')])
            elif command != 'right':
                stack.append({'kind': kind, 'start': token.start(), 'explicit': explicit, 'table': False})
        elif value in opening:
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
              ('|', '∣', r'\vert', r'\lvert', r'\rvert'),
              ('‖', '∥', r'\Vert', r'\lVert', r'\rVert'),
              ('⟨', '⟩', r'\langle', r'\rangle')]
    families = {token: i for i, tokens in enumerate(groups) for token in tokens}
    opening = ['[', r'\lbrack', '(', r'\lparen', r'\{', r'\lbrace',
               '|', '∣', '‖', '∥', '⟨', r'\vert', r'\lvert', r'\Vert', r'\lVert', r'\langle']
    closing = [']', r'\rbrack', ')', r'\rparen', r'\}', r'\rbrace',
               '|', '∣', '‖', '∥', '⟩', r'\vert', r'\rvert', r'\Vert', r'\rVert', r'\rangle']
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
