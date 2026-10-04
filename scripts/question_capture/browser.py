"""Sequential Playwright UI capture with checkpoints before every submission."""
import json
import hashlib
import logging
import re
import time
from pathlib import Path
from urllib.parse import urlparse

from core import atomic_json, choose_sequence, choose_review_sequence, journal, normalize
from progress import COURSES, capture as capture_progress

EXTRACT = (Path(__file__).parent / 'dom.js').read_text()
LEARN = 'https://mathacademy.com/learn'


def by_id(scope, identifier):
    if not identifier:
        raise ValueError('Missing observed DOM identifier')
    return scope.locator('[id=' + json.dumps(identifier) + ']')


def kp_for_example(topic, mid, name):
    points = topic[':topic/knowledge-points']
    exact = [k for k in points if k.get(':knowledge-point/canonical-example',{}).get(':question/math-academy-id') == mid]
    title = re.sub(r'^Example:\s*', '', name or '')
    matches = exact or [k for k in points if k[':knowledge-point/title'] == title]
    if len(matches) != 1:
        raise ValueError('Cannot unambiguously map live example to a database KP: ' + mid)
    return matches[0]


class CaptureBrowser:
    def __init__(self, page, args, pacer, solver):
        self.page, self.args, self.pacer, self.solver = page, args, pacer, solver
        self.page.set_default_timeout(args.timeout_ms)
        self.http_block = None
        self.progress_reader = None
        self.image_responses = {}
        self.page.on('response', self._observe_response)

    def _observe_response(self, response):
        host = urlparse(response.url).hostname or ''
        if (host == 'mathacademy.com' or host.endswith('.mathacademy.com')) and response.status in (401,403,429):
            self.http_block = response.status
        if response.ok and response.request.resource_type == 'image':
            self.image_responses[response.url] = response

    def check(self):
        if self.http_block:
            raise RuntimeError('Math Academy returned HTTP ' + str(self.http_block) + '; stop and review before another run')
        if re.search(r'/(login|signin|session-expired)(?:/|\?|$)', self.page.url):
            raise RuntimeError('Authentication required; use the login command')
        if self.page.locator('input[type="password"]').count():
            raise RuntimeError('Login form detected; use the login command')
        if self.page.locator('iframe[src*="captcha"], #challenge-form, .cf-challenge').count():
            raise RuntimeError('Challenge detected; stop for human review')

    def navigate(self, url, force=False):
        # Only idempotent page navigation is retried. Answer/Continue clicks never are.
        from playwright.sync_api import TimeoutError as PlaywrightTimeout
        if self.page.url == url and not force:
            self.check()
            return
        for attempt in range(1,4):
            self.pacer.wait('event', 'page navigation')
            try:
                response = self.page.goto(url, wait_until='domcontentloaded')
            except PlaywrightTimeout:
                self.check()
                if attempt == 3:
                    raise
                self.pacer.backoff(attempt)
                continue
            self.check()
            if response and response.status >= 500:
                if attempt == 3:
                    raise RuntimeError('Repeated server failure: ' + str(response.status))
                self.pacer.backoff(attempt)
                continue
            self.page.locator('body').wait_for(state='visible')
            return

    def queue(self):
        self.navigate(LEARN)
        self.page.locator('#incompleteTasks').wait_for(state='attached')
        # Wait for the asynchronous task list, allowing an empty queue.
        self.page.wait_for_timeout(self.args.settle_ms)
        self.check()
        return self.page.locator('.taskUnlocked').evaluate_all('''nodes => nodes.filter(e => e.getClientRects().length && e.getAttribute('progress') === '0').flatMap(e => {
          const a=e.querySelector('a.taskStartButton'), href=a?.getAttribute('href') || '';
          const m=href.match(/^\\/tasks\\/(\\d+)\\/topics\\/(\\d+)\\/(lesson|review)$/);
          if (!m || e.querySelector('.taskTypeUnlocked')?.textContent.trim().toLowerCase() !== m[3]) return [];
          return [{task_id:Number(m[1]),topic_id:Number(m[2]),card_id:e.id,start_id:a.id,
            task_type:m[3],href,title:e.querySelector('[id^="taskName-"]')?.textContent.trim()}];
        })''')

    def start(self, activity):
        kind = activity.get('task_type', 'lesson')
        self.pacer.wait('event', 'expand the selected ' + kind)
        by_id(self.page, activity['card_id']).click()
        button = by_id(self.page, activity['start_id'])
        button.wait_for(state='visible')
        if button.get_attribute('href') != activity['href']:
            raise ValueError('Queue activity changed before starting')
        self.pacer.wait('event', 'start the selected ' + kind)
        button.click()
        self.page.wait_for_url('**/tasks/' + str(activity['task_id']) + '/topics/' + str(activity['topic_id']) + '/' + kind)
        self.check()

    def read(self, scope, directory, stem):
        directory = Path(directory)
        directory.mkdir(parents=True, exist_ok=True)
        item = scope.evaluate(EXTRACT)
        # Reuse original image responses already loaded by the browser. Canvas and
        # inline SVG retain a rendered capture. No separate HTTP requests are made.
        candidates = scope.locator('img, canvas, svg').all()
        index = 0
        for asset in candidates:
            included = asset.evaluate('''n => !n.closest('.mjpage, mjx-container, .MathJax, .questionWidget-header, .questionWidget-result, .stepHeader') && !n.parentElement?.closest('svg')''')
            if not included:
                continue
            if not asset.is_visible():
                item['errors'].append('Visual asset is not rendered')
                index += 1
                continue
            if asset.evaluate("n => n.localName === 'img'"):
                self.page.wait_for_function('n => n.complete && n.naturalWidth > 0', arg=asset.element_handle())
            metadata = item['assets'][index]
            source_url = metadata.get('source_url')
            response = self.image_responses.get(source_url)
            extension, representation = '.png', 'rendered'
            if metadata['tag'] == 'img' and response is not None:
                pixels = response.body()
                mime = response.headers.get('content-type', '').split(';')[0].strip().lower()
                extension = {'image/png':'.png', 'image/jpeg':'.jpg', 'image/webp':'.webp',
                             'image/gif':'.gif', 'image/svg+xml':'.svg'}.get(mime)
                if not pixels or not extension:
                    raise ValueError('Unsupported original image response: ' + str(source_url))
                representation = 'original'
            else:
                pixels = asset.screenshot()
                mime = 'image/png'
            target = (directory / 'assets' / (hashlib.sha256(pixels).hexdigest() + extension)).resolve()
            target.parent.mkdir(parents=True,exist_ok=True)
            target.write_bytes(pixels)
            metadata.update(path=str(target), content_type=mime, representation=representation,
                            sha256=hashlib.sha256(pixels).hexdigest())
            manifest_path = directory / 'assets/manifest.json'
            manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
            manifest[source_url or stem + '/' + str(index)] = metadata
            atomic_json(manifest_path, manifest)
            marker = '@asset-' + str(index) + '@'
            item['problem'] = item['problem'].replace(marker,str(target))
            item['worked_solution'] = item['worked_solution'].replace(marker,str(target))
            for field in item['fields']:
                for choice in field['choices']:
                    choice['value'] = choice['value'].replace(marker,str(target))
            index += 1
        atomic_json(directory / (stem + '.json'), item)
        screenshot = directory / (stem + '.png')
        scope.screenshot(path=str(screenshot))
        if item['errors']:
            raise ValueError('DOM extraction needs review: ' + '; '.join(item['errors']))
        return item, screenshot

    def _continue(self, identifier):
        current = self.page.locator('.stepButton.current').get_attribute('id')
        button = by_id(self.page, identifier)
        button.wait_for(state='visible')
        self.pacer.wait('event', 'advance to the next item')
        self.check()
        button.click()
        self.page.wait_for_function('''old => document.querySelector('.stepButton.current')?.id !== old ||
          !!document.querySelector('#finalScreen')?.getClientRects().length''', arg=current)

    def knowledge_snapshot(self, state, directory, event, recovered=False):
        directory = Path(directory)
        courses = tuple(getattr(self.args, 'progress_course_ids', COURSES))
        snapshots = state.setdefault('knowledge_snapshots', {})
        target = directory / 'knowledge-state' / (event + '.json')
        if target.exists():
            snapshot = json.loads(target.read_text())
            if snapshot['task_id'] != state['task_id'] or tuple(c['course_id'] for c in snapshot['courses']) != courses:
                raise ValueError('Saved knowledge snapshot has a different task or course scope')
        else:
            previous = None
            if snapshots:
                previous = json.loads((directory / list(snapshots.values())[-1]['path']).read_text())
            if self.progress_reader is None:
                # Keep the live lesson loaded and its widgets untouched in the original tab.
                page = self.page.context.new_page()
                self.progress_reader = CaptureBrowser(page, self.args, self.pacer, None)
            snapshot = capture_progress(self.progress_reader, target.parent, event, state['task_id'],
                                        courses, previous, recovered)
        snapshots[event] = {'path': str(target.relative_to(directory)),
                            'finished_at': snapshot['finished_at'], 'changes': len(snapshot['changes'])}
        atomic_json(directory / 'state.json', state)
        logging.info('Knowledge snapshot %s: %d course rows, %d changes', event,
                     sum(len(c['topics']) for c in snapshot['courses']), len(snapshot['changes']))

    def advance(self, state, directory, token):
        event = 'after-' + token
        state['pending_knowledge_snapshot'] = {'event': event, 'source_step': 'stepButton-' + token}
        atomic_json(Path(directory) / 'state.json', state)
        self._continue('continueButton-' + token)
        self.knowledge_snapshot(state, directory, event)
        state.pop('pending_knowledge_snapshot', None)
        atomic_json(Path(directory) / 'state.json', state)

    def lesson(self, state, directory, topic):
        state.setdefault('task_type', 'lesson')
        return self.activity(state, directory, topic)

    def review(self, state, directory, topic):
        state['task_type'] = 'review'
        return self.activity(state, directory, topic)

    def wait_activity_ready(self):
        # Initial page markup uses numbered placeholders before real step IDs arrive.
        self.page.wait_for_function(r'''() => /^stepButton-[teq]\d+$/.test(document.querySelector('.stepButton.current')?.id || '') ||
          !!document.querySelector('#finalScreen')?.getClientRects().length''')

    def activity(self, state, directory, topic):
        directory = Path(directory)
        kind_name = state.get('task_type', 'lesson')
        is_review = kind_name == 'review'
        completed_event = kind_name + '-completed'
        save = lambda: atomic_json(directory / 'state.json', state)
        if state.get('activity_complete') or state.get(kind_name + '_complete'):
            if completed_event not in state.get('knowledge_snapshots', {}):
                self.navigate(LEARN)
                self.knowledge_snapshot(state, directory, completed_event, recovered=True)
            return
        self.knowledge_snapshot(state, directory, 'baseline')
        if is_review and 'review_sequence' not in state:
            state['review_policy'] = getattr(self.args, 'review_policy', 'maximize')
            state['review_sequence'] = choose_review_sequence(self.pacer.rng, self.args.cwcwc_weight,
                                                              state['review_policy'])
            save()
        pending = state.get('pending_knowledge_snapshot')
        if pending:
            self.wait_activity_ready()
            current = self.page.locator('.stepButton.current').get_attribute('id') if self.page.locator('.stepButton.current').count() else None
            if current != pending['source_step'] or self.page.locator('#finalScreen').is_visible():
                self.knowledge_snapshot(state, directory, pending['event'], recovered=True)
                state.pop('pending_knowledge_snapshot', None)
                save()
        while True:
            self.check()
            self.wait_activity_ready()
            if self.page.locator('#finalScreen').is_visible():
                completion = self.page.locator('#finalScreen').inner_text()
                if 'completed the ' + kind_name not in completion.lower():
                    raise ValueError(kind_name.title() + ' ended without completion: ' + completion)
                if not state['questions'] or not all(q.get('finalized') for q in state['questions'].values()):
                    raise ValueError('Completion screen has incomplete captured content')
                if not is_review:
                    if not state['kps']:
                        raise ValueError('Lesson completed without captured knowledge points')
                    for kp in state['kps'].values():
                        count = sum(q['kp_id'] == kp['id'] and q.get('finalized') for q in state['questions'].values())
                        if count != 5:
                            raise ValueError('Knowledge point did not serve five questions: ' + kp['title'])
                self.page.screenshot(path=str(directory / (completed_event + '.png')))
                state['completion'], state['activity_complete'], state[kind_name + '_complete'] = completion, True, True
                save()
                self.pacer.wait('event', 'finish ' + kind_name)
                by_id(self.page,'finalScreen-doneButton').click()
                self.page.wait_for_url('**/learn')
                self.knowledge_snapshot(state, directory, completed_event)
                return
            current = self.page.locator('.stepButton.current').get_attribute('id')
            match = re.fullmatch(r'stepButton-([teq])(\d+)', current or '')
            if not match:
                raise ValueError('Unknown current step identifier: ' + str(current))
            kind, number = match.groups()
            if is_review and kind != 'q':
                raise ValueError('Unexpected review tutorial/example layout; save for inspection before advancing')
            token = kind + number
            scope = by_id(self.page, 'step-' + token)
            scope.wait_for(state='visible')
            if kind in ('e','q'):
                self.page.wait_for_function('''({id,kind}) => {
                  const e=document.getElementById(id); if(!e) return false;
                  const prompt=e.querySelector(kind==='e'?'.exampleQuestion':'.questionWidget-text');
                  if(!prompt?.textContent.trim() && !prompt?.querySelector('img,canvas,svg')) return false;
                  if(kind==='e' && !e.querySelector('.exampleExplanation')?.textContent.trim()) return false;
                  if(kind==='q' && !e.querySelector('.questionWidget-choicesTable tr,.matheditor-wrapper-answer,.selectList,input,textarea,select,[contenteditable="true"]')) return false;
                  return [...e.querySelectorAll('mjx-container')].every(n=>!!n.querySelector('mjx-assistive-mml math'));
                }''',arg={'id':'step-'+token,'kind':kind})
            if kind == 't':
                (directory / ('tutorial-' + number + '.html')).write_text(scope.evaluate('e => e.outerHTML'))
                self.advance(state, directory, token)
                continue
            if kind == 'e':
                item, screenshot = self.read(scope,directory,'example-' + number)
                mid = 'e-' + number
                kp = kp_for_example(topic, mid, item['name'])
                kp_id = str(kp[':knowledge-point/id'])
                if not item['problem'] or not item['worked_solution']:
                    raise ValueError('Canonical example is incomplete: ' + mid)
                if item['fields']:
                    raise ValueError('Example exposes interactive fields; review this new example layout')
                state['current_kp'] = kp_id
                state['kps'].setdefault(kp_id,{'id':kp_id,'title':kp[':knowledge-point/title'],
                                             'sequence':choose_sequence(self.pacer.rng,self.args.cwcwc_weight)})
                state['examples'][mid] = {'math_academy_id':mid,'is_example':True,'knowledge_point_id':kp_id,
                    'knowledge_point':kp[':knowledge-point/title'],'problem':item['problem'],'worked_solution':item['worked_solution'],
                    'difficulty':None,'answer_fields':[], 'missing_source_fields':['difficulty','answer_fields']}
                save()
                logging.info('Captured %s; KP sequence %s',mid,state['kps'][kp_id]['sequence'])
                self.advance(state, directory, token)
                continue
            kp_id = None if is_review else state.get('current_kp')
            if not is_review and kp_id not in state['kps']:
                raise ValueError('Question has no captured canonical example/KP')
            mid = 'q-' + number
            record = state['questions'].get(mid)
            if record and record.get('finalized'):
                self.advance(state, directory, token)
                continue
            if not record:
                item, screenshot = self.read(scope,directory,mid + '-before')
                if not item['problem'] or not item['fields']:
                    raise ValueError('Question content or answer fields are not loaded: ' + mid)
                count = len(state['questions']) if is_review else sum(q['kp_id'] == kp_id for q in state['questions'].values())
                if is_review:
                    if count >= getattr(self.args, 'review_question_limit', 20):
                        raise ValueError('Review question limit reached; capture saved before another submission')
                    sequence = state['review_sequence']
                    intended = sequence[min(count, len(sequence)-1)]
                else:
                    if count >= 5:
                        raise ValueError('KP unexpectedly served a sixth question')
                    intended = state['kps'][kp_id]['sequence'][count]
                solve_started = time.monotonic()
                decision = self.solver.solve(item,screenshot,directory / mid)
                solver_elapsed = time.monotonic() - solve_started
                record = {'kp_id':kp_id,'before':item,'decision':decision,
                          'intended':intended,'status':'prepared','solver_elapsed_seconds':solver_elapsed}
                state['questions'][mid] = record
                save()
            button = by_id(self.page,'continueButton-' + token)
            if record['status'] == 'prepared':
                self.enter(scope,record)
                self.pacer.wait('answer','before submitting an answer',elapsed=record.get('solver_elapsed_seconds',0))
                self.check()
                self.verify_entered(scope, record)
                self.page.screenshot(path=str(directory / (mid + '-entered.png')))
                record['status'] = 'submitting'
                save()
                journal(directory / 'events.jsonl','answer_submission_intent',question=mid,intended=record['intended'])
                submit = scope.locator('.questionWidget-submitButton')
                if 'disabledButton' in (submit.get_attribute('class') or ''):
                    raise ValueError('Submit is still disabled after filling observed fields')
                submit.click()
            # After a crash/timeout, only inspect/wait. Never blindly resubmit.
            button.wait_for(state='visible')
            item, screenshot = self.read(scope,directory,mid + '-after')
            actual = (item.get('result') or '').strip()
            expected = 'Correct' if record['intended'] == 'C' else 'Incorrect'
            record['after'], record['actual_result'] = item, actual
            record['status'] = 'graded'
            save()
            if actual != expected:
                self.knowledge_snapshot(state, directory, 'unexpected-grade-' + token)
                raise ValueError(mid + ' expected ' + expected + ', received ' + actual + '; stop before another answer')
            if not item['worked_solution']:
                raise ValueError('Revealed worked solution is missing: ' + mid)
            decision = record['decision']
            if actual == 'Incorrect':
                verified = self.solver.solve(item,screenshot,directory / mid,'verify')
                original = {a['key']:a for a in decision['answers']}
                for answer in verified['answers']:
                    first = original[answer['key']]
                    if normalize(first['correct_value'],first['value_type']) != normalize(answer['correct_value'],answer['value_type']):
                        raise ValueError('Worked solution contradicts predicted correct answer: ' + mid)
                record['verification'] = verified
            # Reviews do not show canonical examples to establish the KP live.
            # The activity's per-question KP link supplies the mapping later.
            record['content'] = self.question_content(mid,record,{'id':None,'title':None} if is_review else state['kps'][kp_id])
            record['finalized'] = True
            save()
            logging.info('%s: %s, captured %d fields',mid,actual,len(record['content']['answer_fields']))
            self.advance(state, directory, token)

    def enter(self, scope, record):
        answers = {a['key']:a for a in record['decision']['answers']}
        wrong_used = False
        for field in record['before']['fields']:
            answer = answers[field['key']]
            wrong = record['intended'] == 'W' and not wrong_used
            self.pacer.wait('event','fill answer field ' + field['key'])
            if field['type'] in ('radio','select'):
                choices = [c for c in field['choices'] if c['option'] != answer['correct_option']] if wrong else [c for c in field['choices'] if c['option'] == answer['correct_option']]
                if not choices:
                    raise ValueError('Cannot choose a distinct incorrect option')
                chosen = self.pacer.rng.choice(choices)
                if field['type'] == 'radio':
                    by_id(scope,chosen['dom_id']).click()
                elif field['tag'] == 'select':
                    by_id(scope,field['dom_id']).select_option(chosen['option'])
                else:
                    by_id(scope,field['frame_id']).click()
                    by_id(scope,field['dom_id']).locator('.selectListOptions > .selectListOption').nth(int(chosen['option'])).click()
                field['submitted_value'] = chosen['value']
                field['submitted_option'] = chosen['option']
            else:
                value = answer['wrong_value'] if wrong else answer['correct_value']
                control = by_id(scope,field['dom_id'])
                if field['tag'] == 'mathquill':
                    control.locator('.mq-editable-field').click()
                    editor = control.locator('.mq-textarea textarea')
                    editor.press('ControlOrMeta+A')
                    editor.press('Backspace')
                    for action in answer['wrong_keys' if wrong else 'correct_keys']:
                        if action['text'] is not None:
                            editor.press_sequentially(action['text'],delay=self.pacer.rng.uniform(60,140))
                        else:
                            editor.press(action['key'])
                else:
                    control.fill(value)
                field['submitted_value'] = value
            wrong_used |= wrong

    def verify_entered(self, scope, record):
        for field in record['before']['fields']:
            if field['type'] == 'radio':
                selected = scope.locator('.questionWidget-choiceLetterCircle').evaluate_all('''nodes => nodes.filter(n =>
                  n.style.backgroundColor === 'rgb(64, 64, 64)' && n.style.color === 'white').map(n => n.textContent.trim())''')
                if selected != [field['submitted_option']]:
                    raise ValueError('Actual selected radio option differs from intended option; stop before Submit')
                field['observed_selected_option'] = selected[0]
            elif field['type'] == 'select' and field['tag'] == 'select':
                if by_id(scope,field['dom_id']).input_value() != field['submitted_option']:
                    raise ValueError('Actual selected option differs from intended option; stop before Submit')
            elif field['type'] == 'blank' and field['tag'] != 'mathquill':
                if by_id(scope,field['dom_id']).input_value() != field['submitted_value']:
                    raise ValueError('Actual blank value differs from intended value; stop before Submit')

    @staticmethod
    def question_content(mid, record, kp):
        answers = {a['key']:a for a in record['decision']['answers']}
        fields = []
        for f in record['before']['fields']:
            answer = answers[f['key']]
            choices = [{'type':c['type'],'value':c['value']} for c in f['choices']]
            if f['type'] == 'blank':
                choices = [{'type':answer['value_type'],'value':answer['correct_value']}]
                submitted = f.get('submitted_value')
                if submitted is not None and submitted != answer['correct_value']:
                    choices.append({'type':answer['value_type'],'value':submitted})
            fields.append({'key':f['key'],'type':f['type'],'choices':choices,'correct_value':answer['correct_value']})
        instructions = record['before'].get('calculator_instructions','')
        result = {'math_academy_id':mid,'is_example':False,'knowledge_point_id':kp['id'],
                  'knowledge_point':kp['title'],'problem':record['before']['problem'],
                  'worked_solution':record['after']['worked_solution'],'answer_fields':fields}
        if instructions and not re.search(r'not|without|forbidden',instructions,re.I):
            result['requires_calculator'] = True
        return result

    def history(self, state, directory, topic=None):
        directory = Path(directory)
        task_type = state.get('task_type', 'lesson')
        self.navigate(LEARN + '?taskId=' + str(state['task_id']))
        selector = '.reviewAnswerList .question' if task_type == 'review' else '.kp .question'
        self.page.locator(selector).first.wait_for(state='visible')
        metadata = self.page.locator(selector).evaluate_all('''nodes => nodes.map(q => ({
          id:q.id, difficulty:q.querySelector('.questionDifficulty')?.textContent.trim(),
          kp_title:q.querySelector('.questionKP')?.textContent.trim() || q.closest('.kp')?.querySelector('.kpTitle')?.textContent.trim(),
          kp_href:q.querySelector('.questionKP')?.getAttribute('href'),
          result:q.querySelector('.answerResult')?.textContent.trim(), raw_html:q.outerHTML}))''')
        ids = {q['id'].replace('question-','q-') for q in metadata}
        if len(ids) != len(metadata):
            raise ValueError('Duplicate question IDs in activity')
        if ids != set(state['questions']):
            raise ValueError('Activity IDs do not match the live capture')
        for q in metadata:
            title = re.sub(r'^KP \d+\.\s*','',q['kp_title'] or '').strip()
            mid = q['id'].replace('question-','q-')
            record = state['questions'][mid]
            if task_type == 'review':
                source = re.fullmatch(r'/topics/(\d+)#(\d+)', q['kp_href'] or '')
                if not source or int(source[1]) != state['topic_id'] or topic is None:
                    raise ValueError('Review activity has no valid topic/KP source link: ' + mid)
                matches = [kp for kp in topic[':topic/knowledge-points'] if kp[':knowledge-point/title'] == title]
                if len(matches) != 1:
                    raise ValueError('Review KP title cannot be matched uniquely within the topic: ' + mid)
                kp_id = str(matches[0][':knowledge-point/id'])
                record['kp_id'] = kp_id
                record['content'].update(knowledge_point_id=kp_id, knowledge_point=title)
                state['kps'].setdefault(kp_id, {'id':kp_id, 'title':title})
                record['content']['knowledge_point_source_id'] = int(source[2])
            elif record['content']['knowledge_point'] != title:
                raise ValueError('Activity KP title contradicts live example mapping: ' + mid)
            if q['result'] and q['result'] != record['actual_result']:
                raise ValueError('Activity grade contradicts captured live result: ' + mid)
            difficulty = {'E':'easy','M':'moderate','H':'hard'}.get(q['difficulty'])
            if not difficulty:
                raise ValueError('Activity question lacks a recognized difficulty: ' + mid)
            record['content']['difficulty'] = difficulty
            explanation = by_id(self.page,q['id'].replace('question-','questionExplanation-'))
            if not explanation.is_visible():
                self.pacer.wait('event','expand activity explanation')
                by_id(self.page,q['id']).locator('.answerDetails').click()
            explanation.wait_for(state='visible')
            item, _ = self.read(explanation,directory,'history-' + mid)
            if not item['worked_solution']:
                raise ValueError('Activity explanation is missing: ' + mid)
            record['history'] = item
            record['content']['worked_solution'] = item['worked_solution']
            record['content']['provenance'] = {'activity_question':q['id'], 'kp_title':title, 'kp_href':q['kp_href']}
        atomic_json(directory / 'activity-metadata.json',metadata)
        state['history_complete'] = True
        atomic_json(directory / 'state.json',state)
        content = {'task_id':state['task_id'],'task_type':task_type,'topic_id':state['topic_id'],'content_only':True,
                   'source_url':self.page.url,'sequence_policy':{'CWCWC':self.args.cwcwc_weight,'WCWCC':1-self.args.cwcwc_weight},
                   'questions':[q['content'] for q in state['questions'].values()],
                   'canonical_examples':list(state['examples'].values())}
        if task_type == 'review':
            content['sequence_policy'] = {'scope':'whole review', 'policy':state.get('review_policy','maximize'),
                                          'sequence':state['review_sequence']}
        atomic_json(directory / 'content.json',content)
        return content
