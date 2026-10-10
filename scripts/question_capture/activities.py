"""Math Academy activity definitions: capture source order and preserve EDB identities."""
import copy
import re
import time
import uuid
from email.utils import parsedate_to_datetime
from pathlib import Path
from urllib.parse import urljoin

from core import atomic_json, stable_id
from edn import kw

ACTIVITY_ATTRIBUTES = {
    'activity/id', 'activity/title', 'activity/type', 'activity/scope',
    'activity/steps', 'activity/first-step', 'step/id', 'step/math-academy-id',
    'step/content', 'step/next', 'tutorial/id', 'tutorial/math-academy-id',
    'tutorial/title', 'tutorial/content', 'knowledge-point/title',
    'knowledge-point/canonical-example', 'topic/title', 'multistep/id',
    'multistep/context', 'multistep/steps', 'multistep/first-step',
    'assigned-problem/id', 'assigned-problem/content', 'assigned-problem/topic-coverage',
}
IDENTITIES = ('activity/id', 'step/id', 'tutorial/id', 'knowledge-point/id',
              'question/id', 'topic/id', 'multistep/id', 'assigned-problem/id')


def source_uuid(kind, value):
    # Same namespace as the baseline and newer-capture migration.
    return uuid.uuid5(uuid.NAMESPACE_URL, f'course-academy:ma:{kind}:{value}')


def ref(attr, value):
    return [kw(attr), value]


def identity_ref(entity):
    for attr in IDENTITIES:
        if ':' + attr in entity:
            return ref(attr, entity[':' + attr])
    if ':db/ident' in entity:
        return entity[':db/ident']
    return entity[':db/id']


def _point_for_example(points, mid, title):
    matches = [kp for kp in points if kp.get(':knowledge-point/canonical-example', {}).get(':question/math-academy-id') == mid]
    if len(matches) > 1:
        normalize = lambda value: re.sub(r'\s+', ' ', value).strip()
        matches = [kp for kp in matches if normalize(kp.get(':knowledge-point/title', '')) == normalize(title)]
        if len(matches) != 1:
            raise ValueError('Canonical example maps to multiple knowledge points; review source title')
    return matches[0] if matches else None


def _value(value):
    if isinstance(value, dict):
        return _value(identity_ref(value))
    if isinstance(value, (tuple, list)):
        return tuple(_value(v) for v in value)
    return value


def _formula_html(html):
    from bs4 import BeautifulSoup, NavigableString
    soup = BeautifulSoup(html, 'html.parser')
    for node in soup.select('.mjpage, mjx-container, .MathJax'):
        if node.parent is None:
            continue
        tex = node.select_one('annotation[encoding="application/x-tex"]')
        if tex is None:
            tex = node.select_one('svg > title')
        if tex is not None and not tex.find('math') and tex.get_text().strip():
            display = ('mjpage__block' in node.get('class', []) or
                       node.get('display') == 'true' or node.get('display') == 'block')
            marker = '$$' if display else '$'
            node.replace_with(NavigableString(marker + tex.get_text().strip() + marker))
    return str(soup)


