"""Adaptive placement exams: correct prerequisites, skip requested course skills."""
import csv
import hashlib
import json
import logging
import re
from pathlib import Path

from core import atomic_json, journal


VIEW = r'''() => {
  const visible=n=>!!n?.getClientRects().length && getComputedStyle(n).visibility!=='hidden';
  const q=document.querySelector('#questionContainer');
  const title=q?.querySelector('.questionWidget-title')?.textContent.trim() || '';
  const number=title.match(/^Question\s+(\d+)$/);
  const circle=q?.querySelector('.questionWidget-choiceLetterCircle');
  const source=circle?.id.match(/^questionWidget-choiceLetterCircle-(\d+)-/);
  const prompt=q?.querySelector('.questionWidget-text');
  return {url:location.href, instructions:visible(document.querySelector('#initialScreen-startButton')),
    retry:visible(document.querySelector('#retryScreen-noButton')),
    number:visible(q) && number ? Number(number[1]) : null,
    source_question_id:source ? Number(source[1]) : null,
    result:visible(q) ? q.querySelector('.questionWidget-result')?.textContent.trim() || '' : '',
    next:visible(document.querySelector('#nextButton')),done:visible(document.querySelector('#doneButton')),
    ready:visible(q) && !!prompt && (!!prompt.textContent.trim() || !!prompt.querySelector('img,svg,canvas')) &&
      [...q.querySelectorAll('mjx-container')].every(n=>!!n.querySelector('mjx-assistive-mml math,svg')) &&
      (!!q.querySelector('.questionWidget-result')?.textContent.trim() ||
       !!q.querySelector('.questionWidget-choiceLetterCircle,.matheditor-wrapper-answer,input,textarea,select,.selectList'))};
}'''


def completed_url(state, url):
    return bool(re.fullmatch(r'https://mathacademy\.com/tasks/' + str(state['task_id']) +
                            r'/diagnostics/' + str(state['diagnostic_id']) + r'/analysis(?:[?#].*)?', url))


def configure(args, activity, state, directory):
    """Freeze the course allowlist before START; resumes use the saved policy."""
    if state.get('diagnostic_policy'):
        return
    course_id = activity.get('course_id') or getattr(args, 'diagnostic_course_id', None)
    if not isinstance(course_id, int) or course_id < 1:
        raise ValueError('Diagnostic needs the enrolled course ID or --diagnostic-course-id')
    source = getattr(args, 'diagnostic_topics', None)
    if source is None:
        name = activity.get('course_name') or activity.get('title', '').split(':')[0]
        slug = re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')
        candidates = [p for p in (args.ma_root/'COURSES/Math-Academy').rglob('Topics.csv')
                      if p.parent.name.lower() == 'graph-' + slug]
        if len(candidates) != 1:
            raise ValueError('Diagnostic course graph not found uniquely; supply --diagnostic-topics Topics.csv')
        source = candidates[0]
    source = Path(source).resolve()
    if source.is_dir():
        source /= 'Topics.csv'
    topics = [{'topic_id':int(r['topic-id']), 'title':r['topic-name']}
              for r in csv.DictReader(source.read_text().splitlines())]
    if not topics or any(t['topic_id'] < 1 or not t['title'] for t in topics) or len({t['topic_id'] for t in topics}) != len(topics):
        raise ValueError('Diagnostic topic list is empty or contains invalid/duplicate topics')
    state.update(course_id=course_id, answer_policy='correct_prerequisites_skip_course',
                 diagnostic_policy={'course_id':course_id, 'topics':topics, 'source':str(source),
                                    'sha256':hashlib.sha256(source.read_bytes()).hexdigest()},
                 progress_course_ids=(args.progress_course_ids if getattr(args,'progress_course_ids_explicit',False)
                                      else [course_id]))
    if getattr(args,'progress_urls',None):state['progress_urls']=args.progress_urls
    Path(directory).mkdir(parents=True, exist_ok=True)
    (Path(directory)/'diagnostic-Topics.csv').write_bytes(source.read_bytes())
    atomic_json(Path(directory)/'diagnostic-policy.json', state['diagnostic_policy'])
    atomic_json(Path(directory)/'state.json', state)


def classify(policy, decision, known_topic_id=None):
    ids = {t['topic_id'] for t in policy['topics']}
    if known_topic_id is not None:
        return 'in_course' if known_topic_id in ids else 'prerequisite'
    kind, tid = decision.get('diagnostic_classification'), decision.get('diagnostic_topic_id')
    if kind == 'in_course' and type(tid) is int and tid in ids:
        return kind
    if kind == 'prerequisite' and tid is None:
        return kind
    raise ValueError('Diagnostic classification must identify a supplied course topic or a prerequisite')


def source_topic(reader, mid, directory):
    db = getattr(reader, 'database', None)
    if db is None or mid is None:
        return None
    try:
        rows = db.query('''[:find ?id :in $ ?source :where
          [?q :question/math-academy-id ?source] [?kp :knowledge-point/questions ?q]
          [?t :topic/knowledge-points ?kp] [?t :topic/math-academy-id ?id]]''',
                        [mid], Path(directory)/'selection', 'diagnostic-'+mid)
        ids = {row[0] for row in rows}
        return next(iter(ids)) if len(ids) == 1 else None
    except Exception as error:
        logging.warning('Diagnostic question binding unavailable; using course skill classification: %s', error)
        return None


