"""Sequential Playwright UI capture with checkpoints before every submission."""
import json
import hashlib
import logging
import re
import time
from collections import deque
from pathlib import Path
from urllib.parse import urlparse

from core import atomic_json, assessment_can_start, assessment_requirement, choose_sequence, choose_review_sequence, journal, normalize, stable_id
from progress import COURSES, capture as capture_progress

EXTRACT = (Path(__file__).parent / 'dom.js').read_text()
LEARN = 'https://mathacademy.com/learn'
ACTIVE_STEP = r'''() => {
  const visible=n=>!!n?.getClientRects().length && getComputedStyle(n).visibility!=='hidden';
  const unanswered=[...document.querySelectorAll('.step.questionWidget')].filter(n=>visible(n) &&
    !n.querySelector('.questionWidget-result')?.textContent.trim() && visible(n.querySelector('.questionWidget-submitButton')));
  if(unanswered.length===1) return 'stepButton-'+unanswered[0].id.slice(5);
  if(unanswered.length>1) return null;
  const buttons=[...document.querySelectorAll('[id^="continueButton-"]')].filter(visible);
  if(buttons.length===1) return buttons[0].id.replace('continueButton-','stepButton-');
  if(buttons.length>1) return null;
  const current=document.querySelector('.stepButton.current')?.id || '';
  return /^stepButton-[te]\d+$/.test(current) ? current : null;
}'''

EXTRACT_QUEUE = r'''nodes => nodes.filter(e => e.getClientRects().length).map(e => {
  const a=e.querySelector('a.taskStartButton'), href=a?.getAttribute('href') || '';
  const lesson=href.match(/^\/tasks\/(\d+)\/topics\/(\d+)\/(lesson|review)$/);
  const task=e.id.match(/^task-(\d+)$/), test=href.match(/^\/tasks\/(\d+)\/tests\/(\d+)\/start$/);
  const multistep=href.match(/^\/tasks\/(\d+)\/multisteps\/(\d+)$/);
  const kind=e.querySelector('.taskTypeUnlocked')?.textContent.trim().toLowerCase() || 'unknown';
  const progress=Number(e.getAttribute('progress'));
  const supported=(!!lesson && kind === lesson[3]) || (!!test && kind === 'assessment') || (!!multistep && kind === 'multistep');
  const details={};
  for (const row of e.querySelectorAll('.testDetails tr')) {
    const name=row.querySelector('.testFieldName')?.textContent.trim().replace(/:$/,'');
    if (name) details[name]=row.querySelector('.testFieldValue')?.textContent.trim();
  }
  return {task_id:task ? Number(task[1]) : null,topic_id:lesson ? Number(lesson[2]) : null,
    card_id:e.id,start_id:a?.id || null,task_type:kind,href,
    title:e.querySelector('[id^="taskName-"], .taskNameUnlocked')?.textContent.trim() || '',
    capture_supported:supported,progress:Number.isFinite(progress) ? progress : null,
    in_progress:Number.isFinite(progress) && progress>0,
    ...(kind === 'multistep' ? {multistep_id:multistep ? Number(multistep[2]) : null,
      multistep_card_html:e.outerHTML} : {}),
    ...(kind === 'assessment' ? {test_id:test ? Number(test[2]) : null,assessment_details:details,
      assessment_card_html:e.outerHTML} : {})};
})'''

MATHQUILL_VALUE = r'''n => {
  const node = n.querySelector('.mq-editable-field');
  const library = window.MathQuill;
  if (!node || !library) return null;
  const MQ = library.getInterface ? library.getInterface(2) : library;
  const field = MQ(node); // Retrieve an existing editor; never construct or change one.
  return field && typeof field.latex === 'function' ? field.latex() : null;
}'''


def mathquill_keys(value, actions):
    """Make named symbols explicit when older solver turns assumed autoCommands."""
    names = set(re.findall(r'\\(pi|theta|alpha|beta|gamma|delta|lambda|mu|rho|sigma|phi|omega)\b', value))
    result = []
    for action in actions:
        action = dict(action)
        if action.get('text') is not None:
            for name in sorted(names, key=len, reverse=True):
                action['text'] = re.sub(r'(?<![A-Za-z\\])' + name + r'(?![A-Za-z])',
                                        lambda _: '\\' + name + ' ', action['text'])
        result.append(action)
    return result


def normalize_mathquill(value):
    """Compare editor notation without treating differently grouped math as equal."""
    return normalize(value)


def by_id(scope, identifier):
    if not identifier:
        raise ValueError('Missing observed DOM identifier')
    return scope.locator('[id=' + json.dumps(identifier) + ']')


