"""Normalize this manual multistep capture from saved HTML; no browser requests or writes to EDB."""
import hashlib
import json
import re
import shutil
from pathlib import Path
from urllib.parse import urljoin

from bs4 import BeautifulSoup, Comment, NavigableString, Tag

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
    if isinstance(n, Comment):
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
    if n.name == 'table':
        rows = [[text(cell) for cell in row.find_all(['td', 'th'], recursive=False)] for row in n.find_all('tr')]
        width = max(map(len, rows), default=0)
        if width:
            lines = ['| ' + ' | '.join(row + [''] * (width-len(row))) + ' |' for row in rows]
            lines.insert(1, '| ' + ' | '.join(['---'] * width) + ' |')
            return '\n\n' + '\n'.join(lines) + '\n\n'
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
    rendered = re.sub(r'[ \t]+', ' ', render(n))
    return re.sub(r'\n{3,}', '\n\n', '\n'.join(line.strip() for line in rendered.splitlines())).strip()


def choice(n, option, dom_id):
    value = text(n)
    typ = 'math' if re.fullmatch(r'\$[^$]+\$', value) else 'image' if value.startswith('![](') else 'text'
    result = {'option': option, 'dom_id': dom_id, 'type': typ,
              'value': value[1:-1] if typ == 'math' else value[4:-1] if typ == 'image' else value,
              'html': n.decode_contents()}
    if typ == 'image':
        result['source_url'] = urljoin(BASE, n.find('img')['src'])
    return result


answers = {a['question_id']: a for a in load('answers.json')}
solutions = {s['id'].replace('questionExplanation-', 'question-'): s for s in load('activity-solutions.json')}
initial = BeautifulSoup((ROOT / 'initial.html').read_text(), 'html.parser')
context = initial.select_one('#step-1')
context_text = text(context)
questions = []
for index, h in enumerate(load('activity-questions.json'), 1):
    qid = h['id'].replace('question-', 'q-')
    live = BeautifulSoup(load(h['id'] + '-live.json')['html'], 'html.parser')
    history = BeautifulSoup(h['html'], 'html.parser')
    assert history.select_one('.answerResult').get_text(strip=True) == 'Correct'
    values = [v.replace('\\\\', '\\') for v in answers[qid]['values']]
    fields = []
    nodes = live.select('.matheditor-wrapper-answer')
    assert len(nodes) == len(values)
    for field_index, (node, value) in enumerate(zip(nodes, values), 1):
        key = f'field-{field_index}'
        fields.append({'key': key, 'type': 'blank', 'tag': 'mathquill',
                       'dom_id': node.get('id'),
                       'locator': {'question_selector': '#' + h['id'],
                                   'field_selector': '.matheditor-wrapper-answer', 'index': field_index - 1},
                       'input_html': str(node), 'correct_value': value,
                       'choices': [{'type': 'math', 'value': value, 'correct': True}]})
        node.replace_with(NavigableString('{{' + key + '}}'))
    tid, kid = map(int, re.fullmatch(r'/topics/(\d+)#(\d+)', h['kp_href']).groups())
    difficulty = history.select_one('.questionDifficulty').get_text(strip=True)
    solution = BeautifulSoup(solutions[h['id']]['html'], 'html.parser')
    questions.append({'math_academy_id': qid,
                      'sequence_position': index, 'topic_id': tid,
                      'knowledge_point_source_id': kid, 'knowledge_point': h['kp_title'].strip(),
                      'difficulty': {'E': 'easy', 'M': 'moderate', 'H': 'hard'}[difficulty],
                      'problem': text(live.select_one('.questionText')),
                      'worked_solution': text(solution), 'answer_fields': fields,
                      'shared_context_ref': 'pool-context',
                      'preceding_question_refs': [q['math_academy_id'] for q in questions],
                      'correct_answer_evidence': 'Entered manually and graded Correct by Math Academy; values preserved in history.',
                      'provenance': {'source_url': BASE + '/learn?taskId=13931219',
                                     'kp_href': h['kp_href'], 'live_file': h['id'] + '-live.json',
                                     'worked_solution_file': 'activity-solutions.json'}})
assert len(questions) == 6 and len(solutions) == 6
assert not unknown_math, unknown_math
save('content.json', {'task_id': 13931219, 'multistep_id': 1780, 'task_type': 'multistep',
                      'title': 'Radical Functions and Polynomials in Geometrical Settings',
                      'content_only': True, 'database_committed': False,
                      'shared_contexts': [{'id': 'pool-context', 'problem': context_text, 'html': str(context)}],
                      'questions': questions, 'canonical_examples': [],
                      'dependency_note': 'Questions are ordered parts of one shared problem. Preceding-question refs retain available context, rather than claim every part is mathematically required.'})
bands = {'rgb(255, 255, 255)': 0, 'white': 0, 'rgb(210, 231, 249)': 1,
         'rgb(165, 207, 243)': 2, 'rgb(120, 182, 237)': 3, 'rgb(74, 158, 232)': 4,
         'rgb(29, 134, 226)': 5, 'rgb(23, 107, 181)': 6}
courses = []
for observed in load('knowledge-state-observed.json'):
    assert sum(int(s.split()[0]) for s in observed['declared_topics']) == len(observed['rows'])
    topics = []
    for row in observed['rows']:
        tid, cid = map(int, re.fullmatch(r'/topics/(\d+)\?courseId=(\d+)', row['href']).groups())
        assert cid == observed['course_id'] and row['color'] in bands
        topics.append({**row, 'topic_id': tid, 'display_band': bands[row['color']]})
    assert len(topics) == len({t['topic_id'] for t in topics})
    courses.append({'course_id': cid, 'captured_at': observed['captured_at'], 'topics': topics})
save('knowledge-state-completed.json', {'task_id': 13931219, 'phase': 'activity-completed',
                                      'courses': courses, 'scope': 'course-progress display colors',
                                      'limitations': 'Displayed repetition bands, not continuous/internal knowledge state; courses read sequentially.'})
verification = {'task_id': 13931219, 'score': '6/6', 'xp': 13,
                'questions': 6, 'answer_fields': sum(len(q['answer_fields']) for q in questions),
                'worked_solutions': 6, 'shared_contexts': 1, 'source_image_urls': len(assets),
                'unique_image_hashes': len({a['sha256'] for a in assets.values()}),
                'snapshot_rows': sum(len(c['topics']) for c in courses),
                'canonical_examples_presented': 0, 'unknown_mathml_tags': sorted(unknown_math),
                'database_committed': False, 'automator_modified': False}
save('verification.json', verification)
print(json.dumps(verification, indent=2))
