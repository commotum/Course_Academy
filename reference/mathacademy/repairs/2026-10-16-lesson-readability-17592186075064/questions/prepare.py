"""Display-only question readability changes, frozen at the lesson read basis."""
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
lesson = json.loads((HERE.parent / 'lesson.json').read_text())
changes = []
review = []

def display_pair(equations, labelled=False):
    rows = []
    for i, equation in enumerate(equations, 1):
        lhs, rhs = equation.split('=')
        rows.append((f'l_{{{i}}}:\\quad & ' if labelled else '') + lhs.strip()
                    + (r' &{}={}& ' if labelled else ' &= ') + rhs.strip())
    env = 'alignedat' if labelled else 'aligned'
    args = '{2}' if labelled else ''
    return '$$\n' + '\\begin{' + env + '}' + args + '\n' + ' \\\\[6pt]\n'.join(rows) + '\n\\end{' + env + '}\n$$'

for kp in lesson['topic'][':topic/knowledge-points']:
    for question in [kp[':knowledge-point/canonical-example'], *kp[':knowledge-point/questions']]:
        entity = question[':db/id']
        before = question[':question/problem']
        after = before
        reasons = []
        if entity == 17592186561226:
            disposition = 'Already repaired separately; excluded from this transaction.'
        elif kp[':db/id'] == 17592186073776:
            after = re.sub(r'(?m)^\$([^$\n]+)\$$', lambda m: '$$\n' + m[1] + '\n$$', before)
            if after != before:
                reasons.append('Promote the standalone two-row system from inline math to a spaced display block.')
        elif kp[':db/id'] == 17592186073777:
            match = re.search(r'\$l_\{1\}: (.*), l_\{2\}: (.*)\$\.', before)
            if match:
                after = before[:match.start()] + display_pair(match.groups(), True) + before[match.end():]
                after = after.replace('defined as\n', 'defined by\n\n')
                reasons.append('Stack labelled line definitions, align labels/equalities, and add modest row spacing.')
            else:
                match = re.fullmatch(r'At how many points do the lines \$([^$]+)\$ and \$([^$]+)\$ intersect\?', before)
                assert match, before
                after = 'At how many points do the following lines intersect?\n\n' + display_pair(match.groups())
                reasons.append('Move both line definitions into an aligned display for comparison.')
        else:
            assert kp[':db/id'] == 17592186073778
            match = re.match(r'(Find all points of intersection of the lines|Describe the points that lie on the intersection of the lines) \$([^$]+)\$ and \$([^$]+)\$\.', before)
            assert match, before
            opening = match[1].removesuffix('the lines') + 'the following lines:'
            after = opening + '\n\n' + display_pair(match.groups()[1:])
            remainder = before[match.end():].lstrip()
            if remainder:
                remainder = remainder.replace('only.The', 'only.\n\nThe')
                remainder = re.sub(r'\$\(([xtu])\$,\n\{\{field-1\}\}\n\$\)\$', r'$(\1,$ {{field-1}} $)$', remainder)
                remainder = re.sub(r'The intersection points are (\$\([xtu],\$ \{\{field-1\}\} )\$\)\$, where', r'The intersection points are\n\n\1$),$\n\nwhere', remainder)
                after += '\n\n' + remainder
            reasons.append('Move paired line equations into a spaced aligned display; separate directions and keep response-tuple pieces together.')
        if after != before:
            assert re.findall(r'\{\{[^}]+\}\}', before) == re.findall(r'\{\{[^}]+\}\}', after)
            # Coefficients, variables and equation sides are preserved verbatim except whitespace.
            if kp[':db/id'] == 17592186073776:
                assert re.sub(r'[\s$]', '', before) == re.sub(r'[\s$]', '', after)
            elif kp[':db/id'] == 17592186073777 and 'labelled' in reasons[0]:
                original_equations = match.groups()
                new_equations = re.findall(r'l_\{[12]\}:\\quad & (.*?) &\{\}=\{\}& ([^\n]+)', after)
                assert [re.sub(r'\s', '', e) for e in original_equations] == [re.sub(r'\s', '', a+'='+b.removesuffix(r'\\[6pt]')) for a,b in new_equations]
            else:
                original_equations = match.groups() if kp[':db/id'] == 17592186073777 else match.groups()[1:]
                block = re.search(r'\\begin\{aligned\}\n(.*?)\n\\end\{aligned\}', after, re.S)[1]
                new_equations = block.split(r'\\[6pt]')
                assert [re.sub(r'\s', '', e) for e in original_equations] == [re.sub(r'[\s&]', '', e) for e in new_equations]
            changes.append({'entity': entity, 'attribute': ':question/problem', 'before': before, 'after': after, 'reason': ' '.join(reasons), 'knowledge_point': kp[':db/id']})
            disposition = 'Prompt display/spacing improvement; mathematical equations and field placeholders preserved.'
        elif entity != 17592186561226:
            disposition = 'Prompt already has clearly separated paragraphs and display math.'
        review.append({'entity': entity, 'knowledge_point': kp[':db/id'], 'problem': disposition,
                       'worked_solution': 'Reviewed: paragraphs and displayed derivation steps are already readable; unchanged.' if ':question/worked-solution' in question else 'Missing: left unfilled as requested.'})

assert len(review) == 55
assert len(changes) == 39
(HERE / 'changes.json').write_text(json.dumps(changes, indent=2) + '\n')
(HERE / 'review.json').write_text(json.dumps({'basis': lesson['identity']['basis'], 'questions_reviewed': len(review), 'prompt_changes': len(changes), 'solution_changes': 0, 'math_and_placeholder_preservation': True, 'questions': review}, indent=2) + '\n')
print(json.dumps({'reviewed': len(review), 'changes': len(changes)}))
