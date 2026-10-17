"""Prepare narrowly scoped tutorial layout improvements; no database writes."""
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
snapshot = json.loads((HERE.parent / 'lesson.json').read_text())
tutorials = {}


def collect(value):
    if isinstance(value, dict):
        if ':tutorial/content' in value:
            tutorials[value[':db/id']] = value
        for child in value.values():
            collect(child)
    elif isinstance(value, list):
        for child in value:
            collect(child)


collect(snapshot['activity'])
changes = []


def add(entity, after, reason):
    before = tutorials[entity][':tutorial/content']
    assert before != after
    assert re.findall(r'!\[[^\]]*\]\(([^)]+)\)', before) == re.findall(r'!\[[^\]]*\]\(([^)]+)\)', after)
    changes.append({'entity': entity, 'attribute': ':tutorial/content', 'before': before,
                    'after': after, 'reason': reason, 'topic': 17592186050240})


entity = 17592186075064
before = tutorials[entity][':tutorial/content']
start = before.index('- If we set $x=0$')
end = before.index('\n\nBy selecting any $x$-value', start)
examples = r'''- If we set $x=0$, we get the point

  $$
  \begin{aligned}
  (x, y) &= (0, 3(0) + 2) \\
         &= (0, 2).
  \end{aligned}
  $$

  This point is indeed a solution to the system:

  $$
  \left\{\begin{aligned}
  3(0) - 2 &= -2 \\
  6(0) - 2(2) &= -4
  \end{aligned}\right.
  $$

  Both equations are satisfied. Therefore, $(0,2)$ is a solution.

- If $x= 1$, we get the point

  $$
  \begin{aligned}
  (x, y) &= (1, 3(1) + 2) \\
         &= (1, 5).
  \end{aligned}
  $$

  This point is another solution to the system:

  $$
  \left\{\begin{aligned}
  3(1) - 5 &= -2 \\
  6(1) - 2(5) &= -4
  \end{aligned}\right.
  $$

  Both equations are satisfied. Therefore, $(1,5)$ is a solution.'''
add(entity, before[:start] + examples + before[end:],
    'Separate the two worked examples into properly indented list items with paragraph spacing; stack each point calculation and render each verification system as display math.')

entity = 17592186075049
before = tutorials[entity][':tutorial/content']
start = before.index('| ![](')
images = re.findall(r'!\[[^\]]*\]\([^)]+\)', before[start:])
cases = re.findall(r'^- (Case .*?)$', before[start:], re.M)
assert len(images) == len(cases) == 3
blocks = []
for case, image in zip(cases, images):
    first, remainder = case.split('. ', 1)
    blocks.append(f'- {first}.\n\n  {image}\n\n  {remainder}')
add(entity, before[:start] + '\n\n'.join(blocks),
    'Give each intersection case its own original graph and explanatory paragraph, replacing the cramped three-column image table with a readable vertical sequence.')

entity = 17592186075062
before = tutorials[entity][':tutorial/content']
old = 'Our goal is to express *all* the solutions of this system in the form $({\\color{blue}{x}},{\\color{red}{y}})$. To do this,'
new = old.replace('$. To do this,', '$.\n\nTo do this,')
assert old in before
after = before.replace(old, new)
old_math = '3x - y =-2⇒y = 3x + 2'
new_math = r'''\begin{aligned}
3x - y &= -2 \\
y &= 3x + 2
\end{aligned}'''
assert old_math in after
after = after.replace(old_math, new_math)
add(entity, after,
    'Separate the goal from the solving instruction and show the equivalent equation rearrangement on two aligned rows instead of a crowded inline-arrow chain.')

# Ensure the authored edits preserve every original mathematical token, apart from
# layout, the derivation arrow replaced by vertical progression, and punctuation.
def content_tokens(value):
    value = re.sub(r'!\[[^\]]*\]\([^)]+\)', '', value)
    value = re.sub(r'^\|.*\|$', '', value, flags=re.M)
    value = re.sub(r'^\s*- ', '', value, flags=re.M)
    value = value.replace(r'\begin{aligned}', '').replace(r'\end{aligned}', '')
    value = value.replace(r'\\', '').replace('&', '').replace('⇒', '')
    return re.sub(r'[\s$]', '', value)

for change in changes:
    assert content_tokens(change['before']) == content_tokens(change['after']), change['entity']

entity = 17592186075063
before = tutorials[entity][':tutorial/content']
old_annotation = r'\text{multiply by } -2'
new_annotation = r'\mid\cdot(-2)'
assert before.count(old_annotation) == 1
old_block = r'\left\{\begin{aligned}3x-y &=-2 && \text{multiply by } -2 \\ 6x-2y &=-4\end{aligned}\right.'
new_block = r'\left\{\begin{alignedat}{2}3x-y &=-2 &\quad& \mid\cdot(-2) \\ 6x-2y &=-4\end{alignedat}\right.'
assert before.count(old_block) == 1
add(entity, before.replace(old_block, new_block),
    'Keep the first-equation multiplier visible on mobile using the lesson\'s compact operation notation; the immediately preceding prose explains multiplying by -2.')
assert changes[-1]['after'].replace(new_block, old_block) == before

(HERE / 'changes.json').write_text(json.dumps(changes, indent=2) + '\n')
review = {
    'basis': snapshot['identity']['basis'],
    'topic': 17592186050240,
    'tutorials_reviewed': len(tutorials),
    'tutorials_changed': len(changes),
    'unchanged': [
        {'entity': 17592186075061, 'reason': 'Introduction already has separate paragraphs, display system, image, and clear three-item list.'},
    ],
    'preservation': 'Exact prose and mathematical tokens preserved after ignoring Markdown/TeX layout, image placement, and the equation-rearrangement arrow; one multiplier annotation uses equivalent compact notation. Original image URLs and order unchanged.',
    'database_writes': 0,
}
(HERE / 'review.json').write_text(json.dumps(review, indent=2) + '\n')
print(json.dumps(review, indent=2))
