"""Fixed-length assessments: capture live fields, then join graded history across topics."""
import json
import logging
import re
import time
from pathlib import Path

from core import atomic_json, assessment_can_start, compare_answers, journal, normalize


def choose_quiz_intent(rng, correct_weight):
    return 'C' if rng.random() < correct_weight else 'W'


def prepare_wrong_choice(record, rng):
    """Freeze one distinct displayed distractor before entry or interruption."""
    if record['intended'] != 'W':
        return
    field = record['before']['fields'][0]
    if field['type'] not in ('radio','select'):
        return  # The validated solver result already supplies wrong_value/keys.
    answer = next(a for a in record['decision']['answers'] if a['key'] == field['key'])
    choices = [c for c in field['choices'] if c['option'] != answer['correct_option'] and
               (c['type'] != answer['value_type'] or
                normalize(c['value'],c['type']) != normalize(answer['correct_value'],answer['value_type']))]
    if not choices:
        raise ValueError('Quiz question has no distinct incorrect choice')
    chosen = rng.choice(choices)
    record['wrong_choice'] = {'key':field['key'],'type':chosen['type'],'value':chosen['value']}


def begin_pacing(state, pacer):
    """Choose one durable schedule when starting a timed assessment."""
    if 'assessment_pacing' in state or state.get('assessment_started'):
        return  # Old in-progress captures retain their original timing policy.
    limit = state.get('assessment_details', {}).get('Time Limit', '')
    match = re.fullmatch(r'([1-9]\d*)\s+minutes?', limit, re.I)
    if not match or not pacer.args.assessment_time_max:
        return
    seconds = int(match[1]) * 60
    target = seconds * pacer.rng.uniform(pacer.args.assessment_time_min, pacer.args.assessment_time_max)
    weights = [pacer.rng.uniform(0.65, 1.35) for _ in range(state['assessment_question_count'])]
    total_weight = sum(weights)
    cumulative, offsets = 0, []
    for weight in weights:
        cumulative += weight
        offsets.append(target * cumulative / total_weight)
    state['assessment_pacing'] = {'started_at':time.time(), 'time_limit_seconds':seconds,
                                  'target_seconds':target, 'answer_offsets_seconds':offsets}
    logging.info('Assessment pacing target: %.1f minutes of %s', target / 60, limit)


def pace_before_answer(reader, state, index):
    """Credit real elapsed time, including solving and interruptions, before entry."""
    plan = state.get('assessment_pacing')
    if not plan:
        return
    due = plan['started_at'] + plan['answer_offsets_seconds'][index]
    reserve = max(15, min(60, plan['time_limit_seconds'] * 0.05))
    remaining_questions = state['assessment_question_count'] - index - 1
    while True:
        reader.check()
        check_request_error(reader.page)
        now = time.time()
        remaining = plan['started_at'] + plan['time_limit_seconds'] - now
        timer = reader.page.locator('#timeRemaining')
        if timer.is_visible():
            match = re.fullmatch(r'(\d+)\s+(minutes?|seconds?)\s+remaining', timer.inner_text().strip(), re.I)
            if match:
                # MA rounds displayed minutes up, so use their lower bound.
                displayed = max(0, int(match[1]) - 1) * 60 if match[2].lower().startswith('minute') else int(match[1])
                remaining = min(remaining, displayed)
        allowance = max(0, remaining - reserve - 15 * remaining_questions)
        delay = min(max(0, due - now), allowance)
        if not delay:
            return
        chunk = min(30, delay)
        logging.info('Waiting %.1fs (assessment question %d pacing; %.1fs elapsed)',
                     chunk, index + 1, max(0, now - plan['started_at']))
        # Short interruptible chunks keep shutdown responsive and recheck the
        # visible countdown without navigating or making a network request.
        reader.pacer.sleep(chunk)