def html_to_markdown(html):
    """Render source text, math, tables and canonical image paths; discard UI/comments."""
    from bs4 import BeautifulSoup, Comment, NavigableString
    soup = BeautifulSoup(_formula_html(html), 'html.parser')
    for node in soup.select('script, style, head, .stepHeader, .helpButton, .explanationHeader'):
        node.decompose()

    def render(node):
        if isinstance(node, Comment):
            return ''
        if isinstance(node, NavigableString):
            return re.sub(r'[\t\r\n ]+', ' ', str(node))
        name = node.name
        body = ''.join(render(c) for c in node.children)
        if name == 'img':
            src = node.get('src', '')
            if not src.startswith('images/'):
                raise ValueError('Tutorial has an unresolved image: ' + src)
            return '![' + node.get('alt', '').replace(']', '') + '](' + src + ')'
        if name in ('svg', 'canvas', 'math'):
            raise ValueError('Tutorial has an unresolved graphic or formula')
        if name == 'br':
            return '\n'
        if name in ('strong', 'b'):
            return '**' + body.strip() + '**'
        if name in ('em', 'i'):
            return '*' + body.strip() + '*'
        if name == 'a':
            href = node.get('href', '')
            return '[' + body.strip() + '](' + urljoin('https://mathacademy.com/', href) + ')' if href else body
        if name in ('ul', 'ol'):
            lines = []
            for i, child in enumerate(node.find_all('li', recursive=False), 1):
                lines.append((str(i) + '. ' if name == 'ol' else '- ') + render(child).strip())
            return '\n\n' + '\n'.join(lines) + '\n\n'
        if name == 'table':
            rows = [[render(c).strip().replace('|', '\\|').replace('\n', '<br>')
                     for c in row.find_all(['td', 'th'], recursive=False)]
                    for row in node.find_all('tr')]
            rows = [r for r in rows if r]
            if not rows or len({len(r) for r in rows}) != 1 or node.select('[rowspan], [colspan]'):
                # Preserve source structure for tables Markdown cannot express.
                return '\n\n' + str(node) + '\n\n'
            lines = ['| ' + ' | '.join(r) + ' |' for r in rows]
            lines.insert(1, '| ' + ' | '.join('---' for _ in rows[0]) + ' |')
            return '\n\n' + '\n'.join(lines) + '\n\n'
        if name and re.fullmatch('h[1-6]', name):
            return '\n\n' + '#' * int(name[1]) + ' ' + body.strip() + '\n\n'
        if name in ('p', 'div', 'blockquote', 'section'):
            return '\n\n' + body.strip() + '\n\n'
        if name in ('sup', 'sub'):
            return '<' + name + '>' + body + '</' + name + '>'
        return body

    text = render(soup)
    return re.sub(r'\n[ \t]*\n(?:[ \t]*\n)+', '\n\n', text).strip()


def parse_lesson_html(html, topic_id, render_html=html_to_markdown):
    """The topic page exposes MA stepId/stepType/contentId, in source DOM order."""
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.select_one('#topicName')
    nodes = soup.select('div.step[stepid][steptype][contentid]')
    if title is None or not title.get_text(strip=True) or not nodes:
        raise ValueError('Topic page lacks a complete lesson definition')
    steps, tutorials, examples = [], [], []
    for node in nodes:
        kind, title_node = node['steptype'], node.select_one('.stepName')
        if kind not in ('tutorial', 'example') or title_node is None:
            raise ValueError('Unknown lesson step type or missing source title')
        step_id, content_id = int(node['stepid']), int(node['contentid'])
        if step_id < 1 or content_id < 1:
            raise ValueError('Invalid MA lesson placement identity')
        name = re.sub(r'^Example:\s*', '', title_node.get_text(' ', strip=True)).strip()
        steps.append({'math_academy_id': step_id, 'type': kind, 'content_id': content_id, 'title': name})
        if kind == 'tutorial':
            body = copy.copy(node)
            for ui in body.select('.stepHeader, .helpButton'):
                ui.decompose()
            text = render_html(str(body))
            if not text:
                raise ValueError('Empty tutorial body: ' + str(content_id))
            tutorials.append({'math_academy_id': content_id, 'title': name, 'content': text})
        else:
            problem, solution = node.select_one('.exampleQuestion'), node.select_one('.exampleExplanation')
            if problem is None or solution is None:
                raise ValueError('Canonical example lacks its source problem/solution')
            examples.append({'math_academy_id': 'e-' + str(content_id), 'knowledge_point': name,
                             'problem': render_html(str(problem)), 'worked_solution': render_html(str(solution)),
                             'answer_fields': [], 'missing_source_fields': ['answer_fields', 'difficulty'],
                             'source_kind': 'topic_page_example'})
    if len({s['math_academy_id'] for s in steps}) != len(steps):
        raise ValueError('Duplicate lesson placement ID')
    if len({(s['type'], s['content_id']) for s in steps}) != len(steps):
        raise ValueError('Repeated lesson content needs explicit placement review')
    return {'topic_id': topic_id, 'title': title.get_text(' ', strip=True), 'complete': True,
            'source_url': f'https://mathacademy.com/topics/{topic_id}', 'steps': steps}, tutorials, examples


