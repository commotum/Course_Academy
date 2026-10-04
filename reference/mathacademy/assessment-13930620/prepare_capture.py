"""Normalize this manual assessment capture from saved HTML; no browser requests or writes to EDB."""
import hashlib
import json
import re
import shutil
from pathlib import Path
from urllib.parse import urljoin

from bs4 import BeautifulSoup, NavigableString, Tag

ROOT = Path(__file__).resolve().parent
BASE = 'https://mathacademy.com'


def load(name):
    return json.loads((ROOT / name).read_text())


def save(name, data):
    (ROOT / name).write_text(json.dumps(data, indent=2) + '\n')


assets = {}
(ROOT / 'assets').mkdir(exist_ok=True)
for folder in ('live-assets', 'history-assets'):
    for item in load(folder + '/manifest.json')['assets']:
        if '/graphics/' not in item['url']:
            continue
        source = ROOT / folder / Path(item['path']).name
        suffix = {'image/png': '.png', 'image/svg+xml': '.svg', 'image/jpeg': '.jpg'}[item['contentType']]
        target = ROOT / 'assets' / (item['name'] + suffix)
        shutil.copyfile(source, target)
        digest = hashlib.sha256(target.read_bytes()).hexdigest()
        if item['url'] in assets:
            assert assets[item['url']]['sha256'] == digest
        assets[item['url']] = {**item, 'path': str(target), 'sha256': digest}
save('assets/manifest.json', assets)

OPS = {'−': '-', '±': r'\pm ', '⋅': r'\cdot ', '×': r'\times ', '≠': r'\ne ',
       '≈': r'\approx ', '≤': r'\le ', '≥': r'\ge ', 'π': r'\pi ', 'θ': r'\theta ',
       'α': r'\alpha ', '∞': r'\infty ', '∘': r'\circ ', '\u2061': ''}
unknown_math = set()


def math(n):
    if isinstance(n, NavigableString):
        return OPS.get(str(n), str(n))
    cs = [math(c) for c in n.children]
    tag = n.name.lower()
    if tag in ('mphantom', 'annotation', 'annotation-xml'):
        return ''
    if tag == 'mfrac':
        return r'\frac{' + cs[0] + '}{' + cs[1] + '}'
    if tag in ('msup', 'msub', 'munder', 'mover'):
        if tag == 'mover':
            return r'\overset{' + cs[1] + '}{' + cs[0] + '}'
        return '{' + cs[0] + '}' + ('^' if tag == 'msup' else '_') + '{' + cs[1] + '}'
    if tag in ('msubsup', 'munderover'):
        return '{' + cs[0] + '}_{' + cs[1] + '}^{' + cs[2] + '}'
    if tag == 'msqrt':
        return r'\sqrt{' + ''.join(cs) + '}'
    if tag == 'mroot':
        return r'\sqrt[' + cs[1] + ']{' + cs[0] + '}'
    if tag == 'mspace':
        return r'\,'
    if tag == 'mtext':
        return r'\text{' + n.get_text() + '}'
    if tag in ('mo', 'mi'):
        return OPS.get(n.get_text(), n.get_text())
    if tag == 'mtable':
        return r'\begin{aligned}' + r' \\ '.join(cs) + r'\end{aligned}'
    if tag in ('mtr', 'mlabeledtr'):
        return ' & '.join(cs)
    if tag == 'menclose':
        return r'\cancel{' + ''.join(cs) + '}' if 'strike' in n.get('notation', '') else ''.join(cs)
    if tag == 'semantics':
        return cs[0]
    if tag not in ('math', 'mrow', 'mn', 'mtd', 'mstyle', 'mpadded'):
        unknown_math.add(tag)
    return ''.join(cs)


def render(n):
    if n is None:
        return ''
    if isinstance(n, NavigableString):
        return str(n)
    if not isinstance(n, Tag):
        return ''
    if n.name in ('script', 'style', 'mjx-assistive-mml'):
        return ''
    classes = n.get('class', [])
    if 'matheditor-wrapper-answer' in classes:
        return '{{field-1}}'
    if n.name in ('mjx-container', 'math'):
        m = n if n.name == 'math' else n.find('math')
        assert m is not None, 'Missing assistive MathML'
        tex = math(m)
        return '\n\n$$\n' + tex + '\n$$\n\n' if n.get('display') == 'true' else '$' + tex + '$'
    if n.name == 'img':
        url = urljoin(BASE, n['src'])
        assert url in assets, 'Uncaptured image: ' + url
        return '![](' + assets[url]['path'] + ')'
    children = ''.join(render(c) for c in n.children)
    if n.name == 'br':
        return '\n'
    if n.name == 'li':
        return '- ' + children.strip() + '\n'
    if n.name in ('strong', 'b'):
        return '**' + children + '**'
    if n.name in ('em', 'i'):
        return '*' + children + '*'
    if n.name in ('p', 'div', 'ul', 'ol'):
        return '\n\n' + children + '\n\n'
    return children


def text(n):
    return re.sub(r'\n{3,}', '\n\n', render(n)).strip()


def choice(n, option, dom_id):
    value = text(n)
    typ = 'math' if re.fullmatch(r'\$[^$]+\$', value) else 'image' if value.startswith('![](') else 'text'
    result = {'option': option, 'dom_id': dom_id, 'type': typ,
              'value': value[1:-1] if typ == 'math' else value[4:-1] if typ == 'image' else value,
              'html': n.decode_contents()}
    if typ == 'image':
        result['source_url'] = urljoin(BASE, n.find('img')['src'])
    return result