def finish(reader, state, directory):
    from browser import by_id
    final = by_id(reader.page,'finalScreen')
    final.wait_for(state='visible')
    completion = final.inner_text()
    count = state.get('assessment_question_count')
    if not re.search(r'\bof\s+' + str(count) + r'\s+questions\b',completion,re.I):
        raise ValueError('Assessment ended with an unrecognized completion screen')
    if len(state['questions']) != count or not all(q.get('status') == 'filled' for q in state['questions'].values()):
        raise ValueError('Assessment ended before every live question was captured')
    (directory/'assessment-completed.html').write_text(final.evaluate('e => e.outerHTML'))
    reader.page.screenshot(path=str(directory/'assessment-completed.png'))
    state.update(completion=completion,activity_complete=True,assessment_complete=True,test_submission_status='completed')
    if state.get('assessment_pacing'):
        state['assessment_pacing']['actual_elapsed_seconds'] = max(0, time.time() - state['assessment_pacing']['started_at'])
    atomic_json(directory/'state.json',state)
    reader.pacer.wait('event','finish assessment')
    by_id(reader.page,'finalScreen-doneButton').click()
    reader.page.wait_for_url('**/learn')
    reader.knowledge_snapshot(state,directory,'assessment-completed')


class AssessmentRequestError(RuntimeError):
    pass


def request_error_message(page):
    message = page.locator('#messageBox-message')
    if not message.is_visible():
        return None
    text = ' '.join(message.inner_text().split())
    known = 'Oops, there was an error processing your request. Please check your internet connection.'
    return text if text == known else None


def check_request_error(page):
    if request_error_message(page):
        raise AssessmentRequestError('Math Academy displayed its request-processing error dialog')


def restore_assessment_intents(reader, state, directory):
    """Use a fresh server-rendered screen to resolve interrupted start/submit clicks."""
    pending_submit = state.get('test_submission_status') == 'confirming'
    pending_start = state.get('assessment_start_intent') and not state.get('assessment_started')
    if not (pending_submit or pending_start) or state.get('activity_complete'):
        return
    page = reader.page
    if page.locator('#finalScreen').is_visible():
        return  # _take_assessment captures this result without another submission.
    url = state.get('activity_url')
    if not url and state.get('task_id') and state.get('test_id'):
        from browser import LEARN
        url = LEARN.replace('/learn', '') + '/tasks/' + str(state['task_id']) + '/tests/' + str(state['test_id'])
        state['activity_url'] = url
    if not url:
        return
    reader.navigate(url, force=True)
    page.locator('#startButton:visible, #questions > .question:visible, #finalScreen:visible').first.wait_for(state='visible')
    if page.locator('#finalScreen').is_visible():
        return
    if pending_submit and page.locator('#questions > .question:visible').count():
        state.setdefault('assessment_intent_recoveries', []).append(
            {'intent':'submit', 'reason':'server_restored_unsubmitted_test', 'time':time.time()})
        state.pop('test_submission_status', None)
        logging.warning('Restored assessment remains unsubmitted; reusing its saved answers')
    if pending_start and page.locator('#startButton').is_visible():
        state.setdefault('assessment_intent_recoveries', []).append(
            {'intent':'start', 'reason':'server_restored_instruction_screen', 'time':time.time()})
        state.pop('assessment_start_intent', None)
        logging.warning('Restored assessment has not started; continuing from its instructions')
    atomic_json(Path(directory)/'state.json', state)


