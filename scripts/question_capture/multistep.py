"""Ordered multipart activities with shared context and per-part submission checkpoints."""
import logging
import re
import time
from pathlib import Path

from core import atomic_json, journal, normalize


def dismiss_math_toolboxes(page, scope):
    # Native blur invokes the editor's normal toolbox dismissal handler.
    scope.locator('.mq-textarea textarea').evaluate_all('(editors) => editors.forEach(e => e.blur())')
    page.wait_for_function('''() => [...document.querySelectorAll('[id="mathEditorToolbox"]')].every(e =>
      !e.getClientRects().length || ['hidden','collapse'].includes(getComputedStyle(e).visibility))''')


def restore_empty_multistep(reader, scope, submit, continuation, record, directory, mid):
    if (record.get('status') != 'submitting' or record.get('actual_result') or
            record.get('after', {}).get('result') or continuation.is_visible() or
            not submit.is_visible() or 'disabledButton' not in (submit.get_attribute('class') or '')):
        return False
    fields = record['before']['fields']
    if not fields or not all(f.get('tag') == 'mathquill' for f in fields):
        return False
    empty = scope.evaluate('''q => {
      const visible=e=>!!e?.getClientRects().length && getComputedStyle(e).visibility!=='hidden';
      if(!visible(q) || q.querySelector('.answer, .correctAnswerText, .incorrectAnswerText')) return false;
      if([...q.closest('.step').querySelectorAll('.spinner')].some(visible)) return false;
      const library=window.MathQuill;
      if(!library) return false;
      const MQ=library.getInterface ? library.getInterface(2) : library;
      const editors=[...q.querySelectorAll('.mq-editable-field')];
      return editors.length>0 && editors.every(n=>visible(n) && MQ(n)?.latex()==='');
    }''')
    if not empty:
        return False
    fresh, _ = reader.read(scope, directory, mid + '-recovery')
    if (fresh.get('errors') or fresh.get('result') or
            normalize(fresh['problem']) != normalize(record['local_problem']) or
            [(f['key'], f.get('tag')) for f in fresh['fields']] !=
            [(f['key'], f.get('tag')) for f in fields]):
        return False
    record.setdefault('submission_recoveries', []).append(
        {'reason':'server_restored_empty_multistep', 'time':time.time()})
    record['status'] = 'prepared'
    return True


def with_context(state, item, mid):
    """Keep imported parts understandable without the surrounding Math Academy page."""
    sections = [c['problem'] for c in state.get('shared_contexts', [])]
    for previous in state.get('multistep_question_order', []):
        if previous == mid:
            break
        record = state['questions'].get(previous)
        if (not record or record.get('actual_result') not in ('Correct', 'Incorrect') or
                (record.get('actual_result') == 'Incorrect' and not record.get('verification'))):
            raise ValueError('Multistep preceding part has no recovered correct answer: ' + previous)
        solved = record['local_problem']
        for answer in record['decision']['answers']:
            value = answer['correct_value']
            formatted = ('$' + value + '$' if answer['value_type'] == 'math' else
                         '![](' + value + ')' if answer['value_type'] == 'image' else value)
            placeholder = '{{' + answer['key'] + '}}'
            if placeholder in solved:
                solved = solved.replace(placeholder, formatted)
            else:
                solved += '\n\nConfirmed answer (' + answer['key'] + '): ' + formatted
        sections.append('Earlier part ' + str(record['sequence_position']) + ':\n\n' + solved)
    sections.append('Current part:\n\n' + item['problem'])
    return {**item, 'problem': '\n\n'.join(sections)}