def finish(reader, state, directory):
    if not completed_url(state, reader.page.url):
        raise ValueError('Diagnostic completion must come from this exam’s analysis page')
    reader.page.locator('.courseFrame').first.wait_for(state='visible')
    (Path(directory)/'diagnostic-completed.html').write_text(reader.page.content())
    reader.page.screenshot(path=str(Path(directory)/'diagnostic-completed.png'))
    state.update(activity_complete=True, diagnostic_complete=True,
                 completion='Diagnostic completed: ' + reader.page.url,
                 diagnostic_completion_url=reader.page.url,
                 diagnostic_question_count=len(state['questions']))
    state.pop('diagnostic_pending_next', None)
    atomic_json(Path(directory)/'state.json', state)
    reader.knowledge_snapshot(state, directory, 'diagnostic-completed')


def wait_changed(reader, number):
    reader.page.wait_for_function('old => {const v=(' + VIEW + ')(); return '
                                 '/\/diagnostics\/\d+\/analysis(?:[?#]|$)/.test(v.url) || '
                                 'v.retry || (v.ready && v.number !== old);}', arg=number)


def take_diagnostic(reader, state, directory):
    """Retry observations in place; never reload a timed question to resolve a click."""
    from playwright.sync_api import TimeoutError
    directory = Path(directory)
    for attempt in range(3):
        try:
            return _take_diagnostic(reader, state, directory)
        except TimeoutError:
            reader.check()
            state['diagnostic_observation_retries'] = state.get('diagnostic_observation_retries', 0) + 1
            atomic_json(directory/'state.json', state)
            if attempt == 2:
                raise  # Retain the checkpoint for the batch's existing bounded recovery.
            reader.pacer.backoff(attempt + 1)


