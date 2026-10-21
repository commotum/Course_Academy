"""Saved MA source fragments plus offline action/recovery tests.

Question/history: reference/mathacademy/question-capture/14085116.
Lesson: reference/edb-math/imports/math-academy/newer-captures/source-evidence/topic-3178.html.
Assessment: reference/mathacademy/question-capture-workers/linear/14097922.
Multistep: reference/mathacademy/question-capture/14039183.
Diagnostic/queue regressions: scripts/question_capture/fixtures.
"""
import hashlib
from copy import deepcopy
import json
import tempfile
import threading
import unittest
from pathlib import Path
from types import SimpleNamespace

from scripts.browser.adapter import EXTRACT, MathAcademyBrowser
from scripts.browser.assets import AssetCapture, image_extension, replace_markers, standalone_svg
from scripts.browser.entry import enter, normalized_math, pick_choice, validated_keys, write_math
from scripts.browser.parsing import (activity_from_url, parse_dashboard, parse_history_metadata, parse_lesson_structure,
                                    parse_queue, parse_xp, question_identity)

FIXTURES = Path(__file__).parent / "fixtures"


class SourceParsingTests(unittest.TestCase):
    def test_svg_html_entities_are_preserved_as_xml_character_references(self):
        import xml.etree.ElementTree as ET
        svg='<svg><foreignObject><div xmlns="http://www.w3.org/1999/xhtml">A&nbsp;B &amp; C &ThinSpace; D</div></foreignObject></svg>'
        data,_=standalone_svg(svg)
        root=ET.fromstring(data)
        self.assertIn('A\u00a0B & C \u2009 D',''.join(root.itertext()))
        with self.assertRaises(ET.ParseError):
            standalone_svg('<svg><text>&inventedEntity;</text></svg>')
    def test_laplace_prompt_and_option_share_bytes_but_keep_source_identity(self):
        captured = json.loads((FIXTURES / 'laplace-duplicate-images.json').read_text())
        raw = deepcopy(captured)
        raw['problem'] = raw['problem'].replace(captured['assets'][0]['path'], '@asset-0@')
        for index, choice in enumerate(raw['fields'][0]['choices'], 1):
            choice['value'] = f'@asset-{index}@'
        self.assertEqual(captured['assets'][0]['path'], captured['assets'][3]['path'])
        self.assertNotEqual(captured['assets'][0]['source_url'], captured['assets'][3]['source_url'])
        self.assertEqual(MathAcademyBrowser._binding(raw), MathAcademyBrowser._binding(captured))
        changed = deepcopy(raw)
        changed['assets'][3]['source_url'] = 'https://mathacademy.com/graphics/different-choice'
        self.assertNotEqual(MathAcademyBrowser._binding(changed), MathAcademyBrowser._binding(captured))
        ambiguous = deepcopy(captured)
        ambiguous['assets'][3]['extraction_part'] = 'problem'
        ambiguous['fields'][0]['choices'][2].pop('html', None)
        self.assertNotEqual(MathAcademyBrowser._binding(raw), MathAcademyBrowser._binding(ambiguous))

    def test_image_binding_matches_captured_paths_but_rejects_changed_source(self):
        for tag, source, html in [('img', 'https://mathacademy.com/graphics/q-1-a-1', '<img src="/graphics/q-1-a-1">'),
                                  ('svg', None, '<svg><path d="M0 0L1 1"/></svg>')]:
            with self.subTest(tag=tag):
                raw = {'problem': 'Choose ![](@asset-0@)',
                       'assets': [{'index': 0, 'tag': tag, 'source_url': source, 'html': html}],
                       'fields': [{'key': 'selection', 'type': 'radio', 'choices': [
                           {'option': 'a', 'type': 'image', 'value': '@asset-0@', 'dom_id': 'choice-a'}]}]}
                captured = deepcopy(raw)
                captured['assets'][0]['path'] = '/capture/assets/hash.png'
                captured = replace_markers(captured, {'@asset-0@': '/capture/assets/hash.png'})
                self.assertEqual(MathAcademyBrowser._binding(raw), MathAcademyBrowser._binding(captured))
                changed = deepcopy(raw)
                changed['assets'][0]['html'] += '<!-- changed -->'
                self.assertNotEqual(MathAcademyBrowser._binding(changed), MathAcademyBrowser._binding(captured))
                moved = deepcopy(captured)
                moved['assets'][0]['path'] = '/another/assets/hash.png'
                moved = replace_markers(moved, {'/capture/assets/hash.png': '/another/assets/hash.png'})
                self.assertEqual(MathAcademyBrowser._binding(moved), MathAcademyBrowser._binding(captured))

    def test_table_image_binding_uses_original_source_and_keeps_layout_and_controls(self):
        raw = {'dom_id': 'step-q363860',
               'problem': '<table><tr><td rowspan="2"><img src="@asset-0@" alt=""></td>'
                          '<td>{{field-1}}</td></tr><tr><td><img src="@asset-1@" alt=""></td></tr></table>',
               'assets': [{'index': i, 'tag': 'img', 'source_url': 'https://mathacademy.com/graphics/tree',
                           'html': '<img src="/graphics/tree">', 'extraction_part': 'problem'} for i in range(2)],
               'fields': [{'key': 'field-1', 'type': 'select', 'tag': 'custom-select', 'dom_id': 'select-1',
                           'choices': [{'option': '0', 'type': 'text', 'value': 'M'}]}]}
        captured = deepcopy(raw)
        for asset in captured['assets']:
            asset['path'] = '/capture/assets/shared-tree.png'
        captured = replace_markers(captured, {f'@asset-{i}@': '/capture/assets/shared-tree.png' for i in range(2)})
        self.assertEqual(MathAcademyBrowser._binding(raw), MathAcademyBrowser._binding(captured))
        for kind in ('source', 'layout', 'choice'):
            changed = deepcopy(raw)
            if kind == 'source':
                changed['assets'][1]['source_url'] += '-different'
            elif kind == 'layout':
                changed['problem'] = changed['problem'].replace('rowspan="2"', 'rowspan="3"')
            else:
                changed['fields'][0]['choices'][0]['value'] = 'D'
            with self.subTest(change=kind):
                self.assertNotEqual(MathAcademyBrowser._binding(changed), MathAcademyBrowser._binding(captured))

    def test_learn_course_percentage_uses_authored_label_and_source_course(self):
        html = (FIXTURES / 'learn-course-progress.html').read_text()
        result = parse_dashboard(html + '<div id="dailyGoalPoints">999/50 XP</div>', '1')
        self.assertEqual(result['course_progress'], {'course_id': '76', 'course_href': '/courses/76/progress',
            'displayed_progress': '37%', 'source_selector': '#coursePercentComplete'})
        unknown = parse_dashboard(html.replace('37%', 'Progress unavailable'), '1')
        self.assertEqual(unknown['course_progress']['displayed_progress'], 'Progress unavailable')
        absent = parse_dashboard('<div id="courseProgress">88%</div>', '1')
        self.assertIsNone(absent['course_progress']['displayed_progress'])
        self.assertIsNone(absent['course_progress']['course_id'])

    def test_queue_retains_source_details_and_start_link(self):
        rows = parse_queue((FIXTURES / "quiz-6-required-card.html").read_text())
        self.assertEqual(len(rows), 1)
        row = rows[0]
        self.assertEqual(row["kind"], "assessment")
        self.assertFalse(row["started"])
        self.assertTrue(row["url"].endswith("/start"))
        self.assertTrue(row["details"]["source_fields"])
        self.assertTrue(row["details"]["links"])

    def test_forced_diagnostic_is_started_without_guessing_question_id(self):
        row = activity_from_url("https://mathacademy.com/tasks/22/diagnostics/31")
        self.assertEqual(row["kind"], "diagnostic")
        self.assertTrue(row["started"])
        self.assertIsNone(question_identity("questionContainer", "Question 12", diagnostic=True))

    def test_history_uses_kp_source_link_and_observed_difficulty(self):
        [row] = parse_history_metadata((FIXTURES / "review-history-question.html").read_text())
        self.assertEqual(row["math_academy_id"], "q-1396")
        self.assertEqual(row["topic_id"], "245")
        self.assertEqual(row["knowledge_point_source_id"], 4341)
        self.assertEqual(row["difficulty"], "easy")
        self.assertEqual(row["grade"], "Correct")

    def test_lesson_content_and_placement_are_distinct(self):
        html = '<h1 id="topicName">Vectors</h1><div class="step" id="step-t8" stepid="51" steptype="tutorial" contentid="8"><span class="stepName">Start</span></div><div class="step" stepid="52" steptype="example" contentid="19"><span class="stepName">Example: Add</span></div>'
        record = parse_lesson_structure(html, 3)
        self.assertTrue(record["complete"])
        self.assertEqual([(s["math_academy_id"], s["content_id"]) for s in record["steps"]], [(51, 8), (52, 19)])
        self.assertEqual(record["steps"][1]["title"], "Add")

    def test_semantic_choice_survives_shuffle(self):
        field = {"key": "selection", "choices": [{"value": "B", "option": "a"}, {"value": "A", "option": "b"}]}
        self.assertEqual(pick_choice(field, {"value": "A", "option": "a"})["option"], "b")
        with self.assertRaises(ValueError):
            pick_choice(field, {"value": "absent", "option": "a"})

    def test_original_svg_bytes_are_saved_and_source_html_is_unchanged(self):
        with tempfile.TemporaryDirectory() as directory:
            original = '<svg xmlns="http://www.w3.org/2000/svg"><circle r="4"/></svg>'
            item = {"problem": "![](@asset-0@)", "html": "@asset-0@", "assets": [{"index": 0, "tag": "svg", "html": original}]}
            captured = AssetCapture(SimpleNamespace()).collect(item, None, directory, "step")
            asset = captured["assets"][0]
            self.assertEqual(Path(asset["path"]).read_bytes(), original.encode())
            self.assertEqual(asset["sha256"], hashlib.sha256(original.encode()).hexdigest())
            self.assertEqual(captured["html"], "@asset-0@")
            self.assertIn(asset["path"], captured["problem"])

    def test_inline_svg_assembles_only_observed_shared_definitions(self):
        source='<svg viewBox="0 0 10 10"><use xlink:href="#graph"/></svg>'
        definitions={'graph':'<path id="graph" fill="url(#color)" d="M0 0 L10 10"/>',
                     'color':'<linearGradient id="color"><stop offset="0" stop-color="red"/></linearGradient>'}
        calls=[]
        class Page:
            def evaluate(_,script,ids):
                calls.append(ids)
                return {identity:definitions.get(identity) for identity in ids}
        with tempfile.TemporaryDirectory() as directory:
            item={"problem":"![](@asset-0@)","html":source,"assets":[{"index":0,"tag":"svg","html":source}]}
            captured=AssetCapture(SimpleNamespace(page=Page())).collect(item,None,directory,"step")
            asset=captured['assets'][0]
            self.assertEqual(asset['html'],source)
            self.assertEqual(captured['html'],source)
            self.assertEqual(asset['representation'],'standalone_svg')
            self.assertEqual(asset['source_sha256'],hashlib.sha256(source.encode()).hexdigest())
            self.assertEqual(calls,[['graph'],['color']])
            data=Path(asset['path']).read_bytes()
            self.assertIn(b'viewBox="0 0 10 10"',data)
            self.assertIn(definitions['graph'].encode(),data)
            self.assertIn(definitions['color'].encode(),data)
            from scripts.database.images import extension
            self.assertEqual(extension(data),'svg')
            self.assertEqual(asset['sha256'],hashlib.sha256(data).hexdigest())
            self.assertEqual([record['id'] for record in asset['standalone_definitions']],['graph','color'])
        with self.assertRaises(ValueError):
            standalone_svg(source)

    def test_html_error_page_is_not_stored_as_an_image(self):
        with self.assertRaises(ValueError):
            image_extension(b"<html>Sign in</html>", "image/png")

    def test_xp_denominator_and_penalty_are_source_values(self):
        self.assertEqual(parse_xp("8 of 13 XP")["base_xp"], 13)
        self.assertEqual(parse_xp("-5 / 13")["earned_xp"], -5)

    def test_awarded_xp_phrase_keeps_earned_and_task_base_distinct(self):
        for apostrophe in ("'", "’"):
            source="Congratulations! You've completed the lesson.\nYou've been awarded 7 of the task"+apostrophe+"s 10 XP.\nContinue"
            parsed=parse_xp(source)
            self.assertEqual(parsed['earned_xp'],7)
            self.assertEqual(parsed['base_xp'],10)
            self.assertEqual(parsed['source_text'],source)

    def test_quiz_score_does_not_replace_explicit_xp_award(self):
        for apostrophe in ("'", "’"):
            source = ("Congratulations! You answered 8 of 9 questions correctly for a score of 89%.\n"
                      "You've been awarded all of the task" + apostrophe + "s 15 XP.\nCONTINUE")
            parsed = parse_xp(source)
            self.assertEqual((parsed['earned_xp'], parsed['base_xp']), (15, 15))
            self.assertEqual(parsed['source_text'], source)
        parsed = parse_xp("You answered 7 of 11 questions correctly for a score of 64%.\nYou've been awarded 8 XP.")
        self.assertEqual((parsed['earned_xp'], parsed['base_xp']), (8, None))

    def test_quiz_score_without_xp_award_is_not_an_xp_observation(self):
        for source in ("You answered 8 of 9 questions correctly.", "Your score is 8 / 9 questions."):
            parsed = parse_xp(source)
            self.assertEqual((parsed['earned_xp'], parsed['base_xp']), (None, None))

    def test_math_editor_notation_changes_do_not_change_scope(self):
        self.assertEqual(normalized_math("x/2"), normalized_math(r"\frac{x}{2}"))
        self.assertEqual(normalized_math("x^2"), normalized_math("x^{2}"))
        self.assertEqual(normalized_math(r"\left(x\right)"), normalized_math("(x)"))
        self.assertNotEqual(normalized_math("x/2y"), normalized_math(r"\frac{x}{2y}"))
        self.assertNotEqual(normalized_math("x+1/2"), normalized_math(r"\frac{x+1}{2}"))
        with self.assertRaises(ValueError):
            validated_keys([{"text": None, "key": "Enter"}])

    def test_mathquill_relation_aliases_preserve_the_operator(self):
        for long, short in ((r'\leq', r'\le'), (r'\geq', r'\ge'), (r'\neq', r'\ne')):
            self.assertEqual(normalized_math(long), normalized_math(short))
            self.assertEqual(normalized_math('x'+long+'2'), normalized_math('x'+short+'2'))
        for other in ('<', r'\ge', r'\leqq', r'\leqslant'):
            self.assertNotEqual(normalized_math(r'\leq'), normalized_math(other))