def capture_lesson(reader, state, directory, topic):
    """Read the definition using the current authenticated account, without taking a task."""
    from image_library import ImageLibrary, capture_html_images
    from bs4 import BeautifulSoup
    from browser import AccessBlocked, RateLimited
    directory = Path(directory)
    url = f'https://mathacademy.com/topics/{state["topic_id"]}'
    response = reader.page.context.request.get(url, timeout=reader.args.timeout_ms)

    def check_response(item):
        status = getattr(item, 'status', 200)
        if status == 429:
            value = item.headers.get('retry-after', '')
            try:
                retry = int(value) if re.fullmatch(r'\d{1,7}', value) else max(0, parsedate_to_datetime(value).timestamp() - time.time())
            except (ValueError, TypeError, OverflowError):
                retry = 30
            raise RateLimited(retry)
        if status in (401, 403) or re.search(r'/(login|signin|session-expired)(?:/|\?|$)', getattr(item, 'url', '')):
            raise AccessBlocked('Authentication required for lesson source capture; use the login command')
        if not item.ok:
            raise ValueError('Lesson source request failed with HTTP ' + str(status))

    check_response(response)
    html = response.text()
    if BeautifulSoup(html, 'html.parser').select_one('input[type="password"], iframe[src*="captcha"], #challenge-form, .cf-challenge'):
        raise AccessBlocked('Lesson source request returned an authentication or challenge page')
    source_file = directory / 'lesson-topic.html'
    source_file.write_text(html)
    library = ImageLibrary(Path(getattr(reader.args, 'math_root', '/media/jake/SSD/EDB/math')))

    def fetch(url):
        item = reader.image_responses.get(url)
        if item is None:
            item = reader.page.context.request.get(url, timeout=reader.args.timeout_ms)
        check_response(item)
        return item.body(), item.headers.get('content-type', '').split(';')[0]

    def render(fragment):
        cleaned = _formula_html(fragment)
        localized = capture_html_images(cleaned, page_url=url, fetch_response=fetch,
                                        library=library, evidence_dir=directory,
                                        document_html=html)
        return html_to_markdown(localized)

    definition, tutorials, examples = parse_lesson_html(html, state['topic_id'], render)
    definition['source_file'] = str(source_file.resolve())
    # Resolve by canonical example ID, never by a changed title alone.
    existing = topic.get(':topic/knowledge-points', [])
    new_points = []
    for example in examples:
        mid = example['math_academy_id']
        kp = _point_for_example(existing, mid, example['knowledge_point'])
        captured = state.get('examples', {}).get(mid)
        kid = (str(kp[':knowledge-point/id']) if kp else
               captured['knowledge_point_id'] if captured else
               str(stable_id('knowledge-point', f'{state["topic_id"]}:{mid}')))
        example.update(knowledge_point_id=kid, topic_id=state['topic_id'], source_file=str(source_file.resolve()))
        original = BeautifulSoup(html, 'html.parser').select_one(
            f'div.step[steptype="example"][contentid="{mid[2:]}"]')
        atomic_json(directory / ('lesson-example-' + mid[2:] + '.json'),
                    {'problem': example['problem'], 'worked_solution': example['worked_solution'],
                     'fields': [], 'errors': [], 'html': str(original),
                     'source_file': str(source_file.resolve())})
        if not kp:
            new_points.append({'id': kid, 'title': example['knowledge_point'], 'source_example_id': mid})
    state['lesson_definition'] = definition
    state['tutorials'] = tutorials
    state['lesson_examples'] = examples
    state['lesson_new_knowledge_points'] = new_points
    atomic_json(directory / 'lesson-definition.json', {'lesson_definition': definition, 'tutorials': tutorials,
                                                      'canonical_examples': examples, 'new_knowledge_points': new_points})
    atomic_json(directory / 'state.json', state)
    return definition


CONTENT_PULL = '''[:db/id :tutorial/id :tutorial/math-academy-id :tutorial/title :tutorial/content
 :knowledge-point/id :knowledge-point/title :question/id :question/math-academy-id
 {:knowledge-point/canonical-example [:db/id :question/id :question/math-academy-id]}]'''