def _take_diagnostic(reader, state, directory):
    from browser import by_id, same_question_problem
    from solver import Solver
    page = reader.page
    save = lambda: atomic_json(directory/'state.json', state)
    if state.get('activity_complete'):
        if 'diagnostic-completed' not in state.get('knowledge_snapshots', {}):
            reader.knowledge_snapshot(state, directory, 'diagnostic-completed', recovered=True)
        return
    while True:
        reader.check()
        if completed_url(state, page.url):
            return finish(reader, state, directory)
        page.wait_for_function('() => {const v=(' + VIEW + ')(); return v.instructions || v.retry || v.ready || '
                               '/\/diagnostics\/\d+\/analysis(?:[?#]|$)/.test(v.url);}')
        view = page.evaluate(VIEW)
        if completed_url(state, view['url']):
            continue
        if view['instructions']:
            (directory/'diagnostic-instructions.html').write_text(page.locator('#initialScreen').evaluate('e=>e.outerHTML'))
            state['diagnostic_start_intent'] = True
            save()
            by_id(page, 'initialScreen-startButton').click()
            page.wait_for_function('() => !(' + VIEW + ')().instructions')
            state['diagnostic_started'] = True
            state.pop('diagnostic_start_intent', None)
            save()
            continue
        if view['retry']:
            # Deliberate skips move on. A real prerequisite mistake gets one
            # immediate same-topic retry, without starting a new solver session.
            record = list(state['questions'].values())[-1] if state['questions'] else {}
            retry = record.get('classification') == 'prerequisite' and not state.get('diagnostic_retry_active')
            record['diagnostic_retry_taken'] = bool(retry)
            state['diagnostic_retry_active'] = bool(retry)
            state['diagnostic_pending_next'] = record.get('sequence_position')
            save()
            by_id(page, 'retryScreen-yesButton' if retry else 'retryScreen-noButton').click()
            # The overlay hides before the asynchronous question arrives.
            # Wait for that question, keeping Next's intent through the wait.
            page.wait_for_function('old => {const v=(' + VIEW + ')(); return '
                                   '/\/analysis(?:[?#]|$)/.test(v.url) || '
                                   '(!v.retry && v.ready && v.number !== old);}',
                                   arg=record.get('sequence_position'))
            state.pop('diagnostic_pending_next', None)
            save()
            continue
        number = view['number']
        if not number:
            raise ValueError('Diagnostic has no recognized current question')
        slot = 'question-' + str(number).zfill(3)
        record = state['questions'].get(slot)
        scope = by_id(page, 'questionContainer')
        if state.get('diagnostic_pending_next') == number and not state.get('diagnostic_restored'):
            wait_changed(reader, number)
            continue
        if state.get('diagnostic_pending_next') != number:
            state.pop('diagnostic_pending_next', None)
        if record is None:
            if view['result']:
                raise ValueError('Restored diagnostic grade has no saved live question: '+slot)
            item, screenshot = reader.read(scope, directory, slot+'-before')
            if not item['problem'] or not item['fields']:
                raise ValueError('Diagnostic question is missing rendered problem or fields')
            record = {'before':item, 'screenshot':str(screenshot), 'status':'captured',
                      'sequence_position':number, 'solver_directory':slot,
                      'source_question_id':view['source_question_id']}
            state['questions'][slot] = record
            state['diagnostic_started'] = True
            save()
        if view['result']:
            state.pop('diagnostic_restored', None)
            if view['result'] not in ('Correct', 'Incorrect', 'Skipped Question'):
                raise ValueError('Unrecognized diagnostic grade: '+view['result'])
            if record.get('status') != 'graded':
                page.locator('#nextButton:visible, #doneButton:visible').first.wait_for(state='visible')
                item, _ = reader.read(scope, directory, slot+'-after')
                record.update(after=item, actual_result=item['result'], live_result=item['result'], status='graded')
                if item['result'] == 'Correct':
                    state.pop('diagnostic_retry_active', None)
                save()
                logging.info('Diagnostic question %s: %s (%s)', number, item['result'], record.get('classification'))
            state['diagnostic_pending_next'] = number
            save()
            by_id(page, 'doneButton' if view['done'] else 'nextButton').click()
            wait_changed(reader, number)
            if not page.evaluate(VIEW)['retry']:
                state.pop('diagnostic_retry_active', None)
            state.pop('diagnostic_pending_next', None)
            save()
            continue
        if record.get('status') == 'submitting' and not state.get('diagnostic_restored'):
            page.wait_for_function('() => {const v=(' + VIEW + ')(); return !!v.result || v.retry || '
                                   '/\/analysis(?:[?#]|$)/.test(v.url);}')
            continue
        if state.pop('diagnostic_restored', False):
            # Fresh server navigation restored an unanswered question. Saved
            # answers can be re-entered even when the old checkpoint says submit.
            item, screenshot = reader.read(scope, directory, slot+'-restored')
            if not same_question_problem(record['before'], item):
                raise ValueError('Restored diagnostic problem differs from saved live capture')
            record.setdefault('original_before', record['before'])
            record['before'] = item
            record['screenshot'] = str(screenshot)
            if record.get('decision', {}).get('answers'):
                record['decision'] = Solver.reuse_answer(item, record['decision'])
            record['status'] = 'captured'
            save()
        if 'decision' not in record:
            source = record.get('source_question_id')
            tid = source_topic(reader, 'q-'+str(source) if source else None, directory)
            record['bound_topic_id'] = tid
            if tid is not None and classify(state['diagnostic_policy'], {}, tid) == 'in_course':
                decision = {'confident':True, 'answers':[], 'explanation':'Existing source question belongs to the requested course.'}
            else:
                item = dict(record['before'])
                if tid is None:
                    item['diagnostic_policy'] = state['diagnostic_policy']
                decision = reader.solver.solve(item, Path(record['screenshot']), directory/slot,
                                               'diagnostic' if tid is None else 'solve')
            record['classification'] = classify(state['diagnostic_policy'], decision, tid)
            record['decision'] = decision
            record['intended'] = 'C' if record['classification'] == 'prerequisite' else 'skip'
            save()
        reader.pacer.wait('answer', 'diagnostic answer', elapsed=0)
        if record['classification'] == 'prerequisite':
            reader.enter(scope, record)
            reader.verify_entered(scope, record)
        record['status'] = 'submitting'
        save()
        journal(directory/'events.jsonl', 'diagnostic_submission_intent', question=slot, intended=record['intended'])
        scope.locator('.questionWidget-skipButton' if record['classification'] == 'in_course' else
                      '.questionWidget-submitButton').click()
        page.wait_for_function('() => !!(' + VIEW + ')().result')


def bind_history(state, metadata):
    """History supplies IDs even for blanks; match the durable numbered live slots."""
    numbered = {int(q['question_number'].rstrip('.')):q for q in metadata}
    records = state['questions']
    if len(numbered) != len(metadata) or len(metadata) != len(records):
        raise ValueError('Diagnostic history does not match the captured adaptive question count')
    bound = {}
    for key, record in records.items():
        q = numbered.get(record['sequence_position'])
        if not q:
            raise ValueError('Diagnostic history is missing a captured question position')
        mid = q['id'].replace('question-', 'q-')
        source_id = int(mid[2:])
        if record.get('source_question_id') not in (None, source_id):
            raise ValueError('Diagnostic history question identity differs from live capture')
        if mid in bound:
            raise ValueError('Diagnostic history has duplicate question identities')
        record['source_question_id'] = source_id
        record.setdefault('solver_directory', key)
        record['live_result'] = record.get('live_result', record.get('actual_result'))
        source = re.fullmatch(r'/topics/(\d+)#(\d+)', q['kp_href'] or '')
        if not source:
            raise ValueError('Diagnostic history lacks an authentic source topic/KP')
        record['history_classification'] = classify(state['diagnostic_policy'], {}, int(source[1]))
        bound[mid] = record
    state['questions'] = dict(sorted(bound.items(), key=lambda pair:pair[1]['sequence_position']))
    state['diagnostic_question_order'] = list(state['questions'])