answers = {a['id']: a for a in load('answers.json')}
history = load('activity-questions.json')
questions = []
for h in history:
    assert h['result'] == 'Correct' and h['worked_solution_visible']
    live = load(h['id'] + '-live.json')
    dom = BeautifulSoup(live['html'], 'html.parser')
    solution = BeautifulSoup(h['worked_solution_html'], 'html.parser')
    a = answers[h['id']]
    fields = []
    if live['choices']:
        options = []
        for c in live['choices']:
            row = BeautifulSoup(c['row_html'], 'html.parser')
            options.append(choice(row.select_one('.choiceText'), c['label'], c['id']))
        correct = next(c for c in options if c['option'] == a['correct_choice'])
        fields.append({'key': 'selection', 'type': 'radio', 'choices': options,
                       'correct_value': correct['value']})
    else:
        node = dom.select_one('.matheditor-wrapper-answer')
        assert node is not None
        fields.append({'key': 'field-1', 'type': 'blank', 'tag': 'mathquill',
                       'dom_id': node['id'], 'input_html': str(node), 'choices': [], 'correct_value': a['answer']})
    topic_id, source_kp = map(int, re.fullmatch(r'/topics/(\d+)#(\d+)', h['kp_href']).groups())
    graphic = dom.select_one('img#questionGraphic')
    problem = '\n\n'.join(filter(None, [text(graphic), text(dom.select_one('.questionText'))]))
    q = {'math_academy_id': h['id'].replace('question-', 'q-'),
         'topic_id': topic_id, 'knowledge_point_source_id': source_kp, 'knowledge_point': h['kp_title'],
         'difficulty': {'E': 'easy', 'M': 'moderate', 'H': 'hard'}[h['difficulty']],
         'problem': problem, 'worked_solution': text(solution), 'answer_fields': fields,
         'correct_answer_evidence': {'source': 'manual solution, verified by site Correct grade', 'reason': a['reason']},
         'provenance': {'activity_question': h['id'], 'kp_href': h['kp_href'],
                        'source_url': 'https://mathacademy.com/learn?taskId=13930620'}}
    instructions = dom.select_one('.calculatorInstructions')
    if instructions:
        q['calculator_instructions'] = text(instructions)
    assert q['problem'] and q['worked_solution'] and all(f['correct_value'] for f in fields)
    assert len(fields) == 1
    if fields[0]['type'] == 'radio':
        assert len(fields[0]['choices']) == 5
    questions.append(q)
assert not unknown_math, unknown_math
assert len(questions) == len(answers) == 8
content = {'task_id': 13930620, 'test_id': 589340, 'task_type': 'assessment',
           'content_only': True, 'questions': questions, 'canonical_examples': [],
           'database_committed': False}
if (ROOT / 'content.json').exists():
    prior = load('content.json')
    if 'database_read_basis' in prior:
        content['database_read_basis'] = prior['database_read_basis']
    prior_questions = {q['math_academy_id']: q for q in prior.get('questions', [])}
    for q in questions:
        for key in ('knowledge_point_id', 'database_match_at_capture'):
            if key in prior_questions.get(q['math_academy_id'], {}):
                q[key] = prior_questions[q['math_academy_id']][key]
save('content.json', content)
save('solutions-extracted.json', [{'math_academy_id': q['math_academy_id'], 'worked_solution': q['worked_solution']} for q in questions])

bands = {'rgb(255, 255, 255)': 0, 'white': 0, 'rgb(210, 231, 249)': 1, 'rgb(165, 207, 243)': 2,
         'rgb(120, 182, 237)': 3, 'rgb(74, 158, 232)': 4, 'rgb(29, 134, 226)': 5, 'rgb(23, 107, 181)': 6}
snapshot = load('knowledge-state-observed.json')
courses = []
for c in snapshot['courses']:
    o = c['observed']
    assert sum(int(s.split()[0]) for s in o['declared_topics']) == len(o['rows'])
    topics = []
    for row in o['rows']:
        tid, cid = map(int, re.fullmatch(r'/topics/(\d+)\?courseId=(\d+)', row['href']).groups())
        assert cid == c['course_id'] and row['color'] in bands
        topics.append({**row, 'topic_id': tid, 'display_band': bands[row['color']]})
    assert len(topics) == len({t['topic_id'] for t in topics})
    courses.append({'course_id': c['course_id'], 'captured_at': c['captured_at'], 'topics': topics,
                    'source_url': BASE + '/courses/' + str(c['course_id']) + '/progress', 'units_html': o['units_html']})
snapshot['courses'] = courses
snapshot.update(scope='course-progress display colors', comparison_available=False,
                limitations='Displayed bands only, not exact continuous repetition or full internal knowledge state; courses read sequentially.')
save('knowledge-state-completed.json', snapshot)
verification = {'task_id': 13930620, 'score': '8/8', 'xp': 18, 'questions': len(questions),
                'radio_questions': sum(q['answer_fields'][0]['type'] == 'radio' for q in questions),
                'blank_questions': sum(q['answer_fields'][0]['type'] == 'blank' for q in questions),
                'worked_solutions': sum(bool(q['worked_solution']) for q in questions),
                'choice_count': sum(len(q['answer_fields'][0]['choices']) for q in questions),
                'question_image_urls': len(assets), 'unique_image_hashes': len({a['sha256'] for a in assets.values()}),
                'snapshot_rows': sum(len(c['topics']) for c in courses),
                'canonical_examples_presented': 0, 'unknown_mathml_tags': sorted(unknown_math),
                'database_committed': False, 'automator_modified': False}
save('verification.json', verification)
print(json.dumps(verification, indent=2))