STEP_PULL = '[* {:step/next [:db/id :step/id]} {:step/content ' + CONTENT_PULL + '}]'
LESSON_PULL = '[* {:activity/type [:db/ident]} {:activity/scope [:db/id :topic/id :topic/math-academy-id]} {:activity/first-step [:db/id :step/id]} {:activity/steps ' + STEP_PULL + '}]'
MULTISTEP_PULL = '[* {:multistep/first-step [:db/id :step/id]} {:multistep/steps ' + STEP_PULL + '}]'


def load_activity_snapshot(database, content, directory, basis):
    """Read every identity used by an activity plan from one immutable basis."""
    snapshot = {'lessons': {}, 'tutorials': {}, 'source_steps': {}, 'multisteps': {}, 'assigned_problems': {}, 'activities': {}}
    definition = content.get('lesson_definition')
    if definition:
        tid = definition['topic_id']
        rows = database.query('[:find (pull ?a ' + LESSON_PULL + ''') :in $ ?tid
 :where [?t :topic/math-academy-id ?tid] [?a :activity/scope ?t]
 [?a :activity/type :activity.type/lesson]]''', [tid], directory, 'lesson-definition-before', basis)
        if len(rows) > 1:
            raise ValueError('More than one existing lesson activity for this topic')
        if rows:
            snapshot['lessons'][tid] = rows[0][0]
        ids = [s['content_id'] for s in definition['steps'] if s['type'] == 'tutorial']
        if ids:
            rows = database.query('[:find (pull ?t [*]) :in $ [?id ...] :where [?t :tutorial/math-academy-id ?id]]',
                                  [ids], directory, 'tutorials-before', basis)
            snapshot['tutorials'] = {t[':tutorial/math-academy-id']: t for [t] in rows}
        ids = [s['math_academy_id'] for s in definition['steps']]
        rows = database.query('[:find (pull ?s ' + STEP_PULL + ') :in $ [?id ...] :where [?s :step/math-academy-id ?id]]',
                              [ids], directory, 'placements-before', basis)
        snapshot['source_steps'] = {s[':step/math-academy-id']: s for [s] in rows}
    if content.get('task_type') == 'multistep':
        sid = content['multistep_id']
        specs = [('multisteps', 'multistep', source_uuid('multistep', sid), MULTISTEP_PULL),
                 ('assigned_problems', 'assigned-problem', source_uuid('multistep-assigned-problem', sid),
                  '[* {:assigned-problem/content [:db/id :multistep/id]} {:assigned-problem/topic-coverage [:db/id :topic/id]}]'),
                 ('activities', 'activity', source_uuid('multistep-activity', sid),
                  '[* {:activity/type [:db/ident]} {:activity/first-step [:db/id :step/id]} {:activity/steps [* {:step/next [:db/id :step/id]} {:step/content [:db/id :assigned-problem/id]}]}]')]
        for bucket, kind, identity, pull in specs:
            rows = database.query('[:find (pull ?e ' + pull + ') :in $ ?id :where [?e :' + kind + '/id ?id]]',
                                  [identity], directory, kind + '-before', basis)
            if rows:
                snapshot[bucket][str(identity)] = rows[0][0]
    return snapshot


