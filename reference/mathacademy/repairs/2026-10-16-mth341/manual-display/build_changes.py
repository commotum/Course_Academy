"""Exact, snapshot-based repairs for MTH 341 display defects.

No database writes. Answer-field identities, order, and choices are unchanged.
Shared canonical normalization is deliberately applied after these local fixes.
"""
import collections
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
sys.path.insert(0, str(ROOT / 'scripts/question_capture'))
import math_format as mf

FIELDS = json.loads((ROOT / 'reference/mathacademy/audits/2026-10-16-mth341/fields.json').read_text())


def theorem(n, blank=None):
    status = r'\underline{\phantom{\text{invertible}}}' if blank == 'status' else r'\text{invertible}'
    dimension = r'\underline{\phantom{\dim(\operatorname{Col}(A))}}' if blank == 'dimension' else r'\dim(\operatorname{Col}(A))'
    size = r'\underline{\phantom{n}}' if blank == 'size' else n
    return (
        r'A\text{ is }' + status + r'\quad\Longleftrightarrow\quad\left\{\begin{aligned}'
        + r'\operatorname{Col}(A) &=\mathbb{R}^{' + n + r'} \\ '
        + dimension + ' &=' + size + r'=\operatorname{rank}(A) \\ '
        + r'\operatorname{Null}(A) &=\{0\} \\ '
        + r'\dim(\operatorname{Null}(A)) &=0=\operatorname{nullity}(A)'
        + r'\end{aligned}\right.'
    )


def group_end(text, opening):
    """Find a literal TeX group's closing brace, respecting escaped braces."""
    assert text[opening] == '{'
    depth, i = 1, opening + 1
    while i < len(text):
        if text[i] == '\\':
            i += 2
            continue
        if text[i] == '{':
            depth += 1
        elif text[i] == '}':
            depth -= 1
            if not depth:
                return i
        i += 1
    raise ValueError('Unclosed intended set group')


def recover_set_braces(text):
    edits = []
    # These exact contexts distinguish set braces from groups around variables
    # (e.g. {R}^n), subscripts, or colored expression arguments.
    for match in re.finditer(r'(?:\\text\{(?:Null|Col)\}\(A\)=|\\text\{Span\})\{', text):
        opening = match.end() - 1
        closing = group_end(text, opening)
        body = text[opening + 1:closing]
        if r'\begin{bmatrix}' not in body or not (r'\text{Span}' in match[0] or r'\in R' in body):
            continue
        edits.append((opening, closing, r'\left\{' + body + r'\right\}'))
    for start, end, replacement in reversed(edits):
        text = text[:start] + replacement + text[end + 1:]
    return text, len(edits)