def take_assessment(reader, state, directory):
    """Recover request errors/timeouts without replaying completed submissions."""
    from playwright.sync_api import TimeoutError as PlaywrightTimeout
    directory = Path(directory)
    restore_assessment_intents(reader, state, directory)
    recoveries = 0  # Bound this burst, not all future resumptions of this assessment.
    while True:
        try:
            return _take_assessment(reader, state, directory)
        except (AssessmentRequestError, PlaywrightTimeout) as error:
            reader.check()
            message = request_error_message(reader.page)
            if reader.page.locator('#messageBox-message').is_visible() and not message:
                raise  # Unknown dialogs require inspection, not dismissal.
            if not message and not (state.get('assessment_started') or state.get('assessment_question_count')):
                raise
            if not state.get('activity_url'):
                raise
            if recoveries >= 2:
                raise AssessmentRequestError('Assessment could not recover in this retry burst; retaining it for automatic repair') from error
            recoveries += 1
            attempt = state.get('assessment_recovery_attempts', 0) + 1
            state['assessment_recovery_attempts'] = attempt
            state.setdefault('assessment_recovery_errors', []).append(
                {'attempt': attempt, 'message': message or str(error), 'time': time.time()})
            atomic_json(directory/'state.json',state)
            (directory/('request-error-'+str(attempt)+'.html')).write_text(reader.page.content())
            try:
                reader.page.screenshot(path=str(directory/('request-error-'+str(attempt)+'.png')),timeout=5000)
            except Exception:
                logging.warning('Assessment recovery screenshot unavailable')
            logging.warning('Restoring the same assessment (burst retry %d/2, total %d), retaining saved answers and timer',recoveries,attempt)
            if attempt > 2:
                reader.pacer.backoff(attempt - 2)
            if state.get('test_submission_status') == 'confirming':
                restore_assessment_intents(reader, state, directory)
            else:
                reader.navigate(state['activity_url'],force=True)


