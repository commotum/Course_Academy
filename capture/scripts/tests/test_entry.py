"""Dropdown regressions use captured markup and local event handlers only."""
from pathlib import Path
import unittest

from scripts.browser.entry import click_dropdown, enter, verify_entered

FIXTURES = Path(__file__).parent / 'fixtures'


class CustomSelectTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from playwright.sync_api import sync_playwright
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch(headless=True)

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.playwright.stop()

    def setUp(self):
        self.context = self.browser.new_context()
        self.context.route('**/*', lambda route: route.abort())
        self.page = self.context.new_page()
        self.page.set_default_timeout(2000)
        self.addCleanup(self.context.close)

    def field(self, choices):
        return {'key': 'field-1', 'type': 'select', 'tag': 'custom-select',
                'dom_id': 'selectList-184106-0', 'choices': choices}

    def test_captured_hidden_mathjax_option_matches_visible_selected_frame(self):
        self.page.set_content((FIXTURES / 'custom-select-parity.html').read_text())
        field = self.field([{'option': str(index), 'type': 'math', 'value': value}
                            for index, value in enumerate(['3p+7', '3p-7', '3p-14'])])
        hidden = self.page.locator('.selectListOption').nth(1).inner_text().strip()
        self.assertEqual(hidden, '')
        result = enter(self.page.locator('#question'), field, {'value': '3p-7'})
        self.assertEqual(result['option'], '1')
        self.assertEqual(self.page.locator('.selectListOption.selected').count(), 1)
        self.assertNotEqual(self.page.locator('.selectListFrame').inner_text().strip(), hidden)
        # Retry an already-selected unsubmitted field with the same retained menu.
        self.assertEqual(enter(self.page.locator('#question'), field, {'value': '3p-7'})['option'], '1')

    def test_frame_is_scrolled_before_finding_a_direct_mouse_target(self):
        self.page.set_content('''<div style="height:1600px"></div><div id="question">
          <div id="selectList-184106-0" class="selectList">
            <div class="selectListFrame" style="position:relative;width:100px;height:32px;padding:5px;border:1px solid black">
              <span style="position:absolute;inset:5px">Choose</span>
            </div><div class="selectListOptions" style="visibility:hidden">
              <div class="selectListOption" style="height:25px">One</div>
            </div>
          </div></div><script>
          const frame=document.querySelector('.selectListFrame'), menu=document.querySelector('.selectListOptions');
          frame.onmousedown=()=>{menu.style.visibility='visible';};
          window.addEventListener('mousedown',event=>{
            if(event.target!==frame && !menu.contains(event.target))menu.style.visibility='hidden';
          });
          menu.firstElementChild.onclick=()=>{frame.textContent='One';menu.style.visibility='hidden';};
          </script>''')
        result = enter(self.page.locator('#question'), self.field([
            {'option': '0', 'type': 'text', 'value': 'One'}]), {'value': 'One'})
        self.assertEqual(result['value'], 'One')

    def test_option_click_uses_exposed_edge_when_center_is_covered(self):
        self.page.set_content('''<div id="option" style="position:relative;width:100px;height:40px"
          onclick="window.chosen=true">One</div><div style="position:absolute;left:18px;top:8px;width:80px;height:40px;z-index:10">Toolbox</div>''')
        click_dropdown(self.page.locator('#option'))
        self.assertTrue(self.page.evaluate('window.chosen'))

    def test_settled_custom_select_verifies_even_with_menu_outside_question(self):
        self.page.set_content((FIXTURES / 'custom-select-parity.html').read_text())
        field = self.field([{'option': str(index), 'type': 'math', 'value': value}
                            for index, value in enumerate(['3p+7', '3p-7', '3p-14'])])
        scope = self.page.locator('#question')
        entered = enter(scope, field, {'value': '3p-7'})
        self.page.evaluate("document.body.appendChild(document.querySelector('.selectListOptions'))")
        self.assertEqual(verify_entered(scope, {'fields': [field]}, [entered]), [entered])
        self.page.evaluate("document.querySelector('.selectListFrame').innerHTML=document.querySelector('.selectListOption').innerHTML")
        with self.assertRaisesRegex(ValueError, 'readback differs before submission'):
            verify_entered(scope, {'fields': [field]}, [entered])

    def test_settled_mathquill_rejects_sanitization_and_unfinished_commands(self):
        self.page.set_content('''<div id="question"><div class="matheditor-wrapper-answer"><span class="mq-editable-field"></span></div></div>
          <script>window.value='2';window.MathQuill=()=>({latex(){return window.value;}});</script>''')
        question = {'fields': [{'key': 'field-1', 'type': 'blank', 'tag': 'mathquill'}]}
        answers = [{'key': 'field-1', 'value': '2'}]
        scope = self.page.locator('#question')
        verify_entered(scope, question, answers)
        self.page.evaluate("window.value='3'")
        with self.assertRaisesRegex(ValueError, 'Math editor value changed'):
            verify_entered(scope, question, answers)
        self.page.evaluate("window.value='2';document.querySelector('.mq-editable-field').innerHTML='<span class=\"mq-latex-command-input\"></span>'")
        with self.assertRaisesRegex(ValueError, 'Unfinished MathQuill command'):
            verify_entered(scope, question, answers)

    def test_settled_radio_detects_selection_cleared_after_entry(self):
        self.page.set_content('''<div id="question"><span id="choice" class="choiceLetterCircle selectedChoice">A</span></div>''')
        question = {'fields': [{'key': 'field-1', 'type': 'radio', 'choices': [
            {'option': 'A', 'value': 'One', 'type': 'text', 'dom_id': 'choice'}]}]}
        answers = [{'key': 'field-1', 'value': 'One'}]
        scope = self.page.locator('#question')
        verify_entered(scope, question, answers)
        self.page.evaluate("document.querySelector('#choice').classList.remove('selectedChoice')")
        with self.assertRaisesRegex(ValueError, 'Radio selection changed'):
            verify_entered(scope, question, answers)

    def set_wrong_frame(self, expected, wrong):
        self.page.set_content('<div id="question"><div id="selectList-184106-0" class="selectList">'
            '<div class="selectListFrame" style="border:1px solid black;padding:8px">Choose</div>'
            '<div class="selectListOptions" style="visibility:hidden"><div class="selectListOption">'
            + expected + '</div></div></div></div>')
        self.page.evaluate('''wrong=>{
          const frame=document.querySelector('.selectListFrame'), menu=document.querySelector('.selectListOptions');
          frame.onclick=()=>{menu.style.visibility='visible';};
          menu.firstElementChild.onclick=()=>{frame.innerHTML=wrong;menu.firstElementChild.classList.add('selected');menu.style.visibility='hidden';};
        }''', wrong)

    def test_wrong_image_selection_does_not_pass_because_both_text_values_are_empty(self):
        self.set_wrong_frame('<img src="https://example.invalid/a.png" width="20" height="20">',
                             '<img src="https://example.invalid/b.png" width="20" height="20">')
        with self.assertRaisesRegex(ValueError, 'readback differs'):
            enter(self.page.locator('#question'), self.field([
                {'option': '0', 'type': 'image', 'value': 'a.png'}]), {'value': 'a.png'})

    def test_wrong_math_structure_does_not_pass_with_equal_flattened_text(self):
        self.set_wrong_frame('<math><msup><mi>x</mi><mn>2</mn></msup></math>',
                             '<math><mi>x</mi><mn>2</mn></math>')
        with self.assertRaisesRegex(ValueError, 'readback differs'):
            enter(self.page.locator('#question'), self.field([
                {'option': '0', 'type': 'math', 'value': 'x^2'}]), {'value': 'x^2'})


if __name__ == '__main__':
    unittest.main()