changes = []
for field in FIELDS:
    before = field['value']
    after = before
    reasons = []
    eid, attr = field['entity'], field['attribute']

    # A capture lost the visible left brace of all four simultaneous conditions.
    if r'⇔\,{\,\begin{aligned}' in after:
        n = re.search(r'\\text\{Col\}\(A\)=\{R\}\^\{([^{}]+)\}', after)[1]
        blank = {17592186124791: 'dimension', 17592186272237: 'size', 17592186272335: 'status'}.get(eid) if attr == ':question/problem' else None
        if '$A$ is invertible $' in after:
            pattern = r'\$A\$ is invertible \$\\,⇔\\,\{\\,\\begin\{aligned\}.*?\\end\{aligned\}\$'
            after, count = re.subn(pattern, lambda _: '$$\n' + theorem(n, blank) + '\n$$', after, count=1, flags=re.S)
        else:
            pattern = r'A\\text\{.*?⇔\\,\{\\,\\begin\{aligned\}.*?\\end\{aligned\}'
            after, count = re.subn(pattern, lambda _: theorem(n, blank), after, count=1, flags=re.S)
        assert count == 1, (eid, attr)
        reasons.append('Rebuild the malformed invertible-matrix equivalence with a scalable brace, aligned conditions, visible zero-set braces, and the source blank in its original position.')

    # The other captures retain an escaped brace but not its scalable form.
    # Preserve the original conditions, including all genuine bbox blanks.
    scaled_theorems = 0
    for match in list(re.finditer(r'⇔\\,\\\{\\,\\begin\{aligned\}', after))[::-1]:
        opening = after.index(r'\begin{aligned}', match.start())
        span = mf.environment(after, opening)
        assert span is not None
        prefix = r'⇔\,\left\{'
        after = after[:match.start()] + prefix + after[opening:span[2]] + r'\right.' + after[span[2]:]
        scaled_theorems += 1
    if scaled_theorems:
        reasons.append('Make the existing theorem-condition brace scalable while preserving every condition and existing blank.')

    # Existing prose elsewhere in these fields also needs visible set braces.
    after, count = re.subn(r'(\\text\{Null\}\(A\)(?:=|\\ne\s*))\{0\}', lambda m: m[1] + r'\{0\}', after)
    if count:
        reasons.append('Escape the set braces around the zero vector in Null(A) statements so they are displayed.')

    after, count = recover_set_braces(after)
    if count:
        reasons.append('Recover visible scalable set delimiters around the existing null-space parametrization or spanning vectors; preserve all vector entries and parameters.')

    if eid == 17592186272352 and attr == ':question/problem':
        old = r'B={{b}_{1},{b}_{2},{b}_{3},{b}_{4},{b}_{5}}'
        assert old in after
        after = after.replace(old, r'B=\{{b}_{1},{b}_{2},{b}_{3},{b}_{4},{b}_{5}\}')
        reasons.append('Restore visible braces around the five listed basis vectors.')

    if eid in (17592186138700, 17592186138764, 17592186074030, 17592186193236) and attr == ':question/problem':
        after, count = re.subn(r'\$\(\$\s*\{\{field-1\}\}\s*\$\$,\s*\{\{field-2\}\}\s*\$\)\$', lambda _: '$($ {{field-1}} $,$ {{field-2}} $)$', after)
        assert count == 1
        if eid == 17592186074030:
            after = after.replace('substitution.The solution', 'substitution.\n\nThe solution')
        reasons.append('Repair the coordinate-answer delimiter sequence while preserving the x/y input order and field keys.')

    if eid == 17592186497411 and attr == ':question/worked-solution':
        assert r'$$2\,240.$' in after
        after = after.replace(r'$$2\,240.$', r'$2\,240$ dollars.')
        reasons.append('Repair the malformed final currency delimiter and retain the revenue amount of 2,240 dollars.')

    if r'=\=' in after:
        assert 'matrix-answer-label' in after
        after = after.replace(r'=\=', '=')
        reasons.append('Remove the invalid \\= command from the answer-matrix label; keep the single equals sign.')

    if eid == 17592186100741 and attr == ':question/worked-solution':
        assert r'\right\rbrack \[5pt]' in after
        after = after.replace(r'\right\rbrack \[5pt]', r'\right\rbrack \\[5pt]')
        reasons.append('Restore the missing backslash in the calculation row break; [5pt] remains row spacing.')

    if eid == 17592186235392 and attr == ':question/problem':
        # Four independent entries were surrounded by browser-layout indentation.
        start = after.index('find the values ${t}_{ij}.$') + len('find the values ${t}_{ij}.$')
        after = after[:start] + '\n\n' + '\n\n'.join('${t}_{' + ij + '}=$ {{field-' + str(i) + '}}' for i, ij in enumerate(('11', '12', '21', '22'), 1))
        assert re.findall(r'\{\{field-\d+\}\}', before) == re.findall(r'\{\{field-\d+\}\}', after)
        reasons.append('Remove captured browser indentation that creates code blocks; keep each matrix-entry label attached to its original answer field.')

    if eid == 17592186075064 and attr == ':tutorial/content':
        replacements = {
            '(x, y)|= (0, 3(0) + 2); = (0, 2)': '(x, y) = (0, 3(0) + 2) = (0, 2)',
            '(x, y)|= (1, 3(1) + 2); = (1, 5)': '(x, y) = (1, 3(1) + 2) = (1, 5)',
        }
        for old, new in replacements.items():
            assert old in after
            after = after.replace(old, new)
        reasons.append('Remove stray vertical-bar and semicolon capture artifacts from the two point-evaluation equalities.')

    # Put multiplication instructions in a separate aligned annotation column.
    # These were previously concatenated into the equation right-hand side.
    annotation_blocks = {
        (17592186075063, ':tutorial/content'): (
            r'{3x - y =-2 \mid \mid \cdot (-2); 6x - 2y =-4',
            r'\left\{\begin{aligned}3x-y &=-2 && \text{multiply by } -2 \\ 6x-2y &=-4\end{aligned}\right.'),
        (17592186073480, ':question/worked-solution'): (
            r'{4x + 2y = 4; 2x + y = 4 \mid \mid \cdot (-2)',
            r'\left\{\begin{aligned}4x+2y &=4 \\ 2x+y &=4 && \text{multiply by } -2\end{aligned}\right.'),
        (17592186073482, ':question/worked-solution'): (
            r'{3x + 2y = 2 \mid \mid \cdot (-2); 6x + 4y = 4',
            r'\left\{\begin{aligned}3x+2y &=2 && \text{multiply by } -2 \\ 6x+4y &=4\end{aligned}\right.'),
    }
    if (eid, attr) in annotation_blocks:
        old, new = annotation_blocks[eid, attr]
        assert old in after
        after = after.replace(old, new)
        reasons.append('Separate the row-multiplication annotation from the equation right-hand side using an aligned annotation column.')
        if eid == 17592186075063:
            old = r'3x - y =-2; 2 \cdot (3x - y) = 2 \cdot (-2); 6x - 2y =-4'
            assert old in after
            after = after.replace(old, r'\begin{aligned}3x-y &=-2 \\ 2\cdot(3x-y) &=2\cdot(-2) \\ 6x-2y &=-4\end{aligned}')
            reasons.append('Restore separate aligned rows in the semicolon-flattened multiplication calculation.')

    if after != before:
        # Prove local fixes survive the shared canonical pass. Keep after itself
        # unnormalized so other workers can apply their exact snapshot patches.
        normalized = mf.normalize_tex(after) if field['kind'] == 'math' else mf.normalize_prose(after)
        (mf.validate_tex if field['kind'] == 'math' else mf.validate_prose)(normalized)
        assert collections.Counter(re.findall(r'\{\{[^{}]+\}\}', before)) == collections.Counter(re.findall(r'\{\{[^{}]+\}\}', after)), (eid, attr)
        changes.append({'entity': eid, 'attribute': attr, 'before': before, 'after': after, 'rationale': ' '.join(reasons)})

(HERE / 'changes.json').write_text(json.dumps(changes, ensure_ascii=False, indent=2) + '\n')
(HERE / 'summary.json').write_text(json.dumps({'fields': len(changes), 'entities': len({c['entity'] for c in changes}), 'attributes': dict(collections.Counter(c['attribute'] for c in changes)), 'unresolved_manual_defects': []}, indent=2) + '\n')
print(f'Prepared {len(changes)} manual display patches.')
