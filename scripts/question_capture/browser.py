"""Sequential Playwright UI capture with checkpoints before every submission."""
import json
import hashlib
import logging
import re
import time
from collections import deque
from pathlib import Path
from urllib.parse import urlparse

from core import atomic_json, assessment_can_start, assessment_requirement, choose_sequence, choose_review_sequence, compare_answers, journal, normalize, stable_id
from progress import COURSES, capture as capture_progress

EXTRACT = (Path(__file__).parent / 'dom.js').read_text()
SELECT_SNAPSHOT = '''n => {
  const root=document.createElement('div'), prompt=document.createElement('div');
  prompt.className='questionText';prompt.appendChild(n.cloneNode(true));root.appendChild(prompt);
  const item=('''+EXTRACT+''')(root);
  return {value:item.problem, images:item.assets.map(a=>a.source_url), errors:item.errors};
}'''
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
  const diagnostic=href.match(/^\/tasks\/(\d+)\/diagnostics\/(\d+)$/);
  const kind=e.querySelector('.taskTypeUnlocked')?.textContent.trim().toLowerCase() || 'unknown';
  const progress=Number(e.getAttribute('progress'));
  const supported=(!!lesson && kind === lesson[3]) || (!!test && kind === 'assessment') || (!!multistep && kind === 'multistep') || (!!diagnostic && kind === 'diagnostic');
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
    ...(kind === 'diagnostic' ? {diagnostic_id:diagnostic ? Number(diagnostic[2]) : null,
      diagnostic_card_html:e.outerHTML} : {}),
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
    # Repair an exact older solver action pattern that omitted the outer fence
    # explicitly present in the intended value. Verification still checks it.
    powered_log = re.fullmatch(r'\(\\ln\((\d+)\)\)\^(\d+)',value)
    if powered_log and result == [
            {'text':r'\ln','key':None},{'text':powered_log[1],'key':None},
            {'text':None,'key':'ArrowRight'},{'text':'^'+powered_log[2],'key':None},
            {'text':None,'key':'ArrowRight'}]:
        result = [{'text':'(','key':None}] + result[:3] + [{'text':None,'key':'ArrowRight'}] + result[3:]
    # MathQuill's slash captures only the last term of an unfenced sum.
    # Group an exact whole-numerator action before creating its fraction.
    fraction = re.fullmatch(r'\\+frac\{([^{}]+)\}\{(.+)\}', value)
    if (fraction and re.search(r'.[+-]', fraction[1]) and len(result) >= 2 and
            result[0] == {'text':fraction[1],'key':None} and
            result[1] == {'text':'/','key':None}):
        result[0]['text'] = '(' + fraction[1] + ')'
    # Closing the typed parentheses already leaves their inner cursor.
    # In this exact saved pattern, the next Right exits the denominator.
    powered_denominator = re.fullmatch(r'(.+)\\frac\{([^{}]+)\}\{(\([^{}]+\))\^(\d+)\}', value)
    if powered_denominator:
        prefix, numerator, base, power = powered_denominator.groups()
        expected = [
            {'text':prefix + numerator,'key':None},
            {'text':'/','key':None},
            {'text':base,'key':None},
            {'text':None,'key':'ArrowRight'},
            {'text':'^' + power,'key':None},
            {'text':None,'key':'ArrowRight'},
            {'text':None,'key':'ArrowRight'}]
        if result == expected:
            result = result[:3] + result[4:]
    return result


def normalize_mathquill(value):
    """Compare editor notation without treating differently grouped math as equal."""
    return normalize(value)


def same_question_problem(before, after):
    if normalize(before['problem']) == normalize(after['problem']):
        return True
    # Reloaded graded blanks are static math instead of answer widgets.
    rendered = before['problem']
    for field in before.get('fields', []):
        value = field.get('observed_mathquill_latex', field.get('submitted_value'))
        if value is not None:
            rendered = rendered.replace('{{' + field['key'] + '}}', '$' + value + '$')
    return normalize(rendered) == normalize(after['problem'])


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
    from playwright.sync_api import Error as PlaywrightError
    try:
        return _repair_math_editor_document(route)
    except PlaywrightError as error:
        # An exception escaping this callback strands Playwright's pending
        # navigation. Always finish the route; page.goto can then handle retry.
        logging.warning('Document request failed (%s); releasing navigation for retry',
                        network_failure_reason(error))
        try:
            route.abort('connectionfailed' if is_network_error(error) else 'failed')
        except PlaywrightError:
            pass  # A closed page or completed route needs no further action.