class _Plan:
    def __init__(self, question_transaction):
        self.forms, self.retractions, self.decisions = [], [], []
        self.local = {}
        def visit(value):
            if isinstance(value, dict):
                if ':db/id' in value:
                    for attr in IDENTITIES:
                        if ':' + attr in value:
                            self.local[(kw(attr), value[':' + attr])] = value[':db/id']
                for child in value.values():
                    visit(child)
            elif isinstance(value, list):
                for child in value:
                    visit(child)
        visit(question_transaction)

    def reference(self, kind, identity, old=None):
        key = (kw(kind + '/id'), identity)
        return self.local.get(key, ref(kind + '/id', identity)) if old else self.local.get(key, kind + '-' + str(identity))

    def entity(self, kind, identity, old, values, many=()):
        target = self.reference(kind, identity, old)
        update = {kw('db/id'): target}
        if not old:
            update[kw(kind + '/id')] = identity
        for attr, desired in values.items():
            attr = kw(attr)
            previous = (old or {}).get(attr)
            if attr in many:
                previous = previous or []
                old_keys = {_value(v): v for v in previous}
                new_keys = {_value(v): v for v in desired}
                for key in old_keys.keys() - new_keys.keys():
                    self.retract(old, kind, identity, attr, old_keys[key])
                additions = [new_keys[k] for k in new_keys.keys() - old_keys.keys()]
                if additions:
                    update[attr] = sorted(additions, key=str)
            elif desired is None:
                if previous is not None:
                    self.retract(old, kind, identity, attr, previous)
            elif _value(previous) != _value(desired):
                update[attr] = desired
                if previous is not None:
                    self.guard(old, attr, previous)
        if len(update) > 1:
            update[kw('db/ensure')] = kw('topic/identity-validate' if kind == 'topic' else kind + '/validate')
            self.forms.append(update)
        self.local[(kw(kind + '/id'), identity)] = target
        return target

    def guard(self, old, attr, value):
        if old and ':db/id' in old:
            self.retractions.append([old[':db/id'], kw(attr), value.get(':db/id') if isinstance(value, dict) else value])

    def retract(self, old, kind, identity, attr, value):
        self.forms.append([kw('db/retract'), self.reference(kind, identity, old), kw(attr),
                           identity_ref(value) if isinstance(value, dict) else value])
        self.guard(old, attr, value)


def _ordered(old, kind):
    if not old:
        return []
    steps = {str(s[':step/id']): s for s in old.get(':' + kind + '/steps', [])}
    first = old.get(':' + kind + '/first-step')
    current = str(first[':step/id']) if first else None
    result = []
    while current:
        if current not in steps or current in {str(s[':step/id']) for s in result}:
            raise ValueError('Existing activity has an invalid step route')
        step = steps[current]
        result.append(step)
        current = str(step[':step/next'][':step/id']) if step.get(':step/next') else None
    if len(result) != len(steps):
        raise ValueError('Existing activity contains unreachable steps')
    return result


def _step_key(step):
    c = step[':step/content']
    if ':tutorial/id' in c:
        return ('tutorial', c.get(':tutorial/math-academy-id'))
    if ':knowledge-point/id' in c:
        mid = c.get(':knowledge-point/canonical-example', {}).get(':question/math-academy-id', '')
        return ('example', int(mid[2:])) if re.fullmatch(r'e-\d+', mid) else ('unknown', str(c[':knowledge-point/id']))
    return ('question', c.get(':question/math-academy-id'))


