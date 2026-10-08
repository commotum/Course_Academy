"""Replay the authentic skipped dropdown question and its submitting checkpoint."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock

from browser import CaptureBrowser, EXTRACT
from capture import arguments
from core import Pacer, atomic_json
from diagnostic import take_diagnostic, recover_saved_grades

FIXTURES=Path(__file__).parent/'fixtures'
BEFORE=(FIXTURES/'diagnostic-skipped-select-before.html').read_text()
AFTER=(FIXTURES/'diagnostic-skipped-select-after.html').read_text()


class SkippedSelectTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from playwright.sync_api import sync_playwright
        cls.runtime=sync_playwright().start();cls.browser=cls.runtime.chromium.launch(headless=True)

    @classmethod
    def tearDownClass(cls):
        cls.browser.close();cls.runtime.stop()

    def setUp(self):
        self.context=self.browser.new_context(offline=True);self.page=self.context.new_page()
        self.page.set_default_timeout(2000)

    def tearDown(self):self.context.close()

    def test_skipped_select_preserves_ids_choices_and_solution(self):
        self.page.set_content(BEFORE)
        before=self.page.locator('#questionContainer').evaluate(EXTRACT)
        self.page.set_content(AFTER)
        after=self.page.locator('#questionContainer').evaluate(EXTRACT)
        self.assertEqual(after['errors'],[])
        self.assertEqual(after['result'],'Skipped Question')
        self.assertTrue(after['worked_solution'])
        self.assertEqual(len(after['fields']),2)
        for first,last in zip(before['fields'],after['fields']):
            self.assertEqual(first['key'],last['key'])
            self.assertEqual(first['frame_id'],last['frame_id'])
            self.assertEqual([c['value'] for c in first['choices']],[c['value'] for c in last['choices']])
            self.assertTrue(last['choices_complete'])

    def test_disabled_controls_still_require_a_grade_and_real_frame_ids(self):
        self.page.set_content(AFTER)
        self.page.locator('.questionWidget-result').evaluate('n=>n.textContent=""')
        self.assertEqual(len(self.page.locator('#questionContainer').evaluate(EXTRACT)['errors']),2)
        self.page.set_content(AFTER)
        self.page.locator('.selectListFrameDisabled').evaluate_all('nodes=>nodes.forEach(n=>n.removeAttribute("id"))')
        self.assertEqual(len(self.page.locator('#questionContainer').evaluate(EXTRACT)['errors']),2)

    def test_skipped_readonly_textbox_is_preserved_as_an_answer_field(self):
        self.page.set_content('<div id="questionContainer"><div class="questionWidget-text">Find x: '
            '<div class="freeResponseTextbox" id="answer-1">?</div></div>'
            '<div class="questionWidget-result">Skipped Question</div>'
            '<div class="questionWidget-explanation">The solution is x=2.</div></div>')
        item=self.page.locator('#questionContainer').evaluate(EXTRACT)
        self.assertEqual(item['errors'],[])
        self.assertEqual(len(item['fields']),1)
        self.assertEqual(item['fields'][0]['dom_id'],'answer-1')

    def test_submitting_checkpoint_recovers_skip_without_another_submission(self):
        self.page.set_content(BEFORE)
        before=self.page.locator('#questionContainer').evaluate(EXTRACT)
        url='https://mathacademy.com/tasks/1/diagnostics/2';requests=[]
        def respond(route):
            if route.request.resource_type=='image':
                route.fulfill(status=204,body='');return
            path=route.request.url
            requests.append(path)
            if path==url+'/analysis':body='<div class="courseFrame">Diagnostic complete</div>'
            else:
                body=AFTER+'<button id="nextButton">Next</button><script>'
                body+='document.querySelector("#nextButton").onclick=()=>location.href='+repr(url+'/analysis')+';'
                body+='document.querySelector(".questionWidget-skipButton").onclick=()=>fetch("/unexpected-submit");</script>'
            route.fulfill(content_type='text/html; charset=utf-8',body=body)
        self.context.route('**/*',respond)
        args=arguments(['run','--timeout-ms','2000','--settle-ms','0','--event-min','0','--event-max','0',
                        '--answer-min','0','--answer-max','0'])
        solver=Mock();reader=CaptureBrowser(self.page,args,Pacer(args,sleeper=lambda _:None),solver)
        reader.knowledge_snapshot=Mock()
        state={'task_id':1,'diagnostic_id':2,'task_type':'diagnostic','diagnostic_started':True,
               'diagnostic_restored':True,'questions':{'question-011':{'before':before,'status':'submitting',
               'classification':'in_course','sequence_position':11,'intended':'skip','decision':{'answers':[]}}}}
        with tempfile.TemporaryDirectory() as work:
            atomic_json(Path(work)/'state.json',state)
            reader.navigate(url);take_diagnostic(reader,state,work)
            saved=state['questions']['question-011']
            self.assertEqual(saved['actual_result'],'Skipped Question')
            self.assertEqual(saved['status'],'graded')
            self.assertTrue(saved['after']['worked_solution'])
            self.assertTrue((Path(work)/'question-011-after.json').is_file())
            self.assertTrue(state['diagnostic_complete'])
        self.assertEqual(requests,[url,url+'/analysis'])
        solver.solve.assert_not_called()
        reader.knowledge_snapshot.assert_called_once()

    def test_saved_skip_recovers_when_reopening_has_advanced_to_next_question(self):
        self.page.set_content(BEFORE)
        before=self.page.locator('#questionContainer').evaluate(EXTRACT)
        self.page.set_content(AFTER)
        after=self.page.locator('#questionContainer').evaluate(EXTRACT)
        after['fields'][0]['frame_id']=None
        after['errors']=['Select frame has no ID']
        state={'questions':{'question-011':{'before':before,'status':'submitting','sequence_position':11}}}
        reader=Mock(page=self.page)
        with tempfile.TemporaryDirectory() as work:
            path=Path(work)/'question-011-after.json'
            atomic_json(path,after)
            self.assertEqual(recover_saved_grades(reader,state,work,advanced_past=11),0)
            self.assertEqual(recover_saved_grades(reader,state,work,advanced_past=12),1)
            record=state['questions']['question-011']
            self.assertEqual(record['live_result'],'Skipped Question')
            self.assertEqual(record['after']['errors'],[])
            self.assertEqual(len(record['after']['fields']),2)
            self.assertTrue(record['after']['fields'][0]['frame_id'])
            self.assertTrue(path.with_name('question-011-after-original.json').exists())
            self.assertEqual(recover_saved_grades(reader,state,work,advanced_past=12),0)
        reader.solver.solve.assert_not_called()


if __name__=='__main__':unittest.main()