def _repair_math_editor_document(route):
    if route.request.resource_type != 'document' or route.request.method != 'GET':
        return route.continue_()
    # Let the browser follow redirects so page scripts see the destination URL.
    # Fetching the final document and fulfilling /learn leaves its URL unchanged.
    response = route.fetch(max_redirects=0,timeout=30000)
    if response.status in (301,302,303,307,308):
        return route.fulfill(response=response)
    if 'text/html' not in response.headers.get('content-type','').lower():
        return route.fulfill(response=response)
    original = response.text()
    cleaned = deduplicate_math_editor(original)
    if cleaned != original:
        logging.info('Removed duplicate math-editor.js tag from %s',route.request.url)
    route.fulfill(response=response,body=cleaned)


def is_network_error(error):
    return bool(re.search(r'\b(?:EAI_AGAIN|ENOTFOUND|ECONNRESET|ECONNREFUSED|EHOSTUNREACH|ENETUNREACH|ETIMEDOUT)\b|'
                          r'getaddrinfo|net::ERR_(?:NAME_NOT_RESOLVED|NAME_RESOLUTION_FAILED|INTERNET_DISCONNECTED|'
                          r'CONNECTION_(?:FAILED|REFUSED|RESET|CLOSED|ABORTED|TIMED_OUT)|NETWORK_CHANGED|'
                          r'ADDRESS_UNREACHABLE|TIMED_OUT)',str(error)))


def network_failure_reason(error):
    # Route.fetch's full error includes request headers. Log only its error code.
    match=re.search(r'\b(?:EAI_AGAIN|ENOTFOUND|ECONNRESET|ECONNREFUSED|EHOSTUNREACH|ENETUNREACH|ETIMEDOUT)\b|'
                    r'net::ERR_[A-Z_]+',str(error))
    return match[0] if match else type(error).__name__


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


def history_kp_matches(topic_id, live, history):
    # Observed live example / results-page title variants, scoped to their
    # topics. Preserve the canonical example's KP ID; never fuzzy-match titles.
    aliases = {
        612: ('Identifying the Largest Intervals of Continuity of a Function',
              'Identifying the Intervals of Continuity of a Function'),
        708: ('Solving a Rational Equations by Factoring a Quadratic Denominator With No Constant Term',
              'Solving Rationals Equations by Factoring a Quadratic Denominator With No Constant Term'),
    }
    return kp_title_identity(live) == kp_title_identity(history) or aliases.get(topic_id) == (live,history)


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