def _lesson(plan, content, topics, snapshot):
    definition = content['lesson_definition']
    if not definition.get('complete') or not definition.get('steps'):
        raise ValueError('A complete source lesson definition is required')
    tid, desired = definition['topic_id'], definition['steps']
    topic, old = topics[tid], snapshot['lessons'].get(tid)
    old_order = _ordered(old, 'activity')
    old_keys = {_step_key(s): s for s in old_order}
    if len(old_keys) != len(old_order):
        raise ValueError('Existing lesson has ambiguous repeated content')
    wanted = {(s['type'], s['content_id']) for s in desired}
    if len(wanted) != len(desired):
        raise ValueError('Repeated source lesson content needs review')
    matches = [old_keys.get((s['type'], s['content_id'])) for s in desired]
    used = {str(s[':step/id']) for s in matches if s}
    # Identity replacement requires one missing tutorial between the same matched
    # neighbors AND an unchanged title. Position alone cannot merge two entities.
    for index, item in enumerate(desired):
        if matches[index] or item['type'] != 'tutorial':
            continue
        before = next((matches[i] for i in range(index - 1, -1, -1) if matches[i]), None)
        after = next((matches[i] for i in range(index + 1, len(desired)) if matches[i]), None)
        start = old_order.index(before) + 1 if before else 0
        stop = old_order.index(after) if after else len(old_order)
        candidates = [s for s in old_order[start:stop] if str(s[':step/id']) not in used]
        pending = [i for i in range(index + 1, len(desired)) if not matches[i] and
                   (after is None or i < next(j for j in range(index + 1, len(desired)) if matches[j] is after))]
        candidates = [s for s in candidates if _step_key(s)[0] == 'tutorial']
        if len(candidates) == 1 and not pending:
            previous = candidates[0]
            if previous[':step/content'].get(':tutorial/title', '').strip() != item['title'].strip():
                raise ValueError('Possible tutorial replacement changed identity and title; review before import')
            matches[index] = previous
            used.add(str(previous[':step/id']))
            plan.decisions.append({'kind': 'tutorial_identity_update', 'previous_source_id': _step_key(previous)[1],
                                   'source_id': item['content_id'], 'tutorial_id': str(previous[':step/content'][':tutorial/id']),
                                   'evidence': 'same title and unique position between preserved neighboring sections'})
    tutorials = {t['math_academy_id']: t for t in content.get('tutorials', [])}
    points = topic.get(':topic/knowledge-points', [])
    new_points = {p['source_example_id']: p for p in content.get('new_knowledge_points', [])}
    sequence = []
    for item, previous in zip(desired, matches):
        step_uuid = previous[':step/id'] if previous else source_uuid('step', item['math_academy_id'])
        occupied = snapshot['source_steps'].get(item['math_academy_id'])
        if occupied and occupied[':step/id'] != step_uuid:
            raise ValueError('MA placement identity already belongs to a different step')
        if item['type'] == 'tutorial':
            captured = tutorials.get(item['content_id'])
            if not captured or not captured.get('content'):
                raise ValueError('Lesson tutorial body is missing')
            old_tutorial = (previous[':step/content'] if previous else snapshot['tutorials'].get(item['content_id']))
            tutorial_uuid = old_tutorial[':tutorial/id'] if old_tutorial else source_uuid('tutorial', item['content_id'])
            conflict = snapshot['tutorials'].get(item['content_id'])
            if conflict and conflict[':tutorial/id'] != tutorial_uuid:
                raise ValueError('Replacement tutorial source ID resolves to another existing entity')
            target = plan.entity('tutorial', tutorial_uuid, old_tutorial,
                                 {'tutorial/math-academy-id': item['content_id'], 'tutorial/title': captured['title'],
                                  'tutorial/content': captured['content']})
        else:
            mid = 'e-' + str(item['content_id'])
            kp = _point_for_example(points, mid, item['title'])
            if kp:
                target = plan.entity('knowledge-point', kp[':knowledge-point/id'], kp,
                                     {'knowledge-point/title': item['title']})
            else:
                point = new_points.get(mid)
                if not point:
                    raise ValueError('Lesson canonical example has no prepared knowledge point: ' + mid)
                key = (kw('knowledge-point/id'), uuid.UUID(str(point['id'])))
                if key not in plan.local:
                    raise ValueError('New lesson knowledge point is absent from question transaction: ' + mid)
                target = plan.local[key]
        sequence.append((step_uuid, previous, item['math_academy_id'], target))
    refs = [plan.reference('step', sid, prev) for sid, prev, _, _ in sequence]
    for i, (sid, prev, maid, target) in enumerate(sequence):
        plan.entity('step', sid, prev, {'step/math-academy-id': maid, 'step/content': target,
                                      'step/next': refs[i + 1] if i + 1 < len(refs) else None})
    aid = old[':activity/id'] if old else source_uuid('lesson', tid)
    plan.entity('activity', aid, old, {'activity/title': definition['title'], 'activity/type': kw('activity.type/lesson'),
                                     'activity/scope': identity_ref(topic), 'activity/steps': refs,
                                     'activity/first-step': refs[0]}, many=(kw('activity/steps'),))
    retained = {sid for sid, _, _, _ in sequence}
    for step in old_order:
        if step[':step/id'] not in retained and step.get(':step/next'):
            plan.retract(step, 'step', step[':step/id'], 'step/next', step[':step/next'])
    plan.entity('topic', topic[':topic/id'], topic, {'topic/title': definition['title']})
    plan.decisions.append({'kind': 'lesson', 'topic_id': tid, 'steps': len(sequence),
                           'reused_steps': sum(previous is not None for _, previous, _, _ in sequence),
                           'removed_steps': len(old_order) - len(retained & {s[':step/id'] for s in old_order})})


