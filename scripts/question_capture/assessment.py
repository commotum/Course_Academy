"""Fixed-length assessments: capture live fields, then join graded history across topics."""
import json
import logging
import re
import time
from pathlib import Path

from core import atomic_json, journal, normalize


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
    atomic_json(directory/'state.json',state)
    reader.pacer.wait('event','finish assessment')
    by_id(reader.page,'finalScreen-doneButton').click()
    reader.page.wait_for_url('**/learn')
    reader.knowledge_snapshot(state,directory,'assessment-completed')


def take_assessment(reader, state, directory):
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
    # Confirmation sends the whole test. An uncertain final submission is read,
    # never replayed, even if restoring the page displays the old questions.
    if state.get('test_submission_status') == 'confirming':
        raise ValueError('Assessment submission is unconfirmed; inspect its result before another submission')
    if not state.get('assessment_started'):
        if state.get('assessment_requirement') != 'required':
            raise ValueError('Assessment requirement is unknown or optional; stop before the timer starts')
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
            reader.pacer.wait('event','start required assessment timer')
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
    if navigator.count() != len(observed):
        raise ValueError('Unknown assessment navigation layout')
    save()
    for qid in order:
        reader.check()
        scope = by_id(page,qid)
        if not scope.is_visible():
            reader.pacer.wait('event','navigate assessment question')
            navigator.nth(observed.index(qid)).click()
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
            record = {'before':item,'decision':decision,'intended':'C','status':'prepared',
                      'solver_elapsed_seconds':time.monotonic()-started}
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
        reader.enter(scope,record)
        try:
            reader.verify_entered(scope,record)
        finally:
            save()
        page.screenshot(path=str(directory/(mid+'-entered.png')))
        record['status'] = 'filled'
        save()
        logging.info('%s: assessment answer filled; %d/%d questions captured',mid,len(state['questions']),len(order))
    reader.check()
    (directory/'assessment-answered.html').write_text(page.content())
    reader.pacer.wait('answer','before submitting assessment',elapsed=sum(
        q.get('solver_elapsed_seconds',0) for q in state['questions'].values()))
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
    reader.navigate(LEARN+'?taskId='+str(state['task_id']))
    selector = '.question[id^="question-"]'
    reader.page.locator(selector).first.wait_for(state='visible')
    metadata = reader.page.locator(selector).evaluate_all('''nodes => nodes.map(q => ({
      id:q.id,difficulty:q.querySelector('.questionDifficulty')?.textContent.trim(),
      kp_title:q.querySelector('.questionKP')?.textContent.trim(),
      kp_href:q.querySelector('.questionKP')?.getAttribute('href'),
      result:q.querySelector('.answerResult')?.textContent.trim(),raw_html:q.outerHTML,
      details_html:q.querySelector('.answerDetails')?.outerHTML}))''')
    ids = [q['id'].replace('question-','q-') for q in metadata]
    if len(set(ids)) != len(ids) or set(ids) != set(state['questions']):
        raise ValueError('Assessment activity IDs differ from the live capture')
    topics = {}
    for q in metadata:
        mid = q['id'].replace('question-','q-')
        source = re.fullmatch(r'/topics/(\d+)#(\d+)',q['kp_href'] or '')
        if not source or q['result'] not in ('Correct','Incorrect'):
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
        if q['result'] == 'Incorrect' and not record.get('verification'):
            # Preserve the actual submitted value, but recover the correct value
            # from the revealed solution before producing database content.
            verified_item = {**record['before'],'worked_solution':item['worked_solution']}
            verified = reader.solver.solve(verified_item,screenshot,directory/mid,'verify')
            record['verification'] = verified
        if record.get('verification'):
            record['decision'] = record['verification']
        kp = {'id':str(points[0][':knowledge-point/id']),'title':q['kp_title']}
        record['kp_id'] = kp['id']
        record['content'] = reader.question_content(mid,record,kp)
        record['content'].update(topic_id=tid,difficulty=difficulty,knowledge_point_source_id=int(source[2]),
                                 provenance={'activity_question':q['id'],'kp_href':q['kp_href'],'kp_title':q['kp_title']})
        if is_multistep:
            record['content'].update(sequence_position=record['sequence_position'], local_problem=record['local_problem'],
                                     shared_context_refs=[c['id'] for c in state.get('shared_contexts', [])])
        record['finalized'] = True
        atomic_json(directory/'state.json',state)
    atomic_json(directory/'activity-metadata.json',metadata)
    content = {'task_id':state['task_id'],'task_type':state['task_type'],
               'topic_id':None,'content_only':True,'source_url':reader.page.url,
               'answer_policy':'all correct',
               'questions':[q['content'] for q in state['questions'].values()],'canonical_examples':[]}
    if is_multistep:
        if any(q['actual_result'] != 'Correct' for q in state['questions'].values()):
            raise ValueError('Multistep history conflicts with the saved correct grades')
        content.update(multistep_id=state['multistep_id'],title=state.get('title'),
                       shared_contexts=state.get('shared_contexts', []), question_order=state['multistep_question_order'])
        content['questions'].sort(key=lambda q:q['sequence_position'])
    else:
        content.update(test_id=state['test_id'],assessment_details=state['assessment_details'],
                       assessment_notice=state.get('assessment_notice'),optional_xp_remaining=state.get('optional_xp_remaining'))
    atomic_json(directory/'content.json',content)
    state['history_complete'] = True
    atomic_json(directory/'state.json',state)
    return content