def history_asset_bindings(incoming, record, mid):
    """Match explanation images only when the saved solution text is identical."""
    after = record.get('after', {})
    if record.get('status') != 'graded' or not after.get('worked_solution'):
        return []
    image = r'!\[[^\]]*\]\(([^)]+)\)'
    old_paths = re.findall(image, after['worked_solution'])
    new_paths = re.findall(image, incoming.get('worked_solution', ''))
    normalized = lambda text: re.sub(r'\s+', ' ', re.sub(image, '![](@image@)', text)).strip()
    if (len(old_paths) != len(new_paths) or not old_paths or
            normalized(after['worked_solution']) != normalized(incoming.get('worked_solution', ''))):
        return []
    originals = {a.get('path'):a for a in after.get('assets', [])}
    result = []
    for old_path, marker in zip(old_paths, new_paths):
        found = re.fullmatch(r'@asset-(\d+)@', marker)
        if not found:
            continue
        index = int(found[1])
        if index >= len(incoming.get('assets', [])):
            continue
        alias = incoming['assets'][index].get('source_url', '')
        original = originals.get(old_path, {})
        path = Path(old_path)
        if (re.fullmatch(r'https://mathacademy\.com/graphics/'+re.escape(mid)+r'-e-\d+', alias) and
                original.get('source_url') and original.get('content_type') and path.is_file() and
                original.get('sha256') == hashlib.sha256(path.read_bytes()).hexdigest()):
            result.append((index, original))
    return result


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
        from playwright.sync_api import Error as PlaywrightError, TimeoutError as PlaywrightTimeout
        if self.page.url == url and not force:
            self.check()
            return
        attempt = 0
        while True:
            attempt += 1
            self.pacer.wait('event', 'page navigation')
            try:
                response = self.page.goto(url, wait_until='domcontentloaded')
                if response and response.request.redirected_from:
                    if url == LEARN and re.search(r'/tasks/\d+/(?:tests|diagnostics)/\d+(?:[/?#]|$)',self.page.url):
                        self.check()
                        return  # The queue caller reports the forced active assessment.
                    # Playwright routes only the first request of a redirect
                    # chain. Load the destination once directly so its document
                    # receives the same editor-tag repair as other navigations.
                    self.pacer.wait('event','initialize redirected page')
                    response = self.page.goto(self.page.url, wait_until='domcontentloaded')
            except PlaywrightError as error:
                if not isinstance(error,PlaywrightTimeout) and not is_network_error(error):
                    raise
                self.check()
                logging.warning('Navigation unavailable (%s); retaining checkpoints and waiting for network recovery',
                                network_failure_reason(error))
                self.pacer.backoff(attempt)
                continue
            self.check()
            if response and response.status >= 500:
                logging.warning('Math Academy returned HTTP %s; waiting for service recovery',response.status)
                self.pacer.backoff(attempt)
                continue
            # Positioned assessment content can leave the body with zero height.
            # Require a visible body or child; hidden pages still fail.
            self.page.locator('body:visible, body > :visible').first.wait_for(state='visible')
            return

    def queue(self):
        self.navigate(LEARN, force=True)
        if re.search(r'/tasks/\d+/(?:tests|diagnostics)/\d+(?:[/?#]|$)',self.page.url):
            raise ValueError('Math Academy redirected the queue to an unfinished assessment or diagnostic: '+self.page.url+'; restoring its saved capture')
        self.page.locator('#incompleteTasks').wait_for(state='attached')
        # Wait for the asynchronous task list, allowing an empty queue.
        self.page.wait_for_timeout(self.args.settle_ms)
        self.check()
        if getattr(self.args,'state_dir',None):
            from dashboard import capture as capture_dashboard
            capture_dashboard(self.page,self.args.state_dir)
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
            if item['task_type'] in ('multistep','diagnostic') and not item['href']:
                self.pacer.wait('event','expand '+item['task_type']+' queue details')
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
        course = self.page.locator('a#courseNameLink, a.courseNameLink').first
        if course.count():
            match = re.fullmatch(r'/courses/(\d+)/progress',course.get_attribute('href') or '')
            for item in queue:
                if item['task_type'] == 'diagnostic':
                    item.update(course_id=int(match[1]) if match else None,course_name=course.inner_text().strip())
        for item in queue:
            if item['task_type'] == 'assessment':
                item.update(assessment_requirement(item['assessment_details'], only_activity=len(queue) == 1,
                                                   title=item['title']))
        return queue

    def start(self, activity):
        kind = activity.get('task_type', 'lesson')
        if kind not in ('lesson','review','assessment','multistep','diagnostic') or not activity.get('capture_supported',True):
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
            if kind not in ('multistep','diagnostic') or not card.locator('.taskDetails').is_visible():
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
                    '**/tasks/' + str(activity['task_id']) + '/diagnostics/' + str(activity['diagnostic_id'])
                    if kind == 'diagnostic' else
                    '**/tasks/' + str(activity['task_id']) + '/topics/' + str(activity['topic_id']) + '/' + kind)
        self.page.wait_for_url(expected,wait_until='domcontentloaded')
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
                recovered = False
                if asset.is_visible() and asset.evaluate("n => n.localName === 'img' && n.complete && n.naturalWidth === 0"):
                    self.pacer.backoff(1)
                    asset.evaluate('n => { n.src = n.src; }')
                    try:
                        asset.wait_for(state='visible')
                        self.page.wait_for_function('n => n.complete && n.naturalWidth > 0', arg=asset.element_handle())
                        recovered = True
                    except PlaywrightTimeout:
                        pass
                if not recovered:
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
        from progress import targets, target as progress_target
        courses = targets(self.args,state)
        sidebar=state.get('progress_mode',getattr(self.args,'progress_mode','fixed'))=='sidebar'
        snapshots = state.setdefault('knowledge_snapshots', {})
        target = directory / 'knowledge-state' / (event + '.json')
        if target.exists():
            snapshot = json.loads(target.read_text())
            observed=tuple(c.get('source_url') or progress_target(c['course_id'])['source_url'] for c in snapshot['courses'])
            expected=tuple(progress_target(c)['source_url'] for c in courses)
            if snapshot['task_id'] != state['task_id'] or not sidebar and observed != expected:
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
            if sidebar:
                start_url=self.page.evaluate("() => document.querySelector('a#courseNameLink, a.courseNameLink')?.getAttribute('href') || null")
                if start_url and start_url.startswith('/'):start_url='https://mathacademy.com'+start_url
                if not start_url:
                    enrolled=state.get('course_id') or getattr(self.args,'diagnostic_course_id',None)
                    start_url=progress_target(enrolled or courses[-1])['source_url']
                snapshot = capture_progress(self.progress_reader, target.parent, event, state['task_id'],
                                            None, previous, recovered, start_url=start_url)
            else:
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
        # Called while restoring saved activity state after fresh navigation.
        # The server's empty unanswered widgets determine whether to retry.
        fields = record['before']['fields']
        radio = len(fields) == 1 and fields[0]['type'] == 'radio'
        blanks = bool(fields) and all(f['type'] == 'blank' for f in fields)
        if not (radio or blanks):
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
        if blanks:
            empty = []
            for field in fields:
                control = answer_control(scope, field)
                value = control.evaluate(MATHQUILL_VALUE) if field['tag'] == 'mathquill' else control.input_value()
                empty.append(value == '')
            evidence['blanks_empty'] = all(empty)
        if not (evidence['unanswered'] and evidence['submit_visible'] and evidence['submit_disabled']
                and (evidence['choices_unselected'] if radio else evidence['blanks_empty']) and not evidence['pending']):
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

    @staticmethod
    def is_staged_question(scope):
        # DynamicSelect renders a health bar before any later proof sections
        # exist. Static selects have no health bar; ordinary questions keep
        # their existing player.
        return bool(scope.locator('.proofSection').count() or (
            scope.locator('.questionWidget-healthFrame').count() and scope.locator('.selectList').count()))

    @staticmethod
    def restored_proof_rejection(directory, record, item):
        """Bind a transient saved rejection to the same restored server stage."""
        def health(capture):
            match = re.search(r'class="questionWidget-healthBar"[^>]*style="[^\"]*width:\s*([\d.]+)%',capture.get('html',''))
            return float(match[1]) if match else None
        before = record['before']
        old_health, current_health = health(before), health(item)
        if old_health is None or current_health is None:
            return None
        # The initial health bar animates from 0% after rendering. Permit that
        # first-stage placeholder only with an exact saved rejection binding;
        # later submissions still require a real decline in the displayed bar.
        if current_health >= old_health and not (old_health == 0 and not record.get('proof_stages')):
            return None
        if before.get('dom_id') != item.get('dom_id') or normalize(before['problem']) != normalize(item['problem']):
            return None
        identity = lambda f: (f['key'],f['dom_id'],[(c['type'],normalize(c['value'],c['type'])) for c in f['choices']])
        if [identity(f) for f in before['fields']] != [identity(f) for f in item['fields']]:
            return None
        for source in sorted(Path(directory).glob('diagnostics/*/current-question.json'),reverse=True):
            captured = json.loads(source.read_text())
            if (captured.get('proof_feedback') != "Oops, that's not quite right. Please try again." or
                    captured.get('dom_id') != item.get('dom_id') or health(captured) != current_health or
                    normalize(captured.get('problem','')) != normalize(item['problem']) or captured.get('errors') or
                    [identity(f) for f in captured['fields']] != [identity(f) for f in item['fields']]):
                continue
            matches = True
            for old, restored, graded in zip(before['fields'],item['fields'],captured['fields']):
                selected = restored.get('source_selected',{})
                saved = graded.get('source_selected',{})
                if (not selected or selected != saved or 'submitted_value' not in old or
                        normalize(selected['value'],selected['type']) != normalize(old['submitted_value'],selected['type'])):
                    matches = False
                    break
            if matches:
                return {'path':str(source.resolve()),'sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
                        'before_health_percent':old_health,'restored_health_percent':current_health,
                        'reason':'saved source rejection and restored selections/health match the pending submission'}
        return None

    def proof_question(self, scope, record, directory, mid, save):
        """Complete only newly exposed proof fields, inspecting every stage grade."""
        from solver import Solver
        stages = record.setdefault('proof_stages', [])
        if record['status'] == 'submitting' and not record.get('proof_pending'):
            record['proof_pending'] = {'keys':[f['key'] for f in record['before']['fields']]}
            save()
        while True:
            self.check()
            stage = len(stages)
            item, screenshot = self.read(scope, directory, mid + '-proof-observed-' + str(stage))
            current = {f['key']:f for f in item['fields']}
            previous = {f['key']:f for f in record['before']['fields']}
            if not set(previous).issubset(current):
                raise ValueError('Proof stage lost previously captured fields: ' + mid)
            for key, old in previous.items():
                fresh = current[key]
                if old['dom_id'] != fresh['dom_id'] or old['choices'] != fresh['choices']:
                    # Re-rendering changes generated HTML, but not source values.
                    identity = lambda f: [(c['option'],c['type'],normalize(c['value'],c['type'])) for c in f['choices']]
                    if old['dom_id'] != fresh['dom_id'] or identity(old) != identity(fresh):
                        raise ValueError('Proof stage changed a captured field: ' + key)
                for name in ('submitted_value','submitted_option','entered_keys'):
                    if name in old: fresh[name] = old[name]
            pending = record.get('proof_pending')
            terminal = item.get('result') in ('Correct','Incorrect','Partial Credit')
            if pending and not terminal:
                submitted = [current.get(key, {}) for key in pending['keys']]
                retry = item.get('proof_feedback') == "Oops, that's not quite right. Please try again."
                rejection = None if retry else self.restored_proof_rejection(directory,record,item)
                retry = retry or rejection is not None
                if not submitted or not (retry or all(f.get('source_result') in ('Correct','Incorrect') for f in submitted)):
                    raise ValueError('Uncertain proof submission has no source outcome; stop without resubmission: ' + mid)
                for field in submitted:
                    observed = field.get('source_selected', {})
                    if ('submitted_value' not in field or normalize(observed.get('value',''),observed.get('type','text')) !=
                            normalize(field['submitted_value'],observed.get('type','text'))):
                        raise ValueError('Proof source grade does not match the submitted value: ' + field.get('key','unknown'))
                predictions = {a['key']:a for a in record['decision']['answers']}
                for field in submitted:
                    prediction = predictions.get(field['key'],{})
                    distinct = normalize(field['submitted_value'],prediction.get('value_type','text')) != normalize(
                        prediction.get('correct_value',''),prediction.get('value_type','text'))
                    if record['intended']=='W' and distinct:
                        record['wrong_submission_used'] = True
                    if field.get('source_result')=='Incorrect' and not distinct:
                        record['proof_needs_solve'] = True
                if retry and not any(normalize(f['submitted_value']) != normalize(
                        predictions.get(f['key'],{}).get('correct_value','')) for f in submitted):
                    record['proof_needs_solve'] = True
                rejected = [[f['key'],f.get('submitted_value')] for f in submitted if retry or f.get('source_result')=='Incorrect']
                repeats = sum(s.get('rejected_values')==rejected for s in stages) if rejected else 0
                stages.append({'submitted_keys':pending['keys'], 'outcome':'accepted' if all(
                    f.get('source_result')=='Correct' for f in submitted) else 'rejected', 'observation':item,
                    'decision':record['decision'], 'intended':record['intended'], 'rejected_values':rejected,
                    'restored_rejection_evidence':rejection})
                record.pop('proof_pending',None)
                record['status'] = 'prepared'
                if repeats >= 1:
                    save()
                    raise ValueError('Repeated unchanged proof rejection; stop before another submission: ' + mid)
            record['before'] = item
            save()
            if terminal:
                if pending:
                    stages.append({'submitted_keys':pending['keys'], 'outcome':item['result'],
                                   'observation':item, 'decision':record['decision'], 'intended':record['intended']})
                record.pop('proof_pending',None)
                record.pop('entry_keys',None)
                item, _ = self.read(scope,directory,mid+'-after')
                record.update(after=item,actual_result=item['result'],status='graded')
                save()
                return
            keys = [f['key'] for f in item['fields'] if f.get('source_result') != 'Correct']
            if not keys:
                raise ValueError('Proof accepted every field without exposing a next stage or final grade')
            # New stages have their own answer artifacts but use this activity's
            # existing solver session. The question keeps its one C/W decision.
            known = {a['key'] for a in record['decision']['answers']}
            if known != set(current) or record.get('proof_needs_solve'):
                started = time.monotonic()
                record['decision'] = self.solver.solve(item,screenshot,Path(directory)/mid,'proof-solve-'+str(len(stages)))
                record['solver_elapsed_seconds'] = time.monotonic()-started
                record.pop('proof_needs_solve',None)
            else:
                record['decision'] = Solver.reuse_answer(item,record['decision'])
            item, screenshot = self.read(scope,directory,mid+'-before')
            for field in item['fields']:
                for name in ('submitted_value','submitted_option','entered_keys'):
                    if name in current[field['key']]:field[name]=current[field['key']][name]
            record['before'] = item
            record['entry_keys'] = keys
            save()
            self.enter(scope,record)
            self.pacer.wait('answer','before submitting a proof stage',elapsed=record.get('solver_elapsed_seconds',0))
            self.check()
            self.verify_entered(scope,record)
            self.page.screenshot(path=str(Path(directory)/(mid+'-proof-entered-'+str(len(stages))+'.png')))
            record['proof_pending'] = {'keys':keys,'feedback_before':item.get('proof_feedback')}
            record['status'] = 'submitting'
            save()
            journal(Path(directory)/'events.jsonl','proof_submission_intent',question=mid,stage=len(stages),intended=record['intended'],keys=keys)
            submit=scope.locator('.questionWidget-submitButton')
            if 'disabledButton' in (submit.get_attribute('class') or ''):
                raise ValueError('Proof Submit is disabled after filling observed fields')
            submit.click()
            self.page.wait_for_function('''({id,ids,feedbackBefore})=>{
              const n=document.getElementById(id),visible=e=>{const r=e?.getBoundingClientRect();return !!r && r.width>0 && r.height>0 && getComputedStyle(e).visibility!=='hidden';};
              if(visible(document.getElementById('continueButton-'+id.replace('step-','')))) return true;
              const frames=ids.map(id=>document.getElementById(id)?.querySelector('.selectListFrame,.selectListFrameDisabled'));
              // These classes are a completed source grade even when the site's
              // empty spinner retains display:block after the request finishes.
              if(frames.every(e=>e?.matches('.correctSelection,.correctSelectionMultipleAttempts'))) return true;
              const spinner=n?.querySelector('.questionWidget-spinner');
              if(visible(spinner) && spinner.style.display==='block') return false;
              if(visible(n?.querySelector('.questionWidget-feedback')) &&
                 n.querySelector('.questionWidget-feedback').textContent.trim()==="Oops, that's not quite right. Please try again." &&
                 feedbackBefore!=="Oops, that's not quite right. Please try again.") return true;
              return frames.every(e=>e?.matches('.correctSelection,.correctSelectionMultipleAttempts,.incorrectSelection'));
            }''',arg={'id':scope.get_attribute('id'),'ids':[current[key]['dom_id'] for key in keys],
                     'feedbackBefore':record['proof_pending']['feedback_before']})

    def activity(self, state, directory, topic):
        if state.get('task_type') == 'diagnostic':
            from diagnostic import take_diagnostic
            return take_diagnostic(self,state,directory)
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
            if record.get('status') == 'submitting':
                proof_scope = by_id(self.page, 'step-' + mid.replace('-', ''))
                if (self.is_staged_question(proof_scope) and
                        self.current_step() == 'stepButton-' + mid.replace('-', '')):
                    # The proof player reconciles intermediate source grades;
                    # the ordinary player expects a whole-question result.
                    continue
            if record.get('status') == 'submitting' and self.current_step() == 'stepButton-' + mid.replace('-', ''):
                scope = by_id(self.page, 'step-' + mid.replace('-', ''))
                if self.restore_unanswered_submission(scope, record):
                    save()
                    journal(directory / 'events.jsonl', 'submission_recovered_unanswered', question=mid)
            if record.get('status') == 'submitting':
                # A restored activity may open on the next question. Reconcile the
                # saved result before answering it, rather than orphaning a grade.
                source = directory / (mid + '-after.json')
                item = json.loads(source.read_text()) if source.exists() else {}
                # A grading response can succeed while step navigation fails.
                # Recover its actual result from the reloaded page when the
                # interrupted capture never saved a complete explanation.
                if (not item.get('worked_solution') or item.get('errors') or
                        item.get('result') not in ('Correct', 'Incorrect', 'Partial Credit') or
                        normalize(item.get('problem', '')) != normalize(record['before']['problem'])):
                    scope = by_id(self.page, 'step-' + mid.replace('-', ''))
                    grade = scope.locator('.questionWidget-result')
                    if grade.count() and grade.inner_text().strip() in ('Correct', 'Incorrect', 'Partial Credit'):
                        if not scope.is_visible():
                            self.pacer.wait('event', 'restore graded question for capture')
                            by_id(self.page, 'stepButton-' + mid.replace('-', '')).click()
                            scope.wait_for(state='visible')
                        item, _ = self.read(scope, directory, mid + '-after')
                if (item.get('errors') or item.get('result') not in ('Correct', 'Incorrect', 'Partial Credit') or
                    not item.get('worked_solution') or
                    not same_question_problem(record['before'], item) or
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
                from retry_policy import earned_xp, completion_outcome
                state['earned_xp'] = earned_xp(completion)
                save()  # Even a failed completion must trigger a perfect retake.
                outcome = completion_outcome(completion,kind_name)
                if outcome is None:
                    raise ValueError(kind_name.title() + ' ended without completion: ' + completion)
                if not state['questions'] or not all(q.get('finalized') for q in state['questions'].values()):
                    raise ValueError('Completion screen has incomplete captured content')
                if not is_review:
                    if not state['kps']:
                        raise ValueError('Lesson completed without captured knowledge points')
                    for kp in state['kps'].values():
                        count = sum(q['kp_id'] == kp['id'] and q.get('finalized') for q in state['questions'].values())
                        if outcome == 'failed':
                            if count < 1 or count > 5:
                                raise ValueError('Failed lesson has an unexpected captured KP question count')
                            continue
                        if count < 1 or count > 5:
                            raise ValueError('Knowledge point served an unexpected question count: ' + kp['title'])
                self.page.screenshot(path=str(directory / (completed_event + '.png')))
                state['completion'], state['activity_complete'], state[kind_name + '_complete'] = completion, True, True
                state['activity_outcome'] = outcome
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
            if self.is_staged_question(scope):
                self.proof_question(scope,record,directory,mid,save)
                self.finalize_question(state,directory,mid,record)
                save()
                logging.info('%s: %s, captured %d proof fields across %d stages',mid,
                             record['actual_result'],len(record['content']['answer_fields']),len(record['proof_stages']))
                self.advance(state,directory,token)
                continue
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
            record['grade_deviation'] = {'intended':expected, 'observed':actual}
            logging.warning('%s graded %s instead of %s; retaining the actual result and continuing',mid,actual,expected)
            if actual == 'Correct':
                record.setdefault('predicted_answers', json.loads(json.dumps(record['decision']['answers'])))
                submitted = {f['key']:f for f in record['before']['fields']}
                for answer in record['decision']['answers']:
                    field = submitted[answer['key']]
                    answer['correct_value'] = field['submitted_value']
                    answer['correct_option'] = field.get('submitted_option')
                    selected = next((c for c in field.get('choices', [])
                                     if c['option'] == field.get('submitted_option')), None)
                    if selected:
                        answer['value_type'] = selected['type']
        if not item['worked_solution']:
            raise ValueError('Revealed worked solution is missing: ' + mid)
        if actual in ('Incorrect','Partial Credit') and not record.get('verification'):
            verification_input = {**item, 'problem':record['before']['problem'], 'fields':record['before']['fields']}
            verified = self.solver.solve(verification_input,Path(directory)/(mid+'-after.png'),Path(directory)/mid,'verify')
            original = {a['key']:a for a in record['decision']['answers']}
            for answer in verified['answers']:
                first = original[answer['key']]
                outcome = compare_answers(first['correct_value'],answer['correct_value'],answer['value_type'],
                                          prompt=record['before']['problem'])['outcome']
                if first['value_type'] != answer['value_type'] or outcome != 'equivalent':
                    record.setdefault('predicted_answers', json.loads(json.dumps(record['decision']['answers'])))
                    record.setdefault('answer_reconciliations', []).append({
                        'key':answer['key'], 'predicted':first['correct_value'],
                        'worked_solution_answer':answer['correct_value'], 'comparison':outcome,
                        'reason':verified['explanation']})
                    first.update({key:answer[key] for key in ('correct_value','value_type','correct_option','correct_keys') if key in answer})
                    logging.warning('%s/%s: using the solver-reviewed worked-solution answer',mid,answer['key'])
            record['verification'] = verified
        kp = {'id':None,'title':None} if state.get('task_type') == 'review' else state['kps'][record['kp_id']]
        record['content'] = self.question_content(mid,record,kp)
        record['finalized'] = True

    def enter(self, scope, record):
        answers = {a['key']:a for a in record['decision']['answers']}
        wrong_used = record.get('wrong_submission_used',False)
        for field in record['before']['fields']:
            if record.get('entry_keys') is not None and field['key'] not in record['entry_keys']:
                continue
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
                    # MA reparents this menu to body when opened. Retain the
                    # exact option node while it still belongs to this field;
                    # a scoped locator would no longer find it after opening.
                    option = by_id(scope,field['dom_id']).locator(
                        '.selectListOptions > .selectListOption').nth(int(chosen['option'])).element_handle()
                    if option is None:
                        raise ValueError('Captured dropdown option is missing; stop before Submit')
                    expected = option.evaluate(SELECT_SNAPSHOT)
                    selected = by_id(scope,field['frame_id'])
                    observed = selected.evaluate(SELECT_SNAPSHOT)
                    already_selected = ('proof_stages' in record and
                        not selected.locator('.selectListSelectedText').count() and
                        not expected['errors'] and not observed['errors'] and
                        expected['images'] == observed['images'] and
                        normalize(expected['value'],'text') == normalize(observed['value'],'text'))
                    if not already_selected:
                        selected.click()
                        option.click()
                        observed = selected.evaluate(SELECT_SNAPSHOT)
                    if (expected['errors'] or observed['errors'] or expected['images'] != observed['images'] or
                            normalize(expected['value'],'text') != normalize(observed['value'],'text')):
                        raise ValueError('Actual selected dropdown value differs from intended option; stop before Submit')
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
            if wrong and record.get('entry_keys') is not None:
                record['wrong_submission_used'] = True

    def type_mathquill(self, editor, text, field):
        # These classes belong to Math Academy's displayed symbol toolbox.
        # Math Academy hides the previous editor's toolbox after 100 ms.
        # Wait out overlapping toolboxes before choosing a visible button.
        symbol_just_inserted = False
        for part in re.split(r'(\\(?:pi|theta|alpha|beta|gamma|delta|lambda|mu|rho|sigma|phi|omega|infty|ln|sin|cos|tan|sec|csc|cot|sqrt|leq|geq|le|ge|neq)\b\s*)', text):
            if not part:
                continue
            symbol = re.fullmatch(r'\\([a-z]+)\s*', part)
            if symbol:
                symbol_just_inserted = True
                name = symbol[1]
                icon = {'leq':'lte','le':'lte','geq':'gte','ge':'gte','neq':'ne'}.get(name,name)
                selector = '#mathEditorToolbox .mathIcon.' + icon + 'Icon'
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
                    # Finish the command while its input still owns the cursor.
                    # ArrowRight leaves an unfinished command whose latex()
                    # misleadingly already equals the intended symbol.
                    editor.press('Enter')
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
            if record.get('entry_keys') is not None and field['key'] not in record['entry_keys']:
                continue
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
                if answer_control(scope,field).locator('.mq-latex-command-input').count():
                    raise ValueError('Unfinished MathQuill command; stop before Submit')
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
            category = 'model_interpretation'
            grade = record.get('actual_result') or record['after'].get('result')
            if (grade == 'Correct' and f.get('submitted_value') is not None and
                    compare_answers(f['submitted_value'],answer['correct_value'],answer['value_type'],
                                    prompt=record['before']['problem'])['outcome'] == 'equivalent'):
                category = 'ma_successful_grade'
            fields.append({'key':f['key'],'type':f['type'],'choices':choices,'correct_value':answer['correct_value'],
                           'choices_complete':f.get('choices_complete',False), 'correct_origin':category})
        instructions = record['before'].get('calculator_instructions','')
        result = {'math_academy_id':mid,'knowledge_point_id':kp['id'],
                  'knowledge_point':kp['title'],'problem':record['before']['problem'],
                  'worked_solution':record['after']['worked_solution'],'answer_fields':fields}
        if instructions and not re.search(r'not|without|forbidden',instructions,re.I):
            result['requires_calculator'] = True
        return result

    def read_history(self, explanation, record, directory, mid):
        """Restore broken history image aliases from this question's live result."""
        incoming = explanation.evaluate(EXTRACT)
        bindings = history_asset_bindings(incoming, record, mid)
        handlers = []
        try:
            for index, original in bindings:
                source = incoming['assets'][index]['source_url']
                handler = lambda route, request, original=original: route.fulfill(
                    body=Path(original['path']).read_bytes(), content_type=original['content_type'])
                self.page.route(original['source_url'], handler)
                handlers.append((original['source_url'], handler))
                explanation.locator('img').evaluate_all('''(nodes, binding) => {
                  for (const image of nodes) if (image.src === binding.source) image.src=binding.original;
                }''', {'source':source, 'original':original['source_url']})
            if bindings:
                archive = Path(directory)/'history-recovery'
                archive.mkdir(exist_ok=True)
                for suffix in ('.json', '.png'):
                    old = Path(directory)/('history-'+mid+suffix)
                    saved = archive/old.name
                    if old.exists() and not saved.exists():
                        saved.write_bytes(old.read_bytes())
                atomic_json(archive/(mid+'-asset-bindings.json'), [
                    {'history_url':incoming['assets'][index]['source_url'], 'original':original}
                    for index, original in bindings])
            return self.read(explanation, directory, 'history-'+mid)
        finally:
            for url, handler in handlers:
                self.page.unroute(url, handler)

    def history(self, state, directory, topic=None):
        if state.get('task_type') in ('assessment','multistep','diagnostic'):
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
                matches = [kp for kp in topic[':topic/knowledge-points'] if
                           history_kp_matches(state['topic_id'], kp[':knowledge-point/title'], title)]
                if len(matches) != 1:
                    raise ValueError('Review KP title cannot be matched uniquely within the topic: ' + mid)
                kp_id = str(matches[0][':knowledge-point/id'])
                record['kp_id'] = kp_id
                record['content'].update(knowledge_point_id=kp_id, knowledge_point=matches[0][':knowledge-point/title'])
                state['kps'].setdefault(kp_id, {'id':kp_id, 'title':matches[0][':knowledge-point/title']})
                record['content']['knowledge_point_source_id'] = int(source[2])
            elif not history_kp_matches(state['topic_id'],record['content']['knowledge_point'],title):
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
            item, _ = self.read_history(explanation,record,directory,mid)
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