def deduplicate_math_editor(html):
    """Keep the first identical editor script tag; preserve all other page HTML."""
    seen = set()
    def keep_first(match):
        source = match['source']
        if source in seen:
            return ''
        seen.add(source)
        return match[0]
    return re.sub(r'''<script\b(?=[^>]*\bsrc=["'](?P<source>/js/math-editor\.js(?:\?[^"']*)?)["'])[^>]*>\s*</script\s*>''',
                  keep_first,html,flags=re.I)


def repair_math_editor_document(route):
    # Browsers can fetch one script once but execute it for both tags, so
    # deduplicate the HTML rather than counting network requests.
    if route.request.resource_type != 'document' or route.request.method != 'GET':
        return route.continue_()
    # Let the browser follow redirects so page scripts see the destination URL.
    # Fetching the final document and fulfilling /learn leaves its URL unchanged.
    response = route.fetch(max_redirects=0)
    if response.status in (301,302,303,307,308):
        return route.fulfill(response=response)
    if 'text/html' not in response.headers.get('content-type','').lower():
        return route.fulfill(response=response)
    original = response.text()
    cleaned = deduplicate_math_editor(original)
    if cleaned != original:
        logging.info('Removed duplicate math-editor.js tag from %s',route.request.url)
    route.fulfill(response=response,body=cleaned)


def answer_control(scope, field):
    if field.get('dom_id'):
        return by_id(scope,field['dom_id'])
    if field.get('tag') == 'mathquill' and isinstance(field.get('dom_index'),int) and field['dom_index'] >= 0:
        return scope.locator('.matheditor-wrapper-answer').nth(field['dom_index'])
    raise ValueError('Answer control has no observed locator')


class AccessBlocked(RuntimeError):
    """An authentication/access failure that affects the entire browser session."""


def kp_title_identity(title):
    # Legacy imported titles use this older spelling; live MA uses Leibniz.
    return re.sub(r'\bLeibnitz\b', 'Leibniz', title)


