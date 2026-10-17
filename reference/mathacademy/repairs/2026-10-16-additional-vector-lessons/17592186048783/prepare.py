"""Source-backed conformability lesson repairs; no database operations."""
from pathlib import Path
import hashlib
import json
import re
import sys
from bs4 import BeautifulSoup

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
sys.path.insert(0, str(ROOT / 'scripts/question_capture'))
from math_format import matrix_operands, MATH

snapshot = json.loads((HERE / 'lesson.json').read_text())
topic = snapshot['topic']
questions = [q for kp in topic[':topic/knowledge-points'] for q in [kp[':knowledge-point/canonical-example'], *kp[':knowledge-point/questions']]]
byid = {q[':db/id']: q for q in questions}
tutorials = {s[':step/content'][':db/id']: s[':step/content']
             for a in topic[':activity/_scope'] for s in a[':activity/steps'] if ':tutorial/content' in s[':step/content']}
formulas = {x['math_academy_id']: x for x in json.loads((HERE / 'source-formulas.json').read_text())}
CAP = ROOT / 'reference/mathacademy/question-capture/13979047'
WORK = ROOT / 'reference/mathacademy/question-capture-workers/linear/14043361'
ORIGINAL = Path('/home/jake/Developer/MA/DATA/Lessons/1198/Source/1198.html')
original = BeautifulSoup(ORIGINAL.read_text(), 'html.parser')
changes = []
answer_changes = []
review = []
source_evidence = []
MAT = re.compile(r'([A-Z])\s*=\s*(\\begin\{bmatrix\}.*?\\end\{bmatrix\})', re.S)