def take_multistep(reader, state, directory):
    from browser import by_id, LEARN
    from solver import Solver
    directory = Path(directory)
    save = lambda: atomic_json(directory / 'state.json', state)
    page = reader.page
    if state.get('activity_complete'):
        if 'multistep-completed' not in state.get('knowledge_snapshots', {}):
            reader.navigate(LEARN)
            reader.knowledge_snapshot(state, directory, 'multistep-completed', recovered=True)
        return
    state['answer_policy'] = 'all_correct'
    if not page.locator('#finalScreen').is_visible():
        page.locator('#steps > .step .question').first.wait_for(state='attached')
        layout = page.locator('#steps > .step').evaluate_all('''nodes => nodes.map(n => ({
          step:n.id,question:n.querySelector('.question')?.id || null}))''')
        parts = [p for p in layout if p['question']]
        first_question = next((i for i,p in enumerate(layout) if p['question']), len(layout))
        if any(not p['question'] for p in layout[first_question:]):
            raise ValueError('Unknown intervening multistep context layout; stop before answering')
        if (not parts or any(not re.fullmatch(r'step-\d+',p['step']) or
                            not re.fullmatch(r'question-\d+',p['question']) for p in parts)):
            raise ValueError('Unknown multistep layout; stop before answering')
        order = [p['question'].replace('question-', 'q-') for p in parts]
        if len(set(order)) != len(order) or state.get('multistep_question_order', order) != order:
            raise ValueError('Multistep question order changed on restoration')
        state['multistep_question_order'] = order
        if 'shared_contexts' not in state:
            contexts = []
            for part in layout:
                if part['question']:
                    break  # Only the initial shared setup belongs before every part.
                scope = by_id(page, part['step'])
                # Question markup arrives before Math Academy reveals its page.
                # Attachment alone cannot establish that shared setup is ready.
                scope.wait_for(state='visible')
                page.wait_for_function('''id => [...document.getElementById(id)
                  .querySelectorAll('mjx-container')].every(n=>!!n.querySelector('math, svg'))''',arg=part['step'])
                item, screenshot = reader.read(scope, directory, 'context-' + part['step'])
                if not item['problem'] or item['fields']:
                    raise ValueError('Shared multistep context is incomplete')
                contexts.append({**item, 'id':part['step'], 'screenshot':str(screenshot.resolve())})
            state['shared_contexts'] = contexts
        save()
        for position, part in enumerate(parts, 1):
            reader.check()
            mid = part['question'].replace('question-', 'q-')
            record = state['questions'].get(mid)
            scope = by_id(page,part['question'])
            scope.wait_for(state='visible')
            continuation = by_id(page,part['step'].replace('step-', 'continueButton-'))
            # A confirmed grade is never answered again after restarting.
            if record and record.get('status') == 'graded':
                if record.get('actual_result') not in ('Correct', 'Incorrect') or not record.get('after', {}).get('worked_solution'):
                    raise ValueError('Multistep prior grade needs inspection: ' + mid)
                restored_grade = scope.locator('.correctAnswerText, .incorrectAnswerText')
                if restored_grade.count() and restored_grade.inner_text().strip() != record['actual_result']:
                    item, screenshot = reader.read(scope, directory, mid + '-after')
                    record.setdefault('grade_reconciliations', []).append(
                        {'previous':record['actual_result'], 'observed':item['result'], 'time':time.time()})
                    record.update(after=item, actual_result=item['result'])
                    save()
                else:
                    item = record['after']
                    screenshot = directory / (mid + '-after.png')
            else:
                if not record:
                    if scope.locator('.answer').count():
                        raise ValueError('Served part was already answered without a saved live capture: ' + mid)
                    page.wait_for_function('''id => {
                      const q=document.getElementById(id);
                      return !!q.querySelector('.questionText')?.textContent.trim() &&
                        [...q.querySelectorAll('mjx-container')].every(n=>!!n.querySelector('math'));
                    }''', arg=part['question'])
                    local, screenshot = reader.read(scope, directory, mid + '-before')
                    if not local['problem'] or not local['fields']:
                        raise ValueError('Multistep problem or fields are missing: ' + mid)
                    item = with_context(state, local, mid)
                    started = time.monotonic()
                    decision = reader.solver.solve(item, screenshot, directory / mid)
                    record = {'before':item, 'local_problem':local['problem'], 'decision':decision,
                              'sequence_position':position, 'source_step':part['step'], 'intended':'C',
                              'status':'prepared', 'solver_elapsed_seconds':time.monotonic()-started}
                    state['questions'][mid] = record
                    save()
                if record['status'] == 'submitting':
                    restored_submit = by_id(page, part['step'].replace('step-', 'submitButton-'))
                    if restore_empty_multistep(reader, scope, restored_submit, continuation, record, directory, mid):
                        save()
                if record['status'] == 'prepared':
                    fresh, _ = reader.read(scope, directory, mid + '-before')
                    if normalize(fresh['problem']) != normalize(record['local_problem']):
                        raise ValueError('Restored multistep problem changed: ' + mid)
                    item = with_context(state, fresh, mid)
                    record['decision'] = Solver.reuse_answer(item, record['decision'])
                    record['before'] = item
                    save()
                    reader.enter(scope, record)
                    reader.pacer.wait('answer', 'before submitting a multistep part', elapsed=record['solver_elapsed_seconds'])
                    submit = by_id(page,part['step'].replace('step-', 'submitButton-'))
                    # MathEditor polls changes every 200ms. A symbol click can
                    # finish before the site's callback enables Submit.
                    from playwright.sync_api import expect
                    try:
                        expect(submit).not_to_have_class(re.compile(r'\bdisabledButton\b'),timeout=reader.args.timeout_ms)
                    except AssertionError as exc:
                        raise ValueError('Multistep Submit is disabled; stop before submitting') from exc
                    dismiss_math_toolboxes(page, scope)
                    # The editor may sanitize a value while updating the button.
                    # Verify after that update and blur, before recording submission intent.
                    try:
                        reader.verify_entered(scope, record)
                    finally:
                        save()
                    page.screenshot(path=str(directory / (mid + '-entered.png')))
                    if 'disabledButton' in (submit.get_attribute('class') or ''):
                        raise ValueError('Multistep Submit is disabled; stop before submitting')
                    reader.check()
                    record['status'] = 'submitting'
                    save()
                    journal(directory / 'events.jsonl', 'answer_submission_intent', question=mid, intended='C')
                    submit.click()
                # An interrupted submission is inspected, never clicked again.
                continuation.wait_for(state='visible')
                item, screenshot = reader.read(scope, directory, mid + '-after')
                record.update(after=item, actual_result=item['result'], status='graded')
                save()
            if item['result'] not in ('Correct', 'Incorrect') or not item['worked_solution']:
                raise ValueError('Multistep answer or explanation needs inspection: ' + mid)
            if item['result'] == 'Incorrect' and not record.get('verification'):
                from assessment import reconcile_graded_answer
                reconcile_graded_answer(reader, record, item, screenshot, directory, mid)
                save()
            logging.info('%s: %s, captured %d fields', mid, item['result'],
                         len(record.get('before', item).get('fields', [])))
            # Older parts remain visible but their Continue buttons disappear.
            if continuation.is_visible():
                state['pending_multistep_continue'] = part['step']
                save()
                reader.pacer.wait('event', 'advance multistep part')
                reader.check()
                continuation.click()
                continuation.wait_for(state='hidden')
            state.pop('pending_multistep_continue', None)
            save()
    final = by_id(page, 'finalScreen')
    final.wait_for(state='visible')
    completion = final.inner_text()
    order = state.get('multistep_question_order', [])
    if ('completed the task' not in completion.lower() or not order or
        set(order) != set(state['questions']) or any(
            q.get('status') != 'graded' or q.get('actual_result') not in ('Correct', 'Incorrect') or
            not q.get('after', {}).get('worked_solution') for q in state['questions'].values())):
        raise ValueError('Multistep completion has incomplete captured parts or an unexpected result')
    (directory / 'multistep-completed.html').write_text(page.content())
    page.screenshot(path=str(directory / 'multistep-completed.png'))
    state.update(completion=completion, activity_complete=True, multistep_complete=True)
    save()
    reader.pacer.wait('event', 'finish multistep')
    by_id(page,'finalScreen-doneButton').click()
    page.wait_for_url('**/learn')
    reader.knowledge_snapshot(state, directory, 'multistep-completed')