def kp_for_example(topic, mid, name, allow_new=False):
    points = topic[':topic/knowledge-points']
    exact = [k for k in points if k.get(':knowledge-point/canonical-example',{}).get(':question/math-academy-id') == mid]
    title = re.sub(r'^Example:\s*', '', name or '')
    matches = exact or [k for k in points if kp_title_identity(k[':knowledge-point/title']) == kp_title_identity(title)]
    if len(exact) > 1:
        # Canonical refs permit reuse. The observed title must disambiguate
        # multiple KPs referencing the same content; never pick by list order.
        matches = [k for k in exact if kp_title_identity(k[':knowledge-point/title']) == kp_title_identity(title)]
    if not matches and not exact and allow_new and title and (name or '').startswith('Example:') and re.fullmatch(r'e-\d+',mid):
        return {':knowledge-point/id':stable_id('knowledge-point',str(topic[':topic/math-academy-id'])+':'+mid),
                ':knowledge-point/title':title,'captured_new':True}
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
        self.diagnostic_events = deque(maxlen=200)
        self.page.on('response', self._observe_response)
        self.page.on('pageerror', lambda error:self._diagnostic_event('pageerror',message=str(error)))
        self.page.on('console', self._observe_console)
        self.page.on('requestfailed', lambda request:self._diagnostic_event(
            'requestfailed',url=request.url,method=request.method,error=request.failure))

    def _diagnostic_event(self, event, **details):
        self.diagnostic_events.append({'time':time.time(),'event':event,**details})

    def _observe_console(self, message):
        if message.type in ('error','warning'):
            self._diagnostic_event('console',level=message.type,message=message.text,
                                   location=message.location)

    def _observe_response(self, response):
        host = urlparse(response.url).hostname or ''
        if response.status >= 400:
            self._diagnostic_event('http_error',url=response.url,status=response.status)
        if (host == 'mathacademy.com' or host.endswith('.mathacademy.com')) and response.status in (401,403,429):
            self.http_block = response.status
        if response.ok and response.request.resource_type == 'image':
            self.image_responses[response.url] = response

    def check(self):
        stop = getattr(self.args, 'stop_event', None)
        if stop is not None and stop.is_set():
            raise KeyboardInterrupt('Stopped; saved checkpoints are retained')
        if self.http_block:
            raise AccessBlocked('Math Academy returned HTTP ' + str(self.http_block) + '; stop and review before another run')
        if re.search(r'/(login|signin|session-expired)(?:/|\?|$)', self.page.url):
            raise AccessBlocked('Authentication required; use the login command')
        if self.page.locator('input[type="password"]').count():
            raise AccessBlocked('Login form detected; use the login command')
        if self.page.locator('iframe[src*="captcha"], #challenge-form, .cf-challenge').count():
            raise AccessBlocked('Challenge detected; stop for human review')

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
                if response and response.request.redirected_from:
                    if url == LEARN and re.search(r'/tasks/\d+/tests/\d+(?:[/?#]|$)',self.page.url):
                        self.check()
                        return  # The queue caller reports the forced active assessment.
                    # Playwright routes only the first request of a redirect
                    # chain. Load the destination once directly so its document
                    # receives the same editor-tag repair as other navigations.
                    self.pacer.wait('event','initialize redirected page')
                    response = self.page.goto(self.page.url, wait_until='domcontentloaded')
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
            # Positioned assessment content can leave the body with zero height.
            # Require a visible body or child; hidden pages still fail.
            self.page.locator('body:visible, body > :visible').first.wait_for(state='visible')
            return

    def queue(self):
        self.navigate(LEARN, force=True)
        if re.search(r'/tasks/\d+/tests/\d+(?:[/?#]|$)',self.page.url):
            raise ValueError('Math Academy redirected the queue to an unfinished assessment: '+self.page.url+'; explicitly resume its saved capture')
        self.page.locator('#incompleteTasks').wait_for(state='attached')
        # Wait for the asynchronous task list, allowing an empty queue.
        self.page.wait_for_timeout(self.args.settle_ms)
        self.check()
        self.completed_outcomes = self.page.locator('#completedTasks .taskCompleted').evaluate_all(r'''nodes => nodes.flatMap(e => {
          const kind=e.querySelector('.taskTypeLocked')?.textContent.trim().toLowerCase();
          const xp=e.querySelector('.taskPoints')?.textContent.trim().match(/^(-?\d+)\s*\//);
          const topic=e.querySelector('a[id^="taskTopicLink-"]')?.getAttribute('href')?.match(/^\/topics\/(\d+)/);
          const task=e.id.match(/^task-(\d+)$/);
          return xp && topic && task && ['lesson','review'].includes(kind) ?
            [{task_id:Number(task[1]),topic_id:Number(topic[1]),task_type:kind,earned_xp:Number(xp[1])}] : [];
        })''')
        cards = self.page.locator('#incompleteTasks .taskUnlocked')
        initial = cards.evaluate_all(EXTRACT_QUEUE)
        for item in initial:
            if item['task_type'] == 'multistep' and not item['in_progress'] and not item['href']:
                self.pacer.wait('event','expand multistep queue details')
                card = by_id(self.page,item['card_id'])
                card.click()
                card.locator('a.taskStartButton').wait_for(state='visible')
                continue
            if item['task_type'] != 'assessment' or item['in_progress']:
                continue
            card = by_id(self.page,item['card_id'])
            if not card.locator('.testDetails').is_visible():
                self.pacer.wait('event','expand assessment eligibility details')
                card.click()
                card.locator('.testDetails').wait_for(state='visible')
                card.locator('a.taskStartButton').wait_for(state='visible')
        self.check()
        queue = cards.evaluate_all(EXTRACT_QUEUE)
        for item in queue:
            if item['task_type'] == 'assessment':
                item.update(assessment_requirement(item['assessment_details'], only_activity=len(queue) == 1,
                                                   title=item['title']))
        return queue

    def start(self, activity):
        kind = activity.get('task_type', 'lesson')
        if kind not in ('lesson','review','assessment','multistep') or not activity.get('capture_supported',True):
            raise ValueError('Activity is recorded but unsupported by the capture player')
        if kind == 'assessment':
            card = by_id(self.page,activity['card_id'])
            queue = self.page.locator('#incompleteTasks .taskUnlocked').evaluate_all(EXTRACT_QUEUE)
            current = next(item for item in queue if item['card_id'] == activity['card_id'])
            current.update(assessment_requirement(current['assessment_details'], only_activity=len(queue) == 1,
                                                  title=current['title']))
            excluded = set(activity.get('assessment_fallback_excluded_tasks',[]))
            alternatives = [item for item in queue
                if item['task_type'] in ('lesson','review','multistep') and
                item.get('capture_supported',True) and not item.get('in_progress') and
                item['task_id'] not in excluded]
            for item in queue:
                if (item['task_type'] == 'assessment' and item['task_id'] != current['task_id'] and
                    item.get('capture_supported') and not item.get('in_progress') and item['task_id'] not in excluded):
                    details = assessment_requirement(item['assessment_details'], only_activity=len(queue) == 1,
                                                     title=item['title'])
                    if assessment_can_start({**item,**details}):
                        alternatives.append(item)
            current['assessment_optional_fallback'] = bool(activity.get('assessment_optional_fallback') and not alternatives)
            if not assessment_can_start(current):
                raise ValueError('Assessment is not required, an eligible retake, or the only eligible activity; stop before Start')
        else:
            card = by_id(self.page, activity['card_id'])
            if kind != 'multistep' or not card.locator('.taskDetails').is_visible():
                self.pacer.wait('event', 'expand the selected ' + kind)
                card.click()
        button = by_id(self.page, activity['start_id'])
        button.wait_for(state='visible')
        if button.get_attribute('href') != activity['href']:
            raise ValueError('Queue activity changed before starting')
        self.pacer.wait('event', 'start the selected ' + kind)
        button.click()
        expected = ('**/tasks/' + str(activity['task_id']) + '/tests/' + str(activity['test_id']) + '/start'
                    if kind == 'assessment' else
                    '**/tasks/' + str(activity['task_id']) + '/multisteps/' + str(activity['multistep_id'])
                    if kind == 'multistep' else
                    '**/tasks/' + str(activity['task_id']) + '/topics/' + str(activity['topic_id']) + '/' + kind)
        self.page.wait_for_url(expected)
        self.check()

    def read(self, scope, directory, stem):
        from playwright.sync_api import TimeoutError as PlaywrightTimeout

        directory = Path(directory)
        directory.mkdir(parents=True, exist_ok=True)
        item = scope.evaluate(EXTRACT)
        # Reuse original image responses already loaded by the browser. Canvas and
        # inline SVG retain a rendered capture. No separate HTTP requests are made.
        candidates = scope.locator('img, canvas, svg').all()
        index = 0
        for asset in candidates:
            included = asset.evaluate('''n => {
              if(n.localName==='svg' && n.closest('.mjpage, mjx-container, .MathJax') &&
                 n.getAttribute('width')==='0' && n.getAttribute('viewBox')?.trim().split(/\\s+/)[2]==='0' &&
                 !n.textContent.trim() && !n.querySelector('path,use,text,line,polyline,polygon,circle,ellipse,rect,image,foreignObject')) return false;
              if(n.closest('.questionWidget-header, .questionWidget-result, .stepHeader, .spinnerFrame, .answer') ||
                 n.parentElement?.closest('svg')) return false;
              const formula=n.closest('.mjpage, mjx-container, .MathJax');
              return !formula || (n.localName==='svg' && !formula.querySelector('mjx-assistive-mml math') &&
                !n.querySelector('title')?.textContent.trim());
            }''')
            if not included:
                continue
            try:
                # Continue can appear before explanation graphics have loaded.
                asset.wait_for(state='visible')
                if asset.evaluate("n => n.localName === 'img'"):
                    self.page.wait_for_function('n => n.complete && n.naturalWidth > 0', arg=asset.element_handle())
            except PlaywrightTimeout:
                item['errors'].append('Visual asset is not rendered')
                index += 1
                continue
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
        current = self.current_step()
        button = by_id(self.page, identifier)
        button.wait_for(state='visible')
        self.pacer.wait('event', 'advance to the next item')
        self.check()
        button.click()
        self.page.wait_for_function('old => ('+ACTIVE_STEP+')() !== old || '
          "!!document.querySelector('#finalScreen')?.getClientRects().length", arg=current)

    def knowledge_snapshot(self, state, directory, event, recovered=False):
        if event != state.get('task_type','lesson') + '-completed':
            raise ValueError('Knowledge snapshots are only captured after completed activities')
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
            previous_path = state.get('previous_activity_snapshot')
            if previous_path:
                previous = json.loads(Path(previous_path).read_text())
            elif 'baseline' in snapshots:
                # Existing runs may already have a baseline; never fetch a new one.
                previous = json.loads((directory / snapshots['baseline']['path']).read_text())
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
        state['pending_continue'] = {'source_step': 'stepButton-' + token}
        atomic_json(Path(directory) / 'state.json', state)
        self._continue('continueButton-' + token)
        state.pop('pending_continue', None)
        atomic_json(Path(directory) / 'state.json', state)

    def lesson(self, state, directory, topic):
        state.setdefault('task_type', 'lesson')
        return self.activity(state, directory, topic)

    def review(self, state, directory, topic):
        state['task_type'] = 'review'
        return self.activity(state, directory, topic)

    def wait_activity_ready(self):
        # Initial page markup uses numbered placeholders before real step IDs arrive.
        self.page.wait_for_function('() => !!('+ACTIVE_STEP+')() || '
            "!!document.querySelector('#finalScreen')?.getClientRects().length")

    def current_step(self):
        return self.page.evaluate(ACTIVE_STEP)

    def restore_unanswered_submission(self, scope, record):
        # Only a fresh, explicit --resume navigation may prove a failed radio
        # submission was not graded. Never replay a submission in its live page.
        if not getattr(self.args, 'resume', None):
            return False
        fields = record['before']['fields']
        if len(fields) != 1 or fields[0]['type'] != 'radio':
            return False
        evidence = scope.evaluate('''n => {
          const visible=e=>!!e?.getClientRects().length && getComputedStyle(e).visibility!=='hidden';
          const submit=n.querySelector('.questionWidget-submitButton');
          const spinner=n.querySelector('.questionWidget-spinner');
          const circles=[...n.querySelectorAll('.questionWidget-choiceLetterCircle, .choiceLetterCircle')];
          return {unanswered:!n.querySelector('.questionWidget-result')?.textContent.trim(),
            submit_visible:visible(submit),submit_disabled:!!submit?.classList.contains('disabledButton'),
            pending:visible(spinner) && (spinner.style.display==='block' ||
              [...spinner.children].some(visible)),
            choices_unselected:circles.length>0 && circles.every(e=>!e.classList.contains('selectedChoice') &&
              !(e.style.backgroundColor==='rgb(64, 64, 64)' && e.style.color==='white'))};
        }''')
        if not (evidence['unanswered'] and evidence['submit_visible'] and evidence['submit_disabled']
                and evidence['choices_unselected'] and not evidence['pending']):
            return False
        fresh = scope.evaluate(EXTRACT)
        for asset in record['before'].get('assets', []):
            fresh['problem'] = fresh['problem'].replace('@asset-' + str(asset['index']) + '@', asset['path'])
        if fresh['errors'] or normalize(fresh['problem']) != normalize(record['before']['problem']):
            return False
        record.setdefault('submission_recoveries', []).append({'reason':'server_restored_unanswered',
                                                              'observed':evidence,'time':time.time()})
        record['status'] = 'prepared'
        return True

    def activity(self, state, directory, topic):
        if state.get('task_type') == 'multistep':
            from multistep import take_multistep
            return take_multistep(self,state,directory)
        if state.get('task_type') == 'assessment':
            from assessment import take_assessment
            return take_assessment(self,state,directory)
        directory = Path(directory)
        kind_name = state.get('task_type', 'lesson')
        is_review = kind_name == 'review'
        perfect = state.get('answer_policy') == 'all_correct'
        completed_event = kind_name + '-completed'
        save = lambda: atomic_json(directory / 'state.json', state)
        if state.get('activity_complete') or state.get(kind_name + '_complete'):
            if completed_event not in state.get('knowledge_snapshots', {}):
                self.navigate(LEARN)
                self.knowledge_snapshot(state, directory, completed_event, recovered=True)
            return
        # Preserve old source files but retire any interrupted per-step scrape.
        legacy_pending = state.pop('pending_knowledge_snapshot', None)
        if legacy_pending:
            state.setdefault('pending_continue', {'source_step':legacy_pending['source_step']})
            save()
        if is_review and 'review_sequence' not in state:
            state['review_sequence'] = 'CCCCC' if perfect else choose_review_sequence(self.pacer.rng, self.args.cwcwc_weight)
            save()
        if is_review and state['review_sequence'] == 'CWCWCC':
            state['legacy_review_sequence'] = state['review_sequence']
            state['review_sequence'] = 'CWCWC'
            save()
        if is_review and state['review_sequence'] not in (('CCCCC',) if perfect else ('CWCWC','WCWCC')):
            raise ValueError('Saved review sequence does not match the configured lesson policy')
        pending = state.get('pending_continue')
        if pending:
            self.wait_activity_ready()
            current = self.current_step()
            if current != pending['source_step'] or self.page.locator('#finalScreen').is_visible():
                state.pop('pending_continue', None)
                save()
        # A saved grade can be finalized even if Continue already advanced the UI.
        if any(q.get('status') == 'submitting' for q in state['questions'].values()):
            self.wait_activity_ready()
        for mid, record in state['questions'].items():
            if record.get('status') == 'submitting' and self.current_step() == 'stepButton-' + mid.replace('-', ''):
                scope = by_id(self.page, 'step-' + mid.replace('-', ''))
                if self.restore_unanswered_submission(scope, record):
                    save()
                    journal(directory / 'events.jsonl', 'submission_recovered_unanswered', question=mid)
            if record.get('status') == 'submitting' and self.current_step() != 'stepButton-' + mid.replace('-', ''):
                # A restored activity may open on the next question. Reconcile the
                # saved result before answering it, rather than orphaning a grade.
                source = directory / (mid + '-after.json')
                item = json.loads(source.read_text()) if source.exists() else {}
                if (item.get('errors') or item.get('result') not in ('Correct', 'Incorrect') or
                    not item.get('worked_solution') or
                    normalize(item.get('problem', '')) != normalize(record['before']['problem']) or
                    any(not a.get('path') or not Path(a['path']).is_file() for a in item.get('assets', []))):
                    raise ValueError('Previous submission needs a complete saved result before advancing: ' + mid)
                record.update(after=item, actual_result=item['result'], status='graded')
                save()
            if record.get('status') == 'graded' and not record.get('finalized'):
                self.finalize_question(state,directory,mid,record)
                save()
        while True:
            self.check()
            self.wait_activity_ready()
            if self.page.locator('#finalScreen').is_visible():
                completion = self.page.locator('#finalScreen').inner_text()
                from retry_policy import earned_xp
                state['earned_xp'] = earned_xp(completion)
                save()  # Even a failed completion must trigger a perfect retake.
                if 'completed the ' + kind_name not in completion.lower():
                    raise ValueError(kind_name.title() + ' ended without completion: ' + completion)
                if not state['questions'] or not all(q.get('finalized') for q in state['questions'].values()):
                    raise ValueError('Completion screen has incomplete captured content')
                if not is_review:
                    if not state['kps']:
                        raise ValueError('Lesson completed without captured knowledge points')
                    for kp in state['kps'].values():
                        count = sum(q['kp_id'] == kp['id'] and q.get('finalized') for q in state['questions'].values())
                        if (not perfect and count != 5) or (perfect and (count < 1 or any(
                            q['actual_result'] != 'Correct' for q in state['questions'].values()))):
                            raise ValueError('Knowledge point did not serve five questions: ' + kp['title'])
                self.page.screenshot(path=str(directory / (completed_event + '.png')))
                state['completion'], state['activity_complete'], state[kind_name + '_complete'] = completion, True, True
                save()
                self.pacer.wait('event', 'finish ' + kind_name)
                by_id(self.page,'finalScreen-doneButton').click()
                self.page.wait_for_url('**/learn', wait_until='domcontentloaded')
                self.knowledge_snapshot(state, directory, completed_event)
                return
            current = self.current_step()
            match = re.fullmatch(r'stepButton-([teq])(\d+)', current or '')
            if not match:
                raise ValueError('Unknown current step identifier: ' + str(current))
            kind, number = match.groups()
            if is_review and kind != 'q':
                raise ValueError('Unexpected review tutorial/example layout; save for inspection before advancing')
            token = kind + number
            scope = by_id(self.page, 'step-' + token)
            scope.wait_for(state='visible')
            if kind == 'q':
                record = state['questions'].get('q-' + number)
                if record and record.get('finalized'):
                    # Graded blanks are rendered as static math on reload;
                    # their editable answer widget has already been removed.
                    result = scope.locator('.questionWidget-result')
                    if not result.count() or result.inner_text().strip() != record['actual_result']:
                        raise ValueError('Restored page does not confirm the saved grade for q-' + number)
                    self.advance(state, directory, token)
                    continue
            if kind in ('e','q'):
                self.page.wait_for_function('''({id,kind}) => {
                  const e=document.getElementById(id); if(!e) return false;
                  const prompt=e.querySelector(kind==='e'?'.exampleQuestion':'.questionWidget-text');
                  if(!prompt?.textContent.trim() && !prompt?.querySelector('img,canvas,svg')) return false;
                  if(kind==='e' && !e.querySelector('.exampleExplanation')?.textContent.trim()) return false;
                  if(kind==='q' && !e.querySelector('.questionWidget-choicesTable tr,.matheditor-wrapper-answer,.selectList,input,textarea,select,[contenteditable="true"]')) return false;
                  return [...e.querySelectorAll('mjx-container')].every(n=>!!n.querySelector('mjx-assistive-mml math, svg'));
                }''',arg={'id':'step-'+token,'kind':kind})
            if kind == 't':
                (directory / ('tutorial-' + number + '.html')).write_text(scope.evaluate('e => e.outerHTML'))
                self.advance(state, directory, token)
                continue
            if kind == 'e':
                item, screenshot = self.read(scope,directory,'example-' + number)
                mid = 'e-' + number
                kp = kp_for_example(topic, mid, item['name'], allow_new=True)
                kp_id = str(kp[':knowledge-point/id'])
                if not item['problem'] or not item['worked_solution']:
                    raise ValueError('Canonical example is incomplete: ' + mid)
                if item['fields']:
                    raise ValueError('Example exposes interactive fields; review this new example layout')
                state['current_kp'] = kp_id
                state['kps'].setdefault(kp_id,{'id':kp_id,'title':kp[':knowledge-point/title'],
                                             'sequence':'CCCCC' if perfect else choose_sequence(self.pacer.rng,self.args.cwcwc_weight)})
                if kp.get('captured_new'):
                    state['kps'][kp_id]['source_example_id'] = mid
                state['examples'][mid] = {'math_academy_id':mid,'knowledge_point_id':kp_id,
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
            if not record:
                item, screenshot = self.read(scope,directory,mid + '-before')
                if not item['problem'] or not item['fields']:
                    raise ValueError('Question content or answer fields are not loaded: ' + mid)
                count = len(state['questions']) if is_review else sum(q['kp_id'] == kp_id for q in state['questions'].values())
                if is_review:
                    if count >= getattr(self.args, 'review_question_limit', 20):
                        raise ValueError('Review question limit reached; capture saved before another submission')
                    sequence = state['review_sequence']
                    intended = sequence[count % len(sequence)]
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
                # Choice letters may be shuffled on a restored page. Reuse the
                # solved value, then match it to today's observed DOM option.
                fresh, _ = self.read(scope,directory,mid + '-before')
                if normalize(fresh['problem']) != normalize(record['before']['problem']):
                    raise ValueError('Restored question problem changed: ' + mid)
                from solver import Solver
                record['decision'] = Solver.reuse_answer(fresh,record['decision'])
                record['before'] = fresh
                save()
                self.enter(scope,record)
                self.pacer.wait('answer','before submitting an answer',elapsed=record.get('solver_elapsed_seconds',0))
                self.check()
                try:
                    self.verify_entered(scope, record)
                finally:
                    save()  # Retain the observed input even when verification stops.
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
            record['after'], record['actual_result'] = item, actual
            record['status'] = 'graded'
            save()
            self.finalize_question(state,directory,mid,record)
            save()
            logging.info('%s: %s, captured %d fields',mid,actual,len(record['content']['answer_fields']))
            self.advance(state, directory, token)

    def finalize_question(self, state, directory, mid, record):
        expected = 'Correct' if record['intended'] == 'C' else 'Incorrect'
        actual, item = record['actual_result'], record['after']
        if actual != expected:
            raise ValueError(mid + ' expected ' + expected + ', received ' + actual + '; stop before another answer')
        if not item['worked_solution']:
            raise ValueError('Revealed worked solution is missing: ' + mid)
        if actual == 'Incorrect' and not record.get('verification'):
            verified = self.solver.solve(item,Path(directory)/(mid+'-after.png'),Path(directory)/mid,'verify')
            original = {a['key']:a for a in record['decision']['answers']}
            for answer in verified['answers']:
                first = original[answer['key']]
                if normalize(first['correct_value'],first['value_type']) != normalize(answer['correct_value'],answer['value_type']):
                    raise ValueError('Worked solution contradicts predicted correct answer: ' + mid)
            record['verification'] = verified
        kp = {'id':None,'title':None} if state.get('task_type') == 'review' else state['kps'][record['kp_id']]
        record['content'] = self.question_content(mid,record,kp)
        record['finalized'] = True

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
                saved = record.get('wrong_choice') if wrong else None
                if saved:
                    if saved['key'] != field['key']:
                        raise ValueError('Saved incorrect choice belongs to a different field')
                    choices = [c for c in choices if c['type'] == saved['type'] and
                               normalize(c['value'],c['type']) == normalize(saved['value'],saved['type'])]
                    if len(choices) != 1:
                        raise ValueError('Saved incorrect choice does not match exactly one restored option')
                    chosen = choices[0]
                else:
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
                control = answer_control(scope,field)
                if field['tag'] == 'mathquill':
                    editor = control.locator('.mq-textarea textarea')
                    # A nearby field can sit underneath the previous field's
                    # floating symbol menu. Native textarea focus changes the
                    # active editor and fires its usual focus/blur handlers.
                    editor.focus()
                    editor.press('ControlOrMeta+A')
                    editor.press('Backspace')
                    actions = mathquill_keys(value, answer['wrong_keys' if wrong else 'correct_keys'])
                    field['entered_keys'] = actions
                    symbol_just_inserted = False
                    for action in actions:
                        if action['text'] is not None:
                            symbol_just_inserted = self.type_mathquill(editor, action['text'], field)
                        else:
                            if not (symbol_just_inserted and action['key'] == 'Space'):
                                editor.press(action['key'])
                            symbol_just_inserted = False
                else:
                    control.fill(value)
                field['submitted_value'] = value
            wrong_used |= wrong

    def type_mathquill(self, editor, text, field):
        # These classes belong to Math Academy's displayed symbol toolbox.
        # Math Academy hides the previous editor's toolbox after 100 ms.
        # Wait out overlapping toolboxes before choosing a visible button.
        symbol_just_inserted = False
        for part in re.split(r'(\\(?:pi|theta|alpha|beta|gamma|delta|lambda|mu|rho|sigma|phi|omega|infty|ln)\b\s*)', text):
            if not part:
                continue
            symbol = re.fullmatch(r'\\([a-z]+)\s*', part)
            if symbol:
                symbol_just_inserted = True
                name = symbol[1]
                selector = '#mathEditorToolbox .mathIcon.' + name + 'Icon'
                buttons = self.page.locator(selector + ':visible')
                if buttons.count() > 1:
                    from playwright.sync_api import expect
                    try:
                        expect(buttons).to_have_count(1, timeout=self.args.timeout_ms)
                    except AssertionError as exc:
                        raise ValueError('Symbol toolboxes did not settle to one visible button: ' + name
                                         + '; stop before Submit') from exc
                    field.setdefault('waited_for_symbols', []).append(name)
                if buttons.count() == 1:
                    buttons.click()
                    field.setdefault('clicked_symbols', []).append({'symbol': name, 'selector': selector})
                else:
                    editor.press_sequentially('\\' + name, delay=self.pacer.rng.uniform(60,140))
                    # In MA's distribution Space inserts a mathematical space,
                    # splitting the numerator; ArrowRight preserves its grouping.
                    # Finish the active root command while keeping its cursor
                    # inside the radicand; ArrowRight would immediately exit it.
                    editor.press('Enter' if name == 'sqrt' else 'ArrowRight')
                    if name in ('ln','sin','cos','tan','sec','csc','cot'):
                        # Match a function button's empty argument when the
                        # current field has no button for this named function.
                        editor.press_sequentially('(', delay=self.pacer.rng.uniform(60,140))
            else:
                symbol_just_inserted = False
                editor.press_sequentially(part, delay=self.pacer.rng.uniform(60,140))
        return symbol_just_inserted

    def verify_entered(self, scope, record):
        for field in record['before']['fields']:
            if field['type'] == 'radio':
                selected = scope.locator('.questionWidget-choiceLetterCircle, .choiceLetterCircle').evaluate_all('''nodes => nodes.filter(n =>
                  n.classList.contains('selectedChoice') || (n.style.backgroundColor === 'rgb(64, 64, 64)' &&
                  n.style.color === 'white')).map(n => n.textContent.trim())''')
                if selected != [field['submitted_option']]:
                    raise ValueError('Actual selected radio option differs from intended option; stop before Submit')
                field['observed_selected_option'] = selected[0]
            elif field['type'] == 'select' and field['tag'] == 'select':
                if by_id(scope,field['dom_id']).input_value() != field['submitted_option']:
                    raise ValueError('Actual selected option differs from intended option; stop before Submit')
            elif field['type'] == 'blank' and field['tag'] != 'mathquill':
                if by_id(scope,field['dom_id']).input_value() != field['submitted_value']:
                    raise ValueError('Actual blank value differs from intended value; stop before Submit')
            elif field['tag'] == 'mathquill':
                observed = answer_control(scope,field).evaluate(MATHQUILL_VALUE)
                field['observed_mathquill_latex'] = observed
                if not isinstance(observed, str) or normalize_mathquill(observed) != normalize_mathquill(field['submitted_value']):
                    raise ValueError('Actual MathQuill value differs from intended value; stop before Submit: '
                                     + repr(observed) + ' != ' + repr(field['submitted_value']))

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
        result = {'math_academy_id':mid,'knowledge_point_id':kp['id'],
                  'knowledge_point':kp['title'],'problem':record['before']['problem'],
                  'worked_solution':record['after']['worked_solution'],'answer_fields':fields}
        if instructions and not re.search(r'not|without|forbidden',instructions,re.I):
            result['requires_calculator'] = True
        return result

    def history(self, state, directory, topic=None):
        if state.get('task_type') in ('assessment','multistep'):
            from assessment import assessment_history
            return assessment_history(self,state,directory,topic)
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
                matches = [kp for kp in topic[':topic/knowledge-points'] if kp_title_identity(kp[':knowledge-point/title']) == kp_title_identity(title)]
                if len(matches) != 1:
                    raise ValueError('Review KP title cannot be matched uniquely within the topic: ' + mid)
                kp_id = str(matches[0][':knowledge-point/id'])
                record['kp_id'] = kp_id
                record['content'].update(knowledge_point_id=kp_id, knowledge_point=matches[0][':knowledge-point/title'])
                state['kps'].setdefault(kp_id, {'id':kp_id, 'title':matches[0][':knowledge-point/title']})
                record['content']['knowledge_point_source_id'] = int(source[2])
            elif kp_title_identity(record['content']['knowledge_point']) != kp_title_identity(title):
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
            atomic_json(directory/'state.json',state)
        atomic_json(directory / 'activity-metadata.json',metadata)
        state['history_complete'] = True
        atomic_json(directory / 'state.json',state)
        content = {'task_id':state['task_id'],'task_type':task_type,'topic_id':state['topic_id'],'content_only':True,
                   'source_url':self.page.url,'sequence_policy':{'CWCWC':self.args.cwcwc_weight,'WCWCC':1-self.args.cwcwc_weight},
                   'questions':[q['content'] for q in state['questions'].values()],
                   'canonical_examples':list(state['examples'].values())}
        new_points=[{'id':kp['id'],'title':kp['title'],'source_example_id':kp['source_example_id']}
                    for kp in state['kps'].values() if kp.get('source_example_id')]
        if new_points:
            content['new_knowledge_points'] = new_points
        if task_type == 'review':
            content['sequence_policy'] = {'scope':'whole review','CWCWC':self.args.cwcwc_weight,
                'WCWCC':1-self.args.cwcwc_weight,'sequence':state['review_sequence'],
                'continuation':'repeat saved pattern until site completion'}
        if state.get('answer_policy') == 'all_correct':
            content['sequence_policy'] = {'answer_policy':'all_correct','perfect_retake_of':state['perfect_retake_of']}
        atomic_json(directory / 'content.json',content)
        return content