def _take_assessment(reader, state, directory):
    from browser import by_id, LEARN
    from solver import Solver
    directory = Path(directory)
    save = lambda:atomic_json(directory/'state.json',state)
    page = reader.page
    if state.get('activity_complete'):
        if 'assessment-completed' not in state.get('knowledge_snapshots',{}):
            reader.navigate(LEARN)
            reader.knowledge_snapshot(state,directory,'assessment-completed',recovered=True)
        return
    if page.locator('#finalScreen').is_visible():
        return finish(reader,state,directory)
    # Interrupted clicks are reconciled from a fresh server page by the wrapper.
    if state.get('test_submission_status') == 'confirming':
        raise ValueError('Assessment submission is unconfirmed; inspect its result before another submission')
    check_request_error(page)
    state.setdefault('assessment_correct_weight',reader.args.assessment_correct_weight)
    state['answer_policy'] = 'independent_weighted'
    # Navigation can finish before the instruction screen becomes visible.
    # Wait for either the START screen or the running/restored test before
    # deciding which path to take. An early is_visible() is not a layout signal.
    page.locator('#startButton:visible, #questions > .question:visible, #finalScreen:visible').first.wait_for(state='visible')
    if page.locator('#finalScreen').is_visible():
        return finish(reader,state,directory)
    if not state.get('assessment_started'):
        if not assessment_can_start(state):
            raise ValueError('Assessment is not eligible under its saved selection policy; stop before the timer starts')
        count = state.get('assessment_details',{}).get('Questions','')
        if not re.fullmatch(r'[1-9]\d*',count):
            raise ValueError('Assessment question count is missing; stop before the timer starts')
        state['assessment_question_count'] = int(count)
        if page.locator('#startButton').is_visible():
            if state.get('assessment_start_intent'):
                raise ValueError('Assessment start is unconfirmed; do not restart its timer')
            (directory/'assessment-instructions.html').write_text(page.locator('#screen').evaluate('e => e.outerHTML'))
            state['assessment_start_intent'] = True
            state['activity_url'] = LEARN.replace('/learn','') + '/tasks/' + str(state['task_id']) + '/tests/' + str(state['test_id'])
            save()
            reader.pacer.wait('event','start assessment timer')
            begin_pacing(state,reader.pacer)
            save()
            by_id(page,'startButton').click()
        page.locator('#questions > .question').first.wait_for(state='attached')
        state['assessment_started'] = True
        save()
    page.locator('#questions > .question').first.wait_for(state='attached')
    observed = page.locator('#questions > .question').evaluate_all('nodes => nodes.map(n => n.id)')
    if (len(observed) != state['assessment_question_count'] or len(set(observed)) != len(observed) or
        any(not re.fullmatch(r'question-\d+',qid) for qid in observed)):
        raise ValueError('Assessment question set does not match the saved queue count')
    order = state.setdefault('assessment_question_order',observed)
    if set(order) != set(observed):
        raise ValueError('Restored assessment served different question IDs')
    navigator = by_id(page,'questionNavigator').locator('.questionButton')
    # Questions attach before asynchronous free-response/MathJax initialization
    # finishes and renders the navigator. Wait for the complete expected set.
    from playwright.sync_api import expect
    try:
        expect(navigator).to_have_count(len(observed),timeout=reader.args.timeout_ms)
    except AssertionError as exc:
        raise ValueError('Unknown assessment navigation layout') from exc
    # Preserve initialized widgets for every question, including unvisited
    # ones, before pacing or navigation can fail.
    source = directory/'assessment-live.html'
    if not source.exists():
        source.write_text(page.content())
    save()
    for index, qid in enumerate(order):
        reader.check()
        check_request_error(page)
        scope = by_id(page,qid)
        if not scope.is_visible():
            reader.pacer.wait('event','navigate assessment question')
            check_request_error(page)
            navigator.nth(observed.index(qid)).click(timeout=min(reader.args.timeout_ms,5000))
            check_request_error(page)
        scope.wait_for(state='visible')
        page.wait_for_function('''id => {
          const q=document.getElementById(id);
          return !!q.querySelector('.questionText')?.textContent.trim() &&
            [...q.querySelectorAll('mjx-container')].every(n=>!!n.querySelector('math'));
        }''',arg=qid)
        mid = qid.replace('question-','q-')
        item, screenshot = reader.read(scope,directory,mid+'-before')
        if not item['problem'] or not item['fields']:
            raise ValueError('Assessment problem or fields are missing: '+mid)
        record = state['questions'].get(mid)
        if record is None:
            started = time.monotonic()
            decision = reader.solver.solve(item,screenshot,directory/mid)
            record = {'before':item,'decision':decision,
                      'intended':choose_quiz_intent(reader.pacer.rng,state['assessment_correct_weight']),
                      'status':'prepared',
                      'solver_elapsed_seconds':time.monotonic()-started}
            prepare_wrong_choice(record,reader.pacer.rng)
            state['questions'][mid] = record
            save()
        else:
            if normalize(item['problem']) != normalize(record['before']['problem']):
                raise ValueError('Restored assessment problem changed: '+mid)
            record['decision'] = Solver.reuse_answer(item,record['decision'])
            record['before'] = item
            save()
        # Filling/editing an unsubmitted test is repeatable. Final test submission
        # has a separate durable intent and is never blindly repeated.
        if record.get('status') != 'filled':
            pace_before_answer(reader,state,index)
        check_request_error(page)
        reader.enter(scope,record)
        try:
            reader.verify_entered(scope,record)
        finally:
            save()
        page.screenshot(path=str(directory/(mid+'-entered.png')))
        record['status'] = 'filled'
        save()
        logging.info('%s: assessment answer filled (intended %s); %d/%d questions captured',
                     mid,record['intended'],len(state['questions']),len(order))
    reader.check()
    check_request_error(page)
    (directory/'assessment-answered.html').write_text(page.content())
    reader.pacer.wait('answer','before submitting assessment',elapsed=sum(
        q.get('solver_elapsed_seconds',0) for q in state['questions'].values()))
    check_request_error(page)
    button = by_id(page,'submitTestButton')
    if 'disabledButton' in (button.get_attribute('class') or ''):
        raise ValueError('Assessment Submit Test remains disabled after filling answers')
    button.click()  # Opens the non-submitting confirmation dialog.
    dialog = by_id(page,'confirmationDialog')
    dialog.wait_for(state='visible')
    if not re.search(r'submit\s+this\s+test',dialog.inner_text(),re.I):
        raise ValueError('Unknown assessment confirmation; stop before confirming')
    state['test_submission_status'] = 'confirming'
    save()
    journal(directory/'events.jsonl','assessment_submission_intent',task_id=state['task_id'])
    reader.pacer.wait('event','confirm whole assessment submission')
    dialog.get_by_text('Yes',exact=True).click()
    return finish(reader,state,directory)