def _multistep(plan, content, topics, snapshot):
    source_id, mids = content['multistep_id'], content.get('question_order', [])
    questions = {q['math_academy_id']: q for q in content['questions']}
    if not mids or len(set(mids)) != len(mids) or set(mids) != set(questions):
        raise ValueError('Full multistep preparation requires all original question parts')
    uid = source_uuid('multistep', source_id)
    old = snapshot['multisteps'].get(str(uid))
    old_order = _ordered(old, 'multistep')
    previous = {s[':step/content'][':question/math-academy-id']: s for s in old_order}
    if len(previous) != len(old_order):
        raise ValueError('Existing multistep repeats a question identity')
    # Source step-N values in multistep pages are UI ordinal IDs, not verified
    # global MA placement IDs. Retain as evidence only, never step/math-academy-id.
    sequence = []
    for index, mid in enumerate(mids):
        q = questions[mid]
        if not q.get('local_problem') or q['problem'] != q['local_problem']:
            raise ValueError('Multistep question must use its original local problem')
        prev = previous.get(mid)
        sid = prev[':step/id'] if prev else source_uuid('multistep-step', f'{source_id}:{index}:{mid}')
        candidates = [target for (attr, ident), target in plan.local.items() if attr == ':question/id'
                      and any(isinstance(f, dict) and f.get(':question/id') == ident and
                              f.get(':question/math-academy-id') == mid for f in plan.question_transaction)]
        target = (identity_ref(prev[':step/content']) if prev else
                  candidates[0] if candidates else ref('question/math-academy-id', mid))
        # Existing entities are safe lookup refs; new entities must use their tempid.
        sequence.append((sid, prev, target))
    refs = [plan.reference('step', sid, prev) for sid, prev, _ in sequence]
    for i, (sid, prev, target) in enumerate(sequence):
        plan.entity('step', sid, prev, {'step/content': target, 'step/next': refs[i + 1] if i + 1 < len(refs) else None})
    contexts = content.get('shared_contexts', [])
    context = '\n\n'.join(c['problem'].strip() for c in contexts if c.get('problem', '').strip()) or None
    target = plan.entity('multistep', uid, old, {'multistep/context': context, 'multistep/steps': refs,
                                              'multistep/first-step': refs[0]}, many=(kw('multistep/steps'),))
    for step in old_order:
        if step[':step/content'][':question/math-academy-id'] not in mids and step.get(':step/next'):
            plan.retract(step, 'step', step[':step/id'], 'step/next', step[':step/next'])
    pid = source_uuid('multistep-assigned-problem', source_id)
    pold = snapshot['assigned_problems'].get(str(pid))
    coverage = [identity_ref(topics[tid]) for tid in sorted({q['topic_id'] for q in questions.values()})]
    assigned = plan.entity('assigned-problem', pid, pold, {'assigned-problem/content': target,
                                                         'assigned-problem/topic-coverage': coverage},
                           many=(kw('assigned-problem/topic-coverage'),))
    aid = source_uuid('multistep-activity', source_id)
    aold = snapshot['activities'].get(str(aid))
    outer_order = _ordered(aold, 'activity')
    if len(outer_order) > 1:
        raise ValueError('Multistep wrapper has additional authored steps; review before replacing')
    outer_old = outer_order[0] if outer_order else None
    outer_id = outer_old[':step/id'] if outer_old else source_uuid('multistep-outer-step', source_id)
    outer = plan.entity('step', outer_id, outer_old, {'step/content': assigned, 'step/next': None})
    if not content.get('title'):
        raise ValueError('Multistep source title is missing')
    plan.entity('activity', aid, aold, {'activity/title': content['title'], 'activity/type': kw('activity.type/assignment'),
                                      'activity/steps': [outer], 'activity/first-step': outer}, many=(kw('activity/steps'),))
    plan.decisions.append({'kind': 'multistep', 'source_id': source_id, 'steps': len(sequence),
                           'reused_steps': sum(prev is not None for _, prev, _ in sequence)})


def build_activity_transaction(content, topics, snapshot, question_transaction):
    plan = _Plan(question_transaction)
    plan.question_transaction = question_transaction
    if content.get('lesson_definition'):
        _lesson(plan, content, topics, snapshot)
    if content.get('task_type') == 'multistep':
        _multistep(plan, content, topics, snapshot)
    return plan.forms, {'decisions': plan.decisions, 'retractions': plan.retractions,
                        'transaction_forms': len(plan.forms)}