def save(name, value):
    (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def source(mid, after=False):
    for root in [CAP, WORK]:
        path = root / f'q-{mid}-{"after" if after else "before"}.json'
        if path.exists():
            raw = path.read_bytes()
            return {'path': str(path.relative_to(ROOT)), 'sha256': hashlib.sha256(raw).hexdigest(),
                    'html': json.loads(raw)['html']}
    node = original.select_one('#question-' + str(mid))
    assert node is not None, mid
    return {'path': str(ORIGINAL), 'sha256': hashlib.sha256(ORIGINAL.read_bytes()).hexdigest(), 'html': str(node)}


def add(entity, attribute, after, reason, evidence):
    before = (tutorials if attribute == ':tutorial/content' else byid)[entity][attribute]
    assert before != after
    assert re.findall(r'\{\{[^{}]+\}\}', before) == re.findall(r'\{\{[^{}]+\}\}', after)
    changes.append({'entity': entity, 'attribute': attribute, 'before': before, 'after': after,
                    'reason': reason, 'source': evidence})


def responsive_operands(text):
    """Keep every named matrix cell and factor label; replace grouping only."""
    matches = list(MATH.finditer(text))
    if not matches:
        return text
    # Three matrices currently share a single unbreakable display.
    first = matches[0]
    operands = MAT.findall(first[0])
    if len(operands) >= 2:
        return text[:first.start()] + matrix_operands([name + '=' + mat for name, mat in operands]) + text[first.end():]
    # Two standalone definitions, separated by "and" after "Let".
    if not text.startswith('Let') or len(matches) < 2:
        return text
    a, b = matches[:2]
    if len(MAT.findall(a[0])) != 1 or len(MAT.findall(b[0])) != 1:
        return text
    operands = MAT.findall(a[0]) + MAT.findall(b[0])
    tail = text[b.end():].strip().lstrip('.').strip()
    return 'Let\n\n' + matrix_operands([name + '=' + mat for name, mat in operands]) + '\n\n' + tail


def dimensions(text):
    pattern = r'are\{\{field-1\}\}\$\\times \$\s*\{\{field-2\}\}'
    return re.sub(pattern, lambda _: 'are <span style="display: inline-flex; align-items: center; gap: .35em; white-space: nowrap;">{{field-1}} $\\times$ {{field-2}}</span>', text)


# Every mixed SVG-title fragment has been independently recovered in extract_source.py.
A = r'\begin{bmatrix}1 & 12 \\ 6 & -4\end{bmatrix}'
B = r'\begin{bmatrix}1 & 3 \\ 2 & -2 \\ 3 & 5\end{bmatrix}'
before = tutorials[17592186101958][':tutorial/content']
pieces = re.split(r'\$\$.*?\$\$', before, flags=re.S)
assert len(pieces) == 3
product = formulas[2990]['formulas'][8]['reconstructed_tex']
assert product.startswith('AB =') and product.count(r'\begin{bmatrix}') == 2
product = re.sub(r'\s+', ' ', product).strip().replace(r'\color{blue}', r'\color{#4169E1}').replace(r'\color{red}', r'\color{#C04B4B}')
intro = pieces[0].strip() + '\n\n' + matrix_operands(['A=' + A, 'B=' + B]) + '\n\n' + pieces[1].strip() + '\n\n$$\n' + product + '\n$$\n\n' + pieces[2].strip()
intro = intro.replace(r'\color{blue}', r'\color{#4169E1}').replace(r'\color{red}', r'\color{#C04B4B}')
add(17592186101958, ':tutorial/content', intro,
    'Restore both source matrices, A/B definitions and full attempted product; retain source row/column highlights and use responsive operands.', formulas[2990]['path'])
rule = (HERE / 'tutorial-3800-source-reconstructed.md').read_text().strip()
rule = rule.replace(r'\fbox{n}', r'\boxed{n}').replace(r'\color{blue}', r'\color{#4169E1}').replace(r'\color{red}', r'\color{#C04B4B}')
add(17592186101985, ':tutorial/content', rule,
    'Restore full m×n and n×k dimensions around the nested MathML n fragments; keep source box/color cues.', formulas[3800]['path'])

for q in questions:
    before = q[':question/problem']
    after = responsive_operands(before)
    assert MAT.findall(before) == MAT.findall(after), q[':db/id']
    reasons = []
    if after != before:
        reasons.append('Separate named operands into responsive matrix groups while retaining every label and cell.')
    if q[':db/id'] == 17592186100691:
        after = after.replace('- The product $A\\times B$', '- **I.** The product $A\\times B$').replace('- The product $B\\times A$', '- **II.** The product $B\\times A$')
        reasons.append('Restore source Roman statement labels referenced by the solution.')
    if q[':db/id'] == 17592186101409:
        after = re.sub(r'(?m)^(I{1,3})\. (The product .*?)$', lambda m: '- **' + m[1] + '.** ' + m[2], after)
        after = after.replace('following statement are', 'following statements are')
        reasons.append('Render the three source statements as separate labeled list items.')
    spaced = dimensions(after)
    if spaced != after:
        after = spaced
        reasons.append('Separate the dimension answer from prose and keep both fields with × as one readable unit.')
    if q[':db/id'] in [17592186101410, 17592186101411]:
        after = after.replace(r'\cdot', r'\times')
        reasons.append('Restore the source × dimension separator, replacing an erroneous multiplication dot.')
        evidence = source(q[':question/math-academy-id'][2:])
        soup = BeautifulSoup(evidence['html'], 'html.parser')
        allowed = [re.sub(r'\s+', '', n.get_text()) for n in soup.select('.questionWidget-choiceText math')]
        for f in q[':question/answer-fields']:
            for answer in f[':answer-field/choices']:
                if 'cdot' not in answer[':answer/value']:
                    continue
                old = answer[':answer/value']
                pair = re.fullmatch(r'(\d+)\s+\\+cdot\s+(\d+)', old)
                assert pair and pair[1] + '×' + pair[2] in allowed
                answer_changes.append({'entity': answer[':db/id'], 'attribute': ':answer/value',
                    'before': old, 'after': pair[1] + r' \times ' + pair[2],
                    'reason': 'Restore the original source matrix-dimension notation ×; preserve the answer entity and dimension pair.',
                    'source': evidence['path'], 'question': q[':db/id'],
                    'answer_field': f[':db/id'], 'answer_field_key': f[':answer-field/key'],
                    'source_dimension_pair': [int(pair[1]), int(pair[2])]})
        source_evidence.append({'kind': 'dimension-times', 'question': q[':db/id'],
                                **evidence, 'source_choice_dimensions': allowed})
    if after != before:
        add(q[':db/id'], ':question/problem', after, ' '.join(reasons), q.get(':question/math-academy-id', 'Generated content; current snapshot at basis3269'))
    review.append({'entity': q[':db/id'], 'ma_id': q.get(':question/math-academy-id'),
                   'matrices': [{'label': label, 'rows': len(mat.split(r'\\')),
                                 'columns': len(re.search(r'\{bmatrix\}(.*?)\\end', mat, re.S)[1].split(r'\\')[0].split('&'))}
                                for label, mat in MAT.findall(before)],
                   'existing_solution': bool(q.get(':question/worked-solution')),
                   'missing_solution_deferred': not bool(q.get(':question/worked-solution')),
                   'prompt_changed': after != before})

# These two mistakes are present in the retained Math Academy explanation too.
# Correct only the inconsistent sentence/labels, preserving the correct answer.
q = byid[17592186101321]
evidence = source(22067, True)
assert re.search(r'<mn>3</mn>\s*<mo>×</mo>\s*<mn>2</mn>', evidence['html'])
after = q[':question/worked-solution'].replace('$A$ is a $3\\times 2$ matrix', '$A$ is a $4\\times 2$ matrix')
add(q[':db/id'], ':question/worked-solution', after,
    'Correct an original-source typo: displayed A has four rows and two columns; subsequent source derivation and answer already use four rows.', evidence['path'])
source_evidence.append({'kind': 'original-source-typo', 'question': q[':db/id'], **evidence,
                        'proof': {'A_shape_from_all_displayed_cells': [4, 2], 'B_shape': [2, 4], 'requested_product': 'BA', 'answer_dimensions_unchanged': [2, 2]}})
q = byid[17592186338807]
evidence = source(70702, True)
after = q[':question/worked-solution'].replace(r'{R}_{2\times', r'{S}_{2\times').replace(r'{S}_{\boxed', r'{R}_{\boxed')
add(q[':db/id'], ':question/worked-solution', after,
    'Correct an original-source diagram label swap: S is 2×4, R is 4×5, so the displayed factors must be S then R for SR.', evidence['path'])
source_evidence.append({'kind': 'original-source-label-swap', 'question': q[':db/id'], **evidence,
                        'proof': {'S_shape_from_prompt': [2, 4], 'R_shape_from_prompt': [4, 5], 'requested_product': 'SR', 'answer_dimensions_unchanged': [2, 5]}})

# Existing source statement labels are generated by ol/questionStatements CSS.
for mid, path in [(4403, CAP / 'example-4403.json'), (42374, WORK / 'q-42374-before.json')]:
    raw = json.loads(path.read_text())
    soup = BeautifulSoup(raw['html'], 'html.parser')
    ol = soup.select_one('ol.questionStatements')
    assert ol is not None
    source_evidence.append({'kind': 'statement-order', 'ma_id': mid, 'source': str(path.relative_to(ROOT)),
                           'html': str(ol), 'statement_count': len(ol.find_all('li', recursive=False)),
                           'restored_labels': ['I', 'II'] if mid == 4403 else ['I', 'II', 'III']})

assert len(questions) == 45 and len(tutorials) == 2 and len(answer_changes) == 9
save('content-changes.json', changes)
save('changes.json', changes + answer_changes)
save('answer-changes.json', answer_changes)
save('source-preservation.json', {'identity': snapshot['identity'], 'source_evidence': source_evidence,
     'restored_tutorials': formulas,
     'preserved': ['all question/answer/field identities', 'all answer field keys and correct links',
                   'all displayed matrix cell sequences', 'all difficulties and learner state'],
     'deferred': 'Three wholly missing worked solutions are unchanged.'})
save('review.json', {'identity': snapshot['identity'], 'title': topic[':topic/title'],
     'counts': {'knowledge_points': 3, 'tutorials': 2, 'canonical_examples': 3, 'practice_questions': 42,
                'question_fields_changed': sum(c['attribute'].startswith(':question/') for c in changes),
                'tutorials_restored': 2, 'answer_dimension_notation_repairs': 9,
                'missing_solutions_deferred': sum(x['missing_solution_deferred'] for x in review)},
     'questions': review,
     'root_causes': ['Old extractor preferred the first nested MathML fragment over the complete mixed SVG title.',
                     'Roman ordered-list styles were flattened during capture.',
                     'Dimension controls lost surrounding spacing; joined matrix displays could not wrap.',
                     'Old baseline imported × as dot notation in two questions and their answer values.',
                     'Two source explanations contain independent dimension/label mistakes; generators already correct these.']})
print(json.dumps({'content_changes': len(changes), 'answer_notation_changes': len(answer_changes)}))