def assessment_history(reader, state, directory, load_topic):
    from browser import by_id, LEARN
    directory = Path(directory)
    is_multistep = state.get('task_type') == 'multistep'
    is_diagnostic = state.get('task_type') == 'diagnostic'
    reader.navigate(LEARN+'?taskId='+str(state['task_id']))
    selector = '.question[id^="question-"]'
    reader.page.locator(selector).first.wait_for(state='visible')
    metadata = reader.page.locator(selector).evaluate_all('''nodes => nodes.map(q => ({
      id:q.id,difficulty:q.querySelector('.questionDifficulty')?.textContent.trim(),
      kp_title:q.querySelector('.questionKP')?.textContent.trim(),
      kp_href:q.querySelector('.questionKP')?.getAttribute('href'),
      question_number:q.querySelector('.questionNumber')?.textContent.trim(),
      result:q.querySelector('.answerResult')?.textContent.trim(),raw_html:q.outerHTML,
      details_html:q.querySelector('.answerDetails')?.outerHTML}))''')
    for question in metadata:
        question['source_result'] = question['result']
    if is_diagnostic:
        from diagnostic import bind_history
        bind_history(state, metadata)
        atomic_json(directory/'state.json',state)
    ids = [q['id'].replace('question-','q-') for q in metadata]
    if len(set(ids)) != len(ids) or set(ids) != set(state['questions']):
        raise ValueError('Assessment activity IDs differ from the live capture')
    topics = {}
    for q in metadata:
        mid = q['id'].replace('question-','q-')
        source = re.fullmatch(r'/topics/(\d+)#(\d+)',q['kp_href'] or '')
        if not source or q['result'] not in ('Correct','Incorrect','No Credit'):
            raise ValueError('Assessment question has no source KP or grade: '+mid)
        tid = int(source[1])
        if tid not in topics:
            topics[tid] = load_topic(tid,directory/'selection/topics'/str(tid))
        points = [kp for kp in topics[tid][':topic/knowledge-points']
                  if kp[':knowledge-point/title'] == q['kp_title']]
        if len(points) != 1:
            raise ValueError('Assessment KP cannot be matched uniquely within its source topic: '+mid)
        difficulty = {'E':'easy','M':'moderate','H':'hard'}.get(q['difficulty'])
        if not difficulty:
            raise ValueError('Assessment question has no recognized difficulty: '+mid)
        explanation = by_id(reader.page,q['id'].replace('question-','questionExplanation-'))
        if not explanation.is_visible():
            reader.pacer.wait('event','expand assessment explanation')
            by_id(reader.page,q['id']).locator('.answerDetails').click()
        explanation.wait_for(state='visible')
        item, screenshot = reader.read(explanation,directory,'history-'+mid)
        if not item['worked_solution']:
            raise ValueError('Assessment explanation is missing: '+mid)
        record = state['questions'][mid]
        record.update(history=item,after=item,actual_result=q['result'])
        if (q['result'] in ('Incorrect','No Credit') or record.get('intended') == 'W') and not record.get('verification'):
            # Preserve the actual submitted value, but recover the correct value
            # from the revealed solution before producing database content.
            verified_item = {**record['before'],'worked_solution':item['worked_solution']}
            verified = reader.solver.solve(verified_item,screenshot,directory/record.get('solver_directory',mid),'verify')
            record.setdefault('predicted_answers', json.loads(json.dumps(record['decision']['answers'])))
            record['verification'] = verified
        if record.get('verification'):
            record['decision'] = record['verification']
        if q['result'] == 'Correct':
            answers = {a['key']:a for a in record['decision']['answers']}
            for field in record['before']['fields']:
                submitted = field.get('submitted_value')
                answer = answers[field['key']]
                if submitted is not None and compare_answers(submitted,answer['correct_value'],answer['value_type'],
                                                            prompt=record['before']['problem'])['outcome'] != 'equivalent':
                    reconcile_graded_answer(reader, record, item, screenshot, directory, mid)
                    break
        kp = {'id':str(points[0][':knowledge-point/id']),'title':q['kp_title']}
        record['kp_id'] = kp['id']
        record['content'] = reader.question_content(mid,record,kp)
        record['content'].update(topic_id=tid,difficulty=difficulty,knowledge_point_source_id=int(source[2]),
                                 provenance={'activity_question':q['id'],'kp_href':q['kp_href'],'kp_title':q['kp_title']})
        if is_multistep:
            record['content'].update(sequence_position=record['sequence_position'], local_problem=record['local_problem'],
                                     shared_context_refs=[c['id'] for c in state.get('shared_contexts', [])])
        if is_diagnostic:
            record['content'].update(sequence_position=record['sequence_position'],
                                     diagnostic_classification=record['classification'],
                                     diagnostic_history_classification=record['history_classification'],
                                     diagnostic_live_result=record.get('live_result'))
        record['finalized'] = True
        atomic_json(directory/'state.json',state)
    atomic_json(directory/'activity-metadata.json',metadata)
    content = {'task_id':state['task_id'],'task_type':state['task_type'],
               'topic_id':None,'content_only':True,'source_url':reader.page.url,
               'answer_policy':'all correct' if is_multistep else state.get('answer_policy','all correct'),
               'questions':[q['content'] for q in state['questions'].values()],'canonical_examples':[]}
    if is_multistep:
        content.update(multistep_id=state['multistep_id'],title=state.get('title'),
                       shared_contexts=state.get('shared_contexts', []), question_order=state['multistep_question_order'])
        content['questions'].sort(key=lambda q:q['sequence_position'])
    elif is_diagnostic:
        content.update(diagnostic_id=state['diagnostic_id'],course_id=state['course_id'],
                       question_order=state['diagnostic_question_order'],
                       diagnostic_policy=state['diagnostic_policy'])
        content['questions'].sort(key=lambda q:q['sequence_position'])
    else:
        content.update(test_id=state['test_id'],assessment_details=state['assessment_details'],
                       assessment_notice=state.get('assessment_notice'),optional_xp_remaining=state.get('optional_xp_remaining'),
                       assessment_is_retake=state.get('assessment_is_retake',False),
                       assessment_optional_fallback=state.get('assessment_optional_fallback',False),
                       assessment_correct_weight=state.get('assessment_correct_weight',1.0))
    atomic_json(directory/'content.json',content)
    state['history_complete'] = True
    atomic_json(directory/'state.json',state)
    return content


def reconcile_graded_answer(reader, record, item, screenshot, directory, mid):
    """Let the activity solver weigh the displayed solution against its actual grade."""
    previous = json.loads(json.dumps(record['decision']))
    evidence = {'actual_grade':record['actual_result'],
                'submitted_values':{f['key']:f.get('submitted_value') for f in record['before']['fields']},
                'previous_predicted_answers':previous['answers']}
    reviewed = {**record['before'], 'worked_solution':item['worked_solution'] +
                '\n\nCaptured grading evidence (separate from the worked solution):\n' +
                json.dumps(evidence, ensure_ascii=False)}
    decision = reader.solver.solve(reviewed, screenshot, Path(directory)/mid, 'reconcile-grade')
    record.setdefault('predicted_answers', previous['answers'])
    record.setdefault('answer_reconciliations', []).append(
        {**evidence, 'reviewed_answers':decision['answers'], 'reason':decision.get('explanation','')})
    record['verification'] = decision
    record['decision'] = decision
    logging.warning('%s: using the activity solver judgment for the grade/solution disagreement', mid)