class OfflineBrowserTests(unittest.TestCase):
    def test_unstyled_empty_final_screen_does_not_complete_unanswered_review(self):
        from scripts.browser.adapter import VIEW
        self.page.set_content('''<div id="steps"><div class="step questionWidget" id="step-q8740">
          <div class="questionWidget-text">Choose the equation.</div>
          <div class="questionWidget-choiceLetterCircle">a</div>
          <button class="questionWidget-submitButton">Submit</button></div></div>
          <div id="finalScreen"><div id="finalScreen-completionMessage"></div>
          <div id="finalScreen-pointsMessage"></div><button>Continue</button></div>''')
        self.assertEqual(self.page.evaluate(VIEW)['kind'], 'question')
        self.page.locator('#finalScreen-completionMessage').evaluate("n=>n.textContent='Review complete'")
        self.assertEqual(self.page.evaluate(VIEW)['kind'], 'complete')

    @classmethod
    def setUpClass(cls):
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            raise unittest.SkipTest("Playwright is required for offline DOM tests")
        cls.pw = sync_playwright().start()
        try:
            cls.browser = cls.pw.chromium.launch(headless=True)
        except Exception:
            cls.pw.stop()
            raise

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.pw.stop()

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.directory = Path(self.temporary.name)
        self.context = self.browser.new_context()
        self.context.route("**/*", lambda route: route.abort())  # No live websites.
        self.page = self.context.new_page()
        config = SimpleNamespace(timeout_ms=1000, course_id="55", account="test")
        self.adapter = MathAcademyBrowser(config, threading.Event())
        self.adapter.page = self.page
        self.adapter.context = self.context
        self.adapter.directory = self.directory
        self.adapter.activity = {"task_id": "1", "kind": "review", "topic_id": "245", "details": {}}

    def tearDown(self):
        self.context.close()
        self.temporary.cleanup()

    def test_mathml_currency_glyphs_are_escaped_without_changing_math_delimiters(self):
        for token in ('mi','mo','mn','mtext'):
            with self.subTest(token=token):
                self.page.set_content('<div id="q"><div class="questionText"><math><'+token+'>$</'+token+'><mn>25</mn></math></div></div>')
                value=self.page.locator('#q').evaluate(EXTRACT)['problem']
                self.assertIn(r'\$',value)
                self.assertFalse(value.startswith('$$'))

    def test_tex_spacing_in_mixed_number_is_removed_before_mathquill_entry(self):
        self.page.set_content('<div id="wrapper"><span class="mq-editable-field"></span></div>')
        self.page.evaluate(r'''() => {
          let latex='';const field={focus(){},select(){},write(v){latex=v.includes('\\,')?'':v},latex(){return latex}};
          window.MathQuill={getInterface:()=>()=>field};
        }''')
        self.assertEqual(write_math(self.page.locator('#wrapper'),r'2\,\frac{2}{5}',[]),r'2\frac{2}{5}')

    def test_relation_alias_readback_succeeds_without_entry_retry(self):
        self.page.set_content('<div id="wrapper"><span class="mq-editable-field"></span></div>')
        self.page.evaluate(r'''() => {
          let latex='';window.writes=0;
          const field={focus(){},select(){},write(v){window.writes++;latex=v.replace('\\leq','\\le')},latex(){return latex}};
          window.MathQuill={getInterface:()=>()=>field};
        }''')
        self.assertEqual(write_math(self.page.locator('#wrapper'),r'\leq',[{'text':r'\leq'}]),r'\le')
        self.assertEqual(self.page.evaluate('writes'),1)

    def test_partially_visible_dropdown_option_uses_an_exposed_point_without_scrolling(self):
        from scripts.browser.entry import click_dropdown
        self.page.set_viewport_size({'width':600,'height':300})
        self.page.set_content('<button id="option" style="position:fixed;top:295px;left:20px;height:30px" onclick="this.dataset.selected=1">Choose</button>')
        click_dropdown(self.page.locator('#option'),scroll=False)
        self.assertEqual(self.page.locator('#option').get_attribute('data-selected'),'1')
        self.assertEqual(self.page.evaluate('scrollY'),0)

    def test_saved_radio_keeps_math_and_all_choices(self):
        self.page.set_content((FIXTURES / "q-1396-before.html").read_text())
        item = self.page.locator("#step-q1396").evaluate(EXTRACT)
        self.assertIn("a\\times b", item["problem"])
        self.assertEqual(len(item["fields"][0]["choices"]), 5)
        self.assertTrue(item["fields"][0]["choices_complete"])
        self.assertEqual(item["errors"], [])

    def test_saved_diagnostic_selects_are_not_lost_after_skip(self):
        counts = []
        for name in ("diagnostic-skipped-select-before.html", "diagnostic-skipped-select-after.html"):
            self.page.set_content((FIXTURES / name).read_text())
            scope = self.page.locator("#questionContainer")
            if not scope.count():
                scope = self.page.locator("body")
            item = scope.evaluate(EXTRACT)
            counts.append(len(item["fields"]))
            self.assertTrue(all(f["choices"] for f in item["fields"]))
        self.assertTrue(counts[0])
        self.assertEqual(counts[0], counts[1])

    def test_saved_lesson_preserves_tutorial_and_example_placement_ids(self):
        html = (FIXTURES / "lesson-3178-fragment.html").read_text()
        definition = parse_lesson_structure(html, 3178)
        self.assertEqual([(x["math_academy_id"], x["content_id"]) for x in definition["steps"]], [(657075, 7725), (657079, 12356)])
        self.page.set_content(html)
        tutorial = self.page.locator('div.step[stepid="657075"]').evaluate(EXTRACT)
        example = self.page.locator('div.step[stepid="657079"]').evaluate(EXTRACT)
        self.assertTrue(tutorial["problem"])
        self.assertTrue(example["problem"])
        self.assertTrue(example["worked_solution"])
        self.assertNotIn("Continue", tutorial["problem"])

    def test_fixed_phantom_spacing_does_not_invalidate_full_lesson_definition(self):
        html = '''<h1 id="topicName">Long division</h1><div id="steps">
          <div class="step" id="step-71" stepid="71" steptype="example" contentid="10">
          <span class="stepName">Example: Divide</span>
          <div class="exampleQuestion">Divide 504 by 8.</div>
          <div class="exampleExplanation"><math><menclose notation="longdiv"><mn>5</mn>
          <mphantom><mo stretchy="false">|</mo></mphantom><mn>0</mn>
          <mphantom><mo stretchy="false">|</mo></mphantom><mn>4</mn></menclose></math>
          The quotient is 63.</div></div></div>'''
        self.adapter._goto = lambda url, page: page.set_content(html)
        self.adapter._settle_content = lambda *args: None
        result = self.adapter._lesson({'topic_id': '1'}, self.directory)
        self.assertTrue(result['lesson_definition']['complete'])
        self.assertEqual(result['lesson_definition']['issues'], [])
        self.assertEqual(result['canonical_examples'][0]['errors'], [])
        self.assertIn(r'\phantom{|}', result['canonical_examples'][0]['worked_solution'])

    def test_saved_assessment_and_multistep_keep_field_structure(self):
        for filename, expected in [("assessment-105178-question.html", "q-105178"),
                                   ("multistep-128186-question.html", "q-128186")]:
            self.page.set_content((FIXTURES / filename).read_text())
            scope = self.page.locator('.question').first
            item = scope.evaluate(EXTRACT)
            self.assertEqual(question_identity(item["dom_id"]), expected)
            self.assertTrue(item["problem"])
            self.assertTrue(item["fields"])
        self.page.set_content((FIXTURES / "multistep-128186-context.html").read_text())
        context = self.page.locator('.step').evaluate(EXTRACT)
        self.assertIn("initial value problem", context["problem"])
        self.assertFalse(context["fields"])

    def test_multistep_question_controls_precede_selected_shared_context(self):
        self.adapter.activity['kind'] = 'multistep'
        self.page.set_content('''<div id="stepButton-1" class="stepButton current"></div>
          <button id="stepButton-2" class="stepButton" onclick="
            document.getElementById('stepButton-1').classList.remove('current');
            this.classList.add('current')">Question 1</button>
          <div id="steps">
          <div id="step-1" class="step">Carla is organizing a nut sale.</div>
          <div id="step-2" class="step"><div id="question-134231" class="question">
            <div class="questionText">How many bags?</div><input id="answer"/>
            <button class="submitButton">Submit</button>
            <div class="correctAnswerText" style="display:none"></div></div>
            <button id="continueButton-2" style="display:none"
              onclick="if(document.getElementById('stepButton-2').classList.contains('current')) {
                this.style.display='none';document.getElementById('step-3').style.display='block';
              }">Continue</button></div>
          <div id="step-3" class="step" style="display:none">
            <div id="question-134232" class="question"><div class="questionText">Next part?</div>
              <input/><button class="submitButton">Submit</button></div></div></div>''')
        observation = self.adapter.observe(self.directory)
        self.assertEqual(observation['kind'], 'question')
        self.assertEqual(observation['key'], 'step-2')
        self.assertEqual(observation['question']['math_academy_id'], 'q-134231')
        self.assertEqual(observation['shared_context'], 'Carla is organizing a nut sale.')
        self.assertEqual(len(observation['part_order']), 2)
        # The source can keep the setup selected after grading the first part.
        self.page.evaluate('''() => {
          document.querySelector('#step-2 .submitButton').style.display='none';
          document.querySelector('#step-2 .correctAnswerText').textContent='Correct';
          document.querySelector('#step-2 .correctAnswerText').style.display='block';
          document.getElementById('continueButton-2').style.display='block';
        }''')
        graded = self.adapter.observe(self.directory)
        self.assertTrue(graded['accepted'])
        self.assertEqual(graded['next'], '#continueButton-2')
        self.adapter._pause = lambda *args, **kwargs: None
        self.adapter.advance(graded, self.directory)
        self.assertEqual(self.adapter._view()['key'], 'step-3')

    def test_graded_question_is_not_submitted_again(self):
        self.page.set_content('''<div class="step questionWidget" id="step-q1">
          <div class="questionWidget-text">What is 2+2?</div><input id="answer"/>
          <div class="questionWidget-result"></div>
          <button class="questionWidget-submitButton" onclick="window.submissions=(window.submissions||0)+1;this.parentNode.querySelector('.questionWidget-result').textContent='Correct';this.style.display='none';document.getElementById('continueButton-q1').style.display='block'">Submit</button>
          <button id="continueButton-q1" style="display:none">Continue</button></div>''')
        before = self.adapter.observe(self.directory)
        self.assertFalse(before["accepted"])
        self.adapter.respond(before, [{"key": "field-1", "value": "4"}], self.directory)
        after = self.adapter.observe(self.directory)
        self.assertTrue(after["accepted"])
        self.adapter.respond(before, [{"key": "field-1", "value": "4"}], self.directory)
        self.assertEqual(self.page.evaluate("window.submissions"), 1)

    def test_unknown_submission_outcome_is_reloaded_before_any_retry(self):
        self.page.set_content('''<div class="step questionWidget" id="step-q1"><div class="questionWidget-text">What is 2+2?</div><input id="answer"/><button class="questionWidget-submitButton" onclick="window.submissions=(window.submissions||0)+1">Submit</button></div>''')
        observation = self.adapter.observe(self.directory)
        self.adapter.state["pending_action"] = {"key": observation["key"], "action": "submit"}
        self.adapter.state["restored"] = False
        reloads = []
        self.adapter._goto = lambda url: reloads.append(url)
        self.adapter.respond(observation, [{"key": "field-1", "value": "4"}], self.directory)
        self.assertEqual(len(reloads), 1)
        self.assertIsNone(self.page.evaluate("window.submissions"))
        self.assertTrue(self.adapter.state["restored"])

    def test_pending_assessment_submission_reloads_before_confirming_again(self):
        self.adapter.activity["kind"] = "assessment"
        self.page.set_content('<button id="submitTestButton" onclick="window.clicked=true">Submit test</button>')
        self.adapter.state["pending_action"] = {"action": "submit_assessment"}
        self.adapter.state["restored"] = False
        reloads = []
        self.adapter._goto = lambda url: reloads.append(url)
        result = self.adapter.respond({"key": "assessment-submit"}, {"action": "submit_assessment"}, self.directory)
        self.assertEqual(len(reloads), 1)
        self.assertIsNone(self.page.evaluate("window.clicked"))
        self.assertTrue(result["not_submitted"])

    def test_continue_selects_its_step_after_scrolling_to_a_short_tutorial(self):
        # MA selects the step occupying most of the viewport on scroll. Its
        # Continue handler advances from that selection, not the button's ID.
        self.page.set_content('''<style>body{margin:0}.step{display:block}
          #step-q1{height:1800px}#step-t2{height:100px}
          #stepButton-t2{position:fixed;top:10px;right:10px}</style>
          <div id="stepButton-q1" class="stepButton current"></div>
          <button id="stepButton-t2" class="stepButton"
            onmousedown="select('t2')">Tutorial</button>
          <div class="step" id="step-q1"><p>Earlier accepted question</p></div>
          <div class="step" id="step-t2"><p>Short tutorial.</p>
          <button id="continueButton-t2" onmousedown="setTimeout(()=>{
            window.continues=(window.continues||0)+1;
            if(document.querySelector('.stepButton.current').id==='stepButton-t2'){
              document.getElementById('step-t3').style.display='block';
              this.style.display='none';}else{select('t2');}},10)">Continue</button></div>
          <div class="step" id="step-t3" style="display:none"><p>Next tutorial</p>
          <button id="continueButton-t3">Continue</button></div>
          <script>function select(id){document.querySelector('.stepButton.current').classList.remove('current');
            document.getElementById('stepButton-'+id).classList.add('current');}
            window.addEventListener('scroll',()=>select('q1'));</script>''')
        observation = self.adapter._view()
        self.adapter._pause = lambda *args, **kwargs: None
        self.adapter.advance(observation, self.directory)
        self.assertEqual(self.adapter._view()['key'], 'step-t3')
        self.assertEqual(self.page.evaluate('window.continues'), 1)

    def test_pending_continue_reloads_before_clicking_again(self):
        self.page.set_content('<div class="step" id="step-t1"><p>Read this.</p><button id="continueButton-t1" onclick="window.clicked=true">Continue</button></div>')
        observation = self.adapter._view()
        self.adapter.state["pending_action"] = {"action": "advance", "key": observation["key"]}
        self.adapter.state["restored"] = False
        reloads = []
        self.adapter._goto = lambda url: reloads.append(url)
        self.adapter.advance(observation, self.directory)
        self.assertEqual(len(reloads), 1)
        self.assertIsNone(self.page.evaluate("window.clicked"))

    def test_assessment_minutes_label_uses_conservative_rounded_budget(self):
        self.page.set_content('<span id="timeRemaining">15 minutes remaining</span>')
        self.assertEqual(self.adapter._remaining(), 840)

    def test_assessment_entry_is_not_a_grade_and_whole_submit_is_separate(self):
        self.adapter.activity["kind"] = "assessment"
        self.page.set_content('''<div id="questions"><div class="question" id="question-4"><div class="questionText">First</div><input id="a"/></div><div class="question" id="question-5"><div class="questionText">Second</div><input id="b"/></div></div>
          <button id="submitTestButton" onclick="document.getElementById('confirmationDialog').style.display='block'">Submit test</button>
          <div id="confirmationDialog" style="display:none">Submit this test?<button onclick="document.getElementById('finalScreen').style.display='block'">Yes</button></div>
          <div id="finalScreen" style="display:none">8 of 13 XP</div>''')
        first = self.adapter.observe(self.directory)
        self.assertFalse(first["accepted"])
        self.adapter.respond(first, [{"key": "field-1", "value": "4"}], self.directory)
        second = self.adapter.observe(self.directory)
        self.assertEqual(second["question"]["math_academy_id"], "q-5")
        self.adapter.respond(second, [{"key": "field-1", "value": "5"}], self.directory)
        submit = self.adapter.observe(self.directory)
        self.assertEqual(submit["action"], "submit_assessment")
        self.adapter.respond(submit, {"action": "submit_assessment"}, self.directory)
        done = self.adapter.observe(self.directory)
        self.assertEqual(done["kind"], "complete")
        self.assertEqual(done["completion"]["base_xp"], 13)

    def test_queue_expands_each_card_even_when_previous_one_collapses(self):
        self.page.set_content('''<div id="incompleteTasks">
          <div id="task-1" class="taskUnlocked" progress="0"><span class="taskTypeUnlocked">Lesson</span><span id="taskName-1" onclick="expand(1)">One</span><div class="taskDetails" style="display:none"></div></div>
          <div id="task-2" class="taskUnlocked" progress="0.5"><span class="taskTypeUnlocked">Review</span><span id="taskName-2" onclick="expand(2)">Two</span><div class="taskDetails" style="display:none"></div></div></div>
          <script>function expand(id){document.querySelectorAll('.taskDetails').forEach(n=>n.style.display='none');let n=document.querySelector('#task-'+id+' .taskDetails');n.style.display='block';n.innerHTML='<a class="taskStartButton" href="/tasks/'+id+'/topics/245/'+(id===1?'lesson':'review')+'">Start</a>';}</script>''')
        self.adapter._goto = lambda *args: None
        queue = self.adapter.queue(self.directory)
        self.assertEqual(len(queue), 2)
        self.assertTrue(all(item["url"] for item in queue))
        self.assertTrue(queue[1]["started"])
        self.assertTrue((self.directory / "queue-card-1.html").exists())

    def test_multistep_shared_context_is_not_prepended_to_local_problem(self):
        self.adapter.activity["kind"] = "multistep"
        self.page.set_content('''<div id="steps"><div class="step" id="step-1"><p>A shared setup.</p></div><div class="step" id="step-2"><div class="question" id="question-7"><div class="questionText">Find x.</div><input id="x"/></div><button class="submitButton" id="submitButton-2">Submit</button></div></div>''')
        item = self.adapter.observe(self.directory)
        self.assertEqual(item["question"]["problem"], "Find x.")
        self.assertEqual(item["shared_context"], "A shared setup.")
        self.assertEqual(item["part_order"][0]["math_academy_id"], "q-7")

    def test_multistep_context_dom_id_is_not_a_tutorial_identity(self):
        self.adapter.activity['kind'] = 'multistep'
        self.page.set_content('''<div id="steps"><div class="step" id="step-1">
          <p>A shared setup.</p><button id="continueButton-1">Continue</button>
          </div></div>''')
        item = self.adapter.observe(self.directory)
        self.assertEqual(item['kind'], 'tutorial')
        self.assertIsNone(item['tutorial']['math_academy_id'])
        self.assertEqual(item['tutorial']['dom_id'], 'step-1')
        self.assertEqual(item['shared_context'], 'A shared setup.')

    def test_late_postprocessing_never_borrows_newer_activity_xp(self):
        self.adapter.state = {"task_id": "2", "completion": {"earned_xp": 99, "base_xp": 100}}
        (self.directory / "browser-state.json").write_text(json.dumps({"task_id": "1", "completion": {"earned_xp": 3, "base_xp": 5}}))
        def dashboard(url, page=None):
            page.set_content('<div id="completedTasks"></div>')
        self.adapter._goto = dashboard
        result = self.adapter.postprocess(self.adapter.activity, self.directory)
        self.assertEqual(result["completion"]["earned_xp"], 3)
        self.assertEqual(self.adapter.state["completion"], {"earned_xp": 99, "base_xp": 100})
        first = result["dashboard"]["html_path"]
        second = self.adapter.postprocess(self.adapter.activity, self.directory)
        self.assertNotEqual(first, second["dashboard"]["html_path"])
        self.assertTrue(Path(first).exists())
        self.assertEqual(len(list((self.directory / "post-activity").glob("*/observations.json"))), 2)

    def test_postprocess_saves_learn_percentage_with_its_source_evidence(self):
        html = (FIXTURES / 'learn-course-progress.html').read_text()
        def show_page(url, page=None):
            page.set_content(html + '<div id="completedTasks"></div>' if url.endswith('/learn') else
                '<table class="moduleTopics"><tr><td><a class="topicLink" href="/topics/1?courseId=76">Topic</a>'
                '<span class="topicCircle" style="background:white"></span></td></tr></table>')
        self.adapter._goto = show_page
        result = self.adapter.postprocess(self.adapter.activity, self.directory)
        dashboard = result['dashboard']
        self.assertEqual(dashboard['course_progress']['displayed_progress'], '37%')
        self.assertEqual(dashboard['course_progress']['course_id'], '76')
        self.assertGreater(dashboard['captured_at'], 0)
        self.assertIn('coursePercentComplete', Path(dashboard['html_path']).read_text())
        saved = json.loads(next((self.directory / 'post-activity').glob('*/observations.json')).read_text())
        self.assertEqual(saved['dashboard'], dashboard)

    def test_review_completed_dashboard_card_finishes_only_the_pinned_activity(self):
        self.page.set_content((FIXTURES / 'review-autocompleted-dashboard.html').read_text())
        self.adapter.activity = {'task_id': '14108723', 'kind': 'review'}
        observation = self.adapter.observe(self.directory)
        self.assertEqual(observation['kind'], 'complete')
        self.assertEqual(observation['completion']['task_id'], '14108723')
        self.assertEqual((observation['completion']['earned_xp'], observation['completion']['base_xp']), (2, 4))
        self.assertTrue(self.adapter.state['completed'])
        self.adapter.activity = {'task_id': '14108724', 'kind': 'review'}
        self.assertEqual(self.adapter._view()['kind'], 'unknown')

    def test_unknown_page_offers_continuation_controls_without_navigation_links(self):
        self.page.set_content('<a id="topic" href="/topics/3852">Rank–Nullity</a>'
            '<a id="course" href="/courses/76">Linear Algebra</a>'
            '<a id="question" href="/learn?taskId=99">Question details</a>'
            '<a id="continue" class="button" href="#">Continue</a><button id="retry">Retry</button>')
        buttons = self.adapter._view()['buttons']
        self.assertEqual({button['selector'] for button in buttons}, {'#continue', '#retry'})

    def test_unknown_page_agent_can_choose_a_current_idless_continue(self):
        self.page.set_content('''<div><button onclick="this.remove();document.getElementById('finalScreen').style.display='block';window.recoveryClicks=(window.recoveryClicks||0)+1">Continue</button></div><div id="finalScreen" style="display:none">Done</div>''')
        observation = self.adapter.observe(self.directory)
        [button] = observation["buttons"]
        self.assertTrue(button["selector"])
        decision = {"action": "advance", "button_selector": button["selector"], "button_text": button["text"]}
        self.adapter.recover(observation, decision, self.directory)
        self.adapter.recover(observation, decision, self.directory)
        self.assertEqual(self.page.evaluate("window.recoveryClicks"), 1)
        self.assertEqual(self.adapter.observe(self.directory)["kind"], "complete")

    def test_unknown_page_recovery_rejects_unobserved_or_abandon_controls(self):
        self.page.set_content('<button id="continue">Continue</button><button id="quit">Quit</button>')
        observation = self.adapter.observe(self.directory)
        with self.assertRaises(ValueError):
            self.adapter.recover(observation, {"action": "advance", "button_selector": "#quit", "button_text": "Quit"}, self.directory)
        with self.assertRaises(ValueError):
            self.adapter.recover(observation, {"action": "advance", "button_selector": "#unseen", "button_text": "Continue"}, self.directory)

    def test_math_editor_uses_validated_keys_when_write_cannot_enter_value(self):
        self.page.set_content('''<div class="matheditor-wrapper-answer"><span class="mq-editable-field"><textarea></textarea></span></div><script>
          window.calls=[];window.output='';window.MathQuill=()=>({focus(){},select(){},write(){throw Error('unsupported direct write')},keystroke(key){calls.push(['key',key]);if(key==='Backspace')output='';},cmd(value){calls.push(['command',value]);output+=value;},typedText(value){calls.push(['text',value]);output+=value;},latex(){return output;}});
        </script>''')
        observed = write_math(self.page.locator('.matheditor-wrapper-answer'), r"\pi", [{"text": r"\pi", "key": None}])
        self.assertEqual(observed, r"\pi")
        self.assertIn(["command", r"\pi"], self.page.evaluate("window.calls"))
        self.assertNotIn(["text", r"\pi"], self.page.evaluate("window.calls"))

    def test_image_response_cache_is_scoped_to_the_current_activity(self):
        self.adapter._goto = lambda *args: None
        activity = {**self.adapter.activity, "url": "https://mathacademy.com/tasks/1/topics/245/review"}
        sentinel = object()
        self.adapter.image_responses["current-image"] = sentinel
        self.adapter.open(activity, self.directory, {})
        self.assertIs(self.adapter.image_responses["current-image"], sentinel)
        following = {**activity, "task_id": "2", "url": "https://mathacademy.com/tasks/2/topics/245/review"}
        self.adapter.open(following, self.directory / "next", {})
        self.assertEqual(self.adapter.image_responses, {})

    def test_custom_dropdown_can_reparent_its_menu_to_body(self):
        self.page.set_content('''<div id="question"><div class="selectList" id="select"><div class="selectListFrame" style="padding:8px;border:1px solid black" onclick="let m=document.querySelector('.selectListOptions');document.body.appendChild(m);m.style.display='block';">Choose</div><div class="selectListOptions" style="display:none"><div class="selectListOption" id="one" onclick="document.querySelector('.selectListFrame').textContent=this.textContent;this.parentNode.style.display='none'">One</div></div></div></div>''')
        field = {"key": "field-1", "type": "select", "tag": "custom-select", "dom_id": "select", "choices": [{"value": "One", "type": "text", "option": "0", "dom_id": "one"}]}
        response = enter(self.page.locator('#question'), field, {"value": "One"})
        self.assertEqual(response["value"], "One")
        self.assertEqual(self.page.locator('.selectListFrame').inner_text(), "One")

    def scroll_dropdown(self):
        """Own q184176 options with the archived public widget's event handlers."""
        saved = json.loads((FIXTURES / 'scroll-dropdown-q184176.json').read_text())
        self.page.set_viewport_size({'width': 730, 'height': 300})
        self.page.set_content('''<style>body{margin:0}.selectListFrame{height:21px;width:190px;border:1px solid}
          .selectListOptions{position:absolute;visibility:hidden;background:white;width:190px}
          .selectListOption{height:21px}mjx-assistive-mml{display:none}
          #scroll{position:absolute;top:40px;height:240px;width:600px;overflow:auto}</style>
          <div id="scroll"><div style="height:1000px"></div><div id="question">''' + saved['html'] +
          '''</div><div style="height:1000px"></div></div>''')
        self.page.add_script_tag(content=(FIXTURES / 'public-select-list.js').read_text())
        self.page.evaluate('''()=>{
          window.Core={findLeft:n=>n.getBoundingClientRect().left+scrollX,
            findTop:n=>n.getBoundingClientRect().top+document.querySelector('#scroll').scrollTop+scrollY,
            getHeight:n=>n.getBoundingClientRect().height};
          const w=Object.create(SelectList.prototype);
          w.element=document.querySelector('.selectList');w.frame=w.element.querySelector('.selectListFrame');
          w.optionsDiv=w.element.querySelector('.selectListOptions');w.options=[...w.optionsDiv.children];
          w.options.forEach((n,i)=>{n.index=i;n.onmousedown=w.onMouseDownOption.bind(w)});
          w.selectedOption=w.options[0];w.locked=false;w.onSelect=()=>{};window.widget=w;window.opens=0;
          w.frame.onmousedown=()=>{window.opens++;w.showOptions()};
          window.addEventListener('mousedown',e=>{if(e.target!==w.element&&e.target!==w.frame)w.hideOptions()});
          w.attchedScrollEventHandlers();
        }''')
        question = self.page.locator('#question').evaluate(EXTRACT)
        return question['fields'][0], saved

    def test_own_ninth_dropdown_option_positions_before_open_without_scrolling_open_menu(self):
        field, saved = self.scroll_dropdown()
        response = enter(self.page.locator('#question'), field, {'value': saved['value']})
        self.assertEqual(response['option'], saved['option'])
        self.assertEqual(self.page.evaluate('widget.getSelectedIndex()'), 8)
        self.assertEqual(self.page.evaluate('window.opens'), 1)
        self.assertEqual(self.page.locator('.selectListFrame').evaluate('n=>n.innerHTML'),
                         self.page.evaluate('widget.options[8].innerHTML'))

    def test_partly_clipped_ninth_row_is_positioned_before_open(self):
        field, saved = self.scroll_dropdown()
        self.page.set_viewport_size({'width': 730, 'height': 360})
        # The old center-before-open location exposes the ninth row's top but
        # clips its bottom; Playwright's ordinary click would scroll/hide it.
        self.page.evaluate('''()=>{
          widget.frame.scrollIntoView({block:'center'});
        }''')
        self.page.evaluate("()=>new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve)))")
        self.page.evaluate('''()=>{widget.showOptions();window.partial=widget.options[8].getBoundingClientRect().toJSON();
          widget.hideOptions();window.openMenuScrolls=0;
          window.addEventListener('scroll',()=>{
            if(getComputedStyle(widget.optionsDiv).visibility==='visible')window.openMenuScrolls++;
          },true);
        }''')
        partial = self.page.evaluate('window.partial')
        self.assertLess(partial['top'], 360)
        self.assertGreater(partial['bottom'], 360)
        enter(self.page.locator('#question'), field, {'value': saved['value']})
        self.assertEqual(self.page.evaluate('widget.getSelectedIndex()'), 8)
        self.assertEqual(self.page.evaluate('window.opens'), 1)
        self.assertEqual(self.page.evaluate('window.openMenuScrolls'), 0)

    def test_scroll_hidden_menu_reopens_same_nodes_once(self):
        field, saved = self.scroll_dropdown()
        self.page.evaluate('''()=>{const show=widget.showOptions.bind(widget);widget.showOptions=()=>{
          show();if(window.opens===1)widget.hideOptions();
        }}''')
        enter(self.page.locator('#question'), field, {'value': saved['value']})
        self.assertEqual(self.page.evaluate('window.opens'), 2)
        self.assertEqual(self.page.evaluate('widget.getSelectedIndex()'), 8)

    def test_visible_partly_clipped_option_selects_exposed_part_without_scroll_or_reopen(self):
        field, saved = self.scroll_dropdown()
        self.page.evaluate('''()=>{const show=widget.showOptions.bind(widget);window.openMenuScrolls=0;
          window.addEventListener('scroll',()=>{
            if(getComputedStyle(widget.optionsDiv).visibility==='visible')window.openMenuScrolls++;
          },true);
          widget.showOptions=()=>{show();
            widget.optionsDiv.style.top=(innerHeight-10-widget.options[8].offsetTop)+'px';
          };
        }''')
        enter(self.page.locator('#question'), field, {'value': saved['value']})
        self.assertEqual(self.page.evaluate('widget.getSelectedIndex()'), 8)
        self.assertEqual(self.page.evaluate('window.opens'), 1)
        self.assertEqual(self.page.evaluate('window.openMenuScrolls'), 0)

    def test_hidden_reopen_cannot_switch_to_replacement_frame(self):
        field, saved = self.scroll_dropdown()
        self.page.evaluate('''()=>{const show=widget.showOptions.bind(widget);widget.showOptions=()=>{
          show();widget.hideOptions();widget.frame.replaceWith(widget.frame.cloneNode(true));
        }}''')
        with self.assertRaisesRegex(ValueError, 'no exposed frame'):
            enter(self.page.locator('#question'), field, {'value': saved['value']})
        self.assertEqual(self.page.evaluate('widget.getSelectedIndex()'), 0)
        self.assertEqual(self.page.evaluate('window.opens'), 1)

    def test_actual_public_lesson_header_insets_window_scroll_before_open(self):
        field, saved = self.scroll_dropdown()
        self.page.set_viewport_size({'width': 1280, 'height': 800})
        self.page.add_style_tag(content=(FIXTURES / 'public-student-lesson.css').read_text())
        self.page.evaluate('''header=>{
          document.body.insertAdjacentHTML('afterbegin',header);
          document.querySelector('#scroll').id='lessonContent';
          widget.scrollableAncestor=widget.findScrollableParent();
          Core.findTop=n=>n.getBoundingClientRect().top+scrollY;
          widget.frame.scrollIntoView({block:'start'});
          window.openMenuScrolls=0;window.headerTopAtOpen=null;
          const show=widget.showOptions.bind(widget);widget.showOptions=()=>{
            window.headerTopAtOpen=widget.frame.getBoundingClientRect().top;show();
          };
          window.addEventListener('scroll',()=>{
            if(getComputedStyle(widget.optionsDiv).visibility==='visible')window.openMenuScrolls++;
          },true);
        }''', (FIXTURES / 'public-lesson-header.html').read_text())
        header_bottom = self.page.locator('#header').evaluate('n=>n.getBoundingClientRect().bottom')
        self.assertGreater(header_bottom, 0)
        self.assertEqual(self.page.locator('#header').evaluate("n=>getComputedStyle(n).position"), 'fixed')
        self.assertLess(self.page.locator('.selectListFrame').evaluate('n=>n.getBoundingClientRect().top'), header_bottom)
        enter(self.page.locator('#question'), field, {'value': saved['value']})
        self.assertGreaterEqual(self.page.evaluate('window.headerTopAtOpen'), header_bottom + 2)
        self.assertEqual(self.page.evaluate('widget.getSelectedIndex()'), 8)
        self.assertEqual(self.page.evaluate('window.openMenuScrolls'), 0)

    def test_actual_public_header_insets_nested_scroller_only_when_needed(self):
        for below_header in (False, True):
            with self.subTest(below_header=below_header):
                field, saved = self.scroll_dropdown()
                self.page.set_viewport_size({'width': 1280, 'height': 800})
                self.page.add_style_tag(content=(FIXTURES / 'public-student-lesson.css').read_text())
                self.page.evaluate('''header=>{
                  document.body.insertAdjacentHTML('afterbegin',header);
                  window.windowScrolls=0;window.addEventListener('scroll',e=>{
                    if(e.target===document)window.windowScrolls++;
                  });
                }''', (FIXTURES / 'public-lesson-header.html').read_text())
                if below_header:
                    self.page.locator('#scroll').evaluate("n=>n.style.top=(document.querySelector('#header').getBoundingClientRect().bottom+20)+'px'")
                enter(self.page.locator('#question'), field, {'value': saved['value']})
                self.assertGreaterEqual(self.page.locator('.selectListFrame').evaluate('n=>n.getBoundingClientRect().top'),
                                        self.page.locator('#header').evaluate('n=>n.getBoundingClientRect().bottom') + 2)
                self.assertEqual(self.page.evaluate('window.windowScrolls'), 0)
                self.assertEqual(self.page.evaluate('widget.getSelectedIndex()'), 8)

    def test_header_container_scroll_limit_uses_window_only_for_remaining_inset(self):
        field, saved = self.scroll_dropdown()
        self.page.set_viewport_size({'width': 1280, 'height': 800})
        self.page.add_style_tag(content=(FIXTURES / 'public-student-lesson.css').read_text())
        self.page.evaluate('''header=>{
          document.body.insertAdjacentHTML('afterbegin',header);
          const container=document.querySelector('#scroll');container.style.top='500px';
          container.firstElementChild.remove();document.body.insertAdjacentHTML('beforeend','<div style="height:2000px"></div>');
          window.scrollTo(0,500);
        }''', (FIXTURES / 'public-lesson-header.html').read_text())
        enter(self.page.locator('#question'), field, {'value': saved['value']})
        self.assertEqual(self.page.locator('#scroll').evaluate('n=>n.scrollTop'), 0)
        self.assertGreaterEqual(self.page.locator('.selectListFrame').evaluate('n=>n.getBoundingClientRect().top'),
                                self.page.locator('#header').evaluate('n=>n.getBoundingClientRect().bottom') + 2)
        self.assertEqual(self.page.evaluate('widget.getSelectedIndex()'), 8)

    def test_dropdown_overlay_cannot_trigger_reopen_or_click_through(self):
        field, saved = self.scroll_dropdown()
        self.page.evaluate('''()=>{const original=widget.showOptions.bind(widget);widget.showOptions=()=>{
          original();const r=widget.frame.getBoundingClientRect();const overlay=document.createElement('div');
          overlay.style.cssText=`position:fixed;inset:0;z-index:10000`;document.body.appendChild(overlay);
        }}''')
        with self.assertRaisesRegex(ValueError, 'no exposed'):
            enter(self.page.locator('#question'), field, {'value': saved['value']})
        self.assertEqual(self.page.evaluate('widget.getSelectedIndex()'), 0)
        self.assertLessEqual(self.page.evaluate('window.opens'), 1)

    def test_scroll_dropdown_rejects_changed_frame_readback(self):
        field, saved = self.scroll_dropdown()
        self.page.evaluate("()=>widget.onSelect=()=>widget.frame.textContent='changed source content'")
        with self.assertRaisesRegex(ValueError, 'readback differs'):
            enter(self.page.locator('#question'), field, {'value': saved['value']})

    def test_scroll_dropdown_does_not_reenter_accepted_field(self):
        field, saved = self.scroll_dropdown()
        field['source_result'] = 'Correct'
        self.assertTrue(enter(self.page.locator('#question'), field, {'value': saved['value']})['already_accepted'])
        self.assertEqual(self.page.evaluate('window.opens'), 0)


if __name__ == "__main__":
    unittest.main()
